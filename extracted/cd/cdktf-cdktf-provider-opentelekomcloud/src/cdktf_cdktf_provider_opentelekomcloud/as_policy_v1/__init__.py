r'''
# `opentelekomcloud_as_policy_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_as_policy_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1).
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


class AsPolicyV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV1.AsPolicyV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1 opentelekomcloud_as_policy_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        scaling_group_id: builtins.str,
        scaling_policy_name: builtins.str,
        scaling_policy_type: builtins.str,
        alarm_id: typing.Optional[builtins.str] = None,
        cool_down_time: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        scaling_policy_action: typing.Optional[typing.Union["AsPolicyV1ScalingPolicyAction", typing.Dict[builtins.str, typing.Any]]] = None,
        scheduled_policy: typing.Optional[typing.Union["AsPolicyV1ScheduledPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1 opentelekomcloud_as_policy_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param scaling_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#scaling_group_id AsPolicyV1#scaling_group_id}.
        :param scaling_policy_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#scaling_policy_name AsPolicyV1#scaling_policy_name}.
        :param scaling_policy_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#scaling_policy_type AsPolicyV1#scaling_policy_type}.
        :param alarm_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#alarm_id AsPolicyV1#alarm_id}.
        :param cool_down_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#cool_down_time AsPolicyV1#cool_down_time}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#id AsPolicyV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#region AsPolicyV1#region}.
        :param scaling_policy_action: scaling_policy_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#scaling_policy_action AsPolicyV1#scaling_policy_action}
        :param scheduled_policy: scheduled_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#scheduled_policy AsPolicyV1#scheduled_policy}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__591e0f1c77e71a5dd1844962e54549ce73ef0cca30292daf3a0f8981602c2834)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AsPolicyV1Config(
            scaling_group_id=scaling_group_id,
            scaling_policy_name=scaling_policy_name,
            scaling_policy_type=scaling_policy_type,
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
        '''Generates CDKTF code for importing a AsPolicyV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AsPolicyV1 to import.
        :param import_from_id: The id of the existing AsPolicyV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AsPolicyV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bab287ec81809a489ad4b71b3009f96fed470bd7955b1ae9037bff21fbacaff)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putScalingPolicyAction")
    def put_scaling_policy_action(
        self,
        *,
        instance_number: typing.Optional[jsii.Number] = None,
        operation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#instance_number AsPolicyV1#instance_number}.
        :param operation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#operation AsPolicyV1#operation}.
        '''
        value = AsPolicyV1ScalingPolicyAction(
            instance_number=instance_number, operation=operation
        )

        return typing.cast(None, jsii.invoke(self, "putScalingPolicyAction", [value]))

    @jsii.member(jsii_name="putScheduledPolicy")
    def put_scheduled_policy(
        self,
        *,
        launch_time: builtins.str,
        end_time: typing.Optional[builtins.str] = None,
        recurrence_type: typing.Optional[builtins.str] = None,
        recurrence_value: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param launch_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#launch_time AsPolicyV1#launch_time}.
        :param end_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#end_time AsPolicyV1#end_time}.
        :param recurrence_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#recurrence_type AsPolicyV1#recurrence_type}.
        :param recurrence_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#recurrence_value AsPolicyV1#recurrence_value}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#start_time AsPolicyV1#start_time}.
        '''
        value = AsPolicyV1ScheduledPolicy(
            launch_time=launch_time,
            end_time=end_time,
            recurrence_type=recurrence_type,
            recurrence_value=recurrence_value,
            start_time=start_time,
        )

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
    @jsii.member(jsii_name="scalingPolicyAction")
    def scaling_policy_action(self) -> "AsPolicyV1ScalingPolicyActionOutputReference":
        return typing.cast("AsPolicyV1ScalingPolicyActionOutputReference", jsii.get(self, "scalingPolicyAction"))

    @builtins.property
    @jsii.member(jsii_name="scheduledPolicy")
    def scheduled_policy(self) -> "AsPolicyV1ScheduledPolicyOutputReference":
        return typing.cast("AsPolicyV1ScheduledPolicyOutputReference", jsii.get(self, "scheduledPolicy"))

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
    @jsii.member(jsii_name="scalingGroupIdInput")
    def scaling_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingPolicyActionInput")
    def scaling_policy_action_input(
        self,
    ) -> typing.Optional["AsPolicyV1ScalingPolicyAction"]:
        return typing.cast(typing.Optional["AsPolicyV1ScalingPolicyAction"], jsii.get(self, "scalingPolicyActionInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingPolicyNameInput")
    def scaling_policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingPolicyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingPolicyTypeInput")
    def scaling_policy_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingPolicyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduledPolicyInput")
    def scheduled_policy_input(self) -> typing.Optional["AsPolicyV1ScheduledPolicy"]:
        return typing.cast(typing.Optional["AsPolicyV1ScheduledPolicy"], jsii.get(self, "scheduledPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="alarmId")
    def alarm_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alarmId"))

    @alarm_id.setter
    def alarm_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64fd82e51176a8449607a7772408b235e1e6f8e8a1838db9a180bb9e9668f36f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="coolDownTime")
    def cool_down_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "coolDownTime"))

    @cool_down_time.setter
    def cool_down_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a14b981e630878f04b1a3b5e1b994541297d8e44dfec494cafdd497acf5fbe62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coolDownTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be123a2ce99e015ea3d1f71bc5dca3b1b4f7e402cb22c47a8af16772771e58da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20493d3b364ded6883bfa51915c14ea40d9c4d20b52f331ceeb325323d3ef351)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scalingGroupId")
    def scaling_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingGroupId"))

    @scaling_group_id.setter
    def scaling_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ba56b0771055c6dd8e611d475a5c6d4ab623d0419ee7a04b955af46a35113c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scalingPolicyName")
    def scaling_policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingPolicyName"))

    @scaling_policy_name.setter
    def scaling_policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aac4b9463530c3649f2bc4b111534aa5b8aafd7d8881f502427911844c6dec6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingPolicyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scalingPolicyType")
    def scaling_policy_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingPolicyType"))

    @scaling_policy_type.setter
    def scaling_policy_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ca84b89b629beb8443eaed4d7440cc9324ce4f239a89d0072afc3e951c2a29d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingPolicyType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV1.AsPolicyV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "scaling_group_id": "scalingGroupId",
        "scaling_policy_name": "scalingPolicyName",
        "scaling_policy_type": "scalingPolicyType",
        "alarm_id": "alarmId",
        "cool_down_time": "coolDownTime",
        "id": "id",
        "region": "region",
        "scaling_policy_action": "scalingPolicyAction",
        "scheduled_policy": "scheduledPolicy",
    },
)
class AsPolicyV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        scaling_group_id: builtins.str,
        scaling_policy_name: builtins.str,
        scaling_policy_type: builtins.str,
        alarm_id: typing.Optional[builtins.str] = None,
        cool_down_time: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        scaling_policy_action: typing.Optional[typing.Union["AsPolicyV1ScalingPolicyAction", typing.Dict[builtins.str, typing.Any]]] = None,
        scheduled_policy: typing.Optional[typing.Union["AsPolicyV1ScheduledPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param scaling_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#scaling_group_id AsPolicyV1#scaling_group_id}.
        :param scaling_policy_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#scaling_policy_name AsPolicyV1#scaling_policy_name}.
        :param scaling_policy_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#scaling_policy_type AsPolicyV1#scaling_policy_type}.
        :param alarm_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#alarm_id AsPolicyV1#alarm_id}.
        :param cool_down_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#cool_down_time AsPolicyV1#cool_down_time}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#id AsPolicyV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#region AsPolicyV1#region}.
        :param scaling_policy_action: scaling_policy_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#scaling_policy_action AsPolicyV1#scaling_policy_action}
        :param scheduled_policy: scheduled_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#scheduled_policy AsPolicyV1#scheduled_policy}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(scaling_policy_action, dict):
            scaling_policy_action = AsPolicyV1ScalingPolicyAction(**scaling_policy_action)
        if isinstance(scheduled_policy, dict):
            scheduled_policy = AsPolicyV1ScheduledPolicy(**scheduled_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0af2f752d29d467d2bf07567af297712f343380a1ee69389d40bf012ecdad28f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument scaling_group_id", value=scaling_group_id, expected_type=type_hints["scaling_group_id"])
            check_type(argname="argument scaling_policy_name", value=scaling_policy_name, expected_type=type_hints["scaling_policy_name"])
            check_type(argname="argument scaling_policy_type", value=scaling_policy_type, expected_type=type_hints["scaling_policy_type"])
            check_type(argname="argument alarm_id", value=alarm_id, expected_type=type_hints["alarm_id"])
            check_type(argname="argument cool_down_time", value=cool_down_time, expected_type=type_hints["cool_down_time"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument scaling_policy_action", value=scaling_policy_action, expected_type=type_hints["scaling_policy_action"])
            check_type(argname="argument scheduled_policy", value=scheduled_policy, expected_type=type_hints["scheduled_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scaling_group_id": scaling_group_id,
            "scaling_policy_name": scaling_policy_name,
            "scaling_policy_type": scaling_policy_type,
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
    def scaling_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#scaling_group_id AsPolicyV1#scaling_group_id}.'''
        result = self._values.get("scaling_group_id")
        assert result is not None, "Required property 'scaling_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scaling_policy_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#scaling_policy_name AsPolicyV1#scaling_policy_name}.'''
        result = self._values.get("scaling_policy_name")
        assert result is not None, "Required property 'scaling_policy_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scaling_policy_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#scaling_policy_type AsPolicyV1#scaling_policy_type}.'''
        result = self._values.get("scaling_policy_type")
        assert result is not None, "Required property 'scaling_policy_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alarm_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#alarm_id AsPolicyV1#alarm_id}.'''
        result = self._values.get("alarm_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cool_down_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#cool_down_time AsPolicyV1#cool_down_time}.'''
        result = self._values.get("cool_down_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#id AsPolicyV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#region AsPolicyV1#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling_policy_action(self) -> typing.Optional["AsPolicyV1ScalingPolicyAction"]:
        '''scaling_policy_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#scaling_policy_action AsPolicyV1#scaling_policy_action}
        '''
        result = self._values.get("scaling_policy_action")
        return typing.cast(typing.Optional["AsPolicyV1ScalingPolicyAction"], result)

    @builtins.property
    def scheduled_policy(self) -> typing.Optional["AsPolicyV1ScheduledPolicy"]:
        '''scheduled_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#scheduled_policy AsPolicyV1#scheduled_policy}
        '''
        result = self._values.get("scheduled_policy")
        return typing.cast(typing.Optional["AsPolicyV1ScheduledPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsPolicyV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV1.AsPolicyV1ScalingPolicyAction",
    jsii_struct_bases=[],
    name_mapping={"instance_number": "instanceNumber", "operation": "operation"},
)
class AsPolicyV1ScalingPolicyAction:
    def __init__(
        self,
        *,
        instance_number: typing.Optional[jsii.Number] = None,
        operation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#instance_number AsPolicyV1#instance_number}.
        :param operation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#operation AsPolicyV1#operation}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd675edbd2d840117e95d492ef8a1a0bdcb9ba699d244fd2c1c4c3a1c3522bc1)
            check_type(argname="argument instance_number", value=instance_number, expected_type=type_hints["instance_number"])
            check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_number is not None:
            self._values["instance_number"] = instance_number
        if operation is not None:
            self._values["operation"] = operation

    @builtins.property
    def instance_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#instance_number AsPolicyV1#instance_number}.'''
        result = self._values.get("instance_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def operation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#operation AsPolicyV1#operation}.'''
        result = self._values.get("operation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsPolicyV1ScalingPolicyAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AsPolicyV1ScalingPolicyActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV1.AsPolicyV1ScalingPolicyActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e980e7ba920c55c7821f71eca46f2407822c1ac2cb8dc6eb6a67b3a7e7f9ee5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstanceNumber")
    def reset_instance_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceNumber", []))

    @jsii.member(jsii_name="resetOperation")
    def reset_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperation", []))

    @builtins.property
    @jsii.member(jsii_name="instanceNumberInput")
    def instance_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "instanceNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="operationInput")
    def operation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceNumber")
    def instance_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "instanceNumber"))

    @instance_number.setter
    def instance_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5db5414b31a2240fd149772256d2a206b50bc3926f1036ca0a86277e7253da0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operation")
    def operation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operation"))

    @operation.setter
    def operation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a1771089e1606ca5ab11521147e07cc28289da5db81850073c2ac53f29bd19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AsPolicyV1ScalingPolicyAction]:
        return typing.cast(typing.Optional[AsPolicyV1ScalingPolicyAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AsPolicyV1ScalingPolicyAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__948cd520e130310f09f8f45fb8f34c5d7ec6e1e6390661adb1ac784107ac1d74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV1.AsPolicyV1ScheduledPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "launch_time": "launchTime",
        "end_time": "endTime",
        "recurrence_type": "recurrenceType",
        "recurrence_value": "recurrenceValue",
        "start_time": "startTime",
    },
)
class AsPolicyV1ScheduledPolicy:
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
        :param launch_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#launch_time AsPolicyV1#launch_time}.
        :param end_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#end_time AsPolicyV1#end_time}.
        :param recurrence_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#recurrence_type AsPolicyV1#recurrence_type}.
        :param recurrence_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#recurrence_value AsPolicyV1#recurrence_value}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#start_time AsPolicyV1#start_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c222afc491c2b3e39d61b609038908726292bfb697c712d312d125ae3e3122c2)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#launch_time AsPolicyV1#launch_time}.'''
        result = self._values.get("launch_time")
        assert result is not None, "Required property 'launch_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#end_time AsPolicyV1#end_time}.'''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recurrence_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#recurrence_type AsPolicyV1#recurrence_type}.'''
        result = self._values.get("recurrence_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recurrence_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#recurrence_value AsPolicyV1#recurrence_value}.'''
        result = self._values.get("recurrence_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_policy_v1#start_time AsPolicyV1#start_time}.'''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsPolicyV1ScheduledPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AsPolicyV1ScheduledPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asPolicyV1.AsPolicyV1ScheduledPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24f7d2b42050200022676cad97136e7629e60e4fad0dee5481b315ba165065a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__272729cf2bf7d53807f72898e7e4ccbec416312eb0059c955bd383813b392f7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="launchTime")
    def launch_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "launchTime"))

    @launch_time.setter
    def launch_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e584973de287dbd0eb83706125efca3e6e88e2117f20f1d70f0b1e33f58afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recurrenceType")
    def recurrence_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recurrenceType"))

    @recurrence_type.setter
    def recurrence_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__686777d68348cf479d9272dc5ff951f9288b661f50558cf241efddf5e7327528)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrenceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recurrenceValue")
    def recurrence_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recurrenceValue"))

    @recurrence_value.setter
    def recurrence_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__081682b6f53c9076834e8c9ffab72b4f0dcde667eda7130e10a42d22e23f13c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrenceValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75b5516cb25c2b7bc6a9cb089e9edc35898c9fff28e18af18f2e806122a217f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AsPolicyV1ScheduledPolicy]:
        return typing.cast(typing.Optional[AsPolicyV1ScheduledPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AsPolicyV1ScheduledPolicy]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b64a1306701b8bf08e4d0ff056d2f3f24b101a58bddef6003d58849bf57575d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AsPolicyV1",
    "AsPolicyV1Config",
    "AsPolicyV1ScalingPolicyAction",
    "AsPolicyV1ScalingPolicyActionOutputReference",
    "AsPolicyV1ScheduledPolicy",
    "AsPolicyV1ScheduledPolicyOutputReference",
]

publication.publish()

def _typecheckingstub__591e0f1c77e71a5dd1844962e54549ce73ef0cca30292daf3a0f8981602c2834(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    scaling_group_id: builtins.str,
    scaling_policy_name: builtins.str,
    scaling_policy_type: builtins.str,
    alarm_id: typing.Optional[builtins.str] = None,
    cool_down_time: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    scaling_policy_action: typing.Optional[typing.Union[AsPolicyV1ScalingPolicyAction, typing.Dict[builtins.str, typing.Any]]] = None,
    scheduled_policy: typing.Optional[typing.Union[AsPolicyV1ScheduledPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7bab287ec81809a489ad4b71b3009f96fed470bd7955b1ae9037bff21fbacaff(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64fd82e51176a8449607a7772408b235e1e6f8e8a1838db9a180bb9e9668f36f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a14b981e630878f04b1a3b5e1b994541297d8e44dfec494cafdd497acf5fbe62(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be123a2ce99e015ea3d1f71bc5dca3b1b4f7e402cb22c47a8af16772771e58da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20493d3b364ded6883bfa51915c14ea40d9c4d20b52f331ceeb325323d3ef351(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ba56b0771055c6dd8e611d475a5c6d4ab623d0419ee7a04b955af46a35113c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aac4b9463530c3649f2bc4b111534aa5b8aafd7d8881f502427911844c6dec6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ca84b89b629beb8443eaed4d7440cc9324ce4f239a89d0072afc3e951c2a29d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0af2f752d29d467d2bf07567af297712f343380a1ee69389d40bf012ecdad28f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scaling_group_id: builtins.str,
    scaling_policy_name: builtins.str,
    scaling_policy_type: builtins.str,
    alarm_id: typing.Optional[builtins.str] = None,
    cool_down_time: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    scaling_policy_action: typing.Optional[typing.Union[AsPolicyV1ScalingPolicyAction, typing.Dict[builtins.str, typing.Any]]] = None,
    scheduled_policy: typing.Optional[typing.Union[AsPolicyV1ScheduledPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd675edbd2d840117e95d492ef8a1a0bdcb9ba699d244fd2c1c4c3a1c3522bc1(
    *,
    instance_number: typing.Optional[jsii.Number] = None,
    operation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e980e7ba920c55c7821f71eca46f2407822c1ac2cb8dc6eb6a67b3a7e7f9ee5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5db5414b31a2240fd149772256d2a206b50bc3926f1036ca0a86277e7253da0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a1771089e1606ca5ab11521147e07cc28289da5db81850073c2ac53f29bd19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__948cd520e130310f09f8f45fb8f34c5d7ec6e1e6390661adb1ac784107ac1d74(
    value: typing.Optional[AsPolicyV1ScalingPolicyAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c222afc491c2b3e39d61b609038908726292bfb697c712d312d125ae3e3122c2(
    *,
    launch_time: builtins.str,
    end_time: typing.Optional[builtins.str] = None,
    recurrence_type: typing.Optional[builtins.str] = None,
    recurrence_value: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f7d2b42050200022676cad97136e7629e60e4fad0dee5481b315ba165065a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__272729cf2bf7d53807f72898e7e4ccbec416312eb0059c955bd383813b392f7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e584973de287dbd0eb83706125efca3e6e88e2117f20f1d70f0b1e33f58afa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686777d68348cf479d9272dc5ff951f9288b661f50558cf241efddf5e7327528(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081682b6f53c9076834e8c9ffab72b4f0dcde667eda7130e10a42d22e23f13c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b5516cb25c2b7bc6a9cb089e9edc35898c9fff28e18af18f2e806122a217f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b64a1306701b8bf08e4d0ff056d2f3f24b101a58bddef6003d58849bf57575d(
    value: typing.Optional[AsPolicyV1ScheduledPolicy],
) -> None:
    """Type checking stubs"""
    pass
