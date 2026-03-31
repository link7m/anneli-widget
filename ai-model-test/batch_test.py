#!/usr/bin/env python3
"""
Dental Smile AI — Batch Prompt Tester
Tests prompts across multiple input images simultaneously.
Generates an HTML comparison grid so you can spot inconsistencies instantly.

Usage:
  1. Put test images in inputs/ folder (name them descriptively):
     - tight_smile.jpg
     - gummy_smile.jpg
     - crooked_teeth.jpg
     - gaps.jpg
     - stained.jpg

  2. Run:
     python3 batch_test.py --token r8_YOUR_TOKEN

  3. Open batch_results.html in browser
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

# ── PROMPTS TO TEST ──────────────────────────────────────────────────────
# Edit these. Add/remove as needed. Keep the dict key short.

PROMPTS = {
    "s5c_winner": (
        "Redesign the smile area for this person. Perfect dental arch, straight "
        "aligned teeth, natural warm white color. Beautiful smile arc following "
        "lower lip curve. Ideal tooth-to-lip proportion. Comfortable natural "
        "smile width. Even gums, minimal gum show. Realistic tooth texture with "
        "subtle light reflection. Face, skin, eyes, hair, ears, jawline, "
        "background, lighting all stay exactly the same."
    ),
    "s5c_open": (
        "Redesign the smile area for this person with a full confident smile. "
        "Perfect dental arch, straight aligned teeth, natural warm white color. "
        "Upper teeth fully visible, ideal smile width for the face. Even gums, "
        "minimal gum show. Natural relaxed lower lip. Realistic tooth texture "
        "with subtle light reflection. Face, skin, eyes, hair, ears, jawline, "
        "background, lighting all stay exactly the same."
    ),
}

MODEL = "black-forest-labs/flux-kontext-max"

# ── CORE ─────────────────────────────────────────────────────────────────

def get_images():
    imgs = []
    for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp"):
        imgs.extend(INPUT_DIR.glob(ext))
    if not imgs:
        print(f"ERROR: No images in {INPUT_DIR}/")
        print("Add test photos named descriptively: tight_smile.jpg, gummy.jpg, etc.")
        sys.exit(1)
    return sorted(imgs)


def to_data_uri(path):
    ext = path.suffix.lower().lstrip(".")
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}
    with open(path, "rb") as f:
        return f"data:{mime.get(ext, 'image/jpeg')};base64,{base64.b64encode(f.read()).decode()}"


def run_one(model, prompt_name, prompt_text, img_path):
    """Run a single prediction. Returns dict with result info."""
    img_name = img_path.stem
    out_path = OUTPUT_DIR / f"{prompt_name}__{img_name}.jpg"

    if out_path.exists():
        return {"prompt": prompt_name, "image": img_name, "file": str(out_path),
                "success": True, "time": 0, "skipped": True}

    start = time.time()
    try:
        output = replicate.run(model, input={
            "prompt": prompt_text,
            "input_image": to_data_uri(img_path),
            "aspect_ratio": "match_input_image",
            "output_format": "jpg",
            "safety_tolerance": 6,
        })

        url = str(output[0]) if isinstance(output, list) else str(output)
        resp = requests.get(url, timeout=120)
        resp.raise_for_status()
        with open(out_path, "wb") as f:
            f.write(resp.content)

        elapsed = round(time.time() - start, 1)
        return {"prompt": prompt_name, "image": img_name, "file": str(out_path),
                "success": True, "time": elapsed, "skipped": False}

    except Exception as e:
        elapsed = round(time.time() - start, 1)
        return {"prompt": prompt_name, "image": img_name, "file": None,
                "success": False, "time": elapsed, "error": str(e), "skipped": False}


def generate_html(results, images, prompts):
    """Generate comparison HTML grid: rows=images, cols=prompts."""
    img_names = [p.stem for p in images]

    prompt_cols = "".join(f"<th>{p}</th>" for p in prompts)
    rows = ""
    for img in images:
        name = img.stem
        # Input image cell
        cells = f'<td><img src="inputs/{img.name}" alt="{name}"><div class="label">INPUT: {name}</div></td>'
        for pname in prompts:
            r = next((x for x in results if x["image"] == name and x["prompt"] == pname), None)
            if r and r["success"]:
                rel = f"batch_outputs/{pname}__{name}.jpg"
                cells += f'<td><img src="{rel}" alt="{pname}"><div class="label">{pname}</div></td>'
            else:
                err = r["error"][:40] if r else "missing"
                cells += f'<td class="error">{err}</td>'
        rows += f"<tr>{cells}</tr>\n"

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>Smile AI Batch Test</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: system-ui; background: #111; color: #eee; padding: 20px; }}
h1 {{ text-align: center; margin-bottom: 5px; }}
.info {{ text-align: center; color: #888; margin-bottom: 20px; font-size: 14px; }}
table {{ border-collapse: collapse; width: 100%; }}
th {{ background: #222; padding: 10px; font-size: 13px; color: #aaa; border: 1px solid #333;
     position: sticky; top: 0; z-index: 10; }}
td {{ border: 1px solid #333; padding: 4px; vertical-align: top; position: relative; }}
td img {{ width: 100%; display: block; border-radius: 4px; }}
.label {{ position: absolute; bottom: 8px; left: 8px; background: rgba(0,0,0,0.8);
         padding: 2px 8px; border-radius: 4px; font-size: 11px; color: #ccc; }}
.error {{ background: #1a0000; color: #f66; text-align: center; padding: 20px; font-size: 12px; }}
tr:hover td {{ outline: 2px solid #2563eb; }}
</style></head>
<body>
<h1>Smile AI — Batch Comparison</h1>
<p class="info">Model: {MODEL} | {len(images)} images x {len(prompts)} prompts | {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
<table>
<tr><th>Input</th>{prompt_cols}</tr>
{rows}
</table>
</body></html>"""

    out = DIR / "batch_results.html"
    with open(out, "w") as f:
        f.write(html)
    print(f"\nComparison grid: {out}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", help="Replicate API token")
    parser.add_argument("--model", default=MODEL, help="Model to use")
    parser.add_argument("--parallel", type=int, default=2, help="Parallel requests (default 2)")
    args = parser.parse_args()

    if args.token:
        os.environ["REPLICATE_API_TOKEN"] = args.token
    if not os.environ.get("REPLICATE_API_TOKEN"):
        print("ERROR: Set REPLICATE_API_TOKEN or use --token")
        sys.exit(1)

    images = get_images()
    prompt_names = list(PROMPTS.keys())
    total = len(images) * len(PROMPTS)

    print(f"Model: {args.model}")
    print(f"Images: {len(images)} | Prompts: {len(PROMPTS)} | Total: {total}")
    print(f"Parallel: {args.parallel}")
    print("-" * 60)

    results = []
    done = 0

    with ThreadPoolExecutor(max_workers=args.parallel) as pool:
        futures = {}
        for pname, ptext in PROMPTS.items():
            for img in images:
                f = pool.submit(run_one, args.model, pname, ptext, img)
                futures[f] = (pname, img.stem)

        for f in as_completed(futures):
            r = f.result()
            done += 1
            status = "SKIP" if r.get("skipped") else ("OK" if r["success"] else "FAIL")
            t = f"{r['time']}s" if r['time'] else ""
            print(f"[{done}/{total}] {r['prompt']} / {r['image']} — {status} {t}")
            results.append(r)

    # Save raw results
    with open(DIR / "batch_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # Generate HTML
    generate_html(results, images, prompt_names)

    ok = sum(1 for r in results if r["success"])
    print(f"\nDone: {ok}/{total} successful")
    print("Open batch_results.html in browser to compare")


if __name__ == "__main__":
    main()
