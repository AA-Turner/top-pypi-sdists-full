from datetime import date

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Monte Carlo's CLI"
copyright = f"{date.today().year}, Monte Carlo Data, Inc"
author = "Monte Carlo Data, Inc"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx_click"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]

html_theme_options = {
    "external_links": [
        {"name": "Dashboard", "url": "https://getmontecarlo.com"},
        {"name": "API reference", "url": "https://apidocs.getmontecarlo.com/"},
        {"name": "Product docs", "url": "https://docs.getmontecarlo.com/"},
    ],
    "favicons": [
        {
            "rel": "icon",
            "sizes": "16x16",
            "href": "logo.png",
        }
    ],
    "logo": {
        "text": "Monte Carlo's CLI Reference",
    },
    "search_bar_text": "Search",
    "show_toc_level": 2,
}

html_context = {"default_mode": "dark"}
