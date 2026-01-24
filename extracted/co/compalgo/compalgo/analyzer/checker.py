from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

from .parser import PyTealParser
from .teal_parser import parse_teal_file

SEVERITY_WEIGHT = {"critical": 20, "high": 10, "medium": 5, "low": 2, "info": 0}

# P0 rule IDs
DELETE_WITHOUT_ADMIN_CHECK = "DELETE_WITHOUT_ADMIN_CHECK"
UPDATE_WITHOUT_ADMIN_CHECK = "UPDATE_WITHOUT_ADMIN_CHECK"
MISSING_ADMIN_SENDER_CHECK = "MISSING_ADMIN_SENDER_CHECK"
REKEY_NOT_ZERO = "REKEY_NOT_ZERO"
CLOSEREMAINDER_NOT_ZERO = "CLOSEREMAINDER_NOT_ZERO"
MISSING_ARG_VALIDATION = "MISSING_ARG_VALIDATION"
STATE_MUTATION_UNGUARDED = "STATE_MUTATION_UNGUARDED"
INNER_TXN_UNGUARDED = "INNER_TXN_UNGUARDED"
EXCESSIVE_FEE_UNBOUNDED = "EXCESSIVE_FEE_UNBOUNDED"

RULES_ALL = [
    DELETE_WITHOUT_ADMIN_CHECK,
    UPDATE_WITHOUT_ADMIN_CHECK,
    MISSING_ADMIN_SENDER_CHECK,
    REKEY_NOT_ZERO,
    CLOSEREMAINDER_NOT_ZERO,
    MISSING_ARG_VALIDATION,
    STATE_MUTATION_UNGUARDED,
    INNER_TXN_UNGUARDED,
    EXCESSIVE_FEE_UNBOUNDED,
]

# Default severity mapping
RULE_SEVERITY = {
    DELETE_WITHOUT_ADMIN_CHECK: "critical",
    UPDATE_WITHOUT_ADMIN_CHECK: "high",
    MISSING_ADMIN_SENDER_CHECK: "high",
    REKEY_NOT_ZERO: "high",
    CLOSEREMAINDER_NOT_ZERO: "high",
    MISSING_ARG_VALIDATION: "high",
    STATE_MUTATION_UNGUARDED: "high",
    INNER_TXN_UNGUARDED: "high",
    EXCESSIVE_FEE_UNBOUNDED: "medium",
}

# Control mapping (minimal P0)
RULE_CONTROLS = {
    DELETE_WITHOUT_ADMIN_CHECK: [{"framework": "SOC2", "control_id": "CC6.1"}],
    UPDATE_WITHOUT_ADMIN_CHECK: [{"framework": "SOC2", "control_id": "CC6.1"}],
    MISSING_ADMIN_SENDER_CHECK: [{"framework": "SOC2", "control_id": "CC6.1"}],
    REKEY_NOT_ZERO: [{"framework": "SOC2", "control_id": "CC6.1"}],
    CLOSEREMAINDER_NOT_ZERO: [{"framework": "SOC2", "control_id": "CC6.1"}],
    MISSING_ARG_VALIDATION: [{"framework": "PCI", "control_id": "6.5.1"}],
    STATE_MUTATION_UNGUARDED: [{"framework": "SOC2", "control_id": "CC6.1"}],
    INNER_TXN_UNGUARDED: [{"framework": "PCI", "control_id": "10.2"}],
    EXCESSIVE_FEE_UNBOUNDED: [{"framework": "PCI", "control_id": "10.2"}],
}


def _load_policy(enabled: Optional[str]) -> List[str]:
    if not enabled:
        return RULES_ALL
    here = os.path.dirname(os.path.dirname(__file__))
    pol_dir = os.path.join(here, "policies")
    path = os.path.join(pol_dir, f"{enabled}.json")
    if not os.path.exists(path):
        return RULES_ALL
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("enabled_rules", RULES_ALL)


@dataclass
class CheckResult:
    file_path: str
    score: int
    passed: bool
    violations: List[Dict[str, Any]]
    counts: Dict[str, int]


class ComplianceChecker:
    def __init__(self, policy_pack: str = "algorand-baseline", threshold: int = 80):
        self.policy_pack = policy_pack
        self.threshold = threshold
        self.enabled_rules = _load_policy(policy_pack)
        self.py_parser = PyTealParser()

    def _score(self, violations: List[Dict[str, Any]]) -> int:
        penalty = sum(SEVERITY_WEIGHT.get(v.get("severity", "info"), 0) for v in violations)
        max_penalty = max(1, 10 * SEVERITY_WEIGHT["high"])  # normalize
        score = max(0, 100 - int((penalty / max_penalty) * 100))
        return score

    def _check_signals(self, file_path: str, signals: Dict[str, Any]) -> List[Dict[str, Any]]:
        v: List[Dict[str, Any]] = []
        enabled = set(self.enabled_rules)
        has_admin = signals.get("has_sender_check", False) or signals.get("has_admin_sender_assert", False)
        has_delete = signals.get("has_delete_application", False) or signals.get("uses_delete", False)
        has_update = signals.get("has_update_application", False) or signals.get("uses_update", False)
        has_global_put = signals.get("has_global_put", False) or signals.get("uses_global_put", False)
        has_local_put = signals.get("has_local_put", False) or signals.get("uses_local_put", False)
        has_box_ops = signals.get("has_box_ops", False) or signals.get("uses_box_ops", False)
        has_rekey_check = signals.get("has_rekey_to_check", False) or signals.get("has_rekey_zero_assert", False)
        has_close_check = signals.get("has_close_check", False) or signals.get("has_close_zero_assert", False)
        has_inner_txn = signals.get("has_inner_txn", False) or signals.get("uses_inner_txn", False)
        has_fee_check = signals.get("has_fee_check", False) or signals.get("has_fee_bound_assert", False)
        has_arg_use = signals.get("has_arg_validation", False) or signals.get("uses_btoi_args", False)
        has_assert = signals.get("has_assert", False)
        
        # Application lifecycle
        if has_delete and DELETE_WITHOUT_ADMIN_CHECK in enabled and not has_admin:
            v.append(self._violation(DELETE_WITHOUT_ADMIN_CHECK, file_path, "DeleteApplication without admin sender check"))
        if has_update and UPDATE_WITHOUT_ADMIN_CHECK in enabled and not has_admin:
            v.append(self._violation(UPDATE_WITHOUT_ADMIN_CHECK, file_path, "UpdateApplication without admin sender check"))
        # Global admin check for state mutation
        if (has_global_put or has_local_put or has_box_ops) and MISSING_ADMIN_SENDER_CHECK in enabled and not has_admin:
            v.append(self._violation(MISSING_ADMIN_SENDER_CHECK, file_path, "State mutation without admin sender check"))
        # Account controls
        if REKEY_NOT_ZERO in enabled and not has_rekey_check:
            v.append(self._violation(REKEY_NOT_ZERO, file_path, "Missing assert: Txn.rekey_to() == Global.zero_address()"))
        if CLOSEREMAINDER_NOT_ZERO in enabled and not has_close_check:
            v.append(self._violation(CLOSEREMAINDER_NOT_ZERO, file_path, "Missing assert: Txn.close_remainder_to() == Global.zero_address()"))
        # Args validation
        if MISSING_ARG_VALIDATION in enabled and has_arg_use and not has_assert:
            v.append(self._violation(MISSING_ARG_VALIDATION, file_path, "Application args used without assertions/validation"))
        # Inner txn safety
        if INNER_TXN_UNGUARDED in enabled and has_inner_txn and not has_assert:
            v.append(self._violation(INNER_TXN_UNGUARDED, file_path, "Inner transactions present without assertions/limits"))
        # Fee bounds
        if EXCESSIVE_FEE_UNBOUNDED in enabled and not has_fee_check:
            v.append(self._violation(EXCESSIVE_FEE_UNBOUNDED, file_path, "No fee upper-bound assertion (Txn.fee() <= Int(N))"))
        return v

    def _violation(self, rule_id: str, file_path: str, message: str) -> Dict[str, Any]:
        return {
            "rule_id": rule_id,
            "severity": RULE_SEVERITY.get(rule_id, "low"),
            "message": message,
            "file_path": file_path,
            "controls": RULE_CONTROLS.get(rule_id, []),
        }

    def check_file(self, file_path: str) -> CheckResult:
        if file_path.endswith(".teal"):
            signals = parse_teal_file(file_path)
        else:
            program = self.py_parser.parse_file(file_path)
            signals = program.features
        violations = self._check_signals(file_path, signals)
        score = self._score(violations)
        passed = score >= self.threshold and not any(v["severity"] in ("critical", "high") for v in violations)
        counts = {}
        for v in violations:
            counts[v["severity"]] = counts.get(v["severity"], 0) + 1
        return CheckResult(file_path=file_path, score=score, passed=passed, violations=violations, counts=counts)

    def check_path(self, path: str) -> List[CheckResult]:
        results: List[CheckResult] = []
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for fn in files:
                    if fn.endswith((".py", ".teal")):
                        results.append(self.check_file(os.path.join(root, fn)))
        else:
            results.append(self.check_file(path))
        return results
