# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import builtins
import builtins
from enum import Enum

__all__ = [
    'DashboardPartMetadataType',
    'FontSize',
    'FontStyle',
    'OsType',
    'ProvisioningState',
    'ShellType',
]


class DashboardPartMetadataType(builtins.str, Enum):
    """
    The dashboard part metadata type.
    """
    MARKDOWN = "Extension/HubsExtension/PartType/MarkdownPart"
    """
    The markdown part type.
    """


class FontSize(builtins.str, Enum):
    """
    Size of terminal font.
    """
    NOT_SPECIFIED = "NotSpecified"
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"


class FontStyle(builtins.str, Enum):
    """
    Style of terminal font.
    """
    NOT_SPECIFIED = "NotSpecified"
    MONOSPACE = "Monospace"
    COURIER = "Courier"


class OsType(builtins.str, Enum):
    """
    The operating system type of the cloud shell. Deprecated, use preferredShellType.
    """
    WINDOWS = "Windows"
    LINUX = "Linux"


class ProvisioningState(builtins.str, Enum):
    """
    Provisioning state of the console.
    """
    NOT_SPECIFIED = "NotSpecified"
    ACCEPTED = "Accepted"
    PENDING = "Pending"
    UPDATING = "Updating"
    CREATING = "Creating"
    REPAIRING = "Repairing"
    FAILED = "Failed"
    CANCELED = "Canceled"
    SUCCEEDED = "Succeeded"


class ShellType(builtins.str, Enum):
    """
    The shell type of the cloud shell.
    """
    BASH = "bash"
    PWSH = "pwsh"
    POWERSHELL = "powershell"
