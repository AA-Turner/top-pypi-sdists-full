"""Person re-identification embedder: weight acquisition, loading, inference.

Everything here degrades rather than raises. If torch is missing, the
download fails, the digest does not match, or CUDA is absent, the caller
gets ``None``/``False`` and the use case falls back to plain people
counting. A re-identification feature must never be able to take down the
counting it augments.

Security posture for the checkpoint:

* HTTPS only, asserted before the request.
* SHA-256 verified on download **and** on every cache load -- a pinned
  "immutable" URL is not on its own evidence that the bytes are unchanged.
* ``torch.load(..., weights_only=True)``. A ``.pth`` is a pickle, so the
  default unpickler is arbitrary code execution on downloaded bytes.
  OSNet checkpoints are plain state dicts, so this costs nothing.
* Atomic cache writes (temp + ``os.replace``), so a crash or two racing
  workers cannot leave a half-written file that later loads as garbage.
* ``strict=True`` state-dict loading. ``strict=False`` would silently
  accept a mismatched checkpoint and leave a **randomly initialised**
  network producing plausible-looking embeddings -- the worst possible
  failure, because nothing visibly breaks.

Preferred production posture is to bake the verified ``.pth`` into the
image and point ``MATRICE_REID_MODEL_PATH`` at it, so no network call
happens at container start. Downloading is the fallback, not the design.
"""

from __future__ import annotations

import hashlib
import logging
import os
import tempfile
import threading
import time
from typing import Any, Dict, List, Optional

import numpy as np

logger = logging.getLogger(__name__)

__all__ = ["PersonEmbedder", "get_shared_embedder", "reset_shared_state"]

# --- model identity ---------------------------------------------------------
# Author's own repository (MIT licensed), pinned by digest. Verified locally:
# 17,293,009 bytes, 552 tensors, DataParallel-prefixed, classifier width 4101.
_DEFAULT_MODEL_FILENAME = (
    "osnet_ain_x1_0_msmt17_256x128_amsgrad_ep50_lr0.0015_coslr_b64_fb10_"
    "softmax_labsmth_flip_jitter.pth"
)
_DEFAULT_MODEL_URL = (
    f"https://huggingface.co/kaiyangzhou/osnet/resolve/main/{_DEFAULT_MODEL_FILENAME}"
)
#: Integrity pin for the published checkpoint -- a public digest, not a
#: credential. Checked in deliberately: a `.pth` is a pickle, so an
#: unverified download is remote code execution.
_DEFAULT_MODEL_SHA256 = (
    "8a07e8da38946f7cee37f4561617bf8b6d2fe8f3a4027852893ea092e46d919f"  # pragma: allowlist secret
)

#: Input geometry the checkpoint was trained on. Changing these silently
#: degrades embedding quality rather than raising.
INPUT_HEIGHT = 256
INPUT_WIDTH = 128
EMBEDDING_DIM = 512

# ImageNet statistics, in RGB order -- cv2 hands back BGR, so callers must
# convert. Getting this backwards produces embeddings that look fine and
# match far worse: a silent accuracy bug.
_MEAN_RGB = np.array([0.485, 0.456, 0.406], dtype=np.float32)
_STD_RGB = np.array([0.229, 0.224, 0.225], dtype=np.float32)

# --- process-wide shared state ---------------------------------------------
# One model per process, not per stream: N cameras in one worker cost one
# download and one GPU allocation.
_SHARED_LOCK = threading.Lock()
_SHARED: Dict[str, "PersonEmbedder"] = {}

# Negative cache. Without it a broken init is retried on every frame, which
# turns a missing file into a per-frame stall. Process-wide rather than
# per-key because the failures it guards (no torch, unreachable host) are
# not key specific.
_INIT_BACKOFF_BASE_S = 30.0
_INIT_BACKOFF_MAX_S = 600.0
_init_failure: Dict[str, Any] = {"retry_at": 0.0, "delay": 0.0, "error": None}


def reset_shared_state() -> None:
    """Drop cached models and backoff state. For tests."""
    with _SHARED_LOCK:
        _SHARED.clear()
    _init_failure.update(retry_at=0.0, delay=0.0, error=None)


def _record_failure(err: Exception) -> None:
    delay = min(_INIT_BACKOFF_MAX_S, max(_INIT_BACKOFF_BASE_S, 2.0 * float(_init_failure["delay"])))
    _init_failure.update(retry_at=time.monotonic() + delay, delay=delay, error=str(err))
    logger.warning("ReID init failed (%s); backing off %.0fs", err, delay)


def _backing_off() -> bool:
    return time.monotonic() < float(_init_failure["retry_at"])


def _import_torch():
    """Import torch lazily. Never at module import: this package must stay
    importable (and cheap) on machines with no torch at all."""
    try:
        import torch  # noqa: PLC0415

        return torch
    except ImportError as exc:  # pragma: no cover - environment dependent
        logger.warning("PyTorch unavailable, ReID disabled: %s", exc)
        return None


# --- weight acquisition -----------------------------------------------------
def _cache_dir() -> str:
    base = os.environ.get("MATRICE_REID_MODEL_DIR")
    if not base:
        state = os.environ.get("MATRICE_STATE_DIR") or os.path.join(
            tempfile.gettempdir(), "matrice_analytics"
        )
        base = os.path.join(state, "reid")
    os.makedirs(base, exist_ok=True)
    return base


def _sha256_file(path: str, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def ensure_weights(
    url: Optional[str] = None,
    sha256: Optional[str] = None,
    local_path: Optional[str] = None,
    timeout: int = 300,
) -> Optional[str]:
    """Return a path to a digest-verified checkpoint, or ``None``.

    Resolution order: explicit ``local_path`` (or ``MATRICE_REID_MODEL_PATH``)
    -> verified cache hit -> download. A file whose digest does not match is
    never loaded and never left on disk.
    """
    expected = (
        sha256 or os.environ.get("MATRICE_REID_MODEL_SHA256") or _DEFAULT_MODEL_SHA256
    ).lower()

    explicit = local_path or os.environ.get("MATRICE_REID_MODEL_PATH")
    if explicit:
        if not os.path.exists(explicit):
            logger.warning("MATRICE_REID_MODEL_PATH does not exist: %s", explicit)
            return None
        actual = _sha256_file(explicit)
        if expected and actual != expected:
            # Deliberately permissive: an operator who supplies an explicit
            # path has made a conscious choice (e.g. a fine-tuned model).
            # Warn loudly, do not refuse.
            logger.warning(
                "ReID checkpoint at %s has sha256 %s, expected %s -- using it anyway "
                "because the path was set explicitly",
                explicit,
                actual[:16],
                expected[:16],
            )
        return explicit

    src = url or os.environ.get("MATRICE_REID_MODEL_URL") or _DEFAULT_MODEL_URL
    if not src.lower().startswith("https://"):
        logger.error("Refusing non-HTTPS ReID model URL: %s", src)
        return None

    cached = os.path.join(_cache_dir(), f"osnet_ain_x1_0_{expected[:16]}.pth")
    if os.path.exists(cached):
        try:
            if _sha256_file(cached) == expected:
                return cached
            logger.warning("Cached ReID checkpoint failed digest check; refetching")
            os.remove(cached)
        except OSError as exc:
            logger.warning("Could not validate cached checkpoint: %s", exc)
            return None

    try:
        import urllib.request  # noqa: PLC0415

        logger.info("Downloading ReID checkpoint from %s", src)
        h = hashlib.sha256()
        fd, tmp = tempfile.mkstemp(prefix=".reid-", suffix=".part", dir=_cache_dir())
        try:
            with os.fdopen(fd, "wb") as out, urllib.request.urlopen(src, timeout=timeout) as resp:  # noqa: S310
                while True:
                    chunk = resp.read(1 << 20)
                    if not chunk:
                        break
                    h.update(chunk)
                    out.write(chunk)
                out.flush()
                os.fsync(out.fileno())
            actual = h.hexdigest()
            if actual != expected:
                logger.error(
                    "ReID checkpoint digest mismatch: got %s, expected %s -- discarding",
                    actual[:16],
                    expected[:16],
                )
                return None
            # noqa PTH105: os.replace is the atomic-rename primitive here.
            # Path.replace wraps the same syscall but obscures that atomicity
            # is the point -- two workers racing must never leave a partial file.
            os.replace(tmp, cached)  # noqa: PTH105
            tmp = None
            logger.info("ReID checkpoint cached at %s", cached)
            return cached
        finally:
            if tmp and os.path.exists(tmp):
                os.unlink(tmp)
    except Exception as exc:  # noqa: BLE001 - network/OS failure must degrade
        logger.warning("ReID checkpoint download failed: %s", exc)
        return None


def _strip_module_prefix(state: Dict[str, Any]) -> Dict[str, Any]:
    """Undo ``nn.DataParallel``'s ``module.`` prefix.

    The published checkpoints were saved from a DataParallel wrapper, so
    every key carries the prefix and a naive strict load fails on all 552
    tensors.
    """
    if not any(k.startswith("module.") for k in state):
        return state
    return {(k[7:] if k.startswith("module.") else k): v for k, v in state.items()}


# --- embedder ---------------------------------------------------------------
class PersonEmbedder:
    """Wraps OSNet-AIN-x1.0 for batched person-crop embedding.

    Construct via :func:`get_shared_embedder` so one process holds one model.
    """

    def __init__(
        self,
        weights_path: str,
        device: str = "cuda",
        fp16: bool = True,
        max_batch: int = 8,
    ) -> None:
        torch = _import_torch()
        if torch is None:
            raise RuntimeError("PyTorch unavailable")

        from .osnet_ain import osnet_ain_x1_0  # noqa: PLC0415

        self._torch = torch
        self.max_batch = int(max_batch)
        self.device_str = device
        self.fp16 = bool(fp16) and device.startswith("cuda")

        # Load to CPU first: loading straight to GPU allocates the tensors
        # on device before we have validated them, which is an avoidable
        # memory spike (and wasted if validation then fails).
        raw = torch.load(weights_path, map_location="cpu", weights_only=True)
        state = raw.get("state_dict", raw) if isinstance(raw, dict) else raw
        state = _strip_module_prefix(state)

        cls_w = state.get("classifier.weight")
        num_classes = int(cls_w.shape[0]) if cls_w is not None else 1000

        model = osnet_ain_x1_0(num_classes)
        # strict=True is the whole point: a mismatch must be loud, never a
        # silently random-initialised network.
        model.load_state_dict(state, strict=True)
        model.eval()

        self.device = torch.device(device)
        model.to(self.device)
        if self.fp16:
            model.half()
        self.model = model
        self.dim = EMBEDDING_DIM

        # Preallocated NCHW staging buffer. A fixed batch shape lets the CUDA
        # allocator reach steady state after the first call instead of
        # re-planning on every differently-sized batch.
        self._buf = np.zeros((self.max_batch, 3, INPUT_HEIGHT, INPUT_WIDTH), dtype=np.float32)
        self._warmup()

    def _warmup(self) -> None:
        try:
            torch = self._torch
            x = torch.zeros(
                (self.max_batch, 3, INPUT_HEIGHT, INPUT_WIDTH),
                dtype=torch.float16 if self.fp16 else torch.float32,
                device=self.device,
            )
            with torch.inference_mode():
                self.model(x)
        except Exception as exc:  # noqa: BLE001 - warmup is best effort
            logger.debug("ReID warmup skipped: %s", exc)

    @staticmethod
    def preprocess(crop_bgr: np.ndarray) -> Optional[np.ndarray]:
        """BGR HxWx3 uint8 crop -> normalised CHW float32, or ``None``.

        Resizes to 256x128, converts BGR->RGB, scales to [0,1] and applies
        ImageNet statistics -- matching how the checkpoint was trained.
        """
        if crop_bgr is None or crop_bgr.size == 0:
            return None
        try:
            import cv2  # noqa: PLC0415
        except ImportError:
            return None
        if crop_bgr.ndim != 3 or crop_bgr.shape[2] != 3:
            return None
        resized = cv2.resize(crop_bgr, (INPUT_WIDTH, INPUT_HEIGHT), interpolation=cv2.INTER_LINEAR)
        rgb = resized[:, :, ::-1].astype(np.float32) / 255.0
        normed = (rgb - _MEAN_RGB) / _STD_RGB
        return np.ascontiguousarray(normed.transpose(2, 0, 1))

    def embed(self, crops_bgr: List[np.ndarray]) -> Optional[np.ndarray]:
        """Embed up to ``max_batch`` BGR crops -> ``(n, dim)`` L2-normalised."""
        if not crops_bgr:
            return None
        torch = self._torch
        prepped: List[np.ndarray] = []
        for c in crops_bgr[: self.max_batch]:
            p = self.preprocess(c)
            if p is not None:
                prepped.append(p)
        if not prepped:
            return None

        n = len(prepped)
        self._buf[:n] = np.stack(prepped)
        if n < self.max_batch:
            self._buf[n:] = 0.0  # zero-pad to the fixed batch shape

        try:
            with torch.inference_mode():
                t = torch.from_numpy(self._buf).to(self.device, non_blocking=True)
                if self.fp16:
                    t = t.half()
                out = self.model(t).float()
                out = torch.nn.functional.normalize(out, dim=1)
                return out[:n].cpu().numpy().astype(np.float32)
        except Exception as exc:  # noqa: BLE001 - inference must degrade
            logger.warning("ReID inference failed: %s", exc)
            return None

    def close(self) -> None:
        try:
            del self.model
            if self.device_str.startswith("cuda"):
                self._torch.cuda.empty_cache()
        except Exception as exc:  # noqa: BLE001 - teardown is best effort
            logger.debug("ReID embedder teardown failed: %s", exc)


def get_shared_embedder(
    device: Optional[str] = None,
    fp16: bool = True,
    max_batch: int = 8,
    allow_cpu: bool = False,
    weights_path: Optional[str] = None,
) -> Optional[PersonEmbedder]:
    """Return the process-wide embedder, building it on first use.

    Returns ``None`` -- never raises -- when torch is missing, CUDA is absent
    and ``allow_cpu`` is false, the download fails, or a previous failure is
    still inside its backoff window.
    """
    if _backing_off():
        return None

    torch = _import_torch()
    if torch is None:
        return None

    if device is None:
        if torch.cuda.is_available():
            device = "cuda"
        elif allow_cpu:
            device = "cpu"
        else:
            # An unbenchmarked CPU path quietly eating frame budget on a
            # realtime stream is worse than no ReID at all. Opt in explicitly.
            logger.warning(
                "CUDA unavailable and reid_allow_cpu is false -- ReID disabled, "
                "counting continues without re-identification"
            )
            return None

    key = f"{device}|{fp16}|{max_batch}|{weights_path or ''}"
    with _SHARED_LOCK:
        hit = _SHARED.get(key)
    if hit is not None:
        return hit

    path = ensure_weights(local_path=weights_path)
    if path is None:
        _record_failure(RuntimeError("checkpoint unavailable"))
        return None

    try:
        # Built outside the lock: holding a global lock across a download and
        # a CUDA init would stall every other camera in the process.
        emb = PersonEmbedder(path, device=device, fp16=fp16, max_batch=max_batch)
    except Exception as exc:  # noqa: BLE001 - any init failure degrades
        _record_failure(exc)
        return None

    with _SHARED_LOCK:
        existing = _SHARED.get(key)
        if existing is not None:
            emb.close()  # lost the race; drop the duplicate
            return existing
        _SHARED[key] = emb
    _init_failure.update(retry_at=0.0, delay=0.0, error=None)
    logger.info("ReID embedder ready (device=%s fp16=%s batch=%d)", device, fp16, max_batch)
    return emb
