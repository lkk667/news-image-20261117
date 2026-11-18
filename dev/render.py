"""Render the entry image: a newspaper front page summing up
Tuesday 17 November 2026 in six stories.

Drawn with Pillow only (flat shapes, no photos, no copied artwork).
Output: entry.png, 1024x1024, next to this script's parent directory.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 231)
INK = (17, 17, 17)
NAVY = (20, 33, 61)
PANEL = (255, 255, 255)
BORDER = (216, 210, 196)
MUTED = (90, 84, 70)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = f"{FONT_DIR}/DejaVuSans-Bold.ttf"
REG = f"{FONT_DIR}/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_star(draw, cx, cy, r_out, r_in, n=8, fill=(245, 197, 24)):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


# ---------------------------------------------------------------- stories
# (kicker, kicker colour, headline, summary)
STORIES = [
    (
        "UKRAINE",
        (139, 30, 30),
        "Kerch Bridge arch collapses",
        "Second strike in a day drops 270 m of road into the sea. Russia "
        "hits Kyiv's Dnipro bridges; heat, water, power cut.",
    ),
    (
        "THE GULF",
        (11, 94, 75),
        "Iran drones target U.S. radar",
        "Bahrain intercepts the drones, no casualties. Tankers hit "
        "near Hormuz; a third U.S. carrier joins the region.",
    ),
    (
        "CHINA \u00b7 APEC",
        (176, 42, 48),
        "Xi, Trump, Putin to meet",
        "China confirms the first three-way summit, Thursday in "
        "Shenzhen. Nuclear arms and the Iran war top the agenda.",
    ),
    (
        "CYBER",
        (91, 45, 142),
        "Hack hits 178 major websites",
        "Via Optimizely, attackers reached BBC, CNN, Zoom and HSBC "
        "pages, skimming cards and swapping crypto wallets.",
    ),
    (
        "UNITED STATES",
        (31, 78, 121),
        "Pentagon fails its ninth audit",
        "Auditors could not verify books covering $4.8 trillion in "
        "assets. A clean audit is now promised by 2028.",
    ),
    (
        "SPACE",
        (122, 74, 18),
        "Vulcan fell short, ULA says",
        "Tuesday update on Sunday's failure that lost 40 Amazon Leo "
        "satellites \u2014 ULA's first lost mission since 2006.",
    ),
]


# ------------------------------------------------------- flat illustrations
def ill_bridge(d, x, y):
    d.rectangle([x, y, x + 150, y + 88], fill=(188, 216, 233))
    d.rectangle([x, y + 88, x + 150, y + 150], fill=(46, 107, 138))
    d.rectangle([x, y + 96, x + 150, y + 100], fill=(120, 170, 200))
    # deck, left and right of the gap
    d.rectangle([x + 8, y + 76, x + 62, y + 86], fill=(107, 114, 128))
    d.rectangle([x + 90, y + 76, x + 142, y + 86], fill=(107, 114, 128))
    # standing road arch (left)
    d.arc([x + 16, y + 34, x + 58, y + 96], 180, 360, fill=(75, 85, 99), width=5)
    # broken arch falling into the water (right)
    d.line([x + 92, y + 78, x + 112, y + 104], fill=(75, 85, 99), width=5)
    d.line([x + 112, y + 104, x + 132, y + 80], fill=(75, 85, 99), width=5)
    d.rectangle([x + 100, y + 112, x + 112, y + 118], fill=(75, 85, 99))
    d.rectangle([x + 118, y + 120, x + 128, y + 125], fill=(75, 85, 99))
    # blast + smoke at the gap
    draw_star(d, x + 76, y + 66, 16, 7, fill=(245, 158, 11))
    d.ellipse([x + 58, y + 30, x + 76, y + 48], fill=(156, 163, 175))
    d.ellipse([x + 72, y + 22, x + 92, y + 42], fill=(176, 183, 195))


def ill_gulf(d, x, y):
    d.rectangle([x, y, x + 150, y + 96], fill=(234, 217, 168))
    d.rectangle([x, y + 96, x + 150, y + 150], fill=(46, 107, 138))
    d.ellipse([x + 118, y + 12, x + 140, y + 34], fill=(245, 197, 24))
    # radar dish on a mast
    d.line([x + 42, y + 66, x + 42, y + 98], fill=(55, 65, 81), width=5)
    d.arc([x + 18, y + 28, x + 66, y + 72], 180, 360, fill=(55, 65, 81), width=5)
    d.line([x + 42, y + 50, x + 62, y + 32], fill=(55, 65, 81), width=3)
    d.line([x + 42, y + 50, x + 24, y + 34], fill=(55, 65, 81), width=3)
    # drone above
    d.rectangle([x + 96, y + 44, x + 112, y + 50], fill=(31, 41, 55))
    for dx, dy in [(92, 38), (112, 38), (92, 52), (112, 52)]:
        d.ellipse([x + dx, y + dy, x + dx + 8, y + dy + 4], fill=(31, 41, 55))
    # intercept burst between drone and dish
    draw_star(d, x + 78, y + 46, 11, 5, fill=(245, 158, 11))
    # aircraft carrier in the sea
    d.polygon(
        [(x + 14, y + 122), (x + 136, y + 122), (x + 124, y + 140), (x + 26, y + 140)],
        fill=(100, 116, 139),
    )
    d.rectangle([x + 84, y + 106, x + 98, y + 122], fill=(71, 85, 105))
    d.line([x + 91, y + 96, x + 91, y + 106], fill=(71, 85, 105), width=3)


def ill_summit(d, x, y):
    d.rectangle([x, y, x + 150, y + 150], fill=(243, 232, 216))
    # three flags on poles
    poles = [34, 75, 116]
    for px in poles:
        d.line([x + px, y + 34, x + px, y + 108], fill=(90, 84, 70), width=3)
    # China flag
    d.rectangle([x + 34, y + 34, x + 62, y + 54], fill=(222, 41, 16))
    d.ellipse([x + 39, y + 39, x + 45, y + 45], fill=(255, 222, 0))
    # US flag
    d.rectangle([x + 75, y + 34, x + 103, y + 54], fill=(255, 255, 255))
    for sy in (38, 44, 50):
        d.rectangle([x + 75, y + sy, x + 103, y + sy + 2], fill=(178, 34, 52))
    d.rectangle([x + 75, y + 34, x + 88, y + 44], fill=(60, 59, 110))
    # Russia flag
    d.rectangle([x + 116, y + 34, x + 144, y + 54], fill=(255, 255, 255))
    d.rectangle([x + 116, y + 40, x + 144, y + 47], fill=(0, 57, 166))
    d.rectangle([x + 116, y + 47, x + 144, y + 54], fill=(213, 0, 50))
    # three leaders, shoulders behind the table
    for cx, col in [(48, (31, 78, 121)), (89, (176, 42, 48)), (130, (31, 41, 55))]:
        d.ellipse([x + cx - 9, y + 76, x + cx + 9, y + 94], fill=(232, 196, 160))
        d.pieslice([x + cx - 16, y + 92, x + cx + 16, y + 122], 180, 360, fill=col)
    # table
    d.rectangle([x + 12, y + 116, x + 138, y + 126], fill=(146, 94, 52))
    d.rectangle([x + 20, y + 126, x + 26, y + 142], fill=(120, 72, 32))
    d.rectangle([x + 124, y + 126, x + 130, y + 142], fill=(120, 72, 32))


def ill_cyber(d, x, y):
    d.rectangle([x, y, x + 150, y + 150], fill=(232, 228, 242))
    # monitor with code lines
    d.rectangle([x + 22, y + 26, x + 128, y + 102], fill=(31, 41, 55))
    d.rectangle([x + 28, y + 32, x + 122, y + 96], fill=(15, 23, 42))
    for i, (cw, col) in enumerate(
        [(52, (74, 222, 128)), (74, (96, 165, 250)), (44, (74, 222, 128)),
         (66, (248, 113, 113)), (58, (96, 165, 250))]
    ):
        d.rectangle([x + 36, y + 40 + i * 11, x + 36 + cw, y + 46 + i * 11], fill=col)
    d.rectangle([x + 66, y + 102, x + 84, y + 112], fill=(31, 41, 55))
    d.rectangle([x + 52, y + 112, x + 98, y + 116], fill=(31, 41, 55))
    # warning triangle
    d.polygon([(x + 108, y + 92), (x + 132, y + 132), (x + 84, y + 132)],
              fill=(245, 197, 24), outline=(31, 41, 55))
    d.rectangle([x + 106, y + 104, x + 110, y + 118], fill=(31, 41, 55))
    d.rectangle([x + 106, y + 122, x + 110, y + 126], fill=(31, 41, 55))
    # red crosses on the code
    for cx, cy in [(34, 40), (34, 62)]:
        d.line([x + cx, y + cy, x + cx + 8, y + cy + 8], fill=(220, 38, 38), width=2)


def ill_pentagon(d, x, y):
    d.rectangle([x, y, x + 150, y + 150], fill=(229, 231, 235))
    cx, cy, r = x + 75, y + 68, 52
    pts = []
    for i in range(5):
        a = -math.pi / 2 + 2 * math.pi * i / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=(156, 163, 175), outline=(75, 85, 99))
    d.polygon(pts, outline=(75, 85, 99))
    # dollar sign, crossed out: books that cannot be verified
    fnt = font(BOLD, 44)
    d.text((cx, cy - 4), "$", font=fnt, fill=(31, 41, 55), anchor="mm")
    d.ellipse([cx - 42, cy - 42, cx + 42, cy + 42], outline=(220, 38, 38), width=6)
    d.line([cx - 30, cy + 30, cx + 30, cy - 30], fill=(220, 38, 38), width=6)
    # "9th year" label
    fnt2 = font(BOLD, 22)
    d.text((cx, y + 132), "9TH YEAR", font=fnt2, fill=(220, 38, 38), anchor="mm")


def ill_rocket(d, x, y):
    d.rectangle([x, y, x + 150, y + 150], fill=(220, 233, 242))
    # dotted flight path
    for i in range(6):
        d.ellipse([x + 18 + i * 7, y + 128 - i * 9, x + 22 + i * 7, y + 132 - i * 9],
                  fill=(100, 116, 139))
    # rocket drawn upright on its own layer, then tilted
    layer = Image.new("RGBA", (150, 150), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.polygon([(60, 34), (90, 34), (75, 8)], fill=(220, 38, 38))
    ld.rectangle([60, 34, 90, 96], fill=(248, 250, 252))
    ld.rectangle([60, 34, 90, 40], fill=(220, 38, 38))
    ld.ellipse([68, 52, 82, 66], fill=(96, 165, 250), outline=(31, 41, 55), width=2)
    ld.polygon([(60, 82), (46, 104), (60, 96)], fill=(220, 38, 38))
    ld.polygon([(90, 82), (104, 104), (90, 96)], fill=(220, 38, 38))
    ld.polygon([(68, 96), (82, 96), (75, 128)], fill=(245, 158, 11))
    ld.polygon([(71, 96), (79, 96), (75, 116)], fill=(245, 197, 24))
    layer = layer.rotate(28, resample=Image.BICUBIC, center=(75, 75))
    # paste the rotated rocket onto the main image
    d._image.paste(layer, (x, y), layer)
    # lost satellites: small squares with panels
    for sx, sy in [(16, 104), (118, 26), (122, 112)]:
        d.rectangle([x + sx, y + sy, x + sx + 12, y + sy + 12], fill=(31, 78, 121))
        d.rectangle([x + sx - 10, y + sy + 3, x + sx, y + sy + 9], fill=(96, 165, 250))
        d.rectangle([x + sx + 12, y + sy + 3, x + sx + 22, y + sy + 9], fill=(96, 165, 250))


ILLUSTRATIONS = [ill_bridge, ill_gulf, ill_summit, ill_cyber, ill_pentagon, ill_rocket]


# ------------------------------------------------------------------- render
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    title_f = font(BOLD, 56)
    d.text((W // 2, 12), "THE WORLD TODAY", font=title_f, fill=INK, anchor="ma")
    d.line([16, 78, W - 16, 78], fill=INK, width=3)
    d.line([16, 83, W - 16, 83], fill=INK, width=1)

    # date bar
    d.rectangle([16, 90, W - 16, 144], fill=NAVY)
    date_f = font(BOLD, 36)
    d.text((W // 2, 117), "TUESDAY 17 NOVEMBER 2026", font=date_f,
           fill=(255, 255, 255), anchor="mm")

    # deck line
    deck_f = font(BOLD, 19)
    d.text((W // 2, 146), "THE DAY IN SIX STORIES", font=deck_f,
           fill=MUTED, anchor="ma")

    # grid: 2 cols x 3 rows
    gx, gy, gap = 16, 172, 12
    pw, ph = 490, 274
    kicker_f = font(BOLD, 19)
    headline_f = font(BOLD, 32)
    summary_f = font(REG, 24)

    for i, (kicker, kcol, headline, summary) in enumerate(STORIES):
        px = gx + (i % 2) * (pw + gap)
        py = gy + (i // 2) * (ph + gap)
        d.rectangle([px, py, px + pw, py + ph], fill=PANEL, outline=BORDER, width=2)

        # illustration, drawn at 150x150 then scaled to 132, vertically centred
        layer = Image.new("RGB", (150, 150), PAPER)
        ld = ImageDraw.Draw(layer)
        ILLUSTRATIONS[i](ld, 0, 0)
        layer = layer.resize((132, 132), Image.LANCZOS)
        img.paste(layer, (px + 10, py + (ph - 132) // 2))

        # text block
        tx = px + 152
        tw = px + pw - 14 - tx
        ty = py + 14
        d.rectangle([tx, ty + 4, tx + 12, ty + 16], fill=kcol)
        d.text((tx + 20, ty), kicker, font=kicker_f, fill=kcol, anchor="la")
        ty += 30

        hlines = wrap(d, headline, headline_f, tw)
        assert len(hlines) <= 2, f"headline too long: {headline!r} -> {hlines}"
        for ln in hlines:
            d.text((tx, ty), ln, font=headline_f, fill=INK, anchor="la")
            ty += 37
        ty += 6

        # summary: fit in the remaining space, shrinking if needed
        max_lines = max(1, (py + ph - 10 - ty) // 28)
        sfont = summary_f
        slines = wrap(d, summary, sfont, tw)
        while len(slines) > max_lines and sfont.size > 20:
            sfont = font(REG, sfont.size - 1)
            slines = wrap(d, summary, sfont, tw)
        if len(slines) > max_lines:
            slines = slines[:max_lines]
            last = slines[-1]
            while d.textlength(last + "\u2026", font=sfont) > tw and len(last) > 1:
                last = last[:-1]
            slines[-1] = last + "\u2026"
        lh = 28 if sfont.size >= 24 else 26
        for ln in slines:
            d.text((tx, ty), ln, font=sfont, fill=(38, 38, 38), anchor="la")
            ty += lh
        assert ty <= py + ph - 6, f"text overflow in panel {i}: {ty} > {py + ph - 6}"

    return img


def main():
    img = render()
    out = Path(__file__).resolve().parent.parent / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} {img.size} {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
