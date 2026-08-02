import json
import re
from pathlib import Path

import typer

# FR-001, FR-012a... ; chiffres obligatoires pour éviter de capter FR-IDs/FR-API en prose
_FR = re.compile(r"\bFR-\d+[a-zA-Z]?\b")


def parse_fr_ids(text: str) -> set[str]:
    return set(_FR.findall(text))


def coverage_gaps(required: set[str], covered: set[str]) -> list[str]:
    """FR présents dans la spec mais absents de la map de couverture (oublis)."""
    return sorted(required - covered)


def main(spec: str, screens_map: str) -> None:
    """Liste les FR de la spec sans écran dans la map de couverture."""
    required = parse_fr_ids(Path(spec).read_text(encoding="utf-8"))
    covered = parse_fr_ids(Path(screens_map).read_text(encoding="utf-8"))
    gaps = coverage_gaps(required, covered)
    typer.echo(json.dumps({"verdict": "GAPS" if gaps else "COVERED", "gaps": gaps}, indent=2, ensure_ascii=False))
    raise typer.Exit(code=1 if gaps else 0)
