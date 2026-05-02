"""Comprehensive tests for sage/core/unified_classifier.py - Request Classification."""

import pytest

from sage.core.unified_classifier import (
    # Enums
    RequestType,
    OutputFormat,
    Pipeline,
    Complexity,
    # Dataclasses
    QuantityResult,
    ClassificationResult,
    # Classes
    UnifiedQuantityParser,
    UnifiedRequestClassifier,
    # Convenience functions
    classify_request,
    parse_quantity,
    is_read_only_request,
    get_required_quantity,
)


# =============================================================================
# Tests for RequestType Enum
# =============================================================================


class TestRequestType:
    """Tests for RequestType enum."""

    def test_analysis(self):
        """ANALYSIS is defined."""
        assert RequestType.ANALYSIS is not None

    def test_list_generation(self):
        """LIST_GENERATION is defined."""
        assert RequestType.LIST_GENERATION is not None

    def test_implementation(self):
        """IMPLEMENTATION is defined."""
        assert RequestType.IMPLEMENTATION is not None

    def test_refactoring(self):
        """REFACTORING is defined."""
        assert RequestType.REFACTORING is not None

    def test_debugging(self):
        """DEBUGGING is defined."""
        assert RequestType.DEBUGGING is not None

    def test_documentation(self):
        """DOCUMENTATION is defined."""
        assert RequestType.DOCUMENTATION is not None

    def test_testing(self):
        """TESTING is defined."""
        assert RequestType.TESTING is not None


# =============================================================================
# Tests for OutputFormat Enum
# =============================================================================


class TestOutputFormat:
    """Tests for OutputFormat enum."""

    def test_plain_text(self):
        """PLAIN_TEXT is defined."""
        assert OutputFormat.PLAIN_TEXT is not None

    def test_numbered_list(self):
        """NUMBERED_LIST is defined."""
        assert OutputFormat.NUMBERED_LIST is not None

    def test_table(self):
        """TABLE is defined."""
        assert OutputFormat.TABLE is not None

    def test_json(self):
        """JSON is defined."""
        assert OutputFormat.JSON is not None


# =============================================================================
# Tests for Pipeline Enum
# =============================================================================


class TestPipeline:
    """Tests for Pipeline enum."""

    def test_analysis_only(self):
        """ANALYSIS_ONLY is defined."""
        assert Pipeline.ANALYSIS_ONLY is not None

    def test_list_generation(self):
        """LIST_GENERATION is defined."""
        assert Pipeline.LIST_GENERATION is not None


# =============================================================================
# Tests for Complexity Enum
# =============================================================================


class TestComplexity:
    """Tests for Complexity enum."""

    def test_trivial(self):
        """TRIVIAL has value 1."""
        assert Complexity.TRIVIAL.value == 1

    def test_simple(self):
        """SIMPLE has value 2."""
        assert Complexity.SIMPLE.value == 2

    def test_moderate(self):
        """MODERATE has value 3."""
        assert Complexity.MODERATE.value == 3

    def test_complex(self):
        """COMPLEX has value 4."""
        assert Complexity.COMPLEX.value == 4

    def test_expert(self):
        """EXPERT has value 5."""
        assert Complexity.EXPERT.value == 5


# =============================================================================
# Tests for QuantityResult Dataclass
# =============================================================================


class TestQuantityResult:
    """Tests for QuantityResult dataclass."""

    def test_create_default(self):
        """Create with defaults."""
        result = QuantityResult()
        assert result.quantity is None
        assert result.modifier is None

    def test_is_exact_no_modifier(self):
        """is_exact True without modifier."""
        result = QuantityResult(quantity=50)
        assert result.is_exact is True

    def test_is_exact_with_modifier(self):
        """is_exact False with modifier."""
        result = QuantityResult(quantity=50, modifier="over")
        assert result.is_exact is False

    def test_minimum_required_no_quantity(self):
        """minimum_required is 0 without quantity."""
        result = QuantityResult()
        assert result.minimum_required == 0

    def test_minimum_required_exact(self):
        """minimum_required equals quantity for exact."""
        result = QuantityResult(quantity=100)
        assert result.minimum_required == 100


# =============================================================================
# Tests for ClassificationResult Dataclass
# =============================================================================


class TestClassificationResult:
    """Tests for ClassificationResult dataclass."""

    def test_create_minimal(self):
        """Create with required fields."""
        result = ClassificationResult(original_request="Test request")
        assert result.original_request == "Test request"
        assert result.request_type == RequestType.QUESTION

    def test_get_summary(self):
        """get_summary returns readable string."""
        result = ClassificationResult(
            original_request="Test",
            request_type=RequestType.ANALYSIS,
        )
        summary = result.get_summary()
        assert "ANALYSIS" in summary


# =============================================================================
# Tests for UnifiedQuantityParser
# =============================================================================


class TestUnifiedQuantityParser:
    """Tests for UnifiedQuantityParser class."""

    def test_init(self):
        """Initialize parser."""
        parser = UnifiedQuantityParser()
        assert parser is not None

    def test_parse_no_quantity(self):
        """Parse text with no quantity."""
        parser = UnifiedQuantityParser()
        result = parser.parse("Hello world")
        assert result.quantity is None

    def test_parse_numeric_with_context(self):
        """Parse '100 items'."""
        parser = UnifiedQuantityParser()
        result = parser.parse("Give me 100 items")
        assert result.quantity == 100

    def test_parse_modified_over(self):
        """Parse 'over 100'."""
        parser = UnifiedQuantityParser()
        result = parser.parse("Find over 100 bugs")
        assert result.quantity == 100
        assert result.modifier == "over"

    def test_parse_modified_at_least(self):
        """Parse 'at least 50'."""
        parser = UnifiedQuantityParser()
        result = parser.parse("Give me at least 50 ideas")
        assert result.quantity == 50
        assert result.modifier == "at_least"

    def test_parse_range_dash(self):
        """Parse '50-100'."""
        parser = UnifiedQuantityParser()
        result = parser.parse("Find 50-100 issues")
        assert result.quantity == 50
        assert result.range_max == 100

    def test_parse_range_between(self):
        """Parse 'between 50 and 100'."""
        parser = UnifiedQuantityParser()
        result = parser.parse("List between 50 and 100 items")
        assert result.quantity == 50
        assert result.range_max == 100

    def test_parse_spelled_hundred(self):
        """Parse 'hundred'."""
        parser = UnifiedQuantityParser()
        result = parser.parse("Give me a hundred items")
        assert result.quantity == 100

    def test_parse_compound_twenty_five(self):
        """Parse 'twenty-five'."""
        parser = UnifiedQuantityParser()
        result = parser.parse("List twenty-five things")
        assert result.quantity == 25

    def test_parse_compound_one_hundred(self):
        """Parse 'one hundred'."""
        parser = UnifiedQuantityParser()
        result = parser.parse("Give me one hundred items")
        assert result.quantity == 100

    def test_parse_implicit_few(self):
        """Parse 'few'."""
        parser = UnifiedQuantityParser()
        result = parser.parse("Give me a few examples")
        assert result.quantity == 3

    def test_parse_special_dozen(self):
        """Parse 'dozen'."""
        parser = UnifiedQuantityParser()
        result = parser.parse("Give me a dozen items")
        assert result.quantity == 12


# =============================================================================
# Tests for UnifiedRequestClassifier
# =============================================================================


class TestUnifiedRequestClassifier:
    """Tests for UnifiedRequestClassifier class."""

    def test_init(self):
        """Initialize classifier."""
        classifier = UnifiedRequestClassifier()
        assert classifier.quantity_parser is not None

    def test_classify_analysis_request(self):
        """Classify analysis request."""
        classifier = UnifiedRequestClassifier()
        result = classifier.classify("Analyze this code")
        assert result.request_type == RequestType.ANALYSIS

    def test_classify_list_request(self):
        """Classify list request."""
        classifier = UnifiedRequestClassifier()
        # Use 'items' instead of 'bugs' to avoid DEBUGGING classification
        result = classifier.classify("List all the functions in this code")
        assert result.request_type == RequestType.LIST_GENERATION

    def test_classify_implementation_request(self):
        """Classify implementation request."""
        classifier = UnifiedRequestClassifier()
        result = classifier.classify("Implement a new feature")
        assert result.request_type == RequestType.IMPLEMENTATION

    def test_classify_debugging_request(self):
        """Classify debugging request."""
        classifier = UnifiedRequestClassifier()
        result = classifier.classify("Fix this bug in the code")
        assert result.request_type == RequestType.DEBUGGING

    def test_classify_refactoring_request(self):
        """Classify refactoring request."""
        classifier = UnifiedRequestClassifier()
        result = classifier.classify("Refactor this function to be more efficient")
        assert result.request_type == RequestType.REFACTORING

    def test_classify_documentation_request(self):
        """Classify documentation request."""
        classifier = UnifiedRequestClassifier()
        result = classifier.classify("Write documentation for this API")
        assert result.request_type == RequestType.DOCUMENTATION

    def test_classify_testing_request(self):
        """Classify testing request."""
        classifier = UnifiedRequestClassifier()
        result = classifier.classify("Write unit tests for this class")
        assert result.request_type == RequestType.TESTING

    def test_classify_question(self):
        """Classify question that doesn't match other patterns."""
        classifier = UnifiedRequestClassifier()
        # Simple question without any indicator keywords
        result = classifier.classify("hello?")
        # Questions without specific patterns go to QUESTION
        assert result.request_type == RequestType.QUESTION

    def test_classify_read_only(self):
        """Detect read-only constraint."""
        classifier = UnifiedRequestClassifier()
        result = classifier.classify("Just analyze, don't modify anything")
        assert result.read_only is True

    def test_classify_output_format_json(self):
        """Detect JSON output format."""
        classifier = UnifiedRequestClassifier()
        result = classifier.classify("Return the results as JSON")
        assert result.output_format == OutputFormat.JSON

    def test_classify_output_format_table(self):
        """Detect table output format."""
        classifier = UnifiedRequestClassifier()
        result = classifier.classify("Show me a table of all errors")
        assert result.output_format == OutputFormat.TABLE

    def test_classify_numbered_list(self):
        """Detect numbered list format."""
        classifier = UnifiedRequestClassifier()
        result = classifier.classify("List 100 things")
        assert result.output_format == OutputFormat.NUMBERED_LIST

    def test_classify_pipeline_analysis_only(self):
        """Select ANALYSIS_ONLY pipeline."""
        classifier = UnifiedRequestClassifier()
        result = classifier.classify("Just analyze this, don't change anything")
        assert result.pipeline == Pipeline.ANALYSIS_ONLY

    def test_classify_detect_python(self):
        """Detect Python language."""
        classifier = UnifiedRequestClassifier()
        result = classifier.classify("Write this in Python")
        assert "python" in result.languages

    def test_classify_detect_framework_react(self):
        """Detect React framework."""
        classifier = UnifiedRequestClassifier()
        result = classifier.classify("Build a React component")
        assert "react" in result.frameworks

    def test_classify_detect_file_patterns(self):
        """Detect file patterns."""
        classifier = UnifiedRequestClassifier()
        result = classifier.classify("Fix the bug in main.py")
        assert "main.py" in result.file_patterns

    def test_classify_priority_required(self):
        """Detect priority ranking requirement."""
        classifier = UnifiedRequestClassifier()
        result = classifier.classify("List bugs by priority")
        assert result.priority_ranking_required is True

    def test_classify_must_include_code(self):
        """must_include_code True for implementation."""
        classifier = UnifiedRequestClassifier()
        result = classifier.classify("Implement a sorting function")
        assert result.must_include_code is True


# =============================================================================
# Tests for Convenience Functions
# =============================================================================


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_classify_request(self):
        """classify_request works."""
        result = classify_request("Analyze this code")
        assert isinstance(result, ClassificationResult)

    def test_parse_quantity_numeric(self):
        """parse_quantity works for numeric."""
        result = parse_quantity("Give me 100 items")
        assert result.quantity == 100

    def test_is_read_only_request_true(self):
        """is_read_only_request returns True."""
        assert is_read_only_request("Just analyze, don't modify") is True

    def test_is_read_only_request_false(self):
        """is_read_only_request returns False."""
        assert is_read_only_request("Implement this feature") is False

    def test_get_required_quantity_numeric(self):
        """get_required_quantity returns quantity."""
        assert get_required_quantity("List 50 items") == 50

    def test_get_required_quantity_none(self):
        """get_required_quantity returns 0 for no quantity."""
        assert get_required_quantity("Hello world") == 0


# =============================================================================
# Integration Tests
# =============================================================================


class TestUnifiedClassifierIntegration:
    """Integration tests for unified classifier."""

    def test_full_classification_flow(self):
        """Full classification flow."""
        # Use 'items' instead of 'bugs' to avoid DEBUGGING classification
        request = "List over 100 different Python improvements in main.py"
        result = classify_request(request)

        assert result.quantity.quantity == 100
        assert result.quantity.modifier == "over"
        assert result.request_type == RequestType.LIST_GENERATION
        assert "python" in result.languages

    def test_debugging_flow(self):
        """Debugging classification flow."""
        request = "Fix the TypeError bug in auth.py"
        result = classify_request(request)

        assert result.request_type == RequestType.DEBUGGING
        assert result.must_include_code is True
        assert "auth.py" in result.file_patterns

    def test_read_only_analysis_flow(self):
        """Read-only analysis flow."""
        request = "Don't modify anything, just explain what this code does"
        result = classify_request(request)

        assert result.read_only is True
        assert result.pipeline == Pipeline.ANALYSIS_ONLY
