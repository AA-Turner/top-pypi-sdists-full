#!/usr/bin/env python3
#
# lazr.restfulclient documentation build configuration file

from lazr.restfulclient import __version__

extensions = []
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"

project = "lazr.restfulclient"
copyright = "2008-2024, Canonical Ltd."
author = "LAZR Developers <lazr-developers@lists.launchpad.net>"

version = __version__
release = __version__

language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"
todo_include_todos = False

html_theme = "alabaster"
html_sidebars = {
    "**": [
        "relations.html",
        "searchbox.html",
    ]
}
htmlhelp_basename = "lazrrestfulclientdoc"
