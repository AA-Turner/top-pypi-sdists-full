import pytest as pytest

from snowflake.core.network_policy import NetworkPolicy
from tests.integ.utils import random_string


@pytest.fixture(scope='session')
def prepare_rules_for_network_polices(cursor):
    allowed_rules = []
    blocked_rules = []
    for _ in range(3):
        allow_rule_name = random_string(10, 'allowed_network_rule_').upper()
        cursor.execute(f"""
            CREATE NETWORK RULE IF NOT EXISTS {allow_rule_name}
                MODE=INTERNAL_STAGE TYPE=AWSVPCEID VALUE_LIST=('vpce-1234567{_ % 10}');
                    """).fetchone()
        allowed_rules.append(allow_rule_name)

    for _ in range(5):
        blocked_rule_name = random_string(10, 'blocked_network_rule_').upper()
        cursor.execute(f"""
            CREATE NETWORK RULE IF NOT EXISTS {blocked_rule_name}
                MODE=INTERNAL_STAGE TYPE=AWSVPCEID VALUE_LIST=('vpce-1234567{_ % 10}');
                    """).fetchone()
        blocked_rules.append(blocked_rule_name)

    try:
        yield allowed_rules, blocked_rules
    finally:
        for r in allowed_rules + blocked_rules:
            cursor.execute(f"DROP NETWORK RULE IF EXISTS {r}")


@pytest.fixture
def template_network_policy(prepare_rules_for_network_polices):
    allowed_rules , blocked_rules = prepare_rules_for_network_polices

    return NetworkPolicy(
        name = 'to_be_named',
        allowed_network_rule_list = allowed_rules,
        blocked_network_rule_list = blocked_rules,
        allowed_ip_list=['8.8.8.8'],
        blocked_ip_list=['0.0.0.0'],
    )

