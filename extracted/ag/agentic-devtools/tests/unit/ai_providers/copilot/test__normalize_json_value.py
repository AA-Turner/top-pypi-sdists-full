from collections.abc import Mapping

import pytest

from agentic_devtools.ai_providers import copilot as copilot_module


def test_normalize_json_value_recovers_from_recursionerror(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(copilot_module, "_safe_json_value", lambda value: (_ for _ in ()).throw(RecursionError()))

    assert copilot_module._normalize_json_value({"token": "secret"}) == "<max-depth>"


def test_normalize_json_value_recovers_from_mapping_iteration_errors() -> None:
    class RaisingMapping(Mapping[str, object]):
        def __getitem__(self, key: str) -> object:
            raise RuntimeError("unreadable")

        def __iter__(self):
            raise RuntimeError("unreadable")

        def __len__(self) -> int:
            return 1

        def items(self):
            raise RuntimeError("unreadable")

    assert copilot_module._normalize_json_value(RaisingMapping()) == "<unreadable>"
