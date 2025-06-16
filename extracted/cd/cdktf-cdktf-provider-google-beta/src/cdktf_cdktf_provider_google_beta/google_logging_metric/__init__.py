r'''
# `google_logging_metric`

Refer to the Terraform Registry for docs: [`google_logging_metric`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric).
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


class GoogleLoggingMetric(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLoggingMetric.GoogleLoggingMetric",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric google_logging_metric}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        filter: builtins.str,
        name: builtins.str,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_options: typing.Optional[typing.Union["GoogleLoggingMetricBucketOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        label_extractors: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metric_descriptor: typing.Optional[typing.Union["GoogleLoggingMetricMetricDescriptor", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleLoggingMetricTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        value_extractor: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric google_logging_metric} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param filter: An advanced logs filter (https://cloud.google.com/logging/docs/view/advanced-filters) which is used to match log entries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#filter GoogleLoggingMetric#filter}
        :param name: The client-assigned metric identifier. Examples - "error_count", "nginx/requests". Metric identifiers are limited to 100 characters and can include only the following characters A-Z, a-z, 0-9, and the special characters _-.,+!*',()%/. The forward-slash character (/) denotes a hierarchy of name pieces, and it cannot be the first character of the name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#name GoogleLoggingMetric#name}
        :param bucket_name: The resource name of the Log Bucket that owns the Log Metric. Only Log Buckets in projects are supported. The bucket has to be in the same project as the metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#bucket_name GoogleLoggingMetric#bucket_name}
        :param bucket_options: bucket_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#bucket_options GoogleLoggingMetric#bucket_options}
        :param description: A description of this metric, which is used in documentation. The maximum length of the description is 8000 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#description GoogleLoggingMetric#description}
        :param disabled: If set to True, then this metric is disabled and it does not generate any points. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#disabled GoogleLoggingMetric#disabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#id GoogleLoggingMetric#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param label_extractors: A map from a label key string to an extractor expression which is used to extract data from a log entry field and assign as the label value. Each label key specified in the LabelDescriptor must have an associated extractor expression in this map. The syntax of the extractor expression is the same as for the valueExtractor field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#label_extractors GoogleLoggingMetric#label_extractors}
        :param metric_descriptor: metric_descriptor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#metric_descriptor GoogleLoggingMetric#metric_descriptor}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#project GoogleLoggingMetric#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#timeouts GoogleLoggingMetric#timeouts}
        :param value_extractor: A valueExtractor is required when using a distribution logs-based metric to extract the values to record from a log entry. Two functions are supported for value extraction - EXTRACT(field) or REGEXP_EXTRACT(field, regex). The argument are 1. field - The name of the log entry field from which the value is to be extracted. 2. regex - A regular expression using the Google RE2 syntax (https://github.com/google/re2/wiki/Syntax) with a single capture group to extract data from the specified log entry field. The value of the field is converted to a string before applying the regex. It is an error to specify a regex that does not include exactly one capture group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#value_extractor GoogleLoggingMetric#value_extractor}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b617281b19ad099059068fbe9cfff49fbd90a58e59f27fc69016d0f594f18c8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleLoggingMetricConfig(
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
        '''Generates CDKTF code for importing a GoogleLoggingMetric resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleLoggingMetric to import.
        :param import_from_id: The id of the existing GoogleLoggingMetric that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleLoggingMetric to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d919d604f362b396a57d514066093b197e48917fa79dfc15459c9c73bdcbf6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBucketOptions")
    def put_bucket_options(
        self,
        *,
        explicit_buckets: typing.Optional[typing.Union["GoogleLoggingMetricBucketOptionsExplicitBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        exponential_buckets: typing.Optional[typing.Union["GoogleLoggingMetricBucketOptionsExponentialBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        linear_buckets: typing.Optional[typing.Union["GoogleLoggingMetricBucketOptionsLinearBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param explicit_buckets: explicit_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#explicit_buckets GoogleLoggingMetric#explicit_buckets}
        :param exponential_buckets: exponential_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#exponential_buckets GoogleLoggingMetric#exponential_buckets}
        :param linear_buckets: linear_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#linear_buckets GoogleLoggingMetric#linear_buckets}
        '''
        value = GoogleLoggingMetricBucketOptions(
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
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleLoggingMetricMetricDescriptorLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metric_kind: Whether the metric records instantaneous values, changes to a value, etc. Some combinations of metricKind and valueType might not be supported. For counter metrics, set this to DELTA. Possible values: ["DELTA", "GAUGE", "CUMULATIVE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#metric_kind GoogleLoggingMetric#metric_kind}
        :param value_type: Whether the measurement is an integer, a floating-point number, etc. Some combinations of metricKind and valueType might not be supported. For counter metrics, set this to INT64. Possible values: ["BOOL", "INT64", "DOUBLE", "STRING", "DISTRIBUTION", "MONEY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#value_type GoogleLoggingMetric#value_type}
        :param display_name: A concise name for the metric, which can be displayed in user interfaces. Use sentence case without an ending period, for example "Request count". This field is optional but it is recommended to be set for any metrics associated with user-visible concepts, such as Quota. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#display_name GoogleLoggingMetric#display_name}
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#labels GoogleLoggingMetric#labels}
        :param unit: The unit in which the metric value is reported. It is only applicable if the valueType is 'INT64', 'DOUBLE', or 'DISTRIBUTION'. The supported units are a subset of `The Unified Code for Units of Measure <http://unitsofmeasure.org/ucum.html>`_ standard Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#unit GoogleLoggingMetric#unit}
        '''
        value = GoogleLoggingMetricMetricDescriptor(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#create GoogleLoggingMetric#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#delete GoogleLoggingMetric#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#update GoogleLoggingMetric#update}.
        '''
        value = GoogleLoggingMetricTimeouts(
            create=create, delete=delete, update=update
        )

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
    def bucket_options(self) -> "GoogleLoggingMetricBucketOptionsOutputReference":
        return typing.cast("GoogleLoggingMetricBucketOptionsOutputReference", jsii.get(self, "bucketOptions"))

    @builtins.property
    @jsii.member(jsii_name="metricDescriptor")
    def metric_descriptor(self) -> "GoogleLoggingMetricMetricDescriptorOutputReference":
        return typing.cast("GoogleLoggingMetricMetricDescriptorOutputReference", jsii.get(self, "metricDescriptor"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleLoggingMetricTimeoutsOutputReference":
        return typing.cast("GoogleLoggingMetricTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketOptionsInput")
    def bucket_options_input(
        self,
    ) -> typing.Optional["GoogleLoggingMetricBucketOptions"]:
        return typing.cast(typing.Optional["GoogleLoggingMetricBucketOptions"], jsii.get(self, "bucketOptionsInput"))

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
    ) -> typing.Optional["GoogleLoggingMetricMetricDescriptor"]:
        return typing.cast(typing.Optional["GoogleLoggingMetricMetricDescriptor"], jsii.get(self, "metricDescriptorInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleLoggingMetricTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleLoggingMetricTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ca2fbfd0fe9f9c5eb49a92604f483e9062495fbc4673a6836bf372e4c7258557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3c77e296fef1da7f3ccd2ce8c4d7ada0538a3afec168315c15f8c9604a14f80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3ca7ab4c6a411734d2066eb05849f57078ad38c922571d26ccc66ba882aae27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d054f1e48386d6023a238f553a9bde349aa3db1d23360fb79adeb312ed84719)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2df4ed2869c839969d226d0e6646bd77931ff79625f78a3867842bd3eb99a8db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__844c60cf351cef2c3c926481494d2406449d4d3d3bb2829c3a518065263cf3ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labelExtractors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed4a0775f57fbed340927ea23b4bc2886cc372a75ad0302a405b9a18835f36e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__928bda63ce3890674b4df77c89ec22663794fdcc63b3925c3449a53e75d67735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valueExtractor")
    def value_extractor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueExtractor"))

    @value_extractor.setter
    def value_extractor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d3a2c456add4213d24aa8068d6142b9f2eaaec0b54612aa25e29419b4dc31bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueExtractor", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLoggingMetric.GoogleLoggingMetricBucketOptions",
    jsii_struct_bases=[],
    name_mapping={
        "explicit_buckets": "explicitBuckets",
        "exponential_buckets": "exponentialBuckets",
        "linear_buckets": "linearBuckets",
    },
)
class GoogleLoggingMetricBucketOptions:
    def __init__(
        self,
        *,
        explicit_buckets: typing.Optional[typing.Union["GoogleLoggingMetricBucketOptionsExplicitBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        exponential_buckets: typing.Optional[typing.Union["GoogleLoggingMetricBucketOptionsExponentialBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        linear_buckets: typing.Optional[typing.Union["GoogleLoggingMetricBucketOptionsLinearBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param explicit_buckets: explicit_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#explicit_buckets GoogleLoggingMetric#explicit_buckets}
        :param exponential_buckets: exponential_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#exponential_buckets GoogleLoggingMetric#exponential_buckets}
        :param linear_buckets: linear_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#linear_buckets GoogleLoggingMetric#linear_buckets}
        '''
        if isinstance(explicit_buckets, dict):
            explicit_buckets = GoogleLoggingMetricBucketOptionsExplicitBuckets(**explicit_buckets)
        if isinstance(exponential_buckets, dict):
            exponential_buckets = GoogleLoggingMetricBucketOptionsExponentialBuckets(**exponential_buckets)
        if isinstance(linear_buckets, dict):
            linear_buckets = GoogleLoggingMetricBucketOptionsLinearBuckets(**linear_buckets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d0372ccceb81265d00b332c73dc0c978e23ead4030495656b6bd5c5b0f78e24)
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
    ) -> typing.Optional["GoogleLoggingMetricBucketOptionsExplicitBuckets"]:
        '''explicit_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#explicit_buckets GoogleLoggingMetric#explicit_buckets}
        '''
        result = self._values.get("explicit_buckets")
        return typing.cast(typing.Optional["GoogleLoggingMetricBucketOptionsExplicitBuckets"], result)

    @builtins.property
    def exponential_buckets(
        self,
    ) -> typing.Optional["GoogleLoggingMetricBucketOptionsExponentialBuckets"]:
        '''exponential_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#exponential_buckets GoogleLoggingMetric#exponential_buckets}
        '''
        result = self._values.get("exponential_buckets")
        return typing.cast(typing.Optional["GoogleLoggingMetricBucketOptionsExponentialBuckets"], result)

    @builtins.property
    def linear_buckets(
        self,
    ) -> typing.Optional["GoogleLoggingMetricBucketOptionsLinearBuckets"]:
        '''linear_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#linear_buckets GoogleLoggingMetric#linear_buckets}
        '''
        result = self._values.get("linear_buckets")
        return typing.cast(typing.Optional["GoogleLoggingMetricBucketOptionsLinearBuckets"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLoggingMetricBucketOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLoggingMetric.GoogleLoggingMetricBucketOptionsExplicitBuckets",
    jsii_struct_bases=[],
    name_mapping={"bounds": "bounds"},
)
class GoogleLoggingMetricBucketOptionsExplicitBuckets:
    def __init__(self, *, bounds: typing.Sequence[jsii.Number]) -> None:
        '''
        :param bounds: The values must be monotonically increasing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#bounds GoogleLoggingMetric#bounds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be0f55aece3eae396de86bc1e9928ebf7eb2091638aeb3fdcb431f0c0c9de291)
            check_type(argname="argument bounds", value=bounds, expected_type=type_hints["bounds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bounds": bounds,
        }

    @builtins.property
    def bounds(self) -> typing.List[jsii.Number]:
        '''The values must be monotonically increasing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#bounds GoogleLoggingMetric#bounds}
        '''
        result = self._values.get("bounds")
        assert result is not None, "Required property 'bounds' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLoggingMetricBucketOptionsExplicitBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleLoggingMetricBucketOptionsExplicitBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLoggingMetric.GoogleLoggingMetricBucketOptionsExplicitBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c0d8abff14490c877ae206dfd08ac9bf4cc5cfb7347d69502883890a9307ead)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d45461b7d46926393f1965bbbc3c527e83e5f5413c494ff298cd9f8c56f20906)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bounds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleLoggingMetricBucketOptionsExplicitBuckets]:
        return typing.cast(typing.Optional[GoogleLoggingMetricBucketOptionsExplicitBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleLoggingMetricBucketOptionsExplicitBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a995cdb6bf7523f253420905d877641818b90e6d33693376f68ce7aaea723064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLoggingMetric.GoogleLoggingMetricBucketOptionsExponentialBuckets",
    jsii_struct_bases=[],
    name_mapping={
        "growth_factor": "growthFactor",
        "num_finite_buckets": "numFiniteBuckets",
        "scale": "scale",
    },
)
class GoogleLoggingMetricBucketOptionsExponentialBuckets:
    def __init__(
        self,
        *,
        growth_factor: jsii.Number,
        num_finite_buckets: jsii.Number,
        scale: jsii.Number,
    ) -> None:
        '''
        :param growth_factor: Must be greater than 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#growth_factor GoogleLoggingMetric#growth_factor}
        :param num_finite_buckets: Must be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#num_finite_buckets GoogleLoggingMetric#num_finite_buckets}
        :param scale: Must be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#scale GoogleLoggingMetric#scale}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57415f5793cfd7c36db423fe2cf84409ad1c2ba69d252dc645c29f1fd31774fa)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#growth_factor GoogleLoggingMetric#growth_factor}
        '''
        result = self._values.get("growth_factor")
        assert result is not None, "Required property 'growth_factor' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def num_finite_buckets(self) -> jsii.Number:
        '''Must be greater than 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#num_finite_buckets GoogleLoggingMetric#num_finite_buckets}
        '''
        result = self._values.get("num_finite_buckets")
        assert result is not None, "Required property 'num_finite_buckets' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale(self) -> jsii.Number:
        '''Must be greater than 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#scale GoogleLoggingMetric#scale}
        '''
        result = self._values.get("scale")
        assert result is not None, "Required property 'scale' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLoggingMetricBucketOptionsExponentialBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleLoggingMetricBucketOptionsExponentialBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLoggingMetric.GoogleLoggingMetricBucketOptionsExponentialBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26703202e3259cdae0fc5f28176e3a1647201d1235a4001ffaa745637333a3e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3468fe3d27e864f1617becfc43f36224612bc7ba1305411deec036aa670c929)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "growthFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numFiniteBuckets")
    def num_finite_buckets(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numFiniteBuckets"))

    @num_finite_buckets.setter
    def num_finite_buckets(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a78106f6ed483130d0bcc42218eae6a045bd7bc1ffa5b793c974009d15d3465)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numFiniteBuckets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scale")
    def scale(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scale"))

    @scale.setter
    def scale(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f1d6aa32f03952ea6b8965bcfcfd4169d08af9db30240ba957434cd4728accd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scale", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleLoggingMetricBucketOptionsExponentialBuckets]:
        return typing.cast(typing.Optional[GoogleLoggingMetricBucketOptionsExponentialBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleLoggingMetricBucketOptionsExponentialBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d1ead8a25db5b1380810b5664fdc8b3f99a24a1bcced494bd6de69f81cb2570)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLoggingMetric.GoogleLoggingMetricBucketOptionsLinearBuckets",
    jsii_struct_bases=[],
    name_mapping={
        "num_finite_buckets": "numFiniteBuckets",
        "offset": "offset",
        "width": "width",
    },
)
class GoogleLoggingMetricBucketOptionsLinearBuckets:
    def __init__(
        self,
        *,
        num_finite_buckets: jsii.Number,
        offset: jsii.Number,
        width: jsii.Number,
    ) -> None:
        '''
        :param num_finite_buckets: Must be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#num_finite_buckets GoogleLoggingMetric#num_finite_buckets}
        :param offset: Lower bound of the first bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#offset GoogleLoggingMetric#offset}
        :param width: Must be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#width GoogleLoggingMetric#width}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14db14d1b11a465229ccd9aad6557d7437a13d551ac3a08cd1983a8885b51cbe)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#num_finite_buckets GoogleLoggingMetric#num_finite_buckets}
        '''
        result = self._values.get("num_finite_buckets")
        assert result is not None, "Required property 'num_finite_buckets' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def offset(self) -> jsii.Number:
        '''Lower bound of the first bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#offset GoogleLoggingMetric#offset}
        '''
        result = self._values.get("offset")
        assert result is not None, "Required property 'offset' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def width(self) -> jsii.Number:
        '''Must be greater than 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#width GoogleLoggingMetric#width}
        '''
        result = self._values.get("width")
        assert result is not None, "Required property 'width' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLoggingMetricBucketOptionsLinearBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleLoggingMetricBucketOptionsLinearBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLoggingMetric.GoogleLoggingMetricBucketOptionsLinearBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea2a942251bbdd4f13830647922f82d8c2541dd64c20f375cd980aa4920904cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0935f261f958323d1e5491100458d32c9136fdcca7fde383b8608a7d095170d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numFiniteBuckets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="offset")
    def offset(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "offset"))

    @offset.setter
    def offset(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8c9d9e9a27ca17c210867804777add6a8733c50715e3b6f9225317dc95b4faa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "width"))

    @width.setter
    def width(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cfc3467b73a5333911fab8d02a85168d276c9a9244581386a5c0af7ba72c269)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "width", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleLoggingMetricBucketOptionsLinearBuckets]:
        return typing.cast(typing.Optional[GoogleLoggingMetricBucketOptionsLinearBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleLoggingMetricBucketOptionsLinearBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ac6179c2d164d250d5f06910b31f09bbe304e62cdf4b6e0b783f83901577fb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleLoggingMetricBucketOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLoggingMetric.GoogleLoggingMetricBucketOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__518e06009e7d78a7c6158df0ccc9370ced1150e0c4408840b7110e4e4852f693)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExplicitBuckets")
    def put_explicit_buckets(self, *, bounds: typing.Sequence[jsii.Number]) -> None:
        '''
        :param bounds: The values must be monotonically increasing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#bounds GoogleLoggingMetric#bounds}
        '''
        value = GoogleLoggingMetricBucketOptionsExplicitBuckets(bounds=bounds)

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
        :param growth_factor: Must be greater than 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#growth_factor GoogleLoggingMetric#growth_factor}
        :param num_finite_buckets: Must be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#num_finite_buckets GoogleLoggingMetric#num_finite_buckets}
        :param scale: Must be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#scale GoogleLoggingMetric#scale}
        '''
        value = GoogleLoggingMetricBucketOptionsExponentialBuckets(
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
        :param num_finite_buckets: Must be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#num_finite_buckets GoogleLoggingMetric#num_finite_buckets}
        :param offset: Lower bound of the first bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#offset GoogleLoggingMetric#offset}
        :param width: Must be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#width GoogleLoggingMetric#width}
        '''
        value = GoogleLoggingMetricBucketOptionsLinearBuckets(
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
    ) -> GoogleLoggingMetricBucketOptionsExplicitBucketsOutputReference:
        return typing.cast(GoogleLoggingMetricBucketOptionsExplicitBucketsOutputReference, jsii.get(self, "explicitBuckets"))

    @builtins.property
    @jsii.member(jsii_name="exponentialBuckets")
    def exponential_buckets(
        self,
    ) -> GoogleLoggingMetricBucketOptionsExponentialBucketsOutputReference:
        return typing.cast(GoogleLoggingMetricBucketOptionsExponentialBucketsOutputReference, jsii.get(self, "exponentialBuckets"))

    @builtins.property
    @jsii.member(jsii_name="linearBuckets")
    def linear_buckets(
        self,
    ) -> GoogleLoggingMetricBucketOptionsLinearBucketsOutputReference:
        return typing.cast(GoogleLoggingMetricBucketOptionsLinearBucketsOutputReference, jsii.get(self, "linearBuckets"))

    @builtins.property
    @jsii.member(jsii_name="explicitBucketsInput")
    def explicit_buckets_input(
        self,
    ) -> typing.Optional[GoogleLoggingMetricBucketOptionsExplicitBuckets]:
        return typing.cast(typing.Optional[GoogleLoggingMetricBucketOptionsExplicitBuckets], jsii.get(self, "explicitBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="exponentialBucketsInput")
    def exponential_buckets_input(
        self,
    ) -> typing.Optional[GoogleLoggingMetricBucketOptionsExponentialBuckets]:
        return typing.cast(typing.Optional[GoogleLoggingMetricBucketOptionsExponentialBuckets], jsii.get(self, "exponentialBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="linearBucketsInput")
    def linear_buckets_input(
        self,
    ) -> typing.Optional[GoogleLoggingMetricBucketOptionsLinearBuckets]:
        return typing.cast(typing.Optional[GoogleLoggingMetricBucketOptionsLinearBuckets], jsii.get(self, "linearBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleLoggingMetricBucketOptions]:
        return typing.cast(typing.Optional[GoogleLoggingMetricBucketOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleLoggingMetricBucketOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba15160c488c50d299192ba8538aa3abdea90a57ca26803d08f8a88b1d35690c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLoggingMetric.GoogleLoggingMetricConfig",
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
class GoogleLoggingMetricConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bucket_options: typing.Optional[typing.Union[GoogleLoggingMetricBucketOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        label_extractors: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metric_descriptor: typing.Optional[typing.Union["GoogleLoggingMetricMetricDescriptor", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleLoggingMetricTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param filter: An advanced logs filter (https://cloud.google.com/logging/docs/view/advanced-filters) which is used to match log entries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#filter GoogleLoggingMetric#filter}
        :param name: The client-assigned metric identifier. Examples - "error_count", "nginx/requests". Metric identifiers are limited to 100 characters and can include only the following characters A-Z, a-z, 0-9, and the special characters _-.,+!*',()%/. The forward-slash character (/) denotes a hierarchy of name pieces, and it cannot be the first character of the name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#name GoogleLoggingMetric#name}
        :param bucket_name: The resource name of the Log Bucket that owns the Log Metric. Only Log Buckets in projects are supported. The bucket has to be in the same project as the metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#bucket_name GoogleLoggingMetric#bucket_name}
        :param bucket_options: bucket_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#bucket_options GoogleLoggingMetric#bucket_options}
        :param description: A description of this metric, which is used in documentation. The maximum length of the description is 8000 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#description GoogleLoggingMetric#description}
        :param disabled: If set to True, then this metric is disabled and it does not generate any points. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#disabled GoogleLoggingMetric#disabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#id GoogleLoggingMetric#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param label_extractors: A map from a label key string to an extractor expression which is used to extract data from a log entry field and assign as the label value. Each label key specified in the LabelDescriptor must have an associated extractor expression in this map. The syntax of the extractor expression is the same as for the valueExtractor field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#label_extractors GoogleLoggingMetric#label_extractors}
        :param metric_descriptor: metric_descriptor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#metric_descriptor GoogleLoggingMetric#metric_descriptor}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#project GoogleLoggingMetric#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#timeouts GoogleLoggingMetric#timeouts}
        :param value_extractor: A valueExtractor is required when using a distribution logs-based metric to extract the values to record from a log entry. Two functions are supported for value extraction - EXTRACT(field) or REGEXP_EXTRACT(field, regex). The argument are 1. field - The name of the log entry field from which the value is to be extracted. 2. regex - A regular expression using the Google RE2 syntax (https://github.com/google/re2/wiki/Syntax) with a single capture group to extract data from the specified log entry field. The value of the field is converted to a string before applying the regex. It is an error to specify a regex that does not include exactly one capture group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#value_extractor GoogleLoggingMetric#value_extractor}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bucket_options, dict):
            bucket_options = GoogleLoggingMetricBucketOptions(**bucket_options)
        if isinstance(metric_descriptor, dict):
            metric_descriptor = GoogleLoggingMetricMetricDescriptor(**metric_descriptor)
        if isinstance(timeouts, dict):
            timeouts = GoogleLoggingMetricTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f05dc066a13230cd661df3b8160e23a819c647af4afb0934b767c2ca29adbc9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#filter GoogleLoggingMetric#filter}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#name GoogleLoggingMetric#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''The resource name of the Log Bucket that owns the Log Metric.

        Only Log Buckets in projects
        are supported. The bucket has to be in the same project as the metric.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#bucket_name GoogleLoggingMetric#bucket_name}
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_options(self) -> typing.Optional[GoogleLoggingMetricBucketOptions]:
        '''bucket_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#bucket_options GoogleLoggingMetric#bucket_options}
        '''
        result = self._values.get("bucket_options")
        return typing.cast(typing.Optional[GoogleLoggingMetricBucketOptions], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of this metric, which is used in documentation. The maximum length of the description is 8000 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#description GoogleLoggingMetric#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to True, then this metric is disabled and it does not generate any points.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#disabled GoogleLoggingMetric#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#id GoogleLoggingMetric#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#label_extractors GoogleLoggingMetric#label_extractors}
        '''
        result = self._values.get("label_extractors")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metric_descriptor(
        self,
    ) -> typing.Optional["GoogleLoggingMetricMetricDescriptor"]:
        '''metric_descriptor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#metric_descriptor GoogleLoggingMetric#metric_descriptor}
        '''
        result = self._values.get("metric_descriptor")
        return typing.cast(typing.Optional["GoogleLoggingMetricMetricDescriptor"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#project GoogleLoggingMetric#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleLoggingMetricTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#timeouts GoogleLoggingMetric#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleLoggingMetricTimeouts"], result)

    @builtins.property
    def value_extractor(self) -> typing.Optional[builtins.str]:
        '''A valueExtractor is required when using a distribution logs-based metric to extract the values to record from a log entry.

        Two functions are supported for value extraction - EXTRACT(field) or
        REGEXP_EXTRACT(field, regex). The argument are 1. field - The name of the log entry field from which
        the value is to be extracted. 2. regex - A regular expression using the Google RE2 syntax
        (https://github.com/google/re2/wiki/Syntax) with a single capture group to extract data from the specified
        log entry field. The value of the field is converted to a string before applying the regex. It is an
        error to specify a regex that does not include exactly one capture group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#value_extractor GoogleLoggingMetric#value_extractor}
        '''
        result = self._values.get("value_extractor")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLoggingMetricConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLoggingMetric.GoogleLoggingMetricMetricDescriptor",
    jsii_struct_bases=[],
    name_mapping={
        "metric_kind": "metricKind",
        "value_type": "valueType",
        "display_name": "displayName",
        "labels": "labels",
        "unit": "unit",
    },
)
class GoogleLoggingMetricMetricDescriptor:
    def __init__(
        self,
        *,
        metric_kind: builtins.str,
        value_type: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleLoggingMetricMetricDescriptorLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metric_kind: Whether the metric records instantaneous values, changes to a value, etc. Some combinations of metricKind and valueType might not be supported. For counter metrics, set this to DELTA. Possible values: ["DELTA", "GAUGE", "CUMULATIVE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#metric_kind GoogleLoggingMetric#metric_kind}
        :param value_type: Whether the measurement is an integer, a floating-point number, etc. Some combinations of metricKind and valueType might not be supported. For counter metrics, set this to INT64. Possible values: ["BOOL", "INT64", "DOUBLE", "STRING", "DISTRIBUTION", "MONEY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#value_type GoogleLoggingMetric#value_type}
        :param display_name: A concise name for the metric, which can be displayed in user interfaces. Use sentence case without an ending period, for example "Request count". This field is optional but it is recommended to be set for any metrics associated with user-visible concepts, such as Quota. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#display_name GoogleLoggingMetric#display_name}
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#labels GoogleLoggingMetric#labels}
        :param unit: The unit in which the metric value is reported. It is only applicable if the valueType is 'INT64', 'DOUBLE', or 'DISTRIBUTION'. The supported units are a subset of `The Unified Code for Units of Measure <http://unitsofmeasure.org/ucum.html>`_ standard Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#unit GoogleLoggingMetric#unit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1b04a33a21352caa718019784d8604c2cc150b81ad255f0ab6ef7fb967613c8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#metric_kind GoogleLoggingMetric#metric_kind}
        '''
        result = self._values.get("metric_kind")
        assert result is not None, "Required property 'metric_kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value_type(self) -> builtins.str:
        '''Whether the measurement is an integer, a floating-point number, etc.

        Some combinations of metricKind and valueType might not be supported.
        For counter metrics, set this to INT64. Possible values: ["BOOL", "INT64", "DOUBLE", "STRING", "DISTRIBUTION", "MONEY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#value_type GoogleLoggingMetric#value_type}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#display_name GoogleLoggingMetric#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleLoggingMetricMetricDescriptorLabels"]]]:
        '''labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#labels GoogleLoggingMetric#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleLoggingMetricMetricDescriptorLabels"]]], result)

    @builtins.property
    def unit(self) -> typing.Optional[builtins.str]:
        '''The unit in which the metric value is reported.

        It is only applicable if the valueType is
        'INT64', 'DOUBLE', or 'DISTRIBUTION'. The supported units are a subset of
        `The Unified Code for Units of Measure <http://unitsofmeasure.org/ucum.html>`_ standard

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#unit GoogleLoggingMetric#unit}
        '''
        result = self._values.get("unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLoggingMetricMetricDescriptor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLoggingMetric.GoogleLoggingMetricMetricDescriptorLabels",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "description": "description",
        "value_type": "valueType",
    },
)
class GoogleLoggingMetricMetricDescriptorLabels:
    def __init__(
        self,
        *,
        key: builtins.str,
        description: typing.Optional[builtins.str] = None,
        value_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: The label key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#key GoogleLoggingMetric#key}
        :param description: A human-readable description for the label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#description GoogleLoggingMetric#description}
        :param value_type: The type of data that can be assigned to the label. Default value: "STRING" Possible values: ["BOOL", "INT64", "STRING"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#value_type GoogleLoggingMetric#value_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e616b109322d2ae4ce9b94b216ed804a43491cbcd23d1866c05953dde9800cd6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#key GoogleLoggingMetric#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description for the label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#description GoogleLoggingMetric#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_type(self) -> typing.Optional[builtins.str]:
        '''The type of data that can be assigned to the label. Default value: "STRING" Possible values: ["BOOL", "INT64", "STRING"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#value_type GoogleLoggingMetric#value_type}
        '''
        result = self._values.get("value_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLoggingMetricMetricDescriptorLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleLoggingMetricMetricDescriptorLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLoggingMetric.GoogleLoggingMetricMetricDescriptorLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__382a4d58d6135c6a920b8d2db61e03cb308cb79d5ee949f8ac651bf39c0e2045)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleLoggingMetricMetricDescriptorLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc8fb247291b81c67d22d7e3e50cecd78a0b7dfcbda56271ba920a8f4b310113)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleLoggingMetricMetricDescriptorLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1318d98c96d6f90b5898c4f86d710437b970ad7eca5e67fd8bc5d8b78da4d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2b0c9658e2a668b8cfa3044daed8b6a7ec42ed44486d6745d8224a4f1cb2ab2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0ed010ced0b4a9bd82977abcd28c06a73615956dc2f22b737f772c3050e9129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleLoggingMetricMetricDescriptorLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleLoggingMetricMetricDescriptorLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleLoggingMetricMetricDescriptorLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9618ea9b81e8b2e7123a719df3478bdf010a99226b305b5df3247bf8b74c542)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleLoggingMetricMetricDescriptorLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLoggingMetric.GoogleLoggingMetricMetricDescriptorLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04a4959e75e83376b5e2ac550b233c8c38d0de75315b3dc33469a74bd8f364ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e345e4bc9fe281e22898908cb1f84bd682d69e39de97f5ff559324255af01dfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a897ab8598631638dbb6f3573339a393872d33d02ae31502663904b9fc40b901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valueType")
    def value_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueType"))

    @value_type.setter
    def value_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5efead72228a21b8d05f5cafe9414915d5ae5c9f43f16ddda003a81d60ebd215)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleLoggingMetricMetricDescriptorLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleLoggingMetricMetricDescriptorLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleLoggingMetricMetricDescriptorLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b07d220971bbf2fc0680fa3d8c0b1a27b9cb2746382f2922b59bdd4fc063ab1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleLoggingMetricMetricDescriptorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLoggingMetric.GoogleLoggingMetricMetricDescriptorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fdcd2dd50c74e2553eb7dd31a369d8c65dc9042c47eee6a58c1807b22fd2488)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLabels")
    def put_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleLoggingMetricMetricDescriptorLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9441e1b73ef96ce482d1dd9cf27f27d12b30911e68093e442bf5c7b94c9640c1)
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
    def labels(self) -> GoogleLoggingMetricMetricDescriptorLabelsList:
        return typing.cast(GoogleLoggingMetricMetricDescriptorLabelsList, jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleLoggingMetricMetricDescriptorLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleLoggingMetricMetricDescriptorLabels]]], jsii.get(self, "labelsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__52512c466ad80552bd443f01e2a0e2829c26a0e556c3201f6751b8ff6f71ae5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricKind")
    def metric_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricKind"))

    @metric_kind.setter
    def metric_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a636534269e480e98f2f0430130d66e23145484e595c4fb685ff7ceb49170a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unit"))

    @unit.setter
    def unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82658997d0001ff2f366ef17502f9d84bec2fefcd6457f03440189861fa7d344)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valueType")
    def value_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueType"))

    @value_type.setter
    def value_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39251af9753f34fe0901721e9712af610523a938fce0d55714297200b76ce066)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleLoggingMetricMetricDescriptor]:
        return typing.cast(typing.Optional[GoogleLoggingMetricMetricDescriptor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleLoggingMetricMetricDescriptor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3e7686d0afa4f0b08cbba351b22c136925b46641cf5dd5dd48b1b907acfd5c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLoggingMetric.GoogleLoggingMetricTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleLoggingMetricTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#create GoogleLoggingMetric#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#delete GoogleLoggingMetric#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#update GoogleLoggingMetric#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7593d220e64403aebdd7a8fd87f490d9d9d93de2419b72455c75c0ded78be4e6)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#create GoogleLoggingMetric#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#delete GoogleLoggingMetric#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_logging_metric#update GoogleLoggingMetric#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLoggingMetricTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleLoggingMetricTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLoggingMetric.GoogleLoggingMetricTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ccaf32891510f1f2e2e4a9e0e31a4793f8124478a8951d5b32f722bc316e055)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abf3349e133093d60d0de49f3c85a27d590bb4548c3c0d4d80e5346302a47ae6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d47767401c32a592d9357d6605991f36b88467b1a69078af79d7ce34f55654a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d300b42f0bf9ca8c778ce76210f2b22cb40fbbbc8af1f23d4bb08cc437c3a977)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleLoggingMetricTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleLoggingMetricTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleLoggingMetricTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__223f53fbef000d9f9d81305e263004c006bf167a5d2396888ea4ae224e452432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleLoggingMetric",
    "GoogleLoggingMetricBucketOptions",
    "GoogleLoggingMetricBucketOptionsExplicitBuckets",
    "GoogleLoggingMetricBucketOptionsExplicitBucketsOutputReference",
    "GoogleLoggingMetricBucketOptionsExponentialBuckets",
    "GoogleLoggingMetricBucketOptionsExponentialBucketsOutputReference",
    "GoogleLoggingMetricBucketOptionsLinearBuckets",
    "GoogleLoggingMetricBucketOptionsLinearBucketsOutputReference",
    "GoogleLoggingMetricBucketOptionsOutputReference",
    "GoogleLoggingMetricConfig",
    "GoogleLoggingMetricMetricDescriptor",
    "GoogleLoggingMetricMetricDescriptorLabels",
    "GoogleLoggingMetricMetricDescriptorLabelsList",
    "GoogleLoggingMetricMetricDescriptorLabelsOutputReference",
    "GoogleLoggingMetricMetricDescriptorOutputReference",
    "GoogleLoggingMetricTimeouts",
    "GoogleLoggingMetricTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0b617281b19ad099059068fbe9cfff49fbd90a58e59f27fc69016d0f594f18c8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    filter: builtins.str,
    name: builtins.str,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_options: typing.Optional[typing.Union[GoogleLoggingMetricBucketOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    label_extractors: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metric_descriptor: typing.Optional[typing.Union[GoogleLoggingMetricMetricDescriptor, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleLoggingMetricTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__96d919d604f362b396a57d514066093b197e48917fa79dfc15459c9c73bdcbf6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2fbfd0fe9f9c5eb49a92604f483e9062495fbc4673a6836bf372e4c7258557(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3c77e296fef1da7f3ccd2ce8c4d7ada0538a3afec168315c15f8c9604a14f80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3ca7ab4c6a411734d2066eb05849f57078ad38c922571d26ccc66ba882aae27(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d054f1e48386d6023a238f553a9bde349aa3db1d23360fb79adeb312ed84719(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2df4ed2869c839969d226d0e6646bd77931ff79625f78a3867842bd3eb99a8db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844c60cf351cef2c3c926481494d2406449d4d3d3bb2829c3a518065263cf3ca(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed4a0775f57fbed340927ea23b4bc2886cc372a75ad0302a405b9a18835f36e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__928bda63ce3890674b4df77c89ec22663794fdcc63b3925c3449a53e75d67735(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3a2c456add4213d24aa8068d6142b9f2eaaec0b54612aa25e29419b4dc31bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d0372ccceb81265d00b332c73dc0c978e23ead4030495656b6bd5c5b0f78e24(
    *,
    explicit_buckets: typing.Optional[typing.Union[GoogleLoggingMetricBucketOptionsExplicitBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    exponential_buckets: typing.Optional[typing.Union[GoogleLoggingMetricBucketOptionsExponentialBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    linear_buckets: typing.Optional[typing.Union[GoogleLoggingMetricBucketOptionsLinearBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be0f55aece3eae396de86bc1e9928ebf7eb2091638aeb3fdcb431f0c0c9de291(
    *,
    bounds: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c0d8abff14490c877ae206dfd08ac9bf4cc5cfb7347d69502883890a9307ead(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45461b7d46926393f1965bbbc3c527e83e5f5413c494ff298cd9f8c56f20906(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a995cdb6bf7523f253420905d877641818b90e6d33693376f68ce7aaea723064(
    value: typing.Optional[GoogleLoggingMetricBucketOptionsExplicitBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57415f5793cfd7c36db423fe2cf84409ad1c2ba69d252dc645c29f1fd31774fa(
    *,
    growth_factor: jsii.Number,
    num_finite_buckets: jsii.Number,
    scale: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26703202e3259cdae0fc5f28176e3a1647201d1235a4001ffaa745637333a3e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3468fe3d27e864f1617becfc43f36224612bc7ba1305411deec036aa670c929(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a78106f6ed483130d0bcc42218eae6a045bd7bc1ffa5b793c974009d15d3465(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f1d6aa32f03952ea6b8965bcfcfd4169d08af9db30240ba957434cd4728accd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d1ead8a25db5b1380810b5664fdc8b3f99a24a1bcced494bd6de69f81cb2570(
    value: typing.Optional[GoogleLoggingMetricBucketOptionsExponentialBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14db14d1b11a465229ccd9aad6557d7437a13d551ac3a08cd1983a8885b51cbe(
    *,
    num_finite_buckets: jsii.Number,
    offset: jsii.Number,
    width: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2a942251bbdd4f13830647922f82d8c2541dd64c20f375cd980aa4920904cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0935f261f958323d1e5491100458d32c9136fdcca7fde383b8608a7d095170d4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8c9d9e9a27ca17c210867804777add6a8733c50715e3b6f9225317dc95b4faa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cfc3467b73a5333911fab8d02a85168d276c9a9244581386a5c0af7ba72c269(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ac6179c2d164d250d5f06910b31f09bbe304e62cdf4b6e0b783f83901577fb2(
    value: typing.Optional[GoogleLoggingMetricBucketOptionsLinearBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__518e06009e7d78a7c6158df0ccc9370ced1150e0c4408840b7110e4e4852f693(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba15160c488c50d299192ba8538aa3abdea90a57ca26803d08f8a88b1d35690c(
    value: typing.Optional[GoogleLoggingMetricBucketOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f05dc066a13230cd661df3b8160e23a819c647af4afb0934b767c2ca29adbc9(
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
    bucket_options: typing.Optional[typing.Union[GoogleLoggingMetricBucketOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    label_extractors: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metric_descriptor: typing.Optional[typing.Union[GoogleLoggingMetricMetricDescriptor, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleLoggingMetricTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    value_extractor: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b04a33a21352caa718019784d8604c2cc150b81ad255f0ab6ef7fb967613c8(
    *,
    metric_kind: builtins.str,
    value_type: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleLoggingMetricMetricDescriptorLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e616b109322d2ae4ce9b94b216ed804a43491cbcd23d1866c05953dde9800cd6(
    *,
    key: builtins.str,
    description: typing.Optional[builtins.str] = None,
    value_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382a4d58d6135c6a920b8d2db61e03cb308cb79d5ee949f8ac651bf39c0e2045(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc8fb247291b81c67d22d7e3e50cecd78a0b7dfcbda56271ba920a8f4b310113(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1318d98c96d6f90b5898c4f86d710437b970ad7eca5e67fd8bc5d8b78da4d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b0c9658e2a668b8cfa3044daed8b6a7ec42ed44486d6745d8224a4f1cb2ab2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0ed010ced0b4a9bd82977abcd28c06a73615956dc2f22b737f772c3050e9129(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9618ea9b81e8b2e7123a719df3478bdf010a99226b305b5df3247bf8b74c542(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleLoggingMetricMetricDescriptorLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a4959e75e83376b5e2ac550b233c8c38d0de75315b3dc33469a74bd8f364ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e345e4bc9fe281e22898908cb1f84bd682d69e39de97f5ff559324255af01dfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a897ab8598631638dbb6f3573339a393872d33d02ae31502663904b9fc40b901(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5efead72228a21b8d05f5cafe9414915d5ae5c9f43f16ddda003a81d60ebd215(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b07d220971bbf2fc0680fa3d8c0b1a27b9cb2746382f2922b59bdd4fc063ab1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleLoggingMetricMetricDescriptorLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fdcd2dd50c74e2553eb7dd31a369d8c65dc9042c47eee6a58c1807b22fd2488(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9441e1b73ef96ce482d1dd9cf27f27d12b30911e68093e442bf5c7b94c9640c1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleLoggingMetricMetricDescriptorLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52512c466ad80552bd443f01e2a0e2829c26a0e556c3201f6751b8ff6f71ae5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a636534269e480e98f2f0430130d66e23145484e595c4fb685ff7ceb49170a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82658997d0001ff2f366ef17502f9d84bec2fefcd6457f03440189861fa7d344(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39251af9753f34fe0901721e9712af610523a938fce0d55714297200b76ce066(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e7686d0afa4f0b08cbba351b22c136925b46641cf5dd5dd48b1b907acfd5c2(
    value: typing.Optional[GoogleLoggingMetricMetricDescriptor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7593d220e64403aebdd7a8fd87f490d9d9d93de2419b72455c75c0ded78be4e6(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ccaf32891510f1f2e2e4a9e0e31a4793f8124478a8951d5b32f722bc316e055(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf3349e133093d60d0de49f3c85a27d590bb4548c3c0d4d80e5346302a47ae6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47767401c32a592d9357d6605991f36b88467b1a69078af79d7ce34f55654a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d300b42f0bf9ca8c778ce76210f2b22cb40fbbbc8af1f23d4bb08cc437c3a977(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__223f53fbef000d9f9d81305e263004c006bf167a5d2396888ea4ae224e452432(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleLoggingMetricTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
