"""Synchronous orchestration for the retro-spec command.

Enforces issue state gate → collects artifacts → resolves placement →
conflict preflight → synthesizes via LLM → writes spec.md → optionally
creates a git commit, with best-effort cleanup if a later write or commit
step fails.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from agentic_devtools.cli.git.operations import create_commit, has_local_changes
from agentic_devtools.cli.github.repo_resolution import resolve_github_repo_safe
from agentic_devtools.cli.speckit.hierarchy import ChildEntry, HierarchyNode, load_hierarchy, save_hierarchy
from agentic_devtools.cli.speckit.shared.commit import format_commit_message
from agentic_devtools.cli.speckit.shared.hierarchy import hierarchy_level_for_path

from .artifact_collector import (
    collect_commit_messages,
    discover_related_prs,
    fetch_issue,
    fetch_pr_diffs,
    get_diff_budget,
)
from .placement import resolve_placement
from .synthesis import assemble_context, format_retroactive_spec, synthesize_spec, write_spec_file
from .templates import build_system_prompt


def _prepend_artifact_availability(content: str, notices: list[str]) -> str:
    """Prepend a deterministic artifact-availability section when notices exist."""
    if not notices:
        return content
    return "## Artifact Availability\n\n" + "\n\n".join(notices) + "\n\n" + content


def retro_spec_command(
    issue_number: int,
    specs_root: str | Path | None = None,
    dry_run: bool = False,
    output: str | None = None,
    commit: bool = False,
) -> None:
    """Orchestrate the retro-spec generation command.

    Args:
        issue_number: The closed issue number to generate a spec for.
        specs_root: Path to the specs/ directory. Defaults to ./specs.
        dry_run: If True, print spec to stdout without writing files.
        output: Custom output path for the spec file.
        commit: If True, create a git commit after writing.
    """
    if specs_root is None:
        specs_root = Path.cwd() / "specs"
    specs_root = Path(specs_root)

    if not output and specs_root.exists() and not specs_root.is_dir():
        print(
            f"Error: --specs-root path is not a directory: {specs_root}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Resolve owner/repo from git remote exclusively
    repo_slug = resolve_github_repo_safe()
    if not repo_slug:
        print(
            "Error: Could not determine GitHub repository. "
            "Ensure this is a git repository with a GitHub origin remote configured.",
            file=sys.stderr,
        )
        sys.exit(1)

    owner, repo = repo_slug.split("/", 1)

    if output and commit:
        print("Warning: --commit is ignored when --output is provided.", file=sys.stderr)
        commit = False

    # Phase 1: Validate issue state
    print(f"Fetching issue #{issue_number}...", file=sys.stderr)
    issue = fetch_issue(owner, repo, issue_number)
    print(f"  Title: {issue.title}", file=sys.stderr)
    print(f"  State: {issue.state}", file=sys.stderr)

    # Phase 2: Collect artifacts
    print("Discovering related PRs...", file=sys.stderr)
    prs = discover_related_prs(owner, repo, issue_number)
    print(f"  Found {len(prs)} related PRs.", file=sys.stderr)

    if not prs and not issue.body and not issue.comments:
        print(
            "Error: Insufficient artifacts to generate a spec. The issue has no body, no comments, and no related PRs.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not prs:
        print(
            "  ⚠ Warning: No related PRs found. Spec will be generated from issue body and comments only.",
            file=sys.stderr,
        )

    diffs: list[str] = []
    commits: list[str] = []
    remaining_diff_budget = get_diff_budget()
    included_diff_prs = 0
    omitted_diff_prs = 0
    partially_omitted_diff_prs = 0
    diff_budget_exhausted = False
    for i, pr in enumerate(prs, 1):
        print(f"  Retrieving PR {i}/{len(prs)} #{pr.number}: {pr.title}...", file=sys.stderr)

        # Always collect commit messages, even after the diff budget is exhausted.
        pr_commits = collect_commit_messages(owner, repo, pr.number)
        commits.extend(pr_commits)

        if diff_budget_exhausted or remaining_diff_budget <= 0:
            omitted_diff_prs += 1
            continue

        pr_diffs = fetch_pr_diffs(owner, repo, pr.number)
        pr_added = False
        pr_omitted_due_budget = False
        pr_notice_only = False
        for diff_entry in pr_diffs:
            # Always preserve the file-omission notice emitted by fetch_pr_diffs,
            # regardless of whether it fits within the remaining budget.
            is_omission_notice = diff_entry.startswith("[Diff budget exhausted")
            if not is_omission_notice and len(diff_entry) > remaining_diff_budget:
                pr_omitted_due_budget = True
                diff_budget_exhausted = True
                break
            diffs.append(diff_entry)
            if not is_omission_notice:
                remaining_diff_budget -= len(diff_entry)
                pr_added = True
            else:
                # The inner budget notice means this PR's files were partially omitted;
                # the outer budget loop must also stop after this PR.
                diff_budget_exhausted = True
                if pr_added:
                    # Real diff content was already retained from this PR, but the
                    # inner notice indicates further files were omitted.
                    pr_omitted_due_budget = True
                else:
                    # The very first (and only) entry was a notice — no real diff
                    # content was retained from this PR.
                    pr_notice_only = True
        if pr_added or (not pr_omitted_due_budget and not pr_notice_only):
            included_diff_prs += 1
            if pr_omitted_due_budget:
                partially_omitted_diff_prs += 1
        else:
            # Zero real diff entries were added from this PR: either its first
            # entry exceeded the remaining budget, or fetch_pr_diffs returned
            # only its own inner omission notice with no real diff content.
            omitted_diff_prs += 1

    budget_notice_parts: list[str] = []
    if partially_omitted_diff_prs > 0:
        budget_notice_parts.append(
            "included "
            f"{included_diff_prs} PR(s) but omitted additional diff entries from "
            f"{partially_omitted_diff_prs} partially included PR(s)"
        )
    if omitted_diff_prs > 0:
        if partially_omitted_diff_prs > 0:
            budget_notice_parts.append(f"omitted {omitted_diff_prs} subsequent PR(s)")
        else:
            budget_notice_parts.append(
                f"included {included_diff_prs} PR(s), omitted {omitted_diff_prs} subsequent PR(s)"
            )
    if budget_notice_parts:
        diffs.append(f"[Diff budget exhausted: {'; '.join(budget_notice_parts)}.]")

    # Phase 3: Resolve placement
    if output:
        # Custom output path — skip hierarchy
        target_path = Path(output)
        spec_file = target_path / "spec.md" if target_path.exists() and target_path.is_dir() else target_path
        needs_hierarchy_update = False
        parent_issue = None
    else:
        print("Resolving hierarchy placement...", file=sys.stderr)
        placement = resolve_placement(owner, repo, issue_number, specs_root, issue_title=issue.title)
        target_path = placement.target_path
        spec_file = target_path / "spec.md"
        needs_hierarchy_update = placement.needs_hierarchy_update
        parent_issue = placement.parent_issue
        print(f"  Target path: {target_path}", file=sys.stderr)
        if parent_issue:
            print(f"  Parent issue: #{parent_issue}", file=sys.stderr)

    # Phase 4: Conflict preflight
    existing_spec = (
        spec_file
        if (spec_file.exists() or spec_file.is_symlink())
        else (_find_existing_spec_dir(specs_root, issue_number) if not output else None)
    )
    if existing_spec is not None:
        print(
            f"Error: Target spec already exists at {existing_spec}. "
            "Cannot overwrite existing spec.\n"
            "Remove the existing spec or use a different issue number.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Validate commit mode before the expensive synthesis step.
    # Skip for dry runs: previewing a commit requires no clean working tree.
    if commit and not dry_run and has_local_changes():
        print(
            "Error: Working tree has uncommitted changes or untracked files.\n"
            "Commit, stash, or discard all local changes before generating a "
            "retroactive spec so the resulting commit is scoped to the retro-spec "
            "artifacts only.\n"
            "  • Run `git status` to see outstanding changes.\n"
            "  • Use `git stash` to temporarily shelve them, or\n"
            "    `agdt-git-save-work` to commit them first.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Phase 5: Synthesize spec
    print("Synthesizing spec via LLM...", file=sys.stderr)
    system_prompt = build_system_prompt()
    context = assemble_context(issue, prs, diffs, commits)
    has_implementation_artifacts = bool(prs) and (
        bool(commits) or any(diff_entry and not diff_entry.startswith("[") for diff_entry in diffs)
    )
    artifact_availability_notices: list[str] = []
    if budget_notice_parts:
        artifact_availability_notices.append(
            "> **Warning**: Diff artifacts were truncated because the shared diff budget was exhausted; "
            + "; ".join(budget_notice_parts)
            + "."
        )
    spec_content = synthesize_spec(
        context,
        system_prompt,
        has_implementation_artifacts=has_implementation_artifacts,
        pr_artifacts=prs,
        diff_entries=diffs,
        commit_messages=commits,
    )
    if not has_implementation_artifacts:
        if prs:
            artifact_availability_notices.append(
                "> **Warning**: Related pull request metadata was available, but "
                "usable merged implementation artifacts (diffs/commits) were not; "
                "this document is based on issue evidence and PR metadata only."
            )
        else:
            artifact_availability_notices.append(
                "> **Warning**: No merged pull request artifacts were available; "
                "this document is based on the issue evidence only."
            )
    spec_content = _prepend_artifact_availability(spec_content, artifact_availability_notices)

    # Dry-run: print to stdout and exit
    if dry_run:
        print(f"\n--- DRY RUN: would write to {spec_file} ---\n")
        print(
            format_retroactive_spec(
                spec_content,
                issue_number=issue.number,
                title=issue.title,
                labels=issue.labels,
                milestone=issue.milestone,
            ),
            end="",
        )
        print("\n--- End of dry-run output ---")
        print(f"  Issue: #{issue_number} — {issue.title}", file=sys.stderr)
        print(f"  PRs analyzed: {len(prs)}", file=sys.stderr)
        print(f"  Commits collected: {len(commits)}", file=sys.stderr)
        if needs_hierarchy_update and parent_issue:
            hierarchy_path_preview = target_path.parent / "hierarchy.yml"
            print(
                f"  Would register #{issue_number} in parent hierarchy: {hierarchy_path_preview}",
                file=sys.stderr,
            )
        print("No changes made.", file=sys.stderr)
        return

    # Phase 6: Write spec file
    print(f"Writing spec to {spec_file}...", file=sys.stderr)
    target_dir = spec_file.parent
    target_dir_existed = target_dir.exists()
    # Hierarchy rollback state — set in Phase 8 if a hierarchy update is performed.
    hierarchy_path: Path | None = None
    hierarchy_existed: bool = False
    original_hierarchy_content: str = ""
    try:
        write_spec_file(
            spec_content,
            target_dir,
            output_file=spec_file,
            issue_number=issue.number,
            title=issue.title,
            labels=issue.labels,
            milestone=issue.milestone,
        )

        # Phase 8: Register child in parent hierarchy.yml.
        # speckit.agdt:nest processes only {N}-{slug} flat directories and exits
        # before planning when none exist, so it cannot register a child placed
        # directly into an existing numeric parent directory by retro-spec.
        # retro-spec therefore performs the registration itself here.
        if needs_hierarchy_update and parent_issue:
            _pending_hierarchy_path = target_path.parent / "hierarchy.yml"
            hierarchy_existed = _pending_hierarchy_path.exists()
            original_hierarchy_content = (
                _pending_hierarchy_path.read_text(encoding="utf-8") if hierarchy_existed else ""
            )
            written = _register_child_in_hierarchy(
                hierarchy_path=_pending_hierarchy_path,
                parent_dir=target_path.parent,
                specs_root=specs_root,
                issue_number=issue_number,
                issue_title=issue.title,
            )
            if written:
                hierarchy_path = _pending_hierarchy_path
                print(
                    f"Registered issue #{issue_number} in parent hierarchy: {hierarchy_path}",
                    file=sys.stderr,
                )

        # Phase 9: Create git commit if requested
        if commit:
            commit_msg = format_commit_message(
                commit_type="docs",
                scope=f"#{issue_number}",
                description="generate retroactive spec from implementation artifacts",
                issue=f"#{issue_number}",
                co_authored=True,
            )

            files_to_stage = [spec_file]
            if hierarchy_path is not None:
                files_to_stage.append(hierarchy_path)
            _stage_retro_spec(files_to_stage)
            _validate_staged_files(files_to_stage)
            create_commit(message=commit_msg, dry_run=False)
    except (Exception, SystemExit):
        _cleanup_partial_retro_spec(
            spec_file=spec_file,
            target_dir=target_dir,
            target_dir_existed=target_dir_existed,
            specs_root=specs_root,
            hierarchy_path=hierarchy_path,
            hierarchy_existed=hierarchy_existed,
            original_hierarchy_content=original_hierarchy_content,
            reset_index=commit,
        )
        raise

    print(f"Retroactive spec generated for issue #{issue_number}.", file=sys.stderr)
    if commit:
        print("Changes committed.", file=sys.stderr)


def _stage_retro_spec(files: list[Path]) -> None:
    """Stage only files generated by this retro-spec invocation."""
    git_root = _get_git_root()
    if git_root is None:
        raise RuntimeError("Could not determine the repository root while staging the retroactive spec.")
    try:
        relative_files = [path.resolve().relative_to(git_root.resolve()).as_posix() for path in files]
    except ValueError as exc:
        raise RuntimeError("Generated retro-spec files must be inside the repository.") from exc

    result = subprocess.run(
        ["git", "add", "--", *relative_files],
        capture_output=True,
        text=True,
        shell=False,
        cwd=git_root,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or f"exit code {result.returncode}"
        raise RuntimeError(f"git add failed for retro-spec files: {detail}")


def _validate_staged_files(expected_files: list[Path]) -> None:
    """Abort if the index contains files beyond those generated by this invocation.

    Raises RuntimeError when unexpected staged changes are detected, protecting the
    "stage only generated files" contract even when another process staged files
    during LLM synthesis.
    """
    git_root = _get_git_root()
    if git_root is None:
        raise RuntimeError("Could not determine the repository root while validating staged files.")

    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
        shell=False,
        cwd=git_root,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or f"exit code {result.returncode}"
        raise RuntimeError(f"git diff --cached failed while validating staged files: {detail}")

    staged_paths = {(git_root / line).resolve() for line in result.stdout.splitlines() if line}
    expected_paths = {path.resolve() for path in expected_files}
    unexpected = staged_paths - expected_paths
    if unexpected:
        git_root_resolved = git_root.resolve()
        relative_names = sorted(str(p.relative_to(git_root_resolved)) for p in unexpected)
        raise RuntimeError(
            "Unexpected files are staged in the index. Aborting commit to preserve the "
            "'stage only generated files' contract. Unexpected paths: " + ", ".join(relative_names)
        )


def _register_child_in_hierarchy(
    *,
    hierarchy_path: Path,
    parent_dir: Path,
    specs_root: Path,
    issue_number: int,
    issue_title: str,
) -> bool:
    """Register ``issue_number`` as a child in the parent's ``hierarchy.yml``.

    speckit.agdt:nest only processes ``{N}-{slug}`` flat directories and exits
    before planning when none exist, so it cannot register a child placed
    directly into an existing numeric parent directory by retro-spec.
    retro-spec calls this helper instead.

    If ``hierarchy_path`` already exists the child entry is merged in,
    preserving all other metadata.  If it does not exist a minimal node is
    created.  A child entry that is already present with identical metadata
    is a no-op (returns ``False`` and the file is not rewritten); a
    conflicting definition raises ``ValueError``.

    Args:
        hierarchy_path: Absolute path to the parent's ``hierarchy.yml``.
        parent_dir: Absolute path to the parent spec directory.
        specs_root: Absolute path to the specs root directory.
        issue_number: Child issue number to register.
        issue_title: Human-readable title for the child entry.

    Returns:
        ``True`` if the file was written (new entry added or file created),
        ``False`` if the child was already present with matching metadata.

    Raises:
        ValueError: If an existing child entry has conflicting metadata.
        OSError: If the hierarchy file cannot be read or written.
        Exception: YAML parse errors from ``load_hierarchy`` propagate unchanged
            if the existing ``hierarchy.yml`` is malformed.
    """
    child_entry = ChildEntry(key=str(issue_number), title=issue_title, order=None)

    if hierarchy_path.exists():
        node = load_hierarchy(hierarchy_path)
        existing = {c.key: c for c in node.children}
        existing_child = existing.get(child_entry.key)
        if existing_child is None:
            node.children.append(child_entry)
        elif existing_child.title != child_entry.title:
            raise ValueError(
                f"Conflicting child definition for issue #{issue_number} in "
                f"'{hierarchy_path}': existing title={existing_child.title!r}, "
                f"new title={child_entry.title!r}. Resolve the existing "
                "hierarchy.yml entry before running retro-spec."
            )
        else:
            # Child already registered with matching metadata — no write needed.
            return False
    else:
        parent_key: str | None = None
        grandparent_dir = parent_dir.parent
        if grandparent_dir != specs_root and grandparent_dir.name.isdigit():
            parent_key = grandparent_dir.name
        node = HierarchyNode(
            title=f"Issue #{parent_dir.name}" if parent_dir.name.isdigit() else parent_dir.name,
            level=hierarchy_level_for_path(parent_dir, specs_root),
            parent=parent_key,
            children=[child_entry],
        )

    save_hierarchy(node, hierarchy_path)
    return True


def _find_existing_spec_dir(specs_root: Path, issue_number: int) -> Path | None:
    """Find any existing issue spec directory under ``specs_root`` recursively."""
    if not specs_root.is_dir():
        return None
    prefix = f"{issue_number}-"
    for candidate in specs_root.rglob("*"):
        if candidate.is_dir() and (candidate.name == str(issue_number) or candidate.name.startswith(prefix)):
            return candidate
    return None


def _cleanup_partial_retro_spec(
    *,
    spec_file: Path,
    target_dir: Path,
    target_dir_existed: bool,
    specs_root: Path,
    hierarchy_path: Path | None = None,
    hierarchy_existed: bool = False,
    original_hierarchy_content: str = "",
    reset_index: bool = True,
) -> None:
    """Best-effort cleanup for failed retro-spec runs after the write phase begins."""
    if reset_index:
        git_root = _get_git_root()
        relative_spec: str | None = None
        if git_root is not None:
            try:
                relative_spec = spec_file.resolve().relative_to(git_root.resolve()).as_posix()
            except ValueError:
                pass
        if relative_spec is None:
            # Without a trustworthy root-relative path, a bare `git reset` would
            # silently unstage unrelated staged changes.  Skip index mutation and
            # warn instead so the caller can clean up manually.
            print(
                "Warning: could not determine spec path relative to git root; "
                "git index was not modified during retro-spec cleanup.",
                file=sys.stderr,
            )
        else:
            files_to_unstage = [relative_spec]
            if hierarchy_path is not None and git_root is not None:
                try:
                    relative_hierarchy = hierarchy_path.resolve().relative_to(git_root.resolve()).as_posix()
                    files_to_unstage.append(relative_hierarchy)
                except ValueError:
                    pass
            try:
                # Unstage only the generated files, leaving any unrelated staged
                # changes untouched.
                reset_result = subprocess.run(
                    ["git", "restore", "--staged", "--", *files_to_unstage],
                    capture_output=True,
                    text=True,
                    shell=False,
                    cwd=git_root,
                )
                if reset_result.returncode != 0:
                    failure_detail = reset_result.stderr.strip() or f"exit code {reset_result.returncode}"
                    print(
                        f"Warning: could not reset git index during retro-spec cleanup: {failure_detail}",
                        file=sys.stderr,
                    )
            except OSError as exc:
                print(f"Warning: could not reset git index during retro-spec cleanup: {exc}", file=sys.stderr)

    # Roll back the hierarchy.yml change: restore original content or remove the newly created file.
    if hierarchy_path is not None:
        try:
            if hierarchy_existed:
                hierarchy_path.write_text(original_hierarchy_content, encoding="utf-8")
            elif hierarchy_path.exists():
                hierarchy_path.unlink()
        except OSError as exc:
            print(f"Warning: could not roll back hierarchy file '{hierarchy_path}': {exc}", file=sys.stderr)

    try:
        if spec_file.exists():
            spec_file.unlink()
    except OSError as exc:
        print(f"Warning: could not remove partial retro-spec file '{spec_file}': {exc}", file=sys.stderr)

    if not target_dir_existed:
        stop_at = Path(specs_root)
        if not _is_relative_to(target_dir, stop_at):
            # --output pointed outside specs_root: only prune the directory we
            # created; never walk upward past its parent into unrelated trees.
            stop_at = target_dir.parent
        _prune_empty_dirs(target_dir, stop_at=stop_at)


def _get_git_root() -> Path | None:
    """Return the absolute path to the git repository root, or None if not in a repo."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            shell=False,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip())


def _is_relative_to(path: Path, other: Path) -> bool:
    """Return True if resolved *path* is equal to or nested under resolved *other*."""
    try:
        path.resolve().relative_to(other.resolve())
    except ValueError:
        return False
    return True


def _prune_empty_dirs(path: Path, *, stop_at: Path) -> None:
    """Remove newly-created empty directories up to, but not including, stop_at."""
    current = path
    stop_path = stop_at.resolve()
    while current.exists() and current.resolve() != stop_path:
        try:
            current.rmdir()
        except OSError:
            break
        current = current.parent
