from enum import Enum
from pydantic import BaseModel


class ComplianceStatusId(Enum):
    """
    The normalized status identifier of the compliance check.
    """
    Pass: int = 1 # The compliance check passed for all the evaluated resources.
    Warning: int = 2 # The compliance check did not yield a result due to missing information.
    Fail: int = 3 # The compliance check failed for at least one of the evaluated resources.

class Compliance(BaseModel):
    """
    The Compliance object contains information about Industry and Regulatory
    Framework standards, controls and requirements.
    """

    standards: list[str]

    # Recommended:
    control: str | None = None
    status: str | None = None # The resultant status of the compliance check  normalized to the caption
                              # of the `status_id` value. In the case of 'Other', it is
                              # defined by the event source.
    status_id: ComplianceStatusId | None = None # The normalized status identifier of the compliance
                                                # check.

    # Optional:
    requirements: list[str] | None = None
    status_code: str | None = None # The resultant status code of the compliance check.
    status_detail: str | None = None # The contextual description of the status, status_code values.
