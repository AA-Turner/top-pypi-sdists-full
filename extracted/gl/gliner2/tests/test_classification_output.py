"""
Test classification output formatting to ensure results are not misrouted to relation_extraction.

This test addresses the bug where classification results were being incorrectly placed under
the 'relation_extraction' key instead of being at the top level with the task name as key.
"""

import json
from gliner2 import GLiNER2


def test_single_label_classification():
    """Test single-label classification output format."""
    
    print("\n" + "=" * 80)
    print("SINGLE-LABEL CLASSIFICATION TEST")
    print("=" * 80)
    
    print("\nLoading model: fastino/gliner2-base-v1...")
    model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
    print("Model loaded successfully!\n")
    
    text = "This product is amazing and exceeded all my expectations!"
    
    print(f"Test Text: {text}")
    print("-" * 80)
    
    # Create schema with single-label classification
    schema = model.create_schema().classification(
        "sentiment",
        ["positive", "negative", "neutral"],
        multi_label=False,
        cls_threshold=0.5
    )
    
    print("\nSchema:")
    print("  - Classification: sentiment (single-label)")
    print("  - Labels: positive, negative, neutral")
    
    # Extract without confidence
    print("\n" + "-" * 80)
    print("EXTRACTION WITHOUT CONFIDENCE")
    print("-" * 80)
    result = model.extract(text, schema, include_confidence=False)
    print(json.dumps(result, indent=2))
    
    # Verify output structure
    assert "sentiment" in result, "sentiment key should be at top level"
    assert "relation_extraction" not in result, "relation_extraction should not exist for classification-only"
    assert isinstance(result["sentiment"], str), "Single-label result should be a string without confidence"
    
    print("\n✓ Single-label classification without confidence: PASSED")
    
    # Extract with confidence
    print("\n" + "-" * 80)
    print("EXTRACTION WITH CONFIDENCE")
    print("-" * 80)
    result_with_conf = model.extract(text, schema, include_confidence=True)
    print(json.dumps(result_with_conf, indent=2))
    
    # Verify output structure with confidence
    assert "sentiment" in result_with_conf, "sentiment key should be at top level"
    assert "relation_extraction" not in result_with_conf, "relation_extraction should not exist"
    assert isinstance(result_with_conf["sentiment"], dict), "Result with confidence should be a dict"
    assert "label" in result_with_conf["sentiment"], "Result should have 'label' field"
    assert "confidence" in result_with_conf["sentiment"], "Result should have 'confidence' field"
    
    print(f"\nExtracted sentiment: {result_with_conf['sentiment']['label']}")
    print(f"Confidence: {result_with_conf['sentiment']['confidence']:.4f}")
    print("\n✓ Single-label classification with confidence: PASSED")
    
    print("\n" + "=" * 80)
    print("Single-label classification test completed!")
    print("=" * 80)


def test_multi_label_classification():
    """Test multi-label classification output format."""
    
    print("\n" + "=" * 80)
    print("MULTI-LABEL CLASSIFICATION TEST")
    print("=" * 80)
    
    print("\nLoading model: fastino/gliner2-base-v1...")
    model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
    print("Model loaded successfully!\n")
    
    text = "Apple announced new health monitoring features in their latest smartwatch, boosting their stock price."
    
    print(f"Test Text: {text}")
    print("-" * 80)
    
    # Create schema with multi-label classification
    schema = model.create_schema().classification(
        "topics",
        ["technology", "business", "health", "politics", "sports"],
        multi_label=True,
        cls_threshold=0.3
    )
    
    print("\nSchema:")
    print("  - Classification: topics (multi-label)")
    print("  - Labels: technology, business, health, politics, sports")
    print("  - Threshold: 0.3")
    
    # Extract without confidence
    print("\n" + "-" * 80)
    print("EXTRACTION WITHOUT CONFIDENCE")
    print("-" * 80)
    result = model.extract(text, schema, include_confidence=False)
    print(json.dumps(result, indent=2))
    
    # Verify output structure
    assert "topics" in result, "topics key should be at top level"
    assert "relation_extraction" not in result, "relation_extraction should NOT exist for classification-only"
    assert isinstance(result["topics"], list), "Multi-label result should be a list"
    
    if len(result["topics"]) > 0:
        assert isinstance(result["topics"][0], str), "Multi-label items should be strings without confidence"
    
    print("\n✓ Multi-label classification without confidence: PASSED")
    
    # Extract with confidence
    print("\n" + "-" * 80)
    print("EXTRACTION WITH CONFIDENCE")
    print("-" * 80)
    result_with_conf = model.extract(text, schema, include_confidence=True)
    print(json.dumps(result_with_conf, indent=2))
    
    # Verify output structure with confidence
    assert "topics" in result_with_conf, "topics key should be at top level"
    assert "relation_extraction" not in result_with_conf, "relation_extraction should NOT exist"
    assert isinstance(result_with_conf["topics"], list), "Result should be a list"
    
    if len(result_with_conf["topics"]) > 0:
        assert isinstance(result_with_conf["topics"][0], dict), "Items should be dicts with confidence"
        assert "label" in result_with_conf["topics"][0], "Items should have 'label' field"
        assert "confidence" in result_with_conf["topics"][0], "Items should have 'confidence' field"
    
    print("\nExtracted topics:")
    for item in result_with_conf["topics"]:
        print(f"  - {item['label']}: {item['confidence']:.4f}")
    
    print("\n✓ Multi-label classification with confidence: PASSED")
    
    print("\n" + "=" * 80)
    print("Multi-label classification test completed!")
    print("=" * 80)


def test_classification_with_other_tasks():
    """Test that classification works correctly when combined with other extraction tasks."""
    
    print("\n" + "=" * 80)
    print("MIXED TASKS TEST (Classification + Entities + Relations)")
    print("=" * 80)
    
    print("\nLoading model: fastino/gliner2-base-v1...")
    model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
    print("Model loaded successfully!\n")
    
    text = "Apple CEO Tim Cook announced new iPhone features. This is exciting news!"
    
    print(f"Test Text: {text}")
    print("-" * 80)
    
    # Create schema with multiple task types
    schema = model.create_schema()
    schema.entities(["company", "person", "product"])
    schema.relations(["CEO_of"])
    schema.classification("sentiment", ["positive", "negative", "neutral"])
    
    print("\nSchema:")
    print("  - Entities: company, person, product")
    print("  - Relations: CEO_of")
    print("  - Classification: sentiment")
    
    # Extract with confidence
    print("\n" + "-" * 80)
    print("EXTRACTION WITH CONFIDENCE")
    print("-" * 80)
    result = model.extract(text, schema, include_confidence=True)
    print(json.dumps(result, indent=2))
    
    # Verify output structure
    assert "sentiment" in result, "sentiment should be at top level"
    assert "entities" in result, "entities should be present"
    assert "relation_extraction" in result, "relation_extraction should exist for relations"
    
    # Verify classification is NOT under relation_extraction
    if "relation_extraction" in result:
        assert "sentiment" not in result["relation_extraction"], \
            "sentiment should NOT be under relation_extraction"
        assert "CEO_of" in result["relation_extraction"], \
            "CEO_of relation should be under relation_extraction"
    
    # Verify classification format
    assert isinstance(result["sentiment"], dict), "Sentiment should be a dict"
    assert "label" in result["sentiment"], "Sentiment should have 'label' field"
    assert "confidence" in result["sentiment"], "Sentiment should have 'confidence' field"
    
    print("\nResults breakdown:")
    print(f"  Entities: {len(result.get('entities', {}))}")
    print(f"  Relations: {list(result.get('relation_extraction', {}).keys())}")
    print(f"  Sentiment: {result['sentiment']['label']} ({result['sentiment']['confidence']:.4f})")
    
    print("\n✓ Mixed tasks with classification: PASSED")
    
    print("\n" + "=" * 80)
    print("Mixed tasks test completed!")
    print("=" * 80)


def test_multiple_classifications():
    """Test multiple classification tasks in the same schema."""
    
    print("\n" + "=" * 80)
    print("MULTIPLE CLASSIFICATIONS TEST")
    print("=" * 80)
    
    print("\nLoading model: fastino/gliner2-base-v1...")
    model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
    print("Model loaded successfully!\n")
    
    text = "Breaking news: The government announced new healthcare reforms today."
    
    print(f"Test Text: {text}")
    print("-" * 80)
    
    # Create schema with multiple classification tasks
    schema = model.create_schema()
    schema.classification("sentiment", ["positive", "negative", "neutral"])
    schema.classification("urgency", ["urgent", "normal", "low_priority"])
    
    print("\nSchema:")
    print("  - Classification 1: sentiment")
    print("  - Classification 2: urgency")
    
    # Extract with confidence
    print("\n" + "-" * 80)
    print("EXTRACTION WITH CONFIDENCE")
    print("-" * 80)
    result = model.extract(text, schema, include_confidence=True)
    print(json.dumps(result, indent=2))
    
    # Verify both classifications are at top level
    assert "sentiment" in result, "sentiment should be at top level"
    assert "urgency" in result, "urgency should be at top level"
    assert "relation_extraction" not in result, "relation_extraction should not exist"
    
    # Verify both have correct format
    for task in ["sentiment", "urgency"]:
        assert isinstance(result[task], dict), f"{task} should be a dict"
        assert "label" in result[task], f"{task} should have 'label' field"
        assert "confidence" in result[task], f"{task} should have 'confidence' field"
    
    print("\nResults:")
    print(f"  Sentiment: {result['sentiment']['label']} ({result['sentiment']['confidence']:.4f})")
    print(f"  Urgency: {result['urgency']['label']} ({result['urgency']['confidence']:.4f})")
    
    print("\n✓ Multiple classifications: PASSED")
    
    print("\n" + "=" * 80)
    print("Multiple classifications test completed!")
    print("=" * 80)


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("CLASSIFICATION OUTPUT REGRESSION TESTS")
    print("=" * 80)
    print("\nThese tests verify that classification results are correctly formatted")
    print("and NOT misrouted to 'relation_extraction' key.")
    print("=" * 80)
    
    try:
        test_single_label_classification()
        test_multi_label_classification()
        test_classification_with_other_tasks()
        test_multiple_classifications()
        
        print("\n" + "=" * 80)
        print("ALL TESTS PASSED! ✓")
        print("=" * 80)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        raise



