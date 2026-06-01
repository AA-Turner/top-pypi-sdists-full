"""HTTP response-specific types that depend on httpx."""

from collections.abc import Callable
from typing import Any

from httpx import Response

from csrd.models.model_parser._types import ResponseModelType

ResponseHandler = Callable[[Response], Response | None]
ResponseHandlerMap = dict[int, ResponseHandler]
ModelHandler = Callable[[Response, ResponseModelType | None], Any]

__all__ = ("ModelHandler", "ResponseHandler", "ResponseHandlerMap")
