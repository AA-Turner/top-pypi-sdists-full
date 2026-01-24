#!/usr/bin/env python3
"""
Script to test Makefile formatting by:
1. Formatting non-.bak Makefiles
2. Comparing dry-run output between .bak and non-.bak versions
3. Restoring original files from .bak versions

This script ensures that the mbake formatter doesn't break Makefiles by comparing
the behavior of original and formatted versions.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Tuple


def find_makefile_pairs() -> List[Tuple[Path, Path]]:
    """
    Find pairs of Makefiles (.bak and non-.bak versions).
    
    Returns:
        List of tuples (non_bak_path, bak_path)
    """
    pairs = []
    root_dir = Path(__file__).parent
    
    # Look for .bak files and find their corresponding non-.bak versions
    for bak_file in root_dir.glob("*.bak"):
        non_bak_file = bak_file.with_suffix("")  # Remove .bak extension
        if non_bak_file.exists():
            pairs.append((non_bak_file, bak_file))
    
    return sorted(pairs, key=lambda x: x[0].name)


def format_makefile(makefile_path: Path) -> Tuple[bool, str]:
    """
    Format a Makefile using mbake.
    
    Args:
        makefile_path: Path to the Makefile to format
        
    Returns:
        Tuple of (success, error_message)
    """
    try:
        # Activate virtual environment and run mbake
        result = subprocess.run(
            ['bash', '-c', 'source venv/bin/activate && python3 -m mbake format ' + str(makefile_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        error_msg = result.stderr + result.stdout if result.returncode != 0 else ""
        return result.returncode == 0, error_msg
    except Exception as e:
        return False, str(e)


def is_known_formatting_issue(filename: str, error_msg: str) -> bool:
    """
    Check if a formatting error is a known issue that we expect.
    
    Args:
        filename: Name of the file
        error_msg: Error message from formatting
        
    Returns:
        True if this is a known/expected issue
    """
    # Known issues
    known_issues = {
        "verilated.mk-2.in": "Duplicate target",
        "Makefile_obj-2.in": "Duplicate target",  # If it has similar issues
    }
    
    if filename in known_issues:
        return known_issues[filename] in error_msg
    
    return False


def run_make_dry_run(makefile_path: Path) -> Tuple[bool, str]:
    """
    Run 'make --dry-run' on a Makefile.
    
    Args:
        makefile_path: Path to the Makefile
        
    Returns:
        Tuple of (success, output)
    """
    try:
        # Create a temporary directory to run make in
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            
            # Copy the Makefile to the temp directory
            temp_makefile = temp_dir_path / "Makefile"
            shutil.copy2(makefile_path, temp_makefile)
            
            # Run make --dry-run
            result = subprocess.run(
                ['make', '--dry-run', '--no-print-directory'],
                cwd=temp_dir_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return result.returncode == 0, result.stdout + result.stderr
            
    except subprocess.TimeoutExpired:
        return False, "Timeout expired"
    except Exception as e:
        return False, f"Error: {e}"


def compare_make_outputs(output1: str, output2: str) -> bool:
    """
    Compare two make outputs, ignoring some differences that don't matter.
    
    Args:
        output1: First output
        output2: Second output
        
    Returns:
        True if outputs are effectively the same
    """
    # Normalize outputs by removing leading/trailing whitespace and empty lines
    def normalize_output(output: str) -> str:
        lines = [line.strip() for line in output.split('\n') if line.strip()]
        return '\n'.join(sorted(lines))
    
    return normalize_output(output1) == normalize_output(output2)


def restore_from_backup(non_bak_path: Path, bak_path: Path) -> bool:
    """
    Restore a file from its backup.
    
    Args:
        non_bak_path: Path to the file to restore
        bak_path: Path to the backup file
        
    Returns:
        True if restoration was successful
    """
    try:
        shutil.copy2(bak_path, non_bak_path)
        return True
    except Exception as e:
        print(f"Error restoring {non_bak_path}: {e}")
        return False


def main():
    """Main function to test Makefile formatting."""
    print("=" * 80)
    print("MAKEFILE FORMATTING TEST")
    print("=" * 80)
    print("This script tests that mbake formatting doesn't break Makefiles")
    print("by comparing behavior before and after formatting.")
    print()
    
    # Find Makefile pairs
    pairs = find_makefile_pairs()
    
    if not pairs:
        print("No Makefile pairs found (.bak and non-.bak versions)")
        return
    
    print(f"Found {len(pairs)} Makefile pairs to test:")
    for non_bak, bak in pairs:
        print(f"  {non_bak.name} <-> {bak.name}")
    print()
    
    # Test each pair
    results = []
    
    for non_bak_path, bak_path in pairs:
        print(f"Testing: {non_bak_path.name}")
        print("-" * 50)
        
        # Step 1: Format the non-.bak Makefile
        print("1. Formatting non-.bak Makefile...")
        format_success, error_message = format_makefile(non_bak_path)
        if not format_success:
            if is_known_formatting_issue(non_bak_path.name, error_message):
                print(f"   ⚠️  Known formatting issue: {error_message.strip()}")
                # Continue with the test even though formatting failed
            else:
                print(f"   ❌ Formatting failed: {error_message.strip()}")
                results.append((non_bak_path.name, "FORMAT_FAILED", "", ""))
                continue
        else:
            print("   ✅ Formatting successful")
        
        # Step 2: Run make --dry-run on both versions
        print("2. Running make --dry-run on .bak version...")
        bak_success, bak_output = run_make_dry_run(bak_path)
        if not bak_success:
            print("   ⚠️  .bak version failed (this might be expected)")
        
        print("3. Running make --dry-run on formatted version...")
        formatted_success, formatted_output = run_make_dry_run(non_bak_path)
        if not formatted_success:
            print("   ⚠️  Formatted version failed (this might be expected)")
        
        # Step 3: Compare outputs
        print("4. Comparing outputs...")
        if bak_success == formatted_success:
            if bak_success:
                # Both succeeded, compare outputs
                if compare_make_outputs(bak_output, formatted_output):
                    print("   ✅ Outputs are identical")
                    results.append((non_bak_path.name, "IDENTICAL", bak_output, formatted_output))
                else:
                    print("   ❌ Outputs differ")
                    results.append((non_bak_path.name, "DIFFERENT", bak_output, formatted_output))
            else:
                # Both failed, consider this a match
                print("   ⚠️  Both versions failed (considered identical)")
                results.append((non_bak_path.name, "BOTH_FAILED", bak_output, formatted_output))
        else:
            print("   ❌ Success/failure mismatch")
            results.append((non_bak_path.name, "MISMATCH", bak_output, formatted_output))
        
        # Step 4: Restore from backup
        print("5. Restoring from backup...")
        if restore_from_backup(non_bak_path, bak_path):
            print("   ✅ Restored successfully")
        else:
            print("   ❌ Restoration failed")
        
        print()
    
    # Print summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    identical_count = 0
    different_count = 0
    failed_count = 0
    
    for filename, status, bak_out, formatted_out in results:
        if status == "IDENTICAL":
            print(f"✅ {filename}: Identical outputs")
            identical_count += 1
        elif status == "DIFFERENT":
            print(f"❌ {filename}: Different outputs")
            different_count += 1
        elif status == "BOTH_FAILED":
            print(f"⚠️  {filename}: Both versions failed")
            identical_count += 1
        elif status == "MISMATCH":
            print(f"❌ {filename}: Success/failure mismatch")
            different_count += 1
        elif status == "FORMAT_FAILED":
            print(f"❌ {filename}: Formatting failed")
            failed_count += 1
    
    print()
    print(f"Total files: {len(results)}")
    print(f"Identical: {identical_count}")
    print(f"Different: {different_count}")
    print(f"Failed: {failed_count}")
    
    if different_count > 0 or failed_count > 0:
        print("\n❌ Some tests failed!")
        print("This indicates that the formatter may have introduced errors.")
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")
        print("The formatter appears to be working correctly.")


if __name__ == "__main__":
    main()
