from enum import Enum

from pydantic import BaseModel

from .policy import Policy

class AgentTypeId(Enum):
    """
    The normalized representation of an agent or sensor. E.g., EDR, vulnerability
    management, APM, backup & recovery, etc.
    """
    Endpoint_Detection_And_Response: int = 1 # Any EDR sensor or agent. Or any tool that
                                             # provides similar threat detection, anti-malware,
                                             # anti-ransomware, or similar capabilities. E.g.,
                                             # Crowdstrike Falcon, Microsoft Defender for Endpoint,
                                             # Wazuh.
    Data_Loss_Prevention: int = 2 # Any DLP sensor or agent. Or any tool that provides similar data
                                  # classification, data loss detection, and/or data loss prevention
                                  # capabilities. E.g., Forcepoint DLP, Microsoft Purview, Symantec
                                  # DLP.
    Backup_and_Recovery: int = 3 # Any agent or sensor that provides backups, archival, or recovery
                                 # capabilities. E.g., Azure Backup, AWS Backint Agent.
    Performance_Monitoring_and_Observability: int = 4 # Any agent or sensor that provides Application
                                                      # Performance Monitoring (APM), active tracing,
                                                      # profiling, or other observability use cases and
                                                      # optionally forwards the logs. E.g.,
                                                      # New Relic Agent, Datadog Agent, Azure Monitor Agent.
    VulnerabilityManagement: int = 5 # Any agent or sensor that provides vulnerability management
                                      # or scanning capabilities. E.g., Qualys VMDR, Microsoft
                                      # Defender for Endpoint, Crowdstrike Spotlight, Amazon Inspector Agent.
    Log_Forwarding: int = 6 # Any agent or sensor that forwards logs to a 3rd party storage system such as
                            # a data lake or SIEM. E.g., Splunk Universal Forwarder, Tenzir, FluentBit, Amazon
                            # CloudWatch Agent, Amazon Kinesis Agent.
    Mobile_Device_Management: int = 7 # Any agent or sensor responsible for providing Mobile Device Management
                                      # (MDM) or Mobile Enterprise Management (MEM) capabilities. E.g.,
                                      # JumpCloud Agent, Esper Agent, Jamf Pro binary.
    Configuration_Management: int = 8 # Any agent or sensor that provides configuration management of a device,
                                      # such as scanning for software, license management, or applying
                                      # configurations. E.g., AWS Systems Manager Agent, Flexera,
                                      # ServiceNow MID Server.
    Remote_Access: int = 9 # Any agent or sensor that provides remote access capabilities to a device. E.g.,
                           # BeyondTrust, Amazon Systems Manager Agent, Verkada Agent.

class Agent(BaseModel):
    """
    An Agent (also known as a Sensor) is typically installed on an Operating System
    (OS) and serves as a specialized software component that can be designed to
    monitor, detect, collect, archive, or take action. These activities and possible
    actions are defined by the upstream system controlling the Agent and its
    intended purpose. For instance, an Agent can include Endpoint Detection &
    Response (EDR) agents, backup/disaster recovery sensors, Application Performance
    Monitoring or profiling sensors, and similar software.
    """

    # Recommended:
    type_id: AgentTypeId | None = None # The normalized representation of an agent or sensor. E.g.,
                                       # EDR, vulnerability management, APM, backup & recovery, etc.
    uid: str | None = None # The UID of the agent or sensor, sometimes known as a Sensor ID or
                           # `aid`.
    name: str | None = None # The name of the agent or sensor. For example: `AWS SSM Agent`.

    # Optional:
    type: str | None = None # The normalized caption of the type_id value for the agent or sensor. In
                            # the case of 'Other' or 'Unknown', it is defined by the event source.
    uid_alt: str | None = None # An alternative or contextual identifier for the agent or sensor, such
                               # as a configuration, organization, or license UID.
    version: str | None = None # The semantic version of the agent or sensor, e.g.,
                               # `7.101.50.0`.
    vendor_name: str | None = None # The company or author who created the agent or sensor. For
                                   # example: `Crowdstrike`.
    policies: list[Policy] | None = None # Describes the various policies that may be applied or
                                         # enforced by an agent or sensor. E.g., Conditional Access,
                                         # prevention, auto-update, tamper protection, destination
                                         # configuration, etc.
