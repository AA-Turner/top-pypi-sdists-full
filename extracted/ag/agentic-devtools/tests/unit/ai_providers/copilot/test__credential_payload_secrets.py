from agentic_devtools.ai_providers import copilot as copilot_module


def test_credential_payload_secrets_cyclic_mapping_returns_empty_set() -> None:
    cyclic: dict[str, object] = {}
    cyclic["self"] = cyclic
    assert copilot_module._credential_payload_secrets(cyclic) == set()


def test_credential_payload_secrets_cyclic_list_returns_empty_set() -> None:
    cyclic: list[object] = []
    cyclic.append(cyclic)
    assert copilot_module._credential_payload_secrets(cyclic) == set()
