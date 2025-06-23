# coding=utf-8
from setuptools import (
    find_packages,
    setup,
)

setup(
    name='nominal-api-protos',
    version='0.731.12',
    python_requires='>=3.8',
    package_data={"": ["py.typed"]},
    packages=find_packages(),
    install_requires=[
        'protobuf>=5.25.0',
    ],
)