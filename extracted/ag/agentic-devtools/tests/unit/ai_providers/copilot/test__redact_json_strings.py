from agentic_devtools.ai_providers import copilot as copilot_module


def test_redact_json_strings_redacts_numeric_secret_leaf() -> None:
    redacted = copilot_module._redact_json_strings(
        {"message": 123456},
        payload_secrets=frozenset({"123456"}),
    )

    assert redacted == {"message": "<redacted>"}
