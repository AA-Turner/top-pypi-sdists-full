"""Typed model deployments: model-owned scaling groups, their revisions, and readiness."""

from __future__ import annotations

import dataclasses
import math
import random
import time
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Mapping, Optional, Sequence, Tuple, cast

import grpc

from chalk.client._model_remote import (
    ModelCallHandle,
    ModelDeploymentMismatchError,
    ModelDeploymentNotReadyError,
    ModelRemoteError,
    bind_inputs,
    call_model_url,
    enqueue_model_call,
    is_stale_route_error,
    model_deployment_queue_name,
)
from chalk.scalinggroup.spec import (
    AutoScalingSpec,
    GrpcReadinessProbe,
    GrpcStartupProbe,
    ScalingGroupResourceRequest,
    auto_scaling_spec_from_proto,
    auto_scaling_spec_to_proto,
)
from chalk.utils.collections import FrozenOrderedSet

if TYPE_CHECKING:
    from chalk.client.client_grpc import ChalkGRPCClient

DEPLOY_MODEL_VERSION_DEPRECATION = (
    "deploy_model_version_to_scaling_group() is deprecated; use create_model_deployment(), "
    + "which returns a typed ModelDeployment and can wait for readiness."
)

# Defaults the SDK adds to the env of images that run the Chalk handler shim.
HANDLER_SHIM_ENV_DEFAULTS = {"PYTHONPATH": "/app", "CHALK_FNQ_STREAMS_SUPPORTED": "true"}

# structpb carries numbers as float64, which represents integers exactly only up to 2**53 - 1.
_MAX_EXACT_STRUCT_INTEGER = 2**53 - 1

# Statuses reported for a deployment whose pods are serving. ``Degraded`` is ready only
# when it still meets the replica threshold.
_READY_STATUSES = FrozenOrderedSet(["Available", "Degraded"])
_SCALED_TO_ZERO_STATUS = "ScaledToZero"
# ``Failed`` is kept for older status producers that predate ``Error``.
_TERMINAL_STATUSES = FrozenOrderedSet(["Error", "Failed", "Unhealthy", "Deleted"])


class ModelDeploymentError(ModelRemoteError):
    """A model deployment lifecycle operation failed."""


class ModelDeploymentFailedError(ModelDeploymentError):
    """The deployment reached a terminal state while waiting for it to become ready."""

    def __init__(self, message: str, deployment: Optional["ModelDeployment"] = None) -> None:
        super().__init__(message)
        self.deployment = deployment


class ModelDeploymentTimeoutError(ModelDeploymentError, TimeoutError):
    """The deployment did not become ready before the timeout."""

    def __init__(self, message: str, deployment: "ModelDeployment") -> None:
        super().__init__(message)
        self.deployment = deployment


@dataclasses.dataclass(frozen=True)
class QueuePolicy:
    """Async model queue capacity and terminal result retention.

    ``max_items`` caps pending calls; ``result_ttl_seconds`` retains completed
    results, including failures. Both must be positive integers.
    """

    max_items: int = 500_000
    result_ttl_seconds: int = 86_400


@dataclasses.dataclass(frozen=True)
class ModelDeploymentSpec:
    """The complete serving spec for a new revision of a model deployment.

    `update_model_deployment` replaces the deployment's whole spec with this one: any
    field left at its default takes that default, and nothing is carried over from the
    current revision.

    Parameters
    ----------
    model_version
        Version of the deployment's model to serve.
    scaling
        Autoscaling configuration.
    resources
        Resource requests (CPU, memory, GPU).
    handler
        Dotted path to the handler function. Inferred for Chalk-built images.
    env_vars
        Extra environment variables for the container.
    secrets
        Secret Registry secrets (``chalkcompute.Secret``) to inject into the container.
    readiness_probe
        gRPC readiness probe.
    startup_probe
        gRPC startup probe. Defaults to the standard gRPC health check method.
    chalk_workload_identity
        Use Chalk workload identity for cloud resource access.
    retries
        Retries after the initial asynchronous execution; defaults to zero.
        Requires Redis Streams and uses the queue's fixed reclaim delay.
    queue_policy
        Pending-item capacity and asynchronous result retention.
    """

    model_version: int
    scaling: AutoScalingSpec
    resources: Optional[ScalingGroupResourceRequest] = None
    handler: Optional[str] = None
    env_vars: Optional[Mapping[str, str]] = None
    secrets: Optional[Sequence[Any]] = None
    readiness_probe: Optional[GrpcReadinessProbe] = None
    startup_probe: Optional[GrpcStartupProbe] = None
    chalk_workload_identity: bool = False
    retries: Optional[int] = None
    queue_policy: Optional[QueuePolicy] = None


@dataclasses.dataclass(frozen=True)
class ModelDeployment:
    """A model deployment: a stable, named endpoint serving one selected revision.

    ``remote()`` and ``defer()`` invoke the model it serves. ``refresh()`` and
    ``wait_ready()`` re-read it. All of them go through the client and environment that
    produced this object.
    """

    id: str
    name: str
    revision_id: str
    """The selected revision. After a rollback this is not the newest revision."""
    model_name: str
    model_version: int
    status: str
    status_message: Optional[str]
    scaling: AutoScalingSpec
    """The selected revision's autoscaling configuration."""
    resources: Optional[ScalingGroupResourceRequest]
    """The selected revision's resource requests, or ``None`` if none were set."""
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    web_url: Optional[str]
    """Public URL that ``remote()`` calls. Unset until routing is ready."""
    ready_replicas: int
    available_replicas: int
    model_id: Optional[str] = None
    """The owning registry model's stable ID, when returned by the API."""

    _client: Any = dataclasses.field(default=None, repr=False, compare=False)

    _queue_name: str = dataclasses.field(default="", repr=False, compare=False)
    """The function queue ``defer()`` enqueues on, preserved across revisions and model renames."""
    _input_features: Optional[Tuple[str, ...]] = dataclasses.field(default=None, repr=False, compare=False)
    """The served model version's input features, fetched on first call unless provided."""
    _live_web_url: Optional[str] = dataclasses.field(default=None, repr=False, compare=False)
    """Replaces ``web_url`` for calls after the URL changed under this snapshot."""
    _live_model_version: Optional[int] = dataclasses.field(default=None, repr=False, compare=False)
    """The version actually served, once a re-read found the deployment moved past ``model_version``."""
    _live_model_name: Optional[str] = dataclasses.field(default=None, repr=False, compare=False)
    """The current registry name after a re-read follows a model rename."""

    @property
    def min_replicas(self) -> int:
        return self.scaling.min_replicas

    def _bound_client(self) -> Any:
        if self._client is None:
            raise ModelDeploymentError("This ModelDeployment is not bound to a client")
        return self._client

    def _served_version(self) -> int:
        return self._live_model_version if self._live_model_version is not None else self.model_version

    def _bind(self, args: Sequence[Any], kwargs: Mapping[str, Any]) -> "dict[str, list[Any]]":
        input_features = self._input_features
        if input_features is None:
            input_features = self._fetch_input_features(self._served_version())
            object.__setattr__(self, "_input_features", input_features)
        return bind_inputs(input_features, args, kwargs)

    def _fetch_input_features(self, version: int, model_name: Optional[str] = None) -> Tuple[str, ...]:
        client = self._bound_client()
        model_name = model_name or _model_name_by_id(client, self.model_id, self._live_model_name or self.model_name)
        fields = client._model_version_fields(model_name, version)  # pyright: ignore[reportPrivateUsage]
        return tuple(fields["input_features"])

    def remote(self, *args: Any, **kwargs: Any) -> Any:
        """Invoke the model with one row of feature values, blocking until it responds.

        The call goes straight to this deployment's public URL, so it is served by
        whichever revision the deployment has selected.

        Parameters
        ----------
        args
            Feature values in the model version's ``input_features`` order.
        kwargs
            Feature values by name. A feature given both positionally and by keyword,
            an unknown name, or a missing feature raises ``ValueError`` before the
            model is called.

        Returns
        -------
        Any
            The model's first output value.

        Raises
        ------
        ValueError
            The arguments do not bind to the served version's input features.
        ModelDeploymentNotReadyError
            The deployment has no public URL yet.
        ModelDeploymentMismatchError
            A re-read found the deployment serving a different model.
        ModelRemoteError
            The deployment returned an error or an empty response.

        Examples
        --------
        >>> deployment = client.get_model_deployment(name="risk")
        >>> deployment.remote(txn_amount=42.0, account_age_days=365)
        0.83
        """
        client = self._bound_client()
        web_url = self._live_web_url or self.web_url
        if not web_url:
            # Resolve before binding: the deployment may now serve a version with other inputs.
            web_url = self._resolve_web_url()
        inputs = self._bind(args, kwargs)
        try:
            batch = call_model_url(client, web_url, inputs)
        except Exception as e:
            # A connection failure can mean routing moved; re-read the URL and retry once.
            if not is_stale_route_error(e):
                raise
            fresh_url, inputs = self._resolve_and_rebind(args, kwargs, inputs)
            if fresh_url == web_url:
                raise
            batch = call_model_url(client, fresh_url, inputs)
        return batch.column(0).to_pylist()[0]

    def _resolve_and_rebind(
        self, args: Sequence[Any], kwargs: Mapping[str, Any], inputs: "dict[str, list[Any]]"
    ) -> "tuple[str, dict[str, list[Any]]]":
        """Re-read the URL; if the served version changed, bind the call's arguments to its inputs."""
        served_before = self._served_version()
        web_url = self._resolve_web_url()
        if self._served_version() == served_before:
            return web_url, inputs
        try:
            return web_url, self._bind(args, kwargs)
        except ValueError as e:
            raise ValueError(
                f"Model deployment {self.name!r} now serves v{self._served_version()}, "
                + f"whose inputs do not match this call: {e}"
            ) from e

    def _resolve_web_url(self) -> str:
        """Re-read this deployment's URL, following it to whichever version it now serves."""
        fresh = self.refresh()
        same_model = (
            fresh.model_id == self.model_id
            if fresh.model_id and self.model_id
            else fresh.model_name == (self._live_model_name or self.model_name)
        )
        if not same_model:
            raise ModelDeploymentMismatchError(
                f"Model deployment {self.name!r} now serves model {fresh.model_name!r}, not {self.model_name!r}"
            )
        if not fresh.web_url:
            raise ModelDeploymentNotReadyError(
                f"Model deployment {self.name!r} has no public URL yet (status: {fresh.status or 'unknown'})"
            )
        if fresh.model_version != self._served_version():
            # Fetch the new schema before committing the version, so a failed fetch leaves
            # the cached version and inputs consistent.
            input_features = self._fetch_input_features(fresh.model_version, fresh.model_name)
            object.__setattr__(self, "_input_features", input_features)
            object.__setattr__(self, "_live_model_version", fresh.model_version)
        object.__setattr__(self, "_live_web_url", fresh.web_url)
        object.__setattr__(self, "_live_model_name", fresh.model_name)
        return fresh.web_url

    def defer(self, *args: Any, **kwargs: Any) -> ModelCallHandle:
        """Enqueue the call ``remote()`` would make onto this deployment's queue.

        ``handle.get()`` returns what ``remote()`` would have returned::

            handle = deployment.defer(1.0, 2.0)
            result = handle.get(timeout=30)

        Pending calls are consumed by whichever revision the deployment has selected
        when they run.
        """
        inputs = self._bind(args, kwargs)
        get_queue_client = self._bound_client()._get_queue_client
        queue_name = self._queue_name or self.model_name
        call_id, _ = enqueue_model_call(get_queue_client(), queue_name, inputs)
        return ModelCallHandle(get_queue_client, queue_name, call_id)

    def refresh(self) -> "ModelDeployment":
        """Re-read this deployment by its stable ID, returning a new object."""
        return self._bound_client().get_model_deployment(id=self.id, include_deleted=True)

    def wait_ready(self, *, timeout: float = 300, poll_interval: float = 2) -> "ModelDeployment":
        """Poll until the deployment can serve ``.remote()`` calls, returning the ready deployment.

        Ready means the status is serving, at least ``min_replicas`` replicas are ready,
        and the public URL is set. A deployment with ``min_replicas=0`` is also ready once
        it reports ``ScaledToZero`` with a URL.

        Raises
        ------
        ModelDeploymentFailedError
            The deployment reached ``Error``, ``Failed``, ``Unhealthy``, or ``Deleted``, or
            no longer exists.
        ModelDeploymentTimeoutError
            ``timeout`` seconds elapsed first. The error carries the last observed state.
        """
        start = time.monotonic()
        deadline = start + timeout
        current = self
        while True:
            if _is_ready(current):
                return current
            if current.status in _TERMINAL_STATUSES:
                raise ModelDeploymentFailedError(
                    f"Model deployment {current.name!r} ({current.id}) is {current.status}"
                    + (f": {current.status_message}" if current.status_message else ""),
                    current,
                )
            now = time.monotonic()
            if now >= deadline:
                raise ModelDeploymentTimeoutError(
                    f"Model deployment {current.name!r} ({current.id}) was not ready after "
                    + f"{now - start:.1f}s: status={current.status!r}"
                    + (f" ({current.status_message})" if current.status_message else "")
                    + f", ready_replicas={current.ready_replicas}, required_replicas={current.min_replicas}"
                    + f", web_url={'set' if current.web_url else 'unset'}",
                    current,
                )
            # Jitter keeps many waiting clients from polling in lockstep.
            time.sleep(max(0.0, min(poll_interval * random.uniform(0.8, 1.2), deadline - now)))
            try:
                current = current.refresh()
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.NOT_FOUND:  # pyright: ignore[reportAttributeAccessIssue]
                    raise ModelDeploymentFailedError(
                        f"Model deployment {current.name!r} ({current.id}) no longer exists", current
                    ) from e
                raise


def _is_ready(deployment: ModelDeployment) -> bool:
    if not deployment.web_url:
        return False
    if deployment.min_replicas == 0 and deployment.status == _SCALED_TO_ZERO_STATUS:
        return True
    return deployment.status in _READY_STATUSES and deployment.ready_replicas >= max(deployment.min_replicas, 1)


@dataclasses.dataclass(frozen=True)
class ModelDeploymentRevision:
    """One immutable revision of a model deployment."""

    id: str
    deployment_id: str
    deployment_name: str
    model_name: str
    model_version: int
    status: str
    status_message: Optional[str]
    created_at: Optional[datetime]
    deleted_at: Optional[datetime]
    selected: bool
    """Whether the deployment currently serves this revision (the wire field ``latest``).
    After a rollback, the selected revision is not the newest one."""


@dataclasses.dataclass(frozen=True)
class ListModelDeploymentsResponse:
    deployments: Sequence[ModelDeployment]
    next_cursor: Optional[str]
    """Pass back as ``cursor`` for the next page; ``None`` on the last page."""


@dataclasses.dataclass(frozen=True)
class ListModelDeploymentRevisionsResponse:
    revisions: Sequence[ModelDeploymentRevision]
    next_cursor: Optional[str]
    """Pass back as ``cursor`` for the next page; ``None`` on the last page."""


def model_version_from_metadata(metadata: Mapping[str, Any]) -> Tuple[str, int]:
    """Read ``(model_name, model_version)`` from a model scaling group's structpb metadata.

    Raises ``ValueError`` for a generic scaling group or malformed metadata; a
    fractional version is rejected rather than truncated.
    """
    if "model_name" not in metadata or metadata["model_name"].WhichOneof("kind") != "string_value":
        raise ValueError("Scaling group is not a model deployment: model_name metadata is missing or not a string")
    model_name = metadata["model_name"].string_value
    if not model_name:
        raise ValueError("Scaling group is not a model deployment: model_name metadata is empty")
    if "model_version" not in metadata or metadata["model_version"].WhichOneof("kind") != "number_value":
        raise ValueError("Scaling group is not a model deployment: model_version metadata is missing or not a number")
    number = metadata["model_version"].number_value
    if not math.isfinite(number) or not number.is_integer():
        raise ValueError(f"model_version metadata must be an integer, got {number!r}")
    if number < 0 or number > _MAX_EXACT_STRUCT_INTEGER:
        raise ValueError(f"model_version metadata {number!r} is outside the exact structpb integer range")
    return model_name, int(number)


def _timestamp(pb: Any, field: str) -> Optional[datetime]:
    if not pb.HasField(field):
        return None
    ts = getattr(pb, field)
    if not ts.seconds and not ts.nanos:
        return None
    return ts.ToDatetime(tzinfo=timezone.utc)


def _optional_str(pb: Any, field: str) -> Optional[str]:
    return getattr(pb, field) if pb.HasField(field) else None


def _resources_from_proto(container_spec: Any) -> Optional[ScalingGroupResourceRequest]:
    if not container_spec.HasField("resources"):
        return None
    limits = container_spec.resources
    return ScalingGroupResourceRequest(
        cpu=_optional_str(limits, "cpu"),
        memory=_optional_str(limits, "memory"),
        gpu=_optional_str(limits, "gpu"),
    )


def _model_name_by_id(
    client: Any, model_id: Optional[str], recorded_name: str, names: Optional[dict[str, str]] = None
) -> str:
    """Resolve the current name without allowing reuse of a revision's old name to change ownership."""
    if not model_id or client is None:
        return recorded_name
    if names is not None and model_id in names:
        return names[model_id]
    from chalk._gen.chalk.server.v1.model_registry_pb2 import GetModelRequest

    try:
        response = client._stub_refresher.call_model_stub(  # pyright: ignore[reportPrivateUsage]
            lambda stub: stub.GetModel(GetModelRequest(model_id=model_id, include_deleted=True))
        )
    except grpc.RpcError as e:
        if e.code() != grpc.StatusCode.NOT_FOUND:  # pyright: ignore[reportAttributeAccessIssue]
            raise
        # Archived deployments can outlive their registry model.
        name = recorded_name
    else:
        name = response.model.model_name
    if names is not None:
        names[model_id] = name
    return name


def model_deployment_from_proto(
    pb: Any,
    client: Optional["ChalkGRPCClient"] = None,
    *,
    record: Any = None,
    current_revision: Any = None,
    model_names: Optional[dict[str, str]] = None,
) -> ModelDeployment:
    """Prefer the model records, falling back to materialized scaling groups from older servers."""
    if record is not None and not record.id:
        record = None
    if record is not None and pb.id and record.id != pb.id:
        raise ValueError("Model deployment record does not match its scaling group")
    # The first API returning records did not yet include lifecycle state.
    source = record if record is not None and record.status else pb
    if current_revision is not None and current_revision.id:
        if current_revision.model_scaling_group_id != (record.id if record is not None else pb.id):
            raise ValueError("Model revision does not belong to its deployment")
        if source.revision_id and current_revision.id != source.revision_id:
            raise ValueError("Model revision is not the deployment's selected revision")
        model_name = current_revision.spec.model_version.model_name
        model_version = current_revision.model_version
        spec = current_revision.spec
    else:
        model_name, model_version = model_version_from_metadata(pb.metadata)
        spec = pb.spec
    model_id = _optional_str(record, "model_id") if record is not None else None
    model_name = _model_name_by_id(client, model_id, model_name, model_names)
    return ModelDeployment(
        id=record.id if record is not None else pb.id,
        name=record.name if record is not None else pb.name,
        revision_id=source.revision_id,
        model_name=model_name,
        model_version=model_version,
        status=source.status,
        status_message=_optional_str(source, "status_message"),
        scaling=auto_scaling_spec_from_proto(spec.scaling_spec),
        resources=_resources_from_proto(spec.container_spec),
        created_at=_timestamp(record if record is not None else pb, "created_at"),
        updated_at=_timestamp(source, "updated_at"),
        deleted_at=_timestamp(source, "deleted_at"),
        web_url=_optional_str(source, "web_url") or None,
        ready_replicas=source.ready_replicas,
        available_replicas=source.available_replicas,
        model_id=model_id,
        _client=client,
        _queue_name=(record.queue_name if record is not None else "") or model_deployment_queue_name(pb, model_name),
    )


def model_deployment_from_response(response: Any, client: "ChalkGRPCClient") -> ModelDeployment:
    return model_deployment_from_proto(
        response.scaling_group,
        client,
        record=response.model_scaling_group,
        current_revision=getattr(response, "current_revision", None),
    )


def model_deployments_from_response(response: Any, client: "ChalkGRPCClient") -> list[ModelDeployment]:
    from chalk._gen.chalk.scalinggroup.v1.service_pb2 import ScalingGroupResponse

    groups = {group.id: group for group in response.scaling_groups}
    revisions = {revision.model_scaling_group_id: revision for revision in response.current_revisions}
    names: dict[str, str] = {}
    if response.model_scaling_groups:
        return [
            model_deployment_from_proto(
                groups.get(record.id, ScalingGroupResponse()),
                client,
                record=record,
                current_revision=revisions.get(record.id),
                model_names=names,
            )
            for record in response.model_scaling_groups
        ]
    return [model_deployment_from_proto(group, client) for group in response.scaling_groups]


def model_deployment_revision_from_proto(pb: Any, model_revision: Any = None) -> ModelDeploymentRevision:
    """Use the model revision's immutable identity/spec and the scaling revision's runtime state."""
    if model_revision is not None and model_revision.id:
        if model_revision.id != pb.id or model_revision.model_scaling_group_id != pb.scaling_group_id:
            raise ValueError("Model revision does not match its scaling group revision")
        model_name = model_revision.spec.model_version.model_name
        model_version = model_revision.model_version
    else:
        model_revision = None
        model_name, model_version = model_version_from_metadata(pb.metadata)
    return ModelDeploymentRevision(
        id=pb.id,
        deployment_id=model_revision.model_scaling_group_id if model_revision is not None else pb.scaling_group_id,
        deployment_name=pb.scaling_group_name,
        model_name=model_name,
        model_version=model_version,
        status=pb.status,
        status_message=_optional_str(pb, "status_message"),
        created_at=_timestamp(model_revision if model_revision is not None else pb, "created_at"),
        deleted_at=_timestamp(pb, "deleted_at"),
        selected=pb.latest,
    )


@dataclasses.dataclass(frozen=True)
class ModelServingArtifact:
    """What deploying a model version needs from its registered artifact."""

    version: int
    volumes: Sequence[Mapping[str, Any]]
    image: Optional[str]
    """Image built at deploy time, or ``None`` to use the version's registered image."""
    serving_handler: Optional[str]
    """Handler of an image that runs the Chalk handler shim, else ``None``."""


def resources_to_proto(resources: ScalingGroupResourceRequest) -> Any:
    from chalk._gen.chalk.container.v1 import service_pb2 as container_pb

    return container_pb.ResourceLimits(cpu=resources.cpu, memory=resources.memory, gpu=resources.gpu)


def readiness_probe_to_proto(probe: GrpcReadinessProbe) -> Any:
    from chalk._gen.chalk.container.v1 import service_pb2 as container_pb

    return container_pb.ReadinessProbe(
        grpc=container_pb.GrpcHealthProbe(service=probe.service),
        period_seconds=probe.period_seconds,
        timeout_seconds=probe.timeout_seconds,
        failure_threshold=probe.failure_threshold,
    )


def startup_probe_to_proto(probe: GrpcStartupProbe) -> Any:
    from chalk._gen.chalk.container.v1 import service_pb2 as container_pb

    return container_pb.StartupProbe(grpc=container_pb.GrpcProbe(method=probe.method))


def model_queue_policies(retries: Optional[int], queue_policy: Optional[QueuePolicy]) -> dict[str, int]:
    """Validate asynchronous model policies before any image build or upload."""
    values: dict[str, int] = {}
    policies: tuple[tuple[str, object, int], ...] = (
        ("retries", cast(object, retries), 0),
        (
            "result_ttl_seconds",
            cast(object, queue_policy.result_ttl_seconds) if queue_policy is not None else None,
            1,
        ),
        (
            "max_items",
            cast(object, queue_policy.max_items) if queue_policy is not None else None,
            1,
        ),
    )
    for option, value, minimum in policies:
        if value is None:
            continue
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{option} must be an int")
        if not minimum <= value <= 2**31 - 1:
            raise ValueError(f"{option} must be between {minimum} and {2**31 - 1}")
        values[option] = value
    return values


def merge_model_spec(
    current: Any,
    *,
    artifact: Optional[ModelServingArtifact] = None,
    scaling: Optional[AutoScalingSpec] = None,
    resources: Optional[ScalingGroupResourceRequest] = None,
    handler: Optional[str] = None,
    env_vars: Optional[Mapping[str, str]] = None,
    secret_refs: Optional[Sequence[Any]] = None,
    readiness_probe: Optional[GrpcReadinessProbe] = None,
    startup_probe: Optional[GrpcStartupProbe] = None,
) -> Any:
    """Return a copy of a ``ModelScalingGroupSpec`` with the given fields replaced.

    Each argument that is not ``None`` replaces that whole field; everything else is kept.
    ``artifact`` switches the model version, replacing its image, handler, and volumes.
    """
    from google.protobuf import json_format

    from chalk._gen.chalk.container.v1 import service_pb2 as container_pb
    from chalk._gen.chalk.modeldeployment.v1 import service_pb2 as md_pb

    spec = md_pb.ModelScalingGroupSpec()
    spec.CopyFrom(current)
    container = spec.container_spec

    if env_vars is not None:
        new_env = dict(env_vars)
        # The handler-shim defaults were added by the SDK, not the user; keep them unless overridden.
        for key in HANDLER_SHIM_ENV_DEFAULTS:
            if key in container.env_vars and key not in new_env:
                new_env[key] = container.env_vars[key]
        container.env_vars.clear()
        container.env_vars.update(new_env)

    if artifact is not None:
        spec.model_version.identifier.version = artifact.version
        if artifact.image is not None:
            spec.image = artifact.image
        else:
            spec.ClearField("image")
        # The SDK mounts only model-artifact volumes, so a new version replaces all of them.
        del container.volumes[:]
        for volume in artifact.volumes:
            json_format.ParseDict(volume, container.volumes.add())
        effective_handler = handler if handler is not None else artifact.serving_handler
        if effective_handler is not None:
            spec.handler = effective_handler
        else:
            spec.ClearField("handler")
        if artifact.serving_handler is not None:
            for key, value in HANDLER_SHIM_ENV_DEFAULTS.items():
                if key not in container.env_vars:
                    container.env_vars[key] = value
    elif handler is not None:
        spec.handler = handler

    if scaling is not None:
        spec.scaling_spec.CopyFrom(auto_scaling_spec_to_proto(scaling))
    if resources is not None:
        if resources.cpu is None and resources.memory is None and resources.gpu is None:
            container.ClearField("resources")
        else:
            container.resources.CopyFrom(resources_to_proto(resources))
    if secret_refs is not None:
        del container.secret_refs[:]
        for ref in secret_refs:
            container.secret_refs.add().CopyFrom(
                ref if isinstance(ref, container_pb.SecretRef) else json_format.ParseDict(ref, container_pb.SecretRef())
            )
    if readiness_probe is not None:
        container.readiness_probe.CopyFrom(readiness_probe_to_proto(readiness_probe))
    if startup_probe is not None:
        container.startup_probe.CopyFrom(startup_probe_to_proto(startup_probe))
    return spec


__all__ = (
    "ListModelDeploymentRevisionsResponse",
    "ListModelDeploymentsResponse",
    "ModelDeployment",
    "ModelDeploymentError",
    "ModelDeploymentFailedError",
    "ModelDeploymentRevision",
    "ModelDeploymentSpec",
    "ModelDeploymentTimeoutError",
)
