"""
Configuration and tasks for **Nox**.
"""

import glob
import logging
import os
import tarfile
import textwrap
import zipfile
from datetime import datetime, timezone
from pathlib import Path


try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore[no-redef]

import nox
import rich
import rich.console
import rich.markdown
import rich.tree
from packaging.requirements import Requirement


PROJECT_DIR = Path(__file__).parent
MYPY_PATHS = [
    [
        "./conftest.py",
        "./noxfile.py",
        "src/",
        "tests/",
    ],
    [
        "docs/conf.py",
        "docs/conftest.py",
    ],
    [
        "docs/examples/",
    ],
]
LINT_PATHS = [p for paths in MYPY_PATHS for p in paths]

# Dependencies for which to test against multiple versions
PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12", "3.13", "3.14"]
COVERAGE_PYTHON_VERSIONS = ["3.9", "3.13"]

DEPS_MATRIX = {
    "attrs",
    "cattrs",
}

IN_CI = "CI" in os.environ
OMMIT_IN_REPORT = [
    "src/typed_settings/argparse_utils.py",
    "src/typed_settings/attrs.py",
    "src/typed_settings/click_utils.py",
    "src/typed_settings/mypy.py",
]
if IN_CI:
    OMMIT_IN_REPORT += [
        "src/typed_settings/_onepassword.py",
        "tests/test_onepassword.py",
    ]


def list_wheel(filename: Path) -> list[tuple[bool, Path, int, datetime]]:
    """
    List contents of a Wheel package.

    Return a list of tuples *(is_dir, filename, size_in_bytes, mtime)*.
    """
    with zipfile.ZipFile(filename) as zf:
        items = [
            (
                item.is_dir(),
                Path(item.filename),
                item.file_size,
                datetime(*item.date_time, tzinfo=timezone.utc),
            )
            for item in zf.infolist()
        ]
    return items


def list_sdist(filename: Path) -> tuple[list[tuple[bool, Path, int, datetime]], str]:
    """
    List contents of a source distribution.

    Return a list of tuples *(is_dir, filename, size_in_bytes, mtime)* and the
    package metadata.
    """
    with tarfile.open(filename) as tf:
        items = [
            (
                item.isdir(),
                Path(item.name),
                item.size,
                datetime.fromtimestamp(item.mtime, tz=timezone.utc),
            )
            for item in tf.getmembers()
        ]
        fname = f"{filename.stem.removesuffix('.tar')}/PKG-INFO"
        metadata = tf.extractfile(fname).read().decode()  # type: ignore[union-attr]
        return items, metadata


def get_filetree(
    filename: Path, infos: list[tuple[bool, Path, int, datetime]]
) -> rich.tree.Tree:
    """
    Return a rich "Tree" for the contents of a Wheel or sdist.
    """
    tree = rich.tree.Tree(f":package: [bold magenta]{filename.name}[/]")
    nodes: dict[Path, rich.tree.Tree] = {}
    maxlen: dict[Path, int] = {}
    for _is_dir, path, _size, _time in infos:
        maxlen[path.parent] = max(len(path.name), maxlen.get(path.parent, 0))

    for is_dir, path, size, time in infos:
        components = [path, *path.parents][:-1]
        idx = 0 if is_dir else 1
        files = components[:idx]
        parents = components[idx:]
        for parent in reversed(parents):
            if parent not in nodes:
                label = f":open_file_folder: [bold blue]{parent.name}[/]"
                nodes[parent] = nodes.get(parent.parent, tree).add(label)
        parent_node = nodes[parent]
        width = maxlen[parent]
        for file in files:
            label = (
                f":page_facing_up: [bold]{file.name:<{width}}[/] "
                f"[green]{time:%Y-%m-%d}[/]T[green]{time:%H-%M-%S}[/]Z "
                f"[blue]{size}[cyan]B[/]"
            )
            parent_node.add(label)

    return tree


def uv_sync(session: nox.Session, group: str = "", all: bool = True) -> None:
    """
    Run "uv sync" and install dev dependency *group*.
    """
    extras = ("--all-extras",) if all else ()
    dev_groups = ("--no-dev", "--group", group) if group else ()
    session.run_install(
        "uv",
        "sync",
        *extras,
        *dev_groups,
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )


@nox.session
def build(session: nox.Session) -> None:
    """
    Build an sdist and a wheel for TS.
    """
    # Set 'SOURCE_DATE_EPOCH' based on the last commit for build reproducibility.
    source_date_epoch = session.run(  # type: ignore[union-attr]
        "git", "log", "-1", "--pretty=%ct", external=True, silent=True
    ).strip()
    env = {"SOURCE_DATE_EPOCH": source_date_epoch}
    session.log(f"Setting SOURCE_DATE_EPOCH to {source_date_epoch}.")

    session.run("rm", "-rf", "dist", external=True)
    session.run("uv", "build", "--out-dir=dist", env=env, external=True)
    session.run("uvx", "check-wheel-contents", "dist", external=True)
    session.run("uvx", "twine", "check", "--strict", "dist/*", external=True)

    console = rich.console.Console(stderr=True)

    session.log("Distribution contents:")
    for dist in Path("dist").glob("typed_settings-*"):
        if dist.suffix == ".whl":
            items = list_wheel(dist)
        else:
            items, metadata = list_sdist(dist)
        console.print(get_filetree(dist, items))
    assert metadata, "No sdist has been built"

    session.log("Metadata:")
    metadata, _, readme = metadata.partition("\n\n")
    logging.getLogger("markdown_it").setLevel("WARNING")
    console.print(textwrap.indent(metadata, "    "))
    console.print()
    console.print(rich.markdown.Markdown(readme))


@nox.session(python=PYTHON_VERSIONS, tags=["test"])
@nox.parametrize(
    "deps_min_version",
    [True, False],
    ["min_deps_version", "latest_deps_version"],
)
def test(session: nox.Session, deps_min_version: bool) -> None:
    """
    Run all tests for various configurations (Python and dependency versions).

    Run the full matrix (all combinations of latest/min dependencies and packakge
    formats) only for the latest stable Python version to save some CI/CD minutes.
    """
    pkgs = glob.glob("dist/*.whl")
    if len(pkgs) == 0:
        session.log('Package not found, running "build" ...')
        build(session)
        pkgs = glob.glob("dist/*.whl")
    if len(pkgs) != 1:
        session.error(f"Expected exactly 1 file: {', '.join(pkgs)}")
    pkg_file = pkgs[0]

    # If testing against the minium versions of our dependencies,
    # extract their minium version from pyproject.toml and pin
    # these versions.
    install_deps = []
    if deps_min_version:
        pyproject = tomllib.loads(PROJECT_DIR.joinpath("pyproject.toml").read_text())
        deps = pyproject["project"]["dependencies"]
        for dep in deps:
            req = Requirement(dep)
            if req.name not in DEPS_MATRIX:
                continue
            spec = str(req.specifier)
            assert spec.startswith(">="), spec
            spec = spec.replace(">=", "==")
            install_deps.append(f"{req.name}{spec}")

    uv_sync(session, group="test")
    # Explicitly install the built wheel and dependencies:
    session.install(f"typed-settings @ file:{pkg_file}", *install_deps)

    env: dict[str, str] = {}
    test_args: tuple[str, ...] = ()
    test_prefix: tuple[str, ...] = ()

    version_tuple = tuple(map(int, session.python.split(".")))  # type: ignore
    if version_tuple >= (3, 12):
        # Still experimental but has much better performance:
        env = {"COVERAGE_CORE": "sysmon"}

    if version_tuple < (3, 10):
        # Skip doctests on older Python versions
        # The output of arparse's "--help" has changed in 3.10
        test_args = ("tests", "-k", "not test_readme")

    if session.python in COVERAGE_PYTHON_VERSIONS:
        # Only measure coverage for the minimum and maximum supported Python versions
        # for performance reasons:
        test_prefix = ("coverage", "run", "-m")

    session.run(*test_prefix, "pytest", *test_args, env=env)


@nox.session(tags=["test"])
def test_no_optionals(session: nox.Session) -> None:
    """
    Run tests with no optional dependencies installed.
    """
    pkgs = glob.glob("dist/*.whl")
    # Install as little as possible:
    session.install(f"typed-settings @ {pkgs[0]}", "coverage", "pytest", "sybil")
    session.run(
        "coverage",
        "run",
        "-m",
        "pytest",
        "tests/test_no_optionals.py",
        env={"COVERAGE_CORE": "sysmon"},
    )


@nox.session(name="coverage-report", tags=["test"])
def coverage_report(session: nox.Session) -> None:
    """
    Create a coverate report from the results of the test sessions.
    """
    uv_sync(session, group="test")

    args = []
    if OMMIT_IN_REPORT:
        args.append(f"--omit={','.join(OMMIT_IN_REPORT)}")

    session.run("coverage", "combine")
    # Only let the "report" command fail under 100%
    session.run("coverage", "xml", "--fail-under=0")
    session.run("coverage", "html", "--fail-under=0")
    session.run("coverage", "report", *args)


@nox.session(python=False, tags=["lint"])
def fix(session: nox.Session) -> None:
    """
    Run code fixers.
    """
    session.run("ruff", "check", "--fix-only", *LINT_PATHS)
    session.run("ruff", "format", *LINT_PATHS)


@nox.session(tags=["lint"])
def lint(session: nox.Session) -> None:
    """
    Run the linters.
    """
    uv_sync(session, group="lint")
    session.run("ruff", "check", *LINT_PATHS)


@nox.session(tags=["lint"])
def mypy(session: nox.Session) -> None:
    """
    Run type checking with MyPy.
    """
    uv_sync(session, group="lint")
    for paths in MYPY_PATHS:
        session.run("mypy", "--show-error-codes", *paths)


@nox.session(name="sec-check", tags=["lint"])
def sec_check(session: nox.Session) -> None:
    """
    Run a security check with pip-audit.
    """
    uv_sync(session)
    session.run("pip-audit")


@nox.session(python=False, tags=["lint"])
def docs(session: nox.Session) -> None:
    """
    Build the docs.

    Make a clean build if "clean" is in the session's positional args.

    Open the built documentation in the default webbrowser if "open" is in the session's
    positional args.
    """
    targets = ("clean", "html") if "clean" in session.posargs else ("html",)
    session.run("make", "-C", "docs", *targets)
    if "open" in session.posargs:
        import webbrowser

        index = Path.cwd().joinpath("docs", "_build", "html", "index.html")
        webbrowser.open(f"file://{index}")
