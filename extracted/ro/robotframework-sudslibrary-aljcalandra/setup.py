#!/usr/bin/env python3

import os
import sys
from os.path import join, dirname

#sys.path.append(join(dirname(__file__), 'src'))
#from ez_setup import use_setuptools
#use_setuptools()
from setuptools import setup

exec(compile(open(join(dirname(__file__), 'src', 'SudsLibrary', 'version.py')).read(), join(dirname(__file__), 'src', 'SudsLibrary', 'version.py'), 'exec'))

DESCRIPTION = """
SudsLibrary is a web service testing library for Robot Framework
that leverages Suds to test SOAP-based services.
""".strip()

CLASSIFIERS  = """
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python :: 3
Topic :: Software Development :: Testing
""".strip().splitlines()

# determine whether to use Jurko's fork of Suds. This will only work for source
# distributions.
suds_rqmnt = 'suds-bis'
suds_rqmnt = os.environ.get('SUDS_LIBRARY_SUDS_REQUIREMENT', suds_rqmnt)


setup(name         = 'robotframework-sudslibrary-aljcalandra',
      version      = VERSION,
      description  = 'Robot Framework test library for SOAP-based services.',
      long_description = DESCRIPTION,
      author       = 'Kevin Ormbrek',
      author_email = 'kormbrek@gmail.com',
      url          = 'https://github.com/ombre42/robotframework-sudslibrary',
      license      = 'Apache License 2.0',
      keywords     = 'robotframework testing testautomation soap suds web service',
      platforms    = 'any',
      classifiers  = CLASSIFIERS,
      zip_safe     = True,
      install_requires = [
                            suds_rqmnt,
                            'robotframework >= 2.6.0',
                         ],
      package_dir  = {'' : 'src'},
      packages     = ['SudsLibrary']
      )
