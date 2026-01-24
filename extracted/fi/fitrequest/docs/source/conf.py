# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'fitrequest'
copyright = '2025, support@skillcorner.com'  # noqa: A001
author = 'SkillCorner'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosectionlabel',
    'sphinx_copybutton',
    'sphinx_design',
    'sphinx.ext.inheritance_diagram',
    'sphinxcontrib.autodoc_pydantic',
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}
autodoc_type_aliases = {'ValidMethodDecorator': 'fitrequest.method_decorator.ValidaMethodDecorator'}

html_theme_options = {
    'collapse_navigation': True,  # Enable collapsible sections
}

# https://autodoc-pydantic.readthedocs.io/en/stable/index.html
autodoc_pydantic_model_show_json = False
autodoc_pydantic_model_show_config_summary = False
autodoc_pydantic_model_show_validator_members = False
autodoc_pydantic_model_show_validator_summary = False
autodoc_pydantic_model_hide_reused_validator = True
autodoc_pydantic_model_hide_paramlist = True
autodoc_pydantic_field_list_validators = False
autodoc_pydantic_field_show_constraints = False
