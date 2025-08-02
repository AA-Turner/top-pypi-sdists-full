r'''
# `data_opentelekomcloud_ces_multiple_metric_data_v1`

Refer to the Terraform Registry for docs: [`data_opentelekomcloud_ces_multiple_metric_data_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1).
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


class DataOpentelekomcloudCesMultipleMetricDataV1(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesMultipleMetricDataV1.DataOpentelekomcloudCesMultipleMetricDataV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1 opentelekomcloud_ces_multiple_metric_data_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        filter: builtins.str,
        from_: jsii.Number,
        metrics: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataOpentelekomcloudCesMultipleMetricDataV1Metrics", typing.Dict[builtins.str, typing.Any]]]],
        period: builtins.str,
        to: jsii.Number,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1 opentelekomcloud_ces_multiple_metric_data_v1} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param filter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#filter DataOpentelekomcloudCesMultipleMetricDataV1#filter}.
        :param from_: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#from DataOpentelekomcloudCesMultipleMetricDataV1#from}.
        :param metrics: metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#metrics DataOpentelekomcloudCesMultipleMetricDataV1#metrics}
        :param period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#period DataOpentelekomcloudCesMultipleMetricDataV1#period}.
        :param to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#to DataOpentelekomcloudCesMultipleMetricDataV1#to}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#id DataOpentelekomcloudCesMultipleMetricDataV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dd9c40a0057b0d606b50c9c51b83465e734b781d6c540f777afbc07ca8afde9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOpentelekomcloudCesMultipleMetricDataV1Config(
            filter=filter,
            from_=from_,
            metrics=metrics,
            period=period,
            to=to,
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
        '''Generates CDKTF code for importing a DataOpentelekomcloudCesMultipleMetricDataV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpentelekomcloudCesMultipleMetricDataV1 to import.
        :param import_from_id: The id of the existing DataOpentelekomcloudCesMultipleMetricDataV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpentelekomcloudCesMultipleMetricDataV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af980ba5878fe7d1b5917ebfc66846eb346306da987835801f3702edc5df9cb6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMetrics")
    def put_metrics(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataOpentelekomcloudCesMultipleMetricDataV1Metrics", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9f3ee08de7f3966cc2afd72f26644876b5e190200d2b5d7cb87d89b04602d45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetrics", [value]))

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
    @jsii.member(jsii_name="metrics")
    def metrics(self) -> "DataOpentelekomcloudCesMultipleMetricDataV1MetricsList":
        return typing.cast("DataOpentelekomcloudCesMultipleMetricDataV1MetricsList", jsii.get(self, "metrics"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="fromInput")
    def from_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fromInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsInput")
    def metrics_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataOpentelekomcloudCesMultipleMetricDataV1Metrics"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataOpentelekomcloudCesMultipleMetricDataV1Metrics"]]], jsii.get(self, "metricsInput"))

    @builtins.property
    @jsii.member(jsii_name="periodInput")
    def period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "periodInput"))

    @builtins.property
    @jsii.member(jsii_name="toInput")
    def to_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "toInput"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15bc0a7b8acc95bc7746a9fa71c24c8aceaa96efc82686b5d0c410f2bcd02295)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="from")
    def from_(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "from"))

    @from_.setter
    def from_(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce0a4a01a1cc87000aa5c429906d3f939cf48df16062000d0ae2eb4b02ad9853)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "from", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b2d29e51caf99953084568c83b45601366694f9cea5629a9d92d478545a4d51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "period"))

    @period.setter
    def period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c81c714354db7734a9a4f9b74491b917b2c82ca1d8e4a96d6c21e7907d0eb0b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "period", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="to")
    def to(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "to"))

    @to.setter
    def to(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc1056b9c406747d5b43fad7fd2db5a1feddff1a8d4a378b3b36313960a2ca3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "to", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesMultipleMetricDataV1.DataOpentelekomcloudCesMultipleMetricDataV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "filter": "filter",
        "from_": "from",
        "metrics": "metrics",
        "period": "period",
        "to": "to",
        "id": "id",
    },
)
class DataOpentelekomcloudCesMultipleMetricDataV1Config(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        filter: builtins.str,
        from_: jsii.Number,
        metrics: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataOpentelekomcloudCesMultipleMetricDataV1Metrics", typing.Dict[builtins.str, typing.Any]]]],
        period: builtins.str,
        to: jsii.Number,
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
        :param filter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#filter DataOpentelekomcloudCesMultipleMetricDataV1#filter}.
        :param from_: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#from DataOpentelekomcloudCesMultipleMetricDataV1#from}.
        :param metrics: metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#metrics DataOpentelekomcloudCesMultipleMetricDataV1#metrics}
        :param period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#period DataOpentelekomcloudCesMultipleMetricDataV1#period}.
        :param to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#to DataOpentelekomcloudCesMultipleMetricDataV1#to}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#id DataOpentelekomcloudCesMultipleMetricDataV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bc8a74f36b3185b2958fcfca75059d0f503f20bf6070917c589119b180e36ba)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
            check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument to", value=to, expected_type=type_hints["to"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter": filter,
            "from_": from_,
            "metrics": metrics,
            "period": period,
            "to": to,
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
    def filter(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#filter DataOpentelekomcloudCesMultipleMetricDataV1#filter}.'''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def from_(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#from DataOpentelekomcloudCesMultipleMetricDataV1#from}.'''
        result = self._values.get("from_")
        assert result is not None, "Required property 'from_' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def metrics(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataOpentelekomcloudCesMultipleMetricDataV1Metrics"]]:
        '''metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#metrics DataOpentelekomcloudCesMultipleMetricDataV1#metrics}
        '''
        result = self._values.get("metrics")
        assert result is not None, "Required property 'metrics' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataOpentelekomcloudCesMultipleMetricDataV1Metrics"]], result)

    @builtins.property
    def period(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#period DataOpentelekomcloudCesMultipleMetricDataV1#period}.'''
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def to(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#to DataOpentelekomcloudCesMultipleMetricDataV1#to}.'''
        result = self._values.get("to")
        assert result is not None, "Required property 'to' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#id DataOpentelekomcloudCesMultipleMetricDataV1#id}.

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
        return "DataOpentelekomcloudCesMultipleMetricDataV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesMultipleMetricDataV1.DataOpentelekomcloudCesMultipleMetricDataV1Metrics",
    jsii_struct_bases=[],
    name_mapping={
        "dimensions": "dimensions",
        "metric_name": "metricName",
        "namespace": "namespace",
    },
)
class DataOpentelekomcloudCesMultipleMetricDataV1Metrics:
    def __init__(
        self,
        *,
        dimensions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensions", typing.Dict[builtins.str, typing.Any]]]],
        metric_name: builtins.str,
        namespace: builtins.str,
    ) -> None:
        '''
        :param dimensions: dimensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#dimensions DataOpentelekomcloudCesMultipleMetricDataV1#dimensions}
        :param metric_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#metric_name DataOpentelekomcloudCesMultipleMetricDataV1#metric_name}.
        :param namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#namespace DataOpentelekomcloudCesMultipleMetricDataV1#namespace}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76c5e2404a5fb0a015f9d591fbdbf265f5f084b89499be071fd16bddc78c7058)
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dimensions": dimensions,
            "metric_name": metric_name,
            "namespace": namespace,
        }

    @builtins.property
    def dimensions(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensions"]]:
        '''dimensions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#dimensions DataOpentelekomcloudCesMultipleMetricDataV1#dimensions}
        '''
        result = self._values.get("dimensions")
        assert result is not None, "Required property 'dimensions' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensions"]], result)

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#metric_name DataOpentelekomcloudCesMultipleMetricDataV1#metric_name}.'''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#namespace DataOpentelekomcloudCesMultipleMetricDataV1#namespace}.'''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudCesMultipleMetricDataV1Metrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesMultipleMetricDataV1.DataOpentelekomcloudCesMultipleMetricDataV1MetricsDatapoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOpentelekomcloudCesMultipleMetricDataV1MetricsDatapoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudCesMultipleMetricDataV1MetricsDatapoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOpentelekomcloudCesMultipleMetricDataV1MetricsDatapointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesMultipleMetricDataV1.DataOpentelekomcloudCesMultipleMetricDataV1MetricsDatapointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0d073b69456de561ffb01f8c88c9a6a42db43dc279769b911977a974b781b7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataOpentelekomcloudCesMultipleMetricDataV1MetricsDatapointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88aedea113406d1dd3b940c0a34a05612f29ab4ef90ccfeb761e08458c05fea0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOpentelekomcloudCesMultipleMetricDataV1MetricsDatapointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1c112f7b755a9bf5513f1b9a3f011497f0537802ece162abfdcb027e5f7de94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bf81f13a6dbd00bee677b1826419c72817e9999d61db4be17800ea4b2c7bbd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75cd13785c2db24124f8f45a6d812b8bd88fc0d664acc2d5748ff168a6c39364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataOpentelekomcloudCesMultipleMetricDataV1MetricsDatapointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesMultipleMetricDataV1.DataOpentelekomcloudCesMultipleMetricDataV1MetricsDatapointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65f7c31c03527933d8c8f97f06bab61d89a7fd39884919de457dafb09bd4aaca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="average")
    def average(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "average"))

    @builtins.property
    @jsii.member(jsii_name="max")
    def max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "max"))

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @builtins.property
    @jsii.member(jsii_name="sum")
    def sum(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sum"))

    @builtins.property
    @jsii.member(jsii_name="timestamp")
    def timestamp(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timestamp"))

    @builtins.property
    @jsii.member(jsii_name="variance")
    def variance(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "variance"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOpentelekomcloudCesMultipleMetricDataV1MetricsDatapoints]:
        return typing.cast(typing.Optional[DataOpentelekomcloudCesMultipleMetricDataV1MetricsDatapoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOpentelekomcloudCesMultipleMetricDataV1MetricsDatapoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd7eea949cdaced63d160f7baede1746629c5cbbb2967d285d21bea4f87ab982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesMultipleMetricDataV1.DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensions:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#name DataOpentelekomcloudCesMultipleMetricDataV1#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#value DataOpentelekomcloudCesMultipleMetricDataV1#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04109596a0f325ff8e1f8fcefac5729d3e8bb523b46abe036c2d343c7a9f8ecb)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#name DataOpentelekomcloudCesMultipleMetricDataV1#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_multiple_metric_data_v1#value DataOpentelekomcloudCesMultipleMetricDataV1#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesMultipleMetricDataV1.DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abb8e4941b9fc87ebd6a1654e46d584a7044c4ced3d1f3ed1a72946efb1cb541)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdd134ca422b383c99a1c1315ad3a596fb1fda35d3c0116ee9fbc18384397041)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1ec68578b5a70c2f6c0fc9708a8e670b0e25e9a8461d7bcfa7818b53c10d37b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9a4b42118908600e640b6d5bf5c838268ce91c450ee4af73d739eda22211ccd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6937449a2ff74e53c16c73eb36b4c5ac904a23162e584995f290f3ae752be15f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__161a0c5cb231493c944a4f36391e45aea68668ae9757d1fd302b862026ae64c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesMultipleMetricDataV1.DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6626d30e845f3d5d6972f35bb7491be8d6799c02768cb1899c5ab4f41c6feee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f036ee393d356142aef1d5b44235a24267e1955c5892722c8cd1197f6d3b89bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__927c9a4d9b76e6b6e52b64dfa0ab2067f3abe4fdd4ac0a8d28abd3e6c41a9656)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb0aac6fd60122b9b3aef77f98557e2cfa0f82c192fc220cc5fc0746c74f7827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataOpentelekomcloudCesMultipleMetricDataV1MetricsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesMultipleMetricDataV1.DataOpentelekomcloudCesMultipleMetricDataV1MetricsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d3026277592d74ae045f8b2214d0e53535959f6f728ca22c1e56d8248ca2e25)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataOpentelekomcloudCesMultipleMetricDataV1MetricsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc207dfd8a6c0b6c0fa35040544295abe61e7bc84151ccdbb5e2cdf45391b78d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOpentelekomcloudCesMultipleMetricDataV1MetricsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a49a3d39b366ea49217d6f5e23f7c0b6cac5fd8289e1870ef525fde9be158ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd9e5ba000bd5695dca703f99bf04c5eb1fa95962e45bcace4e0fee850f76a28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fc592b6fb595980cc5e1b5320c02d753348f055e307084df61bd21759c5a1cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataOpentelekomcloudCesMultipleMetricDataV1Metrics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataOpentelekomcloudCesMultipleMetricDataV1Metrics]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataOpentelekomcloudCesMultipleMetricDataV1Metrics]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d1f36c3f0f118b9371ad4de5e2dafb84d141378896400f4eeb90421392f0d3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataOpentelekomcloudCesMultipleMetricDataV1MetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesMultipleMetricDataV1.DataOpentelekomcloudCesMultipleMetricDataV1MetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__941ae3d98699b73f3bd9be47e1d84346df525de2b745b6bc1b7106e5bab6818e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDimensions")
    def put_dimensions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__373bb00580de39dff8166e9e1b1ca8d52af5be68de60c2f5807c4353bc122b6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDimensions", [value]))

    @builtins.property
    @jsii.member(jsii_name="datapoints")
    def datapoints(
        self,
    ) -> DataOpentelekomcloudCesMultipleMetricDataV1MetricsDatapointsList:
        return typing.cast(DataOpentelekomcloudCesMultipleMetricDataV1MetricsDatapointsList, jsii.get(self, "datapoints"))

    @builtins.property
    @jsii.member(jsii_name="dimensions")
    def dimensions(
        self,
    ) -> DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensionsList:
        return typing.cast(DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensionsList, jsii.get(self, "dimensions"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unit"))

    @builtins.property
    @jsii.member(jsii_name="dimensionsInput")
    def dimensions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensions]]], jsii.get(self, "dimensionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__43ea1731a0f9736e2193398b54c88b65c826306707a41741f4cd520a291965e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9f70a3079cbe1a48eb038d5507d40a1142fd9764bf24d2353cd208e1d88a9ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOpentelekomcloudCesMultipleMetricDataV1Metrics]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOpentelekomcloudCesMultipleMetricDataV1Metrics]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOpentelekomcloudCesMultipleMetricDataV1Metrics]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73aff0c4e7f2c4c379394019fca4c3c79117edd1a5852e7539eee1bf51f77c70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataOpentelekomcloudCesMultipleMetricDataV1",
    "DataOpentelekomcloudCesMultipleMetricDataV1Config",
    "DataOpentelekomcloudCesMultipleMetricDataV1Metrics",
    "DataOpentelekomcloudCesMultipleMetricDataV1MetricsDatapoints",
    "DataOpentelekomcloudCesMultipleMetricDataV1MetricsDatapointsList",
    "DataOpentelekomcloudCesMultipleMetricDataV1MetricsDatapointsOutputReference",
    "DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensions",
    "DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensionsList",
    "DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensionsOutputReference",
    "DataOpentelekomcloudCesMultipleMetricDataV1MetricsList",
    "DataOpentelekomcloudCesMultipleMetricDataV1MetricsOutputReference",
]

publication.publish()

def _typecheckingstub__7dd9c40a0057b0d606b50c9c51b83465e734b781d6c540f777afbc07ca8afde9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    filter: builtins.str,
    from_: jsii.Number,
    metrics: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataOpentelekomcloudCesMultipleMetricDataV1Metrics, typing.Dict[builtins.str, typing.Any]]]],
    period: builtins.str,
    to: jsii.Number,
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

def _typecheckingstub__af980ba5878fe7d1b5917ebfc66846eb346306da987835801f3702edc5df9cb6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f3ee08de7f3966cc2afd72f26644876b5e190200d2b5d7cb87d89b04602d45(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataOpentelekomcloudCesMultipleMetricDataV1Metrics, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15bc0a7b8acc95bc7746a9fa71c24c8aceaa96efc82686b5d0c410f2bcd02295(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0a4a01a1cc87000aa5c429906d3f939cf48df16062000d0ae2eb4b02ad9853(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2d29e51caf99953084568c83b45601366694f9cea5629a9d92d478545a4d51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c81c714354db7734a9a4f9b74491b917b2c82ca1d8e4a96d6c21e7907d0eb0b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc1056b9c406747d5b43fad7fd2db5a1feddff1a8d4a378b3b36313960a2ca3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc8a74f36b3185b2958fcfca75059d0f503f20bf6070917c589119b180e36ba(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    filter: builtins.str,
    from_: jsii.Number,
    metrics: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataOpentelekomcloudCesMultipleMetricDataV1Metrics, typing.Dict[builtins.str, typing.Any]]]],
    period: builtins.str,
    to: jsii.Number,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76c5e2404a5fb0a015f9d591fbdbf265f5f084b89499be071fd16bddc78c7058(
    *,
    dimensions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensions, typing.Dict[builtins.str, typing.Any]]]],
    metric_name: builtins.str,
    namespace: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d073b69456de561ffb01f8c88c9a6a42db43dc279769b911977a974b781b7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88aedea113406d1dd3b940c0a34a05612f29ab4ef90ccfeb761e08458c05fea0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1c112f7b755a9bf5513f1b9a3f011497f0537802ece162abfdcb027e5f7de94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf81f13a6dbd00bee677b1826419c72817e9999d61db4be17800ea4b2c7bbd2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75cd13785c2db24124f8f45a6d812b8bd88fc0d664acc2d5748ff168a6c39364(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65f7c31c03527933d8c8f97f06bab61d89a7fd39884919de457dafb09bd4aaca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd7eea949cdaced63d160f7baede1746629c5cbbb2967d285d21bea4f87ab982(
    value: typing.Optional[DataOpentelekomcloudCesMultipleMetricDataV1MetricsDatapoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04109596a0f325ff8e1f8fcefac5729d3e8bb523b46abe036c2d343c7a9f8ecb(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb8e4941b9fc87ebd6a1654e46d584a7044c4ced3d1f3ed1a72946efb1cb541(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdd134ca422b383c99a1c1315ad3a596fb1fda35d3c0116ee9fbc18384397041(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ec68578b5a70c2f6c0fc9708a8e670b0e25e9a8461d7bcfa7818b53c10d37b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a4b42118908600e640b6d5bf5c838268ce91c450ee4af73d739eda22211ccd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6937449a2ff74e53c16c73eb36b4c5ac904a23162e584995f290f3ae752be15f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__161a0c5cb231493c944a4f36391e45aea68668ae9757d1fd302b862026ae64c1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6626d30e845f3d5d6972f35bb7491be8d6799c02768cb1899c5ab4f41c6feee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f036ee393d356142aef1d5b44235a24267e1955c5892722c8cd1197f6d3b89bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__927c9a4d9b76e6b6e52b64dfa0ab2067f3abe4fdd4ac0a8d28abd3e6c41a9656(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0aac6fd60122b9b3aef77f98557e2cfa0f82c192fc220cc5fc0746c74f7827(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d3026277592d74ae045f8b2214d0e53535959f6f728ca22c1e56d8248ca2e25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc207dfd8a6c0b6c0fa35040544295abe61e7bc84151ccdbb5e2cdf45391b78d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a49a3d39b366ea49217d6f5e23f7c0b6cac5fd8289e1870ef525fde9be158ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd9e5ba000bd5695dca703f99bf04c5eb1fa95962e45bcace4e0fee850f76a28(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fc592b6fb595980cc5e1b5320c02d753348f055e307084df61bd21759c5a1cd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d1f36c3f0f118b9371ad4de5e2dafb84d141378896400f4eeb90421392f0d3a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataOpentelekomcloudCesMultipleMetricDataV1Metrics]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__941ae3d98699b73f3bd9be47e1d84346df525de2b745b6bc1b7106e5bab6818e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__373bb00580de39dff8166e9e1b1ca8d52af5be68de60c2f5807c4353bc122b6c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataOpentelekomcloudCesMultipleMetricDataV1MetricsDimensions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43ea1731a0f9736e2193398b54c88b65c826306707a41741f4cd520a291965e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f70a3079cbe1a48eb038d5507d40a1142fd9764bf24d2353cd208e1d88a9ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73aff0c4e7f2c4c379394019fca4c3c79117edd1a5852e7539eee1bf51f77c70(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOpentelekomcloudCesMultipleMetricDataV1Metrics]],
) -> None:
    """Type checking stubs"""
    pass
