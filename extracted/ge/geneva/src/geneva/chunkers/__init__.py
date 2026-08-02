# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Built-in chunkers: scalar UDTFs that split one input row into many output
rows (1:N expansion), e.g. splitting a video or audio file into fixed-length
clips. See :func:`geneva.chunker`."""

from geneva.chunkers.audio import chunk_audio_udtf
from geneva.chunkers.video import chunk_video_udtf

__all__ = [
    "chunk_audio_udtf",
    "chunk_video_udtf",
]
