from pydantic import BaseModel

from .fingerprint import Fingerprint
from .certificate import DigitalCertificate
from .tls_extension import TLSExtension

class TLS(BaseModel):
    """
    The Transport Layer Security (TLS) object describes the negotiated TLS protocol
    used for secure communications over an establish network connection.
    """

    version: str # The TLS protocol version.

    # Recommended:
    certificate: DigitalCertificate | None = None
    certificate_chain: list[str] | None = None
    cipher: str | None = None
    client_ciphers: list[str] | None = None
    ja3_hash: Fingerprint | None = None
    ja3s_hash: Fingerprint | None = None
    sni: str | None = None

    # Optional:
    alert: int | None = None
    extension_list: list[TLSExtension] | None = None
    tls_extension_list: list[TLSExtension] | None = None
    handshake_dur: int | None = None
    key_length: int | None = None
    sans: list[dict] | None = None
    server_ciphers: list[str] | None = None
