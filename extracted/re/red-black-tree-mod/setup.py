
"""setup.py for red black trees."""

from distutils.core import setup
# from distutils.extension import Extension

version = '1.22'

setup(
    name='red-black-tree-mod',
    py_modules=[
        'red_black_set_mod',
        'red_black_dict_mod'
        ],
    version=version,
    description='Flexible python implementation of red black trees',
    long_description='''
A pair of python modules implementing red black trees is provided.

Red-black trees are a little slower than treaps (some question this), but they give a nice
low standard deviation in operation times, and this code is rather flexible.

A module is provided for red black trees that enforce uniqueness.
They allow for set-like use and dictionary-like use.

This code is known to work on CPython 2.x, CPython 3.x, Pypy and Jython.

Much of the work here was done by Duncan G. Smith.  Dan just put some finishing touches on it.
''',
    author='Duncan G. Smith, Daniel Richard Stromberg',
    author_email='strombrg@gmail.com',
    url='http://stromberg.dnsalias.org/~strombrg/red-black-tree-mod/',
    platforms='Cross platform',
    license='MIT',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        ],
    )
