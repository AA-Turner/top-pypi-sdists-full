"""
CompZ Basic Usage Example

This script demonstrates how to use CompZ SDK to anchor and verify compliance data.
"""

from compz import CompZClient
from pathlib import Path
import json

def main():
    print("=" * 60)
    print("CompZ SDK - Basic Usage Example")
    print("=" * 60)
    print()
    
    # Load example compliance data
    example_file = Path(__file__).parent / 'compliance_result.json'
    with open(example_file) as f:
        compliance_data = json.load(f)
    
    print("📄 Loaded compliance data:")
    print(f"   Repo: {compliance_data['repo_id']}")
    print(f"   Frameworks: {', '.join(compliance_data['frameworks'])}")
    print(f"   Controls: {len(compliance_data['control_evaluations'])}")
    print(f"   Risk Score: {compliance_data['risk_score']}")
    print()
    
    # Initialize CompZ client
    # No parameters = local mode (hashing works without blockchain)
    client = CompZClient()
    print()
    
    # Check what mode we're in
    status = client.get_status()
    can_anchor = status['mode'] == 'self-hosted'
    
    # Demonstrate hashing (always works)
    print("=" * 60)
    print("🔐 Computing Cryptographic Hash")
    print("=" * 60)
    print()
    
    from compz.hash import hash_compliance
    from compz.normalize import normalize_json
    
    normalized = normalize_json(compliance_data)
    comp_hash = hash_compliance(normalized)
    
    print(f"✅ Hash computed: {comp_hash}")
    print(f"📊 Normalized size: {len(normalized)} bytes")
    print()
    
    # Try anchoring to blockchain
    print("=" * 60)
    print("🚀 Anchoring to Zcash Blockchain")
    print("=" * 60)
    print()
    
    if can_anchor:
        # Real blockchain anchoring
        try:
            anchor_result = client.anchor(compliance_data)
            
            print()
            print("💾 Saving result...")
            with open('anchor_result.json', 'w') as f:
                json.dump(anchor_result.model_dump(), f, indent=2)
            print("   Saved to: anchor_result.json")
            print()
            
            # Verify immediately
            print("=" * 60)
            print("🔍 Verifying compliance data...")
            print("=" * 60)
            print()
            
            verify_result = client.verify(compliance_data, anchor_result.txid)
        except Exception as e:
            print(f"⚠️  Anchoring failed: {str(e)}")
            anchor_result = None
            verify_result = None
    else:
        # Demo mode - show what would happen
        print("⚠️  Blockchain anchoring not available in local mode")
        print()
        print("📝 What WOULD happen with blockchain access:")
        print(f"   1. Hash ({comp_hash[:32]}...) stored in Zcash memo")
        print("   2. Shielded transaction sent to blockchain")
        print("   3. Transaction ID (TXID) returned as proof")
        print("   4. Anyone can verify using: compz verify <file> <txid>")
        print()
        print("💡 To enable blockchain anchoring:")
        print("   Option A: Configure Zcash RPC in .env (see .env.example)")
        print("   Option B: Use Zashi wallet: compz pay compliance_result.json --qr")
        print()
        anchor_result = None
        verify_result = None
    
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    if anchor_result:
        print(f"✅ Anchored: {anchor_result.txid[:16]}...")
        print(f"✅ Verified: {verify_result.valid}")
        print(f"🌐 Network: {anchor_result.network}")
        print(f"🔐 Hash: {anchor_result.hash[:32]}...")
        
        if anchor_result.explorer_url:
            print(f"🔗 View on explorer:")
            print(f"   {anchor_result.explorer_url}")
    else:
        print(f"✅ Hash computed: {comp_hash[:32]}...")
        print(f"⚠️  Blockchain anchoring: Not available (local mode)")
        print(f"💡 SDK working correctly - hashing functional!")
    
    print()
    print("=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print("1. For production, switch to self-hosted mode:")
    print("   client = CompZClient(")
    print("       rpc_url='http://localhost:18232',")
    print("       rpc_user='user',")
    print("       rpc_pass='pass'")
    print("   )")
    print()
    print("2. Integrate with CI/CD:")
    print("   - Run 'compz anchor' after security scans")
    print("   - Store txid in database")
    print("   - Share txid with auditors for verification")
    print()
    print("3. Check the documentation:")
    print("   https://github.com/Compliledger/CompZ")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
