from __future__ import annotations

import importlib.metadata
import os
import re
import subprocess
import zipfile
from pathlib import Path
from typing import TYPE_CHECKING, Any, NamedTuple

import pytest

if TYPE_CHECKING:
    from collections.abc import Mapping

# The integration projects install the hook from this checkout (not from PyPI),
# so the tests exercise the code of the working tree.
REPO_ROOT = Path(__file__).resolve().parents[2]
# The projects build with the hatchling of the test environment, so the
# hatchling matrix of the CI is exercised by real builds and not only by
# the Python API.
HATCHLING_VERSION = importlib.metadata.version("hatchling")
WARN_ONLY_ENV = "HATCHLING_AUTOEXTRAS_WARN_ONLY"


def run_uv_build(
    path: Path, env: Mapping[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    r"""Run ``uv build`` in a project, without checking the result.

    uv does not detect the changes of the sources of a local directory
    (the cache key is ``pyproject.toml``), so the hook is refreshed to
    build with the current code.

    Args:
        path: The path of the project.
        env: Environment variables added to the environment of the build.

    Returns:
        The completed process, with the captured output.
    """
    return subprocess.run(
        ["uv", "build", "--refresh-package", "hatchling-autoextras-hook"],  # noqa: S607
        cwd=path,
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, **(env or {})},
    )


def build_minimal_project(
    path: Path, config: str = "", extra_extras: str = "", dynamic: str = '"maintainers"'
) -> None:
    r"""Create a minimal project.

    Args:
        path: The path where to build the minimal project.
        config: Extra lines for the ``autoextras`` hook table.
        extra_extras: Extra lines for the optional dependencies table.
        dynamic: The content of the ``dynamic`` list of the project.
    """
    path.joinpath("pyproject.toml").write_text(
        f"""[build-system]
requires = ["hatchling=={HATCHLING_VERSION}", "hatchling-autoextras-hook @ {REPO_ROOT.as_uri()}"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.sdist]
only-include = ["src"]

[project]
name = "testpkg"
version = "0.1.0"
description = "Test project"
dynamic = [{dynamic}]
readme = "README.md"
requires-python = ">=3.11"

[project.optional-dependencies]
numpy = [ "numpy>=2.0" ]
dev = [ "pytest>=9.0" ]
{extra_extras}

[tool.hatch.metadata.hooks.autoextras]
{config}
""",
        encoding="utf-8",
    )

    path.joinpath("README.md").write_text("Test package", encoding="utf-8")

    # Minimal module
    path_pkg = path.joinpath("src").joinpath("testpkg")
    path_pkg.mkdir(exist_ok=True, parents=True)
    path_pkg.joinpath("__init__.py").write_text("", encoding="utf-8")


def find_wheel_path(path: Path) -> Path:
    r"""Find the wheel path.

    Args:
        path: The project path.

    Returns:
        The wheel path.
    """
    dist_dir = path.joinpath("dist")
    wheels = list(dist_dir.glob("*.whl"))
    assert len(wheels) == 1, "Expected exactly one wheel"
    return wheels[0]


def read_metadata(path: Path) -> str:
    r"""Read the METADATA file of a wheel.

    Args:
        path: The path to the wheel.

    Returns:
        The content of the METADATA file.
    """
    with zipfile.ZipFile(path) as zf:
        namelist = zf.namelist()
        metadata_files = [n for n in namelist if n.endswith("METADATA")]
        assert metadata_files, "METADATA file not found in wheel"
        return zf.read(metadata_files[0]).decode()


def read_extras(path: Path) -> dict[str, list[str]]:
    r"""Read the extras of the METADATA of a wheel.

    Args:
        path: The path to the wheel.

    Returns:
        The dependencies of each extra, in the order of the METADATA.
        An extra without dependency maps to an empty list.
    """
    extras: dict[str, list[str]] = {}
    lines = read_metadata(path).splitlines()
    for line in lines:
        if line.startswith("Provides-Extra: "):
            extras[line.removeprefix("Provides-Extra: ")] = []
    for line in lines:
        if line.startswith("Requires-Dist: ") and (
            match := re.fullmatch(r"Requires-Dist: (.+); extra == '(.+)'", line)
        ):
            extras[match.group(2)].append(match.group(1))
    return extras


def build_project(
    path: Path,
    config: str = "",
    extra_extras: str = "",
    env: Mapping[str, str] | None = None,
    dynamic: str = '"maintainers"',
) -> subprocess.CompletedProcess[str]:
    r"""Build a project and return the result without checking it.

    Args:
        path: The path where to build the project.
        config: Extra lines for the ``autoextras`` hook table.
        extra_extras: Extra lines for the optional dependencies table.
        env: Environment variables added to the environment of the build.
        dynamic: The content of the ``dynamic`` list of the project.

    Returns:
        The completed process, with the captured output.
    """
    path.mkdir(exist_ok=True, parents=True)
    build_minimal_project(path, config=config, extra_extras=extra_extras, dynamic=dynamic)
    return run_uv_build(path, env)


def build_extras(path: Path, config: str = "", extra_extras: str = "") -> dict[str, list[str]]:
    r"""Build a project and return the extras of its wheel.

    Args:
        path: The path where to build the project.
        config: Extra lines for the ``autoextras`` hook table.
        extra_extras: Extra lines for the optional dependencies table.

    Returns:
        The dependencies of each extra of the wheel.
    """
    build_project(path, config=config, extra_extras=extra_extras).check_returncode()
    return read_extras(find_wheel_path(path))


def output(result: subprocess.CompletedProcess[str]) -> str:
    r"""Return the output of a build (standard output and error).

    Args:
        result: The completed process.

    Returns:
        The standard output followed by the standard error.
    """
    return result.stdout + result.stderr


DEFAULT_EXTRAS = {
    "all": ["numpy>=2.0", "pytest>=9.0"],
    "dev": ["pytest>=9.0"],
    "numpy": ["numpy>=2.0"],
}

# Hatchling resolves the self-references of an extra (``pkg[dev]``) from
# 1.23.0; the older versions keep them as is in the METADATA.
RESOLVES_SELF_REFERENCES = tuple(int(n) for n in HATCHLING_VERSION.split(".")[:2]) >= (1, 23)
SELF_REFERENCE_ALL = (
    ["numpy>=2.0", "pytest>=9.0", "sphinx"]
    if RESOLVES_SELF_REFERENCES
    else ["numpy>=2.0", "sphinx", "testpkg[dev]"]
)


def build_failure(
    tmp_path_factory: pytest.TempPathFactory, name: str, **kwargs: Any
) -> subprocess.CompletedProcess[str]:
    r"""Build a project in a new directory, without checking the result.

    Args:
        tmp_path_factory: The factory of temporary directories.
        name: The name of the directory of the project.
        **kwargs: The arguments of ``build_project``.

    Returns:
        The completed process, with the captured output.
    """
    return build_project(tmp_path_factory.mktemp(name) / "project", **kwargs)


#######################################
#     Builds that succeed             #
#######################################


def test_autoextras_integration(tmp_path: Path) -> None:
    r"""The generated extra merges all the optional dependencies and the
    original extras are kept."""
    assert build_extras(tmp_path / "project") == DEFAULT_EXTRAS


def test_autoextras_integration_custom_name(tmp_path: Path) -> None:
    assert build_extras(tmp_path / "project", config='extra-name = "complete"') == {
        "complete": ["numpy>=2.0", "pytest>=9.0"],
        "dev": ["pytest>=9.0"],
        "numpy": ["numpy>=2.0"],
    }


def test_autoextras_integration_exclude(tmp_path: Path) -> None:
    r"""Excluded extras must not contribute to the combined extra, but
    must still be provided as extras."""
    assert build_extras(
        tmp_path / "project", config='extra-name = "complete"\nexclude = ["dev"]'
    ) == {"complete": ["numpy>=2.0"], "dev": ["pytest>=9.0"], "numpy": ["numpy>=2.0"]}


def test_autoextras_integration_overwrite(tmp_path: Path) -> None:
    r"""With overwrite enabled, the existing extra is replaced."""
    assert (
        build_extras(
            tmp_path / "project", config="overwrite = true", extra_extras='all = [ "old-dep" ]'
        )
        == DEFAULT_EXTRAS
    )


def test_autoextras_integration_normalized_extra_name(tmp_path: Path) -> None:
    r"""An extra name that is not normalized is normalized by
    hatchling."""
    assert build_extras(tmp_path / "project", config='extra-name = "Full_Extra"') == {
        "dev": ["pytest>=9.0"],
        "full-extra": ["numpy>=2.0", "pytest>=9.0"],
        "numpy": ["numpy>=2.0"],
    }


def test_autoextras_integration_exclude_normalized(tmp_path: Path) -> None:
    r"""The excluded names are matched like hatchling does."""
    assert build_extras(
        tmp_path / "project",
        config='exclude = ["DEV"]',
        extra_extras='my_extra = [ "rich>=13" ]',
    ) == {
        "all": ["numpy>=2.0", "rich>=13"],
        "dev": ["pytest>=9.0"],
        "my-extra": ["rich>=13"],
        "numpy": ["numpy>=2.0"],
    }


def test_autoextras_integration_self_reference_is_deduplicated(tmp_path: Path) -> None:
    r"""An extra that references the package is copied as is and
    resolved by hatchling: the numpy dependency is not duplicated."""
    extras = build_extras(tmp_path / "project", extra_extras='full = [ "testpkg[numpy]" ]')
    assert extras["all"].count("numpy>=2.0") == 1


def test_autoextras_integration_self_reference_excluded(tmp_path: Path) -> None:
    r"""Excluding an extra does not remove it from an extra that depends
    on it; the result depends on the hatchling version."""
    extras = build_extras(
        tmp_path / "project",
        config='exclude = ["dev"]',
        extra_extras='docs = [ "sphinx", "testpkg[dev]" ]',
    )
    assert extras["all"] == SELF_REFERENCE_ALL


#######################################
#     Builds that fail                #
#######################################


@pytest.fixture(scope="module")
def existing_extra(tmp_path_factory: pytest.TempPathFactory) -> subprocess.CompletedProcess[str]:
    return build_failure(tmp_path_factory, "existing", extra_extras='all = [ "old-dep" ]')


@pytest.fixture(scope="module")
def existing_extra_spelling(
    tmp_path_factory: pytest.TempPathFactory,
) -> subprocess.CompletedProcess[str]:
    return build_failure(tmp_path_factory, "spelling", extra_extras='All = [ "old-dep" ]')


@pytest.fixture(scope="module")
def unknown_option(tmp_path_factory: pytest.TempPathFactory) -> subprocess.CompletedProcess[str]:
    return build_failure(tmp_path_factory, "unknown", config='excludes = ["dev"]')


@pytest.fixture(scope="module")
def old_option_name(tmp_path_factory: pytest.TempPathFactory) -> subprocess.CompletedProcess[str]:
    return build_failure(tmp_path_factory, "old-name", config='group-name = "complete"')


@pytest.fixture(scope="module")
def unmatched_exclude(
    tmp_path_factory: pytest.TempPathFactory,
) -> subprocess.CompletedProcess[str]:
    return build_failure(tmp_path_factory, "unmatched", config='exclude = ["tset"]')


@pytest.fixture(scope="module")
def blank_dependency(tmp_path_factory: pytest.TempPathFactory) -> subprocess.CompletedProcess[str]:
    return build_failure(tmp_path_factory, "blank", extra_extras='docs = [ "sphinx", " " ]')


@pytest.fixture(scope="module")
def dynamic_and_static(
    tmp_path_factory: pytest.TempPathFactory,
) -> subprocess.CompletedProcess[str]:
    return build_failure(tmp_path_factory, "dynamic", dynamic='"optional-dependencies"')


def test_autoextras_integration_existing_extra_fails(
    existing_extra: subprocess.CompletedProcess[str],
) -> None:
    r"""The build must fail if the extra exists and overwrite is not
    enabled."""
    assert existing_extra.returncode != 0


def test_autoextras_integration_existing_extra_message(
    existing_extra: subprocess.CompletedProcess[str],
) -> None:
    assert "Cannot create the 'all' extra: 'all' already exists" in output(existing_extra)


def test_autoextras_integration_existing_extra_other_spelling_fails(
    existing_extra_spelling: subprocess.CompletedProcess[str],
) -> None:
    r"""An existing extra with another spelling of the name is a
    conflict, detected by the hook."""
    assert existing_extra_spelling.returncode != 0


def test_autoextras_integration_existing_extra_other_spelling_message(
    existing_extra_spelling: subprocess.CompletedProcess[str],
) -> None:
    assert "Cannot create the 'all' extra: 'All' already exists" in output(existing_extra_spelling)


def test_autoextras_integration_unknown_option_fails(
    unknown_option: subprocess.CompletedProcess[str],
) -> None:
    r"""An unknown option must fail the build."""
    assert unknown_option.returncode != 0


def test_autoextras_integration_unknown_option_message(
    unknown_option: subprocess.CompletedProcess[str],
) -> None:
    r"""The error names the unknown option."""
    assert "Unknown option(s) in [tool.hatch.metadata.hooks.autoextras]: ['excludes']" in output(
        unknown_option
    )


def test_autoextras_integration_old_option_name_fails(
    old_option_name: subprocess.CompletedProcess[str],
) -> None:
    r"""The old name of the option, group-name, must fail the build."""
    assert old_option_name.returncode != 0


def test_autoextras_integration_old_option_name_message(
    old_option_name: subprocess.CompletedProcess[str],
) -> None:
    r"""The error names the old option and lists the valid ones."""
    assert (
        "Unknown option(s) in [tool.hatch.metadata.hooks.autoextras]: ['group-name']. "
        "Valid options: ['exclude', 'extra-name', 'overwrite']"
    ) in output(old_option_name)


def test_autoextras_integration_exclude_unmatched_fails(
    unmatched_exclude: subprocess.CompletedProcess[str],
) -> None:
    r"""An ``exclude`` entry that matches no extra fails the build."""
    assert unmatched_exclude.returncode != 0


def test_autoextras_integration_exclude_unmatched_message(
    unmatched_exclude: subprocess.CompletedProcess[str],
) -> None:
    r"""The error names the unmatched entry."""
    assert (
        "'exclude' in [tool.hatch.metadata.hooks.autoextras] contains names that match no extra: ['tset']"
        in output(unmatched_exclude)
    )


def test_autoextras_integration_blank_dependency_fails(
    blank_dependency: subprocess.CompletedProcess[str],
) -> None:
    r"""A blank dependency fails the build."""
    assert blank_dependency.returncode != 0


def test_autoextras_integration_blank_dependency_message(
    blank_dependency: subprocess.CompletedProcess[str],
) -> None:
    r"""The error names the source extra and the position."""
    assert "Dependency #2 of extra 'docs' must not be blank" in output(blank_dependency)


def test_autoextras_integration_dynamic_and_static_table_fails(
    dynamic_and_static: subprocess.CompletedProcess[str],
) -> None:
    r"""``dynamic = ["optional-dependencies"]`` cannot be combined with a
    static table: hatchling refuses the project."""
    assert dynamic_and_static.returncode != 0


def test_autoextras_integration_dynamic_and_static_table_message(
    dynamic_and_static: subprocess.CompletedProcess[str],
) -> None:
    assert "cannot be both statically defined and listed in field" in output(dynamic_and_static)


#######################################
#     Warn-only mode                  #
#######################################


class Build(NamedTuple):
    r"""A build in warn-only mode: its result and its project path."""

    result: subprocess.CompletedProcess[str]
    path: Path


def build_warn_only(tmp_path_factory: pytest.TempPathFactory, name: str, config: str) -> Build:
    r"""Build a project with the warn-only variable.

    Args:
        tmp_path_factory: The factory of temporary directories.
        name: The name of the directory of the project.
        config: Lines for the ``autoextras`` hook table.

    Returns:
        The completed process and the path of the project.
    """
    path = tmp_path_factory.mktemp(name) / "project"
    return Build(build_project(path, config=config, env={WARN_ONLY_ENV: "1"}), path)


@pytest.fixture(scope="module")
def warn_unknown_option(tmp_path_factory: pytest.TempPathFactory) -> Build:
    return build_warn_only(tmp_path_factory, "warn-unknown", 'excludes = ["dev"]')


@pytest.fixture(scope="module")
def warn_unmatched_exclude(tmp_path_factory: pytest.TempPathFactory) -> Build:
    return build_warn_only(tmp_path_factory, "warn-unmatched", 'exclude = ["dev", "tset"]')


def test_autoextras_integration_unknown_option_warn_only_succeeds(
    warn_unknown_option: Build,
) -> None:
    r"""With the warn-only variable, the build succeeds."""
    assert warn_unknown_option.result.returncode == 0


def test_autoextras_integration_unknown_option_warn_only_message(
    warn_unknown_option: Build,
) -> None:
    r"""With the warn-only variable, the unknown option is named in a
    warning."""
    assert "Unknown option(s) in [tool.hatch.metadata.hooks.autoextras]: ['excludes']" in output(
        warn_unknown_option.result
    )


def test_autoextras_integration_unknown_option_warn_only_metadata(
    warn_unknown_option: Build,
) -> None:
    r"""The extras built in warn-only mode are the ones of a build
    without the unknown option."""
    assert read_extras(find_wheel_path(warn_unknown_option.path)) == DEFAULT_EXTRAS


def test_autoextras_integration_exclude_unmatched_warn_only_succeeds(
    warn_unmatched_exclude: Build,
) -> None:
    r"""With the warn-only variable, the build succeeds."""
    assert warn_unmatched_exclude.result.returncode == 0


def test_autoextras_integration_exclude_unmatched_warn_only_message(
    warn_unmatched_exclude: Build,
) -> None:
    r"""With the warn-only variable, the unmatched entry is named in a
    warning."""
    assert "match no extra: ['tset']" in output(warn_unmatched_exclude.result)


def test_autoextras_integration_exclude_unmatched_warn_only_metadata(
    warn_unmatched_exclude: Build,
) -> None:
    r"""The extras built in warn-only mode are the ones of a build
    without the unmatched entry."""
    assert read_extras(find_wheel_path(warn_unmatched_exclude.path)) == {
        "all": ["numpy>=2.0"],
        "dev": ["pytest>=9.0"],
        "numpy": ["numpy>=2.0"],
    }
