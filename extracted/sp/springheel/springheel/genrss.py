#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - RSS Feed Generation
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

"""Generate RSS feeds."""

from feedgen.feed import FeedGenerator
import datetime, os, html
from datetime import timezone
from springheel.classes import Strip
from typing import List


def generateFeed(base_url: str, rssmeta: dict, comics: List[Strip], o_path: str) -> str:
    """
    Generate an RSS feed for a comic site.

    Parameters
    ----------
    base_url : str
        The URL of the base site.
    rssmeta : dict
        Metadata needed by the RSS feed.
    comics : list of springheel.Strip
        All comic strips on the site.
    o_path : str
        The path of the output/ directory. The feed is saved as feed.xml
        in this location.

    Returns
    -------
    str
        The generated RSS feed.
    """

    fg = FeedGenerator()
    fg.id(base_url)
    fg.title(rssmeta["title"])
    fg.author({"name": rssmeta["author"], "email": rssmeta["email"]})
    fg.link(href=rssmeta["link"], rel="self")
    fg.language(rssmeta["language"])
    fg.description(rssmeta["desc"])

    # Sort strips by date so the newest ones will come first
    descending_strips = list(comics)
    descending_strips.sort(key=lambda x: (x.date_s))

    for i in descending_strips:
        # Avoid double escape
        title = html.unescape(i.title)
        author = html.unescape(i.author)
        fe = fg.add_entry()
        full_url = "".join([base_url, i.html_filename])
        link = {
            "href": full_url,
            "rel": "alternate",
            "type": "image",
            "hreflang": i.lang,
            "title": title,
        }
        fe.id(full_url)
        fe.link(link)
        authord = {"name": author, "email": i.author_email}
        fe.author(authord)
        ## Feedgen throws a fit if it doesn't get a timezone. This'll
        ## fix its little red wagon.
        utc = timezone.utc
        adate = i.date.replace(tzinfo=utc)
        fe.published(adate)
        fe.title(title)
        page = str(i.page_real_num)
        fe.description(i.h1_title)

    rssfeed = fg.rss_str(pretty=True)

    o_fn = os.path.join(o_path, "feed.xml")

    fg.rss_file(o_fn)
    return rssfeed
