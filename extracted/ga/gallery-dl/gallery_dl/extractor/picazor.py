# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://picazor.com/"""

from .common import Extractor, Message
from .. import text


class PicazorUserExtractor(Extractor):
    """Extractor for picazor users"""
    category = "picazor"
    subcategory = "user"
    root = "https://picazor.com"
    browser = "firefox"
    directory_fmt = ("{category}", "{user}")
    filename_fmt = "{id}_{num:>03}.{extension}"
    archive_fmt = "{id}_{num}"
    pattern = r"(?:https?://)?(?:www\.)?picazor\.(com|one)/[a-z]{2}/([^/?#]+)"
    example = "https://picazor.com/en/USERNAME"

    def items(self):
        tld, user = self.groups
        root = self.root[:-3] + tld
        first = True

        url = f"{root}/api/files/{user}/sfiles"
        params = {"page": 1}
        headers = {"Referer": f"{root}/en/{user}"}

        while True:
            data = self.request_json(url, params=params, headers=headers)
            if not data:
                break

            for item in data:
                path = item.get("path")
                if not path:
                    continue

                if first:
                    first = False
                    self.kwdict["user"] = user
                    self.kwdict["count"] = item.get("order")
                    yield Message.Directory, "", {
                        "userId": item.get("userId"),
                        "user"  : user,
                    }

                item.pop("blurDataURL", None)
                item["num"] = item["order"]

                file_url = root + path
                text.nameext_from_url(file_url, item)
                yield Message.Url, file_url, item

            params["page"] += 1
