from pathlib import Path


def test_discovered_tool_registration_creates_and_reconciles_purpose() -> None:
    sql = (
        Path(__file__).parents[3]
        / "db/migrations/0543_purpose_mcp_discovered_tools.sql"
    ).read_text()

    registration = sql.split("DO $reconcile$", 1)[0]
    reconciliation = sql.split("DO $reconcile$", 1)[1]

    assert "RETURNING id INTO v_tool_id" in registration
    assert "PERFORM platform.upsert_unit_purpose(" in registration
    assert registration.index("PERFORM platform.upsert_unit_purpose(") < registration.index(
        "INSERT INTO tool.binding"
    )
    assert "FROM tool.definition d" in reconciliation
    assert "d.source_kind = 'mcp_discovered'" in reconciliation
    assert "PERFORM platform.upsert_unit_purpose(" in reconciliation
