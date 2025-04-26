import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-ecr-deployment",
    "version": "4.0.1",
    "description": "CDK construct to deploy docker image to Amazon ECR",
    "license": "Apache-2.0",
    "url": "https://github.com/cdklabs/cdk-ecr-deployment",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services<aws-cdk-dev@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/cdk-ecr-deployment"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_ecr_deployment",
        "cdk_ecr_deployment._jsii"
    ],
    "package_data": {
        "cdk_ecr_deployment._jsii": [
            "cdk-ecr-deployment@4.0.1.jsii.tgz"
        ],
        "cdk_ecr_deployment": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.80.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.109.0, <2.0.0",
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
