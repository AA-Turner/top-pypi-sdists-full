r'''
# `datadog_cost_budget`

Refer to the Terraform Registry for docs: [`datadog_cost_budget`](https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget).
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


class CostBudget(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.costBudget.CostBudget",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget datadog_cost_budget}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        end_month: jsii.Number,
        metrics_query: builtins.str,
        name: builtins.str,
        start_month: jsii.Number,
        entries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CostBudgetEntries", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget datadog_cost_budget} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param end_month: The month when the budget ends (YYYYMM). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#end_month CostBudget#end_month}
        :param metrics_query: The cost query used to track against the budget. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#metrics_query CostBudget#metrics_query}
        :param name: The name of the budget. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#name CostBudget#name}
        :param start_month: The month when the budget starts (YYYYMM). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#start_month CostBudget#start_month}
        :param entries: entries block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#entries CostBudget#entries}
        :param id: The ID of the budget. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#id CostBudget#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f3471df32c1f536a98611990fc050edffc35f0365b84bdd001456e0f1cf0743)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CostBudgetConfig(
            end_month=end_month,
            metrics_query=metrics_query,
            name=name,
            start_month=start_month,
            entries=entries,
            id=id,
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
        '''Generates CDKTF code for importing a CostBudget resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CostBudget to import.
        :param import_from_id: The id of the existing CostBudget that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CostBudget to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09cae8f491b84e84bdf75d4b2200c85f9e289b4799d8f6eca0d6b68ae5124635)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEntries")
    def put_entries(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CostBudgetEntries", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87edb7ee2d1321fbcd847459e9457929884a2a62382d6bafaf83c279ff694ec4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEntries", [value]))

    @jsii.member(jsii_name="resetEntries")
    def reset_entries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntries", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="entries")
    def entries(self) -> "CostBudgetEntriesList":
        return typing.cast("CostBudgetEntriesList", jsii.get(self, "entries"))

    @builtins.property
    @jsii.member(jsii_name="totalAmount")
    def total_amount(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalAmount"))

    @builtins.property
    @jsii.member(jsii_name="endMonthInput")
    def end_month_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "endMonthInput"))

    @builtins.property
    @jsii.member(jsii_name="entriesInput")
    def entries_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CostBudgetEntries"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CostBudgetEntries"]]], jsii.get(self, "entriesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsQueryInput")
    def metrics_query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricsQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="startMonthInput")
    def start_month_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startMonthInput"))

    @builtins.property
    @jsii.member(jsii_name="endMonth")
    def end_month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "endMonth"))

    @end_month.setter
    def end_month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40363f64772dd4092c5cfade6c634a86e78deebe6e33f443cba07c97858b9f98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endMonth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ead92430bde77322b9e12b511530041f6b3a8cdfd0a5531d05ce13f6e25e1c5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsQuery")
    def metrics_query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricsQuery"))

    @metrics_query.setter
    def metrics_query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__291e5f54d61e83ba68e22c30dd0b2218215192294927e2bee2846af52cd01fcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsQuery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66e28fbec37c73a375c5c8dea82c91b3a9fa74bae71fb23cbee25441afd0def2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startMonth")
    def start_month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startMonth"))

    @start_month.setter
    def start_month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ab568bf19c918f8f793c9239e764eeae1a78faab0cb9ac6c0672d129e9e7d47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startMonth", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.costBudget.CostBudgetConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "end_month": "endMonth",
        "metrics_query": "metricsQuery",
        "name": "name",
        "start_month": "startMonth",
        "entries": "entries",
        "id": "id",
    },
)
class CostBudgetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        end_month: jsii.Number,
        metrics_query: builtins.str,
        name: builtins.str,
        start_month: jsii.Number,
        entries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CostBudgetEntries", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param end_month: The month when the budget ends (YYYYMM). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#end_month CostBudget#end_month}
        :param metrics_query: The cost query used to track against the budget. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#metrics_query CostBudget#metrics_query}
        :param name: The name of the budget. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#name CostBudget#name}
        :param start_month: The month when the budget starts (YYYYMM). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#start_month CostBudget#start_month}
        :param entries: entries block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#entries CostBudget#entries}
        :param id: The ID of the budget. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#id CostBudget#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46cd1b66e872d85ca4135909dbb609337a202d01780632b5e1e7dd06a873d213)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument end_month", value=end_month, expected_type=type_hints["end_month"])
            check_type(argname="argument metrics_query", value=metrics_query, expected_type=type_hints["metrics_query"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument start_month", value=start_month, expected_type=type_hints["start_month"])
            check_type(argname="argument entries", value=entries, expected_type=type_hints["entries"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_month": end_month,
            "metrics_query": metrics_query,
            "name": name,
            "start_month": start_month,
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
        if entries is not None:
            self._values["entries"] = entries
        if id is not None:
            self._values["id"] = id

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
    def end_month(self) -> jsii.Number:
        '''The month when the budget ends (YYYYMM).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#end_month CostBudget#end_month}
        '''
        result = self._values.get("end_month")
        assert result is not None, "Required property 'end_month' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def metrics_query(self) -> builtins.str:
        '''The cost query used to track against the budget.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#metrics_query CostBudget#metrics_query}
        '''
        result = self._values.get("metrics_query")
        assert result is not None, "Required property 'metrics_query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the budget.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#name CostBudget#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_month(self) -> jsii.Number:
        '''The month when the budget starts (YYYYMM).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#start_month CostBudget#start_month}
        '''
        result = self._values.get("start_month")
        assert result is not None, "Required property 'start_month' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def entries(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CostBudgetEntries"]]]:
        '''entries block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#entries CostBudget#entries}
        '''
        result = self._values.get("entries")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CostBudgetEntries"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''The ID of the budget.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#id CostBudget#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CostBudgetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.costBudget.CostBudgetEntries",
    jsii_struct_bases=[],
    name_mapping={"amount": "amount", "month": "month", "tag_filters": "tagFilters"},
)
class CostBudgetEntries:
    def __init__(
        self,
        *,
        amount: jsii.Number,
        month: jsii.Number,
        tag_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CostBudgetEntriesTagFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param amount: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#amount CostBudget#amount}.
        :param month: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#month CostBudget#month}.
        :param tag_filters: tag_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#tag_filters CostBudget#tag_filters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c6abb02a0745bf03525845858cf9516ae69025177b7f297c0616c1c03faceb3)
            check_type(argname="argument amount", value=amount, expected_type=type_hints["amount"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument tag_filters", value=tag_filters, expected_type=type_hints["tag_filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "amount": amount,
            "month": month,
        }
        if tag_filters is not None:
            self._values["tag_filters"] = tag_filters

    @builtins.property
    def amount(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#amount CostBudget#amount}.'''
        result = self._values.get("amount")
        assert result is not None, "Required property 'amount' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def month(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#month CostBudget#month}.'''
        result = self._values.get("month")
        assert result is not None, "Required property 'month' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def tag_filters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CostBudgetEntriesTagFilters"]]]:
        '''tag_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#tag_filters CostBudget#tag_filters}
        '''
        result = self._values.get("tag_filters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CostBudgetEntriesTagFilters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CostBudgetEntries(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CostBudgetEntriesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.costBudget.CostBudgetEntriesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3578a669eda23a2fba9223d05b84022e255f4c78f69a4662a9b3c1e95ab3ecc2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CostBudgetEntriesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3dbc1e40026248847a15af4f2fe1abedbff73852090576547b8a72c98e19026)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CostBudgetEntriesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9184a8262aec0f3cfeac4178734673660ec7c1757014c708ed6984cf29c31b34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e31985f8ad7a068a3eb2d2f4459623985ff529669342ddb60d01e4094ab0f46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a531260031601c0b7fc1ef0ba554bd68adde5816edf2cd757afba5b884947fa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CostBudgetEntries]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CostBudgetEntries]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CostBudgetEntries]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26f86b6aac5e1c491a27518171d5a443615c4323fc4719e5c7b49e5782324690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CostBudgetEntriesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.costBudget.CostBudgetEntriesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__438567174ca64dba2090eec83a379edc6c7e85d288c7176da91381d8ba1260f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTagFilters")
    def put_tag_filters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CostBudgetEntriesTagFilters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68f78f15a4fbe788f919e9ae73df42f60995410af783639cdd7c3ccca0ab7ef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTagFilters", [value]))

    @jsii.member(jsii_name="resetTagFilters")
    def reset_tag_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagFilters", []))

    @builtins.property
    @jsii.member(jsii_name="tagFilters")
    def tag_filters(self) -> "CostBudgetEntriesTagFiltersList":
        return typing.cast("CostBudgetEntriesTagFiltersList", jsii.get(self, "tagFilters"))

    @builtins.property
    @jsii.member(jsii_name="amountInput")
    def amount_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "amountInput"))

    @builtins.property
    @jsii.member(jsii_name="monthInput")
    def month_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthInput"))

    @builtins.property
    @jsii.member(jsii_name="tagFiltersInput")
    def tag_filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CostBudgetEntriesTagFilters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CostBudgetEntriesTagFilters"]]], jsii.get(self, "tagFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="amount")
    def amount(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "amount"))

    @amount.setter
    def amount(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e11e57ab44bd8e841ad65ea4413d07a1d4056a3b8c5a9ec0c101c09c6dc6f4e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "amount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2481de66893200affa5ae242626700ecd74281b89fd6a09bd11ba6d195993aa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CostBudgetEntries]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CostBudgetEntries]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CostBudgetEntries]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1871ed9ea2c1d75b0e1e471fa55c3c24564876fe13db8b1e12ee9ebd91574e62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.costBudget.CostBudgetEntriesTagFilters",
    jsii_struct_bases=[],
    name_mapping={"tag_key": "tagKey", "tag_value": "tagValue"},
)
class CostBudgetEntriesTagFilters:
    def __init__(self, *, tag_key: builtins.str, tag_value: builtins.str) -> None:
        '''
        :param tag_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#tag_key CostBudget#tag_key}.
        :param tag_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#tag_value CostBudget#tag_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02fedae8e6f288fda0ce87974dc9b98594864cbde25be6c73703b559b93a8bc9)
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tag_key": tag_key,
            "tag_value": tag_value,
        }

    @builtins.property
    def tag_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#tag_key CostBudget#tag_key}.'''
        result = self._values.get("tag_key")
        assert result is not None, "Required property 'tag_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/cost_budget#tag_value CostBudget#tag_value}.'''
        result = self._values.get("tag_value")
        assert result is not None, "Required property 'tag_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CostBudgetEntriesTagFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CostBudgetEntriesTagFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.costBudget.CostBudgetEntriesTagFiltersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b842faaabb941bc69b90b044f531e08337c36d40ebe63161db2c2afcddd2a912)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CostBudgetEntriesTagFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd0c62d6d3a6ae50bdce4d041632b7ed7c142e22f00fb14d01e606714294e06f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CostBudgetEntriesTagFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__718f4c1878a6d307fc8a7d1c18624cfa15f9ae1874cf945aa317f698da59c5eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6eae8bffc820b2ba6f94c9215fdc3ba76641c99fa36d30556359c5bb9754c21)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf307e8492955ece42b0fae12f3ff6a87f7b2b0f998e5f8e23d1bbda231997bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CostBudgetEntriesTagFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CostBudgetEntriesTagFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CostBudgetEntriesTagFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d842277174478346eafb5131412a6a93ec69e007f7282ec43a8c9f74339f66a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CostBudgetEntriesTagFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.costBudget.CostBudgetEntriesTagFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__baede691fe15968f9c28df7a6c68576ad237158bd2a19f0908ba249ac87a938e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__752b25807bf87109b4e137fddecfb2b58d22e42db9acf611cfab750bd21f8635)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bd33470b592887117c30363627bb3d1368c1ea439a6dbb405b3d05ce0b14e51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CostBudgetEntriesTagFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CostBudgetEntriesTagFilters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CostBudgetEntriesTagFilters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fe4a3dcca89085d4de3b5963bf050231e5fe46a6338deee3810ced990760049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CostBudget",
    "CostBudgetConfig",
    "CostBudgetEntries",
    "CostBudgetEntriesList",
    "CostBudgetEntriesOutputReference",
    "CostBudgetEntriesTagFilters",
    "CostBudgetEntriesTagFiltersList",
    "CostBudgetEntriesTagFiltersOutputReference",
]

publication.publish()

def _typecheckingstub__7f3471df32c1f536a98611990fc050edffc35f0365b84bdd001456e0f1cf0743(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    end_month: jsii.Number,
    metrics_query: builtins.str,
    name: builtins.str,
    start_month: jsii.Number,
    entries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CostBudgetEntries, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__09cae8f491b84e84bdf75d4b2200c85f9e289b4799d8f6eca0d6b68ae5124635(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87edb7ee2d1321fbcd847459e9457929884a2a62382d6bafaf83c279ff694ec4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CostBudgetEntries, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40363f64772dd4092c5cfade6c634a86e78deebe6e33f443cba07c97858b9f98(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ead92430bde77322b9e12b511530041f6b3a8cdfd0a5531d05ce13f6e25e1c5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291e5f54d61e83ba68e22c30dd0b2218215192294927e2bee2846af52cd01fcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66e28fbec37c73a375c5c8dea82c91b3a9fa74bae71fb23cbee25441afd0def2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab568bf19c918f8f793c9239e764eeae1a78faab0cb9ac6c0672d129e9e7d47(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46cd1b66e872d85ca4135909dbb609337a202d01780632b5e1e7dd06a873d213(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    end_month: jsii.Number,
    metrics_query: builtins.str,
    name: builtins.str,
    start_month: jsii.Number,
    entries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CostBudgetEntries, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c6abb02a0745bf03525845858cf9516ae69025177b7f297c0616c1c03faceb3(
    *,
    amount: jsii.Number,
    month: jsii.Number,
    tag_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CostBudgetEntriesTagFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3578a669eda23a2fba9223d05b84022e255f4c78f69a4662a9b3c1e95ab3ecc2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3dbc1e40026248847a15af4f2fe1abedbff73852090576547b8a72c98e19026(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9184a8262aec0f3cfeac4178734673660ec7c1757014c708ed6984cf29c31b34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e31985f8ad7a068a3eb2d2f4459623985ff529669342ddb60d01e4094ab0f46(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a531260031601c0b7fc1ef0ba554bd68adde5816edf2cd757afba5b884947fa7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26f86b6aac5e1c491a27518171d5a443615c4323fc4719e5c7b49e5782324690(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CostBudgetEntries]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__438567174ca64dba2090eec83a379edc6c7e85d288c7176da91381d8ba1260f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68f78f15a4fbe788f919e9ae73df42f60995410af783639cdd7c3ccca0ab7ef5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CostBudgetEntriesTagFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e11e57ab44bd8e841ad65ea4413d07a1d4056a3b8c5a9ec0c101c09c6dc6f4e7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2481de66893200affa5ae242626700ecd74281b89fd6a09bd11ba6d195993aa9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1871ed9ea2c1d75b0e1e471fa55c3c24564876fe13db8b1e12ee9ebd91574e62(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CostBudgetEntries]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02fedae8e6f288fda0ce87974dc9b98594864cbde25be6c73703b559b93a8bc9(
    *,
    tag_key: builtins.str,
    tag_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b842faaabb941bc69b90b044f531e08337c36d40ebe63161db2c2afcddd2a912(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd0c62d6d3a6ae50bdce4d041632b7ed7c142e22f00fb14d01e606714294e06f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718f4c1878a6d307fc8a7d1c18624cfa15f9ae1874cf945aa317f698da59c5eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6eae8bffc820b2ba6f94c9215fdc3ba76641c99fa36d30556359c5bb9754c21(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf307e8492955ece42b0fae12f3ff6a87f7b2b0f998e5f8e23d1bbda231997bc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d842277174478346eafb5131412a6a93ec69e007f7282ec43a8c9f74339f66a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CostBudgetEntriesTagFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baede691fe15968f9c28df7a6c68576ad237158bd2a19f0908ba249ac87a938e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__752b25807bf87109b4e137fddecfb2b58d22e42db9acf611cfab750bd21f8635(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd33470b592887117c30363627bb3d1368c1ea439a6dbb405b3d05ce0b14e51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe4a3dcca89085d4de3b5963bf050231e5fe46a6338deee3810ced990760049(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CostBudgetEntriesTagFilters]],
) -> None:
    """Type checking stubs"""
    pass
