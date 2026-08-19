# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import contextlib
import enum
import functools
import hashlib
import inspect
import logging
import math
import signal
import threading
import time
import typing
import warnings
from array import array
from collections.abc import Callable, Iterator
from types import CodeType, NoneType, UnionType
from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    ClassVar,
    Generic,
    Optional,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
    get_type_hints,
)

import attrs
import numpy
import pyarrow as pa
from attrs import validators as valid
from lance.blob import BlobFile

import geneva.cloudpickle as pickle
from geneva.checkpoint_utils import format_checkpoint_prefix
from geneva.utils.batch_size import resolve_batch_size
from geneva.utils.schema import (
    parse_field_path,
    resolve_arrow_field_path,
    resolve_projected_field_path,
)

if TYPE_CHECKING:
    from geneva.debug.error_store import ErrorHandlingConfig, ExceptionMatcher
    from geneva.manifest.mgr import GenevaManifest

_LOG = logging.getLogger(__name__)
_ATTRS_FACTORY_TYPE = type(attrs.Factory(lambda: None))

# special column name used to mark the rows that were not selected
# for backfilling.  This is used to avoid calling expensive UDFs
# on rows that are not selected.
BACKFILL_SELECTED = "__geneva_backfill_selected"

_ColumnsT = TypeVar("_ColumnsT")


class _CodeIdentityError(Exception):
    """Raised internally when a callable's code identity cannot be derived."""


def _const_repr(const: Any) -> str:
    """Return a stable textual encoding of a code-object constant.

    ``repr`` is deterministic for the scalar/tuple constants the compiler emits,
    but unordered for ``set``/``frozenset`` literals, so those are sorted first.
    """
    if isinstance(const, (set, frozenset)):
        inner = ",".join(sorted(_const_repr(item) for item in const))
        return f"{type(const).__name__}({{{inner}}})"
    return repr(const)


def _update_code_digest(hasher: Any, code: CodeType) -> None:
    """Fold a code object's bytecode, names, and constants into ``hasher``.

    Nested code objects (inner functions, lambdas, comprehensions) live in
    ``co_consts`` and are recursed into so edits to inner bodies are captured.
    """
    hasher.update(code.co_code)
    hasher.update(repr(code.co_names).encode())
    hasher.update(repr(code.co_varnames).encode())
    for const in code.co_consts:
        if isinstance(const, CodeType):
            hasher.update(b"<code>")
            _update_code_digest(hasher, const)
        else:
            hasher.update(_const_repr(const).encode())


def _fold_value(hasher: Any, value: Any) -> None:
    """Best-effort deterministic fold of a picklable value into ``hasher``.

    Falls back to a by-reference type marker for values that cannot be pickled,
    so hashing never raises on an unusual bound argument or instance attribute.
    """
    try:
        hasher.update(pickle.dumps(value))
    except Exception:
        hasher.update(f"<byref:{type(value).__name__}>".encode())


def _update_function_digest(hasher: Any, func: Any, seen: set[int]) -> None:
    """Fold a plain function/method's code identity into ``hasher``.

    Combines the code object, ``__qualname__``/``__module__`` for
    disambiguation, and closure cell contents (guarded). ``seen`` tracks the
    ids of callables already folded so self-referential closures (a factory
    returning a function that closes over itself) do not recurse forever.
    Raises ``_CodeIdentityError`` when the callable exposes no code object.
    """
    fid = id(func)
    if fid in seen:
        hasher.update(b"<cycle>")
        return
    seen.add(fid)
    code = getattr(func, "__code__", None)
    if not isinstance(code, CodeType):
        raise _CodeIdentityError
    hasher.update(str(getattr(func, "__qualname__", "")).encode())
    hasher.update(str(getattr(func, "__module__", "")).encode())
    _update_code_digest(hasher, code)
    for cell in getattr(func, "__closure__", None) or ():
        try:
            contents = cell.cell_contents
        except ValueError:
            hasher.update(b"<empty-cell>")
            continue
        if inspect.isfunction(contents):
            with contextlib.suppress(_CodeIdentityError):
                _update_function_digest(hasher, contents, seen)
                continue
        _fold_value(hasher, contents)


def _update_callable_code_digest(hasher: Any, target: Any, seen: set[int]) -> None:
    """Fold a callable's code identity into ``hasher``.

    Unwraps ``functools.partial`` (folding in bound args/keywords) and
    ``functools.wraps``/``__wrapped__`` chains, then digests the code of a plain
    function/method or, for a callable instance, its ``__call__`` method plus
    the instance ``__dict__``. ``seen`` is threaded into the function digest so
    self-referential closures terminate. Raises ``_CodeIdentityError`` when no
    code identity can be derived (e.g. built-in callables).
    """
    if isinstance(target, functools.partial):
        hasher.update(b"<partial>")
        _fold_value(hasher, target.args)
        _fold_value(hasher, tuple(sorted(target.keywords.items())))
        _update_callable_code_digest(hasher, target.func, seen)
        return

    unwrapped = target
    with contextlib.suppress(Exception):
        unwrapped = inspect.unwrap(target)
    if unwrapped is not target:
        _update_callable_code_digest(hasher, unwrapped, seen)
        return

    if inspect.isfunction(target) or inspect.ismethod(target):
        _update_function_digest(hasher, target, seen)
        return

    # Callable instance: hash its __call__ code identity plus instance state.
    call = inspect.getattr_static(type(target), "__call__", None)
    if inspect.isfunction(call):
        _update_function_digest(hasher, call, seen)
        _fold_value(hasher, getattr(target, "__dict__", {}))
        return

    raise _CodeIdentityError


def _func_version_hash(func: Callable) -> str:
    """Hash a callable's code identity for use as an auto-generated version.

    Two complementary digests are folded together so the version changes
    whenever behaviour changes:

    * A code-identity walk of the callable's own code object -- bytecode,
      constants (recursing into nested code objects), names, and closure
      contents. cloudpickle serializes module-importable callables *by
      reference* (module + qualname only), so this walk is what makes an edit
      to a module-defined UDF body change the version.
    * cloudpickle's own by-value bytes, which capture referenced globals,
      bound-instance/``__self__`` state, decorator/wrapper closures, and
      ``__slots__`` values that the code walk alone cannot see. This is
      best-effort: callables that reference unpicklable module-level state
      (e.g. a ``threading.Lock``) simply contribute no by-value bytes.

    Falls back to a by-reference type marker (with a warning) only when neither
    digest can be derived (e.g. an opaque built-in callable).
    """
    hasher = hashlib.md5()
    contributed = False

    # By-value fingerprint: sensitive to closure/instance/global state. Skipped
    # when the callable references unpicklable state (contributed stays False).
    with contextlib.suppress(Exception):
        hasher.update(pickle.dumps(func))
        contributed = True

    # Code-identity walk: sensitive to body edits even under pickle-by-reference.
    with contextlib.suppress(_CodeIdentityError):
        _update_callable_code_digest(hasher, func, set())
        contributed = True

    if not contributed:
        warnings.warn(
            f"Could not resolve a stable version for {func!r}; its "
            "auto-generated version may not change when the code is edited. "
            "Pass an explicit version to guarantee checkpoint invalidation.",
            UserWarning,
            stacklevel=5,
        )
        hasher.update(f"<byref:{type(func).__name__}>".encode())
    return hasher.hexdigest()


class Columns(Generic[_ColumnsT]):
    """Return annotation marker for UDFs that produce multiple columns.

    Annotating a UDF's return type as ``Columns[T]`` declares that the UDF
    emits a struct whose top-level fields are unpacked into sibling table
    columns at ``add_columns`` time. ``T`` must currently be a
    ``NamedTuple``; the framework infers the output struct schema from its
    field type annotations. Other types raise ``ValueError`` at decoration
    time.

    Each top-level struct field becomes its own table column with the same
    name. To attach a ``Columns[T]`` UDF, pass it directly to
    [`Table.add_columns`][geneva.table.Table.add_columns] (not wrapped in a
    dict). The sibling columns share a backfill group and must be
    backfilled and dropped together.

    Supply an explicit ``data_type=pa.struct([...])`` on ``@udf`` when a
    field needs Arrow metadata (e.g. ``lance-encoding:blob``); ``T`` is
    still a ``NamedTuple`` in that case — ``data_type`` only overrides the
    inferred schema, it does not unlock non-``NamedTuple`` ``T``.

    Examples
    --------
    >>> from typing import NamedTuple
    >>> import geneva
    >>> from geneva import udf
    >>>
    >>> class Dimensions(NamedTuple):
    ...     height: int
    ...     width: int
    >>>
    >>> @udf
    ... def dimensions(image_id: int) -> geneva.Columns[Dimensions]:
    ...     return Dimensions(image_id + 10, image_id + 20)
    >>>
    >>> table.add_columns(dimensions)  # adds "height" and "width" columns
    """


def _columns_annotation_inner(annotation: Any) -> Any | None:
    origin = get_origin(annotation)
    if origin is Annotated:
        base, *_ = get_args(annotation)
        return _columns_annotation_inner(base)

    if origin is Columns:
        args = get_args(annotation)
        if len(args) != 1:
            raise ValueError(
                "Columns[...] return annotation requires one type argument"
            )
        return args[0]

    return None


@attrs.define(frozen=True)
class UnpackedUDFField:
    """One top-level struct field unpacked into a sibling table column."""

    struct_field_name: str
    output_column: str
    field: pa.Field


@attrs.define(frozen=True)
class UnpackedUDF:
    """Call-site wrapper that expands a struct-returning UDF into columns."""

    udf: "UDF"
    prefix: str = ""
    fields: tuple[UnpackedUDFField, ...] = attrs.field(init=False)

    def __attrs_post_init__(self) -> None:
        if not pa.types.is_struct(self.udf.data_type):
            raise ValueError("Columns[...] UDF requires a struct output data_type")
        if not isinstance(self.prefix, str):
            raise TypeError("Columns[...] UDF prefix must be a string")
        if self.prefix and not self.prefix.isidentifier():
            raise ValueError(
                "Columns[...] UDF prefix must be empty or a valid identifier prefix"
            )

        seen: set[str] = set()
        unpacked_fields: list[UnpackedUDFField] = []
        struct_type = self.udf.data_type
        for idx in range(struct_type.num_fields):
            field = struct_type.field(idx)
            output_column = f"{self.prefix}{field.name}"
            if output_column in seen:
                raise ValueError(
                    "Columns[...] UDF produced duplicate output column "
                    f"{output_column!r}"
                )
            seen.add(output_column)
            unpacked_fields.append(
                UnpackedUDFField(
                    struct_field_name=field.name,
                    output_column=output_column,
                    field=field,
                )
            )

        object.__setattr__(self, "fields", tuple(unpacked_fields))


def _validate_timeout(
    instance: object,
    attribute: attrs.Attribute,
    value: float | None,
) -> None:
    """Validate that timeout is a positive finite number of seconds."""
    if value is None:
        return
    if not math.isfinite(value) or value <= 0:
        raise ValueError("timeout must be a positive finite number of seconds")


def _field_default_value(field: attrs.Attribute, instance: object | None = None) -> Any:
    """Return an attrs field default value, invoking factories when needed."""
    default = field.default
    if default is attrs.NOTHING:
        raise AttributeError(f"Missing required attribute '{field.name}'")
    if isinstance(default, _ATTRS_FACTORY_TYPE):
        default_factory = cast("Any", default)
        if default_factory.takes_self:
            if instance is None:
                raise AttributeError(
                    f"Cannot compute self-based default for attribute '{field.name}'"
                )
            return default_factory.factory(instance)
        return default_factory.factory()
    return default


# ---------------------------------------------------------------------------
# Helpers for dotted column paths (struct.field)
# ---------------------------------------------------------------------------


def _split_column_path(col_name: str) -> list[str]:
    return parse_field_path(col_name)


def _get_field_type_from_schema(schema: pa.Schema, col_name: str) -> pa.DataType:
    """Resolve the leaf PyArrow type for a (possibly dotted) column path.

    Supports nested struct paths such as ``info.left`` or ``info.nested.x`` by
    traversing struct children until the leaf field is found.
    """

    return resolve_arrow_field_path(schema, col_name).field.type


def _get_array_from_record_batch(batch: pa.RecordBatch, col_name: str) -> pa.Array:
    """Fetch column data from a RecordBatch, supporting dotted struct paths."""

    # If the full path is already a projected column, return directly.
    if col_name in batch.schema.names:
        return batch[col_name]
    try:
        projected_name = resolve_projected_field_path(batch.schema, col_name)
    except (KeyError, ValueError):
        projected_name = None
    if projected_name is not None:
        return batch[projected_name]

    resolved = resolve_arrow_field_path(batch.schema, col_name)
    if resolved.canonical_path in batch.schema.names:
        return batch[resolved.canonical_path]

    arr: pa.Array = batch[resolved.segments[0]]
    for part in resolved.segments[1:]:
        if not pa.types.is_struct(arr.type):
            raise KeyError(col_name)
        # pyarrow guarantees RecordBatch columns are Arrays; cast to StructArray
        # after the struct type check so static typing knows ``field`` exists.
        arr = cast("pa.StructArray", arr).field(part)  # pyright: ignore[reportAttributeAccessIssue]

    return arr


def _get_field_from_record_batch(batch: pa.RecordBatch, col_name: str) -> pa.Field:
    """Fetch a field from a RecordBatch schema, supporting dotted struct paths."""

    if col_name in batch.schema.names:
        return batch.schema.field(col_name)
    try:
        projected_name = resolve_projected_field_path(batch.schema, col_name)
    except (KeyError, ValueError):
        projected_name = None
    if projected_name is not None:
        return batch.schema.field(projected_name)

    resolved = resolve_arrow_field_path(batch.schema, col_name)
    if resolved.canonical_path in batch.schema.names:
        return batch.schema.field(resolved.canonical_path)

    return resolved.field


def _blob_list_to_record_batch(rows: list[dict[str, Any]]) -> pa.RecordBatch:
    """Convert a list[dict] (from blob-column reads) into a RecordBatch.

    Lance yields ``list[dict]`` instead of ``pa.RecordBatch`` when the scan
    includes blob columns.  BlobFile values are eagerly read into ``bytes``
    so that downstream Arrow operations work normally.

    Known limitation: ``pa.RecordBatch.from_pylist`` infers the schema from
    the data.  An empty *rows* list produces a zero-column batch, and columns
    that are ``None`` in every row are typed as ``pa.null()`` rather than
    their real type.
    """
    materialized = [
        {k: v.readall() if isinstance(v, BlobFile) else v for k, v in row.items()}
        for row in rows
    ]
    return pa.RecordBatch.from_pylist(materialized)


def _get_value_from_row(row: dict[str, Any], col_name: str) -> Any:
    """Fetch a value from a row dict with dotted paths."""

    parts = _split_column_path(col_name)
    cur: Any = row

    for part in parts:
        if not isinstance(cur, dict) or part not in cur:
            raise KeyError(col_name)
        cur = cur[part]
        if cur is None:
            # Early exit: once None, deeper fields are also None
            break

    return cur


class UDFArgType(enum.Enum):
    """
    The type of arguments that the UDF expects.
    """

    # Scalar Batch
    SCALAR = 0
    # Array mode
    ARRAY = 1
    # Pass a pyarrow RecordBatch
    RECORD_BATCH = 2


@attrs.define
class UDF(Callable[[pa.RecordBatch], pa.Array]):  # type: ignore
    """User-defined function (UDF) to be applied to a Lance Table."""

    # The reference to the callable
    func: Callable = attrs.field()
    name: str = attrs.field(default="")
    cuda: Optional[bool] = attrs.field(default=False)
    num_cpus: Optional[float] = attrs.field(
        default=1.0,
        converter=lambda v: None if v is None else float(v),
        validator=valid.optional(valid.ge(0.0)),
        on_setattr=[attrs.setters.convert, attrs.setters.validate],
    )
    num_gpus: Optional[float] = attrs.field(
        default=None,
        converter=lambda v: None if v is None else float(v),
        validator=valid.optional(valid.ge(0.0)),
        on_setattr=[attrs.setters.convert, attrs.setters.validate],
    )
    memory: int | None = attrs.field(default=None)
    batch_size: int | None = attrs.field(default=None)
    checkpoint_size: int | None = attrs.field(default=None)
    min_checkpoint_size: int | None = attrs.field(default=1)
    max_checkpoint_size: int | None = attrs.field(default=None)
    task_size: int | None = attrs.field(default=None)
    timeout: float | None = attrs.field(
        default=None,
        converter=lambda v: None if v is None else float(v),
        validator=_validate_timeout,
        on_setattr=[attrs.setters.convert, attrs.setters.validate],
    )

    # Error handling configuration
    error_handling: Optional["ErrorHandlingConfig"] = attrs.field(default=None)

    # Backwards-compatible deserialization: when a UDF was pickled with an
    # older Geneva that didn't have newly-added attrs fields, the slots
    # exist on the class but were never set during unpickling.  Return the
    # attrs default so the UDF still works.
    _FIELD_DEFAULTS: ClassVar[dict[str, Any]] = {
        "timeout": None,
        "error_handling": None,
    }

    def __getattr__(self, name: str) -> Any:
        defaults = object.__getattribute__(self, "_FIELD_DEFAULTS")
        if name in defaults:
            return defaults[name]
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute {name!r}"
        )

    def _record_batch_input(self) -> bool:
        sig = inspect.signature(self.func)
        if len(sig.parameters) == 1:
            param = list(sig.parameters.values())[0]
            return param.annotation == pa.RecordBatch
        return False

    def has_preprocess(self) -> bool:
        """True if the user code declares an optional ``preprocess()`` method.

        Detection looks at the *class*, not the instance: ``preprocess``
        is a common name for ML-side state (image transforms,
        tokenizers) that stateful UDFs assign to ``self.preprocess`` —
        e.g. ``GenEmbeddings`` holds an OpenCLIP image transform there.
        An instance-attribute check would mistake that callable for the
        protocol method and route record batches through it.
        """
        target = self.func
        cls = target if inspect.isclass(target) else type(target)
        return inspect.isfunction(getattr(cls, "preprocess", None))

    @property
    def arg_type(self) -> UDFArgType:
        if self._record_batch_input():
            return UDFArgType.RECORD_BATCH
        if _is_batched_func(self.func):
            return UDFArgType.ARRAY
        return UDFArgType.SCALAR

    @property
    def is_multi_output(self) -> bool:
        annotations = _get_annotations(self.func)
        return _columns_annotation_inner(annotations.get("return")) is not None

    input_columns: list[str] | None = attrs.field(default=None)

    data_type: pa.DataType = attrs.field(default=None)

    version: str = attrs.field(default="")

    _checkpoint_key_override: str | None = attrs.field(
        default=None, alias="checkpoint_key", repr=False
    )

    field_metadata: dict[str, str] = attrs.field(factory=dict)

    auto_backfill: bool = attrs.field(
        default=False,
        converter=lambda v: v if isinstance(v, bool) else str(v).lower() == "true",
    )

    # Optional GenevaManifest carrying the runtime environment (image, pip
    # deps, env vars, captured-environment zips). Snapshotted into column
    # field metadata at add_columns time when set; otherwise the column
    # falls back to the deployment default (remote mode) or the surrounding
    # cluster context (native mode). See revamped-api.md.
    manifest: "GenevaManifest | None" = attrs.field(default=None)

    @manifest.validator  # type: ignore[misc]
    def _validate_manifest(self, _attribute: Any, value: Any) -> None:
        if value is None:
            return
        # Avoid the import cycle and the runtime cost when no manifest is set.
        from geneva.manifest import GenevaManifest

        if not isinstance(value, GenevaManifest):
            raise TypeError(
                f"@udf(manifest=...) must be a GenevaManifest, got "
                f"{type(value).__name__}"
            )

    def __getstate__(self) -> dict[str, Any]:
        """Serialize UDFs compatibly across optional slot additions like timeout."""
        state: dict[str, Any] = {}
        for field in attrs.fields(self.__class__):
            if hasattr(self, field.name):
                state[field.name] = getattr(self, field.name)
            else:
                state[field.name] = _field_default_value(field, self)
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        """Restore UDF state while filling newer optional fields with defaults.

        Pickle restore bypasses attrs converters and __attrs_post_init__. This path
        only backfills newer optional fields, and relies on attrs field order if a
        missing field ever uses takes_self=True to depend on earlier fields.
        """
        for field in attrs.fields(self.__class__):
            if field.name in state:
                value = state[field.name]
            else:
                value = _field_default_value(field, self)
            object.__setattr__(self, field.name, value)

    def __attrs_post_init__(self) -> None:
        """
        Initialize UDF fields and normalize num_gpus after all fields are set:
          1) if cuda=True and num_gpus is None or 0.0 -> set to 1.0
          2) otherwise ignore cuda and just use num_gpus setting
        """
        # Set default name
        if not self.name:
            if inspect.isfunction(self.func):
                self.name = self.func.__name__
            elif isinstance(self.func, Callable):
                self.name = self.func.__class__.__name__
            else:
                raise ValueError(
                    f"func must be a function or a callable, got {self.func}"
                )

        # Set default input_columns
        if self.input_columns is None:
            sig = inspect.signature(self.func)
            params = list(sig.parameters.keys())
            if self._record_batch_input():
                self.input_columns = None
            else:
                self.input_columns = params

        # Validate input_columns
        if self.arg_type == UDFArgType.RECORD_BATCH:
            if self.input_columns is not None:
                raise ValueError(
                    "RecordBatch input UDF must not declare any input columns. "
                    "RecordBatch UDFs receive the entire batch and should not "
                    "specify input_columns. Consider using a stateful RecordBatch "
                    "UDF and parameterize it or use UDF with Array inputs."
                )
        else:
            if self.input_columns is None:
                raise ValueError("Array and Scalar input UDF must declare input column")

        if self.timeout is not None and self.arg_type != UDFArgType.SCALAR:
            raise ValueError(
                "timeout is only supported for scalar UDFs. "
                "Array and RecordBatch UDFs must not set timeout."
            )
        if self.timeout is not None:
            warnings.warn(
                "UDF timeout uses process-global SIGALRM/ITIMER_REAL. It only works "
                "for scalar UDFs running on a Unix-like worker process main thread "
                "(including MultiProcessBatchApplier worker processes). UDFs or "
                "libraries that install their own SIGALRM handlers/timers, or rely "
                "on main-thread signal behavior while coordinating work in "
                "background threads, may be incompatible.",
                UserWarning,
                stacklevel=2,
            )

        # Set default data_type
        if self.data_type is None:
            if self.arg_type != UDFArgType.SCALAR:
                raise ValueError(
                    "batched UDFs do not support data_type inference yet,"
                    " please specify data_type",
                )
            self.data_type = _infer_func_arrow_type(self.func, None)  # type: ignore[arg-type]

        # Validate data_type
        if self.data_type is None:
            raise ValueError("data_type must be set")
        if not isinstance(self.data_type, pa.DataType):
            raise ValueError(
                f"data_type must be a pyarrow.DataType, got {self.data_type}"
            )

        # Set default version
        if not self.version:
            self.version = _func_version_hash(self.func)

        # Normalize override
        if not self._checkpoint_key_override:
            self._checkpoint_key_override = None

        # Handle cuda/num_gpus normalization
        if self.cuda:
            warnings.warn(
                "The 'cuda' flag is deprecated. Please set 'num_gpus' explicitly "
                "(0.0 for CPU, >=1.0 for GPU).",
                DeprecationWarning,
                stacklevel=2,
            )

        if self.num_gpus is None:
            self.num_gpus = 1.0 if self.cuda is True else 0.0
        # otherwise fall back to user specified num_gpus

    @property
    def checkpoint_key(self) -> str:
        """Base checkpoint identifier for the UDF."""

        return self._checkpoint_key_override or f"{self.name}:{self.version}"

    @checkpoint_key.setter
    def checkpoint_key(self, value: str | None) -> None:
        self._checkpoint_key_override = value or None

    @property
    def checkpoint_version(self) -> str:
        """Version token embedded in the ``_ver-`` segment of checkpoint keys.

        This is the override when set, otherwise the UDF version. It is the
        single source of truth for the value compared during mismatch
        detection, which reads it back from the key rather than from
        checkpoint contents.
        """
        return self._checkpoint_key_override or self.version

    def checkpoint_prefix(
        self,
        *,
        column: str,
        dataset_uri: str,
        where: str | None = None,
        src_files_hash: str | None = None,
    ) -> str:
        """Build the prefix portion of a checkpoint key for this UDF."""

        return format_checkpoint_prefix(
            udf_name=self.name,
            udf_version=self.checkpoint_version,
            column=column,
            where=where,
            dataset_uri=dataset_uri,
            src_files_hash=src_files_hash,
        )

    def __repr__(self) -> str:
        """Custom repr that safely handles missing attributes during unpickling.

        This is necessary because attrs-generated __repr__ can fail when called
        during exception handling in Ray if the object hasn't been fully unpickled yet.
        """
        try:
            # Try to get all attrs fields safely
            field_strs = []
            for field in attrs.fields(self.__class__):
                # Check if attribute exists first before accessing it
                if hasattr(self, field.name):
                    value = getattr(self, field.name)
                    field_strs.append(f"{field.name}={value!r}")
                else:
                    field_strs.append(f"{field.name}=<not set>")

            return f"{self.__class__.__qualname__}({', '.join(field_strs)})"
        except Exception:
            # Fallback if even that fails
            return f"<{self.__class__.__name__} (repr failed)>"

    def _scalar_func_record_batch_call(
        self, record_batch: pa.RecordBatch | list[dict[str, Any]]
    ) -> pa.Array:
        """
        We use this when the UDF uses single call like
        `func(x_int, y_string, ...) -> type`

        this function automatically dispatches rows to the func and returns `pa.Array`
        """
        # Fallback to legacy pylist path if a list of dicts is provided
        if not isinstance(record_batch, pa.RecordBatch):
            return self._scalar_func_record_batch_call_py(record_batch)

        annotations = _get_annotations(self.func)
        sig = inspect.signature(self.func)
        params = list(sig.parameters.values())
        pos_params = [
            p
            for p in params
            if p.kind
            in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            )
        ]
        varargs_param = next(
            (p for p in params if p.kind == inspect.Parameter.VAR_POSITIONAL),
            None,
        )
        required_pos_count = sum(
            1 for p in pos_params if p.default is inspect.Parameter.empty
        )
        input_cols = cast("list[str]", self.input_columns)  # type: ignore[arg-type]

        if len(input_cols) > len(pos_params) and varargs_param is None:
            raise ValueError(
                f"UDF '{self.name}' expects {len(pos_params)} parameters but "
                f"{len(input_cols)} input_columns were provided."
            )

        if len(input_cols) < required_pos_count:
            raise ValueError(
                f"UDF '{self.name}' expects at least {required_pos_count} parameters "
                f"but {len(input_cols)} input_columns were provided."
            )

        # Build value accessors for each input column to avoid pylist conversion.
        from geneva.apply.blob_range import is_blob_field

        accessors = []
        for idx, col in enumerate(input_cols):
            param = pos_params[idx] if idx < len(pos_params) else varargs_param
            expected_type = annotations.get(param.name) if param else None
            field = _get_field_from_record_batch(record_batch, col)
            accessors.append(
                _make_value_accessor(
                    _get_array_from_record_batch(record_batch, col),
                    expected_type,
                    is_blob=is_blob_field(field),
                )
            )

        backfill_mask = (
            record_batch[BACKFILL_SELECTED]
            if BACKFILL_SELECTED in record_batch.schema.names
            else None
        )

        def _iter_arrow():  # noqa: ANN202
            for idx in range(record_batch.num_rows):
                if backfill_mask is not None and not backfill_mask[idx].as_py():
                    # Row not selected for backfill - keep placeholder
                    yield None
                    continue

                args = [accessor(idx) for accessor in accessors]
                yield self._call_scalar_with_timeout(*args)

        arr = _scalar_results_to_array(_iter_arrow(), self.data_type)
        # this should always by an Array, never should we get a ChunkedArray back here
        assert isinstance(arr, pa.Array)
        return arr

    def _scalar_func_record_batch_call_py(self, rows: list[dict[str, Any]]) -> pa.Array:
        """Legacy pylist path used when a RecordBatch is not provided."""

        def _iter():  # noqa: ANN202
            for item in rows:
                if BACKFILL_SELECTED not in item or item.get(BACKFILL_SELECTED):
                    # we know input_columns is not none here
                    args = [
                        _get_value_from_row(item, col)
                        for col in self.input_columns  # pyright: ignore[reportOptionalIterable]
                    ]  # type: ignore
                    yield self._call_scalar_with_timeout(*args)
                else:
                    yield None

        arr = _scalar_results_to_array(_iter(), self.data_type)
        assert isinstance(arr, pa.Array)
        return arr

    def _call_scalar_with_timeout(self, *args: Any) -> Any:
        """Execute a scalar UDF call with an optional timeout in seconds."""
        if self.timeout is None:
            return self.func(*args)

        with self._scalar_timeout_context():
            return self.func(*args)

    @contextlib.contextmanager
    def _scalar_timeout_context(self) -> Iterator[None]:
        """Apply a per-call timeout for scalar UDF execution.

        This uses SIGALRM/ITIMER_REAL and is therefore Unix-only. The timeout
        is measured in seconds, only works on the main thread, and is
        best-effort for Python execution.
        """
        timeout_seconds = self.timeout
        assert timeout_seconds is not None

        if not all(
            hasattr(signal, attr) for attr in ("SIGALRM", "ITIMER_REAL", "setitimer")
        ) or not hasattr(signal, "getitimer"):
            raise RuntimeError(
                f"UDF '{self.name}' uses timeout={timeout_seconds}, but this runtime "
                "does not support signal.setitimer(SIGALRM)."
            )

        if threading.current_thread() is not threading.main_thread():
            raise RuntimeError(
                f"UDF '{self.name}' uses timeout={timeout_seconds}, but SIGALRM-based "
                "timeouts only work on the main thread. This can fail at runtime "
                "if a worker executes UDFs from a thread pool."
            )

        previous_handler = signal.getsignal(signal.SIGALRM)
        previous_timer = signal.getitimer(signal.ITIMER_REAL)
        start = time.monotonic()

        def _handle_timeout(signum, frame) -> None:  # noqa: ARG001
            raise TimeoutError(
                f"UDF '{self.name}' exceeded timeout={timeout_seconds} seconds"
            )

        try:
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.setitimer(signal.ITIMER_REAL, timeout_seconds)
            yield
        except ValueError as exc:
            raise RuntimeError(
                f"UDF '{self.name}' uses timeout={timeout_seconds}, but this runtime "
                "cannot install SIGALRM handlers."
            ) from exc
        finally:
            elapsed = time.monotonic() - start
            remaining = max(0.0, previous_timer[0] - elapsed)
            signal.setitimer(signal.ITIMER_REAL, 0.0, 0.0)
            signal.signal(signal.SIGALRM, previous_handler)
            signal.setitimer(
                signal.ITIMER_REAL,
                remaining,
                previous_timer[1],
            )

    def _input_columns_validator(self, attribute, value) -> None:
        """Validate input_columns attribute for attrs compatibility."""
        if self.arg_type == UDFArgType.RECORD_BATCH:
            if value is not None:
                raise ValueError(
                    "RecordBatch input UDF must not declare any input columns. "
                    "RecordBatch UDFs receive the entire batch and should not "
                    "specify input_columns."
                )
        else:
            if value is None:
                raise ValueError("Array and Scalar input UDF must declare input column")

    def validate_against_schema(
        self, table_schema: pa.Schema, input_columns: list[str] | None = None
    ) -> None:
        """
        Validate UDF against table schema.

        This is the primary validation method that should be called before executing
        a UDF. It performs comprehensive validation including:

        1. **Column Existence**: Verifies all input columns exist in the table schema
        2. **Type Compatibility**: Checks that column types match UDF type annotations
           (if present)
        3. **RecordBatch Constraints**: Ensures RecordBatch UDFs don't have
           input_columns defined

        The validation happens at two points in the UDF lifecycle:
        - At `add_columns()` time when defining the column
        - At `backfill()` time when executing (if input_columns are overridden)

        Parameters
        ----------
        table_schema: pa.Schema
            The schema of the table being processed
        input_columns: list[str] | None
            The input column names to validate. If None, uses self.input_columns.

        Raises
        ------
        ValueError: If validation fails for any of the following reasons:
            - Input columns don't exist in table schema
            - Type mismatch between table and UDF expectations
            - RecordBatch UDF has input_columns defined
            - Array/Scalar UDF has no input_columns defined

        Warns
        -----
        UserWarning: If type validation is skipped due to:
            - UDF has no type annotations
            - Type annotation can't be mapped to PyArrow types

        Examples
        --------
        >>> @udf(data_type=pa.int32())
        ... def my_udf(a: int) -> int:
        ...     return a * 2
        >>> my_udf.validate_against_schema(table.schema)  # Validates column 'a' exists
        """

        # Determine which columns to validate
        cols_to_validate = (
            input_columns if input_columns is not None else self.input_columns
        )

        # Check RecordBatch UDFs
        if self.arg_type == UDFArgType.RECORD_BATCH:
            # Error if input_columns are specified for RecordBatch UDFs
            if cols_to_validate is not None:
                raise ValueError(
                    f"UDF '{self.name}' is a RecordBatch UDF but has input_columns "
                    f"{cols_to_validate} specified. RecordBatch UDFs receive the "
                    f"entire batch and should not declare input_columns. "
                    f"Remove the input_columns parameter."
                )
            # RecordBatch UDFs don't need column validation
            return

        # For Array and Scalar UDFs, input_columns must be defined
        if cols_to_validate is None:
            arg_type_name = self.arg_type.name if self.arg_type else "UNKNOWN"
            raise ValueError(
                f"UDF '{self.name}' (type: {arg_type_name}) has no input_columns "
                f"defined. Array and Scalar UDFs must specify input columns either "
                f"through function parameter names or the input_columns parameter."
            )

        # Validate all input columns exist in table schema. UDFs with a
        # ``preprocess()`` method may legitimately list columns that
        # don't exist in the source — preprocess produces them from the
        # read batch and adds them before ``__call__`` runs. The
        # preprocess-overlap pipelining stage explicitly depends on this.
        # We can't tell which missing columns are preprocess-produced vs.
        # typos without an explicit declaration, so when preprocess
        # exists we trust the caller and skip the existence check
        # entirely (the pipelining runtime will surface real bugs as
        # KeyError on the read batch).
        if self.has_preprocess():
            self._validate_column_types(table_schema, cols_to_validate)
            return

        missing_columns: list[str] = []
        for col in cols_to_validate:
            try:
                _get_field_type_from_schema(table_schema, col)
            except KeyError:  # noqa: PERF203
                missing_columns.append(col)

        if missing_columns:
            raise ValueError(
                f"UDF '{self.name}' expects input columns {missing_columns} which are "
                f"not found in table schema. Available columns: {table_schema.names}. "
                f"Check your UDF's function parameter names or input_columns parameter."
            )

        # Validate type compatibility for each input column
        self._validate_column_types(table_schema, cols_to_validate)

    def _validate_column_types(
        self, table_schema: pa.Schema, input_columns: list[str]
    ) -> None:
        """
        Validate type compatibility between table schema and UDF expectations.

        This method checks if the table column types match the UDF's type annotations.
        If no type annotations are present or types can't be mapped, validation is
        skipped with a warning.

        Parameters
        ----------
        table_schema: pa.Schema
            The schema of the table being processed
        input_columns: list[str]
            The input column names to validate types for

        Raises
        ------
        ValueError: If there's a type mismatch between table schema and UDF expectations

        Warns
        -----
        UserWarning: If type validation is skipped due to missing annotations or
            unmappable types
        """
        import warnings

        # Get type annotations from the UDF function
        annotations = _get_annotations(self.func)

        if not annotations:
            # No type annotations found - warn user
            warnings.warn(
                f"UDF '{self.name}' has no type annotations. Type validation will be "
                f"skipped. Consider adding type hints to your UDF function parameters "
                f"for better error detection.",
                UserWarning,
                stacklevel=4,
            )
            return

        # For each input column, validate type if annotation exists.
        sig = inspect.signature(self.func)
        params = list(sig.parameters.values())
        pos_params = [
            p
            for p in params
            if p.kind
            in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            )
        ]
        varargs_param = next(
            (p for p in params if p.kind == inspect.Parameter.VAR_POSITIONAL),
            None,
        )
        required_pos_count = sum(
            1 for p in pos_params if p.default is inspect.Parameter.empty
        )

        if len(input_columns) > len(pos_params) and varargs_param is None:
            raise ValueError(
                f"UDF '{self.name}' expects {len(pos_params)} parameters but "
                f"{len(input_columns)} input_columns were provided."
            )

        if len(input_columns) < required_pos_count:
            raise ValueError(
                f"UDF '{self.name}' expects at least {required_pos_count} parameters "
                f"but {len(input_columns)} input_columns were provided."
            )

        # UDFs with ``preprocess()`` may declare ``input_columns`` whose
        # values come from preprocess rather than from the source table,
        # so those columns aren't in ``table_schema``. Skip type checks
        # for them — the runtime will raise a clear error if preprocess
        # produces the wrong type.
        has_preprocess = self.has_preprocess()

        for idx, col_name in enumerate(input_columns):
            param = pos_params[idx] if idx < len(pos_params) else varargs_param
            param_name = param.name if param else f"arg_{idx}"
            expected_type = annotations.get(param_name) if param else None

            # Get the actual type from table schema (supports dotted paths)
            try:
                table_type = _get_field_type_from_schema(table_schema, col_name)
            except KeyError:
                if has_preprocess:
                    continue
                raise
            is_list_type = (
                pa.types.is_list(table_type)
                or pa.types.is_large_list(table_type)
                or pa.types.is_fixed_size_list(table_type)
            )

            if expected_type is None:
                continue

            wants_numpy = _annotation_requests_numpy_ndarray(expected_type)
            wants_list = _annotation_requests_list(expected_type)

            if wants_numpy and wants_list:
                raise ValueError(
                    f"Parameter '{param_name}' in UDF '{self.name}' is annotated as "
                    "both numpy.ndarray and list; choose one representation for "
                    "list-backed columns."
                )

            if wants_numpy:
                if is_list_type:
                    # Compatible – skip further validation because dtype/shape
                    # information is not available from the annotation alone.
                    continue
                raise ValueError(
                    f"Type mismatch for column '{col_name}' (parameter '{param_name}') "
                    f"in UDF '{self.name}': table has type {table_type}, but the "
                    "parameter is annotated as numpy.ndarray. numpy.ndarray inputs are "
                    "supported only for list, large_list, or fixed-size list Arrow "
                    "columns."
                )

            if wants_list:
                if is_list_type:
                    continue
                raise ValueError(
                    f"Type mismatch for column '{col_name}' (parameter '{param_name}') "
                    f"in UDF '{self.name}': table has type {table_type}, but the "
                    "parameter is annotated as a Python list. List annotations require "
                    "Arrow list, large_list, or fixed-size list column types."
                )

            # Try to map expected type to PyArrow type for comparison
            try:
                expected_pa_type = self._python_type_to_arrow_type(expected_type)

                # Check if types are compatible
                if not self._types_compatible(table_type, expected_pa_type):
                    raise ValueError(
                        f"Type mismatch for column '{col_name}' (parameter "
                        f"'{param_name}') in UDF '{self.name}': table has type "
                        f"{table_type}, but UDF expects {expected_pa_type} (from "
                        f"annotation {expected_type}). This will likely cause "
                        "serialization or conversion errors during execution."
                    )
            except (ValueError, KeyError):
                # If we can't map the type, skip validation with warning
                warnings.warn(
                    f"Could not validate type for column '{col_name}' (parameter "
                    f"'{param_name}') in UDF '{self.name}' with annotation "
                    f"{expected_type}. Type validation skipped for this column.",
                    UserWarning,
                    stacklevel=4,
                )

    def _python_type_to_arrow_type(self, python_type) -> pa.DataType:
        """
        Convert Python type annotation to PyArrow type.

        Raises ValueError if type cannot be mapped.
        """
        # Handle PyArrow types directly
        if isinstance(python_type, pa.DataType):
            return python_type

        # Handle pa.Array annotation (for batched UDFs)
        if python_type == pa.Array:
            # Can't determine specific array type, so return None to skip validation
            raise ValueError("Cannot validate generic pa.Array type")

        # Map Python/numpy types to PyArrow types
        type_map = {
            bool: pa.bool_(),
            bytes: pa.binary(),
            float: pa.float32(),
            int: pa.int64(),
            str: pa.string(),
            numpy.bool_: pa.bool_(),
            numpy.uint8: pa.uint8(),
            numpy.uint16: pa.uint16(),
            numpy.uint32: pa.uint32(),
            numpy.uint64: pa.uint64(),
            numpy.int8: pa.int8(),
            numpy.int16: pa.int16(),
            numpy.int32: pa.int32(),
            numpy.int64: pa.int64(),
            numpy.float16: pa.float16(),
            numpy.float32: pa.float32(),
            numpy.float64: pa.float64(),
            numpy.str_: pa.string(),
        }

        if python_type in type_map:
            return type_map[python_type]

        raise ValueError(f"Cannot map Python type {python_type} to PyArrow type")

    def _types_compatible(self, actual: pa.DataType, expected: pa.DataType) -> bool:
        """
        Check if actual type is compatible with expected type.

        This is more permissive than exact equality, allowing for:
        - Exact matches
        - Nullable vs non-nullable variants
        """
        # Exact match
        if actual == expected:
            return True

        # Check base types match (ignoring nullability, precision differences)
        # For numeric types, check if they're in the same family
        if pa.types.is_integer(actual) and pa.types.is_integer(expected):
            # Allow integer types if bit width and signedness match
            return actual.bit_width == expected.bit_width and (
                (
                    pa.types.is_signed_integer(actual)
                    and pa.types.is_signed_integer(expected)
                )
                or (
                    pa.types.is_unsigned_integer(actual)
                    and pa.types.is_unsigned_integer(expected)
                )
            )

        if pa.types.is_floating(actual) and pa.types.is_floating(expected):
            # Require exact match for floating point types (float32 vs float64 matters!)
            return actual.bit_width == expected.bit_width

        # For other types, require exact match
        return False

    def __call__(self, *args, use_applier: bool = False, **kwargs) -> pa.Array:
        # dispatch coming from Applier or user calling with a `RecordBatch`
        if use_applier or (
            len(args) == 1 and isinstance(args[0], (pa.RecordBatch, list))
        ):
            record_batch = cast("pa.RecordBatch | list[dict[str, Any]]", args[0])
            match self.arg_type:
                case UDFArgType.SCALAR:
                    if isinstance(record_batch, list):
                        return self._scalar_func_record_batch_call_py(record_batch)
                    return self._scalar_func_record_batch_call(record_batch)
                case UDFArgType.ARRAY:
                    # Blob columns yield list[dict] instead of RecordBatch;
                    # materialize BlobFiles and convert before extracting
                    # columns (mirrors the RECORD_BATCH branch).
                    if isinstance(record_batch, list):
                        record_batch = _blob_list_to_record_batch(record_batch)
                    # Validate columns exist before accessing them
                    try:
                        arrs = [
                            _get_array_from_record_batch(record_batch, col)
                            for col in self.input_columns  # pyright: ignore[reportOptionalIterable]
                        ]  # type:ignore
                    except KeyError as e:
                        raise KeyError(
                            f"UDF '{self.name}' failed: column {e} not found in "
                            f"RecordBatch. Available columns: "
                            f"{record_batch.schema.names}. UDF expects "
                            f"input_columns: {self.input_columns}."
                        ) from e
                    return self.func(*arrs)
                case UDFArgType.RECORD_BATCH:
                    if isinstance(record_batch, pa.RecordBatch):
                        return self.func(record_batch)
                    # a list of dicts with BlobFiles that need to de-ref'ed
                    assert isinstance(record_batch, list)
                    return self.func(_blob_list_to_record_batch(record_batch))
        # dispatch is trying to access the function's original pattern
        return self.func(*args, **kwargs)


def udf(
    func: Callable | None = None,
    *,
    data_type: pa.DataType | None = None,
    version: str | None = None,
    cuda: bool = False,  # deprecated
    field_metadata: dict[str, str] | None = None,
    input_columns: list[str] | None = None,
    num_cpus: int | float | None = None,
    num_gpus: int | float | None = None,
    memory: int | None = None,
    batch_size: int | None = None,
    checkpoint_size: int | None = None,
    min_checkpoint_size: int | None = 1,
    max_checkpoint_size: int | None = None,
    task_size: int | None = None,
    timeout: float | None = None,
    on_error: "list[ExceptionMatcher] | ErrorHandlingConfig | None" = None,
    error_handling: Optional["ErrorHandlingConfig"] = None,
    auto_backfill: bool = False,
    manifest: "GenevaManifest | None" = None,
    **kwargs,
) -> UDF | functools.partial:
    """Decorator of a User Defined Function ([UDF][geneva.transformer.UDF]).

    Parameters
    ----------
    func: Callable
        The callable to be decorated. If None, returns a partial function.
    data_type: pa.DataType, optional
        The data type of the output PyArrow Array from the UDF.
        If None, it will be inferred from the function signature.
    version: str, optional
        A version string to manage the changes of function.
        If not provided, it will use the hash of the serialized function.
    cuda: bool, optional, Deprecated
        If true, load CUDA optimized kernels.  Equvalent to num_gpus=1
    field_metadata: dict[str, str], optional
        A dictionary of metadata to be attached to the output `pyarrow.Field`.
    input_columns: list[str], optional
        A list of input column names for the UDF. If not provided, it will be
        inferred from the function signature. Or scan all columns. Names may
        also refer to columns produced by an optional ``preprocess()`` step
        (see Notes); the validator skips the source-schema existence check
        for those.
    num_cpus: int, float, optional
        The (fraction) number of CPUs to acquire to run the job.
    num_gpus: int, float, optional
        The (fraction) number of GPUs to acquire to run the job.  Default 0.
    memory: int, optional
        The amount of memory in bytes to acquire to run the job. Used by
        admission control to validate cluster resources before starting.
    batch_size: int, optional (deprecated)
        Legacy parameter controlling map/read batch size. Prefer checkpoint_size.
    checkpoint_size: int, optional
        Alias for batch_size; preferred for overriding map-task batch size.
        When adaptive sizing is enabled, an explicit checkpoint_size seeds the
        initial checkpoint size; otherwise the initial size defaults to
        min_checkpoint_size.
    min_checkpoint_size: int, optional
        Minimum adaptive checkpoint size (lower bound). Defaults to 1.
    max_checkpoint_size: int, optional
        Maximum adaptive checkpoint size (upper bound). This also caps the
        largest read batch and thus the maximum memory footprint per batch.
    task_size: int, optional
        Preferred read-task size for jobs that don't specify an explicit
        ``task_size``. This is advisory and may be overridden by job-level
        parameters.
    timeout: float, optional
        Per-row scalar UDF timeout in seconds. Each retry attempt gets a fresh
        timeout budget. Only supported for scalar UDFs, and requires execution
        on a Unix-like worker process main thread. This uses process-global
        ``SIGALRM`` / ``ITIMER_REAL`` state, so UDFs or libraries that install
        their own signal handlers/timers, or that depend on main-thread signal
        behavior while coordinating work in background threads, may be
        incompatible.
    on_error: list[ExceptionMatcher] | ErrorHandlingConfig, optional
        Simplified error handling configuration. Can be:
        - A factory function: retry_transient(), retry_all(), skip_on_error()
        - A list of matchers: [Retry(...), Skip(...), Fail(...)]

        UDF backfill also exposes fatal worker-loss exceptions such as
        ``FatalWorkerExitError`` and ``FatalWorkerTransientError``. By default,
        fatal worker errors are retried up to 3 total attempts, then bisected
        until only failing rows are written as NULL. Native crashes
        skip retry but still use row isolation; OOM and deterministic integrity
        failures keep their specialized behavior. An explicit matching
        ``on_error`` policy overrides the default for that error type. Ordinary
        UDF exceptions retain their existing fail-fast default.

        Examples
        --------

            @udf(data_type=pa.int32(), on_error=retry_transient())
            def my_udf(x: int) -> int: ...

            @udf(data_type=pa.int32(), on_error=retry_transient(max_attempts=5))
            def my_udf(x: int) -> int: ...

            @udf(
                data_type=pa.int32(),
                on_error=[
                    Retry(ConnectionError, TimeoutError, max_attempts=3),
                    Retry(ValueError, match="rate limit", max_attempts=5),
                    Skip(ValueError),
                ]
            )
            def my_udf(x: int) -> int: ...

            @udf(
                data_type=pa.int32(),
                on_error=[Retry(FatalWorkerTransientError, max_attempts=5)],
            )
            def my_udf(x: int) -> int: ...

    error_handling: ErrorHandlingConfig, optional
        Advanced error handling configuration using tenacity. Use this for
        full control over retry behavior with custom callbacks.
        Cannot be used together with ``on_error``.
    auto_backfill: bool, optional
        Automatically backfill this column asynchronously in LanceDB Enterprise when
        data or UDF version changes. Default: False
    manifest: GenevaManifest | None, optional
        Optional execution-environment spec (image, pip deps, py_modules,
        captured workspace zips). Built via ``GenevaManifest.create_pip()``,
        ``.create_conda()``, or ``Connection.capture_local_environment()``.
        When set, the manifest is snapshotted into the column's field
        metadata at ``add_columns`` time so the backfill executor can
        reconstruct the same environment without consulting any external
        registry. When omitted, native columns fall back to the embedded
        image/tag in the UDFSpec envelope, and remote columns fall back
        to the deployment-default manifest resolved server-side. Default:
        ``None``.

    Notes
    -----
    - **Column/parameter mapping**: For scalar and array UDFs, parameter names map
      directly to input column names. If you want a column to be delivered as a
      ``numpy.ndarray`` without extra copies, annotate the parameter as
      ``numpy.ndarray`` and ensure the column's Arrow type is a list
      (``pa.list_``/``pa.large_list``/``pa.fixed_size_list``). Other column types
      continue to be passed as Python scalars/objects.
    - **Python lists**: When a parameter is annotated as ``list[...]``, the column
      must be an Arrow list/large_list/fixed_size_list. In that case each value is
      delivered to the UDF as a Python list instead of a numpy array.
    - **Return type with numpy.ndarray**: If your function returns a
      ``numpy.ndarray``, you must provide an explicit ``data_type`` (for example,
      ``pa.list_(pa.float32())``); the ndarray shape/dtype cannot be inferred
      automatically from the annotation alone.
    - **Optional ``preprocess()`` hook**: Stateful (class-based) UDFs may
      declare a ``preprocess(self, batch: pa.RecordBatch) -> pa.RecordBatch``
      method. When GPU pipelining is enabled, the framework runs
      ``preprocess()`` in a pool of reader threads before dispatching
      ``__call__``, letting CPU-side decode / transform / tokenize overlap
      with GPU compute on previous batches. The contract:

      * ``preprocess()`` returns a ``RecordBatch`` whose columns include
        every name listed in ``input_columns`` for ``__call__``.
      * Coupling between ``preprocess()`` and ``__call__`` is by **column
        name only** — the framework dispatches ``__call__`` by pulling
        ``input_columns`` out of the post-preprocess batch. There is no
        type/shape metadata flowing between the two; if names mismatch,
        the failure is a runtime ``KeyError`` on the first batch.
      * Names introduced by ``preprocess()`` are user-chosen. Conventional
        practice is a non-user-facing prefix (``_pp_*``) to avoid colliding
        with persisted columns.

      ``preprocess()`` runs only when GPU pipelining is enabled (config
      ``enable_gpu_pipelining`` / env ``JOB__ENABLE_GPU_PIPELINING=true``).
      For best throughput the hot path inside ``preprocess()`` should
      release the GIL — use native libraries (cv2, HF ``tokenizers``,
      torchaudio, numpy vector ops) rather than per-element Python loops.
    """
    if inspect.isclass(func):

        @functools.wraps(func)
        def _wrapper(*args, **kwargs) -> UDF | functools.partial:
            callable_obj = func(*args, **kwargs)
            return udf(
                callable_obj,
                cuda=cuda,
                data_type=data_type,
                version=version,
                field_metadata=field_metadata,
                input_columns=input_columns,
                num_cpus=num_cpus,
                num_gpus=num_gpus,
                memory=memory,
                batch_size=batch_size,
                checkpoint_size=checkpoint_size,
                min_checkpoint_size=min_checkpoint_size,
                max_checkpoint_size=max_checkpoint_size,
                task_size=task_size,
                timeout=timeout,
                on_error=on_error,
                error_handling=error_handling,
                auto_backfill=auto_backfill,
                manifest=manifest,
            )

        return _wrapper  # type: ignore

    if func is None:
        return functools.partial(
            udf,
            cuda=cuda,
            data_type=data_type,
            version=version,
            field_metadata=field_metadata,
            input_columns=input_columns,
            num_cpus=num_cpus,
            num_gpus=num_gpus,
            memory=memory,
            batch_size=batch_size,
            checkpoint_size=checkpoint_size,
            min_checkpoint_size=min_checkpoint_size,
            max_checkpoint_size=max_checkpoint_size,
            task_size=task_size,
            timeout=timeout,
            on_error=on_error,
            error_handling=error_handling,
            auto_backfill=auto_backfill,
            manifest=manifest,
            **kwargs,
        )

    effective_batch_size = resolve_batch_size(
        batch_size=batch_size,
        checkpoint_size=checkpoint_size,
    )

    # Resolve on_error to error_handling
    effective_error_handling = error_handling
    if on_error is not None:
        if error_handling is not None:
            raise ValueError(
                "Cannot specify both 'on_error' and 'error_handling'. "
                "Use 'on_error' for simple cases or 'error_handling' for advanced use."
            )
        from geneva.debug.error_store import resolve_on_error

        effective_error_handling = resolve_on_error(on_error)

    # we depend on default behavior of attrs to infer the output schema
    def _include_if_not_none(name, value) -> dict[str, Any]:
        if value is not None:
            return {name: value}
        return {}

    args = {
        "func": func,
        "cuda": cuda,
        **_include_if_not_none("data_type", data_type),
        **_include_if_not_none("version", version),
        **_include_if_not_none("field_metadata", field_metadata),
        **_include_if_not_none("input_columns", input_columns),
        **_include_if_not_none("num_cpus", num_cpus),
        **_include_if_not_none("num_gpus", num_gpus),
        **_include_if_not_none("memory", memory),
        **_include_if_not_none("batch_size", effective_batch_size),
        **_include_if_not_none("checkpoint_size", checkpoint_size),
        **_include_if_not_none("min_checkpoint_size", min_checkpoint_size),
        **_include_if_not_none("max_checkpoint_size", max_checkpoint_size),
        **_include_if_not_none("task_size", task_size),
        **_include_if_not_none("timeout", timeout),
        **_include_if_not_none("error_handling", effective_error_handling),
        "auto_backfill": auto_backfill,
        **_include_if_not_none("manifest", manifest),
    }
    # can't use functools.update_wrapper because attrs makes certain assumptions
    # and attributes read-only. We will figure out docs and stuff later
    return UDF(**args)


def _get_annotations(func: Callable) -> dict[str, Any]:
    """Get evaluated annotations when possible.

    Many UDF modules use ``from __future__ import annotations`` which stores
    annotations as strings. We attempt to evaluate them so list/ndarray handling
    can honor the developer's intent. If evaluation fails, fall back to raw
    annotations.
    """

    target = func if inspect.isfunction(func) else func.__call__  # type: ignore[union-attr]

    # First try typing.get_type_hints for robust evaluation on Python 3.10+.
    # Cloudpickle/Ray may omit names that are only used in annotations; augment
    # the namespace with typing/builtins so evaluation still succeeds.
    globalns = getattr(target, "__globals__", {}) or {}
    augmented_ns: dict[str, Any] = dict(globalns)
    augmented_ns.update(vars(typing))
    augmented_ns.setdefault("Any", Any)
    augmented_ns.setdefault("Optional", Optional)
    augmented_ns.setdefault("Union", Union)
    augmented_ns.setdefault("list", list)
    augmented_ns.setdefault("dict", dict)
    augmented_ns.setdefault("numpy", numpy)
    augmented_ns.setdefault("np", numpy)
    augmented_ns.setdefault("pa", pa)
    augmented_ns.setdefault("Columns", Columns)

    with contextlib.suppress(Exception):
        try:
            return get_type_hints(
                target,
                globalns=augmented_ns,
                localns=augmented_ns,
                include_extras=True,
            )
        except TypeError:
            # include_extras not supported on some versions
            return get_type_hints(target, globalns=augmented_ns, localns=augmented_ns)

    # Fallback to inspect.get_annotations; eval_str may not exist on older versions.
    try:
        return inspect.get_annotations(target, eval_str=True)
    except Exception:
        return inspect.get_annotations(target)


def _is_batched_func(func: Callable) -> bool:
    annotations = _get_annotations(func)
    if "return" not in annotations:
        return False

    ret_type = annotations["return"]
    if ret_type != pa.Array and not isinstance(ret_type, pa.DataType):
        return False

    input_keys = list(annotations.keys() - {"return"})
    if len(input_keys) == 1:
        return all(
            annotations[input_key] in [pa.RecordBatch, pa.Array]
            for input_key in input_keys
        )

    if any(annotations[input_key] == pa.RecordBatch for input_key in input_keys):
        raise ValueError(
            "UDF can not have multiple parameters with 'pa.RecordBatch' type"
        )
    return all(annotations[input_key] in [pa.Array] for input_key in input_keys)


def _annotation_matches_type(annotation: Any | None, target: type) -> bool:
    """Return True if annotation (including Union/Annotated) includes ``target``."""

    if annotation is None:
        return False

    if annotation is target:
        return True

    origin = get_origin(annotation)
    if origin is None:
        return False

    if origin is target:
        return True

    if origin is Annotated:
        base, *_ = get_args(annotation)
        return _annotation_matches_type(base, target)

    if origin in (Union, UnionType):
        return any(
            _annotation_matches_type(arg, target)
            for arg in get_args(annotation)
            if arg is not NoneType
        )

    return False


def _annotation_requests_numpy_ndarray(annotation: Any | None) -> bool:
    return _annotation_matches_type(annotation, numpy.ndarray)


def _annotation_requests_list(annotation: Any | None) -> bool:
    return _annotation_matches_type(annotation, list)


def _is_binary_arrow_type(data_type: pa.DataType) -> bool:
    return pa.types.is_binary(data_type) or pa.types.is_large_binary(data_type)


def _write_binary_result(value_sink: pa.BufferOutputStream, value: Any) -> int:
    if isinstance(value, pa.Buffer):
        value_sink.write(value)
        return value.size
    try:
        view = memoryview(value)
    except TypeError as exc:
        raise pa.ArrowTypeError(
            f"Expected bytes-like value for binary scalar UDF output, got "
            f"{type(value).__name__!r}"
        ) from exc
    byte_view = view.cast("B") if view.format != "B" else view
    value_sink.write(byte_view)
    return byte_view.nbytes


def _scalar_results_to_array(
    results: Iterator[Any], data_type: pa.DataType
) -> pa.Array:
    """Build scalar UDF results without accumulating Python binary objects.

    Binary outputs use Arrow buffers directly so UDFs can return ``bytes``,
    ``bytearray``, ``memoryview``, or ``pa.Buffer``. The validity bitmap is
    allocated lazily: all-valid result batches pass ``None`` for the null
    bitmap, and the bitmap is only created after the first null result. Once a
    null is seen, prior rows are marked valid and later rows maintain the bitmap
    while the payload buffer continues to stream in one pass.
    """

    if not _is_binary_arrow_type(data_type):
        return cast("pa.Array", pa.array(results, type=data_type))

    offsets = array("q" if pa.types.is_large_binary(data_type) else "i", [0])
    validity: bytearray | None = None
    valid_count = 0
    length = 0
    value_sink = pa.BufferOutputStream()

    for value in results:
        if value is None:
            if validity is None:
                validity = _binary_validity_for_prior_rows(length)
            else:
                _ensure_binary_validity_byte(validity, length)
            offsets.append(offsets[-1])
            length += 1
            continue

        value_size = _write_binary_result(value_sink, value)
        offsets.append(offsets[-1] + value_size)
        if validity is not None:
            _ensure_binary_validity_byte(validity, length)
            validity[length // 8] |= 1 << (length % 8)
        valid_count += 1
        length += 1

    null_count = length - valid_count
    null_bitmap = None if validity is None else pa.py_buffer(validity)
    return pa.Array.from_buffers(
        data_type,
        length,
        cast(
            "list[pa.Buffer]",
            [null_bitmap, pa.py_buffer(offsets), value_sink.getvalue()],
        ),
        null_count=null_count,
    )


def _binary_validity_for_prior_rows(prior_rows: int) -> bytearray:
    byte_count = (prior_rows + 8) // 8
    validity = bytearray(byte_count)
    full_bytes, remainder = divmod(prior_rows, 8)
    validity[:full_bytes] = b"\xff" * full_bytes
    if remainder:
        validity[full_bytes] = (1 << remainder) - 1
    return validity


def _ensure_binary_validity_byte(validity: bytearray, row_idx: int) -> None:
    byte_idx = row_idx // 8
    if byte_idx >= len(validity):
        validity.extend(b"\x00" * (byte_idx + 1 - len(validity)))


def _make_value_accessor(
    array: pa.Array, expected_type: Any | None = None, *, is_blob: bool = False
) -> Callable[[int], Any]:
    """Return a fast row accessor for a column.

    For list/large_list/fixed_size_list columns we can either:
    - Return Python lists when the parameter is annotated as ``list[...]``
    - Return numpy arrays (zero-copy when possible) when the parameter is annotated
      as ``numpy.ndarray`` or no preference is declared.
    """

    if is_blob:
        from geneva.apply.blob_range import BufferBackedBlobFile, InMemoryBlobFile

        if _is_binary_arrow_type(array.type):
            offset_dtype = (
                numpy.int64 if pa.types.is_large_binary(array.type) else numpy.int32
            )
            offset_buffer = array.buffers()[1]
            assert offset_buffer is not None
            offsets = numpy.frombuffer(offset_buffer, dtype=offset_dtype)
            values_buffer = array.buffers()[2] or pa.py_buffer(b"")
            base_offset = array.offset
            valid = (
                None
                if array.null_count == 0
                else array.is_valid().to_numpy(zero_copy_only=False)
            )

            def _binary_blob_getter(i: int) -> Any:
                if valid is not None and not valid[i]:
                    return None
                start = int(offsets[base_offset + i])
                end = int(offsets[base_offset + i + 1])
                return BufferBackedBlobFile(
                    values_buffer, offset=start, size=end - start
                )

            return _binary_blob_getter

        def _blob_getter(i: int) -> Any:
            scalar = array[i]
            if not scalar.is_valid:
                return None
            value = scalar.as_py()
            if isinstance(value, BlobFile):
                return value
            if isinstance(value, dict):
                # Legacy Lance blob scans may expose a dict payload shape.
                value = value.get("data")
                if value is None:
                    return None
            return InMemoryBlobFile(value)

        return _blob_getter

    prefers_numpy = _annotation_requests_numpy_ndarray(expected_type)
    prefers_pylist = _annotation_requests_list(expected_type)

    if prefers_numpy and prefers_pylist:
        raise ValueError(
            "Ambiguous type annotation requesting both list and numpy.ndarray for the "
            "same parameter. Please choose one."
        )

    is_list_like = pa.types.is_list(array.type) or pa.types.is_large_list(array.type)
    is_fixed_size_list = pa.types.is_fixed_size_list(array.type)

    if prefers_numpy and not (is_list_like or is_fixed_size_list):
        raise ValueError(
            f"Column has type {array.type} but parameter is "
            "annotated as numpy.ndarray; "
            "numpy.ndarray inputs require list, large_list, or fixed-size list "
            "columns."
        )

    if prefers_pylist and not (is_list_like or is_fixed_size_list):
        raise ValueError(
            f"Column has type {array.type} but parameter is annotated as list; "
            "list annotations require list, large_list, or fixed-size list columns."
        )

    if is_list_like:
        list_array = cast("pa.ListArray | pa.LargeListArray", array)
        if prefers_pylist:
            valid = (
                None
                if list_array.null_count == 0
                else list_array.is_valid().to_numpy(zero_copy_only=False)
            )

            def _getter(i: int) -> Any:
                if valid is not None and not valid[i]:
                    return None
                return list_array[i].as_py()

            return _getter

        try:
            values_np = list_array.values.to_numpy(zero_copy_only=False)
            offsets = list_array.offsets.to_numpy(zero_copy_only=False)
        except (pa.ArrowInvalid, pa.ArrowTypeError, NotImplementedError):
            # Fallback to numpy object array per-row when zero-copy path
            # is unavailable (e.g., nested lists)
            valid = (
                None
                if list_array.null_count == 0
                else list_array.is_valid().to_numpy(zero_copy_only=False)
            )

            def _fallback(i: int) -> Any:
                if valid is not None and not valid[i]:
                    return None
                return numpy.array(list_array[i].as_py(), dtype=object)

            return _fallback

        valid = (
            None
            if list_array.null_count == 0
            else list_array.is_valid().to_numpy(zero_copy_only=False)
        )

        def _getter(i: int) -> Any:
            if valid is not None and not valid[i]:
                return None
            start = offsets[i]
            end = offsets[i + 1]
            return values_np[start:end]

        return _getter

    if is_fixed_size_list:
        fsl_array = cast("pa.FixedSizeListArray", array)

        if prefers_pylist:
            valid = (
                None
                if fsl_array.null_count == 0
                else fsl_array.is_valid().to_numpy(zero_copy_only=False)
            )

            def _getter(i: int) -> Any:
                if valid is not None and not valid[i]:
                    return None
                return fsl_array[i].as_py()

            return _getter

        try:
            values_np = fsl_array.values.to_numpy(zero_copy_only=False)
        except (pa.ArrowInvalid, pa.ArrowTypeError, NotImplementedError):
            valid = (
                None
                if fsl_array.null_count == 0
                else fsl_array.is_valid().to_numpy(zero_copy_only=False)
            )

            def _fallback(i: int) -> Any:
                if valid is not None and not valid[i]:
                    return None
                return numpy.array(fsl_array[i].as_py(), dtype=object)

            return _fallback

        list_size = fsl_array.type.list_size  # type: ignore[assignment]
        base_offset = fsl_array.offset

        valid = (
            None
            if fsl_array.null_count == 0
            else fsl_array.is_valid().to_numpy(zero_copy_only=False)
        )

        def _getter(i: int) -> Any:
            if valid is not None and not valid[i]:
                return None
            start = (base_offset + i) * list_size
            end = start + list_size
            return values_np[start:end]

        return _getter

    return lambda i: array[i].as_py()


# Build numpy type mapping - numpy.bool deprecated in 1.x, reintroduced in 2.x
_NUMPY_TYPE_MAP = {
    bool: pa.bool_(),
    bytes: pa.binary(),
    float: pa.float32(),
    int: pa.int64(),
    str: pa.string(),
    numpy.bool_: pa.bool_(),
    numpy.uint8: pa.uint8(),
    numpy.uint16: pa.uint16(),
    numpy.uint32: pa.uint32(),
    numpy.uint64: pa.uint64(),
    numpy.int8: pa.int8(),
    numpy.int16: pa.int16(),
    numpy.int32: pa.int32(),
    numpy.int64: pa.int64(),
    numpy.float16: pa.float16(),
    numpy.float32: pa.float32(),
    numpy.float64: pa.float64(),
    numpy.str_: pa.string(),
}

# Add numpy.bool if available (numpy 2.x)
# In numpy 2.x, numpy.bool is a proper type, not a deprecated alias
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=FutureWarning, message=".*np\\.bool.*")
    warnings.filterwarnings(
        "ignore", category=FutureWarning, message=".*numpy\\.bool.*"
    )
    numpy_bool = getattr(numpy, "bool", None)
    if isinstance(numpy_bool, type):
        _NUMPY_TYPE_MAP[numpy_bool] = pa.bool_()


def _infer_func_arrow_type(func: Callable, input_schema: pa.Schema) -> pa.DataType:
    """Infer the output schema of a UDF

    currently independent of the input schema, in the future we may want to
    infer the output schema based on the input schema, or the UDF itself could
    request the input schema to be passed in.
    """
    if isinstance(func, UDF):
        return func.data_type

    annotations = _get_annotations(func)
    if "return" not in annotations:
        raise ValueError(f"UDF {func} does not have a return type annotation")

    data_type = annotations["return"]
    # do dispatch to handle different types of output types
    # e.g. pydantic -> pyarrow type inference
    if isinstance(data_type, pa.DataType):
        return data_type

    if data_type is numpy.ndarray:
        raise ValueError(
            "UDF return annotation 'numpy.ndarray' cannot be mapped to a PyArrow "
            "type automatically. Please supply 'data_type' explicitly, e.g. "
            "pa.list_(pa.float32()) for a float vector output."
        )

    columns_inner = _columns_annotation_inner(data_type)
    if columns_inner is not None:
        if _is_namedtuple(columns_inner):
            return pa.struct(_namedtuple_to_schema(columns_inner))
        raise ValueError(
            "Columns[T] UDF return annotation currently requires T to be a "
            f"NamedTuple type, got {columns_inner}"
        )

    if t := _NUMPY_TYPE_MAP.get(data_type):
        return t

    raise ValueError(f"UDF {func} has an invalid return type annotation {data_type}")


# ---------------------------------------------------------------------------
# UDTF (User-Defined Table Function)
# ---------------------------------------------------------------------------


@attrs.define
class UDTF:
    """User-Defined Table Function (UDTF) to transform a Geneva Table.

    !!! warning
        This API is in **beta** and may change in future releases.

    Unlike UDFs which operate row-by-row producing a single column, UDTFs can:
    - Access the entire table (or filtered subset)
    - Produce multiple output columns
    - Change the number of rows (filter, expand, aggregate)
    - Perform cross-row operations (e.g., deduplication, clustering)

    The UDTF yields ``pa.RecordBatch`` objects via a generator interface.
    """

    # Required fields first (no defaults)
    func: Callable = attrs.field()
    output_schema: pa.Schema = attrs.field()

    # Optional fields with defaults
    name: str = attrs.field(default="")
    input_columns: list[str] | None = attrs.field(default=None)
    partition_by: str | None = attrs.field(default=None)
    partition_by_indexed_column: str | None = attrs.field(default=None)

    # Resource requirements (for Ray task)
    num_cpus: float | None = attrs.field(
        default=1.0,
        converter=lambda v: None if v is None else float(v),
        validator=valid.optional(valid.ge(0.0)),
    )
    num_gpus: float | None = attrs.field(
        default=0.0,
        converter=lambda v: None if v is None else float(v),
        validator=valid.optional(valid.ge(0.0)),
    )
    memory: int | None = attrs.field(default=None)

    # Execution config
    version: str = attrs.field(default="")
    error_handling: Optional["ErrorHandlingConfig"] = attrs.field(default=None)

    auto_refresh: bool = attrs.field(
        default=False,
        converter=lambda v: v if isinstance(v, bool) else str(v).lower() == "true",
    )

    # Optional GenevaManifest carrying the runtime environment (image, pip
    # deps, env vars). Snapshotted into the view metadata at create time.
    manifest: "GenevaManifest | None" = attrs.field(default=None)

    @manifest.validator  # type: ignore[misc]
    def _validate_manifest(self, _attribute: Any, value: Any) -> None:
        if value is None:
            return
        from geneva.manifest import GenevaManifest

        if not isinstance(value, GenevaManifest):
            raise TypeError(
                f"@udtf(manifest=...) must be a GenevaManifest, got "
                f"{type(value).__name__}"
            )

    def __attrs_post_init__(self) -> None:
        """Initialize UDTF fields after all fields are set."""
        if self.partition_by and self.partition_by_indexed_column:
            raise ValueError(
                "partition_by and partition_by_indexed_column are mutually exclusive"
            )

        # Set default name
        if not self.name:
            if inspect.isclass(self.func) or inspect.isfunction(self.func):
                self.name = self.func.__name__
            elif isinstance(self.func, Callable):
                self.name = self.func.__class__.__name__
            else:
                raise ValueError(
                    f"func must be a class, function, or callable, got {self.func}"
                )

        # Set default version from hash of function
        if not self.version:
            self.version = _func_version_hash(self.func)

    def execute(self, source: Any) -> "Iterator[pa.RecordBatch]":
        """Execute the UDTF, yielding record batches.

        Parameters
        ----------
            source
                Input data source (e.g. GenevaQueryBuilder).

        Raises
        ------
            ValueError
                If the first yielded batch's schema does not match
                ``output_schema``.
        """
        first = True
        for batch in self.func(source):
            if first:
                if batch.schema != self.output_schema:
                    raise ValueError(
                        f"UDTF '{self.name}' output schema mismatch: "
                        f"expected {self.output_schema}, got {batch.schema}"
                    )
                first = False
            yield batch

    @property
    def checkpoint_key(self) -> str:
        """Base checkpoint identifier for the UDTF."""
        return f"udtf:{self.name}:{self.version}"

    def validate_against_schema(self, table_schema: pa.Schema) -> None:
        """Validate input columns exist in table schema."""
        if self.input_columns:
            missing = []
            for col in self.input_columns:
                try:
                    resolve_arrow_field_path(table_schema, col)
                except (KeyError, ValueError):  # noqa: PERF203
                    missing.append(col)
            if missing:
                raise ValueError(
                    f"UDTF '{self.name}' requires columns {missing} which are not "
                    f"found in table. Available columns: {table_schema.names}"
                )


def udtf(
    func: Callable | type | None = None,
    *,
    output_schema: pa.Schema,
    input_columns: list[str] | None = None,
    partition_by: str | None = None,
    partition_by_indexed_column: str | None = None,
    num_cpus: float = 1.0,
    num_gpus: float = 0.0,
    memory: int | None = None,
    version: str = "",
    on_error: "list[ExceptionMatcher] | ErrorHandlingConfig | None" = None,
    manifest: "GenevaManifest | None" = None,
    auto_refresh: bool = False,
) -> UDTF | functools.partial:
    """Decorator to create a User-Defined Table Function (UDTF).

    !!! warning
        This API is in **beta** and may change in future releases.

    A UDTF transforms a Geneva table into another table. Unlike UDFs which
    operate row-by-row, UDTFs can perform cross-row operations like
    deduplication, clustering, or aggregation.

    Parameters
    ----------
    func : Callable | type
        The function or class to be decorated. Must implement
        ``__call__(self, source) -> Iterator[pa.RecordBatch]``.
    output_schema : pa.Schema
        The PyArrow schema for the output table (required).
    input_columns : list[str], optional
        Columns required from source table. If None, the UDTF can access
        all columns.
    partition_by : str, optional
        Column name for parallel partition execution via Ray actors.
        Each distinct value of this column is processed independently.
    partition_by_indexed_column : str, optional
        Column name that has an existing IVF vector index to dispatch
        partitions from.  Works with any IVF-family index (IVF_FLAT,
        IVF_PQ, IVF_HNSW_SQ, etc.).  Mutually exclusive with
        ``partition_by``.
    num_cpus : float, optional
        Number of CPUs to request for the Ray task. Default 1.0.
    num_gpus : float, optional
        Number of GPUs to request for the Ray task. Default 0.0.
    memory : int, optional
        Memory in bytes to request for the Ray task.
    version : str, optional
        Version string for cache invalidation. If not provided, uses
        hash of the serialized function.
    on_error : list[ExceptionMatcher] | ErrorHandlingConfig, optional
        Error handling configuration for the UDTF.

    Examples
    --------
    Class-based UDTF::

        @geneva.udtf(
            output_schema=pa.schema([
                pa.field("row_id", pa.int64()),
                pa.field("cluster_id", pa.int64()),
                pa.field("duplicate_row_ids", pa.list_(pa.int64())),
            ]),
            input_columns=["row_id", "phash"],
        )
        class PHashIvfFlatHammingDedupe:
            def __init__(self, threshold: int = 4):
                self.threshold = threshold

            def __call__(self, source) -> Iterator[pa.RecordBatch]:
                tbl = source.to_arrow()
                # ... compute clusters ...
                yield pa.RecordBatch.from_pydict({...})

    Function-based UDTF::

        @geneva.udtf(
            output_schema=pa.schema([...]),
            input_columns=["row_id", "text"],
        )
        def compute_scores(source, model_name: str = "default"):
            for batch in source.to_batches():
                result = process(batch)
                yield result
    """
    # Normalize error handling
    effective_error_handling: ErrorHandlingConfig | None = None
    if isinstance(on_error, list):
        from geneva.debug.error_store import resolve_on_error

        effective_error_handling = resolve_on_error(on_error)
    elif on_error is not None:
        effective_error_handling = on_error

    if inspect.isclass(func):
        # Decorator used on a class: @udtf(...) class Foo
        @functools.wraps(func)
        def _class_wrapper(*args, **kwargs) -> UDTF:
            # When instantiated, return a UDTF with the class as func
            # but with kwargs captured for later execution
            callable_obj = func(*args, **kwargs)
            return UDTF(
                func=callable_obj,
                output_schema=output_schema,
                input_columns=input_columns,
                partition_by=partition_by,
                partition_by_indexed_column=partition_by_indexed_column,
                num_cpus=num_cpus,
                num_gpus=num_gpus,
                memory=memory,
                version=version,
                error_handling=effective_error_handling,
                manifest=manifest,
                auto_refresh=auto_refresh,
            )

        # Also make the wrapper callable directly as a UDTF
        # so @udtf(...) class Foo can be used as Foo() or Foo(threshold=4)
        return _class_wrapper  # type: ignore

    if func is None:
        # Decorator with arguments: @udtf(output_schema=...)
        return functools.partial(
            udtf,
            output_schema=output_schema,
            input_columns=input_columns,
            partition_by=partition_by,
            partition_by_indexed_column=partition_by_indexed_column,
            num_cpus=num_cpus,
            num_gpus=num_gpus,
            memory=memory,
            version=version,
            on_error=on_error,
            manifest=manifest,
            auto_refresh=auto_refresh,
        )

    # Decorator without parentheses or function passed directly
    return UDTF(
        func=func,
        output_schema=output_schema,
        input_columns=input_columns,
        partition_by=partition_by,
        partition_by_indexed_column=partition_by_indexed_column,
        num_cpus=num_cpus,
        num_gpus=num_gpus,
        memory=memory,
        version=version,
        error_handling=effective_error_handling,
        manifest=manifest,
        auto_refresh=auto_refresh,
    )


def batch_udtf(
    func: Callable | type | None = None,
    **kwargs: Any,
) -> UDTF | functools.partial:
    """Alias for [`udtf`][geneva.udtf] — the N:M batch UDTF variant.

    !!! warning
        This API is in **beta** and may change in future releases.

    Takes an entire table/partition as input and yields RecordBatches.
    Use ``@chunker`` instead for per-row 1:N expansion.

    See Also
    --------
    [`Connection.create_udtf_view`][geneva.db.Connection.create_udtf_view] :
    Apply a batch UDTF to a table.
    """
    return udtf(func, **kwargs)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Scalar UDTF (1:N Row Expansion)
# ---------------------------------------------------------------------------


def _infer_output_schema_from_return_type(func: Callable) -> pa.Schema:
    """Infer the output pa.Schema from the return type annotation of a scalar UDTF.

    Supports:
    - Iterator[NamedTuple] / Generator[NamedTuple, ...]
    - list[NamedTuple]
    - Iterator[dict] (requires explicit schema)

    Raises ValueError if the schema cannot be inferred.
    """
    hints = get_type_hints(func)
    ret = hints.get("return")
    if ret is None:
        raise ValueError(
            f"chunker '{func.__name__}' must have a return type annotation "
            "(e.g., Iterator[MyNamedTuple])."
        )

    origin = get_origin(ret)

    # Unwrap Iterator[X], Generator[X, ...], or list[X]
    inner = None
    if origin is Iterator or origin is typing.Generator or origin is list:
        args = get_args(ret)
        if args:
            inner = args[0]
    else:
        inner = ret

    if inner is None:
        raise ValueError(
            f"chunker '{func.__name__}': cannot infer output schema from "
            f"return type {ret}. Use Iterator[NamedTuple] or provide "
            "output_schema explicitly."
        )

    # Check if inner is a NamedTuple
    if _is_namedtuple(inner):
        return _namedtuple_to_schema(inner)

    raise ValueError(
        f"chunker '{func.__name__}': cannot infer output schema from "
        f"type {inner}. Use a NamedTuple as the yield type or provide "
        "output_schema explicitly."
    )


def _is_namedtuple(cls: type) -> bool:
    """Check if a type is a NamedTuple."""
    return (
        isinstance(cls, type)
        and issubclass(cls, tuple)
        and hasattr(cls, "_fields")
        and hasattr(cls, "__annotations__")
    )


# Mapping from Python types to PyArrow types for NamedTuple field inference
_PYTHON_TO_ARROW_TYPE: dict[type, pa.DataType] = {
    int: pa.int64(),
    float: pa.float64(),
    str: pa.utf8(),
    bool: pa.bool_(),
    bytes: pa.binary(),
}


def _python_type_to_arrow(py_type: type) -> pa.DataType:
    """Convert a Python type annotation to a PyArrow DataType."""
    # Handle Optional[X] -> X
    origin = get_origin(py_type)
    if origin is Union or origin is UnionType:
        args = [a for a in get_args(py_type) if a is not NoneType]
        if len(args) == 1:
            return _python_type_to_arrow(args[0])

    if py_type in _PYTHON_TO_ARROW_TYPE:
        return _PYTHON_TO_ARROW_TYPE[py_type]

    # Handle list[X] -> pa.list_(X)
    if origin is list:
        args = get_args(py_type)
        if args:
            return pa.list_(_python_type_to_arrow(args[0]))
        return pa.list_(pa.utf8())  # fallback

    raise ValueError(
        f"Cannot convert Python type {py_type} to PyArrow type. "
        "Provide output_schema explicitly."
    )


def _namedtuple_to_schema(nt_cls: type) -> pa.Schema:
    """Convert a NamedTuple class to a pa.Schema."""
    hints = get_type_hints(nt_cls)
    fields = []
    for field_name in nt_cls._fields:  # type: ignore[attr-defined]
        py_type = hints.get(field_name)
        if py_type is None:
            raise ValueError(
                f"NamedTuple field '{field_name}' has no type annotation. "
                "All fields must be annotated for schema inference."
            )
        arrow_type = _python_type_to_arrow(py_type)
        fields.append(pa.field(field_name, arrow_type))
    return pa.schema(fields)


@attrs.define
class Chunker:
    """Scalar User-Defined Table Function for 1:N row expansion.

    !!! warning
        This API is in **beta** and may change in future releases.

    Unlike batch UDTFs which operate on entire tables/partitions, scalar UDTFs
    operate per-row: for each input row, the function yields zero or more
    output rows. Input columns are bound by parameter name (same as UDFs).

    The function should be a generator that yields NamedTuples, dicts, or tuples.
    """

    func: Callable = attrs.field()
    output_schema: pa.Schema = attrs.field()

    # Whether this is the batched variant (takes Arrow Arrays, returns RecordBatch)
    batch: bool = attrs.field(default=False)

    name: str = attrs.field(default="")
    input_columns: list[str] | None = attrs.field(default=None)

    # Whether the input columns are copied into the output view. Input columns
    # are always fetched to run the chunker; when False they are not written to
    # each output row, avoiding duplication of large inputs (e.g. video/audio
    # bytes) across every expanded row. Defaults to False because chunkers
    # typically split a large input into many rows, so copying the input onto
    # each row is rarely wanted; set True to carry the inputs through.
    inherit_input_columns: bool = attrs.field(default=False)

    # Resource requirements
    num_cpus: float | None = attrs.field(
        default=1.0,
        converter=lambda v: None if v is None else float(v),
        validator=valid.optional(valid.ge(0.0)),
    )
    num_gpus: float | None = attrs.field(
        default=0.0,
        converter=lambda v: None if v is None else float(v),
        validator=valid.optional(valid.ge(0.0)),
    )
    memory: int | None = attrs.field(default=None)

    # Execution config
    version: str = attrs.field(default="")
    error_handling: Optional["ErrorHandlingConfig"] = attrs.field(default=None)

    auto_refresh: bool = attrs.field(
        default=False,
        converter=lambda v: v if isinstance(v, bool) else str(v).lower() == "true",
    )

    # Optional GenevaManifest carrying the runtime environment (image, pip
    # deps, env vars). Snapshotted into the view metadata at create time.
    manifest: "GenevaManifest | None" = attrs.field(default=None)

    @manifest.validator  # type: ignore[misc]
    def _validate_manifest(self, _attribute: Any, value: Any) -> None:
        if value is None:
            return
        from geneva.manifest import GenevaManifest

        if not isinstance(value, GenevaManifest):
            raise TypeError(
                f"@chunker(manifest=...) must be a GenevaManifest, got "
                f"{type(value).__name__}"
            )

    # Backwards-compatible deserialization: a Chunker is cloudpickled whole
    # into the materialized-view metadata (see marshal_chunker), so a view
    # created before a field was added unpickles into the current slotted
    # class with that slot unset. Return the attrs default so old views still
    # refresh, and keep future field additions backward-compatible.
    _FIELD_DEFAULTS: ClassVar[dict[str, Any]] = {
        "inherit_input_columns": False,
    }

    def __getattr__(self, name: str) -> Any:
        defaults = object.__getattribute__(self, "_FIELD_DEFAULTS")
        if name in defaults:
            return defaults[name]
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute {name!r}"
        )

    def __getstate__(self) -> dict[str, Any]:
        """Serialize compatibly across optional slot additions."""
        state: dict[str, Any] = {}
        for field in attrs.fields(self.__class__):
            if hasattr(self, field.name):
                state[field.name] = getattr(self, field.name)
            else:
                state[field.name] = _field_default_value(field, self)
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        """Restore state while filling newer optional fields with defaults.

        Pickle restore bypasses attrs converters and __attrs_post_init__; this
        only backfills fields missing from older payloads with their defaults.
        """
        for field in attrs.fields(self.__class__):
            if field.name in state:
                value = state[field.name]
            else:
                value = _field_default_value(field, self)
            object.__setattr__(self, field.name, value)

    def __attrs_post_init__(self) -> None:
        if not self.name:
            if inspect.isfunction(self.func):
                self.name = self.func.__name__
            elif isinstance(self.func, Callable):
                self.name = self.func.__class__.__name__
            else:
                raise ValueError(
                    f"func must be a function or callable, got {self.func}"
                )

        if self.input_columns is None:
            sig = inspect.signature(self.func)
            self.input_columns = [p for p in sig.parameters if p != "__source_row_id"]

        if not self.version:
            self.version = _func_version_hash(self.func)

    def execute_on_record_batch(self, record_batch: pa.RecordBatch) -> pa.RecordBatch:
        """Execute the scalar UDTF on a record batch, expanding rows 1:N.

        For each row in the input batch, calls the function and collects
        all yielded output rows. Returns a single RecordBatch containing
        all expanded rows with ``__source_row_id`` and ``__child_index`` columns.

        This is a thin wrapper over :meth:`execute_on_record_batch_iter` with
        no output bound, preserving the historical single-batch return.

        Parameters
        ----------
        record_batch : pa.RecordBatch
            Input batch. Must contain a ``__source_row_id`` column.

        Returns
        -------
        pa.RecordBatch
            Expanded output with ``__source_row_id``, ``__child_index``,
            and all columns from the output schema.
        """
        batches = list(self.execute_on_record_batch_iter(record_batch, max_rows=None))
        if len(batches) == 1:
            return batches[0]
        if not batches:
            return pa.RecordBatch.from_pydict(
                {
                    f.name: pa.array([], type=f.type)
                    for f in self.expanded_output_schema
                },
                schema=self.expanded_output_schema,
            )
        return (
            pa.Table.from_batches(batches, schema=self.expanded_output_schema)
            .combine_chunks()
            .to_batches()[0]
        )

    def execute_on_record_batch_iter(
        self,
        record_batch: pa.RecordBatch,
        max_rows: int | None = None,
    ) -> Iterator[pa.RecordBatch]:
        """Execute the scalar UDTF, streaming bounded sub-batches.

        Yields output sub-batches each holding at most ``max_rows`` rows so
        that peak memory is bounded regardless of how large the full expansion
        would be. Flushing happens on a *source-row boundary* — one source
        row's children are never split across sub-batches — which keeps
        ``__child_index`` contiguous per source row. Empty sub-batches are
        never yielded.

        Parameters
        ----------
        record_batch : pa.RecordBatch
            Input batch. Must contain a ``__source_row_id`` column.
        max_rows : int | None
            Maximum output rows per yielded sub-batch. ``None`` means no bound
            (the whole expansion is yielded as a single sub-batch).

        Yields
        ------
        pa.RecordBatch
            Expanded output sub-batches with ``__source_row_id``,
            ``__child_index``, and all columns from the output schema.
        """
        if self.batch:
            yield from self._execute_batch_iter(record_batch, max_rows)
        else:
            yield from self._execute_scalar_iter(record_batch, max_rows)

    def _execute_scalar_iter(
        self,
        record_batch: pa.RecordBatch,
        max_rows: int | None,
    ) -> Iterator[pa.RecordBatch]:
        """Per-row execution, yielding ``<= max_rows`` sub-batches."""
        input_cols = cast("list[str]", self.input_columns)
        annotations = _get_annotations(self.func)
        sig = inspect.signature(self.func)
        params = list(sig.parameters.values())

        # Build value accessors (same pattern as UDF._scalar_func_record_batch_call)
        accessors = []
        for idx, col in enumerate(input_cols):
            param = params[idx] if idx < len(params) else None
            expected_type = annotations.get(param.name) if param else None
            accessors.append(
                _make_value_accessor(
                    _get_array_from_record_batch(record_batch, col),
                    expected_type,
                )
            )

        # Get source row IDs
        source_row_ids = record_batch["__source_row_id"]

        # Resolve error handling strategy
        skip_on_error = False
        if self.error_handling is not None:
            from geneva.debug.error_store import FaultIsolation

            skip_on_error = (
                self.error_handling.fault_isolation == FaultIsolation.SKIP_ROWS
            )

        # Accumulators for the current sub-batch.
        all_source_row_ids: list[int] = []
        all_child_indices: list[int] = []
        output_cols: dict[str, list] = {field.name: [] for field in self.output_schema}

        def build_sub_batch() -> pa.RecordBatch:
            arrays: dict[str, pa.Array] = {
                "__source_row_id": pa.array(all_source_row_ids, type=pa.int64()),
                "__child_index": pa.array(all_child_indices, type=pa.int32()),
            }
            for field in self.output_schema:
                arrays[field.name] = pa.array(output_cols[field.name], type=field.type)
            return pa.RecordBatch.from_pydict(
                arrays, schema=self.expanded_output_schema
            )

        def reset() -> None:
            all_source_row_ids.clear()
            all_child_indices.clear()
            for col in output_cols.values():
                col.clear()

        for row_idx in range(record_batch.num_rows):
            args = [accessor(row_idx) for accessor in accessors]
            src_row_id = source_row_ids[row_idx].as_py()

            try:
                for child_index, result in enumerate(self.func(*args)):
                    all_source_row_ids.append(src_row_id)
                    all_child_indices.append(child_index)

                    if hasattr(result, "_asdict"):
                        d = result._asdict()
                        for field in self.output_schema:
                            output_cols[field.name].append(d[field.name])
                    elif isinstance(result, dict):
                        for field in self.output_schema:
                            output_cols[field.name].append(result[field.name])
                    else:
                        for i, field in enumerate(self.output_schema):
                            output_cols[field.name].append(result[i])
            except Exception:
                if skip_on_error:
                    _LOG.warning(
                        "chunker '%s': skipping source row %d due to error",
                        self.name,
                        src_row_id,
                        exc_info=True,
                    )
                    continue
                raise

            # Flush on a source-row boundary once the bound is reached.
            if (
                max_rows is not None
                and max_rows > 0
                and len(all_source_row_ids) >= max_rows
            ):
                yield build_sub_batch()
                reset()

        # Always emit the final accumulator. When the input produced no output
        # rows and nothing was flushed, this yields a single empty batch so the
        # non-streaming wrapper can return an empty result with the right schema.
        if all_source_row_ids or record_batch.num_rows == 0:
            yield build_sub_batch()
        elif max_rows is None:
            # max_rows is None means callers expect exactly one batch even when
            # every source row yielded zero outputs.
            yield build_sub_batch()

    def _execute_batch_iter(
        self,
        record_batch: pa.RecordBatch,
        max_rows: int | None,
    ) -> Iterator[pa.RecordBatch]:
        """Batched execution with bounded peak memory.

        The input is sliced into ``<= max_rows`` source-row chunks and the batch
        ``func`` is invoked once per chunk, so peak memory is bounded by a single
        chunk's expansion rather than the full input's. Each chunk's result is
        then sliced into ``<= max_rows`` output sub-batches for bounded fragment
        writes. ``max_rows`` is ``None`` (or ``<= 0``) means no bound: the whole
        input is expanded in one call and yielded as is.

        In batch mode every input row is one source row, so slicing the input on
        a row boundary never splits a source row; ``__child_index`` (numbered per
        ``__source_row_id`` within each call) is therefore identical to the
        single-shot expansion.
        """
        if max_rows is None or max_rows <= 0 or record_batch.num_rows == 0:
            yield self._execute_batch(record_batch)
            return

        for in_start in range(0, record_batch.num_rows, max_rows):
            result_batch = self._execute_batch(record_batch.slice(in_start, max_rows))
            if result_batch.num_rows <= max_rows:
                yield result_batch
                continue
            for start in range(0, result_batch.num_rows, max_rows):
                yield result_batch.slice(start, max_rows)

    def _execute_batch(self, record_batch: pa.RecordBatch) -> pa.RecordBatch:
        """Batched execution: pass Arrow Arrays to func, get RecordBatch back."""
        input_cols = cast("list[str]", self.input_columns)

        # Build kwargs with Arrow Arrays keyed by column name
        kwargs: dict[str, pa.Array] = {}
        for col in input_cols:
            kwargs[col] = _get_array_from_record_batch(record_batch, col)

        # Also pass __source_row_id so the batch function can map outputs
        kwargs["__source_row_id"] = record_batch["__source_row_id"]

        result_batch = self.func(**kwargs)

        # Validate output has required columns
        if "__source_row_id" not in result_batch.schema.names:
            raise ValueError(
                f"chunker(batch=True) '{self.name}' must include "
                "'__source_row_id' in output to map expanded rows to inputs."
            )

        # Add __child_index if not present (auto-generate per source_row_id).
        # Note: rows for the same source_row_id must be contiguous in the
        # output; interleaved output will restart the child index counter.
        if "__child_index" not in result_batch.schema.names:
            src_ids = result_batch["__source_row_id"].to_pylist()
            child_indices = []
            counters: dict[int, int] = {}
            for sid in src_ids:
                idx = counters.get(sid, 0)
                child_indices.append(idx)
                counters[sid] = idx + 1
            result_batch = result_batch.append_column(
                pa.field("__child_index", pa.int32()),
                pa.array(child_indices, type=pa.int32()),
            )

        return result_batch

    @property
    def checkpoint_key(self) -> str:
        return f"chunker:{self.name}:{self.version}"

    @property
    def expanded_output_schema(self) -> pa.Schema:
        """Output schema including __source_row_id and __child_index."""
        return pa.schema(
            [
                pa.field("__source_row_id", pa.int64()),
                pa.field("__child_index", pa.int32()),
            ]
            + list(self.output_schema)
        )


def chunker(
    func: Callable | None = None,
    *,
    output_schema: pa.Schema | None = None,
    batch: bool = False,
    input_columns: list[str] | None = None,
    inherit_input_columns: bool = False,
    num_cpus: float = 1.0,
    num_gpus: float = 0.0,
    memory: int | None = None,
    version: str = "",
    on_error: "list[ExceptionMatcher] | ErrorHandlingConfig | None" = None,
    manifest: "GenevaManifest | None" = None,
    auto_refresh: bool = False,
) -> Chunker | functools.partial:
    """Decorator to create a chunker for 1:N row expansion.

    !!! warning
        This API is in **beta** and may change in future releases.

    A scalar UDTF operates per-row: for each input row, it yields zero or
    more output rows. Input columns are bound by parameter name (same as UDFs).

    Parameters
    ----------
    func : Callable
        The generator function. Parameters map to input columns by name.
        Return type should be ``Iterator[NamedTuple]``.
    output_schema : pa.Schema, optional
        Output schema. If not provided, inferred from the return type
        annotation (must be a NamedTuple).
    batch : bool
        If True, the function receives Arrow Arrays and returns a
        RecordBatch (vectorized variant). Default False.
    input_columns : list[str], optional
        Input column names. If not provided, inferred from function
        parameter names.
    inherit_input_columns : bool
        Whether to copy the input columns into the output view. Input columns
        are always fetched to run the chunker; when False they are kept out of
        each output row, avoiding duplication of large inputs (e.g. video or
        audio bytes). Default False; set True to carry the inputs through to
        every expanded row.
    num_cpus : float
        CPUs per Ray task. Default 1.0.
    num_gpus : float
        GPUs per Ray task. Default 0.0.
    memory : int, optional
        Memory in bytes per Ray task.
    version : str, optional
        Version string for cache invalidation.
    on_error : list[ExceptionMatcher] | ErrorHandlingConfig, optional
        Error handling configuration.

    Examples
    --------
    Generator-based scalar UDTF::

        from typing import Iterator, NamedTuple

        class Clip(NamedTuple):
            clip_start: float
            clip_end: float

        @chunker
        def extract_clips(duration: float) -> Iterator[Clip]:
            for start in range(0, int(duration), 10):
                yield Clip(clip_start=start, clip_end=min(start + 10, duration))

    Batched scalar UDTF::

        @chunker(batch=True, output_schema=clip_schema)
        def extract_clips(
            duration: pa.Array,
            __source_row_id: pa.Array,
        ) -> pa.RecordBatch:
            # Return expanded RecordBatch with __source_row_id
            ...

    See Also
    --------
    [`Connection.create_udtf_view`][geneva.db.Connection.create_udtf_view]
    : Apply a scalar UDTF to a table.
    """
    # Resolve error handling
    effective_error_handling: ErrorHandlingConfig | None = None
    if isinstance(on_error, list):
        from geneva.debug.error_store import resolve_on_error

        effective_error_handling = resolve_on_error(on_error)
    elif on_error is not None:
        effective_error_handling = on_error

    if func is None:
        return functools.partial(
            chunker,
            output_schema=output_schema,
            batch=batch,
            input_columns=input_columns,
            inherit_input_columns=inherit_input_columns,
            num_cpus=num_cpus,
            num_gpus=num_gpus,
            memory=memory,
            version=version,
            on_error=on_error,
            manifest=manifest,
            auto_refresh=auto_refresh,
        )

    # Infer output_schema from return type if not provided
    if output_schema is None:
        output_schema = _infer_output_schema_from_return_type(func)

    return Chunker(
        func=func,
        output_schema=output_schema,
        batch=batch,
        input_columns=input_columns,
        inherit_input_columns=inherit_input_columns,
        num_cpus=num_cpus,
        num_gpus=num_gpus,
        memory=memory,
        version=version,
        error_handling=effective_error_handling,
        manifest=manifest,
        auto_refresh=auto_refresh,
    )
