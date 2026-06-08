# Configuration file for the Sphinx documentation builder.

from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore[no-redef]

_THIS_DIR = Path(__file__).parent
_REPO = _THIS_DIR.parent.parent
_PYPROJECT = _REPO / "pyproject.toml"

with open(_PYPROJECT, "rb") as _f:
    pyproject = tomllib.load(_f)
nitpicky = True

nitpick_ignore = [
    ("py:class", "Token"),
    ("py:class", "'Token'"),
]

nitpick_ignore_regex = [
    ("py:class", r".*lark.*"),
]

version = pyproject["project"]["version"]
release = version

# -- Project information

project = "sh"
copyright = "2023, Andrew Moffat"
author = "Andrew Moffat"

# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
    "lark": ("https://lark-parser.readthedocs.io/en/latest/", None),
    "jinja2": ("https://jinja.palletsprojects.com/en/latest/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

html_theme = "sphinx_rtd_theme"

# -- Options for EPUB output
epub_show_urls = "footnote"

autodoc_typehints = "both"

add_module_names = False
