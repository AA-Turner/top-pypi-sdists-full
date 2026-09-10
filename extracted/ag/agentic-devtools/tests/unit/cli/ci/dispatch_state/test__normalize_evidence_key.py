from agentic_devtools.cli.ci import dispatch_state as dispatch_state_module


def test_normalizes_casing_and_delimiters() -> None:
    assert dispatch_state_module._normalize_evidence_key("AuthHeaderValue") == "auth_header_value"
    assert dispatch_state_module._normalize_evidence_key("x-token/id") == "x_token_id"
