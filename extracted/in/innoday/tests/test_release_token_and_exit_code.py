"""A release that did not happen must not exit 0 -- and may offer to borrow `gh`.

Two faults in the same command, found together.

**The exit code.** With no GitHub token, `innoday blastoff --yes` printed
`❌  No GitHub token provided!` and exited **0**. The engine stopped by
returning None, plumbum turned that into 0, and the proxy passed it on, so every
CI job and script reading the exit code saw a successful release. Nothing was
tagged.

**The dead end.** That message is the end of the road: set an environment
variable and start again. Where the `gh` CLI is installed and signed in there is
a credential right there, so the run now offers it -- and says, every time, that
it is a *personal* one and that the tags and GitHub Releases will carry that
person's name rather than the organisation's. That is a stopgap for the platform
lending its own credential (`havilandsoftware/innoday#753`), not a convenience,
which is why it always asks and never assumes.
"""

import argparse
import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.cli.commands.release_proxy import ReleaseProxyCommands

# An obviously fake credential, distinctive enough that a substring search of
# everything the command printed is a real check that it never leaked.
TOKEN = "gho_NEVER_PRINT_THIS_abc123"

GH_STATUS = (
    "github.com\n"
    "  ✓ Logged in to github.com account octocat (keyring)\n"
    "  - Token scopes: 'repo', 'read:org'\n"
)


def args(**overrides):
    """The namespace `blastoff` builds, with the release-shaped defaults."""
    defaults = dict(
        hotfix=False,
        dry_run=False,
        do_release=False,
        assume_yes=True,  # the reported case: `--yes`, so the run will tag
        topics=None,
        repo=None,
        commit=None,
        branch=None,
        org_id="org-1",
        project_id="proj-1",
        token=None,
        github_org=None,
        summary=None,
        commits=False,
        as_json=False,
        generate_summary=False,
        dir=None,
    )
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def store():
    st = MagicMock()
    st.load_org_config.return_value = SimpleNamespace(
        next_version="v1.4.0",
        last_released_version="v1.3.0",
        last_released="2026-07-01T00:00:00Z",
        topics=["pf"],
    )
    st.ticket_picture.return_value = None
    return st


class FakeStdin:
    """A terminal that answers one question.

    `isatty()` is what decides whether the offer is made at all, and
    `readline()` is how `_borrow_personal_token` reads the answer -- the same
    pair `_confirmer` uses, for the same reason: by the time the engine runs,
    stdin has been replaced by the brief.
    """

    def __init__(self, answer="", tty=True):
        self._answer = answer
        self._tty = tty

    def isatty(self):
        return self._tty

    def readline(self):
        return self._answer


def drive(monkeypatch, *, stdin=None, gh=None, env_token=None, **arg_overrides):
    """Run `_drive_release`, returning (exit code, argv handed to the engine).

    argv is None when the engine was never reached -- which is the point of
    several of these tests: a run that cannot get a credential must not start.
    """
    monkeypatch.delenv("GH_TOKEN", raising=False)
    if env_token:
        monkeypatch.setenv("GH_TOKEN", env_token)
    monkeypatch.setattr("sys.stdin", stdin or FakeStdin(tty=False))

    captured = {"argv": None}

    def fake_invoke(app_cls, argv, st, stdin=None, confirm=None):
        captured["argv"] = argv
        return 0

    async def fake_content(*a, **k):
        # **Assembled, as it is in the real thing.** This returned None, which
        # is the *fallback* -- the org has no GitHub connection and the engine
        # has to go and find the release itself. `test_a_report_only_run_needs
        # _nothing` is about the opposite case, so it has to be handed content
        # for its name to be true. The shape only has to be truthy; nothing here
        # renders it.
        return {"repos": ["web"], "included": [], "outstanding": []}

    gh_calls = []

    def fake_gh(*argv):
        gh_calls.append(argv)
        return gh(*argv) if gh else None

    with (
        patch.object(
            ReleaseProxyCommands, "_invoke_blastoff", staticmethod(fake_invoke)
        ),
        patch.object(
            ReleaseProxyCommands, "_fetch_content", staticmethod(fake_content)
        ),
        patch("src.cli.commands.release_proxy._run_gh", fake_gh),
    ):
        code = asyncio.run(
            ReleaseProxyCommands._drive_release(
                args(**arg_overrides),
                store(),
                "pf",
                "havilandsoftware",
                ["pf"],
                MagicMock(),
                "org-1",
                "proj-1",
            )
        )
    captured["code"] = code
    captured["gh_calls"] = gh_calls
    return captured


def signed_in(*argv):
    """A `gh` that is installed, signed in, and will hand over a token."""
    if argv == ("auth", "status"):
        return GH_STATUS, ""
    if argv == ("auth", "token"):
        return f"{TOKEN}\n", ""
    return None


class TestTheExitCodeIsTheEnginesAnswer:
    """`retcode or 0` could only ever flatten a code, never supply one."""

    @staticmethod
    def _engine(retcode):
        class FakeEngine:
            version_store = None
            confirm = None

            @staticmethod
            def run(argv, exit=True):
                return object(), retcode

        return FakeEngine

    @pytest.mark.parametrize("retcode", [1, 2, 3])
    def test_a_failure_propagates(self, retcode):
        assert (
            ReleaseProxyCommands._invoke_blastoff(
                self._engine(retcode), [], MagicMock()
            )
            == retcode
        )

    def test_success_is_still_zero(self):
        assert (
            ReleaseProxyCommands._invoke_blastoff(self._engine(0), [], MagicMock()) == 0
        )

    def test_none_is_zero(self):
        """Unreachable through plumbum, which converts it first, and reachable
        through a test double. It means the same thing in both: nothing said it
        failed."""
        assert (
            ReleaseProxyCommands._invoke_blastoff(self._engine(None), [], MagicMock())
            == 0
        )

    def test_the_release_returns_what_the_engine_said(self, monkeypatch):
        """The code has to survive `_drive_release`, not just `_invoke_blastoff`."""
        monkeypatch.delenv("GH_TOKEN", raising=False)

        async def fake_content(*a, **k):
            return None

        def failing_invoke(*a, **k):
            return 1

        with (
            patch.object(
                ReleaseProxyCommands, "_invoke_blastoff", staticmethod(failing_invoke)
            ),
            patch.object(
                ReleaseProxyCommands, "_fetch_content", staticmethod(fake_content)
            ),
        ):
            code = asyncio.run(
                ReleaseProxyCommands._drive_release(
                    args(token="supplied"),  # a token, so the offer never fires
                    store(),
                    "pf",
                    "havilandsoftware",
                    ["pf"],
                    MagicMock(),
                    "org-1",
                    "proj-1",
                )
            )
        assert code == 1

    def test_the_process_exits_with_it(self):
        """...and survives the CLI's own dispatch, which is what CI reads."""
        from src.cli import main as cli_main

        with (
            patch.object(
                cli_main,
                "CLIConfig",
                return_value=MagicMock(legacy_context_error=None),
            ),
            patch.object(cli_main, "_prime_org_id", new=AsyncMock()),
            patch.object(
                cli_main, "_prime_project_id", new=AsyncMock(return_value=None)
            ),
            patch.object(
                cli_main.ReleaseProxyCommands,
                "execute_release",
                new=AsyncMock(return_value=1),
            ),
        ):
            assert cli_main.main(["blastoff"]) == 1


class TestWithoutGh:
    """No `gh`, or a logged-out one: the message does not change, the code does."""

    def test_the_old_message_survives(self, monkeypatch, capsys):
        drive(monkeypatch, stdin=FakeStdin(tty=True), gh=lambda *a: None)
        assert "No GitHub token" in capsys.readouterr().out

    def test_it_does_not_release(self, monkeypatch):
        result = drive(monkeypatch, stdin=FakeStdin(tty=True), gh=lambda *a: None)
        assert result["argv"] is None, "the engine must not be reached"
        assert result["code"] == 1

    def test_a_logged_out_gh_is_the_same_answer(self, monkeypatch, capsys):
        """`_run_gh` returns None for a non-zero exit, which is what
        `gh auth status` does when nobody is logged in."""
        result = drive(
            monkeypatch,
            stdin=FakeStdin(tty=True),
            gh=lambda *a: None if a == ("auth", "status") else (TOKEN, ""),
        )
        assert result["code"] == 1
        assert ("auth", "token") not in result["gh_calls"]
        assert TOKEN not in capsys.readouterr().out


class TestWithGh:
    """Installed and signed in: ask, say what it costs, and honour the answer."""

    def test_declining_does_not_release(self, monkeypatch, capsys):
        result = drive(monkeypatch, stdin=FakeStdin("n\n"), gh=signed_in)
        assert result["argv"] is None, "the engine must not be reached"
        assert result["code"] == 1
        assert ("auth", "token") not in result["gh_calls"], "never fetched unasked"
        assert "Nothing was tagged" in capsys.readouterr().out

    def test_accepting_supplies_the_token(self, monkeypatch):
        result = drive(monkeypatch, stdin=FakeStdin("y\n"), gh=signed_in)
        assert result["code"] == 0
        assert result["argv"][-2:] == ["-k", TOKEN]

    def test_the_prompt_says_it_is_personal(self, monkeypatch, capsys):
        drive(monkeypatch, stdin=FakeStdin("y\n"), gh=signed_in)
        out = capsys.readouterr().out
        assert "personal" in out
        assert "octocat" in out, "whose account is the whole point of asking"
        assert "attributed to that account" in out

    def test_the_token_is_never_printed(self, monkeypatch, capsys):
        """Not in the prompt, not in the confirmation, not anywhere."""
        drive(monkeypatch, stdin=FakeStdin("y\n"), gh=signed_in)
        captured = capsys.readouterr()
        assert TOKEN not in captured.out
        assert TOKEN not in captured.err

    def test_an_empty_token_is_no_token(self, monkeypatch, capsys):
        """`gh auth status` says yes and `gh auth token` says nothing: the same
        dead end as having no `gh`, and treated as one."""
        result = drive(
            monkeypatch,
            stdin=FakeStdin("y\n"),
            gh=lambda *a: (GH_STATUS, "") if a == ("auth", "status") else ("\n", ""),
        )
        assert result["code"] == 1
        assert result["argv"] is None
        assert "No GitHub token" in capsys.readouterr().out


class TestNobodyToAsk:
    """A credential this personal is never taken on an assumption."""

    def test_a_pipe_is_not_prompted(self, monkeypatch, capsys):
        result = drive(monkeypatch, stdin=FakeStdin(tty=False), gh=signed_in)
        assert result["code"] == 1
        assert result["argv"] is None
        assert ("auth", "token") not in result["gh_calls"]
        out = capsys.readouterr().out
        assert "No GitHub token" in out
        assert "terminal" in out, "say what could be done instead"

    def test_json_is_not_prompted(self, monkeypatch):
        """One document for a machine; a question would corrupt it. `--json`
        never tags either, so this is the hotfix's path into the same guard."""
        assert ReleaseProxyCommands._borrow_personal_token(args(as_json=True)) is None


class TestWhatAlreadyHasACredential:
    """`--token` and `GH_TOKEN` keep precedence, unchanged."""

    def test_an_explicit_token_is_not_second_guessed(self, monkeypatch):
        result = drive(
            monkeypatch, stdin=FakeStdin("y\n"), gh=signed_in, token="supplied"
        )
        assert result["gh_calls"] == [], "`gh` is not consulted at all"
        assert result["argv"][2:4] == ["-k", "supplied"]

    def test_the_env_var_is_enough(self, monkeypatch):
        """The engine reads `GH_TOKEN` itself, so the proxy adds no `-k` -- it
        just has to recognise that a credential is already here and not ask."""
        result = drive(
            monkeypatch,
            stdin=FakeStdin("y\n"),
            gh=signed_in,
            env_token="from-the-environment",
        )
        assert result["gh_calls"] == [], "`gh` is not consulted at all"
        assert result["code"] == 0
        assert "-k" not in result["argv"]

    def test_a_report_only_run_needs_nothing(self, monkeypatch):
        """The content arrives assembled, so a report touches GitHub not at all
        -- which is the whole reason the proxy stopped asking for a token."""
        result = drive(
            monkeypatch,
            stdin=FakeStdin(tty=True),
            gh=signed_in,
            assume_yes=False,
            do_release=False,
        )
        assert result["gh_calls"] == []
        assert result["code"] == 0
        assert "-k" not in result["argv"]


class TestANarrowedHotfix:
    """The same guard, on the one path that still reads GitHub to report.

    A hotfix used to need a credential for its report **always**, because it
    assembled itself from GitHub rather than from content the platform had
    fetched. Now it is driven like a release and gets the same assembled
    content -- except when `--repo`, `--commit` or `--branch` narrow it, which
    the `/release/content` payload cannot express. Those still read GitHub from
    here, and are still offered `gh`'s credential rather than dead-ended.
    """

    def _drive(self, monkeypatch, *, stdin, gh, **overrides):
        monkeypatch.delenv("GH_TOKEN", raising=False)
        monkeypatch.setattr("sys.stdin", stdin)
        captured = {"argv": None, "asked_the_server": False}

        def fake_invoke(app_cls, argv, st, stdin=None, confirm=None):
            captured["argv"] = argv
            return 0

        async def fake_content(*a, **k):
            captured["asked_the_server"] = True
            return {"repos": ["web"], "included": [], "outstanding": []}

        with (
            patch.object(
                ReleaseProxyCommands, "_invoke_blastoff", staticmethod(fake_invoke)
            ),
            patch.object(
                ReleaseProxyCommands, "_fetch_content", staticmethod(fake_content)
            ),
            patch("src.cli.commands.release_proxy._run_gh", gh),
        ):
            captured["code"] = asyncio.run(
                ReleaseProxyCommands._drive_release(
                    args(hotfix=True, repo="web", **overrides),
                    store(),
                    "pf",
                    "havilandsoftware",
                    ["pf"],
                    MagicMock(),
                    "org-1",
                    "proj-1",
                    hotfix=True,
                )
            )
        return captured

    def test_without_gh_it_fails(self, monkeypatch, capsys):
        result = self._drive(monkeypatch, stdin=FakeStdin(tty=True), gh=lambda *a: None)
        assert result["code"] == 1
        assert result["argv"] is None
        assert "No GitHub token" in capsys.readouterr().out

    def test_accepting_supplies_the_token(self, monkeypatch, capsys):
        result = self._drive(monkeypatch, stdin=FakeStdin("y\n"), gh=signed_in)
        assert result["code"] == 0
        assert result["argv"][-2:] == ["-k", TOKEN]
        assert TOKEN not in capsys.readouterr().out

    def test_it_does_not_ask_the_server_for_content_it_cannot_use(self, monkeypatch):
        """The window the platform assembles has no end and covers every
        repository; a narrowed hotfix would render work its tag does not
        contain."""
        result = self._drive(monkeypatch, stdin=FakeStdin("y\n"), gh=signed_in)
        assert result["asked_the_server"] is False
