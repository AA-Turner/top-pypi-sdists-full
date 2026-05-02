from __future__ import annotations

import math
from dataclasses import dataclass

import torch

from cortex.fabric.config import FabricConfig


@dataclass(frozen=True)
class AnatomySpec:
    num_cells: int
    coord_dim: int
    coords: torch.Tensor
    cell_layout: torch.Tensor
    neighbor_idx: torch.Tensor
    neighbor_valid: torch.Tensor
    edge_type: torch.Tensor
    edge_distance: torch.Tensor
    edge_delay: torch.Tensor | None
    metadata: dict


@dataclass(frozen=True)
class FabricSpec:
    config: FabricConfig
    anatomy: AnatomySpec
    family_names: tuple[str, ...]
    recurrent_cell_idx: torch.Tensor
    kv_group_id: torch.Tensor
    num_kv_groups: int
    input_cell_idx: torch.Tensor
    output_cell_idx: torch.Tensor
    slot_init: torch.Tensor


def init_fabric(config: FabricConfig | None = None, **kwargs) -> FabricSpec:
    cfg = config if config is not None else FabricConfig(**kwargs)
    coords = _build_coords(cfg)
    family_names = tuple(cfg.families.keys())
    input_cell_idx, output_cell_idx = _build_ports(cfg, coords)
    recurrent_cell_idx = _build_recurrent_cells(coords.shape[0], input_cell_idx, output_cell_idx)
    cell_layout = -torch.ones(coords.shape[0], dtype=torch.long)
    cell_layout[recurrent_cell_idx] = _assign_cells(cfg, coords.index_select(0, recurrent_cell_idx), family_names)
    neighbor_idx, neighbor_valid, edge_type, edge_distance, edge_delay = _build_sparse_graph(
        cfg,
        coords,
        input_cell_idx=input_cell_idx,
        output_cell_idx=output_cell_idx,
    )
    kv_group_id, num_kv_groups = _build_kv_groups(cfg, coords)
    slot_init = _build_slot_init(
        cfg,
        coords,
        cell_layout,
        recurrent_cell_idx,
        input_cell_idx,
        output_cell_idx,
    )
    anatomy = AnatomySpec(
        num_cells=coords.shape[0],
        coord_dim=coords.shape[1],
        coords=coords,
        cell_layout=cell_layout,
        neighbor_idx=neighbor_idx,
        neighbor_valid=neighbor_valid,
        edge_type=edge_type,
        edge_distance=edge_distance,
        edge_delay=edge_delay,
        metadata={"shape": cfg.coord_shape, "wrap": cfg.wrap},
    )
    return FabricSpec(
        config=cfg,
        anatomy=anatomy,
        family_names=family_names,
        recurrent_cell_idx=recurrent_cell_idx,
        kv_group_id=kv_group_id,
        num_kv_groups=num_kv_groups,
        input_cell_idx=input_cell_idx,
        output_cell_idx=output_cell_idx,
        slot_init=slot_init,
    )


def _build_coords(cfg: FabricConfig) -> torch.Tensor:
    axes = [torch.arange(size, dtype=torch.float32) for size in cfg.coord_shape]
    return torch.cartesian_prod(*axes)


def _assign_cells(cfg: FabricConfig, coords: torch.Tensor, family_names: tuple[str, ...]) -> torch.Tensor:
    num_cells = coords.shape[0]
    weights = torch.tensor([cfg.cell_mix[name] for name in family_names], dtype=torch.float64)
    weights = weights / weights.sum()
    expected = weights * float(num_cells)
    counts = expected.floor().to(torch.long)
    remainder = int(num_cells - counts.sum().item())
    if remainder > 0:
        frac = expected - counts.to(expected.dtype)
        order = torch.argsort(frac, descending=True)
        counts[order[:remainder]] += 1
    labels = []
    for family_idx, count in enumerate(counts.tolist()):
        labels.extend([family_idx] * count)
    layout = torch.tensor(labels, dtype=torch.long)
    if cfg.cell_arrangement == "x_bands":
        order = torch.argsort(_lexsort_key(coords))
        arranged = torch.empty(num_cells, dtype=torch.long)
        arranged[order] = layout
        return arranged
    gen = torch.Generator(device="cpu")
    gen.manual_seed(cfg.seed)
    perm = torch.randperm(num_cells, generator=gen)
    return layout.index_select(0, perm)


def _build_sparse_graph(
    cfg: FabricConfig,
    coords: torch.Tensor,
    *,
    input_cell_idx: torch.Tensor,
    output_cell_idx: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor | None]:
    distances = _pairwise_distances(coords, cfg.coord_shape, wrap=cfg.wrap)
    num_cells = coords.shape[0]
    input_mask = torch.zeros(num_cells, dtype=torch.bool)
    input_mask[input_cell_idx] = True
    output_mask = torch.zeros(num_cells, dtype=torch.bool)
    output_mask[output_cell_idx] = True
    neighbors: list[list[int]] = []
    edge_types: list[list[int]] = []
    edge_distances: list[list[float]] = []
    delays: list[list[int]] = []
    for recv in range(num_cells):
        if bool(input_mask[recv]):
            neighbors.append([])
            edge_types.append([])
            edge_distances.append([])
            delays.append([])
            continue

        local_mask = (distances[recv] > 0) & (distances[recv] <= cfg.local_radius)
        local_mask = local_mask & ~output_mask
        if bool(output_mask[recv]):
            local_mask = local_mask & ~input_mask
        local_ids = torch.nonzero(local_mask, as_tuple=False).reshape(-1)
        local_ids = local_ids[torch.argsort(distances[recv, local_ids])]
        recv_neighbors = local_ids.tolist()
        recv_types = [0] * len(recv_neighbors)
        recv_edge_distances = [float(distances[recv, send].item()) for send in recv_neighbors]

        if cfg.patch_edges_per_cell > 0:
            patch_mask = (
                (distances[recv] >= cfg.patch_min_dist)
                & (distances[recv] <= cfg.patch_max_dist)
                & ~local_mask
                & (distances[recv] > 0)
            )
            patch_mask = patch_mask & ~output_mask
            if bool(output_mask[recv]):
                patch_mask = patch_mask & ~input_mask
            patch_ids = torch.nonzero(patch_mask, as_tuple=False).reshape(-1)
            patch_ids = patch_ids[torch.argsort(distances[recv, patch_ids])]
            patch_ids = patch_ids[: cfg.patch_edges_per_cell]
            recv_neighbors.extend(patch_ids.tolist())
            recv_types.extend([1] * patch_ids.numel())
            recv_edge_distances.extend(float(distances[recv, send].item()) for send in patch_ids.tolist())

        recv_delays = []
        for send in recv_neighbors:
            if cfg.conduction_speed is None or cfg.max_delay is None:
                recv_delays.append(1)
            else:
                delay = int(math.ceil(float(distances[recv, send].item()) / cfg.conduction_speed))
                recv_delays.append(max(1, min(cfg.max_delay, delay)))

        neighbors.append(recv_neighbors)
        edge_types.append(recv_types)
        edge_distances.append(recv_edge_distances)
        delays.append(recv_delays)

    max_neighbors = max((len(items) for items in neighbors), default=0)
    if max_neighbors == 0:
        raise ValueError("fabric graph has no edges; increase local_radius or change anatomy size")

    neighbor_idx = torch.zeros(num_cells, max_neighbors, dtype=torch.long)
    neighbor_valid = torch.zeros(num_cells, max_neighbors, dtype=torch.bool)
    edge_type = torch.zeros(num_cells, max_neighbors, dtype=torch.long)
    edge_distance = torch.zeros(num_cells, max_neighbors, dtype=coords.dtype)
    edge_delay = torch.ones(num_cells, max_neighbors, dtype=torch.long)
    for recv in range(num_cells):
        count = len(neighbors[recv])
        if count == 0:
            continue
        neighbor_idx[recv, :count] = torch.tensor(neighbors[recv], dtype=torch.long)
        neighbor_valid[recv, :count] = True
        edge_type[recv, :count] = torch.tensor(edge_types[recv], dtype=torch.long)
        edge_distance[recv, :count] = torch.tensor(edge_distances[recv], dtype=coords.dtype)
        edge_delay[recv, :count] = torch.tensor(delays[recv], dtype=torch.long)

    return neighbor_idx, neighbor_valid, edge_type, edge_distance, edge_delay if cfg.max_delay is not None else None


def _pairwise_distances(coords: torch.Tensor, shape: tuple[int, ...], *, wrap: bool) -> torch.Tensor:
    diffs = (coords[:, None, :] - coords[None, :, :]).abs()
    if wrap:
        shape_tensor = torch.tensor(shape, dtype=coords.dtype).view(1, 1, -1)
        diffs = torch.minimum(diffs, shape_tensor - diffs)
    return torch.linalg.vector_norm(diffs, dim=-1)


def _lexsort_key(coords: torch.Tensor) -> torch.Tensor:
    strides = []
    acc = 1
    max_vals = coords.max(dim=0).values.to(torch.long) + 1
    for size in reversed(max_vals[1:].tolist()):
        acc *= int(size)
        strides.append(acc)
    strides = list(reversed(strides)) + [1]
    key = torch.zeros(coords.shape[0], dtype=torch.long)
    coords_long = coords.to(torch.long)
    for axis, stride in enumerate(strides):
        key = key + coords_long[:, axis] * stride
    return key


def _build_kv_groups(cfg: FabricConfig, coords: torch.Tensor) -> tuple[torch.Tensor, int]:
    if cfg.projection_region_shape is None:
        region_shape = tuple(max(1, size // 4) for size in cfg.coord_shape)
    else:
        region_shape = cfg.projection_region_shape
    region = torch.div(coords.to(torch.long), torch.tensor(region_shape, dtype=torch.long), rounding_mode="floor")
    grid_dims = [(size + tile - 1) // tile for size, tile in zip(cfg.coord_shape, region_shape, strict=True)]
    strides = []
    acc = 1
    for size in reversed(grid_dims[1:]):
        acc *= size
        strides.append(acc)
    strides = list(reversed(strides)) + [1]
    kv_group_id = sum(region[:, axis] * strides[axis] for axis in range(region.shape[1]))
    num_groups = int(kv_group_id.max().item()) + 1 if kv_group_id.numel() > 0 else 0
    return kv_group_id.to(torch.long), num_groups


def _build_ports(cfg: FabricConfig, coords: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    x_coord = coords[:, 0]
    input_mask = x_coord < float(cfg.input_band_width)
    output_mask = x_coord >= float(cfg.width - cfg.output_band_width)
    input_idx = torch.nonzero(input_mask, as_tuple=False).reshape(-1).to(torch.long)
    output_idx = torch.nonzero(output_mask, as_tuple=False).reshape(-1).to(torch.long)
    if input_idx.numel() == 0 or output_idx.numel() == 0:
        raise ValueError("port construction produced an empty input or output port set")
    if bool(torch.isin(input_idx, output_idx).any()):
        raise ValueError("input and output port cells must be disjoint")
    return input_idx, output_idx


def _build_recurrent_cells(num_cells: int, input_idx: torch.Tensor, output_idx: torch.Tensor) -> torch.Tensor:
    recurrent_mask = torch.ones(num_cells, dtype=torch.bool)
    recurrent_mask[input_idx] = False
    recurrent_mask[output_idx] = False
    recurrent_idx = torch.nonzero(recurrent_mask, as_tuple=False).reshape(-1).to(torch.long)
    if recurrent_idx.numel() == 0:
        raise ValueError("fabric must contain at least one recurrent cell after reserving boundary port cells")
    return recurrent_idx


def _build_slot_init(
    cfg: FabricConfig,
    coords: torch.Tensor,
    cell_layout: torch.Tensor,
    recurrent_idx: torch.Tensor,
    input_idx: torch.Tensor,
    output_idx: torch.Tensor,
) -> torch.Tensor:
    shape = torch.tensor(cfg.coord_shape, dtype=coords.dtype)
    coords_norm = coords / shape.view(1, -1).clamp_min(1.0)
    sin_feat = torch.sin(2.0 * math.pi * coords_norm)
    cos_feat = torch.cos(2.0 * math.pi * coords_norm)
    num_families = len(cfg.families)
    family_one_hot = torch.zeros(coords.shape[0], num_families, dtype=coords.dtype)
    family_one_hot[recurrent_idx] = torch.nn.functional.one_hot(
        cell_layout[recurrent_idx], num_classes=num_families
    ).to(coords.dtype)
    input_mask = torch.zeros(coords.shape[0], 1, dtype=coords.dtype)
    input_mask[input_idx] = 1.0
    output_mask = torch.zeros(coords.shape[0], 1, dtype=coords.dtype)
    output_mask[output_idx] = 1.0
    base = torch.cat([coords_norm, sin_feat, cos_feat, family_one_hot, input_mask, output_mask], dim=-1)
    repeats = math.ceil(cfg.d_slot / base.shape[1])
    slot = base.repeat(1, repeats)[:, : cfg.d_slot]
    gen = torch.Generator(device="cpu")
    gen.manual_seed(cfg.seed + 17)
    noise = 0.01 * torch.randn(coords.shape[0], cfg.d_slot, generator=gen, dtype=coords.dtype)
    return slot + noise


__all__ = ["AnatomySpec", "FabricSpec", "init_fabric"]
