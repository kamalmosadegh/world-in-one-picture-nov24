# The World in One Picture — 24 November 2026

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Pillow](https://img.shields.io/badge/Pillow-image%20drawing-lightgrey.svg)](https://pillow.readthedocs.io/)

A 1024×1024 newspaper-style poster that sums up the world's news of
Tuesday 24 November 2026 — six stories, one image. A daily snapshot of
the world, drawn as a single front page: headline, stories, and a
ticker of the day's other news.

## The day

- **Nvidia reinstates Jensen Huang as CEO** — Eleven days after
  resigning in scandal, the chipmaker's co-founder returns after direct
  pressure from President Trump. Shares leapt 33%.
- **Ukraine sinks Russian warship off Libya** — Seven sea drones sank the
  corvette Merkury at Benghazi and hit the cargo ship Angara, Kyiv said.
- **NATO vows to defend space** — Chief Mark Rutte says the alliance will
  defend "every inch", after reports Russia may launch a nuclear-armed
  satellite within weeks.
- **Democrats take historic House majority** — At least 258 seats — the
  largest House majority since 1992.
- **Trump halts Iowa explosives blast** — The Army's detonation of five
  tons of ageing lead azide is paused until a court rules.
- **Settler arson condemned as "Jewish terrorism"** — Opposition leader
  Gadi Eisenkot denounces overnight attacks on Palestinian villages
  near Ramallah.

The footer ticker adds the day's other headlines: COP31 climate talks
ending with no deal in Antalya, and India and Nepal signing eight
agreements.

## Features

- **One-page news poster** — six lead stories laid out like a newspaper
  front page, with a headline ticker of the day's other news.
- **Deterministic rendering** — the poster is drawn once with Pillow and
  DejaVu fonts, so every run produces the exact same image.
- **Byte-exact delivery** — `main.py` copies the poster byte for byte,
  so the image you see is the image in this repository.

## Results

- Poster: 1024×1024 PNG, 140,033 bytes (limit 1 MiB), drawn with Pillow
  and DejaVu fonts, legible at 300 pixels across.
- `draw_poster.py` is deterministic: two consecutive runs produce
  byte-identical files (SHA-256
  `44ac3409630f2312019f11ac66495263df9c46e4a1807ada9e12b447396be8e2`,
  verified with `cmp`).
- `main.py` copies the poster byte for byte, so both runs write the
  same bytes (verified).

## How to run

```sh
python3 draw_poster.py        # redraw entry.png with Pillow
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # copy it to out/entry.png
```

`main.py` runs on Python 3.13 with the standard library only; the poster is
drawn with Pillow and shipped beside it as `entry.png`.

---

**Kamal Mosadegh** — Freelance Developer · Contact by email:
kamalmosadegh6977@gmail.com
