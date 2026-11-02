"""Orchestration of the additive v2 PR-review artifacts during setup.

Ties together the deterministic v2 artifact generation — manifest, budget-bounded
pr-context skeleton, triage (review depth + cost caps), and blank answer files —
into a single best-effort entry point invoked from ``setup_pull_request_review``.

This is **additive**: it never alters the existing file-review loop. All failures
are caught and reported as warnings so review setup is never aborted by v2 work.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from ...config import load_review_focus_areas
from ...state import get_value
from .pr_review_answers import scaffold_answer_files
from .pr_review_manifest import (
    build_manifest,
    extract_commit_hash,
    load_queue_entries,
    render_pr_context,
    resolve_pr_context_budget,
    resolve_repo_root,
)
from .pr_review_triage import _apply_depth_to_queue, load_triage_config, triage_manifest


def _generate_v2_review_artifacts(pull_request_id: int, pr_details: dict[str, Any], prompts_dir: Path) -> None:
    commit_hash = extract_commit_hash(pr_details)
    commit_hash_short = get_value("review.commit_hash_short") or commit_hash[:12] or ""
    jira_key = get_value("jira.issue_key") or ""
    repo_root = resolve_repo_root()
    focus_areas = load_review_focus_areas(repo_root) or ""
    queue_entries = load_queue_entries(prompts_dir)

    manifest = build_manifest(
        pull_request_id,
        pr_details,
        queue_entries,
        commit_hash,
        commit_hash_short,
        jira_key=jira_key,
        focus_areas=focus_areas,
    )

    config = load_triage_config(repo_root)
    triage_manifest(manifest, config)

    skeleton, budget_info = render_pr_context(manifest, resolve_pr_context_budget())
    manifest["budget"] = budget_info
    prompts_dir.mkdir(parents=True, exist_ok=True)
    with open(prompts_dir / "manifest.json", "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
    (prompts_dir / "pr-context.md").write_text(skeleton, encoding="utf-8")

    _apply_depth_to_queue(prompts_dir, manifest)
    scaffold_answer_files(pull_request_id, prompts_dir, manifest, commit_hash)

    print(
        f"v2 review artifacts: manifest ({len(manifest['files'])} files), "
        f"pr-context [{budget_info['stage']}], "
        f"triage {manifest['triage']['deepCount']} deep / {manifest['triage']['lightCount']} light"
    )


def generate_v2_review_artifacts(
    pull_request_id: int,
    pr_details: dict[str, Any],
    prompts_dir: Path,
) -> None:
    """Best-effort generation of all additive v2 review artifacts.

    Never raises — any failure is logged as a warning so the existing review
    setup flow proceeds unchanged.
    """
    try:
        _generate_v2_review_artifacts(pull_request_id, pr_details, Path(prompts_dir))
    except Exception as exc:
        print(
            f"Warning: v2 review artifact generation failed (setup unaffected): {exc}",
            file=sys.stderr,
        )
