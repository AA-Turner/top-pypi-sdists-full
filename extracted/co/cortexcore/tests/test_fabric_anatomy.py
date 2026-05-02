from __future__ import annotations

import torch
from cortex.fabric import FabricConfig, FabricFamilyConfig, init_fabric


def test_init_fabric_builds_2d_anatomy_with_ports_and_neighbors():
    spec = init_fabric(
        FabricConfig(
            width=4,
            height=3,
            hidden_size=8,
            families={
                "slstm": FabricFamilyConfig(family_type="slstm"),
                "axoncell": FabricFamilyConfig(family_type="axoncell"),
            },
            cell_mix={"slstm": 0.5, "axoncell": 0.5},
            projection_region_shape=(2, 1),
            input_band_width=1,
            output_band_width=1,
            seed=3,
        )
    )

    assert spec.anatomy.coords.shape == (12, 2)
    assert spec.anatomy.neighbor_idx.shape[:1] == (12,)
    assert spec.input_cell_idx.numel() == 3
    assert spec.output_cell_idx.numel() == 3
    assert spec.slot_init.shape == (12, 16)
    assert spec.num_kv_groups > 0
    assert spec.anatomy.edge_distance.shape == spec.anatomy.neighbor_idx.shape
    assert bool((spec.anatomy.edge_distance[spec.anatomy.neighbor_valid] > 0).all())


def test_init_fabric_builds_3d_anatomy():
    spec = init_fabric(
        FabricConfig(
            width=3,
            height=2,
            depth=2,
            hidden_size=4,
            projection_region_shape=(1, 1, 1),
        )
    )

    assert spec.anatomy.coords.shape == (12, 3)
    assert spec.anatomy.coord_dim == 3
    assert spec.anatomy.num_cells == 12


def test_init_fabric_supports_banded_family_arrangement():
    spec = init_fabric(
        FabricConfig(
            width=4,
            height=2,
            hidden_size=8,
            families={
                "axoncell": FabricFamilyConfig(family_type="axoncell"),
                "slstm": FabricFamilyConfig(family_type="slstm"),
            },
            cell_mix={"axoncell": 0.25, "slstm": 0.75},
            cell_arrangement="x_bands",
            seed=5,
        )
    )

    coords = spec.anatomy.coords
    layout = spec.anatomy.cell_layout
    recurrent_coords = coords[layout >= 0]
    recurrent_layout = layout[layout >= 0]
    order = recurrent_coords[:, 0].argsort(stable=True)
    assert int(recurrent_layout[order[0]].item()) == 0
    assert int((layout == 0).sum().item()) == 1


def test_port_cells_use_source_sink_connectivity():
    spec = init_fabric(
        FabricConfig(
            width=4,
            height=3,
            hidden_size=8,
            families={
                "slstm": FabricFamilyConfig(family_type="slstm"),
                "axoncell": FabricFamilyConfig(family_type="axoncell"),
            },
            cell_mix={"slstm": 0.5, "axoncell": 0.5},
            input_band_width=1,
            output_band_width=1,
            wrap=False,
            seed=9,
        )
    )

    neighbor_valid = spec.anatomy.neighbor_valid
    neighbor_idx = spec.anatomy.neighbor_idx

    assert not bool(neighbor_valid[spec.input_cell_idx].any())
    if spec.output_cell_idx.numel() > 0:
        output_sender_mask = (neighbor_idx.unsqueeze(-1) == spec.output_cell_idx.view(1, 1, -1)).any(dim=-1)
        assert not bool((output_sender_mask & neighbor_valid).any())


def test_output_cells_do_not_read_directly_from_input_cells():
    spec = init_fabric(
        FabricConfig(
            width=3,
            height=8,
            hidden_size=8,
            families={"slstm": FabricFamilyConfig(family_type="slstm")},
            cell_mix={"slstm": 1.0},
            input_band_width=1,
            output_band_width=1,
            local_radius=1.5,
            wrap=True,
            seed=7,
        )
    )

    input_mask = torch.zeros(spec.anatomy.num_cells, dtype=torch.bool)
    input_mask[spec.input_cell_idx] = True
    for recv in spec.output_cell_idx.tolist():
        valid = spec.anatomy.neighbor_valid[recv]
        senders = spec.anatomy.neighbor_idx[recv][valid]
        assert not bool(input_mask[senders].any())
