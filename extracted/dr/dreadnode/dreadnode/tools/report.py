import re
import typing as t
from pathlib import Path

from loguru import logger

from dreadnode.agents.tools import tool
from dreadnode.storage.storage import write_timestamped


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower())
    slug = slug.strip("._-")
    return slug or "report"


def _resolve_filename(
    *,
    title: str | None,
    filename: str | None,
    format: t.Literal["markdown", "text"],
) -> str:
    candidate = Path(filename).name if filename else _slugify(title or "report")
    if not Path(candidate).suffix:
        suffix = ".md" if format == "markdown" else ".txt"
        candidate = f"{candidate}{suffix}"
    return candidate


@tool(name="report")
def report(
    content: t.Annotated[
        str | None,
        (
            "Full markdown or plain-text body of the deliverable. Pass the complete "
            "report text — not a summary, not a sentence like 'saved to foo.md'. The "
            "caller only sees what this tool persists. If the report already exists "
            "on disk, use `source_path` instead of retyping it."
        ),
    ] = None,
    *,
    source_path: t.Annotated[
        str | None,
        (
            "Path to an existing file whose contents should be persisted as the "
            "report. Use this instead of `content` when you have already written "
            "the full report to disk. Relative paths resolve against the runtime "
            "working directory. Mutually exclusive with `content`."
        ),
    ] = None,
    title: t.Annotated[
        str | None,
        "Optional human-readable title used for logging and default filename generation.",
    ] = None,
    filename: t.Annotated[
        str | None,
        "Optional filename for the report artifact. Path components are ignored.",
    ] = None,
    format: t.Annotated[
        t.Literal["markdown", "text"],
        "Output format hint for the saved report artifact.",
    ] = "markdown",
) -> str:
    """
    Persist a named report artifact for the current run or session.

    Use this for deliverables the user should be able to retrieve later —
    findings reports, migration summaries, plans, investigation writeups.
    The full body is persisted as an artifact on the current Dreadnode
    run and written under the user's Dreadnode cache (``~/.dreadnode/reports/``
    by default).

    Provide the body one of two ways:
    - `content=` — the full text of the report
    - `source_path=` — a path to a file you have already written

    Do not use this tool to point at a file (e.g. content="saved report
    to findings.md"). The caller sees only what this tool persists, so a
    pointer string means the report is effectively lost. Pass the real
    body, or use `source_path` to persist an existing file.
    """
    from dreadnode import _get_default_instance, log_output
    from dreadnode.core.types import Markdown, Text

    if (content is None) == (source_path is None):
        raise ValueError(
            "Provide exactly one of `content` (the full report body) or "
            "`source_path` (a file to persist as the report).",
        )

    default_name_hint: str | None = None
    if source_path is not None:
        source = Path(source_path)
        if not source.is_absolute():
            source = (Path.cwd() / source).resolve()
        if not source.is_file():
            raise ValueError(
                f"source_path does not point to a readable file: {source_path}",
            )
        body_text = source.read_text(encoding="utf-8")
        default_name_hint = source.name
    else:
        body_text = t.cast("str", content)

    if not body_text.strip():
        raise ValueError("Report content must not be empty.")

    instance = _get_default_instance()

    effective_filename = filename
    if effective_filename is None and title is None:
        effective_filename = default_name_hint

    resolved_name = _resolve_filename(
        title=title,
        filename=effective_filename,
        format=format,
    )
    path = write_timestamped(instance.storage.reports_path, resolved_name, body_text)

    # Span attribute is cache-relative so we don't ship absolute filesystem paths
    # (which would leak the user's home dir, hostname, or custom cache override)
    # to the platform on every report. The agent-facing return uses the absolute
    # path so it can read the file back if needed.
    relative_path = path.relative_to(instance.cache)
    renderable = Markdown(body_text) if format == "markdown" else Text(body_text, format="text")
    log_output(
        "report",
        renderable,
        label=title or path.name,
        attributes={"path": str(relative_path), "format": format},
    )
    logger.info("Saved report artifact to {}", path)
    return f"Saved {format} report to {path}"
