# Copyright (c) 2021-2025 Cardiff University
# Distributed under the terms of the BSD-3-Clause license

import igwn_auth_utils
import sphinx_github_style

# -- metadata ---------------

project = "igwn-auth-utils"
copyright = "2021-2025 Cardiff University"
author = "Duncan Macleod"
top_module = igwn_auth_utils
release = top_module.__version__
version = release.split('.dev', 1)[0]

# -- sphinx config ----------

needs_sphinx = "4.0"
extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",
    "sphinx.ext.napoleon",
    "sphinx_automodapi.automodapi",
    "sphinx_copybutton",
    "sphinx_design",
]
default_role = "obj"

references_file = "references.rst"
excluded_patterns = [
    references_file,
]
rst_epilog = f"\n.. include:: /{references_file}"

# -- theme options ----------

html_theme = "furo"
html_title = f"{project} {version}"
templates_path = [
    "_templates",
]

# -- extensions -------------

# automodapi
automodapi_inherited_members = False

# autosummary
autosummary_generate = True
autoclass_content = "class"
autodoc_default_flags = [
    "show-inheritance",
    "members",
    "no-inherited-members",
]

# intersphinx
intersphinx_mapping = {
    "cryptography": ("https://cryptography.io/en/stable", None),
    "gssapi": ("https://pythongssapi.github.io/python-gssapi/", None),
    "python": ("https://docs.python.org/", None),
    "requests": ("https://requests.readthedocs.io/en/stable/", None),
    "requests-gracedb": (
        "https://requests-gracedb.readthedocs.io/en/stable/",
        None,
    ),
    "scitokens": ("https://scitokens.readthedocs.io/en/stable/", None),
}

# linkcode
linkcode_url = sphinx_github_style.get_linkcode_url(
    blob=sphinx_github_style.get_linkcode_revision("head"),
    url=f"https://git.ligo.org/computing/software/{project}",
)
linkcode_resolve = sphinx_github_style.get_linkcode_resolve(linkcode_url)
