r'''
# `google_pubsub_topic`

Refer to the Terraform Registry for docs: [`google_pubsub_topic`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic).
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


class PubsubTopic(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopic",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic google_pubsub_topic}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        ingestion_data_source_settings: typing.Optional[typing.Union["PubsubTopicIngestionDataSourceSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        message_retention_duration: typing.Optional[builtins.str] = None,
        message_storage_policy: typing.Optional[typing.Union["PubsubTopicMessageStoragePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        message_transforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PubsubTopicMessageTransforms", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        schema_settings: typing.Optional[typing.Union["PubsubTopicSchemaSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["PubsubTopicTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic google_pubsub_topic} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#name PubsubTopic#name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#id PubsubTopic#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ingestion_data_source_settings: ingestion_data_source_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#ingestion_data_source_settings PubsubTopic#ingestion_data_source_settings}
        :param kms_key_name: The resource name of the Cloud KMS CryptoKey to be used to protect access to messages published on this topic. Your project's PubSub service account ('service-{{PROJECT_NUMBER}}@gcp-sa-pubsub.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. The expected format is 'projects/* /locations/* /keyRings/* /cryptoKeys/*' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#kms_key_name PubsubTopic#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param labels: A set of key/value label pairs to assign to this Topic. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#labels PubsubTopic#labels}
        :param message_retention_duration: Indicates the minimum duration to retain a message after it is published to the topic. If this field is set, messages published to the topic in the last messageRetentionDuration are always available to subscribers. For instance, it allows any attached subscription to seek to a timestamp that is up to messageRetentionDuration in the past. If this field is not set, message retention is controlled by settings on individual subscriptions. The rotation period has the format of a decimal number, followed by the letter 's' (seconds). Cannot be more than 31 days or less than 10 minutes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#message_retention_duration PubsubTopic#message_retention_duration}
        :param message_storage_policy: message_storage_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#message_storage_policy PubsubTopic#message_storage_policy}
        :param message_transforms: message_transforms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#message_transforms PubsubTopic#message_transforms}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#project PubsubTopic#project}.
        :param schema_settings: schema_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#schema_settings PubsubTopic#schema_settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#timeouts PubsubTopic#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25a4b255d477dbb29368b5c62db08af517f7c9e151c7e77fc3a8e34accf0c08e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PubsubTopicConfig(
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
        '''Generates CDKTF code for importing a PubsubTopic resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PubsubTopic to import.
        :param import_from_id: The id of the existing PubsubTopic that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PubsubTopic to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09054ad2222523bdb5dececfb3440b992705e3a3e3b98cd7c7320b0859416cc3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIngestionDataSourceSettings")
    def put_ingestion_data_source_settings(
        self,
        *,
        aws_kinesis: typing.Optional[typing.Union["PubsubTopicIngestionDataSourceSettingsAwsKinesis", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_msk: typing.Optional[typing.Union["PubsubTopicIngestionDataSourceSettingsAwsMsk", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_event_hubs: typing.Optional[typing.Union["PubsubTopicIngestionDataSourceSettingsAzureEventHubs", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_storage: typing.Optional[typing.Union["PubsubTopicIngestionDataSourceSettingsCloudStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        confluent_cloud: typing.Optional[typing.Union["PubsubTopicIngestionDataSourceSettingsConfluentCloud", typing.Dict[builtins.str, typing.Any]]] = None,
        platform_logs_settings: typing.Optional[typing.Union["PubsubTopicIngestionDataSourceSettingsPlatformLogsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws_kinesis: aws_kinesis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#aws_kinesis PubsubTopic#aws_kinesis}
        :param aws_msk: aws_msk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#aws_msk PubsubTopic#aws_msk}
        :param azure_event_hubs: azure_event_hubs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#azure_event_hubs PubsubTopic#azure_event_hubs}
        :param cloud_storage: cloud_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#cloud_storage PubsubTopic#cloud_storage}
        :param confluent_cloud: confluent_cloud block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#confluent_cloud PubsubTopic#confluent_cloud}
        :param platform_logs_settings: platform_logs_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#platform_logs_settings PubsubTopic#platform_logs_settings}
        '''
        value = PubsubTopicIngestionDataSourceSettings(
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
        :param allowed_persistence_regions: A list of IDs of GCP regions where messages that are published to the topic may be persisted in storage. Messages published by publishers running in non-allowed GCP regions (or running outside of GCP altogether) will be routed for storage in one of the allowed regions. An empty list means that no regions are allowed, and is not a valid configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#allowed_persistence_regions PubsubTopic#allowed_persistence_regions}
        :param enforce_in_transit: If true, 'allowedPersistenceRegions' is also used to enforce in-transit guarantees for messages. That is, Pub/Sub will fail topics.publish operations on this topic and subscribe operations on any subscription attached to this topic in any region that is not in 'allowedPersistenceRegions'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#enforce_in_transit PubsubTopic#enforce_in_transit}
        '''
        value = PubsubTopicMessageStoragePolicy(
            allowed_persistence_regions=allowed_persistence_regions,
            enforce_in_transit=enforce_in_transit,
        )

        return typing.cast(None, jsii.invoke(self, "putMessageStoragePolicy", [value]))

    @jsii.member(jsii_name="putMessageTransforms")
    def put_message_transforms(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PubsubTopicMessageTransforms", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__009c6fd9469867de50acfe181dab89c198666c8beed63e0afeac165d426cc579)
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
        :param schema: The name of the schema that messages published should be validated against. Format is projects/{project}/schemas/{schema}. The value of this field will be *deleted-schema* if the schema has been deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#schema PubsubTopic#schema}
        :param encoding: The encoding of messages validated against schema. Default value: "ENCODING_UNSPECIFIED" Possible values: ["ENCODING_UNSPECIFIED", "JSON", "BINARY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#encoding PubsubTopic#encoding}
        '''
        value = PubsubTopicSchemaSettings(schema=schema, encoding=encoding)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#create PubsubTopic#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#delete PubsubTopic#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#update PubsubTopic#update}.
        '''
        value = PubsubTopicTimeouts(create=create, delete=delete, update=update)

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
    ) -> "PubsubTopicIngestionDataSourceSettingsOutputReference":
        return typing.cast("PubsubTopicIngestionDataSourceSettingsOutputReference", jsii.get(self, "ingestionDataSourceSettings"))

    @builtins.property
    @jsii.member(jsii_name="messageStoragePolicy")
    def message_storage_policy(
        self,
    ) -> "PubsubTopicMessageStoragePolicyOutputReference":
        return typing.cast("PubsubTopicMessageStoragePolicyOutputReference", jsii.get(self, "messageStoragePolicy"))

    @builtins.property
    @jsii.member(jsii_name="messageTransforms")
    def message_transforms(self) -> "PubsubTopicMessageTransformsList":
        return typing.cast("PubsubTopicMessageTransformsList", jsii.get(self, "messageTransforms"))

    @builtins.property
    @jsii.member(jsii_name="schemaSettings")
    def schema_settings(self) -> "PubsubTopicSchemaSettingsOutputReference":
        return typing.cast("PubsubTopicSchemaSettingsOutputReference", jsii.get(self, "schemaSettings"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "PubsubTopicTimeoutsOutputReference":
        return typing.cast("PubsubTopicTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ingestionDataSourceSettingsInput")
    def ingestion_data_source_settings_input(
        self,
    ) -> typing.Optional["PubsubTopicIngestionDataSourceSettings"]:
        return typing.cast(typing.Optional["PubsubTopicIngestionDataSourceSettings"], jsii.get(self, "ingestionDataSourceSettingsInput"))

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
    ) -> typing.Optional["PubsubTopicMessageStoragePolicy"]:
        return typing.cast(typing.Optional["PubsubTopicMessageStoragePolicy"], jsii.get(self, "messageStoragePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="messageTransformsInput")
    def message_transforms_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PubsubTopicMessageTransforms"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PubsubTopicMessageTransforms"]]], jsii.get(self, "messageTransformsInput"))

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
    def schema_settings_input(self) -> typing.Optional["PubsubTopicSchemaSettings"]:
        return typing.cast(typing.Optional["PubsubTopicSchemaSettings"], jsii.get(self, "schemaSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PubsubTopicTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PubsubTopicTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2abdd4060b24e09d6fe6987af1ef086218c13e76e6148c811b23e4cff5717b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72fa7672aa566e24bb50cc77bd00c52ed89ea9a32d4f04bd4635285dd0ce0ec9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d640dad8d18a35de9fd46eb8ff52061da45580e290693e6d70928154a8cc976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="messageRetentionDuration")
    def message_retention_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageRetentionDuration"))

    @message_retention_duration.setter
    def message_retention_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7846927d9bac7c315033c3ec696d98704d1262d2df818972b2adc3bc038b7da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageRetentionDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39c5564edf73340c51e04e6bb5c1d832c82e8f14f34f336cbf07a3c202c6045b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a62f0b65d89a68e9236ee4658b90b8948917dc78ad6a00588e5810bd19b180e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicConfig",
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
class PubsubTopicConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        ingestion_data_source_settings: typing.Optional[typing.Union["PubsubTopicIngestionDataSourceSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        message_retention_duration: typing.Optional[builtins.str] = None,
        message_storage_policy: typing.Optional[typing.Union["PubsubTopicMessageStoragePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        message_transforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PubsubTopicMessageTransforms", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        schema_settings: typing.Optional[typing.Union["PubsubTopicSchemaSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["PubsubTopicTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#name PubsubTopic#name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#id PubsubTopic#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ingestion_data_source_settings: ingestion_data_source_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#ingestion_data_source_settings PubsubTopic#ingestion_data_source_settings}
        :param kms_key_name: The resource name of the Cloud KMS CryptoKey to be used to protect access to messages published on this topic. Your project's PubSub service account ('service-{{PROJECT_NUMBER}}@gcp-sa-pubsub.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. The expected format is 'projects/* /locations/* /keyRings/* /cryptoKeys/*' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#kms_key_name PubsubTopic#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param labels: A set of key/value label pairs to assign to this Topic. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#labels PubsubTopic#labels}
        :param message_retention_duration: Indicates the minimum duration to retain a message after it is published to the topic. If this field is set, messages published to the topic in the last messageRetentionDuration are always available to subscribers. For instance, it allows any attached subscription to seek to a timestamp that is up to messageRetentionDuration in the past. If this field is not set, message retention is controlled by settings on individual subscriptions. The rotation period has the format of a decimal number, followed by the letter 's' (seconds). Cannot be more than 31 days or less than 10 minutes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#message_retention_duration PubsubTopic#message_retention_duration}
        :param message_storage_policy: message_storage_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#message_storage_policy PubsubTopic#message_storage_policy}
        :param message_transforms: message_transforms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#message_transforms PubsubTopic#message_transforms}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#project PubsubTopic#project}.
        :param schema_settings: schema_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#schema_settings PubsubTopic#schema_settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#timeouts PubsubTopic#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(ingestion_data_source_settings, dict):
            ingestion_data_source_settings = PubsubTopicIngestionDataSourceSettings(**ingestion_data_source_settings)
        if isinstance(message_storage_policy, dict):
            message_storage_policy = PubsubTopicMessageStoragePolicy(**message_storage_policy)
        if isinstance(schema_settings, dict):
            schema_settings = PubsubTopicSchemaSettings(**schema_settings)
        if isinstance(timeouts, dict):
            timeouts = PubsubTopicTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__327caa8e14d39eec3aad85ca2d4b60b93037ee83beffe48d7c74526cd948e637)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#name PubsubTopic#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#id PubsubTopic#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingestion_data_source_settings(
        self,
    ) -> typing.Optional["PubsubTopicIngestionDataSourceSettings"]:
        '''ingestion_data_source_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#ingestion_data_source_settings PubsubTopic#ingestion_data_source_settings}
        '''
        result = self._values.get("ingestion_data_source_settings")
        return typing.cast(typing.Optional["PubsubTopicIngestionDataSourceSettings"], result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''The resource name of the Cloud KMS CryptoKey to be used to protect access to messages published on this topic.

        Your project's PubSub service account
        ('service-{{PROJECT_NUMBER}}@gcp-sa-pubsub.iam.gserviceaccount.com') must have
        'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature.
        The expected format is 'projects/* /locations/* /keyRings/* /cryptoKeys/*'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#kms_key_name PubsubTopic#kms_key_name}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs to assign to this Topic.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#labels PubsubTopic#labels}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#message_retention_duration PubsubTopic#message_retention_duration}
        '''
        result = self._values.get("message_retention_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_storage_policy(
        self,
    ) -> typing.Optional["PubsubTopicMessageStoragePolicy"]:
        '''message_storage_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#message_storage_policy PubsubTopic#message_storage_policy}
        '''
        result = self._values.get("message_storage_policy")
        return typing.cast(typing.Optional["PubsubTopicMessageStoragePolicy"], result)

    @builtins.property
    def message_transforms(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PubsubTopicMessageTransforms"]]]:
        '''message_transforms block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#message_transforms PubsubTopic#message_transforms}
        '''
        result = self._values.get("message_transforms")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PubsubTopicMessageTransforms"]]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#project PubsubTopic#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_settings(self) -> typing.Optional["PubsubTopicSchemaSettings"]:
        '''schema_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#schema_settings PubsubTopic#schema_settings}
        '''
        result = self._values.get("schema_settings")
        return typing.cast(typing.Optional["PubsubTopicSchemaSettings"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["PubsubTopicTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#timeouts PubsubTopic#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["PubsubTopicTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubTopicConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicIngestionDataSourceSettings",
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
class PubsubTopicIngestionDataSourceSettings:
    def __init__(
        self,
        *,
        aws_kinesis: typing.Optional[typing.Union["PubsubTopicIngestionDataSourceSettingsAwsKinesis", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_msk: typing.Optional[typing.Union["PubsubTopicIngestionDataSourceSettingsAwsMsk", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_event_hubs: typing.Optional[typing.Union["PubsubTopicIngestionDataSourceSettingsAzureEventHubs", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_storage: typing.Optional[typing.Union["PubsubTopicIngestionDataSourceSettingsCloudStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        confluent_cloud: typing.Optional[typing.Union["PubsubTopicIngestionDataSourceSettingsConfluentCloud", typing.Dict[builtins.str, typing.Any]]] = None,
        platform_logs_settings: typing.Optional[typing.Union["PubsubTopicIngestionDataSourceSettingsPlatformLogsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws_kinesis: aws_kinesis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#aws_kinesis PubsubTopic#aws_kinesis}
        :param aws_msk: aws_msk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#aws_msk PubsubTopic#aws_msk}
        :param azure_event_hubs: azure_event_hubs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#azure_event_hubs PubsubTopic#azure_event_hubs}
        :param cloud_storage: cloud_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#cloud_storage PubsubTopic#cloud_storage}
        :param confluent_cloud: confluent_cloud block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#confluent_cloud PubsubTopic#confluent_cloud}
        :param platform_logs_settings: platform_logs_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#platform_logs_settings PubsubTopic#platform_logs_settings}
        '''
        if isinstance(aws_kinesis, dict):
            aws_kinesis = PubsubTopicIngestionDataSourceSettingsAwsKinesis(**aws_kinesis)
        if isinstance(aws_msk, dict):
            aws_msk = PubsubTopicIngestionDataSourceSettingsAwsMsk(**aws_msk)
        if isinstance(azure_event_hubs, dict):
            azure_event_hubs = PubsubTopicIngestionDataSourceSettingsAzureEventHubs(**azure_event_hubs)
        if isinstance(cloud_storage, dict):
            cloud_storage = PubsubTopicIngestionDataSourceSettingsCloudStorage(**cloud_storage)
        if isinstance(confluent_cloud, dict):
            confluent_cloud = PubsubTopicIngestionDataSourceSettingsConfluentCloud(**confluent_cloud)
        if isinstance(platform_logs_settings, dict):
            platform_logs_settings = PubsubTopicIngestionDataSourceSettingsPlatformLogsSettings(**platform_logs_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4d9d45b87cbabc5222b58e0cd90c1b1add270f6285f7fe74f61306c52fb2fcc)
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
    ) -> typing.Optional["PubsubTopicIngestionDataSourceSettingsAwsKinesis"]:
        '''aws_kinesis block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#aws_kinesis PubsubTopic#aws_kinesis}
        '''
        result = self._values.get("aws_kinesis")
        return typing.cast(typing.Optional["PubsubTopicIngestionDataSourceSettingsAwsKinesis"], result)

    @builtins.property
    def aws_msk(
        self,
    ) -> typing.Optional["PubsubTopicIngestionDataSourceSettingsAwsMsk"]:
        '''aws_msk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#aws_msk PubsubTopic#aws_msk}
        '''
        result = self._values.get("aws_msk")
        return typing.cast(typing.Optional["PubsubTopicIngestionDataSourceSettingsAwsMsk"], result)

    @builtins.property
    def azure_event_hubs(
        self,
    ) -> typing.Optional["PubsubTopicIngestionDataSourceSettingsAzureEventHubs"]:
        '''azure_event_hubs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#azure_event_hubs PubsubTopic#azure_event_hubs}
        '''
        result = self._values.get("azure_event_hubs")
        return typing.cast(typing.Optional["PubsubTopicIngestionDataSourceSettingsAzureEventHubs"], result)

    @builtins.property
    def cloud_storage(
        self,
    ) -> typing.Optional["PubsubTopicIngestionDataSourceSettingsCloudStorage"]:
        '''cloud_storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#cloud_storage PubsubTopic#cloud_storage}
        '''
        result = self._values.get("cloud_storage")
        return typing.cast(typing.Optional["PubsubTopicIngestionDataSourceSettingsCloudStorage"], result)

    @builtins.property
    def confluent_cloud(
        self,
    ) -> typing.Optional["PubsubTopicIngestionDataSourceSettingsConfluentCloud"]:
        '''confluent_cloud block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#confluent_cloud PubsubTopic#confluent_cloud}
        '''
        result = self._values.get("confluent_cloud")
        return typing.cast(typing.Optional["PubsubTopicIngestionDataSourceSettingsConfluentCloud"], result)

    @builtins.property
    def platform_logs_settings(
        self,
    ) -> typing.Optional["PubsubTopicIngestionDataSourceSettingsPlatformLogsSettings"]:
        '''platform_logs_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#platform_logs_settings PubsubTopic#platform_logs_settings}
        '''
        result = self._values.get("platform_logs_settings")
        return typing.cast(typing.Optional["PubsubTopicIngestionDataSourceSettingsPlatformLogsSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubTopicIngestionDataSourceSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicIngestionDataSourceSettingsAwsKinesis",
    jsii_struct_bases=[],
    name_mapping={
        "aws_role_arn": "awsRoleArn",
        "consumer_arn": "consumerArn",
        "gcp_service_account": "gcpServiceAccount",
        "stream_arn": "streamArn",
    },
)
class PubsubTopicIngestionDataSourceSettingsAwsKinesis:
    def __init__(
        self,
        *,
        aws_role_arn: builtins.str,
        consumer_arn: builtins.str,
        gcp_service_account: builtins.str,
        stream_arn: builtins.str,
    ) -> None:
        '''
        :param aws_role_arn: AWS role ARN to be used for Federated Identity authentication with Kinesis. Check the Pub/Sub docs for how to set up this role and the required permissions that need to be attached to it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#aws_role_arn PubsubTopic#aws_role_arn}
        :param consumer_arn: The Kinesis consumer ARN to used for ingestion in Enhanced Fan-Out mode. The consumer must be already created and ready to be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#consumer_arn PubsubTopic#consumer_arn}
        :param gcp_service_account: The GCP service account to be used for Federated Identity authentication with Kinesis (via a 'AssumeRoleWithWebIdentity' call for the provided role). The 'awsRoleArn' must be set up with 'accounts.google.com:sub' equals to this service account number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#gcp_service_account PubsubTopic#gcp_service_account}
        :param stream_arn: The Kinesis stream ARN to ingest data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#stream_arn PubsubTopic#stream_arn}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27f19aa50a07dc992a8fa3377e488bc230ce92fe9d073d6dd3a814b2851136fa)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#aws_role_arn PubsubTopic#aws_role_arn}
        '''
        result = self._values.get("aws_role_arn")
        assert result is not None, "Required property 'aws_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def consumer_arn(self) -> builtins.str:
        '''The Kinesis consumer ARN to used for ingestion in Enhanced Fan-Out mode.

        The consumer must be already
        created and ready to be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#consumer_arn PubsubTopic#consumer_arn}
        '''
        result = self._values.get("consumer_arn")
        assert result is not None, "Required property 'consumer_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gcp_service_account(self) -> builtins.str:
        '''The GCP service account to be used for Federated Identity authentication with Kinesis (via a 'AssumeRoleWithWebIdentity' call for the provided role).

        The 'awsRoleArn' must be set up with 'accounts.google.com:sub'
        equals to this service account number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#gcp_service_account PubsubTopic#gcp_service_account}
        '''
        result = self._values.get("gcp_service_account")
        assert result is not None, "Required property 'gcp_service_account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stream_arn(self) -> builtins.str:
        '''The Kinesis stream ARN to ingest data from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#stream_arn PubsubTopic#stream_arn}
        '''
        result = self._values.get("stream_arn")
        assert result is not None, "Required property 'stream_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubTopicIngestionDataSourceSettingsAwsKinesis(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubTopicIngestionDataSourceSettingsAwsKinesisOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicIngestionDataSourceSettingsAwsKinesisOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c4f4b130d9c6a378c7726330ca83cbc21a8303cea2e9c33a4b02f43ee2400ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20c7bd10f0756c84c70114e2323ddf5c6580c4e711343c7a2bfb0f178b2037b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerArn")
    def consumer_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerArn"))

    @consumer_arn.setter
    def consumer_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fbca0712d33d531a2215485d18f59bf5943387c20c73e538416a44976c3bcb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccount")
    def gcp_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpServiceAccount"))

    @gcp_service_account.setter
    def gcp_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f027732ecaad38982f80c1164ba7ee61373d5d26d2cd95b7cf700ef2df1cb53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streamArn")
    def stream_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streamArn"))

    @stream_arn.setter
    def stream_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b4a3ff64843cff9d737b46b7b04251a1dc7b6f50418b71141807dcd1e9711b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PubsubTopicIngestionDataSourceSettingsAwsKinesis]:
        return typing.cast(typing.Optional[PubsubTopicIngestionDataSourceSettingsAwsKinesis], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubTopicIngestionDataSourceSettingsAwsKinesis],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5987bcb292b1be9f872a40a66dacd9827949cfd6ab87acf5247d998175b917d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicIngestionDataSourceSettingsAwsMsk",
    jsii_struct_bases=[],
    name_mapping={
        "aws_role_arn": "awsRoleArn",
        "cluster_arn": "clusterArn",
        "gcp_service_account": "gcpServiceAccount",
        "topic": "topic",
    },
)
class PubsubTopicIngestionDataSourceSettingsAwsMsk:
    def __init__(
        self,
        *,
        aws_role_arn: builtins.str,
        cluster_arn: builtins.str,
        gcp_service_account: builtins.str,
        topic: builtins.str,
    ) -> None:
        '''
        :param aws_role_arn: AWS role ARN to be used for Federated Identity authentication with MSK. Check the Pub/Sub docs for how to set up this role and the required permissions that need to be attached to it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#aws_role_arn PubsubTopic#aws_role_arn}
        :param cluster_arn: ARN that uniquely identifies the MSK cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#cluster_arn PubsubTopic#cluster_arn}
        :param gcp_service_account: The GCP service account to be used for Federated Identity authentication with MSK (via a 'AssumeRoleWithWebIdentity' call for the provided role). The 'awsRoleArn' must be set up with 'accounts.google.com:sub' equals to this service account number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#gcp_service_account PubsubTopic#gcp_service_account}
        :param topic: The name of the MSK topic that Pub/Sub will import from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#topic PubsubTopic#topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eefd0227008352a9df18c2573584a05e1a8ad677a343426f04f515015b5ab4a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#aws_role_arn PubsubTopic#aws_role_arn}
        '''
        result = self._values.get("aws_role_arn")
        assert result is not None, "Required property 'aws_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_arn(self) -> builtins.str:
        '''ARN that uniquely identifies the MSK cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#cluster_arn PubsubTopic#cluster_arn}
        '''
        result = self._values.get("cluster_arn")
        assert result is not None, "Required property 'cluster_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gcp_service_account(self) -> builtins.str:
        '''The GCP service account to be used for Federated Identity authentication with MSK (via a 'AssumeRoleWithWebIdentity' call for the provided role).

        The 'awsRoleArn' must be set up with 'accounts.google.com:sub'
        equals to this service account number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#gcp_service_account PubsubTopic#gcp_service_account}
        '''
        result = self._values.get("gcp_service_account")
        assert result is not None, "Required property 'gcp_service_account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''The name of the MSK topic that Pub/Sub will import from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#topic PubsubTopic#topic}
        '''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubTopicIngestionDataSourceSettingsAwsMsk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubTopicIngestionDataSourceSettingsAwsMskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicIngestionDataSourceSettingsAwsMskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47a8e35ca7449e565dd03251926fb73d209615ccbee0fb18a6c335749a0b6668)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ac52365428b7cd770e23cd6dd1b633151fa17a377b6c182d0e312a87048a250)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterArn"))

    @cluster_arn.setter
    def cluster_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__088ac5c3e5651443f5e0e72be8557d216a8687d576649ca6fc8ac5f9764710b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccount")
    def gcp_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpServiceAccount"))

    @gcp_service_account.setter
    def gcp_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4de7a9a8e2cf658364b74cd272983ee95d80ce8d694b76555e45779eeac08ddd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b235f176bb43d88d993afb8ac92c440694b04b346bd1f60635ca23fbb2e5a41e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PubsubTopicIngestionDataSourceSettingsAwsMsk]:
        return typing.cast(typing.Optional[PubsubTopicIngestionDataSourceSettingsAwsMsk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubTopicIngestionDataSourceSettingsAwsMsk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd670e2fd6c5a8405b1631a7365aa7b8f3053036153217c3ba6bec85949889a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicIngestionDataSourceSettingsAzureEventHubs",
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
class PubsubTopicIngestionDataSourceSettingsAzureEventHubs:
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
        :param client_id: The Azure event hub client ID to use for ingestion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#client_id PubsubTopic#client_id}
        :param event_hub: The Azure event hub to ingest data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#event_hub PubsubTopic#event_hub}
        :param gcp_service_account: The GCP service account to be used for Federated Identity authentication with Azure (via a 'AssumeRoleWithWebIdentity' call for the provided role). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#gcp_service_account PubsubTopic#gcp_service_account}
        :param namespace: The Azure event hub namespace to ingest data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#namespace PubsubTopic#namespace}
        :param resource_group: The name of the resource group within an Azure subscription. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#resource_group PubsubTopic#resource_group}
        :param subscription_id: The Azure event hub subscription ID to use for ingestion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#subscription_id PubsubTopic#subscription_id}
        :param tenant_id: The Azure event hub tenant ID to use for ingestion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#tenant_id PubsubTopic#tenant_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4de7d74087af1aaff78a5f2ec132051092de1f130885df3c3c855e91cf18eea7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#client_id PubsubTopic#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_hub(self) -> typing.Optional[builtins.str]:
        '''The Azure event hub to ingest data from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#event_hub PubsubTopic#event_hub}
        '''
        result = self._values.get("event_hub")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcp_service_account(self) -> typing.Optional[builtins.str]:
        '''The GCP service account to be used for Federated Identity authentication with Azure (via a 'AssumeRoleWithWebIdentity' call for the provided role).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#gcp_service_account PubsubTopic#gcp_service_account}
        '''
        result = self._values.get("gcp_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The Azure event hub namespace to ingest data from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#namespace PubsubTopic#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_group(self) -> typing.Optional[builtins.str]:
        '''The name of the resource group within an Azure subscription.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#resource_group PubsubTopic#resource_group}
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscription_id(self) -> typing.Optional[builtins.str]:
        '''The Azure event hub subscription ID to use for ingestion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#subscription_id PubsubTopic#subscription_id}
        '''
        result = self._values.get("subscription_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''The Azure event hub tenant ID to use for ingestion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#tenant_id PubsubTopic#tenant_id}
        '''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubTopicIngestionDataSourceSettingsAzureEventHubs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubTopicIngestionDataSourceSettingsAzureEventHubsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicIngestionDataSourceSettingsAzureEventHubsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55121a4db7e09816e0d43b58c6e2700d0968fbfe85e55ab2042419ea9fa078ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5edb45de7c4dfd7d4be842aa3a7af780ae5f3d75fb829af57c86b3913d3812c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventHub")
    def event_hub(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventHub"))

    @event_hub.setter
    def event_hub(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9582df58f80312028de90358da9713a43e01b21d175b453c4cc4f9c746a4f531)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventHub", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccount")
    def gcp_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpServiceAccount"))

    @gcp_service_account.setter
    def gcp_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8d0af5fefd656eea383c4277576167cd519c76383bf9966deb9bab3e6163f73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2296100119afe62be4f54a478f03aa99f7d5e3b7d77fae50dc885daf7eb8c947)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroup")
    def resource_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroup"))

    @resource_group.setter
    def resource_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7533d17a4ac581dc9850ee20ee8f8dd481fad547f40d522a6399a5826405f0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subscriptionId")
    def subscription_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subscriptionId"))

    @subscription_id.setter
    def subscription_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a8353b21087564d1e18827a73388932390bf909cf178ce2c262ab28f2faf783)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscriptionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a32fb6bba2320f271c16cf26593991dc33db2f0af3ddf140357f88de9b369271)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PubsubTopicIngestionDataSourceSettingsAzureEventHubs]:
        return typing.cast(typing.Optional[PubsubTopicIngestionDataSourceSettingsAzureEventHubs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubTopicIngestionDataSourceSettingsAzureEventHubs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cab08234dbe4f04ad7fa3517666c3d21bd94c37bdea12baddf87ce1234ccfa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicIngestionDataSourceSettingsCloudStorage",
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
class PubsubTopicIngestionDataSourceSettingsCloudStorage:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        avro_format: typing.Optional[typing.Union["PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat", typing.Dict[builtins.str, typing.Any]]] = None,
        match_glob: typing.Optional[builtins.str] = None,
        minimum_object_create_time: typing.Optional[builtins.str] = None,
        pubsub_avro_format: typing.Optional[typing.Union["PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat", typing.Dict[builtins.str, typing.Any]]] = None,
        text_format: typing.Optional[typing.Union["PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket: Cloud Storage bucket. The bucket name must be without any prefix like "gs://". See the bucket naming requirements: https://cloud.google.com/storage/docs/buckets#naming. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#bucket PubsubTopic#bucket}
        :param avro_format: avro_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#avro_format PubsubTopic#avro_format}
        :param match_glob: Glob pattern used to match objects that will be ingested. If unset, all objects will be ingested. See the supported patterns: https://cloud.google.com/storage/docs/json_api/v1/objects/list#list-objects-and-prefixes-using-glob Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#match_glob PubsubTopic#match_glob}
        :param minimum_object_create_time: The timestamp set in RFC3339 text format. If set, only objects with a larger or equal timestamp will be ingested. Unset by default, meaning all objects will be ingested. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#minimum_object_create_time PubsubTopic#minimum_object_create_time}
        :param pubsub_avro_format: pubsub_avro_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#pubsub_avro_format PubsubTopic#pubsub_avro_format}
        :param text_format: text_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#text_format PubsubTopic#text_format}
        '''
        if isinstance(avro_format, dict):
            avro_format = PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat(**avro_format)
        if isinstance(pubsub_avro_format, dict):
            pubsub_avro_format = PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat(**pubsub_avro_format)
        if isinstance(text_format, dict):
            text_format = PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat(**text_format)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6f2095ffb540c6325805d0e96c566e23b27e504378db5a644f558683b9b5cd8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#bucket PubsubTopic#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def avro_format(
        self,
    ) -> typing.Optional["PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat"]:
        '''avro_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#avro_format PubsubTopic#avro_format}
        '''
        result = self._values.get("avro_format")
        return typing.cast(typing.Optional["PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat"], result)

    @builtins.property
    def match_glob(self) -> typing.Optional[builtins.str]:
        '''Glob pattern used to match objects that will be ingested.

        If unset, all
        objects will be ingested. See the supported patterns:
        https://cloud.google.com/storage/docs/json_api/v1/objects/list#list-objects-and-prefixes-using-glob

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#match_glob PubsubTopic#match_glob}
        '''
        result = self._values.get("match_glob")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum_object_create_time(self) -> typing.Optional[builtins.str]:
        '''The timestamp set in RFC3339 text format.

        If set, only objects with a
        larger or equal timestamp will be ingested. Unset by default, meaning
        all objects will be ingested.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#minimum_object_create_time PubsubTopic#minimum_object_create_time}
        '''
        result = self._values.get("minimum_object_create_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pubsub_avro_format(
        self,
    ) -> typing.Optional["PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat"]:
        '''pubsub_avro_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#pubsub_avro_format PubsubTopic#pubsub_avro_format}
        '''
        result = self._values.get("pubsub_avro_format")
        return typing.cast(typing.Optional["PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat"], result)

    @builtins.property
    def text_format(
        self,
    ) -> typing.Optional["PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat"]:
        '''text_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#text_format PubsubTopic#text_format}
        '''
        result = self._values.get("text_format")
        return typing.cast(typing.Optional["PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubTopicIngestionDataSourceSettingsCloudStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbaa4b697ed94ce14cacf4b44ffe1928921e9feb96a8d49e71db4e56d02d412c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat]:
        return typing.cast(typing.Optional[PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65085a207885ad8533e88b49f4f50ca289398a2bc0be813e4e7e4aa24627af33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PubsubTopicIngestionDataSourceSettingsCloudStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicIngestionDataSourceSettingsCloudStorageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2139f5fdeb4301085d72c2bafd044545df841af9af8456e50f1d24b8eba0ac88)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAvroFormat")
    def put_avro_format(self) -> None:
        value = PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat()

        return typing.cast(None, jsii.invoke(self, "putAvroFormat", [value]))

    @jsii.member(jsii_name="putPubsubAvroFormat")
    def put_pubsub_avro_format(self) -> None:
        value = PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat()

        return typing.cast(None, jsii.invoke(self, "putPubsubAvroFormat", [value]))

    @jsii.member(jsii_name="putTextFormat")
    def put_text_format(
        self,
        *,
        delimiter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delimiter: The delimiter to use when using the 'text' format. Each line of text as specified by the delimiter will be set to the 'data' field of a Pub/Sub message. When unset, '\\n' is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#delimiter PubsubTopic#delimiter}
        '''
        value = PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat(
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
    ) -> PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormatOutputReference:
        return typing.cast(PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormatOutputReference, jsii.get(self, "avroFormat"))

    @builtins.property
    @jsii.member(jsii_name="pubsubAvroFormat")
    def pubsub_avro_format(
        self,
    ) -> "PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormatOutputReference":
        return typing.cast("PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormatOutputReference", jsii.get(self, "pubsubAvroFormat"))

    @builtins.property
    @jsii.member(jsii_name="textFormat")
    def text_format(
        self,
    ) -> "PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormatOutputReference":
        return typing.cast("PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormatOutputReference", jsii.get(self, "textFormat"))

    @builtins.property
    @jsii.member(jsii_name="avroFormatInput")
    def avro_format_input(
        self,
    ) -> typing.Optional[PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat]:
        return typing.cast(typing.Optional[PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat], jsii.get(self, "avroFormatInput"))

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
    ) -> typing.Optional["PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat"]:
        return typing.cast(typing.Optional["PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat"], jsii.get(self, "pubsubAvroFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="textFormatInput")
    def text_format_input(
        self,
    ) -> typing.Optional["PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat"]:
        return typing.cast(typing.Optional["PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat"], jsii.get(self, "textFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3771ceed42005f70e18cac3cb7ec2164fc7312ef21ee52fe2944b33ce458cebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchGlob")
    def match_glob(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchGlob"))

    @match_glob.setter
    def match_glob(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dc34fc712776511881dbcc0bf582dc863d0363041727fcb7b3b2debdbeb7cf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchGlob", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumObjectCreateTime")
    def minimum_object_create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumObjectCreateTime"))

    @minimum_object_create_time.setter
    def minimum_object_create_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fdba0b5077e9861fb9661ba8d5eab92607bc66480a82fd275af8731c302f5de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumObjectCreateTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PubsubTopicIngestionDataSourceSettingsCloudStorage]:
        return typing.cast(typing.Optional[PubsubTopicIngestionDataSourceSettingsCloudStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubTopicIngestionDataSourceSettingsCloudStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66353aed15741b44dbc97816de3386ab719e2e8915f65fa6077cc2337f47eed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39c4978f0ed965c7961cf5a6a0ee33824d100a6af52e48bd7e34db441bcee766)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat]:
        return typing.cast(typing.Optional[PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36fb6c8ed58d476ae57f727d4325abdfc11a31970c1dc353b7b7e71c34e8cae9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat",
    jsii_struct_bases=[],
    name_mapping={"delimiter": "delimiter"},
)
class PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat:
    def __init__(self, *, delimiter: typing.Optional[builtins.str] = None) -> None:
        '''
        :param delimiter: The delimiter to use when using the 'text' format. Each line of text as specified by the delimiter will be set to the 'data' field of a Pub/Sub message. When unset, '\\n' is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#delimiter PubsubTopic#delimiter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f40583c2140ff95e6741181becced4820725dde9fc0a2a4aab0c86f973369128)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#delimiter PubsubTopic#delimiter}
        '''
        result = self._values.get("delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7924a47106fa6b618e2d748b7fc14adeda3a068cb56c947a13c831597b17b65)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbb2c87c685a497473bb9a218ec37651f2765a37238e8951fa7bf1a674e96bab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat]:
        return typing.cast(typing.Optional[PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab196b203e31d00bb20d9fd1800ce86867f415697ed15dfdb999f1904a9c8455)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicIngestionDataSourceSettingsConfluentCloud",
    jsii_struct_bases=[],
    name_mapping={
        "bootstrap_server": "bootstrapServer",
        "gcp_service_account": "gcpServiceAccount",
        "identity_pool_id": "identityPoolId",
        "topic": "topic",
        "cluster_id": "clusterId",
    },
)
class PubsubTopicIngestionDataSourceSettingsConfluentCloud:
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
        :param bootstrap_server: The Confluent Cloud bootstrap server. The format is url:port. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#bootstrap_server PubsubTopic#bootstrap_server}
        :param gcp_service_account: The GCP service account to be used for Federated Identity authentication with Confluent Cloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#gcp_service_account PubsubTopic#gcp_service_account}
        :param identity_pool_id: Identity pool ID to be used for Federated Identity authentication with Confluent Cloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#identity_pool_id PubsubTopic#identity_pool_id}
        :param topic: Name of the Confluent Cloud topic that Pub/Sub will import from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#topic PubsubTopic#topic}
        :param cluster_id: The Confluent Cloud cluster ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#cluster_id PubsubTopic#cluster_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__436fd1bcf6e13adb53578bdd2dbbe284ae9022702779a2a82ff7f827dd753241)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#bootstrap_server PubsubTopic#bootstrap_server}
        '''
        result = self._values.get("bootstrap_server")
        assert result is not None, "Required property 'bootstrap_server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gcp_service_account(self) -> builtins.str:
        '''The GCP service account to be used for Federated Identity authentication with Confluent Cloud.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#gcp_service_account PubsubTopic#gcp_service_account}
        '''
        result = self._values.get("gcp_service_account")
        assert result is not None, "Required property 'gcp_service_account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_pool_id(self) -> builtins.str:
        '''Identity pool ID to be used for Federated Identity authentication with Confluent Cloud.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#identity_pool_id PubsubTopic#identity_pool_id}
        '''
        result = self._values.get("identity_pool_id")
        assert result is not None, "Required property 'identity_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''Name of the Confluent Cloud topic that Pub/Sub will import from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#topic PubsubTopic#topic}
        '''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_id(self) -> typing.Optional[builtins.str]:
        '''The Confluent Cloud cluster ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#cluster_id PubsubTopic#cluster_id}
        '''
        result = self._values.get("cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubTopicIngestionDataSourceSettingsConfluentCloud(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubTopicIngestionDataSourceSettingsConfluentCloudOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicIngestionDataSourceSettingsConfluentCloudOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5a84427e1cf1e0b4b55d5ae77a8b362f2549e1059f35b4f8fb379f7e4544991)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5243f82c55e32a5dd5b375ca8360a659a7ac9b9c1d49ec3c587fa3f575b067a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootstrapServer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb36d8dab4b7d687746187f42f082c46daec50ea21fa1388dc6ea7c69c97699e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccount")
    def gcp_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpServiceAccount"))

    @gcp_service_account.setter
    def gcp_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__841f74e13e1851d46272f5295d41e218a07895c6bf80be306124f6b910a34c2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityPoolId")
    def identity_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityPoolId"))

    @identity_pool_id.setter
    def identity_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8e822af20548e30763a6f3c4338f1819d7db798f95ef253e5cdcf365c60a8c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityPoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14142b42939eeeb400f250d2730eabd81b443cac16d82967713718b00659b591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PubsubTopicIngestionDataSourceSettingsConfluentCloud]:
        return typing.cast(typing.Optional[PubsubTopicIngestionDataSourceSettingsConfluentCloud], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubTopicIngestionDataSourceSettingsConfluentCloud],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3229fcc4b49ffa233cee1ef38ea6ef020731d513e588be474bc32f07cb4ffdb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PubsubTopicIngestionDataSourceSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicIngestionDataSourceSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cef87ae3a12aa844f761dea9cf7f7e7d1efb44928a928d1ebf3c7d2d7a0db889)
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
        :param aws_role_arn: AWS role ARN to be used for Federated Identity authentication with Kinesis. Check the Pub/Sub docs for how to set up this role and the required permissions that need to be attached to it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#aws_role_arn PubsubTopic#aws_role_arn}
        :param consumer_arn: The Kinesis consumer ARN to used for ingestion in Enhanced Fan-Out mode. The consumer must be already created and ready to be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#consumer_arn PubsubTopic#consumer_arn}
        :param gcp_service_account: The GCP service account to be used for Federated Identity authentication with Kinesis (via a 'AssumeRoleWithWebIdentity' call for the provided role). The 'awsRoleArn' must be set up with 'accounts.google.com:sub' equals to this service account number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#gcp_service_account PubsubTopic#gcp_service_account}
        :param stream_arn: The Kinesis stream ARN to ingest data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#stream_arn PubsubTopic#stream_arn}
        '''
        value = PubsubTopicIngestionDataSourceSettingsAwsKinesis(
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
        :param aws_role_arn: AWS role ARN to be used for Federated Identity authentication with MSK. Check the Pub/Sub docs for how to set up this role and the required permissions that need to be attached to it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#aws_role_arn PubsubTopic#aws_role_arn}
        :param cluster_arn: ARN that uniquely identifies the MSK cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#cluster_arn PubsubTopic#cluster_arn}
        :param gcp_service_account: The GCP service account to be used for Federated Identity authentication with MSK (via a 'AssumeRoleWithWebIdentity' call for the provided role). The 'awsRoleArn' must be set up with 'accounts.google.com:sub' equals to this service account number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#gcp_service_account PubsubTopic#gcp_service_account}
        :param topic: The name of the MSK topic that Pub/Sub will import from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#topic PubsubTopic#topic}
        '''
        value = PubsubTopicIngestionDataSourceSettingsAwsMsk(
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
        :param client_id: The Azure event hub client ID to use for ingestion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#client_id PubsubTopic#client_id}
        :param event_hub: The Azure event hub to ingest data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#event_hub PubsubTopic#event_hub}
        :param gcp_service_account: The GCP service account to be used for Federated Identity authentication with Azure (via a 'AssumeRoleWithWebIdentity' call for the provided role). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#gcp_service_account PubsubTopic#gcp_service_account}
        :param namespace: The Azure event hub namespace to ingest data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#namespace PubsubTopic#namespace}
        :param resource_group: The name of the resource group within an Azure subscription. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#resource_group PubsubTopic#resource_group}
        :param subscription_id: The Azure event hub subscription ID to use for ingestion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#subscription_id PubsubTopic#subscription_id}
        :param tenant_id: The Azure event hub tenant ID to use for ingestion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#tenant_id PubsubTopic#tenant_id}
        '''
        value = PubsubTopicIngestionDataSourceSettingsAzureEventHubs(
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
        avro_format: typing.Optional[typing.Union[PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat, typing.Dict[builtins.str, typing.Any]]] = None,
        match_glob: typing.Optional[builtins.str] = None,
        minimum_object_create_time: typing.Optional[builtins.str] = None,
        pubsub_avro_format: typing.Optional[typing.Union[PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat, typing.Dict[builtins.str, typing.Any]]] = None,
        text_format: typing.Optional[typing.Union[PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket: Cloud Storage bucket. The bucket name must be without any prefix like "gs://". See the bucket naming requirements: https://cloud.google.com/storage/docs/buckets#naming. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#bucket PubsubTopic#bucket}
        :param avro_format: avro_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#avro_format PubsubTopic#avro_format}
        :param match_glob: Glob pattern used to match objects that will be ingested. If unset, all objects will be ingested. See the supported patterns: https://cloud.google.com/storage/docs/json_api/v1/objects/list#list-objects-and-prefixes-using-glob Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#match_glob PubsubTopic#match_glob}
        :param minimum_object_create_time: The timestamp set in RFC3339 text format. If set, only objects with a larger or equal timestamp will be ingested. Unset by default, meaning all objects will be ingested. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#minimum_object_create_time PubsubTopic#minimum_object_create_time}
        :param pubsub_avro_format: pubsub_avro_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#pubsub_avro_format PubsubTopic#pubsub_avro_format}
        :param text_format: text_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#text_format PubsubTopic#text_format}
        '''
        value = PubsubTopicIngestionDataSourceSettingsCloudStorage(
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
        :param bootstrap_server: The Confluent Cloud bootstrap server. The format is url:port. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#bootstrap_server PubsubTopic#bootstrap_server}
        :param gcp_service_account: The GCP service account to be used for Federated Identity authentication with Confluent Cloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#gcp_service_account PubsubTopic#gcp_service_account}
        :param identity_pool_id: Identity pool ID to be used for Federated Identity authentication with Confluent Cloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#identity_pool_id PubsubTopic#identity_pool_id}
        :param topic: Name of the Confluent Cloud topic that Pub/Sub will import from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#topic PubsubTopic#topic}
        :param cluster_id: The Confluent Cloud cluster ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#cluster_id PubsubTopic#cluster_id}
        '''
        value = PubsubTopicIngestionDataSourceSettingsConfluentCloud(
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
        :param severity: The minimum severity level of Platform Logs that will be written. If unspecified, no Platform Logs will be written. Default value: "SEVERITY_UNSPECIFIED" Possible values: ["SEVERITY_UNSPECIFIED", "DISABLED", "DEBUG", "INFO", "WARNING", "ERROR"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#severity PubsubTopic#severity}
        '''
        value = PubsubTopicIngestionDataSourceSettingsPlatformLogsSettings(
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
    ) -> PubsubTopicIngestionDataSourceSettingsAwsKinesisOutputReference:
        return typing.cast(PubsubTopicIngestionDataSourceSettingsAwsKinesisOutputReference, jsii.get(self, "awsKinesis"))

    @builtins.property
    @jsii.member(jsii_name="awsMsk")
    def aws_msk(self) -> PubsubTopicIngestionDataSourceSettingsAwsMskOutputReference:
        return typing.cast(PubsubTopicIngestionDataSourceSettingsAwsMskOutputReference, jsii.get(self, "awsMsk"))

    @builtins.property
    @jsii.member(jsii_name="azureEventHubs")
    def azure_event_hubs(
        self,
    ) -> PubsubTopicIngestionDataSourceSettingsAzureEventHubsOutputReference:
        return typing.cast(PubsubTopicIngestionDataSourceSettingsAzureEventHubsOutputReference, jsii.get(self, "azureEventHubs"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorage")
    def cloud_storage(
        self,
    ) -> PubsubTopicIngestionDataSourceSettingsCloudStorageOutputReference:
        return typing.cast(PubsubTopicIngestionDataSourceSettingsCloudStorageOutputReference, jsii.get(self, "cloudStorage"))

    @builtins.property
    @jsii.member(jsii_name="confluentCloud")
    def confluent_cloud(
        self,
    ) -> PubsubTopicIngestionDataSourceSettingsConfluentCloudOutputReference:
        return typing.cast(PubsubTopicIngestionDataSourceSettingsConfluentCloudOutputReference, jsii.get(self, "confluentCloud"))

    @builtins.property
    @jsii.member(jsii_name="platformLogsSettings")
    def platform_logs_settings(
        self,
    ) -> "PubsubTopicIngestionDataSourceSettingsPlatformLogsSettingsOutputReference":
        return typing.cast("PubsubTopicIngestionDataSourceSettingsPlatformLogsSettingsOutputReference", jsii.get(self, "platformLogsSettings"))

    @builtins.property
    @jsii.member(jsii_name="awsKinesisInput")
    def aws_kinesis_input(
        self,
    ) -> typing.Optional[PubsubTopicIngestionDataSourceSettingsAwsKinesis]:
        return typing.cast(typing.Optional[PubsubTopicIngestionDataSourceSettingsAwsKinesis], jsii.get(self, "awsKinesisInput"))

    @builtins.property
    @jsii.member(jsii_name="awsMskInput")
    def aws_msk_input(
        self,
    ) -> typing.Optional[PubsubTopicIngestionDataSourceSettingsAwsMsk]:
        return typing.cast(typing.Optional[PubsubTopicIngestionDataSourceSettingsAwsMsk], jsii.get(self, "awsMskInput"))

    @builtins.property
    @jsii.member(jsii_name="azureEventHubsInput")
    def azure_event_hubs_input(
        self,
    ) -> typing.Optional[PubsubTopicIngestionDataSourceSettingsAzureEventHubs]:
        return typing.cast(typing.Optional[PubsubTopicIngestionDataSourceSettingsAzureEventHubs], jsii.get(self, "azureEventHubsInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageInput")
    def cloud_storage_input(
        self,
    ) -> typing.Optional[PubsubTopicIngestionDataSourceSettingsCloudStorage]:
        return typing.cast(typing.Optional[PubsubTopicIngestionDataSourceSettingsCloudStorage], jsii.get(self, "cloudStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="confluentCloudInput")
    def confluent_cloud_input(
        self,
    ) -> typing.Optional[PubsubTopicIngestionDataSourceSettingsConfluentCloud]:
        return typing.cast(typing.Optional[PubsubTopicIngestionDataSourceSettingsConfluentCloud], jsii.get(self, "confluentCloudInput"))

    @builtins.property
    @jsii.member(jsii_name="platformLogsSettingsInput")
    def platform_logs_settings_input(
        self,
    ) -> typing.Optional["PubsubTopicIngestionDataSourceSettingsPlatformLogsSettings"]:
        return typing.cast(typing.Optional["PubsubTopicIngestionDataSourceSettingsPlatformLogsSettings"], jsii.get(self, "platformLogsSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PubsubTopicIngestionDataSourceSettings]:
        return typing.cast(typing.Optional[PubsubTopicIngestionDataSourceSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubTopicIngestionDataSourceSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30458bbc60049d915278766f842640fcd614231a678e7d454d8cccd0cc6af8ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicIngestionDataSourceSettingsPlatformLogsSettings",
    jsii_struct_bases=[],
    name_mapping={"severity": "severity"},
)
class PubsubTopicIngestionDataSourceSettingsPlatformLogsSettings:
    def __init__(self, *, severity: typing.Optional[builtins.str] = None) -> None:
        '''
        :param severity: The minimum severity level of Platform Logs that will be written. If unspecified, no Platform Logs will be written. Default value: "SEVERITY_UNSPECIFIED" Possible values: ["SEVERITY_UNSPECIFIED", "DISABLED", "DEBUG", "INFO", "WARNING", "ERROR"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#severity PubsubTopic#severity}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87daa3461a23c77188c9ce9b57663af7d34365f42bbedc26ad2bd0eb9285ef45)
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if severity is not None:
            self._values["severity"] = severity

    @builtins.property
    def severity(self) -> typing.Optional[builtins.str]:
        '''The minimum severity level of Platform Logs that will be written.

        If unspecified,
        no Platform Logs will be written. Default value: "SEVERITY_UNSPECIFIED" Possible values: ["SEVERITY_UNSPECIFIED", "DISABLED", "DEBUG", "INFO", "WARNING", "ERROR"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#severity PubsubTopic#severity}
        '''
        result = self._values.get("severity")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubTopicIngestionDataSourceSettingsPlatformLogsSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubTopicIngestionDataSourceSettingsPlatformLogsSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicIngestionDataSourceSettingsPlatformLogsSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bab23d2024dafe3cd2d26154a4492f206e86825100e5f290eb0911eb3d2f58f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b9781dfe486731293563f41baf92b68af2b83b77c1f9195a403bb6df80d92fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PubsubTopicIngestionDataSourceSettingsPlatformLogsSettings]:
        return typing.cast(typing.Optional[PubsubTopicIngestionDataSourceSettingsPlatformLogsSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubTopicIngestionDataSourceSettingsPlatformLogsSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb4927ad0a0c3c017be8dde3dac0c82c38c239602c1f9e180bf30e96ec188bc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicMessageStoragePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_persistence_regions": "allowedPersistenceRegions",
        "enforce_in_transit": "enforceInTransit",
    },
)
class PubsubTopicMessageStoragePolicy:
    def __init__(
        self,
        *,
        allowed_persistence_regions: typing.Sequence[builtins.str],
        enforce_in_transit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_persistence_regions: A list of IDs of GCP regions where messages that are published to the topic may be persisted in storage. Messages published by publishers running in non-allowed GCP regions (or running outside of GCP altogether) will be routed for storage in one of the allowed regions. An empty list means that no regions are allowed, and is not a valid configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#allowed_persistence_regions PubsubTopic#allowed_persistence_regions}
        :param enforce_in_transit: If true, 'allowedPersistenceRegions' is also used to enforce in-transit guarantees for messages. That is, Pub/Sub will fail topics.publish operations on this topic and subscribe operations on any subscription attached to this topic in any region that is not in 'allowedPersistenceRegions'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#enforce_in_transit PubsubTopic#enforce_in_transit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7acfce2f26378d4dd851ee8b921b9a42a96b61fda75583caa51f0fc5ead3c5c6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#allowed_persistence_regions PubsubTopic#allowed_persistence_regions}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#enforce_in_transit PubsubTopic#enforce_in_transit}
        '''
        result = self._values.get("enforce_in_transit")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubTopicMessageStoragePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubTopicMessageStoragePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicMessageStoragePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee36bc0e41749624d550b0b4ffbf1bd0479949d160a28978f13cbf9d0832daa8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd47e18688f01a4de33db3cda5cc7cf2368d074fc724ab4ad0454fa06670b1ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8af2631b2bc47640d88bc8a7a6917d98272a2215e61913b71ddc6aee9a27827b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceInTransit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PubsubTopicMessageStoragePolicy]:
        return typing.cast(typing.Optional[PubsubTopicMessageStoragePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubTopicMessageStoragePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ada06454be42e6f402f600fd28a01f0dd64720bf1a633a76b7df309f85f4b039)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicMessageTransforms",
    jsii_struct_bases=[],
    name_mapping={"disabled": "disabled", "javascript_udf": "javascriptUdf"},
)
class PubsubTopicMessageTransforms:
    def __init__(
        self,
        *,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        javascript_udf: typing.Optional[typing.Union["PubsubTopicMessageTransformsJavascriptUdf", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param disabled: Controls whether or not to use this transform. If not set or 'false', the transform will be applied to messages. Default: 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#disabled PubsubTopic#disabled}
        :param javascript_udf: javascript_udf block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#javascript_udf PubsubTopic#javascript_udf}
        '''
        if isinstance(javascript_udf, dict):
            javascript_udf = PubsubTopicMessageTransformsJavascriptUdf(**javascript_udf)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607d7fb70cc745bfcfe96633eb9673a3aedd7a595a04d9a0bf51bf20f69da497)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#disabled PubsubTopic#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def javascript_udf(
        self,
    ) -> typing.Optional["PubsubTopicMessageTransformsJavascriptUdf"]:
        '''javascript_udf block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#javascript_udf PubsubTopic#javascript_udf}
        '''
        result = self._values.get("javascript_udf")
        return typing.cast(typing.Optional["PubsubTopicMessageTransformsJavascriptUdf"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubTopicMessageTransforms(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicMessageTransformsJavascriptUdf",
    jsii_struct_bases=[],
    name_mapping={"code": "code", "function_name": "functionName"},
)
class PubsubTopicMessageTransformsJavascriptUdf:
    def __init__(self, *, code: builtins.str, function_name: builtins.str) -> None:
        '''
        :param code: JavaScript code that contains a function 'function_name' with the following signature: ``` /** * Transforms a Pub/Sub message. - -
        :param function_name: Name of the JavaScript function that should be applied to Pub/Sub messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#function_name PubsubTopic#function_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8231b90ea7012a6c3fa72f6a466c3d873d529772ffe9954d494dfbaba4c1d405)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#function_name PubsubTopic#function_name}
        '''
        result = self._values.get("function_name")
        assert result is not None, "Required property 'function_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubTopicMessageTransformsJavascriptUdf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubTopicMessageTransformsJavascriptUdfOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicMessageTransformsJavascriptUdfOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2017c9e61471754c8e70477b6b16ef0ee4b0cc4c6a4a09644c536eb71a409edb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cde5ef7c6ee8e7863b8bd767c9ba8da20da5cc8a349856b394fdf8acadbde714)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "code", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionName"))

    @function_name.setter
    def function_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5cd82a31f5f736c4569cc0383df7a14bdd6fe666ad830b55ad569991c726a40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PubsubTopicMessageTransformsJavascriptUdf]:
        return typing.cast(typing.Optional[PubsubTopicMessageTransformsJavascriptUdf], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubTopicMessageTransformsJavascriptUdf],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c438d192eaf38b2bfdd1e24d55b72dcbe6d6163e37e4f85de95d208b71241195)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PubsubTopicMessageTransformsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicMessageTransformsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe61c7b97a10e88e9f29c084622424474bb02ae121e623a870830d5d435361e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "PubsubTopicMessageTransformsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__672eee35aa648cd18e1874e804d73a112798c4e89282400b3eaf436fa0f96b24)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PubsubTopicMessageTransformsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6bbf9e96d65bc06faa8c8c6c34560a1bd12cbec07472f2e2f19140fecc1da95)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e54e9eccd448c5dc06b4408675a6d1bc2fcbb43f37d9f5f27f1bbce258814c29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9a17c0e735fed46e8ea4cf950b17fc25a7274b1dd6fe6d51c8dc41c5fb0328c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PubsubTopicMessageTransforms]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PubsubTopicMessageTransforms]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PubsubTopicMessageTransforms]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c065f562d27e2d6727be1c8b625b8102ceeef79de0f2112d99867c68f286934d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PubsubTopicMessageTransformsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicMessageTransformsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a5ca2b87eac7c380fdbf6d07500e416dbb49b2680181d1c4bf405ac2bf50ab0)
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
        :param function_name: Name of the JavaScript function that should be applied to Pub/Sub messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#function_name PubsubTopic#function_name}
        '''
        value = PubsubTopicMessageTransformsJavascriptUdf(
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
    ) -> PubsubTopicMessageTransformsJavascriptUdfOutputReference:
        return typing.cast(PubsubTopicMessageTransformsJavascriptUdfOutputReference, jsii.get(self, "javascriptUdf"))

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
    ) -> typing.Optional[PubsubTopicMessageTransformsJavascriptUdf]:
        return typing.cast(typing.Optional[PubsubTopicMessageTransformsJavascriptUdf], jsii.get(self, "javascriptUdfInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__981118d14b68aca56a4ebf4723fe61230a613db275fd57555e9643755cebdb4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PubsubTopicMessageTransforms]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PubsubTopicMessageTransforms]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PubsubTopicMessageTransforms]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a46378ed226a8f67a0224e3455e088e52944cac16a409c8c97408026b971aa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicSchemaSettings",
    jsii_struct_bases=[],
    name_mapping={"schema": "schema", "encoding": "encoding"},
)
class PubsubTopicSchemaSettings:
    def __init__(
        self,
        *,
        schema: builtins.str,
        encoding: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema: The name of the schema that messages published should be validated against. Format is projects/{project}/schemas/{schema}. The value of this field will be *deleted-schema* if the schema has been deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#schema PubsubTopic#schema}
        :param encoding: The encoding of messages validated against schema. Default value: "ENCODING_UNSPECIFIED" Possible values: ["ENCODING_UNSPECIFIED", "JSON", "BINARY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#encoding PubsubTopic#encoding}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__688c60bd4a7eac17eabc2fbfa16f0fbb5bd8cf9a5eeb311d7f911b577debd93a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#schema PubsubTopic#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encoding(self) -> typing.Optional[builtins.str]:
        '''The encoding of messages validated against schema. Default value: "ENCODING_UNSPECIFIED" Possible values: ["ENCODING_UNSPECIFIED", "JSON", "BINARY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#encoding PubsubTopic#encoding}
        '''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubTopicSchemaSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubTopicSchemaSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicSchemaSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2ba838f7e143f2ce85002fb07ef305cfdc0b252af6302fc2f07a237f9a6a868)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bf208997aee70d91121f52f0546f65f04d1733aaee3dd5edd77c95eb6f80297)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad4cf19c64f9f5a2cc5e6572afbbe25fd29db80e88ec76c91ef9cca648ade2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PubsubTopicSchemaSettings]:
        return typing.cast(typing.Optional[PubsubTopicSchemaSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[PubsubTopicSchemaSettings]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a56f71f472215be2df8a22e29d58e81820b28751dfa86ac32ac6690e452e46a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class PubsubTopicTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#create PubsubTopic#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#delete PubsubTopic#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#update PubsubTopic#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feb0c463d37c538826397283298ff29190717e9fada957e9e1faf70b79274c3f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#create PubsubTopic#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#delete PubsubTopic#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_topic#update PubsubTopic#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubTopicTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubTopicTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubTopic.PubsubTopicTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f462a37f5f3530f3b98cbe5748a1b8314b07ade5f07cd65cd77ef00bc624682)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6d4ededbd1e53c5c8ed08bc388f0ea9b8292ce6b1136e396fe1c33f0af5b294)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee84026f30a62e95f92a080e8b9178cda033b4c4a98135d15786eff5e256de30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c9e0383ddbbe272d5c329a61bcdc4f57bc3b2f10d13295f429b39516e32fd0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PubsubTopicTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PubsubTopicTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PubsubTopicTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8d02f18ed9c90412f41970bde516c1b007ce7e6c723d8eaed7c87f5b9ce5cac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "PubsubTopic",
    "PubsubTopicConfig",
    "PubsubTopicIngestionDataSourceSettings",
    "PubsubTopicIngestionDataSourceSettingsAwsKinesis",
    "PubsubTopicIngestionDataSourceSettingsAwsKinesisOutputReference",
    "PubsubTopicIngestionDataSourceSettingsAwsMsk",
    "PubsubTopicIngestionDataSourceSettingsAwsMskOutputReference",
    "PubsubTopicIngestionDataSourceSettingsAzureEventHubs",
    "PubsubTopicIngestionDataSourceSettingsAzureEventHubsOutputReference",
    "PubsubTopicIngestionDataSourceSettingsCloudStorage",
    "PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat",
    "PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormatOutputReference",
    "PubsubTopicIngestionDataSourceSettingsCloudStorageOutputReference",
    "PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat",
    "PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormatOutputReference",
    "PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat",
    "PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormatOutputReference",
    "PubsubTopicIngestionDataSourceSettingsConfluentCloud",
    "PubsubTopicIngestionDataSourceSettingsConfluentCloudOutputReference",
    "PubsubTopicIngestionDataSourceSettingsOutputReference",
    "PubsubTopicIngestionDataSourceSettingsPlatformLogsSettings",
    "PubsubTopicIngestionDataSourceSettingsPlatformLogsSettingsOutputReference",
    "PubsubTopicMessageStoragePolicy",
    "PubsubTopicMessageStoragePolicyOutputReference",
    "PubsubTopicMessageTransforms",
    "PubsubTopicMessageTransformsJavascriptUdf",
    "PubsubTopicMessageTransformsJavascriptUdfOutputReference",
    "PubsubTopicMessageTransformsList",
    "PubsubTopicMessageTransformsOutputReference",
    "PubsubTopicSchemaSettings",
    "PubsubTopicSchemaSettingsOutputReference",
    "PubsubTopicTimeouts",
    "PubsubTopicTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__25a4b255d477dbb29368b5c62db08af517f7c9e151c7e77fc3a8e34accf0c08e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    ingestion_data_source_settings: typing.Optional[typing.Union[PubsubTopicIngestionDataSourceSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    message_retention_duration: typing.Optional[builtins.str] = None,
    message_storage_policy: typing.Optional[typing.Union[PubsubTopicMessageStoragePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    message_transforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PubsubTopicMessageTransforms, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    schema_settings: typing.Optional[typing.Union[PubsubTopicSchemaSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[PubsubTopicTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__09054ad2222523bdb5dececfb3440b992705e3a3e3b98cd7c7320b0859416cc3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__009c6fd9469867de50acfe181dab89c198666c8beed63e0afeac165d426cc579(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PubsubTopicMessageTransforms, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2abdd4060b24e09d6fe6987af1ef086218c13e76e6148c811b23e4cff5717b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72fa7672aa566e24bb50cc77bd00c52ed89ea9a32d4f04bd4635285dd0ce0ec9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d640dad8d18a35de9fd46eb8ff52061da45580e290693e6d70928154a8cc976(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7846927d9bac7c315033c3ec696d98704d1262d2df818972b2adc3bc038b7da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c5564edf73340c51e04e6bb5c1d832c82e8f14f34f336cbf07a3c202c6045b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a62f0b65d89a68e9236ee4658b90b8948917dc78ad6a00588e5810bd19b180e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327caa8e14d39eec3aad85ca2d4b60b93037ee83beffe48d7c74526cd948e637(
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
    ingestion_data_source_settings: typing.Optional[typing.Union[PubsubTopicIngestionDataSourceSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    message_retention_duration: typing.Optional[builtins.str] = None,
    message_storage_policy: typing.Optional[typing.Union[PubsubTopicMessageStoragePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    message_transforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PubsubTopicMessageTransforms, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    schema_settings: typing.Optional[typing.Union[PubsubTopicSchemaSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[PubsubTopicTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d9d45b87cbabc5222b58e0cd90c1b1add270f6285f7fe74f61306c52fb2fcc(
    *,
    aws_kinesis: typing.Optional[typing.Union[PubsubTopicIngestionDataSourceSettingsAwsKinesis, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_msk: typing.Optional[typing.Union[PubsubTopicIngestionDataSourceSettingsAwsMsk, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_event_hubs: typing.Optional[typing.Union[PubsubTopicIngestionDataSourceSettingsAzureEventHubs, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_storage: typing.Optional[typing.Union[PubsubTopicIngestionDataSourceSettingsCloudStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    confluent_cloud: typing.Optional[typing.Union[PubsubTopicIngestionDataSourceSettingsConfluentCloud, typing.Dict[builtins.str, typing.Any]]] = None,
    platform_logs_settings: typing.Optional[typing.Union[PubsubTopicIngestionDataSourceSettingsPlatformLogsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f19aa50a07dc992a8fa3377e488bc230ce92fe9d073d6dd3a814b2851136fa(
    *,
    aws_role_arn: builtins.str,
    consumer_arn: builtins.str,
    gcp_service_account: builtins.str,
    stream_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c4f4b130d9c6a378c7726330ca83cbc21a8303cea2e9c33a4b02f43ee2400ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c7bd10f0756c84c70114e2323ddf5c6580c4e711343c7a2bfb0f178b2037b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fbca0712d33d531a2215485d18f59bf5943387c20c73e538416a44976c3bcb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f027732ecaad38982f80c1164ba7ee61373d5d26d2cd95b7cf700ef2df1cb53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b4a3ff64843cff9d737b46b7b04251a1dc7b6f50418b71141807dcd1e9711b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5987bcb292b1be9f872a40a66dacd9827949cfd6ab87acf5247d998175b917d0(
    value: typing.Optional[PubsubTopicIngestionDataSourceSettingsAwsKinesis],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eefd0227008352a9df18c2573584a05e1a8ad677a343426f04f515015b5ab4a(
    *,
    aws_role_arn: builtins.str,
    cluster_arn: builtins.str,
    gcp_service_account: builtins.str,
    topic: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a8e35ca7449e565dd03251926fb73d209615ccbee0fb18a6c335749a0b6668(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ac52365428b7cd770e23cd6dd1b633151fa17a377b6c182d0e312a87048a250(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088ac5c3e5651443f5e0e72be8557d216a8687d576649ca6fc8ac5f9764710b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4de7a9a8e2cf658364b74cd272983ee95d80ce8d694b76555e45779eeac08ddd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b235f176bb43d88d993afb8ac92c440694b04b346bd1f60635ca23fbb2e5a41e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd670e2fd6c5a8405b1631a7365aa7b8f3053036153217c3ba6bec85949889a9(
    value: typing.Optional[PubsubTopicIngestionDataSourceSettingsAwsMsk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4de7d74087af1aaff78a5f2ec132051092de1f130885df3c3c855e91cf18eea7(
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

def _typecheckingstub__55121a4db7e09816e0d43b58c6e2700d0968fbfe85e55ab2042419ea9fa078ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5edb45de7c4dfd7d4be842aa3a7af780ae5f3d75fb829af57c86b3913d3812c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9582df58f80312028de90358da9713a43e01b21d175b453c4cc4f9c746a4f531(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d0af5fefd656eea383c4277576167cd519c76383bf9966deb9bab3e6163f73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2296100119afe62be4f54a478f03aa99f7d5e3b7d77fae50dc885daf7eb8c947(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7533d17a4ac581dc9850ee20ee8f8dd481fad547f40d522a6399a5826405f0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8353b21087564d1e18827a73388932390bf909cf178ce2c262ab28f2faf783(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32fb6bba2320f271c16cf26593991dc33db2f0af3ddf140357f88de9b369271(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cab08234dbe4f04ad7fa3517666c3d21bd94c37bdea12baddf87ce1234ccfa6(
    value: typing.Optional[PubsubTopicIngestionDataSourceSettingsAzureEventHubs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6f2095ffb540c6325805d0e96c566e23b27e504378db5a644f558683b9b5cd8(
    *,
    bucket: builtins.str,
    avro_format: typing.Optional[typing.Union[PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat, typing.Dict[builtins.str, typing.Any]]] = None,
    match_glob: typing.Optional[builtins.str] = None,
    minimum_object_create_time: typing.Optional[builtins.str] = None,
    pubsub_avro_format: typing.Optional[typing.Union[PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat, typing.Dict[builtins.str, typing.Any]]] = None,
    text_format: typing.Optional[typing.Union[PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbaa4b697ed94ce14cacf4b44ffe1928921e9feb96a8d49e71db4e56d02d412c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65085a207885ad8533e88b49f4f50ca289398a2bc0be813e4e7e4aa24627af33(
    value: typing.Optional[PubsubTopicIngestionDataSourceSettingsCloudStorageAvroFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2139f5fdeb4301085d72c2bafd044545df841af9af8456e50f1d24b8eba0ac88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3771ceed42005f70e18cac3cb7ec2164fc7312ef21ee52fe2944b33ce458cebf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc34fc712776511881dbcc0bf582dc863d0363041727fcb7b3b2debdbeb7cf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fdba0b5077e9861fb9661ba8d5eab92607bc66480a82fd275af8731c302f5de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66353aed15741b44dbc97816de3386ab719e2e8915f65fa6077cc2337f47eed8(
    value: typing.Optional[PubsubTopicIngestionDataSourceSettingsCloudStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c4978f0ed965c7961cf5a6a0ee33824d100a6af52e48bd7e34db441bcee766(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36fb6c8ed58d476ae57f727d4325abdfc11a31970c1dc353b7b7e71c34e8cae9(
    value: typing.Optional[PubsubTopicIngestionDataSourceSettingsCloudStoragePubsubAvroFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f40583c2140ff95e6741181becced4820725dde9fc0a2a4aab0c86f973369128(
    *,
    delimiter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7924a47106fa6b618e2d748b7fc14adeda3a068cb56c947a13c831597b17b65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb2c87c685a497473bb9a218ec37651f2765a37238e8951fa7bf1a674e96bab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab196b203e31d00bb20d9fd1800ce86867f415697ed15dfdb999f1904a9c8455(
    value: typing.Optional[PubsubTopicIngestionDataSourceSettingsCloudStorageTextFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436fd1bcf6e13adb53578bdd2dbbe284ae9022702779a2a82ff7f827dd753241(
    *,
    bootstrap_server: builtins.str,
    gcp_service_account: builtins.str,
    identity_pool_id: builtins.str,
    topic: builtins.str,
    cluster_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a84427e1cf1e0b4b55d5ae77a8b362f2549e1059f35b4f8fb379f7e4544991(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5243f82c55e32a5dd5b375ca8360a659a7ac9b9c1d49ec3c587fa3f575b067a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb36d8dab4b7d687746187f42f082c46daec50ea21fa1388dc6ea7c69c97699e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__841f74e13e1851d46272f5295d41e218a07895c6bf80be306124f6b910a34c2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e822af20548e30763a6f3c4338f1819d7db798f95ef253e5cdcf365c60a8c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14142b42939eeeb400f250d2730eabd81b443cac16d82967713718b00659b591(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3229fcc4b49ffa233cee1ef38ea6ef020731d513e588be474bc32f07cb4ffdb2(
    value: typing.Optional[PubsubTopicIngestionDataSourceSettingsConfluentCloud],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef87ae3a12aa844f761dea9cf7f7e7d1efb44928a928d1ebf3c7d2d7a0db889(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30458bbc60049d915278766f842640fcd614231a678e7d454d8cccd0cc6af8ac(
    value: typing.Optional[PubsubTopicIngestionDataSourceSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87daa3461a23c77188c9ce9b57663af7d34365f42bbedc26ad2bd0eb9285ef45(
    *,
    severity: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bab23d2024dafe3cd2d26154a4492f206e86825100e5f290eb0911eb3d2f58f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b9781dfe486731293563f41baf92b68af2b83b77c1f9195a403bb6df80d92fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb4927ad0a0c3c017be8dde3dac0c82c38c239602c1f9e180bf30e96ec188bc9(
    value: typing.Optional[PubsubTopicIngestionDataSourceSettingsPlatformLogsSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7acfce2f26378d4dd851ee8b921b9a42a96b61fda75583caa51f0fc5ead3c5c6(
    *,
    allowed_persistence_regions: typing.Sequence[builtins.str],
    enforce_in_transit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee36bc0e41749624d550b0b4ffbf1bd0479949d160a28978f13cbf9d0832daa8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd47e18688f01a4de33db3cda5cc7cf2368d074fc724ab4ad0454fa06670b1ab(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8af2631b2bc47640d88bc8a7a6917d98272a2215e61913b71ddc6aee9a27827b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada06454be42e6f402f600fd28a01f0dd64720bf1a633a76b7df309f85f4b039(
    value: typing.Optional[PubsubTopicMessageStoragePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607d7fb70cc745bfcfe96633eb9673a3aedd7a595a04d9a0bf51bf20f69da497(
    *,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    javascript_udf: typing.Optional[typing.Union[PubsubTopicMessageTransformsJavascriptUdf, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8231b90ea7012a6c3fa72f6a466c3d873d529772ffe9954d494dfbaba4c1d405(
    *,
    code: builtins.str,
    function_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2017c9e61471754c8e70477b6b16ef0ee4b0cc4c6a4a09644c536eb71a409edb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde5ef7c6ee8e7863b8bd767c9ba8da20da5cc8a349856b394fdf8acadbde714(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5cd82a31f5f736c4569cc0383df7a14bdd6fe666ad830b55ad569991c726a40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c438d192eaf38b2bfdd1e24d55b72dcbe6d6163e37e4f85de95d208b71241195(
    value: typing.Optional[PubsubTopicMessageTransformsJavascriptUdf],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe61c7b97a10e88e9f29c084622424474bb02ae121e623a870830d5d435361e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__672eee35aa648cd18e1874e804d73a112798c4e89282400b3eaf436fa0f96b24(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6bbf9e96d65bc06faa8c8c6c34560a1bd12cbec07472f2e2f19140fecc1da95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e54e9eccd448c5dc06b4408675a6d1bc2fcbb43f37d9f5f27f1bbce258814c29(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a17c0e735fed46e8ea4cf950b17fc25a7274b1dd6fe6d51c8dc41c5fb0328c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c065f562d27e2d6727be1c8b625b8102ceeef79de0f2112d99867c68f286934d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PubsubTopicMessageTransforms]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5ca2b87eac7c380fdbf6d07500e416dbb49b2680181d1c4bf405ac2bf50ab0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__981118d14b68aca56a4ebf4723fe61230a613db275fd57555e9643755cebdb4a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a46378ed226a8f67a0224e3455e088e52944cac16a409c8c97408026b971aa0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PubsubTopicMessageTransforms]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__688c60bd4a7eac17eabc2fbfa16f0fbb5bd8cf9a5eeb311d7f911b577debd93a(
    *,
    schema: builtins.str,
    encoding: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2ba838f7e143f2ce85002fb07ef305cfdc0b252af6302fc2f07a237f9a6a868(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bf208997aee70d91121f52f0546f65f04d1733aaee3dd5edd77c95eb6f80297(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad4cf19c64f9f5a2cc5e6572afbbe25fd29db80e88ec76c91ef9cca648ade2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a56f71f472215be2df8a22e29d58e81820b28751dfa86ac32ac6690e452e46a(
    value: typing.Optional[PubsubTopicSchemaSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb0c463d37c538826397283298ff29190717e9fada957e9e1faf70b79274c3f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f462a37f5f3530f3b98cbe5748a1b8314b07ade5f07cd65cd77ef00bc624682(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d4ededbd1e53c5c8ed08bc388f0ea9b8292ce6b1136e396fe1c33f0af5b294(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee84026f30a62e95f92a080e8b9178cda033b4c4a98135d15786eff5e256de30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9e0383ddbbe272d5c329a61bcdc4f57bc3b2f10d13295f429b39516e32fd0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8d02f18ed9c90412f41970bde516c1b007ce7e6c723d8eaed7c87f5b9ce5cac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PubsubTopicTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
