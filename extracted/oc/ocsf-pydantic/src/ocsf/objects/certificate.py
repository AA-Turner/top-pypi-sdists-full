from datetime import datetime
from pydantic import BaseModel
from .fingerprint import Fingerprint

class DigitalCertificate(BaseModel):
    """
    The Digital Certificate, also known as a Public Key Certificate, object contains
    information about the ownership and usage of a public key. It serves as a means
    to establish trust in the authenticity and integrity of the public key and the
    associated entity.
    """

    fingerprints: list[Fingerprint] # The fingerprint list of the certificate.
    issuer: str # The certificate issuer distinguished name.
    serial_number: str # The serial number of the certificate used to create the digital
                       # signature.

    # Recommended:
    created_time: datetime | None = None # The time when the certificate was created.
    expiration_time: datetime | None = None # The expiration time of the certificate.
    subject: str | None = None # The certificate subject distinguished name.
    version: str | None = None # The certificate version.

    # Optional:
    uid: str | None = None # The unique identifier of the certificate.
