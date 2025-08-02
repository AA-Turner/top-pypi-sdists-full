import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-spot-one",
    "version": "2.0.328",
    "description": "One spot instance with EIP and defined duration. No interruption.",
    "license": "Apache-2.0",
    "url": "https://github.com/pahud/cdk-spot-one.git",
    "long_description_content_type": "text/markdown",
    "author": "Pahud Hsieh<pahudnet@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/pahud/cdk-spot-one.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_spot_one",
        "cdk_spot_one._jsii"
    ],
    "package_data": {
        "cdk_spot_one._jsii": [
            "cdk-spot-one@2.0.328.jsii.tgz"
        ],
        "cdk_spot_one": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.1.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.78.1, <2.0.0",
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
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": [
        "src/cdk_spot_one/_jsii/bin/ec2-connect"
    ]
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
