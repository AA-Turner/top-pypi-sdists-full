r'''
# `datadog_logs_metric`

Refer to the Terraform Registry for docs: [`datadog_logs_metric`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric).
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


class LogsMetric(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsMetric.LogsMetric",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric datadog_logs_metric}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        compute: typing.Union["LogsMetricCompute", typing.Dict[builtins.str, typing.Any]],
        filter: typing.Union["LogsMetricFilter", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        group_by: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsMetricGroupBy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric datadog_logs_metric} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param compute: compute block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#compute LogsMetric#compute}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#filter LogsMetric#filter}
        :param name: The name of the log-based metric. This field can't be updated after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#name LogsMetric#name}
        :param group_by: group_by block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#group_by LogsMetric#group_by}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#id LogsMetric#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1bd5abf79d449868ffba30ab4500395334e8c723246af86623f01f36292c801)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LogsMetricConfig(
            compute=compute,
            filter=filter,
            name=name,
            group_by=group_by,
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
        '''Generates CDKTF code for importing a LogsMetric resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LogsMetric to import.
        :param import_from_id: The id of the existing LogsMetric that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LogsMetric to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d86e6cbaff8708611c52796a7d3d88af7d0da6ee0e548b2d8fba5a2caac3283)
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
        :param aggregation_type: The type of aggregation to use. This field can't be updated after creation. Valid values are ``count``, ``distribution``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#aggregation_type LogsMetric#aggregation_type}
        :param include_percentiles: Toggle to include/exclude percentiles for a distribution metric. Defaults to false. Can only be applied to metrics that have an ``aggregation_type`` of distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#include_percentiles LogsMetric#include_percentiles}
        :param path: The path to the value the log-based metric will aggregate on (only used if the aggregation type is a "distribution"). This field can't be updated after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#path LogsMetric#path}
        '''
        value = LogsMetricCompute(
            aggregation_type=aggregation_type,
            include_percentiles=include_percentiles,
            path=path,
        )

        return typing.cast(None, jsii.invoke(self, "putCompute", [value]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(self, *, query: builtins.str) -> None:
        '''
        :param query: The search query - following the log search syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#query LogsMetric#query}
        '''
        value = LogsMetricFilter(query=query)

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putGroupBy")
    def put_group_by(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsMetricGroupBy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2269ba906028b6bd868148264f8db45a0840013a8db6e5f9e46c409f516c7a35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGroupBy", [value]))

    @jsii.member(jsii_name="resetGroupBy")
    def reset_group_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupBy", []))

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
    @jsii.member(jsii_name="compute")
    def compute(self) -> "LogsMetricComputeOutputReference":
        return typing.cast("LogsMetricComputeOutputReference", jsii.get(self, "compute"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> "LogsMetricFilterOutputReference":
        return typing.cast("LogsMetricFilterOutputReference", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="groupBy")
    def group_by(self) -> "LogsMetricGroupByList":
        return typing.cast("LogsMetricGroupByList", jsii.get(self, "groupBy"))

    @builtins.property
    @jsii.member(jsii_name="computeInput")
    def compute_input(self) -> typing.Optional["LogsMetricCompute"]:
        return typing.cast(typing.Optional["LogsMetricCompute"], jsii.get(self, "computeInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional["LogsMetricFilter"]:
        return typing.cast(typing.Optional["LogsMetricFilter"], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="groupByInput")
    def group_by_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsMetricGroupBy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsMetricGroupBy"]]], jsii.get(self, "groupByInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d039b57a614bce83146e516e154cf0f1d6fa92b6944f46c9f65d0bdce397074)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42b795899e2ce653525f9ecc9bc6fe1bb454dafebc180968689d722412f53cdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsMetric.LogsMetricCompute",
    jsii_struct_bases=[],
    name_mapping={
        "aggregation_type": "aggregationType",
        "include_percentiles": "includePercentiles",
        "path": "path",
    },
)
class LogsMetricCompute:
    def __init__(
        self,
        *,
        aggregation_type: builtins.str,
        include_percentiles: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aggregation_type: The type of aggregation to use. This field can't be updated after creation. Valid values are ``count``, ``distribution``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#aggregation_type LogsMetric#aggregation_type}
        :param include_percentiles: Toggle to include/exclude percentiles for a distribution metric. Defaults to false. Can only be applied to metrics that have an ``aggregation_type`` of distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#include_percentiles LogsMetric#include_percentiles}
        :param path: The path to the value the log-based metric will aggregate on (only used if the aggregation type is a "distribution"). This field can't be updated after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#path LogsMetric#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ece69d0f5c15ac4ac00f169a3f6f99f77302dfb788d0ca728bd991e079f8258f)
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
        '''The type of aggregation to use. This field can't be updated after creation. Valid values are ``count``, ``distribution``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#aggregation_type LogsMetric#aggregation_type}
        '''
        result = self._values.get("aggregation_type")
        assert result is not None, "Required property 'aggregation_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include_percentiles(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Toggle to include/exclude percentiles for a distribution metric.

        Defaults to false. Can only be applied to metrics that have an ``aggregation_type`` of distribution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#include_percentiles LogsMetric#include_percentiles}
        '''
        result = self._values.get("include_percentiles")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the value the log-based metric will aggregate on (only used if the aggregation type is a "distribution").

        This field can't be updated after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#path LogsMetric#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsMetricCompute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsMetricComputeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsMetric.LogsMetricComputeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8efb71910307294363c5678fb60952d27ccbf12671cc17206ee27989a6321c17)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c40d6f16e2f760118929e2324f1884510343097e73cd4e56f30374ab88f801b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c1c1cdc0d78a93d28e085c096219e895192014fd0c902ed77f2fb492ac7ef91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includePercentiles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c48970d3dff633395a4e7c45d07dbacf67a88f29f105bc01ccbd34ea91183bff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LogsMetricCompute]:
        return typing.cast(typing.Optional[LogsMetricCompute], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LogsMetricCompute]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f675a02e6ac6b3a289bcafa32082641f293b58a9ffefbd7afbdbd4aa42ae159)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsMetric.LogsMetricConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "compute": "compute",
        "filter": "filter",
        "name": "name",
        "group_by": "groupBy",
        "id": "id",
    },
)
class LogsMetricConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        compute: typing.Union[LogsMetricCompute, typing.Dict[builtins.str, typing.Any]],
        filter: typing.Union["LogsMetricFilter", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        group_by: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsMetricGroupBy", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param compute: compute block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#compute LogsMetric#compute}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#filter LogsMetric#filter}
        :param name: The name of the log-based metric. This field can't be updated after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#name LogsMetric#name}
        :param group_by: group_by block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#group_by LogsMetric#group_by}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#id LogsMetric#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(compute, dict):
            compute = LogsMetricCompute(**compute)
        if isinstance(filter, dict):
            filter = LogsMetricFilter(**filter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__614318b37d6afaf0d9a37465e4c3a3a655a3c7274cd2034f836e5b760e1abe4f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument compute", value=compute, expected_type=type_hints["compute"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument group_by", value=group_by, expected_type=type_hints["group_by"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compute": compute,
            "filter": filter,
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
        if group_by is not None:
            self._values["group_by"] = group_by
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
    def compute(self) -> LogsMetricCompute:
        '''compute block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#compute LogsMetric#compute}
        '''
        result = self._values.get("compute")
        assert result is not None, "Required property 'compute' is missing"
        return typing.cast(LogsMetricCompute, result)

    @builtins.property
    def filter(self) -> "LogsMetricFilter":
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#filter LogsMetric#filter}
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast("LogsMetricFilter", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the log-based metric. This field can't be updated after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#name LogsMetric#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_by(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsMetricGroupBy"]]]:
        '''group_by block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#group_by LogsMetric#group_by}
        '''
        result = self._values.get("group_by")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsMetricGroupBy"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#id LogsMetric#id}.

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
        return "LogsMetricConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsMetric.LogsMetricFilter",
    jsii_struct_bases=[],
    name_mapping={"query": "query"},
)
class LogsMetricFilter:
    def __init__(self, *, query: builtins.str) -> None:
        '''
        :param query: The search query - following the log search syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#query LogsMetric#query}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08deadc2a1e5afa556ba2a8f3a5d96057e2edf0cff8d1cb724a46587b65ed1fb)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }

    @builtins.property
    def query(self) -> builtins.str:
        '''The search query - following the log search syntax.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#query LogsMetric#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsMetricFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsMetricFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsMetric.LogsMetricFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21c487237c453c96e71dff5ee81be1b89ae1dc511afe72e48836272a97a954e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__d6a2c172d0dc4f2746bedc9e9b0816156f1374fd1e3d5769949d79e36778b666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LogsMetricFilter]:
        return typing.cast(typing.Optional[LogsMetricFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LogsMetricFilter]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b05e18b268c7c65200606a1ca5efbda183f19bdda490be4bbde94cf4da694e59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsMetric.LogsMetricGroupBy",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "tag_name": "tagName"},
)
class LogsMetricGroupBy:
    def __init__(self, *, path: builtins.str, tag_name: builtins.str) -> None:
        '''
        :param path: The path to the value the log-based metric will be aggregated over. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#path LogsMetric#path}
        :param tag_name: Name of the tag that gets created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#tag_name LogsMetric#tag_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90c933ef8cc2621b649c393be9dc471b26d581742318440b2ac908d4c2a11d3e)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "tag_name": tag_name,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''The path to the value the log-based metric will be aggregated over.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#path LogsMetric#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag_name(self) -> builtins.str:
        '''Name of the tag that gets created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_metric#tag_name LogsMetric#tag_name}
        '''
        result = self._values.get("tag_name")
        assert result is not None, "Required property 'tag_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsMetricGroupBy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsMetricGroupByList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsMetric.LogsMetricGroupByList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25f9373bd9810f647d2e555562be799a26e655688ce95a6b20b28524b0db3942)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LogsMetricGroupByOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f45b09405a8bce04f5b5260a242a136ca02afd928ef36cb7986ea538c8a5190)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LogsMetricGroupByOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90f88bcffca3eb5423bbd41a2af4c7ceba14ad25ca582cf1ceb8d4c09ef3c3d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__533a6691d03b1b40dd8a4033f151e733cddd6c701374ca84ed51e54692868ff4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1709db5a8c51eeb5d0c458ea9afef6e537088de422cbb03907198ef8bc96c038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsMetricGroupBy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsMetricGroupBy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsMetricGroupBy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02cf8d76087a0a3b87ed5a162428cc85c20985bbad8c96068f72d5c7b5ff85b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsMetricGroupByOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsMetric.LogsMetricGroupByOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0c8e0fed1d23aa9718d221d0f970ffac241ecb6203286590fa40d7550b13948)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
            type_hints = typing.get_type_hints(_typecheckingstub__233b24fcfd5b28fefb4c2572fe4d54a49245b059c7508087a68046707f3eb117)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagName")
    def tag_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagName"))

    @tag_name.setter
    def tag_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e3cfd129675b1f1214f722efb4d151422244bd6d9058d0756ce18076f818977)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsMetricGroupBy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsMetricGroupBy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsMetricGroupBy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__499ac16512ec42c4107683e35c45814ce1245e513a338ae37e106fa956766c72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LogsMetric",
    "LogsMetricCompute",
    "LogsMetricComputeOutputReference",
    "LogsMetricConfig",
    "LogsMetricFilter",
    "LogsMetricFilterOutputReference",
    "LogsMetricGroupBy",
    "LogsMetricGroupByList",
    "LogsMetricGroupByOutputReference",
]

publication.publish()

def _typecheckingstub__b1bd5abf79d449868ffba30ab4500395334e8c723246af86623f01f36292c801(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    compute: typing.Union[LogsMetricCompute, typing.Dict[builtins.str, typing.Any]],
    filter: typing.Union[LogsMetricFilter, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    group_by: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsMetricGroupBy, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__9d86e6cbaff8708611c52796a7d3d88af7d0da6ee0e548b2d8fba5a2caac3283(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2269ba906028b6bd868148264f8db45a0840013a8db6e5f9e46c409f516c7a35(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsMetricGroupBy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d039b57a614bce83146e516e154cf0f1d6fa92b6944f46c9f65d0bdce397074(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42b795899e2ce653525f9ecc9bc6fe1bb454dafebc180968689d722412f53cdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ece69d0f5c15ac4ac00f169a3f6f99f77302dfb788d0ca728bd991e079f8258f(
    *,
    aggregation_type: builtins.str,
    include_percentiles: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8efb71910307294363c5678fb60952d27ccbf12671cc17206ee27989a6321c17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c40d6f16e2f760118929e2324f1884510343097e73cd4e56f30374ab88f801b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c1c1cdc0d78a93d28e085c096219e895192014fd0c902ed77f2fb492ac7ef91(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c48970d3dff633395a4e7c45d07dbacf67a88f29f105bc01ccbd34ea91183bff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f675a02e6ac6b3a289bcafa32082641f293b58a9ffefbd7afbdbd4aa42ae159(
    value: typing.Optional[LogsMetricCompute],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__614318b37d6afaf0d9a37465e4c3a3a655a3c7274cd2034f836e5b760e1abe4f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    compute: typing.Union[LogsMetricCompute, typing.Dict[builtins.str, typing.Any]],
    filter: typing.Union[LogsMetricFilter, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    group_by: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsMetricGroupBy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08deadc2a1e5afa556ba2a8f3a5d96057e2edf0cff8d1cb724a46587b65ed1fb(
    *,
    query: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c487237c453c96e71dff5ee81be1b89ae1dc511afe72e48836272a97a954e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a2c172d0dc4f2746bedc9e9b0816156f1374fd1e3d5769949d79e36778b666(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b05e18b268c7c65200606a1ca5efbda183f19bdda490be4bbde94cf4da694e59(
    value: typing.Optional[LogsMetricFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c933ef8cc2621b649c393be9dc471b26d581742318440b2ac908d4c2a11d3e(
    *,
    path: builtins.str,
    tag_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f9373bd9810f647d2e555562be799a26e655688ce95a6b20b28524b0db3942(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f45b09405a8bce04f5b5260a242a136ca02afd928ef36cb7986ea538c8a5190(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f88bcffca3eb5423bbd41a2af4c7ceba14ad25ca582cf1ceb8d4c09ef3c3d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__533a6691d03b1b40dd8a4033f151e733cddd6c701374ca84ed51e54692868ff4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1709db5a8c51eeb5d0c458ea9afef6e537088de422cbb03907198ef8bc96c038(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02cf8d76087a0a3b87ed5a162428cc85c20985bbad8c96068f72d5c7b5ff85b3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsMetricGroupBy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c8e0fed1d23aa9718d221d0f970ffac241ecb6203286590fa40d7550b13948(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__233b24fcfd5b28fefb4c2572fe4d54a49245b059c7508087a68046707f3eb117(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e3cfd129675b1f1214f722efb4d151422244bd6d9058d0756ce18076f818977(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__499ac16512ec42c4107683e35c45814ce1245e513a338ae37e106fa956766c72(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsMetricGroupBy]],
) -> None:
    """Type checking stubs"""
    pass
