r'''
# `google_logging_metric`

Refer to the Terraform Registry for docs: [`google_logging_metric`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric).
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


class LoggingMetric(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.loggingMetric.LoggingMetric",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric google_logging_metric}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        filter: builtins.str,
        name: builtins.str,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_options: typing.Optional[typing.Union["LoggingMetricBucketOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        label_extractors: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metric_descriptor: typing.Optional[typing.Union["LoggingMetricMetricDescriptor", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["LoggingMetricTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        value_extractor: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric google_logging_metric} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param filter: An advanced logs filter (https://cloud.google.com/logging/docs/view/advanced-filters) which is used to match log entries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#filter LoggingMetric#filter}
        :param name: The client-assigned metric identifier. Examples - "error_count", "nginx/requests". Metric identifiers are limited to 100 characters and can include only the following characters A-Z, a-z, 0-9, and the special characters _-.,+!*',()%/. The forward-slash character (/) denotes a hierarchy of name pieces, and it cannot be the first character of the name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#name LoggingMetric#name}
        :param bucket_name: The resource name of the Log Bucket that owns the Log Metric. Only Log Buckets in projects are supported. The bucket has to be in the same project as the metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#bucket_name LoggingMetric#bucket_name}
        :param bucket_options: bucket_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#bucket_options LoggingMetric#bucket_options}
        :param description: A description of this metric, which is used in documentation. The maximum length of the description is 8000 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#description LoggingMetric#description}
        :param disabled: If set to True, then this metric is disabled and it does not generate any points. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#disabled LoggingMetric#disabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#id LoggingMetric#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param label_extractors: A map from a label key string to an extractor expression which is used to extract data from a log entry field and assign as the label value. Each label key specified in the LabelDescriptor must have an associated extractor expression in this map. The syntax of the extractor expression is the same as for the valueExtractor field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#label_extractors LoggingMetric#label_extractors}
        :param metric_descriptor: metric_descriptor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#metric_descriptor LoggingMetric#metric_descriptor}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#project LoggingMetric#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#timeouts LoggingMetric#timeouts}
        :param value_extractor: A valueExtractor is required when using a distribution logs-based metric to extract the values to record from a log entry. Two functions are supported for value extraction - EXTRACT(field) or REGEXP_EXTRACT(field, regex). The argument are 1. field - The name of the log entry field from which the value is to be extracted. 2. regex - A regular expression using the Google RE2 syntax (https://github.com/google/re2/wiki/Syntax) with a single capture group to extract data from the specified log entry field. The value of the field is converted to a string before applying the regex. It is an error to specify a regex that does not include exactly one capture group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#value_extractor LoggingMetric#value_extractor}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21e7ef5033d7c455eb6f2708a4b7786962373f75322014eebcacb52b5381f6f9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LoggingMetricConfig(
            filter=filter,
            name=name,
            bucket_name=bucket_name,
            bucket_options=bucket_options,
            description=description,
            disabled=disabled,
            id=id,
            label_extractors=label_extractors,
            metric_descriptor=metric_descriptor,
            project=project,
            timeouts=timeouts,
            value_extractor=value_extractor,
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
        '''Generates CDKTF code for importing a LoggingMetric resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LoggingMetric to import.
        :param import_from_id: The id of the existing LoggingMetric that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LoggingMetric to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1f859b357a789d027991213cd666dc5d4c8c7e1c14f69ecc1082927ce8afbc3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBucketOptions")
    def put_bucket_options(
        self,
        *,
        explicit_buckets: typing.Optional[typing.Union["LoggingMetricBucketOptionsExplicitBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        exponential_buckets: typing.Optional[typing.Union["LoggingMetricBucketOptionsExponentialBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        linear_buckets: typing.Optional[typing.Union["LoggingMetricBucketOptionsLinearBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param explicit_buckets: explicit_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#explicit_buckets LoggingMetric#explicit_buckets}
        :param exponential_buckets: exponential_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#exponential_buckets LoggingMetric#exponential_buckets}
        :param linear_buckets: linear_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#linear_buckets LoggingMetric#linear_buckets}
        '''
        value = LoggingMetricBucketOptions(
            explicit_buckets=explicit_buckets,
            exponential_buckets=exponential_buckets,
            linear_buckets=linear_buckets,
        )

        return typing.cast(None, jsii.invoke(self, "putBucketOptions", [value]))

    @jsii.member(jsii_name="putMetricDescriptor")
    def put_metric_descriptor(
        self,
        *,
        metric_kind: builtins.str,
        value_type: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoggingMetricMetricDescriptorLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metric_kind: Whether the metric records instantaneous values, changes to a value, etc. Some combinations of metricKind and valueType might not be supported. For counter metrics, set this to DELTA. Possible values: ["DELTA", "GAUGE", "CUMULATIVE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#metric_kind LoggingMetric#metric_kind}
        :param value_type: Whether the measurement is an integer, a floating-point number, etc. Some combinations of metricKind and valueType might not be supported. For counter metrics, set this to INT64. Possible values: ["BOOL", "INT64", "DOUBLE", "STRING", "DISTRIBUTION", "MONEY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#value_type LoggingMetric#value_type}
        :param display_name: A concise name for the metric, which can be displayed in user interfaces. Use sentence case without an ending period, for example "Request count". This field is optional but it is recommended to be set for any metrics associated with user-visible concepts, such as Quota. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#display_name LoggingMetric#display_name}
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#labels LoggingMetric#labels}
        :param unit: The unit in which the metric value is reported. It is only applicable if the valueType is 'INT64', 'DOUBLE', or 'DISTRIBUTION'. The supported units are a subset of `The Unified Code for Units of Measure <http://unitsofmeasure.org/ucum.html>`_ standard Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#unit LoggingMetric#unit}
        '''
        value = LoggingMetricMetricDescriptor(
            metric_kind=metric_kind,
            value_type=value_type,
            display_name=display_name,
            labels=labels,
            unit=unit,
        )

        return typing.cast(None, jsii.invoke(self, "putMetricDescriptor", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#create LoggingMetric#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#delete LoggingMetric#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#update LoggingMetric#update}.
        '''
        value = LoggingMetricTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketOptions")
    def reset_bucket_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketOptions", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabelExtractors")
    def reset_label_extractors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabelExtractors", []))

    @jsii.member(jsii_name="resetMetricDescriptor")
    def reset_metric_descriptor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricDescriptor", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetValueExtractor")
    def reset_value_extractor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueExtractor", []))

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
    @jsii.member(jsii_name="bucketOptions")
    def bucket_options(self) -> "LoggingMetricBucketOptionsOutputReference":
        return typing.cast("LoggingMetricBucketOptionsOutputReference", jsii.get(self, "bucketOptions"))

    @builtins.property
    @jsii.member(jsii_name="metricDescriptor")
    def metric_descriptor(self) -> "LoggingMetricMetricDescriptorOutputReference":
        return typing.cast("LoggingMetricMetricDescriptorOutputReference", jsii.get(self, "metricDescriptor"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "LoggingMetricTimeoutsOutputReference":
        return typing.cast("LoggingMetricTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketOptionsInput")
    def bucket_options_input(self) -> typing.Optional["LoggingMetricBucketOptions"]:
        return typing.cast(typing.Optional["LoggingMetricBucketOptions"], jsii.get(self, "bucketOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelExtractorsInput")
    def label_extractors_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelExtractorsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricDescriptorInput")
    def metric_descriptor_input(
        self,
    ) -> typing.Optional["LoggingMetricMetricDescriptor"]:
        return typing.cast(typing.Optional["LoggingMetricMetricDescriptor"], jsii.get(self, "metricDescriptorInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LoggingMetricTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LoggingMetricTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="valueExtractorInput")
    def value_extractor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueExtractorInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c71022270ee5ed1691299d9c69a30b85b22858bee37fee2d6281029d3d3980e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41e2aa3ee1ffc86d37f7b8173775141baa24b49a2707061dfb1dd37de3577863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4487ebf8035a550f50d685d9c31fbf1ac72bd6dc4820a716084ddc9fd7477c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f97589d088dbffe6320597af4b761089defbcc49bd345b65c91d9740b7481a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b705cb6f6153f02505c8c001dad506e1571f08f0146dbfcde752576bce21e610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labelExtractors")
    def label_extractors(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labelExtractors"))

    @label_extractors.setter
    def label_extractors(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eefeb71c4bc0d53995880dc0ec7f150f57a030527f6cbfbc8ad9a01da58e14e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labelExtractors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f6c1367fcd180658bc3f888bf34994c0753855f65d9f97f1977afd057f81b58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ccd155f3ca3f02300e95d2cbc60b5b01d7de6aa7c865113213f3d9a56f4aa95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valueExtractor")
    def value_extractor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueExtractor"))

    @value_extractor.setter
    def value_extractor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a09726559cf10b53cc8ba3bf4645d61950c74dc62a48ca65a1aa2b12654c9e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueExtractor", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.loggingMetric.LoggingMetricBucketOptions",
    jsii_struct_bases=[],
    name_mapping={
        "explicit_buckets": "explicitBuckets",
        "exponential_buckets": "exponentialBuckets",
        "linear_buckets": "linearBuckets",
    },
)
class LoggingMetricBucketOptions:
    def __init__(
        self,
        *,
        explicit_buckets: typing.Optional[typing.Union["LoggingMetricBucketOptionsExplicitBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        exponential_buckets: typing.Optional[typing.Union["LoggingMetricBucketOptionsExponentialBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        linear_buckets: typing.Optional[typing.Union["LoggingMetricBucketOptionsLinearBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param explicit_buckets: explicit_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#explicit_buckets LoggingMetric#explicit_buckets}
        :param exponential_buckets: exponential_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#exponential_buckets LoggingMetric#exponential_buckets}
        :param linear_buckets: linear_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#linear_buckets LoggingMetric#linear_buckets}
        '''
        if isinstance(explicit_buckets, dict):
            explicit_buckets = LoggingMetricBucketOptionsExplicitBuckets(**explicit_buckets)
        if isinstance(exponential_buckets, dict):
            exponential_buckets = LoggingMetricBucketOptionsExponentialBuckets(**exponential_buckets)
        if isinstance(linear_buckets, dict):
            linear_buckets = LoggingMetricBucketOptionsLinearBuckets(**linear_buckets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5f8a8cef61feb1877424343b7333f39f57ebc5bb0b97395431ac80879622cd1)
            check_type(argname="argument explicit_buckets", value=explicit_buckets, expected_type=type_hints["explicit_buckets"])
            check_type(argname="argument exponential_buckets", value=exponential_buckets, expected_type=type_hints["exponential_buckets"])
            check_type(argname="argument linear_buckets", value=linear_buckets, expected_type=type_hints["linear_buckets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if explicit_buckets is not None:
            self._values["explicit_buckets"] = explicit_buckets
        if exponential_buckets is not None:
            self._values["exponential_buckets"] = exponential_buckets
        if linear_buckets is not None:
            self._values["linear_buckets"] = linear_buckets

    @builtins.property
    def explicit_buckets(
        self,
    ) -> typing.Optional["LoggingMetricBucketOptionsExplicitBuckets"]:
        '''explicit_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#explicit_buckets LoggingMetric#explicit_buckets}
        '''
        result = self._values.get("explicit_buckets")
        return typing.cast(typing.Optional["LoggingMetricBucketOptionsExplicitBuckets"], result)

    @builtins.property
    def exponential_buckets(
        self,
    ) -> typing.Optional["LoggingMetricBucketOptionsExponentialBuckets"]:
        '''exponential_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#exponential_buckets LoggingMetric#exponential_buckets}
        '''
        result = self._values.get("exponential_buckets")
        return typing.cast(typing.Optional["LoggingMetricBucketOptionsExponentialBuckets"], result)

    @builtins.property
    def linear_buckets(
        self,
    ) -> typing.Optional["LoggingMetricBucketOptionsLinearBuckets"]:
        '''linear_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#linear_buckets LoggingMetric#linear_buckets}
        '''
        result = self._values.get("linear_buckets")
        return typing.cast(typing.Optional["LoggingMetricBucketOptionsLinearBuckets"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingMetricBucketOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.loggingMetric.LoggingMetricBucketOptionsExplicitBuckets",
    jsii_struct_bases=[],
    name_mapping={"bounds": "bounds"},
)
class LoggingMetricBucketOptionsExplicitBuckets:
    def __init__(self, *, bounds: typing.Sequence[jsii.Number]) -> None:
        '''
        :param bounds: The values must be monotonically increasing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#bounds LoggingMetric#bounds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82c89d9902918288103066aba5b6af26573431c0dd3e37c02f11044c8ac935ea)
            check_type(argname="argument bounds", value=bounds, expected_type=type_hints["bounds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bounds": bounds,
        }

    @builtins.property
    def bounds(self) -> typing.List[jsii.Number]:
        '''The values must be monotonically increasing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#bounds LoggingMetric#bounds}
        '''
        result = self._values.get("bounds")
        assert result is not None, "Required property 'bounds' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingMetricBucketOptionsExplicitBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoggingMetricBucketOptionsExplicitBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.loggingMetric.LoggingMetricBucketOptionsExplicitBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c33aeec2d143e34af15c4271f7916706a419b870311f2bb324a9f58d4b085eeb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="boundsInput")
    def bounds_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "boundsInput"))

    @builtins.property
    @jsii.member(jsii_name="bounds")
    def bounds(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "bounds"))

    @bounds.setter
    def bounds(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e81b67dbd8154712d5a11d948312349b73fe6e18dcea367855cf833fd4efcaf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bounds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LoggingMetricBucketOptionsExplicitBuckets]:
        return typing.cast(typing.Optional[LoggingMetricBucketOptionsExplicitBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LoggingMetricBucketOptionsExplicitBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__929b3dca7d1122c2147e58c03400270443be081ccdfbbf2b4e7b3d5b7599e9ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.loggingMetric.LoggingMetricBucketOptionsExponentialBuckets",
    jsii_struct_bases=[],
    name_mapping={
        "growth_factor": "growthFactor",
        "num_finite_buckets": "numFiniteBuckets",
        "scale": "scale",
    },
)
class LoggingMetricBucketOptionsExponentialBuckets:
    def __init__(
        self,
        *,
        growth_factor: jsii.Number,
        num_finite_buckets: jsii.Number,
        scale: jsii.Number,
    ) -> None:
        '''
        :param growth_factor: Must be greater than 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#growth_factor LoggingMetric#growth_factor}
        :param num_finite_buckets: Must be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#num_finite_buckets LoggingMetric#num_finite_buckets}
        :param scale: Must be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#scale LoggingMetric#scale}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0099bca4383ea9e958177620d106a68c9cfd55885caf7cb4849be5ffd3b6f6db)
            check_type(argname="argument growth_factor", value=growth_factor, expected_type=type_hints["growth_factor"])
            check_type(argname="argument num_finite_buckets", value=num_finite_buckets, expected_type=type_hints["num_finite_buckets"])
            check_type(argname="argument scale", value=scale, expected_type=type_hints["scale"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "growth_factor": growth_factor,
            "num_finite_buckets": num_finite_buckets,
            "scale": scale,
        }

    @builtins.property
    def growth_factor(self) -> jsii.Number:
        '''Must be greater than 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#growth_factor LoggingMetric#growth_factor}
        '''
        result = self._values.get("growth_factor")
        assert result is not None, "Required property 'growth_factor' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def num_finite_buckets(self) -> jsii.Number:
        '''Must be greater than 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#num_finite_buckets LoggingMetric#num_finite_buckets}
        '''
        result = self._values.get("num_finite_buckets")
        assert result is not None, "Required property 'num_finite_buckets' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale(self) -> jsii.Number:
        '''Must be greater than 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#scale LoggingMetric#scale}
        '''
        result = self._values.get("scale")
        assert result is not None, "Required property 'scale' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingMetricBucketOptionsExponentialBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoggingMetricBucketOptionsExponentialBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.loggingMetric.LoggingMetricBucketOptionsExponentialBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c73d70fe72a6476ccc93c1c0a79d9193b5ee38533bca646341b38caae0f2f58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="growthFactorInput")
    def growth_factor_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "growthFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="numFiniteBucketsInput")
    def num_finite_buckets_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numFiniteBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleInput")
    def scale_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleInput"))

    @builtins.property
    @jsii.member(jsii_name="growthFactor")
    def growth_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "growthFactor"))

    @growth_factor.setter
    def growth_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a43e2ffe1025a3a3acd7d736537db4a9ecca7571c720d36f581fdabbf479573)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "growthFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numFiniteBuckets")
    def num_finite_buckets(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numFiniteBuckets"))

    @num_finite_buckets.setter
    def num_finite_buckets(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcd013e698cb2f5cc4cf8eb386c99499430c368c26ec7d96d55f243f7fa66750)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numFiniteBuckets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scale")
    def scale(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scale"))

    @scale.setter
    def scale(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__621829c976b7be5e41bb72a6f713420f0f400ffa31303d5ab2bcc76e151d2387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scale", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LoggingMetricBucketOptionsExponentialBuckets]:
        return typing.cast(typing.Optional[LoggingMetricBucketOptionsExponentialBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LoggingMetricBucketOptionsExponentialBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1c19f9ec722164297846ea39d1a48fe9504c9b45fd2f344ddf53591568ae849)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.loggingMetric.LoggingMetricBucketOptionsLinearBuckets",
    jsii_struct_bases=[],
    name_mapping={
        "num_finite_buckets": "numFiniteBuckets",
        "offset": "offset",
        "width": "width",
    },
)
class LoggingMetricBucketOptionsLinearBuckets:
    def __init__(
        self,
        *,
        num_finite_buckets: jsii.Number,
        offset: jsii.Number,
        width: jsii.Number,
    ) -> None:
        '''
        :param num_finite_buckets: Must be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#num_finite_buckets LoggingMetric#num_finite_buckets}
        :param offset: Lower bound of the first bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#offset LoggingMetric#offset}
        :param width: Must be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#width LoggingMetric#width}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f312145c745b854a4671e66ec7f0919b32bb83c201c5522d7719b0b7cf1365b5)
            check_type(argname="argument num_finite_buckets", value=num_finite_buckets, expected_type=type_hints["num_finite_buckets"])
            check_type(argname="argument offset", value=offset, expected_type=type_hints["offset"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "num_finite_buckets": num_finite_buckets,
            "offset": offset,
            "width": width,
        }

    @builtins.property
    def num_finite_buckets(self) -> jsii.Number:
        '''Must be greater than 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#num_finite_buckets LoggingMetric#num_finite_buckets}
        '''
        result = self._values.get("num_finite_buckets")
        assert result is not None, "Required property 'num_finite_buckets' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def offset(self) -> jsii.Number:
        '''Lower bound of the first bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#offset LoggingMetric#offset}
        '''
        result = self._values.get("offset")
        assert result is not None, "Required property 'offset' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def width(self) -> jsii.Number:
        '''Must be greater than 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#width LoggingMetric#width}
        '''
        result = self._values.get("width")
        assert result is not None, "Required property 'width' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingMetricBucketOptionsLinearBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoggingMetricBucketOptionsLinearBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.loggingMetric.LoggingMetricBucketOptionsLinearBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d26f467faaface2875a6ebd367073b10e822ec8603cd215cd955e7a1e2c9594)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="numFiniteBucketsInput")
    def num_finite_buckets_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numFiniteBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="offsetInput")
    def offset_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "offsetInput"))

    @builtins.property
    @jsii.member(jsii_name="widthInput")
    def width_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "widthInput"))

    @builtins.property
    @jsii.member(jsii_name="numFiniteBuckets")
    def num_finite_buckets(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numFiniteBuckets"))

    @num_finite_buckets.setter
    def num_finite_buckets(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f1f6709d3216f5ad768921f5b4ad5dcf0f0d92ed57d88d91f71ff77fe1291ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numFiniteBuckets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="offset")
    def offset(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "offset"))

    @offset.setter
    def offset(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edc25012f89c42844cdfd7a99b4e47589670a6680109a672479c67f5b0954dab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "width"))

    @width.setter
    def width(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d49118bdb6c061c9d7ff25cbc0af98f2eff47efb80fadc1dceb6c208be5d951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "width", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LoggingMetricBucketOptionsLinearBuckets]:
        return typing.cast(typing.Optional[LoggingMetricBucketOptionsLinearBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LoggingMetricBucketOptionsLinearBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__034c45fe5cf17fbde26d194006ac8a2e8acd1a10cb314ebef09b95ce2f92f99d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LoggingMetricBucketOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.loggingMetric.LoggingMetricBucketOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fef223d100b05324035556adc47a590c5042f845171aa24a82d7535666eb734)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExplicitBuckets")
    def put_explicit_buckets(self, *, bounds: typing.Sequence[jsii.Number]) -> None:
        '''
        :param bounds: The values must be monotonically increasing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#bounds LoggingMetric#bounds}
        '''
        value = LoggingMetricBucketOptionsExplicitBuckets(bounds=bounds)

        return typing.cast(None, jsii.invoke(self, "putExplicitBuckets", [value]))

    @jsii.member(jsii_name="putExponentialBuckets")
    def put_exponential_buckets(
        self,
        *,
        growth_factor: jsii.Number,
        num_finite_buckets: jsii.Number,
        scale: jsii.Number,
    ) -> None:
        '''
        :param growth_factor: Must be greater than 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#growth_factor LoggingMetric#growth_factor}
        :param num_finite_buckets: Must be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#num_finite_buckets LoggingMetric#num_finite_buckets}
        :param scale: Must be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#scale LoggingMetric#scale}
        '''
        value = LoggingMetricBucketOptionsExponentialBuckets(
            growth_factor=growth_factor,
            num_finite_buckets=num_finite_buckets,
            scale=scale,
        )

        return typing.cast(None, jsii.invoke(self, "putExponentialBuckets", [value]))

    @jsii.member(jsii_name="putLinearBuckets")
    def put_linear_buckets(
        self,
        *,
        num_finite_buckets: jsii.Number,
        offset: jsii.Number,
        width: jsii.Number,
    ) -> None:
        '''
        :param num_finite_buckets: Must be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#num_finite_buckets LoggingMetric#num_finite_buckets}
        :param offset: Lower bound of the first bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#offset LoggingMetric#offset}
        :param width: Must be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#width LoggingMetric#width}
        '''
        value = LoggingMetricBucketOptionsLinearBuckets(
            num_finite_buckets=num_finite_buckets, offset=offset, width=width
        )

        return typing.cast(None, jsii.invoke(self, "putLinearBuckets", [value]))

    @jsii.member(jsii_name="resetExplicitBuckets")
    def reset_explicit_buckets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExplicitBuckets", []))

    @jsii.member(jsii_name="resetExponentialBuckets")
    def reset_exponential_buckets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExponentialBuckets", []))

    @jsii.member(jsii_name="resetLinearBuckets")
    def reset_linear_buckets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinearBuckets", []))

    @builtins.property
    @jsii.member(jsii_name="explicitBuckets")
    def explicit_buckets(
        self,
    ) -> LoggingMetricBucketOptionsExplicitBucketsOutputReference:
        return typing.cast(LoggingMetricBucketOptionsExplicitBucketsOutputReference, jsii.get(self, "explicitBuckets"))

    @builtins.property
    @jsii.member(jsii_name="exponentialBuckets")
    def exponential_buckets(
        self,
    ) -> LoggingMetricBucketOptionsExponentialBucketsOutputReference:
        return typing.cast(LoggingMetricBucketOptionsExponentialBucketsOutputReference, jsii.get(self, "exponentialBuckets"))

    @builtins.property
    @jsii.member(jsii_name="linearBuckets")
    def linear_buckets(self) -> LoggingMetricBucketOptionsLinearBucketsOutputReference:
        return typing.cast(LoggingMetricBucketOptionsLinearBucketsOutputReference, jsii.get(self, "linearBuckets"))

    @builtins.property
    @jsii.member(jsii_name="explicitBucketsInput")
    def explicit_buckets_input(
        self,
    ) -> typing.Optional[LoggingMetricBucketOptionsExplicitBuckets]:
        return typing.cast(typing.Optional[LoggingMetricBucketOptionsExplicitBuckets], jsii.get(self, "explicitBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="exponentialBucketsInput")
    def exponential_buckets_input(
        self,
    ) -> typing.Optional[LoggingMetricBucketOptionsExponentialBuckets]:
        return typing.cast(typing.Optional[LoggingMetricBucketOptionsExponentialBuckets], jsii.get(self, "exponentialBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="linearBucketsInput")
    def linear_buckets_input(
        self,
    ) -> typing.Optional[LoggingMetricBucketOptionsLinearBuckets]:
        return typing.cast(typing.Optional[LoggingMetricBucketOptionsLinearBuckets], jsii.get(self, "linearBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LoggingMetricBucketOptions]:
        return typing.cast(typing.Optional[LoggingMetricBucketOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LoggingMetricBucketOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e704f1c1ef60b50bdf912f772d9dd424654998cd67fe4a4f2b22c1e44fd38fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.loggingMetric.LoggingMetricConfig",
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
        "name": "name",
        "bucket_name": "bucketName",
        "bucket_options": "bucketOptions",
        "description": "description",
        "disabled": "disabled",
        "id": "id",
        "label_extractors": "labelExtractors",
        "metric_descriptor": "metricDescriptor",
        "project": "project",
        "timeouts": "timeouts",
        "value_extractor": "valueExtractor",
    },
)
class LoggingMetricConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_options: typing.Optional[typing.Union[LoggingMetricBucketOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        label_extractors: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metric_descriptor: typing.Optional[typing.Union["LoggingMetricMetricDescriptor", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["LoggingMetricTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        value_extractor: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param filter: An advanced logs filter (https://cloud.google.com/logging/docs/view/advanced-filters) which is used to match log entries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#filter LoggingMetric#filter}
        :param name: The client-assigned metric identifier. Examples - "error_count", "nginx/requests". Metric identifiers are limited to 100 characters and can include only the following characters A-Z, a-z, 0-9, and the special characters _-.,+!*',()%/. The forward-slash character (/) denotes a hierarchy of name pieces, and it cannot be the first character of the name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#name LoggingMetric#name}
        :param bucket_name: The resource name of the Log Bucket that owns the Log Metric. Only Log Buckets in projects are supported. The bucket has to be in the same project as the metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#bucket_name LoggingMetric#bucket_name}
        :param bucket_options: bucket_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#bucket_options LoggingMetric#bucket_options}
        :param description: A description of this metric, which is used in documentation. The maximum length of the description is 8000 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#description LoggingMetric#description}
        :param disabled: If set to True, then this metric is disabled and it does not generate any points. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#disabled LoggingMetric#disabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#id LoggingMetric#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param label_extractors: A map from a label key string to an extractor expression which is used to extract data from a log entry field and assign as the label value. Each label key specified in the LabelDescriptor must have an associated extractor expression in this map. The syntax of the extractor expression is the same as for the valueExtractor field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#label_extractors LoggingMetric#label_extractors}
        :param metric_descriptor: metric_descriptor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#metric_descriptor LoggingMetric#metric_descriptor}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#project LoggingMetric#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#timeouts LoggingMetric#timeouts}
        :param value_extractor: A valueExtractor is required when using a distribution logs-based metric to extract the values to record from a log entry. Two functions are supported for value extraction - EXTRACT(field) or REGEXP_EXTRACT(field, regex). The argument are 1. field - The name of the log entry field from which the value is to be extracted. 2. regex - A regular expression using the Google RE2 syntax (https://github.com/google/re2/wiki/Syntax) with a single capture group to extract data from the specified log entry field. The value of the field is converted to a string before applying the regex. It is an error to specify a regex that does not include exactly one capture group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#value_extractor LoggingMetric#value_extractor}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bucket_options, dict):
            bucket_options = LoggingMetricBucketOptions(**bucket_options)
        if isinstance(metric_descriptor, dict):
            metric_descriptor = LoggingMetricMetricDescriptor(**metric_descriptor)
        if isinstance(timeouts, dict):
            timeouts = LoggingMetricTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69a3107b5ebcf240927d9623e15f5e3d0704a5b2758904eea3ad1f67380f3046)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_options", value=bucket_options, expected_type=type_hints["bucket_options"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument label_extractors", value=label_extractors, expected_type=type_hints["label_extractors"])
            check_type(argname="argument metric_descriptor", value=metric_descriptor, expected_type=type_hints["metric_descriptor"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument value_extractor", value=value_extractor, expected_type=type_hints["value_extractor"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_options is not None:
            self._values["bucket_options"] = bucket_options
        if description is not None:
            self._values["description"] = description
        if disabled is not None:
            self._values["disabled"] = disabled
        if id is not None:
            self._values["id"] = id
        if label_extractors is not None:
            self._values["label_extractors"] = label_extractors
        if metric_descriptor is not None:
            self._values["metric_descriptor"] = metric_descriptor
        if project is not None:
            self._values["project"] = project
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if value_extractor is not None:
            self._values["value_extractor"] = value_extractor

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
        '''An advanced logs filter (https://cloud.google.com/logging/docs/view/advanced-filters) which is used to match log entries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#filter LoggingMetric#filter}
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The client-assigned metric identifier.

        Examples - "error_count", "nginx/requests".
        Metric identifiers are limited to 100 characters and can include only the following
        characters A-Z, a-z, 0-9, and the special characters _-.,+!*',()%/. The forward-slash
        character (/) denotes a hierarchy of name pieces, and it cannot be the first character
        of the name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#name LoggingMetric#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''The resource name of the Log Bucket that owns the Log Metric.

        Only Log Buckets in projects
        are supported. The bucket has to be in the same project as the metric.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#bucket_name LoggingMetric#bucket_name}
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_options(self) -> typing.Optional[LoggingMetricBucketOptions]:
        '''bucket_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#bucket_options LoggingMetric#bucket_options}
        '''
        result = self._values.get("bucket_options")
        return typing.cast(typing.Optional[LoggingMetricBucketOptions], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of this metric, which is used in documentation. The maximum length of the description is 8000 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#description LoggingMetric#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to True, then this metric is disabled and it does not generate any points.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#disabled LoggingMetric#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#id LoggingMetric#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def label_extractors(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map from a label key string to an extractor expression which is used to extract data from a log entry field and assign as the label value.

        Each label key specified in the LabelDescriptor must
        have an associated extractor expression in this map. The syntax of the extractor expression is
        the same as for the valueExtractor field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#label_extractors LoggingMetric#label_extractors}
        '''
        result = self._values.get("label_extractors")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metric_descriptor(self) -> typing.Optional["LoggingMetricMetricDescriptor"]:
        '''metric_descriptor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#metric_descriptor LoggingMetric#metric_descriptor}
        '''
        result = self._values.get("metric_descriptor")
        return typing.cast(typing.Optional["LoggingMetricMetricDescriptor"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#project LoggingMetric#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["LoggingMetricTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#timeouts LoggingMetric#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["LoggingMetricTimeouts"], result)

    @builtins.property
    def value_extractor(self) -> typing.Optional[builtins.str]:
        '''A valueExtractor is required when using a distribution logs-based metric to extract the values to record from a log entry.

        Two functions are supported for value extraction - EXTRACT(field) or
        REGEXP_EXTRACT(field, regex). The argument are 1. field - The name of the log entry field from which
        the value is to be extracted. 2. regex - A regular expression using the Google RE2 syntax
        (https://github.com/google/re2/wiki/Syntax) with a single capture group to extract data from the specified
        log entry field. The value of the field is converted to a string before applying the regex. It is an
        error to specify a regex that does not include exactly one capture group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#value_extractor LoggingMetric#value_extractor}
        '''
        result = self._values.get("value_extractor")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingMetricConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.loggingMetric.LoggingMetricMetricDescriptor",
    jsii_struct_bases=[],
    name_mapping={
        "metric_kind": "metricKind",
        "value_type": "valueType",
        "display_name": "displayName",
        "labels": "labels",
        "unit": "unit",
    },
)
class LoggingMetricMetricDescriptor:
    def __init__(
        self,
        *,
        metric_kind: builtins.str,
        value_type: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoggingMetricMetricDescriptorLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metric_kind: Whether the metric records instantaneous values, changes to a value, etc. Some combinations of metricKind and valueType might not be supported. For counter metrics, set this to DELTA. Possible values: ["DELTA", "GAUGE", "CUMULATIVE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#metric_kind LoggingMetric#metric_kind}
        :param value_type: Whether the measurement is an integer, a floating-point number, etc. Some combinations of metricKind and valueType might not be supported. For counter metrics, set this to INT64. Possible values: ["BOOL", "INT64", "DOUBLE", "STRING", "DISTRIBUTION", "MONEY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#value_type LoggingMetric#value_type}
        :param display_name: A concise name for the metric, which can be displayed in user interfaces. Use sentence case without an ending period, for example "Request count". This field is optional but it is recommended to be set for any metrics associated with user-visible concepts, such as Quota. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#display_name LoggingMetric#display_name}
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#labels LoggingMetric#labels}
        :param unit: The unit in which the metric value is reported. It is only applicable if the valueType is 'INT64', 'DOUBLE', or 'DISTRIBUTION'. The supported units are a subset of `The Unified Code for Units of Measure <http://unitsofmeasure.org/ucum.html>`_ standard Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#unit LoggingMetric#unit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59a1661b616a5a922f86ea4ebafb09ccae20db1b27ae091a22ad387463999761)
            check_type(argname="argument metric_kind", value=metric_kind, expected_type=type_hints["metric_kind"])
            check_type(argname="argument value_type", value=value_type, expected_type=type_hints["value_type"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_kind": metric_kind,
            "value_type": value_type,
        }
        if display_name is not None:
            self._values["display_name"] = display_name
        if labels is not None:
            self._values["labels"] = labels
        if unit is not None:
            self._values["unit"] = unit

    @builtins.property
    def metric_kind(self) -> builtins.str:
        '''Whether the metric records instantaneous values, changes to a value, etc.

        Some combinations of metricKind and valueType might not be supported.
        For counter metrics, set this to DELTA. Possible values: ["DELTA", "GAUGE", "CUMULATIVE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#metric_kind LoggingMetric#metric_kind}
        '''
        result = self._values.get("metric_kind")
        assert result is not None, "Required property 'metric_kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value_type(self) -> builtins.str:
        '''Whether the measurement is an integer, a floating-point number, etc.

        Some combinations of metricKind and valueType might not be supported.
        For counter metrics, set this to INT64. Possible values: ["BOOL", "INT64", "DOUBLE", "STRING", "DISTRIBUTION", "MONEY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#value_type LoggingMetric#value_type}
        '''
        result = self._values.get("value_type")
        assert result is not None, "Required property 'value_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''A concise name for the metric, which can be displayed in user interfaces.

        Use sentence case
        without an ending period, for example "Request count". This field is optional but it is
        recommended to be set for any metrics associated with user-visible concepts, such as Quota.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#display_name LoggingMetric#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoggingMetricMetricDescriptorLabels"]]]:
        '''labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#labels LoggingMetric#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoggingMetricMetricDescriptorLabels"]]], result)

    @builtins.property
    def unit(self) -> typing.Optional[builtins.str]:
        '''The unit in which the metric value is reported.

        It is only applicable if the valueType is
        'INT64', 'DOUBLE', or 'DISTRIBUTION'. The supported units are a subset of
        `The Unified Code for Units of Measure <http://unitsofmeasure.org/ucum.html>`_ standard

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#unit LoggingMetric#unit}
        '''
        result = self._values.get("unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingMetricMetricDescriptor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.loggingMetric.LoggingMetricMetricDescriptorLabels",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "description": "description",
        "value_type": "valueType",
    },
)
class LoggingMetricMetricDescriptorLabels:
    def __init__(
        self,
        *,
        key: builtins.str,
        description: typing.Optional[builtins.str] = None,
        value_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: The label key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#key LoggingMetric#key}
        :param description: A human-readable description for the label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#description LoggingMetric#description}
        :param value_type: The type of data that can be assigned to the label. Default value: "STRING" Possible values: ["BOOL", "INT64", "STRING"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#value_type LoggingMetric#value_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04809fc8d569fa88e4a60ca0d1d2c82b8d23f910c29a3969ed44671a11e121bd)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument value_type", value=value_type, expected_type=type_hints["value_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if description is not None:
            self._values["description"] = description
        if value_type is not None:
            self._values["value_type"] = value_type

    @builtins.property
    def key(self) -> builtins.str:
        '''The label key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#key LoggingMetric#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description for the label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#description LoggingMetric#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_type(self) -> typing.Optional[builtins.str]:
        '''The type of data that can be assigned to the label. Default value: "STRING" Possible values: ["BOOL", "INT64", "STRING"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#value_type LoggingMetric#value_type}
        '''
        result = self._values.get("value_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingMetricMetricDescriptorLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoggingMetricMetricDescriptorLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.loggingMetric.LoggingMetricMetricDescriptorLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3998a5703b692cde1cc3fae671d4d15599bfa2fbcdb66f2277aacab8ca0b781f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LoggingMetricMetricDescriptorLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9486146495c033d1be4e8d522d7680c1864455bd94c3ee2aaa82729b2be8610)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoggingMetricMetricDescriptorLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f4c700eadc3374c5abda490773a6482d44cc82587b93b1feb94360df49ccfe5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c5bf8fcc5607647272ece83b1ad8424238f59d715eb421fa93a5df41a1d21fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68a05146f93c297266613ad4c6347b263031866248c96826d555c24d74b5de89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoggingMetricMetricDescriptorLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoggingMetricMetricDescriptorLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoggingMetricMetricDescriptorLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebcd75660e9dc45994c4e0e049b11e6d3b0212d8272b13cc138723744329a4ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LoggingMetricMetricDescriptorLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.loggingMetric.LoggingMetricMetricDescriptorLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2b2d6a74b78be08b415200baab0257f90aa75332996ca5fc4810a5eaef5ef91)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetValueType")
    def reset_value_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueType", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueTypeInput")
    def value_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e90c0c8e3878692a2e14a7a1ff64e0818583bf38bbcc1fc5d10b4d3e668a2ab9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5092c1b0c694b484bd60413992e5aea0499edaabb9b4d9d15f33e108859945b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valueType")
    def value_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueType"))

    @value_type.setter
    def value_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b16cde0bcbc7fdd154911e1a906ccadefb681f5683d013fcc46c1307aba3dece)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LoggingMetricMetricDescriptorLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LoggingMetricMetricDescriptorLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LoggingMetricMetricDescriptorLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ad0d793f4082bc7f2135ba6a3c2ce17284309eddaddfd7b04876a73c842f282)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LoggingMetricMetricDescriptorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.loggingMetric.LoggingMetricMetricDescriptorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7a828676d04c28e3256369d9413c2a9d182c0e60fcefb6045f3df87a952a3bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLabels")
    def put_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoggingMetricMetricDescriptorLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f50d555f12f6bd57dd7f0c96f2caede6b73f37fb5ac3b4a8ebc937c4dc0c49b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLabels", [value]))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetUnit")
    def reset_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnit", []))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> LoggingMetricMetricDescriptorLabelsList:
        return typing.cast(LoggingMetricMetricDescriptorLabelsList, jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoggingMetricMetricDescriptorLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoggingMetricMetricDescriptorLabels]]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricKindInput")
    def metric_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricKindInput"))

    @builtins.property
    @jsii.member(jsii_name="unitInput")
    def unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitInput"))

    @builtins.property
    @jsii.member(jsii_name="valueTypeInput")
    def value_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff207b5fe2b26c348af6424388d1e7eeeed1d5ecec27f990131cf5381904026)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricKind")
    def metric_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricKind"))

    @metric_kind.setter
    def metric_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__660e35881fa83f15bed63e47ec315e6d9ad5956076355f1a9cc2c184256d9e10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unit"))

    @unit.setter
    def unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00f6839162e7b0e1dee9abd605909fca1d493e59d09bcaabf980dbe165452381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valueType")
    def value_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueType"))

    @value_type.setter
    def value_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43636ceb245a25e73c36b7c85c4e22b86540421f2b7a17ae7392c2a414b43eca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LoggingMetricMetricDescriptor]:
        return typing.cast(typing.Optional[LoggingMetricMetricDescriptor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LoggingMetricMetricDescriptor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3c9d27afc1dfe8bd88cf6f03bb9b548d8ebb406109c48745b87984a64d65746)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.loggingMetric.LoggingMetricTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class LoggingMetricTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#create LoggingMetric#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#delete LoggingMetric#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#update LoggingMetric#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99647e048a05e2c981557d02572c74fadfbb4106c7ffd8b3ca269ec8c4e34c1e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#create LoggingMetric#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#delete LoggingMetric#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/logging_metric#update LoggingMetric#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingMetricTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoggingMetricTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.loggingMetric.LoggingMetricTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd1354096eb45e04f2f1ac791d91354c08f8f03d53b6de0f53c824eba254e2b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a3c97b6aa25ef1fb812149c71c2d2c194a346b6edc4997baa12ff89ddea044d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__238427bf973bc6adcc7cfd1f6c05bf78cf5a4e2ee9c5b3e9f539e76e77ca9fe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6ca8b3b933fa71f81e03a9fe5c02ff12a0ec87f488019ebd7b6fcd27633b292)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LoggingMetricTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LoggingMetricTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LoggingMetricTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__057a05970b2af9043afd993216fc587feb91b8a2978d4fd1f53724ce1a43723a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LoggingMetric",
    "LoggingMetricBucketOptions",
    "LoggingMetricBucketOptionsExplicitBuckets",
    "LoggingMetricBucketOptionsExplicitBucketsOutputReference",
    "LoggingMetricBucketOptionsExponentialBuckets",
    "LoggingMetricBucketOptionsExponentialBucketsOutputReference",
    "LoggingMetricBucketOptionsLinearBuckets",
    "LoggingMetricBucketOptionsLinearBucketsOutputReference",
    "LoggingMetricBucketOptionsOutputReference",
    "LoggingMetricConfig",
    "LoggingMetricMetricDescriptor",
    "LoggingMetricMetricDescriptorLabels",
    "LoggingMetricMetricDescriptorLabelsList",
    "LoggingMetricMetricDescriptorLabelsOutputReference",
    "LoggingMetricMetricDescriptorOutputReference",
    "LoggingMetricTimeouts",
    "LoggingMetricTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__21e7ef5033d7c455eb6f2708a4b7786962373f75322014eebcacb52b5381f6f9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    filter: builtins.str,
    name: builtins.str,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_options: typing.Optional[typing.Union[LoggingMetricBucketOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    label_extractors: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metric_descriptor: typing.Optional[typing.Union[LoggingMetricMetricDescriptor, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[LoggingMetricTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    value_extractor: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__a1f859b357a789d027991213cd666dc5d4c8c7e1c14f69ecc1082927ce8afbc3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c71022270ee5ed1691299d9c69a30b85b22858bee37fee2d6281029d3d3980e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e2aa3ee1ffc86d37f7b8173775141baa24b49a2707061dfb1dd37de3577863(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4487ebf8035a550f50d685d9c31fbf1ac72bd6dc4820a716084ddc9fd7477c7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f97589d088dbffe6320597af4b761089defbcc49bd345b65c91d9740b7481a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b705cb6f6153f02505c8c001dad506e1571f08f0146dbfcde752576bce21e610(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eefeb71c4bc0d53995880dc0ec7f150f57a030527f6cbfbc8ad9a01da58e14e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f6c1367fcd180658bc3f888bf34994c0753855f65d9f97f1977afd057f81b58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ccd155f3ca3f02300e95d2cbc60b5b01d7de6aa7c865113213f3d9a56f4aa95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a09726559cf10b53cc8ba3bf4645d61950c74dc62a48ca65a1aa2b12654c9e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f8a8cef61feb1877424343b7333f39f57ebc5bb0b97395431ac80879622cd1(
    *,
    explicit_buckets: typing.Optional[typing.Union[LoggingMetricBucketOptionsExplicitBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    exponential_buckets: typing.Optional[typing.Union[LoggingMetricBucketOptionsExponentialBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    linear_buckets: typing.Optional[typing.Union[LoggingMetricBucketOptionsLinearBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82c89d9902918288103066aba5b6af26573431c0dd3e37c02f11044c8ac935ea(
    *,
    bounds: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33aeec2d143e34af15c4271f7916706a419b870311f2bb324a9f58d4b085eeb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e81b67dbd8154712d5a11d948312349b73fe6e18dcea367855cf833fd4efcaf4(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__929b3dca7d1122c2147e58c03400270443be081ccdfbbf2b4e7b3d5b7599e9ae(
    value: typing.Optional[LoggingMetricBucketOptionsExplicitBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0099bca4383ea9e958177620d106a68c9cfd55885caf7cb4849be5ffd3b6f6db(
    *,
    growth_factor: jsii.Number,
    num_finite_buckets: jsii.Number,
    scale: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c73d70fe72a6476ccc93c1c0a79d9193b5ee38533bca646341b38caae0f2f58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a43e2ffe1025a3a3acd7d736537db4a9ecca7571c720d36f581fdabbf479573(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd013e698cb2f5cc4cf8eb386c99499430c368c26ec7d96d55f243f7fa66750(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__621829c976b7be5e41bb72a6f713420f0f400ffa31303d5ab2bcc76e151d2387(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c19f9ec722164297846ea39d1a48fe9504c9b45fd2f344ddf53591568ae849(
    value: typing.Optional[LoggingMetricBucketOptionsExponentialBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f312145c745b854a4671e66ec7f0919b32bb83c201c5522d7719b0b7cf1365b5(
    *,
    num_finite_buckets: jsii.Number,
    offset: jsii.Number,
    width: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d26f467faaface2875a6ebd367073b10e822ec8603cd215cd955e7a1e2c9594(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1f6709d3216f5ad768921f5b4ad5dcf0f0d92ed57d88d91f71ff77fe1291ea(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edc25012f89c42844cdfd7a99b4e47589670a6680109a672479c67f5b0954dab(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d49118bdb6c061c9d7ff25cbc0af98f2eff47efb80fadc1dceb6c208be5d951(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__034c45fe5cf17fbde26d194006ac8a2e8acd1a10cb314ebef09b95ce2f92f99d(
    value: typing.Optional[LoggingMetricBucketOptionsLinearBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fef223d100b05324035556adc47a590c5042f845171aa24a82d7535666eb734(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e704f1c1ef60b50bdf912f772d9dd424654998cd67fe4a4f2b22c1e44fd38fa(
    value: typing.Optional[LoggingMetricBucketOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a3107b5ebcf240927d9623e15f5e3d0704a5b2758904eea3ad1f67380f3046(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    filter: builtins.str,
    name: builtins.str,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_options: typing.Optional[typing.Union[LoggingMetricBucketOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    label_extractors: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metric_descriptor: typing.Optional[typing.Union[LoggingMetricMetricDescriptor, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[LoggingMetricTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    value_extractor: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a1661b616a5a922f86ea4ebafb09ccae20db1b27ae091a22ad387463999761(
    *,
    metric_kind: builtins.str,
    value_type: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoggingMetricMetricDescriptorLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04809fc8d569fa88e4a60ca0d1d2c82b8d23f910c29a3969ed44671a11e121bd(
    *,
    key: builtins.str,
    description: typing.Optional[builtins.str] = None,
    value_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3998a5703b692cde1cc3fae671d4d15599bfa2fbcdb66f2277aacab8ca0b781f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9486146495c033d1be4e8d522d7680c1864455bd94c3ee2aaa82729b2be8610(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f4c700eadc3374c5abda490773a6482d44cc82587b93b1feb94360df49ccfe5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c5bf8fcc5607647272ece83b1ad8424238f59d715eb421fa93a5df41a1d21fd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68a05146f93c297266613ad4c6347b263031866248c96826d555c24d74b5de89(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebcd75660e9dc45994c4e0e049b11e6d3b0212d8272b13cc138723744329a4ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoggingMetricMetricDescriptorLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2b2d6a74b78be08b415200baab0257f90aa75332996ca5fc4810a5eaef5ef91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e90c0c8e3878692a2e14a7a1ff64e0818583bf38bbcc1fc5d10b4d3e668a2ab9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5092c1b0c694b484bd60413992e5aea0499edaabb9b4d9d15f33e108859945b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b16cde0bcbc7fdd154911e1a906ccadefb681f5683d013fcc46c1307aba3dece(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad0d793f4082bc7f2135ba6a3c2ce17284309eddaddfd7b04876a73c842f282(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LoggingMetricMetricDescriptorLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a828676d04c28e3256369d9413c2a9d182c0e60fcefb6045f3df87a952a3bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f50d555f12f6bd57dd7f0c96f2caede6b73f37fb5ac3b4a8ebc937c4dc0c49b3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoggingMetricMetricDescriptorLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff207b5fe2b26c348af6424388d1e7eeeed1d5ecec27f990131cf5381904026(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__660e35881fa83f15bed63e47ec315e6d9ad5956076355f1a9cc2c184256d9e10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00f6839162e7b0e1dee9abd605909fca1d493e59d09bcaabf980dbe165452381(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43636ceb245a25e73c36b7c85c4e22b86540421f2b7a17ae7392c2a414b43eca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3c9d27afc1dfe8bd88cf6f03bb9b548d8ebb406109c48745b87984a64d65746(
    value: typing.Optional[LoggingMetricMetricDescriptor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99647e048a05e2c981557d02572c74fadfbb4106c7ffd8b3ca269ec8c4e34c1e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd1354096eb45e04f2f1ac791d91354c08f8f03d53b6de0f53c824eba254e2b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a3c97b6aa25ef1fb812149c71c2d2c194a346b6edc4997baa12ff89ddea044d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__238427bf973bc6adcc7cfd1f6c05bf78cf5a4e2ee9c5b3e9f539e76e77ca9fe2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6ca8b3b933fa71f81e03a9fe5c02ff12a0ec87f488019ebd7b6fcd27633b292(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__057a05970b2af9043afd993216fc587feb91b8a2978d4fd1f53724ce1a43723a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LoggingMetricTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
