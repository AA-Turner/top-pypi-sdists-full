# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import builtins
import copy
import warnings
import sys
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
if sys.version_info >= (3, 11):
    from typing import NotRequired, TypedDict, TypeAlias
else:
    from typing_extensions import NotRequired, TypedDict, TypeAlias
from .. import _utilities
from . import outputs

__all__ = [
    'ScraperDestination',
    'ScraperDestinationAmpConfigurationProperties',
    'ScraperRoleConfiguration',
    'ScraperScrapeConfiguration',
    'ScraperSource',
    'ScraperSourceEksConfigurationProperties',
    'WorkspaceLoggingConfiguration',
]

@pulumi.output_type
class ScraperDestination(dict):
    """
    Scraper metrics destination
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ampConfiguration":
            suggest = "amp_configuration"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ScraperDestination. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ScraperDestination.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ScraperDestination.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 amp_configuration: Optional['outputs.ScraperDestinationAmpConfigurationProperties'] = None):
        """
        Scraper metrics destination
        :param 'ScraperDestinationAmpConfigurationProperties' amp_configuration: Configuration for Amazon Managed Prometheus metrics destination
        """
        if amp_configuration is not None:
            pulumi.set(__self__, "amp_configuration", amp_configuration)

    @property
    @pulumi.getter(name="ampConfiguration")
    def amp_configuration(self) -> Optional['outputs.ScraperDestinationAmpConfigurationProperties']:
        """
        Configuration for Amazon Managed Prometheus metrics destination
        """
        return pulumi.get(self, "amp_configuration")


@pulumi.output_type
class ScraperDestinationAmpConfigurationProperties(dict):
    """
    Configuration for Amazon Managed Prometheus metrics destination
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "workspaceArn":
            suggest = "workspace_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ScraperDestinationAmpConfigurationProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ScraperDestinationAmpConfigurationProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ScraperDestinationAmpConfigurationProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 workspace_arn: builtins.str):
        """
        Configuration for Amazon Managed Prometheus metrics destination
        :param builtins.str workspace_arn: ARN of an Amazon Managed Prometheus workspace
        """
        pulumi.set(__self__, "workspace_arn", workspace_arn)

    @property
    @pulumi.getter(name="workspaceArn")
    def workspace_arn(self) -> builtins.str:
        """
        ARN of an Amazon Managed Prometheus workspace
        """
        return pulumi.get(self, "workspace_arn")


@pulumi.output_type
class ScraperRoleConfiguration(dict):
    """
    Role configuration
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "sourceRoleArn":
            suggest = "source_role_arn"
        elif key == "targetRoleArn":
            suggest = "target_role_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ScraperRoleConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ScraperRoleConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ScraperRoleConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 source_role_arn: Optional[builtins.str] = None,
                 target_role_arn: Optional[builtins.str] = None):
        """
        Role configuration
        :param builtins.str source_role_arn: IAM Role in source account
        :param builtins.str target_role_arn: IAM Role in the target account
        """
        if source_role_arn is not None:
            pulumi.set(__self__, "source_role_arn", source_role_arn)
        if target_role_arn is not None:
            pulumi.set(__self__, "target_role_arn", target_role_arn)

    @property
    @pulumi.getter(name="sourceRoleArn")
    def source_role_arn(self) -> Optional[builtins.str]:
        """
        IAM Role in source account
        """
        return pulumi.get(self, "source_role_arn")

    @property
    @pulumi.getter(name="targetRoleArn")
    def target_role_arn(self) -> Optional[builtins.str]:
        """
        IAM Role in the target account
        """
        return pulumi.get(self, "target_role_arn")


@pulumi.output_type
class ScraperScrapeConfiguration(dict):
    """
    Scraper configuration
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "configurationBlob":
            suggest = "configuration_blob"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ScraperScrapeConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ScraperScrapeConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ScraperScrapeConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 configuration_blob: Optional[builtins.str] = None):
        """
        Scraper configuration
        :param builtins.str configuration_blob: Prometheus compatible scrape configuration in base64 encoded blob format
        """
        if configuration_blob is not None:
            pulumi.set(__self__, "configuration_blob", configuration_blob)

    @property
    @pulumi.getter(name="configurationBlob")
    def configuration_blob(self) -> Optional[builtins.str]:
        """
        Prometheus compatible scrape configuration in base64 encoded blob format
        """
        return pulumi.get(self, "configuration_blob")


@pulumi.output_type
class ScraperSource(dict):
    """
    Scraper metrics source
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "eksConfiguration":
            suggest = "eks_configuration"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ScraperSource. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ScraperSource.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ScraperSource.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 eks_configuration: Optional['outputs.ScraperSourceEksConfigurationProperties'] = None):
        """
        Scraper metrics source
        :param 'ScraperSourceEksConfigurationProperties' eks_configuration: Configuration for EKS metrics source
        """
        if eks_configuration is not None:
            pulumi.set(__self__, "eks_configuration", eks_configuration)

    @property
    @pulumi.getter(name="eksConfiguration")
    def eks_configuration(self) -> Optional['outputs.ScraperSourceEksConfigurationProperties']:
        """
        Configuration for EKS metrics source
        """
        return pulumi.get(self, "eks_configuration")


@pulumi.output_type
class ScraperSourceEksConfigurationProperties(dict):
    """
    Configuration for EKS metrics source
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clusterArn":
            suggest = "cluster_arn"
        elif key == "subnetIds":
            suggest = "subnet_ids"
        elif key == "securityGroupIds":
            suggest = "security_group_ids"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ScraperSourceEksConfigurationProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ScraperSourceEksConfigurationProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ScraperSourceEksConfigurationProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cluster_arn: builtins.str,
                 subnet_ids: Sequence[builtins.str],
                 security_group_ids: Optional[Sequence[builtins.str]] = None):
        """
        Configuration for EKS metrics source
        :param builtins.str cluster_arn: ARN of an EKS cluster
        :param Sequence[builtins.str] subnet_ids: List of subnet IDs
        :param Sequence[builtins.str] security_group_ids: List of security group IDs
        """
        pulumi.set(__self__, "cluster_arn", cluster_arn)
        pulumi.set(__self__, "subnet_ids", subnet_ids)
        if security_group_ids is not None:
            pulumi.set(__self__, "security_group_ids", security_group_ids)

    @property
    @pulumi.getter(name="clusterArn")
    def cluster_arn(self) -> builtins.str:
        """
        ARN of an EKS cluster
        """
        return pulumi.get(self, "cluster_arn")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Sequence[builtins.str]:
        """
        List of subnet IDs
        """
        return pulumi.get(self, "subnet_ids")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Optional[Sequence[builtins.str]]:
        """
        List of security group IDs
        """
        return pulumi.get(self, "security_group_ids")


@pulumi.output_type
class WorkspaceLoggingConfiguration(dict):
    """
    Logging configuration
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "logGroupArn":
            suggest = "log_group_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkspaceLoggingConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkspaceLoggingConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkspaceLoggingConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 log_group_arn: Optional[builtins.str] = None):
        """
        Logging configuration
        :param builtins.str log_group_arn: CloudWatch log group ARN
        """
        if log_group_arn is not None:
            pulumi.set(__self__, "log_group_arn", log_group_arn)

    @property
    @pulumi.getter(name="logGroupArn")
    def log_group_arn(self) -> Optional[builtins.str]:
        """
        CloudWatch log group ARN
        """
        return pulumi.get(self, "log_group_arn")


