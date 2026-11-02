from agentic_devtools.cli.ci.dispatch_reservation import _request_key


def test_joins_request_identity_fields() -> None:
    assert _request_key("owner/repo", 123, "a" * 40, 2) == f"owner/repo|123|{'a' * 40}|2"
