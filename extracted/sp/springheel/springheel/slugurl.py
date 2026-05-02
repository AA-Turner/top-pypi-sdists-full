#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Slugify
########
##  Copyright 2020–2021 garrick. Some rights reserved.
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

import html
from slugify import slugify


def slugify_url(txt: str) -> str:
    """
    Convert a piece of text to a URL-like slug.

    Parameters
    ----------
    txt : str
        The string to convert.

    Returns
    -------
    str
        The slugified string.
    """
    escaped_txt = html.escape(txt)
    slugified = slugify(escaped_txt, lowercase=True, max_length=200)
    return slugified
