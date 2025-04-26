from .test_base import FileBasedTests, generate_test_cases


# Generating real TestCase classes for each importable backend
from ._test_async_types_coroutine import *  # @UnusedWildImport
generate_test_cases(globals(), 'AsyncTypesCoroutine', '_async', FileBasedTests)
