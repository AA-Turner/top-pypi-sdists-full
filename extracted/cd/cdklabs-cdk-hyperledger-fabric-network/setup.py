import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdklabs.cdk-hyperledger-fabric-network",
    "version": "0.8.990",
    "description": "CDK construct to deploy a Hyperledger Fabric network running on Amazon Managed Blockchain",
    "license": "MIT-0",
    "url": "https://github.com/cdklabs/cdk-hyperledger-fabric-network.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/cdk-hyperledger-fabric-network.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdklabs.cdk_hyperledger_fabric_network",
        "cdklabs.cdk_hyperledger_fabric_network._jsii"
    ],
    "package_data": {
        "cdklabs.cdk_hyperledger_fabric_network._jsii": [
            "cdk-hyperledger-fabric-network@0.8.990.jsii.tgz"
        ],
        "cdklabs.cdk_hyperledger_fabric_network": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.24.1, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.116.0, <2.0.0",
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
