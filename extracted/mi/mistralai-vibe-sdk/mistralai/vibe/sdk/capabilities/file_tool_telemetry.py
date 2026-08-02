"""Telemetry helpers for SDK-provided file tools."""

from pathlib import PurePath

from pydantic import ValidationError

from mistralai.vibe.sdk.capabilities.builtins.read_file_tool import ReadFileResult
from mistralai.vibe.sdk.capabilities.builtins.search_replace_tool import SearchReplaceResult
from mistralai.vibe.sdk.capabilities.builtins.write_file_tool import WriteFileResult
from mistralai.vibe.sdk.execution_record.state import CompletedOutput


def builtin_file_metrics(
    *,
    tool_name: str | None,
    output: CompletedOutput,
) -> dict[str, int | str]:
    if not isinstance(output.value, dict):
        return {}

    try:
        match tool_name:
            case "write_file":
                result = WriteFileResult.model_validate(output.value)
                metrics: dict[str, int | str] = (
                    {"nb_files_modified": 1} if result.file_existed else {"nb_files_created": 1}
                )
                return metrics | _file_extension(result.path)
            case "search_replace":
                result = SearchReplaceResult.model_validate(output.value)
                metrics = {"nb_files_modified": 1} if result.lines_changed > 0 else {}
                return metrics | _file_extension(result.file)
            case "read_file":
                result = ReadFileResult.model_validate(output.value)
                return _file_extension(result.path)
    except ValidationError:
        return {}

    return {}


def _file_extension(path: str) -> dict[str, int | str]:
    extension = PurePath(path).suffix.lower()
    return {"file_extension": extension} if extension else {}
