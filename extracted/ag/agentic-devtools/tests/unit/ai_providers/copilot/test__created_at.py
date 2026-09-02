from agentic_devtools.ai_providers import copilot as copilot_module


def test_created_at_reads_canonical_field_first() -> None:
    body = {
        "created_at": "2026-01-01T00:00:00Z",
        "createdAt": "2027-01-01T00:00:00Z",
        "timestamp": "2028-01-01T00:00:00Z",
    }

    assert copilot_module._created_at(body) == "2026-01-01T00:00:00Z"


def test_created_at_falls_back_to_alias_when_primary_is_invalid() -> None:
    body = {"created_at": "invalid", "createdAt": "2026-01-01T00:00:00Z"}

    assert copilot_module._created_at(body) == "2026-01-01T00:00:00Z"


def test_created_at_returns_none_when_no_valid_timestamp_exists() -> None:
    assert copilot_module._created_at({"created_at": "invalid", "timestamp": 123}) is None
