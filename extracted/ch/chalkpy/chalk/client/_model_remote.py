"""Resolve model deployments and invoke them through their public URL or function queue."""

from __future__ import annotations

import collections.abc
import time
from typing import TYPE_CHECKING, Any, Callable, List, Mapping, Optional, Sequence, Tuple, TypeVar
from urllib.parse import urlsplit

import grpc

if TYPE_CHECKING:
    import pyarrow as pa
    from chalkcompute import RemoteCallClient  # pyright: ignore[reportMissingImports]

    from chalk.client.client_grpc import ChalkGRPCClient
    from chalk.client.model_deployment import ModelDeployment

T = TypeVar("T")
DEFAULT_HANDLER = "handler"


class ModelRemoteError(RuntimeError):
    pass


class ModelNotDeployedError(ModelRemoteError):
    """The model version has no active deployment."""


class ModelDeploymentNotReadyError(ModelNotDeployedError):
    """The model version's deployment exists but has no public URL yet."""


class ModelDeploymentAmbiguousError(ModelRemoteError):
    """Several deployments serve the model version; select one by ID or name."""


class ModelDeploymentMismatchError(ModelRemoteError):
    """The selected deployment does not serve the requested model version."""


def with_model_deployment_key(request: T, deployment_id: Optional[str], deployment_name: Optional[str]) -> T:
    """Set the request's ``model_scaling_group_key`` oneof from exactly one of the deployment's ID or name."""
    if deployment_id is not None and deployment_name is None:
        setattr(request, "model_scaling_group_id", deployment_id)
    elif deployment_name is not None and deployment_id is None:
        setattr(request, "model_scaling_group_name", deployment_name)
    else:
        raise ValueError("Provide exactly one of the model deployment's id or name")
    return request


def bind_inputs(
    input_features: Sequence[str],
    args: Sequence[Any],
    kwargs: Mapping[str, Any],
) -> "dict[str, list[Any]]":
    """Bind one row of positional/keyword args to ``input_features`` -> ``{feature: [value]}``."""
    if len(args) > len(input_features):
        raise ValueError(f"Expected at most {len(input_features)} positional args, got {len(args)}")
    bound: dict[str, Any] = dict(zip(input_features, args))
    for key, value in kwargs.items():
        if key not in input_features:
            raise ValueError(f"Unknown input feature {key!r}; expected one of {list(input_features)}")
        if key in bound:
            raise ValueError(f"Input feature {key!r} given both positionally and by keyword")
        bound[key] = value
    missing = [f for f in input_features if f not in bound]
    if missing:
        raise ValueError(f"Missing input features: {missing}")
    return {f: [bound[f]] for f in input_features}


def _grpc_target_from_url(web_url: str) -> Tuple[str, bool]:
    """``https://host`` -> ``("host:443", True)``; explicit port and ``http://`` are honored."""
    parsed = urlsplit(web_url)
    use_tls = parsed.scheme != "http"
    host = parsed.hostname or ""
    if parsed.port:
        return f"{host}:{parsed.port}", use_tls
    if use_tls:
        return f"{host}:443", True
    return host, False


def _list_deployments_serving(client: "ChalkGRPCClient", model_name: str, version: int) -> "ModelDeployment":
    from chalk._gen.chalk.modeldeployment.v1 import service_pb2 as md_pb
    from chalk._gen.chalk.models.v1.model_version_pb2 import ModelVersionIdentifier
    from chalk.client.model_deployment import model_deployments_from_response

    # Two results are enough to tell a unique deployment from an ambiguous one.
    request = md_pb.ListModelScalingGroupsRequest(
        model_version=md_pb.ModelVersionSelector(
            model_name=model_name,
            identifier=ModelVersionIdentifier(version=version),
        ),
        limit=2,
    )
    response = client._stub_refresher.call_model_deployment_stub(  # pyright: ignore[reportPrivateUsage]
        lambda stub: stub.ListModelScalingGroups(request)
    )
    groups = model_deployments_from_response(response, client)
    if not groups:
        raise ModelNotDeployedError(f"Model {model_name!r} v{version} has no active deployment")
    if len(groups) > 1:
        raise ModelDeploymentAmbiguousError(
            f"Model {model_name!r} v{version} is served by several deployments "
            + f"({', '.join(repr(g.name) for g in groups)}); select one with deployment_id or deployment_name"
        )
    return groups[0]


def _get_selected_deployment(
    client: "ChalkGRPCClient",
    model_name: str,
    version: Optional[int],
    deployment_id: Optional[str],
    deployment_name: Optional[str],
) -> "ModelDeployment":
    from chalk._gen.chalk.modeldeployment.v1 import service_pb2 as md_pb
    from chalk._gen.chalk.server.v1.model_registry_pb2 import GetModelRequest
    from chalk.client.model_deployment import model_deployment_from_response

    label = f"id {deployment_id!r}" if deployment_id is not None else f"{deployment_name!r}"
    request = with_model_deployment_key(md_pb.GetModelScalingGroupRequest(), deployment_id, deployment_name)
    try:
        response = client._stub_refresher.call_model_deployment_stub(  # pyright: ignore[reportPrivateUsage]
            lambda stub: stub.GetModelScalingGroup(request)
        )
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:  # pyright: ignore[reportAttributeAccessIssue]
            raise ModelNotDeployedError(f"No model deployment {label}") from e
        raise
    try:
        group = model_deployment_from_response(response, client)
    except ValueError as e:
        raise ModelDeploymentMismatchError(f"Deployment {label} is not a model deployment") from e
    if group.model_id:
        try:
            model = client._stub_refresher.call_model_stub(  # pyright: ignore[reportPrivateUsage]
                lambda stub: stub.GetModel(GetModelRequest(model_name=model_name))
            ).model
        except grpc.RpcError as e:
            if e.code() != grpc.StatusCode.NOT_FOUND:  # pyright: ignore[reportAttributeAccessIssue]
                raise
            same_model = False
        else:
            same_model = model.id == group.model_id
    else:
        # Backfilled deployments without model_id retain the server's name-based check.
        same_model = group.model_name == model_name
    if not same_model or (version is not None and group.model_version != version):
        requested = f"{model_name!r}" + (f" v{version}" if version is not None else "")
        raise ModelDeploymentMismatchError(
            f"Deployment {group.name!r} serves {group.model_name!r} v{group.model_version}, not {requested}"
        )
    return group


def resolve_model_deployment(
    client: "ChalkGRPCClient",
    model_name: str,
    *,
    version: Optional[int],
    deployment_id: Optional[str] = None,
    deployment_name: Optional[str] = None,
) -> "ModelDeployment":
    """Return the deployment that serves ``model_name`` v``version``.

    With ``deployment_id`` or ``deployment_name``, that deployment is used after checking it
    serves the model (and ``version``, when given). Without either, the version must be
    served by exactly one deployment.
    """
    if deployment_id is not None or deployment_name is not None:
        return _get_selected_deployment(client, model_name, version, deployment_id, deployment_name)
    if version is None:
        raise ValueError("A version is required unless a deployment is selected")
    return _list_deployments_serving(client, model_name, version)


def model_deployment_queue_name(group: Any, model_name: str) -> str:
    """The function queue a deployment consumes, as recorded on its selected revision.

    Revisions created before per-deployment queues consume the model-wide queue, matching
    how the server picks the queue for them.
    """
    queue_name = group.metadata["fnq_queue_name"].string_value if "fnq_queue_name" in group.metadata else ""
    return queue_name or model_name


def _encode_inputs(inputs: "Mapping[str, Sequence[Any]] | pa.RecordBatch | pa.Table") -> bytes:
    """Serialize inputs to Arrow IPC stream bytes (the format the runtime expects)."""
    import pyarrow as pa

    if isinstance(inputs, collections.abc.Mapping):
        arrays = {k: pa.array(v) for k, v in inputs.items()}
        batch = pa.record_batch(list(arrays.values()), names=list(arrays.keys()))
    elif isinstance(inputs, pa.RecordBatch):
        batch = inputs
    else:
        batches = inputs.combine_chunks().to_batches()
        batch = batches[0] if batches else pa.RecordBatch.from_pylist([], schema=inputs.schema)

    sink = pa.BufferOutputStream()
    with pa.ipc.new_stream(sink, batch.schema) as writer:
        writer.write_batch(batch)
    return sink.getvalue().to_pybytes()


def _decode_output(chunks: Sequence[bytes]) -> "pa.RecordBatch":
    import pyarrow as pa

    if not chunks:
        raise ModelRemoteError("Empty response from model deployment")
    batches = list(pa.ipc.open_stream(chunks[0]))
    if not batches:
        raise ModelRemoteError("Response from model deployment contained no record batches")
    return batches[0]


def _new_remote_call_client(
    target: str,
    use_tls: bool,
    metadata: Sequence[Tuple[str, str]],
) -> "RemoteCallClient":
    try:
        from chalkcompute import RemoteCallClient, RemoteCallClientUnavailable  # pyright: ignore[reportMissingImports]
    except ImportError as e:
        raise ImportError(
            "Install `chalkcompute` (`pip install 'chalkpy[compute]'`) to enable direct model calls."
        ) from e

    try:
        return RemoteCallClient(target, metadata=list(metadata), use_tls=use_tls)
    except RemoteCallClientUnavailable as e:
        raise ImportError("Reinstall `chalkcompute`: its native extension is missing.") from e


def _transport_call(
    target: str,
    use_tls: bool,
    handler: str,
    feather_bytes: bytes,
    metadata: Sequence[Tuple[str, str]],
) -> List[bytes]:
    remote_client = _new_remote_call_client(target, use_tls, metadata)
    try:
        return list(remote_client.call_ipc(handler, feather_bytes))
    finally:
        remote_client.close()


def is_stale_route_error(error: BaseException) -> bool:
    """Whether a direct call failed to reach the deployment, rather than the model rejecting it.

    Only connection-level failures qualify; status errors from the model are never retried.
    """
    try:
        from chalkcompute._remote_call_client import (  # pyright: ignore[reportMissingImports]
            RemoteCallTransportError,
            RemoteCallUnavailableError,
        )
    except ImportError:
        return False
    return isinstance(error, (RemoteCallTransportError, RemoteCallUnavailableError))


def call_model_url(
    client: "ChalkGRPCClient",
    web_url: str,
    inputs: "Mapping[str, Sequence[Any]] | pa.RecordBatch | pa.Table",
    *,
    handler: str = DEFAULT_HANDLER,
) -> "pa.RecordBatch":
    """Invoke a model by calling a deployment's public URL directly.

    ``inputs`` is a column mapping or pyarrow batch/table whose column order
    matches the model's input schema.
    """
    target, use_tls = _grpc_target_from_url(web_url)
    metadata = client._get_remote_call_metadata()  # pyright: ignore[reportPrivateUsage]
    return _decode_output(_transport_call(target, use_tls, handler, _encode_inputs(inputs), metadata))


def new_queue_client(client: "ChalkGRPCClient") -> "RemoteCallClient":
    """Client for the function-queue server fronted by the environment's grpc-engine ingress.

    The caller owns the returned client and must ``close()`` it — wrap in
    ``contextlib.closing`` when its lifetime is scoped.

    The Bearer token is captured at construction, so callers holding one across a
    long poll loop should rebuild rather than outlive the token.
    """
    try:
        target, use_tls = client._get_engine_grpc_target()  # pyright: ignore[reportPrivateUsage]
    except ValueError as e:
        raise ModelRemoteError(str(e)) from e
    metadata = client._get_queue_call_metadata()  # pyright: ignore[reportPrivateUsage]
    return _new_remote_call_client(target, use_tls, metadata)


def enqueue_model_call(
    queue_client: "RemoteCallClient",
    queue_name: str,
    inputs: "Mapping[str, Sequence[Any]] | pa.RecordBatch | pa.Table",
) -> Tuple[str, bytes]:
    """Enqueue one call, returning ``(call_id, request_bytes)``.

    The queue name comes from the selected deployment's stored revision.
    Legacy revisions retain their model-wide queue until redeployed.

    The encoded request is returned so callers can resubmit it after a transient failure.
    """
    feather_bytes = _encode_inputs(inputs)
    call_id = queue_client.enqueue(queue_name, feather_bytes)
    return call_id, feather_bytes


def _decode_first_value(chunks: Sequence[bytes]) -> Any:
    """First column of the first row across all result chunks.
    Unlike ``_decode_output``, this scans every chunk and batch: a queued result can
    arrive split across successive polls.
    """
    import pyarrow as pa

    for chunk in chunks:
        for batch in pa.ipc.open_stream(chunk):
            if batch.num_rows:  # Skip empty batches.
                return batch.column(0)[0].as_py()
    raise ModelRemoteError("Model call produced no output rows")


class ModelCallHandle:
    """Handle for a deferred model call, returned by ``DeployedModelVersion.defer()``."""

    def __init__(self, get_queue_client: Callable[[], "RemoteCallClient"], queue_name: str, call_id: str) -> None:
        super().__init__()
        self._get_queue_client = get_queue_client
        self._queue_name = queue_name
        self._call_id = call_id
        self._cursor = ""
        self._poll_count = 0
        self._chunks: List[bytes] = []
        self._done = False
        self._result: Any = None
        self._error: Optional[ModelRemoteError] = None

    @property
    def call_id(self) -> str:
        """Server-assigned id of the queued call."""
        return self._call_id

    def get(self, timeout: Optional[float] = None) -> Any:
        """Block until the call completes, returning what ``remote()`` would return.

        Raises ``ModelRemoteError`` if the call failed, or ``TimeoutError`` if
        ``timeout`` seconds elapse first.
        """
        if self._error is not None:
            raise self._error
        if self._done:
            return self._result

        deadline = None if timeout is None else time.monotonic() + timeout
        last_status = "unknown"

        while True:
            # poll_next blocks server-side and backs off internally, so this loop must not sleep.
            result = self._get_queue_client().poll_next(self._call_id, self._cursor, self._poll_count)
            self._cursor = result.cursor
            self._poll_count = result.poll_count
            last_status = result.status_name
            self._chunks.extend(result.chunks)

            if result.is_failed:
                self._error = ModelRemoteError(result.error_message or f"Model call {self._call_id} failed")
                raise self._error

            if result.is_completed:
                self._result = _decode_first_value(self._chunks)
                self._done = True
                return self._result

            if deadline is not None and time.monotonic() >= deadline:
                raise TimeoutError(
                    f"Model call {self._call_id} ({self._queue_name!r}) timed out (last status: {last_status})"
                )
