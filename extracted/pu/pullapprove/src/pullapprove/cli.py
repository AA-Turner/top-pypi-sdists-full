from __future__ import annotations

import os
import subprocess
import sys
from collections import Counter, deque
from pathlib import Path
from textwrap import dedent

import click
from pydantic import ValidationError

from . import git
from .config import (
    CONFIG_FILENAME,
    CompiledConfigModels,
    ConfigModel,
    ConfigModels,
    is_config_filename,
    is_config_path,
)
from .diff import DiffFile, DiffHunk, filter_diff_text, iter_file_hunks
from .matches import ChangeMatches, match_diff, match_files
from .printer import MatchesPrinter
from .text import plural
from .trust import TRUST_FAMILIES, Trust, trust_diff, trust_label


@click.group()
@click.version_option(package_name="pullapprove")
@click.pass_context
def cli(ctx: click.Context) -> None:
    pass


@cli.command()
@click.option("--filename", default=CONFIG_FILENAME, help="Configuration filename")
def init(filename: str) -> None:
    """Create a new config file"""
    config_path = Path(filename)
    if config_path.exists():
        click.secho(f"{filename} already exists!", fg="red")
        sys.exit(1)

    # Could we use blame to guess?
    # go straight to agent?
    # gh auth status can give us the user? or ask what's their username?
    # keep it simple - agent can do more when I get to it

    contents = f"""
    [[scopes]]
    name = "default"
    paths = ["**/*"]
    request = 1
    require = 1
    reviewers = ["<YOU>"]

    [[scopes]]
    name = "pullapprove"
    paths = ["**/{CONFIG_FILENAME}"]
    request = 1
    require = 1
    reviewers = ["<YOU>"]
    """
    config_path.write_text(dedent(contents).strip() + "\n")
    click.secho(f"Created {filename}")


@cli.command()
@click.option("--quiet", is_flag=True)
def check(quiet: bool) -> ConfigModels:
    """
    Validate configuration files
    """

    if not quiet:
        if Path(".pullapprove.yml").exists():
            click.secho(
                f"{click.style('[Warning]', fg='yellow')} This repo still contains a PullApprove v3 config file (.pullapprove.yml). Consider migrating it to PullApprove v5."
            )
        if Path("CODEOWNERS").exists():
            click.secho(
                f"{click.style('[Warning]', fg='yellow')} This repo still contains a CODEOWNERS file. Consider migrating it to PullApprove v5."
            )
        if Path("docs/CODEOWNERS").exists():
            click.secho(
                f"{click.style('[Warning]', fg='yellow')} This repo still contains a CODEOWNERS file (docs/CODEOWNERS). Consider migrating it to PullApprove v5."
            )
        if Path(".github/CODEOWNERS").exists():
            click.secho(
                f"{click.style('[Warning]', fg='yellow')} This repo still contains a CODEOWNERS file (.github/CODEOWNERS). Consider migrating it to PullApprove v5."
            )

    errors = {}
    configs = ConfigModels(root={})

    for root, _, files in os.walk("."):
        for f in files:
            if is_config_filename(f):
                config_path = Path(root) / f

                if not quiet:
                    click.echo(config_path, nl=False)
                try:
                    configs.add_config(
                        ConfigModel.from_filesystem(config_path), config_path
                    )

                    if not quiet:
                        click.secho(" -> OK", fg="green")
                except ValidationError as e:
                    if not quiet:
                        click.secho(" -> ERROR", fg="red")

                    errors[config_path] = e

    for path, error in errors.items():
        click.secho(str(path), fg="red", err=True)
        click.echo(str(error), err=True)

    if errors:
        raise click.ClickException("Configuration validation failed.")

    # Compile the whole set offline to catch what per-file validation
    # can't: unknown aliases, missing/circular extends, and invalid
    # combinations like wildcard+negation. teams=None leaves `@team` refs
    # unexpanded — the same partial resolution `match`/`coverage` use —
    # so anything that errors here would also error in production.
    try:
        configs.compiled()
    except (ValidationError, ValueError) as e:
        click.secho(f"ERROR: {e}", fg="red", err=True)
        raise click.ClickException("Configuration validation failed.")

    if not configs and not quiet:
        click.secho(f"No {CONFIG_FILENAME} files found.", fg="red", err=True)
        sys.exit(1)

    return configs


def _compiled_configs_at(ref: str) -> CompiledConfigModels:
    """The configs committed at `ref`, which is what PullApprove enforces on a
    pull request into it. A pull request's own config changes only take
    effect once they merge."""
    try:
        contents = {
            path: git.git_file_at(path=Path("."), ref=ref, file_path=path)
            for path in git.git_ls_tree(path=Path("."), ref=ref)
            if is_config_path(path)
        }
    except subprocess.CalledProcessError as exc:
        raise click.ClickException(f"Could not read the configs at {ref}.") from exc

    try:
        return ConfigModels.from_contents(contents).compiled()
    except (ValidationError, ValueError) as e:
        raise click.ClickException(f"The configs at {ref} are invalid: {e}") from e


@cli.command()
@click.option("--changed", is_flag=True, help="Show only changed files")
@click.option("--staged", is_flag=True, help="Show only staged files")
@click.option("--diff", is_flag=True, help="Show diff content with matches")
@click.option(
    "--by-scope", is_flag=True, help="Organize output by scope instead of by path"
)
@click.option(
    "--scope",
    multiple=True,
    help="Filter to show only files matching these scopes (can be used multiple times)",
)
@click.option(
    "--base",
    help="Match HEAD as a pull request into this branch or commit, "
    "using the configs committed there",
)
@click.option(
    "--author",
    help="Match as a pull request by this user, applying each scope's `authors`",
)
@click.option("--json", "as_json", is_flag=True, help="Output matches as JSON")
@click.argument("paths", nargs=-1, type=click.Path())
@click.pass_context
def match(
    ctx: click.Context,
    changed: bool,
    staged: bool,
    diff: bool,
    by_scope: bool,
    scope: tuple[str, ...],
    base: str | None,
    author: str | None,
    as_json: bool,
    paths: tuple[str, ...],
) -> None:
    """
    Show files and their matching scopes

    If PATHS are provided, only those specific paths will be matched.
    Directories will be recursively expanded to include all files within them.
    Otherwise, all files in the repository will be matched.

    With --base, HEAD is matched the way PullApprove would match a pull
    request into that branch: the diff since HEAD branched off it, against
    the configs committed there.
    """
    if as_json and (by_scope or scope):
        # JSON is every match, for the script to slice however it wants
        raise click.UsageError("--json can't be combined with --by-scope or --scope.")

    if paths and (diff or staged or changed or base):
        raise click.UsageError(
            "Cannot use --diff, --staged, --changed, or --base with specific paths."
        )

    if base and (staged or changed):
        raise click.UsageError("--base can't be combined with --staged or --changed.")

    if base:
        # Resolved once, so the configs and the diff come from the same commit
        try:
            base = git.git_commit_sha(path=Path("."), ref=base)
        except subprocess.CalledProcessError as exc:
            # Usually a shallow clone that never fetched the base
            raise click.ClickException(
                f"Could not find the commit {base}. --base needs it and the "
                "history back to where HEAD branched off it (in GitHub "
                "Actions, checkout with fetch-depth: 0)."
            ) from exc
        configs = _compiled_configs_at(base)
    else:
        configs = ctx.invoke(check, quiet=True).compiled()

    if not configs:
        raise click.ClickException("No valid configurations found.")

    # A misspelled --scope would otherwise just look like nothing matched
    known_scopes: set[str] = set()
    for config in configs.root.values():
        for config_scope in config.scopes:
            known_scopes.add(config_scope.name)
    unknown_scopes = [s for s in scope if s not in known_scopes]
    if unknown_scopes:
        raise click.UsageError(f"Unknown scope: {', '.join(unknown_scopes)}")

    if author:
        # PullApprove drops the scopes an author is excluded from before
        # matching, so which scope owns a path can depend on who opened the
        # pull request
        try:
            configs = configs.filter_for_pullrequest(author_username=author)
        except ValueError as e:
            raise click.ClickException(
                f"Can't apply --author: {e}. "
                "The command line can't look up team members."
            ) from e

    matches, all_files = _match_changes(
        configs=configs,
        paths=paths,
        changed=changed,
        staged=staged,
        diff=diff,
        base=base,
    )

    printer = MatchesPrinter(matches=matches, all_files=all_files)
    if as_json:
        printer.print_json()
    elif by_scope:
        printer.print_by_scope(scope_filter=scope)
    else:
        printer.print_by_path(scope_filter=scope)


def _match_changes(
    *,
    configs: CompiledConfigModels,
    paths: tuple[str, ...],
    changed: bool,
    staged: bool,
    diff: bool,
    base: str | None,
) -> tuple[ChangeMatches, list[str]]:
    """Match the files `match` was pointed at, returning the matches and every
    one of those files (including the ones no scope owns)."""
    if paths:
        # Match only the git-tracked files at or under the provided paths
        all_git_files = set(git.git_ls_files(Path(".")))
        expanded_paths = []

        for path_str in paths:
            path = Path(path_str)
            if path.is_dir():
                # Filter git files that are within this directory
                dir_prefix = str(path) + "/"
                for git_file in all_git_files:
                    if git_file.startswith(dir_prefix) or git_file == str(path):
                        expanded_paths.append(git_file)
            elif path.is_file() or str(path) in all_git_files:
                # Include if it's a git-tracked file
                if str(path) in all_git_files:
                    expanded_paths.append(str(path))
                else:
                    click.secho(
                        f"File not tracked by git: {path}", fg="yellow", err=True
                    )
            else:
                click.secho(
                    f"Path does not exist or not tracked by git: {path}",
                    fg="yellow",
                    err=True,
                )

        return match_files(configs, iter(expanded_paths)), expanded_paths

    if diff or staged or base:
        diff_args = list(git.HOST_DIFF_ARGS)
        if staged:
            diff_args.append("--staged")
        if base:
            diff_args.append(f"{base}...HEAD")

        try:
            diff_results = match_diff(
                configs, git.git_diff_stream(Path("."), *diff_args)
            )
        except subprocess.CalledProcessError as exc:
            # git failed (not a repo, bad state) — it already explained itself on
            # stderr, so exit cleanly instead of dumping a traceback.
            if base:
                # Usually a shallow clone that stops before the merge base
                raise click.ClickException(
                    f"Could not diff {base}...HEAD. The history back to where "
                    "HEAD branched off has to be fetched (in GitHub Actions, "
                    "checkout with fetch-depth: 0)."
                ) from exc
            raise click.ClickException("Could not read a diff from git.") from exc
        # For diff mode, we only show files in the diff
        return diff_results.matches, diff_results.changed_paths

    if changed:
        # For changed mode, we only show changed files
        all_files = git.git_ls_changes(Path("."))
    else:
        # For normal mode, show all files to see gaps
        all_files = list(git.git_ls_files(Path(".")))
    return match_files(configs, iter(all_files)), all_files


@cli.command()
@click.option(
    "--check",
    "check_flag",
    is_flag=True,
    help="Exit with non-zero status if coverage is incomplete",
)
@click.argument("path", type=click.Path(exists=True), default=".")
@click.pass_context
def coverage(ctx: click.Context, path: str, check_flag: bool) -> None:
    """
    Calculate file coverage for review scopes
    """
    configs = ctx.invoke(check, quiet=True).compiled()

    num_matched = 0
    num_total = 0
    uncovered_files = []

    # First, get all files to know the total count for progress bar
    all_files = list(git.git_ls_files(Path(path)))

    if not all_files:
        click.echo("No files found")
        return

    # Process files with progress bar
    with click.progressbar(
        all_files, label="Analyzing coverage", show_percent=True, show_pos=True
    ) as files:
        # Use match_files to get proper scope matching including code patterns
        results = match_files(configs, iter(files))

        # Count files with and without scope matches
        for path_str, path_match in results.paths.items():
            if path_match.scopes:
                num_matched += 1
            else:
                uncovered_files.append(path_str)
            num_total += 1

        # Also count files that weren't in the results (no scope matches at all)
        for f in all_files:
            if f not in results.paths:
                uncovered_files.append(f)
                num_total += 1

    percentage = (num_matched / num_total) * 100

    # Display coverage statistics
    if num_matched == num_total:
        click.secho(f"\n✓ {num_matched}/{num_total} files covered (100.0%)", fg="green")
    else:
        # Show uncovered files
        if uncovered_files:
            click.echo("\nUncovered files:")
            for file in sorted(uncovered_files)[:10]:  # Show first 10
                click.echo(f"  - {file}")
            if len(uncovered_files) > 10:
                click.echo(f"  ...and {len(uncovered_files) - 10} more")

        click.secho(
            f"\n{num_matched}/{num_total} files covered ({percentage:.1f}%)",
            fg="yellow",
        )

    if check_flag and num_matched != num_total:
        sys.exit(1)


@cli.command(
    "diff",
    context_settings={
        "ignore_unknown_options": True,
        # Everything from the first git argument onward is git's, verbatim —
        # including a `--` separator, which click otherwise swallows. Without
        # this, `pullapprove diff HEAD -- deleted.py` reaches git as
        # `diff HEAD deleted.py`, and git refuses a path it can't also read as
        # a revision. The cost is that PullApprove's own flags have to come
        # first, which the help text says.
        "allow_interspersed_args": False,
    },
)
@click.option(
    "--hide",
    "hide_families",
    multiple=True,
    help="Hide only these label families, e.g. formatting (repeatable). "
    "Default: hide every labeled hunk.",
)
@click.option(
    "--no-pager",
    is_flag=True,
    help="Write to stdout instead of paging (paging is the default at a terminal).",
)
@click.option(
    "--quiet", is_flag=True, help="Don't print the hidden-hunk summary to stderr."
)
@click.argument("git_diff_args", nargs=-1, type=click.UNPROCESSED)
def diff(
    hide_families: tuple[str, ...],
    no_pager: bool,
    quiet: bool,
    git_diff_args: tuple[str, ...],
) -> None:
    """
    Show a diff with mechanically-trivial hunks hidden — a trust-aware `git diff`.

    Runs `git diff`, forwarding any extra arguments (`--staged`, revisions,
    pathspecs); with no arguments, piped stdin is read instead. Trusted hunks —
    lockfiles, whitespace, formatting, comments, imports, type annotations — are
    dropped, and the result stays a valid unified diff. At a terminal the output
    is paged through git's pager (like `git diff`); when piped it goes straight
    to stdout:

        pullapprove diff                  # paged, an alternative to `git diff`
        pullapprove diff --staged         # forwarded to git
        pullapprove diff main -- app/     # `--` and pathspecs reach git intact
        git diff | pullapprove diff       # paged
        git diff | pullapprove diff --no-pager | delta

    PullApprove's own options (--hide, --no-pager, --quiet) must come
    before the first git argument. Everything from there on is handed to git
    untouched, so `--` and pathspecs mean to git exactly what they always do.
    """
    # --hide takes a family (e.g. formatting) or a full label (formatting:style).
    # Reject typos up front so a misspelled filter can't silently hide everything.
    known = TRUST_FAMILIES | {label.value for label in Trust}
    unknown = [name for name in hide_families if name not in known]
    if unknown:
        raise click.BadParameter(
            f"unknown trust {'family' if len(unknown) == 1 else 'families'}: "
            f"{', '.join(unknown)}. "
            f"Valid families: {', '.join(sorted(TRUST_FAMILIES))}.",
            param_hint="--hide",
        )

    diff_text = _read_diff(git_diff_args)

    def is_hidden(label: Trust) -> bool:
        if not hide_families:
            return True
        return label in hide_families or label.family in hide_families

    # Classify each hunk, queueing one keep/hide decision per hunk in document
    # order. `filter_diff_text` re-parses the same lines with the same header
    # parsers, so its `keep_hunk` calls arrive in that same order and the queue
    # joins the two walks — no coordinate keys needed (concatenated multi-commit
    # input like `git log -p` can repeat identical coordinates). The shared
    # `split("\n")` is what guarantees the alignment: `str.splitlines` also
    # breaks on `\r` and other separators, which could let the two walks see
    # different lines.
    keep: deque[bool] = deque()
    counts: Counter[str] = Counter()
    for file, hunk in iter_file_hunks(diff_text.split("\n")):
        label = trust_label(file, hunk)
        if label and is_hidden(label):
            keep.append(False)
            counts[label] += 1
        else:
            keep.append(True)

    filtered = filter_diff_text(
        diff_text, lambda path, old_line, new_line: keep.popleft()
    )

    # Page at a terminal like git does; pipe straight through when redirected.
    if no_pager or not sys.stdout.isatty():
        click.echo(filtered, nl=False)
    else:
        git.page(filtered)

    if not quiet and counts:
        total = sum(counts.values())
        breakdown = ", ".join(f"{label} ({n})" for label, n in sorted(counts.items()))
        click.secho(
            f"Hid {total} {plural(total, 'hunk')}: {breakdown}",
            fg="yellow",
            err=True,
        )


def _read_diff(git_diff_args: tuple[str, ...]) -> str:
    """Read a unified diff: from `git diff` when arguments were given, from piped
    stdin otherwise.

    Explicit arguments always win — hooks, CI, and cron run with stdin redirected
    from /dev/null (not a tty), and `pullapprove diff --staged` there must run
    git, not silently read an empty stdin."""
    if not git_diff_args and not sys.stdin.isatty():
        return sys.stdin.read()
    try:
        # Run from the caller's cwd (not the repo root) so any forwarded pathspec
        # is resolved relative to where the user invoked us, matching `git diff`.
        # Git still emits repo-root-relative paths in the diff body regardless.
        return "".join(git.git_diff_stream(Path.cwd(), *git_diff_args))
    except subprocess.CalledProcessError as exc:
        # Not a git repo, or git rejected the arguments — git already explained
        # why on stderr, so exit cleanly instead of dumping a traceback.
        raise click.ClickException("Could not read a diff from git.") from exc


@cli.command("trust", context_settings={"ignore_unknown_options": True})
@click.option(
    "--list",
    "list_hunks",
    is_flag=True,
    help="List every hunk and its trust label, grouped by file.",
)
@click.argument("git_diff_args", nargs=-1, type=click.UNPROCESSED)
def trust(list_hunks: bool, git_diff_args: tuple[str, ...]) -> None:
    """
    Report what the trust classifier identifies in a diff.

    Runs `git diff`, forwarding any extra arguments (`--staged`, revisions,
    pathspecs); with no arguments, piped stdin is read instead. The default
    prints a summary of how much of the change is mechanical; --list prints
    every hunk and its label, so you can see — and debug — exactly what the
    classifier identifies.
    """
    files = trust_diff(_read_diff(git_diff_args))
    if list_hunks:
        _trust_list(files)
    else:
        _trust_summary(files)


def _hunk_header(hunk: DiffHunk) -> str:
    old = (
        f"{hunk.old_line}"
        if hunk.old_length is None
        else f"{hunk.old_line},{hunk.old_length}"
    )
    new = (
        f"{hunk.new_line}"
        if hunk.new_length is None
        else f"{hunk.new_line},{hunk.new_length}"
    )
    return f"@@ -{old} +{new} @@"


def _trust_list(files: list[DiffFile]) -> None:
    hunks = [(file, hunk) for file in files for hunk in file.hunks]
    if not hunks:
        click.echo("No changes.")
        return
    width = max(len(_hunk_header(hunk)) for _, hunk in hunks)
    current_path = None
    for file, hunk in hunks:
        if file.new_path != current_path:
            current_path = file.new_path
            click.secho(current_path, bold=True)
        header = _hunk_header(hunk).ljust(width)
        label = (
            click.style(hunk.trust, fg="green")
            if hunk.trust
            else click.style("needs review", fg="yellow")
        )
        click.echo(f"  {header}  {label}")


def _trust_summary(files: list[DiffFile]) -> None:
    all_hunks = [hunk for file in files for hunk in file.hunks]
    total = len(all_hunks)
    if not total:
        click.echo("No changes.")
        return

    counts = Counter(hunk.trust for hunk in all_hunks if hunk.trust)
    n_trusted = sum(counts.values())
    n_review = total - n_trusted

    def pct(n: int) -> int:
        return round(n / total * 100)

    click.echo(
        f"{total} {plural(total, 'hunk')} · {len(files)} {plural(len(files), 'file')}"
    )

    click.secho(f"  {n_trusted} trusted ({pct(n_trusted)}%)", fg="green")
    if counts:
        width = max(len(label) for label in counts)
        for label, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
            click.echo(f"     {label.ljust(width)}  {n:>3}")
    click.secho(f"  {n_review} need review ({pct(n_review)}%)", fg="yellow")

    fully = [
        file.new_path
        for file in files
        if file.hunks and all(hunk.trust for hunk in file.hunks)
    ]
    if fully:
        shown = ", ".join(fully[:10])
        more = f" +{len(fully) - 10} more" if len(fully) > 10 else ""
        click.echo(
            f"  {len(fully)} {plural(len(fully), 'file')} fully trusted: {shown}{more}"
        )


# list - find open PRs, find status url and send json request (needs PA token)
