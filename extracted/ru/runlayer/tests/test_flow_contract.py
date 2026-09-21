"""Closed flow-summary vocabularies stay in lockstep with the hook code.

``flow_contract`` must not import ``hook.clients`` / ``hook.dispatch`` /
``hook_install`` (its import closure is stdlib-only), so the client and
hook-event sets are literal copies; these tests pin the copies to their
sources.
"""

import pytest

from runlayer_cli.flow_contract import CLIENT_FLOW_CLIENTS, CLIENT_FLOW_HOOK_EVENTS
from runlayer_cli.hook import dispatch as hook_dispatch
from runlayer_cli.hook.clients import EVENT_NORMALIZE, Client, normalize_event_name
from runlayer_cli.hook_install import clients as hook_install_clients


def _registered_hook_names() -> set[str]:
    """Every event name an installer writes into a client's hook config."""
    tables = (
        hook_install_clients._ENFORCEMENT_HOOKS,
        hook_install_clients._PIPELINE_HOOKS,
        hook_install_clients._MCP_USAGE_METADATA_HOOKS,
    )
    return {name for table in tables for names in table.values() for name in names}


def test_clients_match_client_enum() -> None:
    assert CLIENT_FLOW_CLIENTS == {c.value for c in Client}


def test_hook_events_cover_every_normalized_name() -> None:
    assert set(EVENT_NORMALIZE.values()) <= CLIENT_FLOW_HOOK_EVENTS


def test_hook_events_cover_every_dispatch_key() -> None:
    assert set(hook_dispatch._DISPATCH_TABLE) <= CLIENT_FLOW_HOOK_EVENTS


@pytest.mark.parametrize("name", sorted(_registered_hook_names()))
def test_hook_events_cover_every_installer_registered_name(name: str) -> None:
    # A registered name that is not in the set spools as "other", which
    # defeats the attribution the field exists for.
    assert normalize_event_name(name) in CLIENT_FLOW_HOOK_EVENTS


def test_hook_events_include_the_fallback_bucket() -> None:
    assert "other" in CLIENT_FLOW_HOOK_EVENTS
