import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk8s-image",
    "version": "0.2.695",
    "description": "Build & Push local docker images inside CDK8s applications",
    "license": "Apache-2.0",
    "url": "https://github.com/cdk8s-team/cdk8s-image.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdk8s-team/cdk8s-image.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk8s_image",
        "cdk8s_image._jsii"
    ],
    "package_data": {
        "cdk8s_image._jsii": [
            "cdk8s-image@0.2.695.jsii.tgz"
        ],
        "cdk8s_image": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "cdk8s>=2.68.91, <3.0.0",
        "constructs>=10.3.0, <11.0.0",
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
