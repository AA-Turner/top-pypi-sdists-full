import ast
import glob
import os
import sys
from pathlib import Path
from typing import Callable
from typing import List

from tecton.cli import printer
from tecton_core.errors import TectonValidationError
from tecton_proto.modelartifactservice.model_artifact_data__client_pb2 import ModelType


def error_and_exit(message: str):
    error_message = f"⛔ {message}"
    printer.safe_print(error_message, file=sys.stderr)
    sys.exit(1)


def _find_function_and_validate(objects: List[ast.FunctionDef], name: str, condition: Callable[[int], bool]):
    find_object = [obj for obj in objects if obj.name == name]
    if not condition(len(find_object)):
        error_and_exit(f"Exactly one `{name}` function should be found in the model file.")


def validate(model_file: str, artifact_files: List[str], archive_root_path: Path) -> None:
    if Path(model_file).is_absolute():
        error_and_exit(f"Paths defined in ModelConfig must be relative paths. {model_file} is not a relative path.")
    model_file_path = archive_root_path / model_file
    if not os.path.isfile(model_file_path):
        error_and_exit(f"File {model_file_path} defined in ModelConfig does not exist.")

    invalid_file_paths = []
    for file_path in artifact_files:
        if Path(file_path).is_absolute():
            error_and_exit(f"Paths defined in ModelConfig must be relative paths. {file_path} is not a relative path.")
        files = glob.glob(str(archive_root_path / file_path))
        if len(files) == 0:
            invalid_file_paths.append(file_path)
        for file in files:
            if Path(archive_root_path).resolve() not in Path(file).resolve().parents:
                error_and_exit(
                    f"All `artifact_files` must be within directory containing model config file. {Path(archive_root_path).resolve()} : {Path(file).resolve().parents}"
                )
    if len(invalid_file_paths) > 0:
        error_and_exit(f"File paths: {','.join(invalid_file_paths)} defined in ModelConfig does not match any files.")

    model_file_text = model_file_path.read_text()
    ast_module = ast.parse(model_file_text)
    functions = [obj for obj in ast_module.body if type(obj) == ast.FunctionDef]

    _find_function_and_validate(functions, "load_context", lambda x: x == 1)
    _find_function_and_validate(functions, "preprocessor", lambda x: x <= 1)
    _find_function_and_validate(functions, "postprocessor", lambda x: x <= 1)


def model_type_string_to_enum(model_type: str) -> ModelType:
    if model_type == "pytorch":
        return ModelType.PYTORCH
    elif model_type == "python":
        return ModelType.PYTHON
    msg = f"Invalid Model Type: {model_type}"
    raise TectonValidationError(msg)
