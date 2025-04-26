"""
Comply with PEP 517's restictions on in-tree backends.

We use setuptools to package Incremental and want to activate
the in-tree Incremental plugin to manage its own version. To do
this we specify ``backend-path`` in our ``pyproject.toml``,
but PEP 517 requires that when ``backend-path`` is specified:

> The backend code MUST be loaded from one of the directories
> specified in backend-path (i.e., it is not permitted to
> specify backend-path and not have in-tree backend code).

We comply by re-publishing setuptools' ``build_meta``.
"""

from setuptools import build_meta

__all__ = ["build_meta"]
