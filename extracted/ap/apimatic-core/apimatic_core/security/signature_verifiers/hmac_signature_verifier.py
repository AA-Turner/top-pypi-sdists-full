import hmac
import hashlib
from typing import Callable, Optional, Union

from apimatic_core_interfaces.http.request import Request
from apimatic_core_interfaces.security.signature_verifier import SignatureVerifier
from apimatic_core_interfaces.types.signature_verification_result import SignatureVerificationResult


class DigestEncoder:
    """Minimal encoder interface for HMAC digests."""
    def encode(self, digest: bytes) -> str:  # pragma: no cover - interface
        raise NotImplementedError


class HexEncoder(DigestEncoder):
    """Lowercase hexadecimal encoding."""
    def encode(self, digest: bytes) -> str:
        return digest.hex()


class Base64Encoder(DigestEncoder):
    """Standard Base64 encoding."""
    def encode(self, digest: bytes) -> str:
        import base64
        return base64.b64encode(digest).decode("utf-8")


class Base64UrlEncoder(DigestEncoder):
    """URL-safe Base64 without '=' padding."""
    def encode(self, digest: bytes) -> str:
        import base64
        return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")


class HmacSignatureVerifier(SignatureVerifier):
    """
    HMAC signature verifier that delegates message construction to a user-supplied callable.

    Parameters
    ----------
    secret_key : str
        Shared secret used for HMAC.
    signature_header : str
        Header name containing the provided signature (case-insensitive lookup).
    canonical_message_builder : Optional[Callable[[Request], Union[bytes, str, None]]]
        Function that produces the exact message to sign. If omitted (None) or returns None,
        the verifier will use request.raw_body (bytes) if present, otherwise request.body (text, UTF-8).
    hash_alg : Callable (defaults to hashlib.sha256)
        Hash algorithm for HMAC.
    encoder : DigestEncoder (defaults to HexEncoder())
        Encoder to transform HMAC digest bytes into a string for comparison.
    signature_value_template : Optional[str]
        If provided, wraps/defines the expected signature. If it contains '{digest}', the
        placeholder is replaced with the encoded digest; otherwise it is treated as a constant.
    """

    def __init__(
        self,
        *,
        secret_key: str,
        signature_header: str,
        canonical_message_builder: Optional[Callable[[Request], Union[bytes, None]]] = None,
        hash_alg=hashlib.sha256,
        encoder: Optional[DigestEncoder] = HexEncoder(),
        signature_value_template: Optional[str] = '{digest}',
    ) -> None:
        if not isinstance(secret_key, str) or not secret_key:
            raise ValueError("key must be a non-empty string")
        if not isinstance(signature_header, str) or not signature_header.strip():
            raise ValueError("signature_header must be a non-empty string")

        self._secret_key = secret_key
        self._signature_header_lc = signature_header.lower().strip()
        self._message_resolver = canonical_message_builder
        self._hash_alg = hash_alg
        self._encoder = encoder
        self._signature_value_template = signature_value_template

    def verify(self, request: Request) -> SignatureVerificationResult:
        try:
            provided = self._read_signature_header(request)
            if provided is None:
                return SignatureVerificationResult.failed(
                    [f"Signature header '{self._signature_header_lc}' is missing"]
                )

            message_bytes = self._resolve_message_bytes(request)
            digest = hmac.new(self._secret_key.encode("utf-8"), message_bytes, self._hash_alg).digest()
            encoded_digest = self._encoder.encode(digest)
            expected = self._signature_value_template.replace("{digest}", encoded_digest)

            is_match = hmac.compare_digest(provided, expected)
            return SignatureVerificationResult.passed() if is_match else SignatureVerificationResult.failed(
                ["Signature mismatch"]
            )
        except Exception as exc:
            return SignatureVerificationResult.failed(
                [f"Signature Verification Failed: {exc}"]
            )

    # ------------- internal helpers -------------

    def _read_signature_header(self, request: Request) -> Optional[str]:
        headers = {str(k).lower(): str(v) for k, v in (getattr(request, "headers", {}) or {}).items()}
        value = headers.get(self._signature_header_lc)
        return None if value is None or value.strip() == "" else value

    def _resolve_message_bytes(self, request: Request) -> bytes:
        if self._message_resolver is None:
            return request.raw_body

        return self._message_resolver(request)
