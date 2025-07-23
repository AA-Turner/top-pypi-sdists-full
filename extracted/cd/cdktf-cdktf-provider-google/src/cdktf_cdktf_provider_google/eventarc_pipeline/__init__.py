r'''
# `google_eventarc_pipeline`

Refer to the Terraform Registry for docs: [`google_eventarc_pipeline`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline).
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


class EventarcPipeline(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipeline",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline google_eventarc_pipeline}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        destinations: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventarcPipelineDestinations", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        pipeline_id: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        crypto_key_name: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        input_payload_format: typing.Optional[typing.Union["EventarcPipelineInputPayloadFormat", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["EventarcPipelineLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mediations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventarcPipelineMediations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        retry_policy: typing.Optional[typing.Union["EventarcPipelineRetryPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["EventarcPipelineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline google_eventarc_pipeline} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param destinations: destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#destinations EventarcPipeline#destinations}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#location EventarcPipeline#location}
        :param pipeline_id: The user-provided ID to be assigned to the Pipeline. It should match the format '^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#pipeline_id EventarcPipeline#pipeline_id}
        :param annotations: User-defined annotations. See https://google.aip.dev/128#annotations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#annotations EventarcPipeline#annotations}
        :param crypto_key_name: Resource name of a KMS crypto key (managed by the user) used to encrypt/decrypt the event data. If not set, an internal Google-owned key will be used to encrypt messages. It must match the pattern "projects/{project}/locations/{location}/keyRings/{keyring}/cryptoKeys/{key}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#crypto_key_name EventarcPipeline#crypto_key_name}
        :param display_name: Display name of resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#display_name EventarcPipeline#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#id EventarcPipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param input_payload_format: input_payload_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#input_payload_format EventarcPipeline#input_payload_format}
        :param labels: User labels attached to the Pipeline that can be used to group resources. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#labels EventarcPipeline#labels}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#logging_config EventarcPipeline#logging_config}
        :param mediations: mediations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#mediations EventarcPipeline#mediations}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#project EventarcPipeline#project}.
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#retry_policy EventarcPipeline#retry_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#timeouts EventarcPipeline#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8d06537300aa362197ab5d3cc425367cfe70a11e594ee4df8ba892e8713a370)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EventarcPipelineConfig(
            destinations=destinations,
            location=location,
            pipeline_id=pipeline_id,
            annotations=annotations,
            crypto_key_name=crypto_key_name,
            display_name=display_name,
            id=id,
            input_payload_format=input_payload_format,
            labels=labels,
            logging_config=logging_config,
            mediations=mediations,
            project=project,
            retry_policy=retry_policy,
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
        '''Generates CDKTF code for importing a EventarcPipeline resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EventarcPipeline to import.
        :param import_from_id: The id of the existing EventarcPipeline that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EventarcPipeline to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbb162719dfdba07c7aeef4367676d169a059dcd07ae800dd86524277f0af42c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDestinations")
    def put_destinations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventarcPipelineDestinations", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a7ebf84798a1e7ab731eb9db751a8eb755abce70fe0994dcf49591def51185)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDestinations", [value]))

    @jsii.member(jsii_name="putInputPayloadFormat")
    def put_input_payload_format(
        self,
        *,
        avro: typing.Optional[typing.Union["EventarcPipelineInputPayloadFormatAvro", typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union["EventarcPipelineInputPayloadFormatJson", typing.Dict[builtins.str, typing.Any]]] = None,
        protobuf: typing.Optional[typing.Union["EventarcPipelineInputPayloadFormatProtobuf", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param avro: avro block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#avro EventarcPipeline#avro}
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#json EventarcPipeline#json}
        :param protobuf: protobuf block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#protobuf EventarcPipeline#protobuf}
        '''
        value = EventarcPipelineInputPayloadFormat(
            avro=avro, json=json, protobuf=protobuf
        )

        return typing.cast(None, jsii.invoke(self, "putInputPayloadFormat", [value]))

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        log_severity: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_severity: The minimum severity of logs that will be sent to Stackdriver/Platform Telemetry. Logs at severitiy ≥ this value will be sent, unless it is NONE. Possible values: ["NONE", "DEBUG", "INFO", "NOTICE", "WARNING", "ERROR", "CRITICAL", "ALERT", "EMERGENCY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#log_severity EventarcPipeline#log_severity}
        '''
        value = EventarcPipelineLoggingConfig(log_severity=log_severity)

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

    @jsii.member(jsii_name="putMediations")
    def put_mediations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventarcPipelineMediations", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d63adef02e613b78acd35229e5bccbe5efec63f96759507ff4f2b8e367b8e71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMediations", [value]))

    @jsii.member(jsii_name="putRetryPolicy")
    def put_retry_policy(
        self,
        *,
        max_attempts: typing.Optional[jsii.Number] = None,
        max_retry_delay: typing.Optional[builtins.str] = None,
        min_retry_delay: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_attempts: The maximum number of delivery attempts for any message. The value must be between 1 and 100. The default value for this field is 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#max_attempts EventarcPipeline#max_attempts}
        :param max_retry_delay: The maximum amount of seconds to wait between retry attempts. The value must be between 1 and 600. The default value for this field is 60. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#max_retry_delay EventarcPipeline#max_retry_delay}
        :param min_retry_delay: The minimum amount of seconds to wait between retry attempts. The value must be between 1 and 600. The default value for this field is 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#min_retry_delay EventarcPipeline#min_retry_delay}
        '''
        value = EventarcPipelineRetryPolicy(
            max_attempts=max_attempts,
            max_retry_delay=max_retry_delay,
            min_retry_delay=min_retry_delay,
        )

        return typing.cast(None, jsii.invoke(self, "putRetryPolicy", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#create EventarcPipeline#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#delete EventarcPipeline#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#update EventarcPipeline#update}.
        '''
        value = EventarcPipelineTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetCryptoKeyName")
    def reset_crypto_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCryptoKeyName", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInputPayloadFormat")
    def reset_input_payload_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputPayloadFormat", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

    @jsii.member(jsii_name="resetMediations")
    def reset_mediations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMediations", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRetryPolicy")
    def reset_retry_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryPolicy", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="destinations")
    def destinations(self) -> "EventarcPipelineDestinationsList":
        return typing.cast("EventarcPipelineDestinationsList", jsii.get(self, "destinations"))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="inputPayloadFormat")
    def input_payload_format(
        self,
    ) -> "EventarcPipelineInputPayloadFormatOutputReference":
        return typing.cast("EventarcPipelineInputPayloadFormatOutputReference", jsii.get(self, "inputPayloadFormat"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(self) -> "EventarcPipelineLoggingConfigOutputReference":
        return typing.cast("EventarcPipelineLoggingConfigOutputReference", jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="mediations")
    def mediations(self) -> "EventarcPipelineMediationsList":
        return typing.cast("EventarcPipelineMediationsList", jsii.get(self, "mediations"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicy")
    def retry_policy(self) -> "EventarcPipelineRetryPolicyOutputReference":
        return typing.cast("EventarcPipelineRetryPolicyOutputReference", jsii.get(self, "retryPolicy"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "EventarcPipelineTimeoutsOutputReference":
        return typing.cast("EventarcPipelineTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="cryptoKeyNameInput")
    def crypto_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cryptoKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationsInput")
    def destinations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventarcPipelineDestinations"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventarcPipelineDestinations"]]], jsii.get(self, "destinationsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inputPayloadFormatInput")
    def input_payload_format_input(
        self,
    ) -> typing.Optional["EventarcPipelineInputPayloadFormat"]:
        return typing.cast(typing.Optional["EventarcPipelineInputPayloadFormat"], jsii.get(self, "inputPayloadFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(self) -> typing.Optional["EventarcPipelineLoggingConfig"]:
        return typing.cast(typing.Optional["EventarcPipelineLoggingConfig"], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="mediationsInput")
    def mediations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventarcPipelineMediations"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventarcPipelineMediations"]]], jsii.get(self, "mediationsInput"))

    @builtins.property
    @jsii.member(jsii_name="pipelineIdInput")
    def pipeline_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pipelineIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicyInput")
    def retry_policy_input(self) -> typing.Optional["EventarcPipelineRetryPolicy"]:
        return typing.cast(typing.Optional["EventarcPipelineRetryPolicy"], jsii.get(self, "retryPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EventarcPipelineTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EventarcPipelineTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a4abd9a434c50435762a4446d254b4828ca9fc68d9a393f9f467ccad08a447a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cryptoKeyName")
    def crypto_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cryptoKeyName"))

    @crypto_key_name.setter
    def crypto_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f38ef5e851ff6da02386c2ee21b51d0a2f3c4e383b99e63b50682fc754efea02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cryptoKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c33cae7b59e6996b8823ae9dde39ebbea64995de98ae7a130fcf76f21d14809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d05fa5001b5a716a63c5e2c5229cb16d15a1d621dabac722d8690bcb5fabab1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__746d59b6137fbeae2556307b47edd75cb021462dc1d08fbb012bd1fa61a3c30f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a393d8ffc64dcd11cd30d5d7c5ac4fc07325243523033b0886a1a838361376b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pipelineId")
    def pipeline_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pipelineId"))

    @pipeline_id.setter
    def pipeline_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f6b4c93ab45794c6794b7cccd8870b34c374377a04630a938704ce87aef8edf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pipelineId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb718f6977ff6af6d57a8a0390f151b1bc179c1c87cd7397abdf8fda089bf8f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "destinations": "destinations",
        "location": "location",
        "pipeline_id": "pipelineId",
        "annotations": "annotations",
        "crypto_key_name": "cryptoKeyName",
        "display_name": "displayName",
        "id": "id",
        "input_payload_format": "inputPayloadFormat",
        "labels": "labels",
        "logging_config": "loggingConfig",
        "mediations": "mediations",
        "project": "project",
        "retry_policy": "retryPolicy",
        "timeouts": "timeouts",
    },
)
class EventarcPipelineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        destinations: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventarcPipelineDestinations", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        pipeline_id: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        crypto_key_name: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        input_payload_format: typing.Optional[typing.Union["EventarcPipelineInputPayloadFormat", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["EventarcPipelineLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mediations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventarcPipelineMediations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        retry_policy: typing.Optional[typing.Union["EventarcPipelineRetryPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["EventarcPipelineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param destinations: destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#destinations EventarcPipeline#destinations}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#location EventarcPipeline#location}
        :param pipeline_id: The user-provided ID to be assigned to the Pipeline. It should match the format '^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#pipeline_id EventarcPipeline#pipeline_id}
        :param annotations: User-defined annotations. See https://google.aip.dev/128#annotations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#annotations EventarcPipeline#annotations}
        :param crypto_key_name: Resource name of a KMS crypto key (managed by the user) used to encrypt/decrypt the event data. If not set, an internal Google-owned key will be used to encrypt messages. It must match the pattern "projects/{project}/locations/{location}/keyRings/{keyring}/cryptoKeys/{key}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#crypto_key_name EventarcPipeline#crypto_key_name}
        :param display_name: Display name of resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#display_name EventarcPipeline#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#id EventarcPipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param input_payload_format: input_payload_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#input_payload_format EventarcPipeline#input_payload_format}
        :param labels: User labels attached to the Pipeline that can be used to group resources. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#labels EventarcPipeline#labels}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#logging_config EventarcPipeline#logging_config}
        :param mediations: mediations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#mediations EventarcPipeline#mediations}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#project EventarcPipeline#project}.
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#retry_policy EventarcPipeline#retry_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#timeouts EventarcPipeline#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(input_payload_format, dict):
            input_payload_format = EventarcPipelineInputPayloadFormat(**input_payload_format)
        if isinstance(logging_config, dict):
            logging_config = EventarcPipelineLoggingConfig(**logging_config)
        if isinstance(retry_policy, dict):
            retry_policy = EventarcPipelineRetryPolicy(**retry_policy)
        if isinstance(timeouts, dict):
            timeouts = EventarcPipelineTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f2e5aee555a4ebd7b479b830650d537b80814e357987af80370d42bd63b70d6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument pipeline_id", value=pipeline_id, expected_type=type_hints["pipeline_id"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument crypto_key_name", value=crypto_key_name, expected_type=type_hints["crypto_key_name"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument input_payload_format", value=input_payload_format, expected_type=type_hints["input_payload_format"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument mediations", value=mediations, expected_type=type_hints["mediations"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument retry_policy", value=retry_policy, expected_type=type_hints["retry_policy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destinations": destinations,
            "location": location,
            "pipeline_id": pipeline_id,
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
        if annotations is not None:
            self._values["annotations"] = annotations
        if crypto_key_name is not None:
            self._values["crypto_key_name"] = crypto_key_name
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if input_payload_format is not None:
            self._values["input_payload_format"] = input_payload_format
        if labels is not None:
            self._values["labels"] = labels
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if mediations is not None:
            self._values["mediations"] = mediations
        if project is not None:
            self._values["project"] = project
        if retry_policy is not None:
            self._values["retry_policy"] = retry_policy
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
    def destinations(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventarcPipelineDestinations"]]:
        '''destinations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#destinations EventarcPipeline#destinations}
        '''
        result = self._values.get("destinations")
        assert result is not None, "Required property 'destinations' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventarcPipelineDestinations"]], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#location EventarcPipeline#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pipeline_id(self) -> builtins.str:
        '''The user-provided ID to be assigned to the Pipeline. It should match the format '^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#pipeline_id EventarcPipeline#pipeline_id}
        '''
        result = self._values.get("pipeline_id")
        assert result is not None, "Required property 'pipeline_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined annotations. See https://google.aip.dev/128#annotations.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#annotations EventarcPipeline#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def crypto_key_name(self) -> typing.Optional[builtins.str]:
        '''Resource name of a KMS crypto key (managed by the user) used to encrypt/decrypt the event data.

        If not set, an internal Google-owned key
        will be used to encrypt messages. It must match the pattern
        "projects/{project}/locations/{location}/keyRings/{keyring}/cryptoKeys/{key}".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#crypto_key_name EventarcPipeline#crypto_key_name}
        '''
        result = self._values.get("crypto_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Display name of resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#display_name EventarcPipeline#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#id EventarcPipeline#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_payload_format(
        self,
    ) -> typing.Optional["EventarcPipelineInputPayloadFormat"]:
        '''input_payload_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#input_payload_format EventarcPipeline#input_payload_format}
        '''
        result = self._values.get("input_payload_format")
        return typing.cast(typing.Optional["EventarcPipelineInputPayloadFormat"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User labels attached to the Pipeline that can be used to group resources.

        An object containing a list of "key": value pairs. Example: {
        "name": "wrench", "mass": "1.3kg", "count": "3" }.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#labels EventarcPipeline#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def logging_config(self) -> typing.Optional["EventarcPipelineLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#logging_config EventarcPipeline#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["EventarcPipelineLoggingConfig"], result)

    @builtins.property
    def mediations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventarcPipelineMediations"]]]:
        '''mediations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#mediations EventarcPipeline#mediations}
        '''
        result = self._values.get("mediations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventarcPipelineMediations"]]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#project EventarcPipeline#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retry_policy(self) -> typing.Optional["EventarcPipelineRetryPolicy"]:
        '''retry_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#retry_policy EventarcPipeline#retry_policy}
        '''
        result = self._values.get("retry_policy")
        return typing.cast(typing.Optional["EventarcPipelineRetryPolicy"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["EventarcPipelineTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#timeouts EventarcPipeline#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["EventarcPipelineTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcPipelineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineDestinations",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_config": "authenticationConfig",
        "http_endpoint": "httpEndpoint",
        "message_bus": "messageBus",
        "network_config": "networkConfig",
        "output_payload_format": "outputPayloadFormat",
        "topic": "topic",
        "workflow": "workflow",
    },
)
class EventarcPipelineDestinations:
    def __init__(
        self,
        *,
        authentication_config: typing.Optional[typing.Union["EventarcPipelineDestinationsAuthenticationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        http_endpoint: typing.Optional[typing.Union["EventarcPipelineDestinationsHttpEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        message_bus: typing.Optional[builtins.str] = None,
        network_config: typing.Optional[typing.Union["EventarcPipelineDestinationsNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        output_payload_format: typing.Optional[typing.Union["EventarcPipelineDestinationsOutputPayloadFormat", typing.Dict[builtins.str, typing.Any]]] = None,
        topic: typing.Optional[builtins.str] = None,
        workflow: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authentication_config: authentication_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#authentication_config EventarcPipeline#authentication_config}
        :param http_endpoint: http_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#http_endpoint EventarcPipeline#http_endpoint}
        :param message_bus: The resource name of the Message Bus to which events should be published. The Message Bus resource should exist in the same project as the Pipeline. Format: 'projects/{project}/locations/{location}/messageBuses/{message_bus}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#message_bus EventarcPipeline#message_bus}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#network_config EventarcPipeline#network_config}
        :param output_payload_format: output_payload_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#output_payload_format EventarcPipeline#output_payload_format}
        :param topic: The resource name of the Pub/Sub topic to which events should be published. Format: 'projects/{project}/locations/{location}/topics/{topic}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#topic EventarcPipeline#topic}
        :param workflow: The resource name of the Workflow whose Executions are triggered by the events. The Workflow resource should be deployed in the same project as the Pipeline. Format: 'projects/{project}/locations/{location}/workflows/{workflow}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#workflow EventarcPipeline#workflow}
        '''
        if isinstance(authentication_config, dict):
            authentication_config = EventarcPipelineDestinationsAuthenticationConfig(**authentication_config)
        if isinstance(http_endpoint, dict):
            http_endpoint = EventarcPipelineDestinationsHttpEndpoint(**http_endpoint)
        if isinstance(network_config, dict):
            network_config = EventarcPipelineDestinationsNetworkConfig(**network_config)
        if isinstance(output_payload_format, dict):
            output_payload_format = EventarcPipelineDestinationsOutputPayloadFormat(**output_payload_format)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__037f1505370397eb42a4153974d80f1195446c17af31a1fd5a061f6ef6e0e668)
            check_type(argname="argument authentication_config", value=authentication_config, expected_type=type_hints["authentication_config"])
            check_type(argname="argument http_endpoint", value=http_endpoint, expected_type=type_hints["http_endpoint"])
            check_type(argname="argument message_bus", value=message_bus, expected_type=type_hints["message_bus"])
            check_type(argname="argument network_config", value=network_config, expected_type=type_hints["network_config"])
            check_type(argname="argument output_payload_format", value=output_payload_format, expected_type=type_hints["output_payload_format"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument workflow", value=workflow, expected_type=type_hints["workflow"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authentication_config is not None:
            self._values["authentication_config"] = authentication_config
        if http_endpoint is not None:
            self._values["http_endpoint"] = http_endpoint
        if message_bus is not None:
            self._values["message_bus"] = message_bus
        if network_config is not None:
            self._values["network_config"] = network_config
        if output_payload_format is not None:
            self._values["output_payload_format"] = output_payload_format
        if topic is not None:
            self._values["topic"] = topic
        if workflow is not None:
            self._values["workflow"] = workflow

    @builtins.property
    def authentication_config(
        self,
    ) -> typing.Optional["EventarcPipelineDestinationsAuthenticationConfig"]:
        '''authentication_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#authentication_config EventarcPipeline#authentication_config}
        '''
        result = self._values.get("authentication_config")
        return typing.cast(typing.Optional["EventarcPipelineDestinationsAuthenticationConfig"], result)

    @builtins.property
    def http_endpoint(
        self,
    ) -> typing.Optional["EventarcPipelineDestinationsHttpEndpoint"]:
        '''http_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#http_endpoint EventarcPipeline#http_endpoint}
        '''
        result = self._values.get("http_endpoint")
        return typing.cast(typing.Optional["EventarcPipelineDestinationsHttpEndpoint"], result)

    @builtins.property
    def message_bus(self) -> typing.Optional[builtins.str]:
        '''The resource name of the Message Bus to which events should be published.

        The Message Bus resource should exist in the same project as
        the Pipeline. Format:
        'projects/{project}/locations/{location}/messageBuses/{message_bus}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#message_bus EventarcPipeline#message_bus}
        '''
        result = self._values.get("message_bus")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_config(
        self,
    ) -> typing.Optional["EventarcPipelineDestinationsNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#network_config EventarcPipeline#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["EventarcPipelineDestinationsNetworkConfig"], result)

    @builtins.property
    def output_payload_format(
        self,
    ) -> typing.Optional["EventarcPipelineDestinationsOutputPayloadFormat"]:
        '''output_payload_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#output_payload_format EventarcPipeline#output_payload_format}
        '''
        result = self._values.get("output_payload_format")
        return typing.cast(typing.Optional["EventarcPipelineDestinationsOutputPayloadFormat"], result)

    @builtins.property
    def topic(self) -> typing.Optional[builtins.str]:
        '''The resource name of the Pub/Sub topic to which events should be published. Format: 'projects/{project}/locations/{location}/topics/{topic}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#topic EventarcPipeline#topic}
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow(self) -> typing.Optional[builtins.str]:
        '''The resource name of the Workflow whose Executions are triggered by the events.

        The Workflow resource should be deployed in the same
        project as the Pipeline. Format:
        'projects/{project}/locations/{location}/workflows/{workflow}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#workflow EventarcPipeline#workflow}
        '''
        result = self._values.get("workflow")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcPipelineDestinations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineDestinationsAuthenticationConfig",
    jsii_struct_bases=[],
    name_mapping={"google_oidc": "googleOidc", "oauth_token": "oauthToken"},
)
class EventarcPipelineDestinationsAuthenticationConfig:
    def __init__(
        self,
        *,
        google_oidc: typing.Optional[typing.Union["EventarcPipelineDestinationsAuthenticationConfigGoogleOidc", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth_token: typing.Optional[typing.Union["EventarcPipelineDestinationsAuthenticationConfigOauthToken", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param google_oidc: google_oidc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#google_oidc EventarcPipeline#google_oidc}
        :param oauth_token: oauth_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#oauth_token EventarcPipeline#oauth_token}
        '''
        if isinstance(google_oidc, dict):
            google_oidc = EventarcPipelineDestinationsAuthenticationConfigGoogleOidc(**google_oidc)
        if isinstance(oauth_token, dict):
            oauth_token = EventarcPipelineDestinationsAuthenticationConfigOauthToken(**oauth_token)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08ab37c87ddb37bf5f20cb5b746eaab64df99abff43ce87f042bc1e7a0fd4386)
            check_type(argname="argument google_oidc", value=google_oidc, expected_type=type_hints["google_oidc"])
            check_type(argname="argument oauth_token", value=oauth_token, expected_type=type_hints["oauth_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if google_oidc is not None:
            self._values["google_oidc"] = google_oidc
        if oauth_token is not None:
            self._values["oauth_token"] = oauth_token

    @builtins.property
    def google_oidc(
        self,
    ) -> typing.Optional["EventarcPipelineDestinationsAuthenticationConfigGoogleOidc"]:
        '''google_oidc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#google_oidc EventarcPipeline#google_oidc}
        '''
        result = self._values.get("google_oidc")
        return typing.cast(typing.Optional["EventarcPipelineDestinationsAuthenticationConfigGoogleOidc"], result)

    @builtins.property
    def oauth_token(
        self,
    ) -> typing.Optional["EventarcPipelineDestinationsAuthenticationConfigOauthToken"]:
        '''oauth_token block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#oauth_token EventarcPipeline#oauth_token}
        '''
        result = self._values.get("oauth_token")
        return typing.cast(typing.Optional["EventarcPipelineDestinationsAuthenticationConfigOauthToken"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcPipelineDestinationsAuthenticationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineDestinationsAuthenticationConfigGoogleOidc",
    jsii_struct_bases=[],
    name_mapping={"service_account": "serviceAccount", "audience": "audience"},
)
class EventarcPipelineDestinationsAuthenticationConfigGoogleOidc:
    def __init__(
        self,
        *,
        service_account: builtins.str,
        audience: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account: Service account email used to generate the OIDC Token. The principal who calls this API must have iam.serviceAccounts.actAs permission in the service account. See https://cloud.google.com/iam/docs/understanding-service-accounts for more information. Eventarc service agents must have roles/roles/iam.serviceAccountTokenCreator role to allow the Pipeline to create OpenID tokens for authenticated requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#service_account EventarcPipeline#service_account}
        :param audience: Audience to be used to generate the OIDC Token. The audience claim identifies the recipient that the JWT is intended for. If unspecified, the destination URI will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#audience EventarcPipeline#audience}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__056e03a1e53a2b4449c2a6730cc8d3b4dd4dc6985beed68d5af5eda64b0ef15a)
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument audience", value=audience, expected_type=type_hints["audience"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_account": service_account,
        }
        if audience is not None:
            self._values["audience"] = audience

    @builtins.property
    def service_account(self) -> builtins.str:
        '''Service account email used to generate the OIDC Token.

        The principal who calls this API must have
        iam.serviceAccounts.actAs permission in the service account. See
        https://cloud.google.com/iam/docs/understanding-service-accounts
        for more information. Eventarc service agents must have
        roles/roles/iam.serviceAccountTokenCreator role to allow the
        Pipeline to create OpenID tokens for authenticated requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#service_account EventarcPipeline#service_account}
        '''
        result = self._values.get("service_account")
        assert result is not None, "Required property 'service_account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def audience(self) -> typing.Optional[builtins.str]:
        '''Audience to be used to generate the OIDC Token.

        The audience claim
        identifies the recipient that the JWT is intended for. If
        unspecified, the destination URI will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#audience EventarcPipeline#audience}
        '''
        result = self._values.get("audience")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcPipelineDestinationsAuthenticationConfigGoogleOidc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcPipelineDestinationsAuthenticationConfigGoogleOidcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineDestinationsAuthenticationConfigGoogleOidcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8da92feeb0ad357d47ed44c1b8f9e78af61b0ce0df7675d76b8cb5f62d2883ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAudience")
    def reset_audience(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudience", []))

    @builtins.property
    @jsii.member(jsii_name="audienceInput")
    def audience_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audienceInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="audience")
    def audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audience"))

    @audience.setter
    def audience(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56760f5d38488686ceb88e108ff398f98158058f283b4c741f3df2304f6cc281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audience", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2e3a72e232a08c4731cfc140fe6c9cc9b8614e12c617cb7178bb7176e343548)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventarcPipelineDestinationsAuthenticationConfigGoogleOidc]:
        return typing.cast(typing.Optional[EventarcPipelineDestinationsAuthenticationConfigGoogleOidc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcPipelineDestinationsAuthenticationConfigGoogleOidc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__770e46b7155850041be548eab25f7356855886709aaa2c5f2842c3d4314edce2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineDestinationsAuthenticationConfigOauthToken",
    jsii_struct_bases=[],
    name_mapping={"service_account": "serviceAccount", "scope": "scope"},
)
class EventarcPipelineDestinationsAuthenticationConfigOauthToken:
    def __init__(
        self,
        *,
        service_account: builtins.str,
        scope: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account: Service account email used to generate the `OAuth token <https://developers.google.com/identity/protocols/OAuth2>`_. The principal who calls this API must have iam.serviceAccounts.actAs permission in the service account. See https://cloud.google.com/iam/docs/understanding-service-accounts for more information. Eventarc service agents must have roles/roles/iam.serviceAccountTokenCreator role to allow Pipeline to create OAuth2 tokens for authenticated requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#service_account EventarcPipeline#service_account}
        :param scope: OAuth scope to be used for generating OAuth access token. If not specified, "https://www.googleapis.com/auth/cloud-platform" will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#scope EventarcPipeline#scope}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25da3285785d017f1c52033bed3be3178630f16fb472a5efe8d3d64003dc5a19)
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_account": service_account,
        }
        if scope is not None:
            self._values["scope"] = scope

    @builtins.property
    def service_account(self) -> builtins.str:
        '''Service account email used to generate the `OAuth token <https://developers.google.com/identity/protocols/OAuth2>`_. The principal who calls this API must have iam.serviceAccounts.actAs permission in the service account. See https://cloud.google.com/iam/docs/understanding-service-accounts for more information. Eventarc service agents must have roles/roles/iam.serviceAccountTokenCreator role to allow Pipeline to create OAuth2 tokens for authenticated requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#service_account EventarcPipeline#service_account}
        '''
        result = self._values.get("service_account")
        assert result is not None, "Required property 'service_account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''OAuth scope to be used for generating OAuth access token. If not specified, "https://www.googleapis.com/auth/cloud-platform" will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#scope EventarcPipeline#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcPipelineDestinationsAuthenticationConfigOauthToken(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcPipelineDestinationsAuthenticationConfigOauthTokenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineDestinationsAuthenticationConfigOauthTokenOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fb3e87a41a7a16d7539f525b4016340ef2098962b0cd33987c5db4ad7d7e9bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__924c564d1f04c59d6e4a4474fa4cba1c04a979753d377b316398dac9522c647c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc65bdcff4e700cfcec14ba9edccd58fc3076d45c93e4c80eed46f01e289e147)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventarcPipelineDestinationsAuthenticationConfigOauthToken]:
        return typing.cast(typing.Optional[EventarcPipelineDestinationsAuthenticationConfigOauthToken], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcPipelineDestinationsAuthenticationConfigOauthToken],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c342a75edd63bbc8ebd33a0f3c87cd5be317f595c8d5384ec676a3ec1362b11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventarcPipelineDestinationsAuthenticationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineDestinationsAuthenticationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e490d61a44c89313a704dabad8d43485dc67a13a4d97820f8e732323e31cf0e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGoogleOidc")
    def put_google_oidc(
        self,
        *,
        service_account: builtins.str,
        audience: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account: Service account email used to generate the OIDC Token. The principal who calls this API must have iam.serviceAccounts.actAs permission in the service account. See https://cloud.google.com/iam/docs/understanding-service-accounts for more information. Eventarc service agents must have roles/roles/iam.serviceAccountTokenCreator role to allow the Pipeline to create OpenID tokens for authenticated requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#service_account EventarcPipeline#service_account}
        :param audience: Audience to be used to generate the OIDC Token. The audience claim identifies the recipient that the JWT is intended for. If unspecified, the destination URI will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#audience EventarcPipeline#audience}
        '''
        value = EventarcPipelineDestinationsAuthenticationConfigGoogleOidc(
            service_account=service_account, audience=audience
        )

        return typing.cast(None, jsii.invoke(self, "putGoogleOidc", [value]))

    @jsii.member(jsii_name="putOauthToken")
    def put_oauth_token(
        self,
        *,
        service_account: builtins.str,
        scope: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account: Service account email used to generate the `OAuth token <https://developers.google.com/identity/protocols/OAuth2>`_. The principal who calls this API must have iam.serviceAccounts.actAs permission in the service account. See https://cloud.google.com/iam/docs/understanding-service-accounts for more information. Eventarc service agents must have roles/roles/iam.serviceAccountTokenCreator role to allow Pipeline to create OAuth2 tokens for authenticated requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#service_account EventarcPipeline#service_account}
        :param scope: OAuth scope to be used for generating OAuth access token. If not specified, "https://www.googleapis.com/auth/cloud-platform" will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#scope EventarcPipeline#scope}
        '''
        value = EventarcPipelineDestinationsAuthenticationConfigOauthToken(
            service_account=service_account, scope=scope
        )

        return typing.cast(None, jsii.invoke(self, "putOauthToken", [value]))

    @jsii.member(jsii_name="resetGoogleOidc")
    def reset_google_oidc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoogleOidc", []))

    @jsii.member(jsii_name="resetOauthToken")
    def reset_oauth_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthToken", []))

    @builtins.property
    @jsii.member(jsii_name="googleOidc")
    def google_oidc(
        self,
    ) -> EventarcPipelineDestinationsAuthenticationConfigGoogleOidcOutputReference:
        return typing.cast(EventarcPipelineDestinationsAuthenticationConfigGoogleOidcOutputReference, jsii.get(self, "googleOidc"))

    @builtins.property
    @jsii.member(jsii_name="oauthToken")
    def oauth_token(
        self,
    ) -> EventarcPipelineDestinationsAuthenticationConfigOauthTokenOutputReference:
        return typing.cast(EventarcPipelineDestinationsAuthenticationConfigOauthTokenOutputReference, jsii.get(self, "oauthToken"))

    @builtins.property
    @jsii.member(jsii_name="googleOidcInput")
    def google_oidc_input(
        self,
    ) -> typing.Optional[EventarcPipelineDestinationsAuthenticationConfigGoogleOidc]:
        return typing.cast(typing.Optional[EventarcPipelineDestinationsAuthenticationConfigGoogleOidc], jsii.get(self, "googleOidcInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthTokenInput")
    def oauth_token_input(
        self,
    ) -> typing.Optional[EventarcPipelineDestinationsAuthenticationConfigOauthToken]:
        return typing.cast(typing.Optional[EventarcPipelineDestinationsAuthenticationConfigOauthToken], jsii.get(self, "oauthTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventarcPipelineDestinationsAuthenticationConfig]:
        return typing.cast(typing.Optional[EventarcPipelineDestinationsAuthenticationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcPipelineDestinationsAuthenticationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ba5e11c4acb3a9df145d5bafc462238281a32dd2980785b3d96b77dbb9e2ddd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineDestinationsHttpEndpoint",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "message_binding_template": "messageBindingTemplate"},
)
class EventarcPipelineDestinationsHttpEndpoint:
    def __init__(
        self,
        *,
        uri: builtins.str,
        message_binding_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: The URI of the HTTP enpdoint. The value must be a RFC2396 URI string. Examples: 'https://svc.us-central1.p.local:8080/route'. Only the HTTPS protocol is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#uri EventarcPipeline#uri}
        :param message_binding_template: The CEL expression used to modify how the destination-bound HTTP request is constructed. If a binding expression is not specified here, the message is treated as a CloudEvent and is mapped to the HTTP request according to the CloudEvent HTTP Protocol Binding Binary Content Mode (https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/http-protocol-binding.md#31-binary-content-mode). In this representation, all fields except the 'data' and 'datacontenttype' field on the message are mapped to HTTP request headers with a prefix of 'ce-'. To construct the HTTP request payload and the value of the content-type HTTP header, the payload format is defined as follows: 1. Use the output_payload_format_type on the Pipeline.Destination if it is set, else: 2. Use the input_payload_format_type on the Pipeline if it is set, else: 3. Treat the payload as opaque binary data. The 'data' field of the message is converted to the payload format or left as-is for case 3) and then attached as the payload of the HTTP request. The 'content-type' header on the HTTP request is set to the payload format type or left empty for case 3). However, if a mediation has updated the 'datacontenttype' field on the message so that it is not the same as the payload format type but it is still a prefix of the payload format type, then the 'content-type' header on the HTTP request is set to this 'datacontenttype' value. For example, if the 'datacontenttype' is "application/json" and the payload format type is "application/json; charset=utf-8", then the 'content-type' header on the HTTP request is set to "application/json; charset=utf-8". If a non-empty binding expression is specified then this expression is used to modify the default CloudEvent HTTP Protocol Binding Binary Content representation. The result of the CEL expression must be a map of key/value pairs which is used as follows: - If a map named 'headers' exists on the result of the expression, then its key/value pairs are directly mapped to the HTTP request headers. The headers values are constructed from the corresponding value type's canonical representation. If the 'headers' field doesn't exist then the resulting HTTP request will be the headers of the CloudEvent HTTP Binding Binary Content Mode representation of the final message. Note: If the specified binding expression, has updated the 'datacontenttype' field on the message so that it is not the same as the payload format type but it is still a prefix of the payload format type, then the 'content-type' header in the 'headers' map is set to this 'datacontenttype' value. - If a field named 'body' exists on the result of the expression then its value is directly mapped to the body of the request. If the value of the 'body' field is of type bytes or string then it is used for the HTTP request body as-is, with no conversion. If the body field is of any other type then it is converted to a JSON string. If the body field does not exist then the resulting payload of the HTTP request will be data value of the CloudEvent HTTP Binding Binary Content Mode representation of the final message as described earlier. - Any other fields in the resulting expression will be ignored. The CEL expression may access the incoming CloudEvent message in its definition, as follows: - The 'data' field of the incoming CloudEvent message can be accessed using the 'message.data' value. Subfields of 'message.data' may also be accessed if an input_payload_format has been specified on the Pipeline. - Each attribute of the incoming CloudEvent message can be accessed using the 'message.' value, where is replaced with the name of the attribute. - Existing headers can be accessed in the CEL expression using the 'headers' variable. The 'headers' variable defines a map of key/value pairs corresponding to the HTTP headers of the CloudEvent HTTP Binding Binary Content Mode representation of the final message as described earlier. For example, the following CEL expression can be used to construct an HTTP request by adding an additional header to the HTTP headers of the CloudEvent HTTP Binding Binary Content Mode representation of the final message and by overwriting the body of the request: Example:: { "headers": headers.merge({"new-header-key": "new-header-value"}), "body": "new-body" } - The default binding for the message payload can be accessed using the 'body' variable. It conatins a string representation of the message payload in the format specified by the 'output_payload_format' field. If the 'input_payload_format' field is not set, the 'body' variable contains the same message payload bytes that were published. Additionally, the following CEL extension functions are provided for use in this CEL expression: - toBase64Url: map.toBase64Url() -> string - Converts a CelValue to a base64url encoded string - toJsonString: map.toJsonString() -> string - Converts a CelValue to a JSON string - merge: map1.merge(map2) -> map3 - Merges the passed CEL map with the existing CEL map the function is applied to. - If the same key exists in both maps, if the key's value is type map both maps are merged else the value from the passed map is used. - denormalize: map.denormalize() -> map - Denormalizes a CEL map such that every value of type map or key in the map is expanded to return a single level map. - The resulting keys are "." separated indices of the map keys. - For example: { "a": 1, "b": { "c": 2, "d": 3 } "e": [4, 5] } .denormalize() -> { "a": 1, "b.c": 2, "b.d": 3, "e.0": 4, "e.1": 5 } - setField: map.setField(key, value) -> message - Sets the field of the message with the given key to the given value. - If the field is not present it will be added. - If the field is present it will be overwritten. - The key can be a dot separated path to set a field in a nested message. - Key must be of type string. - Value may be any valid type. - removeFields: map.removeFields([key1, key2, ...]) -> message - Removes the fields of the map with the given keys. - The keys can be a dot separated path to remove a field in a nested message. - If a key is not found it will be ignored. - Keys must be of type string. - toMap: [map1, map2, ...].toMap() -> map - Converts a CEL list of CEL maps to a single CEL map - toCloudEventJsonWithPayloadFormat: message.toCloudEventJsonWithPayloadFormat() -> map - Converts a message to the corresponding structure of JSON format for CloudEvents. - It converts 'data' to destination payload format specified in 'output_payload_format'. If 'output_payload_format' is not set, the data will remain unchanged. - It also sets the corresponding datacontenttype of the CloudEvent, as indicated by 'output_payload_format'. If no 'output_payload_format' is set it will use the value of the "datacontenttype" attribute on the CloudEvent if present, else remove "datacontenttype" attribute. - This function expects that the content of the message will adhere to the standard CloudEvent format. If it doesn't then this function will fail. - The result is a CEL map that corresponds to the JSON representation of the CloudEvent. To convert that data to a JSON string it can be chained with the toJsonString function. The Pipeline expects that the message it receives adheres to the standard CloudEvent format. If it doesn't then the outgoing message request may fail with a persistent error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#message_binding_template EventarcPipeline#message_binding_template}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26476e2660200ccb647e2022a6af6b9ff9001ea9b899a90003402498bd922bd4)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument message_binding_template", value=message_binding_template, expected_type=type_hints["message_binding_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if message_binding_template is not None:
            self._values["message_binding_template"] = message_binding_template

    @builtins.property
    def uri(self) -> builtins.str:
        '''The URI of the HTTP enpdoint.

        The value must be a RFC2396 URI string.
        Examples: 'https://svc.us-central1.p.local:8080/route'.
        Only the HTTPS protocol is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#uri EventarcPipeline#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def message_binding_template(self) -> typing.Optional[builtins.str]:
        '''The CEL expression used to modify how the destination-bound HTTP request is constructed.

        If a binding expression is not specified here, the message
        is treated as a CloudEvent and is mapped to the HTTP request according
        to the CloudEvent HTTP Protocol Binding Binary Content Mode
        (https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/http-protocol-binding.md#31-binary-content-mode).
        In this representation, all fields except the 'data' and
        'datacontenttype' field on the message are mapped to HTTP request
        headers with a prefix of 'ce-'.

        To construct the HTTP request payload and the value of the content-type
        HTTP header, the payload format is defined as follows:

        1. Use the output_payload_format_type on the Pipeline.Destination if it
           is set, else:
        2. Use the input_payload_format_type on the Pipeline if it is set,
           else:
        3. Treat the payload as opaque binary data.

        The 'data' field of the message is converted to the payload format or
        left as-is for case 3) and then attached as the payload of the HTTP
        request. The 'content-type' header on the HTTP request is set to the
        payload format type or left empty for case 3). However, if a mediation
        has updated the 'datacontenttype' field on the message so that it is
        not the same as the payload format type but it is still a prefix of the
        payload format type, then the 'content-type' header on the HTTP request
        is set to this 'datacontenttype' value. For example, if the
        'datacontenttype' is "application/json" and the payload format type is
        "application/json; charset=utf-8", then the 'content-type' header on
        the HTTP request is set to "application/json; charset=utf-8".

        If a non-empty binding expression is specified then this expression is
        used to modify the default CloudEvent HTTP Protocol Binding Binary
        Content representation.
        The result of the CEL expression must be a map of key/value pairs
        which is used as follows:

        - If a map named 'headers' exists on the result of the expression,
          then its key/value pairs are directly mapped to the HTTP request
          headers. The headers values are constructed from the corresponding
          value type's canonical representation. If the 'headers' field doesn't
          exist then the resulting HTTP request will be the headers of the
          CloudEvent HTTP Binding Binary Content Mode representation of the final
          message. Note: If the specified binding expression, has updated the
          'datacontenttype' field on the message so that it is not the same as
          the payload format type but it is still a prefix of the payload format
          type, then the 'content-type' header in the 'headers' map is set to
          this 'datacontenttype' value.
        - If a field named 'body' exists on the result of the expression then
          its value is directly mapped to the body of the request. If the value
          of the 'body' field is of type bytes or string then it is used for
          the HTTP request body as-is, with no conversion. If the body field is
          of any other type then it is converted to a JSON string. If the body
          field does not exist then the resulting payload of the HTTP request
          will be data value of the CloudEvent HTTP Binding Binary Content Mode
          representation of the final message as described earlier.
        - Any other fields in the resulting expression will be ignored.

        The CEL expression may access the incoming CloudEvent message in its
        definition, as follows:

        - The 'data' field of the incoming CloudEvent message can be accessed
          using the 'message.data' value. Subfields of 'message.data' may also be
          accessed if an input_payload_format has been specified on the Pipeline.
        - Each attribute of the incoming CloudEvent message can be accessed
          using the 'message.' value, where  is replaced with the
          name of the attribute.
        - Existing headers can be accessed in the CEL expression using the
          'headers' variable. The 'headers' variable defines a map of key/value
          pairs corresponding to the HTTP headers of the CloudEvent HTTP Binding
          Binary Content Mode representation of the final message as described
          earlier. For example, the following CEL expression can be used to
          construct an HTTP request by adding an additional header to the HTTP
          headers of the CloudEvent HTTP Binding Binary Content Mode
          representation of the final message and by overwriting the body of the
          request:

        Example::

           {
           "headers": headers.merge({"new-header-key": "new-header-value"}),
           "body": "new-body"
           }

        - The default binding for the message payload can be accessed using the
          'body' variable. It conatins a string representation of the message
          payload in the format specified by the 'output_payload_format' field.
          If the 'input_payload_format' field is not set, the 'body'
          variable contains the same message payload bytes that were published.

        Additionally, the following CEL extension functions are provided for
        use in this CEL expression:

        - toBase64Url:
          map.toBase64Url() -> string
        - Converts a CelValue to a base64url encoded string
        - toJsonString: map.toJsonString() -> string
        - Converts a CelValue to a JSON string
        - merge:
          map1.merge(map2) -> map3
        - Merges the passed CEL map with the existing CEL map the
          function is applied to.
        - If the same key exists in both maps, if the key's value is type
          map both maps are merged else the value from the passed map is
          used.
        - denormalize:
          map.denormalize() -> map
        - Denormalizes a CEL map such that every value of type map or key
          in the map is expanded to return a single level map.
        - The resulting keys are "." separated indices of the map keys.
        - For example:
          {
          "a": 1,
          "b": {
          "c": 2,
          "d": 3
          }
          "e": [4, 5]
          }
          .denormalize()
          -> {
          "a": 1,
          "b.c": 2,
          "b.d": 3,
          "e.0": 4,
          "e.1": 5
          }
        - setField:
          map.setField(key, value) -> message
        - Sets the field of the message with the given key to the
          given value.
        - If the field is not present it will be added.
        - If the field is present it will be overwritten.
        - The key can be a dot separated path to set a field in a nested
          message.
        - Key must be of type string.
        - Value may be any valid type.
        - removeFields:
          map.removeFields([key1, key2, ...]) -> message
        - Removes the fields of the map with the given keys.
        - The keys can be a dot separated path to remove a field in a
          nested message.
        - If a key is not found it will be ignored.
        - Keys must be of type string.
        - toMap:
          [map1, map2, ...].toMap() -> map
        - Converts a CEL list of CEL maps to a single CEL map
        - toCloudEventJsonWithPayloadFormat:
          message.toCloudEventJsonWithPayloadFormat() -> map
        - Converts a message to the corresponding structure of JSON
          format for CloudEvents.
        - It converts 'data' to destination payload format
          specified in 'output_payload_format'. If 'output_payload_format' is
          not set, the data will remain unchanged.
        - It also sets the corresponding datacontenttype of
          the CloudEvent, as indicated by
          'output_payload_format'. If no
          'output_payload_format' is set it will use the value of the
          "datacontenttype" attribute on the CloudEvent if present, else
          remove "datacontenttype" attribute.
        - This function expects that the content of the message will
          adhere to the standard CloudEvent format. If it doesn't then this
          function will fail.
        - The result is a CEL map that corresponds to the JSON
          representation of the CloudEvent. To convert that data to a JSON
          string it can be chained with the toJsonString function.

        The Pipeline expects that the message it receives adheres to the
        standard CloudEvent format. If it doesn't then the outgoing message
        request may fail with a persistent error.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#message_binding_template EventarcPipeline#message_binding_template}
        '''
        result = self._values.get("message_binding_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcPipelineDestinationsHttpEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcPipelineDestinationsHttpEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineDestinationsHttpEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22523c5ea67b07bbd7455749b56a64b1d050a660ae0e53a7999471ed565aaba6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMessageBindingTemplate")
    def reset_message_binding_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageBindingTemplate", []))

    @builtins.property
    @jsii.member(jsii_name="messageBindingTemplateInput")
    def message_binding_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageBindingTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="messageBindingTemplate")
    def message_binding_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageBindingTemplate"))

    @message_binding_template.setter
    def message_binding_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09f8ee8eb0ece6ba75d32335a628f9e9da79658b533e05953c6ebd82d14cd1e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageBindingTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17620aa7f3b83ae2ca9c7d90009d78911dd432fb909dcf01dc2d0e809a949a5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventarcPipelineDestinationsHttpEndpoint]:
        return typing.cast(typing.Optional[EventarcPipelineDestinationsHttpEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcPipelineDestinationsHttpEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bccf08807ca5049eea2716d1834c46ccc54e293cb55b06d0753917a71482ad73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventarcPipelineDestinationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineDestinationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea29ed316f948938858bc2a24ef6786f0b155722dddbafb17f98c677246e2fad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EventarcPipelineDestinationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__765701db335dfb14578fdb51aa027729129bed838c3846ee8c00ec2e92d7757b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventarcPipelineDestinationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0152769295f81cb73f330ad1cc5ba8dc040c59225647a723af3e5d8af888a07c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f18adc14f454a9b25d963feb97e3ee673b2222ee76dea9bc5d93bcbb5a53c4c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92724f1ed30f52983bdd5411d84d85402070e5a0e0bc89ce8d8865d43fa48ff4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventarcPipelineDestinations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventarcPipelineDestinations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventarcPipelineDestinations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db433d4bea1a7e2915c503cf58981893101e7aec85894a2697b87adb548750ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineDestinationsNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={"network_attachment": "networkAttachment"},
)
class EventarcPipelineDestinationsNetworkConfig:
    def __init__(
        self,
        *,
        network_attachment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param network_attachment: Name of the NetworkAttachment that allows access to the consumer VPC. Format: 'projects/{PROJECT_ID}/regions/{REGION}/networkAttachments/{NETWORK_ATTACHMENT_NAME}' Required for HTTP endpoint destinations. Must not be specified for Workflows, MessageBus, or Topic destinations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#network_attachment EventarcPipeline#network_attachment}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56b475af01585579a92c697221dc5dcd8513d5dc93405d41d4448337ef3cf379)
            check_type(argname="argument network_attachment", value=network_attachment, expected_type=type_hints["network_attachment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if network_attachment is not None:
            self._values["network_attachment"] = network_attachment

    @builtins.property
    def network_attachment(self) -> typing.Optional[builtins.str]:
        '''Name of the NetworkAttachment that allows access to the consumer VPC.

        Format:
        'projects/{PROJECT_ID}/regions/{REGION}/networkAttachments/{NETWORK_ATTACHMENT_NAME}'

        Required for HTTP endpoint destinations. Must not be specified for
        Workflows, MessageBus, or Topic destinations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#network_attachment EventarcPipeline#network_attachment}
        '''
        result = self._values.get("network_attachment")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcPipelineDestinationsNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcPipelineDestinationsNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineDestinationsNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78d2dc67a176242d4c1fa5ee312ce71124b645c935a60aebd2da1bd7a1a12991)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNetworkAttachment")
    def reset_network_attachment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkAttachment", []))

    @builtins.property
    @jsii.member(jsii_name="networkAttachmentInput")
    def network_attachment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkAttachmentInput"))

    @builtins.property
    @jsii.member(jsii_name="networkAttachment")
    def network_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkAttachment"))

    @network_attachment.setter
    def network_attachment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b9e75c05b29d985176144d2562faaaf8674fbd36621f6abec58d126c8dbc68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkAttachment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventarcPipelineDestinationsNetworkConfig]:
        return typing.cast(typing.Optional[EventarcPipelineDestinationsNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcPipelineDestinationsNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daa9e8317c52ed96e7f21676908cc7a8615fd4e4d42125c4cb64e562d90187e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineDestinationsOutputPayloadFormat",
    jsii_struct_bases=[],
    name_mapping={"avro": "avro", "json": "json", "protobuf": "protobuf"},
)
class EventarcPipelineDestinationsOutputPayloadFormat:
    def __init__(
        self,
        *,
        avro: typing.Optional[typing.Union["EventarcPipelineDestinationsOutputPayloadFormatAvro", typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union["EventarcPipelineDestinationsOutputPayloadFormatJson", typing.Dict[builtins.str, typing.Any]]] = None,
        protobuf: typing.Optional[typing.Union["EventarcPipelineDestinationsOutputPayloadFormatProtobuf", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param avro: avro block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#avro EventarcPipeline#avro}
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#json EventarcPipeline#json}
        :param protobuf: protobuf block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#protobuf EventarcPipeline#protobuf}
        '''
        if isinstance(avro, dict):
            avro = EventarcPipelineDestinationsOutputPayloadFormatAvro(**avro)
        if isinstance(json, dict):
            json = EventarcPipelineDestinationsOutputPayloadFormatJson(**json)
        if isinstance(protobuf, dict):
            protobuf = EventarcPipelineDestinationsOutputPayloadFormatProtobuf(**protobuf)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__684038ae5fea68c5637c497c0809dedb6c49623eda2e9ace351972caa1207a56)
            check_type(argname="argument avro", value=avro, expected_type=type_hints["avro"])
            check_type(argname="argument json", value=json, expected_type=type_hints["json"])
            check_type(argname="argument protobuf", value=protobuf, expected_type=type_hints["protobuf"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if avro is not None:
            self._values["avro"] = avro
        if json is not None:
            self._values["json"] = json
        if protobuf is not None:
            self._values["protobuf"] = protobuf

    @builtins.property
    def avro(
        self,
    ) -> typing.Optional["EventarcPipelineDestinationsOutputPayloadFormatAvro"]:
        '''avro block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#avro EventarcPipeline#avro}
        '''
        result = self._values.get("avro")
        return typing.cast(typing.Optional["EventarcPipelineDestinationsOutputPayloadFormatAvro"], result)

    @builtins.property
    def json(
        self,
    ) -> typing.Optional["EventarcPipelineDestinationsOutputPayloadFormatJson"]:
        '''json block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#json EventarcPipeline#json}
        '''
        result = self._values.get("json")
        return typing.cast(typing.Optional["EventarcPipelineDestinationsOutputPayloadFormatJson"], result)

    @builtins.property
    def protobuf(
        self,
    ) -> typing.Optional["EventarcPipelineDestinationsOutputPayloadFormatProtobuf"]:
        '''protobuf block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#protobuf EventarcPipeline#protobuf}
        '''
        result = self._values.get("protobuf")
        return typing.cast(typing.Optional["EventarcPipelineDestinationsOutputPayloadFormatProtobuf"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcPipelineDestinationsOutputPayloadFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineDestinationsOutputPayloadFormatAvro",
    jsii_struct_bases=[],
    name_mapping={"schema_definition": "schemaDefinition"},
)
class EventarcPipelineDestinationsOutputPayloadFormatAvro:
    def __init__(
        self,
        *,
        schema_definition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema_definition: The entire schema definition is stored in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#schema_definition EventarcPipeline#schema_definition}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d44e03856ae6a53a6b1be9395fb19b85aa0e9e662d72b8d0cf70d1370a2e9c71)
            check_type(argname="argument schema_definition", value=schema_definition, expected_type=type_hints["schema_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if schema_definition is not None:
            self._values["schema_definition"] = schema_definition

    @builtins.property
    def schema_definition(self) -> typing.Optional[builtins.str]:
        '''The entire schema definition is stored in this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#schema_definition EventarcPipeline#schema_definition}
        '''
        result = self._values.get("schema_definition")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcPipelineDestinationsOutputPayloadFormatAvro(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcPipelineDestinationsOutputPayloadFormatAvroOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineDestinationsOutputPayloadFormatAvroOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab5e60f12403894424ebddd6f6e7c2c6ba383d0aece3896fe8e2cabe7a210449)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSchemaDefinition")
    def reset_schema_definition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaDefinition", []))

    @builtins.property
    @jsii.member(jsii_name="schemaDefinitionInput")
    def schema_definition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaDefinition")
    def schema_definition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaDefinition"))

    @schema_definition.setter
    def schema_definition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c5c8cc5d1265788ea3027599ddd13392405e1454abf8dc5986e9309cf8839ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaDefinition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventarcPipelineDestinationsOutputPayloadFormatAvro]:
        return typing.cast(typing.Optional[EventarcPipelineDestinationsOutputPayloadFormatAvro], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcPipelineDestinationsOutputPayloadFormatAvro],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9add6a53a764d1bfb8733c468402e50f3ff82eaa0bec9394dfd636287195ed34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineDestinationsOutputPayloadFormatJson",
    jsii_struct_bases=[],
    name_mapping={},
)
class EventarcPipelineDestinationsOutputPayloadFormatJson:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcPipelineDestinationsOutputPayloadFormatJson(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcPipelineDestinationsOutputPayloadFormatJsonOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineDestinationsOutputPayloadFormatJsonOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d203d964654fa37652ba820d3b23dd82a4a2dff7bb1031271e2419e7a712e460)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventarcPipelineDestinationsOutputPayloadFormatJson]:
        return typing.cast(typing.Optional[EventarcPipelineDestinationsOutputPayloadFormatJson], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcPipelineDestinationsOutputPayloadFormatJson],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee0a369ef5918078ab6736c7cafe79345d73472fdccb4f45fd7aae055fc6e82d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventarcPipelineDestinationsOutputPayloadFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineDestinationsOutputPayloadFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3413a76be45efdf24a67366617f778fce2f3fc29afe6a1ac00aeb860efeb7cdf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAvro")
    def put_avro(
        self,
        *,
        schema_definition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema_definition: The entire schema definition is stored in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#schema_definition EventarcPipeline#schema_definition}
        '''
        value = EventarcPipelineDestinationsOutputPayloadFormatAvro(
            schema_definition=schema_definition
        )

        return typing.cast(None, jsii.invoke(self, "putAvro", [value]))

    @jsii.member(jsii_name="putJson")
    def put_json(self) -> None:
        value = EventarcPipelineDestinationsOutputPayloadFormatJson()

        return typing.cast(None, jsii.invoke(self, "putJson", [value]))

    @jsii.member(jsii_name="putProtobuf")
    def put_protobuf(
        self,
        *,
        schema_definition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema_definition: The entire schema definition is stored in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#schema_definition EventarcPipeline#schema_definition}
        '''
        value = EventarcPipelineDestinationsOutputPayloadFormatProtobuf(
            schema_definition=schema_definition
        )

        return typing.cast(None, jsii.invoke(self, "putProtobuf", [value]))

    @jsii.member(jsii_name="resetAvro")
    def reset_avro(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvro", []))

    @jsii.member(jsii_name="resetJson")
    def reset_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJson", []))

    @jsii.member(jsii_name="resetProtobuf")
    def reset_protobuf(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtobuf", []))

    @builtins.property
    @jsii.member(jsii_name="avro")
    def avro(
        self,
    ) -> EventarcPipelineDestinationsOutputPayloadFormatAvroOutputReference:
        return typing.cast(EventarcPipelineDestinationsOutputPayloadFormatAvroOutputReference, jsii.get(self, "avro"))

    @builtins.property
    @jsii.member(jsii_name="json")
    def json(
        self,
    ) -> EventarcPipelineDestinationsOutputPayloadFormatJsonOutputReference:
        return typing.cast(EventarcPipelineDestinationsOutputPayloadFormatJsonOutputReference, jsii.get(self, "json"))

    @builtins.property
    @jsii.member(jsii_name="protobuf")
    def protobuf(
        self,
    ) -> "EventarcPipelineDestinationsOutputPayloadFormatProtobufOutputReference":
        return typing.cast("EventarcPipelineDestinationsOutputPayloadFormatProtobufOutputReference", jsii.get(self, "protobuf"))

    @builtins.property
    @jsii.member(jsii_name="avroInput")
    def avro_input(
        self,
    ) -> typing.Optional[EventarcPipelineDestinationsOutputPayloadFormatAvro]:
        return typing.cast(typing.Optional[EventarcPipelineDestinationsOutputPayloadFormatAvro], jsii.get(self, "avroInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonInput")
    def json_input(
        self,
    ) -> typing.Optional[EventarcPipelineDestinationsOutputPayloadFormatJson]:
        return typing.cast(typing.Optional[EventarcPipelineDestinationsOutputPayloadFormatJson], jsii.get(self, "jsonInput"))

    @builtins.property
    @jsii.member(jsii_name="protobufInput")
    def protobuf_input(
        self,
    ) -> typing.Optional["EventarcPipelineDestinationsOutputPayloadFormatProtobuf"]:
        return typing.cast(typing.Optional["EventarcPipelineDestinationsOutputPayloadFormatProtobuf"], jsii.get(self, "protobufInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventarcPipelineDestinationsOutputPayloadFormat]:
        return typing.cast(typing.Optional[EventarcPipelineDestinationsOutputPayloadFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcPipelineDestinationsOutputPayloadFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c835753dea67698bb3d4bd18c4c1d267e77e19d2f3288d61c89930c983bb2208)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineDestinationsOutputPayloadFormatProtobuf",
    jsii_struct_bases=[],
    name_mapping={"schema_definition": "schemaDefinition"},
)
class EventarcPipelineDestinationsOutputPayloadFormatProtobuf:
    def __init__(
        self,
        *,
        schema_definition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema_definition: The entire schema definition is stored in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#schema_definition EventarcPipeline#schema_definition}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b571410c0ce67ce9377caad6783f51db972da0826559deb6dc6b0cbb03da96c6)
            check_type(argname="argument schema_definition", value=schema_definition, expected_type=type_hints["schema_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if schema_definition is not None:
            self._values["schema_definition"] = schema_definition

    @builtins.property
    def schema_definition(self) -> typing.Optional[builtins.str]:
        '''The entire schema definition is stored in this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#schema_definition EventarcPipeline#schema_definition}
        '''
        result = self._values.get("schema_definition")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcPipelineDestinationsOutputPayloadFormatProtobuf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcPipelineDestinationsOutputPayloadFormatProtobufOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineDestinationsOutputPayloadFormatProtobufOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01b545716c18b1f99c734b7edb73cb5d397b2198468c77a202e925c57488e4db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSchemaDefinition")
    def reset_schema_definition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaDefinition", []))

    @builtins.property
    @jsii.member(jsii_name="schemaDefinitionInput")
    def schema_definition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaDefinition")
    def schema_definition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaDefinition"))

    @schema_definition.setter
    def schema_definition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5e45a43039904fafe37c3ae70332ed1c2db6ea245356a1206d45610c6de22c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaDefinition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventarcPipelineDestinationsOutputPayloadFormatProtobuf]:
        return typing.cast(typing.Optional[EventarcPipelineDestinationsOutputPayloadFormatProtobuf], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcPipelineDestinationsOutputPayloadFormatProtobuf],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae131f8cd93c8b486ede61065cc669c17d66ee9785318090ab093c560e86a36c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventarcPipelineDestinationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineDestinationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__616f30087972ea3a30090766ccc633166cc002ec422de1fab01ff85cd164d101)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAuthenticationConfig")
    def put_authentication_config(
        self,
        *,
        google_oidc: typing.Optional[typing.Union[EventarcPipelineDestinationsAuthenticationConfigGoogleOidc, typing.Dict[builtins.str, typing.Any]]] = None,
        oauth_token: typing.Optional[typing.Union[EventarcPipelineDestinationsAuthenticationConfigOauthToken, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param google_oidc: google_oidc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#google_oidc EventarcPipeline#google_oidc}
        :param oauth_token: oauth_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#oauth_token EventarcPipeline#oauth_token}
        '''
        value = EventarcPipelineDestinationsAuthenticationConfig(
            google_oidc=google_oidc, oauth_token=oauth_token
        )

        return typing.cast(None, jsii.invoke(self, "putAuthenticationConfig", [value]))

    @jsii.member(jsii_name="putHttpEndpoint")
    def put_http_endpoint(
        self,
        *,
        uri: builtins.str,
        message_binding_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: The URI of the HTTP enpdoint. The value must be a RFC2396 URI string. Examples: 'https://svc.us-central1.p.local:8080/route'. Only the HTTPS protocol is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#uri EventarcPipeline#uri}
        :param message_binding_template: The CEL expression used to modify how the destination-bound HTTP request is constructed. If a binding expression is not specified here, the message is treated as a CloudEvent and is mapped to the HTTP request according to the CloudEvent HTTP Protocol Binding Binary Content Mode (https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/http-protocol-binding.md#31-binary-content-mode). In this representation, all fields except the 'data' and 'datacontenttype' field on the message are mapped to HTTP request headers with a prefix of 'ce-'. To construct the HTTP request payload and the value of the content-type HTTP header, the payload format is defined as follows: 1. Use the output_payload_format_type on the Pipeline.Destination if it is set, else: 2. Use the input_payload_format_type on the Pipeline if it is set, else: 3. Treat the payload as opaque binary data. The 'data' field of the message is converted to the payload format or left as-is for case 3) and then attached as the payload of the HTTP request. The 'content-type' header on the HTTP request is set to the payload format type or left empty for case 3). However, if a mediation has updated the 'datacontenttype' field on the message so that it is not the same as the payload format type but it is still a prefix of the payload format type, then the 'content-type' header on the HTTP request is set to this 'datacontenttype' value. For example, if the 'datacontenttype' is "application/json" and the payload format type is "application/json; charset=utf-8", then the 'content-type' header on the HTTP request is set to "application/json; charset=utf-8". If a non-empty binding expression is specified then this expression is used to modify the default CloudEvent HTTP Protocol Binding Binary Content representation. The result of the CEL expression must be a map of key/value pairs which is used as follows: - If a map named 'headers' exists on the result of the expression, then its key/value pairs are directly mapped to the HTTP request headers. The headers values are constructed from the corresponding value type's canonical representation. If the 'headers' field doesn't exist then the resulting HTTP request will be the headers of the CloudEvent HTTP Binding Binary Content Mode representation of the final message. Note: If the specified binding expression, has updated the 'datacontenttype' field on the message so that it is not the same as the payload format type but it is still a prefix of the payload format type, then the 'content-type' header in the 'headers' map is set to this 'datacontenttype' value. - If a field named 'body' exists on the result of the expression then its value is directly mapped to the body of the request. If the value of the 'body' field is of type bytes or string then it is used for the HTTP request body as-is, with no conversion. If the body field is of any other type then it is converted to a JSON string. If the body field does not exist then the resulting payload of the HTTP request will be data value of the CloudEvent HTTP Binding Binary Content Mode representation of the final message as described earlier. - Any other fields in the resulting expression will be ignored. The CEL expression may access the incoming CloudEvent message in its definition, as follows: - The 'data' field of the incoming CloudEvent message can be accessed using the 'message.data' value. Subfields of 'message.data' may also be accessed if an input_payload_format has been specified on the Pipeline. - Each attribute of the incoming CloudEvent message can be accessed using the 'message.' value, where is replaced with the name of the attribute. - Existing headers can be accessed in the CEL expression using the 'headers' variable. The 'headers' variable defines a map of key/value pairs corresponding to the HTTP headers of the CloudEvent HTTP Binding Binary Content Mode representation of the final message as described earlier. For example, the following CEL expression can be used to construct an HTTP request by adding an additional header to the HTTP headers of the CloudEvent HTTP Binding Binary Content Mode representation of the final message and by overwriting the body of the request: Example:: { "headers": headers.merge({"new-header-key": "new-header-value"}), "body": "new-body" } - The default binding for the message payload can be accessed using the 'body' variable. It conatins a string representation of the message payload in the format specified by the 'output_payload_format' field. If the 'input_payload_format' field is not set, the 'body' variable contains the same message payload bytes that were published. Additionally, the following CEL extension functions are provided for use in this CEL expression: - toBase64Url: map.toBase64Url() -> string - Converts a CelValue to a base64url encoded string - toJsonString: map.toJsonString() -> string - Converts a CelValue to a JSON string - merge: map1.merge(map2) -> map3 - Merges the passed CEL map with the existing CEL map the function is applied to. - If the same key exists in both maps, if the key's value is type map both maps are merged else the value from the passed map is used. - denormalize: map.denormalize() -> map - Denormalizes a CEL map such that every value of type map or key in the map is expanded to return a single level map. - The resulting keys are "." separated indices of the map keys. - For example: { "a": 1, "b": { "c": 2, "d": 3 } "e": [4, 5] } .denormalize() -> { "a": 1, "b.c": 2, "b.d": 3, "e.0": 4, "e.1": 5 } - setField: map.setField(key, value) -> message - Sets the field of the message with the given key to the given value. - If the field is not present it will be added. - If the field is present it will be overwritten. - The key can be a dot separated path to set a field in a nested message. - Key must be of type string. - Value may be any valid type. - removeFields: map.removeFields([key1, key2, ...]) -> message - Removes the fields of the map with the given keys. - The keys can be a dot separated path to remove a field in a nested message. - If a key is not found it will be ignored. - Keys must be of type string. - toMap: [map1, map2, ...].toMap() -> map - Converts a CEL list of CEL maps to a single CEL map - toCloudEventJsonWithPayloadFormat: message.toCloudEventJsonWithPayloadFormat() -> map - Converts a message to the corresponding structure of JSON format for CloudEvents. - It converts 'data' to destination payload format specified in 'output_payload_format'. If 'output_payload_format' is not set, the data will remain unchanged. - It also sets the corresponding datacontenttype of the CloudEvent, as indicated by 'output_payload_format'. If no 'output_payload_format' is set it will use the value of the "datacontenttype" attribute on the CloudEvent if present, else remove "datacontenttype" attribute. - This function expects that the content of the message will adhere to the standard CloudEvent format. If it doesn't then this function will fail. - The result is a CEL map that corresponds to the JSON representation of the CloudEvent. To convert that data to a JSON string it can be chained with the toJsonString function. The Pipeline expects that the message it receives adheres to the standard CloudEvent format. If it doesn't then the outgoing message request may fail with a persistent error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#message_binding_template EventarcPipeline#message_binding_template}
        '''
        value = EventarcPipelineDestinationsHttpEndpoint(
            uri=uri, message_binding_template=message_binding_template
        )

        return typing.cast(None, jsii.invoke(self, "putHttpEndpoint", [value]))

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(
        self,
        *,
        network_attachment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param network_attachment: Name of the NetworkAttachment that allows access to the consumer VPC. Format: 'projects/{PROJECT_ID}/regions/{REGION}/networkAttachments/{NETWORK_ATTACHMENT_NAME}' Required for HTTP endpoint destinations. Must not be specified for Workflows, MessageBus, or Topic destinations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#network_attachment EventarcPipeline#network_attachment}
        '''
        value = EventarcPipelineDestinationsNetworkConfig(
            network_attachment=network_attachment
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfig", [value]))

    @jsii.member(jsii_name="putOutputPayloadFormat")
    def put_output_payload_format(
        self,
        *,
        avro: typing.Optional[typing.Union[EventarcPipelineDestinationsOutputPayloadFormatAvro, typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union[EventarcPipelineDestinationsOutputPayloadFormatJson, typing.Dict[builtins.str, typing.Any]]] = None,
        protobuf: typing.Optional[typing.Union[EventarcPipelineDestinationsOutputPayloadFormatProtobuf, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param avro: avro block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#avro EventarcPipeline#avro}
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#json EventarcPipeline#json}
        :param protobuf: protobuf block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#protobuf EventarcPipeline#protobuf}
        '''
        value = EventarcPipelineDestinationsOutputPayloadFormat(
            avro=avro, json=json, protobuf=protobuf
        )

        return typing.cast(None, jsii.invoke(self, "putOutputPayloadFormat", [value]))

    @jsii.member(jsii_name="resetAuthenticationConfig")
    def reset_authentication_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationConfig", []))

    @jsii.member(jsii_name="resetHttpEndpoint")
    def reset_http_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpEndpoint", []))

    @jsii.member(jsii_name="resetMessageBus")
    def reset_message_bus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageBus", []))

    @jsii.member(jsii_name="resetNetworkConfig")
    def reset_network_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConfig", []))

    @jsii.member(jsii_name="resetOutputPayloadFormat")
    def reset_output_payload_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputPayloadFormat", []))

    @jsii.member(jsii_name="resetTopic")
    def reset_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopic", []))

    @jsii.member(jsii_name="resetWorkflow")
    def reset_workflow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkflow", []))

    @builtins.property
    @jsii.member(jsii_name="authenticationConfig")
    def authentication_config(
        self,
    ) -> EventarcPipelineDestinationsAuthenticationConfigOutputReference:
        return typing.cast(EventarcPipelineDestinationsAuthenticationConfigOutputReference, jsii.get(self, "authenticationConfig"))

    @builtins.property
    @jsii.member(jsii_name="httpEndpoint")
    def http_endpoint(self) -> EventarcPipelineDestinationsHttpEndpointOutputReference:
        return typing.cast(EventarcPipelineDestinationsHttpEndpointOutputReference, jsii.get(self, "httpEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(
        self,
    ) -> EventarcPipelineDestinationsNetworkConfigOutputReference:
        return typing.cast(EventarcPipelineDestinationsNetworkConfigOutputReference, jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="outputPayloadFormat")
    def output_payload_format(
        self,
    ) -> EventarcPipelineDestinationsOutputPayloadFormatOutputReference:
        return typing.cast(EventarcPipelineDestinationsOutputPayloadFormatOutputReference, jsii.get(self, "outputPayloadFormat"))

    @builtins.property
    @jsii.member(jsii_name="authenticationConfigInput")
    def authentication_config_input(
        self,
    ) -> typing.Optional[EventarcPipelineDestinationsAuthenticationConfig]:
        return typing.cast(typing.Optional[EventarcPipelineDestinationsAuthenticationConfig], jsii.get(self, "authenticationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="httpEndpointInput")
    def http_endpoint_input(
        self,
    ) -> typing.Optional[EventarcPipelineDestinationsHttpEndpoint]:
        return typing.cast(typing.Optional[EventarcPipelineDestinationsHttpEndpoint], jsii.get(self, "httpEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="messageBusInput")
    def message_bus_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageBusInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(
        self,
    ) -> typing.Optional[EventarcPipelineDestinationsNetworkConfig]:
        return typing.cast(typing.Optional[EventarcPipelineDestinationsNetworkConfig], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="outputPayloadFormatInput")
    def output_payload_format_input(
        self,
    ) -> typing.Optional[EventarcPipelineDestinationsOutputPayloadFormat]:
        return typing.cast(typing.Optional[EventarcPipelineDestinationsOutputPayloadFormat], jsii.get(self, "outputPayloadFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="workflowInput")
    def workflow_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workflowInput"))

    @builtins.property
    @jsii.member(jsii_name="messageBus")
    def message_bus(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageBus"))

    @message_bus.setter
    def message_bus(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db64951de8b296d465bda55fdfbacf7bfed2fea2973d0d644eac4122aa4d3ac9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageBus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__872974d01064dcdca1b249fb470193b926dcdf8019a26f794a96aa2d1f4e89d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workflow")
    def workflow(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workflow"))

    @workflow.setter
    def workflow(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__867e6e335a439d2b1eb9f8dc72074bd80ac7018ec80601580a98a5f53c601c21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workflow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventarcPipelineDestinations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventarcPipelineDestinations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventarcPipelineDestinations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d814f1487999879d477d565a52b1df29cc910e5e3f0e6b1761d0685bc4885d26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineInputPayloadFormat",
    jsii_struct_bases=[],
    name_mapping={"avro": "avro", "json": "json", "protobuf": "protobuf"},
)
class EventarcPipelineInputPayloadFormat:
    def __init__(
        self,
        *,
        avro: typing.Optional[typing.Union["EventarcPipelineInputPayloadFormatAvro", typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union["EventarcPipelineInputPayloadFormatJson", typing.Dict[builtins.str, typing.Any]]] = None,
        protobuf: typing.Optional[typing.Union["EventarcPipelineInputPayloadFormatProtobuf", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param avro: avro block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#avro EventarcPipeline#avro}
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#json EventarcPipeline#json}
        :param protobuf: protobuf block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#protobuf EventarcPipeline#protobuf}
        '''
        if isinstance(avro, dict):
            avro = EventarcPipelineInputPayloadFormatAvro(**avro)
        if isinstance(json, dict):
            json = EventarcPipelineInputPayloadFormatJson(**json)
        if isinstance(protobuf, dict):
            protobuf = EventarcPipelineInputPayloadFormatProtobuf(**protobuf)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f77e16ddabb73973e14d1d12d7e774dc9cad9a3f3b16247c24399fd7ed7843e0)
            check_type(argname="argument avro", value=avro, expected_type=type_hints["avro"])
            check_type(argname="argument json", value=json, expected_type=type_hints["json"])
            check_type(argname="argument protobuf", value=protobuf, expected_type=type_hints["protobuf"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if avro is not None:
            self._values["avro"] = avro
        if json is not None:
            self._values["json"] = json
        if protobuf is not None:
            self._values["protobuf"] = protobuf

    @builtins.property
    def avro(self) -> typing.Optional["EventarcPipelineInputPayloadFormatAvro"]:
        '''avro block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#avro EventarcPipeline#avro}
        '''
        result = self._values.get("avro")
        return typing.cast(typing.Optional["EventarcPipelineInputPayloadFormatAvro"], result)

    @builtins.property
    def json(self) -> typing.Optional["EventarcPipelineInputPayloadFormatJson"]:
        '''json block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#json EventarcPipeline#json}
        '''
        result = self._values.get("json")
        return typing.cast(typing.Optional["EventarcPipelineInputPayloadFormatJson"], result)

    @builtins.property
    def protobuf(self) -> typing.Optional["EventarcPipelineInputPayloadFormatProtobuf"]:
        '''protobuf block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#protobuf EventarcPipeline#protobuf}
        '''
        result = self._values.get("protobuf")
        return typing.cast(typing.Optional["EventarcPipelineInputPayloadFormatProtobuf"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcPipelineInputPayloadFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineInputPayloadFormatAvro",
    jsii_struct_bases=[],
    name_mapping={"schema_definition": "schemaDefinition"},
)
class EventarcPipelineInputPayloadFormatAvro:
    def __init__(
        self,
        *,
        schema_definition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema_definition: The entire schema definition is stored in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#schema_definition EventarcPipeline#schema_definition}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a41a6b4463daba7c8b56fff9c2c36238551ea57b96ae3b95f791090513ba3314)
            check_type(argname="argument schema_definition", value=schema_definition, expected_type=type_hints["schema_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if schema_definition is not None:
            self._values["schema_definition"] = schema_definition

    @builtins.property
    def schema_definition(self) -> typing.Optional[builtins.str]:
        '''The entire schema definition is stored in this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#schema_definition EventarcPipeline#schema_definition}
        '''
        result = self._values.get("schema_definition")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcPipelineInputPayloadFormatAvro(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcPipelineInputPayloadFormatAvroOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineInputPayloadFormatAvroOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__035c0b73f0d966bae71c27386596368d5e52ee38cc028bfe24f65e741c9bfc11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSchemaDefinition")
    def reset_schema_definition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaDefinition", []))

    @builtins.property
    @jsii.member(jsii_name="schemaDefinitionInput")
    def schema_definition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaDefinition")
    def schema_definition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaDefinition"))

    @schema_definition.setter
    def schema_definition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35f734e785f4e11a901324ce86b4e5f168dddf3bbd6aafe163f8cc4f991d7444)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaDefinition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EventarcPipelineInputPayloadFormatAvro]:
        return typing.cast(typing.Optional[EventarcPipelineInputPayloadFormatAvro], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcPipelineInputPayloadFormatAvro],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f45c109abd418aec3b559461d1be317c48ce382c095468b35bc3fbf77973d641)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineInputPayloadFormatJson",
    jsii_struct_bases=[],
    name_mapping={},
)
class EventarcPipelineInputPayloadFormatJson:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcPipelineInputPayloadFormatJson(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcPipelineInputPayloadFormatJsonOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineInputPayloadFormatJsonOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__135867b919c832ce6f07271e06046a878fcc08962ac4212d04b691daf3d4a86a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EventarcPipelineInputPayloadFormatJson]:
        return typing.cast(typing.Optional[EventarcPipelineInputPayloadFormatJson], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcPipelineInputPayloadFormatJson],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24b05bbe3bcf21493b85c12425012c073e14e7d68e2f81063caf364c2a1461b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventarcPipelineInputPayloadFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineInputPayloadFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1136e5baea62c5b9ebe378fda1b84675438424ae7bc56cd0e3a53cbe87659c45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAvro")
    def put_avro(
        self,
        *,
        schema_definition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema_definition: The entire schema definition is stored in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#schema_definition EventarcPipeline#schema_definition}
        '''
        value = EventarcPipelineInputPayloadFormatAvro(
            schema_definition=schema_definition
        )

        return typing.cast(None, jsii.invoke(self, "putAvro", [value]))

    @jsii.member(jsii_name="putJson")
    def put_json(self) -> None:
        value = EventarcPipelineInputPayloadFormatJson()

        return typing.cast(None, jsii.invoke(self, "putJson", [value]))

    @jsii.member(jsii_name="putProtobuf")
    def put_protobuf(
        self,
        *,
        schema_definition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema_definition: The entire schema definition is stored in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#schema_definition EventarcPipeline#schema_definition}
        '''
        value = EventarcPipelineInputPayloadFormatProtobuf(
            schema_definition=schema_definition
        )

        return typing.cast(None, jsii.invoke(self, "putProtobuf", [value]))

    @jsii.member(jsii_name="resetAvro")
    def reset_avro(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvro", []))

    @jsii.member(jsii_name="resetJson")
    def reset_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJson", []))

    @jsii.member(jsii_name="resetProtobuf")
    def reset_protobuf(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtobuf", []))

    @builtins.property
    @jsii.member(jsii_name="avro")
    def avro(self) -> EventarcPipelineInputPayloadFormatAvroOutputReference:
        return typing.cast(EventarcPipelineInputPayloadFormatAvroOutputReference, jsii.get(self, "avro"))

    @builtins.property
    @jsii.member(jsii_name="json")
    def json(self) -> EventarcPipelineInputPayloadFormatJsonOutputReference:
        return typing.cast(EventarcPipelineInputPayloadFormatJsonOutputReference, jsii.get(self, "json"))

    @builtins.property
    @jsii.member(jsii_name="protobuf")
    def protobuf(self) -> "EventarcPipelineInputPayloadFormatProtobufOutputReference":
        return typing.cast("EventarcPipelineInputPayloadFormatProtobufOutputReference", jsii.get(self, "protobuf"))

    @builtins.property
    @jsii.member(jsii_name="avroInput")
    def avro_input(self) -> typing.Optional[EventarcPipelineInputPayloadFormatAvro]:
        return typing.cast(typing.Optional[EventarcPipelineInputPayloadFormatAvro], jsii.get(self, "avroInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonInput")
    def json_input(self) -> typing.Optional[EventarcPipelineInputPayloadFormatJson]:
        return typing.cast(typing.Optional[EventarcPipelineInputPayloadFormatJson], jsii.get(self, "jsonInput"))

    @builtins.property
    @jsii.member(jsii_name="protobufInput")
    def protobuf_input(
        self,
    ) -> typing.Optional["EventarcPipelineInputPayloadFormatProtobuf"]:
        return typing.cast(typing.Optional["EventarcPipelineInputPayloadFormatProtobuf"], jsii.get(self, "protobufInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EventarcPipelineInputPayloadFormat]:
        return typing.cast(typing.Optional[EventarcPipelineInputPayloadFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcPipelineInputPayloadFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e46fd262844875c1f57d6918ec33c1a0bba3fe92ff9ed363de468b96f904622)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineInputPayloadFormatProtobuf",
    jsii_struct_bases=[],
    name_mapping={"schema_definition": "schemaDefinition"},
)
class EventarcPipelineInputPayloadFormatProtobuf:
    def __init__(
        self,
        *,
        schema_definition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema_definition: The entire schema definition is stored in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#schema_definition EventarcPipeline#schema_definition}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1ab18bcb40e2b4708942cf53269957fa68dff2b2ad3084156940171638171ce)
            check_type(argname="argument schema_definition", value=schema_definition, expected_type=type_hints["schema_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if schema_definition is not None:
            self._values["schema_definition"] = schema_definition

    @builtins.property
    def schema_definition(self) -> typing.Optional[builtins.str]:
        '''The entire schema definition is stored in this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#schema_definition EventarcPipeline#schema_definition}
        '''
        result = self._values.get("schema_definition")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcPipelineInputPayloadFormatProtobuf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcPipelineInputPayloadFormatProtobufOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineInputPayloadFormatProtobufOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b6896de7cc00de74d7fb728cd9a6a1c5071f75c78ca6d1c0bd151c863663b3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSchemaDefinition")
    def reset_schema_definition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaDefinition", []))

    @builtins.property
    @jsii.member(jsii_name="schemaDefinitionInput")
    def schema_definition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaDefinition")
    def schema_definition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaDefinition"))

    @schema_definition.setter
    def schema_definition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a3d4bc1029026956daa5f87532a3536fd3322f20663589d0d4a7e81213c374d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaDefinition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventarcPipelineInputPayloadFormatProtobuf]:
        return typing.cast(typing.Optional[EventarcPipelineInputPayloadFormatProtobuf], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcPipelineInputPayloadFormatProtobuf],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee29d4c3c32e1f8a0d7d47c3d989c623e0a248b02110169447fc6515389cfa36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"log_severity": "logSeverity"},
)
class EventarcPipelineLoggingConfig:
    def __init__(self, *, log_severity: typing.Optional[builtins.str] = None) -> None:
        '''
        :param log_severity: The minimum severity of logs that will be sent to Stackdriver/Platform Telemetry. Logs at severitiy ≥ this value will be sent, unless it is NONE. Possible values: ["NONE", "DEBUG", "INFO", "NOTICE", "WARNING", "ERROR", "CRITICAL", "ALERT", "EMERGENCY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#log_severity EventarcPipeline#log_severity}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5bf5bea8d5035dc513c70a217349602982fff603df2acfbb8e32d85ccef788c)
            check_type(argname="argument log_severity", value=log_severity, expected_type=type_hints["log_severity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_severity is not None:
            self._values["log_severity"] = log_severity

    @builtins.property
    def log_severity(self) -> typing.Optional[builtins.str]:
        '''The minimum severity of logs that will be sent to Stackdriver/Platform Telemetry.

        Logs at severitiy ≥ this value will be sent, unless it is NONE. Possible values: ["NONE", "DEBUG", "INFO", "NOTICE", "WARNING", "ERROR", "CRITICAL", "ALERT", "EMERGENCY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#log_severity EventarcPipeline#log_severity}
        '''
        result = self._values.get("log_severity")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcPipelineLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcPipelineLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ba75fb35c33e65f454b6d8e2c3a3efdd50c3bab7eb34cd3051768c5d8d9e47a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLogSeverity")
    def reset_log_severity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogSeverity", []))

    @builtins.property
    @jsii.member(jsii_name="logSeverityInput")
    def log_severity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logSeverityInput"))

    @builtins.property
    @jsii.member(jsii_name="logSeverity")
    def log_severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logSeverity"))

    @log_severity.setter
    def log_severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1245d4150de355812e1e9a4bb2e6c0f27ca0eccd35cf7abc1dc63a09b8aa8299)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logSeverity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EventarcPipelineLoggingConfig]:
        return typing.cast(typing.Optional[EventarcPipelineLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcPipelineLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41c013a9f07b1dbb645abd1a588b7b8cb4274c580d2ffd404ab5c8fd1ba64878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineMediations",
    jsii_struct_bases=[],
    name_mapping={"transformation": "transformation"},
)
class EventarcPipelineMediations:
    def __init__(
        self,
        *,
        transformation: typing.Optional[typing.Union["EventarcPipelineMediationsTransformation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param transformation: transformation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#transformation EventarcPipeline#transformation}
        '''
        if isinstance(transformation, dict):
            transformation = EventarcPipelineMediationsTransformation(**transformation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13e74448df7da12596a7b5c48f46fa42faac30943e619d96e974e5fa0750811c)
            check_type(argname="argument transformation", value=transformation, expected_type=type_hints["transformation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if transformation is not None:
            self._values["transformation"] = transformation

    @builtins.property
    def transformation(
        self,
    ) -> typing.Optional["EventarcPipelineMediationsTransformation"]:
        '''transformation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#transformation EventarcPipeline#transformation}
        '''
        result = self._values.get("transformation")
        return typing.cast(typing.Optional["EventarcPipelineMediationsTransformation"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcPipelineMediations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcPipelineMediationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineMediationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b743ba8c6e48e8903cc0918b88d70d78da71b4e8636acb422fbd341f96a4d53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EventarcPipelineMediationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f59378972fcb4bf81cec2fbfd99f15633552583da8f4a95ae89e2fd7645f6d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventarcPipelineMediationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__616f26ffc06e09c8a5b178de47509dc4e2404e39f07b24ab1b497f3afc2cacf6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__039f7d09ffeb8b891e51fb6a4c7248bbaf5016c1e076f982667367298bd835bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c419ad7b16bec8650e002ccb1f02646cf5270182f3fd1887cb284ce58724f7d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventarcPipelineMediations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventarcPipelineMediations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventarcPipelineMediations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe627d9a95339a667cc32182c0b00434cc55b3c19ce2b3fa9e0c17605b290236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventarcPipelineMediationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineMediationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__860e69909be7ca4191ce94c54501790621195381d30c51d36989838b61806b50)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTransformation")
    def put_transformation(
        self,
        *,
        transformation_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param transformation_template: The CEL expression template to apply to transform messages. The following CEL extension functions are provided for use in this CEL expression: - merge: map1.merge(map2) -> map3 - Merges the passed CEL map with the existing CEL map the function is applied to. - If the same key exists in both maps, if the key's value is type map both maps are merged else the value from the passed map is used. - denormalize: map.denormalize() -> map - Denormalizes a CEL map such that every value of type map or key in the map is expanded to return a single level map. - The resulting keys are "." separated indices of the map keys. - For example: { "a": 1, "b": { "c": 2, "d": 3 } "e": [4, 5] } .denormalize() -> { "a": 1, "b.c": 2, "b.d": 3, "e.0": 4, "e.1": 5 } - setField: map.setField(key, value) -> message - Sets the field of the message with the given key to the given value. - If the field is not present it will be added. - If the field is present it will be overwritten. - The key can be a dot separated path to set a field in a nested message. - Key must be of type string. - Value may be any valid type. - removeFields: map.removeFields([key1, key2, ...]) -> message - Removes the fields of the map with the given keys. - The keys can be a dot separated path to remove a field in a nested message. - If a key is not found it will be ignored. - Keys must be of type string. - toMap: [map1, map2, ...].toMap() -> map - Converts a CEL list of CEL maps to a single CEL map - toDestinationPayloadFormat(): message.data.toDestinationPayloadFormat() -> string or bytes - Converts the message data to the destination payload format specified in Pipeline.Destination.output_payload_format - This function is meant to be applied to the message.data field. - If the destination payload format is not set, the function will return the message data unchanged. - toCloudEventJsonWithPayloadFormat: message.toCloudEventJsonWithPayloadFormat() -> map - Converts a message to the corresponding structure of JSON format for CloudEvents - This function applies toDestinationPayloadFormat() to the message data. It also sets the corresponding datacontenttype of the CloudEvent, as indicated by Pipeline.Destination.output_payload_format. If no output_payload_format is set it will use the existing datacontenttype on the CloudEvent if present, else leave datacontenttype absent. - This function expects that the content of the message will adhere to the standard CloudEvent format. If it doesn't then this function will fail. - The result is a CEL map that corresponds to the JSON representation of the CloudEvent. To convert that data to a JSON string it can be chained with the toJsonString function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#transformation_template EventarcPipeline#transformation_template}
        '''
        value = EventarcPipelineMediationsTransformation(
            transformation_template=transformation_template
        )

        return typing.cast(None, jsii.invoke(self, "putTransformation", [value]))

    @jsii.member(jsii_name="resetTransformation")
    def reset_transformation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransformation", []))

    @builtins.property
    @jsii.member(jsii_name="transformation")
    def transformation(
        self,
    ) -> "EventarcPipelineMediationsTransformationOutputReference":
        return typing.cast("EventarcPipelineMediationsTransformationOutputReference", jsii.get(self, "transformation"))

    @builtins.property
    @jsii.member(jsii_name="transformationInput")
    def transformation_input(
        self,
    ) -> typing.Optional["EventarcPipelineMediationsTransformation"]:
        return typing.cast(typing.Optional["EventarcPipelineMediationsTransformation"], jsii.get(self, "transformationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventarcPipelineMediations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventarcPipelineMediations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventarcPipelineMediations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c9b5ae397d4794232a91d6badb3858eafd94955b1bdfff5b01e7dcab32b44d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineMediationsTransformation",
    jsii_struct_bases=[],
    name_mapping={"transformation_template": "transformationTemplate"},
)
class EventarcPipelineMediationsTransformation:
    def __init__(
        self,
        *,
        transformation_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param transformation_template: The CEL expression template to apply to transform messages. The following CEL extension functions are provided for use in this CEL expression: - merge: map1.merge(map2) -> map3 - Merges the passed CEL map with the existing CEL map the function is applied to. - If the same key exists in both maps, if the key's value is type map both maps are merged else the value from the passed map is used. - denormalize: map.denormalize() -> map - Denormalizes a CEL map such that every value of type map or key in the map is expanded to return a single level map. - The resulting keys are "." separated indices of the map keys. - For example: { "a": 1, "b": { "c": 2, "d": 3 } "e": [4, 5] } .denormalize() -> { "a": 1, "b.c": 2, "b.d": 3, "e.0": 4, "e.1": 5 } - setField: map.setField(key, value) -> message - Sets the field of the message with the given key to the given value. - If the field is not present it will be added. - If the field is present it will be overwritten. - The key can be a dot separated path to set a field in a nested message. - Key must be of type string. - Value may be any valid type. - removeFields: map.removeFields([key1, key2, ...]) -> message - Removes the fields of the map with the given keys. - The keys can be a dot separated path to remove a field in a nested message. - If a key is not found it will be ignored. - Keys must be of type string. - toMap: [map1, map2, ...].toMap() -> map - Converts a CEL list of CEL maps to a single CEL map - toDestinationPayloadFormat(): message.data.toDestinationPayloadFormat() -> string or bytes - Converts the message data to the destination payload format specified in Pipeline.Destination.output_payload_format - This function is meant to be applied to the message.data field. - If the destination payload format is not set, the function will return the message data unchanged. - toCloudEventJsonWithPayloadFormat: message.toCloudEventJsonWithPayloadFormat() -> map - Converts a message to the corresponding structure of JSON format for CloudEvents - This function applies toDestinationPayloadFormat() to the message data. It also sets the corresponding datacontenttype of the CloudEvent, as indicated by Pipeline.Destination.output_payload_format. If no output_payload_format is set it will use the existing datacontenttype on the CloudEvent if present, else leave datacontenttype absent. - This function expects that the content of the message will adhere to the standard CloudEvent format. If it doesn't then this function will fail. - The result is a CEL map that corresponds to the JSON representation of the CloudEvent. To convert that data to a JSON string it can be chained with the toJsonString function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#transformation_template EventarcPipeline#transformation_template}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6497e67cd5f6c378c90685b7c609e2237e812b30f1c9c5c4c1f9dfb39ced7e8)
            check_type(argname="argument transformation_template", value=transformation_template, expected_type=type_hints["transformation_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if transformation_template is not None:
            self._values["transformation_template"] = transformation_template

    @builtins.property
    def transformation_template(self) -> typing.Optional[builtins.str]:
        '''The CEL expression template to apply to transform messages.

        The following CEL extension functions are provided for
        use in this CEL expression:

        - merge:
          map1.merge(map2) -> map3
        - Merges the passed CEL map with the existing CEL map the
          function is applied to.
        - If the same key exists in both maps, if the key's value is type
          map both maps are merged else the value from the passed map is
          used.
        - denormalize:
          map.denormalize() -> map
        - Denormalizes a CEL map such that every value of type map or key
          in the map is expanded to return a single level map.
        - The resulting keys are "." separated indices of the map keys.
        - For example:
          {
          "a": 1,
          "b": {
          "c": 2,
          "d": 3
          }
          "e": [4, 5]
          }
          .denormalize()
          -> {
          "a": 1,
          "b.c": 2,
          "b.d": 3,
          "e.0": 4,
          "e.1": 5
          }
        - setField:
          map.setField(key, value) -> message
        - Sets the field of the message with the given key to the
          given value.
        - If the field is not present it will be added.
        - If the field is present it will be overwritten.
        - The key can be a dot separated path to set a field in a nested
          message.
        - Key must be of type string.
        - Value may be any valid type.
        - removeFields:
          map.removeFields([key1, key2, ...]) -> message
        - Removes the fields of the map with the given keys.
        - The keys can be a dot separated path to remove a field in a
          nested message.
        - If a key is not found it will be ignored.
        - Keys must be of type string.
        - toMap:
          [map1, map2, ...].toMap() -> map
        - Converts a CEL list of CEL maps to a single CEL map
        - toDestinationPayloadFormat():
          message.data.toDestinationPayloadFormat() -> string or bytes
        - Converts the message data to the destination payload format
          specified in Pipeline.Destination.output_payload_format
        - This function is meant to be applied to the message.data field.
        - If the destination payload format is not set, the function will
          return the message data unchanged.
        - toCloudEventJsonWithPayloadFormat:
          message.toCloudEventJsonWithPayloadFormat() -> map
        - Converts a message to the corresponding structure of JSON
          format for CloudEvents
        - This function applies toDestinationPayloadFormat() to the
          message data. It also sets the corresponding datacontenttype of
          the CloudEvent, as indicated by
          Pipeline.Destination.output_payload_format. If no
          output_payload_format is set it will use the existing
          datacontenttype on the CloudEvent if present, else leave
          datacontenttype absent.
        - This function expects that the content of the message will
          adhere to the standard CloudEvent format. If it doesn't then this
          function will fail.
        - The result is a CEL map that corresponds to the JSON
          representation of the CloudEvent. To convert that data to a JSON
          string it can be chained with the toJsonString function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#transformation_template EventarcPipeline#transformation_template}
        '''
        result = self._values.get("transformation_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcPipelineMediationsTransformation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcPipelineMediationsTransformationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineMediationsTransformationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3aa6d1c5d46af02b93bac1e051ca5e00d78a1e396f8901ace30cc7901231dae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTransformationTemplate")
    def reset_transformation_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransformationTemplate", []))

    @builtins.property
    @jsii.member(jsii_name="transformationTemplateInput")
    def transformation_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transformationTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="transformationTemplate")
    def transformation_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transformationTemplate"))

    @transformation_template.setter
    def transformation_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b779c9d0039db7828311aec74c5b2851eb5ffe68c28537c0fed753d902865059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transformationTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventarcPipelineMediationsTransformation]:
        return typing.cast(typing.Optional[EventarcPipelineMediationsTransformation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcPipelineMediationsTransformation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__424d5a008f4534eb4133aac54de80c65f5e44dd4ea75d2cc4a3ae9b686db5d20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineRetryPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "max_attempts": "maxAttempts",
        "max_retry_delay": "maxRetryDelay",
        "min_retry_delay": "minRetryDelay",
    },
)
class EventarcPipelineRetryPolicy:
    def __init__(
        self,
        *,
        max_attempts: typing.Optional[jsii.Number] = None,
        max_retry_delay: typing.Optional[builtins.str] = None,
        min_retry_delay: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_attempts: The maximum number of delivery attempts for any message. The value must be between 1 and 100. The default value for this field is 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#max_attempts EventarcPipeline#max_attempts}
        :param max_retry_delay: The maximum amount of seconds to wait between retry attempts. The value must be between 1 and 600. The default value for this field is 60. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#max_retry_delay EventarcPipeline#max_retry_delay}
        :param min_retry_delay: The minimum amount of seconds to wait between retry attempts. The value must be between 1 and 600. The default value for this field is 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#min_retry_delay EventarcPipeline#min_retry_delay}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5d57dfe990c6752a42f4ec6fc891177595e19017040d93b7299fbfb02369fc)
            check_type(argname="argument max_attempts", value=max_attempts, expected_type=type_hints["max_attempts"])
            check_type(argname="argument max_retry_delay", value=max_retry_delay, expected_type=type_hints["max_retry_delay"])
            check_type(argname="argument min_retry_delay", value=min_retry_delay, expected_type=type_hints["min_retry_delay"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_attempts is not None:
            self._values["max_attempts"] = max_attempts
        if max_retry_delay is not None:
            self._values["max_retry_delay"] = max_retry_delay
        if min_retry_delay is not None:
            self._values["min_retry_delay"] = min_retry_delay

    @builtins.property
    def max_attempts(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of delivery attempts for any message.

        The value must
        be between 1 and 100.
        The default value for this field is 5.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#max_attempts EventarcPipeline#max_attempts}
        '''
        result = self._values.get("max_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retry_delay(self) -> typing.Optional[builtins.str]:
        '''The maximum amount of seconds to wait between retry attempts.

        The value
        must be between 1 and 600.
        The default value for this field is 60.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#max_retry_delay EventarcPipeline#max_retry_delay}
        '''
        result = self._values.get("max_retry_delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_retry_delay(self) -> typing.Optional[builtins.str]:
        '''The minimum amount of seconds to wait between retry attempts.

        The value
        must be between 1 and 600.
        The default value for this field is 5.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#min_retry_delay EventarcPipeline#min_retry_delay}
        '''
        result = self._values.get("min_retry_delay")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcPipelineRetryPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcPipelineRetryPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineRetryPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__380ba86f23b6a18cb72caf40563823a72a7c91cb75c4a28fa4335ad63bad7dba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxAttempts")
    def reset_max_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAttempts", []))

    @jsii.member(jsii_name="resetMaxRetryDelay")
    def reset_max_retry_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRetryDelay", []))

    @jsii.member(jsii_name="resetMinRetryDelay")
    def reset_min_retry_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinRetryDelay", []))

    @builtins.property
    @jsii.member(jsii_name="maxAttemptsInput")
    def max_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetryDelayInput")
    def max_retry_delay_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxRetryDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="minRetryDelayInput")
    def min_retry_delay_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minRetryDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAttempts")
    def max_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAttempts"))

    @max_attempts.setter
    def max_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a69de134603b0b971b1be76bd2af01bb4e8708c75b828f677878d1bea09d9ae2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetryDelay")
    def max_retry_delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxRetryDelay"))

    @max_retry_delay.setter
    def max_retry_delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77dba7446c1da9539b7a8253c20e5198a1aaa965e80199ac2f391b75ab239d63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetryDelay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minRetryDelay")
    def min_retry_delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minRetryDelay"))

    @min_retry_delay.setter
    def min_retry_delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1321af7c371ec7af022ea8f9ca10f982f122b05e1229e8b37880a1cb33b02e48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minRetryDelay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EventarcPipelineRetryPolicy]:
        return typing.cast(typing.Optional[EventarcPipelineRetryPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcPipelineRetryPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f080b1c6f10a8ab4c5f636e27e49489960763f1c6452769549d76c2a352ed3c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class EventarcPipelineTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#create EventarcPipeline#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#delete EventarcPipeline#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#update EventarcPipeline#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb7c3728ddf42e5aafd5dfc7304805e8229765bc56e5c7d34d4efd43db2cef76)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#create EventarcPipeline#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#delete EventarcPipeline#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_pipeline#update EventarcPipeline#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcPipelineTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcPipelineTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcPipeline.EventarcPipelineTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__276fc83c6b9717ae2a6c02b8a8ac81318d72eb69d1b882c51c750b2d52fdce65)
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
            type_hints = typing.get_type_hints(_typecheckingstub__185c6430d327e4e886caae9bbb072fa5212c9d7139bd127b2ac2b9980d5a2e7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5195531f621e01b3cd5dc9e9130120902ad0e523cfb1188c1f78ab813da83b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a17a15273da99fa7c942a771e46139772bf1acda6d668af055cf24ccfca5bab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventarcPipelineTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventarcPipelineTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventarcPipelineTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e3f0d115a89809eb550fb0815650fb20bd6b18d0434fdaa714ff25128b1d187)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "EventarcPipeline",
    "EventarcPipelineConfig",
    "EventarcPipelineDestinations",
    "EventarcPipelineDestinationsAuthenticationConfig",
    "EventarcPipelineDestinationsAuthenticationConfigGoogleOidc",
    "EventarcPipelineDestinationsAuthenticationConfigGoogleOidcOutputReference",
    "EventarcPipelineDestinationsAuthenticationConfigOauthToken",
    "EventarcPipelineDestinationsAuthenticationConfigOauthTokenOutputReference",
    "EventarcPipelineDestinationsAuthenticationConfigOutputReference",
    "EventarcPipelineDestinationsHttpEndpoint",
    "EventarcPipelineDestinationsHttpEndpointOutputReference",
    "EventarcPipelineDestinationsList",
    "EventarcPipelineDestinationsNetworkConfig",
    "EventarcPipelineDestinationsNetworkConfigOutputReference",
    "EventarcPipelineDestinationsOutputPayloadFormat",
    "EventarcPipelineDestinationsOutputPayloadFormatAvro",
    "EventarcPipelineDestinationsOutputPayloadFormatAvroOutputReference",
    "EventarcPipelineDestinationsOutputPayloadFormatJson",
    "EventarcPipelineDestinationsOutputPayloadFormatJsonOutputReference",
    "EventarcPipelineDestinationsOutputPayloadFormatOutputReference",
    "EventarcPipelineDestinationsOutputPayloadFormatProtobuf",
    "EventarcPipelineDestinationsOutputPayloadFormatProtobufOutputReference",
    "EventarcPipelineDestinationsOutputReference",
    "EventarcPipelineInputPayloadFormat",
    "EventarcPipelineInputPayloadFormatAvro",
    "EventarcPipelineInputPayloadFormatAvroOutputReference",
    "EventarcPipelineInputPayloadFormatJson",
    "EventarcPipelineInputPayloadFormatJsonOutputReference",
    "EventarcPipelineInputPayloadFormatOutputReference",
    "EventarcPipelineInputPayloadFormatProtobuf",
    "EventarcPipelineInputPayloadFormatProtobufOutputReference",
    "EventarcPipelineLoggingConfig",
    "EventarcPipelineLoggingConfigOutputReference",
    "EventarcPipelineMediations",
    "EventarcPipelineMediationsList",
    "EventarcPipelineMediationsOutputReference",
    "EventarcPipelineMediationsTransformation",
    "EventarcPipelineMediationsTransformationOutputReference",
    "EventarcPipelineRetryPolicy",
    "EventarcPipelineRetryPolicyOutputReference",
    "EventarcPipelineTimeouts",
    "EventarcPipelineTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f8d06537300aa362197ab5d3cc425367cfe70a11e594ee4df8ba892e8713a370(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    destinations: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventarcPipelineDestinations, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    pipeline_id: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    crypto_key_name: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    input_payload_format: typing.Optional[typing.Union[EventarcPipelineInputPayloadFormat, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    logging_config: typing.Optional[typing.Union[EventarcPipelineLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    mediations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventarcPipelineMediations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    retry_policy: typing.Optional[typing.Union[EventarcPipelineRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[EventarcPipelineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__bbb162719dfdba07c7aeef4367676d169a059dcd07ae800dd86524277f0af42c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a7ebf84798a1e7ab731eb9db751a8eb755abce70fe0994dcf49591def51185(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventarcPipelineDestinations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d63adef02e613b78acd35229e5bccbe5efec63f96759507ff4f2b8e367b8e71(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventarcPipelineMediations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a4abd9a434c50435762a4446d254b4828ca9fc68d9a393f9f467ccad08a447a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38ef5e851ff6da02386c2ee21b51d0a2f3c4e383b99e63b50682fc754efea02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c33cae7b59e6996b8823ae9dde39ebbea64995de98ae7a130fcf76f21d14809(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d05fa5001b5a716a63c5e2c5229cb16d15a1d621dabac722d8690bcb5fabab1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__746d59b6137fbeae2556307b47edd75cb021462dc1d08fbb012bd1fa61a3c30f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a393d8ffc64dcd11cd30d5d7c5ac4fc07325243523033b0886a1a838361376b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f6b4c93ab45794c6794b7cccd8870b34c374377a04630a938704ce87aef8edf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb718f6977ff6af6d57a8a0390f151b1bc179c1c87cd7397abdf8fda089bf8f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2e5aee555a4ebd7b479b830650d537b80814e357987af80370d42bd63b70d6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    destinations: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventarcPipelineDestinations, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    pipeline_id: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    crypto_key_name: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    input_payload_format: typing.Optional[typing.Union[EventarcPipelineInputPayloadFormat, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    logging_config: typing.Optional[typing.Union[EventarcPipelineLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    mediations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventarcPipelineMediations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    retry_policy: typing.Optional[typing.Union[EventarcPipelineRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[EventarcPipelineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__037f1505370397eb42a4153974d80f1195446c17af31a1fd5a061f6ef6e0e668(
    *,
    authentication_config: typing.Optional[typing.Union[EventarcPipelineDestinationsAuthenticationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    http_endpoint: typing.Optional[typing.Union[EventarcPipelineDestinationsHttpEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    message_bus: typing.Optional[builtins.str] = None,
    network_config: typing.Optional[typing.Union[EventarcPipelineDestinationsNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    output_payload_format: typing.Optional[typing.Union[EventarcPipelineDestinationsOutputPayloadFormat, typing.Dict[builtins.str, typing.Any]]] = None,
    topic: typing.Optional[builtins.str] = None,
    workflow: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08ab37c87ddb37bf5f20cb5b746eaab64df99abff43ce87f042bc1e7a0fd4386(
    *,
    google_oidc: typing.Optional[typing.Union[EventarcPipelineDestinationsAuthenticationConfigGoogleOidc, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth_token: typing.Optional[typing.Union[EventarcPipelineDestinationsAuthenticationConfigOauthToken, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056e03a1e53a2b4449c2a6730cc8d3b4dd4dc6985beed68d5af5eda64b0ef15a(
    *,
    service_account: builtins.str,
    audience: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da92feeb0ad357d47ed44c1b8f9e78af61b0ce0df7675d76b8cb5f62d2883ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56760f5d38488686ceb88e108ff398f98158058f283b4c741f3df2304f6cc281(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e3a72e232a08c4731cfc140fe6c9cc9b8614e12c617cb7178bb7176e343548(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__770e46b7155850041be548eab25f7356855886709aaa2c5f2842c3d4314edce2(
    value: typing.Optional[EventarcPipelineDestinationsAuthenticationConfigGoogleOidc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25da3285785d017f1c52033bed3be3178630f16fb472a5efe8d3d64003dc5a19(
    *,
    service_account: builtins.str,
    scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb3e87a41a7a16d7539f525b4016340ef2098962b0cd33987c5db4ad7d7e9bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924c564d1f04c59d6e4a4474fa4cba1c04a979753d377b316398dac9522c647c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc65bdcff4e700cfcec14ba9edccd58fc3076d45c93e4c80eed46f01e289e147(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c342a75edd63bbc8ebd33a0f3c87cd5be317f595c8d5384ec676a3ec1362b11(
    value: typing.Optional[EventarcPipelineDestinationsAuthenticationConfigOauthToken],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e490d61a44c89313a704dabad8d43485dc67a13a4d97820f8e732323e31cf0e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba5e11c4acb3a9df145d5bafc462238281a32dd2980785b3d96b77dbb9e2ddd(
    value: typing.Optional[EventarcPipelineDestinationsAuthenticationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26476e2660200ccb647e2022a6af6b9ff9001ea9b899a90003402498bd922bd4(
    *,
    uri: builtins.str,
    message_binding_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22523c5ea67b07bbd7455749b56a64b1d050a660ae0e53a7999471ed565aaba6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09f8ee8eb0ece6ba75d32335a628f9e9da79658b533e05953c6ebd82d14cd1e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17620aa7f3b83ae2ca9c7d90009d78911dd432fb909dcf01dc2d0e809a949a5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bccf08807ca5049eea2716d1834c46ccc54e293cb55b06d0753917a71482ad73(
    value: typing.Optional[EventarcPipelineDestinationsHttpEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea29ed316f948938858bc2a24ef6786f0b155722dddbafb17f98c677246e2fad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__765701db335dfb14578fdb51aa027729129bed838c3846ee8c00ec2e92d7757b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0152769295f81cb73f330ad1cc5ba8dc040c59225647a723af3e5d8af888a07c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18adc14f454a9b25d963feb97e3ee673b2222ee76dea9bc5d93bcbb5a53c4c1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92724f1ed30f52983bdd5411d84d85402070e5a0e0bc89ce8d8865d43fa48ff4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db433d4bea1a7e2915c503cf58981893101e7aec85894a2697b87adb548750ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventarcPipelineDestinations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56b475af01585579a92c697221dc5dcd8513d5dc93405d41d4448337ef3cf379(
    *,
    network_attachment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78d2dc67a176242d4c1fa5ee312ce71124b645c935a60aebd2da1bd7a1a12991(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b9e75c05b29d985176144d2562faaaf8674fbd36621f6abec58d126c8dbc68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daa9e8317c52ed96e7f21676908cc7a8615fd4e4d42125c4cb64e562d90187e1(
    value: typing.Optional[EventarcPipelineDestinationsNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__684038ae5fea68c5637c497c0809dedb6c49623eda2e9ace351972caa1207a56(
    *,
    avro: typing.Optional[typing.Union[EventarcPipelineDestinationsOutputPayloadFormatAvro, typing.Dict[builtins.str, typing.Any]]] = None,
    json: typing.Optional[typing.Union[EventarcPipelineDestinationsOutputPayloadFormatJson, typing.Dict[builtins.str, typing.Any]]] = None,
    protobuf: typing.Optional[typing.Union[EventarcPipelineDestinationsOutputPayloadFormatProtobuf, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44e03856ae6a53a6b1be9395fb19b85aa0e9e662d72b8d0cf70d1370a2e9c71(
    *,
    schema_definition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5e60f12403894424ebddd6f6e7c2c6ba383d0aece3896fe8e2cabe7a210449(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5c8cc5d1265788ea3027599ddd13392405e1454abf8dc5986e9309cf8839ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9add6a53a764d1bfb8733c468402e50f3ff82eaa0bec9394dfd636287195ed34(
    value: typing.Optional[EventarcPipelineDestinationsOutputPayloadFormatAvro],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d203d964654fa37652ba820d3b23dd82a4a2dff7bb1031271e2419e7a712e460(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee0a369ef5918078ab6736c7cafe79345d73472fdccb4f45fd7aae055fc6e82d(
    value: typing.Optional[EventarcPipelineDestinationsOutputPayloadFormatJson],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3413a76be45efdf24a67366617f778fce2f3fc29afe6a1ac00aeb860efeb7cdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c835753dea67698bb3d4bd18c4c1d267e77e19d2f3288d61c89930c983bb2208(
    value: typing.Optional[EventarcPipelineDestinationsOutputPayloadFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b571410c0ce67ce9377caad6783f51db972da0826559deb6dc6b0cbb03da96c6(
    *,
    schema_definition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01b545716c18b1f99c734b7edb73cb5d397b2198468c77a202e925c57488e4db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e45a43039904fafe37c3ae70332ed1c2db6ea245356a1206d45610c6de22c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae131f8cd93c8b486ede61065cc669c17d66ee9785318090ab093c560e86a36c(
    value: typing.Optional[EventarcPipelineDestinationsOutputPayloadFormatProtobuf],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__616f30087972ea3a30090766ccc633166cc002ec422de1fab01ff85cd164d101(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db64951de8b296d465bda55fdfbacf7bfed2fea2973d0d644eac4122aa4d3ac9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872974d01064dcdca1b249fb470193b926dcdf8019a26f794a96aa2d1f4e89d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__867e6e335a439d2b1eb9f8dc72074bd80ac7018ec80601580a98a5f53c601c21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d814f1487999879d477d565a52b1df29cc910e5e3f0e6b1761d0685bc4885d26(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventarcPipelineDestinations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f77e16ddabb73973e14d1d12d7e774dc9cad9a3f3b16247c24399fd7ed7843e0(
    *,
    avro: typing.Optional[typing.Union[EventarcPipelineInputPayloadFormatAvro, typing.Dict[builtins.str, typing.Any]]] = None,
    json: typing.Optional[typing.Union[EventarcPipelineInputPayloadFormatJson, typing.Dict[builtins.str, typing.Any]]] = None,
    protobuf: typing.Optional[typing.Union[EventarcPipelineInputPayloadFormatProtobuf, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41a6b4463daba7c8b56fff9c2c36238551ea57b96ae3b95f791090513ba3314(
    *,
    schema_definition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035c0b73f0d966bae71c27386596368d5e52ee38cc028bfe24f65e741c9bfc11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35f734e785f4e11a901324ce86b4e5f168dddf3bbd6aafe163f8cc4f991d7444(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f45c109abd418aec3b559461d1be317c48ce382c095468b35bc3fbf77973d641(
    value: typing.Optional[EventarcPipelineInputPayloadFormatAvro],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135867b919c832ce6f07271e06046a878fcc08962ac4212d04b691daf3d4a86a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24b05bbe3bcf21493b85c12425012c073e14e7d68e2f81063caf364c2a1461b7(
    value: typing.Optional[EventarcPipelineInputPayloadFormatJson],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1136e5baea62c5b9ebe378fda1b84675438424ae7bc56cd0e3a53cbe87659c45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e46fd262844875c1f57d6918ec33c1a0bba3fe92ff9ed363de468b96f904622(
    value: typing.Optional[EventarcPipelineInputPayloadFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ab18bcb40e2b4708942cf53269957fa68dff2b2ad3084156940171638171ce(
    *,
    schema_definition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b6896de7cc00de74d7fb728cd9a6a1c5071f75c78ca6d1c0bd151c863663b3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a3d4bc1029026956daa5f87532a3536fd3322f20663589d0d4a7e81213c374d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee29d4c3c32e1f8a0d7d47c3d989c623e0a248b02110169447fc6515389cfa36(
    value: typing.Optional[EventarcPipelineInputPayloadFormatProtobuf],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5bf5bea8d5035dc513c70a217349602982fff603df2acfbb8e32d85ccef788c(
    *,
    log_severity: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ba75fb35c33e65f454b6d8e2c3a3efdd50c3bab7eb34cd3051768c5d8d9e47a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1245d4150de355812e1e9a4bb2e6c0f27ca0eccd35cf7abc1dc63a09b8aa8299(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c013a9f07b1dbb645abd1a588b7b8cb4274c580d2ffd404ab5c8fd1ba64878(
    value: typing.Optional[EventarcPipelineLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e74448df7da12596a7b5c48f46fa42faac30943e619d96e974e5fa0750811c(
    *,
    transformation: typing.Optional[typing.Union[EventarcPipelineMediationsTransformation, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b743ba8c6e48e8903cc0918b88d70d78da71b4e8636acb422fbd341f96a4d53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f59378972fcb4bf81cec2fbfd99f15633552583da8f4a95ae89e2fd7645f6d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__616f26ffc06e09c8a5b178de47509dc4e2404e39f07b24ab1b497f3afc2cacf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__039f7d09ffeb8b891e51fb6a4c7248bbaf5016c1e076f982667367298bd835bd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c419ad7b16bec8650e002ccb1f02646cf5270182f3fd1887cb284ce58724f7d2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe627d9a95339a667cc32182c0b00434cc55b3c19ce2b3fa9e0c17605b290236(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventarcPipelineMediations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860e69909be7ca4191ce94c54501790621195381d30c51d36989838b61806b50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9b5ae397d4794232a91d6badb3858eafd94955b1bdfff5b01e7dcab32b44d1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventarcPipelineMediations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6497e67cd5f6c378c90685b7c609e2237e812b30f1c9c5c4c1f9dfb39ced7e8(
    *,
    transformation_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3aa6d1c5d46af02b93bac1e051ca5e00d78a1e396f8901ace30cc7901231dae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b779c9d0039db7828311aec74c5b2851eb5ffe68c28537c0fed753d902865059(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424d5a008f4534eb4133aac54de80c65f5e44dd4ea75d2cc4a3ae9b686db5d20(
    value: typing.Optional[EventarcPipelineMediationsTransformation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5d57dfe990c6752a42f4ec6fc891177595e19017040d93b7299fbfb02369fc(
    *,
    max_attempts: typing.Optional[jsii.Number] = None,
    max_retry_delay: typing.Optional[builtins.str] = None,
    min_retry_delay: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380ba86f23b6a18cb72caf40563823a72a7c91cb75c4a28fa4335ad63bad7dba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a69de134603b0b971b1be76bd2af01bb4e8708c75b828f677878d1bea09d9ae2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77dba7446c1da9539b7a8253c20e5198a1aaa965e80199ac2f391b75ab239d63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1321af7c371ec7af022ea8f9ca10f982f122b05e1229e8b37880a1cb33b02e48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f080b1c6f10a8ab4c5f636e27e49489960763f1c6452769549d76c2a352ed3c2(
    value: typing.Optional[EventarcPipelineRetryPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb7c3728ddf42e5aafd5dfc7304805e8229765bc56e5c7d34d4efd43db2cef76(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__276fc83c6b9717ae2a6c02b8a8ac81318d72eb69d1b882c51c750b2d52fdce65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__185c6430d327e4e886caae9bbb072fa5212c9d7139bd127b2ac2b9980d5a2e7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5195531f621e01b3cd5dc9e9130120902ad0e523cfb1188c1f78ab813da83b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a17a15273da99fa7c942a771e46139772bf1acda6d668af055cf24ccfca5bab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e3f0d115a89809eb550fb0815650fb20bd6b18d0434fdaa714ff25128b1d187(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventarcPipelineTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
