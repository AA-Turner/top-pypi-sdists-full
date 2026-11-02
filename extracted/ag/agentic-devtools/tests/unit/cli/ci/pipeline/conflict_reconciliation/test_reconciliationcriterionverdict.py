"""Criterion verdict records are frozen."""

from dataclasses import FrozenInstanceError

import pytest


def test_frozen(attestation):
    with pytest.raises(FrozenInstanceError):
        attestation.criterion_verdicts[0].rationale = "changed"
