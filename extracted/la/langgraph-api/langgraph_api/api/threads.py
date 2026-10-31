import re
from contextlib import aclosing
from typing import TYPE_CHECKING, Any, get_args

from starlette.exceptions import HTTPException
from starlette.responses import Response
from starlette.routing import BaseRoute

from langgraph_api import config as lg_api_config
from langgraph_api.config import USE_CUSTOM_CHECKPOINTER
from langgraph_api.encryption.shared import (
    using_encryption,
)
from langgraph_api.feature_flags import (
    IS_POSTGRES_OR_GRPC_BACKEND,
    PREFER_GRPC_CHECKPOINTER,
)
from langgraph_api.route import ApiRequest, ApiResponse, ApiRoute
from langgraph_api.schema import THREAD_FIELDS, THREAD_STATE_FIELDS, ThreadStreamMode
from langgraph_api.serde import Fragment, json_dumpb
from langgraph_api.sse import EventSourceResponse
from langgraph_api.state import state_snapshot_to_thread_state
from langgraph_api.utils import (
    fetchone,
    get_pagination_headers,
    uuid7,
    validate_select_columns,
    validate_stream_id,
    validate_uuid,
)
from langgraph_api.utils.extract import extract_path_value, validate_extract
from langgraph_api.utils.headers import get_configurable_headers
from langgraph_api.validation import (
    ThreadCountRequest,
    ThreadCreate,
    ThreadPatch,
    ThreadPruneRequest,
    ThreadSearchRequest,
    ThreadStateCheckpointRequest,
    ThreadStateSearch,
    ThreadStateUpdate,
)
from langgraph_runtime.database import connect
from langgraph_runtime.retry import retry_db

if IS_POSTGRES_OR_GRPC_BACKEND:
    from langgraph_api.grpc.ops import Threads
else:
    from langgraph_runtime.ops import Threads

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Mapping

    from langgraph.types import StateSnapshot


@retry_db
async def create_thread(
    request: ApiRequest,
):
    """Create a thread."""
    payload = await request.json(ThreadCreate)
    if thread_id := payload.get("thread_id"):
        validate_uuid(thread_id, "Invalid thread ID: must be a UUID")

    thread_id = thread_id or str(uuid7())
    supersteps = payload.get("supersteps")

    if IS_POSTGRES_OR_GRPC_BACKEND and not supersteps:
        iter = await Threads.put(
            None,
            thread_id,
            metadata=payload.get("metadata") or {},
            if_exists=payload.get("if_exists") or "raise",
            ttl=payload.get("ttl"),
        )
    else:
        # Need connection for inmem put or gRPC State.bulk
        async with connect(supports_core_api=PREFER_GRPC_CHECKPOINTER) as conn:
            iter = await Threads.put(
                conn,
                thread_id,
                metadata=payload.get("metadata") or {},
                if_exists=payload.get("if_exists") or "raise",
                ttl=payload.get("ttl"),
            )
            config = {
                "configurable": {
                    **get_configurable_headers(request.headers),
                    "thread_id": thread_id,
                }
            }
            if supersteps:
                try:
                    await Threads.State.bulk(
                        conn,
                        config=config,
                        supersteps=supersteps,
                    )
                except HTTPException as e:
                    detail = f"Thread {thread_id} was created, but there were problems updating the state: {e.detail}"
                    raise HTTPException(status_code=201, detail=detail) from e

    thread = await fetchone(iter, not_found_code=409)
    return ApiResponse(thread)


def _exclude_metadata_kwargs(payload: dict) -> dict:
    """Normalize `exclude_metadata` (object or list of objects) into ops kwargs."""
    exclude_metadata = payload.get("exclude_metadata")
    if exclude_metadata is None:
        return {}
    if isinstance(exclude_metadata, dict):
        exclude_metadata = [exclude_metadata]
    return {"exclude_metadata": exclude_metadata}


@retry_db
async def search_threads(
    request: ApiRequest,
):
    """List threads."""
    payload = await request.json(ThreadSearchRequest)
    select = validate_select_columns(payload.get("select") or None, THREAD_FIELDS)
    limit = int(payload.get("limit") or 10)
    offset = int(payload.get("offset") or 0)

    # Validate and parse extract parameter
    raw_extract = payload.get("extract")
    extract = validate_extract(raw_extract) if raw_extract else None

    # SQL-side extraction must be skipped when encryption is active: the
    # Go backend decrypts *after* the SQL query runs, so the
    # extraction expressions would operate on ciphertext.  We re-extract
    # in Python from the already-decrypted response instead.
    needs_python_extract = using_encryption()

    # When encryption is active and both select and extract are used, the
    # storage layer returns only the selected columns.  After decryption we
    # need the root columns referenced by extract paths so we can re-extract
    # from plaintext.  Augment the select sent to storage, then strip the
    # extra columns after re-extraction.
    storage_select = select
    extra_select_cols: set[str] | None = None
    if select and extract and needs_python_extract:
        extract_roots = {path.split(".")[0].split("[")[0] for path in extract.values()}
        extra_select_cols = extract_roots - set(select)
        if extra_select_cols:
            storage_select = list(select) + sorted(extra_select_cols)

    # When we need Python-side extraction, skip SQL extraction since
    # it would extract from ciphertext (wrong) and we'll redo it anyway.
    storage_extract = None if needs_python_extract else extract

    exclude_kwargs = _exclude_metadata_kwargs(payload)
    async with connect() as conn:
        threads_iter, next_offset = await Threads.search(
            conn,
            status=payload.get("status"),
            values=payload.get("values"),
            metadata=payload.get("metadata"),
            ids=payload.get("ids"),
            limit=limit,
            offset=offset,
            sort_by=payload.get("sort_by"),
            sort_order=payload.get("sort_order"),
            select=storage_select,
            extract=storage_extract,
            **exclude_kwargs,
        )
    threads, response_headers = await get_pagination_headers(
        threads_iter, next_offset, offset
    )

    # When SQL-side extraction was skipped (encryption active), extract
    # from the decrypted plaintext in Python.
    if extract and needs_python_extract:
        for thread in threads:
            thread["extracted"] = {
                alias: extract_path_value(thread, path)
                for alias, path in extract.items()
            }
    # Strip columns that were added only for re-extraction.
    if extra_select_cols:
        for thread in threads:
            for col in extra_select_cols:
                thread.pop(col, None)

    return ApiResponse(threads, headers=response_headers)


@retry_db
async def count_threads(
    request: ApiRequest,
):
    """Count threads."""
    payload = await request.json(ThreadCountRequest)
    async with connect() as conn:
        count = await Threads.count(
            conn,
            status=payload.get("status"),
            values=payload.get("values"),
            metadata=payload.get("metadata"),
            **_exclude_metadata_kwargs(payload),
        )
    return ApiResponse(count)


@retry_db
async def get_thread_state(
    request: ApiRequest,
):
    """Get state for a thread."""
    thread_id = request.path_params["thread_id"]
    validate_uuid(thread_id, "Invalid thread ID: must be a UUID")
    subgraphs = request.query_params.get("subgraphs") in ("true", "True")
    async with connect(supports_core_api=PREFER_GRPC_CHECKPOINTER) as conn:
        config = {
            "configurable": {
                **get_configurable_headers(request.headers),
                "thread_id": thread_id,
            }
        }
        state = state_snapshot_to_thread_state(
            await Threads.State.get(conn, config=config, subgraphs=subgraphs)
        )
    return ApiResponse(state)


@retry_db
async def get_thread_state_at_checkpoint(
    request: ApiRequest,
):
    """Get state for a thread."""
    thread_id = request.path_params["thread_id"]
    validate_uuid(thread_id, "Invalid thread ID: must be a UUID")
    checkpoint_id = request.path_params["checkpoint_id"]
    async with connect(supports_core_api=PREFER_GRPC_CHECKPOINTER) as conn:
        config = {
            "configurable": {
                **get_configurable_headers(request.headers),
                "thread_id": thread_id,
                "checkpoint_id": checkpoint_id,
            }
        }
        state = state_snapshot_to_thread_state(
            await Threads.State.get(
                conn,
                config=config,
                subgraphs=request.query_params.get("subgraphs") in ("true", "True"),
            )
        )
    return ApiResponse(state)


@retry_db
async def get_thread_state_at_checkpoint_post(
    request: ApiRequest,
):
    """Get state for a thread."""
    thread_id = request.path_params["thread_id"]
    validate_uuid(thread_id, "Invalid thread ID: must be a UUID")
    payload = await request.json(ThreadStateCheckpointRequest)
    async with connect(supports_core_api=PREFER_GRPC_CHECKPOINTER) as conn:
        config = {
            "configurable": {
                **payload["checkpoint"],
                **get_configurable_headers(request.headers),
                "thread_id": thread_id,
            }
        }
        state = state_snapshot_to_thread_state(
            await Threads.State.get(
                conn,
                config=config,
                subgraphs=payload.get("subgraphs", False),
            )
        )
    return ApiResponse(state)


@retry_db
async def update_thread_state(
    request: ApiRequest,
):
    """Add state to a thread."""
    thread_id = request.path_params["thread_id"]
    validate_uuid(thread_id, "Invalid thread ID: must be a UUID")
    payload = await request.json(ThreadStateUpdate)
    config = {"configurable": {"thread_id": thread_id}}
    if payload.get("checkpoint_id"):
        config["configurable"]["checkpoint_id"] = payload["checkpoint_id"]
    if payload.get("checkpoint"):
        config["configurable"].update(payload["checkpoint"])
    try:
        if user_id := request.user.display_name:
            config["configurable"]["user_id"] = user_id
    except AssertionError:
        pass
    config["configurable"].update(get_configurable_headers(request.headers))
    config["configurable"]["thread_id"] = thread_id
    async with connect(supports_core_api=PREFER_GRPC_CHECKPOINTER) as conn:
        inserted = await Threads.State.post(
            conn,
            config,
            payload.get("values"),
            payload.get("as_node"),
        )
    return ApiResponse(inserted)


@retry_db
async def get_thread_history(
    request: ApiRequest,
):
    """Get all past states for a thread."""
    thread_id = request.path_params["thread_id"]
    validate_uuid(thread_id, "Invalid thread ID: must be a UUID")
    limit_ = request.query_params.get("limit", 1)
    try:
        limit = int(limit_)
    except ValueError:
        raise HTTPException(status_code=422, detail=f"Invalid limit {limit_}") from None
    before = request.query_params.get("before")
    select = _validate_history_select(request.query_params.getlist("select"))
    config = {
        "configurable": {
            "thread_id": thread_id,
            "checkpoint_ns": "",
            **get_configurable_headers(request.headers),
        }
    }
    return await _history_response(select, config=config, limit=limit, before=before)


@retry_db
async def get_thread_history_post(
    request: ApiRequest,
):
    """Get all past states for a thread."""
    thread_id = request.path_params["thread_id"]
    validate_uuid(thread_id, "Invalid thread ID: must be a UUID")
    payload = await request.json(ThreadStateSearch)
    select = _validate_history_select(payload.get("select"))
    config = {"configurable": {"thread_id": thread_id, "checkpoint_ns": ""}}
    config["configurable"].update(payload.get("checkpoint", {}))
    config["configurable"].update(get_configurable_headers(request.headers))
    config["configurable"]["thread_id"] = thread_id
    return await _history_response(
        select,
        config=config,
        limit=int(payload.get("limit") or 1),
        before=payload.get("before"),
        metadata=payload.get("metadata"),
    )


async def _history_response(select: list[str] | None, **kwargs: Any) -> ApiResponse:
    budget = lg_api_config.THREAD_HISTORY_MAX_STATE_BYTES
    async with connect(supports_core_api=PREFER_GRPC_CHECKPOINTER) as conn:
        entries = await _serialize_history(
            _history_states(
                conn,
                incremental=bool(budget),
                channels=_selected_value_keys(select),
                **kwargs,
            ),
            budget=budget,
            select=select,
        )
    return ApiResponse(entries)


def _history_states(
    conn: Any,
    *,
    incremental: bool,
    channels: list[str] | None = None,
    **kwargs: Any,
) -> "AsyncIterator[StateSnapshot]":
    if hasattr(Threads.State, "iterate"):
        return Threads.State.iterate(
            conn, incremental=incremental, channels=channels, **kwargs
        )
    # langgraph-runtime-inmem releases before ``iterate`` only have ``list``.
    return _listed_history_states(conn, **kwargs)


async def _listed_history_states(
    conn: Any, **kwargs: Any
) -> "AsyncIterator[StateSnapshot]":
    for state in await Threads.State.list(conn, **kwargs):
        yield state


_SELECT_VALUES_KEY = re.compile(r"values\.[A-Za-z0-9_-]+")


def _validate_history_select(select: list[str] | None) -> list[str] | None:
    """Accept top-level state fields, and ``values.<key>`` for one key of the values."""
    validate_select_columns(
        [f for f in select or () if not _SELECT_VALUES_KEY.fullmatch(f)] or None,
        THREAD_STATE_FIELDS,
    )
    return select or None


def _selected_value_keys(select: list[str] | None) -> list[str] | None:
    """State keys history entries return, or None when they return all of them."""
    if not select or "values" in select:
        return None
    return [f.removeprefix("values.") for f in select if f.startswith("values.")]


def _project_thread_state(
    thread_state: "Mapping[str, Any]",
    select: list[str],
    value_keys: list[str] | None,
) -> dict[str, Any]:
    projected = {k: v for k, v in thread_state.items() if k in select}
    values = thread_state.get("values")
    if value_keys and isinstance(values, dict):
        projected["values"] = {k: values[k] for k in value_keys if k in values}
    return projected


async def _serialize_history(
    states: "AsyncIterator[StateSnapshot]",
    *,
    budget: int,
    select: list[str] | None = None,
) -> list[Fragment]:
    """Serialize history entries until they reach ``budget`` bytes (0: no limit).

    The newest entry is always returned. Each later entry is returned only if
    the entries stay within the budget, and history stops at the first one
    that does not. ``select`` keeps only the named fields of each entry, and
    ``values.<key>`` keeps one key of the values. The budget counts each entry
    as loaded, before projection, so state the checkpointer skipped isn't counted.
    """
    value_keys = _selected_value_keys(select)
    entries: list[Fragment] = []
    total_bytes = 1  # the response array's opening bracket
    async with aclosing(states):
        async for state in states:
            thread_state = state_snapshot_to_thread_state(state)
            entry = json_dumpb(
                _project_thread_state(thread_state, select, value_keys)
                if select
                else thread_state
            )
            if budget:
                # Count the loaded entry, plus a comma or the closing bracket.
                total_bytes += 1 + (
                    len(json_dumpb(thread_state)) if select else len(entry)
                )
            # Drop the decoded entry before the next checkpoint loads.
            del state, thread_state
            if budget and entries and total_bytes > budget:
                break
            entries.append(Fragment(entry))
            if budget and total_bytes >= budget:
                # Nothing more can fit, so don't load another checkpoint.
                break
    return entries


@retry_db
async def get_thread_storage(request: ApiRequest):
    """Bytes a thread's checkpoints occupy, per table and per channel."""
    thread_id = request.path_params["thread_id"]
    validate_uuid(thread_id, "Invalid thread ID: must be a UUID")
    if USE_CUSTOM_CHECKPOINTER or not hasattr(Threads, "storage"):
        raise HTTPException(
            status_code=501,
            detail="Checkpoint storage is only reported for the built-in checkpointer.",
        )
    async with connect() as conn:
        storage = await Threads.storage(conn, thread_id)
    return ApiResponse({"thread_id": thread_id, **storage})


@retry_db
async def get_thread(
    request: ApiRequest,
):
    """Get a thread by ID."""
    thread_id = request.path_params["thread_id"]
    validate_uuid(thread_id, "Invalid thread ID: must be a UUID")

    # Parse include parameter for optional fields (e.g., ttl)
    include_param = request.query_params.get("include", "")
    include_fields = [f.strip() for f in include_param.split(",") if f.strip()]
    include_ttl = "ttl" in include_fields

    async with connect() as conn:
        thread = await Threads.get(conn, thread_id, include_ttl=include_ttl)

    thread_data = await fetchone(thread)
    return ApiResponse(thread_data)


@retry_db
async def patch_thread(
    request: ApiRequest,
):
    """Update a thread."""
    thread_id = request.path_params["thread_id"]
    validate_uuid(thread_id, "Invalid thread ID: must be a UUID")
    payload = await request.json(ThreadPatch)

    return_minimal = request.headers.get("Prefer") == "return=minimal"

    async with connect() as conn:
        thread = await Threads.patch(
            conn,
            thread_id,
            metadata=payload.get("metadata") or {},
            ttl=payload.get("ttl"),
            read_mask_paths=(["thread_id"] if return_minimal else None),
        )

    if return_minimal:
        await fetchone(thread)  # drain the iterator
        return Response(status_code=204)

    thread_data = await fetchone(thread)
    return ApiResponse(thread_data)


@retry_db
async def delete_thread(request: ApiRequest):
    """Delete a thread by ID."""
    thread_id = request.path_params["thread_id"]
    validate_uuid(thread_id, "Invalid thread ID: must be a UUID")
    async with connect() as conn:
        tid = await Threads.delete(conn, thread_id)
    await fetchone(tid)
    return Response(status_code=204)


@retry_db
async def prune_threads(request: ApiRequest):
    """Prune threads by ID."""
    payload = await request.json(ThreadPruneRequest)
    thread_ids = payload.get("thread_ids", [])
    strategy = payload.get("strategy", "delete")

    # Validate each thread_id is a valid UUID
    for tid in thread_ids:
        validate_uuid(tid, "Invalid thread ID: must be a UUID")

    # Validate strategy
    if strategy not in ("delete", "keep_latest"):
        raise HTTPException(
            status_code=422,
            detail=f"Invalid strategy: {strategy}. Expected 'delete' or 'keep_latest'.",
        )

    # Empty list is a no-op, return early
    if not thread_ids:
        return ApiResponse({"pruned_count": 0})

    pruned_count = await Threads.prune(
        thread_ids=thread_ids,
        strategy=strategy,
    )

    return ApiResponse({"pruned_count": pruned_count})


@retry_db
async def copy_thread(request: ApiRequest):
    thread_id = request.path_params["thread_id"]
    async with connect() as conn:
        iter = await Threads.copy(conn, thread_id)

    thread_data = await fetchone(iter, not_found_code=409)
    return ApiResponse(thread_data)


@retry_db
async def join_thread_stream(request: ApiRequest):
    """Join a thread stream."""
    thread_id = request.path_params["thread_id"]
    validate_uuid(thread_id, "Invalid thread ID: must be a UUID")
    last_event_id = request.headers.get("last-event-id") or None
    validate_stream_id(
        last_event_id, "Invalid last-event-id: must be a valid Redis stream ID"
    )

    # Parse stream_modes parameter - can be single string or comma-separated list
    stream_modes_param = request.query_params.get("stream_modes")
    if stream_modes_param:
        if "," in stream_modes_param:
            # Handle comma-separated list
            stream_modes = [mode.strip() for mode in stream_modes_param.split(",")]
        else:
            # Handle single value
            stream_modes = [stream_modes_param]
        # Validate each mode
        for mode in stream_modes:
            if mode not in get_args(ThreadStreamMode):
                raise HTTPException(
                    status_code=422, detail=f"Invalid stream mode: {mode}"
                )
    else:
        # Default to run_modes
        stream_modes = ["run_modes"]

    return EventSourceResponse(
        Threads.Stream.join(
            thread_id,
            last_event_id=last_event_id,
            stream_modes=stream_modes,
        ),
    )


threads_routes: list[BaseRoute] = [
    ApiRoute("/threads", endpoint=create_thread, methods=["POST"]),
    ApiRoute("/threads/search", endpoint=search_threads, methods=["POST"]),
    ApiRoute("/threads/count", endpoint=count_threads, methods=["POST"]),
    ApiRoute("/threads/prune", endpoint=prune_threads, methods=["POST"]),
    ApiRoute("/threads/{thread_id}", endpoint=get_thread, methods=["GET"]),
    ApiRoute("/threads/{thread_id}", endpoint=patch_thread, methods=["PATCH"]),
    ApiRoute("/threads/{thread_id}", endpoint=delete_thread, methods=["DELETE"]),
    ApiRoute("/threads/{thread_id}/state", endpoint=get_thread_state, methods=["GET"]),
    ApiRoute(
        "/threads/{thread_id}/storage", endpoint=get_thread_storage, methods=["GET"]
    ),
    ApiRoute(
        "/threads/{thread_id}/state", endpoint=update_thread_state, methods=["POST"]
    ),
    ApiRoute(
        "/threads/{thread_id}/history", endpoint=get_thread_history, methods=["GET"]
    ),
    ApiRoute("/threads/{thread_id}/copy", endpoint=copy_thread, methods=["POST"]),
    ApiRoute(
        "/threads/{thread_id}/history",
        endpoint=get_thread_history_post,
        methods=["POST"],
    ),
    ApiRoute(
        "/threads/{thread_id}/state/{checkpoint_id}",
        endpoint=get_thread_state_at_checkpoint,
        methods=["GET"],
    ),
    ApiRoute(
        "/threads/{thread_id}/state/checkpoint",
        endpoint=get_thread_state_at_checkpoint_post,
        methods=["POST"],
    ),
    ApiRoute(
        "/threads/{thread_id}/stream",
        endpoint=join_thread_stream,
        methods=["GET"],
    ),
]
