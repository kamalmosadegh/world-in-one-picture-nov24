#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news poster (1024x1024 PNG).

Renders a newspaper front page: a masthead naming the day, one lead
story, five further stories with small pictograms, and a footer ticker.
Deterministic: fixed strings, fixed geometry, no randomness, no time
or network access. Run:  python3 draw_poster.py  -> writes entry.png
next to this file.
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
MUTED = (74, 74, 74)
NAVY = (24, 48, 84)
RED = (178, 28, 28)
GREEN = (22, 101, 52)
GOLD = (201, 162, 39)
CARD = (255, 255, 255)
LINE = (180, 172, 150)
TICKER_BG = (24, 48, 84)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting `width` px."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def para(draw, xy, text, fnt, fill, width, leading=None):
    """Draw wrapped text, return the y just below the last line."""
    x, y = xy
    if leading is None:
        leading = int(fnt.size * 1.32)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, xy, text, color=RED):
    fnt = font(SANS_B, 17)
    draw.text(xy, text, font=fnt, fill=color)
    return xy[1] + 24


def pictogram_ship(draw, box):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    draw.line((cx, cy - 26, cx, cy + 6), fill=NAVY, width=4)
    draw.polygon([(cx, cy - 26), (cx + 26, cy - 4), (cx, cy - 4)], fill=RED)
    draw.polygon([(x0 + 4, cy + 8), (x1 - 4, cy + 8),
                  (x1 - 14, cy + 26), (x0 + 14, cy + 26)], fill=NAVY)
    for wx in range(x0 + 4, x1 - 2, 14):
        draw.line((wx, y1 - 2, wx + 8, y1 - 2), fill=(90, 130, 180), width=3)


def pictogram_satellite(draw, box):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    draw.rectangle((x0 + 2, cy - 8, cx - 16, cy + 8), fill=NAVY)
    draw.rectangle((cx + 16, cy - 8, x1 - 2, cy + 8), fill=NAVY)
    draw.rectangle((cx - 12, cy - 12, cx + 12, cy + 12), fill=RED)
    draw.line((cx - 12, cy - 12, cx - 26, cy - 26), fill=INK, width=3)
    draw.ellipse((cx - 30, cy - 30, cx - 22, cy - 22), fill=GOLD)


def pictogram_capitol(draw, box):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    draw.rectangle((x0 + 2, y1 - 12, x1 - 2, y1 - 2), fill=NAVY)
    for i in range(5):
        px = x0 + 10 + i * 16
        draw.rectangle((px, y1 - 34, px + 7, y1 - 12), fill=NAVY)
    draw.pieslice((cx - 22, y0 + 2, cx + 22, y0 + 46), 180, 360, fill=RED)
    draw.line((cx, y0 - 2, cx, y0 + 6), fill=INK, width=3)


def pictogram_warning(draw, box):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    draw.polygon([(cx, y0 + 2), (x1 - 2, y1 - 4), (x0 + 2, y1 - 4)],
                 fill=GOLD, outline=INK)
    draw.text((cx - 7, y0 + 18), "!", font=font(SANS_B, 34), fill=INK)


def pictogram_flame(draw, box):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    draw.polygon([(cx, y0 + 2), (cx + 20, cy - 2), (cx + 12, cy + 16),
                  (cx + 26, cy + 22), (cx, y1 - 2), (cx - 26, cy + 22),
                  (cx - 12, cy + 16), (cx - 20, cy - 2)], fill=RED)
    draw.ellipse((cx - 9, cy + 2, cx + 9, cy + 22), fill=GOLD)


def card(draw, box, kicker_text, headline, body, pictogram):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=10, fill=CARD, outline=LINE, width=2)
    px0, py0 = x1 - 96, y0 + 14
    pictogram(draw, (px0, py0, px0 + 76, py0 + 64))
    tx = x0 + 18
    ty = kicker(draw, (tx, y0 + 14), kicker_text)
    ty = para(draw, (tx, ty + 2), headline, font(SERIF, 26), INK,
              x1 - 108 - tx, leading=30)
    para(draw, (tx, ty + 4), body, font(SANS, 18), MUTED,
         x1 - 20 - tx, leading=23)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # --- Masthead -------------------------------------------------------
    draw.rectangle((0, 0, W, 100), fill=NAVY)
    draw.text((W // 2, 8), "THE WORLD IN ONE PICTURE",
              font=font(SERIF, 52), fill=(255, 255, 255), anchor="ma")
    draw.text((W // 2, 66), "TUESDAY, 24 NOVEMBER 2026",
              font=font(SANS_B, 24), fill=GOLD, anchor="ma")

    # --- Lead story -----------------------------------------------------
    draw.rounded_rectangle((24, 116, 1000, 420), radius=12, fill=CARD,
                           outline=LINE, width=2)
    draw.text((48, 132), "LEAD STORY  •  BUSINESS", font=font(SANS_B, 18),
              fill=RED)
    draw.text((48, 162), "HUANG IS BACK",
              font=font(SERIF, 62), fill=INK)
    para(draw, (48, 236),
         "Nvidia reinstates Jensen Huang as chief executive",
         font(SERIF, 29), INK, 600, leading=36)
    para(draw, (48, 316),
         "Eleven days after resigning in scandal, the chipmaker's "
         "co-founder returns after direct pressure from President "
         "Trump. Shares leapt 33%.",
         font(SANS, 22), MUTED, 600, leading=29)

    # Lead graphic: rising chip / market arrow.
    gx0, gy0, gx1, gy1 = 700, 150, 968, 396
    draw.rounded_rectangle((gx0, gy0, gx1, gy1), radius=10, fill=(232, 245, 233),
                           outline=GREEN, width=2)
    draw.line([(gx0 + 30, gy1 - 46), (gx0 + 100, gy1 - 86),
               (gx0 + 160, gy1 - 66), (gx0 + 230, gy1 - 126)],
              fill=GREEN, width=8)
    draw.polygon([(gx0 + 230, gy1 - 126), (gx0 + 196, gy1 - 126),
                  (gx0 + 230, gy1 - 92)], fill=GREEN)
    draw.rectangle((gx0 + 58, gy0 + 80, gx1 - 58, gy0 + 130), fill=NAVY)
    draw.text(((gx0 + gx1) // 2, gy0 + 84), "NVDA",
              font=font(SANS_B, 30), fill=(255, 255, 255), anchor="ma")
    draw.text(((gx0 + gx1) // 2, gy1 - 52), "+33%",
              font=font(SERIF, 44), fill=GREEN, anchor="ma")

    # --- Five further stories -------------------------------------------
    card(draw, (24, 436, 500, 616), "UKRAINE  •  LIBYA",
         "Ukraine sinks Russian warship off Libya",
         "Seven sea drones sank the corvette Merkury at Benghazi "
         "and hit the cargo ship Angara, Kyiv said — the war carried "
         "2,400 km from the front.",
         pictogram_ship)
    card(draw, (524, 436, 1000, 616), "SPACE  •  NATO",
         "NATO vows to defend space",
         "Chief Mark Rutte says the alliance will defend \"every "
         "inch\", after reports Russia may launch a nuclear-armed "
         "satellite within weeks.",
         pictogram_satellite)
    card(draw, (24, 632, 500, 812), "USA  •  POLITICS",
         "Democrats take historic House majority",
         "At least 258 seats — the largest House majority since "
         "1992 — after Virginia Foxx concedes in North Carolina.",
         pictogram_capitol)
    card(draw, (524, 632, 1000, 812), "USA  •  IOWA",
         "Trump halts Iowa explosives blast",
         "The president ordered the Army to pause the detonation "
         "of five tons of ageing lead azide until a court rules.",
         pictogram_warning)
    card(draw, (24, 828, 1000, 940), "WEST BANK",
         "Settler arson condemned as \u201cJewish terrorism\u201d",
         "Opposition leader Gadi Eisenkot denounces overnight attacks on "
         "Palestinian villages near Ramallah; police open an inquiry.",
         pictogram_flame)

    # --- Footer ticker --------------------------------------------------
    draw.rectangle((0, 952, W, 1006), fill=TICKER_BG)
    ticker = ("ALSO TODAY:  COP31 climate talks end with no deal in Antalya   •   "
              "India and Nepal sign eight agreements   •   Trump tells federal "
              "contractors to check with the White House first")
    para(draw, (24, 960), ticker, font(SANS_B, 18), (255, 255, 255),
         W - 48, leading=23)
    draw.text((W // 2, 1010), "The World in One Picture — 24 November 2026  •  "
              "Sources: Reuters, CNN, AP, BBC",
              font=font(SANS, 14), fill=MUTED, anchor="ma")

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
