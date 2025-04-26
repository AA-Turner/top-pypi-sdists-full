r'''
# `datadog_rum_metric`

Refer to the Terraform Registry for docs: [`datadog_rum_metric`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric).
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


class RumMetric(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.rumMetric.RumMetric",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric datadog_rum_metric}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        event_type: builtins.str,
        name: builtins.str,
        compute: typing.Optional[typing.Union["RumMetricCompute", typing.Dict[builtins.str, typing.Any]]] = None,
        filter: typing.Optional[typing.Union["RumMetricFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        group_by: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RumMetricGroupBy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        uniqueness: typing.Optional[typing.Union["RumMetricUniqueness", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric datadog_rum_metric} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param event_type: The type of RUM events to filter on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#event_type RumMetric#event_type}
        :param name: The name of the RUM-based metric. This field can't be updated after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#name RumMetric#name}
        :param compute: compute block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#compute RumMetric#compute}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#filter RumMetric#filter}
        :param group_by: group_by block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#group_by RumMetric#group_by}
        :param uniqueness: uniqueness block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#uniqueness RumMetric#uniqueness}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5ea56942a801b5240ca57c2b8937e058b2298e21c8635ed345f993262862b9d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = RumMetricConfig(
            event_type=event_type,
            name=name,
            compute=compute,
            filter=filter,
            group_by=group_by,
            uniqueness=uniqueness,
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
        '''Generates CDKTF code for importing a RumMetric resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RumMetric to import.
        :param import_from_id: The id of the existing RumMetric that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RumMetric to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cc13eeb8e730ec127b798c41d56bebb9849d331bea2ba679a37319bdb02e843)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCompute")
    def put_compute(
        self,
        *,
        aggregation_type: builtins.str,
        include_percentiles: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aggregation_type: The type of aggregation to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#aggregation_type RumMetric#aggregation_type}
        :param include_percentiles: Toggle to include or exclude percentile aggregations for distribution metrics. Only present when ``aggregation_type`` is ``distribution``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#include_percentiles RumMetric#include_percentiles}
        :param path: The path to the value the RUM-based metric will aggregate on. Only present when ``aggregation_type`` is ``distribution``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#path RumMetric#path}
        '''
        value = RumMetricCompute(
            aggregation_type=aggregation_type,
            include_percentiles=include_percentiles,
            path=path,
        )

        return typing.cast(None, jsii.invoke(self, "putCompute", [value]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(self, *, query: typing.Optional[builtins.str] = None) -> None:
        '''
        :param query: The search query. Follows RUM search syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#query RumMetric#query}
        '''
        value = RumMetricFilter(query=query)

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putGroupBy")
    def put_group_by(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RumMetricGroupBy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38555a5c3bed11e39a8ab41d0aaf59f55baa0ed2f59e34d62494eb98083d1d79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGroupBy", [value]))

    @jsii.member(jsii_name="putUniqueness")
    def put_uniqueness(self, *, when: typing.Optional[builtins.str] = None) -> None:
        '''
        :param when: When to count updatable events. ``match`` when the event is first seen, or ``end`` when the event is complete. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#when RumMetric#when}
        '''
        value = RumMetricUniqueness(when=when)

        return typing.cast(None, jsii.invoke(self, "putUniqueness", [value]))

    @jsii.member(jsii_name="resetCompute")
    def reset_compute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompute", []))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetGroupBy")
    def reset_group_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupBy", []))

    @jsii.member(jsii_name="resetUniqueness")
    def reset_uniqueness(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUniqueness", []))

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
    @jsii.member(jsii_name="compute")
    def compute(self) -> "RumMetricComputeOutputReference":
        return typing.cast("RumMetricComputeOutputReference", jsii.get(self, "compute"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> "RumMetricFilterOutputReference":
        return typing.cast("RumMetricFilterOutputReference", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="groupBy")
    def group_by(self) -> "RumMetricGroupByList":
        return typing.cast("RumMetricGroupByList", jsii.get(self, "groupBy"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="uniqueness")
    def uniqueness(self) -> "RumMetricUniquenessOutputReference":
        return typing.cast("RumMetricUniquenessOutputReference", jsii.get(self, "uniqueness"))

    @builtins.property
    @jsii.member(jsii_name="computeInput")
    def compute_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RumMetricCompute"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RumMetricCompute"]], jsii.get(self, "computeInput"))

    @builtins.property
    @jsii.member(jsii_name="eventTypeInput")
    def event_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RumMetricFilter"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RumMetricFilter"]], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="groupByInput")
    def group_by_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RumMetricGroupBy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RumMetricGroupBy"]]], jsii.get(self, "groupByInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="uniquenessInput")
    def uniqueness_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RumMetricUniqueness"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RumMetricUniqueness"]], jsii.get(self, "uniquenessInput"))

    @builtins.property
    @jsii.member(jsii_name="eventType")
    def event_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventType"))

    @event_type.setter
    def event_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1b0bc51613a31e2e583b906c431b9d94198b01bc7cc5695f9857dea154c2953)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bcda8e38f79ae82955cb035853fc0b5d9a8f2925836964faf9f76ec01ea7705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.rumMetric.RumMetricCompute",
    jsii_struct_bases=[],
    name_mapping={
        "aggregation_type": "aggregationType",
        "include_percentiles": "includePercentiles",
        "path": "path",
    },
)
class RumMetricCompute:
    def __init__(
        self,
        *,
        aggregation_type: builtins.str,
        include_percentiles: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aggregation_type: The type of aggregation to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#aggregation_type RumMetric#aggregation_type}
        :param include_percentiles: Toggle to include or exclude percentile aggregations for distribution metrics. Only present when ``aggregation_type`` is ``distribution``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#include_percentiles RumMetric#include_percentiles}
        :param path: The path to the value the RUM-based metric will aggregate on. Only present when ``aggregation_type`` is ``distribution``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#path RumMetric#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13940534ba6f3d7f0044cb6aedd304c8174e8f6909506720904427ca8e073e87)
            check_type(argname="argument aggregation_type", value=aggregation_type, expected_type=type_hints["aggregation_type"])
            check_type(argname="argument include_percentiles", value=include_percentiles, expected_type=type_hints["include_percentiles"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aggregation_type": aggregation_type,
        }
        if include_percentiles is not None:
            self._values["include_percentiles"] = include_percentiles
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def aggregation_type(self) -> builtins.str:
        '''The type of aggregation to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#aggregation_type RumMetric#aggregation_type}
        '''
        result = self._values.get("aggregation_type")
        assert result is not None, "Required property 'aggregation_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include_percentiles(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Toggle to include or exclude percentile aggregations for distribution metrics. Only present when ``aggregation_type`` is ``distribution``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#include_percentiles RumMetric#include_percentiles}
        '''
        result = self._values.get("include_percentiles")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the value the RUM-based metric will aggregate on. Only present when ``aggregation_type`` is ``distribution``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#path RumMetric#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RumMetricCompute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RumMetricComputeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.rumMetric.RumMetricComputeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b24e62bb99f7dc65ff1fe1a015d482c6be66bacba53a0acdfe738d84c9f4b627)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludePercentiles")
    def reset_include_percentiles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludePercentiles", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="aggregationTypeInput")
    def aggregation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aggregationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="includePercentilesInput")
    def include_percentiles_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includePercentilesInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregationType")
    def aggregation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aggregationType"))

    @aggregation_type.setter
    def aggregation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1917112847c1ec09b2e41b79f68d8687a508d3c6bcdffcb46a4268d2c601d20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includePercentiles")
    def include_percentiles(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includePercentiles"))

    @include_percentiles.setter
    def include_percentiles(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b6accbf67cf379537b6a93e71791f53fd4e62f9fb2a9d26a60fb8b3e07d9a18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includePercentiles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0004f7ece1d035a8ad08da551fe2553e147ef99763c1a0e68afa4426df9cb57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RumMetricCompute]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RumMetricCompute]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RumMetricCompute]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0ba133008d98556d570c406386bb2fbeef1f032410ca42c7dfefe47cd8d1355)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.rumMetric.RumMetricConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "event_type": "eventType",
        "name": "name",
        "compute": "compute",
        "filter": "filter",
        "group_by": "groupBy",
        "uniqueness": "uniqueness",
    },
)
class RumMetricConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        event_type: builtins.str,
        name: builtins.str,
        compute: typing.Optional[typing.Union[RumMetricCompute, typing.Dict[builtins.str, typing.Any]]] = None,
        filter: typing.Optional[typing.Union["RumMetricFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        group_by: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RumMetricGroupBy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        uniqueness: typing.Optional[typing.Union["RumMetricUniqueness", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param event_type: The type of RUM events to filter on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#event_type RumMetric#event_type}
        :param name: The name of the RUM-based metric. This field can't be updated after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#name RumMetric#name}
        :param compute: compute block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#compute RumMetric#compute}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#filter RumMetric#filter}
        :param group_by: group_by block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#group_by RumMetric#group_by}
        :param uniqueness: uniqueness block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#uniqueness RumMetric#uniqueness}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(compute, dict):
            compute = RumMetricCompute(**compute)
        if isinstance(filter, dict):
            filter = RumMetricFilter(**filter)
        if isinstance(uniqueness, dict):
            uniqueness = RumMetricUniqueness(**uniqueness)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be5da0eb6f71ac9e1f29e73061c2a5cdf1067a7c20c5efb26958eb6ee1975add)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument compute", value=compute, expected_type=type_hints["compute"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument group_by", value=group_by, expected_type=type_hints["group_by"])
            check_type(argname="argument uniqueness", value=uniqueness, expected_type=type_hints["uniqueness"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_type": event_type,
            "name": name,
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
        if compute is not None:
            self._values["compute"] = compute
        if filter is not None:
            self._values["filter"] = filter
        if group_by is not None:
            self._values["group_by"] = group_by
        if uniqueness is not None:
            self._values["uniqueness"] = uniqueness

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
    def event_type(self) -> builtins.str:
        '''The type of RUM events to filter on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#event_type RumMetric#event_type}
        '''
        result = self._values.get("event_type")
        assert result is not None, "Required property 'event_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the RUM-based metric. This field can't be updated after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#name RumMetric#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compute(self) -> typing.Optional[RumMetricCompute]:
        '''compute block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#compute RumMetric#compute}
        '''
        result = self._values.get("compute")
        return typing.cast(typing.Optional[RumMetricCompute], result)

    @builtins.property
    def filter(self) -> typing.Optional["RumMetricFilter"]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#filter RumMetric#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional["RumMetricFilter"], result)

    @builtins.property
    def group_by(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RumMetricGroupBy"]]]:
        '''group_by block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#group_by RumMetric#group_by}
        '''
        result = self._values.get("group_by")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RumMetricGroupBy"]]], result)

    @builtins.property
    def uniqueness(self) -> typing.Optional["RumMetricUniqueness"]:
        '''uniqueness block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#uniqueness RumMetric#uniqueness}
        '''
        result = self._values.get("uniqueness")
        return typing.cast(typing.Optional["RumMetricUniqueness"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RumMetricConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.rumMetric.RumMetricFilter",
    jsii_struct_bases=[],
    name_mapping={"query": "query"},
)
class RumMetricFilter:
    def __init__(self, *, query: typing.Optional[builtins.str] = None) -> None:
        '''
        :param query: The search query. Follows RUM search syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#query RumMetric#query}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef5332e3a005389985b313e64764b01ef1f52531bf5338d02a738ad638a7698)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if query is not None:
            self._values["query"] = query

    @builtins.property
    def query(self) -> typing.Optional[builtins.str]:
        '''The search query. Follows RUM search syntax.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#query RumMetric#query}
        '''
        result = self._values.get("query")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RumMetricFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RumMetricFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.rumMetric.RumMetricFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6eacd57b30f23fdb35b795eb45705652436ae053ca472c3158ed7d4d670b1e6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d9e4b0b95ae439af3c6a76f2b9dd7bb7f80a239eaff135144c6f1ccffbdfdeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RumMetricFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RumMetricFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RumMetricFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e74f3b0777c8e4d4d2331d82319e9d28b4d9474ef23ca1a0f42a5aef83609ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.rumMetric.RumMetricGroupBy",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "tag_name": "tagName"},
)
class RumMetricGroupBy:
    def __init__(
        self,
        *,
        path: typing.Optional[builtins.str] = None,
        tag_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: The path to the value the RUM-based metric will be aggregated over. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#path RumMetric#path}
        :param tag_name: Name of the tag that gets created. By default, ``path`` is used as the tag name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#tag_name RumMetric#tag_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63a6e3abf868cdaf91193ff8bbf13b053d3a87f54a077d1e0b621bc05619f1af)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if path is not None:
            self._values["path"] = path
        if tag_name is not None:
            self._values["tag_name"] = tag_name

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the value the RUM-based metric will be aggregated over.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#path RumMetric#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_name(self) -> typing.Optional[builtins.str]:
        '''Name of the tag that gets created. By default, ``path`` is used as the tag name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#tag_name RumMetric#tag_name}
        '''
        result = self._values.get("tag_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RumMetricGroupBy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RumMetricGroupByList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.rumMetric.RumMetricGroupByList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a563d213fc49a7de44130f18c78763e50dc08096eadda266b629902609c47d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RumMetricGroupByOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4301e709f7b668884b0396f1e26a38948a6bda305700ea460bce598184cef7fb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RumMetricGroupByOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__934d6ffae72122c12972d05b803f297ac6452493b9c5b37f5ca6678d5a07310f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e44f67f05cdf2ceb9fbc7b8b8f4244ea0deb535e2ab3652e8e58521c9f80c773)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b804d0ac91e1259ca5a39e5bd2bd4796c4c044bf34e0fc72eb8609c2cdfe73db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RumMetricGroupBy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RumMetricGroupBy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RumMetricGroupBy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b355cd566cc929eaee3c110456836f2d8e09a3d71273fa332e28c473414ebd3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RumMetricGroupByOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.rumMetric.RumMetricGroupByOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c64decbe1b881b2c59f6e1aae57f5a80f9428761437fa60d4925141dba9f837)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetTagName")
    def reset_tag_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagName", []))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="tagNameInput")
    def tag_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagNameInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94d51e5fb0d69197e20b47eaef5b9857e5bd991ec4fefc2a5aa33d5f46643e37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagName")
    def tag_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagName"))

    @tag_name.setter
    def tag_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41cc7f0ddcc63681a9042beb27f5a0bf54a602a50621a04dbb3842df03e0c581)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RumMetricGroupBy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RumMetricGroupBy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RumMetricGroupBy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30fbcc7a74dfaed3dfc6cd0a9fb45dc16a8456ebf1b04c72332f04e83eecf4bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.rumMetric.RumMetricUniqueness",
    jsii_struct_bases=[],
    name_mapping={"when": "when"},
)
class RumMetricUniqueness:
    def __init__(self, *, when: typing.Optional[builtins.str] = None) -> None:
        '''
        :param when: When to count updatable events. ``match`` when the event is first seen, or ``end`` when the event is complete. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#when RumMetric#when}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2847a96fc6474e19eb792e2ff60c71bf6cbce7e203e399504c4c72d4012684b)
            check_type(argname="argument when", value=when, expected_type=type_hints["when"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if when is not None:
            self._values["when"] = when

    @builtins.property
    def when(self) -> typing.Optional[builtins.str]:
        '''When to count updatable events. ``match`` when the event is first seen, or ``end`` when the event is complete.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/rum_metric#when RumMetric#when}
        '''
        result = self._values.get("when")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RumMetricUniqueness(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RumMetricUniquenessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.rumMetric.RumMetricUniquenessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7113b686d4336a1f425acce68390b3c2dfaf2fa5b6f000ab7a551c73f40c178b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetWhen")
    def reset_when(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWhen", []))

    @builtins.property
    @jsii.member(jsii_name="whenInput")
    def when_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "whenInput"))

    @builtins.property
    @jsii.member(jsii_name="when")
    def when(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "when"))

    @when.setter
    def when(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__199a5cdba1bbd1b24102ab6530bf660f2a6e7b4872f3b4a5c2f7d908a5bc2b4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "when", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RumMetricUniqueness]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RumMetricUniqueness]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RumMetricUniqueness]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ca9160910118d223cb37625f6b069432d6faf7d391cad4f76c21c70f4d93ffb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "RumMetric",
    "RumMetricCompute",
    "RumMetricComputeOutputReference",
    "RumMetricConfig",
    "RumMetricFilter",
    "RumMetricFilterOutputReference",
    "RumMetricGroupBy",
    "RumMetricGroupByList",
    "RumMetricGroupByOutputReference",
    "RumMetricUniqueness",
    "RumMetricUniquenessOutputReference",
]

publication.publish()

def _typecheckingstub__a5ea56942a801b5240ca57c2b8937e058b2298e21c8635ed345f993262862b9d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    event_type: builtins.str,
    name: builtins.str,
    compute: typing.Optional[typing.Union[RumMetricCompute, typing.Dict[builtins.str, typing.Any]]] = None,
    filter: typing.Optional[typing.Union[RumMetricFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    group_by: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RumMetricGroupBy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    uniqueness: typing.Optional[typing.Union[RumMetricUniqueness, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9cc13eeb8e730ec127b798c41d56bebb9849d331bea2ba679a37319bdb02e843(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38555a5c3bed11e39a8ab41d0aaf59f55baa0ed2f59e34d62494eb98083d1d79(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RumMetricGroupBy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1b0bc51613a31e2e583b906c431b9d94198b01bc7cc5695f9857dea154c2953(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bcda8e38f79ae82955cb035853fc0b5d9a8f2925836964faf9f76ec01ea7705(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13940534ba6f3d7f0044cb6aedd304c8174e8f6909506720904427ca8e073e87(
    *,
    aggregation_type: builtins.str,
    include_percentiles: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b24e62bb99f7dc65ff1fe1a015d482c6be66bacba53a0acdfe738d84c9f4b627(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1917112847c1ec09b2e41b79f68d8687a508d3c6bcdffcb46a4268d2c601d20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6accbf67cf379537b6a93e71791f53fd4e62f9fb2a9d26a60fb8b3e07d9a18(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0004f7ece1d035a8ad08da551fe2553e147ef99763c1a0e68afa4426df9cb57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ba133008d98556d570c406386bb2fbeef1f032410ca42c7dfefe47cd8d1355(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RumMetricCompute]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be5da0eb6f71ac9e1f29e73061c2a5cdf1067a7c20c5efb26958eb6ee1975add(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_type: builtins.str,
    name: builtins.str,
    compute: typing.Optional[typing.Union[RumMetricCompute, typing.Dict[builtins.str, typing.Any]]] = None,
    filter: typing.Optional[typing.Union[RumMetricFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    group_by: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RumMetricGroupBy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    uniqueness: typing.Optional[typing.Union[RumMetricUniqueness, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef5332e3a005389985b313e64764b01ef1f52531bf5338d02a738ad638a7698(
    *,
    query: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eacd57b30f23fdb35b795eb45705652436ae053ca472c3158ed7d4d670b1e6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d9e4b0b95ae439af3c6a76f2b9dd7bb7f80a239eaff135144c6f1ccffbdfdeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e74f3b0777c8e4d4d2331d82319e9d28b4d9474ef23ca1a0f42a5aef83609ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RumMetricFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63a6e3abf868cdaf91193ff8bbf13b053d3a87f54a077d1e0b621bc05619f1af(
    *,
    path: typing.Optional[builtins.str] = None,
    tag_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a563d213fc49a7de44130f18c78763e50dc08096eadda266b629902609c47d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4301e709f7b668884b0396f1e26a38948a6bda305700ea460bce598184cef7fb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__934d6ffae72122c12972d05b803f297ac6452493b9c5b37f5ca6678d5a07310f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e44f67f05cdf2ceb9fbc7b8b8f4244ea0deb535e2ab3652e8e58521c9f80c773(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b804d0ac91e1259ca5a39e5bd2bd4796c4c044bf34e0fc72eb8609c2cdfe73db(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b355cd566cc929eaee3c110456836f2d8e09a3d71273fa332e28c473414ebd3a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RumMetricGroupBy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c64decbe1b881b2c59f6e1aae57f5a80f9428761437fa60d4925141dba9f837(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d51e5fb0d69197e20b47eaef5b9857e5bd991ec4fefc2a5aa33d5f46643e37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41cc7f0ddcc63681a9042beb27f5a0bf54a602a50621a04dbb3842df03e0c581(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30fbcc7a74dfaed3dfc6cd0a9fb45dc16a8456ebf1b04c72332f04e83eecf4bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RumMetricGroupBy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2847a96fc6474e19eb792e2ff60c71bf6cbce7e203e399504c4c72d4012684b(
    *,
    when: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7113b686d4336a1f425acce68390b3c2dfaf2fa5b6f000ab7a551c73f40c178b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__199a5cdba1bbd1b24102ab6530bf660f2a6e7b4872f3b4a5c2f7d908a5bc2b4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ca9160910118d223cb37625f6b069432d6faf7d391cad4f76c21c70f4d93ffb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RumMetricUniqueness]],
) -> None:
    """Type checking stubs"""
    pass
