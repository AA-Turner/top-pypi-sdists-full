from setuptools import setup, find_packages
from currint import __version__

setup(
    name='currint',
    version=__version__,
    description='Integer-based, fixed precision currency calculation',
    packages=find_packages(),
    author='Andrew Godwin',
    author_email='andrew@aeracode.org',
    install_requires=[
        'six',
    ],
    test_suite='currint.tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
    ],
)

