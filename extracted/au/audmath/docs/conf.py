import os
import shutil

import toml

import audeer


config = toml.load(audeer.path("..", "pyproject.toml"))


# Project -----------------------------------------------------------------
project = config["project"]["name"]
author = ", ".join(author["name"] for author in config["project"]["authors"])
version = audeer.git_repo_version()
title = "{} Documentation".format(project)


# General -----------------------------------------------------------------
master_doc = "index"
source_suffix = ".rst"
exclude_patterns = [
    "api-src",
    "build",
    "tests",
    "Thumbs.db",
    ".DS_Store",
]
templates_path = ["_templates"]
pygments_style = None
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # support for Google-style docstrings
    "sphinx.ext.autosummary",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.katex",
    "matplotlib.sphinxext.plot_directive",
]
intersphinx_mapping = {
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "python": ("https://docs.python.org/3/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
}
linkcheck_ignore = [
    "https://gitlab.audeering.com",
    "https://github.com/dougthor42/PyErf/blob/cf38a2c62556cbd4927c9b3f5523f39b6a492472/pyerf/pyerf.py#L183-L287",
]
copybutton_prompt_text = r">>> |\.\.\. |$ "
copybutton_prompt_is_regexp = True

# Disable auto-generation of TOC entries in the API
# https://github.com/sphinx-doc/sphinx/issues/6316
toc_object_entries = False

# Matplot plot_directive settings
plot_html_show_source_link = False
plot_html_show_formats = False
plot_formats = ["png"]
plot_rcparams = {"font.size": 13}


# HTML --------------------------------------------------------------------
html_theme = "sphinx_audeering_theme"
html_theme_options = {
    "display_version": True,
    "footer_links": False,
    "logo_only": False,
}
html_context = {
    "display_github": True,
}
html_title = title


# Copy API (sub-)module RST files to docs/api/ folder ---------------------
audeer.rmdir("api")
audeer.mkdir("api")
api_src_files = audeer.list_file_names("api-src")
api_dst_files = [
    audeer.path("api", os.path.basename(src_file)) for src_file in api_src_files
]
for src_file, dst_file in zip(api_src_files, api_dst_files):
    shutil.copyfile(src_file, dst_file)
