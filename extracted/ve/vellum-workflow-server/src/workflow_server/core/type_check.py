import pathlib
import tempfile
from typing import Any, Literal, Union

from workflow_server.core.type_checker import get_checker
from workflow_server.core.type_checker.base import TypeCheckResult


def type_check(
    files: dict[str, str],
    type_checker: Union[Literal["zuban", "mypy"], None, Any] = None,
) -> TypeCheckResult:
    if type_checker in ("mypy", "zuban"):
        runner = get_checker(type_checker)
    else:
        runner = get_checker()

    configuration_status = runner.is_configured()
    if not configuration_status[0]:
        return TypeCheckResult(
            success=False,
            failure_message=configuration_status[1],
        )

    with tempfile.TemporaryDirectory(prefix="pws_type_check_") as tmpdir:
        tmpdir_path = pathlib.Path(tmpdir).resolve()
        write_files(tmpdir_path, files)

        return runner.run(tmpdir_path)


def write_files(tmpdir_path: pathlib.Path, files: dict[str, str]) -> None:
    for file_name, file_content in files.items():
        # Skip directory entries
        if file_name.endswith("/"):
            continue

        raw_path = pathlib.Path(file_name)

        # Users shouldn't specify absolute paths
        # since we stuff files into random namespaces.
        if raw_path.is_absolute():
            raise ValueError(f"File {raw_path} is absolute")

        target = (tmpdir_path / raw_path).resolve()
        if not target.is_relative_to(tmpdir_path):
            raise ValueError(f"File {raw_path} is not in {tmpdir_path}")

        # Create the parent directories if they don't exist
        target.parent.mkdir(parents=True, exist_ok=True)

        # Write the file content
        target.write_text(file_content)


def build_cache() -> None:
    mypy_checker = get_checker("mypy")
    configuration_status = mypy_checker.is_configured()
    if configuration_status[0]:
        mypy_checker.build_cache()
