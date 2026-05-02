import logging
import os
import pathlib
import re
from typing import Optional

from workflow_server.core.type_checker.base import ConfigurationStatus, TypeCheckResult, WorkflowTypeChecker

logger = logging.getLogger(__name__)


def _get_mypy_overrides() -> list[str]:
    import importlib.util

    if not importlib.util.find_spec("mypy"):
        return []

    from importlib.metadata import version

    from packaging.version import parse as parse_version

    config_path = pathlib.Path(__file__).parent / "serialization.mypy.ini"
    cache_dir = os.getenv("VELLUM_MYPY_CACHE_DIR", "/var/tmp/vellum_mypy_cache")
    flags = [
        "--config-file",
        str(config_path),
        "--cache-dir",
        cache_dir,
    ]
    try:
        if parse_version(version("mypy")) >= parse_version("1.19.0"):
            flags.append("--fixed-format-cache")
    except Exception:
        logger.warning("Failed to determine mypy version. Using default cache format.")

    return flags


class MypyWorkflowTypeChecker(WorkflowTypeChecker):
    def is_configured(self) -> ConfigurationStatus:
        try:
            import mypy.api  # noqa: F401
        except ImportError:
            return False, "mypy is not installed in the current environment"

        self._is_configured = True
        return True, None

    def _run(self, dir: pathlib.Path) -> TypeCheckResult:
        if not self._is_configured:
            return TypeCheckResult(
                success=False,
                failure_message="mypy is not configured",
            )

        import mypy.api

        stdout, stderr, exit_code = mypy.api.run([str(dir), *_get_mypy_overrides()])
        return TypeCheckResult(
            success=exit_code == 0,
            type_errors=stdout,
            failure_message=stderr,
        )

    def _clean_type_errors(self, type_errors: str, dir: pathlib.Path) -> str:
        dir_prefix = re.escape(str(dir))
        pattern = re.compile(f"{dir_prefix}/?")
        return pattern.sub("", type_errors)

    def build_cache(self) -> Optional[str]:
        if not self._is_configured:
            logger.warning("mypy is not configured, skipping cache build")
            return None

        # Warm cache on Vellum SDK.
        import mypy.api

        _, stderr, exit_code = mypy.api.run(["-c", "import vellum; import vellum.workflows", *_get_mypy_overrides()])

        # Typically, an exit code of 1 indicates mypy successfully ran and outputted type errors to stdout,
        # and an exit code of 2 indicates an issue with how we invoked mypy.
        if stderr and exit_code:
            logger.warning(
                "Failed to build mypy cache",
                extra={"stderr": stderr, "exit_code": exit_code},
            )
            return stderr

        return None
