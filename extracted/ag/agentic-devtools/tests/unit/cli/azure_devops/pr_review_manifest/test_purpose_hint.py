"""Tests for purpose_hint."""

from agentic_devtools.cli.azure_devops.pr_review_manifest import purpose_hint


class TestPurposeHint:
    def test_empty_path(self):
        assert purpose_hint("", "edit") == "metadata-only change"

    def test_test_file(self):
        assert purpose_hint("/tests/test_state.py", "edit") == "tests/fixtures for test_state.py"

    def test_spec_file(self):
        assert purpose_hint("/src/a.spec.ts", "edit") == "tests/fixtures for a.spec.ts"

    def test_snapshots(self):
        assert purpose_hint("/x/__snapshots__/a.snap", "add") == "tests/fixtures for a.snap"

    def test_sql_is_migration(self):
        assert purpose_hint("/db/schema.sql", "add") == "database schema/migration"

    def test_migration_path(self):
        assert purpose_hint("/db/migrations/0001.py", "add") == "database schema/migration"

    def test_no_false_positive_for_migration_substring(self):
        # 'immigration_policy.py' contains 'migration' as a substring but not as a component.
        assert purpose_hint("/src/immigration_policy.py", "edit") == "edits immigration_policy.py"

    def test_documentation(self):
        assert purpose_hint("/README.md", "edit") == "documentation"
        assert purpose_hint("/notes.rst", "edit") == "documentation"
        assert purpose_hint("/info.txt", "edit") == "documentation"

    def test_lockfile_by_extension(self):
        assert purpose_hint("/poetry.lock", "edit") == "dependency lockfile"

    def test_lockfile_by_name(self):
        assert purpose_hint("/package-lock.json", "edit") == "dependency lockfile"

    def test_configuration(self):
        assert purpose_hint("/config.yaml", "edit") == "configuration"

    def test_source_verbs(self):
        assert purpose_hint("/src/a.py", "add") == "adds a.py"
        assert purpose_hint("/src/a.py", "edit") == "edits a.py"
        assert purpose_hint("/src/a.py", "delete") == "deletes a.py"
        assert purpose_hint("/src/a.py", "rename") == "renames a.py"

    def test_no_false_positive_for_test_substring_in_filename(self):
        # 'latest_config.py' contains 'test' but is not a test file.
        assert purpose_hint("/src/latest_config.py", "edit") == "edits latest_config.py"

    def test_no_false_positive_for_spec_substring_in_filename(self):
        # 'specimen.py' contains 'spec' but is not a test file.
        assert purpose_hint("/src/specimen.py", "edit") == "edits specimen.py"

    def test_test_dir_component(self):
        # /test/ as a directory component (singular) is a test directory.
        assert purpose_hint("/test/helpers.py", "edit") == "tests/fixtures for helpers.py"

    def test_test_underscore_prefix_filename(self):
        # test_ prefix on the filename with no test directory.
        assert purpose_hint("/src/test_utils.py", "edit") == "tests/fixtures for test_utils.py"

    def test_suffix_test_filename(self):
        # *_test.py suffix pattern.
        assert purpose_hint("/src/utils_test.py", "edit") == "tests/fixtures for utils_test.py"
        # *-test.js suffix pattern.
        assert purpose_hint("/src/util-test.js", "edit") == "tests/fixtures for util-test.js"

    def test_steps_suffix_filename(self):
        # *.steps.ts (BDD step definitions) treated as test/fixture.
        assert purpose_hint("/features/login.steps.ts", "edit") == "tests/fixtures for login.steps.ts"
