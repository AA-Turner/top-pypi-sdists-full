"""Submission packaging — bundle the artifacts a 3PAO needs.

`efterlev submission package` writes a single archive (zip by default)
containing every artifact a 3PAO would want to see plus a README
explaining what's inside. The customer hands the zip to their 3PAO
instead of trying to figure out which of the files under `.efterlev/`
matter.

Pure deterministic: reads existing artifacts; no LLM call.
"""

from __future__ import annotations

from efterlev.primitives.submission.package import (
    SubmissionManifest,
    SubmissionResult,
    build_submission,
)

__all__ = [
    "SubmissionManifest",
    "SubmissionResult",
    "build_submission",
]
