"""Deterministic per-file review-depth triage (v2 PR review).

Classifies each changed file as ``light`` (single-model, no rubber ducks) or
``deep`` (rubber ducks required), writing ``reviewDepth`` + a per-file reason
list into the manifest and queue. Enforces cost caps (model calls / changed
lines / minutes) by deterministically demoting the lowest-risk deep files to
light when a budget is exceeded.

This stage is **deterministic only** — no agent or duck calls (agent
finalization of depth is P2). Config is read from ``pullRequestReview.triage``
in ``.github/agdt-config.json`` and merged over in-code defaults so the command
is independent of any P0 config-foundation work.
"""

from __future__ import annotations

import json
import sys
from fnmatch import fnmatchcase
from pathlib import Path
from typing import Any

from ...config import load_repo_config
from ...state import get_state_dir, get_value
from .pr_review_manifest import resolve_repo_root

# In-code defaults (plan §7 + §15.8). Cost caps replace the file-count cap.
_DEFAULT_TRIAGE_CONFIG: dict[str, Any] = {
    "enabled": True,
    "defaultDepth": "deep",
    "deepGlobs": [
        "**/auth/**",
        "**/crypto/**",
        "**/secrets/**",
        "**/payment/**",
        "**/*.sql",
        "**/migrations/**",
    ],
    "lightGlobs": [
        "**/*.md",
        "**/*.lock",
        "**/__snapshots__/**",
        "**/_version.py",
    ],
    "minDiffLinesForDeep": 20,
    "maxDeepModelCalls": 30,
    "maxDeepTotalChangedLines": 2000,
    "maxReviewMinutes": 60,
}

_TRIVIAL_MODES = frozenset({"deleted", "renamed", "binary", "metadata-only"})
_MANY_THREADS = 3

# Cost model: a deep file costs 3 model calls + 10 minutes; a light file 1 + 3.
_DEEP_MODEL_CALLS = 3
_DEEP_MINUTES = 10
_LIGHT_MINUTES = 3

# Risk weights used to order demotions (lowest-risk demoted first).
_RISK_WEIGHTS = {
    "force-deep:glob": 100,
    "force-deep:prior-needs-work": 80,
    "force-deep:existing-threads": 70,
    "force-deep:large-diff": 40,
    "default:deep": 20,
}


def load_triage_config(repo_root: str | None) -> dict[str, Any]:
    """Load triage config, merging ``pullRequestReview.triage`` over defaults."""
    config: dict[str, Any] = dict(_DEFAULT_TRIAGE_CONFIG)
    config["deepGlobs"] = list(_DEFAULT_TRIAGE_CONFIG["deepGlobs"])
    config["lightGlobs"] = list(_DEFAULT_TRIAGE_CONFIG["lightGlobs"])

    repo_config = load_repo_config(repo_root or str(Path.cwd()))
    pr_section = repo_config.get("pullRequestReview")
    if not isinstance(pr_section, dict):
        return config
    triage = pr_section.get("triage")
    if not isinstance(triage, dict):
        return config

    for key, default_value in _DEFAULT_TRIAGE_CONFIG.items():
        if key not in triage or not isinstance(triage[key], type(default_value)):
            continue
        value = triage[key]
        # bool is a subclass of int — reject booleans for numeric thresholds.
        if isinstance(default_value, int) and not isinstance(default_value, bool) and isinstance(value, bool):
            continue
        if key in {"deepGlobs", "lightGlobs"}:
            value = [pattern for pattern in value if isinstance(pattern, str)]
        config[key] = value

    if config["defaultDepth"] not in {"deep", "light"}:
        config["defaultDepth"] = _DEFAULT_TRIAGE_CONFIG["defaultDepth"]
    return config


def _matches_any_glob(normalized_path: str, patterns: list[str]) -> bool:
    """Case-insensitive glob match where ``*`` spans path separators."""
    target = (normalized_path or "").lower()
    return any(fnmatchcase(target, pattern.lower()) for pattern in patterns)


def classify_file_depth(file_row: dict[str, Any], config: dict[str, Any]) -> tuple[str, list[str]]:
    """Deterministically classify a single file's review depth.

    Returns ``(depth, reasons)`` where depth is ``light`` or ``deep`` and
    reasons is the ordered list of rule labels that produced the decision.
    """
    normalized = file_row.get("normalizedPath", "")
    review_mode = file_row.get("reviewMode", "diff")
    changed = int(file_row.get("changedLines") or 0)

    if review_mode in _TRIVIAL_MODES:
        return "light", [f"force-light:{review_mode}"]
    if _matches_any_glob(normalized, config["lightGlobs"]):
        return "light", ["force-light:glob"]
    if _matches_any_glob(normalized, config["deepGlobs"]):
        return "deep", ["force-deep:glob"]
    if file_row.get("priorStatus") == "needs-work":
        return "deep", ["force-deep:prior-needs-work"]
    if int(file_row.get("existingThreadCount") or 0) >= _MANY_THREADS:
        return "deep", ["force-deep:existing-threads"]
    if changed >= int(config["minDiffLinesForDeep"]):
        return "deep", ["force-deep:large-diff"]
    depth = config["defaultDepth"]
    return depth, [f"default:{depth}"]


def _risk_score(reasons: list[str]) -> int:
    return max((_RISK_WEIGHTS.get(reason, 0) for reason in reasons), default=0)


def _costs(entries: list[dict[str, Any]]) -> tuple[int, int, int]:
    """Return (deep_model_calls, deep_changed_lines, total_minutes)."""
    deep = [entry for entry in entries if entry["depth"] == "deep"]
    light_count = len(entries) - len(deep)
    model_calls = len(deep) * _DEEP_MODEL_CALLS
    changed = sum(int(entry["changedLines"]) for entry in deep)
    minutes = len(deep) * _DEEP_MINUTES + light_count * _LIGHT_MINUTES
    return model_calls, changed, minutes


def apply_cost_caps(
    entries: list[dict[str, Any]],
    config: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Demote lowest-risk deep files to light until all cost caps are satisfied.

    Args:
        entries: One dict per file ``{fileKey, depth, reasons, changedLines}``.
        config: Triage config with the ``max*`` caps.

    Returns:
        ``(entries, demotions)`` — entries with demoted depths applied, and the
        list of demotion records for transparent reporting.
    """
    entries = [dict(entry) for entry in entries]
    for entry in entries:
        entry["reasons"] = list(entry["reasons"])
    demotions: list[dict[str, Any]] = []

    max_calls = int(config["maxDeepModelCalls"])
    max_changed = int(config["maxDeepTotalChangedLines"])
    max_minutes = int(config["maxReviewMinutes"])

    while True:
        model_calls, changed, minutes = _costs(entries)
        if model_calls <= max_calls and changed <= max_changed and minutes <= max_minutes:
            break
        deep = [entry for entry in entries if entry["depth"] == "deep"]
        if not deep:
            break
        deep.sort(key=lambda entry: (_risk_score(entry["reasons"]), int(entry["changedLines"]), entry["fileKey"]))
        victim = deep[0]
        victim["depth"] = "light"
        victim["reasons"].append("demoted:cost-cap")
        demotions.append({"fileKey": victim["fileKey"], "from": "deep", "to": "light", "reason": "cost-cap"})

    return entries, demotions


def _summarize_triage(
    capped: list[dict[str, Any]],
    demotions: list[dict[str, Any]],
    config: dict[str, Any],
    *,
    enabled: bool,
) -> dict[str, Any]:
    deep_count = sum(1 for entry in capped if entry["depth"] == "deep")
    return {
        "enabled": enabled,
        "deepCount": deep_count,
        "lightCount": len(capped) - deep_count,
        "demotions": demotions,
        "caps": {
            "maxDeepModelCalls": int(config["maxDeepModelCalls"]),
            "maxDeepTotalChangedLines": int(config["maxDeepTotalChangedLines"]),
            "maxReviewMinutes": int(config["maxReviewMinutes"]),
        },
    }


def triage_manifest(manifest: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    """Classify every file in the manifest and apply cost caps in place.

    Writes ``reviewDepth`` + ``reviewDepthReasons`` onto each file row and a
    ``triage`` summary onto the manifest. Returns the same manifest object.
    """
    rows = manifest.get("files", [])

    if not config.get("enabled", True):
        default_depth = config["defaultDepth"]
        for row in rows:
            row["reviewDepth"] = default_depth
            row["reviewDepthReasons"] = ["triage-disabled"]
        synthetic = [{"fileKey": row["fileKey"], "depth": default_depth} for row in rows]
        manifest["triage"] = _summarize_triage(synthetic, [], config, enabled=False)
        return manifest

    entries: list[dict[str, Any]] = []
    for row in rows:
        depth, reasons = classify_file_depth(row, config)
        entries.append(
            {
                "fileKey": row["fileKey"],
                "depth": depth,
                "reasons": reasons,
                "changedLines": int(row.get("changedLines") or 0),
            }
        )

    capped, demotions = apply_cost_caps(entries, config)
    by_key = {entry["fileKey"]: entry for entry in capped}
    for row in rows:
        entry = by_key[row["fileKey"]]
        row["reviewDepth"] = entry["depth"]
        row["reviewDepthReasons"] = entry["reasons"]

    manifest["triage"] = _summarize_triage(capped, demotions, config, enabled=True)
    return manifest


# ---------------------------------------------------------------------------
# CLI command
# ---------------------------------------------------------------------------


def _apply_depth_to_queue(prompts_dir: Path, manifest: dict[str, Any]) -> None:
    queue_path = prompts_dir / "queue.json"
    if not queue_path.exists():
        return
    try:
        with open(queue_path, encoding="utf-8") as handle:
            payload = json.load(handle)
    except (OSError, ValueError):
        return

    depth_by_path: dict[str, dict[str, Any]] = {}
    for row in manifest.get("files", []):
        depth_by_path[row["normalizedPath"]] = {
            "reviewDepth": row.get("reviewDepth"),
            "reviewDepthReasons": row.get("reviewDepthReasons", []),
        }

    pending = payload.get("pending")
    if not isinstance(pending, list):
        return
    for entry in pending:
        if not isinstance(entry, dict):
            continue
        info = depth_by_path.get(entry.get("normalizedPath", ""))
        if info is not None:
            entry["reviewDepth"] = info["reviewDepth"]
            entry["reviewDepthReasons"] = info["reviewDepthReasons"]

    try:
        with open(queue_path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
    except OSError as exc:
        print(f"Warning: could not update {queue_path}: {exc}", file=sys.stderr)


def triage_command() -> None:
    """CLI entry point for ``agdt-pr-review-triage``."""
    import argparse

    from .helpers import resolve_review_artifact_dir_name

    parser = argparse.ArgumentParser(description="Classify per-file review depth for the v2 PR review.")
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
    commit_hash_short = get_value("review.commit_hash_short")
    dir_name = resolve_review_artifact_dir_name(pull_request_id, commit_hash_short, backfill=not args.dry_run)
    prompts_dir = state_dir / "pull-request-review" / dir_name
    manifest_path = prompts_dir / "manifest.json"

    if not manifest_path.exists():
        # Fall back to the PR-scoped directory when state is stale (e.g. review.commit_hash_short
        # still points at a previous PR). This keeps the command working without requiring the
        # caller to reset state between runs.
        fallback_dir = f"PR{pull_request_id}"
        if dir_name != fallback_dir:
            fallback_prompts_dir = state_dir / "pull-request-review" / fallback_dir
            fallback_manifest = fallback_prompts_dir / "manifest.json"
            if fallback_manifest.exists():
                prompts_dir = fallback_prompts_dir
                manifest_path = fallback_manifest
    if not manifest_path.exists():
        print(f"Error: manifest not found: {manifest_path}. Run agdt-pr-review-build-manifest first.", file=sys.stderr)
        sys.exit(1)
    try:
        with open(manifest_path, encoding="utf-8") as handle:
            manifest = json.load(handle)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Error: could not read manifest file: {exc}", file=sys.stderr)
        sys.exit(1)

    config = load_triage_config(resolve_repo_root())
    triage_manifest(manifest, config)

    summary = manifest["triage"]
    if args.dry_run:
        print(
            f"[dry-run] triage: {summary['deepCount']} deep / {summary['lightCount']} light, "
            f"{len(summary['demotions'])} demotion(s)"
        )
        return

    with open(manifest_path, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
    _apply_depth_to_queue(prompts_dir, manifest)

    print(f"Triage complete: {summary['deepCount']} deep / {summary['lightCount']} light")
    if summary["demotions"]:
        print(f"Demoted {len(summary['demotions'])} deep file(s) to light to satisfy cost caps.")
