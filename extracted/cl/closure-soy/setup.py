#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages

setup(
    name="closure-soy",
    description="Google Closure's Soy templates packaged for Python",
    long_description=open('README.rst').read(),
    author='Michael Su',
    author_email='mdasu1@gmail.com',
    version="20121221",
    url="http://pypi.python.org/pypi/closure-soy",
    license='BSD',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            "closure-soy = closure_soy:main"
        ]
    },
    package_data={
        '': ["*.jar"]
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'License :: OSI Approved :: BSD License',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ]
)
