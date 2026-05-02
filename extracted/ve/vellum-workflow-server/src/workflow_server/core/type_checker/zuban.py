import pathlib
import re
import shutil
import subprocess
from typing import Optional

from workflow_server.core.type_checker.base import ConfigurationStatus, TypeCheckResult, WorkflowTypeChecker


class ZubanWorkflowTypeChecker(WorkflowTypeChecker):
    def __init__(self, zuban_path: Optional[str] = None):
        super().__init__()

        if not zuban_path:
            zuban_path = shutil.which("zuban")

        self.zuban_path = zuban_path

    def is_configured(self) -> ConfigurationStatus:
        if not self.zuban_path:
            return False, "zuban not found"

        self._is_configured = True
        return True, None

    def _run(self, dir: pathlib.Path) -> TypeCheckResult:
        if not self.zuban_path:
            return TypeCheckResult(success=False, failure_message="zuban not found")

        try:
            data_path = pathlib.Path(__file__).parent / "serialization.mypy.ini"
            res = subprocess.run(
                [self.zuban_path, "check", dir.name, "--config-file", str(data_path)],
                capture_output=True,
                text=True,
                cwd=dir.parent,
            )
        except OSError as e:
            return TypeCheckResult(
                success=False,
                failure_message=f"Unexpected failure running zuban: {e}",
            )

        if res.returncode == 0:
            return TypeCheckResult(
                success=True,
            )
        elif res.returncode == 1:
            return TypeCheckResult(
                success=False,
                type_errors=res.stdout,
                failure_message=res.stderr,
            )
        else:
            return TypeCheckResult(
                success=False,
                failure_message=f"Unexpected failure running zuban:\n{res.stderr}",
            )

    def _clean_type_errors(self, type_errors: str, dir: pathlib.Path) -> str:
        dir_prefix = re.escape(str(dir.name))
        pattern = re.compile(f"{dir_prefix}/?")
        return pattern.sub("", type_errors)
