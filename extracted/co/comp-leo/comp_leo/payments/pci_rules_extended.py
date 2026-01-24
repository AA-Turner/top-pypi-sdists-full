"""Extended PCI-DSS compliance rules for comprehensive payment security."""

import re
from typing import List, Dict, Any, Set, Tuple

# ============================================================================
# ENHANCED DETECTION PATTERNS
# ============================================================================

# Expanded forbidden payment data patterns (PCI-DSS 3.2)
FORBIDDEN_PAYMENT_PATTERNS_EXTENDED = {
    # CVV variants
    'cvv': r'\b(cvv2?|cvc2?|cid|cav|csc|cvd|cvn|card_?verification|security_?code)\b',
    
    # PIN variants
    'pin': r'\b(pin|pinblock|pin_block|pin_offset|pvv|pvki|personal_?identification)\b',
    
    # Full track data
    'full_track': r'\b(track_?[12]_?data|magnetic|mag_stripe|stripe_data|full_?track)\b',
    
    # Service code and discretionary data
    'service_code': r'\b(service_?code|discretionary_?data)\b',
    
    # 3D-Secure sensitive authentication values
    'cav': r'\b(cav2|cavv|aav|ucaf|authentication_?value)\b',
    
    # Security questions/answers
    'security_answers': r'\b(security_?(answer|question)|mother.*maiden|challenge_?(answer|response))\b',
}

# Blockchain-specific sensitive patterns
BLOCKCHAIN_SENSITIVE_PATTERNS = {
    # Aleo private keys (APrivateKey1... - flexible length for testing)
    'aleo_private_key': r'\bAPrivateKey1[a-z0-9]{40,}\b',
    
    # Aleo view keys
    'aleo_view_key': r'\bAViewKey1[a-z0-9]{40,}\b',
    
    # Generic private key patterns
    'private_key_generic': r'\b(private_?key|priv_?key|secret_?key)\s*[:=]\s*["\'][a-zA-Z0-9+/=]{32,}["\']\b',
    
    # Mnemonic seed phrases (12, 15, 18, 21, 24 words)
    'seed_phrase': r'\b([a-z]+\s){11,23}[a-z]+\b',
    
    # Hardcoded credentials
    'hardcoded_password': r'\b(password|passwd|pwd|secret)\s*[:=]\s*["\'][^"\']{4,}["\']\b',
}

# Weak cryptographic patterns (PCI-DSS 4.1)
WEAK_CRYPTO_PATTERNS = {
    'weak_hash': r'\b(md5|sha1|crc32)\b',
    'weak_cipher': r'\b(des|rc4|blowfish)\b(?!\w)',  # Avoid matching in comments
    'hardcoded_salt': r'\bsalt\s*[:=]\s*["\'][^"\']+["\']\b',
}

# Insecure randomness patterns (PCI-DSS 6.5.3)
WEAK_RANDOMNESS_PATTERNS = {
    'predictable_random': r'\b(rand|random)\s*\(\s*\)\s*[%*]\s*\d+\b',
    'timestamp_as_random': r'\b(timestamp|time|now)\s*as\s*(random|seed|nonce)\b',
    'sequential_id': r'\b(id|nonce|salt)\s*[:=]\s*(\d+|0x[0-9a-f]+)\b',
}

# ============================================================================
# REQUIREMENT 2.2: SECURE CONFIGURATION
# ============================================================================

def check_secure_configuration(program_source: str, transitions: List[Any]) -> List[Dict[str, Any]]:
    """
    PCI-DSS 2.2: Develop configuration standards for system components.
    
    Checks for:
    - Default admin addresses
    - Test mode flags
    - Debug code in production
    - Hardcoded addresses
    """
    violations = []
    
    # Pattern for hardcoded admin addresses (handles Leo syntax: const admin: address = aleo1...)
    admin_patterns = [
        r'admin\s*:\s*address\s*=\s*aleo1[a-z0-9]+',  # Leo: admin: address = aleo1...
        r'owner\s*:\s*address\s*=\s*aleo1[a-z0-9]+',  # Leo: owner: address = aleo1...
        r'admin\s*=\s*aleo1[a-z0-9]+',  # Simple: admin = aleo1...
        r'owner\s*=\s*aleo1[a-z0-9]+',  # Simple: owner = aleo1...
        r'default_?admin',
        r'test_?admin',
    ]
    
    for i, line in enumerate(program_source.split('\n'), 1):
        line_lower = line.lower()
        
        # Check for hardcoded admin addresses
        for pattern in admin_patterns:
            if re.search(pattern, line_lower):
                violations.append({
                    'line': i,
                    'severity': 'HIGH',
                    'pci_requirement': '2.2.1',
                    'message': 'Hardcoded admin/owner address detected',
                    'code': line.strip(),
                    'remediation': 'Pass admin address as parameter or use initialization function',
                    'cwe': 'CWE-798: Use of Hard-coded Credentials'
                })
        
        # Check for test/debug mode (handles Leo syntax: const test_mode: bool = true)
        if re.search(r'\b(test_?mode|debug_?mode|dev_?mode)\s*:\s*bool\s*=\s*true\b', line_lower) or \
           re.search(r'\b(test_?mode|debug_?mode|dev_?mode)\s*=\s*true\b', line_lower):
            violations.append({
                'line': i,
                'severity': 'CRITICAL',
                'pci_requirement': '2.2.2',
                'message': 'Test/debug mode flag detected',
                'code': line.strip(),
                'remediation': 'Remove test mode flags from production code',
                'cwe': 'CWE-489: Active Debug Code'
            })
        
        # Check for TODO/FIXME/HACK comments indicating incomplete security
        if re.search(r'//\s*(TODO|FIXME|HACK|XXX).*\b(security|auth|admin|password)\b', line, re.IGNORECASE):
            violations.append({
                'line': i,
                'severity': 'MEDIUM',
                'pci_requirement': '2.2.4',
                'message': 'Incomplete security implementation detected in comments',
                'code': line.strip(),
                'remediation': 'Complete security implementation before deployment',
                'cwe': 'CWE-1164: Irrelevant Code'
            })
    
    return violations


# ============================================================================
# REQUIREMENT 4.1: STRONG CRYPTOGRAPHY
# ============================================================================

def check_strong_cryptography(program_source: str) -> List[Dict[str, Any]]:
    """
    PCI-DSS 4.1: Use strong cryptography and security protocols.
    
    Checks for:
    - Weak hash functions (MD5, SHA-1)
    - Weak encryption algorithms
    - Hardcoded cryptographic keys/salts
    """
    violations = []
    
    for i, line in enumerate(program_source.split('\n'), 1):
        line_lower = line.lower()
        
        # Check for weak hash functions
        for crypto_type, pattern in WEAK_CRYPTO_PATTERNS.items():
            if re.search(pattern, line_lower):
                if crypto_type == 'weak_hash':
                    violations.append({
                        'line': i,
                        'severity': 'HIGH',
                        'pci_requirement': '4.1.1',
                        'message': f'Weak hash function detected: {line.strip()}',
                        'code': line.strip(),
                        'remediation': 'Use SHA-256, SHA-3, or Poseidon hash (native to Leo)',
                        'cwe': 'CWE-327: Use of Broken Cryptographic Algorithm'
                    })
                elif crypto_type == 'weak_cipher':
                    violations.append({
                        'line': i,
                        'severity': 'CRITICAL',
                        'pci_requirement': '4.1.1',
                        'message': f'Weak encryption algorithm detected: {line.strip()}',
                        'code': line.strip(),
                        'remediation': 'Use AES-256 or stronger encryption',
                        'cwe': 'CWE-326: Inadequate Encryption Strength'
                    })
                elif crypto_type == 'hardcoded_salt':
                    violations.append({
                        'line': i,
                        'severity': 'HIGH',
                        'pci_requirement': '4.1.2',
                        'message': 'Hardcoded cryptographic salt detected',
                        'code': line.strip(),
                        'remediation': 'Generate salt dynamically or pass as secure parameter',
                        'cwe': 'CWE-760: Use of Predictable Salt'
                    })
    
    return violations


# ============================================================================
# REQUIREMENT 6.5.3: INSECURE CRYPTOGRAPHIC STORAGE
# ============================================================================

def check_insecure_cryptographic_storage(program_source: str) -> List[Dict[str, Any]]:
    """
    PCI-DSS 6.5.3: Insecure cryptographic storage.
    
    Checks for:
    - Weak randomness
    - Predictable IDs/nonces
    - Timestamp-based randomness
    """
    violations = []
    
    for i, line in enumerate(program_source.split('\n'), 1):
        line_lower = line.lower()
        
        # Check for weak randomness patterns
        for random_type, pattern in WEAK_RANDOMNESS_PATTERNS.items():
            if re.search(pattern, line_lower):
                if random_type == 'predictable_random':
                    violations.append({
                        'line': i,
                        'severity': 'HIGH',
                        'pci_requirement': '6.5.3',
                        'message': 'Weak random number generation detected',
                        'code': line.strip(),
                        'remediation': 'Use ChaCha20 RNG or Aleo\'s native randomness',
                        'cwe': 'CWE-338: Use of Cryptographically Weak PRNG'
                    })
                elif random_type == 'timestamp_as_random':
                    violations.append({
                        'line': i,
                        'severity': 'HIGH',
                        'pci_requirement': '6.5.3',
                        'message': 'Timestamp used as randomness source',
                        'code': line.strip(),
                        'remediation': 'Use cryptographically secure random source',
                        'cwe': 'CWE-330: Use of Insufficiently Random Values'
                    })
                elif random_type == 'sequential_id':
                    violations.append({
                        'line': i,
                        'severity': 'MEDIUM',
                        'pci_requirement': '6.5.3',
                        'message': 'Sequential or hardcoded ID/nonce detected',
                        'code': line.strip(),
                        'remediation': 'Generate IDs using secure random values',
                        'cwe': 'CWE-341: Predictable Seed in PRNG'
                    })
    
    return violations


# ============================================================================
# REQUIREMENT 8.2: STRONG AUTHENTICATION (Multi-Signature)
# ============================================================================

def check_multi_signature_requirements(transitions: List[Any], program_source: str) -> List[Dict[str, Any]]:
    """
    PCI-DSS 8.2: Implement strong authentication.
    Adapted for blockchain: Multi-signature for high-value operations.
    
    Checks for:
    - Multi-sig on admin functions
    - Multi-sig on high-value transfers
    - Threshold signature verification
    """
    violations = []
    
    # Keywords indicating admin functions
    admin_keywords = ['admin', 'owner', 'pause', 'upgrade', 'migrate', 'emergency', 'withdraw_all']
    
    # Keywords indicating high-value operations
    high_value_keywords = ['withdraw', 'transfer_all', 'bulk_transfer', 'sweep']
    
    for transition in transitions:
        name_lower = transition.name.lower()
        body_lower = transition.body.lower()
        
        # Check if it's an admin function
        is_admin = any(keyword in name_lower for keyword in admin_keywords)
        
        # Check if it's a high-value operation
        is_high_value = any(keyword in name_lower for keyword in high_value_keywords)
        
        # Check for multi-sig patterns
        has_multi_sig = any(pattern in body_lower for pattern in [
            'multi_sig', 'multisig', 'threshold', 'quorum',
            'verify_signatures', 'check_signatures', 'n_of_m'
        ])
        
        if is_admin and not has_multi_sig:
            violations.append({
                'line': transition.line_start,
                'function': transition.name,
                'severity': 'CRITICAL',
                'pci_requirement': '8.2.1',
                'message': f'Admin function "{transition.name}" lacks multi-signature protection',
                'remediation': 'Add multi-signature verification: assert(verify_multi_sig(signers, threshold, message));',
                'cwe': 'CWE-306: Missing Authentication for Critical Function'
            })
        
        if is_high_value and not has_multi_sig:
            violations.append({
                'line': transition.line_start,
                'function': transition.name,
                'severity': 'HIGH',
                'pci_requirement': '8.2.3',
                'message': f'High-value function "{transition.name}" lacks multi-signature protection',
                'remediation': 'Implement multi-sig for operations above threshold amount',
                'cwe': 'CWE-306: Missing Authentication for Critical Function'
            })
    
    return violations


# ============================================================================
# REQUIREMENT 10.3: DETAILED AUDIT LOGGING
# ============================================================================

def check_detailed_audit_logging(transitions: List[Any], program_source: str) -> List[Dict[str, Any]]:
    """
    PCI-DSS 10.3: Record audit trail entries for all system components.
    
    Checks for:
    - Complete audit fields (who, what, when, where, how)
    - Timestamp in logs
    - User identification in logs
    - Action type in logs
    - Success/failure status
    """
    violations = []
    
    from ..payments.pci_rules import is_payment_function
    
    for transition in transitions:
        # Only check payment/sensitive functions
        if not is_payment_function(transition.name, transition.body):
            continue
        
        body_lower = transition.body.lower()
        
        # Check for finalize (audit log mechanism in Leo)
        has_finalize = 'finalize' in body_lower or 'then finalize' in body_lower
        
        if not has_finalize:
            violations.append({
                'line': transition.line_start,
                'function': transition.name,
                'severity': 'HIGH',
                'pci_requirement': '10.3.1',
                'message': f'Payment function "{transition.name}" has no audit logging (finalize)',
                'remediation': 'Add: return then finalize(tx_id, caller, amount, timestamp);',
                'cwe': 'CWE-778: Insufficient Logging'
            })
            continue
        
        # Check for required audit fields
        required_fields = {
            'user': ['caller', 'self.caller', 'sender', 'user'],
            'action': ['action', 'operation', 'function', 'event_type'],
            'timestamp': ['timestamp', 'block.timestamp', 'time'],
            'amount': ['amount', 'value', 'quantity'],
            'status': ['status', 'success', 'result'],
        }
        
        missing_fields = []
        for field_type, patterns in required_fields.items():
            if not any(pattern in body_lower for pattern in patterns):
                missing_fields.append(field_type)
        
        if missing_fields:
            violations.append({
                'line': transition.line_start,
                'function': transition.name,
                'severity': 'MEDIUM',
                'pci_requirement': '10.3.3',
                'message': f'Audit log missing required fields: {", ".join(missing_fields)}',
                'remediation': f'Include in finalize: {", ".join(missing_fields)}',
                'cwe': 'CWE-778: Insufficient Logging'
            })
    
    return violations


# ============================================================================
# REQUIREMENT 11.2: VULNERABILITY DETECTION
# ============================================================================

def check_common_vulnerabilities(program_source: str, transitions: List[Any]) -> List[Dict[str, Any]]:
    """
    PCI-DSS 11.2: Run internal and external network vulnerability scans.
    Adapted: Detect common smart contract vulnerabilities.
    
    Checks for:
    - Reentrancy patterns
    - Integer overflow risks
    - Unchecked external calls
    - Missing error handling
    """
    violations = []
    
    for transition in transitions:
        body = transition.body
        body_lower = body.lower()
        
        # Check for external calls without validation
        external_call_pattern = r'\.aleo/[a-z_]+/[a-z_]+'
        if re.search(external_call_pattern, body_lower):
            # Check if there's validation after the call
            has_validation = any(pattern in body_lower for pattern in [
                'assert', 'require', 'check', 'verify', 'if', 'is_err'
            ])
            
            if not has_validation:
                violations.append({
                    'line': transition.line_start,
                    'function': transition.name,
                    'severity': 'HIGH',
                    'pci_requirement': '11.2.1',
                    'message': f'Unchecked external call in "{transition.name}"',
                    'remediation': 'Validate external call results: assert(result.is_ok());',
                    'cwe': 'CWE-252: Unchecked Return Value'
                })
        
        # Check for potential integer overflow
        arithmetic_ops = ['+', '-', '*', '/', '**']
        if any(op in body for op in arithmetic_ops):
            # Check for overflow protection
            has_overflow_check = any(pattern in body_lower for pattern in [
                'checked_add', 'checked_sub', 'checked_mul',
                'safe_add', 'safe_sub', 'safe_mul',
                'assert.*<', 'assert.*>', 'require.*<', 'require.*>'
            ])
            
            # Look for amount/value operations
            if any(word in body_lower for word in ['amount', 'balance', 'value']) and not has_overflow_check:
                violations.append({
                    'line': transition.line_start,
                    'function': transition.name,
                    'severity': 'MEDIUM',
                    'pci_requirement': '11.2.3',
                    'message': f'Potential integer overflow in "{transition.name}"',
                    'remediation': 'Use checked arithmetic or add overflow assertions',
                    'cwe': 'CWE-190: Integer Overflow'
                })
        
        # Check for reentrancy-like patterns (state change after external call)
        lines = body.split('\n')
        external_call_found = False
        state_change_after_call = False
        
        for line in lines:
            if '.aleo/' in line.lower():
                external_call_found = True
            elif external_call_found and ('mapping::' in line.lower() or 'self.' in line.lower()):
                state_change_after_call = True
                break
        
        if state_change_after_call:
            violations.append({
                'line': transition.line_start,
                'function': transition.name,
                'severity': 'HIGH',
                'pci_requirement': '11.2.2',
                'message': f'Potential reentrancy: state change after external call in "{transition.name}"',
                'remediation': 'Follow checks-effects-interactions pattern: update state before external calls',
                'cwe': 'CWE-841: Improper Enforcement of Behavioral Workflow'
            })
    
    return violations


# ============================================================================
# BLOCKCHAIN-SPECIFIC CHECKS
# ============================================================================

def check_private_key_exposure(program_source: str) -> List[Dict[str, Any]]:
    """
    Check for exposed private keys, view keys, or seed phrases in code.
    Critical for blockchain payment security.
    """
    violations = []
    
    for i, line in enumerate(program_source.split('\n'), 1):
        # Check for each blockchain-sensitive pattern
        for pattern_type, pattern in BLOCKCHAIN_SENSITIVE_PATTERNS.items():
            if re.search(pattern, line):
                violations.append({
                    'line': i,
                    'severity': 'CRITICAL',
                    'pci_requirement': '3.5.1',
                    'message': f'Exposed {pattern_type.replace("_", " ")} detected',
                    'code': line.strip()[:50] + '...',  # Truncate for security
                    'remediation': 'Remove all private keys from source code. Use secure key management.',
                    'cwe': 'CWE-798: Hard-coded Credentials'
                })
    
    return violations


def check_rate_limiting(transitions: List[Any], program_source: str) -> List[Dict[str, Any]]:
    """
    PCI-DSS 12.3: Usage policies - Check for rate limiting on payment functions.
    """
    violations = []
    
    from ..payments.pci_rules import is_payment_function
    
    for transition in transitions:
        if not is_payment_function(transition.name, transition.body):
            continue
        
        body_lower = transition.body.lower()
        
        # Check for rate limiting patterns
        has_rate_limit = any(pattern in body_lower for pattern in [
            'rate_limit', 'cooldown', 'last_call', 'time_between',
            'daily_limit', 'per_user_limit', 'velocity_check'
        ])
        
        if not has_rate_limit:
            violations.append({
                'line': transition.line_start,
                'function': transition.name,
                'severity': 'MEDIUM',
                'pci_requirement': '12.3.5',
                'message': f'Payment function "{transition.name}" lacks rate limiting',
                'remediation': 'Implement rate limiting: assert(block.timestamp - last_call[caller] > COOLDOWN);',
                'cwe': 'CWE-770: Allocation of Resources Without Limits'
            })
    
    return violations
