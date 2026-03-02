"""Memory tools: memory_read, memory_write, memory_search, usage_report."""

from pathlib import Path
from salmalm.tools.tool_registry import register
from salmalm.constants import MEMORY_FILE, MEMORY_DIR
from salmalm.core import _tfidf, get_usage_report


def _resolve_memory_path(fname: str) -> Path:
    """Resolve memory file path and guard against path traversal.

    BUG-CT fix: callers pass user/LLM-supplied filenames.
    Without validation, 'fname=../../etc/passwd' would escape MEMORY_DIR.
    """
    if fname == "MEMORY.md":
        return MEMORY_FILE
    # Strip any leading slashes / dots to prevent traversal
    # Use Path.name to allow only bare filenames (no directory components)
    safe_name = Path(fname).name
    if not safe_name or safe_name in (".", ".."):
        raise ValueError(f"Invalid memory filename: {fname!r}")
    p = (MEMORY_DIR / safe_name).resolve()
    # Final check: resolved path must be inside MEMORY_DIR
    try:
        p.relative_to(MEMORY_DIR.resolve())
    except ValueError:
        raise ValueError(f"Path traversal blocked: {fname!r}")
    return p


@register("memory_read")
def handle_memory_read(args: dict) -> str:
    """Handle memory read."""
    fname = args["file"]
    try:
        p = _resolve_memory_path(fname)
    except ValueError as e:
        return f"❌ {e}"
    if not p.exists():
        return f"File not found: {fname}"
    return p.read_text(encoding="utf-8")[:30000]


@register("memory_write")
def handle_memory_write(args: dict) -> str:
    """Handle memory write."""
    fname = args["file"]
    try:
        p = _resolve_memory_path(fname)
    except ValueError as e:
        return f"❌ {e}"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(args["content"], encoding="utf-8")
    return f"{fname} saved"


@register("memory_search")
def handle_memory_search(args: dict) -> str:
    """Handle memory search."""
    query = args["query"]
    max_results = args.get("max_results", 5)
    results = _tfidf.search(query, max_results)
    if not results:
        return f'No results for: "{query}"'
    out = []
    for score, label, lineno, snippet in results:
        out.append(f"{label}#{lineno} (similarity:{score:.3f})\n{snippet}\n")
    return "\n".join(out)


@register("usage_report")
def handle_usage_report(args: dict) -> str:
    """Handle usage report."""
    report = get_usage_report()
    lines = [
        "SalmAlm Usage Report",
        f"Uptime: {report['elapsed_hours']}h",
        f"Input: {report['total_input']:,} tokens",
        f"Output: {report['total_output']:,} tokens",
        f"Total cost: ${report['total_cost']:.4f}",
        "",
    ]
    for m, d in report.get("by_model", {}).items():
        lines.append(f"  {m}: {d['calls']}calls, ${d['cost']:.4f}")
    return "\n".join(lines)
