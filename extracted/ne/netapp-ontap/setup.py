"""
Copyright &copy; 2024 NetApp Inc. All rights reserved.

This module defines how the netapp_ontap library gets built/installed. Build the
package by running "python3 setup.py sdist bdist_wheel"
"""

import os
import setuptools
from pathlib import Path

# Read the content of README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "netapp_ontap" / "README.md").read_text(
    encoding="utf-8"
)

setuptools.setup(
    name=os.getenv("PACKAGE_NAME", "netapp-ontap"),
    version="9.16.1.0",
    author="NetApp",
    author_email="ng-ontap-rest-python-lib@netapp.com",
    description="A library for working with ONTAP's REST APIs simply in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.netapp.com/developer/",
    project_urls={
        "Documentation": "https://library.netapp.com/ecmdocs/ECMLP3331665/html/index.html",
    },
    keywords="NetApp ONTAP REST API development",
    packages=setuptools.find_packages(),
    package_data={
        "netapp_ontap": ["py.typed", "README.md"],
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "marshmallow>=3.21.3",
        "requests>=2.32.3",
        "requests-toolbelt>=1.0.0",
        "urllib3>=1.26.7",
        "certifi>=2022.12.7",
    ],
    python_requires=">=3.9",
    include_package_data=True,
)
