"""Plato SDK v2 - Models."""

from __future__ import annotations

from pydantic import BaseModel, Field

from plato._generated.models import EnvironmentContext, SessionContext, WaitForReadyResult


class EnvironmentContextWithMesh(EnvironmentContext):
    """EnvironmentContext plus the SDK-local ``mesh_ip``.

    The backend's canonical EnvironmentContext schema carries no ``mesh_ip`` —
    the SDK resolves it client-side (from wait-for-ready / job info) and keeps
    it on the context for SSH-user registration and host resolution. Contexts
    parsed from server responses stay plain EnvironmentContext (``extra="allow"``
    preserves any extras); locally built contexts use this subclass so the
    field is typed instead of smuggled through pydantic extras.
    """

    mesh_ip: str | None = None


def env_context_mesh_ip(ctx: EnvironmentContext) -> str | None:
    """Read ``mesh_ip`` off any EnvironmentContext variant, or None.

    Locally built contexts are EnvironmentContextWithMesh (typed field);
    server-parsed contexts are plain EnvironmentContext, where a mesh_ip in the
    payload survives only as a pydantic extra — and plain attribute access
    raises AttributeError when it's absent entirely.
    """
    if isinstance(ctx, EnvironmentContextWithMesh):
        return ctx.mesh_ip
    mesh_ip = (ctx.model_extra or {}).get("mesh_ip")
    return mesh_ip if isinstance(mesh_ip, str) else None


def context_with_mesh_ips(
    context: SessionContext,
    results: dict[str, WaitForReadyResult] | None,
) -> SessionContext:
    """Fold each job's ``mesh_ip`` from the wait-for-ready results into its env context.

    The backend delivers ``mesh_ip`` on the per-job wait-for-ready result
    (``WaitForReadyResult.mesh_ip``), never on ``EnvironmentContext``. The
    ``create`` / ``wait_until_ready`` paths otherwise assign ``response.context``
    verbatim, leaving envs with no mesh address — unlike ``add_env``, which
    populates it. This upgrades each env to ``EnvironmentContextWithMesh`` with
    the resolved ``mesh_ip`` so ``Environment.mesh_ip`` and mesh networking work
    on every code path.
    """
    if not context.envs:
        return context
    results = results or {}
    envs: list[EnvironmentContext] = []
    for ctx in context.envs:
        data = ctx.model_dump()
        result = results.get(ctx.job_id)
        # Prefer the wait-for-ready mesh_ip; fall back to any server-sent extra.
        data["mesh_ip"] = (result.mesh_ip if result else None) or data.get("mesh_ip")
        envs.append(EnvironmentContextWithMesh(**data))
    context.envs = envs
    return context


# ============================================================================
# Configuration Models
# ============================================================================


class SimConfig(BaseModel):
    """Compute configuration for a blank VM."""

    cpus: int = Field(default=1, ge=1, le=8, description="vCPUs")
    memory: int = Field(default=2048, ge=512, le=16384, description="Memory in MB")
    disk: int = Field(default=10240, ge=1024, le=102400, description="Disk space in MB")


class EnvOption(BaseModel):
    """Configuration for a single environment in a session.

    Each EnvOption creates one job/VM. Provide either:
    - artifact_id: Use a specific artifact/snapshot
    - sim_config: Start a blank VM with specified resources

    If neither is provided, resolves artifact via the prod-latest tag.
    """

    simulator: str = Field(description="Simulator name (e.g., 'espocrm')")
    alias: str | None = Field(
        default=None,
        description="Custom name for this environment (defaults to simulator name)",
    )
    artifact_id: str | None = Field(default=None, description="Specific artifact/snapshot ID to use")
    sim_config: SimConfig | None = Field(
        default=None,
        description="Compute config for blank VM (mutually exclusive with artifact_id)",
    )

    @classmethod
    def from_simulator(cls, simulator: str, alias: str | None = None) -> EnvOption:
        """Create an EnvOption from just a simulator name (uses prod-latest artifact)."""
        return cls(simulator=simulator, alias=alias)

    @classmethod
    def from_artifact(cls, simulator: str, artifact_id: str, alias: str | None = None) -> EnvOption:
        """Create an EnvOption from a simulator and artifact_id."""
        return cls(simulator=simulator, artifact_id=artifact_id, alias=alias)

    @classmethod
    def blank_vm(
        cls,
        simulator: str,
        alias: str | None = None,
        cpus: int = 1,
        memory: int = 2048,
        disk: int = 10240,
    ) -> EnvOption:
        """Create an EnvOption for a blank VM with custom resources."""
        return cls(
            simulator=simulator,
            alias=alias,
            sim_config=SimConfig(cpus=cpus, memory=memory, disk=disk),
        )


class SandboxState(BaseModel):
    """Schema for one sandbox slot (``.plato/sandboxes/<name>.json``).

    All fields that can be persisted in the state file.
    """

    # Slot name within the working directory. Sandboxes are addressed by it
    # (`--name`, `$PLATO_SANDBOX`, `plato sandbox use`), so several can live in
    # one working directory instead of clobbering a single state file.
    name: str | None = None

    # Core identifiers
    session_id: str
    job_id: str
    public_url: str | None = None
    # Browser RDP viewer URL, set when the sandbox was started with
    # --manual-control (Windows/qemu VMs only).
    rdp_url: str | None = None

    # Mode and service
    mode: str  # "blank", "config", "artifact", "simulator"

    # Blank mode fields
    dataset: str | None = None
    provider: str | None = None
    cpus: int | None = None
    memory: int | None = None
    disk: int | None = None
    app_port: int | None = None
    messaging_port: int | None = None

    # Config mode fields
    plato_config_path: str | None = None

    # Simulator/artifact mode fields
    simulator_name: str | None = None
    artifact_id: str | None = None
    tag: str | None = None

    # SSH configuration
    ssh_config_path: str | None = None
    ssh_host: str | None = None
    ssh_command: str | None = None  # Full SSH command for copy-paste
    ssh_key_path: str | None = None  # Private key, so `stop` can clean it up

    # Process management
    heartbeat_pid: int | None = None

    # Lifecycle. expires_at is the idle lease the heartbeat enforces: it exits
    # (and the backend then reaps the VM) once expires_at passes, and commands
    # that use the sandbox push it forward by `timeout` — so an actively-used
    # sandbox stays alive and an abandoned one dies at most `timeout` after
    # the last touch. stopped_at marks a slot as dead so other commands (and
    # the heartbeat itself) stop targeting it.
    created_at: float | None = None
    expires_at: float | None = None
    timeout: float | None = None
    stopped_at: float | None = None

    # Network
    network_connected: bool = False

    # Chronos session attachment: when set, this sandbox's job was added to
    # the Plato session backing an existing Chronos session (via add-job)
    # instead of a fresh standalone session, so lifecycle commands must stay
    # job-scoped to avoid touching the shared session's other envs.
    attached: bool = False
    chronos_session_id: str | None = None
    # WireGuard mesh IP of the sandbox VM within the shared session's network.
    # Present for attached sandboxes (the session always has a mesh and add-job
    # joins the VM before ready). From VMs in the same session, SSH/tunnels use
    # this directly — in-VPC, no gateway NAT round-trip.
    mesh_ip: str | None = None
