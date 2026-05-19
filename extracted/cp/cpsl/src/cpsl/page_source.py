from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from aiohttp import web

SOURCE_EXTENSIONS = (".tsx", ".ts", ".jsx", ".js")
IGNORED_DIRS = {"node_modules", ".git", "__pycache__"}
SOURCE_HEADERS = {
    "Content-Type": "text/plain; charset=utf-8",
    "Cache-Control": "no-cache",
}


def component_root(component_path: str) -> Path:
    return (Path.cwd() / component_path).resolve().parent


def component_entry(component_path: str) -> Path:
    return (Path.cwd() / component_path).resolve()


def safe_component_path(component_path: str) -> str | None:
    if not component_path:
        return None
    entry = component_entry(component_path)
    cwd = Path.cwd().resolve()
    if not is_within(entry, cwd):
        return None
    if entry.suffix not in SOURCE_EXTENSIONS or not entry.is_file():
        return None
    if any(part in IGNORED_DIRS for part in entry.relative_to(cwd).parts):
        return None
    return entry.relative_to(cwd).as_posix()


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def module_candidates(requested: Path) -> list[Path]:
    if requested.suffix:
        return [requested]
    return [
        *(requested.with_suffix(ext) for ext in SOURCE_EXTENSIONS),
        *(requested / f"index{ext}" for ext in SOURCE_EXTENSIONS),
    ]


def resolve_page_module(component_path: str, relative_path: str) -> Path | None:
    root = component_root(component_path)
    requested = (root / relative_path).resolve()
    if not is_within(requested, root):
        return None

    for candidate in module_candidates(requested):
        if candidate.suffix in SOURCE_EXTENSIONS and candidate.is_file():
            return candidate
    return None


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def build_source_manifest(component_path: str) -> dict[str, Any] | None:
    root = component_root(component_path)
    entry = component_entry(component_path)
    if not entry.is_file() or not is_within(entry, root):
        return None

    modules: dict[str, str] = {"": read_text(entry)}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in IGNORED_DIRS]
        base = Path(dirpath)
        for filename in filenames:
            path = base / filename
            if path.suffix not in SOURCE_EXTENSIONS or path.resolve() == entry:
                continue
            rel = path.relative_to(root).as_posix()
            try:
                modules[rel] = read_text(path)
            except OSError:
                continue
    return {"modules": modules}


def page_source_handler(component_path: str):
    async def handler(_request: web.Request) -> web.StreamResponse:
        entry = component_entry(component_path)
        if not entry.is_file():
            return web.json_response({"error": "not found"}, status=404)
        return web.FileResponse(entry, headers=SOURCE_HEADERS)

    return handler


def page_module_source_handler(component_path: str):
    async def handler(request: web.Request) -> web.StreamResponse:
        rel_path = request.match_info.get("relative_path", "")
        path = resolve_page_module(component_path, rel_path)
        if not path:
            return web.json_response({"error": "not found"}, status=404)
        return web.FileResponse(path, headers=SOURCE_HEADERS)

    return handler


def page_source_manifest_handler(component_path: str):
    async def handler(_request: web.Request) -> web.Response:
        manifest = build_source_manifest(component_path)
        if manifest is None:
            return web.json_response({"error": "not found"}, status=404)
        return web.json_response(manifest)

    return handler
