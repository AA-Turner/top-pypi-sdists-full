"""What GPUs a cube has and what is using them, for the AI tab.

Read from Kubernetes (nodes and pods) through the caller's own Teleport identity,
because Apollo knows which entities exist but not which of them hold a GPU: on
`cube-m9u9i4lc` a model outside the catalog held the only GPU, and a catalog-only
check offered every model as if it were free.

Never raises: a failed read is `GpuState(available=False)`, which the checks treat as
"unknown" and never as "free" or "too small".
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
import time
from dataclasses import dataclass, field, replace

logger = logging.getLogger(__name__)

GPU_RESOURCE = "nvidia.com/gpu"
PRODUCT_LABEL = "nvidia.com/gpu.product"
MEMORY_LABEL = "nvidia.com/gpu.memory"   # MiB per GPU, set by NVIDIA GPU feature discovery
COUNT_LABEL = "nvidia.com/gpu.count"     # GPUs on the node, also set by feature discovery
# Cap on each kubectl call. kubectl from dev to cube-m9u9i4lc took 7-15 s a call on
# 2026-10-06 (the service read measured 15.5 s) and both GPU calls timed out at 10 s
# and again at 20 s, so the read runs in the background with a generous cap and a page
# load waits only `wait` seconds for it.
READ_TIMEOUT_SECONDS = 40.0
CACHE_SECONDS = 10.0
# A failed read is remembered longer, so the tab's 15 s polling does not pay for it
# again on every request (seen on dev 2026-10-06: `get nodes` failing every poll).
FAILURE_CACHE_SECONDS = 60.0

# A card sold as "24 GB" reports 24467 MiB and an L40S sold as "48 GB" reports 46068,
# so a catalog requirement in marketing GB is compared against 95% of it in MiB.
_FIT_MIB_PER_GB = 950


@dataclass(frozen=True)
class GpuState:
    available: bool                  # the read succeeded
    total: int = 0                   # allocatable GPUs across nodes
    in_use: int = 0                  # requested by running pods
    product: str = ""                # e.g. "NVIDIA-RTX-PRO-4000-Blackwell"
    memory_mib: int | None = None    # per GPU, smallest across GPU nodes
    users: tuple[str, ...] = field(default_factory=tuple)    # "namespace/name" of pods holding GPUs
    waiting: tuple[str, ...] = field(default_factory=tuple)  # pods that asked for one and are not running
    # Whether the pod read succeeded. Without it the cards are known (so fit is) but not
    # what holds them: on cube-m9u9i4lc (OpenShift, ~175 pods) the node read answered
    # while every cluster-wide pod list timed out, even at 60 pods a page.
    usage_known: bool = True
    # Framebuffer (used MiB, free MiB) per GPU, from NVIDIA's DCGM exporter. Empty when
    # it could not be read. vLLM reserves its share of a card at startup
    # (gpuMemoryUtilization), so "used" is what the models on it have claimed, which
    # is what decides whether another model can start beside them. On cube-9p4t83wd
    # (2026-10-13) Gemma 4 31B and Trinity Mini together held 94 of 97 GB.
    framebuffer: tuple[tuple[int, int], ...] = field(default_factory=tuple)
    # (Apollo entity name, fraction of its GPU) for each running pod that holds a GPU and
    # starts vLLM with `--gpu-memory-utilization`. The DCGM exporter attributes a
    # time-sliced card to one pod, so it cannot say which model holds what; this can.
    # vLLM documents the flag as a per-instance budget ("it does not matter if you have
    # another vLLM instance running on the same GPU"), claimed at startup and held. On
    # cube-9p4t83wd (2026-10-13) Gemma 4 31B ran at 0.57 and Trinity Mini at 0.38: 55 and
    # 36 of the 96 GB card, which is the 92 GB in use the exporter measured.
    reserved: tuple[tuple[str, float], ...] = field(default_factory=tuple)

    def reserved_gb(self, entity_name: str | None) -> int | None:
        """GB of its GPU the model `entity_name` reserves, or None when that is not known
        (no pod read, no flag on the pod, or no card size)."""
        if not entity_name or self.memory_mib is None:
            return None
        fraction = dict(self.reserved).get(entity_name)
        return None if fraction is None else round(fraction * self.memory_mib / 1024)

    @property
    def _roomiest(self) -> tuple[int, int] | None:
        """(used, free) MiB of the GPU with the most free memory: where one more
        single-GPU model would have to go."""
        return max(self.framebuffer, key=lambda f: f[1]) if self.framebuffer else None

    @property
    def memory_used_gb(self) -> int | None:
        r = self._roomiest
        return None if r is None else round(r[0] / 1024)

    @property
    def memory_free_gb(self) -> int | None:
        r = self._roomiest
        return None if r is None else round(r[1] / 1024)

    @property
    def free(self) -> int | None:
        if not self.usage_known:
            return None
        return max(0, self.total - self.in_use)

    @property
    def memory_gb(self) -> int | None:
        return None if self.memory_mib is None else round(self.memory_mib / 1024)

    def fits(self, min_vram_gb: int) -> str:
        """yes | no | unknown: whether one GPU here is big enough."""
        if not self.available or self.memory_mib is None:
            return "unknown"
        return "yes" if self.memory_mib >= min_vram_gb * _FIT_MIB_PER_GB else "no"


UNKNOWN = GpuState(available=False)


def _gpus(resources: dict | None) -> int:
    try:
        return int((resources or {}).get(GPU_RESOURCE) or 0)
    except (TypeError, ValueError):
        return 0


def _workload(meta: dict) -> str:
    """The workload a pod belongs to, which is what a person recognises: a Deployment's
    pod is named after its ReplicaSet (`<deployment>-<hash>`), so the hash is dropped."""
    for owner in meta.get("ownerReferences") or []:
        kind, name = owner.get("kind"), owner.get("name") or ""
        if kind == "ReplicaSet" and "-" in name:
            return name.rsplit("-", 1)[0]
        if kind in ("StatefulSet", "DaemonSet", "Job") and name:
            return name
    return meta.get("name", "")


# The pod fields the read needs, and only those, one pod per line with tab-separated
# fields. `get pods -A -o json` returns every pod's full spec through the Teleport proxy
# and timed out on dev (2026-10-06, ~135 pods); a template over the same list answers
# quickly. JSONPath rather than custom columns because a pod's arguments can contain
# line breaks (a script passed to `sh -c`): custom columns print them as they are, and on
# cube-9p4t83wd (2026-10-13) the rest of an OVN pod's script read as two more pods,
# while JSONPath prints string arrays as JSON, line breaks escaped (165 of 165 lines
# there had exactly nine fields). Order matters: it is the order `parse_pod_rows` reads.
# Dots inside a key are escaped for JSONPath, and the `\t` is for kubectl to expand.
_POD_FIELDS = (
    ".metadata.namespace", ".metadata.name", ".status.phase",
    ".spec.containers[*].resources.requests.nvidia\\.com/gpu",
    ".metadata.ownerReferences[0].kind", ".metadata.ownerReferences[0].name",
    # Apollo stamps the entity on every pod it deploys, which ties a pod to a model
    # without guessing from names.
    ".metadata.annotations.apollo\\.palantir\\.com/metadata\\.entity\\.id",
    # Read only for the `--gpu-memory-utilization` number; nothing else in them is kept
    # or logged, since a pod's arguments can carry a credential.
    ".spec.containers[*].args", ".spec.containers[*].command",
)
POD_JSONPATH = "{range .items[*]}" + '{"\\t"}'.join("{" + f + "}" for f in _POD_FIELDS) + '{"\\n"}{end}'
ENTITY_ANNOTATION = "apollo.palantir.com/metadata.entity.id"
_GPU_UTILIZATION_RE = re.compile(r"--gpu-memory-utilization(?:=|\s+)([0-9]*\.?[0-9]+)")
# A row is a pod only when its first fields look like one: a DNS-label namespace and
# name, a pod phase, and GPU counts. Defence in depth; the format already keeps one pod
# to one line.
_DNS_LABEL_RE = re.compile(r"^[a-z0-9]([-a-z0-9.]*[a-z0-9])?$")
_POD_PHASES = frozenset({"Pending", "Running", "Succeeded", "Failed", "Unknown"})
_GPU_FIELD_RE = re.compile(r"^([0-9]+( [0-9]+)*)?$")


def _json_strings(text: str) -> list[str]:
    """The strings in JSONPath's rendering of a string-array field across containers
    (`["a","b"] ["c"]`). Anything that does not parse yields what parsed before it."""
    out: list[str] = []
    decoder, i, text = json.JSONDecoder(), 0, text or ""
    while i < len(text):
        if text[i].isspace():
            i += 1
            continue
        try:
            value, i = decoder.raw_decode(text, i)
        except ValueError:
            break
        if isinstance(value, list):
            out.extend(v for v in value if isinstance(v, str))
    return out


def _utilization(text: str) -> float | None:
    """The `--gpu-memory-utilization` fraction in a pod's arguments, if any."""
    m = _GPU_UTILIZATION_RE.search(text or "")
    if not m:
        return None
    value = float(m.group(1))
    return value if 0 < value <= 1 else None


def _entity_name(entity_id: str) -> str:
    """`aeid:<env>:helm-chart:<entity>` -> `<entity>`; "" for anything else."""
    prefix, sep, name = (entity_id or "").rpartition(":helm-chart:")
    return name if sep and prefix.startswith("aeid:") and name else ""


def parse_pod_rows(text: str) -> dict:
    """`kubectl get pods -o jsonpath=POD_JSONPATH` -> the subset of `get pods -o json`
    that `parse` reads."""
    items = []
    for line in (text or "").splitlines():
        cols = line.split("\t")
        if len(cols) != len(_POD_FIELDS):
            continue
        ns, name, phase, gpus, owner_kind, owner_name, entity, args, command = cols
        if not (_DNS_LABEL_RE.match(ns) and _DNS_LABEL_RE.match(name)
                and phase in _POD_PHASES and _GPU_FIELD_RE.match(gpus)):
            continue
        containers = [{"resources": {"requests": {GPU_RESOURCE: g}}} for g in gpus.split()]
        meta = {"namespace": ns, "name": name}
        if owner_kind:
            meta["ownerReferences"] = [{"kind": owner_kind, "name": owner_name}]
        if entity:
            meta["annotations"] = {ENTITY_ANNOTATION: entity}
        utilization = _utilization(" ".join(_json_strings(command) + _json_strings(args)))
        if utilization is not None:
            containers = containers or [{}]
            containers[0] = {**containers[0], "args": [f"--gpu-memory-utilization={utilization}"]}
        items.append({"metadata": meta, "status": {"phase": phase},
                      "spec": {"containers": containers}})
    return {"items": items}


def parse_node_rows(text: str) -> dict | None:
    """`kubectl get nodes --show-labels --no-headers` -> the subset of `get nodes -o json`
    that `parse` reads, with allocatable taken from feature discovery's count label.

    Nodes are read as a table because the JSON is mostly `status.images`, every image
    cached on the node: on cube-m9u9i4lc (OpenShift) `get nodes -o json` timed out
    through Teleport while the table answered at once. None when no node carries the
    count label, since then "no GPU" and "no feature discovery" look the same."""
    items, labelled = [], False
    for line in (text or "").splitlines():
        cols = line.split()
        if len(cols) < 2:
            continue
        labels = {}
        for pair in cols[-1].split(","):
            k, sep, v = pair.partition("=")
            if sep:
                labels[k] = v
        labelled = labelled or COUNT_LABEL in labels
        items.append({"metadata": {"labels": labels},
                      "status": {"allocatable": {GPU_RESOURCE: labels.get(COUNT_LABEL, "0")}}})
    return {"items": items} if labelled else None


def parse(nodes: dict, pods: dict | None) -> GpuState:
    """Build a GpuState from `kubectl get nodes -o json` and pods in the same shape
    (`parse_pod_rows` builds that from the JSONPath read). `pods=None` means the
    pod read failed: the cards are still described, their usage is not."""
    total, product, memory = 0, "", None
    for node in nodes.get("items") or []:
        count = _gpus((node.get("status") or {}).get("allocatable"))
        if not count:
            continue
        total += count
        labels = (node.get("metadata") or {}).get("labels") or {}
        product = product or labels.get(PRODUCT_LABEL, "")
        try:
            mib = int(labels.get(MEMORY_LABEL, ""))
            memory = mib if memory is None else min(memory, mib)
        except ValueError:
            pass
    if pods is None:
        return GpuState(
            available=True, total=total, product=product, memory_mib=memory, usage_known=False,
        )
    in_use, users, waiting, reserved = 0, [], [], []
    for pod in pods.get("items") or []:
        spec = pod.get("spec") or {}
        containers = spec.get("containers") or []
        asked = sum(_gpus((c.get("resources") or {}).get("requests")) for c in containers)
        if not asked:
            continue
        meta = pod.get("metadata") or {}
        name = f"{meta.get('namespace', '')}/{_workload(meta)}"
        if (pod.get("status") or {}).get("phase") == "Running":
            in_use += asked
            users.append(name)
            entity = _entity_name((meta.get("annotations") or {}).get(ENTITY_ANNOTATION, ""))
            utilization = next(
                (u for c in containers
                 for u in [_utilization(" ".join([*(c.get("command") or []), *(c.get("args") or [])]))]
                 if u is not None),
                None,
            )
            if entity and utilization is not None:
                reserved.append((entity, utilization))
        else:
            waiting.append(name)
    return GpuState(
        available=True, total=total, in_use=in_use, product=product, memory_mib=memory,
        users=tuple(users), waiting=tuple(waiting), reserved=tuple(reserved),
    )


# Where the NVIDIA GPU operator puts its DCGM exporter: OpenShift's OperatorHub install
# (`nvidia-gpu-operator`, both cubes checked 2026-10-13) and the upstream Helm default.
DCGM_NAMESPACES = ("nvidia-gpu-operator", "gpu-operator")
DCGM_SERVICE = "nvidia-dcgm-exporter:9400"
_DCGM_LINE_RE = re.compile(r'^(DCGM_FI_DEV_FB_(?:USED|FREE))\{([^}]*)\}\s+([0-9.eE+-]+)\s*$')
_UUID_RE = re.compile(r'UUID="([^"]+)"')


def parse_dcgm(text: str) -> tuple[tuple[int, int], ...]:
    """DCGM exporter metrics -> (used MiB, free MiB) per GPU, by GPU UUID. A GPU missing
    either figure is left out rather than guessed."""
    used: dict[str, int] = {}
    free: dict[str, int] = {}
    for line in (text or "").splitlines():
        m = _DCGM_LINE_RE.match(line.strip())
        if not m:
            continue
        uuid = _UUID_RE.search(m.group(2))
        if not uuid:
            continue
        try:
            value = int(float(m.group(3)))
        except ValueError:
            continue
        (used if m.group(1).endswith("USED") else free)[uuid.group(1)] = value
    return tuple((used[u], free[u]) for u in sorted(used) if u in free)


_cache: dict[tuple[str, str], tuple[float, GpuState]] = {}

# The last card each (profile, cube) was SEEN with: count, product and memory, which
# change only when someone swaps hardware. A later read that fails keeps reporting
# them, with usage unknown, rather than dropping back to "unknown". On dev
# (2026-10-08) kubectl through Teleport succeeded on one poll and timed out on the
# next, so the AI tab flipped between "24 GB, too large" and "unknown, Deploy" for
# the same 48 GB model within one session.
_cards: dict[tuple[str, str], tuple[float, GpuState]] = {}
CARD_KEEP_SECONDS = 24 * 3600


def _card_only(state: GpuState) -> GpuState:
    return GpuState(
        available=True, total=state.total, product=state.product, memory_mib=state.memory_mib,
        usage_known=False,
    )


def _why(output: str) -> str:
    """A failure's kind, never its text: kubectl output can name internal hosts."""
    text = (output or "").lower()
    if "forbidden" in text:
        return "forbidden"
    if "timed out" in text or "timeout" in text:
        return "timeout"
    if "credentials" in text or "tbot" in text:
        return "credentials"
    return "error"


_inflight: dict[tuple[str, str], asyncio.Task] = {}


async def read_gpus(cluster: str, profile: str, wait: float | None = None) -> GpuState:
    """The cube's GPUs. `cluster` is an environment the caller already authorized.

    One read per (profile, cluster) is in flight at a time. With `wait`, return UNKNOWN
    after that many seconds and let the read finish in the background, so the next
    request finds it cached: a page load must not hang on a cold kubectl.
    """
    key = (profile, cluster)
    hit = _cache.get(key)
    if hit and hit[0] > time.monotonic():
        return hit[1]
    task = _inflight.get(key)
    if task is None or task.done() or task.get_loop() is not asyncio.get_running_loop():
        task = asyncio.get_running_loop().create_task(_read(cluster, profile, key))
        _inflight[key] = task
        task.add_done_callback(lambda t, k=key: _inflight.pop(k, None) if _inflight.get(k) is t else None)
    if wait is None:
        return await asyncio.shield(task)
    try:
        return await asyncio.wait_for(asyncio.shield(task), timeout=wait)
    except asyncio.TimeoutError:
        return UNKNOWN


async def _read(cluster: str, profile: str, key: tuple[str, str]) -> GpuState:
    from cube_cloud.teleport.kubeconfig import TRUNCATION_MARKER, run_kubectl

    state = UNKNOWN
    try:
        (nodes_out, rc1), (pods_out, rc2), framebuffer = await asyncio.wait_for(asyncio.gather(
            run_kubectl(["get", "nodes", "--show-labels", "--no-headers"], cluster=cluster,
                        profile=profile, timeout=READ_TIMEOUT_SECONDS),
            run_kubectl(["get", "pods", "-A", "-o", f"jsonpath={POD_JSONPATH}",
                         "--field-selector=status.phase!=Succeeded,status.phase!=Failed"],
                        cluster=cluster, profile=profile, timeout=READ_TIMEOUT_SECONDS),
            _read_framebuffer(cluster, profile),
        ), timeout=READ_TIMEOUT_SECONDS + 5)
        if rc1 != 0 or rc2 != 0:
            logger.warning(
                "reactor gpu read on %s: kubectl failed (nodes: %s, pods: %s)", cluster,
                "ok" if rc1 == 0 else _why(nodes_out), "ok" if rc2 == 0 else _why(pods_out),
            )
        # run_kubectl cuts long output and keeps the child's return code 0. A cut list is
        # a failed read: the pods after the cut would otherwise not exist, and a GPU held
        # by one of them would read as free.
        if rc1 == 0 and nodes_out.endswith(TRUNCATION_MARKER):
            logger.warning("reactor gpu read on %s: the node list was truncated", cluster)
            rc1 = -1
        if rc2 == 0 and pods_out.endswith(TRUNCATION_MARKER):
            logger.warning("reactor gpu read on %s: the pod list was truncated", cluster)
            rc2 = -1
        nodes = parse_node_rows(nodes_out) if rc1 == 0 else None
        if rc1 == 0 and nodes is None:
            logger.info("reactor gpu read on %s: no node carries %s", cluster, COUNT_LABEL)
        if nodes is not None:
            # Nodes alone still say how big the GPU is, which is what keeps a model that
            # cannot fit from being offered.
            state = parse(nodes, parse_pod_rows(pods_out) if rc2 == 0 else None)
            if framebuffer:
                state = replace(state, framebuffer=framebuffer)
    except Exception as e:  # noqa: BLE001 -- class only; kubectl output can echo cluster internals
        logger.warning("reactor gpu read on %s failed (%s)", cluster, type(e).__name__)
    now = time.monotonic()
    if state.available:
        _cards[key] = (now + CARD_KEEP_SECONDS, _card_only(state))
    else:
        card = _cards.get(key)
        if card and card[0] > now:
            state = card[1]
    # A partial read is cached like a failure: its pod half would fail again next poll.
    ttl = CACHE_SECONDS if state.available and state.usage_known else FAILURE_CACHE_SECONDS
    _cache[key] = (now + ttl, state)
    return state


async def _read_framebuffer(cluster: str, profile: str) -> tuple[tuple[int, int], ...]:
    """Used and free GPU memory from the DCGM exporter, through the API server's service
    proxy (a GET; no exec, no port-forward). Empty when no exporter answers: the page then
    shows the card's size without what is in use, never a guess."""
    from cube_cloud.teleport.kubeconfig import run_kubectl

    for namespace in DCGM_NAMESPACES:
        out, rc = await run_kubectl(
            ["get", "--raw", f"/api/v1/namespaces/{namespace}/services/{DCGM_SERVICE}/proxy/metrics"],
            cluster=cluster, profile=profile, timeout=READ_TIMEOUT_SECONDS,
        )
        if rc == 0:
            parsed = parse_dcgm(out)
            if parsed:
                return parsed
    logger.info("reactor gpu read on %s: no DCGM exporter answered", cluster)
    return ()
