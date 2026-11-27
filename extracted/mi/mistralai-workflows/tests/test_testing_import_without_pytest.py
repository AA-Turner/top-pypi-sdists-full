import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

_IMPORT_TESTING = """
import mistralai.workflows.testing
from mistralai.workflows.testing import (
    DEFAULT_TEST_TASK_QUEUE,
    TEST_TASK_QUEUE,
    get_internal_activities,
    min_api_version,
)
"""


def _run(script: str, **env: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-c", _IMPORT_TESTING + textwrap.dedent(script)],
        capture_output=True,
        text=True,
        env={**os.environ, **env},
        timeout=120,
    )


class TestTestingImportWithoutPytest:
    @pytest.mark.parametrize(
        ("script", "returncode"),
        [
            pytest.param(
                """
                import sys

                assert get_internal_activities()
                assert "pytest" not in sys.modules
                """,
                0,
                id="imports-without-pytest",
            ),
            pytest.param(
                """
                try:
                    min_api_version("2.0")
                except ImportError as exc:
                    assert "pytest" in str(exc)
                else:
                    raise AssertionError("min_api_version must require pytest")

                import mistralai.workflows.testing.fixtures
                """,
                1,
                id="pytest-backed-surfaces-require-pytest",
            ),
        ],
    )
    def test_optional_pytest(self, tmp_path: Path, script: str, returncode: int) -> None:
        (tmp_path / "pytest.py").write_text('raise ImportError("pytest is unavailable")\n', encoding="utf-8")
        pythonpath = os.pathsep.join([str(tmp_path), os.environ.get("PYTHONPATH", "")])

        result = _run(script, PYTHONPATH=pythonpath)

        assert result.returncode == returncode, result.stderr
        if returncode:
            assert "ImportError: pytest is unavailable" in result.stderr
