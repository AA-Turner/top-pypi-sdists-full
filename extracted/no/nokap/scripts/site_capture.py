"""
Capture a real website (pypi.org) as PNG and PDF for visual verification.

This tests captures of full web pages rather than isolated HTML elements.
Output goes to _visual_check/ alongside the table captures.
"""

from __future__ import annotations

from pathlib import Path

import nokap

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "_visual_check"
URL = "https://pypi.org"


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    generated: list[Path] = []

    # --- PNG screenshots ---
    # Full viewport
    name = "site_full_zoom1.png"
    out = OUTPUT_DIR / name
    print(f"  {name} ...", end=" ", flush=True)
    nokap.webshot(URL, out, delay=1.0)
    print(f"{out.stat().st_size / 1024:.1f} KB")
    generated.append(out)

    # Full viewport at zoom 2
    name = "site_full_zoom2.png"
    out = OUTPUT_DIR / name
    print(f"  {name} ...", end=" ", flush=True)
    nokap.webshot(URL, out, zoom=2, delay=1.0)
    print(f"{out.stat().st_size / 1024:.1f} KB")
    generated.append(out)

    # Selector-based: capture the main content area
    name = "site_selector_main.png"
    out = OUTPUT_DIR / name
    print(f"  {name} ...", end=" ", flush=True)
    nokap.webshot(URL, out, selector="main", expand=10, delay=1.0)
    print(f"{out.stat().st_size / 1024:.1f} KB")
    generated.append(out)

    # --- PDF full-page ---
    name = "site_fullpage_letter.pdf"
    out = OUTPUT_DIR / name
    print(f"  {name} ...", end=" ", flush=True)
    nokap.webshot(URL, out, delay=1.0, print_background=True)
    print(f"{out.stat().st_size / 1024:.1f} KB")
    generated.append(out)

    name = "site_fullpage_a4.pdf"
    out = OUTPUT_DIR / name
    print(f"  {name} ...", end=" ", flush=True)
    nokap.webshot(URL, out, delay=1.0, page_size="a4", print_background=True)
    print(f"{out.stat().st_size / 1024:.1f} KB")
    generated.append(out)

    # --- PDF element-bounded: main content ---
    name = "site_element_main.pdf"
    out = OUTPUT_DIR / name
    print(f"  {name} ...", end=" ", flush=True)
    nokap.webshot(URL, out, selector="main", expand=10, delay=1.0)
    print(f"{out.stat().st_size / 1024:.1f} KB")
    generated.append(out)

    nokap.close()

    print(f"\nGenerated {len(generated)} files in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
