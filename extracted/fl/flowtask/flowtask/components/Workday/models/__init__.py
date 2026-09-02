"""Backward-compatibility shim — re-exports from the new interface home.

Models moved to flowtask.interfaces.workday.models in TASK-102.
Full shims created in TASK-105.
"""
from flowtask.interfaces.workday.models import (
    TimeBlock, Location, Worker, TimeRequest, Organization, CostCenter,
    Applicant, Candidate, JobRequisition, JobPosting, JobPostingSite,
    TimeOffBalance, CustomPunchFieldReportEntry, WorkerGroup, WorkdayReference,
)

__all__ = [
    "TimeBlock", "Location", "Worker", "TimeRequest", "Organization",
    "CostCenter", "Applicant", "Candidate", "JobRequisition", "JobPosting",
    "JobPostingSite", "TimeOffBalance", "CustomPunchFieldReportEntry",
    "WorkerGroup", "WorkdayReference",
]
