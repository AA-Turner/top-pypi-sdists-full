"""Tests for validate_issue_template_block."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.issue_template.exceptions import TemplateValidationError
from agentic_devtools.cli.issue_template.mapping_validation import validate_issue_template_block


class TestValidateIssueTemplateBlock:
    """FR-005 block shape validation."""

    def test_array_block_rejected(self) -> None:
        with pytest.raises(TemplateValidationError, match="issueTemplate.*must be an object"):
            validate_issue_template_block([1, 2, 3], "issueTemplate")

    def test_missing_mapping_returns_empty(self) -> None:
        assert validate_issue_template_block({}, "issueTemplate") == {}

    def test_null_mapping_returns_empty(self) -> None:
        assert validate_issue_template_block({"property_section_mapping": None}, "issueTemplate") == {}

    def test_non_object_mapping_rejected(self) -> None:
        with pytest.raises(TemplateValidationError, match="property_section_mapping.*must be an object"):
            validate_issue_template_block({"property_section_mapping": 42}, "issueTemplate")

    def test_valid_block(self) -> None:
        block = {"property_section_mapping": {"url": "omit"}}
        assert validate_issue_template_block(block, "issue_template") == {"url": "omit"}
