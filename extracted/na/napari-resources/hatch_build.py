"""Custom build hooks for generating logo assets during the package build."""

from __future__ import annotations

import sys
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

PROJECT_ROOT = Path(__file__).parent.resolve()
SRC_DIR = PROJECT_ROOT / "src"
LOGOS_DIR = SRC_DIR / "napari_resources" / "resources" / "logos"


class CustomBuildHook(BuildHookInterface):
    """Regenerate the logo SVGs before building the package."""

    def initialize(self, version: str, build_data: dict) -> None:
        """Generate all SVGs."""
        if self.target_name not in {"wheel", "editable", "sdist"}:
            return

        sys.path.insert(0, str(SRC_DIR))

        # generate all the logo SVGs from the templates and variants
        from napari_resources.generate_logos import generate_logos

        output_dir = LOGOS_DIR / "generated"

        output_dir.mkdir(parents=True, exist_ok=True)

        generate_logos(
            output_dir=output_dir,
            quiet=False,
            variants_dir=LOGOS_DIR / "variants",
            templates_dir=LOGOS_DIR / "templates",
        )
