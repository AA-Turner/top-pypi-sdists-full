"""The sandbox skill walker reads a SKILL.md through the PAGED fs_read.

Failing-then-passing witness for ops.system_error class
``sandbox_skill_discovery_failed`` ("expected string or bytes-like object,
got 'SandboxReadResult'"): ``fs_read`` started returning one bounded page
(``SandboxReadResult``) and ``walk_via_proxy`` kept treating it as the file
text, so every sandbox skill discovery failed in the parser.
"""

from __future__ import annotations

import asyncio
from typing import Any

from matrx_ai.skills.ingest import walk_via_proxy
from matrx_ai.tools import _sandbox_proxy
from matrx_ai.tools._sandbox_proxy import SandboxBinding, SandboxReadResult

SKILL_MD = """---
name: paged-skill
description: A skill whose SKILL.md arrives in two pages.
---

# Paged skill

Body that is long enough to split.
"""

FLAT_MD = """---
name: flat-skill
description: A flat-layout skill.
---

# Flat skill
"""


def test_walk_via_proxy_reads_whole_file_from_pages(monkeypatch: Any) -> None:
    root = "/home/agent/.claude/skills"
    files = {f"{root}/paged-skill/SKILL.md": SKILL_MD, f"{root}/flat-skill.md": FLAT_MD}

    async def fake_list(_b: Any, path: str, **_kw: Any) -> dict:
        if path != root:
            raise _sandbox_proxy.SandboxProxyError("missing", status=404)
        return {
            "entries": [
                {"name": "paged-skill", "kind": "dir", "path": f"{root}/paged-skill"},
                {"name": "flat-skill.md", "kind": "file", "path": f"{root}/flat-skill.md"},
            ]
        }

    async def fake_read(_b: Any, path: str, *, encoding: str = "utf8", offset: int = 0, limit: int = 40) -> SandboxReadResult:
        text = files[path]
        chunk = text[offset : offset + 40]
        nxt = offset + len(chunk)
        return SandboxReadResult(
            content=chunk, size=len(text), offset=offset, limit=40,
            next_offset=nxt, truncated=nxt < len(text), server_bounded=True,
        )

    monkeypatch.setattr(_sandbox_proxy, "fs_list", fake_list)
    monkeypatch.setattr(_sandbox_proxy, "fs_read", fake_read)

    binding = SandboxBinding(sandbox_id="sbx", base_url="http://x", access_token="t", root_path="/home/agent")
    skills, roots = asyncio.run(walk_via_proxy(binding))

    assert root in roots
    by_id = {s.skill_id: s for s in skills}
    assert set(by_id) == {"paged-skill", "flat-skill"}
