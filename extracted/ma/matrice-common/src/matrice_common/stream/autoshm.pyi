"""Auto-generated stub for module: autoshm."""
from typing import Any, Optional

from .cuda_shm_ring_buffer import CUPY_AVAILABLE, MAP_SHARED, PROT_READ, CudaIpcRingBuffer, _cvd_remap, cp, np
from .databus import DataBus, DataFormat, _parse_format
from .device_topology import topology

# Constants
logger: Any

# Functions
def consumer_auto(camera_id: str, node_id: str = 'sg', port_name: str = 'frames', fmt: Any = 'cupy', consumer_key: str = 'inference', local_gpu_id: Optional[int] = None, max_retries: int = 10, retry_delay: float = 0.5) -> Any:
    """
    Connect a consumer that reads ``camera_id`` on ``local_gpu_id`` no matter
        which GPU the producer decoded on. Resolves the producer GPU from the header,
        enables peer access, and peer-copies frames into local memory.
    
        local_gpu_id=None means "the current cupy device" (the worker's inference GPU).
    """
    ...
def resolve_decode_gpu(camera_id: str, node_id: str = 'sg', port_name: str = 'frames', max_retries: int = 10, retry_delay: float = 0.5) -> int:
    """
    Return the GPU the producer decoded this camera on, read from the ring-
        buffer header. CO-LOCATION (the supported cross-GPU strategy): the caller
        runs this camera's inference on the returned GPU so consume is zero-copy and
        no NVLink/P2P is needed. Retries while the producer is still initializing.
    """
    ...

# Classes
class AutoConsumer:
    # Drop-in for the connector's use of a DataBus consumer: exposes ``.rb``
    #     (a PeerReadRingBuffer or HostBounceRingBuffer) and ``.close()``.

    def __init__(self: Any, rb: Any) -> None: ...

    def close(self: Any) -> None: ...

    def is_stale(self: Any) -> bool: ...

    def rb(self: Any) -> Any: ...

class HostBounceRingBuffer:
    # LAST-RESORT cross-GPU consumer for hosts WITHOUT NVLink/P2P.
    #
    #     Why this exists / when it runs
    #     ------------------------------
    #     A CUDA-IPC handle can only be opened on the producer's OWN device, so a
    #     consumer on GPU Y cannot map a producer's GPU-X memory without P2P. This
    #     class connects on the PRODUCER GPU (same-device IPC -> always legal) and
    #     bounces every frame DtoH -> pinned host -> HtoD to the local inference GPU.
    #
    #     This is a PCIe round trip per frame (~250 us @1080p NV12 with pinned host
    #     memory) and consumes PCIe bandwidth + a pinned host buffer per camera. It is
    #     a SAFETY NET ONLY: the supported path is CO-LOCATION (consume each camera on
    #     its decode GPU via resolve_decode_gpu()). It is OFF by default and only used
    #     when MATRICE_XGPU_FALLBACK=host_stage. It emits a throttled WARNING every
    #     MATRICE_XGPU_WARN_EVERY_SEC so the degradation is never silent.
    #
    #     Precondition: the consumer process must see BOTH GPUs (do NOT pin
    #     CUDA_VISIBLE_DEVICES to a single device, or the producer GPU can't be mapped).

    def __init__(self: Any, camera_id: str, local_gpu_id: int, num_slots: int, width: int, height: int, channels: int) -> None: ...

    def read_frame(self: Any, slot: Any) -> Any: ...

    def read_latest(self: Any) -> Any: ...

    def read_next(self: Any) -> Any: ...

class PeerReadRingBuffer:
    # A consumer ring buffer that may attach to a producer on a DIFFERENT GPU.
    #
    #     Reads return frames copied to the local device (one peer copy over NVLink)
    #     when the producer is on another GPU, and identical zero-copy views when the
    #     producer is on the same GPU.

    def __init__(self: Any, camera_id: str, gpu_id: int, num_slots: int, width: int, height: int, channels: int, is_producer: bool = False) -> None: ...

    def read_frame(self: Any, slot: int) -> Any: ...

    def read_latest(self: Any) -> Any: ...

    def read_next(self: Any) -> Any: ...

class PeerUnavailableError(Exception):
    # Cross-GPU consume requested but no P2P/NVLink path exists (terminal — the
    #     caller must run inference on the producer's GPU on this host).

    ...
