# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from functools import cached_property

from contrast.reporting.teamserver_responses.protect_rule import ProtectRule


class ApplicationSettings:
    """
    This class is responsible for safely parsing V1 TeamServer Application Settings from a response to a usable format.
    The format can be found here: https://github.com/Contrast-Security-Inc/contrast-agent-api-spec. At the time of the
    creation of this class, the specific schema is ApplicationSettings in agent-endpoints.yml.
    """

    def __init__(self, application_settings_json: dict | None = None):
        self.application_settings_json = application_settings_json or {}

    @cached_property
    def disabled_assess_rules(self) -> list[str]:
        return [
            rule_name
            for rule_name, rule_details in self.application_settings_json.get(
                "assess", {}
            ).items()
            if not rule_details.get("enable", False)
        ]

    @cached_property
    def protect_rules(self) -> list[ProtectRule]:
        return [
            ProtectRule({"id": name, **value})
            for name, value in self.application_settings_json.get("protect", {})
            .get("rules", {})
            .items()
            if value
        ]

    @cached_property
    def sensitive_data_masking_policy(self) -> dict:
        return self.application_settings_json.get("sensitive_data_masking_policy", {})

    @cached_property
    def session_id(self) -> str | None:
        return self.application_settings_json.get("session_id", None)

    def common_config(self):
        ts_exclusions = self.application_settings_json.get("exclusions", {})
        return {
            "application.sensitive_data_masking_policy.mask_attack_vector": self.sensitive_data_masking_policy.get(
                "mask_attack_vector"
            ),
            "application.sensitive_data_masking_policy.mask_http_body": self.sensitive_data_masking_policy.get(
                "mask_http_body"
            ),
            "application.sensitive_data_masking_policy.rules": self.sensitive_data_masking_policy.get(
                "rules", []
            ),
            "application.url_exclusions": ts_exclusions.get("url", []),
            "application.input_exclusions": [
                {
                    # there's a hiccup in the API where "name" was repurposed for input exclusions
                    "modes": exclusion.get("modes", []),
                    "urls": exclusion.get("urls", []),
                    "match_strategy": exclusion.get("match_strategy", ""),
                    "assess_rules": exclusion.get("assess_rules", []),
                    "protect_rules": exclusion.get("protect_rules", []),
                    "input_type": exclusion.get("type", ""),
                    # there's a hiccup in the API where "name" was repurposed for input exclusions
                    "input_name": exclusion.get("name", ""),
                }
                for exclusion in ts_exclusions.get("input", [])
            ],
        }
