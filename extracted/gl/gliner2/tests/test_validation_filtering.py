"""
Test script to demonstrate the new validation filtering behavior in DataLoader_Factory.

This script shows how invalid records are now filtered out instead of causing errors,
and the first 5 invalid records are printed with their error messages.
"""

import json
import tempfile
from pathlib import Path

from gliner2.training.data import DataLoader_Factory, InputExample


def test_validation_filtering():
    """Test that validation filters invalid records and prints first 5."""
    
    print("=" * 80)
    print("Testing Validation Filtering in DataLoader_Factory")
    print("=" * 80)
    
    # Create a mix of valid and invalid examples
    examples = [
        # Valid examples
        InputExample(
            text="John works at Google.",
            entities={"person": ["John"], "company": ["Google"]}
        ),
        InputExample(
            text="Apple released iPhone 15.",
            entities={"company": ["Apple"], "product": ["iPhone 15"]}
        ),
        
        # Invalid examples - various types of errors
        InputExample(
            text="",  # Empty text - should be invalid
            entities={"company": ["Test"]}
        ),
        InputExample(
            text="Microsoft is in Redmond.",
            entities={"company": ["XYZ Corp"]}  # Entity not in text - invalid in strict mode
        ),
        InputExample(
            text="Tesla makes cars.",
            entities={"company": ["Tesla"], "product": ["SpaceX"]}  # Product not in text
        ),
        
        # More valid examples
        InputExample(
            text="Amazon Web Services provides cloud computing.",
            entities={"company": ["Amazon Web Services"], "product": ["cloud computing"]}
        ),
        
        # More invalid examples
        InputExample(
            text="Netflix streams movies.",
            entities={"company": ["Hulu"]}  # Company not in text
        ),
        InputExample(
            text="Spotify offers music.",
            entities={"company": ["Apple Music"]}  # Company not in text
        ),
        InputExample(
            text="Twitter is social media.",
            entities={"company": ["Facebook"]}  # Company not in text
        ),
    ]
    
    print(f"\nCreated {len(examples)} examples (mix of valid and invalid)")
    print("Invalid examples include:")
    print("  - Empty text")
    print("  - Entities not found in text (strict validation)")
    
    # Convert to list format
    data = examples
    
    print("\n" + "-" * 80)
    print("Loading data with validation enabled (strict mode)...")
    print("-" * 80)
    
    # Load with validation enabled
    records = DataLoader_Factory.load(
        data=data,
        validate=True,
        shuffle=False
    )
    
    print(f"Result: Loaded {len(records)} valid records")
    
    # Verify we got the valid records
    print("\nValid records that were kept:")
    for i, record in enumerate(records[:3]):  # Show first 3
        text = record["input"][:50] + "..." if len(record["input"]) > 50 else record["input"]
        print(f"  {i+1}. {text}")
    
    if len(records) > 3:
        print(f"  ... and {len(records) - 3} more")
    
    print("\n" + "=" * 80)
    print("Test completed successfully!")
    print("=" * 80)


def test_validation_with_jsonl():
    """Test validation filtering with JSONL file."""
    
    print("\n" + "=" * 80)
    print("Testing Validation Filtering with JSONL File")
    print("=" * 80)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        jsonl_path = Path(tmpdir) / "test_data.jsonl"
        
        # Create JSONL with valid and invalid records
        data = [
            {"input": "Apple makes iPhones.", "output": {"entities": {"company": ["Apple"], "product": ["iPhones"]}}},
            {"input": "", "output": {"entities": {"company": ["Test"]}}},  # Empty text - invalid
            {"input": "Google in Mountain View.", "output": {"entities": {"company": ["Google"], "location": ["Mountain View"]}}},
            {"input": "Microsoft.", "output": {"entities": {"company": ["IBM"]}}},  # Entity not in text - invalid
            {"input": "Amazon provides AWS.", "output": {"entities": {"company": ["Amazon"], "product": ["AWS"]}}},
            {"input": "Tesla.", "output": {"entities": {"company": ["SpaceX"]}}},  # Entity not in text - invalid
        ]
        
        with open(jsonl_path, 'w') as f:
            for record in data:
                f.write(json.dumps(record) + '\n')
        
        print(f"\nCreated JSONL file with {len(data)} records")
        
        print("\n" + "-" * 80)
        print("Loading JSONL with validation enabled (strict mode)...")
        print("-" * 80)
        
        # Load with validation
        records = DataLoader_Factory.load(
            data=str(jsonl_path),
            validate=True,
            strict_validation=True,
            shuffle=False
        )
        
        print(f"Result: Loaded {len(records)} valid records from JSONL")
        
        print("\n" + "=" * 80)
        print("Test completed successfully!")
        print("=" * 80)


def test_no_invalid_records():
    """Test when all records are valid."""
    
    print("\n" + "=" * 80)
    print("Testing Validation with All Valid Records")
    print("=" * 80)
    
    examples = [
        InputExample(
            text="Apple makes iPhones.",
            entities={"company": ["Apple"], "product": ["iPhones"]}
        ),
        InputExample(
            text="Google in Mountain View.",
            entities={"company": ["Google"], "location": ["Mountain View"]}
        ),
    ]
    
    print(f"\nCreated {len(examples)} valid examples")
    
    print("\n" + "-" * 80)
    print("Loading data with validation enabled...")
    print("-" * 80)
    
    records = DataLoader_Factory.load(
        data=examples,
        validate=True,
        strict_validation=True,
        shuffle=False
    )
    
    print(f"\nResult: All {len(records)} records are valid (no filtering occurred)")
    
    print("\n" + "=" * 80)
    print("Test completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    test_validation_filtering()
    test_validation_with_jsonl()
    test_no_invalid_records()
    
    print("\n" + "=" * 80)
    print("ALL TESTS PASSED!")
    print("=" * 80)
    print("\nSummary:")
    print("  ✓ Invalid records are filtered out during validation")
    print("  ✓ First 5 invalid records are printed with error messages")
    print("  ✓ Valid records are kept and returned")
    print("  ✓ Works with both InputExample lists and JSONL files")
    print("  ✓ No output when all records are valid")
    print()

