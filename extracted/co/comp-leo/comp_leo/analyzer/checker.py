"""Core compliance checking engine."""

import re
from typing import List, Optional, Dict, Any
from pathlib import Path
import time

from comp_leo.analyzer.parser import LeoParser, LeoProgram, LeoFunction
from comp_leo.core.models import (
    CheckResult, Violation, Severity, ViolationType,
    ControlMapping, Remediation
)
from comp_leo.policies.rule_engine import RuleEngine


class ComplianceChecker:
    """
    Main compliance checking engine.
    
    Orchestrates parsing, rule evaluation, and scoring for Leo programs.
    """
    
    def __init__(self, policy_pack: str = "aleo-baseline"):
        self.parser = LeoParser()
        self.rule_engine = RuleEngine()
        self.policy_pack = policy_pack
        
        # Load policy pack
        self.rule_engine.load_policy_pack(policy_pack)
    
    def check_file(self, file_path: str, threshold: int = 75) -> CheckResult:
        """Run compliance checks on a Leo file."""
        start_time = time.time()
        
        # Parse
        program = self.parser.parse_file(file_path)
        
        # Run checks
        violations = self._run_checks(program)
        
        # Compute score
        score = self._compute_score(violations, len(self.rule_engine.get_enabled_rules()))
        
        end_time = time.time()
        
        result = CheckResult(
            passed=score >= threshold and all(v.severity != Severity.CRITICAL for v in violations),
            score=score,
            threshold=threshold,
            violations=violations,
            total_checks=len(self.rule_engine.get_enabled_rules()),
            policy_pack=self.policy_pack,
            scan_duration_ms=(end_time - start_time) * 1000,
            scanned_files=[file_path]
        )
        
        return result
    
    def check_directory(self, directory: str, threshold: int = 75) -> CheckResult:
        """Run compliance checks on all Leo files in a directory."""
        start_time = time.time()
        
        dir_path = Path(directory)
        leo_files = list(dir_path.rglob("*.leo"))
        
        if not leo_files:
            raise ValueError(f"No .leo files found in {directory}")
        
        all_violations = []
        scanned_files = []
        
        for leo_file in leo_files:
            program = self.parser.parse_file(str(leo_file))
            violations = self._run_checks(program)
            all_violations.extend(violations)
            scanned_files.append(str(leo_file))
        
        # Compute aggregate score
        score = self._compute_score(all_violations, len(self.rule_engine.get_enabled_rules()) * len(leo_files))
        
        end_time = time.time()
        
        result = CheckResult(
            passed=score >= threshold and all(v.severity != Severity.CRITICAL for v in all_violations),
            score=score,
            threshold=threshold,
            violations=all_violations,
            total_checks=len(self.rule_engine.get_enabled_rules()) * len(leo_files),
            policy_pack=self.policy_pack,
            scan_duration_ms=(end_time - start_time) * 1000,
            scanned_files=scanned_files
        )
        
        return result
    
    def _run_checks(self, program: LeoProgram) -> List[Violation]:
        """Run all enabled checks on a program."""
        violations = []
        
        # Run each enabled rule
        for rule in self.rule_engine.get_enabled_rules():
            rule_violations = self._apply_rule(rule, program)
            violations.extend(rule_violations)
        
        return violations
    
    def _apply_rule(self, rule: Dict[str, Any], program: LeoProgram) -> List[Violation]:
        """Apply a single rule to a program."""
        violations = []
        
        rule_id = rule["id"]
        # Replace both dashes and dots with underscores for function names
        check_func_name = f"_check_{rule_id.replace('-', '_').replace('.', '_')}"
        
        # Dynamically call check function if it exists
        if hasattr(self, check_func_name):
            check_func = getattr(self, check_func_name)
            violations = check_func(program, rule)
        
        return violations
    
    # ============================================================================
    # CHECK FUNCTIONS - Each implements a specific compliance rule
    # ============================================================================
    
    def _check_input_validation_missing(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """Check for missing input validation in transitions."""
        violations = []
        
        for transition in program.transitions:
            if not transition.has_assertions and len(transition.parameters) > 0:
                # Look for basic validation patterns
                has_validation = any([
                    "assert" in transition.body,
                    "require" in transition.body,
                    # Check for comparison operators
                    re.search(r'\w+\s*[<>!=]=?\s*\w+', transition.body)
                ])
                
                if not has_validation:
                    violations.append(self._create_violation(
                        rule=rule,
                        program=program,
                        line=transition.line_start,
                        message=f"Transition '{transition.name}' accepts inputs but lacks validation",
                        code_snippet=self._get_code_snippet(program, transition.line_start, 5),
                        remediation=Remediation(
                            description="Add assertions to validate input parameters",
                            code_example=f"assert(param > 0u64);  // Validate non-zero\nassert(param < MAX_VALUE);  // Range check",
                            automated=False
                        )
                    ))
        
        return violations
    
    def _check_state_mutation_unprotected(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """Check for unprotected state mutations."""
        violations = []
        
        for func in program.transitions + program.functions:
            if func.modifies_state:
                # Check for access control
                has_access_control = any([
                    "assert" in func.body and "self.caller" in func.body,
                    "owner" in func.body.lower(),
                    "admin" in func.body.lower(),
                    "authorized" in func.body.lower()
                ])
                
                if not has_access_control:
                    violations.append(self._create_violation(
                        rule=rule,
                        program=program,
                        line=func.line_start,
                        message=f"Function '{func.name}' mutates state without access control",
                        code_snippet=self._get_code_snippet(program, func.line_start, 3),
                        remediation=Remediation(
                            description="Add caller verification before state changes",
                            code_example="assert_eq(self.caller, owner);  // Only owner can modify",
                            automated=False
                        )
                    ))
        
        return violations
    
    def _check_logging_insufficient(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """Check for insufficient logging in critical operations."""
        violations = []
        
        critical_patterns = [
            (r'Mapping::set', "State write"),
            (r'Mapping::remove', "State deletion"),
            (r'transfer', "Token transfer"),
        ]
        
        for func in program.transitions:
            func_body = func.body
            
            for pattern, operation in critical_patterns:
                if re.search(pattern, func_body):
                    # Check for logging (events, returns, etc.)
                    has_logging = any([
                        "return" in func_body,
                        "Future" in func_body,  # Async operations are logged
                        "emit" in func_body
                    ])
                    
                    if not has_logging and not func.is_async:
                        violations.append(self._create_violation(
                            rule=rule,
                            program=program,
                            line=func.line_start,
                            message=f"{operation} in '{func.name}' lacks audit trail",
                            code_snippet=self._get_code_snippet(program, func.line_start, 5),
                            remediation=Remediation(
                                description="Return transaction hash or emit event for audit trail",
                                code_example="return tx_hash;  // Log operation for audit",
                                automated=False
                            )
                        ))
                    break
        
        return violations
    
    def _check_integer_overflow_risk(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """Check for potential integer overflow/underflow."""
        violations = []
        
        arithmetic_ops = ['+', '-', '*', '/']
        
        for func in program.transitions + program.functions:
            lines = func.body.split('\n')
            
            for i, line in enumerate(lines):
                # Check for arithmetic without bounds checking
                if any(op in line for op in arithmetic_ops):
                    # Look for u8, u16, u32, u64, u128 operations
                    if re.search(r'\d+u(8|16|32|64|128)', line):
                        # Check if surrounded by checks
                        context = '\n'.join(lines[max(0, i-2):min(len(lines), i+3)])
                        
                        has_overflow_check = any([
                            "checked_add" in context,
                            "checked_sub" in context,
                            "checked_mul" in context,
                            "assert" in context and (">" in context or "<" in context)
                        ])
                        
                        if not has_overflow_check:
                            violations.append(self._create_violation(
                                rule=rule,
                                program=program,
                                line=func.line_start + i,
                                message=f"Potential overflow in arithmetic operation",
                                code_snippet=line.strip(),
                                remediation=Remediation(
                                    description="Use checked arithmetic or add bounds validation",
                                    code_example="assert(amount <= MAX_SAFE_VALUE);\nlet result: u64 = amount + fee;",
                                    automated=False
                                )
                            ))
                            break
        
        return violations
    
    def _check_private_data_exposure(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """Check for potential privacy leaks through public fields."""
        violations = []
        
        sensitive_keywords = ['password', 'secret', 'private_key', 'ssn', 'email', 'phone']
        
        # Check struct fields
        for struct in program.structs:
            for field in struct.fields:
                field_name = field['name'].lower()
                
                if any(keyword in field_name for keyword in sensitive_keywords):
                    violations.append(self._create_violation(
                        rule=rule,
                        program=program,
                        line=struct.line_number,
                        message=f"Struct field '{field['name']}' may expose sensitive data",
                        code_snippet=f"{field['name']}: {field['type']}",
                        remediation=Remediation(
                            description="Consider using private record types for sensitive data",
                            code_example="record PrivateData {\n    owner: address,\n    secret: field  // Encrypted by default\n}",
                            automated=False
                        )
                    ))
        
        # Check public transitions with sensitive parameter names
        for transition in program.transitions:
            if transition.visibility == "public":
                for param in transition.parameters:
                    param_name = param['name'].lower()
                    if any(keyword in param_name for keyword in sensitive_keywords):
                        violations.append(self._create_violation(
                            rule=rule,
                            program=program,
                            line=transition.line_start,
                            message=f"Public transition exposes sensitive parameter '{param['name']}'",
                            remediation=Remediation(
                                description="Use private parameters or records for sensitive data",
                                code_example="transition process(private secret_data: field) { ... }",
                                automated=False
                            )
                        ))
        
        return violations
    
    def _check_reentrancy_vulnerability(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """Check for potential reentrancy vulnerabilities."""
        violations = []
        
        for func in program.transitions:
            if func.has_external_calls and func.modifies_state:
                lines = func.body.split('\n')
                
                # Check if state modification happens after external call
                external_call_line = -1
                state_mod_line = -1
                
                for i, line in enumerate(lines):
                    if '.aleo/' in line or 'call' in line.lower():
                        external_call_line = i
                    if 'Mapping::set' in line or 'Mapping::remove' in line:
                        if state_mod_line == -1:
                            state_mod_line = i
                
                if external_call_line > -1 and state_mod_line > external_call_line:
                    violations.append(self._create_violation(
                        rule=rule,
                        program=program,
                        line=func.line_start + state_mod_line,
                        message=f"State modification after external call in '{func.name}'",
                        code_snippet=self._get_code_snippet(program, func.line_start + state_mod_line, 3),
                        remediation=Remediation(
                            description="Follow checks-effects-interactions pattern: modify state before external calls",
                            automated=False
                        )
                    ))
        
        return violations
    
    def _check_mapping_key_collision(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """Check for potential mapping key collisions."""
        violations = []
        
        for mapping in program.mappings:
            # Warn if key type is too simple (e.g., u8 - only 256 possible keys)
            if mapping.key_type in ['u8', 'u16', 'bool']:
                violations.append(self._create_violation(
                    rule=rule,
                    program=program,
                    line=mapping.line_number,
                    message=f"Mapping '{mapping.name}' uses restrictive key type '{mapping.key_type}'",
                    code_snippet=f"mapping {mapping.name}: {mapping.key_type} => {mapping.value_type};",
                    remediation=Remediation(
                        description="Consider using address, field, or hash for mapping keys",
                        code_example=f"mapping {mapping.name}: field => {mapping.value_type};",
                        automated=False
                    )
                ))
        
        return violations
    
    def _check_unchecked_return_values(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """Check for unchecked return values from critical operations."""
        violations = []
        
        for func in program.transitions:
            lines = func.body.split('\n')
            
            for i, line in enumerate(lines):
                # Check for Mapping::get without error handling
                if 'Mapping::get(' in line and 'let' not in line:
                    violations.append(self._create_violation(
                        rule=rule,
                        program=program,
                        line=func.line_start + i,
                        message="Mapping::get result not assigned - may cause runtime error",
                        code_snippet=line.strip(),
                        remediation=Remediation(
                            description="Assign result to variable or use Mapping::get_or_use with default",
                            code_example="let value: Entry = Mapping::get(entries, key);",
                            automated=True,
                            confidence=0.9
                        )
                    ))
        
        return violations
    
    # ============================================================================
    # PCI-DSS PAYMENT COMPLIANCE CHECKS
    # ============================================================================
    
    def _check_pci_3_2_forbidden_data(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """
        PCI-DSS 3.2: Check for forbidden sensitive authentication data storage.
        Never store: CVV, PIN, full track data.
        """
        from comp_leo.payments import detect_forbidden_payment_data, detect_hardcoded_credentials
        
        violations = []
        
        # Check all identifiers (variables, fields, parameters)
        for struct in program.structs:
            for field in struct.fields:
                field_name = field.get('name', field.get('field_name', ''))
                result = detect_forbidden_payment_data(field_name)
                if result.get('detected'):
                    field_vis = field.get('visibility', 'private')
                    field_type = field.get('type', field.get('type_name', ''))
                    violations.append(self._create_violation(
                        rule=rule,
                        program=program,
                        line=struct.line_number,
                        message=result['message'],
                        code_snippet=f"{field_vis} {field_name}: {field_type};",
                        remediation=Remediation(
                            description=result['remediation'],
                            code_example="private payment_token: field;  // Use tokenized reference",
                            automated=False
                        )
                    ))
        
        for transition in program.transitions:
            for param in transition.parameters:
                param_name = param.get('name', param['name'] if isinstance(param, dict) else param.name)
                result = detect_forbidden_payment_data(param_name)
                if result.get('detected'):
                    violations.append(self._create_violation(
                        rule=rule,
                        program=program,
                        line=transition.line_start,
                        message=result['message'],
                        code_snippet=self._get_code_snippet(program, transition.line_start, 2),
                        remediation=Remediation(
                            description=result['remediation'],
                            code_example="Use payment tokens instead of sensitive data",
                            automated=False
                        )
                    ))
        
        # Check for hardcoded card numbers
        hardcoded = detect_hardcoded_credentials(program.source_code)
        for issue in hardcoded:
            violations.append(self._create_violation(
                rule=rule,
                program=program,
                line=issue['line'],
                message=issue['message'],
                code_snippet=issue['code'],
                remediation=Remediation(
                    description=issue['remediation'],
                    code_example="// Never hardcode payment data",
                    automated=False
                )
            ))
        
        return violations
    
    def _check_pci_3_4_cardholder_data_protection(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """
        PCI-DSS 3.4: Render cardholder data unreadable (must be private).
        """
        from comp_leo.payments import check_cardholder_data_visibility
        
        violations = []
        
        for struct in program.structs:
            for field in struct.fields:
                field_name = field.get('name', '')
                field_vis = field.get('visibility', 'private')
                field_type = field.get('type', '')
                result = check_cardholder_data_visibility(field_name, field_vis)
                if result.get('violation'):
                    violations.append(self._create_violation(
                        rule=rule,
                        program=program,
                        line=struct.line_number,
                        message=result['message'],
                        code_snippet=f"{field_vis} {field_name}: {field_type};",
                        remediation=Remediation(
                            description=result['remediation'],
                            code_example=f"private {field_name}: {field_type};",
                            automated=True,
                            confidence=0.95
                        )
                    ))
        
        # Check transition parameters
        for transition in program.transitions:
            for param in transition.parameters:
                param_name = param.get('name', '')
                param_vis = param.get('visibility', 'private')
                param_type = param.get('type', '')
                result = check_cardholder_data_visibility(param_name, param_vis)
                if result.get('violation'):
                    violations.append(self._create_violation(
                        rule=rule,
                        program=program,
                        line=transition.line_start,
                        message=result['message'],
                        code_snippet=self._get_code_snippet(program, transition.line_start, 3),
                        remediation=Remediation(
                            description=result['remediation'],
                            code_example=f"private {param_name}: {param_type}",
                            automated=True,
                            confidence=0.90
                        )
                    ))
        
        return violations
    
    def _check_pci_6_5_1_payment_input_validation(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """
        PCI-DSS 6.5.1: Check payment amount validation.
        """
        from comp_leo.payments import is_payment_function, check_payment_amount_validation
        
        violations = []
        
        for transition in program.transitions:
            if is_payment_function(transition.name, transition.body):
                param_names = [p.get('name', '') if isinstance(p, dict) else p.name for p in transition.parameters]
                issues = check_payment_amount_validation(transition.body, param_names)
                
                for issue in issues:
                    violations.append(self._create_violation(
                        rule=rule,
                        program=program,
                        line=transition.line_start,
                        message=issue['message'],
                        code_snippet=self._get_code_snippet(program, transition.line_start, 5),
                        remediation=Remediation(
                            description=issue['remediation'],
                            code_example="assert(amount > 0u64);\nassert(amount < MAX_AMOUNT);",
                            automated=False
                        )
                    ))
        
        return violations
    
    def _check_pci_7_1_payment_access_control(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """
        PCI-DSS 7.1: Restrict access to payment functions.
        """
        from comp_leo.payments import is_payment_function, check_payment_access_control
        
        violations = []
        
        for transition in program.transitions:
            if is_payment_function(transition.name, transition.body):
                has_owner_param = any(
                    'owner' in p.get('name', '').lower() or 'address' in p.get('type', '').lower()
                    for p in transition.parameters
                )
                
                result = check_payment_access_control(
                    transition.name,
                    transition.body,
                    has_owner_param
                )
                
                if result.get('violation'):
                    violations.append(self._create_violation(
                        rule=rule,
                        program=program,
                        line=transition.line_start,
                        message=result['message'],
                        code_snippet=self._get_code_snippet(program, transition.line_start, 5),
                        remediation=Remediation(
                            description=result['remediation'],
                            code_example="assert_eq(self.caller, owner);",
                            automated=False
                        )
                    ))
        
        return violations
    
    def _check_pci_10_2_payment_audit_logging(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """
        PCI-DSS 10.2: Implement audit trails for payment transactions.
        """
        from comp_leo.payments import is_payment_function, check_payment_audit_logging
        
        violations = []
        
        for transition in program.transitions:
            if is_payment_function(transition.name, transition.body):
                result = check_payment_audit_logging(transition.name, transition.body)
                
                if result.get('violation'):
                    violations.append(self._create_violation(
                        rule=rule,
                        program=program,
                        line=transition.line_start,
                        message=result['message'],
                        code_snippet=self._get_code_snippet(program, transition.line_start, 5),
                        remediation=Remediation(
                            description=result['remediation'],
                            code_example="return then finalize(payment_id, amount, self.caller);",
                            automated=False
                        )
                    ))
        
        return violations
    
    def _check_pci_11_3_4_transaction_limits(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """
        PCI-DSS 11.3.4: Define transaction limits for anomaly detection.
        """
        from comp_leo.payments import check_transaction_limits, is_payment_function
        
        violations = []
        
        # Check if program has payment functions
        has_payments = any(
            is_payment_function(t.name, t.body) for t in program.transitions
        )
        
        if has_payments:
            # Get program constants
            constants = {}
            for line in program.source_lines:
                if 'const' in line.lower():
                    constants[line] = True
            
            result = check_transaction_limits(constants, has_payments)
            
            if result.get('violation'):
                violations.append(self._create_violation(
                    rule=rule,
                    program=program,
                    line=1,
                    message=result['message'],
                    code_snippet="// Add at program level",
                    remediation=Remediation(
                        description=result['remediation'],
                        code_example="const MAX_AMOUNT: u64 = 1000000u64;  // $10k limit\nconst MAX_DAILY_AMOUNT: u64 = 10000000u64;",
                        automated=False
                    )
                ))
        
        return violations
    
    def _check_pci_12_10_6_refund_mechanism(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """
        PCI-DSS 12.10.6: Check for refund/reversal capability.
        """
        from comp_leo.payments import check_refund_mechanism, is_payment_function
        
        violations = []
        
        # Check if program has payment functions
        has_payments = any(
            is_payment_function(t.name, t.body) for t in program.transitions
        )
        
        if has_payments:
            transition_names = [t.name for t in program.transitions]
            result = check_refund_mechanism(transition_names)
            
            if result.get('violation'):
                violations.append(self._create_violation(
                    rule=rule,
                    program=program,
                    line=1,
                    message=result['message'],
                    code_snippet="// Missing refund functionality",
                    remediation=Remediation(
                        description=result['remediation'],
                        code_example="transition refund_payment(payment_id: field, owner: address) {\n    // Refund logic\n}",
                        automated=False
                    )
                ))
        
        return violations
    
    # ============================================================================
    # EXTENDED PCI-DSS CHECKS (v1.1+)
    # ============================================================================
    
    def _check_pci_2_2_secure_configuration(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """
        PCI-DSS 2.2: Secure configuration standards.
        """
        from comp_leo.payments import check_secure_configuration
        
        violations = []
        issues = check_secure_configuration(program.source_code, program.transitions)
        
        for issue in issues:
            violations.append(self._create_violation(
                rule=rule,
                program=program,
                line=issue['line'],
                message=issue['message'],
                code_snippet=issue.get('code', ''),
                remediation=Remediation(
                    description=issue['remediation'],
                    code_example="// Pass admin as parameter instead of hardcoding",
                    automated=False
                )
            ))
        
        return violations
    
    def _check_pci_3_5_private_key_protection(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """
        PCI-DSS 3.5: Cryptographic key protection.
        """
        from comp_leo.payments import check_private_key_exposure
        
        violations = []
        issues = check_private_key_exposure(program.source_code)
        
        for issue in issues:
            violations.append(self._create_violation(
                rule=rule,
                program=program,
                line=issue['line'],
                message=issue['message'],
                code_snippet="[REDACTED FOR SECURITY]",  # Don't show the actual key
                remediation=Remediation(
                    description=issue['remediation'],
                    code_example="// Use secure key management, never hardcode keys",
                    automated=False
                )
            ))
        
        return violations
    
    def _check_pci_4_1_strong_cryptography(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """
        PCI-DSS 4.1: Use strong cryptography.
        """
        from comp_leo.payments import check_strong_cryptography
        
        violations = []
        issues = check_strong_cryptography(program.source_code)
        
        for issue in issues:
            violations.append(self._create_violation(
                rule=rule,
                program=program,
                line=issue['line'],
                message=issue['message'],
                code_snippet=issue.get('code', ''),
                remediation=Remediation(
                    description=issue['remediation'],
                    code_example="// Use SHA-256, SHA-3, or Poseidon (Leo native)",
                    automated=False
                )
            ))
        
        return violations
    
    def _check_pci_6_5_3_insecure_cryptographic_storage(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """
        PCI-DSS 6.5.3: Insecure cryptographic storage.
        """
        from comp_leo.payments import check_insecure_cryptographic_storage
        
        violations = []
        issues = check_insecure_cryptographic_storage(program.source_code)
        
        for issue in issues:
            violations.append(self._create_violation(
                rule=rule,
                program=program,
                line=issue['line'],
                message=issue['message'],
                code_snippet=issue.get('code', ''),
                remediation=Remediation(
                    description=issue['remediation'],
                    code_example="// Use ChaCha20 RNG or cryptographically secure random",
                    automated=False
                )
            ))
        
        return violations
    
    def _check_pci_8_2_multi_signature_auth(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """
        PCI-DSS 8.2: Multi-signature authentication.
        """
        from comp_leo.payments import check_multi_signature_requirements
        
        violations = []
        issues = check_multi_signature_requirements(program.transitions, program.source_code)
        
        for issue in issues:
            violations.append(self._create_violation(
                rule=rule,
                program=program,
                line=issue['line'],
                message=issue['message'],
                code_snippet=self._get_code_snippet(program, issue['line'], 3),
                remediation=Remediation(
                    description=issue['remediation'],
                    code_example="assert(verify_multi_sig(signers, threshold, message));",
                    automated=False
                )
            ))
        
        return violations
    
    def _check_pci_10_3_detailed_audit_logging(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """
        PCI-DSS 10.3: Detailed audit logging fields.
        """
        from comp_leo.payments import check_detailed_audit_logging
        
        violations = []
        issues = check_detailed_audit_logging(program.transitions, program.source_code)
        
        for issue in issues:
            violations.append(self._create_violation(
                rule=rule,
                program=program,
                line=issue['line'],
                message=issue['message'],
                code_snippet=self._get_code_snippet(program, issue['line'], 3),
                remediation=Remediation(
                    description=issue['remediation'],
                    code_example="return then finalize(tx_id, caller, amount, timestamp, status);",
                    automated=False
                )
            ))
        
        return violations
    
    def _check_pci_11_2_vulnerability_detection(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """
        PCI-DSS 11.2: Common vulnerability detection.
        """
        from comp_leo.payments import check_common_vulnerabilities
        
        violations = []
        issues = check_common_vulnerabilities(program.source_code, program.transitions)
        
        for issue in issues:
            violations.append(self._create_violation(
                rule=rule,
                program=program,
                line=issue['line'],
                message=issue['message'],
                code_snippet=self._get_code_snippet(program, issue['line'], 3),
                remediation=Remediation(
                    description=issue['remediation'],
                    code_example="// Follow checks-effects-interactions pattern",
                    automated=False
                )
            ))
        
        return violations
    
    def _check_pci_12_3_rate_limiting(self, program: LeoProgram, rule: Dict) -> List[Violation]:
        """
        PCI-DSS 12.3: Rate limiting on payment functions.
        """
        from comp_leo.payments import check_rate_limiting
        
        violations = []
        issues = check_rate_limiting(program.transitions, program.source_code)
        
        for issue in issues:
            violations.append(self._create_violation(
                rule=rule,
                program=program,
                line=issue['line'],
                message=issue['message'],
                code_snippet=self._get_code_snippet(program, issue['line'], 3),
                remediation=Remediation(
                    description=issue['remediation'],
                    code_example="assert(block.timestamp - last_call[caller] > COOLDOWN);",
                    automated=False
                )
            ))
        
        return violations
    
    # ============================================================================
    # UTILITY METHODS
    # ============================================================================
    
    def _create_violation(
        self,
        rule: Dict[str, Any],
        program: LeoProgram,
        line: int,
        message: str,
        code_snippet: Optional[str] = None,
        remediation: Optional[Remediation] = None
    ) -> Violation:
        """Create a violation from rule and context."""
        
        # Convert controls from strings to ControlMapping objects if needed
        # Resolve cross-domain control metadata from catalog when available
        controls = []
        try:
            from comp_leo.policies.catalog import get_control  # lazy import
        except Exception:
            get_control = None
        for ctrl in rule.get("controls", []):
            if isinstance(ctrl, str):
                mapped = None
                if get_control:
                    try:
                        mapped = get_control(ctrl)
                    except Exception:
                        mapped = None
                if mapped:
                    # Map catalog fields to ControlMapping
                    framework = mapped.get("Standard_Name") or mapped.get("Domain") or rule.get("framework", "PCI")
                    control_name = mapped.get("Section_Title") or mapped.get("Requirement_Ref") or ctrl
                    description = mapped.get("Requirement_Description") or rule.get("description", "")
                    controls.append(ControlMapping(
                        framework=framework,
                        control_id=ctrl,
                        control_name=control_name,
                        description=description
                    ))
                else:
                    # Fallback: attempt to infer framework from rule or control prefix
                    inferred_fw = rule.get("framework") or ("PCI-DSS" if ctrl.startswith("pci") or ctrl.startswith("PCI") else "PCI")
                    controls.append(ControlMapping(
                        framework=inferred_fw,
                        control_id=ctrl,
                        control_name=f"{inferred_fw} {ctrl}",
                        description=rule.get("description", "")
                    ))
            else:
                controls.append(ctrl)
        
        return Violation(
            rule_id=rule["id"],
            rule_name=rule["name"],
            severity=Severity(rule["severity"]),
            violation_type=ViolationType(rule["violation_type"]),
            message=message,
            file_path=program.file_path,
            line_number=line,
            code_snippet=code_snippet,
            controls=controls,
            remediation=remediation
        )
    
    def _get_code_snippet(self, program: LeoProgram, line: int, context: int = 3) -> str:
        """Extract code snippet around a line."""
        start = max(0, line - context - 1)
        end = min(len(program.source_lines), line + context)
        
        snippet_lines = program.source_lines[start:end]
        return '\n'.join(snippet_lines)
    
    def _compute_score(self, violations: List[Violation], total_checks: int) -> int:
        """Compute compliance score from violations."""
        if total_checks == 0:
            return 100
        
        # Weight by severity
        severity_weights = {
            Severity.CRITICAL: 20,
            Severity.HIGH: 10,
            Severity.MEDIUM: 5,
            Severity.LOW: 2,
            Severity.INFO: 0
        }
        
        penalty = sum(severity_weights.get(v.severity, 0) for v in violations)
        
        # Normalize to 0-100 scale
        max_penalty = total_checks * severity_weights[Severity.HIGH]  # Assume average HIGH severity
        score = max(0, 100 - int((penalty / max_penalty) * 100))
        
        return score
