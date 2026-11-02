"""A provider-written object is adopted under a NAMED lifecycle, chosen by name.

A workflow step (or any caller that is configured, not coded) can only name a
policy as text. The package owns the one list of declared policies so a name
resolves to exactly the policy the janitor would use, and an unknown name is
refused with the names that exist rather than silently adopting under nothing.
"""

from __future__ import annotations

import pytest

from matrx_files import (
    DECLARED_RETENTION_POLICIES,
    MEET_RECORDING_RETENTION_POLICY,
    VOICE_RECORDING_RETENTION_POLICY,
    retention_policy_by_name,
)


def test_every_declared_policy_resolves_by_its_own_name() -> None:
    assert retention_policy_by_name("meet_recordings_30d") is MEET_RECORDING_RETENTION_POLICY
    assert retention_policy_by_name("voice_recordings_30d") is VOICE_RECORDING_RETENTION_POLICY
    for name, policy in DECLARED_RETENTION_POLICIES.items():
        assert policy.name == name


def test_an_unknown_name_is_refused_naming_the_known_ones() -> None:
    with pytest.raises(KeyError) as raised:
        retention_policy_by_name("forever")
    message = str(raised.value)
    assert "forever" in message
    assert "meet_recordings_30d" in message


def test_policy_names_are_unique() -> None:
    names = [policy.name for policy in DECLARED_RETENTION_POLICIES.values()]
    assert len(names) == len(set(names))
