#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from typing import Tuple


def url_split(url: str) -> Tuple[str, dict]:
    if "?" not in url:
        return url, {}

    path, query = url.split("?")
    params = {}
    if "&" in query:
        for pair in query.split("&"):
            k, v = pair.split("=")
            params[k] = v
    else:
        k, v = params.split("&")
        params[k] = v
    return path, params
