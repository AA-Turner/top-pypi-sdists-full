import os

from setuptools import setup, find_packages

with open(os.path.join("codon_usage_data", "version.txt"), "r") as f:
    __version__ = f.read()

with open(os.path.join("python_codon_tables", "README.rst"), "r") as f:
    long_description = f.read()

setup(
    name="python_codon_tables",
    version=__version__,
    author="Zulko",
    description="Codon Usage Tables for Python, from kazusa.or.jp",
    url="https://github.com/Edinburgh-Genome-Foundry/codon-usage-tables",
    long_description=long_description,
    license="Public Domain",
    keywords="DNA codon usage",
    packages=find_packages(exclude="docs"),
    include_package_data=True,
    package_data={
        "python_codon_tables": ["../codon_usage_data/*", "../codon_usage_data/**/*"]
    },
)
