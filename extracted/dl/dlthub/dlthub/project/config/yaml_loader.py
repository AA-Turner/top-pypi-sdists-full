import os
from typing import Any, TextIO

import yaml


def load_file(file_path: str) -> Any:
    with open(file_path, "r", encoding="utf-8") as file:
        # TODO: add error messages or prevent files containing only simple types to be loaded
        return yaml.load(file, IncludeLoader) or {}


def load_string(yaml_string: str) -> Any:
    return yaml.load(yaml_string, IncludeLoader) or {}


class IncludeLoader(yaml.FullLoader):
    """Custom YAML loader that supports !include tag to include other YAML files.

    Example:
    ```
    sources:
        my_source: !include source.yaml
    ```
    The above config will look for `source.yaml` in the same directory as the file being loaded.
    """

    def __init__(self, stream: TextIO) -> None:
        if hasattr(stream, "name"):
            self._base_dir = os.path.dirname(os.path.abspath(stream.name))
        else:
            self._base_dir = os.getcwd()
        super().__init__(stream)

    def include(self, node: Any) -> Any:
        filename = self.construct_scalar(node)
        file_path = os.path.join(self._base_dir, filename)
        return load_file(file_path)


IncludeLoader.add_constructor("!include", IncludeLoader.include)
