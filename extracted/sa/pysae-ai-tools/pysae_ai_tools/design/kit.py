from pathlib import Path

import typer

from .catalog import discover_catalog
from .tokens import parse_theme

_RULES = (
    "## Règles\n\n"
    "- Couleurs : uniquement tokens sémantiques (zéro hex brut, zéro palette Tailwind par défaut).\n"
    "- Typo : Poppins (400/500/600).\n"
    "- Espacement : échelle 4px (pas de valeur arbitraire).\n"
    "- Composants : réutiliser le catalogue ci-dessus ; tout composant nouveau doit être justifié.\n"
)


def build_kit(root: Path) -> str:
    css = next((p for rel in ("src/index.css", "index.css") if (p := root / rel).is_file()), None)
    tokens = parse_theme(css.read_text(encoding="utf-8")) if css else None
    catalog = sorted(discover_catalog(root))
    parts = ["# design.md (généré)\n\n", "## Tokens\n\n"]
    if tokens:
        parts.append("Couleurs : " + ", ".join(sorted(tokens.colors)) + "\n")
        parts.append("Radii : " + ", ".join(sorted(tokens.radii)) + "\n")
    parts.append("\n## Composants\n\n" + "\n".join(f"- {c}" for c in catalog) + "\n\n")
    parts.append(_RULES)
    return "".join(parts)


def main(root: str = ".", out: str | None = None) -> None:
    """Génère design.md depuis les tokens @theme + le catalogue components/ui."""
    base = Path(root)
    target = Path(out) if out else base / "design.md"
    target.write_text(build_kit(base), encoding="utf-8")
    typer.echo(f"design.md écrit : {target}")
