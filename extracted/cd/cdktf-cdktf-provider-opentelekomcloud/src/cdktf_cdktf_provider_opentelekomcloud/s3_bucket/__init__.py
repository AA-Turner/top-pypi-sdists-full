r'''
# `opentelekomcloud_s3_bucket`

Refer to the Terraform Registry for docs: [`opentelekomcloud_s3_bucket`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket).
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


class S3Bucket(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.s3Bucket.S3Bucket",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket opentelekomcloud_s3_bucket}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        acl: typing.Optional[builtins.str] = None,
        arn: typing.Optional[builtins.str] = None,
        bucket: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        cors_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3BucketCorsRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hosted_zone_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lifecycle_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3BucketLifecycleRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        logging: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3BucketLogging", typing.Dict[builtins.str, typing.Any]]]]] = None,
        policy: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        versioning: typing.Optional[typing.Union["S3BucketVersioning", typing.Dict[builtins.str, typing.Any]]] = None,
        website: typing.Optional[typing.Union["S3BucketWebsite", typing.Dict[builtins.str, typing.Any]]] = None,
        website_domain: typing.Optional[builtins.str] = None,
        website_endpoint: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket opentelekomcloud_s3_bucket} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#acl S3Bucket#acl}.
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#arn S3Bucket#arn}.
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#bucket S3Bucket#bucket}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#bucket_prefix S3Bucket#bucket_prefix}.
        :param cors_rule: cors_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#cors_rule S3Bucket#cors_rule}
        :param force_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#force_destroy S3Bucket#force_destroy}.
        :param hosted_zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#hosted_zone_id S3Bucket#hosted_zone_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#id S3Bucket#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lifecycle_rule: lifecycle_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#lifecycle_rule S3Bucket#lifecycle_rule}
        :param logging: logging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#logging S3Bucket#logging}
        :param policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#policy S3Bucket#policy}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#region S3Bucket#region}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#tags S3Bucket#tags}.
        :param versioning: versioning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#versioning S3Bucket#versioning}
        :param website: website block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#website S3Bucket#website}
        :param website_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#website_domain S3Bucket#website_domain}.
        :param website_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#website_endpoint S3Bucket#website_endpoint}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e51401f767815ecd670daeebe84ea244e2a5035f4d7372dfc32b9b4dde2235b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = S3BucketConfig(
            acl=acl,
            arn=arn,
            bucket=bucket,
            bucket_prefix=bucket_prefix,
            cors_rule=cors_rule,
            force_destroy=force_destroy,
            hosted_zone_id=hosted_zone_id,
            id=id,
            lifecycle_rule=lifecycle_rule,
            logging=logging,
            policy=policy,
            region=region,
            tags=tags,
            versioning=versioning,
            website=website,
            website_domain=website_domain,
            website_endpoint=website_endpoint,
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
        '''Generates CDKTF code for importing a S3Bucket resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the S3Bucket to import.
        :param import_from_id: The id of the existing S3Bucket that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the S3Bucket to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a8342b3a506d78a774152de6c2ffee0e0412c5ec0d9d4633f07dd1b972f84ee)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCorsRule")
    def put_cors_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3BucketCorsRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ca7fe88968630d40b5e6977900ad4d438db39c510b5a04c80de8f1ed405ec9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCorsRule", [value]))

    @jsii.member(jsii_name="putLifecycleRule")
    def put_lifecycle_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3BucketLifecycleRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d6ed41e1cbf41400775dd2edabcdc3ae0311894f92c91ed1d7cca6900400b5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLifecycleRule", [value]))

    @jsii.member(jsii_name="putLogging")
    def put_logging(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3BucketLogging", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26c6534a8300f53bf3bea1994b97e408ab0576277bc0a4c662850b90400365e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLogging", [value]))

    @jsii.member(jsii_name="putVersioning")
    def put_versioning(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mfa_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#enabled S3Bucket#enabled}.
        :param mfa_delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#mfa_delete S3Bucket#mfa_delete}.
        '''
        value = S3BucketVersioning(enabled=enabled, mfa_delete=mfa_delete)

        return typing.cast(None, jsii.invoke(self, "putVersioning", [value]))

    @jsii.member(jsii_name="putWebsite")
    def put_website(
        self,
        *,
        error_document: typing.Optional[builtins.str] = None,
        index_document: typing.Optional[builtins.str] = None,
        redirect_all_requests_to: typing.Optional[builtins.str] = None,
        routing_rules: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param error_document: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#error_document S3Bucket#error_document}.
        :param index_document: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#index_document S3Bucket#index_document}.
        :param redirect_all_requests_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#redirect_all_requests_to S3Bucket#redirect_all_requests_to}.
        :param routing_rules: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#routing_rules S3Bucket#routing_rules}.
        '''
        value = S3BucketWebsite(
            error_document=error_document,
            index_document=index_document,
            redirect_all_requests_to=redirect_all_requests_to,
            routing_rules=routing_rules,
        )

        return typing.cast(None, jsii.invoke(self, "putWebsite", [value]))

    @jsii.member(jsii_name="resetAcl")
    def reset_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcl", []))

    @jsii.member(jsii_name="resetArn")
    def reset_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArn", []))

    @jsii.member(jsii_name="resetBucket")
    def reset_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucket", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetCorsRule")
    def reset_cors_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCorsRule", []))

    @jsii.member(jsii_name="resetForceDestroy")
    def reset_force_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceDestroy", []))

    @jsii.member(jsii_name="resetHostedZoneId")
    def reset_hosted_zone_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostedZoneId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLifecycleRule")
    def reset_lifecycle_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleRule", []))

    @jsii.member(jsii_name="resetLogging")
    def reset_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogging", []))

    @jsii.member(jsii_name="resetPolicy")
    def reset_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicy", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetVersioning")
    def reset_versioning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersioning", []))

    @jsii.member(jsii_name="resetWebsite")
    def reset_website(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebsite", []))

    @jsii.member(jsii_name="resetWebsiteDomain")
    def reset_website_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebsiteDomain", []))

    @jsii.member(jsii_name="resetWebsiteEndpoint")
    def reset_website_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebsiteEndpoint", []))

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
    @jsii.member(jsii_name="bucketDomainName")
    def bucket_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketDomainName"))

    @builtins.property
    @jsii.member(jsii_name="corsRule")
    def cors_rule(self) -> "S3BucketCorsRuleList":
        return typing.cast("S3BucketCorsRuleList", jsii.get(self, "corsRule"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleRule")
    def lifecycle_rule(self) -> "S3BucketLifecycleRuleList":
        return typing.cast("S3BucketLifecycleRuleList", jsii.get(self, "lifecycleRule"))

    @builtins.property
    @jsii.member(jsii_name="logging")
    def logging(self) -> "S3BucketLoggingList":
        return typing.cast("S3BucketLoggingList", jsii.get(self, "logging"))

    @builtins.property
    @jsii.member(jsii_name="versioning")
    def versioning(self) -> "S3BucketVersioningOutputReference":
        return typing.cast("S3BucketVersioningOutputReference", jsii.get(self, "versioning"))

    @builtins.property
    @jsii.member(jsii_name="website")
    def website(self) -> "S3BucketWebsiteOutputReference":
        return typing.cast("S3BucketWebsiteOutputReference", jsii.get(self, "website"))

    @builtins.property
    @jsii.member(jsii_name="aclInput")
    def acl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aclInput"))

    @builtins.property
    @jsii.member(jsii_name="arnInput")
    def arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arnInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="corsRuleInput")
    def cors_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3BucketCorsRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3BucketCorsRule"]]], jsii.get(self, "corsRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="forceDestroyInput")
    def force_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="hostedZoneIdInput")
    def hosted_zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostedZoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleRuleInput")
    def lifecycle_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3BucketLifecycleRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3BucketLifecycleRule"]]], jsii.get(self, "lifecycleRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingInput")
    def logging_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3BucketLogging"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3BucketLogging"]]], jsii.get(self, "loggingInput"))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="versioningInput")
    def versioning_input(self) -> typing.Optional["S3BucketVersioning"]:
        return typing.cast(typing.Optional["S3BucketVersioning"], jsii.get(self, "versioningInput"))

    @builtins.property
    @jsii.member(jsii_name="websiteDomainInput")
    def website_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "websiteDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="websiteEndpointInput")
    def website_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "websiteEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="websiteInput")
    def website_input(self) -> typing.Optional["S3BucketWebsite"]:
        return typing.cast(typing.Optional["S3BucketWebsite"], jsii.get(self, "websiteInput"))

    @builtins.property
    @jsii.member(jsii_name="acl")
    def acl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acl"))

    @acl.setter
    def acl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf93eb8d8588522d23afb6f151b9f76839a765404602df932d71adbe448c5732)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @arn.setter
    def arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f817c5d2df90ffd8c5f50c8383d6b253d8be408ef433020bfb3d401981e73de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f19fc6912851b1fb3228202efc921b2a795aac62e178c8190c8582a907409bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c33a5544681581242bd7dc7b5471e766624d0d0ce30795bb7a40d22e4ed8fae9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceDestroy")
    def force_destroy(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceDestroy"))

    @force_destroy.setter
    def force_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0caf6ce2cc0aa53ccec30844c1e1685387570eba0bc4162b5f3b8e6053bbcd8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostedZoneId")
    def hosted_zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostedZoneId"))

    @hosted_zone_id.setter
    def hosted_zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f183883d97d1ada919d53182964e8b1bf87728d51ad72837783c940c096aabe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostedZoneId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a15ddafab2885052fc3424fb936a68ad233e2220b1062d89fb1123ba1326a2bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be8e7d779821a5f188bb9d430dff9e8aa07c799956a934d2cfe08c88b6d65cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec275f25515d3fb9fd48e0b5fd694a11723c27e2537fd8b79389cdfed7d6402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e3fb40ece5134238114f8cc07846108f61307a0a476f4ca217ec3d922286d62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="websiteDomain")
    def website_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "websiteDomain"))

    @website_domain.setter
    def website_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79d26c566777ab9ba8e7c78fffb5a86293bcbe3e97110da163c9572b0949c15d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "websiteDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="websiteEndpoint")
    def website_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "websiteEndpoint"))

    @website_endpoint.setter
    def website_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c90330e605a45d4ca82b5763fb19ea6b6944b15edac4c4f31f968bdc84fd28cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "websiteEndpoint", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.s3Bucket.S3BucketConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "acl": "acl",
        "arn": "arn",
        "bucket": "bucket",
        "bucket_prefix": "bucketPrefix",
        "cors_rule": "corsRule",
        "force_destroy": "forceDestroy",
        "hosted_zone_id": "hostedZoneId",
        "id": "id",
        "lifecycle_rule": "lifecycleRule",
        "logging": "logging",
        "policy": "policy",
        "region": "region",
        "tags": "tags",
        "versioning": "versioning",
        "website": "website",
        "website_domain": "websiteDomain",
        "website_endpoint": "websiteEndpoint",
    },
)
class S3BucketConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        acl: typing.Optional[builtins.str] = None,
        arn: typing.Optional[builtins.str] = None,
        bucket: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        cors_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3BucketCorsRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hosted_zone_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lifecycle_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3BucketLifecycleRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        logging: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3BucketLogging", typing.Dict[builtins.str, typing.Any]]]]] = None,
        policy: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        versioning: typing.Optional[typing.Union["S3BucketVersioning", typing.Dict[builtins.str, typing.Any]]] = None,
        website: typing.Optional[typing.Union["S3BucketWebsite", typing.Dict[builtins.str, typing.Any]]] = None,
        website_domain: typing.Optional[builtins.str] = None,
        website_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#acl S3Bucket#acl}.
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#arn S3Bucket#arn}.
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#bucket S3Bucket#bucket}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#bucket_prefix S3Bucket#bucket_prefix}.
        :param cors_rule: cors_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#cors_rule S3Bucket#cors_rule}
        :param force_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#force_destroy S3Bucket#force_destroy}.
        :param hosted_zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#hosted_zone_id S3Bucket#hosted_zone_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#id S3Bucket#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lifecycle_rule: lifecycle_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#lifecycle_rule S3Bucket#lifecycle_rule}
        :param logging: logging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#logging S3Bucket#logging}
        :param policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#policy S3Bucket#policy}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#region S3Bucket#region}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#tags S3Bucket#tags}.
        :param versioning: versioning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#versioning S3Bucket#versioning}
        :param website: website block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#website S3Bucket#website}
        :param website_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#website_domain S3Bucket#website_domain}.
        :param website_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#website_endpoint S3Bucket#website_endpoint}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(versioning, dict):
            versioning = S3BucketVersioning(**versioning)
        if isinstance(website, dict):
            website = S3BucketWebsite(**website)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a97f9c702a103c59cba9fab45fb399802b35c4863ce4732556ba6ec440df9e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument acl", value=acl, expected_type=type_hints["acl"])
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument cors_rule", value=cors_rule, expected_type=type_hints["cors_rule"])
            check_type(argname="argument force_destroy", value=force_destroy, expected_type=type_hints["force_destroy"])
            check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lifecycle_rule", value=lifecycle_rule, expected_type=type_hints["lifecycle_rule"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument versioning", value=versioning, expected_type=type_hints["versioning"])
            check_type(argname="argument website", value=website, expected_type=type_hints["website"])
            check_type(argname="argument website_domain", value=website_domain, expected_type=type_hints["website_domain"])
            check_type(argname="argument website_endpoint", value=website_endpoint, expected_type=type_hints["website_endpoint"])
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
        if acl is not None:
            self._values["acl"] = acl
        if arn is not None:
            self._values["arn"] = arn
        if bucket is not None:
            self._values["bucket"] = bucket
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if cors_rule is not None:
            self._values["cors_rule"] = cors_rule
        if force_destroy is not None:
            self._values["force_destroy"] = force_destroy
        if hosted_zone_id is not None:
            self._values["hosted_zone_id"] = hosted_zone_id
        if id is not None:
            self._values["id"] = id
        if lifecycle_rule is not None:
            self._values["lifecycle_rule"] = lifecycle_rule
        if logging is not None:
            self._values["logging"] = logging
        if policy is not None:
            self._values["policy"] = policy
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if versioning is not None:
            self._values["versioning"] = versioning
        if website is not None:
            self._values["website"] = website
        if website_domain is not None:
            self._values["website_domain"] = website_domain
        if website_endpoint is not None:
            self._values["website_endpoint"] = website_endpoint

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
    def acl(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#acl S3Bucket#acl}.'''
        result = self._values.get("acl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#arn S3Bucket#arn}.'''
        result = self._values.get("arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#bucket S3Bucket#bucket}.'''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#bucket_prefix S3Bucket#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cors_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3BucketCorsRule"]]]:
        '''cors_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#cors_rule S3Bucket#cors_rule}
        '''
        result = self._values.get("cors_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3BucketCorsRule"]]], result)

    @builtins.property
    def force_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#force_destroy S3Bucket#force_destroy}.'''
        result = self._values.get("force_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hosted_zone_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#hosted_zone_id S3Bucket#hosted_zone_id}.'''
        result = self._values.get("hosted_zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#id S3Bucket#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3BucketLifecycleRule"]]]:
        '''lifecycle_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#lifecycle_rule S3Bucket#lifecycle_rule}
        '''
        result = self._values.get("lifecycle_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3BucketLifecycleRule"]]], result)

    @builtins.property
    def logging(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3BucketLogging"]]]:
        '''logging block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#logging S3Bucket#logging}
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3BucketLogging"]]], result)

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#policy S3Bucket#policy}.'''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#region S3Bucket#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#tags S3Bucket#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def versioning(self) -> typing.Optional["S3BucketVersioning"]:
        '''versioning block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#versioning S3Bucket#versioning}
        '''
        result = self._values.get("versioning")
        return typing.cast(typing.Optional["S3BucketVersioning"], result)

    @builtins.property
    def website(self) -> typing.Optional["S3BucketWebsite"]:
        '''website block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#website S3Bucket#website}
        '''
        result = self._values.get("website")
        return typing.cast(typing.Optional["S3BucketWebsite"], result)

    @builtins.property
    def website_domain(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#website_domain S3Bucket#website_domain}.'''
        result = self._values.get("website_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def website_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#website_endpoint S3Bucket#website_endpoint}.'''
        result = self._values.get("website_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3BucketConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.s3Bucket.S3BucketCorsRule",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_methods": "allowedMethods",
        "allowed_origins": "allowedOrigins",
        "allowed_headers": "allowedHeaders",
        "expose_headers": "exposeHeaders",
        "max_age_seconds": "maxAgeSeconds",
    },
)
class S3BucketCorsRule:
    def __init__(
        self,
        *,
        allowed_methods: typing.Sequence[builtins.str],
        allowed_origins: typing.Sequence[builtins.str],
        allowed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        expose_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_age_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param allowed_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#allowed_methods S3Bucket#allowed_methods}.
        :param allowed_origins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#allowed_origins S3Bucket#allowed_origins}.
        :param allowed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#allowed_headers S3Bucket#allowed_headers}.
        :param expose_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#expose_headers S3Bucket#expose_headers}.
        :param max_age_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#max_age_seconds S3Bucket#max_age_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cecd1c3487158ae3fb5cb001b66668e911be2c08c32ecc81eaeaf6a41b3c6eaa)
            check_type(argname="argument allowed_methods", value=allowed_methods, expected_type=type_hints["allowed_methods"])
            check_type(argname="argument allowed_origins", value=allowed_origins, expected_type=type_hints["allowed_origins"])
            check_type(argname="argument allowed_headers", value=allowed_headers, expected_type=type_hints["allowed_headers"])
            check_type(argname="argument expose_headers", value=expose_headers, expected_type=type_hints["expose_headers"])
            check_type(argname="argument max_age_seconds", value=max_age_seconds, expected_type=type_hints["max_age_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_methods": allowed_methods,
            "allowed_origins": allowed_origins,
        }
        if allowed_headers is not None:
            self._values["allowed_headers"] = allowed_headers
        if expose_headers is not None:
            self._values["expose_headers"] = expose_headers
        if max_age_seconds is not None:
            self._values["max_age_seconds"] = max_age_seconds

    @builtins.property
    def allowed_methods(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#allowed_methods S3Bucket#allowed_methods}.'''
        result = self._values.get("allowed_methods")
        assert result is not None, "Required property 'allowed_methods' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def allowed_origins(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#allowed_origins S3Bucket#allowed_origins}.'''
        result = self._values.get("allowed_origins")
        assert result is not None, "Required property 'allowed_origins' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def allowed_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#allowed_headers S3Bucket#allowed_headers}.'''
        result = self._values.get("allowed_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def expose_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#expose_headers S3Bucket#expose_headers}.'''
        result = self._values.get("expose_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_age_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#max_age_seconds S3Bucket#max_age_seconds}.'''
        result = self._values.get("max_age_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3BucketCorsRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3BucketCorsRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.s3Bucket.S3BucketCorsRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e25ae54490d4f7c79cd89c2e364064e4a39e326af749d000931333318c6015e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "S3BucketCorsRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6bb0eea306b4fd634e87ea7124cf45f1f92b066b38a6868ebd46718cd79b6d2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("S3BucketCorsRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd50a512d271ccbfd2d17bd5f636d571b8d1d83f55e9f0731a25bcf17a6f5b7b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44c566ccadc66f67a8162bf564625740955c7877e984c0a0b674265e5ee8e201)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ab453588887ac020bac4bfc5e2ecc265b7a5798f75fd27ba8507d273262d3cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketCorsRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketCorsRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketCorsRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58a00a31776a054cfb8a1c21171b3e1bb4a71498cf44b2e366447054c82f8b26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class S3BucketCorsRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.s3Bucket.S3BucketCorsRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__407ea27398f91bae9e67225ad52d254a8fcabd23064979af138df100dc72b4b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowedHeaders")
    def reset_allowed_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedHeaders", []))

    @jsii.member(jsii_name="resetExposeHeaders")
    def reset_expose_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExposeHeaders", []))

    @jsii.member(jsii_name="resetMaxAgeSeconds")
    def reset_max_age_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAgeSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="allowedHeadersInput")
    def allowed_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedMethodsInput")
    def allowed_methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedOriginsInput")
    def allowed_origins_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedOriginsInput"))

    @builtins.property
    @jsii.member(jsii_name="exposeHeadersInput")
    def expose_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exposeHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAgeSecondsInput")
    def max_age_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAgeSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedHeaders")
    def allowed_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedHeaders"))

    @allowed_headers.setter
    def allowed_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3236a89b2cecb32562464ffb373a039697ff9e4616c5fea8f5cf9e6001d75971)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedMethods")
    def allowed_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedMethods"))

    @allowed_methods.setter
    def allowed_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b7f186fb888d1c2a7bf3e4f769f615460ec01ce029f245f84f8266b4758d22f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedOrigins")
    def allowed_origins(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedOrigins"))

    @allowed_origins.setter
    def allowed_origins(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d29e9b1d4a561a5d57e0cc38a9a013be0303c9cf4fb9a230302fa771a7eb6564)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedOrigins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exposeHeaders")
    def expose_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exposeHeaders"))

    @expose_headers.setter
    def expose_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7138aafc43c275d83227201a650bdb0b88661ffb671158403cdcc46437d310e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exposeHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAgeSeconds")
    def max_age_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAgeSeconds"))

    @max_age_seconds.setter
    def max_age_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c67be5b0586c7eb3fab6ae3fb358d7660a665e7b0f2bfe467ea6d2ed0c61bc24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAgeSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3BucketCorsRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3BucketCorsRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3BucketCorsRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c416cf953b998049fb7b98655c7c407467b598b3841210eefd71d1f721669064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.s3Bucket.S3BucketLifecycleRule",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "abort_incomplete_multipart_upload_days": "abortIncompleteMultipartUploadDays",
        "expiration": "expiration",
        "id": "id",
        "noncurrent_version_expiration": "noncurrentVersionExpiration",
        "prefix": "prefix",
    },
)
class S3BucketLifecycleRule:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        abort_incomplete_multipart_upload_days: typing.Optional[jsii.Number] = None,
        expiration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3BucketLifecycleRuleExpiration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        noncurrent_version_expiration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3BucketLifecycleRuleNoncurrentVersionExpiration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#enabled S3Bucket#enabled}.
        :param abort_incomplete_multipart_upload_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#abort_incomplete_multipart_upload_days S3Bucket#abort_incomplete_multipart_upload_days}.
        :param expiration: expiration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#expiration S3Bucket#expiration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#id S3Bucket#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param noncurrent_version_expiration: noncurrent_version_expiration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#noncurrent_version_expiration S3Bucket#noncurrent_version_expiration}
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#prefix S3Bucket#prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65f4a699de255aaad3858e960db247bcdbd797df768b2bbdb1b616969d715cfc)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument abort_incomplete_multipart_upload_days", value=abort_incomplete_multipart_upload_days, expected_type=type_hints["abort_incomplete_multipart_upload_days"])
            check_type(argname="argument expiration", value=expiration, expected_type=type_hints["expiration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument noncurrent_version_expiration", value=noncurrent_version_expiration, expected_type=type_hints["noncurrent_version_expiration"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if abort_incomplete_multipart_upload_days is not None:
            self._values["abort_incomplete_multipart_upload_days"] = abort_incomplete_multipart_upload_days
        if expiration is not None:
            self._values["expiration"] = expiration
        if id is not None:
            self._values["id"] = id
        if noncurrent_version_expiration is not None:
            self._values["noncurrent_version_expiration"] = noncurrent_version_expiration
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#enabled S3Bucket#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def abort_incomplete_multipart_upload_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#abort_incomplete_multipart_upload_days S3Bucket#abort_incomplete_multipart_upload_days}.'''
        result = self._values.get("abort_incomplete_multipart_upload_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def expiration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3BucketLifecycleRuleExpiration"]]]:
        '''expiration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#expiration S3Bucket#expiration}
        '''
        result = self._values.get("expiration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3BucketLifecycleRuleExpiration"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#id S3Bucket#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def noncurrent_version_expiration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3BucketLifecycleRuleNoncurrentVersionExpiration"]]]:
        '''noncurrent_version_expiration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#noncurrent_version_expiration S3Bucket#noncurrent_version_expiration}
        '''
        result = self._values.get("noncurrent_version_expiration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3BucketLifecycleRuleNoncurrentVersionExpiration"]]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#prefix S3Bucket#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3BucketLifecycleRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.s3Bucket.S3BucketLifecycleRuleExpiration",
    jsii_struct_bases=[],
    name_mapping={
        "date": "date",
        "days": "days",
        "expired_object_delete_marker": "expiredObjectDeleteMarker",
    },
)
class S3BucketLifecycleRuleExpiration:
    def __init__(
        self,
        *,
        date: typing.Optional[builtins.str] = None,
        days: typing.Optional[jsii.Number] = None,
        expired_object_delete_marker: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param date: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#date S3Bucket#date}.
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#days S3Bucket#days}.
        :param expired_object_delete_marker: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#expired_object_delete_marker S3Bucket#expired_object_delete_marker}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb850f728bf8f07e87c575a4eb9c1845b39547e255550a9a36f25de62d4efd4f)
            check_type(argname="argument date", value=date, expected_type=type_hints["date"])
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
            check_type(argname="argument expired_object_delete_marker", value=expired_object_delete_marker, expected_type=type_hints["expired_object_delete_marker"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if date is not None:
            self._values["date"] = date
        if days is not None:
            self._values["days"] = days
        if expired_object_delete_marker is not None:
            self._values["expired_object_delete_marker"] = expired_object_delete_marker

    @builtins.property
    def date(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#date S3Bucket#date}.'''
        result = self._values.get("date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#days S3Bucket#days}.'''
        result = self._values.get("days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def expired_object_delete_marker(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#expired_object_delete_marker S3Bucket#expired_object_delete_marker}.'''
        result = self._values.get("expired_object_delete_marker")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3BucketLifecycleRuleExpiration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3BucketLifecycleRuleExpirationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.s3Bucket.S3BucketLifecycleRuleExpirationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6b8173702f580603bdf87b202b5ebdaa95ac69984f3409cbdc9dcc7956a67a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "S3BucketLifecycleRuleExpirationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0149a294f27816f47ede988bb140417503a67bde3740f48226d235ac932f6bb6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("S3BucketLifecycleRuleExpirationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2751681c346923ea1f799aca456d57d410af13c4ec4e4862cce763938bdae256)
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
            type_hints = typing.get_type_hints(_typecheckingstub__895478b545d16caaf5d8d2cf86be1c38afc7c699cdad306f482a9c6fac415633)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4144decd422d0b5e45f277d630f9245505e557c3fe148937c8c71227d16a79ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketLifecycleRuleExpiration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketLifecycleRuleExpiration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketLifecycleRuleExpiration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25c5990666bbcb2d6db0e6505d8de843bbc0ca324ee14438be210f345e0a6457)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class S3BucketLifecycleRuleExpirationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.s3Bucket.S3BucketLifecycleRuleExpirationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c75e8555d1f19d3aedd12b0d685ff38aa3ae2865931f60068607d8c4a75d6639)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDate")
    def reset_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDate", []))

    @jsii.member(jsii_name="resetDays")
    def reset_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDays", []))

    @jsii.member(jsii_name="resetExpiredObjectDeleteMarker")
    def reset_expired_object_delete_marker(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpiredObjectDeleteMarker", []))

    @builtins.property
    @jsii.member(jsii_name="dateInput")
    def date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dateInput"))

    @builtins.property
    @jsii.member(jsii_name="daysInput")
    def days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "daysInput"))

    @builtins.property
    @jsii.member(jsii_name="expiredObjectDeleteMarkerInput")
    def expired_object_delete_marker_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "expiredObjectDeleteMarkerInput"))

    @builtins.property
    @jsii.member(jsii_name="date")
    def date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "date"))

    @date.setter
    def date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1931447711f739aa45b5169e22a9248bf1f73ad48b8a9e2c7be61c58e8ed39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "date", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="days")
    def days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "days"))

    @days.setter
    def days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dffc0cec5b4fed15cbd5b02c16613fa9df762dc27beba4c8c4c66c33e476216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "days", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expiredObjectDeleteMarker")
    def expired_object_delete_marker(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "expiredObjectDeleteMarker"))

    @expired_object_delete_marker.setter
    def expired_object_delete_marker(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e61df8cf9b4321a4dca2e77b51be05d7051e927517e739588b69d8f99372fad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiredObjectDeleteMarker", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3BucketLifecycleRuleExpiration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3BucketLifecycleRuleExpiration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3BucketLifecycleRuleExpiration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed9bdcd6b0bdc8e223b1e6b5929bbf7a3e696c8ce7960200b1983239fffdc4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class S3BucketLifecycleRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.s3Bucket.S3BucketLifecycleRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2714b7b3d6327834fefdeadd9af5011f1e4607098eb6a319a3042b58c7080983)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "S3BucketLifecycleRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e229319760927309b4143d9c8daa5a354c0bfeb787fc725f2a6306ac405bbf21)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("S3BucketLifecycleRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a2c09fc49a1bd4dccc78914e8b9e51e342833c7400b7a18df73b795e00b485d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7cf4ad135eefd40b2216f907253c34a3b72519647e4f053bea9f72a06603e4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d03a6de1c5491cac98ace5e41682fde86ea748c1c25ebc8e3200275183022cce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketLifecycleRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketLifecycleRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketLifecycleRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc75381c9b41b078d83ea67350c162117dda7356aef01631bd8d28d1f173214)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.s3Bucket.S3BucketLifecycleRuleNoncurrentVersionExpiration",
    jsii_struct_bases=[],
    name_mapping={"days": "days"},
)
class S3BucketLifecycleRuleNoncurrentVersionExpiration:
    def __init__(self, *, days: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#days S3Bucket#days}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__938186c4035f8cff7b1096804a771b7b49672aa397113b3dc09a65f75660119f)
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if days is not None:
            self._values["days"] = days

    @builtins.property
    def days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#days S3Bucket#days}.'''
        result = self._values.get("days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3BucketLifecycleRuleNoncurrentVersionExpiration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3BucketLifecycleRuleNoncurrentVersionExpirationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.s3Bucket.S3BucketLifecycleRuleNoncurrentVersionExpirationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdac36f2b355b2854586f5e0b04aaf05ffbe7a038aa2b88afdb0a43e58457b4c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "S3BucketLifecycleRuleNoncurrentVersionExpirationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8daf2371f5eddf9e8f26b260eb7feaae128ba7db59df772e3994496cbe48cb2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("S3BucketLifecycleRuleNoncurrentVersionExpirationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa3d7d98ea8ac1b1b6aa1a050c0fa10eca94854bb559e659378b28e50abe96be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__376238802304e820c40110630e99a319803076ecccfbf11e4ee6faa853d7d1fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20816aa2d7c08d6af5bfb3be5068bbb1c73a4af38dfb906220ee8003221c1278)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketLifecycleRuleNoncurrentVersionExpiration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketLifecycleRuleNoncurrentVersionExpiration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketLifecycleRuleNoncurrentVersionExpiration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b268e4fba2d187b79115803c82f8562f195aca302d79b332ede86d44b613eef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class S3BucketLifecycleRuleNoncurrentVersionExpirationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.s3Bucket.S3BucketLifecycleRuleNoncurrentVersionExpirationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1450b3f43ce7c73d517a12307ea98e13d97c2a5fbe902e381c4a279be34f1b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDays")
    def reset_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDays", []))

    @builtins.property
    @jsii.member(jsii_name="daysInput")
    def days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "daysInput"))

    @builtins.property
    @jsii.member(jsii_name="days")
    def days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "days"))

    @days.setter
    def days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa8e5cfb59a10f589357d0ed363cb33d88d303068356a4a8b8f88e87e526a8c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "days", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3BucketLifecycleRuleNoncurrentVersionExpiration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3BucketLifecycleRuleNoncurrentVersionExpiration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3BucketLifecycleRuleNoncurrentVersionExpiration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3c7523a38dc9edf061582ed1806de033eccbc8f4eb3d47536c54f94b2279acd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class S3BucketLifecycleRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.s3Bucket.S3BucketLifecycleRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8a47db346cfb8ebc6b3b504ea7520e7afaa63a60aa230c188c9e9a77447ce9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putExpiration")
    def put_expiration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3BucketLifecycleRuleExpiration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adfa69b0f8c1f71ce542c12c6775033673f9ff3eefdf69e8769e3f109b44e2a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExpiration", [value]))

    @jsii.member(jsii_name="putNoncurrentVersionExpiration")
    def put_noncurrent_version_expiration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3BucketLifecycleRuleNoncurrentVersionExpiration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15078237de05dfd76eae1054f10c7d2d176306420140a2550f62c8806f6ef4c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNoncurrentVersionExpiration", [value]))

    @jsii.member(jsii_name="resetAbortIncompleteMultipartUploadDays")
    def reset_abort_incomplete_multipart_upload_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAbortIncompleteMultipartUploadDays", []))

    @jsii.member(jsii_name="resetExpiration")
    def reset_expiration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpiration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNoncurrentVersionExpiration")
    def reset_noncurrent_version_expiration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoncurrentVersionExpiration", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="expiration")
    def expiration(self) -> S3BucketLifecycleRuleExpirationList:
        return typing.cast(S3BucketLifecycleRuleExpirationList, jsii.get(self, "expiration"))

    @builtins.property
    @jsii.member(jsii_name="noncurrentVersionExpiration")
    def noncurrent_version_expiration(
        self,
    ) -> S3BucketLifecycleRuleNoncurrentVersionExpirationList:
        return typing.cast(S3BucketLifecycleRuleNoncurrentVersionExpirationList, jsii.get(self, "noncurrentVersionExpiration"))

    @builtins.property
    @jsii.member(jsii_name="abortIncompleteMultipartUploadDaysInput")
    def abort_incomplete_multipart_upload_days_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "abortIncompleteMultipartUploadDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationInput")
    def expiration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketLifecycleRuleExpiration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketLifecycleRuleExpiration]]], jsii.get(self, "expirationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="noncurrentVersionExpirationInput")
    def noncurrent_version_expiration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketLifecycleRuleNoncurrentVersionExpiration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketLifecycleRuleNoncurrentVersionExpiration]]], jsii.get(self, "noncurrentVersionExpirationInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="abortIncompleteMultipartUploadDays")
    def abort_incomplete_multipart_upload_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "abortIncompleteMultipartUploadDays"))

    @abort_incomplete_multipart_upload_days.setter
    def abort_incomplete_multipart_upload_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd9f2542d3ead3bd1d2a02215da54c59acd7dc0900a225929ed090e7affe1f03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "abortIncompleteMultipartUploadDays", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__2f8f5a7680853a82ef003d5045b7a1880b22a3d86c204f9e163b98fba8655531)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9de33be43935ca22515bdcbd6d3d017b14e1bfe05f85aabd0a8173d7fa33797)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3f27e41f3f3d25e9a7a485e3f0561c6496ac78ff1dad3a64aca9e25c4742757)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3BucketLifecycleRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3BucketLifecycleRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3BucketLifecycleRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d04d7001a5fc06cd7080fda535afd36632721d3593ab6c14b1e859c125c294d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.s3Bucket.S3BucketLogging",
    jsii_struct_bases=[],
    name_mapping={"target_bucket": "targetBucket", "target_prefix": "targetPrefix"},
)
class S3BucketLogging:
    def __init__(
        self,
        *,
        target_bucket: builtins.str,
        target_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#target_bucket S3Bucket#target_bucket}.
        :param target_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#target_prefix S3Bucket#target_prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__063a545355d2f977667733d2fe1bdc0575df0cd7749d48460153c2637585d78b)
            check_type(argname="argument target_bucket", value=target_bucket, expected_type=type_hints["target_bucket"])
            check_type(argname="argument target_prefix", value=target_prefix, expected_type=type_hints["target_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_bucket": target_bucket,
        }
        if target_prefix is not None:
            self._values["target_prefix"] = target_prefix

    @builtins.property
    def target_bucket(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#target_bucket S3Bucket#target_bucket}.'''
        result = self._values.get("target_bucket")
        assert result is not None, "Required property 'target_bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#target_prefix S3Bucket#target_prefix}.'''
        result = self._values.get("target_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3BucketLogging(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3BucketLoggingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.s3Bucket.S3BucketLoggingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0a38b4ef6ea3a52e0e8f702e11f8366c970754313203b872a2636848ae3aeb5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "S3BucketLoggingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__418df6ffbbcb7d968816307748e0b73f2a6a68c2cdb63ead66790c823e755e56)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("S3BucketLoggingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1756f5219dac92b53351dee9b9d4c98a818ca6924ad36c8d5b7606733e4a34b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2deb049cc69af194b2f96834cd55ef0a9fb749b8ae23189ebc458bc679d65ff4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a35162f7a8efcc05cf97de6104b1fc64fa80bcb00866029943f6cc5c93fd844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketLogging]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketLogging]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketLogging]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17d58a497f12f34ac660c9f5623bc5856cb9e55fc960f51a64bddf7657e6b835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class S3BucketLoggingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.s3Bucket.S3BucketLoggingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0816aa81a0be8a28d00c93f3e187d6ff842174f8a4e0d71f8922969fb1405ff7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetTargetPrefix")
    def reset_target_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="targetBucketInput")
    def target_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="targetPrefixInput")
    def target_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="targetBucket")
    def target_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetBucket"))

    @target_bucket.setter
    def target_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a7790d1fae67371d93b0b9ffaef5c2056d881c7176982dcee6c2294e7e0d2b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetPrefix")
    def target_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetPrefix"))

    @target_prefix.setter
    def target_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53712f6a904b4a9d8f917c5ae08451501adb9593a44c5e92a400862a89164901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3BucketLogging]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3BucketLogging]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3BucketLogging]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a43af77272d7db64b936cfd0556245e56e80d409e833b6e3257ea1c2494a7bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.s3Bucket.S3BucketVersioning",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "mfa_delete": "mfaDelete"},
)
class S3BucketVersioning:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mfa_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#enabled S3Bucket#enabled}.
        :param mfa_delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#mfa_delete S3Bucket#mfa_delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf715ed46cb5709384bfe86c09e27bbe2b19c55c152754f4017363f8bb21a5ac)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument mfa_delete", value=mfa_delete, expected_type=type_hints["mfa_delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if mfa_delete is not None:
            self._values["mfa_delete"] = mfa_delete

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#enabled S3Bucket#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def mfa_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#mfa_delete S3Bucket#mfa_delete}.'''
        result = self._values.get("mfa_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3BucketVersioning(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3BucketVersioningOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.s3Bucket.S3BucketVersioningOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__556b88585a099896673481471488e2a516af46c808d5bbba1b0d96889d13f7f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetMfaDelete")
    def reset_mfa_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMfaDelete", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="mfaDeleteInput")
    def mfa_delete_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mfaDeleteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__692f2405f8934e03c8e092085025afeb6bfc2b6abdb15be15db7a20b06277b3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mfaDelete")
    def mfa_delete(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mfaDelete"))

    @mfa_delete.setter
    def mfa_delete(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ade27af545d7f203ce7ee9d2ce8e8fb32ad927394aa1fe99d5c60959a84aebce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mfaDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[S3BucketVersioning]:
        return typing.cast(typing.Optional[S3BucketVersioning], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[S3BucketVersioning]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df17fa88bf9401214b9546204ffe02839fe9d1cc2ff582deb43d306bca7f8c0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.s3Bucket.S3BucketWebsite",
    jsii_struct_bases=[],
    name_mapping={
        "error_document": "errorDocument",
        "index_document": "indexDocument",
        "redirect_all_requests_to": "redirectAllRequestsTo",
        "routing_rules": "routingRules",
    },
)
class S3BucketWebsite:
    def __init__(
        self,
        *,
        error_document: typing.Optional[builtins.str] = None,
        index_document: typing.Optional[builtins.str] = None,
        redirect_all_requests_to: typing.Optional[builtins.str] = None,
        routing_rules: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param error_document: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#error_document S3Bucket#error_document}.
        :param index_document: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#index_document S3Bucket#index_document}.
        :param redirect_all_requests_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#redirect_all_requests_to S3Bucket#redirect_all_requests_to}.
        :param routing_rules: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#routing_rules S3Bucket#routing_rules}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9aef8ff168994d6446ed30630d16afd5cf20c40fbebb9692756d064037c126f)
            check_type(argname="argument error_document", value=error_document, expected_type=type_hints["error_document"])
            check_type(argname="argument index_document", value=index_document, expected_type=type_hints["index_document"])
            check_type(argname="argument redirect_all_requests_to", value=redirect_all_requests_to, expected_type=type_hints["redirect_all_requests_to"])
            check_type(argname="argument routing_rules", value=routing_rules, expected_type=type_hints["routing_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if error_document is not None:
            self._values["error_document"] = error_document
        if index_document is not None:
            self._values["index_document"] = index_document
        if redirect_all_requests_to is not None:
            self._values["redirect_all_requests_to"] = redirect_all_requests_to
        if routing_rules is not None:
            self._values["routing_rules"] = routing_rules

    @builtins.property
    def error_document(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#error_document S3Bucket#error_document}.'''
        result = self._values.get("error_document")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def index_document(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#index_document S3Bucket#index_document}.'''
        result = self._values.get("index_document")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_all_requests_to(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#redirect_all_requests_to S3Bucket#redirect_all_requests_to}.'''
        result = self._values.get("redirect_all_requests_to")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_rules(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/s3_bucket#routing_rules S3Bucket#routing_rules}.'''
        result = self._values.get("routing_rules")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3BucketWebsite(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3BucketWebsiteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.s3Bucket.S3BucketWebsiteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__342635dc87c5ce7beb22b05875fcc3026c32593f902b622840ebd1191fd65a12)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetErrorDocument")
    def reset_error_document(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorDocument", []))

    @jsii.member(jsii_name="resetIndexDocument")
    def reset_index_document(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIndexDocument", []))

    @jsii.member(jsii_name="resetRedirectAllRequestsTo")
    def reset_redirect_all_requests_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectAllRequestsTo", []))

    @jsii.member(jsii_name="resetRoutingRules")
    def reset_routing_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingRules", []))

    @builtins.property
    @jsii.member(jsii_name="errorDocumentInput")
    def error_document_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "errorDocumentInput"))

    @builtins.property
    @jsii.member(jsii_name="indexDocumentInput")
    def index_document_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexDocumentInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectAllRequestsToInput")
    def redirect_all_requests_to_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectAllRequestsToInput"))

    @builtins.property
    @jsii.member(jsii_name="routingRulesInput")
    def routing_rules_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="errorDocument")
    def error_document(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorDocument"))

    @error_document.setter
    def error_document(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__099a04c6eeb71d315f392b6f6a1a73dc12871c299c9b32a7135ef47ba3db0cb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorDocument", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indexDocument")
    def index_document(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "indexDocument"))

    @index_document.setter
    def index_document(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3467ffe19b7e07be0984896756412e0590f599cb9708b216c25cc6e42c80d81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indexDocument", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectAllRequestsTo")
    def redirect_all_requests_to(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectAllRequestsTo"))

    @redirect_all_requests_to.setter
    def redirect_all_requests_to(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebdb31769ba37f3d8499378352cb92f342420908fd9c07b526db32212c557198)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectAllRequestsTo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingRules")
    def routing_rules(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingRules"))

    @routing_rules.setter
    def routing_rules(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74bf03570a0a2a58216f37bd48aa97e557927c58e96f6789a129f9c6db242d90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingRules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[S3BucketWebsite]:
        return typing.cast(typing.Optional[S3BucketWebsite], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[S3BucketWebsite]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__834d2a26b13c33c69f719d4a1cb194a9849db0d47f05ab8f3774a274e7ec4500)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "S3Bucket",
    "S3BucketConfig",
    "S3BucketCorsRule",
    "S3BucketCorsRuleList",
    "S3BucketCorsRuleOutputReference",
    "S3BucketLifecycleRule",
    "S3BucketLifecycleRuleExpiration",
    "S3BucketLifecycleRuleExpirationList",
    "S3BucketLifecycleRuleExpirationOutputReference",
    "S3BucketLifecycleRuleList",
    "S3BucketLifecycleRuleNoncurrentVersionExpiration",
    "S3BucketLifecycleRuleNoncurrentVersionExpirationList",
    "S3BucketLifecycleRuleNoncurrentVersionExpirationOutputReference",
    "S3BucketLifecycleRuleOutputReference",
    "S3BucketLogging",
    "S3BucketLoggingList",
    "S3BucketLoggingOutputReference",
    "S3BucketVersioning",
    "S3BucketVersioningOutputReference",
    "S3BucketWebsite",
    "S3BucketWebsiteOutputReference",
]

publication.publish()

def _typecheckingstub__1e51401f767815ecd670daeebe84ea244e2a5035f4d7372dfc32b9b4dde2235b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    acl: typing.Optional[builtins.str] = None,
    arn: typing.Optional[builtins.str] = None,
    bucket: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    cors_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3BucketCorsRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lifecycle_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3BucketLifecycleRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    logging: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3BucketLogging, typing.Dict[builtins.str, typing.Any]]]]] = None,
    policy: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    versioning: typing.Optional[typing.Union[S3BucketVersioning, typing.Dict[builtins.str, typing.Any]]] = None,
    website: typing.Optional[typing.Union[S3BucketWebsite, typing.Dict[builtins.str, typing.Any]]] = None,
    website_domain: typing.Optional[builtins.str] = None,
    website_endpoint: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__5a8342b3a506d78a774152de6c2ffee0e0412c5ec0d9d4633f07dd1b972f84ee(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ca7fe88968630d40b5e6977900ad4d438db39c510b5a04c80de8f1ed405ec9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3BucketCorsRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d6ed41e1cbf41400775dd2edabcdc3ae0311894f92c91ed1d7cca6900400b5f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3BucketLifecycleRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c6534a8300f53bf3bea1994b97e408ab0576277bc0a4c662850b90400365e6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3BucketLogging, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf93eb8d8588522d23afb6f151b9f76839a765404602df932d71adbe448c5732(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f817c5d2df90ffd8c5f50c8383d6b253d8be408ef433020bfb3d401981e73de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f19fc6912851b1fb3228202efc921b2a795aac62e178c8190c8582a907409bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33a5544681581242bd7dc7b5471e766624d0d0ce30795bb7a40d22e4ed8fae9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0caf6ce2cc0aa53ccec30844c1e1685387570eba0bc4162b5f3b8e6053bbcd8d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f183883d97d1ada919d53182964e8b1bf87728d51ad72837783c940c096aabe4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a15ddafab2885052fc3424fb936a68ad233e2220b1062d89fb1123ba1326a2bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be8e7d779821a5f188bb9d430dff9e8aa07c799956a934d2cfe08c88b6d65cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec275f25515d3fb9fd48e0b5fd694a11723c27e2537fd8b79389cdfed7d6402(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3fb40ece5134238114f8cc07846108f61307a0a476f4ca217ec3d922286d62(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d26c566777ab9ba8e7c78fffb5a86293bcbe3e97110da163c9572b0949c15d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c90330e605a45d4ca82b5763fb19ea6b6944b15edac4c4f31f968bdc84fd28cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a97f9c702a103c59cba9fab45fb399802b35c4863ce4732556ba6ec440df9e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    acl: typing.Optional[builtins.str] = None,
    arn: typing.Optional[builtins.str] = None,
    bucket: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    cors_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3BucketCorsRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lifecycle_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3BucketLifecycleRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    logging: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3BucketLogging, typing.Dict[builtins.str, typing.Any]]]]] = None,
    policy: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    versioning: typing.Optional[typing.Union[S3BucketVersioning, typing.Dict[builtins.str, typing.Any]]] = None,
    website: typing.Optional[typing.Union[S3BucketWebsite, typing.Dict[builtins.str, typing.Any]]] = None,
    website_domain: typing.Optional[builtins.str] = None,
    website_endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cecd1c3487158ae3fb5cb001b66668e911be2c08c32ecc81eaeaf6a41b3c6eaa(
    *,
    allowed_methods: typing.Sequence[builtins.str],
    allowed_origins: typing.Sequence[builtins.str],
    allowed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    expose_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_age_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25ae54490d4f7c79cd89c2e364064e4a39e326af749d000931333318c6015e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6bb0eea306b4fd634e87ea7124cf45f1f92b066b38a6868ebd46718cd79b6d2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd50a512d271ccbfd2d17bd5f636d571b8d1d83f55e9f0731a25bcf17a6f5b7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c566ccadc66f67a8162bf564625740955c7877e984c0a0b674265e5ee8e201(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ab453588887ac020bac4bfc5e2ecc265b7a5798f75fd27ba8507d273262d3cb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58a00a31776a054cfb8a1c21171b3e1bb4a71498cf44b2e366447054c82f8b26(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketCorsRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__407ea27398f91bae9e67225ad52d254a8fcabd23064979af138df100dc72b4b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3236a89b2cecb32562464ffb373a039697ff9e4616c5fea8f5cf9e6001d75971(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b7f186fb888d1c2a7bf3e4f769f615460ec01ce029f245f84f8266b4758d22f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29e9b1d4a561a5d57e0cc38a9a013be0303c9cf4fb9a230302fa771a7eb6564(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7138aafc43c275d83227201a650bdb0b88661ffb671158403cdcc46437d310e1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c67be5b0586c7eb3fab6ae3fb358d7660a665e7b0f2bfe467ea6d2ed0c61bc24(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c416cf953b998049fb7b98655c7c407467b598b3841210eefd71d1f721669064(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3BucketCorsRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65f4a699de255aaad3858e960db247bcdbd797df768b2bbdb1b616969d715cfc(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    abort_incomplete_multipart_upload_days: typing.Optional[jsii.Number] = None,
    expiration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3BucketLifecycleRuleExpiration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    noncurrent_version_expiration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3BucketLifecycleRuleNoncurrentVersionExpiration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb850f728bf8f07e87c575a4eb9c1845b39547e255550a9a36f25de62d4efd4f(
    *,
    date: typing.Optional[builtins.str] = None,
    days: typing.Optional[jsii.Number] = None,
    expired_object_delete_marker: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b8173702f580603bdf87b202b5ebdaa95ac69984f3409cbdc9dcc7956a67a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0149a294f27816f47ede988bb140417503a67bde3740f48226d235ac932f6bb6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2751681c346923ea1f799aca456d57d410af13c4ec4e4862cce763938bdae256(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__895478b545d16caaf5d8d2cf86be1c38afc7c699cdad306f482a9c6fac415633(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4144decd422d0b5e45f277d630f9245505e557c3fe148937c8c71227d16a79ca(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c5990666bbcb2d6db0e6505d8de843bbc0ca324ee14438be210f345e0a6457(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketLifecycleRuleExpiration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75e8555d1f19d3aedd12b0d685ff38aa3ae2865931f60068607d8c4a75d6639(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1931447711f739aa45b5169e22a9248bf1f73ad48b8a9e2c7be61c58e8ed39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dffc0cec5b4fed15cbd5b02c16613fa9df762dc27beba4c8c4c66c33e476216(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e61df8cf9b4321a4dca2e77b51be05d7051e927517e739588b69d8f99372fad(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed9bdcd6b0bdc8e223b1e6b5929bbf7a3e696c8ce7960200b1983239fffdc4d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3BucketLifecycleRuleExpiration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2714b7b3d6327834fefdeadd9af5011f1e4607098eb6a319a3042b58c7080983(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e229319760927309b4143d9c8daa5a354c0bfeb787fc725f2a6306ac405bbf21(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a2c09fc49a1bd4dccc78914e8b9e51e342833c7400b7a18df73b795e00b485d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7cf4ad135eefd40b2216f907253c34a3b72519647e4f053bea9f72a06603e4f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d03a6de1c5491cac98ace5e41682fde86ea748c1c25ebc8e3200275183022cce(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc75381c9b41b078d83ea67350c162117dda7356aef01631bd8d28d1f173214(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketLifecycleRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938186c4035f8cff7b1096804a771b7b49672aa397113b3dc09a65f75660119f(
    *,
    days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdac36f2b355b2854586f5e0b04aaf05ffbe7a038aa2b88afdb0a43e58457b4c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8daf2371f5eddf9e8f26b260eb7feaae128ba7db59df772e3994496cbe48cb2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa3d7d98ea8ac1b1b6aa1a050c0fa10eca94854bb559e659378b28e50abe96be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__376238802304e820c40110630e99a319803076ecccfbf11e4ee6faa853d7d1fa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20816aa2d7c08d6af5bfb3be5068bbb1c73a4af38dfb906220ee8003221c1278(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b268e4fba2d187b79115803c82f8562f195aca302d79b332ede86d44b613eef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketLifecycleRuleNoncurrentVersionExpiration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1450b3f43ce7c73d517a12307ea98e13d97c2a5fbe902e381c4a279be34f1b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa8e5cfb59a10f589357d0ed363cb33d88d303068356a4a8b8f88e87e526a8c8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3c7523a38dc9edf061582ed1806de033eccbc8f4eb3d47536c54f94b2279acd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3BucketLifecycleRuleNoncurrentVersionExpiration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a47db346cfb8ebc6b3b504ea7520e7afaa63a60aa230c188c9e9a77447ce9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adfa69b0f8c1f71ce542c12c6775033673f9ff3eefdf69e8769e3f109b44e2a8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3BucketLifecycleRuleExpiration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15078237de05dfd76eae1054f10c7d2d176306420140a2550f62c8806f6ef4c0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3BucketLifecycleRuleNoncurrentVersionExpiration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd9f2542d3ead3bd1d2a02215da54c59acd7dc0900a225929ed090e7affe1f03(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f8f5a7680853a82ef003d5045b7a1880b22a3d86c204f9e163b98fba8655531(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9de33be43935ca22515bdcbd6d3d017b14e1bfe05f85aabd0a8173d7fa33797(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f27e41f3f3d25e9a7a485e3f0561c6496ac78ff1dad3a64aca9e25c4742757(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04d7001a5fc06cd7080fda535afd36632721d3593ab6c14b1e859c125c294d0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3BucketLifecycleRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063a545355d2f977667733d2fe1bdc0575df0cd7749d48460153c2637585d78b(
    *,
    target_bucket: builtins.str,
    target_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0a38b4ef6ea3a52e0e8f702e11f8366c970754313203b872a2636848ae3aeb5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418df6ffbbcb7d968816307748e0b73f2a6a68c2cdb63ead66790c823e755e56(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1756f5219dac92b53351dee9b9d4c98a818ca6924ad36c8d5b7606733e4a34b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2deb049cc69af194b2f96834cd55ef0a9fb749b8ae23189ebc458bc679d65ff4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a35162f7a8efcc05cf97de6104b1fc64fa80bcb00866029943f6cc5c93fd844(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17d58a497f12f34ac660c9f5623bc5856cb9e55fc960f51a64bddf7657e6b835(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3BucketLogging]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0816aa81a0be8a28d00c93f3e187d6ff842174f8a4e0d71f8922969fb1405ff7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a7790d1fae67371d93b0b9ffaef5c2056d881c7176982dcee6c2294e7e0d2b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53712f6a904b4a9d8f917c5ae08451501adb9593a44c5e92a400862a89164901(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a43af77272d7db64b936cfd0556245e56e80d409e833b6e3257ea1c2494a7bd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3BucketLogging]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf715ed46cb5709384bfe86c09e27bbe2b19c55c152754f4017363f8bb21a5ac(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mfa_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556b88585a099896673481471488e2a516af46c808d5bbba1b0d96889d13f7f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692f2405f8934e03c8e092085025afeb6bfc2b6abdb15be15db7a20b06277b3b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ade27af545d7f203ce7ee9d2ce8e8fb32ad927394aa1fe99d5c60959a84aebce(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df17fa88bf9401214b9546204ffe02839fe9d1cc2ff582deb43d306bca7f8c0f(
    value: typing.Optional[S3BucketVersioning],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9aef8ff168994d6446ed30630d16afd5cf20c40fbebb9692756d064037c126f(
    *,
    error_document: typing.Optional[builtins.str] = None,
    index_document: typing.Optional[builtins.str] = None,
    redirect_all_requests_to: typing.Optional[builtins.str] = None,
    routing_rules: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__342635dc87c5ce7beb22b05875fcc3026c32593f902b622840ebd1191fd65a12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__099a04c6eeb71d315f392b6f6a1a73dc12871c299c9b32a7135ef47ba3db0cb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3467ffe19b7e07be0984896756412e0590f599cb9708b216c25cc6e42c80d81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebdb31769ba37f3d8499378352cb92f342420908fd9c07b526db32212c557198(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74bf03570a0a2a58216f37bd48aa97e557927c58e96f6789a129f9c6db242d90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__834d2a26b13c33c69f719d4a1cb194a9849db0d47f05ab8f3774a274e7ec4500(
    value: typing.Optional[S3BucketWebsite],
) -> None:
    """Type checking stubs"""
    pass
