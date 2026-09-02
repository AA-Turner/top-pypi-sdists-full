"""Backward-compatible re-exports for flowtask.components.Workday (TASK-105 / FEAT-026).

All operational logic now lives under flowtask.interfaces.workday/.
This package keeps the same public surface (G6).
"""

from .workday import Workday

# Models (moved to flowtask.interfaces.workday.models in TASK-102)
from flowtask.interfaces.workday.models import (
    Worker, TimeBlock, Location, TimeRequest, Organization,
    CostCenter, Applicant, Candidate, JobRequisition, JobPosting,
    JobPostingSite, TimeOffBalance, CustomPunchFieldReportEntry,
    WorkerGroup, WorkdayReference,
)

# Handler types (moved to flowtask.interfaces.workday.handlers in TASK-104)
from flowtask.interfaces.workday.handlers import (
    WorkerType, TimeBlockType, LocationType, TimeRequestType, OrganizationType,
    CostCenterType, ApplicantType, CandidateType, JobRequisitionType, JobPostingType,
    JobPostingSiteType, TimeOffBalanceType, TimeBlockReportType, CustomReportType,
    CustomPunchFieldReportType, CustomPunchFieldReportRestType,
    RecruitingAgencyUsersType, ReferencesType,
)

# Service and config
from flowtask.interfaces.workday.service import WorkdayService
from flowtask.interfaces.workday.config import WorkdayConfig

__all__ = [
    "Workday",
    "Worker", "TimeBlock", "Location", "TimeRequest", "Organization",
    "CostCenter", "Applicant", "Candidate", "JobRequisition", "JobPosting",
    "JobPostingSite", "TimeOffBalance", "CustomPunchFieldReportEntry",
    "WorkerGroup", "WorkdayReference",
    "WorkerType", "TimeBlockType", "LocationType", "TimeRequestType",
    "OrganizationType", "CostCenterType", "ApplicantType", "CandidateType",
    "JobRequisitionType", "JobPostingType", "JobPostingSiteType",
    "TimeOffBalanceType", "TimeBlockReportType", "CustomReportType",
    "CustomPunchFieldReportType", "CustomPunchFieldReportRestType",
    "RecruitingAgencyUsersType", "ReferencesType",
    "WorkdayService", "WorkdayConfig",
]
