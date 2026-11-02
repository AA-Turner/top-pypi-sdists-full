"""Tests for validate_property_section_mapping and validate_issue_template_block."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.issue_template.exceptions import TemplateValidationError
from agentic_devtools.cli.issue_template.mapping_validation import validate_property_section_mapping


class TestValidatePropertySectionMapping:
    """FR-005 config key/target/shape validation matrix."""

    def test_valid_mapping_canonicalizes_alias(self) -> None:
        result = validate_property_section_mapping(
            {"issue_id": "frontmatter", "url": "body:Links", "created_at": "omit"}
        )
        assert result == {"id": "frontmatter", "url": "body:Links", "created_at": "omit"}

    def test_non_object_mapping_rejected(self) -> None:
        with pytest.raises(TemplateValidationError, match="must be an object"):
            validate_property_section_mapping(42)

    def test_non_string_value_rejected(self) -> None:
        with pytest.raises(TemplateValidationError, match=r'"url" must be a string'):
            validate_property_section_mapping({"url": {"section": "Links"}})

    def test_shape_validation_runs_before_target_validation(self) -> None:
        """Non-string entry values fail before unsupported string targets."""
        with pytest.raises(TemplateValidationError, match=r'"url" must be a string'):
            validate_property_section_mapping({"description": "sidebar", "url": 42})

    def test_frontmatter_only_key_non_frontmatter_target_rejected(self) -> None:
        with pytest.raises(TemplateValidationError, match="status.*frontmatter"):
            validate_property_section_mapping({"status": "body:Details"})

    def test_frontmatter_only_key_frontmatter_accepted(self) -> None:
        assert validate_property_section_mapping({"title": "frontmatter"}) == {"title": "frontmatter"}

    def test_unsupported_target_rejected(self) -> None:
        with pytest.raises(TemplateValidationError, match="sidebar"):
            validate_property_section_mapping({"description": "sidebar"})

    def test_omit_target_accepted(self) -> None:
        assert validate_property_section_mapping({"url": "omit"}) == {"url": "omit"}

    def test_out_of_scope_key_rejected(self) -> None:
        with pytest.raises(TemplateValidationError, match="not a configurable canonical property"):
            validate_property_section_mapping({"priority": "frontmatter"})

    def test_derived_key_rejected(self) -> None:
        with pytest.raises(TemplateValidationError, match="not a configurable canonical property"):
            validate_property_section_mapping({"rendered_at": "frontmatter"})

    def test_empty_section_name_rejected(self) -> None:
        with pytest.raises(TemplateValidationError, match="description.*empty"):
            validate_property_section_mapping({"description": "body:   "})

    def test_control_char_section_name_rejected(self) -> None:
        with pytest.raises(TemplateValidationError, match="control or DEL"):
            validate_property_section_mapping({"description": "body:Bad\tSection"})

    def test_del_char_section_name_rejected(self) -> None:
        with pytest.raises(TemplateValidationError, match="control or DEL"):
            validate_property_section_mapping({"description": "body:Bad\u007fSection"})

    def test_hash_section_name_rejected(self) -> None:
        with pytest.raises(TemplateValidationError, match="#"):
            validate_property_section_mapping({"description": "body:Foo#Bar"})

    def test_section_name_128_accepted(self) -> None:
        name = "x" * 128
        assert validate_property_section_mapping({"description": f"body:{name}"}) == {"description": f"body:{name}"}

    def test_section_name_129_rejected(self) -> None:
        with pytest.raises(TemplateValidationError, match="128"):
            validate_property_section_mapping({"description": "body:" + "x" * 129})

    def test_id_issue_id_conflict_rejected(self) -> None:
        with pytest.raises(TemplateValidationError, match="conflicting targets"):
            validate_property_section_mapping({"id": "frontmatter", "issue_id": "omit"})

    def test_id_issue_id_same_target_collapses(self) -> None:
        assert validate_property_section_mapping({"id": "frontmatter", "issue_id": "frontmatter"}) == {
            "id": "frontmatter"
        }

    def test_id_present_with_non_string_issue_id_defers_to_shape(self) -> None:
        with pytest.raises(TemplateValidationError, match="must be a string"):
            validate_property_section_mapping({"id": "frontmatter", "issue_id": 5})

    def test_empty_mapping_returns_empty(self) -> None:
        assert validate_property_section_mapping({}) == {}
