from __future__ import annotations

import re
from typing import List, NamedTuple, Optional, cast

from evergreen_lint.model import LintError, Rule


class VariantConfig(NamedTuple):
    name_regex: Optional[str] = None
    display_name_regex: Optional[str] = None

    def print(self, indent: int = 2) -> str:
        output = ""

        for key, value in self._asdict().items():
            if value is not None:
                output = f'{output}\n{" " * indent}{key}: "{value}"'

        return output


class TagConfig(NamedTuple):
    tag_name: str
    variant_config: VariantConfig


class EnforceTagsForVariantsConfig(NamedTuple):
    tags: List[TagConfig]

    @classmethod
    def from_config_dict(cls, config_dict) -> EnforceTagsForVariantsConfig:
        return cls(
            tags=[
                TagConfig(
                    tag_name=tag_config["tag_name"],
                    variant_config=VariantConfig(**tag_config["variant_config"]),
                )
                for tag_config in config_dict.get("tags")
            ]
        )


class EnforceTagsForVariants(Rule):
    """
    Enforce tags presence in variant definitions.

    The configuration example:

    ```
    - rule: "enforce-tags-for-variants"
      tags:
        # the rule will fail if the variant has matching configuration
        # and is not tagged with the tag that matches tag_name
        # and vice-versa
        - tag_name: "required"
          variant_config:
            name_regex: ".*"
            display_name_regex: "^!.+$"
    ```

    """

    @staticmethod
    def name() -> str:
        return "enforce-tags-for-variants"

    @staticmethod
    def defaults() -> dict:
        return {"tags": []}

    def __call__(self, config: dict, yaml: dict) -> List[LintError]:
        variant_is_not_tagged_error_msg = (
            "Build variant '{variant}' should be tagged with '{tag}',"
            " because build variant configuration matches the following:"
            " {variant_config}"
        )
        variant_config_not_matches_error_msg = (
            "Tag '{tag}' should be removed from build variant '{variant}'"
            " because build variant configuration does not match the following:"
            " {variant_config}"
        )

        failed_checks = []
        rule_config = EnforceTagsForVariantsConfig.from_config_dict(config)

        for variant_def in cast(List, yaml.get("buildvariants", [])):
            for cfg in rule_config.tags:
                variant_is_tagged = cfg.tag_name in variant_def.get("tags", [])

                variant_config_checks: List[bool] = []
                if cfg.variant_config.name_regex:
                    variant_config_checks.append(
                        re.match(
                            cfg.variant_config.name_regex,
                            variant_def["name"],
                        )
                        is not None
                    )
                if cfg.variant_config.display_name_regex:
                    variant_config_checks.append(
                        re.match(
                            cfg.variant_config.display_name_regex,
                            variant_def["display_name"],
                        )
                        is not None
                    )
                variant_config_matches = all(variant_config_checks)

                if variant_config_matches and not variant_is_tagged:
                    failed_checks.append(
                        variant_is_not_tagged_error_msg.format(
                            tag=cfg.tag_name,
                            variant=variant_def["name"],
                            variant_config=cfg.variant_config.print(),
                        )
                    )

                if variant_is_tagged and not variant_config_matches:
                    failed_checks.append(
                        variant_config_not_matches_error_msg.format(
                            tag=cfg.tag_name,
                            variant=variant_def["name"],
                            variant_config=cfg.variant_config.print(),
                        )
                    )

        return failed_checks
