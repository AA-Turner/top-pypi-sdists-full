r'''
# `provider`

Refer to the Terraform Registry for docs: [`opentelekomcloud`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs).
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


class OpentelekomcloudProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.provider.OpentelekomcloudProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs opentelekomcloud}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_key: typing.Optional[builtins.str] = None,
        agency_domain_name: typing.Optional[builtins.str] = None,
        agency_name: typing.Optional[builtins.str] = None,
        alias: typing.Optional[builtins.str] = None,
        allow_reauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auth_url: typing.Optional[builtins.str] = None,
        backoff_retry_timeout: typing.Optional[jsii.Number] = None,
        cacert_file: typing.Optional[builtins.str] = None,
        cert: typing.Optional[builtins.str] = None,
        cloud: typing.Optional[builtins.str] = None,
        delegated_project: typing.Optional[builtins.str] = None,
        domain_id: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        endpoint_type: typing.Optional[builtins.str] = None,
        insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key: typing.Optional[builtins.str] = None,
        max_backoff_retries: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        passcode: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        security_token: typing.Optional[builtins.str] = None,
        swauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        tenant_name: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        user_id: typing.Optional[builtins.str] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs opentelekomcloud} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param access_key: The access key for API operations. You can retrieve this from the 'My Credential' section of the console. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#access_key OpentelekomcloudProvider#access_key}
        :param agency_domain_name: The name of domain who created the agency (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#agency_domain_name OpentelekomcloudProvider#agency_domain_name}
        :param agency_name: The name of agency. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#agency_name OpentelekomcloudProvider#agency_name}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#alias OpentelekomcloudProvider#alias}
        :param allow_reauth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#allow_reauth OpentelekomcloudProvider#allow_reauth}.
        :param auth_url: The Identity authentication URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#auth_url OpentelekomcloudProvider#auth_url}
        :param backoff_retry_timeout: Timeout in seconds for backoff retry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#backoff_retry_timeout OpentelekomcloudProvider#backoff_retry_timeout}
        :param cacert_file: A Custom CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#cacert_file OpentelekomcloudProvider#cacert_file}
        :param cert: A client certificate to authenticate with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#cert OpentelekomcloudProvider#cert}
        :param cloud: An entry in a ``clouds.yaml`` file to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#cloud OpentelekomcloudProvider#cloud}
        :param delegated_project: The name of delegated project (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#delegated_project OpentelekomcloudProvider#delegated_project}
        :param domain_id: The ID of the Domain to scope to (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#domain_id OpentelekomcloudProvider#domain_id}
        :param domain_name: The name of the Domain to scope to (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#domain_name OpentelekomcloudProvider#domain_name}
        :param endpoint_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#endpoint_type OpentelekomcloudProvider#endpoint_type}.
        :param insecure: Trust self-signed certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#insecure OpentelekomcloudProvider#insecure}
        :param key: A client private key to authenticate with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#key OpentelekomcloudProvider#key}
        :param max_backoff_retries: How many times HTTP request should be retried when rate limit reached. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#max_backoff_retries OpentelekomcloudProvider#max_backoff_retries}
        :param max_retries: How many times HTTP connection should be retried until giving up. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#max_retries OpentelekomcloudProvider#max_retries}
        :param passcode: One-time MFA passcode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#passcode OpentelekomcloudProvider#passcode}
        :param password: Password to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#password OpentelekomcloudProvider#password}
        :param region: The OpenTelekomCloud region to connect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#region OpentelekomcloudProvider#region}
        :param secret_key: The secret key for API operations. You can retrieve this from the 'My Credential' section of the console. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#secret_key OpentelekomcloudProvider#secret_key}
        :param security_token: Security token to use for OBS federated authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#security_token OpentelekomcloudProvider#security_token}
        :param swauth: Use Swift's authentication system instead of Keystone. Only used for interaction with Swift. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#swauth OpentelekomcloudProvider#swauth}
        :param tenant_id: The ID of the Tenant (Identity v2) or Project (Identity v3) to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#tenant_id OpentelekomcloudProvider#tenant_id}
        :param tenant_name: The name of the Tenant (Identity v2) or Project (Identity v3) to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#tenant_name OpentelekomcloudProvider#tenant_name}
        :param token: Authentication token to use as an alternative to username/password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#token OpentelekomcloudProvider#token}
        :param user_id: User ID to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#user_id OpentelekomcloudProvider#user_id}
        :param user_name: Username to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#user_name OpentelekomcloudProvider#user_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f19b09b6a4b958a59149fefac7a07c00625b0a23b7c2ad34bbc3b21fa8d278ec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = OpentelekomcloudProviderConfig(
            access_key=access_key,
            agency_domain_name=agency_domain_name,
            agency_name=agency_name,
            alias=alias,
            allow_reauth=allow_reauth,
            auth_url=auth_url,
            backoff_retry_timeout=backoff_retry_timeout,
            cacert_file=cacert_file,
            cert=cert,
            cloud=cloud,
            delegated_project=delegated_project,
            domain_id=domain_id,
            domain_name=domain_name,
            endpoint_type=endpoint_type,
            insecure=insecure,
            key=key,
            max_backoff_retries=max_backoff_retries,
            max_retries=max_retries,
            passcode=passcode,
            password=password,
            region=region,
            secret_key=secret_key,
            security_token=security_token,
            swauth=swauth,
            tenant_id=tenant_id,
            tenant_name=tenant_name,
            token=token,
            user_id=user_id,
            user_name=user_name,
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
        '''Generates CDKTF code for importing a OpentelekomcloudProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OpentelekomcloudProvider to import.
        :param import_from_id: The id of the existing OpentelekomcloudProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OpentelekomcloudProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf9e726e08667ae4c2aa8d4ba55e042303b0f178f069ab0737f59b1c830cc695)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAccessKey")
    def reset_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessKey", []))

    @jsii.member(jsii_name="resetAgencyDomainName")
    def reset_agency_domain_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgencyDomainName", []))

    @jsii.member(jsii_name="resetAgencyName")
    def reset_agency_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgencyName", []))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetAllowReauth")
    def reset_allow_reauth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowReauth", []))

    @jsii.member(jsii_name="resetAuthUrl")
    def reset_auth_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthUrl", []))

    @jsii.member(jsii_name="resetBackoffRetryTimeout")
    def reset_backoff_retry_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackoffRetryTimeout", []))

    @jsii.member(jsii_name="resetCacertFile")
    def reset_cacert_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacertFile", []))

    @jsii.member(jsii_name="resetCert")
    def reset_cert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCert", []))

    @jsii.member(jsii_name="resetCloud")
    def reset_cloud(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloud", []))

    @jsii.member(jsii_name="resetDelegatedProject")
    def reset_delegated_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelegatedProject", []))

    @jsii.member(jsii_name="resetDomainId")
    def reset_domain_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainId", []))

    @jsii.member(jsii_name="resetDomainName")
    def reset_domain_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainName", []))

    @jsii.member(jsii_name="resetEndpointType")
    def reset_endpoint_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointType", []))

    @jsii.member(jsii_name="resetInsecure")
    def reset_insecure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecure", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetMaxBackoffRetries")
    def reset_max_backoff_retries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxBackoffRetries", []))

    @jsii.member(jsii_name="resetMaxRetries")
    def reset_max_retries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRetries", []))

    @jsii.member(jsii_name="resetPasscode")
    def reset_passcode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasscode", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSecretKey")
    def reset_secret_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretKey", []))

    @jsii.member(jsii_name="resetSecurityToken")
    def reset_security_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityToken", []))

    @jsii.member(jsii_name="resetSwauth")
    def reset_swauth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSwauth", []))

    @jsii.member(jsii_name="resetTenantId")
    def reset_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantId", []))

    @jsii.member(jsii_name="resetTenantName")
    def reset_tenant_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantName", []))

    @jsii.member(jsii_name="resetToken")
    def reset_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToken", []))

    @jsii.member(jsii_name="resetUserId")
    def reset_user_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserId", []))

    @jsii.member(jsii_name="resetUserName")
    def reset_user_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserName", []))

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
    @jsii.member(jsii_name="agencyDomainNameInput")
    def agency_domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agencyDomainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="agencyNameInput")
    def agency_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agencyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="allowReauthInput")
    def allow_reauth_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowReauthInput"))

    @builtins.property
    @jsii.member(jsii_name="authUrlInput")
    def auth_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="backoffRetryTimeoutInput")
    def backoff_retry_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backoffRetryTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="cacertFileInput")
    def cacert_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacertFileInput"))

    @builtins.property
    @jsii.member(jsii_name="certInput")
    def cert_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudInput")
    def cloud_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudInput"))

    @builtins.property
    @jsii.member(jsii_name="delegatedProjectInput")
    def delegated_project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delegatedProjectInput"))

    @builtins.property
    @jsii.member(jsii_name="domainIdInput")
    def domain_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainIdInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointTypeInput")
    def endpoint_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureInput")
    def insecure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="maxBackoffRetriesInput")
    def max_backoff_retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxBackoffRetriesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetriesInput")
    def max_retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetriesInput"))

    @builtins.property
    @jsii.member(jsii_name="passcodeInput")
    def passcode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passcodeInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretKeyInput")
    def secret_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="securityTokenInput")
    def security_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="swauthInput")
    def swauth_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "swauthInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantNameInput")
    def tenant_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property
    @jsii.member(jsii_name="userIdInput")
    def user_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameInput")
    def user_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKey")
    def access_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKey"))

    @access_key.setter
    def access_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3172b590a5b9bdfb2dc036a4707953c9b163f5bd15562d4ff5ae45e98b7f5020)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="agencyDomainName")
    def agency_domain_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agencyDomainName"))

    @agency_domain_name.setter
    def agency_domain_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c4bcac68a338e57ea0829c716ce01840cc5fe52bb2c40664f1ab78ca06748ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agencyDomainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="agencyName")
    def agency_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agencyName"))

    @agency_name.setter
    def agency_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95799e02207dcfe0156e5a0d09c5fa444c0796876e26a08e6b661ee1f76b1e11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agencyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a8c8a0f937546f5fa90203ea8bae720fbdf9eb46d8f309497e355dcb1beb230)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowReauth")
    def allow_reauth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowReauth"))

    @allow_reauth.setter
    def allow_reauth(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af0af7f726c5c28ba0a4275949289839ff18e3943fccadac132cdfdd50287c10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowReauth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authUrl")
    def auth_url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authUrl"))

    @auth_url.setter
    def auth_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2bb961cf0d47c6cb580701fa6b0de11e1667273bb4e8120bb2c84568c4e4784)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backoffRetryTimeout")
    def backoff_retry_timeout(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backoffRetryTimeout"))

    @backoff_retry_timeout.setter
    def backoff_retry_timeout(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c199e6a45c567b94962a41f5a6f4c5a77838eeec89833e3d3c2f5b2f13147553)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backoffRetryTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cacertFile")
    def cacert_file(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacertFile"))

    @cacert_file.setter
    def cacert_file(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf6a505fa8ae233bc84d147c35d3dee4b0bc3bf559c82cfae5ac49e1708e9677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacertFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cert")
    def cert(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cert"))

    @cert.setter
    def cert(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f5ff2cfd114ed2f88d1ba2099cb2c05fb07d13500a43ffb9b2eab790091e5e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloud")
    def cloud(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloud"))

    @cloud.setter
    def cloud(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__887c36f38e927f27bf0474b7af1b563cba26d72d6245697f9d85880c3d402108)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloud", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delegatedProject")
    def delegated_project(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delegatedProject"))

    @delegated_project.setter
    def delegated_project(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fc16d5debce0a8860c78d09b2ee74851127d931ab5b829d9dd06a0526adc65a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delegatedProject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainId"))

    @domain_id.setter
    def domain_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ac7032fce22b9414a16c00018ced13508f86dd0c9b6d755596b16463a9e9265)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abf12410dca374ab29fc50b310bc5f14b54e76b5e77c1f7b51a01e5b1c432ceb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpointType")
    def endpoint_type(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointType"))

    @endpoint_type.setter
    def endpoint_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce29fadc76cb1a45509d361ed2c62ebc36bc5e03c35770c687952cd6148d1aa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointType", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__1b2be7d37dab8ecf05256fdb769c99b53544f669aae7b1d1f574d9b83e549c29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "key"))

    @key.setter
    def key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6565f9d9010bc716fdf441d19efefff3442b9a52f4a4bf9a997eed9d10689d87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxBackoffRetries")
    def max_backoff_retries(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxBackoffRetries"))

    @max_backoff_retries.setter
    def max_backoff_retries(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__708bd769831a36616e62db2c336cb222f8a77a503ae1141dd45a83fa2a827ea7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxBackoffRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetries"))

    @max_retries.setter
    def max_retries(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60785e85ad8faa17e399c9893716fe684769b926cb6307ce8891b9dfe715a529)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passcode")
    def passcode(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passcode"))

    @passcode.setter
    def passcode(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0cb20997394429b9a9145a69d98d46e3593cc22dfa18caf88b147b2f3cdda31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passcode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "password"))

    @password.setter
    def password(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fed9306fcc7952f4cacef6c3a407dd576c14b1bbced31b599a3e2c83c1b4d68a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))

    @region.setter
    def region(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fc5ae1aea312df8541adca0cbbcdec6ba821883b6d276bdbd8a3f951b33888c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretKey")
    def secret_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretKey"))

    @secret_key.setter
    def secret_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4cfe001cf9502f21be91992d0309a5a6355d0b25a23fe010058991ef1b9f37e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityToken")
    def security_token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityToken"))

    @security_token.setter
    def security_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb22454f3f549ad2f7c8f45ae2e24d5f3fac2ab080a2fdd8d701c72889820263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="swauth")
    def swauth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "swauth"))

    @swauth.setter
    def swauth(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3707224789c866f47aa60215b768b0027c03dbbe69c982a7af889c5ca0b6f34f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "swauth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e45fe59e51c12e62c10a6d5ee5cd55355079296744d28ad14824f8a40b193d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantName")
    def tenant_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantName"))

    @tenant_name.setter
    def tenant_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c68974106bdca0c35cee773caece0edf2b881c8ed00ac1de3e7e70445b608268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "token"))

    @token.setter
    def token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6cac84878a9f7cd18f6834ff48b37f72ef981b8715f3d39186d278f86ada0d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "token", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userId"))

    @user_id.setter
    def user_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff1cc6a67d7d548fe3d339a7a7d19bfdf8160980ea750ac1a9dc8697535b29fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60774c8a815da1e9cc9a7d4a34a6bb4cd77fef07a42636980108155af8ec65e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.provider.OpentelekomcloudProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "access_key": "accessKey",
        "agency_domain_name": "agencyDomainName",
        "agency_name": "agencyName",
        "alias": "alias",
        "allow_reauth": "allowReauth",
        "auth_url": "authUrl",
        "backoff_retry_timeout": "backoffRetryTimeout",
        "cacert_file": "cacertFile",
        "cert": "cert",
        "cloud": "cloud",
        "delegated_project": "delegatedProject",
        "domain_id": "domainId",
        "domain_name": "domainName",
        "endpoint_type": "endpointType",
        "insecure": "insecure",
        "key": "key",
        "max_backoff_retries": "maxBackoffRetries",
        "max_retries": "maxRetries",
        "passcode": "passcode",
        "password": "password",
        "region": "region",
        "secret_key": "secretKey",
        "security_token": "securityToken",
        "swauth": "swauth",
        "tenant_id": "tenantId",
        "tenant_name": "tenantName",
        "token": "token",
        "user_id": "userId",
        "user_name": "userName",
    },
)
class OpentelekomcloudProviderConfig:
    def __init__(
        self,
        *,
        access_key: typing.Optional[builtins.str] = None,
        agency_domain_name: typing.Optional[builtins.str] = None,
        agency_name: typing.Optional[builtins.str] = None,
        alias: typing.Optional[builtins.str] = None,
        allow_reauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auth_url: typing.Optional[builtins.str] = None,
        backoff_retry_timeout: typing.Optional[jsii.Number] = None,
        cacert_file: typing.Optional[builtins.str] = None,
        cert: typing.Optional[builtins.str] = None,
        cloud: typing.Optional[builtins.str] = None,
        delegated_project: typing.Optional[builtins.str] = None,
        domain_id: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        endpoint_type: typing.Optional[builtins.str] = None,
        insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key: typing.Optional[builtins.str] = None,
        max_backoff_retries: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        passcode: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        security_token: typing.Optional[builtins.str] = None,
        swauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        tenant_name: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        user_id: typing.Optional[builtins.str] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_key: The access key for API operations. You can retrieve this from the 'My Credential' section of the console. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#access_key OpentelekomcloudProvider#access_key}
        :param agency_domain_name: The name of domain who created the agency (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#agency_domain_name OpentelekomcloudProvider#agency_domain_name}
        :param agency_name: The name of agency. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#agency_name OpentelekomcloudProvider#agency_name}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#alias OpentelekomcloudProvider#alias}
        :param allow_reauth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#allow_reauth OpentelekomcloudProvider#allow_reauth}.
        :param auth_url: The Identity authentication URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#auth_url OpentelekomcloudProvider#auth_url}
        :param backoff_retry_timeout: Timeout in seconds for backoff retry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#backoff_retry_timeout OpentelekomcloudProvider#backoff_retry_timeout}
        :param cacert_file: A Custom CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#cacert_file OpentelekomcloudProvider#cacert_file}
        :param cert: A client certificate to authenticate with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#cert OpentelekomcloudProvider#cert}
        :param cloud: An entry in a ``clouds.yaml`` file to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#cloud OpentelekomcloudProvider#cloud}
        :param delegated_project: The name of delegated project (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#delegated_project OpentelekomcloudProvider#delegated_project}
        :param domain_id: The ID of the Domain to scope to (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#domain_id OpentelekomcloudProvider#domain_id}
        :param domain_name: The name of the Domain to scope to (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#domain_name OpentelekomcloudProvider#domain_name}
        :param endpoint_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#endpoint_type OpentelekomcloudProvider#endpoint_type}.
        :param insecure: Trust self-signed certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#insecure OpentelekomcloudProvider#insecure}
        :param key: A client private key to authenticate with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#key OpentelekomcloudProvider#key}
        :param max_backoff_retries: How many times HTTP request should be retried when rate limit reached. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#max_backoff_retries OpentelekomcloudProvider#max_backoff_retries}
        :param max_retries: How many times HTTP connection should be retried until giving up. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#max_retries OpentelekomcloudProvider#max_retries}
        :param passcode: One-time MFA passcode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#passcode OpentelekomcloudProvider#passcode}
        :param password: Password to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#password OpentelekomcloudProvider#password}
        :param region: The OpenTelekomCloud region to connect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#region OpentelekomcloudProvider#region}
        :param secret_key: The secret key for API operations. You can retrieve this from the 'My Credential' section of the console. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#secret_key OpentelekomcloudProvider#secret_key}
        :param security_token: Security token to use for OBS federated authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#security_token OpentelekomcloudProvider#security_token}
        :param swauth: Use Swift's authentication system instead of Keystone. Only used for interaction with Swift. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#swauth OpentelekomcloudProvider#swauth}
        :param tenant_id: The ID of the Tenant (Identity v2) or Project (Identity v3) to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#tenant_id OpentelekomcloudProvider#tenant_id}
        :param tenant_name: The name of the Tenant (Identity v2) or Project (Identity v3) to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#tenant_name OpentelekomcloudProvider#tenant_name}
        :param token: Authentication token to use as an alternative to username/password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#token OpentelekomcloudProvider#token}
        :param user_id: User ID to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#user_id OpentelekomcloudProvider#user_id}
        :param user_name: Username to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#user_name OpentelekomcloudProvider#user_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a52b3f259b0a87db1c3c691be4f6a456b017461314df719108eb69b4d713b368)
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument agency_domain_name", value=agency_domain_name, expected_type=type_hints["agency_domain_name"])
            check_type(argname="argument agency_name", value=agency_name, expected_type=type_hints["agency_name"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument allow_reauth", value=allow_reauth, expected_type=type_hints["allow_reauth"])
            check_type(argname="argument auth_url", value=auth_url, expected_type=type_hints["auth_url"])
            check_type(argname="argument backoff_retry_timeout", value=backoff_retry_timeout, expected_type=type_hints["backoff_retry_timeout"])
            check_type(argname="argument cacert_file", value=cacert_file, expected_type=type_hints["cacert_file"])
            check_type(argname="argument cert", value=cert, expected_type=type_hints["cert"])
            check_type(argname="argument cloud", value=cloud, expected_type=type_hints["cloud"])
            check_type(argname="argument delegated_project", value=delegated_project, expected_type=type_hints["delegated_project"])
            check_type(argname="argument domain_id", value=domain_id, expected_type=type_hints["domain_id"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
            check_type(argname="argument insecure", value=insecure, expected_type=type_hints["insecure"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument max_backoff_retries", value=max_backoff_retries, expected_type=type_hints["max_backoff_retries"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument passcode", value=passcode, expected_type=type_hints["passcode"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
            check_type(argname="argument security_token", value=security_token, expected_type=type_hints["security_token"])
            check_type(argname="argument swauth", value=swauth, expected_type=type_hints["swauth"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument tenant_name", value=tenant_name, expected_type=type_hints["tenant_name"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_key is not None:
            self._values["access_key"] = access_key
        if agency_domain_name is not None:
            self._values["agency_domain_name"] = agency_domain_name
        if agency_name is not None:
            self._values["agency_name"] = agency_name
        if alias is not None:
            self._values["alias"] = alias
        if allow_reauth is not None:
            self._values["allow_reauth"] = allow_reauth
        if auth_url is not None:
            self._values["auth_url"] = auth_url
        if backoff_retry_timeout is not None:
            self._values["backoff_retry_timeout"] = backoff_retry_timeout
        if cacert_file is not None:
            self._values["cacert_file"] = cacert_file
        if cert is not None:
            self._values["cert"] = cert
        if cloud is not None:
            self._values["cloud"] = cloud
        if delegated_project is not None:
            self._values["delegated_project"] = delegated_project
        if domain_id is not None:
            self._values["domain_id"] = domain_id
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if endpoint_type is not None:
            self._values["endpoint_type"] = endpoint_type
        if insecure is not None:
            self._values["insecure"] = insecure
        if key is not None:
            self._values["key"] = key
        if max_backoff_retries is not None:
            self._values["max_backoff_retries"] = max_backoff_retries
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if passcode is not None:
            self._values["passcode"] = passcode
        if password is not None:
            self._values["password"] = password
        if region is not None:
            self._values["region"] = region
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if security_token is not None:
            self._values["security_token"] = security_token
        if swauth is not None:
            self._values["swauth"] = swauth
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id
        if tenant_name is not None:
            self._values["tenant_name"] = tenant_name
        if token is not None:
            self._values["token"] = token
        if user_id is not None:
            self._values["user_id"] = user_id
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def access_key(self) -> typing.Optional[builtins.str]:
        '''The access key for API operations. You can retrieve this from the 'My Credential' section of the console.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#access_key OpentelekomcloudProvider#access_key}
        '''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def agency_domain_name(self) -> typing.Optional[builtins.str]:
        '''The name of domain who created the agency (Identity v3).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#agency_domain_name OpentelekomcloudProvider#agency_domain_name}
        '''
        result = self._values.get("agency_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def agency_name(self) -> typing.Optional[builtins.str]:
        '''The name of agency.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#agency_name OpentelekomcloudProvider#agency_name}
        '''
        result = self._values.get("agency_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#alias OpentelekomcloudProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_reauth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#allow_reauth OpentelekomcloudProvider#allow_reauth}.'''
        result = self._values.get("allow_reauth")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auth_url(self) -> typing.Optional[builtins.str]:
        '''The Identity authentication URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#auth_url OpentelekomcloudProvider#auth_url}
        '''
        result = self._values.get("auth_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backoff_retry_timeout(self) -> typing.Optional[jsii.Number]:
        '''Timeout in seconds for backoff retry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#backoff_retry_timeout OpentelekomcloudProvider#backoff_retry_timeout}
        '''
        result = self._values.get("backoff_retry_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cacert_file(self) -> typing.Optional[builtins.str]:
        '''A Custom CA certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#cacert_file OpentelekomcloudProvider#cacert_file}
        '''
        result = self._values.get("cacert_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cert(self) -> typing.Optional[builtins.str]:
        '''A client certificate to authenticate with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#cert OpentelekomcloudProvider#cert}
        '''
        result = self._values.get("cert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud(self) -> typing.Optional[builtins.str]:
        '''An entry in a ``clouds.yaml`` file to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#cloud OpentelekomcloudProvider#cloud}
        '''
        result = self._values.get("cloud")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delegated_project(self) -> typing.Optional[builtins.str]:
        '''The name of delegated project (Identity v3).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#delegated_project OpentelekomcloudProvider#delegated_project}
        '''
        result = self._values.get("delegated_project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Domain to scope to (Identity v3).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#domain_id OpentelekomcloudProvider#domain_id}
        '''
        result = self._values.get("domain_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Domain to scope to (Identity v3).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#domain_name OpentelekomcloudProvider#domain_name}
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#endpoint_type OpentelekomcloudProvider#endpoint_type}.'''
        result = self._values.get("endpoint_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Trust self-signed certificates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#insecure OpentelekomcloudProvider#insecure}
        '''
        result = self._values.get("insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''A client private key to authenticate with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#key OpentelekomcloudProvider#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_backoff_retries(self) -> typing.Optional[jsii.Number]:
        '''How many times HTTP request should be retried when rate limit reached.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#max_backoff_retries OpentelekomcloudProvider#max_backoff_retries}
        '''
        result = self._values.get("max_backoff_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''How many times HTTP connection should be retried until giving up.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#max_retries OpentelekomcloudProvider#max_retries}
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def passcode(self) -> typing.Optional[builtins.str]:
        '''One-time MFA passcode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#passcode OpentelekomcloudProvider#passcode}
        '''
        result = self._values.get("passcode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password to login with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#password OpentelekomcloudProvider#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The OpenTelekomCloud region to connect to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#region OpentelekomcloudProvider#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''The secret key for API operations. You can retrieve this from the 'My Credential' section of the console.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#secret_key OpentelekomcloudProvider#secret_key}
        '''
        result = self._values.get("secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_token(self) -> typing.Optional[builtins.str]:
        '''Security token to use for OBS federated authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#security_token OpentelekomcloudProvider#security_token}
        '''
        result = self._values.get("security_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def swauth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use Swift's authentication system instead of Keystone. Only used for interaction with Swift.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#swauth OpentelekomcloudProvider#swauth}
        '''
        result = self._values.get("swauth")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Tenant (Identity v2) or Project (Identity v3) to login with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#tenant_id OpentelekomcloudProvider#tenant_id}
        '''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Tenant (Identity v2) or Project (Identity v3) to login with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#tenant_name OpentelekomcloudProvider#tenant_name}
        '''
        result = self._values.get("tenant_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''Authentication token to use as an alternative to username/password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#token OpentelekomcloudProvider#token}
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_id(self) -> typing.Optional[builtins.str]:
        '''User ID to login with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#user_id OpentelekomcloudProvider#user_id}
        '''
        result = self._values.get("user_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''Username to login with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs#user_name OpentelekomcloudProvider#user_name}
        '''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OpentelekomcloudProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "OpentelekomcloudProvider",
    "OpentelekomcloudProviderConfig",
]

publication.publish()

def _typecheckingstub__f19b09b6a4b958a59149fefac7a07c00625b0a23b7c2ad34bbc3b21fa8d278ec(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_key: typing.Optional[builtins.str] = None,
    agency_domain_name: typing.Optional[builtins.str] = None,
    agency_name: typing.Optional[builtins.str] = None,
    alias: typing.Optional[builtins.str] = None,
    allow_reauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auth_url: typing.Optional[builtins.str] = None,
    backoff_retry_timeout: typing.Optional[jsii.Number] = None,
    cacert_file: typing.Optional[builtins.str] = None,
    cert: typing.Optional[builtins.str] = None,
    cloud: typing.Optional[builtins.str] = None,
    delegated_project: typing.Optional[builtins.str] = None,
    domain_id: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    endpoint_type: typing.Optional[builtins.str] = None,
    insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    max_backoff_retries: typing.Optional[jsii.Number] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    passcode: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    secret_key: typing.Optional[builtins.str] = None,
    security_token: typing.Optional[builtins.str] = None,
    swauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    tenant_name: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    user_id: typing.Optional[builtins.str] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf9e726e08667ae4c2aa8d4ba55e042303b0f178f069ab0737f59b1c830cc695(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3172b590a5b9bdfb2dc036a4707953c9b163f5bd15562d4ff5ae45e98b7f5020(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4bcac68a338e57ea0829c716ce01840cc5fe52bb2c40664f1ab78ca06748ea(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95799e02207dcfe0156e5a0d09c5fa444c0796876e26a08e6b661ee1f76b1e11(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a8c8a0f937546f5fa90203ea8bae720fbdf9eb46d8f309497e355dcb1beb230(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af0af7f726c5c28ba0a4275949289839ff18e3943fccadac132cdfdd50287c10(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2bb961cf0d47c6cb580701fa6b0de11e1667273bb4e8120bb2c84568c4e4784(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c199e6a45c567b94962a41f5a6f4c5a77838eeec89833e3d3c2f5b2f13147553(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf6a505fa8ae233bc84d147c35d3dee4b0bc3bf559c82cfae5ac49e1708e9677(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f5ff2cfd114ed2f88d1ba2099cb2c05fb07d13500a43ffb9b2eab790091e5e5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887c36f38e927f27bf0474b7af1b563cba26d72d6245697f9d85880c3d402108(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc16d5debce0a8860c78d09b2ee74851127d931ab5b829d9dd06a0526adc65a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac7032fce22b9414a16c00018ced13508f86dd0c9b6d755596b16463a9e9265(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf12410dca374ab29fc50b310bc5f14b54e76b5e77c1f7b51a01e5b1c432ceb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce29fadc76cb1a45509d361ed2c62ebc36bc5e03c35770c687952cd6148d1aa4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b2be7d37dab8ecf05256fdb769c99b53544f669aae7b1d1f574d9b83e549c29(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6565f9d9010bc716fdf441d19efefff3442b9a52f4a4bf9a997eed9d10689d87(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__708bd769831a36616e62db2c336cb222f8a77a503ae1141dd45a83fa2a827ea7(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60785e85ad8faa17e399c9893716fe684769b926cb6307ce8891b9dfe715a529(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0cb20997394429b9a9145a69d98d46e3593cc22dfa18caf88b147b2f3cdda31(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed9306fcc7952f4cacef6c3a407dd576c14b1bbced31b599a3e2c83c1b4d68a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fc5ae1aea312df8541adca0cbbcdec6ba821883b6d276bdbd8a3f951b33888c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4cfe001cf9502f21be91992d0309a5a6355d0b25a23fe010058991ef1b9f37e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb22454f3f549ad2f7c8f45ae2e24d5f3fac2ab080a2fdd8d701c72889820263(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3707224789c866f47aa60215b768b0027c03dbbe69c982a7af889c5ca0b6f34f(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e45fe59e51c12e62c10a6d5ee5cd55355079296744d28ad14824f8a40b193d3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68974106bdca0c35cee773caece0edf2b881c8ed00ac1de3e7e70445b608268(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6cac84878a9f7cd18f6834ff48b37f72ef981b8715f3d39186d278f86ada0d6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff1cc6a67d7d548fe3d339a7a7d19bfdf8160980ea750ac1a9dc8697535b29fa(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60774c8a815da1e9cc9a7d4a34a6bb4cd77fef07a42636980108155af8ec65e3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a52b3f259b0a87db1c3c691be4f6a456b017461314df719108eb69b4d713b368(
    *,
    access_key: typing.Optional[builtins.str] = None,
    agency_domain_name: typing.Optional[builtins.str] = None,
    agency_name: typing.Optional[builtins.str] = None,
    alias: typing.Optional[builtins.str] = None,
    allow_reauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auth_url: typing.Optional[builtins.str] = None,
    backoff_retry_timeout: typing.Optional[jsii.Number] = None,
    cacert_file: typing.Optional[builtins.str] = None,
    cert: typing.Optional[builtins.str] = None,
    cloud: typing.Optional[builtins.str] = None,
    delegated_project: typing.Optional[builtins.str] = None,
    domain_id: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    endpoint_type: typing.Optional[builtins.str] = None,
    insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    max_backoff_retries: typing.Optional[jsii.Number] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    passcode: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    secret_key: typing.Optional[builtins.str] = None,
    security_token: typing.Optional[builtins.str] = None,
    swauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    tenant_name: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    user_id: typing.Optional[builtins.str] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
