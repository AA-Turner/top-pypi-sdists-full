#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Generate site navigation
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

"""Generate site navigation."""

from typing import Union


def genTopNav(
    characters_page: bool,
    extras_page: bool,
    store_page: Union[str, bool],
    translated_strings: dict,
    gen_about: bool,
) -> str:
    """
    Generate the navigation at the top of each page.

    Parameters
    ----------
    characters_page : bool
        Whether or not to link to the characters page.
    extras_page : bool
        Whether or not to link to an extras page.
    store_page : str
        If not None, a URL to an external store page.
    translated_strings : dict
        The translation file contents for this site.
    gen_about : bool
        Whether or not to include ``about.html`` in the navigation.

    Returns
    -------
    str
        An HTML unordered list of navigation links.
    """
    char_s = translated_strings["char_s"]
    archive_s = translated_strings["archive_s"]
    extra_s = translated_strings["extra_s"]
    store_s = translated_strings["store_s"]
    about_s = translated_strings["about_s"]

    d = [{"s": archive_s, "u": "archive.html"}]
    if gen_about:
        d.append({"s": about_s, "u": "about.html"})
    if characters_page:
        d.append({"s": char_s, "u": "characters.html"})
    if extras_page:
        d.append({"s": extra_s, "u": "extras.html"})
    if store_page:
        d.append({"s": store_s, "u": store_page})

    elements = ["<ul>"]

    for pair in d:
        line = '<li><a href="{u}">{s}</a></li>'.format(u=pair["u"], s=pair["s"])
        elements.append(line)
    elements.append("</ul>")
    return elements
