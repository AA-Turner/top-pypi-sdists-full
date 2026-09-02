"""Tests for the A2 capability-negotiation additive flags (TRK-M1-02).

``supports_assignment`` and ``supports_terminal_transition`` describe two
affordances the sync engine must negotiate (TRK-M1-03 A11) so it never
patches assignees or a terminal status onto a connector that must refuse
them. This file pins:

- the flags exist on TrackerCapabilities, default False, and are included
  in as_dict() (which stays dict[str, bool] — REQ-02, N20);
- each shipped connector's get_capabilities() equals the frozen per-
  connector table from the TRK-M1-01 draft (A2, P10):
  InMemory -> True/True, Beads -> False/False, FP -> False/False.

Consulting these flags inside SyncEngine (A11, N4) is TRK-M1-03 scope, not
tested here.
"""

from __future__ import annotations

import dataclasses

import pytest

from spec_kitty_tracker.capabilities import TrackerCapabilities
from spec_kitty_tracker.connectors.beads import BeadsConnector
from spec_kitty_tracker.connectors.fp import FPConnector
from spec_kitty_tracker.connectors.in_memory import InMemoryConnector


def test_new_flags_default_false_and_are_bool() -> None:
    caps = TrackerCapabilities()
    assert caps.supports_assignment is False
    assert caps.supports_terminal_transition is False


def test_as_dict_stays_dict_str_bool_and_includes_new_flags() -> None:
    caps = TrackerCapabilities(supports_assignment=True, supports_terminal_transition=True)
    as_dict = caps.as_dict()

    assert as_dict["supports_assignment"] is True
    assert as_dict["supports_terminal_transition"] is True
    assert all(isinstance(value, bool) for value in as_dict.values())
    assert isinstance(as_dict, dict)


def test_new_flags_are_declared_dataclass_fields() -> None:
    field_names = {f.name for f in dataclasses.fields(TrackerCapabilities)}
    assert "supports_assignment" in field_names
    assert "supports_terminal_transition" in field_names


@pytest.mark.asyncio
async def test_in_memory_connector_capability_table() -> None:
    connector = InMemoryConnector(name="in_memory", workspace="test")
    caps = await connector.get_capabilities()
    assert caps.supports_assignment is True
    assert caps.supports_terminal_transition is True


@pytest.mark.asyncio
async def test_beads_connector_capability_table() -> None:
    connector = BeadsConnector()
    caps = await connector.get_capabilities()
    assert caps.supports_assignment is False
    assert caps.supports_terminal_transition is False


@pytest.mark.asyncio
async def test_fp_connector_capability_table() -> None:
    connector = FPConnector()
    caps = await connector.get_capabilities()
    assert caps.supports_assignment is False
    assert caps.supports_terminal_transition is False
