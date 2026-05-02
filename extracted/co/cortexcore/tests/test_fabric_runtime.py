from __future__ import annotations

import math

import cortex.fabric.families as fabric_families
import cortex.kernels.dispatch as kernel_dispatch
import pytest
import torch
from cortex.fabric import FabricConfig, FabricFamilyConfig, FabricRuntime, build_fabric, init_fabric
from cortex.fabric.families import build_family_module
from tensordict import TensorDictBase


def _make_spec():
    return init_fabric(
        FabricConfig(
            width=4,
            height=4,
            hidden_size=8,
            families={
                "slstm": FabricFamilyConfig(family_type="slstm"),
                "axoncell": FabricFamilyConfig(family_type="axoncell"),
            },
            cell_mix={"slstm": 0.5, "axoncell": 0.5},
            patch_edges_per_cell=0,
            projection_region_shape=(2, 2),
            k_max=4,
            default_k=2,
            seed=11,
        )
    )


def test_fabric_runtime_forward_shape_and_state():
    runtime = build_fabric(_make_spec())
    assert isinstance(runtime, FabricRuntime)
    x = torch.randn(2, 5, 8)

    y, state = runtime(x, state=None, k=2)

    assert y.shape == x.shape
    assert state is not None
    assert "cells" in state.keys()
    assert state["cells"].shape == (2, runtime.coords.shape[0], runtime.hidden_size)
    assert "slstm" in state.keys()
    assert "axoncell" in state.keys()


def test_fabric_runtime_accepts_rowwise_k_tensor():
    stack = build_fabric(_make_spec())
    x = torch.randn(2, 4, 8)
    k = torch.tensor([1, 3], dtype=torch.long)

    y, _ = stack(x, state=None, k=k)

    assert y.shape == x.shape


def test_fabric_runtime_accepts_row_constant_bt_k_tensor():
    stack = build_fabric(_make_spec())
    x = torch.randn(2, 3, 8)
    k = torch.tensor([[1, 1, 1], [2, 2, 2]], dtype=torch.long)

    y, _ = stack(x, state=None, k=k)

    assert y.shape == x.shape


def test_fabric_stream_sequence_matches_repeated_steps_for_cells_and_state():
    runtime = build_fabric(_make_spec())
    assert isinstance(runtime, FabricRuntime)
    batch_size = 2
    time_steps = 4
    boundary_seq = torch.randn(batch_size, time_steps, runtime.input_cell_idx.numel(), runtime.hidden_size)

    y_seq, state_seq = runtime.forward_cells(boundary_input=boundary_seq, state=None, k=1, mode="stream")

    state_step = None
    step_outputs = []
    for step_idx in range(time_steps):
        y_step, state_step = runtime.forward_cells(
            boundary_input=boundary_seq[:, step_idx],
            state=state_step,
            k=1,
            mode="stream",
        )
        step_outputs.append(y_step)
    y_stream = torch.stack(step_outputs, dim=1)

    torch.testing.assert_close(y_seq, y_stream, rtol=0.0, atol=0.0)
    _assert_fabric_state_close(state_seq, state_step, rtol=0.0, atol=0.0)
    torch.testing.assert_close(state_seq["cells"], y_seq[:, -1], rtol=0.0, atol=0.0)


def test_fabric_stream_sequence_matches_repeated_steps_for_k_gt_one_and_resets():
    runtime = build_fabric(_make_spec())
    assert isinstance(runtime, FabricRuntime)
    batch_size = 2
    time_steps = 5
    boundary_seq = torch.randn(batch_size, time_steps, runtime.input_cell_idx.numel(), runtime.hidden_size)
    resets = torch.tensor(
        [
            [False, False, True, False, False],
            [False, True, False, False, True],
        ],
        dtype=torch.bool,
    )

    y_seq, state_seq = runtime.forward_cells(
        boundary_input=boundary_seq,
        state=None,
        resets=resets,
        k=2,
        mode="stream",
    )

    state_step = None
    step_outputs = []
    for step_idx in range(time_steps):
        y_step, state_step = runtime.forward_cells(
            boundary_input=boundary_seq[:, step_idx],
            state=state_step,
            resets=resets[:, step_idx],
            k=2,
            mode="stream",
        )
        step_outputs.append(y_step)
    y_stream = torch.stack(step_outputs, dim=1)

    torch.testing.assert_close(y_seq, y_stream, rtol=0.0, atol=0.0)
    _assert_fabric_state_close(state_seq, state_step, rtol=0.0, atol=0.0)
    torch.testing.assert_close(state_seq["cells"], y_seq[:, -1], rtol=0.0, atol=0.0)


def test_fabric_stream_chunking_matches_full_sequence_and_stores_cells():
    runtime = build_fabric(_make_spec())
    assert isinstance(runtime, FabricRuntime)
    boundary_seq = torch.randn(2, 6, runtime.input_cell_idx.numel(), runtime.hidden_size)

    y_full, state_full = runtime.forward_cells(boundary_input=boundary_seq, state=None, k=2, mode="stream")

    state_chunk = None
    chunks = []
    for start in (0, 2, 4):
        end = min(start + 2, boundary_seq.shape[1])
        y_chunk, state_chunk = runtime.forward_cells(
            boundary_input=boundary_seq[:, start:end],
            state=state_chunk,
            k=2,
            mode="stream",
        )
        chunks.append(y_chunk)
    y_chunked = torch.cat(chunks, dim=1)

    torch.testing.assert_close(y_full, y_chunked, rtol=0.0, atol=0.0)
    _assert_fabric_state_close(state_full, state_chunk, rtol=0.0, atol=0.0)
    torch.testing.assert_close(state_full["cells"], y_full[:, -1], rtol=0.0, atol=0.0)


def test_fabric_diffusion_stores_last_cell_snapshot():
    runtime = build_fabric(_make_spec())
    assert isinstance(runtime, FabricRuntime)
    boundary_seq = torch.randn(2, 4, runtime.input_cell_idx.numel(), runtime.hidden_size)

    y_diff, state_diff = runtime.forward_cells(boundary_input=boundary_seq, state=None, k=2, mode="diffusion")

    torch.testing.assert_close(state_diff["cells"], y_diff[:, -1], rtol=0.0, atol=0.0)


def test_fabric_defaults_to_single_attention_head():
    spec = init_fabric(FabricConfig(width=4, height=4, hidden_size=8))

    assert spec.config.num_heads == 1


def test_fabric_slstm_defaults_to_single_head():
    family = build_family_module(
        FabricFamilyConfig(family_type="slstm"),
        hidden_size=16,
        num_cells=2,
        init_noise_std=0.0,
    )

    assert family.num_heads == 1
    assert family.head_dim == 16


def test_fabric_slstm_respects_num_heads_override():
    family = build_family_module(
        FabricFamilyConfig(family_type="slstm", num_heads=4),
        hidden_size=16,
        num_cells=2,
        init_noise_std=0.0,
    )

    assert family.num_heads == 4
    assert family.head_dim == 4


def test_fabric_axon_forward_step_matches_sequence_wrapper():
    family = build_family_module(
        FabricFamilyConfig(family_type="axoncell"),
        hidden_size=8,
        num_cells=4,
        init_noise_std=0.0,
    )
    x_step = torch.randn(6, 4, 8, requires_grad=True)
    x_seq = x_step.detach().clone().requires_grad_(True)
    state = family.init_state(6, device="cpu", dtype=torch.float32)
    resets = torch.tensor([True, False, False, True, False, True], dtype=torch.bool)

    y_step, state_step = family.forward_step(x_step, state.clone(), resets=resets)
    step_loss = y_step.square().sum()
    step_grads = torch.autograd.grad(step_loss, (x_step, *family.parameters()))

    y_seq, state_seq = family(x_seq.unsqueeze(1), state.clone(), resets=resets)
    seq_loss = y_seq.square().sum()
    seq_grads = torch.autograd.grad(seq_loss, (x_seq, *family.parameters()))

    torch.testing.assert_close(y_step, y_seq.squeeze(1), rtol=1e-6, atol=1e-6)
    _assert_family_state_close(state_step, state_seq, rtol=1e-6, atol=1e-6)
    torch.testing.assert_close(step_grads[0], seq_grads[0].squeeze(1), rtol=1e-6, atol=1e-6)
    for step_grad, seq_grad in zip(step_grads[1:], seq_grads[1:], strict=True):
        torch.testing.assert_close(step_grad, seq_grad, rtol=1e-6, atol=1e-6)


def test_fabric_slstm_forward_step_packed_matches_sequence_wrapper():
    family = build_family_module(
        FabricFamilyConfig(family_type="slstm"),
        hidden_size=8,
        num_cells=4,
        init_noise_std=0.0,
    )
    x_step = torch.randn(6, 4, 8, requires_grad=True)
    x_seq = x_step.detach().clone().requires_grad_(True)
    state = family.init_state(6, device="cpu", dtype=torch.float32)
    resets = torch.tensor([True, False, False, True, False, True], dtype=torch.bool)

    packed_state = family.pack_step_state(state.clone(), batch=6, device="cpu", dtype=torch.float32)
    y_step, next_packed_state = family.forward_step_packed(x_step, packed_state, resets=resets)
    state_step = family.unpack_step_state(next_packed_state)
    step_loss = y_step.square().sum()
    step_grads = torch.autograd.grad(step_loss, (x_step, *family.parameters()))

    y_seq, state_seq = family(x_seq.unsqueeze(1), state.clone(), resets=resets)
    seq_loss = y_seq.square().sum()
    seq_grads = torch.autograd.grad(seq_loss, (x_seq, *family.parameters()))

    torch.testing.assert_close(y_step, y_seq.squeeze(1), rtol=1e-6, atol=1e-6)
    _assert_family_state_close(state_step, state_seq, rtol=1e-6, atol=1e-6)
    torch.testing.assert_close(step_grads[0], seq_grads[0].squeeze(1), rtol=1e-6, atol=1e-6)
    for step_grad, seq_grad in zip(step_grads[1:], seq_grads[1:], strict=True):
        torch.testing.assert_close(step_grad, seq_grad, rtol=1e-6, atol=1e-6)


def test_fabric_axon_forward_step_packed_matches_sequence_wrapper():
    family = build_family_module(
        FabricFamilyConfig(family_type="axoncell"),
        hidden_size=8,
        num_cells=4,
        init_noise_std=0.0,
    )
    x_step = torch.randn(6, 4, 8, requires_grad=True)
    x_seq = x_step.detach().clone().requires_grad_(True)
    state = family.init_state(6, device="cpu", dtype=torch.float32)
    resets = torch.tensor([True, False, False, True, False, True], dtype=torch.bool)

    packed_state = family.pack_step_state(state.clone(), batch=6, device="cpu", dtype=torch.float32)
    y_step, next_packed_state = family.forward_step_packed(x_step, packed_state, resets=resets)
    state_step = family.unpack_step_state(next_packed_state)
    step_loss = y_step.square().sum()
    step_grads = torch.autograd.grad(step_loss, (x_step, *family.parameters()))

    y_seq, state_seq = family(x_seq.unsqueeze(1), state.clone(), resets=resets)
    seq_loss = y_seq.square().sum()
    seq_grads = torch.autograd.grad(seq_loss, (x_seq, *family.parameters()))

    torch.testing.assert_close(y_step, y_seq.squeeze(1), rtol=1e-6, atol=1e-6)
    _assert_family_state_close(state_step, state_seq, rtol=1e-6, atol=1e-6)
    torch.testing.assert_close(step_grads[0], seq_grads[0].squeeze(1), rtol=1e-6, atol=1e-6)
    for step_grad, seq_grad in zip(step_grads[1:], seq_grads[1:], strict=True):
        torch.testing.assert_close(step_grad, seq_grad, rtol=1e-6, atol=1e-6)


def test_fabric_cpu_backend_selection_uses_pytorch_kernels(monkeypatch: pytest.MonkeyPatch) -> None:
    selected: list[tuple[str, str, str, bool]] = []

    dispatch_select_backend = kernel_dispatch.select_backend
    families_select_backend = fabric_families.select_backend

    def record_dispatch_backend(*args, **kwargs):
        backend = dispatch_select_backend(*args, **kwargs)
        selected.append(("dispatch", backend.__name__, kwargs["tensor"].device.type, kwargs["tensor"].is_cuda))
        return backend

    def record_family_backend(*args, **kwargs):
        backend = families_select_backend(*args, **kwargs)
        selected.append(("families", backend.__name__, kwargs["tensor"].device.type, kwargs["tensor"].is_cuda))
        return backend

    monkeypatch.setattr(kernel_dispatch, "select_backend", record_dispatch_backend)
    monkeypatch.setattr(fabric_families, "select_backend", record_family_backend)

    slstm = build_family_module(
        FabricFamilyConfig(family_type="slstm"),
        hidden_size=8,
        num_cells=4,
        init_noise_std=0.0,
    )
    slstm_state = slstm.init_state(2, device="cpu", dtype=torch.float32)
    slstm(torch.randn(2, 1, 4, 8), slstm_state)

    axon = build_family_module(
        FabricFamilyConfig(family_type="axoncell"),
        hidden_size=8,
        num_cells=4,
        init_noise_std=0.0,
    )
    axon_state = axon.init_state(2, device="cpu", dtype=torch.float32)
    axon(torch.randn(2, 1, 4, 8), axon_state)

    runtime = build_fabric(_make_spec())
    boundary_seq = torch.randn(2, 3, runtime.input_cell_idx.numel(), runtime.hidden_size)
    runtime.forward_cells(boundary_input=boundary_seq, state=None, k=2, mode="stream")

    assert ("dispatch", "slstm_sequence_pytorch", "cpu", False) in selected
    assert ("families", "rtu_stream_diag_pytorch", "cpu", False) in selected
    assert ("dispatch", "rtu_stream_diag_pytorch", "cpu", False) in selected


@pytest.mark.parametrize("family_type", ["slstm", "axoncell"])
@pytest.mark.parametrize("k", [1, 2])
def test_fabric_stream_sequence_single_family_matches_repeated_steps_for_cells_and_state(family_type, k):
    runtime = build_fabric(
        init_fabric(
            FabricConfig(
                width=4,
                height=4,
                hidden_size=8,
                families={family_type: FabricFamilyConfig(family_type=family_type)},
                cell_mix={family_type: 1.0},
                patch_edges_per_cell=0,
                projection_region_shape=(2, 2),
                k_max=2,
                default_k=k,
                seed=19,
            )
        )
    )
    batch_size = 2
    time_steps = 5
    boundary_seq = torch.randn(batch_size, time_steps, runtime.input_cell_idx.numel(), runtime.hidden_size)
    resets = torch.tensor(
        [
            [False, False, True, False, False],
            [False, True, False, False, True],
        ],
        dtype=torch.bool,
    )

    y_seq, state_seq = runtime.forward_cells(
        boundary_input=boundary_seq,
        state=None,
        resets=resets,
        k=k,
        mode="stream",
    )

    state_step = None
    step_outputs = []
    for step_idx in range(time_steps):
        y_step, state_step = runtime.forward_cells(
            boundary_input=boundary_seq[:, step_idx],
            state=state_step,
            resets=resets[:, step_idx],
            k=k,
            mode="stream",
        )
        step_outputs.append(y_step)
    y_stream = torch.stack(step_outputs, dim=1)

    torch.testing.assert_close(y_seq, y_stream, rtol=0.0, atol=0.0)
    _assert_fabric_state_close(state_seq, state_step, rtol=0.0, atol=0.0)


def test_fabric_message_fast_path_matches_sparse_reference_2d():
    runtime = build_fabric(
        init_fabric(
            FabricConfig(
                width=5,
                height=4,
                hidden_size=8,
                families={"slstm": FabricFamilyConfig(family_type="slstm")},
                cell_mix={"slstm": 1.0},
                local_radius=2.5,
                projection_region_shape=(2, 2),
                input_band_width=1,
                output_band_width=1,
                wrap=True,
                conduction_speed=1.0,
                max_delay=4,
                seed=17,
            )
        )
    )
    assert isinstance(runtime, FabricRuntime)
    z_prev = torch.randn(2, 3, runtime.coords.shape[0], runtime.config.d_public)
    q = runtime.q_proj(runtime.slot_embed).view(runtime.coords.shape[0], runtime.head_dim)
    gathered_kv_weight = torch.cat(
        (
            runtime.k_weight.index_select(0, runtime.kv_group_id),
            runtime.v_weight.index_select(0, runtime.kv_group_id),
        ),
        dim=-1,
    )
    step_idx = torch.tensor([1, 3], dtype=torch.long)

    fast = runtime._compute_messages(
        z_prev,
        q=q,
        gathered_kv_weight=gathered_kv_weight,
        step_idx=step_idx,
    )
    reference = _reference_messages(
        runtime,
        z_prev,
        q=q,
        gathered_kv_weight=gathered_kv_weight,
        step_idx=step_idx,
    )

    torch.testing.assert_close(fast, reference, rtol=1e-5, atol=1e-5)


def test_fabric_message_fast_path_matches_sparse_reference_3d():
    runtime = build_fabric(
        init_fabric(
            FabricConfig(
                width=3,
                height=3,
                depth=2,
                hidden_size=4,
                families={"axoncell": FabricFamilyConfig(family_type="axoncell")},
                cell_mix={"axoncell": 1.0},
                local_radius=1.5,
                projection_region_shape=(1, 1, 1),
                input_band_width=1,
                output_band_width=1,
                wrap=False,
                seed=23,
            )
        )
    )
    assert isinstance(runtime, FabricRuntime)
    z_prev = torch.randn(2, 2, runtime.coords.shape[0], runtime.config.d_public)
    q = runtime.q_proj(runtime.slot_embed).view(runtime.coords.shape[0], runtime.head_dim)
    gathered_kv_weight = torch.cat(
        (
            runtime.k_weight.index_select(0, runtime.kv_group_id),
            runtime.v_weight.index_select(0, runtime.kv_group_id),
        ),
        dim=-1,
    )

    fast = runtime._compute_messages(
        z_prev,
        q=q,
        gathered_kv_weight=gathered_kv_weight,
        step_idx=2,
    )
    reference = _reference_messages(
        runtime,
        z_prev,
        q=q,
        gathered_kv_weight=gathered_kv_weight,
        step_idx=2,
    )

    torch.testing.assert_close(fast, reference, rtol=1e-5, atol=1e-5)


def test_fabric_stream_step_subset_messages_match_full_reference():
    runtime = build_fabric(
        init_fabric(
            FabricConfig(
                width=5,
                height=4,
                hidden_size=8,
                families={"slstm": FabricFamilyConfig(family_type="slstm")},
                cell_mix={"slstm": 1.0},
                local_radius=2.5,
                projection_region_shape=(2, 2),
                input_band_width=1,
                output_band_width=1,
                wrap=True,
                conduction_speed=1.0,
                max_delay=4,
                seed=17,
            )
        )
    )
    assert isinstance(runtime, FabricRuntime)
    z_prev_step = torch.randn(2, runtime.coords.shape[0], runtime.config.d_public)
    q = runtime.q_proj(runtime.slot_embed).view(runtime.coords.shape[0], runtime.head_dim)
    sender_kv_weight = torch.cat(
        (
            runtime.k_weight.index_select(0, runtime.kv_group_id),
            runtime.v_weight.index_select(0, runtime.kv_group_id),
        ),
        dim=-1,
    ).index_select(0, runtime.sender_cell_idx)
    k_all, v_all = runtime._project_sender_kv_step(z_prev_step, sender_kv_weight=sender_kv_weight)
    full_reference = _reference_messages_step(runtime, z_prev_step, q=q, step_idx=torch.tensor([1, 1]))

    recurrent_msg = runtime._compute_messages_step_subset(
        k_all,
        v_all,
        q_subset=q.index_select(0, runtime.recurrent_cell_idx),
        neighbor_idx=runtime.recurrent_neighbor_idx,
        neighbor_valid=runtime.recurrent_neighbor_valid,
        edge_distance=runtime.recurrent_edge_distance,
        edge_delay=runtime.recurrent_edge_delay,
        use_delay=runtime.spec.anatomy.edge_delay is not None,
        step_idx=1,
    )
    output_msg = runtime._compute_messages_step_subset(
        k_all,
        v_all,
        q_subset=q.index_select(0, runtime.output_cell_idx),
        neighbor_idx=runtime.output_neighbor_idx,
        neighbor_valid=runtime.output_neighbor_valid,
        edge_distance=runtime.output_edge_distance,
        edge_delay=runtime.output_edge_delay,
        use_delay=runtime.spec.anatomy.edge_delay is not None,
        step_idx=1,
    )

    torch.testing.assert_close(
        recurrent_msg,
        full_reference[:, runtime.recurrent_cell_idx, :],
        rtol=1e-5,
        atol=1e-5,
    )
    torch.testing.assert_close(
        output_msg,
        full_reference[:, runtime.output_cell_idx, :],
        rtol=1e-5,
        atol=1e-5,
    )


@pytest.mark.parametrize(
    ("k_rows_values", "all_active"),
    [
        ([0, 0], False),
        ([1, 1], True),
        ([0, 1], None),
    ],
)
def test_fabric_stream_step_k1_fast_path_matches_previous_reference(k_rows_values, all_active):
    runtime = build_fabric(
        init_fabric(
            FabricConfig(
                width=4,
                height=4,
                hidden_size=8,
                families={"slstm": FabricFamilyConfig(family_type="slstm")},
                cell_mix={"slstm": 1.0},
                patch_edges_per_cell=0,
                projection_region_shape=(2, 2),
                k_max=4,
                default_k=1,
                seed=7,
            )
        )
    )
    assert isinstance(runtime, FabricRuntime)
    batch_size = 2
    cells_prev = runtime.init_state(batch_size, device="cpu", dtype=torch.float32)["cells"]
    boundary_step = torch.randn(batch_size, runtime.input_cell_idx.numel(), runtime.hidden_size)
    state = runtime.init_state(batch_size, device="cpu", dtype=torch.float32)
    q = runtime.q_proj(runtime.slot_embed).view(runtime.coords.shape[0], runtime.head_dim)
    recurrent_q = q.index_select(0, runtime.recurrent_cell_idx)
    output_q = q.index_select(0, runtime.output_cell_idx)
    sender_kv_weight = torch.cat(
        (
            runtime.k_weight.index_select(0, runtime.kv_group_id),
            runtime.v_weight.index_select(0, runtime.kv_group_id),
        ),
        dim=-1,
    ).index_select(0, runtime.sender_cell_idx)
    sender_input_to_kv_weight = torch.einsum("dh,sdm->shm", runtime.public_proj.weight, sender_kv_weight)
    recurrent_sender_input_to_kv_weight = sender_input_to_kv_weight.index_select(0, runtime.recurrent_sender_idx)
    value_to_cell_weight = runtime.msg_to_cell.weight @ runtime.msg_out.weight
    value_to_output_weight = torch.einsum("dv,pdh->pvh", runtime.msg_out.weight, runtime.output_cell_weight)
    recurrent_cell_bias = (
        runtime.cell_bias_proj(runtime.slot_embed)
        .view(1, 1, runtime.coords.shape[0], runtime.hidden_size)[:, :, runtime.recurrent_cell_idx, :]
        .squeeze(1)
    )
    family_materialized = {
        name: (
            runtime.family_modules[name].materialize_params()
            if hasattr(runtime.family_modules[name], "materialize_params")
            else None
        )
        for name in runtime._family_names
    }
    k_rows = torch.tensor(k_rows_values, dtype=torch.long)

    fast_y, fast_state = runtime._forward_stream_step_k1(
        cells_prev=cells_prev,
        family_state=state,
        family_resets=None,
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
    )
    reference_y, reference_state = _reference_stream_step_k1_previous(
        runtime,
        cells_prev,
        family_state=state,
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
    )

    torch.testing.assert_close(fast_y, reference_y, rtol=0.0, atol=0.0)
    _assert_fabric_state_close(fast_state, reference_state, rtol=0.0, atol=0.0)


@pytest.mark.parametrize(
    ("families", "cell_mix"),
    [
        ({"slstm": FabricFamilyConfig(family_type="slstm")}, {"slstm": 1.0}),
        (
            {
                "slstm": FabricFamilyConfig(family_type="slstm"),
                "axoncell": FabricFamilyConfig(family_type="axoncell"),
            },
            {"slstm": 0.5, "axoncell": 0.5},
        ),
    ],
)
@pytest.mark.parametrize("k_rows_values", [[2, 2], [1, 2]])
def test_fabric_stream_step_boundary_multistep_fast_path_matches_previous_reference(
    families,
    cell_mix,
    k_rows_values,
):
    runtime = build_fabric(
        init_fabric(
            FabricConfig(
                width=4,
                height=4,
                hidden_size=8,
                families=families,
                cell_mix=cell_mix,
                patch_edges_per_cell=0,
                projection_region_shape=(2, 2),
                k_max=4,
                default_k=2,
                seed=13,
            )
        )
    )
    assert isinstance(runtime, FabricRuntime)
    batch_size = 2
    state_fast = runtime.init_state(batch_size, device="cpu", dtype=torch.float32)
    state_ref = state_fast.clone()
    cells_prev = state_fast["cells"]
    boundary_step = torch.randn(batch_size, runtime.input_cell_idx.numel(), runtime.hidden_size)
    resets = torch.tensor([False, True], dtype=torch.bool)
    family_resets = resets.view(-1, 1)
    q = runtime.q_proj(runtime.slot_embed).view(runtime.coords.shape[0], runtime.head_dim)
    recurrent_q = q.index_select(0, runtime.recurrent_cell_idx)
    output_q = q.index_select(0, runtime.output_cell_idx)
    gathered_kv_weight = torch.cat(
        (
            runtime.k_weight.index_select(0, runtime.kv_group_id),
            runtime.v_weight.index_select(0, runtime.kv_group_id),
        ),
        dim=-1,
    )
    sender_kv_weight = gathered_kv_weight.index_select(0, runtime.sender_cell_idx)
    sender_input_to_kv_weight = torch.einsum("dh,sdm->shm", runtime.public_proj.weight, sender_kv_weight)
    recurrent_sender_input_to_kv_weight = sender_input_to_kv_weight.index_select(0, runtime.recurrent_sender_idx)
    value_to_cell_weight = runtime.msg_to_cell.weight @ runtime.msg_out.weight
    value_to_output_weight = torch.einsum("dv,pdh->pvh", runtime.msg_out.weight, runtime.output_cell_weight)
    cell_bias = runtime.cell_bias_proj(runtime.slot_embed).view(1, 1, runtime.coords.shape[0], runtime.hidden_size)
    recurrent_cell_bias = cell_bias[:, :, runtime.recurrent_cell_idx, :].squeeze(1)
    family_materialized = {
        name: (
            runtime.family_modules[name].materialize_params()
            if hasattr(runtime.family_modules[name], "materialize_params")
            else None
        )
        for name in runtime._family_names
    }
    k_rows = torch.tensor(k_rows_values, dtype=torch.long)

    fast_y, fast_state = runtime._forward_stream_step_boundary_multistep(
        cells_prev=cells_prev,
        family_state=state_fast,
        family_resets=family_resets,
        k_rows=k_rows,
        max_steps=int(k_rows.max().item()),
        recurrent_q=recurrent_q,
        output_q=output_q,
        sender_input_to_kv_weight=sender_input_to_kv_weight,
        recurrent_sender_input_to_kv_weight=recurrent_sender_input_to_kv_weight,
        value_to_cell_weight=value_to_cell_weight,
        value_to_output_weight=value_to_output_weight,
        recurrent_cell_bias=recurrent_cell_bias,
        boundary_step=boundary_step,
        family_materialized=family_materialized,
    )
    reference_y, reference_state = _reference_stream_step_boundary_multistep_previous(
        runtime,
        cells_prev,
        family_state=state_ref,
        family_resets=family_resets,
        k_rows=k_rows,
        max_steps=int(k_rows.max().item()),
        q=q,
        gathered_kv_weight=gathered_kv_weight,
        cell_bias=cell_bias,
        boundary_step=boundary_step,
        family_materialized=family_materialized,
    )

    torch.testing.assert_close(fast_y, reference_y, rtol=1e-5, atol=1e-5)
    _assert_fabric_state_close(fast_state, reference_state, rtol=1e-5, atol=1e-5)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA required for fused fabric message parity test")
def test_fabric_cuda_message_kernel_matches_reference_forward_and_backward():
    runtime = build_fabric(
        init_fabric(
            FabricConfig(
                width=5,
                height=4,
                hidden_size=8,
                families={"slstm": FabricFamilyConfig(family_type="slstm")},
                cell_mix={"slstm": 1.0},
                local_radius=2.5,
                projection_region_shape=(2, 2),
                input_band_width=1,
                output_band_width=1,
                wrap=True,
                conduction_speed=1.0,
                max_delay=4,
                seed=17,
            )
        )
    ).cuda()
    assert isinstance(runtime, FabricRuntime)

    z_prev_fast = torch.randn(2, 3, runtime.coords.shape[0], runtime.config.d_public, device="cuda", requires_grad=True)
    q_fast = (
        runtime.q_proj(runtime.slot_embed).view(runtime.coords.shape[0], runtime.head_dim).detach().requires_grad_(True)
    )
    gathered_fast = (
        torch.cat(
            (
                runtime.k_weight.index_select(0, runtime.kv_group_id),
                runtime.v_weight.index_select(0, runtime.kv_group_id),
            ),
            dim=-1,
        )
        .detach()
        .requires_grad_(True)
    )
    step_idx = torch.tensor([1, 3], dtype=torch.long, device="cuda")

    fast = runtime._compute_messages(
        z_prev_fast,
        q=q_fast,
        gathered_kv_weight=gathered_fast,
        step_idx=step_idx,
    )
    fast_loss = fast.square().mean()
    fast_grads = torch.autograd.grad(fast_loss, (z_prev_fast, q_fast, gathered_fast))

    z_prev_ref = z_prev_fast.detach().clone().requires_grad_(True)
    q_ref = q_fast.detach().clone().requires_grad_(True)
    gathered_ref = gathered_fast.detach().clone().requires_grad_(True)
    reference = _reference_messages(
        runtime,
        z_prev_ref,
        q=q_ref,
        gathered_kv_weight=gathered_ref,
        step_idx=step_idx,
    )
    reference_loss = reference.square().mean()
    reference_grads = torch.autograd.grad(reference_loss, (z_prev_ref, q_ref, gathered_ref))

    torch.testing.assert_close(fast, reference, rtol=1e-5, atol=1e-5)
    for fast_grad, ref_grad in zip(fast_grads, reference_grads, strict=True):
        torch.testing.assert_close(fast_grad, ref_grad, rtol=2e-4, atol=2e-4)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA required for family stream parity test")
@pytest.mark.parametrize("k", [1, 2])
def test_fabric_cuda_family_streams_match_serial_recurrent_step(k):
    base_cfg = FabricConfig(
        width=4,
        height=4,
        hidden_size=8,
        families={
            "slstm": FabricFamilyConfig(family_type="slstm"),
            "axoncell": FabricFamilyConfig(family_type="axoncell"),
        },
        cell_mix={"slstm": 0.5, "axoncell": 0.5},
        patch_edges_per_cell=0,
        projection_region_shape=(2, 2),
        k_max=2,
        default_k=k,
        seed=11,
    )
    runtime_serial = build_fabric(init_fabric(base_cfg)).cuda()
    runtime_streams = build_fabric(init_fabric(base_cfg.model_copy(update={"use_family_cuda_streams": True}))).cuda()
    runtime_streams.load_state_dict(runtime_serial.state_dict())

    batch_size = 2
    time_steps = 4
    boundary_seq = torch.randn(
        batch_size,
        time_steps,
        runtime_serial.input_cell_idx.numel(),
        runtime_serial.hidden_size,
        device="cuda",
    )
    resets = torch.tensor(
        [
            [False, False, True, False],
            [False, True, False, False],
        ],
        dtype=torch.bool,
        device="cuda",
    )

    y_serial, state_serial = runtime_serial.forward_cells(
        boundary_input=boundary_seq,
        state=None,
        resets=resets,
        k=k,
        mode="stream",
    )
    y_streams, state_streams = runtime_streams.forward_cells(
        boundary_input=boundary_seq,
        state=None,
        resets=resets,
        k=k,
        mode="stream",
    )

    torch.testing.assert_close(y_serial, y_streams, rtol=1e-6, atol=1e-6)
    _assert_fabric_state_close(state_serial, state_streams, rtol=1e-6, atol=1e-6)


def _reference_messages(
    runtime: FabricRuntime,
    z_prev: torch.Tensor,
    *,
    q: torch.Tensor,
    gathered_kv_weight: torch.Tensor,
    step_idx: int | torch.Tensor,
) -> torch.Tensor:
    batch_size, time_steps, num_cells, _ = z_prev.shape
    kv_all = torch.einsum("btnd,ndm->btnm", z_prev, gathered_kv_weight).view(
        batch_size,
        time_steps,
        num_cells,
        runtime.head_dim + runtime.value_dim,
    )
    k_all, v_all = kv_all.split((runtime.head_dim, runtime.value_dim), dim=-1)
    k_neighbors = k_all[:, :, runtime.neighbor_idx, :]
    v_neighbors = v_all[:, :, runtime.neighbor_idx, :]
    q_neighbors = q.view(1, 1, num_cells, 1, runtime.head_dim)
    logits = (q_neighbors * k_neighbors).sum(dim=-1) / math.sqrt(float(runtime.head_dim))
    invalid_mask = ~runtime.neighbor_valid.view(1, 1, num_cells, -1)
    logits = logits.masked_fill(invalid_mask, float("-inf"))
    if float(runtime.config.distance_logit_scale) > 0.0:
        logits = logits - float(runtime.config.distance_logit_scale) * runtime.edge_distance.view(1, 1, num_cells, -1)
    if runtime.spec.anatomy.edge_delay is not None:
        if isinstance(step_idx, int):
            step_view = step_idx
        else:
            step_tensor = torch.as_tensor(step_idx, device=z_prev.device, dtype=runtime.edge_delay.dtype)
            if step_tensor.dim() == 1 and step_tensor.shape[0] == batch_size:
                step_view = step_tensor.view(batch_size, 1, 1, 1)
            elif step_tensor.dim() == 2 and step_tensor.shape == (batch_size, time_steps):
                step_view = step_tensor.view(batch_size, time_steps, 1, 1)
            else:
                raise ValueError(f"Unsupported step_idx shape {tuple(step_tensor.shape)}")
        logits = logits.masked_fill(runtime.edge_delay.view(1, 1, num_cells, -1) > step_view, float("-inf"))
    weights = torch.softmax(logits.to(dtype=torch.float32), dim=3).to(dtype=v_neighbors.dtype)
    weights = torch.where(runtime.neighbor_valid.view(1, 1, num_cells, -1), weights, torch.zeros_like(weights))
    msg_heads = (weights.unsqueeze(-1) * v_neighbors).sum(dim=3)
    return runtime.msg_out(msg_heads.reshape(batch_size, time_steps, num_cells, runtime.value_dim))


def _reference_messages_step(
    runtime: FabricRuntime,
    z_prev_step: torch.Tensor,
    *,
    q: torch.Tensor,
    step_idx: int | torch.Tensor,
) -> torch.Tensor:
    gathered_kv_weight = torch.cat(
        (
            runtime.k_weight.index_select(0, runtime.kv_group_id),
            runtime.v_weight.index_select(0, runtime.kv_group_id),
        ),
        dim=-1,
    )
    return _reference_messages(
        runtime,
        z_prev_step.unsqueeze(1),
        q=q,
        gathered_kv_weight=gathered_kv_weight,
        step_idx=step_idx,
    ).squeeze(1)


def _reference_stream_step_k1_previous(
    runtime: FabricRuntime,
    cells_prev: torch.Tensor,
    *,
    family_state: TensorDictBase,
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
) -> tuple[torch.Tensor, TensorDictBase]:
    if boundary_step is not None:
        cells_prev = cells_prev.clone()
        if runtime._partitioned_layout:
            cells_prev[:, runtime._input_slice, :] = boundary_step
        else:
            cells_prev[:, runtime.input_cell_idx, :] = boundary_step
    if runtime._partitioned_layout:
        sender_cells_prev = cells_prev[:, : runtime.sender_cell_idx.numel(), :]
        recurrent_slice = runtime._recurrent_slice
        output_slice = runtime._output_slice
        recurrent_prev = cells_prev[:, recurrent_slice, :]
    else:
        sender_cells_prev = cells_prev.index_select(1, runtime.sender_cell_idx)
        recurrent_slice = None
        output_slice = None
        recurrent_prev = cells_prev[:, runtime.recurrent_cell_idx, :]
    k_all, v_all = _reference_project_sender_kv_from_cells_step(
        sender_cells_prev,
        sender_input_to_kv_weight=sender_input_to_kv_weight,
        head_dim=runtime.head_dim,
        value_dim=runtime.value_dim,
    )
    if all_active is False:
        cells_mid = cells_prev
        blended_family_state = family_state
        final_k = k_all
        final_v = v_all
    else:
        recurrent_msg = runtime._compute_messages_step_subset_raw(
            k_all,
            v_all,
            q_subset=recurrent_q,
            neighbor_idx=runtime.recurrent_neighbor_idx,
            neighbor_valid=runtime.recurrent_neighbor_valid,
            edge_distance=runtime.recurrent_edge_distance,
            edge_delay=runtime.recurrent_edge_delay,
            use_delay=runtime.spec.anatomy.edge_delay is not None,
            step_idx=1,
        )
        recurrent_input = torch.nn.functional.linear(recurrent_msg, value_to_cell_weight) + recurrent_cell_bias
        recurrent_next, next_family_state = runtime._run_family_updates_recurrent_step(
            recurrent_input,
            family_state,  # type: ignore[arg-type]
            resets=None,
            batch_size=cells_prev.shape[0],
            family_materialized=family_materialized,
        )
        if all_active is True:
            recurrent_mid = recurrent_next
            blended_family_state = next_family_state
        else:
            active_rows = k_rows > 0
            recurrent_mid = torch.where(active_rows.view(-1, 1, 1), recurrent_next, recurrent_prev)
            blended_family_state = runtime._blend_family_states(
                family_state,  # type: ignore[arg-type]
                next_family_state,
                active_rows,
            )
        cells_mid = cells_prev.clone()
        if recurrent_slice is not None:
            cells_mid[:, recurrent_slice, :] = recurrent_mid
        else:
            cells_mid[:, runtime.recurrent_cell_idx, :] = recurrent_mid

        recurrent_k, recurrent_v = _reference_project_sender_kv_from_cells_step(
            recurrent_mid,
            sender_input_to_kv_weight=recurrent_sender_input_to_kv_weight,
            head_dim=runtime.head_dim,
            value_dim=runtime.value_dim,
        )
        if runtime._partitioned_layout:
            final_k = torch.cat((k_all[:, : runtime._num_input_cells, :], recurrent_k), dim=1)
            final_v = torch.cat((v_all[:, : runtime._num_input_cells, :], recurrent_v), dim=1)
        else:
            final_k = k_all.clone()
            final_v = v_all.clone()
            final_k[:, runtime.recurrent_sender_idx, :] = recurrent_k
            final_v[:, runtime.recurrent_sender_idx, :] = recurrent_v
    output_msg = runtime._compute_messages_step_subset_raw(
        final_k,
        final_v,
        q_subset=output_q,
        neighbor_idx=runtime.output_neighbor_idx,
        neighbor_valid=runtime.output_neighbor_valid,
        edge_distance=runtime.output_edge_distance,
        edge_delay=runtime.output_edge_delay,
        use_delay=runtime.spec.anatomy.edge_delay is not None,
        step_idx=k_rows,
    )
    output_cells = _reference_project_output_cells_step_raw(
        output_msg,
        value_to_output_weight=value_to_output_weight,
        output_cell_bias=runtime.output_cell_bias,
    ).to(dtype=cells_prev.dtype)
    cells_out = cells_mid.clone()
    if output_slice is not None:
        cells_out[:, output_slice, :] = output_cells
    else:
        cells_out[:, runtime.output_cell_idx, :] = output_cells
    next_state = runtime.init_state(cells_prev.shape[0], device=cells_prev.device, dtype=cells_prev.dtype)
    next_state["cells"] = cells_out
    for family_name in runtime._family_names:
        next_state[family_name] = blended_family_state[family_name]
    return cells_out, next_state


def _reference_stream_step_boundary_multistep_previous(
    runtime: FabricRuntime,
    cells_prev: torch.Tensor,
    *,
    family_state: TensorDictBase,
    family_resets: torch.Tensor | None,
    k_rows: torch.Tensor,
    max_steps: int,
    q: torch.Tensor,
    gathered_kv_weight: torch.Tensor,
    cell_bias: torch.Tensor,
    boundary_step: torch.Tensor,
    family_materialized: dict[str, object | None],
) -> tuple[torch.Tensor, TensorDictBase]:
    cells_prev = cells_prev.clone()
    if runtime._partitioned_layout:
        cells_prev[:, runtime._input_slice, :] = boundary_step
    else:
        cells_prev[:, runtime.input_cell_idx, :] = boundary_step

    y_prev = cells_prev.unsqueeze(1)
    running_family_state = family_state
    boundary_step_seq = boundary_step.unsqueeze(1)
    for step_idx in range(max_steps):
        z_prev = runtime.public_proj(y_prev)
        msg = runtime._compute_messages(
            z_prev,
            q=q,
            gathered_kv_weight=gathered_kv_weight,
            step_idx=step_idx + 1,
        )
        family_input = runtime.msg_to_cell(msg) + cell_bias
        y_next, next_family_state = runtime._run_family_updates(
            family_input,
            running_family_state,  # type: ignore[arg-type]
            resets=family_resets,
            batch_size=cells_prev.shape[0],
            time_steps=1,
            family_materialized=family_materialized,
        )
        if runtime._partitioned_layout:
            y_next[:, :, runtime._input_slice, :] = boundary_step_seq
        else:
            y_next[:, :, runtime.input_cell_idx, :] = boundary_step_seq
        active_rows = step_idx < k_rows
        y_prev = torch.where(active_rows.view(-1, 1, 1, 1), y_next, y_prev)
        running_family_state = runtime._blend_family_states(
            running_family_state,  # type: ignore[arg-type]
            next_family_state,
            active_rows,
        )

    final_z = runtime.public_proj(y_prev)
    final_msg = runtime._compute_messages(
        final_z,
        q=q,
        gathered_kv_weight=gathered_kv_weight,
        step_idx=k_rows,
    )
    y_out = y_prev.clone()
    y_out[:, :, runtime.output_cell_idx, :] = runtime._project_output_cells(final_msg[:, :, runtime.output_cell_idx, :])
    next_state = runtime.init_state(cells_prev.shape[0], device=cells_prev.device, dtype=cells_prev.dtype)
    next_state["cells"] = y_out.squeeze(1)
    for family_name in runtime._family_names:
        next_state[family_name] = running_family_state[family_name]
    return y_out.squeeze(1), next_state


def _reference_project_sender_kv_from_cells_step(
    sender_cells_step: torch.Tensor,
    *,
    sender_input_to_kv_weight: torch.Tensor,
    head_dim: int,
    value_dim: int,
) -> tuple[torch.Tensor, torch.Tensor]:
    kv_all = torch.einsum("bnh,nhm->bnm", sender_cells_step, sender_input_to_kv_weight)
    return kv_all.split((head_dim, value_dim), dim=-1)


def _reference_project_output_cells_step_raw(
    output_msg: torch.Tensor,
    *,
    value_to_output_weight: torch.Tensor,
    output_cell_bias: torch.Tensor,
) -> torch.Tensor:
    return torch.einsum("bpd,pdh->bph", output_msg, value_to_output_weight) + output_cell_bias.view(
        1,
        -1,
        output_cell_bias.shape[-1],
    )


def _assert_fabric_state_close(
    actual: TensorDictBase,
    expected: TensorDictBase,
    *,
    rtol: float,
    atol: float,
) -> None:
    assert actual.keys() == expected.keys()
    torch.testing.assert_close(actual["cells"], expected["cells"], rtol=rtol, atol=atol)
    for family_name in actual.keys():
        if family_name == "cells":
            continue
        actual_family = actual[family_name]
        expected_family = expected[family_name]
        assert isinstance(actual_family, TensorDictBase)
        assert isinstance(expected_family, TensorDictBase)
        assert actual_family.keys() == expected_family.keys()
        for key in actual_family.keys():
            torch.testing.assert_close(actual_family[key], expected_family[key], rtol=rtol, atol=atol)


def _assert_family_state_close(
    actual: TensorDictBase,
    expected: TensorDictBase,
    *,
    rtol: float,
    atol: float,
) -> None:
    assert actual.keys() == expected.keys()
    for key in actual.keys():
        torch.testing.assert_close(actual[key], expected[key], rtol=rtol, atol=atol)
