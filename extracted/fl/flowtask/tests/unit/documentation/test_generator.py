"""Unit tests for ComponentDocGenerator."""
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from flowtask.documentation.generator import ComponentDocGenerator
from flowtask.documentation.models import DocumentationIndex, ComponentDoc


@pytest.fixture
def tmp_output_dir(tmp_path):
    """Create temporary output directory."""
    return tmp_path / "documentation"


@pytest.fixture
def generator(tmp_output_dir):
    """Create a ComponentDocGenerator instance."""
    return ComponentDocGenerator(output_dir=tmp_output_dir)


@pytest.fixture
def mock_component_source():
    """Source code for a mock component."""
    return '''
from flowtask.components.flow import FlowComponent

class MockTestComponent(FlowComponent):
    """
    MockTestComponent

    A mock component for testing documentation generation.

    :widths: auto

    | input_path  | Yes | Path to input file  |
    | output_path | Yes | Path to output file |
    | verbose     | No  | Enable verbose mode |

    Example:

    ```yaml
    MockTestComponent:
      input_path: /data/input.csv
      output_path: /data/output.csv
    ```
    """
    _version = "1.0.0"
    pass


class NonDocumentedComponent(FlowComponent):
    """A component without the :widths: auto marker."""
    pass
'''


@pytest.fixture
def mock_component_dir(tmp_path, mock_component_source):
    """Create a mock components directory with test component."""
    comp_dir = tmp_path / "mock_components"
    comp_dir.mkdir()
    (comp_dir / "__init__.py").write_text("")
    (comp_dir / "MockComp.py").write_text(mock_component_source)
    return comp_dir


class TestComponentDocGenerator:
    """Tests for ComponentDocGenerator class."""

    def test_init(self, generator, tmp_output_dir):
        """Generator initializes with output directory."""
        assert generator.output_dir == tmp_output_dir
        assert generator.parser is not None
        assert generator.schema_gen is not None

    def test_generate_creates_output_dir(self, generator, tmp_output_dir):
        """Generator creates output directory if not exists."""
        generator.generate([])
        assert tmp_output_dir.exists()

    def test_generate_creates_components_dir(self, generator, tmp_output_dir):
        """Generator creates components subdirectory."""
        generator.generate([])
        assert (tmp_output_dir / "components").exists()

    def test_generate_creates_index(self, generator, tmp_output_dir):
        """Generator creates index.json."""
        generator.generate([])
        assert (tmp_output_dir / "index.json").exists()

    def test_generate_returns_documentation_index(self, generator):
        """Generator returns DocumentationIndex object."""
        result = generator.generate([])
        assert isinstance(result, DocumentationIndex)

    def test_index_has_updated_at(self, generator):
        """Index contains updated_at timestamp."""
        index = generator.generate([])
        assert index.updated_at is not None

    def test_index_has_components_dict(self, generator):
        """Index contains components dictionary."""
        index = generator.generate([])
        assert isinstance(index.components, dict)

    def test_missing_dir_no_error(self, generator):
        """Missing scan directory doesn't raise error."""
        nonexistent = Path("/nonexistent/path/that/does/not/exist")
        result = generator.scan_components([nonexistent])
        assert result == []

    def test_index_json_valid(self, generator, tmp_output_dir):
        """Generated index.json is valid JSON."""
        generator.generate([])
        index_path = tmp_output_dir / "index.json"
        content = index_path.read_text()
        parsed = json.loads(content)
        assert "updated_at" in parsed
        assert "components" in parsed

    def test_is_documentable_with_marker(self, generator):
        """_is_documentable returns True for class with marker."""
        class MockClass:
            __doc__ = "Test\n\n:widths: auto\n\n| field | Yes | desc |"
        assert generator._is_documentable(MockClass) is True

    def test_is_documentable_without_marker(self, generator):
        """_is_documentable returns False for class without marker."""
        class MockClass:
            __doc__ = "Test without the marker"
        assert generator._is_documentable(MockClass) is False

    def test_is_documentable_no_docstring(self, generator):
        """_is_documentable returns False for class without docstring."""
        class MockClass:
            pass
        assert generator._is_documentable(MockClass) is False


class TestGeneratorWithRealComponents:
    """Integration tests with real Flowtask components."""

    def test_scan_real_components_dir(self, generator):
        """Scanner finds components in real flowtask/components directory."""
        from pathlib import Path
        components_path = Path("flowtask/components")

        if not components_path.exists():
            pytest.skip("flowtask/components directory not found")

        components = generator.scan_components([components_path])
        # Should find at least some components
        assert len(components) > 0

    def test_generate_real_components(self, tmp_output_dir):
        """Generate documentation for real components."""
        from pathlib import Path
        components_path = Path("flowtask/components")

        if not components_path.exists():
            pytest.skip("flowtask/components directory not found")

        generator = ComponentDocGenerator(output_dir=tmp_output_dir)
        index = generator.generate([components_path])

        # Should generate docs for at least some components
        assert len(index.components) > 0

        # Check that files were created
        for name, paths in index.components.items():
            schema_path = tmp_output_dir / paths["schema"]
            doc_path = tmp_output_dir / paths["doc"]
            assert schema_path.exists(), f"Schema file not found for {name}"
            assert doc_path.exists(), f"Doc file not found for {name}"

    def test_generated_schema_is_valid(self, tmp_output_dir):
        """Generated schema files are valid JSON."""
        from pathlib import Path
        components_path = Path("flowtask/components")

        if not components_path.exists():
            pytest.skip("flowtask/components directory not found")

        generator = ComponentDocGenerator(output_dir=tmp_output_dir)
        index = generator.generate([components_path])

        if not index.components:
            pytest.skip("No components were documented")

        # Check first component
        first_name = list(index.components.keys())[0]
        schema_path = tmp_output_dir / index.components[first_name]["schema"]

        content = schema_path.read_text()
        parsed = json.loads(content)

        assert "title" in parsed
        assert "properties" in parsed
        assert parsed["type"] == "object"

    def test_generated_doc_is_valid(self, tmp_output_dir):
        """Generated doc files are valid JSON."""
        from pathlib import Path
        components_path = Path("flowtask/components")

        if not components_path.exists():
            pytest.skip("flowtask/components directory not found")

        generator = ComponentDocGenerator(output_dir=tmp_output_dir)
        index = generator.generate([components_path])

        if not index.components:
            pytest.skip("No components were documented")

        # Check first component
        first_name = list(index.components.keys())[0]
        doc_path = tmp_output_dir / index.components[first_name]["doc"]

        content = doc_path.read_text()
        parsed = json.loads(content)

        assert "name" in parsed
        assert "description" in parsed
        assert "attributes" in parsed


class TestGenerateSingle:
    """Tests for generate_single method."""

    def test_generate_single_documented_class(self, generator):
        """generate_single returns ComponentDoc for documented class."""
        # Create a mock class with documentation
        class MockComponent:
            __doc__ = """
            MockComponent

            A test component.

            :widths: auto

            | field1 | Yes | Required field |
            | field2 | No  | Optional field |

            ```yaml
            MockComponent:
              field1: value
            ```
            """
            _version = "2.0.0"

        # Mock _is_documentable to return True
        with patch.object(generator, '_is_documentable', return_value=True):
            result = generator.generate_single(MockComponent)

        assert result is not None
        assert isinstance(result, ComponentDoc)
        assert result.name == "MockComponent"
        assert result.version == "2.0.0"

    def test_generate_single_undocumented_class(self, generator):
        """generate_single returns None for undocumented class."""
        class UndocumentedClass:
            __doc__ = "No marker here"

        result = generator.generate_single(UndocumentedClass)
        assert result is None


class TestFileOperations:
    """Tests for file writing operations."""

    def test_write_json_creates_file(self, generator, tmp_output_dir):
        """_write_json creates a valid JSON file."""
        tmp_output_dir.mkdir(parents=True, exist_ok=True)
        test_path = tmp_output_dir / "test.json"
        test_data = {"key": "value", "number": 42}

        generator._write_json(test_path, test_data)

        assert test_path.exists()
        content = json.loads(test_path.read_text())
        assert content == test_data

    def test_write_json_formats_output(self, generator, tmp_output_dir):
        """_write_json formats JSON with indentation."""
        tmp_output_dir.mkdir(parents=True, exist_ok=True)
        test_path = tmp_output_dir / "test.json"
        test_data = {"key": "value"}

        generator._write_json(test_path, test_data)

        content = test_path.read_text()
        # Should have newlines (indented)
        assert "\n" in content


class TestModulePath:
    """Tests for module path resolution."""

    def test_file_to_module_flowtask(self, generator):
        """_file_to_module handles flowtask paths."""
        path = Path("flowtask/components/DownloadFrom.py")
        result = generator._file_to_module(path)
        assert result == "flowtask.components.DownloadFrom"

    def test_file_to_module_plugins(self, generator):
        """_file_to_module handles plugins paths."""
        path = Path("plugins/components/CustomComp.py")
        result = generator._file_to_module(path)
        assert result == "plugins.components.CustomComp"

    def test_file_to_module_unknown(self, generator):
        """_file_to_module returns None for unknown paths."""
        path = Path("unknown/path/module.py")
        result = generator._file_to_module(path)
        assert result is None
