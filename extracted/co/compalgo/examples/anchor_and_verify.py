#!/usr/bin/env python3
"""
P0 End-to-End Example: Anchor and Verify Compliance Verdict
============================================================

This script demonstrates the complete P0 flow:
1. Scan a vulnerable contract for compliance issues
2. Build a Compliance Verdict object
3. Anchor the verdict hash on Algorand TestNet
4. Verify the verdict against the on-chain transaction

Configuration:
- Reads from .env file (ALGO_MNEMONIC, ALGOD_URL, INDEXER_URL, ALGO_NETWORK)
- No system-level environment variables needed
- Safe for Windows PowerShell

Requirements:
- .env file with ALGO_MNEMONIC set to your Pera TestNet wallet mnemonic
- TestNet ALGO in your wallet (get from https://bank.testnet.algorand.network/)

Usage:
    python examples/anchor_and_verify.py
"""
import sys
import json
from pathlib import Path

# Add parent directory to path so we can import compalgo
sys.path.insert(0, str(Path(__file__).parent.parent))

from compalgo.analyzer.checker import ComplianceChecker
from compalgo.core.verdict import build_verdict
from compalgo.client import CompliLedgerClient
from compalgo.config import AlgoConfig


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_step(step: str, description: str) -> None:
    """Print a step header."""
    print(f"\n[{step}] {description}")
    print("-" * 80)


def main():
    print_section("CompALGO - Algorand Compliance Proof Anchoring Demo")
    print("P0 Flow: Scan → Verdict → Anchor → Verify")
    
    # ========================================================================
    # Load Configuration from .env
    # ========================================================================
    print_step("Step 0", "Loading configuration from .env file")
    
    try:
        config = AlgoConfig.from_env()
        config.validate(require_mnemonic=True)
        print(f"✅ Config loaded: {config}")
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\n📋 Setup Instructions:")
        print("   1. Copy .env.example to .env")
        print("   2. Edit .env and set ALGO_MNEMONIC to your Pera TestNet wallet mnemonic")
        print("   3. Get TestNet ALGO from: https://bank.testnet.algorand.network/")
        print("\n   Then run this script again.")
        sys.exit(1)
    
    # ========================================================================
    # Step 1: Scan Vulnerable Contract
    # ========================================================================
    print_step("Step 1", "Scanning vulnerable smart contract")
    
    contract_path = "examples/vulnerable_escrow.py"
    checker = ComplianceChecker(policy_pack="algorand-baseline", threshold=80)
    
    try:
        result = checker.check_file(contract_path)
    except FileNotFoundError:
        print(f"❌ Contract file not found: {contract_path}")
        print("   Make sure you're running this from the project root directory.")
        sys.exit(1)
    
    print(f"📄 Contract: {contract_path}")
    print(f"📊 Score: {result.score}/100")
    print(f"✅ Passed: {'Yes' if result.passed else 'No'}")
    print(f"⚠️  Violations: {len(result.violations)}")
    
    if result.violations:
        print("\nDetected Violations:")
        for i, v in enumerate(result.violations[:5], 1):  # Show first 5
            severity = v['severity'].upper()
            rule_id = v['rule_id']
            message = v['message']
            print(f"  {i}. [{severity}] {rule_id}: {message}")
        if len(result.violations) > 5:
            print(f"  ... and {len(result.violations) - 5} more violations")
    
    # ========================================================================
    # Step 2: Build Compliance Verdict
    # ========================================================================
    print_step("Step 2", "Building Compliance Verdict")
    
    verdict = build_verdict(
        contract=contract_path,
        violations=result.violations,
        framework="SOC2",
        control_id="CC6.1",
        fail_on="medium",  # Fail if any medium+ severity violations
    )
    
    print(f"🏛️  Framework: {verdict.framework}:{verdict.control_id}")
    print(f"📋 Status: {verdict.status.upper()}")
    print(f"⚠️  Severity: {verdict.severity.upper()}")
    print(f"📜 Rules Triggered: {', '.join(verdict.rules_triggered[:5])}")
    if len(verdict.rules_triggered) > 5:
        print(f"                    ... and {len(verdict.rules_triggered) - 5} more")
    
    # Calculate and display hash
    verdict_hash = verdict.hash_hex()
    print(f"\n🔐 Verdict Hash (SHA-256):")
    print(f"   {verdict_hash}")
    
    # Save verdict to file
    output_dir = Path("examples/output")
    output_dir.mkdir(exist_ok=True)
    verdict_file = output_dir / "verdict_demo.json"
    
    with open(verdict_file, "w", encoding="utf-8") as f:
        json.dump(verdict.model_dump(), f, indent=2)
    print(f"\n💾 Verdict saved to: {verdict_file}")
    
    # ========================================================================
    # Step 3: Anchor on Algorand TestNet
    # ========================================================================
    print_step("Step 3", "Anchoring verdict hash on Algorand TestNet")
    
    try:
        # Create client using .env configuration
        client = CompliLedgerClient.from_env(config)
        
        print(f"🌐 Network: {config.network.upper()}")
        print(f"🔗 Algod URL: {config.algod_url}")
        print(f"📍 Indexer URL: {config.indexer_url}")
        print("\n⏳ Sending transaction to Algorand... (this may take 3-5 seconds)")
        
        # Anchor the verdict on-chain
        anchor_result = client.mint_verdict(verdict)
        
        print("\n✅ Anchored successfully!")
        print(f"📝 Transaction ID: {anchor_result.txid}")
        print(f"🔍 Explorer URL:")
        print(f"   {anchor_result.explorer_url}")
        print(f"\n💡 Your proof is now permanently on the Algorand blockchain!")
        print(f"   Cost: ~0.001 ALGO")
        
    except Exception as e:
        print(f"\n❌ Anchoring failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("   - Check that your ALGO_MNEMONIC is correct in .env")
        print("   - Ensure you have TestNet ALGO in your wallet")
        print("   - Get free TestNet ALGO: https://bank.testnet.algorand.network/")
        sys.exit(1)
    
    # ========================================================================
    # Step 4: Verify Against Blockchain
    # ========================================================================
    print_step("Step 4", "Verifying verdict against blockchain")
    
    print(f"🔎 Fetching transaction from Algorand...")
    print(f"   TXID: {anchor_result.txid}")
    
    try:
        # Verify the verdict matches the on-chain hash
        is_valid = client.verify_verdict(verdict, anchor_result.txid)
        
        if is_valid:
            print("\n✅ VERIFICATION SUCCESSFUL!")
            print("   The on-chain hash matches the verdict hash.")
            print("   This verdict is cryptographically proven on Algorand.")
        else:
            print("\n❌ VERIFICATION FAILED!")
            print("   The on-chain hash does NOT match the verdict hash.")
            print("   This could indicate tampering or an incorrect TXID.")
            sys.exit(1)
    
    except Exception as e:
        print(f"\n⚠️  Verification error: {e}")
        print("   Note: It may take a few seconds for the transaction to be indexed.")
        print("   Try running the verify command manually after a few seconds:")
        print(f"   compalgo verify --verdict {verdict_file} --txid {anchor_result.txid}")
    
    # ========================================================================
    # Summary
    # ========================================================================
    print_section("Demo Complete! 🎉")
    
    print("\n📊 Summary:")
    print(f"   Contract: {contract_path}")
    print(f"   Score: {result.score}/100")
    print(f"   Status: {verdict.status.upper()}")
    print(f"   Violations: {len(result.violations)}")
    print(f"   Verdict Hash: {verdict_hash[:32]}...")
    print(f"   TXID: {anchor_result.txid}")
    print(f"\n🔗 Blockchain Proof:")
    print(f"   {anchor_result.explorer_url}")
    print(f"\n💾 Verdict File:")
    print(f"   {verdict_file}")
    
    print("\n" + "=" * 80)
    print("Your compliance proof is now permanently anchored on Algorand! 🚀")
    print("=" * 80 + "\n")
    
    # Additional verification instructions
    print("📖 Next Steps:")
    print("   1. View your transaction on AlgoExplorer (link above)")
    print("   2. Verify anytime with:")
    print(f"      compalgo verify --verdict {verdict_file} --txid {anchor_result.txid}")
    print("   3. Share the TXID and verdict file for audit verification")
    print("")


if __name__ == "__main__":
    main()
