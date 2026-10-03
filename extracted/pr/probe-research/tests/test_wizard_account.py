"""`probe wizard` → Sign out: the credentials this device holds.

The wizard managed everything about a machine except WHOSE data it writes to.
Install could only ever add a credential (and skipped the browser entirely once
one existed, so a wrong-account install had no path forward), and the only thing
that cleared one was Uninstall, which takes the plugins with it.

Two failure modes are covered first here because they are the ones that lie:

- a sign-out that leaves capture running, still uploading this device's sessions
  to the account the user just left;
- a sign-out that reports success while an exported PROBE_TOKEN keeps the CLI
  authenticated, which no process can unset from inside the wizard.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from probe.cli import capture, doctor, setup
from probe.cli.actions import ACCOUNT_ACTIONS, ACTION_COPY, Action
from probe.cli.capabilities import Capabilities, TokenSource
from probe.sdk.config import load_context, load_file, save_context, use_context


@pytest.fixture(autouse=True)
def isolate(tmp_path, monkeypatch):
    """Point every credential path at a tmpdir so tests never touch a real install."""
    monkeypatch.setenv("PROBE_RESEARCH_TAP_PLUGIN_DIR", str(tmp_path / "tap"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "probe" / "config.json"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    for name in setup.ENV_CREDENTIALS:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.delenv("PROBE_BASE_URL", raising=False)
    (tmp_path / "tap").mkdir(parents=True, exist_ok=True)
    return tmp_path


def _caps(**overrides) -> Capabilities:
    return Capabilities(**overrides)


class _FakeClient:
    """Stands in for the SDK client wherever the account flow reaches the API.

    Records every revoke, because "did this actually revoke the token it
    replaced" is the assertion that matters most here -- a stranded device token
    stays valid on the server, and after the overwrite nobody holds a copy to
    revoke it with.
    """

    revoked: list[tuple[str, str]] = []
    email = "new@prbe.ai"
    fails = False

    def __init__(self, *, settings=None, **_kwargs):
        self.settings = settings

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        return False

    def me(self) -> dict:
        return {"email": self.email}

    def logout(self) -> None:
        if self.fails:
            raise RuntimeError("offline")
        _FakeClient.revoked.append((self.settings.base_url, self.settings.token))


@pytest.fixture
def api(monkeypatch):
    _FakeClient.revoked = []
    _FakeClient.fails = False
    _FakeClient.email = "new@prbe.ai"
    monkeypatch.setattr("probe.sdk.client.Client", _FakeClient)
    return _FakeClient


# --- the menu ---------------------------------------------------------------


def test_sign_in_and_sign_out_are_the_flag_spelling_of_the_account_screen():
    """A screen cannot be the contract for CI: it asks. These are what a script
    names instead, and they must never hang waiting for a keypress."""
    assert Action("login") is Action.SIGN_IN
    assert Action("logout") is Action.SIGN_OUT
    assert ACCOUNT_ACTIONS == {Action.ACCOUNT, Action.SIGN_IN, Action.SIGN_OUT}
    assert Action.SIGN_IN not in ACTION_COPY and Action.SIGN_OUT in ACTION_COPY


def test_the_action_flag_help_names_only_real_actions():
    """It used to advertise `remove`, which is not an Action -- so the flag the
    help text recommended for an unattended uninstall exited 2."""
    params = {p.name: p for p in _wizard_command().params}
    help_text = params["action"].help
    advertised = {value.strip() for value in help_text.partition(":")[2].split("|")}
    supported = {action.value for action in Action if action is not Action.EXIT}
    assert advertised == supported, "--action help must list every supported action exactly"


def _wizard_command():
    from typer.main import get_command

    import probe.cli.main  # noqa: F401

    group = get_command(sys.modules["probe.cli.main"].app)
    return group.commands["wizard"]


def test_the_state_summary_shows_the_account_even_when_signed_out():
    """ "not signed in" was the one account state the summary could not show, so
    the machine that most needs the account row never got one."""
    lines = setup.describe_state({"claude_code": _caps(agent_source="claude_code")})
    assert any("Account" in line and "not signed in" in line for line in lines)


def test_saved_accounts_marks_the_active_one():
    save_context({"base_url": "https://api.test", "token": "probe_pat_A"})
    save_context({"base_url": "https://staging.test"}, name="staging")

    accounts = {account.name: account for account in setup.saved_accounts()}

    assert accounts["default"].active is True and accounts["default"].has_token is True
    assert accounts["staging"].active is False and accounts["staging"].has_token is False
    assert "no credential saved" in accounts["staging"].describe()


def _menu_rows(monkeypatch, build):
    """Build a screen without a terminal and return its rows as (title, value)."""
    import questionary

    from probe.cli import tui

    seen: list = []

    def fake_select(message, *, choices, **kwargs):
        seen.extend(choices)
        return SimpleNamespace()

    monkeypatch.setattr(questionary, "select", fake_select)
    monkeypatch.setattr(tui, "ask", lambda question, **kwargs: None)
    build()
    # Separator subclasses Choice, so "is it a Choice" is not the question.
    return [
        (str(choice.title).splitlines()[0], choice.value)
        for choice in seen
        if not isinstance(choice, questionary.Separator)
    ]


def test_the_account_screen_only_offers_rows_that_mean_something(monkeypatch):
    """A menu that lists impossible options makes the reader work out which ones
    are real: no "switch" with one account saved, no "sign out" with none."""
    bare = _menu_rows(monkeypatch, lambda: setup.run_account_menu(_caps(), saved=[]))
    assert [value for _, value in bare] == [setup.AccountAction.BACK]

    saved = [
        setup.SavedAccount("default", "https://api.test", True, True),
        setup.SavedAccount("staging", "https://staging.test", True, False),
    ]
    full = _menu_rows(
        monkeypatch,
        lambda: setup.run_account_menu(_caps(logged_in_as="me@prbe.ai"), saved=saved),
    )
    assert [value for _, value in full] == [
        setup.AccountAction.SWITCH,
        setup.AccountAction.REMOVE,
        setup.AccountAction.SIGN_OUT,
        setup.AccountAction.BACK,
    ]
    assert [title for title, _ in full][:3] == [
        "Switch to an account saved here", "Remove a saved account", "Sign out",
    ]
    alone = _menu_rows(
        monkeypatch,
        lambda: setup.run_account_menu(_caps(logged_in_as="me@prbe.ai"), saved=saved[:1]),
    )
    assert [value for _, value in alone] == [setup.AccountAction.SIGN_OUT, setup.AccountAction.BACK], (
        "switching and removing act on OTHER accounts: no rows with only the active one"
    )


def test_the_switch_screen_lists_only_the_other_accounts(monkeypatch):
    from probe.cli import tui

    saved = [
        setup.SavedAccount("default", "https://api.test", True, True),
        setup.SavedAccount("staging", "https://staging.test", False, False),
    ]

    rows = _menu_rows(monkeypatch, lambda: setup.run_switch_menu(saved))

    assert [value for _, value in rows] == ["staging", tui.BACK]


def test_the_header_tells_offline_apart_from_signed_out():
    """`logged_in_as` is an email the API confirmed, so it is empty in BOTH
    cases -- and telling an offline researcher "not signed in" invites them to
    re-approve a device that was never signed out."""
    save_context({"base_url": "https://api.test", "token": "probe_pat_A"})

    offline = setup.describe_account(_caps(base_url="https://api.test"))
    assert any("could not reach the endpoint" in line for line in offline)

    empty = setup.describe_account(_caps(base_url="https://api.test"), saved=[])
    assert any("not signed in" in line for line in empty)


def test_sign_out_is_offered_offline_when_a_token_is_saved():
    """`logged_in_as` is a VERIFIED email, so it is None on a laptop with no
    network -- which is exactly when someone wants out of an account."""
    save_context({"base_url": "https://api.test", "token": "probe_pat_A"})

    assert setup.can_sign_out(_caps(), setup.saved_accounts()) is True
    assert setup.can_sign_out(_caps(), []) is False


# --- signing out ------------------------------------------------------------


def test_sign_out_revokes_the_stored_token_and_clears_the_context(api):
    """The token has to die on the SERVER too: once the local copy is gone the
    user has nothing left to revoke it with.

    BOTH tokens. `mcp_token` used to be wiped locally and left LIVE server-side,
    so a signed-out machine kept working read access through the copy Codex
    holds in its own config -- see the dedicated test below.
    """
    save_context({"base_url": "https://api.test", "token": "probe_pat_OLD", "mcp_token": "r"})

    lines = setup.sign_out(("claude_code",))

    assert api.revoked == [("https://api.test", "probe_pat_OLD"), ("https://api.test", "r")]
    assert load_context() == {}
    assert any("Signed out" in line for line in lines)
    assert any("plugins are still installed" in line for line in lines)


def test_sign_out_does_not_leave_a_live_read_token_in_codex(api, isolate, monkeypatch):
    """The gap this closes: `sign_out` released `token` and nothing else, so the
    read-only `mcp_token` stayed valid on the server while `clear_context` wiped
    the only local copy that could revoke it -- and Codex kept ITS copy in
    ~/.codex/config.toml. A machine someone had signed out of therefore still
    held working read access to the team's research.
    """
    from probe.cli import codex_config

    codex_home = isolate / "codex"
    codex_home.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    codex_config.write_mcp_bearer(
        "probe-research", url=codex_config.PRODUCTION_MCP_URL, token="probe_pat_READ"
    )
    save_context(
        {"base_url": "https://api.test", "token": "probe_pat_OLD", "mcp_token": "probe_pat_READ"}
    )

    lines = setup.sign_out(("claude_code",))

    assert ("https://api.test", "probe_pat_READ") in api.revoked, "the read token must be released"
    assert codex_config.configured_bearer("probe-research") is None, (
        "Codex must not keep a credential this device just signed out of"
    )
    assert any("Removed the Codex MCP entry" in line for line in lines)


def test_sign_out_leaves_every_other_saved_account_alone(api):
    """Signing out of staging must not sign you out of prod: that is why the
    config holds named contexts at all."""
    save_context({"base_url": "https://staging.test", "token": "probe_pat_STAGING"}, name="staging")
    save_context({"base_url": "https://api.test", "token": "probe_pat_PROD"}, name="prod")
    use_context("staging")

    setup.sign_out(("claude_code",))

    assert load_context("staging") == {}
    assert load_context("prod")["token"] == "probe_pat_PROD"


def test_sign_out_stops_capture_so_it_cannot_keep_uploading_to_the_old_account(api, monkeypatch):
    """The credential capture holds belongs to the account being left. Clearing
    the CLI's token and leaving the uploader running would keep shipping this
    device's sessions there -- signed out everywhere except where it counts."""
    save_context({"base_url": "https://api.test", "token": "probe_pat_OLD"})
    monkeypatch.setattr(setup, "capture_token_sources", lambda source: (TokenSource.PAIRED_FILE,))
    stopped: list[str] = []
    monkeypatch.setattr(
        setup,
        "turn_off",
        lambda mode: (
            stopped.append(os.environ["PROBE_AGENT"])
            or SimpleNamespace(summary=lambda: "Session capture is off.", warnings=[])
        ),
    )

    lines = setup.sign_out(("claude_code", "codex"))

    # One teardown per agent, each scoped to that agent's own state directory.
    assert stopped == ["claude_code", "codex"]
    assert any("Claude Code: Session capture is off." in line for line in lines)
    assert any("Codex: Session capture is off." in line for line in lines)


def test_sign_out_names_an_env_credential_it_cannot_unset(api, monkeypatch):
    """An exported PROBE_TOKEN outranks the file we just cleared. Reporting
    "signed out" without saying so is the same lie about the API that capture.py
    exists to prevent about transcripts."""
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_FROM_SHELL")
    save_context({"base_url": "https://api.test", "token": "probe_pat_OLD"})

    lines = setup.sign_out(("claude_code",))

    warning = " ".join(line for line in lines if line.startswith("!"))
    assert "PROBE_TOKEN" in warning and "outranks" in warning
    assert any("unset PROBE_TOKEN" in line for line in lines)


def test_sign_out_never_revokes_a_token_it_did_not_store(api, monkeypatch):
    """A token exported into the shell belongs to whoever exported it -- CI, a
    colleague's profile. Revoking it because it happened to resolve here would
    break something the wizard was never given."""
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_FROM_SHELL")

    setup.sign_out(("claude_code",))

    assert api.revoked == []


def test_sign_out_still_clears_the_disk_when_the_revoke_fails(api):
    """Being unable to reach the API must not leave the credentials sitting on
    the machine -- offline is a message, not a reason to keep them.

    The message says "release", not "revoke", and the difference is real: the
    server now unbinds the credential from THIS machine and revokes it only when
    no other device still holds it. Saying "revoke" would tell the user they had
    disconnected a laptop that is still working."""
    api.fails = True
    save_context({"base_url": "https://api.test", "token": "probe_pat_OLD"})

    lines = setup.sign_out(("claude_code",))

    assert load_context() == {}
    assert any(line.startswith("! could not release") for line in lines)
    assert any("Connected clients" in line for line in lines)


# --- signing in -------------------------------------------------------------


def _authorize_stub(monkeypatch, *, token="probe_pat_NEW", messages=(), granted=None):
    calls: list[dict] = []

    def fake(grants, *, base_url, capture_sources=None, on_prompt=None, open_browser=True):
        calls.append({"grants": grants, "base_url": base_url, "capture_sources": capture_sources})
        minted = (
            granted if granted is not None else {"api": {"token": token}, "mcp": {"token": "r"}}
        )
        return minted, list(messages)

    monkeypatch.setattr(setup, "authorize", fake)
    return calls


def test_sign_in_works_on_a_machine_that_is_already_signed_in(api, monkeypatch):
    """The point of the whole screen. `needs_authorization` skips the browser for
    a device that already holds a credential, so before this there was no way
    inside the wizard to correct an install made under the wrong account."""
    save_context({"base_url": "https://api.test", "token": "probe_pat_OLD"})
    calls = _authorize_stub(monkeypatch)
    monkeypatch.setattr(setup, "capture_token_sources", lambda source: ())

    result = setup.sign_in(base_url="https://api.test", sources=("claude_code",))

    assert result.ok is True
    assert calls[0]["grants"] == ["api", "mcp"]
    assert any("Signed in as new@prbe.ai" in line for line in result.lines)


def test_sign_in_revokes_the_credential_it_replaced(api, monkeypatch):
    """After the mint, never before: revoking first would leave a refused
    approval with no credentials at all."""
    save_context({"base_url": "https://api.test", "token": "probe_pat_OLD"})
    _authorize_stub(monkeypatch, token="probe_pat_NEW")
    monkeypatch.setattr(setup, "capture_token_sources", lambda source: ())

    result = setup.sign_in(base_url="https://api.test", sources=("claude_code",))

    assert api.revoked == [("https://api.test", "probe_pat_OLD")]
    assert any("Revoked the token this device was using before" in line for line in result.lines)


def test_sign_in_on_a_fresh_machine_revokes_nothing(api, monkeypatch):
    _authorize_stub(monkeypatch)
    monkeypatch.setattr(setup, "capture_token_sources", lambda source: ())

    setup.sign_in(base_url="https://api.test", sources=("claude_code",))

    assert api.revoked == []


def test_sign_in_re_pairs_capture_this_device_stores(api, monkeypatch):
    """Otherwise the CLI writes to the new account while every transcript keeps
    going to the old one, under a token the new account cannot even see."""
    calls = _authorize_stub(
        monkeypatch,
        granted={"api": {"token": "n"}, "mcp": {"token": "r"}, "capture": {"token": "ing"}},
    )
    monkeypatch.setattr(
        setup,
        "capture_token_sources",
        lambda source: (TokenSource.PAIRED_FILE,) if source == "claude_code" else (),
    )
    cleared: list[str] = []
    monkeypatch.setattr(
        setup, "clear_killswitch", lambda: cleared.append(os.environ["PROBE_AGENT"])
    )

    result = setup.sign_in(base_url="https://api.test", sources=("claude_code", "codex"))

    assert calls[0]["grants"] == ["api", "mcp", "capture"]
    # Only the agent that actually captures here, and only from a credential we
    # can replace.
    assert calls[0]["capture_sources"] == ["claude_code"]
    # A device switched off by `turn_off` carries a killswitch the new
    # credential cannot see past: pairing without clearing it would report
    # capture re-paired while it sends nothing.
    assert cleared == ["claude_code"]
    assert result.ok is True


def test_sign_in_does_not_re_pair_capture_that_lives_in_the_environment(api, monkeypatch):
    """The wizard cannot unset a variable in the parent shell, so a token minted
    for that agent would be shadowed the moment it landed -- capture would keep
    uploading to the old account while the run reported it re-paired."""
    calls = _authorize_stub(monkeypatch)
    monkeypatch.setattr(setup, "capture_token_sources", lambda source: (TokenSource.ENVIRONMENT,))

    setup.sign_in(base_url="https://api.test", sources=("claude_code",))

    assert calls[0]["grants"] == ["api", "mcp"]
    assert calls[0]["capture_sources"] is None


def test_a_refused_approval_reports_failure_and_touches_nothing(api, monkeypatch):
    save_context({"base_url": "https://api.test", "token": "probe_pat_OLD"})
    _authorize_stub(monkeypatch, granted={}, messages=["browser approval failed: denied"])
    monkeypatch.setattr(setup, "capture_token_sources", lambda source: ())

    result = setup.sign_in(base_url="https://api.test", sources=("claude_code",))

    assert result.ok is False
    assert api.revoked == [], "a failed sign-in must not strand this device with nothing"
    assert load_context()["token"] == "probe_pat_OLD"
    assert any("did not complete" in line for line in result.lines)


@pytest.fixture
def prepared_device(api, monkeypatch, tmp_path):
    """Exercise credential persistence while replacing only the browser transport."""
    from probe.sdk import device

    monkeypatch.setenv("PRBE_CODEX_TAP_PLUGIN_DIR", str(tmp_path / "codex-tap"))
    monkeypatch.setenv("PROBE_PI_TAP_PLUGIN_DIR", str(tmp_path / "pi-tap"))
    monkeypatch.delenv("PRBE_CODEX_TAP_TOKEN", raising=False)
    monkeypatch.delenv("PROBE_PI_TAP_TOKEN", raising=False)
    monkeypatch.setattr(setup, "sync_codex_mcp_token", lambda: [])
    calls = []

    def mint(base_url, **kwargs):
        calls.append(kwargs)
        sources = kwargs.get("capture_sources") or [kwargs.get("capture_source", "claude_code")]
        grants = [
            {"grant": grant, "token": f"new-{grant}"}
            for grant in kwargs["grants"]
            if grant != "capture"
        ]
        if "capture" in kwargs["grants"]:
            grants.extend(
                {"grant": "capture", "capture_source": source, "token": f"new-{source}"}
                for source in sources
            )
        return {"grants": grants}

    monkeypatch.setattr(device, "device_authorize", mint)
    return calls


def test_prepare_install_grants_all_agents_once_before_enabling_capture(prepared_device, monkeypatch):
    from probe.sdk import config

    sources = ("claude_code", "codex", "pi")
    real_save = config.save_context

    def save_after_disabling(updates):
        assert all((setup.tap_plugin_dir(source) / ".disabled").exists() for source in sources)
        real_save(updates)

    monkeypatch.setattr(config, "save_context", save_after_disabling)
    result = setup.sign_in(base_url="https://api.test", sources=sources, prepare_install=True)

    assert result.ok
    assert len(prepared_device) == 1
    assert prepared_device[0]["grants"] == ["api", "mcp", "capture"]
    assert prepared_device[0]["capture_sources"] == list(sources)
    assert load_context()["ingest_token"] == "new-claude_code"
    for source in sources:
        directory = setup.tap_plugin_dir(source)
        assert (directory / ".disabled").exists()
        if source != "claude_code":
            assert (directory / ".token").read_text() == f"new-{source}"

    # The existing install apply path activates saved capture without minting
    # anything else, even when an old copy of the plugin is already present.
    with setup.agent_target("claude_code"):
        setup.apply_capture(
            _caps(capture_plugin_installed=True), True, mode=setup.OffMode.DISABLE
        )
    assert not (setup.tap_plugin_dir("claude_code") / ".disabled").exists()
    assert (setup.tap_plugin_dir("codex") / ".disabled").exists()
    assert len(prepared_device) == 1


def test_a_claude_sign_in_leaves_pis_capture_folder_alone(prepared_device):
    """D3: pi never reads Claude Code's capture token, so a Claude Code sign-in
    has no reason to write a consent marker into pi's folder -- that marker,
    never removed, is what silently kept pi capture (and the daemon) off."""
    result = setup.sign_in(
        base_url="https://api.test", sources=("claude_code",), prepare_install=True
    )

    assert result.ok
    assert prepared_device[0]["capture_source"] == "claude_code"
    assert not (setup.tap_plugin_dir("pi") / ".disabled").exists()
    assert not (setup.tap_plugin_dir("pi") / ".token").exists()
    assert not (setup.tap_plugin_dir("codex") / ".disabled").exists()


def test_preparing_pi_replaces_the_shared_claude_fallback_but_keeps_it_disabled(prepared_device):
    save_context({"base_url": "https://api.test", "ingest_token": "old-claude-capture"})

    result = setup.sign_in(base_url="https://api.test", sources=("pi",), prepare_install=True)

    assert result.ok
    assert prepared_device[0]["capture_source"] == "pi"
    assert (setup.tap_plugin_dir("pi") / ".token").read_text() == "new-pi"
    assert (setup.tap_plugin_dir("pi") / ".disabled").exists()


@pytest.mark.parametrize("disabled", [False, True])
def test_prepare_install_preserves_existing_capture_state(prepared_device, disabled):
    save_context({"base_url": "https://api.test", "ingest_token": "old-capture"})
    marker = setup.tap_plugin_dir("claude_code") / ".disabled"
    if disabled:
        marker.write_text("Disabled by the researcher.\n")

    result = setup.sign_in(
        base_url="https://api.test", sources=("claude_code",), prepare_install=True
    )

    assert result.ok
    assert load_context()["ingest_token"] == "new-claude_code"
    assert marker.exists() is disabled
    if disabled:
        assert marker.read_text() == "Disabled by the researcher.\n"


def test_preparing_install_preserves_environment_only_capture(prepared_device, monkeypatch):
    monkeypatch.setenv("PROBE_INGEST_TOKEN", "environment-capture")

    result = setup.sign_in(
        base_url="https://api.test", sources=("claude_code",), prepare_install=True
    )

    assert result.ok
    assert prepared_device[0]["grants"] == ["api", "mcp"]
    assert "ingest_token" not in load_context()
    assert os.environ["PROBE_INGEST_TOKEN"] == "environment-capture"
    assert not (setup.tap_plugin_dir("claude_code") / ".disabled").exists()


def test_declined_preparation_does_not_write_capture_markers(prepared_device, monkeypatch):
    from probe.sdk import device

    save_context({"token": "existing-api"})

    def refuse(*args, **kwargs):
        assert not (setup.tap_plugin_dir("claude_code") / ".disabled").exists()
        raise device.DeviceLoginError("denied")

    monkeypatch.setattr(device, "device_authorize", refuse)
    result = setup.sign_in(
        base_url="https://api.test", sources=("claude_code",), prepare_install=True
    )

    assert not result.ok
    assert load_context()["token"] == "existing-api"
    assert not (setup.tap_plugin_dir("claude_code") / ".disabled").exists()
    assert not (setup.tap_plugin_dir("pi") / ".disabled").exists()


def test_capture_marker_failure_does_not_persist_new_credentials(prepared_device, monkeypatch):
    original_write = Path.write_text

    def reject_marker(path, *args, **kwargs):
        if path.name == ".disabled":
            raise OSError("read-only capture directory")
        return original_write(path, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", reject_marker)
    result = setup.sign_in(
        base_url="https://api.test", sources=("claude_code",), prepare_install=True
    )

    assert not result.ok
    assert "token" not in load_context()
    assert "ingest_token" not in load_context()
    assert any("could not save the minted credentials" in line for line in result.lines)


# --- switching between accounts already saved here --------------------------


def test_switching_is_local_and_mints_nothing(api, monkeypatch):
    save_context({"base_url": "https://api.test", "token": "probe_pat_PROD"}, name="prod")
    save_context({"base_url": "https://staging.test", "token": "probe_pat_STAGING"}, name="staging")
    use_context("prod")
    monkeypatch.setattr(setup, "capture_token_sources", lambda source: ())

    lines = setup.switch_account("staging", ("claude_code",))

    assert load_file()["current_context"] == "staging"
    assert load_context("staging")["token"] == "probe_pat_STAGING"
    assert api.revoked == []
    assert any("staging" in line and "https://staging.test" in line for line in lines)


def test_switching_to_an_account_with_no_credential_says_so(api, monkeypatch):
    save_context({"base_url": "https://api.test", "token": "t"})
    save_context({"base_url": "https://staging.test"}, name="staging")
    monkeypatch.setattr(setup, "capture_token_sources", lambda source: ())

    lines = setup.switch_account("staging", ("claude_code",))

    assert any("probe wizard --action login --context staging" in line and "no credential" in line
               for line in lines)


def test_switching_warns_that_a_paired_capture_token_does_not_follow(api, monkeypatch):
    """`ingest_token` lives inside the context, so it moves. A PAIRED device
    token does not -- it is one file per agent, minted by whoever approved it,
    and it keeps uploading there."""
    save_context({"base_url": "https://staging.test", "token": "t"}, name="staging")
    monkeypatch.setattr(setup, "capture_token_sources", lambda source: (TokenSource.PAIRED_FILE,))

    lines = setup.switch_account("staging", ("claude_code",))

    warning = " ".join(line for line in lines if line.startswith("!"))
    assert "Claude Code" in warning and "re-pair" in warning


# --- how the wizard reaches all of it ---------------------------------------


def _run(action, monkeypatch, *, caps=None, yes=False, sources=("claude_code",), interactive=False):
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setattr(setup, "interactive", lambda: interactive)
    return cli_main._run_wizard_action(
        action,
        caps=caps or _caps(),
        base_now="https://api.test",
        yes=yes,
        tracking=None,
        capture=None,
        auto_update=None,
        agent_rules=None,
        uninstall=False,
        configured=True,
        selected_agents=sources,
    )


def test_the_headless_account_screen_reports_and_changes_nothing(monkeypatch):
    """A screen nobody can answer must not answer for them: minting or clearing
    a credential unasked is the one thing this action may never do."""
    save_context({"base_url": "https://api.test", "token": "probe_pat_KEEP"})
    monkeypatch.setattr(setup, "sign_in", lambda *a, **k: pytest.fail("must not sign in"))
    monkeypatch.setattr(setup, "sign_out", lambda *a, **k: pytest.fail("must not sign out"))

    lines = _run(Action.ACCOUNT, monkeypatch, caps=_caps(logged_in_as="old@prbe.ai"))

    assert load_context()["token"] == "probe_pat_KEEP"
    assert any("old@prbe.ai" in line for line in lines)
    assert any("--action login" in line and "--action logout" in line for line in lines)


def test_the_screen_runs_the_row_that_was_picked(monkeypatch, capsys):
    """The wiring nothing else covers: a questionary answer has to reach the
    function that acts on it."""
    monkeypatch.setattr(
        setup, "run_account_menu", lambda caps, saved=None: setup.AccountAction.SIGN_OUT
    )
    monkeypatch.setattr(setup, "sign_out", lambda sources: ["signed out"])
    monkeypatch.setattr(setup, "confirm_sign_out", lambda account=None: True)  # the page's yes

    import typer

    with pytest.raises(typer.Exit) as caught:
        _run(Action.ACCOUNT, monkeypatch, interactive=True)
    assert caught.value.exit_code == 0
    assert "signed out" in capsys.readouterr().out


def test_picking_switch_opens_the_account_list(monkeypatch):
    monkeypatch.setattr(
        setup, "run_account_menu", lambda caps, saved=None: setup.AccountAction.SWITCH
    )
    monkeypatch.setattr(setup, "run_switch_menu", lambda saved: "staging")
    picked: list = []
    monkeypatch.setattr(
        setup, "switch_account", lambda name, sources: picked.append((name, sources)) or ["ok"]
    )

    assert _run(Action.ACCOUNT, monkeypatch, interactive=True) == ["ok"]
    assert picked == [("staging", ("claude_code",))]


def test_backing_out_of_the_screen_changes_nothing(monkeypatch):
    save_context({"base_url": "https://api.test", "token": "probe_pat_KEEP"})
    monkeypatch.setattr(
        setup, "run_account_menu", lambda caps, saved=None: setup.AccountAction.BACK
    )
    monkeypatch.setattr(setup, "sign_out", lambda sources: pytest.fail("BACK is not an action"))

    # None, not []: "nothing happened" is what lets the wizard loop skip the
    # result page, the press-enter pause, and the per-agent state re-read.
    assert _run(Action.ACCOUNT, monkeypatch, interactive=True) is None
    assert load_context()["token"] == "probe_pat_KEEP"


def test_action_logout_signs_out_of_every_selected_agent(monkeypatch, capsys):
    seen: list[tuple] = []
    monkeypatch.setattr(setup, "sign_out", lambda sources: seen.append(sources) or ["done"])

    import typer

    with pytest.raises(typer.Exit) as caught:
        _run(Action.SIGN_OUT, monkeypatch, sources=("claude_code", "codex"))

    assert seen == [("claude_code", "codex")], "capture is per agent, so both are torn down"
    assert caught.value.exit_code == 0
    assert "done" in capsys.readouterr().out


def test_action_login_signs_in_once_for_the_device(monkeypatch):
    """One config file, not one per coding agent: two approvals for one machine
    would mint two tokens and leave the second overwriting the first."""
    seen: list[dict] = []

    def fake_sign_in(*, base_url, sources, on_prompt=None, open_browser=True):
        seen.append({"base_url": base_url, "sources": sources})
        return setup.SignInResult(ok=True, lines=["Signed in as new@prbe.ai"])

    monkeypatch.setattr(setup, "sign_in", fake_sign_in)

    lines = _run(Action.SIGN_IN, monkeypatch, sources=("claude_code", "codex"))

    assert seen == [{"base_url": "https://api.test", "sources": ("claude_code", "codex")}]
    assert lines == ["Signed in as new@prbe.ai"]


@pytest.mark.parametrize("interactive", [False, True])
def test_action_login_redraws_approval_pages_but_keeps_piped_output_append_only(
    monkeypatch, capsys, interactive,
):
    from probe.cli import tui

    heading = "Approve this device in the browser to sign in."
    pages = []
    monkeypatch.setattr(tui, "interactive", lambda: interactive)
    monkeypatch.setattr(tui, "page", lambda lines: pages.append(list(lines)))

    def sign_in(*, on_prompt, **kwargs):
        if interactive:
            assert pages == [[heading, ""]]
        for code in ("first-code", "refreshed-code"):
            on_prompt(SimpleNamespace(
                verification_uri_complete=f"https://example.test/approve/{code}", user_code=code,
            ))
        return setup.SignInResult(ok=True, lines=["Signed in."])

    monkeypatch.setattr(setup, "sign_in", sign_in)
    assert _run(Action.SIGN_IN, monkeypatch, interactive=interactive) == ["Signed in."]
    output = capsys.readouterr().out
    if interactive:
        assert pages == [
            [heading, ""],
            [heading, "", "  visit: https://example.test/approve/first-code", "  code:  first-code"],
            [heading, "", "  visit: https://example.test/approve/refreshed-code", "  code:  refreshed-code"],
        ]
        assert output == ""
    else:
        assert pages == []
        assert output == (
            f"{heading}\n\n"
            "  visit: https://example.test/approve/first-code\n  code:  first-code\n"
            "  visit: https://example.test/approve/refreshed-code\n  code:  refreshed-code\n"
        )


def test_a_scripted_login_that_failed_exits_non_zero(monkeypatch):
    """A caller that cannot see the exit status cannot tell an approved device
    from a refused one, and would install plugins against a credential nobody
    minted. The MENU path deliberately does not exit -- retrying there is one
    keystroke."""
    import typer

    monkeypatch.setattr(
        setup,
        "sign_in",
        lambda **_kwargs: setup.SignInResult(ok=False, lines=["! Sign-in did not complete"]),
    )

    with pytest.raises(typer.Exit) as exit_info:
        _run(Action.SIGN_IN, monkeypatch)
    assert exit_info.value.exit_code == 1

    monkeypatch.setattr(
        setup, "run_account_menu", lambda caps, saved=None: setup.AccountAction.SIGN_IN
    )
    assert _run(Action.ACCOUNT, monkeypatch, interactive=True) == ["! Sign-in did not complete"]


def test_the_wizard_does_not_ask_which_agent_before_an_account_action(monkeypatch):
    """ "Which coding agents should Probe connect?" has no bearing on signing
    out, and the credential half of an account is device-wide anyway."""
    from typer.testing import CliRunner

    import probe.cli.main  # noqa: F401
    from probe.cli import bootstrap
    from probe.cli import doctor as doctor_impl

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(doctor_impl, "collect", lambda: _caps(logged_in_as="old@prbe.ai"))
    monkeypatch.setattr(
        setup, "run_agent_menu", lambda defaults, action=None: pytest.fail("no agent question here")
    )
    seen: list[tuple] = []
    monkeypatch.setattr(setup, "sign_out", lambda sources: seen.append(sources) or ["signed out"])

    result = CliRunner().invoke(cli_main.app, ["wizard", "--action", "logout"])

    assert result.exit_code == 0, result.output
    assert seen, "the logout action never ran"
    assert "signed out" in result.output


def test_doctor_names_the_active_saved_account():
    """ "not logged in" on a machine holding three accounts sends someone hunting
    for a lost credential when the answer is that a different one is active."""
    report = doctor.render(_caps(logged_in_as="me@prbe.ai", config_context="staging"))

    assert "Saved account" in report and "staging" in report


# --- uninstall signs out too ------------------------------------------------


def test_uninstall_releases_the_account_so_a_reinstall_asks_to_sign_in(api):
    """The gap this closes: Uninstall removed the plugins and left the ACCOUNT.

    Both tokens stayed live server-side, the config kept its copy, and the next
    `probe wizard` therefore skipped the browser entirely -- `needs_authorization`
    reads a stored token as "already signed in". Someone who removed Probe from
    a shared box was still signed into it.
    """
    save_context({"base_url": "https://api.test", "token": "probe_pat_OLD", "mcp_token": "r"})

    lines = setup.finish_removal()

    assert api.revoked == [("https://api.test", "probe_pat_OLD"), ("https://api.test", "r")]
    assert load_context() == {}, "a removed device must hold no credential"
    assert any("sign in" in line for line in lines)
    assert any("already sent" in line for line in lines)


def test_uninstall_leaves_every_other_saved_account_alone(api):
    """Same rule sign-out has: uninstalling on a staging login must not take the
    prod credentials with it."""
    save_context({"base_url": "https://staging.test", "token": "probe_pat_STAGING"}, name="staging")
    save_context({"base_url": "https://api.test", "token": "probe_pat_PROD"}, name="prod")
    use_context("staging")

    setup.finish_removal()

    assert load_context("staging") == {}
    assert load_context("prod")["token"] == "probe_pat_PROD"


def test_uninstall_still_clears_the_disk_when_the_revoke_fails(api):
    """An offline laptop must still come out of Uninstall signed out: the
    removal has already taken the plugins, and stopping half way there would
    leave a machine that reads as installed and cannot be reinstalled cleanly.
    """
    api.fails = True
    save_context({"base_url": "https://api.test", "token": "probe_pat_OLD"})

    lines = setup.finish_removal()

    assert load_context() == {}
    assert any(line.startswith("! could not release") for line in lines)


def test_sign_out_and_uninstall_release_the_same_credentials():
    """One implementation, so the two can never drift into clearing different
    things -- which is how `mcp_token` survived sign-out for as long as it did.
    """
    import inspect

    assert "release_credentials()" in inspect.getsource(setup.sign_out)
    assert "release_credentials()" in inspect.getsource(setup.finish_removal)


def test_only_sign_out_promises_the_plugins_are_still_there(api):
    """The line that makes sign-out reversible is a lie after an uninstall."""
    save_context({"base_url": "https://api.test", "token": "probe_pat_OLD"})
    removal = setup.finish_removal()

    save_context({"base_url": "https://api.test", "token": "probe_pat_OLD"})
    signout = setup.sign_out(("claude_code",))

    assert any("plugins are still installed" in line for line in signout)
    assert not any("plugins are still installed" in line for line in removal)


def test_removing_probe_no_longer_claims_the_account_survives(monkeypatch):
    """`remove_everything` used to close with "Your account ... are untouched --
    revoke this device's tokens in Settings". It is `finish_removal`'s job now,
    and the old sentence would be describing the opposite of what happens."""
    from probe.cli import claude_cli

    monkeypatch.setattr(
        setup,
        "turn_off",
        # The real dataclass, not a SimpleNamespace: `remove_everything` reads
        # `plugin_removed`/`verified` off it to decide whether the killswitch
        # marker is still guarding anything, and a stub shaped like the caller's
        # wishes rather than the callee's signature is how the `ok, detail =
        # uninstall_plugin(...)` TypeError survived a passing suite.
        lambda mode: capture.TurnOffResult(
            killswitch_set=True, daemon_stopped=True, plugin_removed=True
        ),
    )
    monkeypatch.setattr(
        setup, "uninstall_plugin", lambda name: claude_cli.Result(ok=True, detail="removed")
    )

    messages = setup.remove_everything(_caps())

    assert "Removed." in messages
    assert not any("untouched" in message for message in messages)
    assert not any("Settings" in message for message in messages)


def test_a_removed_device_reads_as_fresh_again(monkeypatch, isolate):
    """`Capabilities.configured` decides whether the next install offers the
    fresh defaults or "whatever is currently on" -- and after a removal that is
    nothing at all, so a device stuck at configured=True reinstalls with every
    box unticked.

    Two leftovers used to keep it True forever: the `.disabled` killswitch the
    teardown writes, and the `last_attempt` record `save(enabled=False)` keeps.
    """
    from probe.cli import autoupdate, claude_cli
    from probe.cli.capabilities import tap_plugin_dir

    autoupdate.record_attempt(
        autoupdate.Attempt(at=1, ok=True, detail="upgraded", from_version="1", to_version="2")
    )
    autoupdate.save(enabled=True)
    monkeypatch.setattr(
        setup,
        "turn_off",
        lambda mode: capture._set_killswitch()
        and capture.TurnOffResult(
            killswitch_set=True, daemon_stopped=True, plugin_removed=True
        ),
    )
    monkeypatch.setattr(
        setup, "uninstall_plugin", lambda name: claude_cli.Result(ok=True, detail="removed")
    )

    setup.remove_everything(_caps())

    assert not (tap_plugin_dir() / ".disabled").exists(), (
        "the killswitch guards nothing once the plugin and every credential are gone"
    )
    assert autoupdate.load() == autoupdate.Settings(enabled=False), (
        "the auto-update record is this device's Probe bookkeeping; Probe is gone"
    )
    assert not Capabilities(capture_killswitched=False).configured


def test_the_killswitch_survives_a_removal_that_did_not_verify(monkeypatch, isolate):
    """The one thing this file may never do quietly is turn capture back on.

    An exported PROBE_INGEST_TOKEN, or a plugin the uninstall could not remove,
    leaves something that could still upload -- and clearing `.disabled` there
    would hand it back the session it was stopped from starting.
    """
    from probe.cli import claude_cli
    from probe.cli.capabilities import TokenSource, tap_plugin_dir

    monkeypatch.setattr(
        setup,
        "turn_off",
        lambda mode: capture._set_killswitch()
        and capture.TurnOffResult(
            killswitch_set=True,
            daemon_stopped=True,
            plugin_removed=False,
            remaining=[TokenSource.ENVIRONMENT],
        ),
    )
    monkeypatch.setattr(
        setup, "uninstall_plugin", lambda name: claude_cli.Result(ok=True, detail="removed")
    )

    setup.remove_everything(_caps())

    assert (tap_plugin_dir() / ".disabled").exists()


# ---------------------------------------------------------------------------
# Sign out asks first, and is drawn red (Richard 2026-09-29).
# ---------------------------------------------------------------------------


def _sign_out(monkeypatch, answer):
    import importlib

    import typer

    cli_main = importlib.import_module("probe.cli.main")
    from probe.cli import tui

    signed_out: list = []
    monkeypatch.setattr(setup, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(setup, "confirm_sign_out", lambda account=None: answer)
    monkeypatch.setattr(setup, "sign_out", lambda sources: signed_out.append(sources) or ["Signed out."])
    try:
        result = cli_main._run_account_action(
            Action.SIGN_OUT, caps=_caps(logged_in_as="a@b.c"), base_now="https://api.test", yes=False,
            sources=("claude_code",),
        )
    except typer.Exit:
        result = "exited"
    return result, signed_out


@pytest.mark.parametrize("answer", [False, None, "back"])
def test_sign_out_stays_signed_in_unless_the_page_says_yes(monkeypatch, answer):
    result, signed_out = _sign_out(monkeypatch, answer)
    assert result is None and signed_out == [], "back to the menu, nothing changed"


def test_sign_out_signs_out_on_yes(monkeypatch):
    result, signed_out = _sign_out(monkeypatch, True)
    assert result == "exited" and signed_out == [("claude_code",)]


def test_the_sign_out_row_is_red_and_the_page_names_the_account():
    from probe.cli import tui
    from probe.cli.actions import DANGER_ACTIONS

    assert DANGER_ACTIONS == {Action.SIGN_OUT}
    rows = {getattr(c, "value", None): c for c in setup.action_choices()}
    assert getattr(rows[Action.SIGN_OUT], "probe_style", None) == tui.DANGER_STYLE
    assert getattr(rows[Action.EXIT], "probe_style", None) is None
    assert tui.plain_title([("class:danger", "Sign out\n  x")]) == "Sign out\n  x"


def test_every_heading_has_a_blank_line_under_it():
    import questionary

    choices = setup.action_choices()
    for index, choice in enumerate(choices):
        if isinstance(choice, questionary.Separator) and str(choice.title).strip():
            after = choices[index + 1]
            assert isinstance(after, questionary.Separator) and not str(after.title).strip(), choice.title
