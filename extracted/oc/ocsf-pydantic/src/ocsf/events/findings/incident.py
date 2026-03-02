from datetime import datetime
from enum import Enum

from pydantic import AnyUrl

from ocsf.events.base import BaseEvent

from ocsf.objects.attack import MITREATTCK
from ocsf.objects.finding_info import FindingInformation
from ocsf.objects.group import Group
from ocsf.objects.user import User


class IncidentFindingActivityId(Enum):
    """
    The normalized identifier of the Incident activity.
    """
    Create: int = 1
    Update: int = 2
    Close: int = 3


class IncidentFindingStatusId(Enum):
    """
    The normalized status identifier of the Incident.
    """
    New: int = 1 # The service desk has received the incident but has not
                 # assigned it to an agent.
    In_Progress: int = 2 # The incident has been assigned to an agent but has
                         # not been resolved. The agent is actively working with
                         # the user to diagnose and resolve the incident.
    On_Hold: int = 3 # The incident requires some information or response from
                     # the user or from a third party.
    Resolved: int = 4 # The service desk has confirmed that the incident is resolved.
    Closed: int = 5 # The incident is resolved and no further action is necessary.


class IncidentFinding(BaseEvent):
    """
    An Incident Finding reports the creation, update, or closure of security
    incidents as a result of detections and/or analytics.
    """

    class_uid: int = 2005
    class_name: str = 'Incident Finding'

    activity_id: IncidentFindingActivityId # The normalized identifier of the Incident
                                           # activity.
    finding_info_list: list[FindingInformation]
    status_id: IncidentFindingStatusId # The normalized status identifier of the
                                       # Incident.

    # Recommended:
    confidence_id: int | None = None
    desc: str | None = None # The short description of the Incident.
    impact: str | None = None
    impact_id: int | None = None
    impact_score: int | None = None
    priority_id: int | None = None
    src_url: AnyUrl | None = None # A Url link used to access the original incident.
    status: str | None = None # The normalized status of the Incident normalized to the caption of the
                              # status_id value. In the case of 'Other', it is defined by the source.
    verdict: str | None = None
    verdict_id: int | None = None

    # Optional:
    activity_name: str | None = None # The Incident activity name, as defined by the
                                     # `activity_id`.
    assignee: User | None = None
    assignee_group: Group | None = None
    attacks: list[MITREATTCK] | None = None # An array of MITRE ATT&CK objects
                                            # describing the tactics, techniques & sub-techniques
                                            # associated to the Incident.
    comment: str | None = None # Additional user supplied details for updating or closing the incident.
    confidence: str | None = None
    confidence_score: int | None = None
    end_time: datetime | None = None # The time of the most recent event included in the incident.
    priority: str | None = None
    start_time: datetime | None = None # The time of the least recent event included in the incident.
    is_suspected_breach: bool | None = None
