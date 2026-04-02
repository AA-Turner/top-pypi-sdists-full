from ratio.http.response import Response
from typing import Literal
from http import HTTPStatus


RedirectionType = Literal["temporary", "permanent", "301", "302"]


def _get_status_by_redirect_type(type_: RedirectionType) -> HTTPStatus:
    match type_:
        case "permanent":
            return HTTPStatus.PERMANENT_REDIRECT
        case "301":
            return HTTPStatus.MOVED_PERMANENTLY
        case "302":
            return HTTPStatus.FOUND
        case _:
            return HTTPStatus.TEMPORARY_REDIRECT


def redirect(url: str, type_: RedirectionType = "temporary") -> Response:
    status = _get_status_by_redirect_type(type_)
    response = Response.from_http_status(status)
    response.headers.put("Location", {url})
    return response
