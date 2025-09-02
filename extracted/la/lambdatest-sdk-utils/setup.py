from setuptools import setup, find_packages
import lambdatest_sdk_utils

setup(
    name="lambdatest-sdk-utils",
    version="1.0.3",
    author="LambdaTest <keys@lambdatest.com>",
    description="SDK utils",
    long_description="SDK utils for lambdatest",
    long_description_content_type="text/markdown",
    url="https://github.com/LambdaTest/lambdatest-python-sdk",
    keywords="lambdatest python selenium sdk",
    packages=find_packages(),
    license="MIT",
    install_requires=[
        "requests==2.*",
    ],
    python_requires='>=3.6',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
    ],
)
