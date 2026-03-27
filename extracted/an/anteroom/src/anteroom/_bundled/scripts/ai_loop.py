#!/usr/bin/env python3
"""Local Claude->checks->Codex review loop for issue or PR work.

This script is designed for locally authenticated CLIs:
- claude
- codex
- gh

It does not use API tokens directly.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def _run(
    args: list[str],
    *,
    cwd: Path,
    capture_output: bool = True,
    check: bool = True,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        input=input_text,
        text=True,
        capture_output=capture_output,
        check=check,
    )


def _slugify(text: str, *, limit: int = 48) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return (slug[:limit]).rstrip("-") or "work"


def _quote_cmd(args: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in args)


@dataclass
class Target:
    kind: str
    number: int
    title: str
    branch: str
    pr_number: int | None = None


@dataclass
class ReviewResult:
    status: str
    summary: str
    findings_markdown: str


class LoopRunner:
    def __init__(self, ns: argparse.Namespace) -> None:
        self.ns = ns
        self.repo_root = Path(ns.repo_root).resolve()
        self.git_root = self._git_root(self.repo_root)
        self.gh = ns.gh_bin
        self.claude = ns.claude_bin
        self.codex = ns.codex_bin

    def _git_root(self, cwd: Path) -> Path:
        proc = _run(["git", "rev-parse", "--show-toplevel"], cwd=cwd)
        return Path(proc.stdout.strip()).resolve()

    def _print_step(self, text: str) -> None:
        print(f"\n==> {text}", flush=True)

    def _repo_slug(self) -> str:
        proc = _run([self.gh, "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"], cwd=self.git_root)
        return proc.stdout.strip()

    def _resolve_issue(self, number: int) -> Target:
        proc = _run(
            [self.gh, "issue", "view", str(number), "--json", "number,title,state"],
            cwd=self.git_root,
        )
        payload = json.loads(proc.stdout)
        if payload["state"] != "OPEN":
            raise SystemExit(f"Issue #{number} is not open")
        branch = f"issue-{number}-{_slugify(payload['title'])}"
        return Target(kind="issue", number=number, title=payload["title"], branch=branch)

    def _resolve_pr(self, number: int) -> Target:
        proc = _run(
            [self.gh, "pr", "view", str(number), "--json", "number,title,state,isDraft,headRefName"],
            cwd=self.git_root,
        )
        payload = json.loads(proc.stdout)
        if payload["state"] != "OPEN":
            raise SystemExit(f"PR #{number} is not open")
        if payload["isDraft"]:
            raise SystemExit(f"PR #{number} is a draft")
        return Target(
            kind="pr",
            number=number,
            title=payload["title"],
            branch=payload["headRefName"],
            pr_number=payload["number"],
        )

    def _find_worktree_for_branch(self, branch: str) -> Path | None:
        proc = _run(["git", "worktree", "list", "--porcelain"], cwd=self.git_root)
        current_path: Path | None = None
        current_branch: str | None = None
        for raw_line in proc.stdout.splitlines():
            if raw_line.startswith("worktree "):
                if current_path and current_branch == f"refs/heads/{branch}":
                    return current_path
                current_path = Path(raw_line.split(" ", 1)[1]).resolve()
                current_branch = None
            elif raw_line.startswith("branch "):
                current_branch = raw_line.split(" ", 1)[1]
        if current_path and current_branch == f"refs/heads/{branch}":
            return current_path
        return None

    def _default_worktree_path(self, branch: str) -> Path:
        return self.git_root.parent / f"{self.git_root.name}-{branch}"

    def _ensure_issue_worktree(self, target: Target) -> Path:
        existing = self._find_worktree_for_branch(target.branch)
        if existing:
            return existing
        if self.ns.worktree:
            path = Path(self.ns.worktree).resolve()
        else:
            path = self._default_worktree_path(target.branch)
        if path.exists():
            return path
        self._print_step(f"creating worktree {path}")
        _run(["git", "worktree", "add", "-b", target.branch, str(path), self.ns.base_branch], cwd=self.git_root)
        return path

    def _ensure_pr_worktree(self, target: Target) -> Path:
        existing = self._find_worktree_for_branch(target.branch)
        if existing:
            return existing
        if self.ns.worktree:
            path = Path(self.ns.worktree).resolve()
        else:
            path = self._default_worktree_path(target.branch)
        if path.exists():
            return path
        self._print_step(f"fetching PR branch {target.branch}")
        _run(["git", "fetch", "origin", f"{target.branch}:{target.branch}"], cwd=self.git_root)
        self._print_step(f"creating worktree {path}")
        _run(["git", "worktree", "add", str(path), target.branch], cwd=self.git_root)
        return path

    def _resolve_target(self) -> tuple[Target, Path]:
        if self.ns.issue is not None:
            target = self._resolve_issue(self.ns.issue)
            return target, self._ensure_issue_worktree(target)
        if self.ns.pr is not None:
            target = self._resolve_pr(self.ns.pr)
            return target, self._ensure_pr_worktree(target)
        raise SystemExit("Expected --issue or --pr")

    def _claude_prompt(self, target: Target, findings: str | None) -> str:
        if findings:
            return (
                f"Address these review findings on the current branch for {target.kind} #{target.number} "
                f"({target.title}). Make the code changes only, do not create a commit unless asked, and finish "
                f"with a concise summary.\n\n{findings}"
            )
        return (
            f"Implement {target.kind} #{target.number}: {target.title}. Work on the current branch in this repo. "
            f"Make the code changes only, do not create a commit unless asked, and finish with a concise summary."
        )

    def _run_claude(self, worktree: Path, prompt: str) -> None:
        args = [self.claude, "-p", prompt]
        self._print_step(f"running Claude: {_quote_cmd(args)}")
        env = os.environ.copy()
        env.pop("ANTHROPIC_API_KEY", None)
        subprocess.run(args, cwd=worktree, check=True, env=env)

    def _run_checks(self, worktree: Path) -> None:
        if self.ns.skip_checks:
            return
        for command in self.ns.check:
            self._print_step(f"running check: {command}")
            subprocess.run(command, cwd=worktree, shell=True, check=True, text=True)

    def _codex_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "status": {"type": "string", "enum": ["clean", "findings"]},
                "summary": {"type": "string"},
                "findings_markdown": {"type": "string"},
            },
            "required": ["status", "summary", "findings_markdown"],
        }

    def _review_prompt(self, target: Target) -> str:
        if target.kind == "pr":
            return (
                f"Review PR #{target.pr_number} on the current branch like a code reviewer. Focus on bugs, regressions, "
                f"stale docs, and missing tests. Ignore style nits. If there are no real findings, return status clean. "
                f"If there are real findings, return status findings and concise markdown in findings_markdown."
            )
        return (
            f"Review the current branch for work related to issue #{target.number} ({target.title}). Focus on bugs, "
            f"regressions, stale docs, and missing tests. Ignore style nits. If there are no real findings, return "
            f"status clean. If there are real findings, return status findings and concise markdown in findings_markdown."
        )

    def _run_codex_review(self, worktree: Path, target: Target) -> ReviewResult:
        with tempfile.TemporaryDirectory(prefix="ai-loop-") as tmp_dir:
            schema_path = Path(tmp_dir) / "review-schema.json"
            output_path = Path(tmp_dir) / "review-output.json"
            schema_path.write_text(json.dumps(self._codex_schema()), encoding="ascii")
            prompt = self._review_prompt(target)
            args = [
                self.codex,
                "exec",
                "-C",
                str(worktree),
                "--output-schema",
                str(schema_path),
                "-o",
                str(output_path),
                prompt,
            ]
            self._print_step(f"running Codex: {_quote_cmd(args)}")
            subprocess.run(args, cwd=worktree, check=True)
            payload = json.loads(output_path.read_text(encoding="utf-8"))
        return ReviewResult(
            status=payload["status"],
            summary=payload["summary"].strip(),
            findings_markdown=payload["findings_markdown"].strip(),
        )

    def _post_pr_comment(self, pr_number: int, body: str) -> str:
        proc = _run([self.gh, "pr", "comment", str(pr_number), "--body", body], cwd=self.git_root)
        return proc.stdout.strip()

    def _post_issue_comment(self, issue_number: int, body: str) -> str:
        proc = _run([self.gh, "issue", "comment", str(issue_number), "--body", body], cwd=self.git_root)
        return proc.stdout.strip()

    def _maybe_post_comment(self, target: Target, review: ReviewResult) -> None:
        if review.status != "findings":
            return
        if target.pr_number is not None:
            self._print_step(f"posting PR comment to #{target.pr_number}")
            url = self._post_pr_comment(target.pr_number, review.findings_markdown)
            print(f"posted comment: {url}", flush=True)
            return
        if self.ns.comment_on_issue and target.kind == "issue":
            self._print_step(f"posting issue comment to #{target.number}")
            url = self._post_issue_comment(target.number, review.findings_markdown)
            print(f"posted comment: {url}", flush=True)

    def run(self) -> int:
        target, worktree = self._resolve_target()
        print(f"repo:     {self._repo_slug()}")
        print(f"target:   {target.kind} #{target.number} — {target.title}")
        print(f"branch:   {target.branch}")
        print(f"worktree: {worktree}")

        findings: str | None = None
        for round_no in range(1, self.ns.max_rounds + 1):
            self._print_step(f"round {round_no}/{self.ns.max_rounds}")
            self._run_claude(worktree, self._claude_prompt(target, findings))
            self._run_checks(worktree)
            review = self._run_codex_review(worktree, target)
            print(f"\nCodex summary: {review.summary}\n", flush=True)
            if review.status == "clean":
                print("loop complete: no findings on current head", flush=True)
                return 0
            print(review.findings_markdown, flush=True)
            self._maybe_post_comment(target, review)
            findings = review.findings_markdown

        print("loop stopped: max rounds reached with findings still present", flush=True)
        return 1


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--issue", type=int, help="GitHub issue number to implement and review")
    target.add_argument("--pr", type=int, help="GitHub pull request number to review/fix")

    parser.add_argument("--repo-root", default=os.getcwd(), help="Repository root or any path inside the repo")
    parser.add_argument("--worktree", help="Optional explicit worktree path")
    parser.add_argument("--base-branch", default="main", help="Base branch used for new issue worktrees")
    parser.add_argument("--max-rounds", type=int, default=3, help="Maximum Claude/Codex fix-review rounds")
    parser.add_argument(
        "--check",
        action="append",
        default=[],
        help="Shell command to run after each Claude round (repeatable)",
    )
    parser.add_argument("--skip-checks", action="store_true", help="Skip local checks between Claude and Codex")
    parser.add_argument(
        "--comment-on-issue",
        action="store_true",
        help="In issue mode, post Codex findings back to the issue",
    )
    parser.add_argument("--claude-bin", default="claude", help="Claude CLI executable")
    parser.add_argument("--codex-bin", default="codex", help="Codex CLI executable")
    parser.add_argument("--gh-bin", default="gh", help="GitHub CLI executable")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    ns = _parse_args(argv or sys.argv[1:])
    try:
        return LoopRunner(ns).run()
    except subprocess.CalledProcessError as exc:
        print(f"command failed ({exc.returncode}): {_quote_cmd(exc.cmd)}", file=sys.stderr)
        if exc.stdout:
            print(exc.stdout, file=sys.stderr, end="")
        if exc.stderr:
            print(exc.stderr, file=sys.stderr, end="")
        return exc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
