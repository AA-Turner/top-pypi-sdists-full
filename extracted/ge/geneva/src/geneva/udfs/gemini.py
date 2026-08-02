# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Compatibility shim for ``geneva.udfs.gemini``."""

from geneva.udfs.text.gemini import (
    KNOWN_GEMINI_MODELS,
    _gemini_retry,
    _GeminiModel,
    gemini_udf,
)

__all__ = [
    "KNOWN_GEMINI_MODELS",
    "gemini_udf",
    "_GeminiModel",
    "_gemini_retry",
]
