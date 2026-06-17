import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-cdk.aws-msk-alpha",
    "version": "2.260.0.a0",
    "description": "The CDK Construct Library for AWS::MSK",
    "license": "Apache-2.0",
    "url": "https://github.com/aws/aws-cdk",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/aws/aws-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk.aws_msk_alpha",
        "aws_cdk.aws_msk_alpha._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_msk_alpha._jsii": [
            "aws-msk-alpha@2.260.0-alpha.0.jsii.tgz"
        ],
        "aws_cdk.aws_msk_alpha": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.10",
    "install_requires": [
        "aws-cdk-lib>=2.260.0, <3.0.0",
        "constructs>=10.5.0, <11.0.0",
        "jsii>=1.133.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard==2.13.3"
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
        "Development Status :: 4 - Beta",
        "License :: OSI Approved",
        "Framework :: AWS CDK",
        "Framework :: AWS CDK :: 2"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
