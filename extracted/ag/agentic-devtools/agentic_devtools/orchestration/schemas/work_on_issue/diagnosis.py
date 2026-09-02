"""Test failure diagnosis models for structured LLM output schemas.

Provides TestFailureDiagnosis and RepairAction for analyzing and fixing test failures.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class RepairAction(BaseModel):
    """A specific code change to fix a failing test.

    Represents the minimal change needed to make a test pass,
    with clear identification of the target location and change.
    """

    file_path: str = Field(description="Path to the file that needs to be changed")
    line: int | None = Field(default=None, description="Line number where the change should be applied")
    original_code: str = Field(default="", description="The code that should be replaced (if applicable)")
    replacement_code: str = Field(description="The new code to insert or replace")
    explanation: str = Field(default="", description="Why this change fixes the test failure")


class TestFailureDiagnosis(BaseModel):
    """Analysis of why a test failed and proposed repair actions.

    Provides a structured diagnosis including root cause analysis
    and one or more repair actions to fix the failure.
    """

    test_name: str = Field(description="Fully qualified name of the failing test")
    error_message: str = Field(description="The error message or assertion failure text")
    root_cause: str = Field(description="Analysis of the root cause of the failure")
    repair_actions: list[RepairAction] = Field(
        default_factory=list,
        description="Ordered list of code changes to fix the failure",
    )
