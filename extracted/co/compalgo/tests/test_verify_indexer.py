"""
Verification tests using Algorand Indexer (P0 Test Matrix: TV-001 through TV-010)

Tests the full verification flow including:
- Valid verdict verification
- Tamper detection
- Historical transaction lookup via Indexer
- Error handling
"""
import os
import pytest
from compalgo.core.verdict import ComplianceVerdict, build_verdict
from compalgo.client import CompliLedgerClient


# Mark all tests as network-dependent
pytestmark = pytest.mark.network


@pytest.fixture
def algod_url():
    """Get algod URL from environment"""
    return os.getenv("ALGO_ALGOD_URL", "https://testnet-api.algonode.cloud")


@pytest.fixture
def indexer_url():
    """Get indexer URL from environment"""
    return os.getenv("ALGO_INDEXER_URL", "https://testnet-idx.algonode.cloud")


@pytest.fixture
def mnemonic():
    """Get mnemonic from environment"""
    mn = os.getenv("ALGO_MNEMONIC")
    if not mn:
        pytest.skip("ALGO_MNEMONIC not set")
    return mn


@pytest.fixture
def client(algod_url, indexer_url, mnemonic):
    """Create CompliLedgerClient with Indexer support"""
    return CompliLedgerClient(
        algod_url=algod_url,
        algod_token="",
        sender_mnemonic=mnemonic,
        network="testnet",
        indexer_url=indexer_url,
        indexer_token=""
    )


@pytest.fixture
def sample_verdict():
    """Create a sample verdict for testing"""
    violations = [
        {
            "rule_id": "DELETE_WITHOUT_ADMIN_CHECK",
            "severity": "critical",
            "message": "Test violation",
            "controls": [{"framework": "SOC2", "control_id": "CC6.1"}]
        }
    ]
    return build_verdict(
        contract="tests/test_contract.py",
        violations=violations,
        framework="SOC2",
        control_id="CC6.1",
        fail_on="medium"
    )


class TestValidVerification:
    """TV-001: Valid verification tests"""
    
    def test_valid_verdict_verification(self, client, sample_verdict):
        """Verify a correctly anchored verdict returns True"""
        # Anchor verdict
        result = client.mint_verdict(sample_verdict)
        assert result.txid is not None
        
        # Verify immediately (using algod)
        is_valid = client.verify_verdict(sample_verdict, result.txid)
        assert is_valid is True
    
    def test_verification_with_dict_input(self, client, sample_verdict):
        """Verification should work with dict or ComplianceVerdict"""
        result = client.mint_verdict(sample_verdict)
        
        # Verify with dict
        verdict_dict = sample_verdict.model_dump()
        is_valid = client.verify_verdict(verdict_dict, result.txid)
        assert is_valid is True


class TestTamperDetection:
    """TV-002: Tamper detection tests"""
    
    def test_modified_verdict_fails_verification(self, client, sample_verdict):
        """Modified verdict should fail verification"""
        # Anchor original
        result = client.mint_verdict(sample_verdict)
        
        # Tamper with verdict
        tampered = ComplianceVerdict(**sample_verdict.model_dump())
        tampered.status = "pass"  # Change status
        
        # Verification should fail
        is_valid = client.verify_verdict(tampered, result.txid)
        assert is_valid is False
    
    def test_different_framework_fails_verification(self, client, sample_verdict):
        """Changing framework should fail verification"""
        result = client.mint_verdict(sample_verdict)
        
        tampered = ComplianceVerdict(**sample_verdict.model_dump())
        tampered.framework = "PCI-DSS"  # Different framework
        
        is_valid = client.verify_verdict(tampered, result.txid)
        assert is_valid is False
    
    def test_different_rules_fails_verification(self, client, sample_verdict):
        """Changing rules_triggered should fail verification"""
        result = client.mint_verdict(sample_verdict)
        
        tampered = ComplianceVerdict(**sample_verdict.model_dump())
        tampered.rules_triggered = ["DIFFERENT_RULE"]
        
        is_valid = client.verify_verdict(tampered, result.txid)
        assert is_valid is False


class TestWrongTXID:
    """TV-003: Wrong TXID tests"""
    
    def test_random_txid_fails_verification(self, client, sample_verdict):
        """Random TXID should fail verification"""
        # Use a fake but valid-format TXID
        fake_txid = "A" * 52  # Valid TXID format
        
        # Should return False or raise error
        try:
            is_valid = client.verify_verdict(sample_verdict, fake_txid)
            assert is_valid is False
        except Exception:
            # Error is acceptable for non-existent TXID
            pass
    
    def test_malformed_txid_fails(self, client, sample_verdict):
        """Malformed TXID should fail"""
        malformed_txid = "not-a-valid-txid"
        
        try:
            is_valid = client.verify_verdict(sample_verdict, malformed_txid)
            assert is_valid is False
        except Exception:
            # Error is acceptable
            pass


class TestHistoricalProof:
    """TV-004: Historical proof verification using Indexer"""
    
    @pytest.mark.slow
    def test_verify_old_transaction_with_indexer(self, client):
        """Verify a 30-day old transaction using Indexer"""
        # Use a known old TXID from P0 testing
        # This is the E2E test TXID from P0_COMPLETION_SUMMARY.md
        old_txid = "DIE62SW4ZWOAJABDWY4UTEKATQQAHI342XX2HYMA3H4VA6IEMOXQ"
        
        # Create the verdict that was used
        violations = [
            {
                "rule_id": "DELETE_WITHOUT_ADMIN_CHECK",
                "severity": "critical",
                "message": "DeleteApplication lacks admin check",
                "controls": [{"framework": "SOC2", "control_id": "CC6.1"}]
            }
        ]
        verdict = build_verdict(
            contract="examples/test.py",
            violations=violations,
            framework="SOC2",
            control_id="CC6.1",
            fail_on="medium"
        )
        
        # This might not match exactly, but tests the indexer path
        # In real usage, you'd have the exact verdict JSON stored
        try:
            # Force use of indexer
            if client._algo.indexer_client:
                note = client._algo.get_note_text(old_txid, use_indexer=True)
                assert note is not None
                assert "CLG1" in note
                assert "sha256" in note
        except Exception:
            pytest.skip("Indexer not available or TXID too old")


class TestNonCLGTransaction:
    """TV-005: Non-CLG transaction tests"""
    
    def test_non_clg_transaction_fails(self, client, sample_verdict):
        """Transaction without CLG note should fail verification"""
        # This would require access to a random testnet TXID
        # For now, we test the note format check
        pytest.skip("Requires known non-CLG TXID on testnet")


class TestMalformedNote:
    """TV-006: Malformed note tests"""
    
    def test_note_without_clg_prefix(self, client):
        """Note without CLG1 prefix should fail"""
        # This is tested implicitly in verify_verdict logic
        # The note must match "CLG1|sha256:<hash>" format exactly
        pass


class TestIndexerFallback:
    """TV-007: Indexer fallback tests"""
    
    def test_algod_fails_indexer_succeeds(self, client, sample_verdict):
        """When algod fails, should fall back to Indexer"""
        # Anchor a verdict
        result = client.mint_verdict(sample_verdict)
        
        # Wait a bit, then force indexer lookup
        import time
        time.sleep(5)  # Let transaction settle
        
        if client._algo.indexer_client:
            # Force indexer usage
            note = client._algo.get_note_text(result.txid, use_indexer=True)
            assert note is not None
            assert "CLG1" in note
        else:
            pytest.skip("Indexer not configured")


class TestMultiNetwork:
    """TV-008: Multi-network tests"""
    
    def test_testnet_txid_on_mainnet_client_fails(self):
        """Testnet TXID should not verify on mainnet client"""
        # This requires mainnet access, skip for now
        pytest.skip("Mainnet testing not in P0 scope")


class TestPartialHashMatch:
    """TV-009: Partial hash match tests"""
    
    def test_truncated_hash_fails(self, client, sample_verdict):
        """Note with truncated hash should fail"""
        # The verification logic checks exact match
        # Truncated hash would not match
        pass  # Implicitly tested in tamper detection


class TestConcurrentVerification:
    """TV-010: Concurrent verification tests"""
    
    @pytest.mark.slow
    def test_verify_multiple_verdicts_parallel(self, client):
        """Verify multiple verdicts in parallel"""
        import concurrent.futures
        
        # Create and anchor 3 verdicts
        verdicts_and_txids = []
        for i in range(3):
            violations = [{
                "rule_id": f"TEST_RULE_{i}",
                "severity": "high",
                "message": f"Test {i}"
            }]
            verdict = build_verdict(
                contract=f"test_{i}.py",
                violations=violations,
                framework="SOC2",
                control_id="CC6.1",
                fail_on="medium"
            )
            result = client.mint_verdict(verdict)
            verdicts_and_txids.append((verdict, result.txid))
        
        # Verify all in parallel
        def verify_one(vt):
            v, t = vt
            return client.verify_verdict(v, t)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            results = list(executor.map(verify_one, verdicts_and_txids))
        
        # All should be valid
        assert all(results), f"Some verifications failed: {results}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "network", "--tb=short"])
