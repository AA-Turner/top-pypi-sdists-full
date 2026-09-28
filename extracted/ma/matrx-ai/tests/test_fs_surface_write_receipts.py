"""fs_write / fs_edit / fs_patch carry the surface-write receipt and keep the patch contract.

Use case: a small clinic's front desk runs ``intake_checklist.sh`` every morning
and keeps its settings in ``intake.yaml``. The agent edits both. The person must
see WHAT changed (the before → after receipt the chat's diff card renders), and a
patch must name exactly one place or fail loudly — never a silent overwrite and
never a half-applied patch that leaves the checklist script inconsistent.

Checked on all three backends: local disk, the active-sandbox proxy (a fake
daemon standing in for the orchestrator), and the durable VFS (an in-memory
workspace).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from matrx_ai.tools import _sandbox_proxy
from matrx_ai.tools.implementations import filesystem, vfs_filesystem
from matrx_ai.tools.models import ToolContext

CHECKLIST = """#!/usr/bin/env bash
# Morning intake checklist — Riverside Family Clinic
set -euo pipefail

check "Front desk tablet charged"
check "Insurance card scanner online"
check "Consent forms printed: 20"
check "Flu-season screening questions loaded"
"""

CONFIG = """clinic: Riverside Family Clinic
open_at: "08:00"
intake:
  max_walk_ins: 12
  require_photo_id: true
  reminder_minutes: 30
"""


async def _no_emit(**_: Any) -> None:
    return None


# ── backends ─────────────────────────────────────────────────────────────────


class _Local:
    name = "local"

    def __init__(self, root: Path) -> None:
        self.root = root

    def seed(self, path: str, text: str) -> None:
        (self.root / path).write_text(text, encoding="utf-8")

    def seed_bytes(self, path: str, data: bytes) -> None:
        (self.root / path).write_bytes(data)

    def read(self, path: str) -> bytes:
        return (self.root / path).read_bytes()

    def exists(self, path: str) -> bool:
        return (self.root / path).exists()


class _FakeDaemon:
    """In-memory stand-in for the sandbox's matrx_agent /fs endpoints.

    Its /fs/patch deliberately applies PARTIALLY (as the real daemon may), so a
    test can prove the tool never reaches it with an edit that would fail.
    """

    name = "sandbox"

    def __init__(self) -> None:
        self.files: dict[str, str] = {}
        self.patch_calls = 0

    def _key(self, path: str) -> str:
        return path.removeprefix("/home/agent/")

    def seed(self, path: str, text: str) -> None:
        self.files[path] = text

    def read(self, path: str) -> bytes:
        return self.files[path].encode("utf-8")

    def exists(self, path: str) -> bool:
        return path in self.files

    async def fs_read(self, binding, path, *, encoding="utf8", offset=0, limit=1_048_576):
        key = self._key(path)
        if key not in self.files:
            raise _sandbox_proxy.SandboxProxyError("not found", status=404, error_type="not_found")
        text = self.files[key]
        chunk = text[offset : offset + limit]
        nxt = offset + len(chunk)
        return _sandbox_proxy.SandboxReadResult(
            content=chunk,
            size=len(text.encode("utf-8")),
            offset=offset,
            limit=limit,
            next_offset=nxt,
            truncated=nxt < len(text),
            server_bounded=True,
        )

    async def fs_write(self, binding, path, content, *, encoding="utf8", create_parents=True):
        self.files[self._key(path)] = content
        return {"path": path, "size": len(content.encode("utf-8"))}

    async def fs_patch(self, binding, path, edits, *, create_if_missing=False):
        self.patch_calls += 1
        key = self._key(path)
        before = self.files.get(key, "")
        text = before
        applied, failed = [], []
        for i, e in enumerate(edits):
            n = text.count(e["old_text"])
            if n == 0 or (n > 1 and not e["replace_all"]):
                failed.append({"edit_index": i, "reason": "old_text not found", "old_text_preview": ""})
                continue
            text = text.replace(e["old_text"], e["new_text"], -1 if e["replace_all"] else 1)
            applied.append({"edit_index": i, "mode": "replace", "delta_chars": 0})
        self.files[key] = text  # partial apply — the tool must never let this happen
        return {
            "edits_applied": applied,
            "edits_failed": failed,
            "size_before": len(before),
            "size_after": len(text),
        }


class _MemVFS:
    name = "vfs"

    def __init__(self) -> None:
        self.files: dict[str, bytes] = {}

    def seed(self, path: str, text: str) -> None:
        self.files["/" + path] = text.encode("utf-8")

    def seed_bytes(self, path: str, data: bytes) -> None:
        self.files["/" + path] = data

    def read(self, path: str) -> bytes:
        return self.files["/" + path]

    def exists(self, path: str) -> bool:
        return "/" + path in self.files

    async def _cat_file(self, path: str) -> bytes:
        if path not in self.files:
            raise FileNotFoundError(path)
        return self.files[path]

    async def _pipe_file(self, path: str, data: bytes) -> None:
        self.files[path] = data

    async def _makedirs(self, path: str, exist_ok: bool = False) -> None:
        return None


@pytest.fixture(params=["local", "sandbox", "vfs"])
def backend(request, monkeypatch, tmp_path: Path):
    monkeypatch.setattr(filesystem, "emit_fs_changed", _no_emit)
    kind = request.param
    if kind == "local":
        monkeypatch.setattr(filesystem, "_should_use_durable_vfs", lambda: False)
        monkeypatch.setattr(filesystem, "get_active_sandbox", lambda: None)
        monkeypatch.setattr(filesystem, "_resolve_path", lambda rel, ctx: tmp_path / rel)
        return _Local(tmp_path)
    if kind == "sandbox":
        daemon = _FakeDaemon()
        binding = _sandbox_proxy.SandboxBinding(
            sandbox_id="sbx-clinic", base_url="https://orchestrator.test/sandboxes/sbx-clinic",
            access_token="t", root_path="/home/agent",
        )
        monkeypatch.setattr(filesystem, "_should_use_durable_vfs", lambda: False)
        monkeypatch.setattr(filesystem, "get_active_sandbox", lambda: binding)
        monkeypatch.setattr(filesystem, "_proxy_fs_read", daemon.fs_read)
        monkeypatch.setattr(filesystem, "_proxy_fs_write", daemon.fs_write)
        monkeypatch.setattr(filesystem, "_proxy_fs_patch", daemon.fs_patch)
        return daemon
    vfs = _MemVFS()

    async def _get(ctx: Any) -> _MemVFS:
        return vfs

    monkeypatch.setattr(filesystem, "_should_use_durable_vfs", lambda: True)
    monkeypatch.setattr(filesystem, "_refuse_if_their_machine_is_down", lambda name, ctx: None)
    monkeypatch.setattr(vfs_filesystem, "get_workspace_fs", _get)
    return vfs


CTX = ToolContext(call_id="c-clinic", user_id="u-front-desk")


def _receipt(result) -> dict[str, Any]:
    assert result.success, result.error
    assert result.surface_write is not None, "a successful file write must carry its receipt"
    return result.surface_write.model_dump()


# ── receipts ─────────────────────────────────────────────────────────────────


async def test_fs_write_overwrite_receipt_carries_before_and_after(backend) -> None:
    backend.seed("intake.yaml", CONFIG)
    new = CONFIG.replace("max_walk_ins: 12", "max_walk_ins: 15")
    r = await filesystem.fs_write({"path": "intake.yaml", "content": new}, CTX)
    rec = _receipt(r)
    assert rec["before"] == CONFIG
    assert rec["after"] == new
    assert rec["mode"] == "overwrite"
    assert rec["target_type"] == "file"
    assert rec["target_id"].endswith("intake.yaml") and rec["target_label"] == rec["target_id"]
    assert rec["content_format"] == "code" and rec["language"] == "yaml"
    assert backend.read("intake.yaml") == new.encode("utf-8")


async def test_fs_write_to_a_new_file_has_an_empty_before(backend) -> None:
    r = await filesystem.fs_write({"path": "intake_checklist.sh", "content": CHECKLIST}, CTX)
    rec = _receipt(r)
    assert rec["before"] == "" and rec["after"] == CHECKLIST
    assert rec["language"] == "shell"
    # Nothing existed, so nothing was replaced: the card must say "Created"
    # (live 2026-09-26: a new file's card read "Replaced").
    assert rec["mode"] == "create"


async def test_fs_write_append_receipt_shows_the_whole_file(backend) -> None:
    backend.seed("intake_checklist.sh", CHECKLIST)
    line = 'check "Masks restocked at the door"\n'
    r = await filesystem.fs_write(
        {"path": "intake_checklist.sh", "content": line, "append": True}, CTX
    )
    rec = _receipt(r)
    assert rec["mode"] == "append"
    assert rec["before"] == CHECKLIST
    assert rec["after"] == CHECKLIST + line
    assert backend.read("intake_checklist.sh") == (CHECKLIST + line).encode("utf-8")


async def test_markdown_file_is_markdown_not_code(backend) -> None:
    r = await filesystem.fs_write({"path": "README.md", "content": "# Intake\n"}, CTX)
    rec = _receipt(r)
    assert rec["content_format"] == "markdown" and rec["language"] is None


async def test_fs_edit_receipt_is_a_one_edit_patch(backend) -> None:
    backend.seed("intake_checklist.sh", CHECKLIST)
    r = await filesystem.fs_edit(
        {
            "path": "intake_checklist.sh",
            "old_str": "Consent forms printed: 20",
            "new_str": "Consent forms printed: 30",
        },
        CTX,
    )
    rec = _receipt(r)
    assert rec["mode"] == "patch" and rec["edits"] == 1
    assert rec["before"] == CHECKLIST
    assert rec["after"] == CHECKLIST.replace("printed: 20", "printed: 30")
    assert r.output["replaced"] == 1


async def test_fs_patch_receipt_counts_edits(backend) -> None:
    backend.seed("intake.yaml", CONFIG)
    r = await filesystem.fs_patch(
        {
            "path": "intake.yaml",
            "edits": [
                {"old_text": "max_walk_ins: 12", "new_text": "max_walk_ins: 10"},
                {"old_text": "reminder_minutes: 30", "new_text": "reminder_minutes: 45"},
            ],
        },
        CTX,
    )
    rec = _receipt(r)
    assert rec["mode"] == "patch" and rec["edits"] == 2
    assert rec["before"] == CONFIG
    expected = CONFIG.replace("max_walk_ins: 12", "max_walk_ins: 10").replace(
        "reminder_minutes: 30", "reminder_minutes: 45"
    )
    assert rec["after"] == expected
    assert r.output["edits_failed"] == []
    assert backend.read("intake.yaml") == expected.encode("utf-8")


async def test_replace_all_is_an_explicit_opt_in(backend) -> None:
    backend.seed("intake_checklist.sh", CHECKLIST)
    r = await filesystem.fs_edit(
        {"path": "intake_checklist.sh", "old_str": 'check "', "new_str": 'verify "', "replace_all": True},
        CTX,
    )
    rec = _receipt(r)
    assert rec["after"].count('verify "') == 4
    assert r.output["replaced"] == 4


# ── the patch contract ───────────────────────────────────────────────────────


async def test_fs_patch_is_all_or_nothing(backend) -> None:
    backend.seed("intake_checklist.sh", CHECKLIST)
    original = backend.read("intake_checklist.sh")
    r = await filesystem.fs_patch(
        {
            "path": "intake_checklist.sh",
            "edits": [
                {"old_text": "Consent forms printed: 20", "new_text": "Consent forms printed: 25"},
                {"old_text": "COVID screening questions loaded", "new_text": "x"},  # not in file
                {"old_text": 'check "', "new_text": 'verify "'},  # 4 places, no replace_all
            ],
        },
        CTX,
    )
    assert r.success is False
    assert r.surface_write is None
    assert r.error.error_type == "patch_no_match"  # the first failing edit's type
    assert "edit 1" in r.error.message and "edit 2" in r.error.message
    assert "NOTHING" in r.error.message
    assert r.error.suggested_action
    assert [f["edit_index"] for f in r.output["failures"]] == [1, 2]
    assert [f["error_type"] for f in r.output["failures"]] == ["patch_no_match", "patch_ambiguous"]
    # Byte-identical: the good first edit was NOT applied either.
    assert backend.read("intake_checklist.sh") == original
    if isinstance(backend, _FakeDaemon):
        assert backend.patch_calls == 0, "a failing patch must never reach the daemon"


async def test_fs_edit_no_match(backend) -> None:
    backend.seed("intake.yaml", CONFIG)
    r = await filesystem.fs_edit(
        {"path": "intake.yaml", "old_str": "max_walk_ins: 99", "new_str": "max_walk_ins: 5"}, CTX
    )
    assert r.success is False and r.surface_write is None
    assert r.error.error_type == "patch_no_match"
    assert "fs_read" in r.error.suggested_action
    assert backend.read("intake.yaml") == CONFIG.encode("utf-8")


async def test_fs_edit_ambiguous_names_count_and_lines(backend) -> None:
    backend.seed("intake_checklist.sh", CHECKLIST)
    r = await filesystem.fs_edit(
        {"path": "intake_checklist.sh", "old_str": 'check "', "new_str": 'verify "'}, CTX
    )
    assert r.success is False
    assert r.error.error_type == "patch_ambiguous"
    assert "4 places" in r.error.message
    assert "lines 5, 6, 7, 8" in r.error.message
    assert "replace_all=true" in r.error.suggested_action
    assert backend.read("intake_checklist.sh") == CHECKLIST.encode("utf-8")


async def test_fs_patch_ambiguous_alone_is_patch_ambiguous(backend) -> None:
    backend.seed("intake_checklist.sh", CHECKLIST)
    r = await filesystem.fs_patch(
        {"path": "intake_checklist.sh", "edits": [{"old_text": 'check "', "new_text": "x"}]}, CTX
    )
    assert r.error.error_type == "patch_ambiguous"
    assert r.output["failures"][0]["match_count"] == 4
    assert r.output["failures"][0]["match_lines"] == [5, 6, 7, 8]


# ── binary / undecodable: skip the receipt, never fail the write ─────────────


@pytest.mark.parametrize("which", ["local", "vfs"])
async def test_binary_prior_skips_the_receipt_but_writes(which, monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(filesystem, "emit_fs_changed", _no_emit)
    if which == "local":
        be: Any = _Local(tmp_path)
        monkeypatch.setattr(filesystem, "_should_use_durable_vfs", lambda: False)
        monkeypatch.setattr(filesystem, "get_active_sandbox", lambda: None)
        monkeypatch.setattr(filesystem, "_resolve_path", lambda rel, ctx: tmp_path / rel)
    else:
        be = _MemVFS()

        async def _get(ctx: Any) -> _MemVFS:
            return be

        monkeypatch.setattr(filesystem, "_should_use_durable_vfs", lambda: True)
        monkeypatch.setattr(filesystem, "_refuse_if_their_machine_is_down", lambda name, ctx: None)
        monkeypatch.setattr(vfs_filesystem, "get_workspace_fs", _get)
    be.seed_bytes("badge.png", b"\x89PNG\r\n\x1a\n\xff\xfe\x00")
    r = await filesystem.fs_write({"path": "badge.png", "content": "replaced"}, CTX)
    assert r.success, r.error
    assert r.surface_write is None
    assert be.read("badge.png") == b"replaced"


async def test_sandbox_unreadable_prior_skips_the_receipt_but_writes(monkeypatch) -> None:
    daemon = _FakeDaemon()
    binding = _sandbox_proxy.SandboxBinding(
        sandbox_id="sbx", base_url="https://o.test/sandboxes/sbx", access_token="t"
    )

    async def _read_fails(*a: Any, **k: Any):
        raise _sandbox_proxy.SandboxProxyError("boom", status=500)

    monkeypatch.setattr(filesystem, "emit_fs_changed", _no_emit)
    monkeypatch.setattr(filesystem, "_should_use_durable_vfs", lambda: False)
    monkeypatch.setattr(filesystem, "get_active_sandbox", lambda: binding)
    monkeypatch.setattr(filesystem, "_proxy_fs_read", _read_fails)
    monkeypatch.setattr(filesystem, "_proxy_fs_write", daemon.fs_write)
    r = await filesystem.fs_write({"path": "intake.yaml", "content": CONFIG}, CTX)
    assert r.success and r.surface_write is None
    assert daemon.files["intake.yaml"] == CONFIG


def test_receipt_is_out_of_band() -> None:
    """The receipt never reaches the model: ToolResult excludes it from every dump."""
    from matrx_ai.tools.models import ToolResult

    r = filesystem.with_file_surface_write(
        ToolResult(success=True, output={"path": "intake.yaml"}, tool_name="fs_write", call_id="c"),
        path="intake.yaml",
        before=CONFIG,
        after=CONFIG + "#\n",
        mode="overwrite",
    )
    assert r.surface_write is not None
    assert "surface_write" not in r.model_dump()
