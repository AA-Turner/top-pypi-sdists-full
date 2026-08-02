# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Unit tests for vision UDFs (ObjectDetector, ZeroShotClassifier).

These tests validate UDF registration, metadata, argument types, and
struct output without downloading models (no GPU required).
"""

import pyarrow as pa
import pytest

from geneva.transformer import UDF, UDFArgType


class TestObjectDetector:
    """Tests for the ObjectDetector batched UDF."""

    def test_udf_instance(self) -> None:
        from geneva.udfs.vision.object_detection import ObjectDetector

        assert isinstance(ObjectDetector(), UDF)

    def test_arg_type_is_array(self) -> None:
        from geneva.udfs.vision.object_detection import ObjectDetector

        assert ObjectDetector().arg_type is UDFArgType.ARRAY

    def test_data_type_is_struct(self) -> None:
        from geneva.udfs.vision.object_detection import (
            DETECTION_TYPE,
            ObjectDetector,
        )

        assert ObjectDetector().data_type == DETECTION_TYPE

    def test_input_columns(self) -> None:
        from geneva.udfs.vision.object_detection import ObjectDetector

        assert ObjectDetector().input_columns == ["image"]

    def test_checkpoint_size(self) -> None:
        from geneva.udfs.vision.object_detection import ObjectDetector

        assert ObjectDetector().batch_size == 32

    def test_detection_type_schema(self) -> None:
        from geneva.udfs.vision.object_detection import DETECTION_TYPE

        expected = pa.struct(
            [
                ("label", pa.string()),
                ("confidence", pa.float32()),
                ("bbox_area_pct", pa.float32()),
            ]
        )
        assert expected == DETECTION_TYPE

    def test_default_queries(self) -> None:
        from geneva.udfs.vision.object_detection import ObjectDetector

        udf = ObjectDetector()
        assert udf.func.queries == ["object"]  # type: ignore[union-attr]

    def test_custom_queries(self) -> None:
        from geneva.udfs.vision.object_detection import ObjectDetector

        queries = ["ambulance", "fire truck"]
        udf = ObjectDetector(queries=queries)
        assert udf.func.queries == queries  # type: ignore[union-attr]

    def test_call_with_all_none_returns_defaults(self) -> None:
        """When all inputs are None, should return none_result."""
        # __call__ lazy-imports torch even for an all-null fast path; skip
        # cleanly on lean installs where torch isn't available.
        pytest.importorskip("torch")
        from geneva.udfs.vision.object_detection import (
            DETECTION_TYPE,
            ObjectDetector,
        )

        udf = ObjectDetector()
        udf.func.processor = "sentinel"  # type: ignore[union-attr]
        images = pa.array([None, None], type=pa.binary())
        result = udf.func(images)  # type: ignore[misc]

        assert isinstance(result, pa.Array)
        assert len(result) == 2
        assert result.type == DETECTION_TYPE
        for i in range(2):
            row = result[i].as_py()
            assert row["label"] == "none"
            assert row["confidence"] == 0.0
            assert row["bbox_area_pct"] == 0.0


class TestZeroShotClassifier:
    """Tests for the ZeroShotClassifier batched UDF."""

    def test_udf_instance(self) -> None:
        from geneva.udfs.vision.scene_classification import (
            ZeroShotClassifier,
        )

        assert isinstance(ZeroShotClassifier(), UDF)

    def test_arg_type_is_array(self) -> None:
        from geneva.udfs.vision.scene_classification import (
            ZeroShotClassifier,
        )

        assert ZeroShotClassifier().arg_type is UDFArgType.ARRAY

    def test_data_type_is_struct(self) -> None:
        from geneva.udfs.vision.scene_classification import (
            CLASSIFICATION_TYPE,
            ZeroShotClassifier,
        )

        assert ZeroShotClassifier().data_type == CLASSIFICATION_TYPE

    def test_input_columns(self) -> None:
        from geneva.udfs.vision.scene_classification import (
            ZeroShotClassifier,
        )

        assert ZeroShotClassifier().input_columns == ["image"]

    def test_checkpoint_size(self) -> None:
        from geneva.udfs.vision.scene_classification import (
            ZeroShotClassifier,
        )

        assert ZeroShotClassifier().batch_size == 64

    def test_classification_type_schema(self) -> None:
        from geneva.udfs.vision.scene_classification import (
            CLASSIFICATION_TYPE,
        )

        expected = pa.struct(
            [
                ("top_label", pa.string()),
                ("top_score", pa.float32()),
            ]
        )
        assert expected == CLASSIFICATION_TYPE

    def test_default_labels(self) -> None:
        from geneva.udfs.vision.scene_classification import (
            ZeroShotClassifier,
        )

        udf = ZeroShotClassifier()
        assert udf.func.labels == ["object"]  # type: ignore[union-attr]

    def test_custom_labels(self) -> None:
        from geneva.udfs.vision.scene_classification import (
            ZeroShotClassifier,
        )

        labels = ["highway", "bridge"]
        udf = ZeroShotClassifier(labels=labels)
        assert udf.func.labels == labels  # type: ignore[union-attr]

    def test_call_with_all_none_returns_defaults(self) -> None:
        """When all inputs are None, should return none_result."""
        pytest.importorskip("torch")
        from geneva.udfs.vision.scene_classification import (
            CLASSIFICATION_TYPE,
            ZeroShotClassifier,
        )

        udf = ZeroShotClassifier()
        udf.func.processor = "sentinel"  # type: ignore[union-attr]
        images = pa.array([None, None], type=pa.binary())
        result = udf.func(images)  # type: ignore[misc]

        assert isinstance(result, pa.Array)
        assert len(result) == 2
        assert result.type == CLASSIFICATION_TYPE
        for i in range(2):
            row = result[i].as_py()
            assert row["top_label"] == "unknown"
            assert row["top_score"] == 0.0
