#!/bin/bash
# Dental Veneer AI Model Test Runner
# Usage: ./run_tests.sh [your-replicate-token]
#
# Or set the token first:
#   export REPLICATE_API_TOKEN=r8_...
#   ./run_tests.sh

set -e
cd "$(dirname "$0")"

TOKEN_ARG=""
if [ -n "$1" ]; then
    TOKEN_ARG="--token $1"
fi

echo "=== Step 1: Download test images ==="
python3 download_test_images.py

echo ""
echo "=== Step 2: Run flux-kontext-pro (current model, all prompts, 1 image) ==="
echo "Quick test to find best prompt..."
python3 test_models.py --models flux-kontext-pro --images smile1 $TOKEN_ARG

echo ""
echo "=== Step 3: Run best prompts on flux-kontext-max ==="
echo "Testing premium model..."
python3 test_models.py --models flux-kontext-max --images smile1 $TOKEN_ARG

echo ""
echo "=== Step 4: Run winning combos on all images ==="
echo "Testing consistency across photos..."
python3 test_models.py --images smile1 smile2 smile3 $TOKEN_ARG

echo ""
echo "=== DONE ==="
echo "Open compare.html in a browser to view results side-by-side."
echo "Results data: results.json"
