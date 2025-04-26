r'''
# `snowflake_api_authentication_integration_with_client_credentials`

Refer to the Terraform Registry for docs: [`snowflake_api_authentication_integration_with_client_credentials`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials).
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


class ApiAuthenticationIntegrationWithClientCredentials(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentials",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials snowflake_api_authentication_integration_with_client_credentials}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        oauth_client_id: builtins.str,
        oauth_client_secret: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        oauth_access_token_validity: typing.Optional[jsii.Number] = None,
        oauth_allowed_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        oauth_client_auth_method: typing.Optional[builtins.str] = None,
        oauth_refresh_token_validity: typing.Optional[jsii.Number] = None,
        oauth_token_endpoint: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials snowflake_api_authentication_integration_with_client_credentials} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param enabled: Specifies whether this security integration is enabled or disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#enabled ApiAuthenticationIntegrationWithClientCredentials#enabled}
        :param name: Specifies the identifier (i.e. name) for the integration. This value must be unique in your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#name ApiAuthenticationIntegrationWithClientCredentials#name}
        :param oauth_client_id: Specifies the client ID for the OAuth application in the external service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#oauth_client_id ApiAuthenticationIntegrationWithClientCredentials#oauth_client_id}
        :param oauth_client_secret: Specifies the client secret for the OAuth application in the ServiceNow instance from the previous step. The connector uses this to request an access token from the ServiceNow instance. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#oauth_client_secret ApiAuthenticationIntegrationWithClientCredentials#oauth_client_secret}
        :param comment: Specifies a comment for the integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#comment ApiAuthenticationIntegrationWithClientCredentials#comment}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#id ApiAuthenticationIntegrationWithClientCredentials#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param oauth_access_token_validity: Specifies the default lifetime of the OAuth access token (in seconds) issued by an OAuth server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#oauth_access_token_validity ApiAuthenticationIntegrationWithClientCredentials#oauth_access_token_validity}
        :param oauth_allowed_scopes: Specifies a list of scopes to use when making a request from the OAuth by a role with USAGE on the integration during the OAuth client credentials flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#oauth_allowed_scopes ApiAuthenticationIntegrationWithClientCredentials#oauth_allowed_scopes}
        :param oauth_client_auth_method: Specifies that POST is used as the authentication method to the external service. If removed from the config, the resource is recreated. Valid values are (case-insensitive): ``CLIENT_SECRET_POST``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#oauth_client_auth_method ApiAuthenticationIntegrationWithClientCredentials#oauth_client_auth_method}
        :param oauth_refresh_token_validity: Specifies the value to determine the validity of the refresh token obtained from the OAuth server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#oauth_refresh_token_validity ApiAuthenticationIntegrationWithClientCredentials#oauth_refresh_token_validity}
        :param oauth_token_endpoint: Specifies the token endpoint used by the client to obtain an access token by presenting its authorization grant or refresh token. The token endpoint is used with every authorization grant except for the implicit grant type (since an access token is issued directly). If removed from the config, the resource is recreated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#oauth_token_endpoint ApiAuthenticationIntegrationWithClientCredentials#oauth_token_endpoint}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25e22f5a68ec2f32ee1644ebc6a1ef8d77c014c1d29e5805b3248f983cb54674)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApiAuthenticationIntegrationWithClientCredentialsConfig(
            enabled=enabled,
            name=name,
            oauth_client_id=oauth_client_id,
            oauth_client_secret=oauth_client_secret,
            comment=comment,
            id=id,
            oauth_access_token_validity=oauth_access_token_validity,
            oauth_allowed_scopes=oauth_allowed_scopes,
            oauth_client_auth_method=oauth_client_auth_method,
            oauth_refresh_token_validity=oauth_refresh_token_validity,
            oauth_token_endpoint=oauth_token_endpoint,
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
        '''Generates CDKTF code for importing a ApiAuthenticationIntegrationWithClientCredentials resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApiAuthenticationIntegrationWithClientCredentials to import.
        :param import_from_id: The id of the existing ApiAuthenticationIntegrationWithClientCredentials that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApiAuthenticationIntegrationWithClientCredentials to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaca6126a741b68cefd98d37d0db1e793e56bd2ba7a701f6c7a8ee178b7650d5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOauthAccessTokenValidity")
    def reset_oauth_access_token_validity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthAccessTokenValidity", []))

    @jsii.member(jsii_name="resetOauthAllowedScopes")
    def reset_oauth_allowed_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthAllowedScopes", []))

    @jsii.member(jsii_name="resetOauthClientAuthMethod")
    def reset_oauth_client_auth_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthClientAuthMethod", []))

    @jsii.member(jsii_name="resetOauthRefreshTokenValidity")
    def reset_oauth_refresh_token_validity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthRefreshTokenValidity", []))

    @jsii.member(jsii_name="resetOauthTokenEndpoint")
    def reset_oauth_token_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthTokenEndpoint", []))

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
    @jsii.member(jsii_name="describeOutput")
    def describe_output(
        self,
    ) -> "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputList":
        return typing.cast("ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputList", jsii.get(self, "describeOutput"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(
        self,
    ) -> "ApiAuthenticationIntegrationWithClientCredentialsShowOutputList":
        return typing.cast("ApiAuthenticationIntegrationWithClientCredentialsShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthAccessTokenValidityInput")
    def oauth_access_token_validity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "oauthAccessTokenValidityInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthAllowedScopesInput")
    def oauth_allowed_scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "oauthAllowedScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientAuthMethodInput")
    def oauth_client_auth_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthClientAuthMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientIdInput")
    def oauth_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientSecretInput")
    def oauth_client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthClientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthRefreshTokenValidityInput")
    def oauth_refresh_token_validity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "oauthRefreshTokenValidityInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthTokenEndpointInput")
    def oauth_token_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthTokenEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9e17b9ff01f640af83e8a42f73f780a1ea0b1543026f658e802bc38337fda05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__98216723c60354ef39ec4b7da52946a7224b323f143fc2b6c18ef9004c64fe8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a5dd559b26988e347700bd7ca2e4064e89e6d24084ed39ed6dbfc3132fe5b24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__506e4d3d8f1a0c4678b0f43856342e0d0b0fbce0d9771339956bb2fbef0cd598)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthAccessTokenValidity")
    def oauth_access_token_validity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "oauthAccessTokenValidity"))

    @oauth_access_token_validity.setter
    def oauth_access_token_validity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9818cda6aa0cb8c4d9fa111f589f72e99e88ed09922f53f24c3a9b27a2d1e997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthAccessTokenValidity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthAllowedScopes")
    def oauth_allowed_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthAllowedScopes"))

    @oauth_allowed_scopes.setter
    def oauth_allowed_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6a5c4ee0296090f338749fcc62965bd7b6e7fec87eeba1de9bbb846f5f79129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthAllowedScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthClientAuthMethod")
    def oauth_client_auth_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthClientAuthMethod"))

    @oauth_client_auth_method.setter
    def oauth_client_auth_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff637710f60b1284f00353fa8d32ef92e0748cff209fd3b98100f3648c2ca98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthClientAuthMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthClientId")
    def oauth_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthClientId"))

    @oauth_client_id.setter
    def oauth_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d39f6c6fc847b239fe5a2d194505bd730dfc82ebe95d0dbabaaf4dada41dea4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthClientSecret")
    def oauth_client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthClientSecret"))

    @oauth_client_secret.setter
    def oauth_client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d386994f515da9cf6f880a95a0413e8556074f1d5e89b0db4711026fde9c277)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthClientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthRefreshTokenValidity")
    def oauth_refresh_token_validity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "oauthRefreshTokenValidity"))

    @oauth_refresh_token_validity.setter
    def oauth_refresh_token_validity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e050cbb14713ae33e69226a76dcfd6e5769fa26de1d06d83ee5d0f23aa5775ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthRefreshTokenValidity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthTokenEndpoint")
    def oauth_token_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthTokenEndpoint"))

    @oauth_token_endpoint.setter
    def oauth_token_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f91d39ad712a6d871493d6c0326d6307ecbe74f0480765301584451e646c2d68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthTokenEndpoint", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "enabled": "enabled",
        "name": "name",
        "oauth_client_id": "oauthClientId",
        "oauth_client_secret": "oauthClientSecret",
        "comment": "comment",
        "id": "id",
        "oauth_access_token_validity": "oauthAccessTokenValidity",
        "oauth_allowed_scopes": "oauthAllowedScopes",
        "oauth_client_auth_method": "oauthClientAuthMethod",
        "oauth_refresh_token_validity": "oauthRefreshTokenValidity",
        "oauth_token_endpoint": "oauthTokenEndpoint",
    },
)
class ApiAuthenticationIntegrationWithClientCredentialsConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        oauth_client_id: builtins.str,
        oauth_client_secret: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        oauth_access_token_validity: typing.Optional[jsii.Number] = None,
        oauth_allowed_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        oauth_client_auth_method: typing.Optional[builtins.str] = None,
        oauth_refresh_token_validity: typing.Optional[jsii.Number] = None,
        oauth_token_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param enabled: Specifies whether this security integration is enabled or disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#enabled ApiAuthenticationIntegrationWithClientCredentials#enabled}
        :param name: Specifies the identifier (i.e. name) for the integration. This value must be unique in your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#name ApiAuthenticationIntegrationWithClientCredentials#name}
        :param oauth_client_id: Specifies the client ID for the OAuth application in the external service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#oauth_client_id ApiAuthenticationIntegrationWithClientCredentials#oauth_client_id}
        :param oauth_client_secret: Specifies the client secret for the OAuth application in the ServiceNow instance from the previous step. The connector uses this to request an access token from the ServiceNow instance. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#oauth_client_secret ApiAuthenticationIntegrationWithClientCredentials#oauth_client_secret}
        :param comment: Specifies a comment for the integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#comment ApiAuthenticationIntegrationWithClientCredentials#comment}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#id ApiAuthenticationIntegrationWithClientCredentials#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param oauth_access_token_validity: Specifies the default lifetime of the OAuth access token (in seconds) issued by an OAuth server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#oauth_access_token_validity ApiAuthenticationIntegrationWithClientCredentials#oauth_access_token_validity}
        :param oauth_allowed_scopes: Specifies a list of scopes to use when making a request from the OAuth by a role with USAGE on the integration during the OAuth client credentials flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#oauth_allowed_scopes ApiAuthenticationIntegrationWithClientCredentials#oauth_allowed_scopes}
        :param oauth_client_auth_method: Specifies that POST is used as the authentication method to the external service. If removed from the config, the resource is recreated. Valid values are (case-insensitive): ``CLIENT_SECRET_POST``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#oauth_client_auth_method ApiAuthenticationIntegrationWithClientCredentials#oauth_client_auth_method}
        :param oauth_refresh_token_validity: Specifies the value to determine the validity of the refresh token obtained from the OAuth server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#oauth_refresh_token_validity ApiAuthenticationIntegrationWithClientCredentials#oauth_refresh_token_validity}
        :param oauth_token_endpoint: Specifies the token endpoint used by the client to obtain an access token by presenting its authorization grant or refresh token. The token endpoint is used with every authorization grant except for the implicit grant type (since an access token is issued directly). If removed from the config, the resource is recreated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#oauth_token_endpoint ApiAuthenticationIntegrationWithClientCredentials#oauth_token_endpoint}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__474863c3f49624a9b759fadbe50278e3b882360af115f020af32caa92c7cbf41)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument oauth_client_id", value=oauth_client_id, expected_type=type_hints["oauth_client_id"])
            check_type(argname="argument oauth_client_secret", value=oauth_client_secret, expected_type=type_hints["oauth_client_secret"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument oauth_access_token_validity", value=oauth_access_token_validity, expected_type=type_hints["oauth_access_token_validity"])
            check_type(argname="argument oauth_allowed_scopes", value=oauth_allowed_scopes, expected_type=type_hints["oauth_allowed_scopes"])
            check_type(argname="argument oauth_client_auth_method", value=oauth_client_auth_method, expected_type=type_hints["oauth_client_auth_method"])
            check_type(argname="argument oauth_refresh_token_validity", value=oauth_refresh_token_validity, expected_type=type_hints["oauth_refresh_token_validity"])
            check_type(argname="argument oauth_token_endpoint", value=oauth_token_endpoint, expected_type=type_hints["oauth_token_endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "name": name,
            "oauth_client_id": oauth_client_id,
            "oauth_client_secret": oauth_client_secret,
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
        if comment is not None:
            self._values["comment"] = comment
        if id is not None:
            self._values["id"] = id
        if oauth_access_token_validity is not None:
            self._values["oauth_access_token_validity"] = oauth_access_token_validity
        if oauth_allowed_scopes is not None:
            self._values["oauth_allowed_scopes"] = oauth_allowed_scopes
        if oauth_client_auth_method is not None:
            self._values["oauth_client_auth_method"] = oauth_client_auth_method
        if oauth_refresh_token_validity is not None:
            self._values["oauth_refresh_token_validity"] = oauth_refresh_token_validity
        if oauth_token_endpoint is not None:
            self._values["oauth_token_endpoint"] = oauth_token_endpoint

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
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Specifies whether this security integration is enabled or disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#enabled ApiAuthenticationIntegrationWithClientCredentials#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the identifier (i.e. name) for the integration. This value must be unique in your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#name ApiAuthenticationIntegrationWithClientCredentials#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oauth_client_id(self) -> builtins.str:
        '''Specifies the client ID for the OAuth application in the external service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#oauth_client_id ApiAuthenticationIntegrationWithClientCredentials#oauth_client_id}
        '''
        result = self._values.get("oauth_client_id")
        assert result is not None, "Required property 'oauth_client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oauth_client_secret(self) -> builtins.str:
        '''Specifies the client secret for the OAuth application in the ServiceNow instance from the previous step.

        The connector uses this to request an access token from the ServiceNow instance. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#oauth_client_secret ApiAuthenticationIntegrationWithClientCredentials#oauth_client_secret}
        '''
        result = self._values.get("oauth_client_secret")
        assert result is not None, "Required property 'oauth_client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the integration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#comment ApiAuthenticationIntegrationWithClientCredentials#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#id ApiAuthenticationIntegrationWithClientCredentials#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_access_token_validity(self) -> typing.Optional[jsii.Number]:
        '''Specifies the default lifetime of the OAuth access token (in seconds) issued by an OAuth server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#oauth_access_token_validity ApiAuthenticationIntegrationWithClientCredentials#oauth_access_token_validity}
        '''
        result = self._values.get("oauth_access_token_validity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def oauth_allowed_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of scopes to use when making a request from the OAuth by a role with USAGE on the integration during the OAuth client credentials flow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#oauth_allowed_scopes ApiAuthenticationIntegrationWithClientCredentials#oauth_allowed_scopes}
        '''
        result = self._values.get("oauth_allowed_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def oauth_client_auth_method(self) -> typing.Optional[builtins.str]:
        '''Specifies that POST is used as the authentication method to the external service.

        If removed from the config, the resource is recreated. Valid values are (case-insensitive): ``CLIENT_SECRET_POST``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#oauth_client_auth_method ApiAuthenticationIntegrationWithClientCredentials#oauth_client_auth_method}
        '''
        result = self._values.get("oauth_client_auth_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_refresh_token_validity(self) -> typing.Optional[jsii.Number]:
        '''Specifies the value to determine the validity of the refresh token obtained from the OAuth server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#oauth_refresh_token_validity ApiAuthenticationIntegrationWithClientCredentials#oauth_refresh_token_validity}
        '''
        result = self._values.get("oauth_refresh_token_validity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def oauth_token_endpoint(self) -> typing.Optional[builtins.str]:
        '''Specifies the token endpoint used by the client to obtain an access token by presenting its authorization grant or refresh token.

        The token endpoint is used with every authorization grant except for the implicit grant type (since an access token is issued directly). If removed from the config, the resource is recreated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_client_credentials#oauth_token_endpoint ApiAuthenticationIntegrationWithClientCredentials#oauth_token_endpoint}
        '''
        result = self._values.get("oauth_token_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithClientCredentialsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputAuthType",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputAuthType:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputAuthType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputAuthTypeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputAuthTypeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f353f4d0617a589aca4c2e7091dc70df21f5d79ad2c303601e69aa9f9f8e13f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputAuthTypeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e0b64190aec85ef8e7a0eb325914655fc5b44e8fc67c3954fbd2ca63ac49eb3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputAuthTypeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d308a21462ba88c8eefa029b85fd7c91e1067cf6fbe5e5293d1845876d222e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23ee09c8e2c9d3bb71e37ebe520652e63fe44b689b15d534af122cb97a3d50d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb69ba3c71aed7c1ed7e7a0f7eb33aa11c1af5ac5307e0d0f75ca334693d8752)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputAuthTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputAuthTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a13d2866638e9261db687b866c2c7c60e5bd207402093a463abdf4217784083)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputAuthType]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputAuthType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputAuthType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29b3710686fe13be691a833bc23ea5b5364367ad136601d2348ae5bf57ccd7b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputComment",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputComment:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputComment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputCommentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputCommentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__986a9874f2474fc895e05e343ffbd0272e48405ed1c75d0b8871114a82eade94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputCommentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__809b491d526c833820f0552b2417b26dd8c19e6fd3450e86bc8512e0f6658fc1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputCommentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32d2589c651889ccd676959070b7799cc32e245fd936705b9aca99626032f27a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58b1fe5770d660bbb08af6a2d3baa062849dd12350c7a9cdcc62fe6a9029fc8d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__311bcaab23c769b8b9394fbec49ed277ce08ec1fcc0c19f24c423dd7fd1e3cd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputCommentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputCommentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cd9a8e7af24371c336da3f0110f841aced2a7d264635d4a18a3fbef6118f62b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputComment]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputComment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputComment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d8cb03d63abcb143cb6f11109ab1f5824a693e919730cbcedf7245167e635e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputEnabled",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputEnabled:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputEnabled(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputEnabledList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputEnabledList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c01c94d6ec4d027d9205d3f304c7e76bb542ba4a53ff8ab036f5e3aa8a35f313)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputEnabledOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f03f50c8b65ce23c8661b2d2455f261a5d030f8ec01407b8112d904af05ef5d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputEnabledOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572fb06f7e61e35ec9adaff2021e1ae826e17c54098dd4c6fc6ead50ffad4f2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0410d9cda122f8fcb0cac3dc6263ba9af5b6d857e6946d5564525a271016135)
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
            type_hints = typing.get_type_hints(_typecheckingstub__686cc6a441df531dbaaef9541ec5fe497b61294c1ffbddf1e2d305dc9cf92057)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputEnabledOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputEnabledOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1a69f6ea5115f21e3be0d26827b4d102a3d31197a599c718b49981479616c7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputEnabled]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputEnabled], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputEnabled],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30b318d8dbfd47804fb85ff375d6222da1f7377e887fd380adce1f7297bcecd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77aa62829614cb696d4d4ad936f5f012939a78dc76df8f18b0e65a1f6805a95f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6acedd6e28f46bd3547ce93f20cb800356e6aed66b42933addcb8f430e2613a0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__030edd04d46b511fed8377b890c2742b296dd4ed4ceaedf8343a15284ba0670d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e376ebedc1fe022e5352d93b4c8cf6b59de2554cf35921752b53e3db3436503e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__919c32ec64b9384d6340568c9671ed571b32d012af009f134736b2361a1392a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAccessTokenValidity",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAccessTokenValidity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAccessTokenValidity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAccessTokenValidityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAccessTokenValidityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34a16fffce84dad00c8124ea850a76d40c777c6b53215858364150029b275382)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAccessTokenValidityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39afc75d44fa01fdef50353bd3fcc88e341a239aa70997fafea91889cdf9c1f6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAccessTokenValidityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05272b3087de8f5e83f63dbf25cf54d15feb1c3dad07747f5aedc400f4b36a8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb02868926d1aca422f79150fa4676337f7ce7bc077bbbe51102ab8ee7a315dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2856e6a64969d2d0275362dbc3d78bc4529e2867186c28463aa0bc717ff501c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAccessTokenValidityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAccessTokenValidityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63c3f06a23b72402e80a282f47fb568e5b84b665712132d63a39ff144b9d1ff7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAccessTokenValidity]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAccessTokenValidity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAccessTokenValidity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4794692b5e7a4ca8da4fde1268979a70b3e8e353ddd5acf5c52dc4f781e59c9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAllowedScopes",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAllowedScopes:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAllowedScopes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAllowedScopesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAllowedScopesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f6e9a0f757a0ad875d5998b9e320b60b00c1cc1304abe95e96148b8a5f17498)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAllowedScopesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6dbe7afe4be528380ab54ca72156be2b8e7dc77bf5b4b7666c61d0eff9982dc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAllowedScopesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__380131e293c4206a288806d871b306efed34e176e502ac23047e353b1c8ad8d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fbf1d1f37ec8879774f2418c8265c5ebaf522226a5eb589bb4e1fd93be7f481)
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
            type_hints = typing.get_type_hints(_typecheckingstub__569a655d7cf6701e20ff9300f0fc98a0bd0e4cf1dccff3b3ccd27b30b60a6618)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAllowedScopesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAllowedScopesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81b5357f4525ffb1e80b53ed68c64154eb877f571d058eb5d3867c71aa22d1d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAllowedScopes]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAllowedScopes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAllowedScopes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85813a3ae2789aa9a78a77f020af6d415f60653ebe8b4c46ceed1fabe2032b3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAuthorizationEndpoint",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAuthorizationEndpoint:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAuthorizationEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAuthorizationEndpointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAuthorizationEndpointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc24b1f62e3086481be20385c5d7d64f030c7618d94bb18c0e9af31b372746e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAuthorizationEndpointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce9aa815ebbb893323e14c65441aff334d91397b363f5566c2b41b336c604511)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAuthorizationEndpointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a79aacc958a03564a5284dd504e45ccf2ba4f88ba68dea3761afd179f864bb94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48da05bc4473c3d8a1e5cc146bed6f87794a7b2d997f9dd39a7f4ab873041626)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f988b1ffc0195506751bd7f4defd87e50b298dbe791a5f7b85feda4370ee6b21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAuthorizationEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAuthorizationEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2bc84ac71d19a0d1cb0ae495767a4f4a082b28e621f66a03243d9ebef221bc0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAuthorizationEndpoint]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAuthorizationEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAuthorizationEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a80157b52a140a3d35f08892dba3328f093c007a2fcaec00f34fd1501cd7613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientAuthMethod",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientAuthMethod:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientAuthMethod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientAuthMethodList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientAuthMethodList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ffc3ca492743893cea4f6ed240e0eb0aa05e10ee8690f40a82a121944ff8c33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientAuthMethodOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1706cdf46516c0f228de1b434c418ed9d19ae2313986cb202c7782cb702d6632)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientAuthMethodOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b2925f5fbe9c4f6838ce0d9f9c59e7d4466adcea2ab1818c53a97dfb77f66b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b220d39a143183a448871b6542b1edc382861bc6554b52c8f6557a5fad501557)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7eab3f660b7f188c006112c59e62f447274ae97066a442cb762fa260ad6bcf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientAuthMethodOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientAuthMethodOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad60561290fa1e53f5d5da47db6b7c4dc98978ba138e34bc0116f23686f584d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientAuthMethod]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientAuthMethod], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientAuthMethod],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__665fe2a025de696e8c65263733ba12e7be6544cc626de1b6aa5df091fea891f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientId",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientId:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientIdList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientIdList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c22eea157edec5ef07fffe6d057a3fdb14ef20d11e102dff072c4780a98f210)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientIdOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a50f4b11384f98b47054b7f15594c9cabb83a5dde70dfda1bc0ac924e890178)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientIdOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e3a90e21c60b1c062c13ddf7624c9ff06f41e2777a6a4a9d77879f49bdf0287)
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
            type_hints = typing.get_type_hints(_typecheckingstub__950223a76ae8852aad07add0be6b93f0964139e49dd93444c7363e8c6e4d4ee3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91f7a60f7c024a74140b28369d1457186abe20507557c82f8edd6510d722dbf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e117c764138c9797dad6fb4109d1070f1944d94e272d868e933cf1bdd9f322a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientId]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__079296c4c639871e4c2b39124e6ba637018cbfc6b9de3544224895be5a4739c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthGrant",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthGrant:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthGrant(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthGrantList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthGrantList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f5cee2616352d7c7bb8ed0a4f847744d81168a2648801ff7c5d14f2a709c7bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthGrantOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d9cfa3b456fd99557992a0417981c7a61b70f265c967022cbbbab8137d42dec)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthGrantOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5085409dfaa04f9efed8b6ae9ba0bf6eb52b02fa6c9f2dcfa694e8e8553b13b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__382e8554808463bc6cb1dd8d8fe790ebc582ae5c95757dcce532d302900c336b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c72fb1bde553fc0dcce7831288592784dc5c709ca32a0b39c19e68c0f851db1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthGrantOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthGrantOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbc7e57d022d55b301870d387125df493b039f0ef923d30a56098d2b2e5896d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthGrant]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthGrant], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthGrant],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecc78d699f701839ace2da7642ea578dd8912dda2a5e74335918e3d5666f97b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthRefreshTokenValidity",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthRefreshTokenValidity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthRefreshTokenValidity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthRefreshTokenValidityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthRefreshTokenValidityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36d19f3d2c9be68474199213dbc6dc2e913581ed23fbe9d4827c95bee9173afb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthRefreshTokenValidityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a2c372cb5019dca75759770007bf0b815ba9cb6da7ffe73144a4e1547198bef)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthRefreshTokenValidityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7de0e6f22170b4325066756e6e8e10d4227ea0e0d9eb7de7917ff362d66153ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29c1f1054b20c0b22114f2f3d822d8f61e2fa4c5ca8080a165a5de0b9be24049)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8907c5bf7b3b4fa1f9e6e287768e890d479904c9b11fee79ed85cf8eda82e7eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthRefreshTokenValidityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthRefreshTokenValidityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07b423aee48ddecb33bc4cae03652742a301e331d7009385d104ded2d37c9206)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthRefreshTokenValidity]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthRefreshTokenValidity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthRefreshTokenValidity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__456e023cb6d4feb08cc10913e75f1ec212004c156f70dd7ebfd91d4043a6c038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthTokenEndpoint",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthTokenEndpoint:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthTokenEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthTokenEndpointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthTokenEndpointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a87463daf400387bb02ae5729ae30ffc545dcc75e3bb333ebab048f2e5970d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthTokenEndpointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02987b36579f3292766d17533fb2e5aa500139e28493351a12dc481a30508dc3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthTokenEndpointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe9c2c95e260f9363231dc202e9e2e2f7ce7212919a579ae0153b66d87602357)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61cc7118d8bae4d59a76a9470b391574da6a8ef67c27dd1d96dce162b1d27e77)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a28c0580fe7493c5df9a44604c381c86419fc2d1813fd6a100aee4aa19be0fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthTokenEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthTokenEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__321b9814df0e36e8854d33db31e8ee403f1577432a07a50568556917dc695eec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthTokenEndpoint]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthTokenEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthTokenEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a632f8f7b3748ebda2b95d5e552afcacba41980e21f0272f2e15700ed8a81886)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bf8cc1ab2f6798e9fa60617c4368c0b2aad6218be48deae8f09421aa4f2c7c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(
        self,
    ) -> ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputAuthTypeList:
        return typing.cast(ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputAuthTypeList, jsii.get(self, "authType"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(
        self,
    ) -> ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputCommentList:
        return typing.cast(ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputCommentList, jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputEnabledList:
        return typing.cast(ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputEnabledList, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="oauthAccessTokenValidity")
    def oauth_access_token_validity(
        self,
    ) -> ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAccessTokenValidityList:
        return typing.cast(ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAccessTokenValidityList, jsii.get(self, "oauthAccessTokenValidity"))

    @builtins.property
    @jsii.member(jsii_name="oauthAllowedScopes")
    def oauth_allowed_scopes(
        self,
    ) -> ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAllowedScopesList:
        return typing.cast(ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAllowedScopesList, jsii.get(self, "oauthAllowedScopes"))

    @builtins.property
    @jsii.member(jsii_name="oauthAuthorizationEndpoint")
    def oauth_authorization_endpoint(
        self,
    ) -> ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAuthorizationEndpointList:
        return typing.cast(ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAuthorizationEndpointList, jsii.get(self, "oauthAuthorizationEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientAuthMethod")
    def oauth_client_auth_method(
        self,
    ) -> ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientAuthMethodList:
        return typing.cast(ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientAuthMethodList, jsii.get(self, "oauthClientAuthMethod"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientId")
    def oauth_client_id(
        self,
    ) -> ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientIdList:
        return typing.cast(ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientIdList, jsii.get(self, "oauthClientId"))

    @builtins.property
    @jsii.member(jsii_name="oauthGrant")
    def oauth_grant(
        self,
    ) -> ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthGrantList:
        return typing.cast(ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthGrantList, jsii.get(self, "oauthGrant"))

    @builtins.property
    @jsii.member(jsii_name="oauthRefreshTokenValidity")
    def oauth_refresh_token_validity(
        self,
    ) -> ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthRefreshTokenValidityList:
        return typing.cast(ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthRefreshTokenValidityList, jsii.get(self, "oauthRefreshTokenValidity"))

    @builtins.property
    @jsii.member(jsii_name="oauthTokenEndpoint")
    def oauth_token_endpoint(
        self,
    ) -> ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthTokenEndpointList:
        return typing.cast(ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthTokenEndpointList, jsii.get(self, "oauthTokenEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="parentIntegration")
    def parent_integration(
        self,
    ) -> "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputParentIntegrationList":
        return typing.cast("ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputParentIntegrationList", jsii.get(self, "parentIntegration"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutput]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dec3e6723747444baf87cbf3a2acfdc2c225f78d87040be93246277dc46de15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputParentIntegration",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputParentIntegration:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputParentIntegration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputParentIntegrationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputParentIntegrationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79d6814dca1f0eef60d5475386eb0c41dd2b042b8bf71be036e2ba7f7a4b6feb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputParentIntegrationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb5341afbbe6cd2218fb66f87306d90ad419837dc461aacb0a4416750c877d84)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputParentIntegrationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c6b8d1e5f6a5ca00b1faae1276005763858fcfedc387554aab513be5f983f8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06f989c636486151798c687d014f29e389a9e2dfec54b735914d8f9ad07a3196)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77f4687b5c0e44a2ab4810eec147b6d19bed9ca5e7d2500cbde735e12e60cdc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputParentIntegrationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputParentIntegrationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a9c6af01b91b4b3459e31bcfb06f22ccff70a139978775b6ca7a46e7fbf3701)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputParentIntegration]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputParentIntegration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputParentIntegration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__176b3bb444e8b06467dd94e76ca6b07c65a073453d26cbaa95f29ed7579668bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithClientCredentialsShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithClientCredentialsShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithClientCredentialsShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ee8232036ea31ae0e642e6b6572fdea52882cb752b911d6348bb21eedaee9a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithClientCredentialsShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9f91593a53b193079cdbdeb3ae91eed3cadd86ab5eb6cd6b03b93239a2e7934)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithClientCredentialsShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55d4d5548ff7592fe83322d43ed1c69c342cb7ead0f084e9b3d83472e60a8eae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9baf8c2d0d5b65d1714973931ba4260d29d34a1975f08076ed1d7277c233868)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31468a89438edf8cb3a419e47bda9f4e9c60c5b84ef8991c5b9ee8fb91a7d74e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithClientCredentialsShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithClientCredentials.ApiAuthenticationIntegrationWithClientCredentialsShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__045ee71c4d23623852516b483cfd53d0c11f0a13dfbbd47f7516ead524f2ec32)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="integrationType")
    def integration_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "integrationType"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsShowOutput]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsShowOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a1bd3560aebc0c3d86ee66ef6b0e42b508c1341cf7be7d4cbc3a1898e7171d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApiAuthenticationIntegrationWithClientCredentials",
    "ApiAuthenticationIntegrationWithClientCredentialsConfig",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutput",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputAuthType",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputAuthTypeList",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputAuthTypeOutputReference",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputComment",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputCommentList",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputCommentOutputReference",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputEnabled",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputEnabledList",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputEnabledOutputReference",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputList",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAccessTokenValidity",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAccessTokenValidityList",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAccessTokenValidityOutputReference",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAllowedScopes",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAllowedScopesList",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAllowedScopesOutputReference",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAuthorizationEndpoint",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAuthorizationEndpointList",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAuthorizationEndpointOutputReference",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientAuthMethod",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientAuthMethodList",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientAuthMethodOutputReference",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientId",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientIdList",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientIdOutputReference",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthGrant",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthGrantList",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthGrantOutputReference",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthRefreshTokenValidity",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthRefreshTokenValidityList",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthRefreshTokenValidityOutputReference",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthTokenEndpoint",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthTokenEndpointList",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthTokenEndpointOutputReference",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOutputReference",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputParentIntegration",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputParentIntegrationList",
    "ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputParentIntegrationOutputReference",
    "ApiAuthenticationIntegrationWithClientCredentialsShowOutput",
    "ApiAuthenticationIntegrationWithClientCredentialsShowOutputList",
    "ApiAuthenticationIntegrationWithClientCredentialsShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__25e22f5a68ec2f32ee1644ebc6a1ef8d77c014c1d29e5805b3248f983cb54674(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    oauth_client_id: builtins.str,
    oauth_client_secret: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    oauth_access_token_validity: typing.Optional[jsii.Number] = None,
    oauth_allowed_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    oauth_client_auth_method: typing.Optional[builtins.str] = None,
    oauth_refresh_token_validity: typing.Optional[jsii.Number] = None,
    oauth_token_endpoint: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__eaca6126a741b68cefd98d37d0db1e793e56bd2ba7a701f6c7a8ee178b7650d5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e17b9ff01f640af83e8a42f73f780a1ea0b1543026f658e802bc38337fda05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98216723c60354ef39ec4b7da52946a7224b323f143fc2b6c18ef9004c64fe8a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5dd559b26988e347700bd7ca2e4064e89e6d24084ed39ed6dbfc3132fe5b24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__506e4d3d8f1a0c4678b0f43856342e0d0b0fbce0d9771339956bb2fbef0cd598(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9818cda6aa0cb8c4d9fa111f589f72e99e88ed09922f53f24c3a9b27a2d1e997(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6a5c4ee0296090f338749fcc62965bd7b6e7fec87eeba1de9bbb846f5f79129(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff637710f60b1284f00353fa8d32ef92e0748cff209fd3b98100f3648c2ca98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d39f6c6fc847b239fe5a2d194505bd730dfc82ebe95d0dbabaaf4dada41dea4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d386994f515da9cf6f880a95a0413e8556074f1d5e89b0db4711026fde9c277(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e050cbb14713ae33e69226a76dcfd6e5769fa26de1d06d83ee5d0f23aa5775ea(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f91d39ad712a6d871493d6c0326d6307ecbe74f0480765301584451e646c2d68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__474863c3f49624a9b759fadbe50278e3b882360af115f020af32caa92c7cbf41(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    oauth_client_id: builtins.str,
    oauth_client_secret: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    oauth_access_token_validity: typing.Optional[jsii.Number] = None,
    oauth_allowed_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    oauth_client_auth_method: typing.Optional[builtins.str] = None,
    oauth_refresh_token_validity: typing.Optional[jsii.Number] = None,
    oauth_token_endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f353f4d0617a589aca4c2e7091dc70df21f5d79ad2c303601e69aa9f9f8e13f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e0b64190aec85ef8e7a0eb325914655fc5b44e8fc67c3954fbd2ca63ac49eb3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d308a21462ba88c8eefa029b85fd7c91e1067cf6fbe5e5293d1845876d222e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ee09c8e2c9d3bb71e37ebe520652e63fe44b689b15d534af122cb97a3d50d7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb69ba3c71aed7c1ed7e7a0f7eb33aa11c1af5ac5307e0d0f75ca334693d8752(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a13d2866638e9261db687b866c2c7c60e5bd207402093a463abdf4217784083(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b3710686fe13be691a833bc23ea5b5364367ad136601d2348ae5bf57ccd7b1(
    value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputAuthType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__986a9874f2474fc895e05e343ffbd0272e48405ed1c75d0b8871114a82eade94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809b491d526c833820f0552b2417b26dd8c19e6fd3450e86bc8512e0f6658fc1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d2589c651889ccd676959070b7799cc32e245fd936705b9aca99626032f27a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b1fe5770d660bbb08af6a2d3baa062849dd12350c7a9cdcc62fe6a9029fc8d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311bcaab23c769b8b9394fbec49ed277ce08ec1fcc0c19f24c423dd7fd1e3cd2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd9a8e7af24371c336da3f0110f841aced2a7d264635d4a18a3fbef6118f62b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d8cb03d63abcb143cb6f11109ab1f5824a693e919730cbcedf7245167e635e8(
    value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputComment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c01c94d6ec4d027d9205d3f304c7e76bb542ba4a53ff8ab036f5e3aa8a35f313(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f03f50c8b65ce23c8661b2d2455f261a5d030f8ec01407b8112d904af05ef5d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572fb06f7e61e35ec9adaff2021e1ae826e17c54098dd4c6fc6ead50ffad4f2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0410d9cda122f8fcb0cac3dc6263ba9af5b6d857e6946d5564525a271016135(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686cc6a441df531dbaaef9541ec5fe497b61294c1ffbddf1e2d305dc9cf92057(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a69f6ea5115f21e3be0d26827b4d102a3d31197a599c718b49981479616c7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b318d8dbfd47804fb85ff375d6222da1f7377e887fd380adce1f7297bcecd4(
    value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputEnabled],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77aa62829614cb696d4d4ad936f5f012939a78dc76df8f18b0e65a1f6805a95f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6acedd6e28f46bd3547ce93f20cb800356e6aed66b42933addcb8f430e2613a0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030edd04d46b511fed8377b890c2742b296dd4ed4ceaedf8343a15284ba0670d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e376ebedc1fe022e5352d93b4c8cf6b59de2554cf35921752b53e3db3436503e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__919c32ec64b9384d6340568c9671ed571b32d012af009f134736b2361a1392a1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34a16fffce84dad00c8124ea850a76d40c777c6b53215858364150029b275382(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39afc75d44fa01fdef50353bd3fcc88e341a239aa70997fafea91889cdf9c1f6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05272b3087de8f5e83f63dbf25cf54d15feb1c3dad07747f5aedc400f4b36a8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb02868926d1aca422f79150fa4676337f7ce7bc077bbbe51102ab8ee7a315dd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2856e6a64969d2d0275362dbc3d78bc4529e2867186c28463aa0bc717ff501c1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c3f06a23b72402e80a282f47fb568e5b84b665712132d63a39ff144b9d1ff7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4794692b5e7a4ca8da4fde1268979a70b3e8e353ddd5acf5c52dc4f781e59c9a(
    value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAccessTokenValidity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f6e9a0f757a0ad875d5998b9e320b60b00c1cc1304abe95e96148b8a5f17498(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6dbe7afe4be528380ab54ca72156be2b8e7dc77bf5b4b7666c61d0eff9982dc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380131e293c4206a288806d871b306efed34e176e502ac23047e353b1c8ad8d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fbf1d1f37ec8879774f2418c8265c5ebaf522226a5eb589bb4e1fd93be7f481(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__569a655d7cf6701e20ff9300f0fc98a0bd0e4cf1dccff3b3ccd27b30b60a6618(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b5357f4525ffb1e80b53ed68c64154eb877f571d058eb5d3867c71aa22d1d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85813a3ae2789aa9a78a77f020af6d415f60653ebe8b4c46ceed1fabe2032b3f(
    value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAllowedScopes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc24b1f62e3086481be20385c5d7d64f030c7618d94bb18c0e9af31b372746e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9aa815ebbb893323e14c65441aff334d91397b363f5566c2b41b336c604511(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a79aacc958a03564a5284dd504e45ccf2ba4f88ba68dea3761afd179f864bb94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48da05bc4473c3d8a1e5cc146bed6f87794a7b2d997f9dd39a7f4ab873041626(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f988b1ffc0195506751bd7f4defd87e50b298dbe791a5f7b85feda4370ee6b21(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2bc84ac71d19a0d1cb0ae495767a4f4a082b28e621f66a03243d9ebef221bc0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a80157b52a140a3d35f08892dba3328f093c007a2fcaec00f34fd1501cd7613(
    value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthAuthorizationEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ffc3ca492743893cea4f6ed240e0eb0aa05e10ee8690f40a82a121944ff8c33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1706cdf46516c0f228de1b434c418ed9d19ae2313986cb202c7782cb702d6632(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2925f5fbe9c4f6838ce0d9f9c59e7d4466adcea2ab1818c53a97dfb77f66b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b220d39a143183a448871b6542b1edc382861bc6554b52c8f6557a5fad501557(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7eab3f660b7f188c006112c59e62f447274ae97066a442cb762fa260ad6bcf4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad60561290fa1e53f5d5da47db6b7c4dc98978ba138e34bc0116f23686f584d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__665fe2a025de696e8c65263733ba12e7be6544cc626de1b6aa5df091fea891f4(
    value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientAuthMethod],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c22eea157edec5ef07fffe6d057a3fdb14ef20d11e102dff072c4780a98f210(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a50f4b11384f98b47054b7f15594c9cabb83a5dde70dfda1bc0ac924e890178(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e3a90e21c60b1c062c13ddf7624c9ff06f41e2777a6a4a9d77879f49bdf0287(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__950223a76ae8852aad07add0be6b93f0964139e49dd93444c7363e8c6e4d4ee3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f7a60f7c024a74140b28369d1457186abe20507557c82f8edd6510d722dbf7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e117c764138c9797dad6fb4109d1070f1944d94e272d868e933cf1bdd9f322a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__079296c4c639871e4c2b39124e6ba637018cbfc6b9de3544224895be5a4739c3(
    value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthClientId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f5cee2616352d7c7bb8ed0a4f847744d81168a2648801ff7c5d14f2a709c7bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d9cfa3b456fd99557992a0417981c7a61b70f265c967022cbbbab8137d42dec(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5085409dfaa04f9efed8b6ae9ba0bf6eb52b02fa6c9f2dcfa694e8e8553b13b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382e8554808463bc6cb1dd8d8fe790ebc582ae5c95757dcce532d302900c336b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c72fb1bde553fc0dcce7831288592784dc5c709ca32a0b39c19e68c0f851db1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc7e57d022d55b301870d387125df493b039f0ef923d30a56098d2b2e5896d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecc78d699f701839ace2da7642ea578dd8912dda2a5e74335918e3d5666f97b1(
    value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthGrant],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d19f3d2c9be68474199213dbc6dc2e913581ed23fbe9d4827c95bee9173afb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a2c372cb5019dca75759770007bf0b815ba9cb6da7ffe73144a4e1547198bef(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de0e6f22170b4325066756e6e8e10d4227ea0e0d9eb7de7917ff362d66153ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c1f1054b20c0b22114f2f3d822d8f61e2fa4c5ca8080a165a5de0b9be24049(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8907c5bf7b3b4fa1f9e6e287768e890d479904c9b11fee79ed85cf8eda82e7eb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07b423aee48ddecb33bc4cae03652742a301e331d7009385d104ded2d37c9206(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__456e023cb6d4feb08cc10913e75f1ec212004c156f70dd7ebfd91d4043a6c038(
    value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthRefreshTokenValidity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a87463daf400387bb02ae5729ae30ffc545dcc75e3bb333ebab048f2e5970d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02987b36579f3292766d17533fb2e5aa500139e28493351a12dc481a30508dc3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe9c2c95e260f9363231dc202e9e2e2f7ce7212919a579ae0153b66d87602357(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61cc7118d8bae4d59a76a9470b391574da6a8ef67c27dd1d96dce162b1d27e77(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a28c0580fe7493c5df9a44604c381c86419fc2d1813fd6a100aee4aa19be0fc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__321b9814df0e36e8854d33db31e8ee403f1577432a07a50568556917dc695eec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a632f8f7b3748ebda2b95d5e552afcacba41980e21f0272f2e15700ed8a81886(
    value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputOauthTokenEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bf8cc1ab2f6798e9fa60617c4368c0b2aad6218be48deae8f09421aa4f2c7c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dec3e6723747444baf87cbf3a2acfdc2c225f78d87040be93246277dc46de15(
    value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d6814dca1f0eef60d5475386eb0c41dd2b042b8bf71be036e2ba7f7a4b6feb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb5341afbbe6cd2218fb66f87306d90ad419837dc461aacb0a4416750c877d84(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c6b8d1e5f6a5ca00b1faae1276005763858fcfedc387554aab513be5f983f8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f989c636486151798c687d014f29e389a9e2dfec54b735914d8f9ad07a3196(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f4687b5c0e44a2ab4810eec147b6d19bed9ca5e7d2500cbde735e12e60cdc4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a9c6af01b91b4b3459e31bcfb06f22ccff70a139978775b6ca7a46e7fbf3701(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176b3bb444e8b06467dd94e76ca6b07c65a073453d26cbaa95f29ed7579668bc(
    value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsDescribeOutputParentIntegration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee8232036ea31ae0e642e6b6572fdea52882cb752b911d6348bb21eedaee9a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f91593a53b193079cdbdeb3ae91eed3cadd86ab5eb6cd6b03b93239a2e7934(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55d4d5548ff7592fe83322d43ed1c69c342cb7ead0f084e9b3d83472e60a8eae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9baf8c2d0d5b65d1714973931ba4260d29d34a1975f08076ed1d7277c233868(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31468a89438edf8cb3a419e47bda9f4e9c60c5b84ef8991c5b9ee8fb91a7d74e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__045ee71c4d23623852516b483cfd53d0c11f0a13dfbbd47f7516ead524f2ec32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a1bd3560aebc0c3d86ee66ef6b0e42b508c1341cf7be7d4cbc3a1898e7171d2(
    value: typing.Optional[ApiAuthenticationIntegrationWithClientCredentialsShowOutput],
) -> None:
    """Type checking stubs"""
    pass
