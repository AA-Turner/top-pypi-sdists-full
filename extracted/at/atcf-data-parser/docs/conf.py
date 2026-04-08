"""Configuration file for the Sphinx documentation builder."""

import os
import sys
from datetime import datetime
from typing import Any

# Insert the parent directory into the path
sys.path.insert(0, os.path.abspath("../"))

project = "atcf-data-parser"
year = datetime.now().year
copyright = f"{year} palewire"

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_baseurl = "/docs/"
html_theme = "palewire"
html_sidebars: dict[Any, Any] = {}
html_theme_options: dict[Any, Any] = {
    "canonical_url": f"https://palewi.re/docs/{project}/",
    "nosidebar": True,
}

autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "show-inheritance": True,
}
autodoc_mock_imports = ["pytz"]

extensions = [
    "myst_parser",
    "sphinx_click",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinxcontrib.mermaid",
]
