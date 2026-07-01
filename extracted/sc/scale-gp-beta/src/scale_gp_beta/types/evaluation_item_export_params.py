# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .export_format import ExportFormat
from .export_method import ExportMethod

__all__ = ["EvaluationItemExportParams"]


class EvaluationItemExportParams(TypedDict, total=False):
    evaluation_id: Required[str]
    """The ID of the evaluation to export items from."""

    export_format: ExportFormat
    """The format of the exported evaluation items.

    `json` returns a single JSON array, while `jsonl` returns one JSON object per
    line.
    """

    export_method: ExportMethod
    """The method for exporting evaluation items.

    `signed_url` returns a pre-signed URL, while `direct` returns the raw content.
    """

    include_archived: bool
    """If true, include archived evaluation items in the export."""
