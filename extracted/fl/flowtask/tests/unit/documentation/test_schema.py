"""Unit tests for SchemaGenerator."""
import pytest
import json
from flowtask.documentation.schema import SchemaGenerator
from flowtask.documentation.models import ComponentDoc, ComponentAttribute, ComponentSchema


@pytest.fixture
def generator():
    """Create a SchemaGenerator instance."""
    return SchemaGenerator()


@pytest.fixture
def sample_doc():
    """Sample ComponentDoc for testing."""
    return ComponentDoc(
        name="TestComponent",
        description="A test component for unit testing.",
        attributes=[
            ComponentAttribute(
                name="required_field",
                required=True,
                description="A required field"
            ),
            ComponentAttribute(
                name="optional_field",
                required=False,
                description="An optional field"
            ),
        ],
        examples=["TestComponent:\n  required_field: value"]
    )


@pytest.fixture
def doc_with_defaults():
    """ComponentDoc with default values."""
    return ComponentDoc(
        name="DefaultsComponent",
        description="Component with default values.",
        attributes=[
            ComponentAttribute(
                name="timeout",
                required=False,
                description="Timeout in seconds",
                default="30"
            ),
            ComponentAttribute(
                name="retries",
                required=False,
                description="Number of retries",
                default="3"
            ),
        ],
        examples=[]
    )


@pytest.fixture
def empty_doc():
    """ComponentDoc with no attributes."""
    return ComponentDoc(
        name="EmptyComponent",
        description="A component with no attributes.",
        attributes=[],
        examples=[]
    )


class TestSchemaGenerator:
    """Tests for SchemaGenerator class."""

    def test_generate_returns_schema(self, generator, sample_doc):
        """Generator returns ComponentSchema."""
        schema = generator.generate(sample_doc)
        assert isinstance(schema, ComponentSchema)
        assert schema.title == "TestComponent"
        assert schema.description == "A test component for unit testing."

    def test_required_fields_in_required_array(self, generator, sample_doc):
        """Required attributes appear in schema.required."""
        schema = generator.generate(sample_doc)
        assert "required_field" in schema.required
        assert "optional_field" not in schema.required

    def test_all_fields_have_properties(self, generator, sample_doc):
        """All attributes have corresponding properties."""
        schema = generator.generate(sample_doc)
        assert "required_field" in schema.properties
        assert "optional_field" in schema.properties

    def test_properties_have_descriptions(self, generator, sample_doc):
        """Properties include descriptions."""
        schema = generator.generate(sample_doc)
        assert schema.properties["required_field"]["description"] == "A required field"
        assert schema.properties["optional_field"]["description"] == "An optional field"

    def test_properties_have_type(self, generator, sample_doc):
        """Properties include type field."""
        schema = generator.generate(sample_doc)
        assert schema.properties["required_field"]["type"] == "string"
        assert schema.properties["optional_field"]["type"] == "string"

    def test_to_json_valid(self, generator, sample_doc):
        """Schema serializes to valid JSON."""
        schema = generator.generate(sample_doc)
        json_str = generator.to_json(schema)
        parsed = json.loads(json_str)
        assert parsed["title"] == "TestComponent"
        assert "properties" in parsed
        assert "$schema" in parsed

    def test_to_json_includes_schema_draft(self, generator, sample_doc):
        """JSON includes $schema field for draft-07."""
        schema = generator.generate(sample_doc)
        json_str = generator.to_json(schema)
        parsed = json.loads(json_str)
        assert parsed["$schema"] == "http://json-schema.org/draft-07/schema#"

    def test_to_json_required_only_when_present(self, generator, empty_doc):
        """JSON omits required array when no required fields."""
        schema = generator.generate(empty_doc)
        json_str = generator.to_json(schema)
        parsed = json.loads(json_str)
        assert "required" not in parsed

    def test_properties_include_defaults(self, generator, doc_with_defaults):
        """Properties include default values when specified."""
        schema = generator.generate(doc_with_defaults)
        assert schema.properties["timeout"]["default"] == "30"
        assert schema.properties["retries"]["default"] == "3"

    def test_to_dict_returns_dict(self, generator, sample_doc):
        """to_dict returns a dictionary."""
        schema = generator.generate(sample_doc)
        result = generator.to_dict(schema)
        assert isinstance(result, dict)
        assert result["title"] == "TestComponent"
        assert "properties" in result

    def test_empty_attributes_produces_empty_properties(self, generator, empty_doc):
        """Empty attributes list produces empty properties."""
        schema = generator.generate(empty_doc)
        assert schema.properties == {}
        assert schema.required == []

    def test_schema_type_is_object(self, generator, sample_doc):
        """Schema type is always 'object'."""
        schema = generator.generate(sample_doc)
        assert schema.type == "object"

    def test_json_is_properly_formatted(self, generator, sample_doc):
        """JSON output is properly indented."""
        schema = generator.generate(sample_doc)
        json_str = generator.to_json(schema)
        # Should have newlines (indented)
        assert "\n" in json_str
        # Should be parseable
        parsed = json.loads(json_str)
        assert parsed is not None


class TestSchemaGeneratorIntegration:
    """Integration tests for SchemaGenerator with DocstringParser."""

    def test_parse_and_generate(self, generator):
        """Full pipeline: docstring -> parse -> schema."""
        from flowtask.documentation.parser import DocstringParser

        docstring = '''
        IntegrationTest

        A component for testing the full pipeline.

        :widths: auto

        | input_file  | Yes | Path to input file  |
        | output_file | Yes | Path to output file |
        | verbose     | No  | Enable verbose mode |

        Example:

        ```yaml
        IntegrationTest:
          input_file: /data/input.csv
          output_file: /data/output.csv
        ```
        '''

        parser = DocstringParser()
        doc = parser.parse(docstring)
        assert doc is not None

        schema = generator.generate(doc)
        assert schema.title == "IntegrationTest"
        assert len(schema.properties) == 3
        assert len(schema.required) == 2
        assert "input_file" in schema.required
        assert "output_file" in schema.required
        assert "verbose" not in schema.required

    def test_real_component_schema(self, generator):
        """Generate schema for a real component."""
        from flowtask.documentation.parser import DocstringParser

        try:
            from flowtask.components.DownloadFrom import DownloadFromBase
            docstring = DownloadFromBase.__doc__
        except ImportError:
            pytest.skip("DownloadFromBase not available")

        parser = DocstringParser()
        doc = parser.parse(docstring)

        if doc is None:
            pytest.skip("Could not parse component docstring")

        schema = generator.generate(doc)
        assert schema.title == "DownloadFromBase"
        assert len(schema.properties) > 0

        # Verify JSON is valid
        json_str = generator.to_json(schema)
        parsed = json.loads(json_str)
        assert parsed["title"] == "DownloadFromBase"
