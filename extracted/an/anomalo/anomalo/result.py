from __future__ import annotations

from contextlib import suppress
from functools import cached_property
from typing import Any, Literal, overload
from urllib.parse import parse_qs, urlparse

from requests import Response
from requests.utils import parse_header_links


class BadRequestException(RuntimeError):
    def __init__(self, message: str, status_code: int):
        self.status_code = status_code
        super().__init__(message)


class Result:
    def __init__(self, *args: Any, response: Response, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._response = response

    @cached_property
    def total_count(self) -> int | None:
        content_range = self._response.headers.get("Content-Range", "")
        if content_range.startswith("items "):
            with suppress(IndexError, ValueError):
                return int(content_range.split("/", 1)[1])
        return None

    @cached_property
    def pages(self) -> dict[str, dict[str, int]]:
        return {
            link["rel"]: self._get_page_params(link["url"])
            for link in parse_header_links(self._response.headers.get("Link", []))
        }

    @overload
    @classmethod
    def from_raw(
        cls, response: Response, output_style: Literal["json"] = "json"
    ) -> Result: ...

    @overload
    @classmethod
    def from_raw(
        cls, response: Response, output_style: Literal["text"] = "text"
    ) -> str: ...

    @classmethod
    def from_raw(cls, response: Response, output_style: str) -> Result | str:
        if output_style == "json":
            result = response.json()
            if isinstance(result, list):
                return ListResult(result, response=response)
            return DictResult(result or {}, response=response)
        return response.text

    @classmethod
    def _get_page_params(cls, url: str) -> dict[str, int]:
        filter_args = {"limit", "offset"}
        qs_args = parse_qs(urlparse(url).query)
        return {k: int(v[0]) for k, v in qs_args.items() if k in filter_args}


class ListResult(Result, list):
    pass


class DictResult(Result, dict):
    pass
