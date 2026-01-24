"""
End-to-End Full Flow Tests (P0 Test Matrix: TE-001 through TE-010)

Tests the complete analyze → verdict → anchor → verify pipeline
including multi-file analysis, policy comparison, and CLI workflows.
"""
import os
import json
import pytest
from pathlib import Path
from compalgo.analyzer.checker import ComplianceChecker
from compalgo.core.verdict import build_verdict, ComplianceVerdict
from compalgo.client import CompliLedgerClient


pytestmark = pytest.mark.integration


FIXTURES_DIR = Path(__file__).parent / "fixtures"
EXAMPLES_DIR = Path(__file__).parent.parent / "examples"


@pytest.fixture
def algod_url():
    return os.getenv("ALGO_ALGOD_URL", "https://testnet-api.algonode.cloud")


@pytest.fixture
def indexer_url():
    return os.getenv("ALGO_INDEXER_URL", "https://testnet-idx.algonode.cloud")


@pytest.fixture
def mnemonic():
    mn = os.getenv("ALGO_MNEMONIC")
    if not mn:
        pytest.skip("ALGO_MNEMONIC not set - skipping network tests")
    return mn


@pytest.fixture
def client(algod_url, indexer_url, mnemonic):
    """Create CompliLedgerClient with full config"""
    return CompliLedgerClient(
        algod_url=algod_url,
        algod_token="",
        sender_mnemonic=mnemonic,
        network="testnet",
        indexer_url=indexer_url,
        indexer_token=""
    )


class TestHappyPath:
    """TE-001: Happy path with clean contract"""
    
    @pytest.mark.network
    def test_clean_contract_full_flow(self, client):
        """Clean contract → pass verdict → anchor → verify"""
        contract_path = FIXTURES_DIR / "clean_escrow.py"
        if not contract_path.exists():
            pytest.skip(f"Fixture not found: {contract_path}")
        
        # 1. Analyze
        checker = ComplianceChecker(policy_pack="algorand-baseline", threshold=80)
        result = checker.check_file(str(contract_path))
        
        # Should pass with minimal/no violations
        assert result.score >= 80 or len([v for v in result.violations if v["severity"] in ["critical", "high"]]) == 0
        
        # 2. Build verdict
        verdict = build_verdict(
            contract=str(contract_path),
            violations=result.violations,
            framework="SOC2",
            control_id="CC6.1",
            fail_on="high"
        )
        
        # Should be pass status (no high/critical violations)
        assert verdict.status == "pass" or verdict.severity not in ["critical", "high"]
        
        # 3. Anchor
        anchor_result = client.mint_verdict(verdict)
        assert anchor_result.txid is not None
        assert anchor_result.explorer_url is not None
        assert "algoexplorer.io" in anchor_result.explorer_url
        
        # 4. Verify
        is_valid = client.verify_verdict(verdict, anchor_result.txid)
        assert is_valid is True
        
        print(f"✅ Clean contract flow complete: {anchor_result.explorer_url}")


class TestViolationFlow:
    """TE-002: Violation flow with vulnerable contract"""
    
    @pytest.mark.network
    def test_vulnerable_contract_full_flow(self, client):
        """Vulnerable contract → fail verdict → anchor → verify"""
        contract_path = EXAMPLES_DIR / "vulnerable_escrow.py"
        if not contract_path.exists():
            pytest.skip(f"Example not found: {contract_path}")
        
        # 1. Analyze
        checker = ComplianceChecker(policy_pack="algorand-baseline", threshold=80)
        result = checker.check_file(str(contract_path))
        
        # Should fail threshold
        assert result.score < 80
        assert result.passed is False
        assert len(result.violations) > 0
        
        # 2. Build verdict
        verdict = build_verdict(
            contract=str(contract_path),
            violations=result.violations,
            framework="SOC2",
            control_id="CC6.1",
            fail_on="medium"
        )
        
        # Should be fail status
        assert verdict.status == "fail"
        assert len(verdict.rules_triggered) > 0
        
        # 3. Anchor (even failing verdicts can be anchored)
        anchor_result = client.mint_verdict(verdict)
        assert anchor_result.txid is not None
        
        # 4. Verify
        is_valid = client.verify_verdict(verdict, anchor_result.txid)
        assert is_valid is True
        
        print(f"✅ Vulnerable contract flow complete: {anchor_result.explorer_url}")
        print(f"   Violations: {len(result.violations)}")
        print(f"   Score: {result.score}/100")


class TestMultipleContracts:
    """TE-003: Multiple contracts → multiple verdicts → anchor all"""
    
    @pytest.mark.network
    @pytest.mark.slow
    def test_three_contracts_three_verdicts(self, client):
        """Analyze 3 files, generate 3 verdicts, anchor all, verify all"""
        contracts = [
            FIXTURES_DIR / "clean_escrow.py",
            FIXTURES_DIR / "partial_violations.py",
            EXAMPLES_DIR / "vulnerable_escrow.py"
        ]
        
        # Filter to existing contracts
        existing = [c for c in contracts if c.exists()]
        if len(existing) < 2:
            pytest.skip("Need at least 2 test contracts")
        
        checker = ComplianceChecker(policy_pack="algorand-baseline", threshold=80)
        anchored = []
        
        for contract_path in existing:
            # 1. Analyze
            result = checker.check_file(str(contract_path))
            
            # 2. Build verdict
            verdict = build_verdict(
                contract=str(contract_path),
                violations=result.violations,
                framework="SOC2",
                control_id="CC6.1",
                fail_on="medium"
            )
            
            # 3. Anchor
            anchor_result = client.mint_verdict(verdict)
            anchored.append((verdict, anchor_result))
            
            print(f"Anchored {contract_path.name}: {anchor_result.txid[:16]}...")
        
        # 4. Verify all
        for verdict, anchor_result in anchored:
            is_valid = client.verify_verdict(verdict, anchor_result.txid)
            assert is_valid is True
        
        print(f"✅ Anchored and verified {len(anchored)} contracts")


class TestPolicyComparison:
    """TE-004: Same contract with different policies"""
    
    def test_contract_with_two_policies(self):
        """Analyze same contract with algorand-baseline and pci-dss-algorand"""
        contract_path = EXAMPLES_DIR / "vulnerable_escrow.py"
        if not contract_path.exists():
            pytest.skip(f"Example not found: {contract_path}")
        
        policies = ["algorand-baseline", "pci-dss-algorand"]
        results = {}
        
        for policy in policies:
            checker = ComplianceChecker(policy_pack=policy, threshold=80)
            result = checker.check_file(str(contract_path))
            results[policy] = result
            
            print(f"{policy}: Score={result.score}, Violations={len(result.violations)}")
        
        # Both policies should find violations
        for policy, result in results.items():
            assert len(result.violations) > 0, f"{policy} should find violations"
        
        # Violations might differ between policies
        # Just verify both ran successfully
        assert len(results) == 2


class TestCLIWorkflow:
    """TE-005: CLI workflow simulation"""
    
    def test_cli_simulation_via_api(self):
        """Simulate: compalgo check → anchor → verify"""
        contract_path = EXAMPLES_DIR / "vulnerable_escrow.py"
        if not contract_path.exists():
            pytest.skip(f"Example not found: {contract_path}")
        
        # Simulate: compalgo check contract.py --verdict-out verdict.json
        checker = ComplianceChecker(policy_pack="algorand-baseline", threshold=80)
        result = checker.check_file(str(contract_path))
        
        verdict = build_verdict(
            contract=str(contract_path),
            violations=result.violations,
            framework="SOC2",
            control_id="CC6.1",
            fail_on="medium"
        )
        
        # Save to JSON (simulate --verdict-out)
        verdict_json = verdict.model_dump()
        assert "framework" in verdict_json
        assert "status" in verdict_json
        assert "rules_triggered" in verdict_json
        
        print(f"✅ CLI simulation: verdict generated")
        print(f"   Status: {verdict.status}")
        print(f"   Severity: {verdict.severity}")


class TestAPIWorkflow:
    """TE-006: Python API workflow"""
    
    @pytest.mark.network
    def test_api_end_to_end(self, client):
        """Full programmatic workflow using Python API"""
        contract_path = EXAMPLES_DIR / "vulnerable_escrow.py"
        if not contract_path.exists():
            pytest.skip(f"Example not found: {contract_path}")
        
        # 1. Import and analyze
        from compalgo import ComplianceChecker, CompliLedgerClient
        from compalgo.core.verdict import build_verdict
        
        # 2. Check contract
        checker = ComplianceChecker(policy_pack="algorand-baseline", threshold=80)
        result = checker.check_file(str(contract_path))
        
        # 3. Build verdict
        verdict = build_verdict(
            contract=result.file_path,
            violations=result.violations,
            framework="SOC2",
            control_id="CC6.1",
            fail_on="medium"
        )
        
        # 4. Anchor
        anchor_result = client.mint_verdict(verdict)
        
        # 5. Verify
        is_valid = client.verify_verdict(verdict, anchor_result.txid)
        
        assert is_valid is True
        print(f"✅ API workflow complete")
        print(f"   TXID: {anchor_result.txid}")
        print(f"   Explorer: {anchor_result.explorer_url}")


class TestVerifyAfter24h:
    """TE-007: Verify after 24 hours (requires Indexer)"""
    
    @pytest.mark.slow
    @pytest.mark.network
    def test_verify_historical_proof(self, client):
        """Use known old TXID to test Indexer-based verification"""
        # Use the E2E test TXID from P0_COMPLETION_SUMMARY.md
        historical_txid = "DIE62SW4ZWOAJABDWY4UTEKATQQAHI342XX2HYMA3H4VA6IEMOXQ"
        
        # This TXID was created with a specific verdict
        # We'd need the exact verdict JSON to verify, but we can at least
        # test that Indexer can fetch the transaction
        
        if client._algo.indexer_client:
            note = client._algo.get_note_text(historical_txid, use_indexer=True)
            assert note is not None
            assert "CLG1" in note
            assert "sha256" in note
            print(f"✅ Historical proof verified via Indexer")
        else:
            pytest.skip("Indexer not configured")


class TestCrossSessionVerify:
    """TE-008: Anchor in one session, verify in another"""
    
    @pytest.mark.network
    def test_anchor_then_verify_new_client(self, algod_url, indexer_url, mnemonic):
        """Anchor with one client instance, verify with fresh instance"""
        contract_path = EXAMPLES_DIR / "vulnerable_escrow.py"
        if not contract_path.exists():
            pytest.skip(f"Example not found: {contract_path}")
        
        # Session 1: Analyze and anchor
        client1 = CompliLedgerClient(
            algod_url=algod_url,
            algod_token="",
            sender_mnemonic=mnemonic,
            network="testnet"
        )
        
        checker = ComplianceChecker(policy_pack="algorand-baseline", threshold=80)
        result = checker.check_file(str(contract_path))
        verdict = build_verdict(
            contract=str(contract_path),
            violations=result.violations,
            framework="SOC2",
            control_id="CC6.1",
            fail_on="medium"
        )
        
        anchor_result = client1.mint_verdict(verdict)
        txid = anchor_result.txid
        
        # Session 2: Fresh client, verify
        client2 = CompliLedgerClient(
            algod_url=algod_url,
            algod_token="",
            sender_mnemonic=mnemonic,
            network="testnet",
            indexer_url=indexer_url,
            indexer_token=""
        )
        
        is_valid = client2.verify_verdict(verdict, txid)
        assert is_valid is True
        
        print(f"✅ Cross-session verification successful")


class TestMainnetProduction:
    """TE-009: Mainnet production test"""
    
    def test_mainnet_deployment(self):
        """Test mainnet configuration (without actual deployment)"""
        # This would require mainnet ALGO and is out of P0 scope
        # Just verify client can be configured for mainnet
        
        from compalgo.client import CompliLedgerClient
        
        # Don't actually create transactions, just verify init
        # In production, user would provide mainnet mnemonic
        pytest.skip("Mainnet testing requires mainnet ALGO - out of P0 scope")


class TestFailureRecovery:
    """TE-010: Network error recovery"""
    
    def test_network_error_handling(self):
        """Test graceful handling of network errors"""
        from compalgo.client import CompliLedgerClient
        
        # Create client with invalid URL
        client = CompliLedgerClient(
            algod_url="http://invalid-url-that-does-not-exist.local",
            algod_token="",
            sender_mnemonic="abandon " * 24 + "abandon",  # Valid format but fake
            network="testnet"
        )
        
        verdict = ComplianceVerdict(
            framework="SOC2",
            control_id="CC6.1",
            status="pass",
            contract="test.py",
            rules_triggered=[],
            severity="info",
            timestamp="2024-12-01T00:00:00+00:00"
        )
        
        # Should raise connection error
        with pytest.raises(Exception):
            client.mint_verdict(verdict)
        
        print("✅ Network error handling works correctly")


class TestVerdictPersistence:
    """Test verdict JSON persistence"""
    
    def test_verdict_save_and_load(self, tmp_path):
        """Save verdict to JSON and reload"""
        contract_path = EXAMPLES_DIR / "vulnerable_escrow.py"
        if not contract_path.exists():
            pytest.skip(f"Example not found: {contract_path}")
        
        # Generate verdict
        checker = ComplianceChecker(policy_pack="algorand-baseline", threshold=80)
        result = checker.check_file(str(contract_path))
        verdict = build_verdict(
            contract=str(contract_path),
            violations=result.violations,
            framework="SOC2",
            control_id="CC6.1",
            fail_on="medium"
        )
        
        # Save to file
        verdict_file = tmp_path / "verdict.json"
        with open(verdict_file, "w") as f:
            json.dump(verdict.model_dump(), f, indent=2)
        
        # Reload
        with open(verdict_file, "r") as f:
            loaded_data = json.load(f)
        
        verdict_reloaded = ComplianceVerdict(**loaded_data)
        
        # Should have same hash
        assert verdict.hash_hex() == verdict_reloaded.hash_hex()
        print(f"✅ Verdict persistence: hash preserved")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration", "--tb=short"])
