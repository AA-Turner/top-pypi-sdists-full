import pytest
import torch
from mmgp import offload


def test_directional_rules_and_universal_cotenant():
    manager = object.__new__(offload.offload)
    manager.cotenants_map = {"text_encoder_2": ["text_encoder"], "tiny_vae": "*"}
    manager.active_models_ids = ["text_encoder"]
    assert manager.can_model_be_cotenant("text_encoder_2")
    assert manager.can_model_be_cotenant("tiny_vae")
    manager.active_models_ids = ["text_encoder_2", "tiny_vae"]
    assert not manager.can_model_be_cotenant("text_encoder")
    manager.active_models_ids = ["tiny_vae"]
    assert manager.can_model_be_cotenant("transformer")


@pytest.mark.skipif(not torch.cuda.is_available(), reason="Requires CUDA")
def test_universal_cotenant_survives_switches_but_explicit_unload_releases_it():
    models = {name: torch.nn.Linear(4, 4, device="cpu").eval() for name in ("transformer", "vae", "tiny_vae")}
    manager = offload.profile(models, profile_no=5, quantizeTransformer=False, coTenantsMap={"tiny_vae":"*"})
    value = torch.ones(1, 4, device="cuda", dtype=torch.bfloat16)
    try:
        with torch.inference_mode():
            models["transformer"](value)
            models["tiny_vae"](value)
            pointer = models["tiny_vae"].weight.data_ptr()
            models["vae"](value)
            assert set(manager.active_models_ids) == {"vae", "tiny_vae"}
            assert models["transformer"].weight.device.type == "cpu"
            models["transformer"](value)
            assert set(manager.active_models_ids) == {"transformer", "tiny_vae"}
            assert models["tiny_vae"].weight.data_ptr() == pointer
        manager.unload_all()
        assert not manager.active_models_ids
        assert all(model.weight.device.type == "cpu" for model in models.values())
    finally:
        manager.release()
