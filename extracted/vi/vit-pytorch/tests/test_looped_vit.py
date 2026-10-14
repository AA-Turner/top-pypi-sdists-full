import pytest
import torch
from torch import stack
import torch.nn.functional as F
from einops import rearrange

from vit_pytorch.looped_vit import (
    Attention,
    LoopedViT,
    adaptive_exit_targets,
    deep_supervision_loss,
    deep_supervision_weights,
    per_loop_losses,
)

def make_vit(**kwargs):
    return LoopedViT(
        ndim = 2,
        input_shape = (32, 32),
        patch_size = 8,
        num_classes = 10,
        dim = 32,
        pre_loop_depth = 2,
        num_looped_blocks = 2,
        post_loop_depth = 2,
        loop_depth = 4,
        heads = 4,
        dim_head = 8,
        mlp_dim = 64,
        **kwargs,
    )

@pytest.mark.parametrize('ndim, input_shape, patch_size', [
    (1, (16,), 4),
    (2, (32, 32), 8),
    (3, (16, 16, 16), 8),
    (4, (8, 8, 8, 8), 4),
])
@pytest.mark.parametrize('pool', ('cls', 'mean'))
def test_looped_vit_nd(ndim, input_shape, patch_size, pool):
    v = LoopedViT(
        ndim = ndim,
        input_shape = input_shape,
        patch_size = patch_size,
        num_classes = 10,
        dim = 32,
        pre_loop_depth = 2,
        num_looped_blocks = 2,
        post_loop_depth = 2,
        loop_depth = 4,
        pool = pool,
        heads = 4,
        dim_head = 8,
        mlp_dim = 64,
    )

    data = torch.randn(2, 3, *input_shape)

    assert v(data).shape == (2, 10)

    # intermediate loop predictions, deep supervised through the shared post loop stage

    all_logits = v(data, return_all_logits = True)
    assert all_logits.shape == (4, 2, 10)

    # loop depth is a free inference time dial

    assert v(data, loop_depth = 1).shape == (2, 10)
    assert v(data, loop_depth = 8, return_all_logits = True).shape == (8, 2, 10)

def test_looping_changes_compute_not_parameters():
    img = torch.randn(2, 3, 32, 32)

    v = make_vit()
    num_params = sum(p.numel() for p in v.parameters())

    # the looped transformer is shared - loop depth changes compute, not parameters

    assert len(v.looped.layers) == 2
    assert v(img, loop_depth = 1).shape == (2, 10)
    assert v(img, loop_depth = 8).shape == (2, 10)
    assert sum(p.numel() for p in v.parameters()) == num_params

def test_loop_weights_are_non_persistent():
    v = make_vit()

    # supervision weights are a training time choice, kept out of the state dict

    assert 'loop_weights' not in v.state_dict()
    assert torch.allclose(v.loop_weights, deep_supervision_weights(4, 'final_mean'))

    custom = (1., 0.5, 0.25, 0.125)
    v_custom = make_vit(deep_supervision_weighting = custom)

    assert torch.allclose(v_custom.loop_weights, torch.tensor(custom))

    # the buffer plugs straight into the loss

    all_logits = v(torch.randn(2, 3, 32, 32), return_all_logits = True)
    labels = torch.randint(0, 10, (2,))

    loss = deep_supervision_loss(all_logits, labels, weighting = v.loop_weights)
    assert torch.isfinite(loss)

def test_attention_has_gate_without_bias():
    attn = Attention(dim = 32, heads = 4, dim_head = 8)
    assert attn.to_gate.bias is None

def test_xsa_projects_out_own_value_direction():
    attn = Attention(dim = 32, heads = 4, dim_head = 8).eval()

    outputs = {}
    attn.to_out.register_forward_hook(lambda _, inputs, __: outputs.setdefault('z', inputs[0]))

    x = torch.randn(2, 5, 32)

    with torch.no_grad():
        attn(x)

        normed = attn.norm(x)
        q, k, v = attn.to_qkv(normed).chunk(3, dim = -1)
        q, k, v = map(lambda t: rearrange(t, 'b n (h d) -> b h n d', h = 4), (q, k, v))

        out = torch.softmax(torch.matmul(q, k.transpose(-1, -2)) * attn.scale, dim = -1) @ v
        z = rearrange(outputs['z'], 'b n (h d) -> b h n d', h = 4)

        v_hat = F.normalize(v, dim = -1)

        # modulated head output is orthogonal to the token's own value direction
        # and non expansive before the output projection

        orthogonal = (z * v_hat).sum(dim = -1)
        assert torch.allclose(orthogonal, torch.zeros_like(z[..., 0]), atol = 1e-5)
        assert (z.norm(dim = -1) <= out.norm(dim = -1) + 1e-5).all()

def test_deep_supervision_weightings():
    assert deep_supervision_weights(4, 'final').tolist() == [0., 0., 0., 1.]

    expected_exponential = torch.tensor([1 / 8, 1 / 4, 1 / 2, 1.])
    assert torch.allclose(deep_supervision_weights(4, 'exponential'), expected_exponential)

    expected_final_mean = torch.tensor([1 / 3, 1 / 3, 1 / 3, 1.])
    assert torch.allclose(deep_supervision_weights(4, 'final_mean'), expected_final_mean)

    assert torch.allclose(deep_supervision_weights(1, 'final_mean'), torch.tensor([1.]))

    with pytest.raises(AssertionError):
        deep_supervision_weights(4, 'uniform')

def test_deep_supervision_loss_matches_manual_weighted_sum():
    logits = torch.randn(4, 3, 10)
    labels = torch.randint(0, 10, (3,))

    losses = per_loop_losses(logits, labels)

    for weighting in ('final', 'exponential', 'final_mean'):
        weights = deep_supervision_weights(4, weighting)
        expected = (losses * rearrange(weights, 'l -> l 1')).sum(dim = 0).mean()

        loss = deep_supervision_loss(logits, labels, weighting = weighting)
        assert torch.allclose(loss, expected, atol = 1e-6)

def test_deep_supervision_loss_semantics():
    logits = torch.randn(4, 3, 10)
    labels = torch.randint(0, 10, (3,))

    losses = per_loop_losses(logits, labels)

    # paper eqn (3) - a weighted sum over loops, batch mean outside, with unnormalized weights

    expected = (losses[:3].mean(dim = 0) + losses[3]).mean()
    loss = deep_supervision_loss(logits, labels, 'final_mean')
    assert torch.allclose(loss, expected, atol = 1e-6)

    expected = (losses[0] / 8 + losses[1] / 4 + losses[2] / 2 + losses[3]).mean()
    loss = deep_supervision_loss(logits, labels, 'exponential')
    assert torch.allclose(loss, expected, atol = 1e-6)

    expected = losses[3].mean()
    loss = deep_supervision_loss(logits, labels, 'final')
    assert torch.allclose(loss, expected, atol = 1e-6)

def test_custom_deep_supervision_weights():
    logits = torch.randn(4, 3, 10)
    labels = torch.randint(0, 10, (3,))

    losses = per_loop_losses(logits, labels)
    custom = (1., 0.5, 0.25, 0.125)

    # weights may be given as any (w1, ..., wn) sequence or tensor, and must match the loop count

    assert torch.allclose(deep_supervision_weights(4, custom), torch.tensor(custom))
    assert torch.allclose(deep_supervision_weights(4, torch.tensor(custom)), torch.tensor(custom))

    expected = (losses * rearrange(torch.tensor(custom), 'l -> l 1')).sum(dim = 0).mean()

    loss = deep_supervision_loss(logits, labels, weighting = custom)
    assert torch.allclose(loss, expected, atol = 1e-6)

    with pytest.raises(AssertionError):
        deep_supervision_weights(4, (1., 1.))

def test_intermediate_loop_states_not_decoded_at_inference():
    # paper - deep supervision adds no inference compute, intermediates are training only

    v = make_vit()
    img = torch.randn(2, 3, 32, 32)

    calls = []
    hook = v.post_loop.register_forward_hook(lambda *_: calls.append(1))

    v(img)
    assert len(calls) == 1, 'post loop stage runs once per plain inference pass'

    v(img, loop_depth = 8)
    assert len(calls) == 2, 'raising inference loop depth must not decode intermediate states'

    v(img, return_all_logits = True)
    assert len(calls) == 6, 'all loop states decoded when deep supervising'

    hook.remove()

def test_deep_supervision_trains_all_loops():
    v = make_vit()

    img = torch.randn(2, 3, 32, 32)
    labels = torch.randint(0, 10, (2,))

    all_logits = v(img, return_all_logits = True)
    loss = deep_supervision_loss(all_logits, labels)
    loss.backward()

    # every loop of the shared transformer receives a learning signal

    for layer in v.looped.layers:
        for module in layer:
            for param in module.parameters():
                assert param.grad is not None and torch.isfinite(param.grad).all()

def test_adaptive_exit_targets():
    logits = torch.randn(4, 3, 10, dtype = torch.float64)
    labels = torch.randint(0, 10, (3,))

    losses = per_loop_losses(logits, labels)
    targets = adaptive_exit_targets(logits, labels)

    expected = []
    for loop in range(3):
        extra_loops = torch.arange(1, 4 - loop, dtype = losses.dtype)
        gains = (losses[loop] - losses[loop + 1:]) / rearrange(extra_loops, 'l -> l 1')
        expected.append(gains.clamp(min = 0.).amax(dim = 0))

    assert targets.shape == (3, 3)
    assert torch.allclose(targets, stack(expected))

def test_adaptive_looping():
    v = make_vit(adaptive_loop = True)
    img = torch.randn(2, 3, 32, 32)
    labels = torch.randint(0, 10, (2,))

    logits, exit_benefits = v(img, return_all_logits = True, return_exit_benefits = True)
    assert logits.shape == (4, 2, 10)
    assert exit_benefits.shape == (3, 2)

    targets = adaptive_exit_targets(logits, labels)
    gate_loss = F.mse_loss(exit_benefits, targets)
    gate_loss.backward()

    assert all(p.grad is not None for p in v.exit_gate.parameters())
    assert torch.isfinite(gate_loss)

    # exiting as soon as the gate stops predicting any benefit, versus never exiting

    all_logits = v(img, adaptive_exit = True, exit_threshold = 1e9, return_all_logits = True)
    assert all_logits.shape == (1, 2, 10)

    all_logits = v(img, adaptive_exit = True, exit_threshold = -1e9, return_all_logits = True)
    assert all_logits.shape == (4, 2, 10)

    with pytest.raises(AssertionError):
        make_vit()(img, return_exit_benefits = True)
