"""Tests for parse_cooldowns()."""

import json

from agentic_devtools.cli.ci.cooldown import parse_cooldowns


class TestParseCooldowns:
    """parse_cooldowns() filters malformed and expired entries safely."""

    def test_returns_empty_for_missing_raw_value(self) -> None:
        assert parse_cooldowns(None, now=100) == {}
        assert parse_cooldowns("", now=100) == {}

    def test_drops_malformed_and_expired_records(self) -> None:
        long_key = f"{'p' * 128}:{'i' * 128}"
        raw = json.dumps(
            {
                "provider_cooldowns": {
                    "github:GH_TOKEN": {"resume_at": 101, "updated_at": 1},
                    long_key: {"resume_at": 101, "updated_at": 1},
                    "github:expired": {"resume_at": 99, "updated_at": 1},
                    "bad key/": {"resume_at": 200, "updated_at": 1},
                    "github:too:many": {"resume_at": 200, "updated_at": 1},
                    "github:bad": {"resume_at": "later", "updated_at": 1},
                }
            }
        )

        records = parse_cooldowns(raw, now=100)

        assert list(records) == ["github:GH_TOKEN", long_key]

    def test_rejects_invalid_shapes_and_malformed_json(self, caplog) -> None:
        assert parse_cooldowns("{", now=100) == {}
        assert parse_cooldowns(json.dumps([]), now=100) == {}
        assert parse_cooldowns(json.dumps({"provider_cooldowns": {"github:x": []}}), now=100) == {}
        assert (
            parse_cooldowns(
                json.dumps(
                    {
                        "provider_cooldowns": {
                            "github:x": {"resume_at": 101, "updated_at": "bad"},
                            "github:y": {"resume_at": 101, "updated_at": 1, "reason": 3},
                            "github:z": {"resume_at": -1, "updated_at": 1},
                            "github:infinite": {"resume_at": float("inf"), "updated_at": 1},
                            "github:bad-reason": {"resume_at": 101, "updated_at": 1, "reason": "other"},
                            "github:bad-source": {"resume_at": 101, "updated_at": 1, "source": "retry-after\nx=1"},
                            "github:too-far": {"resume_at": 1e300, "updated_at": 1},
                        }
                    }
                ),
                now=100,
            )
            == {}
        )
        assert "malformed" in caplog.text
