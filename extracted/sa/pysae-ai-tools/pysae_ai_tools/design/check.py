import json
from dataclasses import asdict
from pathlib import Path

import typer

from .catalog import UI_DIRS, discover_catalog, primitive_suggestions
from .findings import Report
from .rules import find_arbitrary_values, find_palette_classes, find_raw_colors, find_raw_primitives
from .tokens import ThemeTokens, parse_theme

_CSS_PATHS = ("src/index.css", "index.css")


def _project_root(file: Path) -> Path:
    """Premier ancêtre contenant un catalogue components/ui/, sinon le dossier du fichier."""
    for parent in [file, *file.parents]:
        if any((parent / rel).is_dir() for rel in UI_DIRS):
            return parent
    return file.parent


def _load_theme(base: Path) -> ThemeTokens | None:
    for rel in _CSS_PATHS:
        css = base / rel
        if css.is_file():
            return parse_theme(css.read_text(encoding="utf-8"))
    return None


def run_check(file: str, root: str | None = None) -> Report:
    path = Path(file)
    src = path.read_text(encoding="utf-8")
    base = Path(root) if root else _project_root(path)
    raw = find_raw_colors(src) + find_arbitrary_values(src)
    # R3 (primitive vs composant catalogue) ne vaut que pour le React/JSX : un proto
    # HTML utilise légitimement <button>/<input>. R3 est rejouée au gate maquette->code
    # sur le .tsx livré.
    if path.suffix in (".tsx", ".jsx"):
        raw += find_raw_primitives(src, primitive_suggestions(discover_catalog(base)))
    theme = _load_theme(base)
    if theme is not None:
        raw += find_palette_classes(src, theme.colors)
    raw.sort(key=lambda f: (f.line, f.rule))
    verdict = "VIOLATIONS" if raw else "CLEAN"
    return Report(file=file, verdict=verdict, findings=raw)


def main(file: str, root: str | None = None) -> None:
    """Check a screen source file for design-system deviations."""
    report = run_check(file, root)
    payload = {
        "file": report.file,
        "verdict": report.verdict,
        "findings": [{"n": i, **asdict(f)} for i, f in enumerate(report.findings, start=1)],
    }
    typer.echo(json.dumps(payload, indent=2, ensure_ascii=False))
    raise typer.Exit(code=1 if report.verdict == "VIOLATIONS" else 0)
