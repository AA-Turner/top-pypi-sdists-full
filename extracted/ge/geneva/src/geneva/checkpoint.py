# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Checkpoint Store for Geneva Pipeline"""

import abc
import contextlib
import json
import logging
import os
import re
import tempfile
import threading
from collections.abc import Callable, Iterator
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from typing import TYPE_CHECKING, Optional, cast

import attrs
import lance
import pyarrow as pa
from lance.file import LanceFileSession
from packaging.version import Version

from geneva.checkpoint_utils import hash_string
from geneva.config import ConfigBase, str_to_bool
from geneva.errors import CorruptCheckpointError
from geneva.utils import retry_lance
from geneva.utils.storage import timed_list, timed_list_with_delimiter

if TYPE_CHECKING:
    from lance_namespace import LanceNamespace

_LOG = logging.getLogger(__name__)

# Fault-injection hook: wrap every store returned by the constructors below.
# Identity by default; tests install a wrapper via ``using_checkpoint_store_wrap`` or
# the ``GENEVA_FAULT_CHECKPOINT`` env var. The wrapper lives in the external
# ``geneva_faults`` test library, not in this module.
_CHECKPOINT_WRAP: "Callable[[CheckpointStore], CheckpointStore]" = lambda s: s  # noqa: E731


def _apply_checkpoint_wrap(store: "CheckpointStore") -> "CheckpointStore":
    return _CHECKPOINT_WRAP(store)


def get_checkpoint_store_wrap() -> "Callable[[CheckpointStore], CheckpointStore]":
    """The wrapper applied to every store returned by ``from_uri``."""
    return _CHECKPOINT_WRAP


def set_checkpoint_store_wrap(
    fn: "Callable[[CheckpointStore], CheckpointStore]",
) -> None:
    """Install ``fn`` as the store wrapper process-wide (test-only); pass the identity
    ``lambda s: s`` to reset to production behavior."""
    global _CHECKPOINT_WRAP
    _CHECKPOINT_WRAP = fn


@contextlib.contextmanager
def using_checkpoint_store_wrap(
    fn: "Callable[[CheckpointStore], CheckpointStore]",
) -> "Iterator[Callable[[CheckpointStore], CheckpointStore]]":
    """Install ``fn`` for the duration of the block, restoring the prior wrapper."""
    prev = _CHECKPOINT_WRAP
    set_checkpoint_store_wrap(fn)
    try:
        yield fn
    finally:
        set_checkpoint_store_wrap(prev)


# Checkpoints are transient scratch files, so they should never be blob-encoded: a
# nullable blob column hits a Lance reader panic on read (GEN-578). On write we
# rename ``lance-encoding:blob`` to a Geneva marker on the same field so the column
# is stored with ordinary (FullZip) encoding instead of the buggy BlobLayout path;
# on read we rename it back so the committed fragment — whose schema the writer
# derives from the checkpoint batch — stays blob-encoded. The marker travels with
# the field and survives Lance's metadata round-trip, so no path bookkeeping or
# schema-level state is needed.
_BLOB_ENCODING_KEY = b"lance-encoding:blob"
_WAS_BLOB_KEY = b"geneva::checkpoint::was-blob"
_ARROW_EXTENSION_NAME_KEY = b"ARROW:extension:name"
_LANCE_BLOB_V2_EXTENSION_NAME = b"lance.blob.v2"
_WAS_BLOB_V2_EXTENSION_KEY = b"geneva::checkpoint::was-blob-v2-extension"
_BLOB_V2_DESCRIPTOR_MARKER = b"descriptor"
_BLOB_V2_EXTENSION_TYPE_MARKER = b"extension-type"
_RANGE_CHECKPOINT_SUFFIX_RE = re.compile(r"_range-\d+-\d+$")
# Backfill checkpoint keys end with ``_frag-{id}`` (fragment dedupe) or
# ``_frag-{id}_range-{start}-{end}`` (per-batch). Keys without this suffix
# (UDTF, chunker, legacy sha256 dedupe keys) have no fragment identity and
# always live in the table-root checkpoint store.
_FRAG_KEY_SUFFIX_RE = re.compile(r"_frag-(\d+)(?:_range-\d+-\d+)?$")


def parse_frag_id_from_checkpoint_key(key: str) -> int | None:
    """Return the fragment id encoded in a backfill checkpoint key, or None."""
    match = _FRAG_KEY_SUFFIX_RE.search(key)
    if match is None:
        return None
    return int(match.group(1))


def _checkpoint_identity_prefix_for_column(identity: str, column: str) -> str | None:
    before_col, col_sep, after_col = identity.rpartition(f"_col-{column}_")
    if not col_sep or not after_col.startswith("where-"):
        return None
    return before_col


def _parse_udf_version_from_checkpoint_identity(
    identity: str, column: str
) -> str | None:
    before_col = _checkpoint_identity_prefix_for_column(identity, column)
    if before_col is None:
        return None

    _, ver_sep, version = before_col.rpartition("_ver-")
    if not ver_sep or not version:
        return None
    return version


def _fragment_checkpoint_identity_for_column(
    key: str, column: str
) -> tuple[str, str] | None:
    fragment_prefix, frag_sep, frag_suffix = key.rpartition("_frag-")
    if (
        not frag_sep
        or _RANGE_CHECKPOINT_SUFFIX_RE.search(key)
        or "_range-" in frag_suffix
    ):
        return None

    before_col = _checkpoint_identity_prefix_for_column(fragment_prefix, column)
    if before_col is None:
        return None
    return before_col, frag_suffix


def _parse_udf_version_from_fragment_checkpoint_key(
    key: str, column: str
) -> str | None:
    """Extract the UDF version token from a target-column fragment key.

    Returns ``None`` for non-fragment keys, range checkpoints, keys for another
    column, or unknown/legacy key shapes that do not expose a parseable
    ``_ver-...`` token before ``_col-{column}_``.
    """

    parsed = _fragment_checkpoint_identity_for_column(key, column)
    if parsed is None:
        return None
    before_col, frag_suffix = parsed
    if not frag_suffix.isdigit():
        return None

    _, ver_sep, version = before_col.rpartition("_ver-")
    if not ver_sep or not version:
        return None
    return version


def _is_fragment_checkpoint_for_column(key: str, column: str) -> bool:
    return _fragment_checkpoint_identity_for_column(key, column) is not None


def _swap_field_blob_marker(
    field: pa.Field, from_key: bytes, to_key: bytes
) -> pa.Field:
    """Rebuild ``field``, renaming metadata key ``from_key`` -> ``to_key`` wherever
    it appears, recursing into struct/list children so nested blob fields are
    covered. The value is normalized to ``b"true"``."""
    dtype = field.type
    if pa.types.is_struct(dtype):
        dtype = pa.struct([_swap_field_blob_marker(c, from_key, to_key) for c in dtype])
    elif pa.types.is_large_list(dtype):
        dtype = pa.large_list(
            _swap_field_blob_marker(dtype.value_field, from_key, to_key)
        )
    elif pa.types.is_list(dtype):
        dtype = pa.list_(_swap_field_blob_marker(dtype.value_field, from_key, to_key))
    metadata = dict(field.metadata or {})
    if from_key in metadata:
        metadata.pop(from_key)
        metadata[to_key] = b"true"
    return pa.field(
        field.name, dtype, nullable=field.nullable, metadata=metadata or None
    )


def _swap_batch_blob_marker(
    batch: pa.RecordBatch, from_key: bytes, to_key: bytes
) -> pa.RecordBatch:
    """Return ``batch`` with the blob-encoding metadata key renamed across all
    (possibly nested) fields. Returns the input unchanged when nothing matches, so
    non-blob and legacy checkpoints pass through untouched."""
    new_schema = pa.schema(
        [_swap_field_blob_marker(f, from_key, to_key) for f in batch.schema]
    )
    if batch.schema.metadata:
        new_schema = new_schema.with_metadata(batch.schema.metadata)
    if new_schema.equals(batch.schema, check_metadata=True):
        return batch
    return pa.record_batch(batch.columns, schema=new_schema)


def _is_blob_v2_extension_type(dtype: pa.DataType) -> bool:
    return isinstance(
        dtype, pa.ExtensionType
    ) and dtype.extension_name == _LANCE_BLOB_V2_EXTENSION_NAME.decode("utf-8")


def _blob_v2_extension_type() -> pa.ExtensionType:
    return cast("pa.ExtensionType", lance.blob_field("__geneva_blob").type)


def _strip_field_blob_v2_extension(
    field: pa.Field, array: pa.Array
) -> tuple[pa.Field, pa.Array]:
    if _is_blob_v2_extension_type(field.type):
        extension_array = cast("pa.ExtensionArray", array)
        storage = extension_array.storage
        metadata = dict(field.metadata or {})
        metadata[_WAS_BLOB_V2_EXTENSION_KEY] = _BLOB_V2_EXTENSION_TYPE_MARKER
        return (
            pa.field(
                field.name,
                storage.type,
                nullable=field.nullable,
                metadata=metadata or None,
            ),
            storage,
        )

    dtype = field.type
    if pa.types.is_struct(dtype):
        struct_type = cast("pa.StructType", dtype)
        struct_array = cast("pa.StructArray", array)
        child_fields: list[pa.Field] = []
        child_arrays: list[pa.Array] = []
        for idx in range(struct_type.num_fields):
            child_field, child_array = _strip_field_blob_v2_extension(
                struct_type.field(idx),
                struct_array.field(idx),
            )
            child_fields.append(child_field)
            child_arrays.append(child_array)
        mask = struct_array.is_null() if struct_array.null_count else None
        array = pa.StructArray.from_arrays(
            child_arrays,
            fields=child_fields,
            mask=mask,
        )
        dtype = pa.struct(child_fields)

    metadata = dict(field.metadata or {})
    if metadata.get(_ARROW_EXTENSION_NAME_KEY) == _LANCE_BLOB_V2_EXTENSION_NAME:
        metadata.pop(_ARROW_EXTENSION_NAME_KEY)
        metadata[_WAS_BLOB_V2_EXTENSION_KEY] = _BLOB_V2_DESCRIPTOR_MARKER
    return (
        pa.field(field.name, dtype, nullable=field.nullable, metadata=metadata or None),
        array,
    )


def _restore_field_blob_v2_extension(
    field: pa.Field, array: pa.Array
) -> tuple[pa.Field, pa.Array]:
    metadata = dict(field.metadata or {})
    marker = metadata.get(_WAS_BLOB_V2_EXTENSION_KEY)
    if marker == _BLOB_V2_EXTENSION_TYPE_MARKER:
        metadata.pop(_WAS_BLOB_V2_EXTENSION_KEY, None)
        extension_type = _blob_v2_extension_type()
        return (
            pa.field(
                field.name,
                extension_type,
                nullable=field.nullable,
                metadata=metadata or None,
            ),
            pa.ExtensionArray.from_storage(extension_type, array),
        )

    dtype = field.type
    if pa.types.is_struct(dtype):
        struct_type = cast("pa.StructType", dtype)
        struct_array = cast("pa.StructArray", array)
        child_fields: list[pa.Field] = []
        child_arrays: list[pa.Array] = []
        for idx in range(struct_type.num_fields):
            child_field, child_array = _restore_field_blob_v2_extension(
                struct_type.field(idx),
                struct_array.field(idx),
            )
            child_fields.append(child_field)
            child_arrays.append(child_array)
        mask = struct_array.is_null() if struct_array.null_count else None
        array = pa.StructArray.from_arrays(
            child_arrays,
            fields=child_fields,
            mask=mask,
        )
        dtype = pa.struct(child_fields)

    if marker:
        metadata.pop(_WAS_BLOB_V2_EXTENSION_KEY, None)
        metadata[_ARROW_EXTENSION_NAME_KEY] = _LANCE_BLOB_V2_EXTENSION_NAME
    return (
        pa.field(field.name, dtype, nullable=field.nullable, metadata=metadata or None),
        array,
    )


def _strip_batch_blob_v2_extensions(batch: pa.RecordBatch) -> pa.RecordBatch:
    fields: list[pa.Field] = []
    arrays: list[pa.Array] = []
    for field, array in zip(batch.schema, batch.columns, strict=True):
        new_field, new_array = _strip_field_blob_v2_extension(field, array)
        fields.append(new_field)
        arrays.append(new_array)
    schema = pa.schema(
        fields,
        metadata=cast("dict[bytes | str, bytes | str] | None", batch.schema.metadata),
    )
    if schema.equals(batch.schema, check_metadata=True):
        return batch
    return pa.record_batch(arrays, schema=schema)


def _restore_batch_blob_v2_extensions(batch: pa.RecordBatch) -> pa.RecordBatch:
    fields: list[pa.Field] = []
    arrays: list[pa.Array] = []
    for field, array in zip(batch.schema, batch.columns, strict=True):
        new_field, new_array = _restore_field_blob_v2_extension(field, array)
        fields.append(new_field)
        arrays.append(new_array)
    schema = pa.schema(
        fields,
        metadata=cast("dict[bytes | str, bytes | str] | None", batch.schema.metadata),
    )
    if schema.equals(batch.schema, check_metadata=True):
        return batch
    return pa.record_batch(arrays, schema=schema)


def _field_has_blob_v2_descriptor(field: pa.Field) -> bool:
    if isinstance(
        field.type, pa.ExtensionType
    ) and field.type.extension_name == _LANCE_BLOB_V2_EXTENSION_NAME.decode("utf-8"):
        return True
    metadata = field.metadata or {}
    if metadata.get(_ARROW_EXTENSION_NAME_KEY) == _LANCE_BLOB_V2_EXTENSION_NAME:
        return True
    dtype = field.type
    if pa.types.is_struct(dtype):
        return any(_field_has_blob_v2_descriptor(child) for child in dtype)
    if pa.types.is_list(dtype) or pa.types.is_large_list(dtype):
        return _field_has_blob_v2_descriptor(dtype.value_field)
    return False


def _batch_lance_file_version(batch: pa.RecordBatch) -> str | None:
    if any(_field_has_blob_v2_descriptor(field) for field in batch.schema):
        return "2.2"
    return None


def _is_lance_reader_panic(exc: BaseException) -> bool:
    """True if ``exc`` is a Lance/pyo3 reader panic, not a normal IO/value error.

    Lance decodes via pyo3; an internal invariant violation (e.g. the nullable-blob
    decode bug) surfaces either as ``pyo3_runtime.PanicException`` (a BaseException,
    not Exception) or wrapped as ``pyarrow.lib.ArrowInvalid`` whose message reports a
    panicked task. Ordinary corruption raises a clean ``OSError`` and is excluded.
    """
    if type(exc).__name__ == "PanicException" or type(exc).__module__.startswith(
        "pyo3"
    ):
        return True
    return "panicked" in str(exc)


class CheckpointStore(abc.ABC):
    """Abstract class for checkpoint store, which is used to store intermediate results
      of Geneva pipelines.

    It is implemented as a key-value store of
    [`RecordBatch`][pyarrow.RecordBatch] objects.

    TODO: implementations are not consistently handling keys with '/'.  Please avoid it.
    """

    @abc.abstractmethod
    def __contains__(self, item: str) -> bool:
        pass

    @abc.abstractmethod
    def __getitem__(self, item: str) -> pa.RecordBatch:
        pass

    @abc.abstractmethod
    def __setitem__(self, key: str, value: pa.RecordBatch) -> None:
        pass

    @abc.abstractmethod
    def list_keys(self, prefix: str = "") -> Iterator[str]:
        """List all the available keys for check point."""

    @abc.abstractmethod
    def uri(self) -> str:
        pass

    @abc.abstractmethod
    def delete(self, key: str) -> None:
        """Delete a checkpoint by key.

        Raises
        ------
        KeyError
            If the key does not exist.
        """

    def delete_prefix(self, prefix: str) -> int:
        """Delete all checkpoints matching a prefix.

        Returns the number of deleted checkpoints.

        !!! warning
            Passing an empty string will match and delete **all** checkpoints.
        """
        keys = list(self.list_keys(prefix))
        for key in keys:
            self.delete(key)
        return len(keys)

    def has_udf_version_mismatch(self, column: str, current_udf_version: str) -> bool:
        """Return True if any existing fragment checkpoint for ``column``
        encodes a UDF version different from ``current_udf_version``.

        Stores own this check because the cheapest way to answer it
        depends on the layout. The default implementation iterates
        ``list_keys(prefix="udf-")`` and parses the version token out of
        each fragment-level key. Layouts with a content-identity
        structure (e.g. hierarchical bf= dirs) override this with scoped
        LISTs that avoid opening checkpoint payloads and skip range-only
        per-batch checkpoints (GEN-614).

        Returns False when no checkpoints exist for the column or all
        existing ones match the current version.
        """
        for key in self.list_keys(prefix="udf-"):
            if not _is_fragment_checkpoint_for_column(key, column):
                continue
            stored_version = _parse_udf_version_from_fragment_checkpoint_key(
                key, column
            )
            if stored_version is None:
                # Fragment key for this column with no parseable ``_ver-``
                # token; treat as a mismatch so the caller forces a
                # reprocess.
                return True
            if stored_version != current_udf_version:
                return True
        return False

    def has_srcfiles_hash_mismatch(
        self, column: str, current_srcfiles_hash: str
    ) -> bool:
        """Return True if any existing fragment checkpoint for ``column``
        encodes a srcfiles hash different from ``current_srcfiles_hash``.

        Used to detect when the UDF's input data has changed since the
        column was last computed (e.g. an input column was re-backfilled
        via alter_columns). Returns False if no checkpoints exist for the
        column, or all existing ones match the current hash.

        Default implementation iterates ``list_keys(prefix="udf-")`` and
        extracts each key's ``_srcfiles-{hash}`` segment. Stores with a
        content-identity layout override this with scoped LISTs per
        backfill-identity directory (GEN-614).
        """
        col_pattern = re.compile(rf"_col-{re.escape(column)}_")
        srcfiles_pattern = re.compile(r"_srcfiles-([a-f0-9]+)_")
        range_pattern = re.compile(r"_range-\d+-\d+$")
        existing_hashes: set[str] = set()
        for key in self.list_keys(prefix="udf-"):
            if not col_pattern.search(key):
                continue
            if range_pattern.search(key):
                continue
            m = srcfiles_pattern.search(key)
            if m:
                existing_hashes.add(m.group(1))
        if not existing_hashes:
            return False
        return current_srcfiles_hash not in existing_hashes

    def purge(self, key: str) -> None:
        """Hard-delete a checkpoint, physically reclaiming its storage.

        ``purge`` always reclaims a checkpoint's underlying bytes. The default
        ``self.delete(key)`` is correct for every store because ``delete``
        physically removes the data. Used by sweeps such as
        ``Table.cleanup_checkpoints``.

        Raises
        ------
        KeyError
            If the key does not exist.
        """
        self.delete(key)

    def purge_many(self, keys: list[str]) -> None:
        """Best-effort bulk hard-delete of many checkpoints.

        The inline cleanup path on fragment commit purges every batch
        checkpoint that rolled into the just-written fragment dedupe key —
        ~150 keys per fragment in steady state. Calling :meth:`purge`
        in a Python loop issues one serial blob-delete round-trip per key,
        which dominates commit wall-clock on Azure (see GEN-554).

        Subclasses backed by an object store override this to fan the
        per-blob deletes out over a thread pool / batch API and amortize
        the credential handshake across the whole batch.

        Best-effort: missing keys are silently skipped (matches the
        ``KeyError``-tolerant call site in
        ``FragmentWriterManager._record_fragment``).
        """
        for key in keys:
            with contextlib.suppress(KeyError):
                self.purge(key)

    @classmethod
    def from_uri(
        cls,
        uri: str,
        namespace_client_impl: Optional[str] = None,
        namespace_client_properties: Optional[dict[str, str]] = None,
        table_id: Optional[list[str]] = None,
        storage_options: Optional[dict[str, str]] = None,
        session_root_subdir: Optional[str] = None,
        write_identity_sidecar: bool = True,
        base_checkpoint_uris: Optional[dict[int, str]] = None,
        frag_to_base: Optional[dict[int, int]] = None,
        base_storage_options: Optional[dict[str, str]] = None,
    ) -> "CheckpointStore":
        """Construct a CheckpointStore from a URI.

        Picks the implementation class from ``CheckpointConfig.store_layout``:
        ``"flat"`` (default) returns :class:`FlatLanceCheckpointStore`;
        ``"hierarchical"`` returns :class:`HierarchicalLanceCheckpointStore`.

        When ``base_checkpoint_uris`` and ``frag_to_base`` are provided (a
        multi-base dataset), the store is wrapped in a
        :class:`MultiBaseCheckpointStore` that routes each fragment's
        checkpoints to that fragment's storage base.
        """
        if uri == "memory":
            return _apply_checkpoint_wrap(InMemoryCheckpointStore())
        try:
            if Version(lance.__version__) < Version("0.35.0b3"):
                _LOG.warning(
                    f"pylance {lance.__version__} has issues at scale.  "
                    "Upgrade to 0.35.0b3 or higher to avoid this."
                )
            store_cls = _select_store_class()
            if issubclass(store_cls, HierarchicalLanceCheckpointStore):
                store: CheckpointStore = store_cls(
                    uri,
                    namespace_client_impl=namespace_client_impl,
                    namespace_client_properties=namespace_client_properties,
                    table_id=table_id,
                    storage_options=storage_options,
                    session_root_subdir=session_root_subdir,
                    write_identity_sidecar=write_identity_sidecar,
                )
            else:
                store = store_cls(
                    uri,
                    namespace_client_impl=namespace_client_impl,
                    namespace_client_properties=namespace_client_properties,
                    table_id=table_id,
                    storage_options=storage_options,
                    session_root_subdir=session_root_subdir,
                )
            if base_checkpoint_uris and frag_to_base:
                store = MultiBaseCheckpointStore(
                    store,
                    base_checkpoint_uris=base_checkpoint_uris,
                    frag_to_base=frag_to_base,
                    base_storage_options=base_storage_options,
                    write_identity_sidecar=write_identity_sidecar,
                )
            return _apply_checkpoint_wrap(store)
        except Exception as e:
            raise ValueError(f"Invalid checkpoint store uri: {uri}") from e


def _select_store_class() -> type["FlatLanceCheckpointStore"]:
    """Return the configured Lance-backed checkpoint store class."""
    try:
        layout = CheckpointConfig.get().store_layout
    except Exception:
        # Config unavailable (e.g. partial test setup); fall back to flat.
        _LOG.warning("checkpoint config unavailable; using flat layout", exc_info=True)
        return FlatLanceCheckpointStore
    if layout == "hierarchical":
        _LOG.warning("using experimental hierarchical checkpoint layout")
        return HierarchicalLanceCheckpointStore
    return FlatLanceCheckpointStore


class MultiBaseCheckpointStore(CheckpointStore):
    """Routes each fragment's checkpoints to that fragment's storage base.

    Lance multi-base datasets spread fragment data files across several
    storage bases (``Manifest.base_paths`` + ``DataFile.base_id``). This
    wrapper keeps a fragment's checkpoints co-located with its data files:
    keys ending in ``_frag-{id}[_range-...]`` route to the store rooted at
    that fragment's base; all other keys (UDTF, chunker, legacy sha256
    dedupe keys) stay in the table-root ``default_store``.

    Reads fall back to the other stores on a miss so artifacts written
    before an upgrade (all at the table root) and checkpoints of fragments
    dropped from the manifest remain reachable. Deletes and purges remove
    every copy of a key across stores, since transient routing failures or
    pre-upgrade runs can leave the same key in more than one store.

    Base stores are plain-rooted (no namespace session): a namespace-backed
    ``LanceFileSession`` resolves paths relative to the table's dataset root,
    which cannot address a base outside the table location. Base stores use
    ``base_storage_options`` (falling back to the default store's
    storage_options) for credentials.
    """

    def __init__(
        self,
        default_store: CheckpointStore,
        *,
        base_checkpoint_uris: dict[int, str],
        frag_to_base: dict[int, int],
        base_storage_options: Optional[dict[str, str]] = None,
        write_identity_sidecar: bool = True,
    ) -> None:
        self.default_store = default_store
        self.base_checkpoint_uris = dict(base_checkpoint_uris)
        self.frag_to_base = dict(frag_to_base)
        self.base_storage_options = base_storage_options
        self.write_identity_sidecar = write_identity_sidecar
        self.base_stores: dict[int, CheckpointStore] = {
            base_id: self._make_base_store(base_uri)
            for base_id, base_uri in self.base_checkpoint_uris.items()
        }

    def _make_base_store(self, base_uri: str) -> CheckpointStore:
        store_cls = (
            type(self.default_store)
            if isinstance(self.default_store, FlatLanceCheckpointStore)
            else _select_store_class()
        )
        storage_options = self.base_storage_options
        if storage_options is None:
            storage_options = getattr(self.default_store, "storage_options", None)
        if issubclass(store_cls, HierarchicalLanceCheckpointStore):
            return store_cls(
                base_uri,
                storage_options=storage_options,
                write_identity_sidecar=self.write_identity_sidecar,
            )
        return store_cls(base_uri, storage_options=storage_options)

    def _store_for_key(self, key: str) -> CheckpointStore:
        """The store a key is written to (strict routing, no fallback)."""
        frag_id = parse_frag_id_from_checkpoint_key(key)
        if frag_id is None:
            return self.default_store
        base_id = self.frag_to_base.get(frag_id)
        if base_id is None:
            return self.default_store
        store = self.base_stores.get(base_id)
        if store is None:
            _LOG.warning(
                "checkpoint key %s routes to unknown base %d; using default store",
                key,
                base_id,
            )
            return self.default_store
        return store

    def _stores_for_key_read(self, key: str) -> list[CheckpointStore]:
        """Routed store first, then the remaining stores as read fallbacks."""
        routed = self._store_for_key(key)
        stores = [routed]
        if routed is not self.default_store:
            stores.append(self.default_store)
        stores.extend(s for s in self.base_stores.values() if s is not routed)
        return stores

    def store_for_frag(self, frag_id: int) -> CheckpointStore:
        """The store fragment ``frag_id``'s checkpoints are written to."""
        base_id = self.frag_to_base.get(frag_id)
        if base_id is None:
            return self.default_store
        return self.base_stores.get(base_id, self.default_store)

    def __contains__(self, item: str) -> bool:
        return any(item in store for store in self._stores_for_key_read(item))

    def __getitem__(self, item: str) -> pa.RecordBatch:
        stores = self._stores_for_key_read(item)
        for store in stores[:-1]:
            with contextlib.suppress(KeyError):
                return store[item]
        return stores[-1][item]

    def __setitem__(self, key: str, value: pa.RecordBatch) -> None:
        self._store_for_key(key)[key] = value

    def list_keys(self, prefix: str = "") -> Iterator[str]:
        seen: set[str] = set()
        for store in (self.default_store, *self.base_stores.values()):
            for key in store.list_keys(prefix):
                if key in seen:
                    continue
                seen.add(key)
                yield key

    def uri(self) -> str:
        return self.default_store.uri()

    def delete(self, key: str) -> None:
        """Delete ``key`` from every store that holds it.

        A key can exist in more than one store — written to the table root
        after a transient routing failure (or pre-upgrade) and again to its
        base on a re-run. Removing only the first located copy would leave a
        stale duplicate that reads and listings still see.

        Raises KeyError when no store holds the key.
        """
        removed = False
        for store in self._stores_for_key_read(key):
            with contextlib.suppress(KeyError):
                store.delete(key)
                removed = True
        if not removed:
            raise KeyError(key)

    def purge(self, key: str) -> None:
        """Hard-delete ``key`` from every store that holds it.

        Same every-copy semantics as :meth:`delete`; raises KeyError when no
        store holds the key.
        """
        removed = False
        for store in self._stores_for_key_read(key):
            with contextlib.suppress(KeyError):
                store.purge(key)
                removed = True
        if not removed:
            raise KeyError(key)

    def purge_many(self, keys: list[str]) -> None:
        # Strict routing, no cross-store sweep: purge_many is best-effort
        # (fragment-commit batch cleanup of keys written this run). Batch
        # keys written pre-upgrade at the table root for a base-routed
        # fragment are left for the Table.cleanup_checkpoints sweep, whose
        # per-key purge removes every copy across stores.
        grouped: dict[int, list[str]] = {}
        stores: dict[int, CheckpointStore] = {}
        for key in keys:
            store = self._store_for_key(key)
            grouped.setdefault(id(store), []).append(key)
            stores[id(store)] = store
        for store_id, group in grouped.items():
            stores[store_id].purge_many(group)

    def has_udf_version_mismatch(self, column: str, current_udf_version: str) -> bool:
        # Any-child delegation is correct here (a stale version in any store
        # is a mismatch) and keeps each child's layout-optimized scan.
        return any(
            store.has_udf_version_mismatch(column, current_udf_version)
            for store in (self.default_store, *self.base_stores.values())
        )

    # has_srcfiles_hash_mismatch is intentionally NOT delegated per child:
    # its contract is "current hash not in the UNION of stored hashes", and
    # per-fragment hashes are spread across stores (any-child delegation
    # reports a spurious mismatch whenever one store lacks the probed hash,
    # forcing full recomputes). The inherited default implementation walks
    # this wrapper's chained list_keys, which preserves union semantics.


def unwrap_default_checkpoint_store(store: "CheckpointStore") -> "CheckpointStore":
    """The table-root store behind a ``MultiBaseCheckpointStore``, else ``store``.

    For call sites that dispatch on the concrete store layout
    (e.g. hierarchical-only optimizations) and must see through the
    multi-base wrapper.
    """
    if isinstance(store, MultiBaseCheckpointStore):
        return store.default_store
    return store


def _purge_many_max_workers(default: int) -> int:
    """Thread fan-out cap for ``FlatLanceCheckpointStore.purge_many``.

    Reads ``CHECKPOINT__PURGE_MANY_MAX_WORKERS`` directly so operators can
    pin the worker count (or set it to ``1`` to skip the pool entirely and
    A/B against the serial path) without code changes. Read straight from
    ``os.environ`` because the nested-config loader requires a
    fully-specified ``object_store`` to resolve ``CHECKPOINT__*`` keys.
    """
    env = os.environ.get("CHECKPOINT__PURGE_MANY_MAX_WORKERS")
    if env is None:
        return default
    try:
        return max(1, int(env))
    except ValueError:
        return default


class InMemoryCheckpointStore(CheckpointStore):
    """In memory checkpoint store for testing purposes."""

    def __init__(self) -> None:
        self._store = {}

    def __repr__(self) -> str:
        return self._store.__repr__()

    def __contains__(self, item: str) -> bool:
        return item in self._store

    def __getitem__(self, item: str) -> pa.RecordBatch:
        return self._store[item]

    def __setitem__(self, key: str, value: pa.RecordBatch) -> None:
        self._store[key] = value

    def delete(self, key: str) -> None:
        if key not in self._store:
            raise KeyError(key)
        del self._store[key]

    def list_keys(self, prefix: str = "") -> Iterator[str]:
        for key in self._store:
            if key.startswith(prefix):
                yield key

    def uri(self) -> str:
        return "memory:///"


class FlatLanceCheckpointStore(CheckpointStore):
    """
    Stores checkpoint data as Lance formatted files under a flat ``_ckp/``
    prefix.

    Each checkpoint is one ``.lance`` entry directly under ``_ckp/`` with
    the public key string as its filename. The API mimics a dictionary.

    NOTE: The dict keys are actual paths in a file system and can be
    vulnerable to filesystem traversal attacks.
    """

    # Per-table subdir under the table location used by
    # ``TableReference.open_checkpoint_store`` when the env override
    # ``GENEVA_CHECKPOINT_SUBDIR`` is unset. Flat keeps ``_ckp`` for
    # backward compatibility with every table backfilled to date.
    DEFAULT_TABLE_SUBDIR = "_ckp"

    # Checkpoint subdirectory name (relative to dataset root)
    _CKP_SUBDIR = "_ckp"

    _LAYOUT_LABEL = "flat"

    # Thread fan-out for ``purge_many``. Each key contributes one blob entry
    # (its data), so a ~150-key fragment commit fans out to ~150 deletes; 32
    # workers overlaps the HTTP round-trips without tripping per-account burst
    # limits on Azure/S3.
    _PURGE_MANY_MAX_WORKERS = 32

    def __init__(
        self,
        root: str,
        namespace_client: Optional["LanceNamespace"] = None,
        namespace_client_impl: Optional[str] = None,
        namespace_client_properties: Optional[dict[str, str]] = None,
        table_id: Optional[list[str]] = None,
        storage_options: Optional[dict[str, str]] = None,
        session_root_subdir: Optional[str] = None,
    ) -> None:
        self.root = root
        self.namespace_client = namespace_client
        self.namespace_client_impl = namespace_client_impl
        self.namespace_client_properties = namespace_client_properties
        self.table_id = table_id
        self.storage_options = storage_options
        self.session_root_subdir = session_root_subdir

        # Lazy-initialized runtime state (avoid getting this pickled)
        self._session: Optional[LanceFileSession] = None

    def __getstate__(self) -> dict:
        """Exclude unpicklable session from pickle."""
        return {
            "root": self.root,
            "namespace_client_impl": self.namespace_client_impl,
            "namespace_client_properties": self.namespace_client_properties,
            "table_id": self.table_id,
            "storage_options": self.storage_options,
            "session_root_subdir": self.session_root_subdir,
        }

    def __setstate__(self, state: dict) -> None:
        """Restore state from pickle, leaving session uninitialized."""
        self.root = state["root"]
        self.namespace_client = None
        self.namespace_client_impl = state.get("namespace_client_impl")
        self.namespace_client_properties = state.get("namespace_client_properties")
        self.table_id = state.get("table_id")
        self.storage_options = state.get("storage_options")
        self.session_root_subdir = state.get("session_root_subdir")
        self._session = None

    def _resolve_namespace_client(self) -> Optional["LanceNamespace"]:
        """Resolve namespace client from pre-built instance or impl/properties."""
        if self.namespace_client is not None:
            return self.namespace_client
        if (
            self.namespace_client_impl is not None
            and self.namespace_client_properties is not None
        ):
            from lance_namespace import connect as namespace_connect

            from geneva.db import WORKER_URI_KEY

            props = dict(self.namespace_client_properties)
            if WORKER_URI_KEY in props:
                worker_uri = props.pop(WORKER_URI_KEY)
                props["uri"] = worker_uri
            return namespace_connect(self.namespace_client_impl, props)
        return None

    @property
    def session(self) -> "LanceFileSession":
        """Lazily create LanceFileSession on first access."""
        if self._session is None:
            ns_client = self._resolve_namespace_client()
            if ns_client and self.table_id:
                # Use dataset's file session for proper credential handling
                from geneva.db import open_lance_dataset

                ds = open_lance_dataset(
                    table_id=self.table_id,
                    namespace_client=ns_client,
                    storage_options=self.storage_options,
                )
                session = ds.new_file_session()
                assert session is not None
                self._session = session
            else:
                # Fallback for non-namespace tables
                self._session = LanceFileSession(
                    self.root, storage_options=self.storage_options
                )
        assert self._session is not None
        return self._session

    def _make_path(self, key: str) -> str:
        """Make the full path for a checkpoint key."""
        if self._uses_namespace_session():
            # Session is rooted at the dataset dir; include the configured
            # per-table checkpoint subdir from ``self.root``.
            return f"{self._session_root_subdir()}/{key}.lance"
        return f"{key}.lance"

    def _uses_namespace_session(self) -> bool:
        return self.table_id is not None and (
            self.namespace_client is not None
            or (
                self.namespace_client_impl is not None
                and self.namespace_client_properties is not None
            )
        )

    def _session_root_subdir(self) -> str:
        """Return the checkpoint subdir used in dataset-relative session paths."""
        if not self._uses_namespace_session():
            return self._CKP_SUBDIR
        if self.session_root_subdir:
            return self.session_root_subdir.strip("/") or self._CKP_SUBDIR
        root = self.root.rstrip("/")
        if not root:
            return self._CKP_SUBDIR
        return root.rsplit("/", 1)[-1] or self._CKP_SUBDIR

    @retry_lance
    def __contains__(self, key: str) -> bool:
        _LOG.debug("contains: %s", key)
        return self.session.contains(self._make_path(key))

    @retry_lance
    def __getitem__(self, key: str) -> pa.RecordBatch:
        _LOG.debug("get: %s", key)
        path = self._make_path(key)
        try:
            reader = self.session.open_reader(path)
            table = reader.read_all().to_table().combine_chunks()
            batches = table.to_batches()
            # A 0-row checkpoint (e.g. an all-unmatched partition under deferred
            # carry-forward) has no batches; synthesize an empty one that still
            # carries the schema so callers don't IndexError.
            batch = (
                batches[0]
                if batches
                else pa.RecordBatch.from_arrays(
                    [pa.array([], type=field.type) for field in table.schema],
                    schema=table.schema,
                )
            )
        except OSError as exc:
            if not self.session.contains(path):
                raise KeyError(key) from exc
            raise
        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException as exc:  # noqa: BLE001
            # A poison checkpoint can panic in Lance's Rust reader (a BaseException,
            # not Exception). Convert it to a non-retryable, attributable error so
            # the FragmentWriter isolates this fragment rather than the panic killing
            # the worker and Ray crash-looping on the same file. Genuine transient IO
            # errors (OSError/ValueError) are re-raised for @retry_lance to retry.
            if _is_lance_reader_panic(exc):
                raise CorruptCheckpointError(
                    key,
                    path=self._full_uri(path),
                    cause=f"{type(exc).__name__}: {exc}",
                ) from exc
            raise
        # Restore blob encoding stripped on write, so callers (and the fragment
        # writer that derives the committed schema from this batch) see the
        # original ``lance-encoding:blob`` metadata.
        batch = _swap_batch_blob_marker(batch, _WAS_BLOB_KEY, _BLOB_ENCODING_KEY)
        return _restore_batch_blob_v2_extensions(batch)

    @retry_lance
    def __setitem__(self, key: str, value: pa.RecordBatch) -> None:
        _LOG.debug("set: %s", key)
        path = self._make_path(key)
        version = _batch_lance_file_version(value)
        # Store blob columns with ordinary encoding to avoid the nullable-blob
        # reader panic; __getitem__ restores the metadata on read.
        value = _swap_batch_blob_marker(value, _BLOB_ENCODING_KEY, _WAS_BLOB_KEY)
        value = _strip_batch_blob_v2_extensions(value)
        with self.session.open_writer(
            path,
            schema=value.schema,
            version=version,
        ) as writer:
            writer.write_batch(value)

    def delete(self, key: str) -> None:
        _LOG.debug("delete: %s", key)
        if key not in self:
            raise KeyError(key)
        self._purge_one(self._make_path(key))

    def _full_uri(self, session_rel_path: str) -> str:
        """Join a session-relative path to ``self.root``.

        Strips the configured checkpoint subdir prefix so namespace-session
        paths (which carry the prefix) don't double it against ``self.root``.
        """
        rel = session_rel_path
        prefix = f"{self._session_root_subdir()}/"
        if rel.startswith(prefix):
            rel = rel[len(prefix) :]
        return f"{self.root}/{rel}"

    def _purge_one(self, session_rel_path: str) -> None:
        """Physically remove a single checkpoint entry, tolerating a missing one.

        Routes the delete through the object_store session (``delete_file``),
        which talks to the blob endpoint only — no Azure hierarchical-namespace
        (DFS) probe — so cleanup succeeds on flat-namespace / unreachable-dfs
        accounts where the old PyArrow ``delete_dir``/``delete_file`` chain
        degraded to a no-op (GEN-658). ``delete_file`` raises ``OSError`` when
        the entry is absent; cleanup is best-effort, so that is swallowed.
        """
        try:
            self.session.delete_file(session_rel_path)
        except (FileNotFoundError, OSError):
            _LOG.debug(
                "purge: nothing to remove at %s", session_rel_path, exc_info=True
            )

    def _purge_paths_parallel(self, session_rel_paths: list[str]) -> None:
        """Hard-delete many session-relative paths through the object_store session.

        Fans the per-path ``delete_file`` calls out over a thread pool:
        ``LanceFileSession`` releases the GIL during the blob round-trip, so
        threads let the object-store calls overlap. The session is reused across
        the batch, so credential / connection setup amortizes once (GEN-554),
        and every delete is blob-only — no HNS probe (GEN-658). Paths are
        already session-relative (``_make_path`` output), so the same routine
        serves both the flat and hierarchical layouts.
        """
        if not session_rel_paths:
            return
        max_workers = min(
            len(session_rel_paths),
            _purge_many_max_workers(self._PURGE_MANY_MAX_WORKERS),
        )
        # Single-path: skip pool overhead for the common ``purge(key)`` shape.
        if max_workers <= 1:
            for p in session_rel_paths:
                self._purge_one(p)
            return
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            # Exhaust the iterator so any unexpected raise inside the worker
            # surfaces here (``_purge_one`` swallows the expected misses).
            for _ in pool.map(self._purge_one, session_rel_paths):
                pass

    def purge_many(self, keys: list[str]) -> None:
        """Bulk hard-delete many checkpoints with parallel object-store calls.

        Each key's data entry is deleted. Missing entries are silently skipped
        (no per-key existence probe, no ``KeyError``). The deletes run against a
        single resolved filesystem so credential / connection-pool setup
        amortizes across the whole batch — see GEN-554 for the commit-hot-path
        motivation.
        """
        if not keys:
            return
        paths = [self._make_path(key) for key in keys]
        self._purge_paths_parallel(paths)

    @retry_lance
    def list_keys(self, prefix: str = "") -> Iterator[str]:
        _LOG.debug("list_keys: %s", prefix)
        # LanceFileSession.list() lists by path prefix, not by filename prefix.
        # Since checkpoint keys are stored as flat files (no '/' separators by
        # convention), we list all keys and filter by string prefix here.
        list_prefix = (
            self._session_root_subdir() if self._uses_namespace_session() else None
        )
        files = timed_list(
            self.session,
            list_prefix,
            op="list_keys",
            layout=self._LAYOUT_LABEL,
            root=self.root,
        )
        for file_path in files:
            if not file_path.endswith(".lance"):
                continue
            # Remove _ckp/ prefix if using namespace session
            if self._uses_namespace_session() and file_path.startswith(
                f"{self._session_root_subdir()}/"
            ):
                file_path = file_path[len(self._session_root_subdir()) + 1 :]
            key = file_path.removesuffix(".lance")
            if prefix and not key.startswith(prefix):
                continue
            yield key

    def uri(self) -> str:
        return self.root


class CheckpointRootMixedLayoutError(RuntimeError):
    """Raised when a checkpoint root mixes flat and hierarchical layouts."""


# Parses the trailing ``_frag-{N}[_range-{S}-{E}]`` portion of a checkpoint key.
_FLAT_KEY_FRAG_RE = re.compile(
    r"^(?P<prefix>.+?)_frag-(?P<frag>\d+)"
    r"(?:_range-(?P<start>\d+)-(?P<end>\d+))?$"
)
# Extracts the uri-hash segment from the identity prefix.
_FLAT_KEY_URI_RE = re.compile(r"_uri-(?P<uri>[0-9a-f]+)")
_FLAT_KEY_IDENTITY_RE = re.compile(
    r"^(?P<bf>.+)_uri-(?P<uri>[0-9a-f]+)(?:_srcfiles-(?P<srcfiles>[^_]+))?$"
)
# Parses the suffix remaining after splitting a list/delete prefix on the
# rightmost ``_frag-``. This intentionally only accepts terminal fragment
# prefixes, rejecting identity text such as ``_frag-1_range-x_ver-...``.
_FLAT_KEY_FRAG_SUFFIX_PREFIX_RE = re.compile(
    r"^(?P<frag>\d+)(?P<range_suffix>_range-(?:\d+(?:-\d*)?)?)?$"
)
_HIER_SOURCE_LEAF_RE = re.compile(r"^(?P<frag>\d+)_src-(?P<srcfiles>[^/]+)$")
_HIER_LEGACY_LEAF_RE = re.compile(r"^(?P<frag>\d+)$")


def _parse_flat_key(key: str) -> tuple[str, str, int, Optional[int], Optional[int]]:
    """Parse a flat (public) checkpoint key into its identity + frag/range parts.

    Used by ``HierarchicalLanceCheckpointStore`` to resolve a public key
    string to a hierarchical path. Returns
    ``(identity_prefix, uri_hash, frag_id, range_start, range_end)``.
    Raises ``ValueError`` if the key does not match the expected
    ``udf-...frag-N[_range-S-E]`` shape (UDTF keys are not supported).
    """
    m = _FLAT_KEY_FRAG_RE.match(key)
    if not m:
        raise ValueError(f"unrecognized checkpoint key: {key!r}")
    prefix = m.group("prefix")
    uri_m = _FLAT_KEY_URI_RE.search(prefix)
    if not uri_m:
        raise ValueError(f"no uri-hash segment in checkpoint key: {key!r}")
    frag = int(m.group("frag"))
    start = int(m.group("start")) if m.group("start") else None
    end = int(m.group("end")) if m.group("end") else None
    return prefix, uri_m.group("uri"), frag, start, end


def _split_hierarchical_identity(prefix: str) -> tuple[str, str, Optional[str]]:
    """Return (bf identity, key reconstruction prefix, srcfiles hash)."""
    m = _FLAT_KEY_IDENTITY_RE.match(prefix)
    if m is None:
        return prefix, prefix, None
    bf_prefix = m.group("bf")
    key_prefix = f"{bf_prefix}_uri-{m.group('uri')}"
    return bf_prefix, key_prefix, m.group("srcfiles")


def _fragment_shard(frag_id: int) -> str:
    """Two-hex shard token for target hierarchical fragment/range paths."""
    return hash_string(str(frag_id))[:2]


def _join_path(*parts: str) -> str:
    return "/".join(part for part in parts if part)


_CHUNKER_GENERIC_KEY_RE = re.compile(
    r"^chunker_[^/]+_src-\d+_rowids-\d+-\d+(?:_fragment)?$"
)
_UDTF_GENERIC_KEY_RE = re.compile(
    r"^udtf_[^/]+_src-\d+_(?:__all__|[^/]+=.+)_(?:batch-\d+|fragment)$"
)


def _is_generic_checkpoint_key(key: str) -> bool:
    return bool(_CHUNKER_GENERIC_KEY_RE.match(key) or _UDTF_GENERIC_KEY_RE.match(key))


def _is_generic_checkpoint_prefix(prefix: str) -> bool:
    return prefix.startswith(("chunker_", "udtf_"))


class HierarchicalLanceCheckpointStore(FlatLanceCheckpointStore):
    """Content-identity hierarchical layout for the checkpoint store.

    Paths follow::

        {root}/_ckpv2/bf={identity_hash}/
            fragments/fs={shard}/{N}_src-{srcfiles_hash}.lance
            ranges/fs={shard}/{N}_src-{srcfiles_hash}/{S}-{E}.lance
            _identity.json
            _jobs/{job_id}.lance        # written by completion handler

    where ``identity_hash`` is the md5 of the backfill identity prefix before
    the table URI and per-fragment ``_srcfiles-...`` suffix. Two invocations
    of the same backfill (same udf, version, column, where) share a
    bf-directory so retries reuse the previous attempt's checkpoints. The
    per-fragment source-file identity rides on the fragment/range leaf. See
    ``internal_docs/checkpoint-layout-v2.md`` for the full design.

    The public key string is unchanged on the wire — callers continue to use
    the format ``udf-{n}_ver-{v}_col-{c}_where-{H}_uri-{U}_srcfiles-{S}_frag-{N}
    [_range-{S2}-{E}]``. UDTF keys are not supported and raise ``ValueError``.

    The store refuses to open a root that already contains a flat layout.
    """

    _LAYOUT_LABEL = "hierarchical"

    # Target hierarchical checkpoint root under the table location.
    DEFAULT_TABLE_SUBDIR = "_ckpv2"

    _IDENTITY_FILE = "_identity.json"
    _JOBS_SUBDIR = "_jobs"
    _GENERIC_KEYS_SUBDIR = "_keys"
    _IDENTITY_SCHEMA_VERSION = 1

    def __init__(
        self,
        root: str,
        namespace_client: Optional["LanceNamespace"] = None,
        namespace_client_impl: Optional[str] = None,
        namespace_client_properties: Optional[dict[str, str]] = None,
        table_id: Optional[list[str]] = None,
        storage_options: Optional[dict[str, str]] = None,
        session_root_subdir: Optional[str] = None,
        write_identity_sidecar: bool = True,
    ) -> None:
        super().__init__(
            root,
            namespace_client=namespace_client,
            namespace_client_impl=namespace_client_impl,
            namespace_client_properties=namespace_client_properties,
            table_id=table_id,
            storage_options=storage_options,
            session_root_subdir=session_root_subdir,
        )
        self.write_identity_sidecar = write_identity_sidecar
        # Process-local cache: bf_dir -> identity prefix when present, or
        # None to remember that no _identity.json sidecar exists.
        # Negative caching is load-bearing on the list_keys hot path
        # (see _read_identity). plan_read runs once per backfill at
        # coarse intervals, so a stale None within a single driver
        # lifetime would at worst cost one backfill's re-do; not worth
        # the complexity of a TTL.
        self._identity_cache: dict[str, Optional[str]] = {}
        # Process-local set of bf-dirs known to have an _identity.json on disk.
        self._identity_written: set[str] = set()
        # Latch the coexistence-with-flat check so we only LIST the root once.
        self._coexistence_checked = False
        self._coexistence_lock = threading.Lock()

    def __getstate__(self) -> dict:
        state = super().__getstate__()
        state["write_identity_sidecar"] = self.write_identity_sidecar
        return state

    def __setstate__(self, state: dict) -> None:
        super().__setstate__(state)
        self.write_identity_sidecar = state.get("write_identity_sidecar", True)
        self._identity_cache = {}
        self._identity_written = set()
        self._coexistence_checked = False
        self._coexistence_lock = threading.Lock()

    # ------------------------------------------------------------------ paths

    def _ckp_root(self) -> str:
        """Return the namespace-session prefix for the target checkpoint root."""
        if self._uses_namespace_session():
            return self._session_root_subdir()
        return ""

    def _bf_dir(self, uri_hash: str, bf_hash: str) -> str:
        """Return the bf-directory path, including the namespace prefix."""
        _ = uri_hash  # table identity is pinned by the surrounding table root.
        return _join_path(self._ckp_root(), f"bf={bf_hash}")

    def _make_path(self, key: str) -> str:
        """Resolve a flat checkpoint key to its hierarchical path."""
        try:
            prefix, uri_hash, frag, start, end = _parse_flat_key(key)
        except ValueError:
            if not _is_generic_checkpoint_key(key):
                raise
            return _join_path(
                self._ckp_root(), self._GENERIC_KEYS_SUBDIR, f"{key}.lance"
            )
        bf_prefix, _, srcfiles_hash = _split_hierarchical_identity(prefix)
        bf_hash = hash_string(bf_prefix)
        base = self._bf_dir(uri_hash, bf_hash)
        shard = f"fs={_fragment_shard(frag)}"
        fragment_identity = (
            f"{frag}_src-{srcfiles_hash}" if srcfiles_hash is not None else str(frag)
        )
        if start is None:
            return f"{base}/fragments/{shard}/{fragment_identity}.lance"
        return f"{base}/ranges/{shard}/{fragment_identity}/{start}-{end}.lance"

    def _strip_checkpoint_root_prefix(self, session_rel_path: str) -> str:
        rel = session_rel_path
        prefix = f"{self._session_root_subdir()}/"
        if rel.startswith(prefix):
            rel = rel[len(prefix) :]
        return rel

    def _full_uri(self, session_rel_path: str) -> str:
        rel = self._strip_checkpoint_root_prefix(session_rel_path)
        return f"{self.root}/{rel}" if rel else self.root

    # ``_purge_paths_parallel`` is inherited from the base store: its
    # ``delete_file`` calls take the session-relative paths ``_make_path``
    # already produces for the hierarchical layout, so no fs-path translation
    # is needed.

    # --------------------------------------------------------------- identity

    def _cache_identity_if_absent(self, bf_dir: str, prefix: str) -> None:
        """Fill empty or negative identity cache entries without overwriting."""
        if self._identity_cache.get(bf_dir) is None:
            self._identity_cache[bf_dir] = prefix

    def ensure_identity_sidecar(
        self, checkpoint_prefix: str, *, required: bool = True
    ) -> None:
        """Ensure the bf-directory identity sidecar exists for a checkpoint prefix."""
        uri_m = _FLAT_KEY_URI_RE.search(checkpoint_prefix)
        if uri_m is None:
            if required:
                raise ValueError(
                    "checkpoint prefix must include a _uri- hash segment: "
                    f"{checkpoint_prefix!r}"
                )
            return

        self._check_coexistence_with_flat()
        bf_prefix, key_prefix, _ = _split_hierarchical_identity(checkpoint_prefix)
        bf_dir = self._bf_dir(uri_m.group("uri"), hash_string(bf_prefix))
        self._cache_identity_if_absent(bf_dir, key_prefix)
        self._write_identity_if_missing(bf_dir, key_prefix, raise_on_error=required)

    def _write_identity_if_missing(
        self, bf_dir: str, prefix: str, *, raise_on_error: bool = False
    ) -> None:
        """Write the human-readable identity sidecar once per bf-directory.

        Idempotent across concurrent writers: content is deterministic from
        the identity prefix, so last-write-wins is safe on stores without
        atomic rename. Routes through the Lance ``object_store`` session — the
        same path the checkpoint data uses — rather than PyArrow's filesystem,
        so the write never probes the Azure hierarchical-namespace endpoint
        (``dfs.core.windows.net``) and succeeds on flat-namespace accounts
        where only the blob endpoint is reachable (GEN-645).
        """
        if bf_dir in self._identity_written:
            return
        rel_path = f"{bf_dir}/{self._IDENTITY_FILE}"
        try:
            if self.session.contains(rel_path):
                self._identity_written.add(bf_dir)
                return
        except (OSError, RuntimeError, ValueError):
            # The existence check is only an optimization. A failure here
            # (object_store surfaces these as OSError/RuntimeError/ValueError)
            # must not abort the write; fall through to the idempotent upload,
            # which is authoritative and raises on a genuine problem.
            pass
        payload = json.dumps(
            {
                "prefix": prefix,
                "schema_version": self._IDENTITY_SCHEMA_VERSION,
            }
        ).encode()
        try:
            self._upload_identity_payload(rel_path, payload)
            self._identity_written.add(bf_dir)
        except OSError:
            if raise_on_error:
                raise
            _LOG.debug("identity sidecar write failed for %s", rel_path, exc_info=True)

    def _upload_identity_payload(self, rel_path: str, payload: bytes) -> None:
        """Upload sidecar bytes through the object-store session (blob-only).

        ``LanceFileSession`` only exposes file-to-file transfer, so the bytes
        round-trip through a temporary local file. The session talks to the
        blob endpoint exclusively, so no hierarchical-namespace probe occurs.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            local = os.path.join(tmp_dir, self._IDENTITY_FILE)
            with open(local, "wb") as f:
                f.write(payload)
            self.session.upload_file(local, rel_path)

    def has_udf_version_mismatch(self, column: str, current_udf_version: str) -> bool:
        """Fast path for the hierarchical layout: the version token is in
        the bf-identity prefix, so we only need to verify that a matching
        bf-directory has at least one fragment-level checkpoint before
        comparing the identity version. Range-only per-batch checkpoints
        are ignored.
        """
        for bf_hash, identity in self.iter_bf_identities():
            if _checkpoint_identity_prefix_for_column(identity, column) is None:
                continue
            if not any(self._iter_fragment_leaf_names(bf_hash)):
                continue
            stored_version = _parse_udf_version_from_checkpoint_identity(
                identity, column
            )
            if stored_version is None:
                # Identity for this column with no parseable ``_ver-``
                # token — assume mismatch so the caller reprocesses.
                return True
            if stored_version != current_udf_version:
                return True
        return False

    def _iter_fragment_leaf_names(self, bf_hash: str) -> Iterator[str]:
        """Yield fragment-level leaf names under one bf= directory."""
        scope = _join_path(self._ckp_root(), f"bf={bf_hash}", "fragments")
        try:
            paths = timed_list(
                self.session,
                scope,
                op="list_fragment_leaves",
                layout=self._LAYOUT_LABEL,
                root=self.root,
            )
        except (FileNotFoundError, OSError):
            _LOG.debug("fragment leaf list failed for %s", scope, exc_info=True)
            return
        for path in paths:
            if path.endswith(".lance"):
                yield path.rsplit("/", 1)[-1].removesuffix(".lance")

    def has_srcfiles_hash_mismatch(
        self, column: str, current_srcfiles_hash: str
    ) -> bool:
        """Fast path for the hierarchical layout: list only the
        ``bf=H/fragments/`` subtree of each matching backfill and parse
        the srcfiles hash out of the leaf filename, skipping the
        ``bf=H/ranges/`` subtree (in-flight per-batch checkpoints that
        the existing code already filtered out post-LIST). The LIST is
        bounded by one backfill's fragment count, never by total batch
        activity (GEN-614).
        """
        col_pattern = re.compile(rf"_col-{re.escape(column)}_")
        existing_hashes: set[str] = set()
        for bf_hash, identity in self.iter_bf_identities():
            if not col_pattern.search(identity):
                continue
            for srcfiles in self._iter_fragment_srcfiles(bf_hash):
                existing_hashes.add(srcfiles)
        if not existing_hashes:
            return False
        return current_srcfiles_hash not in existing_hashes

    def _iter_fragment_srcfiles(self, bf_hash: str) -> Iterator[str]:
        """Yield srcfiles hashes from fragment-level leaves under one bf=
        dir. LIST is scoped to ``bf=H/fragments/`` only — the ``ranges/``
        subtree (per-batch checkpoints, in-flight) is skipped entirely.
        Hashes come from the ``{frag}_src-{hash}.lance`` leaf names, so
        no checkpoint payloads are read.
        """
        for leaf in self._iter_fragment_leaf_names(bf_hash):
            m = _HIER_SOURCE_LEAF_RE.match(leaf)
            if m is not None:
                yield m.group("srcfiles")

    def iter_bf_identities(self) -> Iterator[tuple[str, str]]:
        """Yield ``(bf_hash, identity_prefix)`` for every ``bf=*/`` subdir
        whose ``_identity.json`` is parseable.

        Enumerates the ``bf=`` subdirs, then reads each subdir's
        ``_identity.json`` once (cached via ``_read_identity``). Lets
        mismatch-detection callers scope per-column work to the few
        bf-directories that match a column.
        """
        for leaf in self._list_bf_dir_leaves():
            bf_hash = leaf[len("bf=") :]
            bf_dir = _join_path(self._ckp_root(), leaf)
            identity = self._read_identity(bf_dir)
            if identity is None:
                continue
            yield bf_hash, identity

    def _list_bf_dir_leaves(self) -> list[str]:
        """List the immediate ``bf=`` directory names under the checkpoint root.

        A single non-recursive, delimited LIST through the object_store session
        returns just the immediate child prefixes, bounding the listing by
        backfill count rather than total checkpoint count, which can reach 100K+
        on tables with many fragments (GEN-614). The session talks to the blob
        endpoint only, so it needs no Azure hierarchical-namespace (DFS)
        endpoint and works uniformly on flat-namespace / unreachable-dfs
        accounts — no PyArrow selector, no HNS probe, no recursive fallback
        (GEN-645/GEN-661).
        """
        scope = self._ckp_root() or None
        try:
            result = timed_list_with_delimiter(
                self.session,
                scope,
                op="iter_bf_identities",
                layout=self._LAYOUT_LABEL,
                root=self.root,
            )
        except (FileNotFoundError, OSError):
            return []
        # ``common_prefixes`` are the immediate child dirs, session-relative
        # (e.g. ``_ckpv2/bf=H`` in namespace mode); keep only the ``bf=`` leaves.
        leaves = {
            leaf
            for prefix in result.common_prefixes
            if (leaf := prefix.rstrip("/").rsplit("/", 1)[-1]).startswith("bf=")
        }
        return sorted(leaves)

    def _read_identity(self, bf_dir: str) -> Optional[str]:
        """Read the identity prefix for a bf-directory; cached after first
        read (including negative results).

        Caching the absence is load-bearing: ``list_keys`` calls
        ``_path_to_key`` once per path, and ``_path_to_key`` calls back
        here once per path. When a ``bf=`` dir's ``_identity.json`` is
        missing (in-progress backfill whose sidecar hasn't been
        written, or a directory abandoned mid-write), an uncached
        negative makes every one of the dir's 100K+ paths trigger a
        fresh Azure GET that returns 404 -- the coordinator's resume
        flow then looks indistinguishable from being stuck reading the
        same file forever, because it is.

        A partially-written or corrupt sidecar (truncated JSON, bad
        UTF-8, or a non-object payload from a writer that crashed
        mid-write) is treated the same as absent: the read raises
        ``ValueError``/``AttributeError`` rather than ``OSError``, so we
        catch those too and negatively cache, instead of re-raising and
        reintroducing the hang on every path in the dir.
        """
        if bf_dir in self._identity_cache:
            return self._identity_cache[bf_dir]
        rel_path = f"{bf_dir}/{self._IDENTITY_FILE}"
        prefix: Optional[str] = None
        try:
            payload = json.loads(self._download_identity_payload(rel_path).decode())
            candidate = payload.get("prefix")
            if isinstance(candidate, str):
                prefix = candidate
        except (FileNotFoundError, OSError, ValueError, AttributeError):
            prefix = None
        self._identity_cache[bf_dir] = prefix
        return prefix

    def _download_identity_payload(self, rel_path: str) -> bytes:
        """Download sidecar bytes through the object-store session (blob-only).

        Routes through the Lance ``object_store`` session rather than PyArrow's
        filesystem, so the read never probes the Azure hierarchical-namespace
        endpoint (GEN-645). Raises ``OSError`` when the sidecar is absent, which
        ``_read_identity`` treats as a negative result (the negative-caching
        contract from GEN-615).
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            local = os.path.join(tmp_dir, self._IDENTITY_FILE)
            self.session.download_file(rel_path, local)
            with open(local, "rb") as f:
                return f.read()

    # ----------------------------------------------------------- coexistence

    def _check_coexistence_with_flat(self) -> None:
        """Refuse to operate against a root that already has flat-layout keys."""
        if self._coexistence_checked:
            return
        with self._coexistence_lock:
            if self._coexistence_checked:
                return
            list_prefix = self._ckp_root() or None
            try:
                entries = timed_list(
                    self.session,
                    list_prefix,
                    op="coexistence_check",
                    layout=self._LAYOUT_LABEL,
                    root=self.root,
                )
            except Exception:
                # Empty / nonexistent root is fine; nothing to coexist with.
                self._coexistence_checked = True
                return
            for entry in entries:
                if not entry.endswith(".lance"):
                    continue
                rel = self._strip_checkpoint_root_prefix(entry)
                # Target hierarchical entries live under bf=...; generic keys
                # (for example chunker work-item checkpoints) live under _keys/.
                if rel.startswith(("bf=", f"{self._GENERIC_KEYS_SUBDIR}/")):
                    continue
                raise CheckpointRootMixedLayoutError(
                    f"checkpoint root {self.root!r} contains a flat-layout "
                    f"entry {rel!r}; refusing to mix layouts. Point the "
                    "hierarchical store at a fresh root or remove the "
                    "existing flat-layout checkpoints."
                )
            self._coexistence_checked = True

    # ------------------------------------------------------- store interface

    @retry_lance
    def __setitem__(self, key: str, value: pa.RecordBatch) -> None:
        self._check_coexistence_with_flat()
        try:
            prefix, uri_hash, _, _, _ = _parse_flat_key(key)
        except ValueError:
            if not _is_generic_checkpoint_key(key):
                raise
            super().__setitem__(key, value)
            return
        bf_prefix, key_prefix, _ = _split_hierarchical_identity(prefix)
        bf_hash = hash_string(bf_prefix)
        bf_dir = self._bf_dir(uri_hash, bf_hash)
        self._cache_identity_if_absent(bf_dir, key_prefix)
        super().__setitem__(key, value)
        # Best-effort sidecar write; not critical for the hot path.
        if self.write_identity_sidecar:
            self._write_identity_if_missing(bf_dir, key_prefix)

    @retry_lance
    def list_keys(self, prefix: str = "") -> Iterator[str]:
        """Enumerate checkpoint keys, optionally filtered by a flat-key prefix.

        When *prefix* matches a known backfill identity, the listing is scoped
        to a single ``bf=`` directory and bounded by one backfill's worth of
        checkpoints. When *prefix* is empty, the checkpoint root is walked.
        """
        _LOG.debug("hierarchical list_keys: %s", prefix)
        scope = self._scope_for_prefix(prefix)
        files = timed_list(
            self.session,
            scope,
            op="list_keys",
            layout=self._LAYOUT_LABEL,
            root=self.root,
        )
        for path in files:
            key = self._path_to_key(path)
            if key is None:
                continue
            if prefix and not key.startswith(prefix):
                continue
            yield key

    def _scope_for_prefix(self, prefix: str) -> str | None:
        """Pick the narrowest LIST scope that still covers ``prefix``."""
        if not prefix:
            return self._ckp_root() or None
        if _is_generic_checkpoint_prefix(prefix):
            return _join_path(self._ckp_root(), self._GENERIC_KEYS_SUBDIR)
        # If the prefix already includes the uri hash, narrow by bf=.
        uri_m = _FLAT_KEY_URI_RE.search(prefix)
        if not uri_m:
            return self._ckp_root() or None
        uri_hash = uri_m.group("uri")
        # Parse the fragment suffix from the right because the user-controlled
        # identity prefix may itself contain `_frag-`.
        #
        # ReadTask probe:
        #   ..._srcfiles-cc_frag-0_range- -> identity ..._srcfiles-cc,
        #   suffix 0_range-, scope .../bf={hash}/ranges/fs=K/0_src-cc.
        # Identity text containing `_frag-`:
        #   ...udf-test_frag-x..._srcfiles-cc_frag-0_range-
        #   must split on the final `_frag-`, not the one in the identity.
        frag_suffix_m: re.Match[str] | None = None
        identity_prefix = prefix
        before_frag, sep, after_frag = prefix.rpartition("_frag-")
        if sep:
            frag_suffix_m = _FLAT_KEY_FRAG_SUFFIX_PREFIX_RE.match(after_frag)
        if frag_suffix_m is not None:
            identity_prefix = before_frag
        bf_prefix, _, srcfiles_hash = _split_hierarchical_identity(identity_prefix)
        bf_hash = hash_string(bf_prefix)
        bf_dir = self._bf_dir(uri_hash, bf_hash)
        if frag_suffix_m is not None and frag_suffix_m.group("range_suffix"):
            frag = int(frag_suffix_m.group("frag"))
            shard = f"fs={_fragment_shard(frag)}"
            if srcfiles_hash is not None:
                fragment_identity = f"{frag}_src-{srcfiles_hash}"
            else:
                fragment_identity = str(frag)
            return f"{bf_dir}/ranges/{shard}/{fragment_identity}"
        return bf_dir

    def _path_to_key(self, path: str) -> Optional[str]:
        """Reconstruct a flat checkpoint key from a hierarchical path; None to skip."""
        if not path.endswith(".lance"):
            return None
        rel = path
        rel = self._strip_checkpoint_root_prefix(rel)
        # rel = bf=H/{fragments,ranges}/fs=K/...
        parts = rel.split("/")
        if (
            len(parts) == 2
            and parts[0] == self._GENERIC_KEYS_SUBDIR
            and parts[1].endswith(".lance")
        ):
            key = parts[1].removesuffix(".lance")
            return key if _is_generic_checkpoint_key(key) else None
        # Skip _jobs manifests when reconstructing keys.
        if len(parts) < 4 or any(p.startswith("_jobs") for p in parts):
            return None
        if not parts[0].startswith("bf="):
            return None
        bf_dir = _join_path(self._ckp_root(), parts[0])
        identity_prefix = self._read_identity(bf_dir)
        if identity_prefix is None:
            # Identity sidecar missing — cannot reconstruct the flat key.
            return None
        kind = parts[1]
        leaf = parts[-1].removesuffix(".lance")
        if kind == "fragments" and len(parts) == 4 and parts[2].startswith("fs="):
            m = _HIER_SOURCE_LEAF_RE.match(leaf)
            if m is not None:
                return (
                    f"{identity_prefix}_srcfiles-{m.group('srcfiles')}"
                    f"_frag-{m.group('frag')}"
                )
            m = _HIER_LEGACY_LEAF_RE.match(leaf)
            if m is not None:
                return f"{identity_prefix}_frag-{m.group('frag')}"
        if kind == "ranges" and len(parts) == 5 and parts[2].startswith("fs="):
            m = _HIER_SOURCE_LEAF_RE.match(parts[3])
            if m is not None:
                return (
                    f"{identity_prefix}_srcfiles-{m.group('srcfiles')}"
                    f"_frag-{m.group('frag')}_range-{leaf}"
                )
            m = _HIER_LEGACY_LEAF_RE.match(parts[3])
            if m is not None:
                return f"{identity_prefix}_frag-{m.group('frag')}_range-{leaf}"
        return None

    # ``delete`` and ``delete_prefix`` are inherited from the base store
    # (physical delete); the scoped hierarchical ``list_keys`` keeps
    # ``delete_prefix`` bounded to one ``bf=`` subtree.


class CheckpointMode(Enum):
    OBJECT_STORE = "object_store"

    # Store checkpoints in temporary files, for local development
    # and testing.
    # It can be shared between process, i.e., local ray actors.
    TEMPFILE = "tempfile"

    # for testing only
    IN_MEMORY = "in_memory"

    @staticmethod
    def from_str(s: str) -> "CheckpointMode":
        if isinstance(s, CheckpointMode):
            return s
        return CheckpointMode(s)


def _normalize_store_layout(value: str | None) -> str:
    """Coerce a config / env-var string into the canonical layout token.

    Returns one of ``"flat"`` or ``"hierarchical"``.
    """
    if value is None:
        return "flat"
    v = str(value).strip().lower()
    if v in ("flat", "1"):
        return "flat"
    if v in ("hierarchical", "2"):
        return "hierarchical"
    raise ValueError(
        f"unknown checkpoint store_layout {value!r}; expected 'flat' or 'hierarchical'"
    )


@attrs.define
class ObjectStoreCheckpointConfig(ConfigBase):
    path: str

    @classmethod
    def name(cls) -> str:
        return "object_store"

    def make(self) -> CheckpointStore:
        return _apply_checkpoint_wrap(FlatLanceCheckpointStore(self.path))


@attrs.define
class CheckpointConfig(ConfigBase):
    mode: CheckpointMode = attrs.field(
        default=CheckpointMode.OBJECT_STORE, converter=CheckpointMode.from_str
    )

    object_store: ObjectStoreCheckpointConfig | None = attrs.field(default=None)

    # ``"flat"`` (default) selects ``FlatLanceCheckpointStore``;
    # ``"hierarchical"`` selects ``HierarchicalLanceCheckpointStore``. Set
    # via env var ``CHECKPOINT__STORE_LAYOUT`` for opt-in adoption per
    # ``internal_docs/checkpoint-layout-v2.md``.
    store_layout: str = attrs.field(default="flat", converter=_normalize_store_layout)

    # Per-layout default subdir for the per-table checkpoint root, exposed
    # through geneva's standard ``ConfigBase`` env-var pattern
    # (``CHECKPOINT__FLAT_SUBDIR`` / ``CHECKPOINT__HIERARCHICAL_SUBDIR``,
    # matching the existing ``CHECKPOINT__STORE_LAYOUT``). The class
    # constants on the store implementations remain the canonical defaults;
    # these fields just surface them through the config loader so operators
    # can pin the subdir without code changes. ``GENEVA_CHECKPOINT_SUBDIR``
    # (handled in ``TableReference.open_checkpoint_store``) is a blanket
    # override that still wins over both fields for ad-hoc experiments.
    flat_subdir: str = attrs.field(
        default=FlatLanceCheckpointStore.DEFAULT_TABLE_SUBDIR
    )
    hierarchical_subdir: str = attrs.field(
        default=HierarchicalLanceCheckpointStore.DEFAULT_TABLE_SUBDIR
    )

    # When the destination is a multi-base Lance dataset, place each
    # fragment's checkpoints (and staged backfill output files) in the
    # fragment's storage base instead of the table root. Kill switch:
    # ``CHECKPOINT__MULTI_BASE_PLACEMENT=0``. Has no effect on datasets
    # without ``base_paths``.
    multi_base_placement: bool = attrs.field(default=True, converter=str_to_bool)

    @classmethod
    def name(cls) -> str:
        return "checkpoint"

    def _lance_store_cls(self) -> type[FlatLanceCheckpointStore]:
        if self.store_layout == "hierarchical":
            return HierarchicalLanceCheckpointStore
        return FlatLanceCheckpointStore

    def make(self) -> CheckpointStore:
        match self.mode:
            case CheckpointMode.TEMPFILE:
                temp_dir = tempfile.mkdtemp()
                _LOG.info("Create checkpoint store on %s", temp_dir)
                store: CheckpointStore = self._lance_store_cls()(temp_dir)
            case CheckpointMode.OBJECT_STORE:
                if self.object_store is None:
                    raise ValueError("CheckpointConfig::object_store is required")
                store = self._lance_store_cls()(self.object_store.path)
            case CheckpointMode.IN_MEMORY:
                store = InMemoryCheckpointStore()
            case _:
                raise ValueError(f"Unknown checkpoint mode {self.mode}")
        return _apply_checkpoint_wrap(store)
