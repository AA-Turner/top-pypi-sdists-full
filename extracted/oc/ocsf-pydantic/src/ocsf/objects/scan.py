from enum import Enum
from ._entity import Entity

class ScanTypeId(Enum):
    """
    The type id of the scan.
    """
    Unknown: int = 0
    Manual: int = 1 # The scan was manually initiated by the user or administrator.
    Scheduled: int = 2 # The scan was started based on scheduler.
    Updated_Content: int = 3 # The scan was triggered by a content update.
    Quarantined_Items: int = 4 # The scan was triggered by newly quarantined items.
    Attached_Media: int = 5 # The scan was triggered by the attachment of removable media.
    User_Logon: int = 6 # The scan was started due to a user logon.
    Elam: int = 7 # The scan was triggered by an Early Launch Anti-Malware (ELAM) detection.
    Other: int = 99 # The scan type id is not mapped. See the <code>type</code> attribute,
                    # which contains a data source specific value.

class Scan(Entity):
    """
    The Scan object describes characteristics of a proactive scan.
    """

    type_id: ScanTypeId # The type id of the scan.


    # Optional:
    name: str | None = None # The administrator-supplied or application-generated name of the scan. For
                            # example: "Home office weekly user database scan", "Scan folders for
                            # viruses", "Full system virus scan"
    type: str | None = None # The type of scan.
    uid: str | None = None # The application-defined unique identifier assigned to an instance of a
                           # scan.
