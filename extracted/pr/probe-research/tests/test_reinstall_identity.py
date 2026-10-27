"""Identity first: a reinstall holds every credential to the account signed in (plan clean-uninstall-reinstall R-T4).

R5: a daemon key from an earlier install or another team survived sign-in
(`save_context` merges; a key was minted only when none was held), so the
daemon wrote to the OLD team. R7: a stale `PROBE_TOKEN` outranks a new
sign-in, and a warning alone let it win. R8: the sign-in released the old
credentials before what was queued under them was sent. The server is a fake
here: `whoami` answers per token.
"""

from __future__ import annotations

import pytest

from probe.cli import identity_check
from probe.cli import setup as wizard
from probe.sdk.config import load_context, save_context

URL = "https://api.example"
TEAM_A = {"customer_id": "team-a", "user_id": "u1", "email": "me@a.example"}
TEAM_B = {"customer_id": "team-b", "user_id": "u9", "email": "me@b.example"}


@pytest.fixture
def server(monkeypatch):
    """`whoami` answers from `accounts` (token -> /v1/me, or a state string);
    `_revoke` records what was released."""
    accounts: dict = {}
    released: list[str] = []

    def whoami(token, base_url):
        found = accounts.get(token, "rejected")
        return (found, None) if isinstance(found, str) else ("ok", found)

    monkeypatch.setattr(identity_check, "whoami", whoami)
    monkeypatch.setattr(wizard, "_revoke", lambda token, *, base_url, what: released.append(token) or [])
    for name in (*identity_check.TOKEN_VARIABLES, *identity_check.capture_variables(), "PROBE_BASE_URL"):
        monkeypatch.delenv(name, raising=False)
    return accounts, released


def _signed_in(**extra) -> None:
    save_context({"base_url": URL, "token": "probe_pat_mine", **extra})


def test_another_teams_daemon_key_is_released_dropped_and_approved_afresh(server, monkeypatch):
    accounts, released = server
    accounts.update(probe_pat_mine=TEAM_A, probe_pat_old_daemon=TEAM_B)
    _signed_in(companion_token="probe_pat_old_daemon")
    monkeypatch.setattr(identity_check, "_daemon_in_use", lambda: True)
    minted = []

    def mint(url):
        minted.append(url)
        save_context({"companion_token": "probe_pat_new_daemon"})
        return ["approved a new daemon key"]

    report = identity_check.reconcile(mint=mint)
    assert released == ["probe_pat_old_daemon"], "the other team's key is revoked on the server, not just forgotten"
    assert load_context()["companion_token"] == "probe_pat_new_daemon" and minted == [URL]
    assert not report.problems and any("team-b" in line for line in report.lines)


def test_a_refused_daemon_key_is_dropped_and_the_install_is_incomplete_until_one_is_approved(server, monkeypatch):
    accounts, released = server
    accounts.update(probe_pat_mine=TEAM_A)
    _signed_in(companion_token="probe_pat_revoked")
    monkeypatch.setattr(identity_check, "_daemon_in_use", lambda: True)
    report = identity_check.reconcile(mint=lambda url: None)
    assert "companion_token" not in load_context() and released == []
    assert any("daemon mode has no key" in problem for problem in report.problems)


def test_this_accounts_daemon_key_is_kept(server):
    accounts, released = server
    accounts.update(probe_pat_mine=TEAM_A, probe_pat_daemon=TEAM_A)
    _signed_in(companion_token="probe_pat_daemon")
    report = identity_check.reconcile()
    assert load_context()["companion_token"] == "probe_pat_daemon" and released == [] and not report.problems


def test_offline_nothing_is_dropped(server):
    accounts, _released = server
    accounts.update(probe_pat_mine=TEAM_A, probe_pat_daemon="unreachable")
    _signed_in(companion_token="probe_pat_daemon")
    report = identity_check.reconcile()
    assert load_context()["companion_token"] == "probe_pat_daemon" and not report.problems


@pytest.mark.parametrize("name", ["PROBE_TOKEN", "PROBE_MCP_TOKEN", "PROBE_INGEST_TOKEN", "PRBE_CODEX_TAP_TOKEN"])
def test_an_override_of_another_account_makes_the_install_incomplete_and_is_named(server, monkeypatch, name):
    accounts, _released = server
    accounts.update(probe_pat_mine=TEAM_A, probe_pat_stale=TEAM_B)
    _signed_in()
    monkeypatch.setenv(name, "probe_pat_stale")
    report = identity_check.reconcile()
    assert len(report.problems) == 1 and name in report.problems[0] and f"unset {name}" in report.problems[0]


def test_an_override_of_the_same_account_is_fine(server, monkeypatch):
    accounts, _released = server
    accounts.update(probe_pat_mine=TEAM_A, probe_pat_ci=TEAM_A)
    _signed_in()
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_ci")
    assert not identity_check.reconcile().problems


def test_a_base_url_override_that_disagrees_is_named(server, monkeypatch):
    accounts, _released = server
    accounts.update(probe_pat_mine=TEAM_A)
    _signed_in()
    monkeypatch.setenv("PROBE_BASE_URL", "https://other.example")
    problems = identity_check.reconcile().problems
    assert len(problems) == 1 and "PROBE_BASE_URL" in problems[0]


def test_sign_in_drains_the_old_credentials_queue_before_the_exchange(monkeypatch):
    """R8: the device-authorization exchange releases this device's old
    credentials on the server; what was queued under them was stranded."""
    order: list[str] = []
    _signed_in()
    monkeypatch.setattr(identity_check, "drain_before_switch", lambda: order.append("drain") or ["sent 3"])

    def authorize(grants, **_kw):
        order.append("exchange")
        return {}, []

    monkeypatch.setattr(wizard, "authorize", authorize)
    result = wizard.sign_in(base_url=URL)
    assert order == ["drain", "exchange"]
    assert "sent 3" in result.lines


def test_sign_in_clears_keeper_off(monkeypatch):
    """R-T2: `keeper-off` is cleared at any install, sign-in or configure start."""
    from probe.service import keeper, paths

    off = paths.root_dir() / keeper.OFF_NAME
    off.parent.mkdir(parents=True, exist_ok=True)
    off.touch()
    monkeypatch.setattr(wizard, "authorize", lambda grants, **_kw: ({}, []))
    wizard.sign_in(base_url=URL)
    assert not off.exists()


def test_the_drain_sends_what_is_queued_and_says_what_is_left(monkeypatch):
    from probe.sdk import journal

    class Queue:
        def pending(self):
            return iter([(1, "op"), (2, "op")])

    class Fake:
        def namespaces(self):
            return [Queue()]

    class Report:
        delivered, remaining = 1, 1

    monkeypatch.setattr(journal, "Journal", Fake)
    monkeypatch.setattr(journal, "drain", lambda j, **kw: Report())
    lines = identity_check.drain_before_switch(seconds=1)
    assert lines[0].startswith("sent 1 queued write") and "1 queued write(s) could not be sent" in lines[1]


def test_the_wizard_asks_the_server_only_when_there_is_something_to_hold_and_once(server, monkeypatch):
    """The configure of each agent reads `reconcile_once`: no `/v1/me` on a
    machine with no daemon key and no credential variable, one per pass else."""
    accounts, _released = server
    accounts.update(probe_pat_mine=TEAM_A, probe_pat_stale=TEAM_B)
    asked = []
    real = identity_check.whoami
    monkeypatch.setattr(identity_check, "whoami", lambda token, url: asked.append(token) or real(token, url))
    _signed_in()
    assert not identity_check.reconcile_once().problems and asked == []
    monkeypatch.setattr(identity_check, "_once", None)
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_stale")
    first = identity_check.reconcile_once()
    assert identity_check.reconcile_once() is first and len(asked) == 2
    assert "PROBE_TOKEN" in first.problems[0]
