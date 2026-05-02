import importlib

import pytest
import torch


class _FakeCtx:
    def save_for_backward(self, *args) -> None:
        self.saved_tensors = args


def _assert_amp_metadata(ctx: _FakeCtx, *, enabled: bool) -> None:
    assert ctx._fwd_used_autocast is enabled
    assert ctx._dtype == torch.get_autocast_dtype("cuda")


def _import_or_skip(module_name: str):
    try:
        return importlib.import_module(module_name)
    except Exception as exc:
        pytest.skip(f"{module_name} unavailable: {exc}")


def _fake_slstm_forward_sequence(
    *, Wx: torch.Tensor, **_: object
) -> tuple[tuple[torch.Tensor, torch.Tensor], torch.Tensor]:
    true_batch_size = Wx.size(0)
    all_states = torch.zeros(4, 4, true_batch_size, 1, 1)
    last_state = torch.zeros(4, true_batch_size, 1, 1)
    all_gates = torch.zeros(4, true_batch_size, 1, 1, 1)
    return (all_states, last_state), all_gates


def _slstm_module():
    return _import_or_skip("cortex.kernels.triton.slstm.torch.fwbw")


def _slstm_inputs(
    resets: torch.Tensor | None = None,
    backward_recurrent_clip_val: float | None = None,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor | None, float | None]:
    return (
        torch.zeros(4, 2, 1, 1),
        torch.zeros(2, 3, 1, 1, 1),
        torch.zeros(1, 1, 1, 1),
        torch.zeros(1, 1, 1),
        resets,
        backward_recurrent_clip_val,
    )


def _run_slstm_setup_context(
    fn: torch.autograd.Function,
    inputs: tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor | None, float | None],
) -> _FakeCtx:
    ctx = _FakeCtx()
    fn.forward(ctx, *inputs)
    return ctx


def _mlstm_setup_context_case() -> tuple[torch.autograd.Function, _FakeCtx, tuple[object, ...], tuple[object, ...]]:
    mod = _import_or_skip("cortex.kernels.triton.mlstm.torch.fwbw")
    return (
        mod._mlstm_chunkwise_fwbw_generator(torch.bfloat16),
        _FakeCtx(),
        (
            torch.zeros(2, 1, 4, 8),
            torch.zeros(2, 1, 4, 8),
            torch.zeros(2, 1, 4, 8),
            torch.zeros(2, 1, 4),
            torch.zeros(2, 1, 4),
            torch.zeros(2, 1, 8, 8),
            torch.zeros(2, 1, 8),
            torch.zeros(2, 1, 1),
            1.0,
            False,
            0.0,
            128,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            True,
            None,
        ),
        (
            torch.zeros(2, 1, 4, 8),
            None,
            None,
            None,
            torch.zeros(2, 1, 8, 8),
            torch.zeros(2, 1, 8),
            torch.zeros(2, 1, 1),
            torch.zeros(2, 1, 4),
            torch.zeros(2, 1, 4),
        ),
    )


def test_slstm_forward_sets_amp_metadata(monkeypatch: pytest.MonkeyPatch) -> None:
    slstm_fwbw = _slstm_module()
    monkeypatch.setattr(slstm_fwbw, "slstm_forward_sequence", _fake_slstm_forward_sequence)
    fn = slstm_fwbw._rnn_fwbw_generator(torch.float32)
    ctx = _run_slstm_setup_context(fn, _slstm_inputs())
    _assert_amp_metadata(ctx, enabled=False)


def test_slstm_forward_saves_backward_context(monkeypatch: pytest.MonkeyPatch) -> None:
    slstm_fwbw = _slstm_module()
    monkeypatch.setattr(slstm_fwbw, "slstm_forward_sequence", _fake_slstm_forward_sequence)
    fn = slstm_fwbw._rnn_fwbw_generator(torch.float32)
    resets = torch.ones(2, 3, dtype=torch.bool, requires_grad=False)
    ctx = _run_slstm_setup_context(fn, _slstm_inputs(resets=resets, backward_recurrent_clip_val=1.25))

    assert len(ctx.saved_tensors) == 3
    assert ctx.backward_recurrent_clip_val == 1.25
    assert torch.equal(ctx.resets, resets)
    assert ctx.resets is not resets


def test_slstm_vmap_passthrough_uses_forward_impl(monkeypatch: pytest.MonkeyPatch) -> None:
    slstm_fwbw = _slstm_module()
    monkeypatch.setattr(slstm_fwbw, "slstm_forward_sequence", _fake_slstm_forward_sequence)
    fn = slstm_fwbw._rnn_fwbw_generator(torch.float32)
    outputs, out_dims = fn.vmap(None, (None,) * 6, *_slstm_inputs())
    all_states_visible, last_state_out, all_states, all_gates = outputs

    assert all_states_visible.shape == (3, 4, 2, 1, 1)
    assert last_state_out.shape == (4, 2, 1, 1)
    assert all_states.shape == (4, 4, 2, 1, 1)
    assert all_gates.shape == (4, 2, 1, 1, 1)
    assert out_dims == (None, None, None, None)


def test_mlstm_setup_context_sets_amp_metadata() -> None:
    fn, ctx, inputs, output = _mlstm_setup_context_case()
    fn.setup_context(ctx, inputs, output)
    _assert_amp_metadata(ctx, enabled=False)


def test_mlstm_setup_context_preserves_forward_autocast_state(monkeypatch: pytest.MonkeyPatch) -> None:
    fn, ctx, inputs, output = _mlstm_setup_context_case()
    monkeypatch.setattr(torch, "is_autocast_enabled", lambda device_type="cuda": device_type == "cuda")
    fn.setup_context(ctx, inputs, output)
    _assert_amp_metadata(ctx, enabled=True)
