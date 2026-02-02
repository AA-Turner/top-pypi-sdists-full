#!/usr/bin/env python3
"""
Test runner for stdio mode and hooks functionality

This script runs all stdio and hooks related tests to ensure functionality.
"""

import sys
import subprocess
import pytest
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def run_stdio_tests():
    """Run stdio mode tests"""
    print("=" * 60)
    print("Running stdio mode tests...")
    print("=" * 60)
    
    result = subprocess.run([
        "python", "-m", "pytest", 
        "-m", "stdio",
        "--tb=short"
    ], cwd=Path(__file__).parent.parent)
    
    return result.returncode == 0


def run_hooks_tests():
    """Run hooks functionality tests"""
    print("=" * 60)
    print("Running hooks functionality tests...")
    print("=" * 60)
    
    result = subprocess.run([
        "python", "-m", "pytest", 
        "-m", "hooks",
        "--tb=short"
    ], cwd=Path(__file__).parent.parent)
    
    return result.returncode == 0


def run_integration_tests():
    """Run stdio + hooks integration tests"""
    print("=" * 60)
    print("Running stdio + hooks integration tests...")
    print("=" * 60)
    
    result = subprocess.run([
        "python", "-m", "pytest", 
        "-m", "stdio and hooks",
        "--tb=short"
    ], cwd=Path(__file__).parent.parent)
    
    return result.returncode == 0


def run_quick_tests():
    """Run quick tests that don't require API keys"""
    print("=" * 60)
    print("Running quick tests (no API keys required)...")
    print("=" * 60)
    
    # Test stdio logging redirection
    from tooluniverse.logging_config import reconfigure_for_stdio
    reconfigure_for_stdio()
    print("✅ stdio logging redirection test passed")
    
    # Test hook initialization
    from tooluniverse.output_hook import SummarizationHook, HookManager
    from unittest.mock import MagicMock
    
    mock_tu = MagicMock()
    mock_tu.callable_functions = {
        "OutputSummarizer": MagicMock(),
        "OutputSummarizationComposer": MagicMock()
    }
    
    _ = SummarizationHook(
        config={"hook_config": {}},
        tooluniverse=mock_tu
    )
    print("✅ SummarizationHook initialization test passed")
    
    from tooluniverse.default_config import get_default_hook_config
    _ = HookManager(get_default_hook_config(), mock_tu)
    print("✅ HookManager initialization test passed")
    
    return True


def main():
    """Run all tests"""
    print("🧪 Running stdio mode and hooks tests...")
    print()
    
    all_passed = True
    
    # Run quick tests first
    if not run_quick_tests():
        print("❌ Quick tests failed")
        all_passed = False
    else:
        print("✅ Quick tests passed")
    
    print()
    
    # Run unit tests
    if not run_hooks_tests():
        print("❌ Hooks tests failed")
        all_passed = False
    else:
        print("✅ Hooks tests passed")
    
    print()
    
    # Run stdio tests (these might take longer)
    print("⚠️  Note: stdio tests may take several minutes due to server startup...")
    if not run_stdio_tests():
        print("❌ stdio tests failed")
        all_passed = False
    else:
        print("✅ stdio tests passed")
    
    print()
    
    # Run integration tests (these might take even longer)
    print("⚠️  Note: integration tests may take several minutes due to server startup...")
    if not run_integration_tests():
        print("❌ Integration tests failed")
        all_passed = False
    else:
        print("✅ Integration tests passed")
    
    print()
    print("=" * 60)
    if all_passed:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed!")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
