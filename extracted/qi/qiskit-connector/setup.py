# This computer program is Copyright (C) 2025 Dr. Jeffrey Chijioke-Uche
# @Copyright:  (c)2025 - Dr. Jeffrey Chijioke-Uche. [Copyrighted by U.S. Copyright Office]
# This computer program is for qiskit-connector, a Python package for quantum computing.
# Licensed under the Apache License, Version 2.0 & Creative Commons Attribution 4.0 International Public License
# (the "License"); you may not use this file except in compliance with the License.
# See LICENSE.txt or http://www.apache.org/licenses/LICENSE-2.0 for details.

import pathlib
from setuptools import setup, find_packages

# Define the path to the current directory
here = pathlib.Path(__file__).parent.resolve()

# Read long description from README.md
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="qiskit-connector",
    version = "2.4.6",
    author="Dr. Jeffrey Chijioke-Uche",
    author_email="sj@chijioke-uche.com",
    description="Quantum Computing Qiskit Connector For Quantum Backend Use In Realtime",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/schijioke-uche/qiskit-connector",
    project_urls={
        "Homepage": "https://github.com/schijioke-uche/pypi-qiskit-connector",
        "Source": "https://github.com/schijioke-uche/pypi-qiskit-connector",
        "Tracker": "https://github.com/schijioke-uche/pypi-qiskit-connector/issues",
        "Software Publisher": "https://doi.org/10.5281/zenodo.15304310",
    },
    classifiers=[
        "Environment :: Console",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Quantum Computing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Topic :: Software Development :: Assemblers",
        "Topic :: Software Development",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Code Generators",
        "Topic :: System :: Distributed Computing",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    packages=find_packages(include=["qiskit_connector", "qiskit_connector.*"]),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.32.3",
        "python-dotenv>=1.0.0",
        "qiskit>=2.0.0",
        "qiskit-ibm-runtime>=0.38.0",
        "pillow>=11.2.1"
    ],
    license="Apache License 2.0",
    license_files=("LICENSE",),
)
# This setup.py file is used to package the qiskit-connector module for distribution.
# It includes metadata about the package, such as its name, version, author, and description.
# It also specifies the required dependencies and the Python version compatibility.
# The setup function is called to create the package, and the find_packages function is used to automatically discover all packages and subpackages in the specified directory.
# The long description is read from the README.md file, and the package is classified according to its development status, intended audience, and other criteria.
# The package is licensed under the Apache License 2.0, and the license file is included in the package.