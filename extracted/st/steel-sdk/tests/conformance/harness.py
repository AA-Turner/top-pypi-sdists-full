from __future__ import annotations

import re
import json
from typing import Any, Dict, List, Callable, Iterator, cast
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import unquote, unquote_plus

import httpx
import respx

FIXTURE: Dict[str, Any] = json.loads((Path(__file__).parent / "cases.json").read_text(encoding="utf-8"))
BASE_URL = "http://conformance.test"

DATE_TIME = re.compile(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2})(:\d{2})?(\.\d+)?(Z|[+-]\d{2}:\d{2})$")
NUMBER = re.compile(r"^-?\d+(\.\d+)?([eE][+-]?\d+)?$")


def instant(text: str) -> str | None:
    match = DATE_TIME.match(text)
    if match is None:
        return None
    minutes, seconds, fraction, zone = match.groups()
    digits = (fraction or ".0")[1:7].ljust(6, "0")
    offset = "+00:00" if zone in ("Z", "z") else zone
    moment = datetime.fromisoformat(f"{minutes}{seconds or ':00'}.{digits}{offset}")
    return "time:" + moment.astimezone(timezone.utc).isoformat()


def scalar(text: str) -> str:
    moment = instant(text)
    if moment is not None:
        return moment
    if NUMBER.match(text):
        return f"number:{float(text)!r}"
    return text


def normalize(value: Any) -> Any:
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, (int, float)):
        return f"number:{float(value)!r}"
    if isinstance(value, str):
        moment = instant(value)
        return value if moment is None else moment
    if isinstance(value, list):
        return [normalize(item) for item in cast(List[Any], value)]
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in cast(Dict[str, Any], value).items()}
    return value


def dump(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return value.to_dict(mode="json")
    if isinstance(value, list):
        return [dump(item) for item in cast(List[Any], value)]
    return value


def query(raw: str) -> List[str]:
    pairs: List[str] = []
    for pair in raw.split("&"):
        if not pair:
            continue
        key, _, value = pair.partition("=")
        pairs.append(f"{unquote_plus(key)}={scalar(unquote_plus(value))}")
    return sorted(pairs)


def attribute(header: str, name: str) -> str | None:
    for part in header.split(";"):
        key, separator, value = part.strip().partition("=")
        if separator and key.strip().lower() == name:
            return value.strip().strip('"')
    return None


def parts(body: bytes, content_type: str) -> List[str]:
    boundary = attribute(content_type, "boundary")
    assert boundary, f"multipart body without a boundary: {content_type}"
    chunks = body.decode("latin-1").split(f"--{boundary}")
    out: List[str] = []
    for chunk in chunks[1:-1]:
        trimmed = chunk[2:] if chunk.startswith("\r\n") else chunk
        trimmed = trimmed[:-2] if trimmed.endswith("\r\n") else trimmed
        head, _, content = trimmed.partition("\r\n\r\n")
        disposition = next(
            (line for line in head.split("\r\n") if line.lower().startswith("content-disposition:")),
            "",
        )
        name = attribute(disposition, "name") or ""
        text = content.encode("latin-1").decode("utf-8")
        if attribute(disposition, "filename") is not None:
            out.append(f"{name}=file:{text}")
        else:
            out.append(f"{name}={scalar(text)}")
    return sorted(out)


def check(id: str, request: httpx.Request, expected: Dict[str, Any]) -> None:
    assert request.method == expected["method"], f"{id} method"
    raw_path = request.url.raw_path.decode("ascii")
    path, _, search = raw_path.partition("?")
    segments = [unquote(segment) for segment in path.split("/") if segment]
    assert segments == expected["path"], f"{id} path"
    assert query(search) == sorted(f"{key}={scalar(value)}" for key, value in expected["query"]), f"{id} query"
    for name, value in expected["headers"].items():
        assert request.headers.get(name) == value, f"{id} header {name}"
    content_type = request.headers.get("content-type", "")
    body = expected["body"]
    content = request.read()
    if body is None:
        assert content == b"", f"{id} body should be empty"
    elif "json" in body:
        assert content_type.startswith("application/json"), f"{id} content type {content_type}"
        assert normalize(json.loads(content)) == normalize(body["json"]), f"{id} body"
    else:
        assert content_type.startswith("multipart/form-data"), f"{id} content type {content_type}"
        expected_parts = sorted(
            f"{part['name']}=file:{part['file']}" if "file" in part else f"{part['name']}={scalar(part['value'])}"
            for part in body["multipart"]
        )
        assert parts(content, content_type) == expected_parts, f"{id} parts"


def replies(exchanges: List[Dict[str, Any]]) -> Iterator[httpx.Response]:
    for exchange in exchanges:
        reply = exchange["response"]
        headers = {"content-type": reply["contentType"]} if reply["contentType"] else {}
        body = reply["body"]
        if body is None:
            yield httpx.Response(reply["status"], headers=headers)
        elif "json" in body:
            yield httpx.Response(reply["status"], headers=headers, content=json.dumps(body["json"]).encode("utf-8"))
        else:
            yield httpx.Response(reply["status"], headers=headers, content=body["text"].encode("utf-8"))
    while True:
        yield httpx.Response(500)


def conform(id: str, make: Callable[[str, str, bool], Any], call: Callable[[Any], Any]) -> None:
    case = FIXTURE["cases"][id]
    exchanges: List[Dict[str, Any]] = case["exchanges"]
    responses = replies(exchanges)
    requests: List[httpx.Request] = []

    def respond(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return next(responses)

    with respx.mock(base_url=BASE_URL, assert_all_called=False) as router:
        router.route().mock(side_effect=respond)
        result = dump(call(make(BASE_URL, FIXTURE["apiKey"], not case["lenient"])))
    assert len(requests) == len(exchanges), f"{id} requests"
    for request, exchange in zip(requests, exchanges):
        check(id, request, exchange["request"])
    expected = case["result"]
    if "ids" in expected:
        assert result == expected["ids"], f"{id} ids"
    elif "text" in expected:
        assert result == expected["text"], f"{id} text"
    elif "json" in expected:
        assert normalize(result) == normalize(expected["json"]), f"{id} result"
