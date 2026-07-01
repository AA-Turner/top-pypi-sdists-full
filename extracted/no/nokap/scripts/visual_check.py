"""
Generate a matrix of GT table captures for visual verification.

Scans across:
- Format: PNG, PDF (full-page), PDF (element-bounded)
- Zoom: 1, 2, 3
- Expand (margin): 0, 5, 20

Output goes to _visual_check/ with descriptive filenames.
"""

from __future__ import annotations

import itertools
from pathlib import Path

import nokap

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "_visual_check"

# Parameters to scan
ZOOMS = [1, 2, 3]
EXPANDS = [0, 5, 20]

# A simple GT table rendered to HTML
GT_HTML: str | None = None


def _get_gt_html() -> str:
    global GT_HTML
    if GT_HTML is not None:
        return GT_HTML

    from great_tables import GT, exibble

    GT_HTML = GT(exibble.head(5)).as_raw_html(make_page=True, all_important=True)
    return GT_HTML


# A wide GT table (many columns) to test wide-table handling
_WIDE_GT_HTML: str | None = None


def _get_wide_gt_html() -> str:
    global _WIDE_GT_HTML
    if _WIDE_GT_HTML is not None:
        return _WIDE_GT_HTML

    import pandas as pd
    from great_tables import GT

    # Build a wide DataFrame with 20 columns of varied content
    df = pd.DataFrame(
        {
            f"col_{i:02d}": [f"value_{i}_{r}" for r in range(8)]
            for i in range(20)
        }
    )
    _WIDE_GT_HTML = GT(df).as_raw_html(make_page=True, all_important=True)
    return _WIDE_GT_HTML


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    html = _get_gt_html()
    generated: list[Path] = []

    # --- PNG captures (element-bounded screenshots) ---
    for zoom, expand in itertools.product(ZOOMS, EXPANDS):
        name = f"png_zoom{zoom}_expand{expand}.png"
        out = OUTPUT_DIR / name
        print(f"  {name} ...", end=" ", flush=True)
        nokap.from_html(
            html, out, selector="table", zoom=zoom, expand=expand, delay=0.3
        )
        print(f"{out.stat().st_size / 1024:.1f} KB")
        generated.append(out)

    # --- PDF element-bounded captures (zoom is ignored for PDF; vary expand) ---
    for expand in EXPANDS:
        name = f"pdf_element_expand{expand}.pdf"
        out = OUTPUT_DIR / name
        print(f"  {name} ...", end=" ", flush=True)
        nokap.from_html(
            html,
            out,
            selector="table",
            expand=expand,
            delay=0.3,
        )
        print(f"{out.stat().st_size / 1024:.1f} KB")
        generated.append(out)

    # --- PDF full-page captures (varying page sizes) ---
    page_sizes = ["letter", "legal", "tabloid", "ledger", "a0", "a1", "a2", "a3", "a4", "a5", "a6"]
    for page_size in page_sizes:
        name = f"pdf_fullpage_{page_size}.pdf"
        out = OUTPUT_DIR / name
        print(f"  {name} ...", end=" ", flush=True)
        nokap.from_html(
            html,
            out,
            delay=0.3,
            page_size=page_size,
            print_background=True,
        )
        print(f"{out.stat().st_size / 1024:.1f} KB")
        generated.append(out)

    # --- Wide table: element-bounded PDF (tests natural-width measurement) ---
    wide_html = _get_wide_gt_html()
    for expand in EXPANDS:
        name = f"pdf_element_wide_expand{expand}.pdf"
        out = OUTPUT_DIR / name
        print(f"  {name} ...", end=" ", flush=True)
        nokap.from_html(
            wide_html,
            out,
            selector="table",
            expand=expand,
            delay=0.3,
        )
        print(f"{out.stat().st_size / 1024:.1f} KB")
        generated.append(out)

    # Wide table as PNG for comparison
    name = "png_wide_zoom2_expand5.png"
    out = OUTPUT_DIR / name
    print(f"  {name} ...", end=" ", flush=True)
    nokap.from_html(wide_html, out, selector="table", zoom=2, expand=5, delay=0.3)
    print(f"{out.stat().st_size / 1024:.1f} KB")
    generated.append(out)

    nokap.close()

    print(f"\nGenerated {len(generated)} files in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
