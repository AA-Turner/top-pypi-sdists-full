# (c) Copyright 2018 Palantir Technologies Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#!/usr/bin/env python
from setuptools import find_packages, setup, Command
from os import path, makedirs, system
import re
import subprocess
import sys

VERSION_PY_PATH = "conjure_python_client/_version.py"

GIT_REGEX_PATTERN = re.compile(
    r"^"
    + r"(?P<tag>[0-9]+\.[0-9]+\.[0-9]+)"
    + r"(-rc(?P<rc>[0-9]+))?"
    + r"(-(?P<distance>[0-9]+)-g(?P<hash>[a-f0-9]+))?"
    + r"(\.(?P<dirty>dirty))?"
    + r"$"
)


def convert_sls_version_to_python(sls_version: str) -> str:
    match = GIT_REGEX_PATTERN.match(sls_version)
    if not match:
        raise RuntimeError(f"Invalid SLS version {sls_version}")

    python_version = match.group("tag")
    rc_group = match.group("rc")
    distance_group = match.group("distance")
    hash_group = match.group("hash")
    dirty_group = match.group("dirty")

    if rc_group:
        python_version += "rc" + rc_group
    if distance_group:
        if not hash_group:
            raise RuntimeError(
                f"Cannot specify commit distance without hash for version {sls_version}"
            )
        python_version += "+" + distance_group + ".g" + hash_group
    if dirty_group:
        python_version += "." + dirty_group
    return python_version


if not path.exists(VERSION_PY_PATH):
    try:
        gitversion = (
            subprocess.check_output(
                "git describe --tags --always --first-parent".split()
            )
            .decode()
            .strip()
        )
        open(VERSION_PY_PATH, "w").write(
            '__version__ = "{}"\n'.format(
                convert_sls_version_to_python(gitversion)
            )
        )
        if not path.exists("build"):
            makedirs("build")
    except subprocess.CalledProcessError:
        print("outside git repo, not generating new version string")
exec(open(VERSION_PY_PATH).read())


class FormatCommand(Command):
    """Enables setup.py format."""

    description = "Reformat python files using 'black'"
    user_options = [
        ("check", "c", "Don't write the files back, just return the status")
    ]

    def initialize_options(self):
        self.check = False

    def finalize_options(self):
        if self.check != False:
            self.check = True
        pass

    def run(self):
        try:
            if self.check:
                code = self.blackCheck()
            else:
                code = self.black()
            if code == 0:
                sys.exit(0)
            else:
                sys.exit(1)
        except OSError:
            pass

    def black(self):
        return system("black --line-length 79 .")

    def blackCheck(self):
        return system("black --check --quiet --line-length 79 .")


setup(
    name="conjure-python-client",
    version=__version__,
    description="Conjure Python Library",
    # The project's main homepage.
    url="https://github.com/palantir/conjure-python-client",
    author="Palantir Technologies, Inc.",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=["test*", "integration*"]),
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=["requests"],
    tests_require=["pytest", "pyyaml"],
    python_requires=">=3.9",
    cmdclass={"format": FormatCommand},
    package_data={
        "conjure_python_client": ["py.typed"],
    },
)
