import os
from typing import Dict  # noqa: F401

from setuptools import setup

# Read version from hud_sdk/version.py since 'attr:' is not supported in setup.cfg in py35
version = {}  # type: Dict[str, str]
with open(os.path.join("src", "hud_sdk", "version.py")) as fp:
    exec(fp.read(), version)


setup(
    version=version["version"],
    entry_points={
        "console_scripts": [
            "hud-run = hud_sdk.entrypoint:main",
        ],
    },
)
