"""Sphinx configuration for textcharts."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, os.fspath(SRC))
sys.path.insert(0, os.path.abspath("_static"))

try:
    from pygments import styles
    from pygments_cobalt2 import Cobalt2Style

    styles.STYLE_MAP["cobalt2"] = "pygments_cobalt2::Cobalt2Style"

    import types

    cobalt2_module = types.ModuleType("pygments.styles.cobalt2")
    cobalt2_module.Cobalt2Style = Cobalt2Style
    sys.modules["pygments.styles.cobalt2"] = cobalt2_module
except ImportError as exc:
    print(f"Warning: Could not import Cobalt2Style: {exc}")

project = "textcharts"
author = "Joe Harris"
copyright = "2026, Joe Harris"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = ["_build"]

autosummary_generate = True
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_class_signature = "mixed"
autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
    "undoc-members": False,
}

pygments_style = "cobalt2"

html_theme = "furo"
html_static_path = ["_static"]
html_title = "textcharts documentation"
html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "top_of_page_buttons": ["view"],
    "light_css_variables": {
        "color-brand-primary": "#0088ff",
        "color-brand-content": "#0088ff",
        "color-highlight-on-target": "#ffc600",
    },
    "dark_css_variables": {
        "color-brand-primary": "#0088ff",
        "color-brand-content": "#0088ff",
        "color-highlight-on-target": "#ffc600",
    },
    "source_repository": "https://github.com/joeharris76/textcharts/",
    "source_branch": "main",
    "source_directory": "docs/",
}
html_css_files = [
    "custom.css",
]
html_js_files = [
    "collapsible-nav.js",
]

_MARKDOWN_CLASS_DOCS = {
    "textcharts.box_plot.BoxPlot",
    "textcharts.cdf_chart.CDFChart",
    "textcharts.comparison_bar.ComparisonBar",
    "textcharts.diverging_bar.DivergingBar",
    "textcharts.heatmap.Heatmap",
    "textcharts.histogram.Histogram",
    "textcharts.line_chart.LineChart",
    "textcharts.normalized_speedup.NormalizedSpeedup",
    "textcharts.scatter_plot.ScatterPlot",
}


def _sanitize_docstring(_app, what, name, _obj, _options, lines):
    """Replace markdown-fenced class docstrings with a short plain summary."""
    if what != "class" or name not in _MARKDOWN_CLASS_DOCS:
        return
    summary = next((line.strip() for line in lines if line.strip()), "")
    lines[:] = [summary]


def setup(app):
    """Register Sphinx hooks."""
    app.connect("autodoc-process-docstring", _sanitize_docstring)
