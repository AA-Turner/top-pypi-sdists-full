import pytest

from agentic_devtools.adapters.issue_provider import DefinitiveCreationFailure, InMemoryIssueProvider


def test_definitive_creation_failure_is_value_error():
    assert issubclass(DefinitiveCreationFailure, ValueError)
    with pytest.raises(DefinitiveCreationFailure):
        InMemoryIssueProvider().create_issue("", "", "task")
