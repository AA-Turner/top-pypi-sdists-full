r'''
# `provider`

Refer to the Terraform Registry for docs: [`pagerduty`](https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs).
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


class PagerdutyProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.provider.PagerdutyProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs pagerduty}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alias: typing.Optional[builtins.str] = None,
        api_url_override: typing.Optional[builtins.str] = None,
        insecure_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        service_region: typing.Optional[builtins.str] = None,
        skip_credentials_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        token: typing.Optional[builtins.str] = None,
        use_app_oauth_scoped_token: typing.Optional[typing.Union["PagerdutyProviderUseAppOauthScopedToken", typing.Dict[builtins.str, typing.Any]]] = None,
        user_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs pagerduty} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#alias PagerdutyProvider#alias}
        :param api_url_override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#api_url_override PagerdutyProvider#api_url_override}.
        :param insecure_tls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#insecure_tls PagerdutyProvider#insecure_tls}.
        :param service_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#service_region PagerdutyProvider#service_region}.
        :param skip_credentials_validation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#skip_credentials_validation PagerdutyProvider#skip_credentials_validation}.
        :param token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#token PagerdutyProvider#token}.
        :param use_app_oauth_scoped_token: use_app_oauth_scoped_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#use_app_oauth_scoped_token PagerdutyProvider#use_app_oauth_scoped_token}
        :param user_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#user_token PagerdutyProvider#user_token}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3509512539073bbac9bc9e66d0efe0caaf04a43d2d2d30a6569b117bd193cb4a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = PagerdutyProviderConfig(
            alias=alias,
            api_url_override=api_url_override,
            insecure_tls=insecure_tls,
            service_region=service_region,
            skip_credentials_validation=skip_credentials_validation,
            token=token,
            use_app_oauth_scoped_token=use_app_oauth_scoped_token,
            user_token=user_token,
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
        '''Generates CDKTF code for importing a PagerdutyProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PagerdutyProvider to import.
        :param import_from_id: The id of the existing PagerdutyProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PagerdutyProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__602aea9d9d3dbc68d164ba8b94d941795e6af210453222a0ecb39912704f53aa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetApiUrlOverride")
    def reset_api_url_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiUrlOverride", []))

    @jsii.member(jsii_name="resetInsecureTls")
    def reset_insecure_tls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecureTls", []))

    @jsii.member(jsii_name="resetServiceRegion")
    def reset_service_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceRegion", []))

    @jsii.member(jsii_name="resetSkipCredentialsValidation")
    def reset_skip_credentials_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipCredentialsValidation", []))

    @jsii.member(jsii_name="resetToken")
    def reset_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToken", []))

    @jsii.member(jsii_name="resetUseAppOauthScopedToken")
    def reset_use_app_oauth_scoped_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseAppOauthScopedToken", []))

    @jsii.member(jsii_name="resetUserToken")
    def reset_user_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserToken", []))

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
    @jsii.member(jsii_name="apiUrlOverrideInput")
    def api_url_override_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiUrlOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureTlsInput")
    def insecure_tls_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureTlsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceRegionInput")
    def service_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="skipCredentialsValidationInput")
    def skip_credentials_validation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipCredentialsValidationInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property
    @jsii.member(jsii_name="useAppOauthScopedTokenInput")
    def use_app_oauth_scoped_token_input(
        self,
    ) -> typing.Optional["PagerdutyProviderUseAppOauthScopedToken"]:
        return typing.cast(typing.Optional["PagerdutyProviderUseAppOauthScopedToken"], jsii.get(self, "useAppOauthScopedTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="userTokenInput")
    def user_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ab5e1975f1f35ff8003d06ebf251c81aa151b9b3c183802ac9eda99976332d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiUrlOverride")
    def api_url_override(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiUrlOverride"))

    @api_url_override.setter
    def api_url_override(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7b1fa8b4430b3025525c11a441481f604f2d3cb14e8032fb09e75cf5c81901f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiUrlOverride", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="insecureTls")
    def insecure_tls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureTls"))

    @insecure_tls.setter
    def insecure_tls(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e317dff346f42c3f4d8163300830a0a45c34ab4367a8da082b477356ad1065d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecureTls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceRegion")
    def service_region(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceRegion"))

    @service_region.setter
    def service_region(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19e068b11155672d909e4a3bb1fb00989fb34e9c4b4dfc2e673f17488dce5cb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceRegion", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__f9c727215676dfd6aa621a0c0bb4ed4421fd9644cca069f5f743be40b809a939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipCredentialsValidation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "token"))

    @token.setter
    def token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec053ae433540bf873d7de07938287a9cc766ca9841a9758ef9eda90d531eb53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "token", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useAppOauthScopedToken")
    def use_app_oauth_scoped_token(
        self,
    ) -> typing.Optional["PagerdutyProviderUseAppOauthScopedToken"]:
        return typing.cast(typing.Optional["PagerdutyProviderUseAppOauthScopedToken"], jsii.get(self, "useAppOauthScopedToken"))

    @use_app_oauth_scoped_token.setter
    def use_app_oauth_scoped_token(
        self,
        value: typing.Optional["PagerdutyProviderUseAppOauthScopedToken"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8bbf080914872f5e18998ff71070347e6430ae732ba095db63b05b36c396030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useAppOauthScopedToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userToken")
    def user_token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userToken"))

    @user_token.setter
    def user_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__610f760da361297fbb18811c7be0c5d5b0acf937774f7060f3cb21a92800ee40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userToken", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.provider.PagerdutyProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "api_url_override": "apiUrlOverride",
        "insecure_tls": "insecureTls",
        "service_region": "serviceRegion",
        "skip_credentials_validation": "skipCredentialsValidation",
        "token": "token",
        "use_app_oauth_scoped_token": "useAppOauthScopedToken",
        "user_token": "userToken",
    },
)
class PagerdutyProviderConfig:
    def __init__(
        self,
        *,
        alias: typing.Optional[builtins.str] = None,
        api_url_override: typing.Optional[builtins.str] = None,
        insecure_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        service_region: typing.Optional[builtins.str] = None,
        skip_credentials_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        token: typing.Optional[builtins.str] = None,
        use_app_oauth_scoped_token: typing.Optional[typing.Union["PagerdutyProviderUseAppOauthScopedToken", typing.Dict[builtins.str, typing.Any]]] = None,
        user_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#alias PagerdutyProvider#alias}
        :param api_url_override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#api_url_override PagerdutyProvider#api_url_override}.
        :param insecure_tls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#insecure_tls PagerdutyProvider#insecure_tls}.
        :param service_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#service_region PagerdutyProvider#service_region}.
        :param skip_credentials_validation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#skip_credentials_validation PagerdutyProvider#skip_credentials_validation}.
        :param token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#token PagerdutyProvider#token}.
        :param use_app_oauth_scoped_token: use_app_oauth_scoped_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#use_app_oauth_scoped_token PagerdutyProvider#use_app_oauth_scoped_token}
        :param user_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#user_token PagerdutyProvider#user_token}.
        '''
        if isinstance(use_app_oauth_scoped_token, dict):
            use_app_oauth_scoped_token = PagerdutyProviderUseAppOauthScopedToken(**use_app_oauth_scoped_token)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f37403effaf2562475b00ed85353fa25e811a6793d058dc4abb17e4cdf808b0)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument api_url_override", value=api_url_override, expected_type=type_hints["api_url_override"])
            check_type(argname="argument insecure_tls", value=insecure_tls, expected_type=type_hints["insecure_tls"])
            check_type(argname="argument service_region", value=service_region, expected_type=type_hints["service_region"])
            check_type(argname="argument skip_credentials_validation", value=skip_credentials_validation, expected_type=type_hints["skip_credentials_validation"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument use_app_oauth_scoped_token", value=use_app_oauth_scoped_token, expected_type=type_hints["use_app_oauth_scoped_token"])
            check_type(argname="argument user_token", value=user_token, expected_type=type_hints["user_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias
        if api_url_override is not None:
            self._values["api_url_override"] = api_url_override
        if insecure_tls is not None:
            self._values["insecure_tls"] = insecure_tls
        if service_region is not None:
            self._values["service_region"] = service_region
        if skip_credentials_validation is not None:
            self._values["skip_credentials_validation"] = skip_credentials_validation
        if token is not None:
            self._values["token"] = token
        if use_app_oauth_scoped_token is not None:
            self._values["use_app_oauth_scoped_token"] = use_app_oauth_scoped_token
        if user_token is not None:
            self._values["user_token"] = user_token

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#alias PagerdutyProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_url_override(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#api_url_override PagerdutyProvider#api_url_override}.'''
        result = self._values.get("api_url_override")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insecure_tls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#insecure_tls PagerdutyProvider#insecure_tls}.'''
        result = self._values.get("insecure_tls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def service_region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#service_region PagerdutyProvider#service_region}.'''
        result = self._values.get("service_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_credentials_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#skip_credentials_validation PagerdutyProvider#skip_credentials_validation}.'''
        result = self._values.get("skip_credentials_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#token PagerdutyProvider#token}.'''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_app_oauth_scoped_token(
        self,
    ) -> typing.Optional["PagerdutyProviderUseAppOauthScopedToken"]:
        '''use_app_oauth_scoped_token block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#use_app_oauth_scoped_token PagerdutyProvider#use_app_oauth_scoped_token}
        '''
        result = self._values.get("use_app_oauth_scoped_token")
        return typing.cast(typing.Optional["PagerdutyProviderUseAppOauthScopedToken"], result)

    @builtins.property
    def user_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#user_token PagerdutyProvider#user_token}.'''
        result = self._values.get("user_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PagerdutyProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.provider.PagerdutyProviderUseAppOauthScopedToken",
    jsii_struct_bases=[],
    name_mapping={
        "pd_client_id": "pdClientId",
        "pd_client_secret": "pdClientSecret",
        "pd_subdomain": "pdSubdomain",
    },
)
class PagerdutyProviderUseAppOauthScopedToken:
    def __init__(
        self,
        *,
        pd_client_id: typing.Optional[builtins.str] = None,
        pd_client_secret: typing.Optional[builtins.str] = None,
        pd_subdomain: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pd_client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#pd_client_id PagerdutyProvider#pd_client_id}.
        :param pd_client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#pd_client_secret PagerdutyProvider#pd_client_secret}.
        :param pd_subdomain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#pd_subdomain PagerdutyProvider#pd_subdomain}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__334b7455ce7e77f942b9b1650228793b7612f5b73d90c734c7e266d8df20bee2)
            check_type(argname="argument pd_client_id", value=pd_client_id, expected_type=type_hints["pd_client_id"])
            check_type(argname="argument pd_client_secret", value=pd_client_secret, expected_type=type_hints["pd_client_secret"])
            check_type(argname="argument pd_subdomain", value=pd_subdomain, expected_type=type_hints["pd_subdomain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pd_client_id is not None:
            self._values["pd_client_id"] = pd_client_id
        if pd_client_secret is not None:
            self._values["pd_client_secret"] = pd_client_secret
        if pd_subdomain is not None:
            self._values["pd_subdomain"] = pd_subdomain

    @builtins.property
    def pd_client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#pd_client_id PagerdutyProvider#pd_client_id}.'''
        result = self._values.get("pd_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pd_client_secret(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#pd_client_secret PagerdutyProvider#pd_client_secret}.'''
        result = self._values.get("pd_client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pd_subdomain(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs#pd_subdomain PagerdutyProvider#pd_subdomain}.'''
        result = self._values.get("pd_subdomain")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PagerdutyProviderUseAppOauthScopedToken(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "PagerdutyProvider",
    "PagerdutyProviderConfig",
    "PagerdutyProviderUseAppOauthScopedToken",
]

publication.publish()

def _typecheckingstub__3509512539073bbac9bc9e66d0efe0caaf04a43d2d2d30a6569b117bd193cb4a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alias: typing.Optional[builtins.str] = None,
    api_url_override: typing.Optional[builtins.str] = None,
    insecure_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    service_region: typing.Optional[builtins.str] = None,
    skip_credentials_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    token: typing.Optional[builtins.str] = None,
    use_app_oauth_scoped_token: typing.Optional[typing.Union[PagerdutyProviderUseAppOauthScopedToken, typing.Dict[builtins.str, typing.Any]]] = None,
    user_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602aea9d9d3dbc68d164ba8b94d941795e6af210453222a0ecb39912704f53aa(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab5e1975f1f35ff8003d06ebf251c81aa151b9b3c183802ac9eda99976332d6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b1fa8b4430b3025525c11a441481f604f2d3cb14e8032fb09e75cf5c81901f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e317dff346f42c3f4d8163300830a0a45c34ab4367a8da082b477356ad1065d(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19e068b11155672d909e4a3bb1fb00989fb34e9c4b4dfc2e673f17488dce5cb6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c727215676dfd6aa621a0c0bb4ed4421fd9644cca069f5f743be40b809a939(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec053ae433540bf873d7de07938287a9cc766ca9841a9758ef9eda90d531eb53(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8bbf080914872f5e18998ff71070347e6430ae732ba095db63b05b36c396030(
    value: typing.Optional[PagerdutyProviderUseAppOauthScopedToken],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610f760da361297fbb18811c7be0c5d5b0acf937774f7060f3cb21a92800ee40(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f37403effaf2562475b00ed85353fa25e811a6793d058dc4abb17e4cdf808b0(
    *,
    alias: typing.Optional[builtins.str] = None,
    api_url_override: typing.Optional[builtins.str] = None,
    insecure_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    service_region: typing.Optional[builtins.str] = None,
    skip_credentials_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    token: typing.Optional[builtins.str] = None,
    use_app_oauth_scoped_token: typing.Optional[typing.Union[PagerdutyProviderUseAppOauthScopedToken, typing.Dict[builtins.str, typing.Any]]] = None,
    user_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__334b7455ce7e77f942b9b1650228793b7612f5b73d90c734c7e266d8df20bee2(
    *,
    pd_client_id: typing.Optional[builtins.str] = None,
    pd_client_secret: typing.Optional[builtins.str] = None,
    pd_subdomain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
