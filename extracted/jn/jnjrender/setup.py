# setup.py

from setuptools import setup, find_packages

# Read version from the package
from jnjrender import __version__

setup(
    name="jnjrender",
    version=__version__,
    packages=find_packages(),
    description="An utility to render Jinja2 templates in rendered text, taking a yaml environment ",
    author="Andrea Michelotti",
    install_requires=[
        "jinja2",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "jnjrender=jnjrender.cli:main",
        ],
    },
)
