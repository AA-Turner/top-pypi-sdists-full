"""
To install AttrDict:

    python setup.py install
"""
from setuptools import setup

DESCRIPTION = "A dict with attribute-style access"
LONG_DESCRIPTION = "AttrDictionary is an MIT-licensed library that provides mapping objects that allow their elements to be " \
              "accessed both as keys and as attributes. It originates from a fork of AttrDict which is sadly no longer " \
              "maintained. AttrDictionary fully compatible with AttrDict except support for Python 2 versions. " \
              "This version was tested on Python 3.11:"


setup(
    name="attrdictionary",
    version="1.0.0",
    author="Kiselev Aleksandr",
    author_email="kisel.nf97@gmail.com",
    packages=("attrdictionary",),
    url="https://github.com/kiselas/AttrDictionary",
    license="MIT License",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ),
    tests_require=(
        "pytest",
        "coverage",
    ),
    zip_safe=True,
)
