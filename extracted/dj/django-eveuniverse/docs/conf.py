# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

import django

sys.path.insert(0, os.path.abspath(".."))
os.environ["DJANGO_SETTINGS_MODULE"] = "testsite.settings"
django.setup()


# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "django-eveuniverse"
copyright = "2020-22, Erik Kalkoken"
author = "Erik Kalkoken"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",
    "sphinxcontrib_django2",
    "sphinx_copybutton",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

master_doc = "index"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]
html_logo = "https://imgpile.com/images/9sfnDo.png"

html_theme_options = {
    "description": (
        "Complete set of Eve Universe models with on-demand loading from ESI."
    ),
    "fixed_sidebar": True,
    "badge_branch": "master",
    "show_powered_by": False,
    "sidebar_collapse": True,
    "extra_nav_links": {
        "Report Issues": "https://gitlab.com/ErikKalkoken/django-eveuniverse/-/issues",
    },
}


# autodoc
add_module_names = False
autodoc_default_options = {
    "members": True,
    "member-order": "alphabetical",
    "undoc-members": False,
    "exclude-members": (
        "__weakref__, DoesNotExist, MultipleObjectsReturned, "
        "children, get_next_by_last_updated, "
        "get_previous_by_last_updated"
    ),
}
