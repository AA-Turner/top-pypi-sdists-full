"""`probe update` updates the transcript tap, says where it landed, and fails
loudly when it stays behind; `probe doctor` warns about a tap behind the manifest.

The tap is a SEPARATE plugin in the same marketplace. `probe update` has issued
`claude plugin update probe-research-tap@...` since #167, but read nothing back:
a tap left a version behind (seen twice on 09-23, fixed by hand with `claude
plugin marketplace update` + `claude plugin update`) was reported as a clean
update. Every test here fakes the plugin CLI; nothing reaches a real `claude`
or `codex`.
"""

from __future__ import annotations

import pytest

from probe.cli import autoupdate, claude_cli, doctor, updater, upgrading
from probe.cli.versions import Comparison, VersionStatus

MANIFEST = {
    "cli": {"latest": "0.179.3"},
    "plugin": {"latest": "0.96.1"},
    "tap": {"latest": "0.7.2"},
}


@pytest.fixture(autouse=True)
def isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    monkeypatch.delenv(autoupdate.WAIT_FOR_PID_ENV, raising=False)


def _seq(values):
    it = iter(values)
    return lambda: next(it)


# ---------------------------------------------------------------------------
# update_plugin reads the tap on both sides of its own update.
# ---------------------------------------------------------------------------


def _fake_claude(monkeypatch, issued):
    def _run(args, *, timeout):
        issued.append(list(args))
        return claude_cli.Result(ok=True)

    monkeypatch.setattr(updater.claude_cli, "run", _run)
    monkeypatch.setattr(updater.shutil, "which", lambda _name: "/usr/local/bin/claude")


def test_update_plugin_reads_the_tap_before_and_after_its_update(monkeypatch):
    issued: list[list[str]] = []
    _fake_claude(monkeypatch, issued)
    monkeypatch.setattr(updater, "installed_plugin_version", lambda: "0.96.1")
    monkeypatch.setattr(updater, "installed_tap_version", _seq(["0.7.1", "0.7.2"]))

    result = updater.update_plugin("0.96.1")

    assert issued == [
        ["plugin", "marketplace", "update", updater.MARKETPLACE],
        ["plugin", "update", updater.PLUGIN_ID],
        ["plugin", "update", updater.TAP_PLUGIN_ID],
    ]
    assert (result.tap_before, result.tap_after) == ("0.7.1", "0.7.2")
    assert updater.tap_changed(result)
    assert updater.tap_verdict(result, "0.7.2") == ("transcript tap updated to 0.7.2", False)


def _fake_claude_failing_tap(monkeypatch, result):
    """`claude` succeeds for everything but the tap update, which returns `result`."""

    def _run(args, *, timeout):
        if updater.TAP_PLUGIN_ID in args:
            return result
        return claude_cli.Result(ok=True, command=" ".join(["claude", *args]))

    monkeypatch.setattr(updater.claude_cli, "run", _run)
    monkeypatch.setattr(updater.shutil, "which", lambda _name: "/usr/local/bin/claude")
    monkeypatch.setattr(updater, "installed_plugin_version", lambda: "0.96.1")
    monkeypatch.setattr(updater, "installed_tap_version", lambda: "0.7.1")


TAP_COMMAND = f"claude plugin update {updater.TAP_PLUGIN_ID}"


@pytest.mark.parametrize(
    ("result", "reason"),
    [
        (
            claude_cli.Result(ok=False, detail="Error: network unreachable", command=TAP_COMMAND),
            f"`{TAP_COMMAND}` did not complete: Error: network unreachable",
        ),
        (
            claude_cli.Result(
                ok=False, detail="timed out after 90s", reachable=False, command=TAP_COMMAND
            ),
            f"`{TAP_COMMAND}` did not complete: timed out after 90s",
        ),
        # Exit 0 and nothing moved: the in-session no-op.
        (claude_cli.Result(ok=True, command=TAP_COMMAND), updater.TAP_NOOP),
    ],
    ids=["failed", "timed-out", "no-op"],
)
def test_a_tap_that_did_not_move_says_why(monkeypatch, result, reason):
    _fake_claude_failing_tap(monkeypatch, result)

    pres = updater.update_plugin("0.96.1")

    assert pres.tap_detail == reason
    line, behind = updater.tap_verdict(pres, "0.7.2")
    assert behind
    assert line == f"transcript tap is still 0.7.1, behind the latest 0.7.2: {reason}"


def test_a_failed_refresh_is_the_taps_reason_too(monkeypatch):
    """With the plugin already current, its own line never mentions the refresh:
    a bare "skipped" on the tap's line left the reason nowhere on screen."""
    issued: list[list[str]] = []

    def _run(args, *, timeout):
        issued.append(list(args))
        ok = "marketplace" not in args
        return claude_cli.Result(ok=ok, detail="" if ok else "fatal: no network",
                                 command=" ".join(["claude", *args]))

    monkeypatch.setattr(updater.claude_cli, "run", _run)
    monkeypatch.setattr(updater.shutil, "which", lambda _name: "/usr/local/bin/claude")
    monkeypatch.setattr(updater, "installed_plugin_version", lambda: "0.96.1")
    monkeypatch.setattr(updater, "installed_tap_version", lambda: "0.7.1")

    pres = updater.update_plugin("0.96.1")

    assert ["plugin", "update", updater.TAP_PLUGIN_ID] not in issued
    assert pres.confirmed
    assert pres.tap_detail == (
        f"`claude plugin marketplace update {updater.MARKETPLACE}` did not complete: "
        "fatal: no network"
    )
    assert pres.git_blocked is False


def test_the_reason_reaches_the_update_record(monkeypatch):
    _stub_cli(monkeypatch)
    monkeypatch.setattr(
        upgrading.updater,
        "update_plugin",
        lambda target: updater.PluginResult(
            True, True, False, "0.96.1", "0.96.1", "plugin already at the latest (0.96.1)",
            tap_before="0.7.1", tap_after="0.7.1",
            tap_detail=f"`{TAP_COMMAND}` did not complete: Error: network unreachable",
        ),
    )

    outcome = upgrading.perform_update(base_url="https://x", include_plugin=True)

    detail = autoupdate.load().last_attempt.plugin_detail
    assert "Error: network unreachable" in detail
    assert any("Error: network unreachable" in line for line in outcome.lines)


def test_a_tap_no_op_reads_like_a_plugin_no_op(monkeypatch):
    """Exit 0 with nothing moved is one outcome whichever plugin it happens to:
    not confirmed, the same explanation, and the same exit code."""
    _stub_cli(monkeypatch)
    plugin_noop = updater.PluginResult(
        True, False, False, "0.96.0", "0.96.0",
        "`claude` returned success but the plugin version did not advance "
        "(it may have run inside a Claude Code session, which no-ops)",
        tap_before="0.7.2", tap_after="0.7.2", tap_detail=updater.TAP_NOOP,
    )
    tap_noop = updater.PluginResult(
        True, True, False, "0.96.1", "0.96.1", "plugin already at the latest (0.96.1)",
        tap_before="0.7.1", tap_after="0.7.1", tap_detail=updater.TAP_NOOP,
    )
    outcomes = []
    for result in (plugin_noop, tap_noop):
        monkeypatch.setattr(upgrading.updater, "update_plugin", lambda target, r=result: r)
        outcome = upgrading.perform_update(base_url="https://x", include_plugin=True)
        outcomes.append((outcome.ok, autoupdate.load().last_attempt.plugin_ok))
        assert "may have run inside a Claude Code session" in autoupdate.load().last_attempt.plugin_detail
    assert outcomes[0] == outcomes[1]


def test_a_codex_tap_that_did_not_move_says_why(monkeypatch):
    monkeypatch.setattr(updater.shutil, "which", lambda _name: "/usr/bin/codex")
    ok = updater.claude_cli.Result(ok=True)
    monkeypatch.setattr(updater.plugin_cli, "refresh_marketplace", lambda source, marketplace: ok)
    monkeypatch.setattr(updater.plugin_cli, "install", lambda source, plugin_id: ok)
    same = {"probe-research": "0.96.1", "probe-research-tap": "0.7.1"}
    monkeypatch.setattr(updater, "_codex_plugin_versions", lambda codex: dict(same))

    pres = updater.update_codex_plugins()

    assert pres.tap_detail == updater.CODEX_TAP_NOOP
    assert updater.tap_verdict(pres, "0.7.2")[0].endswith(updater.CODEX_TAP_NOOP)


def test_the_tap_is_read_from_the_claude_ledger(tmp_path, monkeypatch):
    ledger = tmp_path / "home" / ".claude" / "plugins" / "installed_plugins.json"
    ledger.parent.mkdir(parents=True)
    ledger.write_text(
        '{"plugins": {"probe-research-tap@research-os-agent": [{"version": "0.7.1"}, '
        '{"version": "0.7.2"}], "probe-research@research-os-agent": [{"version": "0.96.1"}]}}'
    )
    assert updater.installed_tap_version() == "0.7.2"
    assert updater.installed_plugin_version() == "0.96.1"


@pytest.mark.parametrize(
    ("before", "after", "target", "line", "behind"),
    [
        (None, None, "0.7.2", "transcript tap not installed (skipped)", False),
        ("0.7.1", "0.7.1", "0.7.2", "transcript tap is still 0.7.1, behind the latest 0.7.2", True),
        ("0.7.1", "0.7.2", "0.7.2", "transcript tap updated to 0.7.2", False),
        ("0.7.2", "0.7.2", "0.7.2", "transcript tap already at the latest (0.7.2)", False),
        ("0.7.2", "0.7.2", None, "transcript tap at 0.7.2", False),
        # Ahead of an older manifest is not behind.
        ("0.7.3", "0.7.3", "0.7.2", "transcript tap already at the latest (0.7.3)", False),
    ],
)
def test_tap_verdict(before, after, target, line, behind):
    result = updater.PluginResult(True, True, False, "1", "1", "ok", tap_before=before, tap_after=after)
    assert updater.tap_verdict(result, target) == (line, behind)


def test_codex_carries_the_tap_versions_too(monkeypatch):
    monkeypatch.setattr(updater.shutil, "which", lambda _name: "/usr/bin/codex")
    ok = updater.claude_cli.Result(ok=True)
    monkeypatch.setattr(updater.plugin_cli, "refresh_marketplace", lambda source, marketplace: ok)
    monkeypatch.setattr(updater.plugin_cli, "install", lambda source, plugin_id: ok)
    versions = iter(
        [
            {"probe-research": "0.96.1", "probe-research-tap": "0.7.1"},
            {"probe-research": "0.96.1", "probe-research-tap": "0.7.1"},
        ]
    )
    monkeypatch.setattr(updater, "_codex_plugin_versions", lambda codex: next(versions))

    result = updater.update_codex_plugins()

    assert (result.tap_before, result.tap_after) == ("0.7.1", "0.7.1")
    assert updater.tap_verdict(result, "0.7.2")[1] is True


# ---------------------------------------------------------------------------
# perform_update prints all three versions and fails on a tap left behind.
# ---------------------------------------------------------------------------


def _stub_cli(monkeypatch):
    monkeypatch.setattr(upgrading.updater, "fetch_latest", lambda base: MANIFEST)
    monkeypatch.setattr(
        upgrading.updater, "detect_install", lambda: updater.Install(updater.Method.UV_TOOL)
    )
    monkeypatch.setattr(
        upgrading.updater,
        "upgrade_cli",
        lambda install, current, target: updater.CliResult(
            True, True, False, current, "0.179.3", "CLI already at the latest (0.179.3)"
        ),
    )


def _claude_result(tap_before, tap_after, *, confirmed=True):
    return updater.PluginResult(
        attempted=True,
        confirmed=confirmed,
        changed=False,
        before="0.96.1",
        after="0.96.1",
        message="plugin already at the latest (0.96.1)",
        tap_before=tap_before,
        tap_after=tap_after,
    )


def test_update_prints_the_cli_the_plugin_and_the_tap(monkeypatch):
    _stub_cli(monkeypatch)
    monkeypatch.setattr(
        upgrading.updater, "update_plugin", lambda target: _claude_result("0.7.1", "0.7.2")
    )

    outcome = upgrading.perform_update(base_url="https://x", include_plugin=True)

    text = "\n".join(outcome.lines)
    assert "CLI already at the latest (0.179.3)" in text
    assert "plugin already at the latest (0.96.1)" in text
    assert "transcript tap updated to 0.7.2" in text
    assert outcome.ok is True
    # A tap that moved needs a restart as much as a plugin that moved.
    assert outcome.restart_needed is True
    assert autoupdate.load().last_attempt.plugin_ok is True


def test_a_tap_left_behind_fails_the_update_and_says_how_to_fix_it(monkeypatch):
    _stub_cli(monkeypatch)
    monkeypatch.setattr(
        upgrading.updater, "update_plugin", lambda target: _claude_result("0.7.1", "0.7.1")
    )

    outcome = upgrading.perform_update(base_url="https://x", include_plugin=True)

    text = "\n".join(outcome.lines)
    assert "transcript tap is still 0.7.1, behind the latest 0.7.2" in text
    assert f"claude plugin update {updater.TAP_PLUGIN_ID}" in text
    assert f"claude plugin marketplace update {updater.MARKETPLACE}" in text
    assert outcome.ok is False
    attempt = autoupdate.load().last_attempt
    assert attempt.plugin_ok is False
    assert "transcript tap is still 0.7.1" in attempt.plugin_detail


def test_no_tap_installed_is_a_skip_not_a_failure(monkeypatch):
    _stub_cli(monkeypatch)
    monkeypatch.setattr(
        upgrading.updater, "update_plugin", lambda target: _claude_result(None, None)
    )

    outcome = upgrading.perform_update(base_url="https://x", include_plugin=True)

    assert any("transcript tap not installed (skipped)" in line for line in outcome.lines)
    assert outcome.ok is True
    assert autoupdate.load().last_attempt.plugin_ok is True


def test_a_codex_tap_left_behind_prints_the_codex_commands(monkeypatch):
    monkeypatch.setenv("PROBE_AGENT", "codex")
    _stub_cli(monkeypatch)
    monkeypatch.setattr(
        upgrading.updater, "update_codex_plugins", lambda: _claude_result("0.7.1", "0.7.1")
    )

    outcome = upgrading.perform_update(base_url="https://x", include_plugin=True)

    text = "\n".join(outcome.lines)
    assert "transcript tap is still 0.7.1, behind the latest 0.7.2" in text
    assert "codex plugin add probe-research-tap@research-os-agent" in text
    assert "restart Codex" in text
    assert outcome.ok is False


# ---------------------------------------------------------------------------
# probe doctor
# ---------------------------------------------------------------------------


def _row(kind, installed, latest, status):
    return Comparison(kind=kind, installed=installed, latest=latest, minimum=None, status=status)


def test_doctor_warns_when_the_tap_is_behind():
    rows = [
        _row("cli", "0.179.3", "0.179.3", VersionStatus.CURRENT),
        _row("tap", "0.7.1", "0.7.2", VersionStatus.UPDATE),
    ]
    warning = doctor.tap_behind_warning(rows)
    assert warning is not None
    assert "0.7.1" in warning and "0.7.2" in warning and "the wizard's Update" in warning


@pytest.mark.parametrize(
    "rows",
    [
        [],
        [_row("tap", "0.7.2", "0.7.2", VersionStatus.CURRENT)],
        [_row("tap", None, "0.7.2", VersionStatus.UNKNOWN)],
        # Another component behind is the Versions block's job, not this warning's.
        [_row("plugin", "0.95.0", "0.96.1", VersionStatus.UPDATE)],
    ],
)
def test_doctor_is_silent_about_a_current_or_absent_tap(rows):
    assert doctor.tap_behind_warning(rows) is None


def test_doctor_renders_the_warning(monkeypatch):
    rows = (_row("tap", "0.7.1", "0.7.2", VersionStatus.UPDATE),)
    caps = doctor.Capabilities(
        version_rows=rows, warnings=[doctor.tap_behind_warning(rows)]
    )
    rendered = doctor.render(caps)
    assert "Warnings" in rendered
    assert "the transcript tap is 0.7.1, behind the published 0.7.2" in rendered



# ---------------------------------------------------------------------------
# A Mac whose git is blocked says the fix once, not the raw error four times.
# ---------------------------------------------------------------------------

#: Verbatim from a researcher's wizard, 2026-09-24: both CLIs shell out to git,
#: and macOS refuses to run it until the Xcode license is accepted.
XCODE_LICENSE = (
    "You have not agreed to the Xcode license agreements. Please run 'sudo xcodebuild "
    "-license' from within a Terminal window to review and agree to the Xcode and Apple "
    "SDKs license."
)
CLAUDE_LICENSE_FAILURE = (
    "✘ Failed to update marketplace(s): Failed to refresh marketplace 'research-os-agent': "
    f"Failed to clone marketplace repository: {XCODE_LICENSE}"
)
CODEX_LICENSE_FAILURE = (
    "Failed to upgrade marketplace `research-os-agent`: git ls-remote marketplace source "
    f"failed with status exit status: 69: {XCODE_LICENSE}\nError: 1 upgrade failure(s) occurred."
)
LICENSE_FIX = "`sudo xcodebuild -license`"


@pytest.mark.parametrize(
    ("detail", "fixes"),
    [
        (CLAUDE_LICENSE_FAILURE, [LICENSE_FIX]),
        (CODEX_LICENSE_FAILURE, [LICENSE_FIX]),
        (
            "Agreeing to the Xcode/iOS license requires admin privileges, please run "
            "“sudo xcodebuild -license” and then retry this command.",
            [LICENSE_FIX],
        ),
        # Current wordings, as a `git push` prints them.
        (
            "Agreeing to the Xcode and Apple SDKs license requires admin privileges, please "
            "accept the Xcode license as the root user (e.g. 'sudo xcodebuild -license').",
            [LICENSE_FIX],
        ),
        ("You have not agreed to the Xcode and Apple SDKs license.", [LICENSE_FIX]),
        (
            "xcrun: error: invalid active developer path (/Library/Developer/CommandLineTools), "
            "missing xcrun at: /Library/Developer/CommandLineTools/usr/bin/xcrun",
            ["`xcode-select --install`", "`sudo xcode-select --reset`"],
        ),
        (
            "xcode-select: note: No developer tools were found, requesting install.",
            ["`xcode-select --install`"],
        ),
        (
            'xcrun: error: active developer path ("/Applications/Xcode.app/Contents/Developer") '
            "does not exist",
            ["`xcode-select --install`", "`sudo xcode-select --reset`"],
        ),
    ],
    ids=[
        "claude-license",
        "codex-license",
        "license-non-admin",
        "license-root-user",
        "license-apple-sdks",
        "tools-missing",
        "tools-never-installed",
        "xcode-moved",
    ],
)
def test_a_blocked_git_is_said_as_its_fix(detail, fixes):
    message = updater._failed(claude_cli.Result(ok=False, detail=detail, command="x"))
    assert message.startswith("not updated: git on this Mac")
    assert all(fix in message for fix in fixes)
    assert "Failed to" not in message


def test_accepting_the_license_is_left_to_a_person():
    """`probe doctor` replays the fix inside agent sessions. The one-shot
    `-license accept` would let an agent with sudo accept it on the user's behalf."""
    message = updater._failed(claude_cli.Result(ok=False, detail=XCODE_LICENSE, command="x"))
    assert "-license accept" not in message


def test_any_other_failure_keeps_the_raw_reason():
    message = updater._failed(
        claude_cli.Result(ok=False, detail="fatal: could not resolve host", command="x")
    )
    assert message == "`x` did not complete: fatal: could not resolve host"


@pytest.mark.parametrize(
    "server_line",
    [
        "remote: You have not agreed to the Xcode license",
        # Wrapped by the CLI, or behind a colour code.
        "Failed to clone marketplace repository: remote: You have not agreed to the Xcode license",
        "\x1b[31mremote: see sudo xcodebuild -license\x1b[0m",
        # A server's ERR packet, as a real `git ls-remote` prints it.
        "fatal: remote error: You have not agreed to the Xcode license agreements.",
    ],
    ids=["bare", "wrapped", "coloured", "err-packet"],
)
def test_a_git_server_quoting_apple_does_not_hide_the_real_error(server_line):
    """`remote:` text comes from the server, not this machine."""
    detail = f"{server_line}\nfatal: repository not found"
    message = updater._failed(claude_cli.Result(ok=False, detail=detail, command="x"))
    assert message.startswith("`x` did not complete:")
    assert "repository not found" in message


def test_a_blocked_git_is_found_in_output_too_long_to_print_whole():
    """The raw output is matched: `clean_reason` keeps the two ends of a long one,
    and Apple's sentence can sit in the middle it drops."""
    detail = (
        "WARNING: proceeding, even though we could not create PATH aliases\n"
        + "Cloning into '/Users/r/.codex/tmp/marketplaces/research-os-agent'...\n" * 4
        + CODEX_LICENSE_FAILURE
        + "\nhint: "
        + "x" * 300
    )
    assert not updater.git_blocker(updater.clean_reason(detail)), "the test proves nothing"
    message = updater._failed(claude_cli.Result(ok=False, detail=detail, command="x"))
    assert message.startswith("not updated: git on this Mac")


def _update_that_fails(monkeypatch, agent, detail, plugin="0.96.0"):
    """`probe update` whose marketplace refresh fails with `detail`."""
    _stub_cli(monkeypatch)
    if agent == "codex":
        monkeypatch.setenv("PROBE_AGENT", "codex")
        monkeypatch.setattr(updater.shutil, "which", lambda _name: "/usr/bin/codex")
        monkeypatch.setattr(
            updater.plugin_cli,
            "refresh_marketplace",
            lambda source, marketplace: claude_cli.Result(
                ok=False, detail=detail, command=f"codex plugin marketplace upgrade {marketplace}"
            ),
        )
        monkeypatch.setattr(
            updater.plugin_cli,
            "install",
            lambda *a, **k: pytest.fail("reinstalled from a marketplace that did not refresh"),
        )
        monkeypatch.setattr(
            updater,
            "_codex_plugin_versions",
            lambda codex: {"probe-research": plugin, "probe-research-tap": "0.6.1"},
        )
    else:

        def _run(args, *, timeout):
            ok = "marketplace" not in args
            return claude_cli.Result(
                ok=ok, detail="" if ok else detail, command=" ".join(["claude", *args])
            )

        monkeypatch.setattr(updater.claude_cli, "run", _run)
        monkeypatch.setattr(updater.shutil, "which", lambda _name: "/usr/local/bin/claude")
        monkeypatch.setattr(updater, "installed_plugin_version", lambda: plugin)
        monkeypatch.setattr(updater, "installed_tap_version", lambda: "0.6.1")
    return upgrading.perform_update(base_url="https://x", include_plugin=True)


@pytest.mark.parametrize(
    ("agent", "detail"),
    [("claude", CLAUDE_LICENSE_FAILURE), ("codex", CODEX_LICENSE_FAILURE)],
)
def test_a_blocked_mac_gets_one_plain_fix_and_no_manual_commands(monkeypatch, agent, detail):
    outcome = _update_that_fails(monkeypatch, agent, detail)

    text = "\n".join(outcome.lines)
    assert text.count(LICENSE_FIX) == 1
    assert "You have not agreed" not in text
    assert "transcript tap is still 0.6.1, behind the latest 0.7.2: same failure as above" in text
    # The manual commands run the same git and would fail the same way.
    assert "update them manually" not in text
    assert "marketplace update" not in text and "marketplace upgrade" not in text
    assert outcome.ok is False
    attempt = autoupdate.load().last_attempt
    assert attempt.plugin_ok is False
    assert LICENSE_FIX in attempt.plugin_detail


def test_a_current_plugin_with_a_tap_behind_still_gets_the_fix(monkeypatch):
    """The plugin's own line says "already at the latest" and never mentions the
    refresh, so the fix has to ride on the tap's line or it is not on screen."""
    outcome = _update_that_fails(monkeypatch, "claude", CLAUDE_LICENSE_FAILURE, plugin="0.96.1")

    text = "\n".join(outcome.lines)
    assert "plugin already at the latest (0.96.1)" in text
    assert (
        "transcript tap is still 0.6.1, behind the latest 0.7.2: not updated: git on this Mac"
        in text
    )
    assert text.count(LICENSE_FIX) == 1
    assert "update them manually" not in text
    assert outcome.ok is False
    assert LICENSE_FIX in autoupdate.load().last_attempt.plugin_detail


@pytest.mark.parametrize(
    ("agent", "manual"),
    [
        ("claude", f"claude plugin update {updater.PLUGIN_ID}"),
        ("codex", "codex plugin add probe-research@research-os-agent"),
    ],
)
def test_any_other_failure_is_said_once_and_keeps_the_manual_commands(monkeypatch, agent, manual):
    """Only a blocked git drops the manual commands; a network failure is one a
    retry by hand can get past."""
    outcome = _update_that_fails(monkeypatch, agent, "fatal: could not resolve host")

    text = "\n".join(outcome.lines)
    assert text.count("could not resolve host") == 1
    assert "behind the latest 0.7.2: same failure as above" in text
    assert "update them manually" in text
    assert manual in text
    assert outcome.ok is False



def test_a_tap_that_alone_hits_the_blocked_git_gets_the_fix_and_keeps_the_commands(monkeypatch):
    """Only the refresh runs git. A later step saying otherwise contradicts a
    refresh that just worked, so it is shown but hides nothing: keyed on it, a
    plugin already current could hide the commands with the fix off screen."""
    _stub_cli(monkeypatch)

    def _run(args, *, timeout):
        ok = updater.TAP_PLUGIN_ID not in args
        return claude_cli.Result(
            ok=ok, detail="" if ok else XCODE_LICENSE, command=" ".join(["claude", *args])
        )

    monkeypatch.setattr(updater.claude_cli, "run", _run)
    monkeypatch.setattr(updater.shutil, "which", lambda _name: "/usr/local/bin/claude")
    monkeypatch.setattr(updater, "installed_plugin_version", lambda: "0.96.1")
    monkeypatch.setattr(updater, "installed_tap_version", lambda: "0.6.1")

    outcome = upgrading.perform_update(base_url="https://x", include_plugin=True)

    text = "\n".join(outcome.lines)
    assert "behind the latest 0.7.2: not updated: git on this Mac" in text
    assert "update them manually" in text


def test_a_blocked_later_step_never_hides_the_commands_without_the_fix(monkeypatch):
    """The plugin is already current, so its own failure is never printed: a
    flag keyed on it hid the manual commands with no fix anywhere on screen."""
    _stub_cli(monkeypatch)

    def _run(args, *, timeout):
        ok = args[:2] != ["plugin", "update"] or updater.TAP_PLUGIN_ID in args
        return claude_cli.Result(
            ok=ok, detail="" if ok else XCODE_LICENSE, command=" ".join(["claude", *args])
        )

    monkeypatch.setattr(updater.claude_cli, "run", _run)
    monkeypatch.setattr(updater.shutil, "which", lambda _name: "/usr/local/bin/claude")
    monkeypatch.setattr(updater, "installed_plugin_version", lambda: "0.96.1")
    monkeypatch.setattr(updater, "installed_tap_version", lambda: "0.6.1")

    outcome = upgrading.perform_update(base_url="https://x", include_plugin=True)

    text = "\n".join(outcome.lines)
    assert "plugin already at the latest (0.96.1)" in text
    assert LICENSE_FIX not in text
    assert "update them manually" in text
