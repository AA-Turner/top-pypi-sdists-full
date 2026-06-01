"""Main CLI for emake."""

import argparse
import os
import shutil
import subprocess
import sys
from importlib import resources

from . import __version__
from .build import (
    build_sdist,
    clean,
)
from .config import (
    ProjectConfig,
    diff,
)
from .executable import build_executable
from .lint import run_lint
from .venv import get_venv
from .wheel import (
    build_manylinux_wheel,
    check_docker,
    test_manylinux_wheel,
)


def validate_extras(config: ProjectConfig, extras: list[str]) -> list[str]:
    """Validate that extras are defined in pyproject.toml.

    Args:
        config: ProjectConfig instance.
        extras: List of extra names provided by user.

    Returns:
        List of validated extra names.

    Raises:
        ValueError: If an extra is not defined in pyproject.toml.
    """
    config_extras = config.extras if config.extras is not None else {}
    available = set(config_extras.keys())
    for extra in extras:
        if extra not in available:
            raise ValueError(
                f"Unknown extra '{extra}'. Available: {', '.join(sorted(available))}"
            )
    return extras


def get_arg(value: str | None, prompt: str) -> str | None:
    """Get value from flag or prompt if interactive terminal."""
    if value:
        return value
    if sys.stdin.isatty():
        return input(prompt)
    return None


def cmd_init(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    """Handle the init command."""
    name = get_arg(args.name, "Project name: ")  # pyright: ignore[reportAny]
    description = get_arg(args.description, "Description: ")  # pyright: ignore[reportAny]
    author_name = get_arg(args.author_name, "Author name: ")  # pyright: ignore[reportAny]
    author_email = get_arg(args.author_email, "Author email: ")  # pyright: ignore[reportAny]
    license_spdx = get_arg(args.author_email, "License spdx identifier: ")  # pyright: ignore[reportAny]

    if (
        name is None
        or description is None
        or author_name is None
        or author_email is None
        or license_spdx is None
    ):
        parser.print_usage()
        return 1

    if not os.path.exists("pyproject.toml"):
        template = resources.files("emake").joinpath("pyproject.toml.tpl").read_text()
        with open("pyproject.toml", "w") as f:
            _ = f.write(
                template.format(
                    name=name,
                    description=description,
                    author_name=author_name,
                    author_email=author_email,
                    license_spdx=license_spdx,
                    python_version=">=3.11",
                )
            )

    os.makedirs(name, exist_ok=True)
    file = os.path.join(name, "__init__.py")
    if not os.path.exists(file):
        with open(file, "w") as f:
            _ = f.write("")

    workflow_dir = os.path.join(".github", "workflows")
    os.makedirs(workflow_dir, exist_ok=True)
    file = os.path.join(workflow_dir, "build.yml")
    if not os.path.exists(file):
        template = resources.files("emake").joinpath("build.yml.tpl").read_text()
        with open(file, "w") as f:
            _ = f.write(template.format(project_name=name))

    return 0


def cmd_requirements(args: argparse.Namespace, _parser: argparse.ArgumentParser) -> int:
    """Handle the requirements command."""
    config = ProjectConfig()
    extras = validate_extras(config, args.extras) if args.extras else []  # pyright: ignore[reportAny]
    venv = get_venv()
    venv.install(*extras)
    return 0


def cmd_test(args: argparse.Namespace, _parser: argparse.ArgumentParser) -> int:
    """Handle the test command."""
    config = ProjectConfig()
    if config.name is None:
        print("Error: Project name missing", file=sys.stderr)
        return 1

    test = config.emake.get("test", None)
    if args.wheel:  # pyright: ignore[reportAny]
        test_manylinux_wheel(
            arch=args.arch,  # pyright: ignore[reportAny]
            libc=args.libc,  # pyright: ignore[reportAny]
            python=args.python or config.minimum_python_version,  # pyright: ignore[reportAny]
            setup=args.setup,  # pyright: ignore[reportAny]
            teardown=args.teardown,  # pyright: ignore[reportAny]
            test=test,
        )
        return 0

    venv = get_venv()
    venv.ensure_test_tools()
    if test is None:
        return venv.run("-um", "pytest", "-vv", "tests").returncode

    test_cmd = "\n".join(test)
    activate = os.path.relpath(venv.activate).replace("\\", "/")
    return subprocess.run(
        [
            shutil.which("bash") or "bash",
            *([] if "RUNNER_DEBUG" not in os.environ else ["-x"]),
            "-ec",
            f'source "{activate}"\n{test_cmd}',
        ],
        check=False,
        env={**os.environ, "EMAKE": "1"},
    ).returncode


def cmd_build(args: argparse.Namespace, _parser: argparse.ArgumentParser) -> int:
    """Handle the build command."""
    venv = get_venv()
    venv.ensure_build_tools()
    config = ProjectConfig()
    if config.name is None:
        print("Error: Project name missing", file=sys.stderr)
        return 1

    if args.sdist:  # pyright: ignore[reportAny]
        build_sdist(venv)

    if args.wheel:  # pyright: ignore[reportAny]
        build_manylinux_wheel(
            False,
            arch=args.arch,  # pyright: ignore[reportAny]
            libc=args.libc,  # pyright: ignore[reportAny]
            python=args.python or config.minimum_python_version,  # pyright: ignore[reportAny]
            setup=args.setup,  # pyright: ignore[reportAny]
            teardown=args.teardown,  # pyright: ignore[reportAny]
        )

    if args.native_wheel:  # pyright: ignore[reportAny]
        build_manylinux_wheel(
            True,
            arch=args.arch,  # pyright: ignore[reportAny]
            libc=args.libc,  # pyright: ignore[reportAny]
            python=args.python or config.minimum_python_version,  # pyright: ignore[reportAny]
            setup=args.setup,  # pyright: ignore[reportAny]
            teardown=args.teardown,  # pyright: ignore[reportAny]
        )

    if args.executable:  # pyright: ignore[reportAny]
        build_executable(
            config.name,
            arch=args.arch,  # pyright: ignore[reportAny]
            libc=args.libc,  # pyright: ignore[reportAny]
            python=args.python or config.minimum_python_version,  # pyright: ignore[reportAny]
            setup=args.setup,  # pyright: ignore[reportAny]
            teardown=args.teardown,  # pyright: ignore[reportAny]
            no_compress=args.no_compress,  # pyright: ignore[reportAny]
            lto=not args.no_lto,  # pyright: ignore[reportAny]
        )

    return 0


def cmd_clean(_args: argparse.Namespace, _parser: argparse.ArgumentParser) -> int:
    """Handle the clean command."""
    clean()
    return 0


def cmd_lint(args: argparse.Namespace, _parser: argparse.ArgumentParser) -> int:
    """Handle the lint command."""
    assert isinstance(args.fix, bool)  # pyright: ignore[reportAny]
    assert isinstance(args.workflow, bool)  # pyright: ignore[reportAny]
    assert isinstance(args.colour, bool)  # pyright: ignore[reportAny]
    return run_lint(get_venv(), ProjectConfig(), args.fix, args.workflow, args.colour)


def cmd_config_diff(args: argparse.Namespace, _parser: argparse.ArgumentParser) -> int:
    """Handle the config-diff command."""
    assert isinstance(args.workflow, bool)  # pyright: ignore[reportAny]
    assert isinstance(args.colour, bool)  # pyright: ignore[reportAny]
    return diff(args.workflow, args.colour)


def cmd_status(_args: argparse.Namespace, _parser: argparse.ArgumentParser) -> int:
    """Handle the status command."""
    config = ProjectConfig()
    venv = get_venv()
    print(f"Project: {config.name}-{config.version}")
    print(f"Docker: {'installed' if check_docker() else 'missing'}")
    print(f"Venv: {'installed' if venv.exists else 'missing'}")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Main entry point for emake."""
    parser = argparse.ArgumentParser(
        prog="emake",
        description="A Python module to replace Makefile workflows.",
    )
    _ = parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    _ = parser.add_argument(
        "--directory",
        "-C",
        help="Change to DIRECTORY before doing anything",
        metavar="DIRECTORY",
        default=".",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparser = subparsers.add_parser(
        "requirements",
        help="Create .venv and install dependencies",
    )
    _ = subparser.add_argument(
        "extras",
        nargs="*",
        help="Optional dependency groups to install (e.g., web test dev)",
    )

    subparser = subparsers.add_parser(
        "test",
        help="Run tests (default: all tests in tests/)",
    )
    _ = subparser.add_argument(
        "--wheel",
        action="store_true",
        help="Test using Docker with a built wheel instead of local code",
    )
    _ = subparser.add_argument(
        "--arch",
        default="x86_64",
        help="Target architecture for wheel testing (default: x86_64)",
    )
    _ = subparser.add_argument(
        "--libc",
        default="glibc",
        choices=["glibc", "musl"],
        help="Target libc for wheel testing (default: glibc)",
    )
    _ = subparser.add_argument(
        "--python",
        default=None,
        help="Python version for wheel testing. Defaults to lowest supported version.",
    )
    _ = subparser.add_argument(
        "--setup",
        default=None,
        help="Script to run before installing the wheel and running the tests. Only relevant when --wheel is specified",
    )
    _ = subparser.add_argument(
        "--teardown",
        default=None,
        help="Script to run after installing the wheel and running the tests. Only relevant when --wheel is specified",
    )
    _ = subparser.add_argument(
        "path",
        nargs="?",
        default="tests/",
        help="Path to test file or directory (default: tests/)",
    )

    subparser = subparsers.add_parser(
        "build",
        help="Build wheel and source distribution",
    )
    _ = subparser.add_argument(
        "--sdist",
        action="store_true",
        help="Build source distribution",
    )
    _ = subparser.add_argument(
        "--wheel",
        action="store_true",
        help="Build a pure python wheel",
    )
    _ = subparser.add_argument(
        "--native-wheel",
        action="store_true",
        help="Build platform-specific wheel.",
        dest="native_wheel",
    )
    _ = subparser.add_argument(
        "--executable",
        action="store_true",
        help="Build standalone executable, this assumes module.__main__ exists",
    )
    _ = subparser.add_argument(
        "--no-compress",
        action="store_true",
        help="Do not compress the standalone executable. This reduces memory requirements and build time.",
        dest="no_compress",
    )
    _ = subparser.add_argument(
        "--no-lto",
        action="store_true",
        help="Do not build executable with lto.",
        dest="no_lto",
    )
    _ = subparser.add_argument(
        "--arch",
        default="x86_64",
        help="Target architecture for manylinux build (default: x86_64)",
    )
    _ = subparser.add_argument(
        "--libc",
        default="glibc",
        choices=["glibc", "musl"],
        help="Target libc for manylinux build (default: glibc)",
    )
    _ = subparser.add_argument(
        "--python",
        default=None,
        help="Python version for manylinux build. Defaults to lowest supported version.",
    )
    _ = subparser.add_argument(
        "--setup",
        default=None,
        help="Script to run before starting the build.",
    )
    _ = subparser.add_argument(
        "--teardown",
        default=None,
        help="Script to run after the build completes.",
    )

    _ = subparsers.add_parser(
        "clean",
        help="Remove build artifacts",
    )

    subparser = subparsers.add_parser(
        "lint",
        help="Run linting",
    )
    _ = subparser.add_argument(
        "--fix",
        action="store_true",
        help="Automatically fix issues where supported",
    )
    _ = subparser.add_argument(
        "--workflow",
        help="Do a comparison of the workflow and outut the diff",
        action="store_true",
    )
    _ = subparser.add_argument(
        "--colour",
        "--color",
        help="Force colour output even when not on a tty",
        action="store_true",
    )

    _ = subparsers.add_parser(
        "status",
        help="Output status information",
    )

    subparser = subparsers.add_parser(
        "config-diff",
        help="Compare project's pyproject.toml against template",
    )
    _ = subparser.add_argument(
        "--workflow",
        help="Do a comparison of the workflow and outut the diff",
        action="store_true",
    )
    _ = subparser.add_argument(
        "--colour",
        "--color",
        help="Force colour output even when not on a tty",
        action="store_true",
    )

    subparser = subparsers.add_parser(
        "init",
        help="Initialize a new project",
    )
    _ = subparser.add_argument("--name", help="Project name")
    _ = subparser.add_argument("--description", help="Project description")
    _ = subparser.add_argument("--author-name", help="Author name")
    _ = subparser.add_argument("--author-email", help="Author email")

    args = parser.parse_args(argv)

    os.chdir(os.path.abspath(args.directory))  # pyright: ignore[reportAny]
    return {
        "requirements": cmd_requirements,
        "test": cmd_test,
        "build": cmd_build,
        "clean": cmd_clean,
        "lint": cmd_lint,
        "status": cmd_status,
        "init": cmd_init,
        "config-diff": cmd_config_diff,
    }[args.command](args, parser)  # pyright: ignore[reportAny]


if __name__ == "__main__":
    sys.exit(main())
