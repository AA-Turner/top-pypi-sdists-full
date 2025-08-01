# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from functools import cached_property

from contrast.agent.protect.rule.mode import Mode


class ProtectRule:
    def __init__(self, protect_rule_json: dict | None):
        self._raw_rule = protect_rule_json or {}

    @cached_property
    def id(self) -> str:
        return self._raw_rule.get("id", "")

    @cached_property
    def mode(self) -> Mode:
        raw_mode = self._raw_rule.get("mode", "OFF")
        raw_block_at_entry = self._raw_rule.get("blockAtEntry", False)

        # Common configuration uses lower case infinitives whereas TeamServer UI uses
        # capital present participles. This mapping has to handle both.
        return {
            "MONITOR": Mode.MONITOR,
            "MONITORING": Mode.MONITOR,
            "BLOCK": Mode.BLOCK,
            "BLOCKING": (Mode.BLOCK_AT_PERIMETER if raw_block_at_entry else Mode.BLOCK),
            "BLOCK_AT_PERIMETER": Mode.BLOCK_AT_PERIMETER,
            "OFF": Mode.OFF,
        }[raw_mode.upper()]
