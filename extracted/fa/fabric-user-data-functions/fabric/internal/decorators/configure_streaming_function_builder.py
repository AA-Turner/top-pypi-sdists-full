"""
Builds a **streaming** User Data Function.

Unlike :mod:`fabric.internal.decorators.configure_fabric_function_builder` (which
wraps the user function so its result is buffered into a single
``azure.functions.HttpResponse``), this builder registers the function through
the Azure Functions **HTTP streams** path: the trigger parameter is typed as the
FastAPI-extension ``Request`` and the function returns a FastAPI
``StreamingResponse`` whose body is flushed to the client incrementally.

The user writes a normal function that returns a
:class:`fabric.functions.StreamResponse`; this builder adapts it.

.. note::
    The ``azurefunctions-extensions-http-fastapi`` package is imported lazily so
    that importing :mod:`fabric.functions` does not hard-require the streaming
    extension for classic (buffered) apps.
"""

# flake8: noqa: I003
import inspect
from typing import Any, AsyncIterator, Callable, List

from azure.functions import FunctionApp
from azure.functions.decorators.http import HttpMethod

from fabric.functions.fabric_class import UserDataFunctionContext
from fabric.functions.stream_response import StreamResponse
from fabric.functions.udf_exception import UserDataFunctionInvalidInputError
from fabric.internal.converters.basic_datatype_converter import BasicDatatypeConverter
from fabric.internal.invoke_response import StatusCode
from fabric.internal.logging import UdfLogger
from fabric.internal.user_data_function_context_binding import (
    UserDataFunctionContextInput,
)

from fabric.internal.providers import ProviderFactory, ProviderMetadata

from .configure_fabric_function_builder import _is_typeof_fabricitem_input
from .function_parameter_keywords import (
    REQ_PARAMETER,
    UNUSED_FABRIC_CONTEXT_PARAMETER,
)

logger = UdfLogger(__name__)


def apply_fabric_item_providers(
    fabric_item_params: list,
    kwargs: dict,
    func_name: str,
    req: Any,
    provider_factory,
    provider_metadata,
) -> None:
    """Resolve and inject connection-backed FabricItem clients into kwargs.

    Local copy of ``fabric.internal.utils.parameter_utils.apply_fabric_item_providers``.
    That shared helper is introduced by the batch-support refactor which has not
    yet been released to ``main``; this release branch inlines the single function
    it needs so streaming connection injection ships without pulling in batch.
    """
    for arg in fabric_item_params:
        provider = provider_factory.get_provider(arg.annotation)
        if provider:
            item_args = provider_metadata.get_kwargs(func_name, arg.name)
            item = kwargs.get(arg.name, None)
            kwargs[arg.name] = provider.create(item=item, req=req, **item_args)

# Response header the classic (buffered) path stamps via
# ``enforce_formatted_returntype`` to report the invoke result. The FuncSet
# workload proxy reads this header to decide whether to buffer the body
# (``readContent``) and the Fabric host extension reads it for telemetry.
# Keep the literal in sync with ``ensure_formatted_returntype.py``.
_UDF_STATUS_HEADER = "x-fabric-udf-status"


def configure_streaming_function_builder(
    udf: FunctionApp, name: str = None
) -> Callable[..., Any]:
    """Return a decorator that registers ``func`` as a streaming UDF on ``udf``."""

    try:
        from azurefunctions.extensions.http.fastapi import (
            Request as FastApiRequest,
            StreamingResponse as FastApiStreamingResponse,
        )
    except ImportError as e:  # pragma: no cover - environment guard
        raise ImportError(
            "Streaming User Data Functions require the "
            "'azurefunctions-extensions-http-fastapi' package. Add it to your "
            "requirements.txt and redeploy."
        ) from e

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        route_name = name or func.__name__
        user_params = [
            p
            for p in inspect.signature(func).parameters.values()
            if p.name not in ("self",)
        ]

        # Connection-backed "fabric item" params (injected by the host via the
        # stacked connection decorator's binding) vs plain scalar params (parsed
        # from the request body) -- mirrors the classic builder's param split.
        fabric_item_params = [
            p for p in user_params if _is_typeof_fabricitem_input(p.annotation)
        ]
        body_params = [
            p for p in user_params if not _is_typeof_fabricitem_input(p.annotation)
        ]

        async def _streaming_entry(req, **kwargs):
            # Scalars come from the JSON body; connection params are injected by
            # the host as kwargs. Merge, then upgrade provider-backed FabricItems
            # (Cosmos -> CosmosClient, KeyVault -> SecretClient) via the shared
            # provider utility; plain FabricItem / Kusto pass through as-is. Extra
            # host kwargs (e.g. ``notusedfabriccontext``) are absorbed by ``**kwargs``.
            call_kwargs = await _parse_params(req, body_params)
            # gRPC binding and the local-run / notebook harness deliver scalars as
            # named kwargs, not in the body -- prefer those over the parsed value.
            for p in body_params:
                if p.name in kwargs:
                    call_kwargs[p.name] = kwargs[p.name]
            for p in fabric_item_params:
                if p.name in kwargs:
                    call_kwargs[p.name] = kwargs[p.name]
            if fabric_item_params:
                apply_fabric_item_providers(
                    fabric_item_params,
                    call_kwargs,
                    route_name,
                    req,
                    ProviderFactory(),
                    ProviderMetadata(),
                )

            result = func(**call_kwargs)
            if inspect.isawaitable(result):
                result = await result

            if not isinstance(result, StreamResponse):
                raise TypeError(
                    f"Streaming function '{route_name}' must return a "
                    f"fabric.functions.StreamResponse, got "
                    f"{type(result).__name__!r}."
                )

            body = _to_async_byte_iterator(result.content)
            # Type A streaming status: stamp the same ``x-fabric-udf-status`` header
            # the classic (buffered) path emits via ``enforce_formatted_returntype``,
            # so the FuncSet workload proxy recognizes a successful UDF response
            # (its ``readContent`` gate keys off this header) without buffering the
            # stream, and the host extension records it for telemetry.
            #
            # Caveat: a streaming response flushes headers BEFORE the body is
            # produced, so the status is necessarily optimistic. If the function
            # raises mid-stream the header already said ``Succeeded`` and cannot be
            # retracted (the bytes are already on the wire). A user-supplied
            # ``x-fabric-udf-status`` (via ``StreamResponse.headers``) wins.
            stream_headers = dict(result.headers or {})
            # HTTP header names are case-insensitive, so honor a user-supplied
            # status header in any casing instead of stamping a duplicate default.
            has_udf_status = any(
                k.lower() == _UDF_STATUS_HEADER for k in stream_headers
            )
            if not has_udf_status:
                # Only claim success for a successful HTTP status. A StreamResponse
                # with a non-2xx ``status_code`` (e.g. an upstream error relayed by
                # the ``dax_streaming`` example) gets ``Failed`` so the Fabric status
                # does not contradict the HTTP status; callers can still override
                # explicitly via ``StreamResponse.headers``.
                try:
                    http_status = int(result.status_code or 200)
                except (TypeError, ValueError):
                    http_status = 200
                stream_headers[_UDF_STATUS_HEADER] = (
                    StatusCode.SUCCEEDED
                    if 200 <= http_status < 300
                    else StatusCode.FAILED
                )
            return FastApiStreamingResponse(
                body,
                media_type=result.media_type,
                status_code=result.status_code,
                headers=stream_headers or None,
            )

        # Reshape the registered entry's signature + annotations so the Fabric
        # metadata pipeline sees a streaming UDF on par with a classic
        # ``@udf.function()``:
        #
        #   * ``req: FastApiRequest`` + ``return: FastApiStreamingResponse`` keep
        #     the worker in ASGI HTTP-streaming mode (the fastapi extension keys
        #     streaming detection on these annotation *types*).
        #   * The ``notusedfabriccontext`` sentinel param + binding force the
        #     Fabric host extension to load, exactly as the classic path does.
        #   * ``old_return = StreamResponse`` is what
        #     ``metadata_generator`` reads for ``fabricFunctionReturnType``;
        #     without it the function metadata carries a "return type must be
        #     annotated" error and the publish/invoke surface is incomplete.
        #
        # IMPORTANT: plain user params (e.g. ``count``) are deliberately NOT placed
        # in ``__signature__``. The worker's ``validate_function_params`` requires
        # every non-trigger signature parameter to have a matching binding; a plain
        # param has no binding, so including it raises FunctionLoadError ("declared
        # in Python but not in the function definition"). The classic builder
        # (``configure_fabric_function_builder``) keeps plain params out of the
        # signature for exactly this reason and parses them from the request body
        # at runtime. We do the same: ``user_params`` (captured above) drive
        # ``_parse_params`` inside ``_streaming_entry``; the signature carries only
        # the trigger + context params, which have real bindings.
        entry_params = [
            inspect.Parameter(
                REQ_PARAMETER,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=FastApiRequest,
            ),
            inspect.Parameter(
                UNUSED_FABRIC_CONTEXT_PARAMETER,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=UserDataFunctionContext,
            ),
        ]

        # Connection params (unlike scalars) go into the registered signature with
        # their real annotations so the indexer binds the connection decorator's
        # FabricItemInput to them and the host injects the FabricItem.
        for p in fabric_item_params:
            entry_params.append(
                inspect.Parameter(
                    p.name,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=p.annotation,
                )
            )

        annotations = {p.name: p.annotation for p in entry_params}
        annotations["return"] = FastApiStreamingResponse
        # Read by fabric.metadata.metadata_generator for fabricFunctionReturnType.
        annotations["old_return"] = StreamResponse

        _streaming_entry.__signature__ = inspect.Signature(
            entry_params, return_annotation=FastApiStreamingResponse
        )
        _streaming_entry.__annotations__ = annotations

        # Give the registered function the user's name so it surfaces correctly
        # in the host (route, function name, logs).
        _streaming_entry.__name__ = route_name
        _streaming_entry.__doc__ = func.__doc__

        # Register on the underlying FunctionApp using the standard v2 model.
        # Typing the trigger param as the FastAPI Request + returning a
        # StreamingResponse is what puts the worker into ASGI streaming mode.
        builder = udf.route(route=route_name, methods=[HttpMethod.POST])(
            _streaming_entry
        )

        # Force a Fabric binding so the Host Extension is loaded (mirrors the
        # classic ``@udf.function()`` path). The matching signature param above
        # lets the indexer associate this binding by name.
        builder.add_binding(
            binding=UserDataFunctionContextInput(
                name=UNUSED_FABRIC_CONTEXT_PARAMETER
            )
        )

        # Expose the original user function for unit testing / direct calls.
        func._fabric_streaming_entry = _streaming_entry  # type: ignore[attr-defined]
        func._fabric_function_builder = builder  # type: ignore[attr-defined]
        builder._fabric_streaming_entry = _streaming_entry  # type: ignore[attr-defined]
        builder._fabric_function_builder = builder  # type: ignore[attr-defined]

        # Return the builder (not the raw callable) so a stacked connection
        # decorator chains onto THIS streaming function: azure-functions'
        # ``_validate_type`` only reuses the last-registered builder when handed a
        # builder -- a plain callable spawns a fresh one around the un-reshaped
        # function (wrong signature, no streaming route). Required for connection
        # injection; matches the classic ``@udf.function()`` contract.
        return builder

    return decorator


def _get_cleaned_type(param: inspect.Parameter) -> Any:
    """
    Unwrap generic aliases (e.g. ``list[int]`` -> ``list``) to the bare origin
    type, matching ``configure_fabric_function_builder._get_cleaned_type_and_wrap_str``
    so the worker indexer and metadata generator see a concrete type.
    """
    annotation = param.annotation
    if hasattr(annotation, "__origin__"):
        return annotation.__origin__
    return annotation


async def _parse_params(
    req: Any, user_params: List[inspect.Parameter]
) -> dict:
    """
    Parse UDF parameters from the streaming request body.

    Mirrors the flat ``{paramName: value}`` JSON shape used by the classic
    (buffered) path in ``add_parameters`` so the request contract is identical.
    """
    try:
        body = await req.json()
    except Exception:
        body = {}
    if not isinstance(body, dict):
        body = {}

    kwargs: dict = {}
    for param in user_params:
        if param.name in body:
            annotation_name = getattr(param.annotation, "__name__", None)
            value = body[param.name]
            if annotation_name:
                try:
                    value = BasicDatatypeConverter.tryconvert(annotation_name, value)
                except Exception:
                    raise UserDataFunctionInvalidInputError(
                        properties={
                            "parameter_type": annotation_name,
                            "parameter_value": "Unable to parse",
                        }
                    )
            kwargs[param.name] = value
        elif param.default is not inspect.Parameter.empty:
            kwargs[param.name] = param.default
    return kwargs


def _to_async_byte_iterator(content: Any) -> AsyncIterator[bytes]:
    """
    Normalize any supported stream body (sync/async iterable of bytes/str) into
    an async iterator of ``bytes`` for the FastAPI ``StreamingResponse``.
    """

    def _ensure_bytes(chunk: Any) -> bytes:
        if isinstance(chunk, bytes):
            return chunk
        if isinstance(chunk, str):
            return chunk.encode("utf-8")
        if isinstance(chunk, (bytearray, memoryview)):
            return bytes(chunk)
        raise TypeError(
            f"Stream chunks must be bytes or str, got {type(chunk).__name__!r}."
        )

    if hasattr(content, "__aiter__"):

        async def _from_async() -> AsyncIterator[bytes]:
            async for chunk in content:
                yield _ensure_bytes(chunk)

        return _from_async()

    async def _from_sync() -> AsyncIterator[bytes]:
        for chunk in content:
            yield _ensure_bytes(chunk)

    return _from_sync()
