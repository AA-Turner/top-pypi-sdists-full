"""Backward-compatibility shim — types moved to flowtask.interfaces.workday.handlers (TASK-104)."""
from flowtask.interfaces.workday.handlers import (
    WorkerType, TimeBlockType, LocationType, TimeRequestType, OrganizationType,
    CostCenterType, ApplicantType, CandidateType, JobRequisitionType, JobPostingType,
    JobPostingSiteType, TimeOffBalanceType, TimeBlockReportType, CustomReportType,
    CustomPunchFieldReportType, CustomPunchFieldReportRestType,
    RecruitingAgencyUsersType, ReferencesType,
)
from flowtask.interfaces.workday.handlers.location_hierarchy_assignments import LocationHierarchyAssignmentsType
from flowtask.interfaces.workday.handlers.organization_single import GetOrganization

__all__ = [
    "WorkerType", "TimeBlockType", "LocationType", "TimeRequestType", "OrganizationType",
    "CostCenterType", "ApplicantType", "CandidateType", "JobRequisitionType", "JobPostingType",
    "JobPostingSiteType", "TimeOffBalanceType", "TimeBlockReportType", "CustomReportType",
    "CustomPunchFieldReportType", "CustomPunchFieldReportRestType",
    "RecruitingAgencyUsersType", "ReferencesType",
    "LocationHierarchyAssignmentsType", "GetOrganization",
]
