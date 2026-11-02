# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.providers.hardcoded_value_rule import (
    HardcodedValueRule,
)


class HardcodedKey(HardcodedValueRule):
    # These are names, determined by the security team, that indicate a field
    # is likely to be a password or secret token of some sort.
    KEY_FIELD_NAMES = ["KEY", "AES", "DES", "IV", "SECRET"]

    # These are markers whose presence indicates that a field is more
    # likely to be a descriptor or requirement than an actual key.
    # We should ignore fields that contain them.
    NON_KEY_NAMES = ["CONTENT_CODES", "RESPONSE_CODES", "DIV", "SCHEMA"]

    @property
    def name(self):
        return "hardcoded-key"

    def is_name_valid(self, constant):
        constant_name_matches_denylisted_value = any(
            self.fuzzy_match(constant, self.KEY_FIELD_NAMES)
        )
        constant_name_matches_allowlisted_value = any(
            self.fuzzy_match(constant, self.NON_KEY_NAMES)
        )
        return (
            not constant_name_matches_denylisted_value
            or constant_name_matches_allowlisted_value
        )
