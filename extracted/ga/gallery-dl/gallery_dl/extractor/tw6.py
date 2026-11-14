# -*- coding: utf-8 -*-

# Copyright 2026 Mike Fährmann

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://tw6.jp/"""

from .common import Extractor, Message
from .. import text

BASE_PATTERN = r"(?:https?://)?(?:www\.)?tw6\.jp/gallery"


class Tw6Extractor(Extractor):
    """Base class for tw6 extractors"""
    category = "tw6"
    root = "https://tw6.jp"
    directory_fmt = ("{category}", "{master_name}")
    filename_fmt = "{character_name}_{illust_id}.{extension}"
    archive_fmt = "{illust_id}"

    def items(self):
        for post in self.posts():
            url = post["image_url"]
            text.nameext_from_url(url, post)
            yield Message.Directory, "", post
            yield Message.Url, url, post

    def _pagination(self, params):
        url = self.root + "/api/illust_search"
        params["n"] = 0

        while True:
            data = self.request_json(url, params=params)

            if not data:
                break
            yield from data

            params["n"] += 1


class Tw6UserExtractor(Tw6Extractor):
    subcategory = "user"
    pattern = BASE_PATTERN + r"/master/?\?master_id=(\d+)"
    example = "https://tw6.jp/gallery/master/?master_id=12345"

    def posts(self):
        import itertools
        files = self.config("files", True)
        self.kwdict["master_id"] = self.groups[0]

        if not files:
            return ()
        elif files.__class__ is str:
            files = files.split(",")
        elif files.__class__ is not list:
            return itertools.chain(self.posts_profile(), self.posts_gallery())

        genmap = {"profile": self.posts_profile,
                  "gallery": self.posts_gallery}
        return itertools.chain(*[genmap[ft]() for ft in files])

    def posts_profile(self):
        master_id = self.groups[0]
        url = f"{self.root}/gallery/master/?master_id={master_id}"
        page = self.request(url).text

        if name := text.extr(page, 'data-value="master_id:', '"'):
            self.kwdict["master_name"] = text.unescape(name)

        files = []
        if top := text.extr(page, 'class="top-img', '</'):
            files.append({
                "character_name": "master",
                "illust_id": f"m{master_id}_top",
                "image_url": text.unescape(text.extr(top, 'src="', '"')),
                "alt"      : text.unescape(text.extr(top, 'alt="', '"')),
            })
        if desc := text.rextr(page, "</h1>", "<hr>"):
            num = 0
            for img in text.extract_iter(desc, "<img", ">"):
                num += 1
                files.append({
                    "character_name": "master",
                    "illust_id": f"m{master_id}_p{num:>02}",
                    "image_url": text.unescape(text.extr(img, 'src="', '"')),
                })
        return files

    def posts_gallery(self):
        return self._pagination({
            "master_id": self.groups[0],
            "goods"    : "all",
        })


class Tw6PostExtractor(Tw6Extractor):
    subcategory = "post"
    pattern = BASE_PATTERN + r"/?\?id=(\d+)"
    example = "https://tw6.jp/gallery/?id=12345"

    def posts(self):
        pid = text.parse_int(self.groups[0])
        post = next(self._pagination({
            "last_id": pid,
            "goods"  : "all",
        }), None)
        return (post,) if post and post["gallery_image_id"] == pid else ()


class Tw6SearchExtractor(Tw6Extractor):
    subcategory = "search"
    directory_fmt = ("{category}", "Search", "{search_tags}")
    pattern = BASE_PATTERN + r"/search/?\?([^#]+)"
    example = "https://tw6.jp/gallery/search?word=QUERY"

    def posts(self):
        self.kwdict["search"] = params = text.parse_query(self.groups[0])
        self.kwdict["search_tags"] = params.get("word")
        return self._pagination(params)
