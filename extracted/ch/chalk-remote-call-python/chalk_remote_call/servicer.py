from __future__ import annotations

import asyncio
import dataclasses
import inspect
from collections.abc import Callable
from typing import Any

import pyarrow as pa

from chalk_remote_call.arrow_utils import decode_ipc_stream, encode_record_batch
from chalk_remote_call.input_transform import resolve_column_names, transform
from chalk_remote_call.tracing import remote_function_invocation_span


def _is_structured(obj: Any) -> bool:
    """Return True if *obj* is a recognised structured-type instance."""
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return True
    if hasattr(obj, "_asdict"):  # namedtuple
        return True
    if hasattr(obj, "model_dump") and hasattr(obj, "model_fields"):  # pydantic v2
        return True
    return hasattr(obj, "__attrs_attrs__")  # attrs


def _to_dict(obj: Any) -> dict[str, Any]:
    """Convert a single structured-type instance to a plain dict."""
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return dataclasses.asdict(obj)
    val: Any = obj
    if hasattr(val, "_asdict"):  # namedtuple
        return val._asdict()
    if hasattr(val, "model_dump") and hasattr(val, "model_fields"):  # pydantic v2
        return val.model_dump()
    if hasattr(val, "__attrs_attrs__"):  # attrs
        return {a.name: getattr(val, a.name) for a in val.__attrs_attrs__}
    raise TypeError(f"Cannot convert {type(val).__name__} to dict")


def _structured_field_names(obj: Any) -> list[str] | None:
    """Field names in declaration order for a structured instance, or None.

    Avoids dataclasses.asdict / pydantic model_dump, which both deep-copy
    recursively. We only need a flat columnar view.
    """
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return [f.name for f in dataclasses.fields(obj)]
    val: Any = obj
    fields_attr = getattr(val, "_fields", None)
    if fields_attr is not None and isinstance(fields_attr, tuple):  # namedtuple
        return list(fields_attr)
    model_fields = getattr(type(val), "model_fields", None)
    if model_fields is not None and hasattr(val, "model_dump"):  # pydantic v2
        return list(model_fields.keys())
    attrs_attr = getattr(val, "__attrs_attrs__", None)
    if attrs_attr is not None:  # attrs
        return [a.name for a in attrs_attr]
    return None


def _structured_list_to_dict(items: list[Any]) -> dict[str, list[Any]]:
    """Transpose a list of structured instances into columnar form.

    Fast path: flat rows (no structured-type field values) use direct getattr
    per field — avoids the recursive deep-copy in dataclasses.asdict /
    pydantic model_dump.

    Slow path: if any field holds a nested structured instance, fall back to
    _to_dict so pa.array receives plain dicts/lists.
    """
    first = items[0]
    names = _structured_field_names(first)
    has_nested = names is not None and any(_is_structured(getattr(first, n)) for n in names)
    if names is None or has_nested:
        dicts = [_to_dict(item) for item in items]
        keys = list(dicts[0].keys())
        return {key: [d[key] for d in dicts] for key in keys}
    return {name: [getattr(it, name) for it in items] for name in names}


def _coerce_to_record_batch(result: Any) -> pa.RecordBatch:
    """Convert a handler result to a RecordBatch for the response stream."""
    if isinstance(result, pa.RecordBatch):
        return result
    if isinstance(result, pa.Table):
        if result.num_rows > 0:
            return result.combine_chunks().to_batches()[0]
        return pa.RecordBatch.from_pydict(
            {name: [] for name in result.schema.names},
            schema=result.schema,
        )
    if isinstance(result, pa.Array):
        return pa.record_batch([result], names=["result"])
    if isinstance(result, pa.ChunkedArray):
        return pa.record_batch([result.combine_chunks()], names=["result"])
    # For list, dict, scalar — convert via pa.array
    try:
        # Convert structured types (dataclass, namedtuple, pydantic, attrs) to dicts
        if isinstance(result, list) and len(result) > 0 and _is_structured(result[0]):
            result = _structured_list_to_dict(result)
        elif not isinstance(result, dict | list) and _is_structured(result):
            result = {k: [v] for k, v in _to_dict(result).items()}

        if isinstance(result, dict):
            # dict of column_name -> values
            arrays = []
            names = []
            for key, values in result.items():
                names.append(str(key))
                if isinstance(values, pa.Array):
                    arrays.append(values)
                else:
                    arrays.append(pa.array(values if isinstance(values, list) else [values]))
            return pa.record_batch(arrays, names=names)
        if isinstance(result, list):
            arr = pa.array(result)
            return pa.record_batch([arr], names=["result"])
        # Scalar
        arr = pa.array([result])
        return pa.record_batch([arr], names=["result"])
    except Exception as e:
        raise TypeError(f"Cannot convert handler result of type {type(result).__name__} to RecordBatch: {e}") from e


def _get_or_create_event_loop() -> asyncio.AbstractEventLoop:
    """Get the running event loop or create a new one."""
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


def _run_async(coro):
    """Run a coroutine synchronously."""
    loop = _get_or_create_event_loop()
    if loop.is_running():
        # Already inside an async context — can't use run_until_complete.
        # Create a new loop in a thread.
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            return pool.submit(asyncio.run, coro).result()
    return loop.run_until_complete(coro)


def _collect_async_gen(agen) -> list:
    """Collect all items from an async generator synchronously."""

    async def _collect():
        items = []
        async for item in agen:
            items.append(item)
        return items

    return _run_async(_collect())


def _drain_async_gen(agen, emit: Callable[[bytes], None]) -> None:
    """Drain an async generator and emit each encoded item immediately."""

    async def _drain():
        async for item in agen:
            emit(encode_record_batch(_coerce_to_record_batch(item)))

    _run_async(_drain())


def process_batches(
    ipc_bytes: bytes,
    handler: Callable[..., Any],
    arg_names: list[str] | None,
    context_metadata: dict[str, Any],
    emit: Callable[[bytes], None] | None = None,
) -> list[bytes]:
    """Bridge function called from Rust via PyO3.

    Decodes IPC stream, transforms each batch, calls the handler,
    coerces the result, and encodes the response.

    Returns a list of IPC-encoded response bytes (one per input batch).
    When ``emit`` is provided, each encoded response is emitted immediately and
    the returned list is empty.
    """
    batches = decode_ipc_stream(ipc_bytes)
    results = []

    def append_or_emit(chunk: bytes) -> None:
        if emit is None:
            results.append(chunk)
        else:
            emit(chunk)

    for batch in batches:
        try:
            event = transform(batch, arg_names)
        except Exception as e:
            raise ValueError(f"Input transformation failed: {e}") from e

        with remote_function_invocation_span(context_metadata):
            result = handler(event, context_metadata)
            # If the handler is async, await the coroutine.
            if inspect.iscoroutine(result):
                result = _run_async(result)

            if inspect.isgenerator(result):
                # Sync generator: encode each yielded value as a separate chunk.
                for item in result:
                    result_batch = _coerce_to_record_batch(item)
                    append_or_emit(encode_record_batch(result_batch))
            elif inspect.isasyncgen(result):
                # Async generator: stream when possible, otherwise preserve
                # the existing list-returning bridge contract.
                if emit is not None:
                    _drain_async_gen(result, emit)
                else:
                    for item in _collect_async_gen(result):
                        result_batch = _coerce_to_record_batch(item)
                        results.append(encode_record_batch(result_batch))
            else:
                result_batch = _coerce_to_record_batch(result)
                append_or_emit(encode_record_batch(result_batch))

    return results


def _concat_batches(batches: list[pa.RecordBatch]) -> pa.RecordBatch:
    """Combine a caller's batches into a single RecordBatch (vertical concat)."""
    if len(batches) == 1:
        return batches[0]
    return pa.Table.from_batches(batches).combine_chunks().to_batches()[0]


def process_batches_coalesced(
    items_ipc_bytes: list[bytes],
    handler: Callable[..., Any],
    arg_names: list[str] | None,
    context_metadatas: list[dict[str, Any]],
) -> list[bytes]:
    """Batched bridge: coalesces N concurrent callers into one handler invocation.

    Args:
        items_ipc_bytes: One IPC-encoded byte string per caller.
        handler: (events: list[dict[str, pa.Array]], contexts: list[dict]) -> list[Any]
        arg_names: Column-renaming spec (applied identically to every caller).
        context_metadatas: One context dict per caller.

    Returns:
        list[bytes], one IPC-encoded RecordBatch per caller, in input order.

    Raises:
        ValueError: Schemas differ across callers, input is empty, or len mismatch
            between inputs and handler output.
        TypeError: Handler is a generator / async generator (not supported in
            coalesced mode — each caller expects exactly one response chunk).
    """
    if not items_ipc_bytes:
        raise ValueError("process_batches_coalesced called with no items")
    if len(items_ipc_bytes) != len(context_metadatas):
        raise ValueError(
            f"items_ipc_bytes ({len(items_ipc_bytes)}) and context_metadatas "
            f"({len(context_metadatas)}) lengths must match"
        )
    if inspect.isgeneratorfunction(handler) or inspect.isasyncgenfunction(handler):
        raise TypeError("Generator/async-generator handlers are not supported when batching is enabled")

    # Decode each caller's bytes to a single concatenated RecordBatch.
    per_caller_batches: list[pa.RecordBatch] = []
    reference_schema: pa.Schema | None = None
    for i, ipc_bytes in enumerate(items_ipc_bytes):
        batches = decode_ipc_stream(ipc_bytes)
        if not batches:
            raise ValueError(f"Caller {i} produced no batches")
        combined = _concat_batches(batches)
        if reference_schema is None:
            reference_schema = combined.schema
        elif not combined.schema.equals(reference_schema):
            raise ValueError(
                f"Schema mismatch in coalesced batch: caller 0 has {reference_schema}, caller {i} has {combined.schema}"
            )
        per_caller_batches.append(combined)

    # Build events (list of dicts, one per caller) via the same transform used in
    # the single-caller path — keeps behaviour consistent for column renaming.
    events: list[dict[str, pa.Array]] = []
    for batch in per_caller_batches:
        try:
            events.append(transform(batch, arg_names))
        except Exception as e:
            raise ValueError(f"Input transformation failed: {e}") from e

    # Dispatch. Contexts are passed as a parallel list — handler can correlate
    # per-caller metadata with each event by index.
    with remote_function_invocation_span(context_metadatas, coalesced_count=len(context_metadatas)):
        result = handler(events, context_metadatas)
        if inspect.iscoroutine(result):
            result = _run_async(result)

        if not isinstance(result, list):
            raise TypeError(f"Coalesced handler must return a list, got {type(result).__name__}")
        if len(result) != len(events):
            raise ValueError(f"Coalesced handler must return one result per input ({len(events)}); got {len(result)}")

        # Coerce and encode each per-caller result.
        output: list[bytes] = []
        for i, item in enumerate(result):
            try:
                rb = _coerce_to_record_batch(item)
                output.append(encode_record_batch(rb))
            except Exception as e:
                raise RuntimeError(f"Failed to encode response for caller {i}: {e}") from e

    return output


def process_batches_coalesced_combined(
    items_ipc_bytes: list[bytes],
    handler: Callable[..., Any],
    arg_names: list[str] | None,
    context_metadatas: list[dict[str, Any]],
) -> list[bytes]:
    """Coalesced bridge, combined-RecordBatch variant.

    Vertically concatenates every caller's batches into one RecordBatch,
    builds a CSR-style offsets array marking caller boundaries, and invokes
    the handler once. The handler returns one RecordBatch with row count
    equal to the combined input; the framework slices it back into per-caller
    responses (zero-copy on Arrow buffers).

    Handler signature:
        (combined: pa.RecordBatch, offsets: list[int], contexts: list[dict])
            -> pa.RecordBatch

    `offsets` has length `len(contexts) + 1`; caller `i` owns rows
    `[offsets[i] : offsets[i+1])`.

    Raises:
        ValueError: empty input, length mismatch, schema mismatch across
            callers, arg_names length mismatch, or handler output row count
            doesn't match combined input.
        TypeError: handler is a generator / async generator (not supported
            in coalesced modes — each caller expects exactly one response
            chunk).
    """
    if not items_ipc_bytes:
        raise ValueError("process_batches_coalesced_combined called with no items")
    if len(items_ipc_bytes) != len(context_metadatas):
        raise ValueError(
            f"items_ipc_bytes ({len(items_ipc_bytes)}) and context_metadatas "
            f"({len(context_metadatas)}) lengths must match"
        )
    if inspect.isgeneratorfunction(handler) or inspect.isasyncgenfunction(handler):
        raise TypeError("Generator/async-generator handlers are not supported when batching is enabled")

    per_caller: list[pa.RecordBatch] = []
    reference_schema: pa.Schema | None = None
    for i, ipc_bytes in enumerate(items_ipc_bytes):
        batches = decode_ipc_stream(ipc_bytes)
        if not batches:
            raise ValueError(f"Caller {i} produced no batches")
        rb = _concat_batches(batches)
        if reference_schema is None:
            reference_schema = rb.schema
        elif not rb.schema.equals(reference_schema):
            raise ValueError(
                f"Schema mismatch in coalesced batch: caller 0 has {reference_schema}, caller {i} has {rb.schema}"
            )
        per_caller.append(rb)

    assert reference_schema is not None  # guaranteed by the empty-input check above

    offsets: list[int] = [0]
    for rb in per_caller:
        offsets.append(offsets[-1] + rb.num_rows)

    table = pa.Table.from_batches(per_caller)
    combined_batches = table.combine_chunks().to_batches()
    if combined_batches:
        combined = combined_batches[0]
    else:
        combined = pa.RecordBatch.from_pydict(
            {name: [] for name in reference_schema.names},
            schema=reference_schema,
        )

    if arg_names is not None:
        try:
            names = resolve_column_names(combined.schema.names, arg_names)
        except ValueError as e:
            raise ValueError(str(e).replace("RecordBatch has", "combined batch has")) from e
        combined = combined.rename_columns(names)

    with remote_function_invocation_span(context_metadatas, coalesced_count=len(context_metadatas)):
        result = handler(combined, offsets, context_metadatas)
        if inspect.iscoroutine(result):
            result = _run_async(result)

        if isinstance(result, pa.RecordBatch):
            result_rb = result
        else:
            try:
                result_rb = _coerce_to_record_batch(result)
            except Exception as e:
                raise RuntimeError(f"Failed to coerce handler output: {e}") from e

        if result_rb.num_rows != combined.num_rows:
            raise ValueError(
                f"Combined handler must return a RecordBatch with {combined.num_rows} rows "
                f"(matching input); got {result_rb.num_rows}"
            )

        output: list[bytes] = []
        for i in range(len(per_caller)):
            start = offsets[i]
            length = offsets[i + 1] - start
            sliced = result_rb.slice(start, length)
            try:
                output.append(encode_record_batch(sliced))
            except Exception as e:
                raise RuntimeError(f"Failed to encode response for caller {i}: {e}") from e
    return output
