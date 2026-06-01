#!/usr/bin/env python3
"""Check CSS syntax in atlasdocs_theme/assets/stylesheets/."""
import sys
from pathlib import Path

import tinycss2


def validate(css_dir: Path) -> int:
    files = sorted(css_dir.glob("*.css"))
    if not files:
        print("No CSS files found.", file=sys.stderr)
        return 1

    errors: list[str] = []
    for path in files:
        nodes = tinycss2.parse_stylesheet(
            path.read_text(encoding="utf-8"),
            skip_whitespace=True,
            skip_comments=True,
        )
        parse_errors = [n for n in nodes if n.type == "error"]
        if parse_errors:
            for err in parse_errors:
                print(
                    f"  FAIL {path.name}  line {err.source_line}:"
                    f"{err.source_column}: {err.message}",
                    file=sys.stderr,
                )
            errors.append(path.name)
        else:
            print(f"  ok   {path.name}")

    print(f"\n{len(files)} stylesheet(s) checked — {len(errors)} error(s).")
    return len(errors)


if __name__ == "__main__":
    css_dir = (
        Path(__file__).parent.parent / "atlasdocs_theme" / "assets" / "stylesheets"
    )
    sys.exit(validate(css_dir))
