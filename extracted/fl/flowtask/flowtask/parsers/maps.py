from typing import Optional
from ..conf import TASK_PATH
from .json import JSONParser
from ._yaml import YAMLParser
from ..exceptions import ComponentError


async def open_map(
    filename: str, program: str = "navigator", ext: Optional[str] = "json"
):
    model_file = TASK_PATH.joinpath(program, "maps", f"{filename}.{ext}")
    if model_file.is_file():
        try:
            if ext == "json":
                json = JSONParser(str(model_file))
                return await json.run()
            elif ext == "yaml":
                yaml = YAMLParser(str(model_file))
                return await yaml.run()
            else:
                raise ComponentError(
                    f"Task Error: Unsupported Method for Open Maps: {ext!s}"
                )
        except Exception as err:
            raise ComponentError(f"Task: Open Map Error: {err}") from err
    else:
        return False


async def open_model(
    filename: str, program: str = "navigator", ext: Optional[str] = "json"
):
    model_file = TASK_PATH.joinpath(program, "models", f"{filename}.json")
    if model_file.is_file():
        try:
            if ext == "json":
                json = JSONParser(str(model_file))
                return await json.run()
            elif ext == "yaml":
                yaml = YAMLParser(str(model_file))
                return await yaml.run()
            else:
                raise ComponentError(
                    f"Task Error: Unsupported Method for Open Maps: {ext!s}"
                )
        except Exception as err:
            raise ComponentError(f"Task: Open Map Error: {err}") from err
    else:
        return False
