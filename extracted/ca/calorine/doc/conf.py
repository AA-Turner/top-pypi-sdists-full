#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.graphviz',
    'sphinx.ext.ifconfig',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
    'sphinx_sitemap',
    'sphinx_design',
    'nbsphinx',
]

graphviz_output_format = 'svg'
templates_path = ['_templates']
default_role = 'code'
source_suffix = '.rst'
master_doc = 'index'
pygments_style = 'sphinx'
todo_include_todos = False

# Collect basic information from main module
metadata = importlib.metadata.metadata('calorine')
version = metadata.get('Version', 'n/a')
project = metadata.get('Name', 'n/a')
author = metadata.get('Author', 'n/a')

site_url = 'https://calorine.materialsmodeling.org/'
html_js_files = ['delete_empty_code_blocks.js',
                 'hidden_cells.js']
html_css_files = ['custom.css',
                  'hidden_cells.css']
html_logo = '_static/logo.png'
html_favicon = '_static/logo.ico'
html_static_path = ['_static']
htmlhelp_basename = 'calorinedoc'
intersphinx_mapping = {
    'ase':     ('https://wiki.fysik.dtu.dk/ase', None),
    'numpy':   ('https://numpy.org/doc/stable/', None),
    'h5py':    ('http://docs.h5py.org/en/latest/', None),
    'scipy':   ('https://scipy.github.io/devdocs/', None),
    'sklearn': ('https://scikit-learn.org/stable', None),
}

# sphinx theme configuration
html_theme = 'pydata_sphinx_theme'
html_theme_options = {
    'secondary_sidebar_items': ['page-toc'],
    'switcher': {
        'json_url': 'https://calorine.materialsmodeling.org/_static/switcher.json',
        'version_match': version,
    },
    'navbar_start': ['navbar-logo', 'version-switcher'],
}
html_sidebars = {
    'get_started': [],
    'credits': [],
    'genindex': [],
}

# Settings for nbsphinx
nbsphinx_execute = 'never'

# Options for LaTeX output
_PREAMBLE = r"""
\usepackage{amsmath,amssymb}
\renewcommand{\vec}[1]{\boldsymbol{#1}}
\DeclareMathOperator*{\argmin}{\arg\!\min}
\DeclareMathOperator{\argmin}{\arg\!\min}
"""

latex_elements = {
    'preamble': _PREAMBLE,
}
latex_documents = [
    (master_doc, 'calorine.tex', 'calorine Documentation',
     'The calorine developer team', 'manual'),
]


# Options for manual page output
man_pages = [
    (master_doc, 'calorine', 'calorine Documentation',
     [author], 1)
]


# Options for Texinfo output
texinfo_documents = [
    (master_doc, 'calorine', 'calorine Documentation',
     author, 'calorine', 'Strong coupling calculator',
     'Miscellaneous'),
]
