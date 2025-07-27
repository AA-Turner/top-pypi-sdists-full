"""Setup.py entry point for supporting editable installs

Configuration is handled by setuptools through setup.cfg
https://setuptools.readthedocs.io/en/latest/setuptools.html
"""

from pathlib import Path

import setuptools

# Read the simple deprecation README
this_directory = Path(__file__).parent
readme_content = (this_directory / "README.md").read_text()

# Name is added here for GitHub's dependency graph
setuptools.setup(
    name="hijri-converter",
    long_description=readme_content,
    long_description_content_type="text/markdown",
)
