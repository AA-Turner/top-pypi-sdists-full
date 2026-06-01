"""
Basic usage demonstration of the typecoverage library.
Shows common scenarios and how to use the API.
"""

from json import loads
from pathlib import Path
from typing import Any, Dict, List, Tuple

from typecoverage import Issue, Stats, typecoverage, detect_untyped


def demo_string_analysis() -> None:
    """Demonstrate analyzing code as a string."""
    print("=" * 60)
    print("DEMO: Analyzing code strings")
    print("=" * 60)
    # Example code with type issues
    code: str = """
def calculate_area(length, width):
    area = length * width
    return area

def greet_user(name):
    message = f"Hello, {name}!"
    return message

x = 42
y = "hello"
"""
    print("Analyzing this code:")
    print(code)
    print("\nResults:")
    result: str = detect_untyped(
        code,
        context_lines=1,
        statistics=True,
        force_color=False,
    )
    print(result)


def demo_function_analysis() -> None:
    """Demonstrate analyzing live function objects."""
    print("\n" + "=" * 60)
    print("DEMO: Analyzing function objects")
    print("=" * 60)

    # Define some functions with varying type completeness
    def untyped_function(a: Any, b: Any) -> Any:
        """Function with no type annotations."""
        return a + b

    def partially_typed_function(a: int, b: Any) -> Any:
        """Function with partial type annotations."""
        return a + b

    def fully_typed_function(a: int, b: int) -> int:
        """Function with complete type annotations."""
        return a + b

    functions: List[Tuple[str, Any]] = [
        ("Untyped function", untyped_function),
        ("Partially typed function", partially_typed_function),
        ("Fully typed function", fully_typed_function),
    ]
    for name, func in functions:
        print(f"\nAnalyzing {name}:")
        result: str = detect_untyped(
            func,
            context_lines=1,
            force_color=False,
        )
        if result.strip():
            print(result)
        else:
            print("✓ No type annotation issues found")


def demo_class_analysis() -> None:
    """Demonstrate analyzing class objects."""
    print("\n" + "=" * 60)
    print("DEMO: Analyzing class objects")
    print("=" * 60)

    class PartiallyTypedClass:
        """A class with mixed type annotation coverage."""

        def __init__(self, name: str) -> None:
            self.name: str = name
            self.count = 0  # Untyped attribute

        def get_name(self) -> str:  # No return type
            return self.name

        def increment(self, amount: Any) -> None:  # Untyped parameter
            self.count += amount

        def get_count(self) -> int:  # Fully typed
            return self.count

    print("Analyzing PartiallyTypedClass:")
    result: str = detect_untyped(
        PartiallyTypedClass,
        context_lines=1,
        statistics=True,
        force_color=False,
    )
    print(result)


def demo_file_analysis() -> None:
    """Demonstrate analyzing files."""
    print("\n" + "=" * 60)
    print("DEMO: Analyzing files")
    print("=" * 60)
    # Create a temporary file for demonstration
    demo_file: Path = Path("demo_temp.py")
    demo_code: str = '''"""Temporary demo file."""

def process_data(data, options):
    """Process some data with options."""
    if not data:
        return None

    result = []
    for item in data:
        processed = transform_item(item, options)
        result.append(processed)

    return result

def transform_item(item, options):
    """Transform a single item."""
    multiplier = options.get("multiplier", 1)
    return item * multiplier

# Module-level variables
DEFAULT_OPTIONS = {"multiplier": 2}
cache = {}
'''
    try:
        demo_file.write_text(demo_code)
        print(f"Analyzing file: {demo_file}")
        result: str = detect_untyped(
            str(demo_file),
            context_lines=1,
            statistics=True,
            force_color=False,
        )
        print(result)
    finally:
        # Clean up
        if demo_file.exists():
            demo_file.unlink()


def demo_api_usage() -> None:
    """Demonstrate using the typecoverage API directly."""
    print("\n" + "=" * 60)
    print("DEMO: Using typecoverage API directly")
    print("=" * 60)
    checker: typecoverage = typecoverage()
    # Analyze with different options
    code: str = """
def example_func(x, y):
    z = x + y
    return z

for i in range(10):
    pass

try:
    risky_operation()
except Exception as e:
    handle_error(e)

with open('file.txt') as f:
    content = f.read()
"""
    print("Analyzing with default settings:")
    issues: List[Issue]
    errors: List[str]
    issues, errors = checker.analyze_targets(
        code,
        context_lines=0,
    )
    print(f"Found {len(issues)} issues")
    print("\nAnalyzing with different ignore settings:")
    issues, errors = checker.analyze_targets(
        code,
        context_lines=0,
        ignore_for_targets=False,
        ignore_except_vars=False,
        ignore_context_vars=False,
    )
    print(f"Found {len(issues)} issues")
    # Show statistics
    stats: Stats = checker.compute_stats(issues)
    print("\nStatistics:")
    print(f"  Total: {stats.total}")
    print(f"  Arguments: {stats.by_type.get('untyped-argument', 0)}")
    print(f"  Returns: {stats.by_type.get('untyped-return', 0)}")
    print(f"  Variables: {stats.by_type.get('untyped-variable', 0)}")


def demo_suppression() -> None:
    """Demonstrate comment-based suppression."""
    print("\n" + "=" * 60)
    print("DEMO: Comment-based suppression")
    print("=" * 60)
    code_without_suppression: str = """
def func(x, y):
    return x + y
"""
    code_with_suppression: str = """
def func(x, y):  # type: ignore
    return x + y
"""
    print("Code without suppression:")
    result: str = detect_untyped(code_without_suppression, force_color=False)
    print(result)
    print("\nSame code with suppression comment:")
    result = detect_untyped(code_with_suppression, force_color=False)
    if result.strip():
        print(result)
    else:
        print("✓ Issues suppressed by comment")


def demo_json_output() -> None:
    """Demonstrate JSON output format."""
    print("\n" + "=" * 60)
    print("DEMO: JSON output format")
    print("=" * 60)
    code: str = """
def process(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result
"""
    checker: typecoverage = typecoverage()
    result: str = checker.detect_untyped(
        code,
        format="json",
        statistics=True,
    )
    print("JSON output:")
    print(result)
    # Parse and display key information
    data: Dict[str, Any] = loads(result)
    print("\nSummary from JSON:")
    print(f"  Total issues: {data['statistics']['total']}")
    print(f"  Files analyzed: {len(data['by_file'])}")
    print(f"  Issues found: {len(data['issues'])}")


if __name__ == "__main__":
    """Run all demonstrations."""
    print("TYPECOVERAGE LIBRARY DEMONSTRATIONS")
    print("This script shows various ways to use the typecoverage library.")
    demo_string_analysis()
    demo_function_analysis()
    demo_class_analysis()
    demo_file_analysis()
    demo_api_usage()
    demo_suppression()
    demo_json_output()
    print("\n" + "=" * 60)
    print("All demonstrations completed!")
    print("=" * 60)
