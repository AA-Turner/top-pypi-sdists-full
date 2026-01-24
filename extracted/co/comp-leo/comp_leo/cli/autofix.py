"""Auto-fix suggestions (non-AI placeholder for future LLM integration)."""

from typing import List, Optional
from comp_leo.core.models import Violation, Remediation

def generate_fix_preview(violation: Violation, context: str) -> Optional[str]:
    """
    Generate a fix preview for a violation.
    
    In v0.1.0: Rule-based templates
    In v0.4.0+: Will use LLM (GPT-4/Claude) for smart fixes
    
    Args:
        violation: The violation to fix
        context: Surrounding code context
        
    Returns:
        Suggested fix as string or None
    """
    
    # Template-based fixes for common patterns
    fixes = {
        "input-validation-missing": _fix_input_validation,
        "state-mutation-unprotected": _fix_access_control,
        "integer-overflow-risk": _fix_integer_overflow,
    }
    
    fix_fn = fixes.get(violation.rule_id)
    if fix_fn:
        return fix_fn(violation, context)
    
    return None

def _fix_input_validation(violation: Violation, context: str) -> str:
    """Generate input validation fix."""
    return """
// Add input validation
transition your_function(public amount: u64) {
    // Validate inputs
    assert(amount > 0u64);
    assert(amount < 1000000u64);  // Max limit
    
    // Your existing code...
}
"""

def _fix_access_control(violation: Violation, context: str) -> str:
    """Generate access control fix."""
    return """
// Add access control check
async function finalize_your_function(owner: address, value: u64) {
    // Verify caller
    assert_eq(self.caller, owner);
    
    // Your existing state mutation...
    Mapping::set(data, key, value);
}
"""

def _fix_integer_overflow(violation: Violation, context: str) -> str:
    """Generate safe arithmetic fix."""
    return """
// Use checked arithmetic
let result: u64 = a.checked_add(b).unwrap();

// Or add bounds checking
assert(a < u64::MAX - b);
let result: u64 = a + b;
"""

def get_fix_confidence(violation: Violation) -> float:
    """
    Get confidence score for auto-fix.
    
    Returns:
        0.0-1.0 confidence score
        >0.8: Safe to auto-apply
        0.5-0.8: Suggest in PR
        <0.5: Manual guidance only
    """
    
    # Simple rules for v0.1.0
    confidence_map = {
        "input-validation-missing": 0.6,  # Needs context
        "state-mutation-unprotected": 0.7,  # Usually safe pattern
        "integer-overflow-risk": 0.5,  # Depends on logic
    }
    
    return confidence_map.get(violation.rule_id, 0.3)

def batch_fix_suggestions(violations: List[Violation]) -> dict:
    """
    Generate batch fix suggestions.
    
    Returns:
        Dict with fix suggestions grouped by confidence
    """
    
    high_confidence = []
    medium_confidence = []
    low_confidence = []
    
    for v in violations:
        confidence = get_fix_confidence(v)
        fix = generate_fix_preview(v, "")
        
        item = {
            "violation": v,
            "fix": fix,
            "confidence": confidence
        }
        
        if confidence > 0.8:
            high_confidence.append(item)
        elif confidence > 0.5:
            medium_confidence.append(item)
        else:
            low_confidence.append(item)
    
    return {
        "high": high_confidence,
        "medium": medium_confidence,
        "low": low_confidence
    }
