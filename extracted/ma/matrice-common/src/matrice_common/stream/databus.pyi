"""Auto-generated stub for module: databus."""
from typing import Any, Dict, Optional, Tuple, Union

from .cuda_shm_ring_buffer import CudaIpcRingBuffer
from .cuda_shm_ring_buffer import CudaIpcRingBuffer
from .shm_ring_buffer import ShmRingBuffer
from .shm_ring_buffer import ShmRingBuffer
from .shm_ring_buffer import ShmRingBuffer
from .shm_ring_buffer import ShmRingBuffer

# Constants
SHM_BASE_PATH: Any
logger: Any

# Classes
class DataBus:
    # Unified data transport — all methods are static, no state held.

    def compute_address(camera_id: str, node_id: str, port_name: str) -> str:
        """
        Compute deterministic SHM path. Pure function, no I/O.
        """
        ...

    def consumer(camera_id: str, node_id: str, port_name: str, format: Union[str, Any], consumer_key: str = 'default') -> 'Any':
        """
        Create a consumer at the deterministic address.
        
                Auto-detects the transport the producer used (CUDA IPC vs POSIX SHM)
                and handles format conversion transparently. The consumer always gets
                data in the requested format regardless of how the producer wrote it.
        
                Args:
                    camera_id: Camera identifier
                    node_id: Node identifier
                    port_name: Port name
                    format: Desired data format — auto-converts if producer format differs
                    consumer_key: Consumer group ID (independent cursor per key)
                    gpu_id: GPU device ID (for cupy/torch formats)
        """
        ...

    def producer(camera_id: str, node_id: str, port_name: str, format: Union[str, Any]) -> 'Any':
        """
        Create a producer at the deterministic address.
        
                Args:
                    camera_id: Camera identifier
                    node_id: Node identifier (e.g., "sg", "yolo", "output")
                    port_name: Output port name (e.g., "frames", "detection0")
                    format: Data format — determines transport auto-selection
                    gpu_id: GPU device ID (for cupy/torch formats)
                    num_slots: Ring buffer slot count
                    max_msg_size: Max message size in bytes (for json/bytes/numpy formats)
                    width: Frame width (for cupy format, NV12: actual pixel width)
                    height: Frame height (for cupy format, NV12: H*1.5)
        """
        ...

class DataBusConsumer:
    # Consumes data from a DataBus channel.
    #
    #     Wraps CudaIpcRingBuffer (for cupy/torch) or ShmRingBuffer (for json/bytes/numpy).

    def __init__(self: Any, address: str, fmt: Any, transport: str, consumer_key: str = 'default', gpu_id: int = 0) -> None: ...

    def ack(self: Any, frame_idx: int) -> Any:
        """
        Acknowledge consumption up to frame_idx.
        
                For CUDA IPC: updates per-consumer cursor in SHM.
                For POSIX SHM: updates local tracking only.
        """
        ...

    def address(self: Any) -> str: ...

    def close(self: Any) -> Any:
        """
        Close and cleanup.
        """
        ...

    def connected(self: Any) -> bool: ...

    def consume(self: Any) -> Tuple[Optional[Any], Optional[Dict]]:
        """
        Read next unread message.
        
                Returns:
                    (data, metadata) or (None, None) if no new data.
                    For cupy: data is a GPU array view (must stay alive during use)
                    For json: data is a dict/list
                    For bytes: data is bytes
                    For numpy: data is np.ndarray (1D uint8, caller reshapes)
        """
        ...

    def consume_latest(self: Any) -> Tuple[Optional[Any], Optional[Dict]]:
        """
        Read the latest available message, skipping all intermediate frames.
        
                Use this instead of consume() when the consumer is slower than the
                producer and you want overlays to stay in sync with the live video
                (e.g., ML inference at 10 FPS reading from a 30 FPS stream).
        
                Returns:
                    (data, metadata) or (None, None) if no new data.
                    metadata includes 'was_skipped' (bool) indicating if frames were dropped.
        """
        ...

    def is_stale(self: Any) -> bool:
        """
        Check if the underlying ring buffer's SHM file has been recreated.
        
                This indicates the producer restarted and our connection points to
                stale data. Caller should close this consumer and create a new one.
        
                Returns:
                    True if stale (producer restarted), False if still valid.
        """
        ...

    def rb(self: Any) -> Any:
        """
        Access the underlying ring buffer for advanced operations.
        """
        ...

class DataBusProducer:
    # Produces data to a DataBus channel.
    #
    #     Wraps CudaIpcRingBuffer (for cupy/torch) or ShmRingBuffer (for json/bytes/numpy).

    def __init__(self: Any, address: str, fmt: Any, transport: str, camera_id: str = '', **config: Any) -> None: ...

    def close(self: Any) -> Any:
        """
        Close and cleanup underlying ring buffer.
        """
        ...

    def publish(self: Any, data: Any, metadata: Optional[Dict] = None) -> int:
        """
        Publish data with optional metadata. Returns frame_idx.
        
                For cupy/torch: data is a GPU array, metadata keys used:
                    timestamp_ns, rtp_timestamp
                For json: data is a dict/list, serialized with orjson
                For bytes: data is bytes
                For numpy: data is a numpy array, serialized with tobytes()
        """
        ...

    def rb(self: Any) -> Any:
        """
        Access the underlying ring buffer for advanced operations.
        """
        ...

class DataFormat:
    # Data format declaration — determines transport auto-selection.

    BYTES: str
    CUPY: str
    JSON: str
    NUMPY: str
    TORCH: str

