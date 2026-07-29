"""Auto-generated stub for module: device_topology."""
from typing import Any

# Constants
logger: Any
topology: Any

# Classes
class MachineTopology:
    # Process-wide cache of GPU count, peer-access capability, and which
    #     (consumer, producer) peer links have already been enabled. Thread-safe and
    #     idempotent — safe to call enable_peer() on every connect.

    def __init__(self: Any) -> None: ...

    def can_access_peer(self: Any, local_gpu: int, producer_gpu: int) -> bool:
        """
        True if local_gpu can directly read producer_gpu's memory (NVLink/
                PCIe P2P). Same device is trivially True. Result is cached.
        """
        ...

    def device_count(self: Any) -> int: ...

    def enable_peer(self: Any, local_gpu: int, producer_gpu: int) -> bool:
        """
        Idempotently enable local_gpu -> producer_gpu peer access.
        
                Returns True when frames on producer_gpu are reachable from local_gpu
                (same GPU, or NVLink/PCIe P2P successfully enabled).
        
                Returns False when local_gpu != producer_gpu and no peer path exists
                (a multi-GPU host without NVLink/P2P). This is **terminal** for
                cross-GPU consume — there is no transparent host-bounce fallback (the
                CUDA-IPC handle itself can't be opened for another device's memory
                without P2P). consumer_auto turns False into a PeerUnavailableError;
                the operator's remedy is to co-locate inference on the producer's GPU.
                Single-GPU hosts (Orin/Thor) never reach this (producer_gpu == local).
        """
        ...

    def has_full_p2p(self: Any, device_ids: Any = None) -> bool:
        """
        True if every ordered pair among device_ids can peer-access (full P2P/
                NVLink mesh). Used by the SG to decide whether cross-GPU consume is viable
                and by consumer_auto to pick a transport. Same-device pairs are trivially
                OK; a single GPU is trivially a full mesh.
        """
        ...

