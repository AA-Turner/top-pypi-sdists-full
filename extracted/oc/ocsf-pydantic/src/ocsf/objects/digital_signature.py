from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from .certificate import DigitalCertificate
from .fingerprint import Fingerprint


class DigitalSignatureAlgorithmId(Enum):
    """
    The identifier of the normalized digital signature algorithm.
    """
    Other: int = 99
    Unknown: int = 0
    DSA: int = 1 # Digital Signature Algorithm (DSA).
    RSA: int = 2 # Rivest-Shamir-Adleman (RSA) Algorithm.
    ECDSA: int = 3 # Elliptic Curve Digital Signature Algorithm.
    Authenticode: int = 4 # Microsoft Authenticode Digital Signature Algorithm.

class DigitalSignature(BaseModel):
    """
    The Digital Signature object contains information about the cryptographic
    mechanism used to verify the authenticity, integrity, and origin of the file or
    application.
    """

    algorithm_id: DigitalSignatureAlgorithmId # The identifier of the normalized digital
                                                            # signature algorithm.

    # Recommended:
    certificate: DigitalCertificate | None = None

    # Optional:
    algorithm: str | None = None # The digital signature algorithm used to create the signature,
                                 # normalized to the caption of 'algorithm_id'. In the case of 'Other',
                                 # it is defined by the event source.
    created_time: datetime | None = None # The time when the digital signature was created.
    developer_uid: str | None = None
    digest: Fingerprint | None = None
