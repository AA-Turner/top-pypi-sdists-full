from agentic_devtools.cli.ci.dispatch_state import DispatchIdentity, DispatchRecord, validate_dispatch_record

SHA = "a" * 40


def test_returns_validated_record() -> None:
    record = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))

    assert validate_dispatch_record(record) == record
