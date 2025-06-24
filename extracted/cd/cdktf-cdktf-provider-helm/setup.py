import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-helm",
    "version": "12.0.1",
    "description": "Prebuilt helm Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktf/cdktf-provider-helm.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktf/cdktf-provider-helm.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_helm",
        "cdktf_cdktf_provider_helm._jsii",
        "cdktf_cdktf_provider_helm.data_helm_template",
        "cdktf_cdktf_provider_helm.provider",
        "cdktf_cdktf_provider_helm.release"
    ],
    "package_data": {
        "cdktf_cdktf_provider_helm._jsii": [
            "provider-helm@12.0.1.jsii.tgz"
        ],
        "cdktf_cdktf_provider_helm": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "cdktf>=0.21.0, <0.22.0",
        "constructs>=10.4.2, <11.0.0",
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
