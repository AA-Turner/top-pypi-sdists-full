from agentic_devtools.cli.ci import dispatch_state as dispatch_state_module


def test_redacts_basic_and_pat_tokens() -> None:
    text = "Authorization: Basic dXNlcjpwYXNz ghp_abcdefghijklmnopqrstuvwxyz"

    assert dispatch_state_module._redact_secrets(text) == "[REDACTED] [REDACTED]"


def test_redacts_generic_secret_assignments() -> None:
    text = "api_key=supersecret password: value token='abc123'"

    assert dispatch_state_module._redact_secrets(text) == "api_key=[REDACTED] password: [REDACTED] token=[REDACTED]"


def test_redacts_serialized_secret_assignments_and_aliases() -> None:
    text = '{"token":"secret","authorization":"******","auth"="basic","pat":"x","credentials":"y","private_key":"z"}'

    assert dispatch_state_module._redact_secrets(text) == (
        '{"token":[REDACTED],"authorization":[REDACTED],"auth"=[REDACTED],"pat":[REDACTED],'
        '"credentials":[REDACTED],"private_key":[REDACTED]}'
    )
