from __future__ import annotations

from cortex import FabricConfig, FabricFamilyConfig, FabricRuntime, build_fabric, init_fabric


def test_fabric_public_api_builds_runtime() -> None:
    spec = init_fabric(
        FabricConfig(
            width=4,
            height=4,
            hidden_size=8,
            families={"slstm": FabricFamilyConfig(family_type="slstm")},
            cell_mix={"slstm": 1.0},
        )
    )

    runtime = build_fabric(spec)

    assert isinstance(runtime, FabricRuntime)
    assert spec.input_cell_idx.numel() > 0
    assert spec.output_cell_idx.numel() > 0
