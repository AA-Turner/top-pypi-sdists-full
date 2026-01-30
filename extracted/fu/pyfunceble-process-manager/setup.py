"""
The tool to check the availability or syntax of domain, IP or URL.

-- The process manager library for and from the PyFunceble project.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

The process manager library for and from the PyFunceble project.

Welcome to PyFunceble!

This is a project that was initially part of the PyFunceble project. It aims to
separator the process manager from the main project.
The main goal behind that is to make the process manager available to other
projects that may need it without the need to install the whole PyFunceble
project.

Happy testing with PyFunceble!

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://docs.pyfunceble.com

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024, 2025, 2026 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import os
import re

import setuptools


def get_requirements(*, mode="standard"):
    """
    This function extract all requirements from requirements.txt.
    """

    mode2files = {
        "standard": ["requirements.txt"],
        "dev": ["requirements.dev.txt"],
        "test": ["requirements.test.txt"],
    }

    mode2files["full"] = [y for x in mode2files.values() for y in x]

    result = set()

    for file in mode2files[mode]:
        with open(file, "r", encoding="utf-8") as file_stream:
            for line in file_stream:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "#" in line:
                    line = line[: line.find("#")].strip()

                if not line:
                    continue

                result.add(line)

    return list(result)


def get_version():
    """
    This function will extract the version from
    PyFunceble/ext/process_manager/__about__.py.
    """

    to_match = re.compile(r'__version__.*=\s+"(.*)"')

    if os.path.exists("PyFunceble/ext/process_manager/__about__.py"):
        about_path = "PyFunceble/ext/process_manager/__about__.py"
    elif os.path.exists("../PyFunceble/ext/process_manager/__about__.py"):
        about_path = "../PyFunceble/ext/process_manager/__about__.py"
    else:
        raise FileNotFoundError("No __about__.py found.")

    with open(about_path, encoding="utf-8") as file_stream:
        extracted = to_match.findall(file_stream.read())[0]

    return extracted


def get_long_description():  # pragma: no cover
    """
    This function return the long description.
    """

    return open("README.md", encoding="utf-8").read()


if __name__ == "__main__":
    setuptools.setup(
        name="pyfunceble-process-manager",
        version=get_version(),
        python_requires=">=3.8, <4",
        install_requires=get_requirements(mode="standard"),
        extras_require={
            "dev": get_requirements(mode="dev"),
            "test": get_requirements(mode="test"),
            "full": get_requirements(mode="full"),
        },
        description="The process manager library for and from the PyFunceble project.",
        long_description=get_long_description(),
        long_description_content_type="text/markdown",
        author="funilrys",
        author_email="contact@funilrys.com",
        license="Apache 2.0",
        url="https://github.com/PyFunceble/process-manager",
        project_urls={
            "Source": "https://github.com/PyFunceble/process-manager/tree/master",
            "Tracker": "https://github.com/PyFunceble/process-manager/issues",
        },
        platforms=["any"],
        packages=setuptools.find_namespace_packages(
            exclude=("*.tests", "*.tests.*", "tests.*", "tests")
        ),
        include_package_data=True,
        keywords=[
            "PyFunceble",
            "process-manager",
        ],
        classifiers=[
            "Environment :: Console",
            "Topic :: Internet",
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved",
        ],
    )
