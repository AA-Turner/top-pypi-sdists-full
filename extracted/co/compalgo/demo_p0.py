#!/usr/bin/env python3
"""
P0 Demo: Scan → Verdict → Anchor → Verify

This script demonstrates the full P0 flow:
1. Scan a vulnerable contract
2. Generate a Compliance Verdict
3. Anchor the verdict on Algorand testnet
4. Verify the verdict against the TXID
"""
import os
import sys
import json

# Set up environment
os.environ.setdefault("ALGORAND_API_URL", "https://testnet-api.algonode.cloud")

from compalgo.analyzer.checker import ComplianceChecker
from compalgo.core.verdict import build_verdict
from compalgo.client import CompliLedgerClient

print("=" * 70)
print("CompALGO - Algorand Smart Contract Compliance Analyzer")
print("=" * 70)

# Step 1: Scan the vulnerable contract
print("\n[Step 1] Scanning vulnerable contract...")
contract_path = "examples/vulnerable_escrow.py"

checker = ComplianceChecker(policy_pack="algorand-baseline", threshold=80)
result = checker.check_file(contract_path)

print(f"Contract: {contract_path}")
print(f"Score: {result.score}/100")
print(f"Passed: {'✅' if result.passed else '❌'}")
print(f"Violations: {len(result.violations)}")

for v in result.violations:
    print(f"  - [{v['severity'].upper()}] {v['rule_id']}: {v['message']}")

# Step 2: Build Compliance Verdict
print("\n[Step 2] Building Compliance Verdict...")
verdict = build_verdict(
    contract=contract_path,
    violations=result.violations,
    framework="SOC2",
    control_id="CC6.1",
    fail_on="medium",
)

print(f"Framework: {verdict.framework}:{verdict.control_id}")
print(f"Status: {verdict.status}")
print(f"Severity: {verdict.severity}")
print(f"Rules Triggered: {', '.join(verdict.rules_triggered)}")
print(f"Verdict Hash: {verdict.hash_hex()[:16]}...")

# Save verdict to file
verdict_file = "verdict_p0_demo.json"
with open(verdict_file, "w") as f:
    json.dump(verdict.model_dump(), f, indent=2)
print(f"Saved to: {verdict_file}")

# Step 3: Anchor on Algorand
mnemonic = os.getenv("ALGORAND_MNEMONIC")
if not mnemonic:
    print("\n⚠️  ALGORAND_MNEMONIC not set. Skipping anchor step.")
    print("Set ALGORAND_MNEMONIC to complete the full demo.")
    sys.exit(0)

print("\n[Step 3] Anchoring verdict on Algorand testnet...")
client = CompliLedgerClient(
    algod_url=os.getenv("ALGORAND_API_URL"),
    algod_token="",
    sender_mnemonic=mnemonic,
    network="testnet",
)

anchor_result = client.mint_verdict(verdict)
print(f"✅ Anchored!")
print(f"TXID: {anchor_result.txid}")
print(f"Explorer: {anchor_result.explorer_url}")

# Step 4: Verify
print("\n[Step 4] Verifying verdict against blockchain...")
is_valid = client.verify_verdict(verdict, anchor_result.txid)
print(f"Verification: {'✅ VALID' if is_valid else '❌ INVALID'}")

print("\n" + "=" * 70)
print("🎉 P0 Demo Complete!")
print("=" * 70)
print(f"\nYour proof is permanently anchored on Algorand:")
print(f"  {anchor_result.explorer_url}")
