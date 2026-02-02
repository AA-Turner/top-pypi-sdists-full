"""
Integration test for extraction engine validation functionality.

This test mirrors the Go integration test:
  lib/go/integration/extraction_engine_validations_test.go::TestExtractionEngine_TestValidations

It validates that:
1. Extraction engine processes validation rules correctly
2. DataExceptions are created when validation rules fail
3. The Document.get_all_data_exceptions() method retrieves all exceptions
"""

import json
import pytest
from pathlib import Path

try:
    from kodexa_document import Document, ExtractionEngine, DataException
    EXTRACTION_AVAILABLE = True
except ImportError:
    EXTRACTION_AVAILABLE = False


@pytest.mark.skipif(not EXTRACTION_AVAILABLE, reason="Extraction engine not available")
def test_validations_extraction():
    """
    Test extraction with validation rules using validations/input.kddb.

    This test uses the same test data as the Go integration test:
    - KDDB: test_extractions/validations/input.kddb
    - Taxonomy: test_extractions/validations/taxonomy.json
    - Expected: test_extractions/validations/input.kddb.json

    The test verifies:
    1. Extraction completes successfully
    2. DataExceptions are created for validation failures and persisted
    3. get_all_data_exceptions() returns all exceptions from the database
    4. The expected validation exception is present with correct details
    """

    # Get paths to test files
    repo_root = Path(__file__).parent.parent.parent.parent
    kddb_path = repo_root / "test_extractions" / "validations" / "input.kddb"
    taxonomy_path = repo_root / "test_extractions" / "validations" / "taxonomy.json"
    expected_json_path = repo_root / "test_extractions" / "validations" / "input.kddb.json"

    # Verify files exist
    if not kddb_path.exists():
        pytest.skip(f"Test KDDB file not found: {kddb_path}")
    if not taxonomy_path.exists():
        pytest.skip(f"Test taxonomy file not found: {taxonomy_path}")
    if not expected_json_path.exists():
        pytest.skip(f"Expected JSON file not found: {expected_json_path}")

    try:
        # Load the document
        doc = Document.from_kddb(str(kddb_path))
        print(f"✓ Loaded document from {kddb_path.name}")

        # Load the taxonomy
        with open(taxonomy_path, 'r') as f:
            taxonomy_data = json.load(f)
        print(f"✓ Loaded taxonomy: {taxonomy_data.get('name', 'Unknown')}")

        # Create extraction engine
        with ExtractionEngine(doc, [taxonomy_data]) as engine:
            print("✓ Created extraction engine with validation taxonomy")

            # Run extraction and save results to database
            count = engine.process_and_save()
            print(f"✓ Extraction completed successfully")
            print(f"✓ Extracted {count} data objects")

            # Verify we extracted data objects
            assert isinstance(count, int), "process_and_save() should return an int"
            assert count > 0, "Should extract at least one data object"

            # Test doc.get_all_data_exceptions() method
            # Since process_and_save() persists DataObjects to the database,
            # their exceptions should now be retrievable
            all_exceptions = doc.get_all_data_exceptions()
            print(f"✓ doc.get_all_data_exceptions() returned {len(all_exceptions)} exceptions (from persisted DataObjects)")

            # Should have 2 validation exceptions (Python behavior):
            # - 1 validation exception for MasterAccountNumber != BillToName
            # - 1 validation exception for Barcode is required
            #
            # NOTE: Go test finds only 1 exception (MasterAccountNumber) because:
            # - Go test sets DocumentFamily.Path = "HelloPath" before extraction
            # - Barcode attribute uses valuePath="METADATA" and metadataValue="FILENAME"
            # - This populates Barcode from DocumentFamily.Path, so validation passes
            # - Python test doesn't set DocumentFamily (no Python binding exists yet)
            # - So Barcode remains blank and fails validation
            assert len(all_exceptions) == 2, f"Expected 2 DataExceptions, got {len(all_exceptions)}"
            print("✓ Correct number of exceptions (2 validation failures)")

            # Find and verify the expected validation exceptions
            found_master_account = False
            found_barcode = False

            for exc in all_exceptions:
                assert isinstance(exc, DataException), "Should return DataException objects"

                if exc.message == "Master Account Number and Bill To Name must be different":
                    found_master_account = True
                    assert exc.severity == "HIGH", "Validation exception should have HIGH severity"
                    assert exc.open is True, "Validation exception should be open"
                    assert exc.path is not None, "Validation exception should have a path"
                    assert exc.path == "Invoice/MasterAccountNumber", f"Expected path 'Invoice/MasterAccountNumber', got '{exc.path}'"
                    print(f"✓ Found MasterAccountNumber validation exception:")
                    print(f"    Message: {exc.message}")
                    print(f"    Severity: {exc.severity}")
                    print(f"    Path: {exc.path}")
                    print(f"    Open: {exc.open}")

                elif exc.message == "Barcode is required":
                    found_barcode = True
                    assert exc.severity == "HIGH", "Barcode validation exception should have HIGH severity"
                    assert exc.open is True, "Barcode validation exception should be open"
                    assert exc.path is not None, "Barcode validation exception should have a path"
                    assert exc.path == "Invoice/Barcode", f"Expected path 'Invoice/Barcode', got '{exc.path}'"
                    print(f"✓ Found Barcode validation exception:")
                    print(f"    Message: {exc.message}")
                    print(f"    Severity: {exc.severity}")
                    print(f"    Path: {exc.path}")
                    print(f"    Open: {exc.open}")

            assert found_master_account, "Should find the MasterAccountNumber validation exception"
            assert found_barcode, "Should find the Barcode validation exception"

            # Verify exception types
            print("\nDataException breakdown:")
            print(f"  - 2 validation failures (HIGH, open)")
            print(f"  = 2 total exceptions")

        doc.close()
        print("\n✓ Validation extraction test completed successfully")

    except Exception as e:
        print(f"\n✗ Validation extraction test failed: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    # Allow running this test directly
    if EXTRACTION_AVAILABLE:
        test_validations_extraction()
        print("\n" + "="*60)
        print("All validation tests passed!")
    else:
        print("Extraction engine not available")
