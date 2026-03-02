from pydantic import BaseModel

class EmailAuthentication(BaseModel):
    """
    The Email Authentication object describes the Sender Policy Framework (SPF),
    DomainKeys Identified Mail (DKIM) and Domain-based Message Authentication,
    Reporting and Conformance (DMARC) attributes of an email.
    """

    # Recommended:
    dkim_domain: str | None = None
    dkim: str | None = None
    dkim_signature: str | None = None
    dmarc: str | None = None
    dmarc_override: str | None = None
    dmarc_policy: str | None = None
    spf: str | None = None
