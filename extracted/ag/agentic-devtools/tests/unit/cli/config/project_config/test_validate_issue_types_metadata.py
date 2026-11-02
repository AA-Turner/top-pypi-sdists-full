"""Tests for validate_issue_types_metadata function."""

import pytest

from agentic_devtools.cli.config.project_config import validate_issue_types_metadata


def _make_valid_entry() -> dict:
    """Return a minimal valid issue_types_metadata entry."""
    return {
        "lastDiscovered": "2026-07-12T10:00:00+00:00",
        "lastRefreshed": "2026-07-12T10:00:00+00:00",
        "provider": "jira",
        "issue_types": [],
    }


def _make_valid_property() -> dict:
    """Return a minimal valid PropertyEntry."""
    return {
        "name": "summary",
        "display_name": "Summary",
        "type": "string",
        "required": True,
        "allowed_values": None,
        "included_in_template": True,
    }


def _make_valid_issue_type() -> dict:
    """Return a minimal valid IssueTypeEntry."""
    return {
        "id": "10000",
        "name": "Bug",
        "description": "A problem.",
        "is_subtask": False,
        "properties": [_make_valid_property()],
    }


class TestValidateIssueTypesMetadataHappyPath:
    """Tests for valid entries that should pass without error."""

    def test_valid_entry_passes(self):
        """A fully valid entry raises no error."""
        entry = _make_valid_entry()
        entry["issue_types"] = [_make_valid_issue_type()]
        validate_issue_types_metadata(entry)

    def test_empty_issue_types_array_valid(self):
        """An empty issue_types array is accepted."""
        entry = _make_valid_entry()
        validate_issue_types_metadata(entry)

    def test_empty_properties_array_valid(self):
        """An issue type with empty properties array is accepted."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["properties"] = []
        entry["issue_types"] = [it]
        validate_issue_types_metadata(entry)

    def test_empty_description_valid(self):
        """An issue type with empty string description is accepted."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["description"] = ""
        entry["issue_types"] = [it]
        validate_issue_types_metadata(entry)

    def test_allowed_values_null_accepted(self):
        """allowed_values as None is accepted."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["properties"] = [_make_valid_property()]
        it["properties"][0]["allowed_values"] = None
        entry["issue_types"] = [it]
        validate_issue_types_metadata(entry)

    def test_allowed_values_list_of_strings_accepted(self):
        """allowed_values as list of non-empty strings is accepted."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        prop = _make_valid_property()
        prop["allowed_values"] = ["High", "Medium", "Low"]
        it["properties"] = [prop]
        entry["issue_types"] = [it]
        validate_issue_types_metadata(entry)


class TestValidateIssueTypesMetadataForwardCompat:
    """Tests for forward compatibility — unknown keys accepted at all levels."""

    def test_extra_keys_at_top_level(self):
        """Unknown keys at top level are accepted."""
        entry = _make_valid_entry()
        entry["future_field"] = "whatever"
        validate_issue_types_metadata(entry)

    def test_extra_keys_at_issue_type_level(self):
        """Unknown keys in IssueTypeEntry are accepted."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["new_field"] = 42
        entry["issue_types"] = [it]
        validate_issue_types_metadata(entry)

    def test_extra_keys_at_property_level(self):
        """Unknown keys in PropertyEntry are accepted."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["properties"][0]["extra"] = True
        entry["issue_types"] = [it]
        validate_issue_types_metadata(entry)


class TestValidateIssueTypesMetadataMissingFields:
    """Tests for missing required top-level fields."""

    @pytest.mark.parametrize("field", ["lastDiscovered", "lastRefreshed", "provider", "issue_types"])
    def test_missing_required_field(self, field):
        """Missing required top-level field raises ValueError."""
        entry = _make_valid_entry()
        del entry[field]
        with pytest.raises(ValueError, match=f"missing required field '{field}'"):
            validate_issue_types_metadata(entry)


class TestValidateIssueTypesMetadataTimestamps:
    """Tests for ISO-8601 timestamp validation."""

    @pytest.mark.parametrize("field", ["lastDiscovered", "lastRefreshed"])
    def test_unparseable_timestamp(self, field):
        """Unparseable timestamp raises ValueError identifying the field."""
        entry = _make_valid_entry()
        entry[field] = "not-a-timestamp"
        with pytest.raises(ValueError, match=f"'{field}'.*not a valid ISO-8601"):
            validate_issue_types_metadata(entry)

    @pytest.mark.parametrize("field", ["lastDiscovered", "lastRefreshed"])
    def test_timestamp_without_timezone(self, field):
        """Timestamp without timezone raises ValueError."""
        entry = _make_valid_entry()
        entry[field] = "2026-07-12T10:00:00"
        with pytest.raises(ValueError, match=f"'{field}'.*timezone-aware"):
            validate_issue_types_metadata(entry)

    @pytest.mark.parametrize("field", ["lastDiscovered", "lastRefreshed"])
    def test_timestamp_with_z_suffix(self, field):
        """Timestamp with Z suffix raises ValueError."""
        entry = _make_valid_entry()
        entry[field] = "2026-07-12T10:00:00Z"
        with pytest.raises(ValueError, match=f"'{field}'.*not 'Z' suffix"):
            validate_issue_types_metadata(entry)

    @pytest.mark.parametrize("field", ["lastDiscovered", "lastRefreshed"])
    def test_timestamp_non_zero_utc_offset(self, field):
        """Timestamp with non-zero UTC offset raises ValueError."""
        entry = _make_valid_entry()
        entry[field] = "2026-07-12T10:00:00+02:00"
        with pytest.raises(ValueError, match=f"'{field}'.*zero UTC offset"):
            validate_issue_types_metadata(entry)

    @pytest.mark.parametrize("field", ["lastDiscovered", "lastRefreshed"])
    def test_timestamp_wrong_type(self, field):
        """Non-string timestamp raises ValueError."""
        entry = _make_valid_entry()
        entry[field] = 12345
        with pytest.raises(ValueError, match=f"'{field}' must be a string"):
            validate_issue_types_metadata(entry)

    @pytest.mark.parametrize("field", ["lastDiscovered", "lastRefreshed"])
    @pytest.mark.parametrize("offset", ["-00:00", "+0000", "+00"])
    def test_timestamp_non_canonical_zero_offset(self, field, offset):
        """Non-canonical zero-offset encodings are rejected even though they parse to UTC."""
        entry = _make_valid_entry()
        entry[field] = f"2026-07-12T10:00:00{offset}"
        with pytest.raises(ValueError, match=f"'{field}'.*canonical.*\\+00:00"):
            validate_issue_types_metadata(entry)


class TestValidateIssueTypesMetadataProvider:
    """Tests for provider field validation."""

    def test_empty_provider_rejected(self):
        """Empty provider string raises ValueError."""
        entry = _make_valid_entry()
        entry["provider"] = ""
        with pytest.raises(ValueError, match="'provider' must be a non-empty string"):
            validate_issue_types_metadata(entry)

    def test_whitespace_only_provider_rejected(self):
        """Whitespace-only provider string raises ValueError."""
        entry = _make_valid_entry()
        entry["provider"] = "   "
        with pytest.raises(ValueError, match="'provider' must be a non-empty string"):
            validate_issue_types_metadata(entry)

    def test_provider_wrong_type(self):
        """Non-string provider raises ValueError."""
        entry = _make_valid_entry()
        entry["provider"] = 42
        with pytest.raises(ValueError, match="'provider' must be a string"):
            validate_issue_types_metadata(entry)


class TestValidateIssueTypesMetadataIssueTypes:
    """Tests for issue_types array and IssueTypeEntry validation."""

    def test_issue_types_not_a_list(self):
        """Non-list issue_types raises ValueError."""
        entry = _make_valid_entry()
        entry["issue_types"] = "not_a_list"
        with pytest.raises(ValueError, match="'issue_types' must be a list"):
            validate_issue_types_metadata(entry)

    def test_issue_type_not_a_dict(self):
        """Non-dict issue type entry raises ValueError."""
        entry = _make_valid_entry()
        entry["issue_types"] = ["not_a_dict"]
        with pytest.raises(ValueError, match=r"issue_types\[0\] must be a dict"):
            validate_issue_types_metadata(entry)

    def test_issue_type_empty_id(self):
        """Empty id raises ValueError."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["id"] = ""
        entry["issue_types"] = [it]
        with pytest.raises(ValueError, match=r"issue_types\[0\]\.id must be a non-empty"):
            validate_issue_types_metadata(entry)

    def test_issue_type_whitespace_only_id_rejected(self):
        """Whitespace-only id raises ValueError."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["id"] = "   "
        entry["issue_types"] = [it]
        with pytest.raises(ValueError, match=r"issue_types\[0\]\.id must be a non-empty"):
            validate_issue_types_metadata(entry)

    def test_issue_type_id_wrong_type(self):
        """Non-string id raises ValueError."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["id"] = 10000
        entry["issue_types"] = [it]
        with pytest.raises(ValueError, match=r"issue_types\[0\]\.id must be a string"):
            validate_issue_types_metadata(entry)

    def test_issue_type_name_wrong_type(self):
        """Non-string name raises ValueError."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["name"] = 42
        entry["issue_types"] = [it]
        with pytest.raises(ValueError, match=r"issue_types\[0\]\.name must be a string"):
            validate_issue_types_metadata(entry)

    def test_issue_type_empty_name(self):
        """Empty name raises ValueError."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["name"] = ""
        entry["issue_types"] = [it]
        with pytest.raises(ValueError, match=r"issue_types\[0\]\.name must be a non-empty"):
            validate_issue_types_metadata(entry)

    def test_issue_type_whitespace_only_name_rejected(self):
        """Whitespace-only name raises ValueError."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["name"] = "   "
        entry["issue_types"] = [it]
        with pytest.raises(ValueError, match=r"issue_types\[0\]\.name must be a non-empty"):
            validate_issue_types_metadata(entry)

    def test_issue_type_description_wrong_type(self):
        """Non-string description raises ValueError."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["description"] = 123
        entry["issue_types"] = [it]
        with pytest.raises(ValueError, match=r"issue_types\[0\]\.description must be a string"):
            validate_issue_types_metadata(entry)

    def test_issue_type_is_subtask_wrong_type(self):
        """Non-boolean is_subtask raises ValueError."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["is_subtask"] = "true"
        entry["issue_types"] = [it]
        with pytest.raises(ValueError, match=r"issue_types\[0\]\.is_subtask must be a boolean"):
            validate_issue_types_metadata(entry)

    def test_issue_type_properties_not_a_list(self):
        """Non-list properties raises ValueError."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["properties"] = "not_a_list"
        entry["issue_types"] = [it]
        with pytest.raises(ValueError, match=r"issue_types\[0\]\.properties must be a list"):
            validate_issue_types_metadata(entry)


class TestValidateIssueTypesMetadataPropertyEntry:
    """Tests for PropertyEntry validation."""

    def test_property_not_a_dict(self):
        """Non-dict property entry raises ValueError."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["properties"] = ["not_a_dict"]
        entry["issue_types"] = [it]
        with pytest.raises(ValueError, match=r"issue_types\[0\]\.properties\[0\] must be a dict"):
            validate_issue_types_metadata(entry)

    @pytest.mark.parametrize("field", ["name", "display_name", "type"])
    def test_empty_string_field(self, field):
        """Empty string for required string field raises ValueError."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["properties"][0][field] = ""
        entry["issue_types"] = [it]
        with pytest.raises(ValueError, match=f"{field} must be a non-empty string"):
            validate_issue_types_metadata(entry)

    @pytest.mark.parametrize("field", ["name", "display_name", "type"])
    def test_whitespace_only_string_field_rejected(self, field):
        """Whitespace-only string for required string field raises ValueError."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["properties"][0][field] = "   "
        entry["issue_types"] = [it]
        with pytest.raises(ValueError, match=f"{field} must be a non-empty string"):
            validate_issue_types_metadata(entry)

    @pytest.mark.parametrize("field", ["name", "display_name", "type"])
    def test_wrong_type_string_field(self, field):
        """Non-string value for string field raises ValueError."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["properties"][0][field] = 42
        entry["issue_types"] = [it]
        with pytest.raises(ValueError, match=f"{field} must be a string"):
            validate_issue_types_metadata(entry)

    @pytest.mark.parametrize("field", ["required", "included_in_template"])
    def test_non_bool_boolean_field(self, field):
        """Non-boolean value for boolean field raises ValueError."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["properties"][0][field] = "true"
        entry["issue_types"] = [it]
        with pytest.raises(ValueError, match=f"{field} must be a boolean"):
            validate_issue_types_metadata(entry)

    def test_allowed_values_mixed_types(self):
        """allowed_values with non-string element raises ValueError."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["properties"][0]["allowed_values"] = ["High", 1, True]
        entry["issue_types"] = [it]
        with pytest.raises(ValueError, match=r"allowed_values\[1\] must be a string"):
            validate_issue_types_metadata(entry)

    def test_allowed_values_empty_string(self):
        """allowed_values with empty string raises ValueError."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["properties"][0]["allowed_values"] = ["High", ""]
        entry["issue_types"] = [it]
        with pytest.raises(ValueError, match=r"allowed_values\[1\] must be a non-empty"):
            validate_issue_types_metadata(entry)

    def test_allowed_values_whitespace_only_string_rejected(self):
        """allowed_values with whitespace-only string raises ValueError."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["properties"][0]["allowed_values"] = ["High", "   "]
        entry["issue_types"] = [it]
        with pytest.raises(ValueError, match=r"allowed_values\[1\] must be a non-empty"):
            validate_issue_types_metadata(entry)

    def test_allowed_values_wrong_type(self):
        """allowed_values as non-list/non-null raises ValueError."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        it["properties"][0]["allowed_values"] = "not_a_list"
        entry["issue_types"] = [it]
        with pytest.raises(ValueError, match="allowed_values must be a list or null"):
            validate_issue_types_metadata(entry)

    def test_allowed_values_key_missing_raises(self):
        """A property entry with no 'allowed_values' key raises ValueError."""
        entry = _make_valid_entry()
        it = _make_valid_issue_type()
        prop = it["properties"][0]
        del prop["allowed_values"]
        entry["issue_types"] = [it]
        with pytest.raises(ValueError, match="allowed_values must be present"):
            validate_issue_types_metadata(entry)


class TestValidateIssueTypesMetadataEntryType:
    """Tests for entry-level type validation."""

    def test_non_dict_entry_raises(self):
        """Non-dict entry raises ValueError."""
        with pytest.raises(ValueError, match="must be a dict"):
            validate_issue_types_metadata("not_a_dict")  # type: ignore[arg-type]
