"""Tests for _build_submission_manager."""

from types import SimpleNamespace
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.pr_review_submit import (
    _SUBMIT_MAX_RETRIES,
    _build_submission_manager,
)

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_submit"


class TestBuildSubmissionManager:
    def test_wires_processor_and_manager(self):
        review_state = SimpleNamespace(repoId="repo-guid")
        requests_module = object()
        processor = object()
        manager = object()
        with (
            patch(f"{_MODULE}.load_review_state", return_value=review_state) as load,
            patch(f"{_MODULE}.AzureDevOpsConfig") as config_cls,
            patch(f"{_MODULE}.get_auth_headers", return_value={"h": "v"}),
            patch(f"{_MODULE}.get_pat", return_value="pat"),
            patch(f"{_MODULE}.create_review_processor", return_value=processor) as make_proc,
            patch(f"{_MODULE}.SubmissionManager", return_value=manager) as manager_cls,
        ):
            config_cls.from_state.return_value = "config"
            result = _build_submission_manager(99, requests_module)

        assert result is manager
        load.assert_called_once_with(99, fallback_to_branch=False)
        make_proc.assert_called_once_with("config", {"h": "v"}, "repo-guid", requests_module=requests_module)
        manager_cls.assert_called_once_with(processor=processor, max_retries=_SUBMIT_MAX_RETRIES)

    def test_wires_deferred_shared_updates(self):
        """The batch submit path asks the processor to defer shared operations."""
        review_state = SimpleNamespace(repoId="repo-guid")
        requests_module = object()
        with (
            patch(f"{_MODULE}.load_review_state", return_value=review_state),
            patch(f"{_MODULE}.AzureDevOpsConfig") as config_cls,
            patch(f"{_MODULE}.get_auth_headers", return_value={"h": "v"}),
            patch(f"{_MODULE}.get_pat", return_value="pat"),
            patch(f"{_MODULE}.create_review_processor", return_value="processor") as make_proc,
            patch(f"{_MODULE}.SubmissionManager", return_value="manager") as manager_cls,
        ):
            config_cls.from_state.return_value = "config"
            result = _build_submission_manager(99, requests_module, defer_shared_updates=True)

        assert result == "manager"
        make_proc.assert_called_once_with(
            "config",
            {"h": "v"},
            "repo-guid",
            requests_module=requests_module,
            defer_shared_updates=True,
        )
        manager_cls.assert_called_once_with(processor="processor", max_retries=_SUBMIT_MAX_RETRIES)
