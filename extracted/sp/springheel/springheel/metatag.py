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

"""Generate meta tags for link previews."""

from typing import List


def genMetaTags(title: str, url: str, description: str, image: str) -> List[str]:
    """
    Create meta tags so the page will have link previews elsewhere.

    Parameters
    ----------
    title : str
        The title of the page.
    url : str
        The URL of the page.
    description : str
        A description of the page. Defaults to the site description.
        For strips, this will be the commentary block (if available).
    image : str
        Full URL to an image associated with the page. May be a comic
        page or a header banner.

    Returns
    -------
    list of str
        The HTML meta tag elements that will go in the document head.
    """
    formatted = []
    templates = [
        """<meta name="title" content="{title}">""",
        """<meta name="description" content="{description}">""",
        """<meta property="og:type" content="website">""",
        """<meta property="og:url" content="{url}">""",
        """<meta property="og:title" content="{title}">""",
        """<meta property="og:description" content="{description}">""",
        """<meta property="og:image" content="{image}">""",
        """<meta property="twitter:card" content="summary_large_image">""",
        """<meta property="twitter:url" content="{url}">""",
        """<meta property="twitter:title" content="{title}">""",
        """<meta property="twitter:description" content="{description}">""",
        """<meta property="twitter:image" content="{image}">""",
    ]
    for templ in templates:
        fo = templ.format(title=title, url=url, description=description, image=image)
        formatted.append(fo)
    return formatted
