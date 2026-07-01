from typing import List

from abstra_internals.repositories.linter.context import (
    LintContext,
    current_lint_context,
)
from abstra_internals.repositories.linter.models import (
    LinterIssue,
    LinterRule,
)
from abstra_internals.utils.cron import cron_schedule_error


class InvalidJobScheduleFound(LinterIssue):
    def __init__(self, job_title: str, schedule: str, reason: str) -> None:
        self.label = f'The job entitled {job_title} has an invalid schedule "{schedule}" because {reason}'
        self.fixes = []


class JobScheduleValidity(LinterRule):
    label = "Job schedules must be valid cron expressions"
    type = "error"
    fix_with_ai = True

    def find_issues(self) -> List[LinterIssue]:
        project = (current_lint_context() or LintContext()).project
        issues: List[LinterIssue] = []
        for job in project.jobs:
            reason = cron_schedule_error(job.schedule)
            if reason is not None:
                issues.append(
                    InvalidJobScheduleFound(
                        job_title=job.title,
                        schedule=job.schedule,
                        reason=reason,
                    )
                )
        return issues
