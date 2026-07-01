"""
Generate the CVC default background texture.

Design brief (v3):
  - Square 1444x1444 to match the original asset's footprint.
  - High-contrast duotone (cream ink on cobalt-blue ground) with
    NEAR-BINARY line alpha (180-255 range) so the texture survives
    the Backdrop's `difference + 3.3% opacity` wash at full visibility
    — matching the visibility level of the legacy Doré asset.
  - Central "soul loom" medallion, deliberately non-figurative.
  - Canvas-wide subtle telemetry grid (long sparse filaments + dots)
    so cropped viewports never show a flat blue field.
"""
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import math, random, os

W = H = 1444
CREAM = (245, 236, 217)
COBALT = (30, 58, 138)

img = Image.new("RGB", (W, H), COBALT)
draw = ImageDraw.Draw(img, "RGBA")
random.seed(1729)

# === A. Canvas-wide subtle telemetry (covers everything) ===
# (1) Sparse field of tiny dots — keeps the cropped canvas alive.
for _ in range(900):
    x, y = random.uniform(0, W), random.uniform(0, H)
    r = random.choice([1, 1, 1])
    a = random.randint(120, 220)  # bumped from 40-110
    draw.ellipse([x - r, y - r, x + r, y + r], fill=(*CREAM, a))

# (2) Long faint horizontal scan filaments.
for _ in range(28):
    y = random.uniform(0, H)
    x1, x2 = random.uniform(0, W * 0.3), random.uniform(W * 0.7, W)
    a = random.randint(100, 170)  # bumped from 30-70
    draw.line([(x1, y), (x2, y)], fill=(*CREAM, a), width=1)

# (3) Long faint vertical scan filaments.
for _ in range(28):
    x = random.uniform(0, W)
    y1, y2 = random.uniform(0, H * 0.3), random.uniform(H * 0.7, H)
    a = random.randint(100, 170)
    draw.line([(x, y1), (x, y2)], fill=(*CREAM, a), width=1)

# === B. Central "soul loom" medallion ===
cx, cy = W / 2, H * 0.50
RINGS = 18
RING_STEP = 18

for r in range(RING_STEP, RINGS * RING_STEP + 1, RING_STEP):
    falloff = max(0, 1 - r / (RINGS * RING_STEP))
    alpha = int(245 * falloff ** 1.0)  # bumped from 230, gentler falloff
    if alpha < 80:
        alpha = 80
    width = 2 if r < 3 * RING_STEP else 1
    draw.ellipse(
        [cx - r, cy - r, cx + r, cy + r],
        outline=(*CREAM, alpha), width=width,
    )

# Radial spokes.
SPOKES = 72
for i in range(SPOKES):
    theta = (i / SPOKES) * 2 * math.pi
    inner = random.uniform(30, 80)
    outer = random.uniform(RINGS * RING_STEP * 0.5, RINGS * RING_STEP * 0.98)
    x1, y1 = cx + inner * math.cos(theta), cy + inner * math.sin(theta)
    x2, y2 = cx + outer * math.cos(theta), cy + outer * math.sin(theta)
    alpha = random.randint(140, 230)  # bumped from 50-170
    draw.line([(x1, y1), (x2, y2)], fill=(*CREAM, alpha), width=1)

# Inner core — sharp nested rings + bold center dot.
for r, w, a in [(8, 1, 255), (16, 2, 245), (28, 1, 220)]:
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 outline=(*CREAM, a), width=w)
draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(*CREAM, 255))

# === C. Constellation nodes + filament mesh ===
NODES = 280
nodes = []
for _ in range(NODES):
    rad = math.sqrt(random.random()) * RINGS * RING_STEP * 0.95
    theta = random.random() * 2 * math.pi
    x, y = cx + rad * math.cos(theta), cy + rad * math.sin(theta)
    if 10 <= x <= W - 10 and 10 <= y <= H - 10:
        nodes.append((x, y))

for x, y in nodes:
    radius = random.choice([1, 1, 1, 1, 2, 2, 3])
    alpha = random.randint(160, 245)  # bumped from 100-220
    draw.ellipse([x - radius, y - radius, x + radius, y + radius],
                 fill=(*CREAM, alpha))

random.shuffle(nodes)
FILAMENT_LEN = 75
used = set()
for i, (x1, y1) in enumerate(nodes):
    nbrs = []
    for j, (x2, y2) in enumerate(nodes):
        if i == j:
            continue
        d = math.hypot(x2 - x1, y2 - y1)
        if d < FILAMENT_LEN and (i, j) not in used and (j, i) not in used:
            nbrs.append((d, j, x2, y2))
    nbrs.sort()
    for d, j, x2, y2 in nbrs[:2]:
        used.add((i, j))
        alpha = int(220 * (1 - d / FILAMENT_LEN))  # bumped from 170
        if alpha < 80:
            continue
        midx = (x1 + x2) / 2 + random.uniform(-7, 7)
        midy = (y1 + y2) / 2 + random.uniform(-7, 7)
        draw.line([(x1, y1), (midx, midy), (x2, y2)],
                  fill=(*CREAM, alpha), width=1)

# === D. Soften + sharpen + push contrast ===
img = img.filter(ImageFilter.GaussianBlur(radius=0.4))
img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=80, threshold=2))
img = ImageEnhance.Contrast(img).enhance(1.30)  # bumped from 1.15

out_dir = "/Users/jkm/Projects/cvc/cvc/web/src/vendor/nous-ui/assets"
os.makedirs(out_dir, exist_ok=True)

# `src/vendor/nous-ui/assets/` is the source of truth — the build-time
# `sync-vendor-assets.mjs` hook (npm `prebuild`) mirrors its contents to
# `public/ds-assets/` for Vite to serve. We write TWO artifacts here so
# the sync step distributes both:
#   cvc-soulmesh.jpg — canonical asset, referenced by `assets.bg` in
#     every built-in theme via the CSS-var path in Backdrop.
#   filler-bg0.jpg   — fallback asset referenced by the default <img>
#     element in Backdrop. Kept as a separate file so the legacy path
#     stays wired (in case a future theme opts out of `assets.bg`).
#     Both files MUST contain the same image — a mismatch produces a
#     visible seam during theme switches. The build script enforces
#     this by writing the same `img` bytes to both paths.
canonical = os.path.join(out_dir, "cvc-soulmesh.jpg")
legacy = os.path.join(out_dir, "filler-bg0.jpg")

img.save(canonical, "JPEG", quality=82, optimize=True, progressive=True)
img.save(legacy, "JPEG", quality=82, optimize=True, progressive=True)
print(f"wrote {canonical}  {W}x{H}  {os.path.getsize(canonical)/1024:.1f} KB")
print(f"wrote {legacy}    {W}x{H}  {os.path.getsize(legacy)/1024:.1f} KB")