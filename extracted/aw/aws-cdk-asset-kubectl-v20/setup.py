import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-cdk.asset-kubectl-v20",
    "version": "2.1.4",
    "description": "A Lambda Layer that contains kubectl v1.20",
    "license": "Apache-2.0",
    "url": "https://github.com/cdklabs/awscdk-asset-kubectl#readme",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services, Inc.<aws-cdk-dev@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/awscdk-asset-kubectl.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk.asset_kubectl_v20._jsii"
    ],
    "package_data": {
        "aws_cdk.asset_kubectl_v20._jsii": [
            "asset-kubectl-v20@2.1.4.jsii.tgz"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "jsii>=1.106.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
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
