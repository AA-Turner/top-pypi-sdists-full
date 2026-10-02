"""pikobs -- observation diagnostics for data assimilation.

Installed by the environment file (pikobs_env.yml) from GitLab; developers
install their clone with ``pip install -e .``.
"""
from os import path

from setuptools import find_packages, setup

HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description = f.read()
with open(path.join(HERE, "VERSION"), encoding="utf-8") as f:
    version = f.read().strip()

setup(
    name="pikobs",
    version=version,
    url="https://gitlab.science.gc.ca/dlo001/Pikobs",
    license="GPL-3.0-or-later",
    author="David Lobon",
    author_email="dhlobon@gmail.com",
    description="Observation diagnostics for data assimilation: maps, sections, "
                "profiles and time series of the departures, and their tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["pikobs.script*", "pikobs.build_doc*"]),
    # the files pikobs reads at run time; the wrappers are downloaded with
    # wget, and the documentation tools stay in the repository
    package_data={
        "pikobs": ["extension/*.so", "extension/*.json"],
        "pikobs.configobs": ["*.json", "*.csv", "*.txt", "*.npz", "*.npy",
                             "regions_data/*"],
        "pikobs.mapobs": ["*.json", "*.csv", "*.txt", "*.png"],
    },
    python_requires=">=3.10",
    # what pikobs imports, nothing else; the environment file pins the same
    install_requires=[
        "numpy>=1.24,<2",
        "scipy>=1.10",
        "pandas>=2.0",
        "matplotlib>=3.8",
        "pillow",
        "cartopy>=0.22",
        "shapely>=2.0",
        "pyshp",
        "dask[distributed]>=2024.1",
        "rich",
        "global-land-mask",
    ],
)
