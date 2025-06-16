import sys
from setuptools import setup


if sys.version_info < (3, 6):
    print("This module requires python 3.6 or later")
    sys.exit(1)

setup(
    name='CFGraph',
    version='0.2.1',
    packages=['CFGraph'],
    url="http://github.com/hsolbrig/CFGraph",
    license='Apache 2.0',
    author='Harold Solbrig',
    author_email='solbrig@solbrig-informatics.com',
    description='rdflib collections flattening graph',
    install_requires=['rdflib>=0.4.2'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7']
)
