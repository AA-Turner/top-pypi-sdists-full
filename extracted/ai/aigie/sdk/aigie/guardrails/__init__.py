"""
Aigie Guardrails Framework for SLA Production Runtime.

Kytte is an SLA production tool - we don't block, we fix.

Guardrails detect issues and trigger remediation:
- Detect → Evaluate → Fix
- RETRY: Retry with adjusted approach
- REDIRECT: Use fallback model/strategy
- ADJUST: Modify content and continue
- ESCALATE: Create remediation plan

Integrates with Kytte's RemediationService for autonomous fixes.
"""

from .base import (
    BaseGuardrail,
    GuardrailAction,
    GuardrailChain,
    GuardrailRemediationNeeded,
    GuardrailResult,
)
from .detectors import (
    HallucinationDetector,
    PIIDetector,
    PromptInjectionDetector,
    ToxicityDetector,
)

__all__ = [
    # Base classes
    "BaseGuardrail",
    "GuardrailChain",
    "GuardrailResult",
    "GuardrailAction",
    "GuardrailRemediationNeeded",
    # Detectors (SLA-focused - detect and remediate, not block)
    "PIIDetector",
    "ToxicityDetector",
    "HallucinationDetector",
    "PromptInjectionDetector",
]
