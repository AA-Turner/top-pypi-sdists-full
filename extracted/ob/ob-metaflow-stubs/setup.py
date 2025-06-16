import os
import shutil
from setuptools import setup

source_file = "../metaflow/version.py"
destination_file = "./version.py"

if not os.path.exists(destination_file):
    shutil.copy(source_file, destination_file)

with open(destination_file, mode="r") as f:
    version = f.read().splitlines()[0].split("=")[1].strip(" \"'")

setup(
    include_package_data=True,
    name="ob-metaflow-stubs",
    version=version,
    description="Metaflow Stubs: Stubs for the metaflow package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Netflix, Outerbounds & the Metaflow Community",
    author_email="help@outerbounds.co",
    license="Apache License 2.0",
    packages=["metaflow-stubs"],
    package_data={"metaflow-stubs": ["generated_for.txt", "py.typed", "**/*.pyi"]},
    py_modules=["metaflow-stubs"],
    python_requires=">=3.7.0",
)
