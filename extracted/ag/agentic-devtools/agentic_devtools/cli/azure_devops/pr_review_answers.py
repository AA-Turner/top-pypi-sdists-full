"""Blank per-file answer-file scaffolding (v2 PR review).

When prompts are generated, a blank ``answers/<fileKey>.answer.json`` is
scaffolded for each file following the plan §9 schema, with ``status="pending"``
and the carried fields (prId, commitHash, fileKey, filePath, reviewMode,
reviewDepth, promptHash, attemptId). The subagent later fills in the outcome /
summary / suggestions; the orchestrator derives everything else.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ANSWER_SCHEMA_VERSION = 1


def compute_prompt_hash(prompt_text: str) -> str:
    """Return the SHA-256 hex digest of the handed prompt content."""
    return hashlib.sha256(prompt_text.encode("utf-8")).hexdigest()


def derive_attempt_id(file_key: str, commit_hash: str, prompt_hash: str) -> str:
    """Derive a deterministic attempt id for the initial (pending) answer."""
    seed = f"{file_key}:{commit_hash}:{prompt_hash}"
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12]


def build_answer_skeleton(
    *,
    pr_id: int,
    commit_hash: str,
    file_key: str,
    file_path: str,
    review_mode: str,
    review_depth: str | None,
    prompt_hash: str,
) -> dict[str, Any]:
    """Build a blank, pending answer dict (plan §9 schema)."""
    return {
        "schemaVersion": ANSWER_SCHEMA_VERSION,
        "prId": pr_id,
        "commitHash": commit_hash or "",
        "fileKey": file_key,
        "filePath": file_path,
        "reviewMode": review_mode,
        "reviewDepth": review_depth,
        "promptHash": prompt_hash,
        "attemptId": derive_attempt_id(file_key, commit_hash or "", prompt_hash),
        "status": "pending",
        "outcome": None,
        "summary": None,
        "suggestions": [],
        "needsInfo": None,
        "reviewer": None,
        "confidence": None,
    }


def scaffold_answer_files(
    pull_request_id: int,
    prompts_dir: Path,
    manifest: dict[str, Any],
    commit_hash: str,
) -> list[Path]:
    """Scaffold one blank answer file per manifest file row.

    Creates the ``answers/`` subdirectory under *prompts_dir*. Existing answer
    files are left untouched (idempotent re-scaffold preserves in-progress work).

    Args:
        pull_request_id: PR ID stored into each answer.
        prompts_dir: The ``pull-request-review/<hash>/`` artifact directory.
        manifest: The manifest dict whose ``files`` rows drive scaffolding.
        commit_hash: Full commit SHA the answers are produced against.

    Returns:
        The list of answer-file paths that were newly written.
    """
    answers_dir = prompts_dir / "answers"
    answers_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for row in manifest.get("files", []):
        file_key = row["fileKey"]
        answer_path = answers_dir / f"{file_key}.answer.json"
        if answer_path.exists():
            continue

        prompt_file = row.get("promptFile")
        prompt_text = ""
        if isinstance(prompt_file, str) and prompt_file:
            prompt_path = prompts_dir / prompt_file
            if prompt_path.exists():
                prompt_text = prompt_path.read_text(encoding="utf-8")

        skeleton = build_answer_skeleton(
            pr_id=pull_request_id,
            commit_hash=commit_hash,
            file_key=file_key,
            file_path=row.get("normalizedPath", row.get("path", "")),
            review_mode=row.get("reviewMode", "diff"),
            review_depth=row.get("reviewDepth"),
            prompt_hash=compute_prompt_hash(prompt_text),
        )
        with open(answer_path, "w", encoding="utf-8") as handle:
            json.dump(skeleton, handle, indent=2)
        written.append(answer_path)

    return written
