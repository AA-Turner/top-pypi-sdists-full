from __future__ import annotations

import contextlib
import os
import tempfile
from typing import Any

import yaml
from yaml.representer import SafeRepresenter

from .errors import InvalidFile
from .models import State


VERSION_ID = 2

# Present only while a `pull` is still running. The final write omits it, so the
# absence of this key is what tells the next `pull` the file is complete.
IN_PROGRESS_KEY = "AnomaloPullInProgress"


# Include AnomaloVersionID in the output file first without affecting subkey sorting
class MetadataWrapper:
    def __init__(self, data: Any, in_progress: bool = False):
        self.data = data
        self.in_progress = in_progress

    def __iter__(self):
        header: dict[str, Any] = {"AnomaloVersionID": VERSION_ID}
        if self.in_progress:
            header[IN_PROGRESS_KEY] = True
        yield from ({**header, **self.data}).items()


yaml.add_representer(
    MetadataWrapper, SafeRepresenter.represent_dict, Dumper=SafeRepresenter
)  # pytype: disable=wrong-arg-types


class FileDriver:
    def __init__(self, state: State | None = None):
        self.state = state or State()
        # Whether the file last loaded was left behind by an interrupted `pull`.
        self.pull_in_progress = False

    def load_file(self, filename: str) -> None:
        try:
            with open(filename) as file_handle:
                data = yaml.safe_load(file_handle)
        except FileNotFoundError as e:
            raise InvalidFile(filename, "cannot be read") from e
        except yaml.YAMLError as e:
            # A checkpoint killed mid-write leaves unparseable YAML. Report it as an
            # InvalidFile so callers get a message instead of a raw traceback.
            raise InvalidFile(filename, f"is not valid YAML: {e}") from e
        if not isinstance(data, dict) or data.get("AnomaloVersionID") != VERSION_ID:
            raise InvalidFile(filename, "invalid AnomaloVersionID")
        self.pull_in_progress = bool(data.get(IN_PROGRESS_KEY))
        self.state = State.from_dict(data)

    def write_file(self, filename: str, in_progress: bool = False) -> None:
        # Dump to a uniquely named sibling temp file and rename over the target, so
        # an interrupted or concurrent checkpoint write can never truncate the last
        # valid file. It also means the final write publishes a complete file and
        # clears the in-progress marker in one atomic step, with no window in which
        # a finished pull looks interrupted.
        dirname, basename = os.path.split(filename)
        fd, temp_filename = tempfile.mkstemp(
            dir=dirname or ".", prefix=f"{basename}.tmp."
        )
        try:
            with os.fdopen(fd, "w") as file_handle:
                yaml.safe_dump(
                    MetadataWrapper(self.state.to_dict(), in_progress), file_handle
                )
            os.replace(temp_filename, filename)
        except BaseException:
            with contextlib.suppress(OSError):
                os.unlink(temp_filename)
            raise

    def to_string(self) -> str:
        return yaml.safe_dump(self.state.to_dict())
