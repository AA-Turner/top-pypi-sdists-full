from enum import Enum

from ocsf.events.system import SystemActivity

from ocsf.objects.process import Process


class MemoryActivityActivityId(Enum):
    Allocate_Page: int = 1
    Modify_Page: int = 2
    Delete_Page: int = 3
    Buffer_Overflow: int = 4
    Disable_Dep: int = 5 # Data Execution Permission
    Enable_Dep: int = 6 # Data Execution Permission
    Read: int = 7 # Read (Example: `ReadProcessMemory`)
    Write: int = 8 # Write (Example: `WriteProcessMemory`)
    Map_View: int = 9 # Map View (Example: `MapViewOfFile2`)


class MemoryActivity(SystemActivity):
    """
    Memory Activity events report when a process has memory allocated,
    read/modified, or other manipulation activities - such as a buffer overflow or
    turning off data execution protection (DEP).
    """

    class_uid: int = 1004
    class_name: str = 'Memory Activity'

    process: Process # The process that had memory allocated, read/written, or had other
                     # manipulation activities performed on it.

    # Recommended:
    actual_permissions: int | None = None
    base_address: str | None = None # The memory address that was access or requested.
    requested_permissions: int | None = None
    size: int | None = None # The memory size that was access or requested.

    # Optional:
    activity_id: MemoryActivityActivityId | None = None
