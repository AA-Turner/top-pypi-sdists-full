"""Tests for CooldownRecord."""

from agentic_devtools.cli.ci.cooldown import CooldownRecord


class TestCooldownRecord:
    """CooldownRecord serializes stable provider cooldown fields."""

    def test_as_dict_returns_expected_schema(self) -> None:
        record = CooldownRecord(
            resume_at=200.0,
            reason="rate_limit",
            source="retry-after",
            updated_at=100.0,
        )

        assert record.as_dict() == {
            "resume_at": 200.0,
            "reason": "rate_limit",
            "source": "retry-after",
            "updated_at": 100.0,
        }
