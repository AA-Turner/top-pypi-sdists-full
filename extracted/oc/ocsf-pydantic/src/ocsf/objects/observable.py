from enum import Enum
from pydantic import BaseModel

from .reputation import Reputation

class ObservableTypeId(Enum):
    """
    The observable value type identifier.
    """
    Unknown: int = 0 # Unknown observable data type.
    Hostname: int = 1 # Unique name assigned to a device connected to a computer network. A domain
                      # name in general is an Internet address that can be resolved through the Domain
                      # Name System (DNS). For example: `r2-d2.example.com`.
    IPAddress: int = 2 # Internet Protocol address (IP address), in either IPv4 or IPv6 format. For
                       # example, `192.168.200.24` or `2001:0db8:85a3:0000:0000:8a2e:0370:7334`.
    MACAddress: int = 3 # Media Access Control (MAC) address. For example: `18:36:F3:98:4F:9A`.
    UserName: int = 4 # User name. For example: `john_doe`
    EmailAddress: int = 5 # Email address. For example: `john_doe@example.com`.
    URLString: int = 6 # Uniform Resource Locator (URL) string.
    FileName: int = 7 # File name. For example: `text-file.txt`.
    Hash: int = 8 # Hash. A unique value that corresponds to the content of the file, image, ja3_hash
                  # or hassh found in the schema. For example MD5: `3172ac7e2b55cbb81f04a6e65855a628`.
    ProcessName: int = 9 # Process name. For example: `Notepad`.
    ResourceUID: int = 10 # Resource unique identifier. For example, S3 Bucket name or EC2 Instance ID.
    Port: int = 11 # The TCP/UDP port number. For example: 80 or 22.
    Subnet: int = 12 # The subnet represented in a CIDR notation, using the format
                     # network_address/prefix_length. The network_address can be in either IPv4 or IPv6
                     # format. The prefix length indicates the number of bits used for the network
                     # portion, and the remaining bits are available for host addresses within that
                     # subnet. For example: `192.168.1.0/24` `2001:0db8:85a3:0000::/64`
    CommandLine: int = 13 # The full command line used to launch an application, service, process, or
                          # job. For example: `ssh user@10.0.0.10`. If the command line is
                          # unavailable or missing, the empty string `''` is to be used.
    Country: str = 14 # The ISO 3166-1 Alpha-2 country code.
    ProcessID: int = 15 # The process identifier, as reported by the operating system. Process ID (PID)
                        # is a number used by the operating system to uniquely identify an active process.
    HTTPUserAgent: str = 16 # The request header that identifies the operating system and web browser.
    CWE: int = 17 # CWE Object: uid (Object-Specific Attribute)
    CVE: int = 18 # CVE Object: uid (Object-Specific Attribute)
    Endpoint: int = 20 # The Endpoint object describes a physical or virtual device that connects to and
                          # exchanges information with a computer network. Some examples of endpoints are
                            # mobile devices, desktop computers, virtual machines, embedded devices, and
                            # servers. Internet-of-Things devices—like cameras, lighting, refrigerators,
                            # security systems, smart speakers, and thermostats—are also endpoints.
    User: int = 21 # The User object describes the characteristics of a user/person or a security
                     # principal.
    Email: int = 22 # The Email object describes the email metadata such as sender, recipients, and
                    # direction.
    
    URL: int = 23 # The Uniform Resource Locator(URL) object describes the characteristics of a URL.
    File: int = 24 # The File object represents the metadata associated with a file stored in a
                   # computer system. It encompasses information about the file itself, including its
                   # attributes, properties, and organizational details.
    Process: int = 25 # The Process object describes a running instance of a launched program.
    GeoLocation: int = 26 # The Geo Location object describes a geographical location, usually associated
                          # with an IP address.
    Container: int = 27 # The Container object describes an instance of a specific container. A container is
                        # a prepackaged, portable system image that runs isolated on an existing system using a
                        # container runtime like containerd.
    RegistryKey: int = 28 # The registry key object describes a Windows registry key.
    RegistryValue: int = 29 # The registry value object describes a Windows registry value.
    Fingerprint: int = 30 # The Fingerprint object provides detailed information about a digital fingerprint,
                          # which is a compact representation of data used to identify a longer piece of
                          # information, such as a public key or file content. It contains the algorithm and
                          # value of the fingerprint, enabling efficient and reliable identification of the
                          # associated data.

    Other: int = 99 # The observable data type is not mapped. See the `type` attribute,
                    # which may contain data source specific value.

class Observable(BaseModel):
    """
    The observable object is a pivot element that contains related information found
    in many places in the event.
    """

    name: str # The full name of the observable attribute. The `name` is a
              # pointer/reference to an attribute within the event data. For example:
              # `file.name`.
    type_id: ObservableTypeId # The observable value type identifier.


    # Optional:
    reputation: Reputation | None = None
    type: str | None = None # The observable value type name.
    value: str | None = None # The value associated with the observable attribute. The meaning of the
                             # value depends on the observable type.<br/>If the `name`
                             # refers to a scalar attribute, then the `value` is the value
                             # of the attribute.<br/>If the `name` refers to an object
                             # attribute, then the `value` is not populated.
