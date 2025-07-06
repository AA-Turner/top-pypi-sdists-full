#!/usr/bin/env python3
'''
Sphinx configuration file.
'''

# pylint: disable=invalid-name,redefined-builtin

import importlib
import pathlib
import sys

source_code = '../../src'
git_url = 'https://gitlab.inria.fr/jrye/requests-file-adapter'

this_path = pathlib.Path(__file__).resolve()
sys.path.insert(0, str((this_path.parent / source_code).resolve()))

author = 'Jan-Michael Rye'
copyright = '2024, Inria'
project = 'Requests File Adapter'
html_theme = 'sphinx_rtd_theme'

autodoc_mock_imports = [
    'psutil',
    'requests'
]
extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.linkcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo'
]
index_entries = []


def skip(_app, _what, name, _obj, would_skip, _options):  # pylint: disable=too-many-arguments
    '''Customize autodoc member skipping.'''
    if name == '__init__':
        return False
    return would_skip


def setup(app):
    '''Connect the skip function.'''
    app.connect('autodoc-skip-member', skip)


def linkcode_resolve(domain, info):
    '''Get source links for the linkcode extension.'''
    module = info['module']
    if domain != 'py' or not module:
        return None
    top_mod = importlib.import_module(module.split('.')[0])
    mod = importlib.import_module(module)
    top_mod_path = pathlib.Path(top_mod.__file__)
    mod_path = pathlib.Path(mod.__file__)
    subpath = str(mod_path.relative_to(top_mod_path.parent.parent))
    return f'{git_url}/-/blob/main/src/{subpath}'
