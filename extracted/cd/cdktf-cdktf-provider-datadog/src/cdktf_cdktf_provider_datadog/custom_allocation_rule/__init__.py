r'''
# `datadog_custom_allocation_rule`

Refer to the Terraform Registry for docs: [`datadog_custom_allocation_rule`](https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule).
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


class CustomAllocationRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule datadog_custom_allocation_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        providernames: typing.Sequence[builtins.str],
        rule_name: builtins.str,
        costs_to_allocate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CustomAllocationRuleCostsToAllocate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        strategy: typing.Optional[typing.Union["CustomAllocationRuleStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule datadog_custom_allocation_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param enabled: Whether the custom allocation rule is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#enabled CustomAllocationRule#enabled}
        :param providernames: List of cloud providers the rule applies to. Valid values include ``aws``, ``azure``, and ``gcp``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#providernames CustomAllocationRule#providernames}
        :param rule_name: The name of the custom allocation rule. This field is immutable - changing it will force replacement of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#rule_name CustomAllocationRule#rule_name}
        :param costs_to_allocate: costs_to_allocate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#costs_to_allocate CustomAllocationRule#costs_to_allocate}
        :param strategy: strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#strategy CustomAllocationRule#strategy}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a8ebde22f4448073601b3cc7672cec499614cd0ebd76c2b7d47c675cfbd32ad)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = CustomAllocationRuleConfig(
            enabled=enabled,
            providernames=providernames,
            rule_name=rule_name,
            costs_to_allocate=costs_to_allocate,
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
        '''Generates CDKTF code for importing a CustomAllocationRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CustomAllocationRule to import.
        :param import_from_id: The id of the existing CustomAllocationRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CustomAllocationRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acb014525dd058b5ce6a3b5662efef0cdfa84ea6ac7c7f1b67ce3e3a7dfd81b9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCostsToAllocate")
    def put_costs_to_allocate(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CustomAllocationRuleCostsToAllocate", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__182f38aa609bf8b03d4d0e7b9d7569e78c3006c3381e44a0f3c183341d91a224)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCostsToAllocate", [value]))

    @jsii.member(jsii_name="putStrategy")
    def put_strategy(
        self,
        *,
        allocated_by: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CustomAllocationRuleStrategyAllocatedBy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        allocated_by_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CustomAllocationRuleStrategyAllocatedByFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        allocated_by_tag_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        based_on_costs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CustomAllocationRuleStrategyBasedOnCosts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        based_on_timeseries: typing.Optional[typing.Union["CustomAllocationRuleStrategyBasedOnTimeseries", typing.Dict[builtins.str, typing.Any]]] = None,
        evaluate_grouped_by_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CustomAllocationRuleStrategyEvaluateGroupedByFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        evaluate_grouped_by_tag_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        granularity: typing.Optional[builtins.str] = None,
        method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allocated_by: allocated_by block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#allocated_by CustomAllocationRule#allocated_by}
        :param allocated_by_filters: allocated_by_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#allocated_by_filters CustomAllocationRule#allocated_by_filters}
        :param allocated_by_tag_keys: List of tag keys used to allocate costs (e.g., ``["team", "project"]``). Costs will be distributed across unique values of these tags. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#allocated_by_tag_keys CustomAllocationRule#allocated_by_tag_keys}
        :param based_on_costs: based_on_costs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#based_on_costs CustomAllocationRule#based_on_costs}
        :param based_on_timeseries: based_on_timeseries block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#based_on_timeseries CustomAllocationRule#based_on_timeseries}
        :param evaluate_grouped_by_filters: evaluate_grouped_by_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#evaluate_grouped_by_filters CustomAllocationRule#evaluate_grouped_by_filters}
        :param evaluate_grouped_by_tag_keys: List of tag keys used to group costs before allocation. Costs are grouped by these tag values before applying the allocation strategy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#evaluate_grouped_by_tag_keys CustomAllocationRule#evaluate_grouped_by_tag_keys}
        :param granularity: The granularity level for cost allocation. Valid values are ``daily`` or ``monthly``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#granularity CustomAllocationRule#granularity}
        :param method: The allocation method. Valid values are ``even``, ``proportional``, ``proportional_timeseries``, or ``percent``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#method CustomAllocationRule#method}
        '''
        value = CustomAllocationRuleStrategy(
            allocated_by=allocated_by,
            allocated_by_filters=allocated_by_filters,
            allocated_by_tag_keys=allocated_by_tag_keys,
            based_on_costs=based_on_costs,
            based_on_timeseries=based_on_timeseries,
            evaluate_grouped_by_filters=evaluate_grouped_by_filters,
            evaluate_grouped_by_tag_keys=evaluate_grouped_by_tag_keys,
            granularity=granularity,
            method=method,
        )

        return typing.cast(None, jsii.invoke(self, "putStrategy", [value]))

    @jsii.member(jsii_name="resetCostsToAllocate")
    def reset_costs_to_allocate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCostsToAllocate", []))

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
    def costs_to_allocate(self) -> "CustomAllocationRuleCostsToAllocateList":
        return typing.cast("CustomAllocationRuleCostsToAllocateList", jsii.get(self, "costsToAllocate"))

    @builtins.property
    @jsii.member(jsii_name="created")
    def created(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "created"))

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
    @jsii.member(jsii_name="rejected")
    def rejected(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "rejected"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def strategy(self) -> "CustomAllocationRuleStrategyOutputReference":
        return typing.cast("CustomAllocationRuleStrategyOutputReference", jsii.get(self, "strategy"))

    @builtins.property
    @jsii.member(jsii_name="updated")
    def updated(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updated"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="costsToAllocateInput")
    def costs_to_allocate_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomAllocationRuleCostsToAllocate"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomAllocationRuleCostsToAllocate"]]], jsii.get(self, "costsToAllocateInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="providernamesInput")
    def providernames_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "providernamesInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleNameInput")
    def rule_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="strategyInput")
    def strategy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CustomAllocationRuleStrategy"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CustomAllocationRuleStrategy"]], jsii.get(self, "strategyInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3090b7b3bfd273f513729396007ea946e5975485b6e749c20fd07b465719c05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="providernames")
    def providernames(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "providernames"))

    @providernames.setter
    def providernames(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2297c0d57da21fc95cfd85718f204696632adb3f083f2a00bc168b38366cd979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providernames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleName"))

    @rule_name.setter
    def rule_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b12a4650a6f88b72e92784c747c100ab9d43dc8c47b52f1b6d4efbce53b8a9f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "enabled": "enabled",
        "providernames": "providernames",
        "rule_name": "ruleName",
        "costs_to_allocate": "costsToAllocate",
        "strategy": "strategy",
    },
)
class CustomAllocationRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        providernames: typing.Sequence[builtins.str],
        rule_name: builtins.str,
        costs_to_allocate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CustomAllocationRuleCostsToAllocate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        strategy: typing.Optional[typing.Union["CustomAllocationRuleStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param enabled: Whether the custom allocation rule is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#enabled CustomAllocationRule#enabled}
        :param providernames: List of cloud providers the rule applies to. Valid values include ``aws``, ``azure``, and ``gcp``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#providernames CustomAllocationRule#providernames}
        :param rule_name: The name of the custom allocation rule. This field is immutable - changing it will force replacement of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#rule_name CustomAllocationRule#rule_name}
        :param costs_to_allocate: costs_to_allocate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#costs_to_allocate CustomAllocationRule#costs_to_allocate}
        :param strategy: strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#strategy CustomAllocationRule#strategy}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(strategy, dict):
            strategy = CustomAllocationRuleStrategy(**strategy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0b3e94ca34d201d6e5d68ef18cdc127131ca23c8b701acb8b52ca1b59068250)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument providernames", value=providernames, expected_type=type_hints["providernames"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument costs_to_allocate", value=costs_to_allocate, expected_type=type_hints["costs_to_allocate"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "providernames": providernames,
            "rule_name": rule_name,
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
        if costs_to_allocate is not None:
            self._values["costs_to_allocate"] = costs_to_allocate
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
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether the custom allocation rule is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#enabled CustomAllocationRule#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def providernames(self) -> typing.List[builtins.str]:
        '''List of cloud providers the rule applies to. Valid values include ``aws``, ``azure``, and ``gcp``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#providernames CustomAllocationRule#providernames}
        '''
        result = self._values.get("providernames")
        assert result is not None, "Required property 'providernames' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def rule_name(self) -> builtins.str:
        '''The name of the custom allocation rule.

        This field is immutable - changing it will force replacement of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#rule_name CustomAllocationRule#rule_name}
        '''
        result = self._values.get("rule_name")
        assert result is not None, "Required property 'rule_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def costs_to_allocate(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomAllocationRuleCostsToAllocate"]]]:
        '''costs_to_allocate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#costs_to_allocate CustomAllocationRule#costs_to_allocate}
        '''
        result = self._values.get("costs_to_allocate")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomAllocationRuleCostsToAllocate"]]], result)

    @builtins.property
    def strategy(self) -> typing.Optional["CustomAllocationRuleStrategy"]:
        '''strategy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#strategy CustomAllocationRule#strategy}
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional["CustomAllocationRuleStrategy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomAllocationRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleCostsToAllocate",
    jsii_struct_bases=[],
    name_mapping={
        "condition": "condition",
        "tag": "tag",
        "value": "value",
        "values": "values",
    },
)
class CustomAllocationRuleCostsToAllocate:
    def __init__(
        self,
        *,
        condition: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param condition: The condition to match. Valid values are ``=``, ``!=``, ``is``, ``is not``, ``like``, ``in``, ``not in``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#condition CustomAllocationRule#condition}
        :param tag: The tag key to filter on (e.g., ``aws_product``, ``team``, ``environment``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#tag CustomAllocationRule#tag}
        :param value: The single tag value to match. Use this field for conditions like ``=``, ``!=``, ``is``, ``is not``, ``like``. Do not use with ``in`` or ``not in`` conditions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#value CustomAllocationRule#value}
        :param values: A list of tag values to match. Use this field for ``in`` or ``not in`` conditions only. Do not use with single-value conditions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#values CustomAllocationRule#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82dc23b61caec44ea08aa6a00d556347a6bbeab38ed8f41f32e31b140ef52544)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if condition is not None:
            self._values["condition"] = condition
        if tag is not None:
            self._values["tag"] = tag
        if value is not None:
            self._values["value"] = value
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''The condition to match. Valid values are ``=``, ``!=``, ``is``, ``is not``, ``like``, ``in``, ``not in``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#condition CustomAllocationRule#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''The tag key to filter on (e.g., ``aws_product``, ``team``, ``environment``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#tag CustomAllocationRule#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The single tag value to match.

        Use this field for conditions like ``=``, ``!=``, ``is``, ``is not``, ``like``. Do not use with ``in`` or ``not in`` conditions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#value CustomAllocationRule#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of tag values to match.

        Use this field for ``in`` or ``not in`` conditions only. Do not use with single-value conditions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#values CustomAllocationRule#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomAllocationRuleCostsToAllocate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomAllocationRuleCostsToAllocateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleCostsToAllocateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__594ba58f8d871fea122278e42bb18d65b03f28e196d818e39f7dc551c84b8aad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CustomAllocationRuleCostsToAllocateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31e43f6d238c537731fad487ff1ee4d2df5d733002de2cc396cb3255c8da04cd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CustomAllocationRuleCostsToAllocateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d0342a4e54cff4668f233b5b02449c64abd54a351fa99c18648ff46b548e39e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4c9b4aec44545f2a05b801bd94d5e830a303b961ed224cf94fa6c4eb1d2c15f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4115f4eb41746b708f57190f7c296365da5ea9164cd471e34405567c0b6ec79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleCostsToAllocate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleCostsToAllocate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleCostsToAllocate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa4b43690368842bf55a2396ef373a3e2c431250f435ee17bd004d508658a1ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CustomAllocationRuleCostsToAllocateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleCostsToAllocateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70ad864d5f1fb288fca13d3932a565ac51f0566589613dc5a41c6ddcafed4fd2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "condition"))

    @condition.setter
    def condition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4025c45e1b5508e2b4438bfb7265ae37e507580b039b4c75021816b0bc3e89b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "condition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51f30d3c0466d0c578b6f6805e35599aa38a4ce82e1432eed5f963c2ee38a463)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b546fec8a4bbc9a086be106d60129edbac0566555fdaee89aafa695658785520)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8005b07e6762ed7f83a8755fdc11ab64e023a93601af17934df9faaf6bdaf57a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleCostsToAllocate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleCostsToAllocate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleCostsToAllocate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e065c57079af6dcb22f2594ad6f817b2fd223c3b660e233c41c1c04697e2b4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleStrategy",
    jsii_struct_bases=[],
    name_mapping={
        "allocated_by": "allocatedBy",
        "allocated_by_filters": "allocatedByFilters",
        "allocated_by_tag_keys": "allocatedByTagKeys",
        "based_on_costs": "basedOnCosts",
        "based_on_timeseries": "basedOnTimeseries",
        "evaluate_grouped_by_filters": "evaluateGroupedByFilters",
        "evaluate_grouped_by_tag_keys": "evaluateGroupedByTagKeys",
        "granularity": "granularity",
        "method": "method",
    },
)
class CustomAllocationRuleStrategy:
    def __init__(
        self,
        *,
        allocated_by: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CustomAllocationRuleStrategyAllocatedBy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        allocated_by_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CustomAllocationRuleStrategyAllocatedByFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        allocated_by_tag_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        based_on_costs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CustomAllocationRuleStrategyBasedOnCosts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        based_on_timeseries: typing.Optional[typing.Union["CustomAllocationRuleStrategyBasedOnTimeseries", typing.Dict[builtins.str, typing.Any]]] = None,
        evaluate_grouped_by_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CustomAllocationRuleStrategyEvaluateGroupedByFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        evaluate_grouped_by_tag_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        granularity: typing.Optional[builtins.str] = None,
        method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allocated_by: allocated_by block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#allocated_by CustomAllocationRule#allocated_by}
        :param allocated_by_filters: allocated_by_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#allocated_by_filters CustomAllocationRule#allocated_by_filters}
        :param allocated_by_tag_keys: List of tag keys used to allocate costs (e.g., ``["team", "project"]``). Costs will be distributed across unique values of these tags. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#allocated_by_tag_keys CustomAllocationRule#allocated_by_tag_keys}
        :param based_on_costs: based_on_costs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#based_on_costs CustomAllocationRule#based_on_costs}
        :param based_on_timeseries: based_on_timeseries block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#based_on_timeseries CustomAllocationRule#based_on_timeseries}
        :param evaluate_grouped_by_filters: evaluate_grouped_by_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#evaluate_grouped_by_filters CustomAllocationRule#evaluate_grouped_by_filters}
        :param evaluate_grouped_by_tag_keys: List of tag keys used to group costs before allocation. Costs are grouped by these tag values before applying the allocation strategy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#evaluate_grouped_by_tag_keys CustomAllocationRule#evaluate_grouped_by_tag_keys}
        :param granularity: The granularity level for cost allocation. Valid values are ``daily`` or ``monthly``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#granularity CustomAllocationRule#granularity}
        :param method: The allocation method. Valid values are ``even``, ``proportional``, ``proportional_timeseries``, or ``percent``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#method CustomAllocationRule#method}
        '''
        if isinstance(based_on_timeseries, dict):
            based_on_timeseries = CustomAllocationRuleStrategyBasedOnTimeseries(**based_on_timeseries)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b9048f728f18d4c67ba159c1e1b98f6abebc881c0e3e3764f1a2af8b4dafc86)
            check_type(argname="argument allocated_by", value=allocated_by, expected_type=type_hints["allocated_by"])
            check_type(argname="argument allocated_by_filters", value=allocated_by_filters, expected_type=type_hints["allocated_by_filters"])
            check_type(argname="argument allocated_by_tag_keys", value=allocated_by_tag_keys, expected_type=type_hints["allocated_by_tag_keys"])
            check_type(argname="argument based_on_costs", value=based_on_costs, expected_type=type_hints["based_on_costs"])
            check_type(argname="argument based_on_timeseries", value=based_on_timeseries, expected_type=type_hints["based_on_timeseries"])
            check_type(argname="argument evaluate_grouped_by_filters", value=evaluate_grouped_by_filters, expected_type=type_hints["evaluate_grouped_by_filters"])
            check_type(argname="argument evaluate_grouped_by_tag_keys", value=evaluate_grouped_by_tag_keys, expected_type=type_hints["evaluate_grouped_by_tag_keys"])
            check_type(argname="argument granularity", value=granularity, expected_type=type_hints["granularity"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allocated_by is not None:
            self._values["allocated_by"] = allocated_by
        if allocated_by_filters is not None:
            self._values["allocated_by_filters"] = allocated_by_filters
        if allocated_by_tag_keys is not None:
            self._values["allocated_by_tag_keys"] = allocated_by_tag_keys
        if based_on_costs is not None:
            self._values["based_on_costs"] = based_on_costs
        if based_on_timeseries is not None:
            self._values["based_on_timeseries"] = based_on_timeseries
        if evaluate_grouped_by_filters is not None:
            self._values["evaluate_grouped_by_filters"] = evaluate_grouped_by_filters
        if evaluate_grouped_by_tag_keys is not None:
            self._values["evaluate_grouped_by_tag_keys"] = evaluate_grouped_by_tag_keys
        if granularity is not None:
            self._values["granularity"] = granularity
        if method is not None:
            self._values["method"] = method

    @builtins.property
    def allocated_by(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomAllocationRuleStrategyAllocatedBy"]]]:
        '''allocated_by block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#allocated_by CustomAllocationRule#allocated_by}
        '''
        result = self._values.get("allocated_by")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomAllocationRuleStrategyAllocatedBy"]]], result)

    @builtins.property
    def allocated_by_filters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomAllocationRuleStrategyAllocatedByFilters"]]]:
        '''allocated_by_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#allocated_by_filters CustomAllocationRule#allocated_by_filters}
        '''
        result = self._values.get("allocated_by_filters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomAllocationRuleStrategyAllocatedByFilters"]]], result)

    @builtins.property
    def allocated_by_tag_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of tag keys used to allocate costs (e.g., ``["team", "project"]``). Costs will be distributed across unique values of these tags.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#allocated_by_tag_keys CustomAllocationRule#allocated_by_tag_keys}
        '''
        result = self._values.get("allocated_by_tag_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def based_on_costs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomAllocationRuleStrategyBasedOnCosts"]]]:
        '''based_on_costs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#based_on_costs CustomAllocationRule#based_on_costs}
        '''
        result = self._values.get("based_on_costs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomAllocationRuleStrategyBasedOnCosts"]]], result)

    @builtins.property
    def based_on_timeseries(
        self,
    ) -> typing.Optional["CustomAllocationRuleStrategyBasedOnTimeseries"]:
        '''based_on_timeseries block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#based_on_timeseries CustomAllocationRule#based_on_timeseries}
        '''
        result = self._values.get("based_on_timeseries")
        return typing.cast(typing.Optional["CustomAllocationRuleStrategyBasedOnTimeseries"], result)

    @builtins.property
    def evaluate_grouped_by_filters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomAllocationRuleStrategyEvaluateGroupedByFilters"]]]:
        '''evaluate_grouped_by_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#evaluate_grouped_by_filters CustomAllocationRule#evaluate_grouped_by_filters}
        '''
        result = self._values.get("evaluate_grouped_by_filters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomAllocationRuleStrategyEvaluateGroupedByFilters"]]], result)

    @builtins.property
    def evaluate_grouped_by_tag_keys(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''List of tag keys used to group costs before allocation.

        Costs are grouped by these tag values before applying the allocation strategy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#evaluate_grouped_by_tag_keys CustomAllocationRule#evaluate_grouped_by_tag_keys}
        '''
        result = self._values.get("evaluate_grouped_by_tag_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def granularity(self) -> typing.Optional[builtins.str]:
        '''The granularity level for cost allocation. Valid values are ``daily`` or ``monthly``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#granularity CustomAllocationRule#granularity}
        '''
        result = self._values.get("granularity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''The allocation method. Valid values are ``even``, ``proportional``, ``proportional_timeseries``, or ``percent``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#method CustomAllocationRule#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomAllocationRuleStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleStrategyAllocatedBy",
    jsii_struct_bases=[],
    name_mapping={"allocated_tags": "allocatedTags", "percentage": "percentage"},
)
class CustomAllocationRuleStrategyAllocatedBy:
    def __init__(
        self,
        *,
        allocated_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CustomAllocationRuleStrategyAllocatedByAllocatedTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param allocated_tags: allocated_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#allocated_tags CustomAllocationRule#allocated_tags}
        :param percentage: The percentage of costs to allocate to this target as a decimal (e.g., 0.33 for 33%). Used when ``method`` is ``percent``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#percentage CustomAllocationRule#percentage}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24bae35a44abd8791ef510ad0b6a2c57c75d7db78b43c13fb958fbead165797d)
            check_type(argname="argument allocated_tags", value=allocated_tags, expected_type=type_hints["allocated_tags"])
            check_type(argname="argument percentage", value=percentage, expected_type=type_hints["percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allocated_tags is not None:
            self._values["allocated_tags"] = allocated_tags
        if percentage is not None:
            self._values["percentage"] = percentage

    @builtins.property
    def allocated_tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomAllocationRuleStrategyAllocatedByAllocatedTags"]]]:
        '''allocated_tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#allocated_tags CustomAllocationRule#allocated_tags}
        '''
        result = self._values.get("allocated_tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomAllocationRuleStrategyAllocatedByAllocatedTags"]]], result)

    @builtins.property
    def percentage(self) -> typing.Optional[jsii.Number]:
        '''The percentage of costs to allocate to this target as a decimal (e.g., 0.33 for 33%). Used when ``method`` is ``percent``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#percentage CustomAllocationRule#percentage}
        '''
        result = self._values.get("percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomAllocationRuleStrategyAllocatedBy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleStrategyAllocatedByAllocatedTags",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class CustomAllocationRuleStrategyAllocatedByAllocatedTags:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: The tag key to allocate costs to (e.g., ``team``, ``environment``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#key CustomAllocationRule#key}
        :param value: The tag value to allocate costs to (e.g., ``backend``, ``production``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#value CustomAllocationRule#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dafa604a7e3878c08ef347cfc16e83b9ca7149d75331b9a0f07a0de8e60ca3d)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''The tag key to allocate costs to (e.g., ``team``, ``environment``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#key CustomAllocationRule#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The tag value to allocate costs to (e.g., ``backend``, ``production``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#value CustomAllocationRule#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomAllocationRuleStrategyAllocatedByAllocatedTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomAllocationRuleStrategyAllocatedByAllocatedTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleStrategyAllocatedByAllocatedTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c5562c613dce585ae12569f0cf5cad0bdc6baa44ca4cfc443113f4ad5670c83)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CustomAllocationRuleStrategyAllocatedByAllocatedTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c8b019b3d1699e017c6743686284aef18751543e06cfd5d754f340a786e5d85)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CustomAllocationRuleStrategyAllocatedByAllocatedTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__047fd29daace8d0add3b46323f7228f58a0c4339b2301ea433cd157b6d9adad3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d075add18d5bb9c24fa79dd9f7e8f811e9aa362f9a194ac99acb17dc1ccde3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f60eca4575903343106ca87901e76d2996f9416abf8254da0edc9480b41e1b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyAllocatedByAllocatedTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyAllocatedByAllocatedTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyAllocatedByAllocatedTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4431b9dfd56b220423e406bcd26b004bb802e0ba665341a316a2c02170db6cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CustomAllocationRuleStrategyAllocatedByAllocatedTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleStrategyAllocatedByAllocatedTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__722b9d07b49e279631b91de3d68281db01ae1befe21e880a2a60ec6d7640c46c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b9ffa3b00b7a1bedf01aa00ed9ec956bad473f4ccb8846b19e308544c1bf5e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__167fabc17aea49f9fc04fef6e714c9dd0c72c89597240fbef3a3f1fd956d458d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyAllocatedByAllocatedTags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyAllocatedByAllocatedTags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyAllocatedByAllocatedTags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eff9ca79055852559dd8388369af21c0266759b5c18766492a14e3b1ced0572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleStrategyAllocatedByFilters",
    jsii_struct_bases=[],
    name_mapping={
        "condition": "condition",
        "tag": "tag",
        "value": "value",
        "values": "values",
    },
)
class CustomAllocationRuleStrategyAllocatedByFilters:
    def __init__(
        self,
        *,
        condition: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param condition: The condition to match. Valid values are ``=``, ``!=``, ``is``, ``is not``, ``like``, ``in``, ``not in``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#condition CustomAllocationRule#condition}
        :param tag: The tag key to filter on for allocation targets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#tag CustomAllocationRule#tag}
        :param value: The single tag value to match for allocation. Use with conditions like ``=``, ``!=``, ``is``, ``is not``, ``like``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#value CustomAllocationRule#value}
        :param values: A list of tag values to match for allocation. Use with ``in`` or ``not in`` conditions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#values CustomAllocationRule#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f114c32476ea13b35dae320e0bfc683ed1abd280467e8172883f06aa69cffcb0)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if condition is not None:
            self._values["condition"] = condition
        if tag is not None:
            self._values["tag"] = tag
        if value is not None:
            self._values["value"] = value
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''The condition to match. Valid values are ``=``, ``!=``, ``is``, ``is not``, ``like``, ``in``, ``not in``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#condition CustomAllocationRule#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''The tag key to filter on for allocation targets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#tag CustomAllocationRule#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The single tag value to match for allocation. Use with conditions like ``=``, ``!=``, ``is``, ``is not``, ``like``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#value CustomAllocationRule#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of tag values to match for allocation. Use with ``in`` or ``not in`` conditions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#values CustomAllocationRule#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomAllocationRuleStrategyAllocatedByFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomAllocationRuleStrategyAllocatedByFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleStrategyAllocatedByFiltersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7de79a213c3c5b1dd2f8886396528afc7e53f7157650a6991f0980d901d434c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CustomAllocationRuleStrategyAllocatedByFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b756b9687cf744ad7240aa1961f6e0b83ed6accb9ef5f0e2badd205fa07c566)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CustomAllocationRuleStrategyAllocatedByFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8885703ce8c2abfde549a4000e2b92509a795c9e8be4722e3374f8af0677b7f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db1dd7dd3edbe75b815a3fbb01b9e6d6ed68f7ff73ccb6fcfbcd9aff55ee06d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bff97fcacdaa339bc215bfaa93227fcde3f9a33ef8b00eaa310ab2f43dd4f95e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyAllocatedByFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyAllocatedByFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyAllocatedByFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c27fa4588bf2a4deaa6aa588b9b45ed9348cb432b5c0ebde2abcdc767f3a3d1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CustomAllocationRuleStrategyAllocatedByFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleStrategyAllocatedByFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5aef7d275c49d4a32dac00b4f254ecb308d7232afcd270e48233003f92294563)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "condition"))

    @condition.setter
    def condition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e718ab2e509342ff0f22088eea4008c9e9f01508f58deecaf5fa2b38a35474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "condition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c69ee06f7abdf45b53d983de09a5ee17fc111f017e9d4aa2cc6e6b417d4c4f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f633e22ff8d28a4065a8ee116b613f7a62001d638b2374e04553ff6cbf4e3989)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f76b65e601ed74f31f090ee591efc47c16a0f0e3d2811a1744aa8410225d616)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyAllocatedByFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyAllocatedByFilters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyAllocatedByFilters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f63be3ce92293bb5d40eb42ed12f687b7ff2421dddf9c132672c9d94185e7550)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CustomAllocationRuleStrategyAllocatedByList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleStrategyAllocatedByList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cb1c3413931e223fdd00be63369b9b0f64413a378a349243023a70528fa8350)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CustomAllocationRuleStrategyAllocatedByOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26c93d147b7baff8007a4bac87c04133b07ef77ed1ce98b6ac4bd1588e114534)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CustomAllocationRuleStrategyAllocatedByOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64e4dbd97d8885ce9d31ad12d4a747f1ad4cb9cea2806e41de8b1f5a38df690c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02431fc17314c65d07c375200033a4cd904cf00ae6e905698916d2205cf8cd8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b678ea0b2ccc01dd8c192c1315ed8fbadb9dcab5e41dcdab93557283764dedec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyAllocatedBy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyAllocatedBy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyAllocatedBy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3acca19e7e4fec358e8cbeeaa093f980eb43f04a027ab131659467309401696e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CustomAllocationRuleStrategyAllocatedByOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleStrategyAllocatedByOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d920cc6f6d089a4b55f07591a5f5064d41f6bb96691830581640642cd97ed35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAllocatedTags")
    def put_allocated_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomAllocationRuleStrategyAllocatedByAllocatedTags, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ac3ecc3e5f74f5695fdb75631d1187e1efe6b588cf786736698143a2573baf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllocatedTags", [value]))

    @jsii.member(jsii_name="resetAllocatedTags")
    def reset_allocated_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllocatedTags", []))

    @jsii.member(jsii_name="resetPercentage")
    def reset_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPercentage", []))

    @builtins.property
    @jsii.member(jsii_name="allocatedTags")
    def allocated_tags(
        self,
    ) -> CustomAllocationRuleStrategyAllocatedByAllocatedTagsList:
        return typing.cast(CustomAllocationRuleStrategyAllocatedByAllocatedTagsList, jsii.get(self, "allocatedTags"))

    @builtins.property
    @jsii.member(jsii_name="allocatedTagsInput")
    def allocated_tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyAllocatedByAllocatedTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyAllocatedByAllocatedTags]]], jsii.get(self, "allocatedTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="percentageInput")
    def percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "percentageInput"))

    @builtins.property
    @jsii.member(jsii_name="percentage")
    def percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percentage"))

    @percentage.setter
    def percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f050c99c2c41b341f12b52978f739b097afd25ce049e3944aa7f58d1271b09ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyAllocatedBy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyAllocatedBy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyAllocatedBy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cafb84f96332e9f800996946bd220342551f010c7f6bfbc14ca932db5a4aeb11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleStrategyBasedOnCosts",
    jsii_struct_bases=[],
    name_mapping={
        "condition": "condition",
        "tag": "tag",
        "value": "value",
        "values": "values",
    },
)
class CustomAllocationRuleStrategyBasedOnCosts:
    def __init__(
        self,
        *,
        condition: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param condition: The condition to match. Valid values are ``=``, ``!=``, ``is``, ``is not``, ``like``, ``in``, ``not in``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#condition CustomAllocationRule#condition}
        :param tag: The tag key to use as the basis for cost allocation calculations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#tag CustomAllocationRule#tag}
        :param value: The single tag value to use for cost calculations. Use with conditions like ``=``, ``!=``, ``is``, ``is not``, ``like``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#value CustomAllocationRule#value}
        :param values: A list of tag values to use for cost calculations. Use with ``in`` or ``not in`` conditions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#values CustomAllocationRule#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__691696fae2640a83f4fa354a15648cae1f1071559f39b6292d4cc457bfb0b25b)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if condition is not None:
            self._values["condition"] = condition
        if tag is not None:
            self._values["tag"] = tag
        if value is not None:
            self._values["value"] = value
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''The condition to match. Valid values are ``=``, ``!=``, ``is``, ``is not``, ``like``, ``in``, ``not in``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#condition CustomAllocationRule#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''The tag key to use as the basis for cost allocation calculations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#tag CustomAllocationRule#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The single tag value to use for cost calculations. Use with conditions like ``=``, ``!=``, ``is``, ``is not``, ``like``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#value CustomAllocationRule#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of tag values to use for cost calculations. Use with ``in`` or ``not in`` conditions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#values CustomAllocationRule#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomAllocationRuleStrategyBasedOnCosts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomAllocationRuleStrategyBasedOnCostsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleStrategyBasedOnCostsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d104a0729ccef41e9b15322d8b8ca55373c219748f14ef63ff2c4769cd17f9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CustomAllocationRuleStrategyBasedOnCostsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56f528a7539d82061f87bedf75fa33e42f3beef8ec2d32a1a39d9286321289a4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CustomAllocationRuleStrategyBasedOnCostsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17606b775e3cbc237dd3f1ec64fee5be28a75a9e1f26d9d54d965066c778f57d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cb5d100d12c87c70ffff36c5e2c71eb0c6cfdccbf46c35db8df9b4b54d7effc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a46c61762170338440f9f7dd2226ea559adbb57eec4657987fce4bfe63eb9de0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyBasedOnCosts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyBasedOnCosts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyBasedOnCosts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b782aafb33bc4621cc6345cbac691e8f2f58949918a52d55da7c980344b1fc2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CustomAllocationRuleStrategyBasedOnCostsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleStrategyBasedOnCostsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc9d9b8e510730ca61844b4735f823ba02daa856ba1a8789774bef1892d421d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "condition"))

    @condition.setter
    def condition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a888c41876dd89251fcc597c6247d7caef6c2bc32512b9efa023a652725e01b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "condition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51b5256ac937940db601d960b5805f63f433800679d819f4170bf394a77ac61b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1121dfce13e94d5d6cb956ad9e9f389d64e42beba637a9cf761f6e935334ae6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9035000970c2611abbaa8b22712f93ee1eed491f2a50dce1edd23a457c7e67c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyBasedOnCosts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyBasedOnCosts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyBasedOnCosts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9ab4faaa6c6fb8650bf826fbbb464a153234017d35a53a4b629a4610399b600)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleStrategyBasedOnTimeseries",
    jsii_struct_bases=[],
    name_mapping={},
)
class CustomAllocationRuleStrategyBasedOnTimeseries:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomAllocationRuleStrategyBasedOnTimeseries(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomAllocationRuleStrategyBasedOnTimeseriesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleStrategyBasedOnTimeseriesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac723b991ebeb2a857ad4ea59d40e62a1c72586e3861d5cf232479a5deb79bed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyBasedOnTimeseries]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyBasedOnTimeseries]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyBasedOnTimeseries]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2417aab41b56dbaf943e4a7845c2656b59f649668e0990a2e0d00945cc201fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleStrategyEvaluateGroupedByFilters",
    jsii_struct_bases=[],
    name_mapping={
        "condition": "condition",
        "tag": "tag",
        "value": "value",
        "values": "values",
    },
)
class CustomAllocationRuleStrategyEvaluateGroupedByFilters:
    def __init__(
        self,
        *,
        condition: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param condition: The condition to match. Valid values are ``=``, ``!=``, ``is``, ``is not``, ``like``, ``in``, ``not in``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#condition CustomAllocationRule#condition}
        :param tag: The tag key to filter on when grouping costs for evaluation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#tag CustomAllocationRule#tag}
        :param value: The single tag value to match when grouping. Use with conditions like ``=``, ``!=``, ``is``, ``is not``, ``like``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#value CustomAllocationRule#value}
        :param values: A list of tag values to match when grouping. Use with ``in`` or ``not in`` conditions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#values CustomAllocationRule#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd96eecf97571e2ca3346e5cb6ba103f42e40b50051d5802d232c22652ea259e)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if condition is not None:
            self._values["condition"] = condition
        if tag is not None:
            self._values["tag"] = tag
        if value is not None:
            self._values["value"] = value
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''The condition to match. Valid values are ``=``, ``!=``, ``is``, ``is not``, ``like``, ``in``, ``not in``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#condition CustomAllocationRule#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''The tag key to filter on when grouping costs for evaluation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#tag CustomAllocationRule#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The single tag value to match when grouping. Use with conditions like ``=``, ``!=``, ``is``, ``is not``, ``like``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#value CustomAllocationRule#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of tag values to match when grouping. Use with ``in`` or ``not in`` conditions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/custom_allocation_rule#values CustomAllocationRule#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomAllocationRuleStrategyEvaluateGroupedByFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomAllocationRuleStrategyEvaluateGroupedByFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleStrategyEvaluateGroupedByFiltersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff38a2f04efc00ca4fafeaf4ae282e18fcc22dc58171b733fb7f0da1ddfd0cd8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CustomAllocationRuleStrategyEvaluateGroupedByFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e830a3cf4a13240b7333913d316be143e0aaba79ee284ac62f13fec808ff93c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CustomAllocationRuleStrategyEvaluateGroupedByFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e14a435c75661154a7d4af9b3c3487208b6a0dfef1343287533955d2d21ab655)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e60a23468ab38bbfd9bf6527b0706b5093b67198ed32721b7bb3e8ce0e3e0782)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa0c236082aa52076a6f51e0afa58cee7a544799f1c53052c4b73a56067ffbbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyEvaluateGroupedByFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyEvaluateGroupedByFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyEvaluateGroupedByFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__317bd5c62e11fc1ef9f32141fec39315793f939438bc141a765b8fb1b6214b0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CustomAllocationRuleStrategyEvaluateGroupedByFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleStrategyEvaluateGroupedByFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a7d7d90fb4deaa3f33e808e378a423d4569931d48383116336872bf8e1db27f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "condition"))

    @condition.setter
    def condition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8994c8709c4a26af5e38188f6aaa7ed8fa204dac8237e2a651338afeac99f894)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "condition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65727ed9beb1a844bd192903b4a39ab052e8c9b3e105210ae6b5ef5984f40f33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e876a99ee0acdb2069031299191593c0df63bb2d22cde9e9df26bc3977fee7e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6071b7362157cb2bbd4f6a5132c3e189998119441725ed9185b2057d195f8a0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyEvaluateGroupedByFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyEvaluateGroupedByFilters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyEvaluateGroupedByFilters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b472de951c667dac01a5571392e657b5b8d74e7317f167c40d4e2fb479d063d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CustomAllocationRuleStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.customAllocationRule.CustomAllocationRuleStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__722baeb8636d1bfd302c5b90a2ceb5b628259ea446fe57bd5632b658e7f83e94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAllocatedBy")
    def put_allocated_by(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomAllocationRuleStrategyAllocatedBy, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b0fa76d0b77db690fdf5d641350f5916035991f98b78fba2162636f1b975c01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllocatedBy", [value]))

    @jsii.member(jsii_name="putAllocatedByFilters")
    def put_allocated_by_filters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomAllocationRuleStrategyAllocatedByFilters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc082abfcd26d4f602d74893204a16244d2eeaaebb7adb26171f831c1f2db3ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllocatedByFilters", [value]))

    @jsii.member(jsii_name="putBasedOnCosts")
    def put_based_on_costs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomAllocationRuleStrategyBasedOnCosts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9de690c40bc30f08e954f6ffe92e6e94313e94de00feb2810057a3e08a53a263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBasedOnCosts", [value]))

    @jsii.member(jsii_name="putBasedOnTimeseries")
    def put_based_on_timeseries(self) -> None:
        value = CustomAllocationRuleStrategyBasedOnTimeseries()

        return typing.cast(None, jsii.invoke(self, "putBasedOnTimeseries", [value]))

    @jsii.member(jsii_name="putEvaluateGroupedByFilters")
    def put_evaluate_grouped_by_filters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomAllocationRuleStrategyEvaluateGroupedByFilters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b284b13c2597a4d7288fa83075c01bc2b8b034181dc2c7eef90f71914a17d78e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEvaluateGroupedByFilters", [value]))

    @jsii.member(jsii_name="resetAllocatedBy")
    def reset_allocated_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllocatedBy", []))

    @jsii.member(jsii_name="resetAllocatedByFilters")
    def reset_allocated_by_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllocatedByFilters", []))

    @jsii.member(jsii_name="resetAllocatedByTagKeys")
    def reset_allocated_by_tag_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllocatedByTagKeys", []))

    @jsii.member(jsii_name="resetBasedOnCosts")
    def reset_based_on_costs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasedOnCosts", []))

    @jsii.member(jsii_name="resetEvaluateGroupedByFilters")
    def reset_evaluate_grouped_by_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvaluateGroupedByFilters", []))

    @jsii.member(jsii_name="resetEvaluateGroupedByTagKeys")
    def reset_evaluate_grouped_by_tag_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvaluateGroupedByTagKeys", []))

    @jsii.member(jsii_name="resetGranularity")
    def reset_granularity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGranularity", []))

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @builtins.property
    @jsii.member(jsii_name="allocatedBy")
    def allocated_by(self) -> CustomAllocationRuleStrategyAllocatedByList:
        return typing.cast(CustomAllocationRuleStrategyAllocatedByList, jsii.get(self, "allocatedBy"))

    @builtins.property
    @jsii.member(jsii_name="allocatedByFilters")
    def allocated_by_filters(
        self,
    ) -> CustomAllocationRuleStrategyAllocatedByFiltersList:
        return typing.cast(CustomAllocationRuleStrategyAllocatedByFiltersList, jsii.get(self, "allocatedByFilters"))

    @builtins.property
    @jsii.member(jsii_name="basedOnCosts")
    def based_on_costs(self) -> CustomAllocationRuleStrategyBasedOnCostsList:
        return typing.cast(CustomAllocationRuleStrategyBasedOnCostsList, jsii.get(self, "basedOnCosts"))

    @builtins.property
    @jsii.member(jsii_name="basedOnTimeseries")
    def based_on_timeseries(
        self,
    ) -> CustomAllocationRuleStrategyBasedOnTimeseriesOutputReference:
        return typing.cast(CustomAllocationRuleStrategyBasedOnTimeseriesOutputReference, jsii.get(self, "basedOnTimeseries"))

    @builtins.property
    @jsii.member(jsii_name="evaluateGroupedByFilters")
    def evaluate_grouped_by_filters(
        self,
    ) -> CustomAllocationRuleStrategyEvaluateGroupedByFiltersList:
        return typing.cast(CustomAllocationRuleStrategyEvaluateGroupedByFiltersList, jsii.get(self, "evaluateGroupedByFilters"))

    @builtins.property
    @jsii.member(jsii_name="allocatedByFiltersInput")
    def allocated_by_filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyAllocatedByFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyAllocatedByFilters]]], jsii.get(self, "allocatedByFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="allocatedByInput")
    def allocated_by_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyAllocatedBy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyAllocatedBy]]], jsii.get(self, "allocatedByInput"))

    @builtins.property
    @jsii.member(jsii_name="allocatedByTagKeysInput")
    def allocated_by_tag_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allocatedByTagKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="basedOnCostsInput")
    def based_on_costs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyBasedOnCosts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyBasedOnCosts]]], jsii.get(self, "basedOnCostsInput"))

    @builtins.property
    @jsii.member(jsii_name="basedOnTimeseriesInput")
    def based_on_timeseries_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyBasedOnTimeseries]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyBasedOnTimeseries]], jsii.get(self, "basedOnTimeseriesInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluateGroupedByFiltersInput")
    def evaluate_grouped_by_filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyEvaluateGroupedByFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyEvaluateGroupedByFilters]]], jsii.get(self, "evaluateGroupedByFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluateGroupedByTagKeysInput")
    def evaluate_grouped_by_tag_keys_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "evaluateGroupedByTagKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="granularityInput")
    def granularity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "granularityInput"))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="allocatedByTagKeys")
    def allocated_by_tag_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allocatedByTagKeys"))

    @allocated_by_tag_keys.setter
    def allocated_by_tag_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb3da45d934d1e86824df5876f62eb14d1dbe736fa03d951de1b6999b9d63228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocatedByTagKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="evaluateGroupedByTagKeys")
    def evaluate_grouped_by_tag_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "evaluateGroupedByTagKeys"))

    @evaluate_grouped_by_tag_keys.setter
    def evaluate_grouped_by_tag_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7227b04d910035c799910c8e3a0de24088b0fc01cd4b9502462feb2d9367941d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluateGroupedByTagKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="granularity")
    def granularity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "granularity"))

    @granularity.setter
    def granularity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a49b1519f717e2bd1e6449b1eab7cb408e0fa3215410851d6a9f559d9a8a093)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "granularity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc17afa8ce2e9ef33dd199e5f8e9fd8afc6efecaf25bd6ed70a2cf9d2a4b6e0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbd2838b95ba171d3c42c782ab3122cf3dd2d1d7d121c67e06aecbd9c3ad4b08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CustomAllocationRule",
    "CustomAllocationRuleConfig",
    "CustomAllocationRuleCostsToAllocate",
    "CustomAllocationRuleCostsToAllocateList",
    "CustomAllocationRuleCostsToAllocateOutputReference",
    "CustomAllocationRuleStrategy",
    "CustomAllocationRuleStrategyAllocatedBy",
    "CustomAllocationRuleStrategyAllocatedByAllocatedTags",
    "CustomAllocationRuleStrategyAllocatedByAllocatedTagsList",
    "CustomAllocationRuleStrategyAllocatedByAllocatedTagsOutputReference",
    "CustomAllocationRuleStrategyAllocatedByFilters",
    "CustomAllocationRuleStrategyAllocatedByFiltersList",
    "CustomAllocationRuleStrategyAllocatedByFiltersOutputReference",
    "CustomAllocationRuleStrategyAllocatedByList",
    "CustomAllocationRuleStrategyAllocatedByOutputReference",
    "CustomAllocationRuleStrategyBasedOnCosts",
    "CustomAllocationRuleStrategyBasedOnCostsList",
    "CustomAllocationRuleStrategyBasedOnCostsOutputReference",
    "CustomAllocationRuleStrategyBasedOnTimeseries",
    "CustomAllocationRuleStrategyBasedOnTimeseriesOutputReference",
    "CustomAllocationRuleStrategyEvaluateGroupedByFilters",
    "CustomAllocationRuleStrategyEvaluateGroupedByFiltersList",
    "CustomAllocationRuleStrategyEvaluateGroupedByFiltersOutputReference",
    "CustomAllocationRuleStrategyOutputReference",
]

publication.publish()

def _typecheckingstub__3a8ebde22f4448073601b3cc7672cec499614cd0ebd76c2b7d47c675cfbd32ad(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    providernames: typing.Sequence[builtins.str],
    rule_name: builtins.str,
    costs_to_allocate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomAllocationRuleCostsToAllocate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    strategy: typing.Optional[typing.Union[CustomAllocationRuleStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__acb014525dd058b5ce6a3b5662efef0cdfa84ea6ac7c7f1b67ce3e3a7dfd81b9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__182f38aa609bf8b03d4d0e7b9d7569e78c3006c3381e44a0f3c183341d91a224(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomAllocationRuleCostsToAllocate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3090b7b3bfd273f513729396007ea946e5975485b6e749c20fd07b465719c05(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2297c0d57da21fc95cfd85718f204696632adb3f083f2a00bc168b38366cd979(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12a4650a6f88b72e92784c747c100ab9d43dc8c47b52f1b6d4efbce53b8a9f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0b3e94ca34d201d6e5d68ef18cdc127131ca23c8b701acb8b52ca1b59068250(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    providernames: typing.Sequence[builtins.str],
    rule_name: builtins.str,
    costs_to_allocate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomAllocationRuleCostsToAllocate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    strategy: typing.Optional[typing.Union[CustomAllocationRuleStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82dc23b61caec44ea08aa6a00d556347a6bbeab38ed8f41f32e31b140ef52544(
    *,
    condition: typing.Optional[builtins.str] = None,
    tag: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__594ba58f8d871fea122278e42bb18d65b03f28e196d818e39f7dc551c84b8aad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e43f6d238c537731fad487ff1ee4d2df5d733002de2cc396cb3255c8da04cd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0342a4e54cff4668f233b5b02449c64abd54a351fa99c18648ff46b548e39e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4c9b4aec44545f2a05b801bd94d5e830a303b961ed224cf94fa6c4eb1d2c15f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4115f4eb41746b708f57190f7c296365da5ea9164cd471e34405567c0b6ec79(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa4b43690368842bf55a2396ef373a3e2c431250f435ee17bd004d508658a1ef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleCostsToAllocate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ad864d5f1fb288fca13d3932a565ac51f0566589613dc5a41c6ddcafed4fd2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4025c45e1b5508e2b4438bfb7265ae37e507580b039b4c75021816b0bc3e89b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f30d3c0466d0c578b6f6805e35599aa38a4ce82e1432eed5f963c2ee38a463(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b546fec8a4bbc9a086be106d60129edbac0566555fdaee89aafa695658785520(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8005b07e6762ed7f83a8755fdc11ab64e023a93601af17934df9faaf6bdaf57a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e065c57079af6dcb22f2594ad6f817b2fd223c3b660e233c41c1c04697e2b4f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleCostsToAllocate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b9048f728f18d4c67ba159c1e1b98f6abebc881c0e3e3764f1a2af8b4dafc86(
    *,
    allocated_by: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomAllocationRuleStrategyAllocatedBy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    allocated_by_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomAllocationRuleStrategyAllocatedByFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    allocated_by_tag_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    based_on_costs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomAllocationRuleStrategyBasedOnCosts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    based_on_timeseries: typing.Optional[typing.Union[CustomAllocationRuleStrategyBasedOnTimeseries, typing.Dict[builtins.str, typing.Any]]] = None,
    evaluate_grouped_by_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomAllocationRuleStrategyEvaluateGroupedByFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    evaluate_grouped_by_tag_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    granularity: typing.Optional[builtins.str] = None,
    method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24bae35a44abd8791ef510ad0b6a2c57c75d7db78b43c13fb958fbead165797d(
    *,
    allocated_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomAllocationRuleStrategyAllocatedByAllocatedTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dafa604a7e3878c08ef347cfc16e83b9ca7149d75331b9a0f07a0de8e60ca3d(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c5562c613dce585ae12569f0cf5cad0bdc6baa44ca4cfc443113f4ad5670c83(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8b019b3d1699e017c6743686284aef18751543e06cfd5d754f340a786e5d85(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047fd29daace8d0add3b46323f7228f58a0c4339b2301ea433cd157b6d9adad3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d075add18d5bb9c24fa79dd9f7e8f811e9aa362f9a194ac99acb17dc1ccde3d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f60eca4575903343106ca87901e76d2996f9416abf8254da0edc9480b41e1b6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4431b9dfd56b220423e406bcd26b004bb802e0ba665341a316a2c02170db6cc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyAllocatedByAllocatedTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722b9d07b49e279631b91de3d68281db01ae1befe21e880a2a60ec6d7640c46c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b9ffa3b00b7a1bedf01aa00ed9ec956bad473f4ccb8846b19e308544c1bf5e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__167fabc17aea49f9fc04fef6e714c9dd0c72c89597240fbef3a3f1fd956d458d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eff9ca79055852559dd8388369af21c0266759b5c18766492a14e3b1ced0572(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyAllocatedByAllocatedTags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f114c32476ea13b35dae320e0bfc683ed1abd280467e8172883f06aa69cffcb0(
    *,
    condition: typing.Optional[builtins.str] = None,
    tag: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7de79a213c3c5b1dd2f8886396528afc7e53f7157650a6991f0980d901d434c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b756b9687cf744ad7240aa1961f6e0b83ed6accb9ef5f0e2badd205fa07c566(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8885703ce8c2abfde549a4000e2b92509a795c9e8be4722e3374f8af0677b7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1dd7dd3edbe75b815a3fbb01b9e6d6ed68f7ff73ccb6fcfbcd9aff55ee06d4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bff97fcacdaa339bc215bfaa93227fcde3f9a33ef8b00eaa310ab2f43dd4f95e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27fa4588bf2a4deaa6aa588b9b45ed9348cb432b5c0ebde2abcdc767f3a3d1b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyAllocatedByFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aef7d275c49d4a32dac00b4f254ecb308d7232afcd270e48233003f92294563(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e718ab2e509342ff0f22088eea4008c9e9f01508f58deecaf5fa2b38a35474(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c69ee06f7abdf45b53d983de09a5ee17fc111f017e9d4aa2cc6e6b417d4c4f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f633e22ff8d28a4065a8ee116b613f7a62001d638b2374e04553ff6cbf4e3989(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f76b65e601ed74f31f090ee591efc47c16a0f0e3d2811a1744aa8410225d616(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f63be3ce92293bb5d40eb42ed12f687b7ff2421dddf9c132672c9d94185e7550(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyAllocatedByFilters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb1c3413931e223fdd00be63369b9b0f64413a378a349243023a70528fa8350(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c93d147b7baff8007a4bac87c04133b07ef77ed1ce98b6ac4bd1588e114534(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e4dbd97d8885ce9d31ad12d4a747f1ad4cb9cea2806e41de8b1f5a38df690c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02431fc17314c65d07c375200033a4cd904cf00ae6e905698916d2205cf8cd8b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b678ea0b2ccc01dd8c192c1315ed8fbadb9dcab5e41dcdab93557283764dedec(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3acca19e7e4fec358e8cbeeaa093f980eb43f04a027ab131659467309401696e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyAllocatedBy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d920cc6f6d089a4b55f07591a5f5064d41f6bb96691830581640642cd97ed35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ac3ecc3e5f74f5695fdb75631d1187e1efe6b588cf786736698143a2573baf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomAllocationRuleStrategyAllocatedByAllocatedTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f050c99c2c41b341f12b52978f739b097afd25ce049e3944aa7f58d1271b09ff(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cafb84f96332e9f800996946bd220342551f010c7f6bfbc14ca932db5a4aeb11(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyAllocatedBy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__691696fae2640a83f4fa354a15648cae1f1071559f39b6292d4cc457bfb0b25b(
    *,
    condition: typing.Optional[builtins.str] = None,
    tag: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d104a0729ccef41e9b15322d8b8ca55373c219748f14ef63ff2c4769cd17f9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56f528a7539d82061f87bedf75fa33e42f3beef8ec2d32a1a39d9286321289a4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17606b775e3cbc237dd3f1ec64fee5be28a75a9e1f26d9d54d965066c778f57d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb5d100d12c87c70ffff36c5e2c71eb0c6cfdccbf46c35db8df9b4b54d7effc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a46c61762170338440f9f7dd2226ea559adbb57eec4657987fce4bfe63eb9de0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b782aafb33bc4621cc6345cbac691e8f2f58949918a52d55da7c980344b1fc2d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyBasedOnCosts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc9d9b8e510730ca61844b4735f823ba02daa856ba1a8789774bef1892d421d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a888c41876dd89251fcc597c6247d7caef6c2bc32512b9efa023a652725e01b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51b5256ac937940db601d960b5805f63f433800679d819f4170bf394a77ac61b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1121dfce13e94d5d6cb956ad9e9f389d64e42beba637a9cf761f6e935334ae6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9035000970c2611abbaa8b22712f93ee1eed491f2a50dce1edd23a457c7e67c0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9ab4faaa6c6fb8650bf826fbbb464a153234017d35a53a4b629a4610399b600(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyBasedOnCosts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac723b991ebeb2a857ad4ea59d40e62a1c72586e3861d5cf232479a5deb79bed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2417aab41b56dbaf943e4a7845c2656b59f649668e0990a2e0d00945cc201fc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyBasedOnTimeseries]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd96eecf97571e2ca3346e5cb6ba103f42e40b50051d5802d232c22652ea259e(
    *,
    condition: typing.Optional[builtins.str] = None,
    tag: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff38a2f04efc00ca4fafeaf4ae282e18fcc22dc58171b733fb7f0da1ddfd0cd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e830a3cf4a13240b7333913d316be143e0aaba79ee284ac62f13fec808ff93c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14a435c75661154a7d4af9b3c3487208b6a0dfef1343287533955d2d21ab655(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e60a23468ab38bbfd9bf6527b0706b5093b67198ed32721b7bb3e8ce0e3e0782(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0c236082aa52076a6f51e0afa58cee7a544799f1c53052c4b73a56067ffbbf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__317bd5c62e11fc1ef9f32141fec39315793f939438bc141a765b8fb1b6214b0c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomAllocationRuleStrategyEvaluateGroupedByFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7d7d90fb4deaa3f33e808e378a423d4569931d48383116336872bf8e1db27f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8994c8709c4a26af5e38188f6aaa7ed8fa204dac8237e2a651338afeac99f894(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65727ed9beb1a844bd192903b4a39ab052e8c9b3e105210ae6b5ef5984f40f33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e876a99ee0acdb2069031299191593c0df63bb2d22cde9e9df26bc3977fee7e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6071b7362157cb2bbd4f6a5132c3e189998119441725ed9185b2057d195f8a0c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b472de951c667dac01a5571392e657b5b8d74e7317f167c40d4e2fb479d063d8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategyEvaluateGroupedByFilters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722baeb8636d1bfd302c5b90a2ceb5b628259ea446fe57bd5632b658e7f83e94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b0fa76d0b77db690fdf5d641350f5916035991f98b78fba2162636f1b975c01(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomAllocationRuleStrategyAllocatedBy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc082abfcd26d4f602d74893204a16244d2eeaaebb7adb26171f831c1f2db3ab(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomAllocationRuleStrategyAllocatedByFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de690c40bc30f08e954f6ffe92e6e94313e94de00feb2810057a3e08a53a263(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomAllocationRuleStrategyBasedOnCosts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b284b13c2597a4d7288fa83075c01bc2b8b034181dc2c7eef90f71914a17d78e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomAllocationRuleStrategyEvaluateGroupedByFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb3da45d934d1e86824df5876f62eb14d1dbe736fa03d951de1b6999b9d63228(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7227b04d910035c799910c8e3a0de24088b0fc01cd4b9502462feb2d9367941d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a49b1519f717e2bd1e6449b1eab7cb408e0fa3215410851d6a9f559d9a8a093(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc17afa8ce2e9ef33dd199e5f8e9fd8afc6efecaf25bd6ed70a2cf9d2a4b6e0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbd2838b95ba171d3c42c782ab3122cf3dd2d1d7d121c67e06aecbd9c3ad4b08(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomAllocationRuleStrategy]],
) -> None:
    """Type checking stubs"""
    pass
