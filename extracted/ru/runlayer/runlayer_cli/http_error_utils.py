from typing import cast

import httpx


def format_validation_detail_item(item: object) -> str:
    if not isinstance(item, dict):
        return str(item)

    payload = cast(dict[str, object], item)
    loc = payload.get("loc")
    msg = payload.get("msg")
    path = ""
    if isinstance(loc, list):
        parts = [str(part) for part in loc if part != "body"]
        path = ".".join(parts)
    elif loc is not None:
        path = str(loc)

    if isinstance(msg, str) and msg:
        return f"{path}: {msg}" if path else msg

    return str(item)


def extract_http_error_detail(error: httpx.HTTPStatusError) -> str | None:
    try:
        payload = error.response.json()
    except ValueError:
        return None

    if not isinstance(payload, dict):
        return None

    detail = payload.get("detail")
    if isinstance(detail, str) and detail:
        return detail
    if isinstance(detail, list) and detail:
        return "; ".join(format_validation_detail_item(item) for item in detail)

    return None
