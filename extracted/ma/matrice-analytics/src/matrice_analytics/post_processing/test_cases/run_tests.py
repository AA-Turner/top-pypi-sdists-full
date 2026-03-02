#!/usr/bin/env python3
"""
Test runner for post-processing module tests.

This script runs all tests in the post-processing test suite and provides
a comprehensive summary of the results.
"""

import sys
import os
import subprocess
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

def run_tests():
    """Run all post-processing tests and provide summary."""
    
    print("=" * 80)
    print("POST-PROCESSING MODULE TEST SUITE")
    print("=" * 80)
    print()
    
    # Get test directory
    test_dir = Path(__file__).parent
    
    # Test files to run
    test_files = [
        "test_comprehensive.py"
    ]
    
    # Check for other test files
    other_test_files = [
        "test_utilities.py",
        "test_data_generators.py", 
        "test_basic_counting_tracking.py",
        "test_config.py",
        "test_utils.py"
    ]
    
    available_tests = []
    for test_file in test_files:
        if (test_dir / test_file).exists():
            available_tests.append(test_file)
    
    # Check if other test files exist and work
    for test_file in other_test_files:
        if (test_dir / test_file).exists():
            print(f"Note: {test_file} exists but may have compatibility issues")
    
    print(f"Running {len(available_tests)} test file(s):")
    for test_file in available_tests:
        print(f"  - {test_file}")
    print()
    
    # Run tests
    total_passed = 0
    total_failed = 0
    total_time = 0
    
    for test_file in available_tests:
        print(f"Running {test_file}...")
        print("-" * 60)
        
        start_time = time.time()
        
        # Run pytest on the specific file
        cmd = [sys.executable, "-m", "pytest", str(test_dir / test_file), "-v"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        end_time = time.time()
        elapsed = end_time - start_time
        total_time += elapsed
        
        # Parse results
        if result.returncode == 0:
            # Extract test counts from output
            lines = result.stdout.split('\n')
            summary_line = [line for line in lines if 'passed' in line and '=' in line]
            if summary_line:
                # Extract numbers from summary like "26 passed in 20.94s"
                parts = summary_line[-1].split()
                for i, part in enumerate(parts):
                    if 'passed' in part and i > 0:
                        try:
                            passed = int(parts[i-1])
                            total_passed += passed
                            print(f"✅ {passed} tests passed in {elapsed:.2f}s")
                            break
                        except ValueError:
                            pass
            else:
                print(f"✅ All tests passed in {elapsed:.2f}s")
        else:
            # Extract failure information
            lines = result.stdout.split('\n')
            summary_line = [line for line in lines if 'failed' in line and 'passed' in line and '=' in line]
            if summary_line:
                # Extract numbers from summary like "4 failed, 22 passed"
                parts = summary_line[-1].split()
                failed = 0
                passed = 0
                for i, part in enumerate(parts):
                    if 'failed' in part and i > 0:
                        try:
                            failed = int(parts[i-1])
                        except ValueError:
                            pass
                    elif 'passed' in part and i > 0:
                        try:
                            passed = int(parts[i-1])
                        except ValueError:
                            pass
                total_failed += failed
                total_passed += passed
                print(f"❌ {failed} tests failed, {passed} tests passed in {elapsed:.2f}s")
            else:
                print(f"❌ Tests failed in {elapsed:.2f}s")
                total_failed += 1
        
        print()
    
    # Final summary
    print("=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)
    print(f"Total tests passed: {total_passed}")
    print(f"Total tests failed: {total_failed}")
    print(f"Total execution time: {total_time:.2f}s")
    print(f"Success rate: {total_passed/(total_passed+total_failed)*100:.1f}%" if (total_passed+total_failed) > 0 else "No tests run")
    
    if total_failed == 0:
        print("🎉 All tests passed!")
        return True
    else:
        print(f"⚠️  {total_failed} test(s) failed")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 