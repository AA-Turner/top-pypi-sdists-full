from pathlib import Path
from typing import List

from setuptools import find_packages, setup


def parse_requirements(file_name: str = "requirements.txt") -> List[str]:
    with Path.open(Path(__file__).parent / file_name, "r") as f:
        return f.readlines()


def get_long_description():
    with open("README.md", "r") as fh:
        return fh.read()


setup(
    name="pycarlo",
    use_scm_version=True,
    license="Apache Software License (Apache 2.0)",
    description="Monte Carlo's Python SDK",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Monte Carlo Data, Inc",
    author_email="info@montecarlodata.com",
    url="https://www.montecarlodata.com/",
    packages=find_packages(exclude=["tests*", "utils*", "examples*"]),
    include_package_data=True,
    install_requires=parse_requirements(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    setup_requires=["setuptools", "setuptools_scm"],
)
