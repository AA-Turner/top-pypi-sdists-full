"""Check that this Python environment runs the client's cryptography in FIPS mode.

Run it as::

    python -m istari_digital_client.fips_check

It exits 0 when every check passes and 1 otherwise, printing one line per check.

The client has two crypto backends, and both must be FIPS-validated:

* The Python interpreter's OpenSSL, used by ``ssl`` (HTTPS to the platform) and
  ``hashlib`` (content hashes). It is in FIPS mode only on a FIPS build of Python,
  such as RHEL's system Python on a FIPS-enabled host.
* The OpenSSL inside the ``cryptography`` package, used for file encryption and
  identity keys. The wheels on PyPI bundle their own OpenSSL, which is not in FIPS
  mode. ``cryptography`` must be built from source against the FIPS OpenSSL instead.
"""

from __future__ import annotations

import sys
from collections.abc import Callable


def _python_openssl() -> str:
    import _hashlib
    import ssl

    if not _hashlib.get_fips_mode():
        raise RuntimeError(f"{ssl.OPENSSL_VERSION} is not in FIPS mode")
    return ssl.OPENSSL_VERSION


def _cryptography_openssl() -> str:
    import ssl

    from cryptography.hazmat.bindings._rust import openssl as rust_openssl

    version = rust_openssl.openssl_version_text()
    if not rust_openssl.is_fips_enabled():
        raise RuntimeError(
            f"{version} is not in FIPS mode (a PyPI wheel? build cryptography from source)"
        )
    # Built against a different OpenSSL than Python's, cryptography can report FIPS
    # mode and still fail every operation because it cannot load a FIPS provider.
    if version != ssl.OPENSSL_VERSION:
        raise RuntimeError(
            f"{version} is not Python's {ssl.OPENSSL_VERSION}; rebuild cryptography against it"
        )
    return version


def _client_operations() -> str:
    """Run the algorithms the client uses, so a FIPS provider that rejects one fails here."""
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec, rsa

    from istari_digital_client import native_crypto

    rsa_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_pem = rsa_key.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
    )
    ciphertext = native_crypto.encrypt(public_pem, b"fips-check")
    native_crypto.Token.compare_token(
        *native_crypto.Token.from_bytes(ciphertext), ciphertext
    )

    ec_key = ec.generate_private_key(ec.SECP384R1())
    signature = ec_key.sign(b"fips-check", ec.ECDSA(hashes.SHA384()))
    ec_key.public_key().verify(signature, b"fips-check", ec.ECDSA(hashes.SHA384()))
    return "RSA-OAEP, AES-256-GCM, SHA-384, ECDSA P-384"


CHECKS: list[tuple[str, Callable[[], str]]] = [
    ("Python OpenSSL (HTTPS, hashing)", _python_openssl),
    ("cryptography OpenSSL (encryption, identity keys)", _cryptography_openssl),
    ("Client operations", _client_operations),
]


def main() -> int:
    """Run every check, print the results, and return the exit code."""
    passed = True
    for name, check in CHECKS:
        try:
            print(f"ok    {name}: {check()}")
        except Exception as exc:  # noqa: BLE001 — report every failure, not just the first
            print(f"FAIL  {name}: {exc}")
            passed = False
    print("FIPS check passed" if passed else "FIPS check failed")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
