#
# Copyright 2026 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
"""Exposes ``drdev`` to the DataRobot CLI as ``dr dev``."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
import json
import sys

DESCRIPTION = "Start development services from .taskfile-data.yaml or command line"
FALLBACK_VERSION = "0.0.0"


def _plugin_version() -> str:
    """The weekly build publishes under its own distribution name."""
    for distribution in ("datarobot", "datarobot_early_access"):
        try:
            # Truncated metadata yields None instead of raising.
            return version(distribution) or FALLBACK_VERSION
        except PackageNotFoundError:
            continue
    return FALLBACK_VERSION


def main() -> None:
    if sys.argv[1:2] == ["--dr-plugin-manifest"]:
        print(
            json.dumps({
                "name": "dev",
                "version": _plugin_version(),
                "description": DESCRIPTION,
                "authentication": False,
            })
        )
        return

    try:
        from datarobot.core.dev import cli_main, parser
    except ImportError as exc:
        sys.exit(f"dr dev needs the drdev dependencies ({exc}).\n\n    pip install 'datarobot[core]'\n")

    # argparse would take prog from argv[0] and print "dr-dev".
    parser.prog = "dr dev"
    cli_main()
