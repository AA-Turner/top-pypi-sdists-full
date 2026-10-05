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
    'sphinx_copybutton',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
}

autoclass_content = 'both'

copybutton_exclude = '.linenos, .gp, .go'

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

exclude_patterns = ['_build', 'build', 'eggs', '.tox']

pygments_style = 'sphinx'

# These two redirect on purpose and the URLs we publish are the right ones to publish.  The clone
# URL has to keep its .git suffix to be usable with git, even though a browser gets sent to the
# project page, and the bare Read the Docs URL is version agnostic, so it sends readers to
# whichever version is current rather than pinning the docs to today's.
linkcheck_allowed_redirects = {
    r'https://gitlab\.com/flufl/flufl\.bounce\.git': r'https://gitlab\.com/flufl/flufl\.bounce',
    r'https://fluflbounce\.readthedocs\.io': r'https://fluflbounce\.readthedocs\.io/en/stable/',
}

html_theme = 'furo'

htmlhelp_basename = 'fluflbouncedoc'
