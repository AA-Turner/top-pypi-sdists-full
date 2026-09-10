from agentic_devtools.cli.ci import dispatch_state as dispatch_state_module


def test_identifies_sensitive_evidence_keys() -> None:
    assert dispatch_state_module._is_sensitive_evidence_key("Authorization")
    assert dispatch_state_module._is_sensitive_evidence_key("apikey")
    assert dispatch_state_module._is_sensitive_evidence_key("api_key")
    assert dispatch_state_module._is_sensitive_evidence_key("credentials")
    assert dispatch_state_module._is_sensitive_evidence_key("authorization_header")
    assert dispatch_state_module._is_sensitive_evidence_key("response_headers")
    assert dispatch_state_module._is_sensitive_evidence_key("request_body")
    assert dispatch_state_module._is_sensitive_evidence_key("task_prompt")
    assert not dispatch_state_module._is_sensitive_evidence_key("status")
