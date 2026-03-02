"""
Comprehensive test for all extraction types with include_confidence and include_spans.

This test demonstrates the new API features across all extraction types:
- Entity extraction
- Relation extraction
- Structure extraction
- Classification (confidence already supported, spans N/A)
"""

import json
from gliner2 import GLiNER2


def test_comprehensive_extraction():
    """Test all extraction types together with full metadata."""
    
    print("=" * 80)
    print("COMPREHENSIVE EXTRACTION TEST")
    print("=" * 80)
    
    print("\nLoading model: fastino/gliner2-base-v1...")
    model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
    print("Model loaded successfully!\n")
    
    text = "Apple CEO Tim Cook announced the iPhone 15 launch at $999 in Cupertino on September 12, 2023."
    
    print(f"\nTest Text: {text}")
    print("\n" + "-" * 80)
    
    # Create comprehensive schema
    schema = model.create_schema()
    
    # Add entities
    schema.entities(["company", "person", "product", "location", "date", "price"])
    
    # Add relations
    schema.relations(["CEO_of", "located_in", "announced_on"])
    
    # Add structure
    schema.structure("product_announcement")\
        .field("company")\
        .field("product")\
        .field("price")\
        .field("location")\
        .field("date")
    
    # Add classification
    schema.classification("sentiment", ["positive", "negative", "neutral"])
    
    print("\nSchema:")
    print("  - Entities: company, person, product, location, date, price")
    print("  - Relations: CEO_of, located_in, announced_on")
    print("  - Structure: product_announcement")
    print("  - Classification: sentiment")
    
    # Extract with all features
    print("\n" + "-" * 80)
    print("EXTRACTION WITH CONFIDENCE AND SPANS")
    print("-" * 80)
    result = model.extract(text, schema, include_confidence=True, include_spans=True)
    
    print(json.dumps(result, indent=2))
    
    # Verify all span positions
    print("\n" + "-" * 80)
    print("VERIFICATION OF CHARACTER POSITIONS")
    print("-" * 80)
    
    print("\nEntities:")
    for entity_type, entities in result["entities"].items():
        for entity in entities:
            extracted = text[entity["start"]:entity["end"]]
            match = "✓" if extracted == entity["text"] else "✗"
            print(f"  {match} {entity_type}: '{entity['text']}' [{entity['start']}:{entity['end']}]")
    
    print("\nRelations:")
    for rel_type, relations in result["relation_extraction"].items():
        print(f"  {rel_type}:")
        for rel in relations:
            head_extracted = text[rel["head"]["start"]:rel["head"]["end"]]
            tail_extracted = text[rel["tail"]["start"]:rel["tail"]["end"]]
            head_match = "✓" if head_extracted == rel["head"]["text"] else "✗"
            tail_match = "✓" if tail_extracted == rel["tail"]["text"] else "✗"
            print(f"    {head_match} Head: '{rel['head']['text']}' [{rel['head']['start']}:{rel['head']['end']}]")
            print(f"    {tail_match} Tail: '{rel['tail']['text']}' [{rel['tail']['start']}:{rel['tail']['end']}]")
    
    print("\nStructure (product_announcement):")
    for struct in result["product_announcement"]:
        for field_name, field_values in struct.items():
            for value in field_values:
                extracted = text[value["start"]:value["end"]]
                match = "✓" if extracted == value["text"] else "✗"
                print(f"  {match} {field_name}: '{value['text']}' [{value['start']}:{value['end']}]")
    
    print("\nClassification:")
    print(f"  sentiment: {result['sentiment']['label']} (confidence: {result['sentiment']['confidence']})")
    
    print("\n" + "=" * 80)
    print("Comprehensive extraction test completed!")
    print("=" * 80)


def test_mixed_output_formats():
    """Test different combinations of confidence and spans."""
    
    print("\n" + "=" * 80)
    print("MIXED OUTPUT FORMATS TEST")
    print("=" * 80)
    
    text = "Apple launched iPhone 15 in Cupertino."
    
    print(f"\nTest Text: {text}")
    print("\n" + "-" * 80)
    
    # Test 1: Default (no extra metadata)
    print("\n1. DEFAULT OUTPUT (text only)")
    print("-" * 40)
    result = {
        "entities": {
            "company": ["Apple"],
            "product": ["iPhone 15"],
            "location": ["Cupertino"]
        }
    }
    print(json.dumps(result, indent=2))
    
    # Test 2: Only confidence
    print("\n2. ONLY CONFIDENCE")
    print("-" * 40)
    result = {
        "entities": {
            "company": [{"text": "Apple", "confidence": 0.95}],
            "product": [{"text": "iPhone 15", "confidence": 0.89}],
            "location": [{"text": "Cupertino", "confidence": 0.88}]
        }
    }
    print(json.dumps(result, indent=2))
    
    # Test 3: Only spans
    print("\n3. ONLY SPANS")
    print("-" * 40)
    result = {
        "entities": {
            "company": [{"text": "Apple", "start": 0, "end": 5}],
            "product": [{"text": "iPhone 15", "start": 16, "end": 25}],
            "location": [{"text": "Cupertino", "start": 29, "end": 38}]
        }
    }
    print(json.dumps(result, indent=2))
    
    # Test 4: Both confidence and spans
    print("\n4. BOTH CONFIDENCE AND SPANS")
    print("-" * 40)
    result = {
        "entities": {
            "company": [{"text": "Apple", "confidence": 0.95, "start": 0, "end": 5}],
            "product": [{"text": "iPhone 15", "confidence": 0.89, "start": 16, "end": 25}],
            "location": [{"text": "Cupertino", "confidence": 0.88, "start": 29, "end": 38}]
        }
    }
    print(json.dumps(result, indent=2))
    
    print("\n" + "=" * 80)
    print("Mixed output formats test completed!")
    print("=" * 80)


def test_usage_examples():
    """Show practical usage examples."""
    
    print("\n" + "=" * 80)
    print("PRACTICAL USAGE EXAMPLES")
    print("=" * 80)
    
    print("\nExample 1: Named Entity Recognition for downstream processing")
    print("-" * 40)
    print("Use case: Extract entities with positions for highlighting in UI")
    print("\nCode:")
    print("""
    result = model.extract_entities(
        text, 
        ["company", "person", "product"],
        include_spans=True
    )
    
    # Use spans to highlight entities in the original text
    for entity_type, entities in result["entities"].items():
        for entity in entities:
            print(f"Highlight {entity['text']} from {entity['start']} to {entity['end']}")
    """)
    
    print("\n" + "-" * 40)
    print("\nExample 2: Confidence-based filtering")
    print("-" * 40)
    print("Use case: Only keep high-confidence predictions")
    print("\nCode:")
    print("""
    result = model.extract_entities(
        text,
        ["company", "person"],
        include_confidence=True
    )
    
    # Filter by confidence threshold
    high_confidence_entities = {}
    for entity_type, entities in result["entities"].items():
        high_confidence_entities[entity_type] = [
            e for e in entities if e["confidence"] >= 0.90
        ]
    """)
    
    print("\n" + "-" * 40)
    print("\nExample 3: Relation extraction with provenance")
    print("-" * 40)
    print("Use case: Extract relations with exact text positions for verification")
    print("\nCode:")
    print("""
    result = model.extract_relations(
        text,
        ["CEO_of", "works_at"],
        include_confidence=True,
        include_spans=True
    )
    
    # Verify and display relations with context
    for rel_type, relations in result["relation_extraction"].items():
        for rel in relations:
            head_text = text[rel["head"]["start"]:rel["head"]["end"]]
            tail_text = text[rel["tail"]["start"]:rel["tail"]["end"]]
            print(f"{rel_type}: {head_text} -> {tail_text}")
            print(f"  Confidence: {rel['head']['confidence']:.2f}, {rel['tail']['confidence']:.2f}")
    """)
    
    print("\n" + "-" * 40)
    print("\nExample 4: Structured data extraction for knowledge base")
    print("-" * 40)
    print("Use case: Build structured KB with source attribution")
    print("\nCode:")
    print("""
    schema = model.create_schema()
    schema.structure("person_info")\\
        .field("name")\\
        .field("title")\\
        .field("company")\\
        .field("location")
    
    result = model.extract(
        text, schema,
        include_confidence=True,
        include_spans=True
    )
    
    # Store in knowledge base with provenance
    for struct in result["person_info"]:
        kb_entry = {
            "name": struct["name"][0]["text"],
            "source_text": text,
            "source_positions": {
                field: values[0]["start"] 
                for field, values in struct.items() 
                if values
            },
            "confidence_scores": {
                field: values[0]["confidence"]
                for field, values in struct.items()
                if values
            }
        }
    """)
    
    print("\n" + "=" * 80)
    print("Usage examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    test_comprehensive_extraction()
    test_mixed_output_formats()
    test_usage_examples()

