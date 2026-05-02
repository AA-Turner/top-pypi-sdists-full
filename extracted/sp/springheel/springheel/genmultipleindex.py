#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Generate index pages for multiple series
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

"""Generate index pages for sites with multiple comics."""

import os
from slugify import slugify
from typing import List
from springheel.classes import Comic


def genMultipleIndex(
    comics: List[Comic],
    characters_page: bool,
    translated_strings: dict,
    site_desc: str,
    images: dict,
) -> List[str]:
    """
    Generate an index page for a site with multiple comics.

    Parameters
    ----------
    comics : list of springheel.Comic
        A list of the Comics on the site.
    characters_page : bool
        Whether or not to add character-page links.
    translated_strings : dict
        The translation file contents for this site.
    site_desc : str
        A description of the site.
    images : dict
        A dictionary mapping known images to dimensions in pixels.

    Returns
    -------
    list of str
        The HTML elements to use as comic descriptions on the index.
    """
    elements = ["<p>{site_desc}</p>".format(site_desc=site_desc)]
    dopen = """<div class="intro">"""
    dclose = "</div>"

    golatest_s = translated_strings["golatest_s"]
    gofirst_s = translated_strings["gofirst_s"]

    character_s = translated_strings["char_s"]

    ltemplate = [
        "<h2>{category}</h2>",
        '<img src="{banner}" alt="" width="{width}" height="{height}">',
        '<p class="author">by {author}</p>',
        '<p class="desc">{desc} (<span class="status">{status}</span>)</p>',
        "<p>{golatest} | {gofirst}</p>",
    ]

    maintemplate = "\n".join(ltemplate)

    for i in comics:
        golatest = ['<a href="', i.lbp_link, '">', golatest_s, "</a>"]
        golatest = "".join(golatest)
        gofirst = ['<a href="', i.fbp_link, '">', gofirst_s, "</a>"]
        gofirst = "".join(gofirst)
        elements.append(dopen)
        div = maintemplate.format(
            banner=i.banner,
            width=images[i.banner][0],
            height=images[i.banner][1],
            category=i.category_escaped,
            author=i.author,
            desc=i.desc,
            status=i.statuss,
            golatest=golatest,
            gofirst=gofirst,
        )
        elements.append(div)
        if characters_page and i.chars_file:
            cat_slug = slugify(i.category, lowercase=True, max_length=200)
            char_line = '<p><a href="{characters_link}">{character_s}</a></p>'.format(
                characters_link=i.chars_fn, character_s=character_s
            )
            elements.append(char_line)
        elements.append(dclose)
    return elements
