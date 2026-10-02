"""Auto-generated stub for module: model."""
from typing import Any, List, Optional

from .osnet_ain import osnet_ain_x1_0

# Constants
EMBEDDING_DIM: int
INPUT_HEIGHT: int
INPUT_WIDTH: int
logger: Any

# Functions
def ensure_weights(url: Optional[str] = None, sha256: Optional[str] = None, local_path: Optional[str] = None, timeout: int = 300) -> Optional[str]:
    """
    Return a path to a digest-verified checkpoint, or ``None``.
    
        Resolution order: explicit ``local_path`` (or ``MATRICE_REID_MODEL_PATH``)
        -> verified cache hit -> download. A file whose digest does not match is
        never loaded and never left on disk.
    """
    ...
def get_shared_embedder(device: Optional[str] = None, fp16: bool = True, max_batch: int = 8, allow_cpu: bool = False, weights_path: Optional[str] = None) -> Optional[Any]:
    """
    Return the process-wide embedder, building it on first use.
    
        Returns ``None`` -- never raises -- when torch is missing, CUDA is absent
        and ``allow_cpu`` is false, the download fails, or a previous failure is
        still inside its backoff window.
    """
    ...
def reset_shared_state() -> None:
    """
    Drop cached models and backoff state. For tests.
    """
    ...

# Classes
class PersonEmbedder:
    # Wraps OSNet-AIN-x1.0 for batched person-crop embedding.
    #
    #     Construct via :func:`get_shared_embedder` so one process holds one model.

    def __init__(self: Any, weights_path: str, device: str = 'cuda', fp16: bool = True, max_batch: int = 8) -> None: ...

    def close(self: Any) -> None: ...

    def embed(self: Any, crops_bgr: List[Any.Any]) -> Optional[Any.Any]:
        """
        Embed up to ``max_batch`` BGR crops -> ``(n, dim)`` L2-normalised.
        """
        ...

    def preprocess(crop_bgr: Any.Any) -> Optional[Any.Any]:
        """
        BGR HxWx3 uint8 crop -> normalised CHW float32, or ``None``.
        
                Resizes to 256x128, converts BGR->RGB, scales to [0,1] and applies
                ImageNet statistics -- matching how the checkpoint was trained.
        """
        ...

