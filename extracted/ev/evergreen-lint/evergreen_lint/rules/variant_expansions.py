from __future__ import annotations

import re
from typing import Any, Dict, List, NamedTuple, Optional, cast

from evergreen_lint.model import LintError, Rule


def compile_optional_regex(regex: Optional[str]) -> Optional[re.Pattern]:
    return re.compile(regex) if regex is not None else None


class VariantConfig(NamedTuple):
    name_regex: Optional[re.Pattern] = None
    display_name_regex: Optional[re.Pattern] = None
    task_presence_regex: Optional[re.Pattern] = None
    task_absense_regex: Optional[re.Pattern] = None

    @classmethod
    def from_variant_config_dict(cls, config_dict: Optional[Dict[str, Any]]) -> VariantConfig:
        if config_dict is None:
            return cls()
        return cls(
            name_regex=compile_optional_regex(config_dict.get("name_regex")),
            display_name_regex=compile_optional_regex(config_dict.get("display_name_regex")),
            task_presence_regex=compile_optional_regex(config_dict.get("task_presence_regex")),
            task_absense_regex=compile_optional_regex(config_dict.get("task_absense_regex")),
        )

    def matches_variant_definition(self, variant_definition: Dict[str, Any]) -> bool:
        checks = []
        if self.name_regex is not None:
            checks.append(self.name_regex.match(variant_definition.get("name") or "") is not None)
        if self.display_name_regex is not None:
            checks.append(
                self.display_name_regex.match(variant_definition.get("display_name") or "")
                is not None
            )
        if self.task_presence_regex is not None:
            checks.append(
                any(
                    self.task_presence_regex.match(task.get("name") or "") is not None
                    for task in variant_definition.get("tasks") or []
                )
            )
        if self.task_absense_regex is not None:
            checks.append(
                all(
                    self.task_absense_regex.match(task.get("name") or "") is None
                    for task in variant_definition.get("tasks") or []
                )
            )
        return all(checks)

    def print(self, indent: int = 2) -> str:
        output = ""
        prefix = " " * indent

        for key, value in self._asdict().items():
            if value is not None:
                output = (
                    f"{output}\n{prefix}{key}:"
                    f' "{value.pattern if isinstance(value, re.Pattern) else value}"'
                )

        return output


class ExpansionConfig(NamedTuple):
    expansion_name: str
    variant_config: VariantConfig
    expansion_value_regex: Optional[re.Pattern] = None

    @classmethod
    def from_expansion_config_dict(cls, config_dict: Dict[str, Any]) -> ExpansionConfig:
        return cls(
            expansion_name=config_dict["expansion_name"],
            expansion_value_regex=compile_optional_regex(config_dict.get("expansion_value_regex")),
            variant_config=VariantConfig.from_variant_config_dict(
                config_dict.get("variant_config")
            ),
        )


class VariantExpansionsConfig(NamedTuple):
    require_expansions: List[ExpansionConfig]
    prohibit_expansions: List[ExpansionConfig]

    @classmethod
    def from_config_dict(cls, config_dict: Dict[str, Any]) -> VariantExpansionsConfig:
        return cls(
            require_expansions=[
                ExpansionConfig.from_expansion_config_dict(expansion_config)
                for expansion_config in config_dict.get("require_expansions") or []
            ],
            prohibit_expansions=[
                ExpansionConfig.from_expansion_config_dict(expansion_config)
                for expansion_config in config_dict.get("prohibit_expansions") or []
            ],
        )


class VariantExpansions(Rule):
    """
    Validate expansions in variant definitions.

    The configuration example:

    ```
    - rule: "variant-expansions"
      require_expansions:
        - expansion_name: "require-expansion-when-task-1-runs-on-variant"
          expansion_value_regex: ".*"
          variant_config:
            name_regex: ".*"
            display_name_regex: ".*"
            task_presence_regex: "task-1"
        - expansion_name: "require-expansion-when-task-2-does-not-run-on-variant"
          expansion_value_regex: ".*"
          variant_config:
            name_regex: ".*"
            display_name_regex: ".*"
            task_absense_regex: "task-2"
      prohibit_expansions:
        - expansion_name: "prohibit-expansion-when-task-3-runs-on-variant"
          expansion_value_regex: ".*"
          variant_config:
            name_regex: ".*"
            display_name_regex: ".*"
            task_presence_regex: "task-3"
        - expansion_name: "prohibit-expansion-when-task-4-does-not-run-on-variant"
          expansion_value_regex: ".*"
          variant_config:
            name_regex: ".*"
            display_name_regex: ".*"
            task_absense_regex: "task-4"
    ```

    """

    @staticmethod
    def name() -> str:
        return "variant-expansions"

    @staticmethod
    def defaults() -> dict:
        return {"require_expansions": [], "prohibit_expansions": []}

    def __call__(self, config: dict, yaml: dict) -> List[LintError]:
        require_expansion_error_msg = (
            "Build variant expansion '{expansion_name}' should be added to '{variant}'"
            " build variant, because build variant configuration matches the following:"
            " {variant_config}"
        )
        prohibit_expansion_error_msg = (
            "Build variant expansion '{expansion_name}' should be removed from '{variant}'"
            " build variant, because build variant configuration matches the following:"
            " {variant_config}"
        )
        require_expansion_with_value_error_msg = (
            "Build variant expansion '{expansion_name}' value should match"
            " '{expansion_value_regex}' pattern on '{variant}' build variant, because"
            " build variant configuration matches the following:"
            " {variant_config}"
        )
        prohibit_expansion_with_value_error_msg = (
            "Build variant expansion '{expansion_name}' value should not match"
            " '{expansion_value_regex}' pattern on '{variant}' build variant, because"
            " build variant configuration matches the following:"
            " {variant_config}"
        )

        failed_checks = []
        rule_config = VariantExpansionsConfig.from_config_dict(config)

        for variant_def in cast(List, yaml.get("buildvariants") or []):
            variant_name = variant_def["name"]
            variant_expansions = variant_def.get("expansions") or {}

            for require_config in rule_config.require_expansions:
                if not require_config.variant_config.matches_variant_definition(variant_def):
                    continue
                expansion_to_validate = variant_expansions.get(require_config.expansion_name)
                if expansion_to_validate is None:
                    failed_checks.append(
                        require_expansion_error_msg.format(
                            expansion_name=require_config.expansion_name,
                            variant=variant_name,
                            variant_config=require_config.variant_config.print(),
                        )
                    )
                elif (
                    require_config.expansion_value_regex is not None
                    and require_config.expansion_value_regex.match(expansion_to_validate) is None
                ):
                    failed_checks.append(
                        require_expansion_with_value_error_msg.format(
                            expansion_name=require_config.expansion_name,
                            expansion_value_regex=require_config.expansion_value_regex.pattern,
                            variant=variant_name,
                            variant_config=require_config.variant_config.print(),
                        )
                    )

            for prohibit_config in rule_config.prohibit_expansions:
                if not prohibit_config.variant_config.matches_variant_definition(variant_def):
                    continue
                expansion_to_validate = variant_expansions.get(prohibit_config.expansion_name)
                if (
                    prohibit_config.expansion_value_regex is None
                    and expansion_to_validate is not None
                ):
                    failed_checks.append(
                        prohibit_expansion_error_msg.format(
                            expansion_name=prohibit_config.expansion_name,
                            variant=variant_name,
                            variant_config=prohibit_config.variant_config.print(),
                        )
                    )
                elif (
                    prohibit_config.expansion_value_regex is not None
                    and expansion_to_validate is not None
                    and prohibit_config.expansion_value_regex.match(expansion_to_validate)
                    is not None
                ):
                    failed_checks.append(
                        prohibit_expansion_with_value_error_msg.format(
                            expansion_name=prohibit_config.expansion_name,
                            expansion_value_regex=prohibit_config.expansion_value_regex.pattern,
                            variant=variant_name,
                            variant_config=prohibit_config.variant_config.print(),
                        )
                    )

        return failed_checks
