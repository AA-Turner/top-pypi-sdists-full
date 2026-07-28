from typing import List

from abstra_internals.repositories.linter.models import (
    LinterIssue,
    LinterRule,
)


class MissingTaskSchemaForAgentTarget(LinterRule):
    label = "Agent target stages should have task_schema defined"

    def find_issues(self) -> List[LinterIssue]:
        # Agents are now scripts (migration 018), so this rule no longer applies.
        return []
