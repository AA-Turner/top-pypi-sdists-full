from enum import Enum
from pydantic import BaseModel

class SecurityStateStateId(Enum):
    """
    The security state of the managed entity.
    """
    Unknown: int = 0
    Missing_Or_Outdated_Content: int = 1 # The content is missing or outdated.
    Policy_Mismatch: int = 2 # Not in compliance with the expected security policy.
    In_Network_Quarantine: int = 3 # Isolated from the network.
    Protection_Off: int = 4 # Not protected by a security solution.
    Protection_Malfunction: int = 5 # The security solution is not functioning properly.
    Protection_Not_Licensed: int = 6 # The security solution does not have a valid license.
    Unremediated_Threat: int = 7 # A detected threat has not been remediated.
    Suspicious_Reputation: int = 8 # Reputation of the entity is suspicious.
    Reboot_Pending: int = 9 # A reboot is required for one or more pending actions.
    Content_Is_Locked: int = 10 # The content is locked to a specific version.
    Not_Installed: int = 11 # The entity is not installed.
    Writable_System_Partition: int = 12 # The system partition is writeable.
    Safetynet_Failure: int = 13 # The device has failed the SafetyNet check.
    Failed_Boot_Verify: int = 14 # The device has failed the boot verification process.
    Modified_Execution_Environment: int = 15 # The execution environment has been modified.
    Selinux_Disabled: int = 16 # The SELinux security feature has been disabled.
    Elevated_Privilege_Shell: int = 17 # An elevated privilege shell has been detected.
    Ios_File_System_Altered: int = 18 # The file system has been altered on an iOS device.
    Open_Remote_Access: int = 19 # Remote access is enabled.
    Ota_Updates_Disabled: int = 20 # Mobile OTA (Over The Air) updates have been disabled.
    Rooted: int = 21 # The device has been modified to allow root access.
    Android_Partition_Modified: int = 22 # The Android partition has been modified.
    Compliance_Failure: int = 23 # The entity is not compliant with the associated security policy.
    Other: int = 99

class SecurityState(BaseModel):
    """
    The Security State object describes the security related state of a managed
    entity.
    """

    # Recommended:
    state_id: SecurityStateStateId | None = None # The security state of the managed entity.

    # Optional:
    state: str | None = None # The security state, normalized to the caption of the state_id value. In
                             # the case of 'Other', it is defined by the source.
