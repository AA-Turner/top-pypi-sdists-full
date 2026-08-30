# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://fileditchfiles.st/"""

from .common import Extractor, Message
from .. import text, util
import hashlib

BASE_PATTERN = r"(?:https?://)?(?:www\.)?fileditchfiles\.st"


class FileditchfilesExtractor(Extractor):
    """Base class for fileditchfiles extractors"""
    category = "fileditchfiles"
    root = "https://fileditchfiles.st"


class FileditchfilesFileExtractor(FileditchfilesExtractor):
    """Extractor for fileditchfiles files"""
    subcategory = "file"
    filename_fmt = "{id}.{extension}"
    archive_fmt = "{id}"
    pattern = BASE_PATTERN + r"/[^/?#]+/([^/?#]+)/([^/?#]+)"
    example = "https://fileditchfiles.st/xyz01/ID/SLUG"

    def items(self):
        url = text.ensure_http_scheme(self.url)
        page = self.request(url).text

        if (pos := page.find('class="verifying-overlay"')) >= 0:
            data = text.extract_all(page, (
                ("orig_ref", '"orig_ref" value="', '"'),
                ("pow_challenge", 'value="', '"'),
                ("pow_ts"  , 'value="', '"'),
                ("pow_diff", 'value="', '"'),
                ("pow_sig" , 'value="', '"'),
            ), pos)[0]
            diff = text.parse_int(data["pow_diff"])
            data["pow_nonce"] = _nonce(data["pow_challenge"], diff)
            page = self.request(url, method="POST", data=data).text

        extr = text.extract_from(page)
        file = {
            "id": self.groups[0],
            "slug": self.groups[1],
            "path": extr('class="path">', "</span>"),
            "size": text.parse_bytes(extr(
                'class="size">', "</span>").replace(" ", "")[:-1]),
            "downloads": text.parse_int(extr(
                'class="dlcount">⬇ ', " downloads</span>"))
        }
        yield Message.Directory, "", file
        url = "".join(util.json_loads(extr("var u = ", ".join(")))
        yield Message.Url, url, text.nameext_from_url(url, file)


class FileditchfilesShorturlExtractor(FileditchfilesExtractor):
    """Extractor for short file URls"""
    subcategory = "shorturl"
    pattern = r"(?:https?://)?(?:www\.)?theditch\.st/([^/?#]+)"
    example = "https://theditch.st/ID"

    def items(self):
        page = self.request(text.ensure_http_scheme(self.url)).text
        data = {
            "id": self.groups[0],
            "_extractor": FileditchfilesFileExtractor,
        }
        yield Message.Queue, text.extr(page, 'var u = "', '"'), data


def _nonce(challenge, diff):
    def leading_zero_bits(data, need):
        full = need >> 3
        rem = need & 7
        for i in range(0, full):
            if data[i] != 0:
                return False
        if rem:
            if (data[full] & ((0xFF << (8 - rem)) & 0xFF)) != 0:
                return False
        return True

    prefix = challenge + ":"
    nonce = 0
    while True:
        digest = hashlib.sha256((prefix + str(nonce)).encode()).digest() + b"0"
        if leading_zero_bits(digest, diff):
            return nonce
        nonce += 1
