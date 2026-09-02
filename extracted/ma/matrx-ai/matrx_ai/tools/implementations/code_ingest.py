"""Code & docs ingestion tools for coding agents (the ``code_ingest`` bundle).

Pull external code and library knowledge into context, size-capped:

  - ``git_ingest``     — a repo / subdir / gist / local path → summary + tree + content
  - ``llms_txt_fetch`` — a docs site's ``llms.txt`` / ``llms-full.txt`` (LLM-docs standard)
  - ``package_info``   — PyPI / npm registry metadata + README for a named library

All three are server-side matrx_ai tools. ``git_ingest`` depends on the optional
``gitingest`` package (install ``matrx-ai[code-ingest]``) and is imported lazily so
the module loads fine when it's absent. The other two use ``httpx`` (a core dep).
"""
from __future__ import annotations

import asyncio
import os
import shutil
import time
from typing import Any

import httpx

from matrx_ai.tools.arg_models.code_ingest_args import (
    GitIngestArgs,
    LlmsTxtFetchArgs,
    PackageInfoArgs,
)
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult
from matrx_ai.tools.output_caps import cap_text
from matrx_ai.tools.streaming import ToolStreamManager

# gitingest logs each ingestion step at INFO via loguru. Silence its logger so
# tool calls don't spam stdout/stderr; our own progress goes through the emitter.
try:  # pragma: no cover - best effort
    from loguru import logger as _loguru_logger

    _loguru_logger.disable("gitingest")
except Exception:
    pass

_HTTP_TIMEOUT = 30.0
_USER_AGENT = "matrx-ai-code-ingest/1.0 (+https://aimatrx.com)"
_GIT_INGEST_SOURCE_CHARS = 2_000
_GIT_INGEST_SUMMARY_CHARS = 4_000
_GIT_INGEST_TREE_CHARS = 12_000
_GIT_INGEST_CONTENT_CHARS = 28_000


def _looks_remote(source: str) -> bool:
    """True when the source must be cloned (needs the git CLI)."""
    if os.path.exists(os.path.expanduser(source)):
        return False
    s = source.strip().lower()
    return (
        s.startswith(("http://", "https://", "git@", "ssh://", "git://"))
        or s.startswith("github.com/")
        or s.startswith("gitlab.com/")
        or "/" in s  # owner/repo shorthand — gitingest resolves it remotely
    )


async def git_ingest(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = GitIngestArgs(**args)
    stream = ToolStreamManager(ctx.emitter, ctx.call_id, "git_ingest")

    remote = _looks_remote(parsed.source)
    if remote and shutil.which("git") is None:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="unavailable",
                message=(
                    "The `git` CLI is required to ingest a remote repository and was "
                    "not found on PATH. Local filesystem paths do not need git."
                ),
                suggested_action="Install git, or pass a local path instead of a URL.",
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="git_ingest",
            call_id=ctx.call_id,
        )

    try:
        from gitingest import ingest
    except ImportError as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,
                error_type="unavailable",
                message=f"gitingest is not installed: {exc}",
                suggested_action="Install with: pip install 'matrx-ai[code-ingest]'",
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="git_ingest",
            call_id=ctx.call_id,
        )

    try:
        await stream.progress(
            f"Ingesting {'remote ' if remote else ''}{parsed.source[:80]}..."
        )
        # Despite its name, gitingest.ingest_async performs its recursive file
        # walk and content assembly synchronously. Running it on the API loop can
        # freeze every request for large repositories, so keep the entire
        # third-party ingestion lifecycle on a worker thread.
        summary, tree, content = await asyncio.to_thread(
            ingest,
            parsed.source,
            max_file_size=parsed.max_file_size,
            include_patterns=set(parsed.include) if parsed.include else None,
            exclude_patterns=set(parsed.exclude) if parsed.exclude else None,
            branch=parsed.branch,
            include_submodules=parsed.include_submodules,
            token=parsed.token,
        )

        source, source_cap = cap_text(parsed.source, limit=_GIT_INGEST_SOURCE_CHARS)
        summary, summary_cap = cap_text(summary, limit=_GIT_INGEST_SUMMARY_CHARS)
        out: dict[str, Any] = {
            "source": source,
            "source_chars": source_cap.model_dump(),
            "mode": parsed.mode,
            "summary": summary,
            "summary_chars": summary_cap.model_dump(),
        }
        if parsed.mode in ("tree", "digest"):
            bounded_tree, tree_cap = cap_text(tree, limit=_GIT_INGEST_TREE_CHARS)
            out["tree"] = bounded_tree
            out["tree_chars"] = tree_cap.model_dump()
        if parsed.mode == "digest":
            total = len(content)
            content_limit = min(parsed.max_chars, _GIT_INGEST_CONTENT_CHARS)
            bounded_content, content_cap = cap_text(content, limit=content_limit)
            out["content"] = bounded_content
            out["content_chars_returned"] = content_cap.shown_chars
            out["content_total_chars"] = total
            out["truncated"] = content_cap.truncated
            if content_cap.truncated:
                out["note"] = (
                    f"Content truncated to {content_cap.shown_chars} of {total} chars. "
                    "Call git_ingest again with narrower include/exclude globs, lower "
                    "max_file_size, or use mode='tree' to choose a smaller subtree."
                )

        await stream.progress("Ingestion complete")
        return ToolResult(
            success=True,
            output=out,
            started_at=started_at,
            completed_at=time.time(),
            tool_name="git_ingest",
            call_id=ctx.call_id,
            output_self_capped=True,
        )
    except Exception as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,
                error_type="execution",
                message=f"git_ingest failed: {exc}",
                is_retryable=remote,
                suggested_action=(
                    "Check the source is a valid repo/path you can access. For private "
                    "remotes pass `token`. For a specific branch pass `branch`."
                ),
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="git_ingest",
            call_id=ctx.call_id,
        )


def _llms_txt_target(url: str, full: bool) -> str:
    raw = url.strip()
    filename = "llms-full.txt" if full else "llms.txt"
    if raw.startswith(("http://", "https://")):
        if raw.lower().endswith(".txt"):
            return raw
        return f"{raw.rstrip('/')}/{filename}"
    return f"https://{raw.rstrip('/')}/{filename}"


def _parse_llms_txt(text: str) -> dict[str, Any]:
    """Light parse of the llms.txt structure: H1 title, optional blockquote
    summary, and ``## Section`` blocks each with a list of markdown links."""
    import re

    title: str | None = None
    summary: str | None = None
    sections: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    link_re = re.compile(r"^\s*[-*]\s*\[([^\]]+)\]\(([^)]+)\)\s*:?\s*(.*)$")

    for line in text.splitlines():
        if title is None and line.startswith("# "):
            title = line[2:].strip()
            continue
        if summary is None and line.startswith("> "):
            summary = line[2:].strip()
            continue
        if line.startswith("## "):
            current = {"name": line[3:].strip(), "links": []}
            sections.append(current)
            continue
        m = link_re.match(line)
        if m and current is not None:
            current["links"].append(
                {"title": m.group(1).strip(), "url": m.group(2).strip(), "notes": m.group(3).strip() or None}
            )

    return {"title": title, "summary": summary, "sections": sections}


async def llms_txt_fetch(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = LlmsTxtFetchArgs(**args)
    stream = ToolStreamManager(ctx.emitter, ctx.call_id, "llms_txt_fetch")
    target = _llms_txt_target(parsed.url, parsed.full)

    # Direct httpx is correct here: llms.txt is a plain-text docs standard at a
    # well-known path the agent named — not a user cloud-file (MediaRef), so it
    # does not go through FileManager.resolve_media_async.
    try:
        await stream.progress(f"Fetching {target}")
        async with httpx.AsyncClient(timeout=_HTTP_TIMEOUT, follow_redirects=True) as client:
            resp = await client.get(target, headers={"User-Agent": _USER_AGENT})

        if resp.status_code == 404:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="not_found",
                    message=f"No LLM-docs file at {target} (HTTP 404).",
                    suggested_action=(
                        "This site may not publish llms.txt. Try `full=false`/`true`, a "
                        "different host, or read the docs page directly with web_read."
                    ),
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="llms_txt_fetch",
                call_id=ctx.call_id,
            )
        resp.raise_for_status()

        from matrx_ai.tools.kinds.code_docs import LlmsTxtDocument

        text = resp.text
        total = len(text)
        truncated = total > parsed.max_chars
        body = text[: parsed.max_chars] if truncated else text
        note = (
            f"Text truncated to {parsed.max_chars} of {total} chars. "
            f"Set `full=false` for the shorter index, or raise max_chars."
        ) if truncated else None
        return ToolResult(
            success=True,
            output=LlmsTxtDocument(
                url=target,
                content=body,
                chars_returned=len(body),
                total_chars=total,
                truncated=truncated,
                note=note,
                parsed=_parse_llms_txt(body),
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="llms_txt_fetch",
            call_id=ctx.call_id,
        )
    except httpx.HTTPError as exc:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution",
                message=f"llms_txt_fetch failed: {exc}",
                is_retryable=True,
                suggested_action="Verify the host is reachable and serves an llms.txt file.",
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="llms_txt_fetch",
            call_id=ctx.call_id,
        )


async def _fetch_pypi(client: httpx.AsyncClient, name: str, include_readme: bool, max_chars: int) -> dict[str, Any]:
    resp = await client.get(
        f"https://pypi.org/pypi/{name}/json", headers={"User-Agent": _USER_AGENT}
    )
    resp.raise_for_status()
    info = resp.json().get("info", {})
    readme = (info.get("description") or "") if include_readme else ""
    readme_truncated = len(readme) > max_chars
    out: dict[str, Any] = {
        "name": info.get("name") or name,
        "ecosystem": "pypi",
        "latest_version": info.get("version"),
        "summary": info.get("summary"),
        "requires_python": info.get("requires_python"),
        "dependencies": info.get("requires_dist") or [],
        "homepage": info.get("home_page") or (info.get("project_urls") or {}).get("Homepage"),
        "project_urls": info.get("project_urls") or {},
        "license": info.get("license"),
    }
    if include_readme:
        out["readme"] = readme[:max_chars] if readme_truncated else readme
        out["readme_truncated"] = readme_truncated
    return out


async def _fetch_npm(client: httpx.AsyncClient, name: str, include_readme: bool, max_chars: int) -> dict[str, Any]:
    resp = await client.get(
        f"https://registry.npmjs.org/{name}", headers={"User-Agent": _USER_AGENT}
    )
    resp.raise_for_status()
    data = resp.json()
    latest = (data.get("dist-tags") or {}).get("latest")
    version_obj = (data.get("versions") or {}).get(latest, {}) if latest else {}
    deps = version_obj.get("dependencies") or {}
    readme = (data.get("readme") or "") if include_readme else ""
    readme_truncated = len(readme) > max_chars
    out: dict[str, Any] = {
        "name": data.get("name") or name,
        "ecosystem": "npm",
        "latest_version": latest,
        "summary": data.get("description"),
        "engines": version_obj.get("engines") or {},
        "dependencies": [f"{k} {v}" for k, v in deps.items()],
        "homepage": data.get("homepage"),
        "license": data.get("license"),
    }
    if include_readme:
        out["readme"] = readme[:max_chars] if readme_truncated else readme
        out["readme_truncated"] = readme_truncated
    return out


async def package_info(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = PackageInfoArgs(**args)
    stream = ToolStreamManager(ctx.emitter, ctx.call_id, "package_info")

    try:
        await stream.progress(f"Looking up {parsed.ecosystem}:{parsed.name}")
        async with httpx.AsyncClient(timeout=_HTTP_TIMEOUT, follow_redirects=True) as client:
            if parsed.ecosystem == "pypi":
                out = await _fetch_pypi(client, parsed.name, parsed.include_readme, parsed.max_chars)
            else:
                out = await _fetch_npm(client, parsed.name, parsed.include_readme, parsed.max_chars)

        return ToolResult(
            success=True,
            output=out,
            started_at=started_at,
            completed_at=time.time(),
            tool_name="package_info",
            call_id=ctx.call_id,
        )
    except httpx.HTTPStatusError as exc:
        not_found = exc.response is not None and exc.response.status_code == 404
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="not_found" if not_found else "execution",
                message=(
                    f"No {parsed.ecosystem} package named '{parsed.name}'."
                    if not_found
                    else f"package_info failed: {exc}"
                ),
                is_retryable=not not_found,
                suggested_action=(
                    "Check the package name and ecosystem (pypi vs npm)."
                    if not_found
                    else "Retry; the registry may be temporarily unavailable."
                ),
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="package_info",
            call_id=ctx.call_id,
        )
    except httpx.HTTPError as exc:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution",
                message=f"package_info failed: {exc}",
                is_retryable=True,
                suggested_action="Retry; the registry may be temporarily unavailable.",
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="package_info",
            call_id=ctx.call_id,
        )
