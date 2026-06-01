"""
Advanced usage demonstration of the typecoverage library.
Shows complex scenarios and advanced features.
"""

from inspect import stack
from json import loads
from pathlib import Path
from shutil import rmtree
from time import time
from types import FrameType
from typing import Any, Dict, List

from typecoverage import Issue, Stats, typecoverage, analyze_targets


def demo_frame_analysis() -> None:
    """Demonstrate analyzing stack frames."""
    print("=" * 60)
    print("DEMO: Analyzing stack frames")
    print("=" * 60)

    def create_frame_with_issues() -> FrameType:
        """Create a function that generates type issues in its frame."""
        untyped_var: Any = 42  # type: ignore[unused-variable] # noqa: F841
        another_var: Any = "hello"  # type: ignore[unused-variable] # noqa: F841
        # Get the current frame
        return stack()[0].frame

    frame: FrameType = create_frame_with_issues()
    print("Analyzing current frame context:")
    try:
        result: str = typecoverage().detect_untyped(
            frame,
            context_lines=2,
            force_color=False,
        )
        print(result)
    except Exception as e:
        print(f"Frame analysis note: {e}")
        print("(Frame analysis may have limitations depending on context)")


def demo_glob_patterns() -> None:
    """Demonstrate analyzing files using glob patterns."""
    print("\n" + "=" * 60)
    print("DEMO: Glob pattern analysis")
    print("=" * 60)
    # Create temporary directory structure
    temp_dir: Path = Path("temp_demo")
    temp_dir.mkdir(exist_ok=True)
    files: Dict[str, str] = {
        "module1.py":
        """
def func1(x):
    return x * 2

def func2(a, b: int):
    return a + b
""",
        "module2.py":
        """
class MyClass:
    def method1(self, value):
        self.value = value

    def method2(self, x: int) -> int:
        return x + 1
""",
        "subdir/nested.py":
        """
def nested_function(param):
    result = param.upper()
    return result
""",
    }
    try:
        # Create files
        for filename, content in files.items():
            filepath: Path = temp_dir / filename
            filepath.parent.mkdir(exist_ok=True)
            filepath.write_text(content)
        # Analyze using glob pattern
        print(f"Analyzing {temp_dir}/*.py:")
        result: str = typecoverage().detect_untyped(
            f"{temp_dir}/*.py",
            context_lines=1,
            statistics=True,
            force_color=False,
        )
        print(result)
        # Analyze recursively
        print(f"\nAnalyzing {temp_dir}/**/*.py (recursive):")
        result = typecoverage().detect_untyped(
            f"{temp_dir}/**/*.py",
            recursive=True,
            context_lines=1,
            statistics=True,
            force_color=False,
        )
        print(result)
    finally:
        # Clean up
        if temp_dir.exists():
            rmtree(temp_dir)


def demo_exclusion_patterns() -> None:
    """Demonstrate file exclusion patterns."""
    print("\n" + "=" * 60)
    print("DEMO: File exclusion patterns")
    print("=" * 60)
    temp_dir: Path = Path("temp_exclusion_demo")
    temp_dir.mkdir(exist_ok=True)
    files: Dict[str, str] = {
        "main.py": "def main(args): pass",
        "test_file.py": "def test_func(x): pass",
        "helpers.py": "def helper(data): pass",
        "_private.py": "def private_func(x): pass",
        "backup.py.bak": "def old_func(x): pass",
    }
    try:
        # Create files
        for filename, content in files.items():
            (temp_dir / filename).write_text(content)
        # Analyze without exclusions
        print("Analyzing without exclusions:")
        issues: List[Issue]
        errors: List[str]
        issues, errors = analyze_targets(
            str(temp_dir),
            recursive=True,
            extensions=[".py", ".bak"],
        )
        print(f"Found {len(issues)} issues in"
              f"{len({i.file for i in issues})} files")
        # Analyze with exclusions
        print("\nAnalyzing with exclusions (test_, _private):")
        issues, errors = analyze_targets(
            str(temp_dir),
            recursive=True,
            extensions=[".py"],
            exclude=["test_", "_private"],
        )
        print(f"Found {len(issues)} issues in"
              f"{len({i.file for i in issues})} files")
    finally:
        if temp_dir.exists():
            rmtree(temp_dir)


def demo_parallel_processing() -> None:
    """Demonstrate parallel file processing."""
    print("\n" + "=" * 60)
    print("DEMO: Parallel processing performance")
    print("=" * 60)
    temp_dir: Path = Path("temp_parallel_demo")
    temp_dir.mkdir(exist_ok=True)
    # Create many files to demonstrate parallel processing
    file_content: str = """
def function_{i}(param):
    result = param * 2
    return result

class Class_{i}:
    def method(self, x, y):
        return x + y
"""
    try:
        # Create multiple files
        for i in range(10):
            content: str = file_content.format(i=i)
            (temp_dir / f"file_{i}.py").write_text(content)
        print(f"Analyzing {temp_dir} with parallel processing:")
        start_time: float = time()
        issues: List[Issue]
        errors: List[str]
        issues, errors = analyze_targets(
            str(temp_dir),
            recursive=True,
        )
        end_time: float = time()
        processing_time: float = end_time - start_time
        print(f"Processed {len(list(temp_dir.glob('*.py')))} files")
        print(f"Found {len(issues)} issues")
        print(f"Processing time: {processing_time:.3f} seconds")
        print("(Parallel processing automatically used for multiple files)")
    finally:
        if temp_dir.exists():
            rmtree(temp_dir)


def demo_comprehensive_analysis() -> None:
    """Demonstrate comprehensive analysis with all features."""
    print("\n" + "=" * 60)
    print("DEMO: Comprehensive analysis")
    print("=" * 60)
    # Complex code example with various constructs
    complex_code: str = '''
"""Module with various Python constructs."""

from typing import List, Dict, Optional, Union
from enum import Enum
import json

class Status(Enum):
    ACTIVE = 1
    INACTIVE = 2

class DataProcessor:
    """Process data with various methods."""

    def __init__(self, config: Dict[str, str]):
        self.config = config
        self.cache = {}  # Untyped cache

    def process_items(self, items, callback=None):
        """Process items with optional callback."""
        results = []

        for item in items:
            try:
                processed = self._transform_item(item)
                if callback:
                    callback(processed)
                results.append(processed)
            except ValueError as e:
                self._handle_error(e)
                continue

        return results

    def _transform_item(self, item):
        """Transform a single item."""
        # Various untyped variables
        multiplier = self.config.get("multiplier", 1)
        offset = self.config.get("offset", 0)

        with open("config.json") as f:
            extra_config = json.load(f)

        result = item * multiplier + offset

        # List comprehension
        normalized = [x / 100 for x in result if x > 0]

        return normalized

    def _handle_error(self, error):
        """Handle processing errors."""
        print(f"Error: {error}")

# Module-level code
DEFAULT_CONFIG = {"multiplier": 2, "offset": 10}
processor = DataProcessor(DEFAULT_CONFIG)

def main():
    """Main function."""
    test_data = [1, 2, 3, 4, 5]
    result = processor.process_items(test_data)
    return result
'''

    print("Analyzing complex code with various ignore settings:")
    # Test different configurations
    configs: List[Dict[str, Any]] = [
        {
            "name": "Default settings",
            "kwargs": {},
        },
        {
            "name": "Include comprehensions",
            "kwargs": {
                "ignore_comprehensions": False
            },
        },
        {
            "name": "Include underscore vars",
            "kwargs": {
                "ignore_underscore_vars": False
            },
        },
        {
            "name": "Include exception vars",
            "kwargs": {
                "ignore_except_vars": False
            },
        },
        {
            "name": "Include context vars",
            "kwargs": {
                "ignore_context_vars": False
            },
        },
        {
            "name": "Include all variables",
            "kwargs": {
                "ignore_comprehensions": False,
                "ignore_underscore_vars": False,
                "ignore_except_vars": False,
                "ignore_context_vars": False,
            },
        },
    ]
    for config in configs:
        print(f"\n{config['name']}:")
        issues: List[Issue]
        errors: List[str]
        issues, errors = analyze_targets(complex_code, **config["kwargs"])
        if errors:
            print(f"  Errors: {len(errors)}")
        stats: Stats = typecoverage().compute_stats(issues)
        print(f"  Total issues: {stats.total}")
        print(f"  Arguments: {stats.by_type.get('untyped-argument', 0)}")
        print(f"  Returns: {stats.by_type.get('untyped-return', 0)}")
        print(f"  Variables: {stats.by_type.get('untyped-variable', 0)}")


def demo_output_formats() -> None:
    """Demonstrate different output formats."""
    print("\n" + "=" * 60)
    print("DEMO: Output formats and options")
    print("=" * 60)

    code: str = '''
def example_function(data, options):
    """Example with multiple issues."""
    processed_data = []

    for item in data:
        if item.get("active", False):
            result = process_item(item, options)
            processed_data.append(result)

    return processed_data

def process_item(item, options):
    multiplier = options.get("multiplier", 1)
    return item.get("value", 0) * multiplier
'''
    checker: typecoverage = typecoverage()
    # Text format with colors
    print("Text format (no color):")
    result: str = checker.detect_untyped(
        code,
        format="text",
        statistics=True,
        context_lines=1,
        force_color=False,
    )
    print(result[:300] + "..." if len(result) > 300 else result)
    # JSON format
    print("\nJSON format:")
    result = checker.detect_untyped(
        code,
        format="json",
        statistics=True,
    )
    # Pretty print JSON
    data: Dict[str, Any] = loads(result)
    print(f"Version: {data['version']}")
    print(f"Total issues: {data['statistics']['total']}")
    print(f"Issue types: {list(data['statistics'].keys())}")
    print(
        f"First issue: {data['issues'][0]['type']} - {data['issues'][0]['name']}"
    )


if __name__ == "__main__":
    """Run all advanced demonstrations."""
    print("TYPECOVERAGE LIBRARY - ADVANCED DEMONSTRATIONS")
    print("This script shows advanced features and use cases.")
    demo_frame_analysis()
    demo_glob_patterns()
    demo_exclusion_patterns()
    demo_parallel_processing()
    demo_comprehensive_analysis()
    demo_output_formats()
    print("\n" + "=" * 60)
    print("All advanced demonstrations completed!")
    print("=" * 60)
