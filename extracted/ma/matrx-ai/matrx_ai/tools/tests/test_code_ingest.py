"""Tests for the code_ingest bundle tools (git_ingest, llms_txt_fetch, package_info).

DB stubs are configured by the top-level conftest (``packages/matrx-ai/conftest.py``)
before collection, so importing the tools here is safe. Network is mocked with real
``httpx.Response`` objects; ``git_ingest`` uses a real local directory (no git/network).
"""
from __future__ import annotations

import asyncio
import threading
from pathlib import Path
from typing import Any

import httpx
import pytest

from matrx_ai.tools.implementations import code_ingest
from matrx_ai.tools.models import ToolContext
from matrx_ai.tools.result_gate import apply_size_gate

CTX = ToolContext(call_id="test")
# A small, stable local dir to ingest — the arg_models package itself.
LOCAL_DIR = str(Path(code_ingest.__file__).resolve().parent.parent / "arg_models")


# --------------------------------------------------------------------------- #
# git_ingest                                                                   #
# --------------------------------------------------------------------------- #

async def test_git_ingest_local_tree_mode():
    res = await code_ingest.git_ingest({"source": LOCAL_DIR, "mode": "tree"}, CTX)
    assert res.success, res.error
    assert res.output["summary"]
    assert "tree" in res.output
    assert "content" not in res.output  # tree mode omits content


async def test_git_ingest_digest_truncates_with_note():
    res = await code_ingest.git_ingest(
        {"source": LOCAL_DIR, "mode": "digest", "max_chars": 500}, CTX
    )
    assert res.success, res.error
    assert res.output["truncated"] is True
    assert res.output["content_chars_returned"] <= 500
    assert res.output["content_total_chars"] > 500
    assert "note" in res.output and "truncated" in res.output["note"].lower()
    assert res.output_self_capped is True


async def test_git_ingest_large_result_is_structurally_bounded(monkeypatch):
    """Every gitingest-owned text field is capped before the universal gate."""

    def _large_ingest(*_args, **_kwargs):
        return "s" * 20_000, "t" * 80_000, "c" * 200_000

    import gitingest

    monkeypatch.setattr(gitingest, "ingest", _large_ingest)
    res = await code_ingest.git_ingest(
        {"source": LOCAL_DIR, "mode": "digest", "max_chars": 500_000}, CTX
    )

    assert res.success is True
    assert res.output_self_capped is True
    assert res.output["summary_chars"]["truncated"] is True
    assert res.output["tree_chars"]["truncated"] is True
    assert res.output["truncated"] is True
    assert len(res.output["content"]) == code_ingest._GIT_INGEST_CONTENT_CHARS

    content, truncated = apply_size_gate(
        res.to_tool_result_content(),
        output_self_capped=res.output_self_capped,
        tool_name="git_ingest",
        tool_kind="native",
        conversation_id="conv-test",
        user_id="user-test",
    )
    assert truncated is False
    assert len(content["content"]) < 50_000


async def test_git_ingest_keeps_blocking_walk_off_event_loop(monkeypatch):
    """The third-party async entrypoint walks files synchronously; the tool must
    place the complete ingestion lifecycle on a worker thread."""
    loop_thread = threading.get_ident()
    worker_thread: int | None = None
    release = threading.Event()

    def _blocking_ingest(*_args, **_kwargs):
        nonlocal worker_thread
        worker_thread = threading.get_ident()
        release.wait(timeout=1)
        return "summary", "tree", "content"

    import gitingest

    monkeypatch.setattr(gitingest, "ingest", _blocking_ingest)
    task = asyncio.create_task(
        code_ingest.git_ingest({"source": LOCAL_DIR, "mode": "tree"}, CTX)
    )
    await asyncio.sleep(0.01)
    assert worker_thread is not None
    assert worker_thread != loop_thread
    assert task.done() is False
    release.set()
    result = await task
    assert result.success is True


async def test_git_ingest_remote_without_git_is_clean_error(monkeypatch):
    """A remote source with no `git` CLI returns a clean unavailable error and
    never reaches gitingest (no traceback)."""
    monkeypatch.setattr(code_ingest.shutil, "which", lambda _name: None)

    def _boom(*_a, **_kw):  # gitingest must not be called
        raise AssertionError("ingest should not run when git is absent")

    import gitingest

    monkeypatch.setattr(gitingest, "ingest", _boom)
    res = await code_ingest.git_ingest(
        {"source": "https://github.com/owner/repo"}, CTX
    )
    assert res.success is False
    assert res.error.error_type == "unavailable"
    assert res.error.traceback is None


# --------------------------------------------------------------------------- #
# httpx mocking helpers                                                        #
# --------------------------------------------------------------------------- #

class _FakeAsyncClient:
    def __init__(self, responses: dict[str, httpx.Response]):
        self._responses = responses

    async def __aenter__(self) -> "_FakeAsyncClient":
        return self

    async def __aexit__(self, *_a: Any) -> bool:
        return False

    async def get(self, url: str, headers: dict[str, str] | None = None) -> httpx.Response:
        for key, resp in self._responses.items():
            if key in url:
                return resp
        return httpx.Response(404, request=httpx.Request("GET", url))


def _patch_httpx(monkeypatch, responses: dict[str, httpx.Response]) -> None:
    monkeypatch.setattr(
        code_ingest.httpx, "AsyncClient", lambda *a, **k: _FakeAsyncClient(responses)
    )


# --------------------------------------------------------------------------- #
# llms_txt_fetch                                                               #
# --------------------------------------------------------------------------- #

async def test_llms_txt_fetch_parses_structure(monkeypatch):
    body = (
        "# Example Docs\n"
        "> The official docs for Example.\n\n"
        "## Guides\n"
        "- [Quickstart](https://ex.com/quick): get going\n"
        "- [API](https://ex.com/api)\n"
    )
    req = httpx.Request("GET", "https://docs.example.com/llms.txt")
    _patch_httpx(monkeypatch, {"llms.txt": httpx.Response(200, text=body, request=req)})

    res = await code_ingest.llms_txt_fetch({"url": "docs.example.com"}, CTX)
    assert res.success, res.error
    assert res.output.kind_ == "llms_txt_document"
    assert res.output.model_dump(mode="json", by_alias=True)["__kind"] == "llms_txt_document"
    parsed = res.output.parsed
    assert parsed.title == "Example Docs"
    assert parsed.summary == "The official docs for Example."
    assert parsed.sections[0].name == "Guides"
    assert parsed.sections[0].links[0].url == "https://ex.com/quick"
    assert parsed.sections[0].links[0].notes == "get going"


async def test_llms_txt_fetch_target_url_construction(monkeypatch):
    captured: dict[str, str] = {}

    class _Capture(_FakeAsyncClient):
        async def get(self, url: str, headers=None):
            captured["url"] = url
            return httpx.Response(200, text="# x", request=httpx.Request("GET", url))

    monkeypatch.setattr(code_ingest.httpx, "AsyncClient", lambda *a, **k: _Capture({}))
    await code_ingest.llms_txt_fetch({"url": "https://docs.example.com", "full": True}, CTX)
    assert captured["url"] == "https://docs.example.com/llms-full.txt"


async def test_llms_txt_fetch_404_is_not_found(monkeypatch):
    req = httpx.Request("GET", "https://nope.example.com/llms.txt")
    _patch_httpx(monkeypatch, {"llms.txt": httpx.Response(404, request=req)})
    res = await code_ingest.llms_txt_fetch({"url": "nope.example.com"}, CTX)
    assert res.success is False
    assert res.error.error_type == "not_found"


# --------------------------------------------------------------------------- #
# package_info                                                                 #
# --------------------------------------------------------------------------- #

async def test_package_info_pypi(monkeypatch):
    payload = {
        "info": {
            "name": "httpx",
            "version": "0.28.1",
            "summary": "The next generation HTTP client.",
            "requires_python": ">=3.8",
            "requires_dist": ["certifi", "httpcore"],
            "home_page": "https://www.python-httpx.org",
            "project_urls": {"Homepage": "https://www.python-httpx.org"},
            "license": "BSD",
            "description": "x" * 5000,
        }
    }
    req = httpx.Request("GET", "https://pypi.org/pypi/httpx/json")
    _patch_httpx(monkeypatch, {"pypi.org": httpx.Response(200, json=payload, request=req)})

    res = await code_ingest.package_info({"name": "httpx", "max_chars": 1000}, CTX)
    assert res.success, res.error
    assert res.output["latest_version"] == "0.28.1"
    assert res.output["ecosystem"] == "pypi"
    assert res.output["dependencies"] == ["certifi", "httpcore"]
    assert res.output["readme_truncated"] is True
    assert len(res.output["readme"]) == 1000


async def test_package_info_npm(monkeypatch):
    payload = {
        "name": "react",
        "description": "React is a JavaScript library...",
        "dist-tags": {"latest": "19.2.0"},
        "versions": {"19.2.0": {"dependencies": {"loose-envify": "^1.1.0"}}},
        "homepage": "https://react.dev/",
        "license": "MIT",
    }
    req = httpx.Request("GET", "https://registry.npmjs.org/react")
    _patch_httpx(monkeypatch, {"registry.npmjs.org": httpx.Response(200, json=payload, request=req)})

    res = await code_ingest.package_info({"name": "react", "ecosystem": "npm"}, CTX)
    assert res.success, res.error
    assert res.output["latest_version"] == "19.2.0"
    assert res.output["dependencies"] == ["loose-envify ^1.1.0"]


async def test_package_info_not_found(monkeypatch):
    req = httpx.Request("GET", "https://pypi.org/pypi/zzz-nope/json")
    _patch_httpx(monkeypatch, {"pypi.org": httpx.Response(404, request=req)})
    res = await code_ingest.package_info({"name": "zzz-nope"}, CTX)
    assert res.success is False
    assert res.error.error_type == "not_found"


# --------------------------------------------------------------------------- #
# arg validation                                                               #
# --------------------------------------------------------------------------- #

async def test_invalid_args_raise_for_executor_to_catch():
    """Out-of-range args raise ValidationError (the executor wraps it), matching
    the web.py convention of parsing args before the try block."""
    with pytest.raises(Exception):
        await code_ingest.package_info({"name": "httpx", "max_chars": 1}, CTX)
