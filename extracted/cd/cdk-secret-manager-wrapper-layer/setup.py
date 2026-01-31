import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-secret-manager-wrapper-layer",
    "version": "2.1.262",
    "description": "cdk-secret-manager-wrapper-layer",
    "license": "Apache-2.0",
    "url": "https://github.com/neilkuan/cdk-secret-manager-wrapper-layer.git",
    "long_description_content_type": "text/markdown",
    "author": "Neil Kuan<guan840912@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/neilkuan/cdk-secret-manager-wrapper-layer.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_secret_manager_wrapper_layer",
        "cdk_secret_manager_wrapper_layer._jsii"
    ],
    "package_data": {
        "cdk_secret_manager_wrapper_layer._jsii": [
            "cdk-secret-manager-wrapper-layer@2.1.262.jsii.tgz"
        ],
        "cdk_secret_manager_wrapper_layer": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.181.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.126.0, <2.0.0",
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
