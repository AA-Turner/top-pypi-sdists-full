r'''
# `opentelekomcloud_as_policy_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_as_policy_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2).
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


class AsPolicyV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV2.AsPolicyV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2 opentelekomcloud_as_policy_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        scaling_policy_name: builtins.str,
        scaling_policy_type: builtins.str,
        scaling_resource_id: builtins.str,
        scaling_resource_type: builtins.str,
        alarm_id: typing.Optional[builtins.str] = None,
        cool_down_time: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        scaling_policy_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AsPolicyV2ScalingPolicyAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scheduled_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AsPolicyV2ScheduledPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2 opentelekomcloud_as_policy_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param scaling_policy_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#scaling_policy_name AsPolicyV2#scaling_policy_name}.
        :param scaling_policy_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#scaling_policy_type AsPolicyV2#scaling_policy_type}.
        :param scaling_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#scaling_resource_id AsPolicyV2#scaling_resource_id}.
        :param scaling_resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#scaling_resource_type AsPolicyV2#scaling_resource_type}.
        :param alarm_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#alarm_id AsPolicyV2#alarm_id}.
        :param cool_down_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#cool_down_time AsPolicyV2#cool_down_time}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#id AsPolicyV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#region AsPolicyV2#region}.
        :param scaling_policy_action: scaling_policy_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#scaling_policy_action AsPolicyV2#scaling_policy_action}
        :param scheduled_policy: scheduled_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#scheduled_policy AsPolicyV2#scheduled_policy}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed699f96dabd232bb8266527cc39993618963f609f46e724e24a0ac4f88d151b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AsPolicyV2Config(
            scaling_policy_name=scaling_policy_name,
            scaling_policy_type=scaling_policy_type,
            scaling_resource_id=scaling_resource_id,
            scaling_resource_type=scaling_resource_type,
            alarm_id=alarm_id,
            cool_down_time=cool_down_time,
            id=id,
            region=region,
            scaling_policy_action=scaling_policy_action,
            scheduled_policy=scheduled_policy,
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
        '''Generates CDKTF code for importing a AsPolicyV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AsPolicyV2 to import.
        :param import_from_id: The id of the existing AsPolicyV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AsPolicyV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd1427705f22baf1f4c6db5559a023c72414bdf6ebe10d14ad235ebea0c2d13)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putScalingPolicyAction")
    def put_scaling_policy_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AsPolicyV2ScalingPolicyAction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__011ad2fb434c856b009cfa21aa2b760050565bfc23c60e55797789e92342fba4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScalingPolicyAction", [value]))

    @jsii.member(jsii_name="putScheduledPolicy")
    def put_scheduled_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AsPolicyV2ScheduledPolicy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6329a4ecc99fa19be22ddae74f6b7c1023750b179476f63713ca7e642e2ba7a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScheduledPolicy", [value]))

    @jsii.member(jsii_name="resetAlarmId")
    def reset_alarm_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlarmId", []))

    @jsii.member(jsii_name="resetCoolDownTime")
    def reset_cool_down_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoolDownTime", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetScalingPolicyAction")
    def reset_scaling_policy_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScalingPolicyAction", []))

    @jsii.member(jsii_name="resetScheduledPolicy")
    def reset_scheduled_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduledPolicy", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> "AsPolicyV2MetadataList":
        return typing.cast("AsPolicyV2MetadataList", jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="scalingPolicyAction")
    def scaling_policy_action(self) -> "AsPolicyV2ScalingPolicyActionList":
        return typing.cast("AsPolicyV2ScalingPolicyActionList", jsii.get(self, "scalingPolicyAction"))

    @builtins.property
    @jsii.member(jsii_name="scheduledPolicy")
    def scheduled_policy(self) -> "AsPolicyV2ScheduledPolicyList":
        return typing.cast("AsPolicyV2ScheduledPolicyList", jsii.get(self, "scheduledPolicy"))

    @builtins.property
    @jsii.member(jsii_name="alarmIdInput")
    def alarm_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alarmIdInput"))

    @builtins.property
    @jsii.member(jsii_name="coolDownTimeInput")
    def cool_down_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coolDownTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingPolicyActionInput")
    def scaling_policy_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsPolicyV2ScalingPolicyAction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsPolicyV2ScalingPolicyAction"]]], jsii.get(self, "scalingPolicyActionInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingPolicyNameInput")
    def scaling_policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingPolicyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingPolicyTypeInput")
    def scaling_policy_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingPolicyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingResourceIdInput")
    def scaling_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingResourceTypeInput")
    def scaling_resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingResourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduledPolicyInput")
    def scheduled_policy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsPolicyV2ScheduledPolicy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsPolicyV2ScheduledPolicy"]]], jsii.get(self, "scheduledPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="alarmId")
    def alarm_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alarmId"))

    @alarm_id.setter
    def alarm_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__286533eb110bf1b897f6ef8abc9727c2f599c9a7a10981db10eabb322978c58e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="coolDownTime")
    def cool_down_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "coolDownTime"))

    @cool_down_time.setter
    def cool_down_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b4c12383de881c6996d070c6bdbb0bb60343affe9f77c77c4a95bc227371a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coolDownTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__841ba6797671e6fa8936341cbb9eca7da7e30cb3164f9d0a4d6c2a74c79c7de5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29e172906e4f807a2c5ea2a70ba22050c03c9f7b7c548df51eb2c9631ecd52dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scalingPolicyName")
    def scaling_policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingPolicyName"))

    @scaling_policy_name.setter
    def scaling_policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7817e90a56ddef13cd8a1f479c539f80d70b4175201e6aa7a6488a37bf226403)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingPolicyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scalingPolicyType")
    def scaling_policy_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingPolicyType"))

    @scaling_policy_type.setter
    def scaling_policy_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0af590c47e7d1d2c404b68f5d73d0e1257775438c4dc6c819ed8fdb9396d3af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingPolicyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scalingResourceId")
    def scaling_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingResourceId"))

    @scaling_resource_id.setter
    def scaling_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48de529da382fa6ffe14f7dadccc220d3338ccbba21755e86da4aabe772c2831)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scalingResourceType")
    def scaling_resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingResourceType"))

    @scaling_resource_type.setter
    def scaling_resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bda0a141d1ce621b3a5c0b605991d59c6cd3ca1eefcfa9ad3297adffafa30d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingResourceType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV2.AsPolicyV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "scaling_policy_name": "scalingPolicyName",
        "scaling_policy_type": "scalingPolicyType",
        "scaling_resource_id": "scalingResourceId",
        "scaling_resource_type": "scalingResourceType",
        "alarm_id": "alarmId",
        "cool_down_time": "coolDownTime",
        "id": "id",
        "region": "region",
        "scaling_policy_action": "scalingPolicyAction",
        "scheduled_policy": "scheduledPolicy",
    },
)
class AsPolicyV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        scaling_policy_name: builtins.str,
        scaling_policy_type: builtins.str,
        scaling_resource_id: builtins.str,
        scaling_resource_type: builtins.str,
        alarm_id: typing.Optional[builtins.str] = None,
        cool_down_time: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        scaling_policy_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AsPolicyV2ScalingPolicyAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scheduled_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AsPolicyV2ScheduledPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param scaling_policy_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#scaling_policy_name AsPolicyV2#scaling_policy_name}.
        :param scaling_policy_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#scaling_policy_type AsPolicyV2#scaling_policy_type}.
        :param scaling_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#scaling_resource_id AsPolicyV2#scaling_resource_id}.
        :param scaling_resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#scaling_resource_type AsPolicyV2#scaling_resource_type}.
        :param alarm_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#alarm_id AsPolicyV2#alarm_id}.
        :param cool_down_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#cool_down_time AsPolicyV2#cool_down_time}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#id AsPolicyV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#region AsPolicyV2#region}.
        :param scaling_policy_action: scaling_policy_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#scaling_policy_action AsPolicyV2#scaling_policy_action}
        :param scheduled_policy: scheduled_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#scheduled_policy AsPolicyV2#scheduled_policy}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad1bf52cf188e0c8028ff3bd48ce4e084b4282553c767c8d30f6e7afd0efcc25)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument scaling_policy_name", value=scaling_policy_name, expected_type=type_hints["scaling_policy_name"])
            check_type(argname="argument scaling_policy_type", value=scaling_policy_type, expected_type=type_hints["scaling_policy_type"])
            check_type(argname="argument scaling_resource_id", value=scaling_resource_id, expected_type=type_hints["scaling_resource_id"])
            check_type(argname="argument scaling_resource_type", value=scaling_resource_type, expected_type=type_hints["scaling_resource_type"])
            check_type(argname="argument alarm_id", value=alarm_id, expected_type=type_hints["alarm_id"])
            check_type(argname="argument cool_down_time", value=cool_down_time, expected_type=type_hints["cool_down_time"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument scaling_policy_action", value=scaling_policy_action, expected_type=type_hints["scaling_policy_action"])
            check_type(argname="argument scheduled_policy", value=scheduled_policy, expected_type=type_hints["scheduled_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scaling_policy_name": scaling_policy_name,
            "scaling_policy_type": scaling_policy_type,
            "scaling_resource_id": scaling_resource_id,
            "scaling_resource_type": scaling_resource_type,
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
        if alarm_id is not None:
            self._values["alarm_id"] = alarm_id
        if cool_down_time is not None:
            self._values["cool_down_time"] = cool_down_time
        if id is not None:
            self._values["id"] = id
        if region is not None:
            self._values["region"] = region
        if scaling_policy_action is not None:
            self._values["scaling_policy_action"] = scaling_policy_action
        if scheduled_policy is not None:
            self._values["scheduled_policy"] = scheduled_policy

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
    def scaling_policy_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#scaling_policy_name AsPolicyV2#scaling_policy_name}.'''
        result = self._values.get("scaling_policy_name")
        assert result is not None, "Required property 'scaling_policy_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scaling_policy_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#scaling_policy_type AsPolicyV2#scaling_policy_type}.'''
        result = self._values.get("scaling_policy_type")
        assert result is not None, "Required property 'scaling_policy_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scaling_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#scaling_resource_id AsPolicyV2#scaling_resource_id}.'''
        result = self._values.get("scaling_resource_id")
        assert result is not None, "Required property 'scaling_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scaling_resource_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#scaling_resource_type AsPolicyV2#scaling_resource_type}.'''
        result = self._values.get("scaling_resource_type")
        assert result is not None, "Required property 'scaling_resource_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alarm_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#alarm_id AsPolicyV2#alarm_id}.'''
        result = self._values.get("alarm_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cool_down_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#cool_down_time AsPolicyV2#cool_down_time}.'''
        result = self._values.get("cool_down_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#id AsPolicyV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#region AsPolicyV2#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling_policy_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsPolicyV2ScalingPolicyAction"]]]:
        '''scaling_policy_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#scaling_policy_action AsPolicyV2#scaling_policy_action}
        '''
        result = self._values.get("scaling_policy_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsPolicyV2ScalingPolicyAction"]]], result)

    @builtins.property
    def scheduled_policy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsPolicyV2ScheduledPolicy"]]]:
        '''scheduled_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#scheduled_policy AsPolicyV2#scheduled_policy}
        '''
        result = self._values.get("scheduled_policy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AsPolicyV2ScheduledPolicy"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsPolicyV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV2.AsPolicyV2Metadata",
    jsii_struct_bases=[],
    name_mapping={},
)
class AsPolicyV2Metadata:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsPolicyV2Metadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AsPolicyV2MetadataList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV2.AsPolicyV2MetadataList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c447de1a8e156c8dcc38841e7f8eab7562f5e6de9753391e379a4894f1fa55d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AsPolicyV2MetadataOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__069a9c7c6c7006ec3b03e13b306d5658c7ffbe084fd705dd8df9319f0a94d35c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AsPolicyV2MetadataOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__062b0e162eeac652ac399660204c1c879ebf8232d77b866056be69a61cc192cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05d1da3f1add604cba5c027d209e3d98025b6356b6340aff35c1f4d6fcb10c19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f60068147912527a13f107fd08136ed4b647eb42fa0231fad6509cf802069a94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class AsPolicyV2MetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV2.AsPolicyV2MetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e45392f2ce3128d85e2e9b2d2204a21776fadb52c3973476da40432cbb13f6d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="bandwidthShareType")
    def bandwidth_share_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidthShareType"))

    @builtins.property
    @jsii.member(jsii_name="eipAddress")
    def eip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eipAddress"))

    @builtins.property
    @jsii.member(jsii_name="eipId")
    def eip_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eipId"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AsPolicyV2Metadata]:
        return typing.cast(typing.Optional[AsPolicyV2Metadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AsPolicyV2Metadata]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33588c7c16830afa9afce53eafd3be5f87a266cc1bdb67cc574bee2b09491492)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV2.AsPolicyV2ScalingPolicyAction",
    jsii_struct_bases=[],
    name_mapping={
        "limits": "limits",
        "operation": "operation",
        "percentage": "percentage",
        "size": "size",
    },
)
class AsPolicyV2ScalingPolicyAction:
    def __init__(
        self,
        *,
        limits: typing.Optional[jsii.Number] = None,
        operation: typing.Optional[builtins.str] = None,
        percentage: typing.Optional[jsii.Number] = None,
        size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param limits: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#limits AsPolicyV2#limits}.
        :param operation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#operation AsPolicyV2#operation}.
        :param percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#percentage AsPolicyV2#percentage}.
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#size AsPolicyV2#size}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9ba47b625421024409efd04f32ea8f43a5a572e40f192cb7a48cdaf6be69f55)
            check_type(argname="argument limits", value=limits, expected_type=type_hints["limits"])
            check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
            check_type(argname="argument percentage", value=percentage, expected_type=type_hints["percentage"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if limits is not None:
            self._values["limits"] = limits
        if operation is not None:
            self._values["operation"] = operation
        if percentage is not None:
            self._values["percentage"] = percentage
        if size is not None:
            self._values["size"] = size

    @builtins.property
    def limits(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#limits AsPolicyV2#limits}.'''
        result = self._values.get("limits")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def operation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#operation AsPolicyV2#operation}.'''
        result = self._values.get("operation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#percentage AsPolicyV2#percentage}.'''
        result = self._values.get("percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#size AsPolicyV2#size}.'''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsPolicyV2ScalingPolicyAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AsPolicyV2ScalingPolicyActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV2.AsPolicyV2ScalingPolicyActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73b58ebf9359a196ca1d5e415862b1119234964c6a5ebc9928fd57d489e4f9f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AsPolicyV2ScalingPolicyActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af60bf0a42b4b123f2bfce13c6471092a9b65a53f363ff36b1b766900d61202)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AsPolicyV2ScalingPolicyActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e116d3b58499d5fb393147abf7dfdde5f8ae5c45f7abb0f417470d7163555f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08644006f48dee3c7a0b1d09873454ed7f54cd5d3352c962660183aa1c36a741)
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
            type_hints = typing.get_type_hints(_typecheckingstub__200bda376fbc75b227741ad0585fb2791d9e6c10067f0bf2f74fee5967402458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsPolicyV2ScalingPolicyAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsPolicyV2ScalingPolicyAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsPolicyV2ScalingPolicyAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__645affe1bd3e5c768a6df332778e7a5c11bdaf4e5a90137b80aac105198c407e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AsPolicyV2ScalingPolicyActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV2.AsPolicyV2ScalingPolicyActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d624bb3e9e4f0174df87933659f78a545f61236c70fa2483a44c71e34d62990)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLimits")
    def reset_limits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimits", []))

    @jsii.member(jsii_name="resetOperation")
    def reset_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperation", []))

    @jsii.member(jsii_name="resetPercentage")
    def reset_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPercentage", []))

    @jsii.member(jsii_name="resetSize")
    def reset_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSize", []))

    @builtins.property
    @jsii.member(jsii_name="limitsInput")
    def limits_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "limitsInput"))

    @builtins.property
    @jsii.member(jsii_name="operationInput")
    def operation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationInput"))

    @builtins.property
    @jsii.member(jsii_name="percentageInput")
    def percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "percentageInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="limits")
    def limits(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "limits"))

    @limits.setter
    def limits(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9695973628f252d92c906ef7e84a9d254e38e8c476bc5e784d3d08830c533fe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operation")
    def operation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operation"))

    @operation.setter
    def operation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d0dbb87752df808928ae9308003d172e344dc0f9b8ed166d068fa35b39e076f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percentage")
    def percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percentage"))

    @percentage.setter
    def percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69647f83866a78feacee074953e51ebee22a7d8f3087a8a9eb8c18323a052988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19d39499173580091da0f98885d591fbb8e2914bffecfe2f0d124418ca603aa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsPolicyV2ScalingPolicyAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsPolicyV2ScalingPolicyAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsPolicyV2ScalingPolicyAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d508b3d661f79b28affdd4f27ae574d30eef4179f14fd9259b39b405e36dcae6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV2.AsPolicyV2ScheduledPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "launch_time": "launchTime",
        "end_time": "endTime",
        "recurrence_type": "recurrenceType",
        "recurrence_value": "recurrenceValue",
        "start_time": "startTime",
    },
)
class AsPolicyV2ScheduledPolicy:
    def __init__(
        self,
        *,
        launch_time: builtins.str,
        end_time: typing.Optional[builtins.str] = None,
        recurrence_type: typing.Optional[builtins.str] = None,
        recurrence_value: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param launch_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#launch_time AsPolicyV2#launch_time}.
        :param end_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#end_time AsPolicyV2#end_time}.
        :param recurrence_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#recurrence_type AsPolicyV2#recurrence_type}.
        :param recurrence_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#recurrence_value AsPolicyV2#recurrence_value}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#start_time AsPolicyV2#start_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__612b6023156ef0d0d60ad39ec9c46c2748ca04e8ede9164b6975c32e8148bc7e)
            check_type(argname="argument launch_time", value=launch_time, expected_type=type_hints["launch_time"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument recurrence_type", value=recurrence_type, expected_type=type_hints["recurrence_type"])
            check_type(argname="argument recurrence_value", value=recurrence_value, expected_type=type_hints["recurrence_value"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "launch_time": launch_time,
        }
        if end_time is not None:
            self._values["end_time"] = end_time
        if recurrence_type is not None:
            self._values["recurrence_type"] = recurrence_type
        if recurrence_value is not None:
            self._values["recurrence_value"] = recurrence_value
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def launch_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#launch_time AsPolicyV2#launch_time}.'''
        result = self._values.get("launch_time")
        assert result is not None, "Required property 'launch_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#end_time AsPolicyV2#end_time}.'''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recurrence_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#recurrence_type AsPolicyV2#recurrence_type}.'''
        result = self._values.get("recurrence_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recurrence_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#recurrence_value AsPolicyV2#recurrence_value}.'''
        result = self._values.get("recurrence_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v2#start_time AsPolicyV2#start_time}.'''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsPolicyV2ScheduledPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AsPolicyV2ScheduledPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV2.AsPolicyV2ScheduledPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bae95392a922093cf7a0ad182c59254baa2a00dc88ea9062294f5a16bf87f1bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AsPolicyV2ScheduledPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfdf874457b165a1560b52af2746397d327ec73c6480570affc8ea7bdb7abef9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AsPolicyV2ScheduledPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2af036d5e29d8b6c72eb8d87fa9a7c5f81f33bff3a1101bcf0236634c53302f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7291c8458d92ccda47d2f8e3347a6019e846491720f25c8d669d3f8e2d46a09c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c0e3a7fd2034723540d7de988c4f7c6923d2f8dbcfe0d9d44371157a94b900c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsPolicyV2ScheduledPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsPolicyV2ScheduledPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsPolicyV2ScheduledPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03c7d5c0d816ae70af2a33ebbe346c6f34a105a1a272d5ac0e15c7081991c788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AsPolicyV2ScheduledPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV2.AsPolicyV2ScheduledPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b3673287af5d1721d9b78b98f4ab68279aebd1064392eaacde278f6e4b4d0eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEndTime")
    def reset_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTime", []))

    @jsii.member(jsii_name="resetRecurrenceType")
    def reset_recurrence_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecurrenceType", []))

    @jsii.member(jsii_name="resetRecurrenceValue")
    def reset_recurrence_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecurrenceValue", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="launchTimeInput")
    def launch_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "launchTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceTypeInput")
    def recurrence_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recurrenceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceValueInput")
    def recurrence_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recurrenceValueInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__778c1f143daef684af63cf3ef11ce1d9079a817832a998437441d567d7cbeaa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="launchTime")
    def launch_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "launchTime"))

    @launch_time.setter
    def launch_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__688d3d6e9a12cec2773cc948005f96758f453ca2b129234057e1385fced0d7e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recurrenceType")
    def recurrence_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recurrenceType"))

    @recurrence_type.setter
    def recurrence_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f0367d5b4b389ab56add00f8df01a1356ecc31e9866ec5715825e5ef155a0c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrenceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recurrenceValue")
    def recurrence_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recurrenceValue"))

    @recurrence_value.setter
    def recurrence_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b226096b4b595d241c327939024096b651ab99ac95ca8f3ae2ea4aca97511e0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrenceValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d4ee89c3cd1cf2b54c6d739033c42eee38e3ffae3cc373b4a7c26b2112b65d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsPolicyV2ScheduledPolicy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsPolicyV2ScheduledPolicy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsPolicyV2ScheduledPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41640282fee4222294b078a0cc5d9b2f494f2f1175d0b7fb0cf492a347f515db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AsPolicyV2",
    "AsPolicyV2Config",
    "AsPolicyV2Metadata",
    "AsPolicyV2MetadataList",
    "AsPolicyV2MetadataOutputReference",
    "AsPolicyV2ScalingPolicyAction",
    "AsPolicyV2ScalingPolicyActionList",
    "AsPolicyV2ScalingPolicyActionOutputReference",
    "AsPolicyV2ScheduledPolicy",
    "AsPolicyV2ScheduledPolicyList",
    "AsPolicyV2ScheduledPolicyOutputReference",
]

publication.publish()

def _typecheckingstub__ed699f96dabd232bb8266527cc39993618963f609f46e724e24a0ac4f88d151b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    scaling_policy_name: builtins.str,
    scaling_policy_type: builtins.str,
    scaling_resource_id: builtins.str,
    scaling_resource_type: builtins.str,
    alarm_id: typing.Optional[builtins.str] = None,
    cool_down_time: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    scaling_policy_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AsPolicyV2ScalingPolicyAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scheduled_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AsPolicyV2ScheduledPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__6fd1427705f22baf1f4c6db5559a023c72414bdf6ebe10d14ad235ebea0c2d13(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__011ad2fb434c856b009cfa21aa2b760050565bfc23c60e55797789e92342fba4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AsPolicyV2ScalingPolicyAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6329a4ecc99fa19be22ddae74f6b7c1023750b179476f63713ca7e642e2ba7a7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AsPolicyV2ScheduledPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286533eb110bf1b897f6ef8abc9727c2f599c9a7a10981db10eabb322978c58e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b4c12383de881c6996d070c6bdbb0bb60343affe9f77c77c4a95bc227371a6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__841ba6797671e6fa8936341cbb9eca7da7e30cb3164f9d0a4d6c2a74c79c7de5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29e172906e4f807a2c5ea2a70ba22050c03c9f7b7c548df51eb2c9631ecd52dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7817e90a56ddef13cd8a1f479c539f80d70b4175201e6aa7a6488a37bf226403(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0af590c47e7d1d2c404b68f5d73d0e1257775438c4dc6c819ed8fdb9396d3af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48de529da382fa6ffe14f7dadccc220d3338ccbba21755e86da4aabe772c2831(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bda0a141d1ce621b3a5c0b605991d59c6cd3ca1eefcfa9ad3297adffafa30d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad1bf52cf188e0c8028ff3bd48ce4e084b4282553c767c8d30f6e7afd0efcc25(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scaling_policy_name: builtins.str,
    scaling_policy_type: builtins.str,
    scaling_resource_id: builtins.str,
    scaling_resource_type: builtins.str,
    alarm_id: typing.Optional[builtins.str] = None,
    cool_down_time: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    scaling_policy_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AsPolicyV2ScalingPolicyAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scheduled_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AsPolicyV2ScheduledPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c447de1a8e156c8dcc38841e7f8eab7562f5e6de9753391e379a4894f1fa55d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__069a9c7c6c7006ec3b03e13b306d5658c7ffbe084fd705dd8df9319f0a94d35c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__062b0e162eeac652ac399660204c1c879ebf8232d77b866056be69a61cc192cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d1da3f1add604cba5c027d209e3d98025b6356b6340aff35c1f4d6fcb10c19(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60068147912527a13f107fd08136ed4b647eb42fa0231fad6509cf802069a94(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e45392f2ce3128d85e2e9b2d2204a21776fadb52c3973476da40432cbb13f6d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33588c7c16830afa9afce53eafd3be5f87a266cc1bdb67cc574bee2b09491492(
    value: typing.Optional[AsPolicyV2Metadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ba47b625421024409efd04f32ea8f43a5a572e40f192cb7a48cdaf6be69f55(
    *,
    limits: typing.Optional[jsii.Number] = None,
    operation: typing.Optional[builtins.str] = None,
    percentage: typing.Optional[jsii.Number] = None,
    size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73b58ebf9359a196ca1d5e415862b1119234964c6a5ebc9928fd57d489e4f9f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af60bf0a42b4b123f2bfce13c6471092a9b65a53f363ff36b1b766900d61202(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e116d3b58499d5fb393147abf7dfdde5f8ae5c45f7abb0f417470d7163555f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08644006f48dee3c7a0b1d09873454ed7f54cd5d3352c962660183aa1c36a741(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__200bda376fbc75b227741ad0585fb2791d9e6c10067f0bf2f74fee5967402458(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645affe1bd3e5c768a6df332778e7a5c11bdaf4e5a90137b80aac105198c407e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsPolicyV2ScalingPolicyAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d624bb3e9e4f0174df87933659f78a545f61236c70fa2483a44c71e34d62990(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9695973628f252d92c906ef7e84a9d254e38e8c476bc5e784d3d08830c533fe7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d0dbb87752df808928ae9308003d172e344dc0f9b8ed166d068fa35b39e076f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69647f83866a78feacee074953e51ebee22a7d8f3087a8a9eb8c18323a052988(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19d39499173580091da0f98885d591fbb8e2914bffecfe2f0d124418ca603aa6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d508b3d661f79b28affdd4f27ae574d30eef4179f14fd9259b39b405e36dcae6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsPolicyV2ScalingPolicyAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__612b6023156ef0d0d60ad39ec9c46c2748ca04e8ede9164b6975c32e8148bc7e(
    *,
    launch_time: builtins.str,
    end_time: typing.Optional[builtins.str] = None,
    recurrence_type: typing.Optional[builtins.str] = None,
    recurrence_value: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae95392a922093cf7a0ad182c59254baa2a00dc88ea9062294f5a16bf87f1bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfdf874457b165a1560b52af2746397d327ec73c6480570affc8ea7bdb7abef9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2af036d5e29d8b6c72eb8d87fa9a7c5f81f33bff3a1101bcf0236634c53302f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7291c8458d92ccda47d2f8e3347a6019e846491720f25c8d669d3f8e2d46a09c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c0e3a7fd2034723540d7de988c4f7c6923d2f8dbcfe0d9d44371157a94b900c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03c7d5c0d816ae70af2a33ebbe346c6f34a105a1a272d5ac0e15c7081991c788(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AsPolicyV2ScheduledPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b3673287af5d1721d9b78b98f4ab68279aebd1064392eaacde278f6e4b4d0eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__778c1f143daef684af63cf3ef11ce1d9079a817832a998437441d567d7cbeaa4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__688d3d6e9a12cec2773cc948005f96758f453ca2b129234057e1385fced0d7e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f0367d5b4b389ab56add00f8df01a1356ecc31e9866ec5715825e5ef155a0c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b226096b4b595d241c327939024096b651ab99ac95ca8f3ae2ea4aca97511e0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d4ee89c3cd1cf2b54c6d739033c42eee38e3ffae3cc373b4a7c26b2112b65d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41640282fee4222294b078a0cc5d9b2f494f2f1175d0b7fb0cf492a347f515db(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AsPolicyV2ScheduledPolicy]],
) -> None:
    """Type checking stubs"""
    pass
