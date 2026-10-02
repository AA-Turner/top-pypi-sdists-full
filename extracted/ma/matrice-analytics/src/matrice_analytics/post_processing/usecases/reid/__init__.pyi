"""Stub file for post_processing.usecases.reid directory."""
from typing import Any, Callable, Dict, List, Optional, Set

from .osnet_ain import osnet_ain_x1_0

# Constants
EMBEDDING_DIM: int = ...  # From model
INPUT_HEIGHT: int = ...  # From model
INPUT_WIDTH: int = ...  # From model
logger: Any = ...  # From model
OSNET_AIN_X1_0_FEATURE_DIM: int = ...  # From osnet_ain
logger: Any = ...  # From worker

# Functions
# From gallery
def l2_normalize(v: Any.Any) -> Any.Any:
    """
    Return ``v`` scaled to unit L2 norm; a zero vector is returned as-is.
    """
    ...

# From model
def ensure_weights(url: Optional[str] = None, sha256: Optional[str] = None, local_path: Optional[str] = None, timeout: int = 300) -> Optional[str]:
    """
    Return a path to a digest-verified checkpoint, or ``None``.
    
        Resolution order: explicit ``local_path`` (or ``MATRICE_REID_MODEL_PATH``)
        -> verified cache hit -> download. A file whose digest does not match is
        never loaded and never left on disk.
    """
    ...

# From model
def get_shared_embedder(device: Optional[str] = None, fp16: bool = True, max_batch: int = 8, allow_cpu: bool = False, weights_path: Optional[str] = None) -> Optional[Any]:
    """
    Return the process-wide embedder, building it on first use.
    
        Returns ``None`` -- never raises -- when torch is missing, CUDA is absent
        and ``allow_cpu`` is false, the download fails, or a previous failure is
        still inside its backoff window.
    """
    ...

# From model
def reset_shared_state() -> None:
    """
    Drop cached models and backoff state. For tests.
    """
    ...

# From osnet_ain
def osnet_ain_x1_0(num_classes: int = 1000, **kwargs: Any) -> Any:
    """
    OSNet-AIN x1.0 -- ~2.2M params, ~0.98 GFLOPs at 256x128, 512-d output.
    
        ``num_classes`` only sizes the (inference-unused) classifier head, but it
        must match the checkpoint for ``strict=True`` loading. Verified against
        the author's published MSMT17 checkpoint: **4101 identities**. Callers
        should read the width from ``classifier.weight`` rather than hardcoding
        it -- see ``model.load_reid_model``.
    """
    ...

# Classes
# From gallery
class GalleryMatch:
    # Outcome of a gallery query.

    ...

# From gallery
class ReIDGallery:
    # The ``capacity`` most recently seen person embeddings, for one stream.
    #
    #     Not internally locked: a single instance belongs to one use-case instance
    #     (one stream), and every mutation happens on the frame path. The worker
    #     thread never touches this object -- it returns embeddings, and the frame
    #     path does the matching. That keeps the concurrency story trivial.

    def __init__(self: Any, dim: int, capacity: int = 100, match_threshold: float = 0.67, margin: float = 0.06, min_absence_s: float = 3.0) -> None: ...

    def clear(self: Any) -> None: ...

    def insert(self: Any, canonical_id: str, embedding: Any.Any, now: float) -> None:
        """
        Add or overwrite ``canonical_id``'s prototype.
        """
        ...

    def match(self: Any, query: Any.Any, now: float, exclude_ids: Optional[Set[str]] = None, require_absence: bool = True) -> Optional[Any]:
        """
        Best identity for ``query``, or ``None`` when nothing is safe enough.
        
                Applies, in order: the live-elsewhere mask (a person cannot be in two
                places at once), the minimum-absence gate, the absolute threshold and
                the ratio test. Every one of these can only reject.
        
                ``require_absence=False`` drops the minimum-absence gate. That gate
                exists to stop a tracked person being re-matched to themselves during
                a momentary dropout, and it is correct whenever a tracker supplies
                continuity across frames. When the caller has no tracker -- ids that
                are unique per frame -- appearance is the *only* continuity, so a
                person visible right now must be matchable to the entry made for them
                a frame ago. Keeping the gate there rejects every match and mints a
                fresh identity per frame. The live-elsewhere mask still prevents two
                simultaneous detections collapsing into one identity.
        """
        ...

    def similarity(self: Any, canonical_id: str, embedding: Any.Any) -> Optional[float]:
        """
        Cosine similarity of ``embedding`` against a stored prototype.
        
                ``None`` when the identity is not held (it may have been evicted by
                newer traffic) or the dimensions disagree.
        """
        ...

    def size(self: Any) -> int:
        """
        Identities currently retained. Never exceeds ``capacity``.
        """
        ...

    def stats(self: Any) -> Dict[str, Any]: ...

    def touch(self: Any, canonical_id: str, now: float) -> None:
        """
        Mark an identity as seen, so eviction reclaims someone else first.
        
                This is what makes the bound *recency*-based rather than
                insertion-order-based: a person who keeps being seen keeps their row
                however many others pass through.
        """
        ...

    def update_prototype(self: Any, canonical_id: str, embedding: Any.Any, now: float, weight: float = 0.3) -> None:
        """
        Blend a fresh observation into an existing prototype.
        
                ``weight`` is capped so a single long sighting cannot dominate an
                identity's stored appearance. A ``weight`` of 0 is a pure touch --
                it refreshes recency without letting a doubtful crop move the
                prototype at all.
        """
        ...


# From model
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


# From osnet_ain
class ChannelGate:
    # Mini-network generating channel-wise gates conditioned on the input.

    def __init__(self: Any, in_channels: int, num_gates: int | None = None, return_gates: bool = False, gate_activation: str = 'sigmoid', reduction: int = 16, layer_norm: bool = False) -> None: ...

    def forward(self: Any, x: Any) -> Any: ...


# From osnet_ain
class Conv1x1:
    # 1x1 convolution + bn + relu.

    def __init__(self: Any, in_channels: int, out_channels: int, stride: int = 1, groups: int = 1) -> None: ...

    def forward(self: Any, x: Any) -> Any: ...


# From osnet_ain
class Conv1x1Linear:
    # 1x1 convolution + bn (without non-linearity).

    def __init__(self: Any, in_channels: int, out_channels: int, stride: int = 1, bn: bool = True) -> None: ...

    def forward(self: Any, x: Any) -> Any: ...


# From osnet_ain
class ConvLayer:
    # Convolution layer (conv + bn + relu).

    def __init__(self: Any, in_channels: int, out_channels: int, kernel_size: int, stride: int = 1, padding: int = 0, groups: int = 1, IN: bool = False) -> None: ...

    def forward(self: Any, x: Any) -> Any: ...


# From osnet_ain
class LightConv3x3:
    # Lightweight 3x3 convolution: 1x1 (linear) + depthwise 3x3 (nonlinear).

    def __init__(self: Any, in_channels: int, out_channels: int) -> None: ...

    def forward(self: Any, x: Any) -> Any: ...


# From osnet_ain
class LightConvStream:
    # Lightweight convolution stream (``depth`` stacked ``LightConv3x3``).

    def __init__(self: Any, in_channels: int, out_channels: int, depth: int) -> None: ...

    def forward(self: Any, x: Any) -> Any: ...


# From osnet_ain
class OSBlock:
    # Omni-scale feature learning block.

    def __init__(self: Any, in_channels: int, out_channels: int, reduction: int = 4, T: int = 4, **kwargs: Any) -> None: ...

    def forward(self: Any, x: Any) -> Any: ...


# From osnet_ain
class OSBlockINin:
    # Omni-scale feature learning block with instance normalization.

    def __init__(self: Any, in_channels: int, out_channels: int, reduction: int = 4, T: int = 4, **kwargs: Any) -> None: ...

    def forward(self: Any, x: Any) -> Any: ...


# From osnet_ain
class OSNet:
    # Omni-Scale Network.
    #
    #     In ``eval()`` mode ``forward`` returns the ``feature_dim``-wide embedding
    #     (the classifier head is skipped), which is exactly what re-identification
    #     needs. Keep the module in ``eval()``.

    def __init__(self: Any, num_classes: int, blocks: Any, layers: Any, channels: Any, feature_dim: int = 512, conv1_IN: bool = False, **kwargs: Any) -> None: ...

    def featuremaps(self: Any, x: Any) -> Any: ...

    def forward(self: Any, x: Any) -> Any: ...


# From worker
class EmbedWorker:
    # Single daemon thread turning person crops into embeddings.
    #
    #     One worker per use-case instance (i.e. per stream). The embedder it
    #     calls is process-wide and shared, so N streams still cost one model.

    def __init__(self: Any, embed_fn: Callable[[List[Any.Any]], Optional[Any.Any]], max_pending: int = 64, batch_size: int = 8, idle_sleep_s: float = 0.002, name: str = 'reid-embed') -> None: ...

    def alive(self: Any) -> bool: ...

    def forget(self: Any, track_ids: Any) -> None:
        """
        Drop state for tracks the caller no longer cares about.
        """
        ...

    def get_result(self: Any, track_id: Any) -> Optional[Any.Any]: ...

    def has_pending(self: Any, track_id: Any) -> bool: ...

    def offer(self: Any, track_id: Any, crop: Any.Any) -> str:
        """
        Queue ``crop`` for ``track_id``. Never blocks. Returns a disposition.
        """
        ...

    def pop_result(self: Any, track_id: Any) -> Optional[Any.Any]: ...

    def starving(self: Any, grace_s: float = 2.0) -> bool:
        """
        True when work has been queued for ``grace_s`` with nothing completed.
        
                The frame path calls the use case synchronously, and torch inference
                holds the GIL in bursts, so a caller that never yields between frames
                can starve this thread. Frame-count budgets do not help there: the
                frames tick by while no wall-clock time is given to the worker. This
                is the wall-clock escape hatch -- the caller releases deferred tracks
                under their raw ids rather than holding a count hostage.
        """
        ...

    def stats(self: Any) -> Dict[str, Any]: ...

    def stop(self: Any, timeout: float = 2.0) -> None: ...


from . import gallery, model, osnet_ain, worker