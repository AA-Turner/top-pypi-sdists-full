r'''
# `google_eventarc_pipeline`

Refer to the Terraform Registry for docs: [`google_eventarc_pipeline`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline).
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


class GoogleEventarcPipeline(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipeline",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline google_eventarc_pipeline}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        destinations: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleEventarcPipelineDestinations", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        pipeline_id: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        crypto_key_name: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        input_payload_format: typing.Optional[typing.Union["GoogleEventarcPipelineInputPayloadFormat", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["GoogleEventarcPipelineLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mediations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleEventarcPipelineMediations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        retry_policy: typing.Optional[typing.Union["GoogleEventarcPipelineRetryPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleEventarcPipelineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline google_eventarc_pipeline} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param destinations: destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#destinations GoogleEventarcPipeline#destinations}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#location GoogleEventarcPipeline#location}
        :param pipeline_id: The user-provided ID to be assigned to the Pipeline. It should match the format '^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#pipeline_id GoogleEventarcPipeline#pipeline_id}
        :param annotations: User-defined annotations. See https://google.aip.dev/128#annotations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#annotations GoogleEventarcPipeline#annotations}
        :param crypto_key_name: Resource name of a KMS crypto key (managed by the user) used to encrypt/decrypt the event data. If not set, an internal Google-owned key will be used to encrypt messages. It must match the pattern "projects/{project}/locations/{location}/keyRings/{keyring}/cryptoKeys/{key}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#crypto_key_name GoogleEventarcPipeline#crypto_key_name}
        :param display_name: Display name of resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#display_name GoogleEventarcPipeline#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#id GoogleEventarcPipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param input_payload_format: input_payload_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#input_payload_format GoogleEventarcPipeline#input_payload_format}
        :param labels: User labels attached to the Pipeline that can be used to group resources. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#labels GoogleEventarcPipeline#labels}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#logging_config GoogleEventarcPipeline#logging_config}
        :param mediations: mediations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#mediations GoogleEventarcPipeline#mediations}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#project GoogleEventarcPipeline#project}.
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#retry_policy GoogleEventarcPipeline#retry_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#timeouts GoogleEventarcPipeline#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0170cf35c3fd6f15b7f4ad31ad9248a593e5bf494eaf19edd6c7169061ac418b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleEventarcPipelineConfig(
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
        '''Generates CDKTF code for importing a GoogleEventarcPipeline resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleEventarcPipeline to import.
        :param import_from_id: The id of the existing GoogleEventarcPipeline that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleEventarcPipeline to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fffaf5fc0268035b1de1874bc3fdd9e6d840041efc30be6e5c9311f67ea0430b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDestinations")
    def put_destinations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleEventarcPipelineDestinations", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33dd76bf254d0544d7c47f363799f44946e43158feb43843aecc74c09ef8c08b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDestinations", [value]))

    @jsii.member(jsii_name="putInputPayloadFormat")
    def put_input_payload_format(
        self,
        *,
        avro: typing.Optional[typing.Union["GoogleEventarcPipelineInputPayloadFormatAvro", typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union["GoogleEventarcPipelineInputPayloadFormatJson", typing.Dict[builtins.str, typing.Any]]] = None,
        protobuf: typing.Optional[typing.Union["GoogleEventarcPipelineInputPayloadFormatProtobuf", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param avro: avro block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#avro GoogleEventarcPipeline#avro}
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#json GoogleEventarcPipeline#json}
        :param protobuf: protobuf block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#protobuf GoogleEventarcPipeline#protobuf}
        '''
        value = GoogleEventarcPipelineInputPayloadFormat(
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
        :param log_severity: The minimum severity of logs that will be sent to Stackdriver/Platform Telemetry. Logs at severitiy ≥ this value will be sent, unless it is NONE. Possible values: ["NONE", "DEBUG", "INFO", "NOTICE", "WARNING", "ERROR", "CRITICAL", "ALERT", "EMERGENCY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#log_severity GoogleEventarcPipeline#log_severity}
        '''
        value = GoogleEventarcPipelineLoggingConfig(log_severity=log_severity)

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

    @jsii.member(jsii_name="putMediations")
    def put_mediations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleEventarcPipelineMediations", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa02a8ae63bdc94acd3e8b742a65b62b49945d48b7da2037a9d752497f7f5b50)
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
        :param max_attempts: The maximum number of delivery attempts for any message. The value must be between 1 and 100. The default value for this field is 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#max_attempts GoogleEventarcPipeline#max_attempts}
        :param max_retry_delay: The maximum amount of seconds to wait between retry attempts. The value must be between 1 and 600. The default value for this field is 60. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#max_retry_delay GoogleEventarcPipeline#max_retry_delay}
        :param min_retry_delay: The minimum amount of seconds to wait between retry attempts. The value must be between 1 and 600. The default value for this field is 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#min_retry_delay GoogleEventarcPipeline#min_retry_delay}
        '''
        value = GoogleEventarcPipelineRetryPolicy(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#create GoogleEventarcPipeline#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#delete GoogleEventarcPipeline#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#update GoogleEventarcPipeline#update}.
        '''
        value = GoogleEventarcPipelineTimeouts(
            create=create, delete=delete, update=update
        )

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
    def destinations(self) -> "GoogleEventarcPipelineDestinationsList":
        return typing.cast("GoogleEventarcPipelineDestinationsList", jsii.get(self, "destinations"))

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
    ) -> "GoogleEventarcPipelineInputPayloadFormatOutputReference":
        return typing.cast("GoogleEventarcPipelineInputPayloadFormatOutputReference", jsii.get(self, "inputPayloadFormat"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(self) -> "GoogleEventarcPipelineLoggingConfigOutputReference":
        return typing.cast("GoogleEventarcPipelineLoggingConfigOutputReference", jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="mediations")
    def mediations(self) -> "GoogleEventarcPipelineMediationsList":
        return typing.cast("GoogleEventarcPipelineMediationsList", jsii.get(self, "mediations"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicy")
    def retry_policy(self) -> "GoogleEventarcPipelineRetryPolicyOutputReference":
        return typing.cast("GoogleEventarcPipelineRetryPolicyOutputReference", jsii.get(self, "retryPolicy"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleEventarcPipelineTimeoutsOutputReference":
        return typing.cast("GoogleEventarcPipelineTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleEventarcPipelineDestinations"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleEventarcPipelineDestinations"]]], jsii.get(self, "destinationsInput"))

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
    ) -> typing.Optional["GoogleEventarcPipelineInputPayloadFormat"]:
        return typing.cast(typing.Optional["GoogleEventarcPipelineInputPayloadFormat"], jsii.get(self, "inputPayloadFormatInput"))

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
    def logging_config_input(
        self,
    ) -> typing.Optional["GoogleEventarcPipelineLoggingConfig"]:
        return typing.cast(typing.Optional["GoogleEventarcPipelineLoggingConfig"], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="mediationsInput")
    def mediations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleEventarcPipelineMediations"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleEventarcPipelineMediations"]]], jsii.get(self, "mediationsInput"))

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
    def retry_policy_input(
        self,
    ) -> typing.Optional["GoogleEventarcPipelineRetryPolicy"]:
        return typing.cast(typing.Optional["GoogleEventarcPipelineRetryPolicy"], jsii.get(self, "retryPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleEventarcPipelineTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleEventarcPipelineTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d10fa95a5a35f009ae1a7fb433a9588f3f29852eba78c04a0bcf83a7c7615f1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cryptoKeyName")
    def crypto_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cryptoKeyName"))

    @crypto_key_name.setter
    def crypto_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db875b8b74b1f5cf7f6c18966b80fea93faab30886a10d9b2ed56f11e7024d8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cryptoKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bce6fc00bcc617204a5ba3dfc5b5cf301239ae7c7ebaf3ca844a105d62c4175)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2988a4aebc2b8c1148b25a5e725a9f071c05640b8084b3a8a55e211cf6e7a246)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b10258beee9a81b58f9bf39a388148e12e20d6e48101cec9a6b3c17e55124521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09581f75a7783631a70af076034a7d45685003e48ff2a52a5904fee5297a59aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pipelineId")
    def pipeline_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pipelineId"))

    @pipeline_id.setter
    def pipeline_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aa7ce49b7059dbaae5c953e529c5d1d238ca2c55910ce285c25efc32cd12941)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pipelineId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abe5d21b0a84b9154c07656ad9b633bed2b5e562a8e36c9bdb682f45d7d0b82b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineConfig",
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
class GoogleEventarcPipelineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        destinations: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleEventarcPipelineDestinations", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        pipeline_id: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        crypto_key_name: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        input_payload_format: typing.Optional[typing.Union["GoogleEventarcPipelineInputPayloadFormat", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["GoogleEventarcPipelineLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mediations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleEventarcPipelineMediations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        retry_policy: typing.Optional[typing.Union["GoogleEventarcPipelineRetryPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleEventarcPipelineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param destinations: destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#destinations GoogleEventarcPipeline#destinations}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#location GoogleEventarcPipeline#location}
        :param pipeline_id: The user-provided ID to be assigned to the Pipeline. It should match the format '^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#pipeline_id GoogleEventarcPipeline#pipeline_id}
        :param annotations: User-defined annotations. See https://google.aip.dev/128#annotations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#annotations GoogleEventarcPipeline#annotations}
        :param crypto_key_name: Resource name of a KMS crypto key (managed by the user) used to encrypt/decrypt the event data. If not set, an internal Google-owned key will be used to encrypt messages. It must match the pattern "projects/{project}/locations/{location}/keyRings/{keyring}/cryptoKeys/{key}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#crypto_key_name GoogleEventarcPipeline#crypto_key_name}
        :param display_name: Display name of resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#display_name GoogleEventarcPipeline#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#id GoogleEventarcPipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param input_payload_format: input_payload_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#input_payload_format GoogleEventarcPipeline#input_payload_format}
        :param labels: User labels attached to the Pipeline that can be used to group resources. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#labels GoogleEventarcPipeline#labels}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#logging_config GoogleEventarcPipeline#logging_config}
        :param mediations: mediations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#mediations GoogleEventarcPipeline#mediations}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#project GoogleEventarcPipeline#project}.
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#retry_policy GoogleEventarcPipeline#retry_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#timeouts GoogleEventarcPipeline#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(input_payload_format, dict):
            input_payload_format = GoogleEventarcPipelineInputPayloadFormat(**input_payload_format)
        if isinstance(logging_config, dict):
            logging_config = GoogleEventarcPipelineLoggingConfig(**logging_config)
        if isinstance(retry_policy, dict):
            retry_policy = GoogleEventarcPipelineRetryPolicy(**retry_policy)
        if isinstance(timeouts, dict):
            timeouts = GoogleEventarcPipelineTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c8aa72507a032bd4cbdb73a2d9853c5da2f9647ebc5f56830cb6076aa2ad57a)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleEventarcPipelineDestinations"]]:
        '''destinations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#destinations GoogleEventarcPipeline#destinations}
        '''
        result = self._values.get("destinations")
        assert result is not None, "Required property 'destinations' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleEventarcPipelineDestinations"]], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#location GoogleEventarcPipeline#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pipeline_id(self) -> builtins.str:
        '''The user-provided ID to be assigned to the Pipeline. It should match the format '^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#pipeline_id GoogleEventarcPipeline#pipeline_id}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#annotations GoogleEventarcPipeline#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def crypto_key_name(self) -> typing.Optional[builtins.str]:
        '''Resource name of a KMS crypto key (managed by the user) used to encrypt/decrypt the event data.

        If not set, an internal Google-owned key
        will be used to encrypt messages. It must match the pattern
        "projects/{project}/locations/{location}/keyRings/{keyring}/cryptoKeys/{key}".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#crypto_key_name GoogleEventarcPipeline#crypto_key_name}
        '''
        result = self._values.get("crypto_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Display name of resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#display_name GoogleEventarcPipeline#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#id GoogleEventarcPipeline#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_payload_format(
        self,
    ) -> typing.Optional["GoogleEventarcPipelineInputPayloadFormat"]:
        '''input_payload_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#input_payload_format GoogleEventarcPipeline#input_payload_format}
        '''
        result = self._values.get("input_payload_format")
        return typing.cast(typing.Optional["GoogleEventarcPipelineInputPayloadFormat"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User labels attached to the Pipeline that can be used to group resources.

        An object containing a list of "key": value pairs. Example: {
        "name": "wrench", "mass": "1.3kg", "count": "3" }.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#labels GoogleEventarcPipeline#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def logging_config(self) -> typing.Optional["GoogleEventarcPipelineLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#logging_config GoogleEventarcPipeline#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["GoogleEventarcPipelineLoggingConfig"], result)

    @builtins.property
    def mediations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleEventarcPipelineMediations"]]]:
        '''mediations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#mediations GoogleEventarcPipeline#mediations}
        '''
        result = self._values.get("mediations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleEventarcPipelineMediations"]]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#project GoogleEventarcPipeline#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retry_policy(self) -> typing.Optional["GoogleEventarcPipelineRetryPolicy"]:
        '''retry_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#retry_policy GoogleEventarcPipeline#retry_policy}
        '''
        result = self._values.get("retry_policy")
        return typing.cast(typing.Optional["GoogleEventarcPipelineRetryPolicy"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleEventarcPipelineTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#timeouts GoogleEventarcPipeline#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleEventarcPipelineTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcPipelineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineDestinations",
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
class GoogleEventarcPipelineDestinations:
    def __init__(
        self,
        *,
        authentication_config: typing.Optional[typing.Union["GoogleEventarcPipelineDestinationsAuthenticationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        http_endpoint: typing.Optional[typing.Union["GoogleEventarcPipelineDestinationsHttpEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        message_bus: typing.Optional[builtins.str] = None,
        network_config: typing.Optional[typing.Union["GoogleEventarcPipelineDestinationsNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        output_payload_format: typing.Optional[typing.Union["GoogleEventarcPipelineDestinationsOutputPayloadFormat", typing.Dict[builtins.str, typing.Any]]] = None,
        topic: typing.Optional[builtins.str] = None,
        workflow: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authentication_config: authentication_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#authentication_config GoogleEventarcPipeline#authentication_config}
        :param http_endpoint: http_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#http_endpoint GoogleEventarcPipeline#http_endpoint}
        :param message_bus: The resource name of the Message Bus to which events should be published. The Message Bus resource should exist in the same project as the Pipeline. Format: 'projects/{project}/locations/{location}/messageBuses/{message_bus}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#message_bus GoogleEventarcPipeline#message_bus}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#network_config GoogleEventarcPipeline#network_config}
        :param output_payload_format: output_payload_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#output_payload_format GoogleEventarcPipeline#output_payload_format}
        :param topic: The resource name of the Pub/Sub topic to which events should be published. Format: 'projects/{project}/locations/{location}/topics/{topic}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#topic GoogleEventarcPipeline#topic}
        :param workflow: The resource name of the Workflow whose Executions are triggered by the events. The Workflow resource should be deployed in the same project as the Pipeline. Format: 'projects/{project}/locations/{location}/workflows/{workflow}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#workflow GoogleEventarcPipeline#workflow}
        '''
        if isinstance(authentication_config, dict):
            authentication_config = GoogleEventarcPipelineDestinationsAuthenticationConfig(**authentication_config)
        if isinstance(http_endpoint, dict):
            http_endpoint = GoogleEventarcPipelineDestinationsHttpEndpoint(**http_endpoint)
        if isinstance(network_config, dict):
            network_config = GoogleEventarcPipelineDestinationsNetworkConfig(**network_config)
        if isinstance(output_payload_format, dict):
            output_payload_format = GoogleEventarcPipelineDestinationsOutputPayloadFormat(**output_payload_format)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfd7623e461cd1d0da8c56519b68f5dd229a326cc476d1cf211828b0f9b77dbb)
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
    ) -> typing.Optional["GoogleEventarcPipelineDestinationsAuthenticationConfig"]:
        '''authentication_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#authentication_config GoogleEventarcPipeline#authentication_config}
        '''
        result = self._values.get("authentication_config")
        return typing.cast(typing.Optional["GoogleEventarcPipelineDestinationsAuthenticationConfig"], result)

    @builtins.property
    def http_endpoint(
        self,
    ) -> typing.Optional["GoogleEventarcPipelineDestinationsHttpEndpoint"]:
        '''http_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#http_endpoint GoogleEventarcPipeline#http_endpoint}
        '''
        result = self._values.get("http_endpoint")
        return typing.cast(typing.Optional["GoogleEventarcPipelineDestinationsHttpEndpoint"], result)

    @builtins.property
    def message_bus(self) -> typing.Optional[builtins.str]:
        '''The resource name of the Message Bus to which events should be published.

        The Message Bus resource should exist in the same project as
        the Pipeline. Format:
        'projects/{project}/locations/{location}/messageBuses/{message_bus}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#message_bus GoogleEventarcPipeline#message_bus}
        '''
        result = self._values.get("message_bus")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_config(
        self,
    ) -> typing.Optional["GoogleEventarcPipelineDestinationsNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#network_config GoogleEventarcPipeline#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["GoogleEventarcPipelineDestinationsNetworkConfig"], result)

    @builtins.property
    def output_payload_format(
        self,
    ) -> typing.Optional["GoogleEventarcPipelineDestinationsOutputPayloadFormat"]:
        '''output_payload_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#output_payload_format GoogleEventarcPipeline#output_payload_format}
        '''
        result = self._values.get("output_payload_format")
        return typing.cast(typing.Optional["GoogleEventarcPipelineDestinationsOutputPayloadFormat"], result)

    @builtins.property
    def topic(self) -> typing.Optional[builtins.str]:
        '''The resource name of the Pub/Sub topic to which events should be published. Format: 'projects/{project}/locations/{location}/topics/{topic}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#topic GoogleEventarcPipeline#topic}
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow(self) -> typing.Optional[builtins.str]:
        '''The resource name of the Workflow whose Executions are triggered by the events.

        The Workflow resource should be deployed in the same
        project as the Pipeline. Format:
        'projects/{project}/locations/{location}/workflows/{workflow}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#workflow GoogleEventarcPipeline#workflow}
        '''
        result = self._values.get("workflow")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcPipelineDestinations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineDestinationsAuthenticationConfig",
    jsii_struct_bases=[],
    name_mapping={"google_oidc": "googleOidc", "oauth_token": "oauthToken"},
)
class GoogleEventarcPipelineDestinationsAuthenticationConfig:
    def __init__(
        self,
        *,
        google_oidc: typing.Optional[typing.Union["GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidc", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth_token: typing.Optional[typing.Union["GoogleEventarcPipelineDestinationsAuthenticationConfigOauthToken", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param google_oidc: google_oidc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#google_oidc GoogleEventarcPipeline#google_oidc}
        :param oauth_token: oauth_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#oauth_token GoogleEventarcPipeline#oauth_token}
        '''
        if isinstance(google_oidc, dict):
            google_oidc = GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidc(**google_oidc)
        if isinstance(oauth_token, dict):
            oauth_token = GoogleEventarcPipelineDestinationsAuthenticationConfigOauthToken(**oauth_token)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3e73f4a41ef4b3d4273ebb719876b828a37a9b24e282362786e43f6a7e256b6)
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
    ) -> typing.Optional["GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidc"]:
        '''google_oidc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#google_oidc GoogleEventarcPipeline#google_oidc}
        '''
        result = self._values.get("google_oidc")
        return typing.cast(typing.Optional["GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidc"], result)

    @builtins.property
    def oauth_token(
        self,
    ) -> typing.Optional["GoogleEventarcPipelineDestinationsAuthenticationConfigOauthToken"]:
        '''oauth_token block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#oauth_token GoogleEventarcPipeline#oauth_token}
        '''
        result = self._values.get("oauth_token")
        return typing.cast(typing.Optional["GoogleEventarcPipelineDestinationsAuthenticationConfigOauthToken"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcPipelineDestinationsAuthenticationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidc",
    jsii_struct_bases=[],
    name_mapping={"service_account": "serviceAccount", "audience": "audience"},
)
class GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidc:
    def __init__(
        self,
        *,
        service_account: builtins.str,
        audience: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account: Service account email used to generate the OIDC Token. The principal who calls this API must have iam.serviceAccounts.actAs permission in the service account. See https://cloud.google.com/iam/docs/understanding-service-accounts for more information. Eventarc service agents must have roles/roles/iam.serviceAccountTokenCreator role to allow the Pipeline to create OpenID tokens for authenticated requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#service_account GoogleEventarcPipeline#service_account}
        :param audience: Audience to be used to generate the OIDC Token. The audience claim identifies the recipient that the JWT is intended for. If unspecified, the destination URI will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#audience GoogleEventarcPipeline#audience}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a67d5f2d8acddf1c837c7d9a8dbd10dee49da07e269b6e9f2ce1d3ad574c1d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#service_account GoogleEventarcPipeline#service_account}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#audience GoogleEventarcPipeline#audience}
        '''
        result = self._values.get("audience")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__633dbcf83fe10b5b7c052b8e7ac15002aaddbfce57a7f2b4cc7be22eff3720b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ef03312c423a7377d2ef1dead7b8dc9d0231bb505f7c644d11e3fc93766857a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audience", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f1c1a87b242ffeb29026b7512b8da149f6e9a6a2bbe049b65a997113159ebee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidc]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa8f4e24185d6ac2ec2b8bd2876f7d0860b1e338f1800242cf9cc75f485f213c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineDestinationsAuthenticationConfigOauthToken",
    jsii_struct_bases=[],
    name_mapping={"service_account": "serviceAccount", "scope": "scope"},
)
class GoogleEventarcPipelineDestinationsAuthenticationConfigOauthToken:
    def __init__(
        self,
        *,
        service_account: builtins.str,
        scope: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account: Service account email used to generate the `OAuth token <https://developers.google.com/identity/protocols/OAuth2>`_. The principal who calls this API must have iam.serviceAccounts.actAs permission in the service account. See https://cloud.google.com/iam/docs/understanding-service-accounts for more information. Eventarc service agents must have roles/roles/iam.serviceAccountTokenCreator role to allow Pipeline to create OAuth2 tokens for authenticated requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#service_account GoogleEventarcPipeline#service_account}
        :param scope: OAuth scope to be used for generating OAuth access token. If not specified, "https://www.googleapis.com/auth/cloud-platform" will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#scope GoogleEventarcPipeline#scope}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25e313e00da416532fb7450bb7b5230a060e816b2be2a8cfcea5242383f44de9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#service_account GoogleEventarcPipeline#service_account}
        '''
        result = self._values.get("service_account")
        assert result is not None, "Required property 'service_account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''OAuth scope to be used for generating OAuth access token. If not specified, "https://www.googleapis.com/auth/cloud-platform" will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#scope GoogleEventarcPipeline#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcPipelineDestinationsAuthenticationConfigOauthToken(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcPipelineDestinationsAuthenticationConfigOauthTokenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineDestinationsAuthenticationConfigOauthTokenOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aeb491c66a9b13385555656eabc411187e7fc54ee6560d6188464c95de589912)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f10540222f014edb4981d5782bc850dc721eb2d270027466c886cbb4da2daf6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ace5ca0f661a7b8a878eeab00b694b6d99d58c41de751f244932bb5ebe07192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineDestinationsAuthenticationConfigOauthToken]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineDestinationsAuthenticationConfigOauthToken], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcPipelineDestinationsAuthenticationConfigOauthToken],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8832986b795d4bdb73dba398d68cc76a56cee14eeb27f33e6a890020a5af5c05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleEventarcPipelineDestinationsAuthenticationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineDestinationsAuthenticationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa25ab87a0bce9863fdfa807197c39f9587df3d8994ee14a3542fd965421a5ef)
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
        :param service_account: Service account email used to generate the OIDC Token. The principal who calls this API must have iam.serviceAccounts.actAs permission in the service account. See https://cloud.google.com/iam/docs/understanding-service-accounts for more information. Eventarc service agents must have roles/roles/iam.serviceAccountTokenCreator role to allow the Pipeline to create OpenID tokens for authenticated requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#service_account GoogleEventarcPipeline#service_account}
        :param audience: Audience to be used to generate the OIDC Token. The audience claim identifies the recipient that the JWT is intended for. If unspecified, the destination URI will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#audience GoogleEventarcPipeline#audience}
        '''
        value = GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidc(
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
        :param service_account: Service account email used to generate the `OAuth token <https://developers.google.com/identity/protocols/OAuth2>`_. The principal who calls this API must have iam.serviceAccounts.actAs permission in the service account. See https://cloud.google.com/iam/docs/understanding-service-accounts for more information. Eventarc service agents must have roles/roles/iam.serviceAccountTokenCreator role to allow Pipeline to create OAuth2 tokens for authenticated requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#service_account GoogleEventarcPipeline#service_account}
        :param scope: OAuth scope to be used for generating OAuth access token. If not specified, "https://www.googleapis.com/auth/cloud-platform" will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#scope GoogleEventarcPipeline#scope}
        '''
        value = GoogleEventarcPipelineDestinationsAuthenticationConfigOauthToken(
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
    ) -> GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidcOutputReference:
        return typing.cast(GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidcOutputReference, jsii.get(self, "googleOidc"))

    @builtins.property
    @jsii.member(jsii_name="oauthToken")
    def oauth_token(
        self,
    ) -> GoogleEventarcPipelineDestinationsAuthenticationConfigOauthTokenOutputReference:
        return typing.cast(GoogleEventarcPipelineDestinationsAuthenticationConfigOauthTokenOutputReference, jsii.get(self, "oauthToken"))

    @builtins.property
    @jsii.member(jsii_name="googleOidcInput")
    def google_oidc_input(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidc]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidc], jsii.get(self, "googleOidcInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthTokenInput")
    def oauth_token_input(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineDestinationsAuthenticationConfigOauthToken]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineDestinationsAuthenticationConfigOauthToken], jsii.get(self, "oauthTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineDestinationsAuthenticationConfig]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineDestinationsAuthenticationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcPipelineDestinationsAuthenticationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2fb43159444fe4284c3621cff4280629451b67b2a9fc1eba94c68be010764c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineDestinationsHttpEndpoint",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "message_binding_template": "messageBindingTemplate"},
)
class GoogleEventarcPipelineDestinationsHttpEndpoint:
    def __init__(
        self,
        *,
        uri: builtins.str,
        message_binding_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: The URI of the HTTP enpdoint. The value must be a RFC2396 URI string. Examples: 'https://svc.us-central1.p.local:8080/route'. Only the HTTPS protocol is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#uri GoogleEventarcPipeline#uri}
        :param message_binding_template: The CEL expression used to modify how the destination-bound HTTP request is constructed. If a binding expression is not specified here, the message is treated as a CloudEvent and is mapped to the HTTP request according to the CloudEvent HTTP Protocol Binding Binary Content Mode (https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/http-protocol-binding.md#31-binary-content-mode). In this representation, all fields except the 'data' and 'datacontenttype' field on the message are mapped to HTTP request headers with a prefix of 'ce-'. To construct the HTTP request payload and the value of the content-type HTTP header, the payload format is defined as follows: 1. Use the output_payload_format_type on the Pipeline.Destination if it is set, else: 2. Use the input_payload_format_type on the Pipeline if it is set, else: 3. Treat the payload as opaque binary data. The 'data' field of the message is converted to the payload format or left as-is for case 3) and then attached as the payload of the HTTP request. The 'content-type' header on the HTTP request is set to the payload format type or left empty for case 3). However, if a mediation has updated the 'datacontenttype' field on the message so that it is not the same as the payload format type but it is still a prefix of the payload format type, then the 'content-type' header on the HTTP request is set to this 'datacontenttype' value. For example, if the 'datacontenttype' is "application/json" and the payload format type is "application/json; charset=utf-8", then the 'content-type' header on the HTTP request is set to "application/json; charset=utf-8". If a non-empty binding expression is specified then this expression is used to modify the default CloudEvent HTTP Protocol Binding Binary Content representation. The result of the CEL expression must be a map of key/value pairs which is used as follows: - If a map named 'headers' exists on the result of the expression, then its key/value pairs are directly mapped to the HTTP request headers. The headers values are constructed from the corresponding value type's canonical representation. If the 'headers' field doesn't exist then the resulting HTTP request will be the headers of the CloudEvent HTTP Binding Binary Content Mode representation of the final message. Note: If the specified binding expression, has updated the 'datacontenttype' field on the message so that it is not the same as the payload format type but it is still a prefix of the payload format type, then the 'content-type' header in the 'headers' map is set to this 'datacontenttype' value. - If a field named 'body' exists on the result of the expression then its value is directly mapped to the body of the request. If the value of the 'body' field is of type bytes or string then it is used for the HTTP request body as-is, with no conversion. If the body field is of any other type then it is converted to a JSON string. If the body field does not exist then the resulting payload of the HTTP request will be data value of the CloudEvent HTTP Binding Binary Content Mode representation of the final message as described earlier. - Any other fields in the resulting expression will be ignored. The CEL expression may access the incoming CloudEvent message in its definition, as follows: - The 'data' field of the incoming CloudEvent message can be accessed using the 'message.data' value. Subfields of 'message.data' may also be accessed if an input_payload_format has been specified on the Pipeline. - Each attribute of the incoming CloudEvent message can be accessed using the 'message.' value, where is replaced with the name of the attribute. - Existing headers can be accessed in the CEL expression using the 'headers' variable. The 'headers' variable defines a map of key/value pairs corresponding to the HTTP headers of the CloudEvent HTTP Binding Binary Content Mode representation of the final message as described earlier. For example, the following CEL expression can be used to construct an HTTP request by adding an additional header to the HTTP headers of the CloudEvent HTTP Binding Binary Content Mode representation of the final message and by overwriting the body of the request: Example:: { "headers": headers.merge({"new-header-key": "new-header-value"}), "body": "new-body" } - The default binding for the message payload can be accessed using the 'body' variable. It conatins a string representation of the message payload in the format specified by the 'output_payload_format' field. If the 'input_payload_format' field is not set, the 'body' variable contains the same message payload bytes that were published. Additionally, the following CEL extension functions are provided for use in this CEL expression: - toBase64Url: map.toBase64Url() -> string - Converts a CelValue to a base64url encoded string - toJsonString: map.toJsonString() -> string - Converts a CelValue to a JSON string - merge: map1.merge(map2) -> map3 - Merges the passed CEL map with the existing CEL map the function is applied to. - If the same key exists in both maps, if the key's value is type map both maps are merged else the value from the passed map is used. - denormalize: map.denormalize() -> map - Denormalizes a CEL map such that every value of type map or key in the map is expanded to return a single level map. - The resulting keys are "." separated indices of the map keys. - For example: { "a": 1, "b": { "c": 2, "d": 3 } "e": [4, 5] } .denormalize() -> { "a": 1, "b.c": 2, "b.d": 3, "e.0": 4, "e.1": 5 } - setField: map.setField(key, value) -> message - Sets the field of the message with the given key to the given value. - If the field is not present it will be added. - If the field is present it will be overwritten. - The key can be a dot separated path to set a field in a nested message. - Key must be of type string. - Value may be any valid type. - removeFields: map.removeFields([key1, key2, ...]) -> message - Removes the fields of the map with the given keys. - The keys can be a dot separated path to remove a field in a nested message. - If a key is not found it will be ignored. - Keys must be of type string. - toMap: [map1, map2, ...].toMap() -> map - Converts a CEL list of CEL maps to a single CEL map - toCloudEventJsonWithPayloadFormat: message.toCloudEventJsonWithPayloadFormat() -> map - Converts a message to the corresponding structure of JSON format for CloudEvents. - It converts 'data' to destination payload format specified in 'output_payload_format'. If 'output_payload_format' is not set, the data will remain unchanged. - It also sets the corresponding datacontenttype of the CloudEvent, as indicated by 'output_payload_format'. If no 'output_payload_format' is set it will use the value of the "datacontenttype" attribute on the CloudEvent if present, else remove "datacontenttype" attribute. - This function expects that the content of the message will adhere to the standard CloudEvent format. If it doesn't then this function will fail. - The result is a CEL map that corresponds to the JSON representation of the CloudEvent. To convert that data to a JSON string it can be chained with the toJsonString function. The Pipeline expects that the message it receives adheres to the standard CloudEvent format. If it doesn't then the outgoing message request may fail with a persistent error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#message_binding_template GoogleEventarcPipeline#message_binding_template}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ddc2d8b5e3db407ef285bbfef441ebc5d2aa764b8eee70729a8ccb65a3bec71)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#uri GoogleEventarcPipeline#uri}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#message_binding_template GoogleEventarcPipeline#message_binding_template}
        '''
        result = self._values.get("message_binding_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcPipelineDestinationsHttpEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcPipelineDestinationsHttpEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineDestinationsHttpEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d06f9e4a5cbccbad53df04a542fbd14d34885f9ab6226965130bde515eacae0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa8ec507572f06bb97a66da0cddcb6fc79e377ec1219cc928f1db80995e647b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageBindingTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2697ee56853faec6477e2297848679f1a37c93a49850d055933c79a67f9ef32b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineDestinationsHttpEndpoint]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineDestinationsHttpEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcPipelineDestinationsHttpEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fe404dd400c2f78217c5c203e79535c8ee6fd8d67b48eb22bc8945e801b39a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleEventarcPipelineDestinationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineDestinationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe2407e9ded56fdada3f159d2c639e5cf19c11113457b71e0066b254dc21f5c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleEventarcPipelineDestinationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__726b05efba788384aba751087a16347dc13ccf2051b08b782ad1059201731b93)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleEventarcPipelineDestinationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e4591ac30e82302831552dfef992b5329cc137725865739a24289236271ab28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a960345bcbd35bf2e1e185f79e51f9aa51d26176b4c25639158228b1a110fa77)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16251d85be6a173945c81ebee6d29649e3c043affed20254f5930a0997a74146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleEventarcPipelineDestinations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleEventarcPipelineDestinations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleEventarcPipelineDestinations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6280b8d6e13de9f52eeb0900e0beec98b9905e57ccae61aafa8d35b57510b34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineDestinationsNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={"network_attachment": "networkAttachment"},
)
class GoogleEventarcPipelineDestinationsNetworkConfig:
    def __init__(
        self,
        *,
        network_attachment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param network_attachment: Name of the NetworkAttachment that allows access to the consumer VPC. Format: 'projects/{PROJECT_ID}/regions/{REGION}/networkAttachments/{NETWORK_ATTACHMENT_NAME}' Required for HTTP endpoint destinations. Must not be specified for Workflows, MessageBus, or Topic destinations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#network_attachment GoogleEventarcPipeline#network_attachment}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e47e9cdf87410e13db4b667f227ebc104fdfb78ce4469749b56c575cca565ba)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#network_attachment GoogleEventarcPipeline#network_attachment}
        '''
        result = self._values.get("network_attachment")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcPipelineDestinationsNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcPipelineDestinationsNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineDestinationsNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c49f6736daf5e4ba62e6f1fc4255dad6d6096b7cbd52a73bbcd5eacca0b7fb3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f9dda5fa0c56dd30c961f0f0e73871c387b45860e356d26af97a7781ef44ff8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkAttachment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineDestinationsNetworkConfig]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineDestinationsNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcPipelineDestinationsNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9419be67acc55336349806a4cff550245bfa9dead1e181e573b2ffc5c1184af7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineDestinationsOutputPayloadFormat",
    jsii_struct_bases=[],
    name_mapping={"avro": "avro", "json": "json", "protobuf": "protobuf"},
)
class GoogleEventarcPipelineDestinationsOutputPayloadFormat:
    def __init__(
        self,
        *,
        avro: typing.Optional[typing.Union["GoogleEventarcPipelineDestinationsOutputPayloadFormatAvro", typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union["GoogleEventarcPipelineDestinationsOutputPayloadFormatJson", typing.Dict[builtins.str, typing.Any]]] = None,
        protobuf: typing.Optional[typing.Union["GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobuf", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param avro: avro block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#avro GoogleEventarcPipeline#avro}
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#json GoogleEventarcPipeline#json}
        :param protobuf: protobuf block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#protobuf GoogleEventarcPipeline#protobuf}
        '''
        if isinstance(avro, dict):
            avro = GoogleEventarcPipelineDestinationsOutputPayloadFormatAvro(**avro)
        if isinstance(json, dict):
            json = GoogleEventarcPipelineDestinationsOutputPayloadFormatJson(**json)
        if isinstance(protobuf, dict):
            protobuf = GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobuf(**protobuf)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2da4fdf4527932fbaadc86956deeca4e1b3906787daab6b3277267e1d0dcdf0)
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
    ) -> typing.Optional["GoogleEventarcPipelineDestinationsOutputPayloadFormatAvro"]:
        '''avro block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#avro GoogleEventarcPipeline#avro}
        '''
        result = self._values.get("avro")
        return typing.cast(typing.Optional["GoogleEventarcPipelineDestinationsOutputPayloadFormatAvro"], result)

    @builtins.property
    def json(
        self,
    ) -> typing.Optional["GoogleEventarcPipelineDestinationsOutputPayloadFormatJson"]:
        '''json block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#json GoogleEventarcPipeline#json}
        '''
        result = self._values.get("json")
        return typing.cast(typing.Optional["GoogleEventarcPipelineDestinationsOutputPayloadFormatJson"], result)

    @builtins.property
    def protobuf(
        self,
    ) -> typing.Optional["GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobuf"]:
        '''protobuf block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#protobuf GoogleEventarcPipeline#protobuf}
        '''
        result = self._values.get("protobuf")
        return typing.cast(typing.Optional["GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobuf"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcPipelineDestinationsOutputPayloadFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineDestinationsOutputPayloadFormatAvro",
    jsii_struct_bases=[],
    name_mapping={"schema_definition": "schemaDefinition"},
)
class GoogleEventarcPipelineDestinationsOutputPayloadFormatAvro:
    def __init__(
        self,
        *,
        schema_definition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema_definition: The entire schema definition is stored in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#schema_definition GoogleEventarcPipeline#schema_definition}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b1950906964b4ed33fc38f37b1738f901a8d4d1793a04e75636b88f00633898)
            check_type(argname="argument schema_definition", value=schema_definition, expected_type=type_hints["schema_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if schema_definition is not None:
            self._values["schema_definition"] = schema_definition

    @builtins.property
    def schema_definition(self) -> typing.Optional[builtins.str]:
        '''The entire schema definition is stored in this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#schema_definition GoogleEventarcPipeline#schema_definition}
        '''
        result = self._values.get("schema_definition")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcPipelineDestinationsOutputPayloadFormatAvro(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcPipelineDestinationsOutputPayloadFormatAvroOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineDestinationsOutputPayloadFormatAvroOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b7850d4ae31d1480b17cc9b831877dd3bd325b3edc0520d4ecd21bc0232a624)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d76ab18a0b0bf63f48c175442faf91bf2faf5853987060541e66674e54a4a3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaDefinition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormatAvro]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormatAvro], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormatAvro],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f0e3e676707a4b52a57cb0c47522240fc3f5027baf73515b305a39557d09458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineDestinationsOutputPayloadFormatJson",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleEventarcPipelineDestinationsOutputPayloadFormatJson:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcPipelineDestinationsOutputPayloadFormatJson(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcPipelineDestinationsOutputPayloadFormatJsonOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineDestinationsOutputPayloadFormatJsonOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37d5aea34c3136fcba8165cdcf666ae83c5ce247afb1f3b8931617055446a169)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormatJson]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormatJson], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormatJson],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f7361489f3fb156f3f1139639397c09f484ac0a249a548bec54c1c2050123bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleEventarcPipelineDestinationsOutputPayloadFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineDestinationsOutputPayloadFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03712595936a708cfac9e9261e712ba53168dc74b743c3c3d7ae3ed21e9476bb)
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
        :param schema_definition: The entire schema definition is stored in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#schema_definition GoogleEventarcPipeline#schema_definition}
        '''
        value = GoogleEventarcPipelineDestinationsOutputPayloadFormatAvro(
            schema_definition=schema_definition
        )

        return typing.cast(None, jsii.invoke(self, "putAvro", [value]))

    @jsii.member(jsii_name="putJson")
    def put_json(self) -> None:
        value = GoogleEventarcPipelineDestinationsOutputPayloadFormatJson()

        return typing.cast(None, jsii.invoke(self, "putJson", [value]))

    @jsii.member(jsii_name="putProtobuf")
    def put_protobuf(
        self,
        *,
        schema_definition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema_definition: The entire schema definition is stored in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#schema_definition GoogleEventarcPipeline#schema_definition}
        '''
        value = GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobuf(
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
    ) -> GoogleEventarcPipelineDestinationsOutputPayloadFormatAvroOutputReference:
        return typing.cast(GoogleEventarcPipelineDestinationsOutputPayloadFormatAvroOutputReference, jsii.get(self, "avro"))

    @builtins.property
    @jsii.member(jsii_name="json")
    def json(
        self,
    ) -> GoogleEventarcPipelineDestinationsOutputPayloadFormatJsonOutputReference:
        return typing.cast(GoogleEventarcPipelineDestinationsOutputPayloadFormatJsonOutputReference, jsii.get(self, "json"))

    @builtins.property
    @jsii.member(jsii_name="protobuf")
    def protobuf(
        self,
    ) -> "GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobufOutputReference":
        return typing.cast("GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobufOutputReference", jsii.get(self, "protobuf"))

    @builtins.property
    @jsii.member(jsii_name="avroInput")
    def avro_input(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormatAvro]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormatAvro], jsii.get(self, "avroInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonInput")
    def json_input(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormatJson]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormatJson], jsii.get(self, "jsonInput"))

    @builtins.property
    @jsii.member(jsii_name="protobufInput")
    def protobuf_input(
        self,
    ) -> typing.Optional["GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobuf"]:
        return typing.cast(typing.Optional["GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobuf"], jsii.get(self, "protobufInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormat]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__148ac2983e4376323b4a4b5fdb9f4723771c34c3ad5fb0c46553b0944c9cf473)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobuf",
    jsii_struct_bases=[],
    name_mapping={"schema_definition": "schemaDefinition"},
)
class GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobuf:
    def __init__(
        self,
        *,
        schema_definition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema_definition: The entire schema definition is stored in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#schema_definition GoogleEventarcPipeline#schema_definition}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de95446886594a3375d7c57c899ef770b3421a8f94f924fba4a14a39ad6b6765)
            check_type(argname="argument schema_definition", value=schema_definition, expected_type=type_hints["schema_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if schema_definition is not None:
            self._values["schema_definition"] = schema_definition

    @builtins.property
    def schema_definition(self) -> typing.Optional[builtins.str]:
        '''The entire schema definition is stored in this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#schema_definition GoogleEventarcPipeline#schema_definition}
        '''
        result = self._values.get("schema_definition")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobuf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobufOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobufOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bb665d614d25ee41b4915acd16e9fa5e2aa3304828329b67ce25950b34a9c71)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91ffd6787d3fec08011711285eb091d33fa0a807d25af0fdc7e0a3d33a9ff242)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaDefinition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobuf]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobuf], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobuf],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3be934e65768a6a7eb66ea6176a0261bcd37938b6ebd4ea070cbb66d389a2413)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleEventarcPipelineDestinationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineDestinationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0dd8d3587a8bb63f1068561de51417b8a7d9db4200d61cb013d210568bc6810)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAuthenticationConfig")
    def put_authentication_config(
        self,
        *,
        google_oidc: typing.Optional[typing.Union[GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidc, typing.Dict[builtins.str, typing.Any]]] = None,
        oauth_token: typing.Optional[typing.Union[GoogleEventarcPipelineDestinationsAuthenticationConfigOauthToken, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param google_oidc: google_oidc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#google_oidc GoogleEventarcPipeline#google_oidc}
        :param oauth_token: oauth_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#oauth_token GoogleEventarcPipeline#oauth_token}
        '''
        value = GoogleEventarcPipelineDestinationsAuthenticationConfig(
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
        :param uri: The URI of the HTTP enpdoint. The value must be a RFC2396 URI string. Examples: 'https://svc.us-central1.p.local:8080/route'. Only the HTTPS protocol is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#uri GoogleEventarcPipeline#uri}
        :param message_binding_template: The CEL expression used to modify how the destination-bound HTTP request is constructed. If a binding expression is not specified here, the message is treated as a CloudEvent and is mapped to the HTTP request according to the CloudEvent HTTP Protocol Binding Binary Content Mode (https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/http-protocol-binding.md#31-binary-content-mode). In this representation, all fields except the 'data' and 'datacontenttype' field on the message are mapped to HTTP request headers with a prefix of 'ce-'. To construct the HTTP request payload and the value of the content-type HTTP header, the payload format is defined as follows: 1. Use the output_payload_format_type on the Pipeline.Destination if it is set, else: 2. Use the input_payload_format_type on the Pipeline if it is set, else: 3. Treat the payload as opaque binary data. The 'data' field of the message is converted to the payload format or left as-is for case 3) and then attached as the payload of the HTTP request. The 'content-type' header on the HTTP request is set to the payload format type or left empty for case 3). However, if a mediation has updated the 'datacontenttype' field on the message so that it is not the same as the payload format type but it is still a prefix of the payload format type, then the 'content-type' header on the HTTP request is set to this 'datacontenttype' value. For example, if the 'datacontenttype' is "application/json" and the payload format type is "application/json; charset=utf-8", then the 'content-type' header on the HTTP request is set to "application/json; charset=utf-8". If a non-empty binding expression is specified then this expression is used to modify the default CloudEvent HTTP Protocol Binding Binary Content representation. The result of the CEL expression must be a map of key/value pairs which is used as follows: - If a map named 'headers' exists on the result of the expression, then its key/value pairs are directly mapped to the HTTP request headers. The headers values are constructed from the corresponding value type's canonical representation. If the 'headers' field doesn't exist then the resulting HTTP request will be the headers of the CloudEvent HTTP Binding Binary Content Mode representation of the final message. Note: If the specified binding expression, has updated the 'datacontenttype' field on the message so that it is not the same as the payload format type but it is still a prefix of the payload format type, then the 'content-type' header in the 'headers' map is set to this 'datacontenttype' value. - If a field named 'body' exists on the result of the expression then its value is directly mapped to the body of the request. If the value of the 'body' field is of type bytes or string then it is used for the HTTP request body as-is, with no conversion. If the body field is of any other type then it is converted to a JSON string. If the body field does not exist then the resulting payload of the HTTP request will be data value of the CloudEvent HTTP Binding Binary Content Mode representation of the final message as described earlier. - Any other fields in the resulting expression will be ignored. The CEL expression may access the incoming CloudEvent message in its definition, as follows: - The 'data' field of the incoming CloudEvent message can be accessed using the 'message.data' value. Subfields of 'message.data' may also be accessed if an input_payload_format has been specified on the Pipeline. - Each attribute of the incoming CloudEvent message can be accessed using the 'message.' value, where is replaced with the name of the attribute. - Existing headers can be accessed in the CEL expression using the 'headers' variable. The 'headers' variable defines a map of key/value pairs corresponding to the HTTP headers of the CloudEvent HTTP Binding Binary Content Mode representation of the final message as described earlier. For example, the following CEL expression can be used to construct an HTTP request by adding an additional header to the HTTP headers of the CloudEvent HTTP Binding Binary Content Mode representation of the final message and by overwriting the body of the request: Example:: { "headers": headers.merge({"new-header-key": "new-header-value"}), "body": "new-body" } - The default binding for the message payload can be accessed using the 'body' variable. It conatins a string representation of the message payload in the format specified by the 'output_payload_format' field. If the 'input_payload_format' field is not set, the 'body' variable contains the same message payload bytes that were published. Additionally, the following CEL extension functions are provided for use in this CEL expression: - toBase64Url: map.toBase64Url() -> string - Converts a CelValue to a base64url encoded string - toJsonString: map.toJsonString() -> string - Converts a CelValue to a JSON string - merge: map1.merge(map2) -> map3 - Merges the passed CEL map with the existing CEL map the function is applied to. - If the same key exists in both maps, if the key's value is type map both maps are merged else the value from the passed map is used. - denormalize: map.denormalize() -> map - Denormalizes a CEL map such that every value of type map or key in the map is expanded to return a single level map. - The resulting keys are "." separated indices of the map keys. - For example: { "a": 1, "b": { "c": 2, "d": 3 } "e": [4, 5] } .denormalize() -> { "a": 1, "b.c": 2, "b.d": 3, "e.0": 4, "e.1": 5 } - setField: map.setField(key, value) -> message - Sets the field of the message with the given key to the given value. - If the field is not present it will be added. - If the field is present it will be overwritten. - The key can be a dot separated path to set a field in a nested message. - Key must be of type string. - Value may be any valid type. - removeFields: map.removeFields([key1, key2, ...]) -> message - Removes the fields of the map with the given keys. - The keys can be a dot separated path to remove a field in a nested message. - If a key is not found it will be ignored. - Keys must be of type string. - toMap: [map1, map2, ...].toMap() -> map - Converts a CEL list of CEL maps to a single CEL map - toCloudEventJsonWithPayloadFormat: message.toCloudEventJsonWithPayloadFormat() -> map - Converts a message to the corresponding structure of JSON format for CloudEvents. - It converts 'data' to destination payload format specified in 'output_payload_format'. If 'output_payload_format' is not set, the data will remain unchanged. - It also sets the corresponding datacontenttype of the CloudEvent, as indicated by 'output_payload_format'. If no 'output_payload_format' is set it will use the value of the "datacontenttype" attribute on the CloudEvent if present, else remove "datacontenttype" attribute. - This function expects that the content of the message will adhere to the standard CloudEvent format. If it doesn't then this function will fail. - The result is a CEL map that corresponds to the JSON representation of the CloudEvent. To convert that data to a JSON string it can be chained with the toJsonString function. The Pipeline expects that the message it receives adheres to the standard CloudEvent format. If it doesn't then the outgoing message request may fail with a persistent error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#message_binding_template GoogleEventarcPipeline#message_binding_template}
        '''
        value = GoogleEventarcPipelineDestinationsHttpEndpoint(
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
        :param network_attachment: Name of the NetworkAttachment that allows access to the consumer VPC. Format: 'projects/{PROJECT_ID}/regions/{REGION}/networkAttachments/{NETWORK_ATTACHMENT_NAME}' Required for HTTP endpoint destinations. Must not be specified for Workflows, MessageBus, or Topic destinations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#network_attachment GoogleEventarcPipeline#network_attachment}
        '''
        value = GoogleEventarcPipelineDestinationsNetworkConfig(
            network_attachment=network_attachment
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfig", [value]))

    @jsii.member(jsii_name="putOutputPayloadFormat")
    def put_output_payload_format(
        self,
        *,
        avro: typing.Optional[typing.Union[GoogleEventarcPipelineDestinationsOutputPayloadFormatAvro, typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union[GoogleEventarcPipelineDestinationsOutputPayloadFormatJson, typing.Dict[builtins.str, typing.Any]]] = None,
        protobuf: typing.Optional[typing.Union[GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobuf, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param avro: avro block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#avro GoogleEventarcPipeline#avro}
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#json GoogleEventarcPipeline#json}
        :param protobuf: protobuf block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#protobuf GoogleEventarcPipeline#protobuf}
        '''
        value = GoogleEventarcPipelineDestinationsOutputPayloadFormat(
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
    ) -> GoogleEventarcPipelineDestinationsAuthenticationConfigOutputReference:
        return typing.cast(GoogleEventarcPipelineDestinationsAuthenticationConfigOutputReference, jsii.get(self, "authenticationConfig"))

    @builtins.property
    @jsii.member(jsii_name="httpEndpoint")
    def http_endpoint(
        self,
    ) -> GoogleEventarcPipelineDestinationsHttpEndpointOutputReference:
        return typing.cast(GoogleEventarcPipelineDestinationsHttpEndpointOutputReference, jsii.get(self, "httpEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(
        self,
    ) -> GoogleEventarcPipelineDestinationsNetworkConfigOutputReference:
        return typing.cast(GoogleEventarcPipelineDestinationsNetworkConfigOutputReference, jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="outputPayloadFormat")
    def output_payload_format(
        self,
    ) -> GoogleEventarcPipelineDestinationsOutputPayloadFormatOutputReference:
        return typing.cast(GoogleEventarcPipelineDestinationsOutputPayloadFormatOutputReference, jsii.get(self, "outputPayloadFormat"))

    @builtins.property
    @jsii.member(jsii_name="authenticationConfigInput")
    def authentication_config_input(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineDestinationsAuthenticationConfig]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineDestinationsAuthenticationConfig], jsii.get(self, "authenticationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="httpEndpointInput")
    def http_endpoint_input(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineDestinationsHttpEndpoint]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineDestinationsHttpEndpoint], jsii.get(self, "httpEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="messageBusInput")
    def message_bus_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageBusInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineDestinationsNetworkConfig]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineDestinationsNetworkConfig], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="outputPayloadFormatInput")
    def output_payload_format_input(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormat]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormat], jsii.get(self, "outputPayloadFormatInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9c2489e27cd9e435cd9759c6a707004690b50c4787daaa71a1e202ba2c5aee17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageBus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35f0d86945d205898e842972b6ae1b6b31ee0cad9b182a06a22ab9d10f2ded01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workflow")
    def workflow(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workflow"))

    @workflow.setter
    def workflow(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e247417b254e68a8becc5a2a9e66fb5601352cd02e8ef1909dc08fc396354e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workflow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEventarcPipelineDestinations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEventarcPipelineDestinations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEventarcPipelineDestinations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feaf158e31246965e1c64c9c8768f426a3c5207719c4c4471e764707c46117cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineInputPayloadFormat",
    jsii_struct_bases=[],
    name_mapping={"avro": "avro", "json": "json", "protobuf": "protobuf"},
)
class GoogleEventarcPipelineInputPayloadFormat:
    def __init__(
        self,
        *,
        avro: typing.Optional[typing.Union["GoogleEventarcPipelineInputPayloadFormatAvro", typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union["GoogleEventarcPipelineInputPayloadFormatJson", typing.Dict[builtins.str, typing.Any]]] = None,
        protobuf: typing.Optional[typing.Union["GoogleEventarcPipelineInputPayloadFormatProtobuf", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param avro: avro block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#avro GoogleEventarcPipeline#avro}
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#json GoogleEventarcPipeline#json}
        :param protobuf: protobuf block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#protobuf GoogleEventarcPipeline#protobuf}
        '''
        if isinstance(avro, dict):
            avro = GoogleEventarcPipelineInputPayloadFormatAvro(**avro)
        if isinstance(json, dict):
            json = GoogleEventarcPipelineInputPayloadFormatJson(**json)
        if isinstance(protobuf, dict):
            protobuf = GoogleEventarcPipelineInputPayloadFormatProtobuf(**protobuf)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__899bba952eb302bfc44d8f35c05abf4768fe802948250fcc56e8ae2052e44106)
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
    def avro(self) -> typing.Optional["GoogleEventarcPipelineInputPayloadFormatAvro"]:
        '''avro block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#avro GoogleEventarcPipeline#avro}
        '''
        result = self._values.get("avro")
        return typing.cast(typing.Optional["GoogleEventarcPipelineInputPayloadFormatAvro"], result)

    @builtins.property
    def json(self) -> typing.Optional["GoogleEventarcPipelineInputPayloadFormatJson"]:
        '''json block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#json GoogleEventarcPipeline#json}
        '''
        result = self._values.get("json")
        return typing.cast(typing.Optional["GoogleEventarcPipelineInputPayloadFormatJson"], result)

    @builtins.property
    def protobuf(
        self,
    ) -> typing.Optional["GoogleEventarcPipelineInputPayloadFormatProtobuf"]:
        '''protobuf block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#protobuf GoogleEventarcPipeline#protobuf}
        '''
        result = self._values.get("protobuf")
        return typing.cast(typing.Optional["GoogleEventarcPipelineInputPayloadFormatProtobuf"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcPipelineInputPayloadFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineInputPayloadFormatAvro",
    jsii_struct_bases=[],
    name_mapping={"schema_definition": "schemaDefinition"},
)
class GoogleEventarcPipelineInputPayloadFormatAvro:
    def __init__(
        self,
        *,
        schema_definition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema_definition: The entire schema definition is stored in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#schema_definition GoogleEventarcPipeline#schema_definition}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee69bf13a3e7440317f9700fd4083e71a01f186c900c73c73f58be6b2d664ce0)
            check_type(argname="argument schema_definition", value=schema_definition, expected_type=type_hints["schema_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if schema_definition is not None:
            self._values["schema_definition"] = schema_definition

    @builtins.property
    def schema_definition(self) -> typing.Optional[builtins.str]:
        '''The entire schema definition is stored in this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#schema_definition GoogleEventarcPipeline#schema_definition}
        '''
        result = self._values.get("schema_definition")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcPipelineInputPayloadFormatAvro(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcPipelineInputPayloadFormatAvroOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineInputPayloadFormatAvroOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__58249099d8134c88995fc8bff91cb31d92b03d7862e832052ee99cf9a7ca5cd1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b22c6c42b937f2d7d07b8fe7472474458a2890e7668447c4d13f7b4589db431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaDefinition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineInputPayloadFormatAvro]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineInputPayloadFormatAvro], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcPipelineInputPayloadFormatAvro],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b21b978056f4de7391b074740a30ef760318bff3a3f5b70a1f43934229401211)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineInputPayloadFormatJson",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleEventarcPipelineInputPayloadFormatJson:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcPipelineInputPayloadFormatJson(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcPipelineInputPayloadFormatJsonOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineInputPayloadFormatJsonOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a1dc9deef63ac84d299b634979f9cec9a6a84095e1335e52e8c2c4d3ceaaa8f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineInputPayloadFormatJson]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineInputPayloadFormatJson], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcPipelineInputPayloadFormatJson],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af0a2b1133bff4a32ee11f2bb9f28905fe0558c26c57318c165eb806a6e6353c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleEventarcPipelineInputPayloadFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineInputPayloadFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__467132fcabf4094cf5d7eb6143268728ccb5bdc380f7e1f84e04385ceb8af477)
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
        :param schema_definition: The entire schema definition is stored in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#schema_definition GoogleEventarcPipeline#schema_definition}
        '''
        value = GoogleEventarcPipelineInputPayloadFormatAvro(
            schema_definition=schema_definition
        )

        return typing.cast(None, jsii.invoke(self, "putAvro", [value]))

    @jsii.member(jsii_name="putJson")
    def put_json(self) -> None:
        value = GoogleEventarcPipelineInputPayloadFormatJson()

        return typing.cast(None, jsii.invoke(self, "putJson", [value]))

    @jsii.member(jsii_name="putProtobuf")
    def put_protobuf(
        self,
        *,
        schema_definition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema_definition: The entire schema definition is stored in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#schema_definition GoogleEventarcPipeline#schema_definition}
        '''
        value = GoogleEventarcPipelineInputPayloadFormatProtobuf(
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
    def avro(self) -> GoogleEventarcPipelineInputPayloadFormatAvroOutputReference:
        return typing.cast(GoogleEventarcPipelineInputPayloadFormatAvroOutputReference, jsii.get(self, "avro"))

    @builtins.property
    @jsii.member(jsii_name="json")
    def json(self) -> GoogleEventarcPipelineInputPayloadFormatJsonOutputReference:
        return typing.cast(GoogleEventarcPipelineInputPayloadFormatJsonOutputReference, jsii.get(self, "json"))

    @builtins.property
    @jsii.member(jsii_name="protobuf")
    def protobuf(
        self,
    ) -> "GoogleEventarcPipelineInputPayloadFormatProtobufOutputReference":
        return typing.cast("GoogleEventarcPipelineInputPayloadFormatProtobufOutputReference", jsii.get(self, "protobuf"))

    @builtins.property
    @jsii.member(jsii_name="avroInput")
    def avro_input(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineInputPayloadFormatAvro]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineInputPayloadFormatAvro], jsii.get(self, "avroInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonInput")
    def json_input(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineInputPayloadFormatJson]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineInputPayloadFormatJson], jsii.get(self, "jsonInput"))

    @builtins.property
    @jsii.member(jsii_name="protobufInput")
    def protobuf_input(
        self,
    ) -> typing.Optional["GoogleEventarcPipelineInputPayloadFormatProtobuf"]:
        return typing.cast(typing.Optional["GoogleEventarcPipelineInputPayloadFormatProtobuf"], jsii.get(self, "protobufInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineInputPayloadFormat]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineInputPayloadFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcPipelineInputPayloadFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10d955e0edc7de24f6179f6a49261cbc7f2807021d8399f47a43317eeae59a28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineInputPayloadFormatProtobuf",
    jsii_struct_bases=[],
    name_mapping={"schema_definition": "schemaDefinition"},
)
class GoogleEventarcPipelineInputPayloadFormatProtobuf:
    def __init__(
        self,
        *,
        schema_definition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema_definition: The entire schema definition is stored in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#schema_definition GoogleEventarcPipeline#schema_definition}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1f6be3efc27b039e6d2eca5081db0016309d9150b4f67f8ad0e765beec85326)
            check_type(argname="argument schema_definition", value=schema_definition, expected_type=type_hints["schema_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if schema_definition is not None:
            self._values["schema_definition"] = schema_definition

    @builtins.property
    def schema_definition(self) -> typing.Optional[builtins.str]:
        '''The entire schema definition is stored in this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#schema_definition GoogleEventarcPipeline#schema_definition}
        '''
        result = self._values.get("schema_definition")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcPipelineInputPayloadFormatProtobuf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcPipelineInputPayloadFormatProtobufOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineInputPayloadFormatProtobufOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5940517fa9bd262c635bb0aa2528cdafd0a2feaa9e6f74e179843b9ccde487f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c2b6a6022c0fae30b807a9f179d5d43711d6c66f1f30ebd857928d99f599315)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaDefinition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineInputPayloadFormatProtobuf]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineInputPayloadFormatProtobuf], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcPipelineInputPayloadFormatProtobuf],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cd8a64defcccdc3853b3544a1c5ca49b217529470b89cd873837fec1ad202e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"log_severity": "logSeverity"},
)
class GoogleEventarcPipelineLoggingConfig:
    def __init__(self, *, log_severity: typing.Optional[builtins.str] = None) -> None:
        '''
        :param log_severity: The minimum severity of logs that will be sent to Stackdriver/Platform Telemetry. Logs at severitiy ≥ this value will be sent, unless it is NONE. Possible values: ["NONE", "DEBUG", "INFO", "NOTICE", "WARNING", "ERROR", "CRITICAL", "ALERT", "EMERGENCY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#log_severity GoogleEventarcPipeline#log_severity}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3407d66091ec61e7890859ee37f8d8ccf3bd9eaababc568325b3b4b9951aa628)
            check_type(argname="argument log_severity", value=log_severity, expected_type=type_hints["log_severity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_severity is not None:
            self._values["log_severity"] = log_severity

    @builtins.property
    def log_severity(self) -> typing.Optional[builtins.str]:
        '''The minimum severity of logs that will be sent to Stackdriver/Platform Telemetry.

        Logs at severitiy ≥ this value will be sent, unless it is NONE. Possible values: ["NONE", "DEBUG", "INFO", "NOTICE", "WARNING", "ERROR", "CRITICAL", "ALERT", "EMERGENCY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#log_severity GoogleEventarcPipeline#log_severity}
        '''
        result = self._values.get("log_severity")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcPipelineLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcPipelineLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80adf0a4b3cd537d44e3dc8f9074951ffbca1dad5d0c247395f2dcc29392a38a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca93b4ba9a9f1207e13b9d5f1fcb06bf9518cf1dc2dffb69d38c4d6c5cb70a79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logSeverity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleEventarcPipelineLoggingConfig]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcPipelineLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f84883d8acde6ea92631432285d2dd979360ea5672d0a3282333939d39d375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineMediations",
    jsii_struct_bases=[],
    name_mapping={"transformation": "transformation"},
)
class GoogleEventarcPipelineMediations:
    def __init__(
        self,
        *,
        transformation: typing.Optional[typing.Union["GoogleEventarcPipelineMediationsTransformation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param transformation: transformation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#transformation GoogleEventarcPipeline#transformation}
        '''
        if isinstance(transformation, dict):
            transformation = GoogleEventarcPipelineMediationsTransformation(**transformation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc66f052960f16cf889d29c810c3bb21d9a59f8ff07df02f4fd0ba203bf463d3)
            check_type(argname="argument transformation", value=transformation, expected_type=type_hints["transformation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if transformation is not None:
            self._values["transformation"] = transformation

    @builtins.property
    def transformation(
        self,
    ) -> typing.Optional["GoogleEventarcPipelineMediationsTransformation"]:
        '''transformation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#transformation GoogleEventarcPipeline#transformation}
        '''
        result = self._values.get("transformation")
        return typing.cast(typing.Optional["GoogleEventarcPipelineMediationsTransformation"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcPipelineMediations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcPipelineMediationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineMediationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8de1d6f779cdca8c672d28bf40e772768027b8e9c992331cc9df2a8fa2a785a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleEventarcPipelineMediationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd6ada8835e624197217b226eda9c6b4f1eb213d1b85ffbf84ee47595ab559b5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleEventarcPipelineMediationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__497bd249ccadefa8ad30988a19fa95d8291ca8543f64aa4a37b7b02f8ab14ad3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab7de9846cc688ca261b7eddeaab4dd7d70f4b1317ac645148c89e236a8945a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f120f456588f9223c21c53f3ba55f9b58702c27acd99159425ae6b1f5aff1d7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleEventarcPipelineMediations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleEventarcPipelineMediations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleEventarcPipelineMediations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5259cc1165e670ace31da4ef9ad6aec598ba1fd23045865c083f2b503a0cb08d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleEventarcPipelineMediationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineMediationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6121c38bc8ce8f9e6cffd64896b9ae5a76819d1b8028b31ef345f4ab902dbbb5)
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
        :param transformation_template: The CEL expression template to apply to transform messages. The following CEL extension functions are provided for use in this CEL expression: - merge: map1.merge(map2) -> map3 - Merges the passed CEL map with the existing CEL map the function is applied to. - If the same key exists in both maps, if the key's value is type map both maps are merged else the value from the passed map is used. - denormalize: map.denormalize() -> map - Denormalizes a CEL map such that every value of type map or key in the map is expanded to return a single level map. - The resulting keys are "." separated indices of the map keys. - For example: { "a": 1, "b": { "c": 2, "d": 3 } "e": [4, 5] } .denormalize() -> { "a": 1, "b.c": 2, "b.d": 3, "e.0": 4, "e.1": 5 } - setField: map.setField(key, value) -> message - Sets the field of the message with the given key to the given value. - If the field is not present it will be added. - If the field is present it will be overwritten. - The key can be a dot separated path to set a field in a nested message. - Key must be of type string. - Value may be any valid type. - removeFields: map.removeFields([key1, key2, ...]) -> message - Removes the fields of the map with the given keys. - The keys can be a dot separated path to remove a field in a nested message. - If a key is not found it will be ignored. - Keys must be of type string. - toMap: [map1, map2, ...].toMap() -> map - Converts a CEL list of CEL maps to a single CEL map - toDestinationPayloadFormat(): message.data.toDestinationPayloadFormat() -> string or bytes - Converts the message data to the destination payload format specified in Pipeline.Destination.output_payload_format - This function is meant to be applied to the message.data field. - If the destination payload format is not set, the function will return the message data unchanged. - toCloudEventJsonWithPayloadFormat: message.toCloudEventJsonWithPayloadFormat() -> map - Converts a message to the corresponding structure of JSON format for CloudEvents - This function applies toDestinationPayloadFormat() to the message data. It also sets the corresponding datacontenttype of the CloudEvent, as indicated by Pipeline.Destination.output_payload_format. If no output_payload_format is set it will use the existing datacontenttype on the CloudEvent if present, else leave datacontenttype absent. - This function expects that the content of the message will adhere to the standard CloudEvent format. If it doesn't then this function will fail. - The result is a CEL map that corresponds to the JSON representation of the CloudEvent. To convert that data to a JSON string it can be chained with the toJsonString function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#transformation_template GoogleEventarcPipeline#transformation_template}
        '''
        value = GoogleEventarcPipelineMediationsTransformation(
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
    ) -> "GoogleEventarcPipelineMediationsTransformationOutputReference":
        return typing.cast("GoogleEventarcPipelineMediationsTransformationOutputReference", jsii.get(self, "transformation"))

    @builtins.property
    @jsii.member(jsii_name="transformationInput")
    def transformation_input(
        self,
    ) -> typing.Optional["GoogleEventarcPipelineMediationsTransformation"]:
        return typing.cast(typing.Optional["GoogleEventarcPipelineMediationsTransformation"], jsii.get(self, "transformationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEventarcPipelineMediations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEventarcPipelineMediations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEventarcPipelineMediations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ff610dc7b42057dacb7997a66d39614652b67d28b9fa2be49d2d5db5754cf92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineMediationsTransformation",
    jsii_struct_bases=[],
    name_mapping={"transformation_template": "transformationTemplate"},
)
class GoogleEventarcPipelineMediationsTransformation:
    def __init__(
        self,
        *,
        transformation_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param transformation_template: The CEL expression template to apply to transform messages. The following CEL extension functions are provided for use in this CEL expression: - merge: map1.merge(map2) -> map3 - Merges the passed CEL map with the existing CEL map the function is applied to. - If the same key exists in both maps, if the key's value is type map both maps are merged else the value from the passed map is used. - denormalize: map.denormalize() -> map - Denormalizes a CEL map such that every value of type map or key in the map is expanded to return a single level map. - The resulting keys are "." separated indices of the map keys. - For example: { "a": 1, "b": { "c": 2, "d": 3 } "e": [4, 5] } .denormalize() -> { "a": 1, "b.c": 2, "b.d": 3, "e.0": 4, "e.1": 5 } - setField: map.setField(key, value) -> message - Sets the field of the message with the given key to the given value. - If the field is not present it will be added. - If the field is present it will be overwritten. - The key can be a dot separated path to set a field in a nested message. - Key must be of type string. - Value may be any valid type. - removeFields: map.removeFields([key1, key2, ...]) -> message - Removes the fields of the map with the given keys. - The keys can be a dot separated path to remove a field in a nested message. - If a key is not found it will be ignored. - Keys must be of type string. - toMap: [map1, map2, ...].toMap() -> map - Converts a CEL list of CEL maps to a single CEL map - toDestinationPayloadFormat(): message.data.toDestinationPayloadFormat() -> string or bytes - Converts the message data to the destination payload format specified in Pipeline.Destination.output_payload_format - This function is meant to be applied to the message.data field. - If the destination payload format is not set, the function will return the message data unchanged. - toCloudEventJsonWithPayloadFormat: message.toCloudEventJsonWithPayloadFormat() -> map - Converts a message to the corresponding structure of JSON format for CloudEvents - This function applies toDestinationPayloadFormat() to the message data. It also sets the corresponding datacontenttype of the CloudEvent, as indicated by Pipeline.Destination.output_payload_format. If no output_payload_format is set it will use the existing datacontenttype on the CloudEvent if present, else leave datacontenttype absent. - This function expects that the content of the message will adhere to the standard CloudEvent format. If it doesn't then this function will fail. - The result is a CEL map that corresponds to the JSON representation of the CloudEvent. To convert that data to a JSON string it can be chained with the toJsonString function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#transformation_template GoogleEventarcPipeline#transformation_template}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40d61985e9eaab17375f32d82df9fd708e2df18a966526778a0bb71878a3e0a9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#transformation_template GoogleEventarcPipeline#transformation_template}
        '''
        result = self._values.get("transformation_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcPipelineMediationsTransformation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcPipelineMediationsTransformationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineMediationsTransformationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a0ad607f51e87ad952ea0a853b853f17a912d557c2d76613008eda23538d8a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__793be3eed2053ccb8e375219325de8ca01b40e85783f15ab292145f00a301d71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transformationTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEventarcPipelineMediationsTransformation]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineMediationsTransformation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcPipelineMediationsTransformation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd9cc8028c7ec35436db2f0b994d31774edfec2998837c28b304be0f22a17528)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineRetryPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "max_attempts": "maxAttempts",
        "max_retry_delay": "maxRetryDelay",
        "min_retry_delay": "minRetryDelay",
    },
)
class GoogleEventarcPipelineRetryPolicy:
    def __init__(
        self,
        *,
        max_attempts: typing.Optional[jsii.Number] = None,
        max_retry_delay: typing.Optional[builtins.str] = None,
        min_retry_delay: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_attempts: The maximum number of delivery attempts for any message. The value must be between 1 and 100. The default value for this field is 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#max_attempts GoogleEventarcPipeline#max_attempts}
        :param max_retry_delay: The maximum amount of seconds to wait between retry attempts. The value must be between 1 and 600. The default value for this field is 60. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#max_retry_delay GoogleEventarcPipeline#max_retry_delay}
        :param min_retry_delay: The minimum amount of seconds to wait between retry attempts. The value must be between 1 and 600. The default value for this field is 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#min_retry_delay GoogleEventarcPipeline#min_retry_delay}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__382df62065b4b73007d9310d6d9c4225c1dae00a935107c86bca126c61007d6e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#max_attempts GoogleEventarcPipeline#max_attempts}
        '''
        result = self._values.get("max_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retry_delay(self) -> typing.Optional[builtins.str]:
        '''The maximum amount of seconds to wait between retry attempts.

        The value
        must be between 1 and 600.
        The default value for this field is 60.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#max_retry_delay GoogleEventarcPipeline#max_retry_delay}
        '''
        result = self._values.get("max_retry_delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_retry_delay(self) -> typing.Optional[builtins.str]:
        '''The minimum amount of seconds to wait between retry attempts.

        The value
        must be between 1 and 600.
        The default value for this field is 5.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#min_retry_delay GoogleEventarcPipeline#min_retry_delay}
        '''
        result = self._values.get("min_retry_delay")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcPipelineRetryPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcPipelineRetryPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineRetryPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69d5b760da199808579eaf8e4c1f2d6ec2185a5c1c6485e8b3b2c6a6730bce79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e89ac21ccbdef568351a1507b82979456b86bba6cb43a92b13095a895c9b501d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetryDelay")
    def max_retry_delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxRetryDelay"))

    @max_retry_delay.setter
    def max_retry_delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43a420da3ec8ce0edb1d2a3029fd5caef5f4947c8eed71c50e022dfc438c5cf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetryDelay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minRetryDelay")
    def min_retry_delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minRetryDelay"))

    @min_retry_delay.setter
    def min_retry_delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0ee54b515ba48ad44054bf1666d9111973870b096446bb97c92e09c11f34af0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minRetryDelay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleEventarcPipelineRetryPolicy]:
        return typing.cast(typing.Optional[GoogleEventarcPipelineRetryPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcPipelineRetryPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93243be30bb0f364bb3d85e6afaf47eaed1144cf5742c89c9129df997de310fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleEventarcPipelineTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#create GoogleEventarcPipeline#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#delete GoogleEventarcPipeline#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#update GoogleEventarcPipeline#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48e6e9e0250f1285dff698e823de5dfec7afbfa0597305ac5c20af18603c2b35)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#create GoogleEventarcPipeline#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#delete GoogleEventarcPipeline#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_pipeline#update GoogleEventarcPipeline#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcPipelineTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcPipelineTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcPipeline.GoogleEventarcPipelineTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc2381431658d9a385e6bbe51080639117646d9b8647de214b800e1210b592c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a231012be17cfd27e4592b716ff42403d25a32a01df4c76307d051eaf58e11e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f796670d7aaf07429e0e4ae04e320cd937769ebb4ded87f630856c1bfd39dfad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2173e316825379655ac9e815ed019f531802aeda2d43ababed360996ff3a88bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEventarcPipelineTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEventarcPipelineTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEventarcPipelineTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e29d80dd8bf104fc05f8d6edc3cd0467a2e01f2183ea4a23d3134aec0ca9183)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleEventarcPipeline",
    "GoogleEventarcPipelineConfig",
    "GoogleEventarcPipelineDestinations",
    "GoogleEventarcPipelineDestinationsAuthenticationConfig",
    "GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidc",
    "GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidcOutputReference",
    "GoogleEventarcPipelineDestinationsAuthenticationConfigOauthToken",
    "GoogleEventarcPipelineDestinationsAuthenticationConfigOauthTokenOutputReference",
    "GoogleEventarcPipelineDestinationsAuthenticationConfigOutputReference",
    "GoogleEventarcPipelineDestinationsHttpEndpoint",
    "GoogleEventarcPipelineDestinationsHttpEndpointOutputReference",
    "GoogleEventarcPipelineDestinationsList",
    "GoogleEventarcPipelineDestinationsNetworkConfig",
    "GoogleEventarcPipelineDestinationsNetworkConfigOutputReference",
    "GoogleEventarcPipelineDestinationsOutputPayloadFormat",
    "GoogleEventarcPipelineDestinationsOutputPayloadFormatAvro",
    "GoogleEventarcPipelineDestinationsOutputPayloadFormatAvroOutputReference",
    "GoogleEventarcPipelineDestinationsOutputPayloadFormatJson",
    "GoogleEventarcPipelineDestinationsOutputPayloadFormatJsonOutputReference",
    "GoogleEventarcPipelineDestinationsOutputPayloadFormatOutputReference",
    "GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobuf",
    "GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobufOutputReference",
    "GoogleEventarcPipelineDestinationsOutputReference",
    "GoogleEventarcPipelineInputPayloadFormat",
    "GoogleEventarcPipelineInputPayloadFormatAvro",
    "GoogleEventarcPipelineInputPayloadFormatAvroOutputReference",
    "GoogleEventarcPipelineInputPayloadFormatJson",
    "GoogleEventarcPipelineInputPayloadFormatJsonOutputReference",
    "GoogleEventarcPipelineInputPayloadFormatOutputReference",
    "GoogleEventarcPipelineInputPayloadFormatProtobuf",
    "GoogleEventarcPipelineInputPayloadFormatProtobufOutputReference",
    "GoogleEventarcPipelineLoggingConfig",
    "GoogleEventarcPipelineLoggingConfigOutputReference",
    "GoogleEventarcPipelineMediations",
    "GoogleEventarcPipelineMediationsList",
    "GoogleEventarcPipelineMediationsOutputReference",
    "GoogleEventarcPipelineMediationsTransformation",
    "GoogleEventarcPipelineMediationsTransformationOutputReference",
    "GoogleEventarcPipelineRetryPolicy",
    "GoogleEventarcPipelineRetryPolicyOutputReference",
    "GoogleEventarcPipelineTimeouts",
    "GoogleEventarcPipelineTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0170cf35c3fd6f15b7f4ad31ad9248a593e5bf494eaf19edd6c7169061ac418b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    destinations: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleEventarcPipelineDestinations, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    pipeline_id: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    crypto_key_name: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    input_payload_format: typing.Optional[typing.Union[GoogleEventarcPipelineInputPayloadFormat, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    logging_config: typing.Optional[typing.Union[GoogleEventarcPipelineLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    mediations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleEventarcPipelineMediations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    retry_policy: typing.Optional[typing.Union[GoogleEventarcPipelineRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleEventarcPipelineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__fffaf5fc0268035b1de1874bc3fdd9e6d840041efc30be6e5c9311f67ea0430b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33dd76bf254d0544d7c47f363799f44946e43158feb43843aecc74c09ef8c08b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleEventarcPipelineDestinations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa02a8ae63bdc94acd3e8b742a65b62b49945d48b7da2037a9d752497f7f5b50(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleEventarcPipelineMediations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d10fa95a5a35f009ae1a7fb433a9588f3f29852eba78c04a0bcf83a7c7615f1f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db875b8b74b1f5cf7f6c18966b80fea93faab30886a10d9b2ed56f11e7024d8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bce6fc00bcc617204a5ba3dfc5b5cf301239ae7c7ebaf3ca844a105d62c4175(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2988a4aebc2b8c1148b25a5e725a9f071c05640b8084b3a8a55e211cf6e7a246(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10258beee9a81b58f9bf39a388148e12e20d6e48101cec9a6b3c17e55124521(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09581f75a7783631a70af076034a7d45685003e48ff2a52a5904fee5297a59aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa7ce49b7059dbaae5c953e529c5d1d238ca2c55910ce285c25efc32cd12941(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe5d21b0a84b9154c07656ad9b633bed2b5e562a8e36c9bdb682f45d7d0b82b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c8aa72507a032bd4cbdb73a2d9853c5da2f9647ebc5f56830cb6076aa2ad57a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    destinations: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleEventarcPipelineDestinations, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    pipeline_id: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    crypto_key_name: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    input_payload_format: typing.Optional[typing.Union[GoogleEventarcPipelineInputPayloadFormat, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    logging_config: typing.Optional[typing.Union[GoogleEventarcPipelineLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    mediations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleEventarcPipelineMediations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    retry_policy: typing.Optional[typing.Union[GoogleEventarcPipelineRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleEventarcPipelineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd7623e461cd1d0da8c56519b68f5dd229a326cc476d1cf211828b0f9b77dbb(
    *,
    authentication_config: typing.Optional[typing.Union[GoogleEventarcPipelineDestinationsAuthenticationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    http_endpoint: typing.Optional[typing.Union[GoogleEventarcPipelineDestinationsHttpEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    message_bus: typing.Optional[builtins.str] = None,
    network_config: typing.Optional[typing.Union[GoogleEventarcPipelineDestinationsNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    output_payload_format: typing.Optional[typing.Union[GoogleEventarcPipelineDestinationsOutputPayloadFormat, typing.Dict[builtins.str, typing.Any]]] = None,
    topic: typing.Optional[builtins.str] = None,
    workflow: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e73f4a41ef4b3d4273ebb719876b828a37a9b24e282362786e43f6a7e256b6(
    *,
    google_oidc: typing.Optional[typing.Union[GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidc, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth_token: typing.Optional[typing.Union[GoogleEventarcPipelineDestinationsAuthenticationConfigOauthToken, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a67d5f2d8acddf1c837c7d9a8dbd10dee49da07e269b6e9f2ce1d3ad574c1d(
    *,
    service_account: builtins.str,
    audience: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__633dbcf83fe10b5b7c052b8e7ac15002aaddbfce57a7f2b4cc7be22eff3720b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef03312c423a7377d2ef1dead7b8dc9d0231bb505f7c644d11e3fc93766857a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f1c1a87b242ffeb29026b7512b8da149f6e9a6a2bbe049b65a997113159ebee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8f4e24185d6ac2ec2b8bd2876f7d0860b1e338f1800242cf9cc75f485f213c(
    value: typing.Optional[GoogleEventarcPipelineDestinationsAuthenticationConfigGoogleOidc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e313e00da416532fb7450bb7b5230a060e816b2be2a8cfcea5242383f44de9(
    *,
    service_account: builtins.str,
    scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb491c66a9b13385555656eabc411187e7fc54ee6560d6188464c95de589912(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10540222f014edb4981d5782bc850dc721eb2d270027466c886cbb4da2daf6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ace5ca0f661a7b8a878eeab00b694b6d99d58c41de751f244932bb5ebe07192(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8832986b795d4bdb73dba398d68cc76a56cee14eeb27f33e6a890020a5af5c05(
    value: typing.Optional[GoogleEventarcPipelineDestinationsAuthenticationConfigOauthToken],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa25ab87a0bce9863fdfa807197c39f9587df3d8994ee14a3542fd965421a5ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2fb43159444fe4284c3621cff4280629451b67b2a9fc1eba94c68be010764c5(
    value: typing.Optional[GoogleEventarcPipelineDestinationsAuthenticationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ddc2d8b5e3db407ef285bbfef441ebc5d2aa764b8eee70729a8ccb65a3bec71(
    *,
    uri: builtins.str,
    message_binding_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d06f9e4a5cbccbad53df04a542fbd14d34885f9ab6226965130bde515eacae0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa8ec507572f06bb97a66da0cddcb6fc79e377ec1219cc928f1db80995e647b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2697ee56853faec6477e2297848679f1a37c93a49850d055933c79a67f9ef32b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fe404dd400c2f78217c5c203e79535c8ee6fd8d67b48eb22bc8945e801b39a6(
    value: typing.Optional[GoogleEventarcPipelineDestinationsHttpEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2407e9ded56fdada3f159d2c639e5cf19c11113457b71e0066b254dc21f5c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__726b05efba788384aba751087a16347dc13ccf2051b08b782ad1059201731b93(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e4591ac30e82302831552dfef992b5329cc137725865739a24289236271ab28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a960345bcbd35bf2e1e185f79e51f9aa51d26176b4c25639158228b1a110fa77(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16251d85be6a173945c81ebee6d29649e3c043affed20254f5930a0997a74146(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6280b8d6e13de9f52eeb0900e0beec98b9905e57ccae61aafa8d35b57510b34(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleEventarcPipelineDestinations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e47e9cdf87410e13db4b667f227ebc104fdfb78ce4469749b56c575cca565ba(
    *,
    network_attachment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c49f6736daf5e4ba62e6f1fc4255dad6d6096b7cbd52a73bbcd5eacca0b7fb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f9dda5fa0c56dd30c961f0f0e73871c387b45860e356d26af97a7781ef44ff8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9419be67acc55336349806a4cff550245bfa9dead1e181e573b2ffc5c1184af7(
    value: typing.Optional[GoogleEventarcPipelineDestinationsNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2da4fdf4527932fbaadc86956deeca4e1b3906787daab6b3277267e1d0dcdf0(
    *,
    avro: typing.Optional[typing.Union[GoogleEventarcPipelineDestinationsOutputPayloadFormatAvro, typing.Dict[builtins.str, typing.Any]]] = None,
    json: typing.Optional[typing.Union[GoogleEventarcPipelineDestinationsOutputPayloadFormatJson, typing.Dict[builtins.str, typing.Any]]] = None,
    protobuf: typing.Optional[typing.Union[GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobuf, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b1950906964b4ed33fc38f37b1738f901a8d4d1793a04e75636b88f00633898(
    *,
    schema_definition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b7850d4ae31d1480b17cc9b831877dd3bd325b3edc0520d4ecd21bc0232a624(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d76ab18a0b0bf63f48c175442faf91bf2faf5853987060541e66674e54a4a3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f0e3e676707a4b52a57cb0c47522240fc3f5027baf73515b305a39557d09458(
    value: typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormatAvro],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d5aea34c3136fcba8165cdcf666ae83c5ce247afb1f3b8931617055446a169(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7361489f3fb156f3f1139639397c09f484ac0a249a548bec54c1c2050123bc(
    value: typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormatJson],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03712595936a708cfac9e9261e712ba53168dc74b743c3c3d7ae3ed21e9476bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__148ac2983e4376323b4a4b5fdb9f4723771c34c3ad5fb0c46553b0944c9cf473(
    value: typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de95446886594a3375d7c57c899ef770b3421a8f94f924fba4a14a39ad6b6765(
    *,
    schema_definition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb665d614d25ee41b4915acd16e9fa5e2aa3304828329b67ce25950b34a9c71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ffd6787d3fec08011711285eb091d33fa0a807d25af0fdc7e0a3d33a9ff242(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3be934e65768a6a7eb66ea6176a0261bcd37938b6ebd4ea070cbb66d389a2413(
    value: typing.Optional[GoogleEventarcPipelineDestinationsOutputPayloadFormatProtobuf],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0dd8d3587a8bb63f1068561de51417b8a7d9db4200d61cb013d210568bc6810(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c2489e27cd9e435cd9759c6a707004690b50c4787daaa71a1e202ba2c5aee17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35f0d86945d205898e842972b6ae1b6b31ee0cad9b182a06a22ab9d10f2ded01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e247417b254e68a8becc5a2a9e66fb5601352cd02e8ef1909dc08fc396354e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feaf158e31246965e1c64c9c8768f426a3c5207719c4c4471e764707c46117cc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEventarcPipelineDestinations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__899bba952eb302bfc44d8f35c05abf4768fe802948250fcc56e8ae2052e44106(
    *,
    avro: typing.Optional[typing.Union[GoogleEventarcPipelineInputPayloadFormatAvro, typing.Dict[builtins.str, typing.Any]]] = None,
    json: typing.Optional[typing.Union[GoogleEventarcPipelineInputPayloadFormatJson, typing.Dict[builtins.str, typing.Any]]] = None,
    protobuf: typing.Optional[typing.Union[GoogleEventarcPipelineInputPayloadFormatProtobuf, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee69bf13a3e7440317f9700fd4083e71a01f186c900c73c73f58be6b2d664ce0(
    *,
    schema_definition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58249099d8134c88995fc8bff91cb31d92b03d7862e832052ee99cf9a7ca5cd1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b22c6c42b937f2d7d07b8fe7472474458a2890e7668447c4d13f7b4589db431(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21b978056f4de7391b074740a30ef760318bff3a3f5b70a1f43934229401211(
    value: typing.Optional[GoogleEventarcPipelineInputPayloadFormatAvro],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a1dc9deef63ac84d299b634979f9cec9a6a84095e1335e52e8c2c4d3ceaaa8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af0a2b1133bff4a32ee11f2bb9f28905fe0558c26c57318c165eb806a6e6353c(
    value: typing.Optional[GoogleEventarcPipelineInputPayloadFormatJson],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467132fcabf4094cf5d7eb6143268728ccb5bdc380f7e1f84e04385ceb8af477(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d955e0edc7de24f6179f6a49261cbc7f2807021d8399f47a43317eeae59a28(
    value: typing.Optional[GoogleEventarcPipelineInputPayloadFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f6be3efc27b039e6d2eca5081db0016309d9150b4f67f8ad0e765beec85326(
    *,
    schema_definition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5940517fa9bd262c635bb0aa2528cdafd0a2feaa9e6f74e179843b9ccde487f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c2b6a6022c0fae30b807a9f179d5d43711d6c66f1f30ebd857928d99f599315(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd8a64defcccdc3853b3544a1c5ca49b217529470b89cd873837fec1ad202e3(
    value: typing.Optional[GoogleEventarcPipelineInputPayloadFormatProtobuf],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3407d66091ec61e7890859ee37f8d8ccf3bd9eaababc568325b3b4b9951aa628(
    *,
    log_severity: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80adf0a4b3cd537d44e3dc8f9074951ffbca1dad5d0c247395f2dcc29392a38a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca93b4ba9a9f1207e13b9d5f1fcb06bf9518cf1dc2dffb69d38c4d6c5cb70a79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f84883d8acde6ea92631432285d2dd979360ea5672d0a3282333939d39d375(
    value: typing.Optional[GoogleEventarcPipelineLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc66f052960f16cf889d29c810c3bb21d9a59f8ff07df02f4fd0ba203bf463d3(
    *,
    transformation: typing.Optional[typing.Union[GoogleEventarcPipelineMediationsTransformation, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8de1d6f779cdca8c672d28bf40e772768027b8e9c992331cc9df2a8fa2a785a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd6ada8835e624197217b226eda9c6b4f1eb213d1b85ffbf84ee47595ab559b5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__497bd249ccadefa8ad30988a19fa95d8291ca8543f64aa4a37b7b02f8ab14ad3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab7de9846cc688ca261b7eddeaab4dd7d70f4b1317ac645148c89e236a8945a5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f120f456588f9223c21c53f3ba55f9b58702c27acd99159425ae6b1f5aff1d7b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5259cc1165e670ace31da4ef9ad6aec598ba1fd23045865c083f2b503a0cb08d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleEventarcPipelineMediations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6121c38bc8ce8f9e6cffd64896b9ae5a76819d1b8028b31ef345f4ab902dbbb5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff610dc7b42057dacb7997a66d39614652b67d28b9fa2be49d2d5db5754cf92(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEventarcPipelineMediations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40d61985e9eaab17375f32d82df9fd708e2df18a966526778a0bb71878a3e0a9(
    *,
    transformation_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0ad607f51e87ad952ea0a853b853f17a912d557c2d76613008eda23538d8a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__793be3eed2053ccb8e375219325de8ca01b40e85783f15ab292145f00a301d71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9cc8028c7ec35436db2f0b994d31774edfec2998837c28b304be0f22a17528(
    value: typing.Optional[GoogleEventarcPipelineMediationsTransformation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382df62065b4b73007d9310d6d9c4225c1dae00a935107c86bca126c61007d6e(
    *,
    max_attempts: typing.Optional[jsii.Number] = None,
    max_retry_delay: typing.Optional[builtins.str] = None,
    min_retry_delay: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d5b760da199808579eaf8e4c1f2d6ec2185a5c1c6485e8b3b2c6a6730bce79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e89ac21ccbdef568351a1507b82979456b86bba6cb43a92b13095a895c9b501d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a420da3ec8ce0edb1d2a3029fd5caef5f4947c8eed71c50e022dfc438c5cf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0ee54b515ba48ad44054bf1666d9111973870b096446bb97c92e09c11f34af0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93243be30bb0f364bb3d85e6afaf47eaed1144cf5742c89c9129df997de310fe(
    value: typing.Optional[GoogleEventarcPipelineRetryPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48e6e9e0250f1285dff698e823de5dfec7afbfa0597305ac5c20af18603c2b35(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc2381431658d9a385e6bbe51080639117646d9b8647de214b800e1210b592c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a231012be17cfd27e4592b716ff42403d25a32a01df4c76307d051eaf58e11e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f796670d7aaf07429e0e4ae04e320cd937769ebb4ded87f630856c1bfd39dfad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2173e316825379655ac9e815ed019f531802aeda2d43ababed360996ff3a88bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e29d80dd8bf104fc05f8d6edc3cd0467a2e01f2183ea4a23d3134aec0ca9183(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEventarcPipelineTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
