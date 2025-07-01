import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk_databrew_cicd",
    "version": "2.0.636",
    "description": "A construct for AWS Glue DataBrew wtih CICD",
    "license": "Apache-2.0",
    "url": "https://github.com/HsiehShuJeng/cdk-databrew-cicd.git",
    "long_description_content_type": "text/markdown",
    "author": "Shu-Jeng Hsieh",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/HsiehShuJeng/cdk-databrew-cicd.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_databrew_cicd",
        "cdk_databrew_cicd._jsii"
    ],
    "package_data": {
        "cdk_databrew_cicd._jsii": [
            "cdk-databrew-cicd@2.0.636.jsii.tgz"
        ],
        "cdk_databrew_cicd": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.27.0, <3.0.0",
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
