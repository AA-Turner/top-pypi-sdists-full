import pytest

from agentic_devtools.cli.pull_request_publish import _validated_provider


@pytest.mark.parametrize(
    ("value", "expected"),
    [("github", "github"), (" azure_devops ", "azure_devops")],
)
def test_accepts_supported_provider_names(value: str, expected: str) -> None:
    assert _validated_provider(value, "provider") == expected


@pytest.mark.parametrize("value", [None, [], "", "gitlab"])
def test_rejects_unsupported_provider_values(value: object) -> None:
    with pytest.raises(ValueError, match="provider must be 'azure_devops' or 'github'"):
        _validated_provider(value, "provider")
