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
import functools
import os
import shutil
import time
from typing import Any

import httpx
from matrx_utils.http_client import shared_client
from matrx_utils.outbound_guard import OutboundUrlRefused

from matrx_ai.tools._sandbox_proxy import get_active_sandbox
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
#: The most file bytes one git_ingest reads. gitingest's own ceiling is 500 MB (and 10,000 files),
#: and it reads, joins and tokenizes ALL of it on the server for an answer capped at ~44k chars:
#: archestra-ai/archestra (370 MB) ran past the 120 s dispatch ceiling twice on 2026-11-08 and
#: left 4 calls unanswered (system_error sec_a5cf6424, sec_c867987b). gitingest takes no per-call
#: total, so its module ceiling is lowered for each call (only this tool uses gitingest).
_GIT_INGEST_MAX_TOTAL_BYTES = 16 * 1024 * 1024


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


def _names_a_repository(source: str) -> bool:
    """A source that names a repository by URL, never a folder (no filesystem lookup)."""
    s = source.strip().lower()
    return s.startswith(
        ("http://", "https://", "git@", "ssh://", "git://", "github.com/", "gitlab.com/")
    )


def _ingest(source: str, **kwargs: Any) -> tuple[str, str, str]:
    """gitingest's ingest, looked up at call time (tests and the optional extra both rely on it)."""
    import gitingest.entrypoint as entry
    import gitingest.ingestion as walk
    import gitingest.utils.query_parser_utils as parse
    from gitingest import ingest

    walk.MAX_TOTAL_SIZE_BYTES = _GIT_INGEST_MAX_TOTAL_BYTES
    entry.resolve_token = _caller_token_only
    parse._validate_host = _validate_any_git_host
    walk._should_exclude = _should_exclude
    walk._should_include = _should_include
    return ingest(source, **kwargs)


#: What git prints when the host wants a login it was not given (prompts are off on the server).
_GIT_CREDENTIALS_NEEDED = (
    "could not read username",
    "could not read password",
    "terminal prompts disabled",
    "authentication failed",
    "repository not found",
    "invalid username or password",
)


def _needs_credentials(exc: BaseException) -> bool:
    """True when a clone/ls-remote failed because the host asked for credentials."""
    text = str(exc).lower()
    return any(marker in text for marker in _GIT_CREDENTIALS_NEEDED)


def _validate_any_git_host(host: str) -> None:
    """gitingest's ``_validate_host`` without its six-host allow-list.

    Upstream refuses every host that is not github/gitlab/bitbucket/gitea/codeberg or a ``git.`` /
    ``gitlab.`` / ``github.`` subdomain, BEFORE asking the host anything: a public gitee.com repo
    failed as ``Unknown domain 'gitee.com' in URL`` (system_error 62740547, 2026-11-13). Whether a
    host serves a repository is the clone's answer (gitingest's ``check_repo_exists`` asks it next),
    so any host name is accepted here; only an empty or dotless one is refused.
    """
    name = host.lower().rsplit("@", 1)[-1].split(":", 1)[0]
    if not name or "." not in name:
        raise ValueError(f"Unknown domain '{host}' in URL")


def _caller_token_only(token: str | None) -> str | None:
    """gitingest's ``resolve_token`` without its ``GITHUB_TOKEN`` environment fallback.

    The tool runs on the SERVER for whoever called it: the token is the caller's ``token`` arg or
    none. Upstream falls back to the server's own ``GITHUB_TOKEN`` when the arg is empty, which
    hands the server's credential to any caller's clone and fails even a local-folder walk when
    that variable is not in GitHub's PAT format.
    """
    from gitingest.utils.git_utils import validate_github_token

    if token:
        validate_github_token(token)
    return token or None


@functools.lru_cache(maxsize=32)
def _compiled_spec(patterns: frozenset[str]) -> Any:
    from pathspec import PathSpec

    return PathSpec.from_lines("gitwildmatch", patterns)


def _should_exclude(path: Any, base_path: Any, ignore_patterns: set[str]) -> bool:
    """gitingest's ``_should_exclude`` with the pattern set compiled ONCE, not once per path.

    gitingest 0.3.1 (the latest) rebuilds its ~260-pattern ignore PathSpec for every file and
    folder it visits: archestra-ai/archestra (11.5k paths) compiled 3M patterns, 68 of its 76 s.
    Same answer, from a cached spec.
    """
    from gitingest.utils.ingestion_utils import _relative_or_none

    rel_path = _relative_or_none(path, base_path)
    if rel_path is None:  # outside the repository: already excluded
        return True
    return _compiled_spec(frozenset(ignore_patterns)).match_file(str(rel_path))


def _should_include(path: Any, base_path: Any, include_patterns: set[str]) -> bool:
    """gitingest's ``_should_include`` with the pattern set compiled once (see ``_should_exclude``)."""
    from gitingest.utils.ingestion_utils import _relative_or_none

    rel_path = _relative_or_none(path, base_path)
    if rel_path is None:  # outside the repository: not included
        return False
    if path.is_dir():  # folders stay, so their files are visited
        return True
    return _compiled_spec(frozenset(include_patterns)).match_file(str(rel_path))


def _reached_read_ceiling(content: str, max_file_size: int) -> bool:
    """True when the walk read up to the byte ceiling, so files past it were skipped.

    gitingest stops adding a file once it would cross the ceiling, so a walk that stopped holds
    more than ``ceiling - max_file_size`` bytes; one that read everything holds less.
    """
    return len(content) > _GIT_INGEST_MAX_TOTAL_BYTES - max_file_size


async def git_ingest(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = GitIngestArgs(**args)
    stream = ToolStreamManager(ctx.emitter, ctx.call_id, "git_ingest")

    # A turn bound to a box (a cloud sandbox or the person's computer): this tool runs on the
    # SERVER, so a local path would name the server's disk, never the box's. A repository URL is
    # fine; a folder on the box is read with the box's own tools.
    if get_active_sandbox() is not None and not _names_a_repository(parsed.source):
        return ToolResult(
            success=False,
            error=ToolError(
                refusal=True,
                error_type="local_path_on_bound_box",
                message=(
                    f"git_ingest runs on the server and cannot see {parsed.source!r} on the attached "
                    "computer or sandbox. It takes a repository URL."
                ),
                suggested_action=(
                    "For a folder on the attached machine use fs_list and fs_search, then fs_read, "
                    "or shell_execute (git ls-files, git log)."
                ),
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="git_ingest",
            call_id=ctx.call_id,
        )

    remote = _looks_remote(parsed.source)
    if remote and shutil.which("git") is None:
        return ToolResult(
            success=False,
            error=ToolError(
                refusal=True,
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
        import gitingest  # noqa: F401 — the optional extra must be installed; _ingest calls it
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
        await stream.progress(f"Ingesting {'remote ' if remote else ''}{parsed.source[:80]}...")
        # Despite its name, gitingest.ingest_async performs its recursive file
        # walk and content assembly synchronously. Running it on the API loop can
        # freeze every request for large repositories, so keep the entire
        # third-party ingestion lifecycle on a worker thread.
        summary, tree, content = await asyncio.to_thread(
            _ingest,
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
        if _reached_read_ceiling(content, parsed.max_file_size):
            ceiling_mb = _GIT_INGEST_MAX_TOTAL_BYTES // (1024 * 1024)
            out["read_ceiling_reached"] = (
                f"The read stopped at its {ceiling_mb} MB ceiling, so files past it are missing from "
                "the summary counts, the tree and the content. Narrow it with include/exclude globs "
                "or a subdirectory URL to see the rest."
            )
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
        if remote and _needs_credentials(exc):
            # The host asked for a login: the repository is private (or absent) and this call
            # carried no token that can read it. The caller's input, answered with the fix —
            # never an operational failure (filed as tool_execution_failed until 2026-11-21,
            # 752f1b71: a private repository read without a token).
            return ToolResult(
                success=False,
                error=ToolError(
                    refusal=True,
                    error_type="auth_required",
                    message=(
                        f"{parsed.source!r} could not be read: the git host asked for a login, so it "
                        "is private or does not exist"
                        + (" and the token passed cannot read it." if parsed.token else ".")
                    ),
                    suggested_action=(
                        "Check the URL. For a private repository pass a `token` that can read it, "
                        "or ask the person for access."
                    ),
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="git_ingest",
                call_id=ctx.call_id,
            )
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
                {
                    "title": m.group(1).strip(),
                    "url": m.group(2).strip(),
                    "notes": m.group(3).strip() or None,
                }
            )

    return {"title": title, "summary": summary, "sections": sections}


async def llms_txt_fetch(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = LlmsTxtFetchArgs(**args)
    stream = ToolStreamManager(ctx.emitter, ctx.call_id, "llms_txt_fetch")
    target = _llms_txt_target(parsed.url, parsed.full)

    # Direct httpx is correct here: llms.txt is a plain-text docs standard at a
    # well-known path the agent named — not a user cloud-file (MediaRef), so it
    # does not go through FileManager.resolve_media_async. The MODEL names the
    # host, so the guarded client refuses any address inside our network (every
    # redirect hop too) and connects to the IP it checked.
    try:
        await stream.progress(f"Fetching {target}")
        async with shared_client(public_only=True, timeout=_HTTP_TIMEOUT, follow_redirects=True) as client:
            resp = await client.get(target, headers={"User-Agent": _USER_AGENT})

        if resp.status_code == 404:
            return ToolResult(
                success=False,
                error=ToolError(
                    refusal=True,
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
            (
                f"Text truncated to {parsed.max_chars} of {total} chars. "
                f"Set `full=false` for the shorter index, or raise max_chars."
            )
            if truncated
            else None
        )
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
    except OutboundUrlRefused as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,
                error_type="not_allowed",
                message=str(exc),
                is_retryable=False,
                suggested_action="Use the public web address of the site's docs.",
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="llms_txt_fetch",
            call_id=ctx.call_id,
        )
    except httpx.HTTPError as exc:
        return ToolResult(
            success=False,
            error=ToolError.declared(exc=exc, 
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


async def _fetch_pypi(
    client: httpx.AsyncClient, name: str, include_readme: bool, max_chars: int
) -> dict[str, Any]:
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


async def _fetch_npm(
    client: httpx.AsyncClient, name: str, include_readme: bool, max_chars: int
) -> dict[str, Any]:
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
        async with shared_client(timeout=_HTTP_TIMEOUT, follow_redirects=True) as client:
            if parsed.ecosystem == "pypi":
                out = await _fetch_pypi(
                    client, parsed.name, parsed.include_readme, parsed.max_chars
                )
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
            error=ToolError.declared(exc=exc, 
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
            error=ToolError.declared(exc=exc, 
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
