from enum import Enum
from pydantic import BaseModel

class KernelResourceTypeId(Enum):
    """
    The type of the kernel resource.
    """
    Shared_Mutex: int = 1
    System_Call: int = 2

class KernelResource(BaseModel):
    """
    The Kernel Resource object provides information about a specific kernel
    resource, including its name and type. It describes essential attributes
    associated with a resource managed by the kernel of an operating system. Defined
    by D3FEND <a target='_blank'
    href='https://d3fend.mitre.org/dao/artifact/d3f:Kernel/'>d3f:Kernel</a>.
    """

    name: str # The name of the kernel resource.
    type_id: KernelResourceTypeId # The type of the kernel resource.


    # Optional:
    is_system: bool | None = None
    path: str | None = None # The full path of the kernel resource.
    system_call: str | None = None
    type: str | None = None # The type of the kernel resource.
