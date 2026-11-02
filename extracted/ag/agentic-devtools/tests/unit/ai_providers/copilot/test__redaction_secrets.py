from agentic_devtools.ai_providers import copilot as copilot_module


def test_redaction_secrets_includes_nested_credential_payload_value() -> None:
    assert copilot_module._redaction_secrets(payload={"token": {"nested": ["secret"]}}) == {"secret"}


def test_redaction_secrets_includes_non_standard_credential_headers() -> None:
    secrets = copilot_module._redaction_secrets(headers={"X-API-Key": "fixture-secret"})

    assert "fixture-secret" in secrets


def test_redaction_secrets_treats_factory_headers_as_sensitive_except_api_version() -> None:
    secrets = copilot_module._redaction_secrets(
        headers={
            "Cookie": "session=fixture",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2026-03-10",
        }
    )

    assert "session=fixture" in secrets
    assert "application/vnd.github+json" in secrets
    assert "2026-03-10" not in secrets
