import pytest
import torch
from vit_pytorch import ViT
from vit_pytorch.lejepa import LeJEPA

def create_vit():
    return ViT(
        image_size = 64,
        patch_size = 16,
        num_classes = 10,
        dim = 64,
        depth = 2,
        heads = 4,
        mlp_dim = 128
    )

def test_lejepa_default_sigreg():
    model = create_vit()
    learner = LeJEPA(
        model,
        image_size = 64,
        hidden_layer = 'to_latent',
        projection_hidden_size = 64,
        projection_layers = 2,
        num_classes_K = 256
    )

    assert not learner.use_ema
    assert learner.use_sigreg
    assert learner.has_sigreg_loss
    assert learner.target_encoder is None

    images = torch.randn(2, 3, 64, 64)
    loss = learner(images)
    loss.backward()

    assert torch.isfinite(loss)

def test_lejepa_ema_instead_of_sigreg():
    model = create_vit()
    learner = LeJEPA(
        model,
        image_size = 64,
        hidden_layer = 'to_latent',
        projection_hidden_size = 64,
        projection_layers = 2,
        num_classes_K = 256,
        use_ema = True,
        moving_average_decay = 0.9
    )

    assert learner.use_ema
    assert not learner.use_sigreg
    assert not learner.has_sigreg_loss
    assert learner.target_encoder is not None

    opt = torch.optim.Adam(learner.parameters(), lr = 3e-4)

    images = torch.randn(2, 3, 64, 64)
    loss = learner(images)
    loss.backward()

    # check grads exist on online encoder and none on target encoder
    assert any(p.grad is not None for p in learner.encoder.parameters())
    assert all(p.grad is None for p in learner.target_encoder.parameters())

    # check moving average update
    param_before = list(learner.target_encoder.parameters())[0].clone()
    opt.step()
    learner.update_moving_average()
    param_after = list(learner.target_encoder.parameters())[0]

    assert not torch.equal(param_before, param_after)

def test_lejepa_flag_resolution():
    model = create_vit()

    # default
    l1 = LeJEPA(model, image_size = 64, hidden_layer = -1, projection_hidden_size = 32, num_classes_K = 64)
    assert not l1.use_ema and l1.use_sigreg

    # moving_average_decay implies use_ema
    l2 = LeJEPA(model, image_size = 64, hidden_layer = -1, projection_hidden_size = 32, num_classes_K = 64, moving_average_decay = 0.95)
    assert l2.use_ema and not l2.use_sigreg

    # use_sigreg = False implies use_ema
    l3 = LeJEPA(model, image_size = 64, hidden_layer = -1, projection_hidden_size = 32, num_classes_K = 64, use_sigreg = False)
    assert l3.use_ema and not l3.use_sigreg

    # both explicitly True
    l4 = LeJEPA(model, image_size = 64, hidden_layer = -1, projection_hidden_size = 32, num_classes_K = 64, use_ema = True, use_sigreg = True)
    assert l4.use_ema and l4.use_sigreg
