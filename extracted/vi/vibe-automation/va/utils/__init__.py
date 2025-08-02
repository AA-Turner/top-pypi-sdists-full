# Utility helpers shared across the Vibe-Automation SDK

TEST_EXECUTION_PREFIX = "test"
"""Prefix used by the SDK to mark test executions that are *not*
backed by a corresponding execution entity in the backend.
"""


def is_test_execution(execution_id: str) -> bool:  # noqa: D401 – simple helper
    """Return True if *execution_id* denotes a local test execution.

    The convention is that test executions are assigned an id that starts with
    the string defined in :data:`TEST_EXECUTION_PREFIX`.  In those situations
    we must avoid calling backend services (they would fail because the
    execution does not exist server-side).
    """
    return execution_id.startswith(TEST_EXECUTION_PREFIX)
