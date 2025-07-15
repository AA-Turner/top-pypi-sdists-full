import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-solutions-constructs.aws-sqs-lambda",
    "version": "2.86.0",
    "description": "CDK constructs for defining an interaction between an Amazon SQS queue and an AWS Lambda function.",
    "license": "Apache-2.0",
    "url": "https://github.com/awslabs/aws-solutions-constructs.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/awslabs/aws-solutions-constructs.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_solutions_constructs.aws_sqs_lambda",
        "aws_solutions_constructs.aws_sqs_lambda._jsii"
    ],
    "package_data": {
        "aws_solutions_constructs.aws_sqs_lambda._jsii": [
            "aws-sqs-lambda@2.86.0.jsii.tgz"
        ],
        "aws_solutions_constructs.aws_sqs_lambda": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.193.0, <3.0.0",
        "aws-solutions-constructs.core==2.86.0",
        "constructs>=10.0.0, <11.0.0",
        "jsii>=1.111.0, <2.0.0",
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
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
