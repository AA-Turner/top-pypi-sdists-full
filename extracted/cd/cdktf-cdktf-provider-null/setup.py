import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-null",
    "version": "10.0.2",
    "description": "Prebuilt null Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktf/cdktf-provider-null.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktf/cdktf-provider-null.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_null",
        "cdktf_cdktf_provider_null._jsii",
        "cdktf_cdktf_provider_null.data_null_data_source",
        "cdktf_cdktf_provider_null.provider",
        "cdktf_cdktf_provider_null.resource"
    ],
    "package_data": {
        "cdktf_cdktf_provider_null._jsii": [
            "provider-null@10.0.2.jsii.tgz"
        ],
        "cdktf_cdktf_provider_null": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "cdktf>=0.20.0, <0.21.0",
        "constructs>=10.3.0, <11.0.0",
        "jsii>=1.111.0, <2.0.0",
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
