from __future__ import annotations
from typing import Optional, List


class SignatureVerificationResult:
    """
    Outcome of signature verification.

    Attributes:
        ok: True if the signature verification passed.
        errors: Optional list of errors raised by the verifier. None when ok=True.
    """
    ok: bool
    errors: Optional[List[str]] = None

    def __init__(self, ok: bool, errors: Optional[List[str]] = None):
        self.ok = ok
        self.errors = errors

    @staticmethod
    def passed() -> "SignatureVerificationResult":
        return SignatureVerificationResult(ok=True, errors=None)

    @staticmethod
    def failed(errors: Optional[List[str]] = None) -> "SignatureVerificationResult":
        return SignatureVerificationResult(ok=False, errors=errors)