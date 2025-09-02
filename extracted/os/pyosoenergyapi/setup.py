"""Setup pyosoenergyapi package."""
import os
import re

import unasync
from setuptools import setup


def requirements_from_file(filename="requirements.txt"):
    """Get requirements from file."""
    with open(os.path.join(os.path.dirname(__file__), filename)) as r:
        reqs = r.read().strip().split("\n")
    # Return non empty lines and non comments
    return [r for r in reqs if re.match(r"^\w+", r)]


setup(
    version="1.2.4",
    cmdclass={
        "build_py": unasync.cmdclass_build_py(
            rules=[
                unasync.Rule(
                    "/apyosoenergyapi/",
                    "/pyosoenergyapi/",
                    additional_replacements={
                        "apyosoenergyapi": "pyosoenergyapi",
                    },
                )
            ]
        )
    },
    install_requires=requirements_from_file()
)