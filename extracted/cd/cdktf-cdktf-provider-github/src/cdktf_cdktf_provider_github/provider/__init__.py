r'''
# `provider`

Refer to the Terraform Registry for docs: [`github`](https://registry.terraform.io/providers/integrations/github/6.6.0/docs).
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


class GithubProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.provider.GithubProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs github}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alias: typing.Optional[builtins.str] = None,
        app_auth: typing.Optional[typing.Union["GithubProviderAppAuth", typing.Dict[builtins.str, typing.Any]]] = None,
        base_url: typing.Optional[builtins.str] = None,
        insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        organization: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        parallel_requests: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        read_delay_ms: typing.Optional[jsii.Number] = None,
        retryable_errors: typing.Optional[typing.Sequence[jsii.Number]] = None,
        retry_delay_ms: typing.Optional[jsii.Number] = None,
        token: typing.Optional[builtins.str] = None,
        write_delay_ms: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs github} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#alias GithubProvider#alias}
        :param app_auth: app_auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#app_auth GithubProvider#app_auth}
        :param base_url: The GitHub Base API URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#base_url GithubProvider#base_url}
        :param insecure: Enable ``insecure`` mode for testing purposes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#insecure GithubProvider#insecure}
        :param max_retries: Number of times to retry a request after receiving an error status codeDefaults to 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#max_retries GithubProvider#max_retries}
        :param organization: The GitHub organization name to manage. Use this field instead of ``owner`` when managing organization accounts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#organization GithubProvider#organization}
        :param owner: The GitHub owner name to manage. Use this field instead of ``organization`` when managing individual accounts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#owner GithubProvider#owner}
        :param parallel_requests: Allow the provider to make parallel API calls to GitHub. You may want to set it to true when you have a private Github Enterprise without strict rate limits. Although, it is not possible to enable this setting on github.com because we enforce the respect of github.com's best practices to avoid hitting abuse rate limitsDefaults to false if not set Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#parallel_requests GithubProvider#parallel_requests}
        :param read_delay_ms: Amount of time in milliseconds to sleep in between non-write requests to GitHub API. Defaults to 0ms if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#read_delay_ms GithubProvider#read_delay_ms}
        :param retryable_errors: Allow the provider to retry after receiving an error status code, the max_retries should be set for this to workDefaults to [500, 502, 503, 504]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#retryable_errors GithubProvider#retryable_errors}
        :param retry_delay_ms: Amount of time in milliseconds to sleep in between requests to GitHub API after an error response. Defaults to 1000ms or 1s if not set, the max_retries must be set to greater than zero. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#retry_delay_ms GithubProvider#retry_delay_ms}
        :param token: The OAuth token used to connect to GitHub. Anonymous mode is enabled if both ``token`` and ``app_auth`` are not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#token GithubProvider#token}
        :param write_delay_ms: Amount of time in milliseconds to sleep in between writes to GitHub API. Defaults to 1000ms or 1s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#write_delay_ms GithubProvider#write_delay_ms}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__263b17282ec79ed35fd0a2aa7312f65b9722bb22a4a929cbffd643911fccca4e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = GithubProviderConfig(
            alias=alias,
            app_auth=app_auth,
            base_url=base_url,
            insecure=insecure,
            max_retries=max_retries,
            organization=organization,
            owner=owner,
            parallel_requests=parallel_requests,
            read_delay_ms=read_delay_ms,
            retryable_errors=retryable_errors,
            retry_delay_ms=retry_delay_ms,
            token=token,
            write_delay_ms=write_delay_ms,
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
        '''Generates CDKTF code for importing a GithubProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GithubProvider to import.
        :param import_from_id: The id of the existing GithubProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GithubProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd0457126fa28a386b2d6c739593bde426aa89d8bff015d702cb3b2e8e2c1899)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetAppAuth")
    def reset_app_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppAuth", []))

    @jsii.member(jsii_name="resetBaseUrl")
    def reset_base_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaseUrl", []))

    @jsii.member(jsii_name="resetInsecure")
    def reset_insecure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecure", []))

    @jsii.member(jsii_name="resetMaxRetries")
    def reset_max_retries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRetries", []))

    @jsii.member(jsii_name="resetOrganization")
    def reset_organization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganization", []))

    @jsii.member(jsii_name="resetOwner")
    def reset_owner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwner", []))

    @jsii.member(jsii_name="resetParallelRequests")
    def reset_parallel_requests(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelRequests", []))

    @jsii.member(jsii_name="resetReadDelayMs")
    def reset_read_delay_ms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadDelayMs", []))

    @jsii.member(jsii_name="resetRetryableErrors")
    def reset_retryable_errors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryableErrors", []))

    @jsii.member(jsii_name="resetRetryDelayMs")
    def reset_retry_delay_ms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryDelayMs", []))

    @jsii.member(jsii_name="resetToken")
    def reset_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToken", []))

    @jsii.member(jsii_name="resetWriteDelayMs")
    def reset_write_delay_ms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriteDelayMs", []))

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
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="appAuthInput")
    def app_auth_input(self) -> typing.Optional["GithubProviderAppAuth"]:
        return typing.cast(typing.Optional["GithubProviderAppAuth"], jsii.get(self, "appAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="baseUrlInput")
    def base_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseUrlInput"))

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
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property
    @jsii.member(jsii_name="ownerInput")
    def owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelRequestsInput")
    def parallel_requests_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "parallelRequestsInput"))

    @builtins.property
    @jsii.member(jsii_name="readDelayMsInput")
    def read_delay_ms_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "readDelayMsInput"))

    @builtins.property
    @jsii.member(jsii_name="retryableErrorsInput")
    def retryable_errors_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "retryableErrorsInput"))

    @builtins.property
    @jsii.member(jsii_name="retryDelayMsInput")
    def retry_delay_ms_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryDelayMsInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property
    @jsii.member(jsii_name="writeDelayMsInput")
    def write_delay_ms_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "writeDelayMsInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a7df1a85bb512988f19a1417469a68dc9f3f832306ba4600d01b15a54e33a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appAuth")
    def app_auth(self) -> typing.Optional["GithubProviderAppAuth"]:
        return typing.cast(typing.Optional["GithubProviderAppAuth"], jsii.get(self, "appAuth"))

    @app_auth.setter
    def app_auth(self, value: typing.Optional["GithubProviderAppAuth"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d009645caf5b3aa95aaaeb8950fca59e2a4f7a246795a607f36f536e1c8e72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="baseUrl")
    def base_url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseUrl"))

    @base_url.setter
    def base_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1e8a9f050241b0adb2375d77c49a1dc5c5f3d61d7a4d56a2f69760ab81fd9f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseUrl", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__f1547f34bf54e94384030ecc9635020b985570ab2b7847aba4122d15600c23f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetries"))

    @max_retries.setter
    def max_retries(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32c0a42c2776b1c38d4f8f990038986a1e72f98a53d2e654f21b0a8f3afa9121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organization")
    def organization(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__496d5d7dbc7450206d7f18b5b29e4831e368921d1d2814fea48dc536d52ba48d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "owner"))

    @owner.setter
    def owner(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bc3ae5783a9b1025c79fb427d1e9416f60992889ebdb49bd6534fd7e132df2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "owner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parallelRequests")
    def parallel_requests(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "parallelRequests"))

    @parallel_requests.setter
    def parallel_requests(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a1b2b1c8b17f316b9d055b97b99df69adcdd22452cfedccb9830ec8a6aef9dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readDelayMs")
    def read_delay_ms(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "readDelayMs"))

    @read_delay_ms.setter
    def read_delay_ms(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8847ad0c7431444c8e68fe99bc76ddb822d7165ab96efc8ff1b2a83d634c1e2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readDelayMs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryableErrors")
    def retryable_errors(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "retryableErrors"))

    @retryable_errors.setter
    def retryable_errors(
        self,
        value: typing.Optional[typing.List[jsii.Number]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2291135211c272e16efba36349dcf63d24d39b41864f94b137615ff953848fc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryableErrors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryDelayMs")
    def retry_delay_ms(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryDelayMs"))

    @retry_delay_ms.setter
    def retry_delay_ms(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a88d1b36b161093b7e942f47cd58a29aecae1eed806c7a086204fa3231070e18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryDelayMs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "token"))

    @token.setter
    def token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b73d1898a25255187ad5f03a703f4ed7e51498a5dbb653472175fcb74640ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "token", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="writeDelayMs")
    def write_delay_ms(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "writeDelayMs"))

    @write_delay_ms.setter
    def write_delay_ms(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb5ddb0d45949c943310225d59cac2817644a41aec4ea75b70503eb1dee00742)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeDelayMs", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.provider.GithubProviderAppAuth",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "installation_id": "installationId",
        "pem_file": "pemFile",
    },
)
class GithubProviderAppAuth:
    def __init__(
        self,
        *,
        id: builtins.str,
        installation_id: builtins.str,
        pem_file: builtins.str,
    ) -> None:
        '''
        :param id: The GitHub App ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#id GithubProvider#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param installation_id: The GitHub App installation instance ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#installation_id GithubProvider#installation_id}
        :param pem_file: The GitHub App PEM file contents. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#pem_file GithubProvider#pem_file}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8729693c9234c4cd66566a7eb064abb87f28c8f6d397d9318fe071d5de03dc9)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument installation_id", value=installation_id, expected_type=type_hints["installation_id"])
            check_type(argname="argument pem_file", value=pem_file, expected_type=type_hints["pem_file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "installation_id": installation_id,
            "pem_file": pem_file,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''The GitHub App ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#id GithubProvider#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def installation_id(self) -> builtins.str:
        '''The GitHub App installation instance ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#installation_id GithubProvider#installation_id}
        '''
        result = self._values.get("installation_id")
        assert result is not None, "Required property 'installation_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pem_file(self) -> builtins.str:
        '''The GitHub App PEM file contents.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#pem_file GithubProvider#pem_file}
        '''
        result = self._values.get("pem_file")
        assert result is not None, "Required property 'pem_file' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GithubProviderAppAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.provider.GithubProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "app_auth": "appAuth",
        "base_url": "baseUrl",
        "insecure": "insecure",
        "max_retries": "maxRetries",
        "organization": "organization",
        "owner": "owner",
        "parallel_requests": "parallelRequests",
        "read_delay_ms": "readDelayMs",
        "retryable_errors": "retryableErrors",
        "retry_delay_ms": "retryDelayMs",
        "token": "token",
        "write_delay_ms": "writeDelayMs",
    },
)
class GithubProviderConfig:
    def __init__(
        self,
        *,
        alias: typing.Optional[builtins.str] = None,
        app_auth: typing.Optional[typing.Union[GithubProviderAppAuth, typing.Dict[builtins.str, typing.Any]]] = None,
        base_url: typing.Optional[builtins.str] = None,
        insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        organization: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        parallel_requests: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        read_delay_ms: typing.Optional[jsii.Number] = None,
        retryable_errors: typing.Optional[typing.Sequence[jsii.Number]] = None,
        retry_delay_ms: typing.Optional[jsii.Number] = None,
        token: typing.Optional[builtins.str] = None,
        write_delay_ms: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#alias GithubProvider#alias}
        :param app_auth: app_auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#app_auth GithubProvider#app_auth}
        :param base_url: The GitHub Base API URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#base_url GithubProvider#base_url}
        :param insecure: Enable ``insecure`` mode for testing purposes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#insecure GithubProvider#insecure}
        :param max_retries: Number of times to retry a request after receiving an error status codeDefaults to 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#max_retries GithubProvider#max_retries}
        :param organization: The GitHub organization name to manage. Use this field instead of ``owner`` when managing organization accounts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#organization GithubProvider#organization}
        :param owner: The GitHub owner name to manage. Use this field instead of ``organization`` when managing individual accounts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#owner GithubProvider#owner}
        :param parallel_requests: Allow the provider to make parallel API calls to GitHub. You may want to set it to true when you have a private Github Enterprise without strict rate limits. Although, it is not possible to enable this setting on github.com because we enforce the respect of github.com's best practices to avoid hitting abuse rate limitsDefaults to false if not set Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#parallel_requests GithubProvider#parallel_requests}
        :param read_delay_ms: Amount of time in milliseconds to sleep in between non-write requests to GitHub API. Defaults to 0ms if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#read_delay_ms GithubProvider#read_delay_ms}
        :param retryable_errors: Allow the provider to retry after receiving an error status code, the max_retries should be set for this to workDefaults to [500, 502, 503, 504]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#retryable_errors GithubProvider#retryable_errors}
        :param retry_delay_ms: Amount of time in milliseconds to sleep in between requests to GitHub API after an error response. Defaults to 1000ms or 1s if not set, the max_retries must be set to greater than zero. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#retry_delay_ms GithubProvider#retry_delay_ms}
        :param token: The OAuth token used to connect to GitHub. Anonymous mode is enabled if both ``token`` and ``app_auth`` are not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#token GithubProvider#token}
        :param write_delay_ms: Amount of time in milliseconds to sleep in between writes to GitHub API. Defaults to 1000ms or 1s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#write_delay_ms GithubProvider#write_delay_ms}
        '''
        if isinstance(app_auth, dict):
            app_auth = GithubProviderAppAuth(**app_auth)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99f0b1a4ad7bbf7bdfb94d1229c680f6c695f2c4a01bd6bb2ed57295c9dcd6f9)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument app_auth", value=app_auth, expected_type=type_hints["app_auth"])
            check_type(argname="argument base_url", value=base_url, expected_type=type_hints["base_url"])
            check_type(argname="argument insecure", value=insecure, expected_type=type_hints["insecure"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument parallel_requests", value=parallel_requests, expected_type=type_hints["parallel_requests"])
            check_type(argname="argument read_delay_ms", value=read_delay_ms, expected_type=type_hints["read_delay_ms"])
            check_type(argname="argument retryable_errors", value=retryable_errors, expected_type=type_hints["retryable_errors"])
            check_type(argname="argument retry_delay_ms", value=retry_delay_ms, expected_type=type_hints["retry_delay_ms"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument write_delay_ms", value=write_delay_ms, expected_type=type_hints["write_delay_ms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias
        if app_auth is not None:
            self._values["app_auth"] = app_auth
        if base_url is not None:
            self._values["base_url"] = base_url
        if insecure is not None:
            self._values["insecure"] = insecure
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if organization is not None:
            self._values["organization"] = organization
        if owner is not None:
            self._values["owner"] = owner
        if parallel_requests is not None:
            self._values["parallel_requests"] = parallel_requests
        if read_delay_ms is not None:
            self._values["read_delay_ms"] = read_delay_ms
        if retryable_errors is not None:
            self._values["retryable_errors"] = retryable_errors
        if retry_delay_ms is not None:
            self._values["retry_delay_ms"] = retry_delay_ms
        if token is not None:
            self._values["token"] = token
        if write_delay_ms is not None:
            self._values["write_delay_ms"] = write_delay_ms

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#alias GithubProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_auth(self) -> typing.Optional[GithubProviderAppAuth]:
        '''app_auth block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#app_auth GithubProvider#app_auth}
        '''
        result = self._values.get("app_auth")
        return typing.cast(typing.Optional[GithubProviderAppAuth], result)

    @builtins.property
    def base_url(self) -> typing.Optional[builtins.str]:
        '''The GitHub Base API URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#base_url GithubProvider#base_url}
        '''
        result = self._values.get("base_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable ``insecure`` mode for testing purposes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#insecure GithubProvider#insecure}
        '''
        result = self._values.get("insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''Number of times to retry a request after receiving an error status codeDefaults to 3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#max_retries GithubProvider#max_retries}
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def organization(self) -> typing.Optional[builtins.str]:
        '''The GitHub organization name to manage. Use this field instead of ``owner`` when managing organization accounts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#organization GithubProvider#organization}
        '''
        result = self._values.get("organization")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner(self) -> typing.Optional[builtins.str]:
        '''The GitHub owner name to manage. Use this field instead of ``organization`` when managing individual accounts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#owner GithubProvider#owner}
        '''
        result = self._values.get("owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parallel_requests(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow the provider to make parallel API calls to GitHub.

        You may want to set it to true when you have a private Github Enterprise without strict rate limits. Although, it is not possible to enable this setting on github.com because we enforce the respect of github.com's best practices to avoid hitting abuse rate limitsDefaults to false if not set

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#parallel_requests GithubProvider#parallel_requests}
        '''
        result = self._values.get("parallel_requests")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def read_delay_ms(self) -> typing.Optional[jsii.Number]:
        '''Amount of time in milliseconds to sleep in between non-write requests to GitHub API.

        Defaults to 0ms if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#read_delay_ms GithubProvider#read_delay_ms}
        '''
        result = self._values.get("read_delay_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retryable_errors(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Allow the provider to retry after receiving an error status code, the max_retries should be set for this to workDefaults to [500, 502, 503, 504].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#retryable_errors GithubProvider#retryable_errors}
        '''
        result = self._values.get("retryable_errors")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def retry_delay_ms(self) -> typing.Optional[jsii.Number]:
        '''Amount of time in milliseconds to sleep in between requests to GitHub API after an error response.

        Defaults to 1000ms or 1s if not set, the max_retries must be set to greater than zero.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#retry_delay_ms GithubProvider#retry_delay_ms}
        '''
        result = self._values.get("retry_delay_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''The OAuth token used to connect to GitHub.

        Anonymous mode is enabled if both ``token`` and ``app_auth`` are not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#token GithubProvider#token}
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def write_delay_ms(self) -> typing.Optional[jsii.Number]:
        '''Amount of time in milliseconds to sleep in between writes to GitHub API.

        Defaults to 1000ms or 1s if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs#write_delay_ms GithubProvider#write_delay_ms}
        '''
        result = self._values.get("write_delay_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GithubProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "GithubProvider",
    "GithubProviderAppAuth",
    "GithubProviderConfig",
]

publication.publish()

def _typecheckingstub__263b17282ec79ed35fd0a2aa7312f65b9722bb22a4a929cbffd643911fccca4e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alias: typing.Optional[builtins.str] = None,
    app_auth: typing.Optional[typing.Union[GithubProviderAppAuth, typing.Dict[builtins.str, typing.Any]]] = None,
    base_url: typing.Optional[builtins.str] = None,
    insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    organization: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    parallel_requests: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    read_delay_ms: typing.Optional[jsii.Number] = None,
    retryable_errors: typing.Optional[typing.Sequence[jsii.Number]] = None,
    retry_delay_ms: typing.Optional[jsii.Number] = None,
    token: typing.Optional[builtins.str] = None,
    write_delay_ms: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd0457126fa28a386b2d6c739593bde426aa89d8bff015d702cb3b2e8e2c1899(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a7df1a85bb512988f19a1417469a68dc9f3f832306ba4600d01b15a54e33a8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d009645caf5b3aa95aaaeb8950fca59e2a4f7a246795a607f36f536e1c8e72(
    value: typing.Optional[GithubProviderAppAuth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e8a9f050241b0adb2375d77c49a1dc5c5f3d61d7a4d56a2f69760ab81fd9f7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1547f34bf54e94384030ecc9635020b985570ab2b7847aba4122d15600c23f4(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32c0a42c2776b1c38d4f8f990038986a1e72f98a53d2e654f21b0a8f3afa9121(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496d5d7dbc7450206d7f18b5b29e4831e368921d1d2814fea48dc536d52ba48d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bc3ae5783a9b1025c79fb427d1e9416f60992889ebdb49bd6534fd7e132df2a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1b2b1c8b17f316b9d055b97b99df69adcdd22452cfedccb9830ec8a6aef9dc(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8847ad0c7431444c8e68fe99bc76ddb822d7165ab96efc8ff1b2a83d634c1e2c(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2291135211c272e16efba36349dcf63d24d39b41864f94b137615ff953848fc9(
    value: typing.Optional[typing.List[jsii.Number]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a88d1b36b161093b7e942f47cd58a29aecae1eed806c7a086204fa3231070e18(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b73d1898a25255187ad5f03a703f4ed7e51498a5dbb653472175fcb74640ba(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb5ddb0d45949c943310225d59cac2817644a41aec4ea75b70503eb1dee00742(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8729693c9234c4cd66566a7eb064abb87f28c8f6d397d9318fe071d5de03dc9(
    *,
    id: builtins.str,
    installation_id: builtins.str,
    pem_file: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99f0b1a4ad7bbf7bdfb94d1229c680f6c695f2c4a01bd6bb2ed57295c9dcd6f9(
    *,
    alias: typing.Optional[builtins.str] = None,
    app_auth: typing.Optional[typing.Union[GithubProviderAppAuth, typing.Dict[builtins.str, typing.Any]]] = None,
    base_url: typing.Optional[builtins.str] = None,
    insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    organization: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    parallel_requests: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    read_delay_ms: typing.Optional[jsii.Number] = None,
    retryable_errors: typing.Optional[typing.Sequence[jsii.Number]] = None,
    retry_delay_ms: typing.Optional[jsii.Number] = None,
    token: typing.Optional[builtins.str] = None,
    write_delay_ms: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
