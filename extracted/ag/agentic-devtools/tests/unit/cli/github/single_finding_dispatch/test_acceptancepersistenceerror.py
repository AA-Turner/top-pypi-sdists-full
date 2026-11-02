import pytest

from agentic_devtools.cli.github.single_finding_dispatch import AcceptancePersistenceError


def test_acceptance_persistence_error_preserves_reason():
    error = AcceptancePersistenceError("storage timed out")

    assert str(error) == "storage timed out"
    assert error.reason == "storage timed out"


def test_acceptance_persistence_error_requires_a_reason():
    with pytest.raises(ValueError, match="reason"):
        AcceptancePersistenceError(" ")
