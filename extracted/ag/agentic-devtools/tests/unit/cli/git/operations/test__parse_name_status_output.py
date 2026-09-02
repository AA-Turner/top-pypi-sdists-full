"""Tests for agentic_devtools.cli.git.operations._parse_name_status_output."""

from agentic_devtools.cli.git import operations


class TestParseNameStatusOutput:
    """Tests for _parse_name_status_output."""

    def test_parses_nul_delimited_status_records(self):
        """Parse A/M/R records from --name-status -z output."""
        changed_files, change_types, rename_sources = operations._parse_name_status_output(
            "A\x00src/new.ts\x00M\x00src/edit.ts\x00R100\x00src/old.ts\x00src/new-name.ts\x00"
        )

        assert changed_files == ["src/new.ts", "src/edit.ts", "src/new-name.ts"]
        assert change_types == {"src/new.ts": "add", "src/edit.ts": "edit", "src/new-name.ts": "rename"}
        assert rename_sources == {"src/new-name.ts": "src/old.ts"}

    def test_skips_malformed_nul_record_without_path(self):
        """Ignore trailing status token when it has no corresponding path field."""
        changed_files, change_types, rename_sources = operations._parse_name_status_output("M\x00src/file.ts\x00A\x00")

        assert changed_files == ["src/file.ts"]
        assert change_types == {"src/file.ts": "edit"}
        assert rename_sources == {}

    def test_keeps_first_occurrence_order_and_latest_change_type(self):
        """Deduplicate changed_files while preserving the last change type."""
        changed_files, change_types, rename_sources = operations._parse_name_status_output(
            "M\x00src/file.ts\x00D\x00src/file.ts\x00"
        )

        assert changed_files == ["src/file.ts"]
        assert change_types == {"src/file.ts": "delete"}
        assert rename_sources == {}

    def test_preserves_unquoted_utf8_paths_with_name_status_z(self):
        """Keep UTF-8 path text unchanged when parsing -z output."""
        changed_files, change_types, rename_sources = operations._parse_name_status_output("M\x00src/café.py\x00")

        assert changed_files == ["src/café.py"]
        assert change_types == {"src/café.py": "edit"}
        assert rename_sources == {}

    def test_skips_incomplete_rename_record(self):
        """Stop cleanly when an R-status record is missing destination fields."""
        changed_files, change_types, rename_sources = operations._parse_name_status_output("R100\x00src/old.ts\x00")

        assert changed_files == []
        assert change_types == {}
        assert rename_sources == {}

    def test_skips_nul_record_with_empty_path(self):
        """Ignore records where status exists but the parsed path token is empty."""
        changed_files, change_types, rename_sources = operations._parse_name_status_output(
            "M\x00\x00A\x00src/new.ts\x00"
        )

        assert changed_files == ["src/new.ts"]
        assert change_types == {"src/new.ts": "add"}
        assert rename_sources == {}

    def test_parses_nul_records_without_trailing_separator(self):
        """Handle -z output that does not end with a trailing NUL separator."""
        changed_files, change_types, rename_sources = operations._parse_name_status_output("M\x00src/file.ts")

        assert changed_files == ["src/file.ts"]
        assert change_types == {"src/file.ts": "edit"}
        assert rename_sources == {}

    def test_fallback_mode_skips_empty_status_and_empty_path(self):
        """Line-delimited fallback ignores empty status and empty path rows."""
        changed_files, change_types, rename_sources = operations._parse_name_status_output(
            "\tpath-only\nM\t\nA\tsrc/new.ts\n"
        )

        assert changed_files == ["src/new.ts"]
        assert change_types == {"src/new.ts": "add"}
        assert rename_sources == {}
