# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Multi-base (Lance ``base_paths``) placement helpers.

Lance multi-base datasets spread fragment data files across several storage
bases: the manifest records ``base_paths`` (id -> URI) and each ``DataFile``
carries an optional ``base_id``. These helpers resolve which base a fragment
lives in so backfill can co-locate the fragment's checkpoints and staged
output data files with its data (see ``MultiBaseCheckpointStore``).
"""

import logging
from typing import TYPE_CHECKING
from urllib.parse import urlparse, urlunparse

import attrs

if TYPE_CHECKING:
    import lance

    from geneva.checkpoint import CheckpointStore

_LOG = logging.getLogger(__name__)

# Lance layout constant: data files of a dataset-root base live under
# ``{base}/data``; non-root bases hold data files directly.
_DATA_DIR = "data"


def _join_uri_path(uri: str, segment: str) -> str:
    """Append a path segment to a URI, keeping its query and fragment.

    An object-store URI may carry credentials in the query (e.g. an Azure SAS
    token); a plain URL join would drop them and downstream sessions built
    from the result would read unauthenticated.
    """
    parsed = urlparse(uri)
    path = f"{parsed.path.rstrip('/')}/{segment}"
    return urlunparse(parsed._replace(path=path))


@attrs.define(frozen=True)
class DatasetBaseInfo:
    """One entry of a Lance dataset's ``Manifest.base_paths``."""

    base_id: int
    uri: str
    is_dataset_root: bool

    @property
    def data_dir(self) -> str:
        """Directory holding this base's data files."""
        if self.is_dataset_root:
            return _join_uri_path(self.uri, _DATA_DIR)
        return self.uri

    def checkpoint_root(self, subdir: str) -> str:
        """Checkpoint store root for this base (same subdir as the table)."""
        return _join_uri_path(self.uri, subdir)


def resolve_dataset_bases(ds: "lance.LanceDataset") -> dict[int, DatasetBaseInfo]:
    """Read ``Manifest.base_paths`` from a dataset.

    Returns an empty dict for single-base datasets or pylance versions
    without multi-base support.
    """
    base_paths_fn = getattr(getattr(ds, "_ds", None), "base_paths", None)
    if base_paths_fn is None:
        return {}
    bases: dict[int, DatasetBaseInfo] = {}
    for base_id, base_path in base_paths_fn().items():
        bases[int(base_id)] = DatasetBaseInfo(
            base_id=int(base_id),
            uri=str(base_path.path).rstrip("/"),
            is_dataset_root=bool(base_path.is_dataset_root),
        )
    return bases


def resolve_fragment_bases(fragments: list) -> dict[int, int]:
    """Map fragment id -> base id using each fragment's first data file.

    Fragments are written wholesale into one base, so the first data file
    identifies where the fragment's data lives; it is also stable across
    backfill commits, which only append output data files. Fragments rooted
    at the dataset root (``base_id`` absent) are omitted.
    """
    frag_to_base: dict[int, int] = {}
    for frag in fragments:
        data_files = frag.data_files()
        if not data_files:
            continue
        base_id = getattr(data_files[0], "base_id", None)
        if base_id is None:
            continue
        frag_to_base[frag.fragment_id] = int(base_id)
        base_ids = {getattr(df, "base_id", None) for df in data_files}
        if len(base_ids) > 1:
            _LOG.debug(
                "fragment %d has data files in multiple bases %s; "
                "placing with first data file's base %d",
                frag.fragment_id,
                base_ids,
                base_id,
            )
    return frag_to_base


@attrs.define(frozen=True)
class FragmentBasePlacement:
    """Resolved multi-base placement for one backfill destination dataset."""

    bases: dict[int, DatasetBaseInfo]
    frag_to_base: dict[int, int]

    @classmethod
    def from_dataset(cls, ds: "lance.LanceDataset") -> "FragmentBasePlacement | None":
        """Resolve placement for ``ds``; None when it is not multi-base.

        ``frag_to_base`` may be empty when no current fragment lives in a
        base (all data at the dataset root).
        """
        bases = resolve_dataset_bases(ds)
        if not bases:
            return None
        frag_to_base = resolve_fragment_bases(ds.get_fragments())
        frag_to_base = {
            frag_id: base_id
            for frag_id, base_id in frag_to_base.items()
            if base_id in bases
        }
        return cls(bases=bases, frag_to_base=frag_to_base)

    def base_id_for_frag(self, frag_id: int) -> int | None:
        return self.frag_to_base.get(frag_id)

    def data_dir_for_frag(self, frag_id: int) -> str | None:
        """Data-file directory for ``frag_id``; None means the dataset root."""
        base_id = self.frag_to_base.get(frag_id)
        if base_id is None:
            return None
        base = self.bases.get(base_id)
        return base.data_dir if base is not None else None

    def base_data_dirs(self) -> dict[int, str]:
        """Base id -> data-file directory, for bases holding any fragment."""
        used = set(self.frag_to_base.values())
        return {
            base_id: base.data_dir
            for base_id, base in self.bases.items()
            if base_id in used
        }

    def base_checkpoint_uris(
        self, subdir: str, *, include_unused_bases: bool = False
    ) -> dict[int, str]:
        """Base id -> checkpoint root.

        By default only bases holding a current fragment are included;
        ``include_unused_bases`` adds every registered base (cleanup sweeps
        need to reach checkpoints of fragments dropped from the manifest).
        """
        used = set(self.frag_to_base.values())
        return {
            base_id: base.checkpoint_root(subdir)
            for base_id, base in self.bases.items()
            if include_unused_bases or base_id in used
        }


def multi_base_placement_enabled() -> bool:
    """Whether fragment-base checkpoint/data placement is enabled."""
    from geneva.checkpoint import CheckpointConfig

    try:
        return bool(CheckpointConfig.get().multi_base_placement)
    except Exception:
        # Field default. Loud on purpose: an operator disabling the feature
        # through a malformed config value would otherwise silently keep it
        # enabled.
        _LOG.warning(
            "could not read checkpoint config; multi-base placement stays "
            "enabled (CHECKPOINT__MULTI_BASE_PLACEMENT)",
            exc_info=True,
        )
        return True


# First pylance release whose DataReplacement commit preserves
# ``DataFile.base_id`` (both the replace-existing-file branch and the
# new-column special case) and stats staged files against their base
# (lance-format/lance#7609, released in 9.0.0-beta.14). Older pylance
# resolves the replacement file against the dataset root and the commit
# fails, so staged output files are placed in fragment bases only at/after
# this version. Checkpoint placement is geneva-internal and is not gated.
# NOTE: geneva's pin is held below this until a release also containing the
# 2.0 blob projection fix (lance-format/lance#7620) ships — b14 cannot scan
# blob columns in 2.0-layout files at all.
_MIN_LANCE_FOR_BASE_DATA_REPLACEMENT = "9.0.0-beta.14"


def lance_supports_multi_base_data_replacement() -> bool:
    """Whether the installed pylance can commit DataReplacement into bases."""
    import lance
    from packaging.version import Version

    try:
        return Version(lance.__version__) >= Version(
            _MIN_LANCE_FOR_BASE_DATA_REPLACEMENT
        )
    except Exception:
        return False


def _resolve_base_storage_options(store: object) -> dict[str, str] | None:
    """Storage options for base checkpoint stores.

    Base stores are plain-rooted (no namespace session), so when the table's
    store relies on namespace credential vending, describe the table once and
    reuse its storage options. Best-effort: None falls back to ambient
    credentials.
    """
    storage_options = getattr(store, "storage_options", None)
    if storage_options:
        return dict(storage_options)
    try:
        resolve = getattr(store, "_resolve_namespace_client", None)
        table_id = getattr(store, "table_id", None)
        if resolve is None or not table_id:
            return None
        client = resolve()
        if client is None:
            return None
        from lance_namespace import DescribeTableRequest

        response = client.describe_table(DescribeTableRequest(id=table_id))
        opts = getattr(response, "storage_options", None)
        return dict(opts) if opts else None
    except Exception:
        _LOG.warning(
            "failed to resolve storage options for base checkpoint stores",
            exc_info=True,
        )
        return None


def maybe_wrap_checkpoint_store_for_bases(
    store: "CheckpointStore",
    placement: FragmentBasePlacement | None,
    *,
    include_unused_bases: bool = False,
) -> "CheckpointStore":
    """Wrap a Lance-backed store so fragment checkpoints follow their base.

    Returns the store unchanged for single-base placements, non-Lance stores
    (e.g. in-memory), or an already-wrapped store. The per-base checkpoint
    roots reuse the table store's subdir (last segment of its root), so
    operator overrides like ``GENEVA_CHECKPOINT_SUBDIR`` carry over.
    """
    from geneva.checkpoint import (
        FlatLanceCheckpointStore,
        MultiBaseCheckpointStore,
    )

    if placement is None or isinstance(store, MultiBaseCheckpointStore):
        return store
    if not isinstance(store, FlatLanceCheckpointStore):
        return store
    subdir = store.root.rstrip("/").rsplit("/", 1)[-1]
    if not subdir:
        return store
    base_uris = placement.base_checkpoint_uris(
        subdir, include_unused_bases=include_unused_bases
    )
    if not base_uris:
        return store
    return MultiBaseCheckpointStore(
        store,
        base_checkpoint_uris=base_uris,
        frag_to_base=dict(placement.frag_to_base),
        base_storage_options=_resolve_base_storage_options(store),
    )
