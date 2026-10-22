"""Approximate makeup preview on the selfie (makeup only; hair changes are not simulated)."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
W, H = im.size
img = np.asarray(im).astype(np.float32) / 255.0


def mask(draw_fn, blur):
    m = Image.new("L", (W, H), 0)
    draw_fn(ImageDraw.Draw(m))
    m = m.filter(ImageFilter.GaussianBlur(blur))
    return (np.asarray(m).astype(np.float32) / 255.0)[..., None]


def multiply(base, rgb, m, a):
    c = np.array(rgb, np.float32) / 255.0
    return base * (1 - m * a) + base * c * (m * a)


def screen(base, m, a):
    return base * (1 - m * a) + (1 - (1 - base) * (1 - base)) * (m * a)


# 1. Under-eye brightening (soft, peach-toned corrector look)
ue = mask(lambda d: (d.ellipse((740, 975, 905, 1045), fill=255),
                     d.ellipse((1150, 960, 1320, 1030), fill=255)), 22)
img = screen(img, ue, 0.22)

# 2. Brows: fuller, softer taupe, inner fronts kept soft, tails extended slightly
def brows(d):
    d.line([(902, 858), (860, 842), (800, 832), (745, 845), (712, 872)], fill=255, width=20, joint="curve")
    d.line([(1098, 848), (1150, 828), (1220, 808), (1290, 800), (1360, 818)], fill=255, width=20, joint="curve")
fr = mask(brows, 6)
img = multiply(img, (95, 72, 60), fr, 0.36)

# 3. Tightline / thin brown liner on the outer two-thirds of the upper lash line
def liner(d):
    d.line([(860, 912), (800, 912), (752, 928), (722, 952), (700, 944)], fill=255, width=7, joint="curve")
    d.line([(1190, 895), (1260, 892), (1310, 905), (1342, 928), (1366, 920)], fill=255, width=7, joint="curve")
ln = mask(liner, 3)
img = multiply(img, (45, 30, 25), ln, 0.55)

# 4. Blush: placed high on the cheek and swept up toward the temple
bl = Image.new("L", (W, H), 0)
for cx, cy, ang in ((790, 1060, 22), (1300, 1040, -22)):
    e = Image.new("L", (W, H), 0)
    ImageDraw.Draw(e).ellipse((cx - 135, cy - 70, cx + 135, cy + 70), fill=255)
    e = e.rotate(ang, center=(cx, cy))
    bl = Image.fromarray(np.maximum(np.asarray(bl), np.asarray(e)))
bl = (np.asarray(bl.filter(ImageFilter.GaussianBlur(55))).astype(np.float32) / 255.0)[..., None]
img = multiply(img, (240, 165, 170), bl, 0.2)

# 5. Lips: rosy-coral MLBB tint with slightly crisper edge
lips = [(905, 1388), (950, 1350), (1010, 1330), (1045, 1340), (1080, 1330), (1150, 1345), (1215, 1368),
        (1180, 1415), (1110, 1450), (1040, 1458), (965, 1445), (920, 1415)]
lm = mask(lambda d: d.polygon(lips, fill=255), 6)
img = multiply(img, (215, 110, 118), lm, 0.24)

# 6. Very light overall warmth/clarity (no smoothing)
img = np.clip(img, 0, 1)
img = img ** 0.97

Image.fromarray((img * 255).astype(np.uint8)).save(out, quality=95)
