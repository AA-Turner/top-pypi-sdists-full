# setup.py

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()
setup(
    name="ghost-encrypt",
    version="1.0.6",
    description="Cross-Platform tool for de-/encrypting strings, files and sock-streams. Still in development",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/NightKylo/ghost",
    author="Marius Kraus",
    license="Apache",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["ghost"],
    install_requires=["arg_parser"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "ghost=ghost.__main__:main",
        ]
    },
)
