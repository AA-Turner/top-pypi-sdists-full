"""
PCI Evaluator for CompZ

Scans a path for basic PCI-DSS issues using heuristic checks
and outputs a ComplianceResult compatible with CompZ anchoring.
"""

from __future__ import annotations

import json
import time
import os
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

from ..models import ComplianceResult, ControlEvaluation
from .rules import (
    scan_forbidden_data,
    scan_private_keys,
    scan_weak_crypto,
    has_rate_limiting,
    has_transaction_limits,
    summarize_matches,
)


EXCLUDES = {".git", "node_modules", "dist", "build", "__pycache__", ".venv", "venv"}
INCLUDE_EXTS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".java", ".rb", ".rs", ".sol",
    ".json", ".yml", ".yaml", ".toml", ".ini", ".cfg", ".conf", ".env", ".sh", ".md",
}
MAX_FILE_BYTES = 500_000


class PCIEvaluator:
    def __init__(self, policy_id: str = "pci-dss-basic") -> None:
        self.policy_id = policy_id
        self.policy: Dict = self._load_policy(policy_id)

    def _load_policy(self, policy_id: str) -> Dict:
        policies_dir = Path(__file__).parent / "policies"
        policy_path = policies_dir / f"{policy_id}.json"
        if not policy_path.exists():
            raise FileNotFoundError(f"Policy not found: {policy_id}")
        with open(policy_path, "r") as f:
            return json.load(f)

    def _iter_files(self, base: Path) -> List[Path]:
        files: List[Path] = []
        for p in base.rglob("*"):
            if p.is_dir():
                if p.name in EXCLUDES:
                    # skip traversal into excluded dirs
                    try:
                        p.rglob.__self__  # no-op to keep static analyzers quiet
                    except Exception:
                        pass
                continue
            if p.suffix.lower() in INCLUDE_EXTS and p.stat().st_size <= MAX_FILE_BYTES:
                files.append(p)
        return files

    def evaluate(self, path: str, repo_id: str | None = None, commit_hash: str | None = None) -> ComplianceResult:
        start = time.time()
        base = Path(path).resolve()
        repo_id = repo_id or base.name
        commit_hash = commit_hash or os.getenv("GIT_COMMIT", "unknown")

        # Aggregate scan state
        any_rate_limit = False
        any_tx_limits = False
        forbidden_hits: List[str] = []
        key_hits: List[str] = []
        weak_crypto_hits: List[str] = []

        scanned_files = 0
        for file_path in self._iter_files(base):
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            scanned_files += 1

            # Content checks
            forbidden_hits.extend(scan_forbidden_data(content))
            key_hits.extend(scan_private_keys(content))
            weak_crypto_hits.extend(scan_weak_crypto(content))
            if has_rate_limiting(content):
                any_rate_limit = True
            if has_transaction_limits(content):
                any_tx_limits = True

        # Build control evaluations according to policy rule list
        rule_defs: Dict[str, Dict] = {r["id"]: r for r in self.policy.get("rules", [])}

        evals: List[ControlEvaluation] = []

        # pci-3.2-forbidden-data
        r = rule_defs.get("pci-3.2-forbidden-data")
        if r:
            passed = len(forbidden_hits) == 0
            reason = (
                "No forbidden authentication data detected"
                if passed else f"Detected patterns: {summarize_matches(forbidden_hits)}"
            )
            evals.append(ControlEvaluation(
                control_id=r["id"], framework="PCI-DSS", passed=passed, reason=reason, severity=r.get("severity")
            ))

        # pci-3.5-private-key-protection
        r = rule_defs.get("pci-3.5-private-key-protection")
        if r:
            passed = len(key_hits) == 0
            reason = (
                "No private keys or seed phrases exposed"
                if passed else f"Detected secrets: {summarize_matches(key_hits)}"
            )
            evals.append(ControlEvaluation(
                control_id=r["id"], framework="PCI-DSS", passed=passed, reason=reason, severity=r.get("severity")
            ))

        # pci-4.1-strong-cryptography
        r = rule_defs.get("pci-4.1-strong-cryptography")
        if r:
            passed = len(weak_crypto_hits) == 0
            reason = (
                "No weak crypto primitives detected"
                if passed else f"Weak crypto references: {summarize_matches(weak_crypto_hits)}"
            )
            evals.append(ControlEvaluation(
                control_id=r["id"], framework="PCI-DSS", passed=passed, reason=reason, severity=r.get("severity")
            ))

        # pci-11.3.4-transaction-limits
        r = rule_defs.get("pci-11.3.4-transaction-limits")
        if r:
            passed = any_tx_limits
            reason = (
                "Transaction limits detected (MAX/limit/threshold)"
                if passed else "No transaction limits found"
            )
            evals.append(ControlEvaluation(
                control_id=r["id"], framework="PCI-DSS", passed=passed, reason=reason, severity=r.get("severity")
            ))

        # pci-12.3-rate-limiting
        r = rule_defs.get("pci-12.3-rate-limiting")
        if r:
            passed = any_rate_limit
            reason = (
                "Rate limiting keywords detected"
                if passed else "No rate limiting patterns found"
            )
            evals.append(ControlEvaluation(
                control_id=r["id"], framework="PCI-DSS", passed=passed, reason=reason, severity=r.get("severity")
            ))

        # Compute score (simple severity-weighted)
        weights = {"critical": 30, "high": 15, "medium": 8, "low": 4}
        score = 100
        for ev in evals:
            if not ev.passed and ev.severity:
                score -= weights.get(ev.severity.lower(), 5)
        if score < 0:
            score = 0

        end = time.time()
        metadata = {
            "scanner": "compz-pci",
            "policy": self.policy_id,
            "scanned_files": scanned_files,
            "total_controls_evaluated": len(evals),
            "passed_controls": sum(1 for e in evals if e.passed),
            "failed_controls": sum(1 for e in evals if not e.passed),
            "scan_duration_seconds": round(end - start, 3),
        }

        result = ComplianceResult(
            repo_id=str(repo_id),
            commit_hash=str(commit_hash),
            frameworks=["PCI-DSS"],
            control_evaluations=evals,
            risk_score=float(score if score >= 0 else 0),
            timestamp=datetime.utcnow().isoformat() + "Z",
            metadata=metadata,
        )
        return result
