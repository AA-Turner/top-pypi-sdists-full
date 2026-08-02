# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Create a python package for powertrain-build using setuptools and PBR."""

from setuptools import setup

setup(
    setup_requires=['pbr'],
    pbr=True,
)
