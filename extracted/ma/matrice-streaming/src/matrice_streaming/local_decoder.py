"""Notebook-friendly local frame decoder for debugging the streaming pipeline.

No SHM, no ring buffers, no multiprocessing. Just decode frames and inspect them.

Usage:
    from matrice_streaming.local_decoder import LocalDecoder

    with LocalDecoder("videoplayback.mp4", gpu_id=4) as dec:
        # Raw NV12 (same as what goes into CUDA SHM ring buffer)
        nv12 = dec.read_frame()  # CuPy (H*1.5, W, 1) uint8

        # Preprocessed (same as what the inference model sees)
        dec.reset()
        pre = dec.read_preprocessed_frame(640, 640)  # numpy (3, 640, 640) float32 [0,1]

        # BGR for OpenCV / matplotlib display
        dec.reset()
        bgr = dec.read_bgr()  # numpy (H, W, 3) uint8
"""

from __future__ import annotations

from typing import Generator, Optional

import numpy as np

try:
    import cupy as cp
except ImportError as exc:
    raise ImportError("CuPy is required: pip install cupy-cuda12x") from exc

try:
    import PyNvVideoCodec as nvc
except ImportError as exc:
    raise ImportError("PyNvVideoCodec is required for hardware decoding") from exc

try:
    import cv2
except ImportError:
    cv2 = None

from matrice_streaming.streaming_gateway.camera_streamer.codec_detect import (
    normalize_codec,
)
from matrice_streaming.streaming_gateway.camera_streamer.nvdec.nvdec import (
    VideoDownloader,
    surface_to_nv12,
)

_CODEC_MAP = {"h264": "H264", "h265": "HEVC"}


class LocalDecoder:
    """Simple NVDEC decoder for local testing. No SHM, no multiprocessing."""

    def __init__(
        self,
        source: str,
        gpu_id: int = 0,
        codec: str = "h264",
        width: int = 0,
        height: int = 0,
    ):
        """
        Args:
            source: Video file path, RTSP URL, or HTTPS URL.
            gpu_id: GPU device index.
            codec: "h264" or "h265" (also accepts aliases like "hevc").
            width: Output width. 0 = native camera resolution.
            height: Output height. 0 = native camera resolution.
        """
        self._gpu_id = gpu_id
        self._target_w = width
        self._target_h = height
        self._frame_count = 0
        self._resolved_w = 0
        self._resolved_h = 0

        cp.cuda.Device(gpu_id).use()

        codec = normalize_codec(codec)
        codec_name = _CODEC_MAP.get(codec, "H264")
        nvc_codec = getattr(nvc.cudaVideoCodec, codec_name, nvc.cudaVideoCodec.H264)

        # Handle HTTPS URLs (PyNvVideoCodec lacks HTTPS support)
        downloader = VideoDownloader()
        self._source = downloader.prepare_source(source, camera_id="local_test")

        self._demuxer = nvc.CreateDemuxer(self._source)
        self._decoder = nvc.CreateDecoder(
            gpuid=gpu_id,
            codec=nvc_codec,
            usedevicememory=True,
        )

        # Extract FPS
        try:
            fr = self._demuxer.FrameRate()
            self._fps = float(fr) if fr and float(fr) > 0 else 30.0
        except Exception:
            self._fps = 30.0

        # Pending surfaces from current packet (decoder can yield multiple)
        self._pending_surfaces = iter([])

    # ------------------------------------------------------------------
    # Core read methods
    # ------------------------------------------------------------------

    def read_frame(self) -> Optional[cp.ndarray]:
        """Decode next frame as NV12 CuPy array.

        Returns (H*1.5, W, 1) uint8 on GPU, or None at EOF.
        This is the exact format written to the CUDA SHM ring buffer in production.
        """
        while True:
            # Drain pending surfaces from previous packet
            for surface in self._pending_surfaces:
                tensor = surface_to_nv12(surface, self._target_h, self._target_w)
                if tensor is not None:
                    self._frame_count += 1
                    self._update_dims(tensor)
                    return tensor

            # Get next packet
            packet = self._demuxer.Demux()
            if packet is None:
                return None  # EOF

            self._pending_surfaces = self._decoder.Decode(packet)

    def read_preprocessed_frame(
        self,
        model_w: int = 640,
        model_h: int = 640,
    ) -> Optional[np.ndarray]:
        """Decode and preprocess: NV12 -> RGB (BT.601) -> resize -> CHW -> [0,1].

        Returns numpy (3, model_h, model_w) float32, matching the production
        CUDA kernel output in gpu_kernels.py. Returns None at EOF.
        """
        nv12 = self.read_frame()
        if nv12 is None:
            return None
        return self._nv12_to_rgb_chw(nv12, model_w, model_h)

    def read_bgr(self, width: int = 0, height: int = 0) -> Optional[np.ndarray]:
        """Decode and convert to BGR uint8 HWC for OpenCV / matplotlib.

        Args:
            width: Output width. 0 = use decoder's target resolution.
            height: Output height. 0 = use decoder's target resolution.

        Returns numpy (H, W, 3) uint8 BGR, or None at EOF.
        """
        nv12 = self.read_frame()
        if nv12 is None:
            return None
        rgb = self._nv12_to_rgb_hwc(nv12)
        bgr = rgb[:, :, ::-1].copy()

        if width > 0 and height > 0 and cv2 is not None:
            bgr = cv2.resize(bgr, (width, height), interpolation=cv2.INTER_LINEAR)
        return bgr

    # ------------------------------------------------------------------
    # Generators
    # ------------------------------------------------------------------

    def frames(self, limit: int = 0) -> Generator[cp.ndarray, None, None]:
        """Yield NV12 frames. limit=0 means all frames until EOF."""
        count = 0
        while limit == 0 or count < limit:
            frame = self.read_frame()
            if frame is None:
                break
            yield frame
            count += 1

    def preprocessed_frames(
        self,
        model_w: int = 640,
        model_h: int = 640,
        limit: int = 0,
    ) -> Generator[np.ndarray, None, None]:
        """Yield preprocessed frames. limit=0 means all."""
        count = 0
        while limit == 0 or count < limit:
            frame = self.read_preprocessed_frame(model_w, model_h)
            if frame is None:
                break
            yield frame
            count += 1

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def reset(self):
        """Reset to beginning of video (recreates demuxer)."""
        self._demuxer = nvc.CreateDemuxer(self._source)
        self._pending_surfaces = iter([])
        self._frame_count = 0

    def close(self):
        """Release resources."""
        self._demuxer = None
        self._decoder = None
        self._pending_surfaces = iter([])

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __iter__(self):
        return self.frames()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def width(self) -> int:
        """Frame width (resolved after first decode if using native resolution)."""
        return self._resolved_w or self._target_w

    @property
    def height(self) -> int:
        """Frame height (resolved after first decode if using native resolution)."""
        return self._resolved_h or self._target_h

    @property
    def fps(self) -> float:
        return self._fps

    @property
    def frame_count(self) -> int:
        return self._frame_count

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _update_dims(self, nv12: cp.ndarray):
        """Resolve actual dimensions from first decoded frame."""
        if self._resolved_h == 0:
            nv12_h, w, _ = nv12.shape
            self._resolved_h = nv12_h * 2 // 3
            self._resolved_w = w

    def _nv12_to_rgb_chw(self, nv12: cp.ndarray, model_w: int, model_h: int) -> np.ndarray:
        """NV12 -> RGB CHW float32 [0,1], matching production BT.601 kernel.

        Uses numpy (CPU) to avoid CuPy NVRTC compilation issues in containers
        without full CUDA toolkit headers.
        """
        nv12_np = cp.asnumpy(nv12[:, :, 0])  # (H*1.5, W) uint8 on CPU
        total_h, W = nv12_np.shape
        H = total_h * 2 // 3

        y_plane = nv12_np[:H, :].astype(np.float32)
        uv_plane = nv12_np[H:, :].astype(np.float32)

        # Nearest-neighbor upsample UV (matching production kernel)
        U = np.repeat(np.repeat(uv_plane[:, 0::2], 2, axis=1), 2, axis=0)[:H, :W] - 128.0
        V = np.repeat(np.repeat(uv_plane[:, 1::2], 2, axis=1), 2, axis=0)[:H, :W] - 128.0

        # BT.601 YUV -> RGB (exact coefficients from gpu_kernels.py)
        R = np.clip(y_plane + 1.402 * V, 0, 255) / 255.0
        G = np.clip(y_plane - 0.344 * U - 0.714 * V, 0, 255) / 255.0
        B = np.clip(y_plane + 1.772 * U, 0, 255) / 255.0

        rgb_chw = np.stack([R, G, B], axis=0)  # (3, H, W)

        # Letterbox resize to model dims if needed (preserves aspect ratio)
        if model_h != H or model_w != W:
            rgb_hwc = rgb_chw.transpose(1, 2, 0)  # (H, W, 3)
            r = min(model_w / W, model_h / H)
            new_w, new_h = int(round(W * r)), int(round(H * r))
            if cv2 is not None:
                resized = cv2.resize(rgb_hwc, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
            else:
                row_idx = (np.arange(new_h) * H // new_h).astype(int)
                col_idx = (np.arange(new_w) * W // new_w).astype(int)
                resized = rgb_hwc[np.ix_(row_idx, col_idx)]
            # Pad with gray (114/255) to match ultralytics LetterBox
            canvas = np.full((model_h, model_w, 3), 114.0 / 255.0, dtype=np.float32)
            pad_top = int(round((model_h - new_h) / 2 - 0.1))
            pad_left = int(round((model_w - new_w) / 2 - 0.1))
            canvas[pad_top : pad_top + new_h, pad_left : pad_left + new_w] = resized
            return canvas.transpose(2, 0, 1).astype(np.float32)
        return rgb_chw.astype(np.float32)

    def _nv12_to_rgb_hwc(self, nv12: cp.ndarray) -> np.ndarray:
        """NV12 -> RGB HWC uint8 (no resize, no normalize)."""
        nv12_np = cp.asnumpy(nv12[:, :, 0])  # CPU
        total_h, W = nv12_np.shape
        H = total_h * 2 // 3

        y_plane = nv12_np[:H, :].astype(np.float32)
        uv_plane = nv12_np[H:, :].astype(np.float32)

        U = np.repeat(np.repeat(uv_plane[:, 0::2], 2, axis=1), 2, axis=0)[:H, :W] - 128.0
        V = np.repeat(np.repeat(uv_plane[:, 1::2], 2, axis=1), 2, axis=0)[:H, :W] - 128.0

        R = np.clip(y_plane + 1.402 * V, 0, 255)
        G = np.clip(y_plane - 0.344 * U - 0.714 * V, 0, 255)
        B = np.clip(y_plane + 1.772 * U, 0, 255)

        rgb_hwc = np.stack([R, G, B], axis=2).astype(np.uint8)  # (H, W, 3)
        return rgb_hwc
