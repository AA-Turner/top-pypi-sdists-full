#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of python-ghostscript.
# Copyright 2010-2021 by Hartmut Goebel <h.goebel@crazy-compilers.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

__author__ = "Hartmut Goebel <h.goebel@crazy-compilers.com>"
__copyright__ = "Copyright 2010-2021 by Hartmut Goebel <h.goebel@crazy-compilers.com>"
__licence__ = "GNU General Public License version 3 (GPL v3)"
__credits__ = "Based on an example from http://www.ghostscript.com/doc/8.63/API.htm"

import sys
from ghostscript import _gsprint as gs
import locale

start_string = b"systemdict /start get exec\n"

# arguments have to be bytes, encode them
encoding = locale.getpreferredencoding()
args = sys.argv
args = [a.encode(encoding) for a in args]

instance = gs.new_instance()

# no benefit in using set_stdio()
#gs.set_stdio(isntance, gsdll_stdin, gsdll_stdout, gsdll_stderr)

code = gs.init_with_args(instance, args)
if code == 0:
    code = gs.run_string(instance, start_string)
code1 = gs.exit(instance)
if code == 0 or code == gs.e_Quit:
    code = code1
gs.delete_instance(instance)
if not (code == 0 or code == gs.e_Quit):
    sys.exit(1)
