"""
Test LoRA adapter save/load/merge consistency.

Validates that:
1. model + merged_lora == model.load_adapter() + merge
2. Saving and loading adapters preserves weights
3. Merging produces clean models without LoRA artifacts
"""

import tempfile
from pathlib import Path
import torch
import pytest
from gliner2 import GLiNER2
from gliner2.training.lora import apply_lora_to_model, merge_lora_weights, LoRAConfig


def test_lora_merge_consistency():
    """
    Test that merging LoRA produces same weights whether:
    - Path A: Apply LoRA, train, merge directly
    - Path B: Apply LoRA, train, save adapter, load adapter, merge
    """
    # Load base model (use small model for faster testing)
    try:
        model = GLiNER2.from_pretrained("urchade/gliner_small_v2.1")
    except Exception as e:
        pytest.skip(f"Could not load model: {e}")
    
    # Save initial weights
    initial_state = {k: v.clone() for k, v in model.state_dict().items()}
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        adapter_path = Path(tmp_dir) / "adapter"
        merged_model_a_path = Path(tmp_dir) / "merged_a"
        merged_model_b_path = Path(tmp_dir) / "merged_b"
        
        # ===== Path A: Direct merge =====
        model_a = GLiNER2.from_pretrained("urchade/gliner_small_v2.1")
        
        # Apply LoRA
        lora_config = LoRAConfig(
            enabled=True,
            r=8,
            alpha=16.0,
            target_modules=["encoder"]
        )
        model_a, lora_layers_a = apply_lora_to_model(model_a, lora_config)
        model_a._lora_layers = lora_layers_a
        
        # Simulate training by modifying LoRA weights
        for lora_layer in lora_layers_a.values():
            lora_layer.lora_A.data += torch.randn_like(lora_layer.lora_A) * 0.01
            lora_layer.lora_B.data += torch.randn_like(lora_layer.lora_B) * 0.01
        
        # Save adapter before merging (for Path B)
        model_a.save_adapter(str(adapter_path))
        
        # Path A: Merge directly
        merge_lora_weights(model_a)
        model_a.save_pretrained(str(merged_model_a_path), merge_lora=False)
        
        # ===== Path B: Save adapter, load, then merge =====
        model_b = GLiNER2.from_pretrained("urchade/gliner_small_v2.1")
        model_b.load_adapter(str(adapter_path))
        merge_lora_weights(model_b)
        model_b.save_pretrained(str(merged_model_b_path), merge_lora=False)
        
        # ===== Verify both paths produce same weights =====
        from safetensors.torch import load_file
        state_a = load_file(str(merged_model_a_path / "model.safetensors"))
        state_b = load_file(str(merged_model_b_path / "model.safetensors"))
        
        # Check all weights match
        for key in state_a.keys():
            assert key in state_b, f"Key {key} missing in path B"
            diff = (state_a[key] - state_b[key]).abs().max().item()
            assert diff < 1e-6, f"Weight mismatch for {key}: max diff = {diff}"
        
        # Verify weights changed from initial (LoRA had an effect)
        model_final = GLiNER2.from_pretrained(str(merged_model_a_path))
        changed_params = 0
        for key in initial_state.keys():
            if 'encoder' in key and key in model_final.state_dict():
                final_val = model_final.state_dict()[key]
                init_val = initial_state[key]
                if (final_val - init_val).abs().max() > 1e-5:
                    changed_params += 1
        
        assert changed_params > 0, "LoRA should have changed some encoder weights"
        print(f"✓ LoRA merge consistency verified ({changed_params} params changed)")


def test_merge_removes_lora_artifacts():
    """Test that merge_lora_weights removes LoRA layers from the model."""
    try:
        model = GLiNER2.from_pretrained("urchade/gliner_small_v2.1")
    except Exception as e:
        pytest.skip(f"Could not load model: {e}")
    
    # Apply LoRA
    lora_config = LoRAConfig(
        enabled=True,
        r=8,
        alpha=16.0,
        target_modules=["encoder"]
    )
    model, lora_layers = apply_lora_to_model(model, lora_config)
    model._lora_layers = lora_layers
    
    # Verify LoRA layers exist
    from gliner2.training.lora import LoRALayer
    has_lora = any(isinstance(m, LoRALayer) for m in model.modules())
    assert has_lora, "Model should have LoRA layers after apply_lora_to_model"
    
    # Merge LoRA weights
    merge_lora_weights(model)
    
    # Verify LoRA layers are removed
    has_lora_after = any(isinstance(m, LoRALayer) for m in model.modules())
    assert not has_lora_after, "Model should NOT have LoRA layers after merge_lora_weights"
    
    # Verify state dict has no LoRA keys
    state_dict = model.state_dict()
    lora_keys = [k for k in state_dict.keys() if 'lora_A' in k or 'lora_B' in k]
    assert len(lora_keys) == 0, f"State dict should not contain LoRA keys, found: {lora_keys}"
    
    print("✓ merge_lora_weights correctly removes LoRA artifacts")


def test_save_pretrained_with_merge_lora():
    """Test that save_pretrained with merge_lora=True produces clean checkpoints."""
    try:
        model = GLiNER2.from_pretrained("urchade/gliner_small_v2.1")
    except Exception as e:
        pytest.skip(f"Could not load model: {e}")
    
    # Apply LoRA
    lora_config = LoRAConfig(
        enabled=True,
        r=8,
        alpha=16.0,
        target_modules=["encoder"]
    )
    model, lora_layers = apply_lora_to_model(model, lora_config)
    model._lora_layers = lora_layers
    
    # Modify LoRA weights
    for lora_layer in lora_layers.values():
        lora_layer.lora_A.data += torch.randn_like(lora_layer.lora_A) * 0.01
        lora_layer.lora_B.data += torch.randn_like(lora_layer.lora_B) * 0.01
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        save_path = Path(tmp_dir) / "merged_model"
        
        # Save with merge_lora=True
        model.save_pretrained(str(save_path), merge_lora=True)
        
        # Load saved model
        from safetensors.torch import load_file
        state_dict = load_file(str(save_path / "model.safetensors"))
        
        # Verify no LoRA keys in saved state dict
        lora_keys = [k for k in state_dict.keys() if 'lora_A' in k or 'lora_B' in k]
        assert len(lora_keys) == 0, f"Saved model should not contain LoRA keys, found: {lora_keys}"
        
        # Verify model instance no longer has LoRA
        from gliner2.training.lora import LoRALayer
        has_lora = any(isinstance(m, LoRALayer) for m in model.modules())
        assert not has_lora, "Model instance should not have LoRA layers after save with merge_lora=True"
        
        # Verify we can load the saved model
        loaded_model = GLiNER2.from_pretrained(str(save_path))
        assert loaded_model is not None, "Should be able to load merged model"
        
        # Verify loaded model has no LoRA artifacts
        has_lora_loaded = any(isinstance(m, LoRALayer) for m in loaded_model.modules())
        assert not has_lora_loaded, "Loaded model should not have LoRA layers"
        
        print("✓ save_pretrained with merge_lora=True produces clean checkpoints")


def test_save_adapter_then_merge():
    """Test the full workflow: save adapter, load on fresh model, merge."""
    try:
        base_model = GLiNER2.from_pretrained("urchade/gliner_small_v2.1")
    except Exception as e:
        pytest.skip(f"Could not load model: {e}")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        adapter_path = Path(tmp_dir) / "adapter"
        merged_path = Path(tmp_dir) / "merged"
        
        # Apply LoRA and modify weights
        lora_config = LoRAConfig(
            enabled=True,
            r=8,
            alpha=16.0,
            target_modules=["encoder"]
        )
        model, lora_layers = apply_lora_to_model(base_model, lora_config)
        model._lora_layers = lora_layers
        
        # Simulate training
        for lora_layer in lora_layers.values():
            lora_layer.lora_A.data += torch.randn_like(lora_layer.lora_A) * 0.01
            lora_layer.lora_B.data += torch.randn_like(lora_layer.lora_B) * 0.01
        
        # Save adapter only
        model.save_adapter(str(adapter_path))
        
        # Load fresh model and apply adapter
        fresh_model = GLiNER2.from_pretrained("urchade/gliner_small_v2.1")
        fresh_model.load_adapter(str(adapter_path))
        
        # Merge and save
        fresh_model.save_pretrained(str(merged_path), merge_lora=True)
        
        # Verify merged model works
        final_model = GLiNER2.from_pretrained(str(merged_path))
        assert final_model is not None, "Should be able to load final merged model"
        
        # Verify no LoRA artifacts
        from gliner2.training.lora import LoRALayer
        has_lora = any(isinstance(m, LoRALayer) for m in final_model.modules())
        assert not has_lora, "Final model should not have LoRA layers"
        
        print("✓ Full workflow (save adapter → load → merge) works correctly")


def test_model_merge_lora_method():
    """Test the model.merge_lora() convenience method."""
    try:
        model = GLiNER2.from_pretrained("urchade/gliner_small_v2.1")
    except Exception as e:
        pytest.skip(f"Could not load model: {e}")
    
    # Apply LoRA
    lora_config = LoRAConfig(
        enabled=True,
        r=8,
        alpha=16.0,
        target_modules=["encoder"]
    )
    model, lora_layers = apply_lora_to_model(model, lora_config)
    model._lora_layers = lora_layers
    
    # Verify LoRA is loaded
    assert model.has_adapter, "Model should have adapter before merge"
    
    # Modify LoRA weights
    for lora_layer in lora_layers.values():
        lora_layer.lora_A.data += torch.randn_like(lora_layer.lora_A) * 0.01
        lora_layer.lora_B.data += torch.randn_like(lora_layer.lora_B) * 0.01
    
    # Call merge_lora() method
    result = model.merge_lora()
    
    # Should return self for chaining
    assert result is model, "merge_lora() should return self for chaining"
    
    # Verify adapter is removed
    assert not model.has_adapter, "Model should not have adapter after merge"
    assert model._lora_layers == {}, "Internal _lora_layers should be empty"
    assert model._adapter_config is None, "Internal _adapter_config should be None"
    
    # Verify no LoRA layers in model
    from gliner2.training.lora import LoRALayer
    has_lora = any(isinstance(m, LoRALayer) for m in model.modules())
    assert not has_lora, "Model should not have LoRA layers after merge_lora()"
    
    # Verify state dict has no LoRA keys
    state_dict = model.state_dict()
    lora_keys = [k for k in state_dict.keys() if 'lora_A' in k or 'lora_B' in k]
    assert len(lora_keys) == 0, f"State dict should not contain LoRA keys, found: {lora_keys}"
    
    print("✓ model.merge_lora() method works correctly")


def test_merge_lora_without_adapter_raises_error():
    """Test that merge_lora() raises error when no adapter is loaded."""
    try:
        model = GLiNER2.from_pretrained("urchade/gliner_small_v2.1")
    except Exception as e:
        pytest.skip(f"Could not load model: {e}")
    
    # Try to merge without loading adapter
    with pytest.raises(ValueError, match="No adapter loaded"):
        model.merge_lora()
    
    print("✓ merge_lora() correctly raises error when no adapter loaded")


if __name__ == "__main__":
    print("Running LoRA merge consistency tests...")
    test_lora_merge_consistency()
    test_merge_removes_lora_artifacts()
    test_save_pretrained_with_merge_lora()
    test_save_adapter_then_merge()
    test_model_merge_lora_method()
    test_merge_lora_without_adapter_raises_error()
    print("\n✅ All tests passed!")

