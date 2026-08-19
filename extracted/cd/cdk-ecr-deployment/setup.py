import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-ecr-deployment",
    "version": "4.2.52",
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
            "cdk-ecr-deployment@4.2.52.jsii.tgz"
        ],
        "cdk_ecr_deployment": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.10",
    "install_requires": [
        "aws-cdk-lib>=2.80.0, <3.0.0",
        "constructs>=10.5.1, <11.0.0",
        "jsii>=1.139.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
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
