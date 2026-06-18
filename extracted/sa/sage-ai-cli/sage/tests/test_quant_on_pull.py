"""Unit and integration tests for quant_on_pull.py."""

from __future__ import annotations

from pathlib import Path
import pytest

from sage.core.quant_on_pull import plan_quantizations, should_requantize


# ==========================================
# UNIT TESTS
# ==========================================

def test_plan_quantizations_missing_all(tmp_path):
    """Test planning when all desired quants are missing."""
    model_path = tmp_path / "model.gguf"
    plan = plan_quantizations(model_path, available_quants=[])
    assert "Q5_K_M" in plan
    assert "Q8_0" in plan
    assert len(plan) == 2


def test_plan_quantizations_missing_some(tmp_path):
    """Test planning when only some desired quants are available."""
    model_path = tmp_path / "model.gguf"
    plan = plan_quantizations(model_path, available_quants=["Q8_0", "Q4_K_S"])
    assert "Q5_K_M" in plan
    assert "Q8_0" not in plan
    assert plan == ["Q5_K_M"]


def test_plan_quantizations_none_missing(tmp_path):
    """Test planning when all desired quants are available."""
    model_path = tmp_path / "model.gguf"
    plan = plan_quantizations(model_path, available_quants=["Q5_K_M", "Q8_0", "Q4_0"])
    assert plan == []


def test_should_requantize_true(tmp_path):
    """Test should_requantize returns True if quants are missing."""
    model_path = tmp_path / "model.gguf"
    assert should_requantize(model_path, available_quants=["Q8_0"]) is True


def test_should_requantize_false(tmp_path):
    """Test should_requantize returns False if all quants are present."""
    model_path = tmp_path / "model.gguf"
    assert should_requantize(model_path, available_quants=["Q5_K_M", "Q8_0"]) is False


# ==========================================
# INTEGRATION TESTS
# ==========================================

class MockModelRegistry:
    """Mock repository manager simulating a model download and quantization registry."""
    def __init__(self, model_name: str, base_dir: Path):
        self.model_name = model_name
        self.base_dir = base_dir
        self.model_dir = base_dir / model_name
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.available_quants = []

    def get_model_path(self) -> Path:
        return self.model_dir / f"{self.model_name}.gguf"

    def pull_model(self):
        # Simulate initial model pull, bringing base model and maybe some initial low quants
        gguf_file = self.get_model_path()
        gguf_file.write_text("dummy model content")
        self.available_quants.append("Q4_0")

    def sync_quantizations(self):
        model_path = self.get_model_path()
        if should_requantize(model_path, available_quants=self.available_quants):
            needed = plan_quantizations(model_path, available_quants=self.available_quants)
            for quant in needed:
                # Simulate running a quantization command
                quant_file = self.model_dir / f"{self.model_name}.{quant}.gguf"
                quant_file.write_text(f"dummy quant {quant} content")
                self.available_quants.append(quant)


def test_integration_model_pull_and_quantize_flow(tmp_path):
    """Integration test checking the model pull, checking requantize, planning, and executing."""
    registry = MockModelRegistry("phi-3", tmp_path)
    
    # 1. Pull model
    registry.pull_model()
    model_path = registry.get_model_path()
    assert model_path.exists()
    assert registry.available_quants == ["Q4_0"]

    # 2. Check if we need to requantize
    assert should_requantize(model_path, available_quants=registry.available_quants) is True
    plan = plan_quantizations(model_path, available_quants=registry.available_quants)
    assert plan == ["Q5_K_M", "Q8_0"]

    # 3. Perform sync/quantization
    registry.sync_quantizations()

    # 4. Verify that we no longer need to requantize and files are created
    assert should_requantize(model_path, available_quants=registry.available_quants) is False
    assert (registry.model_dir / "phi-3.Q5_K_M.gguf").exists()
    assert (registry.model_dir / "phi-3.Q8_0.gguf").exists()
    assert set(registry.available_quants) == {"Q4_0", "Q5_K_M", "Q8_0"}
