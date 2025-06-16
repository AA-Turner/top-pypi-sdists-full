r'''
# `google_compute_region_instance_group_manager`

Refer to the Terraform Registry for docs: [`google_compute_region_instance_group_manager`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager).
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


class GoogleComputeRegionInstanceGroupManager(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManager",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager google_compute_region_instance_group_manager}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        base_instance_name: builtins.str,
        name: builtins.str,
        version: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionInstanceGroupManagerVersion", typing.Dict[builtins.str, typing.Any]]]],
        all_instances_config: typing.Optional[typing.Union["GoogleComputeRegionInstanceGroupManagerAllInstancesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_healing_policies: typing.Optional[typing.Union["GoogleComputeRegionInstanceGroupManagerAutoHealingPolicies", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        distribution_policy_target_shape: typing.Optional[builtins.str] = None,
        distribution_policy_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_flexibility_policy: typing.Optional[typing.Union["GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_lifecycle_policy: typing.Optional[typing.Union["GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        list_managed_instances_results: typing.Optional[builtins.str] = None,
        named_port: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionInstanceGroupManagerNamedPort", typing.Dict[builtins.str, typing.Any]]]]] = None,
        params: typing.Optional[typing.Union["GoogleComputeRegionInstanceGroupManagerParams", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        standby_policy: typing.Optional[typing.Union["GoogleComputeRegionInstanceGroupManagerStandbyPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        stateful_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionInstanceGroupManagerStatefulDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stateful_external_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionInstanceGroupManagerStatefulExternalIp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stateful_internal_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionInstanceGroupManagerStatefulInternalIp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_size: typing.Optional[jsii.Number] = None,
        target_stopped_size: typing.Optional[jsii.Number] = None,
        target_suspended_size: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeRegionInstanceGroupManagerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        update_policy: typing.Optional[typing.Union["GoogleComputeRegionInstanceGroupManagerUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager google_compute_region_instance_group_manager} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param base_instance_name: The base instance name to use for instances in this group. The value must be a valid RFC1035 name. Supported characters are lowercase letters, numbers, and hyphens (-). Instances are named by appending a hyphen and a random four-character string to the base instance name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#base_instance_name GoogleComputeRegionInstanceGroupManager#base_instance_name}
        :param name: The name of the instance group manager. Must be 1-63 characters long and comply with RFC1035. Supported characters include lowercase letters, numbers, and hyphens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#name GoogleComputeRegionInstanceGroupManager#name}
        :param version: version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#version GoogleComputeRegionInstanceGroupManager#version}
        :param all_instances_config: all_instances_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#all_instances_config GoogleComputeRegionInstanceGroupManager#all_instances_config}
        :param auto_healing_policies: auto_healing_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#auto_healing_policies GoogleComputeRegionInstanceGroupManager#auto_healing_policies}
        :param description: An optional textual description of the instance group manager. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#description GoogleComputeRegionInstanceGroupManager#description}
        :param distribution_policy_target_shape: The shape to which the group converges either proactively or on resize events (depending on the value set in updatePolicy.instanceRedistributionType). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#distribution_policy_target_shape GoogleComputeRegionInstanceGroupManager#distribution_policy_target_shape}
        :param distribution_policy_zones: The distribution policy for this managed instance group. You can specify one or more values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#distribution_policy_zones GoogleComputeRegionInstanceGroupManager#distribution_policy_zones}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#id GoogleComputeRegionInstanceGroupManager#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_flexibility_policy: instance_flexibility_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#instance_flexibility_policy GoogleComputeRegionInstanceGroupManager#instance_flexibility_policy}
        :param instance_lifecycle_policy: instance_lifecycle_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#instance_lifecycle_policy GoogleComputeRegionInstanceGroupManager#instance_lifecycle_policy}
        :param list_managed_instances_results: Pagination behavior of the listManagedInstances API method for this managed instance group. Valid values are: "PAGELESS", "PAGINATED". If PAGELESS (default), Pagination is disabled for the group's listManagedInstances API method. maxResults and pageToken query parameters are ignored and all instances are returned in a single response. If PAGINATED, pagination is enabled, maxResults and pageToken query parameters are respected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#list_managed_instances_results GoogleComputeRegionInstanceGroupManager#list_managed_instances_results}
        :param named_port: named_port block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#named_port GoogleComputeRegionInstanceGroupManager#named_port}
        :param params: params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#params GoogleComputeRegionInstanceGroupManager#params}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#project GoogleComputeRegionInstanceGroupManager#project}
        :param region: The region where the managed instance group resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#region GoogleComputeRegionInstanceGroupManager#region}
        :param standby_policy: standby_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#standby_policy GoogleComputeRegionInstanceGroupManager#standby_policy}
        :param stateful_disk: stateful_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#stateful_disk GoogleComputeRegionInstanceGroupManager#stateful_disk}
        :param stateful_external_ip: stateful_external_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#stateful_external_ip GoogleComputeRegionInstanceGroupManager#stateful_external_ip}
        :param stateful_internal_ip: stateful_internal_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#stateful_internal_ip GoogleComputeRegionInstanceGroupManager#stateful_internal_ip}
        :param target_pools: The full URL of all target pools to which new instances in the group are added. Updating the target pools attribute does not affect existing instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#target_pools GoogleComputeRegionInstanceGroupManager#target_pools}
        :param target_size: The target number of running instances for this managed instance group. This value should always be explicitly set unless this resource is attached to an autoscaler, in which case it should never be set. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#target_size GoogleComputeRegionInstanceGroupManager#target_size}
        :param target_stopped_size: The target number of stopped instances for this managed instance group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#target_stopped_size GoogleComputeRegionInstanceGroupManager#target_stopped_size}
        :param target_suspended_size: The target number of suspended instances for this managed instance group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#target_suspended_size GoogleComputeRegionInstanceGroupManager#target_suspended_size}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#timeouts GoogleComputeRegionInstanceGroupManager#timeouts}
        :param update_policy: update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#update_policy GoogleComputeRegionInstanceGroupManager#update_policy}
        :param wait_for_instances: Whether to wait for all instances to be created/updated before returning. Note that if this is set to true and the operation does not succeed, Terraform will continue trying until it times out. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#wait_for_instances GoogleComputeRegionInstanceGroupManager#wait_for_instances}
        :param wait_for_instances_status: When used with wait_for_instances specifies the status to wait for. When STABLE is specified this resource will wait until the instances are stable before returning. When UPDATED is set, it will wait for the version target to be reached and any per instance configs to be effective and all instances configs to be effective as well as all instances to be stable before returning. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#wait_for_instances_status GoogleComputeRegionInstanceGroupManager#wait_for_instances_status}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a223827e98daecc5f832261e4c56ad88a912b110c7eb8606c17c1b08cfb33f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleComputeRegionInstanceGroupManagerConfig(
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
            params=params,
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
        '''Generates CDKTF code for importing a GoogleComputeRegionInstanceGroupManager resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleComputeRegionInstanceGroupManager to import.
        :param import_from_id: The id of the existing GoogleComputeRegionInstanceGroupManager that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleComputeRegionInstanceGroupManager to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b221e27e8ad71fb75945773c39873bf096eb8bd74903efa04f6f93c787717e2)
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
        :param labels: The label key-value pairs that you want to patch onto the instance,. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#labels GoogleComputeRegionInstanceGroupManager#labels}
        :param metadata: The metadata key-value pairs that you want to patch onto the instance. For more information, see Project and instance metadata, Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#metadata GoogleComputeRegionInstanceGroupManager#metadata}
        '''
        value = GoogleComputeRegionInstanceGroupManagerAllInstancesConfig(
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
        :param health_check: The health check resource that signals autohealing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#health_check GoogleComputeRegionInstanceGroupManager#health_check}
        :param initial_delay_sec: The number of seconds that the managed instance group waits before it applies autohealing policies to new instances or recently recreated instances. Between 0 and 3600. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#initial_delay_sec GoogleComputeRegionInstanceGroupManager#initial_delay_sec}
        '''
        value = GoogleComputeRegionInstanceGroupManagerAutoHealingPolicies(
            health_check=health_check, initial_delay_sec=initial_delay_sec
        )

        return typing.cast(None, jsii.invoke(self, "putAutoHealingPolicies", [value]))

    @jsii.member(jsii_name="putInstanceFlexibilityPolicy")
    def put_instance_flexibility_policy(
        self,
        *,
        instance_selections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param instance_selections: instance_selections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#instance_selections GoogleComputeRegionInstanceGroupManager#instance_selections}
        '''
        value = GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy(
            instance_selections=instance_selections
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceFlexibilityPolicy", [value]))

    @jsii.member(jsii_name="putInstanceLifecyclePolicy")
    def put_instance_lifecycle_policy(
        self,
        *,
        default_action_on_failure: typing.Optional[builtins.str] = None,
        force_update_on_repair: typing.Optional[builtins.str] = None,
        on_failed_health_check: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_action_on_failure: Specifies the action that a MIG performs on a failed VM. If the value of the "on_failed_health_check" field is DEFAULT_ACTION, then the same action also applies to the VMs on which your application fails a health check. Valid values are: REPAIR, DO_NOTHING. If REPAIR (default), then MIG automatically repairs a failed VM by recreating it. For more information, see about repairing VMs in a MIG. If DO_NOTHING, then MIG does not repair a failed VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#default_action_on_failure GoogleComputeRegionInstanceGroupManager#default_action_on_failure}
        :param force_update_on_repair: Specifies whether to apply the group's latest configuration when repairing a VM. Valid options are: YES, NO. If YES and you updated the group's instance template or per-instance configurations after the VM was created, then these changes are applied when VM is repaired. If NO (default), then updates are applied in accordance with the group's update policy type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#force_update_on_repair GoogleComputeRegionInstanceGroupManager#force_update_on_repair}
        :param on_failed_health_check: Specifies the action that a MIG performs on an unhealthy VM. A VM is marked as unhealthy when the application running on that VM fails a health check. Valid values are: DEFAULT_ACTION, DO_NOTHING, REPAIR. If DEFAULT_ACTION (default), then MIG uses the same action configured for the "default_action_on_failure" field. If DO_NOTHING, then MIG does not repair unhealthy VM. If REPAIR, then MIG automatically repairs an unhealthy VM by recreating it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#on_failed_health_check GoogleComputeRegionInstanceGroupManager#on_failed_health_check}
        '''
        value = GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicy(
            default_action_on_failure=default_action_on_failure,
            force_update_on_repair=force_update_on_repair,
            on_failed_health_check=on_failed_health_check,
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceLifecyclePolicy", [value]))

    @jsii.member(jsii_name="putNamedPort")
    def put_named_port(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionInstanceGroupManagerNamedPort", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f0064ae99021551bf68767d026acde8da9fb8eeaf197f36c17d6023fd67339b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNamedPort", [value]))

    @jsii.member(jsii_name="putParams")
    def put_params(
        self,
        *,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param resource_manager_tags: Resource manager tags to bind to the managed instance group. The tags are key-value pairs. Keys must be in the format tagKeys/123 and values in the format tagValues/456. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#resource_manager_tags GoogleComputeRegionInstanceGroupManager#resource_manager_tags}
        '''
        value = GoogleComputeRegionInstanceGroupManagerParams(
            resource_manager_tags=resource_manager_tags
        )

        return typing.cast(None, jsii.invoke(self, "putParams", [value]))

    @jsii.member(jsii_name="putStandbyPolicy")
    def put_standby_policy(
        self,
        *,
        initial_delay_sec: typing.Optional[jsii.Number] = None,
        mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param initial_delay_sec: Specifies the number of seconds that the MIG should wait to suspend or stop a VM after that VM was created. The initial delay gives the initialization script the time to prepare your VM for a quick scale out. The value of initial delay must be between 0 and 3600 seconds. The default value is 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#initial_delay_sec GoogleComputeRegionInstanceGroupManager#initial_delay_sec}
        :param mode: Defines how a MIG resumes or starts VMs from a standby pool when the group scales out. The default mode is "MANUAL". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#mode GoogleComputeRegionInstanceGroupManager#mode}
        '''
        value = GoogleComputeRegionInstanceGroupManagerStandbyPolicy(
            initial_delay_sec=initial_delay_sec, mode=mode
        )

        return typing.cast(None, jsii.invoke(self, "putStandbyPolicy", [value]))

    @jsii.member(jsii_name="putStatefulDisk")
    def put_stateful_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionInstanceGroupManagerStatefulDisk", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74137bd1f00d07b8b1fde0c2c228c2b4e4e39a238ee6712c4cd41d1fc65313fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStatefulDisk", [value]))

    @jsii.member(jsii_name="putStatefulExternalIp")
    def put_stateful_external_ip(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionInstanceGroupManagerStatefulExternalIp", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b7dea1a4653583095bb48a9fbcb01c4869653becb6c634ad565edae64832a23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStatefulExternalIp", [value]))

    @jsii.member(jsii_name="putStatefulInternalIp")
    def put_stateful_internal_ip(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionInstanceGroupManagerStatefulInternalIp", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__441356b7e1690efb818dd9a93801c5e3560a054f77b28433b50bd0def9118bdb)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#create GoogleComputeRegionInstanceGroupManager#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#delete GoogleComputeRegionInstanceGroupManager#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#update GoogleComputeRegionInstanceGroupManager#update}.
        '''
        value = GoogleComputeRegionInstanceGroupManagerTimeouts(
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
        min_ready_sec: typing.Optional[jsii.Number] = None,
        most_disruptive_allowed_action: typing.Optional[builtins.str] = None,
        replacement_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param minimal_action: Minimal action to be taken on an instance. You can specify either NONE to forbid any actions, REFRESH to update without stopping instances, RESTART to restart existing instances or REPLACE to delete and create new instances from the target template. If you specify a REFRESH, the Updater will attempt to perform that action only. However, if the Updater determines that the minimal action you specify is not enough to perform the update, it might perform a more disruptive action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#minimal_action GoogleComputeRegionInstanceGroupManager#minimal_action}
        :param type: The type of update process. You can specify either PROACTIVE so that the instance group manager proactively executes actions in order to bring instances to their target versions or OPPORTUNISTIC so that no action is proactively executed but the update will be performed as part of other actions (for example, resizes or recreateInstances calls). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#type GoogleComputeRegionInstanceGroupManager#type}
        :param instance_redistribution_type: The instance redistribution policy for regional managed instance groups. Valid values are: "PROACTIVE", "NONE". If PROACTIVE (default), the group attempts to maintain an even distribution of VM instances across zones in the region. If NONE, proactive redistribution is disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#instance_redistribution_type GoogleComputeRegionInstanceGroupManager#instance_redistribution_type}
        :param max_surge_fixed: Specifies a fixed number of VM instances. This must be a positive integer. Conflicts with max_surge_percent. Both cannot be 0 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#max_surge_fixed GoogleComputeRegionInstanceGroupManager#max_surge_fixed}
        :param max_surge_percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Conflicts with max_surge_fixed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#max_surge_percent GoogleComputeRegionInstanceGroupManager#max_surge_percent}
        :param max_unavailable_fixed: Specifies a fixed number of VM instances. This must be a positive integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#max_unavailable_fixed GoogleComputeRegionInstanceGroupManager#max_unavailable_fixed}
        :param max_unavailable_percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#max_unavailable_percent GoogleComputeRegionInstanceGroupManager#max_unavailable_percent}
        :param min_ready_sec: Minimum number of seconds to wait for after a newly created instance becomes available. This value must be from range [0, 3600]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#min_ready_sec GoogleComputeRegionInstanceGroupManager#min_ready_sec}
        :param most_disruptive_allowed_action: Most disruptive action that is allowed to be taken on an instance. You can specify either NONE to forbid any actions, REFRESH to allow actions that do not need instance restart, RESTART to allow actions that can be applied without instance replacing or REPLACE to allow all possible actions. If the Updater determines that the minimal update action needed is more disruptive than most disruptive allowed action you specify it will not perform the update at all. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#most_disruptive_allowed_action GoogleComputeRegionInstanceGroupManager#most_disruptive_allowed_action}
        :param replacement_method: The instance replacement method for regional managed instance groups. Valid values are: "RECREATE", "SUBSTITUTE". If SUBSTITUTE (default), the group replaces VM instances with new instances that have randomly generated names. If RECREATE, instance names are preserved. You must also set max_unavailable_fixed or max_unavailable_percent to be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#replacement_method GoogleComputeRegionInstanceGroupManager#replacement_method}
        '''
        value = GoogleComputeRegionInstanceGroupManagerUpdatePolicy(
            minimal_action=minimal_action,
            type=type,
            instance_redistribution_type=instance_redistribution_type,
            max_surge_fixed=max_surge_fixed,
            max_surge_percent=max_surge_percent,
            max_unavailable_fixed=max_unavailable_fixed,
            max_unavailable_percent=max_unavailable_percent,
            min_ready_sec=min_ready_sec,
            most_disruptive_allowed_action=most_disruptive_allowed_action,
            replacement_method=replacement_method,
        )

        return typing.cast(None, jsii.invoke(self, "putUpdatePolicy", [value]))

    @jsii.member(jsii_name="putVersion")
    def put_version(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionInstanceGroupManagerVersion", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68c7dc7b85596f0c869965914da72af0bbb4bb3c406c22fbdcce55fa6e18c3d0)
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

    @jsii.member(jsii_name="resetParams")
    def reset_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParams", []))

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
    ) -> "GoogleComputeRegionInstanceGroupManagerAllInstancesConfigOutputReference":
        return typing.cast("GoogleComputeRegionInstanceGroupManagerAllInstancesConfigOutputReference", jsii.get(self, "allInstancesConfig"))

    @builtins.property
    @jsii.member(jsii_name="autoHealingPolicies")
    def auto_healing_policies(
        self,
    ) -> "GoogleComputeRegionInstanceGroupManagerAutoHealingPoliciesOutputReference":
        return typing.cast("GoogleComputeRegionInstanceGroupManagerAutoHealingPoliciesOutputReference", jsii.get(self, "autoHealingPolicies"))

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
    ) -> "GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyOutputReference":
        return typing.cast("GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyOutputReference", jsii.get(self, "instanceFlexibilityPolicy"))

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
    ) -> "GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicyOutputReference":
        return typing.cast("GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicyOutputReference", jsii.get(self, "instanceLifecyclePolicy"))

    @builtins.property
    @jsii.member(jsii_name="namedPort")
    def named_port(self) -> "GoogleComputeRegionInstanceGroupManagerNamedPortList":
        return typing.cast("GoogleComputeRegionInstanceGroupManagerNamedPortList", jsii.get(self, "namedPort"))

    @builtins.property
    @jsii.member(jsii_name="params")
    def params(self) -> "GoogleComputeRegionInstanceGroupManagerParamsOutputReference":
        return typing.cast("GoogleComputeRegionInstanceGroupManagerParamsOutputReference", jsii.get(self, "params"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="standbyPolicy")
    def standby_policy(
        self,
    ) -> "GoogleComputeRegionInstanceGroupManagerStandbyPolicyOutputReference":
        return typing.cast("GoogleComputeRegionInstanceGroupManagerStandbyPolicyOutputReference", jsii.get(self, "standbyPolicy"))

    @builtins.property
    @jsii.member(jsii_name="statefulDisk")
    def stateful_disk(
        self,
    ) -> "GoogleComputeRegionInstanceGroupManagerStatefulDiskList":
        return typing.cast("GoogleComputeRegionInstanceGroupManagerStatefulDiskList", jsii.get(self, "statefulDisk"))

    @builtins.property
    @jsii.member(jsii_name="statefulExternalIp")
    def stateful_external_ip(
        self,
    ) -> "GoogleComputeRegionInstanceGroupManagerStatefulExternalIpList":
        return typing.cast("GoogleComputeRegionInstanceGroupManagerStatefulExternalIpList", jsii.get(self, "statefulExternalIp"))

    @builtins.property
    @jsii.member(jsii_name="statefulInternalIp")
    def stateful_internal_ip(
        self,
    ) -> "GoogleComputeRegionInstanceGroupManagerStatefulInternalIpList":
        return typing.cast("GoogleComputeRegionInstanceGroupManagerStatefulInternalIpList", jsii.get(self, "statefulInternalIp"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "GoogleComputeRegionInstanceGroupManagerStatusList":
        return typing.cast("GoogleComputeRegionInstanceGroupManagerStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleComputeRegionInstanceGroupManagerTimeoutsOutputReference":
        return typing.cast("GoogleComputeRegionInstanceGroupManagerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updatePolicy")
    def update_policy(
        self,
    ) -> "GoogleComputeRegionInstanceGroupManagerUpdatePolicyOutputReference":
        return typing.cast("GoogleComputeRegionInstanceGroupManagerUpdatePolicyOutputReference", jsii.get(self, "updatePolicy"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> "GoogleComputeRegionInstanceGroupManagerVersionList":
        return typing.cast("GoogleComputeRegionInstanceGroupManagerVersionList", jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="allInstancesConfigInput")
    def all_instances_config_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionInstanceGroupManagerAllInstancesConfig"]:
        return typing.cast(typing.Optional["GoogleComputeRegionInstanceGroupManagerAllInstancesConfig"], jsii.get(self, "allInstancesConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="autoHealingPoliciesInput")
    def auto_healing_policies_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionInstanceGroupManagerAutoHealingPolicies"]:
        return typing.cast(typing.Optional["GoogleComputeRegionInstanceGroupManagerAutoHealingPolicies"], jsii.get(self, "autoHealingPoliciesInput"))

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
    ) -> typing.Optional["GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy"]:
        return typing.cast(typing.Optional["GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy"], jsii.get(self, "instanceFlexibilityPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceLifecyclePolicyInput")
    def instance_lifecycle_policy_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicy"]:
        return typing.cast(typing.Optional["GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicy"], jsii.get(self, "instanceLifecyclePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="listManagedInstancesResultsInput")
    def list_managed_instances_results_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "listManagedInstancesResultsInput"))

    @builtins.property
    @jsii.member(jsii_name="namedPortInput")
    def named_port_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerNamedPort"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerNamedPort"]]], jsii.get(self, "namedPortInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="paramsInput")
    def params_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionInstanceGroupManagerParams"]:
        return typing.cast(typing.Optional["GoogleComputeRegionInstanceGroupManagerParams"], jsii.get(self, "paramsInput"))

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
    ) -> typing.Optional["GoogleComputeRegionInstanceGroupManagerStandbyPolicy"]:
        return typing.cast(typing.Optional["GoogleComputeRegionInstanceGroupManagerStandbyPolicy"], jsii.get(self, "standbyPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="statefulDiskInput")
    def stateful_disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerStatefulDisk"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerStatefulDisk"]]], jsii.get(self, "statefulDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="statefulExternalIpInput")
    def stateful_external_ip_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerStatefulExternalIp"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerStatefulExternalIp"]]], jsii.get(self, "statefulExternalIpInput"))

    @builtins.property
    @jsii.member(jsii_name="statefulInternalIpInput")
    def stateful_internal_ip_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerStatefulInternalIp"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerStatefulInternalIp"]]], jsii.get(self, "statefulInternalIpInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeRegionInstanceGroupManagerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeRegionInstanceGroupManagerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="updatePolicyInput")
    def update_policy_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionInstanceGroupManagerUpdatePolicy"]:
        return typing.cast(typing.Optional["GoogleComputeRegionInstanceGroupManagerUpdatePolicy"], jsii.get(self, "updatePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerVersion"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerVersion"]]], jsii.get(self, "versionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__cfeae3de56ea3f8a69d1872a30b44a34fe4ae401770e1067dee64d3a5adecdc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseInstanceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__483c8f25feed468c2a82c954d0f16e427f0e4a5b0a0e2ad2a171096e475a4a7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="distributionPolicyTargetShape")
    def distribution_policy_target_shape(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "distributionPolicyTargetShape"))

    @distribution_policy_target_shape.setter
    def distribution_policy_target_shape(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c16f9445792196597ce6ec647147d6fe9d344e736a9e37cb262c584e89680ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distributionPolicyTargetShape", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="distributionPolicyZones")
    def distribution_policy_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "distributionPolicyZones"))

    @distribution_policy_zones.setter
    def distribution_policy_zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c3228de417f2063b76e2250ad6a96b8427af6d4a33901f0be7446d4842ff081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distributionPolicyZones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__265c325303a7ffa19212e472c11bbed846588850e85fd1332a9059ce38efbdac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="listManagedInstancesResults")
    def list_managed_instances_results(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "listManagedInstancesResults"))

    @list_managed_instances_results.setter
    def list_managed_instances_results(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e84d0739c6e6ca1f0a3540ecdb59c046ad080b3172708c7c7d0cb72d452b59a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listManagedInstancesResults", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e656f0f17eebd91fabe16c9814a28486ae9956b94fd89c9ebb0f6236aac8fe22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b73a8b0adefe00a2ea802c7704f70f2954f7f1424be94f5c55cc2c05476c648b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86497fea093d199780bcf4d7da28a474c9ab56b25a834b527e435b65cf0fc7ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetPools")
    def target_pools(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetPools"))

    @target_pools.setter
    def target_pools(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f916b4c1d05c5fcf1e374a195c6fbb277173ebc3ffec5945a982ac4f041f2c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetPools", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetSize")
    def target_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetSize"))

    @target_size.setter
    def target_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__856a4cd9b29b06e2ddb6971a4ba492b2e8dcc3655e20a9d02cf2fff6f13980fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetStoppedSize")
    def target_stopped_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetStoppedSize"))

    @target_stopped_size.setter
    def target_stopped_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de1e169c81ef66ca3e6db169ca1694a3cc90855b0b0ffb4adf6e90215eb06dc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetStoppedSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetSuspendedSize")
    def target_suspended_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetSuspendedSize"))

    @target_suspended_size.setter
    def target_suspended_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd76ccfcd8766ac123ae15c53c459c9e3dfaa5720a25fa65b60ca26be647ff5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e656948261dba83c3932bacb02cef5919edb78bd37885b82ba3c2fa0dbb1d3fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="waitForInstancesStatus")
    def wait_for_instances_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "waitForInstancesStatus"))

    @wait_for_instances_status.setter
    def wait_for_instances_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6e5aabaefc1c14562f2fadb6d9fbae6c0998464e94006f2cb0576ab4bb8f926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForInstancesStatus", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerAllInstancesConfig",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels", "metadata": "metadata"},
)
class GoogleComputeRegionInstanceGroupManagerAllInstancesConfig:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param labels: The label key-value pairs that you want to patch onto the instance,. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#labels GoogleComputeRegionInstanceGroupManager#labels}
        :param metadata: The metadata key-value pairs that you want to patch onto the instance. For more information, see Project and instance metadata, Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#metadata GoogleComputeRegionInstanceGroupManager#metadata}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b633494e8293ba9ff1272685860cd1d54568481a4baef09b8dcccd34cf51d8eb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#labels GoogleComputeRegionInstanceGroupManager#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The metadata key-value pairs that you want to patch onto the instance.

        For more information, see Project and instance metadata,

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#metadata GoogleComputeRegionInstanceGroupManager#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionInstanceGroupManagerAllInstancesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionInstanceGroupManagerAllInstancesConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerAllInstancesConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__afd6ad763533f35180b7eda7a67e18391bf52d371f5263bb778a8d3e571f7018)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ae6358560528dbb3e389e4ff63f318e92844fd4d9bc27c4bb9ae2a4ee03e0da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc2ab515c509cde6c076fc398728a1ff9b97d43226f5576468e9989df6a5dbef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionInstanceGroupManagerAllInstancesConfig]:
        return typing.cast(typing.Optional[GoogleComputeRegionInstanceGroupManagerAllInstancesConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionInstanceGroupManagerAllInstancesConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0a80d828c506422638f5909c81c0f4c4b696cca3f25b89d63e8cbec66bfa47d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerAutoHealingPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "health_check": "healthCheck",
        "initial_delay_sec": "initialDelaySec",
    },
)
class GoogleComputeRegionInstanceGroupManagerAutoHealingPolicies:
    def __init__(
        self,
        *,
        health_check: builtins.str,
        initial_delay_sec: jsii.Number,
    ) -> None:
        '''
        :param health_check: The health check resource that signals autohealing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#health_check GoogleComputeRegionInstanceGroupManager#health_check}
        :param initial_delay_sec: The number of seconds that the managed instance group waits before it applies autohealing policies to new instances or recently recreated instances. Between 0 and 3600. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#initial_delay_sec GoogleComputeRegionInstanceGroupManager#initial_delay_sec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__111631cf12b14dee3ade6dcb8dbce6643ccdfb479542b6a1c30529756f98bedf)
            check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
            check_type(argname="argument initial_delay_sec", value=initial_delay_sec, expected_type=type_hints["initial_delay_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "health_check": health_check,
            "initial_delay_sec": initial_delay_sec,
        }

    @builtins.property
    def health_check(self) -> builtins.str:
        '''The health check resource that signals autohealing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#health_check GoogleComputeRegionInstanceGroupManager#health_check}
        '''
        result = self._values.get("health_check")
        assert result is not None, "Required property 'health_check' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def initial_delay_sec(self) -> jsii.Number:
        '''The number of seconds that the managed instance group waits before it applies autohealing policies to new instances or recently recreated instances.

        Between 0 and 3600.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#initial_delay_sec GoogleComputeRegionInstanceGroupManager#initial_delay_sec}
        '''
        result = self._values.get("initial_delay_sec")
        assert result is not None, "Required property 'initial_delay_sec' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionInstanceGroupManagerAutoHealingPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionInstanceGroupManagerAutoHealingPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerAutoHealingPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a0343f5466df1f9001d109b246679bf09791a05a32d9c2045fedf4daabd12f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b049cec12db9cee559f84717e6fcfec45c4d406d5e7b358bf7a798f43e79057)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelaySec")
    def initial_delay_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelaySec"))

    @initial_delay_sec.setter
    def initial_delay_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b25dfe1ae83c31730f1ad89e977a1b16b413538b7ca614cbbbe41edf511c5cf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelaySec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionInstanceGroupManagerAutoHealingPolicies]:
        return typing.cast(typing.Optional[GoogleComputeRegionInstanceGroupManagerAutoHealingPolicies], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionInstanceGroupManagerAutoHealingPolicies],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f360f527b8995324806443455754432a1b801b8a5a7c5d4b98ebe7f514ddb53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerConfig",
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
        "params": "params",
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
class GoogleComputeRegionInstanceGroupManagerConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        version: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionInstanceGroupManagerVersion", typing.Dict[builtins.str, typing.Any]]]],
        all_instances_config: typing.Optional[typing.Union[GoogleComputeRegionInstanceGroupManagerAllInstancesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_healing_policies: typing.Optional[typing.Union[GoogleComputeRegionInstanceGroupManagerAutoHealingPolicies, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        distribution_policy_target_shape: typing.Optional[builtins.str] = None,
        distribution_policy_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_flexibility_policy: typing.Optional[typing.Union["GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_lifecycle_policy: typing.Optional[typing.Union["GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        list_managed_instances_results: typing.Optional[builtins.str] = None,
        named_port: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionInstanceGroupManagerNamedPort", typing.Dict[builtins.str, typing.Any]]]]] = None,
        params: typing.Optional[typing.Union["GoogleComputeRegionInstanceGroupManagerParams", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        standby_policy: typing.Optional[typing.Union["GoogleComputeRegionInstanceGroupManagerStandbyPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        stateful_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionInstanceGroupManagerStatefulDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stateful_external_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionInstanceGroupManagerStatefulExternalIp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stateful_internal_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionInstanceGroupManagerStatefulInternalIp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_size: typing.Optional[jsii.Number] = None,
        target_stopped_size: typing.Optional[jsii.Number] = None,
        target_suspended_size: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeRegionInstanceGroupManagerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        update_policy: typing.Optional[typing.Union["GoogleComputeRegionInstanceGroupManagerUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param base_instance_name: The base instance name to use for instances in this group. The value must be a valid RFC1035 name. Supported characters are lowercase letters, numbers, and hyphens (-). Instances are named by appending a hyphen and a random four-character string to the base instance name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#base_instance_name GoogleComputeRegionInstanceGroupManager#base_instance_name}
        :param name: The name of the instance group manager. Must be 1-63 characters long and comply with RFC1035. Supported characters include lowercase letters, numbers, and hyphens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#name GoogleComputeRegionInstanceGroupManager#name}
        :param version: version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#version GoogleComputeRegionInstanceGroupManager#version}
        :param all_instances_config: all_instances_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#all_instances_config GoogleComputeRegionInstanceGroupManager#all_instances_config}
        :param auto_healing_policies: auto_healing_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#auto_healing_policies GoogleComputeRegionInstanceGroupManager#auto_healing_policies}
        :param description: An optional textual description of the instance group manager. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#description GoogleComputeRegionInstanceGroupManager#description}
        :param distribution_policy_target_shape: The shape to which the group converges either proactively or on resize events (depending on the value set in updatePolicy.instanceRedistributionType). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#distribution_policy_target_shape GoogleComputeRegionInstanceGroupManager#distribution_policy_target_shape}
        :param distribution_policy_zones: The distribution policy for this managed instance group. You can specify one or more values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#distribution_policy_zones GoogleComputeRegionInstanceGroupManager#distribution_policy_zones}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#id GoogleComputeRegionInstanceGroupManager#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_flexibility_policy: instance_flexibility_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#instance_flexibility_policy GoogleComputeRegionInstanceGroupManager#instance_flexibility_policy}
        :param instance_lifecycle_policy: instance_lifecycle_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#instance_lifecycle_policy GoogleComputeRegionInstanceGroupManager#instance_lifecycle_policy}
        :param list_managed_instances_results: Pagination behavior of the listManagedInstances API method for this managed instance group. Valid values are: "PAGELESS", "PAGINATED". If PAGELESS (default), Pagination is disabled for the group's listManagedInstances API method. maxResults and pageToken query parameters are ignored and all instances are returned in a single response. If PAGINATED, pagination is enabled, maxResults and pageToken query parameters are respected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#list_managed_instances_results GoogleComputeRegionInstanceGroupManager#list_managed_instances_results}
        :param named_port: named_port block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#named_port GoogleComputeRegionInstanceGroupManager#named_port}
        :param params: params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#params GoogleComputeRegionInstanceGroupManager#params}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#project GoogleComputeRegionInstanceGroupManager#project}
        :param region: The region where the managed instance group resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#region GoogleComputeRegionInstanceGroupManager#region}
        :param standby_policy: standby_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#standby_policy GoogleComputeRegionInstanceGroupManager#standby_policy}
        :param stateful_disk: stateful_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#stateful_disk GoogleComputeRegionInstanceGroupManager#stateful_disk}
        :param stateful_external_ip: stateful_external_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#stateful_external_ip GoogleComputeRegionInstanceGroupManager#stateful_external_ip}
        :param stateful_internal_ip: stateful_internal_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#stateful_internal_ip GoogleComputeRegionInstanceGroupManager#stateful_internal_ip}
        :param target_pools: The full URL of all target pools to which new instances in the group are added. Updating the target pools attribute does not affect existing instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#target_pools GoogleComputeRegionInstanceGroupManager#target_pools}
        :param target_size: The target number of running instances for this managed instance group. This value should always be explicitly set unless this resource is attached to an autoscaler, in which case it should never be set. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#target_size GoogleComputeRegionInstanceGroupManager#target_size}
        :param target_stopped_size: The target number of stopped instances for this managed instance group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#target_stopped_size GoogleComputeRegionInstanceGroupManager#target_stopped_size}
        :param target_suspended_size: The target number of suspended instances for this managed instance group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#target_suspended_size GoogleComputeRegionInstanceGroupManager#target_suspended_size}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#timeouts GoogleComputeRegionInstanceGroupManager#timeouts}
        :param update_policy: update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#update_policy GoogleComputeRegionInstanceGroupManager#update_policy}
        :param wait_for_instances: Whether to wait for all instances to be created/updated before returning. Note that if this is set to true and the operation does not succeed, Terraform will continue trying until it times out. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#wait_for_instances GoogleComputeRegionInstanceGroupManager#wait_for_instances}
        :param wait_for_instances_status: When used with wait_for_instances specifies the status to wait for. When STABLE is specified this resource will wait until the instances are stable before returning. When UPDATED is set, it will wait for the version target to be reached and any per instance configs to be effective and all instances configs to be effective as well as all instances to be stable before returning. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#wait_for_instances_status GoogleComputeRegionInstanceGroupManager#wait_for_instances_status}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(all_instances_config, dict):
            all_instances_config = GoogleComputeRegionInstanceGroupManagerAllInstancesConfig(**all_instances_config)
        if isinstance(auto_healing_policies, dict):
            auto_healing_policies = GoogleComputeRegionInstanceGroupManagerAutoHealingPolicies(**auto_healing_policies)
        if isinstance(instance_flexibility_policy, dict):
            instance_flexibility_policy = GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy(**instance_flexibility_policy)
        if isinstance(instance_lifecycle_policy, dict):
            instance_lifecycle_policy = GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicy(**instance_lifecycle_policy)
        if isinstance(params, dict):
            params = GoogleComputeRegionInstanceGroupManagerParams(**params)
        if isinstance(standby_policy, dict):
            standby_policy = GoogleComputeRegionInstanceGroupManagerStandbyPolicy(**standby_policy)
        if isinstance(timeouts, dict):
            timeouts = GoogleComputeRegionInstanceGroupManagerTimeouts(**timeouts)
        if isinstance(update_policy, dict):
            update_policy = GoogleComputeRegionInstanceGroupManagerUpdatePolicy(**update_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cdab6c9a39ac9bc9a3723775576b3eceb14fc6c65f74847ffb37585e4e2b911)
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
            check_type(argname="argument params", value=params, expected_type=type_hints["params"])
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
        if params is not None:
            self._values["params"] = params
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#base_instance_name GoogleComputeRegionInstanceGroupManager#base_instance_name}
        '''
        result = self._values.get("base_instance_name")
        assert result is not None, "Required property 'base_instance_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the instance group manager.

        Must be 1-63 characters long and comply with RFC1035. Supported characters include lowercase letters, numbers, and hyphens.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#name GoogleComputeRegionInstanceGroupManager#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerVersion"]]:
        '''version block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#version GoogleComputeRegionInstanceGroupManager#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerVersion"]], result)

    @builtins.property
    def all_instances_config(
        self,
    ) -> typing.Optional[GoogleComputeRegionInstanceGroupManagerAllInstancesConfig]:
        '''all_instances_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#all_instances_config GoogleComputeRegionInstanceGroupManager#all_instances_config}
        '''
        result = self._values.get("all_instances_config")
        return typing.cast(typing.Optional[GoogleComputeRegionInstanceGroupManagerAllInstancesConfig], result)

    @builtins.property
    def auto_healing_policies(
        self,
    ) -> typing.Optional[GoogleComputeRegionInstanceGroupManagerAutoHealingPolicies]:
        '''auto_healing_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#auto_healing_policies GoogleComputeRegionInstanceGroupManager#auto_healing_policies}
        '''
        result = self._values.get("auto_healing_policies")
        return typing.cast(typing.Optional[GoogleComputeRegionInstanceGroupManagerAutoHealingPolicies], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional textual description of the instance group manager.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#description GoogleComputeRegionInstanceGroupManager#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def distribution_policy_target_shape(self) -> typing.Optional[builtins.str]:
        '''The shape to which the group converges either proactively or on resize events (depending on the value set in updatePolicy.instanceRedistributionType).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#distribution_policy_target_shape GoogleComputeRegionInstanceGroupManager#distribution_policy_target_shape}
        '''
        result = self._values.get("distribution_policy_target_shape")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def distribution_policy_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The distribution policy for this managed instance group. You can specify one or more values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#distribution_policy_zones GoogleComputeRegionInstanceGroupManager#distribution_policy_zones}
        '''
        result = self._values.get("distribution_policy_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#id GoogleComputeRegionInstanceGroupManager#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_flexibility_policy(
        self,
    ) -> typing.Optional["GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy"]:
        '''instance_flexibility_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#instance_flexibility_policy GoogleComputeRegionInstanceGroupManager#instance_flexibility_policy}
        '''
        result = self._values.get("instance_flexibility_policy")
        return typing.cast(typing.Optional["GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy"], result)

    @builtins.property
    def instance_lifecycle_policy(
        self,
    ) -> typing.Optional["GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicy"]:
        '''instance_lifecycle_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#instance_lifecycle_policy GoogleComputeRegionInstanceGroupManager#instance_lifecycle_policy}
        '''
        result = self._values.get("instance_lifecycle_policy")
        return typing.cast(typing.Optional["GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicy"], result)

    @builtins.property
    def list_managed_instances_results(self) -> typing.Optional[builtins.str]:
        '''Pagination behavior of the listManagedInstances API method for this managed instance group.

        Valid values are: "PAGELESS", "PAGINATED". If PAGELESS (default), Pagination is disabled for the group's listManagedInstances API method. maxResults and pageToken query parameters are ignored and all instances are returned in a single response. If PAGINATED, pagination is enabled, maxResults and pageToken query parameters are respected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#list_managed_instances_results GoogleComputeRegionInstanceGroupManager#list_managed_instances_results}
        '''
        result = self._values.get("list_managed_instances_results")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def named_port(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerNamedPort"]]]:
        '''named_port block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#named_port GoogleComputeRegionInstanceGroupManager#named_port}
        '''
        result = self._values.get("named_port")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerNamedPort"]]], result)

    @builtins.property
    def params(
        self,
    ) -> typing.Optional["GoogleComputeRegionInstanceGroupManagerParams"]:
        '''params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#params GoogleComputeRegionInstanceGroupManager#params}
        '''
        result = self._values.get("params")
        return typing.cast(typing.Optional["GoogleComputeRegionInstanceGroupManagerParams"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the resource belongs.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#project GoogleComputeRegionInstanceGroupManager#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region where the managed instance group resides.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#region GoogleComputeRegionInstanceGroupManager#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def standby_policy(
        self,
    ) -> typing.Optional["GoogleComputeRegionInstanceGroupManagerStandbyPolicy"]:
        '''standby_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#standby_policy GoogleComputeRegionInstanceGroupManager#standby_policy}
        '''
        result = self._values.get("standby_policy")
        return typing.cast(typing.Optional["GoogleComputeRegionInstanceGroupManagerStandbyPolicy"], result)

    @builtins.property
    def stateful_disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerStatefulDisk"]]]:
        '''stateful_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#stateful_disk GoogleComputeRegionInstanceGroupManager#stateful_disk}
        '''
        result = self._values.get("stateful_disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerStatefulDisk"]]], result)

    @builtins.property
    def stateful_external_ip(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerStatefulExternalIp"]]]:
        '''stateful_external_ip block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#stateful_external_ip GoogleComputeRegionInstanceGroupManager#stateful_external_ip}
        '''
        result = self._values.get("stateful_external_ip")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerStatefulExternalIp"]]], result)

    @builtins.property
    def stateful_internal_ip(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerStatefulInternalIp"]]]:
        '''stateful_internal_ip block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#stateful_internal_ip GoogleComputeRegionInstanceGroupManager#stateful_internal_ip}
        '''
        result = self._values.get("stateful_internal_ip")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerStatefulInternalIp"]]], result)

    @builtins.property
    def target_pools(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The full URL of all target pools to which new instances in the group are added.

        Updating the target pools attribute does not affect existing instances.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#target_pools GoogleComputeRegionInstanceGroupManager#target_pools}
        '''
        result = self._values.get("target_pools")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target_size(self) -> typing.Optional[jsii.Number]:
        '''The target number of running instances for this managed instance group.

        This value should always be explicitly set unless this resource is attached to an autoscaler, in which case it should never be set. Defaults to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#target_size GoogleComputeRegionInstanceGroupManager#target_size}
        '''
        result = self._values.get("target_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_stopped_size(self) -> typing.Optional[jsii.Number]:
        '''The target number of stopped instances for this managed instance group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#target_stopped_size GoogleComputeRegionInstanceGroupManager#target_stopped_size}
        '''
        result = self._values.get("target_stopped_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_suspended_size(self) -> typing.Optional[jsii.Number]:
        '''The target number of suspended instances for this managed instance group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#target_suspended_size GoogleComputeRegionInstanceGroupManager#target_suspended_size}
        '''
        result = self._values.get("target_suspended_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleComputeRegionInstanceGroupManagerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#timeouts GoogleComputeRegionInstanceGroupManager#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleComputeRegionInstanceGroupManagerTimeouts"], result)

    @builtins.property
    def update_policy(
        self,
    ) -> typing.Optional["GoogleComputeRegionInstanceGroupManagerUpdatePolicy"]:
        '''update_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#update_policy GoogleComputeRegionInstanceGroupManager#update_policy}
        '''
        result = self._values.get("update_policy")
        return typing.cast(typing.Optional["GoogleComputeRegionInstanceGroupManagerUpdatePolicy"], result)

    @builtins.property
    def wait_for_instances(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to wait for all instances to be created/updated before returning.

        Note that if this is set to true and the operation does not succeed, Terraform will continue trying until it times out.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#wait_for_instances GoogleComputeRegionInstanceGroupManager#wait_for_instances}
        '''
        result = self._values.get("wait_for_instances")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def wait_for_instances_status(self) -> typing.Optional[builtins.str]:
        '''When used with wait_for_instances specifies the status to wait for.

        When STABLE is specified this resource will wait until the instances are stable before returning. When UPDATED is set, it will wait for the version target to be reached and any per instance configs to be effective and all instances configs to be effective as well as all instances to be stable before returning.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#wait_for_instances_status GoogleComputeRegionInstanceGroupManager#wait_for_instances_status}
        '''
        result = self._values.get("wait_for_instances_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionInstanceGroupManagerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy",
    jsii_struct_bases=[],
    name_mapping={"instance_selections": "instanceSelections"},
)
class GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy:
    def __init__(
        self,
        *,
        instance_selections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param instance_selections: instance_selections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#instance_selections GoogleComputeRegionInstanceGroupManager#instance_selections}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cd1115646e4fba59250ceda1131835619526f00dfbc6842c6dc0d834b826336)
            check_type(argname="argument instance_selections", value=instance_selections, expected_type=type_hints["instance_selections"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_selections is not None:
            self._values["instance_selections"] = instance_selections

    @builtins.property
    def instance_selections(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections"]]]:
        '''instance_selections block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#instance_selections GoogleComputeRegionInstanceGroupManager#instance_selections}
        '''
        result = self._values.get("instance_selections")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections",
    jsii_struct_bases=[],
    name_mapping={"machine_types": "machineTypes", "name": "name", "rank": "rank"},
)
class GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections:
    def __init__(
        self,
        *,
        machine_types: typing.Sequence[builtins.str],
        name: builtins.str,
        rank: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param machine_types: Full machine-type names, e.g. "n1-standard-16". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#machine_types GoogleComputeRegionInstanceGroupManager#machine_types}
        :param name: Instance selection name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#name GoogleComputeRegionInstanceGroupManager#name}
        :param rank: Preference of this instance selection. Lower number means higher preference. MIG will first try to create a VM based on the machine-type with lowest rank and fallback to next rank based on availability. Machine types and instance selections with the same rank have the same preference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#rank GoogleComputeRegionInstanceGroupManager#rank}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0639a8a71f063bc254aaaee91a7a035a63ca9f807434063bd52d1426eeaaba5b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#machine_types GoogleComputeRegionInstanceGroupManager#machine_types}
        '''
        result = self._values.get("machine_types")
        assert result is not None, "Required property 'machine_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Instance selection name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#name GoogleComputeRegionInstanceGroupManager#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rank(self) -> typing.Optional[jsii.Number]:
        '''Preference of this instance selection.

        Lower number means higher preference. MIG will first try to create a VM based on the machine-type with lowest rank and fallback to next rank based on availability. Machine types and instance selections with the same rank have the same preference.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#rank GoogleComputeRegionInstanceGroupManager#rank}
        '''
        result = self._values.get("rank")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__797184d6cfd6bada17d335c96888cf26149e9a57dd405585e7970b8e7f0cc232)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__925c77503369e1f1062739d398192eda0dbd6486a41e526f60af724a1419a64d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c53ed9e10d3b40302d055f32ba73703739b07e407184543b320bc3c25f3c890a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0e60726ae6e664094b8bcacdb173b1b3492a74474a36bc62533e944067a2264)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12b6d2728029cfcc5a1d67ba03f18da1a51686c10a6c09b95427185a5f0671a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54cc52e3e45e4cc3cf8aa0b9c8b2baed73a3d4c7248eb397d79c7fbf3bd02787)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0e70a99585499c2db94ac88492e900ede22db37b95f25c1bcbab43e2637914a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0c12c0d72c98242ac229f7ad3524f3c5e532e4d6ebcb4eba4f68f5c832f0ce6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68c6bf20c6a6748f377e996a554fc898fbf618754a34b38d516387cf990f6b19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rank")
    def rank(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rank"))

    @rank.setter
    def rank(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03970d3c11c22a4f86747156b2dae807ce1da3d0d8360d1e440bdc85a986aa99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rank", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__495a1add70f2c5f5c8824c5d89da1a3537b0006bed7334e81800b8e26e8d1758)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c08b886c16ad7f93812554a0d40f9fbdcfda1db282be62f51837707150a02430)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInstanceSelections")
    def put_instance_selections(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8288ae5d3c98396e0a2e0b83855a2330ffb42b85d6834cc24e4a79c8c148cebe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInstanceSelections", [value]))

    @jsii.member(jsii_name="resetInstanceSelections")
    def reset_instance_selections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceSelections", []))

    @builtins.property
    @jsii.member(jsii_name="instanceSelections")
    def instance_selections(
        self,
    ) -> GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelectionsList:
        return typing.cast(GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelectionsList, jsii.get(self, "instanceSelections"))

    @builtins.property
    @jsii.member(jsii_name="instanceSelectionsInput")
    def instance_selections_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections]]], jsii.get(self, "instanceSelectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy]:
        return typing.cast(typing.Optional[GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b9c2932772407598a7ba947df045405f9b05383f13eed22f8490b8f23dabfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "default_action_on_failure": "defaultActionOnFailure",
        "force_update_on_repair": "forceUpdateOnRepair",
        "on_failed_health_check": "onFailedHealthCheck",
    },
)
class GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicy:
    def __init__(
        self,
        *,
        default_action_on_failure: typing.Optional[builtins.str] = None,
        force_update_on_repair: typing.Optional[builtins.str] = None,
        on_failed_health_check: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_action_on_failure: Specifies the action that a MIG performs on a failed VM. If the value of the "on_failed_health_check" field is DEFAULT_ACTION, then the same action also applies to the VMs on which your application fails a health check. Valid values are: REPAIR, DO_NOTHING. If REPAIR (default), then MIG automatically repairs a failed VM by recreating it. For more information, see about repairing VMs in a MIG. If DO_NOTHING, then MIG does not repair a failed VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#default_action_on_failure GoogleComputeRegionInstanceGroupManager#default_action_on_failure}
        :param force_update_on_repair: Specifies whether to apply the group's latest configuration when repairing a VM. Valid options are: YES, NO. If YES and you updated the group's instance template or per-instance configurations after the VM was created, then these changes are applied when VM is repaired. If NO (default), then updates are applied in accordance with the group's update policy type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#force_update_on_repair GoogleComputeRegionInstanceGroupManager#force_update_on_repair}
        :param on_failed_health_check: Specifies the action that a MIG performs on an unhealthy VM. A VM is marked as unhealthy when the application running on that VM fails a health check. Valid values are: DEFAULT_ACTION, DO_NOTHING, REPAIR. If DEFAULT_ACTION (default), then MIG uses the same action configured for the "default_action_on_failure" field. If DO_NOTHING, then MIG does not repair unhealthy VM. If REPAIR, then MIG automatically repairs an unhealthy VM by recreating it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#on_failed_health_check GoogleComputeRegionInstanceGroupManager#on_failed_health_check}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a43d6ce2ad057dfe867bca3256de83a937089e55518f71fc01141b9a05ceb2d8)
            check_type(argname="argument default_action_on_failure", value=default_action_on_failure, expected_type=type_hints["default_action_on_failure"])
            check_type(argname="argument force_update_on_repair", value=force_update_on_repair, expected_type=type_hints["force_update_on_repair"])
            check_type(argname="argument on_failed_health_check", value=on_failed_health_check, expected_type=type_hints["on_failed_health_check"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_action_on_failure is not None:
            self._values["default_action_on_failure"] = default_action_on_failure
        if force_update_on_repair is not None:
            self._values["force_update_on_repair"] = force_update_on_repair
        if on_failed_health_check is not None:
            self._values["on_failed_health_check"] = on_failed_health_check

    @builtins.property
    def default_action_on_failure(self) -> typing.Optional[builtins.str]:
        '''Specifies the action that a MIG performs on a failed VM.

        If the value of the "on_failed_health_check" field is DEFAULT_ACTION, then the same action also applies to the VMs on which your application fails a health check. Valid values are: REPAIR, DO_NOTHING. If REPAIR (default), then MIG automatically repairs a failed VM by recreating it. For more information, see about repairing VMs in a MIG. If DO_NOTHING, then MIG does not repair a failed VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#default_action_on_failure GoogleComputeRegionInstanceGroupManager#default_action_on_failure}
        '''
        result = self._values.get("default_action_on_failure")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_update_on_repair(self) -> typing.Optional[builtins.str]:
        '''Specifies whether to apply the group's latest configuration when repairing a VM.

        Valid options are: YES, NO. If YES and you updated the group's instance template or per-instance configurations after the VM was created, then these changes are applied when VM is repaired. If NO (default), then updates are applied in accordance with the group's update policy type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#force_update_on_repair GoogleComputeRegionInstanceGroupManager#force_update_on_repair}
        '''
        result = self._values.get("force_update_on_repair")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_failed_health_check(self) -> typing.Optional[builtins.str]:
        '''Specifies the action that a MIG performs on an unhealthy VM.

        A VM is marked as unhealthy when the application running on that VM fails a health check. Valid values are: DEFAULT_ACTION, DO_NOTHING, REPAIR. If DEFAULT_ACTION (default), then MIG uses the same action configured for the  "default_action_on_failure" field. If DO_NOTHING, then MIG does not repair unhealthy VM. If REPAIR, then MIG automatically repairs an unhealthy VM by recreating it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#on_failed_health_check GoogleComputeRegionInstanceGroupManager#on_failed_health_check}
        '''
        result = self._values.get("on_failed_health_check")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc84089bc785d17a0e158bf3070008cae89d833536b2768948ddcab97ecfc474)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDefaultActionOnFailure")
    def reset_default_action_on_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultActionOnFailure", []))

    @jsii.member(jsii_name="resetForceUpdateOnRepair")
    def reset_force_update_on_repair(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceUpdateOnRepair", []))

    @jsii.member(jsii_name="resetOnFailedHealthCheck")
    def reset_on_failed_health_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnFailedHealthCheck", []))

    @builtins.property
    @jsii.member(jsii_name="defaultActionOnFailureInput")
    def default_action_on_failure_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultActionOnFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="forceUpdateOnRepairInput")
    def force_update_on_repair_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forceUpdateOnRepairInput"))

    @builtins.property
    @jsii.member(jsii_name="onFailedHealthCheckInput")
    def on_failed_health_check_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onFailedHealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultActionOnFailure")
    def default_action_on_failure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultActionOnFailure"))

    @default_action_on_failure.setter
    def default_action_on_failure(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c24bc404f230f2b5d59fb2575db71459704f04d2a99f84af1738bab5e58d47b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultActionOnFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceUpdateOnRepair")
    def force_update_on_repair(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forceUpdateOnRepair"))

    @force_update_on_repair.setter
    def force_update_on_repair(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__094190abfe9aa1e10104a2be69f8accfa4565f31a4d604dc3611e3c106f82598)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceUpdateOnRepair", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onFailedHealthCheck")
    def on_failed_health_check(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onFailedHealthCheck"))

    @on_failed_health_check.setter
    def on_failed_health_check(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4cd294a06e0a584ee0ed9d8c7582e9ee70255d5df2e0d6b5b139a6e1a2a4df2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onFailedHealthCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicy]:
        return typing.cast(typing.Optional[GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__790af31565466be8b9755e6fbe1d73c56d7da839a0b9ba17cf7d6d164d2fa8a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerNamedPort",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "port": "port"},
)
class GoogleComputeRegionInstanceGroupManagerNamedPort:
    def __init__(self, *, name: builtins.str, port: jsii.Number) -> None:
        '''
        :param name: The name of the port. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#name GoogleComputeRegionInstanceGroupManager#name}
        :param port: The port number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#port GoogleComputeRegionInstanceGroupManager#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db259ee0ef1c4852842f216d26d7c79a5a19304e73dff134892c92c22bb3d1d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "port": port,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the port.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#name GoogleComputeRegionInstanceGroupManager#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''The port number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#port GoogleComputeRegionInstanceGroupManager#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionInstanceGroupManagerNamedPort(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionInstanceGroupManagerNamedPortList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerNamedPortList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efadfe113c8f35e1dd6aa520d206d47ede32fcf26028da590bdc2d025c7a7b80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeRegionInstanceGroupManagerNamedPortOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d6b60f6b70b2ed20b39a89f7a3e55f13d5fcc5d7cd740f44be3c78a64574c0c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeRegionInstanceGroupManagerNamedPortOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24be34e9a899dc12487f272dc7bfe5983565b2960a7383c6ff978b7733302350)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cdef440384f54d75d61c7d47e8d339612244c08be07ff85074bacb60800b46f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc5d1e77a0e2ee5c5c5eb17ac671b574ea98ff6ed84814909c3c1ea156f9df52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerNamedPort]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerNamedPort]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerNamedPort]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a08d0817cd8d5024fafb0c7dc459311d840741ab3bde397787f7e76c8ae4c63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionInstanceGroupManagerNamedPortOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerNamedPortOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a707fdc6ee3bae690fa43a8aa85d6d4cacf1383617e4d874e0b56c3cb83343a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a05c6eeaaa78940cf19fb36cc47e0e4cb7cb8c0653ed6f70f7958498a82030ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89bec44214e02e00ab7ac494b604f57aaf5459b4cb6e8a1eb0ef9f92dfd022db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerNamedPort]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerNamedPort]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerNamedPort]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd9358d9d57837ba08c5d8aee276a231689ade73771005755d095b357e278d36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerParams",
    jsii_struct_bases=[],
    name_mapping={"resource_manager_tags": "resourceManagerTags"},
)
class GoogleComputeRegionInstanceGroupManagerParams:
    def __init__(
        self,
        *,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param resource_manager_tags: Resource manager tags to bind to the managed instance group. The tags are key-value pairs. Keys must be in the format tagKeys/123 and values in the format tagValues/456. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#resource_manager_tags GoogleComputeRegionInstanceGroupManager#resource_manager_tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91d9fe85262072db14d7b2fbff591d2bac26c673ef222a707bbbf3f152b4c4d3)
            check_type(argname="argument resource_manager_tags", value=resource_manager_tags, expected_type=type_hints["resource_manager_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_manager_tags is not None:
            self._values["resource_manager_tags"] = resource_manager_tags

    @builtins.property
    def resource_manager_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Resource manager tags to bind to the managed instance group.

        The tags are key-value pairs. Keys must be in the format tagKeys/123 and values in the format tagValues/456.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#resource_manager_tags GoogleComputeRegionInstanceGroupManager#resource_manager_tags}
        '''
        result = self._values.get("resource_manager_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionInstanceGroupManagerParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionInstanceGroupManagerParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b18e33c698f8c32b685000e37c316ad6a7b7f5b4161efe923cad4e0263de3a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetResourceManagerTags")
    def reset_resource_manager_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceManagerTags", []))

    @builtins.property
    @jsii.member(jsii_name="resourceManagerTagsInput")
    def resource_manager_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "resourceManagerTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceManagerTags")
    def resource_manager_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "resourceManagerTags"))

    @resource_manager_tags.setter
    def resource_manager_tags(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a11e07a61f3ac431ea9f5e34275434c5d01e71991c4445a6bcc47edc46f740c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceManagerTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionInstanceGroupManagerParams]:
        return typing.cast(typing.Optional[GoogleComputeRegionInstanceGroupManagerParams], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionInstanceGroupManagerParams],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb049514f0eb7f35ddd7f9b4756017b89eb14959bb7c1aee758afa23b5eac97e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStandbyPolicy",
    jsii_struct_bases=[],
    name_mapping={"initial_delay_sec": "initialDelaySec", "mode": "mode"},
)
class GoogleComputeRegionInstanceGroupManagerStandbyPolicy:
    def __init__(
        self,
        *,
        initial_delay_sec: typing.Optional[jsii.Number] = None,
        mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param initial_delay_sec: Specifies the number of seconds that the MIG should wait to suspend or stop a VM after that VM was created. The initial delay gives the initialization script the time to prepare your VM for a quick scale out. The value of initial delay must be between 0 and 3600 seconds. The default value is 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#initial_delay_sec GoogleComputeRegionInstanceGroupManager#initial_delay_sec}
        :param mode: Defines how a MIG resumes or starts VMs from a standby pool when the group scales out. The default mode is "MANUAL". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#mode GoogleComputeRegionInstanceGroupManager#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc3776f1c81886d5fa40376c928f69a0add48e3f5855ab14d1d7d0cc74aba4c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#initial_delay_sec GoogleComputeRegionInstanceGroupManager#initial_delay_sec}
        '''
        result = self._values.get("initial_delay_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Defines how a MIG resumes or starts VMs from a standby pool when the group scales out.

        The default mode is "MANUAL".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#mode GoogleComputeRegionInstanceGroupManager#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionInstanceGroupManagerStandbyPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionInstanceGroupManagerStandbyPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStandbyPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cc5bd28404cf19c1ee5f70ba8e971bf0f1c5ecbae85f5dc3dd2982eab64207d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__186710b4fcd16a16abc939ced58d9a026cdddc9a35b4a5909c7b86f1a844e336)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelaySec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e3fa1b45e0962c4243b1f33ac8d354e724ff7ca6b2acd72937a323f21144111)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionInstanceGroupManagerStandbyPolicy]:
        return typing.cast(typing.Optional[GoogleComputeRegionInstanceGroupManagerStandbyPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionInstanceGroupManagerStandbyPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eddccd7a8e4533a332ca13d320d22133502d88978e3282779e1aa717f91101e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatefulDisk",
    jsii_struct_bases=[],
    name_mapping={"device_name": "deviceName", "delete_rule": "deleteRule"},
)
class GoogleComputeRegionInstanceGroupManagerStatefulDisk:
    def __init__(
        self,
        *,
        device_name: builtins.str,
        delete_rule: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param device_name: The device name of the disk to be attached. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#device_name GoogleComputeRegionInstanceGroupManager#device_name}
        :param delete_rule: A value that prescribes what should happen to the stateful disk when the VM instance is deleted. The available options are NEVER and ON_PERMANENT_INSTANCE_DELETION. NEVER - detach the disk when the VM is deleted, but do not delete the disk. ON_PERMANENT_INSTANCE_DELETION will delete the stateful disk when the VM is permanently deleted from the instance group. The default is NEVER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#delete_rule GoogleComputeRegionInstanceGroupManager#delete_rule}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b5e268b6689fd64f89e09cc39570132efac2e85972aaf98791c89d915acb63)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#device_name GoogleComputeRegionInstanceGroupManager#device_name}
        '''
        result = self._values.get("device_name")
        assert result is not None, "Required property 'device_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def delete_rule(self) -> typing.Optional[builtins.str]:
        '''A value that prescribes what should happen to the stateful disk when the VM instance is deleted.

        The available options are NEVER and ON_PERMANENT_INSTANCE_DELETION. NEVER - detach the disk when the VM is deleted, but do not delete the disk. ON_PERMANENT_INSTANCE_DELETION will delete the stateful disk when the VM is permanently deleted from the instance group. The default is NEVER.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#delete_rule GoogleComputeRegionInstanceGroupManager#delete_rule}
        '''
        result = self._values.get("delete_rule")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionInstanceGroupManagerStatefulDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionInstanceGroupManagerStatefulDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatefulDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36bebae3a448537310ffd1e560a00728f7935715a7629018b51c6c9656db4534)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeRegionInstanceGroupManagerStatefulDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b17e22e6d041865b2308dcd920676ce5abe6d221825daa2bb6f6cf9766a544a5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeRegionInstanceGroupManagerStatefulDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__005b7584423a8b9f298eefaaa80a15e882ff74422df689fb3a992ab6ba822ada)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f03ea565ff87fe6ee07643ecfb8af3a9295d8934b2c121c455598a48838a8a85)
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
            type_hints = typing.get_type_hints(_typecheckingstub__555aacc16e4b60aadcfe0dc4acb3bed2eab688df75a4c36166b2c998046012f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerStatefulDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerStatefulDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerStatefulDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd7055e0234073164f30c72278729650ffaeabbe50e1d38ef36acace9c8991e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionInstanceGroupManagerStatefulDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatefulDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__301c0da0084fa7b3d8c36f39e516a75999bd9e00893f15791b2f4c58ec7c945e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a2159d1896f13b2812e3855488049990058affcbfdaddf961cb9d5a5266a730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteRule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceName")
    def device_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceName"))

    @device_name.setter
    def device_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5197120aeaeedab71c3829b483f8763727269fd56b86863cff90df8e41affa6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerStatefulDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerStatefulDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerStatefulDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1035616c54257a4dbaed986f9f95a9ea1ce646afe015d7e1e17f9098b2f3583)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatefulExternalIp",
    jsii_struct_bases=[],
    name_mapping={"delete_rule": "deleteRule", "interface_name": "interfaceName"},
)
class GoogleComputeRegionInstanceGroupManagerStatefulExternalIp:
    def __init__(
        self,
        *,
        delete_rule: typing.Optional[builtins.str] = None,
        interface_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delete_rule: A value that prescribes what should happen to an associated static Address resource when a VM instance is permanently deleted. The available options are NEVER and ON_PERMANENT_INSTANCE_DELETION. NEVER - detach the IP when the VM is deleted, but do not delete the address resource. ON_PERMANENT_INSTANCE_DELETION will delete the stateful address when the VM is permanently deleted from the instance group. The default is NEVER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#delete_rule GoogleComputeRegionInstanceGroupManager#delete_rule}
        :param interface_name: The network interface name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#interface_name GoogleComputeRegionInstanceGroupManager#interface_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7181185e3d8c51d72e1605a968ab07ab8aea083640364386c0f4b2c8e6b99a92)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#delete_rule GoogleComputeRegionInstanceGroupManager#delete_rule}
        '''
        result = self._values.get("delete_rule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interface_name(self) -> typing.Optional[builtins.str]:
        '''The network interface name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#interface_name GoogleComputeRegionInstanceGroupManager#interface_name}
        '''
        result = self._values.get("interface_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionInstanceGroupManagerStatefulExternalIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionInstanceGroupManagerStatefulExternalIpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatefulExternalIpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81141909af5911d433d4cc938691338da6452229aa6c043d9e64349f15271d00)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeRegionInstanceGroupManagerStatefulExternalIpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__877e10d652ed19fc538631fdd6a72e6e58b23b1f0c26f16020169aae6823e822)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeRegionInstanceGroupManagerStatefulExternalIpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__629b41c1440c0d164618a5921f1d37cdc2ef9adbe760dddb0e2f5c00a904da0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e76d1647e02f0754c76845604ce19f32e3e5f3a55095f5dcedd96114096e668)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc295eebf7208f412ca72bc22e6af54c96285f04d4ffed05dff87f4ae1d01c2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerStatefulExternalIp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerStatefulExternalIp]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerStatefulExternalIp]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba827cfd0cd7aa52e78ce27d20e1af283e2ec25eb04a97548385cead1f8a5fc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionInstanceGroupManagerStatefulExternalIpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatefulExternalIpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a5018c70ccd0bbcc27c1383304e5b8142c9fa83523ccfe4af0cb76de63b95fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10afb2aa0aa08d4207cf8e3a459a8974b4d3d76316856195a199c4b299c628bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteRule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interfaceName")
    def interface_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interfaceName"))

    @interface_name.setter
    def interface_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c13774139df593877fb91af153ee510908a15cc6761e0bbd9d45b5990d65b461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interfaceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerStatefulExternalIp]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerStatefulExternalIp]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerStatefulExternalIp]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ac6473562eb3a92779369f72fc09e062d6fc01ca10c42f14941d79859209456)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatefulInternalIp",
    jsii_struct_bases=[],
    name_mapping={"delete_rule": "deleteRule", "interface_name": "interfaceName"},
)
class GoogleComputeRegionInstanceGroupManagerStatefulInternalIp:
    def __init__(
        self,
        *,
        delete_rule: typing.Optional[builtins.str] = None,
        interface_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delete_rule: A value that prescribes what should happen to an associated static Address resource when a VM instance is permanently deleted. The available options are NEVER and ON_PERMANENT_INSTANCE_DELETION. NEVER - detach the IP when the VM is deleted, but do not delete the address resource. ON_PERMANENT_INSTANCE_DELETION will delete the stateful address when the VM is permanently deleted from the instance group. The default is NEVER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#delete_rule GoogleComputeRegionInstanceGroupManager#delete_rule}
        :param interface_name: The network interface name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#interface_name GoogleComputeRegionInstanceGroupManager#interface_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab25919d2ef08b78df2988d49d85ce71ff7f0bab4be959183b03ccb338de0511)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#delete_rule GoogleComputeRegionInstanceGroupManager#delete_rule}
        '''
        result = self._values.get("delete_rule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interface_name(self) -> typing.Optional[builtins.str]:
        '''The network interface name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#interface_name GoogleComputeRegionInstanceGroupManager#interface_name}
        '''
        result = self._values.get("interface_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionInstanceGroupManagerStatefulInternalIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionInstanceGroupManagerStatefulInternalIpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatefulInternalIpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66d6aee2e2f25d72887dbd4be12b7f3780260d35bcc45a880b182eadadddd368)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeRegionInstanceGroupManagerStatefulInternalIpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__823ad6a05453422863def9cc2858787430b402a65759e34bad6536813c4b8a07)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeRegionInstanceGroupManagerStatefulInternalIpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96fea8315bfb4dc57fb6cb2b83eaff00ee911e34f091236e1c883728caa0df12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fc80f129392c4bc1813ffddf253fd2cf2168055ffa4b3e89ebd7f953b415523)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a73aac20c436b8fdffe2c3d97428f9b6fe58ae02998a0fecec07b0f6cbec2910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerStatefulInternalIp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerStatefulInternalIp]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerStatefulInternalIp]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e71b3c650c7992752a7df3ace53443fc16de804f8df9a4bd59c8ce166d50464d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionInstanceGroupManagerStatefulInternalIpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatefulInternalIpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8586b626a676054d75df50499d1fc81e5f3520af30884071e4a20fe72df12ed7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49f53f0c8d779bdfd52f44533b544ade9f6fe1dcb665bc3675e2426a5cc13ace)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteRule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interfaceName")
    def interface_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interfaceName"))

    @interface_name.setter
    def interface_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f26f9443c96cc0511883b334a59ee14ee950f1e95724daff670e35a1592fbfda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interfaceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerStatefulInternalIp]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerStatefulInternalIp]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerStatefulInternalIp]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__684337e69ae7598a92993df2a1d8b0b91119d61e8c9d6ae471afebaabfbec362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleComputeRegionInstanceGroupManagerStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionInstanceGroupManagerStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatusAllInstancesConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleComputeRegionInstanceGroupManagerStatusAllInstancesConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionInstanceGroupManagerStatusAllInstancesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionInstanceGroupManagerStatusAllInstancesConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatusAllInstancesConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6be0eebd70a1c55fca0d838307b605e4a6fa70e832d6ce7cb39da28f46136443)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeRegionInstanceGroupManagerStatusAllInstancesConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44f2c3daea7d5b2c6c6be0047fa40b2c16fac10c81e6483c2617a747346a009b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeRegionInstanceGroupManagerStatusAllInstancesConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__292b3961ab6f43ead9527894cf0ef969fd13e0bf9b1661b490a7c73b809c6514)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ae0cf9de966e103fa7d90b46b9c277898c38767517c8d26b0bc283b96bb85fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36d92c51bafe4cd16b59c6af6d66569767a01cbd76cf1bca29c6256dc4242249)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionInstanceGroupManagerStatusAllInstancesConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatusAllInstancesConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0abdb196bf1248ba31b48ebde1dc46a79e125a55759ec87fa1c4cbd9a6f033bc)
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
    ) -> typing.Optional[GoogleComputeRegionInstanceGroupManagerStatusAllInstancesConfig]:
        return typing.cast(typing.Optional[GoogleComputeRegionInstanceGroupManagerStatusAllInstancesConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionInstanceGroupManagerStatusAllInstancesConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa3ac59513ffb6c265046144eda1df47185c39a2cb4bd77a630aa7f592a53483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionInstanceGroupManagerStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64192be145fe93649515a753a47ca4d5ba7b633bc1dccd51c6bffb1af37cbc97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeRegionInstanceGroupManagerStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572d4c1248e6fe54782bc66a9bf96b79087f70491b9798e31bb06a8f8ed47305)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeRegionInstanceGroupManagerStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b98a7e38a6314fe325211b6266a026a65c8fe204f68af2c4fa4f2c83514f8bd4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e108276611d269f1ac52b0cc08cd178dbd880d30b7cee09862a87fee6c7307fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__203eb609d4baa309a38532f0b03103a82f7d1f94bbaf30d70f7512c49f9e82e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionInstanceGroupManagerStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e966324b482924b3670f0432350d1f6e80f6218c1cb846e31af78ff144351126)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allInstancesConfig")
    def all_instances_config(
        self,
    ) -> GoogleComputeRegionInstanceGroupManagerStatusAllInstancesConfigList:
        return typing.cast(GoogleComputeRegionInstanceGroupManagerStatusAllInstancesConfigList, jsii.get(self, "allInstancesConfig"))

    @builtins.property
    @jsii.member(jsii_name="isStable")
    def is_stable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isStable"))

    @builtins.property
    @jsii.member(jsii_name="stateful")
    def stateful(self) -> "GoogleComputeRegionInstanceGroupManagerStatusStatefulList":
        return typing.cast("GoogleComputeRegionInstanceGroupManagerStatusStatefulList", jsii.get(self, "stateful"))

    @builtins.property
    @jsii.member(jsii_name="versionTarget")
    def version_target(
        self,
    ) -> "GoogleComputeRegionInstanceGroupManagerStatusVersionTargetList":
        return typing.cast("GoogleComputeRegionInstanceGroupManagerStatusVersionTargetList", jsii.get(self, "versionTarget"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionInstanceGroupManagerStatus]:
        return typing.cast(typing.Optional[GoogleComputeRegionInstanceGroupManagerStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionInstanceGroupManagerStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5acc2a83e511461b73389904d39354177427b9be658c08fb4d04ec1e0fdb2623)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatusStateful",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleComputeRegionInstanceGroupManagerStatusStateful:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionInstanceGroupManagerStatusStateful(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionInstanceGroupManagerStatusStatefulList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatusStatefulList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a42faf4c7494f5c911a19c3dedec6f7dbf54282427f2155a9afa0bf963052bcc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeRegionInstanceGroupManagerStatusStatefulOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50ad690a2830eb1f9ea165d273d46319889f366fb263ff458d33d474f4c74985)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeRegionInstanceGroupManagerStatusStatefulOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e66b03d762b6b60b9ea072ff4149d6a8fca115e55941a2e2977148b2dbb34fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01f840a1dd6179f29d3d4f7cc6ebceaa5ac3ecf1255af6ea9802b4d8d0ad2397)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe520b433dbe561d49d4678b8e44b13ab40d9356542588360b19e13ca32ba451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionInstanceGroupManagerStatusStatefulOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatusStatefulOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30985a4e26dffd427eb0bd829d0ff6846290affc6db6c23803b10b9902543ef1)
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
    ) -> "GoogleComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigsList":
        return typing.cast("GoogleComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigsList", jsii.get(self, "perInstanceConfigs"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionInstanceGroupManagerStatusStateful]:
        return typing.cast(typing.Optional[GoogleComputeRegionInstanceGroupManagerStatusStateful], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionInstanceGroupManagerStatusStateful],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a84b04541a9405a73a32d3c53d2980a68e8a2a9da3d8bfb0b6bf5e49e0c6c49a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigs",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigs:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__577aceac9dc36d3b9345ea5e97a33f1fdc18b54d4f1e39b068c023251429d770)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26bbbd79a4e687cc0cd7903fc9bcfaec0dc584bec98a0ee178705f5a35a18d79)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eb76b3c5233597f41b6938e667742e77b016d21d6d9aa72be7b64724d053400)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2c45f3cee64ffce60668c49f194ae5a245b126751984aff60c4a294fbbbaa9d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cf81cf1130760b6c4b8b539f4221ecef40c8ac1310a96bca5204e2b3afb90f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3efac696aff0186c2b81fca509b6172ea5c23237e8c3b81fdc70e61b68840edc)
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
    ) -> typing.Optional[GoogleComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigs]:
        return typing.cast(typing.Optional[GoogleComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0b700ff6b5ae140ff1983dc68d91856bd2be81e40c208b7ec5363217887364e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatusVersionTarget",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleComputeRegionInstanceGroupManagerStatusVersionTarget:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionInstanceGroupManagerStatusVersionTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionInstanceGroupManagerStatusVersionTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatusVersionTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df81cae8416827b56e0b1ad9963e70b0d0c0925a31f530980add11b673a09a59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeRegionInstanceGroupManagerStatusVersionTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__420e779cc3132d71872b1920d8fa1d9462ee9ee3987ddcd6a317529fcf0c27c6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeRegionInstanceGroupManagerStatusVersionTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d93291a947ef4db9ff7b0e58d4078cb3c9d93ab0dace176d254a1a4be8c638a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11ba95d0ff250520d57503601633c5e27cbbe442f9fc98ae0f7751a5f1f9ea12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e634e474df7c0b27a61e2c5d293efe0ffd81b5ef81bc4b529e9e0a2d5f3c769c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionInstanceGroupManagerStatusVersionTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerStatusVersionTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cb8ae3693013169b6cebc31077c0a4080e5568ed6f2a55ed282f27c91e660b7)
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
    ) -> typing.Optional[GoogleComputeRegionInstanceGroupManagerStatusVersionTarget]:
        return typing.cast(typing.Optional[GoogleComputeRegionInstanceGroupManagerStatusVersionTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionInstanceGroupManagerStatusVersionTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66fde5ed050f523c07b59631f1b86e5db05808961eea5b7b07c221bb3bcaccbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleComputeRegionInstanceGroupManagerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#create GoogleComputeRegionInstanceGroupManager#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#delete GoogleComputeRegionInstanceGroupManager#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#update GoogleComputeRegionInstanceGroupManager#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1327daf235603cabde348de3765128d081ac0b4d8f54e6b0e921238cdd205336)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#create GoogleComputeRegionInstanceGroupManager#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#delete GoogleComputeRegionInstanceGroupManager#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#update GoogleComputeRegionInstanceGroupManager#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionInstanceGroupManagerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionInstanceGroupManagerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba425b10b02b14736c5b6d2aae9a25fad0753876029725d9c88a37f5af8dc216)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cbb91d7eb994fcc644beb6783570f81ab6a8ceba2b37dff326a8ef2b0844cdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb95e571cba7f5310146f4e4ca43638e347a8d58f484f365a54ec57f3bc8d75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adbfcd6a317faac1311671541ee4b086c0cdc8356344798fbba41986ed03e88e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb82b915fddc37b0fa32cb998ff70026ea763bcd51ebd6c1e96d7645dfc32d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerUpdatePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "minimal_action": "minimalAction",
        "type": "type",
        "instance_redistribution_type": "instanceRedistributionType",
        "max_surge_fixed": "maxSurgeFixed",
        "max_surge_percent": "maxSurgePercent",
        "max_unavailable_fixed": "maxUnavailableFixed",
        "max_unavailable_percent": "maxUnavailablePercent",
        "min_ready_sec": "minReadySec",
        "most_disruptive_allowed_action": "mostDisruptiveAllowedAction",
        "replacement_method": "replacementMethod",
    },
)
class GoogleComputeRegionInstanceGroupManagerUpdatePolicy:
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
        min_ready_sec: typing.Optional[jsii.Number] = None,
        most_disruptive_allowed_action: typing.Optional[builtins.str] = None,
        replacement_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param minimal_action: Minimal action to be taken on an instance. You can specify either NONE to forbid any actions, REFRESH to update without stopping instances, RESTART to restart existing instances or REPLACE to delete and create new instances from the target template. If you specify a REFRESH, the Updater will attempt to perform that action only. However, if the Updater determines that the minimal action you specify is not enough to perform the update, it might perform a more disruptive action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#minimal_action GoogleComputeRegionInstanceGroupManager#minimal_action}
        :param type: The type of update process. You can specify either PROACTIVE so that the instance group manager proactively executes actions in order to bring instances to their target versions or OPPORTUNISTIC so that no action is proactively executed but the update will be performed as part of other actions (for example, resizes or recreateInstances calls). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#type GoogleComputeRegionInstanceGroupManager#type}
        :param instance_redistribution_type: The instance redistribution policy for regional managed instance groups. Valid values are: "PROACTIVE", "NONE". If PROACTIVE (default), the group attempts to maintain an even distribution of VM instances across zones in the region. If NONE, proactive redistribution is disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#instance_redistribution_type GoogleComputeRegionInstanceGroupManager#instance_redistribution_type}
        :param max_surge_fixed: Specifies a fixed number of VM instances. This must be a positive integer. Conflicts with max_surge_percent. Both cannot be 0 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#max_surge_fixed GoogleComputeRegionInstanceGroupManager#max_surge_fixed}
        :param max_surge_percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Conflicts with max_surge_fixed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#max_surge_percent GoogleComputeRegionInstanceGroupManager#max_surge_percent}
        :param max_unavailable_fixed: Specifies a fixed number of VM instances. This must be a positive integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#max_unavailable_fixed GoogleComputeRegionInstanceGroupManager#max_unavailable_fixed}
        :param max_unavailable_percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#max_unavailable_percent GoogleComputeRegionInstanceGroupManager#max_unavailable_percent}
        :param min_ready_sec: Minimum number of seconds to wait for after a newly created instance becomes available. This value must be from range [0, 3600]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#min_ready_sec GoogleComputeRegionInstanceGroupManager#min_ready_sec}
        :param most_disruptive_allowed_action: Most disruptive action that is allowed to be taken on an instance. You can specify either NONE to forbid any actions, REFRESH to allow actions that do not need instance restart, RESTART to allow actions that can be applied without instance replacing or REPLACE to allow all possible actions. If the Updater determines that the minimal update action needed is more disruptive than most disruptive allowed action you specify it will not perform the update at all. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#most_disruptive_allowed_action GoogleComputeRegionInstanceGroupManager#most_disruptive_allowed_action}
        :param replacement_method: The instance replacement method for regional managed instance groups. Valid values are: "RECREATE", "SUBSTITUTE". If SUBSTITUTE (default), the group replaces VM instances with new instances that have randomly generated names. If RECREATE, instance names are preserved. You must also set max_unavailable_fixed or max_unavailable_percent to be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#replacement_method GoogleComputeRegionInstanceGroupManager#replacement_method}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faebc8ce6ce799806dace26d82cf41c12ab4602b766b5b6fa1a1c99714b0a51c)
            check_type(argname="argument minimal_action", value=minimal_action, expected_type=type_hints["minimal_action"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument instance_redistribution_type", value=instance_redistribution_type, expected_type=type_hints["instance_redistribution_type"])
            check_type(argname="argument max_surge_fixed", value=max_surge_fixed, expected_type=type_hints["max_surge_fixed"])
            check_type(argname="argument max_surge_percent", value=max_surge_percent, expected_type=type_hints["max_surge_percent"])
            check_type(argname="argument max_unavailable_fixed", value=max_unavailable_fixed, expected_type=type_hints["max_unavailable_fixed"])
            check_type(argname="argument max_unavailable_percent", value=max_unavailable_percent, expected_type=type_hints["max_unavailable_percent"])
            check_type(argname="argument min_ready_sec", value=min_ready_sec, expected_type=type_hints["min_ready_sec"])
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
        if min_ready_sec is not None:
            self._values["min_ready_sec"] = min_ready_sec
        if most_disruptive_allowed_action is not None:
            self._values["most_disruptive_allowed_action"] = most_disruptive_allowed_action
        if replacement_method is not None:
            self._values["replacement_method"] = replacement_method

    @builtins.property
    def minimal_action(self) -> builtins.str:
        '''Minimal action to be taken on an instance.

        You can specify either NONE to forbid any actions, REFRESH to update without stopping instances, RESTART to restart existing instances or REPLACE to delete and create new instances from the target template. If you specify a REFRESH, the Updater will attempt to perform that action only. However, if the Updater determines that the minimal action you specify is not enough to perform the update, it might perform a more disruptive action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#minimal_action GoogleComputeRegionInstanceGroupManager#minimal_action}
        '''
        result = self._values.get("minimal_action")
        assert result is not None, "Required property 'minimal_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of update process.

        You can specify either PROACTIVE so that the instance group manager proactively executes actions in order to bring instances to their target versions or OPPORTUNISTIC so that no action is proactively executed but the update will be performed as part of other actions (for example, resizes or recreateInstances calls).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#type GoogleComputeRegionInstanceGroupManager#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_redistribution_type(self) -> typing.Optional[builtins.str]:
        '''The instance redistribution policy for regional managed instance groups.

        Valid values are: "PROACTIVE", "NONE". If PROACTIVE (default), the group attempts to maintain an even distribution of VM instances across zones in the region. If NONE, proactive redistribution is disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#instance_redistribution_type GoogleComputeRegionInstanceGroupManager#instance_redistribution_type}
        '''
        result = self._values.get("instance_redistribution_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_surge_fixed(self) -> typing.Optional[jsii.Number]:
        '''Specifies a fixed number of VM instances.

        This must be a positive integer. Conflicts with max_surge_percent. Both cannot be 0

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#max_surge_fixed GoogleComputeRegionInstanceGroupManager#max_surge_fixed}
        '''
        result = self._values.get("max_surge_fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_surge_percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Conflicts with max_surge_fixed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#max_surge_percent GoogleComputeRegionInstanceGroupManager#max_surge_percent}
        '''
        result = self._values.get("max_surge_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_unavailable_fixed(self) -> typing.Optional[jsii.Number]:
        '''Specifies a fixed number of VM instances. This must be a positive integer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#max_unavailable_fixed GoogleComputeRegionInstanceGroupManager#max_unavailable_fixed}
        '''
        result = self._values.get("max_unavailable_fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_unavailable_percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#max_unavailable_percent GoogleComputeRegionInstanceGroupManager#max_unavailable_percent}
        '''
        result = self._values.get("max_unavailable_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_ready_sec(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of seconds to wait for after a newly created instance becomes available.

        This value must be from range [0, 3600].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#min_ready_sec GoogleComputeRegionInstanceGroupManager#min_ready_sec}
        '''
        result = self._values.get("min_ready_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def most_disruptive_allowed_action(self) -> typing.Optional[builtins.str]:
        '''Most disruptive action that is allowed to be taken on an instance.

        You can specify either NONE to forbid any actions, REFRESH to allow actions that do not need instance restart, RESTART to allow actions that can be applied without instance replacing or REPLACE to allow all possible actions. If the Updater determines that the minimal update action needed is more disruptive than most disruptive allowed action you specify it will not perform the update at all.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#most_disruptive_allowed_action GoogleComputeRegionInstanceGroupManager#most_disruptive_allowed_action}
        '''
        result = self._values.get("most_disruptive_allowed_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replacement_method(self) -> typing.Optional[builtins.str]:
        '''The instance replacement method for regional managed instance groups.

        Valid values are: "RECREATE", "SUBSTITUTE". If SUBSTITUTE (default), the group replaces VM instances with new instances that have randomly generated names. If RECREATE, instance names are preserved.  You must also set max_unavailable_fixed or max_unavailable_percent to be greater than 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#replacement_method GoogleComputeRegionInstanceGroupManager#replacement_method}
        '''
        result = self._values.get("replacement_method")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionInstanceGroupManagerUpdatePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionInstanceGroupManagerUpdatePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerUpdatePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fa41ee27d7a36457b5a00c14cb313e1c69b32286e317071971b867bea581515)
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

    @jsii.member(jsii_name="resetMinReadySec")
    def reset_min_ready_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinReadySec", []))

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
    @jsii.member(jsii_name="minReadySecInput")
    def min_ready_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minReadySecInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2ed28a2eb428494916554d60a52526ebd0fd78a51fae67d42afeffa65d19bf9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceRedistributionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxSurgeFixed")
    def max_surge_fixed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxSurgeFixed"))

    @max_surge_fixed.setter
    def max_surge_fixed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38f423db798c64283a0350f725ac75123e29681db70772e70fe21809e5ed1049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSurgeFixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxSurgePercent")
    def max_surge_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxSurgePercent"))

    @max_surge_percent.setter
    def max_surge_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df086bd4b0128e13faa036e8577419ce4f72b4abb3913c66ef866c72d9bea84c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSurgePercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUnavailableFixed")
    def max_unavailable_fixed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUnavailableFixed"))

    @max_unavailable_fixed.setter
    def max_unavailable_fixed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__014fbc8ca231c46323a9a0cb418dcce64ed25081e9c8a1fcfd8f6cd521eee7bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUnavailableFixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUnavailablePercent")
    def max_unavailable_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUnavailablePercent"))

    @max_unavailable_percent.setter
    def max_unavailable_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__945bd80a7c002549feeb140276f3d9b9aceb409bfb3ed416356b19b8b7604535)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUnavailablePercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimalAction")
    def minimal_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimalAction"))

    @minimal_action.setter
    def minimal_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6946b0bdc5667231234771554f416cc06d3a84015562f190dd8f672daa95e96a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimalAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minReadySec")
    def min_ready_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReadySec"))

    @min_ready_sec.setter
    def min_ready_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4026bd1ce887929174deefc27854e3ed58fac8c2ce78b2510254de3b828f9552)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReadySec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mostDisruptiveAllowedAction")
    def most_disruptive_allowed_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mostDisruptiveAllowedAction"))

    @most_disruptive_allowed_action.setter
    def most_disruptive_allowed_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9097fe5fc978278fc19304acecae87634301282a90611c573c1ade0f8ae49a36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mostDisruptiveAllowedAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replacementMethod")
    def replacement_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replacementMethod"))

    @replacement_method.setter
    def replacement_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2b889d252ce551fb9d315e5b5dff18098ade97e424ca0ee7b4b9623b057772d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replacementMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f0357088efb8395fb97e8296555e69bf739ed9c57e8f0d0877b12ba1ea725fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionInstanceGroupManagerUpdatePolicy]:
        return typing.cast(typing.Optional[GoogleComputeRegionInstanceGroupManagerUpdatePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionInstanceGroupManagerUpdatePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82e2476e1e17715c9217349d346ed9a3e8279ced348dbfbf813ed18a085f1207)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerVersion",
    jsii_struct_bases=[],
    name_mapping={
        "instance_template": "instanceTemplate",
        "name": "name",
        "target_size": "targetSize",
    },
)
class GoogleComputeRegionInstanceGroupManagerVersion:
    def __init__(
        self,
        *,
        instance_template: builtins.str,
        name: typing.Optional[builtins.str] = None,
        target_size: typing.Optional[typing.Union["GoogleComputeRegionInstanceGroupManagerVersionTargetSize", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param instance_template: The full URL to an instance template from which all new instances of this version will be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#instance_template GoogleComputeRegionInstanceGroupManager#instance_template}
        :param name: Version name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#name GoogleComputeRegionInstanceGroupManager#name}
        :param target_size: target_size block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#target_size GoogleComputeRegionInstanceGroupManager#target_size}
        '''
        if isinstance(target_size, dict):
            target_size = GoogleComputeRegionInstanceGroupManagerVersionTargetSize(**target_size)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d350450103c28769cf774cb9c00dd5c5a234db4a5ddb6a0b2d99871b645efa)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#instance_template GoogleComputeRegionInstanceGroupManager#instance_template}
        '''
        result = self._values.get("instance_template")
        assert result is not None, "Required property 'instance_template' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Version name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#name GoogleComputeRegionInstanceGroupManager#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_size(
        self,
    ) -> typing.Optional["GoogleComputeRegionInstanceGroupManagerVersionTargetSize"]:
        '''target_size block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#target_size GoogleComputeRegionInstanceGroupManager#target_size}
        '''
        result = self._values.get("target_size")
        return typing.cast(typing.Optional["GoogleComputeRegionInstanceGroupManagerVersionTargetSize"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionInstanceGroupManagerVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionInstanceGroupManagerVersionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerVersionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9e02bce5a8ba6958dde33198bda0631c397ae8d07fc495966d99eb6aa45c960)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeRegionInstanceGroupManagerVersionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68e03f6a49f2ffc3717de76e9d63dda91edba43b46642933e1e573a2ec79ab74)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeRegionInstanceGroupManagerVersionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbe21585240b3676fcce62ec3ef24fe850c731376c5c4e081e06f5165cf7857c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34601ccc4be0f686f149f50af71e60687d5f2116e5278e0c67c57f2f116e0847)
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
            type_hints = typing.get_type_hints(_typecheckingstub__35d5b3780b9c6c757493c93dff54931c8cbc1badb8f8b09817933985dabf8474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerVersion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerVersion]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerVersion]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__510af7fc22b1b61827d2c464e40de61ef069ba5bc251d5f6eca7e250491d308f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionInstanceGroupManagerVersionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerVersionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ac234f60ca972b22d7334e11d0ee97cb8e8534693aa7b1257f869f67626baae)
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
        :param fixed: The number of instances which are managed for this version. Conflicts with percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#fixed GoogleComputeRegionInstanceGroupManager#fixed}
        :param percent: The number of instances (calculated as percentage) which are managed for this version. Conflicts with fixed. Note that when using percent, rounding will be in favor of explicitly set target_size values; a managed instance group with 2 instances and 2 versions, one of which has a target_size.percent of 60 will create 2 instances of that version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#percent GoogleComputeRegionInstanceGroupManager#percent}
        '''
        value = GoogleComputeRegionInstanceGroupManagerVersionTargetSize(
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
    ) -> "GoogleComputeRegionInstanceGroupManagerVersionTargetSizeOutputReference":
        return typing.cast("GoogleComputeRegionInstanceGroupManagerVersionTargetSizeOutputReference", jsii.get(self, "targetSize"))

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
    ) -> typing.Optional["GoogleComputeRegionInstanceGroupManagerVersionTargetSize"]:
        return typing.cast(typing.Optional["GoogleComputeRegionInstanceGroupManagerVersionTargetSize"], jsii.get(self, "targetSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTemplate")
    def instance_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceTemplate"))

    @instance_template.setter
    def instance_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58053a01d98e5fcbc03243f235bda74599405f9357ac616ae42db796b179f95f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0914f96853b308d94befb91e0f842946038ee39c565f94b630bf6a5ac1db32ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerVersion]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerVersion]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerVersion]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c694b06f20b390ce9b63052bbfcc2d40160a3e8a1cba3f33c9c12c1a0d7a419e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerVersionTargetSize",
    jsii_struct_bases=[],
    name_mapping={"fixed": "fixed", "percent": "percent"},
)
class GoogleComputeRegionInstanceGroupManagerVersionTargetSize:
    def __init__(
        self,
        *,
        fixed: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed: The number of instances which are managed for this version. Conflicts with percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#fixed GoogleComputeRegionInstanceGroupManager#fixed}
        :param percent: The number of instances (calculated as percentage) which are managed for this version. Conflicts with fixed. Note that when using percent, rounding will be in favor of explicitly set target_size values; a managed instance group with 2 instances and 2 versions, one of which has a target_size.percent of 60 will create 2 instances of that version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#percent GoogleComputeRegionInstanceGroupManager#percent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a65ec63d7e5aaed98c4411a8819c829a89e709f8d351c7424781bc505efcbb2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#fixed GoogleComputeRegionInstanceGroupManager#fixed}
        '''
        result = self._values.get("fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percent(self) -> typing.Optional[jsii.Number]:
        '''The number of instances (calculated as percentage) which are managed for this version.

        Conflicts with fixed. Note that when using percent, rounding will be in favor of explicitly set target_size values; a managed instance group with 2 instances and 2 versions, one of which has a target_size.percent of 60 will create 2 instances of that version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_instance_group_manager#percent GoogleComputeRegionInstanceGroupManager#percent}
        '''
        result = self._values.get("percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionInstanceGroupManagerVersionTargetSize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionInstanceGroupManagerVersionTargetSizeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionInstanceGroupManager.GoogleComputeRegionInstanceGroupManagerVersionTargetSizeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb1e4bb651acb8f04dec1d3d5b91aeb8ed6c4ade7190e0a9edd9dc6f52c5c173)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67edb94f1608bac4355cc99a0ab65322178854cb0b138aa9945f810d1aed3ff1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5991662a53e07833edfb4e71de9a4d4fa7b8dc9d96ab280a8db27d127617a516)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionInstanceGroupManagerVersionTargetSize]:
        return typing.cast(typing.Optional[GoogleComputeRegionInstanceGroupManagerVersionTargetSize], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionInstanceGroupManagerVersionTargetSize],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0fc59a1178cd9d6f374114fe0a1bbcd6bfbb32c8eeff87dad033fccad7dc009)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleComputeRegionInstanceGroupManager",
    "GoogleComputeRegionInstanceGroupManagerAllInstancesConfig",
    "GoogleComputeRegionInstanceGroupManagerAllInstancesConfigOutputReference",
    "GoogleComputeRegionInstanceGroupManagerAutoHealingPolicies",
    "GoogleComputeRegionInstanceGroupManagerAutoHealingPoliciesOutputReference",
    "GoogleComputeRegionInstanceGroupManagerConfig",
    "GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy",
    "GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections",
    "GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelectionsList",
    "GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelectionsOutputReference",
    "GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyOutputReference",
    "GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicy",
    "GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicyOutputReference",
    "GoogleComputeRegionInstanceGroupManagerNamedPort",
    "GoogleComputeRegionInstanceGroupManagerNamedPortList",
    "GoogleComputeRegionInstanceGroupManagerNamedPortOutputReference",
    "GoogleComputeRegionInstanceGroupManagerParams",
    "GoogleComputeRegionInstanceGroupManagerParamsOutputReference",
    "GoogleComputeRegionInstanceGroupManagerStandbyPolicy",
    "GoogleComputeRegionInstanceGroupManagerStandbyPolicyOutputReference",
    "GoogleComputeRegionInstanceGroupManagerStatefulDisk",
    "GoogleComputeRegionInstanceGroupManagerStatefulDiskList",
    "GoogleComputeRegionInstanceGroupManagerStatefulDiskOutputReference",
    "GoogleComputeRegionInstanceGroupManagerStatefulExternalIp",
    "GoogleComputeRegionInstanceGroupManagerStatefulExternalIpList",
    "GoogleComputeRegionInstanceGroupManagerStatefulExternalIpOutputReference",
    "GoogleComputeRegionInstanceGroupManagerStatefulInternalIp",
    "GoogleComputeRegionInstanceGroupManagerStatefulInternalIpList",
    "GoogleComputeRegionInstanceGroupManagerStatefulInternalIpOutputReference",
    "GoogleComputeRegionInstanceGroupManagerStatus",
    "GoogleComputeRegionInstanceGroupManagerStatusAllInstancesConfig",
    "GoogleComputeRegionInstanceGroupManagerStatusAllInstancesConfigList",
    "GoogleComputeRegionInstanceGroupManagerStatusAllInstancesConfigOutputReference",
    "GoogleComputeRegionInstanceGroupManagerStatusList",
    "GoogleComputeRegionInstanceGroupManagerStatusOutputReference",
    "GoogleComputeRegionInstanceGroupManagerStatusStateful",
    "GoogleComputeRegionInstanceGroupManagerStatusStatefulList",
    "GoogleComputeRegionInstanceGroupManagerStatusStatefulOutputReference",
    "GoogleComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigs",
    "GoogleComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigsList",
    "GoogleComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigsOutputReference",
    "GoogleComputeRegionInstanceGroupManagerStatusVersionTarget",
    "GoogleComputeRegionInstanceGroupManagerStatusVersionTargetList",
    "GoogleComputeRegionInstanceGroupManagerStatusVersionTargetOutputReference",
    "GoogleComputeRegionInstanceGroupManagerTimeouts",
    "GoogleComputeRegionInstanceGroupManagerTimeoutsOutputReference",
    "GoogleComputeRegionInstanceGroupManagerUpdatePolicy",
    "GoogleComputeRegionInstanceGroupManagerUpdatePolicyOutputReference",
    "GoogleComputeRegionInstanceGroupManagerVersion",
    "GoogleComputeRegionInstanceGroupManagerVersionList",
    "GoogleComputeRegionInstanceGroupManagerVersionOutputReference",
    "GoogleComputeRegionInstanceGroupManagerVersionTargetSize",
    "GoogleComputeRegionInstanceGroupManagerVersionTargetSizeOutputReference",
]

publication.publish()

def _typecheckingstub__a0a223827e98daecc5f832261e4c56ad88a912b110c7eb8606c17c1b08cfb33f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    base_instance_name: builtins.str,
    name: builtins.str,
    version: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionInstanceGroupManagerVersion, typing.Dict[builtins.str, typing.Any]]]],
    all_instances_config: typing.Optional[typing.Union[GoogleComputeRegionInstanceGroupManagerAllInstancesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_healing_policies: typing.Optional[typing.Union[GoogleComputeRegionInstanceGroupManagerAutoHealingPolicies, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    distribution_policy_target_shape: typing.Optional[builtins.str] = None,
    distribution_policy_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_flexibility_policy: typing.Optional[typing.Union[GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_lifecycle_policy: typing.Optional[typing.Union[GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    list_managed_instances_results: typing.Optional[builtins.str] = None,
    named_port: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionInstanceGroupManagerNamedPort, typing.Dict[builtins.str, typing.Any]]]]] = None,
    params: typing.Optional[typing.Union[GoogleComputeRegionInstanceGroupManagerParams, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    standby_policy: typing.Optional[typing.Union[GoogleComputeRegionInstanceGroupManagerStandbyPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    stateful_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionInstanceGroupManagerStatefulDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stateful_external_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionInstanceGroupManagerStatefulExternalIp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stateful_internal_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionInstanceGroupManagerStatefulInternalIp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_size: typing.Optional[jsii.Number] = None,
    target_stopped_size: typing.Optional[jsii.Number] = None,
    target_suspended_size: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeRegionInstanceGroupManagerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    update_policy: typing.Optional[typing.Union[GoogleComputeRegionInstanceGroupManagerUpdatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6b221e27e8ad71fb75945773c39873bf096eb8bd74903efa04f6f93c787717e2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0064ae99021551bf68767d026acde8da9fb8eeaf197f36c17d6023fd67339b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionInstanceGroupManagerNamedPort, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74137bd1f00d07b8b1fde0c2c228c2b4e4e39a238ee6712c4cd41d1fc65313fa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionInstanceGroupManagerStatefulDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7dea1a4653583095bb48a9fbcb01c4869653becb6c634ad565edae64832a23(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionInstanceGroupManagerStatefulExternalIp, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441356b7e1690efb818dd9a93801c5e3560a054f77b28433b50bd0def9118bdb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionInstanceGroupManagerStatefulInternalIp, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c7dc7b85596f0c869965914da72af0bbb4bb3c406c22fbdcce55fa6e18c3d0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionInstanceGroupManagerVersion, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfeae3de56ea3f8a69d1872a30b44a34fe4ae401770e1067dee64d3a5adecdc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__483c8f25feed468c2a82c954d0f16e427f0e4a5b0a0e2ad2a171096e475a4a7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c16f9445792196597ce6ec647147d6fe9d344e736a9e37cb262c584e89680ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c3228de417f2063b76e2250ad6a96b8427af6d4a33901f0be7446d4842ff081(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__265c325303a7ffa19212e472c11bbed846588850e85fd1332a9059ce38efbdac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84d0739c6e6ca1f0a3540ecdb59c046ad080b3172708c7c7d0cb72d452b59a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e656f0f17eebd91fabe16c9814a28486ae9956b94fd89c9ebb0f6236aac8fe22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b73a8b0adefe00a2ea802c7704f70f2954f7f1424be94f5c55cc2c05476c648b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86497fea093d199780bcf4d7da28a474c9ab56b25a834b527e435b65cf0fc7ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f916b4c1d05c5fcf1e374a195c6fbb277173ebc3ffec5945a982ac4f041f2c6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856a4cd9b29b06e2ddb6971a4ba492b2e8dcc3655e20a9d02cf2fff6f13980fa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de1e169c81ef66ca3e6db169ca1694a3cc90855b0b0ffb4adf6e90215eb06dc7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd76ccfcd8766ac123ae15c53c459c9e3dfaa5720a25fa65b60ca26be647ff5f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e656948261dba83c3932bacb02cef5919edb78bd37885b82ba3c2fa0dbb1d3fa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e5aabaefc1c14562f2fadb6d9fbae6c0998464e94006f2cb0576ab4bb8f926(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b633494e8293ba9ff1272685860cd1d54568481a4baef09b8dcccd34cf51d8eb(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd6ad763533f35180b7eda7a67e18391bf52d371f5263bb778a8d3e571f7018(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae6358560528dbb3e389e4ff63f318e92844fd4d9bc27c4bb9ae2a4ee03e0da(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc2ab515c509cde6c076fc398728a1ff9b97d43226f5576468e9989df6a5dbef(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0a80d828c506422638f5909c81c0f4c4b696cca3f25b89d63e8cbec66bfa47d(
    value: typing.Optional[GoogleComputeRegionInstanceGroupManagerAllInstancesConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__111631cf12b14dee3ade6dcb8dbce6643ccdfb479542b6a1c30529756f98bedf(
    *,
    health_check: builtins.str,
    initial_delay_sec: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a0343f5466df1f9001d109b246679bf09791a05a32d9c2045fedf4daabd12f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b049cec12db9cee559f84717e6fcfec45c4d406d5e7b358bf7a798f43e79057(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b25dfe1ae83c31730f1ad89e977a1b16b413538b7ca614cbbbe41edf511c5cf0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f360f527b8995324806443455754432a1b801b8a5a7c5d4b98ebe7f514ddb53(
    value: typing.Optional[GoogleComputeRegionInstanceGroupManagerAutoHealingPolicies],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cdab6c9a39ac9bc9a3723775576b3eceb14fc6c65f74847ffb37585e4e2b911(
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
    version: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionInstanceGroupManagerVersion, typing.Dict[builtins.str, typing.Any]]]],
    all_instances_config: typing.Optional[typing.Union[GoogleComputeRegionInstanceGroupManagerAllInstancesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_healing_policies: typing.Optional[typing.Union[GoogleComputeRegionInstanceGroupManagerAutoHealingPolicies, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    distribution_policy_target_shape: typing.Optional[builtins.str] = None,
    distribution_policy_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_flexibility_policy: typing.Optional[typing.Union[GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_lifecycle_policy: typing.Optional[typing.Union[GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    list_managed_instances_results: typing.Optional[builtins.str] = None,
    named_port: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionInstanceGroupManagerNamedPort, typing.Dict[builtins.str, typing.Any]]]]] = None,
    params: typing.Optional[typing.Union[GoogleComputeRegionInstanceGroupManagerParams, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    standby_policy: typing.Optional[typing.Union[GoogleComputeRegionInstanceGroupManagerStandbyPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    stateful_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionInstanceGroupManagerStatefulDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stateful_external_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionInstanceGroupManagerStatefulExternalIp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stateful_internal_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionInstanceGroupManagerStatefulInternalIp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_size: typing.Optional[jsii.Number] = None,
    target_stopped_size: typing.Optional[jsii.Number] = None,
    target_suspended_size: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeRegionInstanceGroupManagerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    update_policy: typing.Optional[typing.Union[GoogleComputeRegionInstanceGroupManagerUpdatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    wait_for_instances: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    wait_for_instances_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd1115646e4fba59250ceda1131835619526f00dfbc6842c6dc0d834b826336(
    *,
    instance_selections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0639a8a71f063bc254aaaee91a7a035a63ca9f807434063bd52d1426eeaaba5b(
    *,
    machine_types: typing.Sequence[builtins.str],
    name: builtins.str,
    rank: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797184d6cfd6bada17d335c96888cf26149e9a57dd405585e7970b8e7f0cc232(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__925c77503369e1f1062739d398192eda0dbd6486a41e526f60af724a1419a64d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c53ed9e10d3b40302d055f32ba73703739b07e407184543b320bc3c25f3c890a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e60726ae6e664094b8bcacdb173b1b3492a74474a36bc62533e944067a2264(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b6d2728029cfcc5a1d67ba03f18da1a51686c10a6c09b95427185a5f0671a1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54cc52e3e45e4cc3cf8aa0b9c8b2baed73a3d4c7248eb397d79c7fbf3bd02787(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e70a99585499c2db94ac88492e900ede22db37b95f25c1bcbab43e2637914a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c12c0d72c98242ac229f7ad3524f3c5e532e4d6ebcb4eba4f68f5c832f0ce6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c6bf20c6a6748f377e996a554fc898fbf618754a34b38d516387cf990f6b19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03970d3c11c22a4f86747156b2dae807ce1da3d0d8360d1e440bdc85a986aa99(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__495a1add70f2c5f5c8824c5d89da1a3537b0006bed7334e81800b8e26e8d1758(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c08b886c16ad7f93812554a0d40f9fbdcfda1db282be62f51837707150a02430(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8288ae5d3c98396e0a2e0b83855a2330ffb42b85d6834cc24e4a79c8c148cebe(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicyInstanceSelections, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b9c2932772407598a7ba947df045405f9b05383f13eed22f8490b8f23dabfb(
    value: typing.Optional[GoogleComputeRegionInstanceGroupManagerInstanceFlexibilityPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a43d6ce2ad057dfe867bca3256de83a937089e55518f71fc01141b9a05ceb2d8(
    *,
    default_action_on_failure: typing.Optional[builtins.str] = None,
    force_update_on_repair: typing.Optional[builtins.str] = None,
    on_failed_health_check: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc84089bc785d17a0e158bf3070008cae89d833536b2768948ddcab97ecfc474(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c24bc404f230f2b5d59fb2575db71459704f04d2a99f84af1738bab5e58d47b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__094190abfe9aa1e10104a2be69f8accfa4565f31a4d604dc3611e3c106f82598(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4cd294a06e0a584ee0ed9d8c7582e9ee70255d5df2e0d6b5b139a6e1a2a4df2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__790af31565466be8b9755e6fbe1d73c56d7da839a0b9ba17cf7d6d164d2fa8a6(
    value: typing.Optional[GoogleComputeRegionInstanceGroupManagerInstanceLifecyclePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db259ee0ef1c4852842f216d26d7c79a5a19304e73dff134892c92c22bb3d1d(
    *,
    name: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efadfe113c8f35e1dd6aa520d206d47ede32fcf26028da590bdc2d025c7a7b80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6b60f6b70b2ed20b39a89f7a3e55f13d5fcc5d7cd740f44be3c78a64574c0c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24be34e9a899dc12487f272dc7bfe5983565b2960a7383c6ff978b7733302350(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cdef440384f54d75d61c7d47e8d339612244c08be07ff85074bacb60800b46f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc5d1e77a0e2ee5c5c5eb17ac671b574ea98ff6ed84814909c3c1ea156f9df52(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a08d0817cd8d5024fafb0c7dc459311d840741ab3bde397787f7e76c8ae4c63(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerNamedPort]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a707fdc6ee3bae690fa43a8aa85d6d4cacf1383617e4d874e0b56c3cb83343a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a05c6eeaaa78940cf19fb36cc47e0e4cb7cb8c0653ed6f70f7958498a82030ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89bec44214e02e00ab7ac494b604f57aaf5459b4cb6e8a1eb0ef9f92dfd022db(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd9358d9d57837ba08c5d8aee276a231689ade73771005755d095b357e278d36(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerNamedPort]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d9fe85262072db14d7b2fbff591d2bac26c673ef222a707bbbf3f152b4c4d3(
    *,
    resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b18e33c698f8c32b685000e37c316ad6a7b7f5b4161efe923cad4e0263de3a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a11e07a61f3ac431ea9f5e34275434c5d01e71991c4445a6bcc47edc46f740c9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb049514f0eb7f35ddd7f9b4756017b89eb14959bb7c1aee758afa23b5eac97e(
    value: typing.Optional[GoogleComputeRegionInstanceGroupManagerParams],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc3776f1c81886d5fa40376c928f69a0add48e3f5855ab14d1d7d0cc74aba4c(
    *,
    initial_delay_sec: typing.Optional[jsii.Number] = None,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc5bd28404cf19c1ee5f70ba8e971bf0f1c5ecbae85f5dc3dd2982eab64207d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186710b4fcd16a16abc939ced58d9a026cdddc9a35b4a5909c7b86f1a844e336(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e3fa1b45e0962c4243b1f33ac8d354e724ff7ca6b2acd72937a323f21144111(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eddccd7a8e4533a332ca13d320d22133502d88978e3282779e1aa717f91101e(
    value: typing.Optional[GoogleComputeRegionInstanceGroupManagerStandbyPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b5e268b6689fd64f89e09cc39570132efac2e85972aaf98791c89d915acb63(
    *,
    device_name: builtins.str,
    delete_rule: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36bebae3a448537310ffd1e560a00728f7935715a7629018b51c6c9656db4534(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b17e22e6d041865b2308dcd920676ce5abe6d221825daa2bb6f6cf9766a544a5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__005b7584423a8b9f298eefaaa80a15e882ff74422df689fb3a992ab6ba822ada(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03ea565ff87fe6ee07643ecfb8af3a9295d8934b2c121c455598a48838a8a85(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__555aacc16e4b60aadcfe0dc4acb3bed2eab688df75a4c36166b2c998046012f4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd7055e0234073164f30c72278729650ffaeabbe50e1d38ef36acace9c8991e7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerStatefulDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__301c0da0084fa7b3d8c36f39e516a75999bd9e00893f15791b2f4c58ec7c945e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2159d1896f13b2812e3855488049990058affcbfdaddf961cb9d5a5266a730(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5197120aeaeedab71c3829b483f8763727269fd56b86863cff90df8e41affa6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1035616c54257a4dbaed986f9f95a9ea1ce646afe015d7e1e17f9098b2f3583(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerStatefulDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7181185e3d8c51d72e1605a968ab07ab8aea083640364386c0f4b2c8e6b99a92(
    *,
    delete_rule: typing.Optional[builtins.str] = None,
    interface_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81141909af5911d433d4cc938691338da6452229aa6c043d9e64349f15271d00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__877e10d652ed19fc538631fdd6a72e6e58b23b1f0c26f16020169aae6823e822(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__629b41c1440c0d164618a5921f1d37cdc2ef9adbe760dddb0e2f5c00a904da0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e76d1647e02f0754c76845604ce19f32e3e5f3a55095f5dcedd96114096e668(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc295eebf7208f412ca72bc22e6af54c96285f04d4ffed05dff87f4ae1d01c2f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba827cfd0cd7aa52e78ce27d20e1af283e2ec25eb04a97548385cead1f8a5fc4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerStatefulExternalIp]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5018c70ccd0bbcc27c1383304e5b8142c9fa83523ccfe4af0cb76de63b95fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10afb2aa0aa08d4207cf8e3a459a8974b4d3d76316856195a199c4b299c628bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13774139df593877fb91af153ee510908a15cc6761e0bbd9d45b5990d65b461(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac6473562eb3a92779369f72fc09e062d6fc01ca10c42f14941d79859209456(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerStatefulExternalIp]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab25919d2ef08b78df2988d49d85ce71ff7f0bab4be959183b03ccb338de0511(
    *,
    delete_rule: typing.Optional[builtins.str] = None,
    interface_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d6aee2e2f25d72887dbd4be12b7f3780260d35bcc45a880b182eadadddd368(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__823ad6a05453422863def9cc2858787430b402a65759e34bad6536813c4b8a07(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96fea8315bfb4dc57fb6cb2b83eaff00ee911e34f091236e1c883728caa0df12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc80f129392c4bc1813ffddf253fd2cf2168055ffa4b3e89ebd7f953b415523(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73aac20c436b8fdffe2c3d97428f9b6fe58ae02998a0fecec07b0f6cbec2910(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e71b3c650c7992752a7df3ace53443fc16de804f8df9a4bd59c8ce166d50464d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerStatefulInternalIp]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8586b626a676054d75df50499d1fc81e5f3520af30884071e4a20fe72df12ed7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49f53f0c8d779bdfd52f44533b544ade9f6fe1dcb665bc3675e2426a5cc13ace(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f26f9443c96cc0511883b334a59ee14ee950f1e95724daff670e35a1592fbfda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__684337e69ae7598a92993df2a1d8b0b91119d61e8c9d6ae471afebaabfbec362(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerStatefulInternalIp]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be0eebd70a1c55fca0d838307b605e4a6fa70e832d6ce7cb39da28f46136443(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44f2c3daea7d5b2c6c6be0047fa40b2c16fac10c81e6483c2617a747346a009b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292b3961ab6f43ead9527894cf0ef969fd13e0bf9b1661b490a7c73b809c6514(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae0cf9de966e103fa7d90b46b9c277898c38767517c8d26b0bc283b96bb85fc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d92c51bafe4cd16b59c6af6d66569767a01cbd76cf1bca29c6256dc4242249(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abdb196bf1248ba31b48ebde1dc46a79e125a55759ec87fa1c4cbd9a6f033bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa3ac59513ffb6c265046144eda1df47185c39a2cb4bd77a630aa7f592a53483(
    value: typing.Optional[GoogleComputeRegionInstanceGroupManagerStatusAllInstancesConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64192be145fe93649515a753a47ca4d5ba7b633bc1dccd51c6bffb1af37cbc97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572d4c1248e6fe54782bc66a9bf96b79087f70491b9798e31bb06a8f8ed47305(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98a7e38a6314fe325211b6266a026a65c8fe204f68af2c4fa4f2c83514f8bd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e108276611d269f1ac52b0cc08cd178dbd880d30b7cee09862a87fee6c7307fd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__203eb609d4baa309a38532f0b03103a82f7d1f94bbaf30d70f7512c49f9e82e3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e966324b482924b3670f0432350d1f6e80f6218c1cb846e31af78ff144351126(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5acc2a83e511461b73389904d39354177427b9be658c08fb4d04ec1e0fdb2623(
    value: typing.Optional[GoogleComputeRegionInstanceGroupManagerStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a42faf4c7494f5c911a19c3dedec6f7dbf54282427f2155a9afa0bf963052bcc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ad690a2830eb1f9ea165d273d46319889f366fb263ff458d33d474f4c74985(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e66b03d762b6b60b9ea072ff4149d6a8fca115e55941a2e2977148b2dbb34fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f840a1dd6179f29d3d4f7cc6ebceaa5ac3ecf1255af6ea9802b4d8d0ad2397(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe520b433dbe561d49d4678b8e44b13ab40d9356542588360b19e13ca32ba451(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30985a4e26dffd427eb0bd829d0ff6846290affc6db6c23803b10b9902543ef1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a84b04541a9405a73a32d3c53d2980a68e8a2a9da3d8bfb0b6bf5e49e0c6c49a(
    value: typing.Optional[GoogleComputeRegionInstanceGroupManagerStatusStateful],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__577aceac9dc36d3b9345ea5e97a33f1fdc18b54d4f1e39b068c023251429d770(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26bbbd79a4e687cc0cd7903fc9bcfaec0dc584bec98a0ee178705f5a35a18d79(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eb76b3c5233597f41b6938e667742e77b016d21d6d9aa72be7b64724d053400(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c45f3cee64ffce60668c49f194ae5a245b126751984aff60c4a294fbbbaa9d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf81cf1130760b6c4b8b539f4221ecef40c8ac1310a96bca5204e2b3afb90f3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3efac696aff0186c2b81fca509b6172ea5c23237e8c3b81fdc70e61b68840edc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0b700ff6b5ae140ff1983dc68d91856bd2be81e40c208b7ec5363217887364e(
    value: typing.Optional[GoogleComputeRegionInstanceGroupManagerStatusStatefulPerInstanceConfigs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df81cae8416827b56e0b1ad9963e70b0d0c0925a31f530980add11b673a09a59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__420e779cc3132d71872b1920d8fa1d9462ee9ee3987ddcd6a317529fcf0c27c6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d93291a947ef4db9ff7b0e58d4078cb3c9d93ab0dace176d254a1a4be8c638a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ba95d0ff250520d57503601633c5e27cbbe442f9fc98ae0f7751a5f1f9ea12(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e634e474df7c0b27a61e2c5d293efe0ffd81b5ef81bc4b529e9e0a2d5f3c769c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb8ae3693013169b6cebc31077c0a4080e5568ed6f2a55ed282f27c91e660b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66fde5ed050f523c07b59631f1b86e5db05808961eea5b7b07c221bb3bcaccbe(
    value: typing.Optional[GoogleComputeRegionInstanceGroupManagerStatusVersionTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1327daf235603cabde348de3765128d081ac0b4d8f54e6b0e921238cdd205336(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba425b10b02b14736c5b6d2aae9a25fad0753876029725d9c88a37f5af8dc216(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cbb91d7eb994fcc644beb6783570f81ab6a8ceba2b37dff326a8ef2b0844cdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb95e571cba7f5310146f4e4ca43638e347a8d58f484f365a54ec57f3bc8d75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adbfcd6a317faac1311671541ee4b086c0cdc8356344798fbba41986ed03e88e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb82b915fddc37b0fa32cb998ff70026ea763bcd51ebd6c1e96d7645dfc32d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faebc8ce6ce799806dace26d82cf41c12ab4602b766b5b6fa1a1c99714b0a51c(
    *,
    minimal_action: builtins.str,
    type: builtins.str,
    instance_redistribution_type: typing.Optional[builtins.str] = None,
    max_surge_fixed: typing.Optional[jsii.Number] = None,
    max_surge_percent: typing.Optional[jsii.Number] = None,
    max_unavailable_fixed: typing.Optional[jsii.Number] = None,
    max_unavailable_percent: typing.Optional[jsii.Number] = None,
    min_ready_sec: typing.Optional[jsii.Number] = None,
    most_disruptive_allowed_action: typing.Optional[builtins.str] = None,
    replacement_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fa41ee27d7a36457b5a00c14cb313e1c69b32286e317071971b867bea581515(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed28a2eb428494916554d60a52526ebd0fd78a51fae67d42afeffa65d19bf9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f423db798c64283a0350f725ac75123e29681db70772e70fe21809e5ed1049(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df086bd4b0128e13faa036e8577419ce4f72b4abb3913c66ef866c72d9bea84c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014fbc8ca231c46323a9a0cb418dcce64ed25081e9c8a1fcfd8f6cd521eee7bd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__945bd80a7c002549feeb140276f3d9b9aceb409bfb3ed416356b19b8b7604535(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6946b0bdc5667231234771554f416cc06d3a84015562f190dd8f672daa95e96a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4026bd1ce887929174deefc27854e3ed58fac8c2ce78b2510254de3b828f9552(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9097fe5fc978278fc19304acecae87634301282a90611c573c1ade0f8ae49a36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2b889d252ce551fb9d315e5b5dff18098ade97e424ca0ee7b4b9623b057772d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0357088efb8395fb97e8296555e69bf739ed9c57e8f0d0877b12ba1ea725fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82e2476e1e17715c9217349d346ed9a3e8279ced348dbfbf813ed18a085f1207(
    value: typing.Optional[GoogleComputeRegionInstanceGroupManagerUpdatePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d350450103c28769cf774cb9c00dd5c5a234db4a5ddb6a0b2d99871b645efa(
    *,
    instance_template: builtins.str,
    name: typing.Optional[builtins.str] = None,
    target_size: typing.Optional[typing.Union[GoogleComputeRegionInstanceGroupManagerVersionTargetSize, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e02bce5a8ba6958dde33198bda0631c397ae8d07fc495966d99eb6aa45c960(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e03f6a49f2ffc3717de76e9d63dda91edba43b46642933e1e573a2ec79ab74(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbe21585240b3676fcce62ec3ef24fe850c731376c5c4e081e06f5165cf7857c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34601ccc4be0f686f149f50af71e60687d5f2116e5278e0c67c57f2f116e0847(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35d5b3780b9c6c757493c93dff54931c8cbc1badb8f8b09817933985dabf8474(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510af7fc22b1b61827d2c464e40de61ef069ba5bc251d5f6eca7e250491d308f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionInstanceGroupManagerVersion]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ac234f60ca972b22d7334e11d0ee97cb8e8534693aa7b1257f869f67626baae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58053a01d98e5fcbc03243f235bda74599405f9357ac616ae42db796b179f95f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0914f96853b308d94befb91e0f842946038ee39c565f94b630bf6a5ac1db32ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c694b06f20b390ce9b63052bbfcc2d40160a3e8a1cba3f33c9c12c1a0d7a419e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionInstanceGroupManagerVersion]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a65ec63d7e5aaed98c4411a8819c829a89e709f8d351c7424781bc505efcbb2(
    *,
    fixed: typing.Optional[jsii.Number] = None,
    percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb1e4bb651acb8f04dec1d3d5b91aeb8ed6c4ade7190e0a9edd9dc6f52c5c173(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67edb94f1608bac4355cc99a0ab65322178854cb0b138aa9945f810d1aed3ff1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5991662a53e07833edfb4e71de9a4d4fa7b8dc9d96ab280a8db27d127617a516(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0fc59a1178cd9d6f374114fe0a1bbcd6bfbb32c8eeff87dad033fccad7dc009(
    value: typing.Optional[GoogleComputeRegionInstanceGroupManagerVersionTargetSize],
) -> None:
    """Type checking stubs"""
    pass
