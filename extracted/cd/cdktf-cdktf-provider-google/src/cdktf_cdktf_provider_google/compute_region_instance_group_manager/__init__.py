r'''
# `google_compute_region_instance_group_manager`

Refer to the Terraform Registry for docs: [`google_compute_region_instance_group_manager`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager).
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


class ComputeRegionInstanceGroupManager(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManager",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager google_compute_region_instance_group_manager}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        base_instance_name: builtins.str,
        name: builtins.str,
        version: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceGroupManagerVersion", typing.Dict[builtins.str, typing.Any]]]],
        all_instances_config: typing.Optional[typing.Union["ComputeRegionInstanceGroupManagerAllInstancesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_healing_policies: typing.Optional[typing.Union["ComputeRegionInstanceGroupManagerAutoHealingPolicies", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        distribution_policy_target_shape: typing.Optional[builtins.str] = None,
        distribution_policy_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_flexibility_policy: typing.Optional[typing.Union["ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_lifecycle_policy: typing.Optional[typing.Union["ComputeRegionInstanceGroupManagerInstanceLifecyclePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        list_managed_instances_results: typing.Optional[builtins.str] = None,
        named_port: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceGroupManagerNamedPort", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        standby_policy: typing.Optional[typing.Union["ComputeRegionInstanceGroupManagerStandbyPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        stateful_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceGroupManagerStatefulDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stateful_external_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceGroupManagerStatefulExternalIp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stateful_internal_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceGroupManagerStatefulInternalIp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_size: typing.Optional[jsii.Number] = None,
        target_stopped_size: typing.Optional[jsii.Number] = None,
        target_suspended_size: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionInstanceGroupManagerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        update_policy: typing.Optional[typing.Union["ComputeRegionInstanceGroupManagerUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        wait_for_instances: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        wait_for_instances_status: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager google_compute_region_instance_group_manager} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param base_instance_name: The base instance name to use for instances in this group. The value must be a valid RFC1035 name. Supported characters are lowercase letters, numbers, and hyphens (-). Instances are named by appending a hyphen and a random four-character string to the base instance name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#base_instance_name ComputeRegionInstanceGroupManager#base_instance_name}
        :param name: The name of the instance group manager. Must be 1-63 characters long and comply with RFC1035. Supported characters include lowercase letters, numbers, and hyphens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#name ComputeRegionInstanceGroupManager#name}
        :param version: version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#version ComputeRegionInstanceGroupManager#version}
        :param all_instances_config: all_instances_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#all_instances_config ComputeRegionInstanceGroupManager#all_instances_config}
        :param auto_healing_policies: auto_healing_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#auto_healing_policies ComputeRegionInstanceGroupManager#auto_healing_policies}
        :param description: An optional textual description of the instance group manager. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#description ComputeRegionInstanceGroupManager#description}
        :param distribution_policy_target_shape: The shape to which the group converges either proactively or on resize events (depending on the value set in updatePolicy.instanceRedistributionType). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#distribution_policy_target_shape ComputeRegionInstanceGroupManager#distribution_policy_target_shape}
        :param distribution_policy_zones: The distribution policy for this managed instance group. You can specify one or more values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#distribution_policy_zones ComputeRegionInstanceGroupManager#distribution_policy_zones}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#id ComputeRegionInstanceGroupManager#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_flexibility_policy: instance_flexibility_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#instance_flexibility_policy ComputeRegionInstanceGroupManager#instance_flexibility_policy}
        :param instance_lifecycle_policy: instance_lifecycle_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#instance_lifecycle_policy ComputeRegionInstanceGroupManager#instance_lifecycle_policy}
        :param list_managed_instances_results: Pagination behavior of the listManagedInstances API method for this managed instance group. Valid values are: "PAGELESS", "PAGINATED". If PAGELESS (default), Pagination is disabled for the group's listManagedInstances API method. maxResults and pageToken query parameters are ignored and all instances are returned in a single response. If PAGINATED, pagination is enabled, maxResults and pageToken query parameters are respected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#list_managed_instances_results ComputeRegionInstanceGroupManager#list_managed_instances_results}
        :param named_port: named_port block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#named_port ComputeRegionInstanceGroupManager#named_port}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#project ComputeRegionInstanceGroupManager#project}
        :param region: The region where the managed instance group resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#region ComputeRegionInstanceGroupManager#region}
        :param standby_policy: standby_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#standby_policy ComputeRegionInstanceGroupManager#standby_policy}
        :param stateful_disk: stateful_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#stateful_disk ComputeRegionInstanceGroupManager#stateful_disk}
        :param stateful_external_ip: stateful_external_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#stateful_external_ip ComputeRegionInstanceGroupManager#stateful_external_ip}
        :param stateful_internal_ip: stateful_internal_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#stateful_internal_ip ComputeRegionInstanceGroupManager#stateful_internal_ip}
        :param target_pools: The full URL of all target pools to which new instances in the group are added. Updating the target pools attribute does not affect existing instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#target_pools ComputeRegionInstanceGroupManager#target_pools}
        :param target_size: The target number of running instances for this managed instance group. This value should always be explicitly set unless this resource is attached to an autoscaler, in which case it should never be set. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#target_size ComputeRegionInstanceGroupManager#target_size}
        :param target_stopped_size: The target number of stopped instances for this managed instance group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#target_stopped_size ComputeRegionInstanceGroupManager#target_stopped_size}
        :param target_suspended_size: The target number of suspended instances for this managed instance group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#target_suspended_size ComputeRegionInstanceGroupManager#target_suspended_size}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#timeouts ComputeRegionInstanceGroupManager#timeouts}
        :param update_policy: update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#update_policy ComputeRegionInstanceGroupManager#update_policy}
        :param wait_for_instances: Whether to wait for all instances to be created/updated before returning. Note that if this is set to true and the operation does not succeed, Terraform will continue trying until it times out. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#wait_for_instances ComputeRegionInstanceGroupManager#wait_for_instances}
        :param wait_for_instances_status: When used with wait_for_instances specifies the status to wait for. When STABLE is specified this resource will wait until the instances are stable before returning. When UPDATED is set, it will wait for the version target to be reached and any per instance configs to be effective and all instances configs to be effective as well as all instances to be stable before returning. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#wait_for_instances_status ComputeRegionInstanceGroupManager#wait_for_instances_status}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4065c51ed41658e9d3260d07e3912725c78880f88e7766e115b069e26465709)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeRegionInstanceGroupManagerConfig(
            base_instance_name=base_instance_name,
            name=name,
            version=version,
            all_instances_config=all_instances_config,
            auto_healing_policies=auto_healing_policies,
            description=description,
            distribution_policy_target_shape=distribution_policy_target_shape,
            distribution_policy_zones=distribution_policy_zones,
            id=id,
            instance_flexibility_policy=instance_flexibility_policy,
            instance_lifecycle_policy=instance_lifecycle_policy,
            list_managed_instances_results=list_managed_instances_results,
            named_port=named_port,
            project=project,
            region=region,
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
        '''Generates CDKTF code for importing a ComputeRegionInstanceGroupManager resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeRegionInstanceGroupManager to import.
        :param import_from_id: The id of the existing ComputeRegionInstanceGroupManager that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeRegionInstanceGroupManager to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75749a063f0dd993a4c6ca08b8455f49c26975bfa267aa36831f972a55321433)
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
        :param labels: The label key-value pairs that you want to patch onto the instance,. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#labels ComputeRegionInstanceGroupManager#labels}
        :param metadata: The metadata key-value pairs that you want to patch onto the instance. For more information, see Project and instance metadata, Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#metadata ComputeRegionInstanceGroupManager#metadata}
        '''
        value = ComputeRegionInstanceGroupManagerAllInstancesConfig(
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
        :param health_check: The health check resource that signals autohealing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#health_check ComputeRegionInstanceGroupManager#health_check}
        :param initial_delay_sec: The number of seconds that the managed instance group waits before it applies autohealing policies to new instances or recently recreated instances. Between 0 and 3600. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#initial_delay_sec ComputeRegionInstanceGroupManager#initial_delay_sec}
        '''
        value = ComputeRegionInstanceGroupManagerAutoHealingPolicies(
            health_check=health_check, initial_delay_sec=initial_delay_sec
        )

        return typing.cast(None, jsii.invoke(self, "putAutoHealingPolicies", [value]))

    @jsii.member(jsii_name="putInstanceFlexibilityPolicy")
    def put_instance_flexibility_policy(
        self,
        *,
        instance_selections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param instance_selections: instance_selections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#instance_selections ComputeRegionInstanceGroupManager#instance_selections}
        '''
        value = ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy(
            instance_selections=instance_selections
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceFlexibilityPolicy", [value]))

    @jsii.member(jsii_name="putInstanceLifecyclePolicy")
    def put_instance_lifecycle_policy(
        self,
        *,
        default_action_on_failure: typing.Optional[builtins.str] = None,
        force_update_on_repair: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_action_on_failure: Default behavior for all instance or health check failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#default_action_on_failure ComputeRegionInstanceGroupManager#default_action_on_failure}
        :param force_update_on_repair: Specifies whether to apply the group's latest configuration when repairing a VM. Valid options are: YES, NO. If YES and you updated the group's instance template or per-instance configurations after the VM was created, then these changes are applied when VM is repaired. If NO (default), then updates are applied in accordance with the group's update policy type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#force_update_on_repair ComputeRegionInstanceGroupManager#force_update_on_repair}
        '''
        value = ComputeRegionInstanceGroupManagerInstanceLifecyclePolicy(
            default_action_on_failure=default_action_on_failure,
            force_update_on_repair=force_update_on_repair,
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceLifecyclePolicy", [value]))

    @jsii.member(jsii_name="putNamedPort")
    def put_named_port(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceGroupManagerNamedPort", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__611094a3d8a599ebb657bf50ba480772abe802ebeb6e84cbe5fa2b7fbd83d304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNamedPort", [value]))

    @jsii.member(jsii_name="putStandbyPolicy")
    def put_standby_policy(
        self,
        *,
        initial_delay_sec: typing.Optional[jsii.Number] = None,
        mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param initial_delay_sec: Specifies the number of seconds that the MIG should wait to suspend or stop a VM after that VM was created. The initial delay gives the initialization script the time to prepare your VM for a quick scale out. The value of initial delay must be between 0 and 3600 seconds. The default value is 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#initial_delay_sec ComputeRegionInstanceGroupManager#initial_delay_sec}
        :param mode: Defines how a MIG resumes or starts VMs from a standby pool when the group scales out. The default mode is "MANUAL". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#mode ComputeRegionInstanceGroupManager#mode}
        '''
        value = ComputeRegionInstanceGroupManagerStandbyPolicy(
            initial_delay_sec=initial_delay_sec, mode=mode
        )

        return typing.cast(None, jsii.invoke(self, "putStandbyPolicy", [value]))

    @jsii.member(jsii_name="putStatefulDisk")
    def put_stateful_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceGroupManagerStatefulDisk", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__662b5f5e9b46f14c60e4cce2313edca2bfdfe0a3216630814994a7165bdf8b49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStatefulDisk", [value]))

    @jsii.member(jsii_name="putStatefulExternalIp")
    def put_stateful_external_ip(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceGroupManagerStatefulExternalIp", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__458d730241c5393eb455946cb9809e4efe3d34eef050dc017c314b6e276d17f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStatefulExternalIp", [value]))

    @jsii.member(jsii_name="putStatefulInternalIp")
    def put_stateful_internal_ip(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceGroupManagerStatefulInternalIp", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f47924cc65884ef850024c7d33c30eff48176b76672febedaafad92eb7ec9331)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#create ComputeRegionInstanceGroupManager#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#delete ComputeRegionInstanceGroupManager#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#update ComputeRegionInstanceGroupManager#update}.
        '''
        value = ComputeRegionInstanceGroupManagerTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUpdatePolicy")
    def put_update_policy(
        self,
        *,
        minimal_action: builtins.str,
        type: builtins.str,
        instance_redistribution_type: typing.Optional[builtins.str] = None,
        max_surge_fixed: typing.Optional[jsii.Number] = None,
        max_surge_percent: typing.Optional[jsii.Number] = None,
        max_unavailable_fixed: typing.Optional[jsii.Number] = None,
        max_unavailable_percent: typing.Optional[jsii.Number] = None,
        most_disruptive_allowed_action: typing.Optional[builtins.str] = None,
        replacement_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param minimal_action: Minimal action to be taken on an instance. You can specify either NONE to forbid any actions, REFRESH to update without stopping instances, RESTART to restart existing instances or REPLACE to delete and create new instances from the target template. If you specify a REFRESH, the Updater will attempt to perform that action only. However, if the Updater determines that the minimal action you specify is not enough to perform the update, it might perform a more disruptive action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#minimal_action ComputeRegionInstanceGroupManager#minimal_action}
        :param type: The type of update process. You can specify either PROACTIVE so that the instance group manager proactively executes actions in order to bring instances to their target versions or OPPORTUNISTIC so that no action is proactively executed but the update will be performed as part of other actions (for example, resizes or recreateInstances calls). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#type ComputeRegionInstanceGroupManager#type}
        :param instance_redistribution_type: The instance redistribution policy for regional managed instance groups. Valid values are: "PROACTIVE", "NONE". If PROACTIVE (default), the group attempts to maintain an even distribution of VM instances across zones in the region. If NONE, proactive redistribution is disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#instance_redistribution_type ComputeRegionInstanceGroupManager#instance_redistribution_type}
        :param max_surge_fixed: Specifies a fixed number of VM instances. This must be a positive integer. Conflicts with max_surge_percent. Both cannot be 0 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#max_surge_fixed ComputeRegionInstanceGroupManager#max_surge_fixed}
        :param max_surge_percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Conflicts with max_surge_fixed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#max_surge_percent ComputeRegionInstanceGroupManager#max_surge_percent}
        :param max_unavailable_fixed: Specifies a fixed number of VM instances. This must be a positive integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#max_unavailable_fixed ComputeRegionInstanceGroupManager#max_unavailable_fixed}
        :param max_unavailable_percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#max_unavailable_percent ComputeRegionInstanceGroupManager#max_unavailable_percent}
        :param most_disruptive_allowed_action: Most disruptive action that is allowed to be taken on an instance. You can specify either NONE to forbid any actions, REFRESH to allow actions that do not need instance restart, RESTART to allow actions that can be applied without instance replacing or REPLACE to allow all possible actions. If the Updater determines that the minimal update action needed is more disruptive than most disruptive allowed action you specify it will not perform the update at all. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#most_disruptive_allowed_action ComputeRegionInstanceGroupManager#most_disruptive_allowed_action}
        :param replacement_method: The instance replacement method for regional managed instance groups. Valid values are: "RECREATE", "SUBSTITUTE". If SUBSTITUTE (default), the group replaces VM instances with new instances that have randomly generated names. If RECREATE, instance names are preserved. You must also set max_unavailable_fixed or max_unavailable_percent to be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#replacement_method ComputeRegionInstanceGroupManager#replacement_method}
        '''
        value = ComputeRegionInstanceGroupManagerUpdatePolicy(
            minimal_action=minimal_action,
            type=type,
            instance_redistribution_type=instance_redistribution_type,
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceGroupManagerVersion", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ef88e8628491e053ffedcdb84a6da9a5b186bc433b285d0a196d37150522ab2)
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

    @jsii.member(jsii_name="resetDistributionPolicyTargetShape")
    def reset_distribution_policy_target_shape(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDistributionPolicyTargetShape", []))

    @jsii.member(jsii_name="resetDistributionPolicyZones")
    def reset_distribution_policy_zones(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDistributionPolicyZones", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstanceFlexibilityPolicy")
    def reset_instance_flexibility_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceFlexibilityPolicy", []))

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

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    ) -> "ComputeRegionInstanceGroupManagerAllInstancesConfigOutputReference":
        return typing.cast("ComputeRegionInstanceGroupManagerAllInstancesConfigOutputReference", jsii.get(self, "allInstancesConfig"))

    @builtins.property
    @jsii.member(jsii_name="autoHealingPolicies")
    def auto_healing_policies(
        self,
    ) -> "ComputeRegionInstanceGroupManagerAutoHealingPoliciesOutputReference":
        return typing.cast("ComputeRegionInstanceGroupManagerAutoHealingPoliciesOutputReference", jsii.get(self, "autoHealingPolicies"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="fingerprint")
    def fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fingerprint"))

    @builtins.property
    @jsii.member(jsii_name="instanceFlexibilityPolicy")
    def instance_flexibility_policy(
        self,
    ) -> "ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyOutputReference":
        return typing.cast("ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyOutputReference", jsii.get(self, "instanceFlexibilityPolicy"))

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
    ) -> "ComputeRegionInstanceGroupManagerInstanceLifecyclePolicyOutputReference":
        return typing.cast("ComputeRegionInstanceGroupManagerInstanceLifecyclePolicyOutputReference", jsii.get(self, "instanceLifecyclePolicy"))

    @builtins.property
    @jsii.member(jsii_name="namedPort")
    def named_port(self) -> "ComputeRegionInstanceGroupManagerNamedPortList":
        return typing.cast("ComputeRegionInstanceGroupManagerNamedPortList", jsii.get(self, "namedPort"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="standbyPolicy")
    def standby_policy(
        self,
    ) -> "ComputeRegionInstanceGroupManagerStandbyPolicyOutputReference":
        return typing.cast("ComputeRegionInstanceGroupManagerStandbyPolicyOutputReference", jsii.get(self, "standbyPolicy"))

    @builtins.property
    @jsii.member(jsii_name="statefulDisk")
    def stateful_disk(self) -> "ComputeRegionInstanceGroupManagerStatefulDiskList":
        return typing.cast("ComputeRegionInstanceGroupManagerStatefulDiskList", jsii.get(self, "statefulDisk"))

    @builtins.property
    @jsii.member(jsii_name="statefulExternalIp")
    def stateful_external_ip(
        self,
    ) -> "ComputeRegionInstanceGroupManagerStatefulExternalIpList":
        return typing.cast("ComputeRegionInstanceGroupManagerStatefulExternalIpList", jsii.get(self, "statefulExternalIp"))

    @builtins.property
    @jsii.member(jsii_name="statefulInternalIp")
    def stateful_internal_ip(
        self,
    ) -> "ComputeRegionInstanceGroupManagerStatefulInternalIpList":
        return typing.cast("ComputeRegionInstanceGroupManagerStatefulInternalIpList", jsii.get(self, "statefulInternalIp"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "ComputeRegionInstanceGroupManagerStatusList":
        return typing.cast("ComputeRegionInstanceGroupManagerStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeRegionInstanceGroupManagerTimeoutsOutputReference":
        return typing.cast("ComputeRegionInstanceGroupManagerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updatePolicy")
    def update_policy(
        self,
    ) -> "ComputeRegionInstanceGroupManagerUpdatePolicyOutputReference":
        return typing.cast("ComputeRegionInstanceGroupManagerUpdatePolicyOutputReference", jsii.get(self, "updatePolicy"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> "ComputeRegionInstanceGroupManagerVersionList":
        return typing.cast("ComputeRegionInstanceGroupManagerVersionList", jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="allInstancesConfigInput")
    def all_instances_config_input(
        self,
    ) -> typing.Optional["ComputeRegionInstanceGroupManagerAllInstancesConfig"]:
        return typing.cast(typing.Optional["ComputeRegionInstanceGroupManagerAllInstancesConfig"], jsii.get(self, "allInstancesConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="autoHealingPoliciesInput")
    def auto_healing_policies_input(
        self,
    ) -> typing.Optional["ComputeRegionInstanceGroupManagerAutoHealingPolicies"]:
        return typing.cast(typing.Optional["ComputeRegionInstanceGroupManagerAutoHealingPolicies"], jsii.get(self, "autoHealingPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="baseInstanceNameInput")
    def base_instance_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseInstanceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="distributionPolicyTargetShapeInput")
    def distribution_policy_target_shape_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "distributionPolicyTargetShapeInput"))

    @builtins.property
    @jsii.member(jsii_name="distributionPolicyZonesInput")
    def distribution_policy_zones_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "distributionPolicyZonesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceFlexibilityPolicyInput")
    def instance_flexibility_policy_input(
        self,
    ) -> typing.Optional["ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy"]:
        return typing.cast(typing.Optional["ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy"], jsii.get(self, "instanceFlexibilityPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceLifecyclePolicyInput")
    def instance_lifecycle_policy_input(
        self,
    ) -> typing.Optional["ComputeRegionInstanceGroupManagerInstanceLifecyclePolicy"]:
        return typing.cast(typing.Optional["ComputeRegionInstanceGroupManagerInstanceLifecyclePolicy"], jsii.get(self, "instanceLifecyclePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="listManagedInstancesResultsInput")
    def list_managed_instances_results_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "listManagedInstancesResultsInput"))

    @builtins.property
    @jsii.member(jsii_name="namedPortInput")
    def named_port_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerNamedPort"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerNamedPort"]]], jsii.get(self, "namedPortInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="standbyPolicyInput")
    def standby_policy_input(
        self,
    ) -> typing.Optional["ComputeRegionInstanceGroupManagerStandbyPolicy"]:
        return typing.cast(typing.Optional["ComputeRegionInstanceGroupManagerStandbyPolicy"], jsii.get(self, "standbyPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="statefulDiskInput")
    def stateful_disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerStatefulDisk"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerStatefulDisk"]]], jsii.get(self, "statefulDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="statefulExternalIpInput")
    def stateful_external_ip_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerStatefulExternalIp"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerStatefulExternalIp"]]], jsii.get(self, "statefulExternalIpInput"))

    @builtins.property
    @jsii.member(jsii_name="statefulInternalIpInput")
    def stateful_internal_ip_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerStatefulInternalIp"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerStatefulInternalIp"]]], jsii.get(self, "statefulInternalIpInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionInstanceGroupManagerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionInstanceGroupManagerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="updatePolicyInput")
    def update_policy_input(
        self,
    ) -> typing.Optional["ComputeRegionInstanceGroupManagerUpdatePolicy"]:
        return typing.cast(typing.Optional["ComputeRegionInstanceGroupManagerUpdatePolicy"], jsii.get(self, "updatePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerVersion"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerVersion"]]], jsii.get(self, "versionInput"))

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
    @jsii.member(jsii_name="baseInstanceName")
    def base_instance_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseInstanceName"))

    @base_instance_name.setter
    def base_instance_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c59a3ba77515cd4e16790adb909244f696541fcc98bb60adbbd3b3187ffd5c76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseInstanceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cbef8153032c7e594a52b7d8b2c9c34de94ab65a6eb524c0d87795de9ecee49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="distributionPolicyTargetShape")
    def distribution_policy_target_shape(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "distributionPolicyTargetShape"))

    @distribution_policy_target_shape.setter
    def distribution_policy_target_shape(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5845fc82a61fe7947817748852d1090b1c5fa648e145514d1b3613d66c9b9bd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distributionPolicyTargetShape", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="distributionPolicyZones")
    def distribution_policy_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "distributionPolicyZones"))

    @distribution_policy_zones.setter
    def distribution_policy_zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__828a26b791c1691ac0a8b147347503f3566ece6f1f1cbfa5effef9837fd558a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distributionPolicyZones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f81627a0b2ea4e5bb5d77655b66902360b375d22025d30bb15754db90d910ef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="listManagedInstancesResults")
    def list_managed_instances_results(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "listManagedInstancesResults"))

    @list_managed_instances_results.setter
    def list_managed_instances_results(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7adf7a6df9ee46c9e8a16164a29cceb0762680596254884030ffa67a93cdd0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listManagedInstancesResults", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__799164b6e3e8e7df4f3f45629c45ffa9ddd81026e694f77d9e0bec5512f8b18e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e79a000b2d6578d4962607ac88efc6a23842aa12cfba18588d05ac2af327fde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f448ef44fdff489127d480c9f1cbab1acb204faa122965da8a1b16f0293dc5ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetPools")
    def target_pools(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetPools"))

    @target_pools.setter
    def target_pools(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfc5c1c40d5b7a1efebe884b894aa49278834ba84326332654e99e0474c2524c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetPools", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetSize")
    def target_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetSize"))

    @target_size.setter
    def target_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f3194f0c73664d948998e59313c8c0cda2eddf97e526c7ea2abec443065d0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetStoppedSize")
    def target_stopped_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetStoppedSize"))

    @target_stopped_size.setter
    def target_stopped_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42a83e540fd2041ec43f4e4ba53aa1f2b91f5a236cf0a74b6a800402f8af52cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetStoppedSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetSuspendedSize")
    def target_suspended_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetSuspendedSize"))

    @target_suspended_size.setter
    def target_suspended_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3629040b912959bc64760ebd3dbb333a937ce67ddd846bb3abe3cefca8ac1254)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcea18cb11a49e8e2bbe5a12481726e12647527b3ada18d55682c418b7a2d344)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="waitForInstancesStatus")
    def wait_for_instances_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "waitForInstancesStatus"))

    @wait_for_instances_status.setter
    def wait_for_instances_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ae2855ab0c4b87e0ce86661e4b512e6203a0570632b23e4939c8c92ed26d5a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForInstancesStatus", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerAllInstancesConfig",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels", "metadata": "metadata"},
)
class ComputeRegionInstanceGroupManagerAllInstancesConfig:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param labels: The label key-value pairs that you want to patch onto the instance,. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#labels ComputeRegionInstanceGroupManager#labels}
        :param metadata: The metadata key-value pairs that you want to patch onto the instance. For more information, see Project and instance metadata, Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#metadata ComputeRegionInstanceGroupManager#metadata}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68411701bfd29a1b2b806c01208799d2eb1ae0378f423051045f0c7c87e44e02)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#labels ComputeRegionInstanceGroupManager#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The metadata key-value pairs that you want to patch onto the instance.

        For more information, see Project and instance metadata,

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#metadata ComputeRegionInstanceGroupManager#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceGroupManagerAllInstancesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceGroupManagerAllInstancesConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerAllInstancesConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ae766d4598083b5d85dc29335bd549b7378405f924f47ce207f489b36c0fbcc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b50701d03db34d3d2cf3e5fb292565a8ad28454b691cf03cc717eefc43430e30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa3a844e877449dba23490e430adcf13fd915b3ef70821ac70c1633e1d047c2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceGroupManagerAllInstancesConfig]:
        return typing.cast(typing.Optional[ComputeRegionInstanceGroupManagerAllInstancesConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceGroupManagerAllInstancesConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__413f7e2d811776e0610168cc87a523c0673beea32eeba873e2dda3d192bb9a54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerAutoHealingPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "health_check": "healthCheck",
        "initial_delay_sec": "initialDelaySec",
    },
)
class ComputeRegionInstanceGroupManagerAutoHealingPolicies:
    def __init__(
        self,
        *,
        health_check: builtins.str,
        initial_delay_sec: jsii.Number,
    ) -> None:
        '''
        :param health_check: The health check resource that signals autohealing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#health_check ComputeRegionInstanceGroupManager#health_check}
        :param initial_delay_sec: The number of seconds that the managed instance group waits before it applies autohealing policies to new instances or recently recreated instances. Between 0 and 3600. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#initial_delay_sec ComputeRegionInstanceGroupManager#initial_delay_sec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2336b11ccaeee9d794c0baa83ee95edcd461091f2e14d3d8f3a861b1b74e1855)
            check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
            check_type(argname="argument initial_delay_sec", value=initial_delay_sec, expected_type=type_hints["initial_delay_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "health_check": health_check,
            "initial_delay_sec": initial_delay_sec,
        }

    @builtins.property
    def health_check(self) -> builtins.str:
        '''The health check resource that signals autohealing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#health_check ComputeRegionInstanceGroupManager#health_check}
        '''
        result = self._values.get("health_check")
        assert result is not None, "Required property 'health_check' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def initial_delay_sec(self) -> jsii.Number:
        '''The number of seconds that the managed instance group waits before it applies autohealing policies to new instances or recently recreated instances.

        Between 0 and 3600.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#initial_delay_sec ComputeRegionInstanceGroupManager#initial_delay_sec}
        '''
        result = self._values.get("initial_delay_sec")
        assert result is not None, "Required property 'initial_delay_sec' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceGroupManagerAutoHealingPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceGroupManagerAutoHealingPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerAutoHealingPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1d5d19c2f6ad26588364e6e729ddd57ff551a1c62901124f376e6430e442052)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f20e3fc7a12797757564466c4a046089e237ee187c1ad3f996ba8fb96c41a7a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelaySec")
    def initial_delay_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelaySec"))

    @initial_delay_sec.setter
    def initial_delay_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82959b128014fae2da7f2c81e8ba9e5a0127f65a1b6aa50f84cdfc4c191906d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelaySec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceGroupManagerAutoHealingPolicies]:
        return typing.cast(typing.Optional[ComputeRegionInstanceGroupManagerAutoHealingPolicies], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceGroupManagerAutoHealingPolicies],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73c797331672e11d2ccb3002011f51446072324a9a23057f67f183c14a7c63e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerConfig",
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
        "distribution_policy_target_shape": "distributionPolicyTargetShape",
        "distribution_policy_zones": "distributionPolicyZones",
        "id": "id",
        "instance_flexibility_policy": "instanceFlexibilityPolicy",
        "instance_lifecycle_policy": "instanceLifecyclePolicy",
        "list_managed_instances_results": "listManagedInstancesResults",
        "named_port": "namedPort",
        "project": "project",
        "region": "region",
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
    },
)
class ComputeRegionInstanceGroupManagerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        version: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceGroupManagerVersion", typing.Dict[builtins.str, typing.Any]]]],
        all_instances_config: typing.Optional[typing.Union[ComputeRegionInstanceGroupManagerAllInstancesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_healing_policies: typing.Optional[typing.Union[ComputeRegionInstanceGroupManagerAutoHealingPolicies, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        distribution_policy_target_shape: typing.Optional[builtins.str] = None,
        distribution_policy_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_flexibility_policy: typing.Optional[typing.Union["ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_lifecycle_policy: typing.Optional[typing.Union["ComputeRegionInstanceGroupManagerInstanceLifecyclePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        list_managed_instances_results: typing.Optional[builtins.str] = None,
        named_port: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceGroupManagerNamedPort", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        standby_policy: typing.Optional[typing.Union["ComputeRegionInstanceGroupManagerStandbyPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        stateful_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceGroupManagerStatefulDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stateful_external_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceGroupManagerStatefulExternalIp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stateful_internal_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceGroupManagerStatefulInternalIp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_size: typing.Optional[jsii.Number] = None,
        target_stopped_size: typing.Optional[jsii.Number] = None,
        target_suspended_size: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionInstanceGroupManagerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        update_policy: typing.Optional[typing.Union["ComputeRegionInstanceGroupManagerUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        wait_for_instances: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        wait_for_instances_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param base_instance_name: The base instance name to use for instances in this group. The value must be a valid RFC1035 name. Supported characters are lowercase letters, numbers, and hyphens (-). Instances are named by appending a hyphen and a random four-character string to the base instance name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#base_instance_name ComputeRegionInstanceGroupManager#base_instance_name}
        :param name: The name of the instance group manager. Must be 1-63 characters long and comply with RFC1035. Supported characters include lowercase letters, numbers, and hyphens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#name ComputeRegionInstanceGroupManager#name}
        :param version: version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#version ComputeRegionInstanceGroupManager#version}
        :param all_instances_config: all_instances_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#all_instances_config ComputeRegionInstanceGroupManager#all_instances_config}
        :param auto_healing_policies: auto_healing_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#auto_healing_policies ComputeRegionInstanceGroupManager#auto_healing_policies}
        :param description: An optional textual description of the instance group manager. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#description ComputeRegionInstanceGroupManager#description}
        :param distribution_policy_target_shape: The shape to which the group converges either proactively or on resize events (depending on the value set in updatePolicy.instanceRedistributionType). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#distribution_policy_target_shape ComputeRegionInstanceGroupManager#distribution_policy_target_shape}
        :param distribution_policy_zones: The distribution policy for this managed instance group. You can specify one or more values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#distribution_policy_zones ComputeRegionInstanceGroupManager#distribution_policy_zones}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#id ComputeRegionInstanceGroupManager#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_flexibility_policy: instance_flexibility_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#instance_flexibility_policy ComputeRegionInstanceGroupManager#instance_flexibility_policy}
        :param instance_lifecycle_policy: instance_lifecycle_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#instance_lifecycle_policy ComputeRegionInstanceGroupManager#instance_lifecycle_policy}
        :param list_managed_instances_results: Pagination behavior of the listManagedInstances API method for this managed instance group. Valid values are: "PAGELESS", "PAGINATED". If PAGELESS (default), Pagination is disabled for the group's listManagedInstances API method. maxResults and pageToken query parameters are ignored and all instances are returned in a single response. If PAGINATED, pagination is enabled, maxResults and pageToken query parameters are respected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#list_managed_instances_results ComputeRegionInstanceGroupManager#list_managed_instances_results}
        :param named_port: named_port block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#named_port ComputeRegionInstanceGroupManager#named_port}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#project ComputeRegionInstanceGroupManager#project}
        :param region: The region where the managed instance group resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#region ComputeRegionInstanceGroupManager#region}
        :param standby_policy: standby_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#standby_policy ComputeRegionInstanceGroupManager#standby_policy}
        :param stateful_disk: stateful_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#stateful_disk ComputeRegionInstanceGroupManager#stateful_disk}
        :param stateful_external_ip: stateful_external_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#stateful_external_ip ComputeRegionInstanceGroupManager#stateful_external_ip}
        :param stateful_internal_ip: stateful_internal_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#stateful_internal_ip ComputeRegionInstanceGroupManager#stateful_internal_ip}
        :param target_pools: The full URL of all target pools to which new instances in the group are added. Updating the target pools attribute does not affect existing instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#target_pools ComputeRegionInstanceGroupManager#target_pools}
        :param target_size: The target number of running instances for this managed instance group. This value should always be explicitly set unless this resource is attached to an autoscaler, in which case it should never be set. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#target_size ComputeRegionInstanceGroupManager#target_size}
        :param target_stopped_size: The target number of stopped instances for this managed instance group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#target_stopped_size ComputeRegionInstanceGroupManager#target_stopped_size}
        :param target_suspended_size: The target number of suspended instances for this managed instance group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#target_suspended_size ComputeRegionInstanceGroupManager#target_suspended_size}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#timeouts ComputeRegionInstanceGroupManager#timeouts}
        :param update_policy: update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#update_policy ComputeRegionInstanceGroupManager#update_policy}
        :param wait_for_instances: Whether to wait for all instances to be created/updated before returning. Note that if this is set to true and the operation does not succeed, Terraform will continue trying until it times out. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#wait_for_instances ComputeRegionInstanceGroupManager#wait_for_instances}
        :param wait_for_instances_status: When used with wait_for_instances specifies the status to wait for. When STABLE is specified this resource will wait until the instances are stable before returning. When UPDATED is set, it will wait for the version target to be reached and any per instance configs to be effective and all instances configs to be effective as well as all instances to be stable before returning. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#wait_for_instances_status ComputeRegionInstanceGroupManager#wait_for_instances_status}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(all_instances_config, dict):
            all_instances_config = ComputeRegionInstanceGroupManagerAllInstancesConfig(**all_instances_config)
        if isinstance(auto_healing_policies, dict):
            auto_healing_policies = ComputeRegionInstanceGroupManagerAutoHealingPolicies(**auto_healing_policies)
        if isinstance(instance_flexibility_policy, dict):
            instance_flexibility_policy = ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy(**instance_flexibility_policy)
        if isinstance(instance_lifecycle_policy, dict):
            instance_lifecycle_policy = ComputeRegionInstanceGroupManagerInstanceLifecyclePolicy(**instance_lifecycle_policy)
        if isinstance(standby_policy, dict):
            standby_policy = ComputeRegionInstanceGroupManagerStandbyPolicy(**standby_policy)
        if isinstance(timeouts, dict):
            timeouts = ComputeRegionInstanceGroupManagerTimeouts(**timeouts)
        if isinstance(update_policy, dict):
            update_policy = ComputeRegionInstanceGroupManagerUpdatePolicy(**update_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84aab6450f35bf2a79f6a26b6072fcdf845a8c5d6e67e56d177b4595b3d00ca1)
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
            check_type(argname="argument distribution_policy_target_shape", value=distribution_policy_target_shape, expected_type=type_hints["distribution_policy_target_shape"])
            check_type(argname="argument distribution_policy_zones", value=distribution_policy_zones, expected_type=type_hints["distribution_policy_zones"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_flexibility_policy", value=instance_flexibility_policy, expected_type=type_hints["instance_flexibility_policy"])
            check_type(argname="argument instance_lifecycle_policy", value=instance_lifecycle_policy, expected_type=type_hints["instance_lifecycle_policy"])
            check_type(argname="argument list_managed_instances_results", value=list_managed_instances_results, expected_type=type_hints["list_managed_instances_results"])
            check_type(argname="argument named_port", value=named_port, expected_type=type_hints["named_port"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
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
        if distribution_policy_target_shape is not None:
            self._values["distribution_policy_target_shape"] = distribution_policy_target_shape
        if distribution_policy_zones is not None:
            self._values["distribution_policy_zones"] = distribution_policy_zones
        if id is not None:
            self._values["id"] = id
        if instance_flexibility_policy is not None:
            self._values["instance_flexibility_policy"] = instance_flexibility_policy
        if instance_lifecycle_policy is not None:
            self._values["instance_lifecycle_policy"] = instance_lifecycle_policy
        if list_managed_instances_results is not None:
            self._values["list_managed_instances_results"] = list_managed_instances_results
        if named_port is not None:
            self._values["named_port"] = named_port
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#base_instance_name ComputeRegionInstanceGroupManager#base_instance_name}
        '''
        result = self._values.get("base_instance_name")
        assert result is not None, "Required property 'base_instance_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the instance group manager.

        Must be 1-63 characters long and comply with RFC1035. Supported characters include lowercase letters, numbers, and hyphens.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#name ComputeRegionInstanceGroupManager#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerVersion"]]:
        '''version block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#version ComputeRegionInstanceGroupManager#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerVersion"]], result)

    @builtins.property
    def all_instances_config(
        self,
    ) -> typing.Optional[ComputeRegionInstanceGroupManagerAllInstancesConfig]:
        '''all_instances_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#all_instances_config ComputeRegionInstanceGroupManager#all_instances_config}
        '''
        result = self._values.get("all_instances_config")
        return typing.cast(typing.Optional[ComputeRegionInstanceGroupManagerAllInstancesConfig], result)

    @builtins.property
    def auto_healing_policies(
        self,
    ) -> typing.Optional[ComputeRegionInstanceGroupManagerAutoHealingPolicies]:
        '''auto_healing_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#auto_healing_policies ComputeRegionInstanceGroupManager#auto_healing_policies}
        '''
        result = self._values.get("auto_healing_policies")
        return typing.cast(typing.Optional[ComputeRegionInstanceGroupManagerAutoHealingPolicies], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional textual description of the instance group manager.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#description ComputeRegionInstanceGroupManager#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def distribution_policy_target_shape(self) -> typing.Optional[builtins.str]:
        '''The shape to which the group converges either proactively or on resize events (depending on the value set in updatePolicy.instanceRedistributionType).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#distribution_policy_target_shape ComputeRegionInstanceGroupManager#distribution_policy_target_shape}
        '''
        result = self._values.get("distribution_policy_target_shape")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def distribution_policy_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The distribution policy for this managed instance group. You can specify one or more values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#distribution_policy_zones ComputeRegionInstanceGroupManager#distribution_policy_zones}
        '''
        result = self._values.get("distribution_policy_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#id ComputeRegionInstanceGroupManager#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_flexibility_policy(
        self,
    ) -> typing.Optional["ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy"]:
        '''instance_flexibility_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#instance_flexibility_policy ComputeRegionInstanceGroupManager#instance_flexibility_policy}
        '''
        result = self._values.get("instance_flexibility_policy")
        return typing.cast(typing.Optional["ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy"], result)

    @builtins.property
    def instance_lifecycle_policy(
        self,
    ) -> typing.Optional["ComputeRegionInstanceGroupManagerInstanceLifecyclePolicy"]:
        '''instance_lifecycle_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#instance_lifecycle_policy ComputeRegionInstanceGroupManager#instance_lifecycle_policy}
        '''
        result = self._values.get("instance_lifecycle_policy")
        return typing.cast(typing.Optional["ComputeRegionInstanceGroupManagerInstanceLifecyclePolicy"], result)

    @builtins.property
    def list_managed_instances_results(self) -> typing.Optional[builtins.str]:
        '''Pagination behavior of the listManagedInstances API method for this managed instance group.

        Valid values are: "PAGELESS", "PAGINATED". If PAGELESS (default), Pagination is disabled for the group's listManagedInstances API method. maxResults and pageToken query parameters are ignored and all instances are returned in a single response. If PAGINATED, pagination is enabled, maxResults and pageToken query parameters are respected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#list_managed_instances_results ComputeRegionInstanceGroupManager#list_managed_instances_results}
        '''
        result = self._values.get("list_managed_instances_results")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def named_port(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerNamedPort"]]]:
        '''named_port block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#named_port ComputeRegionInstanceGroupManager#named_port}
        '''
        result = self._values.get("named_port")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerNamedPort"]]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the resource belongs.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#project ComputeRegionInstanceGroupManager#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region where the managed instance group resides.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#region ComputeRegionInstanceGroupManager#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def standby_policy(
        self,
    ) -> typing.Optional["ComputeRegionInstanceGroupManagerStandbyPolicy"]:
        '''standby_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#standby_policy ComputeRegionInstanceGroupManager#standby_policy}
        '''
        result = self._values.get("standby_policy")
        return typing.cast(typing.Optional["ComputeRegionInstanceGroupManagerStandbyPolicy"], result)

    @builtins.property
    def stateful_disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerStatefulDisk"]]]:
        '''stateful_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#stateful_disk ComputeRegionInstanceGroupManager#stateful_disk}
        '''
        result = self._values.get("stateful_disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerStatefulDisk"]]], result)

    @builtins.property
    def stateful_external_ip(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerStatefulExternalIp"]]]:
        '''stateful_external_ip block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#stateful_external_ip ComputeRegionInstanceGroupManager#stateful_external_ip}
        '''
        result = self._values.get("stateful_external_ip")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerStatefulExternalIp"]]], result)

    @builtins.property
    def stateful_internal_ip(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerStatefulInternalIp"]]]:
        '''stateful_internal_ip block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#stateful_internal_ip ComputeRegionInstanceGroupManager#stateful_internal_ip}
        '''
        result = self._values.get("stateful_internal_ip")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerStatefulInternalIp"]]], result)

    @builtins.property
    def target_pools(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The full URL of all target pools to which new instances in the group are added.

        Updating the target pools attribute does not affect existing instances.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#target_pools ComputeRegionInstanceGroupManager#target_pools}
        '''
        result = self._values.get("target_pools")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target_size(self) -> typing.Optional[jsii.Number]:
        '''The target number of running instances for this managed instance group.

        This value should always be explicitly set unless this resource is attached to an autoscaler, in which case it should never be set. Defaults to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#target_size ComputeRegionInstanceGroupManager#target_size}
        '''
        result = self._values.get("target_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_stopped_size(self) -> typing.Optional[jsii.Number]:
        '''The target number of stopped instances for this managed instance group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#target_stopped_size ComputeRegionInstanceGroupManager#target_stopped_size}
        '''
        result = self._values.get("target_stopped_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_suspended_size(self) -> typing.Optional[jsii.Number]:
        '''The target number of suspended instances for this managed instance group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#target_suspended_size ComputeRegionInstanceGroupManager#target_suspended_size}
        '''
        result = self._values.get("target_suspended_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeRegionInstanceGroupManagerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#timeouts ComputeRegionInstanceGroupManager#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeRegionInstanceGroupManagerTimeouts"], result)

    @builtins.property
    def update_policy(
        self,
    ) -> typing.Optional["ComputeRegionInstanceGroupManagerUpdatePolicy"]:
        '''update_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#update_policy ComputeRegionInstanceGroupManager#update_policy}
        '''
        result = self._values.get("update_policy")
        return typing.cast(typing.Optional["ComputeRegionInstanceGroupManagerUpdatePolicy"], result)

    @builtins.property
    def wait_for_instances(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to wait for all instances to be created/updated before returning.

        Note that if this is set to true and the operation does not succeed, Terraform will continue trying until it times out.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#wait_for_instances ComputeRegionInstanceGroupManager#wait_for_instances}
        '''
        result = self._values.get("wait_for_instances")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def wait_for_instances_status(self) -> typing.Optional[builtins.str]:
        '''When used with wait_for_instances specifies the status to wait for.

        When STABLE is specified this resource will wait until the instances are stable before returning. When UPDATED is set, it will wait for the version target to be reached and any per instance configs to be effective and all instances configs to be effective as well as all instances to be stable before returning.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#wait_for_instances_status ComputeRegionInstanceGroupManager#wait_for_instances_status}
        '''
        result = self._values.get("wait_for_instances_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceGroupManagerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy",
    jsii_struct_bases=[],
    name_mapping={"instance_selections": "instanceSelections"},
)
class ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy:
    def __init__(
        self,
        *,
        instance_selections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param instance_selections: instance_selections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#instance_selections ComputeRegionInstanceGroupManager#instance_selections}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e59047334383ee794be5a73142ee50998a50ec93ca872668af8e63b13eccb67)
            check_type(argname="argument instance_selections", value=instance_selections, expected_type=type_hints["instance_selections"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_selections is not None:
            self._values["instance_selections"] = instance_selections

    @builtins.property
    def instance_selections(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections"]]]:
        '''instance_selections block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#instance_selections ComputeRegionInstanceGroupManager#instance_selections}
        '''
        result = self._values.get("instance_selections")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections",
    jsii_struct_bases=[],
    name_mapping={"machine_types": "machineTypes", "name": "name", "rank": "rank"},
)
class ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections:
    def __init__(
        self,
        *,
        machine_types: typing.Sequence[builtins.str],
        name: builtins.str,
        rank: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param machine_types: Full machine-type names, e.g. "n1-standard-16". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#machine_types ComputeRegionInstanceGroupManager#machine_types}
        :param name: Instance selection name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#name ComputeRegionInstanceGroupManager#name}
        :param rank: Preference of this instance selection. Lower number means higher preference. MIG will first try to create a VM based on the machine-type with lowest rank and fallback to next rank based on availability. Machine types and instance selections with the same rank have the same preference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#rank ComputeRegionInstanceGroupManager#rank}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6683a26c3f66131a666a8ea83dc95747bad3579f25484e3a97983a40b7cfd7ac)
            check_type(argname="argument machine_types", value=machine_types, expected_type=type_hints["machine_types"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rank", value=rank, expected_type=type_hints["rank"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "machine_types": machine_types,
            "name": name,
        }
        if rank is not None:
            self._values["rank"] = rank

    @builtins.property
    def machine_types(self) -> typing.List[builtins.str]:
        '''Full machine-type names, e.g. "n1-standard-16".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#machine_types ComputeRegionInstanceGroupManager#machine_types}
        '''
        result = self._values.get("machine_types")
        assert result is not None, "Required property 'machine_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Instance selection name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#name ComputeRegionInstanceGroupManager#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rank(self) -> typing.Optional[jsii.Number]:
        '''Preference of this instance selection.

        Lower number means higher preference. MIG will first try to create a VM based on the machine-type with lowest rank and fallback to next rank based on availability. Machine types and instance selections with the same rank have the same preference.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#rank ComputeRegionInstanceGroupManager#rank}
        '''
        result = self._values.get("rank")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a7e95fa2ae892bf0edb2be696fa59a788977444736e35cec90849ab891aae96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b56658c336b50de9f668135b85c9f9a50cea4a08cf4b25b971b6d7dbd450a3a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7789bede22557a43564551ab7d60f98e319adcbbbf8a33e98d6edfc7c7f1b0e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__787bf9ba91fe97f5cce436436d6a7191cd3de760519651d066d3d6e1d41de7eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cfa6e153c4f4ee69cd620a94d3deb4d93fdf841e5482168c95a186791b7a31b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69b894e0fea78d9e2e6b0a4a3f540ec77b5b4831987addae9f79b5599ce4769b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd74acb9083b46711a92459b7144445d201a8828e9313b76921d411002bf5bd5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetRank")
    def reset_rank(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRank", []))

    @builtins.property
    @jsii.member(jsii_name="machineTypesInput")
    def machine_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "machineTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="rankInput")
    def rank_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rankInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypes")
    def machine_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "machineTypes"))

    @machine_types.setter
    def machine_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74fbb1e8b36b96e2d8a221c9b344f02a218451a1565774f0735b1b9b83114691)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e7fdb29e6e97a27acd90001479d18b643f6f6e39dfab46ae654d95c920897f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rank")
    def rank(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rank"))

    @rank.setter
    def rank(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7e3996e400183010f311ecc67954957ae5acb91019ef95c21e71b8b756289e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rank", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c1d6baeec3f791500f829a0a8f1358755791999414e991b247deab670215ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7396235116e31c99ef807ccf52c76825261cfa0ce245cef8b7064dc47eb499da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInstanceSelections")
    def put_instance_selections(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b374680e04fe54a788f350dd0526c4fefa1adc8dc349df2be8e50cd965694a77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInstanceSelections", [value]))

    @jsii.member(jsii_name="resetInstanceSelections")
    def reset_instance_selections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceSelections", []))

    @builtins.property
    @jsii.member(jsii_name="instanceSelections")
    def instance_selections(
        self,
    ) -> ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelectionsList:
        return typing.cast(ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelectionsList, jsii.get(self, "instanceSelections"))

    @builtins.property
    @jsii.member(jsii_name="instanceSelectionsInput")
    def instance_selections_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections]]], jsii.get(self, "instanceSelectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy]:
        return typing.cast(typing.Optional[ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f50f173809c768d50da78d17b1f30d350bf06cdad27720a75a9df66d9244510)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerInstanceLifecyclePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "default_action_on_failure": "defaultActionOnFailure",
        "force_update_on_repair": "forceUpdateOnRepair",
    },
)
class ComputeRegionInstanceGroupManagerInstanceLifecyclePolicy:
    def __init__(
        self,
        *,
        default_action_on_failure: typing.Optional[builtins.str] = None,
        force_update_on_repair: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_action_on_failure: Default behavior for all instance or health check failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#default_action_on_failure ComputeRegionInstanceGroupManager#default_action_on_failure}
        :param force_update_on_repair: Specifies whether to apply the group's latest configuration when repairing a VM. Valid options are: YES, NO. If YES and you updated the group's instance template or per-instance configurations after the VM was created, then these changes are applied when VM is repaired. If NO (default), then updates are applied in accordance with the group's update policy type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#force_update_on_repair ComputeRegionInstanceGroupManager#force_update_on_repair}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c504f7285c501369c0c96d1486aa020d7c541e51d2aad24031956abd5696131d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#default_action_on_failure ComputeRegionInstanceGroupManager#default_action_on_failure}
        '''
        result = self._values.get("default_action_on_failure")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_update_on_repair(self) -> typing.Optional[builtins.str]:
        '''Specifies whether to apply the group's latest configuration when repairing a VM.

        Valid options are: YES, NO. If YES and you updated the group's instance template or per-instance configurations after the VM was created, then these changes are applied when VM is repaired. If NO (default), then updates are applied in accordance with the group's update policy type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#force_update_on_repair ComputeRegionInstanceGroupManager#force_update_on_repair}
        '''
        result = self._values.get("force_update_on_repair")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceGroupManagerInstanceLifecyclePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceGroupManagerInstanceLifecyclePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerInstanceLifecyclePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f0e8ad2df1741225d24c8f88b6247e057b5c6fb94f0b189a515a3b1d556f6bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e945cc613c9f778427bbc93c0dd72b4cc926dce356ad3bd49a9192dff879388)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultActionOnFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceUpdateOnRepair")
    def force_update_on_repair(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forceUpdateOnRepair"))

    @force_update_on_repair.setter
    def force_update_on_repair(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__663b3a9dd75e870b401d9aa4e365f0d48941d83ec8c673abbc61b4fb1f0ee5d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceUpdateOnRepair", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceGroupManagerInstanceLifecyclePolicy]:
        return typing.cast(typing.Optional[ComputeRegionInstanceGroupManagerInstanceLifecyclePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceGroupManagerInstanceLifecyclePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31b4f1a6c8fffcc42c97a3ab4bb7ab2d886e6f3272d4eabb66b523eb1dfd2203)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerNamedPort",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "port": "port"},
)
class ComputeRegionInstanceGroupManagerNamedPort:
    def __init__(self, *, name: builtins.str, port: jsii.Number) -> None:
        '''
        :param name: The name of the port. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#name ComputeRegionInstanceGroupManager#name}
        :param port: The port number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#port ComputeRegionInstanceGroupManager#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04ef21c4f8620c9febe1af17b0bed085c10f06f1b92b0786f2af2e4ce4c5280c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "port": port,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the port.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#name ComputeRegionInstanceGroupManager#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''The port number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#port ComputeRegionInstanceGroupManager#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceGroupManagerNamedPort(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceGroupManagerNamedPortList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerNamedPortList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5eb8f702aff85abf6eefae0aa53fe77424d34df21f541d48dff36d8b7c630501)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionInstanceGroupManagerNamedPortOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcbeaae926ec24cb6a9176a32d21e9bf6ddb98c59e771ab13dec7d5d3a4298c5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionInstanceGroupManagerNamedPortOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16a3e24969af70e965ecb03fbc8e45a29f1999770c933683442d7671a7acb156)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f886f347ccd0a4a3a40984cf0f0ef8c35bb1dd9b57c7482c20ee61fdf45dd1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad7d028aefb32e7cabbc0bc003f6b4a55c713f71305486e289df0465a9522a46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerNamedPort]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerNamedPort]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerNamedPort]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1381f5ea20ba8ef2a142a0d75f4f4a5814f13c5b0742eafe723546e69f172d08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceGroupManagerNamedPortOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerNamedPortOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eac4b5705103b40ff06944e07e6214d54864a2988b5e73bee6b6a433d0a68eea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b287e717f856e52697077547426da10e1e37cb51b5629f85eb07a8e6a27789e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02bc9618177c086f6a71e99e743cf025875a9c6d95a3ede3dc37f129494ef525)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerNamedPort]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerNamedPort]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerNamedPort]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b4b7d2977a7e3cb7dc9877b10df109175cd7cf247199ee2a51b22bf146a848c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStandbyPolicy",
    jsii_struct_bases=[],
    name_mapping={"initial_delay_sec": "initialDelaySec", "mode": "mode"},
)
class ComputeRegionInstanceGroupManagerStandbyPolicy:
    def __init__(
        self,
        *,
        initial_delay_sec: typing.Optional[jsii.Number] = None,
        mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param initial_delay_sec: Specifies the number of seconds that the MIG should wait to suspend or stop a VM after that VM was created. The initial delay gives the initialization script the time to prepare your VM for a quick scale out. The value of initial delay must be between 0 and 3600 seconds. The default value is 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#initial_delay_sec ComputeRegionInstanceGroupManager#initial_delay_sec}
        :param mode: Defines how a MIG resumes or starts VMs from a standby pool when the group scales out. The default mode is "MANUAL". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#mode ComputeRegionInstanceGroupManager#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c45065543ee2f01aa6babce2f32bb797f978d062fb2acfd6a9319c80e4a9e7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#initial_delay_sec ComputeRegionInstanceGroupManager#initial_delay_sec}
        '''
        result = self._values.get("initial_delay_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Defines how a MIG resumes or starts VMs from a standby pool when the group scales out.

        The default mode is "MANUAL".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#mode ComputeRegionInstanceGroupManager#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceGroupManagerStandbyPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceGroupManagerStandbyPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStandbyPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48e67981ab93fec997385e56aee4de3118bdf4929d17de16504c99ae1e21b138)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c50b080e442ee889970d21b0614f94b564a7812e3ba1d35c45139033b3f9a5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelaySec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6c0efd84a16b921f3266cc9a36eb4b21a674f00d07e209879a015e5defc6b0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceGroupManagerStandbyPolicy]:
        return typing.cast(typing.Optional[ComputeRegionInstanceGroupManagerStandbyPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceGroupManagerStandbyPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a92030dc22710cd93887748d80226c10a4b3af47baa3f19ce84f209453f2269)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatefulDisk",
    jsii_struct_bases=[],
    name_mapping={"device_name": "deviceName", "delete_rule": "deleteRule"},
)
class ComputeRegionInstanceGroupManagerStatefulDisk:
    def __init__(
        self,
        *,
        device_name: builtins.str,
        delete_rule: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param device_name: The device name of the disk to be attached. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#device_name ComputeRegionInstanceGroupManager#device_name}
        :param delete_rule: A value that prescribes what should happen to the stateful disk when the VM instance is deleted. The available options are NEVER and ON_PERMANENT_INSTANCE_DELETION. NEVER - detach the disk when the VM is deleted, but do not delete the disk. ON_PERMANENT_INSTANCE_DELETION will delete the stateful disk when the VM is permanently deleted from the instance group. The default is NEVER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#delete_rule ComputeRegionInstanceGroupManager#delete_rule}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc95e6ad94b29573bffa57fd79ace90675b9992d3dec3f2da9e3f4550b8474c0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#device_name ComputeRegionInstanceGroupManager#device_name}
        '''
        result = self._values.get("device_name")
        assert result is not None, "Required property 'device_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def delete_rule(self) -> typing.Optional[builtins.str]:
        '''A value that prescribes what should happen to the stateful disk when the VM instance is deleted.

        The available options are NEVER and ON_PERMANENT_INSTANCE_DELETION. NEVER - detach the disk when the VM is deleted, but do not delete the disk. ON_PERMANENT_INSTANCE_DELETION will delete the stateful disk when the VM is permanently deleted from the instance group. The default is NEVER.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#delete_rule ComputeRegionInstanceGroupManager#delete_rule}
        '''
        result = self._values.get("delete_rule")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceGroupManagerStatefulDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceGroupManagerStatefulDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatefulDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cae236344e58ceca76ccb9f1db67a634113e1f0ff29b778814cf63d7c874305c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionInstanceGroupManagerStatefulDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62c6ecc26a4f48f988fe41f21d61cec566c75b239900b499c5a2ca4cf861c8bb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionInstanceGroupManagerStatefulDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c214c98f711cc73d9bbf69e28f30b416b16a992f103f5e9cfb35dcbc4b39e5b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e7817131c07276010fd6b1c1a5ea4923b50a074605af7e7992f2d814b51e590)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbfc428b8a32786918cb3d959c213f3a6a01fa334f7c1e2aed04f086863aec58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerStatefulDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerStatefulDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerStatefulDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebbc1426bf69fadf481ac193ffab37f5e6b0d3630ee456dba5d42db97600fdc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceGroupManagerStatefulDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatefulDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e673c0172722557651adfb62a9fc8c4cd4a6402797839ace9b0bd8f9a7580b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e3365f4aec80b95db5acd2656b21a3b15a9eca8e28a0a66263d836816dca50c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteRule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceName")
    def device_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceName"))

    @device_name.setter
    def device_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22508d1a64dc13911458480d3676b8e4636036b8be4edb0441bdb881ab43c0c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerStatefulDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerStatefulDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerStatefulDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e32d8e7466334730855fce7ec6e8a6cd00f8b9e2a138028d1f0fe6d133170b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatefulExternalIp",
    jsii_struct_bases=[],
    name_mapping={"delete_rule": "deleteRule", "interface_name": "interfaceName"},
)
class ComputeRegionInstanceGroupManagerStatefulExternalIp:
    def __init__(
        self,
        *,
        delete_rule: typing.Optional[builtins.str] = None,
        interface_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delete_rule: A value that prescribes what should happen to an associated static Address resource when a VM instance is permanently deleted. The available options are NEVER and ON_PERMANENT_INSTANCE_DELETION. NEVER - detach the IP when the VM is deleted, but do not delete the address resource. ON_PERMANENT_INSTANCE_DELETION will delete the stateful address when the VM is permanently deleted from the instance group. The default is NEVER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#delete_rule ComputeRegionInstanceGroupManager#delete_rule}
        :param interface_name: The network interface name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#interface_name ComputeRegionInstanceGroupManager#interface_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a00e22444af7e59aa2464b7eaea1458682cb511125b1ba251c8ec6bfbb151918)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#delete_rule ComputeRegionInstanceGroupManager#delete_rule}
        '''
        result = self._values.get("delete_rule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interface_name(self) -> typing.Optional[builtins.str]:
        '''The network interface name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#interface_name ComputeRegionInstanceGroupManager#interface_name}
        '''
        result = self._values.get("interface_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceGroupManagerStatefulExternalIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceGroupManagerStatefulExternalIpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatefulExternalIpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__888310f9b6d2ea9fdac558a02bed78bfd48340793e8df28baa40664e76bd26a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionInstanceGroupManagerStatefulExternalIpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c3bdeb81bdc10f20ec84a6ca16a4faead4316210048513f61daa3c9d75bab49)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionInstanceGroupManagerStatefulExternalIpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ee1c3bb6c3fee8ff52d5bef20a9a13e726fa5830625eed96f7e49c41d116a4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a1f2194a4a976a882ac66c3187a33b2d4d0d34969ace59ce8d406cc6a44f450)
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
            type_hints = typing.get_type_hints(_typecheckingstub__699df0f9da6db6607c4d226414d8b76a5f37486daf05604d9fab1c6213430b90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerStatefulExternalIp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerStatefulExternalIp]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerStatefulExternalIp]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62d1ac0a3aa91ae0866e32bcf9ba833e71bbfb174f19144199e0277272a83c33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceGroupManagerStatefulExternalIpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatefulExternalIpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a34b160f8e16362a9d51a3c63699b86f06dc8881fdd98c2cdb5b58d88eef414c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cf97c65c28656575dfa86feffe04abf7f5314e452489aa36f55086d82b3572a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteRule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interfaceName")
    def interface_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interfaceName"))

    @interface_name.setter
    def interface_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d9e19d8f040678ba879d27d791e4fe6f507a0c5ca9ce08f504d8471aa289c90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interfaceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerStatefulExternalIp]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerStatefulExternalIp]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerStatefulExternalIp]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfbf96f48408d6338d146992d358985d0c240845741d10b1398b5409bc142547)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatefulInternalIp",
    jsii_struct_bases=[],
    name_mapping={"delete_rule": "deleteRule", "interface_name": "interfaceName"},
)
class ComputeRegionInstanceGroupManagerStatefulInternalIp:
    def __init__(
        self,
        *,
        delete_rule: typing.Optional[builtins.str] = None,
        interface_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delete_rule: A value that prescribes what should happen to an associated static Address resource when a VM instance is permanently deleted. The available options are NEVER and ON_PERMANENT_INSTANCE_DELETION. NEVER - detach the IP when the VM is deleted, but do not delete the address resource. ON_PERMANENT_INSTANCE_DELETION will delete the stateful address when the VM is permanently deleted from the instance group. The default is NEVER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#delete_rule ComputeRegionInstanceGroupManager#delete_rule}
        :param interface_name: The network interface name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#interface_name ComputeRegionInstanceGroupManager#interface_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51cadf038f944d88c00a8442a485f260bd38845551e78ccf6861e309a3fa434e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#delete_rule ComputeRegionInstanceGroupManager#delete_rule}
        '''
        result = self._values.get("delete_rule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interface_name(self) -> typing.Optional[builtins.str]:
        '''The network interface name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#interface_name ComputeRegionInstanceGroupManager#interface_name}
        '''
        result = self._values.get("interface_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceGroupManagerStatefulInternalIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceGroupManagerStatefulInternalIpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatefulInternalIpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43d86125f7cdd4c8f0ab9ee25bed589bd13c2539f445fce7a8d7b5a0c79190aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionInstanceGroupManagerStatefulInternalIpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64ddb93fa097463a38c92f7815f6d1a6091c5b09e11f091c96515eae348f24c8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionInstanceGroupManagerStatefulInternalIpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d6071626394f2c5017b131c6bc7f16ab7afe1e0725b1f266e398aa6915ad593)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cad7e46f7c0806cde1901ec244f2501e58ab8b40fd380901dc17c7c6e15cdd93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__984b3ed6c004ad82b22138ad5c409b44f1936d38d769142ff8b25e57d7179126)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerStatefulInternalIp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerStatefulInternalIp]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerStatefulInternalIp]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20e623acd973a3dc0849e1ab3aa87ec93fd9f753388323523883e740a3f7d834)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceGroupManagerStatefulInternalIpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatefulInternalIpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24a627244c149dc9a708d8010bdc6d47fb14b72edec3c8ba673d134c5d0d64ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60099ba751d4de3cb801b08721fdd412add6f0c98075ce56ab88f326a5d11ad6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteRule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interfaceName")
    def interface_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interfaceName"))

    @interface_name.setter
    def interface_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__240de0d7673e121f4e83ef08208a5795faa2a6bb9d422af6b5988c2ccfcf9515)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interfaceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerStatefulInternalIp]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerStatefulInternalIp]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerStatefulInternalIp]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6095c78061d5c260b0348e0de0f2b92c097bf16fcb9193f779624080abe1e099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeRegionInstanceGroupManagerStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceGroupManagerStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatusAllInstancesConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeRegionInstanceGroupManagerStatusAllInstancesConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceGroupManagerStatusAllInstancesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceGroupManagerStatusAllInstancesConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatusAllInstancesConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bef716785a53e51548567bb6e49d70ffbf040eff4b9ddcd02895bc22ab80e616)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionInstanceGroupManagerStatusAllInstancesConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a06802755f28b56a66a87a8e62766e7d00a55ea8cfb22c936ec022dfafa59fa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionInstanceGroupManagerStatusAllInstancesConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c74ab949b14ac6877a9cae0a4b1014b2053fd6d58d38e52b55918cb31018e9d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ca6b330d734b5bb241f2de39e2865b66f6aff4fdb03d5b7439e4fa4404f3083)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9efd637761569f91aef76bb66b5ac305b775a7c2c02db6a94e58ffac0e4c2085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceGroupManagerStatusAllInstancesConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatusAllInstancesConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2364dfc75803fd20977744c4408e4d3cca012252763ff958ce088e553892b8c0)
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
    ) -> typing.Optional[ComputeRegionInstanceGroupManagerStatusAllInstancesConfig]:
        return typing.cast(typing.Optional[ComputeRegionInstanceGroupManagerStatusAllInstancesConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceGroupManagerStatusAllInstancesConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93e14c67c10425def41aa14988561607c49b3e522f1a112132c0e4c181791c44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceGroupManagerStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11a5c1c525d0dbd33955f9969b18c820194ba325df750b29513aef6beeda32e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionInstanceGroupManagerStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c98f9d3d21f9a4aadb0591e34f3c353cc3d71edc1f7c547ce2518ef755f48340)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionInstanceGroupManagerStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da51701f31947b3b43bc26ca900d62986d1058531ab1402a6e8ca0d76d583d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97e1441bac0f4ccd64b0b0a40b622b131b2df3df0ee5fc78c5cd65739fbead9c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4226d2dddaeb3fe03513c0adcb6dd30bc969b4932deef042646d831af3fc1050)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceGroupManagerStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2825688ba8234e515dce66e65a93d4503f78bd6ef5a04440ea9a7bd4923a5b4a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allInstancesConfig")
    def all_instances_config(
        self,
    ) -> ComputeRegionInstanceGroupManagerStatusAllInstancesConfigList:
        return typing.cast(ComputeRegionInstanceGroupManagerStatusAllInstancesConfigList, jsii.get(self, "allInstancesConfig"))

    @builtins.property
    @jsii.member(jsii_name="isStable")
    def is_stable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isStable"))

    @builtins.property
    @jsii.member(jsii_name="stateful")
    def stateful(self) -> "ComputeRegionInstanceGroupManagerStatusStatefulList":
        return typing.cast("ComputeRegionInstanceGroupManagerStatusStatefulList", jsii.get(self, "stateful"))

    @builtins.property
    @jsii.member(jsii_name="versionTarget")
    def version_target(
        self,
    ) -> "ComputeRegionInstanceGroupManagerStatusVersionTargetList":
        return typing.cast("ComputeRegionInstanceGroupManagerStatusVersionTargetList", jsii.get(self, "versionTarget"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceGroupManagerStatus]:
        return typing.cast(typing.Optional[ComputeRegionInstanceGroupManagerStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceGroupManagerStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__548a6f608b857d1b8db6dd7bb93375fb9f703fd78f9ec0ad0923119b18da1c5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatusStateful",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeRegionInstanceGroupManagerStatusStateful:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceGroupManagerStatusStateful(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceGroupManagerStatusStatefulList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatusStatefulList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7defa6810ecdba162e17cfdf5524b31e27d39ee352e11b84adf58dc85169e622)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionInstanceGroupManagerStatusStatefulOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__101eb3b75e60f699e3bb55f9f00d55e03b246197356c5a0e4f5e728701531c4b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionInstanceGroupManagerStatusStatefulOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6997e5a2c408a43280067d2f9ec6222080905c2e0a39d9012c4df3c912b97a2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8def014f1793fbd390b02d106eb908faec95eda5a53bda88d63bd009be1d0ee8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__461b70596492e2112d0dc2c6d46cde609368f3bead91f5b2d8b642d6a6296bcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceGroupManagerStatusStatefulOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatusStatefulOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6394e5b4e260f6900bed2b23318bc9f97b359853878c0b41585a9fa1265ca9ca)
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
    ) -> "ComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigsList":
        return typing.cast("ComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigsList", jsii.get(self, "perInstanceConfigs"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceGroupManagerStatusStateful]:
        return typing.cast(typing.Optional[ComputeRegionInstanceGroupManagerStatusStateful], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceGroupManagerStatusStateful],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b60ec4080f8bf2589c245d708611cb9e0cb0deb56cfd83bfaa9b13db2b6767f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigs",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigs:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbe73bb154296bbe15f0ceb9bf30b6512404ec7caad3bd6933df4b6e182a232b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7da953ba67b8f17b4cb3a06f59d1e440ee743f8175a8ee2c000a99ec38b30cbd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__953aa61c262d20560ff1bf6bbae4126286fd18f53eff598e98696d2d5ed4d050)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f358e4cb567263eab8cdd5642aed3c5168297c244488f43941a4ba9a204f4b88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b6bbd01d709e292f4c7c04507f0bdb40b2ec83b8e22652489369bbbbb95bc35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7469f06ca2207983b280b57313e7b45bdb2281d4b8671c640a81ea4ee4f31851)
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
    ) -> typing.Optional[ComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigs]:
        return typing.cast(typing.Optional[ComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea435c88c7e2e59dbb0d5023e6815585acc2b27b9bc8162b9473b082a9bc376e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatusVersionTarget",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeRegionInstanceGroupManagerStatusVersionTarget:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceGroupManagerStatusVersionTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceGroupManagerStatusVersionTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatusVersionTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1438e1a74edf2ba98d7fb5116b55410e367963160e8d1fa29f75f15746de2881)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionInstanceGroupManagerStatusVersionTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4543efff8b3f7ef1c1bf1342be4a6bef3f4ee11534c0bbf7a4f941118c6747ee)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionInstanceGroupManagerStatusVersionTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf48df4ad0c446b0c85cb7b2f28e7bd0c80047bdcbffc04c97799ee77bdf889d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52749f0870b9bc326ba596644054b5070a74325569d8ceb2af8d2c5a6091c999)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0317f931096d57fca2eb8d9803855163905d2a8ce5ccb4c9fce28e933af5721)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceGroupManagerStatusVersionTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerStatusVersionTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac90faf059c1af877525944b2677a443a5268629dc2439202e72206e54fecc86)
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
    ) -> typing.Optional[ComputeRegionInstanceGroupManagerStatusVersionTarget]:
        return typing.cast(typing.Optional[ComputeRegionInstanceGroupManagerStatusVersionTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceGroupManagerStatusVersionTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d2f7a9e2337dcca3beb736703945d9333d2d2fdc6b1fd6592ba558d5cb65808)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeRegionInstanceGroupManagerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#create ComputeRegionInstanceGroupManager#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#delete ComputeRegionInstanceGroupManager#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#update ComputeRegionInstanceGroupManager#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e3760a4ec94087a92ac74187fcacec0480e34ed4af34498ceea7ca848689440)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#create ComputeRegionInstanceGroupManager#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#delete ComputeRegionInstanceGroupManager#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#update ComputeRegionInstanceGroupManager#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceGroupManagerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceGroupManagerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c318205cecf7cc8e6822d2b90fa9a7a1ccca1b3c3e3140f40de7a2a3eca9f520)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef917bd105b7a35cf4ac3121c5220ef6f1213059c35a38e7e5cd61fc657a4b5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fdf4bda5ba1d83905c19f4d86c312faa5fcc2fc70822515b40c1ef7ee922c18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__322e0dae3172edb6fc12dbd49ad93e174ec9b548831fbf3db2548bdeae1beb36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a69530e3daa9a8a52bd0fa81c8bf34fdb7190e8a7d19f9bd395e0e56ca0923bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerUpdatePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "minimal_action": "minimalAction",
        "type": "type",
        "instance_redistribution_type": "instanceRedistributionType",
        "max_surge_fixed": "maxSurgeFixed",
        "max_surge_percent": "maxSurgePercent",
        "max_unavailable_fixed": "maxUnavailableFixed",
        "max_unavailable_percent": "maxUnavailablePercent",
        "most_disruptive_allowed_action": "mostDisruptiveAllowedAction",
        "replacement_method": "replacementMethod",
    },
)
class ComputeRegionInstanceGroupManagerUpdatePolicy:
    def __init__(
        self,
        *,
        minimal_action: builtins.str,
        type: builtins.str,
        instance_redistribution_type: typing.Optional[builtins.str] = None,
        max_surge_fixed: typing.Optional[jsii.Number] = None,
        max_surge_percent: typing.Optional[jsii.Number] = None,
        max_unavailable_fixed: typing.Optional[jsii.Number] = None,
        max_unavailable_percent: typing.Optional[jsii.Number] = None,
        most_disruptive_allowed_action: typing.Optional[builtins.str] = None,
        replacement_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param minimal_action: Minimal action to be taken on an instance. You can specify either NONE to forbid any actions, REFRESH to update without stopping instances, RESTART to restart existing instances or REPLACE to delete and create new instances from the target template. If you specify a REFRESH, the Updater will attempt to perform that action only. However, if the Updater determines that the minimal action you specify is not enough to perform the update, it might perform a more disruptive action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#minimal_action ComputeRegionInstanceGroupManager#minimal_action}
        :param type: The type of update process. You can specify either PROACTIVE so that the instance group manager proactively executes actions in order to bring instances to their target versions or OPPORTUNISTIC so that no action is proactively executed but the update will be performed as part of other actions (for example, resizes or recreateInstances calls). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#type ComputeRegionInstanceGroupManager#type}
        :param instance_redistribution_type: The instance redistribution policy for regional managed instance groups. Valid values are: "PROACTIVE", "NONE". If PROACTIVE (default), the group attempts to maintain an even distribution of VM instances across zones in the region. If NONE, proactive redistribution is disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#instance_redistribution_type ComputeRegionInstanceGroupManager#instance_redistribution_type}
        :param max_surge_fixed: Specifies a fixed number of VM instances. This must be a positive integer. Conflicts with max_surge_percent. Both cannot be 0 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#max_surge_fixed ComputeRegionInstanceGroupManager#max_surge_fixed}
        :param max_surge_percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Conflicts with max_surge_fixed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#max_surge_percent ComputeRegionInstanceGroupManager#max_surge_percent}
        :param max_unavailable_fixed: Specifies a fixed number of VM instances. This must be a positive integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#max_unavailable_fixed ComputeRegionInstanceGroupManager#max_unavailable_fixed}
        :param max_unavailable_percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#max_unavailable_percent ComputeRegionInstanceGroupManager#max_unavailable_percent}
        :param most_disruptive_allowed_action: Most disruptive action that is allowed to be taken on an instance. You can specify either NONE to forbid any actions, REFRESH to allow actions that do not need instance restart, RESTART to allow actions that can be applied without instance replacing or REPLACE to allow all possible actions. If the Updater determines that the minimal update action needed is more disruptive than most disruptive allowed action you specify it will not perform the update at all. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#most_disruptive_allowed_action ComputeRegionInstanceGroupManager#most_disruptive_allowed_action}
        :param replacement_method: The instance replacement method for regional managed instance groups. Valid values are: "RECREATE", "SUBSTITUTE". If SUBSTITUTE (default), the group replaces VM instances with new instances that have randomly generated names. If RECREATE, instance names are preserved. You must also set max_unavailable_fixed or max_unavailable_percent to be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#replacement_method ComputeRegionInstanceGroupManager#replacement_method}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64b40b5af18b694b725c02909d2d0e977c86da5897c18f3fd65f2f51b9e9f599)
            check_type(argname="argument minimal_action", value=minimal_action, expected_type=type_hints["minimal_action"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument instance_redistribution_type", value=instance_redistribution_type, expected_type=type_hints["instance_redistribution_type"])
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
        if instance_redistribution_type is not None:
            self._values["instance_redistribution_type"] = instance_redistribution_type
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#minimal_action ComputeRegionInstanceGroupManager#minimal_action}
        '''
        result = self._values.get("minimal_action")
        assert result is not None, "Required property 'minimal_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of update process.

        You can specify either PROACTIVE so that the instance group manager proactively executes actions in order to bring instances to their target versions or OPPORTUNISTIC so that no action is proactively executed but the update will be performed as part of other actions (for example, resizes or recreateInstances calls).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#type ComputeRegionInstanceGroupManager#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_redistribution_type(self) -> typing.Optional[builtins.str]:
        '''The instance redistribution policy for regional managed instance groups.

        Valid values are: "PROACTIVE", "NONE". If PROACTIVE (default), the group attempts to maintain an even distribution of VM instances across zones in the region. If NONE, proactive redistribution is disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#instance_redistribution_type ComputeRegionInstanceGroupManager#instance_redistribution_type}
        '''
        result = self._values.get("instance_redistribution_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_surge_fixed(self) -> typing.Optional[jsii.Number]:
        '''Specifies a fixed number of VM instances.

        This must be a positive integer. Conflicts with max_surge_percent. Both cannot be 0

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#max_surge_fixed ComputeRegionInstanceGroupManager#max_surge_fixed}
        '''
        result = self._values.get("max_surge_fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_surge_percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Conflicts with max_surge_fixed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#max_surge_percent ComputeRegionInstanceGroupManager#max_surge_percent}
        '''
        result = self._values.get("max_surge_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_unavailable_fixed(self) -> typing.Optional[jsii.Number]:
        '''Specifies a fixed number of VM instances. This must be a positive integer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#max_unavailable_fixed ComputeRegionInstanceGroupManager#max_unavailable_fixed}
        '''
        result = self._values.get("max_unavailable_fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_unavailable_percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#max_unavailable_percent ComputeRegionInstanceGroupManager#max_unavailable_percent}
        '''
        result = self._values.get("max_unavailable_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def most_disruptive_allowed_action(self) -> typing.Optional[builtins.str]:
        '''Most disruptive action that is allowed to be taken on an instance.

        You can specify either NONE to forbid any actions, REFRESH to allow actions that do not need instance restart, RESTART to allow actions that can be applied without instance replacing or REPLACE to allow all possible actions. If the Updater determines that the minimal update action needed is more disruptive than most disruptive allowed action you specify it will not perform the update at all.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#most_disruptive_allowed_action ComputeRegionInstanceGroupManager#most_disruptive_allowed_action}
        '''
        result = self._values.get("most_disruptive_allowed_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replacement_method(self) -> typing.Optional[builtins.str]:
        '''The instance replacement method for regional managed instance groups.

        Valid values are: "RECREATE", "SUBSTITUTE". If SUBSTITUTE (default), the group replaces VM instances with new instances that have randomly generated names. If RECREATE, instance names are preserved.  You must also set max_unavailable_fixed or max_unavailable_percent to be greater than 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#replacement_method ComputeRegionInstanceGroupManager#replacement_method}
        '''
        result = self._values.get("replacement_method")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceGroupManagerUpdatePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceGroupManagerUpdatePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerUpdatePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3326c8b12a15447a1edebc3a416aa3167f37057373a78f93e4e664b32ac6decf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstanceRedistributionType")
    def reset_instance_redistribution_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceRedistributionType", []))

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
    @jsii.member(jsii_name="instanceRedistributionTypeInput")
    def instance_redistribution_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceRedistributionTypeInput"))

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
    @jsii.member(jsii_name="instanceRedistributionType")
    def instance_redistribution_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceRedistributionType"))

    @instance_redistribution_type.setter
    def instance_redistribution_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5255179a1f19570d5945d7c515116b272b274b73d533d05c12b91d321496116)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceRedistributionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxSurgeFixed")
    def max_surge_fixed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxSurgeFixed"))

    @max_surge_fixed.setter
    def max_surge_fixed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71844b870499c713a2b96163c568a6d4bd243c7f31b66d82ae4fcf8dc9e6dc47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSurgeFixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxSurgePercent")
    def max_surge_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxSurgePercent"))

    @max_surge_percent.setter
    def max_surge_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b11b3bcde35674e16f69a4d18536f5ccc5b06fa9ebc5ebec3577afe213f24605)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSurgePercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUnavailableFixed")
    def max_unavailable_fixed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUnavailableFixed"))

    @max_unavailable_fixed.setter
    def max_unavailable_fixed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cad4b0c37719ae46e6ba6bcc822a3d55dc741e5cbaad32a04611ff01345026da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUnavailableFixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUnavailablePercent")
    def max_unavailable_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUnavailablePercent"))

    @max_unavailable_percent.setter
    def max_unavailable_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3419169f3e50858a4cdacd741a0cfd2f2c62f1fd2aad1e8e3c91291a27d8213)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUnavailablePercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimalAction")
    def minimal_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimalAction"))

    @minimal_action.setter
    def minimal_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6abacf76e6d962f109a3dfc54d4c21566b1ed69f1b4ca923018f88ebf5e50e0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimalAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mostDisruptiveAllowedAction")
    def most_disruptive_allowed_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mostDisruptiveAllowedAction"))

    @most_disruptive_allowed_action.setter
    def most_disruptive_allowed_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d6d29cdf26edf599a941182ebe3461bbded469b69df15b42ba5cbadec8bb339)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mostDisruptiveAllowedAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replacementMethod")
    def replacement_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replacementMethod"))

    @replacement_method.setter
    def replacement_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a62e841cb63b494075dd03700f64844fb88fd3d785ba08079f402914e623cc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replacementMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__209daf1d269b80f9d7b1ae1b5b58be8e372c00024a355c8188b4fa3abbaf6a8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceGroupManagerUpdatePolicy]:
        return typing.cast(typing.Optional[ComputeRegionInstanceGroupManagerUpdatePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceGroupManagerUpdatePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b007a37d47148db10fba188acec401f56923e69fe23851bda15a949d1b65e4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerVersion",
    jsii_struct_bases=[],
    name_mapping={
        "instance_template": "instanceTemplate",
        "name": "name",
        "target_size": "targetSize",
    },
)
class ComputeRegionInstanceGroupManagerVersion:
    def __init__(
        self,
        *,
        instance_template: builtins.str,
        name: typing.Optional[builtins.str] = None,
        target_size: typing.Optional[typing.Union["ComputeRegionInstanceGroupManagerVersionTargetSize", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param instance_template: The full URL to an instance template from which all new instances of this version will be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#instance_template ComputeRegionInstanceGroupManager#instance_template}
        :param name: Version name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#name ComputeRegionInstanceGroupManager#name}
        :param target_size: target_size block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#target_size ComputeRegionInstanceGroupManager#target_size}
        '''
        if isinstance(target_size, dict):
            target_size = ComputeRegionInstanceGroupManagerVersionTargetSize(**target_size)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c61293fcc3cb91004c14d06c1817a0e4bfc39e5cb2e5f2db5e0137e0c61dbf0d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#instance_template ComputeRegionInstanceGroupManager#instance_template}
        '''
        result = self._values.get("instance_template")
        assert result is not None, "Required property 'instance_template' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Version name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#name ComputeRegionInstanceGroupManager#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_size(
        self,
    ) -> typing.Optional["ComputeRegionInstanceGroupManagerVersionTargetSize"]:
        '''target_size block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#target_size ComputeRegionInstanceGroupManager#target_size}
        '''
        result = self._values.get("target_size")
        return typing.cast(typing.Optional["ComputeRegionInstanceGroupManagerVersionTargetSize"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceGroupManagerVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceGroupManagerVersionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerVersionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78de44757aa2d5fc88694a75c95e9b5d4a0a6b13b2887953af7ac9837db670ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionInstanceGroupManagerVersionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61c1178300e5c7970d4004aa03c6ff5a0578ad44d6facfc4ba05195f802b321e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionInstanceGroupManagerVersionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb807f930abb7e24c62a7cd72266724e66004f54f7fad029ae932b13df55e9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6a43851730423625d477a55dae195f37dcf28fcfd64dc1aec78012c82bb434b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__765c7647384cfb1e3007f3b3ef39d20bee75ea1873110f7c4f8039220c71be68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerVersion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerVersion]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerVersion]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd79c16a0c2321b55cd6f757d2a4432519e2007bdb6e24f6d3167256a099eb3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceGroupManagerVersionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerVersionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7726ad0fe16faf3ba9fe89fd039081795c5104255c2d0b59f7a6e0deb9834a7f)
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
        :param fixed: The number of instances which are managed for this version. Conflicts with percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#fixed ComputeRegionInstanceGroupManager#fixed}
        :param percent: The number of instances (calculated as percentage) which are managed for this version. Conflicts with fixed. Note that when using percent, rounding will be in favor of explicitly set target_size values; a managed instance group with 2 instances and 2 versions, one of which has a target_size.percent of 60 will create 2 instances of that version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#percent ComputeRegionInstanceGroupManager#percent}
        '''
        value = ComputeRegionInstanceGroupManagerVersionTargetSize(
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
    ) -> "ComputeRegionInstanceGroupManagerVersionTargetSizeOutputReference":
        return typing.cast("ComputeRegionInstanceGroupManagerVersionTargetSizeOutputReference", jsii.get(self, "targetSize"))

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
    ) -> typing.Optional["ComputeRegionInstanceGroupManagerVersionTargetSize"]:
        return typing.cast(typing.Optional["ComputeRegionInstanceGroupManagerVersionTargetSize"], jsii.get(self, "targetSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTemplate")
    def instance_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceTemplate"))

    @instance_template.setter
    def instance_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d79743133689266501e3e5a99823a675be730758dc31c6890a1d5b2b96e47b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d966226d2c080e25fa8cdb6f2ceebc515ae199dff760ca3449a0e0af27afa99a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerVersion]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerVersion]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerVersion]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f26dcef16f8511eaee37a954c69d6f48e3caf9773b11a57e6164fe9a340558e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerVersionTargetSize",
    jsii_struct_bases=[],
    name_mapping={"fixed": "fixed", "percent": "percent"},
)
class ComputeRegionInstanceGroupManagerVersionTargetSize:
    def __init__(
        self,
        *,
        fixed: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed: The number of instances which are managed for this version. Conflicts with percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#fixed ComputeRegionInstanceGroupManager#fixed}
        :param percent: The number of instances (calculated as percentage) which are managed for this version. Conflicts with fixed. Note that when using percent, rounding will be in favor of explicitly set target_size values; a managed instance group with 2 instances and 2 versions, one of which has a target_size.percent of 60 will create 2 instances of that version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#percent ComputeRegionInstanceGroupManager#percent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8589d940b72d5c086b99090e153e1399c3397e2de7a947854f479ebd2efab085)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#fixed ComputeRegionInstanceGroupManager#fixed}
        '''
        result = self._values.get("fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percent(self) -> typing.Optional[jsii.Number]:
        '''The number of instances (calculated as percentage) which are managed for this version.

        Conflicts with fixed. Note that when using percent, rounding will be in favor of explicitly set target_size values; a managed instance group with 2 instances and 2 versions, one of which has a target_size.percent of 60 will create 2 instances of that version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_group_manager#percent ComputeRegionInstanceGroupManager#percent}
        '''
        result = self._values.get("percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceGroupManagerVersionTargetSize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceGroupManagerVersionTargetSizeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceGroupManager.ComputeRegionInstanceGroupManagerVersionTargetSizeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d903f3171fbbc8ee5b8afe09a1bf199e7cc46acc8a965be4d0ae394f8447478)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b31f8a68b07d0586c90bc0cb045d89814bb4a838a7c47c9cc6c3912d9546a4ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39bbaa57e037d8b1a6c4f74db11453782b4eff472e6132573ab478fe7dbe1452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceGroupManagerVersionTargetSize]:
        return typing.cast(typing.Optional[ComputeRegionInstanceGroupManagerVersionTargetSize], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceGroupManagerVersionTargetSize],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__052ba18424ca9a5caefb0bb60042447f2cd581fc4eb62ff32254b76ffc5a50ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeRegionInstanceGroupManager",
    "ComputeRegionInstanceGroupManagerAllInstancesConfig",
    "ComputeRegionInstanceGroupManagerAllInstancesConfigOutputReference",
    "ComputeRegionInstanceGroupManagerAutoHealingPolicies",
    "ComputeRegionInstanceGroupManagerAutoHealingPoliciesOutputReference",
    "ComputeRegionInstanceGroupManagerConfig",
    "ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy",
    "ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections",
    "ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelectionsList",
    "ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelectionsOutputReference",
    "ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyOutputReference",
    "ComputeRegionInstanceGroupManagerInstanceLifecyclePolicy",
    "ComputeRegionInstanceGroupManagerInstanceLifecyclePolicyOutputReference",
    "ComputeRegionInstanceGroupManagerNamedPort",
    "ComputeRegionInstanceGroupManagerNamedPortList",
    "ComputeRegionInstanceGroupManagerNamedPortOutputReference",
    "ComputeRegionInstanceGroupManagerStandbyPolicy",
    "ComputeRegionInstanceGroupManagerStandbyPolicyOutputReference",
    "ComputeRegionInstanceGroupManagerStatefulDisk",
    "ComputeRegionInstanceGroupManagerStatefulDiskList",
    "ComputeRegionInstanceGroupManagerStatefulDiskOutputReference",
    "ComputeRegionInstanceGroupManagerStatefulExternalIp",
    "ComputeRegionInstanceGroupManagerStatefulExternalIpList",
    "ComputeRegionInstanceGroupManagerStatefulExternalIpOutputReference",
    "ComputeRegionInstanceGroupManagerStatefulInternalIp",
    "ComputeRegionInstanceGroupManagerStatefulInternalIpList",
    "ComputeRegionInstanceGroupManagerStatefulInternalIpOutputReference",
    "ComputeRegionInstanceGroupManagerStatus",
    "ComputeRegionInstanceGroupManagerStatusAllInstancesConfig",
    "ComputeRegionInstanceGroupManagerStatusAllInstancesConfigList",
    "ComputeRegionInstanceGroupManagerStatusAllInstancesConfigOutputReference",
    "ComputeRegionInstanceGroupManagerStatusList",
    "ComputeRegionInstanceGroupManagerStatusOutputReference",
    "ComputeRegionInstanceGroupManagerStatusStateful",
    "ComputeRegionInstanceGroupManagerStatusStatefulList",
    "ComputeRegionInstanceGroupManagerStatusStatefulOutputReference",
    "ComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigs",
    "ComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigsList",
    "ComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigsOutputReference",
    "ComputeRegionInstanceGroupManagerStatusVersionTarget",
    "ComputeRegionInstanceGroupManagerStatusVersionTargetList",
    "ComputeRegionInstanceGroupManagerStatusVersionTargetOutputReference",
    "ComputeRegionInstanceGroupManagerTimeouts",
    "ComputeRegionInstanceGroupManagerTimeoutsOutputReference",
    "ComputeRegionInstanceGroupManagerUpdatePolicy",
    "ComputeRegionInstanceGroupManagerUpdatePolicyOutputReference",
    "ComputeRegionInstanceGroupManagerVersion",
    "ComputeRegionInstanceGroupManagerVersionList",
    "ComputeRegionInstanceGroupManagerVersionOutputReference",
    "ComputeRegionInstanceGroupManagerVersionTargetSize",
    "ComputeRegionInstanceGroupManagerVersionTargetSizeOutputReference",
]

publication.publish()

def _typecheckingstub__f4065c51ed41658e9d3260d07e3912725c78880f88e7766e115b069e26465709(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    base_instance_name: builtins.str,
    name: builtins.str,
    version: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceGroupManagerVersion, typing.Dict[builtins.str, typing.Any]]]],
    all_instances_config: typing.Optional[typing.Union[ComputeRegionInstanceGroupManagerAllInstancesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_healing_policies: typing.Optional[typing.Union[ComputeRegionInstanceGroupManagerAutoHealingPolicies, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    distribution_policy_target_shape: typing.Optional[builtins.str] = None,
    distribution_policy_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_flexibility_policy: typing.Optional[typing.Union[ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_lifecycle_policy: typing.Optional[typing.Union[ComputeRegionInstanceGroupManagerInstanceLifecyclePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    list_managed_instances_results: typing.Optional[builtins.str] = None,
    named_port: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceGroupManagerNamedPort, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    standby_policy: typing.Optional[typing.Union[ComputeRegionInstanceGroupManagerStandbyPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    stateful_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceGroupManagerStatefulDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stateful_external_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceGroupManagerStatefulExternalIp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stateful_internal_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceGroupManagerStatefulInternalIp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_size: typing.Optional[jsii.Number] = None,
    target_stopped_size: typing.Optional[jsii.Number] = None,
    target_suspended_size: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionInstanceGroupManagerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    update_policy: typing.Optional[typing.Union[ComputeRegionInstanceGroupManagerUpdatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    wait_for_instances: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    wait_for_instances_status: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__75749a063f0dd993a4c6ca08b8455f49c26975bfa267aa36831f972a55321433(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__611094a3d8a599ebb657bf50ba480772abe802ebeb6e84cbe5fa2b7fbd83d304(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceGroupManagerNamedPort, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662b5f5e9b46f14c60e4cce2313edca2bfdfe0a3216630814994a7165bdf8b49(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceGroupManagerStatefulDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__458d730241c5393eb455946cb9809e4efe3d34eef050dc017c314b6e276d17f1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceGroupManagerStatefulExternalIp, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f47924cc65884ef850024c7d33c30eff48176b76672febedaafad92eb7ec9331(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceGroupManagerStatefulInternalIp, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ef88e8628491e053ffedcdb84a6da9a5b186bc433b285d0a196d37150522ab2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceGroupManagerVersion, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c59a3ba77515cd4e16790adb909244f696541fcc98bb60adbbd3b3187ffd5c76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cbef8153032c7e594a52b7d8b2c9c34de94ab65a6eb524c0d87795de9ecee49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5845fc82a61fe7947817748852d1090b1c5fa648e145514d1b3613d66c9b9bd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828a26b791c1691ac0a8b147347503f3566ece6f1f1cbfa5effef9837fd558a4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81627a0b2ea4e5bb5d77655b66902360b375d22025d30bb15754db90d910ef8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7adf7a6df9ee46c9e8a16164a29cceb0762680596254884030ffa67a93cdd0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799164b6e3e8e7df4f3f45629c45ffa9ddd81026e694f77d9e0bec5512f8b18e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e79a000b2d6578d4962607ac88efc6a23842aa12cfba18588d05ac2af327fde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f448ef44fdff489127d480c9f1cbab1acb204faa122965da8a1b16f0293dc5ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc5c1c40d5b7a1efebe884b894aa49278834ba84326332654e99e0474c2524c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f3194f0c73664d948998e59313c8c0cda2eddf97e526c7ea2abec443065d0f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42a83e540fd2041ec43f4e4ba53aa1f2b91f5a236cf0a74b6a800402f8af52cf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3629040b912959bc64760ebd3dbb333a937ce67ddd846bb3abe3cefca8ac1254(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcea18cb11a49e8e2bbe5a12481726e12647527b3ada18d55682c418b7a2d344(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae2855ab0c4b87e0ce86661e4b512e6203a0570632b23e4939c8c92ed26d5a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68411701bfd29a1b2b806c01208799d2eb1ae0378f423051045f0c7c87e44e02(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae766d4598083b5d85dc29335bd549b7378405f924f47ce207f489b36c0fbcc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50701d03db34d3d2cf3e5fb292565a8ad28454b691cf03cc717eefc43430e30(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3a844e877449dba23490e430adcf13fd915b3ef70821ac70c1633e1d047c2d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__413f7e2d811776e0610168cc87a523c0673beea32eeba873e2dda3d192bb9a54(
    value: typing.Optional[ComputeRegionInstanceGroupManagerAllInstancesConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2336b11ccaeee9d794c0baa83ee95edcd461091f2e14d3d8f3a861b1b74e1855(
    *,
    health_check: builtins.str,
    initial_delay_sec: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d5d19c2f6ad26588364e6e729ddd57ff551a1c62901124f376e6430e442052(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f20e3fc7a12797757564466c4a046089e237ee187c1ad3f996ba8fb96c41a7a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82959b128014fae2da7f2c81e8ba9e5a0127f65a1b6aa50f84cdfc4c191906d3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c797331672e11d2ccb3002011f51446072324a9a23057f67f183c14a7c63e0(
    value: typing.Optional[ComputeRegionInstanceGroupManagerAutoHealingPolicies],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84aab6450f35bf2a79f6a26b6072fcdf845a8c5d6e67e56d177b4595b3d00ca1(
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
    version: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceGroupManagerVersion, typing.Dict[builtins.str, typing.Any]]]],
    all_instances_config: typing.Optional[typing.Union[ComputeRegionInstanceGroupManagerAllInstancesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_healing_policies: typing.Optional[typing.Union[ComputeRegionInstanceGroupManagerAutoHealingPolicies, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    distribution_policy_target_shape: typing.Optional[builtins.str] = None,
    distribution_policy_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_flexibility_policy: typing.Optional[typing.Union[ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_lifecycle_policy: typing.Optional[typing.Union[ComputeRegionInstanceGroupManagerInstanceLifecyclePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    list_managed_instances_results: typing.Optional[builtins.str] = None,
    named_port: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceGroupManagerNamedPort, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    standby_policy: typing.Optional[typing.Union[ComputeRegionInstanceGroupManagerStandbyPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    stateful_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceGroupManagerStatefulDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stateful_external_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceGroupManagerStatefulExternalIp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stateful_internal_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceGroupManagerStatefulInternalIp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_size: typing.Optional[jsii.Number] = None,
    target_stopped_size: typing.Optional[jsii.Number] = None,
    target_suspended_size: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionInstanceGroupManagerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    update_policy: typing.Optional[typing.Union[ComputeRegionInstanceGroupManagerUpdatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    wait_for_instances: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    wait_for_instances_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e59047334383ee794be5a73142ee50998a50ec93ca872668af8e63b13eccb67(
    *,
    instance_selections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6683a26c3f66131a666a8ea83dc95747bad3579f25484e3a97983a40b7cfd7ac(
    *,
    machine_types: typing.Sequence[builtins.str],
    name: builtins.str,
    rank: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a7e95fa2ae892bf0edb2be696fa59a788977444736e35cec90849ab891aae96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b56658c336b50de9f668135b85c9f9a50cea4a08cf4b25b971b6d7dbd450a3a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7789bede22557a43564551ab7d60f98e319adcbbbf8a33e98d6edfc7c7f1b0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787bf9ba91fe97f5cce436436d6a7191cd3de760519651d066d3d6e1d41de7eb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cfa6e153c4f4ee69cd620a94d3deb4d93fdf841e5482168c95a186791b7a31b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b894e0fea78d9e2e6b0a4a3f540ec77b5b4831987addae9f79b5599ce4769b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd74acb9083b46711a92459b7144445d201a8828e9313b76921d411002bf5bd5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74fbb1e8b36b96e2d8a221c9b344f02a218451a1565774f0735b1b9b83114691(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7fdb29e6e97a27acd90001479d18b643f6f6e39dfab46ae654d95c920897f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e3996e400183010f311ecc67954957ae5acb91019ef95c21e71b8b756289e7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c1d6baeec3f791500f829a0a8f1358755791999414e991b247deab670215ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7396235116e31c99ef807ccf52c76825261cfa0ce245cef8b7064dc47eb499da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b374680e04fe54a788f350dd0526c4fefa1adc8dc349df2be8e50cd965694a77(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f50f173809c768d50da78d17b1f30d350bf06cdad27720a75a9df66d9244510(
    value: typing.Optional[ComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c504f7285c501369c0c96d1486aa020d7c541e51d2aad24031956abd5696131d(
    *,
    default_action_on_failure: typing.Optional[builtins.str] = None,
    force_update_on_repair: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0e8ad2df1741225d24c8f88b6247e057b5c6fb94f0b189a515a3b1d556f6bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e945cc613c9f778427bbc93c0dd72b4cc926dce356ad3bd49a9192dff879388(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__663b3a9dd75e870b401d9aa4e365f0d48941d83ec8c673abbc61b4fb1f0ee5d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b4f1a6c8fffcc42c97a3ab4bb7ab2d886e6f3272d4eabb66b523eb1dfd2203(
    value: typing.Optional[ComputeRegionInstanceGroupManagerInstanceLifecyclePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ef21c4f8620c9febe1af17b0bed085c10f06f1b92b0786f2af2e4ce4c5280c(
    *,
    name: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb8f702aff85abf6eefae0aa53fe77424d34df21f541d48dff36d8b7c630501(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcbeaae926ec24cb6a9176a32d21e9bf6ddb98c59e771ab13dec7d5d3a4298c5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a3e24969af70e965ecb03fbc8e45a29f1999770c933683442d7671a7acb156(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f886f347ccd0a4a3a40984cf0f0ef8c35bb1dd9b57c7482c20ee61fdf45dd1b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7d028aefb32e7cabbc0bc003f6b4a55c713f71305486e289df0465a9522a46(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1381f5ea20ba8ef2a142a0d75f4f4a5814f13c5b0742eafe723546e69f172d08(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerNamedPort]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac4b5705103b40ff06944e07e6214d54864a2988b5e73bee6b6a433d0a68eea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b287e717f856e52697077547426da10e1e37cb51b5629f85eb07a8e6a27789e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02bc9618177c086f6a71e99e743cf025875a9c6d95a3ede3dc37f129494ef525(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b4b7d2977a7e3cb7dc9877b10df109175cd7cf247199ee2a51b22bf146a848c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerNamedPort]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c45065543ee2f01aa6babce2f32bb797f978d062fb2acfd6a9319c80e4a9e7(
    *,
    initial_delay_sec: typing.Optional[jsii.Number] = None,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48e67981ab93fec997385e56aee4de3118bdf4929d17de16504c99ae1e21b138(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c50b080e442ee889970d21b0614f94b564a7812e3ba1d35c45139033b3f9a5c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6c0efd84a16b921f3266cc9a36eb4b21a674f00d07e209879a015e5defc6b0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a92030dc22710cd93887748d80226c10a4b3af47baa3f19ce84f209453f2269(
    value: typing.Optional[ComputeRegionInstanceGroupManagerStandbyPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc95e6ad94b29573bffa57fd79ace90675b9992d3dec3f2da9e3f4550b8474c0(
    *,
    device_name: builtins.str,
    delete_rule: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae236344e58ceca76ccb9f1db67a634113e1f0ff29b778814cf63d7c874305c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c6ecc26a4f48f988fe41f21d61cec566c75b239900b499c5a2ca4cf861c8bb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c214c98f711cc73d9bbf69e28f30b416b16a992f103f5e9cfb35dcbc4b39e5b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e7817131c07276010fd6b1c1a5ea4923b50a074605af7e7992f2d814b51e590(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbfc428b8a32786918cb3d959c213f3a6a01fa334f7c1e2aed04f086863aec58(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebbc1426bf69fadf481ac193ffab37f5e6b0d3630ee456dba5d42db97600fdc4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerStatefulDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e673c0172722557651adfb62a9fc8c4cd4a6402797839ace9b0bd8f9a7580b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3365f4aec80b95db5acd2656b21a3b15a9eca8e28a0a66263d836816dca50c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22508d1a64dc13911458480d3676b8e4636036b8be4edb0441bdb881ab43c0c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e32d8e7466334730855fce7ec6e8a6cd00f8b9e2a138028d1f0fe6d133170b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerStatefulDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a00e22444af7e59aa2464b7eaea1458682cb511125b1ba251c8ec6bfbb151918(
    *,
    delete_rule: typing.Optional[builtins.str] = None,
    interface_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__888310f9b6d2ea9fdac558a02bed78bfd48340793e8df28baa40664e76bd26a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c3bdeb81bdc10f20ec84a6ca16a4faead4316210048513f61daa3c9d75bab49(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ee1c3bb6c3fee8ff52d5bef20a9a13e726fa5830625eed96f7e49c41d116a4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a1f2194a4a976a882ac66c3187a33b2d4d0d34969ace59ce8d406cc6a44f450(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__699df0f9da6db6607c4d226414d8b76a5f37486daf05604d9fab1c6213430b90(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d1ac0a3aa91ae0866e32bcf9ba833e71bbfb174f19144199e0277272a83c33(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerStatefulExternalIp]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34b160f8e16362a9d51a3c63699b86f06dc8881fdd98c2cdb5b58d88eef414c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf97c65c28656575dfa86feffe04abf7f5314e452489aa36f55086d82b3572a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d9e19d8f040678ba879d27d791e4fe6f507a0c5ca9ce08f504d8471aa289c90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfbf96f48408d6338d146992d358985d0c240845741d10b1398b5409bc142547(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerStatefulExternalIp]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51cadf038f944d88c00a8442a485f260bd38845551e78ccf6861e309a3fa434e(
    *,
    delete_rule: typing.Optional[builtins.str] = None,
    interface_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43d86125f7cdd4c8f0ab9ee25bed589bd13c2539f445fce7a8d7b5a0c79190aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ddb93fa097463a38c92f7815f6d1a6091c5b09e11f091c96515eae348f24c8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d6071626394f2c5017b131c6bc7f16ab7afe1e0725b1f266e398aa6915ad593(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cad7e46f7c0806cde1901ec244f2501e58ab8b40fd380901dc17c7c6e15cdd93(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__984b3ed6c004ad82b22138ad5c409b44f1936d38d769142ff8b25e57d7179126(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e623acd973a3dc0849e1ab3aa87ec93fd9f753388323523883e740a3f7d834(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerStatefulInternalIp]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a627244c149dc9a708d8010bdc6d47fb14b72edec3c8ba673d134c5d0d64ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60099ba751d4de3cb801b08721fdd412add6f0c98075ce56ab88f326a5d11ad6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__240de0d7673e121f4e83ef08208a5795faa2a6bb9d422af6b5988c2ccfcf9515(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6095c78061d5c260b0348e0de0f2b92c097bf16fcb9193f779624080abe1e099(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerStatefulInternalIp]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef716785a53e51548567bb6e49d70ffbf040eff4b9ddcd02895bc22ab80e616(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a06802755f28b56a66a87a8e62766e7d00a55ea8cfb22c936ec022dfafa59fa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c74ab949b14ac6877a9cae0a4b1014b2053fd6d58d38e52b55918cb31018e9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca6b330d734b5bb241f2de39e2865b66f6aff4fdb03d5b7439e4fa4404f3083(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9efd637761569f91aef76bb66b5ac305b775a7c2c02db6a94e58ffac0e4c2085(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2364dfc75803fd20977744c4408e4d3cca012252763ff958ce088e553892b8c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e14c67c10425def41aa14988561607c49b3e522f1a112132c0e4c181791c44(
    value: typing.Optional[ComputeRegionInstanceGroupManagerStatusAllInstancesConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a5c1c525d0dbd33955f9969b18c820194ba325df750b29513aef6beeda32e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c98f9d3d21f9a4aadb0591e34f3c353cc3d71edc1f7c547ce2518ef755f48340(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da51701f31947b3b43bc26ca900d62986d1058531ab1402a6e8ca0d76d583d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97e1441bac0f4ccd64b0b0a40b622b131b2df3df0ee5fc78c5cd65739fbead9c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4226d2dddaeb3fe03513c0adcb6dd30bc969b4932deef042646d831af3fc1050(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2825688ba8234e515dce66e65a93d4503f78bd6ef5a04440ea9a7bd4923a5b4a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__548a6f608b857d1b8db6dd7bb93375fb9f703fd78f9ec0ad0923119b18da1c5e(
    value: typing.Optional[ComputeRegionInstanceGroupManagerStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7defa6810ecdba162e17cfdf5524b31e27d39ee352e11b84adf58dc85169e622(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101eb3b75e60f699e3bb55f9f00d55e03b246197356c5a0e4f5e728701531c4b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6997e5a2c408a43280067d2f9ec6222080905c2e0a39d9012c4df3c912b97a2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8def014f1793fbd390b02d106eb908faec95eda5a53bda88d63bd009be1d0ee8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__461b70596492e2112d0dc2c6d46cde609368f3bead91f5b2d8b642d6a6296bcf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6394e5b4e260f6900bed2b23318bc9f97b359853878c0b41585a9fa1265ca9ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b60ec4080f8bf2589c245d708611cb9e0cb0deb56cfd83bfaa9b13db2b6767f(
    value: typing.Optional[ComputeRegionInstanceGroupManagerStatusStateful],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe73bb154296bbe15f0ceb9bf30b6512404ec7caad3bd6933df4b6e182a232b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7da953ba67b8f17b4cb3a06f59d1e440ee743f8175a8ee2c000a99ec38b30cbd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__953aa61c262d20560ff1bf6bbae4126286fd18f53eff598e98696d2d5ed4d050(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f358e4cb567263eab8cdd5642aed3c5168297c244488f43941a4ba9a204f4b88(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6bbd01d709e292f4c7c04507f0bdb40b2ec83b8e22652489369bbbbb95bc35(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7469f06ca2207983b280b57313e7b45bdb2281d4b8671c640a81ea4ee4f31851(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea435c88c7e2e59dbb0d5023e6815585acc2b27b9bc8162b9473b082a9bc376e(
    value: typing.Optional[ComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1438e1a74edf2ba98d7fb5116b55410e367963160e8d1fa29f75f15746de2881(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4543efff8b3f7ef1c1bf1342be4a6bef3f4ee11534c0bbf7a4f941118c6747ee(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf48df4ad0c446b0c85cb7b2f28e7bd0c80047bdcbffc04c97799ee77bdf889d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52749f0870b9bc326ba596644054b5070a74325569d8ceb2af8d2c5a6091c999(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0317f931096d57fca2eb8d9803855163905d2a8ce5ccb4c9fce28e933af5721(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac90faf059c1af877525944b2677a443a5268629dc2439202e72206e54fecc86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d2f7a9e2337dcca3beb736703945d9333d2d2fdc6b1fd6592ba558d5cb65808(
    value: typing.Optional[ComputeRegionInstanceGroupManagerStatusVersionTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3760a4ec94087a92ac74187fcacec0480e34ed4af34498ceea7ca848689440(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c318205cecf7cc8e6822d2b90fa9a7a1ccca1b3c3e3140f40de7a2a3eca9f520(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef917bd105b7a35cf4ac3121c5220ef6f1213059c35a38e7e5cd61fc657a4b5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fdf4bda5ba1d83905c19f4d86c312faa5fcc2fc70822515b40c1ef7ee922c18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__322e0dae3172edb6fc12dbd49ad93e174ec9b548831fbf3db2548bdeae1beb36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a69530e3daa9a8a52bd0fa81c8bf34fdb7190e8a7d19f9bd395e0e56ca0923bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b40b5af18b694b725c02909d2d0e977c86da5897c18f3fd65f2f51b9e9f599(
    *,
    minimal_action: builtins.str,
    type: builtins.str,
    instance_redistribution_type: typing.Optional[builtins.str] = None,
    max_surge_fixed: typing.Optional[jsii.Number] = None,
    max_surge_percent: typing.Optional[jsii.Number] = None,
    max_unavailable_fixed: typing.Optional[jsii.Number] = None,
    max_unavailable_percent: typing.Optional[jsii.Number] = None,
    most_disruptive_allowed_action: typing.Optional[builtins.str] = None,
    replacement_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3326c8b12a15447a1edebc3a416aa3167f37057373a78f93e4e664b32ac6decf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5255179a1f19570d5945d7c515116b272b274b73d533d05c12b91d321496116(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71844b870499c713a2b96163c568a6d4bd243c7f31b66d82ae4fcf8dc9e6dc47(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11b3bcde35674e16f69a4d18536f5ccc5b06fa9ebc5ebec3577afe213f24605(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cad4b0c37719ae46e6ba6bcc822a3d55dc741e5cbaad32a04611ff01345026da(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3419169f3e50858a4cdacd741a0cfd2f2c62f1fd2aad1e8e3c91291a27d8213(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6abacf76e6d962f109a3dfc54d4c21566b1ed69f1b4ca923018f88ebf5e50e0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6d29cdf26edf599a941182ebe3461bbded469b69df15b42ba5cbadec8bb339(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a62e841cb63b494075dd03700f64844fb88fd3d785ba08079f402914e623cc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__209daf1d269b80f9d7b1ae1b5b58be8e372c00024a355c8188b4fa3abbaf6a8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b007a37d47148db10fba188acec401f56923e69fe23851bda15a949d1b65e4c(
    value: typing.Optional[ComputeRegionInstanceGroupManagerUpdatePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c61293fcc3cb91004c14d06c1817a0e4bfc39e5cb2e5f2db5e0137e0c61dbf0d(
    *,
    instance_template: builtins.str,
    name: typing.Optional[builtins.str] = None,
    target_size: typing.Optional[typing.Union[ComputeRegionInstanceGroupManagerVersionTargetSize, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78de44757aa2d5fc88694a75c95e9b5d4a0a6b13b2887953af7ac9837db670ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c1178300e5c7970d4004aa03c6ff5a0578ad44d6facfc4ba05195f802b321e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb807f930abb7e24c62a7cd72266724e66004f54f7fad029ae932b13df55e9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6a43851730423625d477a55dae195f37dcf28fcfd64dc1aec78012c82bb434b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__765c7647384cfb1e3007f3b3ef39d20bee75ea1873110f7c4f8039220c71be68(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd79c16a0c2321b55cd6f757d2a4432519e2007bdb6e24f6d3167256a099eb3c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceGroupManagerVersion]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7726ad0fe16faf3ba9fe89fd039081795c5104255c2d0b59f7a6e0deb9834a7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d79743133689266501e3e5a99823a675be730758dc31c6890a1d5b2b96e47b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d966226d2c080e25fa8cdb6f2ceebc515ae199dff760ca3449a0e0af27afa99a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f26dcef16f8511eaee37a954c69d6f48e3caf9773b11a57e6164fe9a340558e3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceGroupManagerVersion]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8589d940b72d5c086b99090e153e1399c3397e2de7a947854f479ebd2efab085(
    *,
    fixed: typing.Optional[jsii.Number] = None,
    percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d903f3171fbbc8ee5b8afe09a1bf199e7cc46acc8a965be4d0ae394f8447478(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31f8a68b07d0586c90bc0cb045d89814bb4a838a7c47c9cc6c3912d9546a4ca(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39bbaa57e037d8b1a6c4f74db11453782b4eff472e6132573ab478fe7dbe1452(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052ba18424ca9a5caefb0bb60042447f2cd581fc4eb62ff32254b76ffc5a50ff(
    value: typing.Optional[ComputeRegionInstanceGroupManagerVersionTargetSize],
) -> None:
    """Type checking stubs"""
    pass
