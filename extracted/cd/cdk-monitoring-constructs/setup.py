import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-monitoring-constructs",
    "version": "9.19.2",
    "description": "cdk-monitoring-constructs",
    "license": "Apache-2.0",
    "url": "https://github.com/cdklabs/cdk-monitoring-constructs",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services<aws-cdk-dev@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/cdk-monitoring-constructs"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_monitoring_constructs",
        "cdk_monitoring_constructs._jsii"
    ],
    "package_data": {
        "cdk_monitoring_constructs._jsii": [
            "cdk-monitoring-constructs@9.19.2.jsii.tgz"
        ],
        "cdk_monitoring_constructs": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.160.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.126.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard==2.13.3"
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
