import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdklabs.appsync-utils",
    "version": "0.0.810",
    "description": "Utilities for creating appsync apis using aws-cdk",
    "license": "Apache-2.0",
    "url": "https://github.com/cdklabs/awscdk-appsync-utils.git",
    "long_description_content_type": "text/markdown",
    "author": "Mitchell Valine<mitchellvaline@yahoo.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/awscdk-appsync-utils.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "awscdk.appsync_utils",
        "awscdk.appsync_utils._jsii"
    ],
    "package_data": {
        "awscdk.appsync_utils._jsii": [
            "awscdk-appsync-utils@0.0.810.jsii.tgz"
        ],
        "awscdk.appsync_utils": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.110.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.113.0, <2.0.0",
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
