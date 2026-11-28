from __future__ import annotations

from importlib.metadata import version

import hatchling_autoextras_hook


def test_version_is_the_version_of_the_distribution() -> None:
    assert hatchling_autoextras_hook.__version__ == version("hatchling-autoextras-hook")
