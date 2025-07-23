import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdklabs.cdk-ethereum-node",
    "version": "0.0.666",
    "description": "CDK construct to deploy an Ethereum node running on Amazon Managed Blockchain",
    "license": "MIT-0",
    "url": "https://github.com/cdklabs/cdk-ethereum-node.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/cdk-ethereum-node.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdklabs.cdk_ethereum_node",
        "cdklabs.cdk_ethereum_node._jsii"
    ],
    "package_data": {
        "cdklabs.cdk_ethereum_node._jsii": [
            "cdk-ethereum-node@0.0.666.jsii.tgz"
        ],
        "cdklabs.cdk_ethereum_node": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.24.1, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
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
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
