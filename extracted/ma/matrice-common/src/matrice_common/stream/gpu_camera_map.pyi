"""Auto-generated stub for module: gpu_camera_map."""
from typing import Any, Dict, List, Optional, Set

# Constants
MAP_SHARED: Any
NOT_INITIALIZED_MSG: str
PROT_READ: Any
PROT_WRITE: Any
SHM_BASE_PATH: Any
logger: Any

# Functions
def get_gpu_camera_map(is_producer: bool = False) -> Any:
    """
    Get or create the global GpuCameraMap instance.
    
        Args:
            is_producer: True if this is the producer process
    
        Returns:
            GpuCameraMap instance (may not be initialized)
    """
    ...

# Classes
class GpuCameraMap:
    # Shared memory store for camera_id -> gpu_id mapping.
    #
    #     Uses a simple JSON format stored in shared memory with a size header.
    #     Thread-safe via file locking for writes.
    #
    #     Format in shared memory:
    #     - 4 bytes: uint32 size of JSON data
    #     - N bytes: JSON string {"camera_id": gpu_id, ...}

    def __init__(self: Any, is_producer: bool = True) -> None:
        """
        Initialize the GPU camera map.
        
                Args:
                    is_producer: True if this process creates/writes the mapping,
                                False if this process only reads.
        """
        ...

    MAX_SIZE: Any
    SHM_PATH: Any

    def check_file_recreated(self: Any) -> bool:
        """
        Return True if the SHM file's on-disk inode no longer matches our open fd.
        
                When the SHM file is unlinked + recreated (SG restart with external cleanup,
                operator `rm -f /dev/shm/gpu_camera_map`, or `docker rm` on the SG container),
                the open fd keeps pointing at the deleted inode while a new inode appears at
                the same path. Comparing os.fstat(fd).st_ino vs os.stat(path).st_ino detects
                this. Mirrors CudaShmRingBuffer.check_file_recreated().
        
                Returns:
                    True if file was recreated (stale) or missing, False if still the same file.
        """
        ...

    def close(self: Any) -> None:
        """
        Close the shared memory mapping.
        
                Producer should call this during cleanup.
        """
        ...

    def connect(self: Any) -> bool:
        """
        Connect to existing shared memory.
        
                For producers: opens with read-write access to allow writing mappings.
                For consumers: opens with read-only access.
        
                Returns:
                    True if successful, False otherwise.
        """
        ...

    def get_all_mappings(self: Any) -> Dict[str, int]:
        """
        Get all camera-to-GPU mappings.
        
                Returns:
                    Dict of camera_id -> gpu_id
        """
        ...

    def get_cameras_for_gpu(self: Any, gpu_id: int) -> List[str]:
        """
        Get all camera IDs assigned to a specific GPU.
        
                Args:
                    gpu_id: GPU ID to filter by
        
                Returns:
                    List of camera IDs assigned to this GPU
        """
        ...

    def get_gpu_id(self: Any, camera_id: str) -> Optional[int]:
        """
        Get GPU ID for a camera (consumer).
        
                Args:
                    camera_id: Camera identifier
        
                Returns:
                    GPU ID if found, None otherwise.
        """
        ...

    def initialize(self: Any) -> bool:
        """
        Initialize as producer - create shared memory.
        
                Creates the shared memory file and initializes with empty mapping.
                Should be called by the streaming gateway before creating ring buffers.
        
                Returns:
                    True if successful, False otherwise.
        """
        ...

    def reconnect(self: Any) -> bool:
        """
        Close the stale mmap+fd and re-open the current SHM file by path.
        
                Idempotent: safe to call even when not connected. Returns True on success,
                False when the file is missing (caller should retry later).
        """
        ...

    def remove_mapping(self: Any, camera_id: str) -> None:
        """
        Remove a single camera from the map (producer only).
        
                Thread-safe via file locking.
        
                Args:
                    camera_id: Camera identifier to remove
        """
        ...

    def replace_all_mappings(self: Any, mappings: Dict[str, int]) -> None:
        """
        Replace the entire map with the given mappings (producer only).
        
                Unlike set_bulk_mapping() which merges, this does a full atomic replace.
                Removed cameras will no longer appear in the map.
        
                Args:
                    mappings: Complete dict of camera_id -> gpu_id
        """
        ...

    def set_bulk_mapping(self: Any, mappings: Dict[str, int]) -> None:
        """
        Set multiple GPU assignments at once (producer only).
        
                More efficient than multiple set_mapping() calls.
                Uses exclusive lock around the entire read-modify-write cycle
                to prevent race conditions when multiple processes write concurrently.
        
                Args:
                    mappings: Dict of camera_id -> gpu_id
        """
        ...

    def set_mapping(self: Any, camera_id: str, gpu_id: int) -> None:
        """
        Set GPU assignment for a camera (producer only).
        
                Thread-safe via file locking.
        
                Args:
                    camera_id: Camera identifier
                    gpu_id: GPU ID to assign this camera to
        """
        ...

