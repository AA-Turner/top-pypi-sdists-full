"""Frozen attestations cannot be assigned to or extended."""

from dataclasses import FrozenInstanceError

import pytest


def test_frozen(attestation):
    with pytest.raises(FrozenInstanceError):
        attestation.repository = "other/repo"
    with pytest.raises(FrozenInstanceError):
        attestation.extra = "value"
