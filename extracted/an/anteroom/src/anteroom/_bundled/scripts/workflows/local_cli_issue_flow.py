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
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Any, NoReturn

PLAN_START = "<!-- anteroom:plan:start -->"
PLAN_END = "<!-- anteroom:plan:end -->"
STATE_DIRNAME = "anteroom-workflows"
DEFAULT_CHECKS = "ruff check src/ tests/ && python -m pytest tests/unit/ -x -q --tb=short"
DEFAULT_AUTOFIX = "ruff check src/ tests/ --fix"
STREAM_SOFT_LIMIT = 60
WORKTREE_JUNK_GLOBS = ("<MagicMock*",)


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


def git_dir(root: Path) -> Path:
    return Path(run_stdout(["git", "rev-parse", "--git-dir"], cwd=root)).resolve()


def state_dir(root: Path, issue_number: int) -> Path:
    return git_dir(root) / STATE_DIRNAME / f"issue-{issue_number}"


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


def pr_review_state(pr_number: int) -> dict[str, Any]:
    data = run_json(
        [
            "gh",
            "pr",
            "view",
            str(pr_number),
            "--json",
            "labels,reviewDecision,isDraft,state,url",
        ]
    )
    data["label_names"] = [label["name"] for label in data.get("labels", [])]
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


def ensure_worktree(root: Path, issue_number: int) -> dict[str, Any]:
    issue = issue_data(issue_number)
    if issue.get("state", "").lower() != "open":
        fail(f"Issue #{issue_number} is not open")

    repo = repo_name()
    branch = issue_branch(issue_number, issue["title"])
    worktree = issue_worktree(root, repo, issue_number, issue["title"])

    run(["git", "fetch", "origin", "main"], cwd=root, check=False)

    if run(["git", "show-ref", "--verify", f"refs/heads/{branch}"], cwd=root, check=False).returncode != 0:
        run(["git", "branch", branch, latest_main_ref(root)], cwd=root)

    if not worktree.exists():
        run(["git", "worktree", "add", str(worktree), branch], cwd=root)

    state = update_state(
        root,
        issue_number,
        issue_number=issue_number,
        issue_title=issue["title"],
        issue_url=issue["url"],
        branch=branch,
        worktree_path=str(worktree),
        repo_name=repo,
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


def build_claude_plan_prompt(issue_number: int) -> str:
    return f"""
Draft or refresh the implementation plan for GitHub issue #{issue_number}.

Use the GitHub issue body and issue comments as the source of truth for
requirements and clarifications. Read the repository directly as needed.

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


def build_codex_plan_review_prompt(issue_number: int) -> str:
    return f"""
Review GitHub issue #{issue_number} as the senior reviewer for this repository.

Use the issue body, issue comments, VISION.md, CLAUDE.md, and relevant code.
Approve only if the plan is implementation-ready with zero blockers.

Return JSON only with this shape:
{{
  "decision": "approve" | "changes_requested",
  "summary": "<one sentence>",
  "comment_markdown": "<markdown comment to post on the issue>"
}}
""".strip()


def build_claude_implement_prompt(issue_number: int) -> str:
    return f"""
Implement GitHub issue #{issue_number} on the current branch.

Use the approved plan in the issue body and the issue comments as the source of
truth. Read the repository directly as needed. Make the changes in this
worktree, keep scope tight, and leave the branch ready for repository checks.

Return only a short markdown change summary.
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


def build_claude_pr_fix_prompt(pr_number: int) -> str:
    return f"""
Address the latest requested changes on GitHub PR #{pr_number}.

Use the PR review history and comments as the source of truth. Make only the
changes needed to satisfy the latest senior-review feedback, then stop.

Return only a short markdown change summary.
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


def _spawn_text_subprocess(command: list[str], *, cwd: Path | None = None) -> subprocess.Popen[str]:
    """Start a text subprocess with line-buffered pipes."""
    return subprocess.Popen(
        command,
        cwd=str(cwd) if cwd else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )


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
            "--output-format", "stream-json",
            "--include-partial-messages",
            "--permission-mode", "bypassPermissions",
            "--", prompt,
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


def codex_once(prompt: str, *, cwd: Path) -> str:
    proc = _spawn_text_subprocess(
        [
            "codex",
            "exec",
            "--json",
            "--color",
            "never",
            "--dangerously-bypass-approvals-and-sandbox",
            "--",
            prompt,
        ],
        cwd=cwd,
    )
    stderr_lines: list[str] = []
    stderr_thread = threading.Thread(target=_forward_stderr, args=(proc.stderr, stderr_lines), daemon=True)
    stderr_thread.start()

    final_text = ""
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

    proc.wait()
    stderr_thread.join()
    if proc.returncode != 0:
        stderr = "\n".join(line for line in stderr_lines if line).strip()
        fail(f"Codex CLI failed: {stderr or f'exit code {proc.returncode}'}")

    return final_text


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


def run_checks(state: dict[str, Any], *, mode: str) -> None:
    if mode == "post-review" and state.get("last_pr_review_decision") != "changes_requested":
        print("no_checks_needed")
        return

    worktree = Path(state["worktree_path"])
    removed_before = cleanup_worktree_junk(worktree)
    if removed_before:
        print(f"removed_junk: {', '.join(removed_before)}")
    command = checks_command()
    try:
        proc = subprocess.run(command, cwd=str(worktree), shell=True, text=True)
    finally:
        removed_after = cleanup_worktree_junk(worktree)
        if removed_after:
            print(f"removed_junk: {', '.join(removed_after)}")
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)
    print("checks_passed")


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
    try:
        proc = subprocess.run(command, cwd=str(worktree), shell=True, text=True)
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


def cmd_review_plan(args: argparse.Namespace) -> int:
    root = git_root()
    state = ensure_worktree(root, args.issue)
    worktree = Path(state["worktree_path"])
    review = extract_json(codex_once(build_codex_plan_review_prompt(args.issue), cwd=worktree))
    decision = str(review.get("decision", "")).strip()
    summary = str(review.get("summary", "")).strip() or "Plan review completed."
    comment = str(review.get("comment_markdown", "")).strip() or summary
    if decision not in {"approve", "changes_requested"}:
        fail(f"Unexpected plan review decision: {decision!r}")

    post_issue_comment(args.issue, comment)
    if decision == "approve":
        edit_issue_labels(args.issue, add=["senior-approved"], remove=["needs-senior-review"])
        update_state(root, args.issue, last_plan_review_decision="approve")
        print("approved")
        return 0

    edit_issue_labels(args.issue, add=["needs-senior-review"], remove=["senior-approved"])
    update_state(root, args.issue, last_plan_review_decision="changes_requested")
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
    run_checks(state, mode=args.mode)
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
        review_state = pr_review_state(existing)
        if review_state.get("isDraft"):
            run(["gh", "pr", "ready", str(existing)], check=False)
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
    review = extract_json(codex_once(build_codex_pr_review_prompt(pr_number), cwd=worktree))
    decision = str(review.get("decision", "")).strip()
    summary = str(review.get("summary", "")).strip() or "PR review completed."
    comment = str(review.get("comment_markdown", "")).strip() or summary
    if decision not in {"approve", "changes_requested"}:
        fail(f"Unexpected PR review decision: {decision!r}")

    post_pr_review(pr_number, decision, comment)
    if decision == "approve":
        edit_pr_labels(pr_number, add=["senior-approved"], remove=["needs-senior-review"])
        update_state(root, args.issue, last_pr_review_decision="approve")
        print("approved")
        return 0

    edit_pr_labels(pr_number, add=["needs-senior-review"], remove=["senior-approved"])
    update_state(root, args.issue, last_pr_review_decision="changes_requested")
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
    summary = strip_fences(claude_once(build_claude_pr_fix_prompt(pr_number), cwd=worktree))
    update_state(root, args.issue, last_pr_fix_summary=summary)
    print(summary or "fixes_applied")
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
            label_text = ", ".join(labels) if labels else "none"
            fail(
                f"PR #{pr_number} is not senior-approved "
                f"(labels: {label_text}; reviewDecision: {review_decision}; draft: {is_draft}; state: {state})"
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
    add_issue_parser("plan", "Draft or refresh the issue implementation plan").set_defaults(func=cmd_plan)
    add_issue_parser("review-plan", "Run Codex senior review on the issue plan").set_defaults(func=cmd_review_plan)
    add_issue_parser("implement", "Implement the approved issue").set_defaults(func=cmd_implement)

    checks = add_issue_parser("checks", "Run repository checks")
    checks.add_argument("--mode", choices=["initial", "post-review"], default="initial")
    checks.set_defaults(func=cmd_checks)

    autofix = add_issue_parser("autofix", "Run best-effort cheap autofixes before retrying checks")
    autofix.add_argument("--mode", choices=["initial", "post-review"], default="initial")
    autofix.set_defaults(func=cmd_autofix)

    sync = add_issue_parser("sync", "Commit and push branch changes")
    sync.add_argument("--mode", choices=["initial", "post-review"], default="initial")
    sync.set_defaults(func=cmd_sync)

    add_issue_parser("open-pr", "Create or recover the draft PR").set_defaults(func=cmd_open_pr)
    add_issue_parser("ready-pr", "Mark the PR ready for review if it is still draft").set_defaults(func=cmd_ready_pr)
    add_issue_parser("review-pr", "Run Codex senior review on the PR").set_defaults(func=cmd_review_pr)
    add_issue_parser("fix-pr", "Apply requested PR changes with Claude").set_defaults(func=cmd_fix_pr)
    assert_pr = add_issue_parser("assert-pr-approved", "Fail unless the PR is senior-approved")
    assert_pr.add_argument("--wait-seconds", type=int, default=0, help="Poll for approval for up to this many seconds")
    assert_pr.add_argument("--poll-interval", type=int, default=5, help="Polling interval in seconds")
    assert_pr.set_defaults(func=cmd_assert_pr_approved)
    return parser


def _required_tools_for_action(action: str) -> tuple[str, ...]:
    base = ("gh", "git")
    if action in {"plan", "implement", "fix-pr"}:
        return (*base, "claude")
    if action in {"review-plan", "review-pr"}:
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
