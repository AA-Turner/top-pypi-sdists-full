"""New-feature tests have been reorganized into domain-specific test modules.

Previously this file contained tests for schema caching, error handling,
progress callbacks, profiling, streaming, exports, and related utilities.
Those tests now live in:

- test_utils.py: TestErrorHandling
- test_models.py: TestBatchResult
- test_schema.py: TestSchemaCache, TestSchemaUtilities
- test_data.py: TestProgressCallbacks, TestDataOperationsWithErrorHandling,
  TestDataOperationsWithProgressCallback, TestBulkDeleteAll, TestStreamingRead
- test_files.py: TestFilesApiRefactor
- test_dealcloud.py: TestDealCloudSchemaCache, TestExports
- test_constants.py: TestFieldTypeNames, TestGetFieldTypeId
- test_profiling.py: all profiling-related test classes
- test_file_utils.py: TestFileUtilities
- test_excel_utils.py: TestExcelUtilities
"""
