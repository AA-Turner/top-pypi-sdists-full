from .imports import *
from .functions import *
class SSLManager:
    def __init__(self, ciphers=None,ssl_options=None, certification=None,cafile=None, tls_min: ssl.TLSVersion = ssl.TLSVersion.TLSv1_2):
        self.ciphers = ciphers or CipherManager().ciphers_string
        self.certification = certification or ssl.CERT_REQUIRED
        self.cafile = cafile or certifi.where()          # << add this
        self.tls_min = tls_min
        self.ssl_options = ssl_options
        self.ssl_context = self.get_context()

    def get_context(self) -> ssl.SSLContext:
        ctx = ssl.create_default_context(
            purpose=ssl.Purpose.SERVER_AUTH,
            cafile=self.cafile
        )
        ctx.minimum_version = self.tls_min
        ctx.options |= ssl.OP_NO_COMPRESSION
        # TLS 1.2 ciphers
        try:
            ctx.set_ciphers(self.ciphers)
        except ssl.SSLError:
            # If OpenSSL rejects (e.g., legacy provider not loaded), fall back to a safe default
            ctx.set_ciphers("ECDHE+AESGCM:ECDHE+CHACHA20")
        # TLS 1.3 suites (optional)
        if hasattr(ctx, "set_ciphersuites"):
            try:
                ctx.set_ciphersuites(
                    "TLS_AES_256_GCM_SHA384:TLS_AES_128_GCM_SHA256:TLS_CHACHA20_POLY1305_SHA256"
                )
            except ssl.SSLError:
                pass
        return ctx
