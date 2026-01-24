from json import loads
from os import environ
from os.path import abspath, dirname, join
from pathlib import Path
from platform import machine, system
from setuptools import setup
from setuptools.command.install import install
from sys import executable
from tarfile import open as taropen
from tempfile import TemporaryDirectory
from typing import Any, List
from urllib.request import Request, urlopen

# Run in python_pip directory.

package_version = environ.get("PACKAGE_VERSION", "1.0.0.40.14")
go_package_version = package_version
# If package version looks like 1.0.a.b.c, we assume a.b.c is the go binary version.
if go_package_version.count(".") == 4:
    go_package_version = ".".join(go_package_version.split(".")[2:])
name = environ.get("PYPI_NAMESPACE", "dbt")


def get_release_list() -> Any:
    """Returns go cli binary release list given package_version."""
    req = Request(
        f"https://api.github.com/repos/dbt-labs/dbt-cli/releases/tags/v{go_package_version}",
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urlopen(req) as resp:
        return loads(resp.read())


def download_binary(url) -> bytes:
    """Downloads and return binary bytes."""
    req = Request(url)
    with urlopen(req) as resp:
        return resp.read()


def lookup_asset_url(release_list: List[Any], go_binary_name: str) -> str:
    """Looks up if any release name has `go_binary_name` as substr. Exits 1 if not
    found."""
    for asset in release_list["assets"]:
        if go_binary_name in asset["name"]:
            return asset["browser_download_url"]
    exit(1)


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        release_list = get_release_list()
        sys = system().lower()
        mach = machine().lower()
        go_binary_name = "unknown"
        if sys == "darwin":
            go_binary_name = "darwin"
        elif sys == "linux":
            if mach == "amd64" or mach == "x86_64":
                go_binary_name = "linux_amd64"
            elif mach == "arm64" or mach == "aarch64":
                go_binary_name = "linux_arm64"
            else:
                exit(1)
        elif sys == "windows":
            if mach == "amd64" or mach == "x86_64":
                go_binary_name = "windows_amd64"
            elif mach == "arm64":
                go_binary_name = "windows_arm64"
            else:
                exit(1)
        else:
            exit(1)

        url = lookup_asset_url(release_list, go_binary_name)
        install_dir = Path(executable).parent
        with TemporaryDirectory() as temp_dir:
            temp_file = join(temp_dir, "temp.tar.gz")
            with open(temp_file, "wb") as file:
                file.write(download_binary(url))
            with taropen(temp_file) as tar:
                tar.extractall(install_dir)


desc = "The dbt Cloud CLI - an ELT tool for running SQL transformations and data models in dbt Cloud. For more documentation on these commands, visit: docs.getdbt.com"

this_directory = abspath(dirname(__file__))
with open(join(this_directory, "README.md")) as f:
    long_desc = f.read()

setup(
    name=name,
    platforms="any",
    version=package_version,
    description=desc,
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author="dbt Labs",
    author_email="info@dbtlabs.com",
    url="https://www.getdbt.com/",
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    cmdclass={
        "install": PostInstallCommand,
    },
    install_requires=["setuptools>=61.2"],
)
