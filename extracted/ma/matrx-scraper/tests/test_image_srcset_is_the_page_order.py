"""An image's srcset is in the page's order in every process (L7i, 2026-11-09).

``Image.to_data`` returned ``list(set(all_sources))``: string hashing is randomized per process, so one page's
srcset came back in a different order on each read (Idaho replay dc30d3da: local.yahoo.com's hero image,
rs_content.extracted_images and rs_media.metadata differed between the two engines on the same page).
"""

from __future__ import annotations

import json
import subprocess
import sys

SOURCES = [f"https://img.example.com/{i}/hero-{w}.webp" for i, w in enumerate((320, 640, 960, 1280, 1920, 2560))]
CODE = (
    "import json; from matrx_scraper.parser.data_types import ExtractionSettings, Image; "
    f"img = Image(src='x', all_sources={SOURCES + SOURCES[:2]!r}); "
    "print(json.dumps(img.to_data(ExtractionSettings(['image'], ['data']))['srcset']))"
)


def _srcset(seed: int) -> list[str]:
    out = subprocess.run([sys.executable, "-c", CODE], capture_output=True, text=True, check=True,
                         env={"PYTHONHASHSEED": str(seed), "PATH": "/usr/bin:/bin"})
    return json.loads(out.stdout)


def test_srcset_keeps_the_page_order_once_each_in_every_process() -> None:
    assert all(_srcset(seed) == SOURCES for seed in (1, 2, 3, 4))
