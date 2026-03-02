from pydantic import BaseModel

from .policy import Policy

class AuthorizationResult(BaseModel):
    """
    The Authorization Result object provides details about the authorization outcome
    and associated policies related to activity.
    """

    # Recommended:
    decision: str | None = None # Authorization Result/outcome, e.g. allowed, denied.

    # Optional:
    policy: Policy | None = None # Details about the Identity/Access management policies that are
                                 # applicable.
