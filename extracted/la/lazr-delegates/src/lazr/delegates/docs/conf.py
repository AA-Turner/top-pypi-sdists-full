#!/usr/bin/env python3
#
# lazr.delegates documentation build configuration file.
#
# This file is execfile()d with the current directory set to its
# containing dir.

from lazr.delegates import __version__

# -- General configuration ------------------------------------------------

extensions = []

templates_path = ["_templates"]

source_suffix = ".rst"

master_doc = "index"

project = "lazr.delegates"
copyright = "2013-2021, LAZR developers"
author = "LAZR Developers <lazr-developers@lists.launchpad.net>"

version = __version__
release = __version__

language = "en"

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

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

htmlhelp_basename = "lazrdelegatesdoc"
