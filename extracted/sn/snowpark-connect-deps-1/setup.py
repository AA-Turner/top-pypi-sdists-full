"""Setup script for snowpark_connect_deps_1 package."""
import os

from setuptools import find_packages, setup

VERSION = "3.56.4"

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

setup(
    name="snowpark-connect-deps-1",
    version=VERSION,
    description="Spark JAR dependencies for Snowpark Connect (Part 1)",
    long_description="Spark framework JAR files for Snowpark Connect. This package contains Apache Spark 3.5.6 core components.",
    long_description_content_type="text/markdown",
    author="Snowflake, Inc",
    license="Apache License, Version 2.0",
    license_files=["LICENSE.txt", "LICENSE-binary", "NOTICE-binary"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "snowpark_connect_deps_1": ["jars/*.jar"],
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
