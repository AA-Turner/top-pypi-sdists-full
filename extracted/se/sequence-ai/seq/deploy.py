"""
`seq.deploy` and the deploy payload — introspect a `@seq.policy` class into the `POST /v1/deployments` body and submit
it, or register a `@seq.benchmark` class; the SDK's side of `seq deploy`.

WHY assembly lives apart from `@seq.policy` registration: registration captures the policy's declaration
(a `PolicyRegistration` a harness reads with sequence_base alone); deploy TRANSLATES that declaration into
the gateway's request shape. The SDK builds no image and pulls no weights: it emits the spec the platform's builder
consumes.

The `weights=` URI expands here to the deploy body's `weights` `VolumeMount{uri, mount=/data}` — a
provisioned pull. No secret value ever enters this payload: `DeploymentRequest` has no secrets field, and secrets
travel name-only in the registration, injected at worker bootstrap.
"""
from __future__ import annotations

from typing import Callable, Optional

from sequence_base.contract import (
    Autoscaler,
    Concurrency,
    DeploymentPolicy,
    DeploymentRequest,
    DeploymentState,
    DeploymentStatusResponse,
    Resources,
)

from seq.code_bundle import pack, pack_dir, with_sources
from seq.errors import PolicyDefinitionError, build_failed, still_building
from seq.project_deps import image_for
from seq.registry import (
    context_declared,
    image_declared,
    importable,
    locals_declared,
    infer_params,
    registration,
    models_declared,
    resources_declared,
)
from seq.weights import DEFAULT_WEIGHTS_MOUNT, weights_volume_mount






def deployment_request(
    cls: type,
    *,
    cpu: float | None = None,
    memory_gb: float | None = None,
    name: str | None = None,
    snapshots: list | None = None,
) -> DeploymentRequest:
    """Introspect a `@seq.policy` class into a full `POST /v1/deployments` body. The `image` / `weights` /
    `resources` parts are produced from the registration. Nothing is built or pulled — the returned request is pure
    data. Its code is the folder the policy was imported from, whole (seq.code_bundle.pack; `seq deploy [folder]`
    imports it from the folder it deploys); what was uploaded is appended to `snapshots` when given, for the deploy to
    say it."""
    reg = registration(cls)



    importable(cls)
    spec = reg.spec
    if name is not None:
        from seq.registry import check_new_name

        check_new_name(name)



    declared = resources_declared(cls)
    cpu = cpu or declared["cpu"]
    memory_gb = memory_gb or declared["memory_gb"]
    context = context_declared(cls)
    declared_models = models_declared(cls)
    snap = pack(reg.handler_ref, local_files=locals_declared(cls)[0], python_sources=locals_declared(cls)[1])
    if snapshots is not None:
        snapshots.append(snap)



    image = image_for(with_sources(spec.image, snap.src_map), snap, handler_ref=reg.handler_ref,
                      kind="policy", declared=image_declared(cls))

    return DeploymentRequest(
        name=name or spec.name,
        image=image,
        weights=weights_volume_mount(spec.weights, DEFAULT_WEIGHTS_MOUNT) if spec.weights else None,

        weights_name=spec.weights_name,
        extra_weights=({n: weights_volume_mount(u, DEFAULT_WEIGHTS_MOUNT) for n, u in spec.extra_weights.items()}
                       if spec.extra_weights else None),

        resources=Resources(gpu=[spec.gpu], cpu=cpu, cpu_limit=declared["cpu_limit"], memory_gb=memory_gb,
                            memory_limit_gb=declared["memory_limit_gb"]),
        policy=DeploymentPolicy(
            handler_ref=reg.handler_ref,


            hz=spec.hz,
            action_chunk_valid_len=spec.action_chunk_valid_len,
            action_chunk_replan_at=spec.action_chunk_replan_at,

            max_wait_for_batch=spec.max_wait_for_batch,
            episodes=spec.episodes,


            params=infer_params(cls),




            secrets=list(spec.secrets),


            models=declared_models or None,


            plan_every_s=reg.plan_every_s,
        ),



        autoscaler=Autoscaler(
            min_containers=spec.min_containers,
            max_gpus=spec.max_gpus,
            buffer_containers=spec.buffer_containers,
        ),



        concurrency=spec.concurrency or Concurrency(),

        image_context=pack_dir(context) if context else None,

        code=snap.bundle,
    )


def _resolve_policy(cls: object) -> type:
    """Accept a decorated class (`seq.deploy(Cls)`) or a `module:Class` string naming one. A string is imported
    here; anything else must already be a class carrying a registration (validated downstream)."""
    if isinstance(cls, str):
        import importlib

        if ":" not in cls:
            raise PolicyDefinitionError(f"{cls!r} must be 'pkg.module:ClassName'")
        module_path, _, cls_name = cls.partition(":")
        module = importlib.import_module(module_path)
        obj = getattr(module, cls_name, None)
        if obj is None:
            raise PolicyDefinitionError(f"{cls!r}: no attribute {cls_name!r} in {module_path}")
        return obj
    return cls


class DeploymentHandle:
    """The referenceable identifier a `seq.deploy(Cls)` hands back — its value IS the deployment name
    (the platform's routing primary key, goal 26). It compares and stringifies as that name, so it drops
    straight into any place a name-string is expected (a later reference, `seq.eval(handle, …)`), while also
    carrying the observability surface: `.status()` (one GET) and `.wait()` (poll to a terminal state).

    Two forms are identity-equivalent (goal 26): `str(handle) == handle.name == the CLI's printed name`.
    """

    def __init__(self, name: str, client: object) -> None:
        self.name = name
        self._client = client

    def status(self) -> DeploymentStatusResponse:
        """One GET /v1/deployments/{name}: the current build state (building | ready | failed)."""
        return self._client.status(self.name)

    def wait(
        self,
        *,
        timeout_s: float | None = None,
        poll_interval_s: float | None = None,
        on_poll: Optional[Callable[[DeploymentStatusResponse], None]] = None,
    ) -> DeploymentStatusResponse:
        """Poll to a terminal state and return it. `failed` raises `sequence_ai.errors.Conflict` with
        `details["state"] == "failed"` (never a silent success, goal 23); still `building` at the bounded deadline
        raises `Unavailable` with `code == "timeout"` (never an infinite hang, goal 24)."""
        kwargs: dict = {}
        if timeout_s is not None:
            kwargs["timeout_s"] = timeout_s
        if poll_interval_s is not None:
            kwargs["poll_interval_s"] = poll_interval_s
        if on_poll is not None:
            kwargs["on_poll"] = on_poll
        final = self._client.wait(self.name, **kwargs)
        if final.status == DeploymentState.FAILED:
            raise build_failed(f"deployment {self.name!r}", final.error)
        if final.status != DeploymentState.READY:
            raise still_building(f"deployment {self.name!r}", f"seq policy status {self.name} --wait")
        return final


    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"DeploymentHandle({self.name!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DeploymentHandle):
            return self.name == other.name
        if isinstance(other, str):
            return self.name == other
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.name)


def deploy(
    cls: object,
    *,
    name: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    wait: bool = True,
    timeout_s: float | None = None,
    poll_interval_s: float | None = None,
) -> DeploymentHandle | str:
    """Deploy a `@seq.policy` class on the platform, or register a `@seq.benchmark` class — what `seq deploy <folder>`
    does, from Python.

    A policy: its declaration becomes the `POST /v1/deployments` body (assembled here first, so a doomed one — no
    @seq.infer, missing weights, a handler the worker could not import — is refused before anything is sent), and the
    returned `DeploymentHandle` stands for the deployment name. A benchmark: its declaration and source become the
    `POST /v1/benchmarks` body, and its name comes back. `wait=True` (the default, as in `seq deploy`) blocks until the
    platform's build is ready, raising when it fails or outlasts `timeout_s`. `name` replaces the declared name.
    The API key is a Bearer credential only, never in the payload or any output."""
    target = _resolve_policy(cls)
    from seq.benchmark_registry import _BENCH_ATTR

    if _BENCH_ATTR in getattr(target, "__dict__", {}):
        return _register_benchmark(target, name=name, base_url=base_url, api_key=api_key, wait=wait,
                                   timeout_s=timeout_s)
    from seq._deploy_gateway import DeploymentsClient

    request = deployment_request(target, name=name)
    client = DeploymentsClient(api_key=api_key, base_url=base_url)
    accepted = client.submit(request)
    handle = DeploymentHandle(accepted.deployment_id, client)
    if wait:
        handle.wait(timeout_s=timeout_s, poll_interval_s=poll_interval_s)
    return handle


def _register_benchmark(cls: type, *, name: str | None, base_url: str | None, api_key: str | None, wait: bool,
                        timeout_s: float | None) -> str:
    """POST the benchmark's declaration and source; with `wait`, until the platform has built its sim image."""
    from seq._eval_gateway import BENCHMARK_WAIT_S, EvalGatewayClient
    from seq.benchmark_registry import benchmark_request

    request = benchmark_request(cls, name=name)
    client = EvalGatewayClient(api_key=api_key, base_url=base_url)
    client.register(request)
    if not wait:
        return request.name

    stalled: list[float] = []
    final = client.wait_benchmark(request.name, timeout_s=timeout_s or BENCHMARK_WAIT_S,
                                  while_moving=timeout_s is None, on_stall=stalled.append)
    if final.status == DeploymentState.FAILED:
        raise build_failed(f"benchmark {request.name!r}", final.error)
    if final.status != DeploymentState.READY:
        from seq._eval_gateway import BUILD_MOVED_S

        raise still_building(f"benchmark {request.name!r}", f"seq benchmark status {request.name} --wait",
                             stalled_s=BUILD_MOVED_S if stalled else None)
    return request.name
