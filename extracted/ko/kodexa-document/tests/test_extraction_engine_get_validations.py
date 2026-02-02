"""
Test for ExtractionEngine.get_document_taxon_validations() method.

This test verifies that the engine's get_document_taxon_validations() method
returns the validation rules that were active during extraction, matching the
Go implementation behavior.
"""

import json
import pytest
from pathlib import Path

try:
    from kodexa_document import Document, ExtractionEngine
    EXTRACTION_AVAILABLE = True
except ImportError:
    EXTRACTION_AVAILABLE = False


@pytest.mark.skipif(not EXTRACTION_AVAILABLE, reason="Extraction engine not available")
def test_engine_get_document_taxon_validations():
    """
    Test that engine.get_document_taxon_validations() returns validations after process_and_save().

    This mirrors the Go test:
      lib/go/integration/extraction_engine_get_validations_test.go::TestExtractionEngine_GetDocumentTaxonValidations

    Verifies:
    1. Before process_and_save(): engine returns 0 validations
    2. After process_and_save(): engine returns validations that were set on the document
    3. The returned validations match what was set on the document
    """

    # Get paths to test files
    repo_root = Path(__file__).parent.parent.parent.parent
    kddb_path = repo_root / "test_extractions" / "validations" / "input.kddb"
    taxonomy_path = repo_root / "test_extractions" / "validations" / "taxonomy.json"

    # Verify files exist
    if not kddb_path.exists():
        pytest.skip(f"Test KDDB file not found: {kddb_path}")
    if not taxonomy_path.exists():
        pytest.skip(f"Test taxonomy file not found: {taxonomy_path}")

    try:
        # Load the document
        doc = Document.from_kddb(str(kddb_path))
        print(f"✓ Loaded document from {kddb_path.name}")

        # Load the taxonomy
        with open(taxonomy_path, 'r') as f:
            taxonomy_data = json.load(f)
        print(f"✓ Loaded taxonomy: {taxonomy_data.get('name', 'Unknown')}")

        # Create validation rules to add to the document
        validation1 = {
            "taxonomyRef": taxonomy_data["ref"],
            "taxonPath": "Invoice/MasterAccountNumber",
            "validation": {
                "name": "Test Validation 1",
                "ruleFormula": "1=1",
                "messageFormula": '"Test message 1"',
                "exceptionId": "test-validation-1"
            }
        }

        validation2 = {
            "taxonomyRef": taxonomy_data["ref"],
            "taxonPath": "Invoice/CorrelationID",
            "validation": {
                "name": "Test Validation 2",
                "ruleFormula": "1=1",
                "messageFormula": '"Test message 2"',
                "exceptionId": "test-validation-2"
            }
        }

        # Add validations to the document
        doc.set_validations([validation1, validation2])
        doc_validations = doc.get_validations()
        print(f"✓ Set {len(doc_validations)} validations on document")
        assert len(doc_validations) == 2, "Document should have 2 validations"

        # Create extraction engine
        with ExtractionEngine(doc, [taxonomy_data]) as engine:
            print("✓ Created extraction engine")

            # BEFORE calling process_and_save(), the engine should have 0 validations
            validations_before = engine.get_document_taxon_validations()
            print(f"✓ Before process_and_save(): engine has {len(validations_before)} validations")
            assert len(validations_before) == 0, "Engine should have 0 validations before process_and_save()"

            # Run extraction
            count = engine.process_and_save()
            print(f"✓ Extraction completed, extracted {count} data objects")

            # AFTER calling process_and_save(), the engine should have 2 validations
            # (copied from document during process)
            validations_after = engine.get_document_taxon_validations()
            print(f"✓ After process_and_save(): engine has {len(validations_after)} validations")
            assert len(validations_after) == 2, f"Engine should have 2 validations after process_and_save(), got {len(validations_after)}"

            # Verify the validations are the same ones from the document
            print("\nValidation details:")
            for i, val in enumerate(validations_after):
                print(f"\n  Validation {i+1}:")
                print(f"    Taxonomy Ref: {val.taxonomy_ref}")
                print(f"    Taxon Path: {val.taxon_path}")
                if val.validation:
                    print(f"    Name: {val.validation.get('name', 'N/A')}")
                    print(f"    Exception ID: {val.validation.get('exceptionId', 'N/A')}")

            # Verify the exception IDs match what we set
            exception_ids = [v.validation.get('exceptionId') for v in validations_after if v.validation]
            assert 'test-validation-1' in exception_ids, "Should find test-validation-1"
            assert 'test-validation-2' in exception_ids, "Should find test-validation-2"

            print("\n✓ Validations match expected values")

        doc.close()
        print("\n✓ Test completed successfully")

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        raise


@pytest.mark.skipif(not EXTRACTION_AVAILABLE, reason="Extraction engine not available")
def test_engine_validations_no_duplicates():
    """
    Test that validations are not duplicated when processing multiple root objects.

    This mirrors the Go test:
      lib/go/integration/extraction_engine_get_validations_test.go::TestExtractionEngine_GetDocumentTaxonValidations_NoDuplicates

    Verifies:
    1. Validations are copied once from document to engine
    2. Multiple root objects don't cause duplicate validations
    """

    # Get paths to test files
    repo_root = Path(__file__).parent.parent.parent.parent
    kddb_path = repo_root / "test_extractions" / "validations" / "input.kddb"
    taxonomy_path = repo_root / "test_extractions" / "validations" / "taxonomy.json"

    # Verify files exist
    if not kddb_path.exists():
        pytest.skip(f"Test KDDB file not found: {kddb_path}")
    if not taxonomy_path.exists():
        pytest.skip(f"Test taxonomy file not found: {taxonomy_path}")

    try:
        # Load the document
        doc = Document.from_kddb(str(kddb_path))

        # Load the taxonomy
        with open(taxonomy_path, 'r') as f:
            taxonomy_data = json.load(f)

        # Create a single validation
        validation = {
            "taxonomyRef": taxonomy_data["ref"],
            "taxonPath": "Invoice/MasterAccountNumber",
            "validation": {
                "name": "Single Validation",
                "ruleFormula": "1=1",
                "messageFormula": '"Test message"',
                "exceptionId": "single-validation"
            }
        }

        # Add validation to the document
        doc.set_validations([validation])

        # Create extraction engine and run extraction
        with ExtractionEngine(doc, [taxonomy_data]) as engine:
            count = engine.process_and_save()
            print(f"✓ Extraction produced {count} data objects")

            # The engine should have exactly 1 validation, not N validations for N root objects
            validations = engine.get_document_taxon_validations()
            print(f"✓ Engine has {len(validations)} validation(s)")

            assert len(validations) == 1, \
                f"Engine should have exactly 1 validation (not duplicated per root object), got {len(validations)}"

            # Verify it's the correct validation
            assert validations[0].validation.get('exceptionId') == 'single-validation'
            print("✓ Validation is correct (no duplicates)")

        doc.close()
        print("\n✓ No-duplicates test completed successfully")

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    # Allow running this test directly
    if EXTRACTION_AVAILABLE:
        print("Running test_engine_get_document_taxon_validations...")
        test_engine_get_document_taxon_validations()
        print("\n" + "="*60)
        print("Running test_engine_validations_no_duplicates...")
        test_engine_validations_no_duplicates()
        print("\n" + "="*60)
        print("All tests passed!")
    else:
        print("Extraction engine not available")
