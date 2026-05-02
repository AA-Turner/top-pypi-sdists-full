#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Comic Archive Page Generation
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

"""Generate links for archive pages."""

import springheel.parseconf, os, datetime
from typing import List
from springheel.classes import Strip


def getLinks(i: Strip, translated_strings: dict) -> str:
    """Generate hyperlinks for the archive page.

    Takes a Strip object and links it according to the archive link
    format for the current language from strings.json.

    Parameters
    ----------
    i : Strip
        The :class:`springheel.classes.Strip` whose link is to be formatted.
    translated_strings: dict
        The translation file contents for this site.

    Returns
    -------
    str
        The formatted link to the page.
    """
    fstring = translated_strings["archive_l_s"]
    date = i.date_fmt
    archive_l = fstring.format(title=i.title, page=i.page, date=date)
    link_format = """<li><a href="{html_filename}">{archive_l}</a> ({date})</li>"""
    archive_link = link_format.format(
        html_filename=i.html_filename, archive_l=archive_l, date=date
    )
    return archive_link


def generateChapArchList(
    archive: List[str],
    chapter: springheel.classes.Chapter,
    translated_strings: dict,
    level: str,
) -> str:
    """
    Generates an ordered list of pages in a chapter.

    Parameters
    ----------
    archive : list of str
        A list of HTML list item elements that link to pages in the
        chapter.
    chapter : springheel.classes.Chapter
        The :class:`springheel.classes.Chapter` whose archive to generate.
    translated_strings : dict
        The translation file contents for this site.
    level : str
        The heading level to use ("2" or "3").

    Returns
    -------
    str
        The completed chapter archive section.
    """
    sep = "\n"
    link_list = sep.join(archive)

    try:
        chapter_s = translated_strings["chapter_s"].format(
            chapter=chapter.chap_number, chapter_title=chapter.chap_title_escaped
        )
    except AttributeError:
        chapter_s = translated_strings["notitle_chapter_s"].format(
            chapter=chapter.chap_number
        )
    all_pages_s = translated_strings["all_pages_s"].format(chapter=chapter.chap_number)

    sect = """<h{level} id="{slug}">{chapter_s}</h{level}>
    <p><a href="{ch_outfn}">{all_pages_s}</a></p>
<ol class="chapterarch">
{link_list}
</ol>"""

    arch_list = sect.format(
        slug=chapter.slug,
        ch_outfn=chapter.ch_outfn,
        all_pages_s=all_pages_s,
        chapter_s=chapter_s,
        link_list=link_list,
        level=level,
    )
    return arch_list


def generateSeriesArchives(
    category: str, status: str, archive: List[str], slug: str
) -> str:
    """
    Generates an ordered list of pages that aren't in a chapter.

    Parameters
    ----------
    category : str
        The category to which these pages belong.
    status : str
        The status of the comic (active, complete, etc.).
    archive : list of str
        A list of HTML list item elements that link to pages in the
        comic.
    slug : str
        A slug to use for the comic category.

    Returns
    -------
    str
        The completed comic archive section.
    """
    sep = "\n"
    link_list = sep.join(archive)
    sect = """<section class="archive">
<h2 id="id-{slug}">{category}</h2>
<p class="status">{status}</p>
<ol class="datearch">
{link_list}
</ol>
</section>"""

    arch_section = sect.format(
        category=category, status=status, link_list=link_list, slug=slug
    )
    return arch_section
