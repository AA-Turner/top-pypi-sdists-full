from datetime import datetime

from pydantic.networks import IPvAnyAddress

from .image import Image
from .network_interface import NetworkInterface
from .group import Group
from .organization import Organization
from .endpoint import Endpoint
from .location import GeoLocation


class Device(Endpoint):
    """
    The Device object represents an addressable computer system or host, which is
    typically connected to a computer network and participates in the transmission
    or processing of data within the computer network. Defined by D3FEND <a
    target='_blank'
    href='https://d3fend.mitre.org/dao/artifact/d3f:Host/'>d3f:Host</a>.
    """

    type_id: int # The device type ID.

    # Recommended:
    hostname: str | None = None # The device hostname.
    region: str | None = None # The region where the virtual machine is located. For example, an AWS
                              # Region.
    type: str | None = None # The device type. For example: `unknown`, `server`,
                            # `desktop`, `laptop`, `tablet`,
                            # `mobile`, `virtual`, `browser`, or
                            # `other`.
    uid: str | None = None # The unique identifier of the device. For example the Windows TargetSID or
                           # AWS EC2 ARN.

    # Optional:
    autoscale_uid: str | None = None
    created_time: datetime | None = None # The time when the device was known to have been created.
    desc: str | None = None # The description of the device, ordinarily as reported by the operating
                            # system.
    domain: str | None = None # The network domain where the device resides. For example:
                              # `work.example.com`.
    first_seen_time: datetime | None = None # The initial discovery time of the device.
    groups: list[Group] | None = None # The group names to which the device belongs. For example:
                                      # `["Windows Laptops", "Engineering"]<code/>.
    hypervisor: str | None = None
    image: Image | None = None # The image used as a template to run the virtual machine.
    imei: str | None = None
    ip: IPvAnyAddress | None = None # The device IP address, in either IPv4 or IPv6 format.
    is_compliant: bool | None = None
    is_managed: bool | None = None
    is_personal: bool | None = None
    is_trusted: bool | None = None
    last_seen_time: datetime | None = None # The most recent discovery time of the device.
    location: GeoLocation | None = None # The geographical location of the device.
    modified_time: datetime | None = None # The time when the device was last known to have been
                                          # modified.
    name: str | None = None # The alternate device name, ordinarily as assigned by an administrator.
                            # <p><b>Note:</b> The <b>Name</b> could be any other string that helps to
                            # identify the device, such as a phone number; for example
                            # `310-555-1234`.</p>
    network_interfaces: list[NetworkInterface] | None = None
    org: Organization | None = None # Organization and org unit related to the device.
    risk_level: str | None = None
    risk_level_id: int | None = None
    risk_score: int | None = None
    subnet: str | None = None
    uid_alt: str | None = None # An alternate unique identifier of the device if any. For example the
                               # ActiveDirectory DN.
