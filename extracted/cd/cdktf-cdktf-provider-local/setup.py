import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-local",
    "version": "10.1.1",
    "description": "Prebuilt local Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktf/cdktf-provider-local.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktf/cdktf-provider-local.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_local",
        "cdktf_cdktf_provider_local._jsii",
        "cdktf_cdktf_provider_local.data_local_file",
        "cdktf_cdktf_provider_local.data_local_sensitive_file",
        "cdktf_cdktf_provider_local.file",
        "cdktf_cdktf_provider_local.provider",
        "cdktf_cdktf_provider_local.sensitive_file"
    ],
    "package_data": {
        "cdktf_cdktf_provider_local._jsii": [
            "provider-local@10.1.1.jsii.tgz"
        ],
        "cdktf_cdktf_provider_local": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "cdktf>=0.20.0, <0.21.0",
        "constructs>=10.3.0, <11.0.0",
        "jsii>=1.103.1, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<5.0.0"
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
