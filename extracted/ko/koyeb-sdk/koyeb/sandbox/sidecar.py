# coding: utf-8

"""
Sidecars: trusted helper services that run next to a sandbox.

A sidecar is a separate service, with its own image, env,
secrets and egress policy, that the sandbox reaches by name over a private
mesh (``http://<name>:<port>``). Secrets given to a sidecar never enter the
sandbox, so a sidecar can hold API keys, run a credential-injecting proxy,
or host a helper service the agent should use but not touch.

This module only describes sidecars and builds their service definitions.
The create, wait and delete flow lives with the sandbox.

Each sidecar runs as a web service with no public route, a TCP health check
on its first port, and the mesh enabled with app scope. Since the sandbox
owns its app, the app scope makes the mesh private to the sandbox and its
sidecars.

The ``Sidecar`` fields and the ``Sandbox`` sidecar API are stable. How
sidecars are hosted is not: today they are services in the sandbox's app,
which ``SidecarInfo.service_id`` and the ``KOYEB_SIDECARS`` env reflect and
which may change when the platform runs sidecars natively.
"""

from __future__ import annotations

import ipaddress
import json
import math
import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

from koyeb.api.models.deployment_definition_type import DeploymentDefinitionType
from koyeb.api.models.deployment_health_check import DeploymentHealthCheck
from koyeb.api.models.deployment_port import DeploymentPort
from koyeb.api.models.mesh_scope import MeshScope
from koyeb.api.models.tcp_health_check import TCPHealthCheck

from .egress import build_egress_policy
from .errors import EgressPolicyError, SandboxTimeoutError, SidecarError
from .spec import SandboxSpec
from .status import classify_deployment_status

# A DNS label the API accepts as a service name: the sandbox reaches the
# sidecar at http://<name>:<port>. The API's slug rule allows no empty
# segment, so no "--" (and no "."; it would break the DNS name).
_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
_MIN_PORT, _MAX_PORT = 1, 64999  # the API reserves ports above 65000
_MAX_PORTS = 5
_MIN_GRACE, _MAX_GRACE = 5, 900  # API bounds for health check grace_period

# Set on the sandbox's env: its sidecars' names and ports, as JSON. Lets a
# handle from get_from_id find the sidecars without extra API calls for
# sandboxes that have none, and lets code in the sandbox discover them.
# Names and ports only: nothing secret.
SIDECARS_ENV = "KOYEB_SIDECARS"


@dataclass
class Sidecar:
    """A trusted helper service that runs next to a sandbox.

    Pass sidecars to ``Sandbox.create(sidecars=[...])``. The sandbox reaches
    each one at ``http://<name>:<port>`` over a private mesh.

    Args:
        name: DNS name the sandbox uses to reach the sidecar. Lowercase
            letters, digits and dashes, 2-63 characters.
        image: Docker image to run.
        ports: TCP ports the sidecar listens on (1-5). The first port is
            health-checked: the sandbox is created only once it accepts
            connections.
        instance_type: Instance type (default: nano).
        entrypoint: Override the image entrypoint.
        command: Override the image command.
        args: Arguments for the command.
        env: Environment variables. Use ``Secret(name=...)`` values so the
            platform injects secrets at deploy time; they never reach the
            sandbox.
        config_files: Files to mount, as ``{path: content}`` or
            ``{path: ConfigFile(...)}``.
        registry_secret: Secret holding registry credentials for a private
            image.
        privileged: Run the sidecar privileged (default: False), e.g. for a
            VPN client that needs /dev/net/tun. Honoured where a privileged
            sandbox is.
        startup_grace_period: Seconds the sidecar may take to start listening
            before failed health checks count (5-900, default: the platform's,
            5). The platform then allows about two more minutes. Raise it for
            images that install or configure things at boot.
        block_network: Block all outbound traffic from the sidecar.
        outbound_allowlist: IPs/CIDRs the sidecar may reach; everything else
            is blocked. Mutually exclusive with block_network. Entries must
            not overlap. With either option the sandbox can still reach the
            sidecar and get replies, but the sidecar can't open new
            connections to the sandbox.

    Example:
        >>> proxy = Sidecar(
        ...     name="proxy",
        ...     image="mitmproxy/mitmproxy:latest",
        ...     ports=[8080],
        ...     command="mitmdump",
        ...     args=["--listen-port", "8080"],
        ...     env={"API_KEY": Secret(name="my-api-key")},
        ... )
    """

    name: str
    image: str
    ports: List[int]
    instance_type: str = "nano"
    entrypoint: Optional[List[str]] = None
    command: Optional[str] = None
    args: Optional[List[str]] = None
    env: Optional[Dict[str, Any]] = None
    config_files: Optional[Dict[str, Any]] = None
    registry_secret: Optional[str] = None
    block_network: bool = False
    outbound_allowlist: Optional[List[str]] = None
    privileged: bool = False
    startup_grace_period: Optional[int] = None

    def __post_init__(self):
        _validate_name(self.name)
        if not isinstance(self.image, str) or not self.image:
            raise SidecarError(f"Sidecar '{self.name}': image is required")
        self.ports = _validate_ports(self.name, self.ports)
        grace = self.startup_grace_period
        if grace is not None and (
            isinstance(grace, bool)
            or not isinstance(grace, int)
            or not _MIN_GRACE <= grace <= _MAX_GRACE
        ):
            raise SidecarError(
                f"Sidecar '{self.name}': startup_grace_period must be an integer "
                f"between {_MIN_GRACE} and {_MAX_GRACE} seconds"
            )
        try:
            egress = build_egress_policy(self.block_network, self.outbound_allowlist)
        except EgressPolicyError as e:
            raise SidecarError(f"Sidecar '{self.name}': {e}") from e
        _check_disjoint(self.name, egress)

    def service_spec(
        self,
        region: Optional[str] = None,
        delete_after_delay: int = 0,
    ) -> SandboxSpec:
        """The service spec for this sidecar.

        A web service with no route (not public), a TCP health check on the
        first port, the mesh enabled with app scope, and no scale-to-zero:
        mesh traffic from the sandbox does not wake a sleeping service.
        ``region`` and ``delete_after_delay`` should match the sandbox's.
        """
        return SandboxSpec(
            name=self.name,
            image=self.image,
            instance_type=self.instance_type,
            definition_type=DeploymentDefinitionType.WEB,
            env=self.env,
            config_files=self.config_files,
            region=region,
            idle_timeout=0,
            registry_secret=self.registry_secret,
            privileged=self.privileged,
            delete_after_delay=delete_after_delay,
            enable_mesh=True,
            entrypoint=self.entrypoint,
            command=self.command,
            args=self.args,
            ports=[DeploymentPort(port=p, protocol="tcp") for p in self.ports],
            routes=[],
            block_network=self.block_network,
            outbound_allowlist=self.outbound_allowlist,
            mesh_scope=MeshScope.MESH_SCOPE_APP,
            health_checks=[
                DeploymentHealthCheck(
                    tcp=TCPHealthCheck(port=self.ports[0]),
                    grace_period=self.startup_grace_period,
                )
            ],
        )


def validate_sidecars(sidecars: Iterable[Sidecar], sandbox_name: str) -> List[Sidecar]:
    """Check a sandbox's sidecars as a set, before any API call.

    Names must be unique and differ from the sandbox's name: they share one
    app, and the sandbox reaches each sidecar by its service name.
    """
    sidecars = list(sidecars)
    seen = set()
    for sidecar in sidecars:
        if not isinstance(sidecar, Sidecar):
            raise SidecarError(f"Expected a Sidecar, got {type(sidecar).__name__}")
        if sidecar.name == sandbox_name:
            raise SidecarError(
                f"Sidecar name '{sidecar.name}' is the sandbox's name; pick another"
            )
        if sidecar.name in seen:
            raise SidecarError(f"Duplicate sidecar name '{sidecar.name}'")
        seen.add(sidecar.name)
    return sidecars


def _validate_name(name: Any) -> None:
    if (
        not isinstance(name, str)
        or not 2 <= len(name) <= 63
        or not _NAME_RE.fullmatch(name)
    ):
        raise SidecarError(
            f"Invalid sidecar name {name!r}: use 2-63 lowercase letters, digits "
            "and single dashes, starting and ending with a letter or digit"
        )


def _validate_ports(name: str, ports: Any) -> List[int]:
    if isinstance(ports, (str, bytes)) or not isinstance(ports, Iterable):
        raise SidecarError(f"Sidecar '{name}': ports must be a list of integers")
    ports = list(ports)
    if not 1 <= len(ports) <= _MAX_PORTS:
        raise SidecarError(
            f"Sidecar '{name}': declare between 1 and {_MAX_PORTS} ports"
        )
    for port in ports:
        if (
            isinstance(port, bool)
            or not isinstance(port, int)
            or not _MIN_PORT <= port <= _MAX_PORT
        ):
            raise SidecarError(
                f"Sidecar '{name}': port {port!r} must be an integer between "
                f"{_MIN_PORT} and {_MAX_PORT}"
            )
    if len(set(ports)) != len(ports):
        raise SidecarError(f"Sidecar '{name}': duplicate port")
    return ports


def _check_disjoint(name: str, egress: Any) -> None:
    """The API rejects overlapping allowlist entries; fail before creating
    anything."""
    nets = [
        ipaddress.ip_network(d.cidr)
        for d in (getattr(egress, "allow_list", None) or [])
    ]
    for i, a in enumerate(nets):
        for b in nets[i + 1 :]:
            if a.version == b.version and a.overlaps(b):
                raise SidecarError(
                    f"Sidecar '{name}': outbound_allowlist entries must not "
                    f"overlap ({a} and {b})"
                )


@dataclass(frozen=True)
class SidecarInfo:
    """A sidecar created with a sandbox.

    The sandbox reaches it at ``http://<name>:<port>``.
    """

    name: str
    service_id: str
    ports: Tuple[int, ...]

    def __post_init__(self):
        object.__setattr__(self, "ports", tuple(self.ports))

    def url(self, port: Optional[int] = None, scheme: str = "http") -> str:
        """URL the sandbox uses to reach this sidecar, on ``port`` (one of
        its declared ports) or the first declared port.

        Raises:
            SidecarError: If ``port`` isn't one of the sidecar's ports
        """
        if port is None:
            port = self.ports[0]
        elif port not in self.ports:
            raise SidecarError(
                f"Sidecar '{self.name}' doesn't declare port {port} "
                f"(ports: {list(self.ports)})"
            )
        return f"{scheme}://{self.name}:{port}"


class SidecarTimeoutError(SidecarError, SandboxTimeoutError):
    """A sidecar didn't become healthy in time. Also a
    SandboxTimeoutError, so existing timeout handling catches it."""


def prepare_sidecars(
    sidecars: Optional[Iterable[Sidecar]],
    *,
    name: str,
    app_id: Optional[str],
    snapshot: Any,
    block_network: bool,
    outbound_allowlist: Optional[List[str]],
    enable_mesh: Optional[bool],
    mesh_scope: Any,
    delete_after_inactivity_delay: int = 0,
    env: Optional[Dict[str, Any]] = None,
) -> Optional[List[Sidecar]]:
    """Validate Sandbox.create arguments when sidecars are given.

    Returns None when there are no sidecars (create behaves as before),
    otherwise the validated list. Fails before any API call.
    """
    if env and SIDECARS_ENV in env:
        # Reserved even without sidecars: get_from_id trusts it to find a
        # sandbox's sidecars, and update_lifecycle then writes to them.
        raise SidecarError(f"env {SIDECARS_ENV} is reserved for sidecars")
    if sidecars is None:
        return None
    sidecars = list(sidecars)
    if not sidecars:
        return None
    if app_id is not None:
        raise SidecarError(
            "sidecars can't be combined with app_id: the sandbox needs its own "
            "app so the mesh stays private to it and its sidecars"
        )
    if snapshot is not None:
        raise SidecarError("sidecars can't be combined with snapshot yet")
    if block_network or outbound_allowlist is not None:
        raise SidecarError(EGRESS_WITH_SIDECARS)
    if enable_mesh is False:
        raise SidecarError("sidecars need the mesh; don't pass enable_mesh=False")
    if mesh_scope not in (
        None,
        MeshScope.MESH_SCOPE_UNSPECIFIED,
        "MESH_SCOPE_UNSPECIFIED",
        MeshScope.MESH_SCOPE_APP,
        "MESH_SCOPE_APP",
    ):
        raise SidecarError("sidecars use mesh_scope MESH_SCOPE_APP; don't set another")
    if delete_after_inactivity_delay:
        raise SidecarError(INACTIVITY_WITH_SIDECARS)
    return validate_sidecars(sidecars, name)


INACTIVITY_WITH_SIDECARS = (
    "delete_after_inactivity can't be used on a sandbox with sidecars: "
    "sidecars never sleep, so the sandbox would be deleted and its sidecars "
    "left running. Use delete_after_delay"
)


def sidecar_service_payloads(
    sidecars: List[Sidecar], app_id: str, sandbox_spec: SandboxSpec
) -> List[Dict[str, Any]]:
    """CreateService payloads for a sandbox's sidecars, with the sandbox's
    region and delete_after_delay."""
    return [
        s.service_spec(
            region=sandbox_spec.region,
            delete_after_delay=sandbox_spec.delete_after_delay,
        ).create_service_payload(app_id)
        for s in sidecars
    ]


EGRESS_WITH_SIDECARS = (
    "block_network and outbound_allowlist can't be used on a sandbox "
    "with sidecars: they also block the mesh, so the sandbox couldn't "
    "reach its sidecars. Set egress on each Sidecar instead"
)


def sidecars_env_value(sidecars: List[Sidecar]) -> str:
    """The SIDECARS_ENV value for a sandbox: names and ports as JSON."""
    return json.dumps(
        [{"name": s.name, "ports": list(s.ports)} for s in sidecars],
        separators=(",", ":"),
    )


def parse_sidecars_env(value: Optional[str]) -> List[Dict[str, Any]]:
    """Names and ports from a SIDECARS_ENV value; [] when unset.

    Strict: anything that isn't a list of valid sidecar names with 1-5
    valid ports raises SidecarError, so a damaged value is never half
    trusted.
    """
    if not value:
        return []
    try:
        entries = json.loads(value)
    except ValueError as e:
        raise SidecarError(f"Invalid {SIDECARS_ENV} value") from e
    if not isinstance(entries, list):
        raise SidecarError(f"Invalid {SIDECARS_ENV} value")
    result, seen = [], set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise SidecarError(f"Invalid {SIDECARS_ENV} value")
        name, ports = entry.get("name"), entry.get("ports")
        try:
            _validate_name(name)
            ports = _validate_ports(name, ports)
        except SidecarError as e:
            raise SidecarError(f"Invalid {SIDECARS_ENV} value: {e}") from e
        if name in seen:
            raise SidecarError(f"Invalid {SIDECARS_ENV} value: duplicate '{name}'")
        seen.add(name)
        result.append({"name": name, "ports": ports})
    return result


def match_sidecars(
    entries: List[Dict[str, Any]], services: Iterable[Any]
) -> Tuple[List[SidecarInfo], List[str]]:
    """Pair KOYEB_SIDECARS entries with the app's services by exact name.
    Returns the matches and the names with no service."""
    by_name = {s.name: s for s in services}
    infos, missing = [], []
    for entry in entries:
        service = by_name.get(entry["name"])
        if service is None:
            missing.append(entry["name"])
        else:
            infos.append(SidecarInfo(entry["name"], service.id, entry["ports"]))
    return infos, missing


def aligned_delete_after(
    delay: int, sandbox_created_at: Any, sidecar_created_at: Any
) -> int:
    """delete_after_create for a sidecar so it expires with its sandbox.

    The platform counts the delay from each service's own creation, and
    sidecars are created before the sandbox: add the gap. 0 (no expiry)
    stays 0; unknown times fall back to ``delay``.
    """
    if not delay or sandbox_created_at is None or sidecar_created_at is None:
        return delay
    gap = (sandbox_created_at - sidecar_created_at).total_seconds()
    return delay + max(0, math.ceil(gap))


def check_sidecar_deployment(info: SidecarInfo, status: Any) -> bool:
    """True when ready, False while starting; raises SidecarError when the
    sidecar won't become ready on its own."""
    classification = classify_deployment_status(status)
    if classification == "terminal_failure":
        status_value = getattr(status, "value", status)
        raise SidecarError(
            f"Sidecar '{info.name}' failed to start (deployment status: {status_value})"
        )
    return classification == "ready"
