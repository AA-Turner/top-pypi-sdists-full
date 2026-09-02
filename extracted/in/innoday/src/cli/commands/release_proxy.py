"""
``innoday blastoff`` -- the deploy command.

Drives blastoff's release engine (the same one bare ``blastoff release`` uses)
with an InnoDay-supplied **brief**, and records the result.

**Named after the engine, not "release".** InnoDay has releases as *rows*,
planned weeks ahead, so ``innoday release`` read as though it created one. It
does not; it ships the one that already exists. ``release`` and ``hotfix`` stay
as aliases -- the first because people have typed it for months, the second
because it is the short form of ``--hotfix`` and worth keeping.

**A brief, not an alias.** Everything blastoff needs is resolved here and handed
over: the GitHub account and topic set from InnoDay (``/onboarding/resolve``, the
same answer ``innoday init`` uses), the version from the project's IN_PROGRESS
release row, and the previous version for the changelog window. There was a
``-c`` flag keying into a ``release_configs`` block in ``.innoday/project.yml``
holding the first two; that was one answer stored twice, matched
case-sensitively so ``pf`` never matched project ``PF``, and held up by a "there
is only one entry" fallback in the engine.

**One run.** A ``confirm`` callback is injected, so the report and the tagging
happen in the same pass. Running twice -- once to look, once with ``--release``
-- re-lists every repository and re-fetches every pull request, and somebody can
merge in between: you approve one report and ship another.

Bare ``blastoff release`` remains the standalone path for projects not managed
by InnoDay, and reads only its own ``org-versions.json``.
"""

import argparse
import contextlib
from pathlib import Path
from typing import Optional, Tuple

import httpx
from rich.console import Console

from src.cli.client import APIError, InnoDayAPIClient
from src.cli.config import CLIConfig
from src.cli.utils.formatters import (
    ProgressReporter,
    format_error,
    format_info,
    format_warning,
)
from src.cli.utils.project_context import load_project_context

console = Console()


def _role_can_release(role: str) -> bool:
    """Whether ``role`` meets the DEVELOPER minimum the release routes require.

    Ranked through the domain's own ``role_satisfies`` rather than a local
    comparison, so the CLI cannot drift from the server's answer -- the ranking
    exists precisely because an earlier equality check made a route asking for
    DEVELOPER reject an ADMIN.

    An unrecognised role passes. This preflight is a courtesy, not a security
    boundary -- the server enforces the real check -- and blocking a release on a
    role string this client has not been taught about would turn a future role
    into an outage.
    """
    from src.domain.organization import OrganizationRole, role_satisfies

    try:
        actual = OrganizationRole(role)
    except ValueError:
        return True
    return role_satisfies(actual, OrganizationRole.DEVELOPER)


class ReleaseProxyCommands:
    """`innoday release` / `innoday hotfix` -- blastoff proxied through InnoDay."""

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser, command: str) -> None:
        """Configure the parser for ``innoday blastoff``.

        One command with one option surface. ``release`` and ``hotfix`` remain
        as aliases -- ``hotfix`` is the short form people type, and it simply
        implies ``--hotfix`` -- so ``command`` only decides that default.
        """
        # **No `-c`.** It was a key into a `release_configs` block in
        # project.yml, and that block held the GitHub org and topic -- values
        # InnoDay already knows and already computes for `innoday init`. Two
        # copies of one answer, kept in step by hand, matched exactly and
        # case-sensitively so `pf` never matched project `PF`; both PF and
        # BLASTOFF ran on a "there is only one entry" fallback. The project comes
        # from the cwd like every other command, and the rest is resolved.
        parser.add_argument(
            "--hotfix",
            action="store_true",
            help="Patch the last released version instead of cutting the next "
            "planned one.",
        )
        # **A bare run reports and stops.** Asking is opt-in, because the cost of
        # the two mistakes is not symmetric: a preview nobody wanted costs a
        # scroll, and a tag nobody wanted is written to every repository in the
        # project and cannot be taken back -- a version tag is load-bearing here
        # (innoday's patch number is the *count* of them), so deleting one to
        # undo a slip silently breaks every future publish.
        #
        # Without this, `innoday blastoff` typed to see what a release contains
        # put you one keystroke from tagging, with the keystroke being the
        # answer to a question you had not asked for.
        parser.add_argument(
            "--release",
            dest="do_release",
            action="store_true",
            help="Ask to tag, having shown the report. Without it the run stops "
            "at the report and nothing is tagged.",
        )
        parser.add_argument(
            "--dry-run",
            dest="dry_run",
            action="store_true",
            help="Report and stop -- which is also what happens with no flags. "
            "Kept as the explicit way to say so.",
        )
        parser.add_argument(
            "-y",
            "--yes",
            dest="assume_yes",
            action="store_true",
            help="Skip the confirmation. For scripts -- a run that cannot ask "
            "refuses to tag without this.",
        )
        parser.add_argument(
            "--topics",
            metavar="LIST",
            help="Override the GitHub topics used to find repositories "
            "(comma-separated). Default: the project's own.",
        )
        # --repo / --commit are **hotfix-only**, and that is a rule not a
        # convenience. A release covers the project: narrowing it to one repo
        # records that the version shipped for the whole group while the others
        # never got the tag, and leaves each skipped repo's *next* window
        # starting from the older tag, so work already claimed is counted twice.
        # A hotfix claims nothing about the group, so being surgical is safe.
        parser.add_argument(
            "--repo",
            metavar="NAME",
            help="Hotfix only this repository. Requires --hotfix.",
        )
        parser.add_argument(
            "--commit",
            metavar="SHA",
            help="Hotfix this exact commit. Requires --hotfix and --repo.",
        )
        parser.add_argument(
            "--org-id",
            default=argparse.SUPPRESS,
            metavar="ORG_ID",
            help="Override organization ID (default: from .innoday/project.yml).",
        )
        parser.add_argument(
            "--project-id",
            default=argparse.SUPPRESS,
            metavar="PROJECT_ID",
            help="Override project ID (default: from .innoday/project.yml).",
        )
        parser.add_argument(
            "--token",
            "-k",
            dest="token",
            metavar="TOKEN",
            help="GitHub token (default: GH_TOKEN env var).",
        )
        parser.add_argument(
            # NOT `--org`. That is the global flag for the InnoDay organization,
            # and this is the GitHub one -- the same string meaning two different
            # things in one CLI. `-o` is kept: it is unambiguous inside this
            # subcommand and is what muscle memory types.
            "--github-org",
            "-o",
            dest="github_org",
            metavar="ORG",
            help="Override the GitHub organization (default: from release_configs).",
        )
        parser.add_argument(
            "--summary",
            metavar="TEXT",
            help="Manual release summary text (used verbatim instead of "
            "auto-generating one).",
        )
        # These shape blastoff's release report. They have to be declared
        # here as well as in blastoff: this parser owns the command line, and
        # an undeclared flag is rejected by argparse before blastoff is ever
        # reached ("unrecognized arguments: --commits"), so a flag that exists
        # in the engine is unreachable through the proxy until it is repeated.
        #
        # **Repeating them is the whole mechanism, and forgetting to is a
        # silent regression rather than an error.** blastoff 0.5.0 made
        # in-process summary generation opt-in behind `--generate-summary`,
        # on the rule that the engine assembles and the caller narrates. This
        # proxy forwarded neither that flag nor `--json`, so the moment the
        # engine was upgraded `innoday release` produced **no summary at
        # all** -- worse than the flaky one it replaced, and visible only by
        # reading the output (#663).
        # **`--prs` and `--pr-list` are gone, not deprecated.** The engine
        # dropped them in 0.7.0: they read as the same flag and acted on
        # opposite sets -- the open pull requests being left out, and the merged
        # ones going in -- and in a dry run the first did nothing at all,
        # because that section was already on. Both are now always shown, and
        # the merged list is no longer truncated, so there is nothing here to
        # ask for. Forwarding a flag the engine no longer defines is an
        # unknown-argument error one layer down, which is the failure this
        # command's own test exists to catch.
        parser.add_argument(
            "--commits",
            action="store_true",
            help="List every commit in the release, not just a per-repo count.",
        )
        parser.add_argument(
            "--json",
            dest="as_json",
            action="store_true",
            help="Emit the assembled release data as JSON instead of the "
            "report -- for a caller that will write the summary itself.",
        )
        parser.add_argument(
            "--generate-summary",
            dest="generate_summary",
            action="store_true",
            help="Ask Claude for the summary from inside this command. Off "
            "by default: it is a billed, non-deterministic step on a command "
            "whose job is to say what it is about to do, and it deadlocks "
            "when run from inside a Claude Code session.",
        )

    # ------------------------------------------------------------------ #
    # Entry points
    # ------------------------------------------------------------------ #

    @staticmethod
    async def execute_release(args: argparse.Namespace, config: CLIConfig) -> int:
        return await ReleaseProxyCommands._run(args, config, mode="release")

    @staticmethod
    async def execute_hotfix(args: argparse.Namespace, config: CLIConfig) -> int:
        return await ReleaseProxyCommands._run(args, config, mode="hotfix")

    # ------------------------------------------------------------------ #
    # Core
    # ------------------------------------------------------------------ #

    @staticmethod
    async def _run(args: argparse.Namespace, config: CLIConfig, mode: str) -> int:
        """Resolve context, build the store, and drive blastoff in-process.

        Async only so the teardown below can *await* the client's close. The body
        is deliberately synchronous work -- blastoff is a plumbum application run
        in-process -- and blocking the loop for its duration is what already
        happened when this was a sync method called from an async one.
        """
        # `innoday hotfix` is an alias, so it arrives as mode="hotfix"; the flag
        # says the same thing on the unified command. Either is enough.
        hotfix = mode == "hotfix" or getattr(args, "hotfix", False)

        scope_error = ReleaseProxyCommands._check_scope(args, hotfix)
        if scope_error:
            console.print(format_error(scope_error))
            return 1

        # **The rocket comes first, before anything that can wait.**
        #
        # It used to start once the release was being assembled, and three
        # network round trips ran ahead of it in silence: resolving the project
        # from InnoDay, checking permission to record a release, and loading the
        # version store. Several seconds of nothing, which reads as a command
        # that did not launch -- the exact impression the rocket exists to
        # prevent, just moved earlier than the first attempt at fixing it.
        #
        # Nothing at all under `--json`: that output is one document for a
        # machine, and a spinner drawn over it is the same corruption a stray
        # line of prose caused in the engine's own report.
        as_json = getattr(args, "as_json", False)
        reporter = None if as_json else ProgressReporter("🚀 Finding your project")
        with reporter or contextlib.nullcontext():
            return await ReleaseProxyCommands._run_with_progress(
                args, config, hotfix, reporter
            )

    @staticmethod
    async def _run_with_progress(
        args: argparse.Namespace,
        config: CLIConfig,
        hotfix: bool,
        reporter: "ProgressReporter | None",
    ) -> int:
        """The body of `_run`, with the spinner already on screen."""
        resolved = await ReleaseProxyCommands._resolve_context(args, config)
        if resolved is None:
            return 1
        org_id, project_id, github_org, topics, alias, prerelease = resolved

        if reporter is not None:
            reporter.update(f"🚀 Checking you can release {alias}")

        # Check who you are and what you may do BEFORE anything is tagged.
        #
        # Both failures used to surface at the very end, after every repo had
        # already been tagged on GitHub: a release that shipped but was never
        # recorded, which is the worst of the three possible outcomes and the
        # hardest to notice. The permission to record a release is knowable up
        # front, so it is checked up front.
        preflight = await ReleaseProxyCommands._preflight(config, org_id, alias)
        if preflight != 0:
            return preflight

        api_client = InnoDayAPIClient(config)
        store = _build_store(
            api_client=api_client,
            org_id=org_id,
            project_id=project_id,
            github_org=github_org,
            topics=topics,
            prerelease=prerelease,
        )

        try:
            if hotfix:
                return ReleaseProxyCommands._drive_hotfix(
                    args, store, alias, github_org, topics
                )
            return await ReleaseProxyCommands._drive_release(
                args,
                store,
                alias,
                github_org,
                topics,
                config,
                org_id,
                project_id,
                reporter=reporter,
            )
        finally:
            # InnoDayAPIClient owns an httpx.AsyncClient; close it so we don't
            # leak the connection when the proxy exits.
            #
            # **On the store's loop, not this one.** Every request this client
            # made went through `_StoreLoop` (the version store's single
            # long-lived loop); closing it from the CLI's own loop would tear
            # down connections that belong to a different one, which raises the
            # very "Event loop is closed" this is meant to avoid.
            #
            # Two earlier versions of these three lines were wrong in different
            # ways: `ensure_future(...)` scheduled a task the closing loop never
            # ran, and a bare `await` closed it from the wrong loop.
            from src.integrations.innoday_version_store import (
                close_on_store_loop,
            )

            close_on_store_loop(api_client.close())

    @staticmethod
    async def _fetch_content(
        config: CLIConfig, org_id, project_id, *, since, window_label, version=None
    ):
        """What the release contains, assembled server-side, or None.

        **None means "carry on without it", never "nothing shipped".** The
        engine still knows how to find a release itself; that path just needs a
        credential. So an organisation with no GitHub connection, or a server
        too old to answer, falls back to the old behaviour with a reason
        printed -- rather than rendering an empty release, which is the one
        outcome that would look like a successful run and be wrong.
        """
        try:
            async with InnoDayAPIClient(config) as client:
                response = await client.get(
                    f"/api/v1/organizations/{org_id}/projects/{project_id}"
                    f"/release/content",
                    params={
                        k: v
                        for k, v in (
                            ("since", since),
                            ("window_label", window_label),
                            ("version", version),
                        )
                        if v
                    },
                )
        except (APIError, httpx.HTTPError) as exc:
            console.print(format_warning(f"Could not assemble the release here: {exc}"))
            return None

        if response.status_code == 200:
            return response.json()

        if response.status_code == 409:
            # The organisation genuinely has no GitHub connection. Say so, and
            # say what it costs -- otherwise the token prompt that follows looks
            # like the tool being awkward rather than the setup being incomplete.
            try:
                detail = response.json().get("detail", "")
            except ValueError:
                detail = ""
            console.print(format_warning(detail or "No GitHub credential stored."))
            console.print(
                format_info(
                    "Falling back to reading GitHub from here, which needs a "
                    "token. Connect the organisation to avoid that."
                )
            )
            return None

        console.print(
            format_warning(
                f"Could not assemble the release here (HTTP "
                f"{response.status_code}); reading GitHub from here instead."
            )
        )
        return None

    @staticmethod
    async def _preflight(config: CLIConfig, org_id: str, alias: str) -> int:
        """Refuse to start a release the caller cannot finish.

        Three distinct failures, which used to be one unreadable line at the end
        of a run that had already tagged every repository:

            ⚠️  Recording release failed (non-blocking): Failed to record
            release: HTTP 403 -- {"detail":"Requires DEVELOPER role or higher"}

        * **No InnoDay account.** Nothing to authenticate with, so nothing later
          in the run can succeed. Say so immediately and point at sign-up.
        * **Not a member of this organization.** The token is real, the org is
          not theirs.
        * **Member, but below DEVELOPER.** The most common one, and the most
          confusing, because everything *up to* recording works: the repos get
          tagged and only the bookkeeping 403s.

        Returns 0 to proceed, 1 to stop. Deliberately fails **open** when the
        check itself cannot run (network down, /auth/me unreachable): refusing to
        release because a preflight could not reach the API would be a worse
        failure than the one it prevents, and the recording step still reports
        honestly if it turns out the caller really was unauthorised.
        """
        from src.cli.commands.session import _base_url, _fetch_me

        token = config.get_cli_token()
        if not token:
            console.print(
                format_error(
                    "You are not signed in to InnoDay, so this release "
                    "cannot be recorded."
                )
            )
            console.print(
                format_info(
                    "Sign up or sign in at https://www.inno.day, then run "
                    "`innoday login`."
                )
            )
            return 1

        try:
            me = await _fetch_me(
                _base_url(config, None), token, config.get_team_secret()
            )
        except Exception:  # noqa: BLE001 -- see the fail-open note above
            return 0

        if me is None:
            console.print(
                format_error(
                    "Your InnoDay session is not valid, so this release "
                    "cannot be recorded."
                )
            )
            console.print(
                format_info(
                    "Run `innoday login`. If you do not have an account yet, "
                    "sign up at https://www.inno.day."
                )
            )
            return 1

        # A platform member reaches every organization, so the membership and
        # role checks below do not apply to them.
        if me.get("is_platform_member"):
            return 0

        orgs = me.get("organizations") or []
        mine = next((o for o in orgs if o.get("id") == org_id), None)
        if mine is None:
            console.print(
                format_error(
                    f"You are not a member of the organization that owns "
                    f"'{alias}', so this release cannot be recorded."
                )
            )
            console.print(
                format_info("Ask an administrator to add you, then try again.")
            )
            return 1

        role = str(mine.get("role") or "")
        if not _role_can_release(role):
            org_label = mine.get("alias") or mine.get("name") or org_id
            console.print(
                format_error(
                    f"Your role in {org_label} is {role or 'unknown'}, and "
                    f"cutting a release needs DEVELOPER or higher."
                )
            )
            console.print(
                format_info(
                    "Ask an administrator to run: "
                    "innoday orgs members --set-role <your-email> --role DEVELOPER"
                )
            )
            console.print(
                format_info(
                    "Nothing has been tagged — this stopped before touching any "
                    "repository."
                )
            )
            return 1

        return 0

    @staticmethod
    async def _drive_release(
        args,
        store,
        alias,
        github_org,
        topics,
        config,
        org_id,
        project_id,
        reporter=None,
    ) -> int:
        """Drive blastoff with a brief, and ask before anything is tagged.

        **A brief, not an alias.** InnoDay has already resolved the GitHub
        account, the topics, the version being cut and where the last one ended,
        so it hands those over rather than leaving blastoff to rediscover them.
        The engine looks nothing up.

        **One run, not two.** A `confirm` callback is injected, so the report and
        the tagging happen in the same pass. Running twice -- once to look, once
        with `--release` -- re-lists every repo and re-fetches every PR, and
        somebody can merge in between, which means approving one report and
        shipping another.
        """
        import json as _json

        from blastoff.release import Release

        if reporter is not None:
            reporter.update("🚀 Working out which version is next")
        try:
            org_config = store.load_org_config(alias)
        except FileNotFoundError as e:
            console.print(format_error(str(e)))
            return 1

        as_json = getattr(args, "as_json", False)

        # **The wait moved, and the progress indicator has to follow it.** It
        # used to be the engine reading GitHub, which animates its own rocket
        # through what it is doing. The platform does that reading now, so the
        # engine finishes instantly and the wait is here -- seventeen seconds on
        # a seven-repository release, every one of them silent, which is the
        # hang the rocket was added for, relocated.
        #
        # Three stages, each one something this command actually does in
        # sequence. Splitting the middle one further would read better and be
        # fiction: it is a single call, and only the server knows what it is
        # doing inside it.
        #
        # Nothing at all under `--json`: that output is one document for a
        # machine, and a spinner drawn over it is the same corruption a stray
        # line of prose caused in the engine's own report.
        if reporter is not None:
            reporter.update("🚀 Working out what ships")
        with contextlib.nullcontext():
            picture = ReleaseProxyCommands._ticket_picture(
                store, org_config.next_version
            )

            brief = {
                "name": alias,
                "github_org": github_org,
                "topics": topics,
                "version": org_config.next_version,
                "previous_version": org_config.last_released_version,
                "previous_released_at": org_config.last_released,
            }
            if picture is not None:
                brief["ticket_count"], brief["open_ticket_count"] = picture

            # **Assembled here, with the organisation's own credential.** Without
            # this the engine goes and finds the release itself, wherever it happens
            # to be running, and so demands a GitHub token from whoever ran the
            # command -- and the nearest one to hand is a personal login. That is
            # the wrong credential for a release, and needing it at all hid the fact
            # that the right one was already stored server-side.
            since_label = (
                f"since {org_config.last_released_version}"
                if org_config.last_released_version
                else "since the last release"
            )
            if reporter is not None:
                reporter.update(f"🚀 Reading what shipped {since_label}")

            content = await ReleaseProxyCommands._fetch_content(
                config,
                org_id,
                project_id,
                since=org_config.last_released,
                window_label=(
                    f"since {org_config.last_released_version}"
                    if org_config.last_released_version
                    else None
                ),
                version=org_config.next_version,
            )
            if content is not None:
                brief["content"] = content

            if reporter is not None:
                reporter.update("🚀 Writing the report")

        # **Put the spinner away before anything is printed.** The report goes
        # to stdout and the confirmation prompt waits on a person; an animation
        # running over either is the thing the rocket was supposed to fix.
        if reporter is not None:
            reporter.stop()

        argv = ["--brief", "-"]
        if getattr(args, "token", None):
            argv += ["-k", args.token]
        if getattr(args, "summary", None):
            argv += ["--summary", args.summary]
        if getattr(args, "commits", False):
            argv.append("--commits")
        if getattr(args, "generate_summary", False):
            argv.append("--generate-summary")
        if as_json:
            argv.append("--json")

        confirm = ReleaseProxyCommands._confirmer(args)
        if confirm is None:
            # `--dry-run`, or `--json`: report and stop. Nothing to approve.
            pass
        elif confirm is True:
            # `--yes`: skip the asking, not the reporting.
            argv.append("--release")
            confirm = None

        result = ReleaseProxyCommands._invoke_blastoff(
            Release,
            argv,
            store,
            stdin=_json.dumps(brief),
            confirm=confirm,
        )
        # **Say what to type next.** A report that stops without saying how to
        # proceed reads as a failure, and the obvious guess -- run it again --
        # is how somebody ends up hunting for a flag while assuming the command
        # is broken.
        if ReleaseProxyCommands._stopped_at_the_report(args):
            console.print(
                format_info(
                    "Report only — nothing was tagged. Add --release to be "
                    "asked, or --release --yes to tag without being asked."
                )
            )
        return result

    @staticmethod
    def _stopped_at_the_report(args) -> bool:
        """True when the run ended at the report for want of `--release`.

        Not the same as `--dry-run`, which asked for exactly this and does not
        need telling. The hint is for somebody who typed `innoday blastoff`
        expecting to cut a release and got a report instead.
        """
        return not any(
            getattr(args, name, False)
            for name in ("do_release", "assume_yes", "dry_run", "as_json")
        )

    @staticmethod
    def _check_scope(args, hotfix: bool) -> Optional[str]:
        """Refuse a narrowed *release*, and a ``--commit`` with no ``--repo``.

        **A release covers the project.** Narrowing it to one repository records
        that the version shipped for the whole group while the others never got
        the tag -- and, more quietly, leaves each skipped repo's *next* window
        starting from the older tag, so work already claimed by this version is
        counted again into the next one. The version boundary silently diverges
        per repository.

        A hotfix claims nothing about the group. It is a patch on top of a
        version that already shipped, so being surgical is the point, and both
        switches belong to it. With neither, a hotfix covers the whole project
        exactly as a release does.
        """
        if not hotfix:
            for flag in ("repo", "commit"):
                if getattr(args, flag, None):
                    return (
                        f"--{flag} is only for a hotfix.\n"
                        "  A release covers the whole project: tagging one "
                        "repository would record that the version shipped for "
                        "all of them, and leave every other repository's next "
                        "release counting the same work twice.\n"
                        f"  Did you mean `--hotfix --{flag} ...`?"
                    )
        if getattr(args, "commit", None) and not getattr(args, "repo", None):
            return (
                "--commit needs --repo.\n"
                "  A commit belongs to one repository, and a hotfix may span "
                "several. Name the one you mean."
            )
        return None

    @staticmethod
    def _confirmer(args):
        """How this run decides to go ahead: a callable, ``True``, or ``None``.

        * ``None`` -- do not tag. ``--dry-run`` says so outright, and ``--json``
          implies it: a caller parsing one document is not going to answer a
          prompt, and a prompt would land in the middle of its stdout.
        * ``True`` -- go without asking (``--yes``).
        * a callable -- ask.

        **A run that cannot ask refuses to tag.** With no terminal and no
        ``--yes`` -- cron, CI, a pipe -- ``input()`` raises, and treating that as
        approval would tag every repository because nobody was there to say no.
        """
        if getattr(args, "dry_run", False) or getattr(args, "as_json", False):
            return None
        # `--yes` is "do not ask me", which only means anything about a release
        # somebody is asking for -- so it carries the intent `--release` states.
        # Requiring both would break every script that already passes `--yes`
        # and would buy nothing: there is no reading of `--yes` that wants a
        # report.
        if getattr(args, "assume_yes", False):
            return True
        if not getattr(args, "do_release", False):
            return None

        import sys

        if not sys.stdin.isatty():
            console.print(
                format_info(
                    "Not a terminal, so nothing was tagged. Re-run with --yes to "
                    "release without being asked, or --dry-run to silence this."
                )
            )
            return None

        # **Hold on to the real terminal now.** The brief is handed to blastoff
        # on stdin, so by the time this is called `sys.stdin` is a spent buffer
        # containing that JSON -- `input()` would read the brief back as the
        # answer, or hit EOF. Captured here, before the swap, and read from
        # directly.
        terminal = sys.stdin

        def ask(version, repos):
            count = len(repos)
            noun = "repository" if count == 1 else "repositories"
            print(
                f"\nTag {count} {noun} with {version} and record the release? [y/N] ",
                end="",
                flush=True,
            )
            return terminal.readline().strip().lower() in ("y", "yes")

        return ask

    @staticmethod
    def _ticket_picture(store, version: str):
        """``(planned, unfinished)`` for the version, or ``None`` if unknowable.

        **The half of the report blastoff structurally cannot provide.** The
        engine decides what is in a release from GitHub merge dates and has no
        idea tickets exist, so it can say which pull requests are in and nothing
        about the work planned in.

        Returned rather than printed: it belongs on the report's own header line
        alongside the repo and PR counts, not as a separate sentence above it.
        Two lines saying overlapping things is what the single-header change
        exists to remove.

        Never raises. A release must not fail because a count would not load.
        """
        counts = getattr(store, "ticket_picture", None)
        if counts is None:
            return None
        try:
            return counts(version)
        except Exception:  # noqa: BLE001 -- informational only, never blocks
            return None

    @staticmethod
    def _drive_hotfix(args, store, alias, github_org, topics) -> int:
        """Patch the last released version, optionally narrowed to one commit.

        The base version comes from InnoDay's release records through the
        injected store, not a file. ``--repo`` and ``--commit`` narrow it; with
        neither, a hotfix covers the whole project exactly as a release does.

        ``--commit`` pins the tag to an exact SHA, which is the normal case: the
        fix is a cherry-pick and the branch has moved on since. blastoff creates
        the git tag at that SHA before creating the release, because creating the
        release alone lets GitHub resolve to the branch head instead.
        """
        from blastoff.hotfix import Hotfix

        argv = ["-c", alias, "-o", github_org, "--topics", ",".join(topics)]
        if getattr(args, "token", None):
            argv += ["-k", args.token]
        if getattr(args, "repo", None):
            argv += ["--repo", args.repo]
        if getattr(args, "commit", None):
            argv += ["--commit", args.commit]

        confirm = ReleaseProxyCommands._confirmer(args)
        if confirm is True:
            argv.append("--release")
            confirm = None

        return ReleaseProxyCommands._invoke_blastoff(
            Hotfix, argv, store, confirm=confirm
        )

    @staticmethod
    def _invoke_blastoff(app_cls, argv, store, stdin=None, confirm=None) -> int:
        """Run a blastoff plumbum Application in-process with the store injected.

        Sets the class-level ``version_store`` (blastoff reads it in ``main()``
        and only falls back to ``FileVersionStore`` when it is None), runs via
        ``run(argv, exit=False)`` so it never calls ``sys.exit``, and restores
        the attribute afterwards so the injection doesn't leak into any later
        invocation in the same process.

        **argv must start with a program name.** plumbum's ``Application.run``
        does ``inst = cls(argv.pop(0))`` -- it takes the same shape as
        ``sys.argv``, where the executable occupies slot zero. Passing the
        switches alone made plumbum consume ``-c`` as the program name and then
        reject the alias behind it as an unexpected positional:

            Error: Expected at most 0 positional arguments, got ['pf']
            Usage: -c [SWITCHES]

        The banner naming the program ``-c`` is the tell. Both `innoday release`
        and `innoday hotfix` failed this way, *after* printing the version they
        had resolved -- so the command looked like it had got as far as talking
        to GitHub when it had not yet parsed its own arguments.
        """
        import io
        import sys

        previous = getattr(app_cls, "version_store", None)
        previous_confirm = getattr(app_cls, "confirm", None)
        app_cls.version_store = store
        # staticmethod: plumbum reads this off the class, and a bare function
        # assigned to a class attribute would arrive with `self` bound to it.
        app_cls.confirm = staticmethod(confirm) if confirm else None
        try:
            # The brief goes in on stdin rather than a temporary file. Leaving a
            # file for blastoff to find is the habit this whole change breaks.
            # (There is no `contextlib.redirect_stdin`; only stdout and stderr
            # have one.)
            real_stdin = sys.stdin
            if stdin is not None:
                sys.stdin = io.StringIO(stdin)
            try:
                _instance, retcode = app_cls.run(["blastoff", *argv], exit=False)
            finally:
                sys.stdin = real_stdin
            return retcode or 0
        except Exception as e:  # noqa: BLE001 -- surface blastoff errors cleanly
            console.print(format_error(f"blastoff failed: {e}"))
            return 1
        finally:
            app_cls.version_store = previous
            app_cls.confirm = previous_confirm

    # ------------------------------------------------------------------ #
    # Context resolution
    # ------------------------------------------------------------------ #

    @staticmethod
    async def _resolve_context(
        args: argparse.Namespace, config: CLIConfig
    ) -> Optional[Tuple[str, str, str, list, str, Optional[str]]]:
        """Resolve (org_id, project_id, github_org, topics, alias, prerelease).

        org_id/project_id come from --org-id/--project-id or the cwd, as always.
        **github_org and topics come from InnoDay**, not from a file: it already
        computes both for `innoday init`, and a hand-maintained copy in
        project.yml was one answer stored twice with nothing keeping the two in
        step. Returns None (after printing an error) if a piece is missing.
        """
        org_id = getattr(args, "org_id", None) or _resolve_org_id(config)
        if not org_id:
            console.print(
                format_error(
                    "No organization resolved. Run from a directory with "
                    ".innoday/project.yml, or pass --org-id."
                )
            )
            return None

        project_id = (
            getattr(args, "project_id", None) or config.get_current_project_id()
        )
        if not project_id:
            console.print(
                format_error(
                    "No project resolved. Run from a directory with "
                    ".innoday/project.yml, or pass --project-id."
                )
            )
            return None

        # Aliases, from the same context every other command reads -- **including
        # `--dir`**. The shape is flat (`org_alias`/`project_alias`), not the
        # nested `org:`/`project:` blocks the YAML has; `load_project_context`
        # flattens it.
        #
        # **Reading the cwd here while org_id/project_id came from `config` split
        # one release across two projects.** `config` honours `--dir`; this call
        # did not, so `innoday --dir <bpai> release` reported
        # "PF v1.11.0 - topics pf,pixelfuel - 9 repos - 11 tickets, 7 open":
        # PF's topics and PF's repos, carrying BPAI's version and BPAI's ticket
        # picture. Every half came from a different project. A real run would have
        # tagged nine PF repos as v1.11.0; what stopped it was only the
        # non-terminal guard refusing to tag without --yes.
        #
        # Same shape as the `latest_release()` divergence: two code paths
        # answering "which project", and nothing reconciling them. One argument
        # closes it, because `load_project_context` already took a start dir.
        context_dir = getattr(args, "dir", None)
        context = load_project_context(Path(context_dir) if context_dir else None) or {}
        org_alias = context.get("org_alias") or config.get_current_organization()
        project_alias = context.get("project_alias")
        resolved = await _resolve_release_target(config, org_alias, project_alias)
        if resolved is None:
            return None
        alias, github_org, topics = resolved

        # Explicit overrides win — the escape hatch for a one-off, not the
        # normal path. The normal path is that InnoDay already knows.
        if getattr(args, "github_org", None):
            github_org = args.github_org
        if getattr(args, "topics", None):
            topics = [t.strip() for t in args.topics.split(",") if t.strip()]

        if not topics:
            console.print(
                format_error(
                    f"Project '{alias}' has no GitHub topics, so no repositories "
                    "can be found.\n"
                    "  A project's lowercased alias is always one of its topics; "
                    "add extras in the organization's settings, or pass --topics."
                )
            )
            return None

        return org_id, project_id, github_org, topics, alias, None


# ---------------------------------------------------------------------------
# Module-level helpers (kept out of the class so they're easy to patch/reuse)
# ---------------------------------------------------------------------------


def _build_store(api_client, org_id, project_id, github_org, topics, prerelease):
    """Construct an InnoDayVersionStore (import kept local to ease patching)."""
    from src.integrations.innoday_version_store import InnoDayVersionStore

    return InnoDayVersionStore(
        api_client=api_client,
        org_id=org_id,
        project_id=project_id,
        github_org=github_org,
        topics=topics,
        prerelease=prerelease,
    )


def _resolve_org_id(config: CLIConfig) -> Optional[str]:
    """Resolve the org UUID from the CLI config (cwd .innoday/project.yml)."""
    org_slug = config.get_current_organization()
    if not org_slug:
        return None
    return config.get_organization_id(org_slug)


async def _resolve_release_target(
    config: CLIConfig, org_ref: str, project_ref: Optional[str]
) -> Optional[Tuple[str, str, list]]:
    """Ask InnoDay for (project alias, GitHub org, topics).

    **This replaced `_load_release_config`**, which read the same three values
    out of a `release_configs` block in `.innoday/project.yml`. InnoDay already
    holds them and already computes the topic set for `innoday init` --
    `WorkspaceOnboardService.github_topics()`, which is the project's lowercased
    alias plus any extras configured for it. Keeping a second copy in a file
    nothing writes gave us a key that had to match on both sides, matched
    case-sensitively so `pf` never matched project `PF`, and a "there is only one
    entry" fallback quietly holding the whole thing up.

    Reuses `/onboarding/resolve` rather than adding an endpoint: it returns
    exactly these fields and is already the answer `innoday init` trusts.

    **Takes aliases, not UUIDs.** That endpoint's resolvers match on alias only
    (`WorkspaceOnboardService.resolve_org` / `resolve_project`), unlike every
    other resolver in the codebase, which accepts either. Passing a UUID gets
    "Organization '<uuid>' not found in InnoDay" -- found by running it, not by
    reading it. `innoday init` calls the same endpoint with aliases; this matches.
    """
    async with InnoDayAPIClient(config) as client:
        response = await client.get(
            "/api/v1/onboarding/resolve",
            params=(
                {"org": org_ref, "project": project_ref}
                if project_ref
                else {"org": org_ref}
            ),
        )
    if response.status_code != 200:
        try:
            detail = response.json().get("detail", response.text)
        except Exception:  # noqa: BLE001 -- a non-JSON body is still worth showing
            detail = response.text
        console.print(
            format_error(f"Could not resolve this project from InnoDay: {detail}")
        )
        return None

    body = response.json() or {}
    org_block = body.get("org") or {}
    project_block = body.get("project") or {}
    github_org = org_block.get("github_org")
    if not github_org:
        console.print(
            format_error(
                "This organization has no GitHub account configured, so there is "
                "nowhere to look for repositories.\n"
                "  Set `github_org` in the organization's settings."
            )
        )
        return None

    # Comma-separated on the wire because a project may span several topics.
    topics = [
        t.strip() for t in (body.get("github_topic") or "").split(",") if t.strip()
    ]
    alias = project_block.get("alias") or org_block.get("alias") or "release"
    return alias, github_org, topics
