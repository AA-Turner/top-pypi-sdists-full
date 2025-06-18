from __future__ import annotations

import re
from typing import List, NamedTuple, Set

from evergreen_lint.model import LintError, Rule


class TagConfig(NamedTuple):
    task_tag_name: str
    allowed_distro_regex: str


class EnforceTasksDistroWithSpecialTagConfig(NamedTuple):
    tags: List[TagConfig]

    @classmethod
    def from_config_dict(cls, config_dict) -> EnforceTasksDistroWithSpecialTagConfig:
        return cls(tags=[TagConfig(**tag_config) for tag_config in config_dict.get("tags", [])])


class EnforceTasksDistroWithSpecialTag(Rule):
    """
    Ensure tasks with special tags only run on allowed distros.

    The configuration example:

    ```
    - rule: "enforce-tasks-distro-with-special-tag"
      tags:
        - task_tag_name: "requires_large_host"
          allowed_distro_regex: "(.*-xxlarge|.*-xlarge|.*-large|.*-medium|macos-.*)"
    ```
    """

    @staticmethod
    def name() -> str:
        return "enforce-tasks-distro-with-special-tag"

    @staticmethod
    def defaults() -> dict:
        return {"tags": []}

    def _get_tasks_with_tag(self, yaml: dict, tag_name: str) -> Set[str]:
        """Find all tasks that have the specified tag."""
        tagged_tasks = set()
        for task in yaml.get("tasks", []):
            if tag_name in task.get("tags", []):
                tagged_tasks.add(task["name"])
        return tagged_tasks

    def _check_distro_requirements(self, distros: List[str], allowed_distro_regex: str) -> bool:
        """Check if any of the distros match the allowed pattern."""
        pattern = re.compile(allowed_distro_regex)
        return any(pattern.match(distro) for distro in distros)

    def __call__(self, config: dict, yaml: dict) -> List[LintError]:
        failed_checks = []
        rule_config = EnforceTasksDistroWithSpecialTagConfig.from_config_dict(config)

        for tag_config in rule_config.tags:
            # Find all tasks with the special tag
            tagged_tasks = self._get_tasks_with_tag(yaml, tag_config.task_tag_name)

            # Check each buildvariant
            for variant in yaml.get("buildvariants", []):
                variant_name = variant["name"]
                variant_distros = variant.get("run_on", [])

                # Check each task in the variant
                for task in variant.get("tasks", []):
                    task_name = task["name"]
                    if task_name not in tagged_tasks:
                        continue

                    # Get task-specific run_on if it exists, otherwise use variant's run_on
                    task_distros = task.get("run_on", variant_distros)

                    if not self._check_distro_requirements(
                        task_distros, tag_config.allowed_distro_regex
                    ):
                        failed_checks.append(
                            f"Task '{task_name}' in variant '{variant_name}' is tagged with"
                            f" '{tag_config.task_tag_name}' but is set to run on incompatible"
                            f" distros: {task_distros}. It should run on a bigger host"
                        )
        return failed_checks
