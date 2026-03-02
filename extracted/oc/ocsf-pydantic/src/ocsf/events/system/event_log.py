from enum import Enum

from ocsf.events.system import SystemActivity

from ocsf.objects.actor import Actor
from ocsf.objects.device import Device
from ocsf.objects.file import File
from ocsf.objects.network_endpoint import NetworkEndpoint

class EventLogActivityActivityId(Enum):
    Clear: int = 1 # Clear the event log database, file, or cache.
    Delete: int = 2 # Delete the event log database, file, or cache.
    Export: int = 3 # Export the event log database, file, or cache.
    Archive: int = 4 # Archive the event log database, file, or cache.
    Rotate: int = 5 # Rotate the event log database, file, or cache.
    Start: int = 6 # Start the event logging service.
    Stop: int = 7 # Stop the event logging service.
    Restart: int = 8 # Restart the event logging service.
    Enable: int = 9 # Enable the event logging service.
    Disable: int = 10 # Disable the event logging service.


class EventLogActivity(SystemActivity):
    """
    Event Log Activity events report actions pertaining to the system's event
    logging service(s), such as disabling logging or clearing the log data.
    """

    class_uid: int = 1008
    class_name: str = 'Event Log Activity'

    # Recommended:
    actor: Actor | None = None # The actor that performed the activity.
    device: Device | None = None # The device that reported the event.
    dst_endpoint: NetworkEndpoint | None = None # The targeted endpoint for the event log activity.
    file: File | None = None # The file targeted by the activity. Example: `/var/log/audit.log`
    log_name: str | None = None # The name of the event log  targeted by the activity.
                                # Example: Windows `Security`.
    log_provider: str | None = None # The logging provider or logging service targeted by the activity.
                                    # Example: `Microsoft-Windows-Security-Auditing`, `Auditd`, or `Syslog`.
    log_type: str | None = None
    log_type_id: int | None = None
    src_endpoint: NetworkEndpoint | None = None # The source endpoint for the event log activity.
    status_code: str | None = None # The event status code, as reported by the event source.
                                   # Example: `0`, `8`, or `21` for Windows ClearEventLog
    status_detail: str | None = None # The status detail contains additional information about the
                                     # event outcome.
                                     # Example: `Success`, `Privilege Missing`, or `Invalid
                                     # Parameter` Windows ClearEventLog

    # Optional:
    activity_id: EventLogActivityActivityId | None = None
