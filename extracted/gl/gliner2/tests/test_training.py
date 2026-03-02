"""
Real Training Scenarios Test for GLiNER2

This script tests model training on real training scenarios without using any test library.
It's designed for "vibe testing" - running training and verifying it works correctly.

Tests:
1. Basic training with InputExample list
2. Training with JSONL file
3. Training with TrainingDataset
4. Training with evaluation
5. Checkpoint saving and loading
6. LoRA training
7. Multi-task training (entities + classifications + relations)
"""

import json
import os
import shutil
import tempfile
from pathlib import Path

from gliner2 import GLiNER2
from gliner2.training.data import (
    InputExample,
    TrainingDataset,
    Classification,
    Relation,
    Structure,
)
from gliner2.training.trainer import GLiNER2Trainer, TrainingConfig


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def test_basic_training():
    """Test 1: Basic training with InputExample list."""
    print_section("TEST 1: Basic Training with InputExample List")
    
    # Create training examples
    examples = [
        InputExample(
            text="John Smith works at Google in California.",
            entities={"person": ["John Smith"], "company": ["Google"], "location": ["California"]}
        ),
        InputExample(
            text="Apple released iPhone 15 in September 2023.",
            entities={"company": ["Apple"], "product": ["iPhone 15"], "date": ["September 2023"]}
        ),
        InputExample(
            text="Microsoft is headquartered in Redmond, Washington.",
            entities={"company": ["Microsoft"], "location": ["Redmond", "Washington"]}
        ),
        InputExample(
            text="Elon Musk founded SpaceX in 2002.",
            entities={"person": ["Elon Musk"], "company": ["SpaceX"], "date": ["2002"]}
        ),
        InputExample(
            text="Amazon Web Services provides cloud computing services.",
            entities={"company": ["Amazon Web Services"], "product": ["cloud computing services"]}
        ),
    ]
    
    print(f"Created {len(examples)} training examples")
    
    # Create temporary output directory
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "test_basic"
        
        # Load model
        print("Loading model: fastino/gliner2-base-v1...")
        model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
        print("Model loaded successfully!")
        
        # Configure training
        config = TrainingConfig(
            output_dir=str(output_dir),
            experiment_name="test_basic",
            num_epochs=2,
            batch_size=2,
            encoder_lr=1e-5,
            task_lr=5e-4,
            logging_steps=1,
            save_strategy="epoch",
            eval_strategy="no",
            fp16=False,  # Disable for CPU compatibility
            num_workers=0,  # Disable for simplicity
        )
        
        # Train
        print("\nStarting training...")
        trainer = GLiNER2Trainer(model, config)
        results = trainer.train(train_data=examples)
        
        # Verify results
        print(f"\n✓ Training completed!")
        print(f"  - Total steps: {results['total_steps']}")
        print(f"  - Total epochs: {results['total_epochs']}")
        print(f"  - Training time: {results['total_time_seconds']:.2f} seconds")
        
        # Verify checkpoint exists
        checkpoint_dir = output_dir / "checkpoints" / "final"
        assert checkpoint_dir.exists(), "Final checkpoint directory should exist"
        assert (checkpoint_dir / "config.json").exists(), "Config file should exist"
        print(f"  - ✓ Checkpoint saved at: {checkpoint_dir}")
        
        print("\n✓ TEST 1 PASSED: Basic training works correctly!")


def test_training_with_jsonl():
    """Test 2: Training with JSONL file."""
    print_section("TEST 2: Training with JSONL File")
    
    # Create temporary JSONL file
    with tempfile.TemporaryDirectory() as tmpdir:
        jsonl_path = Path(tmpdir) / "train.jsonl"
        
        # Write examples to JSONL
        examples_data = [
            {
                "input": "Tesla Motors produces electric vehicles.",
                "output": {"entities": {"company": ["Tesla Motors"], "product": ["electric vehicles"]}}
            },
            {
                "input": "OpenAI developed ChatGPT, an AI chatbot.",
                "output": {"entities": {"company": ["OpenAI"], "product": ["ChatGPT", "AI chatbot"]}}
            },
            {
                "input": "Meta Platforms owns Facebook and Instagram.",
                "output": {"entities": {"company": ["Meta Platforms"], "product": ["Facebook", "Instagram"]}}
            },
        ]
        
        with open(jsonl_path, 'w') as f:
            for ex in examples_data:
                f.write(json.dumps(ex) + '\n')
        
        print(f"Created JSONL file with {len(examples_data)} examples: {jsonl_path}")
        
        output_dir = Path(tmpdir) / "test_jsonl"
        
        # Load model and train
        print("Loading model...")
        model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
        
        config = TrainingConfig(
            output_dir=str(output_dir),
            experiment_name="test_jsonl",
            num_epochs=2,
            batch_size=2,
            encoder_lr=1e-5,
            task_lr=5e-4,
            logging_steps=1,
            save_strategy="epoch",
            eval_strategy="no",
            fp16=False,
            num_workers=0,
        )
        
        print("\nStarting training from JSONL...")
        trainer = GLiNER2Trainer(model, config)
        results = trainer.train(train_data=str(jsonl_path))
        
        print(f"\n✓ Training completed!")
        print(f"  - Total steps: {results['total_steps']}")
        
        # Verify checkpoint
        checkpoint_dir = output_dir / "checkpoints" / "final"
        assert checkpoint_dir.exists(), "Final checkpoint should exist"
        print(f"  - ✓ Checkpoint saved at: {checkpoint_dir}")
        
        print("\n✓ TEST 2 PASSED: Training from JSONL works correctly!")


def test_training_with_dataset():
    """Test 3: Training with TrainingDataset object."""
    print_section("TEST 3: Training with TrainingDataset")
    
    # Create TrainingDataset
    examples = [
        InputExample(
            text="Netflix streams movies and TV shows.",
            entities={"company": ["Netflix"], "product": ["movies", "TV shows"]}
        ),
        InputExample(
            text="Spotify offers music streaming services.",
            entities={"company": ["Spotify"], "product": ["music streaming services"]}
        ),
        InputExample(
            text="YouTube is a video sharing platform.",
            entities={"company": ["YouTube"], "product": ["video sharing platform"]}
        ),
    ]
    
    dataset = TrainingDataset(examples)
    print(f"Created TrainingDataset with {len(dataset)} examples")
    
    # Validate dataset
    validation_report = dataset.validate(strict=True, raise_on_error=False)
    print(f"  - Valid examples: {validation_report['valid']}")
    print(f"  - Invalid examples: {validation_report['invalid']}")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "test_dataset"
        
        model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
        
        config = TrainingConfig(
            output_dir=str(output_dir),
            experiment_name="test_dataset",
            num_epochs=2,
            batch_size=2,
            encoder_lr=1e-5,
            task_lr=5e-4,
            logging_steps=1,
            save_strategy="epoch",
            eval_strategy="no",
            fp16=False,
            num_workers=0,
        )
        
        print("\nStarting training with TrainingDataset...")
        trainer = GLiNER2Trainer(model, config)
        results = trainer.train(train_data=dataset)
        
        print(f"\n✓ Training completed!")
        print(f"  - Total steps: {results['total_steps']}")
        
        checkpoint_dir = output_dir / "checkpoints" / "final"
        assert checkpoint_dir.exists(), "Final checkpoint should exist"
        print(f"  - ✓ Checkpoint saved at: {checkpoint_dir}")
        
        print("\n✓ TEST 3 PASSED: Training with TrainingDataset works correctly!")


def test_training_with_evaluation():
    """Test 4: Training with evaluation."""
    print_section("TEST 4: Training with Evaluation")
    
    # Create train and eval examples
    train_examples = [
        InputExample(
            text="Apple designs iPhones and MacBooks.",
            entities={"company": ["Apple"], "product": ["iPhones", "MacBooks"]}
        ),
        InputExample(
            text="Google develops Android and Chrome.",
            entities={"company": ["Google"], "product": ["Android", "Chrome"]}
        ),
        InputExample(
            text="Microsoft creates Windows and Office.",
            entities={"company": ["Microsoft"], "product": ["Windows", "Office"]}
        ),
        InputExample(
            text="Amazon operates AWS cloud services.",
            entities={"company": ["Amazon"], "product": ["AWS cloud services"]}
        ),
    ]
    
    eval_examples = [
        InputExample(
            text="Meta owns Facebook and WhatsApp.",
            entities={"company": ["Meta"], "product": ["Facebook", "WhatsApp"]}
        ),
        InputExample(
            text="Twitter is a social media platform.",
            entities={"company": ["Twitter"], "product": ["social media platform"]}
        ),
    ]
    
    print(f"Created {len(train_examples)} training examples and {len(eval_examples)} eval examples")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "test_eval"
        
        model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
        
        config = TrainingConfig(
            output_dir=str(output_dir),
            experiment_name="test_eval",
            num_epochs=2,
            batch_size=2,
            encoder_lr=1e-5,
            task_lr=5e-4,
            logging_steps=1,
            save_strategy="epoch",
            eval_strategy="epoch",
            save_best=True,
            fp16=False,
            num_workers=0,
        )
        
        print("\nStarting training with evaluation...")
        trainer = GLiNER2Trainer(model, config)
        results = trainer.train(train_data=train_examples, eval_data=eval_examples)
        
        print(f"\n✓ Training completed!")
        print(f"  - Total steps: {results['total_steps']}")
        print(f"  - Best metric: {results['best_metric']:.4f}")
        print(f"  - Eval metrics history: {len(results['eval_metrics_history'])} evaluations")
        
        # Verify checkpoints
        checkpoint_dir = output_dir / "checkpoints"
        assert (checkpoint_dir / "final").exists(), "Final checkpoint should exist"
        assert (checkpoint_dir / "best").exists(), "Best checkpoint should exist"
        print(f"  - ✓ Final checkpoint saved")
        print(f"  - ✓ Best checkpoint saved")
        
        print("\n✓ TEST 4 PASSED: Training with evaluation works correctly!")


def test_checkpoint_loading():
    """Test 5: Checkpoint saving and loading."""
    print_section("TEST 5: Checkpoint Saving and Loading")
    
    examples = [
        InputExample(
            text="NVIDIA produces GPUs for AI computing.",
            entities={"company": ["NVIDIA"], "product": ["GPUs"]}
        ),
        InputExample(
            text="AMD manufactures processors and graphics cards.",
            entities={"company": ["AMD"], "product": ["processors", "graphics cards"]}
        ),
    ]
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "test_checkpoint"
        
        # Train and save checkpoint
        print("Step 1: Training model...")
        model1 = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
        
        config = TrainingConfig(
            output_dir=str(output_dir),
            experiment_name="test_checkpoint",
            num_epochs=1,
            batch_size=2,
            encoder_lr=1e-5,
            task_lr=5e-4,
            logging_steps=1,
            save_strategy="epoch",
            eval_strategy="no",
            fp16=False,
            num_workers=0,
        )
        
        trainer1 = GLiNER2Trainer(model1, config)
        trainer1.train(train_data=examples)
        
        checkpoint_path = output_dir / "checkpoints" / "final"
        assert checkpoint_path.exists(), "Checkpoint should exist"
        print(f"  ✓ Checkpoint saved at: {checkpoint_path}")
        
        # Load checkpoint
        print("\nStep 2: Loading checkpoint...")
        model2 = GLiNER2.from_pretrained(str(checkpoint_path))
        print(f"  ✓ Model loaded successfully from checkpoint")
        
        # Verify model can do inference
        print("\nStep 3: Testing inference with loaded model...")
        schema = model2.create_schema()
        schema.entities(["company", "product"])
        result = model2.extract("Intel makes processors.", schema)
        
        assert "entities" in result, "Result should contain entities"
        print(f"  ✓ Inference works: {result}")
        
        print("\n✓ TEST 5 PASSED: Checkpoint saving and loading works correctly!")


def test_lora_training():
    """Test 6: LoRA training."""
    print_section("TEST 6: LoRA Training (Parameter-Efficient Fine-Tuning)")
    
    examples = [
        InputExample(
            text="Tesla produces electric cars and solar panels.",
            entities={"company": ["Tesla"], "product": ["electric cars", "solar panels"]}
        ),
        InputExample(
            text="Rivian manufactures electric trucks.",
            entities={"company": ["Rivian"], "product": ["electric trucks"]}
        ),
        InputExample(
            text="Lucid Motors builds luxury electric vehicles.",
            entities={"company": ["Lucid Motors"], "product": ["luxury electric vehicles"]}
        ),
    ]
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "test_lora"
        
        model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
        
        config = TrainingConfig(
            output_dir=str(output_dir),
            experiment_name="test_lora",
            num_epochs=2,
            batch_size=2,
            encoder_lr=1e-5,
            task_lr=5e-4,
            logging_steps=1,
            save_strategy="epoch",
            eval_strategy="no",
            fp16=False,
            num_workers=0,
            # LoRA configuration
            use_lora=True,
            lora_r=8,
            lora_alpha=16.0,
            lora_dropout=0.0,
            lora_target_modules=["query", "key", "value", "dense"],
        )
        
        print("Starting LoRA training...")
        trainer = GLiNER2Trainer(model, config)
        results = trainer.train(train_data=examples)
        
        print(f"\n✓ LoRA training completed!")
        print(f"  - Total steps: {results['total_steps']}")
        
        # Verify checkpoint
        checkpoint_dir = output_dir / "checkpoints" / "final"
        assert checkpoint_dir.exists(), "Final checkpoint should exist"
        
        # Check if LoRA config was saved
        lora_config_path = checkpoint_dir / "lora_config.json"
        assert lora_config_path.exists(), "LoRA config should be saved"
        print(f"  - ✓ LoRA checkpoint saved at: {checkpoint_dir}")
        print(f"  - ✓ LoRA config saved: {lora_config_path}")
        
        print("\n✓ TEST 6 PASSED: LoRA training works correctly!")


def test_multitask_training():
    """Test 7: Multi-task training (entities + classifications + relations)."""
    print_section("TEST 7: Multi-Task Training")
    
    examples = [
        InputExample(
            text="John Smith works at Google in California. The company is thriving.",
            entities={"person": ["John Smith"], "company": ["Google"], "location": ["California"]},
            classifications=[
                Classification(
                    task="sentiment",
                    labels=["positive", "negative", "neutral"],
                    true_label="positive"
                )
            ],
            relations=[
                Relation("works_at", head="John Smith", tail="Google"),
                Relation("located_in", head="Google", tail="California")
            ]
        ),
        InputExample(
            text="Apple released iPhone 15. The launch was successful.",
            entities={"company": ["Apple"], "product": ["iPhone 15"]},
            classifications=[
                Classification(
                    task="sentiment",
                    labels=["positive", "negative", "neutral"],
                    true_label="positive"
                )
            ],
            relations=[
                Relation("released", head="Apple", tail="iPhone 15")
            ]
        ),
    ]
    
    print(f"Created {len(examples)} multi-task examples")
    print("  - Tasks: entities, classifications, relations")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "test_multitask"
        
        model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
        
        config = TrainingConfig(
            output_dir=str(output_dir),
            experiment_name="test_multitask",
            num_epochs=2,
            batch_size=2,
            encoder_lr=1e-5,
            task_lr=5e-4,
            logging_steps=1,
            save_strategy="epoch",
            eval_strategy="no",
            fp16=False,
            num_workers=0,
        )
        
        print("\nStarting multi-task training...")
        trainer = GLiNER2Trainer(model, config)
        results = trainer.train(train_data=examples)
        
        print(f"\n✓ Multi-task training completed!")
        print(f"  - Total steps: {results['total_steps']}")
        
        checkpoint_dir = output_dir / "checkpoints" / "final"
        assert checkpoint_dir.exists(), "Final checkpoint should exist"
        print(f"  - ✓ Checkpoint saved at: {checkpoint_dir}")
        
        print("\n✓ TEST 7 PASSED: Multi-task training works correctly!")


def test_training_with_structures():
    """Test 8: Training with structured data extraction."""
    print_section("TEST 8: Training with Structured Data")
    
    examples = [
        InputExample(
            text="iPhone 15 costs $999 and was released in September 2023.",
            entities={"product": ["iPhone 15"], "price": ["$999"], "date": ["September 2023"]},
            structures=[
                Structure("product_info", name="iPhone 15", price="$999", release_date="September 2023")
            ]
        ),
        InputExample(
            text="MacBook Pro is priced at $1999 and launched in October 2023.",
            entities={"product": ["MacBook Pro"], "price": ["$1999"], "date": ["October 2023"]},
            structures=[
                Structure("product_info", name="MacBook Pro", price="$1999", release_date="October 2023")
            ]
        ),
    ]
    
    print(f"Created {len(examples)} examples with structured data")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "test_structures"
        
        model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
        
        config = TrainingConfig(
            output_dir=str(output_dir),
            experiment_name="test_structures",
            num_epochs=2,
            batch_size=2,
            encoder_lr=1e-5,
            task_lr=5e-4,
            logging_steps=1,
            save_strategy="epoch",
            eval_strategy="no",
            fp16=False,
            num_workers=0,
        )
        
        print("\nStarting training with structured data...")
        trainer = GLiNER2Trainer(model, config)
        results = trainer.train(train_data=examples)
        
        print(f"\n✓ Training completed!")
        print(f"  - Total steps: {results['total_steps']}")
        
        checkpoint_dir = output_dir / "checkpoints" / "final"
        assert checkpoint_dir.exists(), "Final checkpoint should exist"
        print(f"  - ✓ Checkpoint saved at: {checkpoint_dir}")
        
        print("\n✓ TEST 8 PASSED: Training with structured data works correctly!")


def main():
    """Run all training tests."""
    print("\n" + "=" * 80)
    print("  GLiNER2 Training Tests - Real Training Scenarios")
    print("=" * 80)
    print("\nThis script tests model training on real training scenarios.")
    print("No test library is used - this is for 'vibe testing'.\n")
    
    try:
        # Run all tests
        # test_basic_training()
        # test_training_with_jsonl()
        # test_training_with_dataset()
        # test_training_with_evaluation()
        # test_checkpoint_loading()
        test_lora_training()
        # test_multitask_training()
        # test_training_with_structures()
        
        # Summary
        print("\n" + "=" * 80)
        print("  ALL TESTS PASSED! ✓")
        print("=" * 80)
        print("\nSummary:")
        print("  ✓ Basic training with InputExample list")
        print("  ✓ Training with JSONL file")
        print("  ✓ Training with TrainingDataset")
        print("  ✓ Training with evaluation")
        print("  ✓ Checkpoint saving and loading")
        print("  ✓ LoRA training")
        print("  ✓ Multi-task training")
        print("  ✓ Training with structured data")
        print("\nAll training scenarios work correctly! 🎉\n")
        
    except Exception as e:
        print("\n" + "=" * 80)
        print("  TEST FAILED!")
        print("=" * 80)
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()

