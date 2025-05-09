# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import pkg_resources

# -- Project information -----------------------------------------------------

project = 'Schemdraw'
copyright = '2025, Collin J. Delker'
author = 'Collin J. Delker'

# The full version, including alpha/beta/rc tags

release = pkg_resources.get_distribution(project).version

# -- General configuration ---------------------------------------------------

locale_dirs = ['locale/']
gettext_compact = False

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'jupyter_sphinx',
    'sphinx.ext.autodoc',
    'sphinx.ext.autodoc.typehints',
    'sphinx.ext.napoleon',
    'sphinxcontrib.cairosvgconverter',
]

# Add any paths that contain templates here, relative to this directory.
#templates_path = ['_templates']
templates_path = []

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']
html_static_path = []

master_doc = 'index'  # See https://github.com/readthedocs/readthedocs.org/issues/2569

latex_elements = {
     'preamble': r'\DeclareUnicodeCharacter{03A9}{\ensuremath{\Omega}}' +
                 r'\DeclareUnicodeCharacter{03BC}{\ensuremath{\mu}}' +
                 r'\DeclareUnicodeCharacter{2184}{\ensuremath{\supset}}' +
                 r'\DeclareUnicodeCharacter{2295}{\ensuremath{\oplus}}' +
                 r'\DeclareUnicodeCharacter{2228}{\ensuremath{\vee}}' +
                 r'\DeclareUnicodeCharacter{22BB}{\ensuremath{\veebar}}' +
                 r'\DeclareUnicodeCharacter{01C1}{\ensuremath{\parallel}}' +
                 r'\DeclareUnicodeCharacter{2220}{\ensuremath{\angle}}' +
                 r'\DeclareUnicodeCharacter{2227}{\ensuremath{\wedge}}' +
                 r'\DeclareUnicodeCharacter{2212}{\ensuremath{-}}'
}
