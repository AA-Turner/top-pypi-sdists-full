from enum import Enum
from pydantic import BaseModel

class FingerprintAlgorithmId(Enum):
    """
    The identifier of the normalized hash algorithm, which was used to create the
    digital fingerprint.
    """
    Unknown: int = 0
    MD5: int = 1 # MD5 message-digest algorithm producing a 128-bit (16-byte) hash value.
    SHA1: int = 2 # Secure Hash Algorithm 1 producing a 160-bit (20-byte) hash value.
    SHA256: int = 3 # Secure Hash Algorithm 2 producing a 256-bit (32-byte) hash value.
    SHA512: int = 4 # Secure Hash Algorithm 2 producing a 512-bit (64-byte) hash value.
    CTPH: int = 5 # The ssdeep generated fuzzy checksum. Also known as Context Triggered
                  # Piecewise Hash (CTPH).
    TLSH: int = 6 # The TLSH fuzzy hashing algorithm.
    QuickXorHash: int = 7 # Microsoft simple non-cryptographic hash algorithm that works
                          # by XORing the bytes in a circular-shifting fashion.
    Other: int = 99

class Fingerprint(BaseModel):
    """
    The Fingerprint object provides detailed information about a digital
    fingerprint, which is a compact representation of data used to identify a longer
    piece of information, such as a public key or file content. It contains the
    algorithm and value of the fingerprint, enabling efficient and reliable
    identification of the associated data.
    """

    algorithm_id: FingerprintAlgorithmId # The identifier of the normalized hash
                                         # algorithm, which was used to create the
                                         # digital fingerprint.
    value: str # The digital fingerprint value.


    # Optional:
    algorithm: str | None = None # The hash algorithm used to create the digital fingerprint,
                                 # normalized to the caption of 'algorithm_id'. In the case of 'Other',
                                 # it is defined by the event source.
