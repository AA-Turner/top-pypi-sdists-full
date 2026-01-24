from snowflake.core.network_rule import NetworkRule


test_network_rule_template = NetworkRule(
    name="to_be_set",
    type="HOST_PORT",
    mode="EGRESS",
    value_list=["example.com:443", "api.example.com:443"],
    comment="Test network rule",
)

test_network_rule_minimal_template = NetworkRule(
    name="to_be_set",
    type="IPv4",
)
