"""File verdict records are frozen."""

from dataclasses import FrozenInstanceError

import pytest


def test_frozen(attestation):
    with pytest.raises(FrozenInstanceError):
        attestation.file_verdicts[0].behavior = "changed"
