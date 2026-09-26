# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["SubmittedListResponse", "Report", "ReportSubmitter"]


class ReportSubmitter(BaseModel):
    """Information about the submitter of the report."""

    company: Optional[str] = None

    email: Optional[str] = None

    name: Optional[str] = None

    telephone: Optional[str] = None


class Report(BaseModel):
    id: str
    """Public report code."""

    cdate: datetime
    """Time the report was submitted."""

    denial_reason: Optional[
        Literal[
            "unable_to_confirm",
            "incomplete_report",
            "not_on_cloudflare",
            "duplicate_report",
            "content_removed",
            "report_details_mismatch",
            "no_abuse_found",
            "missing_original_work",
            "direct_url_required",
            "wrong_report_category",
            "content_unavailable",
            "law_enforcement_referral_required",
            "domain_dispute_process_required",
        ]
    ] = None
    """Submitter-safe reason for a denied report. Null when unavailable."""

    domain: str
    """Domain identified in the report."""

    status: Literal["submitted", "accepted", "denied"]
    """Status visible to the account that submitted the report."""

    type: Literal["PHISH", "GEN", "THREAT", "DMCA", "EMER", "TM", "REG_WHO", "NCSEI", "NETWORK"]
    """The abuse report type"""

    submitter: Optional[ReportSubmitter] = None
    """Information about the submitter of the report."""


class SubmittedListResponse(BaseModel):
    reports: List[Report]
