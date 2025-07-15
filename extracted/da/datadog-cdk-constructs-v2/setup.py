import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "datadog-cdk-constructs-v2",
    "version": "2.7.0",
    "description": "CDK Construct Library to automatically instrument Python and Node Lambda functions with Datadog using AWS CDK v2",
    "license": "Apache-2.0",
    "url": "https://github.com/DataDog/datadog-cdk-constructs",
    "long_description_content_type": "text/markdown",
    "author": "Datadog",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/DataDog/datadog-cdk-constructs"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "datadog_cdk_constructs_v2",
        "datadog_cdk_constructs_v2._jsii"
    ],
    "package_data": {
        "datadog_cdk_constructs_v2._jsii": [
            "datadog-cdk-constructs-v2@2.7.0.jsii.tgz"
        ],
        "datadog_cdk_constructs_v2": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.177.0, <3.0.0",
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
