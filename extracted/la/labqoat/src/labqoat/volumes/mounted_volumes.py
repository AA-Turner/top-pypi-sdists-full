"""The volumes this worker's host mounted, as the host recorded them."""

from __future__ import annotations

import base64
import json
import os
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import ClassVar

from labqoat.json_document import JsonDocument
from labqoat.volumes.background_commits import BackgroundCommits
from labqoat.volumes.disk_watch import DiskWatch
from labqoat.volumes.mounted_volume import MountedVolume
from labqoat.volumes.worker_volume_api import WorkerVolumeApi
from labqoat.worker.scoped_api import ScopedApi


class MountedVolumes:
    """Every volume mounted into this workload, committed at the end of each call and every 30 seconds."""

    INTERVAL: ClassVar[float] = 30.0
    _current: ClassVar[tuple[tuple[str, str], MountedVolumes] | None] = None

    def __init__(self, mounts: tuple[MountedVolume, ...]) -> None:
        """Hold the workload's mounts."""
        self.mounts = mounts
        self._background: BackgroundCommits | None = None
        self._disk = DiskWatch()

    @classmethod
    def current(cls) -> MountedVolumes:
        """The mounts of this workload, read once per set of credentials; none outside a worker."""
        directory = os.environ.get("LABQOAT_VOLUMES_DIR", "")
        if not directory:
            return cls(())
        key = (directory, os.environ.get("LABQOAT_CREDENTIAL_ID", ""))
        if cls._current is None or cls._current[0] != key:
            cls._current = (key, cls.read(Path(directory)))
        return cls._current[1]

    @classmethod
    def read(cls, directory: Path) -> MountedVolumes:
        """Read the host's record of the mounts and reach their volumes under the run's credentials."""
        document = JsonDocument.expect_dict(json.loads((directory / "mounts.json").read_text()))
        credential = f"{os.environ['LABQOAT_CREDENTIAL_ID']}:{os.environ['LABQOAT_WORKER_SECRET']}"
        headers = {"X-Labqoat-Worker-Authorization": "Basic " + base64.b64encode(credential.encode()).decode()}
        api = ScopedApi(os.environ["LABQOAT_API_URL"], headers, "/api/v1/worker/", timeout_seconds=300.0)
        records = [JsonDocument.expect_dict(item) for item in JsonDocument.expect_list(document["mounts"])]
        return cls(tuple(cls._mount(directory, index, record, api) for index, record in enumerate(records)))

    @staticmethod
    def _mount(directory: Path, index: int, record: JsonDocument, api: ScopedApi) -> MountedVolume:
        """One recorded mount, whose base is kept beside the record."""
        name = JsonDocument.expect_scalar(record["name"], str)
        subpath = JsonDocument.expect_scalar(record.get("subpath", ""), str)
        changes = record.get("changes")
        return MountedVolume(
            Path(JsonDocument.expect_scalar(record["path"], str)),
            name,
            JsonDocument.expect_scalar(record["volume"], str),
            JsonDocument.expect_scalar(record["read_only"], bool),
            directory / f"{index}.json",
            record,
            WorkerVolumeApi(api, name, subpath),
            subpath,
            Path(JsonDocument.expect_scalar(changes, str)) if changes is not None else None,
        )

    def named(self, name: str, subpath: str = "") -> MountedVolume:
        """The writable mount of volume ``name``, of its directory ``subpath`` when one mounts it, or its only mount.

        An unmounted volume is an error.
        """
        mounted = [mount for mount in self.mounts if mount.name == name]
        if not mounted:
            raise LookupError(f"Volume {name!r} is not mounted in this worker; add it to the function's volumes")
        chosen = [mount for mount in mounted if mount.subpath == subpath] or mounted
        return next((mount for mount in chosen if not mount.read_only), chosen[0])

    def commit_all(self) -> None:
        """Commit every writable mount."""
        for mount in self.mounts:
            if not mount.read_only:
                self._disk.check(mount.path, mount.name)
                mount.commit()

    def start(self) -> None:
        """Commit writable mounts in the background for as long as the process lives."""
        if self._background is None and any(not mount.read_only for mount in self.mounts):
            self._background = BackgroundCommits(self.commit_all, self.INTERVAL)
            self._background.start()

    @classmethod
    @contextmanager
    def settled(cls) -> Iterator[None]:
        """Commit every writable mount when a call ends, whether it returned or raised.

        A failure to commit after the call raised is reported and the call's own error is the one that
        propagates; after a call that returned, a failure to commit fails the call.
        """
        try:
            yield
        except BaseException:
            cls.quietly()
            raise
        cls.commit_current()

    @classmethod
    def commit_current(cls) -> None:
        """Commit every writable mount of this workload."""
        cls.current().commit_all()

    @classmethod
    def released(cls) -> None:
        """Commit what this workload changed, stop committing and forget the mounts and the credentials they use.

        A worker does this before it saves its memory: whichever process continues from the snapshot reads its
        own host's mounts under its own credentials the next time it needs them.
        """
        cls.quietly()
        current = cls.current()
        if current._background is not None:
            current._background.stop()
            current._background = None
        cls._current = None

    @classmethod
    def quietly(cls) -> None:
        """Commit every writable mount, reporting rather than raising a failure."""
        try:
            cls.commit_current()
        except Exception as error:
            print(f"Volume commit failed: {error}", file=sys.stderr, flush=True)
