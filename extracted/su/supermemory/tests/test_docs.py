"""Run every ```python snippet in the docs against a mocked API, so docs can't rot.

Snippets in one file share a namespace and run in order, like a reader would.
Snippets with top-level `await` run in an event loop.
"""

import ast
import asyncio
import inspect
import re
from pathlib import Path
from typing import Any

import httpx
import pytest

ROOT = Path(__file__).resolve().parent.parent
DOCS = ["README.md", "MIGRATION.md"]

_SEARCH = {
    "results": [
        {
            "id": "mem_1",
            "memory": "Alex prefers morning meetings",
            "similarity": 0.92,
            "isLatest": True,
            "metadata": {},
            "system": {"updatedAt": "2026-10-01T09:00:00Z"},
        }
    ],
    "searchTime": 12.5,
}
_RESPONSES: dict[str, Any] = {
    "search": _SEARCH,
    "profile": {"profile": {"static": [{"id": "p1", "memory": "Lives in SF"}], "dynamic": [], "buckets": {}}},
    "document": {"id": "doc_1", "status": "queued"},
}


def _respond(request: httpx.Request) -> httpx.Response:
    path = request.url.path
    if "missing" in path:
        return httpx.Response(404, json={"error": "Document not found"}, request=request)
    for key, body in _RESPONSES.items():
        if path.rstrip("/").endswith(key) or f"/{key}/" in path:
            return httpx.Response(200, json=body, request=request)
    return httpx.Response(200, json={}, request=request)


class _Transport(httpx.BaseTransport):
    def handle_request(self, request: httpx.Request) -> httpx.Response:
        request.read()
        return _respond(request)


class _AsyncTransport(httpx.AsyncBaseTransport):
    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        await request.aread()
        return _respond(request)


def _snippets(doc: str) -> list:
    return re.findall(r"```python\n(.*?)```", (ROOT / doc).read_text(), re.S)


@pytest.mark.filterwarnings("error")
@pytest.mark.parametrize("doc", DOCS)
def test_doc_snippets_run(doc: str, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SUPERMEMORY_API_KEY", "sm_test")
    monkeypatch.chdir(tmp_path)
    (tmp_path / "notes.pdf").write_bytes(b"%PDF-1.4 test")
    monkeypatch.setattr(httpx.HTTPTransport, "handle_request", _Transport.handle_request)
    monkeypatch.setattr(httpx.AsyncHTTPTransport, "handle_async_request", _AsyncTransport.handle_async_request)
    monkeypatch.setattr("builtins.print", lambda *_, **__: None)

    namespace: dict[str, Any] = {"__name__": "__docs__"}
    snippets = _snippets(doc)
    assert snippets, f"no python snippets in {doc}"
    for index, snippet in enumerate(snippets, 1):
        code = compile(snippet, f"{doc}#snippet{index}", "exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
        try:
            result = eval(code, namespace)
            if inspect.iscoroutine(result):
                asyncio.run(result)
        except Exception as err:  # noqa: BLE001
            raise AssertionError(f"{doc} snippet {index} failed:\n{snippet}") from err
