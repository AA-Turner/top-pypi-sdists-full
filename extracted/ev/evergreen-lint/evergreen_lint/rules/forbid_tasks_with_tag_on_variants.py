from __future__ import annotations

from typing import List, NamedTuple, Optional, Set

from evergreen_lint.model import LintError, Rule


class TagConfig(NamedTuple):
    variant_tag_name: str  # Tag name for the buildvariant
    forbidden_task_tag: str  # Tag name for tasks that should be forbidden
    ignored_tasks: Optional[
        List[str]
    ] = None  # Optional list of task names to be ignored by this rule


class ForbidTasksWithTagOnVariantsConfig(NamedTuple):
    tags: List[TagConfig]

    @classmethod
    def from_config_dict(cls, config_dict) -> ForbidTasksWithTagOnVariantsConfig:
        return cls(tags=[TagConfig(**tag_config) for tag_config in config_dict.get("tags", [])])


class ForbidTasksWithTagOnVariants(Rule):
    """
    Forbid tasks with specific tags from being used in buildvariants with certain tags.

    The configuration example:

    ```
    - rule: "forbid-tasks-with-tag-on-variants"
      tags:
        - variant_tag_name: "no_task_tag_experimental"
          forbidden_task_tag: "experimental"
          ignored_tasks: []
        - variant_tag_name: "no_task_tag_release_critical"
          forbidden_task_tag: "release_critical"
          ignored_tasks: []
    ```
    """

    @staticmethod
    def name() -> str:
        return "forbid-tasks-with-tag-on-variants"

    @staticmethod
    def defaults() -> dict:
        return {"tags": []}

    @staticmethod
    def _get_variant_tasks(variant: dict) -> Set[str]:
        # Extract task names from a variant
        return {task["name"] for task in variant.get("tasks", [])}

    def __call__(self, config: dict, yaml: dict) -> List[LintError]:
        failed_checks = []
        rule_config = ForbidTasksWithTagOnVariantsConfig.from_config_dict(config)
        for tag_config in rule_config.tags:
            forbidden_tasks: Set[str] = set()
            # Identify tasks with the forbidden tag
            for task in yaml.get("tasks", []):
                if tag_config.forbidden_task_tag in task.get("tags", []):
                    forbidden_tasks.add(task["name"])

            # Check each buildvariant
            for variant in yaml.get("buildvariants", []):
                variant_name = variant["name"]
                variant_tags = set(variant.get("tags", []))

                if tag_config.variant_tag_name not in variant_tags:
                    continue

                variant_tasks = self._get_variant_tasks(variant)

                # Check each task in the variant
                for task_name in variant_tasks:
                    if task_name in forbidden_tasks and (
                        tag_config.ignored_tasks is None
                        or task_name not in tag_config.ignored_tasks
                    ):
                        failed_checks.append(
                            f"Task '{task_name}' is tagged with '{tag_config.forbidden_task_tag}' and therefore should be removed from '{variant_name}' build variant, because the build variant is tagged with '{tag_config.variant_tag_name}'"
                        )

        return failed_checks
