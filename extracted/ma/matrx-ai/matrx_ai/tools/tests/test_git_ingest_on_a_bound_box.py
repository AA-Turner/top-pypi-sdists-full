"""git_ingest never reads the server's disk for a turn bound to a box (a cloud sandbox or the
person's computer). It runs on the server; a repository URL is fine there, but a local path names a
folder on the BOX, which the server cannot see. Until 2026-10-02 such a path was read from the
server's own filesystem and the agent was handed someone else's files, or an error that looked like
the person's folder was empty.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.tools.implementations import code_ingest
from matrx_ai.tools.models import ToolContext

pytestmark = pytest.mark.asyncio
CTX = ToolContext(call_id="t", tool_name="git_ingest")


@pytest.mark.parametrize("target_kind", ["local_machine", "sandbox"])
@pytest.mark.parametrize("source", ["/Users/pat/code/site", "src/app", ".", "C:/Users/pat/site"])
async def test_a_local_path_on_a_bound_box_is_refused_with_the_box_tools(
    monkeypatch: pytest.MonkeyPatch, target_kind: str, source: str
) -> None:
    monkeypatch.setattr(
        code_ingest, "get_active_sandbox", lambda: SimpleNamespace(target_kind=target_kind)
    )

    def must_not_ingest(*_a: object, **_k: object) -> None:
        raise AssertionError("ingested the server's filesystem")

    monkeypatch.setattr(code_ingest, "_ingest", must_not_ingest)
    r = await code_ingest.git_ingest({"source": source}, CTX)
    assert r.success is False and r.error is not None
    assert r.error.error_type == "local_path_on_bound_box"
    assert "fs_list" in (r.error.suggested_action or "")


@pytest.mark.parametrize(
    "source", ["https://github.com/org/repo", "git@github.com:org/repo.git", "github.com/org/repo"]
)
async def test_a_repository_url_on_a_bound_box_still_ingests_on_the_server(
    monkeypatch: pytest.MonkeyPatch, source: str
) -> None:
    monkeypatch.setattr(
        code_ingest, "get_active_sandbox", lambda: SimpleNamespace(target_kind="local_machine")
    )
    seen: list[str] = []
    monkeypatch.setattr(
        code_ingest, "_ingest", lambda src, **_k: (seen.append(src), ("s", "t", "c"))[1]
    )
    monkeypatch.setattr(code_ingest.shutil, "which", lambda _n: "/usr/bin/git")
    r = await code_ingest.git_ingest({"source": source}, CTX)
    assert r.success is True, r.error
    assert seen == [source]
