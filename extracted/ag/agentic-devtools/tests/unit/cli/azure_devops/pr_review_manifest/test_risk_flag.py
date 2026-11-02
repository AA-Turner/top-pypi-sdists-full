"""Tests for risk_flag."""

from agentic_devtools.cli.azure_devops.pr_review_manifest import risk_flag


class TestRiskFlag:
    def test_empty_is_false(self):
        assert risk_flag("") is False
        assert risk_flag(None) is False

    def test_security_substrings(self):
        assert risk_flag("/src/auth/login.py") is True
        assert risk_flag("/lib/crypto.ts") is True
        assert risk_flag("/app/payment_gateway.py") is True

    def test_sql_is_risk(self):
        assert risk_flag("/db/schema.sql") is True

    def test_migration_is_risk(self):
        assert risk_flag("/db/migrations/0001_init.py") is True

    def test_no_false_positive_for_migration_substring(self):
        # 'immigration_policy.py' contains 'migration' as a substring but not as a component.
        assert risk_flag("/src/immigration_policy.py") is False

    def test_plain_source_is_not_risk(self):
        assert risk_flag("/src/util.py") is False
