#!python
# -*- coding: utf-8 -*-
import sys, os, re
from os.path import dirname, abspath, join
from setuptools import setup


HERE = abspath(dirname(__file__))
readme = open(join(HERE, 'README.rst')).read()

package_file = open(join(HERE, 'bunch_py3/__init__.py'), 'r')
__version__ = re.sub(
    r".*\b__version__\s+=\s+'([^']+)'.*",
    r'\1',
    [ line.strip() for line in package_file if '__version__' in line ].pop(0)
)


setup(
    name             = "bunch_py3",
    version          = __version__,
    description      = "A dot-accessible dictionary (a la JavaScript objects)",
    long_description = readme,
    url              = "https://github.com/wilbertom/bunch-py3",
    
    author           = "Wilberto Morales",
    author_email     = "wil@wilbertom.com",
    
    packages         = ['bunch_py3',],
    
    keywords         = ['bunch', 'dict', 'mapping', 'container', 'collection', 'python 3'],
    classifiers      = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3",
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
    license          = 'MIT',
)
