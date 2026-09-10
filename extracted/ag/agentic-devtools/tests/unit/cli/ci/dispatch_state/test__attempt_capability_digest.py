import pytest

from agentic_devtools.cli.ci import dispatch_state as dispatch_state_module


def test_returns_sha256_hex_digest_for_non_empty_strings() -> None:
    digest = dispatch_state_module._attempt_capability_digest("local-capability")

    assert digest == "9868459e209972cc6dad0fa6302af56515c5f9b6e561a35f59bd71ef4ab8f8a2"


def test_rejects_blank_or_non_string_capabilities() -> None:
    for capability in ("", None, 1):
        with pytest.raises(ValueError, match="non-empty string"):
            dispatch_state_module._attempt_capability_digest(capability)
