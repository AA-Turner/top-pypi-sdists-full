import os

import pytest

WORKFLOW_EXAMPLE_HELLO_WORLD = "example-hello-world-workflow"
WORKFLOW_EXAMPLE_LONG_HELLO_WORLD = "example-long-hello-world-workflow"
WORKFLOW_EXAMPLE_INTERACTIVE_GAME = "example-interactive-game-workflow"
WORKFLOW_SIMPLE_CHATBOT = "simple-chatbot-workflow"

DEFAULT_TEST_TASK_QUEUE = "example-dev-worker"
TEST_TASK_QUEUE = os.getenv("DEPLOYMENT_NAME", DEFAULT_TEST_TASK_QUEUE)

_API_VERSION = os.getenv("API_VERSION", "")


def _parse_version(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("-"))


def _current_version_is_older(current_version: str, minimum_version: str) -> bool:
    if not current_version:
        return False
    return _parse_version(current_version) < _parse_version(minimum_version)


def min_api_version(version: str) -> pytest.MarkDecorator:
    return pytest.mark.xfail(
        _current_version_is_older(_API_VERSION, version),
        reason=f"Requires API version >= {version} (current: {_API_VERSION or 'unset'})",
        strict=True,
    )
