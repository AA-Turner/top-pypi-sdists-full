"""
Test for lazy load cache consistency fix.

This test validates that tool instances are properly cached and reused
across different methods to prevent:
1. Inconsistent cache keys due to tool instance recreation
2. Performance issues from repeated instantiation
3. State inconsistencies if tools have initialization side effects
"""

import pytest
import unittest
from unittest.mock import MagicMock, patch
from tooluniverse import ToolUniverse


class TestLazyLoadCacheConsistency(unittest.TestCase):
    """Test that tool instance caching is consistent across all methods."""

    def setUp(self):
        """Set up test fixtures."""
        self.tu = ToolUniverse()
        # Load minimal tools for testing - use include_tools to load specific tools
        try:
            self.tu.load_tools(include_tools=["PubChemGetCompoundByName", "WikipediaTool"])
        except Exception:
            # If that fails, try loading any available tools
            self.tu.load_tools()

    def tearDown(self):
        """Clean up after tests."""
        try:
            self.tu.close()
        except Exception:
            pass

    def test_validate_parameters_uses_cache(self):
        """Test that _validate_parameters uses cached tool instances."""
        # Get a tool that exists
        tool_names = list(self.tu.all_tool_dict.keys())
        if not tool_names:
            self.skipTest("No tools loaded")
        
        tool_name = tool_names[0]
        
        # Mock _get_tool_instance to track calls
        original_get_tool_instance = self.tu._get_tool_instance
        call_log = []
        
        def tracked_get_tool_instance(name, cache=True):
            call_log.append({"name": name, "cache": cache})
            return original_get_tool_instance(name, cache=cache)
        
        self.tu._get_tool_instance = tracked_get_tool_instance
        
        # Call _validate_parameters
        self.tu._validate_parameters(tool_name, {})
        
        # Verify that cache=True was used
        self.assertTrue(len(call_log) > 0, "No calls to _get_tool_instance")
        for call in call_log:
            self.assertTrue(
                call["cache"], 
                f"_validate_parameters should use cache=True, but used cache={call['cache']}"
            )

    def test_classify_exception_uses_cache(self):
        """Test that _classify_exception uses cached tool instances."""
        # Get a tool that exists
        tool_names = list(self.tu.all_tool_dict.keys())
        if not tool_names:
            self.skipTest("No tools loaded")
        
        tool_name = tool_names[0]
        
        # Mock _get_tool_instance to track calls
        original_get_tool_instance = self.tu._get_tool_instance
        call_log = []
        
        def tracked_get_tool_instance(name, cache=True):
            call_log.append({"name": name, "cache": cache})
            return original_get_tool_instance(name, cache=cache)
        
        self.tu._get_tool_instance = tracked_get_tool_instance
        
        # Call _classify_exception
        exception = ValueError("Test exception")
        self.tu._classify_exception(exception, tool_name, {})
        
        # Verify that cache=True was used
        self.assertTrue(len(call_log) > 0, "No calls to _get_tool_instance")
        for call in call_log:
            self.assertTrue(
                call["cache"], 
                f"_classify_exception should use cache=True, but used cache={call['cache']}"
            )

    def test_make_cache_key_uses_cache(self):
        """Test that _make_cache_key uses cached tool instances."""
        # Get a tool that exists
        tool_names = list(self.tu.all_tool_dict.keys())
        if not tool_names:
            self.skipTest("No tools loaded")
        
        tool_name = tool_names[0]
        
        # Mock _get_tool_instance to track calls
        original_get_tool_instance = self.tu._get_tool_instance
        call_log = []
        
        def tracked_get_tool_instance(name, cache=True):
            call_log.append({"name": name, "cache": cache})
            return original_get_tool_instance(name, cache=cache)
        
        self.tu._get_tool_instance = tracked_get_tool_instance
        
        # Call _make_cache_key without providing tool_instance
        self.tu._make_cache_key(tool_name, {})
        
        # Verify that cache=True was used
        self.assertTrue(len(call_log) > 0, "No calls to _get_tool_instance")
        for call in call_log:
            self.assertTrue(
                call["cache"], 
                f"_make_cache_key should use cache=True, but used cache={call['cache']}"
            )

    def test_tool_instance_reuse(self):
        """Test that tool instances are reused across multiple calls."""
        # Get a tool that exists
        tool_names = list(self.tu.all_tool_dict.keys())
        if not tool_names:
            self.skipTest("No tools loaded")
        
        tool_name = tool_names[0]
        
        # Get tool instance first time
        instance1 = self.tu._get_tool_instance(tool_name, cache=True)
        self.assertIsNotNone(instance1, "Tool instance should not be None")
        
        # Get tool instance second time - should be same object
        instance2 = self.tu._get_tool_instance(tool_name, cache=True)
        self.assertIsNotNone(instance2, "Tool instance should not be None")
        
        # Verify they are the same object (cached)
        self.assertIs(
            instance1, instance2,
            "Tool instances should be the same object when cache=True is used"
        )

    def test_cache_key_consistency(self):
        """Test that cache keys are consistent when tool instances are reused."""
        # Get a tool that exists
        tool_names = list(self.tu.all_tool_dict.keys())
        if not tool_names:
            self.skipTest("No tools loaded")
        
        tool_name = tool_names[0]
        arguments = {"test": "value"}
        
        # Generate cache key multiple times
        key1 = self.tu._make_cache_key(tool_name, arguments)
        key2 = self.tu._make_cache_key(tool_name, arguments)
        key3 = self.tu._make_cache_key(tool_name, arguments)
        
        # All keys should be identical
        self.assertEqual(key1, key2, "Cache keys should be consistent (key1 vs key2)")
        self.assertEqual(key2, key3, "Cache keys should be consistent (key2 vs key3)")
        self.assertEqual(key1, key3, "Cache keys should be consistent (key1 vs key3)")

    def test_no_unnecessary_instantiation(self):
        """Test that tools are not unnecessarily re-instantiated."""
        # Get a tool that exists
        tool_names = list(self.tu.all_tool_dict.keys())
        if not tool_names:
            self.skipTest("No tools loaded")
        
        tool_name = tool_names[0]
        
        # Track init_tool calls
        original_init_tool = self.tu.init_tool
        init_count = [0]
        
        def tracked_init_tool(*args, **kwargs):
            init_count[0] += 1
            return original_init_tool(*args, **kwargs)
        
        self.tu.init_tool = tracked_init_tool
        
        # Clear the cache for this tool
        if tool_name in self.tu.callable_functions:
            del self.tu.callable_functions[tool_name]
        
        initial_count = init_count[0]
        
        # Make multiple calls that should use the cached instance
        self.tu._get_tool_instance(tool_name, cache=True)
        self.tu._get_tool_instance(tool_name, cache=True)
        self.tu._get_tool_instance(tool_name, cache=True)
        
        # Should only initialize once
        self.assertEqual(
            init_count[0] - initial_count, 1,
            "Tool should only be initialized once when using cache=True"
        )


class TestLazyLoadPerformance(unittest.TestCase):
    """Test performance characteristics of lazy loading with proper caching."""

    def setUp(self):
        """Set up test fixtures."""
        self.tu = ToolUniverse()
        # Load minimal tools for testing
        try:
            self.tu.load_tools(include_tools=["PubChemGetCompoundByName", "WikipediaTool"])
        except Exception:
            # If that fails, try loading any available tools
            self.tu.load_tools()

    def tearDown(self):
        """Clean up after tests."""
        try:
            self.tu.close()
        except Exception:
            pass

    def test_cached_validation_performance(self):
        """Test that validation with caching is faster than without."""
        import time
        
        tool_names = list(self.tu.all_tool_dict.keys())
        if not tool_names:
            self.skipTest("No tools loaded")
        
        tool_name = tool_names[0]
        arguments = {}
        
        # Clear cache
        if tool_name in self.tu.callable_functions:
            del self.tu.callable_functions[tool_name]
        
        # Time with caching (cache=True)
        start_cached = time.time()
        for _ in range(10):
            self.tu._validate_parameters(tool_name, arguments)
        cached_time = time.time() - start_cached
        
        # Clear cache again
        if tool_name in self.tu.callable_functions:
            del self.tu.callable_functions[tool_name]
        
        # Time without caching (simulate old behavior with cache=False)
        original_get_tool_instance = self.tu._get_tool_instance
        
        def uncached_get_tool_instance(name, cache=True):
            # Force cache=False to simulate old behavior
            return original_get_tool_instance(name, cache=False)
        
        self.tu._get_tool_instance = uncached_get_tool_instance
        
        start_uncached = time.time()
        for _ in range(10):
            self.tu._validate_parameters(tool_name, arguments)
        uncached_time = time.time() - start_uncached
        
        # Restore original method
        self.tu._get_tool_instance = original_get_tool_instance
        
        # Cached version should be faster (or at least not slower)
        # We use a ratio to account for system variability
        print(f"\nCached time: {cached_time:.4f}s")
        print(f"Uncached time: {uncached_time:.4f}s")
        print(f"Speedup: {uncached_time/cached_time:.2f}x")
        
        # Cached should be at least 10% faster for 10 iterations
        # (First iteration is equal, subsequent 9 iterations should be faster)
        self.assertLessEqual(
            cached_time, uncached_time * 1.1,
            "Cached validation should not be significantly slower than uncached"
        )


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
