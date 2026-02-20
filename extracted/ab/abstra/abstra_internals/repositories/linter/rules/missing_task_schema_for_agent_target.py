from typing import List

from abstra_internals.repositories.linter.models import (
    LinterIssue,
    LinterRule,
)
from abstra_internals.repositories.project.project import (
    LocalProjectRepository,
)


class MissingTaskSchemaIssue(LinterIssue):
    def __init__(self, agent_title: str, target_title: str) -> None:
        self.label = (
            f'Agent "{agent_title}" sends tasks to "{target_title}", '
            f"but that stage has no task_schema defined. "
            f"Without a task_schema the agent won't know what parameters to send."
        )
        self.fixes = []


class MissingTaskSchemaForAgentTarget(LinterRule):
    label = "Agent target stages should have task_schema defined"
    type = "warning"

    def find_issues(self) -> List[LinterIssue]:
        project = LocalProjectRepository().load()
        issues = []

        for agent in project.agents:
            for transition in agent.workflow_transitions:
                target = project.get_stage(transition.target_id)
                if target is None:
                    continue
                task_schema = getattr(target, "task_schema", None)
                if not task_schema:
                    issues.append(MissingTaskSchemaIssue(agent.title, target.title))

        return issues
