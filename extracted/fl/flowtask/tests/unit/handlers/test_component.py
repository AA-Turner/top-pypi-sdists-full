"""Unit tests for FlowtaskComponentHandler."""
import pytest
from unittest.mock import MagicMock
import orjson


class TestFlowtaskComponentHandler:
    """Tests for the FlowtaskComponentHandler class."""

    @pytest.fixture
    def mock_docs_dir(self, tmp_path):
        """Create mock documentation directory with test data."""
        docs = tmp_path / "documentation"
        docs.mkdir()
        components = docs / "components"
        components.mkdir()

        # Create index
        index = {
            "updated_at": "2026-03-03T12:00:00",
            "components": {
                "TestComponent": {
                    "schema": "components/TestComponent.schema.json",
                    "doc": "components/TestComponent.doc.json",
                    "category": "data",
                    "tags": ["transform", "pandas"]
                },
                "AnotherComponent": {
                    "schema": "components/AnotherComponent.schema.json",
                    "doc": "components/AnotherComponent.doc.json",
                    "category": "io",
                    "tags": ["file", "read"]
                }
            }
        }
        (docs / "index.json").write_bytes(orjson.dumps(index))

        # Create TestComponent files
        schema = {
            "title": "TestComponent",
            "type": "object",
            "properties": {
                "field1": {"type": "string", "description": "A test field"},
                "field2": {"type": "integer", "description": "Another field"}
            },
            "required": ["field1"]
        }
        doc = {
            "description": "Test component description",
            "examples": ["TestComponent:\n  field1: value", "TestComponent:\n  field1: other\n  field2: 42"]
        }
        (components / "TestComponent.schema.json").write_bytes(orjson.dumps(schema))
        (components / "TestComponent.doc.json").write_bytes(orjson.dumps(doc))

        # Create AnotherComponent files
        schema2 = {
            "title": "AnotherComponent",
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"]
        }
        doc2 = {
            "description": "Another component description",
            "examples": ["AnotherComponent:\n  path: /tmp/file.txt"]
        }
        (components / "AnotherComponent.schema.json").write_bytes(orjson.dumps(schema2))
        (components / "AnotherComponent.doc.json").write_bytes(orjson.dumps(doc2))

        return docs

    @pytest.fixture
    def handler_class(self):
        """Return the handler class for testing."""
        from flowtask.handlers.component import FlowtaskComponentHandler
        return FlowtaskComponentHandler

    @pytest.fixture
    def mock_handler(self, handler_class, mock_docs_dir):
        """Create a mock handler instance with mocked docs_dir."""
        handler = MagicMock(spec=handler_class)
        handler.docs_dir = mock_docs_dir
        handler.logger = MagicMock()
        handler.DEFAULT_CATEGORY = handler_class.DEFAULT_CATEGORY

        # Bind the actual methods to use with our mock
        handler._load_index = lambda: handler_class._load_index(handler)
        handler._load_component_doc = lambda name: handler_class._load_component_doc(handler, name)
        handler._read_description = lambda doc_rel_path: handler_class._read_description(handler, doc_rel_path)
        handler._component_entry = lambda name, info: handler_class._component_entry(handler, name, info)
        handler._filter_components = lambda c, category=None, tag=None: handler_class._filter_components(
            handler, c, category, tag
        )
        handler._group_by_category = lambda entries: handler_class._group_by_category(handler, entries)

        return handler

    def test_load_index_returns_components(self, mock_handler):
        """_load_index returns the index with components."""
        index = mock_handler._load_index()

        assert "components" in index
        assert "TestComponent" in index["components"]
        assert "AnotherComponent" in index["components"]

    def test_load_index_missing_file_returns_empty(self, handler_class, tmp_path):
        """_load_index returns empty structure when index.json is missing."""
        handler = MagicMock(spec=handler_class)
        handler.docs_dir = tmp_path / "nonexistent"
        handler.logger = MagicMock()
        handler._load_index = lambda: handler_class._load_index(handler)

        index = handler._load_index()

        assert index == {"components": {}}

    def test_load_component_doc_returns_formatted_response(self, mock_handler):
        """_load_component_doc returns schema, doc, and example."""
        doc = mock_handler._load_component_doc("TestComponent")

        assert doc is not None
        assert "schema" in doc
        assert "doc" in doc
        assert "example" in doc

        # Verify schema is a JSON string
        schema = orjson.loads(doc["schema"])
        assert schema["title"] == "TestComponent"

        # Verify doc content
        assert doc["doc"] == "Test component description"

        # Verify examples are joined with newlines
        assert "TestComponent:\n  field1: value" in doc["example"]
        assert "TestComponent:\n  field1: other" in doc["example"]

    def test_load_component_doc_unknown_returns_none(self, mock_handler):
        """_load_component_doc returns None for unknown component."""
        doc = mock_handler._load_component_doc("NonExistentComponent")

        assert doc is None

    def test_load_component_doc_missing_files_returns_none(self, handler_class, tmp_path):
        """_load_component_doc returns None when schema/doc files are missing."""
        docs = tmp_path / "docs"
        docs.mkdir()

        # Create index referencing non-existent files
        index = {
            "components": {
                "MissingFiles": {
                    "schema": "components/MissingFiles.schema.json",
                    "doc": "components/MissingFiles.doc.json"
                }
            }
        }
        (docs / "index.json").write_bytes(orjson.dumps(index))

        handler = MagicMock(spec=handler_class)
        handler.docs_dir = docs
        handler.logger = MagicMock()
        handler._load_index = lambda: handler_class._load_index(handler)
        handler._load_component_doc = lambda name: handler_class._load_component_doc(handler, name)

        doc = handler._load_component_doc("MissingFiles")

        assert doc is None

    def test_filter_components_no_filter_returns_all(self, mock_handler):
        """_filter_components with no filters returns all components."""
        index = mock_handler._load_index()
        components = index["components"]

        result = mock_handler._filter_components(components)

        assert len(result) == 2
        for entry in result:
            assert set(entry.keys()) == {"name", "description", "category"}
        by_name = {c["name"]: c for c in result}
        assert by_name["TestComponent"]["description"] == "Test component description"
        assert by_name["TestComponent"]["category"] == "data"
        assert by_name["AnotherComponent"]["description"] == "Another component description"
        assert by_name["AnotherComponent"]["category"] == "io"

    def test_filter_components_by_category(self, mock_handler):
        """_filter_components filters by category."""
        index = mock_handler._load_index()
        components = index["components"]

        result = mock_handler._filter_components(components, category="data")

        assert len(result) == 1
        assert result[0]["name"] == "TestComponent"
        assert result[0]["description"] == "Test component description"
        assert result[0]["category"] == "data"

    def test_filter_components_by_tag(self, mock_handler):
        """_filter_components filters by tag."""
        index = mock_handler._load_index()
        components = index["components"]

        result = mock_handler._filter_components(components, tag="file")

        assert len(result) == 1
        assert result[0]["name"] == "AnotherComponent"
        assert result[0]["description"] == "Another component description"
        assert result[0]["category"] == "io"

    def test_filter_components_case_insensitive(self, mock_handler):
        """_filter_components performs case-insensitive filtering."""
        index = mock_handler._load_index()
        components = index["components"]

        result = mock_handler._filter_components(components, category="DATA")

        assert len(result) == 1
        assert result[0]["name"] == "TestComponent"

    def test_component_entry_uses_default_category(self, mock_handler):
        """_component_entry falls back to DEFAULT_CATEGORY when missing."""
        info = {"doc": "components/TestComponent.doc.json"}

        entry = mock_handler._component_entry("TestComponent", info)

        assert entry["category"] == "Other"

    def test_component_entry_reads_description_from_doc_when_absent(self, mock_handler):
        """_component_entry reads description from doc file if not in index."""
        info = {"doc": "components/TestComponent.doc.json", "category": "data"}

        entry = mock_handler._component_entry("TestComponent", info)

        assert entry["description"] == "Test component description"

    def test_group_by_category(self, mock_handler):
        """_group_by_category buckets entries and sorts categories."""
        entries = [
            {"name": "B", "description": "", "category": "Sources"},
            {"name": "A", "description": "", "category": "Outputs"},
            {"name": "C", "description": "", "category": "Sources"},
        ]

        groups = mock_handler._group_by_category(entries)

        assert [g["category"] for g in groups] == ["Outputs", "Sources"]
        assert [c["name"] for c in groups[0]["components"]] == ["A"]
        assert [c["name"] for c in groups[1]["components"]] == ["B", "C"]

    def test_filter_components_no_matches_returns_empty(self, mock_handler):
        """_filter_components returns empty list when no matches."""
        index = mock_handler._load_index()
        components = index["components"]

        result = mock_handler._filter_components(components, category="nonexistent")

        assert result == []

    def test_missing_docs_directory_returns_empty_list(self, handler_class, tmp_path):
        """Handler returns empty list when docs directory doesn't exist."""
        handler = MagicMock(spec=handler_class)
        handler.docs_dir = tmp_path / "missing_docs"
        handler.logger = MagicMock()
        handler._load_index = lambda: handler_class._load_index(handler)

        index = handler._load_index()

        assert index == {"components": {}}


class TestFlowtaskComponentHandlerIntegration:
    """Integration-style tests for the handler with aiohttp context."""

    @pytest.fixture
    def mock_docs_dir(self, tmp_path):
        """Create mock documentation directory."""
        docs = tmp_path / "documentation"
        docs.mkdir()
        components = docs / "components"
        components.mkdir()

        index = {
            "updated_at": "2026-03-03T12:00:00",
            "components": {
                "TestComponent": {
                    "schema": "components/TestComponent.schema.json",
                    "doc": "components/TestComponent.doc.json"
                }
            }
        }
        (docs / "index.json").write_bytes(orjson.dumps(index))

        schema = {"title": "TestComponent", "properties": {}}
        doc = {"description": "Test description", "examples": ["TestComponent:\n  key: value"]}
        (components / "TestComponent.schema.json").write_bytes(orjson.dumps(schema))
        (components / "TestComponent.doc.json").write_bytes(orjson.dumps(doc))

        return docs

    @pytest.mark.asyncio
    async def test_get_list_components(self, mock_docs_dir):
        """GET request without component_name returns list of components."""
        from flowtask.handlers.component import FlowtaskComponentHandler

        # Mock the handler's dependencies
        mock_request = MagicMock()
        mock_request.query = {}

        handler = MagicMock(spec=FlowtaskComponentHandler)
        handler.docs_dir = mock_docs_dir
        handler.logger = MagicMock()
        handler.request = mock_request
        handler.DEFAULT_CATEGORY = FlowtaskComponentHandler.DEFAULT_CATEGORY

        # Setup match_parameters to return empty (list mode)
        handler.match_parameters = MagicMock(return_value={})

        # Bind actual methods
        handler._load_index = lambda: FlowtaskComponentHandler._load_index(handler)
        handler._read_description = lambda doc_rel_path: FlowtaskComponentHandler._read_description(handler, doc_rel_path)
        handler._component_entry = lambda name, info: FlowtaskComponentHandler._component_entry(handler, name, info)
        handler._filter_components = lambda c, category=None, tag=None: FlowtaskComponentHandler._filter_components(
            handler, c, category, tag
        )

        # Capture json_response call
        response_data = None

        def capture_json_response(data):
            nonlocal response_data
            response_data = data
            return MagicMock()

        handler.json_response = capture_json_response

        # Call the get method logic (simplified)
        params = handler.match_parameters()
        component_name = params.get("component_name")

        if not component_name:
            index = handler._load_index()
            components = index.get("components", {})
            query = handler.request.query
            filtered = handler._filter_components(
                components,
                category=query.get("category"),
                tag=query.get("tag")
            )
            handler.json_response({"components": filtered, "count": len(filtered)})

        assert response_data is not None
        assert "components" in response_data
        assert response_data["count"] == 1
        entry = response_data["components"][0]
        assert entry["name"] == "TestComponent"
        assert entry["description"] == "Test description"
        assert entry["category"] == "Other"

    @pytest.mark.asyncio
    async def test_get_specific_component(self, mock_docs_dir):
        """GET request with component_name returns component documentation."""
        from flowtask.handlers.component import FlowtaskComponentHandler

        handler = MagicMock(spec=FlowtaskComponentHandler)
        handler.docs_dir = mock_docs_dir
        handler.logger = MagicMock()

        # Setup match_parameters to return a component name
        handler.match_parameters = MagicMock(return_value={"component_name": "TestComponent"})

        # Bind actual methods
        handler._load_index = lambda: FlowtaskComponentHandler._load_index(handler)
        handler._load_component_doc = lambda name: FlowtaskComponentHandler._load_component_doc(handler, name)

        # Capture json_response call
        response_data = None

        def capture_json_response(data):
            nonlocal response_data
            response_data = data
            return MagicMock()

        handler.json_response = capture_json_response

        # Call the get method logic (simplified)
        params = handler.match_parameters()
        component_name = params.get("component_name")

        if component_name:
            doc = handler._load_component_doc(component_name)
            if doc:
                handler.json_response(doc)

        assert response_data is not None
        assert "schema" in response_data
        assert "doc" in response_data
        assert "example" in response_data
        assert response_data["doc"] == "Test description"

    @pytest.mark.asyncio
    async def test_get_unknown_component_returns_404(self, mock_docs_dir):
        """GET request for unknown component returns 404."""
        from flowtask.handlers.component import FlowtaskComponentHandler

        handler = MagicMock(spec=FlowtaskComponentHandler)
        handler.docs_dir = mock_docs_dir
        handler.logger = MagicMock()

        # Setup match_parameters to return unknown component
        handler.match_parameters = MagicMock(return_value={"component_name": "UnknownComponent"})

        # Bind actual methods
        handler._load_index = lambda: FlowtaskComponentHandler._load_index(handler)
        handler._load_component_doc = lambda name: FlowtaskComponentHandler._load_component_doc(handler, name)

        # Capture error call
        error_called = False
        error_status = None

        def capture_error(response, status):
            nonlocal error_called, error_status
            error_called = True
            error_status = status
            return MagicMock()

        handler.error = capture_error

        # Call the get method logic (simplified)
        params = handler.match_parameters()
        component_name = params.get("component_name")

        if component_name:
            doc = handler._load_component_doc(component_name)
            if doc is None:
                handler.error(
                    response={"error": f"Component '{component_name}' not found"},
                    status=404
                )

        assert error_called
        assert error_status == 404
