"""A cloud browser that is still starting answers "retry in a few seconds": the model retries it, so it is an
expected lifecycle outcome and never a ``tool_execution_failed`` platform error. Real failures still file."""

from matrx_ai.tools.executor import _is_expected_domain_failure


def test_activation_in_progress_is_expected_for_cloud_browser() -> None:
    assert _is_expected_domain_failure(
        tool_name="cloud_browser",
        error_type="activation_in_progress",
        message="This browser is still starting. Retry this same action in a few seconds",
    )


def test_real_cloud_browser_failures_still_file() -> None:
    assert not _is_expected_domain_failure(tool_name="cloud_browser", error_type="worker_unreachable")
    assert not _is_expected_domain_failure(tool_name="data", error_type="activation_in_progress")
