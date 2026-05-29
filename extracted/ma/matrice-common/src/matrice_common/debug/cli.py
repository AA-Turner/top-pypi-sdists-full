"""matrice_common.debug — host-side per-camera streaming debugger.

Read-only. Auto-discovers running matrice containers, calls the backend with
their credentials, inspects /dev/shm + (optionally) Redis, and emits a
per-camera correlated health report.

Usage as a script::

    python -m matrice_common.debug status         # default: full report
    python -m matrice_common.debug containers
    python -m matrice_common.debug cameras
    python -m matrice_common.debug shm
    python -m matrice_common.debug gpu-map
    python -m matrice_common.debug camera <camera_id>

Usage as a library::

    from matrice_common.debug import main, collect_state, correlate
    main(["status", "--json"])

Global flags: --json, --no-shm, --no-backend, --no-redis, --container <name|id>,
              --base-url <url>, -v
"""

from __future__ import annotations

import argparse
import json
import mmap
import os
import re
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich import box
    _RICH = True
except ImportError:
    _RICH = False


SHM_BASE = os.environ.get("MATRICE_SHM_PATH", "/dev/shm")
DEFAULT_BASE_URL = os.environ.get("MATRICE_BASE_URL", "https://prod.backend.app.matrice.ai")
NAME_RE = re.compile(r"^([a-f0-9]{24})_(.+)$")

RING_HDR_MAGIC = 0x4D415452  # 'MATR' little-endian
HDR_OFF_WRITE_IDX = 0
HDR_OFF_TIMESTAMP_NS = 24
HDR_OFF_GPU_ID = 32
HDR_OFF_NUM_SLOTS = 36
HDR_OFF_WIDTH = 40
HDR_OFF_HEIGHT = 44
HDR_OFF_IPC_HANDLE = 64
HDR_OFF_CONSUMERS = 136
HDR_CONSUMER_COUNT = 32
HDR_CONSUMER_SLOT = 16  # uint64 key_hash, uint64 cursor
HDR_OFF_FRAME_FORMAT = 664
HDR_OFF_MAGIC = 676
HDR_OFF_VERSION = 680

# CudaIpcRingBuffer layout — same first 648 bytes as ShmRingBuffer header,
# then 16 bytes session info, then num_slots × 32 bytes per-slot meta.
# No 'MATR' magic. Discriminator: total_size == 664 + 32 * num_slots.
CIRB_HEADER_SIZE = 648
CIRB_SESSION_SIZE = 16
CIRB_SLOT_META_SIZE = 32
CIRB_SLOT_META_BASE = CIRB_HEADER_SIZE + CIRB_SESSION_SIZE  # 664

RB_PREFIX = "shm_rb_"
DATABUS_PREFIX = "databus__"
DBSTATUS_PREFIX = "databus_status__"
CUDA_IPC_PREFIX = "cuda_ipc_"
GPU_MAP_FILE = "gpu_camera_map"
GFC_FILE = "global_frame_counter"

ROLE_PATTERNS = [
    ("gateway", re.compile(r"streaming[_-]gateway", re.I)),
    ("inference", re.compile(r"inference[_-]tracker|inference[_-]server|deploy[_-]add", re.I)),
    ("analytics", re.compile(r"fe[_-]analytics|analytics[_-]service", re.I)),
    ("fs_streaming", re.compile(r"fe[_-]fs[_-]streaming", re.I)),
    ("video_storage", re.compile(r"video[_-]storage|media[_-]server", re.I)),
]

VERBOSE = False


def vlog(*a):
    if VERBOSE:
        print("[debug]", *a, file=sys.stderr)


def mask(s: Optional[str]) -> str:
    if not s:
        return ""
    if len(s) <= 6:
        return "***"
    return f"{s[:2]}***{s[-3:]}"


# ────────────────────────────────────────────────────────────────────
# Container discovery
# ────────────────────────────────────────────────────────────────────

@dataclass
class ContainerCtx:
    docker_id: str
    name: str
    image: str
    status: str
    role: str  # gateway, inference, analytics, fs_streaming, video_storage, unknown
    instance_id: Optional[str] = None  # the leading 24-hex prefix of the name
    action_id: Optional[str] = None
    deployment_id: Optional[str] = None
    access_key: Optional[str] = None
    secret_key: Optional[str] = None
    base_url: Optional[str] = None
    cmd: List[str] = field(default_factory=list)
    cmd_instance_arg: Optional[str] = None  # last positional arg if it looks like a mongo id

    def public_dict(self) -> dict:
        d = asdict(self)
        d["access_key"] = mask(self.access_key)
        d["secret_key"] = mask(self.secret_key)
        d.pop("cmd", None)  # cmd often embeds plaintext credentials in `export FOO=...`
        return d


def _docker(cmd: List[str], timeout: int = 10) -> str:
    try:
        out = subprocess.check_output(["docker", *cmd], timeout=timeout, stderr=subprocess.STDOUT)
        return out.decode("utf-8", errors="replace")
    except FileNotFoundError:
        return ""
    except subprocess.CalledProcessError as e:
        vlog("docker", cmd, "rc!=0:", e.output[:200] if e.output else "")
        return ""
    except subprocess.TimeoutExpired:
        return ""


def _classify_role(name: str, image: str) -> str:
    s = f"{name} {image}"
    for role, pat in ROLE_PATTERNS:
        if pat.search(s):
            return role
    return "unknown"


def discover_containers() -> List[ContainerCtx]:
    """List every running container and pull matrice-relevant context.

    Read-only. Skips obvious non-matrice things (chromium, jupyter) by name.
    """
    raw = _docker(["ps", "--format", "{{.ID}}|{{.Names}}|{{.Image}}|{{.Status}}"])
    if not raw:
        return []
    skip = re.compile(r"^(remote-browser|jupyter|grafana|prometheus)", re.I)
    ctxs: List[ContainerCtx] = []
    for line in raw.strip().splitlines():
        parts = line.split("|", 3)
        if len(parts) != 4:
            continue
        did, name, image, status = parts
        if skip.search(name):
            continue
        role = _classify_role(name, image)
        m = NAME_RE.match(name)
        instance_id = m.group(1) if m else None
        if role == "unknown" and instance_id is None:
            continue
        ctx = ContainerCtx(docker_id=did, name=name, image=image, status=status,
                           role=role, instance_id=instance_id)
        ctxs.append(ctx)

    for c in ctxs:
        ins_raw = _docker(["inspect", c.docker_id])
        if not ins_raw:
            continue
        try:
            ins = json.loads(ins_raw)[0]
        except Exception:
            continue
        cfg = ins.get("Config", {}) or {}
        env = {}
        for e in cfg.get("Env", []) or []:
            if "=" in e:
                k, v = e.split("=", 1)
                env[k] = v
        c.access_key = env.get("MATRICE_ACCESS_KEY_ID")
        c.secret_key = env.get("MATRICE_SECRET_ACCESS_KEY")
        c.base_url = env.get("MATRICE_BASE_URL") or DEFAULT_BASE_URL
        c.action_id = env.get("ACTION_ID") or env.get("MATRICE_ACTION_ID")
        c.deployment_id = env.get("DEPLOYMENT_ID") or env.get("MATRICE_DEPLOYMENT_ID")
        c.cmd = cfg.get("Cmd") or []
        # Gateway is launched as `python streaming_gateway.py <instance_id>` —
        # pull the trailing 24-hex token from any Cmd entry.
        joined = " ".join(c.cmd) if c.cmd else ""
        m2 = re.search(r"\b([a-f0-9]{24})\b\s*'?\s*$", joined.strip())
        if m2:
            c.cmd_instance_arg = m2.group(1)
        if not c.instance_id and c.cmd_instance_arg:
            c.instance_id = c.cmd_instance_arg
    return ctxs


# ────────────────────────────────────────────────────────────────────
# Backend client (read-only)
# ────────────────────────────────────────────────────────────────────

class BackendError(Exception):
    pass


class BackendClient:
    def __init__(self, access_key: str, secret_key: str, base_url: str, timeout: float = 10.0):
        self.access_key = access_key
        self.secret_key = secret_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._token: Optional[str] = None

    def _http(self, method: str, path: str, headers: Optional[dict] = None,
              body: Optional[bytes] = None, json_body: Optional[dict] = None) -> Any:
        url = f"{self.base_url}{path}"
        # Cloudflare in front of prod.backend.app.matrice.ai bans the default
        # urllib UA ("Python-urllib/x.y") with Error 1010. Use a curl-shaped UA.
        h = {"Accept": "application/json", "User-Agent": "matrice-debug/1.0 curl/8.5.0"}
        if headers:
            h.update(headers)
        data = body
        if json_body is not None:
            data = json.dumps(json_body).encode()
            h.setdefault("Content-Type", "application/json")
        req = urllib.request.Request(url, method=method, headers=h, data=data)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            try:
                payload = json.loads(e.read().decode("utf-8"))
            except Exception:
                payload = {"success": False, "error": f"HTTP {e.code}"}
            return payload
        except Exception as e:
            raise BackendError(str(e))

    def auth(self) -> str:
        body = json.dumps({"accessKey": self.access_key, "secretKey": self.secret_key}).encode()
        resp = self._http("GET", "/v1/accounting/validate_access_key",
                          headers={"Content-Type": "text/plain"}, body=body)
        if not resp.get("success"):
            raise BackendError(f"validate_access_key failed: {resp}")
        token = (resp.get("data") or {}).get("token")
        if not token:
            raise BackendError("no token in validate_access_key response")
        self._token = token
        return token

    def _get(self, path: str) -> Any:
        if not self._token:
            self.auth()
        return self._http("GET", path, headers={"Authorization": f"Bearer {self._token}"})

    def _post(self, path: str, body: dict) -> Any:
        if not self._token:
            self.auth()
        return self._http("POST", path,
                          headers={"Authorization": f"Bearer {self._token}"},
                          json_body=body)

    def consuming_topics(self, instance_id: str) -> List[dict]:
        r = self._get(f"/v1/inference/get_app_deployment_consuming_topics/{instance_id}")
        if not r.get("success"):
            return []
        d = r.get("data") or []
        return d if isinstance(d, list) else []

    def output_topics(self, deployment_id: str, instance_id: str) -> List[dict]:
        r = self._get(f"/v1/inference/get_output_topics_by_app_deployment_and_instance/{deployment_id}/{instance_id}")
        if not r.get("success"):
            return []
        d = r.get("data") or []
        return d if isinstance(d, list) else []

    def camera_ips(self, camera_ids: List[str]) -> Dict[str, str]:
        if not camera_ids:
            return {}
        r = self._post("/v1/inference/camera_instance_ips", {"cameraIds": camera_ids})
        if not r.get("success"):
            return {}
        d = r.get("data") or {}
        return d if isinstance(d, dict) else {}

    def redis_for_instance(self, instance_id: str, action_id: Optional[str] = None) -> Optional[dict]:
        path = f"/v1/actions/get_redis_server_by_instance_id/{instance_id}"
        if action_id:
            path += f"?actionId={action_id}"
        r = self._get(path)
        if not r.get("success"):
            return None
        return r.get("data")


# ────────────────────────────────────────────────────────────────────
# /dev/shm inspection
# ────────────────────────────────────────────────────────────────────

@dataclass
class ShmRingInfo:
    path: str
    name: str
    size: int
    layout: str             # 'shm_rb_v2' | 'cuda_ipc' | 'unknown'
    write_idx: int
    last_ts_ns: int
    age_ms: float
    gpu_id: int
    num_slots: int
    width: int
    height: int
    frame_format: int
    has_cuda_ipc: bool
    consumers: List[Tuple[int, int]]  # (key_hash, cursor)
    magic_ok: bool
    last_slot_frame_idx: Optional[int] = None
    last_slot_ts_ns: Optional[int] = None
    # Two-shot sampling for liveness when timestamp_ns isn't wall-clock.
    write_idx_delta: Optional[int] = None        # frames advanced over sample window
    sample_window_ms: Optional[float] = None     # how long we waited between shots
    estimated_fps: Optional[float] = None
    error: Optional[str] = None


def _read_consumers(mm: mmap.mmap, size: int) -> List[Tuple[int, int]]:
    out: List[Tuple[int, int]] = []
    if size < HDR_OFF_CONSUMERS + HDR_CONSUMER_COUNT * HDR_CONSUMER_SLOT:
        return out
    for i in range(HDR_CONSUMER_COUNT):
        off = HDR_OFF_CONSUMERS + i * HDR_CONSUMER_SLOT
        kh, cur = struct.unpack_from("<QQ", mm, off)
        if kh != 0 or cur != 0:
            out.append((kh, cur))
    return out


def _read_write_idx(path: str) -> Optional[int]:
    """Cheap re-read of just the write_idx for two-shot liveness sampling."""
    try:
        with open(path, "rb") as f:
            data = f.read(8)
            if len(data) < 8:
                return None
            return struct.unpack("<Q", data)[0]
    except Exception:
        return None


def parse_ring_header(path: str) -> Optional[ShmRingInfo]:
    """Parse a SHM ring buffer file. Handles both ShmRingBuffer-v2 (768B header,
    'MATR' magic at 676) and CudaIpcRingBuffer (648B header + 16B session +
    num_slots*32 slot meta, no magic). Falls back to layout='unknown' so the
    caller can ignore parsed fields."""
    try:
        size = os.path.getsize(path)
        with open(path, "rb") as f:
            mm = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
        try:
            magic = struct.unpack_from("<I", mm, HDR_OFF_MAGIC)[0] if size >= HDR_OFF_MAGIC + 4 else 0
            magic_ok = magic == RING_HDR_MAGIC

            write_idx = struct.unpack_from("<Q", mm, HDR_OFF_WRITE_IDX)[0] if size >= 8 else 0
            ts_ns = struct.unpack_from("<Q", mm, HDR_OFF_TIMESTAMP_NS)[0] if size >= HDR_OFF_TIMESTAMP_NS + 8 else 0
            gpu_id = struct.unpack_from("<i", mm, HDR_OFF_GPU_ID)[0] if size >= HDR_OFF_GPU_ID + 4 else -1
            num_slots = struct.unpack_from("<i", mm, HDR_OFF_NUM_SLOTS)[0] if size >= HDR_OFF_NUM_SLOTS + 4 else 0
            width = struct.unpack_from("<i", mm, HDR_OFF_WIDTH)[0] if size >= HDR_OFF_WIDTH + 4 else 0
            height = struct.unpack_from("<i", mm, HDR_OFF_HEIGHT)[0] if size >= HDR_OFF_HEIGHT + 4 else 0
            ipc = bytes(mm[HDR_OFF_IPC_HANDLE:HDR_OFF_IPC_HANDLE + 64]) if size >= HDR_OFF_IPC_HANDLE + 64 else b""
            has_cuda_ipc = any(b != 0 for b in ipc)

            layout = "unknown"
            frame_format = -1
            last_slot_frame_idx: Optional[int] = None
            last_slot_ts_ns: Optional[int] = None
            consumers = _read_consumers(mm, size)

            if magic_ok and size >= HDR_OFF_FRAME_FORMAT + 4:
                # ShmRingBuffer v2 layout (POSIX SHM with frame data on disk in {name}_frames).
                layout = "shm_rb_v2"
                frame_format = struct.unpack_from("<i", mm, HDR_OFF_FRAME_FORMAT)[0]
                # Slot meta is 48B per slot, starting at HDR_OFF_FRAME_FORMAT? No — for v2,
                # per the docs the per-slot meta lives in this same file after the header
                # at offset 768 (the standard HEADER_SIZE). But the .pyi/source says slot
                # meta is at the end after the 768B header. We don't strictly need it for
                # the verdict; skip the last-slot peek for v2 to stay safe.
            elif num_slots > 0 and num_slots <= 10000 and size == CIRB_SLOT_META_BASE + num_slots * CIRB_SLOT_META_SIZE:
                # CudaIpcRingBuffer: GPU frames via IPC, /dev/shm holds only metadata.
                layout = "cuda_ipc"
                # The most recent slot is (write_idx - 1) % num_slots
                if write_idx > 0:
                    slot_idx = (write_idx - 1) % num_slots
                    off = CIRB_SLOT_META_BASE + slot_idx * CIRB_SLOT_META_SIZE
                    if size >= off + 16:
                        last_slot_frame_idx = struct.unpack_from("<Q", mm, off)[0]
                        last_slot_ts_ns = struct.unpack_from("<Q", mm, off + 8)[0]

        finally:
            mm.close()

        now = time.time_ns()
        # Prefer the slot timestamp when present (more precise than header heartbeat).
        eff_ts = last_slot_ts_ns if last_slot_ts_ns else ts_ns
        age_ms = (now - eff_ts) / 1_000_000 if eff_ts else float("inf")
        return ShmRingInfo(
            path=path, name=os.path.basename(path), size=size,
            layout=layout,
            write_idx=write_idx, last_ts_ns=eff_ts, age_ms=age_ms,
            gpu_id=gpu_id, num_slots=num_slots, width=width, height=height,
            frame_format=frame_format, has_cuda_ipc=has_cuda_ipc,
            consumers=consumers, magic_ok=magic_ok,
            last_slot_frame_idx=last_slot_frame_idx,
            last_slot_ts_ns=last_slot_ts_ns,
        )
    except Exception as e:
        return ShmRingInfo(path=path, name=os.path.basename(path), size=0,
                           layout="unknown",
                           write_idx=0, last_ts_ns=0, age_ms=float("inf"),
                           gpu_id=-1, num_slots=0, width=0, height=0,
                           frame_format=-1, has_cuda_ipc=False, consumers=[],
                           magic_ok=False, error=str(e))


def list_shm_artefacts() -> Dict[str, List[str]]:
    out = {"shm_rb": [], "databus": [], "databus_status": [], "cuda_ipc": [],
           "gpu_camera_map": [], "global_frame_counter": []}
    try:
        for entry in os.listdir(SHM_BASE):
            p = os.path.join(SHM_BASE, entry)
            if not os.path.isfile(p):
                continue
            if entry.startswith(RB_PREFIX):
                out["shm_rb"].append(p)
            elif entry.startswith(DBSTATUS_PREFIX):
                out["databus_status"].append(p)
            elif entry.startswith(DATABUS_PREFIX):
                out["databus"].append(p)
            elif entry.startswith(CUDA_IPC_PREFIX):
                out["cuda_ipc"].append(p)
            elif entry == GPU_MAP_FILE:
                out["gpu_camera_map"].append(p)
            elif entry == GFC_FILE:
                out["global_frame_counter"].append(p)
    except OSError as e:
        vlog("listdir", SHM_BASE, "failed:", e)
    return out


def read_gpu_camera_map() -> Dict[str, int]:
    """Read the GpuCameraMap SHM file. Format: <uint32 length><JSON>."""
    path = os.path.join(SHM_BASE, GPU_MAP_FILE)
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "rb") as f:
            length_bytes = f.read(4)
            if len(length_bytes) < 4:
                return {}
            length = struct.unpack("<I", length_bytes)[0]
            data = f.read(length)
            obj = json.loads(data)
            if isinstance(obj, dict) and "mappings" in obj and isinstance(obj["mappings"], dict):
                return {str(k): int(v) for k, v in obj["mappings"].items()}
            if isinstance(obj, dict):
                return {str(k): int(v) for k, v in obj.items() if isinstance(v, (int, float))}
            return {}
    except Exception as e:
        vlog("gpu_camera_map read failed:", e)
        return {}


def read_global_frame_counter() -> Optional[int]:
    path = os.path.join(SHM_BASE, GFC_FILE)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "rb") as f:
            data = f.read(8)
            if len(data) < 8:
                return None
            return struct.unpack("<Q", data)[0]
    except Exception:
        return None


def read_databus_status_all() -> List[dict]:
    """Length-prefixed JSON per file at /dev/shm/databus_status__*."""
    out = []
    try:
        entries = [e for e in os.listdir(SHM_BASE) if e.startswith(DBSTATUS_PREFIX)]
    except OSError:
        return out
    for e in entries:
        path = os.path.join(SHM_BASE, e)
        try:
            with open(path, "rb") as f:
                lb = f.read(4)
                if len(lb) < 4:
                    continue
                length = struct.unpack("<I", lb)[0]
                data = f.read(length)
                obj = json.loads(data)
                obj["_node_id"] = e[len(DBSTATUS_PREFIX):]
                obj["_path"] = path
                out.append(obj)
        except Exception:
            continue
    return out


# Map a databus filename like `databus__<camera_id>__<node>__<port>` → (camera_id, node, port)
DATABUS_RE = re.compile(r"^" + re.escape(DATABUS_PREFIX) + r"([^_].*?)__([^_].*?)__([^_].*)$")


def parse_databus_name(basename: str) -> Optional[Tuple[str, str, str]]:
    m = DATABUS_RE.match(basename)
    if not m:
        return None
    return m.group(1), m.group(2), m.group(3)


# ────────────────────────────────────────────────────────────────────
# Redis probing (read-only)
# ────────────────────────────────────────────────────────────────────

# Stream name patterns observed across deployments. The probe tries each in
# turn and also scans for `{camera_id}_*_output_topic` etc.
# - py_inference consumer_manager.py uses `camera_{id}_input` for the input bus.
# - Live deployments here use `{cam_id}_{app_id}_output_topic`.
REDIS_INPUT_FMT_LEGACY = "camera_{camera_id}_input"
REDIS_INPUT_FMT_TOPIC = "{camera_id}_input_topic"
REDIS_PER_CAMERA_PATTERNS = [
    "{camera_id}_*_output_topic",
    "{camera_id}_*_input_topic",
    "camera_{camera_id}_input",
]
# Field names published per frame (consumer_manager.py:39+)
RKEY_SHM_NAME = b"shm_name"
RKEY_FRAME_IDX = b"frame_idx"
RKEY_TS_NS = b"timestamp_ns"
RKEY_WIDTH = b"width"
RKEY_HEIGHT = b"height"
RKEY_FRAME_FORMAT = b"frame_format"
RKEY_RTP = b"rtp_timestamp"


@dataclass
class RedisInfo:
    host: str
    port: int
    auth: bool
    source: str  # 'docker' | 'api' | 'manual'
    db: int = 0


@dataclass
class RedisStream:
    name: str
    kind: str               # 'input' | 'output' | 'unknown'
    app_id: Optional[str]
    xlen: int
    last_id: Optional[str] = None
    last_age_ms: Optional[float] = None
    last_frame_idx: Optional[int] = None
    last_shm_name: Optional[str] = None
    error: Optional[str] = None


@dataclass
class RedisCameraState:
    streams: List[RedisStream] = field(default_factory=list)
    error: Optional[str] = None

    @property
    def total_xlen(self) -> int:
        return sum(s.xlen for s in self.streams)

    @property
    def newest_age_ms(self) -> Optional[float]:
        ages = [s.last_age_ms for s in self.streams if s.last_age_ms is not None]
        return min(ages) if ages else None

    @property
    def primary_input_stream(self) -> Optional[RedisStream]:
        for s in self.streams:
            if s.kind == "input":
                return s
        return None

    @property
    def app_ids(self) -> List[str]:
        return sorted({s.app_id for s in self.streams if s.app_id})


def discover_redis_from_containers(containers: List[ContainerCtx]) -> Optional[Tuple[RedisInfo, str]]:
    """Find a redis container on this host and pull --requirepass from its Cmd.

    Returns (RedisInfo, password) or None. The password is kept in-memory only.
    """
    redis_re = re.compile(r"^redis[:/]|_redis_setup", re.I)
    for c in containers:
        if not (redis_re.search(c.image or "") or redis_re.search(c.name or "")):
            continue
        try:
            ins = json.loads(_docker(["inspect", c.docker_id]) or "[]")[0]
        except Exception:
            continue
        cmd = " ".join(ins.get("Args", []) or []) or " ".join((ins.get("Config", {}) or {}).get("Cmd", []) or [])
        m = re.search(r"--requirepass\s+(\S+)", cmd)
        if not m:
            continue
        password = m.group(1)
        # Find a host port mapping for 6379 (or assume 127.0.0.1:6379 if host net).
        port = 6379
        ports = (ins.get("NetworkSettings", {}) or {}).get("Ports", {}) or {}
        for k, v in (ports or {}).items():
            if k.startswith("6379/") and v:
                try:
                    port = int(v[0]["HostPort"])
                    break
                except Exception:
                    pass
        return RedisInfo(host="127.0.0.1", port=port, auth=True, source="docker"), password
    return None


def redis_connect(info: RedisInfo, password: Optional[str]):
    """Return a redis-py client or None. Read-only intent — caller must only
    issue read commands (XLEN, XREVRANGE, XINFO, KEYS, SCAN)."""
    try:
        import redis  # type: ignore
    except ImportError:
        vlog("redis-py not installed; skipping redis probe")
        return None
    try:
        client = redis.Redis(host=info.host, port=info.port, password=password,
                             db=info.db, socket_timeout=3, socket_connect_timeout=3,
                             decode_responses=False)
        client.ping()
        return client
    except Exception as e:
        vlog("redis connect failed:", e)
        return None


def _b2s(b) -> str:
    if b is None:
        return ""
    if isinstance(b, bytes):
        return b.decode("utf-8", errors="replace")
    return str(b)


_STREAM_NAME_RE_OUTPUT = re.compile(r"^([a-f0-9]{24})_([a-f0-9]{24})_output_topic$")
_STREAM_NAME_RE_INPUT = re.compile(r"^([a-f0-9]{24})_([a-f0-9]{24})_input_topic$")
_STREAM_NAME_RE_LEGACY = re.compile(r"^camera_([^_]+)_input$")


def _classify_stream(name: str) -> Tuple[str, Optional[str], Optional[str]]:
    """Return (kind, camera_id, app_id) for a stream key name."""
    m = _STREAM_NAME_RE_OUTPUT.match(name)
    if m:
        return "output", m.group(1), m.group(2)
    m = _STREAM_NAME_RE_INPUT.match(name)
    if m:
        return "input", m.group(1), m.group(2)
    m = _STREAM_NAME_RE_LEGACY.match(name)
    if m:
        return "input", m.group(1), None
    return "unknown", None, None


def _probe_one_stream(client, name: str) -> RedisStream:
    kind, _cam, app_id = _classify_stream(name)
    s = RedisStream(name=name, kind=kind, app_id=app_id, xlen=0)
    try:
        s.xlen = int(client.xlen(name))
    except Exception as e:
        msg = str(e)
        if "no such key" not in msg.lower() and "not found" not in msg.lower():
            s.error = msg
        return s
    if s.xlen == 0:
        return s
    try:
        rows = client.xrevrange(name, count=1)
    except Exception as e:
        s.error = f"xrevrange: {e}"
        return s
    if not rows:
        return s
    msg_id, fields = rows[0]
    s.last_id = _b2s(msg_id)
    try:
        ms = int(s.last_id.split("-", 1)[0])
        s.last_age_ms = max(0.0, time.time() * 1000 - ms)
    except Exception:
        pass
    def _gi(k):
        v = fields.get(k)
        if v is None:
            return None
        try:
            return int(v)
        except Exception:
            return None
    s.last_frame_idx = _gi(RKEY_FRAME_IDX)
    sn = fields.get(RKEY_SHM_NAME)
    if sn is not None:
        s.last_shm_name = _b2s(sn)
    return s


def redis_probe_camera(client, camera_id: str) -> RedisCameraState:
    """Find every stream key matching this camera and probe each."""
    state = RedisCameraState()
    seen: set = set()
    for pat in REDIS_PER_CAMERA_PATTERNS:
        match = pat.format(camera_id=camera_id).encode()
        try:
            cursor = 0
            while True:
                cursor, keys = client.scan(cursor=cursor, match=match, count=200)
                for k in keys or []:
                    name = _b2s(k)
                    if name in seen:
                        continue
                    seen.add(name)
                    state.streams.append(_probe_one_stream(client, name))
                if cursor == 0:
                    break
        except Exception as e:
            state.error = f"scan({pat}): {e}"
    return state


def redis_list_camera_streams(client) -> List[str]:
    """Scan for any stream key whose name reveals a camera_id; return camera_ids."""
    cams: set = set()
    for pattern in (b"*_output_topic", b"*_input_topic", b"camera_*_input"):
        try:
            cursor = 0
            while True:
                cursor, keys = client.scan(cursor=cursor, match=pattern, count=500)
                for k in keys or []:
                    _, cam, _ = _classify_stream(_b2s(k))
                    if cam:
                        cams.add(cam)
                if cursor == 0:
                    break
        except Exception as e:
            vlog("redis scan failed:", e)
            break
    return sorted(cams)


# ────────────────────────────────────────────────────────────────────
# Per-camera correlation
# ────────────────────────────────────────────────────────────────────

@dataclass
class CameraReport:
    camera_id: str
    backend_assigned: bool = False
    backend_active: bool = False
    backend_gateway_id: Optional[str] = None
    backend_apps: List[str] = field(default_factory=list)
    backend_codec: Optional[str] = None
    backend_fps: Optional[int] = None
    backend_topic_count: int = 0
    nvdec_gpu: Optional[int] = None
    shm_path: Optional[str] = None
    shm_kind: Optional[str] = None  # 'shm_rb' | 'databus' | 'cuda_ipc' | None
    producer_alive: Optional[bool] = None
    last_frame_age_ms: Optional[float] = None
    frames_written: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    has_cuda_ipc: Optional[bool] = None
    consumers: int = 0
    consumer_max_lag: Optional[int] = None
    num_slots: Optional[int] = None
    redis_xlen: Optional[int] = None
    redis_last_age_ms: Optional[float] = None
    redis_last_frame_idx: Optional[int] = None
    redis_last_shm_name: Optional[str] = None
    redis_shm_match: Optional[bool] = None
    verdict: str = "UNKNOWN"
    reasons: List[str] = field(default_factory=list)


def correlate(
    backend_topics_by_instance: Dict[str, List[dict]],
    gpu_map: Dict[str, int],
    shm_rb_infos: Dict[str, ShmRingInfo],         # camera_id -> ShmRingInfo (shm_rb_*)
    databus_infos: Dict[str, ShmRingInfo],         # camera_id -> ShmRingInfo (databus__*__sg__frames)
    gateway_instance_ids: List[str],
    redis_states: Optional[Dict[str, RedisCameraState]] = None,
    redis_attempted: bool = False,
) -> List[CameraReport]:
    reports: Dict[str, CameraReport] = {}

    # 1. seed from backend (per-instance topics)
    for inst_id, topics in backend_topics_by_instance.items():
        for t in topics:
            cid = t.get("cameraId")
            if not cid:
                continue
            r = reports.setdefault(cid, CameraReport(camera_id=cid))
            r.backend_assigned = True
            r.backend_topic_count += 1
            if t.get("isActive"):
                r.backend_active = True
            r.backend_gateway_id = t.get("streamingGatewayId") or r.backend_gateway_id
            r.backend_codec = t.get("videoCodec") or t.get("video_codec") or r.backend_codec
            try:
                r.backend_fps = int(t.get("cameraFPS")) if t.get("cameraFPS") is not None else r.backend_fps
            except Exception:
                pass
            app_id = t.get("appDeploymentId")
            if app_id and app_id not in r.backend_apps:
                r.backend_apps.append(app_id)

    # 2. seed from gpu_camera_map
    for cid, gpu in gpu_map.items():
        r = reports.setdefault(cid, CameraReport(camera_id=cid))
        r.nvdec_gpu = gpu

    # 3. seed from SHM
    # Wall-clock-looking ts: > 2020-01-01 in nanoseconds (1.577e18). Anything
    # smaller is some monotonic/perf clock and can't be compared to wall now.
    WALL_NS_FLOOR = 1_577_000_000_000_000_000

    def _fill_shm(r: CameraReport, info: ShmRingInfo, kind: str):
        r.shm_path = info.path
        r.shm_kind = kind
        if info.layout in ("shm_rb_v2", "cuda_ipc"):
            r.frames_written = info.write_idx
            r.width = info.width or None
            r.height = info.height or None
            r.has_cuda_ipc = info.has_cuda_ipc
            r.num_slots = info.num_slots or None
            # Liveness: prefer two-shot write_idx delta (works regardless of
            # whether the producer's timestamp is wall-clock or monotonic).
            if info.write_idx_delta is not None:
                r.producer_alive = info.write_idx_delta > 0
            elif info.last_ts_ns and info.last_ts_ns > WALL_NS_FLOOR:
                r.producer_alive = info.age_ms < 2000.0
            elif info.last_ts_ns:
                # producer wrote a non-wall-clock ts — we don't know freshness
                r.producer_alive = None
            else:
                r.producer_alive = False
            # Show wall-clock age only when ts looks like wall clock; otherwise
            # express liveness via the sampled FPS (more honest).
            if info.last_ts_ns and info.last_ts_ns > WALL_NS_FLOOR:
                r.last_frame_age_ms = info.age_ms
            else:
                r.last_frame_age_ms = None
            if info.num_slots and info.consumers:
                r.consumers = len(info.consumers)
                current = info.write_idx
                r.consumer_max_lag = max((current - cur) for _, cur in info.consumers) if current else 0

    for cid, info in shm_rb_infos.items():
        r = reports.setdefault(cid, CameraReport(camera_id=cid))
        _fill_shm(r, info, "shm_rb")
    for cid, info in databus_infos.items():
        r = reports.setdefault(cid, CameraReport(camera_id=cid))
        if r.shm_path is None:
            _fill_shm(r, info, "databus")

    # Redis state per camera (xlen, last frame metadata, app deployment IDs).
    if redis_states:
        for cid, st in redis_states.items():
            r = reports.setdefault(cid, CameraReport(camera_id=cid))
            r.redis_xlen = st.total_xlen
            r.redis_last_age_ms = st.newest_age_ms
            primary = st.primary_input_stream
            if primary is not None:
                r.redis_last_frame_idx = primary.last_frame_idx
                r.redis_last_shm_name = primary.last_shm_name
                if primary.last_shm_name and r.shm_path:
                    expected = os.path.basename(r.shm_path)
                    r.redis_shm_match = (primary.last_shm_name == expected)
            # Augment backend_apps from Redis output topics if backend was empty.
            if not r.backend_apps:
                r.backend_apps = st.app_ids

    # 4. verdict
    backend_attempted = bool(backend_topics_by_instance)
    for r in reports.values():
        reasons: List[str] = []
        if r.backend_assigned and not r.shm_path:
            reasons.append("BACKEND_ASSIGNED_BUT_NO_PRODUCER")
        if not r.backend_assigned and r.shm_path and backend_attempted:
            reasons.append("ORPHAN_PRODUCER")
        if r.nvdec_gpu is not None and not r.shm_path:
            reasons.append("GPU_ASSIGNED_NO_PRODUCER")
        if r.shm_path and r.producer_alive is False:
            reasons.append("PRODUCER_STALE")
        if r.shm_path and r.producer_alive is None:
            reasons.append("UNKNOWN_SHM_FORMAT")
        if r.shm_path and r.nvdec_gpu is None and r.shm_kind in ("shm_rb", "databus"):
            reasons.append("NVDEC_NOT_ATTACHED")
        if r.shm_path and r.producer_alive and r.consumers == 0 and r.shm_kind == "shm_rb":
            # databus producer files don't use the consumer registry the same way
            reasons.append("NO_CONSUMERS")
        if r.consumer_max_lag is not None and r.num_slots and r.consumer_max_lag > r.num_slots // 2:
            reasons.append("CONSUMER_LAGGING")
        # Redis-derived
        if redis_attempted and r.shm_path and r.producer_alive and (r.redis_xlen == 0 or r.redis_xlen is None):
            reasons.append("REDIS_NOT_PUBLISHING")
        if r.redis_last_age_ms is not None and r.redis_last_age_ms > 5000:
            reasons.append("REDIS_STALE")
        if r.redis_shm_match is False:
            reasons.append("REDIS_SHM_NAME_MISMATCH")
        if not r.backend_assigned and not backend_attempted:
            reasons.append("BACKEND_UNREACHABLE")
        # A camera that's only known via empty Redis topics (no backend, no SHM,
        # no GPU map entry) is leftover config, not "OK".
        if (not r.backend_assigned and not r.shm_path and r.nvdec_gpu is None
                and r.redis_xlen == 0 and redis_attempted):
            reasons.append("INACTIVE")
        if not reasons:
            r.verdict = "OK"
        else:
            r.verdict = reasons[0]
            r.reasons = reasons
    # stable sort
    out = sorted(reports.values(), key=lambda x: (x.verdict != "OK", x.camera_id))
    return out


# ────────────────────────────────────────────────────────────────────
# Rendering
# ────────────────────────────────────────────────────────────────────

def _fmt_age(age_ms: Optional[float]) -> str:
    if age_ms is None:
        return "?"
    if age_ms == float("inf"):
        return "∞"
    if age_ms < 1000:
        return f"{age_ms:.0f}ms"
    if age_ms < 60_000:
        return f"{age_ms/1000:.1f}s"
    return f"{age_ms/60_000:.1f}m"


# Tri-state check rendering. Use ANSI when stdout is a TTY.
_USE_COLOR = sys.stdout.isatty()
_TICK = "\033[32m✓\033[0m" if _USE_COLOR else "✓"
_CROSS = "\033[31m✗\033[0m" if _USE_COLOR else "✗"
_DASH = "\033[90m·\033[0m" if _USE_COLOR else "·"


def _check(value: Optional[bool]) -> str:
    """True → ✓, False → ✗, None → · (n/a)."""
    if value is True:
        return _TICK
    if value is False:
        return _CROSS
    return _DASH


def _camera_checks(r: CameraReport, backend_attempted: bool, redis_attempted: bool) -> Dict[str, Optional[bool]]:
    """The seven binary checks shown as ✓/✗/· per camera.

    Each is True (good), False (bad), or None (n/a — not enough data to judge).
    """
    # backend assigned: only meaningful if we actually reached the backend
    backend_ok: Optional[bool] = r.backend_assigned if backend_attempted else None

    # producer present in /dev/shm
    producer_present: Optional[bool] = bool(r.shm_path)

    # producer alive (write_idx advanced or wall-clock ts is fresh)
    alive: Optional[bool] = r.producer_alive

    # NVDEC GPU mapping registered
    gpu_ok: Optional[bool] = r.nvdec_gpu is not None

    # at least one consumer attached (only meaningful for v2 ring buffers;
    # cuda_ipc files do carry a registry too, but most pipelines don't fill it)
    if r.shm_kind in ("shm_rb", "databus") and r.shm_path:
        cons_ok: Optional[bool] = r.consumers > 0
    else:
        cons_ok = None

    # redis: at least one stream has entries and isn't stale
    if redis_attempted:
        if r.redis_xlen is None or r.redis_xlen == 0:
            redis_ok: Optional[bool] = False
        elif r.redis_last_age_ms is not None and r.redis_last_age_ms > 5000:
            redis_ok = False
        else:
            redis_ok = True
    else:
        redis_ok = None

    # shm-name match: only judge when both sides reported something
    match_ok: Optional[bool] = r.redis_shm_match  # may already be None

    return {
        "backend": backend_ok,
        "producer": producer_present,
        "alive": alive,
        "gpu": gpu_ok,
        "consumers": cons_ok,
        "redis": redis_ok,
        "shm_match": match_ok,
    }


def render_table(
    containers: List[ContainerCtx],
    reports: List[CameraReport],
    gpu_map: Dict[str, int],
    shm_artefacts: Dict[str, List[str]],
    gfc: Optional[int],
    backend_errors: Dict[str, str],
    rinfo: Optional[RedisInfo] = None,
):
    if _RICH:
        return _render_rich(containers, reports, gpu_map, shm_artefacts, gfc, backend_errors, rinfo)
    return _render_plain(containers, reports, gpu_map, shm_artefacts, gfc, backend_errors, rinfo)


_VERDICT_STYLE = {
    "OK": "bold green",
    "BACKEND_ASSIGNED_BUT_NO_PRODUCER": "bold red",
    "ORPHAN_PRODUCER": "bold yellow",
    "PRODUCER_STALE": "bold red",
    "UNKNOWN_SHM_FORMAT": "yellow",
    "GPU_ASSIGNED_NO_PRODUCER": "bold red",
    "NVDEC_NOT_ATTACHED": "red",
    "NO_CONSUMERS": "yellow",
    "CONSUMER_LAGGING": "yellow",
    "REDIS_NOT_PUBLISHING": "red",
    "REDIS_STALE": "yellow",
    "REDIS_SHM_NAME_MISMATCH": "red",
    "BACKEND_UNREACHABLE": "magenta",
    "INACTIVE": "dim",
}


def _rich_check(value: Optional[bool]) -> "Text":
    if value is True:
        return Text("✓", style="bold green")
    if value is False:
        return Text("✗", style="bold red")
    return Text("·", style="dim")


def _render_rich(containers, reports, gpu_map, shm_artefacts, gfc, backend_errors, rinfo):
    # Force a sensible width when piped (rich otherwise falls back to 80 cols
    # and squashes everything). When stdout is a real TTY, let rich autodetect.
    width = None
    if not sys.stdout.isatty():
        try:
            width = max(160, int(os.environ.get("COLUMNS", "180")))
        except ValueError:
            width = 180
    console = Console(width=width)

    # ── Containers panel ────────────────────────────────────────────────
    ct = Table(title="containers", box=box.SIMPLE_HEAVY, header_style="bold cyan",
               title_style="bold cyan", show_lines=False, expand=False)
    ct.add_column("role", style="cyan", no_wrap=True)
    ct.add_column("instance_id", style="white")
    ct.add_column("name")
    ct.add_column("status")
    role_color = {"gateway": "green", "inference": "blue", "analytics": "magenta",
                  "fs_streaming": "cyan", "video_storage": "yellow", "unknown": "dim"}
    for c in containers:
        status_style = "green" if c.status.startswith("Up") else (
            "red" if "Restart" in c.status or "Exit" in c.status else "yellow")
        ct.add_row(
            Text(c.role, style=role_color.get(c.role, "white")),
            c.instance_id or "-",
            c.name,
            Text(c.status, style=status_style),
        )
    console.print(ct)

    if backend_errors:
        msg = "\n".join(f"  [bold]{k}[/]: {v[:200]}" for k, v in backend_errors.items())
        console.print(Panel(msg, title="backend errors", border_style="red", expand=False))

    # ── /dev/shm summary panel ──────────────────────────────────────────
    shm_lines = []
    for k, v in shm_artefacts.items():
        n = len(v)
        marker = "[green]●[/]" if n else "[dim]○[/]"
        shm_lines.append(f"  {marker} {k:<22} [bold]{n}[/] file(s)")
    if gfc is not None:
        shm_lines.append(f"  [cyan]global_frame_counter[/]   {gfc}")
    if gpu_map:
        gpus = ", ".join(f"GPU{g}:{cid[:8]}…" for cid, g in sorted(gpu_map.items(), key=lambda x: x[1]))
        shm_lines.append(f"  [cyan]gpu_camera_map[/]         {len(gpu_map)} cameras → {gpus}")
    if rinfo:
        shm_lines.append(f"  [cyan]redis[/]                  {rinfo.host}:{rinfo.port} "
                         f"(auth={rinfo.auth}, source={rinfo.source})")
    console.print(Panel("\n".join(shm_lines), title="/dev/shm + redis", border_style="blue", expand=False))

    # ── Per-camera table ────────────────────────────────────────────────
    if not reports:
        console.print(Panel("[dim](no cameras seen — no backend topics, no SHM segments, no GPU map)[/]",
                            border_style="yellow", expand=False))
        return

    backend_attempted = bool(backend_errors) or any(
        r.backend_assigned or r.backend_topic_count > 0 for r in reports)
    redis_attempted = rinfo is not None

    cam = Table(title="per-camera report", box=box.HEAVY_HEAD, header_style="bold cyan",
                title_style="bold cyan", show_lines=False, expand=False, padding=(0, 1))
    cam.add_column("camera_id", style="white", no_wrap=True, min_width=24)
    # Readable headers for the seven binary checks.
    check_headers = [
        ("backend", "assigned by backend"),
        ("shm file", "/dev/shm producer file present"),
        ("writing", "producer is advancing write_idx"),
        ("gpu map", "listed in /dev/shm/gpu_camera_map"),
        ("consumer", "≥1 consumer attached to SHM"),
        ("redis", "redis stream has fresh entries"),
        ("shm=redis", "redis last shm_name matches /dev/shm file"),
    ]
    for hdr, _tip in check_headers:
        cam.add_column(hdr, justify="center", no_wrap=True)
    cam.add_column("gpu", justify="right", style="cyan", no_wrap=True)
    cam.add_column("frames", justify="right", style="white", no_wrap=True)
    cam.add_column("resolution", justify="right", style="dim", no_wrap=True)
    cam.add_column("apps", justify="right", style="magenta", no_wrap=True)
    cam.add_column("redis xlen", justify="right", no_wrap=True)
    cam.add_column("redis age", justify="right", style="dim", no_wrap=True)
    cam.add_column("verdict", style="white", no_wrap=True)

    for r in reports:
        ck = _camera_checks(r, backend_attempted, redis_attempted)
        verdict_style = _VERDICT_STYLE.get(r.verdict, "white")
        cam.add_row(
            r.camera_id,
            _rich_check(ck["backend"]),
            _rich_check(ck["producer"]),
            _rich_check(ck["alive"]),
            _rich_check(ck["gpu"]),
            _rich_check(ck["consumers"]),
            _rich_check(ck["redis"]),
            _rich_check(ck["shm_match"]),
            str(r.nvdec_gpu) if r.nvdec_gpu is not None else "-",
            f"{r.frames_written:,}" if r.frames_written else "-",
            f"{r.width}×{r.height}" if r.width and r.height else "-",
            str(len(r.backend_apps)) if r.backend_apps else "0",
            f"{r.redis_xlen:,}" if r.redis_xlen else "0",
            _fmt_age(r.redis_last_age_ms),
            Text(r.verdict, style=verdict_style),
        )
    console.print(cam)

    # ── Legend + summary ────────────────────────────────────────────────
    legend_table = Table(box=None, show_header=False, padding=(0, 2), expand=False)
    legend_table.add_column(style="bold")
    legend_table.add_column(style="dim")
    legend_table.add_row("[bold green]✓[/] / [bold red]✗[/] / [dim]·[/]",
                         "ok / issue / not-applicable")
    for hdr, tip in check_headers:
        legend_table.add_row(hdr, tip)
    console.print(Panel(legend_table, title="column key", border_style="dim", expand=False))

    from collections import Counter
    cnt = Counter(r.verdict for r in reports)
    total = sum(cnt.values())
    ok = cnt.get("OK", 0)
    bad = total - ok
    summary_table = Table(box=box.MINIMAL, show_header=False, expand=False, title=None)
    summary_table.add_column(justify="right")
    summary_table.add_column()
    color = "green" if bad == 0 else ("yellow" if ok > 0 else "red")
    summary_table.add_row(Text(f"{ok}/{total}", style=f"bold {color}"), Text("OK", style=color))
    if bad:
        summary_table.add_row(Text(f"{bad}", style="bold red"), Text("broken", style="red"))
        for v, n in sorted(cnt.items(), key=lambda x: (-x[1], x[0])):
            if v == "OK":
                continue
            summary_table.add_row(Text(f"{n}", style="bold"),
                                  Text(v, style=_VERDICT_STYLE.get(v, "white")))
    console.print(Panel(summary_table, title="summary", border_style="green" if bad == 0 else "red",
                        expand=False))


def _render_plain(containers, reports, gpu_map, shm_artefacts, gfc, backend_errors, rinfo):
    print("=" * 100)
    print("CONTAINERS")
    print("=" * 100)
    print(f"{'role':<14} {'instance_id':<26} {'name':<55} {'status'}")
    for c in containers:
        iid = c.instance_id or "-"
        print(f"{c.role:<14} {iid:<26} {c.name:<55} {c.status}")
    if backend_errors:
        print()
        print("BACKEND ERRORS")
        for inst, err in backend_errors.items():
            print(f"  {inst}: {err}")

    print()
    print("=" * 100)
    print("/dev/shm SUMMARY")
    print("=" * 100)
    for k, v in shm_artefacts.items():
        print(f"  {k:<22} {len(v)} file(s)")
    if gfc is not None:
        print(f"  global_frame_counter   {gfc}")
    if gpu_map:
        print(f"  gpu_camera_map         {len(gpu_map)} cameras → GPUs: {gpu_map}")
    if rinfo:
        print(f"  redis                  {rinfo.host}:{rinfo.port} (auth={rinfo.auth}, source={rinfo.source})")

    print()
    print("=" * 100)
    print("PER-CAMERA REPORT")
    print("=" * 100)
    if not reports:
        print("  (no cameras seen — no backend topics, no SHM segments, no GPU map)")
    else:
        backend_attempted = any(c.get("backend") is not None for c in
                                (_camera_checks(r, True, rinfo is not None) for r in reports[:1]))
        # use real signals: did we have any topics or backend_errors?
        backend_attempted = bool(backend_errors) or any(
            (r.backend_assigned or r.backend_topic_count > 0) for r in reports
        )
        redis_attempted = rinfo is not None

        # Two-row header: short codes above, key below.
        hdr1 = (f"{'camera_id':<26}  bk pr al gp co rd sm  "
                f"{'gpu':>3} {'frames':>10} {'cons':>4} {'apps':>4} "
                f"{'r_xlen':>7} {'r_age':>7} {'verdict'}")
        print(hdr1)
        print("-" * 100)
        for r in reports:
            ck = _camera_checks(r, backend_attempted, redis_attempted)
            cells = "  ".join(_check(ck[k]) for k in
                              ("backend", "producer", "alive", "gpu", "consumers", "redis", "shm_match"))
            print(f"{r.camera_id:<26}  {cells}  "
                  f"{(r.nvdec_gpu if r.nvdec_gpu is not None else '-'):>3} "
                  f"{(r.frames_written if r.frames_written is not None else '-'):>10} "
                  f"{r.consumers:>4} "
                  f"{len(r.backend_apps):>4} "
                  f"{(r.redis_xlen if r.redis_xlen is not None else '-'):>7} "
                  f"{_fmt_age(r.redis_last_age_ms):>7} "
                  f"{r.verdict}")
        print()
        print(f"  Legend: {_TICK} ok  {_CROSS} issue  {_DASH} n/a   |   "
              f"bk=backend assigned  pr=producer file  al=producer alive  "
              f"gp=NVDEC gpu_map  co=consumer attached  rd=redis publishing  "
              f"sm=shm name matches redis")

        print()
        # summary
        from collections import Counter
        cnt = Counter(r.verdict for r in reports)
        total = sum(cnt.values())
        ok = cnt.get("OK", 0)
        bad = total - ok
        print(f"SUMMARY: {ok}/{total} OK, {bad} broken")
        for v, n in sorted(cnt.items(), key=lambda x: (-x[1], x[0])):
            if v != "OK":
                print(f"  {n:>3}  {v}")


def render_json(
    containers: List[ContainerCtx],
    reports: List[CameraReport],
    gpu_map: Dict[str, int],
    shm_artefacts: Dict[str, List[str]],
    gfc: Optional[int],
    backend_errors: Dict[str, str],
    rinfo: Optional[RedisInfo] = None,
):
    out = {
        "containers": [c.public_dict() for c in containers],
        "shm_artefacts": {k: [os.path.basename(p) for p in v] for k, v in shm_artefacts.items()},
        "gpu_camera_map": gpu_map,
        "global_frame_counter": gfc,
        "redis": asdict(rinfo) if rinfo else None,
        "backend_errors": backend_errors,
        "cameras": [asdict(r) for r in reports],
    }
    print(json.dumps(out, indent=2, default=str))


# ────────────────────────────────────────────────────────────────────
# Top-level commands
# ────────────────────────────────────────────────────────────────────

def collect_state(args) -> Tuple[
    List[ContainerCtx],
    List[CameraReport],
    Dict[str, int],
    Dict[str, List[str]],
    Optional[int],
    Dict[str, str],
    Dict[str, List[dict]],
    Dict[str, ShmRingInfo],
    Dict[str, ShmRingInfo],
    Dict[str, RedisCameraState],
    Optional[RedisInfo],
]:
    # 1. discover containers
    containers = discover_containers()
    if args.container:
        containers = [c for c in containers
                      if args.container in (c.docker_id, c.name) or c.docker_id.startswith(args.container)]

    # 2. backend per matrice instance (gateway + app)
    backend_topics: Dict[str, List[dict]] = {}
    backend_errors: Dict[str, str] = {}
    if not args.no_backend:
        # cluster containers by (access_key, secret_key, base_url) and reuse one client
        clients: Dict[Tuple[str, str, str], BackendClient] = {}
        for c in containers:
            if not c.access_key or not c.secret_key or not c.instance_id:
                continue
            if c.role not in ("gateway", "inference", "analytics"):
                continue
            key = (c.access_key, c.secret_key, c.base_url or DEFAULT_BASE_URL)
            cli = clients.get(key)
            if cli is None:
                cli = BackendClient(c.access_key, c.secret_key, c.base_url or DEFAULT_BASE_URL)
                try:
                    cli.auth()
                except BackendError as e:
                    backend_errors[mask(c.access_key)] = f"auth failed: {e}"
                    continue
                clients[key] = cli
            try:
                topics = cli.consuming_topics(c.instance_id)
                backend_topics[c.instance_id] = topics
            except BackendError as e:
                backend_errors[c.instance_id] = str(e)

    # 3. SHM
    shm_artefacts = list_shm_artefacts() if not args.no_shm else {k: [] for k in
        ("shm_rb", "databus", "databus_status", "cuda_ipc", "gpu_camera_map", "global_frame_counter")}
    gpu_map = read_gpu_camera_map() if not args.no_shm else {}
    gfc = read_global_frame_counter() if not args.no_shm else None

    shm_rb_infos: Dict[str, ShmRingInfo] = {}
    databus_infos: Dict[str, ShmRingInfo] = {}
    if not args.no_shm:
        for p in shm_artefacts["shm_rb"]:
            info = parse_ring_header(p)
            if not info:
                continue
            cid = os.path.basename(p)[len(RB_PREFIX):]
            shm_rb_infos[cid] = info
        for p in shm_artefacts["databus"]:
            base = os.path.basename(p)
            parsed = parse_databus_name(base)
            if not parsed:
                continue
            cid, node, port = parsed
            # Only one databus file per camera per node — prefer the one that
            # parses as a ring header.
            info = parse_ring_header(p)
            if info is None:
                continue
            if cid not in databus_infos:
                databus_infos[cid] = info

        # Two-shot write_idx sampling for cuda_ipc layout (timestamps in those
        # files aren't wall-clock, so we can only judge liveness by movement).
        # Runs once per call, in parallel for all targets, ~1 s wall time.
        sample_targets: List[Tuple[str, ShmRingInfo, Dict[str, ShmRingInfo]]] = []
        for cid, info in databus_infos.items():
            if info.layout == "cuda_ipc":
                sample_targets.append((cid, info, databus_infos))
        for cid, info in shm_rb_infos.items():
            if info.layout == "cuda_ipc":
                sample_targets.append((cid, info, shm_rb_infos))
        if sample_targets and not getattr(args, "no_sample", False):
            t0 = time.time()
            first = {cid: info.write_idx for cid, info, _ in sample_targets}
            time.sleep(getattr(args, "sample_seconds", 1.0))
            t1 = time.time()
            for cid, info, store in sample_targets:
                later = _read_write_idx(info.path)
                if later is None:
                    continue
                window_ms = (t1 - t0) * 1000
                delta = later - first[cid]
                fps = (delta / (window_ms / 1000)) if window_ms > 0 else None
                # Replace the dataclass with an updated copy
                store[cid] = ShmRingInfo(
                    **{**asdict(info),
                       "write_idx": later,
                       "write_idx_delta": delta,
                       "sample_window_ms": window_ms,
                       "estimated_fps": fps},
                )

    # 4. Redis: discover from local container, scan camera_*_input streams.
    redis_states: Dict[str, RedisCameraState] = {}
    redis_attempted = False
    redis_info: Optional[RedisInfo] = None
    if not args.no_redis:
        found = discover_redis_from_containers(containers)
        if found:
            redis_info, password = found
            client = redis_connect(redis_info, password)
            if client is not None:
                redis_attempted = True
                # union of camera_ids from all sources + a SCAN for stragglers
                cams = set()
                for ts in backend_topics.values():
                    for t in ts:
                        if t.get("cameraId"):
                            cams.add(t["cameraId"])
                cams.update(gpu_map.keys())
                cams.update(shm_rb_infos.keys())
                cams.update(databus_infos.keys())
                cams.update(redis_list_camera_streams(client))
                for cid in cams:
                    redis_states[cid] = redis_probe_camera(client, cid)
                try:
                    client.close()
                except Exception:
                    pass

    gateway_iids = [c.instance_id for c in containers if c.role == "gateway" and c.instance_id]
    reports = correlate(backend_topics, gpu_map, shm_rb_infos, databus_infos, gateway_iids,
                        redis_states=redis_states, redis_attempted=redis_attempted)

    return containers, reports, gpu_map, shm_artefacts, gfc, backend_errors, backend_topics, shm_rb_infos, databus_infos, redis_states, redis_info


def cmd_status(args):
    containers, reports, gpu_map, shm_artefacts, gfc, errs, _topics, _rb, _db, _rstates, rinfo = collect_state(args)
    if args.json:
        render_json(containers, reports, gpu_map, shm_artefacts, gfc, errs, rinfo)
    else:
        render_table(containers, reports, gpu_map, shm_artefacts, gfc, errs, rinfo)


def cmd_containers(args):
    cs = discover_containers()
    if args.container:
        cs = [c for c in cs
              if args.container in (c.docker_id, c.name) or c.docker_id.startswith(args.container)]
    if args.json:
        print(json.dumps([c.public_dict() for c in cs], indent=2))
    else:
        for c in cs:
            print(f"[{c.role}] {c.name}  docker_id={c.docker_id[:12]}  "
                  f"instance_id={c.instance_id}  action_id={c.action_id}  "
                  f"ak={mask(c.access_key)}  base={c.base_url}")


def cmd_cameras(args):
    args.no_shm = True
    args.no_redis = True
    containers, _, _, _, _, errs, topics, _, _, _, _ = collect_state(args)
    if args.json:
        print(json.dumps({"errors": errs, "topics_by_instance": topics}, indent=2))
        return
    for inst_id, ts in topics.items():
        print(f"\n=== instance {inst_id} : {len(ts)} consuming topic(s) ===")
        cams = {}
        for t in ts:
            cams.setdefault(t.get("cameraId"), []).append(t)
        for cid, lst in cams.items():
            apps = sorted({t.get("appDeploymentId") for t in lst if t.get("appDeploymentId")})
            sg = lst[0].get("streamingGatewayId")
            codec = lst[0].get("videoCodec") or lst[0].get("video_codec")
            fps = lst[0].get("cameraFPS")
            active = any(t.get("isActive") for t in lst)
            print(f"  {cid}  active={active}  codec={codec}  fps={fps}  sg={sg}  apps={apps}")
    if errs:
        print("\nerrors:", errs)


def cmd_shm(args):
    art = list_shm_artefacts()
    gpu_map = read_gpu_camera_map()
    gfc = read_global_frame_counter()
    statuses = read_databus_status_all()
    if args.json:
        out = {"artefacts": {k: v for k, v in art.items()},
               "gpu_camera_map": gpu_map,
               "global_frame_counter": gfc,
               "databus_status": statuses}
        print(json.dumps(out, indent=2, default=str))
        return
    print(f"global_frame_counter = {gfc}")
    print(f"gpu_camera_map = {gpu_map}")
    print(f"databus_status nodes = {len(statuses)}")
    for s in statuses:
        node = s.get("_node_id") or s.get("node_id")
        hb = s.get("last_heartbeat_ns") or 0
        age_ms = (time.time_ns() - hb) / 1_000_000 if hb else float("inf")
        print(f"  node={node}  status={s.get('status')}  age={_fmt_age(age_ms)}  buffers={s.get('buffer_addresses')}")
    for kind in ("shm_rb", "databus", "cuda_ipc"):
        files = art[kind]
        print(f"\n{kind} ({len(files)}):")
        for p in files:
            info = parse_ring_header(p)
            if info is None:
                print(f"  {p}  (could not parse)")
                continue
            print(f"  {os.path.basename(p):<70} "
                  f"layout={info.layout:<10} size={info.size:>8} "
                  f"slots={info.num_slots:>4} write_idx={info.write_idx:>8} "
                  f"age={_fmt_age(info.age_ms):>7} gpu={info.gpu_id} "
                  f"{info.width}x{info.height} cuda_ipc={info.has_cuda_ipc} "
                  f"consumers={len(info.consumers)}")


def cmd_gpu_map(args):
    m = read_gpu_camera_map()
    if args.json:
        print(json.dumps(m, indent=2))
    else:
        if not m:
            print("(empty or missing)")
            return
        for cid, gpu in sorted(m.items(), key=lambda x: (x[1], x[0])):
            print(f"  GPU{gpu}  {cid}")


def cmd_camera(args):
    cid = args.camera_id
    containers, reports, gpu_map, art, gfc, errs, topics, rb, db, rstates, rinfo = collect_state(args)
    target = next((r for r in reports if r.camera_id == cid), None)
    if args.json:
        print(json.dumps(asdict(target) if target else {"camera_id": cid, "found": False}, indent=2, default=str))
        return
    if not target:
        print(f"camera {cid} not found in any source (backend topics, /dev/shm, gpu_camera_map)")
        return
    print(f"camera_id           {target.camera_id}")
    print(f"verdict             {target.verdict}   reasons={target.reasons}")
    print(f"backend_assigned    {target.backend_assigned}  active={target.backend_active}  topics={target.backend_topic_count}")
    print(f"backend_gateway_id  {target.backend_gateway_id}")
    print(f"backend_apps        {target.backend_apps}")
    print(f"backend_codec/fps   {target.backend_codec} / {target.backend_fps}")
    print(f"nvdec_gpu           {target.nvdec_gpu}")
    print(f"shm_path/kind       {target.shm_path}  ({target.shm_kind})")
    print(f"producer_alive      {target.producer_alive}  age={_fmt_age(target.last_frame_age_ms)}")
    print(f"frames_written      {target.frames_written}")
    res = f"{target.width}x{target.height}" if target.width and target.height else "-"
    print(f"resolution          {res}  cuda_ipc={target.has_cuda_ipc}")
    print(f"consumers           {target.consumers}  max_lag={target.consumer_max_lag}")
    info = rb.get(cid) or db.get(cid)
    if info:
        print(f"shm_layout          {info.layout}  size={info.size}  num_slots={info.num_slots}")
        if info.last_slot_frame_idx is not None:
            print(f"last_slot           frame_idx={info.last_slot_frame_idx} ts_ns={info.last_slot_ts_ns}")
    if info and info.consumers:
        print("consumer registry:")
        for kh, cur in info.consumers:
            print(f"  key_hash=0x{kh:016x}  cursor={cur}  lag={info.write_idx - cur if info.write_idx else '?'}")
    rs = rstates.get(cid) if rstates else None
    if rs:
        print(f"redis_streams       {len(rs.streams)} matched  app_ids={rs.app_ids}")
        for s in rs.streams:
            print(f"  [{s.kind:<7}] {s.name}  xlen={s.xlen}  "
                  f"last_id={s.last_id}  age={_fmt_age(s.last_age_ms)}  "
                  f"frame_idx={s.last_frame_idx}  shm={s.last_shm_name}"
                  + (f"  err={s.error}" if s.error else ""))
        if rs.error:
            print(f"redis_error         {rs.error}")


# ────────────────────────────────────────────────────────────────────
# main
# ────────────────────────────────────────────────────────────────────

def main(argv=None):
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="emit JSON instead of human table")
    common.add_argument("--no-shm", action="store_true", help="skip /dev/shm inspection")
    common.add_argument("--no-backend", action="store_true", help="skip backend API calls")
    common.add_argument("--no-redis", action="store_true", help="skip redis (currently never enabled)")
    common.add_argument("--container", help="filter to a single container (id prefix or name)")
    common.add_argument("-v", "--verbose", action="store_true")

    p = argparse.ArgumentParser(prog="python -m matrice_common.debug",
                                description=__doc__,
                                parents=[common],
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("status", parents=[common], help="full per-camera report (default)")
    sub.add_parser("containers", parents=[common], help="list discovered matrice containers + masked creds")
    sub.add_parser("cameras", parents=[common], help="list backend assignment per instance")
    sub.add_parser("shm", parents=[common], help="dump /dev/shm artefacts + ring-buffer headers")
    sub.add_parser("gpu-map", parents=[common], help="dump /dev/shm/gpu_camera_map")
    sp_cam = sub.add_parser("camera", parents=[common], help="deep dive on one camera")
    sp_cam.add_argument("camera_id")

    args = p.parse_args(argv)
    global VERBOSE
    VERBOSE = args.verbose
    if not args.cmd:
        args.cmd = "status"

    if args.cmd == "status":
        cmd_status(args)
    elif args.cmd == "containers":
        cmd_containers(args)
    elif args.cmd == "cameras":
        cmd_cameras(args)
    elif args.cmd == "shm":
        cmd_shm(args)
    elif args.cmd == "gpu-map":
        cmd_gpu_map(args)
    elif args.cmd == "camera":
        cmd_camera(args)
