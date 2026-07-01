import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-cdk.lambda-layer-kubectl-v35",
    "version": "2.2.2",
    "description": "A Lambda Layer that contains kubectl v1.35",
    "license": "Apache-2.0",
    "url": "https://github.com/cdklabs/awscdk-asset-kubectl#readme",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services<aws-cdk-dev@amazon.com>",
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
        "aws_cdk.lambda_layer_kubectl_v35",
        "aws_cdk.lambda_layer_kubectl_v35._jsii"
    ],
    "package_data": {
        "aws_cdk.lambda_layer_kubectl_v35._jsii": [
            "lambda-layer-kubectl-v35@2.2.2.jsii.tgz"
        ],
        "aws_cdk.lambda_layer_kubectl_v35": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.224.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.129.0, <2.0.0",
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
