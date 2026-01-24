#!/usr/bin/env python3
"""
Simple test runner for P0 tests
"""
import sys
import os

# Add parent dir to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

print("=" * 60)
print("CompliLedger Algorand SDK - P0 Test Suite")
print("=" * 60)

print("\n[1/4] Testing Verdict schema and hashing...")
from tests.test_verdict import *
test_verdict_canonical_json()
test_verdict_hash_deterministic()
test_verdict_hash_changes_with_content()
test_build_verdict()
print("✅ Verdict tests passed")

print("\n[2/4] Testing Parsers...")
from tests.test_parser import *
test_pyteal_parser_extract_signals()
test_teal_parser_extract_opcodes()
test_teal_parser_rekey_detection()
print("✅ Parser tests passed")

print("\n[3/4] Testing Checker and rule engine...")
from tests.test_checker import *
test_checker_detects_violations()
test_checker_score_calculation()
test_checker_teal_file()
print("✅ Checker tests passed")

print("\n[4/4] Testing E2E anchor and verify...")
if os.getenv("ALGORAND_MNEMONIC"):
    from tests.test_e2e_anchor import test_e2e_anchor_and_verify
    test_e2e_anchor_and_verify()
    print("✅ E2E tests passed")
else:
    print("⚠️  SKIPPED: Set ALGORAND_MNEMONIC to run E2E tests")

print("\n" + "=" * 60)
print("🎉 All tests PASSED!")
print("=" * 60)
