"""Enhanced Code Generation System for SAGE.

This module provides intelligent code generation with:
- Deep context awareness
- Pattern detection and reuse
- Code quality validation
- Auto-completion and suggestions
- Style consistency enforcement
"""

from __future__ import annotations

import ast
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class CodeContext:
    """Context information for code generation."""

    file_path: str
    language: str
    existing_content: str | None = None
    imports: list[str] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)
    functions: list[str] = field(default_factory=list)
    variables: list[str] = field(default_factory=list)
    style_guide: dict[str, Any] = field(default_factory=dict)
    dependencies: list[str] = field(default_factory=list)
    related_files: list[str] = field(default_factory=list)


@dataclass
class CodePattern:
    """A detected code pattern in the codebase."""

    name: str
    pattern_type: str  # naming, structure, error_handling, testing, etc.
    example: str
    frequency: int = 1
    files: list[str] = field(default_factory=list)


@dataclass
class CodeSuggestion:
    """A code suggestion or completion."""

    code: str
    description: str
    confidence: float = 0.5
    source: str = "inference"  # inference, pattern, template, ai


@dataclass
class ValidationResult:
    """Result of code validation."""

    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


class CodeAnalyzer:
    """Analyzes code to extract context and patterns."""

    LANGUAGE_EXTENSIONS = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".jsx": "javascript",
        ".tsx": "typescript",
        ".go": "go",
        ".rs": "rust",
        ".java": "java",
        ".rb": "ruby",
        ".php": "php",
        ".c": "c",
        ".cpp": "cpp",
        ".h": "c",
        ".hpp": "cpp",
    }

    def __init__(self, cwd: Path):
        self.cwd = cwd
        self._pattern_cache: dict[str, list[CodePattern]] = {}
        self._context_cache: dict[str, CodeContext] = {}

    def detect_language(self, file_path: str) -> str:
        """Detect the programming language from file extension."""
        ext = Path(file_path).suffix.lower()
        return self.LANGUAGE_EXTENSIONS.get(ext, "unknown")

    def analyze_file(self, file_path: str) -> CodeContext:
        """Analyze a file and extract context."""
        # Check cache
        cache_key = file_path
        if cache_key in self._context_cache:
            return self._context_cache[cache_key]

        full_path = self.cwd / file_path
        language = self.detect_language(file_path)

        context = CodeContext(
            file_path=file_path,
            language=language,
        )

        if not full_path.exists():
            return context

        try:
            content = full_path.read_text(encoding="utf-8", errors="replace")
            context.existing_content = content

            if language == "python":
                context = self._analyze_python(context, content)
            elif language in ("javascript", "typescript"):
                context = self._analyze_javascript(context, content)
            elif language == "go":
                context = self._analyze_go(context, content)

            # Find related files
            context.related_files = self._find_related_files(file_path)

            self._context_cache[cache_key] = context

        except Exception:
            pass

        return context

    def _analyze_python(self, context: CodeContext, content: str) -> CodeContext:
        """Analyze Python code."""
        # Extract imports
        import_pattern = r"^(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))"
        for match in re.finditer(import_pattern, content, re.MULTILINE):
            module = match.group(1) or match.group(2)
            if module:
                context.imports.append(module.split(".")[0])

        # Parse AST for more detailed analysis
        try:
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    context.classes.append(node.name)
                elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                    context.functions.append(node.name)
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            context.variables.append(target.id)

        except SyntaxError:
            pass

        # Detect style patterns
        context.style_guide = self._detect_python_style(content)

        return context

    def _analyze_javascript(self, context: CodeContext, content: str) -> CodeContext:
        """Analyze JavaScript/TypeScript code."""
        # Extract imports
        import_patterns = [
            r"import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]",
            r"require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
        ]
        for pattern in import_patterns:
            for match in re.finditer(pattern, content):
                context.imports.append(match.group(1))

        # Extract functions
        func_patterns = [
            r"(?:function|const|let|var)\s+(\w+)\s*(?:=\s*(?:async\s+)?\(?|(?:async\s+)?function)",
            r"(\w+)\s*:\s*(?:async\s+)?\([^)]*\)\s*=>",
        ]
        for pattern in func_patterns:
            for match in re.finditer(pattern, content):
                context.functions.append(match.group(1))

        # Extract classes
        class_pattern = r"class\s+(\w+)"
        for match in re.finditer(class_pattern, content):
            context.classes.append(match.group(1))

        return context

    def _analyze_go(self, context: CodeContext, content: str) -> CodeContext:
        """Analyze Go code."""
        # Extract imports
        import_pattern = r'import\s+(?:\(\s*([\s\S]*?)\s*\)|"([^"]+)")'
        for match in re.finditer(import_pattern, content):
            if match.group(1):
                # Multi-import
                for line in match.group(1).split("\n"):
                    if m := re.search(r'"([^"]+)"', line):
                        context.imports.append(m.group(1).split("/")[-1])
            elif match.group(2):
                context.imports.append(match.group(2).split("/")[-1])

        # Extract functions
        func_pattern = r"func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)\s*\("
        for match in re.finditer(func_pattern, content):
            context.functions.append(match.group(1))

        # Extract types/structs
        type_pattern = r"type\s+(\w+)\s+(?:struct|interface)"
        for match in re.finditer(type_pattern, content):
            context.classes.append(match.group(1))

        return context

    def _detect_python_style(self, content: str) -> dict[str, Any]:
        """Detect Python code style patterns."""
        style = {
            "indent": "spaces",
            "indent_size": 4,
            "quote_style": "double",
            "docstring_style": "google",
            "type_hints": False,
            "trailing_comma": False,
        }

        # Detect indentation
        indent_match = re.search(r"\n(\s+)\S", content)
        if indent_match:
            indent = indent_match.group(1)
            if "\t" in indent:
                style["indent"] = "tabs"
                style["indent_size"] = 1
            else:
                style["indent_size"] = len(indent)

        # Detect quote style
        double_count = content.count('"')
        single_count = content.count("'")
        style["quote_style"] = "double" if double_count >= single_count else "single"

        # Detect type hints
        style["type_hints"] = bool(re.search(r"def \w+\([^)]*:\s*\w+", content))

        # Detect trailing commas
        style["trailing_comma"] = bool(re.search(r",\s*\n\s*[\)\]\}]", content))

        return style

    def _find_related_files(self, file_path: str) -> list[str]:
        """Find files related to the given file."""
        related = []
        name = Path(file_path).stem
        parent = Path(file_path).parent

        # Find test files
        test_patterns = [
            f"test_{name}.py",
            f"{name}_test.py",
            f"tests/test_{name}.py",
            f"tests/{name}_test.py",
            f"__tests__/{name}.test.js",
            f"__tests__/{name}.test.ts",
            f"{name}.test.js",
            f"{name}.test.ts",
            f"{name}_test.go",
        ]

        for pattern in test_patterns:
            test_path = self.cwd / pattern
            if test_path.exists():
                related.append(str(test_path.relative_to(self.cwd)))

        # Find files in same directory
        if (self.cwd / parent).exists():
            for f in (self.cwd / parent).iterdir():
                if f.is_file() and f.suffix in self.LANGUAGE_EXTENSIONS:
                    rel_path = str(f.relative_to(self.cwd))
                    if rel_path != file_path and rel_path not in related:
                        related.append(rel_path)

        return related[:10]  # Limit to 10 related files

    def detect_patterns(self, files: list[str] | None = None) -> list[CodePattern]:
        """Detect code patterns across the codebase."""
        if files is None:
            files = []
            for ext in self.LANGUAGE_EXTENSIONS:
                files.extend(str(f.relative_to(self.cwd)) for f in self.cwd.rglob(f"*{ext}"))

        patterns: dict[str, CodePattern] = {}

        for file_path in files[:50]:  # Limit to 50 files
            context = self.analyze_file(file_path)
            if not context.existing_content:
                continue

            # Naming patterns
            self._detect_naming_patterns(context, patterns)

            # Error handling patterns
            self._detect_error_patterns(context, patterns)

            # Testing patterns
            if "test" in file_path.lower():
                self._detect_test_patterns(context, patterns)

        return list(patterns.values())

    def _detect_naming_patterns(
        self,
        context: CodeContext,
        patterns: dict[str, CodePattern],
    ) -> None:
        """Detect naming convention patterns."""
        # Function naming
        for func in context.functions:
            if func.startswith("_"):
                key = "private_prefix_underscore"
                if key not in patterns:
                    patterns[key] = CodePattern(
                        name="Private methods use underscore prefix",
                        pattern_type="naming",
                        example=f"def {func}(...)",
                    )
                patterns[key].frequency += 1
                if context.file_path not in patterns[key].files:
                    patterns[key].files.append(context.file_path)

            elif func.startswith("get_") or func.startswith("set_"):
                key = "getter_setter_prefix"
                if key not in patterns:
                    patterns[key] = CodePattern(
                        name="Getter/setter naming convention",
                        pattern_type="naming",
                        example=f"def {func}(...)",
                    )
                patterns[key].frequency += 1

        # Class naming
        for cls in context.classes:
            if cls[0].isupper():
                key = "pascal_case_classes"
                if key not in patterns:
                    patterns[key] = CodePattern(
                        name="Classes use PascalCase",
                        pattern_type="naming",
                        example=f"class {cls}:",
                    )
                patterns[key].frequency += 1

    def _detect_error_patterns(
        self,
        context: CodeContext,
        patterns: dict[str, CodePattern],
    ) -> None:
        """Detect error handling patterns."""
        content = context.existing_content or ""

        # Try/except patterns
        if "try:" in content:
            # Check for specific exception handling
            if re.search(r"except \w+Error", content):
                key = "specific_exceptions"
                if key not in patterns:
                    patterns[key] = CodePattern(
                        name="Use specific exception types",
                        pattern_type="error_handling",
                        example="except ValueError as e:",
                    )
                patterns[key].frequency += 1
                if context.file_path not in patterns[key].files:
                    patterns[key].files.append(context.file_path)

    def _detect_test_patterns(
        self,
        context: CodeContext,
        patterns: dict[str, CodePattern],
    ) -> None:
        """Detect testing patterns."""
        content = context.existing_content or ""

        # Pytest fixtures
        if "@pytest.fixture" in content:
            key = "pytest_fixtures"
            if key not in patterns:
                patterns[key] = CodePattern(
                    name="Use pytest fixtures for setup",
                    pattern_type="testing",
                    example="@pytest.fixture",
                )
            patterns[key].frequency += 1

        # Parameterized tests
        if "@pytest.mark.parametrize" in content:
            key = "parameterized_tests"
            if key not in patterns:
                patterns[key] = CodePattern(
                    name="Use parameterized tests",
                    pattern_type="testing",
                    example="@pytest.mark.parametrize('input,expected', [...])",
                )
            patterns[key].frequency += 1


class CodeGenerator:
    """Generates code with context awareness and pattern matching."""

    def __init__(
        self,
        cwd: Path,
        analyzer: CodeAnalyzer | None = None,
        send_fn: Callable[[str], str | None] | None = None,
    ):
        self.cwd = cwd
        self.analyzer = analyzer or CodeAnalyzer(cwd)
        self.send_fn = send_fn
        self.patterns: list[CodePattern] = []
        self._template_cache: dict[str, str] = {}

    def generate_with_context(
        self,
        task: str,
        target_file: str,
        related_context: list[str] | None = None,
    ) -> CodeSuggestion:
        """Generate code with full context awareness."""
        # Analyze target file context
        context = self.analyzer.analyze_file(target_file)

        # Gather related context
        related_contexts = []
        if related_context:
            for file_path in related_context:
                related_contexts.append(self.analyzer.analyze_file(file_path))
        elif context.related_files:
            for file_path in context.related_files[:5]:
                related_contexts.append(self.analyzer.analyze_file(file_path))

        # Build context-aware prompt
        prompt = self._build_generation_prompt(task, context, related_contexts)

        if self.send_fn:
            response = self.send_fn(prompt)
            if response:
                # Extract code from response
                code = self._extract_code_from_response(response, context.language)
                return CodeSuggestion(
                    code=code,
                    description=f"Generated code for: {task}",
                    confidence=0.7,
                    source="ai",
                )

        return CodeSuggestion(
            code="",
            description="Failed to generate code",
            confidence=0.0,
        )

    def _build_generation_prompt(
        self,
        task: str,
        context: CodeContext,
        related_contexts: list[CodeContext],
    ) -> str:
        """Build a context-aware prompt for code generation."""
        prompt_parts = [
            f"## Code Generation Task\n\n**Task:** {task}\n",
            f"\n**Target File:** {context.file_path}",
            f"**Language:** {context.language}\n",
        ]

        # Add existing file context
        if context.existing_content:
            prompt_parts.append(f"\n**Existing Code:**\n```{context.language}")
            # Truncate if too long
            existing = context.existing_content
            if len(existing) > 3000:
                existing = existing[:3000] + "\n... (truncated)"
            prompt_parts.append(f"{existing}\n```\n")

        # Add style guide
        if context.style_guide:
            prompt_parts.append("\n**Code Style to Follow:**")
            for key, value in context.style_guide.items():
                prompt_parts.append(f"- {key}: {value}")

        # Add related context
        if related_contexts:
            prompt_parts.append("\n**Related Files for Reference:**")
            for rc in related_contexts[:3]:
                if rc.existing_content:
                    prompt_parts.append(f"\n*{rc.file_path}:*")
                    snippet = rc.existing_content[:500]
                    prompt_parts.append(f"```{rc.language}\n{snippet}\n```")

        # Add available imports/classes/functions
        if context.imports:
            prompt_parts.append(f"\n**Available Imports:** {', '.join(context.imports[:20])}")
        if context.classes:
            prompt_parts.append(f"**Defined Classes:** {', '.join(context.classes[:10])}")
        if context.functions:
            prompt_parts.append(f"**Defined Functions:** {', '.join(context.functions[:20])}")

        # Add patterns to follow
        if self.patterns:
            prompt_parts.append("\n**Code Patterns to Follow:**")
            for pattern in self.patterns[:5]:
                prompt_parts.append(f"- {pattern.name}")

        prompt_parts.append(
            "\n\n**Instructions:**\n"
            "1. Follow the existing code style exactly\n"
            "2. Use existing imports and patterns from the codebase\n"
            "3. Write production-quality code\n"
            "4. Include proper error handling\n"
            "5. Add type hints if the codebase uses them\n"
            "\nGenerate the code:\n"
        )

        return "\n".join(prompt_parts)

    def _extract_code_from_response(self, response: str, language: str) -> str:
        """Extract code from an AI response."""
        # Try to find code blocks
        code_block_pattern = rf"```(?:{language})?\s*\n(.*?)```"
        matches = re.findall(code_block_pattern, response, re.DOTALL)
        if matches:
            return matches[0].strip()

        # Try FILE: blocks
        file_pattern = r"FILE:\s*\S+\s*\n```[^\n]*\n(.*?)```"
        matches = re.findall(file_pattern, response, re.DOTALL)
        if matches:
            return matches[0].strip()

        # Return raw response if no code blocks found
        return response.strip()

    def generate_test(
        self,
        source_file: str,
        test_file: str | None = None,
    ) -> CodeSuggestion:
        """Generate tests for a source file."""
        context = self.analyzer.analyze_file(source_file)

        if not test_file:
            # Generate test file path
            name = Path(source_file).stem
            parent = Path(source_file).parent
            test_file = str(parent / f"test_{name}.py")

        # Build test generation prompt
        prompt = self._build_test_prompt(context)

        if self.send_fn:
            response = self.send_fn(prompt)
            if response:
                code = self._extract_code_from_response(response, context.language)
                return CodeSuggestion(
                    code=code,
                    description=f"Generated tests for {source_file}",
                    confidence=0.7,
                    source="ai",
                )

        return CodeSuggestion(
            code="",
            description="Failed to generate tests",
            confidence=0.0,
        )

    def _build_test_prompt(self, context: CodeContext) -> str:
        """Build a prompt for test generation."""
        prompt_parts = [
            "## Test Generation Task\n",
            f"Generate comprehensive tests for the following {context.language} code:\n",
        ]

        if context.existing_content:
            prompt_parts.append(f"```{context.language}")
            existing = context.existing_content
            if len(existing) > 4000:
                existing = existing[:4000] + "\n... (truncated)"
            prompt_parts.append(f"{existing}\n```\n")

        prompt_parts.append("\n**Requirements:**")
        prompt_parts.append("1. Test all public functions and classes")
        prompt_parts.append("2. Include edge cases (empty inputs, None, boundaries)")
        prompt_parts.append("3. Include error cases (invalid inputs, exceptions)")
        prompt_parts.append("4. Use pytest style with descriptive test names")
        prompt_parts.append("5. Add docstrings explaining what each test verifies")
        prompt_parts.append("6. Use fixtures for common setup")

        if context.functions:
            prompt_parts.append(f"\n**Functions to test:** {', '.join(context.functions[:15])}")
        if context.classes:
            prompt_parts.append(f"**Classes to test:** {', '.join(context.classes[:10])}")

        return "\n".join(prompt_parts)


class CodeValidator:
    """Validates generated code for quality and correctness."""

    def __init__(self, cwd: Path):
        self.cwd = cwd

    def validate(self, code: str, language: str, file_path: str = "") -> ValidationResult:
        """Validate code for syntax and quality issues."""
        result = ValidationResult(valid=True)

        if language == "python":
            self._validate_python(code, result)
        elif language in ("javascript", "typescript"):
            self._validate_javascript(code, result)

        # Common validations
        self._validate_common(code, result)

        result.valid = len(result.errors) == 0
        return result

    def _validate_python(self, code: str, result: ValidationResult) -> None:
        """Validate Python code."""
        # Syntax check
        try:
            compile(code, "<string>", "exec")
        except SyntaxError as e:
            result.errors.append(f"Syntax error at line {e.lineno}: {e.msg}")
            return

        # Parse AST for deeper analysis
        try:
            tree = ast.parse(code)

            # Check for empty functions
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    # Check for just pass or ...
                    if len(node.body) == 1:
                        stmt = node.body[0]
                        if isinstance(stmt, ast.Pass):
                            result.warnings.append(
                                f"Empty function '{node.name}' - contains only 'pass'"
                            )
                        elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
                            if stmt.value.value is ...:
                                result.warnings.append(
                                    f"Empty function '{node.name}' - contains only '...'"
                                )

                # Check for TODO in docstrings
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if (
                        node.body
                        and isinstance(node.body[0], ast.Expr)
                        and isinstance(node.body[0].value, ast.Constant)
                        and isinstance(node.body[0].value.value, str)
                    ):
                        docstring = node.body[0].value.value
                        if "TODO" in docstring or "FIXME" in docstring:
                            result.warnings.append(
                                f"TODO/FIXME found in docstring of '{node.name}'"
                            )

        except Exception as e:
            result.errors.append(f"AST parsing error: {e!s}")

    def _validate_javascript(self, code: str, result: ValidationResult) -> None:
        """Validate JavaScript/TypeScript code."""
        # Basic bracket matching
        brackets = {"(": ")", "[": "]", "{": "}"}
        stack = []

        for i, char in enumerate(code):
            if char in brackets:
                stack.append((char, i))
            elif char in brackets.values():
                if not stack:
                    result.errors.append(f"Unmatched closing bracket '{char}' at position {i}")
                else:
                    open_bracket, _ = stack.pop()
                    if brackets[open_bracket] != char:
                        result.errors.append(f"Mismatched brackets at position {i}")

        if stack:
            for bracket, pos in stack:
                result.errors.append(f"Unclosed bracket '{bracket}' at position {pos}")

        # Check for common issues
        if "console.log(" in code:
            result.warnings.append("console.log() found - consider removing for production")

    def _validate_common(self, code: str, result: ValidationResult) -> None:
        """Common validation for all languages."""
        # Check for placeholder patterns
        placeholders = [
            (r"# TODO", "TODO comment found"),
            (r"// TODO", "TODO comment found"),
            (r"# FIXME", "FIXME comment found"),
            (r"// FIXME", "FIXME comment found"),
            (r"# Placeholder", "Placeholder comment found"),
            (r"pass\s*#\s*placeholder", "Placeholder pass statement"),
            (r"raise NotImplementedError", "NotImplementedError found"),
        ]

        for pattern, message in placeholders:
            if re.search(pattern, code, re.IGNORECASE):
                result.warnings.append(message)

        # Check for hardcoded secrets
        secret_patterns = [
            (r"password\s*=\s*['\"][^'\"]+['\"]", "Possible hardcoded password"),
            (r"api_key\s*=\s*['\"][^'\"]+['\"]", "Possible hardcoded API key"),
            (r"secret\s*=\s*['\"][^'\"]+['\"]", "Possible hardcoded secret"),
            (r"token\s*=\s*['\"][a-zA-Z0-9_-]{20,}['\"]", "Possible hardcoded token"),
        ]

        for pattern, message in secret_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                result.errors.append(f"Security: {message}")

    def validate_test_file(self, code: str, language: str = "python") -> ValidationResult:
        """Validate a test file specifically."""
        result = self.validate(code, language)

        # Additional test-specific validations
        if language == "python":
            # Check for assertions
            assertion_patterns = [
                r"\bassert\b",
                r"\.assert\w+\(",
                r"pytest\.raises",
                r"expect\(",
            ]
            has_assertions = any(re.search(p, code) for p in assertion_patterns)
            if not has_assertions:
                result.errors.append("Test file has no assertions")

            # Check for test functions
            test_funcs = re.findall(r"def (test_\w+)", code)
            if not test_funcs:
                result.errors.append("No test functions found (must start with 'test_')")

            # Check for empty test functions
            empty_tests = re.findall(r"def (test_\w+)\([^)]*\):\s*\n\s*pass", code)
            for test_name in empty_tests:
                result.errors.append(f"Empty test function: {test_name}")

        result.valid = len(result.errors) == 0
        return result


class StyleEnforcer:
    """Enforces consistent code style."""

    def __init__(self, style_config: dict[str, Any] | None = None):
        self.style_config = style_config or {
            "indent": "spaces",
            "indent_size": 4,
            "quote_style": "double",
            "max_line_length": 88,
            "trailing_comma": True,
        }

    def enforce(self, code: str, language: str) -> str:
        """Apply style enforcement to code."""
        if language == "python":
            return self._enforce_python(code)
        return code

    def _enforce_python(self, code: str) -> str:
        """Enforce Python code style."""
        lines = code.split("\n")
        result_lines = []

        for line in lines:
            # Fix indentation if using wrong type
            if self.style_config["indent"] == "spaces":
                # Convert tabs to spaces
                indent_match = re.match(r"^(\t+)", line)
                if indent_match:
                    tabs = len(indent_match.group(1))
                    spaces = " " * (tabs * self.style_config["indent_size"])
                    line = spaces + line[tabs:]

            result_lines.append(line)

        return "\n".join(result_lines)

    def check_style(self, code: str, language: str) -> list[str]:
        """Check code style and return list of issues."""
        issues = []

        if language == "python":
            lines = code.split("\n")

            for i, line in enumerate(lines, 1):
                # Check line length
                if len(line) > self.style_config["max_line_length"]:
                    issues.append(
                        f"Line {i}: exceeds {self.style_config['max_line_length']} characters"
                    )

                # Check indentation
                if (
                    self.style_config["indent"] == "spaces"
                    and "\t" in line[: len(line) - len(line.lstrip())]
                ):
                    issues.append(f"Line {i}: uses tabs instead of spaces")

        return issues
