# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Vision UDFs for object detection and image classification."""

from geneva.udfs.vision.object_detection import ObjectDetector
from geneva.udfs.vision.scene_classification import ZeroShotClassifier

__all__ = [
    "ObjectDetector",
    "ZeroShotClassifier",
]
