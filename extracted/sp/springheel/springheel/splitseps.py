#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
# Springheel - Split items at separators
########
# Copyright 2021 garrick. Some rights reserved.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Split a string at arbitary separators."""

from typing import List


def splitAtSeparators(thing_to_check: str, separators: List[str]) -> List[str]:
    """
    Split a string if it contains any of a number of separators.

    Similar in functionality to splitlines() but with arbitrary
    separators, so that it works on *double* linebreaks, for example.
    Keep in mind that it does indeed use the *first* separator present
    and construct the separators parameter accordingly.

    Parameters
    ----------
    thing_to_check : str
        The string to work on.
    separators : list of str
        A list of separators to use.

    Returns
    -------
    list of str
        The elements of the string, split with the first separator found
        in the separator list.
    """
    for sep in separators:
        if sep in thing_to_check:
            splitted = thing_to_check.split(sep)
            return splitted
