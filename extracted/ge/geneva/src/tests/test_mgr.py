# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Unit tests for geneva.runners.ray._mgr helpers."""

import os

import pytest

import geneva.runners.ray._mgr as ray_mgr


def test_align_uv_project_environment_sets_match(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """uv is pointed at the active venv to silence the VIRTUAL_ENV warning."""
    monkeypatch.setenv("VIRTUAL_ENV", "/abs/path/.venv")
    monkeypatch.delenv("UV_PROJECT_ENVIRONMENT", raising=False)

    ray_mgr._align_uv_project_environment()

    assert os.environ["UV_PROJECT_ENVIRONMENT"] == "/abs/path/.venv"


def test_align_uv_project_environment_respects_caller_override(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An explicit UV_PROJECT_ENVIRONMENT is never overwritten."""
    monkeypatch.setenv("VIRTUAL_ENV", "/abs/path/.venv")
    monkeypatch.setenv("UV_PROJECT_ENVIRONMENT", "/custom/env")

    ray_mgr._align_uv_project_environment()

    assert os.environ["UV_PROJECT_ENVIRONMENT"] == "/custom/env"


def test_align_uv_project_environment_no_venv(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """With no active venv, nothing is set."""
    monkeypatch.delenv("VIRTUAL_ENV", raising=False)
    monkeypatch.delenv("UV_PROJECT_ENVIRONMENT", raising=False)

    ray_mgr._align_uv_project_environment()

    assert "UV_PROJECT_ENVIRONMENT" not in os.environ
