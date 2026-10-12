"""The hosted MCP's internal-TLS phases: what each overlay renders, and how
deploy-mcp.yml picks one, checks it and applies it.

INTERNAL_TLS_EDGE (off | servers | clients | strict) decides what reaches the
cluster. `off` is agent/deploy/mcp/k8s.yaml as it always was; the others are
kustomize overlays in agent/deploy/mcp-tls/ that add ghostunnel sidecars and
move the Ingress -> MCP and MCP -> API hops onto mutual TLS. Nothing renders
these overlays before a production deploy does, so every property the rollout
order depends on is asserted here against the REAL `kubectl kustomize` output:
which phase adds which object, that the client key never reaches the app
container, that an overlay changes nothing it does not mean to.

The workflow half runs the deploy job's own shell steps against a stand-in
`kubectl` on PATH, so the phase check, the render, the deletes and the image
resolution are exercised rather than pattern-matched.
"""

from __future__ import annotations

import copy
import functools
import os
import re
import shutil
import stat
import subprocess
from pathlib import Path

import pytest
import yaml  # via [dev] -> datamodel-code-generator; test_workflow_pytest_workdir.py imports it too.

_REPO = Path(__file__).resolve().parents[2]
_BASE = _REPO / "agent" / "deploy" / "mcp" / "k8s.yaml"
_OVERLAYS = _REPO / "agent" / "deploy" / "mcp-tls"
_WORKFLOW = _REPO / ".github" / "workflows" / "deploy-mcp.yml"

PHASES = ("servers", "clients", "strict")
NAME = "research-os-mcp"
CANARY = "research-os-mcp-tls-canary"
NETPOL = "research-os-mcp-mtls"
SERVER_SECRET = "research-os-internal-tls-mcp"
CLIENT_SECRET = "research-os-internal-tls-client"
LOOPBACK_API = "http://127.0.0.1:18082"
IMAGE = "ghcr.io/prbe-ai/research-os-mcp"

# ingress-nginx -> tls-server: present the shared client identity, verify the
# sidecar's cert against the internal CA, check its SAN.
TLS_ANNOTATIONS = {
    "nginx.ingress.kubernetes.io/backend-protocol": "HTTPS",
    "nginx.ingress.kubernetes.io/proxy-ssl-secret": f"research/{CLIENT_SECRET}",
    "nginx.ingress.kubernetes.io/proxy-ssl-verify": "on",
    "nginx.ingress.kubernetes.io/proxy-ssl-name": f"{NAME}.research.svc.cluster.local",
    "nginx.ingress.kubernetes.io/proxy-ssl-server-name": "on",
}


# --- rendering ----------------------------------------------------------------


def _kubectl() -> str:
    found = shutil.which("kubectl")
    if found is None:
        # GitHub's ubuntu runners ship kubectl, and deploy-mcp.yml renders with
        # it. In CI a missing binary means these checks silently stopped running.
        if os.environ.get("CI"):
            pytest.fail("kubectl is not on PATH in CI; the TLS overlay checks cannot run")
        pytest.skip("kubectl not installed: the TLS overlays render with `kubectl kustomize`")
    return found


@functools.lru_cache(maxsize=None)
def _rendered_text(phase: str) -> str:
    proc = subprocess.run(
        [_kubectl(), "kustomize", str(_OVERLAYS / phase)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, f"`kubectl kustomize {phase}` failed:\n{proc.stderr}"
    return proc.stdout


def _objects(text: str) -> dict[tuple[str, str], dict]:
    docs = [d for d in yaml.safe_load_all(text) if d]
    objects = {(d["kind"], d["metadata"]["name"]): d for d in docs}
    assert len(objects) == len(docs), "two objects share a kind and name"
    return objects


def _render(phase: str) -> dict[tuple[str, str], dict]:
    return _objects(_rendered_text(phase))


def _base() -> dict[tuple[str, str], dict]:
    return _objects(_BASE.read_text())


def _pod(objects: dict) -> dict:
    return objects[("Deployment", NAME)]["spec"]["template"]["spec"]


def _container(pod: dict, name: str) -> dict:
    (found,) = [c for c in pod["containers"] + pod.get("initContainers", []) if c["name"] == name]
    return found


def _env(container: dict) -> dict[str, str]:
    return {e["name"]: e.get("value") for e in container.get("env", [])}


def _ports(service: dict) -> dict[str, tuple[int, object]]:
    return {p.get("name", ""): (p["port"], p.get("targetPort")) for p in service["spec"]["ports"]}


def _backends(ingress: dict) -> list[tuple[str, str, dict]]:
    return [
        (rule["host"], path["path"], path["backend"]["service"]["port"])
        for rule in ingress["spec"]["rules"]
        for path in rule["http"]["paths"]
    ]


# --- what each phase renders --------------------------------------------------


@pytest.mark.parametrize("phase", PHASES)
def test_every_phase_renders_into_the_research_namespace(phase):
    objects = _render(phase)
    assert ("Deployment", NAME) in objects
    assert {o["metadata"].get("namespace") for o in objects.values()} == {"research"}


def test_servers_adds_the_tls_listener_and_the_canary_and_nothing_else():
    base, objects = _base(), _render("servers")
    pod = _pod(objects)

    assert [c["name"] for c in pod["initContainers"]] == ["tls-server"]
    # A multi-port Service must name every port; the plain one keeps its target.
    assert _ports(objects[("Service", NAME)]) == {"http": (80, 8080), "tls": (8443, "tls")}

    canary = objects[("Ingress", CANARY)]
    assert _backends(canary) == [("mcp.research.prbe.ai", "/healthz", {"name": "tls"})]
    assert canary["spec"]["rules"][0]["http"]["paths"][0]["pathType"] == "Exact"
    assert canary["metadata"]["annotations"] == TLS_ANNOTATIONS
    base_ingress = base[("Ingress", NAME)]
    assert canary["spec"]["tls"] == base_ingress["spec"]["tls"]
    assert canary["spec"]["ingressClassName"] == base_ingress["spec"]["ingressClassName"]

    # MCP traffic itself does not move yet: same Ingress, same API URL.
    assert objects[("Ingress", NAME)] == base_ingress
    assert _env(_container(pod, "mcp")) == _env(_container(_pod(base), "mcp"))
    assert not any(kind == "NetworkPolicy" for kind, _ in objects)


def test_clients_moves_both_hops_onto_tls():
    base, objects = _base(), _render("clients")
    pod = _pod(objects)

    assert {c["name"] for c in pod["initContainers"]} == {"tls-server", "tls-client-api"}
    client_args = _container(pod, "tls-client-api")["args"]
    assert client_args[0] == "client"
    assert "--listen=127.0.0.1:18082" in client_args
    assert "--target=research-os.research.svc.cluster.local:8443" in client_args

    # Outbound: only PROBE_BASE_URL changes, onto the sidecar's loopback port.
    mcp_env, base_env = _env(_container(pod, "mcp")), _env(_container(_pod(base), "mcp"))
    assert mcp_env["PROBE_BASE_URL"] == LOOPBACK_API
    assert {k: v for k, v in mcp_env.items() if k != "PROBE_BASE_URL"} == {
        k: v for k, v in base_env.items() if k != "PROBE_BASE_URL"
    }

    # Inbound: every path of the public Ingress reaches the tls port, over mutual TLS,
    # and the base annotations (timeouts, cert-manager) survive.
    ingress, base_ingress = objects[("Ingress", NAME)], base[("Ingress", NAME)]
    assert [(h, p) for h, p, _ in _backends(ingress)] == [(h, p) for h, p, _ in _backends(base_ingress)]
    assert all(port == {"name": "tls"} for _, _, port in _backends(ingress))
    assert ingress["metadata"]["annotations"] == {
        **base_ingress["metadata"]["annotations"],
        **TLS_ANNOTATIONS,
    }

    # The plain port stays for in-cluster callers; the canary is the servers phase's.
    assert _ports(objects[("Service", NAME)]) == {"http": (80, 8080), "tls": (8443, "tls")}
    assert ("Ingress", CANARY) not in objects
    assert not any(kind == "NetworkPolicy" for kind, _ in objects)


def test_strict_closes_the_plain_port():
    clients, objects = _render("clients"), _render("strict")

    assert _ports(objects[("Service", NAME)]) == {"tls": (8443, "tls")}

    policy = objects[("NetworkPolicy", NETPOL)]["spec"]
    assert policy["podSelector"] == {"matchLabels": {"app": NAME}}
    assert policy["policyTypes"] == ["Ingress"]
    (rule,) = policy["ingress"]
    assert rule["ports"] == [{"protocol": "TCP", "port": 8443}]
    assert rule["from"] == [
        {"namespaceSelector": {"matchLabels": {"kubernetes.io/metadata.name": "ingress-nginx"}}},
        {"podSelector": {"matchLabels": {"app.kubernetes.io/name": "research-os-assistant-runner"}}},
    ]

    # Otherwise exactly the clients phase.
    for key in (("Deployment", NAME), ("Ingress", NAME), ("PodDisruptionBudget", NAME)):
        assert objects[key] == clients[key], key
    assert ("Ingress", CANARY) not in objects


@pytest.mark.parametrize("phase", PHASES)
def test_certificate_keys_reach_only_their_sidecar(phase):
    """The mcp container serves every tenant's requests; no TLS key belongs in it."""
    pod = _pod(_render(phase))
    secret_of = {v["name"]: v["secret"]["secretName"] for v in pod.get("volumes", [])}
    owner = {SERVER_SECRET: "tls-server", CLIENT_SECRET: "tls-client-api"}

    assert set(secret_of.values()) <= set(owner)
    for container in pod["containers"] + pod["initContainers"]:
        for mount in container.get("volumeMounts", []):
            secret = secret_of.get(mount["name"])
            if secret is not None:
                assert container["name"] == owner[secret], (container["name"], secret)
                assert mount.get("readOnly") is True
    assert "volumeMounts" not in _container(pod, "mcp")
    for volume in pod.get("volumes", []):
        assert volume["secret"]["defaultMode"] == 0o444


@pytest.mark.parametrize("phase", PHASES)
def test_every_sidecar_is_native_and_locked_down(phase):
    """Native sidecars (they start before the app and outlive its preStop drain),
    run as the chart's do. That the image, resources and client CN equal the
    chart's own is tests/test_chart.py's job: it re-runs on a change to either side."""
    pod = _pod(_render(phase))
    for sidecar in pod["initContainers"]:
        assert sidecar["restartPolicy"] == "Always", sidecar["name"]
        assert sidecar["image"].startswith("mirror.gcr.io/ghostunnel/ghostunnel:") and "@sha256:" in sidecar["image"]
        assert "--timed-reload=1h" in sidecar["args"]
        ctx = sidecar["securityContext"]
        assert ctx["runAsNonRoot"] is True and ctx["readOnlyRootFilesystem"] is True
        assert ctx["allowPrivilegeEscalation"] is False and ctx["capabilities"] == {"drop": ["ALL"]}
    server = _container(pod, "tls-server")
    assert "--allow-cn=research-os-internal-client" in server["args"]
    assert "--target=127.0.0.1:8080" in server["args"]
    assert server["ports"] == [{"containerPort": 8443, "name": "tls"}]
    assert server["startupProbe"]["tcpSocket"] == {"port": 8443}
    assert server["readinessProbe"]["tcpSocket"] == {"port": 8443}


@pytest.mark.parametrize("phase", PHASES)
def test_overlays_change_nothing_they_do_not_mean_to(phase):
    """Strip what the TLS components add and the Deployment and PDB are k8s.yaml's,
    field for field: probes, grace period, rollout shape and resources all survive."""
    base, objects = _base(), _render(phase)
    deployment = copy.deepcopy(objects[("Deployment", NAME)])
    pod = deployment["spec"]["template"]["spec"]
    pod.pop("initContainers")
    pod.pop("volumes")
    base_url = _env(_container(_pod(base), "mcp"))["PROBE_BASE_URL"]
    for entry in _container(pod, "mcp")["env"]:
        if entry["name"] == "PROBE_BASE_URL":
            entry["value"] = base_url

    assert deployment == base[("Deployment", NAME)]
    assert objects[("PodDisruptionBudget", NAME)] == base[("PodDisruptionBudget", NAME)]


# --- deploy-mcp.yml -----------------------------------------------------------


def _workflow() -> dict:
    return yaml.safe_load(_WORKFLOW.read_text())


def _deploy_steps() -> list[dict]:
    return _workflow()["jobs"]["deploy"]["steps"]


def _step(name: str) -> dict:
    (found,) = [s for s in _deploy_steps() if s.get("name") == name]
    return found


def _index(name: str) -> int:
    return [s.get("name") for s in _deploy_steps()].index(name)


def _fake_kubectl(tmp_path: Path) -> Path:
    """A `kubectl` that logs its arguments; `kustomize` goes to the real one,
    `get` prints $FAKE_GET_OUT and exits $FAKE_GET_RC, anything else succeeds."""
    bindir = tmp_path / "bin"
    bindir.mkdir()
    real = shutil.which("kubectl") or "false"
    script = bindir / "kubectl"
    script.write_text(
        "#!/usr/bin/env bash\n"
        'echo "$*" >> "$KUBECTL_LOG"\n'
        f'if [ "$1" = kustomize ]; then exec {real} "$@"; fi\n'
        'for a in "$@"; do\n'
        '  if [ "$a" = get ]; then printf "%s" "${FAKE_GET_OUT:-}"; exit "${FAKE_GET_RC:-0}"; fi\n'
        "done\n"
        "exit 0\n"
    )
    script.chmod(script.stat().st_mode | stat.S_IEXEC)
    return bindir


def _run_step(name: str, tmp_path: Path, **env: str) -> tuple[subprocess.CompletedProcess, list[str]]:
    """Run one deploy step's shell the way the runner does (`bash -e`), from the
    repo root, with a stand-in kubectl. Returns the process and kubectl's calls."""
    bindir = tmp_path / "bin"
    if not bindir.exists():
        _fake_kubectl(tmp_path)
    log = tmp_path / "kubectl.log"
    log.touch()
    github_env = tmp_path / "github_env"
    github_env.touch()
    proc = subprocess.run(
        ["bash", "-e", "-c", _step(name)["run"]],
        cwd=_REPO,
        capture_output=True,
        text=True,
        env={
            "PATH": f"{bindir}{os.pathsep}{os.environ['PATH']}",
            "HOME": str(tmp_path),
            "KUBECTL_LOG": str(log),
            "RUNNER_TEMP": str(tmp_path),
            "GITHUB_ENV": str(github_env),
            "GITHUB_OUTPUT": str(tmp_path / "github_output"),
            "IMAGE": IMAGE,
            "NAMESPACE": "research",
            "DEPLOYMENT": NAME,
            **env,
        },
        check=False,
    )
    return proc, log.read_text().splitlines()


def test_the_phase_variable_defaults_off_and_is_read_by_the_deploy_job():
    env = _workflow()["jobs"]["deploy"]["env"]
    assert env["INTERNAL_TLS_EDGE"] == "${{ vars.INTERNAL_TLS_EDGE || 'off' }}"
    assert env["INTERNAL_TLS_ENABLED"] == "${{ vars.INTERNAL_TLS_ENABLED || 'false' }}"


@pytest.mark.parametrize(
    ("phase", "enabled", "ok"),
    [
        ("off", "false", True),
        ("off", "true", True),
        ("servers", "true", True),
        ("clients", "true", True),
        ("strict", "true", True),
        ("servers", "false", False),  # the chart has issued no certificates
        ("strict", "false", False),
        ("bogus", "true", False),
        ("", "true", False),
        ("Servers", "true", False),
    ],
)
def test_an_unknown_phase_or_a_tls_phase_without_the_chart_fails(tmp_path, phase, enabled, ok):
    proc, calls = _run_step(
        "Validate the internal-TLS phase",
        tmp_path,
        INTERNAL_TLS_EDGE=phase,
        INTERNAL_TLS_ENABLED=enabled,
        APPLY_ONLY="false",
    )
    assert (proc.returncode == 0) is ok, proc.stdout + proc.stderr
    if not ok:
        assert "::error" in proc.stdout
    assert calls == [], "the phase check must not touch the cluster"


def test_the_phase_check_runs_before_any_cluster_access():
    assert _index("Validate the internal-TLS phase") < _index(
        "Assemble kubeconfig from ServiceAccount credentials"
    )


def test_every_tls_phase_the_workflow_accepts_has_an_overlay():
    accepted = {"off", *PHASES}
    assert "off|servers|clients|strict)" in _step("Validate the internal-TLS phase")["run"]
    on_disk = {p.parent.name for p in _OVERLAYS.glob("*/kustomization.yaml")} - {"components"}
    assert on_disk == accepted - {"off"}


@pytest.mark.parametrize(
    ("out", "rc", "ok"),
    [("True", 0, True), ("False", 0, False), ("", 0, False), ("Error from server (NotFound)", 1, False)],
)
def test_a_tls_phase_needs_both_certificates_ready(tmp_path, out, rc, ok):
    step = _step("Check the internal-TLS certificates are issued")
    assert "env.INTERNAL_TLS_EDGE != 'off'" in step["if"]

    proc, calls = _run_step(
        step["name"], tmp_path, INTERNAL_TLS_EDGE="servers", FAKE_GET_OUT=out, FAKE_GET_RC=str(rc)
    )
    assert (proc.returncode == 0) is ok, proc.stdout + proc.stderr
    if ok:
        assert any(SERVER_SECRET in c for c in calls) and any(CLIENT_SECRET in c for c in calls)
        assert all("certificates.cert-manager.io" in c for c in calls)
    else:
        assert "::error" in proc.stdout
    assert _index(step["name"]) < _index("Apply the manifest")


def test_off_applies_k8s_yaml_byte_for_byte(tmp_path):
    image = f"{IMAGE}:sha-{'a' * 40}"
    proc, calls = _run_step(
        "Render the manifest, and dry-run it", tmp_path, INTERNAL_TLS_EDGE="off", APPLY_IMAGE=image
    )
    assert proc.returncode == 0, proc.stderr
    applied = (tmp_path / "mcp.yaml").read_text()
    assert applied == _BASE.read_text().replace("__IMAGE__", image)
    assert not any(c.startswith("kustomize") for c in calls), "phase off must not render an overlay"
    assert calls == [f"apply --dry-run=server -f {tmp_path}/mcp.yaml"]


@pytest.mark.parametrize("phase", PHASES)
def test_a_tls_phase_applies_its_overlay_at_the_resolved_image(tmp_path, phase):
    _kubectl()
    image = f"{IMAGE}:sha-{'b' * 40}"
    proc, calls = _run_step(
        "Render the manifest, and dry-run it", tmp_path, INTERNAL_TLS_EDGE=phase, APPLY_IMAGE=image
    )
    assert proc.returncode == 0, proc.stderr
    applied = (tmp_path / "mcp.yaml").read_text()
    assert applied == _rendered_text(phase).replace("__IMAGE__", image)
    assert "__IMAGE__" not in applied
    assert calls[-1] == f"apply --dry-run=server -f {tmp_path}/mcp.yaml"


def test_the_server_dry_run_comes_before_any_change():
    render = _step("Render the manifest, and dry-run it")["run"]
    apply = _step("Apply the manifest")["run"]
    assert 'kubectl apply --dry-run=server -f "${RUNNER_TEMP}/mcp.yaml"' in render
    assert 'kubectl apply -f "${RUNNER_TEMP}/mcp.yaml"' in apply
    assert (
        _index("Render the manifest, and dry-run it")
        < _index("Remove objects outside this phase")
        < _index("Apply the manifest")
    )
    # Exactly one real apply, and it is that file.
    real = [s for s in _deploy_steps() if "kubectl apply -f" in s.get("run", "")]
    assert [s["name"] for s in real] == ["Apply the manifest"]


@pytest.mark.parametrize(
    ("phase", "deleted"),
    [
        ("off", {f"networkpolicy {NETPOL}", f"ingress {CANARY}"}),
        ("servers", {f"networkpolicy {NETPOL}"}),
        ("clients", {f"networkpolicy {NETPOL}", f"ingress {CANARY}"}),
        ("strict", {f"ingress {CANARY}"}),
    ],
)
def test_leaving_a_phase_deletes_what_only_that_phase_applied(tmp_path, phase, deleted):
    """`kubectl apply` never deletes; without these, a rollback from `strict` keeps
    the 8443-only NetworkPolicy and the plain port the Ingress returns to is dead."""
    proc, calls = _run_step("Remove objects outside this phase", tmp_path, INTERNAL_TLS_EDGE=phase)
    assert proc.returncode == 0, proc.stderr
    assert all(c.endswith("--ignore-not-found") for c in calls), calls
    got = {c.removeprefix("-n research delete ").removesuffix(" --ignore-not-found") for c in calls}
    assert got == deleted


def test_the_deleted_names_are_the_objects_the_overlays_create():
    _kubectl()
    assert ("NetworkPolicy", NETPOL) in _render("strict")
    assert ("Ingress", CANARY) in _render("servers")
    # The public certificate Secret is a different object that must never be confused
    # with the NetworkPolicy: k8s.yaml names it research-os-mcp-tls.
    assert NETPOL != _base()[("Ingress", NAME)]["spec"]["tls"][0]["secretName"]


def test_apply_only_skips_the_gate_and_the_build():
    workflow = _workflow()
    # PyYAML reads the bare `on:` key as boolean True.
    dispatch = workflow[True]["workflow_dispatch"]["inputs"]["apply_only"]
    assert dispatch["type"] == "boolean" and dispatch["default"] is False

    jobs = workflow["jobs"]
    assert "!inputs.apply_only" in jobs["gate"]["if"]
    assert "!inputs.apply_only" in jobs["build"]["if"]

    # deploy must still run with `build` skipped, but only for apply_only on main,
    # and a push still needs a successful build.
    condition = jobs["deploy"]["if"]
    for part in (
        "!cancelled()",
        "vars.DEPLOY_MCP_ENABLED == 'true'",
        "needs.build.result == 'success'",
        "inputs.apply_only",
        "github.ref == 'refs/heads/main'",
        "needs.build.result == 'skipped'",
    ):
        assert part in condition, part


@pytest.mark.parametrize(
    ("running", "ok"),
    [
        (f"{IMAGE}:sha-{'c' * 40}", True),
        ("__IMAGE__", False),
        (f"{IMAGE}:latest", False),
        (f"{IMAGE}:sha-{'c' * 39}", False),
        (f"ghcr.io/someone-else/mcp:sha-{'c' * 40}", False),
        ("", False),
    ],
)
def test_apply_only_pins_the_image_already_running(tmp_path, running, ok):
    proc, calls = _run_step(
        "Resolve the image to apply",
        tmp_path,
        APPLY_ONLY="true",
        GITHUB_SHA="d" * 40,
        FAKE_GET_OUT=running,
    )
    assert (proc.returncode == 0) is ok, proc.stdout + proc.stderr
    assert any(f"get deployment/{NAME}" in c for c in calls)
    if ok:
        assert (tmp_path / "github_env").read_text() == f"APPLY_IMAGE={running}\n"
    else:
        assert "::error" in proc.stdout


def test_a_push_applies_the_image_it_built(tmp_path):
    proc, calls = _run_step(
        "Resolve the image to apply", tmp_path, APPLY_ONLY="false", GITHUB_SHA="e" * 40
    )
    assert proc.returncode == 0, proc.stderr
    assert calls == [], "a push must not read its image from the cluster"
    assert (tmp_path / "github_env").read_text() == f"APPLY_IMAGE={IMAGE}:sha-{'e' * 40}\n"


def test_the_rollout_is_verified_against_the_image_actually_applied():
    verify = _step("Wait for the rollout, and verify what actually landed")["run"]
    assert 'expected="${APPLY_IMAGE}"' in verify
    assert _index("Resolve the image to apply") < _index("Render the manifest, and dry-run it")


def test_the_overlays_are_in_both_deploy_path_lists():
    """A change to an overlay must trigger a deploy, and must count as superseding
    an older run's rollout, exactly like a change to k8s.yaml."""
    workflow = _workflow()
    assert "agent/deploy/mcp-tls/**" in workflow[True]["push"]["paths"]
    assert "agent/deploy/mcp-tls" in _step("Guard against a superseded rollout")["run"]


def test_the_shared_edge_preflight_runs_before_anything_is_applied():
    """scripts/deploy/internal-tls-edge-phase.sh refuses a phase skip, an MCP
    two phases from the API side, and `clients` without ready TLS pods
    (tests/unit/test_internal_tls_edge_phase.py). It only protects production
    if this job runs it, for the MCP, before rendering or applying."""
    step = _step("Check the internal-TLS edge phase")
    assert step["run"].strip() == 'bash scripts/deploy/internal-tls-edge-phase.sh check mcp "${INTERNAL_TLS_EDGE}"'
    assert step["if"] == "steps.freshness.outputs.deploy == 'true'"
    assert _index("Check the internal-TLS edge phase") > _index("Check the cluster credential is still valid")
    for later in ("Render the manifest, and dry-run it", "Remove objects outside this phase", "Apply the manifest"):
        assert _index("Check the internal-TLS edge phase") < _index(later), later


def test_the_mcp_binds_ipv4_where_its_tls_server_dials():
    """tls-server targets 127.0.0.1:8080. uvicorn on `::` goes through asyncio,
    which sets IPV6_V6ONLY, so 127.0.0.1 would be refused: the image's HOST
    must stay an IPv4 bind."""
    dockerfile = (_REPO / "agent" / "deploy" / "mcp" / "Dockerfile").read_text()
    assert re.search(r"\bHOST=0\.0\.0\.0\b", dockerfile)
    server = _container(_pod(_render("servers")), "tls-server")
    assert "--target=127.0.0.1:8080" in server["args"]


def test_deploy_proves_the_mcp_to_api_hop_not_just_healthz():
    run = _step("Verify the MCP reaches the API")["run"]
    assert 'Authorization: Bearer ${token}-${i}' in run and '"$code" = 401' in run
    assert _index("Verify the MCP reaches the API") > _index("Verify the live endpoint")


def test_a_superseded_apply_only_fails_instead_of_ending_green():
    run = _step("Guard against a superseded rollout")["run"]
    branch = run.split('if [ "${APPLY_ONLY}" = true ]; then', 1)[1].split("else", 1)[0]
    assert "::error" in branch and "exit 1" in branch
