# coding=utf-8
from setuptools import (
    find_namespace_packages,
    setup,
)

setup(
    name='nominal-api-protos',
    version='0.835.2',
    python_requires='>=3.8',
    package_data={"": ["py.typed"]},
    packages=find_namespace_packages(),
    install_requires=[
        'protobuf>=5.25.0',
    ],
)