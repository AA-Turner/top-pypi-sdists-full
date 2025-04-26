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

args = [
    b"ps2pdf",	# actual value doesn't matter
    b"-dNOPAUSE",
    b"-dBATCH",
    b"-dSAFER",
    b"-sDEVICE=pdfwrite",
    b"-sOutputFile=/tmp/out.pdf",
    b"-c",
    b".setpdfwrite",
    b"-f",
    b"test.ps"
    ]

instance = gs.new_instance()
code = gs.init_with_args(instance, args)
code1 = gs.exit(instance)
if code == 0 or code == gs.e_Quit:
    code = code1
gs.delete_instance(instance)
if not (code == 0 or code == gs.e_Quit):
    sys.exit(1)
