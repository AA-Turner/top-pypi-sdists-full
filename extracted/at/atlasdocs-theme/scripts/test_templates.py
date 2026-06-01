#!/usr/bin/env python3
"""Validate all minijinja HTML templates in atlasdocs_theme/ for syntax errors."""
import sys
from pathlib import Path

import minijinja


def validate(theme_dir: Path) -> int:
    files = sorted(theme_dir.rglob("*.html"))
    if not files:
        print("ERROR: no HTML templates found under", theme_dir, file=sys.stderr)
        return 1

    errors: list[tuple[Path, minijinja.TemplateError]] = []

    for path in files:
        rel = path.relative_to(theme_dir)
        source = path.read_text(encoding="utf-8")
        env = minijinja.Environment()
        try:
            env.add_template(str(rel), source)
            print(f"  ok   {rel}")
        except minijinja.TemplateError as exc:
            errors.append((rel, exc))
            line_info = f" line {exc.line}" if exc.line else ""
            print(f"  FAIL {rel}{line_info}", file=sys.stderr)
            print(f"       kind   : {exc.kind}", file=sys.stderr)
            print(f"       reason : {exc.message}", file=sys.stderr)
            if exc.detail:
                print(f"       detail : {exc.detail}", file=sys.stderr)

    print()
    if errors:
        print(f"FAILED — {len(errors)} of {len(files)} template(s) have errors:")
        for rel, exc in errors:
            line_info = f":{exc.line}" if exc.line else ""
            print(f"  {rel}{line_info}  →  {exc.message}")
        return len(errors)

    print(f"PASSED — {len(files)} template(s) OK.")
    return 0


if __name__ == "__main__":
    theme_dir = Path(__file__).parent.parent / "atlasdocs_theme"
    sys.exit(validate(theme_dir))
