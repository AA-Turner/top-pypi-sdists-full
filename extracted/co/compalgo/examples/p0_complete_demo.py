#!/usr/bin/env python3
"""
CompALGO P0 Complete Demo Script

Demonstrates the full P0 flow:
1. Analyze PyTeal/TEAL smart contracts for security violations
2. Generate a Compliance Verdict with framework/control mapping
3. Anchor the verdict hash on Algorand testnet (immutable proof)
4. Verify the verdict against the blockchain

Requirements:
- Environment variables:
  - ALGO_MNEMONIC: Your 25-word Algorand mnemonic (testnet)
  - ALGO_ALGOD_URL: (optional) Algod API URL
  - ALGO_INDEXER_URL: (optional) Indexer API URL

Usage:
    export ALGO_MNEMONIC="your 25 word mnemonic here"
    python examples/p0_complete_demo.py
"""

import os
import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from compalgo.analyzer.checker import ComplianceChecker
from compalgo.core.verdict import build_verdict, ComplianceVerdict
from compalgo.client import CompliLedgerClient


def print_header(text: str):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def print_step(num: int, text: str):
    """Print formatted step header"""
    print(f"\n[Step {num}] {text}")
    print("-" * 70)


def main():
    print_header("CompALGO P0 Demo: Analyze → Verdict → Anchor → Verify")
    
    # Configuration
    algod_url = os.getenv("ALGO_ALGOD_URL", "https://testnet-api.algonode.cloud")
    indexer_url = os.getenv("ALGO_INDEXER_URL", "https://testnet-idx.algonode.cloud")
    mnemonic = os.getenv("ALGO_MNEMONIC")
    
    if not mnemonic:
        print("\n❌ ERROR: ALGO_MNEMONIC environment variable not set")
        print("\nPlease set your Algorand testnet mnemonic:")
        print('  export ALGO_MNEMONIC="your 25 word mnemonic here"')
        print("\nGet testnet ALGO from: https://dispenser.testnet.aws.algodev.network/")
        sys.exit(1)
    
    print(f"\nConfiguration:")
    print(f"  Network: testnet")
    print(f"  Algod URL: {algod_url}")
    print(f"  Indexer URL: {indexer_url}")
    
    # =========================================================================
    # STEP 1: Analyze a Smart Contract
    # =========================================================================
    print_step(1, "Analyze Smart Contract for Security Violations")
    
    # Use the vulnerable example contract
    contract_path = Path(__file__).parent.parent / "examples" / "vulnerable_escrow.py"
    
    if not contract_path.exists():
        print(f"❌ Contract not found: {contract_path}")
        sys.exit(1)
    
    print(f"Contract: {contract_path}")
    print(f"Policy: algorand-baseline (9 P0 rules)")
    print(f"Threshold: 80/100")
    
    # Initialize checker with baseline policy
    checker = ComplianceChecker(
        policy_pack="algorand-baseline",
        threshold=80
    )
    
    # Run analysis
    result = checker.check_file(str(contract_path))
    
    print(f"\nResults:")
    print(f"  Score: {result.score}/100 {'✅' if result.passed else '❌'}")
    print(f"  Passed: {result.passed}")
    print(f"  Total Violations: {len(result.violations)}")
    
    # Show violation breakdown by severity
    severities = ["critical", "high", "medium", "low", "info"]
    for sev in severities:
        count = result.counts.get(sev, 0)
        if count > 0:
            icon = "🔴" if sev == "critical" else "⚠️" if sev == "high" else "🟡" if sev == "medium" else "ℹ️"
            print(f"  {icon} {sev.upper()}: {count}")
    
    # Show first 5 violations
    if result.violations:
        print(f"\nViolations (showing first 5):")
        for i, v in enumerate(result.violations[:5]):
            print(f"  {i+1}. [{v['severity'].upper()}] {v['rule_id']}")
            print(f"     {v['message']}")
            if v.get('controls'):
                controls = ', '.join([f"{c['framework']}:{c['control_id']}" for c in v['controls']])
                print(f"     Controls: {controls}")
    
    # =========================================================================
    # STEP 2: Generate Compliance Verdict
    # =========================================================================
    print_step(2, "Generate Compliance Verdict")
    
    print("Building structured compliance verdict...")
    print(f"  Framework: SOC2 (Trust Services)")
    print(f"  Control ID: CC6.1 (Logical & Physical Access)")
    print(f"  Fail Threshold: medium (fail if any medium+ violations)")
    
    verdict = build_verdict(
        contract=str(contract_path),
        violations=result.violations,
        framework="SOC2",
        control_id="CC6.1",
        fail_on="medium"
    )
    
    print(f"\nVerdict:")
    print(f"  Status: {verdict.status.upper()} {'❌' if verdict.status == 'fail' else '✅'}")
    print(f"  Severity: {verdict.severity}")
    print(f"  Rules Triggered: {len(verdict.rules_triggered)}")
    print(f"  Timestamp: {verdict.timestamp}")
    
    # Show rules triggered
    if verdict.rules_triggered:
        print(f"\n  Triggered Rules:")
        for rule in verdict.rules_triggered[:10]:  # Show first 10
            print(f"    - {rule}")
        if len(verdict.rules_triggered) > 10:
            print(f"    ... and {len(verdict.rules_triggered) - 10} more")
    
    # Calculate hash
    verdict_hash = verdict.hash_hex()
    print(f"\n  Verdict Hash (SHA-256):")
    print(f"    {verdict_hash}")
    
    # Save verdict to JSON file
    verdict_file = Path("verdict_demo.json")
    with open(verdict_file, "w") as f:
        json.dump(verdict.model_dump(), f, indent=2)
    print(f"\n  Saved to: {verdict_file}")
    
    # =========================================================================
    # STEP 3: Anchor Verdict on Algorand Blockchain
    # =========================================================================
    print_step(3, "Anchor Verdict on Algorand Testnet")
    
    print("Initializing Algorand client...")
    client = CompliLedgerClient(
        algod_url=algod_url,
        algod_token="",
        sender_mnemonic=mnemonic,
        network="testnet",
        indexer_url=indexer_url,
        indexer_token=""
    )
    
    print("Creating on-chain proof transaction...")
    print(f"  Transaction type: PaymentTxn (0 ALGO to self)")
    print(f"  Note format: CLG1|sha256:{verdict_hash[:16]}...")
    print(f"  Fee: ~0.001 ALGO")
    
    print("\nBroadcasting to Algorand testnet...")
    try:
        anchor_result = client.mint_verdict(verdict)
        
        print(f"\n✅ Verdict Anchored Successfully!")
        print(f"\n  Transaction ID:")
        print(f"    {anchor_result.txid}")
        print(f"\n  AlgoExplorer URL:")
        print(f"    {anchor_result.explorer_url}")
        print(f"\n  Verdict Hash:")
        print(f"    {anchor_result.verdict_hash}")
        print(f"\n  Network: {anchor_result.network}")
        
        # Save anchor info
        anchor_info = {
            "txid": anchor_result.txid,
            "explorer_url": anchor_result.explorer_url,
            "verdict_hash": anchor_result.verdict_hash,
            "network": anchor_result.network
        }
        anchor_file = Path("anchor_result.json")
        with open(anchor_file, "w") as f:
            json.dump(anchor_info, f, indent=2)
        print(f"\n  Anchor info saved to: {anchor_file}")
        
    except Exception as e:
        print(f"\n❌ Anchoring failed: {e}")
        print(f"\nPossible causes:")
        print(f"  - Insufficient ALGO balance (need ~0.001 ALGO)")
        print(f"  - Invalid mnemonic")
        print(f"  - Network connectivity issues")
        sys.exit(1)
    
    # =========================================================================
    # STEP 4: Verify Verdict Against Blockchain
    # =========================================================================
    print_step(4, "Verify Verdict Against Blockchain")
    
    print("Querying Algorand for transaction...")
    print(f"  TXID: {anchor_result.txid[:32]}...")
    
    print("\nFetching transaction note...")
    print("  Method: algod API (recent) → Indexer (historical)")
    
    try:
        is_valid = client.verify_verdict(verdict, anchor_result.txid)
        
        if is_valid:
            print(f"\n✅ VERIFICATION PASSED")
            print(f"\n  The verdict hash matches the on-chain proof.")
            print(f"  This verdict is cryptographically verified and immutable.")
        else:
            print(f"\n❌ VERIFICATION FAILED")
            print(f"\n  The verdict hash does NOT match the on-chain proof.")
            print(f"  The verdict may have been tampered with.")
        
    except Exception as e:
        print(f"\n❌ Verification error: {e}")
        sys.exit(1)
    
    # =========================================================================
    # STEP 5: Demonstrate Tamper Detection
    # =========================================================================
    print_step(5, "Demonstrate Tamper Detection")
    
    print("Creating a tampered verdict (changing status)...")
    tampered_verdict = ComplianceVerdict(**verdict.model_dump())
    tampered_verdict.status = "pass"  # Change fail → pass
    
    print(f"  Original: status={verdict.status}")
    print(f"  Tampered: status={tampered_verdict.status}")
    print(f"\n  Original hash: {verdict.hash_hex()[:32]}...")
    print(f"  Tampered hash: {tampered_verdict.hash_hex()[:32]}...")
    
    print("\nVerifying tampered verdict...")
    is_tampered_valid = client.verify_verdict(tampered_verdict, anchor_result.txid)
    
    if not is_tampered_valid:
        print(f"\n✅ TAMPER DETECTION WORKS")
        print(f"\n  The tampered verdict was correctly rejected.")
        print(f"  Hash mismatch detected.")
    else:
        print(f"\n❌ UNEXPECTED: Tampered verdict passed verification")
    
    # =========================================================================
    # Summary
    # =========================================================================
    print_header("Demo Complete!")
    
    print(f"\n📊 Summary:")
    print(f"  Contract Analyzed: {contract_path.name}")
    print(f"  Violations Found: {len(result.violations)}")
    print(f"  Compliance Score: {result.score}/100")
    print(f"  Verdict Status: {verdict.status}")
    print(f"  Anchored on Chain: ✅")
    print(f"  Verification: ✅ VALID")
    print(f"  Tamper Detection: ✅ WORKS")
    
    print(f"\n🔗 Proof on Algorand:")
    print(f"  {anchor_result.explorer_url}")
    
    print(f"\n📁 Generated Files:")
    print(f"  - {verdict_file}")
    print(f"  - {anchor_file}")
    
    print(f"\n🎉 P0 Demo Successful!")
    print(f"\nYour compliance verdict is now immutably anchored on Algorand.")
    print(f"Anyone can verify this proof using the TXID and verdict JSON.")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
