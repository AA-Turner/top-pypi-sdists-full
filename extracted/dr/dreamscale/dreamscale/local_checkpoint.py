"""A local π0.5 checkpoint folder, for `dreamscale deployments create ./folder`.

Detect reads a listing of the folder, not the folder: every file's size, the bytes of the
small files detection reads (``*.json``, Orbax ``_METADATA``, small ``*.safetensors``) and the
header of each large ``*.safetensors``. The server answers with the files a build of the
chosen checkpoint reads (its params, statistics and configs; never code, pickles or
``train_state/``), and only those are uploaded: content-addressed, so a re-run sends nothing
new and an interrupted upload resumes (``dreamscale.uploads``).

An ABC-VLA ``.pt`` checkpoint is a zip of stored members: its listing carries the bytes a
reader of its directory and pickle reads (``archives``), and the upload sends only the
members a build reads (``data.pkl`` and the model's tensor storages), each as its own blob.
"""

from __future__ import annotations

import base64
import json
import os
import re
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dreamscale import errors

# Files a small-file read may send whole (the intake's own small-file limit).
SMALL_FILE_BYTES = 8 << 20
# A safetensors header larger than this isn't a checkpoint's.
MAX_HEADER_BYTES = 100 << 20
# What one listing carries at most (the intake refuses more).
MAX_FILES = 20_000
MAX_LISTING_BYTES = 16 << 20
# ABC-VLA checkpoints (torch zip archives) and the folder a single one's upload names its
# members under: <file>.members/<member>.
ARCHIVE_SUFFIXES = (".pt", ".pth")
MEMBERS = ".members/"
# The file names a build may read (the intake's rule): plain characters, no hidden parts.
_NAME = re.compile(r"[A-Za-z0-9._-]+(/[A-Za-z0-9._-]+)*\Z")


@dataclass(frozen=True)
class LocalFolder:
    root: Path
    files: dict[str, int]  # path relative to root -> size

    @property
    def label(self) -> str:
        """A default name: the folder's, with its parent's when it's a bare step number."""
        root = self.root.resolve()
        if root.name.isdigit() and root.parent.name:
            return f"{root.parent.name} {root.name}"[:100]
        return (root.name or "checkpoint")[:100]


def is_local_folder(value: str) -> bool:
    text = value.strip()
    return not text.startswith("hf://") and Path(text).expanduser().is_dir()


def trained_base(value: str, path: str | None = None) -> str | None:
    """The base a `dreamscale train download` folder names in its dreamscale.json, if any."""
    if not is_local_folder(value):
        return None
    record = Path(value.strip()).expanduser() / (path or "") / "dreamscale.json"
    try:
        base = json.loads(record.read_text()).get("base")
    except (OSError, ValueError, AttributeError):
        return None
    return base if isinstance(base, str) else None


def is_local_archive(value: str) -> bool:
    """A local ``.pt``/``.pth`` file (an ABC-VLA checkpoint named directly)."""
    text = value.strip()
    path = Path(text).expanduser()
    return not text.startswith("hf://") and path.suffix in ARCHIVE_SUFFIXES and path.is_file()


def scan_archive(path: str | Path) -> LocalFolder:
    """A single checkpoint file, as the folder holding only it."""
    file = Path(path).expanduser()
    if not _NAME.fullmatch(file.name):
        raise _invalid(f"{file.name} isn't a name a build reads",
                       "rename it to letters, digits, '.', '_' and '-'", file.parent)
    return LocalFolder(file.parent, {file.name: file.stat().st_size})


def _invalid(problem: str, fix: str, root: Path) -> errors.DreamscaleError:
    return errors.DreamscaleError(
        errors.ErrorInfo(code="invalid_folder", problem=problem, cause=f"read from {root}",
                         fix=fix)
    )


def scan(path: str | Path) -> LocalFolder:
    """Every file under ``path`` a build could read (hidden files and folders, and names
    with other characters, are left out)."""
    root = Path(path).expanduser()
    files: dict[str, int] = {}
    for folder, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for name in sorted(names):
            rel = (Path(folder) / name).relative_to(root).as_posix()
            if name.startswith(".") or not _NAME.fullmatch(rel):
                continue
            target = Path(folder) / name
            if target.is_file():
                files[rel] = target.stat().st_size
            if len(files) > MAX_FILES:
                raise _invalid(
                    f"{root} holds more than {MAX_FILES:,} files",
                    "point at the checkpoint's own folder (e.g. checkpoints/55000)", root,
                )
    if not files:
        raise _invalid(f"{root} holds no files", "point at a π0.5 checkpoint folder", root)
    return LocalFolder(root, files)


def _header(path: Path) -> bytes | None:
    """A safetensors file's header JSON bytes, or None when it isn't one."""
    with path.open("rb") as handle:
        head = handle.read(8)
        if len(head) < 8:
            return None
        (length,) = struct.unpack("<Q", head)
        if length > MAX_HEADER_BYTES:
            return None
        return handle.read(length)


def listing(folder: LocalFolder) -> dict[str, Any]:
    """What Detect reads: ``files`` (path -> size), and base64 ``contents`` of the small
    files detection reads and ``headers`` of the large safetensors files."""
    contents: dict[str, str] = {}
    headers: dict[str, str] = {}
    sent = 0
    for rel, size in folder.files.items():
        parts = rel.split("/")
        if "train_state" in parts:
            continue  # optimizer state: never read
        leaf = parts[-1]
        data: bytes | None = None
        if leaf.endswith(".safetensors") and size > SMALL_FILE_BYTES:
            data = _header(folder.root / rel)
            if data is not None:
                headers[rel] = base64.b64encode(data).decode()
        elif (leaf == "_METADATA" or leaf.endswith((".json", ".safetensors", ".yaml"))) and (
            size <= SMALL_FILE_BYTES
        ):
            data = (folder.root / rel).read_bytes()
            contents[rel] = base64.b64encode(data).decode()
        sent += len(data or b"")
        if sent > MAX_LISTING_BYTES:
            raise _invalid(
                f"{folder.root} holds more than {MAX_LISTING_BYTES >> 20} MB of configuration "
                "files",
                "point at the checkpoint's own folder (e.g. checkpoints/55000)", folder.root,
            )
    return {"files": dict(folder.files), "contents": contents, "headers": headers}


def archives(folder: LocalFolder) -> dict[str, list[list[Any]]]:
    """For each ``.pt``/``.pth`` file, the spans (offset, base64 bytes) a reader of its zip
    directory and pickle reads: the server inspects the checkpoint from these alone. A file
    that isn't a readable checkpoint archive is left out (Detect says what it found)."""
    from dreamscale_transport import torch_archive as ta

    out: dict[str, list[list[Any]]] = {}
    sent = 0
    for rel in folder.files:
        if not rel.endswith(ARCHIVE_SUFFIXES):
            continue
        with ta.FileReader(folder.root / rel) as file:
            reader = ta.RecordingReader(file)
            try:
                ta.open_archive(reader)
            except ta.ArchiveError:
                continue
        out[rel] = [[offset, base64.b64encode(data).decode()] for offset, data in reader.spans]
        sent += sum(len(data) for _, data in reader.spans)
        if sent > MAX_LISTING_BYTES:
            raise _invalid(
                f"{folder.root} holds more checkpoints than one listing can describe",
                "point at one checkpoint (its .pt file, or the folder holding it)", folder.root,
            )
    return out


def upload_plan(folder: LocalFolder, found: dict[str, Any]) -> tuple[
    list[tuple[str, int]], dict[str, Any]
]:
    """The files Detect said a build reads, with ``uploads.Slice`` for each archive member
    it named (``upload.members``: blob path -> {file, member}), located in the file now."""
    from dreamscale_transport import torch_archive as ta

    from dreamscale.uploads import Slice

    members = (found.get("upload") or {}).get("members") or {}
    names = (found.get("upload") or {}).get("files")
    if not isinstance(names, list) or not names or not isinstance(members, dict):
        raise errors.catalog("pi05_deployments_unavailable")
    files, slices, directories = [], {}, {}
    for name in names:
        source = members.get(name)
        if source is None:
            if name not in folder.files:
                raise _invalid(f"{name} is no longer in the folder",
                               "rerun the command on the unchanged folder", folder.root)
            files.append((name, folder.files[name]))
            continue
        file = source.get("file") if isinstance(source, dict) else None
        if file not in folder.files or name != f"{file}{MEMBERS}{source.get('member')}":
            raise _invalid(f"{file or name} is no longer in the folder",
                           "rerun the command on the unchanged folder", folder.root)
        try:
            with ta.FileReader(folder.root / file) as reader:
                if file not in directories:
                    directories[file] = ta.read_directory(reader)
                offset, length = ta.member_span(reader, directories[file], source["member"])
        except (OSError, ta.ArchiveError) as error:
            raise _invalid(f"{file} changed since it was read ({error})",
                           "rerun the command on the unchanged checkpoint", folder.root) from None
        slices[name] = Slice(folder.root / file, offset, length)
        files.append((name, length))
    return files, slices


def upload_files(folder: LocalFolder, found: dict[str, Any]) -> list[tuple[str, int]]:
    """(path, size) of each file Detect said a build reads, as they are in the folder."""
    names = (found.get("upload") or {}).get("files")
    if not isinstance(names, list) or not names:
        raise errors.catalog("pi05_deployments_unavailable")
    missing = [name for name in names if name not in folder.files]
    if missing:
        raise _invalid(f"{missing[0]} is no longer in the folder",
                       "rerun the command on the unchanged folder", folder.root)
    return [(name, folder.files[name]) for name in names]


def describe(found: dict[str, Any]) -> str:
    from dreamscale.trainings import size_text

    upload = found.get("upload") or {}
    count = len(upload.get("files") or [])
    return f"{count} file{'s' if count != 1 else ''}, {size_text(int(upload.get('bytes') or 0))}"
