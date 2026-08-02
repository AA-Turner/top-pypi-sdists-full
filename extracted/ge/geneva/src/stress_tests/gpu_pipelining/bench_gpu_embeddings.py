#!/usr/bin/env python3
# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Benchmark: OpenCLIP ViT-B/32 embeddings on Oxford-IIT-Pet via Geneva.

Mirrors notebook/demo-geneva-pets-gpu-embeddings-openclip.ipynb but runs as
a standalone script (no Jupyter). Useful for remote runs over ssh or
remote-control agents, and sidesteps Jupyter's autosave race with
external edits.

Iterations (map to the GPU-optimization design doc levers):

    baseline : scalar UDF, batch=1, 1 actor/GPU            — Appendix B's ~10% SM-active regime
    iter1    : array-mode, checkpoint_size=64              — lever #1 (batch size)
    iter2    : persisted-column path (image_rgb uint8
               column) + GPU embed-from-tensor             — preprocess split out, GPU-only
    iter3    : multi-stream replicas (N copies × N streams) — bare in-process replica pool
    iter4a   : iter 2b + torch.compile (CUDA graphs)       — isolates launch-overhead effect
    iter4b   : iter 3  + torch.compile (CUDA graphs)       — tests whether compile unlocks streams

Any iteration that reads image_rgb (iter2b/iter3/iter4a/iter4b) needs the
CPU preprocessor to have run. The script auto-runs it if needed, or you can
pass --skip-preproc when you know the column exists.

Example:

    # Full run
    python bench_gpu_embeddings.py

    # Only iter 4a and 4b against an existing Lance dataset with image_rgb.
    python bench_gpu_embeddings.py \\
        --iters iter4a,iter4b \\
        --skip-data-load \\
        --skip-preproc
"""

from __future__ import annotations

import argparse
import io
import json
import logging
import os
import shutil
import sys
import time
from typing import Any

# Must be set before `import geneva` — otherwise Ray's uv-runtime-env wrapper
# tries to snapshot the current cwd and fails if pyproject.toml isn't there.
os.environ.setdefault("RAY_ENABLE_UV_RUN_RUNTIME_ENV", "0")

import numpy as np  # noqa: E402
import pyarrow as pa  # noqa: E402

import geneva  # noqa: E402
from geneva import udf  # noqa: E402

_LOG = logging.getLogger("bench_gpu_embeddings")

# --------------------------------------------------------------------------
# Constants shared by all iterations.
# --------------------------------------------------------------------------

EMBED_DIM = 512
EMBED_DTYPE = pa.list_(pa.float32(), EMBED_DIM)

PREPROC_DIM = 3 * 224 * 224  # 150528 uint8 per row
PREPROC_DTYPE = pa.list_(pa.uint8(), PREPROC_DIM)

_CLIP_MEAN = (0.48145466, 0.4578275, 0.40821073)
_CLIP_STD = (0.26862954, 0.26130258, 0.27577711)

N_REPLICAS = 4  # multi-stream replicas / iter 4b fan-out

ALL_ITERS = ("baseline", "iter1", "iter2", "iter2c", "iter3", "iter4a", "iter4b")
NEEDS_IMAGE_RGB = {"iter2", "iter2c", "iter3", "iter4a", "iter4b"}

# --------------------------------------------------------------------------
# UDFs — preprocess-overlap and multi-stream-replica variants.
# --------------------------------------------------------------------------


@udf(
    version="openclip-vitb32-scalar",
    data_type=EMBED_DTYPE,
    num_cpus=1,
    num_gpus=1,
)
class OpenClipEmbedScalar:
    """Baseline: one image per model call. PIL decode on GPU actor."""

    def __init__(self) -> None:
        self.model = None
        self.preprocess = None

    def __setup__(self) -> None:
        if self.model is not None:
            return
        import open_clip
        import torch

        m, _, pre = open_clip.create_model_and_transforms(
            "ViT-B-32", pretrained="laion2b_s34b_b79k"
        )
        self.model = m.to("cuda").to(torch.float16).eval()
        self.preprocess = pre

    def __call__(self, image: bytes) -> list[float]:
        import torch
        from PIL import Image

        self.__setup__()
        pil = Image.open(io.BytesIO(image)).convert("RGB")
        tensor = self.preprocess(pil).unsqueeze(0).to("cuda").to(torch.float16)
        with torch.no_grad():
            feats = self.model.encode_image(tensor)
        return feats[0].float().cpu().tolist()


@udf(
    version="openclip-vitb32-batch64",
    data_type=EMBED_DTYPE,
    num_cpus=1,
    num_gpus=1,
    checkpoint_size=64,
)
class OpenClipEmbedBatched:
    """Array-mode (lever #1): model sees `checkpoint_size` images per call."""

    def __init__(self) -> None:
        self.model = None
        self.preprocess = None

    def __setup__(self) -> None:
        if self.model is not None:
            return
        import open_clip
        import torch

        m, _, pre = open_clip.create_model_and_transforms(
            "ViT-B-32", pretrained="laion2b_s34b_b79k"
        )
        self.model = m.to("cuda").to(torch.float16).eval()
        self.preprocess = pre

    def __call__(self, images: pa.Array) -> pa.Array:
        import torch
        from PIL import Image

        self.__setup__()
        pils = [Image.open(io.BytesIO(b.as_py())).convert("RGB") for b in images]
        batch = (
            torch.stack([self.preprocess(p) for p in pils]).to("cuda").to(torch.float16)
        )
        with torch.no_grad():
            feats = self.model.encode_image(batch)
        return pa.array(feats.float().cpu().tolist(), type=EMBED_DTYPE)


@udf(
    version="clip-preproc-cpu-u8-pil-v6-maxcs1024",
    data_type=PREPROC_DTYPE,
    num_cpus=1,
    num_gpus=0,
    memory=2 * 1024 * 1024 * 1024,  # 2 GB: Python + PIL + per-call work buffer
    checkpoint_size=50,
    # Cap Geneva's read batch so the image (binary) column stays under Arrow's
    # int32 list-offset limit (~2 GB cumulative bytes per batch). At 10240 rows
    # × ~200 KB PNGs, Lance was overflowing — see the v5 crash.
    max_checkpoint_size=1024,
)
class ClipPreprocessCPU:
    """Pure-PIL decode + resize-shorter-side(224) + center-crop to uint8."""

    def __call__(self, image: pa.Array) -> pa.Array:
        from PIL import Image

        n = len(image)
        if n == 0:
            values = pa.array(np.empty(0, dtype=np.uint8), type=pa.uint8())
            return pa.FixedSizeListArray.from_arrays(values, PREPROC_DIM)

        out = np.empty((n, PREPROC_DIM), dtype=np.uint8)
        for i, b in enumerate(image):
            pil = Image.open(io.BytesIO(b.as_py())).convert("RGB")
            w, h = pil.size
            if w < h:
                nw, nh = 224, int(round(h * 224 / w))
            else:
                nw, nh = int(round(w * 224 / h)), 224
            pil = pil.resize((nw, nh), Image.BICUBIC)
            left = (nw - 224) // 2
            top = (nh - 224) // 2
            pil = pil.crop((left, top, left + 224, top + 224))
            arr = np.asarray(pil, dtype=np.uint8)
            out[i] = arr.transpose(2, 0, 1).reshape(-1)

        values = pa.array(out.reshape(-1), type=pa.uint8())
        return pa.FixedSizeListArray.from_arrays(values, PREPROC_DIM)


def _from_tensor_udf(version: str, compiled: bool, checkpoint_size: int = 64) -> type:
    """Factory for the GPU embed-from-tensor UDFs (iter 2b, iter 2c, iter 4a)."""

    @udf(
        version=version,
        data_type=EMBED_DTYPE,
        num_cpus=1,
        num_gpus=1,
        checkpoint_size=checkpoint_size,
    )
    class _FromTensor:
        def __init__(self) -> None:
            self.model = None
            self.mean = None
            self.std = None

        def __setup__(self) -> None:
            if self.model is not None:
                return
            import open_clip
            import torch

            m, _, _ = open_clip.create_model_and_transforms(
                "ViT-B-32", pretrained="laion2b_s34b_b79k"
            )
            m = m.to("cuda").to(torch.float16).eval()
            if compiled:
                m = torch.compile(m, mode="reduce-overhead", dynamic=True)
            self.model = m
            self.mean = torch.tensor(
                _CLIP_MEAN, dtype=torch.float16, device="cuda"
            ).view(1, 3, 1, 1)
            self.std = torch.tensor(_CLIP_STD, dtype=torch.float16, device="cuda").view(
                1, 3, 1, 1
            )
            if compiled:
                with torch.no_grad():
                    dummy = torch.zeros(
                        64, 3, 224, 224, device="cuda", dtype=torch.float16
                    )
                    _ = self.model.encode_image(dummy)
                torch.cuda.synchronize()

        def __call__(self, image_rgb: pa.Array) -> pa.Array:
            import torch

            self.__setup__()
            arr = (
                image_rgb.combine_chunks()
                if hasattr(image_rgb, "combine_chunks")
                else image_rgb
            )
            flat = np.asarray(arr.flatten(), dtype=np.uint8)
            batch = flat.reshape(-1, 3, 224, 224)
            tensor = torch.from_numpy(batch).to("cuda", non_blocking=True)
            tensor = tensor.to(torch.float16) / 255.0
            tensor = (tensor - self.mean) / self.std
            with torch.no_grad():
                feats = self.model.encode_image(tensor)
            feats_np = feats.float().cpu().numpy()
            values = pa.array(feats_np.reshape(-1), type=pa.float32())
            return pa.FixedSizeListArray.from_arrays(values, EMBED_DIM)

    _FromTensor.__name__ = (
        "OpenClipEmbedFromTensorCompiled" if compiled else "OpenClipEmbedFromTensor"
    )
    return _FromTensor


def _multi_stream_replicas_udf(version: str, compiled: bool) -> type:
    """Factory for the multi-stream replica UDFs (iter 3, iter 4b)."""

    @udf(
        version=version,
        data_type=EMBED_DTYPE,
        num_cpus=1,
        num_gpus=1,
        checkpoint_size=256,
    )
    class _MultiStreamReplicas:
        def __init__(self) -> None:
            self.replicas = None
            self.streams = None
            self.mean = None
            self.std = None

        def __setup__(self) -> None:
            if self.replicas is not None:
                return
            import open_clip
            import torch

            reps = []
            streams = []
            for _ in range(N_REPLICAS):
                m, _, _ = open_clip.create_model_and_transforms(
                    "ViT-B-32", pretrained="laion2b_s34b_b79k"
                )
                m = m.to("cuda").to(torch.float16).eval()
                if compiled:
                    m = torch.compile(m, mode="reduce-overhead", dynamic=True)
                reps.append(m)
                streams.append(torch.cuda.Stream())
            self.replicas = reps
            self.streams = streams
            self.mean = torch.tensor(
                _CLIP_MEAN, dtype=torch.float16, device="cuda"
            ).view(1, 3, 1, 1)
            self.std = torch.tensor(_CLIP_STD, dtype=torch.float16, device="cuda").view(
                1, 3, 1, 1
            )
            if compiled:
                per = 256 // N_REPLICAS
                with torch.no_grad():
                    for m, s in zip(self.replicas, self.streams):
                        with torch.cuda.stream(s):
                            dummy = torch.zeros(
                                per, 3, 224, 224, device="cuda", dtype=torch.float16
                            )
                            _ = m.encode_image(dummy)
                    torch.cuda.synchronize()

        def __call__(self, image_rgb: pa.Array) -> pa.Array:
            import torch

            self.__setup__()
            arr = (
                image_rgb.combine_chunks()
                if hasattr(image_rgb, "combine_chunks")
                else image_rgb
            )
            flat = np.asarray(arr.flatten(), dtype=np.uint8)
            batch = flat.reshape(-1, 3, 224, 224)
            tensor = torch.from_numpy(batch).to("cuda", non_blocking=True)
            tensor = tensor.to(torch.float16) / 255.0
            tensor = (tensor - self.mean) / self.std

            chunks = torch.chunk(tensor, N_REPLICAS, dim=0)
            out: list[Any] = [None] * len(chunks)
            for i, (chunk, model, stream) in enumerate(
                zip(chunks, self.replicas, self.streams)
            ):
                with torch.cuda.stream(stream):
                    with torch.no_grad():
                        out[i] = model.encode_image(chunk)
            torch.cuda.synchronize()

            feats = torch.cat(out, dim=0)
            feats_np = feats.float().cpu().numpy()
            values = pa.array(feats_np.reshape(-1), type=pa.float32())
            return pa.FixedSizeListArray.from_arrays(values, EMBED_DIM)

    _MultiStreamReplicas.__name__ = (
        "OpenClipEmbedMultiStreamReplicasCompiled"
        if compiled
        else "OpenClipEmbedMultiStreamReplicas"
    )
    return _MultiStreamReplicas


# --------------------------------------------------------------------------
# Fused UDF: preprocess() does the CPU PIL decode/resize/crop in
# pipelining-driven reader threads/actors, __call__() does the GPU embed.
# The point is to compare GPU throughput against the persisted-column
# approach (iter2a + iter2) — if pipelining keeps the GPU fed at the same
# rate, the persisted ``image_rgb`` column becomes optional.
# --------------------------------------------------------------------------


def _fused_preproc_udf() -> type:
    """Factory for ``OpenClipEmbedFused``.

    The class must be built inside a factory so cloudpickle serializes
    it **by value** rather than by module reference. Module-reference
    serialization fails on Ray workers, which don't have ``notebook/``
    on their ``sys.path`` — see ``OpenClipEmbedFromTensor`` for the
    same pattern (factory-built so cloudpickle inlines the definition).
    """

    @udf(
        # ``input_columns`` is the union of (a) what Geneva reads
        # from Lance — only ``image`` exists in the source — and
        # (b) what ``__call__`` consumes after preprocess —
        # ``_pp_rgb``. Geneva tolerates the missing column at read
        # time when ``preprocess()`` is declared; preprocess adds
        # ``_pp_rgb`` to the batch before ``__call__`` runs. Mirrors
        # the ``_DoubleWithPreprocess`` test fixture's pattern.
        input_columns=["image", "_pp_rgb"],
        version="openclip-vitb32-fused-pp-v1",
        data_type=EMBED_DTYPE,
        num_cpus=1,
        num_gpus=1,
        checkpoint_size=64,
    )
    class _FusedPreprocEmbed:
        def __init__(self) -> None:
            self.model = None
            self.mean = None
            self.std = None

        def __setup__(self) -> None:
            if self.model is not None:
                return
            import open_clip
            import torch

            m, _, _ = open_clip.create_model_and_transforms(
                "ViT-B-32", pretrained="laion2b_s34b_b79k"
            )
            self.model = m.to("cuda").to(torch.float16).eval()
            self.mean = torch.tensor(
                _CLIP_MEAN, dtype=torch.float16, device="cuda"
            ).view(1, 3, 1, 1)
            self.std = torch.tensor(_CLIP_STD, dtype=torch.float16, device="cuda").view(
                1, 3, 1, 1
            )

        def preprocess(self, batch: pa.RecordBatch) -> pa.RecordBatch:
            """PIL decode + resize-shorter-side(224) + center-crop to uint8.

            Identical pixel ops to ``ClipPreprocessCPU``, but runs
            in a reader thread so the GPU thread doesn't block on it. Returns the batch
            with a ``_pp_rgb`` FixedSizeList<uint8, 3*224*224> column
            appended. Using a non-user-facing name (``_pp_rgb`` rather
            than the already-persisted ``image_rgb``) lets this UDF
            coexist with iter2's persisted column on the same table.
            """
            from PIL import Image

            image_col = batch["image"]
            n = len(image_col)
            out = np.empty((n, PREPROC_DIM), dtype=np.uint8)
            for i, b in enumerate(image_col):
                pil = Image.open(io.BytesIO(b.as_py())).convert("RGB")
                w, h = pil.size
                if w < h:
                    nw, nh = 224, int(round(h * 224 / w))
                else:
                    nw, nh = int(round(w * 224 / h)), 224
                pil = pil.resize((nw, nh), Image.BICUBIC)
                left = (nw - 224) // 2
                top = (nh - 224) // 2
                pil = pil.crop((left, top, left + 224, top + 224))
                arr = np.asarray(pil, dtype=np.uint8)
                out[i] = arr.transpose(2, 0, 1).reshape(-1)

            values = pa.array(out.reshape(-1), type=pa.uint8())
            rgb_array = pa.FixedSizeListArray.from_arrays(values, PREPROC_DIM)
            return pa.RecordBatch.from_arrays(
                [*list(batch.columns), rgb_array],
                names=[*list(batch.schema.names), "_pp_rgb"],
            )

        def __call__(self, image: pa.Array, _pp_rgb: pa.Array) -> pa.Array:
            del image  # only here so the framework reads it for preprocess
            import torch

            self.__setup__()
            arr = (
                _pp_rgb.combine_chunks()
                if hasattr(_pp_rgb, "combine_chunks")
                else _pp_rgb
            )
            flat = np.asarray(arr.flatten(), dtype=np.uint8)
            batch = flat.reshape(-1, 3, 224, 224)
            tensor = torch.from_numpy(batch).to("cuda", non_blocking=True)
            tensor = tensor.to(torch.float16) / 255.0
            tensor = (tensor - self.mean) / self.std
            with torch.no_grad():
                feats = self.model.encode_image(tensor)
            feats_np = feats.float().cpu().numpy()
            values = pa.array(feats_np.reshape(-1), type=pa.float32())
            return pa.FixedSizeListArray.from_arrays(values, EMBED_DIM)

    _FusedPreprocEmbed.__name__ = "OpenClipEmbedFused"
    return _FusedPreprocEmbed


OpenClipEmbedFused = _fused_preproc_udf()


def _fused_preproc_udf_fat() -> type:
    """Fused UDF with ``num_cpus=8`` so reader threads have room.

    The default fused variant declares ``num_cpus=1``, matching the
    GPU-only iter 2 UDF. That works when preprocess() is empty, but
    for preprocess-overlap pipelining the actor's reader threads
    compete for that single CPU reservation and cap CPU throughput
    far below the
    box ceiling. Appendix G of ``gpus-optimizations.md`` shows ~557
    img/s at 8 CPU workers vs ~120 at 1 — meaning the per-actor CPU
    budget is the actual lever for hitting the GPU's 473 img/s.
    """

    @udf(
        input_columns=["image", "_pp_rgb"],
        version="openclip-vitb32-fused-pp-fat-v1",
        data_type=EMBED_DTYPE,
        num_cpus=8,
        num_gpus=1,
        checkpoint_size=64,
    )
    class _FusedPreprocEmbedFat:
        def __init__(self) -> None:
            self.model = None
            self.mean = None
            self.std = None

        def __setup__(self) -> None:
            if self.model is not None:
                return
            import open_clip
            import torch

            m, _, _ = open_clip.create_model_and_transforms(
                "ViT-B-32", pretrained="laion2b_s34b_b79k"
            )
            self.model = m.to("cuda").to(torch.float16).eval()
            self.mean = torch.tensor(
                _CLIP_MEAN, dtype=torch.float16, device="cuda"
            ).view(1, 3, 1, 1)
            self.std = torch.tensor(_CLIP_STD, dtype=torch.float16, device="cuda").view(
                1, 3, 1, 1
            )

        def preprocess(self, batch: pa.RecordBatch) -> pa.RecordBatch:
            from PIL import Image

            image_col = batch["image"]
            n = len(image_col)
            out = np.empty((n, PREPROC_DIM), dtype=np.uint8)
            for i, b in enumerate(image_col):
                pil = Image.open(io.BytesIO(b.as_py())).convert("RGB")
                w, h = pil.size
                if w < h:
                    nw, nh = 224, int(round(h * 224 / w))
                else:
                    nw, nh = int(round(w * 224 / h)), 224
                pil = pil.resize((nw, nh), Image.BICUBIC)
                left = (nw - 224) // 2
                top = (nh - 224) // 2
                pil = pil.crop((left, top, left + 224, top + 224))
                arr = np.asarray(pil, dtype=np.uint8)
                out[i] = arr.transpose(2, 0, 1).reshape(-1)

            values = pa.array(out.reshape(-1), type=pa.uint8())
            rgb_array = pa.FixedSizeListArray.from_arrays(values, PREPROC_DIM)
            return pa.RecordBatch.from_arrays(
                [*list(batch.columns), rgb_array],
                names=[*list(batch.schema.names), "_pp_rgb"],
            )

        def __call__(self, image: pa.Array, _pp_rgb: pa.Array) -> pa.Array:
            del image
            import torch

            self.__setup__()
            arr = (
                _pp_rgb.combine_chunks()
                if hasattr(_pp_rgb, "combine_chunks")
                else _pp_rgb
            )
            flat = np.asarray(arr.flatten(), dtype=np.uint8)
            batch = flat.reshape(-1, 3, 224, 224)
            tensor = torch.from_numpy(batch).to("cuda", non_blocking=True)
            tensor = tensor.to(torch.float16) / 255.0
            tensor = (tensor - self.mean) / self.std
            with torch.no_grad():
                feats = self.model.encode_image(tensor)
            feats_np = feats.float().cpu().numpy()
            values = pa.array(feats_np.reshape(-1), type=pa.float32())
            return pa.FixedSizeListArray.from_arrays(values, EMBED_DIM)

    _FusedPreprocEmbedFat.__name__ = "OpenClipEmbedFusedFat"
    return _FusedPreprocEmbedFat


OpenClipEmbedFusedFat = _fused_preproc_udf_fat()


def _fused_preproc_udf_cv2() -> type:
    """Fused UDF whose preprocess() uses cv2 instead of PIL.

    PIL releases the GIL for ~30 % of the per-image decode time —
    Python-level loop overhead and PyArrow ``b.as_py()`` hold it
    for the rest, capping thread-pool scaling at ~2-3× single-thread
    (Amdahl). cv2's ``imdecode`` / ``resize`` / ``cvtColor`` are
    pure C with the GIL released throughout, so 8 threads should
    scale closer to 8× and approach the GPU ceiling on this
    workload. Same pixel ops as ``ClipPreprocessCPU`` /
    ``OpenClipEmbedFused`` (resize-shorter-side(224) +
    center-crop) — output is byte-identical modulo BICUBIC vs
    cv2's ``INTER_CUBIC`` rounding.
    """

    @udf(
        input_columns=["image", "_pp_rgb"],
        version="openclip-vitb32-fused-cv2-v1",
        data_type=EMBED_DTYPE,
        num_cpus=1,
        num_gpus=1,
        checkpoint_size=64,
    )
    class _FusedPreprocEmbedCv2:
        def __init__(self) -> None:
            self.model = None
            self.mean = None
            self.std = None

        def __setup__(self) -> None:
            if self.model is not None:
                return
            import open_clip
            import torch

            m, _, _ = open_clip.create_model_and_transforms(
                "ViT-B-32", pretrained="laion2b_s34b_b79k"
            )
            self.model = m.to("cuda").to(torch.float16).eval()
            self.mean = torch.tensor(
                _CLIP_MEAN, dtype=torch.float16, device="cuda"
            ).view(1, 3, 1, 1)
            self.std = torch.tensor(_CLIP_STD, dtype=torch.float16, device="cuda").view(
                1, 3, 1, 1
            )

        def preprocess(self, batch: pa.RecordBatch) -> pa.RecordBatch:
            """cv2 decode + resize-shorter-side(224) + center-crop to uint8 RGB."""
            import cv2

            # Restrict cv2's internal OpenMP/parallel-for to one
            # thread per call. Otherwise eight reader threads × cv2's
            # internal parallelism oversubscribes the box and cores
            # ping-pong between threads instead of staying hot.
            cv2.setNumThreads(1)

            image_col = batch["image"]
            n = len(image_col)
            out = np.empty((n, PREPROC_DIM), dtype=np.uint8)
            for i, b in enumerate(image_col):
                # ``np.frombuffer`` is zero-copy on the underlying
                # bytes object, so the only allocation here is the
                # decoded RGB array — no double-buffering vs PIL.
                buf = np.frombuffer(b.as_py(), dtype=np.uint8)
                img = cv2.imdecode(buf, cv2.IMREAD_COLOR)  # BGR
                h, w = img.shape[:2]
                if w < h:
                    nw, nh = 224, int(round(h * 224 / w))
                else:
                    nw, nh = int(round(w * 224 / h)), 224
                img = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_CUBIC)
                left = (nw - 224) // 2
                top = (nh - 224) // 2
                img = img[top : top + 224, left : left + 224, :]
                # cv2 is BGR; ``cvtColor`` runs the channel reorder in
                # a single C call (GIL-released) AND returns a fresh
                # contiguous buffer — avoids the stride-flip +
                # ``np.ascontiguousarray`` round-trip that cost ~5 ms
                # per 2500-row batch in the PIL-style version.
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                # HWC -> CHW for the model. ``transpose`` is a stride
                # view; ``reshape(-1)`` materialises the contiguous
                # 1-D output. ``out[i] = ...`` then memcpy's into the
                # pre-allocated batch buffer.
                out[i] = img.transpose(2, 0, 1).reshape(-1)

            values = pa.array(out.reshape(-1), type=pa.uint8())
            rgb_array = pa.FixedSizeListArray.from_arrays(values, PREPROC_DIM)
            return pa.RecordBatch.from_arrays(
                [*list(batch.columns), rgb_array],
                names=[*list(batch.schema.names), "_pp_rgb"],
            )

        def __call__(self, image: pa.Array, _pp_rgb: pa.Array) -> pa.Array:
            del image
            import torch

            self.__setup__()
            arr = (
                _pp_rgb.combine_chunks()
                if hasattr(_pp_rgb, "combine_chunks")
                else _pp_rgb
            )
            flat = np.asarray(arr.flatten(), dtype=np.uint8)
            batch = flat.reshape(-1, 3, 224, 224)
            tensor = torch.from_numpy(batch).to("cuda", non_blocking=True)
            tensor = tensor.to(torch.float16) / 255.0
            tensor = (tensor - self.mean) / self.std
            with torch.no_grad():
                feats = self.model.encode_image(tensor)
            feats_np = feats.float().cpu().numpy()
            values = pa.array(feats_np.reshape(-1), type=pa.float32())
            return pa.FixedSizeListArray.from_arrays(values, EMBED_DIM)

    _FusedPreprocEmbedCv2.__name__ = "OpenClipEmbedFusedCv2"
    return _FusedPreprocEmbedCv2


OpenClipEmbedFusedCv2 = _fused_preproc_udf_cv2()


def _fused_preproc_udf_cv2_fast() -> type:
    """cv2 fused UDF with the per-row Python loop overhead stripped.

    The previous ``OpenClipEmbedFusedCv2`` plateaus at ~200 img/s
    not because of the C decoder but because every iteration of
    ``for i, b in enumerate(image_col): b.as_py()`` is GIL-held
    PyArrow scalar conversion. With Amdahl's law and ~30 % Python
    overhead per row, 24 threads cap at ~3× single-thread.

    This variant pulls the bytes out of the Arrow batch in **one**
    operation per batch — getting (data_buffer, offsets) from
    ``image_col.buffers()`` — then iterates a numpy view over the
    offsets array. The per-row work becomes:

        np.frombuffer(data_buf, dtype=np.uint8,
                      count=off[i+1]-off[i], offset=off[i])

    which is zero-copy and GIL-released. The PyArrow→Python scalar
    bridge is hit once per batch, not once per row.
    """

    @udf(
        input_columns=["image", "_pp_rgb"],
        version="openclip-vitb32-fused-cv2-fast-v1",
        data_type=EMBED_DTYPE,
        num_cpus=1,
        num_gpus=1,
        checkpoint_size=64,
    )
    class _FusedPreprocEmbedCv2Fast:
        def __init__(self) -> None:
            self.model = None
            self.mean = None
            self.std = None

        def __setup__(self) -> None:
            if self.model is not None:
                return
            import open_clip
            import torch

            m, _, _ = open_clip.create_model_and_transforms(
                "ViT-B-32", pretrained="laion2b_s34b_b79k"
            )
            self.model = m.to("cuda").to(torch.float16).eval()
            self.mean = torch.tensor(
                _CLIP_MEAN, dtype=torch.float16, device="cuda"
            ).view(1, 3, 1, 1)
            self.std = torch.tensor(_CLIP_STD, dtype=torch.float16, device="cuda").view(
                1, 3, 1, 1
            )

        def preprocess(self, batch: pa.RecordBatch) -> pa.RecordBatch:
            """Zero-copy Arrow byte access + cv2 decode."""
            import cv2

            cv2.setNumThreads(1)

            image_col = batch["image"]

            # ChunkedArray vs Array: ``RecordBatch[col]`` returns
            # an Array (single chunk), but a defensive
            # ``combine_chunks`` covers the case where the caller
            # has stitched chunked data into the batch.
            if hasattr(image_col, "combine_chunks"):
                try:
                    image_col = image_col.combine_chunks()
                except (AttributeError, NotImplementedError):
                    pass

            # ``buffers()`` for a binary array returns
            # ``[validity, offsets, data]``. We rely on no nulls
            # in the image column (production guarantees this);
            # a null check would add per-row work back. Offsets
            # are int32 for ``binary``, int64 for ``large_binary``.
            bufs = image_col.buffers()
            offsets_buf = bufs[1]
            data_buf = bufs[2]
            offset_dtype = (
                np.int64 if pa.types.is_large_binary(image_col.type) else np.int32
            )
            # ``np.frombuffer`` is a zero-copy view over the Arrow
            # buffer. Slice past any leading offset baked into the
            # array (sliced arrays may not start at index 0).
            arr_offset = image_col.offset
            offsets = np.frombuffer(offsets_buf, dtype=offset_dtype)[
                arr_offset : arr_offset + len(image_col) + 1
            ]
            data_view = np.frombuffer(data_buf, dtype=np.uint8)

            n = len(image_col)
            out = np.empty((n, PREPROC_DIM), dtype=np.uint8)
            for i in range(n):
                # Zero-copy bytes view for this row's encoded image.
                buf = data_view[offsets[i] : offsets[i + 1]]
                img = cv2.imdecode(buf, cv2.IMREAD_COLOR)  # BGR
                h, w = img.shape[:2]
                if w < h:
                    nw, nh = 224, int(round(h * 224 / w))
                else:
                    nw, nh = int(round(w * 224 / h)), 224
                img = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_CUBIC)
                left = (nw - 224) // 2
                top = (nh - 224) // 2
                img = img[top : top + 224, left : left + 224, :]
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                out[i] = img.transpose(2, 0, 1).reshape(-1)

            values = pa.array(out.reshape(-1), type=pa.uint8())
            rgb_array = pa.FixedSizeListArray.from_arrays(values, PREPROC_DIM)
            return pa.RecordBatch.from_arrays(
                [*list(batch.columns), rgb_array],
                names=[*list(batch.schema.names), "_pp_rgb"],
            )

        def __call__(self, image: pa.Array, _pp_rgb: pa.Array) -> pa.Array:
            del image
            import torch

            self.__setup__()
            arr = (
                _pp_rgb.combine_chunks()
                if hasattr(_pp_rgb, "combine_chunks")
                else _pp_rgb
            )
            flat = np.asarray(arr.flatten(), dtype=np.uint8)
            batch = flat.reshape(-1, 3, 224, 224)
            tensor = torch.from_numpy(batch).to("cuda", non_blocking=True)
            tensor = tensor.to(torch.float16) / 255.0
            tensor = (tensor - self.mean) / self.std
            with torch.no_grad():
                feats = self.model.encode_image(tensor)
            feats_np = feats.float().cpu().numpy()
            values = pa.array(feats_np.reshape(-1), type=pa.float32())
            return pa.FixedSizeListArray.from_arrays(values, EMBED_DIM)

    _FusedPreprocEmbedCv2Fast.__name__ = "OpenClipEmbedFusedCv2Fast"
    return _FusedPreprocEmbedCv2Fast


OpenClipEmbedFusedCv2Fast = _fused_preproc_udf_cv2_fast()


def _fused_preproc_udf_cv2_multi_stream_replicas() -> type:
    """Fused cv2 preprocess + 4-replica × 4-stream multi-stream embed.

    iter 3 historical (``OpenClipEmbedMultiStreamReplicas``) ran 4
    ViT-B/32 replicas concurrently across 4 CUDA streams against the
    pre-persisted ``image_rgb`` column. On consumer GPUs this
    regressed slightly vs single-model iter 2b because per-stream
    batches were too small (~25 rows in the original test). Now
    that the read path delivers batch=256 to the UDF (after the
    harness bumps min/max_checkpoint_size), each of the 4 streams
    sees ~64 rows — the same per-replica batch as iter 2b.
    Combined with our cv2 fused preprocess, this tests whether
    multi-stream concurrency can extract the time-averaged 40 %
    SM headroom we measured.
    """

    @udf(
        input_columns=["image", "_pp_rgb"],
        version="openclip-vitb32-fused-cv2-multi-stream-replicas-r4-v1",
        data_type=EMBED_DTYPE,
        num_cpus=1,
        num_gpus=1,
        checkpoint_size=256,
    )
    class _FusedMultiStreamReplicas:
        def __init__(self) -> None:
            self.replicas = None
            self.streams = None
            self.mean = None
            self.std = None

        def __setup__(self) -> None:
            if self.replicas is not None:
                return
            import open_clip
            import torch

            reps = []
            streams = []
            for _ in range(N_REPLICAS):
                m, _, _ = open_clip.create_model_and_transforms(
                    "ViT-B-32", pretrained="laion2b_s34b_b79k"
                )
                m = m.to("cuda").to(torch.float16).eval()
                reps.append(m)
                streams.append(torch.cuda.Stream())
            self.replicas = reps
            self.streams = streams
            self.mean = torch.tensor(
                _CLIP_MEAN, dtype=torch.float16, device="cuda"
            ).view(1, 3, 1, 1)
            self.std = torch.tensor(_CLIP_STD, dtype=torch.float16, device="cuda").view(
                1, 3, 1, 1
            )

        def preprocess(self, batch: pa.RecordBatch) -> pa.RecordBatch:
            """Same zero-copy Arrow + cv2 preprocess as cv2fast."""
            import cv2

            cv2.setNumThreads(1)
            image_col = batch["image"]
            if hasattr(image_col, "combine_chunks"):
                try:
                    image_col = image_col.combine_chunks()
                except Exception:
                    pass
            bufs = image_col.buffers()
            offsets_buf = bufs[1]
            data_buf = bufs[2]
            offset_dtype = (
                np.int64 if pa.types.is_large_binary(image_col.type) else np.int32
            )
            arr_offset = image_col.offset
            offsets = np.frombuffer(offsets_buf, dtype=offset_dtype)[
                arr_offset : arr_offset + len(image_col) + 1
            ]
            data_view = np.frombuffer(data_buf, dtype=np.uint8)
            n = len(image_col)
            out = np.empty((n, PREPROC_DIM), dtype=np.uint8)
            for i in range(n):
                buf = data_view[offsets[i] : offsets[i + 1]]
                img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
                h, w = img.shape[:2]
                if w < h:
                    nw, nh = 224, int(round(h * 224 / w))
                else:
                    nw, nh = int(round(w * 224 / h)), 224
                img = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_CUBIC)
                left = (nw - 224) // 2
                top = (nh - 224) // 2
                img = img[top : top + 224, left : left + 224, :]
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                out[i] = img.transpose(2, 0, 1).reshape(-1)
            values = pa.array(out.reshape(-1), type=pa.uint8())
            rgb_array = pa.FixedSizeListArray.from_arrays(values, PREPROC_DIM)
            return pa.RecordBatch.from_arrays(
                [*list(batch.columns), rgb_array],
                names=[*list(batch.schema.names), "_pp_rgb"],
            )

        def __call__(self, image: pa.Array, _pp_rgb: pa.Array) -> pa.Array:
            del image
            import torch

            self.__setup__()
            arr = (
                _pp_rgb.combine_chunks()
                if hasattr(_pp_rgb, "combine_chunks")
                else _pp_rgb
            )
            flat = np.asarray(arr.flatten(), dtype=np.uint8)
            batch = flat.reshape(-1, 3, 224, 224)
            tensor = torch.from_numpy(batch).to("cuda", non_blocking=True)
            tensor = tensor.to(torch.float16) / 255.0
            tensor = (tensor - self.mean) / self.std

            # Fan out across N_REPLICAS streams. ``torch.chunk`` is a
            # view, so the slices share storage with ``tensor``.
            chunks = torch.chunk(tensor, N_REPLICAS, dim=0)
            out: list[Any] = [None] * len(chunks)
            for i, (chunk, model, stream) in enumerate(
                zip(chunks, self.replicas, self.streams)
            ):
                with torch.cuda.stream(stream):
                    with torch.no_grad():
                        out[i] = model.encode_image(chunk)
            torch.cuda.synchronize()

            feats = torch.cat(out, dim=0)
            feats_np = feats.float().cpu().numpy()
            values = pa.array(feats_np.reshape(-1), type=pa.float32())
            return pa.FixedSizeListArray.from_arrays(values, EMBED_DIM)

    _FusedMultiStreamReplicas.__name__ = "OpenClipEmbedFusedMultiStreamReplicas"
    return _FusedMultiStreamReplicas


OpenClipEmbedFusedMultiStreamReplicas = _fused_preproc_udf_cv2_multi_stream_replicas()


def _fused_nvjpeg_udf() -> type:
    """JPEG decode on GPU via nvJPEG + OpenCLIP embed.

    Uses ``torchvision.io.decode_jpeg(..., device='cuda')`` which
    dispatches to NVIDIA's nvJPEG library. On supported hardware
    (Ampere+, including this RTX 4000 Ada) nvJPEG runs JPEG decode
    on dedicated silicon distinct from the SMs, so it can run in
    parallel with the model forward pass.

    The UDF intentionally has **no** ``preprocess()`` method — all
    work happens in ``__call__`` on the GPU. Phase-1 read-overlap
    still applies (the reader thread streams Lance batches while
    the GPU is busy), but there's no CPU preprocess work to push
    into reader threads.

    Reads ``image_jpeg`` (re-encoded by ``prep_jpeg_column.py``).
    Without that column the bench will error at
    ``add_columns`` validation time.
    """

    @udf(
        input_columns=["image_jpeg"],
        version="openclip-vitb32-fused-nvjpeg-v1",
        data_type=EMBED_DTYPE,
        num_cpus=1,
        num_gpus=1,
        checkpoint_size=64,
    )
    class _NvJpegEmbed:
        def __init__(self) -> None:
            self.model = None
            self.mean = None
            self.std = None

        def __setup__(self) -> None:
            if self.model is not None:
                return
            import open_clip
            import torch

            m, _, _ = open_clip.create_model_and_transforms(
                "ViT-B-32", pretrained="laion2b_s34b_b79k"
            )
            self.model = m.to("cuda").to(torch.float16).eval()
            self.mean = torch.tensor(
                _CLIP_MEAN, dtype=torch.float16, device="cuda"
            ).view(1, 3, 1, 1)
            self.std = torch.tensor(_CLIP_STD, dtype=torch.float16, device="cuda").view(
                1, 3, 1, 1
            )

        def __call__(self, image_jpeg: pa.Array) -> pa.Array:
            import torch
            import torch.nn.functional as F
            from torchvision.io import ImageReadMode, decode_jpeg

            self.__setup__()

            # Build a list of GPU-resident byte tensors. ``frombuffer``
            # is zero-copy from the underlying Arrow data; ``.clone()``
            # is needed because torch refuses to stage non-writable
            # buffers across the CUDA copy. Cheap (one alloc per row,
            # not the full decoded payload).
            cuda = torch.device("cuda")
            jpeg_tensors = []
            for b in image_jpeg:
                raw = b.as_py()
                jpeg_tensors.append(torch.frombuffer(raw, dtype=torch.uint8).clone())

            # Batched nvJPEG decode. Returns a list of (3, H_i, W_i)
            # uint8 tensors on the GPU — sizes vary because Oxford
            # pet images aren't uniformly cropped.
            decoded = decode_jpeg(jpeg_tensors, mode=ImageReadMode.RGB, device=cuda)

            # Resize-shorter-side(224) + center-crop on GPU,
            # per-image. Each resize is one ``F.interpolate`` call;
            # batched stacking happens after every image is 224×224.
            resized = []
            for t in decoded:
                _, h, w = t.shape
                if w < h:
                    nw, nh = 224, int(round(h * 224 / w))
                else:
                    nw, nh = int(round(w * 224 / h)), 224
                # interpolate wants float and a 4D tensor.
                # ``bilinear``+``antialias=False`` is significantly
                # cheaper per-launch than the bicubic+antialias the
                # CPU paths use; the embedding quality difference
                # is sub-percent on most CLIP workloads but the
                # launch-overhead reduction is several × per call,
                # which matters because we issue one interpolate
                # per row in a Python loop.
                t = F.interpolate(
                    t.unsqueeze(0).to(torch.float16),
                    size=(nh, nw),
                    mode="bilinear",
                    antialias=False,
                ).squeeze(0)
                top = (nh - 224) // 2
                left = (nw - 224) // 2
                t = t[:, top : top + 224, left : left + 224]
                resized.append(t)

            tensor = torch.stack(resized) / 255.0
            tensor = (tensor - self.mean) / self.std
            with torch.no_grad():
                feats = self.model.encode_image(tensor)
            feats_np = feats.float().cpu().numpy()
            values = pa.array(feats_np.reshape(-1), type=pa.float32())
            return pa.FixedSizeListArray.from_arrays(values, EMBED_DIM)

    _NvJpegEmbed.__name__ = "OpenClipEmbedFusedNvJpeg"
    return _NvJpegEmbed


OpenClipEmbedFusedNvJpeg = _fused_nvjpeg_udf()


# Instantiate the factory-built UDF classes once at module import.
OpenClipEmbedFromTensor = _from_tensor_udf("openclip-vitb32-from-u8-v2", compiled=False)
OpenClipEmbedFromTensorBatch256 = _from_tensor_udf(
    "openclip-vitb32-from-u8-cs256-v1", compiled=False, checkpoint_size=256
)
OpenClipEmbedFromTensorCompiled = _from_tensor_udf(
    "openclip-vitb32-from-u8-compiled-v1", compiled=True
)
OpenClipEmbedMultiStreamReplicas = _multi_stream_replicas_udf(
    f"openclip-vitb32-multi-stream-replicas-u8-r{N_REPLICAS}", compiled=False
)
OpenClipEmbedMultiStreamReplicasCompiled = _multi_stream_replicas_udf(
    f"openclip-vitb32-multi-stream-replicas-compiled-r{N_REPLICAS}", compiled=True
)


# --------------------------------------------------------------------------
# Dataset load.
# --------------------------------------------------------------------------


def write_lance_dataset(
    images_path: str, num_images: int, rows_per_fragment: int
) -> None:
    """Write `num_images` Oxford-IIT-Pet rows to ./db/images.lance."""
    import lance
    from datasets import load_dataset

    shutil.rmtree(images_path + "/db", ignore_errors=True)
    shutil.rmtree(images_path + "/ckp", ignore_errors=True)

    def _iter_rows():
        dataset = load_dataset("timm/oxford-iiit-pet", split="train+test")
        src = len(dataset)
        batch = []
        yielded = 0
        while yielded < num_images:
            row = dataset[yielded % src]
            buf = io.BytesIO()
            row["image"].save(buf, format="png")
            batch.append(
                {
                    "image": buf.getvalue(),
                    "label": row["label"],
                    "image_id": f"{row['image_id']}_{yielded // src}",
                    "label_cat_dog": row["label_cat_dog"],
                }
            )
            yielded += 1
            if len(batch) >= rows_per_fragment:
                yield pa.RecordBatch.from_pylist(batch)
                batch = []
        if batch:
            yield pa.RecordBatch.from_pylist(batch)

    schema = pa.schema(
        [
            pa.field("image", pa.binary()),
            pa.field("label", pa.int16()),
            pa.field("image_id", pa.string()),
            pa.field("label_cat_dog", pa.int16()),
        ]
    )
    _LOG.info(
        "writing %d rows (%d per fragment) to %s/db/images.lance",
        num_images,
        rows_per_fragment,
        images_path,
    )
    lance.write_dataset(
        _iter_rows(),
        images_path + "/db/images.lance",
        mode="overwrite",
        schema=schema,
    )


# --------------------------------------------------------------------------
# Iteration drivers.
# --------------------------------------------------------------------------


def _has_column(t, name: str) -> bool:
    return any(f.name == name for f in t.schema)


def _run_column(
    t,
    *,
    udf_cls: type,
    input_cols: list[str],
    out_col: str,
    label: str,
    concurrency: int | None = None,
) -> float:
    """Drop if exists, add the column, backfill, return elapsed seconds.

    When `concurrency` is None, uses Geneva's default. Pass a lower number
    (e.g. 2) for CPU-heavy UDFs on laptop-class boxes to keep the sum of
    actor resident memory below physical RAM.
    """
    if _has_column(t, out_col):
        try:
            t.drop_columns([out_col])
        except Exception as e:
            _LOG.warning("could not drop %s: %s", out_col, e)

    t.add_columns({out_col: (udf_cls, input_cols)})
    t0 = time.time()
    backfill_kwargs: dict[str, Any] = {"_admission_check": False}
    if concurrency is not None:
        backfill_kwargs["concurrency"] = concurrency
    t.backfill(out_col, **backfill_kwargs)
    elapsed = time.time() - t0
    n_rows = t.count_rows()
    _LOG.info(
        "%s: %.2fs — %.1f img/s",
        label,
        elapsed,
        n_rows / elapsed if elapsed else 0.0,
    )
    return elapsed


def ensure_image_rgb(t) -> float:
    """Run the persisted-column CPU preprocessor if image_rgb isn't present.

    Uses concurrency=1 to survive large Lance fragments. With
    rows_per_fragment=4096 the applier actor can balloon well past
    nominal memory estimates (observed ~19 GB RSS for a single actor
    under load), so we serialize preproc. Default concurrency=8 OOMs
    immediately on this fragment size.
    """
    if _has_column(t, "image_rgb"):
        _LOG.info("image_rgb column already present; skipping preproc")
        return 0.0
    return _run_column(
        t,
        udf_cls=ClipPreprocessCPU,
        input_cols=["image"],
        out_col="image_rgb",
        label="iter2a (CPU preprocess)",
        concurrency=1,
    )


# --------------------------------------------------------------------------
# CLI / main.
# --------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--images-path", default=".", help="Parent dir for db/ and ckp/.")
    p.add_argument("--num-images", type=int, default=40000)
    p.add_argument("--rows-per-fragment", type=int, default=4096)
    p.add_argument(
        "--iters",
        default=",".join(ALL_ITERS),
        help=f"Comma-separated subset of {ALL_ITERS}, or 'all'.",
    )
    p.add_argument(
        "--skip-data-load",
        action="store_true",
        help="Reuse ./db/images.lance if present; skip Hugging Face download.",
    )
    p.add_argument(
        "--skip-preproc",
        action="store_true",
        help="Assume image_rgb column already exists (don't re-run CPU preproc).",
    )
    p.add_argument(
        "--data-load-only",
        action="store_true",
        help=(
            "Bootstrap ./db/images.lance from Hugging Face and exit. Skips "
            "all preprocess and iteration steps. Used by the bootstrap make "
            "target so callers can build the dataset without paying the "
            "60-min image_rgb preproc."
        ),
    )
    p.add_argument(
        "--force-data-load",
        action="store_true",
        help=(
            "Overwrite ./db/images.lance even if it already exists. Without "
            "this flag, the script refuses to clobber an existing dataset "
            "(which would also destroy any preprocess columns built on top "
            "of it). Pair with --data-load-only to rebuild the bootstrap."
        ),
    )
    p.add_argument(
        "--results-json",
        default=None,
        help="Optional path to write a JSON file of {iter: elapsed_s, ...}.",
    )
    p.add_argument("-v", "--verbose", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )

    iters_requested = (
        ALL_ITERS
        if args.iters == "all"
        else tuple(i.strip() for i in args.iters.split(","))
    )
    for name in iters_requested:
        if name not in ALL_ITERS:
            print(f"Unknown iter: {name!r}. Valid: {ALL_ITERS}", file=sys.stderr)
            return 2

    # 1. Dataset.
    db_path = os.path.join(args.images_path, "db", "images.lance")
    exists = os.path.isdir(db_path)
    if args.skip_data_load and exists:
        _LOG.info("reusing existing Lance dataset at %s", db_path)
    elif exists and not args.force_data_load:
        print(
            f"ERROR: {db_path} already exists. Pass --skip-data-load to reuse "
            "it as-is, or --force-data-load to overwrite. Refusing to silently "
            "rebuild because that destroys any preprocess columns "
            "(e.g. image_rgb) layered on top of it.",
            file=sys.stderr,
        )
        return 4
    else:
        if exists:
            _LOG.warning(
                "--force-data-load: overwriting existing dataset at %s", db_path
            )
        write_lance_dataset(args.images_path, args.num_images, args.rows_per_fragment)

    if args.data_load_only:
        _LOG.info("--data-load-only set; exiting after dataset bootstrap")
        return 0

    c = geneva.connect(os.path.join(args.images_path, "db"))
    t = c.open_table("images")
    n_rows = t.count_rows()
    _LOG.info("opened table 'images' with %d rows", n_rows)

    # 2. Make sure image_rgb exists if any downstream iter needs it.
    timings: dict[str, float] = {}
    needs_preproc = any(name in NEEDS_IMAGE_RGB for name in iters_requested)
    if needs_preproc and not args.skip_preproc:
        timings["preproc"] = ensure_image_rgb(t)
    elif needs_preproc and not _has_column(t, "image_rgb"):
        print(
            "ERROR: --skip-preproc set but image_rgb column is missing. Drop the "
            "flag or run with at least `iter2` to build it.",
            file=sys.stderr,
        )
        return 3

    # 3. Iterations. Order is fixed to match the doc's narrative.
    for name in ALL_ITERS:
        if name not in iters_requested:
            continue
        if name == "baseline":
            timings[name] = _run_column(
                t,
                udf_cls=OpenClipEmbedScalar,
                input_cols=["image"],
                out_col="embed_scalar",
                label="baseline (scalar, batch=1)",
            )
        elif name == "iter1":
            timings[name] = _run_column(
                t,
                udf_cls=OpenClipEmbedBatched,
                input_cols=["image"],
                out_col="embed_batch64",
                label="iter 1 (array, batch=64)",
            )
        elif name == "iter2":
            timings[name] = _run_column(
                t,
                udf_cls=OpenClipEmbedFromTensor,
                input_cols=["image_rgb"],
                out_col="embed_from_tensor",
                label="iter 2b (GPU embed-from-tensor, bs=64)",
            )
        elif name == "iter2c":
            # Is iter 2b compute-bound or feed-bound? Run the same UDF at
            # checkpoint_size=256 and compare. If img/s climbs, the GPU has
            # batch headroom and multi-stream-replica scaling is worth pursuing. If it's
            # flat, we're already at the tensor-core ceiling.
            timings[name] = _run_column(
                t,
                udf_cls=OpenClipEmbedFromTensorBatch256,
                input_cols=["image_rgb"],
                out_col="embed_from_tensor_bs256",
                label="iter 2c (GPU embed-from-tensor, bs=256)",
            )
        elif name == "iter3":
            timings[name] = _run_column(
                t,
                udf_cls=OpenClipEmbedMultiStreamReplicas,
                input_cols=["image_rgb"],
                out_col="embed_multi_stream_replicas",
                label=f"iter 3 (multi-stream replicas, r{N_REPLICAS})",
            )
        elif name == "iter4a":
            timings[name] = _run_column(
                t,
                udf_cls=OpenClipEmbedFromTensorCompiled,
                input_cols=["image_rgb"],
                out_col="embed_from_tensor_compiled",
                label="iter 4a (single + compile)",
            )
        elif name == "iter4b":
            timings[name] = _run_column(
                t,
                udf_cls=OpenClipEmbedMultiStreamReplicasCompiled,
                input_cols=["image_rgb"],
                out_col="embed_multi_stream_replicas_compiled",
                label=f"iter 4b (multi-stream replicas + compile, r{N_REPLICAS})",
            )

    # 4. Summary.
    print()
    baseline = timings.get("baseline")
    header = f"{'iteration':<38} {'elapsed (s)':>12} {'img/s':>10}"
    if baseline:
        header += f" {'vs baseline':>12}"
    print(header)
    print("-" * len(header))
    for key, label in [
        ("baseline", "baseline (scalar, batch=1)"),
        ("iter1", "iter 1 (array, batch=64)"),
        ("preproc", "preproc (CPU resize + crop)"),
        ("iter2", "iter 2b (GPU embed-from-tensor, bs=64)"),
        ("iter2c", "iter 2c (GPU embed-from-tensor, bs=256)"),
        ("iter3", f"iter 3 (multi-stream replicas, r{N_REPLICAS})"),
        ("iter4a", "iter 4a (single + compile)"),
        ("iter4b", f"iter 4b (multi-stream replicas + compile, r{N_REPLICAS})"),
    ]:
        if key not in timings:
            continue
        t_sec = timings[key]
        row = f"{label:<38} {t_sec:>12.2f} {n_rows / t_sec:>10.1f}"
        if baseline:
            row += f" {baseline / t_sec:>11.1f}×"
        print(row)

    if args.results_json:
        with open(args.results_json, "w") as f:
            json.dump(
                {"n_rows": n_rows, "timings_s": timings}, f, indent=2, sort_keys=True
            )
        _LOG.info("wrote results to %s", args.results_json)

    try:
        import ray

        ray.shutdown()
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
