# dqsegdb2 documentation build configuration file

import re
import sys
from importlib import metadata

# -- metadata

project = "dqsegdb2"
copyright = "2018-2022, Cardiff University"
author = "Duncan Macleod"
release = metadata.version(project)
version = re.split(r"[\w-]", release)[0]

# -- config

default_role = "obj"

# -- extensions

extensions = [
    "sphinx.ext.ifconfig",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_automodapi.automodapi",
]

# Intersphinx directory
intersphinx_mapping = {
    "igwn-auth-utils": (
        "https://igwn-auth-utils.readthedocs.io/en/stable/",
        None,
    ),
    "igwn-segments": (
        "https://igwn-segments.readthedocs.io/en/stable/",
        None,
    ),
    "python": (
        f"https://docs.python.org/{sys.version_info.major}",
        None,
    ),
    "requests": (
        "https://requests.readthedocs.io/en/stable/",
        None,
    ),
    "scitokens": (
        "https://scitokens.readthedocs.io/en/stable/",
        None,
    ),
}

# don't inherit in automodapi
automodapi_inherited_members = False

# -- theme

html_theme = "furo"
