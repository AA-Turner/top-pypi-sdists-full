from __future__ import annotations

from typing import Any

import yaml
from yaml.representer import SafeRepresenter

from .errors import InvalidFile
from .models import State


VERSION_ID = 2


# Include AnomaloVersionID in the output file first without affecting subkey sorting
class MetadataWrapper:
    def __init__(self, data: Any):
        self.data = data

    def __iter__(self):
        yield from ({**{"AnomaloVersionID": VERSION_ID}, **self.data}).items()


yaml.add_representer(
    MetadataWrapper, SafeRepresenter.represent_dict, Dumper=SafeRepresenter
)  # pytype: disable=wrong-arg-types


class FileDriver:
    def __init__(self, state: State | None = None):
        self.state = state or State()

    def load_file(self, filename: str) -> None:
        try:
            with open(filename) as file_handle:
                data = yaml.safe_load(file_handle)
        except FileNotFoundError as e:
            raise InvalidFile(filename, "cannot be read") from e
        if not isinstance(data, dict) or data.get("AnomaloVersionID") != VERSION_ID:
            raise InvalidFile(filename, "invalid AnomaloVersionID")
        self.state = State.from_dict(data)

    def write_file(self, filename: str) -> None:
        with open(filename, "w") as file_handle:
            yaml.safe_dump(MetadataWrapper(self.state.to_dict()), file_handle)

    def to_string(self) -> str:
        return yaml.safe_dump(self.state.to_dict())
