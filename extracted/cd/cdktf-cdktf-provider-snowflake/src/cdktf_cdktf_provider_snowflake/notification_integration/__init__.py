r'''
# `snowflake_notification_integration`

Refer to the Terraform Registry for docs: [`snowflake_notification_integration`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration).
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


class NotificationIntegration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.notificationIntegration.NotificationIntegration",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration snowflake_notification_integration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        notification_provider: builtins.str,
        aws_sns_role_arn: typing.Optional[builtins.str] = None,
        aws_sns_topic_arn: typing.Optional[builtins.str] = None,
        aws_sqs_arn: typing.Optional[builtins.str] = None,
        aws_sqs_role_arn: typing.Optional[builtins.str] = None,
        azure_storage_queue_primary_uri: typing.Optional[builtins.str] = None,
        azure_tenant_id: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        direction: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcp_pubsub_subscription_name: typing.Optional[builtins.str] = None,
        gcp_pubsub_topic_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration snowflake_notification_integration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#name NotificationIntegration#name}.
        :param notification_provider: The third-party cloud message queuing service (supported values: AZURE_STORAGE_QUEUE, AWS_SNS, GCP_PUBSUB; AWS_SQS is deprecated and will be removed in the future provider versions) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#notification_provider NotificationIntegration#notification_provider}
        :param aws_sns_role_arn: AWS IAM role ARN for notification integration to assume. Required for AWS_SNS provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#aws_sns_role_arn NotificationIntegration#aws_sns_role_arn}
        :param aws_sns_topic_arn: AWS SNS Topic ARN for notification integration to connect to. Required for AWS_SNS provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#aws_sns_topic_arn NotificationIntegration#aws_sns_topic_arn}
        :param aws_sqs_arn: AWS SQS queue ARN for notification integration to connect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#aws_sqs_arn NotificationIntegration#aws_sqs_arn}
        :param aws_sqs_role_arn: AWS IAM role ARN for notification integration to assume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#aws_sqs_role_arn NotificationIntegration#aws_sqs_role_arn}
        :param azure_storage_queue_primary_uri: The queue ID for the Azure Queue Storage queue created for Event Grid notifications. Required for AZURE_STORAGE_QUEUE provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#azure_storage_queue_primary_uri NotificationIntegration#azure_storage_queue_primary_uri}
        :param azure_tenant_id: The ID of the Azure Active Directory tenant used for identity management. Required for AZURE_STORAGE_QUEUE provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#azure_tenant_id NotificationIntegration#azure_tenant_id}
        :param comment: A comment for the integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#comment NotificationIntegration#comment}
        :param direction: Direction of the cloud messaging with respect to Snowflake (required only for error notifications). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#direction NotificationIntegration#direction}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#enabled NotificationIntegration#enabled}.
        :param gcp_pubsub_subscription_name: The subscription id that Snowflake will listen to when using the GCP_PUBSUB provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#gcp_pubsub_subscription_name NotificationIntegration#gcp_pubsub_subscription_name}
        :param gcp_pubsub_topic_name: The topic id that Snowflake will use to push notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#gcp_pubsub_topic_name NotificationIntegration#gcp_pubsub_topic_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#id NotificationIntegration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param type: A type of integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#type NotificationIntegration#type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e36fa304f77865a7509990b6c34e2a03df3ed1ba3e006344fbe37ffcd99ba9b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NotificationIntegrationConfig(
            name=name,
            notification_provider=notification_provider,
            aws_sns_role_arn=aws_sns_role_arn,
            aws_sns_topic_arn=aws_sns_topic_arn,
            aws_sqs_arn=aws_sqs_arn,
            aws_sqs_role_arn=aws_sqs_role_arn,
            azure_storage_queue_primary_uri=azure_storage_queue_primary_uri,
            azure_tenant_id=azure_tenant_id,
            comment=comment,
            direction=direction,
            enabled=enabled,
            gcp_pubsub_subscription_name=gcp_pubsub_subscription_name,
            gcp_pubsub_topic_name=gcp_pubsub_topic_name,
            id=id,
            type=type,
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
        '''Generates CDKTF code for importing a NotificationIntegration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NotificationIntegration to import.
        :param import_from_id: The id of the existing NotificationIntegration that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NotificationIntegration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adfeb2800c8845cf7eaac3ba33ee9802c081e3e567e25f7f749d3aad27cb0afd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAwsSnsRoleArn")
    def reset_aws_sns_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsSnsRoleArn", []))

    @jsii.member(jsii_name="resetAwsSnsTopicArn")
    def reset_aws_sns_topic_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsSnsTopicArn", []))

    @jsii.member(jsii_name="resetAwsSqsArn")
    def reset_aws_sqs_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsSqsArn", []))

    @jsii.member(jsii_name="resetAwsSqsRoleArn")
    def reset_aws_sqs_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsSqsRoleArn", []))

    @jsii.member(jsii_name="resetAzureStorageQueuePrimaryUri")
    def reset_azure_storage_queue_primary_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureStorageQueuePrimaryUri", []))

    @jsii.member(jsii_name="resetAzureTenantId")
    def reset_azure_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureTenantId", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetDirection")
    def reset_direction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirection", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetGcpPubsubSubscriptionName")
    def reset_gcp_pubsub_subscription_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpPubsubSubscriptionName", []))

    @jsii.member(jsii_name="resetGcpPubsubTopicName")
    def reset_gcp_pubsub_topic_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpPubsubTopicName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

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
    @jsii.member(jsii_name="awsSnsExternalId")
    def aws_sns_external_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsSnsExternalId"))

    @builtins.property
    @jsii.member(jsii_name="awsSnsIamUserArn")
    def aws_sns_iam_user_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsSnsIamUserArn"))

    @builtins.property
    @jsii.member(jsii_name="awsSqsExternalId")
    def aws_sqs_external_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsSqsExternalId"))

    @builtins.property
    @jsii.member(jsii_name="awsSqsIamUserArn")
    def aws_sqs_iam_user_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsSqsIamUserArn"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="gcpPubsubServiceAccount")
    def gcp_pubsub_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpPubsubServiceAccount"))

    @builtins.property
    @jsii.member(jsii_name="awsSnsRoleArnInput")
    def aws_sns_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsSnsRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="awsSnsTopicArnInput")
    def aws_sns_topic_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsSnsTopicArnInput"))

    @builtins.property
    @jsii.member(jsii_name="awsSqsArnInput")
    def aws_sqs_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsSqsArnInput"))

    @builtins.property
    @jsii.member(jsii_name="awsSqsRoleArnInput")
    def aws_sqs_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsSqsRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="azureStorageQueuePrimaryUriInput")
    def azure_storage_queue_primary_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azureStorageQueuePrimaryUriInput"))

    @builtins.property
    @jsii.member(jsii_name="azureTenantIdInput")
    def azure_tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azureTenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="directionInput")
    def direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directionInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpPubsubSubscriptionNameInput")
    def gcp_pubsub_subscription_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcpPubsubSubscriptionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpPubsubTopicNameInput")
    def gcp_pubsub_topic_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcpPubsubTopicNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationProviderInput")
    def notification_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="awsSnsRoleArn")
    def aws_sns_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsSnsRoleArn"))

    @aws_sns_role_arn.setter
    def aws_sns_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2f98bdebe9e5169dd789ecb9875011f69aba7af46012e4b586f4a9fe0bd5fe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsSnsRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="awsSnsTopicArn")
    def aws_sns_topic_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsSnsTopicArn"))

    @aws_sns_topic_arn.setter
    def aws_sns_topic_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43a6dd0004ac85effd3406010993bee9d4d63c2a3eb24bebe9d116deb5a3d092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsSnsTopicArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="awsSqsArn")
    def aws_sqs_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsSqsArn"))

    @aws_sqs_arn.setter
    def aws_sqs_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e51987ffab04e1f211785511e180797f8a1e3256a0ba8c3549e8f845ad5d4f51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsSqsArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="awsSqsRoleArn")
    def aws_sqs_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsSqsRoleArn"))

    @aws_sqs_role_arn.setter
    def aws_sqs_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b57076ed8a076f97d3132051c934a010615331f8bb3990df8ae557134c36446d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsSqsRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="azureStorageQueuePrimaryUri")
    def azure_storage_queue_primary_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azureStorageQueuePrimaryUri"))

    @azure_storage_queue_primary_uri.setter
    def azure_storage_queue_primary_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89f21215fe5f87a4a9f0c1a27f90b7308f640eda587fd19977bca1db92855ef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureStorageQueuePrimaryUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="azureTenantId")
    def azure_tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azureTenantId"))

    @azure_tenant_id.setter
    def azure_tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09365c71d8115d52047951081268e6423af4fd02a5fd9bcff60568c154f26a79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureTenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf768a5a9d5cd44c86082448b4a2ad6e77a9e9f5ededbb90a33a6c52731ea45e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "direction"))

    @direction.setter
    def direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c6cee659dd69696e593e4b98d80ceba40b1fba5ec1bf0211f89852c44892590)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "direction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd5c943a2b061373bb99e3c19fb591b808a8edf68065ad3772312b53e725391e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcpPubsubSubscriptionName")
    def gcp_pubsub_subscription_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpPubsubSubscriptionName"))

    @gcp_pubsub_subscription_name.setter
    def gcp_pubsub_subscription_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1304cb4b82c1f2fc0f8ac075348678224186bb053468856d610a6986516169a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpPubsubSubscriptionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcpPubsubTopicName")
    def gcp_pubsub_topic_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpPubsubTopicName"))

    @gcp_pubsub_topic_name.setter
    def gcp_pubsub_topic_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4437a5d013cc980c0f1b17341f86e9f6a14e50871effc5fe952bcdb60c9097f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpPubsubTopicName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91778f49a3a7639527be3e740d0ae98f0b14fce7356dd4c5045ad431f282c36e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe5033c83565217f8d9f4f771f43f3a712c2bbddc29cbb0e935a6b635fd11b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationProvider")
    def notification_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationProvider"))

    @notification_provider.setter
    def notification_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc8440167f1fa3873b5f7c04302af4264185bbd0a892a7549a65c20a2542c780)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationProvider", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d10f9239064ab8c9c77b588e0d140aacd34a512b9deeaba1f77357d5bde94506)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.notificationIntegration.NotificationIntegrationConfig",
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
        "notification_provider": "notificationProvider",
        "aws_sns_role_arn": "awsSnsRoleArn",
        "aws_sns_topic_arn": "awsSnsTopicArn",
        "aws_sqs_arn": "awsSqsArn",
        "aws_sqs_role_arn": "awsSqsRoleArn",
        "azure_storage_queue_primary_uri": "azureStorageQueuePrimaryUri",
        "azure_tenant_id": "azureTenantId",
        "comment": "comment",
        "direction": "direction",
        "enabled": "enabled",
        "gcp_pubsub_subscription_name": "gcpPubsubSubscriptionName",
        "gcp_pubsub_topic_name": "gcpPubsubTopicName",
        "id": "id",
        "type": "type",
    },
)
class NotificationIntegrationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        notification_provider: builtins.str,
        aws_sns_role_arn: typing.Optional[builtins.str] = None,
        aws_sns_topic_arn: typing.Optional[builtins.str] = None,
        aws_sqs_arn: typing.Optional[builtins.str] = None,
        aws_sqs_role_arn: typing.Optional[builtins.str] = None,
        azure_storage_queue_primary_uri: typing.Optional[builtins.str] = None,
        azure_tenant_id: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        direction: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcp_pubsub_subscription_name: typing.Optional[builtins.str] = None,
        gcp_pubsub_topic_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#name NotificationIntegration#name}.
        :param notification_provider: The third-party cloud message queuing service (supported values: AZURE_STORAGE_QUEUE, AWS_SNS, GCP_PUBSUB; AWS_SQS is deprecated and will be removed in the future provider versions) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#notification_provider NotificationIntegration#notification_provider}
        :param aws_sns_role_arn: AWS IAM role ARN for notification integration to assume. Required for AWS_SNS provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#aws_sns_role_arn NotificationIntegration#aws_sns_role_arn}
        :param aws_sns_topic_arn: AWS SNS Topic ARN for notification integration to connect to. Required for AWS_SNS provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#aws_sns_topic_arn NotificationIntegration#aws_sns_topic_arn}
        :param aws_sqs_arn: AWS SQS queue ARN for notification integration to connect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#aws_sqs_arn NotificationIntegration#aws_sqs_arn}
        :param aws_sqs_role_arn: AWS IAM role ARN for notification integration to assume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#aws_sqs_role_arn NotificationIntegration#aws_sqs_role_arn}
        :param azure_storage_queue_primary_uri: The queue ID for the Azure Queue Storage queue created for Event Grid notifications. Required for AZURE_STORAGE_QUEUE provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#azure_storage_queue_primary_uri NotificationIntegration#azure_storage_queue_primary_uri}
        :param azure_tenant_id: The ID of the Azure Active Directory tenant used for identity management. Required for AZURE_STORAGE_QUEUE provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#azure_tenant_id NotificationIntegration#azure_tenant_id}
        :param comment: A comment for the integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#comment NotificationIntegration#comment}
        :param direction: Direction of the cloud messaging with respect to Snowflake (required only for error notifications). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#direction NotificationIntegration#direction}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#enabled NotificationIntegration#enabled}.
        :param gcp_pubsub_subscription_name: The subscription id that Snowflake will listen to when using the GCP_PUBSUB provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#gcp_pubsub_subscription_name NotificationIntegration#gcp_pubsub_subscription_name}
        :param gcp_pubsub_topic_name: The topic id that Snowflake will use to push notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#gcp_pubsub_topic_name NotificationIntegration#gcp_pubsub_topic_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#id NotificationIntegration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param type: A type of integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#type NotificationIntegration#type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c181187ccc249e55a6025eade78d9b867e0a26bb2ee2fb9ff6f0ec7d626fd9d8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument notification_provider", value=notification_provider, expected_type=type_hints["notification_provider"])
            check_type(argname="argument aws_sns_role_arn", value=aws_sns_role_arn, expected_type=type_hints["aws_sns_role_arn"])
            check_type(argname="argument aws_sns_topic_arn", value=aws_sns_topic_arn, expected_type=type_hints["aws_sns_topic_arn"])
            check_type(argname="argument aws_sqs_arn", value=aws_sqs_arn, expected_type=type_hints["aws_sqs_arn"])
            check_type(argname="argument aws_sqs_role_arn", value=aws_sqs_role_arn, expected_type=type_hints["aws_sqs_role_arn"])
            check_type(argname="argument azure_storage_queue_primary_uri", value=azure_storage_queue_primary_uri, expected_type=type_hints["azure_storage_queue_primary_uri"])
            check_type(argname="argument azure_tenant_id", value=azure_tenant_id, expected_type=type_hints["azure_tenant_id"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument gcp_pubsub_subscription_name", value=gcp_pubsub_subscription_name, expected_type=type_hints["gcp_pubsub_subscription_name"])
            check_type(argname="argument gcp_pubsub_topic_name", value=gcp_pubsub_topic_name, expected_type=type_hints["gcp_pubsub_topic_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "notification_provider": notification_provider,
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
        if aws_sns_role_arn is not None:
            self._values["aws_sns_role_arn"] = aws_sns_role_arn
        if aws_sns_topic_arn is not None:
            self._values["aws_sns_topic_arn"] = aws_sns_topic_arn
        if aws_sqs_arn is not None:
            self._values["aws_sqs_arn"] = aws_sqs_arn
        if aws_sqs_role_arn is not None:
            self._values["aws_sqs_role_arn"] = aws_sqs_role_arn
        if azure_storage_queue_primary_uri is not None:
            self._values["azure_storage_queue_primary_uri"] = azure_storage_queue_primary_uri
        if azure_tenant_id is not None:
            self._values["azure_tenant_id"] = azure_tenant_id
        if comment is not None:
            self._values["comment"] = comment
        if direction is not None:
            self._values["direction"] = direction
        if enabled is not None:
            self._values["enabled"] = enabled
        if gcp_pubsub_subscription_name is not None:
            self._values["gcp_pubsub_subscription_name"] = gcp_pubsub_subscription_name
        if gcp_pubsub_topic_name is not None:
            self._values["gcp_pubsub_topic_name"] = gcp_pubsub_topic_name
        if id is not None:
            self._values["id"] = id
        if type is not None:
            self._values["type"] = type

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#name NotificationIntegration#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def notification_provider(self) -> builtins.str:
        '''The third-party cloud message queuing service (supported values: AZURE_STORAGE_QUEUE, AWS_SNS, GCP_PUBSUB;

        AWS_SQS is deprecated and will be removed in the future provider versions)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#notification_provider NotificationIntegration#notification_provider}
        '''
        result = self._values.get("notification_provider")
        assert result is not None, "Required property 'notification_provider' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_sns_role_arn(self) -> typing.Optional[builtins.str]:
        '''AWS IAM role ARN for notification integration to assume. Required for AWS_SNS provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#aws_sns_role_arn NotificationIntegration#aws_sns_role_arn}
        '''
        result = self._values.get("aws_sns_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_sns_topic_arn(self) -> typing.Optional[builtins.str]:
        '''AWS SNS Topic ARN for notification integration to connect to. Required for AWS_SNS provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#aws_sns_topic_arn NotificationIntegration#aws_sns_topic_arn}
        '''
        result = self._values.get("aws_sns_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_sqs_arn(self) -> typing.Optional[builtins.str]:
        '''AWS SQS queue ARN for notification integration to connect to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#aws_sqs_arn NotificationIntegration#aws_sqs_arn}
        '''
        result = self._values.get("aws_sqs_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_sqs_role_arn(self) -> typing.Optional[builtins.str]:
        '''AWS IAM role ARN for notification integration to assume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#aws_sqs_role_arn NotificationIntegration#aws_sqs_role_arn}
        '''
        result = self._values.get("aws_sqs_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def azure_storage_queue_primary_uri(self) -> typing.Optional[builtins.str]:
        '''The queue ID for the Azure Queue Storage queue created for Event Grid notifications. Required for AZURE_STORAGE_QUEUE provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#azure_storage_queue_primary_uri NotificationIntegration#azure_storage_queue_primary_uri}
        '''
        result = self._values.get("azure_storage_queue_primary_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def azure_tenant_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Azure Active Directory tenant used for identity management. Required for AZURE_STORAGE_QUEUE provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#azure_tenant_id NotificationIntegration#azure_tenant_id}
        '''
        result = self._values.get("azure_tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''A comment for the integration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#comment NotificationIntegration#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def direction(self) -> typing.Optional[builtins.str]:
        '''Direction of the cloud messaging with respect to Snowflake (required only for error notifications).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#direction NotificationIntegration#direction}
        '''
        result = self._values.get("direction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#enabled NotificationIntegration#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcp_pubsub_subscription_name(self) -> typing.Optional[builtins.str]:
        '''The subscription id that Snowflake will listen to when using the GCP_PUBSUB provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#gcp_pubsub_subscription_name NotificationIntegration#gcp_pubsub_subscription_name}
        '''
        result = self._values.get("gcp_pubsub_subscription_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcp_pubsub_topic_name(self) -> typing.Optional[builtins.str]:
        '''The topic id that Snowflake will use to push notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#gcp_pubsub_topic_name NotificationIntegration#gcp_pubsub_topic_name}
        '''
        result = self._values.get("gcp_pubsub_topic_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#id NotificationIntegration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''A type of integration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/notification_integration#type NotificationIntegration#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotificationIntegrationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "NotificationIntegration",
    "NotificationIntegrationConfig",
]

publication.publish()

def _typecheckingstub__2e36fa304f77865a7509990b6c34e2a03df3ed1ba3e006344fbe37ffcd99ba9b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    notification_provider: builtins.str,
    aws_sns_role_arn: typing.Optional[builtins.str] = None,
    aws_sns_topic_arn: typing.Optional[builtins.str] = None,
    aws_sqs_arn: typing.Optional[builtins.str] = None,
    aws_sqs_role_arn: typing.Optional[builtins.str] = None,
    azure_storage_queue_primary_uri: typing.Optional[builtins.str] = None,
    azure_tenant_id: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    direction: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcp_pubsub_subscription_name: typing.Optional[builtins.str] = None,
    gcp_pubsub_topic_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__adfeb2800c8845cf7eaac3ba33ee9802c081e3e567e25f7f749d3aad27cb0afd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f98bdebe9e5169dd789ecb9875011f69aba7af46012e4b586f4a9fe0bd5fe0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a6dd0004ac85effd3406010993bee9d4d63c2a3eb24bebe9d116deb5a3d092(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e51987ffab04e1f211785511e180797f8a1e3256a0ba8c3549e8f845ad5d4f51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b57076ed8a076f97d3132051c934a010615331f8bb3990df8ae557134c36446d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f21215fe5f87a4a9f0c1a27f90b7308f640eda587fd19977bca1db92855ef5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09365c71d8115d52047951081268e6423af4fd02a5fd9bcff60568c154f26a79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf768a5a9d5cd44c86082448b4a2ad6e77a9e9f5ededbb90a33a6c52731ea45e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c6cee659dd69696e593e4b98d80ceba40b1fba5ec1bf0211f89852c44892590(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd5c943a2b061373bb99e3c19fb591b808a8edf68065ad3772312b53e725391e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1304cb4b82c1f2fc0f8ac075348678224186bb053468856d610a6986516169a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4437a5d013cc980c0f1b17341f86e9f6a14e50871effc5fe952bcdb60c9097f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91778f49a3a7639527be3e740d0ae98f0b14fce7356dd4c5045ad431f282c36e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe5033c83565217f8d9f4f771f43f3a712c2bbddc29cbb0e935a6b635fd11b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8440167f1fa3873b5f7c04302af4264185bbd0a892a7549a65c20a2542c780(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d10f9239064ab8c9c77b588e0d140aacd34a512b9deeaba1f77357d5bde94506(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c181187ccc249e55a6025eade78d9b867e0a26bb2ee2fb9ff6f0ec7d626fd9d8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    notification_provider: builtins.str,
    aws_sns_role_arn: typing.Optional[builtins.str] = None,
    aws_sns_topic_arn: typing.Optional[builtins.str] = None,
    aws_sqs_arn: typing.Optional[builtins.str] = None,
    aws_sqs_role_arn: typing.Optional[builtins.str] = None,
    azure_storage_queue_primary_uri: typing.Optional[builtins.str] = None,
    azure_tenant_id: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    direction: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcp_pubsub_subscription_name: typing.Optional[builtins.str] = None,
    gcp_pubsub_topic_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
