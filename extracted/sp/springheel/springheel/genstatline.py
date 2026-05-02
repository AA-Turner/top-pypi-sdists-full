#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Generate stat line
########
##  Copyright 2021 garrick. Some rights reserved.
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

"""Generate stat line."""

from typing import List
import springheel.classes


def genStatline(
    strip: springheel.classes.Strip,
    match_chapters: bool,
    match_chapters_list: list,
    translated_strings: dict,
    tline: str,
    meta_trans: str,
    chapmode: bool = False,
) -> str:
    """
    Generate a metadata statistics line for a comic.

    Parameters
    ----------
    strip : springheel.classes.Strip
        The strip to generate a statline for.
    match : springheel.classes.Comic
        The Comic to which the strip belongs.
    translated_strings : dict
        The translation file contents for this site.
    tline : str
        A line of tags applied to the current strip.
    meta_trans : str
        Links to the metadata and transcript files for the comic.
    chapmode : bool, default False
        Whether to create the statline in chapter mode or not. Defaults
        to false.

    Returns
    -------
    str
        The completed statline.
    """
    stat_s = translated_strings["statline_s"].format(
        author=strip.author, date=strip.date_fmt
    )
    if not chapmode:
        if hasattr(strip, "chapter") and strip.chapter and match_chapters:
            (chap_check,) = [
                item
                for item in match_chapters_list
                if item.chap_number == int(strip.chapter)
            ]
            try:
                chapter_title = chap_check.chap_title_escaped.strip()
                chapter_s = translated_strings["chapter_s"].format(
                    chapter=strip.chapter, chapter_title=chapter_title
                )
            except AttributeError:
                chapter_s = translated_strings["notitle_chapter_s"].format(
                    chapter=strip.chapter
                )
            alt_formatted = translated_strings["alt_chapter_s"].format(
                ch_outfn=chap_check.ch_outfn,
                category=strip.category,
                chapter_s=chapter_s,
                page=strip.page,
                title=strip.title,
            )
            stat_line = (
                """<p class="statline">{alt_formatted}{sep}{stat_s}{sep}""".format(
                    alt_formatted=alt_formatted,
                    sep=translated_strings["statline_separator"],
                    stat_s=stat_s,
                )
            )
        else:
            alt_formatted = translated_strings["alt_nochapter_s"].format(
                category=strip.category, page=strip.page, title=strip.title
            )
            stat_line = (
                """<p class="statline">{alt_formatted}{sep}{stat_s}{sep}""".format(
                    alt_formatted=alt_formatted,
                    sep=translated_strings["statline_separator"],
                    stat_s=stat_s,
                )
            )
    else:
        stat_line = """<p class="statline">{stat_s}{sep}""".format(
            sep=translated_strings["statline_separator"],
            stat_s=stat_s,
        )
    try:
        source_link = """<a href="{source}" aria-label="{aria_source}" class="sourcelink">{source_s}</a>""".format(
            source=strip.source,
            source_s=translated_strings["source_s"],
            aria_source=translated_strings["chapbook_source_s"].format(page=strip.page),
        )
        stat_line = "".join(
            [stat_line, source_link, translated_strings["statline_separator"]]
        )
    except AttributeError:
        pass
    stat_line = "".join([stat_line, tline])
    if chapmode:
        stat_line = "".join([stat_line, meta_trans])
    else:
        mtp = translated_strings["statline_separator"].join(
            [meta_trans, strip.permalink]
        )
        stat_line = "".join([stat_line, mtp])
    return stat_line
