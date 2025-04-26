# Copyright (C) 2001-2007 Python Software Foundation

import ez_setup
ez_setup.use_setuptools()

import email
from setuptools import setup, find_packages

setup(
    name                = 'email',
    version             = email.__version__,
    description         = 'Standalone email package',
    long_description    = """\
This is the standalone email package.  This is a copy of what's available in
Python but you may want to use the standalone version if you want the latest
and greatest email package, even in older Pythons.""",
    author              = 'Email SIG',
    author_email        = 'email-sig@python.org',
    url                 = 'http://www.python.org/sigs/email-sig',
    keywords            = 'email',
    license             = 'Python software Foundation',
    packages            = find_packages(),
    )
