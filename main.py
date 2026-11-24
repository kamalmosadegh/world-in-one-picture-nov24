#!/usr/bin/env python3
"""The World in One Picture — 24 November 2026.

Writes the day's news poster to the output directory. The poster
itself is drawn by draw_poster.py (Pillow) and shipped in this
repository as entry.png; this program only copies those exact bytes
to the required output path, so both runs of the entry produce an
identical file. Standard library only, no network access.
"""

import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    # Copy the bytes verbatim: the output must be identical on every run.
    shutil.copyfile(SOURCE, target)
    print("wrote", target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
