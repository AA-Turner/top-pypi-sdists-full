"""Website authentication gates the wizard and keeps install intent separate."""

from __future__ import annotations

import importlib
import os
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner

from probe.cli import bootstrap, doctor, setup, tui
from probe.cli.actions import Action
from probe.cli.capabilities import Capabilities, TokenSource, capture_token_sources, tap_plugin_dir
from probe.sdk.config import load_context, resolve, save_context
from probe.sdk.device import DeviceLoginError, OnboardingRequired

main = importlib.import_module("probe.cli.main")
apply_wizard_action = main._run_wizard_action
collect_capabilities = doctor.collect
sign_in_to_account = setup.sign_in


@pytest.fixture
def entry(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config.json"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_RESEARCH_TAP_PLUGIN_DIR", str(tmp_path / "tap"))
    monkeypatch.setenv("PROBE_BASE_URL", "https://api.test")
    monkeypatch.delenv("PROBE_TOKEN", raising=False)
    monkeypatch.delenv("PROBE_MCP_TOKEN", raising=False)
    monkeypatch.delenv("PROBE_INGEST_TOKEN", raising=False)
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(main, "_version_notice", lambda: None)
    monkeypatch.setattr(main, "_outbox_notice", lambda: None)
    monkeypatch.setattr(setup, "detectable_sources", lambda: ("claude_code",))
    monkeypatch.setattr(doctor, "collect", lambda: Capabilities(claude_available=True))
    monkeypatch.setattr(setup, "interactive", lambda: True)
    monkeypatch.setattr(
        "probe.cli.capabilities.verify_mcp_credential", lambda **_kwargs: True
    )
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "page", lambda *a, **kw: None)
    events = []

    def sign_in(**kwargs):
        events.append(("signin", kwargs))
        save_context({"token": "probe_pat_menu_test"})
        return setup.SignInResult(ok=True, lines=["Signed in."])

    monkeypatch.setattr(setup, "sign_in", sign_in)
    monkeypatch.setattr(
        setup, "run_action_menu", lambda _caps: events.append(("menu", {})) or Action.EXIT
    )
    monkeypatch.setattr(
        setup, "run_confirm_install", lambda *a, **kw: events.append(("confirm", {})) or True
    )
    monkeypatch.setattr(setup, "run_backfill_offer", lambda *_a, **_kw: set())
    monkeypatch.setattr(
        main, "_run_wizard_action", lambda *a, **kw: events.append(("apply", kw)) or []
    )
    return events


def test_bare_launch_authenticates_before_the_main_menu(entry):
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    assert [event for event, _ in entry] == ["signin", "menu"]
    assert "install_code" not in entry[0][1]
    assert entry[0][1]["prepare_install"] is True


def test_signed_in_launch_returns_directly_to_the_main_menu(entry):
    save_context({"token": "probe_pat_existing", "base_url": "https://api.test"})
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    assert [event for event, _ in entry] == ["menu"]


def test_revoked_saved_token_starts_browser_sign_in_again(entry, monkeypatch):
    save_context({"token": "probe_pat_revoked", "base_url": "https://api.test"})
    validity = iter([False, True])
    monkeypatch.setattr(
        doctor, "collect", lambda: Capabilities(api_credential_valid=next(validity))
    )
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    assert [event for event, _ in entry] == ["signin", "menu"]


def test_code_without_install_authenticates_then_opens_the_main_menu(entry):
    save_context({"token": "probe_pat_existing", "base_url": "https://api.test"})
    result = CliRunner().invoke(main.app, ["wizard", "ABCD234567"])
    assert result.exit_code == 0, result.output
    assert [event for event, _ in entry] == ["signin", "menu"]
    assert entry[0][1]["install_code"] == "ABCD234567"
    assert "ABCD234567" not in result.output


def test_install_code_keeps_the_confirmed_grants_and_skips_the_main_menu(entry):
    result = CliRunner().invoke(main.app, ["install", "ABCD234567"])
    assert result.exit_code == 0, result.output
    assert [event for event, _ in entry] == ["confirm", "apply"]
    applied = entry[-1][1]
    assert applied["install_code"] == "ABCD234567"
    assert applied["authorization_needs"] == ["api", "mcp", "capture"]
    assert applied["capture_sources"] == ["claude_code"]


def test_install_without_code_keeps_browser_authorization_after_confirmation(entry):
    result = CliRunner().invoke(main.app, ["install"])
    assert result.exit_code == 0, result.output
    assert [event for event, _ in entry] == ["confirm", "apply"]
    assert entry[-1][1]["install_code"] is None
    assert entry[-1][1]["authorization_needs"] == ["api", "mcp", "capture"]


def test_explicit_install_code_replaces_an_existing_authorized_account(entry, monkeypatch):
    save_context({"token": "probe_pat_existing", "mcp_token": "probe_pat_read"})
    monkeypatch.setattr(
        doctor, "collect", lambda: Capabilities(capture_token_sources=(TokenSource.PAIRED_FILE,))
    )
    monkeypatch.setattr(
        "probe.cli.capabilities.verify_mcp_credential",
        lambda **kwargs: pytest.fail("an explicit code selects the account; do not probe the old one"),
    )
    result = CliRunner().invoke(main.app, ["install", "ABCD234567"])
    assert result.exit_code == 0, result.output
    assert entry[-1][1]["install_code"] == "ABCD234567"
    assert entry[-1][1]["authorization_needs"] == ["api", "mcp", "capture"]


# -- an install code on a device that is already signed in -------------------
#
# The code carries its own identity, and redeeming it detaches the credentials
# bound to this device server-side. So the only account the CLI can name is the
# one being REPLACED, and the only moment it can name it is before the exchange.


def _signed_in_as(email: str | None):
    """A collect() that reports one verified account (or an unnameable one)."""
    return lambda: Capabilities(claude_available=True, logged_in_as=email)


@pytest.fixture
def switch_prompt(monkeypatch):
    """Record every account-switch confirmation and answer it with `answers`."""
    asked: list[str] = []
    answers = {"reply": True}

    def confirm(previous):
        asked.append(previous)
        return answers["reply"]

    monkeypatch.setattr(setup, "run_confirm_account_switch", confirm)
    return SimpleNamespace(asked=asked, answers=answers)


@pytest.mark.parametrize("argv", [["install", "ABCD234567"], ["wizard", "ABCD234567"]])
def test_install_code_asks_before_replacing_a_named_account(entry, monkeypatch, switch_prompt, argv):
    save_context({"token": "probe_pat_existing", "base_url": "https://api.test"})
    monkeypatch.setattr(doctor, "collect", _signed_in_as("old@example.test"))
    result = CliRunner().invoke(main.app, argv)
    assert result.exit_code == 0, result.output
    # Named, and named BEFORE anything redeemed the code.
    assert switch_prompt.asked == ["old@example.test"]
    assert [event for event, _ in entry][0] in {"signin", "confirm"}


@pytest.mark.parametrize("argv", [["install", "ABCD234567"], ["wizard", "ABCD234567"]])
def test_declining_the_account_switch_redeems_nothing(entry, monkeypatch, switch_prompt, argv):
    save_context({"token": "probe_pat_existing", "base_url": "https://api.test"})
    monkeypatch.setattr(doctor, "collect", _signed_in_as("old@example.test"))
    switch_prompt.answers["reply"] = False
    result = CliRunner().invoke(main.app, argv)
    assert result.exit_code == 0, result.output
    assert entry == [], "declining must not sign in, confirm an install, or apply anything"
    assert load_context()["token"] == "probe_pat_existing"
    assert "old@example.test" in result.output


def test_install_code_does_not_ask_when_the_account_cannot_be_named(entry, switch_prompt):
    # A saved token that no `me()` confirmed: offline, or already revoked. There
    # is no account to name, and redeeming a code there is a repair.
    save_context({"token": "probe_pat_unverified", "base_url": "https://api.test"})
    result = CliRunner().invoke(main.app, ["install", "ABCD234567"])
    assert result.exit_code == 0, result.output
    assert switch_prompt.asked == []
    assert [event for event, _ in entry] == ["confirm", "apply"]


def test_install_code_does_not_ask_on_a_fresh_device(entry, switch_prompt):
    result = CliRunner().invoke(main.app, ["install", "ABCD234567"])
    assert result.exit_code == 0, result.output
    assert switch_prompt.asked == []


def test_yes_switches_accounts_without_asking(entry, monkeypatch, switch_prompt):
    save_context({"token": "probe_pat_existing", "base_url": "https://api.test"})
    monkeypatch.setattr(doctor, "collect", _signed_in_as("old@example.test"))
    result = CliRunner().invoke(main.app, ["install", "--yes", "ABCD234567"])
    assert result.exit_code == 0, result.output
    assert switch_prompt.asked == []
    assert [event for event, _ in entry] == ["apply"]


def test_headless_install_code_refuses_to_switch_accounts(entry, monkeypatch, switch_prompt):
    save_context({"token": "probe_pat_existing", "base_url": "https://api.test"})
    monkeypatch.setattr(doctor, "collect", _signed_in_as("old@example.test"))
    monkeypatch.setattr(setup, "interactive", lambda: False)
    result = CliRunner().invoke(main.app, ["install", "ABCD234567"])
    assert result.exit_code == 1, result.output
    assert entry == [], "a switch nobody can be shown is a switch nobody consented to"
    assert load_context()["token"] == "probe_pat_existing"
    assert "old@example.test" in result.output
    assert "--yes" in result.output


def test_guided_install_reports_the_account_the_code_selected(entry, monkeypatch):
    # The gate above can only name the account being replaced; this is the one
    # point at which the account the code SELECTED can be stated at all.
    notes: list[str] = []

    class Recording(tui.Progress):
        def note(self, *lines):
            notes.extend(lines)

    monkeypatch.setattr(tui, "Progress", Recording)
    monkeypatch.setattr(
        setup,
        "authorize",
        lambda *a, **kw: ({"api": {"token": "new-api"}, "mcp": {"token": "new-mcp"}}, []),
    )
    monkeypatch.setattr(setup, "account_email", lambda _base: "new@example.test")
    for name in ("apply_tracking", "apply_auto_update", "apply_agent_rules", "refresh_marketplace"):
        monkeypatch.setattr(setup, name, lambda *a, **kw: [])
    monkeypatch.setattr(
        doctor,
        "collect",
        lambda: Capabilities(
            claude_available=True,
            logged_in_as="new@example.test",
            tracking_plugin_installed=True,
            plugins_verified=True,
        ),
    )
    apply_wizard_action(
        Action.CONFIGURE,
        caps=Capabilities(claude_available=True),
        base_now="https://api.test",
        yes=True,
        tracking=True,
        capture=False,
        auto_update=False,
        agent_rules=False,
        uninstall=False,
        configured=False,
        authorization_needs=["api", "mcp"],
        install_code="ABCD234567",
    )
    assert "Signed in as new@example.test." in notes


@pytest.mark.parametrize("agents", [("claude_code",), ("claude_code", "codex")])
@pytest.mark.parametrize("disabled", [False, True])
def test_guided_install_reuses_saved_grants_even_when_capture_is_disabled(
    entry, monkeypatch, agents, disabled
):
    save_context({"token": "probe_pat_existing", "mcp_token": "probe_pat_read"})
    monkeypatch.setattr(setup, "detectable_sources", lambda: agents)
    monkeypatch.setattr(
        doctor,
        "collect",
        lambda: Capabilities(
            agent_source=os.environ.get("PROBE_AGENT", "claude_code"),
            capture_token_sources=(TokenSource.PAIRED_FILE,),
            capture_killswitched=disabled,
            # An offline email lookup does not invalidate the saved login.
            logged_in_as=None,
            api_credential_valid=None,
        ),
    )
    result = CliRunner().invoke(
        main.app, ["install", "--agent", "both" if len(agents) == 2 else "claude"]
    )
    assert result.exit_code == 0, result.output
    applied = [kwargs for event, kwargs in entry if event == "apply"]
    assert len(applied) == len(agents)
    assert all(kwargs["authorization_needs"] == [] for kwargs in applied)
    assert all(kwargs["selection_override"].capture for kwargs in applied)
    assert not any(event == "signin" for event, _ in entry)


@pytest.mark.parametrize(
    "missing", ["api", "mcp", "capture", "revoked_api", "revoked_mcp", "revoked_capture"]
)
def test_guided_install_repairs_missing_or_rejected_grants(entry, monkeypatch, missing):
    save_context({
        "token": "probe_pat_existing" if missing != "api" else None,
        "mcp_token": "probe_pat_read" if missing != "mcp" else None,
    })
    monkeypatch.setattr(setup, "detectable_sources", lambda: ("claude_code", "codex"))
    monkeypatch.setattr(
        "probe.cli.capabilities.verify_mcp_credential", lambda **_kwargs: missing != "revoked_mcp"
    )

    def collect():
        source = os.environ.get("PROBE_AGENT", "claude_code")
        return Capabilities(
            agent_source=source,
            logged_in_as="researcher@example.com",
            api_credential_valid=missing != "revoked_api",
            capture_token_sources=(
                () if missing == "capture" and source == "codex" else (TokenSource.PAIRED_FILE,)
            ),
            capture_credential_valid=not (missing == "revoked_capture" and source == "codex"),
        )

    monkeypatch.setattr(doctor, "collect", collect)
    result = CliRunner().invoke(main.app, ["install", "--agent", "both"])
    assert result.exit_code == 0, result.output
    applied = [kwargs for event, kwargs in entry if event == "apply"]
    assert applied[0]["authorization_needs"] == ["api", "mcp", "capture"]
    assert applied[0]["capture_sources"] == ["claude_code", "codex"]
    assert applied[1]["authorization_needs"] == [], "the shared approval covers both agents"


def test_installing_pi_requires_its_own_capture_grant(entry, monkeypatch):
    save_context({"token": "probe_pat_existing", "mcp_token": "probe_pat_read"})
    monkeypatch.setattr(setup, "detectable_sources", lambda: ("pi",))
    monkeypatch.setattr(
        doctor,
        "collect",
        lambda: Capabilities(
            agent_source="pi",
            # D3: the CLI config's (Claude Code) token is never one of pi's
            # sources, so a machine signed in for Claude Code has none for pi.
            capture_token_sources=(),
        ),
    )
    result = CliRunner().invoke(main.app, ["install", "--agent", "pi"])
    assert result.exit_code == 0, result.output
    applied = [kwargs for event, kwargs in entry if event == "apply"]
    assert applied[0]["authorization_needs"] == ["api", "mcp", "capture"]
    assert applied[0]["capture_sources"] == ["pi"]


@pytest.mark.parametrize("code", [None, "ABCD234567"])
def test_fresh_wizard_signs_in_once_then_installs_with_the_saved_grants(entry, monkeypatch, code):
    from probe.sdk import device

    authorizations = []

    def mint(base_url, **kwargs):
        authorizations.append(kwargs)
        return {"grants": [
            {"grant": "api", "token": "probe_pat_full"},
            {"grant": "mcp", "token": "probe_pat_read"},
            {"grant": "capture", "token": "ros_ing_capture", "capture_source": "claude_code"},
        ]}

    monkeypatch.setattr(device, "device_authorize", mint)
    monkeypatch.setattr(setup, "sign_in", sign_in_to_account)
    monkeypatch.setattr(setup, "account_email", lambda _base: "researcher@example.com")
    monkeypatch.setattr(setup, "sync_codex_mcp_token", lambda: [])

    def collect():
        return Capabilities(
            claude_available=True,
            logged_in_as="researcher@example.com" if resolve().token else None,
            capture_token_sources=capture_token_sources("claude_code"),
            capture_killswitched=(tap_plugin_dir("claude_code") / ".disabled").exists(),
        )

    monkeypatch.setattr(doctor, "collect", collect)
    actions = iter([Action.CONFIGURE, Action.EXIT])
    monkeypatch.setattr(setup, "run_action_menu", lambda _caps: next(actions))

    def confirm(*args, **kwargs):
        assert resolve().ingest_token == "ros_ing_capture"
        assert not collect().capture_on, "signing in must not enable capture before installation"
        return True

    monkeypatch.setattr(setup, "run_confirm_install", confirm)
    result = CliRunner().invoke(main.app, ["wizard", *([code] if code else [])], input="\n")
    assert result.exit_code == 0, result.output
    assert len(authorizations) == 1
    assert authorizations[0]["grants"] == ["api", "mcp", "capture"]
    assert authorizations[0].get("install_code") == code
    applied = [kwargs for event, kwargs in entry if event == "apply"]
    assert len(applied) == 1
    assert applied[0]["authorization_needs"] == []
    assert applied[0]["install_code"] is None


@pytest.mark.parametrize("repair", ["disabled_capture", "codex_bearer", "legacy_capture"])
def test_install_applies_local_repairs_without_reauthorizing(entry, monkeypatch, repair):
    from probe.cli import claude_cli, onboarding_complete, plugin_cli

    save_context({"token": "probe_pat_existing", "mcp_token": "probe_pat_read"})
    source = "codex"
    tap = tap_plugin_dir(source)
    tap.mkdir(parents=True, exist_ok=True)
    (tap / ".token").write_text("ros_ing_capture")
    if repair == "disabled_capture":
        (tap / ".disabled").touch()
    pending = {repair}

    def collect():
        return Capabilities(
            agent_source=source,
            codex_available=True,
            logged_in_as="researcher@example.com",
            tracking_plugin_installed=True,
            capture_plugin_installed=True,
            legacy_capture_plugin_installed="legacy_capture" in pending,
            capture_token_sources=(TokenSource.PAIRED_FILE,),
            capture_killswitched=(tap / ".disabled").exists(),
            auto_update_enabled=True,
            agent_rules_installed=True,
            mcp_authenticated=True,
        )

    def sync():
        pending.discard("codex_bearer")
        return []

    def uninstall(*args):
        pending.discard("legacy_capture")
        return claude_cli.Result(ok=True, detail="removed")

    monkeypatch.setattr(setup, "detectable_sources", lambda: (source,))
    monkeypatch.setattr(doctor, "collect", collect)
    monkeypatch.setattr(main, "_run_wizard_action", apply_wizard_action)
    monkeypatch.setattr(main, "_register_local_capabilities", lambda *a, **kw: [])
    monkeypatch.setattr(setup, "codex_mcp_token_drifted", lambda: "codex_bearer" in pending)
    monkeypatch.setattr(setup, "sync_codex_mcp_token", sync)
    monkeypatch.setattr(plugin_cli, "uninstall", uninstall)
    monkeypatch.setattr(
        setup, "authorize", lambda *a, **kw: pytest.fail("the saved grants must be reused")
    )
    completed = []
    monkeypatch.setattr(
        onboarding_complete, "show", lambda base: completed.append(base) or True
    )
    result = CliRunner().invoke(main.app, ["install", "--agent", "codex"])
    assert result.exit_code == 0, result.output
    assert completed == ["https://api.test"]
    assert collect().capture_on
    assert not collect().legacy_capture_plugin_installed
    assert "codex_bearer" not in pending
    assert "browser approval" not in result.output


def test_new_browser_account_exits_before_the_menu_or_install(entry, monkeypatch):
    def incomplete(**kwargs):
        raise OnboardingRequired("Finish onboarding", onboarding_url="https://dash.test/onboarding")

    monkeypatch.setattr(setup, "sign_in", incomplete)
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    assert "Complete onboarding on https://dash.test/onboarding first." in result.output
    assert "Then run the install command shown there." in result.output
    assert entry == []


def test_failed_authentication_cannot_open_the_menu(entry, monkeypatch):
    monkeypatch.setattr(
        setup, "sign_in", lambda **kw: setup.SignInResult(ok=False, lines=["Code expired."])
    )
    result = CliRunner().invoke(main.app, ["wizard", "ABCD234567"])
    assert result.exit_code == 1, result.output
    assert "Code expired" in result.output
    assert entry == []


def test_invalid_code_is_rejected_without_bootstrapping(entry, monkeypatch):
    monkeypatch.setattr(
        bootstrap, "ensure_persistent_install", lambda **_: pytest.fail("no work before validation")
    )
    result = CliRunner().invoke(main.app, ["install", "too-short"])
    assert result.exit_code == 2, result.output
    assert "exactly 10" in result.output
    assert entry == []


def test_headless_install_code_still_authenticates_when_tooling_is_declined(entry, monkeypatch):
    monkeypatch.setattr(setup, "interactive", lambda: False)
    result = CliRunner().invoke(
        main.app,
        [
            "install",
            "ABCD234567",
            "--yes",
            "--no-tracking",
            "--no-capture",
            "--no-auto-update",
            "--no-agent-rules",
        ],
    )
    assert result.exit_code == 0, result.output
    assert [event for event, _ in entry] == ["apply"]
    assert entry[0][1]["authorization_needs"] == ["api", "mcp"]
    assert entry[0][1]["capture_sources"] == []


def test_short_code_credentials_use_the_existing_persistence_path(entry, monkeypatch):
    from probe.sdk import device

    calls = []

    def mint(base_url, **kwargs):
        calls.append(kwargs)
        return {
            "grants": [
                {"grant": "api", "token": "probe_pat_full"},
                {"grant": "mcp", "token": "probe_pat_read"},
            ]
        }

    monkeypatch.setattr(device, "device_authorize", mint)
    monkeypatch.setattr(setup, "sync_codex_mcp_token", lambda: [])
    granted, _ = setup.authorize(
        ["api", "mcp"], base_url="https://api.test", install_code="ABCD234567"
    )
    stored = load_context()
    assert calls[0]["install_code"] == "ABCD234567"
    assert granted["api"]["token"] == stored["token"] == "probe_pat_full"
    assert stored["mcp_token"] == "probe_pat_read"
    assert "ABCD234567" not in str(stored)


def test_onboarding_requirement_propagates_through_credential_persistence(entry, monkeypatch):
    from probe.sdk import device

    def mint(*a, **kw):
        raise OnboardingRequired("Finish onboarding", onboarding_url="https://dash.test/onboarding")

    monkeypatch.setattr(device, "device_authorize", mint)
    with pytest.raises(OnboardingRequired):
        setup.authorize(["api"], base_url="https://api.test")
    assert not load_context().get("token")


@pytest.mark.parametrize("incomplete", [False, True])
def test_install_auth_failure_exits_before_any_tooling_changes(entry, monkeypatch, incomplete):
    def authorize(*a, **kw):
        if incomplete:
            raise OnboardingRequired(
                "Finish onboarding", onboarding_url="https://dash.test/onboarding"
            )
        return {}, ["The website code expired."]

    monkeypatch.setattr(setup, "authorize", authorize)
    for name in ("apply_tracking", "apply_capture", "apply_agent_rules", "refresh_marketplace"):
        monkeypatch.setattr(
            setup, name, lambda *a, **kw: pytest.fail("no installation before authentication")
        )
    with pytest.raises(main.typer.Exit) as caught:
        apply_wizard_action(
            Action.CONFIGURE,
            caps=Capabilities(claude_available=True),
            base_now="https://api.test",
            yes=True,
            tracking=True,
            capture=True,
            auto_update=True,
            agent_rules=True,
            uninstall=False,
            configured=False,
            authorization_needs=["api", "mcp", "capture"],
            install_code="ABCD234567",
        )
    assert caught.value.exit_code == (0 if incomplete else 1)


@pytest.mark.parametrize("rejected", [True, False])
def test_doctor_distinguishes_rejected_credentials_from_offline(entry, monkeypatch, rejected):
    from probe.sdk import errors

    save_context({"token": "probe_pat_saved", "base_url": "https://api.test"})

    class Client:
        def __init__(self, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def me(self):
            if rejected:
                raise errors.AuthError("revoked")
            raise errors.TransportError("offline")

    monkeypatch.setattr("probe.sdk.client.Client", Client)
    caps = collect_capabilities()
    assert caps.api_credential_valid is (False if rejected else None)


@pytest.mark.parametrize("code", ["ABCD234567", None])
def test_only_explicit_code_overrides_matching_inherited_credentials(entry, monkeypatch, code):
    from probe.sdk import device

    for variable in ("PROBE_TOKEN", "PROBE_MCP_TOKEN", "PROBE_INGEST_TOKEN"):
        monkeypatch.setenv(variable, "previous-credential")
    monkeypatch.setenv("PROBE_SERVICE_TOKEN", "unrelated-service-token")
    monkeypatch.setattr(
        device,
        "device_authorize",
        lambda *a, **kw: {
            "grants": [
                {"grant": "api", "token": "new-api-token"},
                {"grant": "mcp", "token": "new-mcp-token"},
                {"grant": "capture", "capture_source": "claude_code", "token": "new-capture-token"},
            ]
        },
    )
    during_sync = []
    monkeypatch.setattr(setup, "sync_codex_mcp_token", lambda: during_sync.append(resolve()) or [])
    _granted, messages = setup.authorize(
        ["api", "mcp", "capture"],
        base_url="https://api.test",
        install_code=code,
    )
    settings = resolve()
    if code:
        assert (settings.token, settings.mcp_token, settings.ingest_token) == (
            "new-api-token",
            "new-mcp-token",
            "new-capture-token",
        )
        assert during_sync[0].token == "new-api-token"
        assert during_sync[0].mcp_token == "new-mcp-token"
        assert "unset PROBE_TOKEN PROBE_MCP_TOKEN PROBE_INGEST_TOKEN" in " ".join(messages)
    else:
        assert (
            settings.token == settings.mcp_token == settings.ingest_token == "previous-credential"
        )
        assert not any("unset" in message for message in messages)
    assert settings.service_token == "unrelated-service-token"
    assert "previous-credential" not in " ".join(messages)
    assert "new-api-token" not in " ".join(messages)


def test_explicit_code_preserves_environment_for_unreturned_grants(entry, monkeypatch):
    from probe.sdk import device

    monkeypatch.setenv("PROBE_TOKEN", "previous-api")
    monkeypatch.setenv("PROBE_INGEST_TOKEN", "unrelated-capture")
    monkeypatch.setattr(
        device,
        "device_authorize",
        lambda *a, **kw: {
            "grants": [{"grant": "api", "token": "new-api"}],
        },
    )
    setup.authorize(["api"], base_url="https://api.test", install_code="ABCD234567")
    assert resolve().token == "new-api"
    assert os.environ["PROBE_INGEST_TOKEN"] == "unrelated-capture"


@pytest.mark.parametrize("failure", ["redeem", "persist"])
def test_failed_code_keeps_inherited_credential_precedence(entry, monkeypatch, failure):
    from probe.sdk import config, device

    save_context({"token": "previous-saved-api"})
    monkeypatch.setenv("PROBE_TOKEN", "previous-environment-api")

    def mint(*args, **kwargs):
        if failure == "redeem":
            raise DeviceLoginError("The code expired.")
        return {"grants": [{"grant": "api", "token": "new-api"}]}

    def cannot_save(*args, **kwargs):
        raise OSError("config is read only")

    monkeypatch.setattr(device, "device_authorize", mint)
    if failure == "persist":
        monkeypatch.setattr(config, "save_context", cannot_save)
    granted, _messages = setup.authorize(
        ["api"], base_url="https://api.test", install_code="ABCD234567"
    )
    assert granted == {}
    assert os.environ["PROBE_TOKEN"] == "previous-environment-api"
    assert resolve().token == "previous-environment-api"
    assert load_context()["token"] == "previous-saved-api"


def test_code_selects_the_new_identity_for_signin_and_following_menu_actions(entry, monkeypatch):
    from probe.sdk import device

    monkeypatch.setenv("PROBE_TOKEN", "previous-environment-api")
    monkeypatch.setattr(setup, "sign_in", sign_in_to_account)
    monkeypatch.setattr(
        device,
        "device_authorize",
        lambda *a, **kw: {
            "grants": [
                {"grant": "api", "token": "new-api"},
                {"grant": "mcp", "token": "new-mcp"},
            ]
        },
    )
    monkeypatch.setattr(setup, "sync_codex_mcp_token", lambda: [])
    identities = []

    def account_email(base_url):
        identities.append(resolve().token)
        return "new@example.test"

    monkeypatch.setattr(setup, "account_email", account_email)

    def menu(_caps):
        identities.append(resolve().token)
        return Action.EXIT

    monkeypatch.setattr(setup, "run_action_menu", menu)
    result = CliRunner().invoke(main.app, ["wizard", "ABCD234567"])
    assert result.exit_code == 0, result.output
    assert identities == ["new-api", "new-api"]
    assert "new@example.test" in result.output
    assert "unset PROBE_TOKEN" in result.output
    assert "previous-environment-api" not in result.output
    assert "new-api" not in result.output


@pytest.mark.parametrize("exported_token", [False, True])
def test_sign_out_cleans_the_current_account_and_exits_without_reopening(
    entry, monkeypatch, exported_token
):
    from probe.cli.capabilities import TokenSource

    save_context({"token": "saved-api", "mcp_token": "saved-mcp", "base_url": "https://api.test"})
    if exported_token:
        monkeypatch.setenv("PROBE_TOKEN", "exported-api")
    monkeypatch.setattr(setup, "detectable_sources", lambda: ("claude_code", "codex"))
    monkeypatch.setattr(main, "_run_wizard_action", apply_wizard_action)
    monkeypatch.setattr(
        setup, "sign_in", lambda **kw: pytest.fail("sign-out must not sign back in")
    )
    monkeypatch.setattr(setup, "capture_token_sources", lambda _source: (TokenSource.PAIRED_FILE,))
    monkeypatch.setattr(setup.codex_config, "configured_bearer", lambda _name: None)
    revoked, stopped, menus = [], [], []
    monkeypatch.setattr(setup, "_revoke", lambda token, **kw: revoked.append(token) or [])

    def stop_capture(_mode):
        stopped.append(setup.agent_source())
        return SimpleNamespace(summary=lambda: "capture stopped", warnings=[])

    monkeypatch.setattr(setup, "turn_off", stop_capture)
    monkeypatch.setattr(
        setup, "run_action_menu", lambda caps: menus.append(caps) or Action.SIGN_OUT
    )
    # The confirmation page answered "Sign out" (Richard 2026-09-29).
    monkeypatch.setattr(setup, "confirm_sign_out", lambda account=None: True)
    monkeypatch.setattr(
        tui,
        "page",
        lambda *a, **kw: pytest.fail("sign-out must exit without a return-to-menu page"),
    )
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    assert len(menus) == 1
    assert revoked == ["saved-api", "saved-mcp"]
    assert stopped == ["claude_code", "codex"]
    assert not load_context().get("token")
    assert "Signed out" in result.output


@pytest.mark.parametrize("action", ["account", "settings"])
def test_direct_interactive_account_and_settings_screens_require_login(entry, monkeypatch, action):
    def apply(*a, **kw):
        assert resolve().token
        entry.append(("apply", kw))
        return []

    monkeypatch.setattr(main, "_run_wizard_action", apply)
    result = CliRunner().invoke(main.app, ["wizard", "--action", action])
    assert result.exit_code == 0, result.output
    assert [event for event, _ in entry] == ["signin", "apply"]


def test_no_main_menu_after_an_action_clears_the_account(entry, monkeypatch):
    from probe.sdk.config import clear_context, current_context_name

    save_context({"token": "saved-api"})
    menus = []
    monkeypatch.setattr(
        setup, "run_action_menu", lambda caps: menus.append(caps) or Action.DIAGNOSE
    )

    def clear_account(*a, **kw):
        clear_context(current_context_name())
        return ["The account was cleared."]

    monkeypatch.setattr(main, "_run_wizard_action", clear_account)
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    assert len(menus) == 1
    assert "Sign in to use the wizard" in result.output
    assert not any(event == "signin" for event, _ in entry)


def test_reported_login_success_cannot_open_a_menu_without_credentials(entry, monkeypatch):
    monkeypatch.setattr(setup, "sign_in", lambda **kw: setup.SignInResult(ok=True, lines=[]))
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    assert not any(event == "menu" for event, _ in entry)


@pytest.mark.parametrize("action", ["account", "settings"])
def test_reported_login_success_cannot_open_submenus_with_rejected_credentials(entry, monkeypatch, action):
    monkeypatch.setenv("PROBE_TOKEN", "revoked-exported-token")
    monkeypatch.setattr(doctor, "collect", lambda: Capabilities(api_credential_valid=False))
    result = CliRunner().invoke(main.app, ["wizard", "--action", action])
    assert result.exit_code == 0, result.output
    assert not any(event == "apply" for event, _ in entry)
    assert "Sign in to use the wizard" in result.output


@pytest.mark.parametrize("action", ["diagnose", "uninstall", "logout"])
def test_headless_maintenance_stays_available_while_signed_out(entry, monkeypatch, action):
    monkeypatch.setattr(setup, "interactive", lambda: False)
    monkeypatch.setattr(
        setup, "sign_in", lambda **kw: pytest.fail("maintenance must not require a browser")
    )
    result = CliRunner().invoke(main.app, ["wizard", "--action", action, "--yes"])
    assert result.exit_code == 0, result.output
    assert [event for event, _ in entry] == ["apply"]


def test_uninstall_signs_the_device_out_once_however_many_agents(entry, monkeypatch):
    """The account is device-wide -- one config file -- so it is released ONCE,
    after the last coding agent has been torn down.

    Ordering is the load-bearing part: each agent's pass ends by publishing its
    emptied state to the server with the token this releases, so releasing from
    inside that loop would turn the next agent's registration into a 401 and
    leave the dashboard showing a device that is gone.
    """
    order: list[str] = []
    monkeypatch.setattr(
        main, "_run_wizard_action", lambda *a, **kw: order.append("removed") or ["Removed."]
    )
    monkeypatch.setattr(
        setup, "finish_removal", lambda: order.append("released") or ["Signed out."]
    )

    result = CliRunner().invoke(
        main.app, ["wizard", "--action", "uninstall", "--agent", "both", "--yes"]
    )

    assert result.exit_code == 0, result.output
    assert order == ["removed", "removed", "released"]
    assert "Signed out." in result.output


def test_declining_the_removal_signs_nobody_out(entry, monkeypatch):
    """Uninstall now clears the credentials, so "no" at the confirmation has to
    mean no -- an empty result from a back-out must not fall through into a
    sign-out the user just refused."""
    monkeypatch.setattr(main, "_run_wizard_action", lambda *a, **kw: None)
    monkeypatch.setattr(
        setup, "finish_removal", lambda: pytest.fail("a declined removal must not sign out")
    )

    result = CliRunner().invoke(main.app, ["wizard", "--action", "uninstall"])

    assert result.exit_code == 0, result.output


def test_declining_at_the_confirmation_reports_nothing_happened(entry, monkeypatch):
    """`_run_wizard_action` answers None for a pure back-out. It used to answer
    `[]` here, which reads as "the action ran and had nothing to say" -- a
    "press enter" pause on an empty page, a state re-read for nothing, and now
    also the signal that decides whether to release the account."""
    monkeypatch.setattr(setup, "confirm_removal", lambda *_a, **_kw: False)
    monkeypatch.setattr(
        setup, "remove_everything", lambda *_a, **_kw: pytest.fail("declined, so nothing to remove")
    )

    assert (
        apply_wizard_action(
            Action.UNINSTALL,
            caps=Capabilities(claude_available=True),
            base_now="https://api.test",
            yes=False,
            tracking=None,
            capture=None,
            auto_update=None,
            agent_rules=None,
            uninstall=True,
            configured=True,
        )
        is None
    )


def test_staying_signed_in_on_the_confirmation_page_goes_back_to_the_menu(entry, monkeypatch):
    """Richard 2026-09-29: a confirmation page so nobody signs out by accident.
    "Stay signed in" is the menu again, with nothing changed and the wizard open."""
    save_context({"token": "saved-api", "mcp_token": "saved-mcp", "base_url": "https://api.test"})
    monkeypatch.setattr(main, "_run_wizard_action", apply_wizard_action)
    picks = iter([Action.SIGN_OUT, Action.EXIT])
    menus: list = []
    monkeypatch.setattr(setup, "run_action_menu", lambda caps: menus.append(caps) or next(picks))
    monkeypatch.setattr(setup, "confirm_sign_out", lambda account=None: False)
    monkeypatch.setattr(setup, "sign_out", lambda sources: pytest.fail("declined: must not sign out"))
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    assert len(menus) == 2, "the menu came back after the page"
    assert load_context().get("token") == "saved-api"
