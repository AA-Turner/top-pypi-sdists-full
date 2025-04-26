#!/usr/bin/env python
from codecs import open
from os import path

from setuptools import setup

with open('README.rst') as desc_file:
    description = desc_file.read()

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='spotinst-agent',

    version="1.1.260",

    description='Spectrum instance spotinst-agent that is able to run remote scripts, collect data, deploy applications and more.',

    long_description=description,

    # The project's main homepage.
    url='https://github.com/spotinst/spotinst-spectrum-agent',

    # Author details
    author='Spotinst',
    author_email='service@spotinst.com',

    # Choose your license
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'Topic :: System :: Monitoring',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],

    keywords='spotinst agent infrastructure monitoring execution deployment',
    install_requires=['requests', 'pyyaml'],
    packages=["spotinst_agent"],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'spotinst-agent=spotinst_agent:main'
        ],
    }

)
