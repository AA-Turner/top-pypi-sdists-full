r'''
# `provider`

Refer to the Terraform Registry for docs: [`aws`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs).
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


class AwsProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.provider.AwsProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs aws}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_key: typing.Optional[builtins.str] = None,
        alias: typing.Optional[builtins.str] = None,
        allowed_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        assume_role: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AwsProviderAssumeRole", typing.Dict[builtins.str, typing.Any]]]]] = None,
        assume_role_with_web_identity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AwsProviderAssumeRoleWithWebIdentity", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_ca_bundle: typing.Optional[builtins.str] = None,
        default_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AwsProviderDefaultTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ec2_metadata_service_endpoint: typing.Optional[builtins.str] = None,
        ec2_metadata_service_endpoint_mode: typing.Optional[builtins.str] = None,
        endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AwsProviderEndpoints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        forbidden_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        http_proxy: typing.Optional[builtins.str] = None,
        https_proxy: typing.Optional[builtins.str] = None,
        ignore_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AwsProviderIgnoreTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        no_proxy: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        retry_mode: typing.Optional[builtins.str] = None,
        s3_us_east1_regional_endpoint: typing.Optional[builtins.str] = None,
        s3_use_path_style: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_key: typing.Optional[builtins.str] = None,
        shared_config_files: typing.Optional[typing.Sequence[builtins.str]] = None,
        shared_credentials_files: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_credentials_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_metadata_api_check: typing.Optional[builtins.str] = None,
        skip_region_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_requesting_account_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sts_region: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        token_bucket_rate_limiter_capacity: typing.Optional[jsii.Number] = None,
        use_dualstack_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_fips_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs aws} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param access_key: The access key for API operations. You can retrieve this from the 'Security & Credentials' section of the AWS console. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#access_key AwsProvider#access_key}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#alias AwsProvider#alias}
        :param allowed_account_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#allowed_account_ids AwsProvider#allowed_account_ids}.
        :param assume_role: assume_role block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#assume_role AwsProvider#assume_role}
        :param assume_role_with_web_identity: assume_role_with_web_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#assume_role_with_web_identity AwsProvider#assume_role_with_web_identity}
        :param custom_ca_bundle: File containing custom root and intermediate certificates. Can also be configured using the ``AWS_CA_BUNDLE`` environment variable. (Setting ``ca_bundle`` in the shared config file is not supported.) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#custom_ca_bundle AwsProvider#custom_ca_bundle}
        :param default_tags: default_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#default_tags AwsProvider#default_tags}
        :param ec2_metadata_service_endpoint: Address of the EC2 metadata service endpoint to use. Can also be configured using the ``AWS_EC2_METADATA_SERVICE_ENDPOINT`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ec2_metadata_service_endpoint AwsProvider#ec2_metadata_service_endpoint}
        :param ec2_metadata_service_endpoint_mode: Protocol to use with EC2 metadata service endpoint.Valid values are ``IPv4`` and ``IPv6``. Can also be configured using the ``AWS_EC2_METADATA_SERVICE_ENDPOINT_MODE`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ec2_metadata_service_endpoint_mode AwsProvider#ec2_metadata_service_endpoint_mode}
        :param endpoints: endpoints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#endpoints AwsProvider#endpoints}
        :param forbidden_account_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#forbidden_account_ids AwsProvider#forbidden_account_ids}.
        :param http_proxy: URL of a proxy to use for HTTP requests when accessing the AWS API. Can also be set using the ``HTTP_PROXY`` or ``http_proxy`` environment variables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#http_proxy AwsProvider#http_proxy}
        :param https_proxy: URL of a proxy to use for HTTPS requests when accessing the AWS API. Can also be set using the ``HTTPS_PROXY`` or ``https_proxy`` environment variables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#https_proxy AwsProvider#https_proxy}
        :param ignore_tags: ignore_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ignore_tags AwsProvider#ignore_tags}
        :param insecure: Explicitly allow the provider to perform "insecure" SSL requests. If omitted, default value is ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#insecure AwsProvider#insecure}
        :param max_retries: The maximum number of times an AWS API request is being executed. If the API request still fails, an error is thrown. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#max_retries AwsProvider#max_retries}
        :param no_proxy: Comma-separated list of hosts that should not use HTTP or HTTPS proxies. Can also be set using the ``NO_PROXY`` or ``no_proxy`` environment variables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#no_proxy AwsProvider#no_proxy}
        :param profile: The profile for API operations. If not set, the default profile created with ``aws configure`` will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#profile AwsProvider#profile}
        :param region: The region where AWS operations will take place. Examples are us-east-1, us-west-2, etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#region AwsProvider#region}
        :param retry_mode: Specifies how retries are attempted. Valid values are ``standard`` and ``adaptive``. Can also be configured using the ``AWS_RETRY_MODE`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#retry_mode AwsProvider#retry_mode}
        :param s3_us_east1_regional_endpoint: Specifies whether S3 API calls in the ``us-east-1`` region use the legacy global endpoint or a regional endpoint. Valid values are ``legacy`` or ``regional``. Can also be configured using the ``AWS_S3_US_EAST_1_REGIONAL_ENDPOINT`` environment variable or the ``s3_us_east_1_regional_endpoint`` shared config file parameter Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#s3_us_east_1_regional_endpoint AwsProvider#s3_us_east_1_regional_endpoint}
        :param s3_use_path_style: Set this to true to enable the request to use path-style addressing, i.e., https://s3.amazonaws.com/BUCKET/KEY. By default, the S3 client will use virtual hosted bucket addressing when possible (https://BUCKET.s3.amazonaws.com/KEY). Specific to the Amazon S3 service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#s3_use_path_style AwsProvider#s3_use_path_style}
        :param secret_key: The secret key for API operations. You can retrieve this from the 'Security & Credentials' section of the AWS console. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#secret_key AwsProvider#secret_key}
        :param shared_config_files: List of paths to shared config files. If not set, defaults to [~/.aws/config]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#shared_config_files AwsProvider#shared_config_files}
        :param shared_credentials_files: List of paths to shared credentials files. If not set, defaults to [~/.aws/credentials]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#shared_credentials_files AwsProvider#shared_credentials_files}
        :param skip_credentials_validation: Skip the credentials validation via STS API. Used for AWS API implementations that do not have STS available/implemented. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#skip_credentials_validation AwsProvider#skip_credentials_validation}
        :param skip_metadata_api_check: Skip the AWS Metadata API check. Used for AWS API implementations that do not have a metadata api endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#skip_metadata_api_check AwsProvider#skip_metadata_api_check}
        :param skip_region_validation: Skip static validation of region name. Used by users of alternative AWS-like APIs or users w/ access to regions that are not public (yet). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#skip_region_validation AwsProvider#skip_region_validation}
        :param skip_requesting_account_id: Skip requesting the account ID. Used for AWS API implementations that do not have IAM/STS API and/or metadata API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#skip_requesting_account_id AwsProvider#skip_requesting_account_id}
        :param sts_region: The region where AWS STS operations will take place. Examples are us-east-1 and us-west-2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#sts_region AwsProvider#sts_region}
        :param token: session token. A session token is only required if you are using temporary security credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#token AwsProvider#token}
        :param token_bucket_rate_limiter_capacity: The capacity of the AWS SDK's token bucket rate limiter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#token_bucket_rate_limiter_capacity AwsProvider#token_bucket_rate_limiter_capacity}
        :param use_dualstack_endpoint: Resolve an endpoint with DualStack capability. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#use_dualstack_endpoint AwsProvider#use_dualstack_endpoint}
        :param use_fips_endpoint: Resolve an endpoint with FIPS capability. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#use_fips_endpoint AwsProvider#use_fips_endpoint}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57740e84c090e6dbbe5013b04d4825b1e91195924e8b2a3215a201c1b6c1db94)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = AwsProviderConfig(
            access_key=access_key,
            alias=alias,
            allowed_account_ids=allowed_account_ids,
            assume_role=assume_role,
            assume_role_with_web_identity=assume_role_with_web_identity,
            custom_ca_bundle=custom_ca_bundle,
            default_tags=default_tags,
            ec2_metadata_service_endpoint=ec2_metadata_service_endpoint,
            ec2_metadata_service_endpoint_mode=ec2_metadata_service_endpoint_mode,
            endpoints=endpoints,
            forbidden_account_ids=forbidden_account_ids,
            http_proxy=http_proxy,
            https_proxy=https_proxy,
            ignore_tags=ignore_tags,
            insecure=insecure,
            max_retries=max_retries,
            no_proxy=no_proxy,
            profile=profile,
            region=region,
            retry_mode=retry_mode,
            s3_us_east1_regional_endpoint=s3_us_east1_regional_endpoint,
            s3_use_path_style=s3_use_path_style,
            secret_key=secret_key,
            shared_config_files=shared_config_files,
            shared_credentials_files=shared_credentials_files,
            skip_credentials_validation=skip_credentials_validation,
            skip_metadata_api_check=skip_metadata_api_check,
            skip_region_validation=skip_region_validation,
            skip_requesting_account_id=skip_requesting_account_id,
            sts_region=sts_region,
            token=token,
            token_bucket_rate_limiter_capacity=token_bucket_rate_limiter_capacity,
            use_dualstack_endpoint=use_dualstack_endpoint,
            use_fips_endpoint=use_fips_endpoint,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a AwsProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AwsProvider to import.
        :param import_from_id: The id of the existing AwsProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AwsProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97e78c17cf7a315f66927ed4ef5a9f09ab06b83a94fb0847fa4ff1b7739c805b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAccessKey")
    def reset_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessKey", []))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetAllowedAccountIds")
    def reset_allowed_account_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedAccountIds", []))

    @jsii.member(jsii_name="resetAssumeRole")
    def reset_assume_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssumeRole", []))

    @jsii.member(jsii_name="resetAssumeRoleWithWebIdentity")
    def reset_assume_role_with_web_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssumeRoleWithWebIdentity", []))

    @jsii.member(jsii_name="resetCustomCaBundle")
    def reset_custom_ca_bundle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomCaBundle", []))

    @jsii.member(jsii_name="resetDefaultTags")
    def reset_default_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTags", []))

    @jsii.member(jsii_name="resetEc2MetadataServiceEndpoint")
    def reset_ec2_metadata_service_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEc2MetadataServiceEndpoint", []))

    @jsii.member(jsii_name="resetEc2MetadataServiceEndpointMode")
    def reset_ec2_metadata_service_endpoint_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEc2MetadataServiceEndpointMode", []))

    @jsii.member(jsii_name="resetEndpoints")
    def reset_endpoints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpoints", []))

    @jsii.member(jsii_name="resetForbiddenAccountIds")
    def reset_forbidden_account_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForbiddenAccountIds", []))

    @jsii.member(jsii_name="resetHttpProxy")
    def reset_http_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpProxy", []))

    @jsii.member(jsii_name="resetHttpsProxy")
    def reset_https_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsProxy", []))

    @jsii.member(jsii_name="resetIgnoreTags")
    def reset_ignore_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreTags", []))

    @jsii.member(jsii_name="resetInsecure")
    def reset_insecure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecure", []))

    @jsii.member(jsii_name="resetMaxRetries")
    def reset_max_retries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRetries", []))

    @jsii.member(jsii_name="resetNoProxy")
    def reset_no_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoProxy", []))

    @jsii.member(jsii_name="resetProfile")
    def reset_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProfile", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRetryMode")
    def reset_retry_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryMode", []))

    @jsii.member(jsii_name="resetS3UsEast1RegionalEndpoint")
    def reset_s3_us_east1_regional_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3UsEast1RegionalEndpoint", []))

    @jsii.member(jsii_name="resetS3UsePathStyle")
    def reset_s3_use_path_style(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3UsePathStyle", []))

    @jsii.member(jsii_name="resetSecretKey")
    def reset_secret_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretKey", []))

    @jsii.member(jsii_name="resetSharedConfigFiles")
    def reset_shared_config_files(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedConfigFiles", []))

    @jsii.member(jsii_name="resetSharedCredentialsFiles")
    def reset_shared_credentials_files(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedCredentialsFiles", []))

    @jsii.member(jsii_name="resetSkipCredentialsValidation")
    def reset_skip_credentials_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipCredentialsValidation", []))

    @jsii.member(jsii_name="resetSkipMetadataApiCheck")
    def reset_skip_metadata_api_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipMetadataApiCheck", []))

    @jsii.member(jsii_name="resetSkipRegionValidation")
    def reset_skip_region_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipRegionValidation", []))

    @jsii.member(jsii_name="resetSkipRequestingAccountId")
    def reset_skip_requesting_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipRequestingAccountId", []))

    @jsii.member(jsii_name="resetStsRegion")
    def reset_sts_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStsRegion", []))

    @jsii.member(jsii_name="resetToken")
    def reset_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToken", []))

    @jsii.member(jsii_name="resetTokenBucketRateLimiterCapacity")
    def reset_token_bucket_rate_limiter_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenBucketRateLimiterCapacity", []))

    @jsii.member(jsii_name="resetUseDualstackEndpoint")
    def reset_use_dualstack_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseDualstackEndpoint", []))

    @jsii.member(jsii_name="resetUseFipsEndpoint")
    def reset_use_fips_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseFipsEndpoint", []))

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
    @jsii.member(jsii_name="accessKeyInput")
    def access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedAccountIdsInput")
    def allowed_account_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedAccountIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleInput")
    def assume_role_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderAssumeRole"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderAssumeRole"]]], jsii.get(self, "assumeRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleWithWebIdentityInput")
    def assume_role_with_web_identity_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderAssumeRoleWithWebIdentity"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderAssumeRoleWithWebIdentity"]]], jsii.get(self, "assumeRoleWithWebIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="customCaBundleInput")
    def custom_ca_bundle_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customCaBundleInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTagsInput")
    def default_tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderDefaultTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderDefaultTags"]]], jsii.get(self, "defaultTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="ec2MetadataServiceEndpointInput")
    def ec2_metadata_service_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ec2MetadataServiceEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="ec2MetadataServiceEndpointModeInput")
    def ec2_metadata_service_endpoint_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ec2MetadataServiceEndpointModeInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointsInput")
    def endpoints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderEndpoints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderEndpoints"]]], jsii.get(self, "endpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="forbiddenAccountIdsInput")
    def forbidden_account_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "forbiddenAccountIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="httpProxyInput")
    def http_proxy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsProxyInput")
    def https_proxy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpsProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreTagsInput")
    def ignore_tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderIgnoreTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderIgnoreTags"]]], jsii.get(self, "ignoreTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureInput")
    def insecure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetriesInput")
    def max_retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetriesInput"))

    @builtins.property
    @jsii.member(jsii_name="noProxyInput")
    def no_proxy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "noProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="profileInput")
    def profile_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "profileInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="retryModeInput")
    def retry_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retryModeInput"))

    @builtins.property
    @jsii.member(jsii_name="s3UsEast1RegionalEndpointInput")
    def s3_us_east1_regional_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3UsEast1RegionalEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="s3UsePathStyleInput")
    def s3_use_path_style_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "s3UsePathStyleInput"))

    @builtins.property
    @jsii.member(jsii_name="secretKeyInput")
    def secret_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedConfigFilesInput")
    def shared_config_files_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sharedConfigFilesInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedCredentialsFilesInput")
    def shared_credentials_files_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sharedCredentialsFilesInput"))

    @builtins.property
    @jsii.member(jsii_name="skipCredentialsValidationInput")
    def skip_credentials_validation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipCredentialsValidationInput"))

    @builtins.property
    @jsii.member(jsii_name="skipMetadataApiCheckInput")
    def skip_metadata_api_check_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skipMetadataApiCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="skipRegionValidationInput")
    def skip_region_validation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipRegionValidationInput"))

    @builtins.property
    @jsii.member(jsii_name="skipRequestingAccountIdInput")
    def skip_requesting_account_id_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipRequestingAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="stsRegionInput")
    def sts_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stsRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenBucketRateLimiterCapacityInput")
    def token_bucket_rate_limiter_capacity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tokenBucketRateLimiterCapacityInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property
    @jsii.member(jsii_name="useDualstackEndpointInput")
    def use_dualstack_endpoint_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useDualstackEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="useFipsEndpointInput")
    def use_fips_endpoint_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useFipsEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKey")
    def access_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKey"))

    @access_key.setter
    def access_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f97caf30c4cf5d143ef30e715a281fe5c381f8cf27b32e70b7a2b1302ce9ff5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80bc4aff31cfdf4f07483a4c8d21f0b0eaa38b8f34caf268f8927000ed57c646)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedAccountIds")
    def allowed_account_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedAccountIds"))

    @allowed_account_ids.setter
    def allowed_account_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4f91cb0e9acead45005abbe4dca4dbe00f3208583db5f83d19b04810a167964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedAccountIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="assumeRole")
    def assume_role(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderAssumeRole"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderAssumeRole"]]], jsii.get(self, "assumeRole"))

    @assume_role.setter
    def assume_role(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderAssumeRole"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88a81471684ebb3aa894bba1ea2087f5c39224c89e73be35717bbf2ccc2c958)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assumeRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="assumeRoleWithWebIdentity")
    def assume_role_with_web_identity(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderAssumeRoleWithWebIdentity"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderAssumeRoleWithWebIdentity"]]], jsii.get(self, "assumeRoleWithWebIdentity"))

    @assume_role_with_web_identity.setter
    def assume_role_with_web_identity(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderAssumeRoleWithWebIdentity"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d844f5622298fa89e8fae92c37ff32dfef0b12e23ea848b4ce5eb51a8620ef1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assumeRoleWithWebIdentity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customCaBundle")
    def custom_ca_bundle(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customCaBundle"))

    @custom_ca_bundle.setter
    def custom_ca_bundle(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1bd9f29fa431038e30d34bfb80ae9fa177daa980dc396c0088189d957ae7dba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customCaBundle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTags")
    def default_tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderDefaultTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderDefaultTags"]]], jsii.get(self, "defaultTags"))

    @default_tags.setter
    def default_tags(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderDefaultTags"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69b993e01bdc539cfc190aee74f85d3362f7d07350b4eab2fc55a588e999bee2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ec2MetadataServiceEndpoint")
    def ec2_metadata_service_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ec2MetadataServiceEndpoint"))

    @ec2_metadata_service_endpoint.setter
    def ec2_metadata_service_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eca099fd728ddcbbec4df07840db7fecd1c88cbc3c12f2f897a6025e1b660ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ec2MetadataServiceEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ec2MetadataServiceEndpointMode")
    def ec2_metadata_service_endpoint_mode(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ec2MetadataServiceEndpointMode"))

    @ec2_metadata_service_endpoint_mode.setter
    def ec2_metadata_service_endpoint_mode(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6dee424cdb153a32b34e98d3002fcac5cd19addc01eee013306179206b0a99f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ec2MetadataServiceEndpointMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpoints")
    def endpoints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderEndpoints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderEndpoints"]]], jsii.get(self, "endpoints"))

    @endpoints.setter
    def endpoints(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderEndpoints"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9292ea3762e5c9b3e0beb785585e41485d8a33c9db5dce2b7e0296fc1a8f49b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forbiddenAccountIds")
    def forbidden_account_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "forbiddenAccountIds"))

    @forbidden_account_ids.setter
    def forbidden_account_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc9326a1717f217ef9b1645ad004cccb304224f730752a61a1f896444cf45ddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forbiddenAccountIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpProxy")
    def http_proxy(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpProxy"))

    @http_proxy.setter
    def http_proxy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e6f631015bc72081aa457cc57dfeb85ceb558a0e146df7fc77701a74122599d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpProxy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsProxy")
    def https_proxy(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpsProxy"))

    @https_proxy.setter
    def https_proxy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12f28a6714d54dee0b149d57dc1bd4b07b2d055ba95dcb4cab6a510ee8e57670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsProxy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreTags")
    def ignore_tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderIgnoreTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderIgnoreTags"]]], jsii.get(self, "ignoreTags"))

    @ignore_tags.setter
    def ignore_tags(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderIgnoreTags"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__882b429a5604fb9e73677d843c115941f86b0b8871d5830fba8aa41437555217)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="insecure")
    def insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecure"))

    @insecure.setter
    def insecure(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad49c472700312804b8dd445cd2a191de2700777ae6f5fa260b1ed52a6b5599a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetries"))

    @max_retries.setter
    def max_retries(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaea293f15020e29fe5694012019b9e582971c4f3a5e0065e14c8eca9ae7046c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noProxy")
    def no_proxy(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "noProxy"))

    @no_proxy.setter
    def no_proxy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7318c0da3dc9966e57d2b428a99e595a40962e0f406bf7b3a821f0c91d4e28a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noProxy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="profile")
    def profile(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "profile"))

    @profile.setter
    def profile(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d57fe9789911b3d82c8d661f330959d76ee2dc7869c1cb75b5898acdf94ed4a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))

    @region.setter
    def region(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__486ee42567ffa21efb6d1b916f69581e45a9e0ff38292723c9b498fa98dda526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryMode")
    def retry_mode(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retryMode"))

    @retry_mode.setter
    def retry_mode(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f7e5f9072d44c6a1c54564b6843b0be4e07831bcfc5cac3a29ae58798d3fb64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3UsEast1RegionalEndpoint")
    def s3_us_east1_regional_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3UsEast1RegionalEndpoint"))

    @s3_us_east1_regional_endpoint.setter
    def s3_us_east1_regional_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93b2f848f06249f754ac63a17186248922a5145053012a5e1fd8b20fe1767f16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3UsEast1RegionalEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3UsePathStyle")
    def s3_use_path_style(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "s3UsePathStyle"))

    @s3_use_path_style.setter
    def s3_use_path_style(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ac7770c17b68cc6a4e85c6fabe6315963a8ab254b42904391c9b1964f98d38a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3UsePathStyle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretKey")
    def secret_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretKey"))

    @secret_key.setter
    def secret_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0460c2812f02da34e13a8964d21b5d351f0635480d9b4dce558c8aea77724db9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sharedConfigFiles")
    def shared_config_files(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sharedConfigFiles"))

    @shared_config_files.setter
    def shared_config_files(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c60eecbf5578be99fd002ddbde2feddef3694af92d196eccb29433a6e983153a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedConfigFiles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sharedCredentialsFiles")
    def shared_credentials_files(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sharedCredentialsFiles"))

    @shared_credentials_files.setter
    def shared_credentials_files(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b37bd9c05dcccbe57be6cacdad7a6c8380cba5a4c33868839bda7f47347b9d4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedCredentialsFiles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipCredentialsValidation")
    def skip_credentials_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipCredentialsValidation"))

    @skip_credentials_validation.setter
    def skip_credentials_validation(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65219b90d8b6318afd7e39f491b2b8a793a7771d6c1ece83185513bd9d0f12d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipCredentialsValidation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipMetadataApiCheck")
    def skip_metadata_api_check(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skipMetadataApiCheck"))

    @skip_metadata_api_check.setter
    def skip_metadata_api_check(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aadf2f6ea203c5d94ac4f94eccee099c4748b449f24cc82cea9660b2b19ee15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipMetadataApiCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipRegionValidation")
    def skip_region_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipRegionValidation"))

    @skip_region_validation.setter
    def skip_region_validation(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b32ce7eb1f5c845c19a0746b0149f5c906e1ce856471e9f80a9d148bcb90605)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipRegionValidation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipRequestingAccountId")
    def skip_requesting_account_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipRequestingAccountId"))

    @skip_requesting_account_id.setter
    def skip_requesting_account_id(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cf644a8308df17711c61e179978fbebba6266c3263e29c36275d80f944ace12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipRequestingAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stsRegion")
    def sts_region(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stsRegion"))

    @sts_region.setter
    def sts_region(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf6f79c369d9fce42df29616927a4b96275f18adf0f5ad2b137078c93f5b831f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stsRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "token"))

    @token.setter
    def token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a333bb63ca035e85037d8113d29d49027dbe991c253604d7ad91f5a9c8a4684)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "token", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenBucketRateLimiterCapacity")
    def token_bucket_rate_limiter_capacity(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tokenBucketRateLimiterCapacity"))

    @token_bucket_rate_limiter_capacity.setter
    def token_bucket_rate_limiter_capacity(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3095656322017f1dd9c0b5c48c0e69a22ee51fb0dc402203743a6d953f108a4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenBucketRateLimiterCapacity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useDualstackEndpoint")
    def use_dualstack_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useDualstackEndpoint"))

    @use_dualstack_endpoint.setter
    def use_dualstack_endpoint(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec35f69a49d58d30e4bb74a3b9f095c5c5e3ef3f164a3492b095215510b1eff2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useDualstackEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useFipsEndpoint")
    def use_fips_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useFipsEndpoint"))

    @use_fips_endpoint.setter
    def use_fips_endpoint(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f442a7233365631a5f3a2908a1ad10a79fefcaf2c29b6b2a57e7faae8f9e0494)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useFipsEndpoint", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.provider.AwsProviderAssumeRole",
    jsii_struct_bases=[],
    name_mapping={
        "duration": "duration",
        "external_id": "externalId",
        "policy": "policy",
        "policy_arns": "policyArns",
        "role_arn": "roleArn",
        "session_name": "sessionName",
        "source_identity": "sourceIdentity",
        "tags": "tags",
        "transitive_tag_keys": "transitiveTagKeys",
    },
)
class AwsProviderAssumeRole:
    def __init__(
        self,
        *,
        duration: typing.Optional[builtins.str] = None,
        external_id: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        session_name: typing.Optional[builtins.str] = None,
        source_identity: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        transitive_tag_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param duration: The duration, between 15 minutes and 12 hours, of the role session. Valid time units are ns, us (or µs), ms, s, h, or m. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#duration AwsProvider#duration}
        :param external_id: A unique identifier that might be required when you assume a role in another account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#external_id AwsProvider#external_id}
        :param policy: IAM Policy JSON describing further restricting permissions for the IAM Role being assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#policy AwsProvider#policy}
        :param policy_arns: Amazon Resource Names (ARNs) of IAM Policies describing further restricting permissions for the IAM Role being assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#policy_arns AwsProvider#policy_arns}
        :param role_arn: Amazon Resource Name (ARN) of an IAM Role to assume prior to making API calls. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#role_arn AwsProvider#role_arn}
        :param session_name: An identifier for the assumed role session. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#session_name AwsProvider#session_name}
        :param source_identity: Source identity specified by the principal assuming the role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#source_identity AwsProvider#source_identity}
        :param tags: Assume role session tags. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#tags AwsProvider#tags}
        :param transitive_tag_keys: Assume role session tag keys to pass to any subsequent sessions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#transitive_tag_keys AwsProvider#transitive_tag_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e13c9cf89749eaaf5dd0a7fae994b4dd66132f149e51e34cc333614df59c7ace)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument policy_arns", value=policy_arns, expected_type=type_hints["policy_arns"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument session_name", value=session_name, expected_type=type_hints["session_name"])
            check_type(argname="argument source_identity", value=source_identity, expected_type=type_hints["source_identity"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument transitive_tag_keys", value=transitive_tag_keys, expected_type=type_hints["transitive_tag_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if duration is not None:
            self._values["duration"] = duration
        if external_id is not None:
            self._values["external_id"] = external_id
        if policy is not None:
            self._values["policy"] = policy
        if policy_arns is not None:
            self._values["policy_arns"] = policy_arns
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if session_name is not None:
            self._values["session_name"] = session_name
        if source_identity is not None:
            self._values["source_identity"] = source_identity
        if tags is not None:
            self._values["tags"] = tags
        if transitive_tag_keys is not None:
            self._values["transitive_tag_keys"] = transitive_tag_keys

    @builtins.property
    def duration(self) -> typing.Optional[builtins.str]:
        '''The duration, between 15 minutes and 12 hours, of the role session.

        Valid time units are ns, us (or µs), ms, s, h, or m.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#duration AwsProvider#duration}
        '''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_id(self) -> typing.Optional[builtins.str]:
        '''A unique identifier that might be required when you assume a role in another account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#external_id AwsProvider#external_id}
        '''
        result = self._values.get("external_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''IAM Policy JSON describing further restricting permissions for the IAM Role being assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#policy AwsProvider#policy}
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Amazon Resource Names (ARNs) of IAM Policies describing further restricting permissions for the IAM Role being assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#policy_arns AwsProvider#policy_arns}
        '''
        result = self._values.get("policy_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''Amazon Resource Name (ARN) of an IAM Role to assume prior to making API calls.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#role_arn AwsProvider#role_arn}
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_name(self) -> typing.Optional[builtins.str]:
        '''An identifier for the assumed role session.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#session_name AwsProvider#session_name}
        '''
        result = self._values.get("session_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_identity(self) -> typing.Optional[builtins.str]:
        '''Source identity specified by the principal assuming the role.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#source_identity AwsProvider#source_identity}
        '''
        result = self._values.get("source_identity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Assume role session tags.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#tags AwsProvider#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def transitive_tag_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Assume role session tag keys to pass to any subsequent sessions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#transitive_tag_keys AwsProvider#transitive_tag_keys}
        '''
        result = self._values.get("transitive_tag_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsProviderAssumeRole(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.provider.AwsProviderAssumeRoleWithWebIdentity",
    jsii_struct_bases=[],
    name_mapping={
        "duration": "duration",
        "policy": "policy",
        "policy_arns": "policyArns",
        "role_arn": "roleArn",
        "session_name": "sessionName",
        "web_identity_token": "webIdentityToken",
        "web_identity_token_file": "webIdentityTokenFile",
    },
)
class AwsProviderAssumeRoleWithWebIdentity:
    def __init__(
        self,
        *,
        duration: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        session_name: typing.Optional[builtins.str] = None,
        web_identity_token: typing.Optional[builtins.str] = None,
        web_identity_token_file: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param duration: The duration, between 15 minutes and 12 hours, of the role session. Valid time units are ns, us (or µs), ms, s, h, or m. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#duration AwsProvider#duration}
        :param policy: IAM Policy JSON describing further restricting permissions for the IAM Role being assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#policy AwsProvider#policy}
        :param policy_arns: Amazon Resource Names (ARNs) of IAM Policies describing further restricting permissions for the IAM Role being assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#policy_arns AwsProvider#policy_arns}
        :param role_arn: Amazon Resource Name (ARN) of an IAM Role to assume prior to making API calls. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#role_arn AwsProvider#role_arn}
        :param session_name: An identifier for the assumed role session. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#session_name AwsProvider#session_name}
        :param web_identity_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#web_identity_token AwsProvider#web_identity_token}.
        :param web_identity_token_file: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#web_identity_token_file AwsProvider#web_identity_token_file}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__006dfde6bb37b5cb603bf04cf9efc9a9b9ccdaab3e3bf265876fbf07e7e867b3)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument policy_arns", value=policy_arns, expected_type=type_hints["policy_arns"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument session_name", value=session_name, expected_type=type_hints["session_name"])
            check_type(argname="argument web_identity_token", value=web_identity_token, expected_type=type_hints["web_identity_token"])
            check_type(argname="argument web_identity_token_file", value=web_identity_token_file, expected_type=type_hints["web_identity_token_file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if duration is not None:
            self._values["duration"] = duration
        if policy is not None:
            self._values["policy"] = policy
        if policy_arns is not None:
            self._values["policy_arns"] = policy_arns
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if session_name is not None:
            self._values["session_name"] = session_name
        if web_identity_token is not None:
            self._values["web_identity_token"] = web_identity_token
        if web_identity_token_file is not None:
            self._values["web_identity_token_file"] = web_identity_token_file

    @builtins.property
    def duration(self) -> typing.Optional[builtins.str]:
        '''The duration, between 15 minutes and 12 hours, of the role session.

        Valid time units are ns, us (or µs), ms, s, h, or m.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#duration AwsProvider#duration}
        '''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''IAM Policy JSON describing further restricting permissions for the IAM Role being assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#policy AwsProvider#policy}
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Amazon Resource Names (ARNs) of IAM Policies describing further restricting permissions for the IAM Role being assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#policy_arns AwsProvider#policy_arns}
        '''
        result = self._values.get("policy_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''Amazon Resource Name (ARN) of an IAM Role to assume prior to making API calls.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#role_arn AwsProvider#role_arn}
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_name(self) -> typing.Optional[builtins.str]:
        '''An identifier for the assumed role session.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#session_name AwsProvider#session_name}
        '''
        result = self._values.get("session_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def web_identity_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#web_identity_token AwsProvider#web_identity_token}.'''
        result = self._values.get("web_identity_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def web_identity_token_file(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#web_identity_token_file AwsProvider#web_identity_token_file}.'''
        result = self._values.get("web_identity_token_file")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsProviderAssumeRoleWithWebIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.provider.AwsProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "access_key": "accessKey",
        "alias": "alias",
        "allowed_account_ids": "allowedAccountIds",
        "assume_role": "assumeRole",
        "assume_role_with_web_identity": "assumeRoleWithWebIdentity",
        "custom_ca_bundle": "customCaBundle",
        "default_tags": "defaultTags",
        "ec2_metadata_service_endpoint": "ec2MetadataServiceEndpoint",
        "ec2_metadata_service_endpoint_mode": "ec2MetadataServiceEndpointMode",
        "endpoints": "endpoints",
        "forbidden_account_ids": "forbiddenAccountIds",
        "http_proxy": "httpProxy",
        "https_proxy": "httpsProxy",
        "ignore_tags": "ignoreTags",
        "insecure": "insecure",
        "max_retries": "maxRetries",
        "no_proxy": "noProxy",
        "profile": "profile",
        "region": "region",
        "retry_mode": "retryMode",
        "s3_us_east1_regional_endpoint": "s3UsEast1RegionalEndpoint",
        "s3_use_path_style": "s3UsePathStyle",
        "secret_key": "secretKey",
        "shared_config_files": "sharedConfigFiles",
        "shared_credentials_files": "sharedCredentialsFiles",
        "skip_credentials_validation": "skipCredentialsValidation",
        "skip_metadata_api_check": "skipMetadataApiCheck",
        "skip_region_validation": "skipRegionValidation",
        "skip_requesting_account_id": "skipRequestingAccountId",
        "sts_region": "stsRegion",
        "token": "token",
        "token_bucket_rate_limiter_capacity": "tokenBucketRateLimiterCapacity",
        "use_dualstack_endpoint": "useDualstackEndpoint",
        "use_fips_endpoint": "useFipsEndpoint",
    },
)
class AwsProviderConfig:
    def __init__(
        self,
        *,
        access_key: typing.Optional[builtins.str] = None,
        alias: typing.Optional[builtins.str] = None,
        allowed_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        assume_role: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AwsProviderAssumeRole, typing.Dict[builtins.str, typing.Any]]]]] = None,
        assume_role_with_web_identity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AwsProviderAssumeRoleWithWebIdentity, typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_ca_bundle: typing.Optional[builtins.str] = None,
        default_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AwsProviderDefaultTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ec2_metadata_service_endpoint: typing.Optional[builtins.str] = None,
        ec2_metadata_service_endpoint_mode: typing.Optional[builtins.str] = None,
        endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AwsProviderEndpoints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        forbidden_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        http_proxy: typing.Optional[builtins.str] = None,
        https_proxy: typing.Optional[builtins.str] = None,
        ignore_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AwsProviderIgnoreTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        no_proxy: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        retry_mode: typing.Optional[builtins.str] = None,
        s3_us_east1_regional_endpoint: typing.Optional[builtins.str] = None,
        s3_use_path_style: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_key: typing.Optional[builtins.str] = None,
        shared_config_files: typing.Optional[typing.Sequence[builtins.str]] = None,
        shared_credentials_files: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_credentials_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_metadata_api_check: typing.Optional[builtins.str] = None,
        skip_region_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_requesting_account_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sts_region: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        token_bucket_rate_limiter_capacity: typing.Optional[jsii.Number] = None,
        use_dualstack_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_fips_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param access_key: The access key for API operations. You can retrieve this from the 'Security & Credentials' section of the AWS console. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#access_key AwsProvider#access_key}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#alias AwsProvider#alias}
        :param allowed_account_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#allowed_account_ids AwsProvider#allowed_account_ids}.
        :param assume_role: assume_role block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#assume_role AwsProvider#assume_role}
        :param assume_role_with_web_identity: assume_role_with_web_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#assume_role_with_web_identity AwsProvider#assume_role_with_web_identity}
        :param custom_ca_bundle: File containing custom root and intermediate certificates. Can also be configured using the ``AWS_CA_BUNDLE`` environment variable. (Setting ``ca_bundle`` in the shared config file is not supported.) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#custom_ca_bundle AwsProvider#custom_ca_bundle}
        :param default_tags: default_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#default_tags AwsProvider#default_tags}
        :param ec2_metadata_service_endpoint: Address of the EC2 metadata service endpoint to use. Can also be configured using the ``AWS_EC2_METADATA_SERVICE_ENDPOINT`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ec2_metadata_service_endpoint AwsProvider#ec2_metadata_service_endpoint}
        :param ec2_metadata_service_endpoint_mode: Protocol to use with EC2 metadata service endpoint.Valid values are ``IPv4`` and ``IPv6``. Can also be configured using the ``AWS_EC2_METADATA_SERVICE_ENDPOINT_MODE`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ec2_metadata_service_endpoint_mode AwsProvider#ec2_metadata_service_endpoint_mode}
        :param endpoints: endpoints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#endpoints AwsProvider#endpoints}
        :param forbidden_account_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#forbidden_account_ids AwsProvider#forbidden_account_ids}.
        :param http_proxy: URL of a proxy to use for HTTP requests when accessing the AWS API. Can also be set using the ``HTTP_PROXY`` or ``http_proxy`` environment variables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#http_proxy AwsProvider#http_proxy}
        :param https_proxy: URL of a proxy to use for HTTPS requests when accessing the AWS API. Can also be set using the ``HTTPS_PROXY`` or ``https_proxy`` environment variables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#https_proxy AwsProvider#https_proxy}
        :param ignore_tags: ignore_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ignore_tags AwsProvider#ignore_tags}
        :param insecure: Explicitly allow the provider to perform "insecure" SSL requests. If omitted, default value is ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#insecure AwsProvider#insecure}
        :param max_retries: The maximum number of times an AWS API request is being executed. If the API request still fails, an error is thrown. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#max_retries AwsProvider#max_retries}
        :param no_proxy: Comma-separated list of hosts that should not use HTTP or HTTPS proxies. Can also be set using the ``NO_PROXY`` or ``no_proxy`` environment variables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#no_proxy AwsProvider#no_proxy}
        :param profile: The profile for API operations. If not set, the default profile created with ``aws configure`` will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#profile AwsProvider#profile}
        :param region: The region where AWS operations will take place. Examples are us-east-1, us-west-2, etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#region AwsProvider#region}
        :param retry_mode: Specifies how retries are attempted. Valid values are ``standard`` and ``adaptive``. Can also be configured using the ``AWS_RETRY_MODE`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#retry_mode AwsProvider#retry_mode}
        :param s3_us_east1_regional_endpoint: Specifies whether S3 API calls in the ``us-east-1`` region use the legacy global endpoint or a regional endpoint. Valid values are ``legacy`` or ``regional``. Can also be configured using the ``AWS_S3_US_EAST_1_REGIONAL_ENDPOINT`` environment variable or the ``s3_us_east_1_regional_endpoint`` shared config file parameter Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#s3_us_east_1_regional_endpoint AwsProvider#s3_us_east_1_regional_endpoint}
        :param s3_use_path_style: Set this to true to enable the request to use path-style addressing, i.e., https://s3.amazonaws.com/BUCKET/KEY. By default, the S3 client will use virtual hosted bucket addressing when possible (https://BUCKET.s3.amazonaws.com/KEY). Specific to the Amazon S3 service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#s3_use_path_style AwsProvider#s3_use_path_style}
        :param secret_key: The secret key for API operations. You can retrieve this from the 'Security & Credentials' section of the AWS console. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#secret_key AwsProvider#secret_key}
        :param shared_config_files: List of paths to shared config files. If not set, defaults to [~/.aws/config]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#shared_config_files AwsProvider#shared_config_files}
        :param shared_credentials_files: List of paths to shared credentials files. If not set, defaults to [~/.aws/credentials]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#shared_credentials_files AwsProvider#shared_credentials_files}
        :param skip_credentials_validation: Skip the credentials validation via STS API. Used for AWS API implementations that do not have STS available/implemented. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#skip_credentials_validation AwsProvider#skip_credentials_validation}
        :param skip_metadata_api_check: Skip the AWS Metadata API check. Used for AWS API implementations that do not have a metadata api endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#skip_metadata_api_check AwsProvider#skip_metadata_api_check}
        :param skip_region_validation: Skip static validation of region name. Used by users of alternative AWS-like APIs or users w/ access to regions that are not public (yet). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#skip_region_validation AwsProvider#skip_region_validation}
        :param skip_requesting_account_id: Skip requesting the account ID. Used for AWS API implementations that do not have IAM/STS API and/or metadata API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#skip_requesting_account_id AwsProvider#skip_requesting_account_id}
        :param sts_region: The region where AWS STS operations will take place. Examples are us-east-1 and us-west-2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#sts_region AwsProvider#sts_region}
        :param token: session token. A session token is only required if you are using temporary security credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#token AwsProvider#token}
        :param token_bucket_rate_limiter_capacity: The capacity of the AWS SDK's token bucket rate limiter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#token_bucket_rate_limiter_capacity AwsProvider#token_bucket_rate_limiter_capacity}
        :param use_dualstack_endpoint: Resolve an endpoint with DualStack capability. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#use_dualstack_endpoint AwsProvider#use_dualstack_endpoint}
        :param use_fips_endpoint: Resolve an endpoint with FIPS capability. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#use_fips_endpoint AwsProvider#use_fips_endpoint}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c594a8866496614f028e2c928d60f10d6094c47bbfd585fb76f5f791591813c3)
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument allowed_account_ids", value=allowed_account_ids, expected_type=type_hints["allowed_account_ids"])
            check_type(argname="argument assume_role", value=assume_role, expected_type=type_hints["assume_role"])
            check_type(argname="argument assume_role_with_web_identity", value=assume_role_with_web_identity, expected_type=type_hints["assume_role_with_web_identity"])
            check_type(argname="argument custom_ca_bundle", value=custom_ca_bundle, expected_type=type_hints["custom_ca_bundle"])
            check_type(argname="argument default_tags", value=default_tags, expected_type=type_hints["default_tags"])
            check_type(argname="argument ec2_metadata_service_endpoint", value=ec2_metadata_service_endpoint, expected_type=type_hints["ec2_metadata_service_endpoint"])
            check_type(argname="argument ec2_metadata_service_endpoint_mode", value=ec2_metadata_service_endpoint_mode, expected_type=type_hints["ec2_metadata_service_endpoint_mode"])
            check_type(argname="argument endpoints", value=endpoints, expected_type=type_hints["endpoints"])
            check_type(argname="argument forbidden_account_ids", value=forbidden_account_ids, expected_type=type_hints["forbidden_account_ids"])
            check_type(argname="argument http_proxy", value=http_proxy, expected_type=type_hints["http_proxy"])
            check_type(argname="argument https_proxy", value=https_proxy, expected_type=type_hints["https_proxy"])
            check_type(argname="argument ignore_tags", value=ignore_tags, expected_type=type_hints["ignore_tags"])
            check_type(argname="argument insecure", value=insecure, expected_type=type_hints["insecure"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument no_proxy", value=no_proxy, expected_type=type_hints["no_proxy"])
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument retry_mode", value=retry_mode, expected_type=type_hints["retry_mode"])
            check_type(argname="argument s3_us_east1_regional_endpoint", value=s3_us_east1_regional_endpoint, expected_type=type_hints["s3_us_east1_regional_endpoint"])
            check_type(argname="argument s3_use_path_style", value=s3_use_path_style, expected_type=type_hints["s3_use_path_style"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
            check_type(argname="argument shared_config_files", value=shared_config_files, expected_type=type_hints["shared_config_files"])
            check_type(argname="argument shared_credentials_files", value=shared_credentials_files, expected_type=type_hints["shared_credentials_files"])
            check_type(argname="argument skip_credentials_validation", value=skip_credentials_validation, expected_type=type_hints["skip_credentials_validation"])
            check_type(argname="argument skip_metadata_api_check", value=skip_metadata_api_check, expected_type=type_hints["skip_metadata_api_check"])
            check_type(argname="argument skip_region_validation", value=skip_region_validation, expected_type=type_hints["skip_region_validation"])
            check_type(argname="argument skip_requesting_account_id", value=skip_requesting_account_id, expected_type=type_hints["skip_requesting_account_id"])
            check_type(argname="argument sts_region", value=sts_region, expected_type=type_hints["sts_region"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument token_bucket_rate_limiter_capacity", value=token_bucket_rate_limiter_capacity, expected_type=type_hints["token_bucket_rate_limiter_capacity"])
            check_type(argname="argument use_dualstack_endpoint", value=use_dualstack_endpoint, expected_type=type_hints["use_dualstack_endpoint"])
            check_type(argname="argument use_fips_endpoint", value=use_fips_endpoint, expected_type=type_hints["use_fips_endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_key is not None:
            self._values["access_key"] = access_key
        if alias is not None:
            self._values["alias"] = alias
        if allowed_account_ids is not None:
            self._values["allowed_account_ids"] = allowed_account_ids
        if assume_role is not None:
            self._values["assume_role"] = assume_role
        if assume_role_with_web_identity is not None:
            self._values["assume_role_with_web_identity"] = assume_role_with_web_identity
        if custom_ca_bundle is not None:
            self._values["custom_ca_bundle"] = custom_ca_bundle
        if default_tags is not None:
            self._values["default_tags"] = default_tags
        if ec2_metadata_service_endpoint is not None:
            self._values["ec2_metadata_service_endpoint"] = ec2_metadata_service_endpoint
        if ec2_metadata_service_endpoint_mode is not None:
            self._values["ec2_metadata_service_endpoint_mode"] = ec2_metadata_service_endpoint_mode
        if endpoints is not None:
            self._values["endpoints"] = endpoints
        if forbidden_account_ids is not None:
            self._values["forbidden_account_ids"] = forbidden_account_ids
        if http_proxy is not None:
            self._values["http_proxy"] = http_proxy
        if https_proxy is not None:
            self._values["https_proxy"] = https_proxy
        if ignore_tags is not None:
            self._values["ignore_tags"] = ignore_tags
        if insecure is not None:
            self._values["insecure"] = insecure
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if no_proxy is not None:
            self._values["no_proxy"] = no_proxy
        if profile is not None:
            self._values["profile"] = profile
        if region is not None:
            self._values["region"] = region
        if retry_mode is not None:
            self._values["retry_mode"] = retry_mode
        if s3_us_east1_regional_endpoint is not None:
            self._values["s3_us_east1_regional_endpoint"] = s3_us_east1_regional_endpoint
        if s3_use_path_style is not None:
            self._values["s3_use_path_style"] = s3_use_path_style
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if shared_config_files is not None:
            self._values["shared_config_files"] = shared_config_files
        if shared_credentials_files is not None:
            self._values["shared_credentials_files"] = shared_credentials_files
        if skip_credentials_validation is not None:
            self._values["skip_credentials_validation"] = skip_credentials_validation
        if skip_metadata_api_check is not None:
            self._values["skip_metadata_api_check"] = skip_metadata_api_check
        if skip_region_validation is not None:
            self._values["skip_region_validation"] = skip_region_validation
        if skip_requesting_account_id is not None:
            self._values["skip_requesting_account_id"] = skip_requesting_account_id
        if sts_region is not None:
            self._values["sts_region"] = sts_region
        if token is not None:
            self._values["token"] = token
        if token_bucket_rate_limiter_capacity is not None:
            self._values["token_bucket_rate_limiter_capacity"] = token_bucket_rate_limiter_capacity
        if use_dualstack_endpoint is not None:
            self._values["use_dualstack_endpoint"] = use_dualstack_endpoint
        if use_fips_endpoint is not None:
            self._values["use_fips_endpoint"] = use_fips_endpoint

    @builtins.property
    def access_key(self) -> typing.Optional[builtins.str]:
        '''The access key for API operations. You can retrieve this from the 'Security & Credentials' section of the AWS console.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#access_key AwsProvider#access_key}
        '''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#alias AwsProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allowed_account_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#allowed_account_ids AwsProvider#allowed_account_ids}.'''
        result = self._values.get("allowed_account_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def assume_role(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AwsProviderAssumeRole]]]:
        '''assume_role block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#assume_role AwsProvider#assume_role}
        '''
        result = self._values.get("assume_role")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AwsProviderAssumeRole]]], result)

    @builtins.property
    def assume_role_with_web_identity(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AwsProviderAssumeRoleWithWebIdentity]]]:
        '''assume_role_with_web_identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#assume_role_with_web_identity AwsProvider#assume_role_with_web_identity}
        '''
        result = self._values.get("assume_role_with_web_identity")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AwsProviderAssumeRoleWithWebIdentity]]], result)

    @builtins.property
    def custom_ca_bundle(self) -> typing.Optional[builtins.str]:
        '''File containing custom root and intermediate certificates.

        Can also be configured using the ``AWS_CA_BUNDLE`` environment variable. (Setting ``ca_bundle`` in the shared config file is not supported.)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#custom_ca_bundle AwsProvider#custom_ca_bundle}
        '''
        result = self._values.get("custom_ca_bundle")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderDefaultTags"]]]:
        '''default_tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#default_tags AwsProvider#default_tags}
        '''
        result = self._values.get("default_tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderDefaultTags"]]], result)

    @builtins.property
    def ec2_metadata_service_endpoint(self) -> typing.Optional[builtins.str]:
        '''Address of the EC2 metadata service endpoint to use. Can also be configured using the ``AWS_EC2_METADATA_SERVICE_ENDPOINT`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ec2_metadata_service_endpoint AwsProvider#ec2_metadata_service_endpoint}
        '''
        result = self._values.get("ec2_metadata_service_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2_metadata_service_endpoint_mode(self) -> typing.Optional[builtins.str]:
        '''Protocol to use with EC2 metadata service endpoint.Valid values are ``IPv4`` and ``IPv6``. Can also be configured using the ``AWS_EC2_METADATA_SERVICE_ENDPOINT_MODE`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ec2_metadata_service_endpoint_mode AwsProvider#ec2_metadata_service_endpoint_mode}
        '''
        result = self._values.get("ec2_metadata_service_endpoint_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderEndpoints"]]]:
        '''endpoints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#endpoints AwsProvider#endpoints}
        '''
        result = self._values.get("endpoints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderEndpoints"]]], result)

    @builtins.property
    def forbidden_account_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#forbidden_account_ids AwsProvider#forbidden_account_ids}.'''
        result = self._values.get("forbidden_account_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def http_proxy(self) -> typing.Optional[builtins.str]:
        '''URL of a proxy to use for HTTP requests when accessing the AWS API.

        Can also be set using the ``HTTP_PROXY`` or ``http_proxy`` environment variables.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#http_proxy AwsProvider#http_proxy}
        '''
        result = self._values.get("http_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_proxy(self) -> typing.Optional[builtins.str]:
        '''URL of a proxy to use for HTTPS requests when accessing the AWS API.

        Can also be set using the ``HTTPS_PROXY`` or ``https_proxy`` environment variables.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#https_proxy AwsProvider#https_proxy}
        '''
        result = self._values.get("https_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderIgnoreTags"]]]:
        '''ignore_tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ignore_tags AwsProvider#ignore_tags}
        '''
        result = self._values.get("ignore_tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AwsProviderIgnoreTags"]]], result)

    @builtins.property
    def insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Explicitly allow the provider to perform "insecure" SSL requests. If omitted, default value is ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#insecure AwsProvider#insecure}
        '''
        result = self._values.get("insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of times an AWS API request is being executed.

        If the API request still fails, an error is
        thrown.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#max_retries AwsProvider#max_retries}
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def no_proxy(self) -> typing.Optional[builtins.str]:
        '''Comma-separated list of hosts that should not use HTTP or HTTPS proxies.

        Can also be set using the ``NO_PROXY`` or ``no_proxy`` environment variables.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#no_proxy AwsProvider#no_proxy}
        '''
        result = self._values.get("no_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''The profile for API operations. If not set, the default profile created with ``aws configure`` will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#profile AwsProvider#profile}
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region where AWS operations will take place. Examples are us-east-1, us-west-2, etc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#region AwsProvider#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retry_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies how retries are attempted.

        Valid values are ``standard`` and ``adaptive``. Can also be configured using the ``AWS_RETRY_MODE`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#retry_mode AwsProvider#retry_mode}
        '''
        result = self._values.get("retry_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_us_east1_regional_endpoint(self) -> typing.Optional[builtins.str]:
        '''Specifies whether S3 API calls in the ``us-east-1`` region use the legacy global endpoint or a regional endpoint.

        Valid values are ``legacy`` or ``regional``. Can also be configured using the ``AWS_S3_US_EAST_1_REGIONAL_ENDPOINT`` environment variable or the ``s3_us_east_1_regional_endpoint`` shared config file parameter

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#s3_us_east_1_regional_endpoint AwsProvider#s3_us_east_1_regional_endpoint}
        '''
        result = self._values.get("s3_us_east1_regional_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_use_path_style(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set this to true to enable the request to use path-style addressing, i.e., https://s3.amazonaws.com/BUCKET/KEY. By default, the S3 client will use virtual hosted bucket addressing when possible (https://BUCKET.s3.amazonaws.com/KEY). Specific to the Amazon S3 service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#s3_use_path_style AwsProvider#s3_use_path_style}
        '''
        result = self._values.get("s3_use_path_style")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''The secret key for API operations. You can retrieve this from the 'Security & Credentials' section of the AWS console.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#secret_key AwsProvider#secret_key}
        '''
        result = self._values.get("secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shared_config_files(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of paths to shared config files. If not set, defaults to [~/.aws/config].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#shared_config_files AwsProvider#shared_config_files}
        '''
        result = self._values.get("shared_config_files")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def shared_credentials_files(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of paths to shared credentials files. If not set, defaults to [~/.aws/credentials].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#shared_credentials_files AwsProvider#shared_credentials_files}
        '''
        result = self._values.get("shared_credentials_files")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def skip_credentials_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Skip the credentials validation via STS API. Used for AWS API implementations that do not have STS available/implemented.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#skip_credentials_validation AwsProvider#skip_credentials_validation}
        '''
        result = self._values.get("skip_credentials_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def skip_metadata_api_check(self) -> typing.Optional[builtins.str]:
        '''Skip the AWS Metadata API check. Used for AWS API implementations that do not have a metadata api endpoint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#skip_metadata_api_check AwsProvider#skip_metadata_api_check}
        '''
        result = self._values.get("skip_metadata_api_check")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_region_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Skip static validation of region name.

        Used by users of alternative AWS-like APIs or users w/ access to regions that are not public (yet).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#skip_region_validation AwsProvider#skip_region_validation}
        '''
        result = self._values.get("skip_region_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def skip_requesting_account_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Skip requesting the account ID. Used for AWS API implementations that do not have IAM/STS API and/or metadata API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#skip_requesting_account_id AwsProvider#skip_requesting_account_id}
        '''
        result = self._values.get("skip_requesting_account_id")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sts_region(self) -> typing.Optional[builtins.str]:
        '''The region where AWS STS operations will take place. Examples are us-east-1 and us-west-2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#sts_region AwsProvider#sts_region}
        '''
        result = self._values.get("sts_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''session token. A session token is only required if you are using temporary security credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#token AwsProvider#token}
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_bucket_rate_limiter_capacity(self) -> typing.Optional[jsii.Number]:
        '''The capacity of the AWS SDK's token bucket rate limiter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#token_bucket_rate_limiter_capacity AwsProvider#token_bucket_rate_limiter_capacity}
        '''
        result = self._values.get("token_bucket_rate_limiter_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def use_dualstack_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Resolve an endpoint with DualStack capability.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#use_dualstack_endpoint AwsProvider#use_dualstack_endpoint}
        '''
        result = self._values.get("use_dualstack_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_fips_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Resolve an endpoint with FIPS capability.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#use_fips_endpoint AwsProvider#use_fips_endpoint}
        '''
        result = self._values.get("use_fips_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.provider.AwsProviderDefaultTags",
    jsii_struct_bases=[],
    name_mapping={"tags": "tags"},
)
class AwsProviderDefaultTags:
    def __init__(
        self,
        *,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param tags: Resource tags to default across all resources. Can also be configured with environment variables like ``TF_AWS_DEFAULT_TAGS_<tag_name>``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#tags AwsProvider#tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eebaf0067d800334bb2e8f03568b545daa7ceaffca147b8eed6da77e27758b8d)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Resource tags to default across all resources. Can also be configured with environment variables like ``TF_AWS_DEFAULT_TAGS_<tag_name>``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#tags AwsProvider#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsProviderDefaultTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.provider.AwsProviderEndpoints",
    jsii_struct_bases=[],
    name_mapping={
        "accessanalyzer": "accessanalyzer",
        "account": "account",
        "acm": "acm",
        "acmpca": "acmpca",
        "amg": "amg",
        "amp": "amp",
        "amplify": "amplify",
        "apigateway": "apigateway",
        "apigatewayv2": "apigatewayv2",
        "appautoscaling": "appautoscaling",
        "appconfig": "appconfig",
        "appfabric": "appfabric",
        "appflow": "appflow",
        "appintegrations": "appintegrations",
        "appintegrationsservice": "appintegrationsservice",
        "applicationautoscaling": "applicationautoscaling",
        "applicationinsights": "applicationinsights",
        "applicationsignals": "applicationsignals",
        "appmesh": "appmesh",
        "appregistry": "appregistry",
        "apprunner": "apprunner",
        "appstream": "appstream",
        "appsync": "appsync",
        "athena": "athena",
        "auditmanager": "auditmanager",
        "autoscaling": "autoscaling",
        "autoscalingplans": "autoscalingplans",
        "backup": "backup",
        "batch": "batch",
        "bcmdataexports": "bcmdataexports",
        "beanstalk": "beanstalk",
        "bedrock": "bedrock",
        "bedrockagent": "bedrockagent",
        "billing": "billing",
        "budgets": "budgets",
        "ce": "ce",
        "chatbot": "chatbot",
        "chime": "chime",
        "chimesdkmediapipelines": "chimesdkmediapipelines",
        "chimesdkvoice": "chimesdkvoice",
        "cleanrooms": "cleanrooms",
        "cloud9": "cloud9",
        "cloudcontrol": "cloudcontrol",
        "cloudcontrolapi": "cloudcontrolapi",
        "cloudformation": "cloudformation",
        "cloudfront": "cloudfront",
        "cloudfrontkeyvaluestore": "cloudfrontkeyvaluestore",
        "cloudhsm": "cloudhsm",
        "cloudhsmv2": "cloudhsmv2",
        "cloudsearch": "cloudsearch",
        "cloudtrail": "cloudtrail",
        "cloudwatch": "cloudwatch",
        "cloudwatchevents": "cloudwatchevents",
        "cloudwatchevidently": "cloudwatchevidently",
        "cloudwatchlog": "cloudwatchlog",
        "cloudwatchlogs": "cloudwatchlogs",
        "cloudwatchobservabilityaccessmanager": "cloudwatchobservabilityaccessmanager",
        "cloudwatchrum": "cloudwatchrum",
        "codeartifact": "codeartifact",
        "codebuild": "codebuild",
        "codecatalyst": "codecatalyst",
        "codecommit": "codecommit",
        "codeconnections": "codeconnections",
        "codedeploy": "codedeploy",
        "codeguruprofiler": "codeguruprofiler",
        "codegurureviewer": "codegurureviewer",
        "codepipeline": "codepipeline",
        "codestarconnections": "codestarconnections",
        "codestarnotifications": "codestarnotifications",
        "cognitoidentity": "cognitoidentity",
        "cognitoidentityprovider": "cognitoidentityprovider",
        "cognitoidp": "cognitoidp",
        "comprehend": "comprehend",
        "computeoptimizer": "computeoptimizer",
        "config": "config",
        "configservice": "configservice",
        "connect": "connect",
        "connectcases": "connectcases",
        "controltower": "controltower",
        "costandusagereportservice": "costandusagereportservice",
        "costexplorer": "costexplorer",
        "costoptimizationhub": "costoptimizationhub",
        "cur": "cur",
        "customerprofiles": "customerprofiles",
        "databasemigration": "databasemigration",
        "databasemigrationservice": "databasemigrationservice",
        "databrew": "databrew",
        "dataexchange": "dataexchange",
        "datapipeline": "datapipeline",
        "datasync": "datasync",
        "datazone": "datazone",
        "dax": "dax",
        "deploy": "deploy",
        "detective": "detective",
        "devicefarm": "devicefarm",
        "devopsguru": "devopsguru",
        "directconnect": "directconnect",
        "directoryservice": "directoryservice",
        "dlm": "dlm",
        "dms": "dms",
        "docdb": "docdb",
        "docdbelastic": "docdbelastic",
        "drs": "drs",
        "ds": "ds",
        "dsql": "dsql",
        "dynamodb": "dynamodb",
        "ec2": "ec2",
        "ecr": "ecr",
        "ecrpublic": "ecrpublic",
        "ecs": "ecs",
        "efs": "efs",
        "eks": "eks",
        "elasticache": "elasticache",
        "elasticbeanstalk": "elasticbeanstalk",
        "elasticloadbalancing": "elasticloadbalancing",
        "elasticloadbalancingv2": "elasticloadbalancingv2",
        "elasticsearch": "elasticsearch",
        "elasticsearchservice": "elasticsearchservice",
        "elastictranscoder": "elastictranscoder",
        "elb": "elb",
        "elbv2": "elbv2",
        "emr": "emr",
        "emrcontainers": "emrcontainers",
        "emrserverless": "emrserverless",
        "es": "es",
        "eventbridge": "eventbridge",
        "events": "events",
        "evidently": "evidently",
        "finspace": "finspace",
        "firehose": "firehose",
        "fis": "fis",
        "fms": "fms",
        "fsx": "fsx",
        "gamelift": "gamelift",
        "glacier": "glacier",
        "globalaccelerator": "globalaccelerator",
        "glue": "glue",
        "gluedatabrew": "gluedatabrew",
        "grafana": "grafana",
        "greengrass": "greengrass",
        "groundstation": "groundstation",
        "guardduty": "guardduty",
        "healthlake": "healthlake",
        "iam": "iam",
        "identitystore": "identitystore",
        "imagebuilder": "imagebuilder",
        "inspector": "inspector",
        "inspector2": "inspector2",
        "inspectorv2": "inspectorv2",
        "internetmonitor": "internetmonitor",
        "invoicing": "invoicing",
        "iot": "iot",
        "iotanalytics": "iotanalytics",
        "iotevents": "iotevents",
        "ivs": "ivs",
        "ivschat": "ivschat",
        "kafka": "kafka",
        "kafkaconnect": "kafkaconnect",
        "kendra": "kendra",
        "keyspaces": "keyspaces",
        "kinesis": "kinesis",
        "kinesisanalytics": "kinesisanalytics",
        "kinesisanalyticsv2": "kinesisanalyticsv2",
        "kinesisvideo": "kinesisvideo",
        "kms": "kms",
        "lakeformation": "lakeformation",
        "lambda_": "lambda",
        "launchwizard": "launchwizard",
        "lex": "lex",
        "lexmodelbuilding": "lexmodelbuilding",
        "lexmodelbuildingservice": "lexmodelbuildingservice",
        "lexmodels": "lexmodels",
        "lexmodelsv2": "lexmodelsv2",
        "lexv2_models": "lexv2Models",
        "licensemanager": "licensemanager",
        "lightsail": "lightsail",
        "location": "location",
        "locationservice": "locationservice",
        "logs": "logs",
        "lookoutmetrics": "lookoutmetrics",
        "m2": "m2",
        "macie2": "macie2",
        "managedgrafana": "managedgrafana",
        "mediaconnect": "mediaconnect",
        "mediaconvert": "mediaconvert",
        "medialive": "medialive",
        "mediapackage": "mediapackage",
        "mediapackagev2": "mediapackagev2",
        "mediapackagevod": "mediapackagevod",
        "mediastore": "mediastore",
        "memorydb": "memorydb",
        "mgn": "mgn",
        "mq": "mq",
        "msk": "msk",
        "mwaa": "mwaa",
        "neptune": "neptune",
        "neptunegraph": "neptunegraph",
        "networkfirewall": "networkfirewall",
        "networkmanager": "networkmanager",
        "networkmonitor": "networkmonitor",
        "oam": "oam",
        "opensearch": "opensearch",
        "opensearchingestion": "opensearchingestion",
        "opensearchserverless": "opensearchserverless",
        "opensearchservice": "opensearchservice",
        "opsworks": "opsworks",
        "organizations": "organizations",
        "osis": "osis",
        "outposts": "outposts",
        "paymentcryptography": "paymentcryptography",
        "pcaconnectorad": "pcaconnectorad",
        "pcs": "pcs",
        "pinpoint": "pinpoint",
        "pinpointsmsvoicev2": "pinpointsmsvoicev2",
        "pipes": "pipes",
        "polly": "polly",
        "pricing": "pricing",
        "prometheus": "prometheus",
        "prometheusservice": "prometheusservice",
        "qbusiness": "qbusiness",
        "qldb": "qldb",
        "quicksight": "quicksight",
        "ram": "ram",
        "rbin": "rbin",
        "rds": "rds",
        "recyclebin": "recyclebin",
        "redshift": "redshift",
        "redshiftdata": "redshiftdata",
        "redshiftdataapiservice": "redshiftdataapiservice",
        "redshiftserverless": "redshiftserverless",
        "rekognition": "rekognition",
        "resiliencehub": "resiliencehub",
        "resourceexplorer2": "resourceexplorer2",
        "resourcegroups": "resourcegroups",
        "resourcegroupstagging": "resourcegroupstagging",
        "resourcegroupstaggingapi": "resourcegroupstaggingapi",
        "rolesanywhere": "rolesanywhere",
        "route53": "route53",
        "route53_domains": "route53Domains",
        "route53_profiles": "route53Profiles",
        "route53_recoverycontrolconfig": "route53Recoverycontrolconfig",
        "route53_recoveryreadiness": "route53Recoveryreadiness",
        "route53_resolver": "route53Resolver",
        "rum": "rum",
        "s3": "s3",
        "s3_api": "s3Api",
        "s3_control": "s3Control",
        "s3_outposts": "s3Outposts",
        "s3_tables": "s3Tables",
        "sagemaker": "sagemaker",
        "scheduler": "scheduler",
        "schemas": "schemas",
        "sdb": "sdb",
        "secretsmanager": "secretsmanager",
        "securityhub": "securityhub",
        "securitylake": "securitylake",
        "serverlessapplicationrepository": "serverlessapplicationrepository",
        "serverlessapprepo": "serverlessapprepo",
        "serverlessrepo": "serverlessrepo",
        "servicecatalog": "servicecatalog",
        "servicecatalogappregistry": "servicecatalogappregistry",
        "servicediscovery": "servicediscovery",
        "servicequotas": "servicequotas",
        "ses": "ses",
        "sesv2": "sesv2",
        "sfn": "sfn",
        "shield": "shield",
        "signer": "signer",
        "simpledb": "simpledb",
        "sns": "sns",
        "sqs": "sqs",
        "ssm": "ssm",
        "ssmcontacts": "ssmcontacts",
        "ssmincidents": "ssmincidents",
        "ssmquicksetup": "ssmquicksetup",
        "ssmsap": "ssmsap",
        "sso": "sso",
        "ssoadmin": "ssoadmin",
        "stepfunctions": "stepfunctions",
        "storagegateway": "storagegateway",
        "sts": "sts",
        "swf": "swf",
        "synthetics": "synthetics",
        "taxsettings": "taxsettings",
        "timestreaminfluxdb": "timestreaminfluxdb",
        "timestreamquery": "timestreamquery",
        "timestreamwrite": "timestreamwrite",
        "transcribe": "transcribe",
        "transcribeservice": "transcribeservice",
        "transfer": "transfer",
        "verifiedpermissions": "verifiedpermissions",
        "vpclattice": "vpclattice",
        "waf": "waf",
        "wafregional": "wafregional",
        "wafv2": "wafv2",
        "wellarchitected": "wellarchitected",
        "worklink": "worklink",
        "workspaces": "workspaces",
        "workspacesweb": "workspacesweb",
        "xray": "xray",
    },
)
class AwsProviderEndpoints:
    def __init__(
        self,
        *,
        accessanalyzer: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        acm: typing.Optional[builtins.str] = None,
        acmpca: typing.Optional[builtins.str] = None,
        amg: typing.Optional[builtins.str] = None,
        amp: typing.Optional[builtins.str] = None,
        amplify: typing.Optional[builtins.str] = None,
        apigateway: typing.Optional[builtins.str] = None,
        apigatewayv2: typing.Optional[builtins.str] = None,
        appautoscaling: typing.Optional[builtins.str] = None,
        appconfig: typing.Optional[builtins.str] = None,
        appfabric: typing.Optional[builtins.str] = None,
        appflow: typing.Optional[builtins.str] = None,
        appintegrations: typing.Optional[builtins.str] = None,
        appintegrationsservice: typing.Optional[builtins.str] = None,
        applicationautoscaling: typing.Optional[builtins.str] = None,
        applicationinsights: typing.Optional[builtins.str] = None,
        applicationsignals: typing.Optional[builtins.str] = None,
        appmesh: typing.Optional[builtins.str] = None,
        appregistry: typing.Optional[builtins.str] = None,
        apprunner: typing.Optional[builtins.str] = None,
        appstream: typing.Optional[builtins.str] = None,
        appsync: typing.Optional[builtins.str] = None,
        athena: typing.Optional[builtins.str] = None,
        auditmanager: typing.Optional[builtins.str] = None,
        autoscaling: typing.Optional[builtins.str] = None,
        autoscalingplans: typing.Optional[builtins.str] = None,
        backup: typing.Optional[builtins.str] = None,
        batch: typing.Optional[builtins.str] = None,
        bcmdataexports: typing.Optional[builtins.str] = None,
        beanstalk: typing.Optional[builtins.str] = None,
        bedrock: typing.Optional[builtins.str] = None,
        bedrockagent: typing.Optional[builtins.str] = None,
        billing: typing.Optional[builtins.str] = None,
        budgets: typing.Optional[builtins.str] = None,
        ce: typing.Optional[builtins.str] = None,
        chatbot: typing.Optional[builtins.str] = None,
        chime: typing.Optional[builtins.str] = None,
        chimesdkmediapipelines: typing.Optional[builtins.str] = None,
        chimesdkvoice: typing.Optional[builtins.str] = None,
        cleanrooms: typing.Optional[builtins.str] = None,
        cloud9: typing.Optional[builtins.str] = None,
        cloudcontrol: typing.Optional[builtins.str] = None,
        cloudcontrolapi: typing.Optional[builtins.str] = None,
        cloudformation: typing.Optional[builtins.str] = None,
        cloudfront: typing.Optional[builtins.str] = None,
        cloudfrontkeyvaluestore: typing.Optional[builtins.str] = None,
        cloudhsm: typing.Optional[builtins.str] = None,
        cloudhsmv2: typing.Optional[builtins.str] = None,
        cloudsearch: typing.Optional[builtins.str] = None,
        cloudtrail: typing.Optional[builtins.str] = None,
        cloudwatch: typing.Optional[builtins.str] = None,
        cloudwatchevents: typing.Optional[builtins.str] = None,
        cloudwatchevidently: typing.Optional[builtins.str] = None,
        cloudwatchlog: typing.Optional[builtins.str] = None,
        cloudwatchlogs: typing.Optional[builtins.str] = None,
        cloudwatchobservabilityaccessmanager: typing.Optional[builtins.str] = None,
        cloudwatchrum: typing.Optional[builtins.str] = None,
        codeartifact: typing.Optional[builtins.str] = None,
        codebuild: typing.Optional[builtins.str] = None,
        codecatalyst: typing.Optional[builtins.str] = None,
        codecommit: typing.Optional[builtins.str] = None,
        codeconnections: typing.Optional[builtins.str] = None,
        codedeploy: typing.Optional[builtins.str] = None,
        codeguruprofiler: typing.Optional[builtins.str] = None,
        codegurureviewer: typing.Optional[builtins.str] = None,
        codepipeline: typing.Optional[builtins.str] = None,
        codestarconnections: typing.Optional[builtins.str] = None,
        codestarnotifications: typing.Optional[builtins.str] = None,
        cognitoidentity: typing.Optional[builtins.str] = None,
        cognitoidentityprovider: typing.Optional[builtins.str] = None,
        cognitoidp: typing.Optional[builtins.str] = None,
        comprehend: typing.Optional[builtins.str] = None,
        computeoptimizer: typing.Optional[builtins.str] = None,
        config: typing.Optional[builtins.str] = None,
        configservice: typing.Optional[builtins.str] = None,
        connect: typing.Optional[builtins.str] = None,
        connectcases: typing.Optional[builtins.str] = None,
        controltower: typing.Optional[builtins.str] = None,
        costandusagereportservice: typing.Optional[builtins.str] = None,
        costexplorer: typing.Optional[builtins.str] = None,
        costoptimizationhub: typing.Optional[builtins.str] = None,
        cur: typing.Optional[builtins.str] = None,
        customerprofiles: typing.Optional[builtins.str] = None,
        databasemigration: typing.Optional[builtins.str] = None,
        databasemigrationservice: typing.Optional[builtins.str] = None,
        databrew: typing.Optional[builtins.str] = None,
        dataexchange: typing.Optional[builtins.str] = None,
        datapipeline: typing.Optional[builtins.str] = None,
        datasync: typing.Optional[builtins.str] = None,
        datazone: typing.Optional[builtins.str] = None,
        dax: typing.Optional[builtins.str] = None,
        deploy: typing.Optional[builtins.str] = None,
        detective: typing.Optional[builtins.str] = None,
        devicefarm: typing.Optional[builtins.str] = None,
        devopsguru: typing.Optional[builtins.str] = None,
        directconnect: typing.Optional[builtins.str] = None,
        directoryservice: typing.Optional[builtins.str] = None,
        dlm: typing.Optional[builtins.str] = None,
        dms: typing.Optional[builtins.str] = None,
        docdb: typing.Optional[builtins.str] = None,
        docdbelastic: typing.Optional[builtins.str] = None,
        drs: typing.Optional[builtins.str] = None,
        ds: typing.Optional[builtins.str] = None,
        dsql: typing.Optional[builtins.str] = None,
        dynamodb: typing.Optional[builtins.str] = None,
        ec2: typing.Optional[builtins.str] = None,
        ecr: typing.Optional[builtins.str] = None,
        ecrpublic: typing.Optional[builtins.str] = None,
        ecs: typing.Optional[builtins.str] = None,
        efs: typing.Optional[builtins.str] = None,
        eks: typing.Optional[builtins.str] = None,
        elasticache: typing.Optional[builtins.str] = None,
        elasticbeanstalk: typing.Optional[builtins.str] = None,
        elasticloadbalancing: typing.Optional[builtins.str] = None,
        elasticloadbalancingv2: typing.Optional[builtins.str] = None,
        elasticsearch: typing.Optional[builtins.str] = None,
        elasticsearchservice: typing.Optional[builtins.str] = None,
        elastictranscoder: typing.Optional[builtins.str] = None,
        elb: typing.Optional[builtins.str] = None,
        elbv2: typing.Optional[builtins.str] = None,
        emr: typing.Optional[builtins.str] = None,
        emrcontainers: typing.Optional[builtins.str] = None,
        emrserverless: typing.Optional[builtins.str] = None,
        es: typing.Optional[builtins.str] = None,
        eventbridge: typing.Optional[builtins.str] = None,
        events: typing.Optional[builtins.str] = None,
        evidently: typing.Optional[builtins.str] = None,
        finspace: typing.Optional[builtins.str] = None,
        firehose: typing.Optional[builtins.str] = None,
        fis: typing.Optional[builtins.str] = None,
        fms: typing.Optional[builtins.str] = None,
        fsx: typing.Optional[builtins.str] = None,
        gamelift: typing.Optional[builtins.str] = None,
        glacier: typing.Optional[builtins.str] = None,
        globalaccelerator: typing.Optional[builtins.str] = None,
        glue: typing.Optional[builtins.str] = None,
        gluedatabrew: typing.Optional[builtins.str] = None,
        grafana: typing.Optional[builtins.str] = None,
        greengrass: typing.Optional[builtins.str] = None,
        groundstation: typing.Optional[builtins.str] = None,
        guardduty: typing.Optional[builtins.str] = None,
        healthlake: typing.Optional[builtins.str] = None,
        iam: typing.Optional[builtins.str] = None,
        identitystore: typing.Optional[builtins.str] = None,
        imagebuilder: typing.Optional[builtins.str] = None,
        inspector: typing.Optional[builtins.str] = None,
        inspector2: typing.Optional[builtins.str] = None,
        inspectorv2: typing.Optional[builtins.str] = None,
        internetmonitor: typing.Optional[builtins.str] = None,
        invoicing: typing.Optional[builtins.str] = None,
        iot: typing.Optional[builtins.str] = None,
        iotanalytics: typing.Optional[builtins.str] = None,
        iotevents: typing.Optional[builtins.str] = None,
        ivs: typing.Optional[builtins.str] = None,
        ivschat: typing.Optional[builtins.str] = None,
        kafka: typing.Optional[builtins.str] = None,
        kafkaconnect: typing.Optional[builtins.str] = None,
        kendra: typing.Optional[builtins.str] = None,
        keyspaces: typing.Optional[builtins.str] = None,
        kinesis: typing.Optional[builtins.str] = None,
        kinesisanalytics: typing.Optional[builtins.str] = None,
        kinesisanalyticsv2: typing.Optional[builtins.str] = None,
        kinesisvideo: typing.Optional[builtins.str] = None,
        kms: typing.Optional[builtins.str] = None,
        lakeformation: typing.Optional[builtins.str] = None,
        lambda_: typing.Optional[builtins.str] = None,
        launchwizard: typing.Optional[builtins.str] = None,
        lex: typing.Optional[builtins.str] = None,
        lexmodelbuilding: typing.Optional[builtins.str] = None,
        lexmodelbuildingservice: typing.Optional[builtins.str] = None,
        lexmodels: typing.Optional[builtins.str] = None,
        lexmodelsv2: typing.Optional[builtins.str] = None,
        lexv2_models: typing.Optional[builtins.str] = None,
        licensemanager: typing.Optional[builtins.str] = None,
        lightsail: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        locationservice: typing.Optional[builtins.str] = None,
        logs: typing.Optional[builtins.str] = None,
        lookoutmetrics: typing.Optional[builtins.str] = None,
        m2: typing.Optional[builtins.str] = None,
        macie2: typing.Optional[builtins.str] = None,
        managedgrafana: typing.Optional[builtins.str] = None,
        mediaconnect: typing.Optional[builtins.str] = None,
        mediaconvert: typing.Optional[builtins.str] = None,
        medialive: typing.Optional[builtins.str] = None,
        mediapackage: typing.Optional[builtins.str] = None,
        mediapackagev2: typing.Optional[builtins.str] = None,
        mediapackagevod: typing.Optional[builtins.str] = None,
        mediastore: typing.Optional[builtins.str] = None,
        memorydb: typing.Optional[builtins.str] = None,
        mgn: typing.Optional[builtins.str] = None,
        mq: typing.Optional[builtins.str] = None,
        msk: typing.Optional[builtins.str] = None,
        mwaa: typing.Optional[builtins.str] = None,
        neptune: typing.Optional[builtins.str] = None,
        neptunegraph: typing.Optional[builtins.str] = None,
        networkfirewall: typing.Optional[builtins.str] = None,
        networkmanager: typing.Optional[builtins.str] = None,
        networkmonitor: typing.Optional[builtins.str] = None,
        oam: typing.Optional[builtins.str] = None,
        opensearch: typing.Optional[builtins.str] = None,
        opensearchingestion: typing.Optional[builtins.str] = None,
        opensearchserverless: typing.Optional[builtins.str] = None,
        opensearchservice: typing.Optional[builtins.str] = None,
        opsworks: typing.Optional[builtins.str] = None,
        organizations: typing.Optional[builtins.str] = None,
        osis: typing.Optional[builtins.str] = None,
        outposts: typing.Optional[builtins.str] = None,
        paymentcryptography: typing.Optional[builtins.str] = None,
        pcaconnectorad: typing.Optional[builtins.str] = None,
        pcs: typing.Optional[builtins.str] = None,
        pinpoint: typing.Optional[builtins.str] = None,
        pinpointsmsvoicev2: typing.Optional[builtins.str] = None,
        pipes: typing.Optional[builtins.str] = None,
        polly: typing.Optional[builtins.str] = None,
        pricing: typing.Optional[builtins.str] = None,
        prometheus: typing.Optional[builtins.str] = None,
        prometheusservice: typing.Optional[builtins.str] = None,
        qbusiness: typing.Optional[builtins.str] = None,
        qldb: typing.Optional[builtins.str] = None,
        quicksight: typing.Optional[builtins.str] = None,
        ram: typing.Optional[builtins.str] = None,
        rbin: typing.Optional[builtins.str] = None,
        rds: typing.Optional[builtins.str] = None,
        recyclebin: typing.Optional[builtins.str] = None,
        redshift: typing.Optional[builtins.str] = None,
        redshiftdata: typing.Optional[builtins.str] = None,
        redshiftdataapiservice: typing.Optional[builtins.str] = None,
        redshiftserverless: typing.Optional[builtins.str] = None,
        rekognition: typing.Optional[builtins.str] = None,
        resiliencehub: typing.Optional[builtins.str] = None,
        resourceexplorer2: typing.Optional[builtins.str] = None,
        resourcegroups: typing.Optional[builtins.str] = None,
        resourcegroupstagging: typing.Optional[builtins.str] = None,
        resourcegroupstaggingapi: typing.Optional[builtins.str] = None,
        rolesanywhere: typing.Optional[builtins.str] = None,
        route53: typing.Optional[builtins.str] = None,
        route53_domains: typing.Optional[builtins.str] = None,
        route53_profiles: typing.Optional[builtins.str] = None,
        route53_recoverycontrolconfig: typing.Optional[builtins.str] = None,
        route53_recoveryreadiness: typing.Optional[builtins.str] = None,
        route53_resolver: typing.Optional[builtins.str] = None,
        rum: typing.Optional[builtins.str] = None,
        s3: typing.Optional[builtins.str] = None,
        s3_api: typing.Optional[builtins.str] = None,
        s3_control: typing.Optional[builtins.str] = None,
        s3_outposts: typing.Optional[builtins.str] = None,
        s3_tables: typing.Optional[builtins.str] = None,
        sagemaker: typing.Optional[builtins.str] = None,
        scheduler: typing.Optional[builtins.str] = None,
        schemas: typing.Optional[builtins.str] = None,
        sdb: typing.Optional[builtins.str] = None,
        secretsmanager: typing.Optional[builtins.str] = None,
        securityhub: typing.Optional[builtins.str] = None,
        securitylake: typing.Optional[builtins.str] = None,
        serverlessapplicationrepository: typing.Optional[builtins.str] = None,
        serverlessapprepo: typing.Optional[builtins.str] = None,
        serverlessrepo: typing.Optional[builtins.str] = None,
        servicecatalog: typing.Optional[builtins.str] = None,
        servicecatalogappregistry: typing.Optional[builtins.str] = None,
        servicediscovery: typing.Optional[builtins.str] = None,
        servicequotas: typing.Optional[builtins.str] = None,
        ses: typing.Optional[builtins.str] = None,
        sesv2: typing.Optional[builtins.str] = None,
        sfn: typing.Optional[builtins.str] = None,
        shield: typing.Optional[builtins.str] = None,
        signer: typing.Optional[builtins.str] = None,
        simpledb: typing.Optional[builtins.str] = None,
        sns: typing.Optional[builtins.str] = None,
        sqs: typing.Optional[builtins.str] = None,
        ssm: typing.Optional[builtins.str] = None,
        ssmcontacts: typing.Optional[builtins.str] = None,
        ssmincidents: typing.Optional[builtins.str] = None,
        ssmquicksetup: typing.Optional[builtins.str] = None,
        ssmsap: typing.Optional[builtins.str] = None,
        sso: typing.Optional[builtins.str] = None,
        ssoadmin: typing.Optional[builtins.str] = None,
        stepfunctions: typing.Optional[builtins.str] = None,
        storagegateway: typing.Optional[builtins.str] = None,
        sts: typing.Optional[builtins.str] = None,
        swf: typing.Optional[builtins.str] = None,
        synthetics: typing.Optional[builtins.str] = None,
        taxsettings: typing.Optional[builtins.str] = None,
        timestreaminfluxdb: typing.Optional[builtins.str] = None,
        timestreamquery: typing.Optional[builtins.str] = None,
        timestreamwrite: typing.Optional[builtins.str] = None,
        transcribe: typing.Optional[builtins.str] = None,
        transcribeservice: typing.Optional[builtins.str] = None,
        transfer: typing.Optional[builtins.str] = None,
        verifiedpermissions: typing.Optional[builtins.str] = None,
        vpclattice: typing.Optional[builtins.str] = None,
        waf: typing.Optional[builtins.str] = None,
        wafregional: typing.Optional[builtins.str] = None,
        wafv2: typing.Optional[builtins.str] = None,
        wellarchitected: typing.Optional[builtins.str] = None,
        worklink: typing.Optional[builtins.str] = None,
        workspaces: typing.Optional[builtins.str] = None,
        workspacesweb: typing.Optional[builtins.str] = None,
        xray: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accessanalyzer: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#accessanalyzer AwsProvider#accessanalyzer}
        :param account: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#account AwsProvider#account}
        :param acm: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#acm AwsProvider#acm}
        :param acmpca: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#acmpca AwsProvider#acmpca}
        :param amg: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#amg AwsProvider#amg}
        :param amp: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#amp AwsProvider#amp}
        :param amplify: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#amplify AwsProvider#amplify}
        :param apigateway: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#apigateway AwsProvider#apigateway}
        :param apigatewayv2: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#apigatewayv2 AwsProvider#apigatewayv2}
        :param appautoscaling: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#appautoscaling AwsProvider#appautoscaling}
        :param appconfig: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#appconfig AwsProvider#appconfig}
        :param appfabric: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#appfabric AwsProvider#appfabric}
        :param appflow: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#appflow AwsProvider#appflow}
        :param appintegrations: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#appintegrations AwsProvider#appintegrations}
        :param appintegrationsservice: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#appintegrationsservice AwsProvider#appintegrationsservice}
        :param applicationautoscaling: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#applicationautoscaling AwsProvider#applicationautoscaling}
        :param applicationinsights: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#applicationinsights AwsProvider#applicationinsights}
        :param applicationsignals: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#applicationsignals AwsProvider#applicationsignals}
        :param appmesh: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#appmesh AwsProvider#appmesh}
        :param appregistry: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#appregistry AwsProvider#appregistry}
        :param apprunner: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#apprunner AwsProvider#apprunner}
        :param appstream: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#appstream AwsProvider#appstream}
        :param appsync: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#appsync AwsProvider#appsync}
        :param athena: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#athena AwsProvider#athena}
        :param auditmanager: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#auditmanager AwsProvider#auditmanager}
        :param autoscaling: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#autoscaling AwsProvider#autoscaling}
        :param autoscalingplans: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#autoscalingplans AwsProvider#autoscalingplans}
        :param backup: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#backup AwsProvider#backup}
        :param batch: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#batch AwsProvider#batch}
        :param bcmdataexports: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#bcmdataexports AwsProvider#bcmdataexports}
        :param beanstalk: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#beanstalk AwsProvider#beanstalk}
        :param bedrock: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#bedrock AwsProvider#bedrock}
        :param bedrockagent: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#bedrockagent AwsProvider#bedrockagent}
        :param billing: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#billing AwsProvider#billing}
        :param budgets: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#budgets AwsProvider#budgets}
        :param ce: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ce AwsProvider#ce}
        :param chatbot: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#chatbot AwsProvider#chatbot}
        :param chime: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#chime AwsProvider#chime}
        :param chimesdkmediapipelines: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#chimesdkmediapipelines AwsProvider#chimesdkmediapipelines}
        :param chimesdkvoice: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#chimesdkvoice AwsProvider#chimesdkvoice}
        :param cleanrooms: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cleanrooms AwsProvider#cleanrooms}
        :param cloud9: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloud9 AwsProvider#cloud9}
        :param cloudcontrol: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudcontrol AwsProvider#cloudcontrol}
        :param cloudcontrolapi: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudcontrolapi AwsProvider#cloudcontrolapi}
        :param cloudformation: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudformation AwsProvider#cloudformation}
        :param cloudfront: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudfront AwsProvider#cloudfront}
        :param cloudfrontkeyvaluestore: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudfrontkeyvaluestore AwsProvider#cloudfrontkeyvaluestore}
        :param cloudhsm: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudhsm AwsProvider#cloudhsm}
        :param cloudhsmv2: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudhsmv2 AwsProvider#cloudhsmv2}
        :param cloudsearch: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudsearch AwsProvider#cloudsearch}
        :param cloudtrail: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudtrail AwsProvider#cloudtrail}
        :param cloudwatch: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudwatch AwsProvider#cloudwatch}
        :param cloudwatchevents: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudwatchevents AwsProvider#cloudwatchevents}
        :param cloudwatchevidently: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudwatchevidently AwsProvider#cloudwatchevidently}
        :param cloudwatchlog: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudwatchlog AwsProvider#cloudwatchlog}
        :param cloudwatchlogs: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudwatchlogs AwsProvider#cloudwatchlogs}
        :param cloudwatchobservabilityaccessmanager: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudwatchobservabilityaccessmanager AwsProvider#cloudwatchobservabilityaccessmanager}
        :param cloudwatchrum: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudwatchrum AwsProvider#cloudwatchrum}
        :param codeartifact: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codeartifact AwsProvider#codeartifact}
        :param codebuild: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codebuild AwsProvider#codebuild}
        :param codecatalyst: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codecatalyst AwsProvider#codecatalyst}
        :param codecommit: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codecommit AwsProvider#codecommit}
        :param codeconnections: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codeconnections AwsProvider#codeconnections}
        :param codedeploy: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codedeploy AwsProvider#codedeploy}
        :param codeguruprofiler: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codeguruprofiler AwsProvider#codeguruprofiler}
        :param codegurureviewer: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codegurureviewer AwsProvider#codegurureviewer}
        :param codepipeline: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codepipeline AwsProvider#codepipeline}
        :param codestarconnections: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codestarconnections AwsProvider#codestarconnections}
        :param codestarnotifications: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codestarnotifications AwsProvider#codestarnotifications}
        :param cognitoidentity: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cognitoidentity AwsProvider#cognitoidentity}
        :param cognitoidentityprovider: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cognitoidentityprovider AwsProvider#cognitoidentityprovider}
        :param cognitoidp: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cognitoidp AwsProvider#cognitoidp}
        :param comprehend: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#comprehend AwsProvider#comprehend}
        :param computeoptimizer: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#computeoptimizer AwsProvider#computeoptimizer}
        :param config: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#config AwsProvider#config}
        :param configservice: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#configservice AwsProvider#configservice}
        :param connect: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#connect AwsProvider#connect}
        :param connectcases: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#connectcases AwsProvider#connectcases}
        :param controltower: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#controltower AwsProvider#controltower}
        :param costandusagereportservice: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#costandusagereportservice AwsProvider#costandusagereportservice}
        :param costexplorer: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#costexplorer AwsProvider#costexplorer}
        :param costoptimizationhub: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#costoptimizationhub AwsProvider#costoptimizationhub}
        :param cur: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cur AwsProvider#cur}
        :param customerprofiles: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#customerprofiles AwsProvider#customerprofiles}
        :param databasemigration: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#databasemigration AwsProvider#databasemigration}
        :param databasemigrationservice: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#databasemigrationservice AwsProvider#databasemigrationservice}
        :param databrew: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#databrew AwsProvider#databrew}
        :param dataexchange: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#dataexchange AwsProvider#dataexchange}
        :param datapipeline: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#datapipeline AwsProvider#datapipeline}
        :param datasync: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#datasync AwsProvider#datasync}
        :param datazone: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#datazone AwsProvider#datazone}
        :param dax: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#dax AwsProvider#dax}
        :param deploy: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#deploy AwsProvider#deploy}
        :param detective: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#detective AwsProvider#detective}
        :param devicefarm: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#devicefarm AwsProvider#devicefarm}
        :param devopsguru: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#devopsguru AwsProvider#devopsguru}
        :param directconnect: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#directconnect AwsProvider#directconnect}
        :param directoryservice: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#directoryservice AwsProvider#directoryservice}
        :param dlm: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#dlm AwsProvider#dlm}
        :param dms: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#dms AwsProvider#dms}
        :param docdb: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#docdb AwsProvider#docdb}
        :param docdbelastic: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#docdbelastic AwsProvider#docdbelastic}
        :param drs: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#drs AwsProvider#drs}
        :param ds: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ds AwsProvider#ds}
        :param dsql: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#dsql AwsProvider#dsql}
        :param dynamodb: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#dynamodb AwsProvider#dynamodb}
        :param ec2: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ec2 AwsProvider#ec2}
        :param ecr: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ecr AwsProvider#ecr}
        :param ecrpublic: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ecrpublic AwsProvider#ecrpublic}
        :param ecs: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ecs AwsProvider#ecs}
        :param efs: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#efs AwsProvider#efs}
        :param eks: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#eks AwsProvider#eks}
        :param elasticache: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#elasticache AwsProvider#elasticache}
        :param elasticbeanstalk: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#elasticbeanstalk AwsProvider#elasticbeanstalk}
        :param elasticloadbalancing: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#elasticloadbalancing AwsProvider#elasticloadbalancing}
        :param elasticloadbalancingv2: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#elasticloadbalancingv2 AwsProvider#elasticloadbalancingv2}
        :param elasticsearch: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#elasticsearch AwsProvider#elasticsearch}
        :param elasticsearchservice: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#elasticsearchservice AwsProvider#elasticsearchservice}
        :param elastictranscoder: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#elastictranscoder AwsProvider#elastictranscoder}
        :param elb: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#elb AwsProvider#elb}
        :param elbv2: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#elbv2 AwsProvider#elbv2}
        :param emr: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#emr AwsProvider#emr}
        :param emrcontainers: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#emrcontainers AwsProvider#emrcontainers}
        :param emrserverless: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#emrserverless AwsProvider#emrserverless}
        :param es: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#es AwsProvider#es}
        :param eventbridge: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#eventbridge AwsProvider#eventbridge}
        :param events: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#events AwsProvider#events}
        :param evidently: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#evidently AwsProvider#evidently}
        :param finspace: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#finspace AwsProvider#finspace}
        :param firehose: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#firehose AwsProvider#firehose}
        :param fis: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#fis AwsProvider#fis}
        :param fms: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#fms AwsProvider#fms}
        :param fsx: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#fsx AwsProvider#fsx}
        :param gamelift: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#gamelift AwsProvider#gamelift}
        :param glacier: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#glacier AwsProvider#glacier}
        :param globalaccelerator: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#globalaccelerator AwsProvider#globalaccelerator}
        :param glue: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#glue AwsProvider#glue}
        :param gluedatabrew: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#gluedatabrew AwsProvider#gluedatabrew}
        :param grafana: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#grafana AwsProvider#grafana}
        :param greengrass: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#greengrass AwsProvider#greengrass}
        :param groundstation: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#groundstation AwsProvider#groundstation}
        :param guardduty: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#guardduty AwsProvider#guardduty}
        :param healthlake: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#healthlake AwsProvider#healthlake}
        :param iam: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#iam AwsProvider#iam}
        :param identitystore: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#identitystore AwsProvider#identitystore}
        :param imagebuilder: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#imagebuilder AwsProvider#imagebuilder}
        :param inspector: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#inspector AwsProvider#inspector}
        :param inspector2: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#inspector2 AwsProvider#inspector2}
        :param inspectorv2: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#inspectorv2 AwsProvider#inspectorv2}
        :param internetmonitor: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#internetmonitor AwsProvider#internetmonitor}
        :param invoicing: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#invoicing AwsProvider#invoicing}
        :param iot: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#iot AwsProvider#iot}
        :param iotanalytics: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#iotanalytics AwsProvider#iotanalytics}
        :param iotevents: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#iotevents AwsProvider#iotevents}
        :param ivs: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ivs AwsProvider#ivs}
        :param ivschat: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ivschat AwsProvider#ivschat}
        :param kafka: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#kafka AwsProvider#kafka}
        :param kafkaconnect: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#kafkaconnect AwsProvider#kafkaconnect}
        :param kendra: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#kendra AwsProvider#kendra}
        :param keyspaces: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#keyspaces AwsProvider#keyspaces}
        :param kinesis: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#kinesis AwsProvider#kinesis}
        :param kinesisanalytics: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#kinesisanalytics AwsProvider#kinesisanalytics}
        :param kinesisanalyticsv2: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#kinesisanalyticsv2 AwsProvider#kinesisanalyticsv2}
        :param kinesisvideo: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#kinesisvideo AwsProvider#kinesisvideo}
        :param kms: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#kms AwsProvider#kms}
        :param lakeformation: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#lakeformation AwsProvider#lakeformation}
        :param lambda_: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#lambda AwsProvider#lambda}
        :param launchwizard: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#launchwizard AwsProvider#launchwizard}
        :param lex: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#lex AwsProvider#lex}
        :param lexmodelbuilding: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#lexmodelbuilding AwsProvider#lexmodelbuilding}
        :param lexmodelbuildingservice: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#lexmodelbuildingservice AwsProvider#lexmodelbuildingservice}
        :param lexmodels: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#lexmodels AwsProvider#lexmodels}
        :param lexmodelsv2: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#lexmodelsv2 AwsProvider#lexmodelsv2}
        :param lexv2_models: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#lexv2models AwsProvider#lexv2models}
        :param licensemanager: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#licensemanager AwsProvider#licensemanager}
        :param lightsail: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#lightsail AwsProvider#lightsail}
        :param location: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#location AwsProvider#location}
        :param locationservice: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#locationservice AwsProvider#locationservice}
        :param logs: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#logs AwsProvider#logs}
        :param lookoutmetrics: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#lookoutmetrics AwsProvider#lookoutmetrics}
        :param m2: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#m2 AwsProvider#m2}
        :param macie2: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#macie2 AwsProvider#macie2}
        :param managedgrafana: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#managedgrafana AwsProvider#managedgrafana}
        :param mediaconnect: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#mediaconnect AwsProvider#mediaconnect}
        :param mediaconvert: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#mediaconvert AwsProvider#mediaconvert}
        :param medialive: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#medialive AwsProvider#medialive}
        :param mediapackage: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#mediapackage AwsProvider#mediapackage}
        :param mediapackagev2: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#mediapackagev2 AwsProvider#mediapackagev2}
        :param mediapackagevod: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#mediapackagevod AwsProvider#mediapackagevod}
        :param mediastore: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#mediastore AwsProvider#mediastore}
        :param memorydb: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#memorydb AwsProvider#memorydb}
        :param mgn: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#mgn AwsProvider#mgn}
        :param mq: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#mq AwsProvider#mq}
        :param msk: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#msk AwsProvider#msk}
        :param mwaa: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#mwaa AwsProvider#mwaa}
        :param neptune: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#neptune AwsProvider#neptune}
        :param neptunegraph: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#neptunegraph AwsProvider#neptunegraph}
        :param networkfirewall: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#networkfirewall AwsProvider#networkfirewall}
        :param networkmanager: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#networkmanager AwsProvider#networkmanager}
        :param networkmonitor: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#networkmonitor AwsProvider#networkmonitor}
        :param oam: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#oam AwsProvider#oam}
        :param opensearch: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#opensearch AwsProvider#opensearch}
        :param opensearchingestion: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#opensearchingestion AwsProvider#opensearchingestion}
        :param opensearchserverless: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#opensearchserverless AwsProvider#opensearchserverless}
        :param opensearchservice: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#opensearchservice AwsProvider#opensearchservice}
        :param opsworks: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#opsworks AwsProvider#opsworks}
        :param organizations: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#organizations AwsProvider#organizations}
        :param osis: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#osis AwsProvider#osis}
        :param outposts: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#outposts AwsProvider#outposts}
        :param paymentcryptography: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#paymentcryptography AwsProvider#paymentcryptography}
        :param pcaconnectorad: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#pcaconnectorad AwsProvider#pcaconnectorad}
        :param pcs: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#pcs AwsProvider#pcs}
        :param pinpoint: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#pinpoint AwsProvider#pinpoint}
        :param pinpointsmsvoicev2: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#pinpointsmsvoicev2 AwsProvider#pinpointsmsvoicev2}
        :param pipes: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#pipes AwsProvider#pipes}
        :param polly: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#polly AwsProvider#polly}
        :param pricing: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#pricing AwsProvider#pricing}
        :param prometheus: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#prometheus AwsProvider#prometheus}
        :param prometheusservice: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#prometheusservice AwsProvider#prometheusservice}
        :param qbusiness: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#qbusiness AwsProvider#qbusiness}
        :param qldb: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#qldb AwsProvider#qldb}
        :param quicksight: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#quicksight AwsProvider#quicksight}
        :param ram: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ram AwsProvider#ram}
        :param rbin: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#rbin AwsProvider#rbin}
        :param rds: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#rds AwsProvider#rds}
        :param recyclebin: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#recyclebin AwsProvider#recyclebin}
        :param redshift: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#redshift AwsProvider#redshift}
        :param redshiftdata: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#redshiftdata AwsProvider#redshiftdata}
        :param redshiftdataapiservice: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#redshiftdataapiservice AwsProvider#redshiftdataapiservice}
        :param redshiftserverless: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#redshiftserverless AwsProvider#redshiftserverless}
        :param rekognition: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#rekognition AwsProvider#rekognition}
        :param resiliencehub: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#resiliencehub AwsProvider#resiliencehub}
        :param resourceexplorer2: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#resourceexplorer2 AwsProvider#resourceexplorer2}
        :param resourcegroups: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#resourcegroups AwsProvider#resourcegroups}
        :param resourcegroupstagging: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#resourcegroupstagging AwsProvider#resourcegroupstagging}
        :param resourcegroupstaggingapi: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#resourcegroupstaggingapi AwsProvider#resourcegroupstaggingapi}
        :param rolesanywhere: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#rolesanywhere AwsProvider#rolesanywhere}
        :param route53: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#route53 AwsProvider#route53}
        :param route53_domains: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#route53domains AwsProvider#route53domains}
        :param route53_profiles: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#route53profiles AwsProvider#route53profiles}
        :param route53_recoverycontrolconfig: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#route53recoverycontrolconfig AwsProvider#route53recoverycontrolconfig}
        :param route53_recoveryreadiness: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#route53recoveryreadiness AwsProvider#route53recoveryreadiness}
        :param route53_resolver: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#route53resolver AwsProvider#route53resolver}
        :param rum: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#rum AwsProvider#rum}
        :param s3: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#s3 AwsProvider#s3}
        :param s3_api: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#s3api AwsProvider#s3api}
        :param s3_control: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#s3control AwsProvider#s3control}
        :param s3_outposts: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#s3outposts AwsProvider#s3outposts}
        :param s3_tables: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#s3tables AwsProvider#s3tables}
        :param sagemaker: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#sagemaker AwsProvider#sagemaker}
        :param scheduler: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#scheduler AwsProvider#scheduler}
        :param schemas: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#schemas AwsProvider#schemas}
        :param sdb: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#sdb AwsProvider#sdb}
        :param secretsmanager: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#secretsmanager AwsProvider#secretsmanager}
        :param securityhub: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#securityhub AwsProvider#securityhub}
        :param securitylake: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#securitylake AwsProvider#securitylake}
        :param serverlessapplicationrepository: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#serverlessapplicationrepository AwsProvider#serverlessapplicationrepository}
        :param serverlessapprepo: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#serverlessapprepo AwsProvider#serverlessapprepo}
        :param serverlessrepo: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#serverlessrepo AwsProvider#serverlessrepo}
        :param servicecatalog: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#servicecatalog AwsProvider#servicecatalog}
        :param servicecatalogappregistry: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#servicecatalogappregistry AwsProvider#servicecatalogappregistry}
        :param servicediscovery: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#servicediscovery AwsProvider#servicediscovery}
        :param servicequotas: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#servicequotas AwsProvider#servicequotas}
        :param ses: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ses AwsProvider#ses}
        :param sesv2: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#sesv2 AwsProvider#sesv2}
        :param sfn: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#sfn AwsProvider#sfn}
        :param shield: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#shield AwsProvider#shield}
        :param signer: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#signer AwsProvider#signer}
        :param simpledb: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#simpledb AwsProvider#simpledb}
        :param sns: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#sns AwsProvider#sns}
        :param sqs: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#sqs AwsProvider#sqs}
        :param ssm: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ssm AwsProvider#ssm}
        :param ssmcontacts: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ssmcontacts AwsProvider#ssmcontacts}
        :param ssmincidents: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ssmincidents AwsProvider#ssmincidents}
        :param ssmquicksetup: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ssmquicksetup AwsProvider#ssmquicksetup}
        :param ssmsap: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ssmsap AwsProvider#ssmsap}
        :param sso: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#sso AwsProvider#sso}
        :param ssoadmin: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ssoadmin AwsProvider#ssoadmin}
        :param stepfunctions: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#stepfunctions AwsProvider#stepfunctions}
        :param storagegateway: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#storagegateway AwsProvider#storagegateway}
        :param sts: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#sts AwsProvider#sts}
        :param swf: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#swf AwsProvider#swf}
        :param synthetics: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#synthetics AwsProvider#synthetics}
        :param taxsettings: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#taxsettings AwsProvider#taxsettings}
        :param timestreaminfluxdb: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#timestreaminfluxdb AwsProvider#timestreaminfluxdb}
        :param timestreamquery: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#timestreamquery AwsProvider#timestreamquery}
        :param timestreamwrite: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#timestreamwrite AwsProvider#timestreamwrite}
        :param transcribe: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#transcribe AwsProvider#transcribe}
        :param transcribeservice: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#transcribeservice AwsProvider#transcribeservice}
        :param transfer: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#transfer AwsProvider#transfer}
        :param verifiedpermissions: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#verifiedpermissions AwsProvider#verifiedpermissions}
        :param vpclattice: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#vpclattice AwsProvider#vpclattice}
        :param waf: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#waf AwsProvider#waf}
        :param wafregional: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#wafregional AwsProvider#wafregional}
        :param wafv2: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#wafv2 AwsProvider#wafv2}
        :param wellarchitected: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#wellarchitected AwsProvider#wellarchitected}
        :param worklink: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#worklink AwsProvider#worklink}
        :param workspaces: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#workspaces AwsProvider#workspaces}
        :param workspacesweb: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#workspacesweb AwsProvider#workspacesweb}
        :param xray: Use this to override the default service endpoint URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#xray AwsProvider#xray}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__912b8f0439a9c34ac3f441b30210524e0bb966c3363990a416d3e2f274939834)
            check_type(argname="argument accessanalyzer", value=accessanalyzer, expected_type=type_hints["accessanalyzer"])
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument acm", value=acm, expected_type=type_hints["acm"])
            check_type(argname="argument acmpca", value=acmpca, expected_type=type_hints["acmpca"])
            check_type(argname="argument amg", value=amg, expected_type=type_hints["amg"])
            check_type(argname="argument amp", value=amp, expected_type=type_hints["amp"])
            check_type(argname="argument amplify", value=amplify, expected_type=type_hints["amplify"])
            check_type(argname="argument apigateway", value=apigateway, expected_type=type_hints["apigateway"])
            check_type(argname="argument apigatewayv2", value=apigatewayv2, expected_type=type_hints["apigatewayv2"])
            check_type(argname="argument appautoscaling", value=appautoscaling, expected_type=type_hints["appautoscaling"])
            check_type(argname="argument appconfig", value=appconfig, expected_type=type_hints["appconfig"])
            check_type(argname="argument appfabric", value=appfabric, expected_type=type_hints["appfabric"])
            check_type(argname="argument appflow", value=appflow, expected_type=type_hints["appflow"])
            check_type(argname="argument appintegrations", value=appintegrations, expected_type=type_hints["appintegrations"])
            check_type(argname="argument appintegrationsservice", value=appintegrationsservice, expected_type=type_hints["appintegrationsservice"])
            check_type(argname="argument applicationautoscaling", value=applicationautoscaling, expected_type=type_hints["applicationautoscaling"])
            check_type(argname="argument applicationinsights", value=applicationinsights, expected_type=type_hints["applicationinsights"])
            check_type(argname="argument applicationsignals", value=applicationsignals, expected_type=type_hints["applicationsignals"])
            check_type(argname="argument appmesh", value=appmesh, expected_type=type_hints["appmesh"])
            check_type(argname="argument appregistry", value=appregistry, expected_type=type_hints["appregistry"])
            check_type(argname="argument apprunner", value=apprunner, expected_type=type_hints["apprunner"])
            check_type(argname="argument appstream", value=appstream, expected_type=type_hints["appstream"])
            check_type(argname="argument appsync", value=appsync, expected_type=type_hints["appsync"])
            check_type(argname="argument athena", value=athena, expected_type=type_hints["athena"])
            check_type(argname="argument auditmanager", value=auditmanager, expected_type=type_hints["auditmanager"])
            check_type(argname="argument autoscaling", value=autoscaling, expected_type=type_hints["autoscaling"])
            check_type(argname="argument autoscalingplans", value=autoscalingplans, expected_type=type_hints["autoscalingplans"])
            check_type(argname="argument backup", value=backup, expected_type=type_hints["backup"])
            check_type(argname="argument batch", value=batch, expected_type=type_hints["batch"])
            check_type(argname="argument bcmdataexports", value=bcmdataexports, expected_type=type_hints["bcmdataexports"])
            check_type(argname="argument beanstalk", value=beanstalk, expected_type=type_hints["beanstalk"])
            check_type(argname="argument bedrock", value=bedrock, expected_type=type_hints["bedrock"])
            check_type(argname="argument bedrockagent", value=bedrockagent, expected_type=type_hints["bedrockagent"])
            check_type(argname="argument billing", value=billing, expected_type=type_hints["billing"])
            check_type(argname="argument budgets", value=budgets, expected_type=type_hints["budgets"])
            check_type(argname="argument ce", value=ce, expected_type=type_hints["ce"])
            check_type(argname="argument chatbot", value=chatbot, expected_type=type_hints["chatbot"])
            check_type(argname="argument chime", value=chime, expected_type=type_hints["chime"])
            check_type(argname="argument chimesdkmediapipelines", value=chimesdkmediapipelines, expected_type=type_hints["chimesdkmediapipelines"])
            check_type(argname="argument chimesdkvoice", value=chimesdkvoice, expected_type=type_hints["chimesdkvoice"])
            check_type(argname="argument cleanrooms", value=cleanrooms, expected_type=type_hints["cleanrooms"])
            check_type(argname="argument cloud9", value=cloud9, expected_type=type_hints["cloud9"])
            check_type(argname="argument cloudcontrol", value=cloudcontrol, expected_type=type_hints["cloudcontrol"])
            check_type(argname="argument cloudcontrolapi", value=cloudcontrolapi, expected_type=type_hints["cloudcontrolapi"])
            check_type(argname="argument cloudformation", value=cloudformation, expected_type=type_hints["cloudformation"])
            check_type(argname="argument cloudfront", value=cloudfront, expected_type=type_hints["cloudfront"])
            check_type(argname="argument cloudfrontkeyvaluestore", value=cloudfrontkeyvaluestore, expected_type=type_hints["cloudfrontkeyvaluestore"])
            check_type(argname="argument cloudhsm", value=cloudhsm, expected_type=type_hints["cloudhsm"])
            check_type(argname="argument cloudhsmv2", value=cloudhsmv2, expected_type=type_hints["cloudhsmv2"])
            check_type(argname="argument cloudsearch", value=cloudsearch, expected_type=type_hints["cloudsearch"])
            check_type(argname="argument cloudtrail", value=cloudtrail, expected_type=type_hints["cloudtrail"])
            check_type(argname="argument cloudwatch", value=cloudwatch, expected_type=type_hints["cloudwatch"])
            check_type(argname="argument cloudwatchevents", value=cloudwatchevents, expected_type=type_hints["cloudwatchevents"])
            check_type(argname="argument cloudwatchevidently", value=cloudwatchevidently, expected_type=type_hints["cloudwatchevidently"])
            check_type(argname="argument cloudwatchlog", value=cloudwatchlog, expected_type=type_hints["cloudwatchlog"])
            check_type(argname="argument cloudwatchlogs", value=cloudwatchlogs, expected_type=type_hints["cloudwatchlogs"])
            check_type(argname="argument cloudwatchobservabilityaccessmanager", value=cloudwatchobservabilityaccessmanager, expected_type=type_hints["cloudwatchobservabilityaccessmanager"])
            check_type(argname="argument cloudwatchrum", value=cloudwatchrum, expected_type=type_hints["cloudwatchrum"])
            check_type(argname="argument codeartifact", value=codeartifact, expected_type=type_hints["codeartifact"])
            check_type(argname="argument codebuild", value=codebuild, expected_type=type_hints["codebuild"])
            check_type(argname="argument codecatalyst", value=codecatalyst, expected_type=type_hints["codecatalyst"])
            check_type(argname="argument codecommit", value=codecommit, expected_type=type_hints["codecommit"])
            check_type(argname="argument codeconnections", value=codeconnections, expected_type=type_hints["codeconnections"])
            check_type(argname="argument codedeploy", value=codedeploy, expected_type=type_hints["codedeploy"])
            check_type(argname="argument codeguruprofiler", value=codeguruprofiler, expected_type=type_hints["codeguruprofiler"])
            check_type(argname="argument codegurureviewer", value=codegurureviewer, expected_type=type_hints["codegurureviewer"])
            check_type(argname="argument codepipeline", value=codepipeline, expected_type=type_hints["codepipeline"])
            check_type(argname="argument codestarconnections", value=codestarconnections, expected_type=type_hints["codestarconnections"])
            check_type(argname="argument codestarnotifications", value=codestarnotifications, expected_type=type_hints["codestarnotifications"])
            check_type(argname="argument cognitoidentity", value=cognitoidentity, expected_type=type_hints["cognitoidentity"])
            check_type(argname="argument cognitoidentityprovider", value=cognitoidentityprovider, expected_type=type_hints["cognitoidentityprovider"])
            check_type(argname="argument cognitoidp", value=cognitoidp, expected_type=type_hints["cognitoidp"])
            check_type(argname="argument comprehend", value=comprehend, expected_type=type_hints["comprehend"])
            check_type(argname="argument computeoptimizer", value=computeoptimizer, expected_type=type_hints["computeoptimizer"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument configservice", value=configservice, expected_type=type_hints["configservice"])
            check_type(argname="argument connect", value=connect, expected_type=type_hints["connect"])
            check_type(argname="argument connectcases", value=connectcases, expected_type=type_hints["connectcases"])
            check_type(argname="argument controltower", value=controltower, expected_type=type_hints["controltower"])
            check_type(argname="argument costandusagereportservice", value=costandusagereportservice, expected_type=type_hints["costandusagereportservice"])
            check_type(argname="argument costexplorer", value=costexplorer, expected_type=type_hints["costexplorer"])
            check_type(argname="argument costoptimizationhub", value=costoptimizationhub, expected_type=type_hints["costoptimizationhub"])
            check_type(argname="argument cur", value=cur, expected_type=type_hints["cur"])
            check_type(argname="argument customerprofiles", value=customerprofiles, expected_type=type_hints["customerprofiles"])
            check_type(argname="argument databasemigration", value=databasemigration, expected_type=type_hints["databasemigration"])
            check_type(argname="argument databasemigrationservice", value=databasemigrationservice, expected_type=type_hints["databasemigrationservice"])
            check_type(argname="argument databrew", value=databrew, expected_type=type_hints["databrew"])
            check_type(argname="argument dataexchange", value=dataexchange, expected_type=type_hints["dataexchange"])
            check_type(argname="argument datapipeline", value=datapipeline, expected_type=type_hints["datapipeline"])
            check_type(argname="argument datasync", value=datasync, expected_type=type_hints["datasync"])
            check_type(argname="argument datazone", value=datazone, expected_type=type_hints["datazone"])
            check_type(argname="argument dax", value=dax, expected_type=type_hints["dax"])
            check_type(argname="argument deploy", value=deploy, expected_type=type_hints["deploy"])
            check_type(argname="argument detective", value=detective, expected_type=type_hints["detective"])
            check_type(argname="argument devicefarm", value=devicefarm, expected_type=type_hints["devicefarm"])
            check_type(argname="argument devopsguru", value=devopsguru, expected_type=type_hints["devopsguru"])
            check_type(argname="argument directconnect", value=directconnect, expected_type=type_hints["directconnect"])
            check_type(argname="argument directoryservice", value=directoryservice, expected_type=type_hints["directoryservice"])
            check_type(argname="argument dlm", value=dlm, expected_type=type_hints["dlm"])
            check_type(argname="argument dms", value=dms, expected_type=type_hints["dms"])
            check_type(argname="argument docdb", value=docdb, expected_type=type_hints["docdb"])
            check_type(argname="argument docdbelastic", value=docdbelastic, expected_type=type_hints["docdbelastic"])
            check_type(argname="argument drs", value=drs, expected_type=type_hints["drs"])
            check_type(argname="argument ds", value=ds, expected_type=type_hints["ds"])
            check_type(argname="argument dsql", value=dsql, expected_type=type_hints["dsql"])
            check_type(argname="argument dynamodb", value=dynamodb, expected_type=type_hints["dynamodb"])
            check_type(argname="argument ec2", value=ec2, expected_type=type_hints["ec2"])
            check_type(argname="argument ecr", value=ecr, expected_type=type_hints["ecr"])
            check_type(argname="argument ecrpublic", value=ecrpublic, expected_type=type_hints["ecrpublic"])
            check_type(argname="argument ecs", value=ecs, expected_type=type_hints["ecs"])
            check_type(argname="argument efs", value=efs, expected_type=type_hints["efs"])
            check_type(argname="argument eks", value=eks, expected_type=type_hints["eks"])
            check_type(argname="argument elasticache", value=elasticache, expected_type=type_hints["elasticache"])
            check_type(argname="argument elasticbeanstalk", value=elasticbeanstalk, expected_type=type_hints["elasticbeanstalk"])
            check_type(argname="argument elasticloadbalancing", value=elasticloadbalancing, expected_type=type_hints["elasticloadbalancing"])
            check_type(argname="argument elasticloadbalancingv2", value=elasticloadbalancingv2, expected_type=type_hints["elasticloadbalancingv2"])
            check_type(argname="argument elasticsearch", value=elasticsearch, expected_type=type_hints["elasticsearch"])
            check_type(argname="argument elasticsearchservice", value=elasticsearchservice, expected_type=type_hints["elasticsearchservice"])
            check_type(argname="argument elastictranscoder", value=elastictranscoder, expected_type=type_hints["elastictranscoder"])
            check_type(argname="argument elb", value=elb, expected_type=type_hints["elb"])
            check_type(argname="argument elbv2", value=elbv2, expected_type=type_hints["elbv2"])
            check_type(argname="argument emr", value=emr, expected_type=type_hints["emr"])
            check_type(argname="argument emrcontainers", value=emrcontainers, expected_type=type_hints["emrcontainers"])
            check_type(argname="argument emrserverless", value=emrserverless, expected_type=type_hints["emrserverless"])
            check_type(argname="argument es", value=es, expected_type=type_hints["es"])
            check_type(argname="argument eventbridge", value=eventbridge, expected_type=type_hints["eventbridge"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument evidently", value=evidently, expected_type=type_hints["evidently"])
            check_type(argname="argument finspace", value=finspace, expected_type=type_hints["finspace"])
            check_type(argname="argument firehose", value=firehose, expected_type=type_hints["firehose"])
            check_type(argname="argument fis", value=fis, expected_type=type_hints["fis"])
            check_type(argname="argument fms", value=fms, expected_type=type_hints["fms"])
            check_type(argname="argument fsx", value=fsx, expected_type=type_hints["fsx"])
            check_type(argname="argument gamelift", value=gamelift, expected_type=type_hints["gamelift"])
            check_type(argname="argument glacier", value=glacier, expected_type=type_hints["glacier"])
            check_type(argname="argument globalaccelerator", value=globalaccelerator, expected_type=type_hints["globalaccelerator"])
            check_type(argname="argument glue", value=glue, expected_type=type_hints["glue"])
            check_type(argname="argument gluedatabrew", value=gluedatabrew, expected_type=type_hints["gluedatabrew"])
            check_type(argname="argument grafana", value=grafana, expected_type=type_hints["grafana"])
            check_type(argname="argument greengrass", value=greengrass, expected_type=type_hints["greengrass"])
            check_type(argname="argument groundstation", value=groundstation, expected_type=type_hints["groundstation"])
            check_type(argname="argument guardduty", value=guardduty, expected_type=type_hints["guardduty"])
            check_type(argname="argument healthlake", value=healthlake, expected_type=type_hints["healthlake"])
            check_type(argname="argument iam", value=iam, expected_type=type_hints["iam"])
            check_type(argname="argument identitystore", value=identitystore, expected_type=type_hints["identitystore"])
            check_type(argname="argument imagebuilder", value=imagebuilder, expected_type=type_hints["imagebuilder"])
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
            check_type(argname="argument inspector2", value=inspector2, expected_type=type_hints["inspector2"])
            check_type(argname="argument inspectorv2", value=inspectorv2, expected_type=type_hints["inspectorv2"])
            check_type(argname="argument internetmonitor", value=internetmonitor, expected_type=type_hints["internetmonitor"])
            check_type(argname="argument invoicing", value=invoicing, expected_type=type_hints["invoicing"])
            check_type(argname="argument iot", value=iot, expected_type=type_hints["iot"])
            check_type(argname="argument iotanalytics", value=iotanalytics, expected_type=type_hints["iotanalytics"])
            check_type(argname="argument iotevents", value=iotevents, expected_type=type_hints["iotevents"])
            check_type(argname="argument ivs", value=ivs, expected_type=type_hints["ivs"])
            check_type(argname="argument ivschat", value=ivschat, expected_type=type_hints["ivschat"])
            check_type(argname="argument kafka", value=kafka, expected_type=type_hints["kafka"])
            check_type(argname="argument kafkaconnect", value=kafkaconnect, expected_type=type_hints["kafkaconnect"])
            check_type(argname="argument kendra", value=kendra, expected_type=type_hints["kendra"])
            check_type(argname="argument keyspaces", value=keyspaces, expected_type=type_hints["keyspaces"])
            check_type(argname="argument kinesis", value=kinesis, expected_type=type_hints["kinesis"])
            check_type(argname="argument kinesisanalytics", value=kinesisanalytics, expected_type=type_hints["kinesisanalytics"])
            check_type(argname="argument kinesisanalyticsv2", value=kinesisanalyticsv2, expected_type=type_hints["kinesisanalyticsv2"])
            check_type(argname="argument kinesisvideo", value=kinesisvideo, expected_type=type_hints["kinesisvideo"])
            check_type(argname="argument kms", value=kms, expected_type=type_hints["kms"])
            check_type(argname="argument lakeformation", value=lakeformation, expected_type=type_hints["lakeformation"])
            check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
            check_type(argname="argument launchwizard", value=launchwizard, expected_type=type_hints["launchwizard"])
            check_type(argname="argument lex", value=lex, expected_type=type_hints["lex"])
            check_type(argname="argument lexmodelbuilding", value=lexmodelbuilding, expected_type=type_hints["lexmodelbuilding"])
            check_type(argname="argument lexmodelbuildingservice", value=lexmodelbuildingservice, expected_type=type_hints["lexmodelbuildingservice"])
            check_type(argname="argument lexmodels", value=lexmodels, expected_type=type_hints["lexmodels"])
            check_type(argname="argument lexmodelsv2", value=lexmodelsv2, expected_type=type_hints["lexmodelsv2"])
            check_type(argname="argument lexv2_models", value=lexv2_models, expected_type=type_hints["lexv2_models"])
            check_type(argname="argument licensemanager", value=licensemanager, expected_type=type_hints["licensemanager"])
            check_type(argname="argument lightsail", value=lightsail, expected_type=type_hints["lightsail"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument locationservice", value=locationservice, expected_type=type_hints["locationservice"])
            check_type(argname="argument logs", value=logs, expected_type=type_hints["logs"])
            check_type(argname="argument lookoutmetrics", value=lookoutmetrics, expected_type=type_hints["lookoutmetrics"])
            check_type(argname="argument m2", value=m2, expected_type=type_hints["m2"])
            check_type(argname="argument macie2", value=macie2, expected_type=type_hints["macie2"])
            check_type(argname="argument managedgrafana", value=managedgrafana, expected_type=type_hints["managedgrafana"])
            check_type(argname="argument mediaconnect", value=mediaconnect, expected_type=type_hints["mediaconnect"])
            check_type(argname="argument mediaconvert", value=mediaconvert, expected_type=type_hints["mediaconvert"])
            check_type(argname="argument medialive", value=medialive, expected_type=type_hints["medialive"])
            check_type(argname="argument mediapackage", value=mediapackage, expected_type=type_hints["mediapackage"])
            check_type(argname="argument mediapackagev2", value=mediapackagev2, expected_type=type_hints["mediapackagev2"])
            check_type(argname="argument mediapackagevod", value=mediapackagevod, expected_type=type_hints["mediapackagevod"])
            check_type(argname="argument mediastore", value=mediastore, expected_type=type_hints["mediastore"])
            check_type(argname="argument memorydb", value=memorydb, expected_type=type_hints["memorydb"])
            check_type(argname="argument mgn", value=mgn, expected_type=type_hints["mgn"])
            check_type(argname="argument mq", value=mq, expected_type=type_hints["mq"])
            check_type(argname="argument msk", value=msk, expected_type=type_hints["msk"])
            check_type(argname="argument mwaa", value=mwaa, expected_type=type_hints["mwaa"])
            check_type(argname="argument neptune", value=neptune, expected_type=type_hints["neptune"])
            check_type(argname="argument neptunegraph", value=neptunegraph, expected_type=type_hints["neptunegraph"])
            check_type(argname="argument networkfirewall", value=networkfirewall, expected_type=type_hints["networkfirewall"])
            check_type(argname="argument networkmanager", value=networkmanager, expected_type=type_hints["networkmanager"])
            check_type(argname="argument networkmonitor", value=networkmonitor, expected_type=type_hints["networkmonitor"])
            check_type(argname="argument oam", value=oam, expected_type=type_hints["oam"])
            check_type(argname="argument opensearch", value=opensearch, expected_type=type_hints["opensearch"])
            check_type(argname="argument opensearchingestion", value=opensearchingestion, expected_type=type_hints["opensearchingestion"])
            check_type(argname="argument opensearchserverless", value=opensearchserverless, expected_type=type_hints["opensearchserverless"])
            check_type(argname="argument opensearchservice", value=opensearchservice, expected_type=type_hints["opensearchservice"])
            check_type(argname="argument opsworks", value=opsworks, expected_type=type_hints["opsworks"])
            check_type(argname="argument organizations", value=organizations, expected_type=type_hints["organizations"])
            check_type(argname="argument osis", value=osis, expected_type=type_hints["osis"])
            check_type(argname="argument outposts", value=outposts, expected_type=type_hints["outposts"])
            check_type(argname="argument paymentcryptography", value=paymentcryptography, expected_type=type_hints["paymentcryptography"])
            check_type(argname="argument pcaconnectorad", value=pcaconnectorad, expected_type=type_hints["pcaconnectorad"])
            check_type(argname="argument pcs", value=pcs, expected_type=type_hints["pcs"])
            check_type(argname="argument pinpoint", value=pinpoint, expected_type=type_hints["pinpoint"])
            check_type(argname="argument pinpointsmsvoicev2", value=pinpointsmsvoicev2, expected_type=type_hints["pinpointsmsvoicev2"])
            check_type(argname="argument pipes", value=pipes, expected_type=type_hints["pipes"])
            check_type(argname="argument polly", value=polly, expected_type=type_hints["polly"])
            check_type(argname="argument pricing", value=pricing, expected_type=type_hints["pricing"])
            check_type(argname="argument prometheus", value=prometheus, expected_type=type_hints["prometheus"])
            check_type(argname="argument prometheusservice", value=prometheusservice, expected_type=type_hints["prometheusservice"])
            check_type(argname="argument qbusiness", value=qbusiness, expected_type=type_hints["qbusiness"])
            check_type(argname="argument qldb", value=qldb, expected_type=type_hints["qldb"])
            check_type(argname="argument quicksight", value=quicksight, expected_type=type_hints["quicksight"])
            check_type(argname="argument ram", value=ram, expected_type=type_hints["ram"])
            check_type(argname="argument rbin", value=rbin, expected_type=type_hints["rbin"])
            check_type(argname="argument rds", value=rds, expected_type=type_hints["rds"])
            check_type(argname="argument recyclebin", value=recyclebin, expected_type=type_hints["recyclebin"])
            check_type(argname="argument redshift", value=redshift, expected_type=type_hints["redshift"])
            check_type(argname="argument redshiftdata", value=redshiftdata, expected_type=type_hints["redshiftdata"])
            check_type(argname="argument redshiftdataapiservice", value=redshiftdataapiservice, expected_type=type_hints["redshiftdataapiservice"])
            check_type(argname="argument redshiftserverless", value=redshiftserverless, expected_type=type_hints["redshiftserverless"])
            check_type(argname="argument rekognition", value=rekognition, expected_type=type_hints["rekognition"])
            check_type(argname="argument resiliencehub", value=resiliencehub, expected_type=type_hints["resiliencehub"])
            check_type(argname="argument resourceexplorer2", value=resourceexplorer2, expected_type=type_hints["resourceexplorer2"])
            check_type(argname="argument resourcegroups", value=resourcegroups, expected_type=type_hints["resourcegroups"])
            check_type(argname="argument resourcegroupstagging", value=resourcegroupstagging, expected_type=type_hints["resourcegroupstagging"])
            check_type(argname="argument resourcegroupstaggingapi", value=resourcegroupstaggingapi, expected_type=type_hints["resourcegroupstaggingapi"])
            check_type(argname="argument rolesanywhere", value=rolesanywhere, expected_type=type_hints["rolesanywhere"])
            check_type(argname="argument route53", value=route53, expected_type=type_hints["route53"])
            check_type(argname="argument route53_domains", value=route53_domains, expected_type=type_hints["route53_domains"])
            check_type(argname="argument route53_profiles", value=route53_profiles, expected_type=type_hints["route53_profiles"])
            check_type(argname="argument route53_recoverycontrolconfig", value=route53_recoverycontrolconfig, expected_type=type_hints["route53_recoverycontrolconfig"])
            check_type(argname="argument route53_recoveryreadiness", value=route53_recoveryreadiness, expected_type=type_hints["route53_recoveryreadiness"])
            check_type(argname="argument route53_resolver", value=route53_resolver, expected_type=type_hints["route53_resolver"])
            check_type(argname="argument rum", value=rum, expected_type=type_hints["rum"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument s3_api", value=s3_api, expected_type=type_hints["s3_api"])
            check_type(argname="argument s3_control", value=s3_control, expected_type=type_hints["s3_control"])
            check_type(argname="argument s3_outposts", value=s3_outposts, expected_type=type_hints["s3_outposts"])
            check_type(argname="argument s3_tables", value=s3_tables, expected_type=type_hints["s3_tables"])
            check_type(argname="argument sagemaker", value=sagemaker, expected_type=type_hints["sagemaker"])
            check_type(argname="argument scheduler", value=scheduler, expected_type=type_hints["scheduler"])
            check_type(argname="argument schemas", value=schemas, expected_type=type_hints["schemas"])
            check_type(argname="argument sdb", value=sdb, expected_type=type_hints["sdb"])
            check_type(argname="argument secretsmanager", value=secretsmanager, expected_type=type_hints["secretsmanager"])
            check_type(argname="argument securityhub", value=securityhub, expected_type=type_hints["securityhub"])
            check_type(argname="argument securitylake", value=securitylake, expected_type=type_hints["securitylake"])
            check_type(argname="argument serverlessapplicationrepository", value=serverlessapplicationrepository, expected_type=type_hints["serverlessapplicationrepository"])
            check_type(argname="argument serverlessapprepo", value=serverlessapprepo, expected_type=type_hints["serverlessapprepo"])
            check_type(argname="argument serverlessrepo", value=serverlessrepo, expected_type=type_hints["serverlessrepo"])
            check_type(argname="argument servicecatalog", value=servicecatalog, expected_type=type_hints["servicecatalog"])
            check_type(argname="argument servicecatalogappregistry", value=servicecatalogappregistry, expected_type=type_hints["servicecatalogappregistry"])
            check_type(argname="argument servicediscovery", value=servicediscovery, expected_type=type_hints["servicediscovery"])
            check_type(argname="argument servicequotas", value=servicequotas, expected_type=type_hints["servicequotas"])
            check_type(argname="argument ses", value=ses, expected_type=type_hints["ses"])
            check_type(argname="argument sesv2", value=sesv2, expected_type=type_hints["sesv2"])
            check_type(argname="argument sfn", value=sfn, expected_type=type_hints["sfn"])
            check_type(argname="argument shield", value=shield, expected_type=type_hints["shield"])
            check_type(argname="argument signer", value=signer, expected_type=type_hints["signer"])
            check_type(argname="argument simpledb", value=simpledb, expected_type=type_hints["simpledb"])
            check_type(argname="argument sns", value=sns, expected_type=type_hints["sns"])
            check_type(argname="argument sqs", value=sqs, expected_type=type_hints["sqs"])
            check_type(argname="argument ssm", value=ssm, expected_type=type_hints["ssm"])
            check_type(argname="argument ssmcontacts", value=ssmcontacts, expected_type=type_hints["ssmcontacts"])
            check_type(argname="argument ssmincidents", value=ssmincidents, expected_type=type_hints["ssmincidents"])
            check_type(argname="argument ssmquicksetup", value=ssmquicksetup, expected_type=type_hints["ssmquicksetup"])
            check_type(argname="argument ssmsap", value=ssmsap, expected_type=type_hints["ssmsap"])
            check_type(argname="argument sso", value=sso, expected_type=type_hints["sso"])
            check_type(argname="argument ssoadmin", value=ssoadmin, expected_type=type_hints["ssoadmin"])
            check_type(argname="argument stepfunctions", value=stepfunctions, expected_type=type_hints["stepfunctions"])
            check_type(argname="argument storagegateway", value=storagegateway, expected_type=type_hints["storagegateway"])
            check_type(argname="argument sts", value=sts, expected_type=type_hints["sts"])
            check_type(argname="argument swf", value=swf, expected_type=type_hints["swf"])
            check_type(argname="argument synthetics", value=synthetics, expected_type=type_hints["synthetics"])
            check_type(argname="argument taxsettings", value=taxsettings, expected_type=type_hints["taxsettings"])
            check_type(argname="argument timestreaminfluxdb", value=timestreaminfluxdb, expected_type=type_hints["timestreaminfluxdb"])
            check_type(argname="argument timestreamquery", value=timestreamquery, expected_type=type_hints["timestreamquery"])
            check_type(argname="argument timestreamwrite", value=timestreamwrite, expected_type=type_hints["timestreamwrite"])
            check_type(argname="argument transcribe", value=transcribe, expected_type=type_hints["transcribe"])
            check_type(argname="argument transcribeservice", value=transcribeservice, expected_type=type_hints["transcribeservice"])
            check_type(argname="argument transfer", value=transfer, expected_type=type_hints["transfer"])
            check_type(argname="argument verifiedpermissions", value=verifiedpermissions, expected_type=type_hints["verifiedpermissions"])
            check_type(argname="argument vpclattice", value=vpclattice, expected_type=type_hints["vpclattice"])
            check_type(argname="argument waf", value=waf, expected_type=type_hints["waf"])
            check_type(argname="argument wafregional", value=wafregional, expected_type=type_hints["wafregional"])
            check_type(argname="argument wafv2", value=wafv2, expected_type=type_hints["wafv2"])
            check_type(argname="argument wellarchitected", value=wellarchitected, expected_type=type_hints["wellarchitected"])
            check_type(argname="argument worklink", value=worklink, expected_type=type_hints["worklink"])
            check_type(argname="argument workspaces", value=workspaces, expected_type=type_hints["workspaces"])
            check_type(argname="argument workspacesweb", value=workspacesweb, expected_type=type_hints["workspacesweb"])
            check_type(argname="argument xray", value=xray, expected_type=type_hints["xray"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accessanalyzer is not None:
            self._values["accessanalyzer"] = accessanalyzer
        if account is not None:
            self._values["account"] = account
        if acm is not None:
            self._values["acm"] = acm
        if acmpca is not None:
            self._values["acmpca"] = acmpca
        if amg is not None:
            self._values["amg"] = amg
        if amp is not None:
            self._values["amp"] = amp
        if amplify is not None:
            self._values["amplify"] = amplify
        if apigateway is not None:
            self._values["apigateway"] = apigateway
        if apigatewayv2 is not None:
            self._values["apigatewayv2"] = apigatewayv2
        if appautoscaling is not None:
            self._values["appautoscaling"] = appautoscaling
        if appconfig is not None:
            self._values["appconfig"] = appconfig
        if appfabric is not None:
            self._values["appfabric"] = appfabric
        if appflow is not None:
            self._values["appflow"] = appflow
        if appintegrations is not None:
            self._values["appintegrations"] = appintegrations
        if appintegrationsservice is not None:
            self._values["appintegrationsservice"] = appintegrationsservice
        if applicationautoscaling is not None:
            self._values["applicationautoscaling"] = applicationautoscaling
        if applicationinsights is not None:
            self._values["applicationinsights"] = applicationinsights
        if applicationsignals is not None:
            self._values["applicationsignals"] = applicationsignals
        if appmesh is not None:
            self._values["appmesh"] = appmesh
        if appregistry is not None:
            self._values["appregistry"] = appregistry
        if apprunner is not None:
            self._values["apprunner"] = apprunner
        if appstream is not None:
            self._values["appstream"] = appstream
        if appsync is not None:
            self._values["appsync"] = appsync
        if athena is not None:
            self._values["athena"] = athena
        if auditmanager is not None:
            self._values["auditmanager"] = auditmanager
        if autoscaling is not None:
            self._values["autoscaling"] = autoscaling
        if autoscalingplans is not None:
            self._values["autoscalingplans"] = autoscalingplans
        if backup is not None:
            self._values["backup"] = backup
        if batch is not None:
            self._values["batch"] = batch
        if bcmdataexports is not None:
            self._values["bcmdataexports"] = bcmdataexports
        if beanstalk is not None:
            self._values["beanstalk"] = beanstalk
        if bedrock is not None:
            self._values["bedrock"] = bedrock
        if bedrockagent is not None:
            self._values["bedrockagent"] = bedrockagent
        if billing is not None:
            self._values["billing"] = billing
        if budgets is not None:
            self._values["budgets"] = budgets
        if ce is not None:
            self._values["ce"] = ce
        if chatbot is not None:
            self._values["chatbot"] = chatbot
        if chime is not None:
            self._values["chime"] = chime
        if chimesdkmediapipelines is not None:
            self._values["chimesdkmediapipelines"] = chimesdkmediapipelines
        if chimesdkvoice is not None:
            self._values["chimesdkvoice"] = chimesdkvoice
        if cleanrooms is not None:
            self._values["cleanrooms"] = cleanrooms
        if cloud9 is not None:
            self._values["cloud9"] = cloud9
        if cloudcontrol is not None:
            self._values["cloudcontrol"] = cloudcontrol
        if cloudcontrolapi is not None:
            self._values["cloudcontrolapi"] = cloudcontrolapi
        if cloudformation is not None:
            self._values["cloudformation"] = cloudformation
        if cloudfront is not None:
            self._values["cloudfront"] = cloudfront
        if cloudfrontkeyvaluestore is not None:
            self._values["cloudfrontkeyvaluestore"] = cloudfrontkeyvaluestore
        if cloudhsm is not None:
            self._values["cloudhsm"] = cloudhsm
        if cloudhsmv2 is not None:
            self._values["cloudhsmv2"] = cloudhsmv2
        if cloudsearch is not None:
            self._values["cloudsearch"] = cloudsearch
        if cloudtrail is not None:
            self._values["cloudtrail"] = cloudtrail
        if cloudwatch is not None:
            self._values["cloudwatch"] = cloudwatch
        if cloudwatchevents is not None:
            self._values["cloudwatchevents"] = cloudwatchevents
        if cloudwatchevidently is not None:
            self._values["cloudwatchevidently"] = cloudwatchevidently
        if cloudwatchlog is not None:
            self._values["cloudwatchlog"] = cloudwatchlog
        if cloudwatchlogs is not None:
            self._values["cloudwatchlogs"] = cloudwatchlogs
        if cloudwatchobservabilityaccessmanager is not None:
            self._values["cloudwatchobservabilityaccessmanager"] = cloudwatchobservabilityaccessmanager
        if cloudwatchrum is not None:
            self._values["cloudwatchrum"] = cloudwatchrum
        if codeartifact is not None:
            self._values["codeartifact"] = codeartifact
        if codebuild is not None:
            self._values["codebuild"] = codebuild
        if codecatalyst is not None:
            self._values["codecatalyst"] = codecatalyst
        if codecommit is not None:
            self._values["codecommit"] = codecommit
        if codeconnections is not None:
            self._values["codeconnections"] = codeconnections
        if codedeploy is not None:
            self._values["codedeploy"] = codedeploy
        if codeguruprofiler is not None:
            self._values["codeguruprofiler"] = codeguruprofiler
        if codegurureviewer is not None:
            self._values["codegurureviewer"] = codegurureviewer
        if codepipeline is not None:
            self._values["codepipeline"] = codepipeline
        if codestarconnections is not None:
            self._values["codestarconnections"] = codestarconnections
        if codestarnotifications is not None:
            self._values["codestarnotifications"] = codestarnotifications
        if cognitoidentity is not None:
            self._values["cognitoidentity"] = cognitoidentity
        if cognitoidentityprovider is not None:
            self._values["cognitoidentityprovider"] = cognitoidentityprovider
        if cognitoidp is not None:
            self._values["cognitoidp"] = cognitoidp
        if comprehend is not None:
            self._values["comprehend"] = comprehend
        if computeoptimizer is not None:
            self._values["computeoptimizer"] = computeoptimizer
        if config is not None:
            self._values["config"] = config
        if configservice is not None:
            self._values["configservice"] = configservice
        if connect is not None:
            self._values["connect"] = connect
        if connectcases is not None:
            self._values["connectcases"] = connectcases
        if controltower is not None:
            self._values["controltower"] = controltower
        if costandusagereportservice is not None:
            self._values["costandusagereportservice"] = costandusagereportservice
        if costexplorer is not None:
            self._values["costexplorer"] = costexplorer
        if costoptimizationhub is not None:
            self._values["costoptimizationhub"] = costoptimizationhub
        if cur is not None:
            self._values["cur"] = cur
        if customerprofiles is not None:
            self._values["customerprofiles"] = customerprofiles
        if databasemigration is not None:
            self._values["databasemigration"] = databasemigration
        if databasemigrationservice is not None:
            self._values["databasemigrationservice"] = databasemigrationservice
        if databrew is not None:
            self._values["databrew"] = databrew
        if dataexchange is not None:
            self._values["dataexchange"] = dataexchange
        if datapipeline is not None:
            self._values["datapipeline"] = datapipeline
        if datasync is not None:
            self._values["datasync"] = datasync
        if datazone is not None:
            self._values["datazone"] = datazone
        if dax is not None:
            self._values["dax"] = dax
        if deploy is not None:
            self._values["deploy"] = deploy
        if detective is not None:
            self._values["detective"] = detective
        if devicefarm is not None:
            self._values["devicefarm"] = devicefarm
        if devopsguru is not None:
            self._values["devopsguru"] = devopsguru
        if directconnect is not None:
            self._values["directconnect"] = directconnect
        if directoryservice is not None:
            self._values["directoryservice"] = directoryservice
        if dlm is not None:
            self._values["dlm"] = dlm
        if dms is not None:
            self._values["dms"] = dms
        if docdb is not None:
            self._values["docdb"] = docdb
        if docdbelastic is not None:
            self._values["docdbelastic"] = docdbelastic
        if drs is not None:
            self._values["drs"] = drs
        if ds is not None:
            self._values["ds"] = ds
        if dsql is not None:
            self._values["dsql"] = dsql
        if dynamodb is not None:
            self._values["dynamodb"] = dynamodb
        if ec2 is not None:
            self._values["ec2"] = ec2
        if ecr is not None:
            self._values["ecr"] = ecr
        if ecrpublic is not None:
            self._values["ecrpublic"] = ecrpublic
        if ecs is not None:
            self._values["ecs"] = ecs
        if efs is not None:
            self._values["efs"] = efs
        if eks is not None:
            self._values["eks"] = eks
        if elasticache is not None:
            self._values["elasticache"] = elasticache
        if elasticbeanstalk is not None:
            self._values["elasticbeanstalk"] = elasticbeanstalk
        if elasticloadbalancing is not None:
            self._values["elasticloadbalancing"] = elasticloadbalancing
        if elasticloadbalancingv2 is not None:
            self._values["elasticloadbalancingv2"] = elasticloadbalancingv2
        if elasticsearch is not None:
            self._values["elasticsearch"] = elasticsearch
        if elasticsearchservice is not None:
            self._values["elasticsearchservice"] = elasticsearchservice
        if elastictranscoder is not None:
            self._values["elastictranscoder"] = elastictranscoder
        if elb is not None:
            self._values["elb"] = elb
        if elbv2 is not None:
            self._values["elbv2"] = elbv2
        if emr is not None:
            self._values["emr"] = emr
        if emrcontainers is not None:
            self._values["emrcontainers"] = emrcontainers
        if emrserverless is not None:
            self._values["emrserverless"] = emrserverless
        if es is not None:
            self._values["es"] = es
        if eventbridge is not None:
            self._values["eventbridge"] = eventbridge
        if events is not None:
            self._values["events"] = events
        if evidently is not None:
            self._values["evidently"] = evidently
        if finspace is not None:
            self._values["finspace"] = finspace
        if firehose is not None:
            self._values["firehose"] = firehose
        if fis is not None:
            self._values["fis"] = fis
        if fms is not None:
            self._values["fms"] = fms
        if fsx is not None:
            self._values["fsx"] = fsx
        if gamelift is not None:
            self._values["gamelift"] = gamelift
        if glacier is not None:
            self._values["glacier"] = glacier
        if globalaccelerator is not None:
            self._values["globalaccelerator"] = globalaccelerator
        if glue is not None:
            self._values["glue"] = glue
        if gluedatabrew is not None:
            self._values["gluedatabrew"] = gluedatabrew
        if grafana is not None:
            self._values["grafana"] = grafana
        if greengrass is not None:
            self._values["greengrass"] = greengrass
        if groundstation is not None:
            self._values["groundstation"] = groundstation
        if guardduty is not None:
            self._values["guardduty"] = guardduty
        if healthlake is not None:
            self._values["healthlake"] = healthlake
        if iam is not None:
            self._values["iam"] = iam
        if identitystore is not None:
            self._values["identitystore"] = identitystore
        if imagebuilder is not None:
            self._values["imagebuilder"] = imagebuilder
        if inspector is not None:
            self._values["inspector"] = inspector
        if inspector2 is not None:
            self._values["inspector2"] = inspector2
        if inspectorv2 is not None:
            self._values["inspectorv2"] = inspectorv2
        if internetmonitor is not None:
            self._values["internetmonitor"] = internetmonitor
        if invoicing is not None:
            self._values["invoicing"] = invoicing
        if iot is not None:
            self._values["iot"] = iot
        if iotanalytics is not None:
            self._values["iotanalytics"] = iotanalytics
        if iotevents is not None:
            self._values["iotevents"] = iotevents
        if ivs is not None:
            self._values["ivs"] = ivs
        if ivschat is not None:
            self._values["ivschat"] = ivschat
        if kafka is not None:
            self._values["kafka"] = kafka
        if kafkaconnect is not None:
            self._values["kafkaconnect"] = kafkaconnect
        if kendra is not None:
            self._values["kendra"] = kendra
        if keyspaces is not None:
            self._values["keyspaces"] = keyspaces
        if kinesis is not None:
            self._values["kinesis"] = kinesis
        if kinesisanalytics is not None:
            self._values["kinesisanalytics"] = kinesisanalytics
        if kinesisanalyticsv2 is not None:
            self._values["kinesisanalyticsv2"] = kinesisanalyticsv2
        if kinesisvideo is not None:
            self._values["kinesisvideo"] = kinesisvideo
        if kms is not None:
            self._values["kms"] = kms
        if lakeformation is not None:
            self._values["lakeformation"] = lakeformation
        if lambda_ is not None:
            self._values["lambda_"] = lambda_
        if launchwizard is not None:
            self._values["launchwizard"] = launchwizard
        if lex is not None:
            self._values["lex"] = lex
        if lexmodelbuilding is not None:
            self._values["lexmodelbuilding"] = lexmodelbuilding
        if lexmodelbuildingservice is not None:
            self._values["lexmodelbuildingservice"] = lexmodelbuildingservice
        if lexmodels is not None:
            self._values["lexmodels"] = lexmodels
        if lexmodelsv2 is not None:
            self._values["lexmodelsv2"] = lexmodelsv2
        if lexv2_models is not None:
            self._values["lexv2_models"] = lexv2_models
        if licensemanager is not None:
            self._values["licensemanager"] = licensemanager
        if lightsail is not None:
            self._values["lightsail"] = lightsail
        if location is not None:
            self._values["location"] = location
        if locationservice is not None:
            self._values["locationservice"] = locationservice
        if logs is not None:
            self._values["logs"] = logs
        if lookoutmetrics is not None:
            self._values["lookoutmetrics"] = lookoutmetrics
        if m2 is not None:
            self._values["m2"] = m2
        if macie2 is not None:
            self._values["macie2"] = macie2
        if managedgrafana is not None:
            self._values["managedgrafana"] = managedgrafana
        if mediaconnect is not None:
            self._values["mediaconnect"] = mediaconnect
        if mediaconvert is not None:
            self._values["mediaconvert"] = mediaconvert
        if medialive is not None:
            self._values["medialive"] = medialive
        if mediapackage is not None:
            self._values["mediapackage"] = mediapackage
        if mediapackagev2 is not None:
            self._values["mediapackagev2"] = mediapackagev2
        if mediapackagevod is not None:
            self._values["mediapackagevod"] = mediapackagevod
        if mediastore is not None:
            self._values["mediastore"] = mediastore
        if memorydb is not None:
            self._values["memorydb"] = memorydb
        if mgn is not None:
            self._values["mgn"] = mgn
        if mq is not None:
            self._values["mq"] = mq
        if msk is not None:
            self._values["msk"] = msk
        if mwaa is not None:
            self._values["mwaa"] = mwaa
        if neptune is not None:
            self._values["neptune"] = neptune
        if neptunegraph is not None:
            self._values["neptunegraph"] = neptunegraph
        if networkfirewall is not None:
            self._values["networkfirewall"] = networkfirewall
        if networkmanager is not None:
            self._values["networkmanager"] = networkmanager
        if networkmonitor is not None:
            self._values["networkmonitor"] = networkmonitor
        if oam is not None:
            self._values["oam"] = oam
        if opensearch is not None:
            self._values["opensearch"] = opensearch
        if opensearchingestion is not None:
            self._values["opensearchingestion"] = opensearchingestion
        if opensearchserverless is not None:
            self._values["opensearchserverless"] = opensearchserverless
        if opensearchservice is not None:
            self._values["opensearchservice"] = opensearchservice
        if opsworks is not None:
            self._values["opsworks"] = opsworks
        if organizations is not None:
            self._values["organizations"] = organizations
        if osis is not None:
            self._values["osis"] = osis
        if outposts is not None:
            self._values["outposts"] = outposts
        if paymentcryptography is not None:
            self._values["paymentcryptography"] = paymentcryptography
        if pcaconnectorad is not None:
            self._values["pcaconnectorad"] = pcaconnectorad
        if pcs is not None:
            self._values["pcs"] = pcs
        if pinpoint is not None:
            self._values["pinpoint"] = pinpoint
        if pinpointsmsvoicev2 is not None:
            self._values["pinpointsmsvoicev2"] = pinpointsmsvoicev2
        if pipes is not None:
            self._values["pipes"] = pipes
        if polly is not None:
            self._values["polly"] = polly
        if pricing is not None:
            self._values["pricing"] = pricing
        if prometheus is not None:
            self._values["prometheus"] = prometheus
        if prometheusservice is not None:
            self._values["prometheusservice"] = prometheusservice
        if qbusiness is not None:
            self._values["qbusiness"] = qbusiness
        if qldb is not None:
            self._values["qldb"] = qldb
        if quicksight is not None:
            self._values["quicksight"] = quicksight
        if ram is not None:
            self._values["ram"] = ram
        if rbin is not None:
            self._values["rbin"] = rbin
        if rds is not None:
            self._values["rds"] = rds
        if recyclebin is not None:
            self._values["recyclebin"] = recyclebin
        if redshift is not None:
            self._values["redshift"] = redshift
        if redshiftdata is not None:
            self._values["redshiftdata"] = redshiftdata
        if redshiftdataapiservice is not None:
            self._values["redshiftdataapiservice"] = redshiftdataapiservice
        if redshiftserverless is not None:
            self._values["redshiftserverless"] = redshiftserverless
        if rekognition is not None:
            self._values["rekognition"] = rekognition
        if resiliencehub is not None:
            self._values["resiliencehub"] = resiliencehub
        if resourceexplorer2 is not None:
            self._values["resourceexplorer2"] = resourceexplorer2
        if resourcegroups is not None:
            self._values["resourcegroups"] = resourcegroups
        if resourcegroupstagging is not None:
            self._values["resourcegroupstagging"] = resourcegroupstagging
        if resourcegroupstaggingapi is not None:
            self._values["resourcegroupstaggingapi"] = resourcegroupstaggingapi
        if rolesanywhere is not None:
            self._values["rolesanywhere"] = rolesanywhere
        if route53 is not None:
            self._values["route53"] = route53
        if route53_domains is not None:
            self._values["route53_domains"] = route53_domains
        if route53_profiles is not None:
            self._values["route53_profiles"] = route53_profiles
        if route53_recoverycontrolconfig is not None:
            self._values["route53_recoverycontrolconfig"] = route53_recoverycontrolconfig
        if route53_recoveryreadiness is not None:
            self._values["route53_recoveryreadiness"] = route53_recoveryreadiness
        if route53_resolver is not None:
            self._values["route53_resolver"] = route53_resolver
        if rum is not None:
            self._values["rum"] = rum
        if s3 is not None:
            self._values["s3"] = s3
        if s3_api is not None:
            self._values["s3_api"] = s3_api
        if s3_control is not None:
            self._values["s3_control"] = s3_control
        if s3_outposts is not None:
            self._values["s3_outposts"] = s3_outposts
        if s3_tables is not None:
            self._values["s3_tables"] = s3_tables
        if sagemaker is not None:
            self._values["sagemaker"] = sagemaker
        if scheduler is not None:
            self._values["scheduler"] = scheduler
        if schemas is not None:
            self._values["schemas"] = schemas
        if sdb is not None:
            self._values["sdb"] = sdb
        if secretsmanager is not None:
            self._values["secretsmanager"] = secretsmanager
        if securityhub is not None:
            self._values["securityhub"] = securityhub
        if securitylake is not None:
            self._values["securitylake"] = securitylake
        if serverlessapplicationrepository is not None:
            self._values["serverlessapplicationrepository"] = serverlessapplicationrepository
        if serverlessapprepo is not None:
            self._values["serverlessapprepo"] = serverlessapprepo
        if serverlessrepo is not None:
            self._values["serverlessrepo"] = serverlessrepo
        if servicecatalog is not None:
            self._values["servicecatalog"] = servicecatalog
        if servicecatalogappregistry is not None:
            self._values["servicecatalogappregistry"] = servicecatalogappregistry
        if servicediscovery is not None:
            self._values["servicediscovery"] = servicediscovery
        if servicequotas is not None:
            self._values["servicequotas"] = servicequotas
        if ses is not None:
            self._values["ses"] = ses
        if sesv2 is not None:
            self._values["sesv2"] = sesv2
        if sfn is not None:
            self._values["sfn"] = sfn
        if shield is not None:
            self._values["shield"] = shield
        if signer is not None:
            self._values["signer"] = signer
        if simpledb is not None:
            self._values["simpledb"] = simpledb
        if sns is not None:
            self._values["sns"] = sns
        if sqs is not None:
            self._values["sqs"] = sqs
        if ssm is not None:
            self._values["ssm"] = ssm
        if ssmcontacts is not None:
            self._values["ssmcontacts"] = ssmcontacts
        if ssmincidents is not None:
            self._values["ssmincidents"] = ssmincidents
        if ssmquicksetup is not None:
            self._values["ssmquicksetup"] = ssmquicksetup
        if ssmsap is not None:
            self._values["ssmsap"] = ssmsap
        if sso is not None:
            self._values["sso"] = sso
        if ssoadmin is not None:
            self._values["ssoadmin"] = ssoadmin
        if stepfunctions is not None:
            self._values["stepfunctions"] = stepfunctions
        if storagegateway is not None:
            self._values["storagegateway"] = storagegateway
        if sts is not None:
            self._values["sts"] = sts
        if swf is not None:
            self._values["swf"] = swf
        if synthetics is not None:
            self._values["synthetics"] = synthetics
        if taxsettings is not None:
            self._values["taxsettings"] = taxsettings
        if timestreaminfluxdb is not None:
            self._values["timestreaminfluxdb"] = timestreaminfluxdb
        if timestreamquery is not None:
            self._values["timestreamquery"] = timestreamquery
        if timestreamwrite is not None:
            self._values["timestreamwrite"] = timestreamwrite
        if transcribe is not None:
            self._values["transcribe"] = transcribe
        if transcribeservice is not None:
            self._values["transcribeservice"] = transcribeservice
        if transfer is not None:
            self._values["transfer"] = transfer
        if verifiedpermissions is not None:
            self._values["verifiedpermissions"] = verifiedpermissions
        if vpclattice is not None:
            self._values["vpclattice"] = vpclattice
        if waf is not None:
            self._values["waf"] = waf
        if wafregional is not None:
            self._values["wafregional"] = wafregional
        if wafv2 is not None:
            self._values["wafv2"] = wafv2
        if wellarchitected is not None:
            self._values["wellarchitected"] = wellarchitected
        if worklink is not None:
            self._values["worklink"] = worklink
        if workspaces is not None:
            self._values["workspaces"] = workspaces
        if workspacesweb is not None:
            self._values["workspacesweb"] = workspacesweb
        if xray is not None:
            self._values["xray"] = xray

    @builtins.property
    def accessanalyzer(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#accessanalyzer AwsProvider#accessanalyzer}
        '''
        result = self._values.get("accessanalyzer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#account AwsProvider#account}
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def acm(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#acm AwsProvider#acm}
        '''
        result = self._values.get("acm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def acmpca(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#acmpca AwsProvider#acmpca}
        '''
        result = self._values.get("acmpca")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def amg(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#amg AwsProvider#amg}
        '''
        result = self._values.get("amg")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def amp(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#amp AwsProvider#amp}
        '''
        result = self._values.get("amp")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def amplify(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#amplify AwsProvider#amplify}
        '''
        result = self._values.get("amplify")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def apigateway(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#apigateway AwsProvider#apigateway}
        '''
        result = self._values.get("apigateway")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def apigatewayv2(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#apigatewayv2 AwsProvider#apigatewayv2}
        '''
        result = self._values.get("apigatewayv2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def appautoscaling(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#appautoscaling AwsProvider#appautoscaling}
        '''
        result = self._values.get("appautoscaling")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def appconfig(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#appconfig AwsProvider#appconfig}
        '''
        result = self._values.get("appconfig")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def appfabric(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#appfabric AwsProvider#appfabric}
        '''
        result = self._values.get("appfabric")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def appflow(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#appflow AwsProvider#appflow}
        '''
        result = self._values.get("appflow")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def appintegrations(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#appintegrations AwsProvider#appintegrations}
        '''
        result = self._values.get("appintegrations")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def appintegrationsservice(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#appintegrationsservice AwsProvider#appintegrationsservice}
        '''
        result = self._values.get("appintegrationsservice")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def applicationautoscaling(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#applicationautoscaling AwsProvider#applicationautoscaling}
        '''
        result = self._values.get("applicationautoscaling")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def applicationinsights(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#applicationinsights AwsProvider#applicationinsights}
        '''
        result = self._values.get("applicationinsights")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def applicationsignals(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#applicationsignals AwsProvider#applicationsignals}
        '''
        result = self._values.get("applicationsignals")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def appmesh(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#appmesh AwsProvider#appmesh}
        '''
        result = self._values.get("appmesh")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def appregistry(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#appregistry AwsProvider#appregistry}
        '''
        result = self._values.get("appregistry")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def apprunner(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#apprunner AwsProvider#apprunner}
        '''
        result = self._values.get("apprunner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def appstream(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#appstream AwsProvider#appstream}
        '''
        result = self._values.get("appstream")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def appsync(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#appsync AwsProvider#appsync}
        '''
        result = self._values.get("appsync")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def athena(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#athena AwsProvider#athena}
        '''
        result = self._values.get("athena")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auditmanager(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#auditmanager AwsProvider#auditmanager}
        '''
        result = self._values.get("auditmanager")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def autoscaling(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#autoscaling AwsProvider#autoscaling}
        '''
        result = self._values.get("autoscaling")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def autoscalingplans(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#autoscalingplans AwsProvider#autoscalingplans}
        '''
        result = self._values.get("autoscalingplans")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#backup AwsProvider#backup}
        '''
        result = self._values.get("backup")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def batch(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#batch AwsProvider#batch}
        '''
        result = self._values.get("batch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bcmdataexports(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#bcmdataexports AwsProvider#bcmdataexports}
        '''
        result = self._values.get("bcmdataexports")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def beanstalk(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#beanstalk AwsProvider#beanstalk}
        '''
        result = self._values.get("beanstalk")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bedrock(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#bedrock AwsProvider#bedrock}
        '''
        result = self._values.get("bedrock")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bedrockagent(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#bedrockagent AwsProvider#bedrockagent}
        '''
        result = self._values.get("bedrockagent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def billing(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#billing AwsProvider#billing}
        '''
        result = self._values.get("billing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def budgets(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#budgets AwsProvider#budgets}
        '''
        result = self._values.get("budgets")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ce(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ce AwsProvider#ce}
        '''
        result = self._values.get("ce")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def chatbot(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#chatbot AwsProvider#chatbot}
        '''
        result = self._values.get("chatbot")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def chime(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#chime AwsProvider#chime}
        '''
        result = self._values.get("chime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def chimesdkmediapipelines(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#chimesdkmediapipelines AwsProvider#chimesdkmediapipelines}
        '''
        result = self._values.get("chimesdkmediapipelines")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def chimesdkvoice(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#chimesdkvoice AwsProvider#chimesdkvoice}
        '''
        result = self._values.get("chimesdkvoice")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cleanrooms(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cleanrooms AwsProvider#cleanrooms}
        '''
        result = self._values.get("cleanrooms")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud9(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloud9 AwsProvider#cloud9}
        '''
        result = self._values.get("cloud9")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudcontrol(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudcontrol AwsProvider#cloudcontrol}
        '''
        result = self._values.get("cloudcontrol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudcontrolapi(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudcontrolapi AwsProvider#cloudcontrolapi}
        '''
        result = self._values.get("cloudcontrolapi")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudformation(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudformation AwsProvider#cloudformation}
        '''
        result = self._values.get("cloudformation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudfront(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudfront AwsProvider#cloudfront}
        '''
        result = self._values.get("cloudfront")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudfrontkeyvaluestore(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudfrontkeyvaluestore AwsProvider#cloudfrontkeyvaluestore}
        '''
        result = self._values.get("cloudfrontkeyvaluestore")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudhsm(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudhsm AwsProvider#cloudhsm}
        '''
        result = self._values.get("cloudhsm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudhsmv2(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudhsmv2 AwsProvider#cloudhsmv2}
        '''
        result = self._values.get("cloudhsmv2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudsearch(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudsearch AwsProvider#cloudsearch}
        '''
        result = self._values.get("cloudsearch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudtrail(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudtrail AwsProvider#cloudtrail}
        '''
        result = self._values.get("cloudtrail")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudwatch(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudwatch AwsProvider#cloudwatch}
        '''
        result = self._values.get("cloudwatch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudwatchevents(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudwatchevents AwsProvider#cloudwatchevents}
        '''
        result = self._values.get("cloudwatchevents")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudwatchevidently(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudwatchevidently AwsProvider#cloudwatchevidently}
        '''
        result = self._values.get("cloudwatchevidently")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudwatchlog(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudwatchlog AwsProvider#cloudwatchlog}
        '''
        result = self._values.get("cloudwatchlog")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudwatchlogs(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudwatchlogs AwsProvider#cloudwatchlogs}
        '''
        result = self._values.get("cloudwatchlogs")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudwatchobservabilityaccessmanager(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudwatchobservabilityaccessmanager AwsProvider#cloudwatchobservabilityaccessmanager}
        '''
        result = self._values.get("cloudwatchobservabilityaccessmanager")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudwatchrum(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cloudwatchrum AwsProvider#cloudwatchrum}
        '''
        result = self._values.get("cloudwatchrum")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def codeartifact(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codeartifact AwsProvider#codeartifact}
        '''
        result = self._values.get("codeartifact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def codebuild(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codebuild AwsProvider#codebuild}
        '''
        result = self._values.get("codebuild")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def codecatalyst(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codecatalyst AwsProvider#codecatalyst}
        '''
        result = self._values.get("codecatalyst")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def codecommit(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codecommit AwsProvider#codecommit}
        '''
        result = self._values.get("codecommit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def codeconnections(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codeconnections AwsProvider#codeconnections}
        '''
        result = self._values.get("codeconnections")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def codedeploy(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codedeploy AwsProvider#codedeploy}
        '''
        result = self._values.get("codedeploy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def codeguruprofiler(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codeguruprofiler AwsProvider#codeguruprofiler}
        '''
        result = self._values.get("codeguruprofiler")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def codegurureviewer(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codegurureviewer AwsProvider#codegurureviewer}
        '''
        result = self._values.get("codegurureviewer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def codepipeline(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codepipeline AwsProvider#codepipeline}
        '''
        result = self._values.get("codepipeline")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def codestarconnections(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codestarconnections AwsProvider#codestarconnections}
        '''
        result = self._values.get("codestarconnections")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def codestarnotifications(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#codestarnotifications AwsProvider#codestarnotifications}
        '''
        result = self._values.get("codestarnotifications")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cognitoidentity(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cognitoidentity AwsProvider#cognitoidentity}
        '''
        result = self._values.get("cognitoidentity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cognitoidentityprovider(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cognitoidentityprovider AwsProvider#cognitoidentityprovider}
        '''
        result = self._values.get("cognitoidentityprovider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cognitoidp(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cognitoidp AwsProvider#cognitoidp}
        '''
        result = self._values.get("cognitoidp")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comprehend(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#comprehend AwsProvider#comprehend}
        '''
        result = self._values.get("comprehend")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def computeoptimizer(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#computeoptimizer AwsProvider#computeoptimizer}
        '''
        result = self._values.get("computeoptimizer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def config(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#config AwsProvider#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configservice(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#configservice AwsProvider#configservice}
        '''
        result = self._values.get("configservice")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connect(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#connect AwsProvider#connect}
        '''
        result = self._values.get("connect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connectcases(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#connectcases AwsProvider#connectcases}
        '''
        result = self._values.get("connectcases")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def controltower(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#controltower AwsProvider#controltower}
        '''
        result = self._values.get("controltower")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def costandusagereportservice(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#costandusagereportservice AwsProvider#costandusagereportservice}
        '''
        result = self._values.get("costandusagereportservice")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def costexplorer(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#costexplorer AwsProvider#costexplorer}
        '''
        result = self._values.get("costexplorer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def costoptimizationhub(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#costoptimizationhub AwsProvider#costoptimizationhub}
        '''
        result = self._values.get("costoptimizationhub")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cur(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#cur AwsProvider#cur}
        '''
        result = self._values.get("cur")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def customerprofiles(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#customerprofiles AwsProvider#customerprofiles}
        '''
        result = self._values.get("customerprofiles")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def databasemigration(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#databasemigration AwsProvider#databasemigration}
        '''
        result = self._values.get("databasemigration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def databasemigrationservice(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#databasemigrationservice AwsProvider#databasemigrationservice}
        '''
        result = self._values.get("databasemigrationservice")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def databrew(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#databrew AwsProvider#databrew}
        '''
        result = self._values.get("databrew")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dataexchange(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#dataexchange AwsProvider#dataexchange}
        '''
        result = self._values.get("dataexchange")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datapipeline(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#datapipeline AwsProvider#datapipeline}
        '''
        result = self._values.get("datapipeline")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datasync(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#datasync AwsProvider#datasync}
        '''
        result = self._values.get("datasync")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datazone(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#datazone AwsProvider#datazone}
        '''
        result = self._values.get("datazone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dax(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#dax AwsProvider#dax}
        '''
        result = self._values.get("dax")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deploy(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#deploy AwsProvider#deploy}
        '''
        result = self._values.get("deploy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def detective(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#detective AwsProvider#detective}
        '''
        result = self._values.get("detective")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def devicefarm(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#devicefarm AwsProvider#devicefarm}
        '''
        result = self._values.get("devicefarm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def devopsguru(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#devopsguru AwsProvider#devopsguru}
        '''
        result = self._values.get("devopsguru")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def directconnect(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#directconnect AwsProvider#directconnect}
        '''
        result = self._values.get("directconnect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def directoryservice(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#directoryservice AwsProvider#directoryservice}
        '''
        result = self._values.get("directoryservice")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dlm(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#dlm AwsProvider#dlm}
        '''
        result = self._values.get("dlm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dms(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#dms AwsProvider#dms}
        '''
        result = self._values.get("dms")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docdb(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#docdb AwsProvider#docdb}
        '''
        result = self._values.get("docdb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docdbelastic(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#docdbelastic AwsProvider#docdbelastic}
        '''
        result = self._values.get("docdbelastic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def drs(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#drs AwsProvider#drs}
        '''
        result = self._values.get("drs")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ds(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ds AwsProvider#ds}
        '''
        result = self._values.get("ds")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dsql(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#dsql AwsProvider#dsql}
        '''
        result = self._values.get("dsql")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dynamodb(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#dynamodb AwsProvider#dynamodb}
        '''
        result = self._values.get("dynamodb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ec2 AwsProvider#ec2}
        '''
        result = self._values.get("ec2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ecr(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ecr AwsProvider#ecr}
        '''
        result = self._values.get("ecr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ecrpublic(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ecrpublic AwsProvider#ecrpublic}
        '''
        result = self._values.get("ecrpublic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ecs(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ecs AwsProvider#ecs}
        '''
        result = self._values.get("ecs")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def efs(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#efs AwsProvider#efs}
        '''
        result = self._values.get("efs")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eks(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#eks AwsProvider#eks}
        '''
        result = self._values.get("eks")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticache(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#elasticache AwsProvider#elasticache}
        '''
        result = self._values.get("elasticache")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticbeanstalk(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#elasticbeanstalk AwsProvider#elasticbeanstalk}
        '''
        result = self._values.get("elasticbeanstalk")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticloadbalancing(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#elasticloadbalancing AwsProvider#elasticloadbalancing}
        '''
        result = self._values.get("elasticloadbalancing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticloadbalancingv2(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#elasticloadbalancingv2 AwsProvider#elasticloadbalancingv2}
        '''
        result = self._values.get("elasticloadbalancingv2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticsearch(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#elasticsearch AwsProvider#elasticsearch}
        '''
        result = self._values.get("elasticsearch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticsearchservice(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#elasticsearchservice AwsProvider#elasticsearchservice}
        '''
        result = self._values.get("elasticsearchservice")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elastictranscoder(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#elastictranscoder AwsProvider#elastictranscoder}
        '''
        result = self._values.get("elastictranscoder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elb(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#elb AwsProvider#elb}
        '''
        result = self._values.get("elb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elbv2(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#elbv2 AwsProvider#elbv2}
        '''
        result = self._values.get("elbv2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def emr(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#emr AwsProvider#emr}
        '''
        result = self._values.get("emr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def emrcontainers(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#emrcontainers AwsProvider#emrcontainers}
        '''
        result = self._values.get("emrcontainers")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def emrserverless(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#emrserverless AwsProvider#emrserverless}
        '''
        result = self._values.get("emrserverless")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def es(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#es AwsProvider#es}
        '''
        result = self._values.get("es")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eventbridge(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#eventbridge AwsProvider#eventbridge}
        '''
        result = self._values.get("eventbridge")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def events(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#events AwsProvider#events}
        '''
        result = self._values.get("events")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def evidently(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#evidently AwsProvider#evidently}
        '''
        result = self._values.get("evidently")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def finspace(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#finspace AwsProvider#finspace}
        '''
        result = self._values.get("finspace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firehose(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#firehose AwsProvider#firehose}
        '''
        result = self._values.get("firehose")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fis(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#fis AwsProvider#fis}
        '''
        result = self._values.get("fis")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fms(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#fms AwsProvider#fms}
        '''
        result = self._values.get("fms")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fsx(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#fsx AwsProvider#fsx}
        '''
        result = self._values.get("fsx")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gamelift(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#gamelift AwsProvider#gamelift}
        '''
        result = self._values.get("gamelift")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def glacier(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#glacier AwsProvider#glacier}
        '''
        result = self._values.get("glacier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def globalaccelerator(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#globalaccelerator AwsProvider#globalaccelerator}
        '''
        result = self._values.get("globalaccelerator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def glue(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#glue AwsProvider#glue}
        '''
        result = self._values.get("glue")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gluedatabrew(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#gluedatabrew AwsProvider#gluedatabrew}
        '''
        result = self._values.get("gluedatabrew")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grafana(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#grafana AwsProvider#grafana}
        '''
        result = self._values.get("grafana")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def greengrass(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#greengrass AwsProvider#greengrass}
        '''
        result = self._values.get("greengrass")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groundstation(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#groundstation AwsProvider#groundstation}
        '''
        result = self._values.get("groundstation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def guardduty(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#guardduty AwsProvider#guardduty}
        '''
        result = self._values.get("guardduty")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def healthlake(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#healthlake AwsProvider#healthlake}
        '''
        result = self._values.get("healthlake")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#iam AwsProvider#iam}
        '''
        result = self._values.get("iam")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identitystore(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#identitystore AwsProvider#identitystore}
        '''
        result = self._values.get("identitystore")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def imagebuilder(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#imagebuilder AwsProvider#imagebuilder}
        '''
        result = self._values.get("imagebuilder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inspector(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#inspector AwsProvider#inspector}
        '''
        result = self._values.get("inspector")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inspector2(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#inspector2 AwsProvider#inspector2}
        '''
        result = self._values.get("inspector2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inspectorv2(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#inspectorv2 AwsProvider#inspectorv2}
        '''
        result = self._values.get("inspectorv2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def internetmonitor(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#internetmonitor AwsProvider#internetmonitor}
        '''
        result = self._values.get("internetmonitor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invoicing(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#invoicing AwsProvider#invoicing}
        '''
        result = self._values.get("invoicing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iot(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#iot AwsProvider#iot}
        '''
        result = self._values.get("iot")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iotanalytics(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#iotanalytics AwsProvider#iotanalytics}
        '''
        result = self._values.get("iotanalytics")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iotevents(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#iotevents AwsProvider#iotevents}
        '''
        result = self._values.get("iotevents")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ivs(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ivs AwsProvider#ivs}
        '''
        result = self._values.get("ivs")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ivschat(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ivschat AwsProvider#ivschat}
        '''
        result = self._values.get("ivschat")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kafka(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#kafka AwsProvider#kafka}
        '''
        result = self._values.get("kafka")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kafkaconnect(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#kafkaconnect AwsProvider#kafkaconnect}
        '''
        result = self._values.get("kafkaconnect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kendra(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#kendra AwsProvider#kendra}
        '''
        result = self._values.get("kendra")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keyspaces(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#keyspaces AwsProvider#keyspaces}
        '''
        result = self._values.get("keyspaces")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kinesis(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#kinesis AwsProvider#kinesis}
        '''
        result = self._values.get("kinesis")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kinesisanalytics(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#kinesisanalytics AwsProvider#kinesisanalytics}
        '''
        result = self._values.get("kinesisanalytics")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kinesisanalyticsv2(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#kinesisanalyticsv2 AwsProvider#kinesisanalyticsv2}
        '''
        result = self._values.get("kinesisanalyticsv2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kinesisvideo(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#kinesisvideo AwsProvider#kinesisvideo}
        '''
        result = self._values.get("kinesisvideo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#kms AwsProvider#kms}
        '''
        result = self._values.get("kms")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lakeformation(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#lakeformation AwsProvider#lakeformation}
        '''
        result = self._values.get("lakeformation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#lambda AwsProvider#lambda}
        '''
        result = self._values.get("lambda_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def launchwizard(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#launchwizard AwsProvider#launchwizard}
        '''
        result = self._values.get("launchwizard")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lex(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#lex AwsProvider#lex}
        '''
        result = self._values.get("lex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lexmodelbuilding(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#lexmodelbuilding AwsProvider#lexmodelbuilding}
        '''
        result = self._values.get("lexmodelbuilding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lexmodelbuildingservice(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#lexmodelbuildingservice AwsProvider#lexmodelbuildingservice}
        '''
        result = self._values.get("lexmodelbuildingservice")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lexmodels(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#lexmodels AwsProvider#lexmodels}
        '''
        result = self._values.get("lexmodels")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lexmodelsv2(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#lexmodelsv2 AwsProvider#lexmodelsv2}
        '''
        result = self._values.get("lexmodelsv2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lexv2_models(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#lexv2models AwsProvider#lexv2models}
        '''
        result = self._values.get("lexv2_models")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def licensemanager(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#licensemanager AwsProvider#licensemanager}
        '''
        result = self._values.get("licensemanager")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lightsail(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#lightsail AwsProvider#lightsail}
        '''
        result = self._values.get("lightsail")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#location AwsProvider#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locationservice(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#locationservice AwsProvider#locationservice}
        '''
        result = self._values.get("locationservice")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logs(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#logs AwsProvider#logs}
        '''
        result = self._values.get("logs")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lookoutmetrics(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#lookoutmetrics AwsProvider#lookoutmetrics}
        '''
        result = self._values.get("lookoutmetrics")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def m2(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#m2 AwsProvider#m2}
        '''
        result = self._values.get("m2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def macie2(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#macie2 AwsProvider#macie2}
        '''
        result = self._values.get("macie2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managedgrafana(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#managedgrafana AwsProvider#managedgrafana}
        '''
        result = self._values.get("managedgrafana")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mediaconnect(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#mediaconnect AwsProvider#mediaconnect}
        '''
        result = self._values.get("mediaconnect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mediaconvert(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#mediaconvert AwsProvider#mediaconvert}
        '''
        result = self._values.get("mediaconvert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def medialive(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#medialive AwsProvider#medialive}
        '''
        result = self._values.get("medialive")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mediapackage(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#mediapackage AwsProvider#mediapackage}
        '''
        result = self._values.get("mediapackage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mediapackagev2(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#mediapackagev2 AwsProvider#mediapackagev2}
        '''
        result = self._values.get("mediapackagev2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mediapackagevod(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#mediapackagevod AwsProvider#mediapackagevod}
        '''
        result = self._values.get("mediapackagevod")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mediastore(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#mediastore AwsProvider#mediastore}
        '''
        result = self._values.get("mediastore")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memorydb(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#memorydb AwsProvider#memorydb}
        '''
        result = self._values.get("memorydb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mgn(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#mgn AwsProvider#mgn}
        '''
        result = self._values.get("mgn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mq(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#mq AwsProvider#mq}
        '''
        result = self._values.get("mq")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def msk(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#msk AwsProvider#msk}
        '''
        result = self._values.get("msk")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mwaa(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#mwaa AwsProvider#mwaa}
        '''
        result = self._values.get("mwaa")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def neptune(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#neptune AwsProvider#neptune}
        '''
        result = self._values.get("neptune")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def neptunegraph(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#neptunegraph AwsProvider#neptunegraph}
        '''
        result = self._values.get("neptunegraph")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def networkfirewall(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#networkfirewall AwsProvider#networkfirewall}
        '''
        result = self._values.get("networkfirewall")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def networkmanager(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#networkmanager AwsProvider#networkmanager}
        '''
        result = self._values.get("networkmanager")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def networkmonitor(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#networkmonitor AwsProvider#networkmonitor}
        '''
        result = self._values.get("networkmonitor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oam(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#oam AwsProvider#oam}
        '''
        result = self._values.get("oam")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def opensearch(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#opensearch AwsProvider#opensearch}
        '''
        result = self._values.get("opensearch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def opensearchingestion(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#opensearchingestion AwsProvider#opensearchingestion}
        '''
        result = self._values.get("opensearchingestion")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def opensearchserverless(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#opensearchserverless AwsProvider#opensearchserverless}
        '''
        result = self._values.get("opensearchserverless")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def opensearchservice(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#opensearchservice AwsProvider#opensearchservice}
        '''
        result = self._values.get("opensearchservice")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def opsworks(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#opsworks AwsProvider#opsworks}
        '''
        result = self._values.get("opsworks")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organizations(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#organizations AwsProvider#organizations}
        '''
        result = self._values.get("organizations")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def osis(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#osis AwsProvider#osis}
        '''
        result = self._values.get("osis")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outposts(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#outposts AwsProvider#outposts}
        '''
        result = self._values.get("outposts")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def paymentcryptography(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#paymentcryptography AwsProvider#paymentcryptography}
        '''
        result = self._values.get("paymentcryptography")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pcaconnectorad(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#pcaconnectorad AwsProvider#pcaconnectorad}
        '''
        result = self._values.get("pcaconnectorad")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pcs(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#pcs AwsProvider#pcs}
        '''
        result = self._values.get("pcs")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pinpoint(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#pinpoint AwsProvider#pinpoint}
        '''
        result = self._values.get("pinpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pinpointsmsvoicev2(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#pinpointsmsvoicev2 AwsProvider#pinpointsmsvoicev2}
        '''
        result = self._values.get("pinpointsmsvoicev2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pipes(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#pipes AwsProvider#pipes}
        '''
        result = self._values.get("pipes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def polly(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#polly AwsProvider#polly}
        '''
        result = self._values.get("polly")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pricing(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#pricing AwsProvider#pricing}
        '''
        result = self._values.get("pricing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prometheus(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#prometheus AwsProvider#prometheus}
        '''
        result = self._values.get("prometheus")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prometheusservice(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#prometheusservice AwsProvider#prometheusservice}
        '''
        result = self._values.get("prometheusservice")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def qbusiness(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#qbusiness AwsProvider#qbusiness}
        '''
        result = self._values.get("qbusiness")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def qldb(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#qldb AwsProvider#qldb}
        '''
        result = self._values.get("qldb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quicksight(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#quicksight AwsProvider#quicksight}
        '''
        result = self._values.get("quicksight")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ram(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ram AwsProvider#ram}
        '''
        result = self._values.get("ram")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rbin(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#rbin AwsProvider#rbin}
        '''
        result = self._values.get("rbin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rds(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#rds AwsProvider#rds}
        '''
        result = self._values.get("rds")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recyclebin(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#recyclebin AwsProvider#recyclebin}
        '''
        result = self._values.get("recyclebin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redshift(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#redshift AwsProvider#redshift}
        '''
        result = self._values.get("redshift")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redshiftdata(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#redshiftdata AwsProvider#redshiftdata}
        '''
        result = self._values.get("redshiftdata")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redshiftdataapiservice(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#redshiftdataapiservice AwsProvider#redshiftdataapiservice}
        '''
        result = self._values.get("redshiftdataapiservice")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redshiftserverless(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#redshiftserverless AwsProvider#redshiftserverless}
        '''
        result = self._values.get("redshiftserverless")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rekognition(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#rekognition AwsProvider#rekognition}
        '''
        result = self._values.get("rekognition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resiliencehub(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#resiliencehub AwsProvider#resiliencehub}
        '''
        result = self._values.get("resiliencehub")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resourceexplorer2(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#resourceexplorer2 AwsProvider#resourceexplorer2}
        '''
        result = self._values.get("resourceexplorer2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resourcegroups(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#resourcegroups AwsProvider#resourcegroups}
        '''
        result = self._values.get("resourcegroups")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resourcegroupstagging(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#resourcegroupstagging AwsProvider#resourcegroupstagging}
        '''
        result = self._values.get("resourcegroupstagging")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resourcegroupstaggingapi(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#resourcegroupstaggingapi AwsProvider#resourcegroupstaggingapi}
        '''
        result = self._values.get("resourcegroupstaggingapi")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rolesanywhere(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#rolesanywhere AwsProvider#rolesanywhere}
        '''
        result = self._values.get("rolesanywhere")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route53(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#route53 AwsProvider#route53}
        '''
        result = self._values.get("route53")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route53_domains(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#route53domains AwsProvider#route53domains}
        '''
        result = self._values.get("route53_domains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route53_profiles(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#route53profiles AwsProvider#route53profiles}
        '''
        result = self._values.get("route53_profiles")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route53_recoverycontrolconfig(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#route53recoverycontrolconfig AwsProvider#route53recoverycontrolconfig}
        '''
        result = self._values.get("route53_recoverycontrolconfig")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route53_recoveryreadiness(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#route53recoveryreadiness AwsProvider#route53recoveryreadiness}
        '''
        result = self._values.get("route53_recoveryreadiness")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route53_resolver(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#route53resolver AwsProvider#route53resolver}
        '''
        result = self._values.get("route53_resolver")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rum(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#rum AwsProvider#rum}
        '''
        result = self._values.get("rum")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#s3 AwsProvider#s3}
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_api(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#s3api AwsProvider#s3api}
        '''
        result = self._values.get("s3_api")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_control(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#s3control AwsProvider#s3control}
        '''
        result = self._values.get("s3_control")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_outposts(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#s3outposts AwsProvider#s3outposts}
        '''
        result = self._values.get("s3_outposts")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_tables(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#s3tables AwsProvider#s3tables}
        '''
        result = self._values.get("s3_tables")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#sagemaker AwsProvider#sagemaker}
        '''
        result = self._values.get("sagemaker")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheduler(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#scheduler AwsProvider#scheduler}
        '''
        result = self._values.get("scheduler")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schemas(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#schemas AwsProvider#schemas}
        '''
        result = self._values.get("schemas")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sdb(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#sdb AwsProvider#sdb}
        '''
        result = self._values.get("sdb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secretsmanager(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#secretsmanager AwsProvider#secretsmanager}
        '''
        result = self._values.get("secretsmanager")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def securityhub(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#securityhub AwsProvider#securityhub}
        '''
        result = self._values.get("securityhub")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def securitylake(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#securitylake AwsProvider#securitylake}
        '''
        result = self._values.get("securitylake")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serverlessapplicationrepository(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#serverlessapplicationrepository AwsProvider#serverlessapplicationrepository}
        '''
        result = self._values.get("serverlessapplicationrepository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serverlessapprepo(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#serverlessapprepo AwsProvider#serverlessapprepo}
        '''
        result = self._values.get("serverlessapprepo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serverlessrepo(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#serverlessrepo AwsProvider#serverlessrepo}
        '''
        result = self._values.get("serverlessrepo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def servicecatalog(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#servicecatalog AwsProvider#servicecatalog}
        '''
        result = self._values.get("servicecatalog")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def servicecatalogappregistry(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#servicecatalogappregistry AwsProvider#servicecatalogappregistry}
        '''
        result = self._values.get("servicecatalogappregistry")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def servicediscovery(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#servicediscovery AwsProvider#servicediscovery}
        '''
        result = self._values.get("servicediscovery")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def servicequotas(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#servicequotas AwsProvider#servicequotas}
        '''
        result = self._values.get("servicequotas")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ses(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ses AwsProvider#ses}
        '''
        result = self._values.get("ses")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sesv2(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#sesv2 AwsProvider#sesv2}
        '''
        result = self._values.get("sesv2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sfn(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#sfn AwsProvider#sfn}
        '''
        result = self._values.get("sfn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shield(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#shield AwsProvider#shield}
        '''
        result = self._values.get("shield")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signer(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#signer AwsProvider#signer}
        '''
        result = self._values.get("signer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def simpledb(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#simpledb AwsProvider#simpledb}
        '''
        result = self._values.get("simpledb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sns(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#sns AwsProvider#sns}
        '''
        result = self._values.get("sns")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sqs(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#sqs AwsProvider#sqs}
        '''
        result = self._values.get("sqs")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssm(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ssm AwsProvider#ssm}
        '''
        result = self._values.get("ssm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssmcontacts(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ssmcontacts AwsProvider#ssmcontacts}
        '''
        result = self._values.get("ssmcontacts")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssmincidents(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ssmincidents AwsProvider#ssmincidents}
        '''
        result = self._values.get("ssmincidents")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssmquicksetup(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ssmquicksetup AwsProvider#ssmquicksetup}
        '''
        result = self._values.get("ssmquicksetup")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssmsap(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ssmsap AwsProvider#ssmsap}
        '''
        result = self._values.get("ssmsap")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sso(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#sso AwsProvider#sso}
        '''
        result = self._values.get("sso")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssoadmin(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#ssoadmin AwsProvider#ssoadmin}
        '''
        result = self._values.get("ssoadmin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stepfunctions(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#stepfunctions AwsProvider#stepfunctions}
        '''
        result = self._values.get("stepfunctions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storagegateway(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#storagegateway AwsProvider#storagegateway}
        '''
        result = self._values.get("storagegateway")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sts(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#sts AwsProvider#sts}
        '''
        result = self._values.get("sts")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def swf(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#swf AwsProvider#swf}
        '''
        result = self._values.get("swf")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def synthetics(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#synthetics AwsProvider#synthetics}
        '''
        result = self._values.get("synthetics")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def taxsettings(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#taxsettings AwsProvider#taxsettings}
        '''
        result = self._values.get("taxsettings")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestreaminfluxdb(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#timestreaminfluxdb AwsProvider#timestreaminfluxdb}
        '''
        result = self._values.get("timestreaminfluxdb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestreamquery(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#timestreamquery AwsProvider#timestreamquery}
        '''
        result = self._values.get("timestreamquery")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestreamwrite(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#timestreamwrite AwsProvider#timestreamwrite}
        '''
        result = self._values.get("timestreamwrite")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transcribe(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#transcribe AwsProvider#transcribe}
        '''
        result = self._values.get("transcribe")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transcribeservice(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#transcribeservice AwsProvider#transcribeservice}
        '''
        result = self._values.get("transcribeservice")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transfer(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#transfer AwsProvider#transfer}
        '''
        result = self._values.get("transfer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verifiedpermissions(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#verifiedpermissions AwsProvider#verifiedpermissions}
        '''
        result = self._values.get("verifiedpermissions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpclattice(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#vpclattice AwsProvider#vpclattice}
        '''
        result = self._values.get("vpclattice")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def waf(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#waf AwsProvider#waf}
        '''
        result = self._values.get("waf")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wafregional(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#wafregional AwsProvider#wafregional}
        '''
        result = self._values.get("wafregional")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wafv2(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#wafv2 AwsProvider#wafv2}
        '''
        result = self._values.get("wafv2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wellarchitected(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#wellarchitected AwsProvider#wellarchitected}
        '''
        result = self._values.get("wellarchitected")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def worklink(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#worklink AwsProvider#worklink}
        '''
        result = self._values.get("worklink")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspaces(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#workspaces AwsProvider#workspaces}
        '''
        result = self._values.get("workspaces")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspacesweb(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#workspacesweb AwsProvider#workspacesweb}
        '''
        result = self._values.get("workspacesweb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def xray(self) -> typing.Optional[builtins.str]:
        '''Use this to override the default service endpoint URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#xray AwsProvider#xray}
        '''
        result = self._values.get("xray")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsProviderEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.provider.AwsProviderIgnoreTags",
    jsii_struct_bases=[],
    name_mapping={"key_prefixes": "keyPrefixes", "keys": "keys"},
)
class AwsProviderIgnoreTags:
    def __init__(
        self,
        *,
        key_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key_prefixes: Resource tag key prefixes to ignore across all resources. Can also be configured with the TF_AWS_IGNORE_TAGS_KEY_PREFIXES environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#key_prefixes AwsProvider#key_prefixes}
        :param keys: Resource tag keys to ignore across all resources. Can also be configured with the TF_AWS_IGNORE_TAGS_KEYS environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#keys AwsProvider#keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ab041190cff9dea0fa7e0b3c1dc38ef6ecad92f82f69388d0b2e9a3b135aa52)
            check_type(argname="argument key_prefixes", value=key_prefixes, expected_type=type_hints["key_prefixes"])
            check_type(argname="argument keys", value=keys, expected_type=type_hints["keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key_prefixes is not None:
            self._values["key_prefixes"] = key_prefixes
        if keys is not None:
            self._values["keys"] = keys

    @builtins.property
    def key_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Resource tag key prefixes to ignore across all resources. Can also be configured with the TF_AWS_IGNORE_TAGS_KEY_PREFIXES environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#key_prefixes AwsProvider#key_prefixes}
        '''
        result = self._values.get("key_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Resource tag keys to ignore across all resources. Can also be configured with the TF_AWS_IGNORE_TAGS_KEYS environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs#keys AwsProvider#keys}
        '''
        result = self._values.get("keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsProviderIgnoreTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsProvider",
    "AwsProviderAssumeRole",
    "AwsProviderAssumeRoleWithWebIdentity",
    "AwsProviderConfig",
    "AwsProviderDefaultTags",
    "AwsProviderEndpoints",
    "AwsProviderIgnoreTags",
]

publication.publish()

def _typecheckingstub__57740e84c090e6dbbe5013b04d4825b1e91195924e8b2a3215a201c1b6c1db94(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_key: typing.Optional[builtins.str] = None,
    alias: typing.Optional[builtins.str] = None,
    allowed_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    assume_role: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AwsProviderAssumeRole, typing.Dict[builtins.str, typing.Any]]]]] = None,
    assume_role_with_web_identity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AwsProviderAssumeRoleWithWebIdentity, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_ca_bundle: typing.Optional[builtins.str] = None,
    default_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AwsProviderDefaultTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ec2_metadata_service_endpoint: typing.Optional[builtins.str] = None,
    ec2_metadata_service_endpoint_mode: typing.Optional[builtins.str] = None,
    endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AwsProviderEndpoints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    forbidden_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    http_proxy: typing.Optional[builtins.str] = None,
    https_proxy: typing.Optional[builtins.str] = None,
    ignore_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AwsProviderIgnoreTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    no_proxy: typing.Optional[builtins.str] = None,
    profile: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    retry_mode: typing.Optional[builtins.str] = None,
    s3_us_east1_regional_endpoint: typing.Optional[builtins.str] = None,
    s3_use_path_style: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secret_key: typing.Optional[builtins.str] = None,
    shared_config_files: typing.Optional[typing.Sequence[builtins.str]] = None,
    shared_credentials_files: typing.Optional[typing.Sequence[builtins.str]] = None,
    skip_credentials_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_metadata_api_check: typing.Optional[builtins.str] = None,
    skip_region_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_requesting_account_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sts_region: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    token_bucket_rate_limiter_capacity: typing.Optional[jsii.Number] = None,
    use_dualstack_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_fips_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97e78c17cf7a315f66927ed4ef5a9f09ab06b83a94fb0847fa4ff1b7739c805b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f97caf30c4cf5d143ef30e715a281fe5c381f8cf27b32e70b7a2b1302ce9ff5b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80bc4aff31cfdf4f07483a4c8d21f0b0eaa38b8f34caf268f8927000ed57c646(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f91cb0e9acead45005abbe4dca4dbe00f3208583db5f83d19b04810a167964(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88a81471684ebb3aa894bba1ea2087f5c39224c89e73be35717bbf2ccc2c958(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AwsProviderAssumeRole]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d844f5622298fa89e8fae92c37ff32dfef0b12e23ea848b4ce5eb51a8620ef1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AwsProviderAssumeRoleWithWebIdentity]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1bd9f29fa431038e30d34bfb80ae9fa177daa980dc396c0088189d957ae7dba(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b993e01bdc539cfc190aee74f85d3362f7d07350b4eab2fc55a588e999bee2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AwsProviderDefaultTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eca099fd728ddcbbec4df07840db7fecd1c88cbc3c12f2f897a6025e1b660ff(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6dee424cdb153a32b34e98d3002fcac5cd19addc01eee013306179206b0a99f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9292ea3762e5c9b3e0beb785585e41485d8a33c9db5dce2b7e0296fc1a8f49b0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AwsProviderEndpoints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc9326a1717f217ef9b1645ad004cccb304224f730752a61a1f896444cf45ddf(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6f631015bc72081aa457cc57dfeb85ceb558a0e146df7fc77701a74122599d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12f28a6714d54dee0b149d57dc1bd4b07b2d055ba95dcb4cab6a510ee8e57670(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882b429a5604fb9e73677d843c115941f86b0b8871d5830fba8aa41437555217(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AwsProviderIgnoreTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad49c472700312804b8dd445cd2a191de2700777ae6f5fa260b1ed52a6b5599a(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaea293f15020e29fe5694012019b9e582971c4f3a5e0065e14c8eca9ae7046c(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7318c0da3dc9966e57d2b428a99e595a40962e0f406bf7b3a821f0c91d4e28a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d57fe9789911b3d82c8d661f330959d76ee2dc7869c1cb75b5898acdf94ed4a3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__486ee42567ffa21efb6d1b916f69581e45a9e0ff38292723c9b498fa98dda526(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f7e5f9072d44c6a1c54564b6843b0be4e07831bcfc5cac3a29ae58798d3fb64(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b2f848f06249f754ac63a17186248922a5145053012a5e1fd8b20fe1767f16(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac7770c17b68cc6a4e85c6fabe6315963a8ab254b42904391c9b1964f98d38a(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0460c2812f02da34e13a8964d21b5d351f0635480d9b4dce558c8aea77724db9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c60eecbf5578be99fd002ddbde2feddef3694af92d196eccb29433a6e983153a(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37bd9c05dcccbe57be6cacdad7a6c8380cba5a4c33868839bda7f47347b9d4c(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65219b90d8b6318afd7e39f491b2b8a793a7771d6c1ece83185513bd9d0f12d3(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aadf2f6ea203c5d94ac4f94eccee099c4748b449f24cc82cea9660b2b19ee15(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b32ce7eb1f5c845c19a0746b0149f5c906e1ce856471e9f80a9d148bcb90605(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf644a8308df17711c61e179978fbebba6266c3263e29c36275d80f944ace12(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf6f79c369d9fce42df29616927a4b96275f18adf0f5ad2b137078c93f5b831f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a333bb63ca035e85037d8113d29d49027dbe991c253604d7ad91f5a9c8a4684(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3095656322017f1dd9c0b5c48c0e69a22ee51fb0dc402203743a6d953f108a4c(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec35f69a49d58d30e4bb74a3b9f095c5c5e3ef3f164a3492b095215510b1eff2(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f442a7233365631a5f3a2908a1ad10a79fefcaf2c29b6b2a57e7faae8f9e0494(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e13c9cf89749eaaf5dd0a7fae994b4dd66132f149e51e34cc333614df59c7ace(
    *,
    duration: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
    policy: typing.Optional[builtins.str] = None,
    policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    session_name: typing.Optional[builtins.str] = None,
    source_identity: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    transitive_tag_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006dfde6bb37b5cb603bf04cf9efc9a9b9ccdaab3e3bf265876fbf07e7e867b3(
    *,
    duration: typing.Optional[builtins.str] = None,
    policy: typing.Optional[builtins.str] = None,
    policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    session_name: typing.Optional[builtins.str] = None,
    web_identity_token: typing.Optional[builtins.str] = None,
    web_identity_token_file: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c594a8866496614f028e2c928d60f10d6094c47bbfd585fb76f5f791591813c3(
    *,
    access_key: typing.Optional[builtins.str] = None,
    alias: typing.Optional[builtins.str] = None,
    allowed_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    assume_role: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AwsProviderAssumeRole, typing.Dict[builtins.str, typing.Any]]]]] = None,
    assume_role_with_web_identity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AwsProviderAssumeRoleWithWebIdentity, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_ca_bundle: typing.Optional[builtins.str] = None,
    default_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AwsProviderDefaultTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ec2_metadata_service_endpoint: typing.Optional[builtins.str] = None,
    ec2_metadata_service_endpoint_mode: typing.Optional[builtins.str] = None,
    endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AwsProviderEndpoints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    forbidden_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    http_proxy: typing.Optional[builtins.str] = None,
    https_proxy: typing.Optional[builtins.str] = None,
    ignore_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AwsProviderIgnoreTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    no_proxy: typing.Optional[builtins.str] = None,
    profile: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    retry_mode: typing.Optional[builtins.str] = None,
    s3_us_east1_regional_endpoint: typing.Optional[builtins.str] = None,
    s3_use_path_style: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secret_key: typing.Optional[builtins.str] = None,
    shared_config_files: typing.Optional[typing.Sequence[builtins.str]] = None,
    shared_credentials_files: typing.Optional[typing.Sequence[builtins.str]] = None,
    skip_credentials_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_metadata_api_check: typing.Optional[builtins.str] = None,
    skip_region_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_requesting_account_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sts_region: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    token_bucket_rate_limiter_capacity: typing.Optional[jsii.Number] = None,
    use_dualstack_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_fips_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eebaf0067d800334bb2e8f03568b545daa7ceaffca147b8eed6da77e27758b8d(
    *,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__912b8f0439a9c34ac3f441b30210524e0bb966c3363990a416d3e2f274939834(
    *,
    accessanalyzer: typing.Optional[builtins.str] = None,
    account: typing.Optional[builtins.str] = None,
    acm: typing.Optional[builtins.str] = None,
    acmpca: typing.Optional[builtins.str] = None,
    amg: typing.Optional[builtins.str] = None,
    amp: typing.Optional[builtins.str] = None,
    amplify: typing.Optional[builtins.str] = None,
    apigateway: typing.Optional[builtins.str] = None,
    apigatewayv2: typing.Optional[builtins.str] = None,
    appautoscaling: typing.Optional[builtins.str] = None,
    appconfig: typing.Optional[builtins.str] = None,
    appfabric: typing.Optional[builtins.str] = None,
    appflow: typing.Optional[builtins.str] = None,
    appintegrations: typing.Optional[builtins.str] = None,
    appintegrationsservice: typing.Optional[builtins.str] = None,
    applicationautoscaling: typing.Optional[builtins.str] = None,
    applicationinsights: typing.Optional[builtins.str] = None,
    applicationsignals: typing.Optional[builtins.str] = None,
    appmesh: typing.Optional[builtins.str] = None,
    appregistry: typing.Optional[builtins.str] = None,
    apprunner: typing.Optional[builtins.str] = None,
    appstream: typing.Optional[builtins.str] = None,
    appsync: typing.Optional[builtins.str] = None,
    athena: typing.Optional[builtins.str] = None,
    auditmanager: typing.Optional[builtins.str] = None,
    autoscaling: typing.Optional[builtins.str] = None,
    autoscalingplans: typing.Optional[builtins.str] = None,
    backup: typing.Optional[builtins.str] = None,
    batch: typing.Optional[builtins.str] = None,
    bcmdataexports: typing.Optional[builtins.str] = None,
    beanstalk: typing.Optional[builtins.str] = None,
    bedrock: typing.Optional[builtins.str] = None,
    bedrockagent: typing.Optional[builtins.str] = None,
    billing: typing.Optional[builtins.str] = None,
    budgets: typing.Optional[builtins.str] = None,
    ce: typing.Optional[builtins.str] = None,
    chatbot: typing.Optional[builtins.str] = None,
    chime: typing.Optional[builtins.str] = None,
    chimesdkmediapipelines: typing.Optional[builtins.str] = None,
    chimesdkvoice: typing.Optional[builtins.str] = None,
    cleanrooms: typing.Optional[builtins.str] = None,
    cloud9: typing.Optional[builtins.str] = None,
    cloudcontrol: typing.Optional[builtins.str] = None,
    cloudcontrolapi: typing.Optional[builtins.str] = None,
    cloudformation: typing.Optional[builtins.str] = None,
    cloudfront: typing.Optional[builtins.str] = None,
    cloudfrontkeyvaluestore: typing.Optional[builtins.str] = None,
    cloudhsm: typing.Optional[builtins.str] = None,
    cloudhsmv2: typing.Optional[builtins.str] = None,
    cloudsearch: typing.Optional[builtins.str] = None,
    cloudtrail: typing.Optional[builtins.str] = None,
    cloudwatch: typing.Optional[builtins.str] = None,
    cloudwatchevents: typing.Optional[builtins.str] = None,
    cloudwatchevidently: typing.Optional[builtins.str] = None,
    cloudwatchlog: typing.Optional[builtins.str] = None,
    cloudwatchlogs: typing.Optional[builtins.str] = None,
    cloudwatchobservabilityaccessmanager: typing.Optional[builtins.str] = None,
    cloudwatchrum: typing.Optional[builtins.str] = None,
    codeartifact: typing.Optional[builtins.str] = None,
    codebuild: typing.Optional[builtins.str] = None,
    codecatalyst: typing.Optional[builtins.str] = None,
    codecommit: typing.Optional[builtins.str] = None,
    codeconnections: typing.Optional[builtins.str] = None,
    codedeploy: typing.Optional[builtins.str] = None,
    codeguruprofiler: typing.Optional[builtins.str] = None,
    codegurureviewer: typing.Optional[builtins.str] = None,
    codepipeline: typing.Optional[builtins.str] = None,
    codestarconnections: typing.Optional[builtins.str] = None,
    codestarnotifications: typing.Optional[builtins.str] = None,
    cognitoidentity: typing.Optional[builtins.str] = None,
    cognitoidentityprovider: typing.Optional[builtins.str] = None,
    cognitoidp: typing.Optional[builtins.str] = None,
    comprehend: typing.Optional[builtins.str] = None,
    computeoptimizer: typing.Optional[builtins.str] = None,
    config: typing.Optional[builtins.str] = None,
    configservice: typing.Optional[builtins.str] = None,
    connect: typing.Optional[builtins.str] = None,
    connectcases: typing.Optional[builtins.str] = None,
    controltower: typing.Optional[builtins.str] = None,
    costandusagereportservice: typing.Optional[builtins.str] = None,
    costexplorer: typing.Optional[builtins.str] = None,
    costoptimizationhub: typing.Optional[builtins.str] = None,
    cur: typing.Optional[builtins.str] = None,
    customerprofiles: typing.Optional[builtins.str] = None,
    databasemigration: typing.Optional[builtins.str] = None,
    databasemigrationservice: typing.Optional[builtins.str] = None,
    databrew: typing.Optional[builtins.str] = None,
    dataexchange: typing.Optional[builtins.str] = None,
    datapipeline: typing.Optional[builtins.str] = None,
    datasync: typing.Optional[builtins.str] = None,
    datazone: typing.Optional[builtins.str] = None,
    dax: typing.Optional[builtins.str] = None,
    deploy: typing.Optional[builtins.str] = None,
    detective: typing.Optional[builtins.str] = None,
    devicefarm: typing.Optional[builtins.str] = None,
    devopsguru: typing.Optional[builtins.str] = None,
    directconnect: typing.Optional[builtins.str] = None,
    directoryservice: typing.Optional[builtins.str] = None,
    dlm: typing.Optional[builtins.str] = None,
    dms: typing.Optional[builtins.str] = None,
    docdb: typing.Optional[builtins.str] = None,
    docdbelastic: typing.Optional[builtins.str] = None,
    drs: typing.Optional[builtins.str] = None,
    ds: typing.Optional[builtins.str] = None,
    dsql: typing.Optional[builtins.str] = None,
    dynamodb: typing.Optional[builtins.str] = None,
    ec2: typing.Optional[builtins.str] = None,
    ecr: typing.Optional[builtins.str] = None,
    ecrpublic: typing.Optional[builtins.str] = None,
    ecs: typing.Optional[builtins.str] = None,
    efs: typing.Optional[builtins.str] = None,
    eks: typing.Optional[builtins.str] = None,
    elasticache: typing.Optional[builtins.str] = None,
    elasticbeanstalk: typing.Optional[builtins.str] = None,
    elasticloadbalancing: typing.Optional[builtins.str] = None,
    elasticloadbalancingv2: typing.Optional[builtins.str] = None,
    elasticsearch: typing.Optional[builtins.str] = None,
    elasticsearchservice: typing.Optional[builtins.str] = None,
    elastictranscoder: typing.Optional[builtins.str] = None,
    elb: typing.Optional[builtins.str] = None,
    elbv2: typing.Optional[builtins.str] = None,
    emr: typing.Optional[builtins.str] = None,
    emrcontainers: typing.Optional[builtins.str] = None,
    emrserverless: typing.Optional[builtins.str] = None,
    es: typing.Optional[builtins.str] = None,
    eventbridge: typing.Optional[builtins.str] = None,
    events: typing.Optional[builtins.str] = None,
    evidently: typing.Optional[builtins.str] = None,
    finspace: typing.Optional[builtins.str] = None,
    firehose: typing.Optional[builtins.str] = None,
    fis: typing.Optional[builtins.str] = None,
    fms: typing.Optional[builtins.str] = None,
    fsx: typing.Optional[builtins.str] = None,
    gamelift: typing.Optional[builtins.str] = None,
    glacier: typing.Optional[builtins.str] = None,
    globalaccelerator: typing.Optional[builtins.str] = None,
    glue: typing.Optional[builtins.str] = None,
    gluedatabrew: typing.Optional[builtins.str] = None,
    grafana: typing.Optional[builtins.str] = None,
    greengrass: typing.Optional[builtins.str] = None,
    groundstation: typing.Optional[builtins.str] = None,
    guardduty: typing.Optional[builtins.str] = None,
    healthlake: typing.Optional[builtins.str] = None,
    iam: typing.Optional[builtins.str] = None,
    identitystore: typing.Optional[builtins.str] = None,
    imagebuilder: typing.Optional[builtins.str] = None,
    inspector: typing.Optional[builtins.str] = None,
    inspector2: typing.Optional[builtins.str] = None,
    inspectorv2: typing.Optional[builtins.str] = None,
    internetmonitor: typing.Optional[builtins.str] = None,
    invoicing: typing.Optional[builtins.str] = None,
    iot: typing.Optional[builtins.str] = None,
    iotanalytics: typing.Optional[builtins.str] = None,
    iotevents: typing.Optional[builtins.str] = None,
    ivs: typing.Optional[builtins.str] = None,
    ivschat: typing.Optional[builtins.str] = None,
    kafka: typing.Optional[builtins.str] = None,
    kafkaconnect: typing.Optional[builtins.str] = None,
    kendra: typing.Optional[builtins.str] = None,
    keyspaces: typing.Optional[builtins.str] = None,
    kinesis: typing.Optional[builtins.str] = None,
    kinesisanalytics: typing.Optional[builtins.str] = None,
    kinesisanalyticsv2: typing.Optional[builtins.str] = None,
    kinesisvideo: typing.Optional[builtins.str] = None,
    kms: typing.Optional[builtins.str] = None,
    lakeformation: typing.Optional[builtins.str] = None,
    lambda_: typing.Optional[builtins.str] = None,
    launchwizard: typing.Optional[builtins.str] = None,
    lex: typing.Optional[builtins.str] = None,
    lexmodelbuilding: typing.Optional[builtins.str] = None,
    lexmodelbuildingservice: typing.Optional[builtins.str] = None,
    lexmodels: typing.Optional[builtins.str] = None,
    lexmodelsv2: typing.Optional[builtins.str] = None,
    lexv2_models: typing.Optional[builtins.str] = None,
    licensemanager: typing.Optional[builtins.str] = None,
    lightsail: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    locationservice: typing.Optional[builtins.str] = None,
    logs: typing.Optional[builtins.str] = None,
    lookoutmetrics: typing.Optional[builtins.str] = None,
    m2: typing.Optional[builtins.str] = None,
    macie2: typing.Optional[builtins.str] = None,
    managedgrafana: typing.Optional[builtins.str] = None,
    mediaconnect: typing.Optional[builtins.str] = None,
    mediaconvert: typing.Optional[builtins.str] = None,
    medialive: typing.Optional[builtins.str] = None,
    mediapackage: typing.Optional[builtins.str] = None,
    mediapackagev2: typing.Optional[builtins.str] = None,
    mediapackagevod: typing.Optional[builtins.str] = None,
    mediastore: typing.Optional[builtins.str] = None,
    memorydb: typing.Optional[builtins.str] = None,
    mgn: typing.Optional[builtins.str] = None,
    mq: typing.Optional[builtins.str] = None,
    msk: typing.Optional[builtins.str] = None,
    mwaa: typing.Optional[builtins.str] = None,
    neptune: typing.Optional[builtins.str] = None,
    neptunegraph: typing.Optional[builtins.str] = None,
    networkfirewall: typing.Optional[builtins.str] = None,
    networkmanager: typing.Optional[builtins.str] = None,
    networkmonitor: typing.Optional[builtins.str] = None,
    oam: typing.Optional[builtins.str] = None,
    opensearch: typing.Optional[builtins.str] = None,
    opensearchingestion: typing.Optional[builtins.str] = None,
    opensearchserverless: typing.Optional[builtins.str] = None,
    opensearchservice: typing.Optional[builtins.str] = None,
    opsworks: typing.Optional[builtins.str] = None,
    organizations: typing.Optional[builtins.str] = None,
    osis: typing.Optional[builtins.str] = None,
    outposts: typing.Optional[builtins.str] = None,
    paymentcryptography: typing.Optional[builtins.str] = None,
    pcaconnectorad: typing.Optional[builtins.str] = None,
    pcs: typing.Optional[builtins.str] = None,
    pinpoint: typing.Optional[builtins.str] = None,
    pinpointsmsvoicev2: typing.Optional[builtins.str] = None,
    pipes: typing.Optional[builtins.str] = None,
    polly: typing.Optional[builtins.str] = None,
    pricing: typing.Optional[builtins.str] = None,
    prometheus: typing.Optional[builtins.str] = None,
    prometheusservice: typing.Optional[builtins.str] = None,
    qbusiness: typing.Optional[builtins.str] = None,
    qldb: typing.Optional[builtins.str] = None,
    quicksight: typing.Optional[builtins.str] = None,
    ram: typing.Optional[builtins.str] = None,
    rbin: typing.Optional[builtins.str] = None,
    rds: typing.Optional[builtins.str] = None,
    recyclebin: typing.Optional[builtins.str] = None,
    redshift: typing.Optional[builtins.str] = None,
    redshiftdata: typing.Optional[builtins.str] = None,
    redshiftdataapiservice: typing.Optional[builtins.str] = None,
    redshiftserverless: typing.Optional[builtins.str] = None,
    rekognition: typing.Optional[builtins.str] = None,
    resiliencehub: typing.Optional[builtins.str] = None,
    resourceexplorer2: typing.Optional[builtins.str] = None,
    resourcegroups: typing.Optional[builtins.str] = None,
    resourcegroupstagging: typing.Optional[builtins.str] = None,
    resourcegroupstaggingapi: typing.Optional[builtins.str] = None,
    rolesanywhere: typing.Optional[builtins.str] = None,
    route53: typing.Optional[builtins.str] = None,
    route53_domains: typing.Optional[builtins.str] = None,
    route53_profiles: typing.Optional[builtins.str] = None,
    route53_recoverycontrolconfig: typing.Optional[builtins.str] = None,
    route53_recoveryreadiness: typing.Optional[builtins.str] = None,
    route53_resolver: typing.Optional[builtins.str] = None,
    rum: typing.Optional[builtins.str] = None,
    s3: typing.Optional[builtins.str] = None,
    s3_api: typing.Optional[builtins.str] = None,
    s3_control: typing.Optional[builtins.str] = None,
    s3_outposts: typing.Optional[builtins.str] = None,
    s3_tables: typing.Optional[builtins.str] = None,
    sagemaker: typing.Optional[builtins.str] = None,
    scheduler: typing.Optional[builtins.str] = None,
    schemas: typing.Optional[builtins.str] = None,
    sdb: typing.Optional[builtins.str] = None,
    secretsmanager: typing.Optional[builtins.str] = None,
    securityhub: typing.Optional[builtins.str] = None,
    securitylake: typing.Optional[builtins.str] = None,
    serverlessapplicationrepository: typing.Optional[builtins.str] = None,
    serverlessapprepo: typing.Optional[builtins.str] = None,
    serverlessrepo: typing.Optional[builtins.str] = None,
    servicecatalog: typing.Optional[builtins.str] = None,
    servicecatalogappregistry: typing.Optional[builtins.str] = None,
    servicediscovery: typing.Optional[builtins.str] = None,
    servicequotas: typing.Optional[builtins.str] = None,
    ses: typing.Optional[builtins.str] = None,
    sesv2: typing.Optional[builtins.str] = None,
    sfn: typing.Optional[builtins.str] = None,
    shield: typing.Optional[builtins.str] = None,
    signer: typing.Optional[builtins.str] = None,
    simpledb: typing.Optional[builtins.str] = None,
    sns: typing.Optional[builtins.str] = None,
    sqs: typing.Optional[builtins.str] = None,
    ssm: typing.Optional[builtins.str] = None,
    ssmcontacts: typing.Optional[builtins.str] = None,
    ssmincidents: typing.Optional[builtins.str] = None,
    ssmquicksetup: typing.Optional[builtins.str] = None,
    ssmsap: typing.Optional[builtins.str] = None,
    sso: typing.Optional[builtins.str] = None,
    ssoadmin: typing.Optional[builtins.str] = None,
    stepfunctions: typing.Optional[builtins.str] = None,
    storagegateway: typing.Optional[builtins.str] = None,
    sts: typing.Optional[builtins.str] = None,
    swf: typing.Optional[builtins.str] = None,
    synthetics: typing.Optional[builtins.str] = None,
    taxsettings: typing.Optional[builtins.str] = None,
    timestreaminfluxdb: typing.Optional[builtins.str] = None,
    timestreamquery: typing.Optional[builtins.str] = None,
    timestreamwrite: typing.Optional[builtins.str] = None,
    transcribe: typing.Optional[builtins.str] = None,
    transcribeservice: typing.Optional[builtins.str] = None,
    transfer: typing.Optional[builtins.str] = None,
    verifiedpermissions: typing.Optional[builtins.str] = None,
    vpclattice: typing.Optional[builtins.str] = None,
    waf: typing.Optional[builtins.str] = None,
    wafregional: typing.Optional[builtins.str] = None,
    wafv2: typing.Optional[builtins.str] = None,
    wellarchitected: typing.Optional[builtins.str] = None,
    worklink: typing.Optional[builtins.str] = None,
    workspaces: typing.Optional[builtins.str] = None,
    workspacesweb: typing.Optional[builtins.str] = None,
    xray: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ab041190cff9dea0fa7e0b3c1dc38ef6ecad92f82f69388d0b2e9a3b135aa52(
    *,
    key_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
