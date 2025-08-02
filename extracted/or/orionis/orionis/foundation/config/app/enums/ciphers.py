from enum import Enum

class Cipher(Enum):
    """
    Enumeration of supported AES cipher modes.

    This enum defines various Advanced Encryption Standard (AES) cipher modes and key sizes
    commonly used for encryption and decryption operations.

    Members:
        AES_128_CBC: AES with 128-bit key in Cipher Block Chaining (CBC) mode.
        AES_192_CBC: AES with 192-bit key in CBC mode.
        AES_256_CBC: AES with 256-bit key in CBC mode.
        AES_128_GCM: AES with 128-bit key in Galois/Counter Mode (GCM).
        AES_256_GCM: AES with 256-bit key in GCM.
        AES_CTR: AES in Counter (CTR) mode.
        AES_CFB: AES in Cipher Feedback (CFB) mode.
        AES_CFB8: AES in CFB mode with 8-bit feedback.
        AES_CFB128: AES in CFB mode with 128-bit feedback.
        AES_OFB: AES in Output Feedback (OFB) mode.
        AES_ECB: AES in Electronic Codebook (ECB) mode.
    """

    AES_128_CBC = "AES-128-CBC"
    AES_192_CBC = "AES-192-CBC"
    AES_256_CBC = "AES-256-CBC"
    AES_128_GCM = "AES-128-GCM"
    AES_256_GCM = "AES-256-GCM"
    AES_CTR = "AES-CTR"
    AES_CFB = "AES-CFB"
    AES_CFB8 = "AES-CFB8"
    AES_CFB128 = "AES-CFB128"
    AES_OFB = "AES-OFB"
    AES_ECB = "AES-ECB"
