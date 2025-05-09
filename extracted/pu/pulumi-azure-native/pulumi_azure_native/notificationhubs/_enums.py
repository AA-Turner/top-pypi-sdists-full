# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import builtins
import builtins
from enum import Enum

__all__ = [
    'AccessRights',
    'NamespaceStatus',
    'NamespaceType',
    'OperationProvisioningState',
    'PrivateEndpointConnectionProvisioningState',
    'PrivateLinkConnectionStatus',
    'PublicNetworkAccess',
    'ReplicationRegion',
    'SkuName',
    'ZoneRedundancyPreference',
]


class AccessRights(builtins.str, Enum):
    """
    Defines values for AccessRights.
    """
    MANAGE = "Manage"
    SEND = "Send"
    LISTEN = "Listen"


class NamespaceStatus(builtins.str, Enum):
    """
    Namespace status.
    """
    CREATED = "Created"
    CREATING = "Creating"
    SUSPENDED = "Suspended"
    DELETING = "Deleting"


class NamespaceType(builtins.str, Enum):
    """
    Defines values for NamespaceType.
    """
    MESSAGING = "Messaging"
    NOTIFICATION_HUB = "NotificationHub"


class OperationProvisioningState(builtins.str, Enum):
    """
    Defines values for OperationProvisioningState.
    """
    UNKNOWN = "Unknown"
    IN_PROGRESS = "InProgress"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    CANCELED = "Canceled"
    PENDING = "Pending"
    DISABLED = "Disabled"


class PrivateEndpointConnectionProvisioningState(builtins.str, Enum):
    """
    State of Private Endpoint Connection.
    """
    UNKNOWN = "Unknown"
    SUCCEEDED = "Succeeded"
    CREATING = "Creating"
    UPDATING = "Updating"
    UPDATING_BY_PROXY = "UpdatingByProxy"
    DELETING = "Deleting"
    DELETING_BY_PROXY = "DeletingByProxy"
    DELETED = "Deleted"


class PrivateLinkConnectionStatus(builtins.str, Enum):
    """
    State of Private Link Connection.
    """
    DISCONNECTED = "Disconnected"
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"


class PublicNetworkAccess(builtins.str, Enum):
    """
    Type of public network access.
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class ReplicationRegion(builtins.str, Enum):
    """
    Allowed replication region
    """
    DEFAULT = "Default"
    WEST_US2 = "WestUs2"
    NORTH_EUROPE = "NorthEurope"
    AUSTRALIA_EAST = "AustraliaEast"
    BRAZIL_SOUTH = "BrazilSouth"
    SOUTH_EAST_ASIA = "SouthEastAsia"
    SOUTH_AFRICA_NORTH = "SouthAfricaNorth"
    NONE = "None"


class SkuName(builtins.str, Enum):
    """
    Namespace SKU name.
    """
    FREE = "Free"
    BASIC = "Basic"
    STANDARD = "Standard"


class ZoneRedundancyPreference(builtins.str, Enum):
    """
    Namespace SKU name.
    """
    DISABLED = "Disabled"
    ENABLED = "Enabled"
