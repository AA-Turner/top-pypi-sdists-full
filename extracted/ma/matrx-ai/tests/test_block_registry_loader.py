from __future__ import annotations

import pytest

from matrx_ai.processing.blocks.block_registry import (
    BlockRegistry,
    DetectionMethod,
)


@pytest.mark.asyncio
async def test_custom_types_load_through_host_row_loader() -> None:
    registry = BlockRegistry(auto_register_builtins=False)

    async def load_rows() -> list[dict[str, object]]:
        return [
            {
                "type_key": "custom_cards",
                "display_name": "Custom Cards",
                "detection_method": "json_root_key",
                "detection_config": {"json_root_key": "cards"},
                "streaming_behavior": "complete_only",
                "description": "Host-provided definition",
            }
        ]

    count = await registry.load_custom_types(load_rows)

    assert count == 1
    definition = registry.get("custom_cards")
    assert definition is not None
    assert definition.detection.method is DetectionMethod.JSON_ROOT_KEY
    assert definition.detection.json_root_key == "cards"
    assert definition.is_builtin is False


@pytest.mark.asyncio
async def test_custom_type_loader_errors_are_not_silently_swallowed() -> None:
    registry = BlockRegistry(auto_register_builtins=False)

    async def load_rows() -> list[dict[str, object]]:
        raise RuntimeError("database unavailable")

    with pytest.raises(RuntimeError, match="database unavailable"):
        await registry.load_custom_types(load_rows)
