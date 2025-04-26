#
# Copyright 2020 Stephan Mueller
#
# Licensed under the GPLv3 license

"""Setup for pylint_gitlab module."""

import json
import logging
import os
import subprocess

import setuptools

logger = logging.getLogger(__name__)


def get_install_requirements() -> list:
    """Retrieves list of packages from Pipfile.lock required for installation.

    Returns: List of packages
    """
    with open("Pipfile.lock", encoding="UTF-8") as file:
        pipfile = file.read()

    packages = []
    for name, _ in json.loads(pipfile)["default"].items():
        packages.append(name)
    return packages


def long_description() -> str:
    """Reads README.md

    Returns: Content of ``README.md``
    """
    with open("README.md", "r", encoding="UTF-8") as file:
        return file.read()


def version() -> str:
    """Tries to detect version based on selected strategy.

    Returns: Project version
    """

    version_strategy = os.getenv("VERSION_STRATEGY", "GIT_REF_NAME")

    if version_strategy == "GIT_COMMIT_SHA":

        if os.getenv("CI_COMMIT_SHA", "") != "":
            return os.getenv("CI_COMMIT_SHA")

        process = subprocess.run(["git", "rev-parse", "--quiet", "HEAD"], capture_output=True, check=True)
        commit_sha = process.stdout.decode().strip()
        if commit_sha is not None and commit_sha != "":
            return "0.0.0+commit" + commit_sha

    elif version_strategy == "GIT_REF_NAME":

        if os.getenv("CI_COMMIT_TAG", "") != "":
            return os.getenv("CI_COMMIT_TAG")

        if os.getenv("CI_COMMIT_REF_NAME", "") != "":
            branch = os.getenv("CI_COMMIT_REF_NAME")
        else:
            process = subprocess.run(["git", "symbolic-ref", "--quiet", "HEAD"], capture_output=True, check=True)
            branch = process.stdout.decode().strip().replace("refs/heads/", "", 1)

        if branch is not None and branch != "":
            return "0.0.0+" + branch.replace("/", "-")

    raise ValueError("Version could not be detected.")


setuptools.setup(
    name="pylint-gitlab",
    version=version(),
    author="Stephan Müller",
    author_email="mail@stephanmueller.eu",
    license='GPLv3',
    description="This project provides pylint formatters for a nice integration with GitLab CI.",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/smueller18/pylint-gitlab",
    packages=setuptools.find_packages(),
    install_requires=get_install_requirements(),
    package_data={
        "": ["templates/report.html.j2"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    project_urls={
        'Documentation': 'https://gitlab.com/smueller18/pylint-gitlab',
        'Source': 'https://gitlab.com/smueller18/pylint-gitlab',
        'Tracker': 'https://gitlab.com/smueller18/pylint-gitlab/issues',
    },
)
