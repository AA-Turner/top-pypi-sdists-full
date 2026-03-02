from enum import Enum
from pydantic import BaseModel

class OSTypeId(Enum):
    """
    The type identifier of the operating system.
    """
    Windows: int = 100
    Windows_Mobile: int = 101
    Linux: int = 200
    Android: int = 201
    MacOS: int = 300
    IOS: int = 301
    IPadOS: int = 302
    Solaris: int = 400
    AIX: int = 401
    HPUX: int = 402

class OperatingSystem(BaseModel):
    """
    The Operating System (OS) object describes characteristics of an OS, such as
    Linux or Windows. Defined by D3FEND <a target='_blank' href='https://d3fend.mitr
    e.org/dao/artifact/d3f:OperatingSystem/'>d3f:OperatingSystem</a>.
    """

    name: str # The operating system name.
    type_id: OSTypeId # The type identifier of the operating system.


    # Optional:
    build: str | None = None
    country: str | None = None # The operating system country code, as defined by the ISO 3166-1
                               # standard (Alpha-2 code). For the complete list of country codes, see
                               # <a target='_blank'
                               # href='https://www.iso.org/obp/ui/#iso:pub:PUB500001:en'>ISO 3166-1
                               # alpha-2 codes</a>.
    cpe_name: str | None = None
    cpu_bits: int | None = None
    edition: str | None = None
    lang: str | None = None
    sp_name: str | None = None
    sp_ver: int | None = None
    type: str | None = None # The type of the operating system.
    version: str | None = None # The version of the OS running on the device that originated the event.
                               # For example: "Windows 10", "OS X 10.7", or "iOS 9".
