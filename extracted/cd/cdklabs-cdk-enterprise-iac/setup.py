import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdklabs.cdk-enterprise-iac",
    "version": "0.1.0",
    "description": "@cdklabs/cdk-enterprise-iac",
    "license": "Apache-2.0",
    "url": "https://github.com/cdklabs/cdk-enterprise-iac.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services<aws-cdk-dev@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/cdk-enterprise-iac.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdklabs.cdk_enterprise_iac",
        "cdklabs.cdk_enterprise_iac._jsii"
    ],
    "package_data": {
        "cdklabs.cdk_enterprise_iac._jsii": [
            "cdk-enterprise-iac@0.1.0.jsii.tgz"
        ],
        "cdklabs.cdk_enterprise_iac": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.103.1, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.108.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
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
