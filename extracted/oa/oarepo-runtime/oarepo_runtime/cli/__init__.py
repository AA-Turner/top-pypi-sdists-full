#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""OAREPO Runtime CLI module."""

from __future__ import annotations

from importlib.metadata import entry_points

import click

from .search import init as search_init  # noqa just to register it


@click.group
def oarepo() -> None:
    """OARepo commands. See invenio oarepo --help for details."""


# register additional commands to the oarepo group
for ep in entry_points(group="oarepo.cli"):
    oarepo.add_command(ep.load())  # pragma: nocover
