r'''
# `data_datadog_custom_allocation_rule`

Refer to the Terraform Registry for docs: [`data_datadog_custom_allocation_rule`](https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule).
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


class DataDatadogCustomAllocationRule(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule datadog_custom_allocation_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        costs_to_allocate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatadogCustomAllocationRuleCostsToAllocate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rule_id: typing.Optional[jsii.Number] = None,
        strategy: typing.Optional[typing.Union["DataDatadogCustomAllocationRuleStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule datadog_custom_allocation_rule} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param costs_to_allocate: costs_to_allocate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#costs_to_allocate DataDatadogCustomAllocationRule#costs_to_allocate}
        :param rule_id: The ID of the custom allocation rule to retrieve. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#rule_id DataDatadogCustomAllocationRule#rule_id}
        :param strategy: strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#strategy DataDatadogCustomAllocationRule#strategy}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0aa79ea4c2ad0e5f43ef0fe6f837fe1486ca3d6306b2ba6a5e7ab300f2a9c87)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataDatadogCustomAllocationRuleConfig(
            costs_to_allocate=costs_to_allocate,
            rule_id=rule_id,
            strategy=strategy,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a DataDatadogCustomAllocationRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataDatadogCustomAllocationRule to import.
        :param import_from_id: The id of the existing DataDatadogCustomAllocationRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataDatadogCustomAllocationRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59196fc7bd84a3349c20e52e00fe461b05bb5928d328f96e1dee7ccb026f184a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCostsToAllocate")
    def put_costs_to_allocate(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatadogCustomAllocationRuleCostsToAllocate", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b48df7536e5f5e60c2ff52ada05b612a3d301379b46d83944b94ad1da90b05b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCostsToAllocate", [value]))

    @jsii.member(jsii_name="putStrategy")
    def put_strategy(
        self,
        *,
        allocated_by: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatadogCustomAllocationRuleStrategyAllocatedBy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        allocated_by_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatadogCustomAllocationRuleStrategyAllocatedByFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        based_on_costs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatadogCustomAllocationRuleStrategyBasedOnCosts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        based_on_timeseries: typing.Optional[typing.Union["DataDatadogCustomAllocationRuleStrategyBasedOnTimeseries", typing.Dict[builtins.str, typing.Any]]] = None,
        evaluate_grouped_by_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allocated_by: allocated_by block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#allocated_by DataDatadogCustomAllocationRule#allocated_by}
        :param allocated_by_filters: allocated_by_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#allocated_by_filters DataDatadogCustomAllocationRule#allocated_by_filters}
        :param based_on_costs: based_on_costs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#based_on_costs DataDatadogCustomAllocationRule#based_on_costs}
        :param based_on_timeseries: based_on_timeseries block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#based_on_timeseries DataDatadogCustomAllocationRule#based_on_timeseries}
        :param evaluate_grouped_by_filters: evaluate_grouped_by_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#evaluate_grouped_by_filters DataDatadogCustomAllocationRule#evaluate_grouped_by_filters}
        '''
        value = DataDatadogCustomAllocationRuleStrategy(
            allocated_by=allocated_by,
            allocated_by_filters=allocated_by_filters,
            based_on_costs=based_on_costs,
            based_on_timeseries=based_on_timeseries,
            evaluate_grouped_by_filters=evaluate_grouped_by_filters,
        )

        return typing.cast(None, jsii.invoke(self, "putStrategy", [value]))

    @jsii.member(jsii_name="resetCostsToAllocate")
    def reset_costs_to_allocate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCostsToAllocate", []))

    @jsii.member(jsii_name="resetRuleId")
    def reset_rule_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleId", []))

    @jsii.member(jsii_name="resetStrategy")
    def reset_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStrategy", []))

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
    @jsii.member(jsii_name="costsToAllocate")
    def costs_to_allocate(self) -> "DataDatadogCustomAllocationRuleCostsToAllocateList":
        return typing.cast("DataDatadogCustomAllocationRuleCostsToAllocateList", jsii.get(self, "costsToAllocate"))

    @builtins.property
    @jsii.member(jsii_name="created")
    def created(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "created"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="lastModifiedUserUuid")
    def last_modified_user_uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModifiedUserUuid"))

    @builtins.property
    @jsii.member(jsii_name="orderId")
    def order_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "orderId"))

    @builtins.property
    @jsii.member(jsii_name="providernames")
    def providernames(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "providernames"))

    @builtins.property
    @jsii.member(jsii_name="rejected")
    def rejected(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "rejected"))

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleName"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def strategy(self) -> "DataDatadogCustomAllocationRuleStrategyOutputReference":
        return typing.cast("DataDatadogCustomAllocationRuleStrategyOutputReference", jsii.get(self, "strategy"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="updated")
    def updated(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updated"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="costsToAllocateInput")
    def costs_to_allocate_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatadogCustomAllocationRuleCostsToAllocate"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatadogCustomAllocationRuleCostsToAllocate"]]], jsii.get(self, "costsToAllocateInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleIdInput")
    def rule_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ruleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="strategyInput")
    def strategy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatadogCustomAllocationRuleStrategy"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatadogCustomAllocationRuleStrategy"]], jsii.get(self, "strategyInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleId")
    def rule_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ruleId"))

    @rule_id.setter
    def rule_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8c5486f56023df71b5c0edf3932a90e0c51f20801ec39d446657136d8871c67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "costs_to_allocate": "costsToAllocate",
        "rule_id": "ruleId",
        "strategy": "strategy",
    },
)
class DataDatadogCustomAllocationRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        costs_to_allocate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatadogCustomAllocationRuleCostsToAllocate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rule_id: typing.Optional[jsii.Number] = None,
        strategy: typing.Optional[typing.Union["DataDatadogCustomAllocationRuleStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param costs_to_allocate: costs_to_allocate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#costs_to_allocate DataDatadogCustomAllocationRule#costs_to_allocate}
        :param rule_id: The ID of the custom allocation rule to retrieve. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#rule_id DataDatadogCustomAllocationRule#rule_id}
        :param strategy: strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#strategy DataDatadogCustomAllocationRule#strategy}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(strategy, dict):
            strategy = DataDatadogCustomAllocationRuleStrategy(**strategy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f5ece8960b0d6d5945d4204c3d2e2dc0c9084c261d12a6fdc8981b482144e6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument costs_to_allocate", value=costs_to_allocate, expected_type=type_hints["costs_to_allocate"])
            check_type(argname="argument rule_id", value=rule_id, expected_type=type_hints["rule_id"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if costs_to_allocate is not None:
            self._values["costs_to_allocate"] = costs_to_allocate
        if rule_id is not None:
            self._values["rule_id"] = rule_id
        if strategy is not None:
            self._values["strategy"] = strategy

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
    def costs_to_allocate(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatadogCustomAllocationRuleCostsToAllocate"]]]:
        '''costs_to_allocate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#costs_to_allocate DataDatadogCustomAllocationRule#costs_to_allocate}
        '''
        result = self._values.get("costs_to_allocate")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatadogCustomAllocationRuleCostsToAllocate"]]], result)

    @builtins.property
    def rule_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of the custom allocation rule to retrieve.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#rule_id DataDatadogCustomAllocationRule#rule_id}
        '''
        result = self._values.get("rule_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def strategy(self) -> typing.Optional["DataDatadogCustomAllocationRuleStrategy"]:
        '''strategy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#strategy DataDatadogCustomAllocationRule#strategy}
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional["DataDatadogCustomAllocationRuleStrategy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatadogCustomAllocationRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleCostsToAllocate",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataDatadogCustomAllocationRuleCostsToAllocate:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatadogCustomAllocationRuleCostsToAllocate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatadogCustomAllocationRuleCostsToAllocateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleCostsToAllocateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48df1b94c89bf214c3075721ca6dd9e69857ab35a4a81ad43807fcfee4b6c188)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataDatadogCustomAllocationRuleCostsToAllocateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4469d0fb7f6d2db45fb7cbabf33b94cffd5a10456e4f062f0469ae4ef071deea)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataDatadogCustomAllocationRuleCostsToAllocateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe2d4fafd51a0996f4c0bebe72f2d704a85cd8ad29bf51d0ce51cc53f1a24d19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53e235d202f266b9adf570def9d27026efa957ec57f708c3303db49058762b91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5a8efcf1646d1a7a183ebf90b147ef9befc44561b746237f49efdf050eb1a61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleCostsToAllocate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleCostsToAllocate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleCostsToAllocate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4548eaddaecc6df2c9cd2ce537809ea214ade8697e7c2822e0f9587c5eb63b41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatadogCustomAllocationRuleCostsToAllocateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleCostsToAllocateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7943935c21c9f1fa24731b02d2bf55788dc3dced8eddcb87b79be33c3db82110)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleCostsToAllocate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleCostsToAllocate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleCostsToAllocate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd3d2a6f86a4c32742258c8ba52390c566a2202df0186932a2bf17238446c9f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleStrategy",
    jsii_struct_bases=[],
    name_mapping={
        "allocated_by": "allocatedBy",
        "allocated_by_filters": "allocatedByFilters",
        "based_on_costs": "basedOnCosts",
        "based_on_timeseries": "basedOnTimeseries",
        "evaluate_grouped_by_filters": "evaluateGroupedByFilters",
    },
)
class DataDatadogCustomAllocationRuleStrategy:
    def __init__(
        self,
        *,
        allocated_by: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatadogCustomAllocationRuleStrategyAllocatedBy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        allocated_by_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatadogCustomAllocationRuleStrategyAllocatedByFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        based_on_costs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatadogCustomAllocationRuleStrategyBasedOnCosts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        based_on_timeseries: typing.Optional[typing.Union["DataDatadogCustomAllocationRuleStrategyBasedOnTimeseries", typing.Dict[builtins.str, typing.Any]]] = None,
        evaluate_grouped_by_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allocated_by: allocated_by block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#allocated_by DataDatadogCustomAllocationRule#allocated_by}
        :param allocated_by_filters: allocated_by_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#allocated_by_filters DataDatadogCustomAllocationRule#allocated_by_filters}
        :param based_on_costs: based_on_costs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#based_on_costs DataDatadogCustomAllocationRule#based_on_costs}
        :param based_on_timeseries: based_on_timeseries block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#based_on_timeseries DataDatadogCustomAllocationRule#based_on_timeseries}
        :param evaluate_grouped_by_filters: evaluate_grouped_by_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#evaluate_grouped_by_filters DataDatadogCustomAllocationRule#evaluate_grouped_by_filters}
        '''
        if isinstance(based_on_timeseries, dict):
            based_on_timeseries = DataDatadogCustomAllocationRuleStrategyBasedOnTimeseries(**based_on_timeseries)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6092228987904b839675110709d74c5ef21d4e3d29fca86795fd4435ef4b5763)
            check_type(argname="argument allocated_by", value=allocated_by, expected_type=type_hints["allocated_by"])
            check_type(argname="argument allocated_by_filters", value=allocated_by_filters, expected_type=type_hints["allocated_by_filters"])
            check_type(argname="argument based_on_costs", value=based_on_costs, expected_type=type_hints["based_on_costs"])
            check_type(argname="argument based_on_timeseries", value=based_on_timeseries, expected_type=type_hints["based_on_timeseries"])
            check_type(argname="argument evaluate_grouped_by_filters", value=evaluate_grouped_by_filters, expected_type=type_hints["evaluate_grouped_by_filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allocated_by is not None:
            self._values["allocated_by"] = allocated_by
        if allocated_by_filters is not None:
            self._values["allocated_by_filters"] = allocated_by_filters
        if based_on_costs is not None:
            self._values["based_on_costs"] = based_on_costs
        if based_on_timeseries is not None:
            self._values["based_on_timeseries"] = based_on_timeseries
        if evaluate_grouped_by_filters is not None:
            self._values["evaluate_grouped_by_filters"] = evaluate_grouped_by_filters

    @builtins.property
    def allocated_by(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatadogCustomAllocationRuleStrategyAllocatedBy"]]]:
        '''allocated_by block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#allocated_by DataDatadogCustomAllocationRule#allocated_by}
        '''
        result = self._values.get("allocated_by")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatadogCustomAllocationRuleStrategyAllocatedBy"]]], result)

    @builtins.property
    def allocated_by_filters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatadogCustomAllocationRuleStrategyAllocatedByFilters"]]]:
        '''allocated_by_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#allocated_by_filters DataDatadogCustomAllocationRule#allocated_by_filters}
        '''
        result = self._values.get("allocated_by_filters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatadogCustomAllocationRuleStrategyAllocatedByFilters"]]], result)

    @builtins.property
    def based_on_costs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatadogCustomAllocationRuleStrategyBasedOnCosts"]]]:
        '''based_on_costs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#based_on_costs DataDatadogCustomAllocationRule#based_on_costs}
        '''
        result = self._values.get("based_on_costs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatadogCustomAllocationRuleStrategyBasedOnCosts"]]], result)

    @builtins.property
    def based_on_timeseries(
        self,
    ) -> typing.Optional["DataDatadogCustomAllocationRuleStrategyBasedOnTimeseries"]:
        '''based_on_timeseries block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#based_on_timeseries DataDatadogCustomAllocationRule#based_on_timeseries}
        '''
        result = self._values.get("based_on_timeseries")
        return typing.cast(typing.Optional["DataDatadogCustomAllocationRuleStrategyBasedOnTimeseries"], result)

    @builtins.property
    def evaluate_grouped_by_filters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFilters"]]]:
        '''evaluate_grouped_by_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#evaluate_grouped_by_filters DataDatadogCustomAllocationRule#evaluate_grouped_by_filters}
        '''
        result = self._values.get("evaluate_grouped_by_filters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFilters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatadogCustomAllocationRuleStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleStrategyAllocatedBy",
    jsii_struct_bases=[],
    name_mapping={"allocated_tags": "allocatedTags"},
)
class DataDatadogCustomAllocationRuleStrategyAllocatedBy:
    def __init__(
        self,
        *,
        allocated_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allocated_tags: allocated_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#allocated_tags DataDatadogCustomAllocationRule#allocated_tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b37d6c48490598fc8b77ae9ca2afa5683eb8d1da3bd47ee9d9cb611f759fdc4)
            check_type(argname="argument allocated_tags", value=allocated_tags, expected_type=type_hints["allocated_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allocated_tags is not None:
            self._values["allocated_tags"] = allocated_tags

    @builtins.property
    def allocated_tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTags"]]]:
        '''allocated_tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/data-sources/custom_allocation_rule#allocated_tags DataDatadogCustomAllocationRule#allocated_tags}
        '''
        result = self._values.get("allocated_tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTags"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatadogCustomAllocationRuleStrategyAllocatedBy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTags",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTags:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d58789f360a80871862e155eb2cf04e03e638ebfc04d5008f1c04bf00dbfe6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8010ae4ac324c64c477718904c424ea9b56f946947bb3120b6022efe263801e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52e11af2e2981861f2e144123cb5c822a10c5b26a875bb1eeb292bf5948718d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d10eafb7e28c1dfdd8e830cb77b38f8d5c4a9285110280bc77ba2fe6a4564cf9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4097996e0f6e6bc48f5b41999d44d8e4a41de6068a90ea253f289c7de1adca77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bd9ce424376de27a552e545f5189c15d05f7b89fc4e4314d3546e1432eb1444)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e694488bec8f8a78e70dafbd96b9da9098c9ef5a1aec988a00aa71965e184e30)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc7839367cb1c0200651c19561e8f02be52e56838b2b8ffb46ca7258f011e03e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleStrategyAllocatedByFilters",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataDatadogCustomAllocationRuleStrategyAllocatedByFilters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatadogCustomAllocationRuleStrategyAllocatedByFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatadogCustomAllocationRuleStrategyAllocatedByFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleStrategyAllocatedByFiltersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbd5288efe72787c6b19813a5b0f7bc032d97122cf561e2014ec48f14014573f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataDatadogCustomAllocationRuleStrategyAllocatedByFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24cc124edca7cf575f98c7cb9ea2faa4b0b36f39e5551d5ed6c91f4f41279c35)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataDatadogCustomAllocationRuleStrategyAllocatedByFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1955a0e7b75954d4a8b4e415d0cafe47c6a54c50dd1af30c35f2572ac67eda5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86ff321c3b6d21158cf52bfe1a963605bf573ce547139ddae3ef46e3ec8d5d9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed3d3d4d796960d323cd3edba2beaa4b2226615445a763435584ce1da775b27b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyAllocatedByFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyAllocatedByFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyAllocatedByFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__383223af28806f9a8691850ad2e349bf4bf4810e83a6df412a707d169d5c325e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatadogCustomAllocationRuleStrategyAllocatedByFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleStrategyAllocatedByFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bc15cacc2d04294486dcfd9bcc42a4d28580c16a5b2a26174b501f4daab8382)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyAllocatedByFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyAllocatedByFilters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyAllocatedByFilters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a0e3518871f8b12861cd3a9133038bcea43a957edb46b4a64b84cebb2caa30c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatadogCustomAllocationRuleStrategyAllocatedByList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleStrategyAllocatedByList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d03958b6285c6e5f1a5129223a1226dfc3feb469d6b85f452e93bd35a02b1fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataDatadogCustomAllocationRuleStrategyAllocatedByOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__838572985e7f3f7cbc134abfc16d5469f5c67fdee289f0fabb4f24a76526fd39)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataDatadogCustomAllocationRuleStrategyAllocatedByOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a97c9c822ba6cf127f83d60f446eb7193c8e3c7bc12edf056869fb62f61a0f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d74f25a9ddb990cf85ab469e1ef9aa00b8659ce4e78b208d380a39115947bc6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82d19f05670abe7930be7886adceeb6500a9fa2576714b7e85741f72495fa5a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyAllocatedBy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyAllocatedBy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyAllocatedBy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9918f172d3b6d510f03c802031915e6bf3a0fd8000341a3b0b05bb05d0172c99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatadogCustomAllocationRuleStrategyAllocatedByOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleStrategyAllocatedByOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0dfc016388ec57ebd249aa0ac7b47b4da04c406edfe72740cbf625077930f763)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAllocatedTags")
    def put_allocated_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTags, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79c129b03240b91063fd895401ab6ce732c38ca63fe4f0474377261ece605695)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllocatedTags", [value]))

    @jsii.member(jsii_name="resetAllocatedTags")
    def reset_allocated_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllocatedTags", []))

    @builtins.property
    @jsii.member(jsii_name="allocatedTags")
    def allocated_tags(
        self,
    ) -> DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTagsList:
        return typing.cast(DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTagsList, jsii.get(self, "allocatedTags"))

    @builtins.property
    @jsii.member(jsii_name="percentage")
    def percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percentage"))

    @builtins.property
    @jsii.member(jsii_name="allocatedTagsInput")
    def allocated_tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTags]]], jsii.get(self, "allocatedTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyAllocatedBy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyAllocatedBy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyAllocatedBy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f43dd37adfafaf33d19b40d6c8e94b7249e0e5a449d2f0e250b5aecb15e7cd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleStrategyBasedOnCosts",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataDatadogCustomAllocationRuleStrategyBasedOnCosts:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatadogCustomAllocationRuleStrategyBasedOnCosts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatadogCustomAllocationRuleStrategyBasedOnCostsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleStrategyBasedOnCostsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a63a7825c0dfc1e2e3e5c7cde5a2534999cf0fed3ee4eb3776c2a7a94f083ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataDatadogCustomAllocationRuleStrategyBasedOnCostsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d50f3403b6b9304e8e64017d03b3429147f53f777624a36e60b0fc197c63c8d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataDatadogCustomAllocationRuleStrategyBasedOnCostsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd456bb13b73c5f3dfa165c98844181d4237a7db6f574c483537504bbbd300b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__864092937b2c4724264f9e608fc6198216d8fd649786cc828dadc38792ab474f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__910a54fd431d0cbf9b90daace7917338d4d502cd29157463d7497c051acd896d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyBasedOnCosts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyBasedOnCosts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyBasedOnCosts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f8415dea808e2856159ccca4ae8fd9f8629f061b5da051b91e74587d39a4a3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatadogCustomAllocationRuleStrategyBasedOnCostsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleStrategyBasedOnCostsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c965f482c2f8b77efab213da1a78e67260acedc1b996bda26079d5ef0a7f479f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyBasedOnCosts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyBasedOnCosts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyBasedOnCosts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01f1db9c2bf1e76f47bcd3cfd8da107c244ba40d63e4eec6d710247a58108c73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleStrategyBasedOnTimeseries",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataDatadogCustomAllocationRuleStrategyBasedOnTimeseries:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatadogCustomAllocationRuleStrategyBasedOnTimeseries(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatadogCustomAllocationRuleStrategyBasedOnTimeseriesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleStrategyBasedOnTimeseriesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cba016ecbc1fc46614c203d6f49befec5c91eaa45f1997d79eafc20910290250)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyBasedOnTimeseries]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyBasedOnTimeseries]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyBasedOnTimeseries]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a9c67e6078c9728125952947dfb5511a6be9fa3e68945a05c8856b843a10ef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFilters",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFilters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFiltersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0aec6666538e3353e07f7ccf451a46c221c22579b2ca7a8bc6e677889a9bcde)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__343e61a40931cf4cb4472626e41c81dda168208f69cb1fe29c16face11c567d2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe08ae7e61a8bd23bf8bc7b1ac2404cbc21048f62b62eecbe236e06dd4daa24b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47245a4afb603212e9eb18412ea0eec2e86eabbfa37eeba22749439028710145)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50ab86b97bfe48a67156396ca3dc4925cffec215e15b3e43bb8fcd0c388b2d25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad8c3736103dd2bc945ee1800048bb9c9b965a42dba29417e50da68a96a8b25f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__483d91b30c4520f8bb0cea7cf356fda5afc3ec25e0e8ac0da2ed413222f12aa0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFilters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFilters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c369a9a4c0ec9c7c89816e482c4e426af5349905901324a53d76356cfe14c451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatadogCustomAllocationRuleStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogCustomAllocationRule.DataDatadogCustomAllocationRuleStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eccc975197c9fcfb1f8a5e23db9546e8455f8993c29c02c7c48e2d98ff339ffd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAllocatedBy")
    def put_allocated_by(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatadogCustomAllocationRuleStrategyAllocatedBy, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09f84f2cce18688dd14772052e628082431c98b8dfc1b8242654b3771135c7f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllocatedBy", [value]))

    @jsii.member(jsii_name="putAllocatedByFilters")
    def put_allocated_by_filters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatadogCustomAllocationRuleStrategyAllocatedByFilters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fa9a98d73726c288107ca77aa691ba9b1732d464511e15cac01e1c69c434f40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllocatedByFilters", [value]))

    @jsii.member(jsii_name="putBasedOnCosts")
    def put_based_on_costs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatadogCustomAllocationRuleStrategyBasedOnCosts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__992a836ba9cd55522317c7bef51befef2be744542b8f122e09357c1851dfe755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBasedOnCosts", [value]))

    @jsii.member(jsii_name="putBasedOnTimeseries")
    def put_based_on_timeseries(self) -> None:
        value = DataDatadogCustomAllocationRuleStrategyBasedOnTimeseries()

        return typing.cast(None, jsii.invoke(self, "putBasedOnTimeseries", [value]))

    @jsii.member(jsii_name="putEvaluateGroupedByFilters")
    def put_evaluate_grouped_by_filters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFilters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba3251a1d1df33b62dd4aaa24b32914b850b32bace84579343c9727d2fc331b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEvaluateGroupedByFilters", [value]))

    @jsii.member(jsii_name="resetAllocatedBy")
    def reset_allocated_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllocatedBy", []))

    @jsii.member(jsii_name="resetAllocatedByFilters")
    def reset_allocated_by_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllocatedByFilters", []))

    @jsii.member(jsii_name="resetBasedOnCosts")
    def reset_based_on_costs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasedOnCosts", []))

    @jsii.member(jsii_name="resetEvaluateGroupedByFilters")
    def reset_evaluate_grouped_by_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvaluateGroupedByFilters", []))

    @builtins.property
    @jsii.member(jsii_name="allocatedBy")
    def allocated_by(self) -> DataDatadogCustomAllocationRuleStrategyAllocatedByList:
        return typing.cast(DataDatadogCustomAllocationRuleStrategyAllocatedByList, jsii.get(self, "allocatedBy"))

    @builtins.property
    @jsii.member(jsii_name="allocatedByFilters")
    def allocated_by_filters(
        self,
    ) -> DataDatadogCustomAllocationRuleStrategyAllocatedByFiltersList:
        return typing.cast(DataDatadogCustomAllocationRuleStrategyAllocatedByFiltersList, jsii.get(self, "allocatedByFilters"))

    @builtins.property
    @jsii.member(jsii_name="allocatedByTagKeys")
    def allocated_by_tag_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allocatedByTagKeys"))

    @builtins.property
    @jsii.member(jsii_name="basedOnCosts")
    def based_on_costs(self) -> DataDatadogCustomAllocationRuleStrategyBasedOnCostsList:
        return typing.cast(DataDatadogCustomAllocationRuleStrategyBasedOnCostsList, jsii.get(self, "basedOnCosts"))

    @builtins.property
    @jsii.member(jsii_name="basedOnTimeseries")
    def based_on_timeseries(
        self,
    ) -> DataDatadogCustomAllocationRuleStrategyBasedOnTimeseriesOutputReference:
        return typing.cast(DataDatadogCustomAllocationRuleStrategyBasedOnTimeseriesOutputReference, jsii.get(self, "basedOnTimeseries"))

    @builtins.property
    @jsii.member(jsii_name="evaluateGroupedByFilters")
    def evaluate_grouped_by_filters(
        self,
    ) -> DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFiltersList:
        return typing.cast(DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFiltersList, jsii.get(self, "evaluateGroupedByFilters"))

    @builtins.property
    @jsii.member(jsii_name="evaluateGroupedByTagKeys")
    def evaluate_grouped_by_tag_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "evaluateGroupedByTagKeys"))

    @builtins.property
    @jsii.member(jsii_name="granularity")
    def granularity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "granularity"))

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @builtins.property
    @jsii.member(jsii_name="allocatedByFiltersInput")
    def allocated_by_filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyAllocatedByFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyAllocatedByFilters]]], jsii.get(self, "allocatedByFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="allocatedByInput")
    def allocated_by_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyAllocatedBy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyAllocatedBy]]], jsii.get(self, "allocatedByInput"))

    @builtins.property
    @jsii.member(jsii_name="basedOnCostsInput")
    def based_on_costs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyBasedOnCosts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyBasedOnCosts]]], jsii.get(self, "basedOnCostsInput"))

    @builtins.property
    @jsii.member(jsii_name="basedOnTimeseriesInput")
    def based_on_timeseries_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyBasedOnTimeseries]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyBasedOnTimeseries]], jsii.get(self, "basedOnTimeseriesInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluateGroupedByFiltersInput")
    def evaluate_grouped_by_filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFilters]]], jsii.get(self, "evaluateGroupedByFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61f402850e54e81c9f72ed2e24ae78ca7ec31e4f37aec271d10e57a408d57840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataDatadogCustomAllocationRule",
    "DataDatadogCustomAllocationRuleConfig",
    "DataDatadogCustomAllocationRuleCostsToAllocate",
    "DataDatadogCustomAllocationRuleCostsToAllocateList",
    "DataDatadogCustomAllocationRuleCostsToAllocateOutputReference",
    "DataDatadogCustomAllocationRuleStrategy",
    "DataDatadogCustomAllocationRuleStrategyAllocatedBy",
    "DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTags",
    "DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTagsList",
    "DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTagsOutputReference",
    "DataDatadogCustomAllocationRuleStrategyAllocatedByFilters",
    "DataDatadogCustomAllocationRuleStrategyAllocatedByFiltersList",
    "DataDatadogCustomAllocationRuleStrategyAllocatedByFiltersOutputReference",
    "DataDatadogCustomAllocationRuleStrategyAllocatedByList",
    "DataDatadogCustomAllocationRuleStrategyAllocatedByOutputReference",
    "DataDatadogCustomAllocationRuleStrategyBasedOnCosts",
    "DataDatadogCustomAllocationRuleStrategyBasedOnCostsList",
    "DataDatadogCustomAllocationRuleStrategyBasedOnCostsOutputReference",
    "DataDatadogCustomAllocationRuleStrategyBasedOnTimeseries",
    "DataDatadogCustomAllocationRuleStrategyBasedOnTimeseriesOutputReference",
    "DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFilters",
    "DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFiltersList",
    "DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFiltersOutputReference",
    "DataDatadogCustomAllocationRuleStrategyOutputReference",
]

publication.publish()

def _typecheckingstub__f0aa79ea4c2ad0e5f43ef0fe6f837fe1486ca3d6306b2ba6a5e7ab300f2a9c87(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    costs_to_allocate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatadogCustomAllocationRuleCostsToAllocate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rule_id: typing.Optional[jsii.Number] = None,
    strategy: typing.Optional[typing.Union[DataDatadogCustomAllocationRuleStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__59196fc7bd84a3349c20e52e00fe461b05bb5928d328f96e1dee7ccb026f184a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b48df7536e5f5e60c2ff52ada05b612a3d301379b46d83944b94ad1da90b05b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatadogCustomAllocationRuleCostsToAllocate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8c5486f56023df71b5c0edf3932a90e0c51f20801ec39d446657136d8871c67(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f5ece8960b0d6d5945d4204c3d2e2dc0c9084c261d12a6fdc8981b482144e6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    costs_to_allocate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatadogCustomAllocationRuleCostsToAllocate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rule_id: typing.Optional[jsii.Number] = None,
    strategy: typing.Optional[typing.Union[DataDatadogCustomAllocationRuleStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48df1b94c89bf214c3075721ca6dd9e69857ab35a4a81ad43807fcfee4b6c188(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4469d0fb7f6d2db45fb7cbabf33b94cffd5a10456e4f062f0469ae4ef071deea(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2d4fafd51a0996f4c0bebe72f2d704a85cd8ad29bf51d0ce51cc53f1a24d19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e235d202f266b9adf570def9d27026efa957ec57f708c3303db49058762b91(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a8efcf1646d1a7a183ebf90b147ef9befc44561b746237f49efdf050eb1a61(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4548eaddaecc6df2c9cd2ce537809ea214ade8697e7c2822e0f9587c5eb63b41(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleCostsToAllocate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7943935c21c9f1fa24731b02d2bf55788dc3dced8eddcb87b79be33c3db82110(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd3d2a6f86a4c32742258c8ba52390c566a2202df0186932a2bf17238446c9f5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleCostsToAllocate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6092228987904b839675110709d74c5ef21d4e3d29fca86795fd4435ef4b5763(
    *,
    allocated_by: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatadogCustomAllocationRuleStrategyAllocatedBy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    allocated_by_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatadogCustomAllocationRuleStrategyAllocatedByFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    based_on_costs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatadogCustomAllocationRuleStrategyBasedOnCosts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    based_on_timeseries: typing.Optional[typing.Union[DataDatadogCustomAllocationRuleStrategyBasedOnTimeseries, typing.Dict[builtins.str, typing.Any]]] = None,
    evaluate_grouped_by_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b37d6c48490598fc8b77ae9ca2afa5683eb8d1da3bd47ee9d9cb611f759fdc4(
    *,
    allocated_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d58789f360a80871862e155eb2cf04e03e638ebfc04d5008f1c04bf00dbfe6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8010ae4ac324c64c477718904c424ea9b56f946947bb3120b6022efe263801e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52e11af2e2981861f2e144123cb5c822a10c5b26a875bb1eeb292bf5948718d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d10eafb7e28c1dfdd8e830cb77b38f8d5c4a9285110280bc77ba2fe6a4564cf9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4097996e0f6e6bc48f5b41999d44d8e4a41de6068a90ea253f289c7de1adca77(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bd9ce424376de27a552e545f5189c15d05f7b89fc4e4314d3546e1432eb1444(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e694488bec8f8a78e70dafbd96b9da9098c9ef5a1aec988a00aa71965e184e30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7839367cb1c0200651c19561e8f02be52e56838b2b8ffb46ca7258f011e03e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbd5288efe72787c6b19813a5b0f7bc032d97122cf561e2014ec48f14014573f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24cc124edca7cf575f98c7cb9ea2faa4b0b36f39e5551d5ed6c91f4f41279c35(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1955a0e7b75954d4a8b4e415d0cafe47c6a54c50dd1af30c35f2572ac67eda5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ff321c3b6d21158cf52bfe1a963605bf573ce547139ddae3ef46e3ec8d5d9a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed3d3d4d796960d323cd3edba2beaa4b2226615445a763435584ce1da775b27b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383223af28806f9a8691850ad2e349bf4bf4810e83a6df412a707d169d5c325e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyAllocatedByFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc15cacc2d04294486dcfd9bcc42a4d28580c16a5b2a26174b501f4daab8382(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a0e3518871f8b12861cd3a9133038bcea43a957edb46b4a64b84cebb2caa30c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyAllocatedByFilters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d03958b6285c6e5f1a5129223a1226dfc3feb469d6b85f452e93bd35a02b1fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__838572985e7f3f7cbc134abfc16d5469f5c67fdee289f0fabb4f24a76526fd39(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a97c9c822ba6cf127f83d60f446eb7193c8e3c7bc12edf056869fb62f61a0f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d74f25a9ddb990cf85ab469e1ef9aa00b8659ce4e78b208d380a39115947bc6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82d19f05670abe7930be7886adceeb6500a9fa2576714b7e85741f72495fa5a8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9918f172d3b6d510f03c802031915e6bf3a0fd8000341a3b0b05bb05d0172c99(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyAllocatedBy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dfc016388ec57ebd249aa0ac7b47b4da04c406edfe72740cbf625077930f763(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79c129b03240b91063fd895401ab6ce732c38ca63fe4f0474377261ece605695(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatadogCustomAllocationRuleStrategyAllocatedByAllocatedTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f43dd37adfafaf33d19b40d6c8e94b7249e0e5a449d2f0e250b5aecb15e7cd8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyAllocatedBy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a63a7825c0dfc1e2e3e5c7cde5a2534999cf0fed3ee4eb3776c2a7a94f083ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d50f3403b6b9304e8e64017d03b3429147f53f777624a36e60b0fc197c63c8d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd456bb13b73c5f3dfa165c98844181d4237a7db6f574c483537504bbbd300b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864092937b2c4724264f9e608fc6198216d8fd649786cc828dadc38792ab474f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__910a54fd431d0cbf9b90daace7917338d4d502cd29157463d7497c051acd896d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f8415dea808e2856159ccca4ae8fd9f8629f061b5da051b91e74587d39a4a3b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyBasedOnCosts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c965f482c2f8b77efab213da1a78e67260acedc1b996bda26079d5ef0a7f479f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f1db9c2bf1e76f47bcd3cfd8da107c244ba40d63e4eec6d710247a58108c73(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyBasedOnCosts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba016ecbc1fc46614c203d6f49befec5c91eaa45f1997d79eafc20910290250(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9c67e6078c9728125952947dfb5511a6be9fa3e68945a05c8856b843a10ef8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyBasedOnTimeseries]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0aec6666538e3353e07f7ccf451a46c221c22579b2ca7a8bc6e677889a9bcde(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__343e61a40931cf4cb4472626e41c81dda168208f69cb1fe29c16face11c567d2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe08ae7e61a8bd23bf8bc7b1ac2404cbc21048f62b62eecbe236e06dd4daa24b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47245a4afb603212e9eb18412ea0eec2e86eabbfa37eeba22749439028710145(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ab86b97bfe48a67156396ca3dc4925cffec215e15b3e43bb8fcd0c388b2d25(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad8c3736103dd2bc945ee1800048bb9c9b965a42dba29417e50da68a96a8b25f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__483d91b30c4520f8bb0cea7cf356fda5afc3ec25e0e8ac0da2ed413222f12aa0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c369a9a4c0ec9c7c89816e482c4e426af5349905901324a53d76356cfe14c451(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFilters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eccc975197c9fcfb1f8a5e23db9546e8455f8993c29c02c7c48e2d98ff339ffd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09f84f2cce18688dd14772052e628082431c98b8dfc1b8242654b3771135c7f3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatadogCustomAllocationRuleStrategyAllocatedBy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa9a98d73726c288107ca77aa691ba9b1732d464511e15cac01e1c69c434f40(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatadogCustomAllocationRuleStrategyAllocatedByFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__992a836ba9cd55522317c7bef51befef2be744542b8f122e09357c1851dfe755(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatadogCustomAllocationRuleStrategyBasedOnCosts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba3251a1d1df33b62dd4aaa24b32914b850b32bace84579343c9727d2fc331b8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatadogCustomAllocationRuleStrategyEvaluateGroupedByFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f402850e54e81c9f72ed2e24ae78ca7ec31e4f37aec271d10e57a408d57840(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatadogCustomAllocationRuleStrategy]],
) -> None:
    """Type checking stubs"""
    pass
