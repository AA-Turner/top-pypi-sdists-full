"""PCI-DSS compliance rules for payment contracts."""

import re
from typing import List, Dict, Any, Pattern


# PCI-DSS Forbidden Data Patterns
FORBIDDEN_PAYMENT_PATTERNS = {
    'cvv': r'\b(cvv|cvc|cid|cav|csc)\b',
    'pin': r'\b(pin|pinblock|pin_block)\b',
    'full_track': r'\b(track_?data|magnetic|mag_stripe)\b',
    'card_number': r'\b\d{13,19}\b',  # Detects potential card numbers
}

# Keywords that indicate cardholder data
CARDHOLDER_DATA_KEYWORDS = [
    'card', 'pan', 'payment', 'account_number', 'cardholder',
    'card_number', 'cardnumber', 'cc', 'credit_card',
    'debit', 'expiry', 'expiration', 'billing'
]

# Keywords that indicate payment/financial operations
PAYMENT_FUNCTION_KEYWORDS = [
    'payment', 'pay', 'transfer', 'send', 'deposit',
    'withdraw', 'swap', 'trade', 'buy', 'sell',
    'purchase', 'checkout', 'process', 'refund',
    'stake', 'unstake', 'claim', 'reward'
]


def is_payment_function(function_name: str, function_body: str) -> bool:
    """
    Determine if a function handles payment operations.
    
    Args:
        function_name: Name of the function/transition
        function_body: Body of the function
        
    Returns:
        True if function appears to handle payments
    """
    name_lower = function_name.lower()
    body_lower = function_body.lower()
    
    # Check function name
    if any(keyword in name_lower for keyword in PAYMENT_FUNCTION_KEYWORDS):
        return True
    
    # Check for amount/value parameters with financial operations
    has_amount = any(word in body_lower for word in ['amount', 'value', 'balance'])
    has_transfer = any(word in body_lower for word in ['transfer', 'send', 'receive'])
    
    return has_amount and has_transfer


def detect_forbidden_payment_data(identifier_name: str, context: str = "") -> Dict[str, Any]:
    """
    Detect forbidden payment data in variable/field names.
    
    PCI-DSS Requirement 3.2: Do not store sensitive authentication data after authorization.
    
    Args:
        identifier_name: Name of variable, field, or parameter
        context: Surrounding code context
        
    Returns:
        Dictionary with detection results or None
    """
    name_lower = identifier_name.lower()
    
    for data_type, pattern in FORBIDDEN_PAYMENT_PATTERNS.items():
        if re.search(pattern, name_lower):
            return {
                'detected': True,
                'type': data_type,
                'identifier': identifier_name,
                'severity': 'CRITICAL',
                'pci_requirement': '3.2',
                'message': f'Forbidden to store {data_type.upper()} data',
                'remediation': 'Use payment tokens or hashed references instead'
            }
    
    return {'detected': False}


def check_cardholder_data_visibility(field_name: str, visibility: str) -> Dict[str, Any]:
    """
    Check if cardholder data has proper visibility (must be private).
    
    PCI-DSS Requirement 3.4: Render PAN unreadable anywhere it is stored.
    
    Args:
        field_name: Name of the field
        visibility: Visibility modifier ('public', 'private', etc.)
        
    Returns:
        Dictionary with check results
    """
    field_lower = field_name.lower()
    
    # Check if field contains cardholder data
    is_cardholder_data = any(
        keyword in field_lower for keyword in CARDHOLDER_DATA_KEYWORDS
    )
    
    if is_cardholder_data and visibility == 'public':
        return {
            'violation': True,
            'severity': 'CRITICAL',
            'pci_requirement': '3.4',
            'field': field_name,
            'message': f'Cardholder data field "{field_name}" must be private',
            'remediation': f'Change to: private {field_name}',
            'cwe': 'CWE-312: Cleartext Storage of Sensitive Information'
        }
    
    return {'violation': False}


def check_payment_amount_validation(function_body: str, param_names: List[str]) -> List[Dict[str, Any]]:
    """
    Check if payment amounts are properly validated.
    
    PCI-DSS Requirement 6.5.1: Injection flaws, particularly SQL injection.
    Also covers input validation requirements.
    
    Args:
        function_body: Body of the payment function
        param_names: List of parameter names
        
    Returns:
        List of validation violations
    """
    violations = []
    
    # Find amount/value parameters
    amount_params = [
        p for p in param_names 
        if any(word in p.lower() for word in ['amount', 'value', 'quantity', 'price'])
    ]
    
    for param in amount_params:
        # Check for positive value validation (> 0 or > MIN_AMOUNT or >=)
        has_positive_check = bool(re.search(
            rf'{param}\s*>=?\s*\w+',
            function_body
        )) and ('>' in function_body or '>=' in function_body)
        
        if not has_positive_check:
            violations.append({
                'severity': 'HIGH',
                'pci_requirement': '6.5.1',
                'param': param,
                'message': f'Payment amount "{param}" not validated for positive values',
                'remediation': f'Add: assert({param} > 0u64);',
                'cwe': 'CWE-20: Improper Input Validation'
            })
        
        # Check for maximum limit
        has_max_check = bool(re.search(
            rf'{param}\s*<\s*\w+',
            function_body
        ))
        
        if not has_max_check:
            violations.append({
                'severity': 'MEDIUM',
                'pci_requirement': '6.5.1',
                'param': param,
                'message': f'Payment amount "{param}" has no upper limit',
                'remediation': f'Add: assert({param} < MAX_AMOUNT);',
                'details': 'Define reasonable transaction limits to prevent fraud'
            })
    
    return violations


def check_payment_access_control(function_name: str, function_body: str, has_owner_param: bool) -> Dict[str, Any]:
    """
    Check if payment function has proper access control.
    
    PCI-DSS Requirement 7.1: Limit access to cardholder data by business need to know.
    
    Args:
        function_name: Name of the function
        function_body: Body of the function
        has_owner_param: Whether function has an owner/address parameter
        
    Returns:
        Dictionary with check results
    """
    # Access control patterns
    access_patterns = [
        r'assert_eq\s*\(\s*self\.caller',
        r'assert\s*\(\s*self\.caller\s*==',
        r'require\s*\(\s*authorized',
        r'assert\s*\(\s*is_owner',
        r'only_owner',
        r'onlyOwner'
    ]
    
    has_access_control = any(
        re.search(pattern, function_body)
        for pattern in access_patterns
    )
    
    if not has_access_control:
        return {
            'violation': True,
            'severity': 'CRITICAL',
            'pci_requirement': '7.1',
            'function': function_name,
            'message': f'Payment function "{function_name}" lacks access control',
            'remediation': 'Add: assert_eq(self.caller, authorized_address);',
            'cwe': 'CWE-862: Missing Authorization',
            'details': 'All payment functions must verify caller authorization'
        }
    
    if not has_owner_param:
        return {
            'violation': True,
            'severity': 'HIGH',
            'pci_requirement': '7.1',
            'function': function_name,
            'message': 'Payment function should require owner/address parameter',
            'remediation': 'Add owner: address parameter and verify against self.caller'
        }
    
    return {'violation': False}


def check_payment_audit_logging(function_name: str, function_body: str) -> Dict[str, Any]:
    """
    Check if payment function has audit logging.
    
    PCI-DSS Requirement 10.2: Implement automated audit trails for all system components.
    
    Args:
        function_name: Name of the function
        function_body: Body of the function
        
    Returns:
        Dictionary with check results
    """
    # Check for finalize (async logging in Leo)
    has_finalize = 'then finalize' in function_body or 'finalize(' in function_body
    
    if not has_finalize:
        return {
            'violation': True,
            'severity': 'HIGH',
            'pci_requirement': '10.2',
            'function': function_name,
            'message': f'Payment function "{function_name}" lacks audit logging',
            'remediation': 'Add: return then finalize(payment_id, amount, caller);',
            'details': 'All payment transactions must be logged for audit trail'
        }
    
    # Check if finalize includes essential audit fields
    required_fields = ['amount', 'address', 'caller', 'id', 'timestamp']
    missing_fields = [
        field for field in required_fields
        if field not in function_body.lower()
    ]
    
    if missing_fields and len(missing_fields) >= 3:
        return {
            'violation': True,
            'severity': 'MEDIUM',
            'pci_requirement': '10.2',
            'function': function_name,
            'message': 'Incomplete audit logging - missing key fields',
            'details': f'Consider logging: {", ".join(missing_fields[:3])}',
            'remediation': 'Include transaction amount, parties, timestamp, and unique ID'
        }
    
    return {'violation': False}


def check_refund_mechanism(transitions: List[str]) -> Dict[str, Any]:
    """
    Check if payment system has refund/reversal capability.
    
    PCI-DSS Requirement 12.10.6: Develop and implement a process to respond to security incidents.
    
    Args:
        transitions: List of transition names in the program
        
    Returns:
        Dictionary with check results
    """
    refund_keywords = ['refund', 'reverse', 'cancel', 'chargeback', 'rollback']
    
    has_refund = any(
        any(keyword in t.lower() for keyword in refund_keywords)
        for t in transitions
    )
    
    if not has_refund:
        return {
            'violation': True,
            'severity': 'MEDIUM',
            'pci_requirement': '12.10.6',
            'message': 'Payment system lacks refund/reversal mechanism',
            'remediation': 'Implement refund_payment() transition for dispute resolution',
            'details': 'Ability to reverse fraudulent transactions is important for incident response'
        }
    
    return {'violation': False}


def check_transaction_limits(constants: Dict[str, Any], has_payment_functions: bool) -> Dict[str, Any]:
    """
    Check if reasonable transaction limits are defined.
    
    PCI-DSS Requirement 11.3.4: Detect, alert on, and address anomalies.
    
    Args:
        constants: Dictionary of constants defined in the program
        has_payment_functions: Whether program has payment functions
        
    Returns:
        Dictionary with check results
    """
    if not has_payment_functions:
        return {'violation': False}
    
    limit_keywords = ['max_amount', 'max_transaction', 'limit', 'threshold', 'max_value']
    
    has_limit = any(
        any(keyword in const_name.lower() for keyword in limit_keywords)
        for const_name in constants.keys()
    )
    
    if not has_limit:
        return {
            'violation': True,
            'severity': 'MEDIUM',
            'pci_requirement': '11.3.4',
            'message': 'No transaction limits defined',
            'remediation': 'Define: const MAX_AMOUNT: u64 = 1000000u64; // Set appropriate limit',
            'details': 'Transaction limits help detect and prevent fraud'
        }
    
    return {'violation': False}


def detect_hardcoded_credentials(source_code: str) -> List[Dict[str, Any]]:
    """
    Detect hardcoded sensitive data in source code.
    
    Args:
        source_code: Complete source code
        
    Returns:
        List of detected issues
    """
    violations = []
    lines = source_code.split('\n')
    
    # Pattern for potential card numbers (13-19 digits)
    card_pattern = re.compile(r'\b\d{13,19}\b')
    
    for i, line in enumerate(lines, 1):
        # Skip comments
        if '//' in line:
            line = line[:line.index('//')]
        if '/*' in line or '*/' in line:
            continue
            
        # Check for card number patterns
        matches = card_pattern.findall(line)
        for match in matches:
            # Simple Luhn algorithm check to reduce false positives
            if len(match) >= 13:
                violations.append({
                    'line': i,
                    'severity': 'CRITICAL',
                    'pci_requirement': '3.2',
                    'message': f'Potential credit card number detected: {match[:4]}...{match[-4:]}',
                    'remediation': 'Never hardcode payment card numbers',
                    'code': line.strip()
                })
    
    return violations
