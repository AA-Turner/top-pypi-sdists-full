r'''
# `data_newrelic_service_level_alert_helper`

Refer to the Terraform Registry for docs: [`data_newrelic_service_level_alert_helper`](https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper).
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


class DataNewrelicServiceLevelAlertHelper(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.dataNewrelicServiceLevelAlertHelper.DataNewrelicServiceLevelAlertHelper",
):
    '''Represents a {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper newrelic_service_level_alert_helper}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        alert_type: builtins.str,
        sli_guid: builtins.str,
        slo_period: jsii.Number,
        slo_target: jsii.Number,
        custom_evaluation_period: typing.Optional[jsii.Number] = None,
        custom_tolerated_budget_consumption: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        is_bad_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper newrelic_service_level_alert_helper} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alert_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#alert_type DataNewrelicServiceLevelAlertHelper#alert_type}.
        :param sli_guid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#sli_guid DataNewrelicServiceLevelAlertHelper#sli_guid}.
        :param slo_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#slo_period DataNewrelicServiceLevelAlertHelper#slo_period}.
        :param slo_target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#slo_target DataNewrelicServiceLevelAlertHelper#slo_target}.
        :param custom_evaluation_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#custom_evaluation_period DataNewrelicServiceLevelAlertHelper#custom_evaluation_period}.
        :param custom_tolerated_budget_consumption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#custom_tolerated_budget_consumption DataNewrelicServiceLevelAlertHelper#custom_tolerated_budget_consumption}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#id DataNewrelicServiceLevelAlertHelper#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_bad_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#is_bad_events DataNewrelicServiceLevelAlertHelper#is_bad_events}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3805ecda0dc357f78cf8f305286f7ad05134b8b9e5fb3aecddd1f8470fb6b28c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataNewrelicServiceLevelAlertHelperConfig(
            alert_type=alert_type,
            sli_guid=sli_guid,
            slo_period=slo_period,
            slo_target=slo_target,
            custom_evaluation_period=custom_evaluation_period,
            custom_tolerated_budget_consumption=custom_tolerated_budget_consumption,
            id=id,
            is_bad_events=is_bad_events,
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
        '''Generates CDKTF code for importing a DataNewrelicServiceLevelAlertHelper resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataNewrelicServiceLevelAlertHelper to import.
        :param import_from_id: The id of the existing DataNewrelicServiceLevelAlertHelper that should be imported. Refer to the {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataNewrelicServiceLevelAlertHelper to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54858f1576a472fdcbef37969a11573f9b41fe9b2e4d4c63b6f73cffbaf3c87b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetCustomEvaluationPeriod")
    def reset_custom_evaluation_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomEvaluationPeriod", []))

    @jsii.member(jsii_name="resetCustomToleratedBudgetConsumption")
    def reset_custom_tolerated_budget_consumption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomToleratedBudgetConsumption", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsBadEvents")
    def reset_is_bad_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsBadEvents", []))

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
    @jsii.member(jsii_name="evaluationPeriod")
    def evaluation_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "evaluationPeriod"))

    @builtins.property
    @jsii.member(jsii_name="nrql")
    def nrql(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nrql"))

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threshold"))

    @builtins.property
    @jsii.member(jsii_name="toleratedBudgetConsumption")
    def tolerated_budget_consumption(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "toleratedBudgetConsumption"))

    @builtins.property
    @jsii.member(jsii_name="alertTypeInput")
    def alert_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alertTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="customEvaluationPeriodInput")
    def custom_evaluation_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "customEvaluationPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="customToleratedBudgetConsumptionInput")
    def custom_tolerated_budget_consumption_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "customToleratedBudgetConsumptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isBadEventsInput")
    def is_bad_events_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isBadEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="sliGuidInput")
    def sli_guid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sliGuidInput"))

    @builtins.property
    @jsii.member(jsii_name="sloPeriodInput")
    def slo_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sloPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="sloTargetInput")
    def slo_target_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sloTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="alertType")
    def alert_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alertType"))

    @alert_type.setter
    def alert_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__effc6a28384edb1a394863fee9ff6d0f39c31e40aa377fc5a65f03675252b9be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alertType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customEvaluationPeriod")
    def custom_evaluation_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "customEvaluationPeriod"))

    @custom_evaluation_period.setter
    def custom_evaluation_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8cc49ebdb13f4a30aefd3b44d7fa31f8483487690b9b3d5da83fe550fd8f558)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customEvaluationPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customToleratedBudgetConsumption")
    def custom_tolerated_budget_consumption(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "customToleratedBudgetConsumption"))

    @custom_tolerated_budget_consumption.setter
    def custom_tolerated_budget_consumption(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99f16eb6c00334d16560da55cfd9b6a3f3efa222d8226fe050b66e6d08e0c008)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customToleratedBudgetConsumption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb65a91101602828610e920d4de0970c0e4bfcc9ae01bd24bb34f069c8de56f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isBadEvents")
    def is_bad_events(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isBadEvents"))

    @is_bad_events.setter
    def is_bad_events(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a33eec2bfdb1259b2e86396d5165a8ac15e89179cef0ee84dc1d6e9d0bf3a839)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isBadEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sliGuid")
    def sli_guid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sliGuid"))

    @sli_guid.setter
    def sli_guid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f65c91edb5987fe94135200ea327908f962bb037833a3535cf02dd36ebb62124)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sliGuid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sloPeriod")
    def slo_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sloPeriod"))

    @slo_period.setter
    def slo_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b0113a5d2ab3da43b80debb60d0090f15f1d48f5a30ecc0acb28027f7dc1acf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sloPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sloTarget")
    def slo_target(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sloTarget"))

    @slo_target.setter
    def slo_target(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae242b87f4db119cde01f903f6693aa94c4fd5274655b8db81785b31812bbc69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sloTarget", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.dataNewrelicServiceLevelAlertHelper.DataNewrelicServiceLevelAlertHelperConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "alert_type": "alertType",
        "sli_guid": "sliGuid",
        "slo_period": "sloPeriod",
        "slo_target": "sloTarget",
        "custom_evaluation_period": "customEvaluationPeriod",
        "custom_tolerated_budget_consumption": "customToleratedBudgetConsumption",
        "id": "id",
        "is_bad_events": "isBadEvents",
    },
)
class DataNewrelicServiceLevelAlertHelperConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        alert_type: builtins.str,
        sli_guid: builtins.str,
        slo_period: jsii.Number,
        slo_target: jsii.Number,
        custom_evaluation_period: typing.Optional[jsii.Number] = None,
        custom_tolerated_budget_consumption: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        is_bad_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param alert_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#alert_type DataNewrelicServiceLevelAlertHelper#alert_type}.
        :param sli_guid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#sli_guid DataNewrelicServiceLevelAlertHelper#sli_guid}.
        :param slo_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#slo_period DataNewrelicServiceLevelAlertHelper#slo_period}.
        :param slo_target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#slo_target DataNewrelicServiceLevelAlertHelper#slo_target}.
        :param custom_evaluation_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#custom_evaluation_period DataNewrelicServiceLevelAlertHelper#custom_evaluation_period}.
        :param custom_tolerated_budget_consumption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#custom_tolerated_budget_consumption DataNewrelicServiceLevelAlertHelper#custom_tolerated_budget_consumption}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#id DataNewrelicServiceLevelAlertHelper#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_bad_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#is_bad_events DataNewrelicServiceLevelAlertHelper#is_bad_events}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__588745bacc6c8ff86b6becc4b885ff06223977e343d57a6fd3bddb2a41a2c5b1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument alert_type", value=alert_type, expected_type=type_hints["alert_type"])
            check_type(argname="argument sli_guid", value=sli_guid, expected_type=type_hints["sli_guid"])
            check_type(argname="argument slo_period", value=slo_period, expected_type=type_hints["slo_period"])
            check_type(argname="argument slo_target", value=slo_target, expected_type=type_hints["slo_target"])
            check_type(argname="argument custom_evaluation_period", value=custom_evaluation_period, expected_type=type_hints["custom_evaluation_period"])
            check_type(argname="argument custom_tolerated_budget_consumption", value=custom_tolerated_budget_consumption, expected_type=type_hints["custom_tolerated_budget_consumption"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_bad_events", value=is_bad_events, expected_type=type_hints["is_bad_events"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alert_type": alert_type,
            "sli_guid": sli_guid,
            "slo_period": slo_period,
            "slo_target": slo_target,
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
        if custom_evaluation_period is not None:
            self._values["custom_evaluation_period"] = custom_evaluation_period
        if custom_tolerated_budget_consumption is not None:
            self._values["custom_tolerated_budget_consumption"] = custom_tolerated_budget_consumption
        if id is not None:
            self._values["id"] = id
        if is_bad_events is not None:
            self._values["is_bad_events"] = is_bad_events

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
    def alert_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#alert_type DataNewrelicServiceLevelAlertHelper#alert_type}.'''
        result = self._values.get("alert_type")
        assert result is not None, "Required property 'alert_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sli_guid(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#sli_guid DataNewrelicServiceLevelAlertHelper#sli_guid}.'''
        result = self._values.get("sli_guid")
        assert result is not None, "Required property 'sli_guid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slo_period(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#slo_period DataNewrelicServiceLevelAlertHelper#slo_period}.'''
        result = self._values.get("slo_period")
        assert result is not None, "Required property 'slo_period' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def slo_target(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#slo_target DataNewrelicServiceLevelAlertHelper#slo_target}.'''
        result = self._values.get("slo_target")
        assert result is not None, "Required property 'slo_target' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def custom_evaluation_period(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#custom_evaluation_period DataNewrelicServiceLevelAlertHelper#custom_evaluation_period}.'''
        result = self._values.get("custom_evaluation_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def custom_tolerated_budget_consumption(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#custom_tolerated_budget_consumption DataNewrelicServiceLevelAlertHelper#custom_tolerated_budget_consumption}.'''
        result = self._values.get("custom_tolerated_budget_consumption")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#id DataNewrelicServiceLevelAlertHelper#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_bad_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/data-sources/service_level_alert_helper#is_bad_events DataNewrelicServiceLevelAlertHelper#is_bad_events}.'''
        result = self._values.get("is_bad_events")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataNewrelicServiceLevelAlertHelperConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataNewrelicServiceLevelAlertHelper",
    "DataNewrelicServiceLevelAlertHelperConfig",
]

publication.publish()

def _typecheckingstub__3805ecda0dc357f78cf8f305286f7ad05134b8b9e5fb3aecddd1f8470fb6b28c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    alert_type: builtins.str,
    sli_guid: builtins.str,
    slo_period: jsii.Number,
    slo_target: jsii.Number,
    custom_evaluation_period: typing.Optional[jsii.Number] = None,
    custom_tolerated_budget_consumption: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    is_bad_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__54858f1576a472fdcbef37969a11573f9b41fe9b2e4d4c63b6f73cffbaf3c87b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__effc6a28384edb1a394863fee9ff6d0f39c31e40aa377fc5a65f03675252b9be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8cc49ebdb13f4a30aefd3b44d7fa31f8483487690b9b3d5da83fe550fd8f558(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99f16eb6c00334d16560da55cfd9b6a3f3efa222d8226fe050b66e6d08e0c008(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb65a91101602828610e920d4de0970c0e4bfcc9ae01bd24bb34f069c8de56f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a33eec2bfdb1259b2e86396d5165a8ac15e89179cef0ee84dc1d6e9d0bf3a839(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f65c91edb5987fe94135200ea327908f962bb037833a3535cf02dd36ebb62124(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0113a5d2ab3da43b80debb60d0090f15f1d48f5a30ecc0acb28027f7dc1acf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae242b87f4db119cde01f903f6693aa94c4fd5274655b8db81785b31812bbc69(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__588745bacc6c8ff86b6becc4b885ff06223977e343d57a6fd3bddb2a41a2c5b1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    alert_type: builtins.str,
    sli_guid: builtins.str,
    slo_period: jsii.Number,
    slo_target: jsii.Number,
    custom_evaluation_period: typing.Optional[jsii.Number] = None,
    custom_tolerated_budget_consumption: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    is_bad_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
