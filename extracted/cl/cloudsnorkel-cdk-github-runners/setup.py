import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cloudsnorkel.cdk-github-runners",
    "version": "1.0.0",
    "description": "CDK construct to create GitHub Actions self-hosted runners. Creates ephemeral runners on demand. Easy to deploy and highly customizable.",
    "license": "Apache-2.0",
    "url": "https://github.com/CloudSnorkel/cdk-github-runners.git",
    "long_description_content_type": "text/markdown",
    "author": "Amir Szekely<amir@cloudsnorkel.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/CloudSnorkel/cdk-github-runners.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cloudsnorkel.cdk_github_runners",
        "cloudsnorkel.cdk_github_runners._jsii"
    ],
    "package_data": {
        "cloudsnorkel.cdk_github_runners._jsii": [
            "cdk-github-runners@1.0.0.jsii.tgz"
        ],
        "cloudsnorkel.cdk_github_runners": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.10",
    "install_requires": [
        "aws-cdk-lib>=2.239.0, <3.0.0",
        "constructs>=10.5.1, <11.0.0",
        "jsii>=1.142.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
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
