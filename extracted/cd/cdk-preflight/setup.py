import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-preflight",
    "version": "0.0.189",
    "description": "Catch deploy-time CloudFormation failures at synth time: a Rego rule pack for constraints that resource schemas miss, injected into the AWS CDK built-in validator",
    "license": "Apache-2.0",
    "url": "https://github.com/badmintoncryer/cdk-preflight.git",
    "long_description_content_type": "text/markdown",
    "author": "Kazuho CryerShinozuka<malaysia.cryer@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/badmintoncryer/cdk-preflight.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_preflight",
        "cdk_preflight._jsii"
    ],
    "package_data": {
        "cdk_preflight._jsii": [
            "cdk-preflight@0.0.189.jsii.tgz"
        ],
        "cdk_preflight": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.10",
    "install_requires": [
        "aws-cdk-lib>=2.267.0, <3.0.0",
        "constructs>=10.5.1, <11.0.0",
        "jsii>=1.140.0, <2.0.0",
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
    "scripts": [
        "src/cdk_preflight/_jsii/bin/cdk-preflight",
        "src/cdk_preflight/_jsii/bin/cdkpf"
    ]
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
