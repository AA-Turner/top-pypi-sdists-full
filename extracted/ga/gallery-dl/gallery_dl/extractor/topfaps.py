# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://topfaps.com"""

from .common import Extractor, Message
from .. import text, util

BASE_PATTERN = r"(?:https?://)?(?:www\.)?topfaps\.com"


class TopfapsExtractor(Extractor):
    """Base class for topfaps extractors"""
    category = "topfaps"
    root = "https://topfaps.com"
    cookies_domain = ".topfaps.com"
    directory_fmt = ("{category}", "{creator}")
    filename_fmt = "{id}_{filename}.{extension}"
    archive_fmt = "{type}_{id}"

    @staticmethod
    def _decode_stream(token):
        """Decode 'stream_url_play' into a playable URL

        The token is a reversed base64 string, padded with
        16 junk characters at both ends.
        """
        if not token:
            return None
        try:
            token = token[-17:15:-1]  # token[::-1][16:-16]
            url = util.b64decode(token + "==")
        except Exception:
            return None
        return url if url.startswith("http") else None

    def _video_url(self, url, data):
        """Prepare HLS download via yt-dlp and return the 'ytdl:' URL"""
        self.log.debug("Stream URL: %s", url)
        data["extension"] = "mp4"
        data["_ytdl_manifest"] = "hls"
        data["_ytdl_manifest_headers"] = {
            "Referer"   : self.root + "/",
            "Origin"    : self.root,
            "User-Agent": self.session.headers.get("User-Agent"),
        }
        return "ytdl:" + url

    def _find_stream(self, page):
        """Look for a playable stream URL in a video page"""
        # obfuscated token (same format as 'stream_url_play')
        for token in text.re(r"[A-Za-z0-9+/=]{120,}").findall(page):
            if url := self._decode_stream(token):
                return url
        return None

    def _media_from_item(self, item, creator):
        """Build (url, kwdict) from an entry of the JSON API"""
        is_video = (item.get("type") == 1)
        data = {
            "id"          : item["id"],
            "title"       : text.unescape(item.get("title") or ""),
            "views"       : item.get("count_views"),
            "date"        : self.parse_datetime_iso(item.get(
                "published_date")),
            "creator"     : creator,
            "model_id"    : item.get("model_id"),
            "product_code": item.get("product_code"),
            "type"        : "video" if is_video else "photo",
            "thumbnail"   : item.get("thumbnail"),
        }

        if is_video:
            if url := self._decode_stream(item.get("stream_url_play")):
                data["filename"] = str(item["id"])
                return self._video_url(url, data), data
            self.log.warning("%s: Unable to decode video URL", item["id"])
            return None, None

        if url := item.get("image"):
            return url, text.nameext_from_url(url, data)
        self.log.warning("%s: No image URL found", item["id"])
        return None, None


class TopfapsModelExtractor(TopfapsExtractor):
    """Extractor for a model's posts on topfaps.com"""
    subcategory = "model"
    pattern = BASE_PATTERN + r"/model/([^/?#]+)(?:/?\?([^#]+))?"
    example = "https://topfaps.com/model/CREATOR"

    def items(self):
        creator, query = self.groups
        query = text.parse_query(query) if query else {}

        mtype = (query.get("type") or "all").lower()
        if mtype == "all":
            types = ("photos", "videos")
        else:
            types = (mtype,)
        order = query.get("order") or "0"

        for mtype in types:
            for item in self._pagination(creator, mtype, order):
                url, data = self._media_from_item(item, creator)
                if not url:
                    continue
                yield Message.Directory, "", data
                yield Message.Url, url, data

    def _pagination(self, creator, mtype, order):
        url = f"{self.root}/model/{creator}"
        headers = {
            "Accept"          : "*/*",
            "Accept-Language" : "en-US,en;q=0.9",
            "X-Requested-With": "XMLHttpRequest",
            "Referer"         : url,
        }
        params = {"page": 1, "type": mtype, "order": order}
        seen = set()

        while True:
            response = self.request(url, params=params, headers=headers)
            try:
                data = util.json_loads(response.text)
            except ValueError:
                self.log.error(
                    "Unexpected non-JSON response (status %s, %s): %.500s",
                    response.status_code,
                    response.headers.get("content-type"),
                    response.text)
                return
            if not data or data.__class__ is not list:
                return

            new = 0
            for item in data:
                pid = item["id"]
                if pid in seen:
                    continue
                seen.add(pid)
                new += 1
                yield item

            # stop if the server repeats pages beyond the last one
            if not new:
                return
            params["page"] += 1


class TopfapsPostExtractor(TopfapsExtractor):
    """Extractor for individual photo/video posts on topfaps.com"""
    subcategory = "post"
    pattern = BASE_PATTERN + r"/(photo|video)/(\d+)"
    example = "https://topfaps.com/photo/12345"

    def items(self):
        ptype, post_id = self.groups
        page = self.request(f"{self.root}/{ptype}/{post_id}").text

        title = text.unescape(text.extr(
            page, 'class="img-fluid w-100 thumbnail" alt="', '"')).strip()
        creator = text.extr(page, 'href="/model/', '"') or \
            text.extr(page, f'href="{self.root}/model/', '"') or "unknown"

        data = {
            "id"     : text.parse_int(post_id),
            "title"  : title,
            "creator": creator.strip("/"),
            "type"   : ptype,
        }

        if ptype == "photo":
            url = text.extr(page, 'data-fancybox="" src="', '"')
            if not url:
                match = text.re(
                    r'data-fancybox[^>]*\ssrc="([^"]+)"').search(page)
                url = match[1] if match else None
            if not url:
                raise self.exc.NotFoundError("photo")
            text.nameext_from_url(url, data)
        else:
            url = self._find_stream(page)
            if not url:
                self.log.error("%s: Unable to find video stream", post_id)
                raise self.exc.NotFoundError("video")
            data["filename"] = str(post_id)
            url = self._video_url(url, data)

        yield Message.Directory, "", data
        yield Message.Url, url, data
