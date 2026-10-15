"""Which Hugging Face Hub repos a Trainer starts from and reads (plan data-catalog R9).

The base model a fine-tune starts from and the Hub datasets it trains and
evaluates on are the start of every provenance chain, and the common
fine-tune path should get them with no code change. This module only READS
names off the objects the Trainer hands its callbacks -- ids and revisions,
never content -- and imports neither transformers nor datasets: it is pure
duck typing, so it is testable without either.

* A model: ``model.config._name_or_path`` when it names a Hub repo (``org/name``
  or a bare legacy id such as ``gpt2``) and not a path on this machine, with
  ``config._commit_hash`` as the revision when transformers recorded one.
  A local folder (a custom model, a checkpoint) records nothing: no link is
  better than a wrong one.
* A dataset: a ``datasets`` object whose files came from the Hub -- named in its
  download checksums (``hf://datasets/ORG/NAME@REV/...`` or
  ``https://huggingface.co/datasets/ORG/NAME/resolve/REV/...``), in its cache
  folder (``.../ORG___NAME/...``), or by a Hub ``info.dataset_name`` -- with the
  Hub revision when one is named, else the dataset's own fingerprint.
  Datasets loaded from local files (the packaged ``json``/``csv``/``parquet``
  builders) record nothing.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any

HUB = "https://huggingface.co"

#: A Hub repo id: `name` or `namespace/name` (Hub rules: no `--` or `..`).
_REPO_ID = re.compile(r"^(?:[A-Za-z0-9][A-Za-z0-9._-]{0,95}/)?[A-Za-z0-9][A-Za-z0-9._-]{0,95}$")
#: A commit sha, as transformers records it.
_SHA = re.compile(r"^[0-9a-f]{40}$")
#: A dataset file's download URL naming the repo and revision.
_HF_URL = re.compile(
    r"^(?:hf://datasets/(?P<repo>[^@/]+(?:/[^@/]+)?)@(?P<rev>[^/]+)/"
    r"|https://huggingface\.co/datasets/(?P<repo2>[^/]+/[^/]+)/resolve/(?P<rev2>[^/]+)/)"
)
#: The datasets cache folder of a Hub dataset: `<namespace>___<name>`.
_CACHE_DIR = re.compile(r"/(?P<ns>[A-Za-z0-9][A-Za-z0-9._-]*)___(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)/")
#: Builders that read local files: a dataset named after one of these is not a Hub id.
_PACKAGED = frozenset(
    {"json", "csv", "parquet", "text", "arrow", "pandas", "imagefolder", "audiofolder", "videofolder",
     "webdataset", "generator", "sql", "cache", "xml", "pdffolder", "niftifolder", "spark", "eval"}
)


@dataclass(frozen=True)
class HubRef:
    """One Hub repo a Trainer used: what `probe.source` registers."""

    uri: str
    kind: str  # "model" | "dataset"
    revision: str | None


def _hub_repo(name: Any) -> str | None:
    if not isinstance(name, str):
        return None
    name = name.strip()
    if not name or "--" in name or ".." in name or not _REPO_ID.match(name):
        return None
    if os.path.isabs(name) or name.startswith((".", "~")) or os.path.exists(name):
        return None
    return name


def base_model(model: Any) -> HubRef | None:
    """The Hub model ``model`` was loaded from, or None."""
    config = getattr(model, "config", None)
    repo = _hub_repo(getattr(config, "_name_or_path", None)) if config is not None else None
    if repo is None:
        return None
    commit = getattr(config, "_commit_hash", None)
    return HubRef(uri=f"{HUB}/{repo}", kind="model", revision=commit if isinstance(commit, str) and _SHA.match(commit) else None)


def _is_datasets_object(obj: Any) -> bool:
    module = type(obj).__module__ or ""
    return module == "datasets" or module.startswith("datasets.")


def hub_dataset(obj: Any) -> HubRef | None:
    """The Hub dataset a ``datasets.Dataset`` (or ``IterableDataset``) came
    from, or None for anything else (a torch Dataset, local files)."""
    if obj is None or not _is_datasets_object(obj):
        return None
    info = getattr(obj, "info", None)
    fingerprint = getattr(obj, "_fingerprint", None)
    fingerprint = fingerprint if isinstance(fingerprint, str) and fingerprint else None
    checksums = getattr(info, "download_checksums", None) or {}
    for url in checksums if isinstance(checksums, dict) else ():
        match = _HF_URL.match(str(url))
        if match:
            repo = match.group("repo") or match.group("repo2")
            rev = match.group("rev") or match.group("rev2")
            return HubRef(uri=f"{HUB}/datasets/{repo}", kind="dataset", revision=rev or fingerprint)
    for entry in getattr(obj, "cache_files", None) or ():
        filename = entry.get("filename") if isinstance(entry, dict) else None
        match = _CACHE_DIR.search(str(filename or "").replace(os.sep, "/"))
        if match:
            return HubRef(uri=f"{HUB}/datasets/{match.group('ns')}/{match.group('name')}", kind="dataset", revision=fingerprint)
    name = getattr(info, "dataset_name", None)
    if isinstance(name, str) and name.lower() not in _PACKAGED:
        repo = _hub_repo(name)
        if repo is not None:
            return HubRef(uri=f"{HUB}/datasets/{repo}", kind="dataset", revision=fingerprint)
    return None


def loader_dataset(dataloader: Any) -> Any:
    """The dataset behind a DataLoader (accelerate's wrappers keep `.dataset`)."""
    seen = 0
    obj = dataloader
    while obj is not None and seen < 4 and not _is_datasets_object(obj):
        obj = getattr(obj, "dataset", None)
        seen += 1
    return obj
