#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Update the minimum Adafruit-PlatformDetect dependency in setup.py."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path


PYPI_URL = "https://pypi.org/pypi/Adafruit-PlatformDetect/json"
SETUP_PY = Path("setup.py")
REQUIREMENT_RE = re.compile(r'("Adafruit-PlatformDetect>=)([^"]+)(")')


def release_tuple(version: str) -> tuple[int, ...]:
    """Return the numeric release segment for simple PyPI version comparisons."""
    match = re.match(r"^\d+(?:\.\d+)*", version)
    if not match:
        raise ValueError(f"Unsupported version format: {version}")
    return tuple(int(part) for part in match.group(0).split("."))


def latest_pypi_version() -> str:
    with urllib.request.urlopen(PYPI_URL, timeout=30) as response:
        payload = json.load(response)
    return payload["info"]["version"]


def update_requirement(version: str) -> bool:
    setup_text = SETUP_PY.read_text(encoding="utf-8")
    match = REQUIREMENT_RE.search(setup_text)
    if not match:
        raise RuntimeError(
            "Could not find Adafruit-PlatformDetect requirement in setup.py"
        )

    current_version = match.group(2)
    if release_tuple(version) <= release_tuple(current_version):
        print(
            "Adafruit-PlatformDetect minimum is already current "
            f"({current_version}; latest is {version})"
        )
        return False

    updated_text = REQUIREMENT_RE.sub(rf"\g<1>{version}\3", setup_text, count=1)
    SETUP_PY.write_text(updated_text, encoding="utf-8")
    print(
        f"Updated Adafruit-PlatformDetect minimum from {current_version} to {version}"
    )
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "version",
        nargs="?",
        help="Version to set. Defaults to the latest Adafruit-PlatformDetect version on PyPI.",
    )
    args = parser.parse_args()

    version = args.version or latest_pypi_version()
    update_requirement(version)
    return 0


if __name__ == "__main__":
    sys.exit(main())
