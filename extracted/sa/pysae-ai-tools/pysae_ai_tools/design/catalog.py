from pathlib import Path

# Primitives HTML qui ont en général un équivalent dans un design system.
PRIMITIVES = ("button", "input", "select", "textarea", "table")
# Emplacements conventionnels du catalogue de composants (auto-découverte).
UI_DIRS = ("components/ui", "src/components/ui")


def discover_catalog(root: Path) -> set[str]:
    """Noms de composants déclarés dans le dossier components/ui/ du projet."""
    names: set[str] = set()
    for rel in UI_DIRS:
        ui = root / rel
        if ui.is_dir():
            names |= {f.stem for f in ui.glob("*.tsx")}
    return names


def primitive_suggestions(catalog: set[str]) -> dict[str, str]:
    """Meilleur composant catalogue pour chaque primitive (match exact puis sous-chaîne)."""
    out: dict[str, str] = {}
    for p in PRIMITIVES:
        match = next((c for c in sorted(catalog) if c.lower() == p), None) or next(
            (c for c in sorted(catalog) if p in c.lower()), None
        )
        if match:
            out[p] = match
    return out
