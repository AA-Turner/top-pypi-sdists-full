from agentic_devtools.adapters.pull_request_threads import sanitize_diagnostic


def test_redacts_secrets_from_diagnostics() -> None:
    assert sanitize_diagnostic("token leaked", ("token",)) == "[REDACTED] leaked"
