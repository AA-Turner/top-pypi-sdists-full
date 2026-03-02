from enum import Enum

from pydantic import BaseModel
from .file import File


class ModuleLoadTypeId(Enum):
    Unknown: int = 0
    Standard: int = 1 # A normal module loaded by the normal windows loading
                      # mechanism i.e. LoadLibrary.
    Non_Standard: int = 2 # A module loaded in a way avoidant of normal windows
                          # procedures. i.e. Bootstrapped Loading/Manual Dll Loading.
    Shellcode: int = 3 # A raw module in process memory that is READWRITE_EXECUTE and
                       # had a thread started in its range.
    Mapped: int = 4 # A memory mapped file, typically created with
                    # CreatefileMapping/MapViewOfFile.
    Nonstandard_Backed: int = 5 # A module loaded in a non standard way. However,
                                # GetModuleFileName succeeds on this allocation.
    Other: int = 99

class Module(BaseModel):
    """
    The Module object describes the load attributes of a module.
    """

    load_type_id: ModuleLoadTypeId

    # Recommended:
    base_address: str | None = None
    file: File | None = None # The module file object.
    start_address: str | None = None
    type: str | None = None # The module type.

    # Optional:
    function_name: str | None = None
    load_type: str | None = None
