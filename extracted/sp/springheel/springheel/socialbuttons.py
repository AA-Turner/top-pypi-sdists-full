#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
# Springheel - Social media icons
########
# Copyright 2017-2021 garrick. Some rights reserved.
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

"""Show icons and links to social media sites."""

from springheel.classes import Site
from typing import Tuple
from springheel.tl import gettext as _


def wrapImage(link: str, title: str, image: str) -> str:
    """
    Enclose an image in a hyperlink.

    Notes
    -----
    Assumes that the image in question will be present in
    output/socialbuttons.

    Parameters
    ----------
    link : str
        The URL to use as the hyperlink location.
    title : str
        A string to use as alt text for the image.
    image : str
        A filename in socialbuttons to use for the image.

    Returns
    -------
    str
        An HTML anchor containing the image.
    """
    line = """<a href="{link}"><img src="socialbuttons/{image}" alt="{title}" height="24" width="24"></a>""".format(
        link=link, image=image, title=title
    )
    return line


def getButtons(site: Site, translated_strings: dict) -> Tuple[list, str]:
    """
    Show social media icons on the site as desired.

    Parameters
    ----------
    site : Site
        The site for which icons are being generated.
    translated_strings : dict
        The translation file contents for this site.

    Returns
    -------
    social_links : list of dict
        Dictionaries with metadata about other sites.
    icons : str
        HTML img elements that hyperlink to other sites.
    """

    twitter_handle = site.config.twitter_handle
    tumblr_handle = site.config.tumblr_handle
    patreon_handle = site.config.patreon_handle

    pump_url = site.config.pump_url
    diaspora_url = site.config.diaspora_url
    liberapay_handle = site.config.liberapay_handle
    mastodon_url = site.config.mastodon_url

    rss_url = "feed.xml"
    jsonfeed_url = "feed.json"

    social_links = []

    rss_link = {
        "url": rss_url,
        "site": "",
        "title": translated_strings["rss_s"],
        "image": "rss.png",
    }
    social_links.append(rss_link)
    jf_link = {
        "url": jsonfeed_url,
        "site": "",
        "title": translated_strings["jsonfeed_name"],
        "image": "jsonfeed.png",
    }
    social_links.append(jf_link)

    if site.config.social_icons:
        try:
            twitter_url = "".join["https://twitter.com/", twitter_handle]
            twitter = {
                "url": twitter_url,
                "site": "twitter",
                "title": _("Twitter"),
                "image": "twitter.png",
            }
            social_links.append(twitter)
        except TypeError:
            pass
        try:
            tumblr_url = "".join["https://", tumblr_handle, ".tumblr.com"]
            tumblr = {
                "url": tumblr_url,
                "site": "tumblr",
                "title": _("tumblr."),
                "image": "tumblr.png",
            }
            social_links.append(tumblr)
        except TypeError:
            pass
        try:
            patreon_url = "".join["https://www.patreon.com/", patreon_handle]
            patreon = {
                "url": patreon_url,
                "site": "Patreon",
                "title": _("Patreon"),
                "image": "patreon.png",
            }
            social_links.append(patreon)
        except TypeError:
            pass
        try:
            liberapay_url = "".join["https://liberapay.com/", liberapay_handle]
            liberapay = {
                "url": liberapay_url,
                "site": "Liberapay",
                "title": _("Liberapay"),
                "image": "liberapay.png",
            }
            social_links.append(liberapay)
        except TypeError:
            pass
        try:
            # An additional, identi.ca-specific icon has also been provided.
            # To use it, simply move or rename the existing pump.png
            # and rename identica.png to pump.png.
            pump = {
                "url": "".join(pump_url),
                "site": "pump",
                "title": _("Pump.io"),
                "image": "pump.png",
            }
            social_links.append(pump)
        except TypeError:
            pass
        try:
            diaspora = {
                "url": "".join(diaspora_url),
                "site": "diaspora",
                "title": _("diaspora*"),
                "image": "diaspora.png",
            }
            social_links.append(diaspora)
        except TypeError:
            pass
        try:
            mastodon = {
                "url": "".join(mastodon_url),
                "site": "mastodon",
                "title": _("Mastodon"),
                "image": "mastodon.png",
            }
            social_links.append(mastodon)
        except TypeError:
            pass

    social_icons = []
    for i in social_links:
        icon = wrapImage(i["url"], i["title"], i["image"])
        social_icons.append(icon)

    icons = " ".join(social_icons)

    return (social_links, icons)
