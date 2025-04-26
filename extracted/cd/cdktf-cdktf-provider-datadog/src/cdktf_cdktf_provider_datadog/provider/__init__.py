r'''
# `provider`

Refer to the Terraform Registry for docs: [`datadog`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs).
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


class DatadogProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.provider.DatadogProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs datadog}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alias: typing.Optional[builtins.str] = None,
        api_key: typing.Optional[builtins.str] = None,
        api_url: typing.Optional[builtins.str] = None,
        app_key: typing.Optional[builtins.str] = None,
        default_tags: typing.Optional[typing.Union["DatadogProviderDefaultTags", typing.Dict[builtins.str, typing.Any]]] = None,
        http_client_retry_backoff_base: typing.Optional[jsii.Number] = None,
        http_client_retry_backoff_multiplier: typing.Optional[jsii.Number] = None,
        http_client_retry_enabled: typing.Optional[builtins.str] = None,
        http_client_retry_max_retries: typing.Optional[jsii.Number] = None,
        http_client_retry_timeout: typing.Optional[jsii.Number] = None,
        validate: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs datadog} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#alias DatadogProvider#alias}
        :param api_key: (Required unless validate is false) Datadog API key. This can also be set via the DD_API_KEY environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#api_key DatadogProvider#api_key}
        :param api_url: The API URL. This can also be set via the DD_HOST environment variable, and defaults to ``https://api.datadoghq.com``. Note that this URL must not end with the ``/api/`` path. For example, ``https://api.datadoghq.com/`` is a correct value, while ``https://api.datadoghq.com/api/`` is not. And if you're working with "EU" version of Datadog, use ``https://api.datadoghq.eu/``. Other Datadog region examples: ``https://api.us5.datadoghq.com/``, ``https://api.us3.datadoghq.com/`` and ``https://api.ddog-gov.com/``. See https://docs.datadoghq.com/getting_started/site/ for all available regions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#api_url DatadogProvider#api_url}
        :param app_key: (Required unless validate is false) Datadog APP key. This can also be set via the DD_APP_KEY environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#app_key DatadogProvider#app_key}
        :param default_tags: default_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#default_tags DatadogProvider#default_tags}
        :param http_client_retry_backoff_base: The HTTP request retry back off base. Defaults to 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#http_client_retry_backoff_base DatadogProvider#http_client_retry_backoff_base}
        :param http_client_retry_backoff_multiplier: The HTTP request retry back off multiplier. Defaults to 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#http_client_retry_backoff_multiplier DatadogProvider#http_client_retry_backoff_multiplier}
        :param http_client_retry_enabled: Enables request retries on HTTP status codes 429 and 5xx. Valid values are [``true``, ``false``]. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#http_client_retry_enabled DatadogProvider#http_client_retry_enabled}
        :param http_client_retry_max_retries: The HTTP request maximum retry number. Defaults to 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#http_client_retry_max_retries DatadogProvider#http_client_retry_max_retries}
        :param http_client_retry_timeout: The HTTP request retry timeout period. Defaults to 60 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#http_client_retry_timeout DatadogProvider#http_client_retry_timeout}
        :param validate: Enables validation of the provided API key during provider initialization. Valid values are [``true``, ``false``]. Default is true. When false, api_key won't be checked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#validate DatadogProvider#validate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0805d396d4fc3c279b51fac738ada9fac3aa1057e300db07efda8efdcdde344e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DatadogProviderConfig(
            alias=alias,
            api_key=api_key,
            api_url=api_url,
            app_key=app_key,
            default_tags=default_tags,
            http_client_retry_backoff_base=http_client_retry_backoff_base,
            http_client_retry_backoff_multiplier=http_client_retry_backoff_multiplier,
            http_client_retry_enabled=http_client_retry_enabled,
            http_client_retry_max_retries=http_client_retry_max_retries,
            http_client_retry_timeout=http_client_retry_timeout,
            validate=validate,
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
        '''Generates CDKTF code for importing a DatadogProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DatadogProvider to import.
        :param import_from_id: The id of the existing DatadogProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DatadogProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13b95a8515cb284d8ee4d6dcfb65928fe2f2a9633eae09a21f94353541d45660)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetApiKey")
    def reset_api_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiKey", []))

    @jsii.member(jsii_name="resetApiUrl")
    def reset_api_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiUrl", []))

    @jsii.member(jsii_name="resetAppKey")
    def reset_app_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppKey", []))

    @jsii.member(jsii_name="resetDefaultTags")
    def reset_default_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTags", []))

    @jsii.member(jsii_name="resetHttpClientRetryBackoffBase")
    def reset_http_client_retry_backoff_base(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpClientRetryBackoffBase", []))

    @jsii.member(jsii_name="resetHttpClientRetryBackoffMultiplier")
    def reset_http_client_retry_backoff_multiplier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpClientRetryBackoffMultiplier", []))

    @jsii.member(jsii_name="resetHttpClientRetryEnabled")
    def reset_http_client_retry_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpClientRetryEnabled", []))

    @jsii.member(jsii_name="resetHttpClientRetryMaxRetries")
    def reset_http_client_retry_max_retries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpClientRetryMaxRetries", []))

    @jsii.member(jsii_name="resetHttpClientRetryTimeout")
    def reset_http_client_retry_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpClientRetryTimeout", []))

    @jsii.member(jsii_name="resetValidate")
    def reset_validate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidate", []))

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
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="apiUrlInput")
    def api_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="appKeyInput")
    def app_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTagsInput")
    def default_tags_input(self) -> typing.Optional["DatadogProviderDefaultTags"]:
        return typing.cast(typing.Optional["DatadogProviderDefaultTags"], jsii.get(self, "defaultTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="httpClientRetryBackoffBaseInput")
    def http_client_retry_backoff_base_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "httpClientRetryBackoffBaseInput"))

    @builtins.property
    @jsii.member(jsii_name="httpClientRetryBackoffMultiplierInput")
    def http_client_retry_backoff_multiplier_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "httpClientRetryBackoffMultiplierInput"))

    @builtins.property
    @jsii.member(jsii_name="httpClientRetryEnabledInput")
    def http_client_retry_enabled_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpClientRetryEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="httpClientRetryMaxRetriesInput")
    def http_client_retry_max_retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "httpClientRetryMaxRetriesInput"))

    @builtins.property
    @jsii.member(jsii_name="httpClientRetryTimeoutInput")
    def http_client_retry_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "httpClientRetryTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="validateInput")
    def validate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "validateInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41c6a45870fdb947f3ddde847982a16aa4f1f568f90c0090891bcb1ee998ba63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee1caef371827550f1c55b1ba8b19bb96a191d14b34fa991469a985a09dc4e77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiUrl")
    def api_url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiUrl"))

    @api_url.setter
    def api_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e52d452c54d0316f9b9282499928ab8d6656b1d0a66772d66565d0efc2ccfb4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appKey")
    def app_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appKey"))

    @app_key.setter
    def app_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc7f9a1134524ccf17343d743bf37c227cbfb744f6493c0fa0f0b472b5882088)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTags")
    def default_tags(self) -> typing.Optional["DatadogProviderDefaultTags"]:
        return typing.cast(typing.Optional["DatadogProviderDefaultTags"], jsii.get(self, "defaultTags"))

    @default_tags.setter
    def default_tags(
        self,
        value: typing.Optional["DatadogProviderDefaultTags"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9eca878a805993f868794f71fdfb188e7b5193b11e6d1e4877fb042d1194130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpClientRetryBackoffBase")
    def http_client_retry_backoff_base(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "httpClientRetryBackoffBase"))

    @http_client_retry_backoff_base.setter
    def http_client_retry_backoff_base(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52aee4624da24aea1acb1552acce2042bfe7eb8670eef2c1a7f00b77314ac916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpClientRetryBackoffBase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpClientRetryBackoffMultiplier")
    def http_client_retry_backoff_multiplier(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "httpClientRetryBackoffMultiplier"))

    @http_client_retry_backoff_multiplier.setter
    def http_client_retry_backoff_multiplier(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6b79cf228c79ca64f06762c5f536370611bc19c760e1a92bbd54f82ab46e4f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpClientRetryBackoffMultiplier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpClientRetryEnabled")
    def http_client_retry_enabled(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpClientRetryEnabled"))

    @http_client_retry_enabled.setter
    def http_client_retry_enabled(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b21e0d0de23a863bd7a81f5e1da490ba483abf1d7f5fa3ca794043556d49537a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpClientRetryEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpClientRetryMaxRetries")
    def http_client_retry_max_retries(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "httpClientRetryMaxRetries"))

    @http_client_retry_max_retries.setter
    def http_client_retry_max_retries(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c43b2b70794dd23b6193b86230dd086d39a380ffb516505934c1f8ef002f6a95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpClientRetryMaxRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpClientRetryTimeout")
    def http_client_retry_timeout(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "httpClientRetryTimeout"))

    @http_client_retry_timeout.setter
    def http_client_retry_timeout(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__711a4fe27325ad950c40c539b130cfe134e821ab9c2c2e5188263f30f2e2733a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpClientRetryTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validate")
    def validate(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "validate"))

    @validate.setter
    def validate(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85e8d0f8795f2588aedb2c310fb93daff65345b1a56d3fb6f1156b175f757dc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validate", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.provider.DatadogProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "api_key": "apiKey",
        "api_url": "apiUrl",
        "app_key": "appKey",
        "default_tags": "defaultTags",
        "http_client_retry_backoff_base": "httpClientRetryBackoffBase",
        "http_client_retry_backoff_multiplier": "httpClientRetryBackoffMultiplier",
        "http_client_retry_enabled": "httpClientRetryEnabled",
        "http_client_retry_max_retries": "httpClientRetryMaxRetries",
        "http_client_retry_timeout": "httpClientRetryTimeout",
        "validate": "validate",
    },
)
class DatadogProviderConfig:
    def __init__(
        self,
        *,
        alias: typing.Optional[builtins.str] = None,
        api_key: typing.Optional[builtins.str] = None,
        api_url: typing.Optional[builtins.str] = None,
        app_key: typing.Optional[builtins.str] = None,
        default_tags: typing.Optional[typing.Union["DatadogProviderDefaultTags", typing.Dict[builtins.str, typing.Any]]] = None,
        http_client_retry_backoff_base: typing.Optional[jsii.Number] = None,
        http_client_retry_backoff_multiplier: typing.Optional[jsii.Number] = None,
        http_client_retry_enabled: typing.Optional[builtins.str] = None,
        http_client_retry_max_retries: typing.Optional[jsii.Number] = None,
        http_client_retry_timeout: typing.Optional[jsii.Number] = None,
        validate: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#alias DatadogProvider#alias}
        :param api_key: (Required unless validate is false) Datadog API key. This can also be set via the DD_API_KEY environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#api_key DatadogProvider#api_key}
        :param api_url: The API URL. This can also be set via the DD_HOST environment variable, and defaults to ``https://api.datadoghq.com``. Note that this URL must not end with the ``/api/`` path. For example, ``https://api.datadoghq.com/`` is a correct value, while ``https://api.datadoghq.com/api/`` is not. And if you're working with "EU" version of Datadog, use ``https://api.datadoghq.eu/``. Other Datadog region examples: ``https://api.us5.datadoghq.com/``, ``https://api.us3.datadoghq.com/`` and ``https://api.ddog-gov.com/``. See https://docs.datadoghq.com/getting_started/site/ for all available regions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#api_url DatadogProvider#api_url}
        :param app_key: (Required unless validate is false) Datadog APP key. This can also be set via the DD_APP_KEY environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#app_key DatadogProvider#app_key}
        :param default_tags: default_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#default_tags DatadogProvider#default_tags}
        :param http_client_retry_backoff_base: The HTTP request retry back off base. Defaults to 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#http_client_retry_backoff_base DatadogProvider#http_client_retry_backoff_base}
        :param http_client_retry_backoff_multiplier: The HTTP request retry back off multiplier. Defaults to 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#http_client_retry_backoff_multiplier DatadogProvider#http_client_retry_backoff_multiplier}
        :param http_client_retry_enabled: Enables request retries on HTTP status codes 429 and 5xx. Valid values are [``true``, ``false``]. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#http_client_retry_enabled DatadogProvider#http_client_retry_enabled}
        :param http_client_retry_max_retries: The HTTP request maximum retry number. Defaults to 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#http_client_retry_max_retries DatadogProvider#http_client_retry_max_retries}
        :param http_client_retry_timeout: The HTTP request retry timeout period. Defaults to 60 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#http_client_retry_timeout DatadogProvider#http_client_retry_timeout}
        :param validate: Enables validation of the provided API key during provider initialization. Valid values are [``true``, ``false``]. Default is true. When false, api_key won't be checked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#validate DatadogProvider#validate}
        '''
        if isinstance(default_tags, dict):
            default_tags = DatadogProviderDefaultTags(**default_tags)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0627dc31b14e1dd1b33388294ae7ff9183e0249175790cf0444bf682521e659)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument api_url", value=api_url, expected_type=type_hints["api_url"])
            check_type(argname="argument app_key", value=app_key, expected_type=type_hints["app_key"])
            check_type(argname="argument default_tags", value=default_tags, expected_type=type_hints["default_tags"])
            check_type(argname="argument http_client_retry_backoff_base", value=http_client_retry_backoff_base, expected_type=type_hints["http_client_retry_backoff_base"])
            check_type(argname="argument http_client_retry_backoff_multiplier", value=http_client_retry_backoff_multiplier, expected_type=type_hints["http_client_retry_backoff_multiplier"])
            check_type(argname="argument http_client_retry_enabled", value=http_client_retry_enabled, expected_type=type_hints["http_client_retry_enabled"])
            check_type(argname="argument http_client_retry_max_retries", value=http_client_retry_max_retries, expected_type=type_hints["http_client_retry_max_retries"])
            check_type(argname="argument http_client_retry_timeout", value=http_client_retry_timeout, expected_type=type_hints["http_client_retry_timeout"])
            check_type(argname="argument validate", value=validate, expected_type=type_hints["validate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias
        if api_key is not None:
            self._values["api_key"] = api_key
        if api_url is not None:
            self._values["api_url"] = api_url
        if app_key is not None:
            self._values["app_key"] = app_key
        if default_tags is not None:
            self._values["default_tags"] = default_tags
        if http_client_retry_backoff_base is not None:
            self._values["http_client_retry_backoff_base"] = http_client_retry_backoff_base
        if http_client_retry_backoff_multiplier is not None:
            self._values["http_client_retry_backoff_multiplier"] = http_client_retry_backoff_multiplier
        if http_client_retry_enabled is not None:
            self._values["http_client_retry_enabled"] = http_client_retry_enabled
        if http_client_retry_max_retries is not None:
            self._values["http_client_retry_max_retries"] = http_client_retry_max_retries
        if http_client_retry_timeout is not None:
            self._values["http_client_retry_timeout"] = http_client_retry_timeout
        if validate is not None:
            self._values["validate"] = validate

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#alias DatadogProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_key(self) -> typing.Optional[builtins.str]:
        '''(Required unless validate is false) Datadog API key. This can also be set via the DD_API_KEY environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#api_key DatadogProvider#api_key}
        '''
        result = self._values.get("api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_url(self) -> typing.Optional[builtins.str]:
        '''The API URL.

        This can also be set via the DD_HOST environment variable, and defaults to ``https://api.datadoghq.com``. Note that this URL must not end with the ``/api/`` path. For example, ``https://api.datadoghq.com/`` is a correct value, while ``https://api.datadoghq.com/api/`` is not. And if you're working with "EU" version of Datadog, use ``https://api.datadoghq.eu/``. Other Datadog region examples: ``https://api.us5.datadoghq.com/``, ``https://api.us3.datadoghq.com/`` and ``https://api.ddog-gov.com/``. See https://docs.datadoghq.com/getting_started/site/ for all available regions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#api_url DatadogProvider#api_url}
        '''
        result = self._values.get("api_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_key(self) -> typing.Optional[builtins.str]:
        '''(Required unless validate is false) Datadog APP key. This can also be set via the DD_APP_KEY environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#app_key DatadogProvider#app_key}
        '''
        result = self._values.get("app_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_tags(self) -> typing.Optional["DatadogProviderDefaultTags"]:
        '''default_tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#default_tags DatadogProvider#default_tags}
        '''
        result = self._values.get("default_tags")
        return typing.cast(typing.Optional["DatadogProviderDefaultTags"], result)

    @builtins.property
    def http_client_retry_backoff_base(self) -> typing.Optional[jsii.Number]:
        '''The HTTP request retry back off base. Defaults to 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#http_client_retry_backoff_base DatadogProvider#http_client_retry_backoff_base}
        '''
        result = self._values.get("http_client_retry_backoff_base")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def http_client_retry_backoff_multiplier(self) -> typing.Optional[jsii.Number]:
        '''The HTTP request retry back off multiplier. Defaults to 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#http_client_retry_backoff_multiplier DatadogProvider#http_client_retry_backoff_multiplier}
        '''
        result = self._values.get("http_client_retry_backoff_multiplier")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def http_client_retry_enabled(self) -> typing.Optional[builtins.str]:
        '''Enables request retries on HTTP status codes 429 and 5xx. Valid values are [``true``, ``false``]. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#http_client_retry_enabled DatadogProvider#http_client_retry_enabled}
        '''
        result = self._values.get("http_client_retry_enabled")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_client_retry_max_retries(self) -> typing.Optional[jsii.Number]:
        '''The HTTP request maximum retry number. Defaults to 3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#http_client_retry_max_retries DatadogProvider#http_client_retry_max_retries}
        '''
        result = self._values.get("http_client_retry_max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def http_client_retry_timeout(self) -> typing.Optional[jsii.Number]:
        '''The HTTP request retry timeout period. Defaults to 60 seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#http_client_retry_timeout DatadogProvider#http_client_retry_timeout}
        '''
        result = self._values.get("http_client_retry_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def validate(self) -> typing.Optional[builtins.str]:
        '''Enables validation of the provided API key during provider initialization.

        Valid values are [``true``, ``false``]. Default is true. When false, api_key won't be checked.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#validate DatadogProvider#validate}
        '''
        result = self._values.get("validate")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatadogProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.provider.DatadogProviderDefaultTags",
    jsii_struct_bases=[],
    name_mapping={"tags": "tags"},
)
class DatadogProviderDefaultTags:
    def __init__(
        self,
        *,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param tags: [Experimental - Monitors and Logs Pipelines only] Resource tags to be applied by default across all resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#tags DatadogProvider#tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83860b766dd8e9e0d1e1fec6adafd55f4bbab8a2b45778a4061235e98993f5f8)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''[Experimental - Monitors and Logs Pipelines only] Resource tags to be applied by default across all resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs#tags DatadogProvider#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatadogProviderDefaultTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DatadogProvider",
    "DatadogProviderConfig",
    "DatadogProviderDefaultTags",
]

publication.publish()

def _typecheckingstub__0805d396d4fc3c279b51fac738ada9fac3aa1057e300db07efda8efdcdde344e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alias: typing.Optional[builtins.str] = None,
    api_key: typing.Optional[builtins.str] = None,
    api_url: typing.Optional[builtins.str] = None,
    app_key: typing.Optional[builtins.str] = None,
    default_tags: typing.Optional[typing.Union[DatadogProviderDefaultTags, typing.Dict[builtins.str, typing.Any]]] = None,
    http_client_retry_backoff_base: typing.Optional[jsii.Number] = None,
    http_client_retry_backoff_multiplier: typing.Optional[jsii.Number] = None,
    http_client_retry_enabled: typing.Optional[builtins.str] = None,
    http_client_retry_max_retries: typing.Optional[jsii.Number] = None,
    http_client_retry_timeout: typing.Optional[jsii.Number] = None,
    validate: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13b95a8515cb284d8ee4d6dcfb65928fe2f2a9633eae09a21f94353541d45660(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c6a45870fdb947f3ddde847982a16aa4f1f568f90c0090891bcb1ee998ba63(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee1caef371827550f1c55b1ba8b19bb96a191d14b34fa991469a985a09dc4e77(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e52d452c54d0316f9b9282499928ab8d6656b1d0a66772d66565d0efc2ccfb4f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7f9a1134524ccf17343d743bf37c227cbfb744f6493c0fa0f0b472b5882088(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9eca878a805993f868794f71fdfb188e7b5193b11e6d1e4877fb042d1194130(
    value: typing.Optional[DatadogProviderDefaultTags],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52aee4624da24aea1acb1552acce2042bfe7eb8670eef2c1a7f00b77314ac916(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b79cf228c79ca64f06762c5f536370611bc19c760e1a92bbd54f82ab46e4f4(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21e0d0de23a863bd7a81f5e1da490ba483abf1d7f5fa3ca794043556d49537a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c43b2b70794dd23b6193b86230dd086d39a380ffb516505934c1f8ef002f6a95(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__711a4fe27325ad950c40c539b130cfe134e821ab9c2c2e5188263f30f2e2733a(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e8d0f8795f2588aedb2c310fb93daff65345b1a56d3fb6f1156b175f757dc7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0627dc31b14e1dd1b33388294ae7ff9183e0249175790cf0444bf682521e659(
    *,
    alias: typing.Optional[builtins.str] = None,
    api_key: typing.Optional[builtins.str] = None,
    api_url: typing.Optional[builtins.str] = None,
    app_key: typing.Optional[builtins.str] = None,
    default_tags: typing.Optional[typing.Union[DatadogProviderDefaultTags, typing.Dict[builtins.str, typing.Any]]] = None,
    http_client_retry_backoff_base: typing.Optional[jsii.Number] = None,
    http_client_retry_backoff_multiplier: typing.Optional[jsii.Number] = None,
    http_client_retry_enabled: typing.Optional[builtins.str] = None,
    http_client_retry_max_retries: typing.Optional[jsii.Number] = None,
    http_client_retry_timeout: typing.Optional[jsii.Number] = None,
    validate: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83860b766dd8e9e0d1e1fec6adafd55f4bbab8a2b45778a4061235e98993f5f8(
    *,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
