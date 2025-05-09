# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import builtins
import builtins
from enum import Enum

__all__ = [
    'AdditionalVmPatch',
    'AssessmentDayOfWeek',
    'AutoBackupDaysOfWeek',
    'BackupScheduleType',
    'ClusterSubnetType',
    'Commit',
    'ConnectivityType',
    'DayOfWeek',
    'DiskConfigurationType',
    'Failover',
    'FullBackupFrequencyType',
    'IdentityType',
    'LeastPrivilegeMode',
    'ReadableSecondary',
    'Role',
    'SqlImageSku',
    'SqlManagementMode',
    'SqlServerLicenseType',
    'SqlVmGroupImageSku',
    'SqlWorkloadType',
    'StorageWorkloadType',
    'VmIdentityType',
]


class AdditionalVmPatch(builtins.str, Enum):
    """
    Additional Patch to be enable or enabled on the SQL Virtual Machine.
    """
    NOT_SET = "NotSet"
    MICROSOFT_UPDATE = "MicrosoftUpdate"


class AssessmentDayOfWeek(builtins.str, Enum):
    """
    Day of the week to run assessment.
    """
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class AutoBackupDaysOfWeek(builtins.str, Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class BackupScheduleType(builtins.str, Enum):
    """
    Backup schedule type.
    """
    MANUAL = "Manual"
    AUTOMATED = "Automated"


class ClusterSubnetType(builtins.str, Enum):
    """
    Cluster subnet type.
    """
    SINGLE_SUBNET = "SingleSubnet"
    MULTI_SUBNET = "MultiSubnet"


class Commit(builtins.str, Enum):
    """
    Replica commit mode in availability group.
    """
    SYNCHRONOUS_COMMIT = "Synchronous_Commit"
    ASYNCHRONOUS_COMMIT = "Asynchronous_Commit"


class ConnectivityType(builtins.str, Enum):
    """
    SQL Server connectivity option.
    """
    LOCAL = "LOCAL"
    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"


class DayOfWeek(builtins.str, Enum):
    """
    Day of week to apply the patch on.
    """
    EVERYDAY = "Everyday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class DiskConfigurationType(builtins.str, Enum):
    """
    Disk configuration to apply to SQL Server.
    """
    NEW = "NEW"
    EXTEND = "EXTEND"
    ADD = "ADD"


class Failover(builtins.str, Enum):
    """
    Replica failover mode in availability group.
    """
    AUTOMATIC = "Automatic"
    MANUAL = "Manual"


class FullBackupFrequencyType(builtins.str, Enum):
    """
    Frequency of full backups. In both cases, full backups begin during the next scheduled time window.
    """
    DAILY = "Daily"
    WEEKLY = "Weekly"


class IdentityType(builtins.str, Enum):
    """
    The identity type. Set this to 'SystemAssigned' in order to automatically create and assign an Azure Active Directory principal for the resource.
    """
    NONE = "None"
    SYSTEM_ASSIGNED = "SystemAssigned"
    USER_ASSIGNED = "UserAssigned"
    SYSTEM_ASSIGNED_USER_ASSIGNED = "SystemAssigned,UserAssigned"


class LeastPrivilegeMode(builtins.str, Enum):
    """
    SQL IaaS Agent least privilege mode.
    """
    ENABLED = "Enabled"
    NOT_SET = "NotSet"


class ReadableSecondary(builtins.str, Enum):
    """
    Replica readable secondary mode in availability group.
    """
    NO = "No"
    ALL = "All"
    READ_ONLY = "Read_Only"


class Role(builtins.str, Enum):
    """
    Replica Role in availability group.
    """
    PRIMARY = "Primary"
    SECONDARY = "Secondary"


class SqlImageSku(builtins.str, Enum):
    """
    SQL Server edition type.
    """
    DEVELOPER = "Developer"
    EXPRESS = "Express"
    STANDARD = "Standard"
    ENTERPRISE = "Enterprise"
    WEB = "Web"


class SqlManagementMode(builtins.str, Enum):
    """
    SQL Server Management type. NOTE: This parameter is not used anymore. API will automatically detect the Sql Management, refrain from using it.
    """
    FULL = "Full"
    LIGHT_WEIGHT = "LightWeight"
    NO_AGENT = "NoAgent"


class SqlServerLicenseType(builtins.str, Enum):
    """
    SQL Server license type.
    """
    PAYG = "PAYG"
    AHUB = "AHUB"
    DR = "DR"


class SqlVmGroupImageSku(builtins.str, Enum):
    """
    SQL image sku.
    """
    DEVELOPER = "Developer"
    ENTERPRISE = "Enterprise"


class SqlWorkloadType(builtins.str, Enum):
    """
    SQL Server workload type.
    """
    GENERAL = "GENERAL"
    OLTP = "OLTP"
    DW = "DW"


class StorageWorkloadType(builtins.str, Enum):
    """
    Storage workload type.
    """
    GENERAL = "GENERAL"
    OLTP = "OLTP"
    DW = "DW"


class VmIdentityType(builtins.str, Enum):
    """
    Identity type of the virtual machine. Specify None to opt-out of Managed Identities.
    """
    NONE = "None"
    SYSTEM_ASSIGNED = "SystemAssigned"
    USER_ASSIGNED = "UserAssigned"
