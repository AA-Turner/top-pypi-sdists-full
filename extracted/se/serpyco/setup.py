# -*- coding: utf-8 -*-

from setuptools import Extension, setup

setup(
    ext_modules=[
        Extension("serpyco.serializer", sources=["serpyco/serializer.pyx"]),
        Extension("serpyco.encoder", sources=["serpyco/encoder.pyx"]),
    ],
)
