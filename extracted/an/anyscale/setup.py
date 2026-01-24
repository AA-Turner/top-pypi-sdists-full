import os
import re

from setuptools import find_packages, setup


# mypy: ignore-errors


def find_version(path):
    with open(path) as f:
        match = re.search(
            r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.MULTILINE,
        )
        if match:
            return match.group(1)
        raise RuntimeError("Unable to find version string.")


def read_requirements(path):
    with open(path) as f:
        return [line.strip() for line in f.readlines()]


_gcp_extra_requires = [
    "google-api-python-client",
    "google-cloud-secret-manager",
    "google-cloud-compute",
    "google-cloud-resource-manager",
    "google-cloud-filestore",
    "google-cloud-storage",
    "google-cloud-redis",
    "google-cloud-certificate-manager",
]

_all_extra_requires = _gcp_extra_requires + ["ray>=2.0.0"]

# If adding new webterminal deps,
# Update backend/server/services/application_templates_service.py
# to prevent users from uninstalling them.
_backend_extra_requires = _gcp_extra_requires + [
    "terminado",
    "tornado",
]

extras_require = {
    "gcp": _gcp_extra_requires,
    "all": _all_extra_requires,
    "backend": _backend_extra_requires,
}


def package_files(directory):
    paths = []
    for path, _, filenames in os.walk(directory):
        if os.path.basename(path) == "tests":  # skip test directory
            continue
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths


VERSION_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "anyscale", "version.py"
)
REQUIREMENTS_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "requirements.in"
)

with open("README.md") as fh:
    long_description = fh.read()


setup(
    name="anyscale",
    version=find_version(VERSION_PATH),
    author="Anyscale Inc.",
    description=("Command Line Interface for Anyscale"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[*find_packages(exclude=["tests", "tests.*"])],
    setup_requires=["setuptools_scm"],
    python_requires=">=3.9,<3.14",
    package_data={
        "": [
            "anyscale/webterminal/bash-preexec.sh",
            "anyscale/_private/docgen/api.md",
            "anyscale/_private/docgen/models.md",
            "requirements.in",
            "*.yaml",
            "*.json",
            *package_files("anyscale/client"),
            *package_files("anyscale/sdk"),
        ],
    },
    install_requires=read_requirements(REQUIREMENTS_PATH),
    extras_require=extras_require,
    entry_points={"console_scripts": ["anyscale=anyscale.scripts:main"]},
    include_package_data=True,
    zip_safe=False,
    license_files=["LICENSE", "NOTICE"],
    license="AS License",
)
