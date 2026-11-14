# -*- coding: utf-8 -*-

# Copyright 2020 Leonid "Bepis" Pavel
# Copyright 2023-2026 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://imgchest.com/"""

from .common import GalleryExtractor, Extractor, Message
from .. import text, util

BASE_PATTERN = r"(?:https?://)?(?:www\.)?imgchest\.com"


class ImagechestGalleryExtractor(GalleryExtractor):
    """Extractor for image galleries from imgchest.com"""
    category = "imagechest"
    root = "https://imgchest.com"
    pattern = BASE_PATTERN + r"/p/([A-Za-z0-9]{11})"
    example = "https://imgchest.com/p/abcdefghijk"

    def __init__(self, match):
        self.gallery_id = match[1]
        url = self.root + "/p/" + self.gallery_id
        GalleryExtractor.__init__(self, match, url)

    def _init(self):
        if access_token := self.config("access-token"):
            self.api = ImagechestAPI(self, access_token)
            self.page_url = None
            self.metadata = self._metadata_api

    def metadata(self, page):
        try:
            data = util.json_loads(text.unescape(text.extr(
                page, 'data-page="', '"')))
            post = data["props"]["post"]
        except KeyError:
            raise self.exc.AuthRequired(
                "password", "gallery",
                "This post has been password protected.")
        except ValueError:
            if "<title>Not Found</title>" in page:
                raise self.exc.NotFoundError("gallery")
            self.log.error("Failed to load gallery data")
            post = {}

        self.files = post.pop("files", ())
        self.total = post.get("files_total", 0)
        post["gallery_id"] = self.gallery_id
        post["tags"] = [tag["name"] for tag in post.get("tags", ())]

        return post

    def _metadata_api(self, page):
        post = self.api.post(self.gallery_id)

        post["date"] = self.parse_datetime_iso(post["created"])
        for img in post["images"]:
            img["date"] = self.parse_datetime_iso(img["created"])

        post["gallery_id"] = self.gallery_id
        self.total = post.pop("image_count", 0)
        self.files = post.pop("images")

        return post

    def images(self, page):
        files = self.files
        if len(files) < self.total:
            files = self._pagination()

        try:
            return [
                (file["link"], file)
                for file in files
            ]
        except Exception as exc:
            self.traceback(exc)
            return ()

    def _pagination(self):
        url = f"{self.root}/p/{self.gallery_id}/files"
        params = {"page": 2}
        per_page = 40

        yield from self.files
        while True:
            data = self.request_json(url, params=params)

            yield from data["files"]

            if data["page"] * per_page >= data["total"]:
                break
            params["page"] += 1


class ImagechestUserExtractor(Extractor):
    """Extractor for imgchest.com user profiles"""
    category = "imagechest"
    subcategory = "user"
    root = "https://imgchest.com"
    pattern = BASE_PATTERN + r"/u/([^/?#]+)"
    example = "https://imgchest.com/u/USER"

    def items(self):
        url = self.root + "/api/posts"
        params = {
            "page"    : 1,
            "sort"    : "new",
            "tag"     : "",
            "q"       : "",
            "username": text.unquote(self.groups[0]),
            "nsfw"    : "true",
        }

        while True:
            try:
                data = self.request_json(url, params=params)["data"]
            except (TypeError, KeyError):
                return

            if not data:
                return

            for gallery in data:
                gallery["_extractor"] = ImagechestGalleryExtractor
                yield Message.Queue, gallery["link"], gallery

            params["page"] += 1


class ImagechestAPI():
    """Interface for the Image Chest API

    https://imgchest.com/docs/api/1.0/general/overview
    """
    root = "https://api.imgchest.com"

    def __init__(self, extractor, access_token):
        self.extractor = extractor
        self.headers = {"Authorization": "Bearer " + access_token}

    def file(self, file_id):
        endpoint = "/v1/file/" + file_id
        return self._call(endpoint)

    def post(self, post_id):
        endpoint = "/v1/post/" + post_id
        return self._call(endpoint)

    def user(self, username):
        endpoint = "/v1/user/" + username
        return self._call(endpoint)

    def _call(self, endpoint):
        url = self.root + endpoint

        while True:
            response = self.extractor.request(
                url, headers=self.headers, fatal=None, allow_redirects=False)

            if response.status_code < 300:
                return response.json()["data"]

            elif response.status_code < 400:
                raise self.extractor.exc.AuthenticationError(
                    "Invalid API access token")

            elif response.status_code == 429:
                self.extractor.wait(seconds=600)

            else:
                self.extractor.log.debug(response.text)
                try:
                    msg = f'"{response.json()["message"]}"'
                except Exception as exc:
                    self.log.traceback(exc)
                    msg = "API request failed"
                raise self.extractor.exc.AbortExtraction(msg)
