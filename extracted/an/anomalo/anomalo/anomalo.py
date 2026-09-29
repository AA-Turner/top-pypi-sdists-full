#!/usr/bin/env python

from __future__ import annotations

import sys

import fire

from .cli.cli import CLI
from .client import Client, client_version  # noqa
from .encoder import Encoder  # noqa
from .update_check import UpdateNotice


def main() -> None:
    # stderr, so output piped from stdout (JSON, pulled files) stays parseable.
    version = client_version()
    print(f"anomalo CLI version {version}", file=sys.stderr)
    update_notice = UpdateNotice(version).start()
    try:
        fire.Fire(CLI, name="anomalo")
    finally:
        update_notice.report()


if __name__ == "__main__":
    main()
