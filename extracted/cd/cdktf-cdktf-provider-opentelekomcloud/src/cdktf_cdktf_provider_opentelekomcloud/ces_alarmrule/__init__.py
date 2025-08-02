r'''
# `opentelekomcloud_ces_alarmrule`

Refer to the Terraform Registry for docs: [`opentelekomcloud_ces_alarmrule`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule).
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


class CesAlarmrule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cesAlarmrule.CesAlarmrule",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule opentelekomcloud_ces_alarmrule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        alarm_name: builtins.str,
        condition: typing.Union["CesAlarmruleCondition", typing.Dict[builtins.str, typing.Any]],
        metric: typing.Union["CesAlarmruleMetric", typing.Dict[builtins.str, typing.Any]],
        alarm_action_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        alarm_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CesAlarmruleAlarmActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        alarm_level: typing.Optional[jsii.Number] = None,
        alarm_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ok_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CesAlarmruleOkActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["CesAlarmruleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule opentelekomcloud_ces_alarmrule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alarm_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_name CesAlarmrule#alarm_name}.
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#condition CesAlarmrule#condition}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#metric CesAlarmrule#metric}
        :param alarm_action_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_action_enabled CesAlarmrule#alarm_action_enabled}.
        :param alarm_actions: alarm_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_actions CesAlarmrule#alarm_actions}
        :param alarm_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_description CesAlarmrule#alarm_description}.
        :param alarm_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_enabled CesAlarmrule#alarm_enabled}.
        :param alarm_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_level CesAlarmrule#alarm_level}.
        :param alarm_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_type CesAlarmrule#alarm_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#id CesAlarmrule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ok_actions: ok_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#ok_actions CesAlarmrule#ok_actions}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#timeouts CesAlarmrule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a555f660d732cb307ae0907003203ff4b469655085280fc4b96acb927d1c77e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CesAlarmruleConfig(
            alarm_name=alarm_name,
            condition=condition,
            metric=metric,
            alarm_action_enabled=alarm_action_enabled,
            alarm_actions=alarm_actions,
            alarm_description=alarm_description,
            alarm_enabled=alarm_enabled,
            alarm_level=alarm_level,
            alarm_type=alarm_type,
            id=id,
            ok_actions=ok_actions,
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
        '''Generates CDKTF code for importing a CesAlarmrule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CesAlarmrule to import.
        :param import_from_id: The id of the existing CesAlarmrule that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CesAlarmrule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f59147cb9e789c881c07519365fcdd988cc5daea20ded223b63619d34a6a37b6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAlarmActions")
    def put_alarm_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CesAlarmruleAlarmActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__189abd1a56c975618652f8320df3a9bae7920e2139b9f82bda94475dadfdf015)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAlarmActions", [value]))

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        *,
        comparison_operator: builtins.str,
        count: jsii.Number,
        filter: builtins.str,
        period: jsii.Number,
        value: jsii.Number,
        alarm_frequency: typing.Optional[jsii.Number] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param comparison_operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#comparison_operator CesAlarmrule#comparison_operator}.
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#count CesAlarmrule#count}.
        :param filter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#filter CesAlarmrule#filter}.
        :param period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#period CesAlarmrule#period}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#value CesAlarmrule#value}.
        :param alarm_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_frequency CesAlarmrule#alarm_frequency}.
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#unit CesAlarmrule#unit}.
        '''
        value_ = CesAlarmruleCondition(
            comparison_operator=comparison_operator,
            count=count,
            filter=filter,
            period=period,
            value=value,
            alarm_frequency=alarm_frequency,
            unit=unit,
        )

        return typing.cast(None, jsii.invoke(self, "putCondition", [value_]))

    @jsii.member(jsii_name="putMetric")
    def put_metric(
        self,
        *,
        metric_name: builtins.str,
        namespace: builtins.str,
        dimensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CesAlarmruleMetricDimensions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param metric_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#metric_name CesAlarmrule#metric_name}.
        :param namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#namespace CesAlarmrule#namespace}.
        :param dimensions: dimensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#dimensions CesAlarmrule#dimensions}
        '''
        value = CesAlarmruleMetric(
            metric_name=metric_name, namespace=namespace, dimensions=dimensions
        )

        return typing.cast(None, jsii.invoke(self, "putMetric", [value]))

    @jsii.member(jsii_name="putOkActions")
    def put_ok_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CesAlarmruleOkActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec1a6ff1fc46dfc6530b02f4c9cc0f974b3f9e3907ea33e192d26eac002feed6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOkActions", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#create CesAlarmrule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#delete CesAlarmrule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#update CesAlarmrule#update}.
        '''
        value = CesAlarmruleTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAlarmActionEnabled")
    def reset_alarm_action_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlarmActionEnabled", []))

    @jsii.member(jsii_name="resetAlarmActions")
    def reset_alarm_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlarmActions", []))

    @jsii.member(jsii_name="resetAlarmDescription")
    def reset_alarm_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlarmDescription", []))

    @jsii.member(jsii_name="resetAlarmEnabled")
    def reset_alarm_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlarmEnabled", []))

    @jsii.member(jsii_name="resetAlarmLevel")
    def reset_alarm_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlarmLevel", []))

    @jsii.member(jsii_name="resetAlarmType")
    def reset_alarm_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlarmType", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOkActions")
    def reset_ok_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOkActions", []))

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
    @jsii.member(jsii_name="alarmActions")
    def alarm_actions(self) -> "CesAlarmruleAlarmActionsList":
        return typing.cast("CesAlarmruleAlarmActionsList", jsii.get(self, "alarmActions"))

    @builtins.property
    @jsii.member(jsii_name="alarmState")
    def alarm_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alarmState"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> "CesAlarmruleConditionOutputReference":
        return typing.cast("CesAlarmruleConditionOutputReference", jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="metric")
    def metric(self) -> "CesAlarmruleMetricOutputReference":
        return typing.cast("CesAlarmruleMetricOutputReference", jsii.get(self, "metric"))

    @builtins.property
    @jsii.member(jsii_name="okActions")
    def ok_actions(self) -> "CesAlarmruleOkActionsList":
        return typing.cast("CesAlarmruleOkActionsList", jsii.get(self, "okActions"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CesAlarmruleTimeoutsOutputReference":
        return typing.cast("CesAlarmruleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="alarmActionEnabledInput")
    def alarm_action_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "alarmActionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="alarmActionsInput")
    def alarm_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CesAlarmruleAlarmActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CesAlarmruleAlarmActions"]]], jsii.get(self, "alarmActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="alarmDescriptionInput")
    def alarm_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alarmDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="alarmEnabledInput")
    def alarm_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "alarmEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="alarmLevelInput")
    def alarm_level_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "alarmLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="alarmNameInput")
    def alarm_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alarmNameInput"))

    @builtins.property
    @jsii.member(jsii_name="alarmTypeInput")
    def alarm_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alarmTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional["CesAlarmruleCondition"]:
        return typing.cast(typing.Optional["CesAlarmruleCondition"], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="metricInput")
    def metric_input(self) -> typing.Optional["CesAlarmruleMetric"]:
        return typing.cast(typing.Optional["CesAlarmruleMetric"], jsii.get(self, "metricInput"))

    @builtins.property
    @jsii.member(jsii_name="okActionsInput")
    def ok_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CesAlarmruleOkActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CesAlarmruleOkActions"]]], jsii.get(self, "okActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CesAlarmruleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CesAlarmruleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="alarmActionEnabled")
    def alarm_action_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "alarmActionEnabled"))

    @alarm_action_enabled.setter
    def alarm_action_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4598ec06f4edf942f5945a9cddd83e6e633a7437c12f1ed2c2001ec8a433505d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmActionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alarmDescription")
    def alarm_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alarmDescription"))

    @alarm_description.setter
    def alarm_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c5b08f3e090fd5a0c139085b7f25f05476b9f640b0cad9982d1d4cb15038c79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alarmEnabled")
    def alarm_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "alarmEnabled"))

    @alarm_enabled.setter
    def alarm_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a07468457e751cf3dfa3853828e67e46dd62d5588e69a4834c4a664eb7f64041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alarmLevel")
    def alarm_level(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "alarmLevel"))

    @alarm_level.setter
    def alarm_level(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3027fecea2d154848763093b493d38e415cc609c113e5e430d8bbd5fea3cb691)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alarmName"))

    @alarm_name.setter
    def alarm_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a02ccc1a0312cc75434a8281e98ef55e39b33279d4b231bace0badc40bdbe302)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alarmType")
    def alarm_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alarmType"))

    @alarm_type.setter
    def alarm_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec873839e9ab8490cb2fae1e090f8f819b59421894364cc721cc8c8b5fd11242)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8493c4b6d0baf0909670619f1973c82f91c5d75e26cb6fe2b368ff988cf05a2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cesAlarmrule.CesAlarmruleAlarmActions",
    jsii_struct_bases=[],
    name_mapping={"notification_list": "notificationList", "type": "type"},
)
class CesAlarmruleAlarmActions:
    def __init__(
        self,
        *,
        notification_list: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param notification_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#notification_list CesAlarmrule#notification_list}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#type CesAlarmrule#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__257b150c4ba5499c3749da4aac01fa9a5cc0d9e425b51cb7275cde608dfd2d49)
            check_type(argname="argument notification_list", value=notification_list, expected_type=type_hints["notification_list"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "notification_list": notification_list,
            "type": type,
        }

    @builtins.property
    def notification_list(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#notification_list CesAlarmrule#notification_list}.'''
        result = self._values.get("notification_list")
        assert result is not None, "Required property 'notification_list' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#type CesAlarmrule#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CesAlarmruleAlarmActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CesAlarmruleAlarmActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cesAlarmrule.CesAlarmruleAlarmActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e607a22fb5205c29610c2ec6862e9b6454af9276082eb37142c6eb6861e5a4ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CesAlarmruleAlarmActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfb9dd0d43c1f4609ddf5fc8fd289d5eb4862e378988e993074316d51bef6abd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CesAlarmruleAlarmActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__114263b99049820c1e1ef705f36da85999b5c95a925089192b66c944e4e480e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74ab291a456cb84c725dc53a45962c0115fe5623f94945e1fefdad1c937d47e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86151452013abf8c22966d852ab86673a3a6b408493586caa517eb6749b73b1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CesAlarmruleAlarmActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CesAlarmruleAlarmActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CesAlarmruleAlarmActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4feb752e433c01c964fcb510f5e2befadf9191f69f3bf7fb2d39f3d918dfee6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CesAlarmruleAlarmActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cesAlarmrule.CesAlarmruleAlarmActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d98515a87c5868edc9c7f1e3e88c75a7ff2ffd67c7c479b9dd576b88082416a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="notificationListInput")
    def notification_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notificationListInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationList")
    def notification_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notificationList"))

    @notification_list.setter
    def notification_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c61ee375e12cbf93b2d94acd6e250c76fd447440a1259dc5e5ec94c479e2e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa5b72ba80cd008f5973d9c8873665ff07827ca175c60685e74c0826eabe8b5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CesAlarmruleAlarmActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CesAlarmruleAlarmActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CesAlarmruleAlarmActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb75702f00861d7fef0f4ce71827eee0b31dccec263fd050db8a96139693a9c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cesAlarmrule.CesAlarmruleCondition",
    jsii_struct_bases=[],
    name_mapping={
        "comparison_operator": "comparisonOperator",
        "count": "count",
        "filter": "filter",
        "period": "period",
        "value": "value",
        "alarm_frequency": "alarmFrequency",
        "unit": "unit",
    },
)
class CesAlarmruleCondition:
    def __init__(
        self,
        *,
        comparison_operator: builtins.str,
        count: jsii.Number,
        filter: builtins.str,
        period: jsii.Number,
        value: jsii.Number,
        alarm_frequency: typing.Optional[jsii.Number] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param comparison_operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#comparison_operator CesAlarmrule#comparison_operator}.
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#count CesAlarmrule#count}.
        :param filter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#filter CesAlarmrule#filter}.
        :param period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#period CesAlarmrule#period}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#value CesAlarmrule#value}.
        :param alarm_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_frequency CesAlarmrule#alarm_frequency}.
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#unit CesAlarmrule#unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0299c17c09638f67ba8176b0369c4e0400b295f757cfc007031fe0a632c8673c)
            check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument alarm_frequency", value=alarm_frequency, expected_type=type_hints["alarm_frequency"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison_operator": comparison_operator,
            "count": count,
            "filter": filter,
            "period": period,
            "value": value,
        }
        if alarm_frequency is not None:
            self._values["alarm_frequency"] = alarm_frequency
        if unit is not None:
            self._values["unit"] = unit

    @builtins.property
    def comparison_operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#comparison_operator CesAlarmrule#comparison_operator}.'''
        result = self._values.get("comparison_operator")
        assert result is not None, "Required property 'comparison_operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#count CesAlarmrule#count}.'''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def filter(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#filter CesAlarmrule#filter}.'''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def period(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#period CesAlarmrule#period}.'''
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#value CesAlarmrule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def alarm_frequency(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_frequency CesAlarmrule#alarm_frequency}.'''
        result = self._values.get("alarm_frequency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#unit CesAlarmrule#unit}.'''
        result = self._values.get("unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CesAlarmruleCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CesAlarmruleConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cesAlarmrule.CesAlarmruleConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fbb8a2cac10f10e936cb44b61d8d9e7b472312c8c8a282f3a5e2691b34814eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAlarmFrequency")
    def reset_alarm_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlarmFrequency", []))

    @jsii.member(jsii_name="resetUnit")
    def reset_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnit", []))

    @builtins.property
    @jsii.member(jsii_name="alarmFrequencyInput")
    def alarm_frequency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "alarmFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="comparisonOperatorInput")
    def comparison_operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonOperatorInput"))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="periodInput")
    def period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "periodInput"))

    @builtins.property
    @jsii.member(jsii_name="unitInput")
    def unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="alarmFrequency")
    def alarm_frequency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "alarmFrequency"))

    @alarm_frequency.setter
    def alarm_frequency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9deb20bad35154455fbdf3e06f7189ac6e4533b64e2efee76089489144b21a14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmFrequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comparisonOperator")
    def comparison_operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparisonOperator"))

    @comparison_operator.setter
    def comparison_operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f299aac6ee595324ffd4f1af8c468ad1101bdae1b35cc9feac2f3d46eec6cce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparisonOperator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3c351089cbc16f06b97302a8e3ba8dd3b58100d373df3c30d51777e76924f99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0cbfb23850a718f12e2f0a10eeb08a830cdbfe67c7474c45b3533f6914274b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "period"))

    @period.setter
    def period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a804b12a0586c0cfdfb6e9d7bcba6ae16689ec43ce632f59c2161c96fff1fc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "period", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unit"))

    @unit.setter
    def unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__499ccbedaf1deaae742141e9699b08c5ef4f80165f00201d199c23b4de9846d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325bcf644140c5423a7481dec2f2744d2146fa8e90ab7f3dcdeeef84360853bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CesAlarmruleCondition]:
        return typing.cast(typing.Optional[CesAlarmruleCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CesAlarmruleCondition]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31e6f588e5cef3d5d251ac6611cf9d184ee69d1f0c0d20edccf191ae3cc7150d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cesAlarmrule.CesAlarmruleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "alarm_name": "alarmName",
        "condition": "condition",
        "metric": "metric",
        "alarm_action_enabled": "alarmActionEnabled",
        "alarm_actions": "alarmActions",
        "alarm_description": "alarmDescription",
        "alarm_enabled": "alarmEnabled",
        "alarm_level": "alarmLevel",
        "alarm_type": "alarmType",
        "id": "id",
        "ok_actions": "okActions",
        "timeouts": "timeouts",
    },
)
class CesAlarmruleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        alarm_name: builtins.str,
        condition: typing.Union[CesAlarmruleCondition, typing.Dict[builtins.str, typing.Any]],
        metric: typing.Union["CesAlarmruleMetric", typing.Dict[builtins.str, typing.Any]],
        alarm_action_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        alarm_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CesAlarmruleAlarmActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        alarm_level: typing.Optional[jsii.Number] = None,
        alarm_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ok_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CesAlarmruleOkActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["CesAlarmruleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param alarm_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_name CesAlarmrule#alarm_name}.
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#condition CesAlarmrule#condition}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#metric CesAlarmrule#metric}
        :param alarm_action_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_action_enabled CesAlarmrule#alarm_action_enabled}.
        :param alarm_actions: alarm_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_actions CesAlarmrule#alarm_actions}
        :param alarm_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_description CesAlarmrule#alarm_description}.
        :param alarm_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_enabled CesAlarmrule#alarm_enabled}.
        :param alarm_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_level CesAlarmrule#alarm_level}.
        :param alarm_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_type CesAlarmrule#alarm_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#id CesAlarmrule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ok_actions: ok_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#ok_actions CesAlarmrule#ok_actions}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#timeouts CesAlarmrule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(condition, dict):
            condition = CesAlarmruleCondition(**condition)
        if isinstance(metric, dict):
            metric = CesAlarmruleMetric(**metric)
        if isinstance(timeouts, dict):
            timeouts = CesAlarmruleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__987062ce38215b8d754d40a380a54aaaa74d7efbd973353cfad1b0215d356ea9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
            check_type(argname="argument alarm_action_enabled", value=alarm_action_enabled, expected_type=type_hints["alarm_action_enabled"])
            check_type(argname="argument alarm_actions", value=alarm_actions, expected_type=type_hints["alarm_actions"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_enabled", value=alarm_enabled, expected_type=type_hints["alarm_enabled"])
            check_type(argname="argument alarm_level", value=alarm_level, expected_type=type_hints["alarm_level"])
            check_type(argname="argument alarm_type", value=alarm_type, expected_type=type_hints["alarm_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ok_actions", value=ok_actions, expected_type=type_hints["ok_actions"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alarm_name": alarm_name,
            "condition": condition,
            "metric": metric,
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
        if alarm_action_enabled is not None:
            self._values["alarm_action_enabled"] = alarm_action_enabled
        if alarm_actions is not None:
            self._values["alarm_actions"] = alarm_actions
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_enabled is not None:
            self._values["alarm_enabled"] = alarm_enabled
        if alarm_level is not None:
            self._values["alarm_level"] = alarm_level
        if alarm_type is not None:
            self._values["alarm_type"] = alarm_type
        if id is not None:
            self._values["id"] = id
        if ok_actions is not None:
            self._values["ok_actions"] = ok_actions
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
    def alarm_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_name CesAlarmrule#alarm_name}.'''
        result = self._values.get("alarm_name")
        assert result is not None, "Required property 'alarm_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition(self) -> CesAlarmruleCondition:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#condition CesAlarmrule#condition}
        '''
        result = self._values.get("condition")
        assert result is not None, "Required property 'condition' is missing"
        return typing.cast(CesAlarmruleCondition, result)

    @builtins.property
    def metric(self) -> "CesAlarmruleMetric":
        '''metric block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#metric CesAlarmrule#metric}
        '''
        result = self._values.get("metric")
        assert result is not None, "Required property 'metric' is missing"
        return typing.cast("CesAlarmruleMetric", result)

    @builtins.property
    def alarm_action_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_action_enabled CesAlarmrule#alarm_action_enabled}.'''
        result = self._values.get("alarm_action_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def alarm_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CesAlarmruleAlarmActions]]]:
        '''alarm_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_actions CesAlarmrule#alarm_actions}
        '''
        result = self._values.get("alarm_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CesAlarmruleAlarmActions]]], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_description CesAlarmrule#alarm_description}.'''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_enabled CesAlarmrule#alarm_enabled}.'''
        result = self._values.get("alarm_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def alarm_level(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_level CesAlarmrule#alarm_level}.'''
        result = self._values.get("alarm_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def alarm_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#alarm_type CesAlarmrule#alarm_type}.'''
        result = self._values.get("alarm_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#id CesAlarmrule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ok_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CesAlarmruleOkActions"]]]:
        '''ok_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#ok_actions CesAlarmrule#ok_actions}
        '''
        result = self._values.get("ok_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CesAlarmruleOkActions"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CesAlarmruleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#timeouts CesAlarmrule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CesAlarmruleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CesAlarmruleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cesAlarmrule.CesAlarmruleMetric",
    jsii_struct_bases=[],
    name_mapping={
        "metric_name": "metricName",
        "namespace": "namespace",
        "dimensions": "dimensions",
    },
)
class CesAlarmruleMetric:
    def __init__(
        self,
        *,
        metric_name: builtins.str,
        namespace: builtins.str,
        dimensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CesAlarmruleMetricDimensions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param metric_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#metric_name CesAlarmrule#metric_name}.
        :param namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#namespace CesAlarmrule#namespace}.
        :param dimensions: dimensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#dimensions CesAlarmrule#dimensions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c388e6179d065874cca48762f38e87dc9d9c464179ea80fe451bc20418f4be3)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_name": metric_name,
            "namespace": namespace,
        }
        if dimensions is not None:
            self._values["dimensions"] = dimensions

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#metric_name CesAlarmrule#metric_name}.'''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#namespace CesAlarmrule#namespace}.'''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dimensions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CesAlarmruleMetricDimensions"]]]:
        '''dimensions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#dimensions CesAlarmrule#dimensions}
        '''
        result = self._values.get("dimensions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CesAlarmruleMetricDimensions"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CesAlarmruleMetric(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cesAlarmrule.CesAlarmruleMetricDimensions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class CesAlarmruleMetricDimensions:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#name CesAlarmrule#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#value CesAlarmrule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__727a292c01d16ed6ca60a67e760090e6bf5c165da1528d79e9239b002fa17a9c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#name CesAlarmrule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#value CesAlarmrule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CesAlarmruleMetricDimensions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CesAlarmruleMetricDimensionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cesAlarmrule.CesAlarmruleMetricDimensionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ca5e6f3320fc86614d5d52439a8f71e502599c48eebdc6003f59b890b6615df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CesAlarmruleMetricDimensionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3991b84761ce6967508132269df138ce2589c5935f39b372192f8443c94b55d0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CesAlarmruleMetricDimensionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9826e5741125e4b0aaabbed4eb0e7d6d32d347492856b01230960e20f0473c46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e02b649c1d3f89faf6a91b32c163e58649cf0de20bc178784cc808b6d079cd1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dce3227b5fc39b3c3bf6ca27b998b8f96c48f395d97c62821cc32eafb3dd5b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CesAlarmruleMetricDimensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CesAlarmruleMetricDimensions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CesAlarmruleMetricDimensions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ccd4c03516f2e6eec1e9ac542b9b977d8956d55ad378463ad5ec2c8c1e3d3b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CesAlarmruleMetricDimensionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cesAlarmrule.CesAlarmruleMetricDimensionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75e68bf7266033663750b0ae8ab09ff60a6180409be6de83a9a5dfba2dcb72cf)
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
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eb13892d38f927c066e906dad0c6a3f74f9f4214bd5c0441c0848c78bf4e717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4caf6345dfd39055d7077893b22ff65f8a204d3d2971c98b1d2956a4ef3bfc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CesAlarmruleMetricDimensions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CesAlarmruleMetricDimensions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CesAlarmruleMetricDimensions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__025ca48c24e58cca5b9a9b6b3e81c6b4005608289ac4877483b2345ddcdf73b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CesAlarmruleMetricOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cesAlarmrule.CesAlarmruleMetricOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4038b1e43311db6a003746677447ab19e329b2843f36bd7d925ecbed8531b92b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDimensions")
    def put_dimensions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CesAlarmruleMetricDimensions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ffd7f9131703b94328f8f70c0e011b82fa835059da3c9e2cb8d926880c72d78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDimensions", [value]))

    @jsii.member(jsii_name="resetDimensions")
    def reset_dimensions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDimensions", []))

    @builtins.property
    @jsii.member(jsii_name="dimensions")
    def dimensions(self) -> CesAlarmruleMetricDimensionsList:
        return typing.cast(CesAlarmruleMetricDimensionsList, jsii.get(self, "dimensions"))

    @builtins.property
    @jsii.member(jsii_name="dimensionsInput")
    def dimensions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CesAlarmruleMetricDimensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CesAlarmruleMetricDimensions]]], jsii.get(self, "dimensionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricNameInput")
    def metric_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricNameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricName"))

    @metric_name.setter
    def metric_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a5db1d56af57dfb701cff9b01cefc9086dbf9579008af5e3b0af6bd75aadbd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04db6f90bf7fc1ee0409200610223df8c1b876e69e84a2a0dc958e281eee1272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CesAlarmruleMetric]:
        return typing.cast(typing.Optional[CesAlarmruleMetric], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CesAlarmruleMetric]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f5cd7dfc5e1c2af6b982c601ea977aea377c4f25b1ed39af7b43dfb0301edd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cesAlarmrule.CesAlarmruleOkActions",
    jsii_struct_bases=[],
    name_mapping={"notification_list": "notificationList", "type": "type"},
)
class CesAlarmruleOkActions:
    def __init__(
        self,
        *,
        notification_list: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param notification_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#notification_list CesAlarmrule#notification_list}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#type CesAlarmrule#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2682659244fc1a06ee3f972f5d22f9200c4ca8af9d8ba80188bd55729903dd8c)
            check_type(argname="argument notification_list", value=notification_list, expected_type=type_hints["notification_list"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "notification_list": notification_list,
            "type": type,
        }

    @builtins.property
    def notification_list(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#notification_list CesAlarmrule#notification_list}.'''
        result = self._values.get("notification_list")
        assert result is not None, "Required property 'notification_list' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#type CesAlarmrule#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CesAlarmruleOkActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CesAlarmruleOkActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cesAlarmrule.CesAlarmruleOkActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d885d9ed218f701f8ebd2484ddcd9a1cf84a69d4b4793b3297774ddae31217f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CesAlarmruleOkActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9922bb4a5387e1fdeb16679d4fbaf1cfe46e531111173766e71809a72ddcc7e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CesAlarmruleOkActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd42d763e0a9cc1b486a935f91063daa7831f0fc997749b326928bed437f37f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d4833cd4f8dbdf70a2c01a864c73b00e83ca0792202a45a6f60e4a7c95312d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44d737d163e658d79ca09af62a3a3a23a5c924571f9fe0794669f76fdb64ee0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CesAlarmruleOkActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CesAlarmruleOkActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CesAlarmruleOkActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__030110e578f0e259afe09eb5aea534049be76ccb6583629160c1593e928a0a6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CesAlarmruleOkActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cesAlarmrule.CesAlarmruleOkActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cc510cfabdcb734006aad486e2b3aff1fcb7e32cd1785e18c80a93e205fea55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="notificationListInput")
    def notification_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notificationListInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationList")
    def notification_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notificationList"))

    @notification_list.setter
    def notification_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db602aeca2cedd69bf343e5cdef5d248dd2848241af8dde56e89d93d122939c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5884484d5c2a67ff1830c739f0f146ab1f5740055ae59625ab928a78a28446)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CesAlarmruleOkActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CesAlarmruleOkActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CesAlarmruleOkActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac6d5851f6a9c5de5b2da7c3d7ad4a83949d5ac63604ca84113d5b142ffaa811)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cesAlarmrule.CesAlarmruleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CesAlarmruleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#create CesAlarmrule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#delete CesAlarmrule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#update CesAlarmrule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b204629b245cd8be16bb11836fa517497efaaae4a99a51f900e0203fd150e17)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#create CesAlarmrule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#delete CesAlarmrule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_alarmrule#update CesAlarmrule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CesAlarmruleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CesAlarmruleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cesAlarmrule.CesAlarmruleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f5365c3e99df5a8a6ae7dff41fec3b9606ac037543b446642cbe7a5775d7364)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bec970fd585b7234c0c55f368678032fbdd294740a8adbc440fe4439c735cbed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e38555d9862a58e9f62c76b56b379f881191ddaa5d90610ad6399b2646a1e38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__561be5637096491f858a74b7b56680fdf17f6b0dac33e4d5a8d3c15004bb4f28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CesAlarmruleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CesAlarmruleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CesAlarmruleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4b6179992a382ad0d732684df92a212254001f027df586f49d3861b500b137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CesAlarmrule",
    "CesAlarmruleAlarmActions",
    "CesAlarmruleAlarmActionsList",
    "CesAlarmruleAlarmActionsOutputReference",
    "CesAlarmruleCondition",
    "CesAlarmruleConditionOutputReference",
    "CesAlarmruleConfig",
    "CesAlarmruleMetric",
    "CesAlarmruleMetricDimensions",
    "CesAlarmruleMetricDimensionsList",
    "CesAlarmruleMetricDimensionsOutputReference",
    "CesAlarmruleMetricOutputReference",
    "CesAlarmruleOkActions",
    "CesAlarmruleOkActionsList",
    "CesAlarmruleOkActionsOutputReference",
    "CesAlarmruleTimeouts",
    "CesAlarmruleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7a555f660d732cb307ae0907003203ff4b469655085280fc4b96acb927d1c77e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    alarm_name: builtins.str,
    condition: typing.Union[CesAlarmruleCondition, typing.Dict[builtins.str, typing.Any]],
    metric: typing.Union[CesAlarmruleMetric, typing.Dict[builtins.str, typing.Any]],
    alarm_action_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    alarm_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CesAlarmruleAlarmActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    alarm_level: typing.Optional[jsii.Number] = None,
    alarm_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ok_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CesAlarmruleOkActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[CesAlarmruleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f59147cb9e789c881c07519365fcdd988cc5daea20ded223b63619d34a6a37b6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__189abd1a56c975618652f8320df3a9bae7920e2139b9f82bda94475dadfdf015(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CesAlarmruleAlarmActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1a6ff1fc46dfc6530b02f4c9cc0f974b3f9e3907ea33e192d26eac002feed6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CesAlarmruleOkActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4598ec06f4edf942f5945a9cddd83e6e633a7437c12f1ed2c2001ec8a433505d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c5b08f3e090fd5a0c139085b7f25f05476b9f640b0cad9982d1d4cb15038c79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a07468457e751cf3dfa3853828e67e46dd62d5588e69a4834c4a664eb7f64041(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3027fecea2d154848763093b493d38e415cc609c113e5e430d8bbd5fea3cb691(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a02ccc1a0312cc75434a8281e98ef55e39b33279d4b231bace0badc40bdbe302(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec873839e9ab8490cb2fae1e090f8f819b59421894364cc721cc8c8b5fd11242(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8493c4b6d0baf0909670619f1973c82f91c5d75e26cb6fe2b368ff988cf05a2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257b150c4ba5499c3749da4aac01fa9a5cc0d9e425b51cb7275cde608dfd2d49(
    *,
    notification_list: typing.Sequence[builtins.str],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e607a22fb5205c29610c2ec6862e9b6454af9276082eb37142c6eb6861e5a4ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfb9dd0d43c1f4609ddf5fc8fd289d5eb4862e378988e993074316d51bef6abd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__114263b99049820c1e1ef705f36da85999b5c95a925089192b66c944e4e480e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74ab291a456cb84c725dc53a45962c0115fe5623f94945e1fefdad1c937d47e3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86151452013abf8c22966d852ab86673a3a6b408493586caa517eb6749b73b1c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4feb752e433c01c964fcb510f5e2befadf9191f69f3bf7fb2d39f3d918dfee6a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CesAlarmruleAlarmActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d98515a87c5868edc9c7f1e3e88c75a7ff2ffd67c7c479b9dd576b88082416a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c61ee375e12cbf93b2d94acd6e250c76fd447440a1259dc5e5ec94c479e2e9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa5b72ba80cd008f5973d9c8873665ff07827ca175c60685e74c0826eabe8b5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb75702f00861d7fef0f4ce71827eee0b31dccec263fd050db8a96139693a9c8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CesAlarmruleAlarmActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0299c17c09638f67ba8176b0369c4e0400b295f757cfc007031fe0a632c8673c(
    *,
    comparison_operator: builtins.str,
    count: jsii.Number,
    filter: builtins.str,
    period: jsii.Number,
    value: jsii.Number,
    alarm_frequency: typing.Optional[jsii.Number] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fbb8a2cac10f10e936cb44b61d8d9e7b472312c8c8a282f3a5e2691b34814eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9deb20bad35154455fbdf3e06f7189ac6e4533b64e2efee76089489144b21a14(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f299aac6ee595324ffd4f1af8c468ad1101bdae1b35cc9feac2f3d46eec6cce3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c351089cbc16f06b97302a8e3ba8dd3b58100d373df3c30d51777e76924f99(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0cbfb23850a718f12e2f0a10eeb08a830cdbfe67c7474c45b3533f6914274b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a804b12a0586c0cfdfb6e9d7bcba6ae16689ec43ce632f59c2161c96fff1fc5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__499ccbedaf1deaae742141e9699b08c5ef4f80165f00201d199c23b4de9846d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325bcf644140c5423a7481dec2f2744d2146fa8e90ab7f3dcdeeef84360853bd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e6f588e5cef3d5d251ac6611cf9d184ee69d1f0c0d20edccf191ae3cc7150d(
    value: typing.Optional[CesAlarmruleCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__987062ce38215b8d754d40a380a54aaaa74d7efbd973353cfad1b0215d356ea9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    alarm_name: builtins.str,
    condition: typing.Union[CesAlarmruleCondition, typing.Dict[builtins.str, typing.Any]],
    metric: typing.Union[CesAlarmruleMetric, typing.Dict[builtins.str, typing.Any]],
    alarm_action_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    alarm_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CesAlarmruleAlarmActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    alarm_level: typing.Optional[jsii.Number] = None,
    alarm_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ok_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CesAlarmruleOkActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[CesAlarmruleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c388e6179d065874cca48762f38e87dc9d9c464179ea80fe451bc20418f4be3(
    *,
    metric_name: builtins.str,
    namespace: builtins.str,
    dimensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CesAlarmruleMetricDimensions, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__727a292c01d16ed6ca60a67e760090e6bf5c165da1528d79e9239b002fa17a9c(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca5e6f3320fc86614d5d52439a8f71e502599c48eebdc6003f59b890b6615df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3991b84761ce6967508132269df138ce2589c5935f39b372192f8443c94b55d0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9826e5741125e4b0aaabbed4eb0e7d6d32d347492856b01230960e20f0473c46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e02b649c1d3f89faf6a91b32c163e58649cf0de20bc178784cc808b6d079cd1e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dce3227b5fc39b3c3bf6ca27b998b8f96c48f395d97c62821cc32eafb3dd5b3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ccd4c03516f2e6eec1e9ac542b9b977d8956d55ad378463ad5ec2c8c1e3d3b7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CesAlarmruleMetricDimensions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e68bf7266033663750b0ae8ab09ff60a6180409be6de83a9a5dfba2dcb72cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eb13892d38f927c066e906dad0c6a3f74f9f4214bd5c0441c0848c78bf4e717(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4caf6345dfd39055d7077893b22ff65f8a204d3d2971c98b1d2956a4ef3bfc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025ca48c24e58cca5b9a9b6b3e81c6b4005608289ac4877483b2345ddcdf73b7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CesAlarmruleMetricDimensions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4038b1e43311db6a003746677447ab19e329b2843f36bd7d925ecbed8531b92b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ffd7f9131703b94328f8f70c0e011b82fa835059da3c9e2cb8d926880c72d78(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CesAlarmruleMetricDimensions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5db1d56af57dfb701cff9b01cefc9086dbf9579008af5e3b0af6bd75aadbd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04db6f90bf7fc1ee0409200610223df8c1b876e69e84a2a0dc958e281eee1272(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f5cd7dfc5e1c2af6b982c601ea977aea377c4f25b1ed39af7b43dfb0301edd8(
    value: typing.Optional[CesAlarmruleMetric],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2682659244fc1a06ee3f972f5d22f9200c4ca8af9d8ba80188bd55729903dd8c(
    *,
    notification_list: typing.Sequence[builtins.str],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d885d9ed218f701f8ebd2484ddcd9a1cf84a69d4b4793b3297774ddae31217f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9922bb4a5387e1fdeb16679d4fbaf1cfe46e531111173766e71809a72ddcc7e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd42d763e0a9cc1b486a935f91063daa7831f0fc997749b326928bed437f37f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d4833cd4f8dbdf70a2c01a864c73b00e83ca0792202a45a6f60e4a7c95312d2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44d737d163e658d79ca09af62a3a3a23a5c924571f9fe0794669f76fdb64ee0c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030110e578f0e259afe09eb5aea534049be76ccb6583629160c1593e928a0a6c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CesAlarmruleOkActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc510cfabdcb734006aad486e2b3aff1fcb7e32cd1785e18c80a93e205fea55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db602aeca2cedd69bf343e5cdef5d248dd2848241af8dde56e89d93d122939c9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5884484d5c2a67ff1830c739f0f146ab1f5740055ae59625ab928a78a28446(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6d5851f6a9c5de5b2da7c3d7ad4a83949d5ac63604ca84113d5b142ffaa811(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CesAlarmruleOkActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b204629b245cd8be16bb11836fa517497efaaae4a99a51f900e0203fd150e17(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5365c3e99df5a8a6ae7dff41fec3b9606ac037543b446642cbe7a5775d7364(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec970fd585b7234c0c55f368678032fbdd294740a8adbc440fe4439c735cbed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e38555d9862a58e9f62c76b56b379f881191ddaa5d90610ad6399b2646a1e38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__561be5637096491f858a74b7b56680fdf17f6b0dac33e4d5a8d3c15004bb4f28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4b6179992a382ad0d732684df92a212254001f027df586f49d3861b500b137(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CesAlarmruleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
