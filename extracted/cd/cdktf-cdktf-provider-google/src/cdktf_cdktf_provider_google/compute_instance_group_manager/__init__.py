r'''
# `google_compute_instance_group_manager`

Refer to the Terraform Registry for docs: [`google_compute_instance_group_manager`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class ComputeInstanceGroupManager(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManager",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager google_compute_instance_group_manager}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        base_instance_name: builtins.str,
        name: builtins.str,
        version: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceGroupManagerVersion", typing.Dict[builtins.str, typing.Any]]]],
        all_instances_config: typing.Optional[typing.Union["ComputeInstanceGroupManagerAllInstancesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_healing_policies: typing.Optional[typing.Union["ComputeInstanceGroupManagerAutoHealingPolicies", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_lifecycle_policy: typing.Optional[typing.Union["ComputeInstanceGroupManagerInstanceLifecyclePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        list_managed_instances_results: typing.Optional[builtins.str] = None,
        named_port: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceGroupManagerNamedPort", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        resource_policies: typing.Optional[typing.Union["ComputeInstanceGroupManagerResourcePolicies", typing.Dict[builtins.str, typing.Any]]] = None,
        standby_policy: typing.Optional[typing.Union["ComputeInstanceGroupManagerStandbyPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        stateful_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceGroupManagerStatefulDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stateful_external_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceGroupManagerStatefulExternalIp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stateful_internal_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceGroupManagerStatefulInternalIp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_size: typing.Optional[jsii.Number] = None,
        target_stopped_size: typing.Optional[jsii.Number] = None,
        target_suspended_size: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["ComputeInstanceGroupManagerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        update_policy: typing.Optional[typing.Union["ComputeInstanceGroupManagerUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        wait_for_instances: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        wait_for_instances_status: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager google_compute_instance_group_manager} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param base_instance_name: The base instance name to use for instances in this group. The value must be a valid RFC1035 name. Supported characters are lowercase letters, numbers, and hyphens (-). Instances are named by appending a hyphen and a random four-character string to the base instance name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#base_instance_name ComputeInstanceGroupManager#base_instance_name}
        :param name: The name of the instance group manager. Must be 1-63 characters long and comply with RFC1035. Supported characters include lowercase letters, numbers, and hyphens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#name ComputeInstanceGroupManager#name}
        :param version: version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#version ComputeInstanceGroupManager#version}
        :param all_instances_config: all_instances_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#all_instances_config ComputeInstanceGroupManager#all_instances_config}
        :param auto_healing_policies: auto_healing_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#auto_healing_policies ComputeInstanceGroupManager#auto_healing_policies}
        :param description: An optional textual description of the instance group manager. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#description ComputeInstanceGroupManager#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#id ComputeInstanceGroupManager#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_lifecycle_policy: instance_lifecycle_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#instance_lifecycle_policy ComputeInstanceGroupManager#instance_lifecycle_policy}
        :param list_managed_instances_results: Pagination behavior of the listManagedInstances API method for this managed instance group. Valid values are: "PAGELESS", "PAGINATED". If PAGELESS (default), Pagination is disabled for the group's listManagedInstances API method. maxResults and pageToken query parameters are ignored and all instances are returned in a single response. If PAGINATED, pagination is enabled, maxResults and pageToken query parameters are respected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#list_managed_instances_results ComputeInstanceGroupManager#list_managed_instances_results}
        :param named_port: named_port block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#named_port ComputeInstanceGroupManager#named_port}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#project ComputeInstanceGroupManager#project}
        :param resource_policies: resource_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#resource_policies ComputeInstanceGroupManager#resource_policies}
        :param standby_policy: standby_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#standby_policy ComputeInstanceGroupManager#standby_policy}
        :param stateful_disk: stateful_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#stateful_disk ComputeInstanceGroupManager#stateful_disk}
        :param stateful_external_ip: stateful_external_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#stateful_external_ip ComputeInstanceGroupManager#stateful_external_ip}
        :param stateful_internal_ip: stateful_internal_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#stateful_internal_ip ComputeInstanceGroupManager#stateful_internal_ip}
        :param target_pools: The full URL of all target pools to which new instances in the group are added. Updating the target pools attribute does not affect existing instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#target_pools ComputeInstanceGroupManager#target_pools}
        :param target_size: The target number of running instances for this managed instance group. This value should always be explicitly set unless this resource is attached to an autoscaler, in which case it should never be set. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#target_size ComputeInstanceGroupManager#target_size}
        :param target_stopped_size: The target number of stopped instances for this managed instance group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#target_stopped_size ComputeInstanceGroupManager#target_stopped_size}
        :param target_suspended_size: The target number of suspended instances for this managed instance group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#target_suspended_size ComputeInstanceGroupManager#target_suspended_size}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#timeouts ComputeInstanceGroupManager#timeouts}
        :param update_policy: update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#update_policy ComputeInstanceGroupManager#update_policy}
        :param wait_for_instances: Whether to wait for all instances to be created/updated before returning. Note that if this is set to true and the operation does not succeed, Terraform will continue trying until it times out. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#wait_for_instances ComputeInstanceGroupManager#wait_for_instances}
        :param wait_for_instances_status: When used with wait_for_instances specifies the status to wait for. When STABLE is specified this resource will wait until the instances are stable before returning. When UPDATED is set, it will wait for the version target to be reached and any per instance configs to be effective and all instances configs to be effective as well as all instances to be stable before returning. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#wait_for_instances_status ComputeInstanceGroupManager#wait_for_instances_status}
        :param zone: The zone that instances in this group should be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#zone ComputeInstanceGroupManager#zone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__772c32b9ceeca4b4eea37f1955026786fcca83e4ecdc91a188a54fb1443ef1eb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeInstanceGroupManagerConfig(
            base_instance_name=base_instance_name,
            name=name,
            version=version,
            all_instances_config=all_instances_config,
            auto_healing_policies=auto_healing_policies,
            description=description,
            id=id,
            instance_lifecycle_policy=instance_lifecycle_policy,
            list_managed_instances_results=list_managed_instances_results,
            named_port=named_port,
            project=project,
            resource_policies=resource_policies,
            standby_policy=standby_policy,
            stateful_disk=stateful_disk,
            stateful_external_ip=stateful_external_ip,
            stateful_internal_ip=stateful_internal_ip,
            target_pools=target_pools,
            target_size=target_size,
            target_stopped_size=target_stopped_size,
            target_suspended_size=target_suspended_size,
            timeouts=timeouts,
            update_policy=update_policy,
            wait_for_instances=wait_for_instances,
            wait_for_instances_status=wait_for_instances_status,
            zone=zone,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a ComputeInstanceGroupManager resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeInstanceGroupManager to import.
        :param import_from_id: The id of the existing ComputeInstanceGroupManager that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeInstanceGroupManager to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e54287acce01c46eb9efc9607fc83f4042de3306f30581cc34334c46421a292f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAllInstancesConfig")
    def put_all_instances_config(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param labels: The label key-value pairs that you want to patch onto the instance,. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#labels ComputeInstanceGroupManager#labels}
        :param metadata: The metadata key-value pairs that you want to patch onto the instance. For more information, see Project and instance metadata, Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#metadata ComputeInstanceGroupManager#metadata}
        '''
        value = ComputeInstanceGroupManagerAllInstancesConfig(
            labels=labels, metadata=metadata
        )

        return typing.cast(None, jsii.invoke(self, "putAllInstancesConfig", [value]))

    @jsii.member(jsii_name="putAutoHealingPolicies")
    def put_auto_healing_policies(
        self,
        *,
        health_check: builtins.str,
        initial_delay_sec: jsii.Number,
    ) -> None:
        '''
        :param health_check: The health check resource that signals autohealing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#health_check ComputeInstanceGroupManager#health_check}
        :param initial_delay_sec: The number of seconds that the managed instance group waits before it applies autohealing policies to new instances or recently recreated instances. Between 0 and 3600. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#initial_delay_sec ComputeInstanceGroupManager#initial_delay_sec}
        '''
        value = ComputeInstanceGroupManagerAutoHealingPolicies(
            health_check=health_check, initial_delay_sec=initial_delay_sec
        )

        return typing.cast(None, jsii.invoke(self, "putAutoHealingPolicies", [value]))

    @jsii.member(jsii_name="putInstanceLifecyclePolicy")
    def put_instance_lifecycle_policy(
        self,
        *,
        default_action_on_failure: typing.Optional[builtins.str] = None,
        force_update_on_repair: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_action_on_failure: Default behavior for all instance or health check failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#default_action_on_failure ComputeInstanceGroupManager#default_action_on_failure}
        :param force_update_on_repair: Specifies whether to apply the group's latest configuration when repairing a VM. Valid options are: YES, NO. If YES and you updated the group's instance template or per-instance configurations after the VM was created, then these changes are applied when VM is repaired. If NO (default), then updates are applied in accordance with the group's update policy type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#force_update_on_repair ComputeInstanceGroupManager#force_update_on_repair}
        '''
        value = ComputeInstanceGroupManagerInstanceLifecyclePolicy(
            default_action_on_failure=default_action_on_failure,
            force_update_on_repair=force_update_on_repair,
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceLifecyclePolicy", [value]))

    @jsii.member(jsii_name="putNamedPort")
    def put_named_port(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceGroupManagerNamedPort", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6650ed2126446542e53fbc03b4a4e209b61586a8d7b3e62a4cbec7eeb501d67d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNamedPort", [value]))

    @jsii.member(jsii_name="putResourcePolicies")
    def put_resource_policies(
        self,
        *,
        workload_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param workload_policy: The URL of the workload policy that is specified for this managed instance group. It can be a full or partial URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#workload_policy ComputeInstanceGroupManager#workload_policy}
        '''
        value = ComputeInstanceGroupManagerResourcePolicies(
            workload_policy=workload_policy
        )

        return typing.cast(None, jsii.invoke(self, "putResourcePolicies", [value]))

    @jsii.member(jsii_name="putStandbyPolicy")
    def put_standby_policy(
        self,
        *,
        initial_delay_sec: typing.Optional[jsii.Number] = None,
        mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param initial_delay_sec: Specifies the number of seconds that the MIG should wait to suspend or stop a VM after that VM was created. The initial delay gives the initialization script the time to prepare your VM for a quick scale out. The value of initial delay must be between 0 and 3600 seconds. The default value is 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#initial_delay_sec ComputeInstanceGroupManager#initial_delay_sec}
        :param mode: Defines how a MIG resumes or starts VMs from a standby pool when the group scales out. The default mode is "MANUAL". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#mode ComputeInstanceGroupManager#mode}
        '''
        value = ComputeInstanceGroupManagerStandbyPolicy(
            initial_delay_sec=initial_delay_sec, mode=mode
        )

        return typing.cast(None, jsii.invoke(self, "putStandbyPolicy", [value]))

    @jsii.member(jsii_name="putStatefulDisk")
    def put_stateful_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceGroupManagerStatefulDisk", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0d7be4cfa175de94e74862222ce3274f535b3ad1499891f6a62e10bb994e95f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStatefulDisk", [value]))

    @jsii.member(jsii_name="putStatefulExternalIp")
    def put_stateful_external_ip(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceGroupManagerStatefulExternalIp", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a96df8c5001a94ae94ec24a20230685961a3d2cedc56222e8e2eb0bc4649a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStatefulExternalIp", [value]))

    @jsii.member(jsii_name="putStatefulInternalIp")
    def put_stateful_internal_ip(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceGroupManagerStatefulInternalIp", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__090673e01cbcf46be7e8bd5453bfaa0bdab0d047d239fdc32023808bee4bb3c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStatefulInternalIp", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#create ComputeInstanceGroupManager#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#delete ComputeInstanceGroupManager#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#update ComputeInstanceGroupManager#update}.
        '''
        value = ComputeInstanceGroupManagerTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUpdatePolicy")
    def put_update_policy(
        self,
        *,
        minimal_action: builtins.str,
        type: builtins.str,
        max_surge_fixed: typing.Optional[jsii.Number] = None,
        max_surge_percent: typing.Optional[jsii.Number] = None,
        max_unavailable_fixed: typing.Optional[jsii.Number] = None,
        max_unavailable_percent: typing.Optional[jsii.Number] = None,
        most_disruptive_allowed_action: typing.Optional[builtins.str] = None,
        replacement_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param minimal_action: Minimal action to be taken on an instance. You can specify either NONE to forbid any actions, REFRESH to update without stopping instances, RESTART to restart existing instances or REPLACE to delete and create new instances from the target template. If you specify a REFRESH, the Updater will attempt to perform that action only. However, if the Updater determines that the minimal action you specify is not enough to perform the update, it might perform a more disruptive action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#minimal_action ComputeInstanceGroupManager#minimal_action}
        :param type: The type of update process. You can specify either PROACTIVE so that the instance group manager proactively executes actions in order to bring instances to their target versions or OPPORTUNISTIC so that no action is proactively executed but the update will be performed as part of other actions (for example, resizes or recreateInstances calls). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#type ComputeInstanceGroupManager#type}
        :param max_surge_fixed: Specifies a fixed number of VM instances. This must be a positive integer. Conflicts with max_surge_percent. Both cannot be 0 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#max_surge_fixed ComputeInstanceGroupManager#max_surge_fixed}
        :param max_surge_percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Conflicts with max_surge_fixed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#max_surge_percent ComputeInstanceGroupManager#max_surge_percent}
        :param max_unavailable_fixed: Specifies a fixed number of VM instances. This must be a positive integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#max_unavailable_fixed ComputeInstanceGroupManager#max_unavailable_fixed}
        :param max_unavailable_percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#max_unavailable_percent ComputeInstanceGroupManager#max_unavailable_percent}
        :param most_disruptive_allowed_action: Most disruptive action that is allowed to be taken on an instance. You can specify either NONE to forbid any actions, REFRESH to allow actions that do not need instance restart, RESTART to allow actions that can be applied without instance replacing or REPLACE to allow all possible actions. If the Updater determines that the minimal update action needed is more disruptive than most disruptive allowed action you specify it will not perform the update at all. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#most_disruptive_allowed_action ComputeInstanceGroupManager#most_disruptive_allowed_action}
        :param replacement_method: The instance replacement method for managed instance groups. Valid values are: "RECREATE", "SUBSTITUTE". If SUBSTITUTE (default), the group replaces VM instances with new instances that have randomly generated names. If RECREATE, instance names are preserved. You must also set max_unavailable_fixed or max_unavailable_percent to be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#replacement_method ComputeInstanceGroupManager#replacement_method}
        '''
        value = ComputeInstanceGroupManagerUpdatePolicy(
            minimal_action=minimal_action,
            type=type,
            max_surge_fixed=max_surge_fixed,
            max_surge_percent=max_surge_percent,
            max_unavailable_fixed=max_unavailable_fixed,
            max_unavailable_percent=max_unavailable_percent,
            most_disruptive_allowed_action=most_disruptive_allowed_action,
            replacement_method=replacement_method,
        )

        return typing.cast(None, jsii.invoke(self, "putUpdatePolicy", [value]))

    @jsii.member(jsii_name="putVersion")
    def put_version(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceGroupManagerVersion", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__193b061bbe53a8a2861a916d8dacbc2e96f198c5d7654d9ab1c808473cb7e34f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVersion", [value]))

    @jsii.member(jsii_name="resetAllInstancesConfig")
    def reset_all_instances_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllInstancesConfig", []))

    @jsii.member(jsii_name="resetAutoHealingPolicies")
    def reset_auto_healing_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoHealingPolicies", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstanceLifecyclePolicy")
    def reset_instance_lifecycle_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceLifecyclePolicy", []))

    @jsii.member(jsii_name="resetListManagedInstancesResults")
    def reset_list_managed_instances_results(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetListManagedInstancesResults", []))

    @jsii.member(jsii_name="resetNamedPort")
    def reset_named_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamedPort", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetResourcePolicies")
    def reset_resource_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourcePolicies", []))

    @jsii.member(jsii_name="resetStandbyPolicy")
    def reset_standby_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStandbyPolicy", []))

    @jsii.member(jsii_name="resetStatefulDisk")
    def reset_stateful_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatefulDisk", []))

    @jsii.member(jsii_name="resetStatefulExternalIp")
    def reset_stateful_external_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatefulExternalIp", []))

    @jsii.member(jsii_name="resetStatefulInternalIp")
    def reset_stateful_internal_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatefulInternalIp", []))

    @jsii.member(jsii_name="resetTargetPools")
    def reset_target_pools(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetPools", []))

    @jsii.member(jsii_name="resetTargetSize")
    def reset_target_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetSize", []))

    @jsii.member(jsii_name="resetTargetStoppedSize")
    def reset_target_stopped_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetStoppedSize", []))

    @jsii.member(jsii_name="resetTargetSuspendedSize")
    def reset_target_suspended_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetSuspendedSize", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUpdatePolicy")
    def reset_update_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdatePolicy", []))

    @jsii.member(jsii_name="resetWaitForInstances")
    def reset_wait_for_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWaitForInstances", []))

    @jsii.member(jsii_name="resetWaitForInstancesStatus")
    def reset_wait_for_instances_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWaitForInstancesStatus", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="allInstancesConfig")
    def all_instances_config(
        self,
    ) -> "ComputeInstanceGroupManagerAllInstancesConfigOutputReference":
        return typing.cast("ComputeInstanceGroupManagerAllInstancesConfigOutputReference", jsii.get(self, "allInstancesConfig"))

    @builtins.property
    @jsii.member(jsii_name="autoHealingPolicies")
    def auto_healing_policies(
        self,
    ) -> "ComputeInstanceGroupManagerAutoHealingPoliciesOutputReference":
        return typing.cast("ComputeInstanceGroupManagerAutoHealingPoliciesOutputReference", jsii.get(self, "autoHealingPolicies"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="fingerprint")
    def fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fingerprint"))

    @builtins.property
    @jsii.member(jsii_name="instanceGroup")
    def instance_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceGroup"))

    @builtins.property
    @jsii.member(jsii_name="instanceGroupManagerId")
    def instance_group_manager_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "instanceGroupManagerId"))

    @builtins.property
    @jsii.member(jsii_name="instanceLifecyclePolicy")
    def instance_lifecycle_policy(
        self,
    ) -> "ComputeInstanceGroupManagerInstanceLifecyclePolicyOutputReference":
        return typing.cast("ComputeInstanceGroupManagerInstanceLifecyclePolicyOutputReference", jsii.get(self, "instanceLifecyclePolicy"))

    @builtins.property
    @jsii.member(jsii_name="namedPort")
    def named_port(self) -> "ComputeInstanceGroupManagerNamedPortList":
        return typing.cast("ComputeInstanceGroupManagerNamedPortList", jsii.get(self, "namedPort"))

    @builtins.property
    @jsii.member(jsii_name="operation")
    def operation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operation"))

    @builtins.property
    @jsii.member(jsii_name="resourcePolicies")
    def resource_policies(
        self,
    ) -> "ComputeInstanceGroupManagerResourcePoliciesOutputReference":
        return typing.cast("ComputeInstanceGroupManagerResourcePoliciesOutputReference", jsii.get(self, "resourcePolicies"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="standbyPolicy")
    def standby_policy(
        self,
    ) -> "ComputeInstanceGroupManagerStandbyPolicyOutputReference":
        return typing.cast("ComputeInstanceGroupManagerStandbyPolicyOutputReference", jsii.get(self, "standbyPolicy"))

    @builtins.property
    @jsii.member(jsii_name="statefulDisk")
    def stateful_disk(self) -> "ComputeInstanceGroupManagerStatefulDiskList":
        return typing.cast("ComputeInstanceGroupManagerStatefulDiskList", jsii.get(self, "statefulDisk"))

    @builtins.property
    @jsii.member(jsii_name="statefulExternalIp")
    def stateful_external_ip(
        self,
    ) -> "ComputeInstanceGroupManagerStatefulExternalIpList":
        return typing.cast("ComputeInstanceGroupManagerStatefulExternalIpList", jsii.get(self, "statefulExternalIp"))

    @builtins.property
    @jsii.member(jsii_name="statefulInternalIp")
    def stateful_internal_ip(
        self,
    ) -> "ComputeInstanceGroupManagerStatefulInternalIpList":
        return typing.cast("ComputeInstanceGroupManagerStatefulInternalIpList", jsii.get(self, "statefulInternalIp"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "ComputeInstanceGroupManagerStatusList":
        return typing.cast("ComputeInstanceGroupManagerStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeInstanceGroupManagerTimeoutsOutputReference":
        return typing.cast("ComputeInstanceGroupManagerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updatePolicy")
    def update_policy(self) -> "ComputeInstanceGroupManagerUpdatePolicyOutputReference":
        return typing.cast("ComputeInstanceGroupManagerUpdatePolicyOutputReference", jsii.get(self, "updatePolicy"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> "ComputeInstanceGroupManagerVersionList":
        return typing.cast("ComputeInstanceGroupManagerVersionList", jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="allInstancesConfigInput")
    def all_instances_config_input(
        self,
    ) -> typing.Optional["ComputeInstanceGroupManagerAllInstancesConfig"]:
        return typing.cast(typing.Optional["ComputeInstanceGroupManagerAllInstancesConfig"], jsii.get(self, "allInstancesConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="autoHealingPoliciesInput")
    def auto_healing_policies_input(
        self,
    ) -> typing.Optional["ComputeInstanceGroupManagerAutoHealingPolicies"]:
        return typing.cast(typing.Optional["ComputeInstanceGroupManagerAutoHealingPolicies"], jsii.get(self, "autoHealingPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="baseInstanceNameInput")
    def base_instance_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseInstanceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceLifecyclePolicyInput")
    def instance_lifecycle_policy_input(
        self,
    ) -> typing.Optional["ComputeInstanceGroupManagerInstanceLifecyclePolicy"]:
        return typing.cast(typing.Optional["ComputeInstanceGroupManagerInstanceLifecyclePolicy"], jsii.get(self, "instanceLifecyclePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="listManagedInstancesResultsInput")
    def list_managed_instances_results_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "listManagedInstancesResultsInput"))

    @builtins.property
    @jsii.member(jsii_name="namedPortInput")
    def named_port_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGroupManagerNamedPort"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGroupManagerNamedPort"]]], jsii.get(self, "namedPortInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcePoliciesInput")
    def resource_policies_input(
        self,
    ) -> typing.Optional["ComputeInstanceGroupManagerResourcePolicies"]:
        return typing.cast(typing.Optional["ComputeInstanceGroupManagerResourcePolicies"], jsii.get(self, "resourcePoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="standbyPolicyInput")
    def standby_policy_input(
        self,
    ) -> typing.Optional["ComputeInstanceGroupManagerStandbyPolicy"]:
        return typing.cast(typing.Optional["ComputeInstanceGroupManagerStandbyPolicy"], jsii.get(self, "standbyPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="statefulDiskInput")
    def stateful_disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGroupManagerStatefulDisk"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGroupManagerStatefulDisk"]]], jsii.get(self, "statefulDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="statefulExternalIpInput")
    def stateful_external_ip_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGroupManagerStatefulExternalIp"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGroupManagerStatefulExternalIp"]]], jsii.get(self, "statefulExternalIpInput"))

    @builtins.property
    @jsii.member(jsii_name="statefulInternalIpInput")
    def stateful_internal_ip_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGroupManagerStatefulInternalIp"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGroupManagerStatefulInternalIp"]]], jsii.get(self, "statefulInternalIpInput"))

    @builtins.property
    @jsii.member(jsii_name="targetPoolsInput")
    def target_pools_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "targetPoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="targetSizeInput")
    def target_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="targetStoppedSizeInput")
    def target_stopped_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetStoppedSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="targetSuspendedSizeInput")
    def target_suspended_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetSuspendedSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeInstanceGroupManagerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeInstanceGroupManagerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="updatePolicyInput")
    def update_policy_input(
        self,
    ) -> typing.Optional["ComputeInstanceGroupManagerUpdatePolicy"]:
        return typing.cast(typing.Optional["ComputeInstanceGroupManagerUpdatePolicy"], jsii.get(self, "updatePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGroupManagerVersion"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGroupManagerVersion"]]], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="waitForInstancesInput")
    def wait_for_instances_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "waitForInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="waitForInstancesStatusInput")
    def wait_for_instances_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "waitForInstancesStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="baseInstanceName")
    def base_instance_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseInstanceName"))

    @base_instance_name.setter
    def base_instance_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed2b3370590287b6c9d4614925d660eb3316645c2d3e48dd83f0598866bcdd6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseInstanceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0d4a7edc856e765a0056799102feba9a9250624b66dc77a2a0421f4e57a0003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24916ad8659be425914a7056c7db3843d732a073e9d9978e33000c4dc84db38d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="listManagedInstancesResults")
    def list_managed_instances_results(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "listManagedInstancesResults"))

    @list_managed_instances_results.setter
    def list_managed_instances_results(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49e43270dbe8b0775817768489d565b660de29dca1bf10ac932f5e49c5a8ab36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listManagedInstancesResults", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8afd310ce48f9d4272cbd2e66f6e8176e5d35b5f57c46665139ccd39cf978a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36f8177167dd22487d1e5633057061e64e8fb1217b73353dd36c6b70ea6ffa0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetPools")
    def target_pools(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetPools"))

    @target_pools.setter
    def target_pools(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48074ac0ccb45878e52481263daae1164d5b04e9bcabf120664b879a83373ede)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetPools", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetSize")
    def target_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetSize"))

    @target_size.setter
    def target_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e32a1e0d673cc427b3ecdfdddbed361850038aa1172d14b62e50b9973843ba5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetStoppedSize")
    def target_stopped_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetStoppedSize"))

    @target_stopped_size.setter
    def target_stopped_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dff6bc65034cb05b5f46446267828519cbc66a1bd73d8141592e9fd8d5b2c5f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetStoppedSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetSuspendedSize")
    def target_suspended_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetSuspendedSize"))

    @target_suspended_size.setter
    def target_suspended_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6fecfce22102d6dad5189d8de71cc9f5822fac20a30200b9be790f56fa1290a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetSuspendedSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="waitForInstances")
    def wait_for_instances(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "waitForInstances"))

    @wait_for_instances.setter
    def wait_for_instances(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5829fff854f97989e254fc66fe173a55b865e2bb9e714726d3b161c4f85dd80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="waitForInstancesStatus")
    def wait_for_instances_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "waitForInstancesStatus"))

    @wait_for_instances_status.setter
    def wait_for_instances_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebe0fe2046ebbc4dc283c54ce36b7855dfcbf237483bf35c31e150c7b6215295)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForInstancesStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69672ce2a451d8ef6f46b1fdf97dafc981010d07cc0de31d7f6c8324e4e9fbd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerAllInstancesConfig",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels", "metadata": "metadata"},
)
class ComputeInstanceGroupManagerAllInstancesConfig:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param labels: The label key-value pairs that you want to patch onto the instance,. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#labels ComputeInstanceGroupManager#labels}
        :param metadata: The metadata key-value pairs that you want to patch onto the instance. For more information, see Project and instance metadata, Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#metadata ComputeInstanceGroupManager#metadata}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__376665c84a5d3564feebecba8e2e59586c3f6e063305aa465889000ad92333c4)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The label key-value pairs that you want to patch onto the instance,.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#labels ComputeInstanceGroupManager#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The metadata key-value pairs that you want to patch onto the instance.

        For more information, see Project and instance metadata,

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#metadata ComputeInstanceGroupManager#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceGroupManagerAllInstancesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceGroupManagerAllInstancesConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerAllInstancesConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cb8a5364d520196ad235eb2e219b6d94086d42b933a470ede497669d1576796)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ba97c575b1f06f4b8d018a8a64ff4c5d0a20b2a5016259672917532d717e143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b00a097d661fbd40a723e8b1e17be677eca90fdcb8e3b5616ff302da07429f72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceGroupManagerAllInstancesConfig]:
        return typing.cast(typing.Optional[ComputeInstanceGroupManagerAllInstancesConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceGroupManagerAllInstancesConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__075bf7d407cbd8a9a68a3599f8e120dcaefcecc9ae2d54ebd68f2525ce50e160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerAutoHealingPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "health_check": "healthCheck",
        "initial_delay_sec": "initialDelaySec",
    },
)
class ComputeInstanceGroupManagerAutoHealingPolicies:
    def __init__(
        self,
        *,
        health_check: builtins.str,
        initial_delay_sec: jsii.Number,
    ) -> None:
        '''
        :param health_check: The health check resource that signals autohealing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#health_check ComputeInstanceGroupManager#health_check}
        :param initial_delay_sec: The number of seconds that the managed instance group waits before it applies autohealing policies to new instances or recently recreated instances. Between 0 and 3600. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#initial_delay_sec ComputeInstanceGroupManager#initial_delay_sec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae8542be76f1905a1cf07039be2eebb468970181c3f347d8b4524f3b3cc0e5cb)
            check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
            check_type(argname="argument initial_delay_sec", value=initial_delay_sec, expected_type=type_hints["initial_delay_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "health_check": health_check,
            "initial_delay_sec": initial_delay_sec,
        }

    @builtins.property
    def health_check(self) -> builtins.str:
        '''The health check resource that signals autohealing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#health_check ComputeInstanceGroupManager#health_check}
        '''
        result = self._values.get("health_check")
        assert result is not None, "Required property 'health_check' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def initial_delay_sec(self) -> jsii.Number:
        '''The number of seconds that the managed instance group waits before it applies autohealing policies to new instances or recently recreated instances.

        Between 0 and 3600.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#initial_delay_sec ComputeInstanceGroupManager#initial_delay_sec}
        '''
        result = self._values.get("initial_delay_sec")
        assert result is not None, "Required property 'initial_delay_sec' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceGroupManagerAutoHealingPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceGroupManagerAutoHealingPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerAutoHealingPoliciesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d31175be4915add26970157e153e2716899fecca3110af06e7e5d209cb3b0a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="healthCheckInput")
    def health_check_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="initialDelaySecInput")
    def initial_delay_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialDelaySecInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheck")
    def health_check(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthCheck"))

    @health_check.setter
    def health_check(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b120901647b1e7534c4431a9e82cdedb6709b0a95ad144fc11466d88f0b0a3bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelaySec")
    def initial_delay_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelaySec"))

    @initial_delay_sec.setter
    def initial_delay_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c991a1e1ef9863bfa9bebcb7f79c4f15fe61fd41d31ff958f10029c52dca986e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelaySec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceGroupManagerAutoHealingPolicies]:
        return typing.cast(typing.Optional[ComputeInstanceGroupManagerAutoHealingPolicies], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceGroupManagerAutoHealingPolicies],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7f8565b0e09599e8c01132bfaff6e931e3ad260c0c79e12f12882cfeba5207e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "base_instance_name": "baseInstanceName",
        "name": "name",
        "version": "version",
        "all_instances_config": "allInstancesConfig",
        "auto_healing_policies": "autoHealingPolicies",
        "description": "description",
        "id": "id",
        "instance_lifecycle_policy": "instanceLifecyclePolicy",
        "list_managed_instances_results": "listManagedInstancesResults",
        "named_port": "namedPort",
        "project": "project",
        "resource_policies": "resourcePolicies",
        "standby_policy": "standbyPolicy",
        "stateful_disk": "statefulDisk",
        "stateful_external_ip": "statefulExternalIp",
        "stateful_internal_ip": "statefulInternalIp",
        "target_pools": "targetPools",
        "target_size": "targetSize",
        "target_stopped_size": "targetStoppedSize",
        "target_suspended_size": "targetSuspendedSize",
        "timeouts": "timeouts",
        "update_policy": "updatePolicy",
        "wait_for_instances": "waitForInstances",
        "wait_for_instances_status": "waitForInstancesStatus",
        "zone": "zone",
    },
)
class ComputeInstanceGroupManagerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        base_instance_name: builtins.str,
        name: builtins.str,
        version: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceGroupManagerVersion", typing.Dict[builtins.str, typing.Any]]]],
        all_instances_config: typing.Optional[typing.Union[ComputeInstanceGroupManagerAllInstancesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_healing_policies: typing.Optional[typing.Union[ComputeInstanceGroupManagerAutoHealingPolicies, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_lifecycle_policy: typing.Optional[typing.Union["ComputeInstanceGroupManagerInstanceLifecyclePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        list_managed_instances_results: typing.Optional[builtins.str] = None,
        named_port: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceGroupManagerNamedPort", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        resource_policies: typing.Optional[typing.Union["ComputeInstanceGroupManagerResourcePolicies", typing.Dict[builtins.str, typing.Any]]] = None,
        standby_policy: typing.Optional[typing.Union["ComputeInstanceGroupManagerStandbyPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        stateful_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceGroupManagerStatefulDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stateful_external_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceGroupManagerStatefulExternalIp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stateful_internal_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceGroupManagerStatefulInternalIp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_size: typing.Optional[jsii.Number] = None,
        target_stopped_size: typing.Optional[jsii.Number] = None,
        target_suspended_size: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["ComputeInstanceGroupManagerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        update_policy: typing.Optional[typing.Union["ComputeInstanceGroupManagerUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        wait_for_instances: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        wait_for_instances_status: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param base_instance_name: The base instance name to use for instances in this group. The value must be a valid RFC1035 name. Supported characters are lowercase letters, numbers, and hyphens (-). Instances are named by appending a hyphen and a random four-character string to the base instance name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#base_instance_name ComputeInstanceGroupManager#base_instance_name}
        :param name: The name of the instance group manager. Must be 1-63 characters long and comply with RFC1035. Supported characters include lowercase letters, numbers, and hyphens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#name ComputeInstanceGroupManager#name}
        :param version: version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#version ComputeInstanceGroupManager#version}
        :param all_instances_config: all_instances_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#all_instances_config ComputeInstanceGroupManager#all_instances_config}
        :param auto_healing_policies: auto_healing_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#auto_healing_policies ComputeInstanceGroupManager#auto_healing_policies}
        :param description: An optional textual description of the instance group manager. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#description ComputeInstanceGroupManager#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#id ComputeInstanceGroupManager#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_lifecycle_policy: instance_lifecycle_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#instance_lifecycle_policy ComputeInstanceGroupManager#instance_lifecycle_policy}
        :param list_managed_instances_results: Pagination behavior of the listManagedInstances API method for this managed instance group. Valid values are: "PAGELESS", "PAGINATED". If PAGELESS (default), Pagination is disabled for the group's listManagedInstances API method. maxResults and pageToken query parameters are ignored and all instances are returned in a single response. If PAGINATED, pagination is enabled, maxResults and pageToken query parameters are respected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#list_managed_instances_results ComputeInstanceGroupManager#list_managed_instances_results}
        :param named_port: named_port block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#named_port ComputeInstanceGroupManager#named_port}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#project ComputeInstanceGroupManager#project}
        :param resource_policies: resource_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#resource_policies ComputeInstanceGroupManager#resource_policies}
        :param standby_policy: standby_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#standby_policy ComputeInstanceGroupManager#standby_policy}
        :param stateful_disk: stateful_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#stateful_disk ComputeInstanceGroupManager#stateful_disk}
        :param stateful_external_ip: stateful_external_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#stateful_external_ip ComputeInstanceGroupManager#stateful_external_ip}
        :param stateful_internal_ip: stateful_internal_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#stateful_internal_ip ComputeInstanceGroupManager#stateful_internal_ip}
        :param target_pools: The full URL of all target pools to which new instances in the group are added. Updating the target pools attribute does not affect existing instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#target_pools ComputeInstanceGroupManager#target_pools}
        :param target_size: The target number of running instances for this managed instance group. This value should always be explicitly set unless this resource is attached to an autoscaler, in which case it should never be set. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#target_size ComputeInstanceGroupManager#target_size}
        :param target_stopped_size: The target number of stopped instances for this managed instance group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#target_stopped_size ComputeInstanceGroupManager#target_stopped_size}
        :param target_suspended_size: The target number of suspended instances for this managed instance group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#target_suspended_size ComputeInstanceGroupManager#target_suspended_size}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#timeouts ComputeInstanceGroupManager#timeouts}
        :param update_policy: update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#update_policy ComputeInstanceGroupManager#update_policy}
        :param wait_for_instances: Whether to wait for all instances to be created/updated before returning. Note that if this is set to true and the operation does not succeed, Terraform will continue trying until it times out. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#wait_for_instances ComputeInstanceGroupManager#wait_for_instances}
        :param wait_for_instances_status: When used with wait_for_instances specifies the status to wait for. When STABLE is specified this resource will wait until the instances are stable before returning. When UPDATED is set, it will wait for the version target to be reached and any per instance configs to be effective and all instances configs to be effective as well as all instances to be stable before returning. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#wait_for_instances_status ComputeInstanceGroupManager#wait_for_instances_status}
        :param zone: The zone that instances in this group should be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#zone ComputeInstanceGroupManager#zone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(all_instances_config, dict):
            all_instances_config = ComputeInstanceGroupManagerAllInstancesConfig(**all_instances_config)
        if isinstance(auto_healing_policies, dict):
            auto_healing_policies = ComputeInstanceGroupManagerAutoHealingPolicies(**auto_healing_policies)
        if isinstance(instance_lifecycle_policy, dict):
            instance_lifecycle_policy = ComputeInstanceGroupManagerInstanceLifecyclePolicy(**instance_lifecycle_policy)
        if isinstance(resource_policies, dict):
            resource_policies = ComputeInstanceGroupManagerResourcePolicies(**resource_policies)
        if isinstance(standby_policy, dict):
            standby_policy = ComputeInstanceGroupManagerStandbyPolicy(**standby_policy)
        if isinstance(timeouts, dict):
            timeouts = ComputeInstanceGroupManagerTimeouts(**timeouts)
        if isinstance(update_policy, dict):
            update_policy = ComputeInstanceGroupManagerUpdatePolicy(**update_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1241493119c67face4d74f44b7e398f60b4c2e441ceae192ea1b5583e568f9af)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument base_instance_name", value=base_instance_name, expected_type=type_hints["base_instance_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument all_instances_config", value=all_instances_config, expected_type=type_hints["all_instances_config"])
            check_type(argname="argument auto_healing_policies", value=auto_healing_policies, expected_type=type_hints["auto_healing_policies"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_lifecycle_policy", value=instance_lifecycle_policy, expected_type=type_hints["instance_lifecycle_policy"])
            check_type(argname="argument list_managed_instances_results", value=list_managed_instances_results, expected_type=type_hints["list_managed_instances_results"])
            check_type(argname="argument named_port", value=named_port, expected_type=type_hints["named_port"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument resource_policies", value=resource_policies, expected_type=type_hints["resource_policies"])
            check_type(argname="argument standby_policy", value=standby_policy, expected_type=type_hints["standby_policy"])
            check_type(argname="argument stateful_disk", value=stateful_disk, expected_type=type_hints["stateful_disk"])
            check_type(argname="argument stateful_external_ip", value=stateful_external_ip, expected_type=type_hints["stateful_external_ip"])
            check_type(argname="argument stateful_internal_ip", value=stateful_internal_ip, expected_type=type_hints["stateful_internal_ip"])
            check_type(argname="argument target_pools", value=target_pools, expected_type=type_hints["target_pools"])
            check_type(argname="argument target_size", value=target_size, expected_type=type_hints["target_size"])
            check_type(argname="argument target_stopped_size", value=target_stopped_size, expected_type=type_hints["target_stopped_size"])
            check_type(argname="argument target_suspended_size", value=target_suspended_size, expected_type=type_hints["target_suspended_size"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument update_policy", value=update_policy, expected_type=type_hints["update_policy"])
            check_type(argname="argument wait_for_instances", value=wait_for_instances, expected_type=type_hints["wait_for_instances"])
            check_type(argname="argument wait_for_instances_status", value=wait_for_instances_status, expected_type=type_hints["wait_for_instances_status"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "base_instance_name": base_instance_name,
            "name": name,
            "version": version,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if all_instances_config is not None:
            self._values["all_instances_config"] = all_instances_config
        if auto_healing_policies is not None:
            self._values["auto_healing_policies"] = auto_healing_policies
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if instance_lifecycle_policy is not None:
            self._values["instance_lifecycle_policy"] = instance_lifecycle_policy
        if list_managed_instances_results is not None:
            self._values["list_managed_instances_results"] = list_managed_instances_results
        if named_port is not None:
            self._values["named_port"] = named_port
        if project is not None:
            self._values["project"] = project
        if resource_policies is not None:
            self._values["resource_policies"] = resource_policies
        if standby_policy is not None:
            self._values["standby_policy"] = standby_policy
        if stateful_disk is not None:
            self._values["stateful_disk"] = stateful_disk
        if stateful_external_ip is not None:
            self._values["stateful_external_ip"] = stateful_external_ip
        if stateful_internal_ip is not None:
            self._values["stateful_internal_ip"] = stateful_internal_ip
        if target_pools is not None:
            self._values["target_pools"] = target_pools
        if target_size is not None:
            self._values["target_size"] = target_size
        if target_stopped_size is not None:
            self._values["target_stopped_size"] = target_stopped_size
        if target_suspended_size is not None:
            self._values["target_suspended_size"] = target_suspended_size
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if update_policy is not None:
            self._values["update_policy"] = update_policy
        if wait_for_instances is not None:
            self._values["wait_for_instances"] = wait_for_instances
        if wait_for_instances_status is not None:
            self._values["wait_for_instances_status"] = wait_for_instances_status
        if zone is not None:
            self._values["zone"] = zone

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def base_instance_name(self) -> builtins.str:
        '''The base instance name to use for instances in this group.

        The value must be a valid RFC1035 name. Supported characters are lowercase letters, numbers, and hyphens (-). Instances are named by appending a hyphen and a random four-character string to the base instance name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#base_instance_name ComputeInstanceGroupManager#base_instance_name}
        '''
        result = self._values.get("base_instance_name")
        assert result is not None, "Required property 'base_instance_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the instance group manager.

        Must be 1-63 characters long and comply with RFC1035. Supported characters include lowercase letters, numbers, and hyphens.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#name ComputeInstanceGroupManager#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGroupManagerVersion"]]:
        '''version block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#version ComputeInstanceGroupManager#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGroupManagerVersion"]], result)

    @builtins.property
    def all_instances_config(
        self,
    ) -> typing.Optional[ComputeInstanceGroupManagerAllInstancesConfig]:
        '''all_instances_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#all_instances_config ComputeInstanceGroupManager#all_instances_config}
        '''
        result = self._values.get("all_instances_config")
        return typing.cast(typing.Optional[ComputeInstanceGroupManagerAllInstancesConfig], result)

    @builtins.property
    def auto_healing_policies(
        self,
    ) -> typing.Optional[ComputeInstanceGroupManagerAutoHealingPolicies]:
        '''auto_healing_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#auto_healing_policies ComputeInstanceGroupManager#auto_healing_policies}
        '''
        result = self._values.get("auto_healing_policies")
        return typing.cast(typing.Optional[ComputeInstanceGroupManagerAutoHealingPolicies], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional textual description of the instance group manager.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#description ComputeInstanceGroupManager#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#id ComputeInstanceGroupManager#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_lifecycle_policy(
        self,
    ) -> typing.Optional["ComputeInstanceGroupManagerInstanceLifecyclePolicy"]:
        '''instance_lifecycle_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#instance_lifecycle_policy ComputeInstanceGroupManager#instance_lifecycle_policy}
        '''
        result = self._values.get("instance_lifecycle_policy")
        return typing.cast(typing.Optional["ComputeInstanceGroupManagerInstanceLifecyclePolicy"], result)

    @builtins.property
    def list_managed_instances_results(self) -> typing.Optional[builtins.str]:
        '''Pagination behavior of the listManagedInstances API method for this managed instance group.

        Valid values are: "PAGELESS", "PAGINATED". If PAGELESS (default), Pagination is disabled for the group's listManagedInstances API method. maxResults and pageToken query parameters are ignored and all instances are returned in a single response. If PAGINATED, pagination is enabled, maxResults and pageToken query parameters are respected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#list_managed_instances_results ComputeInstanceGroupManager#list_managed_instances_results}
        '''
        result = self._values.get("list_managed_instances_results")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def named_port(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGroupManagerNamedPort"]]]:
        '''named_port block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#named_port ComputeInstanceGroupManager#named_port}
        '''
        result = self._values.get("named_port")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGroupManagerNamedPort"]]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the resource belongs.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#project ComputeInstanceGroupManager#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_policies(
        self,
    ) -> typing.Optional["ComputeInstanceGroupManagerResourcePolicies"]:
        '''resource_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#resource_policies ComputeInstanceGroupManager#resource_policies}
        '''
        result = self._values.get("resource_policies")
        return typing.cast(typing.Optional["ComputeInstanceGroupManagerResourcePolicies"], result)

    @builtins.property
    def standby_policy(
        self,
    ) -> typing.Optional["ComputeInstanceGroupManagerStandbyPolicy"]:
        '''standby_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#standby_policy ComputeInstanceGroupManager#standby_policy}
        '''
        result = self._values.get("standby_policy")
        return typing.cast(typing.Optional["ComputeInstanceGroupManagerStandbyPolicy"], result)

    @builtins.property
    def stateful_disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGroupManagerStatefulDisk"]]]:
        '''stateful_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#stateful_disk ComputeInstanceGroupManager#stateful_disk}
        '''
        result = self._values.get("stateful_disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGroupManagerStatefulDisk"]]], result)

    @builtins.property
    def stateful_external_ip(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGroupManagerStatefulExternalIp"]]]:
        '''stateful_external_ip block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#stateful_external_ip ComputeInstanceGroupManager#stateful_external_ip}
        '''
        result = self._values.get("stateful_external_ip")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGroupManagerStatefulExternalIp"]]], result)

    @builtins.property
    def stateful_internal_ip(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGroupManagerStatefulInternalIp"]]]:
        '''stateful_internal_ip block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#stateful_internal_ip ComputeInstanceGroupManager#stateful_internal_ip}
        '''
        result = self._values.get("stateful_internal_ip")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGroupManagerStatefulInternalIp"]]], result)

    @builtins.property
    def target_pools(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The full URL of all target pools to which new instances in the group are added.

        Updating the target pools attribute does not affect existing instances.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#target_pools ComputeInstanceGroupManager#target_pools}
        '''
        result = self._values.get("target_pools")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target_size(self) -> typing.Optional[jsii.Number]:
        '''The target number of running instances for this managed instance group.

        This value should always be explicitly set unless this resource is attached to an autoscaler, in which case it should never be set. Defaults to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#target_size ComputeInstanceGroupManager#target_size}
        '''
        result = self._values.get("target_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_stopped_size(self) -> typing.Optional[jsii.Number]:
        '''The target number of stopped instances for this managed instance group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#target_stopped_size ComputeInstanceGroupManager#target_stopped_size}
        '''
        result = self._values.get("target_stopped_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_suspended_size(self) -> typing.Optional[jsii.Number]:
        '''The target number of suspended instances for this managed instance group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#target_suspended_size ComputeInstanceGroupManager#target_suspended_size}
        '''
        result = self._values.get("target_suspended_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeInstanceGroupManagerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#timeouts ComputeInstanceGroupManager#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeInstanceGroupManagerTimeouts"], result)

    @builtins.property
    def update_policy(
        self,
    ) -> typing.Optional["ComputeInstanceGroupManagerUpdatePolicy"]:
        '''update_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#update_policy ComputeInstanceGroupManager#update_policy}
        '''
        result = self._values.get("update_policy")
        return typing.cast(typing.Optional["ComputeInstanceGroupManagerUpdatePolicy"], result)

    @builtins.property
    def wait_for_instances(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to wait for all instances to be created/updated before returning.

        Note that if this is set to true and the operation does not succeed, Terraform will continue trying until it times out.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#wait_for_instances ComputeInstanceGroupManager#wait_for_instances}
        '''
        result = self._values.get("wait_for_instances")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def wait_for_instances_status(self) -> typing.Optional[builtins.str]:
        '''When used with wait_for_instances specifies the status to wait for.

        When STABLE is specified this resource will wait until the instances are stable before returning. When UPDATED is set, it will wait for the version target to be reached and any per instance configs to be effective and all instances configs to be effective as well as all instances to be stable before returning.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#wait_for_instances_status ComputeInstanceGroupManager#wait_for_instances_status}
        '''
        result = self._values.get("wait_for_instances_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''The zone that instances in this group should be created in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#zone ComputeInstanceGroupManager#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceGroupManagerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerInstanceLifecyclePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "default_action_on_failure": "defaultActionOnFailure",
        "force_update_on_repair": "forceUpdateOnRepair",
    },
)
class ComputeInstanceGroupManagerInstanceLifecyclePolicy:
    def __init__(
        self,
        *,
        default_action_on_failure: typing.Optional[builtins.str] = None,
        force_update_on_repair: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_action_on_failure: Default behavior for all instance or health check failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#default_action_on_failure ComputeInstanceGroupManager#default_action_on_failure}
        :param force_update_on_repair: Specifies whether to apply the group's latest configuration when repairing a VM. Valid options are: YES, NO. If YES and you updated the group's instance template or per-instance configurations after the VM was created, then these changes are applied when VM is repaired. If NO (default), then updates are applied in accordance with the group's update policy type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#force_update_on_repair ComputeInstanceGroupManager#force_update_on_repair}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3fc1515a67c904e65f9d2fb8bcfd45bd12bc03693e83ba829ad696c3d60d96f)
            check_type(argname="argument default_action_on_failure", value=default_action_on_failure, expected_type=type_hints["default_action_on_failure"])
            check_type(argname="argument force_update_on_repair", value=force_update_on_repair, expected_type=type_hints["force_update_on_repair"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_action_on_failure is not None:
            self._values["default_action_on_failure"] = default_action_on_failure
        if force_update_on_repair is not None:
            self._values["force_update_on_repair"] = force_update_on_repair

    @builtins.property
    def default_action_on_failure(self) -> typing.Optional[builtins.str]:
        '''Default behavior for all instance or health check failures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#default_action_on_failure ComputeInstanceGroupManager#default_action_on_failure}
        '''
        result = self._values.get("default_action_on_failure")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_update_on_repair(self) -> typing.Optional[builtins.str]:
        '''Specifies whether to apply the group's latest configuration when repairing a VM.

        Valid options are: YES, NO. If YES and you updated the group's instance template or per-instance configurations after the VM was created, then these changes are applied when VM is repaired. If NO (default), then updates are applied in accordance with the group's update policy type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#force_update_on_repair ComputeInstanceGroupManager#force_update_on_repair}
        '''
        result = self._values.get("force_update_on_repair")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceGroupManagerInstanceLifecyclePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceGroupManagerInstanceLifecyclePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerInstanceLifecyclePolicyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b8608d67ba9fb5ed1321b3ded629bc7cc5f6eabc3eed8379e57c242aed9025b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDefaultActionOnFailure")
    def reset_default_action_on_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultActionOnFailure", []))

    @jsii.member(jsii_name="resetForceUpdateOnRepair")
    def reset_force_update_on_repair(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceUpdateOnRepair", []))

    @builtins.property
    @jsii.member(jsii_name="defaultActionOnFailureInput")
    def default_action_on_failure_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultActionOnFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="forceUpdateOnRepairInput")
    def force_update_on_repair_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forceUpdateOnRepairInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultActionOnFailure")
    def default_action_on_failure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultActionOnFailure"))

    @default_action_on_failure.setter
    def default_action_on_failure(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb301d9b091785eb4757516ef3bf17cd12bdca993f2fbb983646d9fc0a343d1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultActionOnFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceUpdateOnRepair")
    def force_update_on_repair(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forceUpdateOnRepair"))

    @force_update_on_repair.setter
    def force_update_on_repair(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c64735f7cd79dfcc4178b98f5a788da1a7de6c7346f1f81f78ae4bcd7cabae85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceUpdateOnRepair", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceGroupManagerInstanceLifecyclePolicy]:
        return typing.cast(typing.Optional[ComputeInstanceGroupManagerInstanceLifecyclePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceGroupManagerInstanceLifecyclePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d4330a124172df0968cf6275d146797315e0a7ea95a3d9b1e3098c355bb876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerNamedPort",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "port": "port"},
)
class ComputeInstanceGroupManagerNamedPort:
    def __init__(self, *, name: builtins.str, port: jsii.Number) -> None:
        '''
        :param name: The name of the port. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#name ComputeInstanceGroupManager#name}
        :param port: The port number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#port ComputeInstanceGroupManager#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a1f47208f8b27293e91cd1c63831429babf6a25a31e39cbfffa8c04f75a2940)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "port": port,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the port.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#name ComputeInstanceGroupManager#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''The port number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#port ComputeInstanceGroupManager#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceGroupManagerNamedPort(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceGroupManagerNamedPortList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerNamedPortList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa9c1ff8faf52bde583c1c83bc28bbf41148499ddfa93655f4e920511b1992e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceGroupManagerNamedPortOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93461c18dd8e0fffdb3129f68408a1b22b178616afd13535fce70dd71d854b6a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceGroupManagerNamedPortOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5787bad7becb8abc528d7dc61c2522982daf0f6eb6bf41a25420a3fcd4f4c523)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c383aa5fce0e7d10b89d9b6563433bf72a9df0bf76bb65f115a27b30a885d74b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e0e910b2d459a886468ccc8f75b7afcdeb69c6400d7a9b04bbd850fa62dbe67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGroupManagerNamedPort]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGroupManagerNamedPort]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGroupManagerNamedPort]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b87caaaa0b7cf288ade24647505151899acfdf142544f19f420eaff790103e68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceGroupManagerNamedPortOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerNamedPortOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8029ef149a2afb864524b38fd033f5d875a7d583aa52d0175eafe1148614079c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4807a861c92385bfcd2fc448fa64321ff746e97c114ed7d0eb9fdcbd6cc706ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77a0beb7ef7c597b6eec53313ff0bdf902f59981f09f8e9cd2f93b04f4264e4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerNamedPort]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerNamedPort]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerNamedPort]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6161046932db128805649741d6de379684a98873b599a0d4a370e654c891ac8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerResourcePolicies",
    jsii_struct_bases=[],
    name_mapping={"workload_policy": "workloadPolicy"},
)
class ComputeInstanceGroupManagerResourcePolicies:
    def __init__(
        self,
        *,
        workload_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param workload_policy: The URL of the workload policy that is specified for this managed instance group. It can be a full or partial URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#workload_policy ComputeInstanceGroupManager#workload_policy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efdca6bc5c0e3a3a6e4da959db79bc2efd2b650a55575de8a73f0017bac563fe)
            check_type(argname="argument workload_policy", value=workload_policy, expected_type=type_hints["workload_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if workload_policy is not None:
            self._values["workload_policy"] = workload_policy

    @builtins.property
    def workload_policy(self) -> typing.Optional[builtins.str]:
        '''The URL of the workload policy that is specified for this managed instance group.

        It can be a full or partial URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#workload_policy ComputeInstanceGroupManager#workload_policy}
        '''
        result = self._values.get("workload_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceGroupManagerResourcePolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceGroupManagerResourcePoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerResourcePoliciesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__405c76856c87db2394d1d10a6772f2fcf1f23de3234ecf8cf3c3d16f4f44cca7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetWorkloadPolicy")
    def reset_workload_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkloadPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="workloadPolicyInput")
    def workload_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workloadPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadPolicy")
    def workload_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workloadPolicy"))

    @workload_policy.setter
    def workload_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67ae4c12f77c6611082ee100d81b4e2d8a18787370d1d73a06fe27097d69f75d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceGroupManagerResourcePolicies]:
        return typing.cast(typing.Optional[ComputeInstanceGroupManagerResourcePolicies], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceGroupManagerResourcePolicies],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75758dff4a15608dc9158c6cc9dbd165dfb64f9fd1093a2a5ff2cdc7c6962adb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStandbyPolicy",
    jsii_struct_bases=[],
    name_mapping={"initial_delay_sec": "initialDelaySec", "mode": "mode"},
)
class ComputeInstanceGroupManagerStandbyPolicy:
    def __init__(
        self,
        *,
        initial_delay_sec: typing.Optional[jsii.Number] = None,
        mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param initial_delay_sec: Specifies the number of seconds that the MIG should wait to suspend or stop a VM after that VM was created. The initial delay gives the initialization script the time to prepare your VM for a quick scale out. The value of initial delay must be between 0 and 3600 seconds. The default value is 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#initial_delay_sec ComputeInstanceGroupManager#initial_delay_sec}
        :param mode: Defines how a MIG resumes or starts VMs from a standby pool when the group scales out. The default mode is "MANUAL". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#mode ComputeInstanceGroupManager#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c71baeb7fc5123330689489a93125eecf3d060452e718233d69ae287af80bd84)
            check_type(argname="argument initial_delay_sec", value=initial_delay_sec, expected_type=type_hints["initial_delay_sec"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if initial_delay_sec is not None:
            self._values["initial_delay_sec"] = initial_delay_sec
        if mode is not None:
            self._values["mode"] = mode

    @builtins.property
    def initial_delay_sec(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of seconds that the MIG should wait to suspend or stop a VM after that VM was created.

        The initial delay gives the initialization script the time to prepare your VM for a quick scale out. The value of initial delay must be between 0 and 3600 seconds. The default value is 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#initial_delay_sec ComputeInstanceGroupManager#initial_delay_sec}
        '''
        result = self._values.get("initial_delay_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Defines how a MIG resumes or starts VMs from a standby pool when the group scales out.

        The default mode is "MANUAL".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#mode ComputeInstanceGroupManager#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceGroupManagerStandbyPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceGroupManagerStandbyPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStandbyPolicyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2ee98a8d9284dd50b291390d17d997857c197221bf9ecdfa3f65d1f5a62ca1e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInitialDelaySec")
    def reset_initial_delay_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialDelaySec", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @builtins.property
    @jsii.member(jsii_name="initialDelaySecInput")
    def initial_delay_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialDelaySecInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="initialDelaySec")
    def initial_delay_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelaySec"))

    @initial_delay_sec.setter
    def initial_delay_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44df9f06ac4f7421d7cb00b456deabf6528bed3a62bbdca5c1f96faca62f5b6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelaySec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac57a6ed4b5b1e405eaaaf997411b8e4aeaa536bd04b4fd5c166e24536f3c493)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceGroupManagerStandbyPolicy]:
        return typing.cast(typing.Optional[ComputeInstanceGroupManagerStandbyPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceGroupManagerStandbyPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7bd536908e3832535671bb72a97f2d5d950ac9fa30fb751b4f4385ff2c93966)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatefulDisk",
    jsii_struct_bases=[],
    name_mapping={"device_name": "deviceName", "delete_rule": "deleteRule"},
)
class ComputeInstanceGroupManagerStatefulDisk:
    def __init__(
        self,
        *,
        device_name: builtins.str,
        delete_rule: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param device_name: The device name of the disk to be attached. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#device_name ComputeInstanceGroupManager#device_name}
        :param delete_rule: A value that prescribes what should happen to the stateful disk when the VM instance is deleted. The available options are NEVER and ON_PERMANENT_INSTANCE_DELETION. NEVER - detach the disk when the VM is deleted, but do not delete the disk. ON_PERMANENT_INSTANCE_DELETION will delete the stateful disk when the VM is permanently deleted from the instance group. The default is NEVER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#delete_rule ComputeInstanceGroupManager#delete_rule}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53c169366b4a6d755a1355d761ec329b6f340f89be84d2f6b2f00f0fa7141842)
            check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
            check_type(argname="argument delete_rule", value=delete_rule, expected_type=type_hints["delete_rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "device_name": device_name,
        }
        if delete_rule is not None:
            self._values["delete_rule"] = delete_rule

    @builtins.property
    def device_name(self) -> builtins.str:
        '''The device name of the disk to be attached.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#device_name ComputeInstanceGroupManager#device_name}
        '''
        result = self._values.get("device_name")
        assert result is not None, "Required property 'device_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def delete_rule(self) -> typing.Optional[builtins.str]:
        '''A value that prescribes what should happen to the stateful disk when the VM instance is deleted.

        The available options are NEVER and ON_PERMANENT_INSTANCE_DELETION. NEVER - detach the disk when the VM is deleted, but do not delete the disk. ON_PERMANENT_INSTANCE_DELETION will delete the stateful disk when the VM is permanently deleted from the instance group. The default is NEVER.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#delete_rule ComputeInstanceGroupManager#delete_rule}
        '''
        result = self._values.get("delete_rule")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceGroupManagerStatefulDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceGroupManagerStatefulDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatefulDiskList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8190def9750a27a015d6d21d5f64e42664c448bb5731a021ee85b652c423b01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceGroupManagerStatefulDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ec99d887cfd66db50da4d5e3451417eea9f3d8cd7918ff256e0a3bab93b86b5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceGroupManagerStatefulDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d783f0faf8c7e72679354c8127573b3aefdeff96c2cf9789ffae067f20aed326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c6e0c7a1ed3fbf802d05f78939d806169933f83104f42d260a83d20929c081e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e3a2b7e594ebc4187fc502a9111c9b6004cccd83893f20893a959d6212d6698)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGroupManagerStatefulDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGroupManagerStatefulDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGroupManagerStatefulDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adde6b8866be63b2a12f37184259f7157d3fd8294b817a2604e04abaafc62371)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceGroupManagerStatefulDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatefulDiskOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5f4920fb2e74f4182e6b40d9e8c29acf15cc63d4352ade4b08a372828cbe444)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDeleteRule")
    def reset_delete_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteRule", []))

    @builtins.property
    @jsii.member(jsii_name="deleteRuleInput")
    def delete_rule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceNameInput")
    def device_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteRule")
    def delete_rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteRule"))

    @delete_rule.setter
    def delete_rule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__670f20c4bd293a2d0eeea8a489600fc0aabd27f5a6ea15d16e84e9a4941762f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteRule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceName")
    def device_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceName"))

    @device_name.setter
    def device_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee0b34b5dbc65fbd899300c3f4a4fbb1b77f365f652d41398d75bbfa2176298e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerStatefulDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerStatefulDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerStatefulDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ce1535d0e59c9233eb5b8e38126e4d48b59fd95dadccd16d47335c58deaf6b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatefulExternalIp",
    jsii_struct_bases=[],
    name_mapping={"delete_rule": "deleteRule", "interface_name": "interfaceName"},
)
class ComputeInstanceGroupManagerStatefulExternalIp:
    def __init__(
        self,
        *,
        delete_rule: typing.Optional[builtins.str] = None,
        interface_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delete_rule: A value that prescribes what should happen to an associated static Address resource when a VM instance is permanently deleted. The available options are NEVER and ON_PERMANENT_INSTANCE_DELETION. NEVER - detach the IP when the VM is deleted, but do not delete the address resource. ON_PERMANENT_INSTANCE_DELETION will delete the stateful address when the VM is permanently deleted from the instance group. The default is NEVER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#delete_rule ComputeInstanceGroupManager#delete_rule}
        :param interface_name: The network interface name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#interface_name ComputeInstanceGroupManager#interface_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7d6d3d9effe882552ba603c12e76df32006280609ff4722e4a4024eb5063747)
            check_type(argname="argument delete_rule", value=delete_rule, expected_type=type_hints["delete_rule"])
            check_type(argname="argument interface_name", value=interface_name, expected_type=type_hints["interface_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delete_rule is not None:
            self._values["delete_rule"] = delete_rule
        if interface_name is not None:
            self._values["interface_name"] = interface_name

    @builtins.property
    def delete_rule(self) -> typing.Optional[builtins.str]:
        '''A value that prescribes what should happen to an associated static Address resource when a VM instance is permanently deleted.

        The available options are NEVER and ON_PERMANENT_INSTANCE_DELETION. NEVER - detach the IP when the VM is deleted, but do not delete the address resource. ON_PERMANENT_INSTANCE_DELETION will delete the stateful address when the VM is permanently deleted from the instance group. The default is NEVER.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#delete_rule ComputeInstanceGroupManager#delete_rule}
        '''
        result = self._values.get("delete_rule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interface_name(self) -> typing.Optional[builtins.str]:
        '''The network interface name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#interface_name ComputeInstanceGroupManager#interface_name}
        '''
        result = self._values.get("interface_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceGroupManagerStatefulExternalIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceGroupManagerStatefulExternalIpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatefulExternalIpList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29eca05db670ee8a5e3f70315cdcb21393549087c2d1fafc3a63c8d29b96e786)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceGroupManagerStatefulExternalIpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce11e0576f9bff3ca2c7efa194eabadce183a945ad846a389b3d7702b0286913)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceGroupManagerStatefulExternalIpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c4b7fa68f33572da234e3a3a4a87d2b4c417f0fb759204d8cb2311492472838)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31a8e649355f6f9d7e2c2568e603572e3003b7721ec242c2b8011119079ca10a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caa6a80ba0ffc033d7293953c73b11a66ff4f93bd1a01920a7f4f6c21b21a939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGroupManagerStatefulExternalIp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGroupManagerStatefulExternalIp]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGroupManagerStatefulExternalIp]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69562d87193ecc15aa0683eee96c075daaf3e5b053ecef1ac7aba06b422116bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceGroupManagerStatefulExternalIpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatefulExternalIpOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e1ce2a93eb47ccf23908e5fcda3d5cb5aa619e424b8df86052cbbb1f725147e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDeleteRule")
    def reset_delete_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteRule", []))

    @jsii.member(jsii_name="resetInterfaceName")
    def reset_interface_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterfaceName", []))

    @builtins.property
    @jsii.member(jsii_name="deleteRuleInput")
    def delete_rule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="interfaceNameInput")
    def interface_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interfaceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteRule")
    def delete_rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteRule"))

    @delete_rule.setter
    def delete_rule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69f3993ac615f8461b1e1154d75e6d02c6698726eb5f0045462da514831a85b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteRule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interfaceName")
    def interface_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interfaceName"))

    @interface_name.setter
    def interface_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__177f0931a5fc2a7da3691316b8159e8819d8b1cc9ad6eef4624ff55e1d2ff1a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interfaceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerStatefulExternalIp]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerStatefulExternalIp]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerStatefulExternalIp]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b571548d80a9f4ebd2866066c1bf70c98de522ddfe449376a3ea5dfbca047a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatefulInternalIp",
    jsii_struct_bases=[],
    name_mapping={"delete_rule": "deleteRule", "interface_name": "interfaceName"},
)
class ComputeInstanceGroupManagerStatefulInternalIp:
    def __init__(
        self,
        *,
        delete_rule: typing.Optional[builtins.str] = None,
        interface_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delete_rule: A value that prescribes what should happen to an associated static Address resource when a VM instance is permanently deleted. The available options are NEVER and ON_PERMANENT_INSTANCE_DELETION. NEVER - detach the IP when the VM is deleted, but do not delete the address resource. ON_PERMANENT_INSTANCE_DELETION will delete the stateful address when the VM is permanently deleted from the instance group. The default is NEVER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#delete_rule ComputeInstanceGroupManager#delete_rule}
        :param interface_name: The network interface name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#interface_name ComputeInstanceGroupManager#interface_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d41df27b0351ef17024713b1740700c118e931b82971c4798bd8f28d3dcea67)
            check_type(argname="argument delete_rule", value=delete_rule, expected_type=type_hints["delete_rule"])
            check_type(argname="argument interface_name", value=interface_name, expected_type=type_hints["interface_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delete_rule is not None:
            self._values["delete_rule"] = delete_rule
        if interface_name is not None:
            self._values["interface_name"] = interface_name

    @builtins.property
    def delete_rule(self) -> typing.Optional[builtins.str]:
        '''A value that prescribes what should happen to an associated static Address resource when a VM instance is permanently deleted.

        The available options are NEVER and ON_PERMANENT_INSTANCE_DELETION. NEVER - detach the IP when the VM is deleted, but do not delete the address resource. ON_PERMANENT_INSTANCE_DELETION will delete the stateful address when the VM is permanently deleted from the instance group. The default is NEVER.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#delete_rule ComputeInstanceGroupManager#delete_rule}
        '''
        result = self._values.get("delete_rule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interface_name(self) -> typing.Optional[builtins.str]:
        '''The network interface name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#interface_name ComputeInstanceGroupManager#interface_name}
        '''
        result = self._values.get("interface_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceGroupManagerStatefulInternalIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceGroupManagerStatefulInternalIpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatefulInternalIpList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3846fb9a8a308f36c0d3e9b9df6d5957d08aa7ae92101d683393a705331edb7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceGroupManagerStatefulInternalIpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7911cc9403f1ee2f03f7d68db5da6d12cbc062f694fbe002604ab556a367dbea)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceGroupManagerStatefulInternalIpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18952c6c9e4d1fd69616e49a172d87b954f085c7b99f728c60483e2b73d65763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d203c0d8bc222f70ce92e6b30345bee7b52b913d286a73e429c072880e54a395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a1ad6e94616ee8c579b7167137547909a7a430adac009139a6221958372af65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGroupManagerStatefulInternalIp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGroupManagerStatefulInternalIp]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGroupManagerStatefulInternalIp]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed6b7f731f1c0f92441364337a09dc490415046b5378d97d73ddc502bcd53a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceGroupManagerStatefulInternalIpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatefulInternalIpOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f30deaf636d19d568cf5235c3deb44e9cb967f01fd27a1536d7f381e66d02923)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDeleteRule")
    def reset_delete_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteRule", []))

    @jsii.member(jsii_name="resetInterfaceName")
    def reset_interface_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterfaceName", []))

    @builtins.property
    @jsii.member(jsii_name="deleteRuleInput")
    def delete_rule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="interfaceNameInput")
    def interface_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interfaceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteRule")
    def delete_rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteRule"))

    @delete_rule.setter
    def delete_rule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ffdb7247d51f27c9f6652492abdbc637f85af2e5cd529ca1264f8a6107bdf5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteRule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interfaceName")
    def interface_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interfaceName"))

    @interface_name.setter
    def interface_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47a1580580a656eb9f0f8efd0dc42add84b9ed4c6281fff45d28f44df52a5cfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interfaceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerStatefulInternalIp]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerStatefulInternalIp]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerStatefulInternalIp]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49b50e9ca48394a65596aabbce05e4b516fe74ab2eea8cf74af37a9429510fdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeInstanceGroupManagerStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceGroupManagerStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatusAllInstancesConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeInstanceGroupManagerStatusAllInstancesConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceGroupManagerStatusAllInstancesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceGroupManagerStatusAllInstancesConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatusAllInstancesConfigList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62a14a02543bf3b872db4e3bdd217678293618c579bfc2e7ceb003d21aa783f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceGroupManagerStatusAllInstancesConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b917d47a2f9fa1ba94b9448281821e7eba4b274dd67066dfb7459b5a2bd7a75e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceGroupManagerStatusAllInstancesConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aeb4aef1f474e7856f3d48efd3e7fee8e16a3489b8fcc91b645baf46347f26e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef53519611096be6cd966be51b8d960392dfffaac5f33abba47f202706a243c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d85f10faae748167f6062391e505c38e2fbe8cbae75637f7738d552a33080382)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceGroupManagerStatusAllInstancesConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatusAllInstancesConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee4cc380296e771830f5c77050a9a71366665b261f412af8cacd93617c4e5a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="currentRevision")
    def current_revision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "currentRevision"))

    @builtins.property
    @jsii.member(jsii_name="effective")
    def effective(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "effective"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceGroupManagerStatusAllInstancesConfig]:
        return typing.cast(typing.Optional[ComputeInstanceGroupManagerStatusAllInstancesConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceGroupManagerStatusAllInstancesConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b24c1670fa28bb161ed9265eb4e4401e9a5ee7bc9ad34c563837b667a6f1b193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceGroupManagerStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatusList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5773ffdc88f9e415e1e1a76471f1c11248808b89db505eee077ef5e0b179f063)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceGroupManagerStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b2ba8513f84c8c1fbccffea2846934959adb02308cc549e9ddf07572753850d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceGroupManagerStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cb5de2b4f06501da76418526aec8996d649536065ad171ca45c97749c0819b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4bb7880016ef02c9b0649d16d6076ad6cd86ed143b9860750d500c38822300e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5293cb4337e5e6bcfc693fa410cf30a0e39237b7605aac5535a93ddc5cdf5f7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceGroupManagerStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatusOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60cafe0ae798f80429815e3427ecfb6da26ca450c6f592bf64541d6ba2e24672)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allInstancesConfig")
    def all_instances_config(
        self,
    ) -> ComputeInstanceGroupManagerStatusAllInstancesConfigList:
        return typing.cast(ComputeInstanceGroupManagerStatusAllInstancesConfigList, jsii.get(self, "allInstancesConfig"))

    @builtins.property
    @jsii.member(jsii_name="isStable")
    def is_stable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isStable"))

    @builtins.property
    @jsii.member(jsii_name="stateful")
    def stateful(self) -> "ComputeInstanceGroupManagerStatusStatefulList":
        return typing.cast("ComputeInstanceGroupManagerStatusStatefulList", jsii.get(self, "stateful"))

    @builtins.property
    @jsii.member(jsii_name="versionTarget")
    def version_target(self) -> "ComputeInstanceGroupManagerStatusVersionTargetList":
        return typing.cast("ComputeInstanceGroupManagerStatusVersionTargetList", jsii.get(self, "versionTarget"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeInstanceGroupManagerStatus]:
        return typing.cast(typing.Optional[ComputeInstanceGroupManagerStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceGroupManagerStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d16af710cfc2a9fb29013d27c1587875efe90c86800e419cb338f28420c2545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatusStateful",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeInstanceGroupManagerStatusStateful:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceGroupManagerStatusStateful(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceGroupManagerStatusStatefulList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatusStatefulList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9878efb940fcc6cf62486c3347ec4902ed38bccb71be93b98efea6727695acc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceGroupManagerStatusStatefulOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29becb9a3ca083884f99954da136e999750cf51d6b6d2b0e830aca0d491720b6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceGroupManagerStatusStatefulOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b14d7d1124c405d51d6cb693545177a512f6559f084d11e20afc8b6cd4da22e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ffb4e64b6e245e60f7a28d164ceb48f50cafdf2d379866833aafdab489a64a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72396cec022d784918f812531bc1d86cbc7bf6fc5923e201ed9bd2f1ad3257d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceGroupManagerStatusStatefulOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatusStatefulOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea333064502f515c1b203003081c9398da0afdc53f7cdbb77f3aa31c5af2db2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hasStatefulConfig")
    def has_stateful_config(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "hasStatefulConfig"))

    @builtins.property
    @jsii.member(jsii_name="perInstanceConfigs")
    def per_instance_configs(
        self,
    ) -> "ComputeInstanceGroupManagerStatusStatefulPerInstanceConfigsList":
        return typing.cast("ComputeInstanceGroupManagerStatusStatefulPerInstanceConfigsList", jsii.get(self, "perInstanceConfigs"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceGroupManagerStatusStateful]:
        return typing.cast(typing.Optional[ComputeInstanceGroupManagerStatusStateful], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceGroupManagerStatusStateful],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6323c019f12484af3516f8a9449332e762e194f73f7bc9ae79f32a3d05f3fed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatusStatefulPerInstanceConfigs",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeInstanceGroupManagerStatusStatefulPerInstanceConfigs:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceGroupManagerStatusStatefulPerInstanceConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceGroupManagerStatusStatefulPerInstanceConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatusStatefulPerInstanceConfigsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7388ecba87671f2750a8208adaae7ad7d707f9e36226404811d2f7c7a053804c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceGroupManagerStatusStatefulPerInstanceConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17eef301e1ad3259f9b38dd7c66af4d87faf359c271b81457b549dfe33e68c4a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceGroupManagerStatusStatefulPerInstanceConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec5bbd6ff7a21eef98aacf50304d7d88f0ed221229d664ed4793924ff8a9357c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8cb786b119a00776fc459324a41b6e8ac527e48cec84572d8b4a16fcb00aa00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df259c52dd5c3e8d33008a3c54b7b909fdaaa1d5ff43f3462d1afb5aa1fb4ad5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceGroupManagerStatusStatefulPerInstanceConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatusStatefulPerInstanceConfigsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f301b9515fc3bf519694f73be6623c195add2e28668a37afd3d549ee0dd973f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allEffective")
    def all_effective(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "allEffective"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceGroupManagerStatusStatefulPerInstanceConfigs]:
        return typing.cast(typing.Optional[ComputeInstanceGroupManagerStatusStatefulPerInstanceConfigs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceGroupManagerStatusStatefulPerInstanceConfigs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e444747d755d468bed194178ca8fd20476cb87f51e7f01585190a97dc7f6cb98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatusVersionTarget",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeInstanceGroupManagerStatusVersionTarget:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceGroupManagerStatusVersionTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceGroupManagerStatusVersionTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatusVersionTargetList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c4279b27076e40d7cf2f53a0da729af0b2b5990f2e008c6d0053f32a80fec42)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceGroupManagerStatusVersionTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e61fea77efdecdba6db618988b0ebad86ca96fe7082a95071dd6f05e3543f309)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceGroupManagerStatusVersionTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a7866dabcf84dc9f3c759e18bbf92aab709175ca974c9f1db4df5c9ad2db2ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d530b91478bdb122771147dcf1cae9521bf0617386156ed320a8faa6e35f99cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de4b54680ede3f74ae5348020bd1ec7ec07d4f931c2e768d1eb3ff734cd97c56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceGroupManagerStatusVersionTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerStatusVersionTargetOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3968c10c291fcad34c6830e7acf092095ef0ea30ebdc412c7b677b78446ff92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="isReached")
    def is_reached(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isReached"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceGroupManagerStatusVersionTarget]:
        return typing.cast(typing.Optional[ComputeInstanceGroupManagerStatusVersionTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceGroupManagerStatusVersionTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8e0b0bc557a5d795ce50fbf26d5e9476dfdb4263e641192289ab15f0b169188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeInstanceGroupManagerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#create ComputeInstanceGroupManager#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#delete ComputeInstanceGroupManager#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#update ComputeInstanceGroupManager#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b88f64b661ab0ba3b72e625202ee8af9a513960db903d3bea9afebfa05b20b)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#create ComputeInstanceGroupManager#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#delete ComputeInstanceGroupManager#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#update ComputeInstanceGroupManager#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceGroupManagerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceGroupManagerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19dcd53ddac27603a1e788afa2200a3e684a5e6ba6c9fbe716b9b944f7c6df76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a42cf8277c04e632523c0a1c0f8296814f975b478522fe0df25b2e3f1b3d074)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae9ad15094a33a558b2a91d829836df9b37bb1ad1cf46a7112184164cc7c1e09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__234970722f2e0d96c11ae97b2042ab0cbf9ce509041a84688e498e044d8448c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc22ebc4aec9ec2868d27d70903e57dc3960d7ef38149e73dd73ef34e23f174)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerUpdatePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "minimal_action": "minimalAction",
        "type": "type",
        "max_surge_fixed": "maxSurgeFixed",
        "max_surge_percent": "maxSurgePercent",
        "max_unavailable_fixed": "maxUnavailableFixed",
        "max_unavailable_percent": "maxUnavailablePercent",
        "most_disruptive_allowed_action": "mostDisruptiveAllowedAction",
        "replacement_method": "replacementMethod",
    },
)
class ComputeInstanceGroupManagerUpdatePolicy:
    def __init__(
        self,
        *,
        minimal_action: builtins.str,
        type: builtins.str,
        max_surge_fixed: typing.Optional[jsii.Number] = None,
        max_surge_percent: typing.Optional[jsii.Number] = None,
        max_unavailable_fixed: typing.Optional[jsii.Number] = None,
        max_unavailable_percent: typing.Optional[jsii.Number] = None,
        most_disruptive_allowed_action: typing.Optional[builtins.str] = None,
        replacement_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param minimal_action: Minimal action to be taken on an instance. You can specify either NONE to forbid any actions, REFRESH to update without stopping instances, RESTART to restart existing instances or REPLACE to delete and create new instances from the target template. If you specify a REFRESH, the Updater will attempt to perform that action only. However, if the Updater determines that the minimal action you specify is not enough to perform the update, it might perform a more disruptive action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#minimal_action ComputeInstanceGroupManager#minimal_action}
        :param type: The type of update process. You can specify either PROACTIVE so that the instance group manager proactively executes actions in order to bring instances to their target versions or OPPORTUNISTIC so that no action is proactively executed but the update will be performed as part of other actions (for example, resizes or recreateInstances calls). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#type ComputeInstanceGroupManager#type}
        :param max_surge_fixed: Specifies a fixed number of VM instances. This must be a positive integer. Conflicts with max_surge_percent. Both cannot be 0 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#max_surge_fixed ComputeInstanceGroupManager#max_surge_fixed}
        :param max_surge_percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Conflicts with max_surge_fixed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#max_surge_percent ComputeInstanceGroupManager#max_surge_percent}
        :param max_unavailable_fixed: Specifies a fixed number of VM instances. This must be a positive integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#max_unavailable_fixed ComputeInstanceGroupManager#max_unavailable_fixed}
        :param max_unavailable_percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#max_unavailable_percent ComputeInstanceGroupManager#max_unavailable_percent}
        :param most_disruptive_allowed_action: Most disruptive action that is allowed to be taken on an instance. You can specify either NONE to forbid any actions, REFRESH to allow actions that do not need instance restart, RESTART to allow actions that can be applied without instance replacing or REPLACE to allow all possible actions. If the Updater determines that the minimal update action needed is more disruptive than most disruptive allowed action you specify it will not perform the update at all. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#most_disruptive_allowed_action ComputeInstanceGroupManager#most_disruptive_allowed_action}
        :param replacement_method: The instance replacement method for managed instance groups. Valid values are: "RECREATE", "SUBSTITUTE". If SUBSTITUTE (default), the group replaces VM instances with new instances that have randomly generated names. If RECREATE, instance names are preserved. You must also set max_unavailable_fixed or max_unavailable_percent to be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#replacement_method ComputeInstanceGroupManager#replacement_method}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae4926e65c420ed99306724ee04b965b43a015471ee406ce46471772f53d2103)
            check_type(argname="argument minimal_action", value=minimal_action, expected_type=type_hints["minimal_action"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument max_surge_fixed", value=max_surge_fixed, expected_type=type_hints["max_surge_fixed"])
            check_type(argname="argument max_surge_percent", value=max_surge_percent, expected_type=type_hints["max_surge_percent"])
            check_type(argname="argument max_unavailable_fixed", value=max_unavailable_fixed, expected_type=type_hints["max_unavailable_fixed"])
            check_type(argname="argument max_unavailable_percent", value=max_unavailable_percent, expected_type=type_hints["max_unavailable_percent"])
            check_type(argname="argument most_disruptive_allowed_action", value=most_disruptive_allowed_action, expected_type=type_hints["most_disruptive_allowed_action"])
            check_type(argname="argument replacement_method", value=replacement_method, expected_type=type_hints["replacement_method"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "minimal_action": minimal_action,
            "type": type,
        }
        if max_surge_fixed is not None:
            self._values["max_surge_fixed"] = max_surge_fixed
        if max_surge_percent is not None:
            self._values["max_surge_percent"] = max_surge_percent
        if max_unavailable_fixed is not None:
            self._values["max_unavailable_fixed"] = max_unavailable_fixed
        if max_unavailable_percent is not None:
            self._values["max_unavailable_percent"] = max_unavailable_percent
        if most_disruptive_allowed_action is not None:
            self._values["most_disruptive_allowed_action"] = most_disruptive_allowed_action
        if replacement_method is not None:
            self._values["replacement_method"] = replacement_method

    @builtins.property
    def minimal_action(self) -> builtins.str:
        '''Minimal action to be taken on an instance.

        You can specify either NONE to forbid any actions, REFRESH to update without stopping instances, RESTART to restart existing instances or REPLACE to delete and create new instances from the target template. If you specify a REFRESH, the Updater will attempt to perform that action only. However, if the Updater determines that the minimal action you specify is not enough to perform the update, it might perform a more disruptive action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#minimal_action ComputeInstanceGroupManager#minimal_action}
        '''
        result = self._values.get("minimal_action")
        assert result is not None, "Required property 'minimal_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of update process.

        You can specify either PROACTIVE so that the instance group manager proactively executes actions in order to bring instances to their target versions or OPPORTUNISTIC so that no action is proactively executed but the update will be performed as part of other actions (for example, resizes or recreateInstances calls).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#type ComputeInstanceGroupManager#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_surge_fixed(self) -> typing.Optional[jsii.Number]:
        '''Specifies a fixed number of VM instances.

        This must be a positive integer. Conflicts with max_surge_percent. Both cannot be 0

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#max_surge_fixed ComputeInstanceGroupManager#max_surge_fixed}
        '''
        result = self._values.get("max_surge_fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_surge_percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Conflicts with max_surge_fixed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#max_surge_percent ComputeInstanceGroupManager#max_surge_percent}
        '''
        result = self._values.get("max_surge_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_unavailable_fixed(self) -> typing.Optional[jsii.Number]:
        '''Specifies a fixed number of VM instances. This must be a positive integer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#max_unavailable_fixed ComputeInstanceGroupManager#max_unavailable_fixed}
        '''
        result = self._values.get("max_unavailable_fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_unavailable_percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#max_unavailable_percent ComputeInstanceGroupManager#max_unavailable_percent}
        '''
        result = self._values.get("max_unavailable_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def most_disruptive_allowed_action(self) -> typing.Optional[builtins.str]:
        '''Most disruptive action that is allowed to be taken on an instance.

        You can specify either NONE to forbid any actions, REFRESH to allow actions that do not need instance restart, RESTART to allow actions that can be applied without instance replacing or REPLACE to allow all possible actions. If the Updater determines that the minimal update action needed is more disruptive than most disruptive allowed action you specify it will not perform the update at all.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#most_disruptive_allowed_action ComputeInstanceGroupManager#most_disruptive_allowed_action}
        '''
        result = self._values.get("most_disruptive_allowed_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replacement_method(self) -> typing.Optional[builtins.str]:
        '''The instance replacement method for managed instance groups.

        Valid values are: "RECREATE", "SUBSTITUTE". If SUBSTITUTE (default), the group replaces VM instances with new instances that have randomly generated names. If RECREATE, instance names are preserved.  You must also set max_unavailable_fixed or max_unavailable_percent to be greater than 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#replacement_method ComputeInstanceGroupManager#replacement_method}
        '''
        result = self._values.get("replacement_method")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceGroupManagerUpdatePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceGroupManagerUpdatePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerUpdatePolicyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f189854b7c36ba7b7e482692f357d1139472ce247f400f5f0e2725cefe335a7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxSurgeFixed")
    def reset_max_surge_fixed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxSurgeFixed", []))

    @jsii.member(jsii_name="resetMaxSurgePercent")
    def reset_max_surge_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxSurgePercent", []))

    @jsii.member(jsii_name="resetMaxUnavailableFixed")
    def reset_max_unavailable_fixed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxUnavailableFixed", []))

    @jsii.member(jsii_name="resetMaxUnavailablePercent")
    def reset_max_unavailable_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxUnavailablePercent", []))

    @jsii.member(jsii_name="resetMostDisruptiveAllowedAction")
    def reset_most_disruptive_allowed_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMostDisruptiveAllowedAction", []))

    @jsii.member(jsii_name="resetReplacementMethod")
    def reset_replacement_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplacementMethod", []))

    @builtins.property
    @jsii.member(jsii_name="maxSurgeFixedInput")
    def max_surge_fixed_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxSurgeFixedInput"))

    @builtins.property
    @jsii.member(jsii_name="maxSurgePercentInput")
    def max_surge_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxSurgePercentInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUnavailableFixedInput")
    def max_unavailable_fixed_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUnavailableFixedInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUnavailablePercentInput")
    def max_unavailable_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUnavailablePercentInput"))

    @builtins.property
    @jsii.member(jsii_name="minimalActionInput")
    def minimal_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimalActionInput"))

    @builtins.property
    @jsii.member(jsii_name="mostDisruptiveAllowedActionInput")
    def most_disruptive_allowed_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mostDisruptiveAllowedActionInput"))

    @builtins.property
    @jsii.member(jsii_name="replacementMethodInput")
    def replacement_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "replacementMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxSurgeFixed")
    def max_surge_fixed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxSurgeFixed"))

    @max_surge_fixed.setter
    def max_surge_fixed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e86a0bb61d06787a84eb64df294d82ef2df6dc92663296ec8b33e975f7994a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSurgeFixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxSurgePercent")
    def max_surge_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxSurgePercent"))

    @max_surge_percent.setter
    def max_surge_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1039386f8093ea45d5c3e13255ee0f3b9cde8fd4f5be1aa64b8fbfdc55351a27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSurgePercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUnavailableFixed")
    def max_unavailable_fixed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUnavailableFixed"))

    @max_unavailable_fixed.setter
    def max_unavailable_fixed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0baf4318abea25cec7b83044b35fe5695e021d8ff603ca6e0fcbe78f573994d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUnavailableFixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUnavailablePercent")
    def max_unavailable_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUnavailablePercent"))

    @max_unavailable_percent.setter
    def max_unavailable_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67f44e6a28f622d2ce118f2d96543b92ce75b004288ca188842c417266a37de3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUnavailablePercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimalAction")
    def minimal_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimalAction"))

    @minimal_action.setter
    def minimal_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f13c84db6c6cc3a1577fd9607ac9554a55e538eb6b7f1eaa1f47591e3d0e3e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimalAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mostDisruptiveAllowedAction")
    def most_disruptive_allowed_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mostDisruptiveAllowedAction"))

    @most_disruptive_allowed_action.setter
    def most_disruptive_allowed_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1546faf124a8dffbf158db285b1546944dff221245085a9c1838dab0da2c219)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mostDisruptiveAllowedAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replacementMethod")
    def replacement_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replacementMethod"))

    @replacement_method.setter
    def replacement_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcefaedb4841e7f868979ff7a2c1cf49dd77a192d9198ed89dd011e515250593)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replacementMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cff75897d0ed390fcfea758a88024c6f9f5e5a32222e6e31931bac6ec8320f16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceGroupManagerUpdatePolicy]:
        return typing.cast(typing.Optional[ComputeInstanceGroupManagerUpdatePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceGroupManagerUpdatePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99f5c38e295c0b12e9d44cfdb377a6a8b435c46c0c7d0b863788a232fb9e35ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerVersion",
    jsii_struct_bases=[],
    name_mapping={
        "instance_template": "instanceTemplate",
        "name": "name",
        "target_size": "targetSize",
    },
)
class ComputeInstanceGroupManagerVersion:
    def __init__(
        self,
        *,
        instance_template: builtins.str,
        name: typing.Optional[builtins.str] = None,
        target_size: typing.Optional[typing.Union["ComputeInstanceGroupManagerVersionTargetSize", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param instance_template: The full URL to an instance template from which all new instances of this version will be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#instance_template ComputeInstanceGroupManager#instance_template}
        :param name: Version name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#name ComputeInstanceGroupManager#name}
        :param target_size: target_size block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#target_size ComputeInstanceGroupManager#target_size}
        '''
        if isinstance(target_size, dict):
            target_size = ComputeInstanceGroupManagerVersionTargetSize(**target_size)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90779ac537ddd224c2a59cb8d81e4004483a770a56c3f54a3fd56a44339e80df)
            check_type(argname="argument instance_template", value=instance_template, expected_type=type_hints["instance_template"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument target_size", value=target_size, expected_type=type_hints["target_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_template": instance_template,
        }
        if name is not None:
            self._values["name"] = name
        if target_size is not None:
            self._values["target_size"] = target_size

    @builtins.property
    def instance_template(self) -> builtins.str:
        '''The full URL to an instance template from which all new instances of this version will be created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#instance_template ComputeInstanceGroupManager#instance_template}
        '''
        result = self._values.get("instance_template")
        assert result is not None, "Required property 'instance_template' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Version name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#name ComputeInstanceGroupManager#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_size(
        self,
    ) -> typing.Optional["ComputeInstanceGroupManagerVersionTargetSize"]:
        '''target_size block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#target_size ComputeInstanceGroupManager#target_size}
        '''
        result = self._values.get("target_size")
        return typing.cast(typing.Optional["ComputeInstanceGroupManagerVersionTargetSize"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceGroupManagerVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceGroupManagerVersionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerVersionList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb791d993516df84feb19cf6824f7fa661eff126932258e28c5f0f7f5c4d0299)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceGroupManagerVersionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4519493b9151539f21286321040d2a4c37fc6c121823b9184fda7698b8e53b3e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceGroupManagerVersionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59fd52236e4ed5472c6f2261d86dbf66f1af8647475f42c097fee3298ca20e40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ed80cf7bca02471b32d2f278ef58d057b2b530e9054eef1d6edf2d6c23be9c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac7c6743e4221cb84c7ef14f84383724cff9782a39fcac06eeeb429c0d9d7888)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGroupManagerVersion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGroupManagerVersion]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGroupManagerVersion]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e15a161e501e3523470b51fa6ce795742959e761c9dc31e54ca2e452cf3f61e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceGroupManagerVersionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerVersionOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__054b14b75c3dc9a9f77abadf3904c9e07bc82664346646bf523adc5f01b0da0f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTargetSize")
    def put_target_size(
        self,
        *,
        fixed: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed: The number of instances which are managed for this version. Conflicts with percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#fixed ComputeInstanceGroupManager#fixed}
        :param percent: The number of instances (calculated as percentage) which are managed for this version. Conflicts with fixed. Note that when using percent, rounding will be in favor of explicitly set target_size values; a managed instance group with 2 instances and 2 versions, one of which has a target_size.percent of 60 will create 2 instances of that version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#percent ComputeInstanceGroupManager#percent}
        '''
        value = ComputeInstanceGroupManagerVersionTargetSize(
            fixed=fixed, percent=percent
        )

        return typing.cast(None, jsii.invoke(self, "putTargetSize", [value]))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetTargetSize")
    def reset_target_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetSize", []))

    @builtins.property
    @jsii.member(jsii_name="targetSize")
    def target_size(
        self,
    ) -> "ComputeInstanceGroupManagerVersionTargetSizeOutputReference":
        return typing.cast("ComputeInstanceGroupManagerVersionTargetSizeOutputReference", jsii.get(self, "targetSize"))

    @builtins.property
    @jsii.member(jsii_name="instanceTemplateInput")
    def instance_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="targetSizeInput")
    def target_size_input(
        self,
    ) -> typing.Optional["ComputeInstanceGroupManagerVersionTargetSize"]:
        return typing.cast(typing.Optional["ComputeInstanceGroupManagerVersionTargetSize"], jsii.get(self, "targetSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTemplate")
    def instance_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceTemplate"))

    @instance_template.setter
    def instance_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fd202745481065254e4c50175906e4a66dfb0185f28d81821e07bbb77ff9855)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8699329e7fdd72e78e8547485a419a882aeab4cf318bb3fd2e07a5e662a4c21d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerVersion]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerVersion]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerVersion]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17abbd273563e1e1d4cb3681af0865fdd5c67ae604240b7ce30b8979a163d32b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerVersionTargetSize",
    jsii_struct_bases=[],
    name_mapping={"fixed": "fixed", "percent": "percent"},
)
class ComputeInstanceGroupManagerVersionTargetSize:
    def __init__(
        self,
        *,
        fixed: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed: The number of instances which are managed for this version. Conflicts with percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#fixed ComputeInstanceGroupManager#fixed}
        :param percent: The number of instances (calculated as percentage) which are managed for this version. Conflicts with fixed. Note that when using percent, rounding will be in favor of explicitly set target_size values; a managed instance group with 2 instances and 2 versions, one of which has a target_size.percent of 60 will create 2 instances of that version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#percent ComputeInstanceGroupManager#percent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__207a2a1d8444e1ac40dfe978be3a6126ba41e8f08c796e93a4111b64f1836dcf)
            check_type(argname="argument fixed", value=fixed, expected_type=type_hints["fixed"])
            check_type(argname="argument percent", value=percent, expected_type=type_hints["percent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fixed is not None:
            self._values["fixed"] = fixed
        if percent is not None:
            self._values["percent"] = percent

    @builtins.property
    def fixed(self) -> typing.Optional[jsii.Number]:
        '''The number of instances which are managed for this version. Conflicts with percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#fixed ComputeInstanceGroupManager#fixed}
        '''
        result = self._values.get("fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percent(self) -> typing.Optional[jsii.Number]:
        '''The number of instances (calculated as percentage) which are managed for this version.

        Conflicts with fixed. Note that when using percent, rounding will be in favor of explicitly set target_size values; a managed instance group with 2 instances and 2 versions, one of which has a target_size.percent of 60 will create 2 instances of that version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_group_manager#percent ComputeInstanceGroupManager#percent}
        '''
        result = self._values.get("percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceGroupManagerVersionTargetSize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceGroupManagerVersionTargetSizeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceGroupManager.ComputeInstanceGroupManagerVersionTargetSizeOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51a47b701f091d0aaf1acdd9cb21f3513d17d21cba279ad7eda0599b7afc8afa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFixed")
    def reset_fixed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixed", []))

    @jsii.member(jsii_name="resetPercent")
    def reset_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPercent", []))

    @builtins.property
    @jsii.member(jsii_name="fixedInput")
    def fixed_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fixedInput"))

    @builtins.property
    @jsii.member(jsii_name="percentInput")
    def percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "percentInput"))

    @builtins.property
    @jsii.member(jsii_name="fixed")
    def fixed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fixed"))

    @fixed.setter
    def fixed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2812b359a8f387ef3253a45bf7f763515fa225f1de0d415bb0c558d6e5363387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15f7d4f82ba7ee79a9a950a1eebdf3660aebf59e0921c373e5219415c7dcea53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceGroupManagerVersionTargetSize]:
        return typing.cast(typing.Optional[ComputeInstanceGroupManagerVersionTargetSize], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceGroupManagerVersionTargetSize],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7cd9de8fac3028022f2c3ea8548ac3a0986486800cae5cf43cf92184ba2eb92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeInstanceGroupManager",
    "ComputeInstanceGroupManagerAllInstancesConfig",
    "ComputeInstanceGroupManagerAllInstancesConfigOutputReference",
    "ComputeInstanceGroupManagerAutoHealingPolicies",
    "ComputeInstanceGroupManagerAutoHealingPoliciesOutputReference",
    "ComputeInstanceGroupManagerConfig",
    "ComputeInstanceGroupManagerInstanceLifecyclePolicy",
    "ComputeInstanceGroupManagerInstanceLifecyclePolicyOutputReference",
    "ComputeInstanceGroupManagerNamedPort",
    "ComputeInstanceGroupManagerNamedPortList",
    "ComputeInstanceGroupManagerNamedPortOutputReference",
    "ComputeInstanceGroupManagerResourcePolicies",
    "ComputeInstanceGroupManagerResourcePoliciesOutputReference",
    "ComputeInstanceGroupManagerStandbyPolicy",
    "ComputeInstanceGroupManagerStandbyPolicyOutputReference",
    "ComputeInstanceGroupManagerStatefulDisk",
    "ComputeInstanceGroupManagerStatefulDiskList",
    "ComputeInstanceGroupManagerStatefulDiskOutputReference",
    "ComputeInstanceGroupManagerStatefulExternalIp",
    "ComputeInstanceGroupManagerStatefulExternalIpList",
    "ComputeInstanceGroupManagerStatefulExternalIpOutputReference",
    "ComputeInstanceGroupManagerStatefulInternalIp",
    "ComputeInstanceGroupManagerStatefulInternalIpList",
    "ComputeInstanceGroupManagerStatefulInternalIpOutputReference",
    "ComputeInstanceGroupManagerStatus",
    "ComputeInstanceGroupManagerStatusAllInstancesConfig",
    "ComputeInstanceGroupManagerStatusAllInstancesConfigList",
    "ComputeInstanceGroupManagerStatusAllInstancesConfigOutputReference",
    "ComputeInstanceGroupManagerStatusList",
    "ComputeInstanceGroupManagerStatusOutputReference",
    "ComputeInstanceGroupManagerStatusStateful",
    "ComputeInstanceGroupManagerStatusStatefulList",
    "ComputeInstanceGroupManagerStatusStatefulOutputReference",
    "ComputeInstanceGroupManagerStatusStatefulPerInstanceConfigs",
    "ComputeInstanceGroupManagerStatusStatefulPerInstanceConfigsList",
    "ComputeInstanceGroupManagerStatusStatefulPerInstanceConfigsOutputReference",
    "ComputeInstanceGroupManagerStatusVersionTarget",
    "ComputeInstanceGroupManagerStatusVersionTargetList",
    "ComputeInstanceGroupManagerStatusVersionTargetOutputReference",
    "ComputeInstanceGroupManagerTimeouts",
    "ComputeInstanceGroupManagerTimeoutsOutputReference",
    "ComputeInstanceGroupManagerUpdatePolicy",
    "ComputeInstanceGroupManagerUpdatePolicyOutputReference",
    "ComputeInstanceGroupManagerVersion",
    "ComputeInstanceGroupManagerVersionList",
    "ComputeInstanceGroupManagerVersionOutputReference",
    "ComputeInstanceGroupManagerVersionTargetSize",
    "ComputeInstanceGroupManagerVersionTargetSizeOutputReference",
]

publication.publish()

def _typecheckingstub__772c32b9ceeca4b4eea37f1955026786fcca83e4ecdc91a188a54fb1443ef1eb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    base_instance_name: builtins.str,
    name: builtins.str,
    version: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceGroupManagerVersion, typing.Dict[builtins.str, typing.Any]]]],
    all_instances_config: typing.Optional[typing.Union[ComputeInstanceGroupManagerAllInstancesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_healing_policies: typing.Optional[typing.Union[ComputeInstanceGroupManagerAutoHealingPolicies, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_lifecycle_policy: typing.Optional[typing.Union[ComputeInstanceGroupManagerInstanceLifecyclePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    list_managed_instances_results: typing.Optional[builtins.str] = None,
    named_port: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceGroupManagerNamedPort, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    resource_policies: typing.Optional[typing.Union[ComputeInstanceGroupManagerResourcePolicies, typing.Dict[builtins.str, typing.Any]]] = None,
    standby_policy: typing.Optional[typing.Union[ComputeInstanceGroupManagerStandbyPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    stateful_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceGroupManagerStatefulDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stateful_external_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceGroupManagerStatefulExternalIp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stateful_internal_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceGroupManagerStatefulInternalIp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_size: typing.Optional[jsii.Number] = None,
    target_stopped_size: typing.Optional[jsii.Number] = None,
    target_suspended_size: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[ComputeInstanceGroupManagerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    update_policy: typing.Optional[typing.Union[ComputeInstanceGroupManagerUpdatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    wait_for_instances: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    wait_for_instances_status: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e54287acce01c46eb9efc9607fc83f4042de3306f30581cc34334c46421a292f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6650ed2126446542e53fbc03b4a4e209b61586a8d7b3e62a4cbec7eeb501d67d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceGroupManagerNamedPort, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d7be4cfa175de94e74862222ce3274f535b3ad1499891f6a62e10bb994e95f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceGroupManagerStatefulDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a96df8c5001a94ae94ec24a20230685961a3d2cedc56222e8e2eb0bc4649a8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceGroupManagerStatefulExternalIp, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090673e01cbcf46be7e8bd5453bfaa0bdab0d047d239fdc32023808bee4bb3c8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceGroupManagerStatefulInternalIp, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__193b061bbe53a8a2861a916d8dacbc2e96f198c5d7654d9ab1c808473cb7e34f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceGroupManagerVersion, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2b3370590287b6c9d4614925d660eb3316645c2d3e48dd83f0598866bcdd6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0d4a7edc856e765a0056799102feba9a9250624b66dc77a2a0421f4e57a0003(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24916ad8659be425914a7056c7db3843d732a073e9d9978e33000c4dc84db38d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e43270dbe8b0775817768489d565b660de29dca1bf10ac932f5e49c5a8ab36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8afd310ce48f9d4272cbd2e66f6e8176e5d35b5f57c46665139ccd39cf978a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f8177167dd22487d1e5633057061e64e8fb1217b73353dd36c6b70ea6ffa0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48074ac0ccb45878e52481263daae1164d5b04e9bcabf120664b879a83373ede(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e32a1e0d673cc427b3ecdfdddbed361850038aa1172d14b62e50b9973843ba5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff6bc65034cb05b5f46446267828519cbc66a1bd73d8141592e9fd8d5b2c5f4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6fecfce22102d6dad5189d8de71cc9f5822fac20a30200b9be790f56fa1290a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5829fff854f97989e254fc66fe173a55b865e2bb9e714726d3b161c4f85dd80(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe0fe2046ebbc4dc283c54ce36b7855dfcbf237483bf35c31e150c7b6215295(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69672ce2a451d8ef6f46b1fdf97dafc981010d07cc0de31d7f6c8324e4e9fbd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__376665c84a5d3564feebecba8e2e59586c3f6e063305aa465889000ad92333c4(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb8a5364d520196ad235eb2e219b6d94086d42b933a470ede497669d1576796(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba97c575b1f06f4b8d018a8a64ff4c5d0a20b2a5016259672917532d717e143(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b00a097d661fbd40a723e8b1e17be677eca90fdcb8e3b5616ff302da07429f72(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__075bf7d407cbd8a9a68a3599f8e120dcaefcecc9ae2d54ebd68f2525ce50e160(
    value: typing.Optional[ComputeInstanceGroupManagerAllInstancesConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8542be76f1905a1cf07039be2eebb468970181c3f347d8b4524f3b3cc0e5cb(
    *,
    health_check: builtins.str,
    initial_delay_sec: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d31175be4915add26970157e153e2716899fecca3110af06e7e5d209cb3b0a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b120901647b1e7534c4431a9e82cdedb6709b0a95ad144fc11466d88f0b0a3bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c991a1e1ef9863bfa9bebcb7f79c4f15fe61fd41d31ff958f10029c52dca986e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f8565b0e09599e8c01132bfaff6e931e3ad260c0c79e12f12882cfeba5207e(
    value: typing.Optional[ComputeInstanceGroupManagerAutoHealingPolicies],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1241493119c67face4d74f44b7e398f60b4c2e441ceae192ea1b5583e568f9af(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    base_instance_name: builtins.str,
    name: builtins.str,
    version: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceGroupManagerVersion, typing.Dict[builtins.str, typing.Any]]]],
    all_instances_config: typing.Optional[typing.Union[ComputeInstanceGroupManagerAllInstancesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_healing_policies: typing.Optional[typing.Union[ComputeInstanceGroupManagerAutoHealingPolicies, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_lifecycle_policy: typing.Optional[typing.Union[ComputeInstanceGroupManagerInstanceLifecyclePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    list_managed_instances_results: typing.Optional[builtins.str] = None,
    named_port: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceGroupManagerNamedPort, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    resource_policies: typing.Optional[typing.Union[ComputeInstanceGroupManagerResourcePolicies, typing.Dict[builtins.str, typing.Any]]] = None,
    standby_policy: typing.Optional[typing.Union[ComputeInstanceGroupManagerStandbyPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    stateful_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceGroupManagerStatefulDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stateful_external_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceGroupManagerStatefulExternalIp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stateful_internal_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceGroupManagerStatefulInternalIp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_size: typing.Optional[jsii.Number] = None,
    target_stopped_size: typing.Optional[jsii.Number] = None,
    target_suspended_size: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[ComputeInstanceGroupManagerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    update_policy: typing.Optional[typing.Union[ComputeInstanceGroupManagerUpdatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    wait_for_instances: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    wait_for_instances_status: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3fc1515a67c904e65f9d2fb8bcfd45bd12bc03693e83ba829ad696c3d60d96f(
    *,
    default_action_on_failure: typing.Optional[builtins.str] = None,
    force_update_on_repair: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b8608d67ba9fb5ed1321b3ded629bc7cc5f6eabc3eed8379e57c242aed9025b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb301d9b091785eb4757516ef3bf17cd12bdca993f2fbb983646d9fc0a343d1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c64735f7cd79dfcc4178b98f5a788da1a7de6c7346f1f81f78ae4bcd7cabae85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d4330a124172df0968cf6275d146797315e0a7ea95a3d9b1e3098c355bb876(
    value: typing.Optional[ComputeInstanceGroupManagerInstanceLifecyclePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a1f47208f8b27293e91cd1c63831429babf6a25a31e39cbfffa8c04f75a2940(
    *,
    name: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa9c1ff8faf52bde583c1c83bc28bbf41148499ddfa93655f4e920511b1992e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93461c18dd8e0fffdb3129f68408a1b22b178616afd13535fce70dd71d854b6a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5787bad7becb8abc528d7dc61c2522982daf0f6eb6bf41a25420a3fcd4f4c523(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c383aa5fce0e7d10b89d9b6563433bf72a9df0bf76bb65f115a27b30a885d74b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e0e910b2d459a886468ccc8f75b7afcdeb69c6400d7a9b04bbd850fa62dbe67(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87caaaa0b7cf288ade24647505151899acfdf142544f19f420eaff790103e68(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGroupManagerNamedPort]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8029ef149a2afb864524b38fd033f5d875a7d583aa52d0175eafe1148614079c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4807a861c92385bfcd2fc448fa64321ff746e97c114ed7d0eb9fdcbd6cc706ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77a0beb7ef7c597b6eec53313ff0bdf902f59981f09f8e9cd2f93b04f4264e4e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6161046932db128805649741d6de379684a98873b599a0d4a370e654c891ac8c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerNamedPort]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efdca6bc5c0e3a3a6e4da959db79bc2efd2b650a55575de8a73f0017bac563fe(
    *,
    workload_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405c76856c87db2394d1d10a6772f2fcf1f23de3234ecf8cf3c3d16f4f44cca7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ae4c12f77c6611082ee100d81b4e2d8a18787370d1d73a06fe27097d69f75d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75758dff4a15608dc9158c6cc9dbd165dfb64f9fd1093a2a5ff2cdc7c6962adb(
    value: typing.Optional[ComputeInstanceGroupManagerResourcePolicies],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c71baeb7fc5123330689489a93125eecf3d060452e718233d69ae287af80bd84(
    *,
    initial_delay_sec: typing.Optional[jsii.Number] = None,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ee98a8d9284dd50b291390d17d997857c197221bf9ecdfa3f65d1f5a62ca1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44df9f06ac4f7421d7cb00b456deabf6528bed3a62bbdca5c1f96faca62f5b6a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac57a6ed4b5b1e405eaaaf997411b8e4aeaa536bd04b4fd5c166e24536f3c493(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7bd536908e3832535671bb72a97f2d5d950ac9fa30fb751b4f4385ff2c93966(
    value: typing.Optional[ComputeInstanceGroupManagerStandbyPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c169366b4a6d755a1355d761ec329b6f340f89be84d2f6b2f00f0fa7141842(
    *,
    device_name: builtins.str,
    delete_rule: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8190def9750a27a015d6d21d5f64e42664c448bb5731a021ee85b652c423b01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec99d887cfd66db50da4d5e3451417eea9f3d8cd7918ff256e0a3bab93b86b5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d783f0faf8c7e72679354c8127573b3aefdeff96c2cf9789ffae067f20aed326(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c6e0c7a1ed3fbf802d05f78939d806169933f83104f42d260a83d20929c081e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e3a2b7e594ebc4187fc502a9111c9b6004cccd83893f20893a959d6212d6698(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adde6b8866be63b2a12f37184259f7157d3fd8294b817a2604e04abaafc62371(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGroupManagerStatefulDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5f4920fb2e74f4182e6b40d9e8c29acf15cc63d4352ade4b08a372828cbe444(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670f20c4bd293a2d0eeea8a489600fc0aabd27f5a6ea15d16e84e9a4941762f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee0b34b5dbc65fbd899300c3f4a4fbb1b77f365f652d41398d75bbfa2176298e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ce1535d0e59c9233eb5b8e38126e4d48b59fd95dadccd16d47335c58deaf6b3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerStatefulDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d6d3d9effe882552ba603c12e76df32006280609ff4722e4a4024eb5063747(
    *,
    delete_rule: typing.Optional[builtins.str] = None,
    interface_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29eca05db670ee8a5e3f70315cdcb21393549087c2d1fafc3a63c8d29b96e786(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce11e0576f9bff3ca2c7efa194eabadce183a945ad846a389b3d7702b0286913(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c4b7fa68f33572da234e3a3a4a87d2b4c417f0fb759204d8cb2311492472838(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31a8e649355f6f9d7e2c2568e603572e3003b7721ec242c2b8011119079ca10a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa6a80ba0ffc033d7293953c73b11a66ff4f93bd1a01920a7f4f6c21b21a939(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69562d87193ecc15aa0683eee96c075daaf3e5b053ecef1ac7aba06b422116bb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGroupManagerStatefulExternalIp]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1ce2a93eb47ccf23908e5fcda3d5cb5aa619e424b8df86052cbbb1f725147e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f3993ac615f8461b1e1154d75e6d02c6698726eb5f0045462da514831a85b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177f0931a5fc2a7da3691316b8159e8819d8b1cc9ad6eef4624ff55e1d2ff1a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b571548d80a9f4ebd2866066c1bf70c98de522ddfe449376a3ea5dfbca047a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerStatefulExternalIp]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d41df27b0351ef17024713b1740700c118e931b82971c4798bd8f28d3dcea67(
    *,
    delete_rule: typing.Optional[builtins.str] = None,
    interface_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3846fb9a8a308f36c0d3e9b9df6d5957d08aa7ae92101d683393a705331edb7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7911cc9403f1ee2f03f7d68db5da6d12cbc062f694fbe002604ab556a367dbea(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18952c6c9e4d1fd69616e49a172d87b954f085c7b99f728c60483e2b73d65763(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d203c0d8bc222f70ce92e6b30345bee7b52b913d286a73e429c072880e54a395(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a1ad6e94616ee8c579b7167137547909a7a430adac009139a6221958372af65(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed6b7f731f1c0f92441364337a09dc490415046b5378d97d73ddc502bcd53a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGroupManagerStatefulInternalIp]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f30deaf636d19d568cf5235c3deb44e9cb967f01fd27a1536d7f381e66d02923(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ffdb7247d51f27c9f6652492abdbc637f85af2e5cd529ca1264f8a6107bdf5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a1580580a656eb9f0f8efd0dc42add84b9ed4c6281fff45d28f44df52a5cfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49b50e9ca48394a65596aabbce05e4b516fe74ab2eea8cf74af37a9429510fdf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerStatefulInternalIp]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62a14a02543bf3b872db4e3bdd217678293618c579bfc2e7ceb003d21aa783f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b917d47a2f9fa1ba94b9448281821e7eba4b274dd67066dfb7459b5a2bd7a75e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aeb4aef1f474e7856f3d48efd3e7fee8e16a3489b8fcc91b645baf46347f26e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef53519611096be6cd966be51b8d960392dfffaac5f33abba47f202706a243c3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85f10faae748167f6062391e505c38e2fbe8cbae75637f7738d552a33080382(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee4cc380296e771830f5c77050a9a71366665b261f412af8cacd93617c4e5a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b24c1670fa28bb161ed9265eb4e4401e9a5ee7bc9ad34c563837b667a6f1b193(
    value: typing.Optional[ComputeInstanceGroupManagerStatusAllInstancesConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5773ffdc88f9e415e1e1a76471f1c11248808b89db505eee077ef5e0b179f063(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b2ba8513f84c8c1fbccffea2846934959adb02308cc549e9ddf07572753850d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb5de2b4f06501da76418526aec8996d649536065ad171ca45c97749c0819b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4bb7880016ef02c9b0649d16d6076ad6cd86ed143b9860750d500c38822300e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5293cb4337e5e6bcfc693fa410cf30a0e39237b7605aac5535a93ddc5cdf5f7f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60cafe0ae798f80429815e3427ecfb6da26ca450c6f592bf64541d6ba2e24672(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d16af710cfc2a9fb29013d27c1587875efe90c86800e419cb338f28420c2545(
    value: typing.Optional[ComputeInstanceGroupManagerStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9878efb940fcc6cf62486c3347ec4902ed38bccb71be93b98efea6727695acc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29becb9a3ca083884f99954da136e999750cf51d6b6d2b0e830aca0d491720b6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b14d7d1124c405d51d6cb693545177a512f6559f084d11e20afc8b6cd4da22e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ffb4e64b6e245e60f7a28d164ceb48f50cafdf2d379866833aafdab489a64a3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72396cec022d784918f812531bc1d86cbc7bf6fc5923e201ed9bd2f1ad3257d5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea333064502f515c1b203003081c9398da0afdc53f7cdbb77f3aa31c5af2db2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6323c019f12484af3516f8a9449332e762e194f73f7bc9ae79f32a3d05f3fed(
    value: typing.Optional[ComputeInstanceGroupManagerStatusStateful],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7388ecba87671f2750a8208adaae7ad7d707f9e36226404811d2f7c7a053804c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17eef301e1ad3259f9b38dd7c66af4d87faf359c271b81457b549dfe33e68c4a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec5bbd6ff7a21eef98aacf50304d7d88f0ed221229d664ed4793924ff8a9357c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8cb786b119a00776fc459324a41b6e8ac527e48cec84572d8b4a16fcb00aa00(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df259c52dd5c3e8d33008a3c54b7b909fdaaa1d5ff43f3462d1afb5aa1fb4ad5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f301b9515fc3bf519694f73be6623c195add2e28668a37afd3d549ee0dd973f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e444747d755d468bed194178ca8fd20476cb87f51e7f01585190a97dc7f6cb98(
    value: typing.Optional[ComputeInstanceGroupManagerStatusStatefulPerInstanceConfigs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4279b27076e40d7cf2f53a0da729af0b2b5990f2e008c6d0053f32a80fec42(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e61fea77efdecdba6db618988b0ebad86ca96fe7082a95071dd6f05e3543f309(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a7866dabcf84dc9f3c759e18bbf92aab709175ca974c9f1db4df5c9ad2db2ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d530b91478bdb122771147dcf1cae9521bf0617386156ed320a8faa6e35f99cf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de4b54680ede3f74ae5348020bd1ec7ec07d4f931c2e768d1eb3ff734cd97c56(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3968c10c291fcad34c6830e7acf092095ef0ea30ebdc412c7b677b78446ff92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8e0b0bc557a5d795ce50fbf26d5e9476dfdb4263e641192289ab15f0b169188(
    value: typing.Optional[ComputeInstanceGroupManagerStatusVersionTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b88f64b661ab0ba3b72e625202ee8af9a513960db903d3bea9afebfa05b20b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19dcd53ddac27603a1e788afa2200a3e684a5e6ba6c9fbe716b9b944f7c6df76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a42cf8277c04e632523c0a1c0f8296814f975b478522fe0df25b2e3f1b3d074(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae9ad15094a33a558b2a91d829836df9b37bb1ad1cf46a7112184164cc7c1e09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__234970722f2e0d96c11ae97b2042ab0cbf9ce509041a84688e498e044d8448c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc22ebc4aec9ec2868d27d70903e57dc3960d7ef38149e73dd73ef34e23f174(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae4926e65c420ed99306724ee04b965b43a015471ee406ce46471772f53d2103(
    *,
    minimal_action: builtins.str,
    type: builtins.str,
    max_surge_fixed: typing.Optional[jsii.Number] = None,
    max_surge_percent: typing.Optional[jsii.Number] = None,
    max_unavailable_fixed: typing.Optional[jsii.Number] = None,
    max_unavailable_percent: typing.Optional[jsii.Number] = None,
    most_disruptive_allowed_action: typing.Optional[builtins.str] = None,
    replacement_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f189854b7c36ba7b7e482692f357d1139472ce247f400f5f0e2725cefe335a7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e86a0bb61d06787a84eb64df294d82ef2df6dc92663296ec8b33e975f7994a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1039386f8093ea45d5c3e13255ee0f3b9cde8fd4f5be1aa64b8fbfdc55351a27(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0baf4318abea25cec7b83044b35fe5695e021d8ff603ca6e0fcbe78f573994d2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f44e6a28f622d2ce118f2d96543b92ce75b004288ca188842c417266a37de3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f13c84db6c6cc3a1577fd9607ac9554a55e538eb6b7f1eaa1f47591e3d0e3e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1546faf124a8dffbf158db285b1546944dff221245085a9c1838dab0da2c219(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcefaedb4841e7f868979ff7a2c1cf49dd77a192d9198ed89dd011e515250593(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cff75897d0ed390fcfea758a88024c6f9f5e5a32222e6e31931bac6ec8320f16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99f5c38e295c0b12e9d44cfdb377a6a8b435c46c0c7d0b863788a232fb9e35ec(
    value: typing.Optional[ComputeInstanceGroupManagerUpdatePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90779ac537ddd224c2a59cb8d81e4004483a770a56c3f54a3fd56a44339e80df(
    *,
    instance_template: builtins.str,
    name: typing.Optional[builtins.str] = None,
    target_size: typing.Optional[typing.Union[ComputeInstanceGroupManagerVersionTargetSize, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb791d993516df84feb19cf6824f7fa661eff126932258e28c5f0f7f5c4d0299(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4519493b9151539f21286321040d2a4c37fc6c121823b9184fda7698b8e53b3e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59fd52236e4ed5472c6f2261d86dbf66f1af8647475f42c097fee3298ca20e40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed80cf7bca02471b32d2f278ef58d057b2b530e9054eef1d6edf2d6c23be9c8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac7c6743e4221cb84c7ef14f84383724cff9782a39fcac06eeeb429c0d9d7888(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15a161e501e3523470b51fa6ce795742959e761c9dc31e54ca2e452cf3f61e5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGroupManagerVersion]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__054b14b75c3dc9a9f77abadf3904c9e07bc82664346646bf523adc5f01b0da0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fd202745481065254e4c50175906e4a66dfb0185f28d81821e07bbb77ff9855(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8699329e7fdd72e78e8547485a419a882aeab4cf318bb3fd2e07a5e662a4c21d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17abbd273563e1e1d4cb3681af0865fdd5c67ae604240b7ce30b8979a163d32b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGroupManagerVersion]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207a2a1d8444e1ac40dfe978be3a6126ba41e8f08c796e93a4111b64f1836dcf(
    *,
    fixed: typing.Optional[jsii.Number] = None,
    percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51a47b701f091d0aaf1acdd9cb21f3513d17d21cba279ad7eda0599b7afc8afa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2812b359a8f387ef3253a45bf7f763515fa225f1de0d415bb0c558d6e5363387(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15f7d4f82ba7ee79a9a950a1eebdf3660aebf59e0921c373e5219415c7dcea53(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7cd9de8fac3028022f2c3ea8548ac3a0986486800cae5cf43cf92184ba2eb92(
    value: typing.Optional[ComputeInstanceGroupManagerVersionTargetSize],
) -> None:
    """Type checking stubs"""
    pass
