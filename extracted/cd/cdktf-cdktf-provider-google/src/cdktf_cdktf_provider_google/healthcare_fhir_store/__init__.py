r'''
# `google_healthcare_fhir_store`

Refer to the Terraform Registry for docs: [`google_healthcare_fhir_store`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store).
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


class HealthcareFhirStore(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcareFhirStore.HealthcareFhirStore",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store google_healthcare_fhir_store}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dataset: builtins.str,
        name: builtins.str,
        version: builtins.str,
        complex_data_type_reference_parsing: typing.Optional[builtins.str] = None,
        default_search_handling_strict: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_referential_integrity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_resource_versioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_history_import: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_update_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        notification_config: typing.Optional[typing.Union["HealthcareFhirStoreNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        notification_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HealthcareFhirStoreNotificationConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stream_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HealthcareFhirStoreStreamConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["HealthcareFhirStoreTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store google_healthcare_fhir_store} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dataset: Identifies the dataset addressed by this request. Must be in the format 'projects/{project}/locations/{location}/datasets/{dataset}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#dataset HealthcareFhirStore#dataset}
        :param name: The resource name for the FhirStore. ** Changing this property may recreate the FHIR store (removing all data) ** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#name HealthcareFhirStore#name}
        :param version: The FHIR specification version. Possible values: ["DSTU2", "STU3", "R4"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#version HealthcareFhirStore#version}
        :param complex_data_type_reference_parsing: Enable parsing of references within complex FHIR data types such as Extensions. If this value is set to ENABLED, then features like referential integrity and Bundle reference rewriting apply to all references. If this flag has not been specified the behavior of the FHIR store will not change, references in complex data types will not be parsed. New stores will have this value set to ENABLED by default after a notification period. Warning: turning on this flag causes processing existing resources to fail if they contain references to non-existent resources. Possible values: ["COMPLEX_DATA_TYPE_REFERENCE_PARSING_UNSPECIFIED", "DISABLED", "ENABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#complex_data_type_reference_parsing HealthcareFhirStore#complex_data_type_reference_parsing}
        :param default_search_handling_strict: If true, overrides the default search behavior for this FHIR store to handling=strict which returns an error for unrecognized search parameters. If false, uses the FHIR specification default handling=lenient which ignores unrecognized search parameters. The handling can always be changed from the default on an individual API call by setting the HTTP header Prefer: handling=strict or Prefer: handling=lenient. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#default_search_handling_strict HealthcareFhirStore#default_search_handling_strict}
        :param disable_referential_integrity: Whether to disable referential integrity in this FHIR store. This field is immutable after FHIR store creation. The default value is false, meaning that the API will enforce referential integrity and fail the requests that will result in inconsistent state in the FHIR store. When this field is set to true, the API will skip referential integrity check. Consequently, operations that rely on references, such as Patient.get$everything, will not return all the results if broken references exist. ** Changing this property may recreate the FHIR store (removing all data) ** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#disable_referential_integrity HealthcareFhirStore#disable_referential_integrity}
        :param disable_resource_versioning: Whether to disable resource versioning for this FHIR store. This field can not be changed after the creation of FHIR store. If set to false, which is the default behavior, all write operations will cause historical versions to be recorded automatically. The historical versions can be fetched through the history APIs, but cannot be updated. If set to true, no historical versions will be kept. The server will send back errors for attempts to read the historical versions. ** Changing this property may recreate the FHIR store (removing all data) ** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#disable_resource_versioning HealthcareFhirStore#disable_resource_versioning}
        :param enable_history_import: Whether to allow the bulk import API to accept history bundles and directly insert historical resource versions into the FHIR store. Importing resource histories creates resource interactions that appear to have occurred in the past, which clients may not want to allow. If set to false, history bundles within an import will fail with an error. ** Changing this property may recreate the FHIR store (removing all data) ** ** This property can be changed manually in the Google Cloud Healthcare admin console without recreating the FHIR store ** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#enable_history_import HealthcareFhirStore#enable_history_import}
        :param enable_update_create: Whether this FHIR store has the updateCreate capability. This determines if the client can use an Update operation to create a new resource with a client-specified ID. If false, all IDs are server-assigned through the Create operation and attempts to Update a non-existent resource will return errors. Please treat the audit logs with appropriate levels of care if client-specified resource IDs contain sensitive data such as patient identifiers, those IDs will be part of the FHIR resource path recorded in Cloud audit logs and Cloud Pub/Sub notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#enable_update_create HealthcareFhirStore#enable_update_create}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#id HealthcareFhirStore#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-supplied key-value pairs used to organize FHIR stores. Label keys must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}][\\p{Ll}\\p{Lo}\\p{N}_-]{0,62} Label values are optional, must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}\\p{N}_-]{0,63} No more than 64 labels can be associated with a given store. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#labels HealthcareFhirStore#labels}
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#notification_config HealthcareFhirStore#notification_config}
        :param notification_configs: notification_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#notification_configs HealthcareFhirStore#notification_configs}
        :param stream_configs: stream_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#stream_configs HealthcareFhirStore#stream_configs}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#timeouts HealthcareFhirStore#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f6723d6efdff6bd3d3998d923e688b4db8758f67cf7d2c56d343b5a27318221)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = HealthcareFhirStoreConfig(
            dataset=dataset,
            name=name,
            version=version,
            complex_data_type_reference_parsing=complex_data_type_reference_parsing,
            default_search_handling_strict=default_search_handling_strict,
            disable_referential_integrity=disable_referential_integrity,
            disable_resource_versioning=disable_resource_versioning,
            enable_history_import=enable_history_import,
            enable_update_create=enable_update_create,
            id=id,
            labels=labels,
            notification_config=notification_config,
            notification_configs=notification_configs,
            stream_configs=stream_configs,
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
        '''Generates CDKTF code for importing a HealthcareFhirStore resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the HealthcareFhirStore to import.
        :param import_from_id: The id of the existing HealthcareFhirStore that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the HealthcareFhirStore to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdcd85df69ea27155ab5c9f62e49cc2b7aa84f69103dad64ef428008a56a9bb2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putNotificationConfig")
    def put_notification_config(self, *, pubsub_topic: builtins.str) -> None:
        '''
        :param pubsub_topic: The Cloud Pub/Sub topic that notifications of changes are published on. Supplied by the client. PubsubMessage.Data will contain the resource name. PubsubMessage.MessageId is the ID of this message. It is guaranteed to be unique within the topic. PubsubMessage.PublishTime is the time at which the message was published. Notifications are only sent if the topic is non-empty. Topic names must be scoped to a project. service-PROJECT_NUMBER@gcp-sa-healthcare.iam.gserviceaccount.com must have publisher permissions on the given Cloud Pub/Sub topic. Not having adequate permissions will cause the calls that send notifications to fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#pubsub_topic HealthcareFhirStore#pubsub_topic}
        '''
        value = HealthcareFhirStoreNotificationConfig(pubsub_topic=pubsub_topic)

        return typing.cast(None, jsii.invoke(self, "putNotificationConfig", [value]))

    @jsii.member(jsii_name="putNotificationConfigs")
    def put_notification_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HealthcareFhirStoreNotificationConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b10d17936272376e7b8c77af4a989a23fd044fb28b06f181cdadc9a4e43191b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNotificationConfigs", [value]))

    @jsii.member(jsii_name="putStreamConfigs")
    def put_stream_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HealthcareFhirStoreStreamConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17265b2e9646f31aea4c38a5530487bd15f7a7bd179690ef1ab367a0aa4f1583)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#create HealthcareFhirStore#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#delete HealthcareFhirStore#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#update HealthcareFhirStore#update}.
        '''
        value = HealthcareFhirStoreTimeouts(
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
    ) -> "HealthcareFhirStoreNotificationConfigOutputReference":
        return typing.cast("HealthcareFhirStoreNotificationConfigOutputReference", jsii.get(self, "notificationConfig"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfigs")
    def notification_configs(self) -> "HealthcareFhirStoreNotificationConfigsList":
        return typing.cast("HealthcareFhirStoreNotificationConfigsList", jsii.get(self, "notificationConfigs"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="streamConfigs")
    def stream_configs(self) -> "HealthcareFhirStoreStreamConfigsList":
        return typing.cast("HealthcareFhirStoreStreamConfigsList", jsii.get(self, "streamConfigs"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "HealthcareFhirStoreTimeoutsOutputReference":
        return typing.cast("HealthcareFhirStoreTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["HealthcareFhirStoreNotificationConfig"]:
        return typing.cast(typing.Optional["HealthcareFhirStoreNotificationConfig"], jsii.get(self, "notificationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfigsInput")
    def notification_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HealthcareFhirStoreNotificationConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HealthcareFhirStoreNotificationConfigs"]]], jsii.get(self, "notificationConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="streamConfigsInput")
    def stream_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HealthcareFhirStoreStreamConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HealthcareFhirStoreStreamConfigs"]]], jsii.get(self, "streamConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "HealthcareFhirStoreTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "HealthcareFhirStoreTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7771c9139bcf96c0c053669ede7c5d77925a7a7b8918a2b83d0cbf808edbaad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "complexDataTypeReferenceParsing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataset")
    def dataset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataset"))

    @dataset.setter
    def dataset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d8b4ea94aa74053085d5211780176dc1be4f76f2bae673ae6f1058b7e09f570)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8484268c6e1b15a71fab8ab074c592838526e372163089c723165c081df57b78)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e146e47beadae1e6e1f7361e8cf65374bef4c6e708c1a5317073a2ce146173d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__850ffd5d1aac74ecb449010cd5a7da1245408249ae70841b2d2217fbd185f639)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb616da4d8911ff11e1b96275c32651199a63ac6f23c23dfbec8941c6cd757e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableHistoryImport", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__01b30c9be0a62d9f302b6de7d65f06d07980b15b022ba2f0deafc95cf4170599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableUpdateCreate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__461bc7539c52209ee04dad904bbf5db6e6f1de0309e2ec313ccbc8644492f4ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5083a3b0ddc2e12cf5243925aee4501de55af54a01649eb1c26b40b518cf2e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e11e9a2683c2db318a69c5f489a2007931e1b4e4c8f1a476403c9d2ead292e5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__020933d2f477a94ea784dc4f5f9c266b7754c1819b74c8563f9f2fad401c1731)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcareFhirStore.HealthcareFhirStoreConfig",
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
        "version": "version",
        "complex_data_type_reference_parsing": "complexDataTypeReferenceParsing",
        "default_search_handling_strict": "defaultSearchHandlingStrict",
        "disable_referential_integrity": "disableReferentialIntegrity",
        "disable_resource_versioning": "disableResourceVersioning",
        "enable_history_import": "enableHistoryImport",
        "enable_update_create": "enableUpdateCreate",
        "id": "id",
        "labels": "labels",
        "notification_config": "notificationConfig",
        "notification_configs": "notificationConfigs",
        "stream_configs": "streamConfigs",
        "timeouts": "timeouts",
    },
)
class HealthcareFhirStoreConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        version: builtins.str,
        complex_data_type_reference_parsing: typing.Optional[builtins.str] = None,
        default_search_handling_strict: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_referential_integrity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_resource_versioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_history_import: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_update_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        notification_config: typing.Optional[typing.Union["HealthcareFhirStoreNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        notification_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HealthcareFhirStoreNotificationConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stream_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HealthcareFhirStoreStreamConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["HealthcareFhirStoreTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dataset: Identifies the dataset addressed by this request. Must be in the format 'projects/{project}/locations/{location}/datasets/{dataset}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#dataset HealthcareFhirStore#dataset}
        :param name: The resource name for the FhirStore. ** Changing this property may recreate the FHIR store (removing all data) ** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#name HealthcareFhirStore#name}
        :param version: The FHIR specification version. Possible values: ["DSTU2", "STU3", "R4"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#version HealthcareFhirStore#version}
        :param complex_data_type_reference_parsing: Enable parsing of references within complex FHIR data types such as Extensions. If this value is set to ENABLED, then features like referential integrity and Bundle reference rewriting apply to all references. If this flag has not been specified the behavior of the FHIR store will not change, references in complex data types will not be parsed. New stores will have this value set to ENABLED by default after a notification period. Warning: turning on this flag causes processing existing resources to fail if they contain references to non-existent resources. Possible values: ["COMPLEX_DATA_TYPE_REFERENCE_PARSING_UNSPECIFIED", "DISABLED", "ENABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#complex_data_type_reference_parsing HealthcareFhirStore#complex_data_type_reference_parsing}
        :param default_search_handling_strict: If true, overrides the default search behavior for this FHIR store to handling=strict which returns an error for unrecognized search parameters. If false, uses the FHIR specification default handling=lenient which ignores unrecognized search parameters. The handling can always be changed from the default on an individual API call by setting the HTTP header Prefer: handling=strict or Prefer: handling=lenient. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#default_search_handling_strict HealthcareFhirStore#default_search_handling_strict}
        :param disable_referential_integrity: Whether to disable referential integrity in this FHIR store. This field is immutable after FHIR store creation. The default value is false, meaning that the API will enforce referential integrity and fail the requests that will result in inconsistent state in the FHIR store. When this field is set to true, the API will skip referential integrity check. Consequently, operations that rely on references, such as Patient.get$everything, will not return all the results if broken references exist. ** Changing this property may recreate the FHIR store (removing all data) ** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#disable_referential_integrity HealthcareFhirStore#disable_referential_integrity}
        :param disable_resource_versioning: Whether to disable resource versioning for this FHIR store. This field can not be changed after the creation of FHIR store. If set to false, which is the default behavior, all write operations will cause historical versions to be recorded automatically. The historical versions can be fetched through the history APIs, but cannot be updated. If set to true, no historical versions will be kept. The server will send back errors for attempts to read the historical versions. ** Changing this property may recreate the FHIR store (removing all data) ** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#disable_resource_versioning HealthcareFhirStore#disable_resource_versioning}
        :param enable_history_import: Whether to allow the bulk import API to accept history bundles and directly insert historical resource versions into the FHIR store. Importing resource histories creates resource interactions that appear to have occurred in the past, which clients may not want to allow. If set to false, history bundles within an import will fail with an error. ** Changing this property may recreate the FHIR store (removing all data) ** ** This property can be changed manually in the Google Cloud Healthcare admin console without recreating the FHIR store ** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#enable_history_import HealthcareFhirStore#enable_history_import}
        :param enable_update_create: Whether this FHIR store has the updateCreate capability. This determines if the client can use an Update operation to create a new resource with a client-specified ID. If false, all IDs are server-assigned through the Create operation and attempts to Update a non-existent resource will return errors. Please treat the audit logs with appropriate levels of care if client-specified resource IDs contain sensitive data such as patient identifiers, those IDs will be part of the FHIR resource path recorded in Cloud audit logs and Cloud Pub/Sub notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#enable_update_create HealthcareFhirStore#enable_update_create}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#id HealthcareFhirStore#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-supplied key-value pairs used to organize FHIR stores. Label keys must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}][\\p{Ll}\\p{Lo}\\p{N}_-]{0,62} Label values are optional, must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}\\p{N}_-]{0,63} No more than 64 labels can be associated with a given store. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#labels HealthcareFhirStore#labels}
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#notification_config HealthcareFhirStore#notification_config}
        :param notification_configs: notification_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#notification_configs HealthcareFhirStore#notification_configs}
        :param stream_configs: stream_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#stream_configs HealthcareFhirStore#stream_configs}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#timeouts HealthcareFhirStore#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(notification_config, dict):
            notification_config = HealthcareFhirStoreNotificationConfig(**notification_config)
        if isinstance(timeouts, dict):
            timeouts = HealthcareFhirStoreTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e3df16e0385494dfdf2022663f9c01789878ea0c59b57736d458d8d979b8bbb)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument dataset", value=dataset, expected_type=type_hints["dataset"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument complex_data_type_reference_parsing", value=complex_data_type_reference_parsing, expected_type=type_hints["complex_data_type_reference_parsing"])
            check_type(argname="argument default_search_handling_strict", value=default_search_handling_strict, expected_type=type_hints["default_search_handling_strict"])
            check_type(argname="argument disable_referential_integrity", value=disable_referential_integrity, expected_type=type_hints["disable_referential_integrity"])
            check_type(argname="argument disable_resource_versioning", value=disable_resource_versioning, expected_type=type_hints["disable_resource_versioning"])
            check_type(argname="argument enable_history_import", value=enable_history_import, expected_type=type_hints["enable_history_import"])
            check_type(argname="argument enable_update_create", value=enable_update_create, expected_type=type_hints["enable_update_create"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument notification_config", value=notification_config, expected_type=type_hints["notification_config"])
            check_type(argname="argument notification_configs", value=notification_configs, expected_type=type_hints["notification_configs"])
            check_type(argname="argument stream_configs", value=stream_configs, expected_type=type_hints["stream_configs"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset": dataset,
            "name": name,
            "version": version,
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#dataset HealthcareFhirStore#dataset}
        '''
        result = self._values.get("dataset")
        assert result is not None, "Required property 'dataset' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The resource name for the FhirStore.

        ** Changing this property may recreate the FHIR store (removing all data) **

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#name HealthcareFhirStore#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''The FHIR specification version. Possible values: ["DSTU2", "STU3", "R4"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#version HealthcareFhirStore#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def complex_data_type_reference_parsing(self) -> typing.Optional[builtins.str]:
        '''Enable parsing of references within complex FHIR data types such as Extensions.

        If this value is set to ENABLED, then features like referential integrity and Bundle reference rewriting apply to all references. If this flag has not been specified the behavior of the FHIR store will not change, references in complex data types will not be parsed. New stores will have this value set to ENABLED by default after a notification period. Warning: turning on this flag causes processing existing resources to fail if they contain references to non-existent resources. Possible values: ["COMPLEX_DATA_TYPE_REFERENCE_PARSING_UNSPECIFIED", "DISABLED", "ENABLED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#complex_data_type_reference_parsing HealthcareFhirStore#complex_data_type_reference_parsing}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#default_search_handling_strict HealthcareFhirStore#default_search_handling_strict}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#disable_referential_integrity HealthcareFhirStore#disable_referential_integrity}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#disable_resource_versioning HealthcareFhirStore#disable_resource_versioning}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#enable_history_import HealthcareFhirStore#enable_history_import}
        '''
        result = self._values.get("enable_history_import")
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#enable_update_create HealthcareFhirStore#enable_update_create}
        '''
        result = self._values.get("enable_update_create")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#id HealthcareFhirStore#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#labels HealthcareFhirStore#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def notification_config(
        self,
    ) -> typing.Optional["HealthcareFhirStoreNotificationConfig"]:
        '''notification_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#notification_config HealthcareFhirStore#notification_config}
        '''
        result = self._values.get("notification_config")
        return typing.cast(typing.Optional["HealthcareFhirStoreNotificationConfig"], result)

    @builtins.property
    def notification_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HealthcareFhirStoreNotificationConfigs"]]]:
        '''notification_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#notification_configs HealthcareFhirStore#notification_configs}
        '''
        result = self._values.get("notification_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HealthcareFhirStoreNotificationConfigs"]]], result)

    @builtins.property
    def stream_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HealthcareFhirStoreStreamConfigs"]]]:
        '''stream_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#stream_configs HealthcareFhirStore#stream_configs}
        '''
        result = self._values.get("stream_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HealthcareFhirStoreStreamConfigs"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["HealthcareFhirStoreTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#timeouts HealthcareFhirStore#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["HealthcareFhirStoreTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcareFhirStoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcareFhirStore.HealthcareFhirStoreNotificationConfig",
    jsii_struct_bases=[],
    name_mapping={"pubsub_topic": "pubsubTopic"},
)
class HealthcareFhirStoreNotificationConfig:
    def __init__(self, *, pubsub_topic: builtins.str) -> None:
        '''
        :param pubsub_topic: The Cloud Pub/Sub topic that notifications of changes are published on. Supplied by the client. PubsubMessage.Data will contain the resource name. PubsubMessage.MessageId is the ID of this message. It is guaranteed to be unique within the topic. PubsubMessage.PublishTime is the time at which the message was published. Notifications are only sent if the topic is non-empty. Topic names must be scoped to a project. service-PROJECT_NUMBER@gcp-sa-healthcare.iam.gserviceaccount.com must have publisher permissions on the given Cloud Pub/Sub topic. Not having adequate permissions will cause the calls that send notifications to fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#pubsub_topic HealthcareFhirStore#pubsub_topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea419479fe927543f45c3543ef6263c21034b015f147d45e8243f5baf8669a8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#pubsub_topic HealthcareFhirStore#pubsub_topic}
        '''
        result = self._values.get("pubsub_topic")
        assert result is not None, "Required property 'pubsub_topic' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcareFhirStoreNotificationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HealthcareFhirStoreNotificationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcareFhirStore.HealthcareFhirStoreNotificationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7993cdb70c752326726930bd35d8c3b00dd8d4b0cc06c7408cd8bb79408967ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__869242b4eab5f9398364052264b80efde9def204b0e216f3b1588be760846020)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pubsubTopic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HealthcareFhirStoreNotificationConfig]:
        return typing.cast(typing.Optional[HealthcareFhirStoreNotificationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HealthcareFhirStoreNotificationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9099604ab725033c82fdd638ee427ad0fe4e83710fe0c2dfb6d44fb94c79d0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcareFhirStore.HealthcareFhirStoreNotificationConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "pubsub_topic": "pubsubTopic",
        "send_full_resource": "sendFullResource",
        "send_previous_resource_on_delete": "sendPreviousResourceOnDelete",
    },
)
class HealthcareFhirStoreNotificationConfigs:
    def __init__(
        self,
        *,
        pubsub_topic: builtins.str,
        send_full_resource: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_previous_resource_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param pubsub_topic: The Cloud Pub/Sub topic that notifications of changes are published on. Supplied by the client. PubsubMessage.Data will contain the resource name. PubsubMessage.MessageId is the ID of this message. It is guaranteed to be unique within the topic. PubsubMessage.PublishTime is the time at which the message was published. Notifications are only sent if the topic is non-empty. Topic names must be scoped to a project. service-PROJECT_NUMBER@gcp-sa-healthcare.iam.gserviceaccount.com must have publisher permissions on the given Cloud Pub/Sub topic. Not having adequate permissions will cause the calls that send notifications to fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#pubsub_topic HealthcareFhirStore#pubsub_topic}
        :param send_full_resource: Whether to send full FHIR resource to this Pub/Sub topic for Create and Update operation. Note that setting this to true does not guarantee that all resources will be sent in the format of full FHIR resource. When a resource change is too large or during heavy traffic, only the resource name will be sent. Clients should always check the "payloadType" label from a Pub/Sub message to determine whether it needs to fetch the full resource as a separate operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#send_full_resource HealthcareFhirStore#send_full_resource}
        :param send_previous_resource_on_delete: Whether to send full FHIR resource to this Pub/Sub topic for deleting FHIR resource. Note that setting this to true does not guarantee that all previous resources will be sent in the format of full FHIR resource. When a resource change is too large or during heavy traffic, only the resource name will be sent. Clients should always check the "payloadType" label from a Pub/Sub message to determine whether it needs to fetch the full previous resource as a separate operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#send_previous_resource_on_delete HealthcareFhirStore#send_previous_resource_on_delete}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d08942df3b7a88531bd0918907f7b4bf0df78b6e1cb91ae77c0e233379a9fe9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#pubsub_topic HealthcareFhirStore#pubsub_topic}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#send_full_resource HealthcareFhirStore#send_full_resource}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#send_previous_resource_on_delete HealthcareFhirStore#send_previous_resource_on_delete}
        '''
        result = self._values.get("send_previous_resource_on_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcareFhirStoreNotificationConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HealthcareFhirStoreNotificationConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcareFhirStore.HealthcareFhirStoreNotificationConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d3bfdb56008bb1d9f45862b123452455e562ee08bf240bf7e1da04578ee4a9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HealthcareFhirStoreNotificationConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c27c3f51cf6e03d9dec10333590ab446e768b86f013d8c177b948e1592491afb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HealthcareFhirStoreNotificationConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2470f0f33aecd52b179597312ed6e44b5ddefd4c6ca758c9788d6afec52e917b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01055dca44f37d5efd77e2d0b29fda95ac420e724dda40d96616e57b485d0d6b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62eab99051400cbe36271b7e698e7c41c518faaaf3f2d5ca11c01801cdbd4aa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HealthcareFhirStoreNotificationConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HealthcareFhirStoreNotificationConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HealthcareFhirStoreNotificationConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a439267505e0c85c4f0a026dace1d7f0ddc6202911a6b25cbbc2302c464041b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HealthcareFhirStoreNotificationConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcareFhirStore.HealthcareFhirStoreNotificationConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66c8bcef40a13b58cffc1812941d64169eeae8399d82d4161267859eb28f60b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27ef72505d035a683f123d44225bd0d7e474064847801ce73c3843ae624a6383)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d71672abde64d315ea45a2c069ec4e543d4386686073f52ee4dd176384e3aeca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8335f5f7c252cae41f6e8d27d5dd2807b7c02c29b4d5b7069871c5664b01289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendPreviousResourceOnDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcareFhirStoreNotificationConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcareFhirStoreNotificationConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcareFhirStoreNotificationConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1c977f8de7f525201006ffb9e7c5cebb593ff22e75b0b565c5f181cfae712b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcareFhirStore.HealthcareFhirStoreStreamConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "bigquery_destination": "bigqueryDestination",
        "resource_types": "resourceTypes",
    },
)
class HealthcareFhirStoreStreamConfigs:
    def __init__(
        self,
        *,
        bigquery_destination: typing.Union["HealthcareFhirStoreStreamConfigsBigqueryDestination", typing.Dict[builtins.str, typing.Any]],
        resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param bigquery_destination: bigquery_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#bigquery_destination HealthcareFhirStore#bigquery_destination}
        :param resource_types: Supply a FHIR resource type (such as "Patient" or "Observation"). See https://www.hl7.org/fhir/valueset-resource-types.html for a list of all FHIR resource types. The server treats an empty list as an intent to stream all the supported resource types in this FHIR store. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#resource_types HealthcareFhirStore#resource_types}
        '''
        if isinstance(bigquery_destination, dict):
            bigquery_destination = HealthcareFhirStoreStreamConfigsBigqueryDestination(**bigquery_destination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6690e0309661f7029ad37ec57be1d19d8c9c77330966175a6d6f0c8205fc0b14)
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
    ) -> "HealthcareFhirStoreStreamConfigsBigqueryDestination":
        '''bigquery_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#bigquery_destination HealthcareFhirStore#bigquery_destination}
        '''
        result = self._values.get("bigquery_destination")
        assert result is not None, "Required property 'bigquery_destination' is missing"
        return typing.cast("HealthcareFhirStoreStreamConfigsBigqueryDestination", result)

    @builtins.property
    def resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Supply a FHIR resource type (such as "Patient" or "Observation").

        See
        https://www.hl7.org/fhir/valueset-resource-types.html for a list of all FHIR resource types. The server treats
        an empty list as an intent to stream all the supported resource types in this FHIR store.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#resource_types HealthcareFhirStore#resource_types}
        '''
        result = self._values.get("resource_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcareFhirStoreStreamConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcareFhirStore.HealthcareFhirStoreStreamConfigsBigqueryDestination",
    jsii_struct_bases=[],
    name_mapping={"dataset_uri": "datasetUri", "schema_config": "schemaConfig"},
)
class HealthcareFhirStoreStreamConfigsBigqueryDestination:
    def __init__(
        self,
        *,
        dataset_uri: builtins.str,
        schema_config: typing.Union["HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param dataset_uri: BigQuery URI to a dataset, up to 2000 characters long, in the format bq://projectId.bqDatasetId. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#dataset_uri HealthcareFhirStore#dataset_uri}
        :param schema_config: schema_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#schema_config HealthcareFhirStore#schema_config}
        '''
        if isinstance(schema_config, dict):
            schema_config = HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig(**schema_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1caef64f709e347e62524c2218686781bd9e2176a2615ce9d81f0b88382a7c31)
            check_type(argname="argument dataset_uri", value=dataset_uri, expected_type=type_hints["dataset_uri"])
            check_type(argname="argument schema_config", value=schema_config, expected_type=type_hints["schema_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_uri": dataset_uri,
            "schema_config": schema_config,
        }

    @builtins.property
    def dataset_uri(self) -> builtins.str:
        '''BigQuery URI to a dataset, up to 2000 characters long, in the format bq://projectId.bqDatasetId.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#dataset_uri HealthcareFhirStore#dataset_uri}
        '''
        result = self._values.get("dataset_uri")
        assert result is not None, "Required property 'dataset_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema_config(
        self,
    ) -> "HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig":
        '''schema_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#schema_config HealthcareFhirStore#schema_config}
        '''
        result = self._values.get("schema_config")
        assert result is not None, "Required property 'schema_config' is missing"
        return typing.cast("HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcareFhirStoreStreamConfigsBigqueryDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HealthcareFhirStoreStreamConfigsBigqueryDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcareFhirStore.HealthcareFhirStoreStreamConfigsBigqueryDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a02177d362a5bbd1b006da0bd3edac01b0f7c3a719f003f377acda87f7dbcaa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSchemaConfig")
    def put_schema_config(
        self,
        *,
        recursive_structure_depth: jsii.Number,
        last_updated_partition_config: typing.Optional[typing.Union["HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        schema_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param recursive_structure_depth: The depth for all recursive structures in the output analytics schema. For example, concept in the CodeSystem resource is a recursive structure; when the depth is 2, the CodeSystem table will have a column called concept.concept but not concept.concept.concept. If not specified or set to 0, the server will use the default value 2. The maximum depth allowed is 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#recursive_structure_depth HealthcareFhirStore#recursive_structure_depth}
        :param last_updated_partition_config: last_updated_partition_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#last_updated_partition_config HealthcareFhirStore#last_updated_partition_config}
        :param schema_type: Specifies the output schema type. - ANALYTICS: Analytics schema defined by the FHIR community. See https://github.com/FHIR/sql-on-fhir/blob/master/sql-on-fhir.md. - ANALYTICS_V2: Analytics V2, similar to schema defined by the FHIR community, with added support for extensions with one or more occurrences and contained resources in stringified JSON. - LOSSLESS: A data-driven schema generated from the fields present in the FHIR data being exported, with no additional simplification. Default value: "ANALYTICS" Possible values: ["ANALYTICS", "ANALYTICS_V2", "LOSSLESS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#schema_type HealthcareFhirStore#schema_type}
        '''
        value = HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig(
            recursive_structure_depth=recursive_structure_depth,
            last_updated_partition_config=last_updated_partition_config,
            schema_type=schema_type,
        )

        return typing.cast(None, jsii.invoke(self, "putSchemaConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="schemaConfig")
    def schema_config(
        self,
    ) -> "HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigOutputReference":
        return typing.cast("HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigOutputReference", jsii.get(self, "schemaConfig"))

    @builtins.property
    @jsii.member(jsii_name="datasetUriInput")
    def dataset_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetUriInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaConfigInput")
    def schema_config_input(
        self,
    ) -> typing.Optional["HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig"]:
        return typing.cast(typing.Optional["HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig"], jsii.get(self, "schemaConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetUri")
    def dataset_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetUri"))

    @dataset_uri.setter
    def dataset_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef42f6fdcef6e86469df83fa6c05af52bb38873eea12d517a174f2a1b81962aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HealthcareFhirStoreStreamConfigsBigqueryDestination]:
        return typing.cast(typing.Optional[HealthcareFhirStoreStreamConfigsBigqueryDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HealthcareFhirStoreStreamConfigsBigqueryDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25ee293aa300df67d2b5edf71892e6b7e4a6e5f39c830bf2c33bdcb84668aa77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcareFhirStore.HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig",
    jsii_struct_bases=[],
    name_mapping={
        "recursive_structure_depth": "recursiveStructureDepth",
        "last_updated_partition_config": "lastUpdatedPartitionConfig",
        "schema_type": "schemaType",
    },
)
class HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig:
    def __init__(
        self,
        *,
        recursive_structure_depth: jsii.Number,
        last_updated_partition_config: typing.Optional[typing.Union["HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        schema_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param recursive_structure_depth: The depth for all recursive structures in the output analytics schema. For example, concept in the CodeSystem resource is a recursive structure; when the depth is 2, the CodeSystem table will have a column called concept.concept but not concept.concept.concept. If not specified or set to 0, the server will use the default value 2. The maximum depth allowed is 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#recursive_structure_depth HealthcareFhirStore#recursive_structure_depth}
        :param last_updated_partition_config: last_updated_partition_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#last_updated_partition_config HealthcareFhirStore#last_updated_partition_config}
        :param schema_type: Specifies the output schema type. - ANALYTICS: Analytics schema defined by the FHIR community. See https://github.com/FHIR/sql-on-fhir/blob/master/sql-on-fhir.md. - ANALYTICS_V2: Analytics V2, similar to schema defined by the FHIR community, with added support for extensions with one or more occurrences and contained resources in stringified JSON. - LOSSLESS: A data-driven schema generated from the fields present in the FHIR data being exported, with no additional simplification. Default value: "ANALYTICS" Possible values: ["ANALYTICS", "ANALYTICS_V2", "LOSSLESS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#schema_type HealthcareFhirStore#schema_type}
        '''
        if isinstance(last_updated_partition_config, dict):
            last_updated_partition_config = HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig(**last_updated_partition_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4be43d23b3fece7e78228efcde1b4afe6462ac0a868f74ada006f036005c1cf6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#recursive_structure_depth HealthcareFhirStore#recursive_structure_depth}
        '''
        result = self._values.get("recursive_structure_depth")
        assert result is not None, "Required property 'recursive_structure_depth' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def last_updated_partition_config(
        self,
    ) -> typing.Optional["HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig"]:
        '''last_updated_partition_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#last_updated_partition_config HealthcareFhirStore#last_updated_partition_config}
        '''
        result = self._values.get("last_updated_partition_config")
        return typing.cast(typing.Optional["HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig"], result)

    @builtins.property
    def schema_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the output schema type.

        - ANALYTICS: Analytics schema defined by the FHIR community.
          See https://github.com/FHIR/sql-on-fhir/blob/master/sql-on-fhir.md.
        - ANALYTICS_V2: Analytics V2, similar to schema defined by the FHIR community, with added support for extensions with one or more occurrences and contained resources in stringified JSON.
        - LOSSLESS: A data-driven schema generated from the fields present in the FHIR data being exported, with no additional simplification. Default value: "ANALYTICS" Possible values: ["ANALYTICS", "ANALYTICS_V2", "LOSSLESS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#schema_type HealthcareFhirStore#schema_type}
        '''
        result = self._values.get("schema_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcareFhirStore.HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "expiration_ms": "expirationMs"},
)
class HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig:
    def __init__(
        self,
        *,
        type: builtins.str,
        expiration_ms: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of partitioning. Possible values: ["PARTITION_TYPE_UNSPECIFIED", "HOUR", "DAY", "MONTH", "YEAR"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#type HealthcareFhirStore#type}
        :param expiration_ms: Number of milliseconds for which to keep the storage for a partition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#expiration_ms HealthcareFhirStore#expiration_ms}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a2e0ce4511e908eaf0497a73648f25c87ebcd54d23735a1a64f7ab40fe8df3b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#type HealthcareFhirStore#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expiration_ms(self) -> typing.Optional[builtins.str]:
        '''Number of milliseconds for which to keep the storage for a partition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#expiration_ms HealthcareFhirStore#expiration_ms}
        '''
        result = self._values.get("expiration_ms")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcareFhirStore.HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90851c72b997b854a1041d7c78685bb7f78d94e7b2e170ed9fe3c2e498cb787f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28afac7e9b0f012fbe4ae32af2ec24e580b905a73e8ec09a10727e4aa8f74d86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationMs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f32b82e5c778c190f573c4a9364ce1256556022a5e89eefb202c1fa59478820)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig]:
        return typing.cast(typing.Optional[HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d5dff24c88810734bcc3c21a7c2aea57d572ac5dadcd627dbf90a64828d8888)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcareFhirStore.HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d479937ab3802a76271364b82f46fbbf7c2e4ebf0421b13ec4088e5012dad807)
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
        :param type: Type of partitioning. Possible values: ["PARTITION_TYPE_UNSPECIFIED", "HOUR", "DAY", "MONTH", "YEAR"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#type HealthcareFhirStore#type}
        :param expiration_ms: Number of milliseconds for which to keep the storage for a partition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#expiration_ms HealthcareFhirStore#expiration_ms}
        '''
        value = HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig(
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
    ) -> HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfigOutputReference:
        return typing.cast(HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfigOutputReference, jsii.get(self, "lastUpdatedPartitionConfig"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdatedPartitionConfigInput")
    def last_updated_partition_config_input(
        self,
    ) -> typing.Optional[HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig]:
        return typing.cast(typing.Optional[HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig], jsii.get(self, "lastUpdatedPartitionConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__89e21743759a616ccf1de495148de1bb55781ea0b1c1f652b7cf451bde333397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recursiveStructureDepth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schemaType")
    def schema_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaType"))

    @schema_type.setter
    def schema_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a1b8c3b910d2b62793df8fb15cdc1dd1ae72d72d71ed5cd7630d84f1ab1ceea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig]:
        return typing.cast(typing.Optional[HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54e6547e1e81bd009b674f3dcdf1b7671b56275afc2451e2bab7b3857d7110eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HealthcareFhirStoreStreamConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcareFhirStore.HealthcareFhirStoreStreamConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8a55694a20ed9581d956922bb388b1d7b98ebb10ce9374d0d8b0f8dc5e756ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HealthcareFhirStoreStreamConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01b5c9732121d4c1cd423f6da7394884efd874015e265fb7a1add6c51c661668)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HealthcareFhirStoreStreamConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16d6fa3c8cbdaf7adbe29fc94f164e4e0da2e517c4bd3e902ee71b589b6894a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdd2f49c8ea95b7ac4e2ed898645799ab22873f490208e44a47da180d9dbf37d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a542291e4330aad06fd0505907cfe59be8afc4ba63df2e3b321c50a16e2373f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HealthcareFhirStoreStreamConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HealthcareFhirStoreStreamConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HealthcareFhirStoreStreamConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf4e659ef7a0cf4705d4c20e2e83c3c52fd7a1eb36d71ef4f53b84ec75b8f1ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HealthcareFhirStoreStreamConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcareFhirStore.HealthcareFhirStoreStreamConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a90248a23e76b2f6a8170fc6a174990367f5d5573b6c8f0e594a9b89445de5ce)
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
        schema_config: typing.Union[HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param dataset_uri: BigQuery URI to a dataset, up to 2000 characters long, in the format bq://projectId.bqDatasetId. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#dataset_uri HealthcareFhirStore#dataset_uri}
        :param schema_config: schema_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#schema_config HealthcareFhirStore#schema_config}
        '''
        value = HealthcareFhirStoreStreamConfigsBigqueryDestination(
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
    ) -> HealthcareFhirStoreStreamConfigsBigqueryDestinationOutputReference:
        return typing.cast(HealthcareFhirStoreStreamConfigsBigqueryDestinationOutputReference, jsii.get(self, "bigqueryDestination"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryDestinationInput")
    def bigquery_destination_input(
        self,
    ) -> typing.Optional[HealthcareFhirStoreStreamConfigsBigqueryDestination]:
        return typing.cast(typing.Optional[HealthcareFhirStoreStreamConfigsBigqueryDestination], jsii.get(self, "bigqueryDestinationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ed7447050fa97d5ad7c578a62da9ef9e464f502c15fe8045237cd5747c33bd5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcareFhirStoreStreamConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcareFhirStoreStreamConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcareFhirStoreStreamConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6d9ae18f0f153502e7950d8727255117013aefd98bbd050abb7f8920edf6c15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcareFhirStore.HealthcareFhirStoreTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class HealthcareFhirStoreTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#create HealthcareFhirStore#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#delete HealthcareFhirStore#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#update HealthcareFhirStore#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc0e2cb8aab25b3d4ecc2bbd0565001e6deabb5b30454399fd821ff5637d2f7)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#create HealthcareFhirStore#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#delete HealthcareFhirStore#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_fhir_store#update HealthcareFhirStore#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcareFhirStoreTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HealthcareFhirStoreTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcareFhirStore.HealthcareFhirStoreTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f749336a266284d3e9179e9172d4893afbc902dd49bcc45c820a5df1fd003bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa189afa204238541305ed5b5ae87e3092fbb1f4075007fba66170904e690375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f08a9efef60067275caa09f4893c918e5502d56aff1aae69c6d6e51c549fb12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f64813ab419810d2df41c64f47138d41cd70a0cebbac3815ae99b92e80b29dc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcareFhirStoreTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcareFhirStoreTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcareFhirStoreTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a2e1e90907afd238e26ea9ea8089f0140402b42f06aae03a2cdbf58c62d9c8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "HealthcareFhirStore",
    "HealthcareFhirStoreConfig",
    "HealthcareFhirStoreNotificationConfig",
    "HealthcareFhirStoreNotificationConfigOutputReference",
    "HealthcareFhirStoreNotificationConfigs",
    "HealthcareFhirStoreNotificationConfigsList",
    "HealthcareFhirStoreNotificationConfigsOutputReference",
    "HealthcareFhirStoreStreamConfigs",
    "HealthcareFhirStoreStreamConfigsBigqueryDestination",
    "HealthcareFhirStoreStreamConfigsBigqueryDestinationOutputReference",
    "HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig",
    "HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig",
    "HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfigOutputReference",
    "HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigOutputReference",
    "HealthcareFhirStoreStreamConfigsList",
    "HealthcareFhirStoreStreamConfigsOutputReference",
    "HealthcareFhirStoreTimeouts",
    "HealthcareFhirStoreTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7f6723d6efdff6bd3d3998d923e688b4db8758f67cf7d2c56d343b5a27318221(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dataset: builtins.str,
    name: builtins.str,
    version: builtins.str,
    complex_data_type_reference_parsing: typing.Optional[builtins.str] = None,
    default_search_handling_strict: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_referential_integrity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_resource_versioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_history_import: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_update_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    notification_config: typing.Optional[typing.Union[HealthcareFhirStoreNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    notification_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HealthcareFhirStoreNotificationConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stream_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HealthcareFhirStoreStreamConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[HealthcareFhirStoreTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__bdcd85df69ea27155ab5c9f62e49cc2b7aa84f69103dad64ef428008a56a9bb2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10d17936272376e7b8c77af4a989a23fd044fb28b06f181cdadc9a4e43191b3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HealthcareFhirStoreNotificationConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17265b2e9646f31aea4c38a5530487bd15f7a7bd179690ef1ab367a0aa4f1583(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HealthcareFhirStoreStreamConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7771c9139bcf96c0c053669ede7c5d77925a7a7b8918a2b83d0cbf808edbaad9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d8b4ea94aa74053085d5211780176dc1be4f76f2bae673ae6f1058b7e09f570(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8484268c6e1b15a71fab8ab074c592838526e372163089c723165c081df57b78(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e146e47beadae1e6e1f7361e8cf65374bef4c6e708c1a5317073a2ce146173d3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__850ffd5d1aac74ecb449010cd5a7da1245408249ae70841b2d2217fbd185f639(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb616da4d8911ff11e1b96275c32651199a63ac6f23c23dfbec8941c6cd757e0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01b30c9be0a62d9f302b6de7d65f06d07980b15b022ba2f0deafc95cf4170599(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__461bc7539c52209ee04dad904bbf5db6e6f1de0309e2ec313ccbc8644492f4ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5083a3b0ddc2e12cf5243925aee4501de55af54a01649eb1c26b40b518cf2e4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e11e9a2683c2db318a69c5f489a2007931e1b4e4c8f1a476403c9d2ead292e5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020933d2f477a94ea784dc4f5f9c266b7754c1819b74c8563f9f2fad401c1731(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e3df16e0385494dfdf2022663f9c01789878ea0c59b57736d458d8d979b8bbb(
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
    version: builtins.str,
    complex_data_type_reference_parsing: typing.Optional[builtins.str] = None,
    default_search_handling_strict: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_referential_integrity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_resource_versioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_history_import: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_update_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    notification_config: typing.Optional[typing.Union[HealthcareFhirStoreNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    notification_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HealthcareFhirStoreNotificationConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stream_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HealthcareFhirStoreStreamConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[HealthcareFhirStoreTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea419479fe927543f45c3543ef6263c21034b015f147d45e8243f5baf8669a8(
    *,
    pubsub_topic: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7993cdb70c752326726930bd35d8c3b00dd8d4b0cc06c7408cd8bb79408967ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__869242b4eab5f9398364052264b80efde9def204b0e216f3b1588be760846020(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9099604ab725033c82fdd638ee427ad0fe4e83710fe0c2dfb6d44fb94c79d0a(
    value: typing.Optional[HealthcareFhirStoreNotificationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d08942df3b7a88531bd0918907f7b4bf0df78b6e1cb91ae77c0e233379a9fe9(
    *,
    pubsub_topic: builtins.str,
    send_full_resource: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    send_previous_resource_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d3bfdb56008bb1d9f45862b123452455e562ee08bf240bf7e1da04578ee4a9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27c3f51cf6e03d9dec10333590ab446e768b86f013d8c177b948e1592491afb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2470f0f33aecd52b179597312ed6e44b5ddefd4c6ca758c9788d6afec52e917b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01055dca44f37d5efd77e2d0b29fda95ac420e724dda40d96616e57b485d0d6b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62eab99051400cbe36271b7e698e7c41c518faaaf3f2d5ca11c01801cdbd4aa4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a439267505e0c85c4f0a026dace1d7f0ddc6202911a6b25cbbc2302c464041b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HealthcareFhirStoreNotificationConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66c8bcef40a13b58cffc1812941d64169eeae8399d82d4161267859eb28f60b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ef72505d035a683f123d44225bd0d7e474064847801ce73c3843ae624a6383(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d71672abde64d315ea45a2c069ec4e543d4386686073f52ee4dd176384e3aeca(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8335f5f7c252cae41f6e8d27d5dd2807b7c02c29b4d5b7069871c5664b01289(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c977f8de7f525201006ffb9e7c5cebb593ff22e75b0b565c5f181cfae712b6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcareFhirStoreNotificationConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6690e0309661f7029ad37ec57be1d19d8c9c77330966175a6d6f0c8205fc0b14(
    *,
    bigquery_destination: typing.Union[HealthcareFhirStoreStreamConfigsBigqueryDestination, typing.Dict[builtins.str, typing.Any]],
    resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1caef64f709e347e62524c2218686781bd9e2176a2615ce9d81f0b88382a7c31(
    *,
    dataset_uri: builtins.str,
    schema_config: typing.Union[HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a02177d362a5bbd1b006da0bd3edac01b0f7c3a719f003f377acda87f7dbcaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef42f6fdcef6e86469df83fa6c05af52bb38873eea12d517a174f2a1b81962aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ee293aa300df67d2b5edf71892e6b7e4a6e5f39c830bf2c33bdcb84668aa77(
    value: typing.Optional[HealthcareFhirStoreStreamConfigsBigqueryDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4be43d23b3fece7e78228efcde1b4afe6462ac0a868f74ada006f036005c1cf6(
    *,
    recursive_structure_depth: jsii.Number,
    last_updated_partition_config: typing.Optional[typing.Union[HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    schema_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2e0ce4511e908eaf0497a73648f25c87ebcd54d23735a1a64f7ab40fe8df3b(
    *,
    type: builtins.str,
    expiration_ms: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90851c72b997b854a1041d7c78685bb7f78d94e7b2e170ed9fe3c2e498cb787f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28afac7e9b0f012fbe4ae32af2ec24e580b905a73e8ec09a10727e4aa8f74d86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f32b82e5c778c190f573c4a9364ce1256556022a5e89eefb202c1fa59478820(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5dff24c88810734bcc3c21a7c2aea57d572ac5dadcd627dbf90a64828d8888(
    value: typing.Optional[HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfigLastUpdatedPartitionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d479937ab3802a76271364b82f46fbbf7c2e4ebf0421b13ec4088e5012dad807(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e21743759a616ccf1de495148de1bb55781ea0b1c1f652b7cf451bde333397(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a1b8c3b910d2b62793df8fb15cdc1dd1ae72d72d71ed5cd7630d84f1ab1ceea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e6547e1e81bd009b674f3dcdf1b7671b56275afc2451e2bab7b3857d7110eb(
    value: typing.Optional[HealthcareFhirStoreStreamConfigsBigqueryDestinationSchemaConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a55694a20ed9581d956922bb388b1d7b98ebb10ce9374d0d8b0f8dc5e756ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01b5c9732121d4c1cd423f6da7394884efd874015e265fb7a1add6c51c661668(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d6fa3c8cbdaf7adbe29fc94f164e4e0da2e517c4bd3e902ee71b589b6894a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdd2f49c8ea95b7ac4e2ed898645799ab22873f490208e44a47da180d9dbf37d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a542291e4330aad06fd0505907cfe59be8afc4ba63df2e3b321c50a16e2373f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf4e659ef7a0cf4705d4c20e2e83c3c52fd7a1eb36d71ef4f53b84ec75b8f1ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HealthcareFhirStoreStreamConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90248a23e76b2f6a8170fc6a174990367f5d5573b6c8f0e594a9b89445de5ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed7447050fa97d5ad7c578a62da9ef9e464f502c15fe8045237cd5747c33bd5f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d9ae18f0f153502e7950d8727255117013aefd98bbd050abb7f8920edf6c15(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcareFhirStoreStreamConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc0e2cb8aab25b3d4ecc2bbd0565001e6deabb5b30454399fd821ff5637d2f7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f749336a266284d3e9179e9172d4893afbc902dd49bcc45c820a5df1fd003bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa189afa204238541305ed5b5ae87e3092fbb1f4075007fba66170904e690375(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f08a9efef60067275caa09f4893c918e5502d56aff1aae69c6d6e51c549fb12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64813ab419810d2df41c64f47138d41cd70a0cebbac3815ae99b92e80b29dc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2e1e90907afd238e26ea9ea8089f0140402b42f06aae03a2cdbf58c62d9c8e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcareFhirStoreTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
