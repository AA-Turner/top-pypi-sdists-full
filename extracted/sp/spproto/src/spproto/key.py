from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def generate_private_key() -> bytes:
    privkey = Ed25519PrivateKey.generate()
    privkey_b = privkey.private_bytes_raw()
    return privkey_b


def get_public_key(
    privkey_b: bytes,
    /
) -> bytes:
    privkey = Ed25519PrivateKey.from_private_bytes(privkey_b)
    pubkey = privkey.public_key()
    pubkey_b = pubkey.public_bytes_raw()
    return pubkey_b
