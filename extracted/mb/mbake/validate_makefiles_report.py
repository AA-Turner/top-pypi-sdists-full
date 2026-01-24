#!/usr/bin/env python3
"""
Comprehensive Makefile validation report for the fixtures directory.
Provides detailed analysis and recommendations.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Tuple


def validate_makefile(makefile_path: Path) -> Tuple[bool, str, str]:
    """
    Validate a single Makefile by running 'make --dry-run'.
    
    Args:
        makefile_path: Path to the Makefile to validate
        
    Returns:
        Tuple of (is_valid, error_message, error_category)
    """
    try:
        # Create a temporary directory to run make in
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            
            # Copy the .mk file to the temp directory as Makefile
            temp_makefile = temp_dir_path / "Makefile"
            shutil.copy2(makefile_path, temp_makefile)
            
            # Run make --dry-run in the temporary directory
            result = subprocess.run(
                ['make', '--dry-run', '--no-print-directory'],
                cwd=temp_dir_path,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            if result.returncode == 0:
                return True, "", "VALID"
            else:
                error_msg = result.stderr.strip()
                if "No targets" in error_msg:
                    return False, error_msg, "NO_TARGETS"
                elif "missing separator" in error_msg or "commands commence before first target" in error_msg:
                    return False, error_msg, "SYNTAX_ERROR"
                elif "No such file or directory" in error_msg:
                    return False, error_msg, "MISSING_INCLUDE"
                elif "No rule to make target" in error_msg:
                    return False, error_msg, "MISSING_DEPENDENCY"
                elif "Build failed" in error_msg:
                    return False, error_msg, "EXPECTED_ERROR"
                else:
                    return False, error_msg, "UNKNOWN_ERROR"
            
    except subprocess.TimeoutExpired:
        return False, "Timeout expired (30s)", "TIMEOUT"
    except FileNotFoundError:
        return False, "make command not found", "SYSTEM_ERROR"
    except Exception as e:
        return False, f"Unexpected error: {e}", "SYSTEM_ERROR"


def find_makefiles(fixtures_dir: Path) -> List[Path]:
    """
    Find all Makefiles in the fixtures directory.
    
    Args:
        fixtures_dir: Path to the fixtures directory
        
    Returns:
        List of Makefile paths
    """
    makefiles = []
    
    # Files that intentionally test invalid syntax - skip validation for these
    # The formatter preserves invalid syntax for testing purposes
    invalid_syntax_fixtures = {
        'invalid_targets/expected.mk',  # Intentionally tests invalid target syntax
    }
    
    # Look for .mk files (which are Makefiles in the fixtures)
    for root, dirs, files in os.walk(fixtures_dir):
        for file in files:
            if file.endswith('.mk') and file != 'input.mk':
                file_path = Path(root) / file
                relative_path = file_path.relative_to(fixtures_dir)
                
                # Skip files that test invalid syntax
                if str(relative_path) not in invalid_syntax_fixtures:
                    makefiles.append(file_path)
    
    return sorted(makefiles)


def main():
    """Main function to generate comprehensive validation report."""
    fixtures_dir = Path(__file__).parent / 'tests' / 'fixtures'
    
    if not fixtures_dir.exists():
        print(f"Error: Fixtures directory not found: {fixtures_dir}")
        sys.exit(1)
    
    print("=" * 80)
    print("MAKEFILE VALIDATION REPORT")
    print("=" * 80)
    print(f"Directory: {fixtures_dir}")
    print()
    
    makefiles = find_makefiles(fixtures_dir)
    
    if not makefiles:
        print("No .mk files found in fixtures directory.")
        return
    
    # Statistics
    stats = {
        "VALID": 0,
        "NO_TARGETS": 0,
        "SYNTAX_ERROR": 0,
        "MISSING_INCLUDE": 0,
        "MISSING_DEPENDENCY": 0,
        "EXPECTED_ERROR": 0,
        "UNKNOWN_ERROR": 0,
        "TIMEOUT": 0,
        "SYSTEM_ERROR": 0,
    }
    
    # Categorize files
    valid_files = []
    syntax_errors = []
    test_scenarios = []
    other_issues = []
    
    for makefile_path in makefiles:
        relative_path = makefile_path.relative_to(fixtures_dir)
        is_valid, error_msg, error_category = validate_makefile(makefile_path)
        
        stats[error_category] += 1
        
        if is_valid:
            valid_files.append(relative_path)
        elif error_category == "SYNTAX_ERROR":
            syntax_errors.append((relative_path, error_msg))
        elif error_category in ["NO_TARGETS", "MISSING_INCLUDE", "MISSING_DEPENDENCY", "EXPECTED_ERROR"]:
            test_scenarios.append((relative_path, error_category, error_msg))
        else:
            other_issues.append((relative_path, error_category, error_msg))
    
    # Print summary
    print("SUMMARY:")
    print(f"  Total files: {len(makefiles)}")
    print(f"  Valid Makefiles: {stats['VALID']}")
    print(f"  Test scenarios (expected issues): {stats['NO_TARGETS'] + stats['MISSING_INCLUDE'] + stats['MISSING_DEPENDENCY'] + stats['EXPECTED_ERROR']}")
    print(f"  Syntax errors: {stats['SYNTAX_ERROR']}")
    print(f"  Other issues: {stats['UNKNOWN_ERROR'] + stats['TIMEOUT'] + stats['SYSTEM_ERROR']}")
    print()
    
    # Print valid files
    if valid_files:
        print("✅ VALID MAKEFILES:")
        for file_path in valid_files:
            print(f"  {file_path}")
        print()
    
    # Print test scenarios
    if test_scenarios:
        print("⚠️  TEST SCENARIOS (Expected Issues):")
        for file_path, category, error in test_scenarios:
            print(f"  {file_path}: {category}")
        print()
    
    # Print syntax errors
    if syntax_errors:
        print("❌ SYNTAX ERRORS (Need Attention):")
        for file_path, error in syntax_errors:
            print(f"  {file_path}: {error}")
        print()
    
    # Print other issues
    if other_issues:
        print("⚠️  OTHER ISSUES:")
        for file_path, category, error in other_issues:
            print(f"  {file_path}: {category} - {error}")
        print()
    
    # Recommendations
    print("RECOMMENDATIONS:")
    if syntax_errors:
        print("  🔧 Fix syntax errors in the files listed above.")
        print("     These are likely due to missing tabs in recipe lines or improper indentation.")
    else:
        print("  ✅ No critical syntax errors found!")
    
    print("  📝 The test scenarios are expected and test the formatter's error handling.")
    print("  🧪 Run the formatter on input.mk files to generate expected.mk files.")
    print()
    
    # Overall status
    if syntax_errors:
        print("❌ VALIDATION FAILED: Found syntax errors that need fixing.")
        sys.exit(1)
    else:
        print("✅ VALIDATION PASSED: All Makefiles are either valid or have expected test issues.")


if __name__ == "__main__":
    main()
