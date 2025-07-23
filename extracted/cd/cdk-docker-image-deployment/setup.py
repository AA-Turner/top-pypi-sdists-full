import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-docker-image-deployment",
    "version": "0.0.865",
    "description": "This module allows you to copy docker image assets to a repository you control. This can be necessary if you want to build a Docker image in one CDK app and consume it in a different app or outside the CDK.",
    "license": "Apache-2.0",
    "url": "https://github.com/cdklabs/cdk-docker-image-deployment#readme",
    "long_description_content_type": "text/markdown",
    "author": "Parker Scanlon",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/cdk-docker-image-deployment.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_docker_image_deployment",
        "cdk_docker_image_deployment._jsii"
    ],
    "package_data": {
        "cdk_docker_image_deployment._jsii": [
            "cdk-docker-image-deployment@0.0.865.jsii.tgz"
        ],
        "cdk_docker_image_deployment": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.24.0, <3.0.0",
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
