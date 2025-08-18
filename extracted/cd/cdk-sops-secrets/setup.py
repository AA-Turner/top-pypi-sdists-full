import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-sops-secrets",
    "version": "2.3.2",
    "description": "CDK Constructs that syncs your sops secrets into AWS SecretsManager secrets.",
    "license": "Apache-2.0",
    "url": "https://constructs.dev/packages/cdk-sops-secrets",
    "long_description_content_type": "text/markdown",
    "author": "Markus Siebert<markus.siebert@deutschebahn.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/dbsystel/cdk-sops-secrets.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_sops_secrets",
        "cdk_sops_secrets._jsii"
    ],
    "package_data": {
        "cdk_sops_secrets._jsii": [
            "cdk-sops-secrets@2.3.2.jsii.tgz"
        ],
        "cdk_sops_secrets": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.191.0, <3.0.0",
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
