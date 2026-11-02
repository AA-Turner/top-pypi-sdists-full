"""Tests for load_schema() function."""

import agentic_devtools.epic_tree.schema as schema_module
from agentic_devtools.epic_tree.schema import load_schema


class TestLoadSchema:
    """Tests for the load_schema function."""

    def setup_method(self):
        """Reset the cached schema before each test."""
        schema_module._cached_schema = None

    def teardown_method(self):
        """Reset the cached schema after each test."""
        schema_module._cached_schema = None

    def test_returns_dict(self):
        """load_schema returns a dictionary."""
        schema = load_schema()
        assert isinstance(schema, dict)

    def test_has_schema_key(self):
        """Loaded schema contains $schema key for Draft 2019-09."""
        schema = load_schema()
        assert "$schema" in schema
        assert "2019-09" in schema["$schema"]

    def test_has_required_top_level_properties(self):
        """Loaded schema defines required top-level properties."""
        schema = load_schema()
        assert "properties" in schema
        assert "schemaVersion" in schema["properties"]
        assert "epic" in schema["properties"]

    def test_caches_result(self):
        """Subsequent calls return the same object (cached)."""
        schema1 = load_schema()
        schema2 = load_schema()
        assert schema1 is schema2

    def test_defines_three_levels(self):
        """Schema defines feature and subtask definitions."""
        schema = load_schema()
        assert "$defs" in schema
        assert "feature" in schema["$defs"]
        assert "subtask" in schema["$defs"]
