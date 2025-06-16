# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '0.3'

setup(
    name='py3o.formats',
    version=version,
    description="Formats declarations for py3o",
    long_description=open("README.rst").read(),
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Text Processing :: General",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='py3o',
    author='Björn Ricks',
    author_email='bjoern.ricks@gmail.com',
    url='http://bitbucket.org/faide/py3o.formats',
    license='MIT License',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['py3o'],
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'setuptools',
    ],
    tests_require=['nose', 'nosexcover'],
    test_suite='nose.collector',
)
