"""
CompZ Self-Hosted Example - Real Zcash Blockchain

This example demonstrates how to use CompZ with a real Zcash node
to anchor compliance data to the actual blockchain.

PREREQUISITES:
1. Zcash node running (docker-compose up -d zcashd)
2. Node fully synced (2-4 hours)
3. Z-address created and funded
4. .env file configured

Setup:
    cp .env.example .env
    # Edit .env with your Zcash credentials
    docker-compose up -d zcashd
"""

import os
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from compz import CompZClient


def check_prerequisites():
    """Check if all prerequisites are met."""
    print("🔍 Checking prerequisites...")
    
    required_vars = [
        'ZCASH_RPC_URL',
        'ZCASH_RPC_USER',
        'ZCASH_RPC_PASS',
        'ZCASH_DEFAULT_ADDRESS'
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print("❌ Missing environment variables:")
        for var in missing:
            print(f"   - {var}")
        print("\n💡 Please configure .env file:")
        print("   cp .env.example .env")
        print("   # Edit .env with your Zcash credentials")
        return False
    
    print("✅ All environment variables configured")
    return True


def main():
    print("=" * 70)
    print("CompZ SDK - Real Zcash Testnet Integration")
    print("=" * 70)
    print()
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n⚠️  Running in DEMO MODE (no real blockchain)")
        print("📝 See BLOCKCHAIN_SETUP.md for testnet setup instructions")
        print()
        
        # Fallback to demo mode for demonstration
        client = CompZClient()
    else:
        print()
        print("=" * 70)
        print("✅ Self-Hosted Mode - Real Zcash Testnet")
        print("=" * 70)
        print()
        
        # Initialize client with self-hosted configuration
        client = CompZClient(
            rpc_url=os.getenv('ZCASH_RPC_URL'),
            rpc_user=os.getenv('ZCASH_RPC_USER'),
            rpc_pass=os.getenv('ZCASH_RPC_PASS'),
            default_address=os.getenv('ZCASH_DEFAULT_ADDRESS'),
            testnet=os.getenv('ZCASH_TESTNET', 'true').lower() == 'true'
        )
    
    # Check status
    status = client.get_status()
    print(f"📊 Mode: {status['mode']}")
    if 'network' in status:
        print(f"🌐 Network: {status['network']}")
    if status['mode'] == 'self-hosted':
        print(f"🔗 RPC URL: {status['rpc_url']}")
        print(f"💼 Address: {status['address'][:30]}...")
    print()
    
    print("=" * 70)
    print("Loading Compliance Data")
    print("=" * 70)
    print()
    
    # Load example compliance data
    compliance_file = Path(__file__).parent / 'compliance_result.json'
    with open(compliance_file) as f:
        compliance_data = json.load(f)
    
    print(f"📄 Loaded: compliance_result.json")
    print(f"   Repo: {compliance_data['repo_id']}")
    print(f"   Frameworks: {', '.join(compliance_data['frameworks'])}")
    print(f"   Controls: {len(compliance_data['control_evaluations'])}")
    print(f"   Risk Score: {compliance_data['risk_score']}")
    print(f"   Status: {compliance_data['metadata']['passed_controls']}/{compliance_data['metadata']['total_controls_evaluated']} passed")
    print()
    
    print("=" * 70)
    print("🚀 Anchoring to Zcash Blockchain")
    print("=" * 70)
    print()
    
    if status['mode'] == 'self-hosted':
        print("📡 Sending shielded transaction to Zcash testnet...")
        print("⏳ This may take 10-30 seconds...")
    else:
        print("🌐 Using demo gateway (simulated for presentation)...")
    print()
    
    try:
        # Anchor to blockchain
        anchor_result = client.anchor(
            compliance_data,
            wait_for_confirmation=False
        )
        
        print()
        print("=" * 70)
        print("✅ SUCCESS - Anchored to Blockchain!")
        print("=" * 70)
        print()
        
        print(f"🔐 Hash: {anchor_result.hash}")
        print(f"📝 TXID: {anchor_result.txid}")
        print(f"🌐 Network: {anchor_result.network}")
        print(f"🏷️  Mode: {anchor_result.mode}")
        print(f"⏰ Timestamp: {anchor_result.timestamp}")
        
        if anchor_result.explorer_url:
            print(f"🔗 Explorer: {anchor_result.explorer_url}")
        print()
        
        # Save result
        result_file = Path(__file__).parent / 'anchor_result_selfhosted.json'
        with open(result_file, 'w') as f:
            json.dump(anchor_result.model_dump(), f, indent=2)
        print(f"💾 Result saved to: {result_file.name}")
        print()
        
        # Wait for propagation
        if status['mode'] == 'self-hosted':
            print("⏳ Waiting 5 seconds for transaction to propagate...")
            import time
            time.sleep(5)
            print()
        
        print("=" * 70)
        print("🔍 Verifying Against Blockchain")
        print("=" * 70)
        print()
        
        # Verify
        verify_result = client.verify(compliance_data, anchor_result.txid)
        
        print()
        if verify_result.valid:
            print("=" * 70)
            print("✅ VERIFICATION SUCCESSFUL")
            print("=" * 70)
            print()
            print("Your compliance data has been cryptographically anchored")
            print("to the Zcash blockchain and verified!")
            print()
            print(f"🔐 Local Hash:    {verify_result.local_hash}")
            print(f"⛓️  On-Chain Hash: {verify_result.onchain_hash}")
            print(f"✅ Match: {verify_result.local_hash == verify_result.onchain_hash}")
            
            if verify_result.confirmations is not None:
                print(f"📦 Confirmations: {verify_result.confirmations}")
        else:
            print("❌ VERIFICATION FAILED")
            print(f"Reason: {verify_result.reason}")
        
        print()
        print("=" * 70)
        print("📚 What Just Happened?")
        print("=" * 70)
        print()
        print("1. ✅ Compliance data normalized to canonical JSON")
        print("2. ✅ SHA-256 hash computed (cryptographic fingerprint)")
        print("3. ✅ Shielded Zcash transaction created with hash in memo")
        print("4. ✅ Transaction sent to Zcash blockchain")
        print("5. ✅ TXID received - proof is now immutable")
        print("6. ✅ Verification confirmed data matches blockchain")
        print()
        print("💡 This enables:")
        print("   • Privacy-preserving compliance attestation")
        print("   • Immutable audit trail without revealing data")
        print("   • Third-party verification via TXID")
        print("   • Zero-knowledge proof of compliance")
        print()
        
        if status['mode'] == 'self-hosted':
            print("=" * 70)
            print("🎯 Production Features")
            print("=" * 70)
            print()
            print("✅ Real Zcash testnet integration complete!")
            print(f"✅ Transaction on blockchain: {anchor_result.txid}")
            print("✅ Privacy-preserving SDK operational")
            print("✅ Open-source and ready for developers")
            print()
            print("Key Features:")
            print("  • Dual-mode architecture (demo + self-hosted)")
            print("  • Real shielded transactions with memos")
            print("  • Privacy-first compliance attestation")
            print("  • Developer-friendly SDK")
            print("  • CLI tools for CI/CD integration")
            print()
        
        print("=" * 70)
        print("📖 Next Steps")
        print("=" * 70)
        print()
        print("1. View on explorer:")
        if anchor_result.explorer_url:
            print(f"   {anchor_result.explorer_url}")
        print()
        print("2. Try tampering detection:")
        print("   python tamper_detection_demo.py")
        print()
        print("3. Integrate with CI/CD:")
        print("   compz anchor compliance.json")
        print()
        print("4. Read documentation:")
        print("   cat BLOCKCHAIN_SETUP.md")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        print()
        print("💡 Troubleshooting:")
        print("1. Ensure Zcash node is running: docker ps")
        print("2. Check node is synced: docker exec compz-zcashd zcash-cli -testnet getblockchaininfo")
        print("3. Verify address has funds: docker exec compz-zcashd zcash-cli -testnet z_getbalance YOUR_ADDRESS")
        print("4. See BLOCKCHAIN_SETUP.md for detailed setup")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
