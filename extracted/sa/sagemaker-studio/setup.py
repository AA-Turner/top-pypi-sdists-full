import os
from pathlib import Path

from setuptools import Command, find_namespace_packages, setup

VERSION = Path(__file__).parent.joinpath("VERSION").read_text()

data_files = []
for root, dirs, files in os.walk("configuration"):
    data_files.append(
        (os.path.relpath(root, "configuration"), [os.path.join(root, f) for f in files])
    )

with open("README.md", "r") as f:
    long_description = f.read()

AMZN_PACKAGE_NAME_PREFIX = os.environ.get("AMZN_PACKAGE_NAME_PREFIX", "")


class CondaCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        pass


setup(
    name=f"{AMZN_PACKAGE_NAME_PREFIX}sagemaker_studio",
    version=VERSION,
    author="Amazon Web Services",
    url="https://aws.amazon.com/sagemaker/",
    description="Python library to interact with Amazon SageMaker Unified Studio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    data_files=data_files,
    license="Apache License 2.0",
    package_data={
        "sagemaker_studio": [
            "boto3_models/datazone/2018-05-10/*.json",
            "boto3_models/glue/2017-03-31/*.json",
            "test/*",
        ],
    },
    packages=find_namespace_packages(where="src"),
    package_dir={
        "sagemaker_studio": "src/sagemaker_studio",
    },
    cmdclass={
        "conda": CondaCommand,
    },
    include_package_data=True,
    python_requires=">=3.9",
    platforms="Linux, Mac OS X, Windows",
    keywords=["AWS", "Amazon", "SageMaker", "SageMaker Unified Studio", "SDK"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
    ],
    install_requires=[
        "boto3>=1.34.106",
        "botocore>=1.34.106",
        "urllib3>=1.26.19",
        "requests>=2.25.1",
        "psutil>=5.9.8",
        "python_dateutil>=2.5.3",
        "setuptools>=21.0.0",
        "packaging>=24.0",
    ],
    tests_require=["pytest"],
    test_suite="src.sagemaker_studio._test",
    extras_require={
        "test": ["pytest >= 6", "pytest-cov", "toml", "coverage"],
        "dev": ["wheel", "invoke", "twine"],
    },
)
