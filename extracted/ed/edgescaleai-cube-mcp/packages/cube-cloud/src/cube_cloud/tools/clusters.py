"""Cube cluster tools: list, status, services (server-side via tbot)."""

from __future__ import annotations

import json
import logging

from cube_common.apollo_client import ApolloClient, ApolloError

from cube_cloud.teleport.kubeconfig import run_kubectl
from cube_cloud.teleport.tbot_manager import tbot
from cube_cloud.tools.environments import _resolve_environment

logger = logging.getLogger(__name__)

# Namespaces list_services hides by default (an explicit `namespace=` filter
# always bypasses this — asking for one directly still works). Best-effort,
# not exhaustive: other platform tooling can add infra namespaces this
# doesn't know about yet.
_DEFAULT_EXCLUDED_NAMESPACES = {
    "kube-system",
    "kube-public",
    "kube-node-lease",
    "groundcover",
    "teleport-apps",
    "teleport",
    "assisted-installer",
    "nvidia-gpu-operator",
    "infrastructure-office",
}
_DEFAULT_EXCLUDED_NAMESPACE_PREFIXES = ("openshift",)


def _is_infra_namespace(namespace: str) -> bool:
    return (
        namespace in _DEFAULT_EXCLUDED_NAMESPACES
        or namespace.startswith(_DEFAULT_EXCLUDED_NAMESPACE_PREFIXES)
    )


async def cube_status(cluster: str | None = None, profile: str = "admin") -> str:
    """Get the status of a Cube node."""
    if not tbot.is_ready:
        return "tbot credentials not ready. Server-side kubectl is not available yet."

    if not cluster:
        return "Error: cluster name is required. Use cube_list to see available clusters."

    output, rc = await run_kubectl(
        ["get", "nodes", "-o", "jsonpath={.items[0].metadata.name}"],
        cluster=cluster,
        profile=profile,
    )
    if rc != 0:
        return f"Failed to get node: {output}"

    node_name = output.strip()
    if not node_name:
        return "No nodes found. The Cube may not be running."

    output, rc = await run_kubectl(["describe", "node", node_name], cluster=cluster, profile=profile)
    if rc != 0:
        return f"Failed to describe node: {output}"

    return f"Cube Node Status ({cluster} / {node_name}):\n\n{output}"


async def cube_list(profile: str = "admin") -> str:
    """List available Cube clusters via dynamic tsh kube discovery."""
    if not tbot.is_ready:
        return "tbot credentials not ready. Server-side cluster listing is not available yet."

    clusters = await tbot.list_kube_clusters_tsh(profile=profile)
    if not clusters:
        return "No Cube clusters found. Teleport kube discovery may still be initializing."

    lines = ["Available Cubes:", "=" * 50]
    for c in clusters:
        lines.append(f"  {c}")

    lines.append("")
    lines.append("Use kubectl_exec with a cluster name to run commands.")
    return "\n".join(lines)


SERVICE_PORT_FIELDS = frozenset({"port", "target", "protocol", "app_uri", "app_uri_tcp"})
SERVICE_FIELDS = frozenset({"name", "namespace", "type", "ports"})


async def fetch_services(
    client: ApolloClient,
    environment: str,
    namespace: str | None = None,
    profile: str = "admin",
    timeout: float = 60,
    resolved_name: str | None = None,
) -> tuple[list[dict], str, int, str]:
    """Kubernetes Services on a cube, structured -> `(services, env_name, hidden, error)`.

    The data layer behind `list_services`. Extracted so the console can consume the
    SAME kubectl call and the SAME `app_uri` construction rather than parsing the
    tool's formatted text — the discipline in `console/reads.py`'s module docstring,
    and the reason `edgeport` ended up with five text parsers that broke on wording
    changes.

    Each service is `{name, namespace, type, ports: [{port, target, protocol,
    app_uri}]}`. `app_uri` is built here, once, so the value the console offers is
    byte-identical to the one the MCP tool suggests — the whole point being that it is
    passed straight to `expose`, where a wrong port surfaces much later as Teleport
    "context deadline exceeded".

    `error` is non-empty on any failure and is already operator-facing; `hidden` counts
    infra-namespace services filtered out in list-everything mode.

    `timeout` bounds the kubectl call. The default is `run_kubectl`'s own; the console's
    page-load read passes a shorter one (`reads.SERVICES_KUBECTL_TIMEOUT_SECONDS`), since
    a disconnected cube otherwise holds that request open for a full minute.

    `resolved_name` is an environment name the caller has ALREADY resolved and
    authorized, and it skips `_resolve_environment` — which, uncached, drains
    `LIST_ENVIRONMENTS` (every environment with its full `rolePolicy`) and issues
    `MY_TEAMS` for its RBAC check. The console passes it: `reads.cube_services` has
    already resolved the cube out of its cached, RBAC-filtered `_visible_environments`,
    and re-resolving on every page-load cache miss cost two Apollo round-trips, one of
    them the heaviest query in the system. Passing it TRANSFERS the Apollo
    authorization to the caller, the `teleport_status.fetch_teleport_status` pattern —
    so only a caller that has just authorized this environment may. The MCP tool and
    the expose write path do not, and resolve (and authorize) here as before. kubectl
    itself still runs as `profile`'s own Teleport identity either way.
    """
    if not tbot.is_ready:
        return [], environment, 0, (
            "tbot credentials not ready. Server-side kubectl is not available yet."
        )

    if resolved_name is not None:
        env_name = resolved_name
    else:
        try:
            env_info = await _resolve_environment(client, environment)
        except ApolloError as e:
            return [], environment, 0, f"list_services failed: {e}"
        env_name = env_info.get("name", environment)

    args = ["get", "svc", "-o", "json"]
    args += ["-n", namespace] if namespace else ["-A"]

    output, rc = await run_kubectl(args, cluster=env_name, profile=profile, timeout=timeout)
    if rc != 0:
        return [], env_name, 0, f"Failed to list services on {env_name}: {output}"

    try:
        data = json.loads(output)
    except json.JSONDecodeError as e:
        return [], env_name, 0, f"Failed to parse kubectl output: {e}"

    hidden = 0
    services: list[dict] = []
    for svc in data.get("items", []):
        meta = svc.get("metadata") or {}
        ns = meta.get("namespace", "?")
        if not namespace and _is_infra_namespace(ns):
            hidden += 1
            continue
        name = meta.get("name", "?")
        spec = svc.get("spec") or {}
        ports = []
        for p in spec.get("ports") or []:
            port = p.get("port")
            ports.append({
                "port": port,
                "target": p.get("targetPort", port),
                "protocol": p.get("protocol", "TCP"),
                # Built ONCE, here, so the console and the MCP tool cannot drift.
                "app_uri": f"http://{name}.{ns}.svc.cluster.local:{port}",
                # The `tcp://` form of the SAME target, for a service that does
                # not speak HTTP (mosquitto on 1883, the MinIO S3 API on 5000 —
                # both real on the fleet). Offered as a second candidate rather
                # than inferred, because nothing here can tell whether a service
                # speaks HTTP: the kubectl `protocol` field above reads "TCP" for
                # every ordinary HTTP service too, so it is not the signal it
                # looks like. The console's write allowlist is built from these
                # same dicts, so emitting it here is what makes a TCP expose
                # possible from the console at all.
                "app_uri_tcp": f"tcp://{name}.{ns}.svc.cluster.local:{port}",
            })
        services.append({
            "name": name, "namespace": ns,
            "type": spec.get("type", "ClusterIP"), "ports": ports,
        })
    return services, env_name, hidden, ""


async def list_services(
    client: ApolloClient,
    environment: str,
    namespace: str | None = None,
    profile: str = "admin",
) -> str:
    """List Kubernetes Services in a cube's cluster, as candidates for expose.

    Takes an Apollo `environment` (not a raw Teleport `cluster` name, unlike
    cube_status/kubectl_exec) so it RBAC-checks access the same way
    expose/unexpose/list_exposed do, and so the environment name it resolves
    can be chained straight into expose's own `environment` argument.
    `auth/apollo_rbac.py::cluster_name` documents that an Apollo environment
    name IS the Teleport/K8s cluster name, so the resolved name is passed to
    `run_kubectl` verbatim.

    When `namespace` is omitted (list-everything mode), known infra
    namespaces (kube-system, openshift*, groundcover, teleport-apps, ...)
    are hidden by default — see `_is_infra_namespace`. Passing `namespace`
    explicitly always bypasses the filter.
    """
    services, env_name, hidden, err = await fetch_services(
        client, environment, namespace, profile
    )
    if err:
        return err

    if not services:
        suffix = f" in namespace \'{namespace}\'" if namespace else ""
        return f"No services found on {env_name}{suffix}."

    lines = [f"Services on {env_name} ({len(services)})", "=" * 60]
    for svc in services:
        lines.append(f"  {svc['namespace']}/{svc['name']}  ({svc['type']})")
        for p in svc["ports"]:
            lines.append(
                f"    port {p['port']}/{p['protocol']} -> targetPort {p['target']}"
                f"   app_uri: {p['app_uri']}"
            )

    lines.append("")
    lines.append(
        "Pass the app_uri for the port your app actually serves on to expose's "
        'app_uri argument — the wrong port surfaces as Teleport "context '
        'deadline exceeded".'
    )
    lines.append(
        "If the service does NOT speak HTTP (MQTT, Postgres, an S3 API), swap "
        "the scheme for tcp:// and pass that instead. A tcp:// app has no "
        "browser URL — it is reached with app_proxy — but exposing it as http:// "
        "does not fail until dial time, with an error that does not name the "
        "cause."
    )
    if hidden:
        lines.append(
            f"({hidden} infra/system service(s) hidden — pass namespace=<name> "
            "to see a specific infra namespace.)"
        )
    return "\n".join(lines)
