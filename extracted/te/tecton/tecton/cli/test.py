import glob
import os
import sys
import warnings
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple

import click
import pytest

from tecton.cli import printer
from tecton.cli.command import TectonCommand
from tecton.cli.command import TectonCommandCategory
from tecton.repo_utils import get_tecton_objects_skip_validation
from tecton_core import conf
from tecton_core import repo_file_handler


ALLOWED_COMPUTE_MODES = ["rift", "spark"]


def get_test_paths(repo_root) -> List[str]:
    # Be _very_ careful updating this:
    #    `glob.glob` does bash-style globbing (ignores hidden files)
    #    `pathlib.Path.glob` does _not_ do bash-style glob (it shows hidden)
    #
    # Ignoring hidden files is a very important expectation for our usage of
    # pytest. Otherwise, we may test files that user does not intend us to
    # (like in their .git or .tox directories).
    #
    # NOTE: This won't filter out hidden files for Windows. Potentially:
    #    `bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)`
    # would filter hidden files for Windows, but this would need some testing.
    candidate_test_files = glob.iglob(f"{repo_root}/**/tests/**/*.py", recursive=True)

    VIRTUAL_ENV = os.getenv("VIRTUAL_ENV")
    if VIRTUAL_ENV:
        candidate_test_files = filter(lambda f: not f.startswith(VIRTUAL_ENV), candidate_test_files)

    # Filter out test files that match patterns in .tectonignore
    from pathlib import Path

    repo_root_path = Path(repo_root)
    ignored_files = repo_file_handler._get_ignored_files(repo_root_path)
    ignored_files_str = {str(f) for f in ignored_files}

    filtered_test_files = [f for f in candidate_test_files if f not in ignored_files_str]

    return filtered_test_files


def run_tests(
    repo_config_path: Optional[Path], pytest_extra_args: Tuple[str, ...] = (), suppress_warnings: bool = False
):
    repo_root = repo_file_handler._maybe_get_repo_root()
    if repo_root is None:
        printer.safe_print("Tecton tests must be run from a feature repo initialized using 'tecton init'!")
        sys.exit(1)

    get_tecton_objects_skip_validation(repo_config_path)

    tests = get_test_paths(repo_root)
    if len(tests) == 0:
        printer.safe_print("⚠️  Running Tests: No tests found.")
        return

    os.chdir(repo_root)
    args = ["-s", *tests]

    # Suppress Python warnings globally during test execution and add pytest warning suppression args
    if suppress_warnings:
        warnings.filterwarnings("ignore")
        args.extend(["--disable-pytest-warnings", "-W", "ignore"])

    if pytest_extra_args:
        args.extend(pytest_extra_args)

    printer.safe_print("🏃 Running Tests")
    exitcode = pytest.main(args)

    if exitcode == 5:
        # https://docs.pytest.org/en/stable/usage.html#possible-exit-codes
        printer.safe_print("⚠️  Running Tests: No tests found.")
        return None
    elif exitcode != 0:
        printer.safe_print("⛔ Running Tests: Tests failed :(")
        sys.exit(1)
    else:
        printer.safe_print("✅ Running Tests: Tests passed!")


@click.command(
    uses_workspace=True, requires_auth=False, cls=TectonCommand, command_category=TectonCommandCategory.WORKSPACE
)
@click.option(
    "--enable-python-serialization/--disable-python-serialization",
    show_default=True,
    is_flag=True,
    default=True,
    help="""
    If disabled, Tecton will not serialize python code during unit tests. This can be useful in some test environments
    or when running code coverage tools, however the tests may be less realistic since serialization issues will not be
    covered. This option is not supported when running tests during `tecton apply`. If using pytest directly, set
    TECTON_FORCE_FUNCTION_SERIALIZATION=false in your environment to achieve the same behavior.
    """,
)
@click.option(
    "--config",
    help="Path to the repo config yaml file. Defaults to the repo.yaml file at the Tecton repo root.",
    default=None,
    type=click.Path(exists=True, dir_okay=False, path_type=Path, readable=True),
)
@click.option(
    "--default-compute-mode",
    help="What compute mode to use to test features if not specified. Should be one of spark or rift.",
    default="spark",
    type=click.Choice(choices=ALLOWED_COMPUTE_MODES, case_sensitive=False),
)
@click.option(
    "--suppress-warnings",
    is_flag=True,
    default=False,
    help="Suppress Python and pytest warnings during test execution. Can also be controlled with TECTON_SUPPRESS_TEST_WARNINGS=1 environment variable.",
)
@click.argument("pytest_extra_args", nargs=-1)
def test(
    enable_python_serialization,
    config: Optional[Path],
    default_compute_mode: str,
    suppress_warnings: bool,
    pytest_extra_args: Tuple[str, ...],
):
    """Run unit tests.

    USAGE:
    `tecton test`: run all tests (using PyTest) in a file that matches glob("TECTON_REPO_ROOT/**/tests/**/*.py")
    `tecton test -- -k "test_name"`: same as above, but passes the `-k "test_name"` args to the PyTest command.
    """
    if conf.get_or_none("TECTON_FORCE_FUNCTION_SERIALIZATION"):
        msg = "Do not set TECTON_FORCE_FUNCTION_SERIALIZATION when using `tecton test`. Use --enable-python-serialization/--disable-python-serialization instead."
        raise RuntimeError(msg)

    if enable_python_serialization:
        conf.set("TECTON_FORCE_FUNCTION_SERIALIZATION", "true")
    else:
        conf.set("TECTON_FORCE_FUNCTION_SERIALIZATION", "false")

    env_suppress_warnings = conf.get_bool("TECTON_SUPPRESS_TEST_WARNINGS")
    should_suppress_warnings = suppress_warnings or env_suppress_warnings

    default_compute_mode = default_compute_mode.lower()
    offline_retrieval_compute_mode = (
        conf._get_runtime_only("TECTON_OFFLINE_RETRIEVAL_COMPUTE_MODE") or default_compute_mode
    )
    batch_compute_mode = conf._get_runtime_only("TECTON_BATCH_COMPUTE_MODE") or default_compute_mode

    # Set TECTON_SKIP_OBJECT_VALIDATION to True by default for tests, but respect user's manual setting
    if conf.is_runtime_set("TECTON_SKIP_OBJECT_VALIDATION"):
        skip_validation = conf._get_runtime_only("TECTON_SKIP_OBJECT_VALIDATION")
    else:
        skip_validation = "True"

    # These values are set explicitly in unit tests in order to avoid needing to be logged into a cluster
    # to run unit tests. Without this, the compute_mode is derived from the user's cluster, which requires log-in.
    with conf._temporary_set(
        "TECTON_OFFLINE_RETRIEVAL_COMPUTE_MODE", offline_retrieval_compute_mode
    ) as a, conf._temporary_set("TECTON_BATCH_COMPUTE_MODE", batch_compute_mode) as b, conf._temporary_set(
        "TECTON_SKIP_OBJECT_VALIDATION", skip_validation
    ) as c:
        # NOTE: if a user wanted to do the equivalent of a `pytest -k "test_name"`
        # they could do `tecton test -- -k "test_name"`.
        run_tests(
            repo_config_path=config,
            pytest_extra_args=pytest_extra_args,
            suppress_warnings=should_suppress_warnings,
        )
