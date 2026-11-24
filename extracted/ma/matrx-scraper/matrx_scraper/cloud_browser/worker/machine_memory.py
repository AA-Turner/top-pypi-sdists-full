"""The person's memory on a Cloud Computer: a READ-ONLY rendering of the platform's memory.

The memory's one home is the platform database (``users.user_memory``); AI Dream decides whose rows a
machine may hold and pushes them here (``POST /machine/memory``). This module only writes what it is
given:

* every file under ``~/.matrx/memory/<path>`` (0444, directories 0555), swapped in whole so a row
  that is gone is a file that is gone, and a path can never leave that root;
* ``~/.matrx/MEMORY.md`` — the server's one rendering (index + text), written even when the set is
  empty so an agent reads why there is none;
* a marked import block in ``~/.claude/CLAUDE.md`` so Claude Code in the terminal reads the
  rendering; added once, the person's own lines never touched.

Nothing here writes back: a change to memory goes through AI Matrx (the memory steward).
"""

from __future__ import annotations

import os
import shutil
import time
from collections.abc import Callable
from pathlib import Path, PurePosixPath
from typing import Any

from fastapi import HTTPException, Request

MEMORY_DIR = ".matrx/memory"
RENDERING_FILE = ".matrx/MEMORY.md"
CLAUDE_FILE = ".claude/CLAUDE.md"
IMPORT_LINE = "@~/.matrx/MEMORY.md"
BLOCK_START = "<!-- matrx:person-memory (added by AI Matrx: your memory, read-only) -->"
BLOCK_END = "<!-- /matrx:person-memory -->"
#: Bounds one push (the server sends far fewer; a runaway body is refused, not half-written).
MAX_FILES = 2000
MAX_FILE_CHARS = 200_000


def clean_path(raw: Any) -> str | None:
    """A memory row's path as a relative path under the memory root, or None when it cannot be one.
    Live rows hold bare paths (``probe.md``); the Memory Lab's store form is ``/memories/probe.md``."""
    if not isinstance(raw, str):
        return None
    text = raw.strip().replace("\\", "/").lstrip("/")
    if text.startswith("memories/"):
        text = text[len("memories/"):]
    parts = [p for p in PurePosixPath(text).parts if p not in ("", ".")]
    if not parts or any(p == ".." for p in parts):
        return None
    return "/".join(parts)


def _make_writable(root: Path) -> None:
    for dirpath, dirnames, _ in os.walk(root):
        os.chmod(dirpath, 0o755)
        for d in dirnames:
            os.chmod(os.path.join(dirpath, d), 0o755)


def _remove_tree(root: Path) -> None:
    if root.exists():
        _make_writable(root)
        shutil.rmtree(root, ignore_errors=True)


def _write_read_only(path: Path, text: str) -> None:
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    tmp.write_text(text, encoding="utf-8")
    os.chmod(tmp, 0o444)
    os.replace(tmp, path)


def _ensure_claude_import(home: Path) -> bool:
    """Add the marked import block to ``~/.claude/CLAUDE.md`` once. True when it was added."""
    path = home / CLAUDE_FILE
    try:
        current = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        current = ""
    if BLOCK_START in current or IMPORT_LINE in current:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    block = f"{BLOCK_START}\n{IMPORT_LINE}\n{BLOCK_END}\n"
    if current:
        block = ("" if current.endswith("\n") else "\n") + "\n" + block
    path.write_text(current + block, encoding="utf-8")
    return True


def apply_memory(home: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Replace the machine's memory rendering with ``payload`` (``files``, ``rendering``, ``source``)."""
    files = payload.get("files")
    if not isinstance(files, list) or len(files) > MAX_FILES:
        raise ValueError(f"files must be a list of at most {MAX_FILES} {{path, content}}")
    rendering = payload.get("rendering")
    if not isinstance(rendering, str):
        raise ValueError("rendering must be text")
    base = Path(home)
    matrx = base / ".matrx"
    matrx.mkdir(parents=True, exist_ok=True)
    stage = matrx / f".memory-new-{os.getpid()}-{time.monotonic_ns()}"
    _remove_tree(stage)
    stage.mkdir()
    written: list[str] = []
    skipped: list[str] = []
    for item in files:
        raw = item.get("path") if isinstance(item, dict) else None
        rel = clean_path(raw)
        content = item.get("content") if isinstance(item, dict) else None
        if rel is None or not isinstance(content, str) or len(content) > MAX_FILE_CHARS:
            skipped.append(str(raw))
            continue
        target = stage / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        written.append(rel)
    for dirpath, dirnames, filenames in os.walk(stage, topdown=False):
        for f in filenames:
            os.chmod(os.path.join(dirpath, f), 0o444)
        for d in dirnames:
            os.chmod(os.path.join(dirpath, d), 0o555)
    live = base / MEMORY_DIR
    old = matrx / f".memory-old-{os.getpid()}-{time.monotonic_ns()}"
    if live.exists():
        _make_writable(live)
        os.replace(live, old)
    os.replace(stage, live)
    os.chmod(live, 0o555)
    _remove_tree(old)
    _write_read_only(base / RENDERING_FILE, rendering)
    import_added = _ensure_claude_import(base)
    return {
        "source": str(payload.get("source") or ""),
        "files": len(written),
        "paths": sorted(written),
        "skipped": skipped,
        "rendering_chars": len(rendering),
        "claude_import_added": import_added,
    }


def install_memory_route(app: Any, *, home: str, verify: Callable[[str], None]) -> None:
    """``POST /machine/memory`` — AI Dream's push (the machine agent token; ``verify`` raises on a bad one)."""
    @app.post("/machine/memory")
    async def machine_memory(request: Request) -> dict[str, object]:
        try:
            verify(request.headers.get("x-sandbox-access-token", ""))
        except Exception as exc:  # noqa: BLE001 - any refusal is a 401
            raise HTTPException(status_code=401, detail=str(getattr(exc, "code", "") or "unauthorized")) from exc
        try:
            payload = await request.json()
        except ValueError as exc:
            raise HTTPException(status_code=422, detail="body must be JSON") from exc
        if not isinstance(payload, dict):
            raise HTTPException(status_code=422, detail="body must be an object")
        try:
            import asyncio

            return await asyncio.to_thread(apply_memory, home, payload)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc


__all__ = ["apply_memory", "clean_path", "install_memory_route"]
