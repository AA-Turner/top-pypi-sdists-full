# -*- coding: utf-8 -*-
# Copyright (c) The python-semanticversion project
# This code is distributed under the two-clause BSD License.


from .base import compare, match, validate, SimpleSpec, NpmSpec, Spec, SpecItem, Version


__author__ = "Raphaël Barrois <raphael.barrois+semver@polytechnique.org>"
try:
    # Python 3.8+
    from importlib.metadata import version

    __version__ = version("semantic_version")
except ImportError:
    __version__ = "2.10.0"  # pkg_resources.get_distribution("python_agent.packages.semantic_version").version
