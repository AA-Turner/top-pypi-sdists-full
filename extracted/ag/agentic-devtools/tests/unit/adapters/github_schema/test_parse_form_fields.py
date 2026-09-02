"""Tests for agentic_devtools.adapters.github_schema.parse_form_fields."""

from __future__ import annotations

from typing import Any

from agentic_devtools.adapters.github_schema import parse_form_fields


class TestParseFormFields:
    """Tests for the parse_form_fields function."""

    def test_dropdown_with_allowed_values(self) -> None:
        """Dropdown field produces PropertySchema with allowed_values."""
        body = [
            {
                "type": "dropdown",
                "id": "priority",
                "attributes": {
                    "label": "Priority",
                    "options": ["high", "medium", "low"],
                },
            }
        ]
        result = parse_form_fields(body)
        assert len(result) == 1
        assert result[0]["name"] == "priority"
        assert result[0]["type"] == "dropdown"
        assert result[0]["allowed_values"] == ["high", "medium", "low"]
        assert result[0]["required"] is False

    def test_textarea_with_id(self) -> None:
        """Textarea field uses id as name when present."""
        body = [
            {
                "type": "textarea",
                "id": "description",
                "attributes": {
                    "label": "Describe the bug",
                    "validations": {"required": True},
                },
            }
        ]
        result = parse_form_fields(body)
        assert len(result) == 1
        assert result[0]["name"] == "description"
        assert result[0]["type"] == "textarea"
        assert result[0]["required"] is True
        assert result[0]["allowed_values"] is None

    def test_textarea_fallback_to_slugified_label(self) -> None:
        """Field without id uses slugified label as name."""
        body = [
            {
                "type": "textarea",
                "attributes": {
                    "label": "Steps To Reproduce",
                },
            }
        ]
        result = parse_form_fields(body)
        assert len(result) == 1
        assert result[0]["name"] == "steps_to_reproduce"

    def test_checkboxes_required_from_validations(self) -> None:
        """Checkboxes required from validations.required."""
        body = [
            {
                "type": "checkboxes",
                "id": "terms",
                "attributes": {
                    "label": "Terms",
                    "validations": {"required": True},
                    "options": [
                        {"label": "I agree", "required": False},
                    ],
                },
            }
        ]
        result = parse_form_fields(body)
        assert result[0]["required"] is True
        assert result[0]["allowed_values"] == ["I agree"]

    def test_checkboxes_required_from_option(self) -> None:
        """Checkboxes required when any option has required=True."""
        body = [
            {
                "type": "checkboxes",
                "id": "agreements",
                "attributes": {
                    "label": "Agreements",
                    "options": [
                        {"label": "Accept ToS", "required": True},
                        {"label": "Subscribe newsletter"},
                    ],
                },
            }
        ]
        result = parse_form_fields(body)
        assert result[0]["required"] is True
        assert result[0]["allowed_values"] == ["Accept ToS", "Subscribe newsletter"]

    def test_skips_markdown_elements(self) -> None:
        """Markdown elements are skipped entirely."""
        body = [
            {"type": "markdown", "attributes": {"value": "# Header"}},
            {"type": "input", "id": "name", "attributes": {"label": "Name"}},
        ]
        result = parse_form_fields(body)
        assert len(result) == 1
        assert result[0]["name"] == "name"

    def test_skips_malformed_elements(self) -> None:
        """Elements without type or name are silently skipped."""
        body: list[dict[str, Any]] = [
            {"attributes": {"label": "No type"}},  # missing type
            {"type": "input"},  # missing id and label
            {"type": "input", "id": "valid", "attributes": {"label": "Valid"}},
        ]
        result = parse_form_fields(body)
        assert len(result) == 1
        assert result[0]["name"] == "valid"

    def test_non_dict_elements_skipped(self) -> None:
        """Non-dict elements in body list are skipped."""
        body: list[Any] = [
            "string_element",
            42,
            None,
            {"type": "input", "id": "ok", "attributes": {"label": "OK"}},
        ]
        result = parse_form_fields(body)
        assert len(result) == 1
        assert result[0]["name"] == "ok"

    def test_empty_body(self) -> None:
        """Empty body list returns empty properties."""
        assert parse_form_fields([]) == []

    def test_input_field(self) -> None:
        """Input field produces correct PropertySchema."""
        body = [
            {
                "type": "input",
                "id": "version",
                "attributes": {"label": "Version"},
            }
        ]
        result = parse_form_fields(body)
        assert result[0]["type"] == "input"
        assert result[0]["required"] is False
        assert result[0]["allowed_values"] is None

    def test_non_dict_attributes_treated_as_empty(self) -> None:
        """Non-dict attributes value is treated as empty dict."""
        body = [
            {
                "type": "input",
                "id": "field1",
                "attributes": "not a dict",
            }
        ]
        result = parse_form_fields(body)
        # Should still produce result since id is present
        assert len(result) == 1
        assert result[0]["name"] == "field1"

    def test_non_dict_validations_treated_as_empty(self) -> None:
        """Non-dict validations value is treated as empty dict."""
        body = [
            {
                "type": "input",
                "id": "field1",
                "attributes": {"label": "Field", "validations": "not a dict"},
            }
        ]
        result = parse_form_fields(body)
        assert len(result) == 1
        assert result[0]["required"] is False

    def test_checkboxes_without_options_list(self) -> None:
        """Checkboxes without options list produces no allowed_values."""
        body = [
            {
                "type": "checkboxes",
                "id": "checks",
                "attributes": {"label": "Checks", "options": "not a list"},
            }
        ]
        result = parse_form_fields(body)
        assert result[0]["allowed_values"] is None

    def test_checkboxes_non_dict_options_skipped(self) -> None:
        """Non-dict options in checkboxes are skipped."""
        body = [
            {
                "type": "checkboxes",
                "id": "checks",
                "attributes": {
                    "label": "Checks",
                    "options": ["not_a_dict", {"label": "Valid"}],
                },
            }
        ]
        result = parse_form_fields(body)
        assert result[0]["allowed_values"] == ["Valid"]

    def test_checkboxes_option_without_string_label(self) -> None:
        """Checkbox option dict without string label is not added to allowed_values."""
        body = [
            {
                "type": "checkboxes",
                "id": "checks",
                "attributes": {
                    "label": "Checks",
                    "options": [{"label": 123}, {"label": "Valid"}],
                },
            }
        ]
        result = parse_form_fields(body)
        assert result[0]["allowed_values"] == ["Valid"]

    def test_dropdown_without_options_list(self) -> None:
        """Dropdown without options list produces no allowed_values."""
        body = [
            {
                "type": "dropdown",
                "id": "severity",
                "attributes": {"label": "Severity", "options": "not a list"},
            }
        ]
        result = parse_form_fields(body)
        assert result[0]["allowed_values"] is None

    def test_checkboxes_all_malformed_options_returns_none(self) -> None:
        """Checkboxes where all options lack string labels produce None allowed_values."""
        body = [
            {
                "type": "checkboxes",
                "id": "checks",
                "attributes": {
                    "label": "Checks",
                    "options": [{"label": 42}, "not_a_dict"],
                },
            }
        ]
        result = parse_form_fields(body)
        assert result[0]["allowed_values"] is None

    def test_dropdown_all_none_options_returns_none(self) -> None:
        """Dropdown where every option is None produces None allowed_values."""
        body = [
            {
                "type": "dropdown",
                "id": "priority",
                "attributes": {"label": "Priority", "options": [None, None]},
            }
        ]
        result = parse_form_fields(body)
        assert result[0]["allowed_values"] is None

    def test_dropdown_dict_options_with_label(self) -> None:
        """Dropdown dict options with a string label are accepted."""
        body = [
            {
                "type": "dropdown",
                "id": "severity",
                "attributes": {
                    "label": "Severity",
                    "options": [{"label": "high"}, {"label": "low"}],
                },
            }
        ]
        result = parse_form_fields(body)
        assert result[0]["allowed_values"] == ["high", "low"]

    def test_dropdown_malformed_dict_options_skipped(self) -> None:
        """Dropdown dict options without a string label are silently skipped."""
        body = [
            {
                "type": "dropdown",
                "id": "severity",
                "attributes": {
                    "label": "Severity",
                    "options": [{"label": 42}, {"other_key": "value"}, None],
                },
            }
        ]
        result = parse_form_fields(body)
        assert result[0]["allowed_values"] is None

    def test_dropdown_mixed_valid_and_invalid_options(self) -> None:
        """Dropdown with mixed valid strings and invalid entries returns only valid ones."""
        body = [
            {
                "type": "dropdown",
                "id": "priority",
                "attributes": {
                    "label": "Priority",
                    "options": ["high", {"label": "medium"}, {"label": 99}, None, 42],
                },
            }
        ]
        result = parse_form_fields(body)
        assert result[0]["allowed_values"] == ["high", "medium"]

    def test_label_that_slugifies_to_empty_is_skipped(self) -> None:
        """Field with non-alphanumeric label and no id is skipped."""
        body = [{"type": "input", "attributes": {"label": "!!!"}}]
        result = parse_form_fields(body)
        assert result == []

    def test_label_with_surrounding_whitespace_no_underscores(self) -> None:
        """Label with surrounding whitespace is stripped before slugifying to avoid leading/trailing underscores."""
        body = [{"type": "input", "attributes": {"label": " Bug "}}]
        result = parse_form_fields(body)
        assert len(result) == 1
        assert result[0]["name"] == "bug"
