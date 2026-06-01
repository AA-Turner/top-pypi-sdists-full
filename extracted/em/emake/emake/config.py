"""Parse pyproject.toml for project configuration."""

import difflib
import os
import sys
from collections import defaultdict
from collections.abc import Mapping
from importlib import resources
from io import BytesIO
from pathlib import Path
from tomllib import TOMLDecodeError, load
from typing import (
    Any,
    cast,
)

from packaging.markers import Marker
from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.utils import canonicalize_name
from packaging.version import Version


class ProjectConfig:
    """Represents project configuration from pyproject.toml."""

    def __init__(self, file: Path | BytesIO | None = None) -> None:
        """Initialize config from pyproject.toml.

        Args:
            path: Path to pyproject.toml. If None, searches current directory.
            file: File-like object to load from instead of path.
        """
        self._data: dict[str, Any]  # pyright: ignore[reportExplicitAny]
        if isinstance(file, BytesIO):
            self._data = load(file)
            return

        elif file is None:
            file = self._find_pyproject()

        with open(file, "rb") as f:
            self._data = load(f)

    def _find_pyproject(self) -> Path:
        """Find pyproject.toml in current or parent directories."""
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            pyproject = parent / "pyproject.toml"
            if pyproject.exists():
                return pyproject

        raise FileNotFoundError("pyproject.toml not found")

    @property
    def name(self) -> str | None:
        """Package name from [project].name."""
        project: dict[str, str | None] | None = self._data.get("project")
        if project is None:
            return None

        return project.get("name")

    @property
    def description(self) -> str | None:
        """Package description from [project].description."""
        project: dict[str, str | None] | None = self._data.get("project")
        if project is None:
            return None

        return project.get("description")

    @property
    def license(self) -> str | None:
        """Package license from [project].license."""
        project: dict[str, str | None] | None = self._data.get("project")
        if project is None:
            return None

        return project.get("license")

    @property
    def authors(self) -> list[tuple[str | None, str | None]] | None:
        """Package name from [project].name."""
        project: dict[str, list[dict[str, str | None]] | None] | None = self._data[  # pyright: ignore[reportAny]
            "project"
        ]
        if project is None:
            return None

        authors = project.get("authors")
        if authors is None:
            return None

        res: list[tuple[str | None, str | None]] = []
        for author in authors:
            name = author.get("name")
            email = author.get("email")
            res.append((name, email))

        return res

    @property
    def version(self) -> str | None:
        """Package version from [project].version."""
        project: dict[str, object] | None = self._data.get("project")
        if project is None:
            return None

        version_val = project["version"]
        assert isinstance(version_val, str), version_val
        return version_val

    @property
    def emake(self) -> dict[str, list[str]]:
        tool: dict[str, object] | None = self._data.get("tool")
        if tool is None:
            return {}

        value = tool.get("emake")
        if value is None:
            return {}

        assert isinstance(value, dict), value
        return cast(dict[str, list[str]], value)

    @property
    def extras(self) -> dict[str, list[str]] | None:
        """Dict of optional dependencies from [project.optional-dependencies]."""
        project: dict[str, dict[str, list[str]]] | None = self._data.get("project")
        if project is None:
            return None

        return project.get("optional-dependencies")

    @property
    def build_system_requires(self) -> list[str]:
        """Build system requires from [build-system].requires."""
        build_system: dict[str, list[str] | None] | None = self._data.get(
            "build-system"
        )
        if build_system is None:
            return []

        return build_system.get("requires") or []

    @property
    def build_backend(self) -> str | None:
        """Build backend from [build-system].build-backend."""
        build_system: dict[str, str | None] | None = self._data.get("build-system")
        if build_system is None:
            return None

        return build_system.get("build-backend")

    @property
    def pyright_exclude(self) -> list[str] | None:
        """Pyright exclude from [tool.pyright].exclude."""
        tool: dict[str, object] | None = self._data.get("tool")
        if tool is None:
            return None

        pyright_val = tool.get("pyright")
        if pyright_val is None:
            return None

        assert isinstance(pyright_val, dict), pyright_val
        pyright_dict = cast(dict[str, list[str] | None], pyright_val)
        return pyright_dict.get("exclude")

    @property
    def ruff_exclude(self) -> list[str] | None:
        """Ruff exclude from [tool.ruff].exclude."""
        tool: dict[str, object] | None = self._data.get("tool")
        if tool is None:
            return None

        ruff_val = tool.get("ruff")
        if ruff_val is None:
            return None

        assert isinstance(ruff_val, dict), ruff_val
        ruff_dict = cast(dict[str, list[str] | None], ruff_val)
        return ruff_dict.get("exclude")

    @property
    def requires_python(self) -> str | None:
        """Get requires-python from [project] and return the requirement value"""
        project = self._data.get("project", {})  # pyright: ignore[reportAny]
        if project is None:
            return None

        assert isinstance(project, dict), project
        project = cast(dict[str, str], project)
        return project.get("requires-python", None)

    @property
    def minimum_python_version(self) -> str:
        if self.requires_python is None:
            return "3.11"

        return _get_min_version(SpecifierSet(self.requires_python)) or "3.11"


def _get_min_version(spec: SpecifierSet) -> str | None:
    """Get minimum version from a specifier like >=3.8 or ==3.8."""
    version = None
    for s in spec:
        s_version = Version(s.version)
        if s.operator == ">=" and (version is None or s_version < version):
            version = s_version

        if s.operator == "==" and (version is None or s_version < version):
            version = s_version

    return str(version) if version is not None else None


def _specifier_covers(exp_spec: SpecifierSet, act_spec: SpecifierSet) -> bool:
    """Check if actual specifier covers expected.

    For >= specifiers, actual covers expected if actual's min version
    is greater than or equal to expected's min version.
    For == specifiers, actual must also be == (exact match required).
    """
    # Check for == first (exact version match required)
    exp_exact = None
    act_exact = None
    for s in exp_spec:
        if s.operator == "==":
            exp_exact = s.version
            break

    for s in act_spec:
        if s.operator == "==":
            act_exact = s.version
            break

    # If expected is exact, actual must match exactly
    if exp_exact is not None:
        if act_exact is None:
            # Check if actual's >= covers expected's ==
            act_min = _get_min_version(act_spec)
            if act_min is None:
                return False

            return Version(str(act_min)) >= Version(str(exp_exact))
        return exp_exact == act_exact

    # For >= specifiers
    exp_min = _get_min_version(exp_spec)
    act_min = _get_min_version(act_spec)

    if exp_min is None:
        return True

    if act_min is None:
        return False

    return Version(str(act_min)) >= Version(str(exp_min))


def _generate_marker_environments(requires_python: str) -> list[Mapping[str, str]]:
    """Generate marker test environments based on requires_python."""
    spec = SpecifierSet(requires_python)
    min_ver = None
    for s in spec:
        if s.operator == ">=":
            min_ver = s.version
            break

    test_version = str(min_ver) if min_ver else requires_python
    envs: list[Mapping[str, str]] = []
    for p in ["linux", "darwin", "win32"]:
        envs.append(
            {
                "python_version": test_version,
                "python_full_version": f"{test_version}.0",
                "sys_platform": p,
                "platform_system": p.capitalize(),
            }
        )

    return envs


def _marker_covers(
    exp_marker: Marker | None,
    act_marker: Marker | None,
    requires_python: str,
) -> bool:
    """Check if actual marker covers expected marker."""
    if exp_marker == act_marker:
        return True

    if act_marker is None:
        return True

    test_envs = _generate_marker_environments(requires_python)

    for env in test_envs:
        try:
            exp_result = (
                True if exp_marker is None else exp_marker.evaluate(environment=env)
            )
            act_result = act_marker.evaluate(environment=env)

            if exp_result and not act_result:
                return False

        except Exception:  # noqa: S112
            continue

    return True


def requirements_not_satisfied_by(
    expected: list[str],
    actual: list[str],
    requires_python: str,
) -> list[str]:
    """Find requirements not satisfied by actual.

    Compares expected requirements against actual requirements, returning those
    not covered by actual (missing or incompatible versions/markers).
    """
    reqs1 = [Requirement(x) for x in expected]
    reqs2 = [Requirement(x) for x in actual]
    groups1: dict[str, list[Requirement]] = defaultdict(list)
    groups2: dict[str, list[Requirement]] = defaultdict(list)
    for req in reqs1:
        name = canonicalize_name(req.name)
        groups1[name].append(req)

    for req in reqs2:
        name = canonicalize_name(req.name)
        groups2[name].append(req)

    not_covered: list[str] = []
    for name, reqs1_list in groups1.items():
        if name not in groups2:
            # Package missing from actual - add all expected requirements
            for req1 in reqs1_list:
                not_covered.append(str(req1))
            continue

        for req1 in reqs1_list:
            for req2 in groups2[name]:
                if (
                    _marker_covers(req1.marker, req2.marker, requires_python)
                    and set(req1.extras).issubset(set(req2.extras))
                    and _specifier_covers(req1.specifier, req2.specifier)
                ):
                    break

            else:
                not_covered.append(str(req1))

    return not_covered


def diff(workflow: bool, colour: bool) -> int:
    """Compare project's pyproject.toml against template.

    Returns:
        Exit code - 0 if no differences, 1 if differences found.
    """
    template = resources.files("emake").joinpath("pyproject.toml.tpl").read_text()
    failed = 0

    def error(msg: str) -> None:
        nonlocal failed
        if colour or sys.stderr.isatty():
            print("\x1b[31m", end="", file=sys.stderr)

        print(f"ERROR: {msg}", file=sys.stderr)
        if colour or sys.stderr.isatty():
            print("\x1b[00m", end="", file=sys.stderr)

        failed += 1

    def diff_list(
        name: str, expected: list[str] | None, actual: list[str] | None
    ) -> None:
        difference = set(expected or []) - set(actual or [])
        if difference:
            error(f"{name} expected {expected}, got {actual}")

    try:
        project = ProjectConfig()

    except TOMLDecodeError:
        error("pyproject.toml is invalid")
        return failed

    if project.name is None:
        error("'pyproject.toml' does not specify a 'name' value.")

    if project.license is None:
        error("'pyproject.toml' does not specify a 'license' value.")

    if project.requires_python is None:
        error("'pyproject.toml' does not specify a 'requires_python' value.")

    if project.authors is None or not project.authors:
        error("'pyproject.toml' does not specify a 'authors' value.")
        author_name = author_email = "x"

    else:
        author_name, author_email = project.authors[0]

    template_text = template.format(
        name=project.name or "x",
        description=project.description or "x",
        author_name=author_name or "x",
        author_email=author_email or "x",
        license_spdx=project.license,
        python_version=project.requires_python or "3",
    )
    with BytesIO(template_text.encode()) as template_io:
        try:
            template_config = ProjectConfig(template_io)

        except TOMLDecodeError:
            error("Generated invalid pyproject.toml")
            print("======================================", file=sys.stderr)
            print(template_text, file=sys.stderr)
            print("======================================", file=sys.stderr)
            return failed

        if project.requires_python is not None:
            if project.extras is None or "test" not in project.extras:
                error("'test' optional dependency group is missing.")

            elif not project.emake.get("test", None) and requirements_not_satisfied_by(
                ["pytest"], project.extras["test"], project.requires_python
            ):
                error("pytest is not installed in the 'test' extras group.")

            missing = requirements_not_satisfied_by(
                template_config.build_system_requires,
                project.build_system_requires,
                project.requires_python,
            )
            if missing:
                error(
                    f"build-system.requires: missing coverage for {', '.join(missing)}"
                )

        if template_config.build_backend != project.build_backend:
            error(
                f"build-system.build-backend: expected {template_config.build_backend}, got {project.build_backend}"
            )

        diff_list(
            "tool.pyright.exclude",
            template_config.pyright_exclude,
            project.pyright_exclude,
        )
        diff_list(
            "tool.ruff.exclude",
            template_config.ruff_exclude,
            project.ruff_exclude,
        )

    if not workflow:
        return failed

    if not os.path.exists(".github/workflows/build.yml"):
        error(".github/workflows/build.yml is missing")
        return failed

    template = resources.files("emake").joinpath("build.yml.tpl").read_text()
    with open(".github/workflows/build.yml") as f:
        diffs = difflib.unified_diff(
            f.read().splitlines(keepends=False),
            template.format(project_name=project.name or "x").splitlines(
                keepends=False
            ),
            fromfile=".github/workflows/build.yml",
            tofile=".github/workflows/build.yml.tpl",
        )
    for line in diffs:
        if colour or sys.stderr.isatty():
            if line.startswith("-"):
                print("\x1b[31m", end="", file=sys.stderr)

            elif line.startswith("+"):
                print("\x1b[32m", end="", file=sys.stderr)

        print(line, file=sys.stderr)
        if colour or sys.stderr.isatty():
            print("\x1b[00m", end="", file=sys.stderr)

    if diffs:
        failed += 1

    return failed
