from datetime import datetime
from enum import Enum

from ocsf.events.base import BaseEvent, CategoryId

from ocsf.objects.device import Device
from ocsf.objects.finding_info import FindingInformation


class FindingActivityId(Enum):
    """
    The normalized identifier of the finding activity.
    """
    Create: int = 1
    Update: int = 2
    Close: int = 3

class FindingStatusId(Enum):
    """
    The normalized status identifier of the Finding, set by the consumer.
    """
    New: int = 1 # The Finding is new and yet to be reviewed.
    In_Progress: int = 2 # The Finding is under review.
    Suppressed: int = 3 # The Finding was reviewed, determined to be benign or
                        # a false positive and is now suppressed.
    Resolved: int = 4 # The Finding was reviewed, remediated and is now considered resolved.

class Finding(BaseEvent):
    """
    The Finding event is a generic event that defines a set of attributes available
    in the Findings category.
    """

    finding_info: FindingInformation

    category_uid: CategoryId = CategoryId.Findings

    # Recommended:
    confidence_id: int | None = None
    device: Device | None = None # Describes the affected device/host. It can be used in conjunction
                                 # with `Affected Resource(s)`. e.g. Specific details
                                 # about an AWS EC2 instance, that is affected by the Finding.
    status_id: FindingStatusId | None = None # The normalized status identifier of the Finding, set by
                                             # the consumer.

    # Optional:
    activity_name: str | None = None # The finding activity name, as defined by the
                                     # `activity_id`.
    activity_id: FindingActivityId | None = None # The normalized identifier of the finding activity.
    comment: str | None = None # A user provided comment about the finding.
    confidence: str | None = None
    confidence_score: int | None = None
    end_time: datetime | None = None # The time of the most recent event included in the finding.
    start_time: datetime | None = None # The time of the least recent event included in the finding.
    status: str | None = None # The normalized status of the Finding set by the consumer normalized to
                              # the caption of the status_id value. In the case of 'Other', it is
                              # defined by the source.
