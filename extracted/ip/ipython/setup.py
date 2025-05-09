# -*- coding: utf-8 -*-
"""Setup script for IPython.

Under Posix environments it works like a typical setup.py script.
Under Windows, the command sdist is not supported, since IPython
requires utilities which are not available under Windows."""

#-----------------------------------------------------------------------------
#  Copyright (c) 2008-2011, IPython Development Team.
#  Copyright (c) 2001-2007, Fernando Perez <fernando.perez@colorado.edu>
#  Copyright (c) 2001, Janko Hauser <jhauser@zscout.de>
#  Copyright (c) 2001, Nathaniel Gray <n8gray@caltech.edu>
#
#  Distributed under the terms of the Modified BSD License.
#
#  The full license is in the file COPYING.rst, distributed with this software.
#-----------------------------------------------------------------------------

import os
import sys

# **Python version check**
#
# This check is also made in IPython/__init__, don't forget to update both when
# changing Python version requirements.
if sys.version_info < (3, 11):
    pip_message = 'This may be due to an out of date pip. Make sure you have pip >= 9.0.1.'
    try:
        import pip
        pip_version = tuple([int(x) for x in pip.__version__.split('.')[:3]])
        if pip_version < (9, 0, 1) :
            pip_message = 'Your pip version is out of date, please install pip >= 9.0.1. '\
            'pip {} detected.'.format(pip.__version__)
        else:
            # pip is new enough - it must be something else
            pip_message = ''
    except Exception:
        pass


    error = """
(information not available for more recent version of IPython)
IPython 8.19+ supports Python 3.10 and above, following SPEC0
IPython 8.13+ supports Python 3.9 and above, following NEP 29.
IPython 8.0-8.12 supports Python 3.8 and above, following NEP 29.

Python {py} detected.
{pip}
""".format(
        py=sys.version_info, pip=pip_message
    )

    print(error, file=sys.stderr)
    sys.exit(1)

# At least we're on the python version we need, move on.

from setuptools import setup

# Our own imports

from setupbase import target_update

from setupbase import (
    setup_args,
    check_package_data_first,
    find_data_files,
    git_prebuild,
)

#-------------------------------------------------------------------------------
# Handle OS specific things
#-------------------------------------------------------------------------------

if os.name in ('nt','dos'):
    os_name = 'windows'
else:
    os_name = os.name

# Under Windows, 'sdist' has not been supported.  Now that the docs build with
# Sphinx it might work, but let's not turn it on until someone confirms that it
# actually works.
if os_name == 'windows' and 'sdist' in sys.argv:
    print('The sdist command is not available under Windows.  Exiting.')
    sys.exit(1)


#-------------------------------------------------------------------------------
# Things related to the IPython documentation
#-------------------------------------------------------------------------------

# update the manuals when building a source dist
if len(sys.argv) >= 2 and sys.argv[1] in ('sdist','bdist_rpm'):

    # List of things to be updated. Each entry is a triplet of args for
    # target_update()
    to_update = [
        (
            "docs/man/ipython.1.gz",
            ["docs/man/ipython.1"],
            "cd docs/man && python -m gzip --best ipython.1",
        ),
    ]


    [ target_update(*t) for t in to_update ]

#---------------------------------------------------------------------------
# Find all the packages, package data, and data_files
#---------------------------------------------------------------------------

data_files = find_data_files()

setup_args['data_files'] = data_files

#---------------------------------------------------------------------------
# custom distutils commands
#---------------------------------------------------------------------------
# imports here, so they are after setuptools import if there was one
from setuptools.command.sdist import sdist

setup_args['cmdclass'] = {
    'build_py': \
            check_package_data_first(git_prebuild('IPython')),
    'sdist' : git_prebuild('IPython', sdist),
}

#---------------------------------------------------------------------------
# Do the actual setup now
#---------------------------------------------------------------------------

if __name__ == "__main__":
    setup(**setup_args)
