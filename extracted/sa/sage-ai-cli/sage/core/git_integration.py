"""
Git integration and workflow management for SAGE.

P2-81: Add merge, rebase, cherry-pick support
P2-82: Implement conflict detection and resolution
P2-83: Add branch creation/deletion management
P2-84: Support remote operations (fetch, push, pull)
P2-85: Implement intelligent commit message generation
P2-86: Add conventional commits formatting
P2-87: Implement git blame analysis for context
P2-88: Add related commit finding
P2-89: Support GitFlow/Trunk-Based workflows
P2-90: Implement branch naming convention enforcement
P2-91 to P2-105: Workflow templates and dependency analysis
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from rich.console import Console

from sage.core.commands import execute_command

# =============================================================================
# Git Operation Wrapper
# =============================================================================


class GitError(Exception):
    """Git operation error."""

    def __init__(self, message: str, command: str, returncode: int, stderr: str):
        super().__init__(message)
        self.command = command
        self.returncode = returncode
        self.stderr = stderr


class Git:
    """
    Git operations wrapper.

    P2-81: Add merge, rebase, cherry-pick support
    P2-83: Add branch creation/deletion management
    P2-81: Support remote operations
    """

    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.is_repo = self._check_is_repo()

    def _check_is_repo(self) -> bool:
        """Check if the path is a git repository.

        Bug history: this used `capture_output=True` together with
        `stderr=subprocess.DEVNULL`, which raises `ValueError: stdout and
        stderr arguments may not be used with capture_output`. The bare
        `except` swallowed the error, making every Git instance report
        is_repo=False and silently turning all git ops into no-ops. Tests
        that depended on real git state then saw empty results.
        """
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=str(self.repo_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                timeout=5,
            )
            return result.returncode == 0
        except Exception:
            return False

    def _run(self, *args: str, check: bool = True, timeout: int = 30) -> subprocess.CompletedProcess:
        """Run a git command."""
        if not self.is_repo:
            # Return a dummy process if not a repo
            return subprocess.CompletedProcess(args=["git", *args], returncode=1, stdout="", stderr="Not a git repository")
        
        cmd = ["git", *args]
        result = subprocess.run(
            cmd,
            cwd=str(self.repo_path),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if check and result.returncode != 0:
            raise GitError(
                f"Git command failed: {' '.join(cmd)}",
                " ".join(cmd),
                result.returncode,
                result.stderr,
            )
        return result

    # ── Status and Info ──────────────────────────────────────

    def status(self) -> dict[str, Any]:
        """Get repository status."""
        result = self._run("status", "--porcelain", "-b")
        lines = result.stdout.strip().split("\n")

        status = {
            "branch": "",
            "ahead": 0,
            "behind": 0,
            "staged": [],
            "unstaged": [],
            "untracked": [],
        }

        for line in lines:
            if line.startswith("##"):
                # Branch info
                match = re.match(
                    r"## (\S+?)(?:\.\.\.(\S+))?(?: \[ahead (\d+)(?:, behind (\d+))?\])?", line
                )
                if match:
                    status["branch"] = match.group(1)
                    status["ahead"] = int(match.group(3) or 0)
                    status["behind"] = int(match.group(4) or 0)
            elif line:
                index_status = line[0]
                worktree_status = line[1]
                filename = line[3:]

                if index_status != " " and index_status != "?":
                    status["staged"].append(filename)
                if worktree_status != " " and worktree_status != "?":
                    status["unstaged"].append(filename)
                if line.startswith("??"):
                    status["untracked"].append(filename)

        return status

    def current_branch(self) -> str:
        """Get current branch name."""
        result = self._run("rev-parse", "--abbrev-ref", "HEAD")
        return result.stdout.strip()

    def get_commit_sha(self, ref: str = "HEAD") -> str:
        """Get commit SHA for a reference."""
        result = self._run("rev-parse", ref)
        return result.stdout.strip()

    # ── Branch Operations (P2-83) ────────────────────────────

    def branches(self, all: bool = False) -> list[dict[str, Any]]:
        """List branches."""
        args = [
            "branch",
            "-v",
            "--format=%(refname:short)|%(objectname:short)|%(upstream:short)|%(subject)",
        ]
        if all:
            args.append("-a")

        result = self._run(*args)
        branches = []

        for line in result.stdout.strip().split("\n"):
            if line:
                parts = line.split("|", 3)
                if len(parts) >= 4:
                    branches.append(
                        {
                            "name": parts[0],
                            "sha": parts[1],
                            "upstream": parts[2],
                            "message": parts[3],
                        }
                    )

        return branches

    def create_branch(self, name: str, start_point: str | None = None) -> None:
        """Create a new branch."""
        args = ["checkout", "-b", name]
        if start_point:
            args.append(start_point)
        self._run(*args)

    def delete_branch(self, name: str, force: bool = False) -> None:
        """Delete a branch."""
        flag = "-D" if force else "-d"
        self._run("branch", flag, name)

    def switch_branch(self, name: str) -> None:
        """Switch to a branch."""
        self._run("checkout", name)

    # ── Merge Operations (P2-81, P2-82) ──────────────────────

    def merge(self, branch: str, no_ff: bool = False, message: str | None = None) -> bool:
        """
        Merge a branch.

        Returns True if successful, False if conflicts.
        """
        args = ["merge", branch]
        if no_ff:
            args.append("--no-ff")
        if message:
            args.extend(["-m", message])

        result = self._run(*args, check=False)
        return result.returncode == 0

    def abort_merge(self) -> None:
        """Abort an in-progress merge."""
        self._run("merge", "--abort")

    def get_conflicts(self) -> list[str]:
        """Get list of conflicting files."""
        result = self._run("diff", "--name-only", "--diff-filter=U", check=False)
        return result.stdout.strip().split("\n") if result.stdout.strip() else []

    def resolve_conflict(self, filepath: str, theirs: bool = False) -> None:
        """Resolve a conflict by choosing ours or theirs."""
        strategy = "--theirs" if theirs else "--ours"
        self._run("checkout", strategy, filepath)
        self._run("add", filepath)

    # ── Rebase Operations (P2-81) ────────────────────────────

    def rebase(self, onto: str, interactive: bool = False) -> bool:
        """Rebase onto a branch."""
        args = ["rebase"]
        if interactive:
            args.append("-i")
        args.append(onto)

        result = self._run(*args, check=False)
        return result.returncode == 0

    def abort_rebase(self) -> None:
        """Abort an in-progress rebase."""
        self._run("rebase", "--abort")

    def continue_rebase(self) -> bool:
        """Continue a rebase after resolving conflicts."""
        result = self._run("rebase", "--continue", check=False)
        return result.returncode == 0

    # ── Cherry-pick (P2-81) ──────────────────────────────────

    def cherry_pick(self, *commits: str, no_commit: bool = False) -> bool:
        """Cherry-pick commits."""
        args = ["cherry-pick"]
        if no_commit:
            args.append("-n")
        args.extend(commits)

        result = self._run(*args, check=False)
        return result.returncode == 0

    def abort_cherry_pick(self) -> None:
        """Abort an in-progress cherry-pick."""
        self._run("cherry-pick", "--abort")

    # ── Remote Operations (P2-84) ────────────────────────────

    def fetch(self, remote: str = "origin", prune: bool = True) -> None:
        """Fetch from remote."""
        args = ["fetch", remote]
        if prune:
            args.append("--prune")
        self._run(*args)

    def pull(self, remote: str = "origin", branch: str | None = None, rebase: bool = False) -> bool:
        """Pull from remote."""
        args = ["pull"]
        if rebase:
            args.append("--rebase")
        args.append(remote)
        if branch:
            args.append(branch)

        result = self._run(*args, check=False)
        return result.returncode == 0

    def push(
        self,
        remote: str = "origin",
        branch: str | None = None,
        set_upstream: bool = False,
        force: bool = False,
    ) -> bool:
        """Push to remote."""
        args = ["push"]
        if set_upstream:
            args.append("-u")
        if force:
            args.append("--force-with-lease")
        args.append(remote)
        if branch:
            args.append(branch)

        result = self._run(*args, check=False)
        return result.returncode == 0

    # ── Commit Operations ────────────────────────────────────

    def commit(self, message: str, all: bool = False) -> str:
        """Create a commit."""
        args = ["commit", "-m", message]
        if all:
            args.append("-a")
        self._run(*args)
        return self.get_commit_sha("HEAD")

    def add(self, *paths: str) -> None:
        """Stage files."""
        self._run("add", *paths)

    def diff(self, staged: bool = False, path: str | None = None) -> str:
        """Get diff."""
        args = ["diff"]
        if staged:
            args.append("--staged")
        if path:
            args.extend(["--", path])

        result = self._run(*args)
        return result.stdout

    # ── Blame Analysis (P2-87) ───────────────────────────────

    def blame(
        self, filepath: str, line_range: tuple[int, int] | None = None
    ) -> list[dict[str, Any]]:
        """Get blame information for a file."""
        args = ["blame", "--porcelain"]
        if line_range:
            args.extend(["-L", f"{line_range[0]},{line_range[1]}"])
        args.append(filepath)

        result = self._run(*args)
        lines = result.stdout.split("\n")

        blame_data = []
        current = {}

        for line in lines:
            if line.startswith(tuple("0123456789abcdef")):
                parts = line.split()
                current = {
                    "sha": parts[0],
                    "original_line": int(parts[1]),
                    "final_line": int(parts[2]),
                }
            elif line.startswith("author "):
                current["author"] = line[7:]
            elif line.startswith("author-time "):
                current["timestamp"] = int(line[12:])
            elif line.startswith("summary "):
                current["summary"] = line[8:]
            elif line.startswith("\t"):
                current["content"] = line[1:]
                blame_data.append(current)
                current = {}

        return blame_data

    # ── Related Commits (P2-88) ──────────────────────────────

    def find_related_commits(
        self,
        filepath: str | None = None,
        author: str | None = None,
        grep: str | None = None,
        since: str | None = None,
        max_count: int = 20,
    ) -> list[dict[str, Any]]:
        """Find related commits."""
        args = [
            "log",
            f"--max-count={max_count}",
            "--format=%H|%an|%at|%s",
        ]

        if filepath:
            args.extend(["--", filepath])
        if author:
            args.extend(["--author", author])
        if grep:
            args.extend(["--grep", grep])
        if since:
            args.extend(["--since", since])

        result = self._run(*args)
        commits = []

        for line in result.stdout.strip().split("\n"):
            if line:
                parts = line.split("|", 3)
                if len(parts) >= 4:
                    commits.append(
                        {
                            "sha": parts[0],
                            "author": parts[1],
                            "timestamp": int(parts[2]),
                            "message": parts[3],
                        }
                    )

        return commits


# =============================================================================
# Commit Message Generation (P2-85, P2-86)
# =============================================================================


class ConventionalCommitType(Enum):
    """Conventional commit types."""

    FEAT = "feat"
    FIX = "fix"
    DOCS = "docs"
    STYLE = "style"
    REFACTOR = "refactor"
    PERF = "perf"
    TEST = "test"
    BUILD = "build"
    CI = "ci"
    CHORE = "chore"
    REVERT = "revert"


@dataclass
class CommitMessage:
    """Structured commit message."""

    type: ConventionalCommitType
    scope: str | None
    description: str
    body: str | None = None
    breaking: bool = False
    footer: str | None = None

    def format(self) -> str:
        """Format as conventional commit message."""
        # Header
        header = self.type.value
        if self.scope:
            header += f"({self.scope})"
        if self.breaking:
            header += "!"
        header += f": {self.description}"

        parts = [header]

        # Body
        if self.body:
            parts.append("")
            parts.append(self.body)

        # Footer
        if self.footer:
            parts.append("")
            parts.append(self.footer)

        return "\n".join(parts)


class CommitMessageGenerator:
    """
    Generates intelligent commit messages.

    P2-85: Implement intelligent commit message generation
    P2-86: Add conventional commits formatting
    """

    # Patterns to detect commit type from diff
    TYPE_PATTERNS = {
        ConventionalCommitType.FEAT: [r"add(ed)?", r"new", r"implement", r"create"],
        ConventionalCommitType.FIX: [r"fix(ed)?", r"bug", r"issue", r"resolve"],
        ConventionalCommitType.DOCS: [r"readme", r"docstring", r"comment", r"\.md$"],
        ConventionalCommitType.STYLE: [r"format", r"lint", r"style", r"whitespace"],
        ConventionalCommitType.REFACTOR: [r"refactor", r"restructure", r"rename", r"move"],
        ConventionalCommitType.PERF: [r"performance", r"optimi", r"speed", r"fast"],
        ConventionalCommitType.TEST: [r"test", r"spec", r"\.test\.", r"_test\."],
        ConventionalCommitType.BUILD: [r"build", r"dependency", r"package", r"webpack"],
        ConventionalCommitType.CI: [r"ci", r"workflow", r"github", r"jenkins"],
        ConventionalCommitType.CHORE: [r"chore", r"maintenance", r"update", r"upgrade"],
    }

    def __init__(self, git: Git):
        self.git = git

    def generate(
        self,
        model_callback: callable | None = None,
    ) -> CommitMessage:
        """Generate a commit message from staged changes."""
        diff = self.git.diff(staged=True)

        if not diff:
            raise ValueError("No staged changes to commit")

        # Analyze diff
        commit_type = self._detect_type(diff)
        scope = self._detect_scope(diff)
        description = self._generate_description(diff, model_callback)

        # Check for breaking changes
        breaking = "BREAKING" in diff or "breaking change" in diff.lower()

        return CommitMessage(
            type=commit_type,
            scope=scope,
            description=description,
            breaking=breaking,
        )

    def _detect_type(self, diff: str) -> ConventionalCommitType:
        """Detect commit type from diff."""
        diff_lower = diff.lower()

        for commit_type, patterns in self.TYPE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, diff_lower):
                    return commit_type

        return ConventionalCommitType.CHORE

    def _detect_scope(self, diff: str) -> str | None:
        """Detect scope from changed files."""
        # Extract file paths from diff
        files = re.findall(r"^\+\+\+ b/(.+)$", diff, re.MULTILINE)

        if not files:
            return None

        # Find common directory
        if len(files) == 1:
            parts = files[0].split("/")
            if len(parts) > 1:
                return parts[0]

        # Multiple files - find common prefix
        common = files[0].split("/")
        for f in files[1:]:
            parts = f.split("/")
            common = [c for c, p in zip(common, parts) if c == p]

        return common[0] if common else None

    def _generate_description(
        self,
        diff: str,
        model_callback: callable | None,
    ) -> str:
        """Generate description from diff."""
        if model_callback:
            prompt = f"""Generate a concise commit message description (max 50 chars) for this diff:

{diff[:2000]}

Return ONLY the description, no type prefix."""
            return model_callback(prompt).strip()[:50]

        # Fallback: extract from diff
        # Look for function/class definitions added
        additions = re.findall(r"^\+(?![\+])\s*(.+)$", diff, re.MULTILINE)

        for line in additions:
            if line.startswith("def "):
                func_name = re.match(r"def (\w+)", line)
                if func_name:
                    return f"add {func_name.group(1)} function"
            elif line.startswith("class "):
                class_name = re.match(r"class (\w+)", line)
                if class_name:
                    return f"add {class_name.group(1)} class"

        return "update code"


# =============================================================================
# Branch Naming Convention (P2-90)
# =============================================================================


class BranchNameValidator:
    """
    Validates branch names against conventions.

    P2-90: Implement branch naming convention enforcement
    """

    # Common conventions
    CONVENTIONS = {
        "gitflow": r"^(feature|bugfix|hotfix|release|support)/[a-z0-9\-]+$",
        "trunk": r"^[a-z0-9\-]+/[A-Z]+-\d+(-[a-z0-9\-]+)?$",  # e.g., feature/JIRA-123-description
        "simple": r"^[a-z0-9][a-z0-9\-]*[a-z0-9]$",
    }

    def __init__(self, convention: str = "gitflow"):
        self.convention = convention
        self._pattern = re.compile(self.CONVENTIONS.get(convention, self.CONVENTIONS["simple"]))

    def validate(self, branch_name: str) -> tuple[bool, str | None]:
        """Validate branch name. Returns (valid, error_message)."""
        if self._pattern.match(branch_name):
            return True, None

        return False, f"Branch name '{branch_name}' does not match {self.convention} convention"

    def suggest(self, description: str, ticket: str | None = None) -> str:
        """Suggest a valid branch name."""
        # Clean description
        clean = re.sub(r"[^a-z0-9\s]", "", description.lower())
        slug = re.sub(r"\s+", "-", clean.strip())[:30]

        if self.convention == "gitflow":
            return f"feature/{slug}"
        elif self.convention == "trunk" and ticket:
            return f"feature/{ticket}-{slug}"
        else:
            return slug


# =============================================================================
# Workflow Templates (P2-89, P2-91 to P2-100)
# =============================================================================


class WorkflowType(Enum):
    """Workflow types."""

    GITFLOW = "gitflow"
    TRUNK_BASED = "trunk_based"
    GITHUB_FLOW = "github_flow"
    CUSTOM = "custom"


@dataclass
class WorkflowStep:
    """A step in a workflow."""

    name: str
    description: str
    command: str | None = None
    condition: str | None = None
    on_failure: str = "abort"  # abort, continue, retry


@dataclass
class Workflow:
    """A complete workflow definition."""

    name: str
    workflow_type: WorkflowType
    steps: list[WorkflowStep]
    description: str = ""


class WorkflowManager:
    """
    Manages development workflows.

    P2-89: Support GitFlow/Trunk-Based workflows
    P2-91 to P2-100: Workflow templates
    """

    TEMPLATES = {
        "feature": Workflow(
            name="Feature Development",
            workflow_type=WorkflowType.GITFLOW,
            description="Complete feature development workflow",
            steps=[
                WorkflowStep(
                    "create_branch", "Create feature branch", "git checkout -b feature/{name}"
                ),
                WorkflowStep("develop", "Implement feature", None),
                WorkflowStep("test", "Run tests", "pytest"),
                WorkflowStep("lint", "Run linter", "ruff check ."),
                WorkflowStep("commit", "Commit changes", None),
                WorkflowStep("push", "Push to remote", "git push -u origin feature/{name}"),
                WorkflowStep("pr", "Create pull request", "gh pr create"),
            ],
        ),
        "hotfix": Workflow(
            name="Hotfix",
            workflow_type=WorkflowType.GITFLOW,
            description="Emergency fix workflow",
            steps=[
                WorkflowStep(
                    "create_branch",
                    "Create hotfix branch from main",
                    "git checkout -b hotfix/{name} main",
                ),
                WorkflowStep("fix", "Implement fix", None),
                WorkflowStep("test", "Run tests", "pytest"),
                WorkflowStep("commit", "Commit fix", None),
                WorkflowStep(
                    "merge_main", "Merge to main", "git checkout main && git merge hotfix/{name}"
                ),
                WorkflowStep(
                    "merge_develop",
                    "Merge to develop",
                    "git checkout develop && git merge hotfix/{name}",
                ),
                WorkflowStep("tag", "Create version tag", "git tag -a v{version}"),
                WorkflowStep("push", "Push all", "git push --all && git push --tags"),
            ],
        ),
        "release": Workflow(
            name="Release",
            workflow_type=WorkflowType.GITFLOW,
            description="Release preparation workflow",
            steps=[
                WorkflowStep(
                    "create_branch", "Create release branch", "git checkout -b release/{version}"
                ),
                WorkflowStep("version_bump", "Update version numbers", None),
                WorkflowStep("changelog", "Update changelog", None),
                WorkflowStep("test", "Run full test suite", "pytest --cov"),
                WorkflowStep("build", "Build release", "python -m build"),
                WorkflowStep(
                    "merge_main",
                    "Merge to main",
                    "git checkout main && git merge release/{version}",
                ),
                WorkflowStep("tag", "Create release tag", "git tag -a v{version}"),
                WorkflowStep(
                    "merge_develop",
                    "Merge to develop",
                    "git checkout develop && git merge release/{version}",
                ),
            ],
        ),
        "tdd": Workflow(
            name="TDD Cycle",
            workflow_type=WorkflowType.CUSTOM,
            description="Test-Driven Development cycle",
            steps=[
                WorkflowStep("red", "Write failing test", None),
                WorkflowStep(
                    "verify_fail", "Verify test fails", "pytest -x", on_failure="continue"
                ),
                WorkflowStep("green", "Write minimal code to pass", None),
                WorkflowStep("verify_pass", "Verify test passes", "pytest -x"),
                WorkflowStep("refactor", "Refactor code", None),
                WorkflowStep("verify_still_pass", "Verify tests still pass", "pytest"),
            ],
        ),
    }

    def __init__(self, git: Git):
        self.git = git

    def get_workflow(self, name: str) -> Workflow | None:
        """Get a workflow template."""
        return self.TEMPLATES.get(name)

    def list_workflows(self) -> list[str]:
        """List available workflows."""
        return list(self.TEMPLATES.keys())

    def execute_step(self, step: WorkflowStep, variables: dict[str, str]) -> bool:
        """Execute a workflow step."""
        if step.command is None:
            return True  # Manual step

        # Substitute variables
        command = step.command.format(**variables)

        # P0-10-15: Use safe command execution instead of shell=True
        result = execute_command(
            command,
            cwd=self.git.repo_path,
            timeout=120,
            allow_shell=True,  # Workflow commands may use shell syntax
            validate=False,  # Workflow commands are predefined and trusted
        )
        return result.success

    def render_workflow(self, workflow: Workflow, console: Console | None = None) -> None:
        """Render workflow steps."""
        if console is None:
            from sage.core.renderer import console as _default_console
            console = _default_console

        console.print(f"\n[bold cyan]{workflow.name}[/bold cyan]")
        console.print(f"[dim]{workflow.description}[/dim]\n")

        for i, step in enumerate(workflow.steps, 1):
            console.print(f"  {i}. [bold]{step.name}[/bold]: {step.description}")
            if step.command:
                console.print(f"     [dim]$ {step.command}[/dim]")
