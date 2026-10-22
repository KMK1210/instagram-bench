"""Build the annotated before/after consultation board."""
import sys
import textwrap
from PIL import Image, ImageDraw, ImageFont

before, after, out = sys.argv[1:4]
S = 1000 / 2576  # source -> panel scale
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
title, h2, body, small = (ImageFont.truetype(FB, 44), ImageFont.truetype(FB, 26),
                          ImageFont.truetype(F, 21), ImageFont.truetype(F, 18))
INK, MUTED, ACCENT, HAIR, BG = (34, 30, 28), (110, 100, 95), (196, 84, 96), (70, 110, 160), (250, 247, 244)

# (number, source xy, colour, heading, explanation)
notes = [
    (1, (1230, 300), HAIR, "Hair: soft side part (not rendered)",
     "Move the dead-centre part 2-3 cm off-centre. Your roots lie flat on the crown; a side part lifts them and adds height and softness at the crown."),
    (2, (560, 1150), HAIR, "Hair: face-framing layers (not rendered)",
     "Keep the collarbone length, but start long layers at the cheekbone and curve them in toward the jaw. That hides the lower-cheek width and puts the eye on your cheekbones."),
    (3, (540, 1850), HAIR, "Hair: blunt the ends + gloss (not rendered)",
     "The ends are thin and wispy. Take off 2-3 cm for a fuller, blunter edge. Add a clear or soft-brown gloss (level 3-4) to reduce frizz and add shine. No lightening needed."),
    (4, (1230, 760), ACCENT, "Brows: fuller, softer, slightly longer",
     "Your brows are fine and sparse at the tails, and they slope down toward the nose, which reads as a frown. Fill with a taupe pencil, keep the fronts soft, and extend the tails 5 mm toward the outer eye."),
    (5, (1395, 935), ACCENT, "Eyes: tightline + thin brown liner",
     "Line the outer two-thirds of the upper lash line, finishing in a 2-3 mm flick that follows the lower lash line. Curl the lashes, since yours grow straight and shade the eye. Skip heavy inner-corner liner."),
    (6, (820, 1035), ACCENT, "Under-eye: peach corrector",
     "There is mild bluish shadow under both eyes. Tap a peach corrector into the inner half only, then a thin concealer. Keep powder light."),
    (7, (1370, 1110), ACCENT, "Blush: high, angled toward the temple",
     "Place a soft rose-peach blush above the apples and sweep it up toward the temples. Placed high, it lifts the full lower cheek. Avoid the centre of the cheek."),
    (8, (1060, 1400), ACCENT, "Lips: rosy-coral tint, crisper edge",
     "Your lips are already balanced. A rose-coral tint plus a little definition at the cupid's bow and the outer corners counteracts the slightly downturned corners."),
    (9, (1030, 1185), ACCENT, "Complexion: sheer, keep the glow",
     "Use a light tint or cushion only where needed (redness by the nose). Blot the T-zone but leave the cheekbone glow. Don't over-matte."),
]

panel = 1000
pad = 50
W = pad * 3 + panel * 2
legend_h = 720
H = 150 + panel + 60 + legend_h
board = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(board)
d.text((pad, 40), "Beauty consultation: before / after", font=title, fill=INK)
d.text((pad, 100), "Makeup changes are simulated on your photo. Hair changes are recommendations only and are marked in blue.",
       font=small, fill=MUTED)

y0 = 150
for i, (path, label) in enumerate(((before, "BEFORE"), (after, "AFTER (makeup simulated)"))):
    x0 = pad + i * (panel + pad)
    board.paste(Image.open(path).convert("RGB").resize((panel, panel), Image.LANCZOS), (x0, y0))
    d.rectangle((x0, y0, x0 + 330 if i else x0 + 130, y0 + 40), fill=(0, 0, 0))
    d.text((x0 + 12, y0 + 8), label, font=small, fill=(255, 255, 255))

ax = pad * 2 + panel
for n, (sx, sy), col, *_ in notes:
    cx, cy = ax + sx * S, y0 + sy * S
    d.ellipse((cx - 19, cy - 19, cx + 19, cy + 19), fill=col, outline=(255, 255, 255), width=3)
    tw = d.textlength(str(n), font=h2)
    d.text((cx - tw / 2, cy - 16), str(n), font=h2, fill=(255, 255, 255))

ly = y0 + panel + 60
colw = (W - pad * 3) // 2
for idx, (n, _, col, head, text) in enumerate(notes):
    col_i = 0 if idx < 5 else 1
    if idx == 5:
        ly = y0 + panel + 60
    x = pad + col_i * (colw + pad)
    d.ellipse((x, ly, x + 34, ly + 34), fill=col)
    tw = d.textlength(str(n), font=h2)
    d.text((x + 17 - tw / 2, ly + 2), str(n), font=h2, fill=(255, 255, 255))
    d.text((x + 50, ly + 2), head, font=h2, fill=INK)
    ly += 40
    for line in textwrap.wrap(text, 78):
        d.text((x + 50, ly), line, font=body, fill=MUTED)
        ly += 28
    ly += 26

board.save(out, quality=92)
