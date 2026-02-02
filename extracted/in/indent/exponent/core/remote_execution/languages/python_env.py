import re
import sys

from exponent.core.remote_execution.types import PythonEnvInfo


def get_python_env_info() -> PythonEnvInfo:
    return PythonEnvInfo(
        interpreter_path=get_active_python_interpreter_path(),
        interpreter_version=get_active_python_interpreter_version(),
    )


def get_active_python_interpreter_path() -> str | None:
    return sys.executable


def get_active_python_interpreter_version() -> str | None:
    version = sys.version

    match = re.search(r"(\d+\.\d+\.\d+).*", version)

    if match:
        return match.group(1)

    return None
