"""Setup script for snowpark_connect_deps_2 package."""
import os

from setuptools import find_packages, setup

VERSION = "3.56.3"

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

setup(
    name="snowpark-connect-deps-2",
    version=VERSION,
    description="Supporting JAR dependencies for Snowpark Connect (Part 2)",
    long_description="Supporting library JAR files for Snowpark Connect. This package contains Scala, Jackson, Commons, and other dependency JARs.",
    long_description_content_type="text/markdown",
    author="Snowflake, Inc",
    license="Apache License, Version 2.0",
    license_files=["LICENSE.txt", "LICENSE-binary", "NOTICE-binary"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "snowpark_connect_deps_2": ["jars/*.jar"],
    },
    python_requires=">=3.10,<3.13",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Java",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries",
    ],
)
