"""Directly invoke a model deployed to a scaling group."""

from __future__ import annotations

import collections.abc
import logging
from typing import TYPE_CHECKING, Any, List, Mapping, Optional, Sequence, Tuple
from urllib.parse import urlsplit

import grpc

if TYPE_CHECKING:
    import pyarrow as pa
    from chalkcompute import RemoteCallClient  # pyright: ignore[reportMissingImports]

    from chalk.client.client_grpc import ChalkGRPCClient

logger = logging.getLogger(__name__)
DEFAULT_HANDLER = "handler"


class ModelRemoteError(RuntimeError):
    pass


class ModelNotDeployedError(ModelRemoteError):
    """Model/scaling group exists but has no reachable ingress."""


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


def resolve_scaling_group_web_url(
    client: "ChalkGRPCClient",
    model_name: str,
    *,
    version: Optional[int] = None,
) -> str:
    """Resolve the public ``web_url`` of the scaling group serving a model version.

    Uses ``version`` (or the model's latest) to look up its deployed scaling group.
    """
    from chalk._gen.chalk.modeldeployment.v1 import service_pb2 as md_pb
    from chalk._gen.chalk.models.v1.model_version_pb2 import ModelVersionIdentifier
    from chalk._gen.chalk.server.v1.model_registry_pb2 import GetModelRequest

    resolved_version = version
    if resolved_version is None:
        try:
            model_resp = client._stub_refresher.call_model_stub(  # pyright: ignore[reportPrivateUsage]
                lambda x: x.GetModel(GetModelRequest(model_name=model_name))
            )
        except grpc.RpcError as e:
            raise ModelNotDeployedError(f"Model {model_name!r} not found: {e.details()}") from e
        resolved_version = model_resp.model.latest_model_version.version
        if not resolved_version:
            raise ModelNotDeployedError(f"Model {model_name!r} has no published versions")

    selector = md_pb.ModelVersionSelector(
        model_name=model_name,
        identifier=ModelVersionIdentifier(version=resolved_version),
    )
    list_resp = client._stub_refresher.call_model_deployment_stub(  # pyright: ignore[reportPrivateUsage]
        lambda x: x.ListModelScalingGroups(md_pb.ListModelScalingGroupsRequest(model_version=selector))
    )
    for group in list_resp.scaling_groups:
        if group.web_url:
            return group.web_url
    raise ModelNotDeployedError(f"Model {model_name!r} v{resolved_version} has no scaling group with a web URL")


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
        raise ModelRemoteError("Empty response from scaling group")
    batches = list(pa.ipc.open_stream(chunks[0]))
    if not batches:
        raise ModelRemoteError("Response from scaling group contained no record batches")
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


def call_model_scaling_group(
    client: "ChalkGRPCClient",
    model_name: str,
    inputs: "Mapping[str, Sequence[Any]] | pa.RecordBatch | pa.Table",
    *,
    version: Optional[int] = None,
    handler: str = DEFAULT_HANDLER,
    web_url: Optional[str] = None,
) -> "pa.RecordBatch":
    """Invoke a deployed model by calling its scaling group ingress directly.

    ``inputs`` is a column mapping or pyarrow batch/table whose column order
    matches the model's input schema.

    ``web_url`` possibly passed from DeployedModelVersion.remote() to skip re-resolution.
    """
    if web_url is None:
        web_url = resolve_scaling_group_web_url(client, model_name, version=version)
    target, use_tls = _grpc_target_from_url(web_url)
    metadata = client._get_remote_call_metadata()  # pyright: ignore[reportPrivateUsage]
    feather_bytes = _encode_inputs(inputs)
    chunks = _transport_call(target, use_tls, handler, feather_bytes, metadata)
    return _decode_output(chunks)


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
    model_name: str,
    inputs: "Mapping[str, Sequence[Any]] | pa.RecordBatch | pa.Table",
) -> Tuple[str, bytes]:
    """Enqueue one call, returning ``(call_id, request_bytes)``.

    The queue name is the bare model name, matching the scaling group's
    ``CHALK_FNQ_FUNCTION_NAME``. One queue per model, shared across versions: the
    deployed revision draining it serves the call.

    The encoded request is returned so callers can resubmit it after a transient failure.
    """
    feather_bytes = _encode_inputs(inputs)
    call_id = queue_client.enqueue(model_name, feather_bytes)
    return call_id, feather_bytes
