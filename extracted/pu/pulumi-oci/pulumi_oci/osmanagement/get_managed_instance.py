# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
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
    'GetManagedInstanceResult',
    'AwaitableGetManagedInstanceResult',
    'get_managed_instance',
    'get_managed_instance_output',
]

@pulumi.output_type
class GetManagedInstanceResult:
    """
    A collection of values returned by getManagedInstance.
    """
    def __init__(__self__, autonomouses=None, bug_updates_available=None, child_software_sources=None, compartment_id=None, description=None, display_name=None, enhancement_updates_available=None, id=None, is_data_collection_authorized=None, is_reboot_required=None, ksplice_effective_kernel_version=None, last_boot=None, last_checkin=None, managed_instance_groups=None, managed_instance_id=None, notification_topic_id=None, os_family=None, os_kernel_version=None, os_name=None, os_version=None, other_updates_available=None, parent_software_sources=None, scheduled_job_count=None, security_updates_available=None, status=None, updates_available=None, work_request_count=None):
        if autonomouses and not isinstance(autonomouses, list):
            raise TypeError("Expected argument 'autonomouses' to be a list")
        pulumi.set(__self__, "autonomouses", autonomouses)
        if bug_updates_available and not isinstance(bug_updates_available, int):
            raise TypeError("Expected argument 'bug_updates_available' to be a int")
        pulumi.set(__self__, "bug_updates_available", bug_updates_available)
        if child_software_sources and not isinstance(child_software_sources, list):
            raise TypeError("Expected argument 'child_software_sources' to be a list")
        pulumi.set(__self__, "child_software_sources", child_software_sources)
        if compartment_id and not isinstance(compartment_id, str):
            raise TypeError("Expected argument 'compartment_id' to be a str")
        pulumi.set(__self__, "compartment_id", compartment_id)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if enhancement_updates_available and not isinstance(enhancement_updates_available, int):
            raise TypeError("Expected argument 'enhancement_updates_available' to be a int")
        pulumi.set(__self__, "enhancement_updates_available", enhancement_updates_available)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_data_collection_authorized and not isinstance(is_data_collection_authorized, bool):
            raise TypeError("Expected argument 'is_data_collection_authorized' to be a bool")
        pulumi.set(__self__, "is_data_collection_authorized", is_data_collection_authorized)
        if is_reboot_required and not isinstance(is_reboot_required, bool):
            raise TypeError("Expected argument 'is_reboot_required' to be a bool")
        pulumi.set(__self__, "is_reboot_required", is_reboot_required)
        if ksplice_effective_kernel_version and not isinstance(ksplice_effective_kernel_version, str):
            raise TypeError("Expected argument 'ksplice_effective_kernel_version' to be a str")
        pulumi.set(__self__, "ksplice_effective_kernel_version", ksplice_effective_kernel_version)
        if last_boot and not isinstance(last_boot, str):
            raise TypeError("Expected argument 'last_boot' to be a str")
        pulumi.set(__self__, "last_boot", last_boot)
        if last_checkin and not isinstance(last_checkin, str):
            raise TypeError("Expected argument 'last_checkin' to be a str")
        pulumi.set(__self__, "last_checkin", last_checkin)
        if managed_instance_groups and not isinstance(managed_instance_groups, list):
            raise TypeError("Expected argument 'managed_instance_groups' to be a list")
        pulumi.set(__self__, "managed_instance_groups", managed_instance_groups)
        if managed_instance_id and not isinstance(managed_instance_id, str):
            raise TypeError("Expected argument 'managed_instance_id' to be a str")
        pulumi.set(__self__, "managed_instance_id", managed_instance_id)
        if notification_topic_id and not isinstance(notification_topic_id, str):
            raise TypeError("Expected argument 'notification_topic_id' to be a str")
        pulumi.set(__self__, "notification_topic_id", notification_topic_id)
        if os_family and not isinstance(os_family, str):
            raise TypeError("Expected argument 'os_family' to be a str")
        pulumi.set(__self__, "os_family", os_family)
        if os_kernel_version and not isinstance(os_kernel_version, str):
            raise TypeError("Expected argument 'os_kernel_version' to be a str")
        pulumi.set(__self__, "os_kernel_version", os_kernel_version)
        if os_name and not isinstance(os_name, str):
            raise TypeError("Expected argument 'os_name' to be a str")
        pulumi.set(__self__, "os_name", os_name)
        if os_version and not isinstance(os_version, str):
            raise TypeError("Expected argument 'os_version' to be a str")
        pulumi.set(__self__, "os_version", os_version)
        if other_updates_available and not isinstance(other_updates_available, int):
            raise TypeError("Expected argument 'other_updates_available' to be a int")
        pulumi.set(__self__, "other_updates_available", other_updates_available)
        if parent_software_sources and not isinstance(parent_software_sources, list):
            raise TypeError("Expected argument 'parent_software_sources' to be a list")
        pulumi.set(__self__, "parent_software_sources", parent_software_sources)
        if scheduled_job_count and not isinstance(scheduled_job_count, int):
            raise TypeError("Expected argument 'scheduled_job_count' to be a int")
        pulumi.set(__self__, "scheduled_job_count", scheduled_job_count)
        if security_updates_available and not isinstance(security_updates_available, int):
            raise TypeError("Expected argument 'security_updates_available' to be a int")
        pulumi.set(__self__, "security_updates_available", security_updates_available)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if updates_available and not isinstance(updates_available, int):
            raise TypeError("Expected argument 'updates_available' to be a int")
        pulumi.set(__self__, "updates_available", updates_available)
        if work_request_count and not isinstance(work_request_count, int):
            raise TypeError("Expected argument 'work_request_count' to be a int")
        pulumi.set(__self__, "work_request_count", work_request_count)

    @property
    @pulumi.getter
    def autonomouses(self) -> Sequence['outputs.GetManagedInstanceAutonomouseResult']:
        """
        if present, indicates the Managed Instance is an autonomous instance. Holds all the Autonomous specific information
        """
        return pulumi.get(self, "autonomouses")

    @property
    @pulumi.getter(name="bugUpdatesAvailable")
    def bug_updates_available(self) -> builtins.int:
        """
        Number of bug fix type updates available to be installed
        """
        return pulumi.get(self, "bug_updates_available")

    @property
    @pulumi.getter(name="childSoftwareSources")
    def child_software_sources(self) -> Sequence['outputs.GetManagedInstanceChildSoftwareSourceResult']:
        """
        list of child Software Sources attached to the Managed Instance
        """
        return pulumi.get(self, "child_software_sources")

    @property
    @pulumi.getter(name="compartmentId")
    def compartment_id(self) -> builtins.str:
        """
        OCID for the Compartment
        """
        return pulumi.get(self, "compartment_id")

    @property
    @pulumi.getter
    def description(self) -> builtins.str:
        """
        Information specified by the user about the managed instance
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> builtins.str:
        """
        User friendly name
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="enhancementUpdatesAvailable")
    def enhancement_updates_available(self) -> builtins.int:
        """
        Number of enhancement type updates available to be installed
        """
        return pulumi.get(self, "enhancement_updates_available")

    @property
    @pulumi.getter
    def id(self) -> builtins.str:
        """
        software source identifier
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isDataCollectionAuthorized")
    def is_data_collection_authorized(self) -> builtins.bool:
        """
        True if user allow data collection for this instance
        """
        return pulumi.get(self, "is_data_collection_authorized")

    @property
    @pulumi.getter(name="isRebootRequired")
    def is_reboot_required(self) -> builtins.bool:
        """
        Indicates whether a reboot is required to complete installation of updates.
        """
        return pulumi.get(self, "is_reboot_required")

    @property
    @pulumi.getter(name="kspliceEffectiveKernelVersion")
    def ksplice_effective_kernel_version(self) -> builtins.str:
        """
        The ksplice effective kernel version
        """
        return pulumi.get(self, "ksplice_effective_kernel_version")

    @property
    @pulumi.getter(name="lastBoot")
    def last_boot(self) -> builtins.str:
        """
        Time at which the instance last booted
        """
        return pulumi.get(self, "last_boot")

    @property
    @pulumi.getter(name="lastCheckin")
    def last_checkin(self) -> builtins.str:
        """
        Time at which the instance last checked in
        """
        return pulumi.get(self, "last_checkin")

    @property
    @pulumi.getter(name="managedInstanceGroups")
    def managed_instance_groups(self) -> Sequence['outputs.GetManagedInstanceManagedInstanceGroupResult']:
        """
        The ids of the managed instance groups of which this instance is a member.
        """
        return pulumi.get(self, "managed_instance_groups")

    @property
    @pulumi.getter(name="managedInstanceId")
    def managed_instance_id(self) -> builtins.str:
        return pulumi.get(self, "managed_instance_id")

    @property
    @pulumi.getter(name="notificationTopicId")
    def notification_topic_id(self) -> builtins.str:
        """
        OCID of the ONS topic used to send notification to users
        """
        return pulumi.get(self, "notification_topic_id")

    @property
    @pulumi.getter(name="osFamily")
    def os_family(self) -> builtins.str:
        """
        The Operating System type of the managed instance.
        """
        return pulumi.get(self, "os_family")

    @property
    @pulumi.getter(name="osKernelVersion")
    def os_kernel_version(self) -> builtins.str:
        """
        Operating System Kernel Version
        """
        return pulumi.get(self, "os_kernel_version")

    @property
    @pulumi.getter(name="osName")
    def os_name(self) -> builtins.str:
        """
        Operating System Name
        """
        return pulumi.get(self, "os_name")

    @property
    @pulumi.getter(name="osVersion")
    def os_version(self) -> builtins.str:
        """
        Operating System Version
        """
        return pulumi.get(self, "os_version")

    @property
    @pulumi.getter(name="otherUpdatesAvailable")
    def other_updates_available(self) -> builtins.int:
        """
        Number of non-classified updates available to be installed
        """
        return pulumi.get(self, "other_updates_available")

    @property
    @pulumi.getter(name="parentSoftwareSources")
    def parent_software_sources(self) -> Sequence['outputs.GetManagedInstanceParentSoftwareSourceResult']:
        """
        the parent (base) Software Source attached to the Managed Instance
        """
        return pulumi.get(self, "parent_software_sources")

    @property
    @pulumi.getter(name="scheduledJobCount")
    def scheduled_job_count(self) -> builtins.int:
        """
        Number of scheduled jobs associated with this instance
        """
        return pulumi.get(self, "scheduled_job_count")

    @property
    @pulumi.getter(name="securityUpdatesAvailable")
    def security_updates_available(self) -> builtins.int:
        """
        Number of security type updates available to be installed
        """
        return pulumi.get(self, "security_updates_available")

    @property
    @pulumi.getter
    def status(self) -> builtins.str:
        """
        status of the managed instance.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="updatesAvailable")
    def updates_available(self) -> builtins.int:
        """
        Number of updates available to be installed
        """
        return pulumi.get(self, "updates_available")

    @property
    @pulumi.getter(name="workRequestCount")
    def work_request_count(self) -> builtins.int:
        """
        Number of work requests associated with this instance
        """
        return pulumi.get(self, "work_request_count")


class AwaitableGetManagedInstanceResult(GetManagedInstanceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetManagedInstanceResult(
            autonomouses=self.autonomouses,
            bug_updates_available=self.bug_updates_available,
            child_software_sources=self.child_software_sources,
            compartment_id=self.compartment_id,
            description=self.description,
            display_name=self.display_name,
            enhancement_updates_available=self.enhancement_updates_available,
            id=self.id,
            is_data_collection_authorized=self.is_data_collection_authorized,
            is_reboot_required=self.is_reboot_required,
            ksplice_effective_kernel_version=self.ksplice_effective_kernel_version,
            last_boot=self.last_boot,
            last_checkin=self.last_checkin,
            managed_instance_groups=self.managed_instance_groups,
            managed_instance_id=self.managed_instance_id,
            notification_topic_id=self.notification_topic_id,
            os_family=self.os_family,
            os_kernel_version=self.os_kernel_version,
            os_name=self.os_name,
            os_version=self.os_version,
            other_updates_available=self.other_updates_available,
            parent_software_sources=self.parent_software_sources,
            scheduled_job_count=self.scheduled_job_count,
            security_updates_available=self.security_updates_available,
            status=self.status,
            updates_available=self.updates_available,
            work_request_count=self.work_request_count)


def get_managed_instance(managed_instance_id: Optional[builtins.str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetManagedInstanceResult:
    """
    This data source provides details about a specific Managed Instance resource in Oracle Cloud Infrastructure OS Management service.

    Returns a specific Managed Instance.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_managed_instance = oci.OsManagement.get_managed_instance(managed_instance_id=test_managed_instance_oci_osmanagement_managed_instance["id"])
    ```


    :param builtins.str managed_instance_id: OCID for the managed instance
    """
    __args__ = dict()
    __args__['managedInstanceId'] = managed_instance_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('oci:OsManagement/getManagedInstance:getManagedInstance', __args__, opts=opts, typ=GetManagedInstanceResult).value

    return AwaitableGetManagedInstanceResult(
        autonomouses=pulumi.get(__ret__, 'autonomouses'),
        bug_updates_available=pulumi.get(__ret__, 'bug_updates_available'),
        child_software_sources=pulumi.get(__ret__, 'child_software_sources'),
        compartment_id=pulumi.get(__ret__, 'compartment_id'),
        description=pulumi.get(__ret__, 'description'),
        display_name=pulumi.get(__ret__, 'display_name'),
        enhancement_updates_available=pulumi.get(__ret__, 'enhancement_updates_available'),
        id=pulumi.get(__ret__, 'id'),
        is_data_collection_authorized=pulumi.get(__ret__, 'is_data_collection_authorized'),
        is_reboot_required=pulumi.get(__ret__, 'is_reboot_required'),
        ksplice_effective_kernel_version=pulumi.get(__ret__, 'ksplice_effective_kernel_version'),
        last_boot=pulumi.get(__ret__, 'last_boot'),
        last_checkin=pulumi.get(__ret__, 'last_checkin'),
        managed_instance_groups=pulumi.get(__ret__, 'managed_instance_groups'),
        managed_instance_id=pulumi.get(__ret__, 'managed_instance_id'),
        notification_topic_id=pulumi.get(__ret__, 'notification_topic_id'),
        os_family=pulumi.get(__ret__, 'os_family'),
        os_kernel_version=pulumi.get(__ret__, 'os_kernel_version'),
        os_name=pulumi.get(__ret__, 'os_name'),
        os_version=pulumi.get(__ret__, 'os_version'),
        other_updates_available=pulumi.get(__ret__, 'other_updates_available'),
        parent_software_sources=pulumi.get(__ret__, 'parent_software_sources'),
        scheduled_job_count=pulumi.get(__ret__, 'scheduled_job_count'),
        security_updates_available=pulumi.get(__ret__, 'security_updates_available'),
        status=pulumi.get(__ret__, 'status'),
        updates_available=pulumi.get(__ret__, 'updates_available'),
        work_request_count=pulumi.get(__ret__, 'work_request_count'))
def get_managed_instance_output(managed_instance_id: Optional[pulumi.Input[builtins.str]] = None,
                                opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetManagedInstanceResult]:
    """
    This data source provides details about a specific Managed Instance resource in Oracle Cloud Infrastructure OS Management service.

    Returns a specific Managed Instance.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_managed_instance = oci.OsManagement.get_managed_instance(managed_instance_id=test_managed_instance_oci_osmanagement_managed_instance["id"])
    ```


    :param builtins.str managed_instance_id: OCID for the managed instance
    """
    __args__ = dict()
    __args__['managedInstanceId'] = managed_instance_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('oci:OsManagement/getManagedInstance:getManagedInstance', __args__, opts=opts, typ=GetManagedInstanceResult)
    return __ret__.apply(lambda __response__: GetManagedInstanceResult(
        autonomouses=pulumi.get(__response__, 'autonomouses'),
        bug_updates_available=pulumi.get(__response__, 'bug_updates_available'),
        child_software_sources=pulumi.get(__response__, 'child_software_sources'),
        compartment_id=pulumi.get(__response__, 'compartment_id'),
        description=pulumi.get(__response__, 'description'),
        display_name=pulumi.get(__response__, 'display_name'),
        enhancement_updates_available=pulumi.get(__response__, 'enhancement_updates_available'),
        id=pulumi.get(__response__, 'id'),
        is_data_collection_authorized=pulumi.get(__response__, 'is_data_collection_authorized'),
        is_reboot_required=pulumi.get(__response__, 'is_reboot_required'),
        ksplice_effective_kernel_version=pulumi.get(__response__, 'ksplice_effective_kernel_version'),
        last_boot=pulumi.get(__response__, 'last_boot'),
        last_checkin=pulumi.get(__response__, 'last_checkin'),
        managed_instance_groups=pulumi.get(__response__, 'managed_instance_groups'),
        managed_instance_id=pulumi.get(__response__, 'managed_instance_id'),
        notification_topic_id=pulumi.get(__response__, 'notification_topic_id'),
        os_family=pulumi.get(__response__, 'os_family'),
        os_kernel_version=pulumi.get(__response__, 'os_kernel_version'),
        os_name=pulumi.get(__response__, 'os_name'),
        os_version=pulumi.get(__response__, 'os_version'),
        other_updates_available=pulumi.get(__response__, 'other_updates_available'),
        parent_software_sources=pulumi.get(__response__, 'parent_software_sources'),
        scheduled_job_count=pulumi.get(__response__, 'scheduled_job_count'),
        security_updates_available=pulumi.get(__response__, 'security_updates_available'),
        status=pulumi.get(__response__, 'status'),
        updates_available=pulumi.get(__response__, 'updates_available'),
        work_request_count=pulumi.get(__response__, 'work_request_count')))
