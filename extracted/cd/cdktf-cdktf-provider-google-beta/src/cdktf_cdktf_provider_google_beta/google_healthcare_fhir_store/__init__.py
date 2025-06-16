r'''
# `google_healthcare_fhir_store`

Refer to the Terraform Registry for docs: [`google_healthcare_fhir_store`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store).
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


class GoogleHealthcareFhirStore(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleHealthcareFhirStore.GoogleHealthcareFhirStore",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store google_healthcare_fhir_store}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dataset: builtins.str,
        name: builtins.str,
        complex_data_type_reference_parsing: typing.Optional[builtins.str] = None,
        default_search_handling_strict: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_referential_integrity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_resource_versioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_history_import: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_history_modifications: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_update_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        notification_config: typing.Optional[typing.Union["GoogleHealthcareFhirStoreNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        notification_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleHealthcareFhirStoreNotificationConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stream_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleHealthcareFhirStoreStreamConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleHealthcareFhirStoreTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store google_healthcare_fhir_store} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dataset: Identifies the dataset addressed by this request. Must be in the format 'projects/{project}/locations/{location}/datasets/{dataset}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#dataset GoogleHealthcareFhirStore#dataset}
        :param name: The resource name for the FhirStore. ** Changing this property may recreate the FHIR store (removing all data) ** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#name GoogleHealthcareFhirStore#name}
        :param complex_data_type_reference_parsing: Enable parsing of references within complex FHIR data types such as Extensions. If this value is set to ENABLED, then features like referential integrity and Bundle reference rewriting apply to all references. If this flag has not been specified the behavior of the FHIR store will not change, references in complex data types will not be parsed. New stores will have this value set to ENABLED by default after a notification period. Warning: turning on this flag causes processing existing resources to fail if they contain references to non-existent resources. Possible values: ["COMPLEX_DATA_TYPE_REFERENCE_PARSING_UNSPECIFIED", "DISABLED", "ENABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#complex_data_type_reference_parsing GoogleHealthcareFhirStore#complex_data_type_reference_parsing}
        :param default_search_handling_strict: If true, overrides the default search behavior for this FHIR store to handling=strict which returns an error for unrecognized search parameters. If false, uses the FHIR specification default handling=lenient which ignores unrecognized search parameters. The handling can always be changed from the default on an individual API call by setting the HTTP header Prefer: handling=strict or Prefer: handling=lenient. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#default_search_handling_strict GoogleHealthcareFhirStore#default_search_handling_strict}
        :param disable_referential_integrity: Whether to disable referential integrity in this FHIR store. This field is immutable after FHIR store creation. The default value is false, meaning that the API will enforce referential integrity and fail the requests that will result in inconsistent state in the FHIR store. When this field is set to true, the API will skip referential integrity check. Consequently, operations that rely on references, such as Patient.get$everything, will not return all the results if broken references exist. ** Changing this property may recreate the FHIR store (removing all data) ** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#disable_referential_integrity GoogleHealthcareFhirStore#disable_referential_integrity}
        :param disable_resource_versioning: Whether to disable resource versioning for this FHIR store. This field can not be changed after the creation of FHIR store. If set to false, which is the default behavior, all write operations will cause historical versions to be recorded automatically. The historical versions can be fetched through the history APIs, but cannot be updated. If set to true, no historical versions will be kept. The server will send back errors for attempts to read the historical versions. ** Changing this property may recreate the FHIR store (removing all data) ** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#disable_resource_versioning GoogleHealthcareFhirStore#disable_resource_versioning}
        :param enable_history_import: Whether to allow the bulk import API to accept history bundles and directly insert historical resource versions into the FHIR store. Importing resource histories creates resource interactions that appear to have occurred in the past, which clients may not want to allow. If set to false, history bundles within an import will fail with an error. ** Changing this property may recreate the FHIR store (removing all data) ** ** This property can be changed manually in the Google Cloud Healthcare admin console without recreating the FHIR store ** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#enable_history_import GoogleHealthcareFhirStore#enable_history_import}
        :param enable_history_modifications: Whether to allow the ExecuteBundle API to accept history bundles, and directly insert and overwrite historical resource versions into the FHIR store. If set to false, using history bundles fails with an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#enable_history_modifications GoogleHealthcareFhirStore#enable_history_modifications}
        :param enable_update_create: Whether this FHIR store has the updateCreate capability. This determines if the client can use an Update operation to create a new resource with a client-specified ID. If false, all IDs are server-assigned through the Create operation and attempts to Update a non-existent resource will return errors. Please treat the audit logs with appropriate levels of care if client-specified resource IDs contain sensitive data such as patient identifiers, those IDs will be part of the FHIR resource path recorded in Cloud audit logs and Cloud Pub/Sub notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#enable_update_create GoogleHealthcareFhirStore#enable_update_create}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#id GoogleHealthcareFhirStore#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-supplied key-value pairs used to organize FHIR stores. Label keys must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}][\\p{Ll}\\p{Lo}\\p{N}_-]{0,62} Label values are optional, must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}\\p{N}_-]{0,63} No more than 64 labels can be associated with a given store. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#labels GoogleHealthcareFhirStore#labels}
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#notification_config GoogleHealthcareFhirStore#notification_config}
        :param notification_configs: notification_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#notification_configs GoogleHealthcareFhirStore#notification_configs}
        :param stream_configs: stream_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#stream_configs GoogleHealthcareFhirStore#stream_configs}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#timeouts GoogleHealthcareFhirStore#timeouts}
        :param version: The FHIR specification version. Default value: "STU3" Possible values: ["DSTU2", "STU3", "R4"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#version GoogleHealthcareFhirStore#version}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae585ad673345dc2da8b741cbc4186a7adfdbff61a7ce36dcb26beef5a95d713)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleHealthcareFhirStoreConfig(
            dataset=dataset,
            name=name,
            complex_data_type_reference_parsing=complex_data_type_reference_parsing,
            default_search_handling_strict=default_search_handling_strict,
            disable_referential_integrity=disable_referential_integrity,
            disable_resource_versioning=disable_resource_versioning,
            enable_history_import=enable_history_import,
            enable_history_modifications=enable_history_modifications,
            enable_update_create=enable_update_create,
            id=id,
            labels=labels,
            notification_config=notification_config,
            notification_configs=notification_configs,
            stream_configs=stream_configs,
            timeouts=timeouts,
            version=version,
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
        '''Generates CDKTF code for importing a GoogleHealthcareFhirStore resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleHealthcareFhirStore to import.
        :param import_from_id: The id of the existing GoogleHealthcareFhirStore that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleHealthcareFhirStore to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdf166323eae5564485002f095a97dcbd333fba4f4fe7ce91c8690ce4efba68e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putNotificationConfig")
    def put_notification_config(self, *, pubsub_topic: builtins.str) -> None:
        '''
        :param pubsub_topic: The Cloud Pub/Sub topic that notifications of changes are published on. Supplied by the client. PubsubMessage.Data will contain the resource name. PubsubMessage.MessageId is the ID of this message. It is guaranteed to be unique within the topic. PubsubMessage.PublishTime is the time at which the message was published. Notifications are only sent if the topic is non-empty. Topic names must be scoped to a project. service-PROJECT_NUMBER@gcp-sa-healthcare.iam.gserviceaccount.com must have publisher permissions on the given Cloud Pub/Sub topic. Not having adequate permissions will cause the calls that send notifications to fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#pubsub_topic GoogleHealthcareFhirStore#pubsub_topic}
        '''
        value = GoogleHealthcareFhirStoreNotificationConfig(pubsub_topic=pubsub_topic)

        return typing.cast(None, jsii.invoke(self, "putNotificationConfig", [value]))

    @jsii.member(jsii_name="putNotificationConfigs")
    def put_notification_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleHealthcareFhirStoreNotificationConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5770f6be787b96efcc6ee5dcae33017588b150e4a9b3669edf192df1bff5d885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNotificationConfigs", [value]))

    @jsii.member(jsii_name="putStreamConfigs")
    def put_stream_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleHealthcareFhirStoreStreamConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aec5c8bc9bbb332fb7d31725d062dc471a348eaab8adb585984c5efa8595e6d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStreamConfigs", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#create GoogleHealthcareFhirStore#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#delete GoogleHealthcareFhirStore#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#update GoogleHealthcareFhirStore#update}.
        '''
        value = GoogleHealthcareFhirStoreTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetComplexDataTypeReferenceParsing")
    def reset_complex_data_type_reference_parsing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComplexDataTypeReferenceParsing", []))

    @jsii.member(jsii_name="resetDefaultSearchHandlingStrict")
    def reset_default_search_handling_strict(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultSearchHandlingStrict", []))

    @jsii.member(jsii_name="resetDisableReferentialIntegrity")
    def reset_disable_referential_integrity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableReferentialIntegrity", []))

    @jsii.member(jsii_name="resetDisableResourceVersioning")
    def reset_disable_resource_versioning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableResourceVersioning", []))

    @jsii.member(jsii_name="resetEnableHistoryImport")
    def reset_enable_history_import(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableHistoryImport", []))

    @jsii.member(jsii_name="resetEnableHistoryModifications")
    def reset_enable_history_modifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableHistoryModifications", []))

    @jsii.member(jsii_name="resetEnableUpdateCreate")
    def reset_enable_update_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableUpdateCreate", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetNotificationConfig")
    def reset_notification_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationConfig", []))

    @jsii.member(jsii_name="resetNotificationConfigs")
    def reset_notification_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationConfigs", []))

    @jsii.member(jsii_name="resetStreamConfigs")
    def reset_stream_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStreamConfigs", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

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
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfig")
    def notification_config(
        self,
    ) -> "GoogleHealthcareFhirStoreNotificationConfigOutputReference":
        return typing.cast("GoogleHealthcareFhirStoreNotificationConfigOutputReference", jsii.get(self, "notificationConfig"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfigs")
    def notification_configs(
        self,
    ) -> "GoogleHealthcareFhirStoreNotificationConfigsList":
        return typing.cast("GoogleHealthcareFhirStoreNotificationConfigsList", jsii.get(self, "notificationConfigs"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="streamConfigs")
    def stream_configs(self) -> "GoogleHealthcareFhirStoreStreamConfigsList":
        return typing.cast("GoogleHealthcareFhirStoreStreamConfigsList", jsii.get(self, "streamConfigs"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleHealthcareFhirStoreTimeoutsOutputReference":
        return typing.cast("GoogleHealthcareFhirStoreTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="complexDataTypeReferenceParsingInput")
    def complex_data_type_reference_parsing_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "complexDataTypeReferenceParsingInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetInput")
    def dataset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultSearchHandlingStrictInput")
    def default_search_handling_strict_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultSearchHandlingStrictInput"))

    @builtins.property
    @jsii.member(jsii_name="disableReferentialIntegrityInput")
    def disable_referential_integrity_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableReferentialIntegrityInput"))

    @builtins.property
    @jsii.member(jsii_name="disableResourceVersioningInput")
    def disable_resource_versioning_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableResourceVersioningInput"))

    @builtins.property
    @jsii.member(jsii_name="enableHistoryImportInput")
    def enable_history_import_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableHistoryImportInput"))

    @builtins.property
    @jsii.member(jsii_name="enableHistoryModificationsInput")
    def enable_history_modifications_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableHistoryModificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="enableUpdateCreateInput")
    def enable_update_create_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableUpdateCreateInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfigInput")
    def notification_config_input(
        self,
    ) -> typing.Optional["GoogleHealthcareFhirStoreNotificationConfig"]:
        return typing.cast(typing.Optional["GoogleHealthcareFhirStoreNotificationConfig"], jsii.get(self, "notificationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfigsInput")
    def notification_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleHealthcareFhirStoreNotificationConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleHealthcareFhirStoreNotificationConfigs"]]], jsii.get(self, "notificationConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="streamConfigsInput")
    def stream_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleHealthcareFhirStoreStreamConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleHealthcareFhirStoreStreamConfigs"]]], jsii.get(self, "streamConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleHealthcareFhirStoreTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleHealthcareFhirStoreTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="complexDataTypeReferenceParsing")
    def complex_data_type_reference_parsing(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "complexDataTypeReferenceParsing"))

    @complex_data_type_reference_parsing.setter
    def complex_data_type_reference_parsing(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fe7762f2c0b0f5472db9903a22a31b2facb4cd2846fe6895241e08109d214b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "complexDataTypeReferenceParsing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataset")
    def dataset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataset"))

    @dataset.setter
    def dataset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__428782c3d2566184a9e4a5b38427d689eac48721e992f5845943a36b49ef6c69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultSearchHandlingStrict")
    def default_search_handling_strict(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultSearchHandlingStrict"))

    @default_search_handling_strict.setter
    def default_search_handling_strict(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9376dc9786d8bdf0d85143c354de79074428f19f614de04ce222b24ce9ab8ace)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSearchHandlingStrict", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableReferentialIntegrity")
    def disable_referential_integrity(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableReferentialIntegrity"))

    @disable_referential_integrity.setter
    def disable_referential_integrity(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59db1597c70995525de617cc475875c4b4498993372ca8e9c13e087b0deccac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableReferentialIntegrity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableResourceVersioning")
    def disable_resource_versioning(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableResourceVersioning"))

    @disable_resource_versioning.setter
    def disable_resource_versioning(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e966017be73a7a8d01a5d5532b21daf24f66ca896280c4f82a386f9aed395812)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableResourceVersioning", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableHistoryImport")
    def enable_history_import(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableHistoryImport"))

    @enable_history_import.setter
    def enable_history_import(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e856b9a0aa6a0cb796ea3d74b18c1d92ba2f3c16045cc5d4d39706fe4e0673c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableHistoryImport", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableHistoryModifications")
    def enable_history_modifications(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableHistoryModifications"))

    @enable_history_modifications.setter
    def enable_history_modifications(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27306b37740e3ff4a959e3637c8101906863d941388ee43c320569b05788581c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableHistoryModifications", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableUpdateCreate")
    def enable_update_create(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableUpdateCreate"))

    @enable_update_create.setter
    def enable_update_create(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9824c393ef16f572fc17eccfcb92b563c9ca601658e4b8f116c7fd2d6ed7e2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableUpdateCreate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3afe0ff6788f50288a655fc8dd27e782a6a610f46fef582c7d502af283d406d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c59e90688be40e67893ead627dfa62f41af01ca63b33f516ecb3492fc05bcef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0601508269ac66090169629ebd5789f2d4d56192a50dc6c4b26ff89d353c93e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a8af512c832c2b80aff67f25c3d0e53164ac07672e949a6bd4cb78ac45a8312)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleHealthcareFhirStore.GoogleHealthcareFhirStoreConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "dataset": "dataset",
        "name": "name",
        "complex_data_type_reference_parsing": "complexDataTypeReferenceParsing",
        "default_search_handling_strict": "defaultSearchHandlingStrict",
        "disable_referential_integrity": "disableReferentialIntegrity",
        "disable_resource_versioning": "disableResourceVersioning",
        "enable_history_import": "enableHistoryImport",
        "enable_history_modifications": "enableHistoryModifications",
        "enable_update_create": "enableUpdateCreate",
        "id": "id",
        "labels": "labels",
        "notification_config": "notificationConfig",
        "notification_configs": "notificationConfigs",
        "stream_configs": "streamConfigs",
        "timeouts": "timeouts",
        "version": "version",
    },
)
class GoogleHealthcareFhirStoreConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dataset: builtins.str,
        name: builtins.str,
        complex_data_type_reference_parsing: typing.Optional[builtins.str] = None,
        default_search_handling_strict: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_referential_integrity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_resource_versioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_history_import: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_history_modifications: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_update_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        notification_config: typing.Optional[typing.Union["GoogleHealthcareFhirStoreNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        notification_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleHealthcareFhirStoreNotificationConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stream_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleHealthcareFhirStoreStreamConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleHealthcareFhirStoreTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dataset: Identifies the dataset addressed by this request. Must be in the format 'projects/{project}/locations/{location}/datasets/{dataset}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#dataset GoogleHealthcareFhirStore#dataset}
        :param name: The resource name for the FhirStore. ** Changing this property may recreate the FHIR store (removing all data) ** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#name GoogleHealthcareFhirStore#name}
        :param complex_data_type_reference_parsing: Enable parsing of references within complex FHIR data types such as Extensions. If this value is set to ENABLED, then features like referential integrity and Bundle reference rewriting apply to all references. If this flag has not been specified the behavior of the FHIR store will not change, references in complex data types will not be parsed. New stores will have this value set to ENABLED by default after a notification period. Warning: turning on this flag causes processing existing resources to fail if they contain references to non-existent resources. Possible values: ["COMPLEX_DATA_TYPE_REFERENCE_PARSING_UNSPECIFIED", "DISABLED", "ENABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#complex_data_type_reference_parsing GoogleHealthcareFhirStore#complex_data_type_reference_parsing}
        :param default_search_handling_strict: If true, overrides the default search behavior for this FHIR store to handling=strict which returns an error for unrecognized search parameters. If false, uses the FHIR specification default handling=lenient which ignores unrecognized search parameters. The handling can always be changed from the default on an individual API call by setting the HTTP header Prefer: handling=strict or Prefer: handling=lenient. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#default_search_handling_strict GoogleHealthcareFhirStore#default_search_handling_strict}
        :param disable_referential_integrity: Whether to disable referential integrity in this FHIR store. This field is immutable after FHIR store creation. The default value is false, meaning that the API will enforce referential integrity and fail the requests that will result in inconsistent state in the FHIR store. When this field is set to true, the API will skip referential integrity check. Consequently, operations that rely on references, such as Patient.get$everything, will not return all the results if broken references exist. ** Changing this property may recreate the FHIR store (removing all data) ** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#disable_referential_integrity GoogleHealthcareFhirStore#disable_referential_integrity}
        :param disable_resource_versioning: Whether to disable resource versioning for this FHIR store. This field can not be changed after the creation of FHIR store. If set to false, which is the default behavior, all write operations will cause historical versions to be recorded automatically. The historical versions can be fetched through the history APIs, but cannot be updated. If set to true, no historical versions will be kept. The server will send back errors for attempts to read the historical versions. ** Changing this property may recreate the FHIR store (removing all data) ** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#disable_resource_versioning GoogleHealthcareFhirStore#disable_resource_versioning}
        :param enable_history_import: Whether to allow the bulk import API to accept history bundles and directly insert historical resource versions into the FHIR store. Importing resource histories creates resource interactions that appear to have occurred in the past, which clients may not want to allow. If set to false, history bundles within an import will fail with an error. ** Changing this property may recreate the FHIR store (removing all data) ** ** This property can be changed manually in the Google Cloud Healthcare admin console without recreating the FHIR store ** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#enable_history_import GoogleHealthcareFhirStore#enable_history_import}
        :param enable_history_modifications: Whether to allow the ExecuteBundle API to accept history bundles, and directly insert and overwrite historical resource versions into the FHIR store. If set to false, using history bundles fails with an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#enable_history_modifications GoogleHealthcareFhirStore#enable_history_modifications}
        :param enable_update_create: Whether this FHIR store has the updateCreate capability. This determines if the client can use an Update operation to create a new resource with a client-specified ID. If false, all IDs are server-assigned through the Create operation and attempts to Update a non-existent resource will return errors. Please treat the audit logs with appropriate levels of care if client-specified resource IDs contain sensitive data such as patient identifiers, those IDs will be part of the FHIR resource path recorded in Cloud audit logs and Cloud Pub/Sub notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#enable_update_create GoogleHealthcareFhirStore#enable_update_create}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#id GoogleHealthcareFhirStore#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-supplied key-value pairs used to organize FHIR stores. Label keys must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}][\\p{Ll}\\p{Lo}\\p{N}_-]{0,62} Label values are optional, must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}\\p{N}_-]{0,63} No more than 64 labels can be associated with a given store. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#labels GoogleHealthcareFhirStore#labels}
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#notification_config GoogleHealthcareFhirStore#notification_config}
        :param notification_configs: notification_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#notification_configs GoogleHealthcareFhirStore#notification_configs}
        :param stream_configs: stream_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#stream_configs GoogleHealthcareFhirStore#stream_configs}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#timeouts GoogleHealthcareFhirStore#timeouts}
        :param version: The FHIR specification version. Default value: "STU3" Possible values: ["DSTU2", "STU3", "R4"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#version GoogleHealthcareFhirStore#version}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(notification_config, dict):
            notification_config = GoogleHealthcareFhirStoreNotificationConfig(**notification_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleHealthcareFhirStoreTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6e3c0835e1646912e5ed454d22f97117b498284d2c4b97d3810a678c580e6c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument dataset", value=dataset, expected_type=type_hints["dataset"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument complex_data_type_reference_parsing", value=complex_data_type_reference_parsing, expected_type=type_hints["complex_data_type_reference_parsing"])
            check_type(argname="argument default_search_handling_strict", value=default_search_handling_strict, expected_type=type_hints["default_search_handling_strict"])
            check_type(argname="argument disable_referential_integrity", value=disable_referential_integrity, expected_type=type_hints["disable_referential_integrity"])
            check_type(argname="argument disable_resource_versioning", value=disable_resource_versioning, expected_type=type_hints["disable_resource_versioning"])
            check_type(argname="argument enable_history_import", value=enable_history_import, expected_type=type_hints["enable_history_import"])
            check_type(argname="argument enable_history_modifications", value=enable_history_modifications, expected_type=type_hints["enable_history_modifications"])
            check_type(argname="argument enable_update_create", value=enable_update_create, expected_type=type_hints["enable_update_create"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument notification_config", value=notification_config, expected_type=type_hints["notification_config"])
            check_type(argname="argument notification_configs", value=notification_configs, expected_type=type_hints["notification_configs"])
            check_type(argname="argument stream_configs", value=stream_configs, expected_type=type_hints["stream_configs"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset": dataset,
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
        if complex_data_type_reference_parsing is not None:
            self._values["complex_data_type_reference_parsing"] = complex_data_type_reference_parsing
        if default_search_handling_strict is not None:
            self._values["default_search_handling_strict"] = default_search_handling_strict
        if disable_referential_integrity is not None:
            self._values["disable_referential_integrity"] = disable_referential_integrity
        if disable_resource_versioning is not None:
            self._values["disable_resource_versioning"] = disable_resource_versioning
        if enable_history_import is not None:
            self._values["enable_history_import"] = enable_history_import
        if enable_history_modifications is not None:
            self._values["enable_history_modifications"] = enable_history_modifications
        if enable_update_create is not None:
            self._values["enable_update_create"] = enable_update_create
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if notification_config is not None:
            self._values["notification_config"] = notification_config
        if notification_configs is not None:
            self._values["notification_configs"] = notification_configs
        if stream_configs is not None:
            self._values["stream_configs"] = stream_configs
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if version is not None:
            self._values["version"] = version

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
    def dataset(self) -> builtins.str:
        '''Identifies the dataset addressed by this request. Must be in the format 'projects/{project}/locations/{location}/datasets/{dataset}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#dataset GoogleHealthcareFhirStore#dataset}
        '''
        result = self._values.get("dataset")
        assert result is not None, "Required property 'dataset' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The resource name for the FhirStore.

        ** Changing this property may recreate the FHIR store (removing all data) **

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#name GoogleHealthcareFhirStore#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def complex_data_type_reference_parsing(self) -> typing.Optional[builtins.str]:
        '''Enable parsing of references within complex FHIR data types such as Extensions.

        If this value is set to ENABLED, then features like referential integrity and Bundle reference rewriting apply to all references. If this flag has not been specified the behavior of the FHIR store will not change, references in complex data types will not be parsed. New stores will have this value set to ENABLED by default after a notification period. Warning: turning on this flag causes processing existing resources to fail if they contain references to non-existent resources. Possible values: ["COMPLEX_DATA_TYPE_REFERENCE_PARSING_UNSPECIFIED", "DISABLED", "ENABLED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#complex_data_type_reference_parsing GoogleHealthcareFhirStore#complex_data_type_reference_parsing}
        '''
        result = self._values.get("complex_data_type_reference_parsing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_search_handling_strict(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, overrides the default search behavior for this FHIR store to handling=strict which returns an error for unrecognized search parameters.

        If false, uses the FHIR specification default handling=lenient which ignores unrecognized search parameters.
        The handling can always be changed from the default on an individual API call by setting the HTTP header Prefer: handling=strict or Prefer: handling=lenient.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#default_search_handling_strict GoogleHealthcareFhirStore#default_search_handling_strict}
        '''
        result = self._values.get("default_search_handling_strict")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_referential_integrity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to disable referential integrity in this FHIR store.

        This field is immutable after FHIR store
        creation. The default value is false, meaning that the API will enforce referential integrity and fail the
        requests that will result in inconsistent state in the FHIR store. When this field is set to true, the API
        will skip referential integrity check. Consequently, operations that rely on references, such as
        Patient.get$everything, will not return all the results if broken references exist.

        ** Changing this property may recreate the FHIR store (removing all data) **

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#disable_referential_integrity GoogleHealthcareFhirStore#disable_referential_integrity}
        '''
        result = self._values.get("disable_referential_integrity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_resource_versioning(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to disable resource versioning for this FHIR store.

        This field can not be changed after the creation
        of FHIR store. If set to false, which is the default behavior, all write operations will cause historical
        versions to be recorded automatically. The historical versions can be fetched through the history APIs, but
        cannot be updated. If set to true, no historical versions will be kept. The server will send back errors for
        attempts to read the historical versions.

        ** Changing this property may recreate the FHIR store (removing all data) **

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#disable_resource_versioning GoogleHealthcareFhirStore#disable_resource_versioning}
        '''
        result = self._values.get("disable_resource_versioning")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_history_import(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to allow the bulk import API to accept history bundles and directly insert historical resource versions into the FHIR store.

        Importing resource histories creates resource interactions that appear to have
        occurred in the past, which clients may not want to allow. If set to false, history bundles within an import
        will fail with an error.

        ** Changing this property may recreate the FHIR store (removing all data) **

        ** This property can be changed manually in the Google Cloud Healthcare admin console without recreating the FHIR store **

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#enable_history_import GoogleHealthcareFhirStore#enable_history_import}
        '''
        result = self._values.get("enable_history_import")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_history_modifications(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to allow the ExecuteBundle API to accept history bundles, and directly insert and overwrite historical resource versions into the FHIR store.

        If set to false, using history bundles fails with an error.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#enable_history_modifications GoogleHealthcareFhirStore#enable_history_modifications}
        '''
        result = self._values.get("enable_history_modifications")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_update_create(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this FHIR store has the updateCreate capability.

        This determines if the client can use an Update
        operation to create a new resource with a client-specified ID. If false, all IDs are server-assigned through
        the Create operation and attempts to Update a non-existent resource will return errors. Please treat the audit
        logs with appropriate levels of care if client-specified resource IDs contain sensitive data such as patient
        identifiers, those IDs will be part of the FHIR resource path recorded in Cloud audit logs and Cloud Pub/Sub
        notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#enable_update_create GoogleHealthcareFhirStore#enable_update_create}
        '''
        result = self._values.get("enable_update_create")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#id GoogleHealthcareFhirStore#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-supplied key-value pairs used to organize FHIR stores.

        Label keys must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must
        conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}][\\p{Ll}\\p{Lo}\\p{N}_-]{0,62}

        Label values are optional, must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128
        bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}\\p{N}_-]{0,63}

        No more than 64 labels can be associated with a given store.

        An object containing a list of "key": value pairs.
        Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#labels GoogleHealthcareFhirStore#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def notification_config(
        self,
    ) -> typing.Optional["GoogleHealthcareFhirStoreNotificationConfig"]:
        '''notification_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#notification_config GoogleHealthcareFhirStore#notification_config}
        '''
        result = self._values.get("notification_config")
        return typing.cast(typing.Optional["GoogleHealthcareFhirStoreNotificationConfig"], result)

    @builtins.property
    def notification_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleHealthcareFhirStoreNotificationConfigs"]]]:
        '''notification_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#notification_configs GoogleHealthcareFhirStore#notification_configs}
        '''
        result = self._values.get("notification_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleHealthcareFhirStoreNotificationConfigs"]]], result)

    @builtins.property
    def stream_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleHealthcareFhirStoreStreamConfigs"]]]:
        '''stream_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#stream_configs GoogleHealthcareFhirStore#stream_configs}
        '''
        result = self._values.get("stream_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleHealthcareFhirStoreStreamConfigs"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleHealthcareFhirStoreTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#timeouts GoogleHealthcareFhirStore#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleHealthcareFhirStoreTimeouts"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The FHIR specification version. Default value: "STU3" Possible values: ["DSTU2", "STU3", "R4"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#version GoogleHealthcareFhirStore#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleHealthcareFhirStoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleHealthcareFhirStore.GoogleHealthcareFhirStoreNotificationConfig",
    jsii_struct_bases=[],
    name_mapping={"pubsub_topic": "pubsubTopic"},
)
class GoogleHealthcareFhirStoreNotificationConfig:
    def __init__(self, *, pubsub_topic: builtins.str) -> None:
        '''
        :param pubsub_topic: The Cloud Pub/Sub topic that notifications of changes are published on. Supplied by the client. PubsubMessage.Data will contain the resource name. PubsubMessage.MessageId is the ID of this message. It is guaranteed to be unique within the topic. PubsubMessage.PublishTime is the time at which the message was published. Notifications are only sent if the topic is non-empty. Topic names must be scoped to a project. service-PROJECT_NUMBER@gcp-sa-healthcare.iam.gserviceaccount.com must have publisher permissions on the given Cloud Pub/Sub topic. Not having adequate permissions will cause the calls that send notifications to fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#pubsub_topic GoogleHealthcareFhirStore#pubsub_topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa2a6eb41fe720976f758f7c0b32343315b98b90314db585ec2967e9001773af)
            check_type(argname="argument pubsub_topic", value=pubsub_topic, expected_type=type_hints["pubsub_topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pubsub_topic": pubsub_topic,
        }

    @builtins.property
    def pubsub_topic(self) -> builtins.str:
        '''The Cloud Pub/Sub topic that notifications of changes are published on.

        Supplied by the client.
        PubsubMessage.Data will contain the resource name. PubsubMessage.MessageId is the ID of this message.
        It is guaranteed to be unique within the topic. PubsubMessage.PublishTime is the time at which the message
        was published. Notifications are only sent if the topic is non-empty. Topic names must be scoped to a
        project. service-PROJECT_NUMBER@gcp-sa-healthcare.iam.gserviceaccount.com must have publisher permissions on the given
        Cloud Pub/Sub topic. Not having adequate permissions will cause the calls that send notifications to fail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#pubsub_topic GoogleHealthcareFhirStore#pubsub_topic}
        '''
        result = self._values.get("pubsub_topic")
        assert result is not None, "Required property 'pubsub_topic' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleHealthcareFhirStoreNotificationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleHealthcareFhirStoreNotificationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleHealthcareFhirStore.GoogleHealthcareFhirStoreNotificationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23599be3f9d44a902958bb05a71b1824d7cb9415500ccc440cdde53c4a40639a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="pubsubTopicInput")
    def pubsub_topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pubsubTopicInput"))

    @builtins.property
    @jsii.member(jsii_name="pubsubTopic")
    def pubsub_topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pubsubTopic"))

    @pubsub_topic.setter
    def pubsub_topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9c117cbba7b4e7a5e1a7a795c12412d6851513865697db37a5e105bebddc2ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pubsubTopic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleHealthcareFhirStoreNotificationConfig]:
        return typing.cast(typing.Optional[GoogleHealthcareFhirStoreNotificationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleHealthcareFhirStoreNotificationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79f5fef025b1d2f894fb268254fc2415888124dce797c3e3233debf3aa1bd460)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleHealthcareFhirStore.GoogleHealthcareFhirStoreNotificationConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "pubsub_topic": "pubsubTopic",
        "send_full_resource": "sendFullResource",
        "send_previous_resource_on_delete": "sendPreviousResourceOnDelete",
    },
)
class GoogleHealthcareFhirStoreNotificationConfigs:
    def __init__(
        self,
        *,
        pubsub_topic: builtins.str,
        send_full_resource: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_previous_resource_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param pubsub_topic: The Cloud Pub/Sub topic that notifications of changes are published on. Supplied by the client. PubsubMessage.Data will contain the resource name. PubsubMessage.MessageId is the ID of this message. It is guaranteed to be unique within the topic. PubsubMessage.PublishTime is the time at which the message was published. Notifications are only sent if the topic is non-empty. Topic names must be scoped to a project. service-PROJECT_NUMBER@gcp-sa-healthcare.iam.gserviceaccount.com must have publisher permissions on the given Cloud Pub/Sub topic. Not having adequate permissions will cause the calls that send notifications to fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#pubsub_topic GoogleHealthcareFhirStore#pubsub_topic}
        :param send_full_resource: Whether to send full FHIR resource to this Pub/Sub topic for Create and Update operation. Note that setting this to true does not guarantee that all resources will be sent in the format of full FHIR resource. When a resource change is too large or during heavy traffic, only the resource name will be sent. Clients should always check the "payloadType" label from a Pub/Sub message to determine whether it needs to fetch the full resource as a separate operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#send_full_resource GoogleHealthcareFhirStore#send_full_resource}
        :param send_previous_resource_on_delete: Whether to send full FHIR resource to this Pub/Sub topic for deleting FHIR resource. Note that setting this to true does not guarantee that all previous resources will be sent in the format of full FHIR resource. When a resource change is too large or during heavy traffic, only the resource name will be sent. Clients should always check the "payloadType" label from a Pub/Sub message to determine whether it needs to fetch the full previous resource as a separate operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#send_previous_resource_on_delete GoogleHealthcareFhirStore#send_previous_resource_on_delete}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d09de8448e55ecc9dfa523dec1bde844b7631ef38511c60924ac37ff615b0d0f)
            check_type(argname="argument pubsub_topic", value=pubsub_topic, expected_type=type_hints["pubsub_topic"])
            check_type(argname="argument send_full_resource", value=send_full_resource, expected_type=type_hints["send_full_resource"])
            check_type(argname="argument send_previous_resource_on_delete", value=send_previous_resource_on_delete, expected_type=type_hints["send_previous_resource_on_delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pubsub_topic": pubsub_topic,
        }
        if send_full_resource is not None:
            self._values["send_full_resource"] = send_full_resource
        if send_previous_resource_on_delete is not None:
            self._values["send_previous_resource_on_delete"] = send_previous_resource_on_delete

    @builtins.property
    def pubsub_topic(self) -> builtins.str:
        '''The Cloud Pub/Sub topic that notifications of changes are published on.

        Supplied by the client.
        PubsubMessage.Data will contain the resource name. PubsubMessage.MessageId is the ID of this message.
        It is guaranteed to be unique within the topic. PubsubMessage.PublishTime is the time at which the message
        was published. Notifications are only sent if the topic is non-empty. Topic names must be scoped to a
        project. service-PROJECT_NUMBER@gcp-sa-healthcare.iam.gserviceaccount.com must have publisher permissions on the given
        Cloud Pub/Sub topic. Not having adequate permissions will cause the calls that send notifications to fail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#pubsub_topic GoogleHealthcareFhirStore#pubsub_topic}
        '''
        result = self._values.get("pubsub_topic")
        assert result is not None, "Required property 'pubsub_topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def send_full_resource(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to send full FHIR resource to this Pub/Sub topic for Create and Update operation.

        Note that setting this to true does not guarantee that all resources will be sent in the format of
        full FHIR resource. When a resource change is too large or during heavy traffic, only the resource name will be
        sent. Clients should always check the "payloadType" label from a Pub/Sub message to determine whether
        it needs to fetch the full resource as a separate operation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#send_full_resource GoogleHealthcareFhirStore#send_full_resource}
        '''
        result = self._values.get("send_full_resource")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def send_previous_resource_on_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to send full FHIR resource to this Pub/Sub topic for deleting FHIR resource.

        Note that setting this to
        true does not guarantee that all previous resources will be sent in the format of full FHIR resource. When a
        resource change is too large or during heavy traffic, only the resource name will be sent. Clients should always
        check the "payloadType" label from a Pub/Sub message to determine whether it needs to fetch the full previous
        resource as a separate operation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#send_previous_resource_on_delete GoogleHealthcareFhirStore#send_previous_resource_on_delete}
        '''
        result = self._values.get("send_previous_resource_on_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleHealthcareFhirStoreNotificationConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleHealthcareFhirStoreNotificationConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleHealthcareFhirStore.GoogleHealthcareFhirStoreNotificationConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a1848289324f2ce9875762a72cbdcde5413df5d5101df6b62defd4178edd9e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleHealthcareFhirStoreNotificationConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84bace3c26f32024683f6b34b85435a92c036fb87d3eaa1d714cbda3c171eb81)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleHealthcareFhirStoreNotificationConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db75add1343f2dc39a18ca4ed6b892b5294cc2de7348aed3afc13f220b393a66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__864eb75b5657348ff86a99535db5daeaaef09cc9075fa0b0295f4338b82664a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ef073ecbd32317df926c9920907aa6d929cf96ea1a510e36ec5c667060bff75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleHealthcareFhirStoreNotificationConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleHealthcareFhirStoreNotificationConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleHealthcareFhirStoreNotificationConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6273f1b8c31db99a5d2da52504eecf1440ffe7afff88019963f4a1f7e08df8db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleHealthcareFhirStoreNotificationConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleHealthcareFhirStore.GoogleHealthcareFhirStoreNotificationConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a4821bcd371c086de5a3ee5544833007d8dba9aba2e9595b87b7fe52fb4ea6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSendFullResource")
    def reset_send_full_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendFullResource", []))

    @jsii.member(jsii_name="resetSendPreviousResourceOnDelete")
    def reset_send_previous_resource_on_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendPreviousResourceOnDelete", []))

    @builtins.property
    @jsii.member(jsii_name="pubsubTopicInput")
    def pubsub_topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pubsubTopicInput"))

    @builtins.property
    @jsii.member(jsii_name="sendFullResourceInput")
    def send_full_resource_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendFullResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="sendPreviousResourceOnDeleteInput")
    def send_previous_resource_on_delete_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendPreviousResourceOnDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="pubsubTopic")
    def pubsub_topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pubsubTopic"))

    @pubsub_topic.setter
    def pubsub_topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264c527cc231bcdfece6882475bb297c179e4748cb419f2a468d8e8335dd38d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pubsubTopic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sendFullResource")
    def send_full_resource(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendFullResource"))

    @send_full_resource.setter
    def send_full_resource(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb3d3eed0875b94ed263aab9124ccc02f4b21a7f819023b93321b2b68245d97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendFullResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sendPreviousResourceOnDelete")
    def send_previous_resource_on_delete(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendPreviousResourceOnDelete"))

    @send_previous_resource_on_delete.setter
    def send_previous_resource_on_delete(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4081e2765f85104e74df58ea598818b6042807d53744f704593ea8cadfd2c38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendPreviousResourceOnDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleHealthcareFhirStoreNotificationConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleHealthcareFhirStoreNotificationConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleHealthcareFhirStoreNotificationConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d19acd25fb72aad69fe0ff249e0df09259d3ecfc62d2a10c43ac64ae3c0b41c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleHealthcareFhirStore.GoogleHealthcareFhirStoreStreamConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "bigquery_destination": "bigqueryDestination",
        "resource_types": "resourceTypes",
    },
)
class GoogleHealthcareFhirStoreStreamConfigs:
    def __init__(
        self,
        *,
        bigquery_destination: typing.Union["GoogleHealthcareFhirStoreStreamConfigsBigqueryDestination", typing.Dict[builtins.str, typing.Any]],
        resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param bigquery_destination: bigquery_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#bigquery_destination GoogleHealthcareFhirStore#bigquery_destination}
        :param resource_types: Supply a FHIR resource type (such as "Patient" or "Observation"). See https://www.hl7.org/fhir/valueset-resource-types.html for a list of all FHIR resource types. The server treats an empty list as an intent to stream all the supported resource types in this FHIR store. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#resource_types GoogleHealthcareFhirStore#resource_types}
        '''
        if isinstance(bigquery_destination, dict):
            bigquery_destination = GoogleHealthcareFhirStoreStreamConfigsBigqueryDestination(**bigquery_destination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eec61991b3f508f18666c46f444b19e9dd1fd2f368a5d7c110f29883cc17c93a)
            check_type(argname="argument bigquery_destination", value=bigquery_destination, expected_type=type_hints["bigquery_destination"])
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bigquery_destination": bigquery_destination,
        }
        if resource_types is not None:
            self._values["resource_types"] = resource_types

    @builtins.property
    def bigquery_destination(
        self,
    ) -> "GoogleHealthcareFhirStoreStreamConfigsBigqueryDestination":
        '''bigquery_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#bigquery_destination GoogleHealthcareFhirStore#bigquery_destination}
        '''
        result = self._values.get("bigquery_destination")
        assert result is not None, "Required property 'bigquery_destination' is missing"
        return typing.cast("GoogleHealthcareFhirStoreStreamConfigsBigqueryDestination", result)

    @builtins.property
    def resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Supply a FHIR resource type (such as "Patient" or "Observation").

        See
        https://www.hl7.org/fhir/valueset-resource-types.html for a list of all FHIR resource types. The server treats
        an empty list as an intent to stream all the supported resource types in this FHIR store.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#resource_types GoogleHealthcareFhirStore#resource_types}
        '''
        result = self._values.get("resource_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleHealthcareFhirStoreStreamConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleHealthcareFhirStore.GoogleHealthcareFhirStoreStreamConfigsBigqueryDestination",
    jsii_struct_bases=[],
    name_mapping={"dataset_uri": "datasetUri", "schema_config": "schemaConfig"},
)
class GoogleHealthcareFhirStoreStreamConfigsBigqueryDestination:
    def __init__(
        self,
        *,
        dataset_uri: builtins.str,
        schema_config: typing.Union["GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param dataset_uri: BigQuery URI to a dataset, up to 2000 characters long, in the format bq://projectId.bqDatasetId. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#dataset_uri GoogleHealthcareFhirStore#dataset_uri}
        :param schema_config: schema_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#schema_config GoogleHealthcareFhirStore#schema_config}
        '''
        if isinstance(schema_config, dict):
            schema_config = GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig(**schema_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8fc21b4ea053902ace2f955ac800fde01812ab5f145d20846ff855488b4b814)
            check_type(argname="argument dataset_uri", value=dataset_uri, expected_type=type_hints["dataset_uri"])
            check_type(argname="argument schema_config", value=schema_config, expected_type=type_hints["schema_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_uri": dataset_uri,
            "schema_config": schema_config,
        }

    @builtins.property
    def dataset_uri(self) -> builtins.str:
        '''BigQuery URI to a dataset, up to 2000 characters long, in the format bq://projectId.bqDatasetId.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#dataset_uri GoogleHealthcareFhirStore#dataset_uri}
        '''
        result = self._values.get("dataset_uri")
        assert result is not None, "Required property 'dataset_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema_config(
        self,
    ) -> "GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig":
        '''schema_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#schema_config GoogleHealthcareFhirStore#schema_config}
        '''
        result = self._values.get("schema_config")
        assert result is not None, "Required property 'schema_config' is missing"
        return typing.cast("GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleHealthcareFhirStoreStreamConfigsBigqueryDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleHealthcareFhirStore.GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ed602c6de318908c7c4aeeb97b17fa3ee446cfc8c33e4fcc5d43a50b44d5f46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSchemaConfig")
    def put_schema_config(
        self,
        *,
        recursive_structure_depth: jsii.Number,
        last_updated_partition_config: typing.Optional[typing.Union["GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        schema_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param recursive_structure_depth: The depth for all recursive structures in the output analytics schema. For example, concept in the CodeSystem resource is a recursive structure; when the depth is 2, the CodeSystem table will have a column called concept.concept but not concept.concept.concept. If not specified or set to 0, the server will use the default value 2. The maximum depth allowed is 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#recursive_structure_depth GoogleHealthcareFhirStore#recursive_structure_depth}
        :param last_updated_partition_config: last_updated_partition_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#last_updated_partition_config GoogleHealthcareFhirStore#last_updated_partition_config}
        :param schema_type: Specifies the output schema type. - ANALYTICS: Analytics schema defined by the FHIR community. See https://github.com/FHIR/sql-on-fhir/blob/master/sql-on-fhir.md. - ANALYTICS_V2: Analytics V2, similar to schema defined by the FHIR community, with added support for extensions with one or more occurrences and contained resources in stringified JSON. - LOSSLESS: A data-driven schema generated from the fields present in the FHIR data being exported, with no additional simplification. Default value: "ANALYTICS" Possible values: ["ANALYTICS", "ANALYTICS_V2", "LOSSLESS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#schema_type GoogleHealthcareFhirStore#schema_type}
        '''
        value = GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig(
            recursive_structure_depth=recursive_structure_depth,
            last_updated_partition_config=last_updated_partition_config,
            schema_type=schema_type,
        )

        return typing.cast(None, jsii.invoke(self, "putSchemaConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="schemaConfig")
    def schema_config(
        self,
    ) -> "GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigOutputReference":
        return typing.cast("GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigOutputReference", jsii.get(self, "schemaConfig"))

    @builtins.property
    @jsii.member(jsii_name="datasetUriInput")
    def dataset_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetUriInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaConfigInput")
    def schema_config_input(
        self,
    ) -> typing.Optional["GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig"]:
        return typing.cast(typing.Optional["GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig"], jsii.get(self, "schemaConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetUri")
    def dataset_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetUri"))

    @dataset_uri.setter
    def dataset_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36c39c528d712841542fb96b037206b164c9edcf1b224520cd975f542de25e3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleHealthcareFhirStoreStreamConfigsBigqueryDestination]:
        return typing.cast(typing.Optional[GoogleHealthcareFhirStoreStreamConfigsBigqueryDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleHealthcareFhirStoreStreamConfigsBigqueryDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42971fcf21904ec09dccdf88b31950d7f15914cae3cbbeef73a91cc141eab700)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleHealthcareFhirStore.GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig",
    jsii_struct_bases=[],
    name_mapping={
        "recursive_structure_depth": "recursiveStructureDepth",
        "last_updated_partition_config": "lastUpdatedPartitionConfig",
        "schema_type": "schemaType",
    },
)
class GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig:
    def __init__(
        self,
        *,
        recursive_structure_depth: jsii.Number,
        last_updated_partition_config: typing.Optional[typing.Union["GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        schema_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param recursive_structure_depth: The depth for all recursive structures in the output analytics schema. For example, concept in the CodeSystem resource is a recursive structure; when the depth is 2, the CodeSystem table will have a column called concept.concept but not concept.concept.concept. If not specified or set to 0, the server will use the default value 2. The maximum depth allowed is 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#recursive_structure_depth GoogleHealthcareFhirStore#recursive_structure_depth}
        :param last_updated_partition_config: last_updated_partition_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#last_updated_partition_config GoogleHealthcareFhirStore#last_updated_partition_config}
        :param schema_type: Specifies the output schema type. - ANALYTICS: Analytics schema defined by the FHIR community. See https://github.com/FHIR/sql-on-fhir/blob/master/sql-on-fhir.md. - ANALYTICS_V2: Analytics V2, similar to schema defined by the FHIR community, with added support for extensions with one or more occurrences and contained resources in stringified JSON. - LOSSLESS: A data-driven schema generated from the fields present in the FHIR data being exported, with no additional simplification. Default value: "ANALYTICS" Possible values: ["ANALYTICS", "ANALYTICS_V2", "LOSSLESS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#schema_type GoogleHealthcareFhirStore#schema_type}
        '''
        if isinstance(last_updated_partition_config, dict):
            last_updated_partition_config = GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig(**last_updated_partition_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2804ae20c8318cc02c1e3264c82f23e1cf422575753444c72560474ce3023e9)
            check_type(argname="argument recursive_structure_depth", value=recursive_structure_depth, expected_type=type_hints["recursive_structure_depth"])
            check_type(argname="argument last_updated_partition_config", value=last_updated_partition_config, expected_type=type_hints["last_updated_partition_config"])
            check_type(argname="argument schema_type", value=schema_type, expected_type=type_hints["schema_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "recursive_structure_depth": recursive_structure_depth,
        }
        if last_updated_partition_config is not None:
            self._values["last_updated_partition_config"] = last_updated_partition_config
        if schema_type is not None:
            self._values["schema_type"] = schema_type

    @builtins.property
    def recursive_structure_depth(self) -> jsii.Number:
        '''The depth for all recursive structures in the output analytics schema.

        For example, concept in the CodeSystem
        resource is a recursive structure; when the depth is 2, the CodeSystem table will have a column called
        concept.concept but not concept.concept.concept. If not specified or set to 0, the server will use the default
        value 2. The maximum depth allowed is 5.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#recursive_structure_depth GoogleHealthcareFhirStore#recursive_structure_depth}
        '''
        result = self._values.get("recursive_structure_depth")
        assert result is not None, "Required property 'recursive_structure_depth' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def last_updated_partition_config(
        self,
    ) -> typing.Optional["GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig"]:
        '''last_updated_partition_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#last_updated_partition_config GoogleHealthcareFhirStore#last_updated_partition_config}
        '''
        result = self._values.get("last_updated_partition_config")
        return typing.cast(typing.Optional["GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig"], result)

    @builtins.property
    def schema_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the output schema type.

        - ANALYTICS: Analytics schema defined by the FHIR community.
          See https://github.com/FHIR/sql-on-fhir/blob/master/sql-on-fhir.md.
        - ANALYTICS_V2: Analytics V2, similar to schema defined by the FHIR community, with added support for extensions with one or more occurrences and contained resources in stringified JSON.
        - LOSSLESS: A data-driven schema generated from the fields present in the FHIR data being exported, with no additional simplification. Default value: "ANALYTICS" Possible values: ["ANALYTICS", "ANALYTICS_V2", "LOSSLESS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#schema_type GoogleHealthcareFhirStore#schema_type}
        '''
        result = self._values.get("schema_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleHealthcareFhirStore.GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "expiration_ms": "expirationMs"},
)
class GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig:
    def __init__(
        self,
        *,
        type: builtins.str,
        expiration_ms: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of partitioning. Possible values: ["PARTITION_TYPE_UNSPECIFIED", "HOUR", "DAY", "MONTH", "YEAR"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#type GoogleHealthcareFhirStore#type}
        :param expiration_ms: Number of milliseconds for which to keep the storage for a partition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#expiration_ms GoogleHealthcareFhirStore#expiration_ms}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a62454b318bb0e1597d14514a60132177267d5d0760e21bce05e2249998f17c)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument expiration_ms", value=expiration_ms, expected_type=type_hints["expiration_ms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if expiration_ms is not None:
            self._values["expiration_ms"] = expiration_ms

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of partitioning. Possible values: ["PARTITION_TYPE_UNSPECIFIED", "HOUR", "DAY", "MONTH", "YEAR"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#type GoogleHealthcareFhirStore#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expiration_ms(self) -> typing.Optional[builtins.str]:
        '''Number of milliseconds for which to keep the storage for a partition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#expiration_ms GoogleHealthcareFhirStore#expiration_ms}
        '''
        result = self._values.get("expiration_ms")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleHealthcareFhirStore.GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac59fa5dbd5245397ed1068efd8491eaaa8fe316d1f16ada6f7e6a91d4435b07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExpirationMs")
    def reset_expiration_ms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationMs", []))

    @builtins.property
    @jsii.member(jsii_name="expirationMsInput")
    def expiration_ms_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expirationMsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationMs")
    def expiration_ms(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expirationMs"))

    @expiration_ms.setter
    def expiration_ms(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f3d78661f725e7718b44276e7129a744ba7a29043a6af50f20264b0040d7841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationMs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5ae2d30341086d819398671c618da4bef07bb882d454b921460b9c3e3d7d2f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig]:
        return typing.cast(typing.Optional[GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c597ce3ec81385c99bfea35853bc863e4d3209b6bb4c97879ea5c6ab42d6a25b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleHealthcareFhirStore.GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f80ef40a07856d84951ced7beba742af72a99a049a2201cc5e617627f1cf4c0c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLastUpdatedPartitionConfig")
    def put_last_updated_partition_config(
        self,
        *,
        type: builtins.str,
        expiration_ms: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of partitioning. Possible values: ["PARTITION_TYPE_UNSPECIFIED", "HOUR", "DAY", "MONTH", "YEAR"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#type GoogleHealthcareFhirStore#type}
        :param expiration_ms: Number of milliseconds for which to keep the storage for a partition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#expiration_ms GoogleHealthcareFhirStore#expiration_ms}
        '''
        value = GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig(
            type=type, expiration_ms=expiration_ms
        )

        return typing.cast(None, jsii.invoke(self, "putLastUpdatedPartitionConfig", [value]))

    @jsii.member(jsii_name="resetLastUpdatedPartitionConfig")
    def reset_last_updated_partition_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastUpdatedPartitionConfig", []))

    @jsii.member(jsii_name="resetSchemaType")
    def reset_schema_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaType", []))

    @builtins.property
    @jsii.member(jsii_name="lastUpdatedPartitionConfig")
    def last_updated_partition_config(
        self,
    ) -> GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfigOutputReference:
        return typing.cast(GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfigOutputReference, jsii.get(self, "lastUpdatedPartitionConfig"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdatedPartitionConfigInput")
    def last_updated_partition_config_input(
        self,
    ) -> typing.Optional[GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig]:
        return typing.cast(typing.Optional[GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig], jsii.get(self, "lastUpdatedPartitionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="recursiveStructureDepthInput")
    def recursive_structure_depth_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "recursiveStructureDepthInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaTypeInput")
    def schema_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="recursiveStructureDepth")
    def recursive_structure_depth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "recursiveStructureDepth"))

    @recursive_structure_depth.setter
    def recursive_structure_depth(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__924bad65e18f1c91d183b630b43e44f8f4f9cea3ba259c0b4a39d8b508fe2b18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recursiveStructureDepth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schemaType")
    def schema_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaType"))

    @schema_type.setter
    def schema_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f5ab9917d6c57c00418369a0355fb5aee2de474aa1dc25bcab1009f0f5c3a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig]:
        return typing.cast(typing.Optional[GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__667a11d4bc53680117ba3016ffbe0639ffdd40e97f3f25fa3bc8fd1d76bab5c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleHealthcareFhirStoreStreamConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleHealthcareFhirStore.GoogleHealthcareFhirStoreStreamConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__132a4e3fd332add00b9874c09822fad6e37d0e8c5e2bbdae1ac3af4efbab5cac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleHealthcareFhirStoreStreamConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aeb8b9c8d3f783b19592542405da781c40555256bfe06ea7db94aef9472e8c0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleHealthcareFhirStoreStreamConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a909df2372a7d1c27805df149d899ec61ba0c651a62784b2e755c0f8e671f26)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22f6c1e154f9718008c510200398fec59600daaf2774b075eaab4e394d68f2bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__edeea906e741d86b29ec3367fd5e3243484386a713fddad81ab09c5905d9bab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleHealthcareFhirStoreStreamConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleHealthcareFhirStoreStreamConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleHealthcareFhirStoreStreamConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dda862590beb3516daa53ccdb3ab961f24d14daad32fb6e325b505170957b2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleHealthcareFhirStoreStreamConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleHealthcareFhirStore.GoogleHealthcareFhirStoreStreamConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9491d997202a6e64545c849cfd8aa27c492fbbef0488a8668df4839483beb6a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putBigqueryDestination")
    def put_bigquery_destination(
        self,
        *,
        dataset_uri: builtins.str,
        schema_config: typing.Union[GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param dataset_uri: BigQuery URI to a dataset, up to 2000 characters long, in the format bq://projectId.bqDatasetId. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#dataset_uri GoogleHealthcareFhirStore#dataset_uri}
        :param schema_config: schema_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#schema_config GoogleHealthcareFhirStore#schema_config}
        '''
        value = GoogleHealthcareFhirStoreStreamConfigsBigqueryDestination(
            dataset_uri=dataset_uri, schema_config=schema_config
        )

        return typing.cast(None, jsii.invoke(self, "putBigqueryDestination", [value]))

    @jsii.member(jsii_name="resetResourceTypes")
    def reset_resource_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTypes", []))

    @builtins.property
    @jsii.member(jsii_name="bigqueryDestination")
    def bigquery_destination(
        self,
    ) -> GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationOutputReference:
        return typing.cast(GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationOutputReference, jsii.get(self, "bigqueryDestination"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryDestinationInput")
    def bigquery_destination_input(
        self,
    ) -> typing.Optional[GoogleHealthcareFhirStoreStreamConfigsBigqueryDestination]:
        return typing.cast(typing.Optional[GoogleHealthcareFhirStoreStreamConfigsBigqueryDestination], jsii.get(self, "bigqueryDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypesInput")
    def resource_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypes")
    def resource_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypes"))

    @resource_types.setter
    def resource_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4002a092ea55eab7a080c35546298ef543a07792c2e3f16a78e4fa708c37c02d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleHealthcareFhirStoreStreamConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleHealthcareFhirStoreStreamConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleHealthcareFhirStoreStreamConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a672f1b37e79c200fec775194d3d3613c7ec0cf354d7d39ce6b576dc1be0bbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleHealthcareFhirStore.GoogleHealthcareFhirStoreTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleHealthcareFhirStoreTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#create GoogleHealthcareFhirStore#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#delete GoogleHealthcareFhirStore#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#update GoogleHealthcareFhirStore#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35bfa6d9c2308fa6fe1fbd1d204b6e91fc96548165dfe5140cf316764d045624)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#create GoogleHealthcareFhirStore#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#delete GoogleHealthcareFhirStore#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_fhir_store#update GoogleHealthcareFhirStore#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleHealthcareFhirStoreTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleHealthcareFhirStoreTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleHealthcareFhirStore.GoogleHealthcareFhirStoreTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__184568de902183a536dc4e974c5370f9b991fe15fe122307790ebc35eda74aaf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f1ee2a9106ca1b5946b31e201caf7eb7765164d171e0746f8c22e3dc2039d2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d70b30fa01413fb2aa81c2efd802b39b3ac5f1a0f941dfd1eba7da710f70e69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__670b4cf293821b85e8bc9b5c94c152f467d82a8ac87993484b15c96dfeb023de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleHealthcareFhirStoreTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleHealthcareFhirStoreTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleHealthcareFhirStoreTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8181bca9684673be863bcc22321861cc1fff97aa9a08e8b824929df8117ffa10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleHealthcareFhirStore",
    "GoogleHealthcareFhirStoreConfig",
    "GoogleHealthcareFhirStoreNotificationConfig",
    "GoogleHealthcareFhirStoreNotificationConfigOutputReference",
    "GoogleHealthcareFhirStoreNotificationConfigs",
    "GoogleHealthcareFhirStoreNotificationConfigsList",
    "GoogleHealthcareFhirStoreNotificationConfigsOutputReference",
    "GoogleHealthcareFhirStoreStreamConfigs",
    "GoogleHealthcareFhirStoreStreamConfigsBigqueryDestination",
    "GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationOutputReference",
    "GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig",
    "GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig",
    "GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfigOutputReference",
    "GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigOutputReference",
    "GoogleHealthcareFhirStoreStreamConfigsList",
    "GoogleHealthcareFhirStoreStreamConfigsOutputReference",
    "GoogleHealthcareFhirStoreTimeouts",
    "GoogleHealthcareFhirStoreTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ae585ad673345dc2da8b741cbc4186a7adfdbff61a7ce36dcb26beef5a95d713(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dataset: builtins.str,
    name: builtins.str,
    complex_data_type_reference_parsing: typing.Optional[builtins.str] = None,
    default_search_handling_strict: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_referential_integrity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_resource_versioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_history_import: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_history_modifications: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_update_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    notification_config: typing.Optional[typing.Union[GoogleHealthcareFhirStoreNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    notification_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleHealthcareFhirStoreNotificationConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stream_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleHealthcareFhirStoreStreamConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleHealthcareFhirStoreTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__bdf166323eae5564485002f095a97dcbd333fba4f4fe7ce91c8690ce4efba68e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5770f6be787b96efcc6ee5dcae33017588b150e4a9b3669edf192df1bff5d885(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleHealthcareFhirStoreNotificationConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec5c8bc9bbb332fb7d31725d062dc471a348eaab8adb585984c5efa8595e6d8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleHealthcareFhirStoreStreamConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe7762f2c0b0f5472db9903a22a31b2facb4cd2846fe6895241e08109d214b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428782c3d2566184a9e4a5b38427d689eac48721e992f5845943a36b49ef6c69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9376dc9786d8bdf0d85143c354de79074428f19f614de04ce222b24ce9ab8ace(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59db1597c70995525de617cc475875c4b4498993372ca8e9c13e087b0deccac6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e966017be73a7a8d01a5d5532b21daf24f66ca896280c4f82a386f9aed395812(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e856b9a0aa6a0cb796ea3d74b18c1d92ba2f3c16045cc5d4d39706fe4e0673c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27306b37740e3ff4a959e3637c8101906863d941388ee43c320569b05788581c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9824c393ef16f572fc17eccfcb92b563c9ca601658e4b8f116c7fd2d6ed7e2d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3afe0ff6788f50288a655fc8dd27e782a6a610f46fef582c7d502af283d406d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c59e90688be40e67893ead627dfa62f41af01ca63b33f516ecb3492fc05bcef(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0601508269ac66090169629ebd5789f2d4d56192a50dc6c4b26ff89d353c93e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a8af512c832c2b80aff67f25c3d0e53164ac07672e949a6bd4cb78ac45a8312(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6e3c0835e1646912e5ed454d22f97117b498284d2c4b97d3810a678c580e6c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dataset: builtins.str,
    name: builtins.str,
    complex_data_type_reference_parsing: typing.Optional[builtins.str] = None,
    default_search_handling_strict: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_referential_integrity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_resource_versioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_history_import: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_history_modifications: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_update_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    notification_config: typing.Optional[typing.Union[GoogleHealthcareFhirStoreNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    notification_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleHealthcareFhirStoreNotificationConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stream_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleHealthcareFhirStoreStreamConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleHealthcareFhirStoreTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa2a6eb41fe720976f758f7c0b32343315b98b90314db585ec2967e9001773af(
    *,
    pubsub_topic: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23599be3f9d44a902958bb05a71b1824d7cb9415500ccc440cdde53c4a40639a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c117cbba7b4e7a5e1a7a795c12412d6851513865697db37a5e105bebddc2ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f5fef025b1d2f894fb268254fc2415888124dce797c3e3233debf3aa1bd460(
    value: typing.Optional[GoogleHealthcareFhirStoreNotificationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d09de8448e55ecc9dfa523dec1bde844b7631ef38511c60924ac37ff615b0d0f(
    *,
    pubsub_topic: builtins.str,
    send_full_resource: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    send_previous_resource_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a1848289324f2ce9875762a72cbdcde5413df5d5101df6b62defd4178edd9e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84bace3c26f32024683f6b34b85435a92c036fb87d3eaa1d714cbda3c171eb81(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db75add1343f2dc39a18ca4ed6b892b5294cc2de7348aed3afc13f220b393a66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864eb75b5657348ff86a99535db5daeaaef09cc9075fa0b0295f4338b82664a4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ef073ecbd32317df926c9920907aa6d929cf96ea1a510e36ec5c667060bff75(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6273f1b8c31db99a5d2da52504eecf1440ffe7afff88019963f4a1f7e08df8db(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleHealthcareFhirStoreNotificationConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4821bcd371c086de5a3ee5544833007d8dba9aba2e9595b87b7fe52fb4ea6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264c527cc231bcdfece6882475bb297c179e4748cb419f2a468d8e8335dd38d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb3d3eed0875b94ed263aab9124ccc02f4b21a7f819023b93321b2b68245d97(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4081e2765f85104e74df58ea598818b6042807d53744f704593ea8cadfd2c38(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19acd25fb72aad69fe0ff249e0df09259d3ecfc62d2a10c43ac64ae3c0b41c0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleHealthcareFhirStoreNotificationConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec61991b3f508f18666c46f444b19e9dd1fd2f368a5d7c110f29883cc17c93a(
    *,
    bigquery_destination: typing.Union[GoogleHealthcareFhirStoreStreamConfigsBigqueryDestination, typing.Dict[builtins.str, typing.Any]],
    resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8fc21b4ea053902ace2f955ac800fde01812ab5f145d20846ff855488b4b814(
    *,
    dataset_uri: builtins.str,
    schema_config: typing.Union[GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed602c6de318908c7c4aeeb97b17fa3ee446cfc8c33e4fcc5d43a50b44d5f46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c39c528d712841542fb96b037206b164c9edcf1b224520cd975f542de25e3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42971fcf21904ec09dccdf88b31950d7f15914cae3cbbeef73a91cc141eab700(
    value: typing.Optional[GoogleHealthcareFhirStoreStreamConfigsBigqueryDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2804ae20c8318cc02c1e3264c82f23e1cf422575753444c72560474ce3023e9(
    *,
    recursive_structure_depth: jsii.Number,
    last_updated_partition_config: typing.Optional[typing.Union[GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    schema_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a62454b318bb0e1597d14514a60132177267d5d0760e21bce05e2249998f17c(
    *,
    type: builtins.str,
    expiration_ms: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac59fa5dbd5245397ed1068efd8491eaaa8fe316d1f16ada6f7e6a91d4435b07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f3d78661f725e7718b44276e7129a744ba7a29043a6af50f20264b0040d7841(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ae2d30341086d819398671c618da4bef07bb882d454b921460b9c3e3d7d2f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c597ce3ec81385c99bfea35853bc863e4d3209b6bb4c97879ea5c6ab42d6a25b(
    value: typing.Optional[GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f80ef40a07856d84951ced7beba742af72a99a049a2201cc5e617627f1cf4c0c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924bad65e18f1c91d183b630b43e44f8f4f9cea3ba259c0b4a39d8b508fe2b18(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f5ab9917d6c57c00418369a0355fb5aee2de474aa1dc25bcab1009f0f5c3a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__667a11d4bc53680117ba3016ffbe0639ffdd40e97f3f25fa3bc8fd1d76bab5c1(
    value: typing.Optional[GoogleHealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__132a4e3fd332add00b9874c09822fad6e37d0e8c5e2bbdae1ac3af4efbab5cac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aeb8b9c8d3f783b19592542405da781c40555256bfe06ea7db94aef9472e8c0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a909df2372a7d1c27805df149d899ec61ba0c651a62784b2e755c0f8e671f26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f6c1e154f9718008c510200398fec59600daaf2774b075eaab4e394d68f2bb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edeea906e741d86b29ec3367fd5e3243484386a713fddad81ab09c5905d9bab2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dda862590beb3516daa53ccdb3ab961f24d14daad32fb6e325b505170957b2b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleHealthcareFhirStoreStreamConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9491d997202a6e64545c849cfd8aa27c492fbbef0488a8668df4839483beb6a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4002a092ea55eab7a080c35546298ef543a07792c2e3f16a78e4fa708c37c02d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a672f1b37e79c200fec775194d3d3613c7ec0cf354d7d39ce6b576dc1be0bbe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleHealthcareFhirStoreStreamConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35bfa6d9c2308fa6fe1fbd1d204b6e91fc96548165dfe5140cf316764d045624(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__184568de902183a536dc4e974c5370f9b991fe15fe122307790ebc35eda74aaf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f1ee2a9106ca1b5946b31e201caf7eb7765164d171e0746f8c22e3dc2039d2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d70b30fa01413fb2aa81c2efd802b39b3ac5f1a0f941dfd1eba7da710f70e69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670b4cf293821b85e8bc9b5c94c152f467d82a8ac87993484b15c96dfeb023de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8181bca9684673be863bcc22321861cc1fff97aa9a08e8b824929df8117ffa10(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleHealthcareFhirStoreTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
