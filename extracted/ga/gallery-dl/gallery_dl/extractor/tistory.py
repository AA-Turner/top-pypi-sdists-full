# -*- coding: utf-8 -*-

# Copyright 2026 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://www.tistory.com/"""

from .common import Extractor, Message
from .. import text

BASE_PATTERN = r"(?:https?://)?(?!www\.)([\w-]+)\.tistory\.com"


class TistoryExtractor(Extractor):
    """Base class for tistory extractors"""
    category = "tistory"
    root = "https://www.tistory.com"


class TistoryBlogExtractor(TistoryExtractor):
    subcategory = "blog"
    pattern = BASE_PATTERN + r"/(?:$|\?|#)"
    example = "https://USER.tistory.com/"

    def items(self):
        data = {"_extractor": TistoryArticleExtractor}
        root = f"https://{self.groups[0]}.tistory.com"
        pnum = 1

        while True:
            page = self.request(f"{root}/?page={pnum}").text

            url = None
            for post in text.extract_iter(page, 'class="post-item"', "</"):
                url = root + text.extr(post, 'href="', '"')
                yield Message.Queue, url, data
            if url is None:
                for post in text.extract_iter(page, '<article class=', "</"):
                    url = root + text.extr(post, 'href="', '"')
                    yield Message.Queue, url, data
            if url is None:
                break

            pnum += 1


class TistoryArticleExtractor(TistoryExtractor):
    subcategory = "article"
    directory_fmt = ("{category}", "{blog}",
                     "{date:%Y-%m-%d}{id:? //} {title}")
    filename_fmt = "{num:>02} {filename}.{extension}"
    archive_fmt = "{txid}/{num}"
    pattern = BASE_PATTERN + r"/(\d+|entry/[^/?#]+)"
    example = "https://USER.tistory.com/12345"

    def items(self):
        user, path = self.groups
        url = f"https://{user}.tistory.com/{path}"
        page = self.request(url).text
        extr = text.extract_from(page)

        article = {
            "id"     : text.parse_int(path),
            "blog"   : text.unquote(user),
            "blog_id": extr('"BLOG":{"id":', ","),
            "url"    : text.unescape(extr(
                'property="og:url" content="', '"')),
            "author" : text.unescape(extr(
                'property="og.article.author" content="', '"')),
            "title"  : text.unescape(extr(
                'property="og:title" content="', '"')),
            "description": text.unescape(extr(
                'property="og:description" content="', '"')),
            "cover"  : text.unescape(extr(
                'property="og:image" content="', '"')),
            "section": text.unescape(extr(
                'property="article:section" content="', '"')),
            "txid"   : extr(
                'property="article:txid" content="', '"'),
            "date"   : self.parse_datetime_iso(extr(
                'property="article:published_time" content="', '"')),
        }

        page_article = extr('="container"', "<!-- PostListinCategory")
        article["tags"] = text.split_html(
            extr('class="tags">', "</div>"))[1::2]

        files = []
        for img in text.extract_iter(page_article, "<img ", ">"):
            url = text.unescape(text.extr(img, 'src="', '"'))
            file = {
                "file_url": url,
                "width": text.parse_int(
                    text.extr(img, 'data-origin-width="', '"') or
                    text.extr(img, 'width="', '"')),
                "height": text.parse_int(
                    text.extr(img, 'data-origin-height="', '"') or
                    text.extr(img, 'height="', '"')),
            }
            if (name := text.extr(img, 'data-filename="', '"')) and \
                    name not in {"blob", "img", ""}:
                text.nameext_from_name(text.unescape(name), file)
                if not file["extension"]:
                    file["extension"] = text.ext_from_url(url)
            else:
                text.nameext_from_url(url, file)
            files.append(file)

        article["count"] = len(files)
        yield Message.Directory, "", article
        for article["num"], file in enumerate(files, 1):
            file.update(article)
            yield Message.Url, file["file_url"], file


class TistoryDirectLinkExtractor(TistoryExtractor):
    subcategory = "direct-link"
    pattern = (r"(?:https?://)?(?:"
               r"cfile\d+\.\w+\.(?:tistory\.com|daum\.net)"
               r"/(?:original|image|attach|media)"
               r"|t\d+\.daumcdn\.net/cfile/tistory"
               r")/\w+")
    example = "http://cfile1.uf.tistory.com/original/0246813579ACEBDF"

    def items(self):
        url = text.ensure_http_scheme(self.url, "http://")
        data = text.nameext_from_url(url)

        if not data["extension"]:
            data["extension"] = "jpg"  # guess extension

        yield Message.Directory, "", data
        yield Message.Url, url, data
