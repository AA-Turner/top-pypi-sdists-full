# copyright 2003-2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of logilab-common.
#
# logilab-common is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 2.1 of the License, or (at your
# option) any later version.
#
# logilab-common is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with logilab-common.  If not, see <http://www.gnu.org/licenses/>.

"""logilab.common packaging information"""

__docformat__ = "restructuredtext en"

import os
from os.path import join

distname = "logilab-common"
modname = "common"
subpackage_of = "logilab"
subpackage_master = True

numversion = (2, 1, 0)
version = ".".join([str(num) for num in numversion])

license = "LGPL"  # 2.1 or later
description = "collection of low-level Python packages and modules" " used by Logilab projects"
web = "https://forge.extranet.logilab.fr/open-source/logilab-common"
author = "Logilab"
author_email = "contact@logilab.fr"


scripts = [join("bin", "logilab-pytest")]
include_dirs = [join("test", "data")]

install_requires = [
    "setuptools",
    "mypy-extensions",
    "typing_extensions",
    'importlib_metadata>=6,<7; python_version < "3.10"',
]
tests_require = [
    "pytz",
    "egenix-mx-base",
]

if os.name == "nt":
    install_requires.append("colorama")

classifiers = [
    "Topic :: Utilities",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
]
