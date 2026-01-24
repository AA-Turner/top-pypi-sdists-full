"""
CompZ Tamper Detection Demo

Demonstrates how CompZ detects tampering by comparing on-chain hash
with recomputed hash from potentially modified data.
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from compz import CompZClient
from compz.hash import hash_compliance


def main():
    print("=" * 70)
    print("CompZ Tamper Detection Demo")
    print("=" * 70)
    print()
    
    # Load original compliance data
    compliance_file = Path(__file__).parent / 'compliance_result.json'
    with open(compliance_file) as f:
        original_data = json.load(f)
    
    print("📄 Original Compliance Data:")
    print(f"   Repo: {original_data['repo_id']}")
    print(f"   Risk Score: {original_data['risk_score']}")
    print(f"   Controls Passed: {original_data['metadata']['passed_controls']}/10")
    print()
    
    # Compute hash
    original_hash = hash_compliance(original_data)
    print(f"🔐 Original Hash: {original_hash}")
    print()
    
    # Simulate anchoring (in real scenario, you'd have a txid)
    print("🚀 Simulating blockchain anchor...")
    print(f"   (In production: client.anchor(original_data))")
    print(f"   Stored hash: {original_hash}")
    print()
    
    print("=" * 70)
    print("⚠️  Scenario 1: Tampering Detected")
    print("=" * 70)
    print()
    
    # Create tampered version
    tampered_data = original_data.copy()
    tampered_data['risk_score'] = 5.0  # Changed from 15.5 to 5.0
    
    print("🔧 Someone tries to modify the data:")
    print(f"   Changed risk_score: 15.5 → 5.0")
    print(f"   (Making compliance look better than it is)")
    print()
    
    # Compute hash of tampered data
    tampered_hash = hash_compliance(tampered_data)
    print(f"🔐 Tampered Hash: {tampered_hash}")
    print(f"🔐 Original Hash: {original_hash}")
    print()
    
    # Compare
    if tampered_hash == original_hash:
        print("✅ Hashes match - Data is authentic")
    else:
        print("❌ TAMPERING DETECTED!")
        print("   Hashes do not match")
        print("   Data has been modified since anchoring")
    print()
    
    print("=" * 70)
    print("✅ Scenario 2: Authentic Data Verified")
    print("=" * 70)
    print()
    
    print("📄 Loading original data again...")
    verified_hash = hash_compliance(original_data)
    print(f"🔐 Computed Hash: {verified_hash}")
    print(f"🔐 Blockchain Hash: {original_hash}")
    print()
    
    if verified_hash == original_hash:
        print("✅ VERIFICATION SUCCESSFUL!")
        print("   Hashes match perfectly")
        print("   Data is authentic and unmodified")
    else:
        print("❌ Verification failed")
    print()
    
    print("=" * 70)
    print("🔍 Why This Matters")
    print("=" * 70)
    print()
    print("CompZ provides cryptographic proof that compliance data")
    print("has not been tampered with:")
    print()
    print("1. 🔐 Original data → normalized → hashed → stored on-chain")
    print("2. ⏰ Timestamp is immutable (blockchain consensus)")
    print("3. 🔍 Anyone can verify: recompute hash and compare")
    print("4. ❌ Any modification changes the hash completely")
    print()
    print("Even a single character change makes hashes completely different!")
    print()
    
    # Demonstrate extreme sensitivity
    print("=" * 70)
    print("🔬 Hash Sensitivity Demonstration")
    print("=" * 70)
    print()
    
    test_data = {"message": "Hello World"}
    hash1 = hash_compliance(test_data)
    print(f"Data: {json.dumps(test_data)}")
    print(f"Hash: {hash1}")
    print()
    
    test_data_modified = {"message": "Hello World!"}  # Added just one "!"
    hash2 = hash_compliance(test_data_modified)
    print(f"Data: {json.dumps(test_data_modified)}")
    print(f"Hash: {hash2}")
    print()
    
    print("Changed just ONE character (added '!')")
    print(f"Hashes match: {hash1 == hash2}")
    print()
    print("This is the power of cryptographic hashing!")
    print()
    
    print("=" * 70)
    print("🎯 Real-World Use Case")
    print("=" * 70)
    print()
    print("Scenario: Quarterly Compliance Audit")
    print()
    print("1. DevOps runs security scan → generates compliance_result.json")
    print("2. CompZ anchors hash to Zcash → gets TXID")
    print("3. DevOps shares TXID with auditors")
    print("4. 3 months later, auditors receive compliance report")
    print("5. Auditors verify: compz verify compliance.json <TXID>")
    print("6. If report was modified: ❌ Tampering detected!")
    print("7. If report is authentic: ✅ Verified on blockchain")
    print()
    print("Result: Auditors have cryptographic proof that the compliance")
    print("report they're reviewing is exactly what was generated during")
    print("the scan - no modifications, no backdating, no manipulation.")
    print()
    
    print("=" * 70)
    print("💡 Privacy Benefit")
    print("=" * 70)
    print()
    print("What's on blockchain: Only the hash (0xabc123...)")
    print("What's NOT on blockchain: Your actual compliance data")
    print()
    print("This means:")
    print("  ✅ Public verifiability")
    print("  ✅ Private data")
    print("  ✅ Tamper-proof audit trail")
    print("  ✅ No sensitive information leaked")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
