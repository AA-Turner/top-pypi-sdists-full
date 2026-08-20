#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import base64
import hashlib
import inspect
import json
import sys
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
from pyspark.errors.exceptions.base import AnalysisException

import snowflake.snowpark.functions as snowpark_fn
import snowflake.snowpark_connect.tcm as tcm
import snowflake.snowpark_connect.utils.udf_utils as udf_utils
from snowflake.snowpark import Session
from snowflake.snowpark.types import (
    ArrayType,
    DataType,
    MapType,
    StructType,
    VariantType,
    _parse_datatype_json_value,
)
from snowflake.snowpark_connect.column_name_handler import ColumnNameMap
from snowflake.snowpark_connect.config import (
    global_config,
    is_force_create_sproc_enabled,
)
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.expression.map_expression import (
    map_single_column_expression,
)
from snowflake.snowpark_connect.expression.map_unresolved_star import (
    map_unresolved_star_as_single_column,
)
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.typed_column import TypedColumn
from snowflake.snowpark_connect.utils.concurrent import SynchronizedDict
from snowflake.snowpark_connect.utils.context import (
    get_is_aggregate_function,
    get_is_evaluating_join_condition,
)
from snowflake.snowpark_connect.utils.jvm_udf_utils import (
    UdfKind,
    decode_jvm_udf_result,
    encode_jvm_udf_args,
    is_decomposable_struct,
)
from snowflake.snowpark_connect.utils.scala_udf_utils import _emit_scala_udf_ddl
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

CREATE_UDF_SPROC_NAME_PREFIX = "__SC_BUILD_IN_CREATE_UDF"


def _invoke_udf(
    udf: "SnowparkUdfBase",
    converted_args: list["snowpark_fn.Column"],
    typed_args: list[TypedColumn],
    override_name: str | None = None,
) -> "snowpark_fn.Column":
    """Append the schema-JSON sentinel (if needed) and return call_udf(...)."""
    from snowflake.snowpark_connect.utils.jvm_udf_utils import to_json

    if udf.kind in (UdfKind.SCALA_UDF, UdfKind.PYTHON_REGISTERED):
        schema_json = to_json([t.typ for t in typed_args], escape_quotes=False)
        converted_args.append(snowpark_fn.lit(schema_json))
    return snowpark_fn.call_udf(override_name or udf.name, *converted_args)


@dataclass
class SnowparkUdfBase(ABC):
    """Abstract base for all Snowflake UDF handles.

    Subclasses represent either an already-created UDF (``SnowparkUDF``) or a
    lazily-created one whose DDL is deferred until the first call site
    (``LazySnowparkUdf``).
    """

    name: str
    return_type: DataType
    original_return_type: DataType | None
    kind: UdfKind
    cast_to_original_return_type: bool

    @abstractmethod
    def _call(
        self,
        converted_args: list["snowpark_fn.Column"],
        typed_args: list[TypedColumn],
        session: Session,
    ) -> "snowpark_fn.Column":
        """Invoke the UDF with already-encoded arguments and return the raw column.

        ``converted_args`` must already contain the per-argument columns (with any
        struct decomposition / VARIANT / epoch encoding applied). ``typed_args`` is the
        original list used to derive the schema-JSON sentinel when ``attach_schema_json``
        is set. This is the low-level primitive; callers use ``invoke``.
        """

    def decomposes_struct_arg(self, position: int, call_site_type: DataType) -> bool:
        """Whether the ``position``-th struct argument is split into per-field columns.

        Callers must keep struct decomposition in lockstep with the generated DDL: a
        struct arg is expanded into N native/VARIANT per-field columns only when the
        function was *created* with a decomposed parameter list; otherwise the whole
        struct is passed as a single VARIANT.  The default follows the call-site type,
        which is correct for UDFs whose DDL is emitted lazily from call-site types.
        """
        return is_decomposable_struct(call_site_type)

    def effective_return_type_for(self, call_site_types: list[DataType]) -> DataType:
        """The DDL return type for these call-site types.

        Lazy Scala UDFs infer a narrower type at DDL-emission time (e.g. DECIMAL(18,4)
        instead of DECIMAL(38,18)); every other handle uses the declared return type.
        Overridden by ``LazySnowparkUdf``.
        """
        return self.original_return_type

    def invoke(
        self,
        typed_args: list[TypedColumn],
        column_mapping: ColumnNameMap,
        session: Session,
    ) -> TypedColumn:
        """Encode arguments, invoke the UDF, and decode the result to its declared type.

        The single public entry point: the UDF handle owns its full marshalling, so both
        call sites (inline ``map_udf`` and registered-SQL ``map_unresolved_function``)
        share one path with no external branching. Returns the result as a ``TypedColumn``
        (column paired with its Spark type).

        The marshalling contract is selected by ``self.kind`` (see ``UdfKind``):
          * ``SCALA_UDF/JAVA_UDAF``: ``encode_jvm_udf_args`` lowers temporals to epoch /
            wraps non-native args in VARIANT; ``decode_jvm_udf_result`` reconstructs the
            declared type on return (epoch → temporal, else cast).
          * ``PYTHON_REGISTERED/JAVA_SCALAR``: args cast to VARIANT; a VARIANT-backed
            return is cast back.
          * ``PYTHON_INLINE``: args pass through; a VARIANT-backed Map/Struct return is
            reconstructed via ``PARSE_JSON`` then cast.
          * ``NATIVE_FUNCTION``: no boundary; args pass through and the result is cast to
            the declared return type.
        """
        match self.kind:
            case UdfKind.SCALA_UDF | UdfKind.JAVA_UDAF:
                args: list = encode_jvm_udf_args(self, typed_args, column_mapping)
            case UdfKind.PYTHON_REGISTERED | UdfKind.JAVA_SCALAR:
                args = [snowpark_fn.cast(tc.col, VariantType()) for tc in typed_args]
            case UdfKind.PYTHON_INLINE | UdfKind.NATIVE_FUNCTION:
                args = [tc.col for tc in typed_args]

        raw = self._call(args, typed_args, session)

        if not self.cast_to_original_return_type:
            return TypedColumn(raw, lambda: [self.return_type])
        rt = self.effective_return_type_for([tc.typ for tc in typed_args])
        match self.kind:
            case UdfKind.SCALA_UDF | UdfKind.JAVA_UDAF:
                col = decode_jvm_udf_result(raw, rt)
            case UdfKind.PYTHON_REGISTERED | UdfKind.JAVA_SCALAR:
                col = snowpark_fn.cast(raw, rt)
            case UdfKind.NATIVE_FUNCTION:
                # Intentionally separate from PYTHON_REGISTERED/JAVA_SCALAR: native
                # functions never go through the VARIANT boundary, so if that branch
                # later adds VARIANT unwrapping, this one must stay a plain cast.
                col = snowpark_fn.cast(raw, rt)
            case UdfKind.PYTHON_INLINE:
                col = snowpark_fn.parse_json(raw).cast(rt)
        return TypedColumn(col, lambda: [rt])


@dataclass
class SnowparkUDF(SnowparkUdfBase):
    input_types: list[DataType]

    def _call(
        self,
        converted_args: list["snowpark_fn.Column"],
        typed_args: list[TypedColumn],
        session: Session,
    ) -> "snowpark_fn.Column":
        return _invoke_udf(self, converted_args, typed_args)

    def decomposes_struct_arg(self, position: int, call_site_type: DataType) -> bool:
        # Eager UDF: the DDL is fixed at creation from the declared input_types, so
        # decomposition must follow the *declared* type — not the call-site type, which
        # may be a concrete struct even when the UDF was registered with an untyped /
        # VARIANT input (e.g. spark.udf.register of a Row => ... closure). Using the
        # call-site type here would emit N decomposed args against a 1-param VARIANT DDL.
        declared = (
            self.input_types[position] if position < len(self.input_types) else None
        )
        return is_decomposable_struct(declared)


@dataclass
class NativeFunctionUdf(SnowparkUdfBase):
    """Handle that forwards a registered name to a native Snowflake function.

    Backs native function passthrough: a ``snowpark.connect.nativeFunction.<name>`` config
    entry names a Snowflake built-in or a pre-existing UDF, and calls to ``<name>`` are
    rewritten to invoke that function directly. No Python is ever executed and no Snowflake
    object is created.

    Two invariants that differ from every other handle:

    * The Snowflake function lives in ``target``, **not** in ``name``. Everywhere else
      ``name`` is a physical function SCOS created and may ``DROP``; here it is only the
      logical Spark-side name. Keeping the two apart means a stray ``DROP FUNCTION`` can
      never reach the user's own permanent UDF. ``DropFunctionCommand`` additionally
      short-circuits on this type.
    * ``input_types`` is always empty, mirroring ``LazyUdfBase``. Nothing on the invoke
      path reads it -- arguments come from the call site, and with no DDL of our own there
      is no signature to coerce them to; Snowflake resolves the overload. Leaving it empty
      also keeps ``DropFunctionCommand``'s "was DDL emitted?" check false. It exists at all
      because that check reads the attribute.
    * ``declaration`` records the exact config value this handle was built from, so a
      lookup can tell whether it is still current. Config is the source of truth and can be
      re-set or unset at any time, and there is no hook that fires on either, so a handle
      cached without this would keep answering for a declaration the user has already
      changed -- silently calling the wrong Snowflake function.
    """

    target: str
    declaration: str
    input_types: list[DataType] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        assert self.kind is UdfKind.NATIVE_FUNCTION

    def _call(
        self,
        converted_args: list["snowpark_fn.Column"],
        typed_args: list[TypedColumn],
        session: Session,
    ) -> "snowpark_fn.Column":
        return snowpark_fn.call_function(self.target, *converted_args)

    def decomposes_struct_arg(self, position: int, call_site_type: DataType) -> bool:
        # There is no generated DDL to stay in lockstep with: a struct argument is passed
        # to the native function as-is.
        return False


@dataclass
class LazyUdfBase(SnowparkUdfBase):
    """Shared skeleton for UDFs whose CREATE FUNCTION DDL is deferred to the first call.

    One physical Snowflake function is emitted per distinct call-site type signature (the
    first reuses the base name; later ones get a short type-hash suffix). Subclasses
    implement ``_emit_ddl`` (the actual CREATE FUNCTION) and may override
    ``_invoke_materialized`` to control how a materialized function is called.

    ORDERING CONTRACT: ``_emit_ddl`` MUST populate every per-signature map it owns
    (return-type overrides, encoding flags, name->types, ...) BEFORE writing the
    ``_type_to_name`` gate. ``_call`` and per-signature reads (e.g.
    ``effective_return_type_for``) consult those maps lock-free once the gate shows the
    key, so the gate must become visible last.
    """

    # Written for structural symmetry with SnowparkUDF; not read on the lazy path
    # (decomposes_struct_arg follows the call-site type).
    input_types: list[DataType] = field(default_factory=list, init=False)
    # repr(call_site_types) -> materialized physical function name for that signature.
    _type_to_name: SynchronizedDict = field(
        default_factory=SynchronizedDict, init=False, repr=False
    )
    # materialized name -> that function's PHYSICAL parameter types (for DropFunctionCommand
    # to emit a DROP FUNCTION with the exact signature).
    _name_to_types: dict = field(default_factory=dict, init=False, repr=False)
    # Guards the check+emit+set critical section; _type_to_name gives read-safety for the
    # outer fast-path gate.
    _ddl_lock: "threading.Lock" = field(
        default_factory=threading.Lock, init=False, repr=False
    )

    def _next_udf_name(self, type_key: str) -> str:
        """Physical name for a signature: base name for the first, hashed suffix after."""
        if not self._type_to_name:
            return self.name
        suffix = hashlib.md5(type_key.encode()).hexdigest()[:8]
        return f"{self.name}_{suffix}"

    def _call(
        self,
        converted_args: list["snowpark_fn.Column"],
        typed_args: list[TypedColumn],
        session: Session,
    ) -> "snowpark_fn.Column":
        call_site_types = [tc.typ for tc in typed_args]
        type_key = repr(call_site_types)
        if type_key not in self._type_to_name:
            with self._ddl_lock:
                if type_key not in self._type_to_name:
                    self._emit_ddl(call_site_types, session, type_key)
        return self._invoke_materialized(
            self._type_to_name[type_key], converted_args, typed_args, type_key
        )

    def _invoke_materialized(
        self,
        name: str,
        converted_args: list["snowpark_fn.Column"],
        typed_args: list[TypedColumn],
        type_key: str,
    ) -> "snowpark_fn.Column":
        """Call the materialized physical function.

        Default: the base ``_invoke_udf`` (appends the schema-JSON sentinel by kind).
        Overridden by ``LazyPythonUdf`` for the per-signature native/VARIANT choice.
        """
        return _invoke_udf(self, converted_args, typed_args, name)

    @abstractmethod
    def _emit_ddl(
        self,
        call_site_types: list[DataType],
        session: Session,
        type_key: str | None = None,
    ) -> None:
        """Create the physical function for ``type_key`` and record it (see ORDERING CONTRACT)."""


@dataclass
class LazySnowparkUdf(LazyUdfBase):
    """Scala UDF registered without input types whose CREATE FUNCTION DDL is deferred.

    Created when spark.udf.register is called without explicit input types.  The DDL
    is emitted on first call-site execution using the real call-site types, avoiding an
    all-VARIANT DDL at registration time.

    When the same UDF is called with different input type signatures (e.g. once with an
    INT column and once with a struct column), a separate DDL is emitted per unique
    signature using a type-derived name suffix.  This handles UDFs declared with AnyRef
    (or similar wildcard) input that are applied across heterogeneous column types.

    ``stage_imports`` holds the Snowflake stage paths (JARs + closure binary) uploaded
    at registration time; they will appear in the ``IMPORTS = (...)`` clause of the
    eventual CREATE FUNCTION statement.
    """

    stage_imports: list[str]
    # DCR inline-closure mode: raw payload bytes to embed in the Java handler body.
    # None in normal mode (closure binary is uploaded to session stage and listed in stage_imports).
    inline_payload: bytes | None = None
    # Lazy UDFs are always Scala scalars — never UDAFs.
    kind: UdfKind = field(default=UdfKind.SCALA_UDF, init=False)
    _materialized: bool = field(default=False, init=False, repr=False)
    # Maps repr(call_site_types) -> effective return DataType for that signature.
    # Only populated when the inferred return type differs from original_return_type
    # (e.g. Decimal return type inferred from call-site input).
    _type_to_effective_rt: dict = field(default_factory=dict, init=False, repr=False)

    def effective_return_type_for(self, call_site_types: list[DataType]) -> DataType:
        """Return the effective DDL return type for the given call-site types.

        Falls back to original_return_type when no inference was applied (the
        common case for non-Decimal or already-specific Decimal return types).
        """
        return self._type_to_effective_rt.get(
            repr(call_site_types), self.original_return_type
        )

    def _emit_ddl(
        self,
        call_site_types: list[DataType],
        session: Session,
        type_key: str | None = None,
    ) -> None:
        if type_key is None:
            type_key = repr(call_site_types)
        udf_name = self._next_udf_name(type_key)

        effective_rt = _emit_scala_udf_ddl(
            udf_name,
            self.stage_imports,
            call_site_types,
            self.original_return_type,
            session,
            inline_payload=self.inline_payload,
        )
        # Store the inferred return type only when it differs from the declared one,
        # so post-processing casts use the actual DDL return type. Written before the
        # _type_to_name gate (see LazyUdfBase ORDERING CONTRACT).
        if effective_rt is not None and effective_rt != self.original_return_type:
            self._type_to_effective_rt[type_key] = effective_rt
        self.input_types = call_site_types
        self._materialized = True
        self._name_to_types[udf_name] = call_site_types
        self._type_to_name[type_key] = udf_name


@dataclass
class LazyPythonUdf(LazyUdfBase):
    """Python UDF registered via ``spark.udf.register`` whose DDL is deferred until the first call.

    At registration time no call-site input types are available, so the DDL cannot be
    emitted with native input types.  On the first call for a given call-site type
    signature the physical Snowflake UDF is created with native types for scalar
    positions (int/float/str/bool/bytes/date/datetime/Decimal), avoiding the all-VARIANT
    round-trip and the schema-JSON coercion wrapper.

    If call-site types contain any non-native position (struct/map/variant/array), the
    call falls back to the all-VARIANT protocol (same as today) to preserve correctness.

    One physical function is created per distinct call-site type signature.
    """

    # Parameters needed to create the physical UDF.
    _proto: expressions_proto.CommonInlineUserDefinedFunction
    _udf_packages: str
    _udf_imports: str
    _artifact_repository: str | None
    _resource_constraint: dict[str, str] | None
    _use_sproc: bool

    kind: UdfKind = field(default=UdfKind.PYTHON_REGISTERED, init=False)

    # Maps repr(call_site_types) -> bool (True = all inputs native, False = all-VARIANT).
    # Read lock-free in _invoke_materialized, so _emit_ddl writes it before the
    # _type_to_name gate (see LazyUdfBase ORDERING CONTRACT).
    _type_to_all_native: dict = field(default_factory=dict, init=False, repr=False)

    def _invoke_materialized(
        self,
        name: str,
        converted_args: list["snowpark_fn.Column"],
        typed_args: list[TypedColumn],
        type_key: str,
    ) -> "snowpark_fn.Column":
        # ``converted_args`` (encoded by the base ``invoke``) is intentionally ignored:
        # the physical signature (native vs all-VARIANT) is chosen per signature here.
        # The base ``invoke`` still owns the return-type cast-back.
        if self._type_to_all_native[type_key]:
            # Native inputs: pass through with no VARIANT cast and no schema-JSON sidecar.
            return snowpark_fn.call_udf(name, *(tc.col for tc in typed_args))

        # All-VARIANT fallback: identical to the base path. ``converted_args`` were
        # already cast to VARIANT by ``invoke`` and ``_invoke_udf`` appends the
        # schema-JSON sentinel for PYTHON_REGISTERED.
        return _invoke_udf(self, converted_args, typed_args, name)

    def _emit_ddl(
        self,
        call_site_types: list[DataType],
        session: Session,
        type_key: str | None = None,
    ) -> None:
        from snowflake.snowpark_connect.utils.python_udf_marshal import (
            python_is_native_input,
        )

        if type_key is None:
            type_key = repr(call_site_types)

        all_native = all(python_is_native_input(t) for t in call_site_types)

        udf_name = session.get_fully_qualified_name_if_possible(
            self._next_udf_name(type_key)
        )

        # Native signatures declare native SQL params (no schema-JSON wrapper); any
        # non-native position falls back to the all-VARIANT + coercion protocol.
        input_types = call_site_types if all_native else None
        coerce = not all_native

        if self._use_sproc:
            physical = process_udf_in_sproc(
                common_inline_user_defined_function=self._proto,
                called_from="register_udf_lazy",
                return_type=self.return_type,
                kind=UdfKind.PYTHON_REGISTERED,
                input_types=input_types,
                udf_name=udf_name,
                replace=True,
                udf_packages=self._udf_packages,
                udf_imports=self._udf_imports,
                original_return_type=self.original_return_type,
                artifact_repository=self._artifact_repository,
                resource_constraint=self._resource_constraint,
                coerce_via_schema_json=coerce,
            )
            physical_name = physical.name
            # The sproc returns the true physical param list (incl. any trailing
            # schema-JSON StringType) in input_types.
            physical_input_types = list(physical.input_types)
        else:
            udf_processor = udf_utils.ProcessCommonInlineUserDefinedFunction(
                common_inline_user_defined_function=self._proto,
                input_types=input_types,
                called_from="register_udf_lazy",
                return_type=self.return_type,
                udf_packages=self._udf_packages,
                udf_imports=self._udf_imports,
                original_return_type=self.original_return_type,
                artifact_repository=self._artifact_repository,
                resource_constraint=self._resource_constraint,
                udf_name=udf_name,
                replace=True,
                coerce_via_schema_json=coerce,
            )
            physical = udf_processor.create_udf()
            physical_name = getattr(physical, "name", udf_name)
            # After create_udf the processor holds the true physical param list: the
            # all-VARIANT default gains a trailing schema-JSON StringType on the
            # fallback path (and struct args may be decomposed). Capture it so
            # DropFunctionCommand emits the exact signature.
            physical_input_types = list(udf_processor._input_types or [])

        # Populate the flag and name->types map BEFORE the _type_to_name gate:
        # _invoke_materialized reads _type_to_all_native on the lock-free fast path once
        # the gate shows the key, so the flag must be visible first.
        self._type_to_all_native[type_key] = all_native
        self._name_to_types[physical_name] = physical_input_types
        self._type_to_name[type_key] = physical_name


def require_creating_udf_in_sproc(
    udf_proto: expressions_proto.CommonInlineUserDefinedFunction,
) -> bool:
    """
    Offloading to a SPROC is required for Python UDFs in the following scenarios:
    * TCM Mode: For security. When running in TCM, we want to avoid
      deserializing user code directly in the TCM because it runs in a 'Permissive lighting sandbox'
      for performance. Moving to a SPROC provides a secure isolation boundary.
      Note: Scala UDFs are exempt because TCM only stages the payload - does not interpret it;
      the deserialization happens in Scala UDF which is isolated.
    * Version Compatibility: If the Python version specified in the UDF metadata
      does not match the current runtime version, a SPROC environment is required
      to provide the correct execution runtime.
    * Testing: When the `snowpark.connect.test.force_create_sproc` config is enabled.
    """
    is_python_udf = udf_proto.WhichOneof("function") == "python_udf"
    client_python_ver = udf_proto.python_udf.python_ver if is_python_udf else None
    server_python_ver = f"{sys.version_info.major}.{sys.version_info.minor}"

    result = (
        is_force_create_sproc_enabled()
        or tcm.TCM_MODE
        or (
            is_python_udf
            and client_python_ver is not None
            and server_python_ver != client_python_ver
        )
    )
    return result


def process_udf_in_sproc(
    common_inline_user_defined_function: expressions_proto.CommonInlineUserDefinedFunction,
    called_from: str,
    return_type: DataType,
    kind: UdfKind,
    input_types: list | None = None,
    input_column_names: list[str] | None = None,
    udf_name: str | None = None,
    replace: bool = False,
    udf_packages: str = "",
    udf_imports: str = "",
    original_return_type: DataType | None = None,
    artifact_repository: str | None = None,
    resource_constraint: dict[str, str] | None = None,
    coerce_via_schema_json: bool = False,
) -> SnowparkUDF:
    """Helper method to call the sproc to create inline UDF and return the essential info of the UDF."""
    session = get_or_create_snowpark_session()
    sproc_name = _get_or_create_udf_sproc_helper(
        session,
        common_inline_user_defined_function.python_udf.python_ver,
    )
    udf_proto_encoded = base64.b64encode(
        common_inline_user_defined_function.SerializeToString()
    ).decode("ascii")

    def gen_input_types_json_str(input_types: list | None = None) -> Optional[str]:
        if input_types is None:
            return None
        return json.dumps([dt.json_value() for dt in input_types])

    input_types_json_str = gen_input_types_json_str(input_types)

    input_column_names_json_str = (
        None if input_column_names is None else json.dumps(input_column_names)
    )

    original_return_type_json_str = (
        None
        if original_return_type is None
        else json.dumps(original_return_type.json_value())
    )

    # resource_constraint is passed from caller (captured on SAS server side)
    resource_constraint_json_str = (
        None if resource_constraint is None else json.dumps(resource_constraint)
    )

    sproc_res = session.call(
        sproc_name,
        called_from,
        json.dumps(return_type.json_value()),
        input_types_json_str,
        input_column_names_json_str,
        snowpark_fn.lit(udf_name),
        replace,
        udf_packages,
        udf_imports,
        udf_proto_encoded,
        original_return_type_json_str,
        artifact_repository,
        resource_constraint_json_str,
        coerce_via_schema_json,
    )

    udf_attr = json.loads(sproc_res)
    return_type = _parse_datatype_json_value(udf_attr["return_type"])
    cast_to_original = isinstance(return_type, VariantType) and isinstance(
        original_return_type, (ArrayType, MapType, StructType)
    )
    snowpark_udf = SnowparkUDF(
        name=udf_attr["name"],
        input_types=[_parse_datatype_json_value(t) for t in udf_attr["input_types"]],
        return_type=return_type,
        original_return_type=original_return_type,
        kind=kind,
        cast_to_original_return_type=cast_to_original,
    )
    if called_from == "register_udf":
        from snowflake.snowpark_connect.utils.spark_session_cache import (
            get_spark_session_cache,
        )

        get_spark_session_cache().udfs.register(
            common_inline_user_defined_function.function_name.lower(),
            snowpark_udf,
        )
    return snowpark_udf


def _get_or_create_udf_sproc_helper(
    session: Session,
    python_version: str = f"{sys.version_info.major}.{sys.version_info.minor}",
) -> str:
    """
    This helper method will get or create a sproc in targeted python version to create the python UDF. The sproc's
    return value is a json string containing the UDF's name, input types, and, return type.
    """
    sproc_name = f"{CREATE_UDF_SPROC_NAME_PREFIX}_{python_version.replace('.', '_')}"
    if sproc_name in session._sprocs:
        return sproc_name

    inline_udf_utils_py_code = inspect.getsource(udf_utils)

    create_udf_sproc_sql = f"""
CREATE OR REPLACE TEMPORARY PROCEDURE {sproc_name}(
    called_from VARCHAR,
    return_type_json_str VARCHAR,
    input_types_json_str VARCHAR,
    input_column_names_json_str VARCHAR,
    udf_name VARCHAR,
    replace BOOLEAN,
    udf_packages VARCHAR,
    udf_imports VARCHAR,
    base64_str VARCHAR,
    original_return_type VARCHAR,
    artifact_repository VARCHAR,
    resource_constraint_json VARCHAR,
    coerce_via_schema_json BOOLEAN
)
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '{python_version}'
PACKAGES = ('pyspark>=3.5.0,<4', 'cloudpickle', 'snowflake-snowpark-python', 'grpcio>=1.48.1', 'snowflake-telemetry-python')
HANDLER = 'create'
EXECUTE AS CALLER
AS $$
import cloudpickle
import base64
from pyspark.sql.connect.proto.expressions_pb2 import CommonInlineUserDefinedFunction
import json
from snowflake.snowpark.types import *
from typing import Optional
from snowflake.snowpark.types import _parse_datatype_json_value

{inline_udf_utils_py_code}

def parse_input_types(input_types_json_str) -> Optional[list[DataType]]:
    if input_types_json_str is None:
        return None
    input_types_json = json.loads(input_types_json_str)
    return [_parse_datatype_json_value(t) for t in input_types_json]

def parse_return_type(return_type_json_str) -> Optional[DataType]:
    return_type_json = json.loads(return_type_json_str)
    result = _parse_datatype_json_value(return_type_json)
    if isinstance(result, (ArrayType, MapType, StructType)):
        result = result._as_nested()
    return result

def parse_resource_constraint(resource_constraint_json) -> Optional[dict[str, str]]:
    if resource_constraint_json is None:
        return None
    return json.loads(resource_constraint_json)

def create(session, called_from, return_type_json_str, input_types_json_str, input_column_names_json_str, udf_name, replace, udf_packages, udf_imports, b64_str, original_return_type, artifact_repository, resource_constraint_json, coerce_via_schema_json):
    session._use_scoped_temp_objects = False
    import snowflake.snowpark.context as context
    context._use_structured_type_semantics = True
    context._is_snowpark_connect_compatible_mode = True

    restored_bytes = base64.b64decode(b64_str.encode('ascii'))
    udf_proto = CommonInlineUserDefinedFunction()
    udf_proto.ParseFromString(restored_bytes)
    udf_processor = ProcessCommonInlineUserDefinedFunction(
        udf_proto,
        input_types=parse_input_types(input_types_json_str),
        return_type=parse_return_type(return_type_json_str),
        called_from=called_from,
        input_column_names=None if input_column_names_json_str is None else json.loads(input_column_names_json_str),
        udf_name=udf_name,
        replace=replace,
        udf_packages=udf_packages,
        udf_imports=udf_imports,
        original_return_type=parse_return_type(original_return_type) if original_return_type else None,
        artifact_repository=artifact_repository,
        resource_constraint=parse_resource_constraint(resource_constraint_json),
        coerce_via_schema_json=coerce_via_schema_json,
    )
    udf = udf_processor.create_udf()
    return json.dumps({{"name": udf.name, "return_type": udf._return_type.json_value(), "input_types": [t.json_value() for t in udf._input_types]}})
$$;
"""
    session.sql(create_udf_sproc_sql).collect()
    session._sprocs.add(sproc_name)
    logger.info(f"Procedure {sproc_name} created")
    return sproc_name


def udf_check(
    udf_proto: expressions_proto.CommonInlineUserDefinedFunction,
) -> None:
    _check_supported_udf(udf_proto)
    _aggregate_function_check(udf_proto)


def _check_supported_udf(
    udf_proto: expressions_proto.CommonInlineUserDefinedFunction,
) -> None:
    match udf_proto.WhichOneof("function"):
        case "python_udf":
            pass
        case "java_udf":
            pass
        case "scalar_scala_udf":
            pass
        case _ as function_type:
            exception = ValueError(
                f"Function type {function_type} not supported for common inline user-defined function"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception


def _aggregate_function_check(
    udf_proto: expressions_proto.CommonInlineUserDefinedFunction,
):
    name, is_aggregate_function = get_is_aggregate_function()
    if not udf_proto.deterministic and name != "default" and is_aggregate_function:
        exception = AnalysisException(
            f"[AGGREGATE_FUNCTION_WITH_NONDETERMINISTIC_EXPRESSION] Non-deterministic expression {name}({udf_proto.function_name}) should not appear in the arguments of an aggregate function."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
        raise exception


def _join_checks(snowpark_udf_arg_names: list[str]):
    is_evaluating_join_condition = get_is_evaluating_join_condition()
    is_left_evaluable, is_right_evaluable = False, False

    for snowpark_udf_arg_name in snowpark_udf_arg_names:
        # UDFs can only reference EITHER the left OR the right side of the join but not both.
        # Example: Assume left has column a and right has column b.
        # lambda a: str(a) is fine because it will only reference either the left dataframe or the right dataframe.
        # lambda a, b: a == b is not fine because it will reference both of the dataframes.
        is_left_evaluable = (
            is_left_evaluable
            or snowpark_udf_arg_name in is_evaluating_join_condition[2]
        )
        is_right_evaluable = (
            is_right_evaluable
            or snowpark_udf_arg_name in is_evaluating_join_condition[3]
        )
        # Check for implicit cartesian product only on inner joins. If crossjoin is disabled, raise an exception.
        if (
            is_evaluating_join_condition[0] == "INNER"
            and not global_config.spark_sql_crossJoin_enabled
            and is_left_evaluable
            and is_right_evaluable
        ):
            exception = AnalysisException(
                f"Detected implicit cartesian product for {is_evaluating_join_condition[0]} join between logical plans. \n"
                f"Join condition is missing or trivial. \n"
                f"Either: use the CROSS JOIN syntax to allow cartesian products between those relations, or; "
                f"enable implicit cartesian products by setting the configuration variable spark.sql.crossJoin.enabled=True."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
            raise exception
        if (
            is_evaluating_join_condition[0] != "INNER"
            and is_evaluating_join_condition[1]
            and is_left_evaluable
            and is_right_evaluable
        ):
            exception = AnalysisException(
                f"[UNSUPPORTED_FEATURE.PYTHON_UDF_IN_ON_CLAUSE] The feature is not supported: "
                f"Python UDF in the ON clause of a {is_evaluating_join_condition[0]} JOIN. "
                f"In case of an INNNER JOIN consider rewriting to a CROSS JOIN with a WHERE clause."
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception


def infer_snowpark_arguments(
    udf_proto: expressions_proto.CommonInlineUserDefinedFunction,
    column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
) -> tuple[list[str], list[TypedColumn]]:
    snowpark_udf_args: list[TypedColumn] = []
    snowpark_udf_arg_names: list[str] = []
    for arg_exp in udf_proto.arguments:
        # Handle unresolved_star expressions specially
        if arg_exp.HasField("unresolved_star"):
            # Use map_unresolved_star_as_struct to expand star into a single combined column
            spark_name, typed_column = map_unresolved_star_as_single_column(
                arg_exp, column_mapping, typer
            )
            snowpark_udf_args.append(typed_column)
            snowpark_udf_arg_names.append(spark_name)
        else:
            (
                snowpark_udf_arg_name,
                snowpark_udf_arg,
            ) = map_single_column_expression(arg_exp, column_mapping, typer)
            snowpark_udf_args.append(snowpark_udf_arg)
            snowpark_udf_arg_names.append(snowpark_udf_arg_name)
    _join_checks(snowpark_udf_arg_names)
    return snowpark_udf_arg_names, snowpark_udf_args
