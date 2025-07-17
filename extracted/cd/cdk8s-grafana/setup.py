import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk8s-grafana",
    "version": "0.1.707",
    "description": "Grafana construct for cdk8s.",
    "license": "Apache-2.0",
    "url": "https://github.com/cdk8s-team/cdk8s-grafana.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdk8s-team/cdk8s-grafana.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk8s_grafana",
        "cdk8s_grafana._jsii"
    ],
    "package_data": {
        "cdk8s_grafana._jsii": [
            "cdk8s-grafana@0.1.707.jsii.tgz"
        ],
        "cdk8s_grafana": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "cdk8s>=2.68.91, <3.0.0",
        "constructs>=10.3.0, <11.0.0",
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
