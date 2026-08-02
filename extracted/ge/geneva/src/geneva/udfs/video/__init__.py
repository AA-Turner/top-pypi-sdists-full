# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Video-focused pre-built UDFs."""

from geneva.udfs.video.frame_extractor import ExtractFirstFrame
from geneva.udfs.video.vjepa2_embedding import VideoEmbedding

__all__ = ["ExtractFirstFrame", "VideoEmbedding"]
