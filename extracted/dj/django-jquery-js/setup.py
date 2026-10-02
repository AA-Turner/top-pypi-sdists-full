#!/usr/bin/env python
"""
Install django-jquery-js using setuptools
"""

from jquery import __version__

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='django-jquery-js',
    version=__version__,
    description='jQuery, bundled up so apps can depend upon it',
    author='Tim Heap',
    author_email='tim@ionata.com.au',
    url='https://bitbucket.org/tim_heap/django-jquery',

    install_requires=['Django>=1.4'],
    zip_safe=False,

    packages=find_packages(),

    include_package_data=True,
    package_data={ },

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
    ],
)
