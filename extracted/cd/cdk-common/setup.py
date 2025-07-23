import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-common",
    "version": "2.0.1239",
    "description": "Common AWS CDK librarys.",
    "license": "Apache-2.0",
    "url": "https://github.com/neilkuan/cdk-common.git",
    "long_description_content_type": "text/markdown",
    "author": "Neil Kuan<guan840912@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/neilkuan/cdk-common.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_common",
        "cdk_common._jsii"
    ],
    "package_data": {
        "cdk_common._jsii": [
            "cdk-common@2.0.1239.jsii.tgz"
        ],
        "cdk_common": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.188.0, <3.0.0",
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
