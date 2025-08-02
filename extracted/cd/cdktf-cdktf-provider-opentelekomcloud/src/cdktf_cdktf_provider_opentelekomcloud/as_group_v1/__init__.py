r'''
# `opentelekomcloud_as_group_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_as_group_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1).
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


class AsGroupV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1 opentelekomcloud_as_group_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        delete_instances: builtins.str,
        delete_publicip: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        networks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AsGroupV1Networks", typing.Dict[builtins.str, typing.Any]]]],
        scaling_group_name: builtins.str,
        vpc_id: builtins.str,
        available_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cool_down_time: typing.Optional[jsii.Number] = None,
        desire_instance_number: typing.Optional[jsii.Number] = None,
        health_periodic_audit_grace_period: typing.Optional[jsii.Number] = None,
        health_periodic_audit_method: typing.Optional[builtins.str] = None,
        health_periodic_audit_time: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        instance_terminate_policy: typing.Optional[builtins.str] = None,
        lbaas_listeners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AsGroupV1LbaasListeners", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lb_listener_id: typing.Optional[builtins.str] = None,
        max_instance_number: typing.Optional[jsii.Number] = None,
        min_instance_number: typing.Optional[jsii.Number] = None,
        notifications: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        scaling_configuration_id: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Union["AsGroupV1SecurityGroups", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["AsGroupV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1 opentelekomcloud_as_group_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param delete_instances: Whether to delete instances when they are removed from the AS group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#delete_instances AsGroupV1#delete_instances}
        :param delete_publicip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#delete_publicip AsGroupV1#delete_publicip}.
        :param networks: networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#networks AsGroupV1#networks}
        :param scaling_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#scaling_group_name AsGroupV1#scaling_group_name}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#vpc_id AsGroupV1#vpc_id}.
        :param available_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#available_zones AsGroupV1#available_zones}.
        :param cool_down_time: The cooling duration, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#cool_down_time AsGroupV1#cool_down_time}
        :param desire_instance_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#desire_instance_number AsGroupV1#desire_instance_number}.
        :param health_periodic_audit_grace_period: The grace period for instance health check, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#health_periodic_audit_grace_period AsGroupV1#health_periodic_audit_grace_period}
        :param health_periodic_audit_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#health_periodic_audit_method AsGroupV1#health_periodic_audit_method}.
        :param health_periodic_audit_time: The health check period for instances, in minutes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#health_periodic_audit_time AsGroupV1#health_periodic_audit_time}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#id AsGroupV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_terminate_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#instance_terminate_policy AsGroupV1#instance_terminate_policy}.
        :param lbaas_listeners: lbaas_listeners block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#lbaas_listeners AsGroupV1#lbaas_listeners}
        :param lb_listener_id: The system supports the binding of up to six classic LB listeners, the IDs of which are separated using a comma. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#lb_listener_id AsGroupV1#lb_listener_id}
        :param max_instance_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#max_instance_number AsGroupV1#max_instance_number}.
        :param min_instance_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#min_instance_number AsGroupV1#min_instance_number}.
        :param notifications: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#notifications AsGroupV1#notifications}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#region AsGroupV1#region}.
        :param scaling_configuration_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#scaling_configuration_id AsGroupV1#scaling_configuration_id}.
        :param security_groups: security_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#security_groups AsGroupV1#security_groups}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#tags AsGroupV1#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#timeouts AsGroupV1#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc0bada361aa92f8e15e7730f6e9b17dd049c55944e3f61a771050b056e81ede)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AsGroupV1Config(
            delete_instances=delete_instances,
            delete_publicip=delete_publicip,
            networks=networks,
            scaling_group_name=scaling_group_name,
            vpc_id=vpc_id,
            available_zones=available_zones,
            cool_down_time=cool_down_time,
            desire_instance_number=desire_instance_number,
            health_periodic_audit_grace_period=health_periodic_audit_grace_period,
            health_periodic_audit_method=health_periodic_audit_method,
            health_periodic_audit_time=health_periodic_audit_time,
            id=id,
            instance_terminate_policy=instance_terminate_policy,
            lbaas_listeners=lbaas_listeners,
            lb_listener_id=lb_listener_id,
            max_instance_number=max_instance_number,
            min_instance_number=min_instance_number,
            notifications=notifications,
            region=region,
            scaling_configuration_id=scaling_configuration_id,
            security_groups=security_groups,
            tags=tags,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a AsGroupV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AsGroupV1 to import.
        :param import_from_id: The id of the existing AsGroupV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AsGroupV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d9892a5d0dfbeaaaf37454c8758324f72dff960b9030f24d1ae064a942436ed)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLbaasListeners")
    def put_lbaas_listeners(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AsGroupV1LbaasListeners", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adcc56aae21ca0859261bf81f7633c345553296d050db36e78514ef20965b0a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLbaasListeners", [value]))

    @jsii.member(jsii_name="putNetworks")
    def put_networks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AsGroupV1Networks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67672dae4c041830b69b1bb5c9fc11df5f6d5c65ed4796babb3b0190a4c56fca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworks", [value]))

    @jsii.member(jsii_name="putSecurityGroups")
    def put_security_groups(self, *, id: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#id AsGroupV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        value = AsGroupV1SecurityGroups(id=id)

        return typing.cast(None, jsii.invoke(self, "putSecurityGroups", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#create AsGroupV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#delete AsGroupV1#delete}.
        '''
        value = AsGroupV1Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAvailableZones")
    def reset_available_zones(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailableZones", []))

    @jsii.member(jsii_name="resetCoolDownTime")
    def reset_cool_down_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoolDownTime", []))

    @jsii.member(jsii_name="resetDesireInstanceNumber")
    def reset_desire_instance_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDesireInstanceNumber", []))

    @jsii.member(jsii_name="resetHealthPeriodicAuditGracePeriod")
    def reset_health_periodic_audit_grace_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthPeriodicAuditGracePeriod", []))

    @jsii.member(jsii_name="resetHealthPeriodicAuditMethod")
    def reset_health_periodic_audit_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthPeriodicAuditMethod", []))

    @jsii.member(jsii_name="resetHealthPeriodicAuditTime")
    def reset_health_periodic_audit_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthPeriodicAuditTime", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstanceTerminatePolicy")
    def reset_instance_terminate_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceTerminatePolicy", []))

    @jsii.member(jsii_name="resetLbaasListeners")
    def reset_lbaas_listeners(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLbaasListeners", []))

    @jsii.member(jsii_name="resetLbListenerId")
    def reset_lb_listener_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLbListenerId", []))

    @jsii.member(jsii_name="resetMaxInstanceNumber")
    def reset_max_instance_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInstanceNumber", []))

    @jsii.member(jsii_name="resetMinInstanceNumber")
    def reset_min_instance_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinInstanceNumber", []))

    @jsii.member(jsii_name="resetNotifications")
    def reset_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifications", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetScalingConfigurationId")
    def reset_scaling_configuration_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScalingConfigurationId", []))

    @jsii.member(jsii_name="resetSecurityGroups")
    def reset_security_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroups", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="currentInstanceNumber")
    def current_instance_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "currentInstanceNumber"))

    @builtins.property
    @jsii.member(jsii_name="instances")
    def instances(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instances"))

    @builtins.property
    @jsii.member(jsii_name="lbaasListeners")
    def lbaas_listeners(self) -> "AsGroupV1LbaasListenersList":
        return typing.cast("AsGroupV1LbaasListenersList", jsii.get(self, "lbaasListeners"))

    @builtins.property
    @jsii.member(jsii_name="networks")
    def networks(self) -> "AsGroupV1NetworksList":
        return typing.cast("AsGroupV1NetworksList", jsii.get(self, "networks"))

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> "AsGroupV1SecurityGroupsOutputReference":
        return typing.cast("AsGroupV1SecurityGroupsOutputReference", jsii.get(self, "securityGroups"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "AsGroupV1TimeoutsOutputReference":
        return typing.cast("AsGroupV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="availableZonesInput")
    def available_zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "availableZonesInput"))

    @builtins.property
    @jsii.member(jsii_name="coolDownTimeInput")
    def cool_down_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coolDownTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInstancesInput")
    def delete_instances_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="deletePublicipInput")
    def delete_publicip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletePublicipInput"))

    @builtins.property
    @jsii.member(jsii_name="desireInstanceNumberInput")
    def desire_instance_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "desireInstanceNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="healthPeriodicAuditGracePeriodInput")
    def health_periodic_audit_grace_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "healthPeriodicAuditGracePeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="healthPeriodicAuditMethodInput")
    def health_periodic_audit_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthPeriodicAuditMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="healthPeriodicAuditTimeInput")
    def health_periodic_audit_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "healthPeriodicAuditTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTerminatePolicyInput")
    def instance_terminate_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTerminatePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="lbaasListenersInput")
    def lbaas_listeners_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsGroupV1LbaasListeners"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsGroupV1LbaasListeners"]]], jsii.get(self, "lbaasListenersInput"))

    @builtins.property
    @jsii.member(jsii_name="lbListenerIdInput")
    def lb_listener_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lbListenerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceNumberInput")
    def max_instance_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInstanceNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="minInstanceNumberInput")
    def min_instance_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInstanceNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="networksInput")
    def networks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsGroupV1Networks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsGroupV1Networks"]]], jsii.get(self, "networksInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationsInput")
    def notifications_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingConfigurationIdInput")
    def scaling_configuration_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingConfigurationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingGroupNameInput")
    def scaling_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsInput")
    def security_groups_input(self) -> typing.Optional["AsGroupV1SecurityGroups"]:
        return typing.cast(typing.Optional["AsGroupV1SecurityGroups"], jsii.get(self, "securityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AsGroupV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AsGroupV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="availableZones")
    def available_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availableZones"))

    @available_zones.setter
    def available_zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5075d760a7411ce78f0dcf0e051098541f970247f065ecbb755feaedd32bad3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availableZones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="coolDownTime")
    def cool_down_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "coolDownTime"))

    @cool_down_time.setter
    def cool_down_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f80cfbb3f08727898bc9eaee6bba0d13afc6290f210dbe3a16e0a161843b0f72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coolDownTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteInstances")
    def delete_instances(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteInstances"))

    @delete_instances.setter
    def delete_instances(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91beac19a661336dd22e847a3cdf4fd69e9215cb45443b624c8ded95ffb70dd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletePublicip")
    def delete_publicip(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deletePublicip"))

    @delete_publicip.setter
    def delete_publicip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95f4af8a97c0fc7b231e39a5e73babb03169343a1478f638b63115f49b585615)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletePublicip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="desireInstanceNumber")
    def desire_instance_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "desireInstanceNumber"))

    @desire_instance_number.setter
    def desire_instance_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd94e89af8882a510ccbadf2b9f2785e9bd8d2d8485cd0e3d8e5266e17bca38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desireInstanceNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthPeriodicAuditGracePeriod")
    def health_periodic_audit_grace_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "healthPeriodicAuditGracePeriod"))

    @health_periodic_audit_grace_period.setter
    def health_periodic_audit_grace_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c7849b460fba4e4ebba01e5a1121e174d016b87fa422bdda69d675d6ca9c475)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthPeriodicAuditGracePeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthPeriodicAuditMethod")
    def health_periodic_audit_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthPeriodicAuditMethod"))

    @health_periodic_audit_method.setter
    def health_periodic_audit_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9321e80ba646a33bd4c42bd074892b26c63f5b64d13d95e85d2774c818edf97a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthPeriodicAuditMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthPeriodicAuditTime")
    def health_periodic_audit_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "healthPeriodicAuditTime"))

    @health_periodic_audit_time.setter
    def health_periodic_audit_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5021228cb4f8205a1cb211e6356eb9dd576c3cf2f48556313d036ed164965a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthPeriodicAuditTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38122bd5aac8858c21284cdbe9c4d77d9461cec2dc88d958ad3ddd69e834b94d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceTerminatePolicy")
    def instance_terminate_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceTerminatePolicy"))

    @instance_terminate_policy.setter
    def instance_terminate_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33fdb0d2d0ff5de64e5b36f95bba6c759b7a9c5c006ea9e72f20701ed22629e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceTerminatePolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lbListenerId")
    def lb_listener_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lbListenerId"))

    @lb_listener_id.setter
    def lb_listener_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbf4358a1a97bd3343dec306a4dcbb56028ecacc7d49fc47c6f296ce626eb5ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lbListenerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxInstanceNumber")
    def max_instance_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstanceNumber"))

    @max_instance_number.setter
    def max_instance_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca55894ffbc04da2a7abf01e873265e45481de519c4a163434d1e4d7fc353f7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstanceNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minInstanceNumber")
    def min_instance_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstanceNumber"))

    @min_instance_number.setter
    def min_instance_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b327358d2279491470c173113af35ceac18bcfcaf6a2f1f296728da1279c3feb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstanceNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notifications")
    def notifications(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notifications"))

    @notifications.setter
    def notifications(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e01d81e4b2006c7358281cb0fe1c61d5f586c19642bdf9c1b9aeffdc6c4d15d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifications", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12c32a447ee5ba594b21d3ac05471fa5dfe432150f13f8e3558f9de03ea8bc0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scalingConfigurationId")
    def scaling_configuration_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingConfigurationId"))

    @scaling_configuration_id.setter
    def scaling_configuration_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d66aba9e5993c6f0e01ce2bf77c818a0a676132c1bf281022d6e46ea4d163ebb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingConfigurationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scalingGroupName")
    def scaling_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingGroupName"))

    @scaling_group_name.setter
    def scaling_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b3a9d9a65790aa6c77e64b7374d157d4f7fe12f2f5c3e81811e3ed4c43d8fd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6b2904bf918483601cc8bf8dcf2b806f183c3e98d674269438fdf3476b53f38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09157180a4aba88ba6fc743d9fddc753770ca068978b6cb643a5fb80a55d4317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "delete_instances": "deleteInstances",
        "delete_publicip": "deletePublicip",
        "networks": "networks",
        "scaling_group_name": "scalingGroupName",
        "vpc_id": "vpcId",
        "available_zones": "availableZones",
        "cool_down_time": "coolDownTime",
        "desire_instance_number": "desireInstanceNumber",
        "health_periodic_audit_grace_period": "healthPeriodicAuditGracePeriod",
        "health_periodic_audit_method": "healthPeriodicAuditMethod",
        "health_periodic_audit_time": "healthPeriodicAuditTime",
        "id": "id",
        "instance_terminate_policy": "instanceTerminatePolicy",
        "lbaas_listeners": "lbaasListeners",
        "lb_listener_id": "lbListenerId",
        "max_instance_number": "maxInstanceNumber",
        "min_instance_number": "minInstanceNumber",
        "notifications": "notifications",
        "region": "region",
        "scaling_configuration_id": "scalingConfigurationId",
        "security_groups": "securityGroups",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class AsGroupV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        delete_instances: builtins.str,
        delete_publicip: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        networks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AsGroupV1Networks", typing.Dict[builtins.str, typing.Any]]]],
        scaling_group_name: builtins.str,
        vpc_id: builtins.str,
        available_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cool_down_time: typing.Optional[jsii.Number] = None,
        desire_instance_number: typing.Optional[jsii.Number] = None,
        health_periodic_audit_grace_period: typing.Optional[jsii.Number] = None,
        health_periodic_audit_method: typing.Optional[builtins.str] = None,
        health_periodic_audit_time: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        instance_terminate_policy: typing.Optional[builtins.str] = None,
        lbaas_listeners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AsGroupV1LbaasListeners", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lb_listener_id: typing.Optional[builtins.str] = None,
        max_instance_number: typing.Optional[jsii.Number] = None,
        min_instance_number: typing.Optional[jsii.Number] = None,
        notifications: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        scaling_configuration_id: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Union["AsGroupV1SecurityGroups", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["AsGroupV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param delete_instances: Whether to delete instances when they are removed from the AS group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#delete_instances AsGroupV1#delete_instances}
        :param delete_publicip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#delete_publicip AsGroupV1#delete_publicip}.
        :param networks: networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#networks AsGroupV1#networks}
        :param scaling_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#scaling_group_name AsGroupV1#scaling_group_name}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#vpc_id AsGroupV1#vpc_id}.
        :param available_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#available_zones AsGroupV1#available_zones}.
        :param cool_down_time: The cooling duration, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#cool_down_time AsGroupV1#cool_down_time}
        :param desire_instance_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#desire_instance_number AsGroupV1#desire_instance_number}.
        :param health_periodic_audit_grace_period: The grace period for instance health check, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#health_periodic_audit_grace_period AsGroupV1#health_periodic_audit_grace_period}
        :param health_periodic_audit_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#health_periodic_audit_method AsGroupV1#health_periodic_audit_method}.
        :param health_periodic_audit_time: The health check period for instances, in minutes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#health_periodic_audit_time AsGroupV1#health_periodic_audit_time}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#id AsGroupV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_terminate_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#instance_terminate_policy AsGroupV1#instance_terminate_policy}.
        :param lbaas_listeners: lbaas_listeners block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#lbaas_listeners AsGroupV1#lbaas_listeners}
        :param lb_listener_id: The system supports the binding of up to six classic LB listeners, the IDs of which are separated using a comma. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#lb_listener_id AsGroupV1#lb_listener_id}
        :param max_instance_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#max_instance_number AsGroupV1#max_instance_number}.
        :param min_instance_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#min_instance_number AsGroupV1#min_instance_number}.
        :param notifications: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#notifications AsGroupV1#notifications}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#region AsGroupV1#region}.
        :param scaling_configuration_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#scaling_configuration_id AsGroupV1#scaling_configuration_id}.
        :param security_groups: security_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#security_groups AsGroupV1#security_groups}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#tags AsGroupV1#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#timeouts AsGroupV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(security_groups, dict):
            security_groups = AsGroupV1SecurityGroups(**security_groups)
        if isinstance(timeouts, dict):
            timeouts = AsGroupV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee75f1381020a62f0bc55040b8fc6d83c5a09cb1d9d21d1b12afcde2b38b991)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument delete_instances", value=delete_instances, expected_type=type_hints["delete_instances"])
            check_type(argname="argument delete_publicip", value=delete_publicip, expected_type=type_hints["delete_publicip"])
            check_type(argname="argument networks", value=networks, expected_type=type_hints["networks"])
            check_type(argname="argument scaling_group_name", value=scaling_group_name, expected_type=type_hints["scaling_group_name"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument available_zones", value=available_zones, expected_type=type_hints["available_zones"])
            check_type(argname="argument cool_down_time", value=cool_down_time, expected_type=type_hints["cool_down_time"])
            check_type(argname="argument desire_instance_number", value=desire_instance_number, expected_type=type_hints["desire_instance_number"])
            check_type(argname="argument health_periodic_audit_grace_period", value=health_periodic_audit_grace_period, expected_type=type_hints["health_periodic_audit_grace_period"])
            check_type(argname="argument health_periodic_audit_method", value=health_periodic_audit_method, expected_type=type_hints["health_periodic_audit_method"])
            check_type(argname="argument health_periodic_audit_time", value=health_periodic_audit_time, expected_type=type_hints["health_periodic_audit_time"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_terminate_policy", value=instance_terminate_policy, expected_type=type_hints["instance_terminate_policy"])
            check_type(argname="argument lbaas_listeners", value=lbaas_listeners, expected_type=type_hints["lbaas_listeners"])
            check_type(argname="argument lb_listener_id", value=lb_listener_id, expected_type=type_hints["lb_listener_id"])
            check_type(argname="argument max_instance_number", value=max_instance_number, expected_type=type_hints["max_instance_number"])
            check_type(argname="argument min_instance_number", value=min_instance_number, expected_type=type_hints["min_instance_number"])
            check_type(argname="argument notifications", value=notifications, expected_type=type_hints["notifications"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument scaling_configuration_id", value=scaling_configuration_id, expected_type=type_hints["scaling_configuration_id"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delete_instances": delete_instances,
            "delete_publicip": delete_publicip,
            "networks": networks,
            "scaling_group_name": scaling_group_name,
            "vpc_id": vpc_id,
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
        if available_zones is not None:
            self._values["available_zones"] = available_zones
        if cool_down_time is not None:
            self._values["cool_down_time"] = cool_down_time
        if desire_instance_number is not None:
            self._values["desire_instance_number"] = desire_instance_number
        if health_periodic_audit_grace_period is not None:
            self._values["health_periodic_audit_grace_period"] = health_periodic_audit_grace_period
        if health_periodic_audit_method is not None:
            self._values["health_periodic_audit_method"] = health_periodic_audit_method
        if health_periodic_audit_time is not None:
            self._values["health_periodic_audit_time"] = health_periodic_audit_time
        if id is not None:
            self._values["id"] = id
        if instance_terminate_policy is not None:
            self._values["instance_terminate_policy"] = instance_terminate_policy
        if lbaas_listeners is not None:
            self._values["lbaas_listeners"] = lbaas_listeners
        if lb_listener_id is not None:
            self._values["lb_listener_id"] = lb_listener_id
        if max_instance_number is not None:
            self._values["max_instance_number"] = max_instance_number
        if min_instance_number is not None:
            self._values["min_instance_number"] = min_instance_number
        if notifications is not None:
            self._values["notifications"] = notifications
        if region is not None:
            self._values["region"] = region
        if scaling_configuration_id is not None:
            self._values["scaling_configuration_id"] = scaling_configuration_id
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def delete_instances(self) -> builtins.str:
        '''Whether to delete instances when they are removed from the AS group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#delete_instances AsGroupV1#delete_instances}
        '''
        result = self._values.get("delete_instances")
        assert result is not None, "Required property 'delete_instances' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def delete_publicip(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#delete_publicip AsGroupV1#delete_publicip}.'''
        result = self._values.get("delete_publicip")
        assert result is not None, "Required property 'delete_publicip' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def networks(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsGroupV1Networks"]]:
        '''networks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#networks AsGroupV1#networks}
        '''
        result = self._values.get("networks")
        assert result is not None, "Required property 'networks' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsGroupV1Networks"]], result)

    @builtins.property
    def scaling_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#scaling_group_name AsGroupV1#scaling_group_name}.'''
        result = self._values.get("scaling_group_name")
        assert result is not None, "Required property 'scaling_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#vpc_id AsGroupV1#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def available_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#available_zones AsGroupV1#available_zones}.'''
        result = self._values.get("available_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cool_down_time(self) -> typing.Optional[jsii.Number]:
        '''The cooling duration, in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#cool_down_time AsGroupV1#cool_down_time}
        '''
        result = self._values.get("cool_down_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def desire_instance_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#desire_instance_number AsGroupV1#desire_instance_number}.'''
        result = self._values.get("desire_instance_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_periodic_audit_grace_period(self) -> typing.Optional[jsii.Number]:
        '''The grace period for instance health check, in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#health_periodic_audit_grace_period AsGroupV1#health_periodic_audit_grace_period}
        '''
        result = self._values.get("health_periodic_audit_grace_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_periodic_audit_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#health_periodic_audit_method AsGroupV1#health_periodic_audit_method}.'''
        result = self._values.get("health_periodic_audit_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_periodic_audit_time(self) -> typing.Optional[jsii.Number]:
        '''The health check period for instances, in minutes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#health_periodic_audit_time AsGroupV1#health_periodic_audit_time}
        '''
        result = self._values.get("health_periodic_audit_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#id AsGroupV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_terminate_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#instance_terminate_policy AsGroupV1#instance_terminate_policy}.'''
        result = self._values.get("instance_terminate_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lbaas_listeners(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsGroupV1LbaasListeners"]]]:
        '''lbaas_listeners block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#lbaas_listeners AsGroupV1#lbaas_listeners}
        '''
        result = self._values.get("lbaas_listeners")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsGroupV1LbaasListeners"]]], result)

    @builtins.property
    def lb_listener_id(self) -> typing.Optional[builtins.str]:
        '''The system supports the binding of up to six classic LB listeners, the IDs of which are separated using a comma.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#lb_listener_id AsGroupV1#lb_listener_id}
        '''
        result = self._values.get("lb_listener_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_instance_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#max_instance_number AsGroupV1#max_instance_number}.'''
        result = self._values.get("max_instance_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_instance_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#min_instance_number AsGroupV1#min_instance_number}.'''
        result = self._values.get("min_instance_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def notifications(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#notifications AsGroupV1#notifications}.'''
        result = self._values.get("notifications")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#region AsGroupV1#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling_configuration_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#scaling_configuration_id AsGroupV1#scaling_configuration_id}.'''
        result = self._values.get("scaling_configuration_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(self) -> typing.Optional["AsGroupV1SecurityGroups"]:
        '''security_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#security_groups AsGroupV1#security_groups}
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional["AsGroupV1SecurityGroups"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#tags AsGroupV1#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AsGroupV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#timeouts AsGroupV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AsGroupV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsGroupV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1LbaasListeners",
    jsii_struct_bases=[],
    name_mapping={
        "pool_id": "poolId",
        "protocol_port": "protocolPort",
        "weight": "weight",
    },
)
class AsGroupV1LbaasListeners:
    def __init__(
        self,
        *,
        pool_id: builtins.str,
        protocol_port: jsii.Number,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#pool_id AsGroupV1#pool_id}.
        :param protocol_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#protocol_port AsGroupV1#protocol_port}.
        :param weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#weight AsGroupV1#weight}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e018b498bccb3aca388ea9af3d0cc03723653e6bfe95a114868828aa5e1f8be)
            check_type(argname="argument pool_id", value=pool_id, expected_type=type_hints["pool_id"])
            check_type(argname="argument protocol_port", value=protocol_port, expected_type=type_hints["protocol_port"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pool_id": pool_id,
            "protocol_port": protocol_port,
        }
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def pool_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#pool_id AsGroupV1#pool_id}.'''
        result = self._values.get("pool_id")
        assert result is not None, "Required property 'pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol_port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#protocol_port AsGroupV1#protocol_port}.'''
        result = self._values.get("protocol_port")
        assert result is not None, "Required property 'protocol_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#weight AsGroupV1#weight}.'''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsGroupV1LbaasListeners(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AsGroupV1LbaasListenersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1LbaasListenersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74796d139f6dc792d8b75e0253fea9c35edf6f970b2a06ac602e41e12efefbb5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AsGroupV1LbaasListenersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4049de7ce9cca491daf37ec99892fe78f936855ea233e2ea31c292aab33eef15)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AsGroupV1LbaasListenersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d25c24070aa1d84f7a2731aed8a3a07e691c4c589508e6fd0a296fdb3d20a3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd525de1df33379b8e1a8bf469766b5e4ddd9b62544bcad9afc6250988fbdac2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b40c1e85519b58f39de9541a318ddc38602c416502590d21a95cb22e38e7e7de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsGroupV1LbaasListeners]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsGroupV1LbaasListeners]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsGroupV1LbaasListeners]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43cfd92b70eab69dbccbbcc6cb8298e8ccbf6ee5384e57d56a5e497fab866af6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AsGroupV1LbaasListenersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1LbaasListenersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c361c9de1974c9c55f52c809c4e44c3ddf312e9cdc02ed9221dd558f2bdb5ff9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetWeight")
    def reset_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeight", []))

    @builtins.property
    @jsii.member(jsii_name="poolIdInput")
    def pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "poolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolPortInput")
    def protocol_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "protocolPortInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="poolId")
    def pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "poolId"))

    @pool_id.setter
    def pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e918c6b729770dcd3fe7e21ea62c9e6991445f46c5aecb3ce539463a2fd9ef25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocolPort")
    def protocol_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "protocolPort"))

    @protocol_port.setter
    def protocol_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac43d0d95f25a763d349939b90ea6be2aab237a6e19eecb1acccd6167a553897)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68f8c3b21be9fc6a379797873c0202e19428e017fa5c01636ca0c65eb62e2293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsGroupV1LbaasListeners]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsGroupV1LbaasListeners]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsGroupV1LbaasListeners]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b41f1e2ac611310870d54c2c0f672ff4f1b45229094b86dfe792bfc0c2348dab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1Networks",
    jsii_struct_bases=[],
    name_mapping={"id": "id"},
)
class AsGroupV1Networks:
    def __init__(self, *, id: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#id AsGroupV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5287edbd5a3980ec6289e610e78912e9cfaf9ce62a7aacd350e116d14107726a)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#id AsGroupV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsGroupV1Networks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AsGroupV1NetworksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1NetworksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2bb3ac9f429cdc53a166d05ffda2f3ce71b48d4c75249fa192029cc52a29af5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AsGroupV1NetworksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d982f901e228879197700dae740f654985418e25b4ac4dbc99f7feb9ad09d2c3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AsGroupV1NetworksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63c7d9780f07b8351b6bed968426adf4e2e3ec4449a26f19e141615b5fcee4fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb307b0cdaad6c4f37f337e2392ded621e9be639aed720104e56f35e28f6a47f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d3405f8ab908a70060a9ff68a9b74a3c85341dc34c33f1a9db42ad3f23d69e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsGroupV1Networks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsGroupV1Networks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsGroupV1Networks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85ef44dbc13a550b71723313a73ec3ba5cb363e8551d4a5b44c152c5cf179102)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AsGroupV1NetworksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1NetworksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__352cf8a6a7c3c1b8568a6405690acd203d883aaa8d2b0dbc1d6774d5261b84e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ae648e359324ea1f91d846007d2341203f9c82895b080253f37e3574006466)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsGroupV1Networks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsGroupV1Networks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsGroupV1Networks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf1f7ba6da4769454a6f1d5bdeddf0a8b31fa621b4292bd5302fa6a41b3ccf4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1SecurityGroups",
    jsii_struct_bases=[],
    name_mapping={"id": "id"},
)
class AsGroupV1SecurityGroups:
    def __init__(self, *, id: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#id AsGroupV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c5d24a0cdf23932d2115f8597102a63e9cbdf4e59ed0c14c6ab5bc3cce819c)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#id AsGroupV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsGroupV1SecurityGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AsGroupV1SecurityGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1SecurityGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac13aa40715609c669c42946a56efcd934c4632de0fb72a830f4fe6dea339dc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98b6add64f8c0894af17a22b304bd134623e987d0577162c956f61a02f5e8c58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AsGroupV1SecurityGroups]:
        return typing.cast(typing.Optional[AsGroupV1SecurityGroups], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AsGroupV1SecurityGroups]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2774b6660b8476e98748f2e0f4ed098fb35f311ded6acfc2d604aafecb9b918)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class AsGroupV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#create AsGroupV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#delete AsGroupV1#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b9fde9e5a1f42e2bd9a2f57c2400f6631ab34a005fd90ed0485f41001261f45)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#create AsGroupV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_group_v1#delete AsGroupV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsGroupV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AsGroupV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asGroupV1.AsGroupV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59997e3b86cf3eaace0544cf2cc3cc9be9f75e55c7b83121f92068e51a843d97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6942151a93cced7b411ee66e11434ed482265dfbe2628824891941e0d0b5beca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90fde3290514194318ee1904c28c215f39dd36176c1fe52b719f17b899a8189c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsGroupV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsGroupV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsGroupV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cdb25117a9a890f79b16cbc6417d488e9360d6b3d11d35ae2dcdac1ca0b2f39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AsGroupV1",
    "AsGroupV1Config",
    "AsGroupV1LbaasListeners",
    "AsGroupV1LbaasListenersList",
    "AsGroupV1LbaasListenersOutputReference",
    "AsGroupV1Networks",
    "AsGroupV1NetworksList",
    "AsGroupV1NetworksOutputReference",
    "AsGroupV1SecurityGroups",
    "AsGroupV1SecurityGroupsOutputReference",
    "AsGroupV1Timeouts",
    "AsGroupV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__dc0bada361aa92f8e15e7730f6e9b17dd049c55944e3f61a771050b056e81ede(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    delete_instances: builtins.str,
    delete_publicip: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    networks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AsGroupV1Networks, typing.Dict[builtins.str, typing.Any]]]],
    scaling_group_name: builtins.str,
    vpc_id: builtins.str,
    available_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cool_down_time: typing.Optional[jsii.Number] = None,
    desire_instance_number: typing.Optional[jsii.Number] = None,
    health_periodic_audit_grace_period: typing.Optional[jsii.Number] = None,
    health_periodic_audit_method: typing.Optional[builtins.str] = None,
    health_periodic_audit_time: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    instance_terminate_policy: typing.Optional[builtins.str] = None,
    lbaas_listeners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AsGroupV1LbaasListeners, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lb_listener_id: typing.Optional[builtins.str] = None,
    max_instance_number: typing.Optional[jsii.Number] = None,
    min_instance_number: typing.Optional[jsii.Number] = None,
    notifications: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    scaling_configuration_id: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Union[AsGroupV1SecurityGroups, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[AsGroupV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6d9892a5d0dfbeaaaf37454c8758324f72dff960b9030f24d1ae064a942436ed(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adcc56aae21ca0859261bf81f7633c345553296d050db36e78514ef20965b0a2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AsGroupV1LbaasListeners, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67672dae4c041830b69b1bb5c9fc11df5f6d5c65ed4796babb3b0190a4c56fca(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AsGroupV1Networks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5075d760a7411ce78f0dcf0e051098541f970247f065ecbb755feaedd32bad3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f80cfbb3f08727898bc9eaee6bba0d13afc6290f210dbe3a16e0a161843b0f72(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91beac19a661336dd22e847a3cdf4fd69e9215cb45443b624c8ded95ffb70dd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f4af8a97c0fc7b231e39a5e73babb03169343a1478f638b63115f49b585615(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd94e89af8882a510ccbadf2b9f2785e9bd8d2d8485cd0e3d8e5266e17bca38(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c7849b460fba4e4ebba01e5a1121e174d016b87fa422bdda69d675d6ca9c475(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9321e80ba646a33bd4c42bd074892b26c63f5b64d13d95e85d2774c818edf97a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5021228cb4f8205a1cb211e6356eb9dd576c3cf2f48556313d036ed164965a1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38122bd5aac8858c21284cdbe9c4d77d9461cec2dc88d958ad3ddd69e834b94d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33fdb0d2d0ff5de64e5b36f95bba6c759b7a9c5c006ea9e72f20701ed22629e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbf4358a1a97bd3343dec306a4dcbb56028ecacc7d49fc47c6f296ce626eb5ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca55894ffbc04da2a7abf01e873265e45481de519c4a163434d1e4d7fc353f7d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b327358d2279491470c173113af35ceac18bcfcaf6a2f1f296728da1279c3feb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e01d81e4b2006c7358281cb0fe1c61d5f586c19642bdf9c1b9aeffdc6c4d15d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12c32a447ee5ba594b21d3ac05471fa5dfe432150f13f8e3558f9de03ea8bc0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66aba9e5993c6f0e01ce2bf77c818a0a676132c1bf281022d6e46ea4d163ebb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3a9d9a65790aa6c77e64b7374d157d4f7fe12f2f5c3e81811e3ed4c43d8fd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b2904bf918483601cc8bf8dcf2b806f183c3e98d674269438fdf3476b53f38(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09157180a4aba88ba6fc743d9fddc753770ca068978b6cb643a5fb80a55d4317(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee75f1381020a62f0bc55040b8fc6d83c5a09cb1d9d21d1b12afcde2b38b991(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    delete_instances: builtins.str,
    delete_publicip: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    networks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AsGroupV1Networks, typing.Dict[builtins.str, typing.Any]]]],
    scaling_group_name: builtins.str,
    vpc_id: builtins.str,
    available_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cool_down_time: typing.Optional[jsii.Number] = None,
    desire_instance_number: typing.Optional[jsii.Number] = None,
    health_periodic_audit_grace_period: typing.Optional[jsii.Number] = None,
    health_periodic_audit_method: typing.Optional[builtins.str] = None,
    health_periodic_audit_time: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    instance_terminate_policy: typing.Optional[builtins.str] = None,
    lbaas_listeners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AsGroupV1LbaasListeners, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lb_listener_id: typing.Optional[builtins.str] = None,
    max_instance_number: typing.Optional[jsii.Number] = None,
    min_instance_number: typing.Optional[jsii.Number] = None,
    notifications: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    scaling_configuration_id: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Union[AsGroupV1SecurityGroups, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[AsGroupV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e018b498bccb3aca388ea9af3d0cc03723653e6bfe95a114868828aa5e1f8be(
    *,
    pool_id: builtins.str,
    protocol_port: jsii.Number,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74796d139f6dc792d8b75e0253fea9c35edf6f970b2a06ac602e41e12efefbb5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4049de7ce9cca491daf37ec99892fe78f936855ea233e2ea31c292aab33eef15(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d25c24070aa1d84f7a2731aed8a3a07e691c4c589508e6fd0a296fdb3d20a3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd525de1df33379b8e1a8bf469766b5e4ddd9b62544bcad9afc6250988fbdac2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b40c1e85519b58f39de9541a318ddc38602c416502590d21a95cb22e38e7e7de(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43cfd92b70eab69dbccbbcc6cb8298e8ccbf6ee5384e57d56a5e497fab866af6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsGroupV1LbaasListeners]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c361c9de1974c9c55f52c809c4e44c3ddf312e9cdc02ed9221dd558f2bdb5ff9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e918c6b729770dcd3fe7e21ea62c9e6991445f46c5aecb3ce539463a2fd9ef25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac43d0d95f25a763d349939b90ea6be2aab237a6e19eecb1acccd6167a553897(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68f8c3b21be9fc6a379797873c0202e19428e017fa5c01636ca0c65eb62e2293(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b41f1e2ac611310870d54c2c0f672ff4f1b45229094b86dfe792bfc0c2348dab(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsGroupV1LbaasListeners]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5287edbd5a3980ec6289e610e78912e9cfaf9ce62a7aacd350e116d14107726a(
    *,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2bb3ac9f429cdc53a166d05ffda2f3ce71b48d4c75249fa192029cc52a29af5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d982f901e228879197700dae740f654985418e25b4ac4dbc99f7feb9ad09d2c3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c7d9780f07b8351b6bed968426adf4e2e3ec4449a26f19e141615b5fcee4fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb307b0cdaad6c4f37f337e2392ded621e9be639aed720104e56f35e28f6a47f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d3405f8ab908a70060a9ff68a9b74a3c85341dc34c33f1a9db42ad3f23d69e9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85ef44dbc13a550b71723313a73ec3ba5cb363e8551d4a5b44c152c5cf179102(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsGroupV1Networks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__352cf8a6a7c3c1b8568a6405690acd203d883aaa8d2b0dbc1d6774d5261b84e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ae648e359324ea1f91d846007d2341203f9c82895b080253f37e3574006466(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf1f7ba6da4769454a6f1d5bdeddf0a8b31fa621b4292bd5302fa6a41b3ccf4c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsGroupV1Networks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c5d24a0cdf23932d2115f8597102a63e9cbdf4e59ed0c14c6ab5bc3cce819c(
    *,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac13aa40715609c669c42946a56efcd934c4632de0fb72a830f4fe6dea339dc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b6add64f8c0894af17a22b304bd134623e987d0577162c956f61a02f5e8c58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2774b6660b8476e98748f2e0f4ed098fb35f311ded6acfc2d604aafecb9b918(
    value: typing.Optional[AsGroupV1SecurityGroups],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b9fde9e5a1f42e2bd9a2f57c2400f6631ab34a005fd90ed0485f41001261f45(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59997e3b86cf3eaace0544cf2cc3cc9be9f75e55c7b83121f92068e51a843d97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6942151a93cced7b411ee66e11434ed482265dfbe2628824891941e0d0b5beca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90fde3290514194318ee1904c28c215f39dd36176c1fe52b719f17b899a8189c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cdb25117a9a890f79b16cbc6417d488e9360d6b3d11d35ae2dcdac1ca0b2f39(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsGroupV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
