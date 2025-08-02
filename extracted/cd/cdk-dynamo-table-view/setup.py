import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-dynamo-table-view",
    "version": "0.2.488",
    "description": "An AWS CDK construct which exposes an endpoint with the contents of a DynamoDB table",
    "license": "Apache-2.0",
    "url": "https://github.com/cdklabs/cdk-dynamo-table-viewer.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services<aws-cdk-dev@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/cdk-dynamo-table-viewer.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_dynamo_table_view",
        "cdk_dynamo_table_view._jsii"
    ],
    "package_data": {
        "cdk_dynamo_table_view._jsii": [
            "cdk-dynamo-table-viewer@0.2.488.jsii.tgz"
        ],
        "cdk_dynamo_table_view": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.60.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.91.0, <2.0.0",
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
