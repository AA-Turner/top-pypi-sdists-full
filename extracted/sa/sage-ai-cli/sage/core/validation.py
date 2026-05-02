"""Content and code validation utilities for SAGE.

This module contains validation functions for:
- Python syntax validation
- JSON syntax validation
- Import validation and hallucination detection
- Garbage code detection (empty functions, missing assertions)

Extracted from main.py for better code organization (P3-72).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

__all__ = [
    "validate_python_syntax",
    "validate_json_syntax",
    "pre_validate_content",
    "extract_imports_from_python",
    "pending_modules_for_files",
    "module_exists_in_codebase",
    "validate_imports_in_content",
    "is_likely_hallucinated_code",
    "is_garbage_content",
    "validate_file_path_against_codebase",
    "detect_hallucinated_duplicate",
    # Constants
    "STDLIB_MODULES",
    "COMMON_PACKAGES",
    "LIKELY_HALLUCINATED_PATTERNS",
    "PLACEHOLDER_IMPORT_PATTERNS",
]


# Standard library modules - always valid
STDLIB_MODULES: set[str] = {
    "abc",
    "argparse",
    "ast",
    "asyncio",
    "base64",
    "bisect",
    "builtins",
    "calendar",
    "cmath",
    "collections",
    "concurrent",
    "configparser",
    "contextlib",
    "copy",
    "csv",
    "ctypes",
    "dataclasses",
    "datetime",
    "decimal",
    "difflib",
    "dis",
    "email",
    "enum",
    "errno",
    "faulthandler",
    "fileinput",
    "fnmatch",
    "fractions",
    "functools",
    "gc",
    "getopt",
    "getpass",
    "glob",
    "graphlib",
    "gzip",
    "hashlib",
    "heapq",
    "hmac",
    "html",
    "http",
    "imaplib",
    "importlib",
    "inspect",
    "io",
    "ipaddress",
    "itertools",
    "json",
    "keyword",
    "linecache",
    "locale",
    "logging",
    "lzma",
    "mailbox",
    "math",
    "mimetypes",
    "mmap",
    "modulefinder",
    "multiprocessing",
    "netrc",
    "numbers",
    "operator",
    "os",
    "pathlib",
    "pickle",
    "pkgutil",
    "platform",
    "plistlib",
    "poplib",
    "posix",
    "posixpath",
    "pprint",
    "profile",
    "pstats",
    "pty",
    "pwd",
    "py_compile",
    "pyclbr",
    "pydoc",
    "queue",
    "quopri",
    "random",
    "re",
    "readline",
    "reprlib",
    "resource",
    "rlcompleter",
    "runpy",
    "sched",
    "secrets",
    "select",
    "selectors",
    "shelve",
    "shlex",
    "shutil",
    "signal",
    "site",
    "smtplib",
    "sndhdr",
    "socket",
    "socketserver",
    "sqlite3",
    "ssl",
    "stat",
    "statistics",
    "string",
    "stringprep",
    "struct",
    "subprocess",
    "sunau",
    "symtable",
    "sys",
    "sysconfig",
    "syslog",
    "tabnanny",
    "tarfile",
    "telnetlib",
    "tempfile",
    "termios",
    "test",
    "textwrap",
    "threading",
    "time",
    "timeit",
    "tkinter",
    "token",
    "tokenize",
    "trace",
    "traceback",
    "tracemalloc",
    "tty",
    "turtle",
    "turtledemo",
    "types",
    "typing",
    "typing_extensions",
    "unicodedata",
    "unittest",
    "urllib",
    "uu",
    "uuid",
    "venv",
    "warnings",
    "wave",
    "weakref",
    "webbrowser",
    "winreg",
    "winsound",
    "wsgiref",
    "xdrlib",
    "xml",
    "xmlrpc",
    "zipapp",
    "zipfile",
    "zipimport",
    "zlib",
    "_thread",
}


# Common third-party packages - always valid
COMMON_PACKAGES: set[str] = {
    "pytest",
    "numpy",
    "pandas",
    "requests",
    "flask",
    "django",
    "fastapi",
    "sqlalchemy",
    "celery",
    "redis",
    "boto3",
    "botocore",
    "PIL",
    "cv2",
    "torch",
    "tensorflow",
    "keras",
    "sklearn",
    "scipy",
    "matplotlib",
    "seaborn",
    "plotly",
    "streamlit",
    "click",
    "rich",
    "httpx",
    "aiohttp",
    "pydantic",
    "attrs",
    "dataclasses_json",
    "marshmallow",
    "yaml",
    "toml",
    "dotenv",
    "openai",
    "anthropic",
    "transformers",
    "huggingface_hub",
    "langchain",
    "llama_index",
    "chromadb",
    "pinecone",
    "weaviate",
    "docker",
    "kubernetes",
    "paramiko",
    "fabric",
    "invoke",
    "setuptools",
    "pip",
    "wheel",
    "twine",
    "black",
    "isort",
    "flake8",
    "mypy",
    "pylint",
    "bandit",
    "semgrep",
    "coverage",
    "tox",
    "nox",
    "pre_commit",
    "git",
    "github",
    "gitlab",
    "jira",
    "slack_sdk",
    "discord",
    "tweepy",
    "beautifulsoup4",
    "bs4",
    "lxml",
    "scrapy",
    "selenium",
    "playwright",
    "pyautogui",
    "pyperclip",
    "faker",
    "factory_boy",
    "hypothesis",
    "mock",
    "responses",
    "freezegun",
    "vcrpy",
    "betamax",
    "pytest_mock",
    "mongomock",
    "moto",
    "localstack",
    "testcontainers",
    "pyfakefs",
    "typer",
    "uvicorn",
    "gunicorn",
    "starlette",
    "jinja2",
    "mako",
}


# Known hallucinated module patterns - these are commonly invented by models
LIKELY_HALLUCINATED_PATTERNS: set[str] = {
    # Common fake API modules (only flagged if they don't exist)
    "sage.api",
    "utils.api",
    "services",
    "service_layer",
    "app.models",
    "app.api",
    "app.services",
    "app.utils",
    "backend.api",
    "backend.models",
    "backend.services",
    "core.api",
    "core.models",
    "core.services",
    # Fake test utilities
    "test_helpers",
    # Fake data modules (only flagged if they don't exist)
    "database",
    "db",
    # CRITICAL: Common wrong project structure guesses
    # Models often assume 'src' is the root when it's not
    "src",
    "src.api",
    "src.models",
    "src.services",
    "src.utils",
    "src.api_client",
    "src.service",
    "src.client",
    "src.server",
    # Common hallucinated service classes
    "ContentService",
    "UserService",
    "APIClient",
    "BaseClient",
    "DataService",
    "AuthService",
    "ApiService",
    # Other common hallucinations
    "ai_utils",
    "model_utils",
    "chat_utils",
    # PLACEHOLDER MODULE NAMES - model wrote "your_module" instead of real module
    "your_module",
    "my_module",
    "some_module",
    "module_name",
    "your_package",
    "my_package",
    "your_project",
    "my_project",
    "your_app",
    "my_app",
    "the_module",
    "actual_module",
    "replace_with",
    "fill_in",
    "placeholder",
    "example_module",
}

# Regex patterns for detecting placeholder imports that indicate hallucination
PLACEHOLDER_IMPORT_PATTERNS: list[str] = [
    r"from\s+['\"]?your_\w+['\"]?\s+import",
    r"from\s+['\"]?my_\w+['\"]?\s+import",
    r"from\s+['\"]?some_\w+['\"]?\s+import",
    r"from\s+['\"]?placeholder['\"]?\s+import",
    r"from\s+['\"]?example_\w+['\"]?\s+import",
    r"from\s+['\"]?module_name['\"]?\s+import",
    r"from\s+['\"]?replace_\w+['\"]?\s+import",
    r"import\s+['\"]?your_\w+['\"]?",
    r"import\s+['\"]?my_\w+['\"]?",
    r"@patch\(['\"]your_\w+",
    r"@patch\(['\"]my_\w+",
    r"@patch\(['\"]module_name",
]


def validate_python_syntax(content: str, filepath: str) -> tuple[bool, str]:
    """Validate Python syntax before writing.

    Args:
        content: The Python source code content
        filepath: Path to the file (for error messages)

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        compile(content, filepath, "exec")
        return True, ""
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Compilation error: {e!s}"


def validate_json_syntax(content: str, filepath: str) -> tuple[bool, str]:
    """Validate JSON syntax before writing.

    Args:
        content: The JSON content
        filepath: Path to the file (for error messages)

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        json.loads(content)
        return True, ""
    except json.JSONDecodeError as e:
        return False, f"JSON error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"JSON parsing error: {e!s}"


def pre_validate_content(filepath: str, content: str) -> tuple[bool, str]:
    """Pre-validate content before writing to disk.

    Catches both structural errors (syntax) and semantic regressions (e.g. a
    model replacing import.meta.env with process.env in a Vite file).

    Args:
        filepath: Path to the file being written
        content: Proposed file content

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Python files — check syntax
    if filepath.endswith(".py"):
        is_valid, error = validate_python_syntax(content, filepath)
        if not is_valid:
            return False, error

        if "test_" in filepath or filepath.startswith("tests/"):
            has_test_func = bool(re.search(r"def test_\w+", content))
            if not has_test_func:
                if not (filepath.endswith("conftest.py") or filepath.endswith("__init__.py")):
                    return False, "Test file must contain at least one test function (def test_...)"

    # JSON files — check syntax
    elif filepath.endswith(".json"):
        is_valid, error = validate_json_syntax(content, filepath)
        if not is_valid:
            return False, error

    # Truncated content
    if content.strip().endswith("...") or content.strip().endswith("# ..."):
        return False, "Content appears truncated (ends with '...')"

    # ── Semantic regression checks ────────────────────────────────────────────
    # These catch patterns where a model produces technically valid code that
    # is semantically wrong for this codebase.

    # Rule 1: Vite/React frontend files must use import.meta.env, not process.env
    # process.env is Node.js — it doesn't exist in the browser bundle.
    _is_frontend = any(
        seg in filepath for seg in ("frontend/src", "frontend\\src")
    ) and filepath.endswith((".js", ".jsx", ".ts", ".tsx"))

    if _is_frontend and "process.env.VITE_" in content:
        return (
            False,
            f"{filepath}: uses process.env.VITE_* which is undefined in the browser. "
            "Vite frontend files must use import.meta.env.VITE_* instead.",
        )

    # Rule 2: Firebase auth initialisation must use parseFirebaseEnv or import.meta.env —
    # never bare process.env for the apiKey / authDomain fields.
    if "firebase" in filepath.lower() and "apiKey" in content and "process.env" in content:
        return (
            False,
            f"{filepath}: Firebase config uses process.env which is unavailable in the "
            "browser. Use import.meta.env.VITE_FIREBASE_* or parseFirebaseEnv(import.meta.env).",
        )

    # Rule 3: vite.config.ts / vite.config.js must not have its server.proxy
    # section removed if it was previously present — that breaks local dev routing.
    if re.search(r"vite\.config\.(t|j)s$", filepath):
        if "proxy" not in content and Path(filepath).exists():
            try:
                existing = Path(filepath).read_text(encoding="utf-8")
                if "proxy" in existing:
                    return (
                        False,
                        f"{filepath}: the new content removes the server.proxy configuration "
                        "which routes API calls during local development. Keep the proxy block.",
                    )
            except OSError:
                pass

    return True, ""


def extract_imports_from_python(content: str) -> list[str]:
    """Extract all imported module names from Python code.

    Returns list of top-level module names (e.g., 'ai_platform' from
    'from ai_platform.backend import foo').
    """
    imports = []

    # Match 'import X' and 'import X as Y'
    for m in re.finditer(r"^import\s+([\w.]+)", content, re.MULTILINE):
        module = m.group(1).split(".")[0]  # Top-level module
        imports.append(module)

    # Match 'from X import Y' and 'from X.Y import Z'
    for m in re.finditer(r"^from\s+([\w.]+)\s+import", content, re.MULTILINE):
        module = m.group(1).split(".")[0]  # Top-level module
        imports.append(module)

    return list(set(imports))


def pending_modules_for_files(filepaths: list[str]) -> set[str]:
    """Infer top-level module names that will exist after a batch write.

    Args:
        filepaths: List of file paths being written

    Returns:
        Set of module names that will be created
    """
    modules: set[str] = set()
    for filepath in filepaths:
        # CRITICAL FIX: Normalize path by removing leading './' to ensure
        # path.parts[0] is the actual directory, not '.'
        # This fixes the bug where './middleware/rate_limiter.py' would
        # add '.' to pending_modules instead of 'middleware'
        normalized = filepath.lstrip(".").lstrip("/")
        path = Path(normalized)
        if path.suffix != ".py":
            continue
        if path.name == "__init__.py":
            if path.parent.name and path.parent.name != ".":
                modules.add(path.parent.name)
            continue
        modules.add(path.stem)
        # Add all directory components as potential modules (for nested packages)
        # e.g., 'api/endpoints/users.py' adds both 'api' and 'endpoints'
        for part in path.parts[:-1]:  # Exclude the filename itself
            if part and part != ".":
                modules.add(part)
    return modules


def module_exists_in_codebase(
    module_name: str,
    cwd: Path,
    pending_modules: set[str] | None = None,
) -> bool:
    """Check if a module exists in the codebase.

    Checks for:
    - module_name.py file
    - module_name/ directory with __init__.py
    - module_name/ directory (namespace package)
    - Standard library modules
    - Common third-party packages

    Args:
        module_name: Name of the module to check
        cwd: Current working directory
        pending_modules: Set of modules about to be created

    Returns:
        True if the module exists or is a known valid module
    """
    if module_name in STDLIB_MODULES:
        return True

    if module_name in COMMON_PACKAGES:
        return True

    if pending_modules and module_name in pending_modules:
        return True

    # Check for local module file
    if (cwd / f"{module_name}.py").exists():
        return True

    # Check for local package directory
    pkg_dir = cwd / module_name
    if pkg_dir.is_dir():
        # Valid if has __init__.py or any .py files (namespace package)
        if (pkg_dir / "__init__.py").exists():
            return True
        if list(pkg_dir.glob("*.py")):
            return True

    # Check in common source directories
    for src_dir in ["src", "lib", "app"]:
        src_path = cwd / src_dir / module_name
        if (cwd / src_dir / f"{module_name}.py").exists():
            return True
        if src_path.is_dir() and (src_path / "__init__.py").exists():
            return True

    return False


def validate_imports_in_content(
    content: str,
    cwd: Path,
    pending_modules: set[str] | None = None,
) -> tuple[bool, list[str]]:
    """Validate that all imports in Python content exist.

    Returns (all_valid, list_of_missing_modules).

    Enhanced with:
    - Known hallucinated module detection
    - Strict validation for test files
    - Better error messages
    """
    imports = extract_imports_from_python(content)
    missing = []

    for module in imports:
        # First check if module actually exists - if so, it's not hallucinated
        if module_exists_in_codebase(module, cwd, pending_modules=pending_modules):
            continue

        # Check if this is a known hallucinated pattern
        if module in LIKELY_HALLUCINATED_PATTERNS or module.lower() in LIKELY_HALLUCINATED_PATTERNS:
            missing.append(f"{module} (HALLUCINATED - does not exist)")
            continue

        # Check for dotted imports that look hallucinated
        if "." in module:
            parts = module.split(".")
            # Check if the root module exists
            if not module_exists_in_codebase(parts[0], cwd, pending_modules=pending_modules):
                missing.append(f"{module} (root module '{parts[0]}' not found)")
                continue

        # If we get here, the module doesn't exist
        missing.append(module)

    return len(missing) == 0, missing


def is_likely_hallucinated_code(
    content: str,
    cwd: Path,
    pending_modules: set[str] | None = None,
) -> tuple[bool, str]:
    """Detect if code contains hallucinated imports or patterns.

    Args:
        content: The code content to check
        cwd: Current working directory
        pending_modules: Set of modules about to be created

    Returns:
        Tuple of (is_hallucinated, reason)
    """
    # CRITICAL: Check for placeholder import patterns FIRST
    # These are imports like "from your_module import" that the model wrote
    # instead of discovering and using actual modules
    for pattern in PLACEHOLDER_IMPORT_PATTERNS:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return True, (
                f"PLACEHOLDER IMPORT DETECTED: '{match.group(0)}'. "
                "The model wrote a placeholder instead of discovering the actual module. "
                "Use READ: and SEARCH: to find real modules before writing imports."
            )

    # Check for imports from non-existent modules
    is_valid, missing = validate_imports_in_content(content, cwd, pending_modules=pending_modules)
    if not is_valid and missing:
        # Check if any are marked as hallucinated
        hallucinated = [m for m in missing if "HALLUCINATED" in m or "not found" in m]
        if hallucinated:
            return True, f"Code imports from hallucinated modules: {', '.join(hallucinated)}"

    # Check for suspicious patterns that suggest hallucination
    suspicious_patterns = [
        (r"from\s+\w+\.api\s+import", "Suspicious 'from X.api import' pattern"),
        (r"from\s+services\.\w+\s+import", "Suspicious 'from services.X import' pattern"),
        (r"from\s+models\s+import", "Suspicious 'from models import' pattern"),
        (r"from\s+schemas\s+import", "Suspicious 'from schemas import' pattern"),
    ]

    for pattern, reason in suspicious_patterns:
        if re.search(pattern, content):
            # Verify the module actually exists
            match = re.search(pattern.replace(r"\s+import", ""), content)
            if match:
                module_part = match.group(0).replace("from ", "").strip()
                root_module = module_part.split(".")[0]
                if not module_exists_in_codebase(root_module, cwd, pending_modules=pending_modules):
                    return True, f"{reason} - module '{root_module}' does not exist"

    return False, ""


def is_garbage_content(filepath: str, content: str) -> tuple[bool, str]:
    """Check if file content is garbage (empty functions, no assertions, etc.).

    STRICT validation to reject placeholder code and incomplete implementations.
    SAGE must write production-ready code, not placeholder stubs.

    Args:
        filepath: Path to the file
        content: File content to check

    Returns:
        Tuple of (is_garbage, reason)
    """
    lines = content.strip().split("\n")
    non_empty_lines = [l for l in lines if l.strip() and not l.strip().startswith("#")]

    # ==========================================================================
    # TEST FILE VALIDATION (STRICT)
    # ==========================================================================
    if "test_" in filepath or filepath.startswith("tests/"):
        has_test_funcs = bool(re.search(r"def test_\w+", content))

        # Tests MUST have real assertions (not just pass or return)
        has_real_assertions = bool(
            re.search(
                r"\b(assert\s+.+|assertEqual\s*\(|assertTrue\s*\(|assertFalse\s*\(|"
                r"assertRaises\s*\(|assertIn\s*\(|assertIsNone\s*\(|assertIsNotNone\s*\(|"
                r"assertGreater\s*\(|assertLess\s*\(|assertAlmostEqual\s*\(|"
                r"expect\s*\(.+\)\s*\.|should\s*\.|pytest\.raises\s*\(|"
                r"to_equal\s*\(|toBe\s*\(|toEqual\s*\(|self\.assert)",
                content,
            )
        )
        if has_test_funcs and not has_real_assertions:
            return True, "Test file has no real assertions - tests MUST assert actual behavior"

        # Tests that only mock without testing anything
        mock_count = len(re.findall(r"@patch|@mock|Mock\(|MagicMock\(|patch\s*\(", content))
        if mock_count > 0 and not has_real_assertions:
            return (
                True,
                "Test file uses mocks but has no assertions - mocking without testing is useless",
            )

        # Tests that just pass
        test_bodies = re.findall(
            r'def test_\w+\([^)]*\):\s*\n(\s+(?:"""[^"]*"""\s*\n)?\s*pass)', content
        )
        if test_bodies:
            return True, "Test functions contain only 'pass' - tests must have real logic"

        # Tests that only have docstrings (no actual code)
        test_only_docstring = re.findall(
            r'def test_\w+\([^)]*\):\s*\n\s+"""[^"]*"""\s*(?:\n\s*)?(?=\n\s*def|\Z)', content
        )
        if test_only_docstring:
            return True, "Test functions only have docstrings without test logic"

    # ==========================================================================
    # EMPTY FUNCTION DETECTION (STRICT - even 1 empty function is suspicious)
    # ==========================================================================

    # Pattern for functions with just pass (stricter regex)
    empty_func_patterns = [
        r"def\s+\w+\([^)]*\):\s*\n\s+pass\s*(?:\n|$)",
        r'def\s+\w+\([^)]*\):\s*\n\s+"""[^"]*"""\s*\n\s+pass\s*(?:\n|$)',
        r"def\s+\w+\([^)]*\)\s*->\s*[^:]+:\s*\n\s+pass\s*(?:\n|$)",
    ]
    empty_funcs = []
    for pattern in empty_func_patterns:
        empty_funcs.extend(re.findall(pattern, content))

    total_funcs = re.findall(r"def\s+\w+\s*\(", content)

    # STRICT: Even 1 empty function in a non-base-class file is suspicious
    if len(empty_funcs) >= 1:
        # Allow base classes/protocols with abstract methods
        is_abstract = bool(re.search(r"@abstractmethod|ABC\)|Protocol\)", content))
        if not is_abstract:
            return (
                True,
                f"File has {len(empty_funcs)} empty function(s) with just 'pass' - write real implementation",
            )

    if len(total_funcs) >= 3 and len(empty_funcs) >= len(total_funcs) * 0.3:
        return True, f"{len(empty_funcs)}/{len(total_funcs)} functions are empty stubs"

    # ==========================================================================
    # PLACEHOLDER PATTERN DETECTION (COMPREHENSIVE)
    # ==========================================================================
    placeholder_indicators = [
        # Comment-based placeholders
        "# Placeholder",
        "# placeholder",
        "# PLACEHOLDER",
        "# TODO",
        "# todo",
        "# TODO:",
        "# todo:",
        "# FIXME",
        "# fixme",
        "# FIXME:",
        "# implement this",
        "# Implement this",
        "# IMPLEMENT",
        "# if needed",
        "# If needed",
        "# add implementation",
        "# Add implementation",
        "# fill in",
        "# Fill in",
        "# your code here",
        "# Your code here",
        "# stub",
        "# STUB",
        "# not implemented",
        "# Not implemented",
        "# TBD",
        "# tbd",
        "# WIP",
        "# wip",
        "# coming soon",
        "# Coming soon",
        # Pass with comments
        "pass  # placeholder",
        "pass # placeholder",
        "pass  # TODO",
        "pass # TODO",
        "pass  # implement",
        "pass # implement",
        # Ellipsis as placeholder
        "...  # placeholder",
        "... # placeholder",
        "...  # TODO",
        "... # TODO",
        # Raise NotImplemented patterns
        "raise NotImplementedError()",
        'raise NotImplementedError("',
        # Continue as placeholder
        "continue  # placeholder",
        "continue # placeholder",
        "continue  # TODO",
        "continue # TODO",
        # Return None patterns that indicate incomplete code
        "return None  # placeholder",
        "return None # placeholder",
        "return None  # TODO",
        "return None # TODO",
    ]

    content_lower = content.lower()
    for indicator in placeholder_indicators:
        if indicator.lower() in content_lower:
            return True, f"File contains placeholder pattern: '{indicator}'"

    # ==========================================================================
    # STUB CLASS DETECTION
    # ==========================================================================

    # Classes that are all empty methods
    class_matches = re.findall(
        r'class\s+(\w+)[^:]*:\s*\n((?:\s+(?:def|@|"""|\'\'\').*\n)*)', content
    )
    for class_name, class_body in class_matches:
        if class_body.strip():
            method_count = len(re.findall(r"def\s+\w+", class_body))
            empty_method_count = len(re.findall(r"def\s+\w+[^:]*:\s*\n\s+pass", class_body))
            if method_count > 0 and empty_method_count == method_count:
                return (
                    True,
                    f"Class '{class_name}' has all empty methods - write real implementation",
                )

    # ==========================================================================
    # MINIMAL CONTENT CHECK
    # ==========================================================================
    if filepath.endswith(".py"):
        non_comment_content = "\n".join(
            l for l in lines if l.strip() and not l.strip().startswith("#")
        )
        stripped = non_comment_content.strip()

        # File is just pass or ...
        if stripped in ("pass", "..."):
            return True, "File contains only 'pass' or '...' - not a real implementation"

        # File has only imports and pass
        if re.match(
            r"^(import\s+\w+|from\s+\w+\s+import\s+\w+|\s)*pass\s*$", stripped, re.MULTILINE
        ):
            return True, "File has only imports and 'pass' - not a real implementation"

    # ==========================================================================
    # FUNCTION THAT DOES NOTHING USEFUL
    # ==========================================================================

    # Functions that just return None or return without value
    useless_return_funcs = re.findall(
        r'def\s+(\w+)\([^)]*\):\s*\n(?:\s+"""[^"]*"""\s*\n)?\s+return\s*(?:None)?\s*(?:\n|$)',
        content,
    )
    if len(useless_return_funcs) >= 2:
        return True, f"Functions {useless_return_funcs[:3]} just return None - write real logic"

    return False, ""


def _find_actual_test_directory(cwd: Path) -> str | None:
    """Find the actual test directory in the project.

    Returns the path to the test directory relative to cwd, or None if not found.
    Examples: 'tests', 'test', 'sage/tests', 'src/tests', etc.
    """
    # Check common patterns for test directories
    test_patterns = [
        # Nested test directories (more specific first)
        "*/tests",
        "*/test",
        "**/tests",
        # Root-level test directories
        "tests",
        "test",
    ]

    for pattern in test_patterns:
        matches = list(cwd.glob(pattern))
        for match in matches:
            if match.is_dir():
                # Verify it actually contains test files
                test_files = list(match.glob("test_*.py")) + list(match.glob("*_test.py"))
                if test_files:
                    return str(match.relative_to(cwd))

    return None


def _detect_canonical_workspace_root(cwd: Path) -> Path | None:
    """Detect if the workspace has a canonical project root subdirectory.

    Some repos have a top-level directory that is just a container, with the
    actual project in a subdirectory (e.g., ai-platform/ containing the real app).

    Indicators of a canonical subdirectory:
    - Contains pyproject.toml, setup.py, or package.json
    - Contains __init__.py or src/ directory
    - Has significantly more source files than the parent

    Args:
        cwd: Current working directory

    Returns:
        Path to canonical root if detected, None otherwise
    """
    # Check if cwd itself has project markers
    project_markers = [
        "pyproject.toml",
        "setup.py",
        "setup.cfg",
        "package.json",
        "Cargo.toml",
        "go.mod",
    ]
    has_root_markers = any((cwd / marker).exists() for marker in project_markers)

    if has_root_markers:
        return None  # cwd is the canonical root

    # Look for subdirectories that look like project roots
    candidates = []
    for subdir in cwd.iterdir():
        if not subdir.is_dir() or subdir.name.startswith("."):
            continue

        # Check for project markers in subdirectory
        subdir_markers = sum(1 for m in project_markers if (subdir / m).exists())
        if subdir_markers > 0:
            # Count Python files as a tie-breaker
            py_count = len(list(subdir.rglob("*.py")))
            candidates.append((subdir, subdir_markers, py_count))

    if not candidates:
        return None

    # Sort by marker count (desc), then py file count (desc)
    candidates.sort(key=lambda x: (-x[1], -x[2]))
    best_candidate = candidates[0][0]

    # Only return if the candidate has significantly more structure
    if candidates[0][1] >= 1:  # At least one project marker
        return best_candidate

    return None


def validate_file_path_against_codebase(
    filepath: str,
    cwd: Path,
) -> tuple[bool, str]:
    """Validate that a FILE: path makes sense for the actual codebase structure.

    This prevents SAGE from creating files in wrong locations like:
    - src/api_client.py when the codebase uses sage/
    - tests/test_api.py when the codebase uses sage/tests/
    - model_registry.py at root when the real one is in ai-platform/backend/

    Args:
        filepath: The path from FILE: block
        cwd: Current working directory

    Returns:
        Tuple of (is_valid, error_message)
    """
    path = Path(filepath)
    parts = path.parts

    if not parts:
        return False, "Empty file path"

    # ══════════════════════════════════════════════════════════════════════════
    # DETECT GARBAGE REPETITIVE PATHS - CRITICAL: Model hallucinating paths
    # ══════════════════════════════════════════════════════════════════════════
    # Detect patterns like ai-platform/ai-platform/ai-platform/...
    if len(parts) > 3:
        # Check for repeated segments
        from collections import Counter

        segment_counts = Counter(parts)
        most_common_segment, most_common_count = segment_counts.most_common(1)[0]
        # If any segment appears more than twice, it's likely garbage
        if most_common_count > 2:
            return False, (
                f"Invalid repetitive path: '{filepath}' contains segment '{most_common_segment}' "
                f"repeated {most_common_count} times. This is likely a model hallucination. "
                f"Use SEARCH: to discover actual project structure."
            )

    # Additional check: path is excessively long (likely garbage)
    if len(filepath) > 500:
        return False, (
            f"Path is excessively long ({len(filepath)} chars). "
            "This is likely a model hallucination."
        )

    # ══════════════════════════════════════════════════════════════════════════
    # DETECT CANONICAL WORKSPACE ROOT - CRITICAL FOR MULTI-LEVEL REPOS
    # ══════════════════════════════════════════════════════════════════════════
    canonical_root = _detect_canonical_workspace_root(cwd)
    if canonical_root:
        # Check if the file path is being created at the wrong level
        # If we're trying to create files at cwd level but there's a canonical root,
        # and the path doesn't start with the canonical root name, it might be wrong
        canonical_name = canonical_root.name

        # Special case: if path is creating source files at root and canonical has same
        if parts[0] not in (canonical_name, "tests", "test", "docs", "scripts", ".github"):
            # Check if a similar path exists under the canonical root
            potential_path = canonical_root / filepath
            existing_similar = list(canonical_root.glob(f"**/{parts[-1]}"))

            if existing_similar:
                return False, (
                    f"FILE: path '{filepath}' creates file at workspace root, but this repo "
                    f"has its project under '{canonical_name}/'. Found similar file(s): "
                    f"{', '.join(str(p.relative_to(cwd)) for p in existing_similar[:3])}. "
                    f"Use the existing location instead."
                )

    # ══════════════════════════════════════════════════════════════════════════
    # DETECT WRONG PROJECT STRUCTURE ASSUMPTIONS
    # ══════════════════════════════════════════════════════════════════════════

    # Check if path starts with 'src/' but codebase doesn't have a src/ directory
    # BUT only block this if there ARE other source directories (established project structure)
    if parts[0] == "src":
        src_dir = cwd / "src"
        if not src_dir.exists():
            # Look for what the actual structure is
            actual_dirs = [
                d.name for d in cwd.iterdir() if d.is_dir() and not d.name.startswith(".")
            ]
            # Filter to likely source directories (contain .py files)
            source_dirs = [
                d for d in actual_dirs if (cwd / d).is_dir() and list((cwd / d).glob("*.py"))
            ]
            # Only reject if there ARE established source directories (not a fresh project)
            if source_dirs:
                return False, (
                    f"FILE: path starts with 'src/' but this codebase does NOT have a src/ directory. "
                    f"Actual source directories: {', '.join(source_dirs[:5])}. "
                    "Use SEARCH: to discover the actual project structure first."
                )

    # ══════════════════════════════════════════════════════════════════════════
    # DETECT WRONG TEST DIRECTORY - CRITICAL FIX
    # If project has tests in nested directory (e.g., sage/tests/), reject tests/ at root
    # ══════════════════════════════════════════════════════════════════════════
    if parts[0] in ("tests", "test"):
        root_test_dir = cwd / parts[0]
        if not root_test_dir.exists():
            # Check if there's a nested test directory
            actual_test_dir = _find_actual_test_directory(cwd)
            if actual_test_dir and actual_test_dir not in ("tests", "test"):
                return False, (
                    f"FILE: path '{filepath}' creates tests in '{parts[0]}/' at project root, "
                    f"but this codebase has tests in '{actual_test_dir}/'. "
                    f"Use the correct path: {actual_test_dir}/{'/'.join(parts[1:])}"
                )

    # Check if creating files in a structure that doesn't exist
    # Only warn when there's an established project (has existing directories with Python files)
    if len(parts) > 1:
        root_dir = cwd / parts[0]
        # Don't automatically whitelist 'tests'/'test' - let the check above handle it
        whitelist = ("scripts", "docs", "config")
        if not root_dir.exists() and parts[0] not in whitelist:
            # Check if this might be a typo or wrong assumption
            existing_dirs = [
                d.name for d in cwd.iterdir() if d.is_dir() and not d.name.startswith(".")
            ]
            # Only block if there are existing Python source directories
            source_dirs = [
                d for d in existing_dirs if (cwd / d).is_dir() and list((cwd / d).glob("*.py"))
            ]
            if parts[0] not in existing_dirs and source_dirs:
                suggestion = f"Existing directories: {', '.join(existing_dirs[:5])}"
                return False, (
                    f"FILE: path '{filepath}' creates files in directory '{parts[0]}/' which doesn't exist. "
                    f"{suggestion}. Use SEARCH: to find the correct location."
                )

    # ══════════════════════════════════════════════════════════════════════════
    # DETECT COMMON HALLUCINATED PATHS
    # ══════════════════════════════════════════════════════════════════════════

    hallucinated_roots = {
        "app",
        "application",
        "server",
        "client",
        "api",
        "services",
        "models",
        "views",
        "controllers",
        "handlers",
        "lib",
        "core",
    }

    if parts[0] in hallucinated_roots:
        root_dir = cwd / parts[0]
        if not root_dir.exists():
            # Only block if there are established source directories
            actual_dirs = [
                d.name for d in cwd.iterdir() if d.is_dir() and not d.name.startswith(".")
            ]
            source_dirs = [
                d for d in actual_dirs if (cwd / d).is_dir() and list((cwd / d).glob("*.py"))
            ]
            if source_dirs:
                return False, (
                    f"FILE: path '{filepath}' uses common boilerplate directory '{parts[0]}/' "
                    "which doesn't exist in this codebase. Use SEARCH: to find where code should go."
                )

    return True, ""


def detect_hallucinated_duplicate(
    filepath: str,
    content: str,
    cwd: Path,
) -> tuple[bool, str]:
    """Detect if the model is creating a duplicate of an existing file.

    This prevents SAGE from inventing new files when real implementations exist,
    like creating src/model_registry.py when ai-platform/backend/model_registry.py
    already exists.

    Args:
        filepath: The path being created
        content: The content being written
        cwd: Current working directory

    Returns:
        Tuple of (is_duplicate, reason)
    """
    filename = Path(filepath).name

    # Search for existing files with the same name
    existing_files = list(cwd.rglob(filename))

    if not existing_files:
        return False, ""  # No duplicates

    # Filter out the exact path (in case of updates to existing file)
    normalized_new_path = (
        Path(filepath).resolve() if Path(filepath).is_absolute() else (cwd / filepath).resolve()
    )
    existing_files = [f for f in existing_files if f.resolve() != normalized_new_path]

    if not existing_files:
        return False, ""  # Only found the file itself

    # Check if content is similar to existing file
    for existing_file in existing_files:
        try:
            existing_content = existing_file.read_text(encoding="utf-8", errors="replace")

            # Quick similarity check based on key patterns
            # Extract class/function definitions from both
            new_defs = set(re.findall(r"(?:def|class)\s+(\w+)", content))
            existing_defs = set(re.findall(r"(?:def|class)\s+(\w+)", existing_content))

            # If there's significant overlap in definitions, it's likely a duplicate
            overlap = new_defs & existing_defs
            if len(overlap) >= 3 or (len(new_defs) > 0 and len(overlap) / len(new_defs) > 0.5):
                rel_path = existing_file.relative_to(cwd)
                return True, (
                    f"FILE: '{filepath}' duplicates existing file '{rel_path}'. "
                    f"Common definitions: {', '.join(list(overlap)[:5])}. "
                    f"Use READ: {rel_path} to modify the existing file instead."
                )

        except Exception:
            continue  # Skip files that can't be read

    # Even if content differs, warn about same filename
    if len(existing_files) >= 1:
        existing_paths = [str(f.relative_to(cwd)) for f in existing_files[:3]]
        return True, (
            f"FILE: '{filepath}' creates a new file but '{filename}' already exists at: "
            f"{', '.join(existing_paths)}. "
            f"Consider modifying the existing file with READ: first."
        )

    return False, ""


# Backward compatibility aliases (prefixed versions for main.py)
_validate_python_syntax = validate_python_syntax
_validate_json_syntax = validate_json_syntax
_pre_validate_content = pre_validate_content
_extract_imports_from_python = extract_imports_from_python
_pending_modules_for_files = pending_modules_for_files
_module_exists_in_codebase = module_exists_in_codebase
_validate_imports_in_content = validate_imports_in_content
_is_likely_hallucinated_code = is_likely_hallucinated_code
_is_garbage_content = is_garbage_content
_validate_file_path_against_codebase = validate_file_path_against_codebase
_detect_hallucinated_duplicate = detect_hallucinated_duplicate
