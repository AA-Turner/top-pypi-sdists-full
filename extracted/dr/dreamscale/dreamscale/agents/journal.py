"""A fresh, fsynced execution journal per run. Journals are never replayed."""

import json
import os
from pathlib import Path


class Journal:
    def __init__(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError as exc:
            raise RuntimeError(
                "Existing journal: start a fresh attended run; never replay pending motion."
            ) from exc
        self.file = os.fdopen(fd, "w")
        self.seen = set()
        self.write({"event": "start"})
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)

    def write(self, value):
        self.file.write(json.dumps(value, allow_nan=False) + "\n")
        self.file.flush()
        os.fsync(self.file.fileno())

    def begin(self, identity, *, call=None):
        if identity in self.seen:
            raise RuntimeError("This motion identity was already dispatched; start a fresh run.")
        self.write(
            {
                "event": "executing",
                "call_id": identity,
                "requested": call.model_dump(mode="json") if call else None,
            }
        )
        self.seen.add(identity)

    def finish(self, receipt):
        self.write({"event": "receipt", **receipt.model_dump(mode="json")})

    def close(self):
        self.file.close()
