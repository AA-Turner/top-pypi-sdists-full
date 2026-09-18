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


# --------------------------------------------------------------------------- #
# Borrowing the `gh` CLI's credential -- an explicitly-labelled stopgap
# --------------------------------------------------------------------------- #
#
# **The organisation's credential is supposed to live on the platform.** InnoDay
# holds each organisation's GitHub credential and uses it server-side, which is
# why a release *report* needs no token from anybody: the content arrives
# already assembled (see `_fetch_content`). Tagging is different -- it writes,
# and it writes from this machine -- and there is as yet no way for the platform
# to lend the organisation's credential to a client for that write.
# `havilandsoftware/innoday#753` is where that capability is tracked.
#
# Until it exists the only credential within reach is the person's own, and the
# run dead-ended telling them to set an environment variable. So we offer
# theirs -- never silently, and never without naming whose account ends up on
# the tag. Every tag and GitHub Release created this way is attributed to that
# personal account rather than to the organisation, which is precisely the thing
# a server-side credential fixes. This whole path is a stopgap: when #753 lands,
# delete it rather than tidying it.
def _run_gh(*argv: str) -> Optional[Tuple[str, str]]:
    """``(stdout, stderr)`` from ``gh``, or ``None`` if it is absent or failed.

    Both streams come back because `gh auth status` has written its answer to
    stderr in some versions of `gh` and to stdout in others, and the caller
    wants the account name out of whichever one carried it. They are handed back
    separately rather than concatenated because `gh auth token` prints a
    credential on stdout, and folding a stray line of stderr into it would hand
    the engine a token that silently is not one.

    Never raises -- an absent binary, a timeout and a non-zero exit are all the
    same answer here, "no token" -- and never logs what it captured.
    """
    import shutil
    import subprocess

    exe = shutil.which("gh")
    if exe is None:
        return None
    try:
        done = subprocess.run([exe, *argv], capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.SubprocessError):
        return None
    if done.returncode != 0:
        return None
    return done.stdout, done.stderr


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
        # **The same thing said the other way round.** `--commit` pins the tag
        # to a SHA; `--branch` pins it to whatever that branch points at now.
        # Both exist because a hotfix is usually a cherry-pick onto a release
        # line, and which of the two you have to hand depends on whether you
        # made the branch or were sent the commit. The engine treats them as one
        # answer and refuses both together, so this does too -- before the
        # report, where stopping costs nothing.
        parser.add_argument(
            "--branch",
            metavar="NAME",
            help="Hotfix this branch's head. Requires --hotfix and --repo.",
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
            # **One driver, and the flag is the only difference.** There were
            # two, and the hotfix one was thirty lines against a hundred and
            # fifty -- not because a hotfix needs less, but because everything
            # added to a release since they were split was added to one of them.
            # It was never handed `config`, `org_id` or `project_id`, so it
            # could not ask InnoDay what the release contained; never handed the
            # reporter, so the spinner ran over the engine's own output and over
            # the `[y/N]` prompt.
            return await ReleaseProxyCommands._drive_release(
                args,
                store,
                alias,
                github_org,
                topics,
                config,
                org_id,
                project_id,
                hotfix=hotfix,
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
        *,
        hotfix: bool = False,
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

        **A hotfix is this same run with the patch digit moving.** It used to be
        a driver of its own, and being separate is the whole reason it fell
        behind: every one of the four things above was added to a release and
        never carried across. A hotfix got no brief, so its preview demanded a
        personal GitHub token for content the platform could already fetch with
        the organisation's own credential; no ticket picture; no reporter, so
        the spinner animated over the engine's report and over the `[y/N]`
        prompt; and no hint afterwards saying how to actually tag. `hotfix` now
        decides the version and adds one flag, and nothing else differs.
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

        version = ReleaseProxyCommands._version_to_cut(org_config, hotfix)
        if version is None:
            # Only reachable for a hotfix: a project with nothing released has
            # no line to patch, and inventing v0.0.1 would claim it had one. A
            # release is never in this position -- the store bootstraps it.
            console.print(
                format_error(
                    f"{alias} has no released version, so there is nothing to "
                    "patch. Cut a release first."
                )
            )
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
            picture = ReleaseProxyCommands._ticket_picture(store, version)

            brief = {
                "name": alias,
                "github_org": github_org,
                "topics": topics,
                "version": version,
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
            #
            # **Except for a hotfix that has been narrowed.** The platform
            # assembles a window with a start and no end, covering every
            # repository the project has. `--commit` and `--branch` put an end on
            # it and `--repo` takes the other repositories out, and neither is
            # something this payload can be asked for -- so handing it over would
            # render a report listing work the tag does not contain. A narrowed
            # hotfix therefore reads GitHub from here, as it always has, and is
            # offered a credential below. Giving it the same token-free preview
            # means teaching `/release/content` to take a repository and an end
            # to the window; until then, saying so beats a confident wrong page.
            narrowed = any(
                getattr(args, name, None) for name in ("repo", "commit", "branch")
            )
            content = None
            if not narrowed:
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
                    version=version,
                )
                if content is not None:
                    brief["content"] = content

            if reporter is not None:
                reporter.update("🚀 Writing the report")

        # **Put the spinner away before anything is printed.** The report goes
        # to stdout and the confirmation prompt waits on a person; an animation
        # running over either is the thing the rocket was supposed to fix. The
        # hotfix driver was never handed the reporter at all, so on that path
        # the spinner kept drawing over the engine's own report and over the
        # question asking whether to tag.
        if reporter is not None:
            reporter.stop()

        argv = ["--brief", "-"]
        if hotfix:
            argv.append("--hotfix")
        # Where the hotfix stops: one repository, and optionally one commit or
        # one branch head inside it. Refused for a release by `_check_scope`
        # long before here, and refused again by the engine.
        for flag in ("repo", "commit", "branch"):
            value = getattr(args, flag, None)
            if value:
                argv += [f"--{flag}", value]
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

        # **A run that can tag needs its credential before it starts, not when
        # it reaches the write.** The report needs none -- the content arrives
        # assembled, fetched server-side with the organisation's own credential
        # -- so this fires for a run on its way to tagging: `--yes`, which put
        # `--release` in argv just above, or a confirm callback, which is a run
        # about to ask.
        #
        # **And for a narrowed hotfix, which has no assembled content to render
        # from.** That run has to read GitHub to print a single line, so the
        # engine refuses outright without a credential -- which is what the old
        # hotfix driver made this offer unconditionally for, back when no hotfix
        # ever had content. A *release* whose content fetch fell back is in the
        # same position and still dead-ends on the engine's own message. Widening
        # the offer to cover that is a change to the release path, and belongs on
        # its own rather than smuggled in with a merge of two drivers.
        #
        # **Without this the failure is invisible rather than loud.** With
        # content supplied and no token, the engine's own check does not fire at
        # all: it prints the report, asks, is told yes, finds no GitHub client
        # to tag with, and so prints every repository as "would_create" -- and
        # then records the release anyway. Nothing is tagged and InnoDay says it
        # shipped.
        will_tag = confirm is not None or "--release" in argv
        needs_credential = will_tag or (hotfix and content is None)
        if needs_credential and not ReleaseProxyCommands._has_github_token(args):
            borrowed = ReleaseProxyCommands._borrow_personal_token(args)
            if borrowed is None:
                return 1
            argv += ["-k", borrowed]

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
    def _version_to_cut(org_config, hotfix: bool) -> Optional[str]:
        """The version this run will tag, or ``None`` when there is not one.

        A release cuts the version the project is heading toward -- slot one of
        its pipeline, the same one the Releases tab calls the next launch. A
        hotfix moves the patch digit on the line that last shipped instead,
        which is a different question with a different answer: a project that
        released v1.9.0 and has v1.10.0 planned patches to v1.9.1, not v1.10.1.

        **Computed here rather than left to the engine.** The engine knows how,
        but only on the path where it loads the config itself; a supplied brief
        names the version outright, and a brief is what this command sends. The
        alternative -- passing the tag as `-t` -- reads as an override and turns
        the post-release bookkeeping off, so the release would ship and never be
        recorded.

        ``None`` only for a hotfix on a project that has never released:
        there is no line to patch, and a v0.0.1 invented here would claim there
        was one.
        """
        if not hotfix:
            return org_config.next_version

        from blastoff.version_manager import SemanticVersion

        last = getattr(org_config, "last_released_version", None)
        if not last:
            return None
        try:
            return SemanticVersion.from_string(last).bump_patch().to_string()
        except Exception:  # noqa: BLE001 -- an unparseable tag is "cannot patch"
            return None

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
            for flag in ("repo", "commit", "branch"):
                if getattr(args, flag, None):
                    return (
                        f"--{flag} is only for a hotfix.\n"
                        "  A release covers the whole project: tagging one "
                        "repository would record that the version shipped for "
                        "all of them, and leave every other repository's next "
                        "release counting the same work twice.\n"
                        f"  Did you mean `--hotfix --{flag} ...`?"
                    )
        for flag in ("commit", "branch"):
            if getattr(args, flag, None) and not getattr(args, "repo", None):
                return (
                    f"--{flag} needs --repo.\n"
                    "  A commit belongs to one repository, and a hotfix may "
                    "span several. Name the one you mean."
                )
        if getattr(args, "commit", None) and getattr(args, "branch", None):
            return (
                "--commit and --branch are two ways to say the same thing.\n"
                "  Both name where the window ends. Pass one."
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
    def _has_github_token(args) -> bool:
        """Whether this run already holds a credential, without asking anybody.

        The two the engine itself reads, and they keep precedence exactly as
        they had it: an explicit ``--token``, then ``GH_TOKEN``. The offer below
        exists only for the run that has neither.
        """
        import os

        return bool(getattr(args, "token", None) or os.environ.get("GH_TOKEN"))

    @staticmethod
    def _gh_account() -> Optional[str]:
        """The account ``gh`` is signed in as, or ``None``.

        ``None`` covers both "gh is not installed" and "gh is installed but
        logged out". From here those are the same answer and earn the same
        message, so they are not distinguished.

        The name is read out of `gh auth status`'s own prose, which is not a
        stable interface. When its shape changes we fall back to a nameless
        stand-in rather than reporting a signed-in user as signed out: the name
        is there to tell somebody whose credential they are about to lend, and
        losing the name is worth a vaguer prompt, not a dead end.
        """
        import re

        result = _run_gh("auth", "status")
        if result is None:
            return None
        stdout, stderr = result
        match = re.search(r"account (\S+)", f"{stdout}\n{stderr}")
        return match.group(1) if match else "your GitHub account"

    @staticmethod
    def _borrow_personal_token(args) -> Optional[str]:
        """Offer the `gh` CLI's credential to a run that has none. Never silent.

        Returns the token, or ``None`` meaning **stop** -- `gh` is not there,
        this run cannot ask anybody, or the person said no. The caller turns
        every one of those into a non-zero exit: a release that did not happen
        must not look like one that did.

        **The token value is never printed** -- not in the prompt, not in the
        confirmation that follows, not in an error. It is handed to the engine
        as an argument to an in-process call rather than through a shell, so it
        does not reach a process listing either.

        **Saying what it costs is the point, not decoration.** This lends a
        *personal* credential to an organisation's release: the tags and the
        GitHub Releases carry that person's name, and the scopes are whatever
        that account happens to have rather than what the release needs. See the
        note above `_run_gh` and `havilandsoftware/innoday#753`.
        """
        import sys

        # Word for word what this said before the offer existed -- for somebody
        # without `gh`, nothing has changed.
        no_token = format_error(
            "No GitHub token provided! Set GH_TOKEN environment variable or "
            "use --token flag."
        )

        account = ReleaseProxyCommands._gh_account()
        if account is None:
            console.print(no_token)
            return None

        # **A prompt needs somebody to answer it.** With no terminal there is
        # nobody, and under `--json` the output is one document for a machine
        # that a question would corrupt. Borrowing somebody's personal
        # credential is the last thing to do on an assumption, so neither case
        # asks: they say what could be done and fail, as before.
        if getattr(args, "as_json", False) or not sys.stdin.isatty():
            console.print(no_token)
            console.print(
                format_info(
                    f"`gh` is signed in as {account}. Run this from a terminal "
                    "to be offered that credential, or pass --token."
                )
            )
            return None

        console.print(
            format_warning(
                "No organisation credential reached this run. `gh` is signed "
                f"in as {account} -- that is a personal credential: every tag "
                "and GitHub Release created here would be attributed to that "
                "account, not to the organisation."
            )
        )
        print(
            f"\nUse {account}'s personal GitHub token for this release? [y/N] ",
            end="",
            flush=True,
        )
        if sys.stdin.readline().strip().lower() not in ("y", "yes"):
            console.print(format_info("Nothing was tagged."))
            return None

        result = _run_gh("auth", "token")
        token = result[0].strip() if result else ""
        if not token:
            # `gh auth status` said yes and `gh auth token` said nothing: the
            # same dead end as having no `gh` at all, and treated as one.
            console.print(format_error("`gh auth token` returned no token."))
            console.print(no_token)
            return None

        console.print(
            format_warning(
                f"Releasing with {account}'s personal credential -- the tags "
                "and GitHub Releases will be attributed to that account rather "
                "than to the organisation."
            )
        )
        return token

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
            # **Whatever the engine returned is the answer, including 2.**
            # `retcode or 0` read as defensive and was the opposite: plumbum has
            # already turned a `main()` that returned None into 0 by the time we
            # see it, so the expression could only ever flatten a code, never
            # supply a missing one. It is spelt out because the bug it stood
            # next to -- an engine that stopped without a GitHub token and
            # returned None, which the CLI reported as a successful release --
            # looked like something this line was doing.
            #
            # None is unreachable through plumbum and reachable through a test
            # double, and means the same thing there: nothing said it failed.
            if retcode is None:
                return 0
            return int(retcode)
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
