"""A stateful in-memory fake of the Probe Research v3 API over httpx.MockTransport.

Routes only what the client exercises, with response shapes matching CONTRACT.md.
Lets us test the SDK + CLI end to end with no live server.
"""

from __future__ import annotations

import base64
import hashlib
import json
import math
import os
import re
import sys
import tempfile
import unicodedata
import uuid
from pathlib import Path

import httpx
import pytest

from probe.client import Client
from probe.config import Settings
from probe.sdk.tags import canonical_tags as _canonical_tags
from probe.transport import Transport


@pytest.fixture(autouse=True)
def _daemon_bites_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    """The daemon's default mode is `conversation` (2026-09-27); the suite's worker
    tests were written for `bites` and pin it. A conversation test sets the mode
    itself, and `test_the_mode_is_read_from_the_environment` checks the default."""
    monkeypatch.setenv("PROBE_DAEMON_MODE", "bites")


@pytest.fixture(autouse=True)
def _fresh_log_stream_answer() -> None:
    """`logstream.server_accepts` keeps the server's answer for the PROCESS
    (plan item (h)); every test here builds its own fake server, so each one
    asks afresh -- otherwise one test's old server decides the next one's."""
    from probe.sdk import logstream

    logstream.reset_feature_cache()


@pytest.fixture(autouse=True)
def _telemetry_off(monkeypatch: pytest.MonkeyPatch) -> None:
    """Pin client telemetry OFF for the whole suite.

    A CI runner has no config file, which RESOLVES to the hosted default — so
    without this, every wizard/backfill test would start a real sender thread
    and post real events to PostHog. Telemetry tests that need the pipeline on
    override this env var themselves and stub the transport.
    """
    monkeypatch.setenv("PROBE_TELEMETRY", "off")


@pytest.fixture(autouse=True)
def _no_real_takeover_wait(monkeypatch: pytest.MonkeyPatch) -> None:
    """A relaunch onto a `running` incumbent now WAITS (2.3), up to 300 s by
    default, for the fake server to call it silent. Every test that opens a
    live duplicate would sleep for real. Tests ABOUT the wait set the budget
    themselves and replace `probe.sdk.client._takeover_sleep`."""
    monkeypatch.setenv("PROBE_TAKEOVER_WAIT_SEC", "0")


@pytest.fixture(autouse=True)
def _no_real_cli_telemetry(monkeypatch: pytest.MonkeyPatch) -> None:
    """No test may reach real PostHog through the CLI's own sender.

    `_telemetry_off` above is the killswitch, and it is the only thing standing
    between this suite and the vendor -- so any test that legitimately turns
    telemetry back ON (the funnel tests do) is one forgotten stub away from a
    live POST from CI. That is not theoretical: a job-telemetry test that
    enabled the pipeline without replacing the queue seam opened a real socket
    and took the interpreter down with it.

    Replaces `_ensure_sender` -- the one door `emit()` goes through -- rather
    than the `_post_batch` alias, which is itself under test (its whole point
    is being the shared core's wire shape, and a stub there asserts against
    the stub). The substitute never starts a drain thread, so nothing can
    reach the network even before the exploding transport would say so.

    Tests that assert on emissions replace the queue seam themselves and never
    get here; this is the floor, exactly like `_no_real_mcp_accounting` below.
    """
    from probe.cli import telemetry

    def _explode(_batch: list) -> None:
        raise AssertionError("CLI telemetry attempted a real PostHog post")

    sender = telemetry._Sender()
    sender.transport = _explode
    monkeypatch.setattr(telemetry, "_ensure_sender", lambda: sender)


@pytest.fixture(autouse=True)
def _no_real_daemon_install(monkeypatch: pytest.MonkeyPatch) -> None:
    """No test may pip-install the daemon's AI libraries for real.

    Choosing `daemon` provisions them (`probe.cli.companion.provision_daemon`),
    and whether that path installs depends on what the machine running the
    tests already has: a dev box with the extra skips it, a CI runner without
    it ran `pip install` and failed a release gate (0.186.0). Tests of the
    install path replace `daemon_install` themselves.
    """
    from probe.cli import daemon_cli

    def _explode() -> None:
        raise AssertionError("a test reached the real `probe daemon install` (pip)")

    monkeypatch.setattr(daemon_cli, "daemon_install", _explode)


@pytest.fixture(autouse=True)
def _no_ambient_pi_binary(monkeypatch: pytest.MonkeyPatch) -> None:
    """Pin pi-binary detection OFF for the whole suite.

    `setup.detectable_sources()` checks `setup.pi_binary_available()` -- a
    real `shutil.which("pi")` -- deliberately NOT routed through
    `plugin_cli.available` (that raises for pi; see `plugin_cli.binary_name`'s
    docstring). That means the many per-test `monkeypatch.setattr(plugin_cli,
    "available", ...)` calls that hold claude/codex detection steady do NOT
    also hold pi steady: a developer running this suite with the real pi
    coding agent on PATH (this repo is building pi support, so this is not a
    hypothetical machine) would get a third source leaking into every
    agent-picker and confirm-screen test written against exactly two, green
    in CI and red on that laptop for a reason nothing in the failure output
    would explain -- the same class of bug `_no_ambient_agent` above exists
    to prevent. Tests that want pi detected override this themselves.

    BOTH BINDINGS, because there are two callers and they do not share one.
    `setup.pi_binary_available` is a re-export of `pi_config`'s function, and
    `backfill.which_agent(Agent.PI)` calls `pi_config.pi_binary_available()`
    directly -- so patching only the `setup` name left the digest resolver
    answering from the developer's real PATH, and `resolve_digest_agent` would
    pick pi on this machine and nothing on CI.

    Patching the ATTRIBUTE rather than clearing the cache is deliberate: the
    real function is `lru_cache`d (once per process, see its docstring), so a
    cleared cache still calls the real sniff. Replacing the name means the
    cache is never consulted at all, and monkeypatch puts the original --
    cache and all -- back afterwards. `test_setup_wizard`'s real-sniff tests
    capture the true function at import time and clear its cache themselves,
    so they are unaffected either way.
    """
    from probe.cli import pi_config
    from probe.cli import setup as wizard

    monkeypatch.setattr(wizard, "pi_binary_available", lambda: False)
    monkeypatch.setattr(pi_config, "pi_binary_available", lambda: False)


@pytest.fixture(autouse=True)
def _no_ambient_marketplace_agent(monkeypatch: pytest.MonkeyPatch) -> None:
    """Pin claude/codex detection OFF for the whole suite -- the other half of
    `_no_ambient_pi_binary` above.

    `plugin_cli.available` is a real `shutil.which`, so it answers from the
    DEVELOPER'S PATH. That was harmless while a headless run hard-coded its
    agent selection to `("claude_code",)` and never consulted detection; it
    stopped being harmless when that default became "every agent found on this
    machine", because detection is now what a headless run RESOLVES TO. A
    laptop with the real claude and codex binaries installed -- which anyone
    working on this repo has -- would configure two agents where CI, having
    neither, configures the one-agent fallback. Green in CI, red on the
    laptop, exactly the failure mode the two fixtures above exist to prevent.

    OFF rather than a fixed pair, so the fallback path is what the suite gets
    by default and every existing expectation is unchanged. The many tests
    that stub `plugin_cli.available` per-test still win: monkeypatch inside a
    test runs after this fixture. Tests that want detection to find something
    say so themselves.
    """
    from probe.cli import plugin_cli

    monkeypatch.setattr(plugin_cli, "available", lambda source: False)


@pytest.fixture(autouse=True)
def _no_ambient_agent(monkeypatch: pytest.MonkeyPatch) -> None:
    """Pin agent detection OFF for the whole suite.

    `_telemetry_core.detect_agent_label()` reads `os.environ`, and both `build_batch`
    and `TelemetryContext.emit` call it with no argument. Without this scrub, an exact
    assertion on an event's properties depends on whether the developer happens to be
    running the suite from inside Claude Code, Cursor or Codex -- green in CI, red on a
    laptop, for reasons nothing in the failure output would explain. Tests that WANT an
    agent set the marker themselves.
    """
    # DERIVED from `AGENTS`, not hand-listed. The hand-list had gone stale by one
    # agent (`PI_CODING_AGENT`), which was harmless while this only steered
    # telemetry labels -- and stopped being harmless at 0170, when
    # `name_customized` in the fake app started depending on agent detection:
    # the suite was green in CI and red on any box running it under pi, which is
    # exactly what `_no_ambient_pi_binary` below exists to prevent.
    from probe.sdk.agent_session import AGENTS

    from probe.sdk.agent_session import FORWARDED_SESSION_ENV

    markers = {"PROBE_AGENT", "CLAUDE_CODE_SESSION_ID", FORWARDED_SESSION_ENV}
    markers.update(var for spec in AGENTS for var in spec.detect_env)
    markers.update(spec.session_env for spec in AGENTS if spec.session_env)
    for marker in sorted(markers):
        monkeypatch.delenv(marker, raising=False)


@pytest.fixture(autouse=True)
def _no_real_capture_daemon_kill(
    monkeypatch: pytest.MonkeyPatch, tmp_path_factory: pytest.TempPathFactory
) -> None:
    """No test may SIGTERM the machine's real transcript uploaders.

    `capture.turn_off()` stops them through `_stop_daemon()`, which globs
    `/tmp/probe-research-tap-watcher-*.pid` -- one file per LIVE session on the
    machine, not the test's. `test_setup_wizard.py` called it unpatched and
    killed every session's capture on a shared dev box seven times in one
    morning, journalling each kill into its own tmp state dir so the real
    `stop-daemon.jsonl` showed nothing (2026-09-28). An env var, not a
    monkeypatch, so a CLI driven in a subprocess is covered too.
    """
    monkeypatch.setenv("PROBE_TEST_TAP_PID_DIR", str(tmp_path_factory.mktemp("tap-pids")))


@pytest.fixture(autouse=True)
def _no_real_device_state(monkeypatch: pytest.MonkeyPatch) -> None:
    """The setup wizard sends ONE server call as it launches
    (`POST /v1/device-state`, `capabilities.fetch_device_state`). Most wizard
    tests run against the DEFAULT endpoint, so the real call would reach
    production. Replaced here -- the fetch itself, so any caller is covered --
    by an older server's answer (the route is missing), which makes
    `doctor.collect()` ask the old way: exactly what every existing wizard test
    already stubs. `test_device_state.py` drives the real call against a
    served fake."""
    from probe.cli import capabilities

    monkeypatch.setattr(
        capabilities,
        "fetch_device_state",
        lambda *_a, **_k: capabilities.DeviceState(capabilities.DeviceStateOutcome.UNSUPPORTED),
    )


@pytest.fixture(autouse=True)
def _no_real_wizard_account_lookup(monkeypatch: pytest.MonkeyPatch) -> None:
    """The setup wizard records its new login's account with one `/v1/me`
    (#2041 round 3). Most wizard tests mint against the DEFAULT endpoint with a
    fake token, so the real lookup would reach production. Replaced by a no-op
    here; `test_outbox_credential_stamp.py` calls the real one against a
    served fake."""
    from probe.cli import setup

    monkeypatch.setattr(setup, "_record_login_account", lambda *a, **k: None, raising=False)


@pytest.fixture(autouse=True)
def _no_real_mcp_accounting(monkeypatch: pytest.MonkeyPatch) -> None:
    """No test may reach real PostHog through the hosted MCP's accounting sender.

    Same reason as `_telemetry_off` above, for the sender that fixture cannot see:
    `mcp.accounting` owns its own `_Sender` (it cannot import `cli/`, which the MCP
    deploy filter excludes). The emitter is gated on the killswitch too, so this is
    belt AND braces -- a future test that legitimately turns telemetry on still must
    not post from CI. Tests that assert on emissions replace `_ensure_sender`
    themselves; this only guarantees the floor.
    """
    from probe.mcp import accounting

    def _explode(_batch: list) -> None:
        raise AssertionError("mcp accounting attempted a real PostHog post")

    sender = accounting._Sender()
    sender.transport = _explode
    monkeypatch.setattr(accounting, "_ensure_sender", lambda: sender)


@pytest.fixture(autouse=True)
def _reset_diagnostics_state() -> None:
    """Diagnostics keeps PROCESS-global state (the transport ring buffer, the
    active breadcrumb, the throttle clock, the sticky first incident).

    Suite-wide, not module-local: test_fluent.py arms breadcrumbs through
    probe.init() and reset none of it, so a stale _ACTIVE_BREADCRUMB pointing at
    a deleted tmp_path leaked into every test that ran after it.
    """
    from probe.sdk import diagnostics

    def clear() -> None:
        diagnostics._TRANSPORT_LOG.clear()
        diagnostics._ACTIVE_BREADCRUMB = None
        diagnostics._INFLIGHT = None
        diagnostics._FIRST_INCIDENT = None
        diagnostics._LAST_REFRESH = 0.0

    clear()
    yield
    clear()


@pytest.fixture(autouse=True)
def _hw_collector_off(monkeypatch: pytest.MonkeyPatch) -> None:
    """Pin the hardware collector OFF regardless of the developer's shell.

    The collector is ON by default for users as of 2026-09-21, which makes
    this fixture load-bearing rather than merely defensive: without it every
    run() in the legacy suite would start a collector and its inventory
    publication (real psutil/NVML probes, extra fake-API calls and queued ops
    that break exact-sequence assertions). The hw tests set their own value explicitly via an autouse
    fixture that runs after this one."""
    monkeypatch.setenv("PROBE_HW", "0")


@pytest.fixture(autouse=True)
def _read_capture_off(monkeypatch: pytest.MonkeyPatch) -> None:
    """Pin the read recorder (lineage) OFF regardless of the developer's shell.

    It is ON by default for `probe.init()`, which would make every legacy test
    that opens a run record pytest's own file reads and, at finish, ask the fake
    backend for `/v1/server/features` -- extra calls that break exact-sequence
    assertions. `test_sdk_inputs.py` turns it on where it is the subject.

    A test that turned it on and bound spawned workers to a run it never
    closed (lineage plan 3, F5) must not leave that binding in `os.environ`
    for the next test: it is undone here."""
    monkeypatch.setenv("PROBE_CAPTURE_READS", "0")
    # Run handles an earlier test left open (never finished) must not count
    # as open runs here: they would keep every worker binding off.
    open_runs = sys.modules.get("probe.sdk._open_runs")
    if open_runs is not None:
        open_runs.clear()
    yield
    recorder = sys.modules.get("probe.sdk.inputs")
    if recorder is not None and getattr(recorder, "_bound", None) is not None:
        recorder._unbind()
    if recorder is not None and os.environ.get(recorder.OWNER_PID_ENV) == str(os.getpid()):
        # A binding this process made and a test dropped without unbinding.
        for name in (recorder.OWNER_PID_ENV, recorder.BIND_ENV, recorder.CHILD_DIR_ENV):
            os.environ.pop(name, None)
    if recorder is not None:
        recorder._follow = None


@pytest.fixture(autouse=True)
def _no_waiting_for_a_connection_that_is_not_there(monkeypatch: pytest.MonkeyPatch) -> None:
    """Do not wait out a dropped connection in a suite that has none.

    A foreground import retries its drain with backoff when the drain parks
    work for a transient reason. Every fake backend here is an unroutable host,
    so every drain in the suite IS a genuine transient failure, and each flush
    would spend the full two-minute wait before giving up. Tests that cover the
    waiting set this back themselves.
    """
    monkeypatch.setenv("PROBE_FLUSH_ATTEMPTS", "1")


@pytest.fixture(autouse=True)
def _no_live_token_verification(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep the hosted MCP's edge token check off by default.

    It calls the real ``/v1/me``, so any test handing a bearer to the wrapper would
    quietly hit production and fail on a 401. Tests that cover verification inject
    their own ``token_rejected`` instead (see tests/test_mcp_hosted.py).
    """
    monkeypatch.setenv("PROBE_MCP_VERIFY_TOKEN", "0")


@pytest.fixture(autouse=True)
def _isolate_config_home(monkeypatch: pytest.MonkeyPatch, tmp_path_factory) -> None:
    """Point every test's config at a throwaway dir — no exceptions.

    ``config_path()`` resolves ``$XDG_CONFIG_HOME/probe/config.json`` and falls back to
    ``~/.config``. Only a handful of tests used to pin the env var, so any *other* test
    that reached config — directly or through ``resolve()`` — read the developer's real
    credential file. That was survivable while the config was read-mostly. It stops being
    survivable once ``load_file()`` migrates shapes: a bug in that path would rewrite a
    real ``~/.config/probe/config.json``, and the tokens in it are not recoverable.

    Autouse and unconditional, so isolation is the default rather than something each new
    test has to remember. Tests that need their own config dir still set the var
    themselves; setting it again inside the test simply wins over this one.

    HOME is redirected too, and the post-condition is asserted on the way out: the env
    var is only half the resolution (``config_path()`` falls back to ``Path.home()``),
    so a test that does ``monkeypatch.delenv("XDG_CONFIG_HOME")`` — a pattern that
    already exists in this repo — would silently re-point every write at the real
    credential file. The assert turns that into a failed test instead.

    The check is "did it escape to the REAL home", not "is it under my tmp dir":
    plenty of tests legitimately point at a tmp dir of their own choosing, and only
    reaching the developer's actual credentials is the failure worth catching.
    """
    real_home = Path.home().resolve()
    # The suite's own temp root is allowed wherever it lives: on Windows it is
    # %TEMP%, which sits inside the user profile.
    base_temp = tmp_path_factory.getbasetemp().resolve()
    root = tmp_path_factory.mktemp("xdg-config")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(root))
    monkeypatch.setenv("HOME", str(root))
    monkeypatch.setenv("USERPROFILE", str(root))  # Windows' Path.home() reads this, not HOME
    # CODEX_HOME is the same hole one directory over, and it now has a WRITER
    # behind it: the wizard registers the Codex MCP by editing
    # `$CODEX_HOME/config.toml`. Redirecting HOME alone leaves a developer who
    # exports CODEX_HOME pointing every test at their real Codex config, where
    # a bad write does not just lose a token — Codex refuses to start.
    monkeypatch.delenv("CODEX_HOME", raising=False)
    # CLAUDE_CONFIG_DIR, likewise: the wizard writes `showThinkingSummaries` and
    # the status line into `$CLAUDE_CONFIG_DIR/settings.json`, so a developer
    # who exports it would otherwise have tests editing their real Claude Code.
    monkeypatch.delenv("CLAUDE_CONFIG_DIR", raising=False)
    # PI_CODING_AGENT_DIR, likewise: an update test reaching the pi step would
    # run a real `pi update` against a developer's own pi install.
    monkeypatch.delenv("PI_CODING_AGENT_DIR", raising=False)
    # KIMI_CODE_HOME, likewise: the daemon's shell lets the agent's instruction
    # file there be read, and the Kimi adapter lists it.
    monkeypatch.delenv("KIMI_CODE_HOME", raising=False)
    # XDG_STATE_HOME is the telemetry flavor of the same hole: machine_id and
    # the identity cache live under it, and the plugin's build_batch now mints
    # a machine id on every call — a developer exporting XDG_STATE_HOME would
    # otherwise get real state written by every batch test.
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)
    # `.probeignore` (plan (n)) is read from these too: a developer exporting
    # them (or a `probe exec` the suite runs under) would change what every
    # capture test captures.
    monkeypatch.delenv("PROBE_IGNORE", raising=False)
    monkeypatch.delenv("PROBE_IGNORE_FILE", raising=False)
    monkeypatch.delenv("PROBE_IGNORE_EXPORTED", raising=False)
    # CODEX_THREAD_ID / CODEX_SANDBOX are the same hole again, and this pair
    # changes BEHAVIOUR rather than paths: `probe wizard` reads them to decide
    # that it is running inside a Codex session and preselects Codex ALONE
    # instead of every agent on the machine. A suite run from inside Codex --
    # which this repo ships an integration for, so it is a normal way to work --
    # then renders a different first screen, and any test that drives the agent
    # picker by keystroke is answering a question it was not shown. Measured:
    # `CODEX_THREAD_ID=abc pytest -k empty_agent_step` fails on an untouched
    # tree, and the failure blames the wizard rather than the shell.
    monkeypatch.delenv("CODEX_THREAD_ID", raising=False)
    monkeypatch.delenv("CODEX_SANDBOX", raising=False)
    yield
    from probe.cli.codex_config import config_path as codex_config_path
    from probe.sdk.config import config_path

    def _in_real_home(path: Path) -> bool:
        parents = path.resolve().parents
        return real_home in parents and base_temp not in parents

    assert not _in_real_home(config_path()), (
        f"config isolation was defeated: {config_path()} is inside the real home"
    )
    assert not _in_real_home(codex_config_path()), (
        f"Codex config isolation was defeated: {codex_config_path()} is inside the real home"
    )
    # The wizard writes Claude Code's settings (status line, thinking summaries).
    # Its default home must be the redirected one; a test that points
    # CLAUDE_CONFIG_DIR somewhere chose that place itself.
    if not os.environ.get("CLAUDE_CONFIG_DIR"):
        from probe.cli import statusline

        claude_settings = statusline.settings_path()
        assert not _in_real_home(claude_settings), (
            f"Claude settings isolation was defeated: {claude_settings} is inside the real home"
        )


# A shim dir holding loud no-op `claude`/`codex` stubs, built once. It is prepended to
# PATH for every test (see `_no_real_agent_cli`) so an accidental real-agent spawn fails
# fast with exit 97 instead of authenticating -- which, under the isolated HOME above,
# means reaching for a login keychain that isn't there and storming SecurityAgent. A
# `claude -p` that escaped this once wedged the keychain hard enough to force a reboot.
# `git` and every other binary are left untouched.
_NO_AGENT_BIN = tempfile.mkdtemp(prefix="probe-tests-no-agent-")
for _name in ("claude", "codex"):
    _stub = Path(_NO_AGENT_BIN) / _name
    _stub.write_text(
        "#!/bin/sh\n"
        f'echo "tests must not run the real {_name} CLI (it reads the macOS '
        'keychain); mock the spawn instead" >&2\n'
        "exit 97\n"
    )
    _stub.chmod(0o755)


@pytest.fixture(autouse=True)
def _no_real_agent_cli(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make a real coding-agent CLI spawn fail loudly instead of touching the keychain.

    Autouse and unconditional, alongside ``_isolate_config_home``: together they are the
    invariant that a test can neither read the developer's real credentials nor prompt
    for the keychain. See ``_NO_AGENT_BIN`` for the why.
    """
    monkeypatch.setenv("PATH", f"{_NO_AGENT_BIN}{os.pathsep}{os.environ['PATH']}")


_RUN_METRICS = re.compile(r"^/v1/runs/([^/]+)/metrics$")
_RUN_METRICS_GROUPED = re.compile(r"^/v1/runs/([^/]+)/metrics/grouped$")
_RUN_METRICS_WIDE = re.compile(r"^/v1/runs/([^/]+)/metrics/wide$")
_RUN_METRICS_EXPORT = re.compile(r"^/v1/runs/([^/]+)/metrics/export$")
_RUN_VIEWS = re.compile(r"^/v1/runs/([^/]+)/views$")
_RUN_VIEWS_PREVIEW = re.compile(r"^/v1/runs/([^/]+)/views/preview$")
_RUN_VIEW_DATA = re.compile(r"^/v1/runs/([^/]+)/views/([^/]+)/data$")
_VIEW = re.compile(r"^/v1/views/([^/]+)$")


def _instant(stamp: str):
    """An ISO timestamp as an aware datetime, so `Z` and `+00:00` compare equal
    -- the server compares the parsed instant, never the spelling."""
    from datetime import datetime

    return datetime.fromisoformat(stamp.replace("Z", "+00:00"))


_RUN_COORDINATES = re.compile(r"^/v1/runs/([^/]+)/coordinates$")
_RUN_SPANS = re.compile(r"^/v1/runs/([^/]+)/spans$")
_RUN_STEPS = re.compile(r"^/v1/runs/([^/]+)/steps$")
_RUN_SERIES = re.compile(r"^/v1/runs/([^/]+)/series$")
_RUN_ARTIFACTS = re.compile(r"^/v1/runs/([^/]+)/artifacts$")
_RUN_REOPEN = re.compile(r"^/v1/runs/([^/]+)/reopen$")
_RUN_BUNDLE = re.compile(r"^/v1/runs/([^/]+)/bundle$")
_RUN_REPRODUCE = re.compile(r"^/v1/runs/([^/]+)/reproduce$")
_RUN_CODE_COMPARE = re.compile(r"^/v1/runs/([^/]+)/code/compare$")
_RUN_CODE = re.compile(r"^/v1/runs/([^/]+)/code$")
_EXPERIMENT_CODE = re.compile(r"^/v1/experiments/([^/]+)/code$")
_RUN_LINEAGE = re.compile(r"^/v1/runs/([^/]+)/lineage$")
_RUN_TRIALS = re.compile(r"^/v1/runs/([^/]+)/trials$")
_RUN_ITEM = re.compile(r"^/v1/runs/([^/]+)$")
_TRIAL_ITEM = re.compile(r"^/v1/trials/([^/]+)$")
_EXPERIMENT_REPRODUCE = re.compile(r"^/v1/experiments/([^/]+)/reproduce$")
_EXP_RUNS = re.compile(r"^/v1/experiments/([^/]+)/runs$")
_PROJ_RUNS = re.compile(r"^/v1/projects/([^/]+)/runs$")
_EXP_ITEM = re.compile(r"^/v1/experiments/([^/]+)$")
_PROJ_ITEM = re.compile(r"^/v1/projects/([^/]+)$")
_WS_ITEM = re.compile(r"^/v1/workspaces/([^/]+)$")
_WS_FILES = re.compile(r"^/v1/workspaces/([^/]+)/files$")
_WS_FILE_UPLOADS = re.compile(r"^/v1/workspaces/([^/]+)/files/uploads$")
_PROJ_ARTIFACTS = re.compile(r"^/v1/projects/([^/]+)/artifacts$")
_PROJ_PAPERS = re.compile(r"^/v1/projects/([^/]+)/papers$")
_PROJ_ARTIFACT_UPLOADS = re.compile(r"^/v1/projects/([^/]+)/artifacts/uploads$")
_EXP_ARTIFACTS = re.compile(r"^/v1/experiments/([^/]+)/artifacts$")
_EXP_ARTIFACT_UPLOADS = re.compile(r"^/v1/experiments/([^/]+)/artifacts/uploads$")
_SHARED_FILE_ITEM = re.compile(r"^/v1/shared/files/([^/]+)$")
_SHARED_FILE_SUB = re.compile(r"^/v1/shared/files/([^/]+)/(confirm|download|unshare)$")
_WS_FILE_SHARE = re.compile(r"^/v1/workspace-files/([^/]+)/share$")

#: The user_id the fake's /v1/me reports; retained as historical row metadata.
_ME = "00000000-0000-0000-0000-000000000001"
_WS_MINE = "11111111-1111-1111-1111-111111111111"
_WS_OTHER = "22222222-2222-2222-2222-222222222222"
_T0 = "2026-01-01T00:00:00Z"

#: `kind_rank` per catalog kind, as app/notes_catalog/service.py's SQL arms
#: number them: the tiebreak inside one `created_at`, and part of the cursor.
_NOTE_KIND_RANK = {
    "project": 6,
    "experiment": 5,
    "run": 4,
    "sub_note": 3,
    "group": 2,
    "artifact": 1,
}

_ASCII_LOWER = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")

_STAMP_OVERFLOW = re.compile(r"^(.*T\d\d:\d\d:)(\d+)((?:\.\d+)?)(Z|[+-]\d\d:\d\d)?$")


def _keyset_time(value: object) -> float:
    """A row's `created_at` as a sortable instant, the way Postgres compares a
    timestamptz: `Z` and `+00:00` are one zone, and fractions count.

    Also reads the fake's own `_stamp()` past 59 seconds (`...00:00:75Z`), which
    is not ISO but is how this fake has always numbered its 60th row onward."""
    from datetime import datetime, timedelta

    text = str(value or "1970-01-01T00:00:00Z")
    match = _STAMP_OVERFLOW.match(text)
    if match is None:
        return 0.0
    head, seconds, fraction, zone = match.groups()
    zone = "+00:00" if zone in (None, "Z") else zone
    base = datetime.fromisoformat(f"{head}00{zone}")
    return (base + timedelta(seconds=int(seconds) + float(fraction or 0))).timestamp()


def _min_max_downsample(points: list[dict], max_points: int | None) -> list[dict]:
    """app/telemetry/store.py `_downsample`, verbatim in effect: the two
    endpoints plus each bucket's finite min and max, at most `max_points`, in
    order, no duplicates. Copied rather than approximated, because how many
    points a CUT series comes back with is what the MCP reads to decide whether
    a series was sampled."""
    n = len(points)
    if max_points is None or n <= max_points:
        return points
    keep = {0, n - 1}
    buckets = max(0, (max_points - len(keep)) // 2)
    for b in range(buckets):
        lo, hi = b * n // buckets, (b + 1) * n // buckets
        if lo >= hi:
            continue
        window = [i for i in range(lo, hi) if math.isfinite(points[i]["value"])]
        if not window:
            keep.add(lo)
            continue
        keep.add(min(window, key=lambda i: points[i]["value"]))
        keep.add(max(window, key=lambda i: points[i]["value"]))
    return [points[i] for i in sorted(keep)]


def _series_read_provenance(source_backed: bool, max_points: int | None) -> dict:
    """What POST /v1/series/query stamps on a series. A LOCAL series is marked
    sampled whenever the read named `max_points` -- cut or not -- exactly as
    provider_reads.local_read_provenance does; a provider series carries the
    provider's own receipt."""
    if source_backed:
        return {"source": "wandb", "coverage": "sampled", "exactness": "sampled"}
    if max_points is None:
        return {"source": "probe", "coverage": "complete", "exactness": "exact"}
    return {
        "source": "probe",
        "coverage": "sampled",
        "exactness": "sampled",
        "fetched_at": "2026-10-02T00:00:00Z",
        "warning": "Probe downsampled this local series for display",
    }


def _newest_first(rows: list[dict]) -> list[dict]:
    """`order_by="created_at DESC"`, as app/artifacts/{project,experiment}_router.py do."""
    return sorted(rows, key=lambda r: r.get("created_at") or "", reverse=True)




def _chosen_name(name: object | None, slug: str) -> str | None:
    """Mirror of `app/core/naming.py::chosen_name`: `name` NEVER holds the slug.

    A caller that sends the slug as the name has not named anything -- honouring
    it literally would stamp `name_customized` on a machine-generated string and
    freeze the row out of ever being named.
    """
    if name is None or name == slug:
        return None
    return name  # type: ignore[return-value]


def _owns_field(value: object | None, authored_by: object | None) -> bool:
    """Mirror of `app/core/authorship.py::owns_field`, the server's ONLY rule for
    whether a written value locks its field against generation.

    Reimplemented rather than imported: the agent test suite cannot see `app.`.
    That is exactly why `test_authorship_default.py` walks the full truth table
    against this function -- a drifting mirror is how a naming test passes while
    production does the opposite.
    """
    if value is None or value == "":
        return False
    if authored_by is None:
        return True  # the historical inference: something arrived, a person sent it
    return authored_by == "human"


def search_response(
    *,
    state: str = "ok",
    exact: list[dict] | None = None,
    semantic: list[dict] | None = None,
    exact_error: str | None = None,
    semantic_error: str | None = None,
    exact_cursor: str | None = None,
    semantic_cursor: str | None = None,
    semantic_lost_channels: list[str] | None = None,
    semantic_degraded_reason: str | None = None,
    semantic_confidence: dict[str, int] | None = None,
) -> dict:
    """A CONTRACT.md-shaped POST /v1/search response.

    Lives here, not in one suite, because every suite that drives the tool
    surface now needs the fake to ANSWER /v1/search: there is no keyword
    fallback to absorb a 404 any more.
    """
    return {
        "query": "q",
        "state": state,
        "exact": {"results": exact or [], "cursor": exact_cursor, "error": exact_error},
        "semantic": {
            "results": semantic or [],
            "cursor": semantic_cursor,
            "error": semantic_error,
            # Omitted entirely unless a test asks for it, so the default
            # fake stays shaped like a backend that predates the field.
            **({"lost_channels": semantic_lost_channels} if semantic_lost_channels else {}),
            # The engine's verdict on its OWN answer: every channel can be
            # alive and the curation behind the results still be a fallback.
            # Omitted unless asked for, like lost_channels, so the default
            # fake stays shaped like a backend predating the field.
            **(
                {"degraded": True, "degraded_reason": semantic_degraded_reason}
                if semantic_degraded_reason
                else {}
            ),
            **({"confidence_breakdown": semantic_confidence} if semantic_confidence else {}),
        },
    }

class FakeApp:
    # Set False to model a backend PREDATING server-side project scope: it
    # accepts the unknown `project_id` body field, ignores it, and answers
    # tenant-wide. The echo is the only thing distinguishing the two, so the
    # fake has to be able to be both.
    echoes_project_scope = True
    # Set False to model a backend PREDATING research-os 0094: it accepts the
    # unknown `notes` field on a project PATCH, drops it, and still answers 200.
    stores_project_notes = True
    #: Whether this fake understands `notes_append` (research-os 0.117.0.0).
    #: False plays a backend that takes the field, ignores it and answers 200,
    #: which is the failure the client's read-back exists to catch.
    stores_notes_append = True
    #: Character ceiling on a notes document, or None for no ceiling. Set it to
    #: play a document at MAX_DOCUMENT_NOTES: the real server refuses the append
    #: with a 422 naming the cap, and refuses it again on every replay. That
    #: permanence is the point -- a retry queue cannot make a full document
    #: accept anything, so the fail-open write path must not swallow it.
    notes_cap = None
    #: The caps the real server enforces (app/core/limits.py): a DOCUMENT for the
    #: two carriers a reader arrives on, an ANNOTATION for the four that ride on
    #: a row. Mirrored here because the fake now publishes the headroom the client
    #: reads, and a fake that made one number up would let a client ship a warning
    #: that fires at the wrong place.
    document_notes_cap = 100_000
    entity_notes_cap = 4_000
    #: Set False to play a backend PREDATING `notes_remaining_chars` /
    #: `notes_limit_chars`: it answers 200 with neither field. The client must
    #: then warn about NOTHING rather than substitute a cap of its own -- that
    #: substitution is the confident-wrong-answer failure the fields exist to end.
    publishes_notes_headroom = True
    # Set False to model a backend PREDATING research-os 0096: it accepts the
    # unknown `notes` field on run and group create/PATCH, drops it, and still
    # answers 2xx -- so the row comes back with NO `notes` key at all, which is
    # what the SDK's silent-drop warning keys on.
    stores_entity_notes = True
    # Set False to model a backend PREDATING project-direct runs (0054): the
    # /v1/projects/{id}/runs route 404s FastAPI-style, GET /v1/runs ignores the
    # project_id/direct params, and run rows carry NO project_id field — the
    # exact shapes the SDK's old-backend guards key on.
    supports_project_direct = True
    # Set False to model a backend PREDATING run reopen (research-os#364): the
    # /v1/runs/{id}/reopen route 404s FastAPI-style.
    supports_reopen = True
    # 0185: False models a pre-rewind server — /v1/server/features 404s and
    # reopen silently IGNORES rewind_to_step (the exact skew the preflight and
    # echo check exist to catch). supports_rewind_echo=False models the
    # pathological middle: features declares rewind but reopen drops the echo.
    supports_rewind = True
    supports_rewind_echo = True
    # 0255: False models a server that predates run reads -- the feature is not
    # declared, so the SDK keeps the read list on disk instead of sending it.
    supports_run_inputs = True
    # Lineage plan 3 (F2): False models a server that predates run WRITES --
    # `run_outputs` is not declared, so the SDK must not send a write list.
    supports_run_outputs = True
    # 0261: False models a server that predates the trash -- a delete there
    # is permanent, and the CLI must say so instead of promising a restore.
    supports_trash = True
    # Plan (c) (#2017): False models a server without `RunPatch.config_merge`.
    # RunPatch forbids no extra fields, so such a server answers 200 and DROPS
    # the field -- which is why the SDK must not send it there.
    supports_config_merge = True
    # False models a backend PREDATING floating runs (daemon v2): POST /v1/runs
    # is FastAPI's 405 and GET /v1/runs IGNORES `unfiled=true`, answering with
    # filed runs -- the shape the SDK's guard refuses to count as unfiled.
    supports_floating = True
    # 0185 writer fencing, mirrored from app/telemetry/fencing.py: a write
    # CARRYING an epoch older than the run's is refused 409 at the door (an
    # epoch-less write passes). The real server has fenced since 0185, and a
    # fake that accepts every stale write lets a test pass on exactly the data
    # loss the fence produces. False models a pre-0185 server.
    fences_writer_epoch = True
    # SDK reliability 1.1: False models a server that predates `keep_epoch` --
    # the feature is not declared, and reopen IGNORES keep_epoch /
    # expected_write_epoch (undeclared body fields are dropped) and bumps the
    # epoch as it always did. The hazard the client's feature check exists for.
    supports_keep_epoch = True
    # SDK reliability 1.10: False models a server whose PATCH /v1/runs/{id}
    # ignores write_epoch (every server before 1.10).
    fences_status_patch = True
    # 0268: False models a server predating run creation keys -- it IGNORES the
    # body field (pydantic drops it) and does not declare `run_creation_key`, so
    # a re-sent create makes a second run, exactly as the real old server does.
    supports_creation_key = True
    # SDK reliability 2.3: False models a server that predates requeue
    # takeover -- not declared, and reopen drops takeover_stale_after_seconds
    # and refuses a running run exactly as before.
    supports_takeover = True
    # 0269: False models a server predating offline sync (plan 2.12): it does
    # not declare `run_offline_create` and ignores `offline` / `started_at`.
    supports_offline_create = True
    # SDK reliability 2.2: False models a server without
    # POST /v1/runs/{id}/writer-gone (FastAPI's route-level 404).
    supports_writer_gone = True
    # SDK reliability 2.8: per-writer leases (0271). OFF by default: every
    # older test models the run-level heartbeat it was written against; the
    # lease tests (test_run_leases.py) turn it on.
    supports_leases = False

    def _note_activity(self, method: str, path: str) -> None:
        """Two liveness clocks per run, in seconds, that tests advance by hand:
        `run_silence` is the reaper's (telemetry OR a beat resets it) and
        `run_beat_silence` counts beats alone (2.3 judges a beating
        incumbent by its beats)."""
        if method != "POST":
            return
        m = re.match(r"^/v1/runs/([^/]+)/(metrics|spans|steps|heartbeat)$", path)
        if m:
            self.run_silence[m.group(1)] = 0.0
            if m.group(2) == "heartbeat":
                self.run_beat_silence[m.group(1)] = 0.0

    def _fence_stale_writer(
        self, method: str, path: str, body: dict | None, request: httpx.Request
    ) -> httpx.Response | None:
        """The fence, in the shapes the real routes answer with.

        /metrics, /spans and /steps raise a PLAIN 409 (`HTTPException(409,
        str(exc))`), and so does a status PATCH (1.10) -- deliberately without
        `existing_id`, which the drain would count as delivered on a retry.
        /heartbeat answers `conflict(..., existing_id=run_id)`.
        """
        if not self.fences_writer_epoch:
            return None
        rid: str | None = None
        carried = None
        plain = True
        if method == "POST":
            for pattern in (_RUN_METRICS, _RUN_SPANS, _RUN_STEPS):
                m = pattern.match(path)
                if m:
                    rid, carried = m.group(1), (body or {}).get("write_epoch")
                    break
            else:
                m = re.match(r"^/v1/runs/([^/]+)/heartbeat$", path)
                if m:
                    rid, plain = m.group(1), False
                    raw = request.url.params.get("write_epoch")
                    carried = int(raw) if raw else None
        elif method == "PATCH" and self.fences_status_patch:
            m = _RUN_ITEM.match(path)
            if m and (body or {}).get("status") is not None:
                rid, carried = m.group(1), body.get("write_epoch")
        if rid is None or carried is None:
            return None
        row = self.runs.get(rid)
        if row is None:
            return None
        current = int(row.get("write_epoch", 1))
        if int(carried) >= current:
            return None
        self.fenced_writes.append(
            {"method": method, "path": path, "carried": int(carried), "current": current}
        )
        message = (
            f"write carries epoch {carried} but run {rid} is on epoch {current}: "
            "this writer was superseded by a reopen. Stop logging from this "
            "process, or reopen the run to obtain the current epoch."
        )
        if plain:
            return httpx.Response(409, json={"detail": message})
        return httpx.Response(409, json={"detail": {"message": message, "existing_id": rid}})
    # 0270 (plan item (h)): True models a server that takes a live run's
    # console log (`run_log_stream`). Off by default -- today's released
    # server -- so a test that opens a teed run sees no extra requests.
    supports_run_log_stream = False
    # 0273 (plan item (g)): True models a server that takes artifacts over
    # 64 MiB in parts (`artifact_multipart`, `/v1/runs/{ref}/artifacts/multipart`).
    # Off by default -- a released server before (g) -- so an existing test
    # logging a big file keeps seeing 0.7's warning and reference row.
    supports_artifact_multipart = False
    #: The layout's part floor (the real server's is 64 MiB; a test may lower it).
    multipart_min_part = 64 * 1024 * 1024
    #: GET polls answered `verifying` before the fake's verifier settles.
    multipart_verify_polls = 0

    def _multipart(self, method: str, path: str, body: dict) -> httpx.Response:
        """0273's doors, faithfully enough to drive the SDK: the server-side
        layout, part URLs, the listing a resume reads, a size-checked
        complete, and a verifier that settles after `multipart_verify_polls`
        GETs -- `verified` when the assembled parts hash to the declared
        sha256, else `failed` (sha256_mismatch)."""
        if not self.supports_artifact_multipart:
            return httpx.Response(404, json={"detail": "Not Found"})
        m = re.fullmatch(r"/v1/runs/([^/]+)/artifacts/multipart(?:/([^/]+)(/parts|/complete)?)?", path)
        if m is None:
            return httpx.Response(404, json={"detail": "Not Found"})
        rid, uid, tail = m.group(1), m.group(2), m.group(3)
        if uid is None and method == "POST":
            ch, size = body["content_hash"], int(body["size_bytes"])
            if size <= 64 * 1024 * 1024 and self.multipart_min_part >= 64 * 1024 * 1024:
                return httpx.Response(422, json={"detail": "use the single-PUT door"})
            for up in self.multipart.values():
                if up["content_hash"] == ch and up["state"] in ("uploading", "verifying"):
                    if up["run_id"] == rid and up["name"] == body["name"]:
                        return httpx.Response(201, json=self._multipart_out(up))
                    return httpx.Response(
                        409, json={"detail": {"message": "in progress", "state": up["state"]}}
                    )
            aid = str(uuid.uuid4())
            art = {
                "id": aid,
                "run_id": rid,
                "name": body["name"],
                "content_hash": ch,
                "size_bytes": size,
                "kind": (body.get("kind") or "file").strip().lower(),
                "meta": body.get("meta"),
                "step_index": body.get("step_index"),
                "span_id": body.get("span_id"),
                "status": "complete" if ch in self.uploaded else "pending",
                "is_reference": False,
            }
            self.artifacts.setdefault(rid, []).append(art)
            if ch in self.uploaded:
                return httpx.Response(201, json={"artifact_id": aid, "have": True})
            part_size = max(self.multipart_min_part, -(-size // 10_000))
            up = {
                "upload_id": str(uuid.uuid4()),
                "artifact_id": aid,
                "run_id": rid,
                "name": body["name"],
                "content_hash": ch,
                "size_bytes": size,
                "part_size": part_size,
                "part_count": -(-size // part_size),
                "state": "uploading",
                "failure_reason": None,
                "parts": {},
                "polls": 0,
                "body": dict(body),
            }
            self.multipart[up["upload_id"]] = up
            return httpx.Response(201, json=self._multipart_out(up))
        up = self.multipart.get(uid or "")
        if up is None or up["run_id"] != rid:
            return httpx.Response(404, json={"detail": "multipart upload not found"})
        conflict = {"message": "not uploading", "state": up["state"], "failure_reason": up["failure_reason"]}
        if tail == "/parts" and method == "POST":
            if up["state"] != "uploading":
                return httpx.Response(409, json={"detail": conflict})
            parts = [
                {
                    "part_number": n,
                    "url": f"http://r2.test/part/{uid}/{n}",
                    "size": self._multipart_part_size(up, n),
                }
                for n in sorted(set(body["part_numbers"]))
            ]
            return httpx.Response(200, json={"upload_id": uid, "expires_in": 3600, "parts": parts})
        if tail is None and method == "GET":
            if up["state"] == "verifying":
                up["polls"] += 1
                if up["polls"] > self.multipart_verify_polls:
                    self._multipart_settle(up)
            return httpx.Response(200, json=self._multipart_status(up))
        if tail == "/complete" and method == "POST":
            if up["state"] in ("verifying", "verified"):
                return httpx.Response(200, json=self._multipart_status(up))
            if up["state"] != "uploading":
                return httpx.Response(409, json={"detail": conflict})
            status = self._multipart_status(up)
            if status["missing_parts"] or status["wrong_size_parts"]:
                return httpx.Response(
                    409,
                    json={"detail": {**conflict, "missing_parts": status["missing_parts"],
                                     "wrong_size_parts": status["wrong_size_parts"]}},
                )
            up["state"] = "verifying"
            return httpx.Response(200, json=self._multipart_status(up))
        if tail is None and method == "DELETE":
            if up["state"] == "verified":
                return httpx.Response(409, json={"detail": conflict})
            if up["state"] in ("uploading", "verifying"):
                up["state"], up["failure_reason"] = "aborted", "aborted_by_client"
                up["parts"].clear()
            return httpx.Response(204)
        return httpx.Response(405, json={"detail": "Method Not Allowed"})

    def _multipart_part_size(self, up: dict, n: int) -> int:
        if n < up["part_count"]:
            return up["part_size"]
        return up["size_bytes"] - up["part_size"] * (up["part_count"] - 1)

    def _multipart_out(self, up: dict) -> dict:
        return {
            "artifact_id": up["artifact_id"],
            "have": False,
            "upload_id": up["upload_id"],
            "state": up["state"],
            "size_bytes": up["size_bytes"],
            "part_size": up["part_size"],
            "part_count": up["part_count"],
            "part_url_batch": 100,
        }

    def _multipart_status(self, up: dict) -> dict:
        missing, wrong = [], []
        if up["state"] == "uploading":
            for n in range(1, up["part_count"] + 1):
                got = up["parts"].get(n)
                if got is None:
                    missing.append(n)
                elif len(got) != self._multipart_part_size(up, n):
                    wrong.append(n)
        return {
            **self._multipart_out(up),
            "run_id": up["run_id"],
            "name": up["name"],
            "content_hash": up["content_hash"],
            "parts": [
                {"part_number": n, "size": len(b), "etag": f'"{n}"'}
                for n, b in sorted(up["parts"].items())
            ] if up["state"] == "uploading" else [],
            "missing_parts": missing,
            "wrong_size_parts": wrong,
            "failure_reason": up["failure_reason"],
        }

    def _multipart_settle(self, up: dict) -> None:
        digest = hashlib.sha256()
        for n in range(1, up["part_count"] + 1):
            digest.update(up["parts"][n])
        art = next(
            (a for a in self.artifacts.get(up["run_id"], []) if a["id"] == up["artifact_id"]), None
        )
        if digest.hexdigest() == up["content_hash"]:
            up["state"] = "verified"
            self.uploaded.add(up["content_hash"])
            if art is not None:
                art["status"] = "complete"
        else:
            up["state"], up["failure_reason"] = "failed", "sha256_mismatch"
            if art is not None:
                art["status"] = "failed"
        up["parts"].clear()  # the bytes are "in the store" now; free the test's memory

    def _multipart_put(self, path: str, request: httpx.Request) -> httpx.Response:
        _, _, uid, number = path.split("/", 3)
        n = int(number)
        up = self.multipart.get(uid)
        if up is None or up["state"] != "uploading":
            return httpx.Response(404, text="NoSuchUpload")
        if n in self.multipart_fail_parts:
            self.multipart_fail_parts.discard(n)
            return httpx.Response(503, text="SlowDown")
        if self.multipart_refuse_part_puts:
            if self.multipart_refuse_part_puts > 0:
                self.multipart_refuse_part_puts -= 1
            return httpx.Response(403, text="<Error><Code>AccessDenied</Code></Error>")
        up["parts"][n] = request.content or b""
        self.multipart_part_puts.append((uid, n))
        return httpx.Response(200, headers={"etag": f'"{n}"'})

    def _echo_scope(self, response: dict, body: dict | None) -> dict:
        if not self.echoes_project_scope or not body or not body.get("project_id"):
            return response
        return {**response, "project_id": body["project_id"]}

    def _view_envelope(self, spec: dict, *, view_id: str | None, name: str | None = None) -> dict:
        """The shape both `view_data` and `preview_view` return.

        Two stepped points and every disclosure field, always populated —
        `missing_inputs` and `dropped_nonfinite` are how a client learns a curve
        is incomplete, so a fake that omitted them would let a caller that
        ignores them pass.
        """
        return {
            "view_id": view_id,
            "name": name,
            "x_axis": "step",
            "points": [
                {"step_index": 0, "wall_clock": "2026-08-03T00:00:00Z", "value": 1.5},
                {"step_index": 1, "wall_clock": "2026-08-03T00:01:00Z", "value": 1.25},
            ],
            "truncated": False,
            "missing_inputs": [],
            "dropped_nonfinite": 0,
            "echo_spec": spec,
        }

    def _stepped_points(self, rid: str, params, *, keys: list[str] | None = None) -> list[dict]:
        """The stepped points a grouped/wide read draws from: key/kind/step-window
        filtered, wall-clock-only points (no step_index) excluded."""
        rows = [r for r in self.metric_points.get(rid, []) if r.get("step_index") is not None]
        if keys:
            rows = [r for r in rows if r.get("key") in keys]
        if params.get("kind") is not None:
            rows = [r for r in rows if r.get("kind") == params["kind"]]
        if params.get("step_from") is not None:
            rows = [r for r in rows if r["step_index"] >= int(params["step_from"])]
        if params.get("step_to") is not None:
            rows = [r for r in rows if r["step_index"] <= int(params["step_to"])]
        return rows

    #: `runs.parent_relation` -> the genealogy relation a parent origin names.
    _PARENT_RELATIONS = {
        "fork": "forked_from", "resume": "resumed_from", "retry": "retried_from", "branch": "branched_from",
    }

    def _run_origin(self, run: dict) -> dict:
        """Mirrors app/lineage/origin.py for what the fake stores: the first
        parent, else the group, else the experiment, else the project, else the
        unfiled bucket."""
        if run.get("parent_run_id"):
            return {"type": "run", "id": run["parent_run_id"], "via": "lineage",
                    "relation": self._PARENT_RELATIONS.get(run.get("parent_relation") or "")}
        for key, kind in (("group_id", "group"), ("experiment_id", "experiment"), ("project_id", "project")):
            if run.get(key):
                return {"type": kind, "id": run[key], "via": "container", "relation": None}
        return {"type": "unfiled", "id": None, "via": "container", "relation": None}

    def _project_origin(self, pid: str) -> dict | None:
        """A project end it builds on or replaces (a stored link), else its
        parent project, else None: a root."""
        for edge in self.edges:
            if (edge.get("source_type"), edge.get("source_id")) == ("project", pid) and edge.get(
                "target_type"
            ) == "project" and edge.get("relation") in ("derived_from", "supersedes"):
                target = edge["target_id"]
                kind = "experiment" if target in self.experiments else "project"
                return {"type": kind, "id": target, "via": "lineage", "relation": edge["relation"]}
        row = self.experiments.get(pid) or self.projects.get(pid) or {}
        parent = row.get("project_id") if pid in self.experiments else row.get("parent_project_id")
        return {"type": "project", "id": parent, "via": "container", "relation": None} if parent else None

    def _project_lineage(self, pid: str, limit: int) -> "httpx.Response":
        """`GET /v1/projects/{id}/lineage` (0278): its own links (stored only --
        the fake keeps no reads, so nothing is derived), its origin, and its
        direct children with theirs, in the server's order."""
        if pid not in self.projects and pid not in self.experiments:
            return httpx.Response(404, json={"detail": "project not found"})
        nodes: list[dict] = []
        for row in self.projects.values():
            if row.get("parent_project_id") == pid:
                nodes.append({"type": "project", "id": row["id"], "name": row.get("name"),
                              "origin": self._project_origin(row["id"])})
        for row in self.experiments.values():
            if row.get("project_id") == pid:
                nodes.append({"type": "experiment", "id": row["id"], "name": row.get("name"),
                              "origin": self._project_origin(row["id"])})
        for row in self.groups.values():
            if row.get("experiment_id") == pid:
                nodes.append({"type": "group", "id": row["id"], "name": row.get("name"),
                              "origin": {"type": "experiment", "id": pid, "via": "container", "relation": None}})
        for row in self.runs.values():
            filed_here = row.get("experiment_id") == pid or (
                row.get("project_id") == pid and not row.get("experiment_id")
            )
            if filed_here:
                nodes.append({"type": "run", "id": row["id"], "name": row.get("name"),
                              "origin": self._run_origin(row)})
        edges = [
            e for e in self.edges
            if ("project", pid) in ((e.get("source_type"), e.get("source_id")),
                                    (e.get("target_type"), e.get("target_id")))
        ]
        return httpx.Response(200, json={
            "project_id": pid,
            "kind": "experiment" if pid in self.experiments else self.projects[pid].get("kind"),
            "origin": self._project_origin(pid),
            "edges": list(reversed(edges)),
            "edges_truncated": False,
            "derived_truncated": False,
            "nodes": nodes[:limit],
            "truncated": len(nodes) > limit,
        })

    def _find_artifact(self, artifact_id: str) -> dict | None:
        """One artifact by id, whatever it hangs off — the fake's echo of the server's
        single anchor-aware confirm/delete core."""
        for rows in self.artifacts.values():
            for row in rows:
                if row.get("id") == artifact_id:
                    return row
        return None

    def _move_artifact(self, artifact_id: str, body: dict) -> "httpx.Response":
        """``POST /v1/artifacts/{id}/move`` — the anchor-move rail.

        Performs a REAL re-anchor (200, the row, id unchanged) so a test can
        assert the artifact actually landed somewhere else rather than that a
        request was merely shaped correctly.

        The refusals are injected through ``artifact_move_error`` instead of being
        reimplemented. Which moves are legal is the engine's rule and it is
        currently MOVING (lateral project->project is landing), so a fake that
        encoded today's answer would fail the CLI for tomorrow's, and a fake that
        guessed would certify the guess. What the CLI owes on that path is only to
        relay the server's own words, and that is what these tests check.
        """
        if self.artifact_move_error is not None:
            status, detail = self.artifact_move_error
            return httpx.Response(status, json={"detail": detail})
        row = self._find_artifact(artifact_id)
        if row is None:
            return httpx.Response(404, json={"detail": "artifact not found"})
        level = (body or {}).get("level")
        if level not in ("run", "experiment", "project"):
            return httpx.Response(422, json={"detail": f"unknown level {level!r}"})
        target_id = (body or {}).get("target_id")
        if target_id is None:
            # A promote derives its destination from the artifact's own chain.
            target_id = row.get(f"{level}_id")
            if target_id is None:
                return httpx.Response(
                    422,
                    json={"detail": f"no {level} on this artifact's chain to promote to"},
                )
        for rows in self.artifacts.values():
            if row in rows:
                rows.remove(row)
        for other in ("run", "experiment", "project"):
            row.pop(f"{other}_id", None)
        row[f"{level}_id"] = target_id
        self.moves.append({"artifact_id": artifact_id, "level": level, "target_id": target_id})
        key = target_id if level == "run" else f"{level}:{target_id}"
        self.artifacts.setdefault(key, []).append(row)
        return httpx.Response(200, json=row)

    def _presign(self, anchor: str, anchor_id: str, body: dict):
        """The shared presign leg for the non-run anchors.

        `have` (the server already holds these bytes) means no PUT. For a file anchor
        the swap to live also already happened, so the row comes back complete.
        """
        content_hash = body["content_hash"]
        artifact_id = str(uuid.uuid4())
        have = content_hash in self.uploaded
        row = {
            "id": artifact_id,
            "name": body["name"],
            "content_hash": content_hash,
            "size_bytes": body.get("size_bytes"),
            "content_type": body.get("content_type"),
            "status": "complete" if have else "pending",
            "is_reference": False,
            "created_at": self._stamp(),
            f"{anchor}_id": anchor_id,
        }
        self.artifacts.setdefault(f"{anchor}:{anchor_id}", []).append(row)
        return httpx.Response(
            201,
            json={
                "artifact_id": artifact_id,
                "have": have,
                "upload_url": None if have else f"{self.upload_base}/put/{artifact_id}",
                "key": f"lab-42/{artifact_id}",
                "upload_headers": getattr(self, "upload_headers", {}),
            },
        )

    def seed_series(
        self, run_id: str, key: str, points: dict[int, float], *, kind: str = "model"
    ) -> None:
        """Give a run a metric series that POST /v1/series/query will return.

        `points` is {step_index: value}; runs deliberately need not share steps,
        because differing length is usually the thing a comparison is about."""
        self.series_points.setdefault(str(run_id), []).append(
            {
                "run_id": str(run_id),
                "key": key,
                "kind": kind,
                "x_axis": "step",
                "dimensions": {},
                "points": [
                    {"step_index": step, "value": value, "wall_clock": "2026-07-27T00:00:00Z"}
                    for step, value in sorted(points.items())
                ],
            }
        )

    def seed_experiment(self, slug: str, *, project_id: str | None = None) -> dict:
        """Put an experiment straight into the fake, no HTTP.

        `client.run()` resolves its parents instead of creating them, so tests
        that are about something ELSE (auth, spans, artifacts) need one to exist
        without going through the create path or its preconditions."""
        eid = str(uuid.uuid4())
        row = {
            "id": eid,
            "customer_id": "lab-42",
            "slug": slug,
            "name": slug,
            "question": "h",
            # An experiment is always filed under a project (the experiment API
            # addresses it there), so a seed with none gets one of its own.
            "project_id": project_id or self._seed_home_project(slug),
            "created_at": _T0,
        }
        self.experiments[eid] = row
        return row

    def _seed_home_project(self, slug: str) -> str:
        """The project a project-less seeded experiment is filed under: a real
        row, so the experiment API (and the client's walk of the project list)
        finds it where the server would."""
        pid = str(uuid.uuid4())
        self.seeded_home_projects.add(pid)
        self.projects[pid] = {
            "id": pid,
            "slug": f"{slug}-home",
            "name": f"{slug}-home",
            "customer_id": "lab-42",
            "workspace_id": self._default_workspace_id(),
            "description": None,
            "metadata": {},
            "parent_project_id": None,
            "kind": "general",
            "created_at": _T0,
        }
        return pid

    def __init__(self):
        #: Titled sub-notes (0146), keyed by their own id.
        self.sub_notes: dict[str, dict] = {}
        self._sub_note_clock = 0
        # Models a backend that predates 0146: every sub-note route answers the
        # bare "Not Found" a missing FastAPI route produces, so the CLI's
        # upgrade-message mapping has something real to hit.
        self.sub_notes_route_absent = False
        self.requests: list[httpx.Request] = []
        #: Bearer tokens the fake refuses with a 401, as the real server does
        #: once a re-login revoked them (plan 2.7).
        self.rejected_tokens: set[str] = set()
        #: Per-token `/v1/me` answers (customer_id, user_id, ...), for a token
        #: that belongs to a different account than the default one.
        self.me_identities: dict[str, dict] = {}
        #: 0270: live log chunks, run id -> {(stream, raw_offset): body}, and
        #: every POST body in arrival order (replays included).
        self.log_chunks: dict[str, dict[tuple[str, int], dict]] = {}
        self.log_chunk_posts: list[dict] = []
        #: The next N log-chunk POSTs answer 503 (an outage), then heal.
        self.log_chunk_failures = 0
        #: The next N log-chunk POSTs answer 429 with this Retry-After (the
        #: server's per-run rate limit), then heal.
        self.log_chunk_throttled = 0
        self.log_chunk_retry_after = 30
        self.runs: dict[str, dict] = {}
        # 0268: creation_key -> (run id, request fingerprint), as the server
        # stores `runs.creation_key` / `creation_sha256`.
        self.creation_keys: dict[str, tuple[str, str]] = {}
        self.trials: dict[str, dict] = {}
        self.run_heartbeats: dict[str, int] = {}
        self.run_attached_beats: dict[str, int] = {}
        self.run_observer_heartbeats: dict[str, int] = {}
        self.experiments: dict[str, dict] = {}
        self.projects: dict[str, dict] = {}
        # Legacy personal rows behave like any other workspace. Keep their metadata
        # so the client cannot accidentally derive permissions or defaults from it.
        self.workspaces: dict[str, dict] = {
            _WS_MINE: {
                "id": _WS_MINE,
                "customer_id": "lab-42",
                "name": "Mine",
                "slug": "mine",
                "kind": "personal",
                "owner_user_id": _ME,
                "project_count": 0,
                "created_at": _T0,
            },
            _WS_OTHER: {
                "id": _WS_OTHER,
                "customer_id": "lab-42",
                "name": "Teammate",
                "slug": "teammate",
                "kind": "personal",
                "owner_user_id": "user-other",
                "project_count": 0,
                "created_at": _T0,
            },
        }
        # Artifacts are keyed by an anchor key ("run:<id>", "project:<id>", ...) so the
        # one confirm handler can find a row whatever it hangs off, exactly like the
        # server's single confirm core.
        self.artifacts: dict[str, list[dict]] = {}
        #: project id -> its papers (0152).
        #: project id -> its reference edges (0153).
        self.project_references: dict[str, list[dict]] = {}
        self.papers: dict[str, list[dict]] = {}
        # Phase 6 derived code reads, seeded by tests as canned payloads: the
        # real assembly is SQL over stored link rows, which the fake has no
        # tables for — mirroring it would be a second implementation to drift.
        #: experiment id -> ExperimentCodeOut-shaped dict.
        self.experiment_code: dict[str, dict] = {}
        #: run id -> RunCodeOut-shaped dict.
        self.run_code: dict[str, dict] = {}
        #: (run id, to param) -> RunCodeCompareOut-shaped dict.
        self.run_code_compare: dict[tuple[str, str], dict] = {}
        # Every accepted `POST /v1/artifacts/{id}/move`, and the refusal a test can
        # make the next one answer with. See _move_artifact.
        self.moves: list[dict] = []
        self.artifact_move_error: tuple[int, object] | None = None
        # Artifact rows are STAMPED and the anchored listings come back newest
        # first, like the real routers (`order_by="created_at DESC"`). The fake
        # used to omit created_at entirely and answer in insertion order -- the
        # exact opposite -- so 'which row is current?' was backwards here and
        # right in production.
        # Re-index fan-outs triggered by a project move, so a test can assert the
        # descendant reprojection actually fired.
        self.reindexed: list[str] = []
        self.tokens: dict[str, dict] = {}
        self.groups: dict[str, dict] = {}
        self.series: dict[str, list[dict]] = {}
        #: run_id -> SeriesResult rows, served by POST /v1/series/query (compare()).
        self.series_points: dict[str, list[dict]] = {}
        self.series_queries: list[dict] = []
        #: Extra fields POST /v1/series/query answers with -- `errors` (per-series
        #: read failures) and `truncated` (the raw-point ceiling) -- as seed knobs.
        self.series_result_extra: dict = {}
        #: Runs that are SOURCE-BACKED (a W&B mirror's passport): the series and
        #: bundle routes answer them 422 `unsupported_source_query` unless the
        #: request names the coverage-v1 read contract, as production does.
        self.source_backed_runs: set[str] = set()
        #: (run_id, trial) -> {"entries": [...], "counts": {...}, ...}, served by
        #: GET /v1/runs/{id}/sandbox-state/diff with its real path-keyed paging.
        self.sandbox_diffs: dict[tuple[str, str], dict] = {}
        self.sandbox_diff_calls: list[dict] = []
        #: run_id -> AgentSessionOut rows the run BUNDLE carries (capped at 50).
        self.run_sessions: dict[str, list[dict]] = {}
        #: artifact_id -> AgentSessionOut rows, GET /v1/artifacts/{id}/sessions.
        self.artifact_sessions: dict[str, list[dict]] = {}
        #: project_id -> ProjectReadmeOut, GET /v1/projects/{id}/readme.
        self.project_readmes: dict[str, dict] = {}
        self.metric_points: dict[str, list[dict]] = {}
        # Points as POSTED (coords/labels/span_id included), keyed by run id.
        # Separate from `metric_points`, which read-path tests seed by hand;
        # write-path tests assert on the captured wire payloads here.
        self.metric_points_posted: dict[str, list[dict]] = {}
        # Coordinate catalog rows (0060), seeded by hand like `metric_points`.
        self.coordinates: dict[str, list[dict]] = {}
        # 0062 per-key declared reduce fns, as a seed knob. The grouped handler
        # also honors `agg` fields on POSTED points, so the write-side
        # declaration is exercisable end to end.
        self.declared_aggs: dict[str, str] = {}
        # Server-side per-page ceilings BELOW the requested max_rows, so the
        # client's next_step/paging loops have something real to follow.
        self.grouped_page_rows: int | None = None
        self.wide_page_rows: int | None = None
        self.spans: dict[str, list[dict]] = {}
        #: run_id -> {step_index: step record}. Where log() puts non-numeric values.
        self.steps: dict[str, dict[int, dict]] = {}
        self.artifact_versions: dict[str, list[dict]] = {}
        self.edges: list[dict] = []
        self.execution_records: dict[str, dict] = {}
        self.experiment_versions: dict[str, list[dict]] = {}
        self.run_events: dict[str, list[dict]] = {}
        self.uploaded: set[str] = set()
        #: 0273: upload id -> the fake's multipart state (see `_multipart`).
        self.multipart: dict[str, dict] = {}
        #: Every part PUT, as (upload id, part number), in arrival order.
        self.multipart_part_puts: list[tuple[str, int]] = []
        #: Part numbers whose next PUT answers 503 (each once).
        self.multipart_fail_parts: set[int] = set()
        #: How many part PUTs the store refuses with 403 (an expired or
        #: foreign signed URL, #2075); -1 refuses every one.
        self.multipart_refuse_part_puts = 0
        self.puts: list[str] = []
        self.put_headers: list[dict[str, str]] = []
        self.gets: list[str] = []
        self.metrics_inserted = 0
        # WHOLE batch bodies, not just points: origin/provenance are batch-level
        # (0087), so a test asserting a derived write has to see the envelope.
        self.metric_batches_posted: list[dict] = []
        # Every write the 0185 fence refused (see `_fence_stale_writer`).
        self.fenced_writes: list[dict] = []
        # 2.3: seconds since each run last showed life (see `_note_activity`).
        self.run_silence: dict[str, float] = {}
        self.run_beat_silence: dict[str, float] = {}
        # 2.2: every writer-gone report received, applied or not.
        self.writer_gone_reports: list[dict] = []
        # 2.8: run id -> session id -> lease (the server's run_writers row).
        self.leases: dict[str, dict[str, dict]] = {}
        #: Every lease release received, in order (body included).
        self.lease_releases: list[dict] = []
        self.views: dict[str, list[dict]] = {}
        self.deleted_series: list[dict] = []
        self.spans_upserted = 0
        self.spans: dict[str, list[dict]] = {}
        self.blobs: dict[str, bytes] = {}
        # per-file code capture fakes (0193)
        self.capture_batches: list[dict] = []
        self.confirm_batches: list[list[str]] = []
        self.reject_capture_names: set[str] = set()
        self.unconfirm_once = False
        #: Names whose rows the fake "reaper" has already failed by confirm time
        #: (0193: a `failed` row is a verdict, not a retry).
        self.fail_capture_names: set[str] = set()
        #: The batch doors exist on this fake server. False = a server that
        #: predates them (404 on the presign door); the client must fall back.
        self.batch_doors = True
        #: Names whose presigned PUT the fake store refuses with 503 (every time).
        self.fail_put_names: set[str] = set()
        self.reject_put_names: set[str] = set()  # storage says 400 (checksum / policy)
        # Where presigned PUTs point. A test serving a second fake as "another
        # server" (#2073: a self-host install whose uploads went to Probe's
        # hosted API) sets it to that server's URL.
        self.upload_base = "http://r2.test"
        self.throttle_put_once = False  # the first PUT answers 429, then normal
        #: Bytes by content hash too, so a deduped run (rows with new ids, no
        #: PUT) can be restored the way the real store serves them.
        self.blobs_by_hash: dict[str, bytes] = {}
        # test knobs
        self.experiment_conflict_id: str | None = None
        #: Requests to the experiment API (`/v1/scopes`, `/v1/projects/{P}/experiments`).
        self.experiment_api_requests: list[str] = []
        #: Experiments moved to the trash through the experiment API.
        self.trashed_experiments: list[dict] = []
        #: Projects `seed_experiment` made to file a project-less seed under.
        self.seeded_home_projects: set[str] = set()
        #: False models a server older than `GET /v1/scopes?slug=` (FastAPI's
        #: bare "Not Found"), so the client's project walk is what answers.
        self.supports_scope_by_slug = True
        self.fail_next_metrics = False
        #: Production's metric-write contention answer (`MetricWriteBusy` ->
        #: `app/telemetry/metrics_router.py`): the next N metric POSTs get
        #: 503 {"detail": "concurrent telemetry write; retry this ingest batch"},
        #: with a `Retry-After` header when `metrics_busy_retry_after` is set
        #: (plan 0.4 adds one server-side).
        self.metrics_busy_next = 0
        self.metrics_busy_retry_after: str | None = None
        # /v1/web/* knobs. `web_responses[kind]` (kind: search|papers|read) is
        # returned verbatim; `web_status` overrides everything with that status
        # and `web_detail` as the body, which is how the 503/502/504 paths --
        # no Firecrawl key, over quota, upstream timeout -- get exercised.
        self.web_requests: list[tuple[str, dict]] = []
        self.web_responses: dict[str, dict | None] = {}
        self.web_status: int | None = None
        self.web_detail: str = "web search is not configured on this deployment"
        # /v1/search (workspaces+kb fold-in): None = a backend that predates the
        # endpoint (404); a dict is returned verbatim. Bodies are captured either way.
        # search_responses (a queue, popped per request) takes precedence over
        # search_response; search_404_once simulates one stale pod mid-deploy.
        #
        # The hosted backend HAS this route, so most suites want the fake to
        # answer it (`search_response = search_response()`). Left None here
        # rather than defaulted, so a test meaning "this route is absent" still
        # has to say so — there is no keyword fallback to absorb a 404 now.
        self.search_response: dict | None = None
        self.search_responses: list[dict] = []
        self.search_requests: list[dict] = []
        #: GET /v1/me call count — see the handler for why it is tracked.
        self.me_requests: int = 0
        # GET /v1/browse. `browse_response = None` models a backend that predates
        # the route, so `source.browse` has a 404 to turn into a truthful
        # CapabilityUnavailable instead of an empty tree.
        self.browse_requests: list[dict] = []
        self.browse_response: dict | None = None
        #: The TEAM NOTE (research-os 0125). An empty document at version 0 is
        #: what a team that has written nothing reads back -- never a 404: a
        #: fake that 404'd instead would let a client with the
        #: missing-means-empty bug pass every test here.
        self.team_note: dict = {
            "body": "",
            "version": 0,
            "updated_at": None,
            "updated_by": "",
            "remaining_chars": 100_000,
        }
        #: Recorded versions, oldest first -- the fake's history table.
        self.team_note_versions: list[dict] = []
        #: Make the next stale sync CONFLICT rather than merge cleanly. Both are
        #: real server behaviours and a client has to handle each.
        self.sync_conflict = False
        self.search_404_workspace_ids: set[str] = set()
        self.search_404_project_ids: set[str] = set()
        self.search_404_once = False
        self.fail_next_uploads = False
        # Captured coding-agent sessions. `work` answers EMPTY for an unknown
        # well-formed id (the real route is deliberately not an oracle);
        # transcripts are keyed by (session_id, source) because `source` is part
        # of the document's identity server-side — the same id under the wrong
        # agent 404s, and a fake that ignored the axis would hide exactly the
        # resolve-the-agent behavior the MCP source implements.
        self.session_work: dict[str, dict] = {}
        self.session_transcripts: dict[tuple[str, str], dict] = {}
        self.session_digests: dict[str, dict] = {}
        # Models a backend that predates the /v1/sessions/* routes: every one
        # 404s the way a missing FastAPI route does (bare "Not Found"), so the
        # source's capability handling has something real to discover.
        self.sessions_route_absent = False
        self._ts = 0
        # /v1/me reports the *token's* scopes, not the principal's: a read-only PAT
        # answers ["read"] even when its owner is an owner.
        self.me_scopes: list[str] = ["read", "write", "delete", "admin"]
        self.me_status = 200

    def _stamp(self) -> str:
        """A fresh, monotonically increasing timestamp per call. Distinct values let a
        test that pins ordering actually catch a wrong re-stamp."""
        self._ts += 1
        return f"2026-07-15T00:00:{self._ts:02d}Z"

    def _default_workspace_id(self) -> str:
        """Model the server fallback without asking the client to provision a row."""
        if not self.workspaces:
            wid = str(uuid.uuid4())
            self.workspaces[wid] = {
                "id": wid,
                "customer_id": "lab-42",
                "name": "Default workspace",
                "slug": "default",
                "kind": "team",
                "owner_user_id": None,
                "project_count": 0,
                "created_at": self._stamp(),
            }
        return min(self.workspaces.values(), key=lambda w: (w["created_at"], w["id"]))["id"]

    def _notes_cap_for(self, row: dict) -> int | None:
        """Which cap this response's row is enforced against, or None.

        Keyed on the fake's OWN stores rather than on the request path, because
        the path does not say: `POST /v1/experiments/{id}/groups` returns a group
        (4k) from an experiment-shaped route (100k), and a prefix table that got
        that backwards would publish a headroom four times too generous on the
        one carrier most likely to fill up.
        """
        row_id = row.get("id")
        if row_id is None:
            return None
        if self.notes_cap is not None:
            # A test playing a document AT its cap sets one number for the whole
            # fake; honouring it here keeps the published headroom agreeing with
            # the 422 the append path returns.
            return self.notes_cap
        if row_id in self.projects or row_id in self.experiments:
            return self.document_notes_cap
        if row_id in self.runs or row_id in self.trials or row_id in self.groups:
            return self.entity_notes_cap
        if any(row_id == a.get("id") for rows in self.artifacts.values() for a in rows):
            return self.entity_notes_cap
        return None

    def _with_notes_headroom(self, response: httpx.Response) -> httpx.Response:
        """Add the headroom fields the real server publishes on entity responses.

        Applied ONCE here rather than at each of the ~15 places this fake builds
        an entity row: the server derives them in one shared validator
        (`app.core.notes.notes_headroom`), so a fake that added them per-handler
        would drift into covering some doors and not others -- and the doors it
        missed would be exactly the ones no test noticed.

        Mirrors the server's rule that an ABSENT `notes` key publishes no
        headroom: a response that did not carry the document cannot say how full
        it is.
        """
        if not self.publishes_notes_headroom or response.status_code >= 300:
            return response
        try:
            row = response.json()
        except ValueError:
            return response
        if not isinstance(row, dict):
            return response
        cap = self._notes_cap_for(row)
        if cap is None:
            return response
        payload = dict(row)
        payload["notes_limit_chars"] = cap
        if "notes" in row:
            payload["notes_remaining_chars"] = max(0, cap - len(row["notes"] or ""))
        # `notes_version` is NOT NULL DEFAULT 0 on every carrier, and entity
        # responses publish it (0130) whether or not a note was ever written.
        payload.setdefault("notes_version", 0)
        return httpx.Response(response.status_code, json=payload)

    def _sub_note_tick(self) -> str:
        """A monotonically increasing fake timestamp — creation order IS tab
        order, so the fake's clock must never tie. All of the motion is in the
        fixed-width microseconds field: a seconds field that grew past two
        digits would sort lexicographically BEFORE its predecessor ("00:100" <
        "00:99") and flip tab order at the hundredth write."""
        self._sub_note_clock += 1
        return f"2026-08-25T00:00:00.{self._sub_note_clock:06d}Z"

    def _sub_note_meta(self, row: dict, cap: int) -> dict:
        """A sub-note WRITE shape: metadata + headroom, never the body —
        mirroring the server, whose write responses refuse to echo a document
        a write-scoped caller could not GET."""
        return {
            "id": row["id"],
            "title": row["title"],
            "chars": len(row["body"]),
            "notes_version": row["notes_version"],
            "remaining_chars": max(0, cap - len(row["body"])),
            "limit_chars": cap,
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }

    def _sub_note_list_row(self, row: dict, cap: int) -> dict:
        """A LIST row: `SubNoteListItem` exactly — no `remaining_chars`. The
        real list omits it (the list is for choosing, the write prices), so a
        consumer that grew to read headroom off list rows must fail HERE, not
        first in production."""
        item = self._sub_note_meta(row, cap)
        del item["remaining_chars"]
        return item

    def _sub_note_parent_exists(self, parent_kind: str, parent_id: str) -> bool:
        """The `_require_entity` gate: sub-note routes 404 with the kind's
        name when the carrier itself is missing, before any sub-note logic."""
        if parent_kind == "project":
            return parent_id in self.projects
        if parent_kind == "experiment":
            return parent_id in self.experiments
        if parent_kind == "run":
            return parent_id in self.runs
        if parent_kind == "group":
            return parent_id in self.groups
        return any(
            parent_id == a.get("id") for rows in self.artifacts.values() for a in rows
        )

    @staticmethod
    def _sub_note_title_error(title: str) -> httpx.Response | None:
        """`normalized_title`'s refusals, message-for-message."""
        trimmed = title.strip()
        if not trimmed:
            return httpx.Response(422, json={"detail": "sub-note title must not be blank"})
        if "\n" in trimmed or "\r" in trimmed:
            return httpx.Response(
                422, json={"detail": "sub-note title must be a single line"}
            )
        if len(trimmed) > 120:
            return httpx.Response(
                422, json={"detail": "sub-note title exceeds the 120-character limit"}
            )
        return None

    @staticmethod
    def _sub_note_verb_count_error(body: dict) -> httpx.Response | None:
        """The schema's mutual-exclusion rule: at most ONE body verb. Runs
        before any resolution, as Pydantic does on the real routes."""
        verbs = [
            v
            for v in (body.get("body"), body.get("body_append"), body.get("body_edit"))
            if v is not None
        ]
        if len(verbs) > 1:
            return httpx.Response(
                422,
                json={"detail": "body, body_append and body_edit are mutually exclusive"},
            )
        return None

    def _apply_sub_note_verb(self, row: dict, body: dict, cap: int) -> httpx.Response | None:
        """The three body verbs on one sub-note; a refusal, or None.

        Same separator and refusal shapes as `_apply_notes_write` — including
        the "notes limit" wording the CLI's cap advice keys on.
        """
        changed = False
        if body.get("body") is not None:
            if len(body["body"]) > cap:
                return httpx.Response(
                    422, json={"detail": f"sub-note body exceeds the {cap}-character limit"}
                )
            if body["body"] != row["body"]:
                row["body"] = body["body"]
                changed = True
        if body.get("body_append") is not None:
            current = row["body"]
            if not current or current.endswith("\n\n"):
                separator = ""
            elif current.endswith("\n"):
                separator = "\n"
            else:
                separator = "\n\n"
            merged = current + separator + body["body_append"]
            if len(merged) > cap:
                return httpx.Response(
                    422,
                    json={
                        "detail": (
                            f"appending would exceed the {cap}-character notes limit; "
                            "nothing further can be stored until this document is compacted"
                        )
                    },
                )
            row["body"] = merged
            changed = True
        if body.get("body_edit") is not None:
            edit = body["body_edit"]
            count = row["body"].count(edit["old_text"])
            if count != 1:
                return httpx.Response(
                    409,
                    json={
                        "detail": {
                            "message": (
                                "old_text must match exactly once; "
                                f"found {count}. Retry with more surrounding context."
                            ),
                            "match_count": count,
                            "current_notes": row["body"],
                        }
                    },
                )
            merged = row["body"].replace(edit["old_text"], edit["new_text"])
            if len(merged) > cap:
                return httpx.Response(
                    422, json={"detail": f"the edit would exceed the {cap}-character notes limit"}
                )
            row["body"] = merged
            changed = True
        if changed:
            row["notes_version"] += 1
            row["updated_at"] = self._sub_note_tick()
        return None

    #: The notes write's own fields, never columns the PATCH copies onto the row:
    #: the three writes and the replace's precondition, idempotency key and force.
    NOTES_WRITE_FIELDS = (
        "notes", "notes_append", "notes_edit", "base_version", "op_key", "force",
    )

    def _apply_notes_write(
        self, row: dict, body: dict, cap: int, *, stores: bool = True
    ) -> httpx.Response | None:
        """The server's three notes primitives on one row; a refusal, or None.

        ONE implementation for every carrier. The fake used to model only the
        project's `notes_append`, and every other PATCH handler copied the request
        body onto the row key by key -- so `append_notes("run", ...)` stored a
        literal `notes_append` field on the run and a test could assert a
        successful append against a row that had never gained the paragraph.

        `notes_edit` is modelled here for the first time. Its two refusals are
        different HTTP answers to a caller (409 "matched twice, retry with more
        context" versus 422 "the result would not fit"), and a fake that silently
        did nothing let both read as success.
        """
        cap = self.notes_cap if self.notes_cap is not None else cap
        if not stores:
            return None
        if body.get("notes") is not None:
            # The replace's precondition (`stale_replace`): a `base_version`
            # that is not the head is refused with the head's version and no
            # body. `notes_version` moves only when the text does (0130).
            head = row.get("notes_version") or 0
            base = body.get("base_version")
            if base is not None and base != head:
                return httpx.Response(
                    409,
                    json={
                        "detail": {
                            "message": (
                                "the document moved since you read it; re-read it and "
                                "merge, then replace again from the version you merged onto"
                            ),
                            "notes_version": head,
                        }
                    },
                )
            if body["notes"] != (row.get("notes") or ""):
                row["notes_version"] = head + 1
            row["notes"] = body["notes"]
        if self.stores_notes_append and body.get("notes_append") is not None:
            current = row.get("notes") or ""
            # Tops the document up to a BLANK LINE, matching research-os
            # 0.117.0.0. Notes are one markdown document, and two paragraphs
            # joined by a single newline render as one paragraph -- so a fake
            # that used \n would let a test pass on prose the real server
            # would render wrong.
            if not current or current.endswith("\n\n"):
                separator = ""
            elif current.endswith("\n"):
                separator = "\n"
            else:
                separator = "\n\n"
            merged = current + separator + body["notes_append"]
            if len(merged) > cap:
                return httpx.Response(
                    422,
                    json={
                        "detail": (
                            f"appending would exceed the {cap}-character notes "
                            "limit; nothing further can be stored until this "
                            "document is compacted"
                        )
                    },
                )
            row["notes"] = merged
        if body.get("notes_edit") is not None:
            current = row.get("notes") or ""
            old_text = body["notes_edit"]["old_text"]
            new_text = body["notes_edit"]["new_text"]
            # NON-overlapping, exactly as the server counts it (a length delta
            # over `replace`), so "x"*90 inside "x"*95 is ONE match here and one
            # match there. Counting overlaps would refuse a compaction the real
            # server performs.
            matches = current.count(old_text)
            if matches != 1:
                return httpx.Response(
                    409,
                    json={
                        "detail": {
                            "message": (
                                "old_text must match exactly once; "
                                f"found {matches}. Retry with more surrounding context."
                            ),
                            "match_count": matches,
                            "current_notes": current,
                        }
                    },
                )
            edited = current.replace(old_text, new_text)
            if len(edited) > cap:
                return httpx.Response(
                    422,
                    json={"detail": f"the edit would exceed the {cap}-character notes limit"},
                )
            row["notes"] = edited
        return None

    def _notes_catalog(self, include_sub_notes: bool = False) -> dict:
        """`GET /v1/notes`: every non-empty note carrier in the tenant.

        Only rows whose document is non-empty, matching the server's
        `btrim(body) <> ''` filter -- a catalog that listed every empty row would
        let a sweep pass here while reporting hundreds of 0% documents against a
        real backend.
        """
        items: list[dict] = []
        body = self.team_note.get("body") or ""
        if body.strip():
            items.append(
                {
                    "kind": "team_note",
                    "id": None,
                    "title": "Team note",
                    "excerpt": body[:280],
                    "ancestors": [],
                    "chars": len(body),
                    "limit_chars": self.document_notes_cap,
                    "created_at": None,
                    "updated_at": self.team_note.get("updated_at"),
                }
            )
        rows: list[tuple[str, dict, int]] = []
        rows += [("project", r, self.document_notes_cap) for r in self.projects.values()]
        rows += [("experiment", r, self.document_notes_cap) for r in self.experiments.values()]
        rows += [("run", r, self.entity_notes_cap) for r in self.runs.values()]
        rows += [("trial", r, self.entity_notes_cap) for r in self.trials.values()]
        rows += [("group", r, self.entity_notes_cap) for r in self.groups.values()]
        rows += [
            ("artifact", a, self.entity_notes_cap)
            for anchored in self.artifacts.values()
            for a in anchored
        ]
        for kind, row, cap in rows:
            document = row.get("notes") or ""
            if not document.strip():
                continue
            items.append(
                {
                    "kind": kind,
                    "id": row.get("id"),
                    "title": row.get("name") or row.get("slug") or "",
                    "excerpt": document[:280],
                    "ancestors": [],
                    "chars": len(document),
                    "limit_chars": self.notes_cap if self.notes_cap is not None else cap,
                    "created_at": row.get("created_at"),
                    "updated_at": row.get("updated_at"),
                }
            )
        if include_sub_notes:
            # Opt-in (0146): sub-note rows join the sweep, ancestors ending
            # with the immediate parent — the real variant's contract.
            for note in self.sub_notes.values():
                if not (note["body"] or "").strip():
                    continue
                cap = 100_000 if note["parent_kind"] in ("project", "experiment") else 4_000
                items.append(
                    {
                        "kind": "sub_note",
                        "id": note["id"],
                        "title": note["title"],
                        "excerpt": note["body"][:280],
                        "ancestors": [
                            {"kind": note["parent_kind"], "id": note["parent_id"], "title": "P"}
                        ],
                        "chars": len(note["body"]),
                        "limit_chars": cap,
                        "created_at": note["created_at"],
                        "updated_at": note["updated_at"],
                    }
                )
        return {"items": items, "next_cursor": None}

    #: 0231: `/v1/projects/{experiment}` IS `/v1/experiments/{experiment}`.
    #:
    #: The server gives every experiment route a project-address twin that
    #: SHARES ITS IMPLEMENTATION, and the SDK now speaks the project address.
    #: This fake has one handler per route, written against the old spelling,
    #: so without an alias every one of those tests fails with "no fake route"
    #: -- a red suite that says nothing about the client.
    #:
    #: Rewriting at the door rather than duplicating ~20 handlers is also the
    #: HONEST double: the real server has one body behind two paths, and a fake
    #: with two bodies could pass while they drifted. It rewrites ONLY when the
    #: id is a known experiment, so a genuine project route is untouched and a
    #: typo still 404s instead of being quietly absorbed.
    def _experiment_alias(self, method, path, body, params):
        if path.startswith("/v1/projects/"):
            entity_id, _, tail = path[len("/v1/projects/") :].partition("/")
            if entity_id in self.experiments:
                # The BARE item path carries the renamed fields; a sub-path
                # (`/runs`, `/sub-notes`, …) carries its own body and must not
                # be touched, where `description` means something else.
                mapped = body
                if not tail and isinstance(body, dict):
                    mapped = dict(body)
                    if "description" in mapped:
                        mapped["question"] = mapped.pop("description")
                    if "parent_project_id" in mapped:
                        mapped["project_id"] = mapped.pop("parent_project_id")
                return (
                    f"/v1/experiments/{entity_id}" + (f"/{tail}" if tail else ""),
                    mapped,
                )
            return path, body
        if path != "/v1/projects":
            return path, body
        # THE COLLECTION DOOR, where the two addresses differ in more than the
        # segment. `kind=experiment` is what makes a created project a leaf, and
        # the two renames the merge decided on travel with it: the QUESTION an
        # experiment answers IS its description, and its project IS its parent.
        if method == "POST" and (body or {}).get("kind") == "experiment":
            mapped = {k: v for k, v in (body or {}).items() if k != "kind"}
            if "description" in mapped:
                mapped["question"] = mapped.pop("description")
            if "parent_project_id" in mapped:
                mapped["project_id"] = mapped.pop("parent_project_id")
            return "/v1/experiments", mapped
        if method == "GET":
            # A slug names ONE row across the tenant, so a slug that belongs to
            # an experiment is asking for that experiment however it is spelled.
            slug = params.get("slug")
            if params.get("kind") == "experiment" or (
                slug and any(r.get("slug") == slug for r in self.experiments.values())
            ):
                return "/v1/experiments", body
        return path, body


    # -- the experiment API (light experiments; the SDK speaks it from R4) ----
    #
    # `GET /v1/scopes/{id}` and `/v1/projects/{P}/experiments[/{E}]`, over the
    # SAME `self.experiments` rows the old-address handlers keep, so a test can
    # mix the two (a run is still created at `/v1/projects/{E}/runs`). Bodies are
    # closed like the real `write_schemas.py` (extra="forbid"); a row answers in
    # `ProjectExperimentOut` shape: `project_id` is the project it is filed under.

    _EXPERIMENT_CREATE_FIELDS = frozenset({"slug", "name", "question", "authored_by"})
    _EXPERIMENT_PATCH_FIELDS = frozenset(
        {"name", "question", "notes", "base_version", "project_id", "authored_by"}
    )

    def _experiment_out(self, row: dict) -> dict:
        return {
            "id": row["id"],
            "project_id": row.get("project_id"),
            "slug": row.get("slug"),
            "legacy_slug": row.get("legacy_slug"),
            "name": row.get("name") or row.get("slug"),
            "question": row.get("question"),
            "run_count": sum(1 for r in self.runs.values() if r.get("experiment_id") == row["id"]),
            "created_at": row.get("created_at") or _T0,
            "updated_at": row.get("updated_at") or row.get("created_at") or _T0,
            "created_by": row.get("created_by"),
        }

    def _experiment_of_project(self, project_id: str, ref: str) -> dict | None:
        for row in self.experiments.values():
            if row.get("project_id") != project_id:
                continue
            if ref in (row["id"], row.get("slug"), row.get("legacy_slug")):
                return row
        return None

    def _experiment_api(self, method, path, body, request) -> httpx.Response | None:
        params = request.url.params
        if path == "/v1/scopes" and method == "GET":
            self.experiment_api_requests.append(f"{method} {path}")
            if not self.supports_scope_by_slug:
                return httpx.Response(404, json={"detail": "Not Found"})
            slug = params.get("slug")
            if not slug:
                return httpx.Response(422, json={"detail": [{"loc": ["query", "slug"], "type": "missing"}]})
            exp = next((r for r in self.experiments.values() if r.get("slug") == slug), None)
            if exp is None:
                proj = next((r for r in self.projects.values() if r.get("slug") == slug), None)
                if proj is not None:
                    return httpx.Response(200, json={
                        "id": proj["id"], "kind": "project", "project_id": proj["id"],
                        "experiment_id": None, "run_id": None})
                exp = next((r for r in self.experiments.values() if r.get("legacy_slug") == slug), None)
            if exp is None:
                return httpx.Response(404, json={"detail": "no project or experiment with this slug"})
            return httpx.Response(200, json={
                "id": exp["id"], "kind": "experiment", "project_id": exp.get("project_id"),
                "experiment_id": exp["id"], "run_id": None})
        m = re.fullmatch(r"/v1/scopes/([^/]+)", path)
        if m and method == "GET":
            self.experiment_api_requests.append(f"{method} {path}")
            ident = m.group(1)
            if ident in self.experiments:
                row = self.experiments[ident]
                return httpx.Response(200, json={
                    "id": ident, "kind": "experiment", "project_id": row.get("project_id"),
                    "experiment_id": ident, "run_id": None})
            if ident in self.projects:
                return httpx.Response(200, json={
                    "id": ident, "kind": "project", "project_id": ident,
                    "experiment_id": None, "run_id": None})
            if ident in self.runs:
                run = self.runs[ident]
                return httpx.Response(200, json={
                    "id": ident, "kind": "run", "project_id": run.get("project_id"),
                    "experiment_id": run.get("experiment_id"), "run_id": ident})
            return httpx.Response(404, json={"detail": "nothing with this id"})
        m = re.fullmatch(r"/v1/projects/([^/]+)/experiments(?:/([^/]+))?", path)
        if not m:
            return None
        self.experiment_api_requests.append(f"{method} {path}")
        project_id, ref = m.group(1), m.group(2)
        if method != "GET" and not all(_is_uuid_text(v) for v in (project_id, ref) if v is not None):
            # Writes take uuids only (`write_router.py`: a slug can be minted
            # again once its holder is in the trash), so a slug in either slot
            # is FastAPI's uuid_parsing 422.
            return httpx.Response(422, json={"detail": [
                {"loc": ["path", "project_ref"], "type": "uuid_parsing",
                 "msg": "Input should be a valid UUID"}]})
        if project_id in self.experiments:
            return httpx.Response(404, json={"detail": "project not found: this id is an experiment"})
        if ref is None and method == "GET":
            rows = sorted(
                (r for r in self.experiments.values() if r.get("project_id") == project_id),
                key=lambda r: (str(r.get("created_at") or ""), r["id"]),
                reverse=True,
            )
            limit, offset = int(params.get("limit", 100)), int(params.get("offset", 0))
            window = rows[offset : offset + limit]
            more = offset + limit < len(rows)
            return httpx.Response(200, json={
                "items": [self._experiment_out(r) for r in window], "total": len(rows),
                "limit": limit, "offset": offset, "next_offset": offset + limit if more else None})
        if ref is None and method == "POST":
            extra = sorted(set(body or {}) - self._EXPERIMENT_CREATE_FIELDS)
            if extra:
                return httpx.Response(422, json={"detail": [
                    {"loc": ["body", k], "type": "extra_forbidden"} for k in extra]})
            slug = (body or {}).get("slug")
            holder = next((r for r in self.experiments.values() if r.get("slug") == slug), None)
            kind = "experiment"
            if holder is None:
                holder = next((r for r in self.projects.values() if r.get("slug") == slug), None)
                kind = "project"
            if holder is None and self.experiment_conflict_id:
                holder = self.experiments.get(self.experiment_conflict_id) or {
                    "id": self.experiment_conflict_id}
                kind = "experiment"
            if holder is not None:
                return httpx.Response(409, json={"detail": {
                    "message": f"slug {slug!r} is taken", "existing_id": holder["id"],
                    "suggestion": f"{slug}-2",
                    "existing": {"id": holder["id"], "kind": kind,
                                 "parent_project_id": holder.get("project_id") if kind == "experiment"
                                 else holder.get("parent_project_id"),
                                 "workspace_id": None}}})
            eid = str(uuid.uuid4())
            row = {
                "id": eid,
                "slug": slug,
                "name": _chosen_name(body.get("name"), slug) or slug,
                "name_customized": _owns_field(_chosen_name(body.get("name"), slug), body.get("authored_by")),
                "question": body.get("question"),
                "project_id": project_id,
                "customer_id": "lab-42",
                "created_at": self._stamp(),
            }
            if body.get("authored_by") is not None:
                row["authored_by"] = body["authored_by"]
            self.experiments[eid] = row
            return httpx.Response(201, json={**self._experiment_out(row), "notes_version": 0})
        row = self._experiment_of_project(project_id, ref) if ref else None
        if row is None:
            return httpx.Response(404, json={"detail": "experiment not found"})
        if method == "GET":
            return httpx.Response(200, json={
                **self._experiment_out(row),
                "notes": row.get("notes"),
                "notes_version": row.get("notes_version", 0),
                "notes_updated_at": None,
                "summary": {"content": "absent", "job": "idle", "blurb": None, "version": 0},
            })
        if method == "PATCH":
            extra = sorted(set(body or {}) - self._EXPERIMENT_PATCH_FIELDS)
            if extra:
                return httpx.Response(422, json={"detail": [
                    {"loc": ["body", k], "type": "extra_forbidden"} for k in extra]})
            if "notes" in body:
                refused = self._apply_notes_write(row, body, self.document_notes_cap)
                if refused is not None:
                    return refused
            target = body.get("project_id")
            if "project_id" in body and target is None:
                return httpx.Response(422, json={"detail": "an experiment is always filed under a project"})
            if target is not None and target in self.experiments:
                return httpx.Response(422, json={"detail": "the target is an experiment"})
            for key in ("name", "question", "authored_by"):
                if body.get(key) is not None:
                    row[key] = body[key]
            if target is not None:
                row["project_id"] = target
            return httpx.Response(200, json={**self._experiment_out(row),
                                             "notes_version": row.get("notes_version", 0)})
        if method == "DELETE":
            if params.get("dry_run") == "true":
                return httpx.Response(200, json={
                    "dry_run": True, "type": "experiment", "id": row["id"], "name": row.get("name"),
                    "count": {"projects": 1, "runs": 0, "groups": 0},
                    "created_by": {"unknown": {"projects": 1, "runs": 0, "groups": 0}},
                    "updated_at": None, "restorable_until": "2026-08-05T00:00:00Z"})
            self.experiments.pop(row["id"])
            # The trash hides the experiment's runs with it (a fake has no
            # hidden state, so they go).
            for rid in [rid for rid, r in self.runs.items() if r.get("experiment_id") == row["id"]]:
                self.runs.pop(rid)
            self.trashed_experiments.append({"id": row["id"], "reason": params.get("reason")})
            return httpx.Response(200, json={
                "trashed": True, "type": "experiment", "id": row["id"], "name": row.get("name"),
                "trash_id": str(uuid.uuid4()), "trashed_at": self._stamp(),
                "restorable_until": "2026-08-05T00:00:00Z",
                "count": {"projects": 1, "runs": 0, "groups": 0},
                "message": "moved to the trash"})
        return httpx.Response(405, json={"detail": "Method Not Allowed"})

    def handler(self, request: httpx.Request) -> httpx.Response:
        return self._with_notes_headroom(self._dispatch(request))

    def _dispatch(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        method = request.method
        path = request.url.path
        bearer = request.headers.get("authorization", "").removeprefix("Bearer ")
        if bearer and bearer in self.rejected_tokens:
            return httpx.Response(401, json={"detail": "invalid or revoked token"})
        # Per-path fault injection. Set `app.fail_paths = {"/v1/..."}` to make ONE
        # route 500 while the rest of the fake stays healthy -- the shape you need to
        # test that a degraded dependency is REPORTED rather than propagated.
        if path in getattr(self, "fail_paths", ()):
            return httpx.Response(500, json={"detail": "injected failure"})
        try:
            body = json.loads(request.content) if request.content else {}
        except (json.JSONDecodeError, ValueError):
            body = {}  # e.g. a raw-bytes PUT to a presigned URL
        path, body = self._experiment_alias(method, path, body, request.url.params)
        fenced = self._fence_stale_writer(method, path, body, request)
        if fenced is not None:
            return fenced
        self._note_activity(method, path)
        answered = self._experiment_api(method, path, body, request)
        if answered is not None:
            return answered

        if path == "/v1/me" and method == "GET":
            # Counted so a test can prove the MCP source caches identity: every
            # envelope carries the caller, so an uncached read is one request
            # per tool call.
            self.me_requests += 1
            if self.me_status != 200:
                return httpx.Response(self.me_status, json={"error": "invalid_token"})
            bearer = request.headers.get("authorization", "").removeprefix("Bearer ")
            return httpx.Response(
                200,
                json={
                    "user_id": "00000000-0000-0000-0000-000000000001",
                    "email": "dev@example.com",
                    "name": "Dev",
                    "customer_id": "lab-42",
                    "role": "owner",
                    "scopes": list(self.me_scopes),
                    "via": "token",
                    **self.me_identities.get(bearer, {}),
                },
            )

        if path == "/v1/tokens/current" and method == "DELETE":
            return httpx.Response(204)

        if path == "/v1/browse" and method == "GET":
            self.browse_requests.append(dict(request.url.params))
            if self.browse_response is None:
                return httpx.Response(404, json={"detail": "Not Found"})
            return httpx.Response(200, json=self.browse_response)

        # -- reads the MCP's entity views and browse modes reach --------------
        m = re.match(r"^/v1/runs/([^/]+)/sandbox-state/diff$", path)
        if m and method == "GET":
            rid, trial = m.group(1), request.url.params.get("trial")
            self.sandbox_diff_calls.append(dict(request.url.params))
            if not trial:
                # `trial` is `Query(...)` on the real route.
                return httpx.Response(422, json={"detail": "trial is required"})
            diff = self.sandbox_diffs.get((rid, trial))
            if diff is None:
                return httpx.Response(
                    404,
                    json={"detail": {"reason": "no_bundle", "message": f"no bundle for {trial}"}},
                )
            entries = sorted(diff["entries"], key=lambda e: e["path"])
            prefix = request.url.params.get("path_prefix")
            if prefix:
                entries = [e for e in entries if e["path"].startswith(prefix)]
            # The real cursor is the LAST PATH of the previous page.
            after = request.url.params.get("cursor")
            if after:
                entries = [e for e in entries if e["path"] > after]
            limit = int(request.url.params.get("limit") or 500)
            page, more = entries[:limit], len(entries) > limit
            return httpx.Response(
                200,
                json={
                    "trial": trial,
                    "schema": "probe.sandbox-state/1",
                    "compare_mode": "hash",
                    "begin_state_hash": "b" * 64,
                    "counts": diff["counts"],
                    "entries": page,
                    "truncated": more,
                    "next_cursor": page[-1]["path"] if more else None,
                },
            )

        m = re.match(r"^/v1/artifacts/([^/]+)/sessions$", path)
        if m and method == "GET":
            rows = self.artifact_sessions.get(m.group(1), [])
            limit = int(request.url.params.get("limit") or 50)
            return httpx.Response(
                200, json={"sessions": rows[:limit], "session_total": len(rows)}
            )

        m = re.match(r"^/v1/projects/([^/]+)/readme$", path)
        if m and method == "GET":
            pid = m.group(1)
            if pid not in self.projects:
                return httpx.Response(404, json={"detail": "project not found"})
            # app/integrations/github/readme_router.py: a project with no
            # attached repository answers `{"state": "none"}` -- no reason, no
            # text. Seeds use the real states (snapshot/live/none/unavailable).
            return httpx.Response(200, json=self.project_readmes.get(pid) or {"state": "none"})

        # -- the tenant-wide notes catalog --------------------------------
        # One flat page per `limit` (offset cursor), with `query` matched
        # literally. What it models above all is the row shape the sweep ranks
        # on -- `chars` and `limit_chars` per row, with the caps differing by
        # kind, which is the whole reason the sweep can compare a run note
        # against a project note at all.
        # -- overview pages (0199) ----------------------------------------
        # The agent door. Models the server's verdicts a CLI test cares about:
        # 404 for an unknown entity or a tenant without the lane
        # (`overview_lane_enabled`), 422 naming the fault for a page the frame
        # would block, and the OverviewOut shape on success.
        m = re.match(r"^/v1/(projects|experiments)/([^/]+)/overview$", path)
        if m and method == "PUT":
            plural, entity_id = m.groups()
            entity_kind = plural[:-1]
            if not getattr(self, "overview_lane_enabled", True):
                return httpx.Response(404, json={"detail": "Not Found"})
            if not self._sub_note_parent_exists(entity_kind, entity_id):
                return httpx.Response(404, json={"detail": f"{entity_kind} not found"})
            html = body.get("html") or ""
            if "<script src=\"https://evil" in html or "<iframe" in html:
                return httpx.Response(
                    422, json={"detail": "<iframe> is not allowed: the page is a FRAGMENT"}
                )
            if not body.get("blurb"):
                return httpx.Response(422, json={"detail": "`blurb` must be a non-empty string"})
            record = {
                "anchor_type": entity_kind,
                "anchor_id": entity_id,
                "content": "fresh",
                "job": "idle",
                "failed_reason": None,
                "skip_reason": None,
                "generated_at": "2026-09-08T00:00:00Z",
                "prompt_version": "1",
                "source": "agent",
                "html": html,
                "plan": body.get("plan") or "Written by the researcher's agent.",
                "blurb": body["blurb"],
                "series": {"manifest": body.get("series") or [], "data": {}},
                "model": None,
                "basis": {"written_by": "agent"},
                "refresh_queued": False,
            }
            self.__dict__.setdefault("overviews", {})[(entity_kind, entity_id)] = record
            return httpx.Response(200, json=record)

        # -- sub-notes (0146) ---------------------------------------------
        m = re.match(r"^/v1/(projects|experiments|runs|groups|artifacts)/([^/]+)/sub-notes$", path)
        if m:
            if self.sub_notes_route_absent:
                return httpx.Response(404, json={"detail": "Not Found"})
            plural, parent_id = m.groups()
            parent_kind = plural[:-1]
            if not self._sub_note_parent_exists(parent_kind, parent_id):
                # `_require_entity` 404s with the kind's name — an entity miss,
                # NOT the route-shaped bare "Not Found" the upgrade mapping
                # keys on.
                return httpx.Response(404, json={"detail": f"{parent_kind} not found"})
            cap = 100_000 if parent_kind in ("project", "experiment") else 4_000
            rows = [r for r in self.sub_notes.values() if r["parent_id"] == parent_id]
            rows.sort(key=lambda r: (r["created_at"], r["id"]))
            if method == "GET":
                return httpx.Response(
                    200,
                    json={
                        "sub_notes": [self._sub_note_list_row(r, cap) for r in rows],
                        "limit_count": 20,
                    },
                )
            body = json.loads(request.content or b"{}")
            if method == "POST":
                bad_title = self._sub_note_title_error(body.get("title") or "")
                if bad_title is not None:
                    return bad_title
                if len(rows) >= 20:
                    return httpx.Response(
                        422,
                        json={
                            "detail": (
                                f"this {parent_kind} already carries 20 sub-notes; "
                                "delete one before creating another"
                            )
                        },
                    )
                text = body.get("body") or ""
                if len(text) > cap:
                    return httpx.Response(
                        422, json={"detail": f"sub-note body exceeds the {cap}-character limit"}
                    )
                row = {
                    "id": str(uuid.uuid4()),
                    "parent_kind": parent_kind,
                    "parent_id": parent_id,
                    "title": (body.get("title") or "").strip(),
                    "body": text,
                    "notes_version": 1 if text else 0,
                    "created_at": self._sub_note_tick(),
                    "updated_at": self._sub_note_tick(),
                }
                self.sub_notes[row["id"]] = row
                return httpx.Response(201, json=self._sub_note_meta(row, cap))
            if method == "PATCH":
                # Schema validation first, as Pydantic runs it: verb rules
                # refuse BEFORE any title resolution happens.
                bad = self._sub_note_verb_count_error(body)
                if bad is not None:
                    return bad
                if not any(
                    body.get(k) is not None for k in ("body", "body_append", "body_edit")
                ):
                    return httpx.Response(
                        422,
                        json={"detail": "one of body, body_append or body_edit is required"},
                    )
                bad_title = self._sub_note_title_error(body.get("note_title") or "")
                if bad_title is not None:
                    return bad_title
                title = (body.get("note_title") or "").strip()
                matches = [r for r in rows if r["title"] == title]
                if not matches:
                    return httpx.Response(
                        404,
                        json={
                            "detail": {
                                "message": f"no sub-note titled {title!r} on this {parent_kind}",
                                "titles": [r["title"] for r in rows],
                            }
                        },
                    )
                if len(matches) > 1:
                    return httpx.Response(
                        409,
                        json={
                            "detail": {
                                "message": (
                                    f"{len(matches)} sub-notes are titled {title!r}; "
                                    "a title-addressed write must match exactly one. "
                                    "Rename one, or address by id."
                                ),
                                "match_count": len(matches),
                                "ids": [r["id"] for r in matches],
                            }
                        },
                    )
                # Same precondition the by-id door enforces, and the real
                # route enforces on both: a double that accepts a stale
                # base_version on one door only is worse than one that accepts
                # it on neither -- it makes the two doors look different when
                # they are not.
                if (
                    body.get("body") is not None
                    and body.get("base_version") is not None
                    and body["base_version"] != matches[0]["notes_version"]
                ):
                    return httpx.Response(
                        409,
                        json={
                            "detail": {
                                "message": "the document moved since you read it",
                                "notes_version": matches[0]["notes_version"],
                            }
                        },
                    )
                refusal = self._apply_sub_note_verb(matches[0], body, cap)
                if refusal is not None:
                    return refusal
                return httpx.Response(200, json=self._sub_note_meta(matches[0], cap))

        m = re.match(r"^/v1/sub-notes/([^/]+)$", path)
        if m:
            if self.sub_notes_route_absent:
                return httpx.Response(404, json={"detail": "Not Found"})
            row = self.sub_notes.get(m.group(1))
            if row is None:
                return httpx.Response(404, json={"detail": "sub-note not found"})
            cap = 100_000 if row["parent_kind"] in ("project", "experiment") else 4_000
            if method == "GET":
                return httpx.Response(
                    200, json={**self._sub_note_meta(row, cap), "body": row["body"]}
                )
            if method == "PATCH":
                body = json.loads(request.content or b"{}")
                bad = self._sub_note_verb_count_error(body)
                if bad is not None:
                    return bad
                has_verb = any(
                    body.get(k) is not None for k in ("body", "body_append", "body_edit")
                )
                if body.get("title") is None and not has_verb:
                    return httpx.Response(
                        422,
                        json={"detail": "nothing to change: send title, or one body verb"},
                    )
                if body.get("title") is not None:
                    bad_title = self._sub_note_title_error(body["title"])
                    if bad_title is not None:
                        return bad_title
                # THE PRECONDITION, so this double matches the real route's
                # shape. A fake that accepts a stale base_version is not
                # evidence about a server that refuses one.
                if (
                    body.get("body") is not None
                    and body.get("base_version") is not None
                    and body["base_version"] != row["notes_version"]
                ):
                    return httpx.Response(
                        409,
                        json={
                            "detail": {
                                "message": "the document moved since you read it",
                                "notes_version": row["notes_version"],
                            }
                        },
                    )
                # ATOMIC like the real route: rename + verb run in one
                # transaction, so a refused verb rolls the rename back with it.
                before = (row["title"], row["updated_at"])
                if body.get("title") is not None:
                    title = body["title"].strip()
                    if title != row["title"]:
                        row["title"] = title
                        row["updated_at"] = self._sub_note_tick()
                refusal = self._apply_sub_note_verb(row, body, cap)
                if refusal is not None:
                    row["title"], row["updated_at"] = before
                    return refusal
                return httpx.Response(200, json=self._sub_note_meta(row, cap))
            if method == "DELETE":
                del self.sub_notes[row["id"]]
                return httpx.Response(204)

        if path == "/v1/notes" and method == "GET":
            include_sub_notes = request.url.params.get("include_sub_notes") == "true"
            catalog = self._notes_catalog(include_sub_notes)
            query = request.url.params.get("query")
            if query is not None:
                # LITERAL and case-insensitive over the row's text and its
                # ancestry, like the real search (never a wildcard).
                needle = query.lower()
                catalog["items"] = [
                    item
                    for item in catalog["items"]
                    if needle in item["title"].lower()
                    or needle in item["excerpt"].lower()
                    or any(needle in a["title"].lower() for a in item.get("ancestors") or [])
                ]
            if request.url.params.get("limit") is not None:
                # A limit selects the FLAT listing, paged exactly as
                # app/notes_catalog/service.py pages it: entity rows newest first
                # by (created_at, kind_rank, id) with a one-row lookahead, the
                # cursor base64 of `<created_at>|<kind_rank>|<id>`, and the team
                # note on the FIRST page only, outside the page's budget. (A
                # cursor the catalog already carries -- a test forcing "there is
                # more" -- is kept.)
                limit = int(request.url.params["limit"])
                team = [i for i in catalog["items"] if i["kind"] == "team_note"]
                rows = sorted(
                    (i for i in catalog["items"] if i["kind"] in _NOTE_KIND_RANK),
                    key=lambda i: (
                        _keyset_time(i.get("created_at")),
                        _NOTE_KIND_RANK[i["kind"]],
                        str(i["id"]),
                    ),
                    reverse=True,
                )
                cursor = request.url.params.get("cursor")
                if cursor:
                    try:
                        at, rank, rid = (
                            base64.urlsafe_b64decode(cursor.encode()).decode().split("|", 2)
                        )
                        key = (_keyset_time(at), int(rank), rid)
                    except (ValueError, UnicodeDecodeError):
                        return httpx.Response(422, json={"detail": "malformed notes cursor"})
                    rows = [
                        i
                        for i in rows
                        if (
                            _keyset_time(i.get("created_at")),
                            _NOTE_KIND_RANK[i["kind"]],
                            str(i["id"]),
                        )
                        < key
                    ]
                page = rows[:limit]
                next_cursor = catalog.get("next_cursor")
                if len(rows) > limit and page:
                    last = page[-1]
                    rank = _NOTE_KIND_RANK[last["kind"]]
                    next_cursor = base64.urlsafe_b64encode(
                        f"{last.get('created_at')}|{rank}|{last['id']}".encode()
                    ).decode()
                catalog = {"items": ([] if cursor else team) + page, "next_cursor": next_cursor}
            return httpx.Response(200, json=catalog)

        # -- the team note (0125) -----------------------------------------
        # SYNC is the agent write and behaves like the server's: a matching
        # base version applies, a stale one merges, and an identical body is a
        # no-op that mints no version. A fake that skipped the no-op would let a
        # retried reconcile pass here and mint duplicate versions in production.
        if path == "/v1/team-note" and method == "GET":
            return httpx.Response(200, json=dict(self.team_note))

        if path == "/v1/team-note/brief" and method == "GET":
            body = self.team_note["body"]
            return httpx.Response(
                200,
                json={
                    "text": body[:32000],
                    "truncated": len(body) > 32000,
                    "version": self.team_note["version"],
                    "read_all": "GET /v1/team-note",
                },
            )

        if path == "/v1/team-note/sync" and method == "POST":
            payload = json.loads(request.content or b"{}")
            body, base = payload["body"], payload["base_version"]
            current = self.team_note["body"]
            if any(
                line.startswith(("<<<<<<<", ">>>>>>>")) for line in body.splitlines()
            ):
                return httpx.Response(
                    422, json={"detail": {"message": "conflict markers", "marker_lines": [1]}}
                )
            if body == current:
                return httpx.Response(
                    200,
                    json={
                        "state": "unchanged",
                        "version": self.team_note["version"],
                        "remaining_chars": 100_000 - len(current),
                        "merged": False,
                    },
                )
            if base != self.team_note["version"]:
                if self.sync_conflict:
                    return httpx.Response(
                        409,
                        json={
                            "detail": {
                                "message": "conflicting edits",
                                "current_version": self.team_note["version"],
                                "conflict_count": 1,
                                "merged_body": (
                                    "<<<<<<< your local edit\n" + body + "=======\n"
                                    + current + ">>>>>>> the team note on the server\n"
                                ),
                            }
                        },
                    )
                body = current.rstrip("\n") + "\n\n" + body  # a clean server-side merge
            self.team_note["body"] = body
            self.team_note["version"] += 1
            self.team_note["remaining_chars"] = 100_000 - len(body)
            self.team_note_versions.append(
                {"version": self.team_note["version"], "body": body}
            )
            return httpx.Response(
                200,
                json={
                    "state": "applied",
                    "version": self.team_note["version"],
                    "remaining_chars": self.team_note["remaining_chars"],
                    "body": body,
                    "merged": body != payload["body"],
                },
            )

        if path in ("/v1/team-note/apply/paragraph", "/v1/team-note/apply/span") and (
            method == "POST"
        ):
            # The server-computed writes (app/team_notes/service.py): read,
            # change and store under the row lock, so no version is sent.
            payload = json.loads(request.content or b"{}")
            current = self.team_note["body"]
            if path.endswith("/paragraph"):
                text = payload.get("text") or ""
                if not text or len(text) > 8_192:
                    return httpx.Response(422, json={"detail": "text must be 1..8192 characters"})
                # `_topped_up`: the stored text right-stripped, a blank line,
                # the paragraph stripped, one trailing newline.
                body = (
                    f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else f"{text.strip()}\n"
                )
            else:
                old_text, new_text = payload.get("old_text") or "", payload.get("new_text", "")
                matches = current.count(old_text) if old_text else 0
                if matches != 1:
                    return httpx.Response(
                        409,
                        json={
                            "detail": {
                                "message": (
                                    "`old_text` must match exactly once; add surrounding "
                                    "context to make it unique, or re-read the document if "
                                    "it matched nothing."
                                ),
                                "match_count": matches,
                            }
                        },
                    )
                body = current.replace(old_text, new_text, 1)
            if len(body) > 100_000:
                return httpx.Response(
                    422,
                    json={
                        "detail": (
                            "the result would exceed the 100000-character team note limit. "
                            "Compact the document first."
                        )
                    },
                )
            self.team_note["body"] = body
            self.team_note["version"] += 1
            self.team_note["remaining_chars"] = 100_000 - len(body)
            self.team_note_versions.append({"version": self.team_note["version"], "body": body})
            return httpx.Response(
                200,
                json={
                    "state": "applied",
                    "version": self.team_note["version"],
                    "remaining_chars": self.team_note["remaining_chars"],
                    "merged": False,
                },
            )

        if path == "/v1/team-note/versions" and method == "GET":
            # Honours `limit`/`before` and emits `next_before` with the SAME
            # over-fetch-by-one rule as service.list_versions. A fake that
            # ignored them would let an SDK paging test pass while walking one
            # page and stopping -- which is the bug the real cursor exists to
            # prevent, so the fake has to be able to fail it.
            params = request.url.params
            limit = int(params.get("limit") or 25)
            before = params.get("before")
            newest_first = [
                {
                    "version": v["version"],
                    "created_at": None,
                    "created_by": "",
                    "size_chars": len(v["body"]),
                }
                for v in reversed(self.team_note_versions)
                if before is None or v["version"] < int(before)
            ]
            page = newest_first[:limit]
            more = len(newest_first) > limit
            return httpx.Response(
                200,
                json={
                    "versions": page,
                    "read_one": "GET /v1/team-note/versions/{version}",
                    "next_before": page[-1]["version"] if more and page else None,
                },
            )

        m = re.match(r"^/v1/team-note/versions/(\d+)$", path)
        if m and method == "GET":
            wanted = int(m.group(1))
            for v in self.team_note_versions:
                if v["version"] == wanted:
                    return httpx.Response(
                        200,
                        json={
                            "body": v["body"],
                            "version": wanted,
                            "remaining_chars": 100_000 - len(v["body"]),
                        },
                    )
            return httpx.Response(404, json={"detail": "no such version"})

        # -- captured coding-agent sessions (read-only, like the real routes) --
        m = re.match(r"^/v1/sessions/([^/]+)/(work|transcript|digest)$", path)
        if m and method == "GET":
            sid, leaf = m.group(1), m.group(2)
            if self.sessions_route_absent:
                return httpx.Response(404, json={"detail": "Not Found"})
            if leaf == "work":
                # An unknown well-formed id answers EMPTY, never 404 — the real
                # route refuses to be an oracle for another product's ids.
                work = self.session_work.get(sid) or {
                    "session_id": sid,
                    "agent": None,
                    "name": None,
                    "device_label": None,
                    "device_hostname": None,
                    "projects": [],
                    "experiments": [],
                    "runs": [],
                    "artifacts": [],
                }
                return httpx.Response(200, json=work)
            if leaf == "transcript":
                source = request.url.params.get("source", "claude_code")
                doc = self.session_transcripts.get((sid, source))
                if doc is None:
                    return httpx.Response(404, json={"detail": "transcript not found"})
                return httpx.Response(200, json=doc)
            digest = self.session_digests.get(sid)
            if digest is None:
                return httpx.Response(404, json={"detail": "no digest for this session"})
            return httpx.Response(200, json=digest)

        if path == "/v1/sql" and method == "POST":
            # Schema discovery only: a fake has no database to run SQL against.
            # Execution, RLS and limits are proven against real Postgres in
            # research-os tests/integration/test_sql_route.py.
            return httpx.Response(
                200,
                json={
                    "database": "experiment",
                    "tables": [{"name": "runs"}, {"name": "experiments"}],
                    "max_rows": 500,
                    "timeout_seconds": 5,
                },
            )
        if path == "/v1/search" and method == "POST":
            self.search_requests.append(body)
            if self.search_404_once:
                self.search_404_once = False
                return httpx.Response(404, json={"detail": "Not Found"})
            if body.get("workspace_id") in self.search_404_workspace_ids:
                return httpx.Response(404, json={"detail": "not found"})
            # The backend's `require_project` shape: the ROUTE answers, and 404s
            # only the scope. Distinct from `search_response is None`, which
            # models the route itself being absent.
            if body.get("project_id") in self.search_404_project_ids:
                return httpx.Response(404, json={"detail": "not found"})
            if self.search_responses:
                return httpx.Response(
                    200, json=self._echo_scope(self.search_responses.pop(0), body)
                )
            if self.search_response is None:
                return httpx.Response(404, json={"detail": "Not Found"})
            return httpx.Response(200, json=self._echo_scope(self.search_response, body))

        # -- the open web (POST /v1/web/*) ------------------------------------
        # Answered by default, unlike /v1/search above, and for the opposite
        # reason: an unconfigured deployment 503s rather than 404s, so "the
        # route is absent" is not a state this family has. A test wanting the
        # door shut sets `web_status` and gets the 503 a real one sends.
        if path.startswith("/v1/web/") and method == "POST":
            self.web_requests.append((path, body))
            if self.web_status is not None:
                return httpx.Response(self.web_status, json={"detail": self.web_detail})
            kind = path.rsplit("/", 1)[-1]
            if self.web_responses.get(kind) is not None:
                return httpx.Response(200, json=self.web_responses[kind])
            if kind == "search":
                return httpx.Response(200, json={"query": body.get("query"), "state": "empty"})
            if kind == "papers":
                return httpx.Response(200, json={"mode": body.get("mode"), "state": "empty"})
            return httpx.Response(
                200, json={"url": body.get("url"), "state": "ok", "text": "", "truncated": False}
            )
        # -- tokens (mint is session-only, so it is NOT routed here: the CLI mints
        # via the device flow, which tests/test_device_login.py covers) --
        if path == "/v1/tokens" and method == "GET":
            return httpx.Response(200, json=list(self.tokens.values()))
        m = re.match(r"^/v1/tokens/([^/]+)$", path)
        if m and method == "DELETE":
            tid = m.group(1)
            if tid not in self.tokens:
                return httpx.Response(404, json={"detail": "token not found"})
            self.tokens.pop(tid)
            return httpx.Response(204)

        if path == "/v1/projects" and method == "POST":
            existing = next(
                (row for row in self.projects.values() if row["slug"] == body["slug"]),
                None,
            )
            if existing:
                return httpx.Response(
                    409,
                    json={
                        "detail": {
                            "message": "slug exists",
                            "existing_id": existing["id"],
                        }
                    },
                )
            workspace_id = body.get("workspace_id")
            if workspace_id is None:
                parent = self.projects.get(body.get("parent_project_id"))
                workspace_id = (
                    parent["workspace_id"] if parent is not None else self._default_workspace_id()
                )
            pid = str(uuid.uuid4())
            row = {
                "id": pid,
                "slug": body["slug"],
                # 0095 + 0170: the STORED name never holds the slug, and a read
                # falls back to it -- so the response is always a string while
                # `name_customized` is what says whether anyone chose it.
                "name": _chosen_name(body.get("name"), body["slug"]) or body["slug"],
                "name_customized": _owns_field(
                    _chosen_name(body.get("name"), body["slug"]), body.get("authored_by")
                ),
                "customer_id": "lab-42",
                "workspace_id": workspace_id,
                "description": body.get("description"),
                "document": body.get("document"),
                "metadata": body.get("metadata") or {},
                # 0148/0149: the fields the tree + kind surfaces write.
                "parent_project_id": body.get("parent_project_id"),
                "kind": body.get("kind", "general"),
                "created_at": _T0,
            }
            self.projects[pid] = row
            return httpx.Response(201, json=row)

        if path == "/v1/projects" and method == "GET":
            rows = list(self.projects.values())
            wanted = request.url.params.get("workspace_id")
            if wanted:
                rows = [r for r in rows if r.get("workspace_id") == wanted]
            # Exact slug lookup, mirroring the engine: this is what lets a client
            # RESOLVE a slug without being able to create one.
            slug = request.url.params.get("slug")
            if slug:
                rows = [r for r in rows if r.get("slug") == slug]
            # Exact, case-insensitive -- mirrors the engine's ?name= filter. A fake
            # that ignored it would make every `name:` assertion pass against an
            # unfiltered page, which is the drop the client guards against.
            name = request.url.params.get("name")
            if name:
                rows = [r for r in rows if str(r.get("name", "")).lower() == name.lower()]
            # Direct children only (0148). A fake that ignored this would look
            # exactly like the pre-0148 backend the client guards against, so
            # every subproject assertion would pass against an unfiltered page.
            parent_id = request.url.params.get("parent_id")
            if parent_id:
                rows = [r for r in rows if r.get("parent_project_id") == parent_id]
            return httpx.Response(200, json=rows)

        m = _PROJ_ITEM.match(path)
        if m and method == "DELETE":
            pid = m.group(1)
            if pid not in self.projects:
                return httpx.Response(404, json={"detail": "not found"})
            # Mirrors the engine cascade (0080): the tree goes with the project.
            doomed = {eid for eid, e in self.experiments.items() if e.get("project_id") == pid}
            for rid in [
                rid
                for rid, r in self.runs.items()
                if r.get("project_id") == pid or r.get("experiment_id") in doomed
            ]:
                self.runs.pop(rid)
            for eid in doomed:
                self.experiments.pop(eid)
            self.projects.pop(pid)
            return httpx.Response(204)

        m = _PROJ_ITEM.match(path)
        if m and method == "GET":
            pid = m.group(1)
            if pid not in self.projects:
                return httpx.Response(404, json={"detail": "not found"})
            # 0153: the reference edges ride the DETAIL read, so they are
            # merged here rather than served from a route of their own.
            detail = dict(self.projects[pid])
            refs = self.project_references.get(pid)
            if refs is not None:
                detail["references"] = refs
            return httpx.Response(200, json=detail)

        m = _PROJ_ITEM.match(path)
        if m and method == "PATCH":
            pid = m.group(1)
            if pid not in self.projects:
                return httpx.Response(404, json={"detail": "not found"})
            row = self.projects[pid]
            if "workspace_id" in body:
                dest = body["workspace_id"]
                if dest not in self.workspaces:
                    # A rejected VALUE, not a missing resource: 422, never 404.
                    return httpx.Response(422, json={"detail": "unknown workspace"})
                # Fan out to descendants ONLY when the workspace actually changes —
                # their documents denormalize workspace_id, so they must reproject.
                if row.get("workspace_id") != dest:
                    row["workspace_id"] = dest
                    for eid, exp in self.experiments.items():
                        if exp.get("project_id") == pid:
                            self.reindexed.append(eid)
                    for rid, run in self.runs.items():
                        if run.get("project_id") == pid:
                            self.reindexed.append(rid)
            # 0148: THE one explicit-null field — presence in the body is the
            # signal, exactly like the real route's model_fields_set check.
            if "parent_project_id" in body:
                row["parent_project_id"] = body["parent_project_id"]
            if body.get("kind") is not None:
                row["kind"] = body["kind"]
            for field in ("name", "description", "document", "metadata"):
                if body.get(field) is not None:
                    row[field] = body[field]
            if body.get("tags") is not None:
                # Whole-list replace (0066), canonicalized as the server does.
                row["tags"] = _canonical_tags(body["tags"])
            # Gated so the fake can be a backend on EITHER side of research-os
            # 0094: ProjectPatch does not forbid extra fields, so a pre-0094
            # server takes `notes`, ignores it, and answers 200 -- the write
            # vanishes and the caller is told it worked. Being able to be both is
            # the only way to test that the client notices (same shape as
            # `echoes_project_scope`).
            refused = self._apply_notes_write(
                row, body, self.document_notes_cap, stores=self.stores_project_notes
            )
            if refused is not None:
                return refused
            return httpx.Response(200, json=row)

        # -- workspaces --
        if path == "/v1/workspaces" and method == "POST":
            slug = (body or {}).get("slug") or ""
            existing = next(
                (w for w in self.workspaces.values() if w.get("slug") == slug), None
            )
            if existing is not None:
                return httpx.Response(
                    409,
                    json={
                        "detail": {
                            "message": "workspace with this slug already exists",
                            "existing_id": existing["id"],
                            "suggestion": f"{slug}-2",
                        }
                    },
                )
            # Team kind, no owner: the route mints nothing else.
            row = {
                "id": str(uuid.uuid4()),
                "customer_id": "lab-42",
                "name": (body or {}).get("name") or slug,
                "slug": slug,
                "kind": "team",
                "owner_user_id": None,
                "project_count": 0,
                "created_at": self._stamp(),
            }
            self.workspaces[row["id"]] = row
            return httpx.Response(201, json=row)

        if path == "/v1/workspaces" and method == "GET":
            # Server order does not depend on the caller or historical kind:
            # `ORDER BY lower(name), id` under the C collation, whose lower()
            # folds ASCII letters only.
            rows = sorted(
                self.workspaces.values(),
                key=getattr(self, "workspace_sort", None)
                or (
                    lambda w: (
                        (w.get("name") or "").translate(_ASCII_LOWER),
                        w["id"],
                    )
                ),
            )
            for row in rows:
                row["project_count"] = sum(
                    1 for p in self.projects.values() if p.get("workspace_id") == row["id"]
                )
            return httpx.Response(200, json=rows)

        m = _WS_ITEM.match(path)
        if m and method == "GET":
            wid = m.group(1)
            if wid not in self.workspaces:
                return httpx.Response(404, json={"detail": "not found"})
            return httpx.Response(200, json=self.workspaces[wid])

        m = _WS_ITEM.match(path)
        if m and method == "PATCH":
            wid = m.group(1)
            if wid not in self.workspaces:
                return httpx.Response(404, json={"detail": "not found"})
            name = (body.get("name") or "").strip()
            if not name:
                return httpx.Response(422, json={"detail": "name must not be blank"})
            self.workspaces[wid]["name"] = name
            return httpx.Response(200, json=self.workspaces[wid])

        m = _WS_ITEM.match(path)
        if m and method == "DELETE":
            wid = m.group(1)
            row = self.workspaces.get(wid)
            if row is None:
                return httpx.Response(404, json={"detail": "workspace not found"})
            filed = sum(
                1 for p in self.projects.values() if p.get("workspace_id") == wid
            )
            files = sum(
                1
                for artifact in self.artifacts.get(f"workspace:{wid}", [])
                if artifact.get("deleted_at") is None and artifact.get("status") == "complete"
            )
            if filed or files:
                return httpx.Response(
                    409,
                    json={"detail": f"workspace is not empty ({filed} project(s), {files} file(s))"},
                )
            del self.workspaces[wid]
            return httpx.Response(204)

        if path == "/v1/experiments" and method == "POST":
            if not (body or {}).get("project_id"):
                return httpx.Response(
                    422, json={"detail": [{"loc": ["body", "project_id"], "type": "missing"}]}
                )
            # Mirror the projects handler and the real UNIQUE (customer_id, slug):
            # without this the fake happily mints duplicate identities, so
            # `create_experiment` never conflicts and a regression that put the
            # POST-then-swallow-409 back inside run() would leave the suite green.
            for _row in self.experiments.values():
                if _row.get("slug") == (body or {}).get("slug"):
                    return httpx.Response(
                        409,
                        json={
                            "detail": {
                                "message": "experiment with this slug already exists",
                                "existing_id": _row["id"],
                            }
                        },
                    )
            if self.experiment_conflict_id:
                return httpx.Response(
                    409,
                    json={
                        "detail": {
                            "message": "slug exists",
                            "existing_id": self.experiment_conflict_id,
                        }
                    },
                )
            eid = str(uuid.uuid4())
            row = {
                "id": eid,
                "slug": body["slug"],
                # Same rule as projects; `name` is OPTIONAL server-side since
                # 0095 and this used to KeyError on a body that omitted it.
                "name": _chosen_name(body.get("name"), body["slug"]) or body["slug"],
                "name_customized": _owns_field(
                    _chosen_name(body.get("name"), body["slug"]), body.get("authored_by")
                ),
                "question": body["question"],
                "description": body.get("description"),
                "document": body.get("document"),
                "project_id": body.get("project_id") or str(uuid.uuid4()),
                "customer_id": "lab-42",
                "created_at": self._stamp(),
            }
            self.experiments[eid] = row
            return httpx.Response(201, json=row)

        if path == "/v1/experiments" and method == "GET":
            rows = list(self.experiments.values())
            project_id = request.url.params.get("project_id")
            if project_id:
                rows = [row for row in rows if row.get("project_id") == project_id]
            # Exact slug lookup, mirroring the engine (see the projects handler).
            slug = request.url.params.get("slug")
            if slug:
                rows = [row for row in rows if row.get("slug") == slug]
            # Exact, case-insensitive -- mirrors the engine's ?name= filter. A fake
            # that ignored it would make every `name:` assertion pass against an
            # unfiltered page, which is the drop the client guards against.
            name = request.url.params.get("name")
            if name:
                rows = [row for row in rows if str(row.get("name", "")).lower() == name.lower()]
            return httpx.Response(200, json=rows)

        if path == "/v1/runs" and method == "POST":
            # Daemon v2 FLOATING run: the project-direct body, no project at all.
            # A backend predating it has GET /v1/runs only, so POST is a 405.
            if not self.supports_floating:
                return httpx.Response(405, json={"detail": "Method Not Allowed"})
            if body.get("group_id") is not None:
                return httpx.Response(
                    422, json={"detail": "group_id requires an experiment-attached run"}
                )
            replay = self._creation_replay(path, body)
            if replay is not None:
                return replay
            conflict = self._run_external_id_conflict(body)
            if conflict is not None:
                return conflict
            rid = str(uuid.uuid4())
            row = self._new_run(rid, None, body, floating=True)
            self._remember_creation(path, body, rid)
            return httpx.Response(201, json=row)

        if path == "/v1/runs" and method == "GET":
            rows = list(self.runs.values())
            params = request.url.params
            if params.get("unfiled") == "true" and self.supports_floating:
                # The caller's floating runs (the fake has one caller).
                rows = [row for row in rows if row.get("project_id") is None]
            elif (
                self.supports_floating
                and not params.get("experiment_id")
                and not params.get("project_id")
                and not params.get("name")
                and not params.get("foreign_key")
            ):
                # 0260, app/runs/service.py `fetch_runs_page`: an unscoped
                # BROWSE holds filed runs only; an identity lookup (name /
                # foreign_key) still sees unfiled ones.
                rows = [row for row in rows if row.get("project_id") is not None]
            # Exact, case-insensitive -- mirrors the engine's ?name= filter.
            name = request.url.params.get("name")
            if name:
                rows = [row for row in rows if str(row.get("name", "")).lower() == name.lower()]
            experiment_id = request.url.params.get("experiment_id")
            if experiment_id:
                rows = [row for row in rows if row.get("experiment_id") == experiment_id]
            status = request.url.params.get("status")
            if status:
                rows = [row for row in rows if row.get("status") == status]
            if request.url.params.get("active") == "true":
                # Effectively live: stored running AND inside the liveness
                # window. The fake marks a stale heartbeat with `_stale`.
                rows = [
                    row for row in rows if row.get("status") == "running" and not row.get("_stale")
                ]
            wanted_tags = request.url.params.get_list("tags")
            if wanted_tags:
                rows = [row for row in rows if set(wanted_tags) <= set(row.get("tags") or [])]
            if self.supports_project_direct:
                # project_id (0054): ALL of a project's runs — direct AND attached.
                project_id = request.url.params.get("project_id")
                if project_id:
                    rows = [row for row in rows if row.get("project_id") == project_id]
                if request.url.params.get("direct") == "true":
                    rows = [row for row in rows if not row.get("experiment_id")]
            else:
                # Pre-0054: unknown params are ignored, rows have no project_id.
                rows = [{k: v for k, v in row.items() if k != "project_id"} for row in rows]
            # Page it EXACTLY like the real endpoint (app/core/pagination.py):
            # newest first by (created_at, id), limit defaulting to 50 and capped
            # at 200, and the KEYSET cursor -- base64 of `<created_at>|<id>`,
            # meaning "rows strictly before this one" -- named whenever a page
            # comes back full. An offset cursor here let a client that resumed
            # by counting rows pass, while production resumes by key.
            rows.sort(
                key=lambda row: (_keyset_time(row.get("created_at")), row["id"]), reverse=True
            )
            limit = min(int(params.get("limit") or 50), 200)
            if cursor := params.get("cursor"):
                try:
                    raw = base64.urlsafe_b64decode(cursor.encode()).decode()
                    at, _, rid = raw.partition("|")
                    uuid.UUID(rid)
                    key = (_keyset_time(at), rid)
                except (ValueError, UnicodeDecodeError):
                    return httpx.Response(422, json={"detail": "malformed pagination cursor"})
                rows = [
                    row
                    for row in rows
                    if (_keyset_time(row.get("created_at")), row["id"]) < key
                ]
            else:
                rows = rows[int(params.get("offset") or 0) :]
            window = rows[:limit]
            headers = {}
            if window and len(window) == limit:
                last = window[-1]
                headers["x-next-cursor"] = base64.urlsafe_b64encode(
                    f"{last.get('created_at')}|{last['id']}".encode()
                ).decode()
            return httpx.Response(200, json=window, headers=headers)

        m = _EXP_ITEM.match(path)
        if m and method == "GET":
            eid = m.group(1)
            return httpx.Response(
                200,
                json=self.experiments.get(
                    eid, {"id": eid, "question": "h", "project_id": str(uuid.uuid4())}
                ),
            )
        if m and method == "PATCH":
            eid = m.group(1)
            row = self.experiments.get(eid)
            if row is None:
                return httpx.Response(404, json={"detail": "not found"})
            refused = self._apply_notes_write(row, body, self.document_notes_cap)
            if refused is not None:
                return refused
            row.update({k: v for k, v in body.items() if k not in self.NOTES_WRITE_FIELDS})
            return httpx.Response(200, json=row)

        m = _TRIAL_ITEM.match(path)
        if m and method in ("GET", "PATCH"):
            trial_id = m.group(1)
            row = self.trials.get(trial_id)
            if row is None:
                return httpx.Response(404, json={"detail": "trial not found"})
            if method == "PATCH":
                refused = self._apply_notes_write(
                    row, body, self.entity_notes_cap, stores=self.stores_entity_notes
                )
                if refused is not None:
                    return refused
                row.update(
                    {
                        key: value
                        for key, value in body.items()
                        if value is not None and key not in self.NOTES_WRITE_FIELDS
                    }
                )
            return httpx.Response(200, json=row)

        if path == "/v1/server/features" and method == "GET":
            # 0185 capability preflight. A pre-rewind server has no such
            # route: FastAPI's route-level 404.
            if not self.supports_rewind:
                return httpx.Response(404, json={"detail": "Not Found"})
            features = ["run_rewind", "write_epoch_fencing"]
            if self.supports_run_inputs:
                features.append("run_inputs")
            if self.supports_run_outputs:
                features.append("run_outputs")
            if self.supports_trash:
                features.append("trash")
            if self.supports_keep_epoch:
                features.append("run_reopen_keep_epoch")
            if self.supports_config_merge:
                features.append("run_config_merge")
            if self.supports_creation_key:
                features.append("run_creation_key")
            if self.supports_takeover:
                features.append("run_reopen_takeover")
            if self.supports_run_log_stream:
                features.append("run_log_stream")
            if self.supports_offline_create:
                features.append("run_offline_create")
            if self.supports_writer_gone:
                features.append("run_writer_gone")
            if self.supports_leases:
                features.append("run_writer_leases")
            if self.supports_artifact_multipart:
                features.append("artifact_multipart")
            return httpx.Response(200, json={"features": features})

        if path.startswith("/v1/runs/") and "/artifacts/multipart" in path:
            return self._multipart(method, path, body)
        if path.startswith("/part/") and method == "PUT":
            return self._multipart_put(path, request)

        m = re.fullmatch(r"/v1/runs/([^/]+)/log-chunks", path)
        if m and method == "POST":
            # 0270: the server's contract (app/runs/log_chunks.py): idempotent
            # by position -- a chunk whose offset is already covered stores
            # nothing and answers where the stream continues.
            if not self.supports_run_log_stream:
                return httpx.Response(404, json={"detail": "Not Found"})
            self.log_chunk_posts.append(dict(body))
            if self.log_chunk_failures:
                self.log_chunk_failures -= 1
                return httpx.Response(503, json={"detail": "object storage is unavailable"})
            if self.log_chunk_throttled:
                self.log_chunk_throttled -= 1
                wait = self.log_chunk_retry_after
                return httpx.Response(
                    429,
                    headers={"Retry-After": str(wait)},
                    json={"detail": {"message": "too many log chunks", "code": "rate_limited", "retry_after": wait}},
                )
            rid = m.group(1)
            if rid not in self.runs:
                return httpx.Response(404, json={"detail": "run not found"})
            # The server's `check_epoch`: a chunk naming another attempt than
            # the run's current one is refused, with the same body.
            current = int(self.runs[rid].get("write_epoch") or 1)
            if body.get("write_epoch") is not None and int(body["write_epoch"]) != current:
                return httpx.Response(
                    409,
                    json={
                        "detail": {
                            "message": "stale write_epoch: this run was reopened by a newer attempt",
                            "code": "stale_write_epoch",
                            "write_epoch": current,
                        }
                    },
                )
            chunks = self.log_chunks.setdefault(rid, {})
            stream, offset, length = body["stream"], int(body["raw_offset"]), int(body["raw_len"])
            covering = next(
                (
                    (o, c)
                    for (s_, o), c in sorted(chunks.items(), key=lambda kv: (kv[0][1] != offset, kv[0][1]))
                    if s_ == stream and o < offset + length and o + int(c["raw_len"]) > offset
                ),
                None,
            )
            if covering is not None:
                o, c = covering
                next_offset, stored = o + int(c["raw_len"]), False
            else:
                chunks[(stream, offset)] = dict(body)
                next_offset, stored = offset + length, True
            return httpx.Response(
                200,
                json={
                    "run_id": rid,
                    "write_epoch": int(self.runs[rid].get("write_epoch") or 1),
                    "stream": stream,
                    "stored": stored,
                    "next_offset": next_offset,
                },
            )

        m = re.fullmatch(r"/v1/artifacts/([^/]+)/lineage", path)
        if m and method == "GET":
            # 0255: which run wrote the file and which runs read it. The fake
            # keeps no reads, so every file here has no readers. `origin` (L18):
            # the run holding it, the one writer the fake knows.
            aid = m.group(1)
            row = next(
                (a for rows in self.artifacts.values() for a in rows if str(a.get("id")) == aid),
                None,
            )
            holder = (row or {}).get("run_id")
            return httpx.Response(200, json={
                "artifact_id": aid,
                "name": (row or {}).get("name", aid),
                "run": None,
                "written_by_run": False,
                "readers": [],
                "origin": (
                    {"type": "run", "id": holder, "via": "lineage", "relation": "produces"}
                    if holder else None
                ),
            })

        # Lineage plan 2 (L12/L18): a project's or experiment's OWN lineage. An
        # experiment arrives here at its legacy address (`_experiment_alias`).
        m = re.fullmatch(r"/v1/(projects|experiments)/([^/]+)/lineage", path)
        if m and method == "GET":
            return self._project_lineage(m.group(2), int(request.url.params.get("limit", 200)))

        m = re.fullmatch(r"/v1/runs/([^/]+)/upstream", path)
        if m and method == "GET":
            rid = m.group(1)
            return httpx.Response(200, json={
                "run_id": rid,
                "depth": int(request.url.params.get("depth", 2)),
                "runs": [{"id": rid, "depth": 0}],
                "edges": [],
                "truncated": False,
            })

        m = re.fullmatch(r"/v1/runs/([^/]+)/inputs", path)
        if m and method == "POST" and self.supports_run_inputs:
            batch = body or {}
            self.__dict__.setdefault("run_inputs", {}).setdefault(m.group(1), []).append(batch)
            return httpx.Response(
                201,
                json={"run_id": m.group(1), "received": len(batch.get("inputs", [])),
                      "stored": len(batch.get("inputs", []))},
            )

        m = re.fullmatch(r"/v1/runs/([^/]+)/outputs", path)
        if m and method == "POST" and self.supports_run_outputs:
            # The shared contract (lineage plan 3, F2b <-> F2c), checked
            # EXACTLY: a body the real server would refuse fails here too.
            batch = body or {}
            problems = run_outputs_problems(batch)
            if problems:
                return httpx.Response(422, json={"detail": problems})
            self.__dict__.setdefault("run_outputs", {}).setdefault(m.group(1), []).append(batch)
            return httpx.Response(
                201, json={"accepted": len(batch.get("outputs", [])), "truncated": False}
            )

        m = re.fullmatch(r"/v1/runs/([^/]+)/writers/([^/]+)/(beat|release)", path)
        if m and method == "POST":
            # 2.8, mirroring app/runs/router.py (beat_writer / release_writer).
            if not self.supports_leases:
                return httpx.Response(404, json={"detail": "Not Found"})
            rid, session, verb = m.group(1), m.group(2), m.group(3)
            row = self.runs.get(rid)
            if row is None:
                return httpx.Response(404, json={"detail": "run not found"})
            epoch = int((body or {}).get("write_epoch") or 1)
            if epoch < int(row.get("write_epoch", 1)):
                self.fenced_writes.append({"path": path, "carried": epoch})
                return httpx.Response(
                    409, json={"detail": {"message": "superseded", "existing_id": rid}}
                )
            protocol = "leases" if row.get("liveness_protocol") == "leases" else "legacy"
            if verb == "beat":
                lease = self._upsert_lease(rid, body or {}, epoch=epoch, session=session)
                state = "live"
                if lease is None:
                    held = self.leases.get(rid, {}).get(session) or {}
                    state = "gone" if held.get("gone_at") else "released"
                return httpx.Response(
                    200,
                    json={
                        "run_status": row["status"],
                        "write_epoch": int(row.get("write_epoch", 1)),
                        "liveness_protocol": protocol,
                        "lease": state,
                    },
                )
            self.lease_releases.append({"run_id": rid, "session_id": session, "body": body})
            lease = self.leases.get(rid, {}).get(session)
            status = (body or {}).get("exit_status")
            released_role = None
            if lease is None and (body or {}).get("writer"):
                # A release names its writer: a lease no beat registered counts.
                lease = self._upsert_lease(rid, body["writer"], epoch=epoch, session=session)
                lease["released_at"] = self._stamp()
                lease["exit_status"] = status
                released_role = lease.get("role")
            elif lease is None:
                return httpx.Response(404, json={"detail": "this session holds no lease"})
            elif not lease["released_at"] and not lease["gone_at"]:
                lease["released_at"] = self._stamp()
                lease["exit_status"] = status
                released_role = lease.get("role")
            reclosable = row.get("status") == "running" or (
                row.get("status") == "crashed" and released_role is not None
            )
            closed = False
            if protocol != "leases":
                # Not `leases` (NULL, flipped): an owner's or launcher's release
                # closes the run with its verdict, as its status PATCH did.
                if reclosable and released_role in ("owner", "launcher") and row["status"] != status:
                    row["status"] = status
                    row["ended_at"] = self._stamp()
                    closed = True
            elif reclosable:
                closed = self._close_by_leases(rid, allow_crashed=True)
            return httpx.Response(
                200,
                json={"run_status": row["status"], "closed": closed, "liveness_protocol": protocol},
            )

        m = re.fullmatch(r"/v1/runs/([^/]+)/writers", path)
        if m and method == "GET":
            return httpx.Response(200, json=list(self.leases.get(m.group(1), {}).values()))

        m = re.fullmatch(r"/v1/runs/([^/]+)/writer-gone", path)
        if m and method == "POST":
            # 2.2, mirroring app/runs/router.py::writer_gone: crash only when
            # the report is the whole story; otherwise 200, applied false.
            if not self.supports_writer_gone:
                return httpx.Response(404, json={"detail": "Not Found"})
            row = self.runs.get(m.group(1))
            if row is None:
                return httpx.Response(404, json={"detail": "run not found"})
            self.writer_gone_reports.append(dict(body or {}))
            if row.get("liveness_protocol") == "leases" and row.get("status") == "running":
                # 2.8: the reported session's lease is GONE; the closure rule
                # decides (crashed once nothing else is live).
                lease = self.leases.get(row["id"], {}).get(str((body or {}).get("session_id")))
                if lease is None or lease["released_at"] or lease["gone_at"]:
                    return httpx.Response(
                        200,
                        json={"run_id": row["id"], "applied": False, "status": row["status"],
                              "reason": "no_live_lease"},
                    )
                lease["gone_at"] = self._stamp()
                closed = self._close_by_leases(row["id"])
                if closed:
                    # As the server records it (reason `writer_gone` when a
                    # GONE is in the verdict), newest first.
                    self.run_events.setdefault(row["id"], []).insert(
                        0,
                        {
                            "event_type": "run.status_changed",
                            "subject_type": "run",
                            "subject_id": row["id"],
                            "payload": {"status": row["status"], "reason": "writer_gone"},
                        },
                    )
                return httpx.Response(
                    200,
                    json={"run_id": row["id"], "applied": closed, "status": row["status"],
                          "reason": row["status"] if closed else "other_writers_live"},
                )
            reason = None
            if row.get("status") != "running":
                reason = "not_running"
            elif int(row.get("write_epoch", 1)) != (body or {}).get("write_epoch"):
                reason = "stale_epoch"
            elif not (body or {}).get("sole_writer"):
                reason = "not_sole_writer"
            elif row.get("liveness_mode") != "in-process":
                reason = "not_in_process"
            elif row.get("attached_at") is not None:
                reason = "attached_writers"
            if reason is None:
                row["status"] = "crashed"
                row["ended_at"] = self._stamp()
                # Newest first, as GET /v1/runs/{id}/events orders them.
                self.run_events.setdefault(row["id"], []).insert(
                    0,
                    {
                        "event_type": "run.status_changed",
                        "subject_type": "run",
                        "subject_id": row["id"],
                        "payload": {
                            "status": "crashed",
                            "reason": "writer_gone",
                            "observed_by": (body or {}).get("observed_by"),
                        },
                    },
                )
            return httpx.Response(
                200,
                json={
                    "run_id": row["id"],
                    "applied": reason is None,
                    "status": row["status"],
                    "reason": reason or "crashed",
                },
            )

        m = _RUN_REOPEN.match(path)
        if m and method == "POST":
            if not self.supports_reopen:
                # Pre-#364: the route does not exist — FastAPI's route-level
                # 404, NOT the handler's "run not found".
                return httpx.Response(404, json={"detail": "Not Found"})
            row = self.runs.get(m.group(1))
            if row is None:
                return httpx.Response(404, json={"detail": "run not found"})
            rewind_to = (body or {}).get("rewind_to_step")
            if not self.supports_rewind:
                # Pre-0185 server: Pydantic drops the undeclared field — the
                # silent-ignore skew the SDK's preflight/echo exist to catch.
                rewind_to = None
            # Idempotent replay (0185): the session that already reopened gets
            # the current receipt back, no second epoch bump, no second delete.
            if row["status"] == "running" and row.get("current_session_id") == (
                body or {}
            ).get("session_id"):
                stored = self.metric_points.get(row["id"], []) + (
                    self.metric_points_posted.get(row["id"], [])
                )
                steps = [
                    p["step_index"] for p in stored if p.get("step_index") is not None
                ]
                receipt = {
                    "run": row,
                    "write_epoch": row.get("write_epoch", 1),
                    "last_step": max(steps) if steps else None,
                }
                if rewind_to is not None and self.supports_rewind_echo:
                    receipt |= {
                        "rewound_to": rewind_to,
                        "deleted_points": 0,
                        "deleted_spans": 0,
                    }
                return httpx.Response(200, json=receipt)
            # 2.3, mirroring app/runs/router.py: a running run is taken over
            # only once it has been silent for the asked threshold; until then
            # the 409 says how long to wait.
            takeover_after = (body or {}).get("takeover_stale_after_seconds")
            takeover = False
            cadence = False
            if (
                row["status"] == "running"
                and takeover_after is not None
                and self.supports_takeover
                and row.get("liveness_mode") == "offline"
                and not row.get("last_heartbeat_at")
            ):
                # Mirrors app/runs/router.py (0269): an offline run inside its
                # sync grace is never taken over (one that has a beat is not
                # being synced). This fake keeps no clock for a run's age, so
                # every offline run here is inside it.
                grace = 7 * 24 * 3600
                return httpx.Response(
                    409,
                    json={
                        "detail": {
                            "message": "run was recorded offline and is being delivered by "
                            f"`probe sync`; retry in {grace}s",
                            "existing_id": row["id"],
                            "retry_after_seconds": grace,
                        }
                    },
                    headers={"Retry-After": str(grace)},
                )
            if (
                row["status"] == "running"
                and takeover_after is not None
                and self.supports_takeover
                and row.get("liveness_protocol") == "leases"
            ):
                # 2.8: a leases run is taken over when no current-epoch lease
                # still BEATS (a draining or expired one does not count).
                epoch = int(row.get("write_epoch", 1))
                beating = [
                    w for w in self.leases.get(row["id"], {}).values()
                    if int(w["write_epoch"]) == epoch and not w["released_at"]
                    and not w["gone_at"] and not w.get("expired") and not w.get("draining")
                ]
                if beating:
                    return httpx.Response(
                        409,
                        json={
                            "detail": {
                                "message": "a writer still beats on a lease; retry in 180s",
                                "existing_id": row["id"],
                                "retry_after_seconds": 180,
                            }
                        },
                        headers={"Retry-After": "180"},
                    )
                takeover = True
            elif row["status"] == "running" and takeover_after is not None and self.supports_takeover:
                # A beating owner (a beat after the insert stamp: counted >= 2)
                # is judged by its beats; anything else waits the reaper's
                # 900 s on the reaper's clock.
                cadence = self.run_heartbeats.get(row["id"], 0) >= 2
                if cadence:
                    silent = self.run_beat_silence.get(row["id"], 0.0)
                    needed = float(takeover_after)
                else:
                    silent = self.run_silence.get(row["id"], 0.0)
                    needed = max(float(takeover_after), 900.0)
                if silent < needed:
                    retry_after = max(1, math.ceil(needed - silent))
                    return httpx.Response(
                        409,
                        json={
                            "detail": {
                                "message": f"run is running; retry in {retry_after}s",
                                "existing_id": row["id"],
                                "retry_after_seconds": retry_after,
                            }
                        },
                        headers={"Retry-After": str(retry_after)},
                    )
                takeover = True
            # Mirrors app/runs/router.py: dead statuses reopen; `completed`
            # additionally unlocks under an explicit rewind (0185).
            reopenable = ("failed", "crashed", "canceled", "untracked")
            allowed = (
                reopenable
                + (("completed",) if rewind_to is not None else ())
                + (("running",) if takeover else ())
            )
            if row["status"] not in allowed:
                return httpx.Response(
                    409,
                    json={
                        "detail": {"message": f"run is {row['status']}; only a dead run reopens"}
                    },
                )
            # 1.1: self-recovery keeps the generation, but only for a row the
            # reaper crashed while the caller's epoch is still the current one.
            # A server predating it drops both fields and bumps (below).
            keep = self.supports_keep_epoch and bool((body or {}).get("keep_epoch"))
            if keep and (
                row["status"] != "crashed"
                or (body or {}).get("expected_write_epoch") != row.get("write_epoch", 1)
            ):
                return httpx.Response(
                    409,
                    json={
                        "detail": {
                            "message": (
                                f"keep_epoch refused: run is {row['status']} on epoch "
                                f"{row.get('write_epoch', 1)}"
                            ),
                            "existing_id": row["id"],
                        }
                    },
                )
            deleted_points = 0
            if rewind_to is not None:
                for store in (self.metric_points, self.metric_points_posted):
                    kept = []
                    for point in store.get(row["id"], []):
                        step = point.get("step_index")
                        if (
                            step is not None
                            and step >= rewind_to
                            and point.get("kind", "model") != "hardware"
                        ):
                            deleted_points += 1
                        else:
                            kept.append(point)
                    if row["id"] in store:
                        store[row["id"]] = kept
            stored = self.metric_points.get(row["id"], []) + self.metric_points_posted.get(
                row["id"], []
            )
            steps = [p["step_index"] for p in stored if p.get("step_index") is not None]
            last_step = max(steps) if steps else None
            prior_status = row["status"]
            row["status"] = "running"
            row["ended_at"] = None
            if not keep:
                row["write_epoch"] = row.get("write_epoch", 1) + 1
            row["current_session_id"] = (body or {}).get("session_id")
            if (body or {}).get("writer") and row.get("liveness_protocol") == "leases":
                lease = self.leases.get(row["id"], {}).get(str(body["writer"]["session_id"]))
                if keep and lease is not None and lease["gone_at"] and not lease["released_at"]:
                    lease["gone_at"] = None  # the writer's own recovery revives it
                self._upsert_lease(row["id"], body["writer"], epoch=row["write_epoch"])
            # The reopen is substantive activity: `updated_at` moves.
            self.run_silence[row["id"]] = 0.0
            if row.get("liveness_mode") == "offline":
                # Mirrors app/runs/router.py (0269): any reopen is a new ONLINE
                # attempt (`probe sync` never reopens), so 'offline' goes.
                row["liveness_mode"] = None
            if takeover:
                # A takeover forgets the dead writer's attachment, and one of
                # a beating incumbent stamps a beat (a racing relaunch waits).
                row["attached_at"] = None
                row["liveness_mode"] = None
                if cadence:
                    self.run_beat_silence[row["id"]] = 0.0
                    self.run_heartbeats[row["id"]] = self.run_heartbeats.get(row["id"], 0) + 1
            row.setdefault("recoveries", []).append(
                {
                    "at": self._stamp(),
                    "prior_status": prior_status,
                    "last_step": last_step,
                    "session_id": row["current_session_id"],
                }
            )
            receipt = {
                "run": row,
                "write_epoch": row["write_epoch"],
                "last_step": last_step,
            }
            if rewind_to is not None and self.supports_rewind_echo:
                receipt |= {
                    "rewound_to": rewind_to,
                    "deleted_points": deleted_points,
                    "deleted_spans": 0,
                }
            return httpx.Response(200, json=receipt)

        m = _EXP_RUNS.match(path)
        if m and method == "POST":
            replay = self._creation_replay(path, body)
            if replay is not None:
                return replay
            conflict = self._run_external_id_conflict(body)
            if conflict is not None:
                return conflict
            rid = str(uuid.uuid4())
            eid = m.group(1)
            # Mirror the engine: an attached run inherits ITS EXPERIMENT'S
            # project (0054).
            row = self._new_run(
                rid,
                eid,
                body,
                project_id=(self.experiments.get(eid) or {}).get("project_id"),
            )
            self._remember_creation(path, body, rid)
            return httpx.Response(201, json=row)

        m = _PROJ_RUNS.match(path)
        if m and method == "POST":
            if not self.supports_project_direct:
                # Pre-0054: the route does not exist — FastAPI's route-level 404,
                # NOT the handler's "project not found".
                return httpx.Response(404, json={"detail": "Not Found"})
            # PROJECT-DIRECT run (0054): no experiment; group_id is rejected
            # like the engine does (run groups are experiment-anchored), and an
            # unknown project is the handler's oracle-safe 404.
            if m.group(1) not in self.projects:
                return httpx.Response(404, json={"detail": "project not found"})
            if body.get("group_id") is not None:
                return httpx.Response(
                    422, json={"detail": "group_id requires an experiment-attached run"}
                )
            replay = self._creation_replay(path, body)
            if replay is not None:
                return replay
            conflict = self._run_external_id_conflict(body)
            if conflict is not None:
                return conflict
            rid = str(uuid.uuid4())
            row = self._new_run(rid, None, body, project_id=m.group(1))
            self._remember_creation(path, body, rid)
            return httpx.Response(201, json=row)

        m = _RUN_METRICS.match(path)
        if m and method == "POST":
            if self.fail_next_metrics:
                self.fail_next_metrics = False
                return httpx.Response(503, json={"detail": "db down"})
            if self.metrics_busy_next > 0:
                self.metrics_busy_next -= 1
                headers = (
                    {"Retry-After": self.metrics_busy_retry_after}
                    if self.metrics_busy_retry_after is not None
                    else {}
                )
                return httpx.Response(
                    503,
                    json={"detail": "concurrent telemetry write; retry this ingest batch"},
                    headers=headers,
                )
            points = body.get("points", [])
            if body.get("origin") == "derived" and not body.get("provenance"):
                return httpx.Response(422, json={"detail": "derived batch requires provenance"})
            self.metrics_inserted += len(points)
            self.metric_batches_posted.append(body)
            self.metric_points_posted.setdefault(m.group(1), []).extend(points)
            return httpx.Response(200, json={"inserted": len(points)})
        if m and method == "GET":
            rows = self.metric_points.get(m.group(1), [])
            key = request.url.params.get("key")
            kind = request.url.params.get("kind")
            limit = request.url.params.get("limit")
            if key is not None:
                rows = [r for r in rows if r.get("key") == key]
            if kind is not None:
                rows = [r for r in rows if r.get("kind") == kind]
            return httpx.Response(200, json=rows[: int(limit)] if limit else rows)

        # -- expression views (0088). Storage + identity only: EVALUATION is the
        # server's job and research-os tests it. What matters here is that the
        # client reaches every route with the right body and reads the envelope.
        m = _RUN_VIEWS_PREVIEW.match(path)
        if m and method == "POST":
            return httpx.Response(200, json=self._view_envelope(body["spec"], view_id=None))

        m = _RUN_VIEWS.match(path)
        if m and method == "POST":
            rid = m.group(1)
            rows = self.views.setdefault(rid, [])
            if any(r["name"] == body["name"] for r in rows):
                return httpx.Response(409, json={"detail": "view name already in use"})
            row = {
                "id": str(uuid.uuid4()),
                "run_id": rid,
                "name": body["name"],
                "spec": body["spec"],
                "created_by": "user:test",
                "created_at": "2026-08-03T00:00:00Z",
                "updated_at": "2026-08-03T00:00:00Z",
            }
            rows.append(row)
            return httpx.Response(201, json=row)
        if m and method == "GET":
            return httpx.Response(200, json=self.views.get(m.group(1), []))

        m = _RUN_VIEW_DATA.match(path)
        if m and method == "GET":
            rid, vid = m.group(1), m.group(2)
            row = next((r for r in self.views.get(rid, []) if r["id"] == vid), None)
            if row is None:
                return httpx.Response(404, json={"detail": "view not found"})
            return httpx.Response(
                200, json=self._view_envelope(row["spec"], view_id=vid, name=row["name"])
            )

        m = _VIEW.match(path)
        if m:
            vid = m.group(1)
            for rid, rows in self.views.items():
                for i, row in enumerate(rows):
                    if row["id"] != vid:
                        continue
                    if method == "PATCH":
                        # The CAS precondition (`_stale_view_conflict`): a caller
                        # naming the revision it read is refused with the CURRENT
                        # head when the view moved. A fence input, never stored.
                        expected = body.pop("expected_updated_at", None)
                        if expected is not None and _instant(expected) != _instant(
                            row["updated_at"]
                        ):
                            current = {k: row[k] for k in ("name", "spec", "updated_at")}
                            return httpx.Response(
                                409,
                                json={
                                    "detail": {
                                        "message": (
                                            "view changed since it was loaded; reload and reapply"
                                        ),
                                        "current": current,
                                    }
                                },
                            )
                        updated = {**row, **{k: v for k, v in body.items() if v is not None}}
                        updated["updated_at"] = "2026-08-03T01:00:00Z"
                        rows[i] = updated
                        return httpx.Response(200, json=updated)
                    if method == "DELETE":
                        rows.pop(i)
                        return httpx.Response(204)
            return httpx.Response(404, json={"detail": "view not found"})

        # -- coordinate reads (0059-0062): grouped / wide / export / catalog --
        m = _RUN_METRICS_GROUPED.match(path)
        if m and method == "GET":
            rid = m.group(1)
            p = request.url.params
            key = p.get("key")
            rows = self._stepped_points(rid, p, keys=[key] if key else None)
            agg = p.get("agg")
            if agg is None:
                # 0062: omitted agg resolves to the key's DECLARED reduce fn
                # (else mean); conflicting declarations are a 422, mirroring
                # the server. Declarations arrive on posted points or the
                # `declared_aggs` seed knob.
                declared = {
                    q["agg"]
                    for q in self.metric_points_posted.get(rid, [])
                    if q.get("key") == key and q.get("agg")
                }
                if key in self.declared_aggs:
                    declared.add(self.declared_aggs[key])
                if len(declared) > 1:
                    return httpx.Response(
                        422, json={"detail": f"conflicting agg declarations for {key!r}"}
                    )
                agg = declared.pop() if declared else "mean"
            by = [axis for axis in (p.get("by") or "").split(",") if axis]
            where = json.loads(p["where"]) if "where" in p else None
            if where:
                rows = [
                    r
                    for r in rows
                    if all((r.get("dimensions") or {}).get(k) == v for k, v in where.items())
                ]
            bucket = int(p.get("step_bucket") or 1)
            max_rows = int(p.get("max_rows") or 10000)
            if self.grouped_page_rows:
                max_rows = min(max_rows, self.grouped_page_rows)
            cells: dict[tuple, list[float]] = {}
            for r in rows:
                b = (r["step_index"] // bucket) * bucket
                group = tuple((axis, (r.get("dimensions") or {}).get(axis)) for axis in by)
                cells.setdefault((b, group), []).append(r["value"])
            fns = {
                "mean": lambda v: sum(v) / len(v),
                "sum": sum,
                "min": min,
                "max": max,
                "count": len,
            }
            groups: list[dict] = []
            truncated, next_step = False, None
            for (b, group), values in sorted(
                cells.items(), key=lambda cell: (cell[0][0], str(cell[0][1]))
            ):
                # Cut only at a bucket boundary, so next_step is a clean re-entry.
                if len(groups) >= max_rows and b != groups[-1]["step_index"]:
                    truncated, next_step = True, b
                    break
                groups.append(
                    {
                        "step_index": b,
                        # Group labels are each axis value's JSON text (int 1 vs "1").
                        "group": {axis: (None if v is None else json.dumps(v)) for axis, v in group}
                        or None,
                        "value": float(fns[agg](values)),
                        "n": len(values),
                    }
                )
            return httpx.Response(
                200,
                json={
                    "key": key,
                    "kind": p.get("kind"),
                    "agg": agg,
                    "by": by or None,
                    "where": where,
                    "step_bucket": bucket,
                    "groups": groups,
                    "truncated": truncated,
                    "next_step": next_step,
                },
            )

        m = _RUN_METRICS_WIDE.match(path)
        if m and method == "GET":
            p = request.url.params
            rows = self._stepped_points(m.group(1), p, keys=p.get_list("key") or None)
            steps = sorted({r["step_index"] for r in rows})
            max_rows = int(p.get("max_rows") or 10000)
            if self.wide_page_rows:
                max_rows = min(max_rows, self.wide_page_rows)
            truncated = len(steps) > max_rows
            next_step = steps[max_rows] if truncated else None
            steps = steps[:max_rows]
            # Columns cover THIS page's window only (a series with no point in
            # the emitted steps is absent from `columns`), so a paging client
            # must realign by series identity, never trust positions.
            window = set(steps)
            rows = [r for r in rows if r["step_index"] in window]
            idents = sorted(
                {
                    (
                        r.get("key"),
                        r.get("kind"),
                        json.dumps(r.get("dimensions") or {}, sort_keys=True),
                    )
                    for r in rows
                }
            )
            values = {
                (
                    r["step_index"],
                    (
                        r.get("key"),
                        r.get("kind"),
                        json.dumps(r.get("dimensions") or {}, sort_keys=True),
                    ),
                ): r["value"]
                for r in rows
            }
            return httpx.Response(
                200,
                json={
                    "columns": [
                        {"key": k, "kind": kd, "dimensions": json.loads(d)} for k, kd, d in idents
                    ],
                    "rows": [
                        {"step_index": s, "values": [values.get((s, c)) for c in idents]}
                        for s in steps
                    ],
                    "truncated": truncated,
                    "next_step": next_step,
                },
            )

        m = _RUN_METRICS_EXPORT.match(path)
        if m and method == "GET":
            p = request.url.params
            rows = sorted(self.metric_points.get(m.group(1), []), key=lambda r: r.get("id", 0))
            for param, field in (("key", "key"), ("kind", "kind")):
                if p.get(param) is not None:
                    rows = [r for r in rows if r.get(field) == p[param]]
            if p.get("step_from") is not None:
                rows = [
                    r
                    for r in rows
                    if r.get("step_index") is not None and r["step_index"] >= int(p["step_from"])
                ]
            if p.get("step_to") is not None:
                rows = [
                    r
                    for r in rows
                    if r.get("step_index") is not None and r["step_index"] <= int(p["step_to"])
                ]
            if p.get("after_id") is not None:
                rows = [r for r in rows if r["id"] > int(p["after_id"])]
            limit = int(p.get("limit") or 1000)
            page, rest = rows[:limit], rows[limit:]
            return httpx.Response(
                200,
                json={
                    "points": page,
                    "next_after_id": page[-1]["id"] if rest else None,
                },
            )

        m = _RUN_COORDINATES.match(path)
        if m and method == "GET":
            return httpx.Response(200, json=self.coordinates.get(m.group(1), []))

        if path == "/v1/series/latest" and method == "POST":
            scalars = []
            for rid in body.get("run_ids", []):
                row = self.runs.get(rid)
                # Every run is validated in-tenant AND live before any read. A
                # run seeded only through `seed_series` exists for this fake too.
                if row is None and rid not in self.series_points:
                    return httpx.Response(404, json={"detail": "run not found"})
                # The CATALOG: seeded rows when a test gave some, else derived
                # from the seeded points, as the real catalog is from logged ones.
                catalog = self.series.get(rid) or [
                    {
                        "kind": s.get("kind", "model"),
                        "key": s["key"],
                        "dimensions": s.get("dimensions") or {},
                        "x_axis": s.get("x_axis", "step"),
                        "point_count": len(s["points"]),
                    }
                    for s in self.series_points.get(rid, [])
                ]
                for s in catalog:
                    if body.get("keys") and s.get("key") not in body["keys"]:
                        continue
                    if body.get("kind") and s.get("kind") != body["kind"]:
                        continue
                    scalars.append({**s, "run_id": rid})
            return httpx.Response(200, json={"scalars": scalars})

        m = _RUN_SERIES.match(path)
        if m and method == "GET":
            return httpx.Response(200, json=self.series.get(m.group(1), []))
        if m and method == "DELETE":
            # Records the identity triple rather than mutating a catalog: what
            # matters on the client side is that the write identity and the
            # delete identity are the same three fields.
            params = request.url.params
            raw = params.get("dimensions")
            self.deleted_series.append(
                {
                    "run_id": m.group(1),
                    "kind": params.get("kind"),
                    "key": params.get("key"),
                    "dimensions": json.loads(raw) if raw else None,
                }
            )
            return httpx.Response(204)

        if path == "/v1/series/query" and method == "POST":
            # Multi-run series read, backing client.compare(). Serves whatever
            # seed_series() put in `series_points`, filtered the way the real
            # endpoint filters: by run, by (key, kind) selector, and by step.
            self.series_queries.append(body)
            run_ids = [str(rid) for rid in body.get("run_ids", [])]
            if self.source_backed_runs.intersection(run_ids) and (
                body.get("source_read_contract") != "coverage-v1"
            ):
                # provider_reads.require_source_read_contract
                return httpx.Response(
                    422,
                    json={
                        "detail": {
                            "code": "unsupported_source_query",
                            "message": (
                                "source-backed metrics require the coverage-v1 read contract"
                            ),
                        }
                    },
                )
            wanted = {(s["key"], s.get("kind", "model")) for s in (body.get("series") or [])}
            # `keys` is the route's key-only prefilter: every kind and dimension
            # variant of each named key, intersected with `series` when both.
            keys = set(body["keys"]) if body.get("keys") else None
            step_from, step_to = body.get("step_from"), body.get("step_to")
            max_points = body.get("max_points")
            out = []
            for rid in run_ids:
                for row in self.series_points.get(rid, []):
                    if wanted and (row["key"], row.get("kind", "model")) not in wanted:
                        continue
                    if keys is not None and row["key"] not in keys:
                        continue
                    # `step_index >= $n` in SQL: a stepless point never passes
                    # a step bound.
                    points = [
                        p
                        for p in row["points"]
                        if (
                            step_from is None
                            or (p.get("step_index") is not None and p["step_index"] >= step_from)
                        )
                        and (
                            step_to is None
                            or (p.get("step_index") is not None and p["step_index"] <= step_to)
                        )
                    ]
                    points = _min_max_downsample(points, max_points)
                    out.append(
                        {
                            **row,
                            "run_id": rid,
                            "points": points,
                            "read_provenance": _series_read_provenance(
                                rid in self.source_backed_runs, max_points
                            ),
                        }
                    )
            return httpx.Response(200, json={"series": out, **self.series_result_extra})

        m = _RUN_STEPS.match(path)
        if m and method == "POST":
            # StepCreate{step_index, name, attributes, summary} -> SpanOut. The
            # per-step record; log() routes non-numeric values into `attributes`.
            # Upserts on (run, step_index) and REPLACES name/attributes/summary,
            # exactly like the real endpoint (`app/telemetry/spans_router.py`:
            # `attributes = EXCLUDED.attributes`). This fake used to MERGE, which
            # hid the client-side clobber plan (f) fixes.
            rid, index = m.group(1), body["step_index"]
            record = {
                "step_index": index,
                "name": body.get("name"),
                "attributes": dict(body.get("attributes") or {}),
                "summary": dict(body.get("summary") or {}),
            }
            self.steps.setdefault(rid, {})[index] = record
            return httpx.Response(
                201, json={"id": str(uuid.uuid4()), "span_type": "step", **record}
            )

        m = _RUN_SPANS.match(path)
        if m and method == "POST":
            n = len(body.get("spans", []))
            self.spans_upserted += n
            self.spans.setdefault(m.group(1), []).extend(body.get("spans", []))
            return httpx.Response(200, json={"upserted": n})
        if m and method == "GET":
            rows = self.spans.get(m.group(1), [])
            span_type = request.url.params.get("span_type")
            parent = request.url.params.get("parent_span_id")
            step_from = request.url.params.get("step_from")
            step_to = request.url.params.get("step_to")
            limit = request.url.params.get("limit")
            if span_type is not None:
                rows = [r for r in rows if r.get("span_type") == span_type]
            if parent is not None:
                rows = [r for r in rows if r.get("parent_span_id") == parent]
            if step_from is not None:
                rows = [
                    r
                    for r in rows
                    if r.get("step_index") is not None and r["step_index"] >= int(step_from)
                ]
            if step_to is not None:
                rows = [
                    r
                    for r in rows
                    if r.get("step_index") is not None and r["step_index"] <= int(step_to)
                ]
            return httpx.Response(200, json=rows[: int(limit)] if limit else rows)

        m = _RUN_ARTIFACTS.match(path)
        if m and method == "POST":
            row = {"id": str(uuid.uuid4()), **body}
            self.artifacts.setdefault(m.group(1), []).append(row)
            return httpx.Response(201, json=row)
        if m and method == "GET":
            rows = self.artifacts.get(m.group(1), [])
            kind = request.url.params.get("kind")
            step_from = request.url.params.get("step_from")
            step_to = request.url.params.get("step_to")
            # Exact, as `name = $n` in app/artifacts/service.py. Ignoring it here made
            # `resolve_artifact` untestable: every lookup "resolved" to the run's first
            # artifact whatever was asked for.
            name = request.url.params.get("name")
            if name is not None:
                rows = [r for r in rows if r.get("name") == name]
            if kind is not None:
                rows = [r for r in rows if r.get("kind") == kind.strip().lower()]
            if step_from is not None:
                rows = [
                    r
                    for r in rows
                    if r.get("step_index") is not None and r["step_index"] >= int(step_from)
                ]
            if step_to is not None:
                rows = [
                    r
                    for r in rows
                    if r.get("step_index") is not None and r["step_index"] <= int(step_to)
                ]
            limit = int(request.url.params.get("limit") or 1000)
            offset = int(request.url.params.get("offset") or 0)
            return httpx.Response(
                200, json=rows[offset : offset + limit],
                headers={"X-Artifact-Pagination": "offset-v1"},
            )

        m = _RUN_BUNDLE.match(path)
        if m and method == "GET":
            rid = m.group(1)
            if rid in self.source_backed_runs and (
                request.url.params.get("source_read_contract") != "coverage-v1"
            ):
                # app/read_models/router.py: a source-backed run's bundle
                # requires the coverage read contract.
                return httpx.Response(
                    422,
                    json={
                        "detail": {
                            "code": "unsupported_source_query",
                            "message": (
                                "source-backed metrics require the coverage-v1 read contract"
                            ),
                        }
                    },
                )
            artifacts = self.artifacts.get(rid, [])
            return httpx.Response(
                200,
                json={
                    "run": self.runs[rid],
                    "series": [],
                    "artifacts": artifacts,
                    "artifact_total": len(artifacts),
                    "span_types": [],
                    "parent_run_id": self.runs[rid].get("parent_run_id"),
                    "child_run_ids": [],
                    # Capped server-side (SESSION_DISPLAY_LIMIT) against an
                    # exact total, and the route takes no offset.
                    "sessions": self.run_sessions.get(rid, [])[:50],
                    "session_total": len(self.run_sessions.get(rid, [])),
                },
            )

        m = _RUN_CODE_COMPARE.match(path)
        if m and method == "GET":
            rid = m.group(1)
            if rid not in self.runs:
                return httpx.Response(404, json={"detail": "run not found"})
            to = request.url.params.get("to")
            if not to:
                # FastAPI refuses a missing required query param with a 422.
                return httpx.Response(422, json={"detail": "to is required"})
            canned = self.run_code_compare.get((rid, to))
            if canned is not None:
                return httpx.Response(200, json=canned)
            return httpx.Response(404, json={"detail": "run not found"})

        m = _RUN_CODE.match(path)
        if m and method == "GET":
            rid = m.group(1)
            if rid not in self.runs:
                return httpx.Response(404, json={"detail": "run not found"})
            return httpx.Response(
                200,
                json=self.run_code.get(rid)
                or {"state": "none", "source_attached": False},
            )

        m = _EXPERIMENT_CODE.match(path)
        if m and method == "GET":
            eid = m.group(1)
            if eid not in self.experiments:
                return httpx.Response(404, json={"detail": "experiment not found"})
            return httpx.Response(
                200,
                json=self.experiment_code.get(eid)
                or {
                    "experiment_id": eid,
                    "project_id": self.experiments[eid].get("project_id"),
                    "sources": [],
                    "runs": [],
                    "windows": [],
                },
            )

        m = _RUN_REPRODUCE.match(path)
        if m and method == "GET":
            rid = m.group(1)
            run = self.runs.get(rid) or next(
                (r for r in self.runs.values() if r.get("slug") == rid), None
            )
            if run is None:
                # The real endpoint 404s an unknown run (resolve_run_ref) rather than
                # auto-vivifying it — the reproduce route must not invent a run.
                return httpx.Response(404, json={"detail": "run not found"})
            launch = (run.get("metadata") or {}).get("launch")
            env_ref = run.get("env_ref")
            # The real endpoint assembles question (from the run's experiment) and
            # the execution record (by resolving env_ref). Mirror that so the client
            # passthrough is exercised against a populated record, not a stub.
            exp = self.experiments.get(run.get("experiment_id") or "")
            question = exp.get("question") if exp else None
            execution_record = self.execution_records.get(env_ref) if env_ref else None
            code_snapshot = next(
                (a for a in self.artifacts.get(run["id"], []) if a.get("kind") == "code_snapshot"),
                None,
            )
            # Mirror the server's _completeness verdict EXACTLY (research-os
            # app/read_models/reproduce.py), validated against a live uvicorn+Postgres
            # cross-repo smoke. The MCP run view forwards `missing` verbatim, so this
            # fidelity is load-bearing — a drifted fake would green a wrong client.
            missing: list = []
            advisories: list = []
            if not env_ref:
                missing.append("execution_record")
            if code_snapshot is None:
                missing.append("code_snapshot_artifact")
            else:
                meta = code_snapshot.get("meta") or {}
                if meta.get("n_pending_upload", 0) > 0:
                    missing.append("pending_code_bytes")
                if meta.get("n_lockfiles", 0) == 0:
                    advisories.append("no_lockfiles")
            if not launch:
                advisories.append("launch_context")
            else:
                for slot in ("process", "runtime", "determinism"):
                    if not launch.get(slot):
                        missing.append(f"launch_{slot}")
                if launch.get("errors"):
                    advisories.append("launch_errors")
            inputs_decision: list = []  # the fake carries none, so the advisory always fires
            if not inputs_decision:
                advisories.append("inputs_decision")
            if not run.get("notes"):
                advisories.append("notes")
            return httpx.Response(
                200,
                json={
                    "run": run,
                    "question": question,
                    "execution_record": execution_record,
                    "launch": launch,
                    "restore_command": f"probe snapshot-restore {run.get('slug') or run['id']}",
                    "code_snapshot": code_snapshot,
                    "inputs_decision": inputs_decision,
                    "note_artifacts": [],
                    "lockfiles": [],
                    "edges": [],
                    "span_env_refs": [],
                    "completeness": {
                        "state": "incomplete" if missing else "unverified",
                        "missing": missing,
                        "advisories": advisories,
                    },
                },
            )

        m = _EXPERIMENT_REPRODUCE.match(path)
        if m and method == "GET":
            eid = m.group(1)
            exp = self.experiments.get(eid)
            if exp is None:
                return httpx.Response(404, json={"detail": "experiment not found"})
            version = request.url.params.get("version")
            # Mirror ExperimentReproduce + _rollup_completeness + _run_summary_state
            # EXACTLY (research-os app/read_models/reproduce.py) — the `experiment`
            # object, the has_code_snapshot signal, and the runs_* rollup keys were
            # all confirmed against a live uvicorn+Postgres cross-repo smoke.
            summaries = []
            for r in self.runs.values():
                if r.get("experiment_id") != eid:
                    continue
                has_code = any(
                    a.get("kind") == "code_snapshot" for a in self.artifacts.get(r["id"], [])
                )
                state = "unverified" if (r.get("env_ref") and has_code) else "incomplete"
                summaries.append(
                    {
                        "id": r["id"],
                        "slug": r.get("slug"),
                        "name": r.get("name"),
                        "status": r.get("status", "running"),
                        "description": r.get("description"),
                        "env_ref": r.get("env_ref"),
                        "has_launch": bool((r.get("metadata") or {}).get("launch")),
                        "has_code_snapshot": has_code,
                        "state": state,
                        "missing_pin": False,
                        "reproduce_url": f"/v1/runs/{r['id']}/reproduce",
                    }
                )
            return httpx.Response(
                200,
                json={
                    "experiment": exp,
                    "versions": [],
                    "resolved_version": int(version) if version else None,
                    "runs": summaries,
                    "completeness": {
                        "runs_total": len(summaries),
                        "runs_unverified": sum(1 for s in summaries if s["state"] == "unverified"),
                        "runs_incomplete": sum(1 for s in summaries if s["state"] == "incomplete"),
                        "missing_pins": 0,
                    },
                },
            )

        m = _RUN_LINEAGE.match(path)
        if m and method == "GET":
            run = self.runs.get(m.group(1))
            return httpx.Response(
                200,
                json={
                    "run_id": m.group(1),
                    "ancestors": [],
                    "descendants": [],
                    "truncated": False,
                    # L18: where it came from, derived like the server's.
                    "origin": self._run_origin(run) if run else None,
                },
            )

        m = _RUN_TRIALS.match(path)
        if m and method == "GET":
            run_ref = m.group(1)
            run = self.runs.get(run_ref)
            run_id = run["id"] if run is not None else run_ref
            rows = sorted(
                (row for row in self.trials.values() if row.get("run_id") == run_id),
                key=lambda row: (row.get("created_at") or "", row.get("id") or ""),
                reverse=True,
            )
            limit = min(int(request.url.params.get("limit") or 50), 200)
            start = int(request.url.params.get("cursor") or 0)
            window = [
                {
                    key: row.get(key)
                    for key in (
                        "id",
                        "rollout_span_id",
                        "run_id",
                        "name",
                        "name_customized",
                        "description",
                        "description_customized",
                        "status",
                        "step_index",
                        "started_at",
                        "ended_at",
                        "provider",
                        "created_at",
                        "updated_at",
                    )
                }
                for row in rows[start : start + limit]
            ]
            headers = {}
            if window and len(window) == limit:
                headers["x-next-cursor"] = str(start + limit)
            return httpx.Response(200, json=window, headers=headers)

        m = _RUN_ITEM.match(path)
        if m and method == "DELETE":
            rid = m.group(1)
            if self.runs.pop(rid, None) is None:
                return httpx.Response(404, json={"detail": "run not found"})
            return httpx.Response(204)
        if m and method == "GET":
            rid = m.group(1)
            row = self.runs.get(rid)
            if row is None:
                # GET /v1/runs/{run_ref} is the ONE item route whose path param is
                # an untyped string rather than format:uuid -- the server resolves
                # a slug here. Mirror that before the auto-vivify
                # fallback below, or a slug becomes a brand-new run's id and
                # every by-petname assertion passes against a fiction.
                row = next((r for r in self.runs.values() if r.get("slug") == rid), None)
            if row is None:
                row = self._new_run(rid, "exp", {"name": "r"})
            return httpx.Response(200, json=row)
        if m and method == "PATCH":
            rid = m.group(1)
            # NB: not setdefault() - _new_run has a side effect (stores the row), so
            # an eager default would clobber the existing run on every PATCH.
            row = self.runs.get(rid) or self._new_run(rid, "exp", {"name": "r"})
            # Pre-0096 (`stores_entity_notes = False`): the notes fields are
            # unknown, so they are accepted and dropped rather than rejected --
            # the row keeps no `notes` key at all, which is what the SDK's
            # silent-drop warning keys on.
            refused = self._apply_notes_write(
                row, body, self.entity_notes_cap, stores=self.stores_entity_notes
            )
            if refused is not None:
                return refused
            for k, v in body.items():
                if k in self.NOTES_WRITE_FIELDS:
                    continue
                if k == "write_epoch":
                    # 1.10: a fence INPUT (checked in `_fence_stale_writer`),
                    # never a column this PATCH writes. Storing it would let a
                    # stale writer rewind the run's generation.
                    continue
                if k == "foreign_keys":  # per-key new-wins merge (mirrors the backend)
                    row["foreign_keys"] = {**(row.get("foreign_keys") or {}), **v}
                elif k == "config_merge":
                    # #2017: `config = config || $n::jsonb` -- shallow, new wins,
                    # a null value stored as null; a non-object is a 422; an
                    # older server drops the unknown field and answers 200.
                    if not self.supports_config_merge:
                        continue
                    if v is not None and not isinstance(v, dict):
                        return httpx.Response(422, json={"detail": "config_merge must be an object"})
                    if v:
                        row["config"] = {**(row.get("config") or {}), **v}
                else:
                    row[k] = v
            return httpx.Response(200, json=row)

        # -- run groups --
        m = re.match(r"^/v1/experiments/([^/]+)/groups$", path)
        if m and method == "POST":
            eid = m.group(1)
            dup = next(
                (
                    g
                    for g in self.groups.values()
                    if g["experiment_id"] == eid and g["name"] == body["name"]
                ),
                None,
            )
            if dup:
                return httpx.Response(
                    409, json={"detail": {"message": "group name exists", "existing_id": dup["id"]}}
                )
            gid = str(uuid.uuid4())
            row = {
                "id": gid,
                "customer_id": "lab-42",
                "experiment_id": eid,
                "kind": body.get("kind", "group"),
                "name": body["name"],
                "spec": body.get("spec", {}),
                "created_at": "2026-07-15T00:00:00Z",
            }
            if self.stores_entity_notes:
                row["notes"] = body.get("notes")
            self.groups[gid] = row
            return httpx.Response(201, json=row)
        if m and method == "GET":
            eid = m.group(1)
            return httpx.Response(
                200, json=[g for g in self.groups.values() if g["experiment_id"] == eid]
            )
        m = re.match(r"^/v1/groups/([^/]+)$", path)
        if m and method in ("GET", "PATCH"):
            gid = m.group(1)
            row = self.groups.get(gid)
            if row is None:
                return httpx.Response(404, json={"detail": "group not found"})
            if method == "PATCH":
                refused = self._apply_notes_write(
                    row, body, self.entity_notes_cap, stores=self.stores_entity_notes
                )
                if refused is not None:
                    return refused
                row.update(
                    {
                        k: v
                        for k, v in body.items()
                        if v is not None and k not in self.NOTES_WRITE_FIELDS
                    }
                )
            return httpx.Response(200, json=row)

        # -- permanent delete --
        m = _EXP_ITEM.match(path)
        if m and method == "DELETE":
            eid = m.group(1)
            if self.experiments.pop(eid, None) is None:
                return httpx.Response(404, json={"detail": "experiment not found"})
            # Mirrors the engine cascade (0080): the experiment's runs go with it.
            for rid in [rid for rid, r in self.runs.items() if r.get("experiment_id") == eid]:
                self.runs.pop(rid)
            return httpx.Response(204)

        m = re.match(r"^/v1/runs/([^/]+)/heartbeat$", path)
        if m and method == "POST":
            rid = m.group(1)
            row = self.runs.get(rid)
            if row is None:
                return httpx.Response(404, json={"detail": "run not found"})
            # 2.8: a lease holder never beats here, so whoever does is a writer
            # no lease shows: a `leases` run keeps the legacy rules for good.
            if row.get("liveness_protocol") == "leases":
                row["liveness_protocol"] = "legacy"
            # Mirrors app/runs/router.py: only a 'running' run is stamped; a late
            # beat racing a completion is a no-op, not an error. role=observer
            # (0106) stamps the observer column and never asserts ownership.
            if row.get("status") == "running":
                if request.url.params.get("role") == "observer":
                    row["observer_heartbeat_at"] = self._stamp()
                    self.run_observer_heartbeats[rid] = self.run_observer_heartbeats.get(rid, 0) + 1
                else:
                    row["last_heartbeat_at"] = self._stamp()
                    self.run_heartbeats[rid] = self.run_heartbeats.get(rid, 0) + 1
                    # 0205: only a beat from INSIDE the work stamps attached_at,
                    # first-write-wins. A launcher beats without the flag, so a
                    # wrapped run whose child never attached stays honest.
                    if request.url.params.get("attached") == "true":
                        row["attached_at"] = row.get("attached_at") or self._stamp()
                        self.run_attached_beats[rid] = self.run_attached_beats.get(rid, 0) + 1
            return httpx.Response(200, json=row)

        if path == "/v1/artifacts/uploads/gc" and method == "POST":
            older_than = body["older_than"]
            swept = 0
            for arts in self.artifacts.values():
                for a in list(arts):
                    # Pending AND old enough: a confirmed artifact is never swept, and
                    # neither is an upload started after the cutoff.
                    if a.get("status") == "pending" and a.get("created_at", "") < older_than:
                        arts.remove(a)
                        swept += 1
            return httpx.Response(200, json={"swept": swept})

        m = re.match(r"^/v1/artifacts/([^/]+)$", path)
        if m and method == "DELETE":
            aid = m.group(1)
            for arts in self.artifacts.values():
                for a in list(arts):
                    if a.get("id") == aid:
                        arts.remove(a)
                        return httpx.Response(204)
            return httpx.Response(404, json={"detail": "artifact not found"})
        if m and method in ("GET", "PATCH"):
            # The artifact detail read and its PATCH (name, description, the
            # notes writes). The notes primitives run through the one shared
            # implementation, against the 4,000-character annotation cap.
            row = self._find_artifact(m.group(1))
            if row is None:
                return httpx.Response(404, json={"detail": "artifact not found"})
            if method == "PATCH":
                refused = self._apply_notes_write(
                    row, body, self.entity_notes_cap, stores=self.stores_entity_notes
                )
                if refused is not None:
                    return refused
                row.update(
                    {
                        key: value
                        for key, value in body.items()
                        if value is not None and key not in self.NOTES_WRITE_FIELDS
                    }
                )
            return httpx.Response(200, json=dict(row))

        # -- reads: series / metrics / spans / experiment edges --
        m = _RUN_SERIES.match(path)
        if m and method == "GET":
            return httpx.Response(200, json=self.series.get(m.group(1), []))

        m = _RUN_METRICS.match(path)
        if m and method == "GET":
            rid = m.group(1)
            rows = self.metric_points.get(rid, [])
            key = request.url.params.get("key")
            if key:
                rows = [p for p in rows if p.get("key") == key]
            return httpx.Response(200, json=rows)

        m = _RUN_SPANS.match(path)
        if m and method == "GET":
            rid = m.group(1)
            rows = self.spans.get(rid, [])
            span_type = request.url.params.get("span_type")
            if span_type:
                rows = [s for s in rows if s.get("span_type") == span_type]
            return httpx.Response(200, json=rows)

        m = re.match(r"^/v1/spans/([^/]+)$", path)
        if m and method == "GET":
            sid = m.group(1)
            for rows in self.spans.values():
                for span in rows:
                    if span.get("id") == sid:
                        return httpx.Response(200, json=span)
            return httpx.Response(404, json={"detail": "span not found"})

        m = re.match(r"^/v1/experiments/([^/]+)/artifacts$", path)
        if m and method == "GET":
            # Mirrors app/artifacts/experiment_router.py: `experiment_id = $1`, and
            # nothing else. This used to roll up the artifacts of the experiment's
            # RUNS -- rows the real route has never returned -- while reading the
            # directly-filed ones from the wrong key, so it missed the only rows that
            # DO belong here. Both halves inverted: it invented an inheritance the
            # backend does not implement and hid the anchor the backend does.
            eid = m.group(1)
            rows = list(self.artifacts.get(f"experiment:{eid}", []))
            rows += [a for a in self.artifacts.get(eid, []) if a.get("experiment_id") == eid]
            return httpx.Response(200, json=_newest_first(rows))

        m = re.match(r"^/v1/experiments/([^/]+)/edges$", path)
        if m and method == "GET":
            # Mirrors app/lineage/router.py: an edge belongs to the experiment when the
            # run/artifact on either end does. Returning every edge instead would let a
            # client that passed the wrong id still pass the test.
            eid = m.group(1)
            run_ids = {r for r, row in self.runs.items() if row.get("experiment_id") == eid}
            artifact_ids = {
                a["id"] for rid in run_ids for a in self.artifacts.get(rid, []) if a.get("id")
            }

            def _touches(edge: dict) -> bool:
                for side in ("source", "target"):
                    kind, ref = edge.get(f"{side}_type"), edge.get(f"{side}_id")
                    if kind == "run" and ref in run_ids:
                        return True
                    if kind == "artifact" and ref in artifact_ids:
                        return True
                return False

            touching = [e for e in self.edges if _touches(e)]
            # The route's opt-in `limit` (stored edges first; the fake derives none).
            limit = request.url.params.get("limit")
            return httpx.Response(200, json=touching[: int(limit)] if limit else touching)

        # -- artifact versions (the chain the retired asset registry folded into) --
        m = re.match(r"^/v1/artifacts/([^/]+)/versions$", path)
        if m:
            aid = m.group(1)
            if method == "POST":
                vers = self.artifact_versions.setdefault(aid, [])
                v = {
                    "id": str(uuid.uuid4()),
                    "customer_id": "lab-42",
                    "artifact_id": aid,
                    "version": len(vers) + 1,
                    "label": body.get("label"),
                    "content_hash": body.get("content_hash"),
                    "uri": body.get("uri"),
                    "size_bytes": body.get("size_bytes"),
                    "content_type": body.get("content_type"),
                    "source_artifact_id": body.get("from_artifact_id"),
                    "meta": body.get("meta", {}),
                    "status": "complete",
                    "origin": "upload",
                    "created_at": "2026-07-11T00:00:00Z",
                }
                vers.append(v)
                return httpx.Response(201, json=v)
            if method == "GET":
                # 404 on an UNKNOWN id, exactly like the route: it calls
                # `require_artifact(conn, artifact_id)` before listing, which raises
                # 404 "artifact not found" for an absent or soft-deleted row
                # (research-os app/artifacts/versions_router.py). Returning 200 + []
                # here would conflate "this artifact has no versions yet" with "no
                # such artifact" -- opposite answers, and the second is the one a
                # caller may use as an existence probe. A fake that cannot tell them
                # apart certifies a client that cannot either.
                if self._find_artifact(aid) is None:
                    return httpx.Response(404, json={"detail": "artifact not found"})
                return httpx.Response(200, json=self.artifact_versions.get(aid, []))

        # -- lineage edges (fold #2) --
        if path == "/v1/edges" and method == "POST":
            row = {
                "id": str(uuid.uuid4()),
                "customer_id": "lab-42",
                **body,
                "created_at": "2026-07-11T00:00:00Z",
            }
            self.edges.append(row)
            return httpx.Response(201, json=row)
        m = re.match(r"^/v1/runs/([^/]+)/edges$", path)
        if m and method == "GET":
            rid = m.group(1)
            return httpx.Response(
                200, json=[e for e in self.edges if rid in (e.get("source_id"), e.get("target_id"))]
            )

        # -- execution records (fold #7) --
        if path == "/v1/execution-records" and method == "POST":
            ch = "sha256:" + hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
            row = {
                "customer_id": "lab-42",
                "content_hash": ch,
                **{k: body.get(k, {}) for k in ("code", "deps", "hardware", "settings", "paths")},
                "created_at": "2026-07-11T00:00:00Z",
            }
            self.execution_records[ch] = row
            return httpx.Response(201, json=row)
        m = re.match(r"^/v1/execution-records/(.+)$", path)
        if m and method == "GET":
            return httpx.Response(
                200, json=self.execution_records.get(m.group(1), {"content_hash": m.group(1)})
            )

        # -- experiment versions (fold #6) --
        m = re.match(r"^/v1/experiments/([^/]+)/versions$", path)
        if m and method == "POST":
            eid = m.group(1)
            vers = self.experiment_versions.setdefault(eid, [])
            v = {
                "id": str(uuid.uuid4()),
                "experiment_id": eid,
                "version": len(vers) + 1,
                "label": body.get("label"),
                "created_at": "2026-07-11T00:00:00Z",
            }
            vers.append(v)
            return httpx.Response(201, json=v)
        if m and method == "GET":
            return httpx.Response(200, json=self.experiment_versions.get(m.group(1), []))

        # -- events (fold #10, read-only) --
        if path == "/v1/events" and method == "GET":
            return httpx.Response(200, json=[])
        m = re.match(r"^/v1/runs/([^/]+)/events$", path)
        if m and method == "GET":
            return httpx.Response(200, json=self.run_events.get(m.group(1), []))

        # -- artifact upload flow (fold #16) --
        m = re.match(r"^/v1/runs/([^/]+)/artifacts/uploads$", path)
        if m and method == "POST":
            if self.fail_next_uploads:
                self.fail_next_uploads = False
                return httpx.Response(503, json={"detail": "storage down"})
            rid = m.group(1)
            ch = body["content_hash"]
            aid = str(uuid.uuid4())
            have = ch in self.uploaded
            art = {
                "id": aid,
                "run_id": rid,
                "name": body["name"],
                "content_hash": ch,
                "size_bytes": body.get("size_bytes"),
                "kind": (body.get("kind") or "file").strip().lower(),
                "meta": body.get("meta"),
                "step_index": body.get("step_index"),
                "span_id": body.get("span_id"),
                "status": "complete" if have else "pending",
                "is_reference": False,
            }
            self.artifacts.setdefault(rid, []).append(art)
            return httpx.Response(
                201,
                json={
                    "artifact_id": aid,
                    "have": have,
                    "upload_url": None if have else f"{self.upload_base}/put/{aid}",
                    "key": f"lab-42/{aid}",
                    "upload_headers": getattr(self, "upload_headers", {}),
                },
            )
        # -- the other three anchors: project / experiment / workspace / shared --
        # ScopedUploadRequest is declared extra="forbid", so anything run-only that
        # reaches here is a 422 — the client is supposed to have refused it first, and
        # this is what proves the client actually does. `notes` is IN the allowlist
        # (0095): it is the one descriptive field this contract accepts, and the
        # absence of it is what drove agents to concatenate descriptions onto `name`.
        for pattern, anchor in (
            (_PROJ_ARTIFACT_UPLOADS, "project"),
            (_EXP_ARTIFACT_UPLOADS, "experiment"),
            (_WS_FILE_UPLOADS, "workspace"),
        ):
            m = pattern.match(path)
            if m and method == "POST":
                extras = sorted(
                    set(body) - {"name", "content_hash", "size_bytes", "content_type", "notes"}
                )
                if extras:
                    return httpx.Response(
                        422, json={"detail": f"extra fields not permitted: {extras}"}
                    )
                return self._presign(anchor, m.group(1), body)
        if path == "/v1/shared/files/uploads" and method == "POST":
            extras = sorted(
                set(body) - {"name", "content_hash", "size_bytes", "content_type", "notes"}
            )
            if extras:
                return httpx.Response(422, json={"detail": f"extra fields not permitted: {extras}"})
            return self._presign("shared", "team", body)

        # -- papers (0152) ------------------------------------------------
        # `papers` is a dict keyed by project id, so a test can seed one
        # project's literature without touching another's — the view is
        # project-anchored and nothing else, and a shared list would let a
        # cross-project bug pass.
        m = _PROJ_PAPERS.match(path)
        if m:
            project_id = m.group(1)
            if method == "POST":
                if not str(body.get("source_url") or "").strip():
                    return httpx.Response(
                        422,
                        json={"detail": "source_url must be a non-blank file path or URL"},
                    )
                row = {
                    "id": str(uuid.uuid4()),
                    "customer_id": "lab-42",
                    "project_id": project_id,
                    "title": body["title"],
                    "authors": body.get("authors"),
                    "source_url": body.get("source_url"),
                    "repo_url": body.get("repo_url"),
                    "summary_md": body.get("summary_md"),
                    "discrepancies_md": body.get("discrepancies_md"),
                    # 0176. Canonicalized HERE because the real server does: a
                    # fake that echoed the raw list back would let the SDK's
                    # write-verification guard pass against a shape production
                    # never returns, which is the exact failure the guard is for.
                    "tags": _canonical_tags(body.get("tags") or []),
                    "extracted_title": None,
                    "extracted_abstract": None,
                    "extraction_metadata": None,
                    "created_at": self._stamp(),
                    "updated_at": self._stamp(),
                }
                self.papers.setdefault(project_id, []).append(row)
                return httpx.Response(201, json=row)
            if method == "GET":
                rows = [
                    {
                        key: value
                        for key, value in row.items()
                        if key
                        not in {
                            "extracted_title",
                            "extracted_abstract",
                            "extraction_metadata",
                        }
                    }
                    for row in self.papers.get(project_id, [])
                ]
                # AND-containment, both sides canonical — the same filter the
                # real route applies. A fake that IGNORED `tags=` would look
                # exactly like the pre-0176 backend the SDK guard exists to
                # refuse, so every filtered read here would fail for the wrong
                # reason.
                wanted = _canonical_tags(request.url.params.get_list("tags"))
                if wanted:
                    rows = [
                        row
                        for row in rows
                        if set(wanted) <= set(_canonical_tags(row.get("tags") or []))
                    ]
                return httpx.Response(
                    200, json=_newest_first(rows)
                )

        for pattern, anchor in (
            (_PROJ_ARTIFACTS, "project"),
            (_EXP_ARTIFACTS, "experiment"),
        ):
            m = pattern.match(path)
            if m and method == "POST":
                aid = str(uuid.uuid4())
                row = {
                    "id": aid,
                    "name": body["name"],
                    "uri": body.get("uri"),
                    "is_reference": bool(body.get("is_reference")),
                    "kind": body.get("kind") or "file",
                    "status": "complete",
                    # `meta` is PERSISTED, like ExperimentArtifactCreate/
                    # ProjectArtifactCreate declare and apply_artifact stores. The fake
                    # used to drop it, which is the shape of guard that certifies its
                    # own rot: a research note IS its `meta`, so a note test would have
                    # gone green against a fake that threw the note away.
                    "meta": body.get("meta") or {},
                    "created_at": self._stamp(),
                    f"{anchor}_id": m.group(1),
                }
                self.artifacts.setdefault(f"{anchor}:{m.group(1)}", []).append(row)
                return httpx.Response(201, json=row)
            if m and method == "GET":
                return httpx.Response(
                    200, json=_newest_first(self.artifacts.get(f"{anchor}:{m.group(1)}", []))
                )

        m = _WS_FILES.match(path)
        if m and method == "GET":
            # `ORDER BY name ASC` under the C collation (code-point order), and
            # `limit` (le=1000) caps one read, like the real route; no cursor.
            rows = sorted(
                self.artifacts.get(f"workspace:{m.group(1)}", []), key=lambda r: str(r["name"])
            )
            if (cap := request.url.params.get("limit")) is not None:
                rows = rows[: int(cap)]
            return httpx.Response(200, json=rows)

        if path == "/v1/shared/files" and method == "GET":
            # `prefix` is a FOLDER filter, and this fake models that EXACTLY,
            # because the kind version certifies broken code. The backend derives
            # `path` as the DIRNAME of `name` (0029, GENERATED column) and matches
            # `path = prefix OR path LIKE 'prefix/%'` -- so a root-level file has
            # path '' and a prefix of its own NAME matches nothing. A fake that
            # did startswith() on `name` instead would make a client that passes
            # the whole name look correct, and that client returns "no such
            # artifact" for every flat-named scorer -- read downstream as licence
            # to create a duplicate.
            # `ORDER BY name ASC` under the C collation: code-point order.
            rows = sorted(self.artifacts.get("shared:team", []), key=lambda r: str(r["name"]))
            if (want := request.url.params.get("prefix")) is not None:
                want = want.rstrip("/")
                if want:

                    def _dirname(row: dict) -> str:
                        nm = str(row.get("name", ""))
                        return nm.rsplit("/", 1)[0] if "/" in nm else ""

                    rows = [
                        a for a in rows if _dirname(a) == want or _dirname(a).startswith(f"{want}/")
                    ]
            # `limit` (le=1000) caps one read, like the real route; no cursor.
            if (cap := request.url.params.get("limit")) is not None:
                rows = rows[: int(cap)]
            return httpx.Response(200, json=rows)

        m = _SHARED_FILE_SUB.match(path)
        if m and method in ("POST", "GET"):
            aid, verb = m.group(1), m.group(2)
            row = self._find_artifact(aid)
            if row is None:
                return httpx.Response(404, json={"detail": "not found"})
            if verb == "download":
                return httpx.Response(200, json={"download_url": f"http://r2.test/get/{aid}"})
            if verb == "confirm":
                row["status"] = "complete"
                return httpx.Response(200, json=row)
            # Unshare uses the same default as an unscoped project create.
            workspace_id = self._default_workspace_id()
            self.artifacts.get("shared:team", []).remove(row)
            row["workspace_id"] = workspace_id
            row.pop("shared_folder_id", None)
            self.artifacts.setdefault(f"workspace:{workspace_id}", []).append(row)
            return httpx.Response(200, json=row)

        m = _SHARED_FILE_ITEM.match(path)
        if m and method == "DELETE":
            row = self._find_artifact(m.group(1))
            if row is None:
                return httpx.Response(404, json={"detail": "not found"})
            self.artifacts.get("shared:team", []).remove(row)
            return httpx.Response(204)

        m = _WS_FILE_SHARE.match(path)
        if m and method == "POST":
            aid = m.group(1)
            row = self._find_artifact(aid)
            if row is None:
                return httpx.Response(404, json={"detail": "not found"})
            # Ownership-transfer MOVE: it leaves the workspace listing entirely.
            for key, rows in self.artifacts.items():
                if key.startswith("workspace:") and row in rows:
                    rows.remove(row)
            self.artifacts.setdefault("shared:team", []).append(row)
            return httpx.Response(200, json=row)

        if path.startswith("/put/") and method == "PUT":
            aid = path.rsplit("/", 1)[-1]
            art = next((a for arts in self.artifacts.values() for a in arts if a.get("id") == aid), None)
            if art is not None and art.get("name") in self.fail_put_names:
                return httpx.Response(503, text="store unavailable")
            if art is not None and art.get("name") in self.reject_put_names:
                return httpx.Response(400, text="BadDigest")
            if self.throttle_put_once:
                self.throttle_put_once = False
                return httpx.Response(429, text="slow down")
            self.puts.append(path)
            self.put_headers.append(dict(request.headers))
            self.blobs[aid] = request.content or b""
            if art is not None and art.get("content_hash"):
                self.blobs_by_hash[art["content_hash"]] = request.content or b""
            return httpx.Response(200)
        m = re.match(r"^/v1/artifacts/([^/]+)/move$", path)
        if m and method == "POST":
            return self._move_artifact(m.group(1), body or {})

        # -- per-file code capture (0193): the batch doors ------------------
        m = re.match(r"^/v1/runs/([^/]+)/artifacts/uploads/batch$", path)
        if m and method == "POST":
            if not self.batch_doors:
                return httpx.Response(404, json={"detail": "Not Found"})
            if self.fail_next_uploads:
                # 500, not 503: the batch doors are idempotent and the client
                # retries 502/503/504 on its own, so a one-shot 503 would just
                # be absorbed. This knob means "the server failed", not "blip".
                self.fail_next_uploads = False
                return httpx.Response(500, json={"detail": "storage down"})
            rid = m.group(1)
            self.capture_batches.append(body)
            items_out: list[dict] = []
            n_have = n_need = n_rejected = 0
            for it in body.get("items") or []:
                # The server canonicalises names to NFC and echoes that form.
                name = unicodedata.normalize("NFC", it["name"])
                if name in self.reject_capture_names:
                    n_rejected += 1
                    items_out.append(
                        {
                            "name": name,
                            "artifact_id": None,
                            "have": False,
                            "upload_url": None,
                            "upload_headers": {},
                            "error": "name refused by the fake",
                        }
                    )
                    continue
                ch = it["content_hash"]
                have = ch in self.uploaded
                rows = self.artifacts.setdefault(rid, [])
                art = next(
                    (a for a in rows if a.get("name") == name and a.get("content_hash") == ch),
                    None,
                )
                if art is None:
                    art = {
                        "id": str(uuid.uuid4()),
                        "run_id": rid,
                        "name": name,
                        "content_hash": ch,
                        "size_bytes": it.get("size_bytes"),
                        "kind": "code",
                        "meta": {"capture": "code-snapshot", "mode": it.get("mode", "100644")},
                        "status": "pending",
                        "is_reference": False,
                        "created_at": body.get("captured_at"),
                    }
                    rows.append(art)
                if have:
                    art["status"] = "complete"
                    n_have += 1
                else:
                    n_need += 1
                items_out.append(
                    {
                        "name": name,
                        "artifact_id": art["id"],
                        "have": have,
                        # A real presigned URL carries its signature in the
                        # query; nothing the client records may echo it.
                        "upload_url": None
                        if have
                        else f"{self.upload_base}/put/{art['id']}?X-Amz-Signature=FAKESIG",
                        "upload_headers": getattr(self, "upload_headers", {}),
                        "error": None,
                    }
                )
            return httpx.Response(
                201,
                json={
                    "run_id": rid,
                    "items": items_out,
                    "n_have": n_have,
                    "n_need": n_need,
                    "n_rejected": n_rejected,
                },
            )
        if path == "/v1/artifacts/confirm/batch" and method == "POST":
            ids = list(body.get("artifact_ids") or [])
            self.confirm_batches.append(ids)
            if self.unconfirm_once:
                self.unconfirm_once = False
                return httpx.Response(
                    200,
                    json={
                        "confirmed": [],
                        "unconfirmed": ids,
                        "refused": [],
                        "unknown": [],
                        "failed": [],
                    },
                )
            confirmed, unconfirmed, refused, unknown, failed = [], [], [], [], []
            for aid in ids:
                art = next((a for arts in self.artifacts.values() for a in arts if a.get("id") == aid), None)
                if art is None:
                    unknown.append(aid)
                    continue
                if (art.get("meta") or {}).get("capture") != "code-snapshot":
                    refused.append(aid)
                    continue
                if art.get("name") in self.fail_capture_names:
                    art["status"] = "failed"
                    failed.append(aid)
                    continue
                # HEAD emulation: the object exists iff a PUT landed for this id.
                if art["status"] == "complete" or aid in self.blobs:
                    art["status"] = "complete"
                    self.uploaded.add(art["content_hash"])
                    confirmed.append(aid)
                else:
                    unconfirmed.append(aid)
            return httpx.Response(
                200,
                json={
                    "confirmed": confirmed,
                    "unconfirmed": unconfirmed,
                    "refused": refused,
                    "unknown": unknown,
                    "failed": failed,
                },
            )
        if path == "/v1/artifacts/download/batch" and method == "POST":
            ids = list(body.get("artifact_ids") or [])
            known = {a["id"]: a for arts in self.artifacts.values() for a in arts}
            items, refused = {}, {}
            for aid in ids:
                art = known.get(aid)
                if art is None:
                    continue
                if art.get("status") != "complete":
                    refused[aid] = f"artifact is {art.get('status')}, not complete"
                elif art.get("is_reference"):
                    refused[aid] = "reference"
                else:
                    items[aid] = {"download_url": f"http://r2.test/get/{aid}?X-Amz-Signature=FAKESIG"}
            return httpx.Response(
                200,
                json={
                    "items": items,
                    "unknown": [aid for aid in ids if aid not in known],
                    "refused": refused,
                },
            )
        m = re.match(r"^/v1/runs/([^/]+)/artifacts/tree$", path)
        if m and method == "GET":
            prefix = (request.url.params.get("prefix") or "").rstrip("/")
            limit = int(request.url.params.get("limit") or 1000)
            rows = [a for a in self.artifacts.get(m.group(1), []) if a.get("status") != "deleted"]
            files, folders = [], {}
            for a in rows:
                name = a.get("name") or ""
                folder = name.rsplit("/", 1)[0] if "/" in name else ""
                if folder == prefix:
                    files.append(a)
                elif not prefix or folder.startswith(prefix + "/"):
                    rest = folder[len(prefix) + 1 :] if prefix else folder
                    child = rest.split("/", 1)[0]
                    folders[child] = folders.get(child, 0) + 1
            files_sorted = sorted(files, key=lambda a: a["name"])
            folders_sorted = [
                {"name": k, "path": f"{prefix}/{k}" if prefix else k, "count": v}
                for k, v in sorted(folders.items())
            ]
            return httpx.Response(
                200,
                json={
                    "prefix": prefix,
                    "files": files_sorted[:limit],
                    "folders": folders_sorted[:limit],
                    "truncated": len(files_sorted) > limit or len(folders_sorted) > limit,
                },
            )
        m = re.match(r"^/v1/artifacts/([^/]+)/confirm$", path)
        if m and method == "POST":
            aid = m.group(1)
            for arts in self.artifacts.values():
                for a in arts:
                    if a.get("id") == aid:
                        a["status"] = "complete"
                        if a.get("content_hash"):
                            self.uploaded.add(a["content_hash"])
                        return httpx.Response(200, json=a)
            return httpx.Response(404, json={"detail": "not found"})

        # artifact download (presigned GET) -> used by asset materialize
        m = re.match(r"^/v1/artifacts/([^/]+)/download$", path)
        if m and method == "POST":
            return httpx.Response(200, json={"download_url": f"http://r2.test/get/{m.group(1)}"})
        if path.startswith("/get/") and method == "GET":
            self.gets.append(path)
            aid = path.rsplit("/", 1)[-1]
            blob = self.blobs.get(aid)
            if blob is None:
                art = next((a for arts in self.artifacts.values() for a in arts if a.get("id") == aid), None)
                if art is not None and art.get("content_hash") in self.blobs_by_hash:
                    blob = self.blobs_by_hash[art["content_hash"]]
            return httpx.Response(200, content=blob if blob is not None else b"ASSET-BYTES")

        if path == "/ingest/v1/runs" and method == "POST":
            rid = str(uuid.uuid4())
            run = body["run"]
            row = self._new_run(
                rid, "exp", {"name": run["name"], "source": run.get("source", "api")}
            )
            return httpx.Response(200, json=row)

        return httpx.Response(404, json={"detail": f"no fake route for {method} {path}"})

    @staticmethod
    def _creation_fingerprint(path: str, body: dict) -> str:
        """Mirror of app/runs/router.py::_creation_fingerprint: the container
        (here, the path) plus the body as sent, minus the key itself."""
        rest = {k: v for k, v in (body or {}).items() if k != "creation_key"}
        return json.dumps([path, rest], sort_keys=True, separators=(",", ":"))

    def _creation_replay(self, path: str, body: dict) -> httpx.Response | None:
        """Mirror of the server's 0268 lookup: the run a creation key already
        made (201 + `Idempotent-Replay`), a 422 for the key on another request,
        or None to create. A server without the feature ignores the key."""
        key = (body or {}).get("creation_key")
        if not self.supports_creation_key or key is None or key not in self.creation_keys:
            return None
        run_id, fingerprint = self.creation_keys[key]
        if fingerprint != self._creation_fingerprint(path, body):
            return httpx.Response(
                422,
                json={
                    "detail": {
                        "code": "creation_key_reused",
                        "message": "this creation_key already created a different run request",
                    }
                },
            )
        return httpx.Response(201, json=self.runs[run_id], headers={"Idempotent-Replay": "true"})

    def _remember_creation(self, path: str, body: dict, run_id: str) -> None:
        key = (body or {}).get("creation_key")
        if self.supports_creation_key and key is not None:
            self.creation_keys[key] = (run_id, self._creation_fingerprint(path, body))

    def _run_external_id_conflict(self, body: dict) -> httpx.Response | None:
        """Mirror the engine's UNIQUE (customer_id, source, external_id): without
        this the fake happily mints duplicate run identities and the supersede
        path in ``run(on_conflict=...)`` has nothing real to test against."""
        ext = (body or {}).get("external_id")
        if ext is None:
            return None
        source = (body or {}).get("source", "api")
        for _row in self.runs.values():
            if _row.get("external_id") == ext and _row.get("source", "api") == source:
                return httpx.Response(
                    409,
                    json={
                        "detail": {
                            "message": "run with this (source, external_id) already exists",
                            "existing_id": _row["id"],
                        }
                    },
                )
        return None

    def _new_run(
        self,
        rid: str,
        experiment_id: str | None,
        body: dict,
        *,
        project_id: str | None = None,
        floating: bool = False,
    ) -> dict:
        # RunDetailOut shape (fold fields surfaced on /v1 reads). project_id is
        # set on every FILED run (0054); the fake defaults one so old seeds stay
        # valid. A floating run (daemon v2) carries the key, null.
        #
        # Bound once: the server derives an unnamed run's NAME from the same slug
        # it stores, so computing it twice here could let the two drift and make a
        # naming test pass against a fiction.
        _slug = body.get("slug") or f"run-{rid[:8]}"
        row = {
            "id": rid,
            "experiment_id": experiment_id,
            "project_id": None if floating else (project_id or str(uuid.uuid4())),
            # Mirrors app/runs/service.py `write_run` + `RunWrite.name_customized`:
            # an unnamed run is named after the caller's slug (or the petname the
            # server mints), and ONLY a caller-supplied name stamps the flag. The
            # fake modelled neither before, which is exactly why nothing caught the
            # SDK fabricating `run-<timestamp>` into every create.
            "name": body["name"] if body.get("name") is not None else _slug,
            # 0170: a name LOCKS the row only when nobody declares otherwise.
            # `owns_field` is the server's rule and this is its only mirror --
            # `_owns_field` below is pinned against a truth table in
            # test_authorship_default.py, because a fake that disagrees with the
            # server makes a naming test pass against a fiction.
            "name_customized": _owns_field(body.get("name"), body.get("authored_by")),
            "description": body.get("description"),
            # 0205: a hand-off opens the row for a job that has not started.
            "status": "created" if body.get("awaiting_attach") else "running",
            # 0205: liveness_mode is DERIVED, never taken from the body. Mirrors
            # app/runs/liveness.py::derive_mode. `last_heartbeat_at` is added
            # below only when a beat actually landed at insert -- this fake has
            # always omitted the key until something beat, and several tests
            # read that absence as "nothing has asserted liveness".
            "liveness_mode": (
                None
                if body.get("awaiting_attach")
                # 0269: an offline create (plan 2.12) reads 'offline'.
                else "offline"
                if body.get("offline") and self.supports_offline_create
                else (
                    "wrapped"
                    if body.get("heartbeat")
                    and (body.get("launcher") or (body.get("metadata") or {}).get("launch"))
                    else "in-process"
                    if body.get("heartbeat")
                    else "legacy"
                )
            ),
            "source": body.get("source", "api"),
            "external_id": body.get("external_id"),
            "tags": body.get("tags", []),
            "metadata": body.get("metadata", {}),
            "config": body.get("config", {}),
            "parent_run_id": body.get("parent_run_id"),
            "parent_relation": body.get("parent_relation"),
            "group_id": body.get("group_id"),
            # Mirrors the engine: a caller-chosen `slug` lands in slug (0.110.0.0).
            "slug": _slug,
            "foreign_keys": body.get("foreign_keys", {}),
            "env_ref": body.get("env_ref"),
            "created_by": "ingest:test",
            # Required on the real RunDetailOut, so read responses match the
            # contract rather than a leaner fiction.
            "customer_id": "lab-42",
            "created_at": self._stamp(),
            # 0106 capability marker: a server that knows observer heartbeats
            # always serializes this key (null until stamped). The SDK's
            # observer capability probe keys on its PRESENCE, so the fake must
            # carry it or every observer-beat test would read the fake as a
            # pre-0106 server and silently not beat.
            "observer_heartbeat_at": None,
            # 0205: always serialized, like the real RunDetailOut. Null means
            # nothing INSIDE the work has reported yet.
            "attached_at": None,
            # 0185: RunDetailOut always serializes the epoch (1 on a fresh
            # row), and a handle reads it to know the generation it writes
            # under. A fake without it models no server that exists.
            "write_epoch": 1,
        }
        # 0205: a create that declares an owner gets the beat stamped AT INSERT,
        # which is the signal the server's derivation reads. Added conditionally
        # because this fake's contract has always been that the key is ABSENT
        # until something beat, and tests read that absence as "nothing has
        # asserted liveness on this run".
        if body.get("heartbeat") and not body.get("awaiting_attach"):
            row["last_heartbeat_at"] = self._stamp()
            self.run_heartbeats[rid] = self.run_heartbeats.get(rid, 0) + 1
        if self.stores_entity_notes:
            row["notes"] = body.get("notes")
        if body.get("started_at") and self.supports_offline_create:
            # 0269: an offline run's REAL start rides on the create. (This fake
            # has never serialized `started_at` otherwise; a server without the
            # feature drops the field.)
            row["started_at"] = body["started_at"]
        # 2.8, mirroring app/runs/router.py: `leases` + the creating writer's
        # lease in the create's own transaction.
        row["liveness_protocol"] = body.get("liveness_protocol")
        if body.get("writer"):
            self._upsert_lease(rid, body["writer"], epoch=1)
        self.runs[rid] = row
        return row

    # -- 2.8 leases, mirroring app/runs/writers.py ------------------------------
    _LEASE_FIELDS = (
        "role", "host", "pid", "rank", "local_rank", "world_size", "interactive",
        "interval_seconds",
    )

    def _upsert_lease(self, rid: str, body: dict, *, epoch: int, session: str | None = None):
        session = str(session or body["session_id"])
        leases = self.leases.setdefault(rid, {})
        lease = leases.get(session)
        if lease is not None and (lease.get("released_at") or lease.get("gone_at")):
            return None  # never revived
        if lease is None:
            lease = leases[session] = {
                "session_id": session, "progress": 0, "released_at": None,
                "exit_status": None, "gone_at": None, "draining": False, "beats": 0,
            }
        lease["write_epoch"] = max(int(lease.get("write_epoch") or 0), int(epoch))
        for key in self._LEASE_FIELDS:
            if body.get(key) is not None:
                lease[key] = body[key]
        if body.get("progress") is not None:
            lease["progress"] = max(lease["progress"], int(body["progress"]))
        for key in ("progress_idle_seconds", "progress_gap_p99_seconds", "progress_longest_gap_seconds"):
            if body.get(key) is not None:
                lease[key] = body[key]
        if body.get("draining_for_seconds") is not None:
            lease["draining"] = True
        lease["beats"] += 1
        return lease

    def _close_by_leases(self, rid: str, *, allow_crashed: bool = False) -> bool:
        """Rules 1-3 with the fake's clock: an unreleased, not-gone lease is
        live (tests age leases by marking them `expired`). ``allow_crashed``:
        a release re-decides a run the system ended `crashed`."""
        row = self.runs[rid]
        open_statuses = ("running", "crashed") if allow_crashed else ("running",)
        if row.get("status") not in open_statuses or row.get("liveness_protocol") != "leases":
            return False
        epoch = int(row.get("write_epoch", 1))
        current = [w for w in self.leases.get(rid, {}).values() if int(w["write_epoch"]) == epoch]
        if not current:
            return False
        released = [w for w in current if w["released_at"]]
        gone = [w for w in current if w["gone_at"]]
        enders = [w for w in released if w.get("role") in ("owner", "launcher")]
        if not (enders or gone or len(released) == len(current)):
            return False
        launchers = [w for w in current if w.get("role") == "launcher"]
        if launchers and not all(w["released_at"] for w in launchers):
            return False
        live = [
            w for w in current
            if not w["released_at"] and not w["gone_at"] and not w.get("expired")
        ]
        if live:
            return False
        worst = {"crashed": 3, "failed": 2, "canceled": 1, "completed": 0}
        verdicts = [w["exit_status"] for w in released] + ["crashed"] * len(gone)
        verdict = max(verdicts, key=lambda v: worst.get(v, 0))
        if verdict == row["status"]:
            return False
        row["status"] = verdict
        row["ended_at"] = self._stamp()
        return True


#: `POST /v1/runs/{id}/outputs` rows (lineage plan 3's shared contract): these
#: keys, exactly.
RUN_OUTPUT_KEYS = (
    "path", "host", "content_hash", "fingerprint", "size_bytes",
    "first_written_at", "last_modified_at", "observation_id",
)


def run_outputs_problems(batch) -> list[str]:
    """Why a `/outputs` body breaks the contract (empty: it keeps it):
    ``{"outputs": [row...], "coverage": {...}}`` with each row exactly
    `RUN_OUTPUT_KEYS` -- path str (<= 2048 UTF-8 bytes), host str|null,
    content_hash sha256 hex or "", fingerprint str|null, size_bytes int >= 0
    |null, first_written_at / last_modified_at ISO instants, observation_id
    str -- at most 2,000 rows, coverage a small object."""
    from datetime import datetime

    problems: list[str] = []
    if not isinstance(batch, dict) or set(batch) - {"outputs", "coverage"}:
        return [f"body keys: {sorted(batch) if isinstance(batch, dict) else type(batch)}"]
    rows = batch.get("outputs")
    if not isinstance(rows, list) or len(rows) > 2000:
        return ["outputs must be a list of at most 2000 rows"]
    coverage = batch.get("coverage")
    if coverage is not None and (not isinstance(coverage, dict) or len(json.dumps(coverage)) > 4000):
        problems.append("coverage must be a small object")
    for i, row in enumerate(rows):
        if not isinstance(row, dict) or tuple(sorted(row)) != tuple(sorted(RUN_OUTPUT_KEYS)):
            problems.append(f"row {i} keys: {sorted(row) if isinstance(row, dict) else row!r}")
            continue
        if not isinstance(row["path"], str) or not row["path"] or len(row["path"].encode()) > 2048:
            problems.append(f"row {i} path")
        if row["host"] is not None and not isinstance(row["host"], str):
            problems.append(f"row {i} host")
        sha = row["content_hash"]
        if not (sha == "" or (isinstance(sha, str) and re.fullmatch(r"[0-9a-f]{64}", sha))):
            problems.append(f"row {i} content_hash {sha!r}")
        if row["fingerprint"] is not None and not isinstance(row["fingerprint"], str):
            problems.append(f"row {i} fingerprint")
        size = row["size_bytes"]
        if size is not None and (type(size) is not int or size < 0):
            problems.append(f"row {i} size_bytes")
        for key in ("first_written_at", "last_modified_at"):
            try:
                stamp = datetime.fromisoformat(str(row[key]).replace("Z", "+00:00"))
                if stamp.tzinfo is None:
                    raise ValueError("naive")
            except ValueError:
                problems.append(f"row {i} {key} {row[key]!r}")
        if not isinstance(row["observation_id"], str) or not row["observation_id"]:
            problems.append(f"row {i} observation_id")
    return problems


def _is_uuid_text(value: str) -> bool:
    try:
        uuid.UUID(value)
    except ValueError:
        return False
    return True


def make_client(
    app: FakeApp,
    *,
    fail_open: bool = True,
    tmp_spool=None,
    async_writes: bool = False,
    **client_kwargs,
) -> Client:
    settings = Settings(
        base_url="http://test",
        token="ros_pat_deadbeef",
        ingest_token="ros_ing_cafef00d",
        hmac_secret="s3cr3t",
    )
    httpx_client = httpx.Client(base_url="http://test", transport=httpx.MockTransport(app.handler))
    transport = Transport(settings, client=httpx_client)
    from probe.sdk.journal import Journal

    # ALWAYS an isolated journal: the default would be the developer's real
    # ~/.local/state/probe/outbox, and Journal._ensure imports any real legacy
    # spool it finds -- a test must never touch either.
    journal = Journal(
        tmp_spool if tmp_spool else tempfile.mkdtemp(prefix="probe-test-journal-"),
        context={"name": None, "base_url": settings.base_url},
    )
    return Client(
        settings=settings,
        transport=transport,
        fail_open=fail_open,
        journal=journal,
        async_writes=async_writes,
        **client_kwargs,
    )


@pytest.fixture(autouse=True)
def _fresh_secret_gate_caches():
    """The gate caches verdicts per process (by sha256 and scan policy), and the
    scrubber caches `scrub_string` / `is_sensitive_key` answers. Tests that
    monkeypatch the scanner must not be answered from a verdict or a scrub an
    earlier test cached for the same input."""
    from probe.sdk import redaction, secret_gate

    # The scrub cache's switches too: `Client.run` turns it on and the hosted MCP
    # app forbids it for the process, and neither may carry into the next test.
    switches = (redaction._CACHE_ENABLED, redaction._CACHE_FORBIDDEN)
    secret_gate.clear_caches()
    redaction.clear_caches()
    yield
    secret_gate.clear_caches()
    redaction.clear_caches()
    redaction._CACHE_ENABLED, redaction._CACHE_FORBIDDEN = switches


@pytest.fixture(autouse=True)
def _no_real_outbox(monkeypatch, tmp_path_factory):
    """Point every durable-state path away from the developer's real
    ~/.local/state. The every-command banner reads the outbox, the drainer
    re-kick would SPAWN against it, and Journal._ensure imports -- AND THEN
    DELETES -- any legacy spool it finds via PROBE_SPOOL_DIR/XDG_STATE_HOME
    (testing review: isolating only PROBE_OUTBOX_DIR left the real spool
    reachable). None of it may be touched by a test."""
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(tmp_path_factory.mktemp("outbox-guard")))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path_factory.mktemp("state-guard")))
    monkeypatch.delenv("PROBE_SPOOL_DIR", raising=False)


@pytest.fixture(autouse=True)
def _short_finish_deadline(monkeypatch):
    """`Run.finish()` retries undelivered writes for up to 600 s by default
    (plan 0.2) before it defers the close. A test whose fake transport is down
    would spend all of that in real sleep, so the suite runs with a short
    default. Tests ABOUT the default read `probe.sdk.run.FINISH_TIMEOUT_DEFAULT_SECONDS`
    through their own monkeypatch or pass `flush_timeout=` explicitly; this
    never touches `PROBE_FINISH_TIMEOUT_SEC`, which also bounds output capture."""
    monkeypatch.setattr("probe.sdk.run.FINISH_TIMEOUT_DEFAULT_SECONDS", 2.0)


@pytest.fixture(autouse=True)
def _no_exit_promotion(monkeypatch):
    """A queued upload arms an atexit promotion that can SPAWN a detached
    worker after pytest has exited and every monkeypatch is undone -- one that
    then reads the developer's real config. Tests that exercise the hook point
    `probe.sdk.client._at_exit` at a list of their own."""
    monkeypatch.setattr("probe.sdk.client._at_exit", lambda callback: None)


@pytest.fixture(autouse=True)
def _sigterm_handler_restored():
    """`probe.init()` puts the SIGTERM flush (`probe.sdk.preempt`) in front of
    SIGTERM for as long as a run is open. A test that leaves a run open would
    leave it installed in the pytest process -- and an xdist worker told to
    stop would then try to close that run. Put back what was there, and forget
    the handler's state, after every test."""
    import signal

    from probe.sdk import preempt

    before = signal.getsignal(signal.SIGTERM)
    yield
    try:
        if signal.getsignal(signal.SIGTERM) is not before and before is not None:
            signal.signal(signal.SIGTERM, before)
    except (ValueError, OSError):
        pass
    commands = preempt._state.commands
    if commands is not None:
        commands.put(("stop",))
    preempt._reset()


@pytest.fixture(autouse=True)
def _no_background_heartbeat(monkeypatch):
    """create_run starts a heartbeat thread by default; a background beat landing
    between an action and its `app.requests[-1]` assertion would make half this
    suite flaky. Kill it globally; tests that exercise liveness re-enable it with
    an explicit interval (the argument outranks the env var)."""
    monkeypatch.setenv("PROBE_HEARTBEAT_SECONDS", "0")


@pytest.fixture(autouse=True)
def _no_output_capture(monkeypatch):
    """Output capture (D17) is on by default: every client.run() in this suite
    would list the working tree at open, sweep it at close and tee the test
    process's own file descriptors. Tests that exercise capture turn it on
    explicitly (the argument outranks the env var)."""
    monkeypatch.setenv("PROBE_CAPTURE_OUTPUTS", "0")
    monkeypatch.delenv("PROBE_CAPTURE_OWNER", raising=False)
    monkeypatch.delenv("PROBE_CAPTURE_ROOT", raising=False)


@pytest.fixture(autouse=True)
def _no_auto_snapshot(monkeypatch):
    """Auto-snapshot (Task 8) would make every client.run() in this suite
    snapshot the working tree. Tests that exercise the auto path re-enable it
    explicitly."""
    monkeypatch.setenv("PROBE_AUTO_SNAPSHOT", "0")


def make_pushed_repo(tmp_path):
    """A working tree with a pushed remote, one clean file, one edited, one
    untracked -- three files git cannot supply. Shared by the snapshot suites."""
    import subprocess

    def _git(cwd, *args):
        proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
        assert proc.returncode == 0, f"git {' '.join(args)}: {proc.stderr}"
        return proc.stdout.strip()

    remote = tmp_path / "remote.git"
    _git(tmp_path, "init", "--bare", "-q", str(remote))
    work = tmp_path / "work"
    work.mkdir()
    _git(work, "init", "-q")
    _git(work, "config", "user.email", "t@e.com")
    _git(work, "config", "user.name", "t")
    (work / "clean.py").write_text("UNCHANGED\n")
    (work / "train.py").write_text("print('v1')\n")
    _git(work, "add", "-A")
    _git(work, "commit", "-qm", "init")
    _git(work, "remote", "add", "origin", str(remote))
    _git(work, "push", "-q", "origin", "HEAD:main")
    (work / "train.py").write_text("print('v2 EDITED, uncommitted')\n")
    (work / "notes.txt").write_text("untracked\n")
    return work


@pytest.fixture(params=["archive", "artifacts"], ids=["archive", "artifacts"])
def code_storage(request, monkeypatch):
    """Run a storage-agnostic test under BOTH snapshot storages. Opt in with
    ``pytestmark = pytest.mark.usefixtures("code_storage")`` in a module whose
    assertions do not depend on the archive's shape."""
    from probe.sdk.run import CODE_STORAGE_ENV

    monkeypatch.setenv(CODE_STORAGE_ENV, request.param)
    return request.param


@pytest.fixture(autouse=True)
def _no_code_storage_leakage(monkeypatch):
    """PROBE_CODE_STORAGE is a real dev-shell export. Per-file storage is the
    default (since the CLI release after 0.140.0); the suite's many archive-path
    tests pin `archive` explicitly (the path stays supported), and the per-file
    tests set `artifacts` themselves. The default itself is pinned in
    test_snapshot_artifacts by deleting the variable."""
    from probe.sdk.run import CODE_STORAGE_ARCHIVE, CODE_STORAGE_ENV

    monkeypatch.setenv(CODE_STORAGE_ENV, CODE_STORAGE_ARCHIVE)


@pytest.fixture(autouse=True)
def _no_capture_enforcement_leakage(monkeypatch):
    """Strip PROBE_ENV_ALLOWLIST from every test's environment. It is a real
    dev-shell export (per-site env capture tuning) and is not otherwise
    isolated the way config/outbox state is -- a developer with it set in
    their shell would get extra captured env values with no test-visible
    cause. Tests that exercise this path set it explicitly, which wins over
    this."""
    monkeypatch.delenv("PROBE_ENV_ALLOWLIST", raising=False)


@pytest.fixture
def app() -> FakeApp:
    return FakeApp()


@pytest.fixture
def client(app: FakeApp, tmp_path) -> Client:
    return make_client(app, tmp_spool=tmp_path / "spool")


def open_run(client: Client, *, experiment: str, name: str | None = None, **run_kw):
    """Create the experiment, then open a run in it.

    `client.run()` does get-or-create its parents, so most of this is belt and
    braces — but creating an experiment needs a question, and these callers have
    no opinion about one. Seeding it here keeps every test that just needs *a run
    to exist* from having to invent a question it does not care about. Tests
    ABOUT identity resolution call create_experiment / run directly and assert on
    the behaviour."""
    from probe import errors as _errors

    project_slug = f"project-{experiment}"
    try:
        project = client.create_project(project_slug, kind="general")
    except _errors.ConflictError:
        project = client.resolve_project(project_slug)
        assert project is not None
    try:
        client.create_experiment(
            experiment,
            experiment,
            question="h",
            project_id=project["id"],
        )
    except _errors.ConflictError:
        pass
    return client.run(experiment=experiment, name=name, **run_kw)


def _git_for_fixture(cwd, *args):
    import subprocess

    proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    assert proc.returncode == 0, f"git {' '.join(args)}: {proc.stderr}"
    return proc.stdout.strip()


@pytest.fixture
def snapshot_repo(tmp_path):
    """A working tree with a pushed remote, one clean file, one edited, one
    untracked -- three files git cannot supply. Shared by the snapshot tests so
    a fourth copy of this fixture does not drift from the others."""
    remote = tmp_path / "remote.git"
    _git_for_fixture(tmp_path, "init", "--bare", "-q", str(remote))
    work = tmp_path / "work"
    work.mkdir()
    _git_for_fixture(work, "init", "-q")
    _git_for_fixture(work, "config", "user.email", "t@e.com")
    _git_for_fixture(work, "config", "user.name", "t")
    (work / "clean.py").write_text("UNCHANGED\n")
    (work / "train.py").write_text("print('v1')\n")
    _git_for_fixture(work, "add", "-A")
    _git_for_fixture(work, "commit", "-qm", "init")
    _git_for_fixture(work, "remote", "add", "origin", str(remote))
    _git_for_fixture(work, "push", "-q", "origin", "HEAD:main")
    (work / "train.py").write_text("print('v2 EDITED, uncommitted')\n")
    (work / "notes.txt").write_text("untracked\n")
    return work
