#
# igwn-ligolw documentation build configuration file

from igwn_ligolw import __version__ as VERSION

# -- project information -------------

project = "igwn-ligolw"
copyright = "2018-2024, Kipp Cannon; 2024- Cardiff University, NASA GSFC"
author = "Kipp Cannon"

# The full version, including alpha/beta/rc tags.
release = VERSION
# The short X.Y version.
version = release.split("+", 1)[0]

# -- general configuration -----------

# The reST default role (used for this markup: `text`) to use for all
# documents.
default_role = "obj"

pygments_dark_style = "monokai"

# -- options for HTML output ---------

html_title = f"{project} {version}"

# The theme to use for HTML and HTML Help pages.
html_theme = "furo"

# -- extensions ----------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx_automodapi.automodapi",
    "sphinx_design",
]

# -- automodapi

automodapi_inherited_members = False

# -- autosummary

autosummary_generate = True

# -- intersphinx

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}
