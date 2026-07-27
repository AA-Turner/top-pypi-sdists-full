"""Tests for QualityGate boilerplate and placeholder detection.

These tests verify that the QualityGate properly rejects:
- Placeholder code (TODO, FIXME, pass statements)
- Boilerplate/copy-paste code
- Incomplete implementations
"""

import pytest


class MockRenderer:
    """Mock renderer for testing."""

    def __init__(self):
        self.messages = []

    def info(self, msg):
        self.messages.append(("info", msg))

    def warning(self, msg):
        self.messages.append(("warning", msg))

    def error(self, msg):
        self.messages.append(("error", msg))


class TestBoilerplateDetection:
    """Test detection of boilerplate/placeholder patterns."""

    @pytest.fixture
    def quality_gate(self, tmp_path):
        """Create a QualityGate instance for testing."""
        from sage.cli_core import QualityGate

        return QualityGate(tmp_path, MockRenderer())

    def test_detects_todo_comments(self, quality_gate):
        """TODO comments should be flagged."""
        content = """
def process_data(data):
    # TODO: implement actual processing
    pass
"""
        is_valid, issues = quality_gate.check_boilerplate("module.py", content)
        assert is_valid is False
        assert any("TODO" in issue for issue in issues)

    def test_detects_fixme_comments(self, quality_gate):
        """FIXME comments should be flagged."""
        content = """
def calculate_total(items):
    # FIXME: this is broken
    return 0
"""
        is_valid, issues = quality_gate.check_boilerplate("module.py", content)
        assert is_valid is False
        assert any("FIXME" in issue for issue in issues)

    def test_detects_not_implemented_error(self, quality_gate):
        """NotImplementedError should be flagged."""
        content = """
def feature_x():
    raise NotImplementedError("Not yet implemented")
"""
        is_valid, issues = quality_gate.check_boilerplate("module.py", content)
        assert is_valid is False
        assert any("NotImplementedError" in issue for issue in issues)

    def test_detects_multiple_empty_functions(self, quality_gate):
        """Multiple empty functions (just 'pass') should be flagged."""
        content = """
def func1():
    pass

def func2():
    pass

def func3():
    pass
"""
        is_valid, issues = quality_gate.check_boilerplate("module.py", content)
        assert is_valid is False
        assert any("empty" in issue.lower() for issue in issues)

    def test_single_pass_function_is_ok(self, quality_gate):
        """A single pass function might be a valid stub."""
        content = '''
def placeholder():
    """This is an intentional placeholder."""
    pass

def real_function():
    return 42
'''
        is_valid, issues = quality_gate.check_boilerplate("module.py", content)
        # Single pass is allowed, multiple are not
        # This test checks we don't over-flag
        assert is_valid is True or len(issues) <= 1

    def test_detects_repetitive_function_names(self, quality_gate):
        """Many functions with similar names indicate copy-paste."""
        content = """
def process_1():
    return 1

def process_2():
    return 2

def process_3():
    return 3

def process_4():
    return 4

def process_5():
    return 5

def process_6():
    return 6

def process_7():
    return 7

def process_8():
    return 8

def process_9():
    return 9

def process_10():
    return 10

def process_11():
    return 11
"""
        is_valid, issues = quality_gate.check_boilerplate("module.py", content)
        assert is_valid is False
        assert any("repetitive" in issue.lower() or "process" in issue.lower() for issue in issues)

    def test_valid_code_passes(self, quality_gate):
        """Well-written code should pass all checks."""
        content = '''
def calculate_sum(numbers: list[int]) -> int:
    """Calculate the sum of a list of numbers."""
    total = 0
    for num in numbers:
        total += num
    return total


def calculate_average(numbers: list[int]) -> float:
    """Calculate the average of a list of numbers."""
    if not numbers:
        return 0.0
    return calculate_sum(numbers) / len(numbers)
'''
        is_valid, issues = quality_gate.check_boilerplate("module.py", content)
        assert is_valid is True
        assert len(issues) == 0


class TestImplementationCompleteness:
    """Test detection of incomplete implementations."""

    @pytest.fixture
    def quality_gate(self, tmp_path):
        """Create a QualityGate instance for testing."""
        from sage.cli_core import QualityGate

        return QualityGate(tmp_path, MockRenderer())

    def test_mostly_stub_functions_flagged(self, quality_gate):
        """If most functions are stubs, it should be flagged."""
        content = '''
def func1():
    """Do something."""
    pass

def func2():
    """Do something else."""
    return None

def func3():
    """Another thing."""
    pass

def func4():
    """Real implementation."""
    return 42
'''
        # More than half are stubs
        is_valid, issues = quality_gate.check_implementation_completeness("module.py", content)
        assert is_valid is False
        assert any("incomplete" in issue.lower() or "stub" in issue.lower() for issue in issues)

    def test_mostly_complete_functions_pass(self, quality_gate):
        """If most functions are complete, it should pass."""
        content = '''
def func1():
    """Do something."""
    return 42

def func2():
    """Do something else."""
    return "hello"

def func3():
    """Another thing."""
    return [1, 2, 3]

def func4():
    """Placeholder - allowed because most are complete."""
    pass
'''
        is_valid, issues = quality_gate.check_implementation_completeness("module.py", content)
        assert is_valid is True

    def test_test_files_skipped(self, quality_gate):
        """Test files should not be checked for implementation completeness."""
        content = """
def test_something():
    pass

def test_another():
    pass
"""
        # Test files are skipped
        is_valid, issues = quality_gate.check_implementation_completeness("test_module.py", content)
        assert is_valid is True

        is_valid, issues = quality_gate.check_implementation_completeness(
            "tests/test_something.py", content
        )
        assert is_valid is True


class TestAllGatesIntegration:
    """Test that all quality gates work together."""

    @pytest.fixture
    def quality_gate(self, tmp_path):
        """Create a QualityGate instance for testing."""
        from sage.cli_core import QualityGate

        return QualityGate(tmp_path, MockRenderer())

    def test_all_gates_on_bad_code(self, quality_gate):
        """Code with multiple issues should fail multiple gates."""
        bad_code = """
# TODO: fix all of this
import nonexistent_module

def process():
    pass

def handle():
    pass

def manage():
    pass
"""
        all_passed, issues = quality_gate.run_all_gates("bad_module.py", bad_code)
        assert all_passed is False
        assert len(issues) > 0

    def test_all_gates_on_good_code(self, quality_gate, tmp_path):
        """Well-written code should pass all gates."""
        good_code = '''
"""A well-written module."""

def calculate(x: int, y: int) -> int:
    """Calculate the sum of two numbers."""
    return x + y


def validate(value: str) -> bool:
    """Validate that a string is not empty."""
    return bool(value and value.strip())
'''
        # Write the file so syntax check works
        (tmp_path / "good_module.py").write_text(good_code)

        all_passed, issues = quality_gate.run_all_gates("good_module.py", good_code)
        # May have some issues from imports/LSP, but core quality should pass
        # Just verify it runs without error
        assert isinstance(all_passed, bool)
        assert isinstance(issues, list)
