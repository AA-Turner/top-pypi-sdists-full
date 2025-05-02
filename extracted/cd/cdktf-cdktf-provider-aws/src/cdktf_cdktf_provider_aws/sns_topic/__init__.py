r'''
# `aws_sns_topic`

Refer to the Terraform Registry for docs: [`aws_sns_topic`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic).
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


class SnsTopic(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.snsTopic.SnsTopic",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic aws_sns_topic}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        application_failure_feedback_role_arn: typing.Optional[builtins.str] = None,
        application_success_feedback_role_arn: typing.Optional[builtins.str] = None,
        application_success_feedback_sample_rate: typing.Optional[jsii.Number] = None,
        archive_policy: typing.Optional[builtins.str] = None,
        content_based_deduplication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delivery_policy: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        fifo_topic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        firehose_failure_feedback_role_arn: typing.Optional[builtins.str] = None,
        firehose_success_feedback_role_arn: typing.Optional[builtins.str] = None,
        firehose_success_feedback_sample_rate: typing.Optional[jsii.Number] = None,
        http_failure_feedback_role_arn: typing.Optional[builtins.str] = None,
        http_success_feedback_role_arn: typing.Optional[builtins.str] = None,
        http_success_feedback_sample_rate: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        kms_master_key_id: typing.Optional[builtins.str] = None,
        lambda_failure_feedback_role_arn: typing.Optional[builtins.str] = None,
        lambda_success_feedback_role_arn: typing.Optional[builtins.str] = None,
        lambda_success_feedback_sample_rate: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        signature_version: typing.Optional[jsii.Number] = None,
        sqs_failure_feedback_role_arn: typing.Optional[builtins.str] = None,
        sqs_success_feedback_role_arn: typing.Optional[builtins.str] = None,
        sqs_success_feedback_sample_rate: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tracing_config: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic aws_sns_topic} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param application_failure_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#application_failure_feedback_role_arn SnsTopic#application_failure_feedback_role_arn}.
        :param application_success_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#application_success_feedback_role_arn SnsTopic#application_success_feedback_role_arn}.
        :param application_success_feedback_sample_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#application_success_feedback_sample_rate SnsTopic#application_success_feedback_sample_rate}.
        :param archive_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#archive_policy SnsTopic#archive_policy}.
        :param content_based_deduplication: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#content_based_deduplication SnsTopic#content_based_deduplication}.
        :param delivery_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#delivery_policy SnsTopic#delivery_policy}.
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#display_name SnsTopic#display_name}.
        :param fifo_topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#fifo_topic SnsTopic#fifo_topic}.
        :param firehose_failure_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#firehose_failure_feedback_role_arn SnsTopic#firehose_failure_feedback_role_arn}.
        :param firehose_success_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#firehose_success_feedback_role_arn SnsTopic#firehose_success_feedback_role_arn}.
        :param firehose_success_feedback_sample_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#firehose_success_feedback_sample_rate SnsTopic#firehose_success_feedback_sample_rate}.
        :param http_failure_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#http_failure_feedback_role_arn SnsTopic#http_failure_feedback_role_arn}.
        :param http_success_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#http_success_feedback_role_arn SnsTopic#http_success_feedback_role_arn}.
        :param http_success_feedback_sample_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#http_success_feedback_sample_rate SnsTopic#http_success_feedback_sample_rate}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#id SnsTopic#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_master_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#kms_master_key_id SnsTopic#kms_master_key_id}.
        :param lambda_failure_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#lambda_failure_feedback_role_arn SnsTopic#lambda_failure_feedback_role_arn}.
        :param lambda_success_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#lambda_success_feedback_role_arn SnsTopic#lambda_success_feedback_role_arn}.
        :param lambda_success_feedback_sample_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#lambda_success_feedback_sample_rate SnsTopic#lambda_success_feedback_sample_rate}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#name SnsTopic#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#name_prefix SnsTopic#name_prefix}.
        :param policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#policy SnsTopic#policy}.
        :param signature_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#signature_version SnsTopic#signature_version}.
        :param sqs_failure_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#sqs_failure_feedback_role_arn SnsTopic#sqs_failure_feedback_role_arn}.
        :param sqs_success_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#sqs_success_feedback_role_arn SnsTopic#sqs_success_feedback_role_arn}.
        :param sqs_success_feedback_sample_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#sqs_success_feedback_sample_rate SnsTopic#sqs_success_feedback_sample_rate}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#tags SnsTopic#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#tags_all SnsTopic#tags_all}.
        :param tracing_config: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#tracing_config SnsTopic#tracing_config}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31d974c6ea71caa64a711d716c588e5eeff5b2ebec265d618be2572dcd34e00)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SnsTopicConfig(
            application_failure_feedback_role_arn=application_failure_feedback_role_arn,
            application_success_feedback_role_arn=application_success_feedback_role_arn,
            application_success_feedback_sample_rate=application_success_feedback_sample_rate,
            archive_policy=archive_policy,
            content_based_deduplication=content_based_deduplication,
            delivery_policy=delivery_policy,
            display_name=display_name,
            fifo_topic=fifo_topic,
            firehose_failure_feedback_role_arn=firehose_failure_feedback_role_arn,
            firehose_success_feedback_role_arn=firehose_success_feedback_role_arn,
            firehose_success_feedback_sample_rate=firehose_success_feedback_sample_rate,
            http_failure_feedback_role_arn=http_failure_feedback_role_arn,
            http_success_feedback_role_arn=http_success_feedback_role_arn,
            http_success_feedback_sample_rate=http_success_feedback_sample_rate,
            id=id,
            kms_master_key_id=kms_master_key_id,
            lambda_failure_feedback_role_arn=lambda_failure_feedback_role_arn,
            lambda_success_feedback_role_arn=lambda_success_feedback_role_arn,
            lambda_success_feedback_sample_rate=lambda_success_feedback_sample_rate,
            name=name,
            name_prefix=name_prefix,
            policy=policy,
            signature_version=signature_version,
            sqs_failure_feedback_role_arn=sqs_failure_feedback_role_arn,
            sqs_success_feedback_role_arn=sqs_success_feedback_role_arn,
            sqs_success_feedback_sample_rate=sqs_success_feedback_sample_rate,
            tags=tags,
            tags_all=tags_all,
            tracing_config=tracing_config,
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
        '''Generates CDKTF code for importing a SnsTopic resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SnsTopic to import.
        :param import_from_id: The id of the existing SnsTopic that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SnsTopic to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cb4335cdc9fb574dcafbc0c67ed3822e61bbdd6ee894251c49e555485d83cf3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetApplicationFailureFeedbackRoleArn")
    def reset_application_failure_feedback_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationFailureFeedbackRoleArn", []))

    @jsii.member(jsii_name="resetApplicationSuccessFeedbackRoleArn")
    def reset_application_success_feedback_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationSuccessFeedbackRoleArn", []))

    @jsii.member(jsii_name="resetApplicationSuccessFeedbackSampleRate")
    def reset_application_success_feedback_sample_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationSuccessFeedbackSampleRate", []))

    @jsii.member(jsii_name="resetArchivePolicy")
    def reset_archive_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchivePolicy", []))

    @jsii.member(jsii_name="resetContentBasedDeduplication")
    def reset_content_based_deduplication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentBasedDeduplication", []))

    @jsii.member(jsii_name="resetDeliveryPolicy")
    def reset_delivery_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeliveryPolicy", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetFifoTopic")
    def reset_fifo_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFifoTopic", []))

    @jsii.member(jsii_name="resetFirehoseFailureFeedbackRoleArn")
    def reset_firehose_failure_feedback_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirehoseFailureFeedbackRoleArn", []))

    @jsii.member(jsii_name="resetFirehoseSuccessFeedbackRoleArn")
    def reset_firehose_success_feedback_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirehoseSuccessFeedbackRoleArn", []))

    @jsii.member(jsii_name="resetFirehoseSuccessFeedbackSampleRate")
    def reset_firehose_success_feedback_sample_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirehoseSuccessFeedbackSampleRate", []))

    @jsii.member(jsii_name="resetHttpFailureFeedbackRoleArn")
    def reset_http_failure_feedback_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpFailureFeedbackRoleArn", []))

    @jsii.member(jsii_name="resetHttpSuccessFeedbackRoleArn")
    def reset_http_success_feedback_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpSuccessFeedbackRoleArn", []))

    @jsii.member(jsii_name="resetHttpSuccessFeedbackSampleRate")
    def reset_http_success_feedback_sample_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpSuccessFeedbackSampleRate", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsMasterKeyId")
    def reset_kms_master_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsMasterKeyId", []))

    @jsii.member(jsii_name="resetLambdaFailureFeedbackRoleArn")
    def reset_lambda_failure_feedback_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaFailureFeedbackRoleArn", []))

    @jsii.member(jsii_name="resetLambdaSuccessFeedbackRoleArn")
    def reset_lambda_success_feedback_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaSuccessFeedbackRoleArn", []))

    @jsii.member(jsii_name="resetLambdaSuccessFeedbackSampleRate")
    def reset_lambda_success_feedback_sample_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaSuccessFeedbackSampleRate", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNamePrefix")
    def reset_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamePrefix", []))

    @jsii.member(jsii_name="resetPolicy")
    def reset_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicy", []))

    @jsii.member(jsii_name="resetSignatureVersion")
    def reset_signature_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignatureVersion", []))

    @jsii.member(jsii_name="resetSqsFailureFeedbackRoleArn")
    def reset_sqs_failure_feedback_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqsFailureFeedbackRoleArn", []))

    @jsii.member(jsii_name="resetSqsSuccessFeedbackRoleArn")
    def reset_sqs_success_feedback_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqsSuccessFeedbackRoleArn", []))

    @jsii.member(jsii_name="resetSqsSuccessFeedbackSampleRate")
    def reset_sqs_success_feedback_sample_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqsSuccessFeedbackSampleRate", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTracingConfig")
    def reset_tracing_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTracingConfig", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="beginningArchiveTime")
    def beginning_archive_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "beginningArchiveTime"))

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="applicationFailureFeedbackRoleArnInput")
    def application_failure_feedback_role_arn_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationFailureFeedbackRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationSuccessFeedbackRoleArnInput")
    def application_success_feedback_role_arn_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationSuccessFeedbackRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationSuccessFeedbackSampleRateInput")
    def application_success_feedback_sample_rate_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "applicationSuccessFeedbackSampleRateInput"))

    @builtins.property
    @jsii.member(jsii_name="archivePolicyInput")
    def archive_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "archivePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="contentBasedDeduplicationInput")
    def content_based_deduplication_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "contentBasedDeduplicationInput"))

    @builtins.property
    @jsii.member(jsii_name="deliveryPolicyInput")
    def delivery_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deliveryPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="fifoTopicInput")
    def fifo_topic_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fifoTopicInput"))

    @builtins.property
    @jsii.member(jsii_name="firehoseFailureFeedbackRoleArnInput")
    def firehose_failure_feedback_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firehoseFailureFeedbackRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="firehoseSuccessFeedbackRoleArnInput")
    def firehose_success_feedback_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firehoseSuccessFeedbackRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="firehoseSuccessFeedbackSampleRateInput")
    def firehose_success_feedback_sample_rate_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "firehoseSuccessFeedbackSampleRateInput"))

    @builtins.property
    @jsii.member(jsii_name="httpFailureFeedbackRoleArnInput")
    def http_failure_feedback_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpFailureFeedbackRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="httpSuccessFeedbackRoleArnInput")
    def http_success_feedback_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpSuccessFeedbackRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="httpSuccessFeedbackSampleRateInput")
    def http_success_feedback_sample_rate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "httpSuccessFeedbackSampleRateInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsMasterKeyIdInput")
    def kms_master_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsMasterKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFailureFeedbackRoleArnInput")
    def lambda_failure_feedback_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lambdaFailureFeedbackRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaSuccessFeedbackRoleArnInput")
    def lambda_success_feedback_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lambdaSuccessFeedbackRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaSuccessFeedbackSampleRateInput")
    def lambda_success_feedback_sample_rate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lambdaSuccessFeedbackSampleRateInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namePrefixInput")
    def name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyInput"))

    @builtins.property
    @jsii.member(jsii_name="signatureVersionInput")
    def signature_version_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "signatureVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="sqsFailureFeedbackRoleArnInput")
    def sqs_failure_feedback_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqsFailureFeedbackRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sqsSuccessFeedbackRoleArnInput")
    def sqs_success_feedback_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqsSuccessFeedbackRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sqsSuccessFeedbackSampleRateInput")
    def sqs_success_feedback_sample_rate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sqsSuccessFeedbackSampleRateInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="tracingConfigInput")
    def tracing_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tracingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationFailureFeedbackRoleArn")
    def application_failure_feedback_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationFailureFeedbackRoleArn"))

    @application_failure_feedback_role_arn.setter
    def application_failure_feedback_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__209c9a6632e66d72eaad3133afd7a9ee2fb9537e53bbe9730b9eaa0d1aa48a01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationFailureFeedbackRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationSuccessFeedbackRoleArn")
    def application_success_feedback_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationSuccessFeedbackRoleArn"))

    @application_success_feedback_role_arn.setter
    def application_success_feedback_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2d21ecdaf367a0ea9aff64c831987f29a33a69140307eaf6b11c99148b7d386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationSuccessFeedbackRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationSuccessFeedbackSampleRate")
    def application_success_feedback_sample_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "applicationSuccessFeedbackSampleRate"))

    @application_success_feedback_sample_rate.setter
    def application_success_feedback_sample_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f376de287d2b2ffdbe6d9d4e507b35a9703fe8bce9d6d3991e7943cc64785964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationSuccessFeedbackSampleRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="archivePolicy")
    def archive_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "archivePolicy"))

    @archive_policy.setter
    def archive_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3f2c18da6289d665c1454ef81a86e271bf99ecdaa512b3827cdaca2b61a5327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archivePolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentBasedDeduplication")
    def content_based_deduplication(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "contentBasedDeduplication"))

    @content_based_deduplication.setter
    def content_based_deduplication(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__872bb23db6a948f3b6aa7be812a272c332a14dfa8fa31c3249ff11c3b68c6557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentBasedDeduplication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deliveryPolicy")
    def delivery_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deliveryPolicy"))

    @delivery_policy.setter
    def delivery_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4988912db5c472b1d8058f12c4bec0309c8de9f08413dee81a988945aa3510b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deliveryPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb829546d974309e9de64bdd26dd34c8b5ea72c73fce7e5144f255846371a782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fifoTopic")
    def fifo_topic(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fifoTopic"))

    @fifo_topic.setter
    def fifo_topic(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a08b9474f67cdea7dc0b187634bad405ea903ed1417593cbbc8c5fe98295055)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fifoTopic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firehoseFailureFeedbackRoleArn")
    def firehose_failure_feedback_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firehoseFailureFeedbackRoleArn"))

    @firehose_failure_feedback_role_arn.setter
    def firehose_failure_feedback_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e9758d57bbf177e76a310e78bd4174002f115c25b7a6fd5fd9d1eda43507193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firehoseFailureFeedbackRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firehoseSuccessFeedbackRoleArn")
    def firehose_success_feedback_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firehoseSuccessFeedbackRoleArn"))

    @firehose_success_feedback_role_arn.setter
    def firehose_success_feedback_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c15ab22d6a690f01b57773f1a906a691fba08c82e99656c72f4fc342aad6aaf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firehoseSuccessFeedbackRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firehoseSuccessFeedbackSampleRate")
    def firehose_success_feedback_sample_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "firehoseSuccessFeedbackSampleRate"))

    @firehose_success_feedback_sample_rate.setter
    def firehose_success_feedback_sample_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a406f317de0423f00e86371e779fed8337ef3eaf9330ac68fe38d484b93aba75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firehoseSuccessFeedbackSampleRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpFailureFeedbackRoleArn")
    def http_failure_feedback_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpFailureFeedbackRoleArn"))

    @http_failure_feedback_role_arn.setter
    def http_failure_feedback_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0290006c0f76a65e6d05c141186edcb832f140ddde72db1555424ed0ea6e632)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpFailureFeedbackRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpSuccessFeedbackRoleArn")
    def http_success_feedback_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpSuccessFeedbackRoleArn"))

    @http_success_feedback_role_arn.setter
    def http_success_feedback_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e66eb082ec520f94db5fd47cb1b4c1bab2dd7a53bce1198b5fca126ebcb32334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpSuccessFeedbackRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpSuccessFeedbackSampleRate")
    def http_success_feedback_sample_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "httpSuccessFeedbackSampleRate"))

    @http_success_feedback_sample_rate.setter
    def http_success_feedback_sample_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3783deecc4601a5afe714aea626c8a7287433920215cf6ef08ea8f017981a2f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpSuccessFeedbackSampleRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8f82783ccc7884a497aa38cb91f722356202eb5e94112654282b04650d15fd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsMasterKeyId")
    def kms_master_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsMasterKeyId"))

    @kms_master_key_id.setter
    def kms_master_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38f42697b95d3fec35fb87f496cae98c32ce3fc4ed336dd6c6c57c49099c454d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsMasterKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lambdaFailureFeedbackRoleArn")
    def lambda_failure_feedback_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lambdaFailureFeedbackRoleArn"))

    @lambda_failure_feedback_role_arn.setter
    def lambda_failure_feedback_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f6fb0ecac5220fba553d1bc3f7395f770e570225e979fb61a5a6491c873299a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaFailureFeedbackRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lambdaSuccessFeedbackRoleArn")
    def lambda_success_feedback_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lambdaSuccessFeedbackRoleArn"))

    @lambda_success_feedback_role_arn.setter
    def lambda_success_feedback_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca4dfa071f58bd7fdce2b0821d1fc1e2fac71850328aae744a7a3dabe41ce039)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaSuccessFeedbackRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lambdaSuccessFeedbackSampleRate")
    def lambda_success_feedback_sample_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lambdaSuccessFeedbackSampleRate"))

    @lambda_success_feedback_sample_rate.setter
    def lambda_success_feedback_sample_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__991bbea634d926bd6dd663cc7f1f0236c9d05fe4c1f46db1605c1fbeabd39fd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaSuccessFeedbackSampleRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbf747f8893433d3e218e528fa5e615aa2d957ca860e01f6d5d20d5348edf3b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namePrefix")
    def name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePrefix"))

    @name_prefix.setter
    def name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__564d4f6deda5b90181b17f89c76460a0c4bb3fe202841858efa39aa51020559c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c8b6384c702533fa37720c2163ca0ff75307519d0e21b7ce605504fd20089b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signatureVersion")
    def signature_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "signatureVersion"))

    @signature_version.setter
    def signature_version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c978e1a46c5436825bc6c5d7cfe02170977b87c413d35c2911c3a6b62a69324)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signatureVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqsFailureFeedbackRoleArn")
    def sqs_failure_feedback_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqsFailureFeedbackRoleArn"))

    @sqs_failure_feedback_role_arn.setter
    def sqs_failure_feedback_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d040a9d6d859b314c610a91d9d3974377637a4f537d274c9f29c493f8f4f9464)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqsFailureFeedbackRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqsSuccessFeedbackRoleArn")
    def sqs_success_feedback_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqsSuccessFeedbackRoleArn"))

    @sqs_success_feedback_role_arn.setter
    def sqs_success_feedback_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd77ca7faa749a8295ed0a9f9b42c104e2bc4ca1200d426dc796a771aba423d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqsSuccessFeedbackRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqsSuccessFeedbackSampleRate")
    def sqs_success_feedback_sample_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sqsSuccessFeedbackSampleRate"))

    @sqs_success_feedback_sample_rate.setter
    def sqs_success_feedback_sample_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e666c188e3a87866a4ddbe2b02dd9d510e892836bce49a6971913d1916632a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqsSuccessFeedbackSampleRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__290e4bf3d0b32b24e20b0669cd45b883111335a4fcc0cd209fa14a552ae7a452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61b3b958aee2a055563031b04e6ae253266d402dbd5f85f68e4cc20366dcfc46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tracingConfig")
    def tracing_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tracingConfig"))

    @tracing_config.setter
    def tracing_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3f3de9101974a9d55cc838130a9508701e31aedc1127a2d382e36b4df4af95c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tracingConfig", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.snsTopic.SnsTopicConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "application_failure_feedback_role_arn": "applicationFailureFeedbackRoleArn",
        "application_success_feedback_role_arn": "applicationSuccessFeedbackRoleArn",
        "application_success_feedback_sample_rate": "applicationSuccessFeedbackSampleRate",
        "archive_policy": "archivePolicy",
        "content_based_deduplication": "contentBasedDeduplication",
        "delivery_policy": "deliveryPolicy",
        "display_name": "displayName",
        "fifo_topic": "fifoTopic",
        "firehose_failure_feedback_role_arn": "firehoseFailureFeedbackRoleArn",
        "firehose_success_feedback_role_arn": "firehoseSuccessFeedbackRoleArn",
        "firehose_success_feedback_sample_rate": "firehoseSuccessFeedbackSampleRate",
        "http_failure_feedback_role_arn": "httpFailureFeedbackRoleArn",
        "http_success_feedback_role_arn": "httpSuccessFeedbackRoleArn",
        "http_success_feedback_sample_rate": "httpSuccessFeedbackSampleRate",
        "id": "id",
        "kms_master_key_id": "kmsMasterKeyId",
        "lambda_failure_feedback_role_arn": "lambdaFailureFeedbackRoleArn",
        "lambda_success_feedback_role_arn": "lambdaSuccessFeedbackRoleArn",
        "lambda_success_feedback_sample_rate": "lambdaSuccessFeedbackSampleRate",
        "name": "name",
        "name_prefix": "namePrefix",
        "policy": "policy",
        "signature_version": "signatureVersion",
        "sqs_failure_feedback_role_arn": "sqsFailureFeedbackRoleArn",
        "sqs_success_feedback_role_arn": "sqsSuccessFeedbackRoleArn",
        "sqs_success_feedback_sample_rate": "sqsSuccessFeedbackSampleRate",
        "tags": "tags",
        "tags_all": "tagsAll",
        "tracing_config": "tracingConfig",
    },
)
class SnsTopicConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        application_failure_feedback_role_arn: typing.Optional[builtins.str] = None,
        application_success_feedback_role_arn: typing.Optional[builtins.str] = None,
        application_success_feedback_sample_rate: typing.Optional[jsii.Number] = None,
        archive_policy: typing.Optional[builtins.str] = None,
        content_based_deduplication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delivery_policy: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        fifo_topic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        firehose_failure_feedback_role_arn: typing.Optional[builtins.str] = None,
        firehose_success_feedback_role_arn: typing.Optional[builtins.str] = None,
        firehose_success_feedback_sample_rate: typing.Optional[jsii.Number] = None,
        http_failure_feedback_role_arn: typing.Optional[builtins.str] = None,
        http_success_feedback_role_arn: typing.Optional[builtins.str] = None,
        http_success_feedback_sample_rate: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        kms_master_key_id: typing.Optional[builtins.str] = None,
        lambda_failure_feedback_role_arn: typing.Optional[builtins.str] = None,
        lambda_success_feedback_role_arn: typing.Optional[builtins.str] = None,
        lambda_success_feedback_sample_rate: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        signature_version: typing.Optional[jsii.Number] = None,
        sqs_failure_feedback_role_arn: typing.Optional[builtins.str] = None,
        sqs_success_feedback_role_arn: typing.Optional[builtins.str] = None,
        sqs_success_feedback_sample_rate: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tracing_config: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param application_failure_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#application_failure_feedback_role_arn SnsTopic#application_failure_feedback_role_arn}.
        :param application_success_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#application_success_feedback_role_arn SnsTopic#application_success_feedback_role_arn}.
        :param application_success_feedback_sample_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#application_success_feedback_sample_rate SnsTopic#application_success_feedback_sample_rate}.
        :param archive_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#archive_policy SnsTopic#archive_policy}.
        :param content_based_deduplication: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#content_based_deduplication SnsTopic#content_based_deduplication}.
        :param delivery_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#delivery_policy SnsTopic#delivery_policy}.
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#display_name SnsTopic#display_name}.
        :param fifo_topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#fifo_topic SnsTopic#fifo_topic}.
        :param firehose_failure_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#firehose_failure_feedback_role_arn SnsTopic#firehose_failure_feedback_role_arn}.
        :param firehose_success_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#firehose_success_feedback_role_arn SnsTopic#firehose_success_feedback_role_arn}.
        :param firehose_success_feedback_sample_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#firehose_success_feedback_sample_rate SnsTopic#firehose_success_feedback_sample_rate}.
        :param http_failure_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#http_failure_feedback_role_arn SnsTopic#http_failure_feedback_role_arn}.
        :param http_success_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#http_success_feedback_role_arn SnsTopic#http_success_feedback_role_arn}.
        :param http_success_feedback_sample_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#http_success_feedback_sample_rate SnsTopic#http_success_feedback_sample_rate}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#id SnsTopic#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_master_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#kms_master_key_id SnsTopic#kms_master_key_id}.
        :param lambda_failure_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#lambda_failure_feedback_role_arn SnsTopic#lambda_failure_feedback_role_arn}.
        :param lambda_success_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#lambda_success_feedback_role_arn SnsTopic#lambda_success_feedback_role_arn}.
        :param lambda_success_feedback_sample_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#lambda_success_feedback_sample_rate SnsTopic#lambda_success_feedback_sample_rate}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#name SnsTopic#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#name_prefix SnsTopic#name_prefix}.
        :param policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#policy SnsTopic#policy}.
        :param signature_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#signature_version SnsTopic#signature_version}.
        :param sqs_failure_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#sqs_failure_feedback_role_arn SnsTopic#sqs_failure_feedback_role_arn}.
        :param sqs_success_feedback_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#sqs_success_feedback_role_arn SnsTopic#sqs_success_feedback_role_arn}.
        :param sqs_success_feedback_sample_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#sqs_success_feedback_sample_rate SnsTopic#sqs_success_feedback_sample_rate}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#tags SnsTopic#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#tags_all SnsTopic#tags_all}.
        :param tracing_config: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#tracing_config SnsTopic#tracing_config}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e65b37f84fe8f0189a08d687bcc921a6b9e54ee278530a143d6623c49f312eb)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument application_failure_feedback_role_arn", value=application_failure_feedback_role_arn, expected_type=type_hints["application_failure_feedback_role_arn"])
            check_type(argname="argument application_success_feedback_role_arn", value=application_success_feedback_role_arn, expected_type=type_hints["application_success_feedback_role_arn"])
            check_type(argname="argument application_success_feedback_sample_rate", value=application_success_feedback_sample_rate, expected_type=type_hints["application_success_feedback_sample_rate"])
            check_type(argname="argument archive_policy", value=archive_policy, expected_type=type_hints["archive_policy"])
            check_type(argname="argument content_based_deduplication", value=content_based_deduplication, expected_type=type_hints["content_based_deduplication"])
            check_type(argname="argument delivery_policy", value=delivery_policy, expected_type=type_hints["delivery_policy"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument fifo_topic", value=fifo_topic, expected_type=type_hints["fifo_topic"])
            check_type(argname="argument firehose_failure_feedback_role_arn", value=firehose_failure_feedback_role_arn, expected_type=type_hints["firehose_failure_feedback_role_arn"])
            check_type(argname="argument firehose_success_feedback_role_arn", value=firehose_success_feedback_role_arn, expected_type=type_hints["firehose_success_feedback_role_arn"])
            check_type(argname="argument firehose_success_feedback_sample_rate", value=firehose_success_feedback_sample_rate, expected_type=type_hints["firehose_success_feedback_sample_rate"])
            check_type(argname="argument http_failure_feedback_role_arn", value=http_failure_feedback_role_arn, expected_type=type_hints["http_failure_feedback_role_arn"])
            check_type(argname="argument http_success_feedback_role_arn", value=http_success_feedback_role_arn, expected_type=type_hints["http_success_feedback_role_arn"])
            check_type(argname="argument http_success_feedback_sample_rate", value=http_success_feedback_sample_rate, expected_type=type_hints["http_success_feedback_sample_rate"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_master_key_id", value=kms_master_key_id, expected_type=type_hints["kms_master_key_id"])
            check_type(argname="argument lambda_failure_feedback_role_arn", value=lambda_failure_feedback_role_arn, expected_type=type_hints["lambda_failure_feedback_role_arn"])
            check_type(argname="argument lambda_success_feedback_role_arn", value=lambda_success_feedback_role_arn, expected_type=type_hints["lambda_success_feedback_role_arn"])
            check_type(argname="argument lambda_success_feedback_sample_rate", value=lambda_success_feedback_sample_rate, expected_type=type_hints["lambda_success_feedback_sample_rate"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument name_prefix", value=name_prefix, expected_type=type_hints["name_prefix"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument signature_version", value=signature_version, expected_type=type_hints["signature_version"])
            check_type(argname="argument sqs_failure_feedback_role_arn", value=sqs_failure_feedback_role_arn, expected_type=type_hints["sqs_failure_feedback_role_arn"])
            check_type(argname="argument sqs_success_feedback_role_arn", value=sqs_success_feedback_role_arn, expected_type=type_hints["sqs_success_feedback_role_arn"])
            check_type(argname="argument sqs_success_feedback_sample_rate", value=sqs_success_feedback_sample_rate, expected_type=type_hints["sqs_success_feedback_sample_rate"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument tracing_config", value=tracing_config, expected_type=type_hints["tracing_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if application_failure_feedback_role_arn is not None:
            self._values["application_failure_feedback_role_arn"] = application_failure_feedback_role_arn
        if application_success_feedback_role_arn is not None:
            self._values["application_success_feedback_role_arn"] = application_success_feedback_role_arn
        if application_success_feedback_sample_rate is not None:
            self._values["application_success_feedback_sample_rate"] = application_success_feedback_sample_rate
        if archive_policy is not None:
            self._values["archive_policy"] = archive_policy
        if content_based_deduplication is not None:
            self._values["content_based_deduplication"] = content_based_deduplication
        if delivery_policy is not None:
            self._values["delivery_policy"] = delivery_policy
        if display_name is not None:
            self._values["display_name"] = display_name
        if fifo_topic is not None:
            self._values["fifo_topic"] = fifo_topic
        if firehose_failure_feedback_role_arn is not None:
            self._values["firehose_failure_feedback_role_arn"] = firehose_failure_feedback_role_arn
        if firehose_success_feedback_role_arn is not None:
            self._values["firehose_success_feedback_role_arn"] = firehose_success_feedback_role_arn
        if firehose_success_feedback_sample_rate is not None:
            self._values["firehose_success_feedback_sample_rate"] = firehose_success_feedback_sample_rate
        if http_failure_feedback_role_arn is not None:
            self._values["http_failure_feedback_role_arn"] = http_failure_feedback_role_arn
        if http_success_feedback_role_arn is not None:
            self._values["http_success_feedback_role_arn"] = http_success_feedback_role_arn
        if http_success_feedback_sample_rate is not None:
            self._values["http_success_feedback_sample_rate"] = http_success_feedback_sample_rate
        if id is not None:
            self._values["id"] = id
        if kms_master_key_id is not None:
            self._values["kms_master_key_id"] = kms_master_key_id
        if lambda_failure_feedback_role_arn is not None:
            self._values["lambda_failure_feedback_role_arn"] = lambda_failure_feedback_role_arn
        if lambda_success_feedback_role_arn is not None:
            self._values["lambda_success_feedback_role_arn"] = lambda_success_feedback_role_arn
        if lambda_success_feedback_sample_rate is not None:
            self._values["lambda_success_feedback_sample_rate"] = lambda_success_feedback_sample_rate
        if name is not None:
            self._values["name"] = name
        if name_prefix is not None:
            self._values["name_prefix"] = name_prefix
        if policy is not None:
            self._values["policy"] = policy
        if signature_version is not None:
            self._values["signature_version"] = signature_version
        if sqs_failure_feedback_role_arn is not None:
            self._values["sqs_failure_feedback_role_arn"] = sqs_failure_feedback_role_arn
        if sqs_success_feedback_role_arn is not None:
            self._values["sqs_success_feedback_role_arn"] = sqs_success_feedback_role_arn
        if sqs_success_feedback_sample_rate is not None:
            self._values["sqs_success_feedback_sample_rate"] = sqs_success_feedback_sample_rate
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if tracing_config is not None:
            self._values["tracing_config"] = tracing_config

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
    def application_failure_feedback_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#application_failure_feedback_role_arn SnsTopic#application_failure_feedback_role_arn}.'''
        result = self._values.get("application_failure_feedback_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_success_feedback_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#application_success_feedback_role_arn SnsTopic#application_success_feedback_role_arn}.'''
        result = self._values.get("application_success_feedback_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_success_feedback_sample_rate(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#application_success_feedback_sample_rate SnsTopic#application_success_feedback_sample_rate}.'''
        result = self._values.get("application_success_feedback_sample_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def archive_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#archive_policy SnsTopic#archive_policy}.'''
        result = self._values.get("archive_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_based_deduplication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#content_based_deduplication SnsTopic#content_based_deduplication}.'''
        result = self._values.get("content_based_deduplication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def delivery_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#delivery_policy SnsTopic#delivery_policy}.'''
        result = self._values.get("delivery_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#display_name SnsTopic#display_name}.'''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fifo_topic(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#fifo_topic SnsTopic#fifo_topic}.'''
        result = self._values.get("fifo_topic")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def firehose_failure_feedback_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#firehose_failure_feedback_role_arn SnsTopic#firehose_failure_feedback_role_arn}.'''
        result = self._values.get("firehose_failure_feedback_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firehose_success_feedback_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#firehose_success_feedback_role_arn SnsTopic#firehose_success_feedback_role_arn}.'''
        result = self._values.get("firehose_success_feedback_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firehose_success_feedback_sample_rate(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#firehose_success_feedback_sample_rate SnsTopic#firehose_success_feedback_sample_rate}.'''
        result = self._values.get("firehose_success_feedback_sample_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def http_failure_feedback_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#http_failure_feedback_role_arn SnsTopic#http_failure_feedback_role_arn}.'''
        result = self._values.get("http_failure_feedback_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_success_feedback_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#http_success_feedback_role_arn SnsTopic#http_success_feedback_role_arn}.'''
        result = self._values.get("http_success_feedback_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_success_feedback_sample_rate(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#http_success_feedback_sample_rate SnsTopic#http_success_feedback_sample_rate}.'''
        result = self._values.get("http_success_feedback_sample_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#id SnsTopic#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_master_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#kms_master_key_id SnsTopic#kms_master_key_id}.'''
        result = self._values.get("kms_master_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_failure_feedback_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#lambda_failure_feedback_role_arn SnsTopic#lambda_failure_feedback_role_arn}.'''
        result = self._values.get("lambda_failure_feedback_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_success_feedback_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#lambda_success_feedback_role_arn SnsTopic#lambda_success_feedback_role_arn}.'''
        result = self._values.get("lambda_success_feedback_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_success_feedback_sample_rate(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#lambda_success_feedback_sample_rate SnsTopic#lambda_success_feedback_sample_rate}.'''
        result = self._values.get("lambda_success_feedback_sample_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#name SnsTopic#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#name_prefix SnsTopic#name_prefix}.'''
        result = self._values.get("name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#policy SnsTopic#policy}.'''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signature_version(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#signature_version SnsTopic#signature_version}.'''
        result = self._values.get("signature_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sqs_failure_feedback_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#sqs_failure_feedback_role_arn SnsTopic#sqs_failure_feedback_role_arn}.'''
        result = self._values.get("sqs_failure_feedback_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sqs_success_feedback_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#sqs_success_feedback_role_arn SnsTopic#sqs_success_feedback_role_arn}.'''
        result = self._values.get("sqs_success_feedback_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sqs_success_feedback_sample_rate(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#sqs_success_feedback_sample_rate SnsTopic#sqs_success_feedback_sample_rate}.'''
        result = self._values.get("sqs_success_feedback_sample_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#tags SnsTopic#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#tags_all SnsTopic#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tracing_config(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sns_topic#tracing_config SnsTopic#tracing_config}.'''
        result = self._values.get("tracing_config")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsTopicConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SnsTopic",
    "SnsTopicConfig",
]

publication.publish()

def _typecheckingstub__a31d974c6ea71caa64a711d716c588e5eeff5b2ebec265d618be2572dcd34e00(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    application_failure_feedback_role_arn: typing.Optional[builtins.str] = None,
    application_success_feedback_role_arn: typing.Optional[builtins.str] = None,
    application_success_feedback_sample_rate: typing.Optional[jsii.Number] = None,
    archive_policy: typing.Optional[builtins.str] = None,
    content_based_deduplication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delivery_policy: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    fifo_topic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    firehose_failure_feedback_role_arn: typing.Optional[builtins.str] = None,
    firehose_success_feedback_role_arn: typing.Optional[builtins.str] = None,
    firehose_success_feedback_sample_rate: typing.Optional[jsii.Number] = None,
    http_failure_feedback_role_arn: typing.Optional[builtins.str] = None,
    http_success_feedback_role_arn: typing.Optional[builtins.str] = None,
    http_success_feedback_sample_rate: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    kms_master_key_id: typing.Optional[builtins.str] = None,
    lambda_failure_feedback_role_arn: typing.Optional[builtins.str] = None,
    lambda_success_feedback_role_arn: typing.Optional[builtins.str] = None,
    lambda_success_feedback_sample_rate: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    policy: typing.Optional[builtins.str] = None,
    signature_version: typing.Optional[jsii.Number] = None,
    sqs_failure_feedback_role_arn: typing.Optional[builtins.str] = None,
    sqs_success_feedback_role_arn: typing.Optional[builtins.str] = None,
    sqs_success_feedback_sample_rate: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tracing_config: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__6cb4335cdc9fb574dcafbc0c67ed3822e61bbdd6ee894251c49e555485d83cf3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__209c9a6632e66d72eaad3133afd7a9ee2fb9537e53bbe9730b9eaa0d1aa48a01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2d21ecdaf367a0ea9aff64c831987f29a33a69140307eaf6b11c99148b7d386(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f376de287d2b2ffdbe6d9d4e507b35a9703fe8bce9d6d3991e7943cc64785964(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f2c18da6289d665c1454ef81a86e271bf99ecdaa512b3827cdaca2b61a5327(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872bb23db6a948f3b6aa7be812a272c332a14dfa8fa31c3249ff11c3b68c6557(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4988912db5c472b1d8058f12c4bec0309c8de9f08413dee81a988945aa3510b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb829546d974309e9de64bdd26dd34c8b5ea72c73fce7e5144f255846371a782(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a08b9474f67cdea7dc0b187634bad405ea903ed1417593cbbc8c5fe98295055(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e9758d57bbf177e76a310e78bd4174002f115c25b7a6fd5fd9d1eda43507193(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c15ab22d6a690f01b57773f1a906a691fba08c82e99656c72f4fc342aad6aaf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a406f317de0423f00e86371e779fed8337ef3eaf9330ac68fe38d484b93aba75(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0290006c0f76a65e6d05c141186edcb832f140ddde72db1555424ed0ea6e632(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e66eb082ec520f94db5fd47cb1b4c1bab2dd7a53bce1198b5fca126ebcb32334(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3783deecc4601a5afe714aea626c8a7287433920215cf6ef08ea8f017981a2f7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f82783ccc7884a497aa38cb91f722356202eb5e94112654282b04650d15fd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f42697b95d3fec35fb87f496cae98c32ce3fc4ed336dd6c6c57c49099c454d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f6fb0ecac5220fba553d1bc3f7395f770e570225e979fb61a5a6491c873299a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca4dfa071f58bd7fdce2b0821d1fc1e2fac71850328aae744a7a3dabe41ce039(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__991bbea634d926bd6dd663cc7f1f0236c9d05fe4c1f46db1605c1fbeabd39fd1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbf747f8893433d3e218e528fa5e615aa2d957ca860e01f6d5d20d5348edf3b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__564d4f6deda5b90181b17f89c76460a0c4bb3fe202841858efa39aa51020559c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c8b6384c702533fa37720c2163ca0ff75307519d0e21b7ce605504fd20089b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c978e1a46c5436825bc6c5d7cfe02170977b87c413d35c2911c3a6b62a69324(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d040a9d6d859b314c610a91d9d3974377637a4f537d274c9f29c493f8f4f9464(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd77ca7faa749a8295ed0a9f9b42c104e2bc4ca1200d426dc796a771aba423d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e666c188e3a87866a4ddbe2b02dd9d510e892836bce49a6971913d1916632a6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__290e4bf3d0b32b24e20b0669cd45b883111335a4fcc0cd209fa14a552ae7a452(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61b3b958aee2a055563031b04e6ae253266d402dbd5f85f68e4cc20366dcfc46(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f3de9101974a9d55cc838130a9508701e31aedc1127a2d382e36b4df4af95c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e65b37f84fe8f0189a08d687bcc921a6b9e54ee278530a143d6623c49f312eb(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    application_failure_feedback_role_arn: typing.Optional[builtins.str] = None,
    application_success_feedback_role_arn: typing.Optional[builtins.str] = None,
    application_success_feedback_sample_rate: typing.Optional[jsii.Number] = None,
    archive_policy: typing.Optional[builtins.str] = None,
    content_based_deduplication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delivery_policy: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    fifo_topic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    firehose_failure_feedback_role_arn: typing.Optional[builtins.str] = None,
    firehose_success_feedback_role_arn: typing.Optional[builtins.str] = None,
    firehose_success_feedback_sample_rate: typing.Optional[jsii.Number] = None,
    http_failure_feedback_role_arn: typing.Optional[builtins.str] = None,
    http_success_feedback_role_arn: typing.Optional[builtins.str] = None,
    http_success_feedback_sample_rate: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    kms_master_key_id: typing.Optional[builtins.str] = None,
    lambda_failure_feedback_role_arn: typing.Optional[builtins.str] = None,
    lambda_success_feedback_role_arn: typing.Optional[builtins.str] = None,
    lambda_success_feedback_sample_rate: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    policy: typing.Optional[builtins.str] = None,
    signature_version: typing.Optional[jsii.Number] = None,
    sqs_failure_feedback_role_arn: typing.Optional[builtins.str] = None,
    sqs_success_feedback_role_arn: typing.Optional[builtins.str] = None,
    sqs_success_feedback_sample_rate: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tracing_config: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
