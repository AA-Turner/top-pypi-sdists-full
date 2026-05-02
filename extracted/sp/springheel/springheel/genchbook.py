#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Generate page for chapter
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

"""Generate chapter page."""

import os, html
from slugify import slugify
import springheel.genstatline


def genChapBook(
    translated_strings: dict,
    chap: list,
    nocomment_test: str,
    modeclass: str,
    meta_file_ext: str,
    transcr_file_ext: str,
) -> str:
    """
    Create a chapter page from a list of chapter elements.

    Parameters
    ----------
    translated_strings : dict
        The translation file contents for this site.
    chap : list
        A list of Chapter objects belonging to a comic.
    nocomment_test : str
        An HTML string. Page commentary is checked against this string,
        which is usually "<p>The author has not provided commentary for
        this comic.</p>" (or equivalent in current locale), to determine
        if the page really has commentary or not. If it does match, the
        page is interpreted as not having commentary and the commentary
        block becomes a mere metadata block.
    modeclass : str
        Either an empty string (default) or " webtoon" in webtoon mode.
        Used as a class selector.
    meta_file_ext : str
        The file extension for metadata files.
    transcr_file_ext : str
        The file extension for transcript files.

    Returns
    -------
    str
        The HTML-formatted page sections, separated by line breaks.
    """
    page_template = """<section id="comic{page_padded}" class="page{additions}">
<h2><a href="{permalink}">{h2_title}</a></h2>
<!--PAGE-->
<figure class="comic{modeclass}">
{img}
{alt_text}
</figure>
<!--END PAGE-->

<section id="commentary{page_padded}">
<h3>{caption_s}</h3>
{commentary}
{statline}
</section>
{tb}
</section>"""
    page_sections = []
    current_lang_page_alt = """ alt="{}\"""".format(translated_strings["page_alt_s"])
    chapbook_page_alt = """ alt="{}\"""".format(
        translated_strings["chapbook_page_alt_s"]
    )
    for page in chap.pages:
        if page.transf:
            # Link to metadata and transcript file in statline
            meta_trans = """<a href="{metadatafile}" aria-label="{aria_meta}">{metadata_s}</a>{statline_separator}<a href="{transcriptfile}" aria-label="{aria_trans}">{transcript_s}</a>""".format(
                statline_separator=translated_strings["statline_separator"],
                metadatafile="".join(["pages/", page.new_meta]),
                transcriptfile="".join(["pages/", page.new_transcr]),
                metadata_s=translated_strings["meta_link_s"].format(
                    file_ext=meta_file_ext
                ),
                transcript_s=translated_strings["transcript_link_s"].format(
                    file_ext=transcr_file_ext
                ),
                aria_meta=translated_strings["chapbook_meta_link_s"].format(
                    page=page.page, file_ext=meta_file_ext
                ),
                aria_trans=translated_strings["chapbook_transcript_link_s"].format(
                    page=page.page, file_ext=transcr_file_ext
                ),
            )
        else:
            # Leave off transcript file if we don't need it
            meta_trans = """<a href="{metadatafile}" aria-label="{aria_meta}">{metadata_s}</a>""".format(
                statline_separator=translated_strings["statline_separator"],
                metadatafile="".join(["pages/", page.new_meta]),
                metadata_s=translated_strings["meta_link_s"].format(
                    file_ext=meta_file_ext
                ),
                aria_meta=translated_strings["chapbook_meta_link_s"].format(
                    page=page.page, file_ext=meta_file_ext
                ),
            )
        stat_line = springheel.genstatline.genStatline(
            page, True, chap, translated_strings, page.tline, meta_trans, True
        )
        if page.commentary == nocomment_test:
            comment_header = translated_strings["meta_s"]
            commentary = ""
        else:
            comment_header = translated_strings["caption_s"]
            commentary = page.commentary
        transcript_block = [
            "<section id=transcript{page_padded}><h3>{transcript_s}</h3>".format(
                page_padded=page.page_padded,
                transcript_s=translated_strings["transcript_s"],
            )
        ]
        transcript_block.append(page.transcript_c)
        transcript_block.append("</section>")
        if page.transf:
            tb = "\n".join(transcript_block)
        else:
            tb = ""
        additions = ""
        # check for double pages
        if int(page.width) > int(page.height) or type(page.page_real_num) == tuple:
            additions += " double"
        page_section = page_template.format(
            page_padded=page.page_padded,
            permalink=page.html_filename,
            h2_title=page.h1_title,
            alt_text=page.figcaption,
            additions=additions,
            img=page.pieces.replace(
                current_lang_page_alt, chapbook_page_alt.format(page=page.page)
            ),
            modeclass=modeclass,
            page_alt=translated_strings["chapbook_page_alt_s"].format(page=page.page),
            commentary=commentary,
            statline=stat_line,
            tb=tb,
            caption_s=comment_header,
            metadata_s=translated_strings["meta_s"],
        )
        page_sections.append(page_section)
    outpage = "\n".join(page_sections)
    return outpage
