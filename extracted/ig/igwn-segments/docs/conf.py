#
# igwn-segments documentation build configuration file

from igwn_segments import __version__

# -- project information -------------

project = "igwn-segments"
copyright = "2018-2024, Kipp Cannon; 2024- Cardiff University, NASA GSFC"
author = "Kipp Cannon"

# The full version, including alpha/beta/rc tags.
release = __version__
# The short X.Y version.
version = release.split("+", 1)[0]

# -- general configuration -----------

# The reST default role (used for this markup: `text`) to use for all
# documents.
default_role = "obj"

templates_path = ["_templates"]

pygments_style = "monokai"
pygments_dark_style = "monokai"

# -- options for HTML output ---------

html_title = f"{project} {version}"

# The theme to use for HTML and HTML Help pages.
html_theme = "furo"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Output file base name for HTML help builder.
htmlhelp_basename = "igwn-segmentsdoc"

# -- extensions ----------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx_automodapi.automodapi",
    "sphinx_design",
]

# -- autosummary

autosummary_generate = True

# -- intersphinx

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}
