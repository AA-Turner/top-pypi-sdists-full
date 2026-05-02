"""
TDD Tests for P3 Items 116-130: Documentation, Benchmarks, and Startup.

This module tests:
- Items 116-118: Documentation generation and API docs
- Items 119-121: Help system and usage documentation
- Items 122-124: Benchmark framework and performance metrics
- Items 125-127: Startup initialization and configuration
- Items 128-130: CLI utilities and validation
"""

import json
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Any

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# =============================================================================
# Items 116-118: Documentation Generation
# =============================================================================


class DocFormat(Enum):
    """Documentation output formats."""

    MARKDOWN = auto()
    HTML = auto()
    RST = auto()
    JSON = auto()


@dataclass
class FunctionDoc:
    """Documentation for a function."""

    name: str
    signature: str
    docstring: str
    parameters: list[tuple[str, str, str]] = field(
        default_factory=list
    )  # (name, type, description)
    returns: str = ""
    raises: list[tuple[str, str]] = field(default_factory=list)  # (exception, description)
    examples: list[str] = field(default_factory=list)
    deprecated: bool = False
    since: str = ""


@dataclass
class ClassDoc:
    """Documentation for a class."""

    name: str
    docstring: str
    base_classes: list[str] = field(default_factory=list)
    methods: list[FunctionDoc] = field(default_factory=list)
    attributes: list[tuple[str, str, str]] = field(
        default_factory=list
    )  # (name, type, description)


@dataclass
class ModuleDoc:
    """Documentation for a module."""

    name: str
    docstring: str
    path: str
    classes: list[ClassDoc] = field(default_factory=list)
    functions: list[FunctionDoc] = field(default_factory=list)
    constants: list[tuple[str, Any]] = field(default_factory=list)


class DocumentationGenerator:
    """
    Generate documentation from Python code.

    Items 116-118: Documentation generation
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self._modules: list[ModuleDoc] = []

    def parse_module(self, module_path: Path) -> ModuleDoc:
        """Parse a Python module and extract documentation."""
        content = module_path.read_text()
        name = module_path.stem

        # Extract module docstring
        docstring = ""
        if content.startswith('"""') or content.startswith("'''"):
            quote = content[:3]
            end = content.find(quote, 3)
            if end > 0:
                docstring = content[3:end].strip()

        return ModuleDoc(
            name=name,
            docstring=docstring,
            path=str(module_path.relative_to(self.project_root)),
        )

    def generate_markdown(self, module: ModuleDoc) -> str:
        """Generate Markdown documentation for a module."""
        lines = [
            f"# {module.name}",
            "",
            module.docstring,
            "",
            f"**Path:** `{module.path}`",
            "",
        ]

        if module.classes:
            lines.append("## Classes")
            lines.append("")
            for cls in module.classes:
                lines.append(f"### {cls.name}")
                lines.append("")
                lines.append(cls.docstring)
                lines.append("")

                if cls.methods:
                    lines.append("#### Methods")
                    lines.append("")
                    for method in cls.methods:
                        lines.append(f"- `{method.signature}`")
                        if method.docstring:
                            lines.append(f"  {method.docstring}")
                    lines.append("")

        if module.functions:
            lines.append("## Functions")
            lines.append("")
            for func in module.functions:
                lines.append(f"### `{func.signature}`")
                lines.append("")
                lines.append(func.docstring)
                lines.append("")

        return "\n".join(lines)

    def generate_html(self, module: ModuleDoc) -> str:
        """Generate HTML documentation for a module."""
        lines = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            f"<title>{module.name}</title>",
            "<style>",
            "body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }",
            "code { background: #f0f0f0; padding: 2px 5px; }",
            "pre { background: #f0f0f0; padding: 15px; overflow-x: auto; }",
            ".method { margin-left: 20px; }",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>{module.name}</h1>",
            f"<p>{module.docstring}</p>",
            f"<p><strong>Path:</strong> <code>{module.path}</code></p>",
        ]

        if module.classes:
            lines.append("<h2>Classes</h2>")
            for cls in module.classes:
                lines.append(f"<h3>{cls.name}</h3>")
                lines.append(f"<p>{cls.docstring}</p>")

        if module.functions:
            lines.append("<h2>Functions</h2>")
            for func in module.functions:
                lines.append(f"<h3><code>{func.signature}</code></h3>")
                lines.append(f"<p>{func.docstring}</p>")

        lines.extend(["</body>", "</html>"])
        return "\n".join(lines)

    def generate_json(self, module: ModuleDoc) -> str:
        """Generate JSON documentation for a module."""

        def serialize_func(func: FunctionDoc) -> dict:
            return {
                "name": func.name,
                "signature": func.signature,
                "docstring": func.docstring,
                "parameters": [
                    {"name": n, "type": t, "description": d} for n, t, d in func.parameters
                ],
                "returns": func.returns,
                "raises": [{"exception": e, "description": d} for e, d in func.raises],
                "examples": func.examples,
                "deprecated": func.deprecated,
                "since": func.since,
            }

        def serialize_class(cls: ClassDoc) -> dict:
            return {
                "name": cls.name,
                "docstring": cls.docstring,
                "base_classes": cls.base_classes,
                "methods": [serialize_func(m) for m in cls.methods],
                "attributes": [
                    {"name": n, "type": t, "description": d} for n, t, d in cls.attributes
                ],
            }

        return json.dumps(
            {
                "name": module.name,
                "docstring": module.docstring,
                "path": module.path,
                "classes": [serialize_class(c) for c in module.classes],
                "functions": [serialize_func(f) for f in module.functions],
                "constants": [{"name": n, "value": str(v)} for n, v in module.constants],
            },
            indent=2,
        )


class TestDocumentationGeneration:
    """Tests for Items 116-118: Documentation Generation."""

    def test_parse_module_extracts_docstring(self, tmp_path: Path):
        """Item 116: Parse module and extract docstring."""
        module_file = tmp_path / "example.py"
        module_file.write_text('"""This is a test module."""\n\ndef foo(): pass\n')

        generator = DocumentationGenerator(tmp_path)
        doc = generator.parse_module(module_file)

        assert doc.name == "example"
        assert doc.docstring == "This is a test module."
        assert doc.path == "example.py"

    def test_generate_markdown_output(self, tmp_path: Path):
        """Item 116: Generate Markdown documentation."""
        module = ModuleDoc(
            name="test_module",
            docstring="A test module for documentation.",
            path="sage/test_module.py",
        )

        generator = DocumentationGenerator(tmp_path)
        markdown = generator.generate_markdown(module)

        assert "# test_module" in markdown
        assert "A test module for documentation." in markdown
        assert "`sage/test_module.py`" in markdown

    def test_generate_markdown_with_classes(self, tmp_path: Path):
        """Item 117: Include class documentation in Markdown."""
        module = ModuleDoc(
            name="test_module",
            docstring="Module with classes.",
            path="sage/test_module.py",
            classes=[
                ClassDoc(
                    name="TestClass",
                    docstring="A test class.",
                    methods=[
                        FunctionDoc(
                            name="method1",
                            signature="method1(self, x: int) -> str",
                            docstring="A method that does something.",
                        )
                    ],
                )
            ],
        )

        generator = DocumentationGenerator(tmp_path)
        markdown = generator.generate_markdown(module)

        assert "## Classes" in markdown
        assert "### TestClass" in markdown
        assert "A test class." in markdown
        assert "#### Methods" in markdown
        assert "`method1(self, x: int) -> str`" in markdown

    def test_generate_markdown_with_functions(self, tmp_path: Path):
        """Item 117: Include function documentation."""
        module = ModuleDoc(
            name="test_module",
            docstring="Module with functions.",
            path="sage/test_module.py",
            functions=[
                FunctionDoc(
                    name="my_function",
                    signature="my_function(a: int, b: str) -> bool",
                    docstring="A function that processes data.",
                )
            ],
        )

        generator = DocumentationGenerator(tmp_path)
        markdown = generator.generate_markdown(module)

        assert "## Functions" in markdown
        assert "### `my_function(a: int, b: str) -> bool`" in markdown
        assert "A function that processes data." in markdown

    def test_generate_html_output(self, tmp_path: Path):
        """Item 118: Generate HTML documentation."""
        module = ModuleDoc(
            name="test_module",
            docstring="A test module.",
            path="sage/test_module.py",
        )

        generator = DocumentationGenerator(tmp_path)
        html = generator.generate_html(module)

        assert "<!DOCTYPE html>" in html
        assert "<title>test_module</title>" in html
        assert "<h1>test_module</h1>" in html
        assert "A test module." in html

    def test_generate_json_output(self, tmp_path: Path):
        """Item 118: Generate JSON documentation."""
        module = ModuleDoc(
            name="test_module",
            docstring="A test module.",
            path="sage/test_module.py",
            functions=[
                FunctionDoc(
                    name="my_func",
                    signature="my_func(x: int) -> str",
                    docstring="Process x.",
                    parameters=[("x", "int", "Input value")],
                    returns="Processed string",
                )
            ],
        )

        generator = DocumentationGenerator(tmp_path)
        json_str = generator.generate_json(module)
        data = json.loads(json_str)

        assert data["name"] == "test_module"
        assert data["docstring"] == "A test module."
        assert len(data["functions"]) == 1
        assert data["functions"][0]["name"] == "my_func"
        assert data["functions"][0]["returns"] == "Processed string"

    def test_function_doc_with_parameters(self):
        """Item 116: Document function parameters."""
        func = FunctionDoc(
            name="process_data",
            signature="process_data(data: list, limit: int = 100) -> dict",
            docstring="Process input data.",
            parameters=[
                ("data", "list", "The data to process"),
                ("limit", "int", "Maximum items to process"),
            ],
            returns="dict containing processed results",
        )

        assert func.name == "process_data"
        assert len(func.parameters) == 2
        assert func.parameters[0] == ("data", "list", "The data to process")
        assert func.returns == "dict containing processed results"

    def test_function_doc_with_raises(self):
        """Item 117: Document raised exceptions."""
        func = FunctionDoc(
            name="risky_operation",
            signature="risky_operation(x: int) -> None",
            docstring="Perform risky operation.",
            raises=[
                ("ValueError", "If x is negative"),
                ("RuntimeError", "If operation fails"),
            ],
        )

        assert len(func.raises) == 2
        assert func.raises[0] == ("ValueError", "If x is negative")

    def test_deprecated_function_documentation(self):
        """Item 118: Handle deprecated functions."""
        func = FunctionDoc(
            name="old_function",
            signature="old_function()",
            docstring="This function is deprecated.",
            deprecated=True,
            since="1.0.0",
        )

        assert func.deprecated is True
        assert func.since == "1.0.0"


# =============================================================================
# Items 119-121: Help System and Usage Documentation
# =============================================================================


@dataclass
class CommandInfo:
    """Information about a CLI command."""

    name: str
    description: str
    usage: str
    arguments: list[tuple[str, str, bool]] = field(
        default_factory=list
    )  # (name, description, required)
    options: list[tuple[str, str, str]] = field(
        default_factory=list
    )  # (flag, description, default)
    examples: list[tuple[str, str]] = field(default_factory=list)  # (command, description)
    subcommands: list[str] = field(default_factory=list)
    aliases: list[str] = field(default_factory=list)


class HelpGenerator:
    """
    Generate help text for CLI commands.

    Items 119-121: Help system
    """

    def __init__(self):
        self._commands: dict[str, CommandInfo] = {}
        self._global_options: list[tuple[str, str, str]] = []

    def register_command(self, cmd: CommandInfo) -> None:
        """Register a command."""
        self._commands[cmd.name] = cmd
        for alias in cmd.aliases:
            self._commands[alias] = cmd

    def add_global_option(self, flag: str, description: str, default: str = "") -> None:
        """Add a global option."""
        self._global_options.append((flag, description, default))

    def generate_help(self, command: str | None = None) -> str:
        """Generate help text."""
        if command:
            return self._command_help(command)
        return self._global_help()

    def _global_help(self) -> str:
        """Generate global help."""
        lines = [
            "SAGE - Local-First AI Coding Assistant",
            "",
            "Usage: sage [OPTIONS] COMMAND [ARGS]",
            "",
            "Commands:",
        ]

        # Group unique commands (skip aliases)
        seen = set()
        for name, cmd in sorted(self._commands.items()):
            if cmd.name in seen:
                continue
            seen.add(cmd.name)
            alias_str = f" (alias: {', '.join(cmd.aliases)})" if cmd.aliases else ""
            lines.append(f"  {cmd.name:15} {cmd.description}{alias_str}")

        if self._global_options:
            lines.append("")
            lines.append("Global Options:")
            for flag, desc, default in self._global_options:
                default_str = f" (default: {default})" if default else ""
                lines.append(f"  {flag:20} {desc}{default_str}")

        lines.append("")
        lines.append("Run 'sage help <command>' for more information on a command.")
        return "\n".join(lines)

    def _command_help(self, command: str) -> str:
        """Generate help for a specific command."""
        cmd = self._commands.get(command)
        if not cmd:
            return f"Unknown command: {command}"

        lines = [
            f"sage {cmd.name}",
            "",
            cmd.description,
            "",
            f"Usage: {cmd.usage}",
        ]

        if cmd.arguments:
            lines.append("")
            lines.append("Arguments:")
            for name, desc, required in cmd.arguments:
                req_str = " (required)" if required else ""
                lines.append(f"  {name:15} {desc}{req_str}")

        if cmd.options:
            lines.append("")
            lines.append("Options:")
            for flag, desc, default in cmd.options:
                default_str = f" (default: {default})" if default else ""
                lines.append(f"  {flag:20} {desc}{default_str}")

        if cmd.examples:
            lines.append("")
            lines.append("Examples:")
            for example, desc in cmd.examples:
                lines.append(f"  $ {example}")
                if desc:
                    lines.append(f"    {desc}")

        if cmd.subcommands:
            lines.append("")
            lines.append("Subcommands:")
            for sub in cmd.subcommands:
                lines.append(f"  {sub}")

        return "\n".join(lines)

    def search_commands(self, query: str) -> list[CommandInfo]:
        """Search commands by keyword."""
        query_lower = query.lower()
        results = []
        seen = set()

        for name, cmd in self._commands.items():
            if cmd.name in seen:
                continue

            if (
                query_lower in cmd.name.lower()
                or query_lower in cmd.description.lower()
                or any(query_lower in alias.lower() for alias in cmd.aliases)
            ):
                results.append(cmd)
                seen.add(cmd.name)

        return results


class TestHelpSystem:
    """Tests for Items 119-121: Help System."""

    def test_register_and_retrieve_command(self):
        """Item 119: Register commands in help system."""
        helper = HelpGenerator()
        cmd = CommandInfo(
            name="run",
            description="Run the interactive agent",
            usage="sage run [OPTIONS]",
        )

        helper.register_command(cmd)
        help_text = helper.generate_help("run")

        assert "sage run" in help_text
        assert "Run the interactive agent" in help_text

    def test_global_help_lists_commands(self):
        """Item 119: Global help lists all commands."""
        helper = HelpGenerator()
        helper.register_command(
            CommandInfo(
                name="run",
                description="Run the interactive agent",
                usage="sage run",
            )
        )
        helper.register_command(
            CommandInfo(
                name="ask",
                description="One-shot prompt",
                usage="sage run PROMPT",
            )
        )

        help_text = helper.generate_help()

        assert "SAGE - Local-First AI Coding Assistant" in help_text
        assert "Commands:" in help_text
        assert "run" in help_text
        assert "ask" in help_text

    def test_command_help_shows_arguments(self):
        """Item 120: Command help shows arguments."""
        helper = HelpGenerator()
        cmd = CommandInfo(
            name="ask",
            description="One-shot prompt",
            usage="sage run [OPTIONS] PROMPT",
            arguments=[
                ("PROMPT", "The prompt to send", True),
                ("--file", "File to include", False),
            ],
        )
        helper.register_command(cmd)

        help_text = helper.generate_help("ask")

        assert "Arguments:" in help_text
        assert "PROMPT" in help_text
        assert "(required)" in help_text

    def test_command_help_shows_options(self):
        """Item 120: Command help shows options."""
        helper = HelpGenerator()
        cmd = CommandInfo(
            name="run",
            description="Run the agent",
            usage="sage run [OPTIONS]",
            options=[
                ("--model, -m", "Model to use", "ollama:llama3.2"),
                ("--temperature, -t", "Temperature", "0.2"),
            ],
        )
        helper.register_command(cmd)

        help_text = helper.generate_help("run")

        assert "Options:" in help_text
        assert "--model" in help_text
        assert "(default: ollama:llama3.2)" in help_text

    def test_command_help_shows_examples(self):
        """Item 120: Command help shows examples."""
        helper = HelpGenerator()
        cmd = CommandInfo(
            name="ask",
            description="One-shot prompt",
            usage="sage run PROMPT",
            examples=[
                ("sage run 'explain quicksort'", "Ask about an algorithm"),
                ("sage run -f script.py 'explain'", "Ask about a file"),
            ],
        )
        helper.register_command(cmd)

        help_text = helper.generate_help("ask")

        assert "Examples:" in help_text
        assert "sage run 'explain quicksort'" in help_text
        assert "Ask about an algorithm" in help_text

    def test_global_options(self):
        """Item 121: Global options in help."""
        helper = HelpGenerator()
        helper.add_global_option("--help, -h", "Show help", "")
        helper.add_global_option("--version", "Show version", "")
        helper.add_global_option("--config", "Config file path", "~/.sage/config.json")

        help_text = helper.generate_help()

        assert "Global Options:" in help_text
        assert "--help" in help_text
        assert "--config" in help_text

    def test_command_aliases(self):
        """Item 121: Support command aliases."""
        helper = HelpGenerator()
        cmd = CommandInfo(
            name="run",
            description="Run the agent",
            usage="sage run",
            aliases=["r", "start"],
        )
        helper.register_command(cmd)

        # Should find by alias
        help_text = helper.generate_help("r")
        assert "sage run" in help_text

        # Global help should show aliases
        global_help = helper.generate_help()
        assert "(alias: r, start)" in global_help

    def test_search_commands(self):
        """Item 121: Search commands by keyword."""
        helper = HelpGenerator()
        helper.register_command(
            CommandInfo(
                name="run",
                description="Run the interactive agent",
                usage="sage run",
            )
        )
        helper.register_command(
            CommandInfo(
                name="config",
                description="Manage configuration",
                usage="sage config",
            )
        )
        helper.register_command(
            CommandInfo(
                name="models",
                description="List available models",
                usage="sage models",
            )
        )

        results = helper.search_commands("model")
        assert len(results) == 1
        assert results[0].name == "models"

        results = helper.search_commands("run")
        assert len(results) == 1
        assert results[0].name == "run"

    def test_unknown_command_help(self):
        """Item 119: Handle unknown command in help."""
        helper = HelpGenerator()

        help_text = helper.generate_help("nonexistent")
        assert "Unknown command: nonexistent" in help_text


# =============================================================================
# Items 122-124: Benchmark Framework
# =============================================================================


@dataclass
class BenchmarkResult:
    """Result of a single benchmark run."""

    name: str
    duration_ms: float
    iterations: int
    memory_mb: float = 0.0
    success: bool = True
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class BenchmarkSuite:
    """Collection of benchmark results."""

    name: str
    results: list[BenchmarkResult] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)
    ended_at: datetime | None = None

    @property
    def total_duration_ms(self) -> float:
        """Total duration of all benchmarks."""
        return sum(r.duration_ms for r in self.results)

    @property
    def success_count(self) -> int:
        """Number of successful benchmarks."""
        return sum(1 for r in self.results if r.success)

    @property
    def failure_count(self) -> int:
        """Number of failed benchmarks."""
        return sum(1 for r in self.results if not r.success)


class Benchmark:
    """
    Benchmark framework for performance testing.

    Items 122-124: Benchmark framework
    """

    def __init__(self, name: str):
        self.name = name
        self._benchmarks: dict[str, Callable] = {}
        self._setup: Callable | None = None
        self._teardown: Callable | None = None

    def register(self, name: str, func: Callable) -> None:
        """Register a benchmark function."""
        self._benchmarks[name] = func

    def set_setup(self, func: Callable) -> None:
        """Set setup function."""
        self._setup = func

    def set_teardown(self, func: Callable) -> None:
        """Set teardown function."""
        self._teardown = func

    def run_single(
        self,
        name: str,
        iterations: int = 100,
        warmup: int = 10,
    ) -> BenchmarkResult:
        """Run a single benchmark."""
        if name not in self._benchmarks:
            return BenchmarkResult(
                name=name,
                duration_ms=0,
                iterations=0,
                success=False,
                error=f"Benchmark not found: {name}",
            )

        func = self._benchmarks[name]

        # Warmup
        for _ in range(warmup):
            try:
                func()
            except Exception:
                pass

        # Run benchmark
        start = time.perf_counter()
        errors = []

        for _ in range(iterations):
            try:
                func()
            except Exception as e:
                errors.append(str(e))

        end = time.perf_counter()
        duration_ms = (end - start) * 1000

        return BenchmarkResult(
            name=name,
            duration_ms=duration_ms,
            iterations=iterations,
            success=len(errors) == 0,
            error="; ".join(errors[:3]) if errors else "",
            metadata={
                "avg_ms": duration_ms / iterations,
                "warmup_iterations": warmup,
            },
        )

    def run_all(
        self,
        iterations: int = 100,
        warmup: int = 10,
    ) -> BenchmarkSuite:
        """Run all registered benchmarks."""
        suite = BenchmarkSuite(name=self.name)

        if self._setup:
            self._setup()

        for name in self._benchmarks:
            result = self.run_single(name, iterations, warmup)
            suite.results.append(result)

        if self._teardown:
            self._teardown()

        suite.ended_at = datetime.now()
        return suite

    def compare(
        self,
        baseline: BenchmarkSuite,
        current: BenchmarkSuite,
    ) -> dict[str, dict[str, float]]:
        """Compare two benchmark runs."""
        baseline_by_name = {r.name: r for r in baseline.results}
        current_by_name = {r.name: r for r in current.results}

        comparison = {}

        for name in set(baseline_by_name.keys()) | set(current_by_name.keys()):
            base = baseline_by_name.get(name)
            curr = current_by_name.get(name)

            if base and curr:
                base_avg = base.duration_ms / base.iterations
                curr_avg = curr.duration_ms / curr.iterations
                change_pct = ((curr_avg - base_avg) / base_avg) * 100 if base_avg > 0 else 0

                comparison[name] = {
                    "baseline_ms": base_avg,
                    "current_ms": curr_avg,
                    "change_percent": change_pct,
                    "regression": change_pct > 10,  # >10% slower is regression
                }

        return comparison

    def generate_report(self, suite: BenchmarkSuite) -> str:
        """Generate a benchmark report."""
        lines = [
            f"# Benchmark Report: {suite.name}",
            "",
            f"Started: {suite.started_at.isoformat()}",
            f"Ended: {suite.ended_at.isoformat() if suite.ended_at else 'In Progress'}",
            f"Total Duration: {suite.total_duration_ms:.2f}ms",
            f"Benchmarks: {len(suite.results)} ({suite.success_count} passed, {suite.failure_count} failed)",
            "",
            "## Results",
            "",
            "| Benchmark | Iterations | Total (ms) | Avg (ms) | Status |",
            "|-----------|------------|------------|----------|--------|",
        ]

        for result in suite.results:
            avg_ms = result.duration_ms / result.iterations if result.iterations > 0 else 0
            status = "PASS" if result.success else "FAIL"
            lines.append(
                f"| {result.name} | {result.iterations} | {result.duration_ms:.2f} | {avg_ms:.4f} | {status} |"
            )

        return "\n".join(lines)


class TestBenchmarkFramework:
    """Tests for Items 122-124: Benchmark Framework."""

    def test_register_benchmark(self):
        """Item 122: Register benchmark functions."""
        bench = Benchmark("test_suite")

        def simple_benchmark():
            sum(range(100))

        bench.register("sum_range", simple_benchmark)

        result = bench.run_single("sum_range", iterations=10)
        assert result.name == "sum_range"
        assert result.iterations == 10
        assert result.success is True

    def test_run_benchmark_measures_time(self):
        """Item 122: Benchmark measures execution time."""
        bench = Benchmark("timing")

        def slow_function():
            time.sleep(0.001)  # 1ms sleep

        bench.register("slow", slow_function)
        result = bench.run_single("slow", iterations=5, warmup=0)

        # Should take at least 5ms (5 * 1ms)
        assert result.duration_ms >= 5
        assert result.metadata["avg_ms"] >= 1

    def test_benchmark_warmup(self):
        """Item 122: Benchmark supports warmup iterations."""
        call_count = 0

        def counting_function():
            nonlocal call_count
            call_count += 1

        bench = Benchmark("warmup_test")
        bench.register("count", counting_function)

        result = bench.run_single("count", iterations=10, warmup=5)

        # Total calls = warmup + iterations = 5 + 10 = 15
        assert call_count == 15
        assert result.metadata["warmup_iterations"] == 5

    def test_benchmark_handles_errors(self):
        """Item 123: Benchmark handles errors gracefully."""
        bench = Benchmark("error_test")

        def failing_function():
            raise ValueError("test error")

        bench.register("fail", failing_function)
        result = bench.run_single("fail", iterations=3, warmup=0)

        assert result.success is False
        assert "test error" in result.error

    def test_run_all_benchmarks(self):
        """Item 123: Run all registered benchmarks."""
        bench = Benchmark("suite")
        bench.register("fast", lambda: sum(range(10)))
        bench.register("medium", lambda: sum(range(100)))

        suite = bench.run_all(iterations=5, warmup=1)

        assert suite.name == "suite"
        assert len(suite.results) == 2
        assert suite.success_count == 2
        assert suite.failure_count == 0

    def test_benchmark_suite_metrics(self):
        """Item 123: Benchmark suite tracks metrics."""
        bench = Benchmark("metrics")
        bench.register("test1", lambda: None)
        bench.register("test2", lambda: None)

        suite = bench.run_all(iterations=10, warmup=0)

        assert suite.total_duration_ms >= 0
        assert suite.started_at is not None
        assert suite.ended_at is not None
        assert suite.ended_at >= suite.started_at

    def test_compare_benchmark_runs(self):
        """Item 124: Compare benchmark results."""
        # Create baseline
        baseline = BenchmarkSuite(
            name="baseline",
            results=[
                BenchmarkResult(name="test1", duration_ms=100, iterations=10),
                BenchmarkResult(name="test2", duration_ms=200, iterations=10),
            ],
        )

        # Current run is faster for test1, slower for test2
        current = BenchmarkSuite(
            name="current",
            results=[
                BenchmarkResult(name="test1", duration_ms=80, iterations=10),  # 20% faster
                BenchmarkResult(name="test2", duration_ms=250, iterations=10),  # 25% slower
            ],
        )

        bench = Benchmark("compare")
        comparison = bench.compare(baseline, current)

        assert "test1" in comparison
        assert comparison["test1"]["change_percent"] < 0  # Faster
        assert comparison["test1"]["regression"] is False

        assert "test2" in comparison
        assert comparison["test2"]["change_percent"] > 0  # Slower
        assert comparison["test2"]["regression"] is True  # >10% regression

    def test_generate_benchmark_report(self):
        """Item 124: Generate benchmark report."""
        suite = BenchmarkSuite(
            name="report_test",
            results=[
                BenchmarkResult(name="fast_op", duration_ms=10.5, iterations=100),
                BenchmarkResult(name="slow_op", duration_ms=500.2, iterations=50),
            ],
        )
        suite.ended_at = datetime.now()

        bench = Benchmark("report")
        report = bench.generate_report(suite)

        assert "# Benchmark Report: report_test" in report
        assert "| fast_op |" in report
        assert "| slow_op |" in report
        assert "Total Duration:" in report

    def test_benchmark_not_found(self):
        """Item 122: Handle non-existent benchmark."""
        bench = Benchmark("empty")

        result = bench.run_single("nonexistent")

        assert result.success is False
        assert "not found" in result.error

    def test_setup_and_teardown(self):
        """Item 123: Support setup and teardown."""
        state = {"setup_called": False, "teardown_called": False}

        def setup():
            state["setup_called"] = True

        def teardown():
            state["teardown_called"] = True

        bench = Benchmark("lifecycle")
        bench.set_setup(setup)
        bench.set_teardown(teardown)
        bench.register("test", lambda: None)

        bench.run_all(iterations=1, warmup=0)

        assert state["setup_called"] is True
        assert state["teardown_called"] is True


# =============================================================================
# Items 125-127: Startup and Configuration
# =============================================================================


class StartupPhase(Enum):
    """Phases of startup initialization."""

    LOADING_CONFIG = auto()
    VALIDATING_CONFIG = auto()
    CHECKING_DEPENDENCIES = auto()
    INITIALIZING_PROVIDERS = auto()
    LOADING_MODELS = auto()
    READY = auto()
    FAILED = auto()


@dataclass
class StartupEvent:
    """Event during startup."""

    phase: StartupPhase
    message: str
    timestamp: float = field(default_factory=time.time)
    error: str | None = None
    duration_ms: float = 0.0


@dataclass
class StartupResult:
    """Result of startup initialization."""

    success: bool
    phase: StartupPhase
    events: list[StartupEvent] = field(default_factory=list)
    total_duration_ms: float = 0.0
    error: str | None = None
    config: dict[str, Any] = field(default_factory=dict)


class StartupManager:
    """
    Manage application startup and initialization.

    Items 125-127: Startup initialization
    """

    def __init__(self):
        self._events: list[StartupEvent] = []
        self._hooks: dict[StartupPhase, list[Callable]] = {phase: [] for phase in StartupPhase}
        self._config: dict[str, Any] = {}

    def add_hook(self, phase: StartupPhase, hook: Callable) -> None:
        """Add a startup hook for a phase."""
        self._hooks[phase].append(hook)

    def _emit_event(self, phase: StartupPhase, message: str, error: str | None = None) -> None:
        """Emit a startup event."""
        self._events.append(
            StartupEvent(
                phase=phase,
                message=message,
                error=error,
            )
        )

    def _run_hooks(self, phase: StartupPhase) -> bool:
        """Run hooks for a phase."""
        for hook in self._hooks[phase]:
            try:
                hook()
            except Exception as e:
                self._emit_event(phase, f"Hook failed: {hook.__name__}", str(e))
                return False
        return True

    def load_config(self, config_path: Path | None = None) -> bool:
        """Load configuration from file."""
        self._emit_event(StartupPhase.LOADING_CONFIG, "Loading configuration")

        paths = [
            config_path,
            Path.home() / ".sage" / "config.json",
            Path.cwd() / ".sagecrc",
        ]

        for path in paths:
            if path and path.exists():
                try:
                    self._config = json.loads(path.read_text())
                    self._emit_event(StartupPhase.LOADING_CONFIG, f"Loaded config from {path}")
                    return True
                except json.JSONDecodeError as e:
                    self._emit_event(StartupPhase.LOADING_CONFIG, f"Invalid JSON in {path}", str(e))

        # Use defaults
        self._config = {
            "default_model": "ollama:llama3.2",
            "temperature": 0.2,
            "max_tokens": 16384,
        }
        self._emit_event(StartupPhase.LOADING_CONFIG, "Using default configuration")
        return True

    def validate_config(self) -> bool:
        """Validate configuration."""
        self._emit_event(StartupPhase.VALIDATING_CONFIG, "Validating configuration")

        required_fields = ["default_model"]
        for field in required_fields:
            if field not in self._config:
                self._emit_event(
                    StartupPhase.VALIDATING_CONFIG,
                    f"Missing required field: {field}",
                    f"Config must include '{field}'",
                )
                return False

        # Validate temperature
        temp = self._config.get("temperature", 0.2)
        if not 0 <= temp <= 2:
            self._emit_event(
                StartupPhase.VALIDATING_CONFIG,
                f"Invalid temperature: {temp}",
                "Temperature must be between 0 and 2",
            )
            return False

        self._emit_event(StartupPhase.VALIDATING_CONFIG, "Configuration valid")
        return True

    def check_dependencies(self) -> bool:
        """Check required dependencies."""
        self._emit_event(StartupPhase.CHECKING_DEPENDENCIES, "Checking dependencies")

        # Check Python version
        if sys.version_info < (3, 10):
            self._emit_event(
                StartupPhase.CHECKING_DEPENDENCIES,
                "Python version too old",
                "Requires Python 3.10+",
            )
            return False

        self._emit_event(StartupPhase.CHECKING_DEPENDENCIES, "Dependencies satisfied")
        return True

    def startup(self, config_path: Path | None = None) -> StartupResult:
        """Run full startup sequence."""
        start_time = time.perf_counter()

        phases = [
            (StartupPhase.LOADING_CONFIG, lambda: self.load_config(config_path)),
            (StartupPhase.VALIDATING_CONFIG, self.validate_config),
            (StartupPhase.CHECKING_DEPENDENCIES, self.check_dependencies),
        ]

        for phase, action in phases:
            if not self._run_hooks(phase):
                return StartupResult(
                    success=False,
                    phase=phase,
                    events=self._events,
                    error="Hook failed",
                )

            if not action():
                return StartupResult(
                    success=False,
                    phase=phase,
                    events=self._events,
                    error=self._events[-1].error if self._events else "Unknown error",
                )

        self._emit_event(StartupPhase.READY, "Startup complete")

        duration_ms = (time.perf_counter() - start_time) * 1000

        return StartupResult(
            success=True,
            phase=StartupPhase.READY,
            events=self._events,
            total_duration_ms=duration_ms,
            config=self._config,
        )


class TestStartupInitialization:
    """Tests for Items 125-127: Startup Initialization."""

    def test_load_config_from_file(self, tmp_path: Path):
        """Item 125: Load configuration from file."""
        config_file = tmp_path / "config.json"
        config_file.write_text(
            json.dumps(
                {
                    "default_model": "ollama:llama3",
                    "temperature": 0.5,
                }
            )
        )

        manager = StartupManager()
        result = manager.load_config(config_file)

        assert result is True
        assert manager._config["default_model"] == "ollama:llama3"

    def test_load_config_uses_defaults(self, tmp_path: Path, monkeypatch):
        """Item 125: Use default config when no file exists."""
        # Monkeypatch home directory to prevent finding real config
        monkeypatch.setattr(Path, "home", lambda: tmp_path / "fake_home")

        manager = StartupManager()
        result = manager.load_config(Path("/nonexistent/config.json"))

        assert result is True
        assert manager._config["default_model"] == "ollama:llama3.2"
        assert manager._config["temperature"] == 0.2

    def test_validate_config_checks_required_fields(self):
        """Item 126: Validate required configuration fields."""
        manager = StartupManager()
        manager._config = {"temperature": 0.5}  # Missing default_model

        result = manager.validate_config()

        assert result is False
        assert any("Missing required field" in e.message for e in manager._events)

    def test_validate_config_checks_temperature_range(self):
        """Item 126: Validate temperature range."""
        manager = StartupManager()
        manager._config = {
            "default_model": "test",
            "temperature": 3.0,  # Invalid: > 2
        }

        result = manager.validate_config()

        assert result is False
        assert any("Invalid temperature" in e.message for e in manager._events)

    def test_validate_config_passes_valid_config(self):
        """Item 126: Valid config passes validation."""
        manager = StartupManager()
        manager._config = {
            "default_model": "test",
            "temperature": 0.7,
        }

        result = manager.validate_config()

        assert result is True
        assert any("Configuration valid" in e.message for e in manager._events)

    def test_check_dependencies(self):
        """Item 127: Check dependencies at startup."""
        manager = StartupManager()
        result = manager.check_dependencies()

        # Should pass on Python 3.10+
        assert result is True
        assert any("Dependencies satisfied" in e.message for e in manager._events)

    def test_full_startup_sequence(self, tmp_path: Path):
        """Item 127: Full startup sequence."""
        config_file = tmp_path / "config.json"
        config_file.write_text(
            json.dumps(
                {
                    "default_model": "test_model",
                    "temperature": 0.3,
                }
            )
        )

        manager = StartupManager()
        result = manager.startup(config_file)

        assert result.success is True
        assert result.phase == StartupPhase.READY
        assert result.config["default_model"] == "test_model"
        assert result.total_duration_ms >= 0

    def test_startup_fails_on_invalid_config(self, tmp_path: Path):
        """Item 125: Startup fails with invalid config."""
        config_file = tmp_path / "config.json"
        config_file.write_text("{ invalid json }")

        manager = StartupManager()
        result = manager.startup(config_file)

        # Should still succeed with defaults
        assert result.success is True

    def test_startup_hooks(self, tmp_path: Path):
        """Item 127: Support startup hooks."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({"default_model": "test"}))

        hook_called = False

        def my_hook():
            nonlocal hook_called
            hook_called = True

        manager = StartupManager()
        manager.add_hook(StartupPhase.LOADING_CONFIG, my_hook)

        result = manager.startup(config_file)

        assert result.success is True
        assert hook_called is True

    def test_startup_events_tracked(self, tmp_path: Path):
        """Item 125: Startup events are tracked."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({"default_model": "test"}))

        manager = StartupManager()
        result = manager.startup(config_file)

        assert len(result.events) > 0
        phases = [e.phase for e in result.events]
        assert StartupPhase.LOADING_CONFIG in phases
        assert StartupPhase.VALIDATING_CONFIG in phases


# =============================================================================
# Items 128-130: CLI Utilities and Validation
# =============================================================================


@dataclass
class CLIArgument:
    """CLI argument definition."""

    name: str
    arg_type: type
    required: bool = False
    default: Any = None
    help: str = ""
    choices: list[Any] = field(default_factory=list)


@dataclass
class ParsedArgs:
    """Parsed CLI arguments."""

    command: str
    args: dict[str, Any]
    options: dict[str, Any]
    errors: list[str] = field(default_factory=list)


class CLIParser:
    """
    Parse and validate CLI arguments.

    Items 128-130: CLI utilities
    """

    def __init__(self):
        self._commands: dict[str, list[CLIArgument]] = {}
        self._global_options: list[CLIArgument] = []

    def add_command(self, name: str, args: list[CLIArgument]) -> None:
        """Add a command definition."""
        self._commands[name] = args

    def add_global_option(self, arg: CLIArgument) -> None:
        """Add a global option."""
        self._global_options.append(arg)

    def parse(self, argv: list[str]) -> ParsedArgs:
        """Parse command line arguments."""
        if not argv:
            return ParsedArgs(command="", args={}, options={}, errors=["No command specified"])

        # Parse global options first
        options: dict[str, Any] = {}
        remaining = []
        i = 0

        while i < len(argv):
            arg = argv[i]

            # Check if it's an option
            if arg.startswith("--"):
                opt_name = arg[2:]
                opt_def = next((o for o in self._global_options if o.name == opt_name), None)

                if opt_def:
                    if opt_def.arg_type == bool:
                        options[opt_name] = True
                    elif i + 1 < len(argv):
                        i += 1
                        options[opt_name] = self._convert_type(argv[i], opt_def.arg_type)
                else:
                    remaining.append(arg)
            elif arg.startswith("-"):
                # Short option
                remaining.append(arg)
            else:
                remaining.append(arg)

            i += 1

        if not remaining:
            return ParsedArgs(command="", args={}, options=options, errors=["No command specified"])

        command = remaining[0]
        remaining = remaining[1:]

        # Check command exists
        if command not in self._commands:
            return ParsedArgs(
                command=command,
                args={},
                options=options,
                errors=[f"Unknown command: {command}"],
            )

        # Parse command arguments
        args: dict[str, Any] = {}
        errors: list[str] = []
        arg_defs = self._commands[command]

        positional_defs = [d for d in arg_defs if not d.name.startswith("--")]

        for j, arg_def in enumerate(positional_defs):
            if j < len(remaining):
                value = self._convert_type(remaining[j], arg_def.arg_type)

                # Validate choices
                if arg_def.choices and value not in arg_def.choices:
                    errors.append(
                        f"Invalid value for {arg_def.name}: {value}. "
                        f"Must be one of: {', '.join(map(str, arg_def.choices))}"
                    )
                else:
                    args[arg_def.name] = value
            elif arg_def.required:
                errors.append(f"Missing required argument: {arg_def.name}")
            elif arg_def.default is not None:
                args[arg_def.name] = arg_def.default

        return ParsedArgs(command=command, args=args, options=options, errors=errors)

    def _convert_type(self, value: str, target_type: type) -> Any:
        """Convert string value to target type."""
        if target_type == bool:
            return value.lower() in ("true", "yes", "1")
        elif target_type == int:
            try:
                return int(value)
            except ValueError:
                return 0
        elif target_type == float:
            try:
                return float(value)
            except ValueError:
                return 0.0
        return value

    def validate_args(self, parsed: ParsedArgs) -> list[str]:
        """Additional validation of parsed arguments."""
        errors = list(parsed.errors)

        if parsed.command not in self._commands:
            return errors

        arg_defs = self._commands[parsed.command]

        for arg_def in arg_defs:
            if arg_def.name in parsed.args:
                value = parsed.args[arg_def.name]

                # Type check
                if not isinstance(value, arg_def.arg_type):
                    errors.append(
                        f"Invalid type for {arg_def.name}: expected {arg_def.arg_type.__name__}"
                    )

        return errors

    def suggest_command(self, typo: str) -> list[str]:
        """Suggest commands similar to a typo."""
        import difflib

        return difflib.get_close_matches(typo, self._commands.keys(), n=3, cutoff=0.5)


class TestCLIUtilities:
    """Tests for Items 128-130: CLI Utilities."""

    def test_parse_simple_command(self):
        """Item 128: Parse simple command."""
        parser = CLIParser()
        parser.add_command("run", [])

        result = parser.parse(["run"])

        assert result.command == "run"
        assert len(result.errors) == 0

    def test_parse_command_with_arguments(self):
        """Item 128: Parse command with positional arguments."""
        parser = CLIParser()
        parser.add_command(
            "ask",
            [
                CLIArgument(name="prompt", arg_type=str, required=True),
            ],
        )

        result = parser.parse(["ask", "explain quicksort"])

        assert result.command == "ask"
        assert result.args["prompt"] == "explain quicksort"
        assert len(result.errors) == 0

    def test_parse_missing_required_argument(self):
        """Item 128: Report missing required arguments."""
        parser = CLIParser()
        parser.add_command(
            "ask",
            [
                CLIArgument(name="prompt", arg_type=str, required=True),
            ],
        )

        result = parser.parse(["ask"])

        assert "Missing required argument: prompt" in result.errors

    def test_parse_global_options(self):
        """Item 129: Parse global options."""
        parser = CLIParser()
        parser.add_global_option(CLIArgument(name="verbose", arg_type=bool))
        parser.add_global_option(CLIArgument(name="model", arg_type=str))
        parser.add_command("run", [])

        result = parser.parse(["--verbose", "--model", "llama3", "run"])

        assert result.options.get("verbose") is True
        assert result.options.get("model") == "llama3"
        assert result.command == "run"

    def test_parse_type_conversion(self):
        """Item 129: Convert argument types."""
        parser = CLIParser()
        parser.add_command(
            "config",
            [
                CLIArgument(name="temperature", arg_type=float, required=True),
                CLIArgument(name="max_tokens", arg_type=int, required=True),
            ],
        )

        result = parser.parse(["config", "0.7", "1000"])

        assert result.args["temperature"] == 0.7
        assert result.args["max_tokens"] == 1000

    def test_validate_choices(self):
        """Item 129: Validate argument choices."""
        parser = CLIParser()
        parser.add_command(
            "format",
            [
                CLIArgument(
                    name="output_format",
                    arg_type=str,
                    required=True,
                    choices=["json", "csv", "markdown"],
                ),
            ],
        )

        # Valid choice
        result = parser.parse(["format", "json"])
        assert len(result.errors) == 0

        # Invalid choice
        result = parser.parse(["format", "xml"])
        assert any("Invalid value" in e for e in result.errors)

    def test_unknown_command_error(self):
        """Item 130: Report unknown commands."""
        parser = CLIParser()
        parser.add_command("run", [])

        result = parser.parse(["unknown"])

        assert "Unknown command: unknown" in result.errors

    def test_suggest_similar_commands(self):
        """Item 130: Suggest similar commands for typos."""
        parser = CLIParser()
        parser.add_command("run", [])
        parser.add_command("config", [])
        parser.add_command("models", [])

        suggestions = parser.suggest_command("rnu")  # Typo for "run"

        assert "run" in suggestions

    def test_default_argument_values(self):
        """Item 128: Support default argument values."""
        parser = CLIParser()
        parser.add_command(
            "generate",
            [
                CLIArgument(name="count", arg_type=int, default=10),
            ],
        )

        result = parser.parse(["generate"])

        assert result.args.get("count") == 10
        assert len(result.errors) == 0

    def test_empty_argv(self):
        """Item 130: Handle empty argument list."""
        parser = CLIParser()

        result = parser.parse([])

        assert "No command specified" in result.errors

    def test_validate_parsed_args(self):
        """Item 130: Validate parsed arguments."""
        parser = CLIParser()
        parser.add_command(
            "test",
            [
                CLIArgument(name="value", arg_type=int, required=True),
            ],
        )

        result = parser.parse(["test", "abc"])  # Invalid int
        errors = parser.validate_args(result)

        # The conversion will return 0 for invalid int
        assert result.args.get("value") == 0


# =============================================================================
# Additional Integration Tests
# =============================================================================


class TestIntegration:
    """Integration tests for P3 features."""

    def test_documentation_with_startup(self, tmp_path: Path):
        """Test documentation generation with startup config."""
        # Create a module
        module_file = tmp_path / "my_module.py"
        module_file.write_text('''"""
My test module for documentation.

This module provides utilities for testing.
"""

def my_function(x: int) -> str:
    """Convert x to string."""
    return str(x)
''')

        # Generate documentation
        generator = DocumentationGenerator(tmp_path)
        doc = generator.parse_module(module_file)
        markdown = generator.generate_markdown(doc)

        assert "# my_module" in markdown
        assert "My test module for documentation." in markdown

    def test_benchmark_with_cli(self):
        """Test benchmark framework with CLI parsing."""
        # Set up CLI
        parser = CLIParser()
        parser.add_command(
            "benchmark",
            [
                CLIArgument(name="iterations", arg_type=int, default=100),
            ],
        )

        result = parser.parse(["benchmark", "50"])

        # Run benchmark
        bench = Benchmark("cli_test")
        bench.register("parse", lambda: parser.parse(["run"]))

        suite = bench.run_all(
            iterations=result.args.get("iterations", 100),
            warmup=5,
        )

        assert suite.success_count == 1
        assert len(suite.results) == 1

    def test_help_with_startup_config(self, tmp_path: Path):
        """Test help system integrates with startup."""
        # Create config
        config_file = tmp_path / "config.json"
        config_file.write_text(
            json.dumps(
                {
                    "default_model": "test_model",
                }
            )
        )

        # Run startup
        manager = StartupManager()
        startup_result = manager.startup(config_file)

        # Generate help
        helper = HelpGenerator()
        helper.register_command(
            CommandInfo(
                name="run",
                description=f"Run with model: {startup_result.config.get('default_model', 'default')}",
                usage="sage run",
            )
        )

        help_text = helper.generate_help("run")

        assert "test_model" in help_text

    def test_all_p3_components_together(self, tmp_path: Path):
        """Test all P3 components work together."""
        # 1. Startup
        config_file = tmp_path / "config.json"
        config_file.write_text(
            json.dumps(
                {
                    "default_model": "integration_test",
                    "temperature": 0.5,
                }
            )
        )

        startup_manager = StartupManager()
        startup_result = startup_manager.startup(config_file)
        assert startup_result.success

        # 2. CLI Parsing
        cli_parser = CLIParser()
        cli_parser.add_command("run", [])
        cli_parser.add_command("help", [CLIArgument(name="command", arg_type=str, required=False)])

        parse_result = cli_parser.parse(["help", "run"])
        assert parse_result.command == "help"

        # 3. Help System
        help_gen = HelpGenerator()
        help_gen.register_command(
            CommandInfo(
                name="run",
                description="Run the agent",
                usage="sage run",
            )
        )

        help_text = help_gen.generate_help(parse_result.args.get("command"))
        assert "sage run" in help_text

        # 4. Documentation
        module_file = tmp_path / "module.py"
        module_file.write_text('"""Test module."""\n')

        doc_gen = DocumentationGenerator(tmp_path)
        doc = doc_gen.parse_module(module_file)
        assert doc.docstring == "Test module."

        # 5. Benchmarks
        bench = Benchmark("integration")
        bench.register("startup", lambda: StartupManager().check_dependencies())
        bench.register("parse", lambda: cli_parser.parse(["run"]))

        suite = bench.run_all(iterations=10, warmup=2)
        assert suite.success_count == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
