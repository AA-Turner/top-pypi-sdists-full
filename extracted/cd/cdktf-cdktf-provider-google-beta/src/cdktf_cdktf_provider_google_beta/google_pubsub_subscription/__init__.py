r'''
# `google_pubsub_subscription`

Refer to the Terraform Registry for docs: [`google_pubsub_subscription`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription).
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


class GooglePubsubSubscription(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscription",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription google_pubsub_subscription}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        topic: builtins.str,
        ack_deadline_seconds: typing.Optional[jsii.Number] = None,
        bigquery_config: typing.Optional[typing.Union["GooglePubsubSubscriptionBigqueryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_storage_config: typing.Optional[typing.Union["GooglePubsubSubscriptionCloudStorageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_policy: typing.Optional[typing.Union["GooglePubsubSubscriptionDeadLetterPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_exactly_once_delivery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_message_ordering: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expiration_policy: typing.Optional[typing.Union["GooglePubsubSubscriptionExpirationPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        filter: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        message_retention_duration: typing.Optional[builtins.str] = None,
        message_transforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GooglePubsubSubscriptionMessageTransforms", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        push_config: typing.Optional[typing.Union["GooglePubsubSubscriptionPushConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        retain_acked_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retry_policy: typing.Optional[typing.Union["GooglePubsubSubscriptionRetryPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GooglePubsubSubscriptionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription google_pubsub_subscription} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the subscription. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#name GooglePubsubSubscription#name}
        :param topic: A reference to a Topic resource, of the form projects/{project}/topics/{{name}} (as in the id property of a google_pubsub_topic), or just a topic name if the topic is in the same project as the subscription. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#topic GooglePubsubSubscription#topic}
        :param ack_deadline_seconds: This value is the maximum time after a subscriber receives a message before the subscriber should acknowledge the message. After message delivery but before the ack deadline expires and before the message is acknowledged, it is an outstanding message and will not be delivered again during that time (on a best-effort basis). For pull subscriptions, this value is used as the initial value for the ack deadline. To override this value for a given message, call subscriptions.modifyAckDeadline with the corresponding ackId if using pull. The minimum custom deadline you can specify is 10 seconds. The maximum custom deadline you can specify is 600 seconds (10 minutes). If this parameter is 0, a default value of 10 seconds is used. For push delivery, this value is also used to set the request timeout for the call to the push endpoint. If the subscriber never acknowledges the message, the Pub/Sub system will eventually redeliver the message. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#ack_deadline_seconds GooglePubsubSubscription#ack_deadline_seconds}
        :param bigquery_config: bigquery_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#bigquery_config GooglePubsubSubscription#bigquery_config}
        :param cloud_storage_config: cloud_storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#cloud_storage_config GooglePubsubSubscription#cloud_storage_config}
        :param dead_letter_policy: dead_letter_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#dead_letter_policy GooglePubsubSubscription#dead_letter_policy}
        :param enable_exactly_once_delivery: If 'true', Pub/Sub provides the following guarantees for the delivery of a message with a given value of messageId on this Subscriptions': - The message sent to a subscriber is guaranteed not to be resent before the message's acknowledgement deadline expires. - An acknowledged message will not be resent to a subscriber. Note that subscribers may still receive multiple copies of a message when 'enable_exactly_once_delivery' is true if the message was published multiple times by a publisher client. These copies are considered distinct by Pub/Sub and have distinct messageId values Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#enable_exactly_once_delivery GooglePubsubSubscription#enable_exactly_once_delivery}
        :param enable_message_ordering: If 'true', messages published with the same orderingKey in PubsubMessage will be delivered to the subscribers in the order in which they are received by the Pub/Sub system. Otherwise, they may be delivered in any order. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#enable_message_ordering GooglePubsubSubscription#enable_message_ordering}
        :param expiration_policy: expiration_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#expiration_policy GooglePubsubSubscription#expiration_policy}
        :param filter: The subscription only delivers the messages that match the filter. Pub/Sub automatically acknowledges the messages that don't match the filter. You can filter messages by their attributes. The maximum length of a filter is 256 bytes. After creating the subscription, you can't modify the filter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#filter GooglePubsubSubscription#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#id GooglePubsubSubscription#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A set of key/value label pairs to assign to this Subscription. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#labels GooglePubsubSubscription#labels}
        :param message_retention_duration: How long to retain unacknowledged messages in the subscription's backlog, from the moment a message is published. If retain_acked_messages is true, then this also configures the retention of acknowledged messages, and thus configures how far back in time a subscriptions.seek can be done. Defaults to 7 days. Cannot be more than 31 days ('"2678400s"') or less than 10 minutes ('"600s"'). A duration in seconds with up to nine fractional digits, terminated by 's'. Example: '"600.5s"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#message_retention_duration GooglePubsubSubscription#message_retention_duration}
        :param message_transforms: message_transforms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#message_transforms GooglePubsubSubscription#message_transforms}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#project GooglePubsubSubscription#project}.
        :param push_config: push_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#push_config GooglePubsubSubscription#push_config}
        :param retain_acked_messages: Indicates whether to retain acknowledged messages. If 'true', then messages are not expunged from the subscription's backlog, even if they are acknowledged, until they fall out of the messageRetentionDuration window. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#retain_acked_messages GooglePubsubSubscription#retain_acked_messages}
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#retry_policy GooglePubsubSubscription#retry_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#timeouts GooglePubsubSubscription#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8e5e2e5996576cf888dc1e67c3f99fdb31177100884f076ee3e2cbc93c3d606)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GooglePubsubSubscriptionConfig(
            name=name,
            topic=topic,
            ack_deadline_seconds=ack_deadline_seconds,
            bigquery_config=bigquery_config,
            cloud_storage_config=cloud_storage_config,
            dead_letter_policy=dead_letter_policy,
            enable_exactly_once_delivery=enable_exactly_once_delivery,
            enable_message_ordering=enable_message_ordering,
            expiration_policy=expiration_policy,
            filter=filter,
            id=id,
            labels=labels,
            message_retention_duration=message_retention_duration,
            message_transforms=message_transforms,
            project=project,
            push_config=push_config,
            retain_acked_messages=retain_acked_messages,
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
        '''Generates CDKTF code for importing a GooglePubsubSubscription resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GooglePubsubSubscription to import.
        :param import_from_id: The id of the existing GooglePubsubSubscription that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GooglePubsubSubscription to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6800ad8af1f13d3ff7a8363d0fa11a9a2435952b06eedc89eb8d67f50255edbd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBigqueryConfig")
    def put_bigquery_config(
        self,
        *,
        table: builtins.str,
        drop_unknown_fields: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        service_account_email: typing.Optional[builtins.str] = None,
        use_table_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_topic_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        write_metadata: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param table: The name of the table to which to write data, of the form {projectId}.{datasetId}.{tableId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#table GooglePubsubSubscription#table}
        :param drop_unknown_fields: When true and use_topic_schema or use_table_schema is true, any fields that are a part of the topic schema or message schema that are not part of the BigQuery table schema are dropped when writing to BigQuery. Otherwise, the schemas must be kept in sync and any messages with extra fields are not written and remain in the subscription's backlog. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#drop_unknown_fields GooglePubsubSubscription#drop_unknown_fields}
        :param service_account_email: The service account to use to write to BigQuery. If not specified, the Pub/Sub `service agent <https://cloud.google.com/iam/docs/service-agents>`_, service-{project_number}@gcp-sa-pubsub.iam.gserviceaccount.com, is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#service_account_email GooglePubsubSubscription#service_account_email}
        :param use_table_schema: When true, use the BigQuery table's schema as the columns to write to in BigQuery. Messages must be published in JSON format. Only one of use_topic_schema and use_table_schema can be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#use_table_schema GooglePubsubSubscription#use_table_schema}
        :param use_topic_schema: When true, use the topic's schema as the columns to write to in BigQuery, if it exists. Only one of use_topic_schema and use_table_schema can be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#use_topic_schema GooglePubsubSubscription#use_topic_schema}
        :param write_metadata: When true, write the subscription name, messageId, publishTime, attributes, and orderingKey to additional columns in the table. The subscription name, messageId, and publishTime fields are put in their own columns while all other message properties (other than data) are written to a JSON object in the attributes column. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#write_metadata GooglePubsubSubscription#write_metadata}
        '''
        value = GooglePubsubSubscriptionBigqueryConfig(
            table=table,
            drop_unknown_fields=drop_unknown_fields,
            service_account_email=service_account_email,
            use_table_schema=use_table_schema,
            use_topic_schema=use_topic_schema,
            write_metadata=write_metadata,
        )

        return typing.cast(None, jsii.invoke(self, "putBigqueryConfig", [value]))

    @jsii.member(jsii_name="putCloudStorageConfig")
    def put_cloud_storage_config(
        self,
        *,
        bucket: builtins.str,
        avro_config: typing.Optional[typing.Union["GooglePubsubSubscriptionCloudStorageConfigAvroConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        filename_datetime_format: typing.Optional[builtins.str] = None,
        filename_prefix: typing.Optional[builtins.str] = None,
        filename_suffix: typing.Optional[builtins.str] = None,
        max_bytes: typing.Optional[jsii.Number] = None,
        max_duration: typing.Optional[builtins.str] = None,
        max_messages: typing.Optional[jsii.Number] = None,
        service_account_email: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: User-provided name for the Cloud Storage bucket. The bucket must be created by the user. The bucket name must be without any prefix like "gs://". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#bucket GooglePubsubSubscription#bucket}
        :param avro_config: avro_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#avro_config GooglePubsubSubscription#avro_config}
        :param filename_datetime_format: User-provided format string specifying how to represent datetimes in Cloud Storage filenames. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#filename_datetime_format GooglePubsubSubscription#filename_datetime_format}
        :param filename_prefix: User-provided prefix for Cloud Storage filename. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#filename_prefix GooglePubsubSubscription#filename_prefix}
        :param filename_suffix: User-provided suffix for Cloud Storage filename. Must not end in "/". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#filename_suffix GooglePubsubSubscription#filename_suffix}
        :param max_bytes: The maximum bytes that can be written to a Cloud Storage file before a new file is created. Min 1 KB, max 10 GiB. The maxBytes limit may be exceeded in cases where messages are larger than the limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#max_bytes GooglePubsubSubscription#max_bytes}
        :param max_duration: The maximum duration that can elapse before a new Cloud Storage file is created. Min 1 minute, max 10 minutes, default 5 minutes. May not exceed the subscription's acknowledgement deadline. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#max_duration GooglePubsubSubscription#max_duration}
        :param max_messages: The maximum messages that can be written to a Cloud Storage file before a new file is created. Min 1000 messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#max_messages GooglePubsubSubscription#max_messages}
        :param service_account_email: The service account to use to write to Cloud Storage. If not specified, the Pub/Sub `service agent <https://cloud.google.com/iam/docs/service-agents>`_, service-{project_number}@gcp-sa-pubsub.iam.gserviceaccount.com, is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#service_account_email GooglePubsubSubscription#service_account_email}
        '''
        value = GooglePubsubSubscriptionCloudStorageConfig(
            bucket=bucket,
            avro_config=avro_config,
            filename_datetime_format=filename_datetime_format,
            filename_prefix=filename_prefix,
            filename_suffix=filename_suffix,
            max_bytes=max_bytes,
            max_duration=max_duration,
            max_messages=max_messages,
            service_account_email=service_account_email,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudStorageConfig", [value]))

    @jsii.member(jsii_name="putDeadLetterPolicy")
    def put_dead_letter_policy(
        self,
        *,
        dead_letter_topic: typing.Optional[builtins.str] = None,
        max_delivery_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param dead_letter_topic: The name of the topic to which dead letter messages should be published. Format is 'projects/{project}/topics/{topic}'. The Cloud Pub/Sub service account associated with the enclosing subscription's parent project (i.e., service-{project_number}@gcp-sa-pubsub.iam.gserviceaccount.com) must have permission to Publish() to this topic. The operation will fail if the topic does not exist. Users should ensure that there is a subscription attached to this topic since messages published to a topic with no subscriptions are lost. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#dead_letter_topic GooglePubsubSubscription#dead_letter_topic}
        :param max_delivery_attempts: The maximum number of delivery attempts for any message. The value must be between 5 and 100. The number of delivery attempts is defined as 1 + (the sum of number of NACKs and number of times the acknowledgement deadline has been exceeded for the message). A NACK is any call to ModifyAckDeadline with a 0 deadline. Note that client libraries may automatically extend ack_deadlines. This field will be honored on a best effort basis. If this parameter is 0, a default value of 5 is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#max_delivery_attempts GooglePubsubSubscription#max_delivery_attempts}
        '''
        value = GooglePubsubSubscriptionDeadLetterPolicy(
            dead_letter_topic=dead_letter_topic,
            max_delivery_attempts=max_delivery_attempts,
        )

        return typing.cast(None, jsii.invoke(self, "putDeadLetterPolicy", [value]))

    @jsii.member(jsii_name="putExpirationPolicy")
    def put_expiration_policy(self, *, ttl: builtins.str) -> None:
        '''
        :param ttl: Specifies the "time-to-live" duration for an associated resource. The resource expires if it is not active for a period of ttl. If ttl is set to "", the associated resource never expires. A duration in seconds with up to nine fractional digits, terminated by 's'. Example - "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#ttl GooglePubsubSubscription#ttl}
        '''
        value = GooglePubsubSubscriptionExpirationPolicy(ttl=ttl)

        return typing.cast(None, jsii.invoke(self, "putExpirationPolicy", [value]))

    @jsii.member(jsii_name="putMessageTransforms")
    def put_message_transforms(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GooglePubsubSubscriptionMessageTransforms", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ddd90af02373bc0e3ef84e2695a29996458cf383e85e3134c1af50a10583c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMessageTransforms", [value]))

    @jsii.member(jsii_name="putPushConfig")
    def put_push_config(
        self,
        *,
        push_endpoint: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        no_wrapper: typing.Optional[typing.Union["GooglePubsubSubscriptionPushConfigNoWrapper", typing.Dict[builtins.str, typing.Any]]] = None,
        oidc_token: typing.Optional[typing.Union["GooglePubsubSubscriptionPushConfigOidcToken", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param push_endpoint: A URL locating the endpoint to which messages should be pushed. For example, a Webhook endpoint might use "https://example.com/push". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#push_endpoint GooglePubsubSubscription#push_endpoint}
        :param attributes: Endpoint configuration attributes. Every endpoint has a set of API supported attributes that can be used to control different aspects of the message delivery. The currently supported attribute is x-goog-version, which you can use to change the format of the pushed message. This attribute indicates the version of the data expected by the endpoint. This controls the shape of the pushed message (i.e., its fields and metadata). The endpoint version is based on the version of the Pub/Sub API. If not present during the subscriptions.create call, it will default to the version of the API used to make such call. If not present during a subscriptions.modifyPushConfig call, its value will not be changed. subscriptions.get calls will always return a valid version, even if the subscription was created without this attribute. The possible values for this attribute are: - v1beta1: uses the push format defined in the v1beta1 Pub/Sub API. - v1 or v1beta2: uses the push format defined in the v1 Pub/Sub API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#attributes GooglePubsubSubscription#attributes}
        :param no_wrapper: no_wrapper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#no_wrapper GooglePubsubSubscription#no_wrapper}
        :param oidc_token: oidc_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#oidc_token GooglePubsubSubscription#oidc_token}
        '''
        value = GooglePubsubSubscriptionPushConfig(
            push_endpoint=push_endpoint,
            attributes=attributes,
            no_wrapper=no_wrapper,
            oidc_token=oidc_token,
        )

        return typing.cast(None, jsii.invoke(self, "putPushConfig", [value]))

    @jsii.member(jsii_name="putRetryPolicy")
    def put_retry_policy(
        self,
        *,
        maximum_backoff: typing.Optional[builtins.str] = None,
        minimum_backoff: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param maximum_backoff: The maximum delay between consecutive deliveries of a given message. Value should be between 0 and 600 seconds. Defaults to 600 seconds. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#maximum_backoff GooglePubsubSubscription#maximum_backoff}
        :param minimum_backoff: The minimum delay between consecutive deliveries of a given message. Value should be between 0 and 600 seconds. Defaults to 10 seconds. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#minimum_backoff GooglePubsubSubscription#minimum_backoff}
        '''
        value = GooglePubsubSubscriptionRetryPolicy(
            maximum_backoff=maximum_backoff, minimum_backoff=minimum_backoff
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#create GooglePubsubSubscription#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#delete GooglePubsubSubscription#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#update GooglePubsubSubscription#update}.
        '''
        value = GooglePubsubSubscriptionTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAckDeadlineSeconds")
    def reset_ack_deadline_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAckDeadlineSeconds", []))

    @jsii.member(jsii_name="resetBigqueryConfig")
    def reset_bigquery_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigqueryConfig", []))

    @jsii.member(jsii_name="resetCloudStorageConfig")
    def reset_cloud_storage_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudStorageConfig", []))

    @jsii.member(jsii_name="resetDeadLetterPolicy")
    def reset_dead_letter_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeadLetterPolicy", []))

    @jsii.member(jsii_name="resetEnableExactlyOnceDelivery")
    def reset_enable_exactly_once_delivery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableExactlyOnceDelivery", []))

    @jsii.member(jsii_name="resetEnableMessageOrdering")
    def reset_enable_message_ordering(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableMessageOrdering", []))

    @jsii.member(jsii_name="resetExpirationPolicy")
    def reset_expiration_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationPolicy", []))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMessageRetentionDuration")
    def reset_message_retention_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageRetentionDuration", []))

    @jsii.member(jsii_name="resetMessageTransforms")
    def reset_message_transforms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageTransforms", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPushConfig")
    def reset_push_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPushConfig", []))

    @jsii.member(jsii_name="resetRetainAckedMessages")
    def reset_retain_acked_messages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetainAckedMessages", []))

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
    @jsii.member(jsii_name="bigqueryConfig")
    def bigquery_config(
        self,
    ) -> "GooglePubsubSubscriptionBigqueryConfigOutputReference":
        return typing.cast("GooglePubsubSubscriptionBigqueryConfigOutputReference", jsii.get(self, "bigqueryConfig"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageConfig")
    def cloud_storage_config(
        self,
    ) -> "GooglePubsubSubscriptionCloudStorageConfigOutputReference":
        return typing.cast("GooglePubsubSubscriptionCloudStorageConfigOutputReference", jsii.get(self, "cloudStorageConfig"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterPolicy")
    def dead_letter_policy(
        self,
    ) -> "GooglePubsubSubscriptionDeadLetterPolicyOutputReference":
        return typing.cast("GooglePubsubSubscriptionDeadLetterPolicyOutputReference", jsii.get(self, "deadLetterPolicy"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="expirationPolicy")
    def expiration_policy(
        self,
    ) -> "GooglePubsubSubscriptionExpirationPolicyOutputReference":
        return typing.cast("GooglePubsubSubscriptionExpirationPolicyOutputReference", jsii.get(self, "expirationPolicy"))

    @builtins.property
    @jsii.member(jsii_name="messageTransforms")
    def message_transforms(self) -> "GooglePubsubSubscriptionMessageTransformsList":
        return typing.cast("GooglePubsubSubscriptionMessageTransformsList", jsii.get(self, "messageTransforms"))

    @builtins.property
    @jsii.member(jsii_name="pushConfig")
    def push_config(self) -> "GooglePubsubSubscriptionPushConfigOutputReference":
        return typing.cast("GooglePubsubSubscriptionPushConfigOutputReference", jsii.get(self, "pushConfig"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicy")
    def retry_policy(self) -> "GooglePubsubSubscriptionRetryPolicyOutputReference":
        return typing.cast("GooglePubsubSubscriptionRetryPolicyOutputReference", jsii.get(self, "retryPolicy"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GooglePubsubSubscriptionTimeoutsOutputReference":
        return typing.cast("GooglePubsubSubscriptionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="ackDeadlineSecondsInput")
    def ack_deadline_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ackDeadlineSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryConfigInput")
    def bigquery_config_input(
        self,
    ) -> typing.Optional["GooglePubsubSubscriptionBigqueryConfig"]:
        return typing.cast(typing.Optional["GooglePubsubSubscriptionBigqueryConfig"], jsii.get(self, "bigqueryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageConfigInput")
    def cloud_storage_config_input(
        self,
    ) -> typing.Optional["GooglePubsubSubscriptionCloudStorageConfig"]:
        return typing.cast(typing.Optional["GooglePubsubSubscriptionCloudStorageConfig"], jsii.get(self, "cloudStorageConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterPolicyInput")
    def dead_letter_policy_input(
        self,
    ) -> typing.Optional["GooglePubsubSubscriptionDeadLetterPolicy"]:
        return typing.cast(typing.Optional["GooglePubsubSubscriptionDeadLetterPolicy"], jsii.get(self, "deadLetterPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="enableExactlyOnceDeliveryInput")
    def enable_exactly_once_delivery_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableExactlyOnceDeliveryInput"))

    @builtins.property
    @jsii.member(jsii_name="enableMessageOrderingInput")
    def enable_message_ordering_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableMessageOrderingInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationPolicyInput")
    def expiration_policy_input(
        self,
    ) -> typing.Optional["GooglePubsubSubscriptionExpirationPolicy"]:
        return typing.cast(typing.Optional["GooglePubsubSubscriptionExpirationPolicy"], jsii.get(self, "expirationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterInput"))

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
    @jsii.member(jsii_name="messageRetentionDurationInput")
    def message_retention_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageRetentionDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="messageTransformsInput")
    def message_transforms_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePubsubSubscriptionMessageTransforms"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePubsubSubscriptionMessageTransforms"]]], jsii.get(self, "messageTransformsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="pushConfigInput")
    def push_config_input(
        self,
    ) -> typing.Optional["GooglePubsubSubscriptionPushConfig"]:
        return typing.cast(typing.Optional["GooglePubsubSubscriptionPushConfig"], jsii.get(self, "pushConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="retainAckedMessagesInput")
    def retain_acked_messages_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "retainAckedMessagesInput"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicyInput")
    def retry_policy_input(
        self,
    ) -> typing.Optional["GooglePubsubSubscriptionRetryPolicy"]:
        return typing.cast(typing.Optional["GooglePubsubSubscriptionRetryPolicy"], jsii.get(self, "retryPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GooglePubsubSubscriptionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GooglePubsubSubscriptionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="ackDeadlineSeconds")
    def ack_deadline_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ackDeadlineSeconds"))

    @ack_deadline_seconds.setter
    def ack_deadline_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c9b63499d1ad43964edc60d842d83299e4d8c096659116db7a1d611f75e1556)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ackDeadlineSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableExactlyOnceDelivery")
    def enable_exactly_once_delivery(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableExactlyOnceDelivery"))

    @enable_exactly_once_delivery.setter
    def enable_exactly_once_delivery(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4657d3337651687f779c0e5d0fdd93da5c4ca669258c9fa36a7c8eb1e411b467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableExactlyOnceDelivery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableMessageOrdering")
    def enable_message_ordering(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableMessageOrdering"))

    @enable_message_ordering.setter
    def enable_message_ordering(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55493f2ce2d38aa9bc1cc777b2ce5bf67256514195a000dffb45c3a848f85265)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableMessageOrdering", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f858a06da9adf1723290dcf007d3e8dae63351bbc757e901be4c2cb99c002878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c24d5013f509e5ff12b63dff8e1a4afe63c3b76defef41771d1b89814bef06d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3298fed324ba9fd73270f8f9497c1a812d9cd7c5f7aa45a74914a35fe4475c1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="messageRetentionDuration")
    def message_retention_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageRetentionDuration"))

    @message_retention_duration.setter
    def message_retention_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f1d1aaef19b61ea46396a46ffd62f14ea393eef7b0fe87180d112316feb89aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageRetentionDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9184886689f30cc2cdfc3d76ee8854fe0139f4f74891944333e4e21765e50cc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae8d5bc87dcd601e7fa182c8a589ae038eedb4ad118b65a72aefef4ac9fcbfff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retainAckedMessages")
    def retain_acked_messages(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "retainAckedMessages"))

    @retain_acked_messages.setter
    def retain_acked_messages(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b578b164a885df21a49f89e7829940d52706a12541a49dacda21777d4f4de647)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retainAckedMessages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__164632d697b7a72eecabeba6d73ab22230e250a68b800921671a78646964b610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionBigqueryConfig",
    jsii_struct_bases=[],
    name_mapping={
        "table": "table",
        "drop_unknown_fields": "dropUnknownFields",
        "service_account_email": "serviceAccountEmail",
        "use_table_schema": "useTableSchema",
        "use_topic_schema": "useTopicSchema",
        "write_metadata": "writeMetadata",
    },
)
class GooglePubsubSubscriptionBigqueryConfig:
    def __init__(
        self,
        *,
        table: builtins.str,
        drop_unknown_fields: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        service_account_email: typing.Optional[builtins.str] = None,
        use_table_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_topic_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        write_metadata: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param table: The name of the table to which to write data, of the form {projectId}.{datasetId}.{tableId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#table GooglePubsubSubscription#table}
        :param drop_unknown_fields: When true and use_topic_schema or use_table_schema is true, any fields that are a part of the topic schema or message schema that are not part of the BigQuery table schema are dropped when writing to BigQuery. Otherwise, the schemas must be kept in sync and any messages with extra fields are not written and remain in the subscription's backlog. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#drop_unknown_fields GooglePubsubSubscription#drop_unknown_fields}
        :param service_account_email: The service account to use to write to BigQuery. If not specified, the Pub/Sub `service agent <https://cloud.google.com/iam/docs/service-agents>`_, service-{project_number}@gcp-sa-pubsub.iam.gserviceaccount.com, is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#service_account_email GooglePubsubSubscription#service_account_email}
        :param use_table_schema: When true, use the BigQuery table's schema as the columns to write to in BigQuery. Messages must be published in JSON format. Only one of use_topic_schema and use_table_schema can be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#use_table_schema GooglePubsubSubscription#use_table_schema}
        :param use_topic_schema: When true, use the topic's schema as the columns to write to in BigQuery, if it exists. Only one of use_topic_schema and use_table_schema can be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#use_topic_schema GooglePubsubSubscription#use_topic_schema}
        :param write_metadata: When true, write the subscription name, messageId, publishTime, attributes, and orderingKey to additional columns in the table. The subscription name, messageId, and publishTime fields are put in their own columns while all other message properties (other than data) are written to a JSON object in the attributes column. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#write_metadata GooglePubsubSubscription#write_metadata}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb37b3f100a29333fb603d0ddb035e561f7e82a3dc752479955bc12334d52c3a)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
            check_type(argname="argument drop_unknown_fields", value=drop_unknown_fields, expected_type=type_hints["drop_unknown_fields"])
            check_type(argname="argument service_account_email", value=service_account_email, expected_type=type_hints["service_account_email"])
            check_type(argname="argument use_table_schema", value=use_table_schema, expected_type=type_hints["use_table_schema"])
            check_type(argname="argument use_topic_schema", value=use_topic_schema, expected_type=type_hints["use_topic_schema"])
            check_type(argname="argument write_metadata", value=write_metadata, expected_type=type_hints["write_metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table": table,
        }
        if drop_unknown_fields is not None:
            self._values["drop_unknown_fields"] = drop_unknown_fields
        if service_account_email is not None:
            self._values["service_account_email"] = service_account_email
        if use_table_schema is not None:
            self._values["use_table_schema"] = use_table_schema
        if use_topic_schema is not None:
            self._values["use_topic_schema"] = use_topic_schema
        if write_metadata is not None:
            self._values["write_metadata"] = write_metadata

    @builtins.property
    def table(self) -> builtins.str:
        '''The name of the table to which to write data, of the form {projectId}.{datasetId}.{tableId}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#table GooglePubsubSubscription#table}
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def drop_unknown_fields(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true and use_topic_schema or use_table_schema is true, any fields that are a part of the topic schema or message schema that are not part of the BigQuery table schema are dropped when writing to BigQuery.

        Otherwise, the schemas must be kept in sync
        and any messages with extra fields are not written and remain in the subscription's backlog.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#drop_unknown_fields GooglePubsubSubscription#drop_unknown_fields}
        '''
        result = self._values.get("drop_unknown_fields")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def service_account_email(self) -> typing.Optional[builtins.str]:
        '''The service account to use to write to BigQuery. If not specified, the Pub/Sub `service agent <https://cloud.google.com/iam/docs/service-agents>`_, service-{project_number}@gcp-sa-pubsub.iam.gserviceaccount.com, is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#service_account_email GooglePubsubSubscription#service_account_email}
        '''
        result = self._values.get("service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_table_schema(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, use the BigQuery table's schema as the columns to write to in BigQuery.

        Messages
        must be published in JSON format. Only one of use_topic_schema and use_table_schema can be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#use_table_schema GooglePubsubSubscription#use_table_schema}
        '''
        result = self._values.get("use_table_schema")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_topic_schema(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, use the topic's schema as the columns to write to in BigQuery, if it exists.

        Only one of use_topic_schema and use_table_schema can be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#use_topic_schema GooglePubsubSubscription#use_topic_schema}
        '''
        result = self._values.get("use_topic_schema")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def write_metadata(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, write the subscription name, messageId, publishTime, attributes, and orderingKey to additional columns in the table.

        The subscription name, messageId, and publishTime fields are put in their own columns while all other message properties (other than data) are written to a JSON object in the attributes column.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#write_metadata GooglePubsubSubscription#write_metadata}
        '''
        result = self._values.get("write_metadata")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubSubscriptionBigqueryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubSubscriptionBigqueryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionBigqueryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6fced1a4a0041d6b46718aef3fbb322440075ecf83dc10ba817d5b146b19483)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDropUnknownFields")
    def reset_drop_unknown_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDropUnknownFields", []))

    @jsii.member(jsii_name="resetServiceAccountEmail")
    def reset_service_account_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountEmail", []))

    @jsii.member(jsii_name="resetUseTableSchema")
    def reset_use_table_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseTableSchema", []))

    @jsii.member(jsii_name="resetUseTopicSchema")
    def reset_use_topic_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseTopicSchema", []))

    @jsii.member(jsii_name="resetWriteMetadata")
    def reset_write_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriteMetadata", []))

    @builtins.property
    @jsii.member(jsii_name="dropUnknownFieldsInput")
    def drop_unknown_fields_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dropUnknownFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmailInput")
    def service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="tableInput")
    def table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableInput"))

    @builtins.property
    @jsii.member(jsii_name="useTableSchemaInput")
    def use_table_schema_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useTableSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="useTopicSchemaInput")
    def use_topic_schema_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useTopicSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="writeMetadataInput")
    def write_metadata_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "writeMetadataInput"))

    @builtins.property
    @jsii.member(jsii_name="dropUnknownFields")
    def drop_unknown_fields(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dropUnknownFields"))

    @drop_unknown_fields.setter
    def drop_unknown_fields(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a999d74942d1a015f3885b2bce920d2ed5cc443680cb67723fc759446678195)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dropUnknownFields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c7bc2a3b0c394410422cf4379354cf559dffc6b30879ceb649ad6b091495463)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "table"))

    @table.setter
    def table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57c1ddbb89fd9e90c7d1e58baea6faf6c243248f8a195b133734fcf0a2a4055a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "table", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useTableSchema")
    def use_table_schema(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useTableSchema"))

    @use_table_schema.setter
    def use_table_schema(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97b0509b241a86b383844f68aae542b4d5128e513bb73a6c1136bab505fe978c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useTableSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useTopicSchema")
    def use_topic_schema(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useTopicSchema"))

    @use_topic_schema.setter
    def use_topic_schema(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f6a7f079e6ea39b70a0bbdf309783a3f3d6e2134cc1584836c928fe44ad5566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useTopicSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="writeMetadata")
    def write_metadata(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "writeMetadata"))

    @write_metadata.setter
    def write_metadata(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__060af42cd66f38600743c8ed5e946b02950ca528fbb5777bce152b8b6e833cfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeMetadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GooglePubsubSubscriptionBigqueryConfig]:
        return typing.cast(typing.Optional[GooglePubsubSubscriptionBigqueryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubSubscriptionBigqueryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__123a26c8061e6ccbbecce2a1396bce8de5dce19770d1a87018ebf6c52f00d3dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionCloudStorageConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "avro_config": "avroConfig",
        "filename_datetime_format": "filenameDatetimeFormat",
        "filename_prefix": "filenamePrefix",
        "filename_suffix": "filenameSuffix",
        "max_bytes": "maxBytes",
        "max_duration": "maxDuration",
        "max_messages": "maxMessages",
        "service_account_email": "serviceAccountEmail",
    },
)
class GooglePubsubSubscriptionCloudStorageConfig:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        avro_config: typing.Optional[typing.Union["GooglePubsubSubscriptionCloudStorageConfigAvroConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        filename_datetime_format: typing.Optional[builtins.str] = None,
        filename_prefix: typing.Optional[builtins.str] = None,
        filename_suffix: typing.Optional[builtins.str] = None,
        max_bytes: typing.Optional[jsii.Number] = None,
        max_duration: typing.Optional[builtins.str] = None,
        max_messages: typing.Optional[jsii.Number] = None,
        service_account_email: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: User-provided name for the Cloud Storage bucket. The bucket must be created by the user. The bucket name must be without any prefix like "gs://". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#bucket GooglePubsubSubscription#bucket}
        :param avro_config: avro_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#avro_config GooglePubsubSubscription#avro_config}
        :param filename_datetime_format: User-provided format string specifying how to represent datetimes in Cloud Storage filenames. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#filename_datetime_format GooglePubsubSubscription#filename_datetime_format}
        :param filename_prefix: User-provided prefix for Cloud Storage filename. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#filename_prefix GooglePubsubSubscription#filename_prefix}
        :param filename_suffix: User-provided suffix for Cloud Storage filename. Must not end in "/". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#filename_suffix GooglePubsubSubscription#filename_suffix}
        :param max_bytes: The maximum bytes that can be written to a Cloud Storage file before a new file is created. Min 1 KB, max 10 GiB. The maxBytes limit may be exceeded in cases where messages are larger than the limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#max_bytes GooglePubsubSubscription#max_bytes}
        :param max_duration: The maximum duration that can elapse before a new Cloud Storage file is created. Min 1 minute, max 10 minutes, default 5 minutes. May not exceed the subscription's acknowledgement deadline. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#max_duration GooglePubsubSubscription#max_duration}
        :param max_messages: The maximum messages that can be written to a Cloud Storage file before a new file is created. Min 1000 messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#max_messages GooglePubsubSubscription#max_messages}
        :param service_account_email: The service account to use to write to Cloud Storage. If not specified, the Pub/Sub `service agent <https://cloud.google.com/iam/docs/service-agents>`_, service-{project_number}@gcp-sa-pubsub.iam.gserviceaccount.com, is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#service_account_email GooglePubsubSubscription#service_account_email}
        '''
        if isinstance(avro_config, dict):
            avro_config = GooglePubsubSubscriptionCloudStorageConfigAvroConfig(**avro_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__956f7a8fbffda70685ed5546f850ac1d64a834c92cd77233ad4458f7918cac81)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument avro_config", value=avro_config, expected_type=type_hints["avro_config"])
            check_type(argname="argument filename_datetime_format", value=filename_datetime_format, expected_type=type_hints["filename_datetime_format"])
            check_type(argname="argument filename_prefix", value=filename_prefix, expected_type=type_hints["filename_prefix"])
            check_type(argname="argument filename_suffix", value=filename_suffix, expected_type=type_hints["filename_suffix"])
            check_type(argname="argument max_bytes", value=max_bytes, expected_type=type_hints["max_bytes"])
            check_type(argname="argument max_duration", value=max_duration, expected_type=type_hints["max_duration"])
            check_type(argname="argument max_messages", value=max_messages, expected_type=type_hints["max_messages"])
            check_type(argname="argument service_account_email", value=service_account_email, expected_type=type_hints["service_account_email"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if avro_config is not None:
            self._values["avro_config"] = avro_config
        if filename_datetime_format is not None:
            self._values["filename_datetime_format"] = filename_datetime_format
        if filename_prefix is not None:
            self._values["filename_prefix"] = filename_prefix
        if filename_suffix is not None:
            self._values["filename_suffix"] = filename_suffix
        if max_bytes is not None:
            self._values["max_bytes"] = max_bytes
        if max_duration is not None:
            self._values["max_duration"] = max_duration
        if max_messages is not None:
            self._values["max_messages"] = max_messages
        if service_account_email is not None:
            self._values["service_account_email"] = service_account_email

    @builtins.property
    def bucket(self) -> builtins.str:
        '''User-provided name for the Cloud Storage bucket.

        The bucket must be created by the user. The bucket name must be without any prefix like "gs://".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#bucket GooglePubsubSubscription#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def avro_config(
        self,
    ) -> typing.Optional["GooglePubsubSubscriptionCloudStorageConfigAvroConfig"]:
        '''avro_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#avro_config GooglePubsubSubscription#avro_config}
        '''
        result = self._values.get("avro_config")
        return typing.cast(typing.Optional["GooglePubsubSubscriptionCloudStorageConfigAvroConfig"], result)

    @builtins.property
    def filename_datetime_format(self) -> typing.Optional[builtins.str]:
        '''User-provided format string specifying how to represent datetimes in Cloud Storage filenames.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#filename_datetime_format GooglePubsubSubscription#filename_datetime_format}
        '''
        result = self._values.get("filename_datetime_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filename_prefix(self) -> typing.Optional[builtins.str]:
        '''User-provided prefix for Cloud Storage filename.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#filename_prefix GooglePubsubSubscription#filename_prefix}
        '''
        result = self._values.get("filename_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filename_suffix(self) -> typing.Optional[builtins.str]:
        '''User-provided suffix for Cloud Storage filename. Must not end in "/".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#filename_suffix GooglePubsubSubscription#filename_suffix}
        '''
        result = self._values.get("filename_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_bytes(self) -> typing.Optional[jsii.Number]:
        '''The maximum bytes that can be written to a Cloud Storage file before a new file is created.

        Min 1 KB, max 10 GiB.
        The maxBytes limit may be exceeded in cases where messages are larger than the limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#max_bytes GooglePubsubSubscription#max_bytes}
        '''
        result = self._values.get("max_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_duration(self) -> typing.Optional[builtins.str]:
        '''The maximum duration that can elapse before a new Cloud Storage file is created.

        Min 1 minute, max 10 minutes, default 5 minutes.
        May not exceed the subscription's acknowledgement deadline.
        A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#max_duration GooglePubsubSubscription#max_duration}
        '''
        result = self._values.get("max_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_messages(self) -> typing.Optional[jsii.Number]:
        '''The maximum messages that can be written to a Cloud Storage file before a new file is created.

        Min 1000 messages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#max_messages GooglePubsubSubscription#max_messages}
        '''
        result = self._values.get("max_messages")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_account_email(self) -> typing.Optional[builtins.str]:
        '''The service account to use to write to Cloud Storage. If not specified, the Pub/Sub `service agent <https://cloud.google.com/iam/docs/service-agents>`_, service-{project_number}@gcp-sa-pubsub.iam.gserviceaccount.com, is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#service_account_email GooglePubsubSubscription#service_account_email}
        '''
        result = self._values.get("service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubSubscriptionCloudStorageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionCloudStorageConfigAvroConfig",
    jsii_struct_bases=[],
    name_mapping={
        "use_topic_schema": "useTopicSchema",
        "write_metadata": "writeMetadata",
    },
)
class GooglePubsubSubscriptionCloudStorageConfigAvroConfig:
    def __init__(
        self,
        *,
        use_topic_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        write_metadata: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param use_topic_schema: When true, the output Cloud Storage file will be serialized using the topic schema, if it exists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#use_topic_schema GooglePubsubSubscription#use_topic_schema}
        :param write_metadata: When true, write the subscription name, messageId, publishTime, attributes, and orderingKey as additional fields in the output. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#write_metadata GooglePubsubSubscription#write_metadata}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce914fe2fc859585d48051a0c037194150a422009b67956ea35a89ba6f60deaa)
            check_type(argname="argument use_topic_schema", value=use_topic_schema, expected_type=type_hints["use_topic_schema"])
            check_type(argname="argument write_metadata", value=write_metadata, expected_type=type_hints["write_metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if use_topic_schema is not None:
            self._values["use_topic_schema"] = use_topic_schema
        if write_metadata is not None:
            self._values["write_metadata"] = write_metadata

    @builtins.property
    def use_topic_schema(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, the output Cloud Storage file will be serialized using the topic schema, if it exists.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#use_topic_schema GooglePubsubSubscription#use_topic_schema}
        '''
        result = self._values.get("use_topic_schema")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def write_metadata(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, write the subscription name, messageId, publishTime, attributes, and orderingKey as additional fields in the output.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#write_metadata GooglePubsubSubscription#write_metadata}
        '''
        result = self._values.get("write_metadata")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubSubscriptionCloudStorageConfigAvroConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubSubscriptionCloudStorageConfigAvroConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionCloudStorageConfigAvroConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5066765ec7fd84be686cd5f45a42d1ead5cf7034c2406a23148e884d21fa61b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUseTopicSchema")
    def reset_use_topic_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseTopicSchema", []))

    @jsii.member(jsii_name="resetWriteMetadata")
    def reset_write_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriteMetadata", []))

    @builtins.property
    @jsii.member(jsii_name="useTopicSchemaInput")
    def use_topic_schema_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useTopicSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="writeMetadataInput")
    def write_metadata_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "writeMetadataInput"))

    @builtins.property
    @jsii.member(jsii_name="useTopicSchema")
    def use_topic_schema(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useTopicSchema"))

    @use_topic_schema.setter
    def use_topic_schema(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a239209820777560fe5c6d271f098efaec5be75a804d5a7c584bd4380876c559)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useTopicSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="writeMetadata")
    def write_metadata(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "writeMetadata"))

    @write_metadata.setter
    def write_metadata(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f707a3a24d8bbf7e6417f408df62472e7fe6de7d2a32183817bd509849011328)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeMetadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePubsubSubscriptionCloudStorageConfigAvroConfig]:
        return typing.cast(typing.Optional[GooglePubsubSubscriptionCloudStorageConfigAvroConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubSubscriptionCloudStorageConfigAvroConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34fa3463c7c2654b23f3d2d0b4e4f77ad4e77f30888540076532280a29226652)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePubsubSubscriptionCloudStorageConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionCloudStorageConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03a378002d42c40f5bbb4e1688da653dca467c2a987541e9394092cda6b006c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAvroConfig")
    def put_avro_config(
        self,
        *,
        use_topic_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        write_metadata: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param use_topic_schema: When true, the output Cloud Storage file will be serialized using the topic schema, if it exists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#use_topic_schema GooglePubsubSubscription#use_topic_schema}
        :param write_metadata: When true, write the subscription name, messageId, publishTime, attributes, and orderingKey as additional fields in the output. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#write_metadata GooglePubsubSubscription#write_metadata}
        '''
        value = GooglePubsubSubscriptionCloudStorageConfigAvroConfig(
            use_topic_schema=use_topic_schema, write_metadata=write_metadata
        )

        return typing.cast(None, jsii.invoke(self, "putAvroConfig", [value]))

    @jsii.member(jsii_name="resetAvroConfig")
    def reset_avro_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvroConfig", []))

    @jsii.member(jsii_name="resetFilenameDatetimeFormat")
    def reset_filename_datetime_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilenameDatetimeFormat", []))

    @jsii.member(jsii_name="resetFilenamePrefix")
    def reset_filename_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilenamePrefix", []))

    @jsii.member(jsii_name="resetFilenameSuffix")
    def reset_filename_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilenameSuffix", []))

    @jsii.member(jsii_name="resetMaxBytes")
    def reset_max_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxBytes", []))

    @jsii.member(jsii_name="resetMaxDuration")
    def reset_max_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxDuration", []))

    @jsii.member(jsii_name="resetMaxMessages")
    def reset_max_messages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxMessages", []))

    @jsii.member(jsii_name="resetServiceAccountEmail")
    def reset_service_account_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountEmail", []))

    @builtins.property
    @jsii.member(jsii_name="avroConfig")
    def avro_config(
        self,
    ) -> GooglePubsubSubscriptionCloudStorageConfigAvroConfigOutputReference:
        return typing.cast(GooglePubsubSubscriptionCloudStorageConfigAvroConfigOutputReference, jsii.get(self, "avroConfig"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="avroConfigInput")
    def avro_config_input(
        self,
    ) -> typing.Optional[GooglePubsubSubscriptionCloudStorageConfigAvroConfig]:
        return typing.cast(typing.Optional[GooglePubsubSubscriptionCloudStorageConfigAvroConfig], jsii.get(self, "avroConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="filenameDatetimeFormatInput")
    def filename_datetime_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filenameDatetimeFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="filenamePrefixInput")
    def filename_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filenamePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="filenameSuffixInput")
    def filename_suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filenameSuffixInput"))

    @builtins.property
    @jsii.member(jsii_name="maxBytesInput")
    def max_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxDurationInput")
    def max_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxMessagesInput")
    def max_messages_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxMessagesInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmailInput")
    def service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__670cf9082cac48376016e75a3fb7b545f32d799d3ac7a3deca64c29735a88104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filenameDatetimeFormat")
    def filename_datetime_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filenameDatetimeFormat"))

    @filename_datetime_format.setter
    def filename_datetime_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c81650a119349668957bd97d7ceba3e9ccb22336fd4a8b23f362310c28c6c56d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filenameDatetimeFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filenamePrefix")
    def filename_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filenamePrefix"))

    @filename_prefix.setter
    def filename_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11fe311ccb499ffa1c4c379ff589156c3f9d67fde4cd19b97cb70fe1fcc2ea7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filenamePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filenameSuffix")
    def filename_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filenameSuffix"))

    @filename_suffix.setter
    def filename_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b11feecd77c2e84db3f8f1e2b05559ce5cde7c2e9a1e3f0949c2dc0a5523ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filenameSuffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxBytes")
    def max_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxBytes"))

    @max_bytes.setter
    def max_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f4fcf5a940c8321434895c23eb2517fa8476ed9e4c9bd0fa84978d2ece568e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDuration")
    def max_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxDuration"))

    @max_duration.setter
    def max_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__689d73a5ac0bdfc934e3ebfd25157283f8f44db54647637f6c5672d3da286abf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxMessages")
    def max_messages(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxMessages"))

    @max_messages.setter
    def max_messages(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daaf96574e2fcdcf69eb91798b207f25c44e2d16ae8db01ea67dc47ffb51e0a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxMessages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9acf373d919651a977ac983697fc6c22f88c9c904ceaa8939464a85ff78ab37a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePubsubSubscriptionCloudStorageConfig]:
        return typing.cast(typing.Optional[GooglePubsubSubscriptionCloudStorageConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubSubscriptionCloudStorageConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8df4d11e9291bc19592323cfd18a9e9b78fb97cb75ffabc60e6379aae9c13a8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionConfig",
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
        "topic": "topic",
        "ack_deadline_seconds": "ackDeadlineSeconds",
        "bigquery_config": "bigqueryConfig",
        "cloud_storage_config": "cloudStorageConfig",
        "dead_letter_policy": "deadLetterPolicy",
        "enable_exactly_once_delivery": "enableExactlyOnceDelivery",
        "enable_message_ordering": "enableMessageOrdering",
        "expiration_policy": "expirationPolicy",
        "filter": "filter",
        "id": "id",
        "labels": "labels",
        "message_retention_duration": "messageRetentionDuration",
        "message_transforms": "messageTransforms",
        "project": "project",
        "push_config": "pushConfig",
        "retain_acked_messages": "retainAckedMessages",
        "retry_policy": "retryPolicy",
        "timeouts": "timeouts",
    },
)
class GooglePubsubSubscriptionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        topic: builtins.str,
        ack_deadline_seconds: typing.Optional[jsii.Number] = None,
        bigquery_config: typing.Optional[typing.Union[GooglePubsubSubscriptionBigqueryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_storage_config: typing.Optional[typing.Union[GooglePubsubSubscriptionCloudStorageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_policy: typing.Optional[typing.Union["GooglePubsubSubscriptionDeadLetterPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_exactly_once_delivery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_message_ordering: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expiration_policy: typing.Optional[typing.Union["GooglePubsubSubscriptionExpirationPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        filter: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        message_retention_duration: typing.Optional[builtins.str] = None,
        message_transforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GooglePubsubSubscriptionMessageTransforms", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        push_config: typing.Optional[typing.Union["GooglePubsubSubscriptionPushConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        retain_acked_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retry_policy: typing.Optional[typing.Union["GooglePubsubSubscriptionRetryPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GooglePubsubSubscriptionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the subscription. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#name GooglePubsubSubscription#name}
        :param topic: A reference to a Topic resource, of the form projects/{project}/topics/{{name}} (as in the id property of a google_pubsub_topic), or just a topic name if the topic is in the same project as the subscription. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#topic GooglePubsubSubscription#topic}
        :param ack_deadline_seconds: This value is the maximum time after a subscriber receives a message before the subscriber should acknowledge the message. After message delivery but before the ack deadline expires and before the message is acknowledged, it is an outstanding message and will not be delivered again during that time (on a best-effort basis). For pull subscriptions, this value is used as the initial value for the ack deadline. To override this value for a given message, call subscriptions.modifyAckDeadline with the corresponding ackId if using pull. The minimum custom deadline you can specify is 10 seconds. The maximum custom deadline you can specify is 600 seconds (10 minutes). If this parameter is 0, a default value of 10 seconds is used. For push delivery, this value is also used to set the request timeout for the call to the push endpoint. If the subscriber never acknowledges the message, the Pub/Sub system will eventually redeliver the message. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#ack_deadline_seconds GooglePubsubSubscription#ack_deadline_seconds}
        :param bigquery_config: bigquery_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#bigquery_config GooglePubsubSubscription#bigquery_config}
        :param cloud_storage_config: cloud_storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#cloud_storage_config GooglePubsubSubscription#cloud_storage_config}
        :param dead_letter_policy: dead_letter_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#dead_letter_policy GooglePubsubSubscription#dead_letter_policy}
        :param enable_exactly_once_delivery: If 'true', Pub/Sub provides the following guarantees for the delivery of a message with a given value of messageId on this Subscriptions': - The message sent to a subscriber is guaranteed not to be resent before the message's acknowledgement deadline expires. - An acknowledged message will not be resent to a subscriber. Note that subscribers may still receive multiple copies of a message when 'enable_exactly_once_delivery' is true if the message was published multiple times by a publisher client. These copies are considered distinct by Pub/Sub and have distinct messageId values Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#enable_exactly_once_delivery GooglePubsubSubscription#enable_exactly_once_delivery}
        :param enable_message_ordering: If 'true', messages published with the same orderingKey in PubsubMessage will be delivered to the subscribers in the order in which they are received by the Pub/Sub system. Otherwise, they may be delivered in any order. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#enable_message_ordering GooglePubsubSubscription#enable_message_ordering}
        :param expiration_policy: expiration_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#expiration_policy GooglePubsubSubscription#expiration_policy}
        :param filter: The subscription only delivers the messages that match the filter. Pub/Sub automatically acknowledges the messages that don't match the filter. You can filter messages by their attributes. The maximum length of a filter is 256 bytes. After creating the subscription, you can't modify the filter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#filter GooglePubsubSubscription#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#id GooglePubsubSubscription#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A set of key/value label pairs to assign to this Subscription. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#labels GooglePubsubSubscription#labels}
        :param message_retention_duration: How long to retain unacknowledged messages in the subscription's backlog, from the moment a message is published. If retain_acked_messages is true, then this also configures the retention of acknowledged messages, and thus configures how far back in time a subscriptions.seek can be done. Defaults to 7 days. Cannot be more than 31 days ('"2678400s"') or less than 10 minutes ('"600s"'). A duration in seconds with up to nine fractional digits, terminated by 's'. Example: '"600.5s"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#message_retention_duration GooglePubsubSubscription#message_retention_duration}
        :param message_transforms: message_transforms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#message_transforms GooglePubsubSubscription#message_transforms}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#project GooglePubsubSubscription#project}.
        :param push_config: push_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#push_config GooglePubsubSubscription#push_config}
        :param retain_acked_messages: Indicates whether to retain acknowledged messages. If 'true', then messages are not expunged from the subscription's backlog, even if they are acknowledged, until they fall out of the messageRetentionDuration window. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#retain_acked_messages GooglePubsubSubscription#retain_acked_messages}
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#retry_policy GooglePubsubSubscription#retry_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#timeouts GooglePubsubSubscription#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bigquery_config, dict):
            bigquery_config = GooglePubsubSubscriptionBigqueryConfig(**bigquery_config)
        if isinstance(cloud_storage_config, dict):
            cloud_storage_config = GooglePubsubSubscriptionCloudStorageConfig(**cloud_storage_config)
        if isinstance(dead_letter_policy, dict):
            dead_letter_policy = GooglePubsubSubscriptionDeadLetterPolicy(**dead_letter_policy)
        if isinstance(expiration_policy, dict):
            expiration_policy = GooglePubsubSubscriptionExpirationPolicy(**expiration_policy)
        if isinstance(push_config, dict):
            push_config = GooglePubsubSubscriptionPushConfig(**push_config)
        if isinstance(retry_policy, dict):
            retry_policy = GooglePubsubSubscriptionRetryPolicy(**retry_policy)
        if isinstance(timeouts, dict):
            timeouts = GooglePubsubSubscriptionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b55b4d96cae3109c0e47d0b0b8b4d72a35e617062e702f0ec8ebed7a037452ec)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument ack_deadline_seconds", value=ack_deadline_seconds, expected_type=type_hints["ack_deadline_seconds"])
            check_type(argname="argument bigquery_config", value=bigquery_config, expected_type=type_hints["bigquery_config"])
            check_type(argname="argument cloud_storage_config", value=cloud_storage_config, expected_type=type_hints["cloud_storage_config"])
            check_type(argname="argument dead_letter_policy", value=dead_letter_policy, expected_type=type_hints["dead_letter_policy"])
            check_type(argname="argument enable_exactly_once_delivery", value=enable_exactly_once_delivery, expected_type=type_hints["enable_exactly_once_delivery"])
            check_type(argname="argument enable_message_ordering", value=enable_message_ordering, expected_type=type_hints["enable_message_ordering"])
            check_type(argname="argument expiration_policy", value=expiration_policy, expected_type=type_hints["expiration_policy"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument message_retention_duration", value=message_retention_duration, expected_type=type_hints["message_retention_duration"])
            check_type(argname="argument message_transforms", value=message_transforms, expected_type=type_hints["message_transforms"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument push_config", value=push_config, expected_type=type_hints["push_config"])
            check_type(argname="argument retain_acked_messages", value=retain_acked_messages, expected_type=type_hints["retain_acked_messages"])
            check_type(argname="argument retry_policy", value=retry_policy, expected_type=type_hints["retry_policy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "topic": topic,
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
        if ack_deadline_seconds is not None:
            self._values["ack_deadline_seconds"] = ack_deadline_seconds
        if bigquery_config is not None:
            self._values["bigquery_config"] = bigquery_config
        if cloud_storage_config is not None:
            self._values["cloud_storage_config"] = cloud_storage_config
        if dead_letter_policy is not None:
            self._values["dead_letter_policy"] = dead_letter_policy
        if enable_exactly_once_delivery is not None:
            self._values["enable_exactly_once_delivery"] = enable_exactly_once_delivery
        if enable_message_ordering is not None:
            self._values["enable_message_ordering"] = enable_message_ordering
        if expiration_policy is not None:
            self._values["expiration_policy"] = expiration_policy
        if filter is not None:
            self._values["filter"] = filter
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if message_retention_duration is not None:
            self._values["message_retention_duration"] = message_retention_duration
        if message_transforms is not None:
            self._values["message_transforms"] = message_transforms
        if project is not None:
            self._values["project"] = project
        if push_config is not None:
            self._values["push_config"] = push_config
        if retain_acked_messages is not None:
            self._values["retain_acked_messages"] = retain_acked_messages
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
    def name(self) -> builtins.str:
        '''Name of the subscription.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#name GooglePubsubSubscription#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''A reference to a Topic resource, of the form projects/{project}/topics/{{name}} (as in the id property of a google_pubsub_topic), or just a topic name if the topic is in the same project as the subscription.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#topic GooglePubsubSubscription#topic}
        '''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ack_deadline_seconds(self) -> typing.Optional[jsii.Number]:
        '''This value is the maximum time after a subscriber receives a message before the subscriber should acknowledge the message.

        After message
        delivery but before the ack deadline expires and before the message is
        acknowledged, it is an outstanding message and will not be delivered
        again during that time (on a best-effort basis).

        For pull subscriptions, this value is used as the initial value for
        the ack deadline. To override this value for a given message, call
        subscriptions.modifyAckDeadline with the corresponding ackId if using
        pull. The minimum custom deadline you can specify is 10 seconds. The
        maximum custom deadline you can specify is 600 seconds (10 minutes).
        If this parameter is 0, a default value of 10 seconds is used.

        For push delivery, this value is also used to set the request timeout
        for the call to the push endpoint.

        If the subscriber never acknowledges the message, the Pub/Sub system
        will eventually redeliver the message.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#ack_deadline_seconds GooglePubsubSubscription#ack_deadline_seconds}
        '''
        result = self._values.get("ack_deadline_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bigquery_config(
        self,
    ) -> typing.Optional[GooglePubsubSubscriptionBigqueryConfig]:
        '''bigquery_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#bigquery_config GooglePubsubSubscription#bigquery_config}
        '''
        result = self._values.get("bigquery_config")
        return typing.cast(typing.Optional[GooglePubsubSubscriptionBigqueryConfig], result)

    @builtins.property
    def cloud_storage_config(
        self,
    ) -> typing.Optional[GooglePubsubSubscriptionCloudStorageConfig]:
        '''cloud_storage_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#cloud_storage_config GooglePubsubSubscription#cloud_storage_config}
        '''
        result = self._values.get("cloud_storage_config")
        return typing.cast(typing.Optional[GooglePubsubSubscriptionCloudStorageConfig], result)

    @builtins.property
    def dead_letter_policy(
        self,
    ) -> typing.Optional["GooglePubsubSubscriptionDeadLetterPolicy"]:
        '''dead_letter_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#dead_letter_policy GooglePubsubSubscription#dead_letter_policy}
        '''
        result = self._values.get("dead_letter_policy")
        return typing.cast(typing.Optional["GooglePubsubSubscriptionDeadLetterPolicy"], result)

    @builtins.property
    def enable_exactly_once_delivery(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If 'true', Pub/Sub provides the following guarantees for the delivery of a message with a given value of messageId on this Subscriptions':  - The message sent to a subscriber is guaranteed not to be resent before the message's acknowledgement deadline expires.

        - An acknowledged message will not be resent to a subscriber.

        Note that subscribers may still receive multiple copies of a message when 'enable_exactly_once_delivery'
        is true if the message was published multiple times by a publisher client. These copies are considered distinct by Pub/Sub and have distinct messageId values

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#enable_exactly_once_delivery GooglePubsubSubscription#enable_exactly_once_delivery}
        '''
        result = self._values.get("enable_exactly_once_delivery")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_message_ordering(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If 'true', messages published with the same orderingKey in PubsubMessage will be delivered to the subscribers in the order in which they are received by the Pub/Sub system.

        Otherwise, they
        may be delivered in any order.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#enable_message_ordering GooglePubsubSubscription#enable_message_ordering}
        '''
        result = self._values.get("enable_message_ordering")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expiration_policy(
        self,
    ) -> typing.Optional["GooglePubsubSubscriptionExpirationPolicy"]:
        '''expiration_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#expiration_policy GooglePubsubSubscription#expiration_policy}
        '''
        result = self._values.get("expiration_policy")
        return typing.cast(typing.Optional["GooglePubsubSubscriptionExpirationPolicy"], result)

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        '''The subscription only delivers the messages that match the filter.

        Pub/Sub automatically acknowledges the messages that don't match the filter. You can filter messages
        by their attributes. The maximum length of a filter is 256 bytes. After creating the subscription,
        you can't modify the filter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#filter GooglePubsubSubscription#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#id GooglePubsubSubscription#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs to assign to this Subscription.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#labels GooglePubsubSubscription#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def message_retention_duration(self) -> typing.Optional[builtins.str]:
        '''How long to retain unacknowledged messages in the subscription's backlog, from the moment a message is published.

        If
        retain_acked_messages is true, then this also configures the retention
        of acknowledged messages, and thus configures how far back in time a
        subscriptions.seek can be done. Defaults to 7 days. Cannot be more
        than 31 days ('"2678400s"') or less than 10 minutes ('"600s"').

        A duration in seconds with up to nine fractional digits, terminated
        by 's'. Example: '"600.5s"'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#message_retention_duration GooglePubsubSubscription#message_retention_duration}
        '''
        result = self._values.get("message_retention_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_transforms(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePubsubSubscriptionMessageTransforms"]]]:
        '''message_transforms block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#message_transforms GooglePubsubSubscription#message_transforms}
        '''
        result = self._values.get("message_transforms")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePubsubSubscriptionMessageTransforms"]]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#project GooglePubsubSubscription#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def push_config(self) -> typing.Optional["GooglePubsubSubscriptionPushConfig"]:
        '''push_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#push_config GooglePubsubSubscription#push_config}
        '''
        result = self._values.get("push_config")
        return typing.cast(typing.Optional["GooglePubsubSubscriptionPushConfig"], result)

    @builtins.property
    def retain_acked_messages(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether to retain acknowledged messages.

        If 'true', then
        messages are not expunged from the subscription's backlog, even if
        they are acknowledged, until they fall out of the
        messageRetentionDuration window.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#retain_acked_messages GooglePubsubSubscription#retain_acked_messages}
        '''
        result = self._values.get("retain_acked_messages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retry_policy(self) -> typing.Optional["GooglePubsubSubscriptionRetryPolicy"]:
        '''retry_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#retry_policy GooglePubsubSubscription#retry_policy}
        '''
        result = self._values.get("retry_policy")
        return typing.cast(typing.Optional["GooglePubsubSubscriptionRetryPolicy"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GooglePubsubSubscriptionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#timeouts GooglePubsubSubscription#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GooglePubsubSubscriptionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubSubscriptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionDeadLetterPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "dead_letter_topic": "deadLetterTopic",
        "max_delivery_attempts": "maxDeliveryAttempts",
    },
)
class GooglePubsubSubscriptionDeadLetterPolicy:
    def __init__(
        self,
        *,
        dead_letter_topic: typing.Optional[builtins.str] = None,
        max_delivery_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param dead_letter_topic: The name of the topic to which dead letter messages should be published. Format is 'projects/{project}/topics/{topic}'. The Cloud Pub/Sub service account associated with the enclosing subscription's parent project (i.e., service-{project_number}@gcp-sa-pubsub.iam.gserviceaccount.com) must have permission to Publish() to this topic. The operation will fail if the topic does not exist. Users should ensure that there is a subscription attached to this topic since messages published to a topic with no subscriptions are lost. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#dead_letter_topic GooglePubsubSubscription#dead_letter_topic}
        :param max_delivery_attempts: The maximum number of delivery attempts for any message. The value must be between 5 and 100. The number of delivery attempts is defined as 1 + (the sum of number of NACKs and number of times the acknowledgement deadline has been exceeded for the message). A NACK is any call to ModifyAckDeadline with a 0 deadline. Note that client libraries may automatically extend ack_deadlines. This field will be honored on a best effort basis. If this parameter is 0, a default value of 5 is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#max_delivery_attempts GooglePubsubSubscription#max_delivery_attempts}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12f9afb36467f7e4955e968f01e0c823bfafaec12cfb802b51bf4a84caa56457)
            check_type(argname="argument dead_letter_topic", value=dead_letter_topic, expected_type=type_hints["dead_letter_topic"])
            check_type(argname="argument max_delivery_attempts", value=max_delivery_attempts, expected_type=type_hints["max_delivery_attempts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dead_letter_topic is not None:
            self._values["dead_letter_topic"] = dead_letter_topic
        if max_delivery_attempts is not None:
            self._values["max_delivery_attempts"] = max_delivery_attempts

    @builtins.property
    def dead_letter_topic(self) -> typing.Optional[builtins.str]:
        '''The name of the topic to which dead letter messages should be published. Format is 'projects/{project}/topics/{topic}'.

        The Cloud Pub/Sub service account associated with the enclosing subscription's
        parent project (i.e.,
        service-{project_number}@gcp-sa-pubsub.iam.gserviceaccount.com) must have
        permission to Publish() to this topic.

        The operation will fail if the topic does not exist.
        Users should ensure that there is a subscription attached to this topic
        since messages published to a topic with no subscriptions are lost.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#dead_letter_topic GooglePubsubSubscription#dead_letter_topic}
        '''
        result = self._values.get("dead_letter_topic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_delivery_attempts(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of delivery attempts for any message. The value must be between 5 and 100.

        The number of delivery attempts is defined as 1 + (the sum of number of
        NACKs and number of times the acknowledgement deadline has been exceeded for the message).

        A NACK is any call to ModifyAckDeadline with a 0 deadline. Note that
        client libraries may automatically extend ack_deadlines.

        This field will be honored on a best effort basis.

        If this parameter is 0, a default value of 5 is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#max_delivery_attempts GooglePubsubSubscription#max_delivery_attempts}
        '''
        result = self._values.get("max_delivery_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubSubscriptionDeadLetterPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubSubscriptionDeadLetterPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionDeadLetterPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__050f1e2bafac2a5962f748c7c79b1c67919c6f58a38938521d55bf2682940be2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDeadLetterTopic")
    def reset_dead_letter_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeadLetterTopic", []))

    @jsii.member(jsii_name="resetMaxDeliveryAttempts")
    def reset_max_delivery_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxDeliveryAttempts", []))

    @builtins.property
    @jsii.member(jsii_name="deadLetterTopicInput")
    def dead_letter_topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deadLetterTopicInput"))

    @builtins.property
    @jsii.member(jsii_name="maxDeliveryAttemptsInput")
    def max_delivery_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxDeliveryAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterTopic")
    def dead_letter_topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deadLetterTopic"))

    @dead_letter_topic.setter
    def dead_letter_topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3375c5cccdaf9cc47ed4836d50bd0d270e79e844f2e6f85a024d67d539eddbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deadLetterTopic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDeliveryAttempts")
    def max_delivery_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDeliveryAttempts"))

    @max_delivery_attempts.setter
    def max_delivery_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b865b71fe0f74c7db804340a15c0c30b65e678517feb21014de5b9c88288b654)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDeliveryAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePubsubSubscriptionDeadLetterPolicy]:
        return typing.cast(typing.Optional[GooglePubsubSubscriptionDeadLetterPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubSubscriptionDeadLetterPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6e1f1f8cfc7632dba981273807c9659b3f9de73a956daaf45f7fd849dd0e693)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionExpirationPolicy",
    jsii_struct_bases=[],
    name_mapping={"ttl": "ttl"},
)
class GooglePubsubSubscriptionExpirationPolicy:
    def __init__(self, *, ttl: builtins.str) -> None:
        '''
        :param ttl: Specifies the "time-to-live" duration for an associated resource. The resource expires if it is not active for a period of ttl. If ttl is set to "", the associated resource never expires. A duration in seconds with up to nine fractional digits, terminated by 's'. Example - "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#ttl GooglePubsubSubscription#ttl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f1f1505ee44f580e6bb5b50ac731d3317ca3409bbd4829ce51f9a2632e3d60)
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ttl": ttl,
        }

    @builtins.property
    def ttl(self) -> builtins.str:
        '''Specifies the "time-to-live" duration for an associated resource.

        The
        resource expires if it is not active for a period of ttl.
        If ttl is set to "", the associated resource never expires.
        A duration in seconds with up to nine fractional digits, terminated by 's'.
        Example - "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#ttl GooglePubsubSubscription#ttl}
        '''
        result = self._values.get("ttl")
        assert result is not None, "Required property 'ttl' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubSubscriptionExpirationPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubSubscriptionExpirationPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionExpirationPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b19fdcc876dcd95d8b9c5ec071fde407b01ffa98d0882bae2aa35eb22e59dc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f5acc0b270cb18ccf3cdec7fe88bd2a30164dc199bb8fa0afd2f68e1b75530c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePubsubSubscriptionExpirationPolicy]:
        return typing.cast(typing.Optional[GooglePubsubSubscriptionExpirationPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubSubscriptionExpirationPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__389f25e77032782e5ba56204703eda6779eba3fdc83bc2a4ccfe95076001c02d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionMessageTransforms",
    jsii_struct_bases=[],
    name_mapping={"disabled": "disabled", "javascript_udf": "javascriptUdf"},
)
class GooglePubsubSubscriptionMessageTransforms:
    def __init__(
        self,
        *,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        javascript_udf: typing.Optional[typing.Union["GooglePubsubSubscriptionMessageTransformsJavascriptUdf", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param disabled: Controls whether or not to use this transform. If not set or 'false', the transform will be applied to messages. Default: 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#disabled GooglePubsubSubscription#disabled}
        :param javascript_udf: javascript_udf block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#javascript_udf GooglePubsubSubscription#javascript_udf}
        '''
        if isinstance(javascript_udf, dict):
            javascript_udf = GooglePubsubSubscriptionMessageTransformsJavascriptUdf(**javascript_udf)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4812736d2ce8fa8bf1e3d9942e14366af9cd117ca703c55ea9b1aaef2aff15e2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#disabled GooglePubsubSubscription#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def javascript_udf(
        self,
    ) -> typing.Optional["GooglePubsubSubscriptionMessageTransformsJavascriptUdf"]:
        '''javascript_udf block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#javascript_udf GooglePubsubSubscription#javascript_udf}
        '''
        result = self._values.get("javascript_udf")
        return typing.cast(typing.Optional["GooglePubsubSubscriptionMessageTransformsJavascriptUdf"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubSubscriptionMessageTransforms(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionMessageTransformsJavascriptUdf",
    jsii_struct_bases=[],
    name_mapping={"code": "code", "function_name": "functionName"},
)
class GooglePubsubSubscriptionMessageTransformsJavascriptUdf:
    def __init__(self, *, code: builtins.str, function_name: builtins.str) -> None:
        '''
        :param code: JavaScript code that contains a function 'function_name' with the following signature: ``` /** * Transforms a Pub/Sub message. - -
        :param function_name: Name of the JavaScript function that should be applied to Pub/Sub messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#function_name GooglePubsubSubscription#function_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3799025e08d62e1ea908ad28f0a5c512fb32247a1940d13a5f48042bd062a75)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#function_name GooglePubsubSubscription#function_name}
        '''
        result = self._values.get("function_name")
        assert result is not None, "Required property 'function_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubSubscriptionMessageTransformsJavascriptUdf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubSubscriptionMessageTransformsJavascriptUdfOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionMessageTransformsJavascriptUdfOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cccff69a3fd078b90662a751a7ab7bf3a7ab261762727670c4ef90a648744567)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a02afce18b634c981fb412876e83a86a2b6f88bac7243076b95f1ada0fc82544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "code", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionName"))

    @function_name.setter
    def function_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e52b719ecea4312bbd91cde10b97d1ab109f33ac697a5b0869a30b2f24aa1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePubsubSubscriptionMessageTransformsJavascriptUdf]:
        return typing.cast(typing.Optional[GooglePubsubSubscriptionMessageTransformsJavascriptUdf], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubSubscriptionMessageTransformsJavascriptUdf],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e15e6a5806b1d7fc56b35dac02e6d79316f9939098084bd6ccc12d422f7bb8c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePubsubSubscriptionMessageTransformsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionMessageTransformsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be17856dbc23abebb5cd5b359140e8ee8e8848afbcd9be24749479a4106e9e0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GooglePubsubSubscriptionMessageTransformsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f80ae4db5137dd822b8b8447b894bac8753ddf1cc36ab3afec1a448ceaba20)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GooglePubsubSubscriptionMessageTransformsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfdca579ffc24d2f95463d3a0019d662dcf802a386c99488a3fb7b14a232ae25)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13e758b8bb25b6e247f5d8bfbd645da05b156345ed4436030f26802918cf15d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3ceedcaff55083a79cacb248f4dda0284a1e912a9d3b23f2a4ba1e022c80be8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePubsubSubscriptionMessageTransforms]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePubsubSubscriptionMessageTransforms]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePubsubSubscriptionMessageTransforms]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efb81ed8fa5533dab082775f620875eff08bba361e522c11c8a1def1306d3b76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePubsubSubscriptionMessageTransformsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionMessageTransformsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d36b908827796f739577ba06b1de04cc78a2f6966f0c83e5df8790c219b0c502)
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
        :param function_name: Name of the JavaScript function that should be applied to Pub/Sub messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#function_name GooglePubsubSubscription#function_name}
        '''
        value = GooglePubsubSubscriptionMessageTransformsJavascriptUdf(
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
    ) -> GooglePubsubSubscriptionMessageTransformsJavascriptUdfOutputReference:
        return typing.cast(GooglePubsubSubscriptionMessageTransformsJavascriptUdfOutputReference, jsii.get(self, "javascriptUdf"))

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
    ) -> typing.Optional[GooglePubsubSubscriptionMessageTransformsJavascriptUdf]:
        return typing.cast(typing.Optional[GooglePubsubSubscriptionMessageTransformsJavascriptUdf], jsii.get(self, "javascriptUdfInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ec7ad358aaf0627bee735bee70b553217971a3bf9e682adaf8eaaf9f60a0d90d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePubsubSubscriptionMessageTransforms]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePubsubSubscriptionMessageTransforms]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePubsubSubscriptionMessageTransforms]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6437df6056b559d7daabb0f253198122784b233c477b8af7fb084d7374151ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionPushConfig",
    jsii_struct_bases=[],
    name_mapping={
        "push_endpoint": "pushEndpoint",
        "attributes": "attributes",
        "no_wrapper": "noWrapper",
        "oidc_token": "oidcToken",
    },
)
class GooglePubsubSubscriptionPushConfig:
    def __init__(
        self,
        *,
        push_endpoint: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        no_wrapper: typing.Optional[typing.Union["GooglePubsubSubscriptionPushConfigNoWrapper", typing.Dict[builtins.str, typing.Any]]] = None,
        oidc_token: typing.Optional[typing.Union["GooglePubsubSubscriptionPushConfigOidcToken", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param push_endpoint: A URL locating the endpoint to which messages should be pushed. For example, a Webhook endpoint might use "https://example.com/push". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#push_endpoint GooglePubsubSubscription#push_endpoint}
        :param attributes: Endpoint configuration attributes. Every endpoint has a set of API supported attributes that can be used to control different aspects of the message delivery. The currently supported attribute is x-goog-version, which you can use to change the format of the pushed message. This attribute indicates the version of the data expected by the endpoint. This controls the shape of the pushed message (i.e., its fields and metadata). The endpoint version is based on the version of the Pub/Sub API. If not present during the subscriptions.create call, it will default to the version of the API used to make such call. If not present during a subscriptions.modifyPushConfig call, its value will not be changed. subscriptions.get calls will always return a valid version, even if the subscription was created without this attribute. The possible values for this attribute are: - v1beta1: uses the push format defined in the v1beta1 Pub/Sub API. - v1 or v1beta2: uses the push format defined in the v1 Pub/Sub API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#attributes GooglePubsubSubscription#attributes}
        :param no_wrapper: no_wrapper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#no_wrapper GooglePubsubSubscription#no_wrapper}
        :param oidc_token: oidc_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#oidc_token GooglePubsubSubscription#oidc_token}
        '''
        if isinstance(no_wrapper, dict):
            no_wrapper = GooglePubsubSubscriptionPushConfigNoWrapper(**no_wrapper)
        if isinstance(oidc_token, dict):
            oidc_token = GooglePubsubSubscriptionPushConfigOidcToken(**oidc_token)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17391aa46e2a5f40791a30b368cda5ef42c31c65af44c06bb6471ba4e81e4d87)
            check_type(argname="argument push_endpoint", value=push_endpoint, expected_type=type_hints["push_endpoint"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument no_wrapper", value=no_wrapper, expected_type=type_hints["no_wrapper"])
            check_type(argname="argument oidc_token", value=oidc_token, expected_type=type_hints["oidc_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "push_endpoint": push_endpoint,
        }
        if attributes is not None:
            self._values["attributes"] = attributes
        if no_wrapper is not None:
            self._values["no_wrapper"] = no_wrapper
        if oidc_token is not None:
            self._values["oidc_token"] = oidc_token

    @builtins.property
    def push_endpoint(self) -> builtins.str:
        '''A URL locating the endpoint to which messages should be pushed. For example, a Webhook endpoint might use "https://example.com/push".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#push_endpoint GooglePubsubSubscription#push_endpoint}
        '''
        result = self._values.get("push_endpoint")
        assert result is not None, "Required property 'push_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Endpoint configuration attributes.

        Every endpoint has a set of API supported attributes that can
        be used to control different aspects of the message delivery.

        The currently supported attribute is x-goog-version, which you
        can use to change the format of the pushed message. This
        attribute indicates the version of the data expected by
        the endpoint. This controls the shape of the pushed message
        (i.e., its fields and metadata). The endpoint version is
        based on the version of the Pub/Sub API.

        If not present during the subscriptions.create call,
        it will default to the version of the API used to make
        such call. If not present during a subscriptions.modifyPushConfig
        call, its value will not be changed. subscriptions.get
        calls will always return a valid version, even if the
        subscription was created without this attribute.

        The possible values for this attribute are:

        - v1beta1: uses the push format defined in the v1beta1 Pub/Sub API.
        - v1 or v1beta2: uses the push format defined in the v1 Pub/Sub API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#attributes GooglePubsubSubscription#attributes}
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def no_wrapper(
        self,
    ) -> typing.Optional["GooglePubsubSubscriptionPushConfigNoWrapper"]:
        '''no_wrapper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#no_wrapper GooglePubsubSubscription#no_wrapper}
        '''
        result = self._values.get("no_wrapper")
        return typing.cast(typing.Optional["GooglePubsubSubscriptionPushConfigNoWrapper"], result)

    @builtins.property
    def oidc_token(
        self,
    ) -> typing.Optional["GooglePubsubSubscriptionPushConfigOidcToken"]:
        '''oidc_token block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#oidc_token GooglePubsubSubscription#oidc_token}
        '''
        result = self._values.get("oidc_token")
        return typing.cast(typing.Optional["GooglePubsubSubscriptionPushConfigOidcToken"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubSubscriptionPushConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionPushConfigNoWrapper",
    jsii_struct_bases=[],
    name_mapping={"write_metadata": "writeMetadata"},
)
class GooglePubsubSubscriptionPushConfigNoWrapper:
    def __init__(
        self,
        *,
        write_metadata: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param write_metadata: When true, writes the Pub/Sub message metadata to 'x-goog-pubsub-:' headers of the HTTP request. Writes the Pub/Sub message attributes to ':' headers of the HTTP request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#write_metadata GooglePubsubSubscription#write_metadata}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02d0b51c82a1f3cc153c5c5bea77049477fe23498931e37869d921ab5c7cb69b)
            check_type(argname="argument write_metadata", value=write_metadata, expected_type=type_hints["write_metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "write_metadata": write_metadata,
        }

    @builtins.property
    def write_metadata(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''When true, writes the Pub/Sub message metadata to 'x-goog-pubsub-:' headers of the HTTP request.

        Writes the
        Pub/Sub message attributes to ':' headers of the HTTP request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#write_metadata GooglePubsubSubscription#write_metadata}
        '''
        result = self._values.get("write_metadata")
        assert result is not None, "Required property 'write_metadata' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubSubscriptionPushConfigNoWrapper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubSubscriptionPushConfigNoWrapperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionPushConfigNoWrapperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c325c8c0bb4bdd2ead93a17dcc5c1384b21d1c603c65276a811a5d117a392828)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="writeMetadataInput")
    def write_metadata_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "writeMetadataInput"))

    @builtins.property
    @jsii.member(jsii_name="writeMetadata")
    def write_metadata(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "writeMetadata"))

    @write_metadata.setter
    def write_metadata(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7eda48dd77fc71314dd69a2c8a738249f035cb547bcb0c1a861e099bf2f2f28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeMetadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePubsubSubscriptionPushConfigNoWrapper]:
        return typing.cast(typing.Optional[GooglePubsubSubscriptionPushConfigNoWrapper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubSubscriptionPushConfigNoWrapper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__678618b6693b1f2ec32f6f04e8c76dc6363220c03d9cd26d11d842b860772c81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionPushConfigOidcToken",
    jsii_struct_bases=[],
    name_mapping={
        "service_account_email": "serviceAccountEmail",
        "audience": "audience",
    },
)
class GooglePubsubSubscriptionPushConfigOidcToken:
    def __init__(
        self,
        *,
        service_account_email: builtins.str,
        audience: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account_email: Service account email to be used for generating the OIDC token. The caller (for subscriptions.create, subscriptions.patch, and subscriptions.modifyPushConfig RPCs) must have the iam.serviceAccounts.actAs permission for the service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#service_account_email GooglePubsubSubscription#service_account_email}
        :param audience: Audience to be used when generating OIDC token. The audience claim identifies the recipients that the JWT is intended for. The audience value is a single case-sensitive string. Having multiple values (array) for the audience field is not supported. More info about the OIDC JWT token audience here: https://tools.ietf.org/html/rfc7519#section-4.1.3 Note: if not specified, the Push endpoint URL will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#audience GooglePubsubSubscription#audience}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d98286dbce6ecd7952bb4e9891249660150d45d6fb8e768b8f422f8ca24c1bd)
            check_type(argname="argument service_account_email", value=service_account_email, expected_type=type_hints["service_account_email"])
            check_type(argname="argument audience", value=audience, expected_type=type_hints["audience"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_account_email": service_account_email,
        }
        if audience is not None:
            self._values["audience"] = audience

    @builtins.property
    def service_account_email(self) -> builtins.str:
        '''Service account email to be used for generating the OIDC token.

        The caller (for subscriptions.create, subscriptions.patch, and
        subscriptions.modifyPushConfig RPCs) must have the
        iam.serviceAccounts.actAs permission for the service account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#service_account_email GooglePubsubSubscription#service_account_email}
        '''
        result = self._values.get("service_account_email")
        assert result is not None, "Required property 'service_account_email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def audience(self) -> typing.Optional[builtins.str]:
        '''Audience to be used when generating OIDC token.

        The audience claim
        identifies the recipients that the JWT is intended for. The audience
        value is a single case-sensitive string. Having multiple values (array)
        for the audience field is not supported. More info about the OIDC JWT
        token audience here: https://tools.ietf.org/html/rfc7519#section-4.1.3
        Note: if not specified, the Push endpoint URL will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#audience GooglePubsubSubscription#audience}
        '''
        result = self._values.get("audience")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubSubscriptionPushConfigOidcToken(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubSubscriptionPushConfigOidcTokenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionPushConfigOidcTokenOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98e1c6da0342752989dae30f62149e3f3484cf851a0db391a265218e7500269f)
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
    @jsii.member(jsii_name="serviceAccountEmailInput")
    def service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="audience")
    def audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audience"))

    @audience.setter
    def audience(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5ba57c319de89a6b523fa8610556ff93eeed472e2725c61006f4f957735676c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audience", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58cf587844289bbd6a463f2e7722e40fc8603b2f44cb2da8d0c00ce047e2bc0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePubsubSubscriptionPushConfigOidcToken]:
        return typing.cast(typing.Optional[GooglePubsubSubscriptionPushConfigOidcToken], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubSubscriptionPushConfigOidcToken],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c322dd1514bdff9e513fcaa01cfd94b78080ed26a98336d105696e51f8b8d5fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePubsubSubscriptionPushConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionPushConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__876d38cbbcf8558fb6ad955259e54bf4b973fe13d217934d3e95009c824349bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNoWrapper")
    def put_no_wrapper(
        self,
        *,
        write_metadata: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param write_metadata: When true, writes the Pub/Sub message metadata to 'x-goog-pubsub-:' headers of the HTTP request. Writes the Pub/Sub message attributes to ':' headers of the HTTP request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#write_metadata GooglePubsubSubscription#write_metadata}
        '''
        value = GooglePubsubSubscriptionPushConfigNoWrapper(
            write_metadata=write_metadata
        )

        return typing.cast(None, jsii.invoke(self, "putNoWrapper", [value]))

    @jsii.member(jsii_name="putOidcToken")
    def put_oidc_token(
        self,
        *,
        service_account_email: builtins.str,
        audience: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account_email: Service account email to be used for generating the OIDC token. The caller (for subscriptions.create, subscriptions.patch, and subscriptions.modifyPushConfig RPCs) must have the iam.serviceAccounts.actAs permission for the service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#service_account_email GooglePubsubSubscription#service_account_email}
        :param audience: Audience to be used when generating OIDC token. The audience claim identifies the recipients that the JWT is intended for. The audience value is a single case-sensitive string. Having multiple values (array) for the audience field is not supported. More info about the OIDC JWT token audience here: https://tools.ietf.org/html/rfc7519#section-4.1.3 Note: if not specified, the Push endpoint URL will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#audience GooglePubsubSubscription#audience}
        '''
        value = GooglePubsubSubscriptionPushConfigOidcToken(
            service_account_email=service_account_email, audience=audience
        )

        return typing.cast(None, jsii.invoke(self, "putOidcToken", [value]))

    @jsii.member(jsii_name="resetAttributes")
    def reset_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributes", []))

    @jsii.member(jsii_name="resetNoWrapper")
    def reset_no_wrapper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoWrapper", []))

    @jsii.member(jsii_name="resetOidcToken")
    def reset_oidc_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOidcToken", []))

    @builtins.property
    @jsii.member(jsii_name="noWrapper")
    def no_wrapper(self) -> GooglePubsubSubscriptionPushConfigNoWrapperOutputReference:
        return typing.cast(GooglePubsubSubscriptionPushConfigNoWrapperOutputReference, jsii.get(self, "noWrapper"))

    @builtins.property
    @jsii.member(jsii_name="oidcToken")
    def oidc_token(self) -> GooglePubsubSubscriptionPushConfigOidcTokenOutputReference:
        return typing.cast(GooglePubsubSubscriptionPushConfigOidcTokenOutputReference, jsii.get(self, "oidcToken"))

    @builtins.property
    @jsii.member(jsii_name="attributesInput")
    def attributes_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "attributesInput"))

    @builtins.property
    @jsii.member(jsii_name="noWrapperInput")
    def no_wrapper_input(
        self,
    ) -> typing.Optional[GooglePubsubSubscriptionPushConfigNoWrapper]:
        return typing.cast(typing.Optional[GooglePubsubSubscriptionPushConfigNoWrapper], jsii.get(self, "noWrapperInput"))

    @builtins.property
    @jsii.member(jsii_name="oidcTokenInput")
    def oidc_token_input(
        self,
    ) -> typing.Optional[GooglePubsubSubscriptionPushConfigOidcToken]:
        return typing.cast(typing.Optional[GooglePubsubSubscriptionPushConfigOidcToken], jsii.get(self, "oidcTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="pushEndpointInput")
    def push_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pushEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "attributes"))

    @attributes.setter
    def attributes(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92c1c9b2e704d4b1558740bace90380f7a889086db1951e9ff95d31f979da14f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pushEndpoint")
    def push_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pushEndpoint"))

    @push_endpoint.setter
    def push_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64c0ebe97f4a5c2c5b400109ab32a595680ffd9e219b264ef4cb21a85bf25e4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pushEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GooglePubsubSubscriptionPushConfig]:
        return typing.cast(typing.Optional[GooglePubsubSubscriptionPushConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubSubscriptionPushConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__892c7608a17f93cffa3f65c2f60f3ec57a5038a6656559421433d22a216d0f94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionRetryPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "maximum_backoff": "maximumBackoff",
        "minimum_backoff": "minimumBackoff",
    },
)
class GooglePubsubSubscriptionRetryPolicy:
    def __init__(
        self,
        *,
        maximum_backoff: typing.Optional[builtins.str] = None,
        minimum_backoff: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param maximum_backoff: The maximum delay between consecutive deliveries of a given message. Value should be between 0 and 600 seconds. Defaults to 600 seconds. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#maximum_backoff GooglePubsubSubscription#maximum_backoff}
        :param minimum_backoff: The minimum delay between consecutive deliveries of a given message. Value should be between 0 and 600 seconds. Defaults to 10 seconds. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#minimum_backoff GooglePubsubSubscription#minimum_backoff}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c43997a2f2bb29b9e529307b1ec0f95b2e19a9ff815f73c96e11a3e60464e6d)
            check_type(argname="argument maximum_backoff", value=maximum_backoff, expected_type=type_hints["maximum_backoff"])
            check_type(argname="argument minimum_backoff", value=minimum_backoff, expected_type=type_hints["minimum_backoff"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if maximum_backoff is not None:
            self._values["maximum_backoff"] = maximum_backoff
        if minimum_backoff is not None:
            self._values["minimum_backoff"] = minimum_backoff

    @builtins.property
    def maximum_backoff(self) -> typing.Optional[builtins.str]:
        '''The maximum delay between consecutive deliveries of a given message.

        Value should be between 0 and 600 seconds. Defaults to 600 seconds.
        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#maximum_backoff GooglePubsubSubscription#maximum_backoff}
        '''
        result = self._values.get("maximum_backoff")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum_backoff(self) -> typing.Optional[builtins.str]:
        '''The minimum delay between consecutive deliveries of a given message.

        Value should be between 0 and 600 seconds. Defaults to 10 seconds.
        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#minimum_backoff GooglePubsubSubscription#minimum_backoff}
        '''
        result = self._values.get("minimum_backoff")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubSubscriptionRetryPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubSubscriptionRetryPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionRetryPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f648d91c3b31504c60d86241cdf741f4fb71ac95f5e7f6313bf81f258f2da83c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaximumBackoff")
    def reset_maximum_backoff(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBackoff", []))

    @jsii.member(jsii_name="resetMinimumBackoff")
    def reset_minimum_backoff(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumBackoff", []))

    @builtins.property
    @jsii.member(jsii_name="maximumBackoffInput")
    def maximum_backoff_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maximumBackoffInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumBackoffInput")
    def minimum_backoff_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimumBackoffInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBackoff")
    def maximum_backoff(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maximumBackoff"))

    @maximum_backoff.setter
    def maximum_backoff(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3a5bd5fb6743262ee689de8407298f8a289db1111ddf0a76b3bfa6d9ba37fbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBackoff", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumBackoff")
    def minimum_backoff(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumBackoff"))

    @minimum_backoff.setter
    def minimum_backoff(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85cb162c31aa614db6b3264fddfb3361506244e0958831d027621ff8799c2928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumBackoff", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GooglePubsubSubscriptionRetryPolicy]:
        return typing.cast(typing.Optional[GooglePubsubSubscriptionRetryPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubSubscriptionRetryPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a48767a3f4b304b31649126b73edb20ded7ca0f390cca2241192e18c54e55d95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GooglePubsubSubscriptionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#create GooglePubsubSubscription#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#delete GooglePubsubSubscription#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#update GooglePubsubSubscription#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f5229b0d40be92d0345208361c3db1d575855b13226470e48557dc15c83d232)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#create GooglePubsubSubscription#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#delete GooglePubsubSubscription#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_subscription#update GooglePubsubSubscription#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubSubscriptionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubSubscriptionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubSubscription.GooglePubsubSubscriptionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8423e987dbf8867942e62df718009e58f48e1694d6382a082629e61c5d242273)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0298a884dac99a55eb69cc6647f79b8c602cf494d9127757a82322f4e75fe9f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63b9d47ff40bf1e0300289b6961a1987b78779d500e7a64bb712136f44c5e389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__508ed9db39e2abfa0ee8a7104fca0d4150839d828b316363f3caf6c9eaeb86d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePubsubSubscriptionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePubsubSubscriptionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePubsubSubscriptionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf2044dc961a4cca03c25ec5454b76806c6e366ace385e17fb27ef63927104de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GooglePubsubSubscription",
    "GooglePubsubSubscriptionBigqueryConfig",
    "GooglePubsubSubscriptionBigqueryConfigOutputReference",
    "GooglePubsubSubscriptionCloudStorageConfig",
    "GooglePubsubSubscriptionCloudStorageConfigAvroConfig",
    "GooglePubsubSubscriptionCloudStorageConfigAvroConfigOutputReference",
    "GooglePubsubSubscriptionCloudStorageConfigOutputReference",
    "GooglePubsubSubscriptionConfig",
    "GooglePubsubSubscriptionDeadLetterPolicy",
    "GooglePubsubSubscriptionDeadLetterPolicyOutputReference",
    "GooglePubsubSubscriptionExpirationPolicy",
    "GooglePubsubSubscriptionExpirationPolicyOutputReference",
    "GooglePubsubSubscriptionMessageTransforms",
    "GooglePubsubSubscriptionMessageTransformsJavascriptUdf",
    "GooglePubsubSubscriptionMessageTransformsJavascriptUdfOutputReference",
    "GooglePubsubSubscriptionMessageTransformsList",
    "GooglePubsubSubscriptionMessageTransformsOutputReference",
    "GooglePubsubSubscriptionPushConfig",
    "GooglePubsubSubscriptionPushConfigNoWrapper",
    "GooglePubsubSubscriptionPushConfigNoWrapperOutputReference",
    "GooglePubsubSubscriptionPushConfigOidcToken",
    "GooglePubsubSubscriptionPushConfigOidcTokenOutputReference",
    "GooglePubsubSubscriptionPushConfigOutputReference",
    "GooglePubsubSubscriptionRetryPolicy",
    "GooglePubsubSubscriptionRetryPolicyOutputReference",
    "GooglePubsubSubscriptionTimeouts",
    "GooglePubsubSubscriptionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c8e5e2e5996576cf888dc1e67c3f99fdb31177100884f076ee3e2cbc93c3d606(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    topic: builtins.str,
    ack_deadline_seconds: typing.Optional[jsii.Number] = None,
    bigquery_config: typing.Optional[typing.Union[GooglePubsubSubscriptionBigqueryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_storage_config: typing.Optional[typing.Union[GooglePubsubSubscriptionCloudStorageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_policy: typing.Optional[typing.Union[GooglePubsubSubscriptionDeadLetterPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_exactly_once_delivery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_message_ordering: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expiration_policy: typing.Optional[typing.Union[GooglePubsubSubscriptionExpirationPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    filter: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    message_retention_duration: typing.Optional[builtins.str] = None,
    message_transforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePubsubSubscriptionMessageTransforms, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    push_config: typing.Optional[typing.Union[GooglePubsubSubscriptionPushConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    retain_acked_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retry_policy: typing.Optional[typing.Union[GooglePubsubSubscriptionRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GooglePubsubSubscriptionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6800ad8af1f13d3ff7a8363d0fa11a9a2435952b06eedc89eb8d67f50255edbd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ddd90af02373bc0e3ef84e2695a29996458cf383e85e3134c1af50a10583c9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePubsubSubscriptionMessageTransforms, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c9b63499d1ad43964edc60d842d83299e4d8c096659116db7a1d611f75e1556(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4657d3337651687f779c0e5d0fdd93da5c4ca669258c9fa36a7c8eb1e411b467(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55493f2ce2d38aa9bc1cc777b2ce5bf67256514195a000dffb45c3a848f85265(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f858a06da9adf1723290dcf007d3e8dae63351bbc757e901be4c2cb99c002878(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c24d5013f509e5ff12b63dff8e1a4afe63c3b76defef41771d1b89814bef06d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3298fed324ba9fd73270f8f9497c1a812d9cd7c5f7aa45a74914a35fe4475c1b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f1d1aaef19b61ea46396a46ffd62f14ea393eef7b0fe87180d112316feb89aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9184886689f30cc2cdfc3d76ee8854fe0139f4f74891944333e4e21765e50cc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8d5bc87dcd601e7fa182c8a589ae038eedb4ad118b65a72aefef4ac9fcbfff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b578b164a885df21a49f89e7829940d52706a12541a49dacda21777d4f4de647(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__164632d697b7a72eecabeba6d73ab22230e250a68b800921671a78646964b610(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb37b3f100a29333fb603d0ddb035e561f7e82a3dc752479955bc12334d52c3a(
    *,
    table: builtins.str,
    drop_unknown_fields: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    service_account_email: typing.Optional[builtins.str] = None,
    use_table_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_topic_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    write_metadata: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6fced1a4a0041d6b46718aef3fbb322440075ecf83dc10ba817d5b146b19483(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a999d74942d1a015f3885b2bce920d2ed5cc443680cb67723fc759446678195(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c7bc2a3b0c394410422cf4379354cf559dffc6b30879ceb649ad6b091495463(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c1ddbb89fd9e90c7d1e58baea6faf6c243248f8a195b133734fcf0a2a4055a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97b0509b241a86b383844f68aae542b4d5128e513bb73a6c1136bab505fe978c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f6a7f079e6ea39b70a0bbdf309783a3f3d6e2134cc1584836c928fe44ad5566(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060af42cd66f38600743c8ed5e946b02950ca528fbb5777bce152b8b6e833cfd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123a26c8061e6ccbbecce2a1396bce8de5dce19770d1a87018ebf6c52f00d3dd(
    value: typing.Optional[GooglePubsubSubscriptionBigqueryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__956f7a8fbffda70685ed5546f850ac1d64a834c92cd77233ad4458f7918cac81(
    *,
    bucket: builtins.str,
    avro_config: typing.Optional[typing.Union[GooglePubsubSubscriptionCloudStorageConfigAvroConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    filename_datetime_format: typing.Optional[builtins.str] = None,
    filename_prefix: typing.Optional[builtins.str] = None,
    filename_suffix: typing.Optional[builtins.str] = None,
    max_bytes: typing.Optional[jsii.Number] = None,
    max_duration: typing.Optional[builtins.str] = None,
    max_messages: typing.Optional[jsii.Number] = None,
    service_account_email: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce914fe2fc859585d48051a0c037194150a422009b67956ea35a89ba6f60deaa(
    *,
    use_topic_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    write_metadata: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5066765ec7fd84be686cd5f45a42d1ead5cf7034c2406a23148e884d21fa61b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a239209820777560fe5c6d271f098efaec5be75a804d5a7c584bd4380876c559(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f707a3a24d8bbf7e6417f408df62472e7fe6de7d2a32183817bd509849011328(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34fa3463c7c2654b23f3d2d0b4e4f77ad4e77f30888540076532280a29226652(
    value: typing.Optional[GooglePubsubSubscriptionCloudStorageConfigAvroConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03a378002d42c40f5bbb4e1688da653dca467c2a987541e9394092cda6b006c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670cf9082cac48376016e75a3fb7b545f32d799d3ac7a3deca64c29735a88104(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c81650a119349668957bd97d7ceba3e9ccb22336fd4a8b23f362310c28c6c56d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11fe311ccb499ffa1c4c379ff589156c3f9d67fde4cd19b97cb70fe1fcc2ea7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b11feecd77c2e84db3f8f1e2b05559ce5cde7c2e9a1e3f0949c2dc0a5523ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f4fcf5a940c8321434895c23eb2517fa8476ed9e4c9bd0fa84978d2ece568e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__689d73a5ac0bdfc934e3ebfd25157283f8f44db54647637f6c5672d3da286abf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daaf96574e2fcdcf69eb91798b207f25c44e2d16ae8db01ea67dc47ffb51e0a9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9acf373d919651a977ac983697fc6c22f88c9c904ceaa8939464a85ff78ab37a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8df4d11e9291bc19592323cfd18a9e9b78fb97cb75ffabc60e6379aae9c13a8f(
    value: typing.Optional[GooglePubsubSubscriptionCloudStorageConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b55b4d96cae3109c0e47d0b0b8b4d72a35e617062e702f0ec8ebed7a037452ec(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    topic: builtins.str,
    ack_deadline_seconds: typing.Optional[jsii.Number] = None,
    bigquery_config: typing.Optional[typing.Union[GooglePubsubSubscriptionBigqueryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_storage_config: typing.Optional[typing.Union[GooglePubsubSubscriptionCloudStorageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_policy: typing.Optional[typing.Union[GooglePubsubSubscriptionDeadLetterPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_exactly_once_delivery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_message_ordering: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expiration_policy: typing.Optional[typing.Union[GooglePubsubSubscriptionExpirationPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    filter: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    message_retention_duration: typing.Optional[builtins.str] = None,
    message_transforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePubsubSubscriptionMessageTransforms, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    push_config: typing.Optional[typing.Union[GooglePubsubSubscriptionPushConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    retain_acked_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retry_policy: typing.Optional[typing.Union[GooglePubsubSubscriptionRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GooglePubsubSubscriptionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12f9afb36467f7e4955e968f01e0c823bfafaec12cfb802b51bf4a84caa56457(
    *,
    dead_letter_topic: typing.Optional[builtins.str] = None,
    max_delivery_attempts: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050f1e2bafac2a5962f748c7c79b1c67919c6f58a38938521d55bf2682940be2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3375c5cccdaf9cc47ed4836d50bd0d270e79e844f2e6f85a024d67d539eddbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b865b71fe0f74c7db804340a15c0c30b65e678517feb21014de5b9c88288b654(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e1f1f8cfc7632dba981273807c9659b3f9de73a956daaf45f7fd849dd0e693(
    value: typing.Optional[GooglePubsubSubscriptionDeadLetterPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f1f1505ee44f580e6bb5b50ac731d3317ca3409bbd4829ce51f9a2632e3d60(
    *,
    ttl: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b19fdcc876dcd95d8b9c5ec071fde407b01ffa98d0882bae2aa35eb22e59dc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5acc0b270cb18ccf3cdec7fe88bd2a30164dc199bb8fa0afd2f68e1b75530c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__389f25e77032782e5ba56204703eda6779eba3fdc83bc2a4ccfe95076001c02d(
    value: typing.Optional[GooglePubsubSubscriptionExpirationPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4812736d2ce8fa8bf1e3d9942e14366af9cd117ca703c55ea9b1aaef2aff15e2(
    *,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    javascript_udf: typing.Optional[typing.Union[GooglePubsubSubscriptionMessageTransformsJavascriptUdf, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3799025e08d62e1ea908ad28f0a5c512fb32247a1940d13a5f48042bd062a75(
    *,
    code: builtins.str,
    function_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cccff69a3fd078b90662a751a7ab7bf3a7ab261762727670c4ef90a648744567(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a02afce18b634c981fb412876e83a86a2b6f88bac7243076b95f1ada0fc82544(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e52b719ecea4312bbd91cde10b97d1ab109f33ac697a5b0869a30b2f24aa1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15e6a5806b1d7fc56b35dac02e6d79316f9939098084bd6ccc12d422f7bb8c9(
    value: typing.Optional[GooglePubsubSubscriptionMessageTransformsJavascriptUdf],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be17856dbc23abebb5cd5b359140e8ee8e8848afbcd9be24749479a4106e9e0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f80ae4db5137dd822b8b8447b894bac8753ddf1cc36ab3afec1a448ceaba20(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfdca579ffc24d2f95463d3a0019d662dcf802a386c99488a3fb7b14a232ae25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e758b8bb25b6e247f5d8bfbd645da05b156345ed4436030f26802918cf15d5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ceedcaff55083a79cacb248f4dda0284a1e912a9d3b23f2a4ba1e022c80be8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efb81ed8fa5533dab082775f620875eff08bba361e522c11c8a1def1306d3b76(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePubsubSubscriptionMessageTransforms]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d36b908827796f739577ba06b1de04cc78a2f6966f0c83e5df8790c219b0c502(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec7ad358aaf0627bee735bee70b553217971a3bf9e682adaf8eaaf9f60a0d90d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6437df6056b559d7daabb0f253198122784b233c477b8af7fb084d7374151ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePubsubSubscriptionMessageTransforms]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17391aa46e2a5f40791a30b368cda5ef42c31c65af44c06bb6471ba4e81e4d87(
    *,
    push_endpoint: builtins.str,
    attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    no_wrapper: typing.Optional[typing.Union[GooglePubsubSubscriptionPushConfigNoWrapper, typing.Dict[builtins.str, typing.Any]]] = None,
    oidc_token: typing.Optional[typing.Union[GooglePubsubSubscriptionPushConfigOidcToken, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02d0b51c82a1f3cc153c5c5bea77049477fe23498931e37869d921ab5c7cb69b(
    *,
    write_metadata: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c325c8c0bb4bdd2ead93a17dcc5c1384b21d1c603c65276a811a5d117a392828(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7eda48dd77fc71314dd69a2c8a738249f035cb547bcb0c1a861e099bf2f2f28(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__678618b6693b1f2ec32f6f04e8c76dc6363220c03d9cd26d11d842b860772c81(
    value: typing.Optional[GooglePubsubSubscriptionPushConfigNoWrapper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d98286dbce6ecd7952bb4e9891249660150d45d6fb8e768b8f422f8ca24c1bd(
    *,
    service_account_email: builtins.str,
    audience: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e1c6da0342752989dae30f62149e3f3484cf851a0db391a265218e7500269f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5ba57c319de89a6b523fa8610556ff93eeed472e2725c61006f4f957735676c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58cf587844289bbd6a463f2e7722e40fc8603b2f44cb2da8d0c00ce047e2bc0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c322dd1514bdff9e513fcaa01cfd94b78080ed26a98336d105696e51f8b8d5fa(
    value: typing.Optional[GooglePubsubSubscriptionPushConfigOidcToken],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876d38cbbcf8558fb6ad955259e54bf4b973fe13d217934d3e95009c824349bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c1c9b2e704d4b1558740bace90380f7a889086db1951e9ff95d31f979da14f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c0ebe97f4a5c2c5b400109ab32a595680ffd9e219b264ef4cb21a85bf25e4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__892c7608a17f93cffa3f65c2f60f3ec57a5038a6656559421433d22a216d0f94(
    value: typing.Optional[GooglePubsubSubscriptionPushConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c43997a2f2bb29b9e529307b1ec0f95b2e19a9ff815f73c96e11a3e60464e6d(
    *,
    maximum_backoff: typing.Optional[builtins.str] = None,
    minimum_backoff: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f648d91c3b31504c60d86241cdf741f4fb71ac95f5e7f6313bf81f258f2da83c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3a5bd5fb6743262ee689de8407298f8a289db1111ddf0a76b3bfa6d9ba37fbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85cb162c31aa614db6b3264fddfb3361506244e0958831d027621ff8799c2928(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a48767a3f4b304b31649126b73edb20ded7ca0f390cca2241192e18c54e55d95(
    value: typing.Optional[GooglePubsubSubscriptionRetryPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f5229b0d40be92d0345208361c3db1d575855b13226470e48557dc15c83d232(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8423e987dbf8867942e62df718009e58f48e1694d6382a082629e61c5d242273(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0298a884dac99a55eb69cc6647f79b8c602cf494d9127757a82322f4e75fe9f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63b9d47ff40bf1e0300289b6961a1987b78779d500e7a64bb712136f44c5e389(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__508ed9db39e2abfa0ee8a7104fca0d4150839d828b316363f3caf6c9eaeb86d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf2044dc961a4cca03c25ec5454b76806c6e366ace385e17fb27ef63927104de(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePubsubSubscriptionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
