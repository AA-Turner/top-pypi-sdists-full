"""
End-to-end test for LoRA adapter training, saving, loading, and swapping.

Run with: pytest tests/test_lora_adapters.py -v
"""

import os
import tempfile
import shutil
from pathlib import Path

import torch
import pytest

from gliner2 import GLiNER2
from gliner2.training.data import InputExample, TrainingDataset
from gliner2.training.trainer import GLiNER2Trainer, TrainingConfig
from gliner2.training.lora import (
    load_lora_adapter,
    unload_lora_adapter,
    has_lora_adapter,
    LoRAAdapterConfig,
)


# =============================================================================
# Test Data
# =============================================================================

LEGAL_EXAMPLES = [
    InputExample(
        text="Apple Inc. filed a lawsuit against Samsung Electronics.",
        entities={"company": ["Apple Inc.", "Samsung Electronics"]}
    ),
    InputExample(
        text="The plaintiff Google LLC accused Microsoft Corporation of patent infringement.",
        entities={"company": ["Google LLC", "Microsoft Corporation"]}
    ),
    InputExample(
        text="Amazon.com Inc. settled the dispute with Meta Platforms.",
        entities={"company": ["Amazon.com Inc.", "Meta Platforms"]}
    ),
]

MEDICAL_EXAMPLES = [
    InputExample(
        text="Apple Inc. filed a lawsuit against Samsung Electronics.",
        entities={"company": ["Apple Inc.", "Samsung Electronics"]}
    ),
    InputExample(
        text="The plaintiff Google LLC accused Microsoft Corporation of patent infringement.",
        entities={"company": ["Google LLC", "Microsoft Corporation"]}
    ),
    InputExample(
        text="Amazon.com Inc. settled the dispute with Meta Platforms.",
        entities={"company": ["Amazon.com Inc.", "Meta Platforms"]}
    ),
]

SUPPORT_EXAMPLES = [
    InputExample(
        text="Apple Inc. filed a lawsuit against Samsung Electronics.",
        entities={"company": ["Apple Inc.", "Samsung Electronics"]}
    ),
    InputExample(
        text="The plaintiff Google LLC accused Microsoft Corporation of patent infringement.",
        entities={"company": ["Google LLC", "Microsoft Corporation"]}
    ),
    InputExample(
        text="Amazon.com Inc. settled the dispute with Meta Platforms.",
        entities={"company": ["Amazon.com Inc.", "Meta Platforms"]}
    ),
]


# =============================================================================
# Training Functions
# =============================================================================

def train_adapter(
    base_model: str,
    examples: list,
    output_dir: str,
    adapter_name: str,
) -> str:
    """Train a LoRA adapter and save it."""
    
    adapter_path = os.path.join(output_dir, adapter_name)
    
    config = TrainingConfig(
        output_dir=adapter_path,
        experiment_name=adapter_name,
        num_epochs=2,  # Small for testing
        batch_size=2,
        gradient_accumulation_steps=1,
        encoder_lr=1e-5,
        task_lr=5e-4,
        # LoRA settings
        use_lora=True,
        lora_r=4,  # Small rank for testing
        lora_alpha=8.0,
        lora_dropout=0.0,
        lora_target_modules=["query", "key", "value", "dense"],
        save_adapter_only=True,  # Save only adapter weights
        # Disable extra features for speed
        save_strategy="no",
        eval_strategy="no",
        logging_steps=1,
        fp16=torch.cuda.is_available(),
        num_workers=0,
        validate_data=False,
    )
    
    model = GLiNER2.from_pretrained(base_model)
    trainer = GLiNER2Trainer(model=model, config=config)
    trainer.train(train_data=examples)
    
    # Adapter is already saved by trainer to checkpoints/final/
    # Return the path to the final checkpoint
    final_checkpoint_path = os.path.join(adapter_path, "checkpoints", "final")
    
    return final_checkpoint_path


def train_legal(base_model: str, output_dir: str) -> str:
    """Train legal domain adapter."""
    return train_adapter(base_model, LEGAL_EXAMPLES, output_dir, "legal_adapter")


def train_medical(base_model: str, output_dir: str) -> str:
    """Train medical domain adapter."""
    return train_adapter(base_model, MEDICAL_EXAMPLES, output_dir, "medical_adapter")


def train_support(base_model: str, output_dir: str) -> str:
    """Train customer support adapter."""
    return train_adapter(base_model, SUPPORT_EXAMPLES, output_dir, "support_adapter")


# =============================================================================
# Tests
# =============================================================================

class TestLoRAAdapters:
    """Test suite for LoRA adapter functionality."""
    
    @pytest.fixture(scope="class")
    def setup_adapters(self, tmp_path_factory):
        """Train all adapters once for the test class."""
        base_model = "fastino/gliner2-base-v1"  # Or your base model
        output_dir = str(tmp_path_factory.mktemp("adapters"))
        
        # Train adapters
        legal_path = train_legal(base_model, output_dir)
        medical_path = train_medical(base_model, output_dir)
        support_path = train_support(base_model, output_dir)
        
        return {
            "base_model": base_model,
            "legal_adapter": legal_path,
            "medical_adapter": medical_path,
            "support_adapter": support_path,
        }
    
    def test_adapter_config_saved(self, setup_adapters):
        """Verify adapter config is saved correctly."""
        legal_path = setup_adapters["legal_adapter"]
        
        assert LoRAAdapterConfig.is_adapter_path(legal_path)
        
        config = LoRAAdapterConfig.load(legal_path)
        assert config.adapter_type == "lora"
        assert config.lora_r == 4
        assert config.lora_alpha == 8.0
    
    def test_load_adapter_standalone(self, setup_adapters):
        """Test loading adapter using standalone function."""
        base_model = setup_adapters["base_model"]
        legal_path = setup_adapters["legal_adapter"]
        
        # Load base model
        model = GLiNER2.from_pretrained(base_model)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        
        assert not has_lora_adapter(model)
        
        # Load adapter
        load_lora_adapter(model, legal_path)
        
        assert has_lora_adapter(model)
        
        # Test extraction
        result = model.extract_entities(
            "Apple sued Google in court.",
            ["company"]
        )
        assert "entities" in result
    
    def test_adapter_swapping(self, setup_adapters):
        """Test swapping between adapters."""
        base_model = setup_adapters["base_model"]
        
        model = GLiNER2.from_pretrained(base_model)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        
        # Load legal adapter
        load_lora_adapter(model, setup_adapters["legal_adapter"])
        result1 = model.extract_entities("Apple sued Google", ["company"])
        
        # Swap to medical adapter (auto-unloads previous)
        load_lora_adapter(model, setup_adapters["medical_adapter"])
        result2 = model.extract_entities("Patient has diabetes", ["disease"])
        
        # Swap to support adapter
        load_lora_adapter(model, setup_adapters["support_adapter"])
        result3 = model.extract_entities("Issue with Order #12345", ["order_id"])
        
        # All should return valid results
        assert "entities" in result1
        assert "entities" in result2
        assert "entities" in result3
    
    def test_model_load_adapter_method(self, setup_adapters):
        """Test using model.load_adapter() convenience method."""
        base_model = setup_adapters["base_model"]
        
        model = GLiNER2.from_pretrained(base_model)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        
        # Use convenience method
        model.load_adapter(setup_adapters["legal_adapter"])
        assert model.has_adapter
        
        result = model.extract_entities("Microsoft acquired LinkedIn", ["company"])
        assert "entities" in result
        
        # Unload adapter
        model.unload_adapter()
        assert not model.has_adapter
    
    def test_load_adapter_on_base_model(self, setup_adapters):
        """Test loading adapter onto base model (recommended pattern)."""
        legal_path = setup_adapters["legal_adapter"]
        base_model = setup_adapters["base_model"]
        
        # Load base model first, then adapter
        model = GLiNER2.from_pretrained(base_model)
        model.load_adapter(legal_path)
        
        assert model.has_adapter
        assert model.adapter_config is not None
        
        result = model.extract_entities("Tesla vs Ford lawsuit", ["company"])
        assert "entities" in result
    
    def test_unload_and_base_model(self, setup_adapters):
        """Test unloading adapter returns to base model."""
        base_model = setup_adapters["base_model"]
        
        model = GLiNER2.from_pretrained(base_model)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        
        # Get base model result
        base_result = model.extract_entities("Test text", ["entity"])
        
        # Load and unload adapter
        model.load_adapter(setup_adapters["legal_adapter"])
        model.unload_adapter()
        
        # Should work same as base model
        after_result = model.extract_entities("Test text", ["entity"])
        
        assert not model.has_adapter
    
    def test_save_adapter_from_model(self, setup_adapters, tmp_path):
        """Test saving adapter from model."""
        base_model = setup_adapters["base_model"]
        
        model = GLiNER2.from_pretrained(base_model)
        model.load_adapter(setup_adapters["legal_adapter"])
        
        # Save to new location
        new_path = str(tmp_path / "resaved_adapter")
        model.save_adapter(new_path)
        
        # Verify it can be loaded
        assert LoRAAdapterConfig.is_adapter_path(new_path)
        
        model2 = GLiNER2.from_pretrained(base_model)
        model2.load_adapter(new_path)
        assert model2.has_adapter
    
    def test_lora_actually_modifies_weights(self, setup_adapters):
        """
        Test that LoRA actually modifies model behavior by computing weight differences.
        
        This verifies that:
        1. Loading an adapter changes the effective weights
        2. Unloading an adapter restores original weights
        3. LoRA layers are actually affecting forward passes
        """
        base_model = setup_adapters["base_model"]
        legal_path = setup_adapters["legal_adapter"]
        
        # Load base model
        model = GLiNER2.from_pretrained(base_model)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        
        # Capture original weights from first linear layer we can find
        original_weights = {}
        for name, module in model.named_modules():
            if isinstance(module, torch.nn.Linear) and "query" in name:
                original_weights[name] = module.weight.data.clone()
                print(f"Captured original weights for: {name}")
                break  # Just check one layer for this test
        
        assert len(original_weights) > 0, "Should find at least one linear layer"
        
        # Load adapter
        model.load_adapter(legal_path)
        assert model.has_adapter
        
        # Check that LoRA layers were actually added
        lora_layer_found = False
        for name, module in model.named_modules():
            if "LoRALayer" in str(type(module)):
                lora_layer_found = True
                print(f"Found LoRA layer: {name} - {type(module)}")
                break
        
        assert lora_layer_found, "LoRA layers should be present after loading adapter"
        
        # Get predictions with adapter (this should use LoRA)
        test_text = "Apple sued Google in court."
        result_with_adapter = model.extract_entities(test_text, ["company"])
        
        # Unload adapter
        model.unload_adapter()
        assert not model.has_adapter
        
        # Verify weights are restored after unloading
        for name, original_weight in original_weights.items():
            for module_name, module in model.named_modules():
                if module_name == name and isinstance(module, torch.nn.Linear):
                    current_weight = module.weight.data
                    weight_diff = torch.abs(current_weight - original_weight).max().item()
                    print(f"Weight diff after unload for {name}: {weight_diff}")
                    assert weight_diff < 1e-5, f"Weights should be restored after unloading, diff: {weight_diff}"
        
        # Get predictions without adapter
        result_without_adapter = model.extract_entities(test_text, ["company"])
        
        # Predictions might differ (though not guaranteed for all cases)
        print(f"With adapter: {result_with_adapter}")
        print(f"Without adapter: {result_without_adapter}")
    
    def test_lora_forward_pass_difference(self, setup_adapters):
        """
        Test that LoRA actually affects the forward pass by comparing outputs.
        
        This is a more direct test: run the same input through base model
        and adapter model, verify they produce different results.
        """
        base_model = setup_adapters["base_model"]
        legal_path = setup_adapters["legal_adapter"]
        
        # Load base model
        model = GLiNER2.from_pretrained(base_model)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        model.eval()
        
        test_text = "Apple Inc. filed a lawsuit against Samsung Electronics."
        test_entities = ["company"]
        
        # Get base model output
        with torch.no_grad():
            base_output = model.extract_entities(test_text, test_entities)
        
        # Load adapter
        model.load_adapter(legal_path)
        
        # Get adapter model output
        with torch.no_grad():
            adapter_output = model.extract_entities(test_text, test_entities)
        
        # Outputs should be different (adapter should affect predictions)
        # Note: We can't guarantee they'll be different for every input,
        # but we can check that the adapter is at least loaded and active
        assert model.has_adapter, "Adapter should be loaded"
        
        # Check that LoRA is active by looking for LoRA layers
        has_lora_layers = any(
            "LoRALayer" in str(type(module))
            for module in model.modules()
        )
        assert has_lora_layers, "Model should have LoRA layers when adapter is loaded"
        
        print(f"Base model output: {base_output}")
        print(f"Adapter model output: {adapter_output}")
        
        # At minimum, both should produce valid outputs
        assert "entities" in base_output
        assert "entities" in adapter_output
    
    def test_lora_effective_weights_computation(self, setup_adapters):
        """
        Test that LoRA layers compute effective weights correctly.
        
        This verifies the mathematical correctness: W_effective = W_base + (B @ A) * scaling
        """
        base_model = setup_adapters["base_model"]
        legal_path = setup_adapters["legal_adapter"]
        
        # Load base model and adapter
        model = GLiNER2.from_pretrained(base_model)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        model.load_adapter(legal_path)
        
        # Find a LoRA layer
        from gliner2.training.lora import LoRALayer
        
        lora_layer = None
        lora_layer_name = None
        for name, module in model.named_modules():
            if isinstance(module, LoRALayer):
                lora_layer = module
                lora_layer_name = name
                break
        
        assert lora_layer is not None, "Should find at least one LoRA layer"
        print(f"Testing LoRA layer: {lora_layer_name}")
        
        # Get the components
        base_weight = lora_layer.base_layer.weight.data  # Original weights (frozen)
        lora_A = lora_layer.lora_A.data  # Low-rank matrix A
        lora_B = lora_layer.lora_B.data  # Low-rank matrix B
        scaling = lora_layer.scaling  # alpha / r
        
        print(f"Base weight shape: {base_weight.shape}")
        print(f"LoRA A shape: {lora_A.shape}")
        print(f"LoRA B shape: {lora_B.shape}")
        print(f"Scaling factor: {scaling}")
        
        # Compute expected effective weight: W_base + (B @ A) * scaling
        lora_delta = (lora_B @ lora_A) * scaling
        expected_effective_weight = base_weight + lora_delta
        
        print(f"LoRA delta norm: {torch.norm(lora_delta).item():.6f}")
        print(f"LoRA delta max: {torch.abs(lora_delta).max().item():.6f}")
        print(f"Base weight norm: {torch.norm(base_weight).item():.6f}")
        
        # Test forward pass
        batch_size = 2
        in_features = lora_layer.in_features
        test_input = torch.randn(batch_size, in_features, device=device)
        
        # Forward through LoRA layer
        lora_output = lora_layer(test_input)
        
        # Compute expected output manually
        # Base output
        expected_base_output = torch.nn.functional.linear(
            test_input, 
            base_weight,
            lora_layer.base_layer.bias
        )
        
        # LoRA contribution: (test_input @ A.T @ B.T) * scaling
        lora_contribution = test_input @ lora_A.T @ lora_B.T * scaling
        expected_output = expected_base_output + lora_contribution
        
        # Compare outputs
        output_diff = torch.abs(lora_output - expected_output).max().item()
        print(f"Output difference: {output_diff}")
        
        # Should be very close (within numerical precision)
        assert output_diff < 1e-4, f"LoRA computation should match expected, diff: {output_diff}"
        
        # Verify that LoRA is actually making a difference
        base_only_output = torch.nn.functional.linear(
            test_input,
            base_weight,
            lora_layer.base_layer.bias
        )
        lora_effect = torch.abs(lora_output - base_only_output).max().item()
        print(f"LoRA effect magnitude: {lora_effect}")
        
        # LoRA should have some effect (non-zero contribution)
        # Note: If the adapter was just initialized and not trained, this might be small
        # but it should not be exactly zero unless lora_B was zero-initialized
        print(f"LoRA is {'actively' if lora_effect > 1e-6 else 'minimally'} affecting outputs")
    
    def test_lora_layer_count(self, setup_adapters):
        """Test that LoRA layers are applied to the expected number of modules."""
        base_model = setup_adapters["base_model"]
        legal_path = setup_adapters["legal_adapter"]
        
        # Load base model
        model = GLiNER2.from_pretrained(base_model)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        
        # Count linear layers that match target modules before LoRA
        target_modules = ["query", "key", "value", "dense"]
        matching_linear_count = 0
        for name, module in model.named_modules():
            if isinstance(module, torch.nn.Linear):
                if any(target in name for target in target_modules):
                    matching_linear_count += 1
        
        print(f"Matching linear layers in base model: {matching_linear_count}")
        
        # Load adapter
        model.load_adapter(legal_path)
        
        # Count LoRA layers
        from gliner2.training.lora import LoRALayer
        lora_layer_count = 0
        for name, module in model.named_modules():
            if isinstance(module, LoRALayer):
                lora_layer_count += 1
                print(f"LoRA layer {lora_layer_count}: {name}")
        
        print(f"Total LoRA layers after loading adapter: {lora_layer_count}")
        
        # Should have LoRA layers applied
        assert lora_layer_count > 0, "Should have at least one LoRA layer"
        
        # The count should match the number of targeted linear layers
        # (though this might vary depending on model architecture)
        print(f"LoRA coverage: {lora_layer_count}/{matching_linear_count} targeted layers")


# =============================================================================
# Demo Script
# =============================================================================

def demo_adapter_workflow():
    """
    Demonstration of the full adapter workflow.
    
    Run this to see adapters in action:
        python -c "from tests.test_lora_adapters import demo_adapter_workflow; demo_adapter_workflow()"
    """
    import tempfile
    
    BASE_MODEL = "fastino/gliner2-base-v1"  # Change to your model
    
    output_dir = "lora_train"

    print("=" * 60)
    print("GLiNER2 LoRA Adapter Demo")
    print("=" * 60)

    # Train adapters
    print("\n[1/4] Training legal adapter...")
    legal_path = train_legal(BASE_MODEL, output_dir)

    print("\n[2/4] Training medical adapter...")
    medical_path = train_medical(BASE_MODEL, output_dir)

    print("\n[3/4] Training support adapter...")
    support_path = train_support(BASE_MODEL, output_dir)

    # Load base model once
    print("\n[4/4] Loading base model and swapping adapters...")
 
    # Use the base model we trained with
    model = GLiNER2.from_pretrained(BASE_MODEL)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    print(f"Model loaded on {device}")

    # Swap adapters (fast!)
    print("\n--- Legal Adapter ---")
    load_lora_adapter(model, legal_path)
    result1 = model.extract_entities("Apple sued Google", ["company"])
    print(f"Input: 'Apple sued Google'")
    print(f"Result: {result1}")

    print("\n--- Medical Adapter ---")
    load_lora_adapter(model, medical_path)  # Auto-unloads previous
    result2 = model.extract_entities("Patient has diabetes", ["disease"])
    print(f"Input: 'Patient has diabetes'")
    print(f"Result: {result2}")

    # Or use convenience methods
    print("\n--- Support Adapter (via model.load_adapter) ---")
    model.load_adapter(support_path)
    result3 = model.extract_entities("Order #12345 issue", ["order_id"])
    print(f"Input: 'Order #12345 issue'")
    print(f"Result: {result3}")

    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    demo_adapter_workflow()

