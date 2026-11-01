# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://febri.jp/"""

from .common import Extractor, Message
from .. import text

BASE_PATTERN = r"(?:https?://)?(?:www\.)?febri\.jp"


class FebriExtractor(Extractor):
    """Base class for febri extractors"""
    category = "febri"
    root = "https://febri.jp"
    directory_fmt = ("{category}", "{date:%Y.%m.%d} {title}")
    filename_fmt = "{num:>02}{caption:? //}.{extension}"
    archive_fmt = "{slug}-{num}"


class FebriArticleExtractor(FebriExtractor):
    subcategory = "article"
    pattern = BASE_PATTERN + r"/topics/([^/?#]+)"
    example = "https://febri.jp/topics/TITLE/"

    def items(self):
        slug = self.groups[0]
        url = f"{self.root}/topics/{slug}/"
        page = self.request(url).text
        extr = text.extract_from(page)

        og_title = extr('property="og:title" content="', ' | Febri"')
        og_description = extr('property="og:description" content="', '"')
        og_url = extr('property="og:url" content="', '"')

        files = [{
            "url"   : extr('property="og:image" content="', '"'),
            "width" : text.parse_int(extr(
                'property="og:image:width" content="', '"')),
            "height" : text.parse_int(extr(
                'property="og:image:height" content="', '"')),
            "type"  : "banner",
        }]

        article = {
            "title": text.unescape(og_title),
            "description": text.unescape(og_description),
            "url"  : text.unescape(og_url),
            "slug" : text.unquote(slug),
            "date" : self.parse_datetime_iso(extr(
                'property="article:published_time" content="', '"')),
            "summary": extr('<div class="des"><p>', "</p>\n</div>"),
            "tags" : text.split_html(extr('<ul class="list-tag">', "</ul>")),
        }

        while True:
            img = extr('<div class="blocks_general image_info', "</div>")
            if not img:
                break
            caption = text.extr(img, "<blockquote", "</blockquote>")
            files.append({
                "type"   : "image",
                "url"    : text.extr(img, 'src="', '"'),
                "caption": text.unescape(
                    caption[caption.find(">")+1:]).strip(),
            })

        article["count"] = len(files)
        yield Message.Directory, url, article
        for num, file in enumerate(files, 1):
            url = file["url"]
            file.update(article)
            file["num"] = num
            yield Message.Url, url, text.nameext_from_url(url, file)


class FebriTopicsExtractor(FebriExtractor):
    subcategory = "topics"
    pattern = BASE_PATTERN + r"/topics(?:/page/(\d+))?/?"
    example = "https://febri.jp/topics/"

    def items(self):
        base = self.root + "/topics/"
        pnum = text.parse_int(self.groups[0], 1)
        data = {"_extractor": FebriArticleExtractor}

        while True:
            url = f"{base}page/{pnum}/" if pnum > 1 else base
            page = self.request(url).text

            for box in text.extract_iter(page, 'class="box-article', '</div>'):
                href = text.unescape(text.extr(box, 'href="', '"'))
                yield Message.Queue, href, data

            if 'rel="next"' not in page:
                break
            pnum += 1
