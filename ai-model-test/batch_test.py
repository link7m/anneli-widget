#!/usr/bin/env python3
"""
Dental Smile AI — Multi-Model Batch Tester
Tests multiple models AND prompts across multiple input images.
Generates HTML comparison grid: rows=images, cols=model+prompt combos.

Usage:
  1. Put test images in inputs/ folder
  2. python3 batch_test.py --token r8_YOUR_TOKEN
  3. Open batch_results.html in browser

  Filter: --only kontext_s5c,smile_correct,seededit
  Speed:  --parallel 3
"""

import replicate
import requests
import base64
import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

DIR = Path(__file__).parent
INPUT_DIR = DIR / "inputs"
OUTPUT_DIR = DIR / "batch_outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════
# TEST CONFIGS — each entry = one column in the comparison grid
# ══════════════════════════════════════════════════════════════════════════

TESTS = {

    # ── FLUX KONTEXT MAX ─────────────────────────────────────────────────
    "kontext_s5c": {
        "model": "black-forest-labs/flux-kontext-max",
        "input": lambda img_uri: {
            "prompt": (
                "Redesign the smile area for this person. Perfect dental arch, "
                "straight aligned teeth, natural warm white color. Beautiful smile "
                "arc following lower lip curve. Ideal tooth-to-lip proportion. "
                "Comfortable natural smile width. Even gums, minimal gum show. "
                "Realistic tooth texture with subtle light reflection. Face, skin, "
                "eyes, hair, ears, jawline, background, lighting all stay exactly the same."
            ),
            "input_image": img_uri,
            "aspect_ratio": "match_input_image",
            "output_format": "jpg",
            "safety_tolerance": 6,
        },
    },

    "kontext_confident": {
        "model": "black-forest-labs/flux-kontext-max",
        "input": lambda img_uri: {
            "prompt": (
                "Redesign the smile area for this person with a confident beautiful "
                "smile. Perfect dental arch, straight aligned teeth, natural warm "
                "white color. Upper teeth fully visible with ideal smile width for "
                "the face. Even gums, minimal gum show. Realistic tooth texture "
                "with subtle light reflection. Face, skin, eyes, hair, ears, jawline, "
                "background, lighting all stay exactly the same."
            ),
            "input_image": img_uri,
            "aspect_ratio": "match_input_image",
            "output_format": "jpg",
            "safety_tolerance": 6,
        },
    },

    "kontext_pro_s5c": {
        "model": "black-forest-labs/flux-kontext-pro",
        "input": lambda img_uri: {
            "prompt": (
                "Redesign the smile area for this person. Perfect dental arch, "
                "straight aligned teeth, natural warm white color. Beautiful smile "
                "arc following lower lip curve. Ideal tooth-to-lip proportion. "
                "Comfortable natural smile width. Even gums, minimal gum show. "
                "Realistic tooth texture with subtle light reflection. Face, skin, "
                "eyes, hair, ears, jawline, background, lighting all stay exactly the same."
            ),
            "input_image": img_uri,
            "aspect_ratio": "match_input_image",
            "output_format": "jpg",
            "safety_tolerance": 6,
        },
    },

    # ── SMILE-CORRECT (SD + LoRA) ────────────────────────────────────────
    "smile_correct": {
        "model": "sourav-sarkar-doc32/smile-correct",
        "input": lambda img_uri: {
            "image": img_uri,
            "num_outputs": 1,
            "prompt": (
                "photo of perfectsmile smile <lora:lora_perfectsmile_v1_from_v1_160:1>"
                "(Beautiful natural teeth, aligned bite teeth), aligned white teeth, "
                "human like teeth, (no teeth gap), celebrity-like teeth, healthy teeth "
                "with a perfect smile, not big incisor, good proportion teeth, "
                "good proportion smile,"
            ),
            "negative_prompt": (
                "(deformed teeth, semi-realistic, cgi, 3d, render, sketch, cartoon, "
                "drawing, anime), (deformed, distorted, abnormal teeth:1.3, "
                "disfigured:1.3, large teeth:2), poorly drawn, bad anatomy, rabbit "
                "teeth, wrong anatomy, missing teeth, disconnected teeth, unnatural "
                "mouth, bunny teeth, big incisor teeth, disproportionate front teeth, "
                "bad smile, reflection, crooked teeth, distorted teeth, cropped, "
                "out of frame, worst quality, low quality, jpeg artifacts, ugly, "
                "morbid, disfigured, gross proportions, too many teeth, lipstick, "
                "lip gloss, too less teeth, unnatural size teeth, poorly drawn mouth, "
                "poorly drawn teeth"
            ),
        },
    },

    # ── SEEDEDIT 3.0 (ByteDance) ─────────────────────────────────────────
    "seededit": {
        "model": "bytedance/seededit-3.0",
        "input": lambda img_uri: {
            "image": img_uri,
            "prompt": (
                "Redesign the smile with perfect straight aligned teeth, natural "
                "warm white color, beautiful smile arc, minimal gum show, realistic "
                "tooth texture"
            ),
        },
    },

    "seededit_v2": {
        "model": "bytedance/seededit-3.0",
        "input": lambda img_uri: {
            "image": img_uri,
            "prompt": (
                "Perfect beautiful smile with straight white teeth, natural "
                "proportions, even gums, realistic enamel texture"
            ),
        },
    },

    # ── P-IMAGE-EDIT (Pruna AI — sub-1-second) ───────────────────────────
    "p_image_edit": {
        "model": "prunaai/p-image-edit",
        "input": lambda img_uri: {
            "image": img_uri,
            "prompt": (
                "Perfect smile with straight aligned teeth, natural warm white "
                "color, beautiful proportions, realistic tooth texture, even gumline"
            ),
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════


def get_images():
    imgs = []
    for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp"):
        imgs.extend(INPUT_DIR.glob(ext))
    if not imgs:
        print(f"ERROR: No images in {INPUT_DIR}/")
        print("Add test photos: tight_smile.jpg, gummy.jpg, crooked.jpg, etc.")
        sys.exit(1)
    return sorted(imgs)


def to_data_uri(path):
    ext = path.suffix.lower().lstrip(".")
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}
    with open(path, "rb") as f:
        return f"data:{mime.get(ext, 'image/jpeg')};base64,{base64.b64encode(f.read()).decode()}"


def run_one(test_name, test_config, img_path):
    """Run a single prediction. Returns dict with result info."""
    img_name = img_path.stem
    out_path = OUTPUT_DIR / f"{test_name}__{img_name}.jpg"

    if out_path.exists():
        return {"test": test_name, "model": test_config["model"], "image": img_name,
                "file": str(out_path), "success": True, "time": 0, "skipped": True}

    data_uri = to_data_uri(img_path)
    input_params = test_config["input"](data_uri)

    start = time.time()
    try:
        output = replicate.run(test_config["model"], input=input_params)

        # Handle different output formats
        if isinstance(output, str):
            url = output
        elif isinstance(output, list):
            url = str(output[0])
        elif hasattr(output, "url"):
            url = output.url
        else:
            url = str(output)

        resp = requests.get(url, timeout=120)
        resp.raise_for_status()
        with open(out_path, "wb") as f:
            f.write(resp.content)

        elapsed = round(time.time() - start, 1)
        return {"test": test_name, "model": test_config["model"], "image": img_name,
                "file": str(out_path), "success": True, "time": elapsed, "skipped": False}

    except Exception as e:
        elapsed = round(time.time() - start, 1)
        return {"test": test_name, "model": test_config["model"], "image": img_name,
                "file": None, "success": False, "time": elapsed, "error": str(e), "skipped": False}


def generate_html(results, images, test_names):
    """Generate comparison HTML grid: rows=images, cols=tests."""
    cols = "".join(
        f'<th><span class="model">{TESTS[t]["model"].split("/")[-1]}</span><br>{t}</th>'
        for t in test_names
    )

    rows = ""
    for img in images:
        name = img.stem
        cells = f'<td class="input-cell"><img src="inputs/{img.name}" alt="{name}"><div class="label">INPUT: {name}</div></td>'
        for tname in test_names:
            r = next((x for x in results if x["image"] == name and x["test"] == tname), None)
            if r and r["success"]:
                rel = f"batch_outputs/{tname}__{name}.jpg"
                t = f" ({r['time']}s)" if r["time"] else ""
                cells += f'<td><img src="{rel}" alt="{tname}"><div class="label">{tname}{t}</div></td>'
            elif r:
                err = r.get("error", "unknown")[:50]
                cells += f'<td class="error">{err}</td>'
            else:
                cells += '<td class="error">not run</td>'
        rows += f"<tr>{cells}</tr>\n"

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>Smile AI — Multi-Model Comparison</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: system-ui; background: #111; color: #eee; padding: 20px; }}
h1 {{ text-align: center; margin-bottom: 5px; }}
.info {{ text-align: center; color: #888; margin-bottom: 20px; font-size: 14px; }}
table {{ border-collapse: collapse; width: 100%; table-layout: fixed; }}
th {{ background: #222; padding: 10px 6px; font-size: 12px; color: #aaa; border: 1px solid #333;
     position: sticky; top: 0; z-index: 10; text-align: center; }}
th .model {{ color: #60a5fa; font-size: 11px; }}
td {{ border: 1px solid #333; padding: 3px; vertical-align: top; position: relative; }}
td img {{ width: 100%; display: block; border-radius: 4px; cursor: zoom-in; }}
td img:active {{ position: fixed; top: 5vh; left: 5vw; width: 90vw; height: 90vh;
               object-fit: contain; z-index: 100; background: #000; border-radius: 0; }}
.input-cell {{ background: #1a1a2e; }}
.label {{ position: absolute; bottom: 6px; left: 6px; background: rgba(0,0,0,0.85);
         padding: 2px 6px; border-radius: 4px; font-size: 10px; color: #ccc; }}
.error {{ background: #1a0000; color: #f66; text-align: center; padding: 20px; font-size: 11px; }}
tr:hover td {{ outline: 2px solid #2563eb; }}
</style></head>
<body>
<h1>Smile AI — Multi-Model Comparison</h1>
<p class="info">{len(test_names)} tests x {len(images)} images | {datetime.now().strftime('%Y-%m-%d %H:%M')} | Click image to zoom</p>
<table>
<tr><th style="width:150px">Input</th>{cols}</tr>
{rows}
</table>
</body></html>"""

    out = DIR / "batch_results.html"
    with open(out, "w") as f:
        f.write(html)
    print(f"\nComparison grid: {out}")


def main():
    parser = argparse.ArgumentParser(description="Multi-model dental smile AI batch tester")
    parser.add_argument("--token", help="Replicate API token")
    parser.add_argument("--only", help="Comma-separated test names to run (default: all)")
    parser.add_argument("--parallel", type=int, default=2, help="Parallel requests (default 2)")
    parser.add_argument("--list", action="store_true", help="List available tests")
    args = parser.parse_args()

    if args.list:
        print("\nAvailable tests:")
        for name, cfg in TESTS.items():
            print(f"  {name:25s} → {cfg['model']}")
        sys.exit(0)

    if args.token:
        os.environ["REPLICATE_API_TOKEN"] = args.token
    if not os.environ.get("REPLICATE_API_TOKEN"):
        print("ERROR: Set REPLICATE_API_TOKEN or use --token")
        sys.exit(1)

    # Filter tests
    tests = TESTS
    if args.only:
        names = [n.strip() for n in args.only.split(",")]
        tests = {k: v for k, v in TESTS.items() if k in names}
        if not tests:
            print(f"ERROR: No matching tests. Available: {', '.join(TESTS.keys())}")
            sys.exit(1)

    images = get_images()
    test_names = list(tests.keys())
    total = len(images) * len(tests)

    print(f"Tests: {len(tests)} | Images: {len(images)} | Total runs: {total}")
    print(f"Parallel: {args.parallel}")
    for name, cfg in tests.items():
        print(f"  {name} → {cfg['model']}")
    print("-" * 60)

    results = []
    done = 0

    with ThreadPoolExecutor(max_workers=args.parallel) as pool:
        futures = {}
        for tname, tcfg in tests.items():
            for img in images:
                f = pool.submit(run_one, tname, tcfg, img)
                futures[f] = (tname, img.stem)

        for f in as_completed(futures):
            r = f.result()
            done += 1
            status = "SKIP" if r.get("skipped") else ("OK" if r["success"] else "FAIL")
            t = f" {r['time']}s" if r["time"] else ""
            print(f"[{done}/{total}] {r['test']} / {r['image']} — {status}{t}")
            results.append(r)

    with open(DIR / "batch_results.json", "w") as f:
        json.dump(results, f, indent=2)

    generate_html(results, images, test_names)

    ok = sum(1 for r in results if r["success"])
    failed = [r for r in results if not r["success"] and not r.get("skipped")]
    print(f"\nDone: {ok}/{total} successful")
    if failed:
        print("\nFailed:")
        for r in failed:
            print(f"  {r['test']} / {r['image']}: {r.get('error', '?')[:60]}")
    print("\nOpen batch_results.html in browser to compare")


if __name__ == "__main__":
    main()
