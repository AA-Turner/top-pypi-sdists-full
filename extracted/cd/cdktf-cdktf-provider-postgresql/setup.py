import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-postgresql",
    "version": "11.4.0",
    "description": "Prebuilt postgresql Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktf/cdktf-provider-postgresql.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktf/cdktf-provider-postgresql.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_postgresql",
        "cdktf_cdktf_provider_postgresql._jsii",
        "cdktf_cdktf_provider_postgresql.data_postgresql_schemas",
        "cdktf_cdktf_provider_postgresql.data_postgresql_sequences",
        "cdktf_cdktf_provider_postgresql.data_postgresql_tables",
        "cdktf_cdktf_provider_postgresql.database",
        "cdktf_cdktf_provider_postgresql.default_privileges",
        "cdktf_cdktf_provider_postgresql.extension",
        "cdktf_cdktf_provider_postgresql.function_resource",
        "cdktf_cdktf_provider_postgresql.grant",
        "cdktf_cdktf_provider_postgresql.grant_role",
        "cdktf_cdktf_provider_postgresql.physical_replication_slot",
        "cdktf_cdktf_provider_postgresql.provider",
        "cdktf_cdktf_provider_postgresql.publication",
        "cdktf_cdktf_provider_postgresql.replication_slot",
        "cdktf_cdktf_provider_postgresql.role",
        "cdktf_cdktf_provider_postgresql.schema",
        "cdktf_cdktf_provider_postgresql.security_label",
        "cdktf_cdktf_provider_postgresql.server",
        "cdktf_cdktf_provider_postgresql.subscription",
        "cdktf_cdktf_provider_postgresql.user_mapping"
    ],
    "package_data": {
        "cdktf_cdktf_provider_postgresql._jsii": [
            "provider-postgresql@11.4.0.jsii.tgz"
        ],
        "cdktf_cdktf_provider_postgresql": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "cdktf>=0.20.0, <0.21.0",
        "constructs>=10.3.0, <11.0.0",
        "jsii>=1.105.0, <2.0.0",
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
