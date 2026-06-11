#!/usr/bin/env python3

"""Updates local Gerrit changes"""
# ruff: noqa: S603 `subprocess` call: check for execution of untrusted input

import asyncio
import logging
import re
import shlex
import subprocess
import sys
from argparse import ArgumentParser
from argparse import Namespace as Args
from collections.abc import Mapping, Sequence
from contextlib import suppress

from aiohttp import ConnectionTimeoutError
from rich import traceback
from rich.console import Console
from rich.status import Status
from rich.table import Table
from trickkiste.logging_helper import apply_common_logging_cli_args, setup_logging

from cwz.gerrit_utils.client import (
    GerritChange,
    GerritClient,
    apply_common_gerrit_cli_args,
    with_gerrit_client,
)


def parse_arguments(args: Sequence[str]) -> Args:
    """Parse command line arguments and return Args object"""
    parser = ArgumentParser("update-gerrit-changes", description="Update local Gerrit commits")
    apply_common_logging_cli_args(parser)
    apply_common_gerrit_cli_args(parser)
    return parser.parse_args(args)


@with_gerrit_client(populate=False)
async def update_gerrit_changes(
    cli_args: Args,  # noqa: ARG001
    status: Status,
    gerrit_client: GerritClient,
) -> None:
    """Display local commit stack together with remote status"""

    async def gerrit_status(commit_sha: str, changes: Sequence[GerritChange]) -> str:
        revisions = changes[0].revisions
        if commit_sha == changes[0].current_revision:
            return f"[bright_blue]same as most recent {changes[0].current_revision_number}[/]"

        local_diff = git_show(commit_sha)

        for commit_id, revision in reversed(list(revisions.items())):
            if not cmd_run(f"git cat-file -p {commit_id}", check=False):
                status.update(f"fetch commit {commit_id[:10]}..")
                cmd_run(f"git fetch origin {commit_id}")
            this_diff = git_show(commit_id)
            if local_diff == this_diff:
                if revision.number == len(revisions):
                    return f"[green]similar as remote {revision.number}[/]"
                return f"[yellow]remote has updates {revision.number}!={len(revisions)}[/]"

        return f"[orange_red1]differs from all {len(revisions)} revisions[/]"

    status.start()
    status.update("Fetch local git state")
    ancestor = current_ancestor()
    merge_base = local_merge_base(f"origin/{ancestor}")
    commits = gerrit_change_ids(merge_base)
    status.update(f"{ancestor=} {merge_base=} {len(commits)=} {gerrit_client}")
    table = Table("Commit", "Change", "Status")

    for commit_sha, (short_message, change_id) in commits.items():
        change_id_str = f"{(change_id and f'[orchid1]{change_id[:8]}[/]') or '-'}"
        status.update(f"fetch changes for {change_id_str}..")
        # changes = (await gerrit_client.get_change_sets(change_id)) if change_id else None
        # fixme(frans): add branches column
        # fixme(frans): show commit ids (with links)
        changes = [
            change
            for change in ((await gerrit_client.get_change_sets(change_id)) if change_id else [])
            # fixme(frans): allow for custom branches
            if change.branch == ancestor
        ]
        assert len(changes) in (0, 1), f"{change_id=}, {len(changes)=}"
        change = changes[0] if changes else None
        link = f"{gerrit_client.url}/c/{change.project}/+/{change.number}" if change else ""

        table.add_row(
            f"[deep_sky_blue2]{commit_sha[:10]}[/] [italic bright_yellow]{short_message}[/]",
            f"[link={link}]{change_id_str}[/]" if link else change_id_str,
            (
                "no Change-Id"
                if change_id is None
                else "[magenta]not in review yet[/magenta]"
                if not changes
                else (await gerrit_status(commit_sha, changes))
            ),
        )

    console.print(table)


def git_show(commitish: str) -> str:
    """Local merge base"""
    return cmd_run(f"git show {commitish}").split("\n", maxsplit=1)[-1]


def local_merge_base(commitish: str) -> str:
    """Local merge base"""
    return cmd_run_lines(f"git merge-base HEAD {commitish}")[0]


def current_ancestor() -> str:
    """Checkmk specific: returns the name of the 'production branch' we're on"""
    return sorted(
        (int(cmd_run_lines(f"git rev-list --max-count=1000 --count HEAD...origin/{b}")[0]), b)
        for b in ("master", "2.5.0", "2.4.0", "2.3.0", "2.2.0")
    )[0][1]


def gerrit_change_ids(base: str) -> Mapping[str, tuple[str, None | str]]:
    """Returns a mapping commit-ID -> Gerrit-Change-Id"""
    git_log_result = cmd_run(f"git log {base}..HEAD --format=%H%x00%B%x01")
    return {
        commit_id.lstrip(): (
            body.split("\n", maxsplit=1)[0],
            (
                m.group(1)
                if (m := re.search(r"^Change-Id:\s*(I[0-9a-f]+)", body, re.MULTILINE))
                else None
            ),
        )
        for entry in git_log_result.split("\x01")
        if "\x00" in entry
        for commit_id, body in [entry.split("\x00", 1)]
    }


def cmd_run(cmd: str | Sequence[str], *, check: bool = True) -> str:
    """Run a command, return stdout lines, explode when it fails"""
    cmd_list = shlex.split(cmd) if isinstance(cmd, str) else cmd
    log().debug("run cmd `%s`" % " ".join(cmd_list))  # noqa: UP031
    return subprocess.run(cmd_list, capture_output=True, text=True, check=check).stdout


def cmd_run_lines(cmd: str | Sequence[str], *, check: bool = True) -> Sequence[str]:
    """Run a command, return stdout lines, explode when it fails"""
    cmd_list = shlex.split(cmd) if isinstance(cmd, str) else cmd
    log().debug("run cmd `%s`" % " ".join(cmd_list))  # noqa: UP031
    stdout = subprocess.run(cmd_list, capture_output=True, text=True, check=check).stdout
    return stdout.splitlines()


console = Console()


def main(args: None | Sequence[str] = None) -> int:
    """See main docstring"""
    traceback.install()
    cli_args = parse_arguments(args or sys.argv[1:])
    setup_logging(log(), level=cli_args.log_level, show_name=20, show_funcname=30)

    with console.status("") as status:
        with suppress(KeyboardInterrupt):
            try:
                asyncio.run(update_gerrit_changes(cli_args, status=status))
            except ConnectionTimeoutError:
                Console(stderr=True).print("Got a ConnectionTimeoutError - is VPN set up correctly")
                return 1

    return 0


def log() -> logging.Logger:
    """Convenience function retrieves 'our' logger"""
    return logging.getLogger("trickkiste.update-gerrit-changes")


def rich_print(*args: object) -> None:
    """Does what you'd expect from print()"""
    console.print(*args)


if __name__ == "__main__":
    raise SystemExit(main())
