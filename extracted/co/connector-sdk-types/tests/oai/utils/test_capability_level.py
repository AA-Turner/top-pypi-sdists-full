from connector_sdk_types.generated.capability_levels import CAPABILITY_LEVELS
from connector_sdk_types.oai.utils import get_capability_level_from_name


class TestCapabilityLevels:
    def test_dict_is_non_empty(self):
        assert len(CAPABILITY_LEVELS) > 0, "capability_levels.py was not generated or is empty"

    def test_all_values_are_valid(self):
        invalid = {k: v for k, v in CAPABILITY_LEVELS.items() if v not in {"read", "write"}}
        assert not invalid, f"Unexpected level values (should be normalized by codegen): {invalid}"

    def test_known_write_capabilities(self):
        write_caps = [
            "assign_entitlement",
            "unassign_entitlement",
            "create_account",
            "delete_account",
            "activate_account",
            "deactivate_account",
            "transfer_data",
            "release_resources",
        ]
        for cap in write_caps:
            assert CAPABILITY_LEVELS[cap] == "write", f"{cap} should be write"

    def test_known_read_capabilities(self):
        read_caps = [
            "list_accounts",
            "list_entitlements",
            "list_resources",
            "find_entitlement_associations",
            "get_last_activity",
            "validate_credentials",
        ]
        for cap in read_caps:
            assert CAPABILITY_LEVELS[cap] == "read", f"{cap} should be read"

    def test_validation_level_normalized_to_read(self):
        assert CAPABILITY_LEVELS["validate_credential_config"] == "read"


class TestGetCapabilityLevelFromName:
    def test_write_capability(self):
        assert get_capability_level_from_name("assign_entitlement") == "write"

    def test_read_capability(self):
        assert get_capability_level_from_name("list_accounts") == "read"

    def test_unknown_capability_defaults_to_write(self):
        assert get_capability_level_from_name("some_custom_capability") == "write"

    def test_return_type_is_literal(self):
        result = get_capability_level_from_name("list_accounts")
        assert result in {"read", "write"}
