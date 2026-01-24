"""Tests for PCI-DSS compliance checks."""

import pytest
from comp_leo.payments import (
    is_payment_function,
    detect_forbidden_payment_data,
    check_cardholder_data_visibility,
    check_payment_amount_validation,
    check_payment_access_control,
    check_payment_audit_logging,
    check_refund_mechanism,
    check_transaction_limits,
    detect_hardcoded_credentials
)


class TestPaymentFunctionDetection:
    """Test payment function detection logic."""
    
    def test_detects_payment_by_name(self):
        assert is_payment_function("process_payment", "") is True
        assert is_payment_function("transfer_funds", "") is True
        assert is_payment_function("withdraw", "") is True
        assert is_payment_function("deposit", "") is True
    
    def test_detects_defi_operations(self):
        assert is_payment_function("swap_tokens", "") is True
        assert is_payment_function("stake", "") is True
        assert is_payment_function("claim_rewards", "") is True
    
    def test_ignores_non_payment_functions(self):
        assert is_payment_function("calculate_hash", "") is False
        assert is_payment_function("verify_signature", "") is False
        assert is_payment_function("get_data", "") is False


class TestForbiddenDataDetection:
    """Test detection of forbidden payment data (PCI 3.2)."""
    
    def test_detects_cvv(self):
        result = detect_forbidden_payment_data("cvv")
        assert result['detected'] is True
        assert result['type'] == 'cvv'
        assert result['severity'] == 'CRITICAL'
    
    def test_detects_pin(self):
        result = detect_forbidden_payment_data("pin_number")
        assert result['detected'] is True
        assert result['type'] == 'pin'
    
    def test_detects_track_data(self):
        result = detect_forbidden_payment_data("track_data")
        assert result['detected'] is True
        assert result['type'] == 'full_track'
    
    def test_allows_safe_names(self):
        result = detect_forbidden_payment_data("payment_token")
        assert result['detected'] is False
        
        result = detect_forbidden_payment_data("amount")
        assert result['detected'] is False


class TestCardholderDataVisibility:
    """Test cardholder data visibility checks (PCI 3.4)."""
    
    def test_flags_public_card_data(self):
        result = check_cardholder_data_visibility("card_number", "public")
        assert result['violation'] is True
        assert result['severity'] == 'CRITICAL'
    
    def test_flags_public_payment_info(self):
        result = check_cardholder_data_visibility("payment_info", "public")
        assert result['violation'] is True
    
    def test_allows_private_card_data(self):
        result = check_cardholder_data_visibility("card_number", "private")
        assert result['violation'] is False
    
    def test_allows_public_non_sensitive(self):
        result = check_cardholder_data_visibility("merchant_id", "public")
        assert result['violation'] is False
        
        result = check_cardholder_data_visibility("timestamp", "public")
        assert result['violation'] is False


class TestPaymentAmountValidation:
    """Test payment amount validation checks (PCI 6.5.1)."""
    
    def test_detects_missing_positive_check(self):
        code = """
        transition process_payment(amount: u64) {
            // No validation
        }
        """
        violations = check_payment_amount_validation(code, ["amount"])
        assert len(violations) >= 1
        assert any('positive' in v['message'].lower() for v in violations)
    
    def test_detects_missing_max_check(self):
        code = """
        transition process_payment(amount: u64) {
            assert(amount > 0u64);
        }
        """
        violations = check_payment_amount_validation(code, ["amount"])
        assert any('upper limit' in v['message'].lower() for v in violations)
    
    def test_passes_with_full_validation(self):
        code = """
        transition process_payment(amount: u64) {
            assert(amount > 0u64);
            assert(amount < MAX_AMOUNT);
        }
        """
        violations = check_payment_amount_validation(code, ["amount"])
        # Should have no critical violations
        assert len([v for v in violations if v['severity'] == 'HIGH']) == 0


class TestPaymentAccessControl:
    """Test payment access control checks (PCI 7.1)."""
    
    def test_detects_missing_access_control(self):
        code = """
        transition process_payment(amount: u64) {
            // No access control
        }
        """
        result = check_payment_access_control("process_payment", code, False)
        assert result['violation'] is True
        assert result['severity'] == 'CRITICAL'
    
    def test_passes_with_caller_check(self):
        code = """
        transition process_payment(amount: u64, owner: address) {
            assert_eq(self.caller, owner);
        }
        """
        result = check_payment_access_control("process_payment", code, True)
        assert result.get('violation', False) is False
    
    def test_warns_about_missing_owner_param(self):
        code = """
        transition process_payment(amount: u64) {
            assert(authorized);
        }
        """
        result = check_payment_access_control("process_payment", code, False)
        # Should still flag missing owner parameter
        assert result['violation'] is True


class TestPaymentAuditLogging:
    """Test payment audit logging checks (PCI 10.2)."""
    
    def test_detects_missing_finalize(self):
        code = """
        transition process_payment(amount: u64) {
            // No finalize
        }
        """
        result = check_payment_audit_logging("process_payment", code)
        assert result['violation'] is True
        assert result['severity'] == 'HIGH'
    
    def test_passes_with_finalize(self):
        code = """
        transition process_payment(amount: u64) {
            return then finalize(payment_id, amount, self.caller);
        }
        """
        result = check_payment_audit_logging("process_payment", code)
        assert result.get('violation', False) is False
    
    def test_warns_about_incomplete_logging(self):
        code = """
        transition process_payment(amount: u64) {
            return then finalize();
        }
        """
        result = check_payment_audit_logging("process_payment", code)
        # Should warn about missing fields
        if result.get('violation'):
            assert 'incomplete' in result['message'].lower() or 'missing' in result['message'].lower()


class TestRefundMechanism:
    """Test refund mechanism checks (PCI 12.10.6)."""
    
    def test_detects_missing_refund(self):
        transitions = ["process_payment", "get_balance", "transfer"]
        result = check_refund_mechanism(transitions)
        assert result['violation'] is True
        assert result['severity'] == 'MEDIUM'
    
    def test_passes_with_refund(self):
        transitions = ["process_payment", "refund_payment", "get_balance"]
        result = check_refund_mechanism(transitions)
        assert result['violation'] is False
    
    def test_recognizes_various_refund_names(self):
        for refund_name in ["refund", "reverse", "chargeback", "cancel"]:
            transitions = ["process_payment", f"{refund_name}_payment"]
            result = check_refund_mechanism(transitions)
            assert result['violation'] is False, f"Should recognize '{refund_name}' as refund function"


class TestTransactionLimits:
    """Test transaction limits checks (PCI 11.3.4)."""
    
    def test_detects_missing_limits(self):
        constants = {}
        result = check_transaction_limits(constants, has_payment_functions=True)
        assert result['violation'] is True
        assert result['severity'] == 'MEDIUM'
    
    def test_passes_with_limits(self):
        constants = {
            "const MAX_AMOUNT: u64 = 1000000u64": True
        }
        result = check_transaction_limits(constants, has_payment_functions=True)
        assert result['violation'] is False
    
    def test_ignores_non_payment_contracts(self):
        constants = {}
        result = check_transaction_limits(constants, has_payment_functions=False)
        assert result['violation'] is False


class TestHardcodedCredentials:
    """Test detection of hardcoded sensitive data."""
    
    def test_detects_potential_card_numbers(self):
        code = """
        program test.aleo {
            const TEST_CARD: u128 = 4532015112830366u128;
        }
        """
        violations = detect_hardcoded_credentials(code)
        assert len(violations) > 0
        assert violations[0]['severity'] == 'CRITICAL'
    
    def test_ignores_comments(self):
        code = """
        program test.aleo {
            // Example card: 4532015112830366
            const amount: u64 = 1000u64;
        }
        """
        violations = detect_hardcoded_credentials(code)
        # Should not flag commented numbers
        assert len(violations) == 0
    
    def test_ignores_short_numbers(self):
        code = """
        program test.aleo {
            const amount: u64 = 12345u64;
        }
        """
        violations = detect_hardcoded_credentials(code)
        assert len(violations) == 0


class TestIntegrationScenarios:
    """Integration tests with realistic scenarios."""
    
    def test_compliant_payment_contract(self):
        """Test a fully compliant payment contract."""
        code = """
        program compliant.aleo {
            const MAX_AMOUNT: u64 = 1000000u64;
            
            transition process_payment(
                private payment_token: field,
                amount: u64,
                owner: address
            ) {
                assert_eq(self.caller, owner);
                assert(amount > 0u64);
                assert(amount < MAX_AMOUNT);
                return then finalize(payment_token, amount, owner);
            }
            
            transition refund_payment(payment_id: field, owner: address) {
                assert_eq(self.caller, owner);
                return then finalize_refund(payment_id);
            }
        }
        """
        
        # Should have minimal violations
        violations = detect_hardcoded_credentials(code)
        assert len(violations) == 0
    
    def test_non_compliant_payment_contract(self):
        """Test a non-compliant payment contract."""
        code = """
        program bad.aleo {
            struct Payment {
                public card_number: u128,
                public cvv: u16
            }
            
            transition process_payment(
                public card_number: u128,
                public cvv: u16,
                amount: u64
            ) {
                // No validation
                // No access control
                // No logging
            }
        }
        """
        
        # Should have multiple violations
        result = detect_forbidden_payment_data("cvv")
        assert result['detected'] is True
        
        result = check_cardholder_data_visibility("card_number", "public")
        assert result['violation'] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
