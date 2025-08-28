import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "must-cdk",
    "version": "0.0.111",
    "description": "must-cdk",
    "license": "Apache-2.0",
    "url": "https://github.com/globalmsq/must-cdk.git",
    "long_description_content_type": "text/markdown",
    "author": "Must Admin<admin-mufin@users.noreply.github.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/globalmsq/must-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "must_cdk",
        "must_cdk._jsii"
    ],
    "package_data": {
        "must_cdk._jsii": [
            "must-cdk@0.0.111.jsii.tgz"
        ],
        "must_cdk": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.206.0, <3.0.0",
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
    "scripts": [
        "src/must_cdk/_jsii/bin/must-cdk"
    ]
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
