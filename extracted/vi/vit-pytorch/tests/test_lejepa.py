import pytest
import torch
from torch import nn

from vit_pytorch import ViT
from vit_pytorch.lejepa import L2Norm, LeJEPA, MLP, sigreg_loss

def create_vit(image_size = 64):
    return ViT(
        image_size = image_size,
        patch_size = 16,
        num_classes = 10,
        dim = 64,
        depth = 2,
        heads = 4,
        mlp_dim = 128
    )

def test_lejepa_sigreg():
    model = create_vit()
    learner = LeJEPA(
        model,
        image_size = 64,
        hidden_layer = 'to_latent',
        projection_hidden_size = 64,
        projection_layers = 2,
        num_classes_K = 256
    )

    images = torch.randn(2, 3, 64, 64)
    loss = learner(images)
    loss.backward()

    assert torch.isfinite(loss)
    assert any(p.grad is not None for p in learner.encoder.parameters())
    assert any(p.grad is not None for p in learner.encoder.projector.parameters())

    proj, embed = learner(images, return_embedding = True)
    assert proj.shape == (2, 256)
    assert embed.shape == (2, 64)

    embed_only = learner(images, return_embedding = True, return_projection = False)
    assert embed_only.shape == (2, 64)

def test_mlp_no_gelu_before_l2norm_and_single_layer():
    mlp_multi = MLP(dim = 32, dim_out = 16, num_layers = 3, hidden_size = 24)
    modules = list(mlp_multi.net)
    l2_idx = next(i for i, m in enumerate(modules) if isinstance(m, L2Norm))
    assert isinstance(modules[l2_idx - 1], nn.Linear)
    assert mlp_multi(torch.randn(2, 32)).shape == (2, 16)

    mlp_single = MLP(dim = 32, dim_out = 16, num_layers = 1, hidden_size = 24)
    assert mlp_single(torch.randn(2, 32)).shape == (2, 16)

def test_lejepa_non_square_image_size():
    model = create_vit(image_size = (64, 48))
    learner = LeJEPA(
        model,
        image_size = (64, 48),
        hidden_layer = 'to_latent',
        projection_hidden_size = 32,
        projection_layers = 2,
        num_classes_K = 64
    )

    loss = learner(torch.randn(2, 3, 64, 48))
    loss.backward()
    assert torch.isfinite(loss)

@pytest.mark.parametrize('dtype', [torch.float32, torch.float64, torch.float16, torch.bfloat16])
def test_sigreg_loss_dtypes(dtype):
    x = torch.randn(4, 32, dtype = dtype)
    loss = sigreg_loss(x, num_slices = 64)
    assert torch.isfinite(loss)
