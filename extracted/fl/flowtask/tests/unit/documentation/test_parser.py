"""Unit tests for DocstringParser."""
import pytest
from flowtask.documentation.parser import DocstringParser
from flowtask.documentation.models import ComponentDoc, ComponentAttribute


@pytest.fixture
def parser():
    """Create a DocstringParser instance."""
    return DocstringParser()


@pytest.fixture
def sample_docstring():
    """Sample docstring in the Flowtask component format."""
    return '''
    DownloadFromBase

    Abstract base class for downloading files from various sources.

    This class utilizes aiohttp for asynchronous HTTP requests.

    :widths: auto

    | credentials | Yes | Dictionary containing username and password |
    | overwrite   | No  | Boolean flag to overwrite existing files    |
    | ssl         | No  | Boolean flag for SSL connection             |

    Example:

    ```yaml
    DownloadFrom:
      credentials:
        username: user
        password: pass
      overwrite: true
    ```
    '''


@pytest.fixture
def multiline_docstring():
    """Docstring with multi-line attribute descriptions."""
    return '''
    TestComponent

    A test component with multi-line descriptions.

    :widths: auto

        | credentials          |    Yes   | Dictionary containing expected username and password for authentication             |
        |                      |          | (default: {"username": str, "password": str}).                                      |
        | timeout              |    No    | Timeout value in seconds for HTTP requests (default: 30).                           |

    Example:

    ```yaml
    TestComponent:
      credentials:
        username: test
    ```
    '''


@pytest.fixture
def real_world_docstring():
    """Real-world docstring format from DownloadFromBase."""
    return '''
    DownloadFromBase

    Abstract base class for downloading files from various sources.

    Inherits from `FlowComponent` and `PandasDataframe` to provide common functionalities
    for component management and data handling.

    This class utilizes `aiohttp` for asynchronous HTTP requests and offers support
    for authentication, SSL connections, and basic file management.

    .. note::
    This class is intended to be subclassed for specific download implementations.

    :widths: auto

        | credentials          |    Yes   | Dictionary containing expected username and password for authentication             |
        |                      |          | (default: {"username": str, "password": str}).                                      |
        | no_host              |    No    | Boolean flag indicating whether to skip defining host and port (default: False).    |
        | overwrite            |    No    | Boolean flag indicating whether to overwrite existing files (default: True).        |
        | create_destination   |    No    | Boolean flag indicating whether to create the destination directory                 |
        |                      |          | if it doesn't exist (default: True).                                               |

    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          DownloadFromBase:
          # attributes here
        ```
    '''


class TestDocstringParser:
    """Tests for DocstringParser class."""

    def test_parse_returns_component_doc(self, parser, sample_docstring):
        """Parser returns ComponentDoc for valid docstring."""
        result = parser.parse(sample_docstring)
        assert isinstance(result, ComponentDoc)
        assert result.name == "DownloadFromBase"

    def test_parse_extracts_attributes(self, parser, sample_docstring):
        """Parser extracts all attributes from table."""
        result = parser.parse(sample_docstring)
        assert len(result.attributes) == 3
        assert result.attributes[0].name == "credentials"
        assert result.attributes[0].required is True
        assert result.attributes[1].name == "overwrite"
        assert result.attributes[1].required is False
        assert result.attributes[2].name == "ssl"
        assert result.attributes[2].required is False

    def test_parse_extracts_examples(self, parser, sample_docstring):
        """Parser extracts YAML examples."""
        result = parser.parse(sample_docstring)
        assert len(result.examples) == 1
        assert "DownloadFrom:" in result.examples[0]
        assert "credentials:" in result.examples[0]

    def test_parse_empty_docstring(self, parser):
        """Parser returns None for empty docstring."""
        assert parser.parse("") is None
        assert parser.parse(None) is None

    def test_parse_no_table_marker(self, parser):
        """Parser returns None for docstring without :widths: auto marker."""
        docstring = "Simple component description without table marker."
        result = parser.parse(docstring)
        assert result is None

    def test_parse_extracts_description(self, parser, sample_docstring):
        """Parser extracts description before table."""
        result = parser.parse(sample_docstring)
        assert "Abstract base class" in result.description
        assert "aiohttp" in result.description

    def test_parse_multiline_descriptions(self, parser, multiline_docstring):
        """Parser handles multi-line attribute descriptions."""
        result = parser.parse(multiline_docstring)
        assert len(result.attributes) == 2

        # First attribute should have merged description
        creds = result.attributes[0]
        assert creds.name == "credentials"
        assert creds.required is True
        assert "username" in creds.description
        assert "password" in creds.description

    def test_parse_real_world_docstring(self, parser, real_world_docstring):
        """Parser handles real-world component docstrings."""
        result = parser.parse(real_world_docstring)
        assert result is not None
        assert result.name == "DownloadFromBase"
        assert "Abstract base class" in result.description

        # Should extract attributes from the main table
        attr_names = [a.name for a in result.attributes]
        assert "credentials" in attr_names
        assert "no_host" in attr_names
        assert "overwrite" in attr_names
        assert "create_destination" in attr_names

    def test_parse_handles_variable_spacing(self, parser):
        """Parser handles variable spacing in table rows."""
        docstring = '''
        SpacingTest

        Test component.

        :widths: auto

        |   field1   |  Yes  |   Description with spaces   |
        |field2|No|Compact description|

        ```yaml
        SpacingTest:
          field1: value
        ```
        '''
        result = parser.parse(docstring)
        assert len(result.attributes) == 2
        assert result.attributes[0].name == "field1"
        assert result.attributes[1].name == "field2"

    def test_parse_skips_duplicate_attributes(self, parser):
        """Parser skips duplicate attribute names."""
        docstring = '''
        DuplicateTest

        Test component.

        :widths: auto

        | field1 | Yes | First description  |
        | field1 | No  | Duplicate entry    |
        | field2 | No  | Another field      |

        ```yaml
        DuplicateTest:
          field1: value
        ```
        '''
        result = parser.parse(docstring)
        # Should only have 2 attributes (field1 once, field2 once)
        assert len(result.attributes) == 2
        names = [a.name for a in result.attributes]
        assert names.count("field1") == 1

    def test_parse_extracts_multiple_examples(self, parser):
        """Parser extracts multiple example blocks."""
        docstring = '''
        MultiExample

        Test component with multiple examples.

        :widths: auto

        | field1 | Yes | A field |

        Example 1:

        ```yaml
        MultiExample:
          field1: value1
        ```

        Example 2:

        ```json
        {"MultiExample": {"field1": "value2"}}
        ```
        '''
        result = parser.parse(docstring)
        assert len(result.examples) == 2

    def test_attribute_has_correct_fields(self, parser, sample_docstring):
        """ComponentAttribute has all expected fields."""
        result = parser.parse(sample_docstring)
        attr = result.attributes[0]

        assert hasattr(attr, 'name')
        assert hasattr(attr, 'required')
        assert hasattr(attr, 'description')
        assert hasattr(attr, 'default')

    def test_parse_preserves_example_formatting(self, parser, sample_docstring):
        """Parser preserves YAML formatting in examples."""
        result = parser.parse(sample_docstring)
        example = result.examples[0]

        # Should preserve indentation structure
        assert "username:" in example
        assert "password:" in example

    def test_parse_stops_at_non_table_content(self, parser):
        """Parser stops parsing table at non-table content."""
        docstring = '''
        StopTest

        Test component.

        :widths: auto

        | field1 | Yes | Description |

        Some random text here that is not a table.

        | field2 | No | Should not be parsed |

        ```yaml
        StopTest:
          field1: value
        ```
        '''
        result = parser.parse(docstring)
        # Should only get field1, not field2
        assert len(result.attributes) == 1
        assert result.attributes[0].name == "field1"


class TestComponentAttribute:
    """Tests for ComponentAttribute model."""

    def test_create_attribute(self):
        """Can create ComponentAttribute with required fields."""
        attr = ComponentAttribute(
            name="test_field",
            required=True,
            description="A test field"
        )
        assert attr.name == "test_field"
        assert attr.required is True
        assert attr.description == "A test field"
        assert attr.default is None

    def test_attribute_with_default(self):
        """ComponentAttribute can have a default value."""
        attr = ComponentAttribute(
            name="timeout",
            required=False,
            description="Timeout in seconds",
            default="30"
        )
        assert attr.default == "30"


class TestComponentDoc:
    """Tests for ComponentDoc model."""

    def test_create_empty_doc(self):
        """Can create ComponentDoc with minimal fields."""
        doc = ComponentDoc()
        assert doc.name == ""
        assert doc.description == ""
        assert doc.attributes == []
        assert doc.examples == []

    def test_create_full_doc(self):
        """Can create ComponentDoc with all fields."""
        doc = ComponentDoc(
            name="TestComponent",
            version="1.0.0",
            description="A test component",
            attributes=[
                ComponentAttribute(name="field1", required=True, description="Field 1")
            ],
            examples=["TestComponent:\n  field1: value"]
        )
        assert doc.name == "TestComponent"
        assert doc.version == "1.0.0"
        assert len(doc.attributes) == 1
        assert len(doc.examples) == 1
