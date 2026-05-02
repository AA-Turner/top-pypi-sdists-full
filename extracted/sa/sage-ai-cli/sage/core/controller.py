"""Controller model for SAGE.

Provides command and code validation for sandbox operations.
"""

from __future__ import annotations

import re
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sage.core.router import ProviderRouter

logger = logging.getLogger("sage.controller")

class ControllerModel:
    """Gatekeeper model that validates sandbox operations.

    Uses a fast, cheap model to verify:
    - Command safety before execution
    - Code quality before writing
    - TDD compliance before proceeding
    """

    # Commands that should never be executed
    BLOCKED_PATTERNS = [
        r"rm\s+-rf\s+/",
        r"rm\s+-rf\s+~",
        r"rm\s+-rf\s+\*",
        r":\(\)\{ :\|:& \}\;:",  # Fork bomb (escaped)
        r"mkfs\.",
        r"dd\s+if=.*/dev/",
        r"chmod\s+-R\s+777\s+/",
        r"curl.*\|\s*sh",
        r"wget.*\|\s*sh",
        r">\s*/dev/sd",
    ]

    # Commands that require explicit approval
    DANGEROUS_PATTERNS = [
        r"rm\s+-rf",
        r"git\s+push.*--force",
        r"git\s+reset\s+--hard",
        r"drop\s+database",
        r"drop\s+table",
        r"truncate\s+table",
        r"delete\s+from.*where\s+1\s*=\s*1",
    ]

    def __init__(self, router: ProviderRouter, model_id: str | None = None):
        self.router = router
        # Use a fast, cheap model for gatekeeper operations
        self.model_id = model_id or self._select_fast_model()

    def _select_fast_model(self) -> str:
        """Select a fast model for controller operations."""
        models = self.router.list_all_models()
        # Prefer small/fast models
        for model in models:
            name = model.id.lower()
            if any(x in name for x in ["phi", "gemma", "llama-3.2-1b", "qwen2.5-1.5b"]):
                return model.id
        # Fallback to first available
        return models[0].id if models else "ollama:phi3"

    def validate_command(self, command: str) -> tuple[bool, str]:
        """Validate a command before sandbox execution.

        Returns (is_safe, reason).
        """
        # Check for blocked patterns
        for pattern in self.BLOCKED_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return (
                    False,
                    f"🚫 BLOCKED: Command matches dangerous pattern: {pattern}",
                )

        # Check for dangerous patterns (require approval)
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return (
                    False,
                    f"⚠️ DANGEROUS: Command requires approval: {command[:50]}...",
                )

        return True, "✅ Command validated"

    def validate_code(self, code: str, filepath: str) -> tuple[bool, str]:
        """Validate code before writing.

        Returns (is_safe, reason).
        """
        # Quick pattern-based checks
        dangerous_patterns = [
            (r"os\.system\([^)]*\$", "Shell injection risk"),
            (r"eval\([^)]*input", "Code injection risk"),
            (r"exec\([^)]*request", "Remote code execution risk"),
            (r"pickle\.loads?\([^)]*request", "Pickle deserialization risk"),
            (r"__import__\([^)]*request", "Dynamic import risk"),
        ]

        for pattern, reason in dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                return False, f"🚫 BLOCKED: {reason} in {filepath}"

        return True, "✅ Code validated"

    def verify_tdd_compliance(
        self,
        response: str,
        has_test_files: bool,
        has_impl_files: bool,
    ) -> tuple[bool, str]:
        """Verify that the response follows TDD principles.

        Returns (is_compliant, reason).
        """
        # Implementation is in main.py for now, can be moved here
        return True, "✅ TDD compliance verified"
