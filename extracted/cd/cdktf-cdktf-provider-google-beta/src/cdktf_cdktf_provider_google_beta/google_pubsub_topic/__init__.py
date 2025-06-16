r'''
# `google_pubsub_topic`

Refer to the Terraform Registry for docs: [`google_pubsub_topic`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic).
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


class GooglePubsubTopic(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopic",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic google_pubsub_topic}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        ingestion_data_source_settings: typing.Optional[typing.Union["GooglePubsubTopicIngestionDataSourceSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        message_retention_duration: typing.Optional[builtins.str] = None,
        message_storage_policy: typing.Optional[typing.Union["GooglePubsubTopicMessageStoragePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        message_transforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GooglePubsubTopicMessageTransforms", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        schema_settings: typing.Optional[typing.Union["GooglePubsubTopicSchemaSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GooglePubsubTopicTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic google_pubsub_topic} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#name GooglePubsubTopic#name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#id GooglePubsubTopic#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ingestion_data_source_settings: ingestion_data_source_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#ingestion_data_source_settings GooglePubsubTopic#ingestion_data_source_settings}
        :param kms_key_name: The resource name of the Cloud KMS CryptoKey to be used to protect access to messages published on this topic. Your project's PubSub service account ('service-{{PROJECT_NUMBER}}@gcp-sa-pubsub.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. The expected format is 'projects/* /locations/* /keyRings/* /cryptoKeys/*' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#kms_key_name GooglePubsubTopic#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param labels: A set of key/value label pairs to assign to this Topic. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#labels GooglePubsubTopic#labels}
        :param message_retention_duration: Indicates the minimum duration to retain a message after it is published to the topic. If this field is set, messages published to the topic in the last messageRetentionDuration are always available to subscribers. For instance, it allows any attached subscription to seek to a timestamp that is up to messageRetentionDuration in the past. If this field is not set, message retention is controlled by settings on individual subscriptions. The rotation period has the format of a decimal number, followed by the letter 's' (seconds). Cannot be more than 31 days or less than 10 minutes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#message_retention_duration GooglePubsubTopic#message_retention_duration}
        :param message_storage_policy: message_storage_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#message_storage_policy GooglePubsubTopic#message_storage_policy}
        :param message_transforms: message_transforms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#message_transforms GooglePubsubTopic#message_transforms}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#project GooglePubsubTopic#project}.
        :param schema_settings: schema_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#schema_settings GooglePubsubTopic#schema_settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#timeouts GooglePubsubTopic#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__632d9ee170a770a95ec0d40830ef047caca59b182c12a2804baeb1e03a825389)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GooglePubsubTopicConfig(
            name=name,
            id=id,
            ingestion_data_source_settings=ingestion_data_source_settings,
            kms_key_name=kms_key_name,
            labels=labels,
            message_retention_duration=message_retention_duration,
            message_storage_policy=message_storage_policy,
            message_transforms=message_transforms,
            project=project,
            schema_settings=schema_settings,
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
        '''Generates CDKTF code for importing a GooglePubsubTopic resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GooglePubsubTopic to import.
        :param import_from_id: The id of the existing GooglePubsubTopic that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GooglePubsubTopic to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48564ab17ae5cde24b80b7be627a8b421d35aa1d9fb5edf5e5a349cb03c8cf63)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIngestionDataSourceSettings")
    def put_ingestion_data_source_settings(
        self,
        *,
        aws_kinesis: typing.Optional[typing.Union["GooglePubsubTopicIngestionDataSourceSettingsAwsKinesis", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_msk: typing.Optional[typing.Union["GooglePubsubTopicIngestionDataSourceSettingsAwsMsk", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_event_hubs: typing.Optional[typing.Union["GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubs", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_storage: typing.Optional[typing.Union["GooglePubsubTopicIngestionDataSourceSettingsCloudStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        confluent_cloud: typing.Optional[typing.Union["GooglePubsubTopicIngestionDataSourceSettingsConfluentCloud", typing.Dict[builtins.str, typing.Any]]] = None,
        platform_logs_settings: typing.Optional[typing.Union["GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws_kinesis: aws_kinesis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#aws_kinesis GooglePubsubTopic#aws_kinesis}
        :param aws_msk: aws_msk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#aws_msk GooglePubsubTopic#aws_msk}
        :param azure_event_hubs: azure_event_hubs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#azure_event_hubs GooglePubsubTopic#azure_event_hubs}
        :param cloud_storage: cloud_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#cloud_storage GooglePubsubTopic#cloud_storage}
        :param confluent_cloud: confluent_cloud block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#confluent_cloud GooglePubsubTopic#confluent_cloud}
        :param platform_logs_settings: platform_logs_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#platform_logs_settings GooglePubsubTopic#platform_logs_settings}
        '''
        value = GooglePubsubTopicIngestionDataSourceSettings(
            aws_kinesis=aws_kinesis,
            aws_msk=aws_msk,
            azure_event_hubs=azure_event_hubs,
            cloud_storage=cloud_storage,
            confluent_cloud=confluent_cloud,
            platform_logs_settings=platform_logs_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putIngestionDataSourceSettings", [value]))

    @jsii.member(jsii_name="putMessageStoragePolicy")
    def put_message_storage_policy(
        self,
        *,
        allowed_persistence_regions: typing.Sequence[builtins.str],
        enforce_in_transit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_persistence_regions: A list of IDs of GCP regions where messages that are published to the topic may be persisted in storage. Messages published by publishers running in non-allowed GCP regions (or running outside of GCP altogether) will be routed for storage in one of the allowed regions. An empty list means that no regions are allowed, and is not a valid configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#allowed_persistence_regions GooglePubsubTopic#allowed_persistence_regions}
        :param enforce_in_transit: If true, 'allowedPersistenceRegions' is also used to enforce in-transit guarantees for messages. That is, Pub/Sub will fail topics.publish operations on this topic and subscribe operations on any subscription attached to this topic in any region that is not in 'allowedPersistenceRegions'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#enforce_in_transit GooglePubsubTopic#enforce_in_transit}
        '''
        value = GooglePubsubTopicMessageStoragePolicy(
            allowed_persistence_regions=allowed_persistence_regions,
            enforce_in_transit=enforce_in_transit,
        )

        return typing.cast(None, jsii.invoke(self, "putMessageStoragePolicy", [value]))

    @jsii.member(jsii_name="putMessageTransforms")
    def put_message_transforms(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GooglePubsubTopicMessageTransforms", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9a1878163a3d126a8be1541984dfc6a2d1d30c3f1636db6c634a77bb581631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMessageTransforms", [value]))

    @jsii.member(jsii_name="putSchemaSettings")
    def put_schema_settings(
        self,
        *,
        schema: builtins.str,
        encoding: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema: The name of the schema that messages published should be validated against. Format is projects/{project}/schemas/{schema}. The value of this field will be *deleted-schema* if the schema has been deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#schema GooglePubsubTopic#schema}
        :param encoding: The encoding of messages validated against schema. Default value: "ENCODING_UNSPECIFIED" Possible values: ["ENCODING_UNSPECIFIED", "JSON", "BINARY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#encoding GooglePubsubTopic#encoding}
        '''
        value = GooglePubsubTopicSchemaSettings(schema=schema, encoding=encoding)

        return typing.cast(None, jsii.invoke(self, "putSchemaSettings", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#create GooglePubsubTopic#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#delete GooglePubsubTopic#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#update GooglePubsubTopic#update}.
        '''
        value = GooglePubsubTopicTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIngestionDataSourceSettings")
    def reset_ingestion_data_source_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngestionDataSourceSettings", []))

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMessageRetentionDuration")
    def reset_message_retention_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageRetentionDuration", []))

    @jsii.member(jsii_name="resetMessageStoragePolicy")
    def reset_message_storage_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageStoragePolicy", []))

    @jsii.member(jsii_name="resetMessageTransforms")
    def reset_message_transforms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageTransforms", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSchemaSettings")
    def reset_schema_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaSettings", []))

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
    @jsii.member(jsii_name="ingestionDataSourceSettings")
    def ingestion_data_source_settings(
        self,
    ) -> "GooglePubsubTopicIngestionDataSourceSettingsOutputReference":
        return typing.cast("GooglePubsubTopicIngestionDataSourceSettingsOutputReference", jsii.get(self, "ingestionDataSourceSettings"))

    @builtins.property
    @jsii.member(jsii_name="messageStoragePolicy")
    def message_storage_policy(
        self,
    ) -> "GooglePubsubTopicMessageStoragePolicyOutputReference":
        return typing.cast("GooglePubsubTopicMessageStoragePolicyOutputReference", jsii.get(self, "messageStoragePolicy"))

    @builtins.property
    @jsii.member(jsii_name="messageTransforms")
    def message_transforms(self) -> "GooglePubsubTopicMessageTransformsList":
        return typing.cast("GooglePubsubTopicMessageTransformsList", jsii.get(self, "messageTransforms"))

    @builtins.property
    @jsii.member(jsii_name="schemaSettings")
    def schema_settings(self) -> "GooglePubsubTopicSchemaSettingsOutputReference":
        return typing.cast("GooglePubsubTopicSchemaSettingsOutputReference", jsii.get(self, "schemaSettings"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GooglePubsubTopicTimeoutsOutputReference":
        return typing.cast("GooglePubsubTopicTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ingestionDataSourceSettingsInput")
    def ingestion_data_source_settings_input(
        self,
    ) -> typing.Optional["GooglePubsubTopicIngestionDataSourceSettings"]:
        return typing.cast(typing.Optional["GooglePubsubTopicIngestionDataSourceSettings"], jsii.get(self, "ingestionDataSourceSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="messageRetentionDurationInput")
    def message_retention_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageRetentionDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="messageStoragePolicyInput")
    def message_storage_policy_input(
        self,
    ) -> typing.Optional["GooglePubsubTopicMessageStoragePolicy"]:
        return typing.cast(typing.Optional["GooglePubsubTopicMessageStoragePolicy"], jsii.get(self, "messageStoragePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="messageTransformsInput")
    def message_transforms_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePubsubTopicMessageTransforms"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePubsubTopicMessageTransforms"]]], jsii.get(self, "messageTransformsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaSettingsInput")
    def schema_settings_input(
        self,
    ) -> typing.Optional["GooglePubsubTopicSchemaSettings"]:
        return typing.cast(typing.Optional["GooglePubsubTopicSchemaSettings"], jsii.get(self, "schemaSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GooglePubsubTopicTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GooglePubsubTopicTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d80012e89fc62d7d405ff750079d41322d0e2f3d879f750547153c5b01b0bb5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f364d62e24d8df2263af02f92eb72f80150e71a13f22d66f1f0b507723577bc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23a17fa6c3ade6a4207a5bbcf69033652775e60e3e4c3331acfc642150c8b1de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="messageRetentionDuration")
    def message_retention_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageRetentionDuration"))

    @message_retention_duration.setter
    def message_retention_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ab083465b27c9decd183a2dd1c239016643a800e57075dfed112a684ec509cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageRetentionDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fff2e780c9e44b984d0834eaafe66f4c7926284800bf5d3c045fcc759e6aae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__705f087c4de2a81428c1e1b494bf78d8a59e07b37dfe553dcb7c73a80ede686f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "id": "id",
        "ingestion_data_source_settings": "ingestionDataSourceSettings",
        "kms_key_name": "kmsKeyName",
        "labels": "labels",
        "message_retention_duration": "messageRetentionDuration",
        "message_storage_policy": "messageStoragePolicy",
        "message_transforms": "messageTransforms",
        "project": "project",
        "schema_settings": "schemaSettings",
        "timeouts": "timeouts",
    },
)
class GooglePubsubTopicConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        ingestion_data_source_settings: typing.Optional[typing.Union["GooglePubsubTopicIngestionDataSourceSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        message_retention_duration: typing.Optional[builtins.str] = None,
        message_storage_policy: typing.Optional[typing.Union["GooglePubsubTopicMessageStoragePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        message_transforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GooglePubsubTopicMessageTransforms", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        schema_settings: typing.Optional[typing.Union["GooglePubsubTopicSchemaSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GooglePubsubTopicTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#name GooglePubsubTopic#name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#id GooglePubsubTopic#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ingestion_data_source_settings: ingestion_data_source_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#ingestion_data_source_settings GooglePubsubTopic#ingestion_data_source_settings}
        :param kms_key_name: The resource name of the Cloud KMS CryptoKey to be used to protect access to messages published on this topic. Your project's PubSub service account ('service-{{PROJECT_NUMBER}}@gcp-sa-pubsub.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. The expected format is 'projects/* /locations/* /keyRings/* /cryptoKeys/*' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#kms_key_name GooglePubsubTopic#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param labels: A set of key/value label pairs to assign to this Topic. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#labels GooglePubsubTopic#labels}
        :param message_retention_duration: Indicates the minimum duration to retain a message after it is published to the topic. If this field is set, messages published to the topic in the last messageRetentionDuration are always available to subscribers. For instance, it allows any attached subscription to seek to a timestamp that is up to messageRetentionDuration in the past. If this field is not set, message retention is controlled by settings on individual subscriptions. The rotation period has the format of a decimal number, followed by the letter 's' (seconds). Cannot be more than 31 days or less than 10 minutes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#message_retention_duration GooglePubsubTopic#message_retention_duration}
        :param message_storage_policy: message_storage_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#message_storage_policy GooglePubsubTopic#message_storage_policy}
        :param message_transforms: message_transforms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#message_transforms GooglePubsubTopic#message_transforms}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#project GooglePubsubTopic#project}.
        :param schema_settings: schema_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#schema_settings GooglePubsubTopic#schema_settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#timeouts GooglePubsubTopic#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(ingestion_data_source_settings, dict):
            ingestion_data_source_settings = GooglePubsubTopicIngestionDataSourceSettings(**ingestion_data_source_settings)
        if isinstance(message_storage_policy, dict):
            message_storage_policy = GooglePubsubTopicMessageStoragePolicy(**message_storage_policy)
        if isinstance(schema_settings, dict):
            schema_settings = GooglePubsubTopicSchemaSettings(**schema_settings)
        if isinstance(timeouts, dict):
            timeouts = GooglePubsubTopicTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__720d9d480f91293b76fa6b5ee681be374fbeae1e414a139d606c26036fde0f9b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ingestion_data_source_settings", value=ingestion_data_source_settings, expected_type=type_hints["ingestion_data_source_settings"])
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument message_retention_duration", value=message_retention_duration, expected_type=type_hints["message_retention_duration"])
            check_type(argname="argument message_storage_policy", value=message_storage_policy, expected_type=type_hints["message_storage_policy"])
            check_type(argname="argument message_transforms", value=message_transforms, expected_type=type_hints["message_transforms"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument schema_settings", value=schema_settings, expected_type=type_hints["schema_settings"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if id is not None:
            self._values["id"] = id
        if ingestion_data_source_settings is not None:
            self._values["ingestion_data_source_settings"] = ingestion_data_source_settings
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name
        if labels is not None:
            self._values["labels"] = labels
        if message_retention_duration is not None:
            self._values["message_retention_duration"] = message_retention_duration
        if message_storage_policy is not None:
            self._values["message_storage_policy"] = message_storage_policy
        if message_transforms is not None:
            self._values["message_transforms"] = message_transforms
        if project is not None:
            self._values["project"] = project
        if schema_settings is not None:
            self._values["schema_settings"] = schema_settings
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
    def name(self) -> builtins.str:
        '''Name of the topic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#name GooglePubsubTopic#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#id GooglePubsubTopic#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingestion_data_source_settings(
        self,
    ) -> typing.Optional["GooglePubsubTopicIngestionDataSourceSettings"]:
        '''ingestion_data_source_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#ingestion_data_source_settings GooglePubsubTopic#ingestion_data_source_settings}
        '''
        result = self._values.get("ingestion_data_source_settings")
        return typing.cast(typing.Optional["GooglePubsubTopicIngestionDataSourceSettings"], result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''The resource name of the Cloud KMS CryptoKey to be used to protect access to messages published on this topic.

        Your project's PubSub service account
        ('service-{{PROJECT_NUMBER}}@gcp-sa-pubsub.iam.gserviceaccount.com') must have
        'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature.
        The expected format is 'projects/* /locations/* /keyRings/* /cryptoKeys/*'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#kms_key_name GooglePubsubTopic#kms_key_name}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs to assign to this Topic.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#labels GooglePubsubTopic#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def message_retention_duration(self) -> typing.Optional[builtins.str]:
        '''Indicates the minimum duration to retain a message after it is published to the topic.

        If this field is set, messages published to the topic in
        the last messageRetentionDuration are always available to subscribers.
        For instance, it allows any attached subscription to seek to a timestamp
        that is up to messageRetentionDuration in the past. If this field is not
        set, message retention is controlled by settings on individual subscriptions.
        The rotation period has the format of a decimal number, followed by the
        letter 's' (seconds). Cannot be more than 31 days or less than 10 minutes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#message_retention_duration GooglePubsubTopic#message_retention_duration}
        '''
        result = self._values.get("message_retention_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_storage_policy(
        self,
    ) -> typing.Optional["GooglePubsubTopicMessageStoragePolicy"]:
        '''message_storage_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#message_storage_policy GooglePubsubTopic#message_storage_policy}
        '''
        result = self._values.get("message_storage_policy")
        return typing.cast(typing.Optional["GooglePubsubTopicMessageStoragePolicy"], result)

    @builtins.property
    def message_transforms(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePubsubTopicMessageTransforms"]]]:
        '''message_transforms block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#message_transforms GooglePubsubTopic#message_transforms}
        '''
        result = self._values.get("message_transforms")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePubsubTopicMessageTransforms"]]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#project GooglePubsubTopic#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_settings(self) -> typing.Optional["GooglePubsubTopicSchemaSettings"]:
        '''schema_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#schema_settings GooglePubsubTopic#schema_settings}
        '''
        result = self._values.get("schema_settings")
        return typing.cast(typing.Optional["GooglePubsubTopicSchemaSettings"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GooglePubsubTopicTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#timeouts GooglePubsubTopic#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GooglePubsubTopicTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubTopicConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicIngestionDataSourceSettings",
    jsii_struct_bases=[],
    name_mapping={
        "aws_kinesis": "awsKinesis",
        "aws_msk": "awsMsk",
        "azure_event_hubs": "azureEventHubs",
        "cloud_storage": "cloudStorage",
        "confluent_cloud": "confluentCloud",
        "platform_logs_settings": "platformLogsSettings",
    },
)
class GooglePubsubTopicIngestionDataSourceSettings:
    def __init__(
        self,
        *,
        aws_kinesis: typing.Optional[typing.Union["GooglePubsubTopicIngestionDataSourceSettingsAwsKinesis", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_msk: typing.Optional[typing.Union["GooglePubsubTopicIngestionDataSourceSettingsAwsMsk", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_event_hubs: typing.Optional[typing.Union["GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubs", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_storage: typing.Optional[typing.Union["GooglePubsubTopicIngestionDataSourceSettingsCloudStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        confluent_cloud: typing.Optional[typing.Union["GooglePubsubTopicIngestionDataSourceSettingsConfluentCloud", typing.Dict[builtins.str, typing.Any]]] = None,
        platform_logs_settings: typing.Optional[typing.Union["GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws_kinesis: aws_kinesis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#aws_kinesis GooglePubsubTopic#aws_kinesis}
        :param aws_msk: aws_msk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#aws_msk GooglePubsubTopic#aws_msk}
        :param azure_event_hubs: azure_event_hubs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#azure_event_hubs GooglePubsubTopic#azure_event_hubs}
        :param cloud_storage: cloud_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#cloud_storage GooglePubsubTopic#cloud_storage}
        :param confluent_cloud: confluent_cloud block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#confluent_cloud GooglePubsubTopic#confluent_cloud}
        :param platform_logs_settings: platform_logs_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#platform_logs_settings GooglePubsubTopic#platform_logs_settings}
        '''
        if isinstance(aws_kinesis, dict):
            aws_kinesis = GooglePubsubTopicIngestionDataSourceSettingsAwsKinesis(**aws_kinesis)
        if isinstance(aws_msk, dict):
            aws_msk = GooglePubsubTopicIngestionDataSourceSettingsAwsMsk(**aws_msk)
        if isinstance(azure_event_hubs, dict):
            azure_event_hubs = GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubs(**azure_event_hubs)
        if isinstance(cloud_storage, dict):
            cloud_storage = GooglePubsubTopicIngestionDataSourceSettingsCloudStorage(**cloud_storage)
        if isinstance(confluent_cloud, dict):
            confluent_cloud = GooglePubsubTopicIngestionDataSourceSettingsConfluentCloud(**confluent_cloud)
        if isinstance(platform_logs_settings, dict):
            platform_logs_settings = GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettings(**platform_logs_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c3a094576b11483ba4ab0751f3db901cb929a1fe7d4f96cd2f3e2c5a9f83ca)
            check_type(argname="argument aws_kinesis", value=aws_kinesis, expected_type=type_hints["aws_kinesis"])
            check_type(argname="argument aws_msk", value=aws_msk, expected_type=type_hints["aws_msk"])
            check_type(argname="argument azure_event_hubs", value=azure_event_hubs, expected_type=type_hints["azure_event_hubs"])
            check_type(argname="argument cloud_storage", value=cloud_storage, expected_type=type_hints["cloud_storage"])
            check_type(argname="argument confluent_cloud", value=confluent_cloud, expected_type=type_hints["confluent_cloud"])
            check_type(argname="argument platform_logs_settings", value=platform_logs_settings, expected_type=type_hints["platform_logs_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_kinesis is not None:
            self._values["aws_kinesis"] = aws_kinesis
        if aws_msk is not None:
            self._values["aws_msk"] = aws_msk
        if azure_event_hubs is not None:
            self._values["azure_event_hubs"] = azure_event_hubs
        if cloud_storage is not None:
            self._values["cloud_storage"] = cloud_storage
        if confluent_cloud is not None:
            self._values["confluent_cloud"] = confluent_cloud
        if platform_logs_settings is not None:
            self._values["platform_logs_settings"] = platform_logs_settings

    @builtins.property
    def aws_kinesis(
        self,
    ) -> typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsAwsKinesis"]:
        '''aws_kinesis block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#aws_kinesis GooglePubsubTopic#aws_kinesis}
        '''
        result = self._values.get("aws_kinesis")
        return typing.cast(typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsAwsKinesis"], result)

    @builtins.property
    def aws_msk(
        self,
    ) -> typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsAwsMsk"]:
        '''aws_msk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#aws_msk GooglePubsubTopic#aws_msk}
        '''
        result = self._values.get("aws_msk")
        return typing.cast(typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsAwsMsk"], result)

    @builtins.property
    def azure_event_hubs(
        self,
    ) -> typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubs"]:
        '''azure_event_hubs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#azure_event_hubs GooglePubsubTopic#azure_event_hubs}
        '''
        result = self._values.get("azure_event_hubs")
        return typing.cast(typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubs"], result)

    @builtins.property
    def cloud_storage(
        self,
    ) -> typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsCloudStorage"]:
        '''cloud_storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#cloud_storage GooglePubsubTopic#cloud_storage}
        '''
        result = self._values.get("cloud_storage")
        return typing.cast(typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsCloudStorage"], result)

    @builtins.property
    def confluent_cloud(
        self,
    ) -> typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsConfluentCloud"]:
        '''confluent_cloud block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#confluent_cloud GooglePubsubTopic#confluent_cloud}
        '''
        result = self._values.get("confluent_cloud")
        return typing.cast(typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsConfluentCloud"], result)

    @builtins.property
    def platform_logs_settings(
        self,
    ) -> typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettings"]:
        '''platform_logs_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#platform_logs_settings GooglePubsubTopic#platform_logs_settings}
        '''
        result = self._values.get("platform_logs_settings")
        return typing.cast(typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubTopicIngestionDataSourceSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicIngestionDataSourceSettingsAwsKinesis",
    jsii_struct_bases=[],
    name_mapping={
        "aws_role_arn": "awsRoleArn",
        "consumer_arn": "consumerArn",
        "gcp_service_account": "gcpServiceAccount",
        "stream_arn": "streamArn",
    },
)
class GooglePubsubTopicIngestionDataSourceSettingsAwsKinesis:
    def __init__(
        self,
        *,
        aws_role_arn: builtins.str,
        consumer_arn: builtins.str,
        gcp_service_account: builtins.str,
        stream_arn: builtins.str,
    ) -> None:
        '''
        :param aws_role_arn: AWS role ARN to be used for Federated Identity authentication with Kinesis. Check the Pub/Sub docs for how to set up this role and the required permissions that need to be attached to it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#aws_role_arn GooglePubsubTopic#aws_role_arn}
        :param consumer_arn: The Kinesis consumer ARN to used for ingestion in Enhanced Fan-Out mode. The consumer must be already created and ready to be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#consumer_arn GooglePubsubTopic#consumer_arn}
        :param gcp_service_account: The GCP service account to be used for Federated Identity authentication with Kinesis (via a 'AssumeRoleWithWebIdentity' call for the provided role). The 'awsRoleArn' must be set up with 'accounts.google.com:sub' equals to this service account number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#gcp_service_account GooglePubsubTopic#gcp_service_account}
        :param stream_arn: The Kinesis stream ARN to ingest data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#stream_arn GooglePubsubTopic#stream_arn}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5f4d5cca52d9ab0c04e5d7bd7db673db00f07749711f720b2596e1c270dfbe2)
            check_type(argname="argument aws_role_arn", value=aws_role_arn, expected_type=type_hints["aws_role_arn"])
            check_type(argname="argument consumer_arn", value=consumer_arn, expected_type=type_hints["consumer_arn"])
            check_type(argname="argument gcp_service_account", value=gcp_service_account, expected_type=type_hints["gcp_service_account"])
            check_type(argname="argument stream_arn", value=stream_arn, expected_type=type_hints["stream_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_role_arn": aws_role_arn,
            "consumer_arn": consumer_arn,
            "gcp_service_account": gcp_service_account,
            "stream_arn": stream_arn,
        }

    @builtins.property
    def aws_role_arn(self) -> builtins.str:
        '''AWS role ARN to be used for Federated Identity authentication with Kinesis.

        Check the Pub/Sub docs for how to set up this role and the
        required permissions that need to be attached to it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#aws_role_arn GooglePubsubTopic#aws_role_arn}
        '''
        result = self._values.get("aws_role_arn")
        assert result is not None, "Required property 'aws_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def consumer_arn(self) -> builtins.str:
        '''The Kinesis consumer ARN to used for ingestion in Enhanced Fan-Out mode.

        The consumer must be already
        created and ready to be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#consumer_arn GooglePubsubTopic#consumer_arn}
        '''
        result = self._values.get("consumer_arn")
        assert result is not None, "Required property 'consumer_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gcp_service_account(self) -> builtins.str:
        '''The GCP service account to be used for Federated Identity authentication with Kinesis (via a 'AssumeRoleWithWebIdentity' call for the provided role).

        The 'awsRoleArn' must be set up with 'accounts.google.com:sub'
        equals to this service account number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#gcp_service_account GooglePubsubTopic#gcp_service_account}
        '''
        result = self._values.get("gcp_service_account")
        assert result is not None, "Required property 'gcp_service_account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stream_arn(self) -> builtins.str:
        '''The Kinesis stream ARN to ingest data from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#stream_arn GooglePubsubTopic#stream_arn}
        '''
        result = self._values.get("stream_arn")
        assert result is not None, "Required property 'stream_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubTopicIngestionDataSourceSettingsAwsKinesis(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubTopicIngestionDataSourceSettingsAwsKinesisOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicIngestionDataSourceSettingsAwsKinesisOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ac1b676ae7841393afe443c5a41029604a1b20fa3c6d16e617a1ee9d07e6b1f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="awsRoleArnInput")
    def aws_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerArnInput")
    def consumer_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerArnInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountInput")
    def gcp_service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcpServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="streamArnInput")
    def stream_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamArnInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRoleArn")
    def aws_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsRoleArn"))

    @aws_role_arn.setter
    def aws_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69209bb1c2e8aead3101f8f5d8d76dbefd8849ec555c2b4cd1d931a52c3e1330)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerArn")
    def consumer_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerArn"))

    @consumer_arn.setter
    def consumer_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eaa8ff34b0446efe283f109f135ddbad3076fed32a4508ce2b50056e0b7af49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccount")
    def gcp_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpServiceAccount"))

    @gcp_service_account.setter
    def gcp_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afd86bec2312898f7009436a5b0635c89595c3dd49ea49f235e08a450bd3b152)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streamArn")
    def stream_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streamArn"))

    @stream_arn.setter
    def stream_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43e3ccc619827f095bed6f0789fde278b8647d50309c59865b2d7006fbb262a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsAwsKinesis]:
        return typing.cast(typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsAwsKinesis], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsAwsKinesis],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2183cf0be596ce715498ca862647dffcdf82bf3ac8577f259117f8ae71099667)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicIngestionDataSourceSettingsAwsMsk",
    jsii_struct_bases=[],
    name_mapping={
        "aws_role_arn": "awsRoleArn",
        "cluster_arn": "clusterArn",
        "gcp_service_account": "gcpServiceAccount",
        "topic": "topic",
    },
)
class GooglePubsubTopicIngestionDataSourceSettingsAwsMsk:
    def __init__(
        self,
        *,
        aws_role_arn: builtins.str,
        cluster_arn: builtins.str,
        gcp_service_account: builtins.str,
        topic: builtins.str,
    ) -> None:
        '''
        :param aws_role_arn: AWS role ARN to be used for Federated Identity authentication with MSK. Check the Pub/Sub docs for how to set up this role and the required permissions that need to be attached to it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#aws_role_arn GooglePubsubTopic#aws_role_arn}
        :param cluster_arn: ARN that uniquely identifies the MSK cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#cluster_arn GooglePubsubTopic#cluster_arn}
        :param gcp_service_account: The GCP service account to be used for Federated Identity authentication with MSK (via a 'AssumeRoleWithWebIdentity' call for the provided role). The 'awsRoleArn' must be set up with 'accounts.google.com:sub' equals to this service account number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#gcp_service_account GooglePubsubTopic#gcp_service_account}
        :param topic: The name of the MSK topic that Pub/Sub will import from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#topic GooglePubsubTopic#topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edbd2270d2eb46f845bf56baca0ec93791dbc5a5ffa8367294bd1c1d0caecf66)
            check_type(argname="argument aws_role_arn", value=aws_role_arn, expected_type=type_hints["aws_role_arn"])
            check_type(argname="argument cluster_arn", value=cluster_arn, expected_type=type_hints["cluster_arn"])
            check_type(argname="argument gcp_service_account", value=gcp_service_account, expected_type=type_hints["gcp_service_account"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_role_arn": aws_role_arn,
            "cluster_arn": cluster_arn,
            "gcp_service_account": gcp_service_account,
            "topic": topic,
        }

    @builtins.property
    def aws_role_arn(self) -> builtins.str:
        '''AWS role ARN to be used for Federated Identity authentication with MSK.

        Check the Pub/Sub docs for how to set up this role and the
        required permissions that need to be attached to it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#aws_role_arn GooglePubsubTopic#aws_role_arn}
        '''
        result = self._values.get("aws_role_arn")
        assert result is not None, "Required property 'aws_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_arn(self) -> builtins.str:
        '''ARN that uniquely identifies the MSK cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#cluster_arn GooglePubsubTopic#cluster_arn}
        '''
        result = self._values.get("cluster_arn")
        assert result is not None, "Required property 'cluster_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gcp_service_account(self) -> builtins.str:
        '''The GCP service account to be used for Federated Identity authentication with MSK (via a 'AssumeRoleWithWebIdentity' call for the provided role).

        The 'awsRoleArn' must be set up with 'accounts.google.com:sub'
        equals to this service account number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#gcp_service_account GooglePubsubTopic#gcp_service_account}
        '''
        result = self._values.get("gcp_service_account")
        assert result is not None, "Required property 'gcp_service_account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''The name of the MSK topic that Pub/Sub will import from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#topic GooglePubsubTopic#topic}
        '''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubTopicIngestionDataSourceSettingsAwsMsk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubTopicIngestionDataSourceSettingsAwsMskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicIngestionDataSourceSettingsAwsMskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c3b6e24cd4829b566a612ad474eb4894b71e56030f471d50b1b4e56fecd893d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="awsRoleArnInput")
    def aws_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterArnInput")
    def cluster_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterArnInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountInput")
    def gcp_service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcpServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRoleArn")
    def aws_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsRoleArn"))

    @aws_role_arn.setter
    def aws_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__623a2d5f9fc1eaa57ff5df188f8c94f72802c0671235f2034c543e2d1f937168)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterArn"))

    @cluster_arn.setter
    def cluster_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85e8423a6446833f5fea91204bc71ed541c367c4378b06d6cbb412692b6496ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccount")
    def gcp_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpServiceAccount"))

    @gcp_service_account.setter
    def gcp_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c1438278e728cf930ced0ad728624f5339da16350cecb83b70121594aea4c12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f3ed3a5e9845da1d472475493d3f72ffb3972e131a6eb16196434c9095d2b34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsAwsMsk]:
        return typing.cast(typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsAwsMsk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsAwsMsk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__033a2cef3c9adcc1f8a3bc78bd88054700a9a015b18be50d03b81f00d27e6c56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubs",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "event_hub": "eventHub",
        "gcp_service_account": "gcpServiceAccount",
        "namespace": "namespace",
        "resource_group": "resourceGroup",
        "subscription_id": "subscriptionId",
        "tenant_id": "tenantId",
    },
)
class GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubs:
    def __init__(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        event_hub: typing.Optional[builtins.str] = None,
        gcp_service_account: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        resource_group: typing.Optional[builtins.str] = None,
        subscription_id: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: The Azure event hub client ID to use for ingestion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#client_id GooglePubsubTopic#client_id}
        :param event_hub: The Azure event hub to ingest data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#event_hub GooglePubsubTopic#event_hub}
        :param gcp_service_account: The GCP service account to be used for Federated Identity authentication with Azure (via a 'AssumeRoleWithWebIdentity' call for the provided role). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#gcp_service_account GooglePubsubTopic#gcp_service_account}
        :param namespace: The Azure event hub namespace to ingest data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#namespace GooglePubsubTopic#namespace}
        :param resource_group: The name of the resource group within an Azure subscription. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#resource_group GooglePubsubTopic#resource_group}
        :param subscription_id: The Azure event hub subscription ID to use for ingestion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#subscription_id GooglePubsubTopic#subscription_id}
        :param tenant_id: The Azure event hub tenant ID to use for ingestion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#tenant_id GooglePubsubTopic#tenant_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e11216acbae1d118c39566571d32acfde2b56c52841b9e2adafe7b2ef6460b94)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument event_hub", value=event_hub, expected_type=type_hints["event_hub"])
            check_type(argname="argument gcp_service_account", value=gcp_service_account, expected_type=type_hints["gcp_service_account"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument subscription_id", value=subscription_id, expected_type=type_hints["subscription_id"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_id is not None:
            self._values["client_id"] = client_id
        if event_hub is not None:
            self._values["event_hub"] = event_hub
        if gcp_service_account is not None:
            self._values["gcp_service_account"] = gcp_service_account
        if namespace is not None:
            self._values["namespace"] = namespace
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if subscription_id is not None:
            self._values["subscription_id"] = subscription_id
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''The Azure event hub client ID to use for ingestion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#client_id GooglePubsubTopic#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_hub(self) -> typing.Optional[builtins.str]:
        '''The Azure event hub to ingest data from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#event_hub GooglePubsubTopic#event_hub}
        '''
        result = self._values.get("event_hub")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcp_service_account(self) -> typing.Optional[builtins.str]:
        '''The GCP service account to be used for Federated Identity authentication with Azure (via a 'AssumeRoleWithWebIdentity' call for the provided role).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#gcp_service_account GooglePubsubTopic#gcp_service_account}
        '''
        result = self._values.get("gcp_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The Azure event hub namespace to ingest data from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#namespace GooglePubsubTopic#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_group(self) -> typing.Optional[builtins.str]:
        '''The name of the resource group within an Azure subscription.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#resource_group GooglePubsubTopic#resource_group}
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscription_id(self) -> typing.Optional[builtins.str]:
        '''The Azure event hub subscription ID to use for ingestion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#subscription_id GooglePubsubTopic#subscription_id}
        '''
        result = self._values.get("subscription_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''The Azure event hub tenant ID to use for ingestion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#tenant_id GooglePubsubTopic#tenant_id}
        '''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a488d3998c131fd16fa283cc686781fd7b9cfeec58b8e200f2767940c76fd58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetEventHub")
    def reset_event_hub(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventHub", []))

    @jsii.member(jsii_name="resetGcpServiceAccount")
    def reset_gcp_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpServiceAccount", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @jsii.member(jsii_name="resetResourceGroup")
    def reset_resource_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroup", []))

    @jsii.member(jsii_name="resetSubscriptionId")
    def reset_subscription_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubscriptionId", []))

    @jsii.member(jsii_name="resetTenantId")
    def reset_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantId", []))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="eventHubInput")
    def event_hub_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventHubInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountInput")
    def gcp_service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcpServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupInput")
    def resource_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="subscriptionIdInput")
    def subscription_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subscriptionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cac61e19f694f92981808198739fb9a8e10a65fd174bf589209d315522da23ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventHub")
    def event_hub(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventHub"))

    @event_hub.setter
    def event_hub(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9557dad704df20b4b329e35be5c6705b9a27f38fda44ea6bdeb8b3edc7ecf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventHub", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccount")
    def gcp_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpServiceAccount"))

    @gcp_service_account.setter
    def gcp_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39d6d6676519f1bddd20a5def6a1d5e802937bb2a77902027c2266aa32aa9826)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__131c4bd3cf48af23a72048c99e5e4c1f23cefcad5b1ed3f2695ea53008c90b5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroup")
    def resource_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroup"))

    @resource_group.setter
    def resource_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5df0f79307e5ed17762ef5c55555962b562fe7b053b87561f4c4e7ab7f5712be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subscriptionId")
    def subscription_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subscriptionId"))

    @subscription_id.setter
    def subscription_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68148d043c966dc6ed158125a8622c57e1639e8b01f13d0e1bfbbcdd785f7597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscriptionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d93fc555bbfbc205254daf74cc8cb7532cc35d1e7b769a776f04168b0d53c0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubs]:
        return typing.cast(typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17da9ae63be4b72ff556d75a8b7210b26f65b21e2d832108a8edc9d04065598a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicIngestionDataSourceSettingsCloudStorage",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "avro_format": "avroFormat",
        "match_glob": "matchGlob",
        "minimum_object_create_time": "minimumObjectCreateTime",
        "pubsub_avro_format": "pubsubAvroFormat",
        "text_format": "textFormat",
    },
)
class GooglePubsubTopicIngestionDataSourceSettingsCloudStorage:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        avro_format: typing.Optional[typing.Union["GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat", typing.Dict[builtins.str, typing.Any]]] = None,
        match_glob: typing.Optional[builtins.str] = None,
        minimum_object_create_time: typing.Optional[builtins.str] = None,
        pubsub_avro_format: typing.Optional[typing.Union["GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat", typing.Dict[builtins.str, typing.Any]]] = None,
        text_format: typing.Optional[typing.Union["GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket: Cloud Storage bucket. The bucket name must be without any prefix like "gs://". See the bucket naming requirements: https://cloud.google.com/storage/docs/buckets#naming. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#bucket GooglePubsubTopic#bucket}
        :param avro_format: avro_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#avro_format GooglePubsubTopic#avro_format}
        :param match_glob: Glob pattern used to match objects that will be ingested. If unset, all objects will be ingested. See the supported patterns: https://cloud.google.com/storage/docs/json_api/v1/objects/list#list-objects-and-prefixes-using-glob Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#match_glob GooglePubsubTopic#match_glob}
        :param minimum_object_create_time: The timestamp set in RFC3339 text format. If set, only objects with a larger or equal timestamp will be ingested. Unset by default, meaning all objects will be ingested. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#minimum_object_create_time GooglePubsubTopic#minimum_object_create_time}
        :param pubsub_avro_format: pubsub_avro_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#pubsub_avro_format GooglePubsubTopic#pubsub_avro_format}
        :param text_format: text_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#text_format GooglePubsubTopic#text_format}
        '''
        if isinstance(avro_format, dict):
            avro_format = GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat(**avro_format)
        if isinstance(pubsub_avro_format, dict):
            pubsub_avro_format = GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat(**pubsub_avro_format)
        if isinstance(text_format, dict):
            text_format = GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat(**text_format)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__807900dd63741444c9a0f0c46cb3a0ce212981d1d4d80e1e0b41e67c833d5ec6)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument avro_format", value=avro_format, expected_type=type_hints["avro_format"])
            check_type(argname="argument match_glob", value=match_glob, expected_type=type_hints["match_glob"])
            check_type(argname="argument minimum_object_create_time", value=minimum_object_create_time, expected_type=type_hints["minimum_object_create_time"])
            check_type(argname="argument pubsub_avro_format", value=pubsub_avro_format, expected_type=type_hints["pubsub_avro_format"])
            check_type(argname="argument text_format", value=text_format, expected_type=type_hints["text_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if avro_format is not None:
            self._values["avro_format"] = avro_format
        if match_glob is not None:
            self._values["match_glob"] = match_glob
        if minimum_object_create_time is not None:
            self._values["minimum_object_create_time"] = minimum_object_create_time
        if pubsub_avro_format is not None:
            self._values["pubsub_avro_format"] = pubsub_avro_format
        if text_format is not None:
            self._values["text_format"] = text_format

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Cloud Storage bucket. The bucket name must be without any prefix like "gs://". See the bucket naming requirements: https://cloud.google.com/storage/docs/buckets#naming.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#bucket GooglePubsubTopic#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def avro_format(
        self,
    ) -> typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat"]:
        '''avro_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#avro_format GooglePubsubTopic#avro_format}
        '''
        result = self._values.get("avro_format")
        return typing.cast(typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat"], result)

    @builtins.property
    def match_glob(self) -> typing.Optional[builtins.str]:
        '''Glob pattern used to match objects that will be ingested.

        If unset, all
        objects will be ingested. See the supported patterns:
        https://cloud.google.com/storage/docs/json_api/v1/objects/list#list-objects-and-prefixes-using-glob

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#match_glob GooglePubsubTopic#match_glob}
        '''
        result = self._values.get("match_glob")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum_object_create_time(self) -> typing.Optional[builtins.str]:
        '''The timestamp set in RFC3339 text format.

        If set, only objects with a
        larger or equal timestamp will be ingested. Unset by default, meaning
        all objects will be ingested.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#minimum_object_create_time GooglePubsubTopic#minimum_object_create_time}
        '''
        result = self._values.get("minimum_object_create_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pubsub_avro_format(
        self,
    ) -> typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat"]:
        '''pubsub_avro_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#pubsub_avro_format GooglePubsubTopic#pubsub_avro_format}
        '''
        result = self._values.get("pubsub_avro_format")
        return typing.cast(typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat"], result)

    @builtins.property
    def text_format(
        self,
    ) -> typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat"]:
        '''text_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#text_format GooglePubsubTopic#text_format}
        '''
        result = self._values.get("text_format")
        return typing.cast(typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubTopicIngestionDataSourceSettingsCloudStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e21aa324562185a133696b3df13020c89ddbf1d9037a2d109f225c8e0a139e2d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat]:
        return typing.cast(typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3e8b29eb1c8c0451b7f57700541831311a5f0dd342a5d3b814fdac2f62ac0b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePubsubTopicIngestionDataSourceSettingsCloudStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicIngestionDataSourceSettingsCloudStorageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f5c1fe7dec3dcfc6a62b9f8982bc30e70de2d5bf9bd743dbe49de0fbb6d1e34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAvroFormat")
    def put_avro_format(self) -> None:
        value = GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat()

        return typing.cast(None, jsii.invoke(self, "putAvroFormat", [value]))

    @jsii.member(jsii_name="putPubsubAvroFormat")
    def put_pubsub_avro_format(self) -> None:
        value = GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat()

        return typing.cast(None, jsii.invoke(self, "putPubsubAvroFormat", [value]))

    @jsii.member(jsii_name="putTextFormat")
    def put_text_format(
        self,
        *,
        delimiter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delimiter: The delimiter to use when using the 'text' format. Each line of text as specified by the delimiter will be set to the 'data' field of a Pub/Sub message. When unset, '\\n' is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#delimiter GooglePubsubTopic#delimiter}
        '''
        value = GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat(
            delimiter=delimiter
        )

        return typing.cast(None, jsii.invoke(self, "putTextFormat", [value]))

    @jsii.member(jsii_name="resetAvroFormat")
    def reset_avro_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvroFormat", []))

    @jsii.member(jsii_name="resetMatchGlob")
    def reset_match_glob(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchGlob", []))

    @jsii.member(jsii_name="resetMinimumObjectCreateTime")
    def reset_minimum_object_create_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumObjectCreateTime", []))

    @jsii.member(jsii_name="resetPubsubAvroFormat")
    def reset_pubsub_avro_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPubsubAvroFormat", []))

    @jsii.member(jsii_name="resetTextFormat")
    def reset_text_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTextFormat", []))

    @builtins.property
    @jsii.member(jsii_name="avroFormat")
    def avro_format(
        self,
    ) -> GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormatOutputReference:
        return typing.cast(GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormatOutputReference, jsii.get(self, "avroFormat"))

    @builtins.property
    @jsii.member(jsii_name="pubsubAvroFormat")
    def pubsub_avro_format(
        self,
    ) -> "GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormatOutputReference":
        return typing.cast("GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormatOutputReference", jsii.get(self, "pubsubAvroFormat"))

    @builtins.property
    @jsii.member(jsii_name="textFormat")
    def text_format(
        self,
    ) -> "GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormatOutputReference":
        return typing.cast("GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormatOutputReference", jsii.get(self, "textFormat"))

    @builtins.property
    @jsii.member(jsii_name="avroFormatInput")
    def avro_format_input(
        self,
    ) -> typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat]:
        return typing.cast(typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat], jsii.get(self, "avroFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="matchGlobInput")
    def match_glob_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchGlobInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumObjectCreateTimeInput")
    def minimum_object_create_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimumObjectCreateTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="pubsubAvroFormatInput")
    def pubsub_avro_format_input(
        self,
    ) -> typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat"]:
        return typing.cast(typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat"], jsii.get(self, "pubsubAvroFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="textFormatInput")
    def text_format_input(
        self,
    ) -> typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat"]:
        return typing.cast(typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat"], jsii.get(self, "textFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6809a2118460757fb076fbb895be7de9f3a1bba6478cd534b100d44886a1971e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchGlob")
    def match_glob(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchGlob"))

    @match_glob.setter
    def match_glob(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b304073a305984ebf91f6c2ea08672de71cecb6080a9b0e4ca45e5c6131e76c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchGlob", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumObjectCreateTime")
    def minimum_object_create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumObjectCreateTime"))

    @minimum_object_create_time.setter
    def minimum_object_create_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6d9ee4c20ce87d3f5d9c80e318f362b349a2f22330a941b7ee00120329dcda6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumObjectCreateTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsCloudStorage]:
        return typing.cast(typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsCloudStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsCloudStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c33891a99ed51f05fa56e5b19b1dbaa9e9361a57aeac68791e034419b01ea2cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39dd7ecccb719b2efe989c432d961500e3936fe4914479b9747ae4a942e1d3a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat]:
        return typing.cast(typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee885ef75e41bebfbfa1884c47407d312f5fecb9d4ea9cd2b783abc8e7251580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat",
    jsii_struct_bases=[],
    name_mapping={"delimiter": "delimiter"},
)
class GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat:
    def __init__(self, *, delimiter: typing.Optional[builtins.str] = None) -> None:
        '''
        :param delimiter: The delimiter to use when using the 'text' format. Each line of text as specified by the delimiter will be set to the 'data' field of a Pub/Sub message. When unset, '\\n' is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#delimiter GooglePubsubTopic#delimiter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0ab88efc2d68ce20733d84e69a37638b0f8e80475b3f6a55dbce706ac1947ab)
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delimiter is not None:
            self._values["delimiter"] = delimiter

    @builtins.property
    def delimiter(self) -> typing.Optional[builtins.str]:
        '''The delimiter to use when using the 'text' format.

        Each line of text as
        specified by the delimiter will be set to the 'data' field of a Pub/Sub
        message. When unset, '\\n' is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#delimiter GooglePubsubTopic#delimiter}
        '''
        result = self._values.get("delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18e3ea52e7bc374e2cabdf385b6ced8a9f4c1553013a8acb0962eb7cb8884365)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDelimiter")
    def reset_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelimiter", []))

    @builtins.property
    @jsii.member(jsii_name="delimiterInput")
    def delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="delimiter")
    def delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delimiter"))

    @delimiter.setter
    def delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6410e699e88fffcb58d36836f856eda698148e432ab5459aed91babbdbd79e78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat]:
        return typing.cast(typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1200dc7eb613a24ab7032f734791f451ccf524590a841ce92678960a5117aaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicIngestionDataSourceSettingsConfluentCloud",
    jsii_struct_bases=[],
    name_mapping={
        "bootstrap_server": "bootstrapServer",
        "gcp_service_account": "gcpServiceAccount",
        "identity_pool_id": "identityPoolId",
        "topic": "topic",
        "cluster_id": "clusterId",
    },
)
class GooglePubsubTopicIngestionDataSourceSettingsConfluentCloud:
    def __init__(
        self,
        *,
        bootstrap_server: builtins.str,
        gcp_service_account: builtins.str,
        identity_pool_id: builtins.str,
        topic: builtins.str,
        cluster_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bootstrap_server: The Confluent Cloud bootstrap server. The format is url:port. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#bootstrap_server GooglePubsubTopic#bootstrap_server}
        :param gcp_service_account: The GCP service account to be used for Federated Identity authentication with Confluent Cloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#gcp_service_account GooglePubsubTopic#gcp_service_account}
        :param identity_pool_id: Identity pool ID to be used for Federated Identity authentication with Confluent Cloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#identity_pool_id GooglePubsubTopic#identity_pool_id}
        :param topic: Name of the Confluent Cloud topic that Pub/Sub will import from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#topic GooglePubsubTopic#topic}
        :param cluster_id: The Confluent Cloud cluster ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#cluster_id GooglePubsubTopic#cluster_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eec81b754bd9c0c299c961b8e9c2823ee7963fb4da073442e6139571739218d6)
            check_type(argname="argument bootstrap_server", value=bootstrap_server, expected_type=type_hints["bootstrap_server"])
            check_type(argname="argument gcp_service_account", value=gcp_service_account, expected_type=type_hints["gcp_service_account"])
            check_type(argname="argument identity_pool_id", value=identity_pool_id, expected_type=type_hints["identity_pool_id"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bootstrap_server": bootstrap_server,
            "gcp_service_account": gcp_service_account,
            "identity_pool_id": identity_pool_id,
            "topic": topic,
        }
        if cluster_id is not None:
            self._values["cluster_id"] = cluster_id

    @builtins.property
    def bootstrap_server(self) -> builtins.str:
        '''The Confluent Cloud bootstrap server. The format is url:port.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#bootstrap_server GooglePubsubTopic#bootstrap_server}
        '''
        result = self._values.get("bootstrap_server")
        assert result is not None, "Required property 'bootstrap_server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gcp_service_account(self) -> builtins.str:
        '''The GCP service account to be used for Federated Identity authentication with Confluent Cloud.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#gcp_service_account GooglePubsubTopic#gcp_service_account}
        '''
        result = self._values.get("gcp_service_account")
        assert result is not None, "Required property 'gcp_service_account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_pool_id(self) -> builtins.str:
        '''Identity pool ID to be used for Federated Identity authentication with Confluent Cloud.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#identity_pool_id GooglePubsubTopic#identity_pool_id}
        '''
        result = self._values.get("identity_pool_id")
        assert result is not None, "Required property 'identity_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''Name of the Confluent Cloud topic that Pub/Sub will import from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#topic GooglePubsubTopic#topic}
        '''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_id(self) -> typing.Optional[builtins.str]:
        '''The Confluent Cloud cluster ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#cluster_id GooglePubsubTopic#cluster_id}
        '''
        result = self._values.get("cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubTopicIngestionDataSourceSettingsConfluentCloud(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubTopicIngestionDataSourceSettingsConfluentCloudOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicIngestionDataSourceSettingsConfluentCloudOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c4270ed2e8b408d3a366da4208067f6f066dc206d38dc862c8fb3cfa44b6294)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClusterId")
    def reset_cluster_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterId", []))

    @builtins.property
    @jsii.member(jsii_name="bootstrapServerInput")
    def bootstrap_server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootstrapServerInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountInput")
    def gcp_service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcpServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="identityPoolIdInput")
    def identity_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="bootstrapServer")
    def bootstrap_server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootstrapServer"))

    @bootstrap_server.setter
    def bootstrap_server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2717a45a8ee2d077807a63ee02720aa2457720d94680cba027d289a20db8a51e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootstrapServer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a903d1f1de551970329999e891b8214a6315d2721282d014898de2be732ea9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccount")
    def gcp_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpServiceAccount"))

    @gcp_service_account.setter
    def gcp_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a35d54b511917bed9e2f95c71e1ff16c8c4883eecc298d2a22909b00eb6cc5ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityPoolId")
    def identity_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityPoolId"))

    @identity_pool_id.setter
    def identity_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__314f278ed19f7359625f089742080a51dadec3b0418662319e41020a38e1c615)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityPoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfd867c9063082259c6095912c4267170914a42d569a2e887b99c3404a30691f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsConfluentCloud]:
        return typing.cast(typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsConfluentCloud], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsConfluentCloud],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0fefd9917b9b4dc47c2c70bb4fef710eb02ab76018410fb5649b7b790f1e594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePubsubTopicIngestionDataSourceSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicIngestionDataSourceSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8962a5458e42c165bbad5fb45a5c9cd479a9adaf50c44b625f046fbcb2d8c1c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAwsKinesis")
    def put_aws_kinesis(
        self,
        *,
        aws_role_arn: builtins.str,
        consumer_arn: builtins.str,
        gcp_service_account: builtins.str,
        stream_arn: builtins.str,
    ) -> None:
        '''
        :param aws_role_arn: AWS role ARN to be used for Federated Identity authentication with Kinesis. Check the Pub/Sub docs for how to set up this role and the required permissions that need to be attached to it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#aws_role_arn GooglePubsubTopic#aws_role_arn}
        :param consumer_arn: The Kinesis consumer ARN to used for ingestion in Enhanced Fan-Out mode. The consumer must be already created and ready to be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#consumer_arn GooglePubsubTopic#consumer_arn}
        :param gcp_service_account: The GCP service account to be used for Federated Identity authentication with Kinesis (via a 'AssumeRoleWithWebIdentity' call for the provided role). The 'awsRoleArn' must be set up with 'accounts.google.com:sub' equals to this service account number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#gcp_service_account GooglePubsubTopic#gcp_service_account}
        :param stream_arn: The Kinesis stream ARN to ingest data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#stream_arn GooglePubsubTopic#stream_arn}
        '''
        value = GooglePubsubTopicIngestionDataSourceSettingsAwsKinesis(
            aws_role_arn=aws_role_arn,
            consumer_arn=consumer_arn,
            gcp_service_account=gcp_service_account,
            stream_arn=stream_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putAwsKinesis", [value]))

    @jsii.member(jsii_name="putAwsMsk")
    def put_aws_msk(
        self,
        *,
        aws_role_arn: builtins.str,
        cluster_arn: builtins.str,
        gcp_service_account: builtins.str,
        topic: builtins.str,
    ) -> None:
        '''
        :param aws_role_arn: AWS role ARN to be used for Federated Identity authentication with MSK. Check the Pub/Sub docs for how to set up this role and the required permissions that need to be attached to it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#aws_role_arn GooglePubsubTopic#aws_role_arn}
        :param cluster_arn: ARN that uniquely identifies the MSK cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#cluster_arn GooglePubsubTopic#cluster_arn}
        :param gcp_service_account: The GCP service account to be used for Federated Identity authentication with MSK (via a 'AssumeRoleWithWebIdentity' call for the provided role). The 'awsRoleArn' must be set up with 'accounts.google.com:sub' equals to this service account number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#gcp_service_account GooglePubsubTopic#gcp_service_account}
        :param topic: The name of the MSK topic that Pub/Sub will import from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#topic GooglePubsubTopic#topic}
        '''
        value = GooglePubsubTopicIngestionDataSourceSettingsAwsMsk(
            aws_role_arn=aws_role_arn,
            cluster_arn=cluster_arn,
            gcp_service_account=gcp_service_account,
            topic=topic,
        )

        return typing.cast(None, jsii.invoke(self, "putAwsMsk", [value]))

    @jsii.member(jsii_name="putAzureEventHubs")
    def put_azure_event_hubs(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        event_hub: typing.Optional[builtins.str] = None,
        gcp_service_account: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        resource_group: typing.Optional[builtins.str] = None,
        subscription_id: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: The Azure event hub client ID to use for ingestion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#client_id GooglePubsubTopic#client_id}
        :param event_hub: The Azure event hub to ingest data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#event_hub GooglePubsubTopic#event_hub}
        :param gcp_service_account: The GCP service account to be used for Federated Identity authentication with Azure (via a 'AssumeRoleWithWebIdentity' call for the provided role). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#gcp_service_account GooglePubsubTopic#gcp_service_account}
        :param namespace: The Azure event hub namespace to ingest data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#namespace GooglePubsubTopic#namespace}
        :param resource_group: The name of the resource group within an Azure subscription. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#resource_group GooglePubsubTopic#resource_group}
        :param subscription_id: The Azure event hub subscription ID to use for ingestion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#subscription_id GooglePubsubTopic#subscription_id}
        :param tenant_id: The Azure event hub tenant ID to use for ingestion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#tenant_id GooglePubsubTopic#tenant_id}
        '''
        value = GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubs(
            client_id=client_id,
            event_hub=event_hub,
            gcp_service_account=gcp_service_account,
            namespace=namespace,
            resource_group=resource_group,
            subscription_id=subscription_id,
            tenant_id=tenant_id,
        )

        return typing.cast(None, jsii.invoke(self, "putAzureEventHubs", [value]))

    @jsii.member(jsii_name="putCloudStorage")
    def put_cloud_storage(
        self,
        *,
        bucket: builtins.str,
        avro_format: typing.Optional[typing.Union[GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat, typing.Dict[builtins.str, typing.Any]]] = None,
        match_glob: typing.Optional[builtins.str] = None,
        minimum_object_create_time: typing.Optional[builtins.str] = None,
        pubsub_avro_format: typing.Optional[typing.Union[GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat, typing.Dict[builtins.str, typing.Any]]] = None,
        text_format: typing.Optional[typing.Union[GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket: Cloud Storage bucket. The bucket name must be without any prefix like "gs://". See the bucket naming requirements: https://cloud.google.com/storage/docs/buckets#naming. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#bucket GooglePubsubTopic#bucket}
        :param avro_format: avro_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#avro_format GooglePubsubTopic#avro_format}
        :param match_glob: Glob pattern used to match objects that will be ingested. If unset, all objects will be ingested. See the supported patterns: https://cloud.google.com/storage/docs/json_api/v1/objects/list#list-objects-and-prefixes-using-glob Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#match_glob GooglePubsubTopic#match_glob}
        :param minimum_object_create_time: The timestamp set in RFC3339 text format. If set, only objects with a larger or equal timestamp will be ingested. Unset by default, meaning all objects will be ingested. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#minimum_object_create_time GooglePubsubTopic#minimum_object_create_time}
        :param pubsub_avro_format: pubsub_avro_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#pubsub_avro_format GooglePubsubTopic#pubsub_avro_format}
        :param text_format: text_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#text_format GooglePubsubTopic#text_format}
        '''
        value = GooglePubsubTopicIngestionDataSourceSettingsCloudStorage(
            bucket=bucket,
            avro_format=avro_format,
            match_glob=match_glob,
            minimum_object_create_time=minimum_object_create_time,
            pubsub_avro_format=pubsub_avro_format,
            text_format=text_format,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudStorage", [value]))

    @jsii.member(jsii_name="putConfluentCloud")
    def put_confluent_cloud(
        self,
        *,
        bootstrap_server: builtins.str,
        gcp_service_account: builtins.str,
        identity_pool_id: builtins.str,
        topic: builtins.str,
        cluster_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bootstrap_server: The Confluent Cloud bootstrap server. The format is url:port. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#bootstrap_server GooglePubsubTopic#bootstrap_server}
        :param gcp_service_account: The GCP service account to be used for Federated Identity authentication with Confluent Cloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#gcp_service_account GooglePubsubTopic#gcp_service_account}
        :param identity_pool_id: Identity pool ID to be used for Federated Identity authentication with Confluent Cloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#identity_pool_id GooglePubsubTopic#identity_pool_id}
        :param topic: Name of the Confluent Cloud topic that Pub/Sub will import from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#topic GooglePubsubTopic#topic}
        :param cluster_id: The Confluent Cloud cluster ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#cluster_id GooglePubsubTopic#cluster_id}
        '''
        value = GooglePubsubTopicIngestionDataSourceSettingsConfluentCloud(
            bootstrap_server=bootstrap_server,
            gcp_service_account=gcp_service_account,
            identity_pool_id=identity_pool_id,
            topic=topic,
            cluster_id=cluster_id,
        )

        return typing.cast(None, jsii.invoke(self, "putConfluentCloud", [value]))

    @jsii.member(jsii_name="putPlatformLogsSettings")
    def put_platform_logs_settings(
        self,
        *,
        severity: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param severity: The minimum severity level of Platform Logs that will be written. If unspecified, no Platform Logs will be written. Default value: "SEVERITY_UNSPECIFIED" Possible values: ["SEVERITY_UNSPECIFIED", "DISABLED", "DEBUG", "INFO", "WARNING", "ERROR"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#severity GooglePubsubTopic#severity}
        '''
        value = GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettings(
            severity=severity
        )

        return typing.cast(None, jsii.invoke(self, "putPlatformLogsSettings", [value]))

    @jsii.member(jsii_name="resetAwsKinesis")
    def reset_aws_kinesis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsKinesis", []))

    @jsii.member(jsii_name="resetAwsMsk")
    def reset_aws_msk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsMsk", []))

    @jsii.member(jsii_name="resetAzureEventHubs")
    def reset_azure_event_hubs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureEventHubs", []))

    @jsii.member(jsii_name="resetCloudStorage")
    def reset_cloud_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudStorage", []))

    @jsii.member(jsii_name="resetConfluentCloud")
    def reset_confluent_cloud(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfluentCloud", []))

    @jsii.member(jsii_name="resetPlatformLogsSettings")
    def reset_platform_logs_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatformLogsSettings", []))

    @builtins.property
    @jsii.member(jsii_name="awsKinesis")
    def aws_kinesis(
        self,
    ) -> GooglePubsubTopicIngestionDataSourceSettingsAwsKinesisOutputReference:
        return typing.cast(GooglePubsubTopicIngestionDataSourceSettingsAwsKinesisOutputReference, jsii.get(self, "awsKinesis"))

    @builtins.property
    @jsii.member(jsii_name="awsMsk")
    def aws_msk(
        self,
    ) -> GooglePubsubTopicIngestionDataSourceSettingsAwsMskOutputReference:
        return typing.cast(GooglePubsubTopicIngestionDataSourceSettingsAwsMskOutputReference, jsii.get(self, "awsMsk"))

    @builtins.property
    @jsii.member(jsii_name="azureEventHubs")
    def azure_event_hubs(
        self,
    ) -> GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubsOutputReference:
        return typing.cast(GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubsOutputReference, jsii.get(self, "azureEventHubs"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorage")
    def cloud_storage(
        self,
    ) -> GooglePubsubTopicIngestionDataSourceSettingsCloudStorageOutputReference:
        return typing.cast(GooglePubsubTopicIngestionDataSourceSettingsCloudStorageOutputReference, jsii.get(self, "cloudStorage"))

    @builtins.property
    @jsii.member(jsii_name="confluentCloud")
    def confluent_cloud(
        self,
    ) -> GooglePubsubTopicIngestionDataSourceSettingsConfluentCloudOutputReference:
        return typing.cast(GooglePubsubTopicIngestionDataSourceSettingsConfluentCloudOutputReference, jsii.get(self, "confluentCloud"))

    @builtins.property
    @jsii.member(jsii_name="platformLogsSettings")
    def platform_logs_settings(
        self,
    ) -> "GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettingsOutputReference":
        return typing.cast("GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettingsOutputReference", jsii.get(self, "platformLogsSettings"))

    @builtins.property
    @jsii.member(jsii_name="awsKinesisInput")
    def aws_kinesis_input(
        self,
    ) -> typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsAwsKinesis]:
        return typing.cast(typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsAwsKinesis], jsii.get(self, "awsKinesisInput"))

    @builtins.property
    @jsii.member(jsii_name="awsMskInput")
    def aws_msk_input(
        self,
    ) -> typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsAwsMsk]:
        return typing.cast(typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsAwsMsk], jsii.get(self, "awsMskInput"))

    @builtins.property
    @jsii.member(jsii_name="azureEventHubsInput")
    def azure_event_hubs_input(
        self,
    ) -> typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubs]:
        return typing.cast(typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubs], jsii.get(self, "azureEventHubsInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageInput")
    def cloud_storage_input(
        self,
    ) -> typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsCloudStorage]:
        return typing.cast(typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsCloudStorage], jsii.get(self, "cloudStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="confluentCloudInput")
    def confluent_cloud_input(
        self,
    ) -> typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsConfluentCloud]:
        return typing.cast(typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsConfluentCloud], jsii.get(self, "confluentCloudInput"))

    @builtins.property
    @jsii.member(jsii_name="platformLogsSettingsInput")
    def platform_logs_settings_input(
        self,
    ) -> typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettings"]:
        return typing.cast(typing.Optional["GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettings"], jsii.get(self, "platformLogsSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePubsubTopicIngestionDataSourceSettings]:
        return typing.cast(typing.Optional[GooglePubsubTopicIngestionDataSourceSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubTopicIngestionDataSourceSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5185f799e89686733edcc5a13a58fcd8c1e3457f388564f47a6a5cab8619e5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettings",
    jsii_struct_bases=[],
    name_mapping={"severity": "severity"},
)
class GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettings:
    def __init__(self, *, severity: typing.Optional[builtins.str] = None) -> None:
        '''
        :param severity: The minimum severity level of Platform Logs that will be written. If unspecified, no Platform Logs will be written. Default value: "SEVERITY_UNSPECIFIED" Possible values: ["SEVERITY_UNSPECIFIED", "DISABLED", "DEBUG", "INFO", "WARNING", "ERROR"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#severity GooglePubsubTopic#severity}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dc31923e9912fdbcc80a5d7b1b0969dac6c411ae72b4810b09a420de4cbd0d3)
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if severity is not None:
            self._values["severity"] = severity

    @builtins.property
    def severity(self) -> typing.Optional[builtins.str]:
        '''The minimum severity level of Platform Logs that will be written.

        If unspecified,
        no Platform Logs will be written. Default value: "SEVERITY_UNSPECIFIED" Possible values: ["SEVERITY_UNSPECIFIED", "DISABLED", "DEBUG", "INFO", "WARNING", "ERROR"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#severity GooglePubsubTopic#severity}
        '''
        result = self._values.get("severity")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfa8fd602fa3277ee27c8ae7d0e8b692c1655222c1af6dc69e890f0a99b9be11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSeverity")
    def reset_severity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeverity", []))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__101a405561c369e5f2f42f70d792b396424862c64c07534742e55b74500072b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettings]:
        return typing.cast(typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73545c04688912a1b425d893e0ac5c48b83cd648f382e550a6503ea6aaf326d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicMessageStoragePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_persistence_regions": "allowedPersistenceRegions",
        "enforce_in_transit": "enforceInTransit",
    },
)
class GooglePubsubTopicMessageStoragePolicy:
    def __init__(
        self,
        *,
        allowed_persistence_regions: typing.Sequence[builtins.str],
        enforce_in_transit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_persistence_regions: A list of IDs of GCP regions where messages that are published to the topic may be persisted in storage. Messages published by publishers running in non-allowed GCP regions (or running outside of GCP altogether) will be routed for storage in one of the allowed regions. An empty list means that no regions are allowed, and is not a valid configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#allowed_persistence_regions GooglePubsubTopic#allowed_persistence_regions}
        :param enforce_in_transit: If true, 'allowedPersistenceRegions' is also used to enforce in-transit guarantees for messages. That is, Pub/Sub will fail topics.publish operations on this topic and subscribe operations on any subscription attached to this topic in any region that is not in 'allowedPersistenceRegions'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#enforce_in_transit GooglePubsubTopic#enforce_in_transit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e04cec55757b93d454c38d6c42e6371220a6c39a31d081ee3e041dd4b186f34)
            check_type(argname="argument allowed_persistence_regions", value=allowed_persistence_regions, expected_type=type_hints["allowed_persistence_regions"])
            check_type(argname="argument enforce_in_transit", value=enforce_in_transit, expected_type=type_hints["enforce_in_transit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_persistence_regions": allowed_persistence_regions,
        }
        if enforce_in_transit is not None:
            self._values["enforce_in_transit"] = enforce_in_transit

    @builtins.property
    def allowed_persistence_regions(self) -> typing.List[builtins.str]:
        '''A list of IDs of GCP regions where messages that are published to the topic may be persisted in storage.

        Messages published by
        publishers running in non-allowed GCP regions (or running outside
        of GCP altogether) will be routed for storage in one of the
        allowed regions. An empty list means that no regions are allowed,
        and is not a valid configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#allowed_persistence_regions GooglePubsubTopic#allowed_persistence_regions}
        '''
        result = self._values.get("allowed_persistence_regions")
        assert result is not None, "Required property 'allowed_persistence_regions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def enforce_in_transit(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, 'allowedPersistenceRegions' is also used to enforce in-transit guarantees for messages.

        That is, Pub/Sub will fail topics.publish
        operations on this topic and subscribe operations on any subscription
        attached to this topic in any region that is not in 'allowedPersistenceRegions'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#enforce_in_transit GooglePubsubTopic#enforce_in_transit}
        '''
        result = self._values.get("enforce_in_transit")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubTopicMessageStoragePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubTopicMessageStoragePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicMessageStoragePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e5712f85b215148ca1a9f8a8060abc52d85b157e9216277127a57ad05183816)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnforceInTransit")
    def reset_enforce_in_transit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceInTransit", []))

    @builtins.property
    @jsii.member(jsii_name="allowedPersistenceRegionsInput")
    def allowed_persistence_regions_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedPersistenceRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceInTransitInput")
    def enforce_in_transit_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforceInTransitInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedPersistenceRegions")
    def allowed_persistence_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedPersistenceRegions"))

    @allowed_persistence_regions.setter
    def allowed_persistence_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__592fd1d39b26c4d863ff6b1108b234251dad43bd14e1fc4126b12a03caf72800)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedPersistenceRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceInTransit")
    def enforce_in_transit(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enforceInTransit"))

    @enforce_in_transit.setter
    def enforce_in_transit(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44866beb85d5ad78e7db9250b746b322b9ccad7133174d515e9364a7014ef348)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceInTransit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GooglePubsubTopicMessageStoragePolicy]:
        return typing.cast(typing.Optional[GooglePubsubTopicMessageStoragePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubTopicMessageStoragePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a68ffe3da161d6cef6625581e386bfee04de474235911fd768a2e1a98045d17e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicMessageTransforms",
    jsii_struct_bases=[],
    name_mapping={"disabled": "disabled", "javascript_udf": "javascriptUdf"},
)
class GooglePubsubTopicMessageTransforms:
    def __init__(
        self,
        *,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        javascript_udf: typing.Optional[typing.Union["GooglePubsubTopicMessageTransformsJavascriptUdf", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param disabled: Controls whether or not to use this transform. If not set or 'false', the transform will be applied to messages. Default: 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#disabled GooglePubsubTopic#disabled}
        :param javascript_udf: javascript_udf block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#javascript_udf GooglePubsubTopic#javascript_udf}
        '''
        if isinstance(javascript_udf, dict):
            javascript_udf = GooglePubsubTopicMessageTransformsJavascriptUdf(**javascript_udf)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56d8a72c66995c88384bb2c03429d1a6012da450a1d39c95d447153dcba0e47d)
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument javascript_udf", value=javascript_udf, expected_type=type_hints["javascript_udf"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disabled is not None:
            self._values["disabled"] = disabled
        if javascript_udf is not None:
            self._values["javascript_udf"] = javascript_udf

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Controls whether or not to use this transform.

        If not set or 'false',
        the transform will be applied to messages. Default: 'true'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#disabled GooglePubsubTopic#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def javascript_udf(
        self,
    ) -> typing.Optional["GooglePubsubTopicMessageTransformsJavascriptUdf"]:
        '''javascript_udf block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#javascript_udf GooglePubsubTopic#javascript_udf}
        '''
        result = self._values.get("javascript_udf")
        return typing.cast(typing.Optional["GooglePubsubTopicMessageTransformsJavascriptUdf"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubTopicMessageTransforms(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicMessageTransformsJavascriptUdf",
    jsii_struct_bases=[],
    name_mapping={"code": "code", "function_name": "functionName"},
)
class GooglePubsubTopicMessageTransformsJavascriptUdf:
    def __init__(self, *, code: builtins.str, function_name: builtins.str) -> None:
        '''
        :param code: JavaScript code that contains a function 'function_name' with the following signature: ``` /** * Transforms a Pub/Sub message. - -
        :param function_name: Name of the JavaScript function that should be applied to Pub/Sub messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#function_name GooglePubsubTopic#function_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f87966a58ed29c2e816a1d193b2f7d3c9c7fcfcac9b5fe0ca39386b4fd6710e)
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "code": code,
            "function_name": function_name,
        }

    @builtins.property
    def code(self) -> builtins.str:
        '''JavaScript code that contains a function 'function_name' with the following signature: ```   /**   * Transforms a Pub/Sub message.

        -
          -

        :return:

        - To

        - filter a message, return 'null'. To transform a message return a map
        - with the following keys:
        -
        - (required) 'data' : {string}

        -
        - (optional) 'attributes' : {Object<string, string>}

        - Returning empty 'attributes' will remove all attributes from the
        - message.
        - -
        '''
        result = self._values.get("code")
        assert result is not None, "Required property 'code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def function_name(self) -> builtins.str:
        '''Name of the JavaScript function that should be applied to Pub/Sub messages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#function_name GooglePubsubTopic#function_name}
        '''
        result = self._values.get("function_name")
        assert result is not None, "Required property 'function_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubTopicMessageTransformsJavascriptUdf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubTopicMessageTransformsJavascriptUdfOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicMessageTransformsJavascriptUdfOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8566ba3abe6094190b9303ee03456e3fff779d6938ea9379f892008455b86b2c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="codeInput")
    def code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codeInput"))

    @builtins.property
    @jsii.member(jsii_name="functionNameInput")
    def function_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "code"))

    @code.setter
    def code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed9d7225d4ec90526785491dd6d637e60e51cda76f7c11be4037566cd75c5953)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "code", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionName"))

    @function_name.setter
    def function_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__044a6ec96c184cbade153b11e36ef35153082b57bcdccb607eeea2ae7bafe4dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePubsubTopicMessageTransformsJavascriptUdf]:
        return typing.cast(typing.Optional[GooglePubsubTopicMessageTransformsJavascriptUdf], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubTopicMessageTransformsJavascriptUdf],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__702d77d3ebc273fffd775ee5d5542e58a667effad570635f6dd3c7e807b12b8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePubsubTopicMessageTransformsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicMessageTransformsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b21d0c7f9eedb64996eeb2774623a478488093e998a07a4e3bdd576b11e16e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GooglePubsubTopicMessageTransformsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7d4c09f7954a0d4f66c2a1284366215036b3213e6162e293cfd4b529aa73840)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GooglePubsubTopicMessageTransformsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b20ede1e8fc4b4f16d22e20e50e0af84025b85c4579b1684f3b2943a2bf52e44)
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
            type_hints = typing.get_type_hints(_typecheckingstub__745285299b334d9c9329d009802baabf2fdf1a049b33e5d605d50c286b193d7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b26c9bf3800d56fb1ca1a6eed7e97d719d3774f69162b45a27f72e2271e2145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePubsubTopicMessageTransforms]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePubsubTopicMessageTransforms]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePubsubTopicMessageTransforms]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__025bd5e3b4af91e748a283f7fc68828be4cd8428cd163db7a2048eb3e6b1925e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePubsubTopicMessageTransformsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicMessageTransformsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41a14ffecb0d618bfde430d3be4df75f6a53211370cacc9025978075adcb78f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putJavascriptUdf")
    def put_javascript_udf(
        self,
        *,
        code: builtins.str,
        function_name: builtins.str,
    ) -> None:
        '''
        :param code: JavaScript code that contains a function 'function_name' with the following signature: ``` /** * Transforms a Pub/Sub message. - -
        :param function_name: Name of the JavaScript function that should be applied to Pub/Sub messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#function_name GooglePubsubTopic#function_name}
        '''
        value = GooglePubsubTopicMessageTransformsJavascriptUdf(
            code=code, function_name=function_name
        )

        return typing.cast(None, jsii.invoke(self, "putJavascriptUdf", [value]))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetJavascriptUdf")
    def reset_javascript_udf(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJavascriptUdf", []))

    @builtins.property
    @jsii.member(jsii_name="javascriptUdf")
    def javascript_udf(
        self,
    ) -> GooglePubsubTopicMessageTransformsJavascriptUdfOutputReference:
        return typing.cast(GooglePubsubTopicMessageTransformsJavascriptUdfOutputReference, jsii.get(self, "javascriptUdf"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="javascriptUdfInput")
    def javascript_udf_input(
        self,
    ) -> typing.Optional[GooglePubsubTopicMessageTransformsJavascriptUdf]:
        return typing.cast(typing.Optional[GooglePubsubTopicMessageTransformsJavascriptUdf], jsii.get(self, "javascriptUdfInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1aba32b68eb6de60318a209577834a9bebf1f7b84cd15c74f00b3e9f699e0a43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePubsubTopicMessageTransforms]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePubsubTopicMessageTransforms]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePubsubTopicMessageTransforms]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80a8af8a07f6dda53d1111ddc98b4969cb67fce930cd1d45f8372f60f1b4a01c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicSchemaSettings",
    jsii_struct_bases=[],
    name_mapping={"schema": "schema", "encoding": "encoding"},
)
class GooglePubsubTopicSchemaSettings:
    def __init__(
        self,
        *,
        schema: builtins.str,
        encoding: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema: The name of the schema that messages published should be validated against. Format is projects/{project}/schemas/{schema}. The value of this field will be *deleted-schema* if the schema has been deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#schema GooglePubsubTopic#schema}
        :param encoding: The encoding of messages validated against schema. Default value: "ENCODING_UNSPECIFIED" Possible values: ["ENCODING_UNSPECIFIED", "JSON", "BINARY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#encoding GooglePubsubTopic#encoding}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa530a827bec62e3c1cdd8f527c4ef9a257a3d01b0f41c2a4a6d9b2f8f9f77cc)
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schema": schema,
        }
        if encoding is not None:
            self._values["encoding"] = encoding

    @builtins.property
    def schema(self) -> builtins.str:
        '''The name of the schema that messages published should be validated against.

        Format is projects/{project}/schemas/{schema}.
        The value of this field will be *deleted-schema*
        if the schema has been deleted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#schema GooglePubsubTopic#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encoding(self) -> typing.Optional[builtins.str]:
        '''The encoding of messages validated against schema. Default value: "ENCODING_UNSPECIFIED" Possible values: ["ENCODING_UNSPECIFIED", "JSON", "BINARY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#encoding GooglePubsubTopic#encoding}
        '''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubTopicSchemaSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubTopicSchemaSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicSchemaSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b07dd0ccb677436152157e147b8ae356e6b32863d37c7b070e1581dd45d6d4a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEncoding")
    def reset_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncoding", []))

    @builtins.property
    @jsii.member(jsii_name="encodingInput")
    def encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encodingInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="encoding")
    def encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encoding"))

    @encoding.setter
    def encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82605c8fa48c936881487f60ad3c98e1f28f13d32c9372932bb42742321ee13f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42e1ce123e1f7681fd3fbe1ac8632f9c7962bdcc6c89b8b76b503572c867a6b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GooglePubsubTopicSchemaSettings]:
        return typing.cast(typing.Optional[GooglePubsubTopicSchemaSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubTopicSchemaSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5054ace255f4f9435d4d723b2e5221675e021c6ba2994df4371faab0af18740)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GooglePubsubTopicTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#create GooglePubsubTopic#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#delete GooglePubsubTopic#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#update GooglePubsubTopic#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cbb744b8e97054687bba13da20ddf4132439bde5e73412e11e97e2b180b2b9a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#create GooglePubsubTopic#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#delete GooglePubsubTopic#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_topic#update GooglePubsubTopic#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubTopicTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubTopicTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubTopic.GooglePubsubTopicTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29d6cecf31b6cdac3359074bcbabc993e31294039774c3555e2a204051244ebf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f58d595c14986e5f9d4f3e11804629d3a7cf378e5d640278608e2167bb15e153)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c986a4c6a71b1fb38c516d84f24e8fbed0912a170095c391636fb79a28bac4ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__656f83f16d8309345afb46501eae796e49a7362c7e33458d055a22c4d500493f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePubsubTopicTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePubsubTopicTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePubsubTopicTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__302403af4c44996c84fcd3b6ac4de0bc3aab0a3ffc5ed126c20437fc67503e7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GooglePubsubTopic",
    "GooglePubsubTopicConfig",
    "GooglePubsubTopicIngestionDataSourceSettings",
    "GooglePubsubTopicIngestionDataSourceSettingsAwsKinesis",
    "GooglePubsubTopicIngestionDataSourceSettingsAwsKinesisOutputReference",
    "GooglePubsubTopicIngestionDataSourceSettingsAwsMsk",
    "GooglePubsubTopicIngestionDataSourceSettingsAwsMskOutputReference",
    "GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubs",
    "GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubsOutputReference",
    "GooglePubsubTopicIngestionDataSourceSettingsCloudStorage",
    "GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat",
    "GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormatOutputReference",
    "GooglePubsubTopicIngestionDataSourceSettingsCloudStorageOutputReference",
    "GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat",
    "GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormatOutputReference",
    "GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat",
    "GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormatOutputReference",
    "GooglePubsubTopicIngestionDataSourceSettingsConfluentCloud",
    "GooglePubsubTopicIngestionDataSourceSettingsConfluentCloudOutputReference",
    "GooglePubsubTopicIngestionDataSourceSettingsOutputReference",
    "GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettings",
    "GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettingsOutputReference",
    "GooglePubsubTopicMessageStoragePolicy",
    "GooglePubsubTopicMessageStoragePolicyOutputReference",
    "GooglePubsubTopicMessageTransforms",
    "GooglePubsubTopicMessageTransformsJavascriptUdf",
    "GooglePubsubTopicMessageTransformsJavascriptUdfOutputReference",
    "GooglePubsubTopicMessageTransformsList",
    "GooglePubsubTopicMessageTransformsOutputReference",
    "GooglePubsubTopicSchemaSettings",
    "GooglePubsubTopicSchemaSettingsOutputReference",
    "GooglePubsubTopicTimeouts",
    "GooglePubsubTopicTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__632d9ee170a770a95ec0d40830ef047caca59b182c12a2804baeb1e03a825389(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    ingestion_data_source_settings: typing.Optional[typing.Union[GooglePubsubTopicIngestionDataSourceSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    message_retention_duration: typing.Optional[builtins.str] = None,
    message_storage_policy: typing.Optional[typing.Union[GooglePubsubTopicMessageStoragePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    message_transforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePubsubTopicMessageTransforms, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    schema_settings: typing.Optional[typing.Union[GooglePubsubTopicSchemaSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GooglePubsubTopicTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__48564ab17ae5cde24b80b7be627a8b421d35aa1d9fb5edf5e5a349cb03c8cf63(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9a1878163a3d126a8be1541984dfc6a2d1d30c3f1636db6c634a77bb581631(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePubsubTopicMessageTransforms, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d80012e89fc62d7d405ff750079d41322d0e2f3d879f750547153c5b01b0bb5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f364d62e24d8df2263af02f92eb72f80150e71a13f22d66f1f0b507723577bc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a17fa6c3ade6a4207a5bbcf69033652775e60e3e4c3331acfc642150c8b1de(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab083465b27c9decd183a2dd1c239016643a800e57075dfed112a684ec509cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fff2e780c9e44b984d0834eaafe66f4c7926284800bf5d3c045fcc759e6aae4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__705f087c4de2a81428c1e1b494bf78d8a59e07b37dfe553dcb7c73a80ede686f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__720d9d480f91293b76fa6b5ee681be374fbeae1e414a139d606c26036fde0f9b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    ingestion_data_source_settings: typing.Optional[typing.Union[GooglePubsubTopicIngestionDataSourceSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    message_retention_duration: typing.Optional[builtins.str] = None,
    message_storage_policy: typing.Optional[typing.Union[GooglePubsubTopicMessageStoragePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    message_transforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePubsubTopicMessageTransforms, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    schema_settings: typing.Optional[typing.Union[GooglePubsubTopicSchemaSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GooglePubsubTopicTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c3a094576b11483ba4ab0751f3db901cb929a1fe7d4f96cd2f3e2c5a9f83ca(
    *,
    aws_kinesis: typing.Optional[typing.Union[GooglePubsubTopicIngestionDataSourceSettingsAwsKinesis, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_msk: typing.Optional[typing.Union[GooglePubsubTopicIngestionDataSourceSettingsAwsMsk, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_event_hubs: typing.Optional[typing.Union[GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubs, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_storage: typing.Optional[typing.Union[GooglePubsubTopicIngestionDataSourceSettingsCloudStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    confluent_cloud: typing.Optional[typing.Union[GooglePubsubTopicIngestionDataSourceSettingsConfluentCloud, typing.Dict[builtins.str, typing.Any]]] = None,
    platform_logs_settings: typing.Optional[typing.Union[GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5f4d5cca52d9ab0c04e5d7bd7db673db00f07749711f720b2596e1c270dfbe2(
    *,
    aws_role_arn: builtins.str,
    consumer_arn: builtins.str,
    gcp_service_account: builtins.str,
    stream_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac1b676ae7841393afe443c5a41029604a1b20fa3c6d16e617a1ee9d07e6b1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69209bb1c2e8aead3101f8f5d8d76dbefd8849ec555c2b4cd1d931a52c3e1330(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eaa8ff34b0446efe283f109f135ddbad3076fed32a4508ce2b50056e0b7af49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd86bec2312898f7009436a5b0635c89595c3dd49ea49f235e08a450bd3b152(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43e3ccc619827f095bed6f0789fde278b8647d50309c59865b2d7006fbb262a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2183cf0be596ce715498ca862647dffcdf82bf3ac8577f259117f8ae71099667(
    value: typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsAwsKinesis],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edbd2270d2eb46f845bf56baca0ec93791dbc5a5ffa8367294bd1c1d0caecf66(
    *,
    aws_role_arn: builtins.str,
    cluster_arn: builtins.str,
    gcp_service_account: builtins.str,
    topic: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c3b6e24cd4829b566a612ad474eb4894b71e56030f471d50b1b4e56fecd893d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__623a2d5f9fc1eaa57ff5df188f8c94f72802c0671235f2034c543e2d1f937168(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e8423a6446833f5fea91204bc71ed541c367c4378b06d6cbb412692b6496ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c1438278e728cf930ced0ad728624f5339da16350cecb83b70121594aea4c12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f3ed3a5e9845da1d472475493d3f72ffb3972e131a6eb16196434c9095d2b34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__033a2cef3c9adcc1f8a3bc78bd88054700a9a015b18be50d03b81f00d27e6c56(
    value: typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsAwsMsk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e11216acbae1d118c39566571d32acfde2b56c52841b9e2adafe7b2ef6460b94(
    *,
    client_id: typing.Optional[builtins.str] = None,
    event_hub: typing.Optional[builtins.str] = None,
    gcp_service_account: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    resource_group: typing.Optional[builtins.str] = None,
    subscription_id: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a488d3998c131fd16fa283cc686781fd7b9cfeec58b8e200f2767940c76fd58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cac61e19f694f92981808198739fb9a8e10a65fd174bf589209d315522da23ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9557dad704df20b4b329e35be5c6705b9a27f38fda44ea6bdeb8b3edc7ecf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d6d6676519f1bddd20a5def6a1d5e802937bb2a77902027c2266aa32aa9826(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__131c4bd3cf48af23a72048c99e5e4c1f23cefcad5b1ed3f2695ea53008c90b5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df0f79307e5ed17762ef5c55555962b562fe7b053b87561f4c4e7ab7f5712be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68148d043c966dc6ed158125a8622c57e1639e8b01f13d0e1bfbbcdd785f7597(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d93fc555bbfbc205254daf74cc8cb7532cc35d1e7b769a776f04168b0d53c0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17da9ae63be4b72ff556d75a8b7210b26f65b21e2d832108a8edc9d04065598a(
    value: typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsAzureEventHubs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__807900dd63741444c9a0f0c46cb3a0ce212981d1d4d80e1e0b41e67c833d5ec6(
    *,
    bucket: builtins.str,
    avro_format: typing.Optional[typing.Union[GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat, typing.Dict[builtins.str, typing.Any]]] = None,
    match_glob: typing.Optional[builtins.str] = None,
    minimum_object_create_time: typing.Optional[builtins.str] = None,
    pubsub_avro_format: typing.Optional[typing.Union[GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat, typing.Dict[builtins.str, typing.Any]]] = None,
    text_format: typing.Optional[typing.Union[GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e21aa324562185a133696b3df13020c89ddbf1d9037a2d109f225c8e0a139e2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e8b29eb1c8c0451b7f57700541831311a5f0dd342a5d3b814fdac2f62ac0b6(
    value: typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f5c1fe7dec3dcfc6a62b9f8982bc30e70de2d5bf9bd743dbe49de0fbb6d1e34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6809a2118460757fb076fbb895be7de9f3a1bba6478cd534b100d44886a1971e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b304073a305984ebf91f6c2ea08672de71cecb6080a9b0e4ca45e5c6131e76c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d9ee4c20ce87d3f5d9c80e318f362b349a2f22330a941b7ee00120329dcda6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33891a99ed51f05fa56e5b19b1dbaa9e9361a57aeac68791e034419b01ea2cd(
    value: typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsCloudStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39dd7ecccb719b2efe989c432d961500e3936fe4914479b9747ae4a942e1d3a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee885ef75e41bebfbfa1884c47407d312f5fecb9d4ea9cd2b783abc8e7251580(
    value: typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ab88efc2d68ce20733d84e69a37638b0f8e80475b3f6a55dbce706ac1947ab(
    *,
    delimiter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e3ea52e7bc374e2cabdf385b6ced8a9f4c1553013a8acb0962eb7cb8884365(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6410e699e88fffcb58d36836f856eda698148e432ab5459aed91babbdbd79e78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1200dc7eb613a24ab7032f734791f451ccf524590a841ce92678960a5117aaa(
    value: typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec81b754bd9c0c299c961b8e9c2823ee7963fb4da073442e6139571739218d6(
    *,
    bootstrap_server: builtins.str,
    gcp_service_account: builtins.str,
    identity_pool_id: builtins.str,
    topic: builtins.str,
    cluster_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c4270ed2e8b408d3a366da4208067f6f066dc206d38dc862c8fb3cfa44b6294(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2717a45a8ee2d077807a63ee02720aa2457720d94680cba027d289a20db8a51e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a903d1f1de551970329999e891b8214a6315d2721282d014898de2be732ea9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a35d54b511917bed9e2f95c71e1ff16c8c4883eecc298d2a22909b00eb6cc5ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__314f278ed19f7359625f089742080a51dadec3b0418662319e41020a38e1c615(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd867c9063082259c6095912c4267170914a42d569a2e887b99c3404a30691f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0fefd9917b9b4dc47c2c70bb4fef710eb02ab76018410fb5649b7b790f1e594(
    value: typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsConfluentCloud],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8962a5458e42c165bbad5fb45a5c9cd479a9adaf50c44b625f046fbcb2d8c1c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5185f799e89686733edcc5a13a58fcd8c1e3457f388564f47a6a5cab8619e5d(
    value: typing.Optional[GooglePubsubTopicIngestionDataSourceSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc31923e9912fdbcc80a5d7b1b0969dac6c411ae72b4810b09a420de4cbd0d3(
    *,
    severity: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa8fd602fa3277ee27c8ae7d0e8b692c1655222c1af6dc69e890f0a99b9be11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101a405561c369e5f2f42f70d792b396424862c64c07534742e55b74500072b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73545c04688912a1b425d893e0ac5c48b83cd648f382e550a6503ea6aaf326d2(
    value: typing.Optional[GooglePubsubTopicIngestionDataSourceSettingsPlatformLogsSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e04cec55757b93d454c38d6c42e6371220a6c39a31d081ee3e041dd4b186f34(
    *,
    allowed_persistence_regions: typing.Sequence[builtins.str],
    enforce_in_transit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e5712f85b215148ca1a9f8a8060abc52d85b157e9216277127a57ad05183816(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__592fd1d39b26c4d863ff6b1108b234251dad43bd14e1fc4126b12a03caf72800(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44866beb85d5ad78e7db9250b746b322b9ccad7133174d515e9364a7014ef348(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a68ffe3da161d6cef6625581e386bfee04de474235911fd768a2e1a98045d17e(
    value: typing.Optional[GooglePubsubTopicMessageStoragePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56d8a72c66995c88384bb2c03429d1a6012da450a1d39c95d447153dcba0e47d(
    *,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    javascript_udf: typing.Optional[typing.Union[GooglePubsubTopicMessageTransformsJavascriptUdf, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f87966a58ed29c2e816a1d193b2f7d3c9c7fcfcac9b5fe0ca39386b4fd6710e(
    *,
    code: builtins.str,
    function_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8566ba3abe6094190b9303ee03456e3fff779d6938ea9379f892008455b86b2c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed9d7225d4ec90526785491dd6d637e60e51cda76f7c11be4037566cd75c5953(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__044a6ec96c184cbade153b11e36ef35153082b57bcdccb607eeea2ae7bafe4dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__702d77d3ebc273fffd775ee5d5542e58a667effad570635f6dd3c7e807b12b8d(
    value: typing.Optional[GooglePubsubTopicMessageTransformsJavascriptUdf],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b21d0c7f9eedb64996eeb2774623a478488093e998a07a4e3bdd576b11e16e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d4c09f7954a0d4f66c2a1284366215036b3213e6162e293cfd4b529aa73840(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b20ede1e8fc4b4f16d22e20e50e0af84025b85c4579b1684f3b2943a2bf52e44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__745285299b334d9c9329d009802baabf2fdf1a049b33e5d605d50c286b193d7a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b26c9bf3800d56fb1ca1a6eed7e97d719d3774f69162b45a27f72e2271e2145(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025bd5e3b4af91e748a283f7fc68828be4cd8428cd163db7a2048eb3e6b1925e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePubsubTopicMessageTransforms]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a14ffecb0d618bfde430d3be4df75f6a53211370cacc9025978075adcb78f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aba32b68eb6de60318a209577834a9bebf1f7b84cd15c74f00b3e9f699e0a43(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a8af8a07f6dda53d1111ddc98b4969cb67fce930cd1d45f8372f60f1b4a01c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePubsubTopicMessageTransforms]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa530a827bec62e3c1cdd8f527c4ef9a257a3d01b0f41c2a4a6d9b2f8f9f77cc(
    *,
    schema: builtins.str,
    encoding: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b07dd0ccb677436152157e147b8ae356e6b32863d37c7b070e1581dd45d6d4a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82605c8fa48c936881487f60ad3c98e1f28f13d32c9372932bb42742321ee13f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e1ce123e1f7681fd3fbe1ac8632f9c7962bdcc6c89b8b76b503572c867a6b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5054ace255f4f9435d4d723b2e5221675e021c6ba2994df4371faab0af18740(
    value: typing.Optional[GooglePubsubTopicSchemaSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cbb744b8e97054687bba13da20ddf4132439bde5e73412e11e97e2b180b2b9a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29d6cecf31b6cdac3359074bcbabc993e31294039774c3555e2a204051244ebf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f58d595c14986e5f9d4f3e11804629d3a7cf378e5d640278608e2167bb15e153(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c986a4c6a71b1fb38c516d84f24e8fbed0912a170095c391636fb79a28bac4ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__656f83f16d8309345afb46501eae796e49a7362c7e33458d055a22c4d500493f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__302403af4c44996c84fcd3b6ac4de0bc3aab0a3ffc5ed126c20437fc67503e7d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePubsubTopicTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
