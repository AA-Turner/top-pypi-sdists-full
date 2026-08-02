# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Collection of built-in User Defined Table Functions provided by Geneva."""

from geneva.udtfs.image_dedup import (
    DEDUP_OUTPUT_SCHEMA,
    EDGE_SCHEMA,
    dedupe_clustering_udtf,
    edge_detection_udtf,
)

__all__ = [
    "DEDUP_OUTPUT_SCHEMA",
    "EDGE_SCHEMA",
    "dedupe_clustering_udtf",
    "edge_detection_udtf",
]
