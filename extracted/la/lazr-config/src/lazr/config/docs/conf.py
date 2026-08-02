#!/usr/bin/env python3
#
# lazr.config documentation build configuration file.

from lazr.config import __version__

# -- General configuration ------------------------------------------------

extensions = []
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"

project = "lazr.config"
copyright = "2008-2024, Canonical Ltd."
author = "LAZR Developers <lazr-developers@lists.launchpad.net>"

version = __version__
release = __version__

language = "en"
exclude_patterns = ["_build", "eggs"]
pygments_style = "sphinx"

# -- Options for HTML output ----------------------------------------------

html_theme = "alabaster"
html_static_path = []
html_sidebars = {
    "**": [
        "relations.html",
        "searchbox.html",
    ]
}

htmlhelp_basename = "lazrconfigdoc"
