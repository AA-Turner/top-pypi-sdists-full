# Configuration file for the Sphinx documentation builder.
# For hfortix-fortios package

import os
import sys
from datetime import datetime

# Add the package to the Python path so autodoc can import it
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------
project = 'HFortix-FortiOS'
copyright = f'{datetime.now().year}, Herman W. Jacobsen'
author = 'Herman W. Jacobsen'

# The full version, including alpha/beta/rc tags
try:
    from hfortix_fortios import __version__
    release = __version__
    version = '.'.join(__version__.split('.')[:2])
except ImportError:
    release = '0.5.154-beta'
    version = '0.5'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'myst_parser',
    'sphinx_copybutton',
    'sphinx_design',
    'sphinx_autodoc_typehints',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

suppress_warnings = ['myst.header']
toctree_maxdepth = 3

# Performance optimizations
import multiprocessing
import os

# Use all available cores for parallel processing
num_cores = multiprocessing.cpu_count()
parallel_read = num_cores
parallel_write = num_cores

# Skip expensive operations during build
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
autodoc_typehints_format = 'short'

# Speed up autosummary
autosummary_generate = True
autosummary_imported_members = False

# Reduce memory usage
keep_warnings = 10  # Only keep last 10 warnings

# Disable slow features for ReadTheDocs builds
if os.environ.get('READTHEDOCS') == 'True':
    # Skip intersphinx inventory loading (slow)
    intersphinx_timeout = 5
    # Optimize navigation for large doc sets
    html_theme_options = {
        'navigation_depth': 4,  # Keep full depth
        'collapse_navigation': False,  # Keep expanded so users can see content
        'sticky_navigation': True,
        'includehidden': True,
        'titles_only': False,  # Show full navigation (not just titles)
    }
else:
    html_theme_options = {
        'navigation_depth': 4,
        'collapse_navigation': False,
        'sticky_navigation': True,
        'includehidden': True,
        'titles_only': False,
    }

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']

# html_theme_options defined above based on environment

html_context = {
    'display_github': True,
    'github_user': 'hermanwjacobsen',
    'github_repo': 'hfortix-fortios',
    'github_version': 'main',
    'conf_py_path': '/docs/source/',
}

# -- Intersphinx mapping -----------------------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'hfortix-core': ('https://hfortix-core.readthedocs.io/en/latest/', None),
}

# Autosummary and Napoleon settings defined above

# -- Napoleon settings (full configuration) ----------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None
