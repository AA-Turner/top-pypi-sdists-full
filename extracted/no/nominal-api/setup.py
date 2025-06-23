# coding=utf-8
from setuptools import (
    find_packages,
    setup,
)

setup(
    name='nominal-api',
    version='0.731.12',
    python_requires='>=3.8',
    package_data={"": ["py.typed"]},
    packages=find_packages(),
    install_requires=[
        'requests',
        'conjure-python-client>=2.8.0,<4',
    ],
)
