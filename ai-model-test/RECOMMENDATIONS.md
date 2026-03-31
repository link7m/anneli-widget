# Dental Veneer AI Model — Research & Recommendations

## The #1 Rule: Don't Scare the Lead

This is a **lead magnet**, not a medical tool. The goal is:
- Person sees result and thinks **"oh nice, I'd want that"**
- NOT "holy shit that's not me" or "that looks fake"

**Subtle > Dramatic.** A lead who thinks the result is achievable will book.
A lead who thinks it looks fake will bounce.

---

## Models Evaluated

### 1. `black-forest-labs/flux-kontext-pro` — RECOMMENDED
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
- **When to use:** If kontext-pro results aren't detailed enough on teeth detail.
- **Trade-off:** 2x cost for incremental improvement. Test before committing.

### 3. Inpainting models (ideogram, bria/genfill) — NOT recommended
- Require a teeth segmentation mask (extra pipeline, extra failure modes)
- Overkill for a lead magnet widget

---

## Prompts — Ranked for Lead Conversion (Subtle + Natural)

### P4 "Warm Natural" — TOP PICK for lead magnets
```
Gently whiten the teeth to a warm, natural shade and slightly improve
alignment. Keep the teeth looking real — maintain natural size differences
and organic shapes. The change should be subtle enough that someone might
think 'you look great today' rather than 'you got your teeth done.'
Do not touch anything else in the photo.
```
**Why best for leads:** The "you look great today" framing literally tells the model
to aim for subtle. Warm white avoids the fake blue-white look. Keeps natural
variations so the person still recognizes their own smile.

### P3 "Gentle Veneer" — Runner-up
```
Subtly improve the teeth to look like natural, high-quality dental veneers.
Use a warm, natural white — not bright or artificial. Keep the original tooth
proportions and slight natural variations between teeth. The result should
look believable, like this person just had great dental work done. Do not
alter the face, lips, skin, lighting, or background.
```
**Why good:** "Believable" and "great dental work" are the right anchors.
Mentions veneers which gives the model a clear reference.

### P5 "Professional Clean" — Safe backup
```
Make the teeth look like the person just had a professional dental cleaning
and minor cosmetic improvements. Slightly whiter, slightly straighter, any
gaps reduced. Keep the natural warmth of the tooth color — avoid any blue-white
or artificial look. Maintain the exact same face, lips, skin tone, and expression.
The improvement should be noticeable but not dramatic.
```
**Why:** "Professional cleaning" is the most conservative framing. Good for
people whose teeth are already decent — won't over-edit.

### P2 "Subtle Healthy" — Ultra-conservative
```
Make the teeth look clean, healthy, and well-cared-for. Slightly whiter and
slightly more even, but keep the natural tooth shapes and sizes. The smile
should still look like the same person — just with better dental hygiene.
Do not change the face, lips, skin, or anything else.
```
**Why:** Most subtle option. "Better dental hygiene" framing = minimal changes.
Might under-deliver for people with very crooked teeth.

### P1 "Current Production" — Baseline
```
Whiten and straighten the teeth moderately. Keep the exact same tooth size and
shape. Align the dental midline so upper and lower teeth centerlines match.
Natural white color, not bright white. Keep some natural irregularities and
slight imperfections. Do not touch anything else on the face.
```
**Issue:** "Keep irregularities" contradicts "straighten." Mixed signals to the model.

---

## How to Test

```bash
# 1. Add your test photos to ai-model-test/inputs/ (or use the sample downloader)
python3 download_test_images.py

# 2. Quick test: all prompts on 1 image
python3 test_models.py --token r8_YOUR_TOKEN --models flux-kontext-pro --images smile1

# 3. Compare results in browser
# Open compare.html — it loads results.json automatically

# 4. Once you pick a winner prompt, test on all images for consistency
python3 test_models.py --token r8_YOUR_TOKEN --prompts p4_warm_natural --images smile1 smile2 smile3

# 5. Optional: test kontext-max with winner prompt
python3 test_models.py --token r8_YOUR_TOKEN --models flux-kontext-max --prompts p4_warm_natural
```

## What to Look For When Comparing

When reviewing outputs, check:
1. **Does it still look like the same person?** (face identity preserved)
2. **Are the teeth believably white?** (warm white, not bleach/blue)
3. **Do the teeth still look natural?** (slight variations, not perfect chiclets)
4. **Are the lips unchanged?** (common failure: model reshapes lips)
5. **Would YOU book a dentist appointment from this?** (the real test)

## Recommendation Summary

| Aspect | Recommendation |
|--------|---------------|
| **Model** | `flux-kontext-pro` (try `max` only if detail is lacking) |
| **Prompt** | P4 "warm natural" (subtle, lead-friendly) |
| **Preprocessing** | Compress to 640px max, JPEG 80% (current approach is fine) |
| **Parameters** | `aspect_ratio: match_input_image`, `output_format: jpg`, `safety_tolerance: 6` |
