import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-pipelines-github",
    "version": "0.4.130",
    "description": "GitHub Workflows support for CDK Pipelines",
    "license": "Apache-2.0",
    "url": "https://github.com/cdklabs/cdk-pipelines-github.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services<aws-cdk-dev@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/cdk-pipelines-github.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_pipelines_github",
        "cdk_pipelines_github._jsii"
    ],
    "package_data": {
        "cdk_pipelines_github._jsii": [
            "cdk-pipelines-github@0.4.130.jsii.tgz"
        ],
        "cdk_pipelines_github": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.80.0, <3.0.0",
        "constructs>=10.0.46, <11.0.0",
        "jsii>=1.112.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
