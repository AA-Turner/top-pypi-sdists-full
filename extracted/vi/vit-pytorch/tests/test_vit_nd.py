import math

import pytest
import torch
from torch.nn.attention.flex_attention import create_block_mask, flex_attention

from vit_pytorch.vit_nd import ViTND

def reference_causal_mask(num_patches_per_dim, causal_dims, seq_len):
    # manually compute expected mask for row-major token layout, with cls token at index 0
    mask = torch.ones(seq_len, seq_len, dtype = torch.bool)

    for qi in range(1, seq_len):
        for kj in range(1, seq_len):
            q_idx = qi - 1
            k_idx = kj - 1

            allowed = True
            for d in causal_dims:
                stride = math.prod(num_patches_per_dim[d + 1:])
                q_coord = (q_idx // stride) % num_patches_per_dim[d]
                k_coord = (k_idx // stride) % num_patches_per_dim[d]
                allowed &= q_coord >= k_coord

            mask[qi, kj] = allowed

    return mask

@pytest.mark.parametrize('ndim, input_shape, causal_dims', [
    (2, (2, 4), (0,)),
    (2, (2, 4), (0, 1)),
    (3, (2, 3, 4), (0,)),
    (3, (2, 3, 4), (0, 1)),
    (3, (2, 3, 4), (0, 2)),
])
def test_vit_nd_causal(ndim, input_shape, causal_dims):
    v = ViTND(
        ndim = ndim,
        input_shape = input_shape,
        patch_size = (1,) * ndim,
        num_classes = 10,
        dim = 32,
        depth = 2,
        heads = 4,
        mlp_dim = 64,
        causal_dims = causal_dims
    )

    num_patches = math.prod(input_shape)
    seq_len = num_patches + 1

    q_idx = torch.arange(seq_len)[:, None]
    k_idx = torch.arange(seq_len)[None, :]

    mask = v.causal_mask_fn(0, 0, q_idx, k_idx)

    assert mask[0].all() and mask[:, 0].all(), 'cls token attends to all and is attended to by all'

    ref = reference_causal_mask(input_shape, causal_dims, seq_len)
    assert torch.equal(mask, ref), 'causal mask incorrect along the given causal dims'

    # flex attention with the mask function should agree with manual attention

    b, heads, dim_head = 2, 4, 8

    q = torch.randn(b, heads, seq_len, dim_head)
    k = torch.randn(b, heads, seq_len, dim_head)
    value = torch.randn(b, heads, seq_len, dim_head)

    block_mask = create_block_mask(v.causal_mask_fn, 1, heads, seq_len, seq_len, device = 'cpu')

    flex_out = flex_attention(q, k, value, block_mask = block_mask, scale = dim_head ** -0.5)

    scores = torch.matmul(q, k.transpose(-1, -2)) * (dim_head ** -0.5)
    scores = scores.masked_fill(~mask, -torch.finfo(scores.dtype).max)
    manual_out = torch.softmax(scores, dim = -1) @ value

    assert torch.allclose(flex_out, manual_out, atol = 1e-4), 'flex attention must agree with manual attention'

    # model runs end to end

    data = torch.randn(2, 3, *input_shape)

    preds = v(data)
    assert preds.shape == (2, 10), 'correct logits outputted'

def test_vit_nd_causal_lone_int():
    # a lone int for causal_dims should be equivalent to a 1-tuple

    v_int = ViTND(
        ndim = 3,
        input_shape = (2, 3, 4),
        patch_size = (1,) * 3,
        num_classes = 10,
        dim = 32,
        depth = 2,
        heads = 4,
        mlp_dim = 64,
        causal_dims = 0
    )

    v_tuple = ViTND(
        ndim = 3,
        input_shape = (2, 3, 4),
        patch_size = (1,) * 3,
        num_classes = 10,
        dim = 32,
        depth = 2,
        heads = 4,
        mlp_dim = 64,
        causal_dims = (0,)
    )

    v_tuple.load_state_dict(v_int.state_dict())

    data = torch.randn(2, 3, 2, 3, 4)

    assert torch.allclose(v_int(data), v_tuple(data)), 'lone int causal_dims must match 1-tuple'
