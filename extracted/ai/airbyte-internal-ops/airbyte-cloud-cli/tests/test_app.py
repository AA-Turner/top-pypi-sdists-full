from __future__ import annotations

import traceback
from unittest.mock import patch

import pytest
from airbyte.exceptions import PyAirbyteInputError, PyAirbyteInternalError
from airbyte_cloud_cli import app as app_module


def test_main_prints_pyairbyte_error_without_traceback(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with patch.object(
        app_module,
        "app",
        side_effect=PyAirbyteInputError(message="Organization ID is required."),
    ), pytest.raises(SystemExit) as error:
        app_module.main()

    assert error.value.code == 1
    stderr = capsys.readouterr().err
    assert stderr == "Organization ID is required.\n"
    assert "Traceback" not in stderr


def test_main_propagates_unexpected_exceptions() -> None:
    with patch.object(
        app_module, "app", side_effect=RuntimeError("unexpected")
    ), pytest.raises(RuntimeError, match="unexpected"):
        app_module.main()


def test_main_includes_guidance_and_help_url(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with patch.object(
        app_module,
        "app",
        side_effect=PyAirbyteInputError(
            message="Credentials are missing.",
            guidance="Set the required credentials.",
            help_url="https://example.com/credentials",
        ),
    ), pytest.raises(SystemExit) as error:
        app_module.main()

    assert error.value.code == 1
    assert capsys.readouterr().err == (
        "Credentials are missing.\n"
        "Guidance: Set the required credentials.\n"
        "More info: https://example.com/credentials\n"
    )


def test_main_reraises_internal_errors_with_traceback() -> None:
    with patch.object(
        app_module,
        "app",
        side_effect=PyAirbyteInternalError(message="Internal failure."),
    ), pytest.raises(PyAirbyteInternalError) as error:
        app_module.main()

    assert any(
        frame.name == "main"
        for frame in traceback.extract_tb(error.value.__traceback__)
    )
