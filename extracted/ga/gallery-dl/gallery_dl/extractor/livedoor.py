# -*- coding: utf-8 -*-

# Copyright 2019-2026 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for http://blog.livedoor.jp/"""

from .common import Extractor, Message
from .. import text

BASE_PATTERN = (r"(?:https?://)?("
                r"blog\.livedoor\.jp/(\w+)|"
                r"(\w+)\.livedoor\.(?:blog|jp))")


class LivedoorExtractor(Extractor):
    """Base class for livedoor extractors"""
    category = "livedoor"
    root = "http://blog.livedoor.jp"
    filename_fmt = "{post[id]}_{post[title]}_{num:>02}.{extension}"
    directory_fmt = ("{category}", "{post[user]}")
    archive_fmt = "{post[id]}_{hash}"

    def __init__(self, match):
        root, user1, user2, _ = match.groups()
        if user2 is None:
            self.root = "http://" + root
            self.user = user1
        else:
            self.root = "https://" + root
            self.user = user2
        Extractor.__init__(self, match)

    def items(self):
        for post in self.posts():
            if images := self._images(post):
                yield Message.Directory, "", {"post": post}
                for image in images:
                    yield Message.Url, image["url"], image

    def posts(self):
        """Return an iterable with post objects"""

    def _extract_post(self, url):
        extr = text.extract_from(self.request(url).text)
        data = extr('<rdf:RDF', '</rdf:RDF>')
        body = extr('class="article-body-inner">', 'class="article-footer">')
        return self._load(data, body)

    def _load(self, data, body):
        extr = text.extract_from(data)
        tags = text.extr(body, 'class="article-tags">', '</dl>')
        about = extr('rdf:about="', '"')

        return {
            "id"         : text.parse_int(
                about.rpartition("/")[2].partition(".")[0]),
            "title"      : text.unescape(extr('dc:title="', '"')),
            "categories" : extr('dc:subject="', '"').partition(",")[::2],
            "description": extr('dc:description="', '"'),
            "date"       : self.parse_datetime_iso(extr('dc:date="', '"')),
            "tags"       : text.split_html(tags)[1:] if tags else [],
            "user"       : self.user,
            "body"       : body,
        }

    def _images(self, post):
        imgs = []
        body = post.pop("body")

        for num, img in enumerate(text.extract_iter(body, "<img ", ">"), 1):
            src = text.extr(img, 'src="', '"')
            alt = text.extr(img, 'alt="', '"')

            if not src:
                continue
            elif "://livedoor.blogimg.jp/" in src:
                url = src.replace("http:", "https:", 1).replace("-s.", ".")
            else:
                url = text.urljoin(self.root, src)
            name, _, ext = url.rpartition("/")[2].rpartition(".")

            imgs.append({
                "url"      : url,
                "num"      : num,
                "hash"     : name,
                "filename" : alt or name,
                "extension": ext,
                "post"     : post,
            })

        return imgs


class LivedoorBlogExtractor(LivedoorExtractor):
    """Extractor for a user's blog on blog.livedoor.jp"""
    subcategory = "blog"
    pattern = BASE_PATTERN + r"/?($|\?|#)"
    example = "http://blog.livedoor.jp/USER/"

    def posts(self):
        response = self.request(self.root + "/")
        page = response.text

        if response.history or self.groups[2]:
            return self.posts_custom(page)
        return self.posts_default(page)

    def posts_default(self, page):
        while True:
            extr = text.extract_from(page)
            while True:
                data = extr('<rdf:RDF', '</rdf:RDF>')
                if not data:
                    break
                body = extr('class="article-body-inner">',
                            'class="article-footer">')
                yield self._load(data, body)
            url = extr('<a rel="next" href="', '"')
            if not url:
                break
            page = self.request(url).text

    def posts_custom(self, page):
        last = None
        while True:
            if (pos := page.find('id="side')) >= 0:
                page = page[:pos]
            for match in LivedoorPostExtractor.pattern.finditer(page):
                if last != match[0]:
                    last = match[0]
                    yield self._extract_post(last)
            url = text.extr(page, '<a rel="next" href="', '"')
            if not url:
                break
            page = self.request(url).text


class LivedoorPostExtractor(LivedoorExtractor):
    """Extractor for images from a blog post on blog.livedoor.jp"""
    subcategory = "post"
    pattern = BASE_PATTERN + r"/archives/(\d+)\.html"
    example = "http://blog.livedoor.jp/USER/archives/12345.html"

    def posts(self):
        url = f"{self.root}/archives/{self.groups[3]}.html"
        return (self._extract_post(url),)
