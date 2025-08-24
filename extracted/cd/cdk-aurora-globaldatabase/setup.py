import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-aurora-globaldatabase",
    "version": "2.3.935",
    "description": "cdk-aurora-globaldatabase is an AWS CDK construct library that provides Cross Region Create Global Aurora RDS Databases.",
    "license": "Apache-2.0",
    "url": "https://github.com/neilkuan/cdk-aurora-globaldatabase.git",
    "long_description_content_type": "text/markdown",
    "author": "Neil Kuan<guan840912@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/neilkuan/cdk-aurora-globaldatabase.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_aurora_globaldatabase",
        "cdk_aurora_globaldatabase._jsii"
    ],
    "package_data": {
        "cdk_aurora_globaldatabase._jsii": [
            "cdk-aurora-globaldatabase@2.3.935.jsii.tgz"
        ],
        "cdk_aurora_globaldatabase": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.126.0, <3.0.0",
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
