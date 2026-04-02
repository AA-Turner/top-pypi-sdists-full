import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-cdk-github-oidc",
    "version": "2.4.1",
    "description": "CDK constructs to use OpenID Connect for authenticating your Github Action workflow with AWS IAM",
    "license": "Apache-2.0",
    "url": "https://github.com/aripalo/aws-cdk-github-oidc.git",
    "long_description_content_type": "text/markdown",
    "author": "Ari Palo<opensource@aripalo.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/aripalo/aws-cdk-github-oidc.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk_github_oidc",
        "aws_cdk_github_oidc._jsii"
    ],
    "package_data": {
        "aws_cdk_github_oidc._jsii": [
            "aws-cdk-github-oidc@2.4.1.jsii.tgz"
        ],
        "aws_cdk_github_oidc": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.89.0, <3.0.0",
        "constructs>=10.0.0, <11.0.0",
        "jsii>=1.86.1, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
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
