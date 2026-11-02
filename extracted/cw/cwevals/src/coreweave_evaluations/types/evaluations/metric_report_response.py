# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["MetricReportResponse"]


class MetricReportResponse(BaseModel):
    commit_id: int
    """Commit that recorded this report.

    An evaluation version includes these values if its last_commit_id is at least
    this commit.
    """

    evaluation_id: str
