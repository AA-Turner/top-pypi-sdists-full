#!/usr/bin/env python3
# -*- coding: utf-8 -*-

########
# Springheel - JSON Feed Generation
########
# Copyright 2020 garrick. Some rights reserved.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Generate JSON Feeds."""

import datetime
from datetime import timezone


def genJsonFeed(jsond: dict, translated_strings: dict) -> dict:
    """
    Generate a JSON Feed for the site.

    Parameters
    ----------
    jsond : dict
        The contents of the `site.jsond` dictionary that lists various JSON
        endpoints.
    translated_strings : dict
        The translation file contents for this site. Used for making a
        feed comment.

    Returns
    -------
    dict
        The contents of a JSON Feed.
    """
    jsonfeed_url = "".join([jsond["base_url"], "feed.json"])
    authors = [{"name": name} for name in jsond["site_authors"]]
    jsonfeed = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": jsond["site_title"],
        "home_page_url": jsond["base_url"],
        "feed_url": jsonfeed_url,
        "description": jsond["description"],
        "language": jsond["language"],
        "user_comment": translated_strings["jsonfeed_descr"].format(
            jsonfeedurl=jsonfeed_url
        ),
        "authors": authors,
    }

    # Get a flattened-out list of all strips.
    cats = jsond["categories"]
    all_strips = []
    for cat in cats:
        for strip in cat["strips"]:
            all_strips.append(strip)
    jfeed_items = []
    for strip in all_strips:
        strip_image = "".join([jsond["base_url"], "pages/", strip["img"]])
        # Just use UTC for the timezone.
        date_dt = datetime.datetime.strptime(strip["date"], "%Y-%m-%d")
        utc = timezone.utc
        adate = date_dt.replace(tzinfo=utc)
        date = adate.isoformat("T")
        authors = [{"name": item} for item in strip["authors"]]
        jfeed_item = {
            "id": strip["url"],
            "url": strip["url"],
            "title": strip["header_title"],
            "date_published": date,
            "authors": authors,
            "language": jsond["language"],
            "content_html": strip["commentary"],
            "image": strip_image,
        }
        if "tags" in strip.keys():
            jfeed_item["tags"] = strip["tags"]
        jfeed_items.append(jfeed_item)
    # Sort strips with newest first
    descending_strips = list(jfeed_items)
    descending_strips.sort(key=lambda x: (x["date_published"]), reverse=True)
    jsonfeed["items"] = descending_strips
    return jsonfeed
