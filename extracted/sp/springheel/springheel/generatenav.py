#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Comic Navigation Block Generation
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

"""Generate comic navigation."""

import logging
from springheel.classes import Arrow
from typing import Union, Tuple, List, Optional
from gettext import gettext as _


def processTup(
    page: Union[int, float, tuple], range_separator: str
) -> Union[str, int, float]:
    """
    Convert multiple page numbers to singles.

    Check if page numbers are a usable type, and convert them to such
    if they are not.

    Parameters
    ----------
    page : int, float, or tuple
        The page number to process.
    range_separator : str
        The string (a single character) to use for separating ranges in
        the current language.

    Returns
    -------
    str, int, or float
        If the input is a tuple (i.e. a range of page numbers), return
        its contents joined by the range separator. Otherwise, the
        original page number (an int or float).
    """
    try:
        joinedpage = range_separator.join([str(i) for i in page])
        return joinedpage
    except TypeError:
        return page


def navGen(
    navdirection: str,
    page_num: str,
    first_page: str,
    last_page: str,
    first: bool,
    final: bool,
    series_slug: str,
    site_style: str,
    translated_strings: dict,
    all_pages: List[str],
    known_pages_real: List[Union[int, float, tuple]],
    current_ind: int,
    images: dict,
    chapter_mode: Optional[bool] = False,
) -> Tuple[str, str]:
    """
    Generate navigation boxes and link rel navigation.

    Parameters
    ----------
    navdirection : str
        Site reading direction. One of ltr or rtl.
    page_num : str
        The page number represented as an integer. Zero-padded.
    first_page : str
        The number of the first page. Likely be 0 or 1. Zero-padded.
    last_page : str
        The number of the latest/final page. Zero-padded.
    first : bool
        Whether or not the current page is the first one.
    final : bool
        Whether or not the current page is the final one.
    series_slug : str
        URL-safe slug for the comic category.
    site_style : str
        The theme whose arrows will be used.
    translated_strings : dict
        The translation file contents for this site.
    all_pages : list of str
        List of all known page numbers for the current category. Used
        to validate navigation and make sure there will not be missing
        pages.
    known_pages_real : list of int, float, or tuple
        A list of raw page numbers. Used for alt text so that
        it works as intended with assistive tech.
    current_ind : int
        The current strip's index in all_pages.
    chapter_mode : bool, optional
        If True, creates chapter navigation instead of page
        navigation. Defaults to False.
    images : dict
        A dictionary mapping image filenames to (width, height) in
        pixels. Used to set the size of arrow images.

    Returns
    -------
    nav : str
        The generated navigation box.
    linkrels : str
        The generated link rel information.
    """
    if len(all_pages) != len(known_pages_real):
        logmesg = _("Can't find original page numbers for all pages:")
        logging.error(logmesg)
        logmesg = _(
            """Formatted page numbers: {all_pages}.
Original page numbers: {known_pages_real}"""
        ).format(all_pages=all_pages, known_pages_real=known_pages_real)
        logging.debug(logmesg)
        return False, False
    try:
        (only_one_number_one,) = known_pages_real
        logmesg = _("Only one navigation item exists, no reason to create navigation")
        logging.debug(logmesg)
        only_linkls = """\n""".join(
            [
                '<link rel="alternate" type="application/rss+xml" title="{rss_s}" href="feed.xml">'.format(
                    rss_s=translated_strings["rss_s"]
                ),
                '<link rel="alternate" type="application/json" title="{jsonfeed_name}" href="feed.json">'.format(
                    jsonfeed_name=translated_strings["jsonfeed_name"]
                ),
            ]
        )
        return ("", only_linkls)
    except ValueError:
        pass

    if page_num == last_page:
        final = True
    elif page_num == first_page:
        first = True

    firstpage_num = first_page
    lastpage_num = last_page
    range_separator = translated_strings["range_separator"]
    # Get nearby existent pages, for navigation generation
    firstpage_num = all_pages[0]
    lastpage_num = all_pages[-1]
    firstpage_real = processTup(known_pages_real[0], range_separator)
    lastpage_real = processTup(known_pages_real[-1], range_separator)
    try:
        nextpage_num = all_pages[current_ind + 1]
        nextpage_real = processTup(known_pages_real[current_ind + 1], range_separator)
    except IndexError:
        nextpage_num = lastpage_num
        nextpage_real = lastpage_real
    try:
        prevpage_num = all_pages[current_ind - 1]
        prevpage_real = processTup(known_pages_real[current_ind - 1], range_separator)
    except IndexError:
        prevpage_num = firstpage_num
        prevpage_real = firstpage_real
    navl = [' <ul class="cominavbox">']
    linkl = [
        '<link rel="alternate" type="application/rss+xml" title="RSS" href="feed.xml">'
    ]
    home_s = translated_strings["home_s"]
    first_s = translated_strings["first_s"]
    prev_s = translated_strings["prev_s"]
    next_s = translated_strings["next_s"]
    last_s = translated_strings["last_s"]

    if not chapter_mode:

        firsts_s = translated_strings["firsts_s"]
        prevs_s = translated_strings["prevs_s"]
        nexts_s = translated_strings["nexts_s"]
        lasts_s = translated_strings["lasts_s"]

        image_template = """<li><a href="{series_slug}_{page}.html"><img src="arrows/{site_style}_{relation}.png" alt="" width="{arw}" height="{arh}"><br><span>{image_long_string}</span></a></li>"""
        linkrel_template = """<link rel="{relation}" href="{series_slug}_{page}.html" title="{page_string}">"""
    else:

        firsts_s = translated_strings["firstsch_s"]
        prevs_s = translated_strings["prevsch_s"]
        nexts_s = translated_strings["nextsch_s"]
        lasts_s = translated_strings["lastsch_s"]

        image_template = """<li><a href="{series_slug}_c{page}.html"><img src="arrows/{site_style}_{relation}.png" alt="" width="{arw}" height="{arh}"><br><span>{image_long_string}</span></a></li>"""
        linkrel_template = """<link rel="{relation}" href="{series_slug}_c{page}.html" title="{page_string}">"""

    navl = ['<ul class="cominavbox" id="{boxlocation}">']
    linkl = [
        '<link rel="alternate" type="application/rss+xml" title="{rss_s}" href="feed.xml">'.format(
            rss_s=translated_strings["rss_s"]
        ),
        '<link rel="alternate" type="application/json" title="{jsonfeed_name}" href="feed.json">'.format(
            jsonfeed_name=translated_strings["jsonfeed_name"]
        ),
    ]
    relations = []
    if not first:
        fd = {"rel": "first", "page": firstpage_num}
        # There is no need for a prev arrow if we already have a first.
        if prevpage_num != firstpage_num:
            pd = {"rel": "prev", "page": prevpage_num, "lrel": "prev"}
            relations.append(pd)
        else:
            fd["lrel"] = "prev"
        relations.append(fd)
    if not final:
        ld = {"rel": "last", "page": lastpage_num}
        # There is no need for a next arrow if we already have a last.
        if nextpage_num != lastpage_num:
            nd = {"rel": "next", "page": nextpage_num, "lrel": "next"}
            relations.append(nd)
        else:
            ld["lrel"] = "next"
        ld = {"rel": "last", "page": lastpage_num}
        relations.append(ld)
    ordering = ["first", "prev", "next", "last"]
    if navdirection == "rtl":
        ordering.reverse()
        image_strings = {
            "last": {
                "rel": "first",
                "long": last_s.format(page=lastpage_real),
                "short": lasts_s,
            },
            "next": {
                "rel": "prev",
                "long": next_s.format(page=(nextpage_real)),
                "short": nexts_s,
                "lrel": "prev",
            },
            "prev": {
                "rel": "next",
                "long": prev_s.format(page=prevpage_real),
                "short": prevs_s,
                "lrel": "next",
            },
            "first": {
                "rel": "last",
                "long": first_s.format(page=firstpage_real),
                "short": firsts_s,
            },
        }

    else:
        image_strings = {
            "first": {
                "rel": "first",
                "long": first_s.format(page=firstpage_real),
                "short": firsts_s,
            },
            "prev": {
                "rel": "prev",
                "long": prev_s.format(page=prevpage_real),
                "short": prevs_s,
                "lrel": "prev",
            },
            "next": {
                "rel": "next",
                "long": next_s.format(page=nextpage_real),
                "short": nexts_s,
                "lrel": "next",
            },
            "last": {
                "rel": "last",
                "long": last_s.format(page=lastpage_real),
                "short": lasts_s,
            },
        }
    ordering_key = {rel: ordinal for ordinal, rel in enumerate(ordering)}
    relations.sort(key=lambda x: ordering_key[x["rel"]])

    for rel in relations:
        arr = Arrow(relation=rel["rel"], page=rel["page"])
        arr.strings = image_strings[arr.relation]
        arr.long = arr.strings["long"]
        arr.short = arr.strings["short"]
        try:
            arr.lrel = rel["lrel"]
        except KeyError:
            pass
        arw, arh = images[f"""{site_style}_{arr.strings["rel"]}.png"""]
        img = image_template.format(
            series_slug=series_slug,
            page=arr.page,
            site_style=site_style,
            relation=arr.strings["rel"],
            image_long_string=arr.long,
            image_short_string=arr.short,
            arw=arw,
            arh=arh,
        )
        navl.append(img)
        try:
            linkrel = linkrel_template.format(
                relation=arr.lrel,
                series_slug=series_slug,
                page=arr.page,
                page_string=arr.long,
            )
            linkl.append(linkrel)
        except AttributeError:
            pass

    navl.append("</ul>")
    nav = """\n""".join(navl)

    linkrels = """\n""".join(linkl)

    return (nav, linkrels)
