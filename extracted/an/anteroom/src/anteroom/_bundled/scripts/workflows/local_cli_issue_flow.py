#!/usr/bin/env python3
"""Drive a local issue workflow through Claude, Codex, and GitHub CLI.

This script is intended for Anteroom workflow steps that want durable
orchestration without using Anteroom's API-backed agent runners. Each action
invokes the local CLI tools in one-shot mode and stores lightweight state under
the repository git-dir so later steps can resume cleanly, including from linked
worktrees where ``.git`` is a file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from queue import Empty, Queue
from typing import Any, NoReturn

PLAN_START = "<!-- anteroom:plan:start -->"
PLAN_END = "<!-- anteroom:plan:end -->"
STATE_DIRNAME = "anteroom-workflows"
DEFAULT_CHECKS = "ruff check src/ tests/ && python -m pytest tests/unit/ -x -q --tb=short"
DEFAULT_AUTOFIX = "ruff check src/ tests/ --fix"
WORKTREE_PYTHON_ENV = "ANTEROOM_WORKTREE_PYTHON"
STREAM_SOFT_LIMIT = 60
WORKTREE_JUNK_GLOBS = ("<MagicMock*", ".tmp_issue_*")
DEFAULT_PLAN_REVIEW_TIMEOUT_SECONDS = 300
_STDERR_NOISE_PATTERNS = (
    "Reading additional input from stdin",
    "reading from stdin",
)


def _filter_stderr_noise(stderr: str) -> str:
    lines = stderr.splitlines()
    filtered = [ln for ln in lines if not any(pat in ln for pat in _STDERR_NOISE_PATTERNS)]
    return "\n".join(filtered).strip()


def _timeout_error_message(timeout_seconds: int, stderr: str) -> str:
    primary = f"Timed out after {timeout_seconds}s"
    cleaned = _filter_stderr_noise(stderr)
    if cleaned:
        return f"{primary}; {cleaned}"[:500]
    return primary


def fail(message: str, *, code: int = 1) -> NoReturn:
    print(message, file=sys.stderr)
    raise SystemExit(code)


def run(
    command: list[str],
    *,
    cwd: Path | None = None,
    check: bool = True,
    capture_output: bool = True,
) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=capture_output,
        stdin=subprocess.DEVNULL,
        check=False,
    )
    if check and proc.returncode != 0:
        cmd = " ".join(command)
        stderr = proc.stderr.strip() if proc.stderr else ""
        stdout = proc.stdout.strip() if proc.stdout else ""
        detail = stderr or stdout or f"exit code {proc.returncode}"
        fail(f"Command failed: {cmd}\n{detail}", code=proc.returncode or 1)
    return proc


def run_stdout(command: list[str], *, cwd: Path | None = None) -> str:
    return run(command, cwd=cwd).stdout.strip()


def run_json(command: list[str], *, cwd: Path | None = None) -> dict[str, Any]:
    output = run_stdout(command, cwd=cwd)
    try:
        return json.loads(output)
    except json.JSONDecodeError as exc:
        fail(f"Expected JSON from {' '.join(command)}: {exc}\n{output}")


def ensure_tool(name: str) -> None:
    if shutil.which(name) is None:
        fail(f"Required tool not found in PATH: {name}")


def git_root() -> Path:
    return Path(run_stdout(["git", "rev-parse", "--show-toplevel"])).resolve()


def _resolve_git_path(root: Path, path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path.resolve()
    return (root / path).resolve()


def git_dir(root: Path) -> Path:
    return _resolve_git_path(root, run_stdout(["git", "rev-parse", "--git-dir"], cwd=root))


def state_dir(root: Path, issue_number: int) -> Path:
    return git_common_dir(root) / STATE_DIRNAME / f"issue-{issue_number}"


def git_common_dir(root: Path) -> Path:
    return _resolve_git_path(root, run_stdout(["git", "rev-parse", "--git-common-dir"], cwd=root))


def state_path(root: Path, issue_number: int) -> Path:
    return state_dir(root, issue_number) / "state.json"


def load_state(root: Path, issue_number: int) -> dict[str, Any]:
    path = state_path(root, issue_number)
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        fail(f"Invalid state file at {path}: {exc}")


def save_state(root: Path, issue_number: int, data: dict[str, Any]) -> None:
    path = state_path(root, issue_number)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def update_state(root: Path, state_issue_number: int, **updates: Any) -> dict[str, Any]:
    state = load_state(root, state_issue_number)
    state.update(updates)
    save_state(root, state_issue_number, state)
    return state


def resolve_worktree_python(env: dict[str, str], state: dict[str, Any]) -> str:
    configured = str(env.get(WORKTREE_PYTHON_ENV, "")).strip()
    if configured:
        return configured
    saved = str(state.get("worktree_python", "")).strip()
    if saved:
        return saved
    return sys.executable


def runtime_env_for_worktree(
    env: dict[str, str], state: dict[str, Any], worktree: Path
) -> tuple[dict[str, str], dict[str, str]]:
    runtime_env = env.copy()
    worktree_env = worktree_python_env(worktree)
    source = "worktree_venv"
    if worktree_env:
        runtime_env[WORKTREE_PYTHON_ENV] = worktree_env["worktree_python"]
        runtime_env["VIRTUAL_ENV"] = worktree_env["worktree_venv"]
        runtime_env["PATH"] = f"{worktree_env['worktree_bin']}:{env.get('PATH', '')}"
    else:
        source = "shared_issue_venv"
        runtime_env[WORKTREE_PYTHON_ENV] = resolve_worktree_python(env, state)
        if state.get("worktree_venv"):
            runtime_env["VIRTUAL_ENV"] = str(state["worktree_venv"])
        if state.get("worktree_bin"):
            runtime_env["PATH"] = f"{state['worktree_bin']}:{env.get('PATH', '')}"
        src_path = str((worktree / "src").resolve())
        existing_pythonpath = runtime_env.get("PYTHONPATH", "").strip()
        runtime_env["PYTHONPATH"] = (
            src_path if not existing_pythonpath else f"{src_path}{os.pathsep}{existing_pythonpath}"
        )
    metadata = {
        "source": source,
        "python": runtime_env.get(WORKTREE_PYTHON_ENV, ""),
        "venv": runtime_env.get("VIRTUAL_ENV", ""),
        "path_prefix": runtime_env.get("PATH", "").split(":", 1)[0] if runtime_env.get("PATH") else "",
        "pythonpath": runtime_env.get("PYTHONPATH", ""),
    }
    if not metadata["python"]:
        fail("Unable to resolve a safe Python runtime for the target worktree")
    return runtime_env, metadata


def checks_env_signature(runtime: dict[str, str], command: str) -> str:
    payload = {
        "command": command,
        "runtime": {
            # Normalize to the effective interpreter identity. Worktree-local
            # `src/` paths and the baseline temp worktree path are expected to
            # differ even when the runtime is otherwise equivalent, so they
            # must not invalidate the baseline.
            "python": runtime.get("python", ""),
            "venv": runtime.get("venv", ""),
            "path_prefix": runtime.get("path_prefix", ""),
        },
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def normalize_stage_command(command: str, *, allow_baseline: bool) -> tuple[str, str]:
    stripped = command.strip()
    if not stripped:
        fail("Empty checks stage is not allowed")
    stage_name = "shell"
    if stripped.startswith("ruff "):
        stage_name = "ruff"
    elif "pytest" in stripped:
        stage_name = "pytest"
        if allow_baseline:
            parts = [part for part in shlex.split(stripped) if part not in {"-x", "--exitfirst"}]
            stripped = shlex.join(parts)
    elif stripped.startswith("mypy ") or " mypy " in f" {stripped} ":
        stage_name = "mypy"
    return stage_name, stripped


def split_check_stages(command: str, *, allow_baseline: bool) -> list[dict[str, str]]:
    unsupported = ("||", ";", "\n")
    if any(token in command for token in unsupported):
        fail("Baseline-aware checks only support simple '&&' stage chains")
    raw_stages = [chunk.strip() for chunk in command.split("&&") if chunk.strip()]
    if not raw_stages:
        fail("Checks command produced no runnable stages")
    return [
        {"name": stage_name, "command": normalized}
        for stage_name, normalized in (
            normalize_stage_command(stage, allow_baseline=allow_baseline) for stage in raw_stages
        )
    ]


def extract_stage_fingerprints(stage_name: str, output: str) -> set[str]:
    fingerprints: set[str] = set()
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if stage_name == "ruff":
            match = re.match(r"^(?P<path>[^:\n]+):\d+:\d+:\s+(?P<code>[A-Z]\d+)\b", line)
            if match:
                fingerprints.add(f"ruff:{match.group('path')}:{match.group('code')}")
        elif stage_name == "pytest":
            match = re.match(r"^(?:FAILED|ERROR)\s+(?P<nodeid>\S+)", line)
            if match:
                fingerprints.add(f"pytest:{match.group('nodeid')}")
        elif stage_name == "mypy":
            match = re.match(
                r"^(?P<path>[^:\n]+):\d+(?::\d+)?:\s+error:.*?(?:\s+\[(?P<code>[^\]]+)\])?$",
                line,
            )
            if match:
                fingerprints.add(f"mypy:{match.group('path')}:{match.group('code') or 'unknown'}")
    return fingerprints


def stage_output_requires_fingerprints(stage_name: str) -> bool:
    return stage_name in {"ruff", "pytest", "mypy"}


def run_check_stages(
    worktree: Path,
    *,
    state: dict[str, Any],
    env: dict[str, str] | None = None,
    allow_baseline: bool = False,
) -> dict[str, Any]:
    command = checks_command()
    base_env = env.copy() if env is not None else os.environ.copy()
    runtime_env, runtime_meta = runtime_env_for_worktree(base_env, state, worktree)
    stages = split_check_stages(command, allow_baseline=allow_baseline)
    results: list[dict[str, Any]] = []
    aggregate_lines: list[str] = []
    overall_exit = 0

    removed_before = cleanup_worktree_junk(worktree)
    if removed_before:
        aggregate_lines.append(f"removed_junk: {', '.join(removed_before)}")
    try:
        for stage in stages:
            proc = subprocess.run(
                stage["command"],
                cwd=str(worktree),
                shell=True,
                text=True,
                env=runtime_env,
                capture_output=True,
                stdin=subprocess.DEVNULL,
            )
            output = ((proc.stdout or "") + (proc.stderr or "")).strip()
            fingerprints = extract_stage_fingerprints(stage["name"], output)
            parse_failed = (
                proc.returncode != 0 and stage_output_requires_fingerprints(stage["name"]) and not fingerprints
            )
            if parse_failed:
                overall_exit = proc.returncode or 1
            elif proc.returncode != 0:
                overall_exit = proc.returncode or 1
            results.append(
                {
                    "name": stage["name"],
                    "command": stage["command"],
                    "returncode": proc.returncode,
                    "output": output,
                    "fingerprints": sorted(fingerprints),
                    "parse_failed": parse_failed,
                }
            )
            if output:
                aggregate_lines.append(f"[{stage['name']}]\n{output}")
            if proc.returncode != 0 and not allow_baseline:
                break
    finally:
        removed_after = cleanup_worktree_junk(worktree)
        if removed_after:
            aggregate_lines.append(f"removed_junk: {', '.join(removed_after)}")

    if overall_exit == 0 and any(stage["returncode"] != 0 for stage in results):
        overall_exit = 1
    output = "\n\n".join(line for line in aggregate_lines if line).strip()
    return {
        "returncode": overall_exit,
        "output": output,
        "results": results,
        "command": command,
        "env_signature": checks_env_signature(runtime_meta, command),
        "runtime": runtime_meta,
    }


def latest_main_sha(root: Path) -> str:
    run(["git", "fetch", "origin", "main"], cwd=root, check=False)
    return run_stdout(["git", "rev-parse", latest_main_ref(root)], cwd=root)


def capture_baseline(state: dict[str, Any], *, root: Path) -> dict[str, Any]:
    base_sha = latest_main_sha(root)
    temp_parent = Path(tempfile.mkdtemp(prefix=f"anteroom-baseline-{state['issue_number']}-", dir=str(root.parent)))
    baseline_worktree = temp_parent / "repo"
    try:
        run(["git", "worktree", "add", "--detach", str(baseline_worktree), base_sha], cwd=root)
        stage_result = run_check_stages(baseline_worktree, state=state, allow_baseline=True)
        baseline = {
            "base_sha": base_sha,
            "checks_command": stage_result["command"],
            "checks_env_signature": stage_result["env_signature"],
            "runtime": stage_result["runtime"],
            "results": [
                {
                    "name": item["name"],
                    "fingerprints": item["fingerprints"],
                    "parse_failed": item["parse_failed"],
                }
                for item in stage_result["results"]
            ],
        }
        if any(item["parse_failed"] for item in stage_result["results"]):
            fail("Baseline capture failed closed because a stage output could not be fingerprinted safely")
        return baseline
    finally:
        run(["git", "worktree", "remove", "--force", str(baseline_worktree)], cwd=root, check=False)
        shutil.rmtree(temp_parent, ignore_errors=True)


def compare_against_baseline(current: dict[str, Any], baseline: dict[str, Any]) -> tuple[bool, str]:
    if baseline.get("base_sha") != latest_main_sha(git_root()):
        return False, "baseline_invalid: base SHA drifted"
    if baseline.get("checks_command") != current["command"]:
        return False, "baseline_invalid: checks command changed"
    if baseline.get("checks_env_signature") != current["env_signature"]:
        return False, "baseline_invalid: checks environment changed"

    baseline_results = {item["name"]: item for item in baseline.get("results", [])}
    new_failures: list[str] = []
    for item in current["results"]:
        if item["parse_failed"]:
            return False, f"baseline_invalid: unable to fingerprint {item['name']} output"
        if item["returncode"] == 0:
            continue
        baseline_item = baseline_results.get(item["name"])
        baseline_fingerprints = set((baseline_item or {}).get("fingerprints", []))
        current_fingerprints = set(item["fingerprints"])
        extra = sorted(current_fingerprints - baseline_fingerprints)
        if extra:
            new_failures.extend(extra)

    if new_failures:
        return False, "new_failures: " + ", ".join(new_failures)
    if any(item["returncode"] != 0 for item in current["results"]):
        return True, "baseline_only"
    return True, "checks_passed"


def issue_data(issue_number: int) -> dict[str, Any]:
    data = run_json(
        [
            "gh",
            "issue",
            "view",
            str(issue_number),
            "--json",
            "number,title,body,state,url,labels",
        ]
    )
    data["label_names"] = [label["name"] for label in data.get("labels", [])]
    return data


def repo_name() -> str:
    return run_stdout(["gh", "repo", "view", "--json", "name", "--jq", ".name"])


def slugify(value: str, *, limit: int = 32) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return slug[:limit].strip("-") or "work"


def issue_branch(issue_number: int, title: str) -> str:
    return f"issue-{issue_number}-{slugify(title, limit=40)}"


def issue_worktree(root: Path, repo: str, issue_number: int, title: str) -> Path:
    name = f"{repo}-{issue_number}-{slugify(title, limit=28)}"
    return (root.parent / name).resolve()


def ensure_labels() -> None:
    run(
        [
            "gh",
            "label",
            "create",
            "needs-senior-review",
            "--color",
            "FBCA04",
            "--description",
            "Awaiting senior reviewer sign-off",
            "--force",
        ]
    )
    run(
        [
            "gh",
            "label",
            "create",
            "senior-approved",
            "--color",
            "0E8A16",
            "--description",
            "Senior reviewer has approved",
            "--force",
        ]
    )


def edit_issue_labels(issue_number: int, *, add: list[str], remove: list[str]) -> None:
    current = set(issue_data(issue_number).get("label_names", []))
    wanted_add = [label for label in add if label not in current]
    wanted_remove = [label for label in remove if label in current]
    if not wanted_add and not wanted_remove:
        return

    command = ["gh", "issue", "edit", str(issue_number)]
    for label in wanted_add:
        command.extend(["--add-label", label])
    for label in wanted_remove:
        command.extend(["--remove-label", label])
    run(command)


def pr_label_names(pr_number: int) -> list[str]:
    data = run_json(["gh", "pr", "view", str(pr_number), "--json", "labels"])
    return [label["name"] for label in data.get("labels", [])]


def _normalize_mergeable(value: Any) -> str:
    mergeable = str(value or "unknown").strip().upper()
    if mergeable in {"MERGEABLE", "CONFLICTING", "UNKNOWN"}:
        return mergeable.lower()
    return "unknown"


def _check_bucket(conclusion: str | None, status: str | None, state: str | None = None) -> str:
    normalized_conclusion = str(conclusion or "").strip().upper()
    normalized_status = str(status or "").strip().upper()
    normalized_state = str(state or "").strip().upper()
    if normalized_conclusion in {"SUCCESS", "NEUTRAL", "SKIPPED"}:
        return "passing"
    if normalized_conclusion in {"FAILURE", "TIMED_OUT", "ACTION_REQUIRED"}:
        return "failing"
    if normalized_conclusion in {"CANCELLED", "STALE"}:
        return "cancelled"
    if normalized_state in {"SUCCESS", "EXPECTED", "NEUTRAL"}:
        return "passing"
    if normalized_state in {"FAILURE", "ERROR"}:
        return "failing"
    if normalized_state in {"PENDING", "QUEUED", "IN_PROGRESS"}:
        return "pending"
    if normalized_status == "COMPLETED":
        return "skipped"
    return "pending"


def summarize_status_checks(status_check_rollup: Any) -> dict[str, Any]:
    counts = {"pending": 0, "failing": 0, "passing": 0, "skipped": 0, "cancelled": 0}
    for item in status_check_rollup or []:
        if not isinstance(item, dict):
            continue
        bucket = _check_bucket(item.get("conclusion"), item.get("status"), item.get("state"))
        counts[bucket] += 1

    if counts["failing"]:
        overall = "failing"
    elif counts["pending"]:
        overall = "pending"
    elif counts["passing"]:
        overall = "passing"
    elif counts["cancelled"]:
        overall = "cancelled"
    else:
        overall = "none"

    return {
        "overall": overall,
        "counts": counts,
        "has_required_pending": counts["pending"] > 0,
        "has_required_failures": counts["failing"] > 0,
    }


def branch_status(
    root: Path,
    head_ref: str,
    base_ref: str,
    *,
    base_sha: str | None = None,
    head_sha: str | None = None,
) -> dict[str, Any]:
    run(["git", "fetch", "origin", base_ref], cwd=root, check=False)
    remote_base_ref = f"origin/{base_ref}"
    remote_base = run(["git", "rev-parse", "--verify", remote_base_ref], cwd=root, check=False)
    comparison_base = remote_base_ref if remote_base.returncode == 0 else base_ref
    ahead = int(run_stdout(["git", "rev-list", "--count", f"{comparison_base}..{head_ref}"], cwd=root) or "0")
    behind = int(run_stdout(["git", "rev-list", "--count", f"{head_ref}..{comparison_base}"], cwd=root) or "0")
    diverged = ahead > 0 and behind > 0
    needs_refresh = behind > 0 or diverged
    return {
        "head_ref": head_ref,
        "base_ref": base_ref,
        "base_sha": base_sha or run_stdout(["git", "rev-parse", comparison_base], cwd=root),
        "head_sha": head_sha or run_stdout(["git", "rev-parse", head_ref], cwd=root),
        "behind_base": behind,
        "ahead_of_base": ahead,
        "diverged": diverged,
        "needs_refresh": needs_refresh,
    }


def classify_pr_lifecycle(pr_state: dict[str, Any]) -> str:
    if not pr_state.get("exists"):
        return "no_pr"
    branch = pr_state["branch_status"]
    checks = pr_state["check_summary"]
    if branch.get("needs_refresh"):
        return "refresh_needed"
    if pr_state.get("is_draft"):
        return "review_repair"
    if checks.get("has_required_failures") or checks.get("has_required_pending"):
        return "review_repair"
    if pr_state.get("mergeable") in {"conflicting", "unknown"}:
        return "review_repair"
    return "review_only"


def inspect_pr_state(root: Path, issue_number: int) -> dict[str, Any]:
    state = ensure_worktree(root, issue_number)
    branch = state["branch"]
    pr_number = current_pr_number(branch)
    if not pr_number:
        return {
            "issue_number": issue_number,
            "pr_number": None,
            "exists": False,
            "url": "",
            "state": "none",
            "is_draft": False,
            "review_decision": "",
            "labels": [],
            "mergeable": "unknown",
            "check_summary": summarize_status_checks([]),
            "branch_status": {
                "head_ref": branch,
                "base_ref": "main",
                "base_sha": "",
                "head_sha": run_stdout(["git", "rev-parse", branch], cwd=root),
                "behind_base": 0,
                "ahead_of_base": 0,
                "diverged": False,
                "needs_refresh": False,
            },
            "lifecycle": "no_pr",
            "ready_for_senior_review": False,
        }

    data = run_json(
        [
            "gh",
            "pr",
            "view",
            str(pr_number),
            "--json",
            "number,url,state,isDraft,reviewDecision,labels,mergeable,headRefName,baseRefName,headRefOid,baseRefOid,statusCheckRollup",
        ]
    )
    labels = [label["name"] for label in data.get("labels", [])]
    branch = branch_status(
        root,
        data.get("headRefName") or state["branch"],
        data.get("baseRefName") or "main",
        base_sha=data.get("baseRefOid"),
        head_sha=data.get("headRefOid"),
    )
    check_summary = summarize_status_checks(data.get("statusCheckRollup") or [])
    normalized = {
        "issue_number": issue_number,
        "pr_number": int(data["number"]),
        "exists": True,
        "url": data.get("url") or "",
        "state": str(data.get("state") or "unknown").lower(),
        "is_draft": bool(data.get("isDraft")),
        "review_decision": str(data.get("reviewDecision") or "").lower(),
        "labels": labels,
        "mergeable": _normalize_mergeable(data.get("mergeable")),
        "check_summary": check_summary,
        "branch_status": branch,
    }
    normalized["lifecycle"] = classify_pr_lifecycle(normalized)
    normalized["ready_for_senior_review"] = normalized["lifecycle"] == "review_only"
    return normalized


def pr_review_state(pr_number: int) -> dict[str, Any]:
    data = run_json(
        [
            "gh",
            "pr",
            "view",
            str(pr_number),
            "--json",
            "labels,reviewDecision,isDraft,state,url,mergeable,statusCheckRollup",
        ]
    )
    data["label_names"] = [label["name"] for label in data.get("labels", [])]
    data["check_summary"] = summarize_status_checks(data.get("statusCheckRollup") or [])
    data["normalized_mergeable"] = _normalize_mergeable(data.get("mergeable"))
    return data


def edit_pr_labels(pr_number: int, *, add: list[str], remove: list[str]) -> None:
    current = set(pr_label_names(pr_number))
    wanted_add = [label for label in add if label not in current]
    wanted_remove = [label for label in remove if label in current]
    if not wanted_add and not wanted_remove:
        return

    command = ["gh", "pr", "edit", str(pr_number)]
    for label in wanted_add:
        command.extend(["--add-label", label])
    for label in wanted_remove:
        command.extend(["--remove-label", label])
    run(command)


def latest_main_ref(root: Path) -> str:
    remote_ref = run(["git", "rev-parse", "--verify", "origin/main"], cwd=root, check=False)
    if remote_ref.returncode == 0:
        return "origin/main"
    return "main"


def list_worktrees(root: Path) -> list[dict[str, str]]:
    output = run_stdout(["git", "worktree", "list", "--porcelain"], cwd=root)
    entries: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            if current:
                entries.append(current)
                current = {}
            continue
        key, _, value = line.partition(" ")
        if not _:
            continue
        current[key] = value
    if current:
        entries.append(current)
    return entries


def worktree_entry_for_branch(root: Path, branch: str) -> dict[str, str] | None:
    target = f"refs/heads/{branch}"
    for entry in list_worktrees(root):
        if entry.get("branch") != target:
            continue
        worktree_path = entry.get("worktree")
        if not worktree_path:
            continue
        return entry
    return None


def worktree_for_branch(root: Path, branch: str) -> Path | None:
    entry = worktree_entry_for_branch(root, branch)
    if entry is None:
        return None
    worktree_path = entry.get("worktree")
    if not worktree_path:
        return None
    resolved = Path(worktree_path).resolve()
    if resolved.exists():
        return resolved
    return None


def worktree_python_env(worktree: Path) -> dict[str, str]:
    venv = worktree / ".venv"
    if os.name == "nt":
        python = venv / "Scripts" / "python.exe"
        bin_dir = venv / "Scripts"
    else:
        python = venv / "bin" / "python"
        bin_dir = venv / "bin"
    if not python.exists() or not bin_dir.exists():
        return {}
    return {
        "worktree_python": str(python.resolve()),
        "worktree_venv": str(venv.resolve()),
        "worktree_bin": str(bin_dir.resolve()),
    }


def classify_worktree_status(worktree: Path) -> dict[str, list[str]]:
    tracked_dirty: list[str] = []
    untracked: list[str] = []
    status = run_stdout(["git", "status", "--porcelain"], cwd=worktree)
    for line in status.splitlines():
        if len(line) < 4:
            continue
        code = line[:2]
        path_text = line[3:].strip() if line[2:3] == " " else line[2:].strip()
        if not path_text:
            continue
        path_name = path_text.split(" -> ")[-1].strip()
        if code == "??":
            untracked.append(path_name)
        else:
            tracked_dirty.append(path_name)
    return {
        "tracked_dirty": sorted(set(tracked_dirty)),
        "untracked": sorted(set(untracked)),
    }


def sanitize_reused_worktree(worktree: Path) -> dict[str, Any]:
    removed_junk = cleanup_worktree_junk(worktree)
    status = classify_worktree_status(worktree)
    tracked_dirty = status["tracked_dirty"]
    unexpected_untracked = [name for name in status["untracked"] if name not in removed_junk]
    if tracked_dirty:
        fail(
            "Refusing to reuse dirty issue worktree with tracked changes: "
            f"{', '.join(tracked_dirty)}. Clean the worktree manually before rerunning prepare."
        )
    if unexpected_untracked:
        fail(
            "Refusing to reuse issue worktree with unexpected untracked files: "
            f"{', '.join(unexpected_untracked)}. Clean the worktree manually before rerunning prepare."
        )
    return {
        "removed_junk": removed_junk,
        "tracked_dirty": tracked_dirty,
        "unexpected_untracked": unexpected_untracked,
    }


def ensure_worktree(root: Path, issue_number: int) -> dict[str, Any]:
    issue = issue_data(issue_number)
    if issue.get("state", "").lower() != "open":
        fail(f"Issue #{issue_number} is not open")

    repo = repo_name()
    branch = issue_branch(issue_number, issue["title"])
    worktree = issue_worktree(root, repo, issue_number, issue["title"])
    reused_existing = False

    run(["git", "fetch", "origin", "main"], cwd=root, check=False)

    if run(["git", "show-ref", "--verify", f"refs/heads/{branch}"], cwd=root, check=False).returncode != 0:
        run(["git", "branch", branch, latest_main_ref(root)], cwd=root)

    attached_worktree = worktree_for_branch(root, branch)
    if attached_worktree is not None:
        worktree = attached_worktree
        reused_existing = True
    elif not worktree.exists():
        attached_entry = worktree_entry_for_branch(root, branch)
        if attached_entry is not None:
            run(["git", "worktree", "prune"], cwd=root)
        attached_worktree = worktree_for_branch(root, branch)
        if attached_worktree is not None:
            worktree = attached_worktree
            reused_existing = True
        else:
            run(["git", "worktree", "add", str(worktree), branch], cwd=root)
    else:
        reused_existing = True

    sanitation = (
        sanitize_reused_worktree(worktree)
        if reused_existing
        else {
            "removed_junk": [],
            "tracked_dirty": [],
            "unexpected_untracked": [],
        }
    )
    if reused_existing:
        if sanitation["removed_junk"]:
            prepare_worktree_status = "reused_junk_cleaned"
        else:
            prepare_worktree_status = "reused_clean"
    else:
        prepare_worktree_status = "created_clean"

    python_env = worktree_python_env(worktree)
    state = update_state(
        root,
        issue_number,
        issue_number=issue_number,
        issue_title=issue["title"],
        issue_url=issue["url"],
        branch=branch,
        worktree_path=str(worktree),
        repo_name=repo,
        worktree_python=python_env.get("worktree_python", ""),
        worktree_venv=python_env.get("worktree_venv", ""),
        worktree_bin=python_env.get("worktree_bin", ""),
        prepare_worktree_status=prepare_worktree_status,
        prepare_removed_junk=sanitation["removed_junk"],
        prepare_tracked_dirty_paths=sanitation["tracked_dirty"],
        prepare_unexpected_untracked_paths=sanitation["unexpected_untracked"],
    )
    return state


def strip_fences(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```") and stripped.endswith("```"):
        lines = stripped.splitlines()
        if len(lines) >= 3:
            return "\n".join(lines[1:-1]).strip()
    return stripped


def extract_json(text: str) -> dict[str, Any]:
    stripped = strip_fences(text)
    match = re.search(r"\{.*\}", stripped, re.DOTALL)
    if not match:
        fail(f"Expected JSON object in model output:\n{stripped}")
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON from model output: {exc}\n{stripped}")


def update_issue_plan(issue_number: int, plan_markdown: str) -> None:
    issue = issue_data(issue_number)
    current_body = issue.get("body") or ""
    plan_section = f"{PLAN_START}\n## Implementation Plan\n\n{plan_markdown.strip()}\n{PLAN_END}"
    pattern = re.compile(rf"{re.escape(PLAN_START)}.*?{re.escape(PLAN_END)}", re.DOTALL)
    if PLAN_START in current_body and PLAN_END in current_body:
        new_body = pattern.sub(plan_section, current_body)
    else:
        suffix = "\n\n" if current_body.strip() else ""
        new_body = f"{current_body.rstrip()}{suffix}{plan_section}\n"

    with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
        tmp.write(new_body)
        tmp_path = tmp.name
    try:
        run(["gh", "issue", "edit", str(issue_number), "--body-file", tmp_path])
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def extract_issue_plan(body: str) -> str:
    match = re.search(rf"{re.escape(PLAN_START)}\s*(.*?)\s*{re.escape(PLAN_END)}", body, re.DOTALL)
    if not match:
        return ""
    return match.group(1).strip()


def strip_issue_plan(body: str) -> str:
    return re.sub(rf"{re.escape(PLAN_START)}.*?{re.escape(PLAN_END)}", "", body, flags=re.DOTALL).strip()


def plan_review_timeout_seconds() -> int:
    raw = os.environ.get("ANTEROOM_LOCAL_PLAN_REVIEW_TIMEOUT_SECONDS", "").strip()
    if not raw:
        return DEFAULT_PLAN_REVIEW_TIMEOUT_SECONDS
    try:
        value = int(raw)
    except ValueError:
        return DEFAULT_PLAN_REVIEW_TIMEOUT_SECONDS
    return value if value > 0 else DEFAULT_PLAN_REVIEW_TIMEOUT_SECONDS


def format_bullets(items: list[str], *, empty: str = "- none") -> str:
    if not items:
        return empty
    return "\n".join(f"- {item}" for item in items)


def assess_existing_work(root: Path, state: dict[str, Any]) -> dict[str, Any]:
    worktree = Path(state["worktree_path"])
    branch = str(state.get("branch", "")).strip()
    run(["git", "fetch", "origin", "main"], cwd=root, check=False)
    base_ref = latest_main_ref(root)
    ahead_count = int(run_stdout(["git", "rev-list", "--count", f"{base_ref}..HEAD"], cwd=worktree) or "0")
    changed_files = [
        line.strip()
        for line in run_stdout(["git", "diff", "--name-only", f"{base_ref}...HEAD"], cwd=worktree).splitlines()
        if line.strip()
    ]
    commit_subjects = [
        line.strip()
        for line in run_stdout(["git", "log", "--format=%s", f"{base_ref}..HEAD"], cwd=worktree).splitlines()
        if line.strip()
    ]
    status = classify_worktree_status(worktree)
    implementation_present = ahead_count > 0 and bool(changed_files)
    return {
        "implementation_present": implementation_present,
        "ahead_of_main": ahead_count,
        "base_ref": base_ref,
        "branch": branch,
        "worktree_clean": not status["tracked_dirty"] and not status["untracked"],
        "tracked_dirty": status["tracked_dirty"],
        "untracked": status["untracked"],
        "changed_files": changed_files,
        "commit_subjects": commit_subjects[:10],
        "changed_test_files": [path for path in changed_files if path.startswith("tests/")],
    }


def build_existing_work_plan(issue_number: int, assessment: dict[str, Any]) -> str:
    changed_files = [str(item) for item in assessment.get("changed_files") or []]
    commit_subjects = [str(item) for item in assessment.get("commit_subjects") or []]
    changed_test_files = [str(item) for item in assessment.get("changed_test_files") or []]
    branch = str(assessment.get("branch", "")).strip() or f"issue-{issue_number}"
    ahead_count = int(assessment.get("ahead_of_main") or 0)
    base_ref = str(assessment.get("base_ref", "origin/main"))
    return f"""
## Summary
Implementation work is already committed on branch `{branch}`. The workflow
should review the current branch state and validate it rather than re-planning
the issue from scratch.

## Existing Branch State
- Branch is ahead of `{base_ref}` by {ahead_count} commit(s).
- Worktree is expected to stay clean while review and validation run.
- Current branch scope should be reviewed against the issue body and
  acceptance criteria, not rediscovered from unrelated repo files.

## Files Already Changed
{format_bullets(changed_files)}

## Commits Already Present
{format_bullets(commit_subjects)}

## Remaining Validation Steps
- Confirm the existing diff still matches the issue goal and current main.
- Run targeted lint and tests for the changed files before the workflow enters full checks.
- Use baseline-aware initial checks to distinguish branch regressions from pre-existing main failures.
- If the branch is still aligned and clean, continue to PR sync/review instead of reopening implementation planning.

## Risks & Considerations
- Existing branch work may have drifted from current `main` and needs a
  focused review of changed files only.
- Validation must stay scoped to the current branch state; reviewers should
  not re-open speculative design work unless the existing implementation is
  misaligned.
- Changed tests currently on the branch:
{format_bullets(changed_test_files, empty="- none")}
""".strip()


def build_claude_plan_prompt(issue_number: int) -> str:
    return f"""
Use Claude's `/plan-work` workflow for GitHub issue #{issue_number}.

Use the worktree path from context. Operate only inside that worktree
when you inspect or edit repository files. Use bash for all GitHub and
git operations.

Match `/plan-work` expectations:
- do vision and scope alignment against VISION.md and CLAUDE.md
- inspect the repository deeply enough to produce a concrete implementation plan
- identify affected files, test coverage needs, and any required docs/config updates
- do not start coding

Required outcome:
- read the issue body and comments
- inspect the repository as needed
- update the issue body plan section between the anteroom markers
- leave the issue with needs-senior-review present and senior-approved removed

Return only markdown for the plan body. Do not include code fences or any
surrounding commentary.

Required sections:
## Summary
## Files to Modify
## Files to Create
## Implementation Steps
## Testing Strategy
## Risks & Considerations
""".strip()


def build_codex_plan_review_prompt(issue_number: int, *, issue_context: str, plan_markdown: str) -> str:
    return f"""
Review GitHub issue #{issue_number} as the senior reviewer for this repository.

Review the proposed plan first, not the whole repository.

Use:
- the issue context below
- the extracted implementation plan below
- VISION.md and CLAUDE.md for policy/alignment

Inspect repository code only if you need to sanity-check a file path or behavior
named in the plan. Do not wander through unrelated code.

Approve only if the plan is implementation-ready with zero blockers.

<issue_context>
{issue_context}
</issue_context>

<implementation_plan>
{plan_markdown}
</implementation_plan>

Return JSON only with this shape:
{{
  "decision": "approve" | "changes_requested",
  "summary": "<one sentence>",
  "comment_markdown": "<markdown comment to post on the issue>"
}}
""".strip()


def build_codex_existing_work_review_prompt(
    issue_number: int,
    *,
    issue_context: str,
    plan_markdown: str,
    assessment: dict[str, Any],
) -> str:
    changed_files = "\n".join(f"- {path}" for path in assessment.get("changed_files") or []) or "- none"
    commit_subjects = "\n".join(f"- {subject}" for subject in assessment.get("commit_subjects") or []) or "- none"
    return f"""
You are an existing-work validator for GitHub issue #{issue_number}. The issue
branch already contains committed implementation work.

This is NOT a fresh-plan review, NOT a senior review, and NOT a full quality
gate. Your sole job is to verify that the existing branch changes are aligned
with the issue and plan, and that the remaining validation path looks viable.

HARD CONSTRAINTS — do NOT do any of the following:
- Do NOT run the test suite, linter, type checker, or any repo-scale validation
- Do NOT execute pytest, ruff, mypy, or similar tools
- Do NOT read or inspect files that are not in the changed-files list below
- Do NOT load or invoke any skills, plugins, or slash commands
- Do NOT perform a senior review or act as a senior reviewer
- Do NOT wander through unrelated code or assess overall repo health

You MAY:
- Read the changed files listed below to verify they match the plan
- Read VISION.md and CLAUDE.md for policy alignment (read-only, do not enforce
  their full checklist — just check for obvious misalignment)
- Use git log/diff to understand the branch changes

<issue_context>
{issue_context}
</issue_context>

<implementation_plan>
{plan_markdown}
</implementation_plan>

<existing_branch_state>
Branch: {assessment.get("branch", "")}
Ahead of {assessment.get("base_ref", "origin/main")}: {assessment.get("ahead_of_main", 0)} commit(s)
Changed files:
{changed_files}

Existing commit subjects:
{commit_subjects}
</existing_branch_state>

Approve if the branch changes are aligned with the issue and the remaining path
is viable. Request changes only if there is a clear misalignment or blocker.

Return JSON only with this shape:
{{
  "decision": "approve" | "changes_requested",
  "summary": "<one sentence>",
  "comment_markdown": "<markdown comment to post on the issue>"
}}
""".strip()


def build_claude_implement_prompt(issue_number: int) -> str:
    return f"""
Implement GitHub issue #{issue_number} in the prepared worktree from context.

Use bash for all repository actions. Keep work scoped to the approved plan
and stop once the branch is ready for the workflow's `/submit-pr` quality
gate.

Match `/submit-pr` expectations while implementing:
- keep tests and docs aligned with any user-visible behavior change
- leave the branch in a state that should pass lint, tests, and other repo checks
- do not create the PR yourself; the workflow handles sync and PR creation

Return a short change summary.
""".strip()


def build_codex_pr_review_prompt(pr_number: int) -> str:
    return f"""
Review GitHub PR #{pr_number} as the senior reviewer for this repository.

Use the PR, linked issue, PR review history, VISION.md, CLAUDE.md, and relevant
code. Approve only if there are zero blockers.

Return JSON only with this shape:
{{
  "decision": "approve" | "changes_requested",
  "summary": "<one sentence>",
  "comment_markdown": "<markdown review body>"
}}
""".strip()


def build_claude_pr_fix_prompt(pr_number: int, *, review_context: str = "") -> str:
    context_block = ""
    if review_context.strip():
        trimmed = review_context.strip()[-8000:]
        context_block = f"""

<senior_review_feedback>
{trimmed}
</senior_review_feedback>
"""

    return f"""
Address the latest requested changes for the PR tied to GitHub PR #{pr_number}.

Use the worktree path from context. Use bash for repository and GitHub
operations. If the PR is already senior-approved or there are no
actionable findings, do nothing and say "no changes were needed".

Work to Claude's `/submit-pr` quality bar:
- fix only the unresolved blockers
- keep tests, docs, and validation aligned with the actual shipped behavior
- leave the branch in a state that should pass `/submit-pr --checks-only`
- leave the branch ready for another senior-review pass

Focus on the senior-review feedback below. Keep the fix scoped to
actual blockers. Before returning, run the smallest targeted validation
needed to prove the blockers are fixed.
{context_block}
Keep this run in PR-repair scope only:
- fix only unresolved review blockers or failing-check fallout
- do not reopen issue planning
- do not reshape the overall implementation approach unless the blocker requires it

If you find junk untracked files with names like `<MagicMock ...>`,
remove them with `rm -f -- <path>`, not `git rm`.

Return a short summary of the changes you made, or that no changes were needed.
""".strip()


def build_claude_fix_checks_prompt(issue_number: int, *, mode: str, failure_context: str = "") -> str:
    mode_context = {
        "initial": ("The initial checks (lint + tests) failed for issue"),
        "post-review": ("Post-review checks failed for issue"),
        "refresh": ("The PR refresh checks failed for issue"),
    }
    context_line = mode_context.get(mode, f"Checks failed (mode={mode}) for issue")

    context_block = ""
    if failure_context.strip():
        trimmed = failure_context.strip()[-8000:]
        context_block = f"""

<failed_checks_output>
{trimmed}
</failed_checks_output>
"""

    return f"""
{context_line} #{issue_number}.
Fix them to the same quality bar expected by Claude's `/submit-pr` workflow.

Use the worktree path from context and operate only inside that worktree.
The source of truth is the failed checks output below, not the issue title,
touched files, or the part of the codebase you were already editing.
Start with the exact first failing test, assertion, and first
repository traceback frame from the failed checks output. If the
failure points outside the files already changed in the branch, follow
the failure signal anyway.
{context_block}
Do not assume the failing code is in the issue's main implementation
area. Only inspect unrelated workflow/helper files if the failing test
or traceback points there directly.

A cheap Ruff autofix step has already run before you. Assume any
remaining failure needs an actual code or test change. Run the smallest
targeted validation needed while you work, and leave the branch ready
for the next full checks round in this workflow. Do not run broad
repo-wide checks here like `python -m pytest -q`, `pytest` on the whole
suite, or `ruff check src/ tests/`; the workflow reruns the full checks
after this step.

If you find junk untracked files with names like `<MagicMock ...>`,
remove them with `rm -f -- <path>`, not `git rm`.

Only fix what is broken -- do not refactor or add features.

Return only a short markdown change summary.
""".strip()


def build_claude_refresh_pr_prompt(issue_number: int) -> str:
    return f"""
Refresh the existing PR branch for GitHub issue #{issue_number} so it is
current and mergeable again.

Use the worktree path from context and operate only inside that worktree.
Use bash for git and GitHub operations.

This workflow is for PR refresh only:
- update the branch against the current base branch
- resolve merge conflicts if present
- fix any breakage introduced by the refresh
- do not reopen issue planning
- do not run senior review yourself

Before returning, run only the smallest targeted validation needed to
prove the branch is refreshed and stable. The workflow runs formal checks
afterward.

Return a short summary of what you refreshed and any conflicts you resolved.
""".strip()


def run_streaming(
    command: list[str],
    *,
    cwd: Path | None = None,
) -> str:
    """Run a command and stream its stdout line-by-line to our stdout.

    Returns the full captured output as a string. Each line is printed
    with flush=True so the parent runner's async line reader picks it up
    immediately for real-time transcript display.
    """
    proc = subprocess.Popen(
        command,
        cwd=str(cwd) if cwd else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
        text=True,
        bufsize=1,
    )
    lines: list[str] = []
    assert proc.stdout is not None
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        stripped = line.rstrip("\n")
        lines.append(stripped)
        print(stripped, flush=True)

    proc.wait()
    stderr = proc.stderr.read() if proc.stderr else ""

    if proc.returncode != 0:
        cmd = " ".join(command)
        detail = stderr.strip() or f"exit code {proc.returncode}"
        fail(f"Command failed: {cmd}\n{detail}", code=proc.returncode or 1)

    return "\n".join(lines).strip()


def _consume_text_chunks(
    buffer: str,
    text: str,
    *,
    soft_limit: int = STREAM_SOFT_LIMIT,
    final: bool = False,
) -> tuple[list[str], str]:
    """Convert partial model text into printable transcript lines.

    Claude's stream-json output arrives as arbitrary text deltas, not
    line-buffered CLI output. Emit completed lines immediately, and emit
    shorter soft-wrapped chunks once the buffer grows so the operator sees
    progress before the model inserts a newline.
    """
    pending = buffer + text
    emitted: list[str] = []

    while True:
        newline_at = pending.find("\n")
        if newline_at != -1:
            line = pending[:newline_at].rstrip("\r").strip()
            pending = pending[newline_at + 1 :]
            if line:
                emitted.append(line)
            continue

        if len(pending) < soft_limit:
            break

        cut = max(
            pending.rfind(". ", 0, soft_limit + 1),
            pending.rfind("! ", 0, soft_limit + 1),
            pending.rfind("? ", 0, soft_limit + 1),
            pending.rfind("; ", 0, soft_limit + 1),
            pending.rfind(", ", 0, soft_limit + 1),
            pending.rfind(" ", 0, soft_limit + 1),
        )
        if cut <= 0:
            cut = soft_limit
        else:
            cut += 1

        line = pending[:cut].strip()
        pending = pending[cut:].lstrip()
        if line:
            emitted.append(line)

    if final:
        tail = pending.strip()
        if tail:
            emitted.append(tail)
        pending = ""

    return emitted, pending


def _spawn_text_subprocess(
    command: list[str],
    *,
    cwd: Path | None = None,
    own_process_group: bool = False,
) -> subprocess.Popen[str]:
    """Start a text subprocess with line-buffered pipes."""
    popen_kwargs: dict[str, Any] = {
        "cwd": str(cwd) if cwd else None,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "stdin": subprocess.DEVNULL,
        "text": True,
        "bufsize": 1,
    }
    if own_process_group:
        if os.name != "nt":
            popen_kwargs["start_new_session"] = True
        else:
            popen_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    return subprocess.Popen(command, **popen_kwargs)


def _forward_stderr(stream: Any, sink: list[str]) -> None:
    """Drain stderr incrementally so child processes cannot block on writes."""
    if stream is None:
        return
    while True:
        line = stream.readline()
        if not line:
            break
        stripped = line.rstrip("\n")
        sink.append(stripped)
        if stripped:
            print(stripped, file=sys.stderr, flush=True)


def claude_once(prompt: str, *, cwd: Path) -> str:
    """Run Claude CLI and stream assistant text in real-time.

    Uses ``--output-format stream-json --include-partial-messages`` so
    token-level ``content_block_delta`` events stream as they're generated,
    instead of buffering until the process exits (plain ``claude -p``).
    """
    proc = _spawn_text_subprocess(
        [
            "claude",
            "-p",
            "--verbose",
            "--output-format",
            "stream-json",
            "--include-partial-messages",
            "--permission-mode",
            "bypassPermissions",
            "--",
            prompt,
        ],
        cwd=cwd,
    )
    result_text = ""
    line_buf = ""
    last_assistant_text = ""
    stderr_lines: list[str] = []
    stderr_thread = threading.Thread(target=_forward_stderr, args=(proc.stderr, stderr_lines), daemon=True)
    stderr_thread.start()
    assert proc.stdout is not None
    while True:
        raw = proc.stdout.readline()
        if not raw:
            break
        raw = raw.strip()
        if not raw:
            continue
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            continue
        etype = event.get("type", "")
        if etype == "stream_event":
            inner = event.get("event", {})
            if inner.get("type") == "content_block_delta":
                text = inner.get("delta", {}).get("text", "")
                if text:
                    emitted, line_buf = _consume_text_chunks(line_buf, text)
                    for line_out in emitted:
                        print(line_out, flush=True)
        elif etype == "assistant":
            message = event.get("message", {})
            content = message.get("content", [])
            text_parts = [
                str(part.get("text", "")).strip()
                for part in content
                if isinstance(part, dict) and part.get("type") == "text" and str(part.get("text", "")).strip()
            ]
            if text_parts:
                last_assistant_text = "\n".join(text_parts)
                for line_out in _consume_text_chunks("", last_assistant_text, final=True)[0]:
                    print(line_out, flush=True)
        elif etype == "result":
            result_text = str(event.get("result", "")).strip()

    proc.wait()
    stderr_thread.join()
    for line_out in _consume_text_chunks(line_buf, "", final=True)[0]:
        print(line_out, flush=True)
    if proc.returncode != 0:
        stderr = "\n".join(line for line in stderr_lines if line).strip()
        detail = result_text or last_assistant_text or stderr or f"exit code {proc.returncode}"
        fail(f"Claude CLI failed: {detail}")

    return result_text


class CodexRunResult:
    def __init__(self, text: str, timed_out: bool = False, stderr: str = "", exit_code: int = 0) -> None:
        self.text = text
        self.timed_out = timed_out
        self.stderr = stderr
        self.exit_code = exit_code


def _terminate_process_group(proc: subprocess.Popen[str]) -> None:
    try:
        if os.name != "nt":
            os.killpg(proc.pid, signal.SIGKILL)
        else:
            proc.kill()
    except ProcessLookupError:
        pass


def codex_once(
    prompt: str,
    *,
    cwd: Path,
    timeout_seconds: int = 120,
    extra_flags: list[str] | None = None,
) -> CodexRunResult:
    cmd = [
        "codex",
        "exec",
        "--json",
        "--color",
        "never",
        "--dangerously-bypass-approvals-and-sandbox",
    ]
    if extra_flags:
        cmd.extend(extra_flags)
    cmd.extend(["--", prompt])
    proc = _spawn_text_subprocess(
        cmd,
        cwd=cwd,
        own_process_group=True,
    )
    stderr_lines: list[str] = []
    stderr_thread = threading.Thread(target=_forward_stderr, args=(proc.stderr, stderr_lines), daemon=True)
    stderr_thread.start()

    final_text = ""
    timed_out = False
    deadline = time.monotonic() + timeout_seconds
    stdout_queue: Queue[str | None] = Queue()

    def forward_stdout(stream: Any, sink: Queue[str | None]) -> None:
        if stream is None:
            sink.put(None)
            return
        while True:
            line = stream.readline()
            if not line:
                sink.put(None)
                break
            sink.put(line)

    stdout_thread = threading.Thread(target=forward_stdout, args=(proc.stdout, stdout_queue), daemon=True)
    stdout_thread.start()
    stdout_closed = False

    while True:
        if time.monotonic() >= deadline:
            timed_out = True
            print(f"Codex review timed out after {timeout_seconds}s; terminating process.", flush=True)
            _terminate_process_group(proc)
            break

        try:
            raw = stdout_queue.get(timeout=0.1)
        except Empty:
            if proc.poll() is not None and stdout_closed:
                break
            continue

        if raw is None:
            stdout_closed = True
            if proc.poll() is not None:
                break
            continue

        raw = raw.strip()
        if not raw:
            continue
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            continue

        etype = event.get("type", "")
        item = event.get("item", {})
        item_type = item.get("type", "")

        if etype == "item.started" and item_type == "command_execution":
            command = str(item.get("command", "")).strip()
            if command:
                print(f"[command] {command}", flush=True)
            continue

        if etype != "item.completed":
            continue

        if item_type == "agent_message":
            text = str(item.get("text", "")).strip()
            if text:
                final_text = text
                for line in text.splitlines():
                    line = line.strip()
                    if line:
                        print(line, flush=True)
        elif item_type == "command_execution":
            output = str(item.get("aggregated_output", "")).strip()
            if output:
                for line in output.splitlines():
                    line = line.strip()
                    if line:
                        print(line, flush=True)

    if timed_out and proc.poll() is None:
        proc.wait()
    elif proc.poll() is None:
        proc.wait()
    stdout_thread.join()
    stderr_thread.join()
    stderr = "\n".join(line for line in stderr_lines if line).strip()
    if timed_out:
        return CodexRunResult(text=final_text, timed_out=True, stderr=stderr, exit_code=124)
    if proc.returncode != 0:
        return CodexRunResult(text=final_text, stderr=stderr, exit_code=proc.returncode)
    return CodexRunResult(text=final_text, stderr=stderr, exit_code=0)


def current_pr_number(branch: str) -> int | None:
    output = run_stdout(
        [
            "gh",
            "pr",
            "list",
            "--head",
            branch,
            "--json",
            "number",
            "--jq",
            ".[0].number // empty",
        ]
    )
    return int(output) if output else None


def cleanup_worktree_junk(worktree: Path) -> list[str]:
    """Remove known bogus transient files that should never be committed.

    The local issue workflow occasionally encounters root-level files with
    names like ``<MagicMock ...>`` created by buggy test paths or mock path
    coercion. They are not source files, but they do pollute ``git status`` and
    can distract the fix loop into invalid commands like ``git rm`` on
    untracked files.
    """
    removed: list[str] = []
    for pattern in WORKTREE_JUNK_GLOBS:
        for path in worktree.glob(pattern):
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
            except FileNotFoundError:
                continue
            removed.append(path.name)
    return sorted(removed)


def commit_and_push(state: dict[str, Any], *, mode: str) -> bool:
    worktree = Path(state["worktree_path"])
    branch = state["branch"]
    issue_number = int(state["issue_number"])
    issue_title = state.get("issue_title", f"issue-{issue_number}")

    removed = cleanup_worktree_junk(worktree)
    if removed:
        print(f"removed_junk: {', '.join(removed)}")

    status = run_stdout(["git", "status", "--porcelain"], cwd=worktree)
    if not status:
        return False

    if mode == "initial":
        subject = f"feat: implement #{issue_number} {issue_title}"
    else:
        subject = f"fix: address senior review for #{issue_number}"
    run(["git", "add", "-A"], cwd=worktree)
    run(["git", "commit", "-m", subject], cwd=worktree)
    run(["git", "push", "-u", "origin", branch], cwd=worktree)
    return True


def checks_command() -> str:
    return os.environ.get("ANTEROOM_LOCAL_CHECKS", DEFAULT_CHECKS)


def autofix_command() -> str:
    return os.environ.get("ANTEROOM_LOCAL_AUTOFIX", DEFAULT_AUTOFIX)


def run_checks(
    state: dict[str, Any], *, mode: str, allow_baseline: bool = False, root: Path | None = None
) -> tuple[int, str]:
    """Run checks and return ``(returncode, output)``.

    Returns the combined stdout+stderr from the checks command together
    with the process exit code so the caller can persist the output to
    workflow state before deciding how to handle the failure.
    """
    if mode == "post-review" and state.get("last_pr_review_decision") != "changes_requested":
        print("no_checks_needed")
        return 0, ""

    worktree = Path(state["worktree_path"])
    stage_result = run_check_stages(worktree, state=state, allow_baseline=allow_baseline)
    output = stage_result["output"]
    if allow_baseline:
        if root is None:
            fail("root is required for baseline-aware checks")
        baseline = state.get("checks_baseline") or {}
        if not baseline:
            fail("Missing baseline capture; run capture-baseline before baseline-aware checks")
        success, summary = compare_against_baseline(stage_result, baseline)
        if output.strip():
            print(output.strip())
        print(summary)
        return (0 if success else 1), "\n".join(filter(None, [output, summary]))

    if output.strip():
        print(output.strip())
    if stage_result["returncode"] == 0:
        print("checks_passed")
    return stage_result["returncode"], output


def run_autofix(state: dict[str, Any], *, mode: str) -> None:
    if mode == "post-review" and state.get("last_pr_review_decision") != "changes_requested":
        print("no_autofix_needed")
        return

    worktree = Path(state["worktree_path"])
    removed_before = cleanup_worktree_junk(worktree)
    if removed_before:
        print(f"removed_junk: {', '.join(removed_before)}")

    command = autofix_command()
    print(f"autofix_command: {command}")
    env = os.environ.copy()
    env[WORKTREE_PYTHON_ENV] = resolve_worktree_python(env, state)
    try:
        proc = subprocess.run(command, cwd=str(worktree), shell=True, text=True, env=env, stdin=subprocess.DEVNULL)
    finally:
        removed_after = cleanup_worktree_junk(worktree)
        if removed_after:
            print(f"removed_junk: {', '.join(removed_after)}")

    if proc.returncode == 0:
        print("autofix_applied")
    else:
        print(f"autofix_incomplete: exit {proc.returncode}")


def post_issue_comment(issue_number: int, body: str) -> None:
    with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
        tmp.write(body.strip() + "\n")
        tmp_path = tmp.name
    try:
        run(["gh", "issue", "comment", str(issue_number), "--body-file", tmp_path])
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def post_pr_review(pr_number: int, decision: str, body: str) -> None:
    with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
        tmp.write(body.strip() + "\n")
        tmp_path = tmp.name
    try:
        if decision == "approve":
            run(["gh", "pr", "review", str(pr_number), "--approve", "--body-file", tmp_path], check=False)
        else:
            run(["gh", "pr", "review", str(pr_number), "--request-changes", "--body-file", tmp_path], check=False)
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def ensure_pr_number(root: Path, issue_number: int) -> int:
    state = load_state(root, issue_number)
    pr_number = state.get("pr_number")
    if pr_number:
        return int(pr_number)
    branch = state.get("branch")
    if not branch:
        fail("Missing branch in workflow state. Run prepare first.")
    found = current_pr_number(branch)
    if not found:
        fail("No PR found for the current issue branch")
    update_state(root, issue_number, pr_number=found)
    return found


def cmd_prepare(args: argparse.Namespace) -> int:
    root = git_root()
    ensure_labels()
    state = ensure_worktree(root, args.issue)
    print(state["worktree_path"])
    status = str(state.get("prepare_worktree_status", "")).strip() or "unknown"
    removed_junk = state.get("prepare_removed_junk") or []
    removed_junk_text = ", ".join(str(item) for item in removed_junk) if removed_junk else "none"
    print(f"prepare_worktree: {status} (removed_junk: {removed_junk_text})", file=sys.stderr)
    return 0


def cmd_capture_baseline(args: argparse.Namespace) -> int:
    root = git_root()
    state = ensure_worktree(root, args.issue)
    baseline = capture_baseline(state, root=root)
    update_state(root, args.issue, checks_baseline=baseline)
    print("baseline_captured")
    return 0


def cmd_assess_existing_work(args: argparse.Namespace) -> int:
    root = git_root()
    state = ensure_worktree(root, args.issue)
    assessment = assess_existing_work(root, state)
    update_state(root, args.issue, existing_work_assessment=assessment)
    token = "existing_work_present" if assessment["implementation_present"] else "no_existing_work"
    print(token)
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    root = git_root()
    state = ensure_worktree(root, args.issue)
    worktree = Path(state["worktree_path"])
    plan = strip_fences(claude_once(build_claude_plan_prompt(args.issue), cwd=worktree))
    update_issue_plan(args.issue, plan)
    edit_issue_labels(args.issue, add=["needs-senior-review"], remove=["senior-approved"])
    update_state(root, args.issue, last_plan_review_decision="pending")
    print("plan_updated")
    return 0


def cmd_plan_existing_work(args: argparse.Namespace) -> int:
    root = git_root()
    state = ensure_worktree(root, args.issue)
    assessment = state.get("existing_work_assessment") or assess_existing_work(root, state)
    if not assessment.get("implementation_present"):
        fail("Existing-work plan requested but no committed branch work was detected")
    plan = build_existing_work_plan(args.issue, assessment)
    update_issue_plan(args.issue, plan)
    edit_issue_labels(args.issue, add=["needs-senior-review"], remove=["senior-approved"])
    update_state(root, args.issue, existing_work_assessment=assessment, last_plan_review_decision="pending")
    print("existing_work_plan_updated")
    return 0


def cmd_review_plan(args: argparse.Namespace) -> int:
    root = git_root()
    state = ensure_worktree(root, args.issue)
    worktree = Path(state["worktree_path"])
    issue = issue_data(args.issue)
    plan_markdown = extract_issue_plan(issue.get("body") or "")
    if not plan_markdown:
        edit_issue_labels(args.issue, add=["needs-senior-review"], remove=["senior-approved"])
        update_state(
            root,
            args.issue,
            last_plan_review_decision="review_failed",
            last_plan_review_failure="missing_plan",
            last_plan_review_error="Issue body has no plan markers to review.",
        )
        print("review_failed: No plan markers found in issue body")
        return 2

    issue_context = strip_issue_plan(issue.get("body") or "")
    timeout = plan_review_timeout_seconds()
    codex_result = codex_once(
        build_codex_plan_review_prompt(args.issue, issue_context=issue_context, plan_markdown=plan_markdown),
        cwd=worktree,
        timeout_seconds=timeout,
    )
    if codex_result.timed_out:
        edit_issue_labels(args.issue, add=["needs-senior-review"], remove=["senior-approved"])
        update_state(
            root,
            args.issue,
            last_plan_review_decision="review_failed",
            last_plan_review_failure="timed_out",
            last_plan_review_error=_timeout_error_message(timeout, codex_result.stderr),
        )
        print("review_failed: Codex plan review timed out")
        return 2
    if codex_result.exit_code != 0:
        edit_issue_labels(args.issue, add=["needs-senior-review"], remove=["senior-approved"])
        runner_error = codex_result.stderr or f"exit code {codex_result.exit_code}"
        update_state(
            root,
            args.issue,
            last_plan_review_decision="review_failed",
            last_plan_review_failure="runner_error",
            last_plan_review_error=runner_error[:500],
        )
        print(f"review_failed: Codex plan review failed ({runner_error})")
        return 2

    try:
        review = extract_json(codex_result.text)
    except SystemExit:
        edit_issue_labels(args.issue, add=["needs-senior-review"], remove=["senior-approved"])
        update_state(
            root,
            args.issue,
            last_plan_review_decision="review_failed",
            last_plan_review_failure="invalid_output",
            last_plan_review_error=(codex_result.text or codex_result.stderr or "missing review JSON")[:500],
        )
        print("review_failed: Codex plan review returned invalid output")
        return 2

    decision = str(review.get("decision", "")).strip()
    summary = str(review.get("summary", "")).strip() or "Plan review completed."
    comment = str(review.get("comment_markdown", "")).strip() or summary
    if decision not in {"approve", "changes_requested"}:
        edit_issue_labels(args.issue, add=["needs-senior-review"], remove=["senior-approved"])
        update_state(
            root,
            args.issue,
            last_plan_review_decision="review_failed",
            last_plan_review_failure="unexpected_decision",
            last_plan_review_error=decision[:500],
        )
        print(f"review_failed: Unexpected plan review decision: {decision!r}")
        return 2

    post_issue_comment(args.issue, comment)
    if decision == "approve":
        edit_issue_labels(args.issue, add=["senior-approved"], remove=["needs-senior-review"])
        update_state(root, args.issue, last_plan_review_decision="approve", last_plan_review_failure="")
        print("approved")
        return 0

    edit_issue_labels(args.issue, add=["needs-senior-review"], remove=["senior-approved"])
    update_state(root, args.issue, last_plan_review_decision="changes_requested", last_plan_review_failure="")
    print("needs_changes")
    return 1


def cmd_review_existing_work(args: argparse.Namespace) -> int:
    root = git_root()
    state = ensure_worktree(root, args.issue)
    worktree = Path(state["worktree_path"])
    assessment = state.get("existing_work_assessment") or assess_existing_work(root, state)
    if not assessment.get("implementation_present"):
        fail("Existing-work review requested but no committed branch work was detected")
    issue = issue_data(args.issue)
    plan_markdown = extract_issue_plan(issue.get("body") or "")
    if not plan_markdown:
        edit_issue_labels(args.issue, add=["needs-senior-review"], remove=["senior-approved"])
        update_state(
            root,
            args.issue,
            last_plan_review_decision="review_failed",
            last_plan_review_failure="missing_plan",
            last_plan_review_error="Issue body has no plan markers to review.",
        )
        print("review_failed: No plan markers found in issue body")
        return 2

    timeout = plan_review_timeout_seconds()
    codex_result = codex_once(
        build_codex_existing_work_review_prompt(
            args.issue,
            issue_context=strip_issue_plan(issue.get("body") or ""),
            plan_markdown=plan_markdown,
            assessment=assessment,
        ),
        cwd=worktree,
        timeout_seconds=timeout,
        extra_flags=["--disable", "plugins"],
    )
    if codex_result.timed_out:
        edit_issue_labels(args.issue, add=["needs-senior-review"], remove=["senior-approved"])
        update_state(
            root,
            args.issue,
            last_plan_review_decision="review_failed",
            last_plan_review_failure="timed_out",
            last_plan_review_error=_timeout_error_message(timeout, codex_result.stderr),
        )
        print("review_failed: Codex existing-work review timed out")
        return 2
    if codex_result.exit_code != 0:
        edit_issue_labels(args.issue, add=["needs-senior-review"], remove=["senior-approved"])
        runner_error = codex_result.stderr or f"exit code {codex_result.exit_code}"
        update_state(
            root,
            args.issue,
            last_plan_review_decision="review_failed",
            last_plan_review_failure="runner_error",
            last_plan_review_error=runner_error[:500],
        )
        print(f"review_failed: Codex existing-work review failed ({runner_error})")
        return 2

    try:
        review = extract_json(codex_result.text)
    except SystemExit:
        edit_issue_labels(args.issue, add=["needs-senior-review"], remove=["senior-approved"])
        update_state(
            root,
            args.issue,
            last_plan_review_decision="review_failed",
            last_plan_review_failure="invalid_output",
            last_plan_review_error=(codex_result.text or codex_result.stderr or "missing review JSON")[:500],
        )
        print("review_failed: Codex existing-work review returned invalid output")
        return 2

    decision = str(review.get("decision", "")).strip()
    summary = str(review.get("summary", "")).strip() or "Existing branch review completed."
    comment = str(review.get("comment_markdown", "")).strip() or summary
    if decision not in {"approve", "changes_requested"}:
        edit_issue_labels(args.issue, add=["needs-senior-review"], remove=["senior-approved"])
        update_state(
            root,
            args.issue,
            last_plan_review_decision="review_failed",
            last_plan_review_failure="unexpected_decision",
            last_plan_review_error=decision[:500],
        )
        print(f"review_failed: Unexpected existing-work review decision: {decision!r}")
        return 2

    post_issue_comment(args.issue, comment)
    if decision == "approve":
        edit_issue_labels(args.issue, add=["senior-approved"], remove=["needs-senior-review"])
        update_state(root, args.issue, last_plan_review_decision="approve", last_plan_review_failure="")
        print("approved")
        return 0

    edit_issue_labels(args.issue, add=["needs-senior-review"], remove=["senior-approved"])
    update_state(root, args.issue, last_plan_review_decision="changes_requested", last_plan_review_failure="")
    print("needs_changes")
    return 1


def cmd_implement(args: argparse.Namespace) -> int:
    root = git_root()
    state = ensure_worktree(root, args.issue)
    worktree = Path(state["worktree_path"])
    summary = strip_fences(claude_once(build_claude_implement_prompt(args.issue), cwd=worktree))
    update_state(root, args.issue, implementation_summary=summary)
    print(summary or "implementation_done")
    return 0


def cmd_checks(args: argparse.Namespace) -> int:
    root = git_root()
    state = ensure_worktree(root, args.issue)
    returncode, output = run_checks(
        state,
        mode=args.mode,
        allow_baseline=bool(getattr(args, "allow_baseline", False)),
        root=root,
    )
    update_state(root, args.issue, last_checks_output=output)
    if returncode != 0:
        raise SystemExit(returncode)
    return 0


def cmd_autofix(args: argparse.Namespace) -> int:
    root = git_root()
    state = ensure_worktree(root, args.issue)
    run_autofix(state, mode=args.mode)
    return 0


def cmd_sync(args: argparse.Namespace) -> int:
    root = git_root()
    state = ensure_worktree(root, args.issue)
    changed = commit_and_push(state, mode=args.mode)
    print("synced" if changed else "no_changes")
    return 0


def cmd_open_pr(args: argparse.Namespace) -> int:
    root = git_root()
    state = ensure_worktree(root, args.issue)
    branch = state["branch"]
    existing = current_pr_number(branch)
    if existing:
        update_state(root, args.issue, pr_number=existing)
        print(existing)
        return 0

    title = f"feat: implement #{args.issue} {state['issue_title']}"
    body = f"Implements #{args.issue}\n\nGenerated by the local Claude/Codex workflow."
    output = run_stdout(
        [
            "gh",
            "pr",
            "create",
            "--head",
            branch,
            "--title",
            title,
            "--body",
            body,
        ]
    )
    pr_number = current_pr_number(branch)
    if not pr_number:
        fail(f"PR create returned output but no PR number was found:\n{output}")
    update_state(root, args.issue, pr_number=pr_number)
    print(pr_number)
    return 0


def cmd_ready_pr(args: argparse.Namespace) -> int:
    root = git_root()
    pr_number = ensure_pr_number(root, args.issue)
    review_state = pr_review_state(pr_number)
    if review_state.get("isDraft"):
        run(["gh", "pr", "ready", str(pr_number)], check=False)
        print("ready")
        return 0
    print("already_ready")
    return 0


def cmd_review_pr(args: argparse.Namespace) -> int:
    root = git_root()
    state = ensure_worktree(root, args.issue)
    worktree = Path(state["worktree_path"])
    pr_number = ensure_pr_number(root, args.issue)
    codex_result = codex_once(build_codex_pr_review_prompt(pr_number), cwd=worktree)
    if codex_result.timed_out:
        edit_pr_labels(pr_number, add=["needs-senior-review"], remove=["senior-approved"])
        update_state(
            root,
            args.issue,
            last_pr_review_decision="review_failed",
            last_pr_review_failure="timed_out",
            last_pr_review_error=(codex_result.stderr or "Timed out during PR review")[:500],
        )
        print("review_failed: Codex PR review timed out")
        return 2
    if codex_result.exit_code != 0:
        edit_pr_labels(pr_number, add=["needs-senior-review"], remove=["senior-approved"])
        update_state(
            root,
            args.issue,
            last_pr_review_decision="review_failed",
            last_pr_review_failure="runner_error",
            last_pr_review_error=(codex_result.stderr or f"exit code {codex_result.exit_code}")[:500],
        )
        print(f"review_failed: Codex PR review failed ({codex_result.stderr or f'exit code {codex_result.exit_code}'})")
        return 2

    try:
        review = extract_json(codex_result.text)
    except SystemExit:
        edit_pr_labels(pr_number, add=["needs-senior-review"], remove=["senior-approved"])
        update_state(
            root,
            args.issue,
            last_pr_review_decision="review_failed",
            last_pr_review_failure="invalid_output",
            last_pr_review_error=(codex_result.text or codex_result.stderr or "missing review JSON")[:500],
        )
        print("review_failed: Codex PR review returned invalid output")
        return 2

    decision = str(review.get("decision", "")).strip()
    summary = str(review.get("summary", "")).strip() or "PR review completed."
    comment = str(review.get("comment_markdown", "")).strip() or summary
    if decision not in {"approve", "changes_requested"}:
        edit_pr_labels(pr_number, add=["needs-senior-review"], remove=["senior-approved"])
        update_state(
            root,
            args.issue,
            last_pr_review_decision="review_failed",
            last_pr_review_failure="unexpected_decision",
            last_pr_review_error=decision[:500],
        )
        print(f"review_failed: Unexpected PR review decision: {decision!r}")
        return 2

    post_pr_review(pr_number, decision, comment)
    if decision == "approve":
        edit_pr_labels(pr_number, add=["senior-approved"], remove=["needs-senior-review"])
        update_state(root, args.issue, last_pr_review_decision="approve", last_pr_review_failure="")
        print("approved")
        return 0

    edit_pr_labels(pr_number, add=["needs-senior-review"], remove=["senior-approved"])
    update_state(
        root,
        args.issue,
        last_pr_review_decision="changes_requested",
        last_pr_review_failure="",
        last_pr_review_comment=comment[:8000],
    )
    print("needs_changes")
    return 1


def cmd_fix_pr(args: argparse.Namespace) -> int:
    root = git_root()
    state = ensure_worktree(root, args.issue)
    if state.get("last_pr_review_decision") != "changes_requested":
        print("no_fix_needed")
        return 0

    worktree = Path(state["worktree_path"])
    pr_number = ensure_pr_number(root, args.issue)
    review_context = str(state.get("last_pr_review_comment", ""))
    summary = strip_fences(
        claude_once(
            build_claude_pr_fix_prompt(pr_number, review_context=review_context),
            cwd=worktree,
        )
    )
    update_state(root, args.issue, last_pr_fix_summary=summary)
    print(summary or "fixes_applied")
    return 0


def cmd_fix_checks(args: argparse.Namespace) -> int:
    root = git_root()
    state = ensure_worktree(root, args.issue)
    worktree = Path(state["worktree_path"])
    failure_context = str(state.get("last_checks_output", ""))
    prompt = build_claude_fix_checks_prompt(args.issue, mode=args.mode, failure_context=failure_context)
    summary = strip_fences(claude_once(prompt, cwd=worktree))
    update_state(root, args.issue, last_fix_checks_summary=summary)
    print(summary or "fixes_applied")
    return 0


def cmd_refresh_pr(args: argparse.Namespace) -> int:
    root = git_root()
    state = ensure_worktree(root, args.issue)
    worktree = Path(state["worktree_path"])
    summary = strip_fences(claude_once(build_claude_refresh_pr_prompt(args.issue), cwd=worktree))
    update_state(root, args.issue, last_refresh_pr_summary=summary)
    print(summary or "refresh_done")
    return 0


def cmd_inspect_pr(args: argparse.Namespace) -> int:
    root = git_root()
    state = inspect_pr_state(root, args.issue)
    print(json.dumps(state, sort_keys=True))
    return 0


def cmd_assert_pr_fresh(args: argparse.Namespace) -> int:
    root = git_root()
    state = inspect_pr_state(root, args.issue)
    if not state["exists"]:
        fail(f"Issue #{args.issue} has no PR to check for freshness")
    branch = state["branch_status"]
    if branch["needs_refresh"]:
        fail(
            f"PR #{state['pr_number']} needs refresh "
            f"(behind_base: {branch['behind_base']}; "
            f"ahead_of_base: {branch['ahead_of_base']}; diverged: {branch['diverged']})"
        )
    print("fresh")
    return 0


def cmd_assert_pr_mergeable(args: argparse.Namespace) -> int:
    root = git_root()
    state = inspect_pr_state(root, args.issue)
    if not state["exists"]:
        fail(f"Issue #{args.issue} has no PR to check for mergeability")
    mergeable = state["mergeable"]
    if mergeable != "mergeable":
        fail(f"PR #{state['pr_number']} is not mergeable (mergeable: {mergeable})")
    print("mergeable")
    return 0


def cmd_assert_pr_approved(args: argparse.Namespace) -> int:
    root = git_root()
    pr_number = ensure_pr_number(root, args.issue)
    wait_seconds = max(int(getattr(args, "wait_seconds", 0) or 0), 0)
    poll_interval = max(int(getattr(args, "poll_interval", 5) or 5), 1)
    deadline = time.monotonic() + wait_seconds

    while True:
        review_state = pr_review_state(pr_number)
        labels = review_state.get("label_names", [])
        if "senior-approved" in labels:
            print("approved")
            return 0
        if time.monotonic() >= deadline:
            review_decision = review_state.get("reviewDecision") or "unknown"
            is_draft = bool(review_state.get("isDraft"))
            state = review_state.get("state") or "unknown"
            mergeable = review_state.get("normalized_mergeable") or "unknown"
            checks = review_state.get("check_summary", {})
            label_text = ", ".join(labels) if labels else "none"
            fail(
                f"PR #{pr_number} is not senior-approved "
                f"(labels: {label_text}; reviewDecision: {review_decision}; draft: {is_draft}; state: {state}; "
                f"mergeable: {mergeable}; checks: {checks.get('overall', 'unknown')})"
            )
        time.sleep(poll_interval)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)

    def add_issue_parser(name: str, help_text: str) -> argparse.ArgumentParser:
        sub = subparsers.add_parser(name, help=help_text)
        sub.add_argument("--issue", type=int, required=True, help="GitHub issue number")
        return sub

    add_issue_parser("prepare", "Create or recover the worktree and local state").set_defaults(func=cmd_prepare)
    add_issue_parser(
        "assess-existing-work",
        "Detect whether the prepared issue branch already contains committed implementation work",
    ).set_defaults(func=cmd_assess_existing_work)
    add_issue_parser("plan", "Draft or refresh the issue implementation plan").set_defaults(func=cmd_plan)
    add_issue_parser(
        "plan-existing-work",
        "Write a compact plan for an issue branch that already contains committed implementation work",
    ).set_defaults(func=cmd_plan_existing_work)
    add_issue_parser("review-plan", "Run Codex senior review on the issue plan").set_defaults(func=cmd_review_plan)
    add_issue_parser("review-existing-work", "Run Codex senior review on the current issue branch state").set_defaults(
        func=cmd_review_existing_work
    )
    add_issue_parser("implement", "Implement the approved issue").set_defaults(func=cmd_implement)
    add_issue_parser("capture-baseline", "Capture current-main check failures for baseline-aware gating").set_defaults(
        func=cmd_capture_baseline
    )

    checks = add_issue_parser("checks", "Run repository checks")
    checks.add_argument("--mode", choices=["initial", "post-review", "refresh"], default="initial")
    checks.add_argument(
        "--allow-baseline",
        action="store_true",
        help="Treat baseline-only failures from current main as passable during issue delivery",
    )
    checks.set_defaults(func=cmd_checks)

    autofix = add_issue_parser("autofix", "Run best-effort cheap autofixes before retrying checks")
    autofix.add_argument("--mode", choices=["initial", "post-review", "refresh"], default="initial")
    autofix.set_defaults(func=cmd_autofix)

    sync = add_issue_parser("sync", "Commit and push branch changes")
    sync.add_argument("--mode", choices=["initial", "post-review", "refresh"], default="initial")
    sync.set_defaults(func=cmd_sync)

    fix_checks = add_issue_parser("fix-checks", "Fix failing checks with Claude")
    fix_checks.add_argument("--mode", choices=["initial", "post-review", "refresh"], default="initial")
    fix_checks.set_defaults(func=cmd_fix_checks)

    add_issue_parser("refresh-pr", "Refresh PR branch against base with Claude").set_defaults(func=cmd_refresh_pr)

    add_issue_parser("open-pr", "Create or recover the PR without changing draft state").set_defaults(func=cmd_open_pr)
    add_issue_parser("inspect-pr", "Print structured PR lifecycle state as JSON").set_defaults(func=cmd_inspect_pr)
    add_issue_parser("ready-pr", "Mark the PR ready for review if it is still draft").set_defaults(func=cmd_ready_pr)
    add_issue_parser("review-pr", "Run Codex senior review on the PR").set_defaults(func=cmd_review_pr)
    add_issue_parser("fix-pr", "Apply requested PR changes with Claude").set_defaults(func=cmd_fix_pr)
    add_issue_parser("assert-pr-fresh", "Fail unless the PR exists and does not need refresh").set_defaults(
        func=cmd_assert_pr_fresh
    )
    add_issue_parser("assert-pr-mergeable", "Fail unless the PR exists and is mergeable").set_defaults(
        func=cmd_assert_pr_mergeable
    )
    assert_pr = add_issue_parser("assert-pr-approved", "Fail unless the PR is senior-approved")
    assert_pr.add_argument("--wait-seconds", type=int, default=0, help="Poll for approval for up to this many seconds")
    assert_pr.add_argument("--poll-interval", type=int, default=5, help="Polling interval in seconds")
    assert_pr.set_defaults(func=cmd_assert_pr_approved)
    return parser


def _required_tools_for_action(action: str) -> tuple[str, ...]:
    base = ("gh", "git")
    if action in {"plan", "implement", "fix-pr", "fix-checks", "refresh-pr"}:
        return (*base, "claude")
    if action in {"review-plan", "review-existing-work", "review-pr"}:
        return (*base, "codex")
    return base


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    for tool in _required_tools_for_action(args.action):
        ensure_tool(tool)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
