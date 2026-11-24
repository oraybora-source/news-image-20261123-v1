#!/usr/bin/env python3
"""news-image-20261123 V1 entrypoint (Python 3.13, standard library only).

The front page (a 1024x1024 PNG) was drawn in this session by render.py
and is shipped in this repository as entry.png. This program only copies
those bytes to the output directory, so two runs are byte-identical and
it needs no network, no clock and no randomness.

Run it the way the harness does:
    python3 main.py            # writes /output/entry.png
or, outside the harness:
    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    src = os.path.join(HERE, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    made_dir = not os.path.isdir(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        raise SystemExit("entry.png copy is incomplete")
    os.chmod(dst, 0o644)
    if made_dir:
        os.chmod(out_dir, 0o755)


if __name__ == "__main__":
    main()
