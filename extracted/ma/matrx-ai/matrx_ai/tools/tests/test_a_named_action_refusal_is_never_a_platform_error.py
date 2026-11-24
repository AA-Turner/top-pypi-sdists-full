"""A NAMED ACTION REFUSAL IS NEVER A PLATFORM ERROR (2026-11-05).

Live: ``tool_execution_failed`` rows for ``org_section_place`` ("That form was not found."),
``org_section_unplace`` ("That placement was not found, or you cannot change it.") and
``mandate_create`` ("Mandate … is invalid", "… already exists — open it instead"). Each was
an Action's honest refusal the agent read and corrected, but ``ActionFailed`` defaulted
``error_type`` to ``execution``, so the tool executor paged operations for it.

SUT: the real ``ActionFailed`` and the executor's real ``_is_expected_domain_failure``.
A real failure (``build_failed``) is still filed.
"""

from __future__ import annotations

import pytest
from matrx_graph.actions import ActionFailed

from matrx_ai.tools.executor import _is_expected_domain_failure


@pytest.mark.parametrize(
    ("code", "expected_type"),
    [
        ("refused", "refused"),
        ("not_found", "not_found"),
        ("mandate_not_found", "not_found"),
        ("kind_not_found", "not_found"),
    ],
)
def test_a_code_that_names_a_refusal_is_not_filed(code: str, expected_type: str) -> None:
    exc = ActionFailed(code=code, message="That placement was not found, or you cannot change it.")
    assert exc.error_type == expected_type
    assert _is_expected_domain_failure(tool_name="org_section_unplace", error_type=exc.error_type, message=exc.message)


def test_a_real_failure_is_still_filed() -> None:
    exc = ActionFailed(code="build_failed", message="The agent builder returned no agent.")
    assert exc.error_type == "execution"
    assert not _is_expected_domain_failure(tool_name="mandate_holder_build", error_type=exc.error_type, message=exc.message)


def test_an_explicit_error_type_wins() -> None:
    assert ActionFailed(code="refused", message="x", error_type="execution").error_type == "execution"
    assert ActionFailed(code="mandate_rejected", message="x", error_type="validation").error_type == "validation"

