from agentic_devtools.adapters import PreCreateLookup as PublicPreCreateLookup
from agentic_devtools.adapters.issue_provider import PreCreateLookup


def test_precreatelookup_is_exported_from_adapters_facade() -> None:
    assert PublicPreCreateLookup is PreCreateLookup
