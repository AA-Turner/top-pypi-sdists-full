"""Auto-generated stub for module: cli."""
from typing import Any, Dict, List, Optional, Tuple

# Constants
CIRB_HEADER_SIZE: int
CIRB_SESSION_SIZE: int
CIRB_SLOT_META_BASE: Any
CIRB_SLOT_META_SIZE: int
CUDA_IPC_PREFIX: str
DATABUS_PREFIX: str
DATABUS_RE: Any
DBSTATUS_PREFIX: str
DEFAULT_BASE_URL: Any
GFC_FILE: str
GPU_MAP_FILE: str
HDR_CONSUMER_COUNT: int
HDR_CONSUMER_SLOT: int
HDR_OFF_CONSUMERS: int
HDR_OFF_FRAME_FORMAT: int
HDR_OFF_GPU_ID: int
HDR_OFF_HEIGHT: int
HDR_OFF_IPC_HANDLE: int
HDR_OFF_MAGIC: int
HDR_OFF_NUM_SLOTS: int
HDR_OFF_TIMESTAMP_NS: int
HDR_OFF_VERSION: int
HDR_OFF_WIDTH: int
HDR_OFF_WRITE_IDX: int
NAME_RE: Any
RB_PREFIX: str
REDIS_INPUT_FMT_LEGACY: str
REDIS_INPUT_FMT_TOPIC: str
REDIS_PER_CAMERA_PATTERNS: List[Any]
RING_HDR_MAGIC: int
RKEY_FRAME_FORMAT: Any
RKEY_FRAME_IDX: Any
RKEY_HEIGHT: Any
RKEY_RTP: Any
RKEY_SHM_NAME: Any
RKEY_TS_NS: Any
RKEY_WIDTH: Any
ROLE_PATTERNS: List[Any]
SHM_BASE: Any
STYLE_BOLD_CYAN: str
STYLE_BOLD_RED: str
VERBOSE: bool

# Functions
def cmd_camera(args: Any) -> Any: ...
def cmd_cameras(args: Any) -> Any: ...
def cmd_containers(args: Any) -> Any: ...
def cmd_gpu_map(args: Any) -> Any: ...
def cmd_shm(args: Any) -> Any: ...
def cmd_status(args: Any) -> Any: ...
def collect_state(args: Any) -> Tuple[List[Any], List[Any], Dict[str, int], Dict[str, List[str]], Optional[int], Dict[str, str], Dict[str, List[dict]], Dict[str, Any], Dict[str, Any], Dict[str, Any], Optional[Any]]: ...
def correlate(backend_topics_by_instance: Dict[str, List[dict]], gpu_map: Dict[str, int], shm_rb_infos: Dict[str, Any], databus_infos: Dict[str, Any], gateway_instance_ids: List[str], redis_states: Optional[Dict[str, Any]] = None, redis_attempted: bool = False) -> List[Any]: ...
def discover_containers() -> List[Any]:
    """
    List every running container and pull matrice-relevant context.
    
        Read-only. Skips obvious non-matrice things (chromium, jupyter) by name.
    """
    ...
def discover_redis_from_containers(containers: List[Any]) -> Optional[Tuple[Any, str]]:
    """
    Find a redis container on this host and pull --requirepass from its Cmd.
    
        Returns (RedisInfo, password) or None. The password is kept in-memory only.
    """
    ...
def list_shm_artefacts() -> Dict[str, List[str]]: ...
def main(argv: Any = None) -> Any: ...
def mask(s: Optional[str]) -> str: ...
def parse_databus_name(basename: str) -> Optional[Tuple[str, str, str]]: ...
def parse_ring_header(path: str) -> Optional[Any]:
    """
    Parse a SHM ring buffer file. Handles both ShmRingBuffer-v2 (768B header,
        'MATR' magic at 676) and CudaIpcRingBuffer (648B header + 16B session +
        num_slots*32 slot meta, no magic). Falls back to layout='unknown' so the
        caller can ignore parsed fields.
    """
    ...
def read_databus_status_all() -> List[dict]:
    """
    Length-prefixed JSON per file at /dev/shm/databus_status__*.
    """
    ...
def read_global_frame_counter() -> Optional[int]: ...
def read_gpu_camera_map() -> Dict[str, int]:
    """
    Read the GpuCameraMap SHM file. Format: <uint32 length><JSON>.
    """
    ...
def redis_connect(info: Any, password: Optional[str]) -> Any:
    """
    Return a redis-py client or None. Read-only intent — caller must only
        issue read commands (XLEN, XREVRANGE, XINFO, KEYS, SCAN).
    """
    ...
def redis_list_camera_streams(client: Any) -> List[str]:
    """
    Scan for any stream key whose name reveals a camera_id; return camera_ids.
    """
    ...
def redis_probe_camera(client: Any, camera_id: str) -> Any:
    """
    Find every stream key matching this camera and probe each.
    """
    ...
def render_json(containers: List[Any], reports: List[Any], gpu_map: Dict[str, int], shm_artefacts: Dict[str, List[str]], gfc: Optional[int], backend_errors: Dict[str, str], rinfo: Optional[Any] = None) -> Any: ...
def render_table(containers: List[Any], reports: List[Any], gpu_map: Dict[str, int], shm_artefacts: Dict[str, List[str]], gfc: Optional[int], backend_errors: Dict[str, str], rinfo: Optional[Any] = None) -> Any: ...
def vlog(*a: Any) -> Any: ...

# Classes
class BackendClient:
    def __init__(self: Any, access_key: str, secret_key: str, base_url: str, timeout: float = 10.0) -> None: ...

    def auth(self: Any) -> str: ...

    def camera_ips(self: Any, camera_ids: List[str]) -> Dict[str, str]: ...

    def consuming_topics(self: Any, instance_id: str) -> List[dict]: ...

    def output_topics(self: Any, deployment_id: str, instance_id: str) -> List[dict]: ...

    def redis_for_instance(self: Any, instance_id: str, action_id: Optional[str] = None) -> Optional[dict]: ...

class BackendError(Exception):
    ...
class CameraReport:
    ...
class ContainerCtx:
    def public_dict(self: Any) -> dict: ...

class RedisCameraState:
    def app_ids(self: Any) -> List[str]: ...

    def newest_age_ms(self: Any) -> Optional[float]: ...

    def primary_input_stream(self: Any) -> Optional[Any]: ...

    def total_xlen(self: Any) -> int: ...

class RedisInfo:
    ...
class RedisStream:
    ...
class ShmRingInfo:
    ...
