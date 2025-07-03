import base64
import hashlib
import secrets


def generate_code_verifier() -> str:
    """Generate a code verifier for PKCE."""
    # RFC 7636 requires 43-128 characters
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
    
def generate_code_challenge(verifier: str) -> str:
    """Generate a code challenge from the verifier using S256 method."""
    digest = hashlib.sha256(verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(digest).decode('utf-8').rstrip('=')
