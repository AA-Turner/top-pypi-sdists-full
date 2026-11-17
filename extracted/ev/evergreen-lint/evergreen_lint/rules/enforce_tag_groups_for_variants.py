from __future__ import annotations

from typing import List, NamedTuple, cast

from evergreen_lint.model import LintError, Rule
from evergreen_lint.rules.tag_groups import TagGroupsConfig, check_tag_groups


class EnforceTagGroupsForVariantsConfig(NamedTuple):
    tag_groups: List[TagGroupsConfig]

    @classmethod
    def from_config_dict(cls, config_dict) -> EnforceTagGroupsForVariantsConfig:
        return cls(
            tag_groups=[
                TagGroupsConfig(**tag_group_config)
                for tag_group_config in config_dict.get("tag_groups")
            ]
        )


class EnforceTagGroupsForVariants(Rule):
    """
    Enforce tag groups in build variant definitions.

    This is the build variant counterpart of `enforce-tags-for-tasks`. Unlike
    `enforce-tags-for-variants`, which requires a tag based on the variant name, this rule
    looks only at the tags a variant already has.

    The configuration example:

    ```
    - rule: "enforce-tag-groups-for-variants"
      tag_groups:
        - group_name: "tag_group_name"
          # the rule will fail, if tag matches the regex and do not match any tag from `tag_list`
          tag_regex: required_tag_.+
          tag_list:
            - required_tag_test_1
            - required_tag_test_2
            - required_tag_test_3
          # the rule will fail, if the number of tags is less than `min_num_of_tags`
          # or more than `max_num_of_tags`
          min_num_of_tags: 1
          max_num_of_tags: 1
    ```

    """

    @staticmethod
    def name() -> str:
        return "enforce-tag-groups-for-variants"

    @staticmethod
    def defaults() -> dict:
        return {"tag_groups": []}

    def __call__(self, config: dict, yaml: dict) -> List[LintError]:
        failed_checks: List[LintError] = []
        rule_config = EnforceTagGroupsForVariantsConfig.from_config_dict(config)

        for variant_def in cast(List, yaml.get("buildvariants", [])):
            failed_checks.extend(
                check_tag_groups(
                    "build variant",
                    variant_def["name"],
                    variant_def.get("tags"),
                    rule_config.tag_groups,
                )
            )

        return failed_checks
