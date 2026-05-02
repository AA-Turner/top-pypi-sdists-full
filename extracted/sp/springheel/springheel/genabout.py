#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2021 garrick. Some rights reserved.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Generate an about page."""

import logging
import html_sanitizer
import springheel.metatag
from springheel.wraptag import wrapWithTag
from springheel.classes import Comic
from typing import List
from springheel.tl import gettext as _


def makeAbout(
    ccomics: List[Comic],
    translated_strings: dict,
    single: bool,
    site: springheel.classes.Site,
    images: dict,
) -> str:
    """
    Make an about page for the site.

    Parameters
    ----------
    ccomics : list of :class:`springheel.classes.Comic`
        The Comic objects described by the about page.
    translated_strings : dict
        The translation file contents for this site.
    single : bool
        Whether the site is single-comic or not. If not, separate
        headings and sections are generated for each comic.
    site : :class:`springheel.classes.Site`
        The Springheel comic site to use.
    images : dict
        A dictionary mapping known images to dimensions in pixels.

    Returns
    -------
    str
        The HTML contents of the about page, ready to ``write()``.
    """
    page_elements = []
    cleaner = html_sanitizer.Sanitizer(
        {
            "tags": {
                "a",
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "h6",
                "strong",
                "em",
                "p",
                "ul",
                "ol",
                "li",
                "br",
                "sub",
                "sup",
                "hr",
                "i",
                "b",
                "ruby",
                "rt",
                "rb",
                "date",
                "dl",
                "dt",
                "dd",
                "code",
                "del",
                "ins",
            },
            "attributes": {"a": ("href", "name", "target", "title", "id", "rel")},
            "empty": {"hr", "a", "br"},
            "separate": {"a", "p", "li"},
            "whitespace": {"br"},
            "keep_typographic_whitespace": False,
            "add_nofollow": False,
            "autolink": False,
            "sanitize_href": html_sanitizer.sanitizer.sanitize_href,
            "element_preprocessors": [
                html_sanitizer.sanitizer.bold_span_to_strong,
                html_sanitizer.sanitizer.italic_span_to_em,
                html_sanitizer.sanitizer.tag_replacer("form", "p"),
                html_sanitizer.sanitizer.target_blank_noopener,
            ],
            "element_postprocessors": [],
            "is_mergeable": lambda e1, e2: True,
        }
    )
    for comic in ccomics:
        section = ["""<section class="archive">"""]
        if not single:
            section.append("<h2>{category}</h2>".format(category=comic.category))
            # no need for heading in single mode
        section.append(
            '<img src="{banner}" alt="" width="{width}" height="{height}">'.format(
                banner=comic.banner,
                width=images[comic.banner][0],
                height=images[comic.banner][1],
            )
        )
        section.append('<p class="author">by {author}</p>'.format(author=comic.author))
        desc_p = wrapWithTag(comic.desc, "p")
        section.append(desc_p)
        try:
            about_raw = comic.about.splitlines()
        except AttributeError:
            logging.debug(
                _(
                    "Creating about page, but comic {category} has no about section defined. Add one to its .conf file."
                ).format(category=comic.category)
            )
            continue
        try:
            mdcheck = [i for i in set(comic.about) if i == "<"][0]
            about_sanitized = [cleaner.sanitize(item) for item in about_raw]
        except IndexError:
            about_sanitized = [
                cleaner.sanitize(wrapWithTag(item, "p")) for item in about_raw
            ]
        section += about_sanitized
        section.append("</section>")
        page_elements.append("\n".join(section))
    about_url = "".join([site.config.base_url, "about.html"])
    site_img_url = "".join([site.config.base_url, site.config.header_filename])
    about_title = " | ".join([translated_strings["about_s"], site.config.site_title])
    meta_tags = springheel.metatag.genMetaTags(
        about_title, about_url, site.config.description, site_img_url
    )
    meta_tags_ready = "\n".join(meta_tags)

    return page_elements, meta_tags_ready
