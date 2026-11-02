"""Tests for GitHubProvider."""

from __future__ import annotations

import json
import subprocess


def _make_run_mock(stdout: str = "", stderr: str = "", returncode: int = 0):
    """Create a mock run_command callable."""

    def mock_run(*args, **kwargs):
        return subprocess.CompletedProcess(args=args[0], returncode=returncode, stdout=stdout, stderr=stderr)

    return mock_run


def _link_run_mock(
    *,
    resolve_id: int | str = 123456,
    post_returncode: int = 0,
    post_stdout: str = "{}",
    post_stderr: str = "",
):
    """Mock run_command for link_subissue: resolves the child, checks sub_issues, then POSTs.

    The child-resolution ``GET /issues/{n}`` returns ``resolve_id`` as the
    database ID; the ``GET /issues/{n}/sub_issues`` idempotency check returns
    an empty list; the ``POST .../sub_issues`` call returns the configured
    result.  Routing distinguishes between the three call shapes.
    """
    resolve_response = json.dumps(
        {"id": resolve_id, "node_id": "I_kwDOchild", "html_url": "https://github.com/org/repo/issues/1"}
    )

    def mock_run(*args, **kwargs):
        argv = args[0]
        if "--method" in argv and "POST" in argv:
            return subprocess.CompletedProcess(
                args=argv, returncode=post_returncode, stdout=post_stdout, stderr=post_stderr
            )
        # GET /issues/{n}/sub_issues — return empty list for the idempotency check
        if any(a.endswith("/sub_issues") for a in argv):
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout="[]", stderr="")
        return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

    return mock_run
