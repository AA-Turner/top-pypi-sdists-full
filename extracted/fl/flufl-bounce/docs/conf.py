import importlib.metadata
import os
import sys

from datetime import date

sys.path[0:0] = [
    os.path.abspath('../src'),
    os.path.abspath('_ext'),
]


extensions = [
    'issue_role',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
}

autoclass_content = 'both'

autodoc_default_options = {
    'exclude-members': '__weakref__',
    'private-members': False,
    'special-members': '__init__',
    'undoc-members': False,
    'typehints': 'both',
}

source_suffix = {'.rst': 'restructuredtext'}

master_doc = 'index'

project = 'flufl.bounce'
author = 'Barry Warsaw'
copyright = f'2004-{date.today().year}, {author}'

version = importlib.metadata.version(project)
release = version

exclude_patterns = ['_build']

pygments_style = 'sphinx'

html_theme = 'furo'

htmlhelp_basename = 'fluflbouncedoc'
