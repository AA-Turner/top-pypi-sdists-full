import pathlib
import importlib.util
from types import ModuleType


def load_local_module(name: str, path: pathlib.Path) -> ModuleType | None:
    spec = importlib.util.spec_from_file_location(name, path)

    if spec is None or spec.loader is None:
        return None

    module = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(module)
    except Exception as error:
        # TODO: Log this somewhere
        _exception = error
        return None

    return module
