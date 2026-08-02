# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
End-to-end test for Geneva feature engineering pipeline.

This test demonstrates a complete Geneva workflow:
1. Loading Oxford pets dataset (images of cats and dogs)
2. Running various UDF backfills:
   - file_size: scalar UDF to compute image byte size
   - dimensions: struct UDF to extract image width/height
   - embedding: vector embeddings using OpenCLIP (512-dim)
   - caption_blip: GPU-accelerated image captions using BLIP model
3. Testing incremental and async backfills
4. Vector search on embeddings
"""

import io
import logging
import time
import uuid
from collections.abc import Callable

import pyarrow as pa
import pytest

import geneva
from geneva.runners.ray.raycluster import RayCluster

_LOG = logging.getLogger(__name__)


# ============================================================================
# UDF Definitions - CPU workloads
# ============================================================================


@geneva.udf(version="0.1")
def file_size(image: bytes) -> int:
    """Compute the byte size of an image."""
    return len(image)


@geneva.udf(
    version="0.1",
    data_type=pa.struct(
        [pa.field("width", pa.int32()), pa.field("height", pa.int32())]
    ),
)
def dimensions(image: bytes) -> tuple[int, int]:
    """Extract image dimensions (width, height)."""
    from PIL import Image

    image_stream = io.BytesIO(image)
    img = Image.open(image_stream)
    return img.size


# ============================================================================
# UDF Definitions - GPU workloads
# ============================================================================


@geneva.udf(version="0.1", data_type=pa.list_(pa.float32(), 512))
class GenEmbeddings(Callable):
    """
    Generate 512-dimensional embeddings using OpenCLIP.

    This is a stateful UDF that loads the model once and reuses it.
    """

    def __init__(self) -> None:
        self.is_loaded = False

    def setup(self) -> None:
        import open_clip

        _LOG.info("Loading OpenCLIP model for embeddings")
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32", pretrained="openai"
        )
        self.model.eval()
        self.is_loaded = True

    def __call__(self, image: bytes) -> list[float]:
        import torch
        from PIL import Image

        if not self.is_loaded:
            self.setup()

        image_stream = io.BytesIO(image)
        pil_image = Image.open(image_stream).convert("RGB")
        image_tensor = self.preprocess(pil_image).unsqueeze(0)

        with torch.no_grad():
            embedding = self.model.encode_image(image_tensor)
            embedding = embedding.squeeze().cpu().numpy()

        return embedding.tolist()


@geneva.udf(cuda=True, version="0.1")
class GenCaption(Callable):
    """
    Generate image captions using BLIP model.

    This is a GPU-accelerated stateful UDF.
    """

    def __init__(self) -> None:
        self.is_loaded = False

    def setup(self) -> None:
        from transformers import BlipForConditionalGeneration, BlipProcessor

        _LOG.info("Loading BLIP model for caption generation")
        self.processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )
        self.model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

        # Move to GPU if available
        import torch

        if torch.cuda.is_available():
            self.model = self.model.to("cuda")
            _LOG.info("BLIP model loaded on GPU")
        else:
            _LOG.warning("GPU not available, BLIP model will run on CPU (slower)")

        self.is_loaded = True

    def __call__(self, image: bytes) -> str:
        import torch
        from PIL import Image

        if not self.is_loaded:
            self.setup()

        image_stream = io.BytesIO(image)
        raw_image = Image.open(image_stream).convert("RGB")

        inputs = self.processor([raw_image], return_tensors="pt")

        # Move inputs to GPU if model is on GPU
        if next(self.model.parameters()).is_cuda:
            inputs = {k: v.to("cuda") for k, v in inputs.items()}

        with torch.no_grad():
            out = self.model.generate(**inputs, max_new_tokens=50)

        caption = self.processor.decode(out[0], skip_special_tokens=True)
        return caption


# ============================================================================
# Tests - CPU workloads
# ============================================================================


def test_oxford_pets_cpu_pipeline(
    oxford_pets_table: tuple,
    standard_cluster: RayCluster,
    batch_size: int,
) -> None:
    """
    Test CPU-based feature engineering pipeline.

    This test:
    1. Uses shared Oxford pets images table
    2. Runs file_size and dimensions UDFs
    3. Validates results
    """
    conn, shared_tbl, _ = oxford_pets_table
    table_name = f"oxford_pets_{uuid.uuid4().hex}"

    _LOG.info(f"Creating working table {table_name} from shared data")

    # Create working table from shared data (avoids re-downloading)
    data = shared_tbl.to_arrow()
    tbl = conn.create_table(table_name, data, mode="overwrite")
    num_images = len(tbl)

    _LOG.info(f"Table created with {num_images} rows")
    _LOG.info(f"Initial schema: {tbl.schema}")

    with standard_cluster:
        # Add columns
        _LOG.info("Adding file_size and dimensions columns")
        tbl.add_columns({"file_size": file_size, "dimensions": dimensions})
        _LOG.info(f"Schema after add_columns: {tbl.schema}")

        # Backfill file_size
        _LOG.info("Backfilling file_size column")
        tbl.backfill("file_size", batch_size=batch_size, commit_granularity=5)
        _LOG.info("file_size backfill complete")

        # Backfill dimensions
        _LOG.info("Backfilling dimensions column")
        tbl.backfill("dimensions", batch_size=batch_size, commit_granularity=5)
        _LOG.info("dimensions backfill complete")

    # Validate results
    df = tbl.to_pandas()
    _LOG.info(f"Final table shape: {df.shape}")
    _LOG.info(f"Final schema: {tbl.schema}")

    # Assertions
    assert len(df) == num_images, f"Expected {num_images} rows, got {len(df)}"
    assert "file_size" in df.columns, "file_size column not found"
    assert "dimensions" in df.columns, "dimensions column not found"
    assert df["file_size"].notna().all(), "file_size has null values"
    assert df["dimensions"].notna().all(), "dimensions has null values"
    assert (df["file_size"] > 0).all(), "file_size should be positive"

    _LOG.info("CPU pipeline test passed!")

    # Cleanup
    conn.drop_table(table_name)


def test_oxford_pets_incremental_backfill(
    oxford_pets_table: tuple,
    standard_cluster: RayCluster,
    batch_size: int,
) -> None:
    """
    Test incremental backfill with num_frags parameter.

    This verifies that backfill can be run multiple times on subsets
    of fragments and will resume from where it left off.
    """
    conn, shared_tbl, _ = oxford_pets_table
    table_name = f"oxford_pets_incremental_{uuid.uuid4().hex}"

    _LOG.info(f"Creating working table {table_name} for incremental backfill test")

    # Create working table from shared data (avoids re-downloading)
    data = shared_tbl.to_arrow()
    tbl = conn.create_table(table_name, data, mode="overwrite")
    num_images = len(tbl)

    with standard_cluster:
        tbl.add_columns({"file_size": file_size})

        # First backfill - process only 2 fragments
        _LOG.info("Backfill 1: Processing first 2 fragments")
        tbl.backfill("file_size", batch_size=batch_size, num_frags=2)
        tbl.checkout_latest()
        df = tbl.to_pandas()
        filled_rows_1 = df["file_size"].notna().sum()
        _LOG.info(f"After backfill 1: {filled_rows_1} rows filled")

        # Second backfill - process 2 more fragments, first 2 already done.
        _LOG.info("Backfill 2: Processing next 2 fragments")
        tbl.backfill("file_size", batch_size=batch_size, num_frags=4)
        tbl.checkout_latest()
        df = tbl.to_pandas()
        filled_rows_2 = df["file_size"].notna().sum()
        _LOG.info(f"After backfill 2: {filled_rows_2} rows filled")

        # Third backfill - complete the rest
        _LOG.info("Backfill 3: Processing remaining fragments")
        tbl.backfill("file_size", batch_size=batch_size)
        tbl.checkout_latest()
        df = tbl.to_pandas()
        filled_rows_3 = df["file_size"].notna().sum()
        _LOG.info(f"After backfill 3: {filled_rows_3} rows filled")

    # Assertions
    assert filled_rows_1 > 0, "First backfill should fill some rows"
    # if there are onyl 2 or fewer fragments, filled_rows_2 will be num_images
    assert filled_rows_2 == num_images or filled_rows_2 > filled_rows_1, (
        "Second backfill should fill more rows"
    )
    assert filled_rows_3 == num_images, (
        f"Final backfill should fill all {num_images} rows"
    )
    assert df["file_size"].notna().all(), (
        "All rows should be filled after complete backfill"
    )

    _LOG.info("Incremental backfill test passed!")

    # Cleanup
    conn.drop_table(table_name)


def test_oxford_pets_async_backfill(
    oxford_pets_table: tuple,
    standard_cluster: RayCluster,
    batch_size: int,
) -> None:
    """
    Test asynchronous backfill with progress monitoring.

    This verifies that backfill_async returns a future that can be
    monitored and that intermediate commits are visible.
    """
    conn, shared_tbl, _ = oxford_pets_table
    table_name = f"oxford_pets_async_{uuid.uuid4().hex}"

    _LOG.info(f"Creating working table {table_name} for async backfill test")

    # Create working table from shared data (avoids re-downloading)
    data = shared_tbl.to_arrow()
    tbl = conn.create_table(table_name, data, mode="overwrite")
    num_images = len(tbl)

    with standard_cluster:
        tbl.add_columns({"file_size": file_size})

        _LOG.info("Starting async backfill")
        fut = tbl.backfill_async(
            "file_size", batch_size=batch_size, commit_granularity=2
        )

        # Monitor progress
        iterations = 0
        while not fut.done():
            time.sleep(2)
            tbl.checkout_latest()
            try:
                df = tbl.to_pandas()
                done_rows = df["file_size"].notna().sum()
                _LOG.info(
                    f"Async backfill in progress: {done_rows}/{num_images} rows, "
                    f"version {tbl.version}"
                )
            except Exception as e:
                _LOG.warning(f"Could not check progress: {e}")
            iterations += 1

            # Safety timeout
            if iterations > 100:
                pytest.fail("Async backfill timed out after 200 seconds")

        _LOG.info("Async backfill completed")

        # Verify final state
        tbl.checkout_latest()
        df = tbl.to_pandas()

    # Assertions
    assert df["file_size"].notna().all(), "All rows should be filled"
    assert len(df) == num_images, f"Expected {num_images} rows"

    _LOG.info("Async backfill test passed!")

    # Cleanup
    conn.drop_table(table_name)


# ============================================================================
# Tests - GPU workloads
# ============================================================================


def test_oxford_pets_embeddings(
    oxford_pets_table: tuple,
    standard_cluster: RayCluster,
    batch_size: int,
    skip_gpu: bool,
) -> None:
    """
    Test vector embedding generation using OpenCLIP.

    This test generates 512-dimensional embeddings and validates
    the output shape and values.
    """
    if skip_gpu:
        pytest.skip("GPU tests skipped (--skip-gpu)")

    conn, shared_tbl, _ = oxford_pets_table
    table_name = f"oxford_pets_embeddings_{uuid.uuid4().hex}"

    # Use smaller dataset for GPU tests (limit to 100 images)
    data = shared_tbl.to_arrow()
    test_images = min(len(data), 100)
    limited_data = data.slice(0, test_images)

    _LOG.info(
        f"Creating working table {table_name} for embedding test "
        f"with {test_images} images"
    )

    # Create working table from shared data (avoids re-downloading)
    tbl = conn.create_table(table_name, limited_data, mode="overwrite")

    with standard_cluster:
        tbl.add_columns({"embedding": GenEmbeddings()})

        _LOG.info("Backfilling embeddings")
        tbl.backfill("embedding", batch_size=batch_size, commit_granularity=2)

    # Validate results
    tbl.checkout_latest()
    df = tbl.to_pandas()

    # Assertions
    assert "embedding" in df.columns, "embedding column not found"
    assert df["embedding"].notna().all(), "embedding has null values"

    # Check embedding dimensions
    first_embedding = df["embedding"].iloc[0]
    assert len(first_embedding) == 512, (
        f"Expected 512-dim embedding, got {len(first_embedding)}"
    )

    _LOG.info("Embedding test passed!")

    # Cleanup
    conn.drop_table(table_name)


def test_oxford_pets_captions_gpu(
    oxford_pets_table: tuple,
    gpu_cluster: RayCluster,
    batch_size: int,
    skip_gpu: bool,
) -> None:
    """
    Test GPU-accelerated caption generation using BLIP.

    This test generates image captions and validates that
    they are non-empty strings.
    """
    if skip_gpu:
        pytest.skip("GPU tests skipped (--skip-gpu)")

    conn, shared_tbl, _ = oxford_pets_table
    table_name = f"oxford_pets_captions_{uuid.uuid4().hex}"

    # Use smaller dataset for GPU tests (limit to 50 images)
    data = shared_tbl.to_arrow()
    test_images = min(len(data), 50)
    limited_data = data.slice(0, test_images)

    _LOG.info(
        f"Creating working table {table_name} for caption test "
        f"with {test_images} images"
    )

    # Create working table from shared data (avoids re-downloading)
    tbl = conn.create_table(table_name, limited_data, mode="overwrite")

    with gpu_cluster:
        tbl.add_columns({"caption_blip": GenCaption()})

        _LOG.info("Backfilling captions with BLIP")
        tbl.backfill("caption_blip", batch_size=batch_size, commit_granularity=2)

    # Validate results
    tbl.checkout_latest()
    df = tbl.to_pandas()

    # Assertions
    assert "caption_blip" in df.columns, "caption_blip column not found"
    assert df["caption_blip"].notna().all(), "caption_blip has null values"

    # Check that captions are non-empty strings
    for caption in df["caption_blip"]:
        assert isinstance(caption, str), (
            f"Caption should be string, got {type(caption)}"
        )
        assert len(caption) > 0, "Caption should be non-empty"

    _LOG.info("Caption test passed!")
    _LOG.info(f"Sample captions: {df['caption_blip'].head(3).tolist()}")

    # Cleanup
    conn.drop_table(table_name)
