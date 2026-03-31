#!/usr/bin/env python3
"""
Dental Veneer AI Model Tester
Tests multiple Replicate models + prompts for teeth whitening/straightening.
Saves all outputs for side-by-side comparison.
"""

import replicate
import requests
import base64
import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# ── Config ──────────────────────────────────────────────────────────────────

OUTPUT_DIR = Path(__file__).parent / "outputs"
INPUT_DIR = Path(__file__).parent / "inputs"
RESULTS_FILE = Path(__file__).parent / "results.json"

# ── Models to test ──────────────────────────────────────────────────────────

MODELS = {
    "flux-kontext-pro": {
        "id": "black-forest-labs/flux-kontext-pro",
        "type": "instruction",  # text-guided editing, no mask needed
        "base_params": {
            "aspect_ratio": "match_input_image",
            "output_format": "jpg",
            "safety_tolerance": 6,
        },
    },
    "flux-kontext-max": {
        "id": "black-forest-labs/flux-kontext-max",
        "type": "instruction",
        "base_params": {
            "aspect_ratio": "match_input_image",
            "output_format": "jpg",
            "safety_tolerance": 6,
        },
    },
}

# ── Prompts to test ─────────────────────────────────────────────────────────
# Each prompt targets a different strategy for natural-looking veneer results

PROMPTS = {
    "p1_current": (
        "Whiten and straighten the teeth moderately. Keep the exact same tooth size "
        "and shape. Align the dental midline so upper and lower teeth centerlines match. "
        "Natural white color, not bright white. Keep some natural irregularities and "
        "slight imperfections. Do not touch anything else on the face."
    ),
    "p2_minimal": (
        "Make the teeth slightly whiter and more aligned. Keep everything else in the "
        "photo exactly the same. The result should look like a natural, healthy smile — "
        "not cosmetically perfect."
    ),
    "p3_veneer_specific": (
        "Edit only the teeth to look like high-quality porcelain dental veneers were "
        "applied. Teeth should be naturally white (shade B1), evenly shaped, and properly "
        "aligned. Maintain the original tooth proportions and gumline. Do not alter the "
        "face, lips, skin, lighting, or background in any way."
    ),
    "p4_dentist_language": (
        "Apply a cosmetic dental transformation to the teeth only: correct alignment, "
        "close any gaps, even out tooth sizes, and whiten to a natural shade (not "
        "Hollywood white). Preserve the person's natural lip shape, facial features, "
        "skin tone, and the exact same background. The smile should look professionally "
        "done but believable."
    ),
    "p5_before_after": (
        "This is a before photo of a dental patient. Transform it into the after photo "
        "showing results of premium porcelain veneer treatment. The teeth should be "
        "straight, uniform, and a natural white color. Everything else — face shape, "
        "skin, lips, hair, background, lighting — must remain completely identical."
    ),
}

# ── Helpers ──────────────────────────────────────────────────────────────────


def get_test_images():
    """Get all test images from the inputs directory."""
    images = []
    for ext in ["*.jpg", "*.jpeg", "*.png", "*.webp"]:
        images.extend(INPUT_DIR.glob(ext))
    if not images:
        print("ERROR: No test images found in ai-model-test/inputs/")
        print("Please add 1-3 selfie photos with visible teeth to that directory.")
        sys.exit(1)
    return sorted(images)


def image_to_data_uri(path: Path) -> str:
    """Convert image file to data URI for Replicate API."""
    ext = path.suffix.lower()
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}
    mime_type = mime.get(ext.lstrip("."), "image/jpeg")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{mime_type};base64,{b64}"


def download_output(url: str, save_path: Path) -> bool:
    """Download result image from Replicate URL."""
    try:
        resp = requests.get(url, timeout=120)
        resp.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(resp.content)
        return True
    except Exception as e:
        print(f"  ERROR downloading: {e}")
        return False


def run_prediction(model_id: str, input_params: dict) -> dict:
    """Run a Replicate prediction and return the result."""
    start = time.time()
    try:
        output = replicate.run(model_id, input=input_params)
        elapsed = time.time() - start

        # Handle different output formats
        if isinstance(output, str):
            url = output
        elif hasattr(output, "url"):
            url = output.url
        elif isinstance(output, list) and len(output) > 0:
            url = str(output[0])
        else:
            url = str(output)

        return {"success": True, "url": url, "time_seconds": round(elapsed, 1)}
    except Exception as e:
        elapsed = time.time() - start
        return {"success": False, "error": str(e), "time_seconds": round(elapsed, 1)}


# ── Main test runner ────────────────────────────────────────────────────────


def run_tests(models_filter=None, prompts_filter=None, images_filter=None):
    """Run all model x prompt x image combinations."""
    test_images = get_test_images()
    results = []

    # Apply filters
    models_to_test = MODELS
    if models_filter:
        models_to_test = {k: v for k, v in MODELS.items() if k in models_filter}

    prompts_to_test = PROMPTS
    if prompts_filter:
        prompts_to_test = {k: v for k, v in PROMPTS.items() if k in prompts_filter}

    if images_filter:
        test_images = [img for img in test_images if img.stem in images_filter]

    total = len(models_to_test) * len(prompts_to_test) * len(test_images)
    current = 0

    print(f"\n{'='*70}")
    print(f"DENTAL VENEER AI MODEL TEST")
    print(f"Models: {len(models_to_test)} | Prompts: {len(prompts_to_test)} | Images: {len(test_images)}")
    print(f"Total predictions: {total}")
    print(f"{'='*70}\n")

    for model_name, model_config in models_to_test.items():
        model_dir = OUTPUT_DIR / model_name
        model_dir.mkdir(parents=True, exist_ok=True)

        for prompt_name, prompt_text in prompts_to_test.items():
            for img_path in test_images:
                current += 1
                img_name = img_path.stem
                output_filename = f"{img_name}__{prompt_name}.jpg"
                output_path = model_dir / output_filename

                # Skip if already exists
                if output_path.exists():
                    print(f"[{current}/{total}] SKIP (exists): {model_name} / {prompt_name} / {img_name}")
                    continue

                print(f"[{current}/{total}] {model_name} / {prompt_name} / {img_name}")

                # Build input params
                data_uri = image_to_data_uri(img_path)
                input_params = {
                    "prompt": prompt_text,
                    "input_image": data_uri,
                    **model_config["base_params"],
                }

                # Run prediction
                result = run_prediction(model_config["id"], input_params)

                if result["success"]:
                    downloaded = download_output(result["url"], output_path)
                    print(f"  ✓ Done in {result['time_seconds']}s → {output_path.name}")
                else:
                    downloaded = False
                    print(f"  ✗ Failed in {result['time_seconds']}s: {result['error']}")

                # Record result
                results.append({
                    "model": model_name,
                    "model_id": model_config["id"],
                    "prompt_name": prompt_name,
                    "prompt_text": prompt_text,
                    "input_image": img_name,
                    "output_file": str(output_path) if downloaded else None,
                    "success": result["success"] and downloaded,
                    "time_seconds": result["time_seconds"],
                    "error": result.get("error"),
                    "timestamp": datetime.now().isoformat(),
                })

                # Save results incrementally
                save_results(results)

    print(f"\n{'='*70}")
    print(f"COMPLETE — {sum(1 for r in results if r['success'])}/{len(results)} successful")
    print(f"Results saved to: {RESULTS_FILE}")
    print(f"Outputs saved to: {OUTPUT_DIR}/")
    print(f"{'='*70}\n")

    print_summary(results)
    return results


def save_results(results):
    """Save results to JSON file."""
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)


def print_summary(results):
    """Print a comparison summary."""
    print("\n── SUMMARY ────────────────────────────────────────────────────────────")
    print(f"\n{'Model':<22} {'Prompt':<22} {'Image':<15} {'Time':>6} {'Status'}")
    print("-" * 80)
    for r in results:
        status = "✓" if r["success"] else f"✗ {r.get('error', '')[:30]}"
        print(f"{r['model']:<22} {r['prompt_name']:<22} {r['input_image']:<15} {r['time_seconds']:>5.1f}s {status}")

    # Average time per model
    print("\n── AVERAGE TIME PER MODEL ─────────────────────────────────────────────")
    from collections import defaultdict
    model_times = defaultdict(list)
    for r in results:
        if r["success"]:
            model_times[r["model"]].append(r["time_seconds"])
    for model, times in sorted(model_times.items()):
        avg = sum(times) / len(times)
        print(f"  {model:<25} avg: {avg:.1f}s  (n={len(times)})")


# ── CLI ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test AI models for dental veneer simulation")
    parser.add_argument("--models", nargs="+", help="Filter: model names to test")
    parser.add_argument("--prompts", nargs="+", help="Filter: prompt names to test")
    parser.add_argument("--images", nargs="+", help="Filter: image stems to test")
    parser.add_argument("--list", action="store_true", help="List available models and prompts")
    parser.add_argument("--token", help="Replicate API token (or set REPLICATE_API_TOKEN env var)")

    args = parser.parse_args()

    # Set token if provided via CLI
    if args.token:
        os.environ["REPLICATE_API_TOKEN"] = args.token

    # Check token is available
    if not os.environ.get("REPLICATE_API_TOKEN"):
        print("ERROR: No Replicate API token found.")
        print("Set it via: export REPLICATE_API_TOKEN=r8_...")
        print("Or pass:    python3 test_models.py --token r8_...")
        sys.exit(1)

    if args.list:
        print("\nModels:")
        for k in MODELS:
            print(f"  {k} → {MODELS[k]['id']}")
        print("\nPrompts:")
        for k, v in PROMPTS.items():
            print(f"  {k}: {v[:80]}...")
        sys.exit(0)

    run_tests(
        models_filter=args.models,
        prompts_filter=args.prompts,
        images_filter=args.images,
    )
