"""dreamscale.datasets — keep your LeRobot datasets on Dreamscale and train on them.

    ds = dreamscale.datasets.upload("./towels")           # Dataset('acme/towels', version=2)
    hub = dreamscale.datasets.import_from("hf://lerobot/svla_so100_pickplace")  # waits for it
    ds = dreamscale.datasets.get("towels@1")              # pinned to v1; "towels" is the latest
    for d in dreamscale.datasets.list():
        print(d.full_name, d.latest_version, d.summary["episodes"])

    run = dreamscale.trainings.create(dataset=ds, base=base, max_usd=50)  # trains ds.version
    run = ds.train(base=base, max_usd=50)                                 # the same
    ds.download("./towels-copy")
    ds.rename("yam-towels")
    dreamscale.datasets.delete("towels@1")                # one version; "towels" deletes all

A dataset is a name and a list of immutable versions. Uploading changed files adds a version;
uploading the same files adds nothing. Uploads resume, from any machine.
"""

from __future__ import annotations

import asyncio
import builtins
import os
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

from dreamscale import errors, policy  # noqa: F401 - policy first: it and control import each other
from dreamscale.control import ControlPlaneClient
from dreamscale.trainings import _client, call, dataset_name_for

IMPORT_POLL_S = 3.0
IMPORT_RUNNING = ("queued", "copying")


def split_ref(ref: str) -> tuple[str, int | None]:
    """``towels@2`` -> (``towels``, 2)."""
    name, at, tail = ref.strip().partition("@")
    if not at:
        return name, None
    if not (tail.isdigit() and int(tail) > 0):
        raise errors.DreamscaleError(
            errors.ErrorInfo(
                code="invalid_dataset_name",
                problem=f"{ref} doesn't name a version",
                cause="a version is a number: towels@2",
                fix="dreamscale datasets show NAME lists its versions",
            )
        )
    return name, int(tail)


class DatasetVersion:
    """One immutable version of a dataset."""

    def __init__(self, dataset: Dataset, data: dict) -> None:
        self._dataset = dataset
        self.data = data

    number = property(lambda self: self.data["version"])
    bytes = property(lambda self: self.data.get("bytes"))
    files = property(lambda self: self.data.get("files"))
    summary = property(lambda self: self.data.get("summary") or {})
    source = property(lambda self: self.data.get("source") or {})
    created_at = property(lambda self: self.data.get("created_at"))

    def __repr__(self) -> str:
        return f"DatasetVersion({self._dataset.full_name!r}, {self.number})"

    def delete(self) -> None:
        self._dataset.delete(version=self.number)


class Dataset:
    """A dataset, and the version this handle points at (its latest unless pinned)."""

    def __init__(
        self, data: dict, *, version: int | None = None,
        client_factory: Callable[..., Any] = ControlPlaneClient,
    ) -> None:
        self.data = data
        self._pinned = version
        self._client_factory = client_factory

    id = property(lambda self: self.data["id"])
    name = property(lambda self: self.data["name"])
    full_name = property(lambda self: self.data["full_name"])
    latest_version = property(lambda self: self.data.get("latest_version"))
    bytes = property(lambda self: self.data.get("bytes"))
    last_used_at = property(lambda self: self.data.get("last_used_at"))

    @property
    def version(self) -> int | None:
        return self._pinned or self.latest_version

    @property
    def summary(self) -> dict:
        return self.data.get("summary") or {}

    @property
    def versions(self) -> builtins.list[DatasetVersion]:
        if "versions" not in self.data:
            self.refresh()
        return [DatasetVersion(self, v) for v in self.data.get("versions") or []]

    @property
    def ref(self) -> str:
        """What ``trainings.create`` reads: this dataset, at this version."""
        return f"{self.id}@{self.version}" if self.version else self.id

    def __repr__(self) -> str:
        return f"Dataset({self.full_name!r}, version={self.version})"

    def refresh(self) -> Dataset:
        self.data = call(self._client_factory, "get_dataset", self.id)
        return self

    def rename(self, name: str) -> Dataset:
        """The old name keeps working until another dataset takes it."""
        self.data = call(self._client_factory, "rename_dataset", self.id, name)
        return self

    def delete(self, version: int | None = None) -> None:
        """Delete it for good, or one version. Runs and deployments made from it keep working."""
        if version is not None:
            call(self._client_factory, "delete_dataset_version", self.id, version)
        else:
            call(self._client_factory, "delete_dataset", self.id)

    def download(self, dest: str | os.PathLike, version: int | None = None) -> Path:
        """A version (default this handle's) into a LeRobot folder; rerun to resume."""
        number = version or self.version
        if number is None:
            raise _empty(self.full_name)
        return _download(self._client_factory, self.id, number, Path(dest))

    def train(self, *, base: str, max_usd: Any, **options: Any) -> Any:
        from dreamscale import trainings

        return trainings.create(
            dataset=self, base=base, max_usd=max_usd, client_factory=self._client_factory,
            **options,
        )


class DatasetImport:
    """A copy of a Hugging Face dataset into a dataset, running on our side."""

    def __init__(
        self, dataset: dict, data: dict, *,
        client_factory: Callable[..., Any] = ControlPlaneClient,
    ) -> None:
        self.dataset = dataset
        self.data = data
        self._client_factory = client_factory

    id = property(lambda self: self.data["id"])
    status = property(lambda self: self.data["status"])

    @property
    def progress(self) -> tuple[int, int]:
        """(bytes copied, bytes in all)."""
        return int(self.data.get("bytes_done") or 0), int(self.data.get("bytes_total") or 0)

    def __repr__(self) -> str:
        return f"DatasetImport({self.id!r}, status={self.status!r})"

    def refresh(self) -> DatasetImport:
        self.data = call(self._client_factory, "get_dataset_import", self.dataset["id"], self.id)
        return self

    def wait(
        self, *, sleep: Callable[[float], None] = time.sleep,
        on_progress: Callable[[DatasetImport], None] | None = None,
    ) -> Dataset:
        """Until the copy finishes: the dataset at its new version. Raises the import's error."""
        while self.status in IMPORT_RUNNING:
            if on_progress is not None:
                on_progress(self)
            sleep(IMPORT_POLL_S)
            self.refresh()
        if self.status != "ready":
            raise import_error(self.data)
        return Dataset(
            call(self._client_factory, "get_dataset", self.dataset["id"]),
            client_factory=self._client_factory,
        )

    def cancel(self) -> DatasetImport:
        self.data = call(
            self._client_factory, "cancel_dataset_import", self.dataset["id"], self.id
        )
        return self


def import_error(data: dict) -> errors.DreamscaleError:
    error = data.get("error") or {}
    if data.get("status") == "canceled":
        error = {"code": "import_canceled", "message": "The import was canceled",
                 "fix": "Run the same command again to copy it."}
    return errors.DreamscaleError(
        errors.ErrorInfo(
            code=str(error.get("code") or "import_failed"),
            problem=str(error.get("message") or "the import failed"),
            cause=f"import {data.get('id')}",
            fix=str(error.get("fix") or "run the same command again"),
        )
    )


def _empty(name: str) -> errors.DreamscaleError:
    return errors.DreamscaleError(
        errors.ErrorInfo(
            code="dataset_empty",
            problem=f"dataset {name} has no data yet",
            cause="a dataset has data once an upload or import of it finishes",
            fix=f"dreamscale datasets upload ./folder --name {name}",
        )
    )


def ensure(name: str, client_factory: Callable[..., Any]) -> dict:
    """The dataset named ``name``, created if it doesn't exist yet."""
    return _ensure(name, client_factory)[0]


def _ensure(name: str, client_factory: Callable[..., Any]) -> tuple[dict, bool]:
    """``(the dataset, whether this call created it)``."""
    try:
        return call(client_factory, "get_dataset", name), False
    except errors.DreamscaleError as error:
        if error.code != "dataset_not_found":
            raise
    try:
        return call(client_factory, "create_dataset", name), True
    except errors.DreamscaleError as error:
        if error.code != "dataset_exists":  # another upload created it first
            raise
    return call(client_factory, "get_dataset", name), False


def start_import(
    name: str, parsed: dict, token: str | None, client_factory: Callable[..., Any]
) -> tuple[dict, dict]:
    """``(the import route's answer, the dataset)``. A refused import takes back the empty dataset
    it created: a wrong repo name mustn't leave a row behind."""
    dataset, created = _ensure(name, client_factory)
    try:
        answer = call(client_factory, "create_dataset_import", dataset["id"], repo=parsed["repo"],
                      revision=parsed["revision"], path=parsed["path"], hf_token=token)
    except errors.DreamscaleError:
        if created:
            try:
                call(client_factory, "delete_dataset", dataset["id"])
            except errors.DreamscaleError:
                pass  # an empty row is harmless, and the refusal is what to show
        raise
    return answer, dataset


def send(
    client_factory: Callable[..., Any], dataset_id: str, root: Path, files, *,
    progress=None, transport=None, concurrency: int | None = None,
) -> dict:
    """Upload ``files`` as the dataset's next version."""
    from dreamscale import uploads

    async def go() -> dict:
        client = _client(client_factory)
        try:
            return await uploads.upload_dataset(
                client, dataset_id, root, files, progress=progress, transport=transport,
                concurrency=concurrency or uploads.DATASET_CONCURRENCY,
            )
        finally:
            await client.close()

    return asyncio.run(go())


def _download(client_factory, ref: str, version: int, dest: Path, *, progress=None,
              transport=None) -> Path:
    from dreamscale import uploads

    async def go() -> dict:
        client = _client(client_factory)
        try:
            return await uploads.download_dataset(
                client, ref, version, dest, progress=progress, transport=transport
            )
        finally:
            await client.close()

    asyncio.run(go())
    return dest


def upload(
    path: str | os.PathLike, *, name: str | None = None, check: bool = True,
    progress: Callable[[int, int, int], None] | None = None,
    client_factory: Callable[..., Any] = ControlPlaneClient,
) -> Dataset:
    """Upload a folder to a dataset (``name`` defaults to the folder's): unchanged data returns
    the existing version, and an interrupted upload resumes. ``check`` runs the hardware check
    here first; it's informational, and raises nothing."""
    from dreamscale.lerobot_dataset import hardware_check, open_upload

    folder = open_upload(path)
    if check and folder.local is not None:
        try:
            hardware_check(folder.local)
        except Exception:  # noqa: BLE001 - informational: training checks again
            pass
    wanted = name or dataset_name_for(folder.root.expanduser().resolve().name)
    dataset = ensure(wanted, client_factory)
    done = send(client_factory, dataset["id"], folder.root, folder.files, progress=progress)
    return Dataset(done["dataset"], client_factory=client_factory)


def parse_hf(source: str) -> dict[str, str | None]:
    """``hf://owner/name[/folder][@revision]`` as the import route takes it."""
    text = source.strip()
    if not text.startswith("hf://"):
        raise errors.DreamscaleError(
            errors.ErrorInfo(
                code="invalid_import_source",
                problem=f"{source} isn't a Hugging Face dataset",
                cause="an import reads hf://owner/name",
                fix="pass hf://owner/name[/folder][@revision]",
            )
        )
    where, _, revision = text.removeprefix("hf://").partition("@")
    pieces = where.strip("/").split("/")
    if len(pieces) < 2:
        raise errors.DreamscaleError(
            errors.ErrorInfo(
                code="invalid_import_source",
                problem=f"{source} isn't a Hugging Face dataset",
                cause="a dataset is owner/name",
                fix="pass hf://owner/name[/folder][@revision]",
            )
        )
    return {"repo": "/".join(pieces[:2]), "path": "/".join(pieces[2:]) or None,
            "revision": revision or None}


def import_from(
    source: str, *, name: str | None = None, hf_token: str | None = None, wait: bool = True,
    client_factory: Callable[..., Any] = ControlPlaneClient,
) -> Dataset | DatasetImport:
    """Copy a Hugging Face dataset in, on our side (``name`` defaults to the repo's). With
    ``wait=False``, the running ``DatasetImport``."""
    parsed = parse_hf(source)
    token = hf_token or os.environ.get("HF_TOKEN") or None
    wanted = name or dataset_name_for(str(parsed["repo"]).rsplit("/", 1)[-1])
    answer, dataset = start_import(wanted, parsed, token, client_factory)
    if answer.get("unchanged"):
        return Dataset(answer["dataset"], client_factory=client_factory)
    running = DatasetImport(dataset, answer, client_factory=client_factory)
    return running.wait() if wait else running


def get(ref: str, *, client_factory: Callable[..., Any] = ControlPlaneClient) -> Dataset:
    """A dataset by name, ``account/name`` or id; ``name@N`` pins the handle to that version."""
    name, version = split_ref(ref)
    return Dataset(call(client_factory, "get_dataset", name), version=version,
                   client_factory=client_factory)


def list(*, client_factory: Callable[..., Any] = ControlPlaneClient) -> builtins.list[Dataset]:
    return [Dataset(d, client_factory=client_factory)
            for d in call(client_factory, "list_datasets")]


def delete(ref: str, *, client_factory: Callable[..., Any] = ControlPlaneClient) -> None:
    """``name`` deletes the dataset; ``name@N`` one version."""
    name, version = split_ref(ref)
    if version is not None:
        call(client_factory, "delete_dataset_version", name, version)
    else:
        call(client_factory, "delete_dataset", name)
