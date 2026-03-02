from ._entity import Entity

from .group import Group

class Policy(Entity):
    """
    The Policy object describes the policies that are applicable. <p>Policy
    attributes provide traceability to the operational state of the security product
    at the time that the event was captured, facilitating forensics,
    troubleshooting, and policy tuning/adjustments.</p>
    """

    # Recommended:
    version: str | None = None # The policy version number.
    is_applied: bool | None = None # A determination if the content of a policy was applied to a target
                                   # or request, or not.

    # Optional:
    desc: str | None = None # The description of the policy.
    group: Group | None = None # The policy group.
    name: str | None = None # The policy name. For example: `IAM Policy`.
    uid: str | None = None # A unique identifier of the policy instance.
