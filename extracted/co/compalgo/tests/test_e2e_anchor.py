"""
E2E test for anchoring and verifying Compliance Verdicts on Algorand testnet

Requires:
- ALGORAND_MNEMONIC env var
- ALGORAND_API_URL env var (defaults to testnet)
"""
import os
import sys
from compalgo.core.verdict import ComplianceVerdict, build_verdict
from compalgo.client import CompliLedgerClient


def test_e2e_anchor_and_verify():
    """Test full E2E: create verdict, anchor on-chain, verify"""
    mnemonic = os.getenv("ALGORAND_MNEMONIC")
    api_url = os.getenv("ALGORAND_API_URL", "https://testnet-api.algonode.cloud")
    
    if not mnemonic:
        print("SKIPPED: ALGORAND_MNEMONIC not set")
        return
    
    # 1. Create a test verdict
    violations = [
        {
            "rule_id": "DELETE_WITHOUT_ADMIN_CHECK",
            "severity": "critical",
            "message": "DeleteApplication lacks admin check",
            "controls": [{"framework": "SOC2", "control_id": "CC6.1"}],
        }
    ]
    verdict = build_verdict(
        contract="examples/test.py",
        violations=violations,
        framework="SOC2",
        control_id="CC6.1",
        fail_on="medium",
    )
    
    print(f"Created verdict: {verdict.status} / {verdict.severity}")
    print(f"Verdict hash: {verdict.hash_hex()}")
    
    # 2. Initialize client and anchor
    client = CompliLedgerClient(
        algod_url=api_url,
        algod_token="",
        sender_mnemonic=mnemonic,
        network="testnet",
    )
    
    print("Anchoring verdict on Algorand testnet...")
    result = client.mint_verdict(verdict)
    
    print(f"✅ Anchored! TXID: {result.txid}")
    print(f"Explorer: {result.explorer_url}")
    print(f"Hash: {result.verdict_hash}")
    
    # 3. Verify the verdict
    print("Verifying verdict...")
    is_valid = client.verify_verdict(verdict, result.txid)
    
    assert is_valid, "Verification failed!"
    print("✅ Verification PASSED")
    
    # 4. Test negative case: tampered verdict should fail
    tampered = ComplianceVerdict(**verdict.model_dump())
    tampered.status = "pass"  # change status
    
    is_valid_tampered = client.verify_verdict(tampered, result.txid)
    assert not is_valid_tampered, "Tampered verdict should fail verification"
    print("✅ Tampered verdict correctly rejected")
    
    print("\n🎉 E2E test PASSED!")
    return result.txid, result.explorer_url


if __name__ == "__main__":
    if not os.getenv("ALGORAND_MNEMONIC"):
        print("Please set ALGORAND_MNEMONIC environment variable")
        sys.exit(1)
    
    txid, url = test_e2e_anchor_and_verify()
    print(f"\nTest transaction: {url}")
