"""Deterministic T1 manifest + budget-bounded pr-context skeleton (v2 PR review).

This module builds two artifacts from the already-generated PR details:

* ``manifest.json`` — the **full**, machine-readable, orchestrator-only manifest:
  one row per file (path, fileKey, change type, diffstat, purpose hint, risk flag,
  reviewMode, reviewDepth placeholder, prompt-file link) plus a deterministic
  cross-file **cluster** map.
* ``pr-context.md`` — a **budget-bounded** human/agent skeleton rendered from the
  manifest, which degrades deterministically when it exceeds the character budget
  (collapse light/low-risk rows → shorten hints → links-only → hard truncate),
  following the :mod:`agentic_devtools.context_budget` precedent.

Everything here is deterministic — no LLM calls, no network. Agent enrichment of
the cross-file narrative happens later (pr-synthesis step), not in this module.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

from ...config import load_review_focus_areas
from ...context_budget import hard_truncate
from ...state import get_state_dir, get_value
from ..subprocess_utils import run_safe
from .pr_review_filekey import build_file_key

MANIFEST_SCHEMA_VERSION = 1
DEFAULT_PR_CONTEXT_BUDGET = 16_000
_PR_CONTEXT_BUDGET_ENV = "AGDT_PR_CONTEXT_BUDGET"

_SHORT_HINT_CHARS = 24

_LOCKFILES = frozenset(
    {
        "package-lock.json",
        "poetry.lock",
        "yarn.lock",
        "pnpm-lock.yaml",
        "cargo.lock",
        "uv.lock",
        "gemfile.lock",
        "composer.lock",
    }
)

_CHANGE_VERB = {"add": "adds", "edit": "edits", "delete": "deletes", "rename": "renames"}

_RISK_SUBSTRINGS = (
    "auth",
    "crypto",
    "secret",
    "password",
    "token",
    "payment",
    "security",
    "credential",
)

# Import-extraction patterns (Python + JS/TS) used for cluster derivation.
_PY_IMPORT_RE = re.compile(r"^\s*(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))")
# \bfrom\b ensures 'from' is matched as a whole word, not as a substring of an
# identifier (e.g. a hypothetical 'infrom' variable), preventing false-positive clusters.
_JS_IMPORT_RE = re.compile(r"""(?:\bfrom\b|require\()\s*['"]([^'"]+)['"]""")


# ---------------------------------------------------------------------------
# Per-file classification helpers (pure)
# ---------------------------------------------------------------------------


def normalize_change_type(change_type: str | None) -> str:
    """Normalize a change-type token to one of add | edit | delete | rename.

    Accepts both git status codes (``A``/``M``/``D``/``R``/``R100``) and the
    long-form Azure DevOps values (``add``/``edit``/``delete``/``rename``).
    Unknown or empty values default to ``edit``.
    """
    raw = (change_type or "").strip().lower()
    if raw in ("a", "add"):
        return "add"
    if raw in ("d", "delete"):
        return "delete"
    if raw.startswith("r"):
        return "rename"
    if raw in ("m", "edit", "modify"):
        return "edit"
    return "edit"


def derive_review_mode(
    change_type: str | None,
    is_binary: bool,
    added_lines: int,
    removed_lines: int,
) -> str:
    """Derive the review mode for a file.

    Returns one of ``deleted``, ``binary``, ``renamed``, ``metadata-only``, or
    ``diff`` based on the change type, binary flag, and diffstat.
    """
    change = normalize_change_type(change_type)
    if change == "delete":
        return "deleted"
    if is_binary:
        return "binary"
    total = (added_lines or 0) + (removed_lines or 0)
    if change == "rename" and total == 0:
        return "renamed"
    if total == 0:
        return "metadata-only"
    return "diff"


def _is_test_path(lower: str, basename: str) -> bool:
    """Return True when a path looks like a test or fixture file.

    Uses directory-component and filename-pattern matching rather than substring
    search to avoid false positives on paths like ``src/latest_config.py``
    (contains "test") or ``src/specimen.py`` (contains "spec").
    """
    # Test directory component: /test/, /tests/, /__tests__/
    parts = lower.split("/")
    if any(p in {"test", "tests", "__tests__"} for p in parts[:-1]):
        return True
    # Snapshots directory
    if "__snapshots__" in lower:
        return True
    # Filename-level markers
    name = basename.lower()
    # test_ prefix (e.g. test_state.py)
    if name.startswith("test_"):
        return True
    # Remove the last extension to inspect the stem
    stem = name.rsplit(".", 1)[0]
    # *_test.ext or *-test.ext (e.g. state_test.py, util-test.js)
    if stem.endswith(("_test", "-test")):
        return True
    # Multi-part suffix: *.test.ext, *.spec.ext, *.steps.ext (e.g. a.spec.ts)
    inner_parts = stem.rsplit(".", 1)
    if len(inner_parts) == 2 and inner_parts[1] in {"test", "spec", "steps"}:
        return True
    return False


def _has_migration_component(lower: str) -> bool:
    """Return True when the path contains 'migration' or 'migrations' as a component.

    Uses component matching instead of a raw substring search to avoid false
    positives on paths such as ``src/immigration_policy.py``.
    """
    return any(part in {"migration", "migrations"} for part in lower.split("/"))


def purpose_hint(normalized_path: str | None, change_type: str | None) -> str:
    """Produce a one-line heuristic purpose hint for a file."""
    change = normalize_change_type(change_type)
    path = (normalized_path or "").strip().lstrip("/")
    if not path:
        return "metadata-only change"

    lower = path.lower()
    basename = path.rsplit("/", 1)[-1]

    if _is_test_path(lower, basename):
        return f"tests/fixtures for {basename}"
    if lower.endswith(".sql") or _has_migration_component(lower):
        return "database schema/migration"
    if lower.endswith((".md", ".rst", ".txt")):
        return "documentation"
    if basename.endswith(".lock") or basename in _LOCKFILES:
        return "dependency lockfile"
    if lower.endswith((".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".config")):
        return "configuration"
    return f"{_CHANGE_VERB[change]} {basename}"


def risk_flag(normalized_path: str | None) -> bool:
    """Return True when a path looks security/schema-sensitive (display heuristic)."""
    lower = (normalized_path or "").lower()
    if not lower:
        return False
    if any(token in lower for token in _RISK_SUBSTRINGS):
        return True
    if lower.endswith(".sql") or _has_migration_component(lower):
        return True
    return False


# ---------------------------------------------------------------------------
# Cross-file cluster derivation (deterministic)
# ---------------------------------------------------------------------------


def _basename(path: str) -> str:
    return path.replace("\\", "/").rsplit("/", 1)[-1]


def _strip_known_suffix(name: str) -> str:
    """Strip a single known source extension from a basename."""
    for ext in (".tsx", ".jsx", ".ts", ".js", ".py", ".mjs", ".cjs"):
        if name.endswith(ext):
            return name[: -len(ext)]
    return name


def _test_stem(basename: str) -> str | None:
    """Return the source stem a test file targets, or None if not a test file."""
    name = basename
    if name.startswith("test_") and name.endswith(".py"):
        return name[len("test_") : -len(".py")]
    stem = _strip_known_suffix(name)
    for marker in (".test", ".spec", "_test", "-test", ".steps"):
        if stem.endswith(marker):
            return stem[: -len(marker)]
    return None


def _source_stem(basename: str) -> str:
    """Return the comparable stem of a (non-test) source basename."""
    return _strip_known_suffix(basename)


def _import_references(text_lines: list[str]) -> set[str]:
    """Extract import target leaf tokens from added source lines."""
    tokens: set[str] = set()
    for line in text_lines:
        py_match = _PY_IMPORT_RE.match(line)
        if py_match:
            module = py_match.group(1) or py_match.group(2) or ""
            for part in module.split("."):
                if part:
                    tokens.add(part.lower())
        js_match = _JS_IMPORT_RE.search(line)
        if js_match:
            target = js_match.group(1)
            leaf = _strip_known_suffix(_basename(target))
            if leaf and leaf not in (".", ".."):
                tokens.add(leaf.lower())
    return tokens


def _path_tokens(normalized_path: str) -> set[str]:
    """Tokens an import could plausibly match a file by (module + filename stem)."""
    path = normalized_path.lstrip("/")
    if not path:
        return set()
    basename = path.rsplit("/", 1)[-1]
    stem = _strip_known_suffix(basename)
    tokens = {stem.lower()}
    if basename.endswith(".py"):
        tokens.add(basename[: -len(".py")].lower())
    return tokens


def _top_dir(normalized_path: str) -> str:
    """Return the directory path (without filename) for grouping heuristics."""
    path = normalized_path.replace("\\", "/").lstrip("/")
    if not path or "/" not in path:
        return ""
    return path.rsplit("/", 1)[0]


class _UnionFind:
    """Minimal union-find for connected-component clustering."""

    def __init__(self, items: list[str]) -> None:
        self._parent = {item: item for item in items}

    def find(self, item: str) -> str:
        while self._parent[item] != item:
            # Path halving: skip one level on each step, compressing the chain.
            self._parent[item] = self._parent[self._parent[item]]
            item = self._parent[item]
        return item

    def union(self, a: str, b: str) -> None:
        root_a, root_b = self.find(a), self.find(b)
        if root_a != root_b:
            # Deterministic: smaller key becomes the root.
            low, high = sorted((root_a, root_b))
            self._parent[high] = low


def derive_clusters(cluster_inputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Derive deterministic cross-file clusters.

    Each input is ``{fileKey, path, normalizedPath, addedTextLines}``. Edges are
    formed by test↔source pairing, schema/migration↔same-folder source, and
    direct import references. Connected components with at least two members are
    returned as clusters (sorted, with the contributing edge reasons).

    Args:
        cluster_inputs: One entry per changed file.

    Returns:
        A sorted list of cluster dicts ``{id, members, paths, reasons}``.
    """
    keys = [entry["fileKey"] for entry in cluster_inputs]
    uf = _UnionFind(keys)
    reasons: dict[tuple[str, ...], set[str]] = {}

    def add_edge(a: str, b: str, reason: str) -> None:
        if a == b:
            return
        uf.union(a, b)
        reasons.setdefault(tuple(sorted((a, b))), set()).add(reason)

    # Build per-file derived values and small look-up indices up-front (O(n))
    # so that each edge category can be resolved in a single pass rather than
    # the O(n²) pairwise loop that was here before.
    import_tokens_by_key: dict[str, set[str]] = {}
    test_stem_by_key: dict[str, str | None] = {}
    source_stem_index: dict[str, list[str]] = {}  # source stem  → file keys
    path_token_index: dict[str, list[str]] = {}  # path token   → file keys
    top_dir_schema_index: dict[str, list[str]] = {}  # top dir      → schema file keys
    top_dir_all_index: dict[str, list[str]] = {}  # top dir      → all file keys

    for entry in cluster_inputs:
        k = entry["fileKey"]
        path = entry["normalizedPath"]
        base = _basename(path)

        import_tokens_by_key[k] = _import_references(entry.get("addedTextLines", []))

        for tok in _path_tokens(path):
            path_token_index.setdefault(tok, []).append(k)

        test_stem_by_key[k] = _test_stem(base)
        source_stem_index.setdefault(_source_stem(base), []).append(k)

        top_dir = _top_dir(path)
        if top_dir:
            lower_path = path.lower()
            top_dir_all_index.setdefault(top_dir, []).append(k)
            if lower_path.endswith(".sql") or _has_migration_component(lower_path):
                top_dir_schema_index.setdefault(top_dir, []).append(k)

    # Test ↔ source edges: for each test file look up matching source stems (~O(n)).
    for k, stem in test_stem_by_key.items():
        if stem is not None:
            for other_k in source_stem_index.get(stem, []):
                add_edge(k, other_k, "test")

    # Schema/migration ↔ same-folder edges: pair every schema file with every
    # other file sharing the same directory (~O(n)).
    for top_dir, schema_keys in top_dir_schema_index.items():
        for sk in schema_keys:
            for ok in top_dir_all_index.get(top_dir, []):
                add_edge(sk, ok, "schema")

    # Import reference edges: for each file's import tokens look up which files
    # have that token in their path (~O(n·t) where t is avg tokens per file).
    for k, import_tokens in import_tokens_by_key.items():
        for tok in import_tokens:
            for other_k in path_token_index.get(tok, []):
                add_edge(k, other_k, "import")

    components: dict[str, list[str]] = {}
    for key in keys:
        components.setdefault(uf.find(key), []).append(key)

    path_by_key = {entry["fileKey"]: entry["normalizedPath"] for entry in cluster_inputs}
    clusters: list[dict[str, Any]] = []
    for members in components.values():
        member_keys = sorted(set(members))
        if len(member_keys) < 2:
            continue
        edge_reasons: set[str] = set()
        for pair, pair_reasons in reasons.items():
            if pair[0] in member_keys and pair[1] in member_keys:
                edge_reasons |= pair_reasons
        clusters.append(
            {
                "members": member_keys,
                "paths": sorted(path_by_key[k] for k in member_keys),
                "reasons": sorted(edge_reasons),
            }
        )

    clusters.sort(key=lambda c: c["members"][0])
    for index, cluster in enumerate(clusters, start=1):
        cluster["id"] = f"cluster-{index}"
    return clusters


# ---------------------------------------------------------------------------
# Manifest assembly
# ---------------------------------------------------------------------------


def _added_text_lines(file_detail: dict[str, Any]) -> list[str]:
    return [str(line.get("content", "")) for line in file_detail.get("addedLines", []) if isinstance(line, dict)]


def _build_prompt_link_map(queue_entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    link_map: dict[str, dict[str, Any]] = {}
    for entry in queue_entries:
        if not isinstance(entry, dict):
            continue
        for key in ("normalizedPath", "path"):
            value = entry.get(key)
            if isinstance(value, str) and value:
                link_map.setdefault(value, entry)
    return link_map


def build_manifest(
    pull_request_id: int,
    pr_details: dict[str, Any],
    queue_entries: list[dict[str, Any]],
    commit_hash: str,
    commit_hash_short: str,
    *,
    jira_key: str = "",
    focus_areas: str = "",
) -> dict[str, Any]:
    """Build the full machine-readable manifest dict from PR details.

    Args:
        pull_request_id: PR ID.
        pr_details: Full PR details payload (with ``files``).
        queue_entries: ``pending`` entries from ``queue.json`` (for prompt links).
        commit_hash: Full commit SHA the review targets (may be empty).
        commit_hash_short: Short commit hash (may be empty).
        jira_key: Linked Jira issue key (optional).
        focus_areas: Repo-specific review focus-area markdown (optional).

    Returns:
        The manifest dict (``budget`` is filled in by the rendering step).
    """
    from .review_helpers import convert_to_prompt_filename, normalize_repo_path

    pr_info = pr_details.get("pullRequest", pr_details)
    link_map = _build_prompt_link_map(queue_entries)

    files_payload = pr_details.get("files", [])
    rows: list[dict[str, Any]] = []
    cluster_inputs: list[dict[str, Any]] = []

    for file_detail in files_payload:
        path = file_detail.get("path", "")
        if not path:
            continue
        normalized = normalize_repo_path(path)
        if not normalized:
            continue
        file_key = build_file_key(normalized)
        change = normalize_change_type(file_detail.get("changeType"))
        is_binary = bool(file_detail.get("isBinary"))
        added = int(file_detail.get("addedLineCount") or 0)
        removed = int(file_detail.get("removedLineCount") or 0)

        entry = link_map.get(normalized) or link_map.get(path)
        if entry and isinstance(entry.get("promptFile"), str):
            prompt_file = entry["promptFile"]
        else:
            prompt_file = convert_to_prompt_filename(path)

        rows.append(
            {
                "fileKey": file_key,
                "path": path,
                "normalizedPath": normalized,
                "changeType": change,
                "reviewMode": derive_review_mode(change, is_binary, added, removed),
                "addedLines": added,
                "removedLines": removed,
                "changedLines": added + removed,
                "isBinary": is_binary,
                "purposeHint": purpose_hint(normalized, change),
                "riskFlag": risk_flag(normalized),
                "reviewDepth": None,
                "reviewDepthReasons": [],
                "promptFile": prompt_file,
            }
        )
        cluster_inputs.append(
            {
                "fileKey": file_key,
                "path": path,
                "normalizedPath": normalized,
                "addedTextLines": _added_text_lines(file_detail),
            }
        )

    # Sort both parallel lists by normalizedPath for deterministic on-disk artifacts
    # regardless of the order Azure DevOps returns files from the API.
    rows.sort(key=lambda r: r["normalizedPath"])
    cluster_inputs.sort(key=lambda c: c["normalizedPath"])

    clusters = derive_clusters(cluster_inputs)

    fingerprint = hashlib.sha256(
        json.dumps(
            [commit_hash, sorted([(r["normalizedPath"], r["changeType"], r["changedLines"]) for r in rows])],
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()[:12]

    return {
        "schemaVersion": MANIFEST_SCHEMA_VERSION,
        "pullRequestId": pull_request_id,
        "commitHash": commit_hash or "",
        "commitHashShort": commit_hash_short or "",
        "manifestVersion": fingerprint,
        "generatedUtc": _deterministic_generated_utc(pr_info),
        "meta": {
            "prTitle": str(pr_info.get("title", "") or ""),
            "prSummary": _summarize(str(pr_info.get("description", "") or "")),
            "jiraKey": jira_key or "",
            "focusAreas": focus_areas or "",
        },
        "files": rows,
        "clusters": clusters,
        "budget": None,
    }


def _summarize(description: str, limit: int = 500) -> str:
    """Collapse whitespace and truncate a PR description for the manifest meta."""
    collapsed = " ".join(description.split())
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[:limit].rstrip() + "…"


def _deterministic_generated_utc(pr_info: dict[str, Any]) -> str:
    """Return a deterministic timestamp-like marker for manifest metadata.

    Empty string is the intentional sentinel when PR metadata does not provide
    a creation timestamp.
    """
    for key in ("creationDate", "createdDate"):
        value = pr_info.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


# ---------------------------------------------------------------------------
# Budget-bounded pr-context skeleton rendering
# ---------------------------------------------------------------------------


def _render_meta(meta: dict[str, Any], pull_request_id: int) -> list[str]:
    lines = [f"# PR Review Context — PR {pull_request_id}", ""]
    if meta.get("prTitle"):
        lines.append(f"**Title:** {meta['prTitle']}")
    if meta.get("jiraKey"):
        lines.append(f"**Issue:** {meta['jiraKey']}")
    if meta.get("prSummary"):
        lines.append(f"**Summary:** {meta['prSummary']}")
    if meta.get("focusAreas"):
        lines.append("")
        lines.append("**Focus areas:**")
        lines.append(meta["focusAreas"])
    lines.append("")
    return lines


def _render_row(row: dict[str, Any], *, hint_chars: int | None, links_only: bool) -> str:
    link = f"[prompt]({row['promptFile']})"
    if links_only:
        return f"- `{row['normalizedPath']}` → {link}"
    risk = "⚠️" if row["riskFlag"] else ""
    depth = row["reviewDepth"] or "?"
    hint = row["purposeHint"]
    if hint_chars is not None and len(hint) > hint_chars:
        hint = hint[:hint_chars].rstrip() + "…"
    return (
        f"| `{row['normalizedPath']}` | {row['changeType']} | "
        f"+{row['addedLines']}/-{row['removedLines']} | {row['reviewMode']} | "
        f"{risk} | {depth} | {hint} | {link} |"
    )


def _render_context(
    meta: dict[str, Any],
    pull_request_id: int,
    rows: list[dict[str, Any]],
    collapsed_count: int,
    clusters: list[dict[str, Any]],
    *,
    hint_chars: int | None,
    links_only: bool,
) -> str:
    lines = _render_meta(meta, pull_request_id)
    lines.append("## Files")
    lines.append("")
    if not links_only:
        lines.append("| path | change | diff | mode | risk | depth | purpose | prompt |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in rows:
        lines.append(_render_row(row, hint_chars=hint_chars, links_only=links_only))
    if collapsed_count:
        lines.append(f"- _+{collapsed_count} light/low-risk file(s) collapsed (see manifest.json)._")
    lines.append("")
    if clusters:
        lines.append("## Clusters")
        lines.append("")
        for cluster in clusters:
            members = ", ".join(f"`{p}`" for p in cluster["paths"])
            lines.append(f"- **{cluster['id']}** ({', '.join(cluster['reasons'])}): {members}")
        lines.append("")
    return "\n".join(lines)


def _is_collapsible(row: dict[str, Any]) -> bool:
    """A row is collapsible when it is neither risk-flagged nor classified deep."""
    if row["riskFlag"]:
        return False
    if row["reviewDepth"] == "deep":
        return False
    return True


def _partition_rows(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    """Split rows into the ones kept full vs the collapsed light/low-risk tail."""
    kept: list[dict[str, Any]] = []
    collapsed = 0
    for row in rows:
        if _is_collapsible(row):
            collapsed += 1
        else:
            kept.append(row)
    if not kept:
        # Never collapse everything — keep the first row so the skeleton is non-empty.
        return rows[:1], max(len(rows) - 1, 0)
    return kept, collapsed


def render_pr_context(manifest: dict[str, Any], budget: int) -> tuple[str, dict[str, Any]]:
    """Render the budget-bounded pr-context skeleton from a manifest.

    Applies a deterministic degradation chain when over budget:
    passthrough → collapse-light → shorten-hints → links-only → truncated.

    Returns:
        ``(skeleton_text, budget_info)`` where ``budget_info`` records the limit,
        full/final character counts, the final stage, and applied degradations.
    """
    meta = manifest.get("meta", {})
    pull_request_id = manifest.get("pullRequestId", 0)
    rows = manifest.get("files", [])
    clusters = manifest.get("clusters", [])

    full = _render_context(meta, pull_request_id, rows, 0, clusters, hint_chars=None, links_only=False)
    full_chars = len(full)

    def info(stage: str, text: str, degradations: list[str]) -> dict[str, Any]:
        return {
            "limit": budget,
            "fullChars": full_chars,
            "finalChars": len(text),
            "stage": stage,
            "degradations": degradations,
        }

    if full_chars <= budget:
        return full, info("passthrough", full, [])

    kept, collapsed = _partition_rows(rows)

    collapsed_text = _render_context(
        meta, pull_request_id, kept, collapsed, clusters, hint_chars=None, links_only=False
    )
    if len(collapsed_text) <= budget:
        return collapsed_text, info("collapse-light", collapsed_text, ["collapse-light"])

    shortened = _render_context(
        meta, pull_request_id, kept, collapsed, clusters, hint_chars=_SHORT_HINT_CHARS, links_only=False
    )
    if len(shortened) <= budget:
        return shortened, info("shorten-hints", shortened, ["collapse-light", "shorten-hints"])

    links = _render_context(meta, pull_request_id, kept, collapsed, clusters, hint_chars=0, links_only=True)
    if len(links) <= budget:
        return links, info("links-only", links, ["collapse-light", "shorten-hints", "links-only"])

    truncated = hard_truncate(links, budget)
    return truncated, info("truncated", truncated, ["collapse-light", "shorten-hints", "links-only", "truncated"])


# ---------------------------------------------------------------------------
# CLI command
# ---------------------------------------------------------------------------


def resolve_repo_root() -> str:
    """Resolve the repository root via git, falling back to the current dir."""
    try:
        result = run_safe(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout.strip()
    except Exception:
        pass
    return str(Path.cwd())


def resolve_pr_context_budget() -> int:
    """Resolve the pr-context character budget from env, else the default."""
    raw = os.environ.get(_PR_CONTEXT_BUDGET_ENV, "").strip()
    if not raw:
        return DEFAULT_PR_CONTEXT_BUDGET
    try:
        value = int(raw)
    except ValueError:
        return DEFAULT_PR_CONTEXT_BUDGET
    return value if value > 0 else DEFAULT_PR_CONTEXT_BUDGET


def build_manifest_command() -> None:
    """CLI entry point for ``agdt-pr-review-build-manifest``."""
    import argparse

    from .helpers import resolve_review_artifact_dir_name

    parser = argparse.ArgumentParser(description="Build the v2 PR review manifest + pr-context skeleton.")
    parser.add_argument("--pr", type=int, default=None, help="Pull request ID")
    parser.add_argument("--dry-run", action="store_true", help="Print without writing artifacts")
    args = parser.parse_args()

    pr_id = args.pr if args.pr is not None else get_value("pull_request_id")
    if pr_id is None:
        print("Error: PR ID required (--pr or pull_request_id state).", file=sys.stderr)
        sys.exit(1)
    try:
        pull_request_id = int(pr_id)
    except (TypeError, ValueError):
        print(
            "Error: pull_request_id in state must be an integer. "
            "Provide --pr or set pull_request_id to an integer value.",
            file=sys.stderr,
        )
        sys.exit(1)
    state_dir = get_state_dir()

    details_path = state_dir / "temp-get-pull-request-details-response.json"
    if not details_path.exists():
        print(f"Error: PR details file not found: {details_path}", file=sys.stderr)
        sys.exit(1)
    try:
        with open(details_path, encoding="utf-8") as handle:
            pr_details = json.load(handle)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Error: could not read PR details file: {exc}", file=sys.stderr)
        sys.exit(1)

    # Derive commit_hash_short from PR details (authoritative) so the artifact
    # directory is correct even when state is stale (e.g. a different PR was
    # reviewed last). When PR details lack a valid commit hash, pass the raw
    # state value into resolve_review_artifact_dir_name() so fallback discovery
    # and self-healing remain centralized (#1182).
    from ...state import is_safe_dir_segment

    commit_hash = extract_commit_hash(pr_details)
    commit_hash_short = ""
    resolver_commit_hash_short: str | None = None
    if commit_hash:
        derived_short = commit_hash[:12]
        commit_hash_short = derived_short if is_safe_dir_segment(derived_short) else ""
        resolver_commit_hash_short = commit_hash_short
    if not commit_hash_short:
        resolver_commit_hash_short = get_value("review.commit_hash_short")
        if isinstance(resolver_commit_hash_short, str):
            commit_hash_short = resolver_commit_hash_short

    dir_name = resolve_review_artifact_dir_name(pull_request_id, resolver_commit_hash_short, backfill=not args.dry_run)
    # When the resolver recovered a commit-hash-scoped directory via fallback discovery,
    # dir_name is a 12-char hex string that does not match the current commit_hash_short.
    # Propagate it so the manifest's commitHashShort field reflects the actual artifact scope.
    if not commit_hash_short and re.fullmatch(r"[0-9a-f]{12}", dir_name):
        commit_hash_short = dir_name
    prompts_dir = state_dir / "pull-request-review" / dir_name

    queue_entries = load_queue_entries(prompts_dir)
    jira_key = get_value("jira.issue_key") or ""
    focus_areas = load_review_focus_areas(resolve_repo_root()) or ""

    manifest = build_manifest(
        pull_request_id,
        pr_details,
        queue_entries,
        commit_hash,
        commit_hash_short,
        jira_key=jira_key,
        focus_areas=focus_areas,
    )
    skeleton, budget_info = render_pr_context(manifest, resolve_pr_context_budget())
    manifest["budget"] = budget_info

    if args.dry_run:
        print(f"[dry-run] manifest: {len(manifest['files'])} files, {len(manifest['clusters'])} clusters")
        print(f"[dry-run] pr-context stage={budget_info['stage']} chars={budget_info['finalChars']}")
        return

    prompts_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = prompts_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
    context_path = prompts_dir / "pr-context.md"
    context_path.write_text(skeleton, encoding="utf-8")

    print(f"Manifest written: {manifest_path}")
    print(f"PR context written: {context_path} (stage={budget_info['stage']})")


def load_queue_entries(prompts_dir: Path) -> list[dict[str, Any]]:
    """Load the ``pending`` entries from ``queue.json`` (empty on any failure)."""
    queue_path = prompts_dir / "queue.json"
    if not queue_path.exists():
        return []
    try:
        with open(queue_path, encoding="utf-8") as handle:
            payload = json.load(handle)
    except (OSError, ValueError):
        return []
    pending = payload.get("pending")
    return pending if isinstance(pending, list) else []


def extract_commit_hash(pr_details: dict[str, Any]) -> str:
    """Extract the full source commit SHA from PR details (empty if absent)."""
    pr_info = pr_details.get("pullRequest", pr_details)
    last_merge = pr_info.get("lastMergeSourceCommit")
    if isinstance(last_merge, dict):
        commit_id = last_merge.get("commitId")
        if isinstance(commit_id, str):
            return commit_id.strip()
    return ""
