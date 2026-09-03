from agentic_devtools.ai_providers import redact_authorization_header


def test_redact_authorization_header_masks_authorization_value() -> None:
    headers = {
        "Authorization": "Bearer " + "ghu_test_sentinel_" + "token",
        "Accept": "application/vnd.github+json",
        "X-Other": "value",
    }

    assert redact_authorization_header(headers) == {
        "Authorization": "<redacted>",
        "Accept": "application/vnd.github+json",
        "X-Other": "value",
    }
    assert headers["Authorization"] == "Bearer " + "ghu_test_sentinel_" + "token"


def test_redact_authorization_header_handles_case_insensitive_bearer_scheme() -> None:
    assert redact_authorization_header({"authorization": "bearer secret"}) == {"authorization": "<redacted>"}


def test_redact_authorization_header_redacts_non_bearer_schemes() -> None:
    assert redact_authorization_header({"Authorization": "Token secret"}) == {"Authorization": "<redacted>"}
