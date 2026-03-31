# Dental Veneer AI Model — Research & Recommendations

## Models Evaluated

### 1. `black-forest-labs/flux-kontext-pro` ⭐ RECOMMENDED
- **Type:** Instruction-based image editing (no mask needed)
- **Cost:** ~$0.05/image
- **Speed:** ~10-20s
- **Why it's best:**
  - Purpose-built for "edit this specific thing" tasks via natural language
  - Preserves face identity extremely well (it's an edit model, not generation)
  - No mask/segmentation needed — just describe what to change
  - Already battle-tested in your current Worker
  - Best price/quality ratio for this use case

### 2. `black-forest-labs/flux-kontext-max`
- **Type:** Premium version of kontext-pro
- **Cost:** ~$0.10/image (2x kontext-pro)
- **Speed:** ~15-30s
- **When to use:** If kontext-pro results aren't detailed enough. The "max" version has better fine detail handling which could matter for individual tooth rendering.
- **Trade-off:** 2x cost for incremental improvement

### 3. `ideogram-ai/ideogram-v3-quality` (inpainting mode)
- **Type:** Inpainting with mask
- **Complexity:** HIGH — requires teeth segmentation mask
- **Why NOT recommended:** You'd need to either manually create masks or add a teeth segmentation step (MediaPipe Face Mesh or similar), adding latency and failure points. Not worth it when kontext-pro handles instruction-based editing well.

### 4. `bria/genfill`
- **Type:** Mask-based inpainting
- **Same issue as ideogram:** Requires a teeth mask, adding pipeline complexity.

### 5. `google/nano-banana-pro`
- **Type:** Instruction-based editing (newer)
- **Worth testing:** Similar approach to kontext — instruction-based, no mask needed.
- **Status:** Newer model, less battle-tested.

---

## Best Prompts (Ranked by Expected Quality)

### 🥇 P3 — Veneer-Specific (RECOMMENDED)
```
Edit only the teeth to look like high-quality porcelain dental veneers were applied.
Teeth should be naturally white (shade B1), evenly shaped, and properly aligned.
Maintain the original tooth proportions and gumline. Do not alter the face, lips,
skin, lighting, or background in any way.
```
**Why:** Uses dental terminology ("shade B1", "gumline") which grounds the model in realistic results. Explicitly names veneers so the model has a clear reference point.

### 🥈 P4 — Dentist Language
```
Apply a cosmetic dental transformation to the teeth only: correct alignment,
close any gaps, even out tooth sizes, and whiten to a natural shade (not
Hollywood white). Preserve the person's natural lip shape, facial features,
skin tone, and the exact same background. The smile should look professionally
done but believable.
```
**Why:** Very specific about what to fix (alignment, gaps, sizes, color). The "not Hollywood white" instruction is key.

### 🥉 P1 — Current Production Prompt
```
Whiten and straighten the teeth moderately. Keep the exact same tooth size and
shape. Align the dental midline so upper and lower teeth centerlines match.
Natural white color, not bright white. Keep some natural irregularities and
slight imperfections. Do not touch anything else on the face.
```
**Why:** Good baseline, but "keep some irregularities" might confuse the model — it's being told to both fix AND keep imperfections.

### P5 — Before/After Framing
```
This is a before photo of a dental patient. Transform it into the after photo
showing results of premium porcelain veneer treatment...
```
**Why:** Framing as "before/after" gives the model strong context. Worth testing.

### P2 — Minimal (backup)
```
Make the teeth slightly whiter and more aligned...
```
**Why:** Most conservative. Good for subtle changes but might under-deliver.

---

## Recommendation Summary

| Aspect | Recommendation |
|--------|---------------|
| **Model** | `flux-kontext-pro` (upgrade to `flux-kontext-max` only if detail is insufficient) |
| **Prompt** | P3 (veneer-specific) or P4 (dentist language) |
| **Preprocessing** | Compress to 640px max, JPEG 80% quality (your current approach is fine) |
| **Parameters** | `aspect_ratio: match_input_image`, `output_format: jpg`, `safety_tolerance: 6` |

## How to Run Tests

```bash
# Quick: test all prompts on 1 image with kontext-pro
python3 test_models.py --token r8_YOUR_TOKEN --models flux-kontext-pro --images smile1

# Full: test everything
./run_tests.sh r8_YOUR_TOKEN

# View results
# Open compare.html in browser (it auto-loads results.json)
```

## Key Insight: Why Instruction-Based > Inpainting for This Use Case

Inpainting models (ideogram, bria/genfill) require a binary mask isolating the teeth.
This means you'd need:
1. A teeth segmentation model (MediaPipe, SAM, or custom)
2. Mask generation pipeline
3. Two API calls instead of one
4. More failure modes (bad mask → bad result)

Instruction-based models (flux-kontext) skip all of this — you just say "change the teeth"
and the model figures out where they are. For a lead magnet widget where speed and
reliability matter more than pixel-perfect control, this is the right trade-off.
