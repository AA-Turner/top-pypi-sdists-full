import ast
import importlib.util
import os
import subprocess
import sys
import threading
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, distribution
from pathlib import Path
from shutil import move
from tempfile import mkdtemp
from typing import (
    Callable,
    Dict,
    Iterator,
    List,
    Literal,
    Mapping,
    Optional,
    Set,
    Tuple,
)

from importlib_metadata import packages_distributions
from packaging.requirements import Requirement
from pip._internal.cli.main import main as pip_main

from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.project.project import LocalProjectRepository
from abstra_internals.services.fs import FileSystemService
from abstra_internals.services.pypi_cache import PyPIVerificationCache
from abstra_internals.settings import Settings
from abstra_internals.utils.ast_cache import ASTCache
from abstra_internals.utils.format import pip_name

install_lock = threading.Lock()


class RequirementsChangeNotifier:
    """Pub/sub for requirements install/uninstall events.
    Decouples this service from controllers/UI: listeners (e.g. UI
    notification) subscribe at bootstrap instead of services importing them.
    """

    _listeners: List[Callable[[], None]] = []
    _lock = threading.Lock()

    @classmethod
    def register(cls, listener: Callable[[], None]) -> None:
        with cls._lock:
            cls._listeners.append(listener)

    @classmethod
    def unregister(cls, listener: Callable[[], None]) -> None:
        with cls._lock:
            try:
                cls._listeners.remove(listener)
            except ValueError:
                pass

    @classmethod
    def clear(cls) -> None:
        """Intended for tests."""
        with cls._lock:
            cls._listeners.clear()

    @classmethod
    def notify(cls) -> None:
        with cls._lock:
            listeners = list(cls._listeners)
        for listener in listeners:
            try:
                listener()
            except Exception as e:
                AbstraLogger.error(f"requirements change callback failed: {e}")


class _PackagesDistributionsCache:
    """
    Cache for packages_distributions() which is expensive (~180ms).

    This mapping only changes when packages are installed/uninstalled,
    which is rare during normal editing. We use a simple TTL-based cache.
    """

    _cache: Optional[Mapping[str, List[str]]] = None
    _cache_time: Optional[float] = None
    _TTL_SECONDS: float = 1800.0  # Cache for 30 minutes

    @classmethod
    def get(cls) -> Mapping[str, List[str]]:
        import time

        now = time.time()

        if (
            cls._cache is not None
            and cls._cache_time is not None
            and (now - cls._cache_time) < cls._TTL_SECONDS
        ):
            return cls._cache

        cls._cache = packages_distributions()
        cls._cache_time = now
        return cls._cache

    @classmethod
    def invalidate(cls) -> None:
        cls._cache = None
        cls._cache_time = None


class _TransitiveDependenciesCache:
    """
    Cache for transitive dependencies calculation.

    Invalidates when requirements.txt is modified (based on mtime).
    This is important for editor performance since get_requirements_lint_markers
    is called on every code change.
    """

    _cache: Optional[Set[str]] = None
    _requirements_mtime: Optional[float] = None
    _requirements_names: Optional[Set[str]] = None

    @classmethod
    def _get_requirements_path(cls) -> Path:
        return Settings.root_path / "requirements.txt"

    @classmethod
    def _get_current_mtime(cls) -> Optional[float]:
        try:
            path = cls._get_requirements_path()
            if path.exists():
                return path.stat().st_mtime
            return None
        except Exception:
            return None

    @classmethod
    def get_covered_packages(cls, requirements_names: Set[str]) -> Set[str]:
        """
        Get cached covered packages, recomputing if requirements.txt changed.
        """
        current_mtime = cls._get_current_mtime()

        # Check if cache is valid
        if (
            cls._cache is not None
            and cls._requirements_mtime == current_mtime
            and cls._requirements_names == requirements_names
        ):
            return cls._cache

        # Recompute
        cls._cache = get_transitive_dependencies(requirements_names)
        cls._requirements_mtime = current_mtime
        cls._requirements_names = requirements_names.copy()

        return cls._cache

    @classmethod
    def invalidate(cls) -> None:
        """Force cache invalidation."""
        cls._cache = None
        cls._requirements_mtime = None
        cls._requirements_names = None


def _is_extra_dependency(req: Requirement) -> bool:
    """
    Check if a requirement is an optional extra dependency.

    Extra dependencies have markers like 'extra == "dev"' or 'extra == "test"'.
    These are only installed when explicitly requested (e.g., pip install pkg[dev]).
    """
    if req.marker is None:
        return False

    # Check if the marker contains 'extra' variable
    # Markers like 'extra == "test"' indicate optional dependencies
    marker_str = str(req.marker)
    return "extra" in marker_str


def get_transitive_dependencies(package_names: Set[str]) -> Set[str]:
    """
    Get all transitive dependencies of the given packages.

    Returns a set of normalized package names that includes:
    - The input packages themselves
    - All their direct and transitive dependencies (excluding optional extras)

    This is used to determine if an installed package is "covered" by
    the requirements.txt (either directly listed or as a transitive dependency).

    Note: Optional extras (e.g., dependencies with 'extra == "dev"') are excluded
    unless explicitly included in the input package_names.
    """
    covered: Set[str] = set()
    to_process = list(package_names)

    while to_process:
        pkg = to_process.pop()
        normalized = pip_name(pkg)

        if normalized in covered:
            continue

        covered.add(normalized)

        try:
            dist = distribution(pkg)
            requires = dist.requires or []

            for req_str in requires:
                try:
                    req = Requirement(req_str)

                    # Skip optional extra dependencies
                    if _is_extra_dependency(req):
                        continue

                    dep_name = pip_name(req.name)
                    if dep_name not in covered:
                        to_process.append(req.name)
                except Exception:
                    continue
        except PackageNotFoundError:
            continue

    return covered


def stream_output(cmd: List[str]):
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    if process.stdout is None:
        return
    for line in iter(process.stdout.readline, ""):
        yield line
    code = process.wait()
    if code != 0:
        yield "__ABSTRA_STREAM_ERROR__"


def check_package(package_name) -> Literal["builtin", "installed", "unknown"]:
    if package_name in sys.builtin_module_names:
        return "builtin"

    spec = importlib.util.find_spec(package_name)
    if spec is not None:
        # Regular package with __init__.py
        if spec.origin is not None:
            if "site-packages" in spec.origin:
                return "installed"
            return "builtin"

        # Namespace package (PEP 420) - no __init__.py, but has submodule_search_locations
        if spec.submodule_search_locations:
            for location in spec.submodule_search_locations:
                if "site-packages" in location:
                    return "installed"
            return "builtin"

    return "unknown"


def _should_skip_directory(path: Path) -> bool:
    """
    Check if a directory should be skipped during Python file search.

    Skips:
    - Hidden directories (starting with .)
    - Python cache directories (__pycache__)
    - Directories ignored by .gitignore (uses FileSystemService for this)
    """
    name = path.name

    # Fast checks first (no I/O required)
    if name.startswith(".") or name == "__pycache__":
        return True

    # Check .gitignore rules (cached, uses git check-ignore when available)
    return FileSystemService.is_ignored(path)


def _has_python_files_recursive(
    directory: Path, max_depth: int, current_depth: int = 0
) -> bool:
    """
    Recursively check if a directory contains Python files up to a maximum depth.

    This function supports Python 3.3+ namespace packages (PEP 420), which don't
    require __init__.py files. A directory structure like:

        src/
            entities/
                square.py
            jobs/
                job.py

    Is valid Python code where `from src.entities.square import Square` works,
    even without any __init__.py files.

    Args:
        directory: The directory to search in
        max_depth: Maximum depth to search (e.g., 5 means up to 5 levels deep)
        current_depth: Current recursion depth (used internally)

    Returns:
        True if any .py file is found within the depth limit, False otherwise
    """
    if current_depth > max_depth:
        return False

    try:
        items = list(directory.iterdir())

        # First pass: check for Python files (fast path, avoids unnecessary recursion)
        for item in items:
            if item.is_file() and item.suffix == ".py":
                return True

        # Second pass: recurse into subdirectories only if no .py files found
        for item in items:
            if item.is_dir() and not _should_skip_directory(item):
                if _has_python_files_recursive(item, max_depth, current_depth + 1):
                    return True
    except PermissionError:
        # Skip directories we can't access
        pass

    return False


# Maximum depth to search for Python files when detecting local modules.
# This limits performance impact while supporting reasonably nested project structures.
_LOCAL_MODULE_MAX_SEARCH_DEPTH = 5


def is_local_module(pkg_name: str) -> bool:
    """
    Check if a package name corresponds to a local module in the project.

    A local module is either:
    - A Python file with the same name (e.g., utils.py)
    - A directory with the same name containing Python files (with or without __init__.py)

    This function supports namespace packages (PEP 420, Python 3.3+), where directories
    don't need __init__.py to be valid packages. For example, this project structure:

        project/
            src/
                entities/
                    square.py

    Allows `from src.entities.square import Square` to work without any __init__.py files.
    The linter should recognize 'src' as a local module and not suggest adding it to
    requirements.txt.

    Args:
        pkg_name: The package name to check (e.g., "src" from "from src.entities import X")

    Returns:
        True if it's a local module, False otherwise
    """
    root = Settings.root_path

    # Check if it's a Python file (e.g., utils.py)
    if (root / f"{pkg_name}.py").exists():
        return True

    # Check if it's a directory with Python files (supports namespace packages)
    pkg_dir = root / pkg_name
    if pkg_dir.is_dir():
        return _has_python_files_recursive(
            pkg_dir,
            max_depth=_LOCAL_MODULE_MAX_SEARCH_DEPTH,
        )

    return False


@dataclass
class ImportAnalysisResult:
    """
    Result of analyzing a single import statement.

    This follows the decision tree:
    1. Is import local? → skip (not included in results)
    2. Is import builtin? → skip (not included in results)
    3. Can import be resolved (installed)?
       3.a Yes → Is it in requirements.txt?
           3.a.1 Yes → status="ok"
           3.a.2 No → status="missing_in_requirements"
       3.b No → Go to step 4
    4. Are all libs in requirements.txt installed?
       4.a No → status="unknown" (can't determine)
       4.b Yes → Go to step 5
    5. Does the import name exist on PyPI?
       5.a Yes → status="missing_in_requirements"
       5.b No → status="invalid_import"
    """

    import_name: str
    package_name: str  # The actual package name (may differ from import_name)
    file_path: Optional[Path]
    line: int
    col_start: int
    col_end: int
    code: str
    status: Literal["ok", "missing_in_requirements", "invalid_import", "unknown"]


def get_uninstalled_requirements(
    requirements: Optional["Requirements"] = None,
) -> List[str]:
    if requirements is None:
        requirements = RequirementsRepository.load()

    uninstalled = []

    for lib in requirements.libraries:
        # Skip URL-based packages
        if lib.url:
            continue

        installed_version = get_installed_version(lib.name)
        if installed_version is None:
            uninstalled.append(lib.name)

    return uninstalled


def analyze_code_imports(
    code: str,
    file_path: Optional[Path] = None,
    requirements_names: Optional[Set[str]] = None,
    uninstalled_libs: Optional[List[str]] = None,
    package_dist_cache: Optional[Mapping[str, List[str]]] = None,
    skip_pypi_check: bool = False,
    parsed_ast: Optional[ast.Module] = None,
    covered_packages: Optional[Set[str]] = None,
) -> List[ImportAnalysisResult]:
    """
    Analyze imports in a code string following the decision tree flow.

    Args:
        code: Python source code to analyze
        file_path: Optional path to the file (for reporting)
        requirements_names: Set of normalized package names in requirements.txt.
                           If None, will be loaded from RequirementsRepository.
        uninstalled_libs: List of uninstalled packages from requirements.txt.
                         If None, will be computed.
        package_dist_cache: Cache from packages_distributions().
                           If None, will be computed.
        skip_pypi_check: If True, skip PyPI verification for unknown packages.
        parsed_ast: Optional pre-parsed AST. If provided, skips parsing.
                   Use with ASTCache.get_with_content() for efficiency.
        covered_packages: Set of normalized package names that are covered by
                         requirements.txt (including transitive dependencies).
                         If None, will be computed from requirements_names.

    Returns:
        List of ImportAnalysisResult for imports that need attention
        (excludes local modules and builtins).
    """
    results: List[ImportAnalysisResult] = []

    # Use pre-parsed AST if provided, otherwise parse the code
    if parsed_ast is not None:
        parsed = parsed_ast
    else:
        try:
            parsed = ast.parse(code)
        except SyntaxError:
            return results

    lines = code.splitlines()

    # Load dependencies if not provided
    requirements = None
    if requirements_names is None:
        requirements = RequirementsRepository.load()
        requirements_names = {pip_name(lib.name) for lib in requirements.libraries}

    if uninstalled_libs is None:
        uninstalled_libs = get_uninstalled_requirements(requirements)

    if package_dist_cache is None:
        package_dist_cache = _PackagesDistributionsCache.get()

    # Compute covered packages (requirements + their transitive dependencies)
    # Uses cache to avoid recomputation on every editor keystroke
    if covered_packages is None:
        covered_packages = _TransitiveDependenciesCache.get_covered_packages(
            requirements_names
        )

    has_uninstalled_libs = len(uninstalled_libs) > 0

    visited_packages: Set[str] = set()

    for node in ast.walk(parsed):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports_info: List[tuple] = []  # (pkg_name, col_start, col_end)
            lineno = node.lineno
            source_line = lines[lineno - 1] if lineno <= len(lines) else ""

            if isinstance(node, ast.Import):
                for alias in node.names:
                    pkg_name = alias.name.split(".")[0]
                    col_start = source_line.find(alias.name)
                    if col_start == -1:
                        col_start = node.col_offset
                    col_end = col_start + len(pkg_name)
                    imports_info.append((pkg_name, col_start, col_end))
            elif (
                isinstance(node, ast.ImportFrom)
                and node.module is not None
                and node.level == 0  # Skip relative imports
            ):
                pkg_name = node.module.split(".")[0]
                from_idx = source_line.find("from ")
                if from_idx != -1:
                    col_start = source_line.find(node.module, from_idx + 5)
                else:
                    col_start = source_line.find(node.module)
                if col_start == -1:
                    col_start = node.col_offset
                col_end = col_start + len(pkg_name)
                imports_info.append((pkg_name, col_start, col_end))

            for pkg_name, col_start, col_end in imports_info:
                if pkg_name in visited_packages:
                    continue
                visited_packages.add(pkg_name)

                # Step 1: Is it a local module?
                if is_local_module(pkg_name):
                    continue

                # Step 2: Check package status
                kind = check_package(pkg_name)

                # Skip builtin modules
                if kind == "builtin":
                    continue

                # Step 3: Can the import be resolved (installed)?
                if kind == "installed":
                    # Get the actual package names that provide this import
                    lib_names = package_dist_cache.get(pkg_name, [pkg_name])

                    # Check if ANY of the providing packages is covered by requirements
                    # (either directly in requirements.txt or as a transitive dependency)
                    is_covered = any(
                        pip_name(lib_name) in covered_packages for lib_name in lib_names
                    )

                    if is_covered:
                        # 3.a.1: Installed and covered by requirements → OK
                        continue
                    else:
                        # 3.a.2: Installed but NOT covered by requirements → Error
                        package_name = lib_names[0] if lib_names else pkg_name
                        results.append(
                            ImportAnalysisResult(
                                import_name=pkg_name,
                                package_name=package_name,
                                file_path=file_path,
                                line=lineno,
                                col_start=col_start,
                                col_end=col_end,
                                code=source_line,
                                status="missing_in_requirements",
                            )
                        )
                        continue

                # Step 4: Import is not resolved (unknown)
                # If there are uninstalled libs, we can't reliably check PyPI
                if has_uninstalled_libs or skip_pypi_check:
                    results.append(
                        ImportAnalysisResult(
                            import_name=pkg_name,
                            package_name=pkg_name,
                            file_path=file_path,
                            line=lineno,
                            col_start=col_start,
                            col_end=col_end,
                            code=source_line,
                            status="unknown",
                        )
                    )
                    continue

                # Step 5: All requirements are installed, check PyPI
                exists_on_pypi = PyPIVerificationCache.verify_package_exists(pkg_name)

                if exists_on_pypi:
                    # 5.a: Exists on PyPI → Missing package
                    results.append(
                        ImportAnalysisResult(
                            import_name=pkg_name,
                            package_name=pkg_name,
                            file_path=file_path,
                            line=lineno,
                            col_start=col_start,
                            col_end=col_end,
                            code=source_line,
                            status="missing_in_requirements",
                        )
                    )
                else:
                    # 5.b: Not on PyPI → Invalid import
                    results.append(
                        ImportAnalysisResult(
                            import_name=pkg_name,
                            package_name=pkg_name,
                            file_path=file_path,
                            line=lineno,
                            col_start=col_start,
                            col_end=col_end,
                            code=source_line,
                            status="invalid_import",
                        )
                    )

    return results


def analyze_project_imports(
    skip_pypi_check: bool = False,
) -> Tuple[List[ImportAnalysisResult], List[str]]:
    """
    Analyze imports across all project files.

    Returns:
        Tuple of (results, uninstalled_libs) where:
        - results: List of ImportAnalysisResult for all imports needing attention
        - uninstalled_libs: List of package names from requirements.txt that aren't installed
    """
    all_results: List[ImportAnalysisResult] = []

    # Load shared state once
    requirements = RequirementsRepository.load()
    requirements_names = {pip_name(lib.name) for lib in requirements.libraries}
    uninstalled_libs = get_uninstalled_requirements(requirements)
    package_dist_cache = packages_distributions()
    covered_packages = get_transitive_dependencies(requirements_names)

    # Track visited packages across all files
    visited_packages: Set[str] = set()

    project = LocalProjectRepository().load()

    for python_file in project.project_files:
        if not python_file.exists():
            continue

        try:
            # Use ASTCache to avoid re-parsing files on multiple linter runs
            parsed_ast, code = ASTCache.get_with_content(python_file)
        except (SyntaxError, UnicodeDecodeError):
            continue

        file_results = analyze_code_imports(
            code=code,
            file_path=python_file,
            requirements_names=requirements_names,
            uninstalled_libs=uninstalled_libs,
            package_dist_cache=package_dist_cache,
            skip_pypi_check=skip_pypi_check,
            parsed_ast=parsed_ast,
            covered_packages=covered_packages,
        )

        # Filter to only include first occurrence of each package
        for result in file_results:
            if result.import_name not in visited_packages:
                visited_packages.add(result.import_name)
                all_results.append(result)

    return all_results, uninstalled_libs


# Helper functions to extend packaging.requirements.Requirement functionality
def requirement_to_text(req: Requirement) -> str:
    """Convert a Requirement to text format."""
    return str(req)


def requirement_from_text(text: str) -> Optional[Requirement]:
    """Create a Requirement from text, handling simple cases gracefully."""
    try:
        text = text.strip()
        if not text:
            return None
        return Requirement(text)
    except Exception:
        return None


def requirement_to_dict(req: Requirement) -> dict:
    """Convert a Requirement to comprehensive dictionary format."""
    # Parse specifiers into a more detailed format
    specifiers = []

    if req.specifier:
        for spec in req.specifier:
            specifiers.append({"operator": spec.operator, "version": spec.version})

    return {
        "name": req.name,
        "specifiers": specifiers,
        "extras": list(req.extras) if req.extras else [],
        "marker": str(req.marker) if req.marker else None,
        "url": req.url,
        "raw_requirement": str(req),
        "installed_version": get_installed_version(req.name),
    }


def requirement_from_dict(data: dict) -> Requirement:
    """Create a Requirement from dictionary format."""
    # Check if we have the raw requirement string (preferred)
    if "raw_requirement" in data and data["raw_requirement"]:
        return Requirement(data["raw_requirement"])

    # Fallback: reconstruct from components
    name = data["name"]

    # Check for new specifiers format
    if "specifiers" in data and data["specifiers"]:
        spec_parts = []
        for spec in data["specifiers"]:
            spec_parts.append(f"{spec['operator']}{spec['version']}")
        spec_string = ",".join(spec_parts)
        req_string = f"{name}{spec_string}"
    # Fallback to old version format for backward compatibility
    elif "version" in data and data["version"]:
        req_string = f"{name}=={data['version']}"
    else:
        req_string = name

    # Add extras if present
    if "extras" in data and data["extras"]:
        extras_str = ",".join(data["extras"])
        req_string = f"{name}[{extras_str}]{req_string[len(name) :]}"

    # Add marker if present
    if "marker" in data and data["marker"]:
        req_string = f"{req_string}; {data['marker']}"

    return Requirement(req_string)


def get_installed_version(package_name: str) -> Optional[str]:
    """Get the installed version of a package."""
    try:
        return distribution(package_name).version
    except PackageNotFoundError:
        return None


def create_requirement(name: str, version: Optional[str] = None) -> Requirement:
    """Create a Requirement with optional version specification."""
    if version:
        return Requirement(f"{name}=={version}")
    else:
        return Requirement(name)


# Abstra is the only package that must always keep a fixed (==) version in
# requirements.txt, so it's never touched by the "remove fixed version"
# operations regardless of the input.
ABSTRA_PACKAGE_NAME = "abstra"


def has_exact_version(req: Requirement) -> bool:
    """Check if a Requirement has a fixed (==) version specifier."""
    if not req.specifier:
        return False
    return any(spec.operator == "==" for spec in req.specifier)


def strip_exact_version(req: Requirement) -> Requirement:
    """Remove == specifiers from a Requirement while preserving extras,
    markers, url and any non-exact specifiers (e.g. >=, <)."""
    parts: List[str] = [req.name]

    if req.extras:
        parts.append(f"[{','.join(sorted(req.extras))}]")

    if req.url:
        parts.append(f" @ {req.url}")
    else:
        other_specs = [s for s in req.specifier if s.operator != "=="]
        if other_specs:
            parts.append(",".join(f"{s.operator}{s.version}" for s in other_specs))

    base = "".join(parts)
    if req.marker:
        base = f"{base}; {req.marker}"

    return Requirement(base)


def iter_uninstall_requirement(req: Requirement) -> Iterator[str]:
    """Uninstall a requirement package, yielding each line of pip output.

    Use this when you need to stream output in real time (e.g. an SSE HTTP
    response). If you don't need streaming, use uninstall_requirement() —
    it returns the full output as a list and is simpler to consume.
    """
    installed_version = get_installed_version(req.name)
    if not installed_version:
        return

    if os.getenv("ABSTRA_RUNNING_IN_WINDOWS_APP"):
        yield from __uninstall_from_standalone(req)
    else:
        yield from __uninstall_from_lib(req)
    _PackagesDistributionsCache.invalidate()
    _TransitiveDependenciesCache.invalidate()
    RequirementsChangeNotifier.notify()


def uninstall_requirement(req: Requirement) -> List[str]:
    """Uninstall a requirement package and return the full pip output as a list of lines.

    Convenience wrapper around iter_uninstall_requirement() for callers that
    don't need real-time streaming.
    """
    return list(iter_uninstall_requirement(req))


def __uninstall_from_standalone(req: Requirement):
    cmd = [
        "uninstall",
        "-y",
        requirement_to_text(req),
        "--target",
        os.environ["ABSTRA_BUNDLED_APP_PACKAGES_FOLDER"],
    ]

    if pip_main(cmd) != 0:
        yield f"Failed to uninstall {requirement_to_text(req)} from standalone\n"
    else:
        yield "Uninstallation finished successfully\n\n"


def __uninstall_from_lib(req: Requirement):
    yield from stream_output([sys.executable, "-m", "pip", "uninstall", "-y", req.name])


def get_requirements_lint_markers(code: str) -> List[dict]:
    """
    Parse code for imports not in requirements.txt.
    Returns Monaco-compatible lint markers.

    Uses the shared analyze_code_imports() function with PyPI check disabled
    for performance (this is called frequently in the editor).

    Args:
        code: The Python source code to analyze

    Returns:
        List of dicts with: line, column, until_line, until_column, message, severity
    """
    # Use shared analysis with PyPI check disabled for editor performance
    results = analyze_code_imports(code, skip_pypi_check=True)

    markers: List[dict] = []
    for result in results:
        # Only show missing_in_requirements and unknown (potential issues)
        if result.status in ("missing_in_requirements", "unknown"):
            markers.append(
                {
                    "line": result.line,
                    "column": result.col_start + 1,
                    "until_line": result.line,
                    "until_column": result.col_end + 1,
                    "message": f"'{result.import_name}' is imported but not in requirements.txt",
                    "severity": "warning",
                }
            )

    return markers


@dataclass
class RequirementRecommendation:
    requirement: Requirement
    reason_file: Path
    reason_line: int
    reason_code: str

    def to_dict(self):
        """Convert to comprehensive dictionary format."""
        return {
            **requirement_to_dict(self.requirement),
            "reason_file": str(self.reason_file),
            "reason_line": self.reason_line,
            "reason_code": self.reason_code,
        }

    def __hash__(self) -> int:
        return hash(
            f"{requirement_to_text(self.requirement)}/{self.reason_file}/{self.reason_line}"
        )


@dataclass
class Requirements:
    libraries: List[Requirement]

    def to_text(self):
        return "\n".join([requirement_to_text(lib) for lib in self.libraries])

    @staticmethod
    def from_text(text: str):
        libraries = []
        for line_num, line in enumerate(text.splitlines(), 1):
            # Remove inline comments
            if "#" in line:
                line = line.split("#")[0]

            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue

            # Skip -r, -c, --find-links, etc. (pip options)
            if line.startswith(("-r", "-c", "--", "-f", "-i", "-e")):
                continue

            try:
                requirement = requirement_from_text(line)
                if requirement is not None:
                    libraries.append(requirement)
                else:
                    # Check if this is a standalone URL that needs to be converted
                    if line.startswith(("http://", "https://", "git+", "file:///")):
                        try:
                            # Try to extract package name from URL
                            package_name = Requirements._extract_package_name_from_url(
                                line
                            )
                            if package_name:
                                # Convert to proper format: package @ url
                                proper_format = f"{package_name} @ {line}"
                                requirement = requirement_from_text(proper_format)
                                if requirement is not None:
                                    libraries.append(requirement)
                                    continue
                        except Exception:
                            pass

                    # Log parsing error but continue
                    print(
                        f"Warning: Could not parse requirement on line {line_num}: '{line}'"
                    )
            except Exception as e:
                # Check if this is a standalone URL that needs to be converted
                if line.startswith(("http://", "https://", "git+", "file:///")):
                    try:
                        # Try to extract package name from URL
                        package_name = Requirements._extract_package_name_from_url(line)
                        if package_name:
                            # Convert to proper format: package @ url
                            proper_format = f"{package_name} @ {line}"
                            requirement = requirement_from_text(proper_format)
                            if requirement is not None:
                                libraries.append(requirement)
                                continue
                    except Exception:
                        pass

                # Log parsing error but continue
                print(
                    f"Warning: Could not parse requirement on line {line_num}: '{line}' - {e}"
                )
                continue

        return Requirements(libraries=libraries)

    @staticmethod
    def _extract_package_name_from_url(url: str) -> Optional[str]:
        """Extract a reasonable package name from a URL.

        This is a heuristic approach since URLs don't inherently contain package names.
        """
        import re
        from urllib.parse import urlparse

        # Remove common URL prefixes
        clean_url = url
        if clean_url.startswith("git+"):
            clean_url = clean_url[4:]

        parsed = urlparse(clean_url)
        path = parsed.path

        # Try to extract from common patterns
        patterns = [
            r"/([^/]+)\.git$",  # git repos: /package.git
            r"/([^/]+)\.zip$",  # zip files: /package.zip
            r"/([^/]+)\.tar\.gz$",  # tar.gz files: /package.tar.gz
            r"/([^/]+)[-_][\d\.]",  # versioned packages: /package-1.0.0
            r"/([^/]+)$",  # last path component
        ]

        for pattern in patterns:
            match = re.search(pattern, path)
            if match:
                name = match.group(1)
                # Clean up the name
                name = re.sub(r"[-_]", "-", name)  # normalize separators
                name = re.sub(r"[^a-zA-Z0-9\-\.]", "", name)  # remove invalid chars
                if name and not name.startswith("."):
                    return name

        # Fallback: use hostname
        if parsed.hostname:
            return f"package-from-{parsed.hostname.replace('.', '-')}"

        return None

    def to_dict(self):
        """Convert to comprehensive dictionary format."""
        return [requirement_to_dict(lib) for lib in self.libraries]

    @staticmethod
    def from_dict(data: list):
        return Requirements(libraries=[requirement_from_dict(lib) for lib in data])

    def add(self, name: str, version: Optional[str] = None):
        if self.has(name, version):
            return
        self.libraries.append(create_requirement(name, version))

    def update(self, name: str, version: str):
        self.libraries = [
            lib if lib.name != name else create_requirement(name, version)
            for lib in self.libraries
        ]

    def remove_fixed_version(self, name: str) -> bool:
        """Remove the exact (==) version specifier from a single requirement.

        Preserves the original order of requirements and the rest of the
        requirement metadata (extras, markers, url, non-exact specifiers).

        The `abstra` package is always preserved as-is, regardless of the
        provided name, since it must keep a fixed version in requirements.txt.

        Returns True if a change was made, False otherwise.
        """
        normalized_name = pip_name(name)
        if normalized_name == ABSTRA_PACKAGE_NAME:
            return False

        changed = False
        new_libraries: List[Requirement] = []
        for lib in self.libraries:
            if pip_name(lib.name) == normalized_name and has_exact_version(lib):
                new_libraries.append(strip_exact_version(lib))
                changed = True
            else:
                new_libraries.append(lib)
        self.libraries = new_libraries
        return changed

    def remove_all_fixed_versions(self, skip: Optional[Set[str]] = None) -> List[str]:
        """Remove the exact (==) version specifier from every requirement,
        except those whose normalized name appears in `skip`.

        The `abstra` package is always implicitly skipped (regardless of the
        contents of `skip`), since it must keep a fixed version in
        requirements.txt.

        Returns the list of requirement names that were updated (preserving
        order).
        """
        skip_normalized: Set[str] = {pip_name(s) for s in (skip or set())}
        skip_normalized.add(ABSTRA_PACKAGE_NAME)
        updated: List[str] = []
        new_libraries: List[Requirement] = []
        for lib in self.libraries:
            if pip_name(lib.name) not in skip_normalized and has_exact_version(lib):
                new_libraries.append(strip_exact_version(lib))
                updated.append(lib.name)
            else:
                new_libraries.append(lib)
        self.libraries = new_libraries
        return updated

    def delete(self, name: str):
        self.libraries = [lib for lib in self.libraries if lib.name != name]

    def delete_duplicates(self, name: str, version: Optional[str]):
        # For packaging.requirements.Requirement, we need to extract version from specifier
        self.libraries = [
            lib
            for lib in self.libraries
            if not (
                lib.name == name and self._get_version_from_requirement(lib) == version
            )
        ]

    def _get_version_from_requirement(self, req: Requirement) -> Optional[str]:
        """Extract exact version from a Requirement's specifier.

        Returns the exact version if the requirement has an == specifier,
        otherwise returns None.
        """
        if req.specifier:
            for spec in req.specifier:
                if spec.operator == "==":
                    return spec.version
        return None

    def _get_requirement_signature(self, req: Requirement) -> str:
        """Get a unique signature for a requirement that includes all specifiers.

        This is used for more accurate duplicate detection.
        """
        return str(req)

    def has(self, lib_name: str, version: Optional[str] = None):
        """Check if a requirement is present.

        If version is None, checks for any requirement with the given name.
        If version is provided, checks for exact version match (== specifier).
        """
        for lib in self.libraries:
            if lib.name == lib_name:
                if version is None:
                    return True
                req_version = self._get_version_from_requirement(lib)
                if req_version == version:
                    return True
        return False

    def has_requirement_like(self, req: Requirement) -> bool:
        """Check if a requirement with the same signature already exists."""
        req_signature = self._get_requirement_signature(req)
        for lib in self.libraries:
            if self._get_requirement_signature(lib) == req_signature:
                return True
        return False

    def ensure(self, lib_name: str, version: Optional[str] = None):
        if (
            self.has(lib_name)
            and version is not None
            and not self.has(lib_name, version)
        ):
            self.update(lib_name, version)
        elif not self.has(lib_name):
            self.add(lib_name, version)

    def get(self, lib_name: str):
        for lib in self.libraries:
            if lib.name == lib_name:
                return self._get_version_from_requirement(lib)
        return None

    def get_duplicates(self) -> Dict[str, List[Requirement]]:
        """Get requirements that have duplicate package names.

        Groups requirements by package name, returns only groups with more than one requirement.
        This allows for sophisticated duplicate detection that considers different version specifiers.
        """
        duplicates = {}
        for lib in self.libraries:
            if not isinstance(duplicates.get(lib.name), list):
                duplicates[lib.name] = [lib]
            else:
                duplicates[lib.name].append(lib)
        return {k: v for k, v in duplicates.items() if len(v) > 1}

    def __install_from_lib(self):
        cmd = [sys.executable, "-m", "pip", "install"]

        for lib in self.libraries:
            if lib.name == "abstra":
                continue

            cmd.append(requirement_to_text(lib))

        yield from stream_output(cmd)

    def __install_from_standalone(self):
        # pip is not thread safe, but we can use a lock to avoid conflicts
        print("Installing from standalone")
        with install_lock:
            for lib in self.libraries:
                if lib.name == "abstra":
                    continue

                cmd = [
                    "install",
                    requirement_to_text(lib),
                    "--target",
                    os.environ["ABSTRA_BUNDLED_APP_PACKAGES_FOLDER"],
                ]

                yield f"Installing {requirement_to_text(lib)} in abstra standalone...\n"

                res = pip_main(cmd)
                req_version = self._get_version_from_requirement(lib)
                if res != 0:
                    yield f"Failed to install {lib.name}=={req_version}\n"
                else:
                    yield "Installation finished successfully\n\n"

    def iter_install(self) -> Iterator[str]:
        """Install all requirements, yielding each line of pip output as it is produced.

        Use this when you need to stream output in real time (e.g. an SSE HTTP
        response). If you don't need streaming, use install() — it returns the
        full output as a list and is simpler to consume.
        """
        if os.getenv("ABSTRA_RUNNING_IN_BUNDLED_APP"):
            yield from self.__install_from_standalone()
        else:
            yield from self.__install_from_lib()
        _PackagesDistributionsCache.invalidate()
        _TransitiveDependenciesCache.invalidate()
        RequirementsChangeNotifier.notify()

    def install(self) -> List[str]:
        """Install all requirements and return the full pip output as a list of lines.

        Convenience wrapper around iter_install() for callers that don't need
        real-time streaming.
        """
        return list(self.iter_install())


@dataclass
class RequirementsRepository:
    @classmethod
    def get_file_path(cls):
        return Settings.root_path / "requirements.txt"

    @classmethod
    def get_recommendation(cls) -> List[RequirementRecommendation]:
        """
        Get recommendations for packages to add to requirements.txt.

        Uses the shared analyze_project_imports() function and converts
        the results to RequirementRecommendation objects.
        """
        # Use shared analysis (skip PyPI check as we only recommend installed packages)
        results, _ = analyze_project_imports(skip_pypi_check=True)

        recommendations: Set[RequirementRecommendation] = set()

        for result in results:
            # Only recommend packages that are missing from requirements
            if result.status != "missing_in_requirements":
                continue

            # For installed packages, get the version
            try:
                version = distribution(result.package_name).version
            except PackageNotFoundError:
                version = None

            recommendations.add(
                RequirementRecommendation(
                    requirement=create_requirement(result.package_name, version),
                    reason_file=result.file_path or Path("."),
                    reason_line=result.line,
                    reason_code=result.code,
                )
            )

        return list(recommendations)

    @classmethod
    def save(cls, requirements: Requirements):
        temp_file = Path(mkdtemp()) / "requirements.txt"

        with temp_file.open("w") as f:
            f.write(requirements.to_text())
        move(str(temp_file), cls.get_file_path())

    @classmethod
    def load(cls) -> Requirements:
        file = cls.get_file_path()
        if file.exists():
            requirements_content = file.read_text(encoding="utf-8")
            return Requirements.from_text(requirements_content)
        else:
            return Requirements(libraries=[])

    @classmethod
    def ensure(cls, lib_name: str):
        requirements = cls.load()
        try:
            requirements.ensure(lib_name, distribution(lib_name).version)
        except PackageNotFoundError:
            # Package not found, skip
            pass
        cls.save(requirements)


@dataclass
class RequirementsValidationResult:
    """Result of validating requirements.txt content."""

    valid: bool
    error: Optional[str]
    missing_packages: Optional[List[str]]

    def to_dict(self) -> dict:
        return {
            "valid": self.valid,
            "error": self.error,
            "missing_packages": self.missing_packages,
        }


def validate_requirements_content(content: str) -> RequirementsValidationResult:
    """
    Validate that the proposed requirements.txt content includes all packages
    that are used in the project.

    Uses the same analysis as the linter (analyze_project_imports) to find
    all imports in the project and checks if they are covered by the proposed
    new requirements.txt content.

    Args:
        content: The proposed new content for requirements.txt

    Returns:
        RequirementsValidationResult with validation status and any missing packages
    """
    # Parse the new requirements content
    try:
        new_requirements = Requirements.from_text(content)
    except Exception as e:
        return RequirementsValidationResult(
            valid=False,
            error=f"Invalid requirements.txt syntax: {e}",
            missing_packages=None,
        )

    # Get normalized names from the new requirements
    new_names = {pip_name(lib.name) for lib in new_requirements.libraries}

    # Use the same analysis as the linter to find all necessary packages
    try:
        results, _ = analyze_project_imports(skip_pypi_check=True)
    except Exception:
        # If analysis fails, allow the operation
        return RequirementsValidationResult(
            valid=True,
            error=None,
            missing_packages=None,
        )

    # Find packages that are used in the code but missing from the new requirements
    # We check packages that are currently installed (status "ok" or "missing_in_requirements")
    missing_packages = set()

    for result in results:
        if result.status in ("ok", "missing_in_requirements"):
            normalized_name = pip_name(result.package_name)
            if normalized_name not in new_names:
                missing_packages.add(result.package_name)

    if missing_packages:
        missing_list = ", ".join(sorted(missing_packages))
        return RequirementsValidationResult(
            valid=False,
            error=(
                f"The following packages are used in the project but missing from "
                f"requirements.txt: {missing_list}. Please add them to requirements.txt."
            ),
            missing_packages=sorted(missing_packages),
        )

    return RequirementsValidationResult(
        valid=True,
        error=None,
        missing_packages=None,
    )
