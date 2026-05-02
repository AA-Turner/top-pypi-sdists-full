from __future__ import annotations

import math
from typing import Literal, Optional

import torch
import torch.nn as nn
from tensordict import TensorDict, TensorDictBase

from cortex.fabric.anatomy import FabricSpec
from cortex.fabric.families import build_family_module
from cortex.kernels.cuda.fabric import fabric_sparse_message_cuda
from cortex.types import MaybeState, ResetMask, Tensor

ExecutionMode = Literal["stream", "diffusion"]


class FabricRuntime(nn.Module):
    def __init__(self, spec: FabricSpec) -> None:
        super().__init__()
        self.spec = spec
        self.config = spec.config
        self.hidden_size = int(spec.config.hidden_size)
        self.num_heads = int(spec.config.num_heads)
        self.head_dim = int(spec.config.head_dim)
        self.value_dim = int(spec.config.head_dim)
        self._has_edge_delay = spec.anatomy.edge_delay is not None
        if self.num_heads != 1:
            raise ValueError("FabricRuntime fast path currently requires single-head fabric attention")
        if spec.config.readout_pool == "mean":
            self.readout_slots = 1
        elif spec.config.readout_pool == "flatten":
            self.readout_slots = int(spec.output_cell_idx.numel())
        else:
            self.readout_slots = int(spec.config.readout_slots)
        self._family_names = spec.family_names
        self._family_name_to_idx = {name: idx for idx, name in enumerate(self._family_names)}

        self.register_buffer("cell_layout", spec.anatomy.cell_layout.clone())
        self.register_buffer("neighbor_idx", spec.anatomy.neighbor_idx.clone())
        self.register_buffer("neighbor_idx_flat", spec.anatomy.neighbor_idx.reshape(-1).clone())
        self.register_buffer("neighbor_valid", spec.anatomy.neighbor_valid.clone())
        self.register_buffer("edge_type", spec.anatomy.edge_type.clone())
        self.register_buffer("edge_distance", spec.anatomy.edge_distance.clone())
        self.register_buffer(
            "edge_delay",
            spec.anatomy.edge_delay.clone()
            if spec.anatomy.edge_delay is not None
            else torch.ones_like(spec.anatomy.edge_type),
        )
        self.register_buffer("kv_group_id", spec.kv_group_id.clone())
        self.register_buffer("recurrent_cell_idx", spec.recurrent_cell_idx.clone())
        self.register_buffer("input_cell_idx", spec.input_cell_idx.clone())
        self.register_buffer("output_cell_idx", spec.output_cell_idx.clone())
        self.register_buffer("coords", spec.anatomy.coords.clone())
        self._num_neighbors = int(spec.anatomy.neighbor_idx.shape[1])
        sender_mask = torch.ones(spec.anatomy.num_cells, dtype=torch.bool)
        sender_mask[spec.output_cell_idx] = False
        sender_cell_idx = torch.nonzero(sender_mask, as_tuple=False).reshape(-1)
        sender_lookup = torch.full((spec.anatomy.num_cells,), -1, dtype=torch.long)
        sender_lookup[sender_cell_idx] = torch.arange(sender_cell_idx.numel(), dtype=torch.long)
        self.register_buffer("sender_cell_idx", sender_cell_idx)
        self.register_buffer("sender_lookup", sender_lookup)
        self.register_buffer("input_sender_idx", sender_lookup[self.input_cell_idx].clone())
        recurrent_lookup = torch.full((spec.anatomy.num_cells,), -1, dtype=torch.long)
        recurrent_lookup[self.recurrent_cell_idx] = torch.arange(self.recurrent_cell_idx.numel(), dtype=torch.long)
        self.register_buffer("recurrent_lookup", recurrent_lookup)
        self.register_buffer("recurrent_sender_idx", sender_lookup[self.recurrent_cell_idx].clone())
        self._num_input_cells = int(self.input_cell_idx.numel())
        self._num_recurrent_cells = int(self.recurrent_cell_idx.numel())
        self._num_output_cells = int(self.output_cell_idx.numel())
        num_senders = int(sender_cell_idx.numel())
        self._partitioned_layout = bool(
            torch.equal(self.input_cell_idx, torch.arange(self._num_input_cells, dtype=torch.long))
            and torch.equal(
                self.recurrent_cell_idx,
                torch.arange(
                    self._num_input_cells,
                    self._num_input_cells + self._num_recurrent_cells,
                    dtype=torch.long,
                ),
            )
            and torch.equal(
                self.output_cell_idx,
                torch.arange(num_senders, num_senders + self._num_output_cells, dtype=torch.long),
            )
        )
        self._input_slice = slice(0, self._num_input_cells)
        self._recurrent_slice = slice(self._num_input_cells, self._num_input_cells + self._num_recurrent_cells)
        self._output_slice = slice(num_senders, num_senders + self._num_output_cells)
        (
            recurrent_neighbor_idx,
            recurrent_neighbor_valid,
            recurrent_edge_distance,
            recurrent_edge_delay,
        ) = _select_receiver_tables(
            self.neighbor_idx,
            self.neighbor_valid,
            self.edge_distance,
            self.edge_delay,
            self.recurrent_cell_idx,
            self.sender_lookup,
        )
        self.register_buffer("recurrent_neighbor_idx", recurrent_neighbor_idx)
        self.register_buffer("recurrent_neighbor_valid", recurrent_neighbor_valid)
        self.register_buffer("recurrent_edge_distance", recurrent_edge_distance)
        self.register_buffer("recurrent_edge_delay", recurrent_edge_delay)
        (
            output_neighbor_idx,
            output_neighbor_valid,
            output_edge_distance,
            output_edge_delay,
        ) = _select_receiver_tables(
            self.neighbor_idx,
            self.neighbor_valid,
            self.edge_distance,
            self.edge_delay,
            self.output_cell_idx,
            self.sender_lookup,
        )
        self.register_buffer("output_neighbor_idx", output_neighbor_idx)
        self.register_buffer("output_neighbor_valid", output_neighbor_valid)
        self.register_buffer("output_edge_distance", output_edge_distance)
        self.register_buffer("output_edge_delay", output_edge_delay)

        self.slot_embed = nn.Parameter(spec.slot_init.clone())

        self.public_proj = nn.Linear(self.hidden_size, int(self.config.d_public), bias=False)
        self.input_proj = nn.Linear(self.hidden_size, int(self.config.d_msg), bias=False)
        self.msg_to_cell = nn.Linear(int(self.config.d_msg), self.hidden_size, bias=False)
        self.cell_bias_proj = nn.Linear(int(self.config.d_slot), self.hidden_size, bias=False)
        self.q_proj = nn.Linear(int(self.config.d_slot), self.num_heads * self.head_dim, bias=False)
        self.k_weight = nn.Parameter(
            torch.empty(spec.num_kv_groups, int(self.config.d_public), self.num_heads * self.head_dim)
        )
        self.v_weight = nn.Parameter(
            torch.empty(spec.num_kv_groups, int(self.config.d_public), self.num_heads * self.value_dim)
        )
        self.msg_out = nn.Linear(self.num_heads * self.value_dim, int(self.config.d_msg), bias=False)
        self.output_cell_weight = nn.Parameter(
            torch.empty(int(self.output_cell_idx.numel()), int(self.config.d_msg), self.hidden_size)
        )
        self.output_cell_bias = nn.Parameter(torch.empty(int(self.output_cell_idx.numel()), self.hidden_size))
        self.readout_query = nn.Parameter(torch.empty(self.readout_slots, self.hidden_size))
        self.readout_out = nn.Linear(self.readout_slots * self.hidden_size, self.hidden_size)

        self.family_modules = nn.ModuleDict()
        self._full_recurrent_family_name: str | None = None
        for name in self._family_names:
            indices = self._build_family_indices(name)
            self.register_buffer(_family_buffer_name(name), indices)
            family_recurrent_idx = self.recurrent_lookup.index_select(0, indices)
            family_recurrent_idx = family_recurrent_idx[family_recurrent_idx >= 0]
            self.register_buffer(_family_recurrent_buffer_name(name), family_recurrent_idx)
            if family_recurrent_idx.numel() == self._num_recurrent_cells and torch.equal(
                family_recurrent_idx, torch.arange(self._num_recurrent_cells, dtype=torch.long)
            ):
                self._full_recurrent_family_name = name
            self.family_modules[name] = build_family_module(
                self.config.families[name],
                self.hidden_size,
                num_cells=int(indices.numel()),
                init_noise_std=float(self.config.family_init_noise_std),
            )
        self._family_streams: dict[str, torch.cuda.Stream] | None = None
        self._constant_step_flat_cache: dict[tuple[str, int, int, int, str, int], torch.Tensor] = {}

        self._reset_parameters()

    def _reset_parameters(self) -> None:
        nn.init.xavier_uniform_(self.public_proj.weight)
        nn.init.xavier_uniform_(self.input_proj.weight)
        nn.init.xavier_uniform_(self.msg_to_cell.weight)
        nn.init.normal_(self.cell_bias_proj.weight, mean=0.0, std=0.02)
        nn.init.xavier_uniform_(self.q_proj.weight)
        nn.init.xavier_uniform_(self.k_weight)
        nn.init.xavier_uniform_(self.v_weight)
        nn.init.xavier_uniform_(self.msg_out.weight)
        nn.init.xavier_uniform_(self.output_cell_weight)
        nn.init.zeros_(self.output_cell_bias)
        nn.init.normal_(self.readout_query, mean=0.0, std=1.0 / math.sqrt(max(1, self.hidden_size)))
        nn.init.xavier_uniform_(self.readout_out.weight)
        if self.readout_out.bias is not None:
            nn.init.zeros_(self.readout_out.bias)

    def init_state(self, batch: int, *, device: torch.device | str = "cpu", dtype: torch.dtype) -> TensorDict:
        state = TensorDict({}, batch_size=[])
        state["cells"] = torch.zeros(batch, self.coords.shape[0], self.hidden_size, device=device, dtype=dtype)
        for family_name in self._family_names:
            state[family_name] = self.family_modules[family_name].init_state(
                batch=batch,
                device=device,
                dtype=dtype,
            )
        return state

    def reset_state(self, state: MaybeState, mask: ResetMask) -> MaybeState:
        if state is None or not isinstance(state, TensorDictBase):
            return state
        cells = state.get("cells")
        state_device = cells.device if torch.is_tensor(cells) else torch.device("cpu")
        batch_mask = torch.as_tensor(mask, dtype=torch.bool, device=state_device)
        if batch_mask.dim() != 1:
            raise ValueError(f"FabricRuntime.reset_state expects a 1D mask, got shape {tuple(batch_mask.shape)}")
        out = TensorDict({}, batch_size=[])
        if torch.is_tensor(cells):
            out["cells"] = torch.where(batch_mask.view(-1, 1, 1), torch.zeros_like(cells), cells)
        for family_name in self._family_names:
            family_state = state.get(family_name)
            if family_state is None:
                continue
            out[family_name] = self.family_modules[family_name].reset_state(family_state, batch_mask)
        return out

    def forward(
        self,
        hidden_input: Tensor,
        state: MaybeState = None,
        *,
        resets: Optional[ResetMask] = None,
        k: int | torch.Tensor | None = None,
        mode: ExecutionMode | None = None,
    ) -> tuple[Tensor, MaybeState]:
        y_cells, next_state = self.forward_cells(
            hidden_input=hidden_input,
            state=state,
            resets=resets,
            k=k,
            mode=mode,
        )
        if y_cells.dim() == 3:
            return self._readout(y_cells.unsqueeze(1)).squeeze(1), next_state
        return self._readout(y_cells), next_state

    def forward_cells(
        self,
        hidden_input: Tensor | None = None,
        state: MaybeState = None,
        *,
        resets: Optional[ResetMask] = None,
        k: int | torch.Tensor | None = None,
        boundary_input: torch.Tensor | None = None,
        mode: ExecutionMode | None = None,
    ) -> tuple[Tensor, MaybeState]:
        """Run the fabric over either per-step hidden vectors or direct boundary-cell values.

        `hidden_input` is a single vector per timestep with shape `[B, H]` or `[B, T, H]`.
        The runtime projects it into the boundary input cells internally.

        `boundary_input` is already in boundary-cell space with shape `[B, P, H]` or
        `[B, T, P, H]`, where `P` is the number of boundary input cells.
        """
        if hidden_input is None and boundary_input is None:
            raise ValueError("forward_cells requires either hidden_input or boundary_input")

        step_mode = (boundary_input.dim() == 3) if boundary_input is not None else (hidden_input.dim() == 2)
        if boundary_input is not None:
            boundary_seq = boundary_input.unsqueeze(1) if step_mode else boundary_input
            if boundary_seq.dim() != 4:
                raise ValueError(
                    f"FabricRuntime boundary_input expects [B,P,D] or [B,T,P,D], got {tuple(boundary_input.shape)}"
                )
            batch_size, time_steps, port_count, msg_dim = boundary_seq.shape
            if port_count != self.input_cell_idx.numel():
                raise ValueError(
                    "FabricRuntime boundary_input count="
                    f"{port_count} must match input cells={self.input_cell_idx.numel()}"
                )
            if msg_dim != self.hidden_size:
                raise ValueError(
                    f"FabricRuntime boundary_input dim={msg_dim} must match hidden_size={self.hidden_size}"
                )
            hidden_seq = None
        else:
            assert hidden_input is not None
            hidden_seq = hidden_input.unsqueeze(1) if step_mode else hidden_input
            if hidden_seq.dim() != 3:
                raise ValueError(
                    f"FabricRuntime hidden_input expects [B,H] or [B,T,H], got {tuple(hidden_input.shape)}"
                )
            batch_size, time_steps, hidden_size = hidden_seq.shape
            if hidden_size != self.hidden_size:
                raise ValueError(
                    f"FabricRuntime hidden_size={self.hidden_size} requires input dim "
                    f"{self.hidden_size}, got {hidden_size}"
                )
            boundary_seq = None

        device = boundary_seq.device if boundary_seq is not None else hidden_seq.device
        dtype = boundary_seq.dtype if boundary_seq is not None else hidden_seq.dtype
        current_state = self._ensure_state(state, batch=batch_size, device=device, dtype=dtype)
        family_resets = _expand_resets_for_time(resets, batch_size=batch_size, time_steps=time_steps, device=device)
        capture_active = bool(device.type == "cuda" and torch.cuda.is_current_stream_capturing())
        step_reset_flags: list[bool] | None = None
        if family_resets is not None:
            if capture_active:
                step_reset_flags = [True] * time_steps
            else:
                if family_resets.dim() == 1:
                    reset_any = family_resets.any().view(1)
                else:
                    reset_any = family_resets.any(dim=0)
                step_reset_flags = reset_any.to(device="cpu", dtype=torch.bool).tolist()
        execution_mode = self.config.execution_mode if mode is None else mode
        cell_bias = self.cell_bias_proj(self.slot_embed).view(1, 1, self.coords.shape[0], self.hidden_size)
        recurrent_cell_bias = cell_bias[:, :, self.recurrent_cell_idx, :].squeeze(1)
        q = self.q_proj(self.slot_embed).view(self.coords.shape[0], self.head_dim)
        recurrent_q = q.index_select(0, self.recurrent_cell_idx)
        output_q = q.index_select(0, self.output_cell_idx)
        gathered_kv_weight = torch.cat(
            (
                self.k_weight.index_select(0, self.kv_group_id),
                self.v_weight.index_select(0, self.kv_group_id),
            ),
            dim=-1,
        )
        sender_kv_weight = gathered_kv_weight.index_select(0, self.sender_cell_idx)
        sender_input_to_kv_weight = torch.einsum("dh,sdm->shm", self.public_proj.weight, sender_kv_weight)
        recurrent_sender_input_to_kv_weight = sender_input_to_kv_weight.index_select(0, self.recurrent_sender_idx)
        value_to_cell_weight = self.msg_to_cell.weight @ self.msg_out.weight
        value_to_output_weight = torch.einsum("dv,pdh->pvh", self.msg_out.weight, self.output_cell_weight)
        constant_k = self._resolve_constant_k_host(k)
        family_materialized = {
            name: (
                self.family_modules[name].materialize_params()
                if hasattr(self.family_modules[name], "materialize_params")
                else None
            )
            for name in self._family_names
        }
        if execution_mode == "stream":
            if step_mode:
                if constant_k is None:
                    k_rows, max_steps = self._resolve_step_k(
                        k,
                        batch_size=batch_size,
                        time_steps=time_steps,
                        step_index=0,
                        device=device,
                    )
                    all_active = None
                else:
                    k_rows = torch.full((batch_size,), constant_k, device=device, dtype=torch.long)
                    max_steps = constant_k
                    all_active = constant_k > 0
                step_resets = family_resets[:, 0] if family_resets is not None else None
                return self._forward_stream_step(
                    hidden_step=hidden_seq[:, 0] if hidden_seq is not None else None,
                    state=current_state,
                    resets=step_resets,
                    has_resets=step_reset_flags[0] if step_reset_flags is not None else None,
                    capture_active=capture_active,
                    k_rows=k_rows,
                    max_steps=max_steps,
                    all_active=all_active if max_steps <= 1 else None,
                    q=q,
                    recurrent_q=recurrent_q,
                    output_q=output_q,
                    gathered_kv_weight=gathered_kv_weight,
                    sender_kv_weight=sender_kv_weight,
                    sender_input_to_kv_weight=sender_input_to_kv_weight,
                    recurrent_sender_input_to_kv_weight=recurrent_sender_input_to_kv_weight,
                    value_to_cell_weight=value_to_cell_weight,
                    value_to_output_weight=value_to_output_weight,
                    cell_bias=cell_bias,
                    recurrent_cell_bias=recurrent_cell_bias,
                    boundary_step=boundary_seq[:, 0] if boundary_seq is not None else None,
                    family_materialized=family_materialized,
                )

            outputs: list[torch.Tensor] = []
            running_state = current_state
            constant_k_rows = None
            constant_max_steps = None
            constant_all_active = None
            step_family_state_cache = None
            if constant_k is not None:
                constant_k_rows = torch.full((batch_size,), constant_k, device=device, dtype=torch.long)
                constant_max_steps = constant_k
                constant_all_active = constant_k > 0
                if constant_k > 0:
                    step_family_state_cache = self._prepare_stream_step_family_cache(
                        running_state,
                        batch=batch_size,
                        device=device,
                        dtype=dtype,
                    )
            for step_index in range(time_steps):
                if constant_k_rows is None or constant_max_steps is None:
                    k_rows, max_steps = self._resolve_step_k(
                        k,
                        batch_size=batch_size,
                        time_steps=time_steps,
                        step_index=step_index,
                        device=device,
                    )
                    all_active = None
                else:
                    k_rows, max_steps = constant_k_rows, constant_max_steps
                    all_active = constant_all_active if max_steps <= 1 else None
                step_resets = family_resets[:, step_index] if family_resets is not None else None
                y_step, running_state = self._forward_stream_step(
                    hidden_step=hidden_seq[:, step_index] if hidden_seq is not None else None,
                    state=running_state,
                    resets=step_resets,
                    has_resets=step_reset_flags[step_index] if step_reset_flags is not None else None,
                    capture_active=capture_active,
                    k_rows=k_rows,
                    max_steps=max_steps,
                    all_active=all_active,
                    q=q,
                    recurrent_q=recurrent_q,
                    output_q=output_q,
                    gathered_kv_weight=gathered_kv_weight,
                    sender_kv_weight=sender_kv_weight,
                    sender_input_to_kv_weight=sender_input_to_kv_weight,
                    recurrent_sender_input_to_kv_weight=recurrent_sender_input_to_kv_weight,
                    value_to_cell_weight=value_to_cell_weight,
                    value_to_output_weight=value_to_output_weight,
                    cell_bias=cell_bias,
                    recurrent_cell_bias=recurrent_cell_bias,
                    boundary_step=boundary_seq[:, step_index] if boundary_seq is not None else None,
                    family_materialized=family_materialized,
                    step_family_state_cache=step_family_state_cache,
                )
                outputs.append(y_step)
            if step_family_state_cache is not None:
                self._apply_stream_step_family_cache(running_state, step_family_state_cache)
            return torch.stack(outputs, dim=1), running_state

        if execution_mode == "diffusion":
            k_rows, max_steps = self._resolve_k(k, batch_size=batch_size, time_steps=time_steps, device=device)
            y_diff, next_state = self._forward_diffusion(
                hidden_seq=hidden_seq,
                state=current_state,
                resets=family_resets,
                k_rows=k_rows,
                max_steps=max_steps,
                q=q,
                gathered_kv_weight=gathered_kv_weight,
                cell_bias=cell_bias,
                boundary_seq=boundary_seq,
                family_materialized=family_materialized,
            )
            if step_mode:
                return y_diff.squeeze(1), next_state
            return y_diff, next_state

        raise ValueError(f"Unsupported fabric execution mode {execution_mode}")

    def _resolve_k(
        self,
        k: int | torch.Tensor | None,
        *,
        batch_size: int,
        time_steps: int,
        device: torch.device,
    ) -> tuple[torch.Tensor, int]:
        if k is None:
            max_steps = int(self.config.default_k)
            k_rows = torch.full((batch_size,), max_steps, device=device, dtype=torch.long)
        elif isinstance(k, int):
            max_steps = max(0, min(int(self.config.k_max), int(k)))
            k_rows = torch.full((batch_size,), max_steps, device=device, dtype=torch.long)
        else:
            k_tensor = torch.as_tensor(k, device=device, dtype=torch.long)
            if k_tensor.dim() == 1 and k_tensor.shape[0] == batch_size:
                k_rows = k_tensor
            elif k_tensor.dim() == 2 and k_tensor.shape == (batch_size, time_steps):
                first = k_tensor[:, :1]
                if not bool((k_tensor == first).all()):
                    raise NotImplementedError(
                        "Per-timestep varying k within one sequence is not yet supported by "
                        "the current sequence-kernel runtime"
                    )
                k_rows = first.reshape(batch_size)
            else:
                raise ValueError(f"k must be int, [B], or [B,T], got shape {tuple(k_tensor.shape)}")

            k_rows = k_rows.clamp(min=0, max=int(self.config.k_max))
            max_steps = int(k_rows.max().item()) if k_rows.numel() > 0 else 0
        return k_rows, max_steps

    def _resolve_constant_k_host(self, k: int | torch.Tensor | None) -> int | None:
        if k is None:
            return int(self.config.default_k)
        if isinstance(k, int):
            return max(0, min(int(self.config.k_max), int(k)))
        return None

    def _resolve_step_k(
        self,
        k: int | torch.Tensor | None,
        *,
        batch_size: int,
        time_steps: int,
        step_index: int,
        device: torch.device,
    ) -> tuple[torch.Tensor, int]:
        if k is None:
            k_rows = torch.full((batch_size,), int(self.config.default_k), device=device, dtype=torch.long)
        elif isinstance(k, int):
            k_rows = torch.full((batch_size,), int(k), device=device, dtype=torch.long)
        else:
            k_tensor = torch.as_tensor(k, device=device, dtype=torch.long)
            if k_tensor.dim() == 1 and k_tensor.shape[0] == batch_size:
                k_rows = k_tensor
            elif k_tensor.dim() == 2 and k_tensor.shape == (batch_size, time_steps):
                k_rows = k_tensor[:, step_index]
            else:
                raise ValueError(f"k must be int, [B], or [B,T], got shape {tuple(k_tensor.shape)}")
        k_rows = k_rows.clamp(min=0, max=int(self.config.k_max))
        max_steps = int(k_rows.max().item()) if k_rows.numel() > 0 else 0
        return k_rows, max_steps

    def _constant_step_flat(
        self,
        step_idx: int,
        *,
        batch_size: int,
        time_steps: int,
        device: torch.device,
        dtype: torch.dtype,
    ) -> torch.Tensor:
        key = (
            device.type,
            -1 if device.index is None else int(device.index),
            batch_size,
            time_steps,
            str(dtype),
            int(step_idx),
        )
        cached = self._constant_step_flat_cache.get(key)
        if cached is None or cached.device != device:
            cached = torch.full((batch_size * time_steps,), step_idx, device=device, dtype=dtype)
            self._constant_step_flat_cache[key] = cached
        return cached

    def _ensure_state(
        self,
        state: MaybeState,
        *,
        batch: int,
        device: torch.device,
        dtype: torch.dtype,
    ) -> TensorDict:
        if state is None or not isinstance(state, TensorDictBase):
            return self.init_state(batch=batch, device=device, dtype=dtype)
        out = TensorDict({}, batch_size=[])
        cells = state.get("cells")
        expected_cells = (batch, self.coords.shape[0], self.hidden_size)
        if not torch.is_tensor(cells) or tuple(cells.shape) != expected_cells:
            out["cells"] = torch.zeros(*expected_cells, device=device, dtype=dtype)
        else:
            out["cells"] = cells.to(device=device, dtype=dtype)
        for family_name in self._family_names:
            family_state = state.get(family_name)
            expected = torch.Size([self._family_num_cells(family_name), batch])
            if family_state is None or family_state.batch_size != expected:
                out[family_name] = self.family_modules[family_name].init_state(batch=batch, device=device, dtype=dtype)
            else:
                out[family_name] = family_state
        return out

    def _forward_stream_step(
        self,
        *,
        hidden_step: torch.Tensor | None,
        state: TensorDict,
        resets: torch.Tensor | None,
        has_resets: bool | None,
        capture_active: bool,
        k_rows: torch.Tensor,
        max_steps: int,
        all_active: bool | None,
        q: torch.Tensor,
        recurrent_q: torch.Tensor,
        output_q: torch.Tensor,
        gathered_kv_weight: torch.Tensor,
        sender_kv_weight: torch.Tensor,
        sender_input_to_kv_weight: torch.Tensor,
        recurrent_sender_input_to_kv_weight: torch.Tensor,
        value_to_cell_weight: torch.Tensor,
        value_to_output_weight: torch.Tensor,
        cell_bias: torch.Tensor,
        recurrent_cell_bias: torch.Tensor,
        boundary_step: torch.Tensor | None,
        family_materialized: dict[str, object | None],
        step_family_state_cache: dict[str, object] | None = None,
    ) -> tuple[torch.Tensor, TensorDict]:
        current_state = state
        if resets is not None and (capture_active or has_resets is True):
            if step_family_state_cache is not None:
                self._reset_stream_step_family_cache(step_family_state_cache, resets)
            reset_state = self.reset_state(current_state, resets)
            assert isinstance(reset_state, TensorDictBase)
            current_state = TensorDict(reset_state.to_dict(), batch_size=[])

        cells_prev = current_state["cells"]
        family_state = current_state
        family_resets = resets.view(-1, 1) if resets is not None else None

        if max_steps <= 1:
            return self._forward_stream_step_k1(
                cells_prev=cells_prev,
                family_state=family_state,
                family_resets=family_resets,
                k_rows=k_rows,
                all_active=all_active,
                recurrent_q=recurrent_q,
                output_q=output_q,
                sender_input_to_kv_weight=sender_input_to_kv_weight,
                recurrent_sender_input_to_kv_weight=recurrent_sender_input_to_kv_weight,
                value_to_cell_weight=value_to_cell_weight,
                value_to_output_weight=value_to_output_weight,
                recurrent_cell_bias=recurrent_cell_bias,
                boundary_step=boundary_step,
                family_materialized=family_materialized,
                step_family_state_cache=step_family_state_cache,
            )
        if boundary_step is not None and hidden_step is None:
            return self._forward_stream_step_boundary_multistep(
                cells_prev=cells_prev,
                family_state=family_state,
                family_resets=family_resets,
                k_rows=k_rows,
                max_steps=max_steps,
                recurrent_q=recurrent_q,
                output_q=output_q,
                sender_input_to_kv_weight=sender_input_to_kv_weight,
                recurrent_sender_input_to_kv_weight=recurrent_sender_input_to_kv_weight,
                value_to_cell_weight=value_to_cell_weight,
                value_to_output_weight=value_to_output_weight,
                recurrent_cell_bias=recurrent_cell_bias,
                boundary_step=boundary_step,
                family_materialized=family_materialized,
                step_family_state_cache=step_family_state_cache,
            )

        if boundary_step is not None:
            cells_prev = cells_prev.clone()
            if self._partitioned_layout:
                cells_prev[:, self._input_slice, :] = boundary_step
            else:
                cells_prev[:, self.input_cell_idx, :] = boundary_step

        y_prev = cells_prev.unsqueeze(1)
        use_packed_loop_cache = (
            step_family_state_cache is not None
            and self._full_recurrent_family_name is not None
            and self._full_recurrent_family_name in step_family_state_cache
        )
        boundary_step_seq = boundary_step.unsqueeze(1) if boundary_step is not None else None
        zero_output_step = None
        if use_packed_loop_cache and boundary_step_seq is not None and self._partitioned_layout:
            zero_output_step = cells_prev.new_zeros(cells_prev.shape[0], 1, self._num_output_cells, self.hidden_size)

        for step_idx in range(max_steps):
            z_prev = self.public_proj(y_prev)
            msg = self._compute_messages(
                z_prev,
                q=q,
                gathered_kv_weight=gathered_kv_weight,
                step_idx=step_idx + 1,
            )
            if hidden_step is not None and (self.config.inject_every_step or step_idx == 0):
                msg = self._inject_hidden_inputs(msg, hidden_step.unsqueeze(1))
            family_input = self.msg_to_cell(msg) + cell_bias
            if use_packed_loop_cache:
                family_y = self._run_family_updates_step_cached(
                    family_input,
                    resets=family_resets,
                    family_materialized=family_materialized,
                    step_family_state_cache=step_family_state_cache,
                )
                if zero_output_step is not None and boundary_step_seq is not None:
                    y_next = torch.cat((boundary_step_seq, family_y.unsqueeze(1), zero_output_step), dim=2)
                else:
                    y_next = family_input.new_zeros(family_input.shape)
                    family_name = self._full_recurrent_family_name
                    assert family_name is not None
                    family_idx = self._family_indices(family_name)
                    y_next[:, 0, family_idx, :] = family_y.to(dtype=y_next.dtype)
            else:
                y_next, next_family_state = self._run_family_updates(
                    family_input,
                    family_state,
                    resets=family_resets,
                    batch_size=y_prev.shape[0],
                    time_steps=1,
                    family_materialized=family_materialized,
                )
            if boundary_step_seq is not None and not (use_packed_loop_cache and zero_output_step is not None):
                y_next[:, :, self.input_cell_idx, :] = boundary_step_seq
            active_rows = step_idx < k_rows
            y_prev = torch.where(active_rows.view(-1, 1, 1, 1), y_next, y_prev)
            if not use_packed_loop_cache:
                family_state = self._blend_family_states(family_state, next_family_state, active_rows)

        final_z = self.public_proj(y_prev)
        final_msg = self._compute_messages(
            final_z,
            q=q,
            gathered_kv_weight=gathered_kv_weight,
            step_idx=k_rows,
        )
        output_cells = self._project_output_cells(final_msg[:, :, self.output_cell_idx, :]).to(dtype=y_prev.dtype)
        if zero_output_step is not None and boundary_step_seq is not None:
            y_out = torch.cat((boundary_step_seq, y_prev[:, :, self._recurrent_slice, :], output_cells), dim=2)
        else:
            y_out = y_prev.clone()
            y_out[:, :, self.output_cell_idx, :] = output_cells
        next_state = TensorDict({}, batch_size=[])
        next_state["cells"] = y_out.squeeze(1)
        for family_name in self._family_names:
            next_state[family_name] = family_state[family_name]
        return y_out.squeeze(1), next_state

    def _forward_stream_step_k1(
        self,
        *,
        cells_prev: torch.Tensor,
        family_state: TensorDict,
        family_resets: torch.Tensor | None,
        k_rows: torch.Tensor,
        all_active: bool | None,
        recurrent_q: torch.Tensor,
        output_q: torch.Tensor,
        sender_input_to_kv_weight: torch.Tensor,
        recurrent_sender_input_to_kv_weight: torch.Tensor,
        value_to_cell_weight: torch.Tensor,
        value_to_output_weight: torch.Tensor,
        recurrent_cell_bias: torch.Tensor,
        boundary_step: torch.Tensor | None,
        family_materialized: dict[str, object | None],
        step_family_state_cache: dict[str, object] | None = None,
    ) -> tuple[torch.Tensor, TensorDict]:
        if self._partitioned_layout:
            if boundary_step is None:
                input_prev = cells_prev[:, self._input_slice, :]
                sender_cells_prev = cells_prev[:, : self._num_input_cells + self._num_recurrent_cells, :]
            else:
                input_prev = boundary_step
                sender_cells_prev = None
            recurrent_slice = self._recurrent_slice
            output_slice = self._output_slice
            recurrent_prev = cells_prev[:, recurrent_slice, :]
            if sender_cells_prev is None:
                sender_cells_prev = torch.cat((input_prev, recurrent_prev), dim=1)
        else:
            if boundary_step is None:
                sender_cells_prev = cells_prev.index_select(1, self.sender_cell_idx)
            else:
                cells_prev = cells_prev.clone()
                cells_prev[:, self.input_cell_idx, :] = boundary_step
                sender_cells_prev = cells_prev.index_select(1, self.sender_cell_idx)
            recurrent_slice = None
            output_slice = None
            recurrent_prev = cells_prev[:, self.recurrent_cell_idx, :]
        if not self._partitioned_layout:
            input_prev = None
            sender_cells_prev = cells_prev.index_select(1, self.sender_cell_idx)
        assert sender_cells_prev is not None
        k_all, v_all = self._project_sender_kv_from_cells_step(
            sender_cells_prev,
            sender_input_to_kv_weight=sender_input_to_kv_weight,
        )
        if self._partitioned_layout:
            input_k = k_all[:, : self._num_input_cells, :]
            input_v = v_all[:, : self._num_input_cells, :]
        if all_active is False:
            recurrent_mid = recurrent_prev
            blended_family_state = family_state
            final_k = k_all
            final_v = v_all
        else:
            recurrent_msg = self._compute_messages_step_subset_raw(
                k_all,
                v_all,
                q_subset=recurrent_q,
                neighbor_idx=self.recurrent_neighbor_idx,
                neighbor_valid=self.recurrent_neighbor_valid,
                edge_distance=self.recurrent_edge_distance,
                edge_delay=self.recurrent_edge_delay,
                use_delay=self._has_edge_delay,
                step_idx=1,
            )
            recurrent_input = torch.nn.functional.linear(recurrent_msg, value_to_cell_weight) + recurrent_cell_bias
            recurrent_next, next_family_state = self._run_family_updates_recurrent_step(
                recurrent_input,
                family_state,
                resets=family_resets,
                batch_size=cells_prev.shape[0],
                family_materialized=family_materialized,
                step_family_state_cache=step_family_state_cache if all_active is True else None,
            )
            if all_active is True:
                recurrent_mid = recurrent_next
                blended_family_state = next_family_state
            else:
                active_rows = k_rows > 0
                recurrent_mid = torch.where(active_rows.view(-1, 1, 1), recurrent_next, recurrent_prev)
                blended_family_state = self._blend_family_states(family_state, next_family_state, active_rows)

            recurrent_k, recurrent_v = self._project_sender_kv_from_cells_step(
                recurrent_mid,
                sender_input_to_kv_weight=recurrent_sender_input_to_kv_weight,
            )
            if self._partitioned_layout:
                final_k = torch.cat((input_k, recurrent_k), dim=1)
                final_v = torch.cat((input_v, recurrent_v), dim=1)
            else:
                final_k = k_all.clone()
                final_v = v_all.clone()
                final_k[:, self.recurrent_sender_idx, :] = recurrent_k
                final_v[:, self.recurrent_sender_idx, :] = recurrent_v
        output_step_idx: int | torch.Tensor = 1 if all_active is True else k_rows
        output_msg = self._compute_messages_step_subset_raw(
            final_k,
            final_v,
            q_subset=output_q,
            neighbor_idx=self.output_neighbor_idx,
            neighbor_valid=self.output_neighbor_valid,
            edge_distance=self.output_edge_distance,
            edge_delay=self.output_edge_delay,
            use_delay=self._has_edge_delay,
            step_idx=output_step_idx,
        )
        output_cells = self._project_output_cells_step_raw(
            output_msg,
            value_to_output_weight=value_to_output_weight,
        ).to(dtype=cells_prev.dtype)
        if output_slice is not None:
            assert input_prev is not None
            cells_out = torch.cat((input_prev, recurrent_mid, output_cells), dim=1)
        else:
            cells_out = cells_prev.clone()
            cells_out[:, self.recurrent_cell_idx, :] = recurrent_mid
            cells_out[:, self.output_cell_idx, :] = output_cells
        next_state = TensorDict({}, batch_size=[])
        next_state["cells"] = cells_out
        for family_name in self._family_names:
            next_state[family_name] = blended_family_state[family_name]
        return cells_out, next_state

    def _forward_stream_step_boundary_multistep(
        self,
        *,
        cells_prev: torch.Tensor,
        family_state: TensorDict,
        family_resets: torch.Tensor | None,
        k_rows: torch.Tensor,
        max_steps: int,
        recurrent_q: torch.Tensor,
        output_q: torch.Tensor,
        sender_input_to_kv_weight: torch.Tensor,
        recurrent_sender_input_to_kv_weight: torch.Tensor,
        value_to_cell_weight: torch.Tensor,
        value_to_output_weight: torch.Tensor,
        recurrent_cell_bias: torch.Tensor,
        boundary_step: torch.Tensor,
        family_materialized: dict[str, object | None],
        step_family_state_cache: dict[str, object] | None = None,
    ) -> tuple[torch.Tensor, TensorDict]:
        batch_size = cells_prev.shape[0]
        recurrent_mid = cells_prev[:, self.recurrent_cell_idx, :]
        input_sender_input_to_kv_weight = sender_input_to_kv_weight.index_select(0, self.input_sender_idx)
        input_k, input_v = self._project_sender_kv_from_cells_step(
            boundary_step,
            sender_input_to_kv_weight=input_sender_input_to_kv_weight,
        )
        use_packed_cache = step_family_state_cache is not None
        running_family_state = family_state

        for step_idx in range(max_steps):
            recurrent_k, recurrent_v = self._project_sender_kv_from_cells_step(
                recurrent_mid,
                sender_input_to_kv_weight=recurrent_sender_input_to_kv_weight,
            )
            if self._partitioned_layout:
                k_all = torch.cat((input_k, recurrent_k), dim=1)
                v_all = torch.cat((input_v, recurrent_v), dim=1)
            else:
                k_all = input_k.new_zeros(batch_size, self.sender_cell_idx.numel(), self.head_dim)
                v_all = input_v.new_zeros(batch_size, self.sender_cell_idx.numel(), self.value_dim)
                k_all[:, self.input_sender_idx, :] = input_k
                v_all[:, self.input_sender_idx, :] = input_v
                k_all[:, self.recurrent_sender_idx, :] = recurrent_k
                v_all[:, self.recurrent_sender_idx, :] = recurrent_v
            recurrent_msg = self._compute_messages_step_subset_raw(
                k_all,
                v_all,
                q_subset=recurrent_q,
                neighbor_idx=self.recurrent_neighbor_idx,
                neighbor_valid=self.recurrent_neighbor_valid,
                edge_distance=self.recurrent_edge_distance,
                edge_delay=self.recurrent_edge_delay,
                use_delay=self._has_edge_delay,
                step_idx=step_idx + 1,
            )
            recurrent_input = torch.nn.functional.linear(recurrent_msg, value_to_cell_weight) + recurrent_cell_bias
            recurrent_next, next_family_state = self._run_family_updates_recurrent_step(
                recurrent_input,
                running_family_state,
                resets=family_resets,
                batch_size=batch_size,
                family_materialized=family_materialized,
                step_family_state_cache=step_family_state_cache,
            )
            active_rows = step_idx < k_rows
            recurrent_mid = torch.where(active_rows.view(-1, 1, 1), recurrent_next, recurrent_mid)
            if not use_packed_cache:
                running_family_state = self._blend_family_states(running_family_state, next_family_state, active_rows)

        recurrent_k, recurrent_v = self._project_sender_kv_from_cells_step(
            recurrent_mid,
            sender_input_to_kv_weight=recurrent_sender_input_to_kv_weight,
        )
        if self._partitioned_layout:
            final_k = torch.cat((input_k, recurrent_k), dim=1)
            final_v = torch.cat((input_v, recurrent_v), dim=1)
            output_cells = self._project_output_cells_step_raw(
                self._compute_messages_step_subset_raw(
                    final_k,
                    final_v,
                    q_subset=output_q,
                    neighbor_idx=self.output_neighbor_idx,
                    neighbor_valid=self.output_neighbor_valid,
                    edge_distance=self.output_edge_distance,
                    edge_delay=self.output_edge_delay,
                    use_delay=self._has_edge_delay,
                    step_idx=k_rows,
                ),
                value_to_output_weight=value_to_output_weight,
            ).to(dtype=cells_prev.dtype)
            cells_out = torch.cat((boundary_step, recurrent_mid, output_cells), dim=1)
        else:
            final_k = input_k.new_zeros(batch_size, self.sender_cell_idx.numel(), self.head_dim)
            final_v = input_v.new_zeros(batch_size, self.sender_cell_idx.numel(), self.value_dim)
            final_k[:, self.input_sender_idx, :] = input_k
            final_v[:, self.input_sender_idx, :] = input_v
            final_k[:, self.recurrent_sender_idx, :] = recurrent_k
            final_v[:, self.recurrent_sender_idx, :] = recurrent_v
            output_cells = self._project_output_cells_step_raw(
                self._compute_messages_step_subset_raw(
                    final_k,
                    final_v,
                    q_subset=output_q,
                    neighbor_idx=self.output_neighbor_idx,
                    neighbor_valid=self.output_neighbor_valid,
                    edge_distance=self.output_edge_distance,
                    edge_delay=self.output_edge_delay,
                    use_delay=self._has_edge_delay,
                    step_idx=k_rows,
                ),
                value_to_output_weight=value_to_output_weight,
            ).to(dtype=cells_prev.dtype)
            cells_out = cells_prev.clone()
            cells_out[:, self.input_cell_idx, :] = boundary_step
            cells_out[:, self.recurrent_cell_idx, :] = recurrent_mid
            cells_out[:, self.output_cell_idx, :] = output_cells
        next_state = TensorDict({}, batch_size=[])
        next_state["cells"] = cells_out
        for family_name in self._family_names:
            next_state[family_name] = running_family_state[family_name]
        return cells_out, next_state

    def _forward_diffusion(
        self,
        *,
        hidden_seq: torch.Tensor | None,
        state: TensorDict,
        resets: torch.Tensor | None,
        k_rows: torch.Tensor,
        max_steps: int,
        q: torch.Tensor,
        gathered_kv_weight: torch.Tensor,
        cell_bias: torch.Tensor,
        boundary_seq: torch.Tensor | None,
        family_materialized: dict[str, object | None],
    ) -> tuple[torch.Tensor, TensorDict]:
        batch_size = state["cells"].shape[0]
        time_steps = boundary_seq.shape[1] if boundary_seq is not None else hidden_seq.shape[1]
        y_prev = state["cells"].unsqueeze(1).expand(batch_size, time_steps, -1, -1).clone()
        if resets is not None:
            y_prev = torch.where(resets.view(batch_size, time_steps, 1, 1), torch.zeros_like(y_prev), y_prev)
        if boundary_seq is not None:
            if self._partitioned_layout:
                y_prev[:, :, self._input_slice, :] = boundary_seq
            else:
                y_prev[:, :, self.input_cell_idx, :] = boundary_seq
        family_state = state

        for step_idx in range(max_steps):
            z_prev = self.public_proj(y_prev)
            msg = self._compute_messages(
                z_prev,
                q=q,
                gathered_kv_weight=gathered_kv_weight,
                step_idx=step_idx + 1,
            )
            if hidden_seq is not None and (self.config.inject_every_step or step_idx == 0):
                msg = self._inject_hidden_inputs(msg, hidden_seq)
            family_input = self.msg_to_cell(msg) + cell_bias
            y_next, next_family_state = self._run_family_updates(
                family_input,
                family_state,
                resets=resets,
                batch_size=batch_size,
                time_steps=time_steps,
                family_materialized=family_materialized,
            )
            if boundary_seq is not None:
                if self._partitioned_layout:
                    y_next[:, :, self._input_slice, :] = boundary_seq
                else:
                    y_next[:, :, self.input_cell_idx, :] = boundary_seq
            active_rows = step_idx < k_rows
            y_prev = torch.where(active_rows.view(batch_size, 1, 1, 1), y_next, y_prev)
            family_state = self._blend_family_states(family_state, next_family_state, active_rows)

        final_z = self.public_proj(y_prev)
        final_msg = self._compute_messages(
            final_z,
            q=q,
            gathered_kv_weight=gathered_kv_weight,
            step_idx=k_rows,
        )
        y_out = y_prev.clone()
        y_out[:, :, self.output_cell_idx, :] = self._project_output_cells(final_msg[:, :, self.output_cell_idx, :]).to(
            dtype=y_out.dtype
        )
        next_state = TensorDict({}, batch_size=[])
        next_state["cells"] = y_out[:, -1].clone()
        for family_name in self._family_names:
            next_state[family_name] = family_state[family_name]
        return y_out, next_state

    def _compute_messages(
        self,
        z_prev: torch.Tensor,
        *,
        q: torch.Tensor,
        gathered_kv_weight: torch.Tensor,
        step_idx: int | torch.Tensor,
    ) -> torch.Tensor:
        batch_size, time_steps, num_cells, _ = z_prev.shape
        flat_batch = batch_size * time_steps
        kv_all = torch.einsum("btnd,ndm->btnm", z_prev, gathered_kv_weight).reshape(
            flat_batch,
            num_cells,
            self.head_dim + self.value_dim,
        )
        k_all, v_all = kv_all.split((self.head_dim, self.value_dim), dim=-1)
        if z_prev.is_cuda:
            if z_prev.dtype != torch.float32:
                raise ValueError(f"Fabric CUDA message kernel requires float32 inputs, got {z_prev.dtype}")
            if isinstance(step_idx, int):
                step_flat = self._constant_step_flat(
                    step_idx,
                    batch_size=batch_size,
                    time_steps=time_steps,
                    device=z_prev.device,
                    dtype=self.edge_delay.dtype,
                )
            else:
                step_flat = _flatten_step_idx(
                    step_idx,
                    batch_size=batch_size,
                    time_steps=time_steps,
                    device=z_prev.device,
                    dtype=self.edge_delay.dtype,
                )
            msg_flat = fabric_sparse_message_cuda(
                q,
                k_all,
                v_all,
                self.neighbor_idx,
                self.neighbor_valid,
                self.edge_distance,
                self.edge_delay,
                step_flat,
                distance_scale=float(self.config.distance_logit_scale),
                use_delay=self._has_edge_delay,
            ).view(batch_size, time_steps, num_cells, self.value_dim)
            return self.msg_out(msg_flat)
        return self._compute_messages_reference(
            k_all,
            v_all,
            batch_size=batch_size,
            time_steps=time_steps,
            num_cells=num_cells,
            q=q,
            step_idx=step_idx,
        )

    def _compute_messages_reference(
        self,
        k_all: torch.Tensor,
        v_all: torch.Tensor,
        *,
        batch_size: int,
        time_steps: int,
        num_cells: int,
        q: torch.Tensor,
        step_idx: int | torch.Tensor,
    ) -> torch.Tensor:
        flat_batch = batch_size * time_steps
        k_neighbors = k_all.index_select(1, self.neighbor_idx_flat).view(
            flat_batch,
            num_cells,
            self._num_neighbors,
            self.head_dim,
        )
        v_neighbors = v_all.index_select(1, self.neighbor_idx_flat).view(
            flat_batch,
            num_cells,
            self._num_neighbors,
            self.value_dim,
        )
        q_scaled = q.view(1, num_cells, 1, self.head_dim) / math.sqrt(float(self.head_dim))
        logits = torch.bmm(
            q_scaled.expand(flat_batch, -1, -1, -1).reshape(flat_batch * num_cells, 1, self.head_dim),
            k_neighbors.reshape(flat_batch * num_cells, self._num_neighbors, self.head_dim).transpose(1, 2),
        ).view(flat_batch, num_cells, self._num_neighbors)
        valid_windows = self.neighbor_valid.view(1, num_cells, self._num_neighbors)
        if float(self.config.distance_logit_scale) > 0.0:
            logits = logits - float(self.config.distance_logit_scale) * self.edge_distance.view(
                1,
                num_cells,
                self._num_neighbors,
            )
        if self.spec.anatomy.edge_delay is not None:
            if isinstance(step_idx, int):
                valid_windows = valid_windows & (self.edge_delay.view(1, num_cells, self._num_neighbors) <= step_idx)
            else:
                step_tensor = torch.as_tensor(step_idx, device=k_all.device, dtype=self.edge_delay.dtype)
                if step_tensor.dim() == 1 and step_tensor.shape[0] == batch_size:
                    step_flat = step_tensor.view(batch_size, 1).expand(batch_size, time_steps).reshape(flat_batch)
                elif step_tensor.dim() == 2 and step_tensor.shape == (batch_size, time_steps):
                    step_flat = step_tensor.reshape(flat_batch)
                else:
                    raise ValueError(f"step_idx tensor must have shape [B] or [B,T], got {tuple(step_tensor.shape)}")
                valid_windows = valid_windows & (
                    self.edge_delay.view(1, num_cells, self._num_neighbors) <= step_flat.view(flat_batch, 1, 1)
                )
        logits = logits.masked_fill(~valid_windows, float("-inf"))
        weights = torch.softmax(logits.to(dtype=torch.float32), dim=-1).to(dtype=v_neighbors.dtype)
        weights = torch.where(valid_windows, weights, torch.zeros_like(weights))
        has_valid = valid_windows.any(dim=-1, keepdim=True)
        weights = torch.where(has_valid, weights, torch.zeros_like(weights))
        msg_flat = torch.bmm(
            weights.reshape(flat_batch * num_cells, 1, self._num_neighbors),
            v_neighbors.reshape(flat_batch * num_cells, self._num_neighbors, self.value_dim),
        ).view(batch_size, time_steps, num_cells, self.value_dim)
        return self.msg_out(msg_flat)

    def _project_sender_kv_step(
        self,
        z_prev_step: torch.Tensor,
        *,
        sender_kv_weight: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        sender_z = z_prev_step.index_select(1, self.sender_cell_idx)
        kv_all = torch.einsum("bnd,ndm->bnm", sender_z, sender_kv_weight)
        return kv_all.split((self.head_dim, self.value_dim), dim=-1)

    def _project_sender_kv_from_cells_step(
        self,
        sender_cells_step: torch.Tensor,
        *,
        sender_input_to_kv_weight: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        kv_all = torch.bmm(sender_cells_step.transpose(0, 1), sender_input_to_kv_weight).transpose(0, 1)
        return kv_all.split((self.head_dim, self.value_dim), dim=-1)

    def _compute_messages_step_subset(
        self,
        k_all: torch.Tensor,
        v_all: torch.Tensor,
        *,
        q_subset: torch.Tensor,
        neighbor_idx: torch.Tensor,
        neighbor_valid: torch.Tensor,
        edge_distance: torch.Tensor,
        edge_delay: torch.Tensor,
        use_delay: bool,
        step_idx: int | torch.Tensor,
    ) -> torch.Tensor:
        msg_flat = self._compute_messages_step_subset_raw(
            k_all,
            v_all,
            q_subset=q_subset,
            neighbor_idx=neighbor_idx,
            neighbor_valid=neighbor_valid,
            edge_distance=edge_distance,
            edge_delay=edge_delay,
            use_delay=use_delay,
            step_idx=step_idx,
        )
        return self.msg_out(msg_flat)

    def _compute_messages_step_subset_raw(
        self,
        k_all: torch.Tensor,
        v_all: torch.Tensor,
        *,
        q_subset: torch.Tensor,
        neighbor_idx: torch.Tensor,
        neighbor_valid: torch.Tensor,
        edge_distance: torch.Tensor,
        edge_delay: torch.Tensor,
        use_delay: bool,
        step_idx: int | torch.Tensor,
    ) -> torch.Tensor:
        batch_size, _, _ = k_all.shape
        num_receivers = neighbor_idx.shape[0]
        num_neighbors = neighbor_idx.shape[1]
        if k_all.is_cuda:
            if k_all.dtype != torch.float32:
                raise ValueError(f"Fabric CUDA message kernel requires float32 inputs, got {k_all.dtype}")
            if isinstance(step_idx, int):
                step_flat = self._constant_step_flat(
                    step_idx,
                    batch_size=batch_size,
                    time_steps=1,
                    device=k_all.device,
                    dtype=edge_delay.dtype,
                )
            else:
                step_flat = _flatten_step_idx(
                    step_idx,
                    batch_size=batch_size,
                    time_steps=1,
                    device=k_all.device,
                    dtype=edge_delay.dtype,
                )
            msg_flat = fabric_sparse_message_cuda(
                q_subset,
                k_all,
                v_all,
                neighbor_idx,
                neighbor_valid,
                edge_distance,
                edge_delay,
                step_flat,
                distance_scale=float(self.config.distance_logit_scale),
                use_delay=use_delay,
            )
            return msg_flat

        flat_neighbor_idx = neighbor_idx.reshape(-1)
        k_neighbors = k_all.index_select(1, flat_neighbor_idx).view(
            batch_size,
            num_receivers,
            num_neighbors,
            self.head_dim,
        )
        v_neighbors = v_all.index_select(1, flat_neighbor_idx).view(
            batch_size,
            num_receivers,
            num_neighbors,
            self.value_dim,
        )
        logits = (q_subset.view(1, num_receivers, 1, self.head_dim) * k_neighbors).sum(dim=-1) / math.sqrt(
            float(self.head_dim)
        )
        valid_windows = neighbor_valid.view(1, num_receivers, num_neighbors)
        if float(self.config.distance_logit_scale) > 0.0:
            logits = logits - float(self.config.distance_logit_scale) * edge_distance.view(
                1,
                num_receivers,
                num_neighbors,
            )
        if use_delay:
            if isinstance(step_idx, int):
                valid_windows = valid_windows & (edge_delay.view(1, num_receivers, num_neighbors) <= step_idx)
            else:
                step_tensor = torch.as_tensor(step_idx, device=k_all.device, dtype=edge_delay.dtype)
                if step_tensor.dim() != 1 or step_tensor.shape[0] != batch_size:
                    raise ValueError(f"step_idx tensor must have shape [B], got {tuple(step_tensor.shape)}")
                valid_windows = valid_windows & (
                    edge_delay.view(1, num_receivers, num_neighbors) <= step_tensor.view(batch_size, 1, 1)
                )
        logits = logits.masked_fill(~valid_windows, float("-inf"))
        weights = torch.softmax(logits.to(dtype=torch.float32), dim=-1).to(dtype=v_neighbors.dtype)
        weights = torch.where(valid_windows, weights, torch.zeros_like(weights))
        has_valid = valid_windows.any(dim=-1, keepdim=True)
        weights = torch.where(has_valid, weights, torch.zeros_like(weights))
        return torch.bmm(
            weights.reshape(batch_size * num_receivers, 1, num_neighbors),
            v_neighbors.reshape(batch_size * num_receivers, num_neighbors, self.value_dim),
        ).view(batch_size, num_receivers, self.value_dim)

    def _inject_hidden_inputs(self, msg: torch.Tensor, hidden_seq: torch.Tensor) -> torch.Tensor:
        if self.input_cell_idx.numel() == 0:
            return msg
        out = msg.clone()
        projected = self.input_proj(hidden_seq).unsqueeze(2)
        out[:, :, self.input_cell_idx, :] = out[:, :, self.input_cell_idx, :] + projected
        return out

    def _inject_boundary_inputs(self, msg: torch.Tensor, boundary_seq: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError("boundary_input now represents direct boundary cell states")

    def _run_family_updates(
        self,
        family_input: torch.Tensor,
        state: TensorDict,
        *,
        resets: torch.Tensor | None,
        batch_size: int,
        time_steps: int,
        family_materialized: dict[str, object | None],
    ) -> tuple[torch.Tensor, TensorDict]:
        y_next = torch.zeros_like(family_input)
        next_state = TensorDict({}, batch_size=[])
        active_families = [name for name in self._family_names if self._family_num_cells(name) > 0]
        if self.config.use_family_cuda_streams and family_input.is_cuda and len(active_families) > 1:
            self._ensure_family_streams(device=family_input.device, families=active_families)
            current = torch.cuda.current_stream(family_input.device)
            outputs: dict[str, tuple[torch.Tensor, TensorDict]] = {}
            for name in active_families:
                stream = self._family_streams[name]
                stream.wait_stream(current)
                with torch.cuda.stream(stream):
                    outputs[name] = self._run_family(
                        name,
                        family_input,
                        state.get(name),
                        resets,
                        batch_size,
                        time_steps,
                        family_materialized,
                    )
            for name in active_families:
                current.wait_stream(self._family_streams[name])
                family_y, family_state = outputs[name]
                idx = self._family_indices(name)
                y_next[:, :, idx, :] = family_y.to(dtype=y_next.dtype)
                next_state[name] = family_state
        else:
            for name in active_families:
                family_y, family_state = self._run_family(
                    name,
                    family_input,
                    state.get(name),
                    resets,
                    batch_size,
                    time_steps,
                    family_materialized,
                )
                idx = self._family_indices(name)
                y_next[:, :, idx, :] = family_y.to(dtype=y_next.dtype)
                next_state[name] = family_state
        return y_next, next_state

    def _run_family_updates_recurrent_step(
        self,
        recurrent_input: torch.Tensor,
        state: TensorDict,
        *,
        resets: torch.Tensor | None,
        batch_size: int,
        family_materialized: dict[str, object | None],
        step_family_state_cache: dict[str, object] | None = None,
    ) -> tuple[torch.Tensor, TensorDict]:
        num_recurrent = int(self.recurrent_cell_idx.numel())
        if num_recurrent == 0:
            return recurrent_input.new_empty(batch_size, 0, self.hidden_size), TensorDict({}, batch_size=[])
        if self._full_recurrent_family_name is not None:
            family_name = self._full_recurrent_family_name
            family_y, family_state = self._run_recurrent_family_step(
                family_name,
                recurrent_input,
                state.get(family_name),
                resets=resets,
                family_materialized=family_materialized,
                step_family_state_cache=step_family_state_cache,
            )
            next_state = TensorDict({}, batch_size=[])
            next_state[family_name] = family_state
            return family_y.to(dtype=recurrent_input.dtype), next_state

        recurrent_next = recurrent_input.new_empty(batch_size, num_recurrent, self.hidden_size)
        next_state = TensorDict({}, batch_size=[])
        active_families = [name for name in self._family_names if self._family_recurrent_indices(name).numel() > 0]
        if self.config.use_family_cuda_streams and recurrent_input.is_cuda and len(active_families) > 1:
            self._ensure_family_streams(device=recurrent_input.device, families=active_families)
            current = torch.cuda.current_stream(recurrent_input.device)
            outputs: dict[str, tuple[torch.Tensor, TensorDict]] = {}
            for name in active_families:
                stream = self._family_streams[name]
                stream.wait_stream(current)
                with torch.cuda.stream(stream):
                    outputs[name] = self._run_recurrent_family_step(
                        name,
                        recurrent_input,
                        state.get(name),
                        resets=resets,
                        family_materialized=family_materialized,
                        step_family_state_cache=step_family_state_cache,
                    )
            for name in active_families:
                current.wait_stream(self._family_streams[name])
                family_y, family_state = outputs[name]
                recurrent_idx = self._family_recurrent_indices(name)
                recurrent_next[:, recurrent_idx, :] = family_y.to(dtype=recurrent_next.dtype)
                next_state[name] = family_state
            return recurrent_next, next_state

        for name in active_families:
            recurrent_idx = self._family_recurrent_indices(name)
            family_y, family_state = self._run_recurrent_family_step(
                name,
                recurrent_input,
                state.get(name),
                resets=resets,
                family_materialized=family_materialized,
                step_family_state_cache=step_family_state_cache,
            )
            recurrent_next[:, recurrent_idx, :] = family_y.to(dtype=recurrent_next.dtype)
            next_state[name] = family_state
        return recurrent_next, next_state

    def _run_recurrent_family_step(
        self,
        family_name: str,
        recurrent_input: torch.Tensor,
        family_state: TensorDict | None,
        *,
        resets: torch.Tensor | None,
        family_materialized: dict[str, object | None],
        step_family_state_cache: dict[str, object] | None = None,
    ) -> tuple[torch.Tensor, TensorDict]:
        recurrent_idx = self._family_recurrent_indices(family_name)
        family_x = recurrent_input[:, recurrent_idx, :]
        family_module = self.family_modules[family_name]
        if step_family_state_cache is not None and family_name in step_family_state_cache:
            forward_step_packed = getattr(family_module, "forward_step_packed", None)
            if not callable(forward_step_packed):
                raise RuntimeError(f"Family {family_name} is missing forward_step_packed for packed stream cache")
            if family_state is None:
                raise RuntimeError(f"Packed stream family cache requires preinitialized state for {family_name}")
            family_y, next_packed_state = forward_step_packed(
                family_x,
                step_family_state_cache[family_name],
                resets=resets,
                materialized=family_materialized.get(family_name),
            )
            step_family_state_cache[family_name] = next_packed_state
            return family_y, family_state
        family_forward_step = getattr(family_module, "forward_step", None)
        if callable(family_forward_step):
            return family_forward_step(
                family_x,
                family_state,
                resets=resets,
                materialized=family_materialized.get(family_name),
            )
        family_y, next_state = family_module(
            family_x.unsqueeze(1),
            family_state,
            resets=resets,
            materialized=family_materialized.get(family_name),
        )
        return family_y.squeeze(1), next_state

    def _run_family_updates_step_cached(
        self,
        family_input: torch.Tensor,
        *,
        resets: torch.Tensor | None,
        family_materialized: dict[str, object | None],
        step_family_state_cache: dict[str, object],
    ) -> torch.Tensor:
        family_name = self._full_recurrent_family_name
        if family_name is None:
            raise RuntimeError("Packed stream family cache requires a full recurrent family")
        family_module = self.family_modules[family_name]
        forward_step_packed = getattr(family_module, "forward_step_packed", None)
        if not callable(forward_step_packed):
            raise RuntimeError(f"Family {family_name} is missing forward_step_packed for packed stream cache")
        family_idx = self._family_indices(family_name)
        family_y, next_packed_state = forward_step_packed(
            family_input[:, 0, family_idx, :],
            step_family_state_cache[family_name],
            resets=resets,
            materialized=family_materialized.get(family_name),
        )
        step_family_state_cache[family_name] = next_packed_state
        return family_y

    def _run_family(
        self,
        family_name: str,
        family_input: torch.Tensor,
        family_state: TensorDict | None,
        resets: torch.Tensor | None,
        batch_size: int,
        time_steps: int,
        family_materialized: dict[str, object | None],
    ) -> tuple[torch.Tensor, TensorDict]:
        idx = self._family_indices(family_name)
        family_x = family_input[:, :, idx, :]
        family_module = self.family_modules[family_name]
        family_resets = None
        if resets is not None:
            family_resets = resets
        y_family, next_state = family_module(
            family_x,
            family_state,
            resets=family_resets,
            materialized=family_materialized.get(family_name),
        )
        return y_family, next_state

    def _blend_family_states(self, prev: TensorDict, next_state: TensorDict, active_rows: torch.Tensor) -> TensorDict:
        if bool(active_rows.all()):
            return next_state
        if not bool(active_rows.any()):
            return prev
        out = TensorDict({}, batch_size=[])
        for family_name in self._family_names:
            prev_state = prev.get(family_name)
            family_next = next_state.get(family_name)
            if prev_state is None:
                if family_next is not None:
                    out[family_name] = family_next
                continue
            if family_next is None:
                out[family_name] = prev_state
                continue
            family_mask = active_rows.view(1, -1)
            out[family_name] = _where_tensordict(family_mask, family_next, prev_state)
        return out

    def _readout(self, y_final: torch.Tensor) -> torch.Tensor:
        pooled = self._pool_output_cells(y_final).reshape(y_final.shape[0], y_final.shape[1], -1)
        return self.readout_out(pooled)

    def _pool_output_cells(self, y_final: torch.Tensor) -> torch.Tensor:
        if self._partitioned_layout:
            port_y = y_final[:, :, self._output_slice, :]
        else:
            port_y = y_final[:, :, self.output_cell_idx, :]
        if self.config.readout_pool == "mean":
            return port_y.mean(dim=2, keepdim=True)
        if self.config.readout_pool == "flatten":
            return port_y
        scores = torch.einsum("btph,qh->btpq", port_y, self.readout_query)
        weights = torch.softmax(scores.to(dtype=torch.float32), dim=2).to(dtype=port_y.dtype)
        return (weights.unsqueeze(-1) * port_y.unsqueeze(3)).sum(dim=2)

    def _family_num_cells(self, family_name: str) -> int:
        return int(self._family_indices(family_name).numel())

    def _family_indices(self, family_name: str) -> torch.Tensor:
        return getattr(self, _family_buffer_name(family_name))

    def _family_recurrent_indices(self, family_name: str) -> torch.Tensor:
        return getattr(self, _family_recurrent_buffer_name(family_name))

    def _build_family_indices(self, family_name: str) -> torch.Tensor:
        family_idx = self._family_name_to_idx[family_name]
        return torch.nonzero(self.cell_layout == family_idx, as_tuple=False).reshape(-1)

    def _ensure_family_streams(self, *, device: torch.device, families: list[str]) -> None:
        if not torch.cuda.is_available():
            return
        if self._family_streams is not None and set(self._family_streams.keys()) == set(families):
            return
        self._family_streams = {name: torch.cuda.Stream(device=device) for name in families}

    def _project_output_cells(self, output_msg: torch.Tensor) -> torch.Tensor:
        return torch.einsum("btpd,pdh->btph", output_msg, self.output_cell_weight) + self.output_cell_bias.view(
            1, 1, -1, self.hidden_size
        )

    def _project_output_cells_step(self, output_msg: torch.Tensor) -> torch.Tensor:
        return torch.einsum("bpd,pdh->bph", output_msg, self.output_cell_weight) + self.output_cell_bias.view(
            1,
            -1,
            self.hidden_size,
        )

    def _project_output_cells_step_raw(
        self,
        output_msg: torch.Tensor,
        *,
        value_to_output_weight: torch.Tensor,
    ) -> torch.Tensor:
        projected = torch.bmm(output_msg.transpose(0, 1), value_to_output_weight).transpose(0, 1)
        return projected + self.output_cell_bias.view(
            1,
            -1,
            self.hidden_size,
        )

    def _prepare_stream_step_family_cache(
        self,
        state: TensorDict,
        *,
        batch: int,
        device: torch.device,
        dtype: torch.dtype,
    ) -> dict[str, object] | None:
        cache: dict[str, object] = {}
        for family_name in self._family_names:
            if self._family_recurrent_indices(family_name).numel() == 0:
                continue
            family_module = self.family_modules[family_name]
            pack_step_state = getattr(family_module, "pack_step_state", None)
            unpack_step_state = getattr(family_module, "unpack_step_state", None)
            reset_packed_step_state = getattr(family_module, "reset_packed_step_state", None)
            forward_step_packed = getattr(family_module, "forward_step_packed", None)
            if not (
                callable(pack_step_state)
                and callable(unpack_step_state)
                and callable(reset_packed_step_state)
                and callable(forward_step_packed)
            ):
                continue
            cache[family_name] = pack_step_state(state.get(family_name), batch=batch, device=device, dtype=dtype)
        return cache or None

    def _reset_stream_step_family_cache(
        self,
        step_family_state_cache: dict[str, object],
        resets: torch.Tensor,
    ) -> None:
        reset_mask = torch.as_tensor(resets, device=self.coords.device, dtype=torch.bool).view(-1)
        for family_name, cached_state in list(step_family_state_cache.items()):
            family_module = self.family_modules[family_name]
            reset_packed_step_state = getattr(family_module, "reset_packed_step_state", None)
            if not callable(reset_packed_step_state):
                continue
            step_family_state_cache[family_name] = reset_packed_step_state(cached_state, reset_mask)

    def _apply_stream_step_family_cache(
        self,
        state: TensorDict,
        step_family_state_cache: dict[str, object],
    ) -> None:
        for family_name, cached_state in step_family_state_cache.items():
            family_module = self.family_modules[family_name]
            unpack_step_state = getattr(family_module, "unpack_step_state", None)
            if not callable(unpack_step_state):
                continue
            state[family_name] = unpack_step_state(cached_state)


class Fabric(nn.Module):
    def __init__(self, spec: FabricSpec, d_hidden: int) -> None:
        super().__init__()
        self.spec = spec
        self.d_hidden = int(d_hidden)
        self.fabric = FabricRuntime(spec)
        self.num_input_cells = int(spec.input_cell_idx.numel())
        self.num_readout_slots = self.fabric.readout_slots
        self.in_proj = nn.Linear(self.d_hidden, self.num_input_cells * self.fabric.hidden_size)
        self.out_proj = nn.Linear(self.num_readout_slots * self.fabric.hidden_size, self.d_hidden)

    def init_state(self, batch: int, *, device: torch.device | str = "cpu", dtype: torch.dtype) -> TensorDict:
        return self.fabric.init_state(batch=batch, device=device, dtype=dtype)

    def reset_state(self, state: MaybeState, mask: ResetMask) -> MaybeState:
        return self.fabric.reset_state(state, mask)

    def forward(
        self,
        hidden_input: Tensor,
        state: MaybeState = None,
        *,
        resets: Optional[ResetMask] = None,
        k: int | torch.Tensor | None = None,
        mode: ExecutionMode | None = None,
    ) -> tuple[Tensor, MaybeState]:
        step_mode = hidden_input.dim() == 2
        hidden_seq = hidden_input.unsqueeze(1) if step_mode else hidden_input
        if hidden_seq.dim() != 3:
            raise ValueError(f"Fabric expects hidden_input shaped [B,H] or [B,T,H], got {tuple(hidden_input.shape)}")
        boundary_input = self.in_proj(hidden_seq).view(
            hidden_seq.shape[0], hidden_seq.shape[1], self.num_input_cells, self.fabric.hidden_size
        )
        y_cells, next_state = self.fabric.forward_cells(
            state=state,
            resets=resets,
            k=k,
            mode=mode,
            boundary_input=boundary_input.squeeze(1) if step_mode else boundary_input,
        )
        if step_mode:
            pooled = self.fabric._pool_output_cells(y_cells.unsqueeze(1)).squeeze(1).reshape(hidden_seq.shape[0], -1)
            return self.out_proj(pooled), next_state
        pooled = self.fabric._pool_output_cells(y_cells).reshape(hidden_seq.shape[0], hidden_seq.shape[1], -1)
        return self.out_proj(pooled), next_state


def build_fabric(spec: FabricSpec, *, d_hidden: int | None = None) -> nn.Module:
    if d_hidden is None:
        return FabricRuntime(spec)
    return Fabric(spec, d_hidden=d_hidden)


def _expand_resets_for_time(
    resets: ResetMask | None,
    *,
    batch_size: int,
    time_steps: int,
    device: torch.device,
) -> torch.Tensor | None:
    if resets is None:
        return None
    mask = torch.as_tensor(resets, device=device, dtype=torch.bool)
    if mask.dim() == 1:
        return mask.view(batch_size, 1).expand(batch_size, time_steps)
    if mask.dim() == 2 and mask.shape == (batch_size, time_steps):
        return mask
    raise ValueError(f"resets must have shape [B] or [B,T], got {tuple(mask.shape)}")


def _flatten_step_idx(
    step_idx: int | torch.Tensor,
    *,
    batch_size: int,
    time_steps: int,
    device: torch.device,
    dtype: torch.dtype,
) -> torch.Tensor:
    if isinstance(step_idx, int):
        return torch.full((batch_size * time_steps,), step_idx, device=device, dtype=dtype)
    step_tensor = torch.as_tensor(step_idx, device=device, dtype=dtype)
    if step_tensor.dim() == 1 and step_tensor.shape[0] == batch_size:
        return step_tensor.view(batch_size, 1).expand(batch_size, time_steps).reshape(batch_size * time_steps)
    if step_tensor.dim() == 2 and step_tensor.shape == (batch_size, time_steps):
        return step_tensor.reshape(batch_size * time_steps)
    raise ValueError(f"step_idx tensor must have shape [B] or [B,T], got {tuple(step_tensor.shape)}")


def _where_tensordict(mask: torch.Tensor, new_state: TensorDictBase, old_state: TensorDictBase) -> TensorDict:
    out = TensorDict({}, batch_size=new_state.batch_size)
    keys = set(new_state.keys()) | set(old_state.keys())
    for key in keys:
        new_value = new_state.get(key)
        old_value = old_state.get(key)
        if isinstance(new_value, TensorDictBase) and isinstance(old_value, TensorDictBase):
            out[key] = _where_tensordict(mask, new_value, old_value)
            continue
        if torch.is_tensor(new_value) and torch.is_tensor(old_value):
            shape = tuple(mask.shape) + (1,) * (new_value.dim() - mask.dim())
            out[key] = torch.where(mask.view(shape), new_value, old_value)
            continue
        out[key] = new_value if new_value is not None else old_value
    return out


def _family_buffer_name(family_name: str) -> str:
    return f"_family_idx__{family_name}"


def _family_recurrent_buffer_name(family_name: str) -> str:
    return f"_family_recurrent_idx__{family_name}"


def _select_receiver_tables(
    neighbor_idx: torch.Tensor,
    neighbor_valid: torch.Tensor,
    edge_distance: torch.Tensor,
    edge_delay: torch.Tensor,
    receiver_idx: torch.Tensor,
    sender_lookup: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    recv_neighbor_idx = neighbor_idx.index_select(0, receiver_idx)
    recv_neighbor_valid = neighbor_valid.index_select(0, receiver_idx)
    recv_edge_distance = edge_distance.index_select(0, receiver_idx)
    recv_edge_delay = edge_delay.index_select(0, receiver_idx)
    compact_idx = sender_lookup.index_select(0, recv_neighbor_idx.reshape(-1)).view_as(recv_neighbor_idx)
    if bool((compact_idx[recv_neighbor_valid] < 0).any()):
        raise ValueError("Receiver subset contains a sender outside the compact sender set")
    compact_idx = torch.where(recv_neighbor_valid, compact_idx, torch.zeros_like(compact_idx))
    return compact_idx, recv_neighbor_valid, recv_edge_distance, recv_edge_delay


__all__ = ["Fabric", "FabricRuntime", "build_fabric"]
