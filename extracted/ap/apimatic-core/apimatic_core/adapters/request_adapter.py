# apimatic_core/adapters/request_adapter.py

from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Mapping, Optional, Union

from http.cookies import SimpleCookie

from apimatic_core_interfaces.http.request import Request
from apimatic_core.adapters.types.django_request_like import DjangoRequestLike
from apimatic_core.adapters.types.flask_request_like import FlaskRequestLike
from apimatic_core.adapters.types.starlette_request_like import StarletteRequestLike


# -----------------------
# Shared utilities
# -----------------------

def _as_listdict(obj: Any) -> Dict[str, List[str]]:
    if not obj:
        return {}
    getlist = getattr(obj, "getlist", None)
    if callable(getlist):
        return {str(k): list(getlist(k)) for k in obj.keys()}
    return {str(k): [str(v)] for k, v in dict(obj).items()}


def _content_type(headers: Mapping[str, str]) -> str:
    """Return lower-cased Content-Type value or empty string."""
    return (headers.get("content-type") or headers.get("Content-Type") or "").lower()


def _is_urlencoded_or_multipart(headers: Mapping[str, str]) -> bool:
    """Check if body is form-like (urlencoded/multipart)."""
    ct = _content_type(headers)
    return ct.startswith(("multipart/form-data", "application/x-www-form-urlencoded"))


def _cookies_from_header(headers: Mapping[str, str]) -> Dict[str, str]:
    """Parse Cookie header into a dict, returns {} if absent/empty."""
    cookie_header = headers.get("Cookie") or headers.get("cookie")
    if not cookie_header:
        return {}
    jar = SimpleCookie()
    jar.load(cookie_header)
    return {k: morsel.value for k, morsel in jar.items()}


def _django_headers_fallback(req: DjangoRequestLike) -> Dict[str, str]:
    """
    Fallback for very old Django where `request.headers` is missing/empty.
    Builds headers from META['HTTP_*'] entries.
    """
    meta = getattr(req, "META", {}) or {}
    return {
        k[5:].replace("_", "-"): str(v)
        for k, v in meta.items()
        if isinstance(k, str) and k.startswith("HTTP_")
    }


def _unwrap_local_proxy(obj: Any) -> Any:
    """
    Best-effort unwrapping for LocalProxy-like objects (e.g., Werkzeug/Flask).
    If `_get_current_object` exists and works, return the underlying object.
    If calling it raises, swallow and return the original object.
    If it doesn't exist, return the original object.
    """
    get_current = getattr(obj, "_get_current_object", None)
    if callable(get_current):
        try:
            return get_current()
        except Exception:
            return obj
    return obj


# -----------------------
# Per-framework converters
# -----------------------

async def _from_starlette(req: StarletteRequestLike) -> Request:
    headers = dict(req.headers)
    raw = await req.body()
    query = _as_listdict(req.query_params)
    cookies = dict(req.cookies)
    url_str = str(req.url)
    path = req.url.path

    form: Dict[str, List[str]] = {}
    if _is_urlencoded_or_multipart(headers):
        form_data = await req.form()
        for k in form_data.keys():
            # Filter out file-like parts (e.g., UploadFile: has filename & read)
            values = [
                str(v)
                for v in form_data.getlist(k)
                if not (hasattr(v, "filename") and hasattr(v, "read"))
            ]
            if values:
                form[k] = values

    return Request(
        method=req.method,
        path=path,
        url=url_str,
        headers=headers,
        raw_body=raw,
        query=query,
        cookies=cookies,
        form=form,
    )


def _from_flask(req: FlaskRequestLike) -> Request:
    headers = dict(req.headers)
    url_str: Optional[str] = getattr(req, "url", None)
    path: str = req.path
    raw: bytes = req.get_data(cache=True)
    query = _as_listdict(req.args)
    cookies = dict(req.cookies) or _cookies_from_header(headers)
    form = _as_listdict(req.form)

    return Request(
        method=req.method,
        path=path,
        url=url_str,
        headers=headers,
        raw_body=raw,
        query=query,
        cookies=cookies,
        form=form,
    )


def _from_django(req: DjangoRequestLike) -> Request:
    headers = dict(getattr(req, "headers", {}) or {}) or _django_headers_fallback(req)
    url_str = req.build_absolute_uri()
    path = req.path
    raw = bytes(getattr(req, "body", b"") or b"")
    query = _as_listdict(getattr(req, "GET", {}))
    cookies = dict(getattr(req, "COOKIES", {}) or {})
    form = _as_listdict(getattr(req, "POST", {}))

    return Request(
        method=req.method,
        path=path,
        url=url_str,
        headers=headers,
        raw_body=raw,
        query=query,
        cookies=cookies,
        form=form,
    )


# -----------------------
# Public API
# -----------------------

async def to_unified_request_async(
    req: Union[StarletteRequestLike, FlaskRequestLike, DjangoRequestLike]
) -> Request:
    """
    Convert a framework request (Starlette/FastAPI, Flask/Werkzeug, or Django) to a unified snapshot.

    Uses structural typing to detect the request “shape” and extracts an immutable snapshot
    (no file uploads). See per-framework helpers for exact extraction rules.
    """
    if isinstance(req, StarletteRequestLike):
        return await _from_starlette(req)
    if isinstance(req, FlaskRequestLike):
        return _from_flask(req)
    if isinstance(req, DjangoRequestLike):
        return _from_django(req)
    raise TypeError(f"Unsupported request type: {type(req)!r}")


def to_unified_request(
    req: Union[StarletteRequestLike, FlaskRequestLike, DjangoRequestLike, Any]
) -> Request:
    """
    Synchronous wrapper around `to_unified_request` with LocalProxy unwrapping.
    """
    unwrapped = _unwrap_local_proxy(req)
    # We expect to be called from sync code; create and run a fresh loop.
    return asyncio.run(to_unified_request_async(unwrapped))
