"""Tests for PullRequestCreationPostSubmitError."""

from agentic_devtools.cli.azure_devops.commands import PullRequestCreationPostSubmitError


def test_error_can_be_caught_as_runtime_error_with_message() -> None:
    message = "workflow advancement failed"

    try:
        raise PullRequestCreationPostSubmitError(message)
    except RuntimeError as error:
        assert str(error) == message
