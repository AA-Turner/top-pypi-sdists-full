#!/usr/bin/env python3
"""
Test script for GLiNER2 API Client

This script tests the GLiNER2.from_api() functionality with:
- Named Entity Recognition (NER)
- Text Classification
- Structured Field Extraction (JSON)
- Relation Extraction
- Combined schema-based extraction
- Confidence scores (include_confidence=True)
- Character positions (include_spans=True)
- Raw results (format_results=False)

Usage:
    export PIONEER_API_KEY="your-api-key"
    python test_api_client.py

    # Or use development environment:
    python test_api_client.py --dev
"""

import os
import sys
import argparse

# Add the parent directory to path for local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gliner2 import GLiNER2

# Development environment settings
DEV_API_URL = "https://ddwcqhkdij.execute-api.us-west-2.amazonaws.com/dev"
DEV_API_KEY = "pio_sk_iKqr4rAUIGe68Izbr4v3n_ec61925c-b31d-4f6e-9040-7d36d4860fb9"


def test_entity_extraction(extractor):
    """Test Named Entity Recognition (NER)"""
    print("\n" + "=" * 60)
    print("TEST 1: Named Entity Recognition (NER)")
    print("=" * 60)

    text = "Apple CEO Tim Cook announced the iPhone 15 Pro at the Steve Jobs Theater in Cupertino, California on September 12, 2023."
    entity_types = ["company", "person", "product", "location", "date"]

    print(f"\nInput text: {text}")
    print(f"Entity types: {entity_types}")

    result = extractor.extract_entities(text, entity_types, threshold=0.5)

    print("\nResults:")
    print(result)

    return result


def test_entity_extraction_with_confidence(extractor):
    """Test Named Entity Recognition (NER) with confidence scores"""
    print("\n" + "=" * 60)
    print("TEST 1b: NER with Confidence Scores")
    print("=" * 60)

    text = "Apple CEO Tim Cook announced the iPhone 15 Pro at the Steve Jobs Theater in Cupertino, California on September 12, 2023."
    entity_types = ["company", "person", "product", "location", "date"]

    print(f"\nInput text: {text}")
    print(f"Entity types: {entity_types}")
    print("include_confidence: True")

    result = extractor.extract_entities(text, entity_types, threshold=0.5, include_confidence=True)

    print("\nResults with confidence scores:")
    print(result)

    return result


def test_entity_extraction_raw(extractor):
    """Test Named Entity Recognition (NER) with raw results"""
    print("\n" + "=" * 60)
    print("TEST 1c: NER with Raw Results (format_results=False)")
    print("=" * 60)

    text = "Apple CEO Tim Cook announced the iPhone 15 Pro in Cupertino."
    entity_types = ["company", "person", "product", "location"]

    print(f"\nInput text: {text}")
    print(f"Entity types: {entity_types}")
    print("format_results: False")

    result = extractor.extract_entities(text, entity_types, threshold=0.5, format_results=False)

    print("\nRaw results (includes span positions, confidence, etc.):")
    print(result)

    return result


def test_entity_extraction_with_spans(extractor):
    """Test Named Entity Recognition (NER) with character positions"""
    print("\n" + "=" * 60)
    print("TEST 1d: NER with Character Positions (include_spans=True)")
    print("=" * 60)

    text = "Apple CEO Tim Cook announced the iPhone 15 Pro in Cupertino."
    entity_types = ["company", "person", "product", "location"]

    print(f"\nInput text: {text}")
    print(f"Entity types: {entity_types}")
    print("include_spans: True")

    result = extractor.extract_entities(text, entity_types, threshold=0.5, include_spans=True)

    print("\nResults with character positions:")
    print(result)

    # Verify span positions by extracting text
    entities = result.get("entities", {})
    for entity_type, values in entities.items():
        if isinstance(values, list):
            for val in values:
                if isinstance(val, dict) and "start" in val and "end" in val:
                    extracted = text[val["start"]:val["end"]]
                    print(
                        f"  ✓ {entity_type}: '{val.get('text', '')}' at [{val['start']}:{val['end']}] -> '{extracted}'")

    return result


def test_entity_extraction_with_confidence_and_spans(extractor):
    """Test Named Entity Recognition (NER) with both confidence and character positions"""
    print("\n" + "=" * 60)
    print("TEST 1e: NER with Confidence AND Positions")
    print("=" * 60)

    text = "Apple CEO Tim Cook announced the iPhone 15 Pro in Cupertino."
    entity_types = ["company", "person", "product", "location"]

    print(f"\nInput text: {text}")
    print(f"Entity types: {entity_types}")
    print("include_confidence: True")
    print("include_spans: True")

    result = extractor.extract_entities(
        text, entity_types, threshold=0.5,
        include_confidence=True, include_spans=True
    )

    print("\nResults with confidence and character positions:")
    print(result)

    # Verify results have all fields
    entities = result.get("entities", {})
    for entity_type, values in entities.items():
        if isinstance(values, list):
            for val in values:
                if isinstance(val, dict):
                    has_text = "text" in val
                    has_conf = "confidence" in val
                    has_start = "start" in val
                    has_end = "end" in val
                    if has_text and has_conf and has_start and has_end:
                        extracted = text[val["start"]:val["end"]]
                        print(
                            f"  ✓ {entity_type}: '{val['text']}' conf={val['confidence']:.3f} at [{val['start']}:{val['end']}] -> '{extracted}'")

    return result


def test_batch_entity_extraction(extractor):
    """Test batch NER extraction"""
    print("\n" + "=" * 60)
    print("TEST 2: Batch Entity Extraction")
    print("=" * 60)

    texts = [
        "Google's Sundar Pichai unveiled Gemini AI in Mountain View.",
        "Microsoft CEO Satya Nadella announced Copilot at Build 2023.",
        "Amazon's Andy Jassy revealed new AWS services in Seattle.",
    ]
    entity_types = ["company", "person", "product", "location"]

    print(f"\nInput texts: {len(texts)} texts")
    for i, t in enumerate(texts, 1):
        print(f"  {i}. {t}")
    print(f"Entity types: {entity_types}")

    results = extractor.batch_extract_entities(texts, entity_types, threshold=0.5)

    print("\nResults:")
    for i, result in enumerate(results, 1):
        print(f"\n  Text {i}:")
        print(f"  {result}")

    return results


def test_text_classification(extractor):
    """Test text classification"""
    print("\n" + "=" * 60)
    print("TEST 3: Text Classification")
    print("=" * 60)

    text = "I absolutely love this product! It exceeded all my expectations and I would highly recommend it to anyone."

    print(f"\nInput text: {text}")

    # Single-label classification
    result = extractor.classify_text(
        text,
        {"sentiment": ["positive", "negative", "neutral"]},
        threshold=0.5
    )

    print("\nSentiment Classification Result:")
    print(result)

    return result


def test_text_classification_with_confidence(extractor):
    """Test text classification with confidence scores"""
    print("\n" + "=" * 60)
    print("TEST 3b: Classification with Confidence Scores")
    print("=" * 60)

    text = "I absolutely love this product! It exceeded all my expectations and I would highly recommend it to anyone."

    print(f"\nInput text: {text}")
    print("include_confidence: True")

    # Single-label classification with confidence
    result = extractor.classify_text(
        text,
        {"sentiment": ["positive", "negative", "neutral"]},
        threshold=0.5,
        include_confidence=True
    )

    print("\nClassification Result with confidence scores:")
    print(result)

    return result


def test_multi_classification(extractor):
    """Test multiple classification tasks"""
    print("\n" + "=" * 60)
    print("TEST 4: Multiple Classification Tasks")
    print("=" * 60)

    text = "Breaking: Major earthquake hits coastal city, rescue teams deployed immediately. Thousands evacuated as aftershocks continue."

    print(f"\nInput text: {text}")

    result = extractor.classify_text(
        text,
        {
            "category": ["politics", "sports", "technology", "disaster", "entertainment"],
            "urgency": ["high", "medium", "low"],
        },
        threshold=0.3
    )

    print("\nMulti-task Classification Result:")
    print(result)

    return result


def test_json_extraction(extractor):
    """Test structured field extraction (extract_json)"""
    print("\n" + "=" * 60)
    print("TEST 5: Structured Field Extraction (JSON)")
    print("=" * 60)

    text = "Contact John Smith at john.smith@email.com or call him at +1-555-123-4567. He works as a Senior Software Engineer at TechCorp Inc."

    structures = {
        "contact": [
            "name::str::Full name of the person",
            "email::str::Email address",
            "phone::str::Phone number",
            "job_title::str::Professional title",
            "company::str::Company name",
        ]
    }

    print(f"\nInput text: {text}")
    print(f"Structure definition: {structures}")

    result = extractor.extract_json(text, structures, threshold=0.4)

    print("\nExtracted Structure:")
    print(result)

    return result


def test_json_extraction_with_confidence(extractor):
    """Test structured field extraction with confidence scores"""
    print("\n" + "=" * 60)
    print("TEST 5b: JSON Extraction with Confidence Scores")
    print("=" * 60)

    text = "Contact John Smith at john.smith@email.com or call him at +1-555-123-4567. He works as a Senior Software Engineer at TechCorp Inc."

    structures = {
        "contact": [
            "name::str::Full name of the person",
            "email::str::Email address",
            "phone::str::Phone number",
            "job_title::str::Professional title",
            "company::str::Company name",
        ]
    }

    print(f"\nInput text: {text}")
    print("include_confidence: True")

    result = extractor.extract_json(text, structures, threshold=0.4, include_confidence=True)

    print("\nExtracted Structure with confidence scores:")
    print(result)

    return result


def test_json_extraction_with_spans(extractor):
    """Test structured field extraction with character positions"""
    print("\n" + "=" * 60)
    print("TEST 5c: JSON Extraction with Character Positions")
    print("=" * 60)

    text = "Contact John Smith at john.smith@email.com or call him at +1-555-123-4567. He works as a Senior Software Engineer at TechCorp Inc."

    structures = {
        "contact": [
            "name::str::Full name of the person",
            "email::str::Email address",
            "phone::str::Phone number",
            "job_title::str::Professional title",
            "company::str::Company name",
        ]
    }

    print(f"\nInput text: {text}")
    print("include_confidence: True")
    print("include_spans: True")

    result = extractor.extract_json(
        text, structures, threshold=0.4,
        include_confidence=True, include_spans=True
    )

    print("\nExtracted Structure with confidence and positions:")
    print(result)

    # Verify positions
    contacts = result.get("contact", [])
    if contacts and isinstance(contacts, list):
        for contact in contacts:
            for field_name, field_value in contact.items():
                if isinstance(field_value, dict) and "start" in field_value and "end" in field_value:
                    extracted = text[field_value["start"]:field_value["end"]]
                    conf = field_value.get("confidence", "N/A")
                    print(
                        f"  ✓ {field_name}: '{field_value.get('text', '')}' conf={conf} at [{field_value['start']}:{field_value['end']}] -> '{extracted}'")

    return result


def test_batch_json_extraction(extractor):
    """Test batch structured extraction"""
    print("\n" + "=" * 60)
    print("TEST 6: Batch Structured Extraction")
    print("=" * 60)

    texts = [
        "iPhone 15 Pro Max costs $1199 with 256GB storage and comes in Natural Titanium.",
        "Samsung Galaxy S24 Ultra is priced at $1299 with 512GB and Titanium Gray color.",
        "Google Pixel 8 Pro available for $999 with 128GB in Obsidian black.",
    ]

    structures = {
        "product": [
            "name::str::Product name",
            "price::str::Price amount",
            "storage::str::Storage capacity",
            "color::str::Color option",
        ]
    }

    print(f"\nInput texts: {len(texts)} texts")
    for i, t in enumerate(texts, 1):
        print(f"  {i}. {t}")

    results = extractor.batch_extract_json(texts, structures, threshold=0.4)

    print("\nExtracted Products:")
    for i, result in enumerate(results, 1):
        print(f"\n  Product {i}:")
        print(f"  {result}")

    return results


def test_schema_extraction(extractor):
    """Test combined schema-based extraction (entities + classification + structure)"""
    print("\n" + "=" * 60)
    print("TEST 7: Combined Schema Extraction")
    print("=" * 60)

    text = """
    Tech Review: The new MacBook Pro M3 is absolutely fantastic! Apple has outdone themselves.
    I tested it in San Francisco last week and the performance is incredible.
    The 14-inch model with 18GB RAM runs complex AI workloads smoothly.
    Highly recommended for developers and creative professionals.
    Rating: 5 out of 5 stars.
    """

    print(f"\nInput text: {text.strip()}")

    schema = (extractor.create_schema()
              .entities(["company", "product", "location"])
              .classification("sentiment", ["positive", "negative", "neutral"])
              .structure("review")
              .field("product_name", dtype="str")
              .field("rating", dtype="str")
              .field("recommendation", dtype="str")
              )

    result = extractor.extract(text, schema, threshold=0.4)

    print("\nCombined Extraction Result:")
    print(result)

    return result


def test_relation_extraction(extractor):
    """Test relation extraction"""
    print("\n" + "=" * 60)
    print("TEST 8: Relation Extraction")
    print("=" * 60)

    text = "John works for Apple Inc. and lives in San Francisco. Apple Inc. is located in Cupertino."
    relation_types = ["works_for", "lives_in", "located_in"]

    print(f"\nInput text: {text}")
    print(f"Relation types: {relation_types}")

    result = extractor.extract_relations(text, relation_types, threshold=0.5)

    print("\nExtracted Relations:")
    print(result)

    return result


def test_relation_extraction_with_descriptions(extractor):
    """Test relation extraction with descriptions"""
    print("\n" + "=" * 60)
    print("TEST 8b: Relation Extraction with Descriptions")
    print("=" * 60)

    text = "Elon Musk founded SpaceX in 2002. SpaceX is located in Hawthorne, California."

    print(f"\nInput text: {text}")

    schema = extractor.create_schema().relations({
        "founded": "Founding relationship where person created organization",
        "located_in": "Geographic relationship where entity is in a location"
    })

    result = extractor.extract(text, schema, threshold=0.5)

    print("\nExtracted Relations with descriptions:")
    print(result)

    return result


def test_batch_relation_extraction(extractor):
    """Test batch relation extraction"""
    print("\n" + "=" * 60)
    print("TEST 8c: Batch Relation Extraction")
    print("=" * 60)

    texts = [
        "John works for Microsoft and lives in Seattle.",
        "Sarah founded TechStartup in 2020.",
        "Bob reports to Alice at Google."
    ]
    relation_types = ["works_for", "founded", "reports_to", "lives_in"]

    print(f"\nInput texts: {len(texts)} texts")
    for i, t in enumerate(texts, 1):
        print(f"  {i}. {t}")
    print(f"Relation types: {relation_types}")

    results = extractor.batch_extract_relations(texts, relation_types, threshold=0.5)

    print("\nExtracted Relations:")
    for i, result in enumerate(results, 1):
        print(f"\n  Text {i}:")
        print(f"  {result}")

    return results


def test_combined_with_relations(extractor):
    """Test combined schema with entities, classification, relations, and structure"""
    print("\n" + "=" * 60)
    print("TEST 9: Combined Schema with Relations")
    print("=" * 60)

    text = """
    Tim Cook works for Apple. Apple is located in Cupertino, California.
    The company announced the iPhone 15 Pro. This is a fantastic product launch!
    """

    print(f"\nInput text: {text.strip()}")

    schema = (extractor.create_schema()
              .entities(["person", "company", "product", "location"])
              .classification("sentiment", ["positive", "negative", "neutral"])
              .relations(["works_for", "located_in"])
              .structure("announcement")
              .field("product_name", dtype="str")
              .field("company", dtype="str")
              )

    result = extractor.extract(text, schema, threshold=0.4)

    print("\nCombined Extraction with Relations:")
    print(result)

    return result


def test_relation_extraction_with_confidence(extractor):
    """Test relation extraction with confidence scores"""
    print("\n" + "=" * 60)
    print("TEST 8d: Relation Extraction with Confidence")
    print("=" * 60)

    text = "John works for Apple Inc. Apple Inc. is located in Cupertino."
    relation_types = ["works_for", "located_in"]

    print(f"\nInput text: {text}")
    print(f"Relation types: {relation_types}")
    print("include_confidence: True")

    result = extractor.extract_relations(text, relation_types, threshold=0.5, include_confidence=True)

    print("\nExtracted Relations with confidence:")
    print(result)

    return result


def test_relation_extraction_with_spans(extractor):
    """Test relation extraction with character positions"""
    print("\n" + "=" * 60)
    print("TEST 8e: Relation Extraction with Character Positions")
    print("=" * 60)

    text = "John works for Apple Inc. Apple Inc. is located in Cupertino."
    relation_types = ["works_for", "located_in"]

    print(f"\nInput text: {text}")
    print(f"Relation types: {relation_types}")
    print("include_confidence: True")
    print("include_spans: True")

    result = extractor.extract_relations(
        text, relation_types, threshold=0.5,
        include_confidence=True, include_spans=True
    )

    print("\nExtracted Relations with confidence and positions:")
    print(result)

    # Verify relation positions
    relations = result.get("relation_extraction", {})
    for rel_type, instances in relations.items():
        if isinstance(instances, list):
            for inst in instances:
                if isinstance(inst, dict) and "head" in inst and "tail" in inst:
                    head = inst["head"]
                    tail = inst["tail"]
                    if isinstance(head, dict) and "start" in head:
                        head_text = text[head["start"]:head["end"]]
                        print(
                            f"  ✓ {rel_type} head: '{head.get('text', '')}' at [{head['start']}:{head['end']}] -> '{head_text}'")
                    if isinstance(tail, dict) and "start" in tail:
                        tail_text = text[tail["start"]:tail["end"]]
                        print(
                            f"  ✓ {rel_type} tail: '{tail.get('text', '')}' at [{tail['start']}:{tail['end']}] -> '{tail_text}'")

    return result


def main():
    """Run all tests"""
    # Parse arguments
    parser = argparse.ArgumentParser(description="Test GLiNER2 API Client")
    parser.add_argument("--dev", action="store_true", help="Use development environment")
    parser.add_argument("--relations-only", action="store_true", help="Run only relation extraction tests")
    args = parser.parse_args()

    print("=" * 60)
    print("GLiNER2 API Client Test Suite")
    print("=" * 60)

    # Determine API settings
    if args.dev:
        api_key = DEV_API_KEY
        api_url = DEV_API_URL
        print(f"\n🔧 Using DEVELOPMENT environment")
        print(f"API URL: {api_url}")
    else:
        api_key = os.environ.get("PIONEER_API_KEY")
        api_url = None  # Use default
        if not api_key:
            print("\nError: PIONEER_API_KEY environment variable not set!")
            print("Please set it with: export PIONEER_API_KEY='your-api-key'")
            print("Or use --dev flag for development environment")
            sys.exit(1)

    print(f"API Key: {api_key[:8]}...{api_key[-4:]}")

    # Initialize the API client
    print("\nInitializing GLiNER2 API client...")
    try:
        if args.dev:
            extractor = GLiNER2.from_api(api_key=api_key, api_base_url=api_url)
        else:
            extractor = GLiNER2.from_api()
        print("✓ API client initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize API client: {e}")
        sys.exit(1)

    # Run tests
    all_results = {}
    total_tests = 0

    # If --relations-only, only run relation tests
    if args.relations_only:
        tests = [
            ("relation_extraction", test_relation_extraction),
            ("relation_with_descriptions", test_relation_extraction_with_descriptions),
            ("batch_relations", test_batch_relation_extraction),
            ("relation_with_confidence", test_relation_extraction_with_confidence),
            ("combined_with_relations", test_combined_with_relations),
        ]
    else:
        tests = [
            ("ner", test_entity_extraction),
            ("ner_confidence", test_entity_extraction_with_confidence),
            ("ner_raw", test_entity_extraction_raw),
            ("ner_spans", test_entity_extraction_with_spans),
            ("ner_confidence_spans", test_entity_extraction_with_confidence_and_spans),
            ("batch_ner", test_batch_entity_extraction),
            ("classification", test_text_classification),
            ("classification_confidence", test_text_classification_with_confidence),
            ("multi_classification", test_multi_classification),
            ("json_extraction", test_json_extraction),
            ("json_confidence", test_json_extraction_with_confidence),
            ("json_spans", test_json_extraction_with_spans),
            ("batch_json", test_batch_json_extraction),
            ("schema", test_schema_extraction),
            ("relation_extraction", test_relation_extraction),
            ("relation_with_descriptions", test_relation_extraction_with_descriptions),
            ("batch_relations", test_batch_relation_extraction),
            ("relation_with_confidence", test_relation_extraction_with_confidence),
            ("relation_with_spans", test_relation_extraction_with_spans),
            ("combined_with_relations", test_combined_with_relations),
        ]

    total_tests = len(tests)

    for test_name, test_func in tests:
        try:
            all_results[test_name] = test_func(extractor)
        except Exception as e:
            print(f"\n✗ {test_name} test failed: {e}")
            import traceback
            traceback.print_exc()

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = len(all_results)

    print(f"\nTests passed: {passed}/{total_tests}")

    if passed == total_tests:
        print("\n✓ All tests completed successfully!")
    else:
        print(f"\n⚠ {total_tests - passed} test(s) failed")

    # Clean up
    extractor.close()

    return all_results


if __name__ == "__main__":
    main()

