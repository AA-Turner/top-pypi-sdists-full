import importlib
import os
import sys
from pathlib import Path
from types import ModuleType
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple

from rich.live import Live
from rich.spinner import Spinner

from tecton.cli import cli_utils
from tecton.cli import printer
from tecton.cli import repo_config as cli__repo_config
from tecton.cli.error_utils import pretty_error
from tecton.cli.printer import SPINNER_TYPE
from tecton.framework import base_tecton_object
from tecton.framework import repo_config as framework__repo_config
from tecton_core import conf
from tecton_core import repo_file_handler
from tecton_core.errors import TectonAPIInaccessibleError
from tecton_core.errors import TectonValidationError


def _import_module_with_pretty_errors(
    file_path: Path,
    module_path: str,
    py_files: List[Path],
    repo_root: Path,
    before_error: Callable[[], None],
) -> ModuleType:
    from pyspark.sql.utils import AnalysisException

    try:
        module = importlib.import_module(module_path)
        if Path(module.__file__) != file_path:
            before_error()
            relpath = file_path.relative_to(repo_root)
            printer.safe_print(
                f"Python module name [bold]{module_path}[/bold] ({relpath}) conflicts with module [bold]{module_path}[/bold] from {module.__file__}. Please use a different name.",
                file=sys.stderr,
            )
            sys.exit(1)

        return module
    except AnalysisException as e:
        before_error()
        pretty_error(
            Path(file_path),
            py_files,
            exception=e,
            repo_root=repo_root,
            error_message="Analysis error",
            error_details=e.desc,
        )
        sys.exit(1)
    except TectonValidationError as e:
        before_error()
        pretty_error(Path(file_path), py_files, exception=e, repo_root=repo_root, error_message=e.args[0])
        sys.exit(1)
    except SyntaxError as e:
        before_error()
        details = None
        if e.text and e.offset:
            details = e.text + (" " * e.offset) + "^^^"
        pretty_error(
            Path(file_path),
            py_files,
            exception=e,
            repo_root=repo_root,
            error_message=e.args[0],
            error_details=details,
        )
        sys.exit(1)
    except TectonAPIInaccessibleError as e:
        before_error()
        printer.safe_print("Failed to connect to Tecton server at", e.args[1], ":", e.args[0])
        sys.exit(1)
    except Exception as e:
        # NOTE: This is only kept for 1.0 to ease the 0.9 -> 1.0 migration.
        _handle_common_v09_compat_errors(
            error=e, file_path=file_path, py_files=py_files, repo_root=repo_root, before_error=before_error
        )

        before_error()
        pretty_error(Path(file_path), py_files, exception=e, repo_root=repo_root, error_message=e.args[0])
        sys.exit(1)


def _handle_common_v09_compat_errors(
    error, file_path: Path, py_files: List[Path], repo_root: Path, before_error: Callable[[], None]
):
    default_upgrade_guidance = (
        "\nDid you replace `from tecton` with `from tecton.v09_compat`? See "
        "https://docs.tecton.ai/docs/release-notes/upgrade-process/to-1_0-upgrade-guide for details on the upgrade "
        "guide."
    )
    error_message = error.args[0]

    # common error for Entity
    is_entity_error = (
        isinstance(error, TypeError)
        and 'type of argument "join_keys" must be one of (List[tecton.types.Field], NoneType); got list instead'
        in error_message
    )

    # common push source error
    is_push_source_import_error = (
        isinstance(error, ImportError) and "cannot import name 'PushSource' from 'tecton'" in error_message
    )

    # common filtered source error
    is_filtered_source_import_error = (
        isinstance(error, ImportError) and "cannot import name 'FilteredSource' from 'tecton'" in error_message
    )

    if is_entity_error or is_push_source_import_error or is_filtered_source_import_error:
        before_error()
        pretty_error(
            Path(file_path),
            py_files,
            exception=error,
            repo_root=repo_root,
            error_message=f"{error_message} {default_upgrade_guidance}",
        )
        sys.exit(1)


def collect_top_level_objects(
    py_files: List[Path], repo_root: Path, pretty_errors: bool
) -> List[base_tecton_object.BaseTectonObject]:
    modules = [cli_utils.py_path_to_module(p, repo_root) for p in py_files]

    spinner = Spinner(SPINNER_TYPE, "Importing feature repository modules")
    with Live(spinner, console=printer.get_console(), refresh_per_second=100) as live:
        for file_path, module_path in zip(py_files, modules):
            if pretty_errors:
                module = _import_module_with_pretty_errors(
                    file_path=file_path,
                    module_path=module_path,
                    py_files=py_files,
                    repo_root=repo_root,
                    before_error=lambda: live.update(
                        Spinner(
                            SPINNER_TYPE,
                            text="⛔ Failed to import feature repository. Please check the error message above for details.",
                        )
                    ),
                )
            else:
                module = importlib.import_module(module_path)
        num_modules = len(modules)
        live.update(
            Spinner(
                SPINNER_TYPE,
                text=f"✅ Imported {num_modules} Python {cli_utils.plural(num_modules, 'module', 'modules')} from the feature repository",
            )
        )
    return list(base_tecton_object._LOCAL_TECTON_OBJECTS)


def get_tecton_objects_skip_validation(
    specified_repo_config: Optional[Path],
) -> Tuple[List[base_tecton_object.BaseTectonObject], str, List[Path], Path]:
    repo_file_handler.ensure_prepare_repo()
    repo_files = repo_file_handler.repo_files()
    repo_root = repo_file_handler.repo_root()

    repo_config = _maybe_load_repo_config_or_default(specified_repo_config)

    py_files = [p for p in repo_files if p.suffix == ".py"]
    os.chdir(Path(repo_root))

    # Skip validate() during object initialization. We only do server-side validation in NDD environment
    with conf._temporary_set("TECTON_SKIP_OBJECT_VALIDATION", True):
        top_level_objects = collect_top_level_objects(py_files, repo_root=Path(repo_root), pretty_errors=True)

    return top_level_objects, repo_root, repo_files, repo_config


def _maybe_load_repo_config_or_default(repo_config_path: Optional[Path]) -> Path:
    if repo_config_path is None:
        repo_config_path = cli__repo_config.get_default_repo_config_path()

    if framework__repo_config.get_repo_config() is None:
        # Load the repo config. The repo config may have already been loaded if tecton objects were collected multiple
        # times, e.g. during `tecton plan` the objects are collected for tests and then the plan.
        cli__repo_config.load_repo_config(repo_config_path)

    return repo_config_path
