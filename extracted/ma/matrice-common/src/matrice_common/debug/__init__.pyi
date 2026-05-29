"""Stub file for debug directory."""
from typing import Any, Dict, List, Optional, Tuple

from .cli import main

# Constants
CIRB_HEADER_SIZE: int = ...  # From cli
CIRB_SESSION_SIZE: int = ...  # From cli
CIRB_SLOT_META_BASE: Any = ...  # From cli
CIRB_SLOT_META_SIZE: int = ...  # From cli
CUDA_IPC_PREFIX: str = ...  # From cli
DATABUS_PREFIX: str = ...  # From cli
DATABUS_RE: Any = ...  # From cli
DBSTATUS_PREFIX: str = ...  # From cli
DEFAULT_BASE_URL: Any = ...  # From cli
GFC_FILE: str = ...  # From cli
GPU_MAP_FILE: str = ...  # From cli
HDR_CONSUMER_COUNT: int = ...  # From cli
HDR_CONSUMER_SLOT: int = ...  # From cli
HDR_OFF_CONSUMERS: int = ...  # From cli
HDR_OFF_FRAME_FORMAT: int = ...  # From cli
HDR_OFF_GPU_ID: int = ...  # From cli
HDR_OFF_HEIGHT: int = ...  # From cli
HDR_OFF_IPC_HANDLE: int = ...  # From cli
HDR_OFF_MAGIC: int = ...  # From cli
HDR_OFF_NUM_SLOTS: int = ...  # From cli
HDR_OFF_TIMESTAMP_NS: int = ...  # From cli
HDR_OFF_VERSION: int = ...  # From cli
HDR_OFF_WIDTH: int = ...  # From cli
HDR_OFF_WRITE_IDX: int = ...  # From cli
NAME_RE: Any = ...  # From cli
RB_PREFIX: str = ...  # From cli
REDIS_INPUT_FMT_LEGACY: str = ...  # From cli
REDIS_INPUT_FMT_TOPIC: str = ...  # From cli
REDIS_PER_CAMERA_PATTERNS: List[Any] = ...  # From cli
RING_HDR_MAGIC: int = ...  # From cli
RKEY_FRAME_FORMAT: Any = ...  # From cli
RKEY_FRAME_IDX: Any = ...  # From cli
RKEY_HEIGHT: Any = ...  # From cli
RKEY_RTP: Any = ...  # From cli
RKEY_SHM_NAME: Any = ...  # From cli
RKEY_TS_NS: Any = ...  # From cli
RKEY_WIDTH: Any = ...  # From cli
ROLE_PATTERNS: List[Any] = ...  # From cli
SHM_BASE: Any = ...  # From cli
VERBOSE: bool = ...  # From cli

# Functions
# From cli
def cmd_camera(args: Any) -> Any: ...

# From cli
def cmd_cameras(args: Any) -> Any: ...

# From cli
def cmd_containers(args: Any) -> Any: ...

# From cli
def cmd_gpu_map(args: Any) -> Any: ...

# From cli
def cmd_shm(args: Any) -> Any: ...

# From cli
def cmd_status(args: Any) -> Any: ...

# From cli
def collect_state(args: Any) -> Tuple[List[Any], List[Any], Dict[str, int], Dict[str, List[str]], Optional[int], Dict[str, str], Dict[str, List[dict]], Dict[str, Any], Dict[str, Any], Dict[str, Any], Optional[Any]]: ...

# From cli
def correlate(backend_topics_by_instance: Dict[str, List[dict]], gpu_map: Dict[str, int], shm_rb_infos: Dict[str, Any], databus_infos: Dict[str, Any], gateway_instance_ids: List[str], redis_states: Optional[Dict[str, Any]] = None, redis_attempted: bool = False) -> List[Any]: ...

# From cli
def discover_containers() -> List[Any]:
    """
    List every running container and pull matrice-relevant context.
    
        Read-only. Skips obvious non-matrice things (chromium, jupyter) by name.
    """
    ...

# From cli
def discover_redis_from_containers(containers: List[Any]) -> Optional[Tuple[Any, str]]:
    """
    Find a redis container on this host and pull --requirepass from its Cmd.
    
        Returns (RedisInfo, password) or None. The password is kept in-memory only.
    """
    ...

# From cli
def list_shm_artefacts() -> Dict[str, List[str]]: ...

# From cli
def main(argv: Any = None) -> Any: ...

# From cli
def mask(s: Optional[str]) -> str: ...

# From cli
def parse_databus_name(basename: str) -> Optional[Tuple[str, str, str]]: ...

# From cli
def parse_ring_header(path: str) -> Optional[Any]:
    """
    Parse a SHM ring buffer file. Handles both ShmRingBuffer-v2 (768B header,
        'MATR' magic at 676) and CudaIpcRingBuffer (648B header + 16B session +
        num_slots*32 slot meta, no magic). Falls back to layout='unknown' so the
        caller can ignore parsed fields.
    """
    ...

# From cli
def read_databus_status_all() -> List[dict]:
    """
    Length-prefixed JSON per file at /dev/shm/databus_status__*.
    """
    ...

# From cli
def read_global_frame_counter() -> Optional[int]: ...

# From cli
def read_gpu_camera_map() -> Dict[str, int]:
    """
    Read the GpuCameraMap SHM file. Format: <uint32 length><JSON>.
    """
    ...

# From cli
def redis_connect(info: Any, password: Optional[str]) -> Any:
    """
    Return a redis-py client or None. Read-only intent — caller must only
        issue read commands (XLEN, XREVRANGE, XINFO, KEYS, SCAN).
    """
    ...

# From cli
def redis_list_camera_streams(client: Any) -> List[str]:
    """
    Scan for any stream key whose name reveals a camera_id; return camera_ids.
    """
    ...

# From cli
def redis_probe_camera(client: Any, camera_id: str) -> Any:
    """
    Find every stream key matching this camera and probe each.
    """
    ...

# From cli
def render_json(containers: List[Any], reports: List[Any], gpu_map: Dict[str, int], shm_artefacts: Dict[str, List[str]], gfc: Optional[int], backend_errors: Dict[str, str], rinfo: Optional[Any] = None) -> Any: ...

# From cli
def render_table(containers: List[Any], reports: List[Any], gpu_map: Dict[str, int], shm_artefacts: Dict[str, List[str]], gfc: Optional[int], backend_errors: Dict[str, str], rinfo: Optional[Any] = None) -> Any: ...

# From cli
def vlog(*a: Any) -> Any: ...

# Classes
# From cli
class BackendClient:
    def __init__(self: Any, access_key: str, secret_key: str, base_url: str, timeout: float = 10.0) -> None: ...

    def auth(self: Any) -> str: ...

    def camera_ips(self: Any, camera_ids: List[str]) -> Dict[str, str]: ...

    def consuming_topics(self: Any, instance_id: str) -> List[dict]: ...

    def output_topics(self: Any, deployment_id: str, instance_id: str) -> List[dict]: ...

    def redis_for_instance(self: Any, instance_id: str, action_id: Optional[str] = None) -> Optional[dict]: ...


# From cli
class BackendError(Exception):
    ...

# From cli
class CameraReport:
    ...

# From cli
class ContainerCtx:
    def public_dict(self: Any) -> dict: ...


# From cli
class RedisCameraState:
    def app_ids(self: Any) -> List[str]: ...

    def newest_age_ms(self: Any) -> Optional[float]: ...

    def primary_input_stream(self: Any) -> Optional[Any]: ...

    def total_xlen(self: Any) -> int: ...


# From cli
class RedisInfo:
    ...

# From cli
class RedisStream:
    ...

# From cli
class ShmRingInfo:
    ...

from . import __main__, cli