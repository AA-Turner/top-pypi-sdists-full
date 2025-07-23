import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-tweet-queue",
    "version": "2.0.869",
    "description": "Defines an SQS queue with tweet stream from a search",
    "license": "Apache-2.0",
    "url": "https://github.com/cdklabs/cdk-tweet-queue",
    "long_description_content_type": "text/markdown",
    "author": "Elad Ben-Israel<elad.benisrael@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/cdk-tweet-queue"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_tweet_queue",
        "cdk_tweet_queue._jsii"
    ],
    "package_data": {
        "cdk_tweet_queue._jsii": [
            "cdk-tweet-queue@2.0.869.jsii.tgz"
        ],
        "cdk_tweet_queue": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.206.0, <3.0.0",
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
