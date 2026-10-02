# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo

__all__ = ["UsageListParams"]


class UsageListParams(TypedDict, total=False):
    ending_at: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]
    """
    End of the time range as an ISO 8601 date-time with timezone, for example
    2026-04-08T18:56:46Z
    """

    starting_at: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]
    """
    Start of the time range as an ISO 8601 date-time with timezone, for example
    2026-04-08T18:56:46Z
    """

    window_size: Required[Literal["HOUR", "DAY"]]
    """Time window size.

    HOUR supports up to 31 days per query; DAY supports up to 365 days per query.
    """

    applications: Annotated[
        Union[
            Literal[
                "structure_and_binding",
                "small_molecule_design",
                "small_molecule_library_screen",
                "protein_design",
                "protein_redesign",
                "protein_library_screen",
                "adme",
            ],
            List[
                Literal[
                    "structure_and_binding",
                    "small_molecule_design",
                    "small_molecule_library_screen",
                    "protein_design",
                    "protein_redesign",
                    "protein_library_screen",
                    "adme",
                ]
            ],
        ],
        PropertyInfo(alias="applications[]"),
    ]
    """Filter to specific applications"""

    group_by: Annotated[
        Union[Literal["workspace_id", "application"], List[Literal["workspace_id", "application"]]],
        PropertyInfo(alias="group_by[]"),
    ]
    """Group results by workspace_id and/or application"""

    limit: int
    """Maximum number of buckets to return"""

    page: str
    """Cursor for pagination"""

    workspace_ids: Annotated[Union[str, SequenceNotStr[str]], PropertyInfo(alias="workspace_ids[]")]
    """Filter to specific workspace IDs"""
