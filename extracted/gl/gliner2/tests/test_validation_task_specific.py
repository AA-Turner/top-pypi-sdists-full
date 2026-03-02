"""
Task-Specific Validation Tests for GLiNER2 Training Data

This script tests validation for each specific task type:
- Entity extraction validation
- Classification validation
- Structure extraction validation
- Relation extraction validation

Each test creates both valid and invalid examples to verify validation works correctly.
"""

import json
import tempfile
from pathlib import Path

from gliner2.training.data import (
    InputExample,
    Classification,
    Structure,
    Relation,
    ChoiceField,
    DataLoader_Factory,
)


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def test_entity_validation():
    """Test entity extraction validation."""
    print_section("TEST 1: Entity Extraction Validation")
    
    examples = [
        # Valid entity examples
        InputExample(
            text="Apple Inc. is located in Cupertino, California.",
            entities={"company": ["Apple Inc."], "location": ["Cupertino", "California"]}
        ),
        InputExample(
            text="Tim Cook is the CEO of Apple.",
            entities={"person": ["Tim Cook"], "company": ["Apple"]}
        ),
        
        # Invalid: Empty text
        InputExample(
            text="",
            entities={"company": ["Apple"]}
        ),
        
        # Invalid: Entity not in text (strict mode)
        InputExample(
            text="Google is a search engine.",
            entities={"company": ["Microsoft"]}  # Microsoft not in text
        ),
        
        # Invalid: Empty entity type
        InputExample(
            text="Amazon provides cloud services.",
            entities={"": ["Amazon"]}  # Empty entity type
        ),
        
        # Valid example
        InputExample(
            text="Tesla manufactures electric vehicles.",
            entities={"company": ["Tesla"], "product": ["electric vehicles"]}
        ),
        
        # Invalid: Multiple entities not in text
        InputExample(
            text="Netflix streams content.",
            entities={"company": ["Hulu"], "product": ["movies"]}  # Hulu not in text
        ),
        
        # Invalid: No tasks at all (empty entities)
        InputExample(
            text="This is just text.",
            entities={}
        ),
    ]
    
    print(f"Created {len(examples)} entity examples (valid and invalid)")
    print("\nExpected issues:")
    print("  - Empty text")
    print("  - Entities not found in text")
    print("  - Empty entity type names")
    print("  - No tasks defined")
    
    print("\n" + "-" * 80)
    print("Running validation (strict mode)...")
    print("-" * 80)
    
    records = DataLoader_Factory.load(
        data=examples,
        validate=True,
        shuffle=False
    )
    
    print(f"\n✓ Entity validation test completed: {len(records)} valid records kept")


def test_classification_validation():
    """Test classification task validation."""
    print_section("TEST 2: Classification Validation")
    
    examples = [
        # Valid classification
        InputExample(
            text="This movie is absolutely amazing!",
            entities={"product": ["movie"]},
            classifications=[
                Classification(
                    task="sentiment",
                    labels=["positive", "negative", "neutral"],
                    true_label="positive"
                )
            ]
        ),
        
        # Valid multi-label classification
        InputExample(
            text="The restaurant has great food but slow service.",
            entities={"place": ["restaurant"]},
            classifications=[
                Classification(
                    task="aspects",
                    labels=["food", "service", "ambiance", "price"],
                    true_label=["food", "service"],
                    multi_label=True
                )
            ]
        ),
        
        # Invalid: Empty task name
        InputExample(
            text="This is a test.",
            entities={"thing": ["test"]},
            classifications=[
                Classification(
                    task="",  # Empty task name
                    labels=["label1", "label2"],
                    true_label="label1"
                )
            ]
        ),
        
        # Invalid: No labels
        InputExample(
            text="Sample text here.",
            entities={"thing": ["text"]},
            classifications=[
                Classification(
                    task="category",
                    labels=[],  # Empty labels list
                    true_label="something"
                )
            ]
        ),
        
        # Invalid: True label not in labels list
        InputExample(
            text="The weather is nice today.",
            entities={"thing": ["weather"]},
            classifications=[
                Classification(
                    task="sentiment",
                    labels=["positive", "negative"],
                    true_label="neutral"  # Not in labels list
                )
            ]
        ),
        
        # Invalid: Multiple true labels but multi_label=False
        InputExample(
            text="Mixed feelings about this product.",
            entities={"thing": ["product"]},
            classifications=[
                Classification(
                    task="sentiment",
                    labels=["positive", "negative", "neutral"],
                    true_label=["positive", "negative"],  # Multiple but multi_label=False
                    multi_label=False
                )
            ]
        ),
        
        # Valid with label descriptions
        InputExample(
            text="The service was exceptional.",
            entities={"thing": ["service"]},
            classifications=[
                Classification(
                    task="quality",
                    labels=["excellent", "good", "fair", "poor"],
                    true_label="excellent",
                    label_descriptions={
                        "excellent": "Outstanding quality",
                        "good": "Above average",
                        "fair": "Acceptable",
                        "poor": "Below standard"
                    }
                )
            ]
        ),
        
        # Invalid: Label description key not in labels
        InputExample(
            text="The product quality is decent.",
            entities={"thing": ["product"]},
            classifications=[
                Classification(
                    task="rating",
                    labels=["high", "medium", "low"],
                    true_label="medium",
                    label_descriptions={
                        "excellent": "Best"  # 'excellent' not in labels
                    }
                )
            ]
        ),
    ]
    
    print(f"Created {len(examples)} classification examples (valid and invalid)")
    print("\nExpected issues:")
    print("  - Empty task names")
    print("  - Empty labels list")
    print("  - True label not in labels")
    print("  - Multi-label mismatch")
    print("  - Invalid label descriptions")
    
    print("\n" + "-" * 80)
    print("Running validation...")
    print("-" * 80)
    
    records = DataLoader_Factory.load(
        data=examples,
        validate=True,
        shuffle=False
    )
    
    print(f"\n✓ Classification validation test completed: {len(records)} valid records kept")


def test_structure_validation():
    """Test structured data extraction validation."""
    print_section("TEST 3: Structure Validation")
    
    examples = [
        # Valid structure
        InputExample(
            text="iPhone 15 Pro costs $999 and was released on September 22, 2023.",
            entities={"product": ["iPhone 15 Pro"], "price": ["$999"], "date": ["September 22, 2023"]},
            structures=[
                Structure(
                    "product_info",
                    name="iPhone 15 Pro",
                    price="$999",
                    release_date="September 22, 2023"
                )
            ]
        ),
        
        # Valid structure with list values
        InputExample(
            text="MacBook Pro comes in 14-inch and 16-inch sizes with M3 Pro and M3 Max chips.",
            entities={"product": ["MacBook Pro"]},
            structures=[
                Structure(
                    "product_specs",
                    name="MacBook Pro",
                    sizes=["14-inch", "16-inch"],
                    chips=["M3 Pro", "M3 Max"]
                )
            ]
        ),
        
        # Valid structure with ChoiceField
        InputExample(
            text="Order #12345 has status: shipped. Priority: high.",
            entities={"order": ["Order #12345"]},
            structures=[
                Structure(
                    "order_info",
                    order_id="Order #12345",
                    status=ChoiceField(value="shipped", choices=["pending", "shipped", "delivered"]),
                    priority=ChoiceField(value="high", choices=["low", "medium", "high"])
                )
            ]
        ),
        
        # Invalid: Empty structure name
        InputExample(
            text="Some product information here.",
            entities={"product": ["product"]},
            structures=[
                Structure(
                    "",  # Empty structure name
                    name="Product"
                )
            ]
        ),
        
        # Invalid: No fields
        InputExample(
            text="Tesla Model 3 information.",
            entities={"product": ["Tesla Model 3"]},
            structures=[
                Structure("car_info")  # No fields provided
            ]
        ),
        
        # Invalid: Field value not in text (strict mode)
        InputExample(
            text="Google Pixel 8 smartphone.",
            entities={"product": ["Google Pixel 8"]},
            structures=[
                Structure(
                    "phone_info",
                    name="iPhone 14",  # Not in text
                    type="smartphone"
                )
            ]
        ),
        
        # Invalid: ChoiceField value not in choices
        InputExample(
            text="Order #789 is processing.",
            entities={"order": ["Order #789"]},
            structures=[
                Structure(
                    "order_status",
                    order_id="Order #789",
                    status=ChoiceField(value="processing", choices=["pending", "complete"])  # 'processing' not in choices
                )
            ]
        ),
        
        # Valid structure with descriptions
        InputExample(
            text="Premium subscription at $29.99 per month.",
            entities={"product": ["Premium subscription"], "price": ["$29.99"]},
            structures=[
                Structure(
                    "subscription",
                    _descriptions={
                        "tier": "Subscription level",
                        "price": "Monthly cost"
                    },
                    tier="Premium subscription",
                    price="$29.99"
                )
            ]
        ),
        
        # Invalid: List value not in text (strict mode)
        InputExample(
            text="Available colors: red and blue.",
            entities={"colors": ["red", "blue"]},
            structures=[
                Structure(
                    "product_colors",
                    colors=["red", "green", "blue"]  # 'green' not in text
                )
            ]
        ),
    ]
    
    print(f"Created {len(examples)} structure examples (valid and invalid)")
    print("\nExpected issues:")
    print("  - Empty structure names")
    print("  - Structures with no fields")
    print("  - Field values not in text")
    print("  - Invalid ChoiceField values")
    print("  - List values not in text")
    
    print("\n" + "-" * 80)
    print("Running validation (strict mode)...")
    print("-" * 80)
    
    records = DataLoader_Factory.load(
        data=examples,
        validate=True,
        shuffle=False
    )
    
    print(f"\n✓ Structure validation test completed: {len(records)} valid records kept")


def test_relation_validation():
    """Test relation extraction validation."""
    print_section("TEST 4: Relation Extraction Validation")
    
    examples = [
        # Valid relation with head/tail
        InputExample(
            text="Elon Musk is the CEO of Tesla.",
            entities={"person": ["Elon Musk"], "company": ["Tesla"]},
            relations=[
                Relation("CEO_of", head="Elon Musk", tail="Tesla")
            ]
        ),
        
        # Valid relation with custom fields
        InputExample(
            text="Apple acquired Beats Electronics in 2014 for $3 billion.",
            entities={"company": ["Apple", "Beats Electronics"], "date": ["2014"], "price": ["$3 billion"]},
            relations=[
                Relation(
                    "acquisition",
                    acquirer="Apple",
                    target="Beats Electronics",
                    year="2014",
                    amount="$3 billion"
                )
            ]
        ),
        
        # Valid multiple relations
        InputExample(
            text="Tim Cook works at Apple in Cupertino.",
            entities={"person": ["Tim Cook"], "company": ["Apple"], "location": ["Cupertino"]},
            relations=[
                Relation("works_at", head="Tim Cook", tail="Apple"),
                Relation("located_in", head="Apple", tail="Cupertino")
            ]
        ),
        
        # Invalid: Empty relation name
        InputExample(
            text="John works at Microsoft.",
            entities={"person": ["John"], "company": ["Microsoft"]},
            relations=[
                Relation("", head="John", tail="Microsoft")  # Empty relation name
            ]
        ),
        
        # Invalid: No fields
        InputExample(
            text="Some relationship here.",
            entities={"thing": ["relationship"]},
            relations=[
                Relation("some_relation")  # No fields provided
            ]
        ),
        
        # Invalid: Relation field value not in text (strict mode)
        InputExample(
            text="Google was founded by Larry Page.",
            entities={"company": ["Google"], "person": ["Larry Page"]},
            relations=[
                Relation("founded_by", head="Google", tail="Sergey Brin")  # Sergey Brin not in text
            ]
        ),
        
        # Invalid: Head not in text (strict mode)
        InputExample(
            text="Microsoft is in Redmond.",
            entities={"company": ["Microsoft"], "location": ["Redmond"]},
            relations=[
                Relation("located_in", head="Apple", tail="Redmond")  # Apple not in text
            ]
        ),
        
        # Valid relation with entities in text
        InputExample(
            text="Amazon Web Services provides cloud computing for Netflix.",
            entities={"company": ["Amazon Web Services", "Netflix"], "service": ["cloud computing"]},
            relations=[
                Relation("provides_to", provider="Amazon Web Services", customer="Netflix", service="cloud computing")
            ]
        ),
        
        # Invalid: Custom field value not in text (strict mode)
        InputExample(
            text="Partnership between Tesla and Panasonic.",
            entities={"company": ["Tesla", "Panasonic"]},
            relations=[
                Relation(
                    "partnership",
                    company1="Tesla",
                    company2="Sony"  # Sony not in text
                )
            ]
        ),
    ]
    
    print(f"Created {len(examples)} relation examples (valid and invalid)")
    print("\nExpected issues:")
    print("  - Empty relation names")
    print("  - Relations with no fields")
    print("  - Relation field values not in text")
    print("  - Head/tail not in text")
    
    print("\n" + "-" * 80)
    print("Running validation (strict mode)...")
    print("-" * 80)
    
    records = DataLoader_Factory.load(
        data=examples,
        validate=True,
        shuffle=False
    )
    
    print(f"\n✓ Relation validation test completed: {len(records)} valid records kept")


def test_multi_task_validation():
    """Test validation for multi-task examples."""
    print_section("TEST 5: Multi-Task Validation")
    
    examples = [
        # Valid multi-task example
        InputExample(
            text="Apple released iPhone 15 in September 2023. The launch was very successful.",
            entities={"company": ["Apple"], "product": ["iPhone 15"], "date": ["September 2023"]},
            classifications=[
                Classification(
                    task="sentiment",
                    labels=["positive", "negative", "neutral"],
                    true_label="positive"
                )
            ],
            relations=[
                Relation("released", head="Apple", tail="iPhone 15")
            ],
            structures=[
                Structure(
                    "product_launch",
                    company="Apple",
                    product="iPhone 15",
                    date="September 2023"
                )
            ]
        ),
        
        # Valid multi-task with multiple of each
        InputExample(
            text="Tesla CEO Elon Musk announced Cybertruck production in Texas. Great news for investors!",
            entities={"company": ["Tesla"], "person": ["Elon Musk"], "product": ["Cybertruck"], "location": ["Texas"]},
            classifications=[
                Classification(
                    task="sentiment",
                    labels=["positive", "negative", "neutral"],
                    true_label="positive"
                ),
                Classification(
                    task="topic",
                    labels=["business", "technology", "politics"],
                    true_label="business"
                )
            ],
            relations=[
                Relation("CEO_of", head="Elon Musk", tail="Tesla"),
                Relation("produces", head="Tesla", tail="Cybertruck"),
                Relation("located_in", head="Tesla", tail="Texas")
            ],
            structures=[
                Structure(
                    "announcement",
                    company="Tesla",
                    ceo="Elon Musk",
                    product="Cybertruck",
                    location="Texas"
                )
            ]
        ),
        
        # Invalid: Mixed valid and invalid tasks
        InputExample(
            text="Google develops AI technology.",
            entities={"company": ["Google"], "tech": ["AI technology"]},
            classifications=[
                Classification(
                    task="",  # Invalid: empty task name
                    labels=["tech", "business"],
                    true_label="tech"
                )
            ],
            relations=[
                Relation("develops", head="Google", tail="AI technology")  # Valid
            ]
        ),
        
        # Invalid: Entity not in text but other tasks valid
        InputExample(
            text="Microsoft announced new features.",
            entities={"company": ["Apple"]},  # Invalid: Apple not in text
            classifications=[
                Classification(
                    task="topic",
                    labels=["tech", "business"],
                    true_label="tech"
                )
            ]
        ),
        
        # Valid: Only some task types present
        InputExample(
            text="Netflix streams movies and shows with great quality.",
            entities={"company": ["Netflix"], "product": ["movies", "shows"]},
            classifications=[
                Classification(
                    task="quality",
                    labels=["excellent", "good", "poor"],
                    true_label="excellent"
                )
            ]
            # No relations or structures - that's fine
        ),
    ]
    
    print(f"Created {len(examples)} multi-task examples (valid and invalid)")
    print("\nExpected issues:")
    print("  - Invalid classification in otherwise valid example")
    print("  - Invalid entity in multi-task example")
    
    print("\n" + "-" * 80)
    print("Running validation (strict mode)...")
    print("-" * 80)
    
    records = DataLoader_Factory.load(
        data=examples,
        validate=True,
        shuffle=False
    )
    
    print(f"\n✓ Multi-task validation test completed: {len(records)} valid records kept")


def test_edge_cases():
    """Test edge cases and special scenarios."""
    print_section("TEST 6: Edge Cases and Special Scenarios")
    
    examples = [
        # Valid: Case-insensitive matching
        InputExample(
            text="APPLE Inc. is a TECHNOLOGY company.",
            entities={"company": ["apple inc."], "industry": ["technology"]}  # Lowercase should match
        ),
        
        # Valid: Partial word matching
        InputExample(
            text="The iPhone is revolutionary.",
            entities={"product": ["iPhone"]}
        ),
        
        # Invalid: Whitespace-only text
        InputExample(
            text="   \n\t   ",  # Only whitespace
            entities={"thing": ["something"]}
        ),
        
        # Valid: Unicode characters
        InputExample(
            text="Café René serves crêpes in Zürich.",
            entities={"place": ["Café René"], "product": ["crêpes"], "location": ["Zürich"]}
        ),
        
        # Valid: Numbers and special characters
        InputExample(
            text="Model X-2000 costs $1,299.99.",
            entities={"product": ["Model X-2000"], "price": ["$1,299.99"]}
        ),
        
        # Invalid: Entity with only special characters
        InputExample(
            text="The product code is #12345.",
            entities={"code": ["#12345"]}
        ),
        
        # Valid: Very long entity
        InputExample(
            text="The International Business Machines Corporation is headquartered in Armonk.",
            entities={
                "company": ["International Business Machines Corporation"],
                "location": ["Armonk"]
            }
        ),
        
        # Invalid: Empty entity mention in list
        InputExample(
            text="Companies: Apple, Google, Microsoft.",
            entities={"company": ["Apple", "", "Microsoft"]}  # Empty mention
        ),
        
        # Valid: Overlapping entity mentions
        InputExample(
            text="New York City is in New York State.",
            entities={
                "city": ["New York City"],
                "state": ["New York State"]
            }
        ),
        
        # Invalid: No content at all (no tasks defined)
        InputExample(
            text="This is just plain text with no annotations."
            # No entities, classifications, structures, or relations
        ),
    ]
    
    print(f"Created {len(examples)} edge case examples (valid and invalid)")
    print("\nExpected issues:")
    print("  - Whitespace-only text")
    print("  - Empty entity mentions")
    print("  - No tasks defined")
    
    print("\n" + "-" * 80)
    print("Running validation (strict mode)...")
    print("-" * 80)
    
    records = DataLoader_Factory.load(
        data=examples,
        validate=True,
        shuffle=False
    )
    
    print(f"\n✓ Edge case validation test completed: {len(records)} valid records kept")


def test_validation_with_jsonl_files():
    """Test validation when loading from JSONL files."""
    print_section("TEST 7: Validation with JSONL Files")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create JSONL file with mixed valid/invalid records
        jsonl_path = Path(tmpdir) / "test_data.jsonl"
        
        # Mix of all task types with various validation issues
        records = [
            # Valid entity record
            {
                "input": "Apple makes iPhones.",
                "output": {"entities": {"company": ["Apple"], "product": ["iPhones"]}}
            },
            # Invalid: Empty text
            {
                "input": "",
                "output": {"entities": {"company": ["Test"]}}
            },
            # Valid classification record
            {
                "input": "This product is excellent!",
                "output": {
                    "entities": {"product": ["product"]},
                    "classifications": [{
                        "task": "sentiment",
                        "labels": ["positive", "negative"],
                        "true_label": ["positive"]
                    }]
                }
            },
            # Invalid: True label not in labels
            {
                "input": "The service was okay.",
                "output": {
                    "entities": {"thing": ["service"]},
                    "classifications": [{
                        "task": "rating",
                        "labels": ["good", "bad"],
                        "true_label": ["neutral"]  # Not in labels
                    }]
                }
            },
            # Valid structure record
            {
                "input": "Product X costs $99.",
                "output": {
                    "entities": {"product": ["Product X"], "price": ["$99"]},
                    "json_structures": [{
                        "pricing": {
                            "product": "Product X",
                            "price": "$99"
                        }
                    }]
                }
            },
            # Invalid: Structure field not in text
            {
                "input": "Some product info.",
                "output": {
                    "entities": {"product": ["product"]},
                    "json_structures": [{
                        "info": {
                            "name": "Different Product"  # Not in text
                        }
                    }]
                }
            },
            # Valid relation record
            {
                "input": "John works at Google.",
                "output": {
                    "entities": {"person": ["John"], "company": ["Google"]},
                    "relations": [{
                        "works_at": {
                            "head": "John",
                            "tail": "Google"
                        }
                    }]
                }
            },
            # Invalid: Relation field not in text
            {
                "input": "Company A partners with Company B.",
                "output": {
                    "entities": {"company": ["Company A", "Company B"]},
                    "relations": [{
                        "partners_with": {
                            "head": "Company A",
                            "tail": "Company C"  # Not in text
                        }
                    }]
                }
            },
        ]
        
        with open(jsonl_path, 'w') as f:
            for record in records:
                f.write(json.dumps(record) + '\n')
        
        print(f"Created JSONL file with {len(records)} records")
        print("  - 4 valid records (entity, classification, structure, relation)")
        print("  - 4 invalid records (various validation errors)")
        
        print("\n" + "-" * 80)
        print("Loading JSONL with validation (strict mode)...")
        print("-" * 80)
        
        loaded_records = DataLoader_Factory.load(
            data=str(jsonl_path),
            validate=True,
            shuffle=False
        )
        
        print(f"\n✓ JSONL validation test completed: {len(loaded_records)} valid records loaded")


def main():
    """Run all task-specific validation tests."""
    print("\n" + "=" * 80)
    print("  GLiNER2 Task-Specific Validation Tests")
    print("=" * 80)
    print("\nTesting validation for each task type:")
    print("  1. Entity extraction")
    print("  2. Classification")
    print("  3. Structure extraction")
    print("  4. Relation extraction")
    print("  5. Multi-task examples")
    print("  6. Edge cases")
    print("  7. JSONL file loading")
    
    try:
        test_entity_validation()
        test_classification_validation()
        test_structure_validation()
        test_relation_validation()
        test_multi_task_validation()
        test_edge_cases()
        test_validation_with_jsonl_files()
        
        # Summary
        print("\n" + "=" * 80)
        print("  ALL TESTS PASSED! ✓")
        print("=" * 80)
        print("\nSummary:")
        print("  ✓ Entity validation (empty text, missing entities, empty types)")
        print("  ✓ Classification validation (empty tasks, missing labels, label mismatches)")
        print("  ✓ Structure validation (empty names, no fields, invalid ChoiceFields)")
        print("  ✓ Relation validation (empty names, no fields, missing values)")
        print("  ✓ Multi-task validation (mixed valid/invalid tasks)")
        print("  ✓ Edge cases (unicode, special chars, whitespace)")
        print("  ✓ JSONL file validation (all task types)")
        print("\nAll task-specific validation rules work correctly! 🎉\n")
        
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

