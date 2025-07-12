from setuptools import setup, find_namespace_packages
from pathlib import Path


version = "1.2.0"
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    include_package_data=True,  # allow Extracting the JSON/YAML files specified in the manifest.in File.
    name="ob_metaflow_extensions",
    version=version,
    description="Outerbounds Platform Extensions for Metaflow",
    author="Outerbounds, Inc.",
    license="Commercial",
    packages=find_namespace_packages(include=["metaflow_extensions.*"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "boto3",
        "kubernetes",
        "ob-metaflow == 2.15.21.1",
    ],
)
