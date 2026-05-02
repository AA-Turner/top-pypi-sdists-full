#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Gettext wrapper
########
##  Copyright 2017 garrick. Some rights reserved.
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.

##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU Lesser General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.

import gettext, sys, os

localedir = os.path.join(sys.modules["springheel"].__path__[0], "locales")
userlang = gettext.translation("messages", localedir=localedir, fallback=True)
userlang.install()
_ = userlang.gettext


def gettext(tlstring: str) -> str:
    """
    Wrapper for gettext in the correct language.

    Parameters
    ----------
    tlstring : str
        A string to translate.

    Returns
    -------
    str
        The translated string.
    """
    return _(tlstring)
