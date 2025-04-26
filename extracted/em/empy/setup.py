#!/usr/bin/env python3

import sys

if sys.version_info >= (3, 10):
    from setuptools import setup
else:
    from distutils.core import setup

PROGRAM = "empy"
VERSION = "4.2"
AUTHOR = "Erik Max Francis <max@alcyone.com>".split(' <')[0]
CONTACT = "software@alcyone.com"
URL = "http://www.alcyone.com/software/empy/"
LICENSE = "BSD"

DESCRIPTION = "A templating system for Python."

LONG_DESCRIPTION = """\
EmPy is a powerful, robust and mature
templating system for inserting Python code in template text.  EmPy
takes a source document, processes it, and produces output.  This is
accomplished via expansions, which are signals to the EmPy system
where to act and are indicated with markup.  Markup is set off by a
customizable prefix (by default the at sign, `@`).  EmPy can expand
arbitrary Python expressions, statements and control structures in
this way, as well as a variety of additional special forms.  The
remaining textual data is sent to the output, allowing Python to be
used in effect as a markup language.
"""

setup(
    name=PROGRAM,
    version=VERSION,
    author=AUTHOR,
    author_email=CONTACT,
    url=URL,
    license=LICENSE,
    python_requires=">=2.4",
    py_modules=[
        "em",
        "emlib",
        "emhelp",
        "emdoc",
    ],
    scripts=[
        "em.py",
    ],
    platforms="any",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: Text Editors :: Text Processing",
        "Topic :: Text Processing :: Filters",
        "Topic :: Text Processing :: General",
        "Topic :: Text Processing :: Markup",
        "Topic :: Utilities",
    ],
)
