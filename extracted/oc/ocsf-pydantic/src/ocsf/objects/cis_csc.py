from pydantic import BaseModel

class CISCSC(BaseModel):
    """
    The CIS Critical Security Control (CSC) contains information as defined by the
    Center for Internet Security Critical Security Control <a target='_blank'
    href='https://www.cisecurity.org/controls'>(CIS CSC)</a>. Prioritized set of
    actions to protect your organization and data from cyber-attack vectors.
    """

    control: str

    # Recommended:
    version: str | None = None # The CIS critical security control version.
