from datetime import datetime
from enum import Enum

from ocsf.objects.scan import Scan
from ocsf.objects.policy import Policy

from ocsf.events.base import BaseEvent


class ScanActivityActivityId(Enum):
    Started: int = 1
    Completed: int = 2
    Cancelled: int = 3
    Duration_Violation: int = 4
    Pause_Violation: int = 5
    Error: int = 6
    Paused: int = 7
    Resumed: int = 8
    Restarted: int = 9
    Delayed: int = 10

class ScanActivity(BaseEvent):
    """
    Scan events report the start, completion, and results of a scan job. The scan
    event includes the number of items that were scanned and the number of
    detections that were resolved.
    """
    class_uid: int = 6007
    class_name: str = 'Scan Activity'

    scan: Scan # The Scan object describes characteristics of the scan job.

    # Recommended:
    command_uid: str | None = None # The command identifier that is associated with this scan event.
                                   # This ID uniquely identifies the proactive scan command, e.g., if
                                   # remotely initiated.
    duration: int | None = None # The duration of the scan
    end_time: datetime | None = None # The end time of the scan job.
    num_detections: int | None = None
    num_files: int | None = None
    num_folders: int | None = None
    num_network_items: int | None = None
    num_processes: int | None = None
    num_registry_items: int | None = None
    num_resolutions: int | None = None
    num_skipped_items: int | None = None
    num_trusted_items: int | None = None
    policy: Policy | None = None # The policy associated with this Scan event; required if the scan was
                                 # initiated by a policy.
    schedule_uid: str | None = None
    start_time: datetime | None = None # The start time of the scan job.
    total: int | None = None # The total number of items that were scanned; zero if no items were
                             # scanned.

    # Optional:
    activity_id: ScanActivityActivityId | None = None
