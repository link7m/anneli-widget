# 2ndLove — Full Website Context & Antigravity Prompt

---

## 1. BRAND IDENTITY

**Brand name:** 2ndLove
**Logo treatment:** "2nd" in gold, "Love" in charcoal. Serif font (Cormorant Garamond), weight 600.
**Tagline:** "Where fine pieces find a new story"
**Business:** Curated luxury second-hand boutique in Tampere, Finland. Physical store at Hämeenpuisto 27b.
**Positioning:** Not a thrift shop. Not a consignment warehouse. A boutique experience — every piece is authenticated, hand-selected, and beautifully presented. Think The Row meets vintage Parisian consignment.

---

## 2. BRAND BOOK — COLORS

```
--gold:        #C9A84C    (primary accent, CTAs, highlights, decorative lines)
--gold-light:  #D4B96A    (hover states, secondary accent)
--dusty-rose:  #EDD5C8    (section backgrounds, warmth)
--champagne:   #F5EDD8    (primary background, hero)
--charcoal:    #1F1F1F    (primary text, dark sections, footer)
--stone:       #8C8C8C    (secondary text, muted labels)
--warm-white:  #FEFCF8    (card backgrounds, modal backgrounds, light text on dark)
```

**Color philosophy:** Warm neutrals. No pure white, no pure black. Everything feels like candlelight on linen. Gold is used sparingly for luxury signaling — never overwhelming.

---

## 3. BRAND BOOK — TYPOGRAPHY

**Headings:** Cormorant Garamond (Google Fonts)
- Weights: 400 (body italic), 500 (subheadings), 600 (main headings), 700 (rare emphasis)
- Italic used for taglines and editorial quotes
- Line-height: 1.2

**Body:** DM Sans (Google Fonts)
- Weights: 300 (light captions), 400 (body), 500 (medium), 600 (buttons, labels, badges)
- Line-height: 1.6–1.8
- Letter-spacing: 2–3px on uppercase labels/buttons

**Font loading:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
```

---

## 4. DESIGN LANGUAGE & STYLE REFERENCE

**Style:** Modern warm minimalism. Clean, generous whitespace, editorial feel.
**Reference:** https://en.relove.fi/page/123/sell-with-us — similar tone: luxury second-hand, clean layout, warm palette, trust-building copy. BUT: 2ndLove should feel more premium and less marketplace-y. More editorial, less catalog.

**Relove reference breakdown (for context, NOT to copy):**
- Clean hero with single value prop headline
- "Why sell with us" benefit cards (4 items)
- Service tier breakdowns with pricing
- Warm tan/beige accent color on white
- futura-pt sans-serif typography
- Straightforward, trust-first copy
- CTAs as text links, not heavy buttons

**Where 2ndLove differs from Relove:**
- More visual storytelling (scroll animation, lifestyle imagery)
- Boutique feel vs. marketplace/platform feel
- Serif headings for editorial luxury
- Gold accent instead of tan — more jewelry, less linen
- Fewer service tiers, simpler proposition
- Physical boutique focus (not shipping/box services)

**General aesthetic keywords:** Apple product pages, Aesop, The Row, Celine old branding, quiet luxury, editorial fashion, warm not cold

---

## 5. WEBSITE STRUCTURE (Full site, not LP)

### Section 1: HERO (100vh, scroll-triggered background animation)
**Layout:** Split. Text left-aligned on the left ~50%. Background visual on the right ~50%.
**Desktop:**
- Left side: Small badge/label up top → Large H1 → Subheadline → Primary CTA button (seller) + secondary text link
- Right side: 16:9 JPEG sequence background (closet animation — see Section 7)
- Text is left-aligned, NOT centered

**Copy (English):**
- Badge: `OPENING SOON IN TAMPERE`
- H1: `Your Wardrobe Deserves a Second Love`
- Subheadline: `Tampere's most carefully curated luxury second-hand boutique. Authenticated designer fashion — thoughtfully selected, beautifully presented, ready for its next chapter.`
- Primary CTA: `Sell With Us` (opens seller flow)
- Secondary link: `Learn more ↓`

### Section 2: SELLER — WHY SELL WITH US (scroll continues, coat stays on right as sticky)
**Layout:** Still left-aligned text because the coat visual is sticky on the right side.
**Content:**
- Section heading: `Why Sell With 2ndLove`
- Subheading: `We handle everything. You earn.`
- 3–4 value props (icon + title + short text), stacked vertically on the left:
  1. **Authenticated & Curated** — Every luxury item is verified for authenticity before it goes on display.
  2. **We Do the Work** — Pricing, photography, display, selling — we handle it all. You just drop off.
  3. **Fair Commission** — Transparent pricing. Real-time tracking. You get what your pieces deserve.
  4. **Boutique Experience** — Not a warehouse rack. Your pieces are displayed in a beautiful space they deserve.

### Section 3: HOW IT WORKS (Seller flow — 3 steps)
**Layout:** Can go full-width or stay left-aligned. Minimal.
- Heading: `How Selling Works`
- Step 1: `Bring Your Pieces` — Drop off your designer items at our Tampere boutique or request a pickup.
- Step 2: `We Curate & Price` — We authenticate, photograph, and price every item for the best possible return.
- Step 3: `You Earn` — Track your items in real time. When they sell, you earn — it's that simple.

### Section 4: SELLER CTA / FORM SECTION
**Layout:** Full-width section, warm background (dusty-rose or champagne).
- Heading: `Ready to Sell?`
- Subheading: `Leave your details and we'll get back to you within 24 hours.`
- Embedded GHL seller form (inline, not modal)

**GHL Seller Form embed:**
```html
<iframe
  src="https://api.leadconnectorhq.com/widget/form/DAOS3ihk8pyJpg5YOQBf"
  style="width:100%;height:100%;border:none;border-radius:0px"
  id="inline-DAOS3ihk8pyJpg5YOQBf"
  data-layout="{'id':'INLINE'}"
  data-trigger-type="alwaysShow"
  data-trigger-value=""
  data-activation-type="alwaysActivated"
  data-activation-value=""
  data-deactivation-type="neverDeactivate"
  data-deactivation-value=""
  data-form-name="Seller"
  data-height="390"
  data-layout-iframe-id="inline-DAOS3ihk8pyJpg5YOQBf"
  data-form-id="DAOS3ihk8pyJpg5YOQBf"
  title="Seller form"
></iframe>
<script src="https://link.msgsndr.com/js/form_embed.js"></script>
```
Min-height for the seller form iframe: 390px.

### Section 5: BUYER OPT-IN (lower on page, secondary priority)
**Layout:** Simpler section. Not the hero focus.
- Heading: `Shop Before Everyone Else`
- Subheading: `Be the first to know when new pieces arrive. Exclusive early access, insider pricing.`
- Embedded GHL buyer form (inline)

**GHL Buyer Form embed:**
```html
<iframe
  src="https://api.leadconnectorhq.com/widget/form/Oj4HDCbkKK9IKAwIzqGm"
  style="width:100%;height:100%;border:none;border-radius:0px"
  id="inline-Oj4HDCbkKK9IKAwIzqGm"
  data-layout="{'id':'INLINE'}"
  data-trigger-type="alwaysShow"
  data-trigger-value=""
  data-activation-type="alwaysActivated"
  data-activation-value=""
  data-deactivation-type="neverDeactivate"
  data-deactivation-value=""
  data-form-name="Buyer"
  data-height="366"
  data-layout-iframe-id="inline-Oj4HDCbkKK9IKAwIzqGm"
  data-form-id="Oj4HDCbkKK9IKAwIzqGm"
  title="Buyer form"
></iframe>
<script src="https://link.msgsndr.com/js/form_embed.js"></script>
```
Min-height for the buyer form iframe: 366px.

### Section 6: FIND US / MAP
- Heading: `Find Us`
- Subheading: `In the heart of Tampere.`
- Google Maps embed
- Address: Hämeenpuisto 27b, Tampere

### Section 7: FOOTER
- Logo (2ndLove)
- Address
- Copyright © 2026

---

## 6. SCROLL ANIMATION — BACKGROUND BEHAVIOR (CRITICAL)

**Concept:** Apple-style scroll-driven background animation using a JPEG image sequence.

**The visual story:**
1. **Frame 1 (initial state):** A styled closet on the right side of the viewport. Closed/neat. Luxurious.
2. **As user scrolls:** The closet "explodes" — doors open, clothes burst outward, garments float.
3. **Final frame:** A single beautiful coat on a hanger remains on the right side. Clean. Iconic. This coat stays as a sticky element while the seller sections scroll on the left.

**Technical behavior:**
- Background is FIXED (position: fixed) and fills the viewport at 16:9 aspect ratio
- The JPEG sequence is tied to scroll position (not time-based autoplay)
- First scroll interaction: the page does exactly **1 viewport height (100vh) of scroll** in a slide-switch motion
- During that 100vh scroll, the full JPEG sequence plays through (closet → explosion → coat)
- After the animation completes, the coat visual stays pinned/sticky on the right ~40-50% of the viewport
- Subsequent sections (seller value props, how it works) scroll on the LEFT side while the coat remains on the right
- The coat eventually scrolls away when reaching the seller form / buyer section

**Image sequence:** User will provide the JPEG files. They should be named sequentially (e.g., frame-001.jpg through frame-060.jpg or similar). The animation is driven by scroll progress mapped to frame index.

**Implementation approach (for Antigravity):**
- Use a `<canvas>` element, fixed position, full viewport
- On scroll, calculate progress (0 to 1) based on scroll position within the animation zone (0 to 100vh)
- Map progress to frame index, draw the corresponding JPEG on canvas
- Preload all frames on page load for smooth playback
- After animation zone, switch canvas to the final frame and keep it as a sticky background
- Use `will-change: transform` and requestAnimationFrame for performance

**Mobile fallback:**
- On mobile (<768px), skip the scroll animation
- Show a static hero image (final coat frame or a lifestyle shot)
- Stack layout vertically (text on top, image below or as background)
- All sections go full-width, centered text

---

## 7. COPY — ENGLISH (Primary, translate to Finnish later)

**Hero:**
- Badge: OPENING SOON IN TAMPERE
- H1: Your Wardrobe Deserves a Second Love
- Sub: Tampere's most carefully curated luxury second-hand boutique. Authenticated designer fashion — thoughtfully selected, beautifully presented, ready for its next chapter.
- CTA: Sell With Us
- Link: Learn more

**Why Sell:**
- Heading: Why Sell With 2ndLove
- Sub: We handle everything. You earn.
- Card 1: Authenticated & Curated — Every luxury item is verified for authenticity before it goes on display.
- Card 2: We Do the Work — Pricing, photography, display, selling — we handle it all. You just drop off.
- Card 3: Fair Commission — Transparent pricing. Real-time tracking. You get what your pieces deserve.
- Card 4: Boutique Experience — Not a warehouse rack. Your pieces are displayed in a beautiful space they deserve.

**How It Works:**
- Heading: How Selling Works
- Step 1: Bring Your Pieces — Drop off your designer items at our Tampere boutique or request a pickup.
- Step 2: We Curate & Price — We authenticate, photograph, and price every item for the best possible return.
- Step 3: You Earn — Track your items in real time. When they sell, you earn — it's that simple.

**Seller CTA:**
- Heading: Ready to Sell?
- Sub: Leave your details and we'll get back to you within 24 hours.

**Buyer:**
- Heading: Shop Before Everyone Else
- Sub: Be the first to know when new pieces arrive. Exclusive early access, insider pricing.

**Find Us:**
- Heading: Find Us
- Sub: In the heart of Tampere.

---

## 8. ANTIGRAVITY PROMPT

```
Build a high-end, single-page website for 2ndLove — a curated luxury second-hand fashion boutique in Tampere, Finland.

STYLE: Modern warm minimalism. Think Apple product page meets Aesop meets quiet luxury fashion editorial. Reference: https://en.relove.fi/page/123/sell-with-us for general tone (warm, clean, trust-building), but 2ndLove should feel more premium, more editorial, more boutique — not marketplace-y. Use serif headings (Cormorant Garamond) for editorial luxury and sans-serif body (DM Sans) for modern clarity.

COLORS:
- Gold accent: #C9A84C (CTAs, lines, highlights)
- Champagne background: #F5EDD8
- Dusty rose sections: #EDD5C8
- Charcoal text: #1F1F1F
- Stone muted: #8C8C8C
- Warm white: #FEFCF8

FONTS:
- Headings: 'Cormorant Garamond', serif (weight 500-600, italic for taglines)
- Body: 'DM Sans', sans-serif (weight 300-600, letter-spacing 2-3px on uppercase)
Load from Google Fonts.

HERO SECTION (100vh):
- Split layout: text LEFT-aligned on the left ~50%, background visual on the right ~50%
- Left side content (vertically centered):
  - Small uppercase badge: "OPENING SOON IN TAMPERE" (gold border, gold text, letter-spacing 3px)
  - H1: "Your Wardrobe Deserves a Second Love" (large serif, "Second Love" or "2nd" in gold)
  - Subheadline: "Tampere's most carefully curated luxury second-hand boutique. Authenticated designer fashion — thoughtfully selected, beautifully presented, ready for its next chapter."
  - Primary CTA button: "Sell With Us" (charcoal bg, warm-white text, uppercase, 13px, letter-spacing 2px)
  - Secondary text link: "Learn more ↓"
- Right side: 16:9 JPEG image sequence background (I will provide the frames)

SCROLL ANIMATION (Apple-style):
- The background is position: fixed, fills the right half of the viewport
- I will attach a JPEG sequence showing: a styled closet → it "explodes" with clothes bursting out → settles on a single coat on a hanger
- The scroll animation plays during the FIRST 100vh of scroll (like a slide-switch — the page scrolls 1 full viewport height and during that scroll the entire image sequence plays)
- Use a <canvas> element to draw frames based on scroll progress (scroll position 0 = frame 1, scroll position 100vh = last frame)
- Preload all JPEG frames for smooth playback
- After the animation completes, the final frame (coat on hanger) stays as a STICKY element on the right side
- The coat remains visible while sections 2 and 3 scroll past on the left side

SECTION 2 — WHY SELL WITH US (left-aligned, coat stays on right):
- Heading: "Why Sell With 2ndLove"
- Sub: "We handle everything. You earn."
- 4 value props stacked vertically on the left side (SVG icon + title + short text):
  1. Authenticated & Curated — Every luxury item is verified for authenticity before it goes on display.
  2. We Do the Work — Pricing, photography, display, selling — we handle it all. You just drop off.
  3. Fair Commission — Transparent pricing. Real-time tracking. You get what your pieces deserve.
  4. Boutique Experience — Not a warehouse rack. Your pieces are displayed in a beautiful space they deserve.
- Use inline SVG icons (stroke style, not fill, gold color) — checkmark-circle, hands, balance-scale, diamond/gem

SECTION 3 — HOW IT WORKS (3 steps):
- Heading: "How Selling Works"
- 3 steps with numbered indicators (gold border square with number):
  1. Bring Your Pieces — Drop off your designer items at our Tampere boutique or request a pickup.
  2. We Curate & Price — We authenticate, photograph, and price every item for the best possible return.
  3. You Earn — Track your items in real time. When they sell, you earn — it's that simple.

SECTION 4 — SELLER FORM CTA:
- Full-width section
- Heading: "Ready to Sell?"
- Sub: "Leave your details and we'll get back to you within 24 hours."
- Embed this iframe inline (NOT in a modal):
  <iframe src="https://api.leadconnectorhq.com/widget/form/DAOS3ihk8pyJpg5YOQBf" style="width:100%;height:100%;border:none" id="inline-DAOS3ihk8pyJpg5YOQBf" data-layout="{'id':'INLINE'}" data-trigger-type="alwaysShow" data-activation-type="alwaysActivated" data-deactivation-type="neverDeactivate" data-form-name="Seller" data-height="390" data-layout-iframe-id="inline-DAOS3ihk8pyJpg5YOQBf" data-form-id="DAOS3ihk8pyJpg5YOQBf" title="Seller form"></iframe>
- Also load: <script src="https://link.msgsndr.com/js/form_embed.js"></script>
- Min-height on the iframe: 390px

SECTION 5 — BUYER OPT-IN (lower priority, bottom of page):
- Heading: "Shop Before Everyone Else"
- Sub: "Be the first to know when new pieces arrive. Exclusive early access, insider pricing."
- Embed this iframe inline:
  <iframe src="https://api.leadconnectorhq.com/widget/form/Oj4HDCbkKK9IKAwIzqGm" style="width:100%;height:100%;border:none" id="inline-Oj4HDCbkKK9IKAwIzqGm" data-layout="{'id':'INLINE'}" data-trigger-type="alwaysShow" data-activation-type="alwaysActivated" data-deactivation-type="neverDeactivate" data-form-name="Buyer" data-height="366" data-layout-iframe-id="inline-Oj4HDCbkKK9IKAwIzqGm" data-form-id="Oj4HDCbkKK9IKAwIzqGm" title="Buyer form"></iframe>
- Min-height on the iframe: 366px

SECTION 6 — FIND US:
- Heading: "Find Us"
- Sub: "In the heart of Tampere."
- Google Maps embed iframe
- Address label: Hämeenpuisto 27b, Tampere

FOOTER:
- Dark charcoal background
- Logo: "2ndLove" (2nd in gold, Love in warm-white)
- Address: Hämeenpuisto 27b, Tampere
- Copyright: © 2026 2ndLove. All rights reserved.

MOBILE (<768px):
- Skip the JPEG scroll animation entirely
- Show a static image (final coat frame) or simple lifestyle hero
- Full-width stacked layout, text centered
- All sections go full-width
- Buttons stack vertically
- Reduce padding and font sizes proportionally

TECHNICAL NOTES:
- Single HTML file with inline CSS and JS (no build tools)
- Use CSS custom properties for all colors
- Smooth scroll behavior
- All icons must be inline SVGs (no emoji, no icon fonts — they render differently on iOS/macOS)
- The GHL form script (link.msgsndr.com/js/form_embed.js) only needs to be loaded once at the bottom
- Performance: preload JPEG frames, use requestAnimationFrame for scroll-driven animation, use will-change on the canvas
```

---

## 9. NOTES FOR ANTIGRAVITY

- The JPEG frame files will be attached separately. Name them sequentially.
- The animation canvas should be `position: fixed; top: 0; right: 0; width: 50vw; height: 100vh;` on desktop.
- After the 100vh scroll animation zone, the canvas should transition to `position: sticky` behavior (or the final frame should be placed in a sticky container).
- The left-side content column should have its own scroll, with generous padding (80-120px vertical sections).
- Keep the page feeling spacious. Lots of breathing room. Never cramped.
- All copy is in English for now. Finnish translation will come later.
