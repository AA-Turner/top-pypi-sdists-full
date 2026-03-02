"""Extract subtasks from PR descriptions."""

import re
from typing import Optional

from ...core.models import PullRequestEntity, TaskEntity
from ...utils.logger import log


class TaskExtractor:
    """Extracts subtasks from PR descriptions (markdown checkboxes)."""

    # Pattern to match markdown checkboxes: - [ ] or - [x] or * [ ] etc.
    CHECKBOX_PATTERN = re.compile(
        r"^[\s]*[-*]\s*\[([ xX])\]\s*(.+?)$",
        re.MULTILINE
    )

    def extract_tasks(self, pr: PullRequestEntity) -> list[TaskEntity]:
        """Extract tasks from a PR description.

        Args:
            pr: PullRequestEntity with description

        Returns:
            List of TaskEntity objects extracted from checkboxes
        """
        if not pr.description:
            return []

        tasks = []
        matches = self.CHECKBOX_PATTERN.findall(pr.description)

        for index, (checkbox, description) in enumerate(matches):
            is_completed = checkbox.lower() == "x"
            description = description.strip()

            # Skip empty descriptions
            if not description:
                continue

            task = TaskEntity(
                id=f"pr_{pr.number}_task_{index}",
                pr_number=pr.number,
                description=description,
                is_completed=is_completed,
                order=index,
            )
            tasks.append(task)

        if tasks:
            log.debug(f"Extracted {len(tasks)} tasks from PR #{pr.number}")

        return tasks

    def extract_tasks_from_prs(
        self,
        prs: list[PullRequestEntity],
    ) -> list[TaskEntity]:
        """Extract tasks from multiple PRs.

        Args:
            prs: List of PullRequestEntity objects

        Returns:
            List of all TaskEntity objects from all PRs
        """
        all_tasks = []

        for pr in prs:
            tasks = self.extract_tasks(pr)
            all_tasks.extend(tasks)

        log.info(f"Extracted {len(all_tasks)} tasks from {len(prs)} PRs")
        return all_tasks


def extract_task_summary(description: str) -> Optional[str]:
    """Extract a summary from a task description.

    Useful for getting a short version of long task descriptions.

    Args:
        description: Full task description

    Returns:
        Shortened summary (first sentence or first N chars)
    """
    if not description:
        return None

    # Get first sentence
    first_sentence = description.split(".")[0].strip()

    # If still too long, truncate
    max_length = 100
    if len(first_sentence) > max_length:
        return first_sentence[:max_length - 3] + "..."

    return first_sentence
