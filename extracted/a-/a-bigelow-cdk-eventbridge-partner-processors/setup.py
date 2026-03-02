import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "a-bigelow.cdk-eventbridge-partner-processors",
    "version": "0.0.420",
    "description": "cdk-eventbridge-partner-processors",
    "license": "Apache-2.0",
    "url": "https://github.com/a-bigelow/cdk-eventbridge-partner-processors.git",
    "long_description_content_type": "text/markdown",
    "author": "a-bigelow<adam@adambigelow.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/a-bigelow/cdk-eventbridge-partner-processors.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "a-bigelow.cdk-eventbridge-partner-processors",
        "a-bigelow.cdk-eventbridge-partner-processors._jsii"
    ],
    "package_data": {
        "a-bigelow.cdk-eventbridge-partner-processors._jsii": [
            "cdk-eventbridge-partner-processors@0.0.420.jsii.tgz"
        ],
        "a-bigelow.cdk-eventbridge-partner-processors": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.37.1, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.93.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
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
