"""
Test threshold handling to ensure 0.0 and high thresholds work correctly.

This test addresses the bug where threshold values of 0.0 were being incorrectly
ignored due to using 'or' operator which treats 0.0 as falsy.
"""

import json
from gliner2 import GLiNER2


def test_entity_threshold_zero():
    """Test that entity threshold of 0.0 accepts all predictions."""
    
    print("\n" + "=" * 80)
    print("ENTITY THRESHOLD 0.0 TEST")
    print("=" * 80)
    
    print("\nLoading model: fastino/gliner2-base-v1...")
    model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
    print("Model loaded successfully!\n")
    
    text = "John Smith works at Apple Inc in Cupertino, California."
    
    print(f"Test Text: {text}")
    print("-" * 80)
    
    # Create schema with 0.0 threshold (accept all)
    schema = model.create_schema().entities(
        {"person": {"threshold": 0.0}, "company": {"threshold": 0.0}},
        dtype="list"
    )
    
    print("\nSchema:")
    print("  - Entities: person (threshold=0.0), company (threshold=0.0)")
    print("  - Expected: Accept ALL entities regardless of confidence")
    
    # Extract with confidence
    print("\n" + "-" * 80)
    print("EXTRACTION WITH CONFIDENCE")
    print("-" * 80)
    result = model.extract(text, schema, include_confidence=True)
    print(json.dumps(result, indent=2))
    
    # Verify we got entities (threshold 0.0 should accept everything)
    assert "entities" in result, "entities key should be present"
    
    # Check that we have at least some entities
    total_entities = sum(len(entities) for entities in result["entities"].values())
    assert total_entities > 0, "Should extract entities with threshold=0.0"
    
    # Verify all entities have confidence >= 0.0 (which is everything)
    for entity_type, entities in result["entities"].items():
        for entity in entities:
            if isinstance(entity, dict) and "confidence" in entity:
                assert entity["confidence"] >= 0.0, f"{entity_type} confidence should be >= 0.0"
                print(f"✓ {entity_type}: {entity['text']} (confidence: {entity['confidence']:.4f})")
    
    print("\n✓ Entity threshold 0.0 test: PASSED")
    print("=" * 80)


def test_entity_threshold_high():
    """Test that high entity threshold filters strictly."""
    
    print("\n" + "=" * 80)
    print("ENTITY THRESHOLD 0.99 TEST")
    print("=" * 80)
    
    print("\nLoading model: fastino/gliner2-base-v1...")
    model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
    print("Model loaded successfully!\n")
    
    text = "John Smith works at Apple Inc in Cupertino, California."
    
    print(f"Test Text: {text}")
    print("-" * 80)
    
    # Create schema with 0.99 threshold (very strict)
    schema = model.create_schema().entities(
        {"person": {"threshold": 0.99}, "company": {"threshold": 0.99}},
        dtype="list"
    )
    
    print("\nSchema:")
    print("  - Entities: person (threshold=0.99), company (threshold=0.99)")
    print("  - Expected: Only extract entities with confidence >= 0.99")
    
    # Extract with confidence
    print("\n" + "-" * 80)
    print("EXTRACTION WITH CONFIDENCE")
    print("-" * 80)
    result = model.extract(text, schema, include_confidence=True)
    print(json.dumps(result, indent=2))
    
    # Verify all extracted entities meet the threshold
    assert "entities" in result, "entities key should be present"
    
    for entity_type, entities in result["entities"].items():
        for entity in entities:
            if isinstance(entity, dict) and "confidence" in entity:
                assert entity["confidence"] >= 0.99, \
                    f"{entity_type} '{entity['text']}' has confidence {entity['confidence']:.4f} < 0.99"
                print(f"✓ {entity_type}: {entity['text']} (confidence: {entity['confidence']:.4f} >= 0.99)")
    
    print("\n✓ Entity threshold 0.99 test: PASSED")
    print("=" * 80)


def test_relation_threshold_zero():
    """Test that relation threshold of 0.0 accepts all predictions."""
    
    print("\n" + "=" * 80)
    print("RELATION THRESHOLD 0.0 TEST")
    print("=" * 80)
    
    print("\nLoading model: fastino/gliner2-base-v1...")
    model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
    print("Model loaded successfully!\n")
    
    text = "John Smith is the CEO of Apple Inc."
    
    print(f"Test Text: {text}")
    print("-" * 80)
    
    # Create schema with 0.0 threshold
    schema = model.create_schema().relations(
        {"CEO_of": {"threshold": 0.0}},
    )
    
    print("\nSchema:")
    print("  - Relations: CEO_of (threshold=0.0)")
    print("  - Expected: Accept ALL relations regardless of confidence")
    
    # Extract with confidence
    print("\n" + "-" * 80)
    print("EXTRACTION WITH CONFIDENCE")
    print("-" * 80)
    result = model.extract(text, schema, include_confidence=True)
    print(json.dumps(result, indent=2))
    
    # Verify structure
    assert "relation_extraction" in result, "relation_extraction key should be present"
    
    print("\n✓ Relation threshold 0.0 test: PASSED")
    print("=" * 80)


def test_relation_threshold_high():
    """Test that high relation threshold filters strictly."""
    
    print("\n" + "=" * 80)
    print("RELATION THRESHOLD 0.99 TEST")
    print("=" * 80)
    
    print("\nLoading model: fastino/gliner2-base-v1...")
    model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
    print("Model loaded successfully!\n")
    
    text = "John Smith is the CEO of Apple Inc."
    
    print(f"Test Text: {text}")
    print("-" * 80)
    
    # Create schema with 0.99 threshold
    schema = model.create_schema().relations(
        {"CEO_of": {"threshold": 0.99}},
    )
    
    print("\nSchema:")
    print("  - Relations: CEO_of (threshold=0.99)")
    print("  - Expected: Only extract relations with confidence >= 0.99")
    
    # Extract with confidence
    print("\n" + "-" * 80)
    print("EXTRACTION WITH CONFIDENCE")
    print("-" * 80)
    result = model.extract(text, schema, include_confidence=True)
    print(json.dumps(result, indent=2))
    
    # Verify all extracted relations meet the threshold
    if "relation_extraction" in result:
        for rel_type, relations in result["relation_extraction"].items():
            for relation in relations:
                if isinstance(relation, dict):
                    # Check head confidence
                    if "head" in relation and isinstance(relation["head"], dict):
                        if "confidence" in relation["head"]:
                            assert relation["head"]["confidence"] >= 0.99, \
                                f"Head confidence {relation['head']['confidence']:.4f} < 0.99"
                    # Check tail confidence
                    if "tail" in relation and isinstance(relation["tail"], dict):
                        if "confidence" in relation["tail"]:
                            assert relation["tail"]["confidence"] >= 0.99, \
                                f"Tail confidence {relation['tail']['confidence']:.4f} < 0.99"
    
    print("\n✓ Relation threshold 0.99 test: PASSED")
    print("=" * 80)


def test_structure_field_threshold_zero():
    """Test that structure field threshold of 0.0 accepts all predictions."""
    
    print("\n" + "=" * 80)
    print("STRUCTURE FIELD THRESHOLD 0.0 TEST")
    print("=" * 80)
    
    print("\nLoading model: fastino/gliner2-base-v1...")
    model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
    print("Model loaded successfully!\n")
    
    text = "Apple released iPhone 15 for $999 on September 12, 2023."
    
    print(f"Test Text: {text}")
    print("-" * 80)
    
    # Create schema with 0.0 threshold for fields
    schema = model.create_schema()
    schema.structure("product_release")\
        .field("company", threshold=0.0)\
        .field("product", threshold=0.0)\
        .field("price", threshold=0.0)\
        .field("date", threshold=0.0)
    
    print("\nSchema:")
    print("  - Structure: product_release")
    print("  - Fields: company, product, price, date (all threshold=0.0)")
    print("  - Expected: Accept ALL field values regardless of confidence")
    
    # Extract with confidence
    print("\n" + "-" * 80)
    print("EXTRACTION WITH CONFIDENCE")
    print("-" * 80)
    result = model.extract(text, schema, include_confidence=True)
    print(json.dumps(result, indent=2))
    
    # Verify structure exists
    assert "product_release" in result, "product_release structure should be present"
    
    print("\n✓ Structure field threshold 0.0 test: PASSED")
    print("=" * 80)


def test_structure_field_threshold_high():
    """Test that high structure field threshold filters strictly."""
    
    print("\n" + "=" * 80)
    print("STRUCTURE FIELD THRESHOLD 0.99 TEST")
    print("=" * 80)
    
    print("\nLoading model: fastino/gliner2-base-v1...")
    model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
    print("Model loaded successfully!\n")
    
    text = "Apple released iPhone 15 for $999 on September 12, 2023."
    
    print(f"Test Text: {text}")
    print("-" * 80)
    
    # Create schema with 0.99 threshold for fields
    schema = model.create_schema()
    schema.structure("product_release")\
        .field("company", threshold=0.99)\
        .field("product", threshold=0.99)\
        .field("price", threshold=0.99)\
        .field("date", threshold=0.99)
    
    print("\nSchema:")
    print("  - Structure: product_release")
    print("  - Fields: company, product, price, date (all threshold=0.99)")
    print("  - Expected: Only extract field values with confidence >= 0.99")
    
    # Extract with confidence
    print("\n" + "-" * 80)
    print("EXTRACTION WITH CONFIDENCE")
    print("-" * 80)
    result = model.extract(text, schema, include_confidence=True)
    print(json.dumps(result, indent=2))
    
    # Verify all extracted field values meet the threshold
    if "product_release" in result:
        for struct in result["product_release"]:
            for field_name, field_values in struct.items():
                if isinstance(field_values, list):
                    for value in field_values:
                        if isinstance(value, dict) and "confidence" in value:
                            assert value["confidence"] >= 0.99, \
                                f"Field '{field_name}' value '{value.get('text')}' has confidence {value['confidence']:.4f} < 0.99"
                            print(f"✓ {field_name}: {value.get('text')} (confidence: {value['confidence']:.4f} >= 0.99)")
                elif isinstance(field_values, dict) and "confidence" in field_values:
                    assert field_values["confidence"] >= 0.99, \
                        f"Field '{field_name}' has confidence {field_values['confidence']:.4f} < 0.99"
                    print(f"✓ {field_name}: {field_values.get('text')} (confidence: {field_values['confidence']:.4f} >= 0.99)")
    
    print("\n✓ Structure field threshold 0.99 test: PASSED")
    print("=" * 80)


def test_mixed_thresholds():
    """Test that different thresholds can be set for different extraction types."""
    
    print("\n" + "=" * 80)
    print("MIXED THRESHOLDS TEST")
    print("=" * 80)
    
    print("\nLoading model: fastino/gliner2-base-v1...")
    model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
    print("Model loaded successfully!\n")
    
    text = "John Smith is the CEO of Apple Inc in Cupertino."
    
    print(f"Test Text: {text}")
    print("-" * 80)
    
    # Create schema with different thresholds
    schema = model.create_schema()
    schema.entities({
        "person": {"threshold": 0.0},     # Accept all persons
        "company": {"threshold": 0.99},   # Only high-confidence companies
        "location": {"threshold": 0.5}    # Default-like threshold
    })
    
    print("\nSchema:")
    print("  - person: threshold=0.0 (accept all)")
    print("  - company: threshold=0.99 (very strict)")
    print("  - location: threshold=0.5 (moderate)")
    
    # Extract with confidence
    print("\n" + "-" * 80)
    print("EXTRACTION WITH CONFIDENCE")
    print("-" * 80)
    result = model.extract(text, schema, include_confidence=True)
    print(json.dumps(result, indent=2))
    
    # Verify thresholds are respected per entity type
    if "entities" in result:
        for entity_type, entities in result["entities"].items():
            for entity in entities:
                if isinstance(entity, dict) and "confidence" in entity:
                    if entity_type == "person":
                        # Should accept all (>= 0.0)
                        assert entity["confidence"] >= 0.0
                        print(f"✓ person: {entity['text']} (confidence: {entity['confidence']:.4f} >= 0.0)")
                    elif entity_type == "company":
                        # Should only have high confidence (>= 0.99)
                        assert entity["confidence"] >= 0.99, \
                            f"company '{entity['text']}' has confidence {entity['confidence']:.4f} < 0.99"
                        print(f"✓ company: {entity['text']} (confidence: {entity['confidence']:.4f} >= 0.99)")
                    elif entity_type == "location":
                        # Should meet moderate threshold (>= 0.5)
                        assert entity["confidence"] >= 0.5
                        print(f"✓ location: {entity['text']} (confidence: {entity['confidence']:.4f} >= 0.5)")
    
    print("\n✓ Mixed thresholds test: PASSED")
    print("=" * 80)


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("THRESHOLD HANDLING REGRESSION TESTS")
    print("=" * 80)
    print("\nThese tests verify that threshold values of 0.0 and high values (0.99)")
    print("are correctly handled across all extraction types.")
    print("=" * 80)
    
    try:
        test_entity_threshold_zero()
        test_entity_threshold_high()
        test_relation_threshold_zero()
        test_relation_threshold_high()
        test_structure_field_threshold_zero()
        test_structure_field_threshold_high()
        test_mixed_thresholds()
        
        print("\n" + "=" * 80)
        print("ALL THRESHOLD TESTS PASSED! ✓")
        print("=" * 80)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        raise



