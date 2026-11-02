"""Tests for watchdog cooldown gating across read-token pool identities."""

from datetime import UTC, datetime
from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.ci.cooldown import CooldownRecord
from agentic_devtools.cli.ci.credential_roles import DEFAULT_CLASSIC_REPO_WORKFLOW_PAT
from agentic_devtools.cli.ci.watchdog_command import _provider_cooldown


def test_checks_default_cooldown_when_read_pool_is_unavailable() -> None:
    provider = Mock()
    now = datetime(2026, 10, 15, tzinfo=UTC)
    paused = ("github:DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", CooldownRecord(resume_at=1_800_000_000))

    with (
        patch.dict("os.environ", {}, clear=True),
        patch("agentic_devtools.cli.ci.watchdog_command._get_read_token_pool", return_value=None),
        patch("agentic_devtools.cli.ci.watchdog_command.active_cooldown", return_value=paused) as active_cooldown,
    ):
        assert _provider_cooldown(provider, now) == paused

    assert active_cooldown.call_args.kwargs["credential_identity"] == (DEFAULT_CLASSIC_REPO_WORKFLOW_PAT,)


def test_checks_default_cooldown_when_an_alternate_pool_identity_is_available() -> None:
    provider = Mock()
    read_pool = Mock()
    read_pool.blocking_cooldown_identities = ()
    read_pool.active_cooldown_for.return_value = None

    with (
        patch.dict("os.environ", {}, clear=True),
        patch("agentic_devtools.cli.ci.watchdog_command._get_read_token_pool", return_value=read_pool),
        patch("agentic_devtools.cli.ci.watchdog_command.active_cooldown", return_value=None) as active_cooldown,
        patch("agentic_devtools.cli.ci.watchdog_command.DispatcherWakeStore") as wake_store,
    ):
        wake_store.return_value.entries.return_value = {}
        assert _provider_cooldown(provider, datetime(2026, 10, 15, tzinfo=UTC)) is None

    assert active_cooldown.call_args.kwargs["credential_identity"] == (DEFAULT_CLASSIC_REPO_WORKFLOW_PAT,)


def test_default_cooldown_pauses_even_when_pool_has_no_blockers() -> None:
    provider = Mock()
    read_pool = Mock()
    read_pool.blocking_cooldown_identities = ()
    paused = ("github:DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", CooldownRecord(resume_at=1_800_000_000))

    with (
        patch.dict("os.environ", {}, clear=True),
        patch("agentic_devtools.cli.ci.watchdog_command._get_read_token_pool", return_value=read_pool),
        patch("agentic_devtools.cli.ci.watchdog_command.active_cooldown", return_value=paused) as active_cooldown,
    ):
        assert _provider_cooldown(provider, datetime(2026, 10, 15, tzinfo=UTC)) == paused

    assert active_cooldown.call_args.kwargs["credential_identity"] == (DEFAULT_CLASSIC_REPO_WORKFLOW_PAT,)


def test_uses_current_run_pool_cooldown_when_persistence_is_unavailable() -> None:
    provider = Mock()
    read_pool = Mock()
    read_pool.blocking_cooldown_identities = ()
    read_pool.active_cooldown_for.return_value = None
    now = datetime(2026, 10, 15, tzinfo=UTC)
    paused = (
        f"github:{DEFAULT_CLASSIC_REPO_WORKFLOW_PAT}",
        CooldownRecord(resume_at=now.timestamp() + 120, source="retry-after", updated_at=now.timestamp()),
    )
    read_pool.active_cooldown_for.return_value = paused

    with (
        patch.dict("os.environ", {}, clear=True),
        patch("agentic_devtools.cli.ci.watchdog_command._get_read_token_pool", return_value=read_pool),
        patch("agentic_devtools.cli.ci.watchdog_command.active_cooldown", return_value=None) as active_cooldown,
    ):
        assert _provider_cooldown(provider, now) == paused

    identities = (DEFAULT_CLASSIC_REPO_WORKFLOW_PAT,)
    assert active_cooldown.call_args.kwargs["credential_identity"] == identities
    read_pool.active_cooldown_for.assert_called_once_with(identities, now=now.timestamp())


def test_checks_all_pool_identities_when_they_are_unavailable() -> None:
    provider = Mock()
    read_pool = Mock()
    identities = (
        "NOEKVIST_EXT_SWICA_CLASSIC_REPO_WORKFLOW_PAT",
        "CTRUX_EXT_SWICA_CLASSIC_REPO_WORKFLOW_PAT",
    )
    read_pool.blocking_cooldown_identities = identities
    read_pool.active_cooldown_for.return_value = None

    with (
        patch.dict("os.environ", {}, clear=True),
        patch("agentic_devtools.cli.ci.watchdog_command._get_read_token_pool", return_value=read_pool),
        patch("agentic_devtools.cli.ci.watchdog_command.active_cooldown", return_value=None) as active_cooldown,
        patch("agentic_devtools.cli.ci.watchdog_command.DispatcherWakeStore") as wake_store,
    ):
        wake_store.return_value.entries.return_value = {}
        assert _provider_cooldown(provider, datetime(2026, 10, 15, tzinfo=UTC)) is None

    assert active_cooldown.call_args.kwargs["credential_identity"] == (
        DEFAULT_CLASSIC_REPO_WORKFLOW_PAT,
        *identities,
    )


def test_uses_latest_pending_wake_as_shared_provider_deadline() -> None:
    provider = Mock()
    read_pool = Mock()
    read_pool.blocking_cooldown_identities = ()
    read_pool.active_cooldown_for.return_value = None
    now = datetime(2026, 10, 15, tzinfo=UTC)
    entries = {
        "earlier": {"resume_at": now.timestamp() + 120},
        "later": {"resume_at": now.timestamp() + 300},
    }
    with (
        patch.dict("os.environ", {}, clear=True),
        patch("agentic_devtools.cli.ci.watchdog_command._get_read_token_pool", return_value=read_pool),
        patch("agentic_devtools.cli.ci.watchdog_command.active_cooldown", return_value=None),
        patch("agentic_devtools.cli.ci.watchdog_command.DispatcherWakeStore") as wake_store,
    ):
        wake_store.return_value.entries.return_value = entries
        paused = _provider_cooldown(provider, now)

    assert paused is not None
    assert paused[1].resume_at == now.timestamp() + 300
    wake_store.return_value.entries.assert_called_once_with(now=now.timestamp())


@pytest.mark.parametrize(
    ("shared_delay", "wake_delay"),
    [(120, 300), (300, 120)],
)
def test_active_shared_cooldown_uses_the_later_pending_wake(shared_delay: int, wake_delay: int) -> None:
    provider = Mock()
    read_pool = Mock()
    read_pool.blocking_cooldown_identities = ()
    read_pool.active_cooldown_for.return_value = None
    now = datetime(2026, 10, 15, tzinfo=UTC)
    shared = ("github:DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", CooldownRecord(now.timestamp() + shared_delay))
    with (
        patch.dict("os.environ", {}, clear=True),
        patch("agentic_devtools.cli.ci.watchdog_command._get_read_token_pool", return_value=read_pool),
        patch("agentic_devtools.cli.ci.watchdog_command.active_cooldown", return_value=shared),
        patch("agentic_devtools.cli.ci.watchdog_command.DispatcherWakeStore") as wake_store,
    ):
        wake_store.return_value.entries.return_value = {"wake": {"resume_at": now.timestamp() + wake_delay}}
        paused = _provider_cooldown(provider, now)

    assert paused is not None
    assert paused[1].resume_at == now.timestamp() + max(shared_delay, wake_delay)


def test_unreadable_wake_deadline_state_fails_closed() -> None:
    provider = Mock()
    now = datetime(2026, 10, 15, tzinfo=UTC)
    with (
        patch.dict("os.environ", {}, clear=True),
        patch("agentic_devtools.cli.ci.watchdog_command._get_read_token_pool", return_value=None),
        patch("agentic_devtools.cli.ci.watchdog_command.active_cooldown", return_value=None),
        patch("agentic_devtools.cli.ci.watchdog_command.DispatcherWakeStore") as wake_store,
    ):
        wake_store.return_value.entries.side_effect = RuntimeError("unreadable")
        paused = _provider_cooldown(provider, now)

    assert paused is not None
    assert paused[1].resume_at == now.timestamp() + 60


def test_real_wake_store_http_503_fails_closed_for_provider_work() -> None:
    provider = Mock()
    provider.get_variable.side_effect = RuntimeError("HTTP 503 service unavailable")
    now = datetime(2026, 10, 15, tzinfo=UTC)

    with (
        patch.dict("os.environ", {}, clear=True),
        patch("agentic_devtools.cli.ci.watchdog_command._get_read_token_pool", return_value=None),
        patch("agentic_devtools.cli.ci.watchdog_command.active_cooldown", return_value=None),
    ):
        paused = _provider_cooldown(provider, now)

    assert paused is not None
    assert paused[1].resume_at == now.timestamp() + 60
    provider.get_variable.assert_called_once_with("AI_PR_LOOP_PROVIDER_COOLDOWNS", use_writer_token=True)
