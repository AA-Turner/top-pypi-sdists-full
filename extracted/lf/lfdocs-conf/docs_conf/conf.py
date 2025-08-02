#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: EPL-1.0
##############################################################################
# Copyright (c) 2017-2018 The Linux Foundation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
##############################################################################
"""LF Sphinx Docs Config.

Configure sphinx-doc through an YAML file.
"""

import datetime
import importlib
import os.path

import sphinx_bootstrap_theme
import yaml


def _merge_yaml(x, y):
    """Merge dictionary 'y' into 'x'.

    This transaction will overwrite existing data values in "y" with values
    from "x".
    """
    z = x.copy()
    z.update(y)
    return z


def collect_project_and_config():
    """Pull project and configuration by merging all config sources.

    Order of precedence:

    1) local conf.yaml
    2) defaults/PROJECT.yaml
    3) defaults/default.yaml

    Return the project name and merged configs from the calling project
    and per-project defaults.
    """
    if not os.path.isfile("conf.yaml"):
        raise IOError("No conf.yaml file found at: {}".format(os.getcwd()))

    with open("conf.yaml", "r") as f:
        local_config = yaml.safe_load(f)

    project_cfg = local_config.get("project_cfg", None)

    docs_path = importlib.util.find_spec("docs_conf").submodule_search_locations[0]

    default_cfg = os.path.join(docs_path, "defaults", "default.yaml")
    with open(os.path.join(docs_path, default_cfg), "r") as f:
        effective_config = yaml.safe_load(f)

    project_cfg_file = os.path.join(
        docs_path, "defaults", "{}.yaml".format(project_cfg)
    )
    if os.path.isfile(project_cfg_file):
        with open(os.path.join(docs_path, project_cfg_file), "r") as f:
            _project_cfg_data = yaml.safe_load(f)
        effective_config = _merge_yaml(effective_config, _project_cfg_data)

    effective_config = _merge_yaml(effective_config, local_config)

    return effective_config


cfg = collect_project_and_config()

# Parse the config and pull in sphinx conf.py settings
project = cfg.get("project")
version = cfg.get("version")
release = cfg.get("release", version)
author = cfg.get("author")
copyright = cfg.get("copyright").format(datetime.datetime.now().year)

needs_sphinx = cfg.get("needs_sphinx", "1.0")
exclude_patterns = cfg.get("exclude_patterns", [])
extensions = cfg.get("extensions", [])
language = cfg.get("language", "en")
master_doc = cfg.get("master_doc", "index")
pygments_style = cfg.get("pygments_style", "sphinx")
source_suffix = cfg.get("source_suffix", ".rst")
templates_path = cfg.get("templates_path", ["_templates"])
todo_include_todos = cfg.get("todo_include_todos", False)

html_extra_path = cfg.get("html_extra_path", [])
html_favicon = cfg.get("html_favicon", None)
html_logo = cfg.get("html_logo", None)
html_sidebars = cfg.get("html_sidebars", {"**": ["localtoc.html", "relations.html"]})
html_static_path = cfg.get("html_static_path", [])
html_theme = cfg.get("html_theme", "bootstrap")
html_theme_options = cfg.get(
    "html_theme_options",
    {
        "bootswatch_theme": "cerulean",
        "navbar_sidebarrel": False,
        "source_link_position": "footer",
    },
)
if html_theme == "opnfv":
    import sphinx_opnfv_theme

    html_theme_path = sphinx_opnfv_theme.get_html_theme_path()
else:
    html_theme_path = cfg.get(
        "html_theme_path", sphinx_bootstrap_theme.get_html_theme_path()
    )
htmlhelp_basename = cfg.get("htmlhelp_basename", "DocsConf")

intersphinx_mapping = {
    "common-packer": (
        "https://docs.releng.linuxfoundation.org/projects/common-packer/en/stable/",
        None,
    ),
    "global-jjb": (
        "https://docs.releng.linuxfoundation.org/projects/global-jjb/en/stable/",
        None,
    ),
    "lfdocs": ("https://docs.releng.linuxfoundation.org/en/latest/", None),
    "lfdocs-conf": (
        "https://docs.releng.linuxfoundation.org/projects/lfdocs-conf/en/stable/",
        None,
    ),
    "lftools": (
        "https://docs.releng.linuxfoundation.org/projects/lftools/en/stable/",
        None,
    ),
    "pipelines": (
        "https://docs.releng.linuxfoundation.org/projects/pipelines/en/latest/",
        None,
    ),
    "python": ("https://docs.python.org/3", None),
}
