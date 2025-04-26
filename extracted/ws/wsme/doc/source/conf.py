# -*- coding: utf-8 -*-
#
# Web Services Made Easy documentation build configuration file

# -- General configuration ----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'wsmeext.sphinxext',
    'sphinx.ext.intersphinx',
]

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Web Services Made Easy'
copyright = u'2011, Christophe de Vienne'

suppress_warnings = ['app.add_directive']

# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# html_theme = 'default'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# -- Options for sphinx.ext.autodoc extension ---------------------------------

autodoc_member_order = 'bysource'


# -- Options for sphinx.ext.intersphinx extension -----------------------------

intersphinx_mapping = {
    'python': ('http://docs.python.org/', None),
}


# -- Options for wsme.sphinxext extension -------------------------------------

wsme_protocols = [
    'restjson', 'restxml',
]


def setup(app):
    # confval directive taken from the sphinx doc
    app.add_object_type('confval', 'confval',
                        objname='configuration value',
                        indextemplate='pair: %s; configuration value')
