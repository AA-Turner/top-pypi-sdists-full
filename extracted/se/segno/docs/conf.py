#
# segno documentation build configuration file
#
import os
import sys

sys.path.insert(0, os.path.abspath('..'))

import segno

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_paramlinks',
    'sphinx.ext.intersphinx',
]

autodoc_member_order = 'groupwise'

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

project = 'Segno'
copyright = '2016 - 2025 Lars Heuer -- "QR Code" and "Micro QR Code" are registered trademarks of DENSO WAVE INCORPORATED.'  # noqa: E501
author = 'Lars Heuer'
version = segno.__version__

language = 'en'

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

show_authors = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


html_theme = 'furo'  # 'sphinx_rtd_theme'  #'classic' #'alabaster'

html_theme_options = {
    'globaltoc_collapse': False
}

html_static_path = ['_static']

pygments_dark_style = 'lightbulb'

# Output file base name for HTML help builder.
htmlhelp_basename = 'segnodoc'


# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  (master_doc, 'segno.tex', 'Segno Documentation', 'Author', 'manual'),
]

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('man/segno', 'segno', 'Segno QR Code encoder', '', 1),
]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  (master_doc, 'segno', 'Segno Documentation',
   author, 'segno', 'One line description of project.',
   'Miscellaneous'),
]

# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ['search.html']
