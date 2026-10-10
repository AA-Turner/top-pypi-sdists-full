# -*- coding: utf-8 -*-

# Copyright 2022-2026 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://toyhou.se/"""

from .common import Extractor, Message
from .. import text, util

BASE_PATTERN = r"(?:https?://)?(?:www\.)?toyhou\.se"


class ToyhouseExtractor(Extractor):
    """Base class for toyhouse extractors"""
    category = "toyhouse"
    root = "https://toyhou.se"
    directory_fmt = ("{category}", "{user|artists!S}")
    archive_fmt = "{id}"

    def _init(self):
        self.offset = 0

    def items(self):
        for post in util.advance(self.posts(), self.offset):
            text.nameext_from_url(post["url"], post)
            post["id"], _, post["hash"] = post["filename"].partition("_")
            yield Message.Directory, "", post
            yield Message.Url, post["url"], post

    def skip_files(self, num):
        self.offset += num
        return num

    def _parse_post(self, post, needle=' href="'):
        extr = text.extract_from(post)
        data = {
            "url": extr(needle, '"'),
            "detail": "\n".join(text.split_html(extr(
                'class="image-detail', 'class="image-credit'))[2:-2]),
            "date": (v := extr('', "</div")) and
            self.parse_datetime(
                v[v.find('mb-1">')+6:], "%d %b %Y, %I:%M:%S %p"),
            "artists": text.split_html(extr(
                '<div class="artist-credit',
                '<div class="image-character'))[1:],
            "characters": text.split_html(
                extr('', 'class="image-') or
                extr('', 'id="footer"'))[2:-1],
        }

        url = data["url"]
        if "/watermarks/" in url:
            data["status"] = "watermark"
        elif "/thumbnails/" in url:
            data["status"] = "thumbnail"
        else:
            data["status"] = "original"

        return data

    def _pagination(self, path):
        url = self.root + path
        params = {"page": 1}

        while True:
            page = self.request(url, params=params).text

            cnt = 0
            for post in text.extract_iter(
                    page, '<li class="gallery-item">', '</li>'):
                cnt += 1
                yield self._parse_post(post)

            if not cnt and params["page"] == 1:
                if self._accept_content_warning(page):
                    continue
                return

            if cnt < 18:
                return
            params["page"] += 1

    def _accept_content_warning(self, page):
        data = {
            text.extr(input, 'name="', '"'): text.unescape(
                text.extr(input, 'value="', '"'))
            for input in text.extract_iter(page, "<input ", ">")
        }

        if not data.get("_token"):
            return False
        self.log.info("Accepting 'Content Warning'")
        self.request(self.root + "/~account/warnings/accept",
                     method="POST", data=data, allow_redirects=False)
        return True


class ToyhouseArtExtractor(ToyhouseExtractor):
    """Extractor for artworks of a toyhouse user"""
    subcategory = "art"
    pattern = BASE_PATTERN + r"/([^/?#]+)/art"
    example = "https://www.toyhou.se/USER/art"

    def posts(self):
        user = self.groups[0]
        self.kwdict["user"] = text.unquote(user)
        return self._pagination(f"/{user}/art")


class ToyhouseCharacterGalleryExtractor(ToyhouseExtractor):
    """Extractor for a toyhouse character's gallery"""
    subcategory = "character-gallery"
    directory_fmt = ("{category}", "Characters",
                     "{character} ({character_id})")
    pattern = BASE_PATTERN + r"/(\d+\.\w+)/gallery"
    example = "https://www.toyhou.se/12345.CHARACTER/gallery"

    def posts(self):
        char = self.groups[0]
        kw = self.kwdict
        kw["character_id"], _, kw["character"] = text.unquote(
            char).partition(".")
        return self._pagination(f"/{char}/gallery")


class ToyhouseImageExtractor(ToyhouseExtractor):
    """Extractor for individual toyhouse images"""
    subcategory = "image"
    pattern = (r"(?:https?://)?(?:"
               r"(?:www\.)?toyhou\.se/(~images|\d+\.\w+)|"
               r"f\d+\.toyhou\.se/file/[^/?#]+/(?:image|watermark|thumbnail)s"
               r")/(\d+)")
    example = "https://toyhou.se/~images/12345"

    def posts(self):
        path, image_id = self.groups
        if path is None:
            path = "~images"
        url = f"{self.root}/{path}/{image_id}"
        page = self.request(url).text
        if ">Content Warning<" in page and self._accept_content_warning(page):
            page = self.request(url).text
        return (self._parse_post(page, '<img class="mw-100" src="'),)
