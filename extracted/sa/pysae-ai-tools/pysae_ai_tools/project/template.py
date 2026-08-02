"""Load the bundled ``.pysae-ai-tools.yaml`` template (shared by init + render)."""

import importlib.resources


def get_template() -> str:
    """Return the bundled, fully-commented ``.pysae-ai-tools.yaml`` template."""
    return (
        importlib.resources.files("pysae_ai_tools.project.templates")
        .joinpath("pysae-ai-tools.yaml")
        .read_text(encoding="utf-8")
    )
