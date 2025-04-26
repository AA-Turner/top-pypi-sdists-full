r'''
# `snowflake_api_authentication_integration_with_authorization_code_grant`

Refer to the Terraform Registry for docs: [`snowflake_api_authentication_integration_with_authorization_code_grant`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant).
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


class ApiAuthenticationIntegrationWithAuthorizationCodeGrant(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrant",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant snowflake_api_authentication_integration_with_authorization_code_grant}.'''

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
        oauth_authorization_endpoint: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant snowflake_api_authentication_integration_with_authorization_code_grant} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param enabled: Specifies whether this security integration is enabled or disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#enabled ApiAuthenticationIntegrationWithAuthorizationCodeGrant#enabled}
        :param name: Specifies the identifier (i.e. name) for the integration. This value must be unique in your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#name ApiAuthenticationIntegrationWithAuthorizationCodeGrant#name}
        :param oauth_client_id: Specifies the client ID for the OAuth application in the external service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_client_id ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_client_id}
        :param oauth_client_secret: Specifies the client secret for the OAuth application in the ServiceNow instance from the previous step. The connector uses this to request an access token from the ServiceNow instance. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_client_secret ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_client_secret}
        :param comment: Specifies a comment for the integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#comment ApiAuthenticationIntegrationWithAuthorizationCodeGrant#comment}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#id ApiAuthenticationIntegrationWithAuthorizationCodeGrant#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param oauth_access_token_validity: Specifies the default lifetime of the OAuth access token (in seconds) issued by an OAuth server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_access_token_validity ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_access_token_validity}
        :param oauth_allowed_scopes: Specifies a list of scopes to use when making a request from the OAuth by a role with USAGE on the integration during the OAuth client credentials flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_allowed_scopes ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_allowed_scopes}
        :param oauth_authorization_endpoint: Specifies the URL for authenticating to the external service. If removed from the config, the resource is recreated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_authorization_endpoint ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_authorization_endpoint}
        :param oauth_client_auth_method: Specifies that POST is used as the authentication method to the external service. If removed from the config, the resource is recreated. Valid values are (case-insensitive): ``CLIENT_SECRET_POST``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_client_auth_method ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_client_auth_method}
        :param oauth_refresh_token_validity: Specifies the value to determine the validity of the refresh token obtained from the OAuth server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_refresh_token_validity ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_refresh_token_validity}
        :param oauth_token_endpoint: Specifies the token endpoint used by the client to obtain an access token by presenting its authorization grant or refresh token. The token endpoint is used with every authorization grant except for the implicit grant type (since an access token is issued directly). If removed from the config, the resource is recreated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_token_endpoint ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_token_endpoint}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0084e204734cbe9566934f236ce4f88073a4c278344895bea41dcfa6f3b935d2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApiAuthenticationIntegrationWithAuthorizationCodeGrantConfig(
            enabled=enabled,
            name=name,
            oauth_client_id=oauth_client_id,
            oauth_client_secret=oauth_client_secret,
            comment=comment,
            id=id,
            oauth_access_token_validity=oauth_access_token_validity,
            oauth_allowed_scopes=oauth_allowed_scopes,
            oauth_authorization_endpoint=oauth_authorization_endpoint,
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
        '''Generates CDKTF code for importing a ApiAuthenticationIntegrationWithAuthorizationCodeGrant resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApiAuthenticationIntegrationWithAuthorizationCodeGrant to import.
        :param import_from_id: The id of the existing ApiAuthenticationIntegrationWithAuthorizationCodeGrant that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApiAuthenticationIntegrationWithAuthorizationCodeGrant to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09688773116f7e222c356bd9157947acf687a9f5988ede9bd4db42936848948e)
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

    @jsii.member(jsii_name="resetOauthAuthorizationEndpoint")
    def reset_oauth_authorization_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthAuthorizationEndpoint", []))

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
    ) -> "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputList":
        return typing.cast("ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputList", jsii.get(self, "describeOutput"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(
        self,
    ) -> "ApiAuthenticationIntegrationWithAuthorizationCodeGrantShowOutputList":
        return typing.cast("ApiAuthenticationIntegrationWithAuthorizationCodeGrantShowOutputList", jsii.get(self, "showOutput"))

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
    @jsii.member(jsii_name="oauthAuthorizationEndpointInput")
    def oauth_authorization_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthAuthorizationEndpointInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__394ffabbb569bf9abc6bf079da92d5385afd263f9f015097193b99c407d99137)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e085d9208f015f1e6c6ab855cc6f91a6561e219526961d199ea35772b36391fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a528f227bc19049c3e2b3ac21bcc684765f1bc3538ed9f1e243e570965d00e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__761af68cd8584433ab50323dcd5fb100aa7c27269b2ed4cf517a887de28822d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthAccessTokenValidity")
    def oauth_access_token_validity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "oauthAccessTokenValidity"))

    @oauth_access_token_validity.setter
    def oauth_access_token_validity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__624ac9463aabd65db10d4f6618e5540f6d41c5d83c16cb85fc2b059ee3f6de33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthAccessTokenValidity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthAllowedScopes")
    def oauth_allowed_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthAllowedScopes"))

    @oauth_allowed_scopes.setter
    def oauth_allowed_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__278079599ee463f3c978e69e9f9358e6cff99584e5896e19d7bd412f791348e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthAllowedScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthAuthorizationEndpoint")
    def oauth_authorization_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthAuthorizationEndpoint"))

    @oauth_authorization_endpoint.setter
    def oauth_authorization_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48d745480a115da02d11e9b62d1e7b277f13d0cd11707b5cb0dcdb45df5cf0d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthAuthorizationEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthClientAuthMethod")
    def oauth_client_auth_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthClientAuthMethod"))

    @oauth_client_auth_method.setter
    def oauth_client_auth_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53adc7bc47af44c9059e1cde578e300e6da1f5e89c63bf8dca852616c3f3de66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthClientAuthMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthClientId")
    def oauth_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthClientId"))

    @oauth_client_id.setter
    def oauth_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2cc21365add95ad956c1f3b79731d132b45b145a4d71f86aaa62980a42d71bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthClientSecret")
    def oauth_client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthClientSecret"))

    @oauth_client_secret.setter
    def oauth_client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ead190bcd8fbff6f0164b8491bb418bdb45b933465949d48095cd6abb5f77490)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthClientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthRefreshTokenValidity")
    def oauth_refresh_token_validity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "oauthRefreshTokenValidity"))

    @oauth_refresh_token_validity.setter
    def oauth_refresh_token_validity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4ba6d78c5e5aefab2f14354fefc1c21c107fe306ebf01f3d66b6602842f974e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthRefreshTokenValidity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthTokenEndpoint")
    def oauth_token_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthTokenEndpoint"))

    @oauth_token_endpoint.setter
    def oauth_token_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3a1a35077c254fa87a9410a7f9a82bbb9ce380cbbfae1e3b43a78ad27e5df3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthTokenEndpoint", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantConfig",
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
        "oauth_authorization_endpoint": "oauthAuthorizationEndpoint",
        "oauth_client_auth_method": "oauthClientAuthMethod",
        "oauth_refresh_token_validity": "oauthRefreshTokenValidity",
        "oauth_token_endpoint": "oauthTokenEndpoint",
    },
)
class ApiAuthenticationIntegrationWithAuthorizationCodeGrantConfig(
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
        oauth_authorization_endpoint: typing.Optional[builtins.str] = None,
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
        :param enabled: Specifies whether this security integration is enabled or disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#enabled ApiAuthenticationIntegrationWithAuthorizationCodeGrant#enabled}
        :param name: Specifies the identifier (i.e. name) for the integration. This value must be unique in your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#name ApiAuthenticationIntegrationWithAuthorizationCodeGrant#name}
        :param oauth_client_id: Specifies the client ID for the OAuth application in the external service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_client_id ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_client_id}
        :param oauth_client_secret: Specifies the client secret for the OAuth application in the ServiceNow instance from the previous step. The connector uses this to request an access token from the ServiceNow instance. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_client_secret ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_client_secret}
        :param comment: Specifies a comment for the integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#comment ApiAuthenticationIntegrationWithAuthorizationCodeGrant#comment}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#id ApiAuthenticationIntegrationWithAuthorizationCodeGrant#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param oauth_access_token_validity: Specifies the default lifetime of the OAuth access token (in seconds) issued by an OAuth server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_access_token_validity ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_access_token_validity}
        :param oauth_allowed_scopes: Specifies a list of scopes to use when making a request from the OAuth by a role with USAGE on the integration during the OAuth client credentials flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_allowed_scopes ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_allowed_scopes}
        :param oauth_authorization_endpoint: Specifies the URL for authenticating to the external service. If removed from the config, the resource is recreated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_authorization_endpoint ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_authorization_endpoint}
        :param oauth_client_auth_method: Specifies that POST is used as the authentication method to the external service. If removed from the config, the resource is recreated. Valid values are (case-insensitive): ``CLIENT_SECRET_POST``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_client_auth_method ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_client_auth_method}
        :param oauth_refresh_token_validity: Specifies the value to determine the validity of the refresh token obtained from the OAuth server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_refresh_token_validity ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_refresh_token_validity}
        :param oauth_token_endpoint: Specifies the token endpoint used by the client to obtain an access token by presenting its authorization grant or refresh token. The token endpoint is used with every authorization grant except for the implicit grant type (since an access token is issued directly). If removed from the config, the resource is recreated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_token_endpoint ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_token_endpoint}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8140889e1be581a8fef12655e75ff030ecad70f41da4a35529228eab0866804)
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
            check_type(argname="argument oauth_authorization_endpoint", value=oauth_authorization_endpoint, expected_type=type_hints["oauth_authorization_endpoint"])
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
        if oauth_authorization_endpoint is not None:
            self._values["oauth_authorization_endpoint"] = oauth_authorization_endpoint
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#enabled ApiAuthenticationIntegrationWithAuthorizationCodeGrant#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the identifier (i.e. name) for the integration. This value must be unique in your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#name ApiAuthenticationIntegrationWithAuthorizationCodeGrant#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oauth_client_id(self) -> builtins.str:
        '''Specifies the client ID for the OAuth application in the external service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_client_id ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_client_id}
        '''
        result = self._values.get("oauth_client_id")
        assert result is not None, "Required property 'oauth_client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oauth_client_secret(self) -> builtins.str:
        '''Specifies the client secret for the OAuth application in the ServiceNow instance from the previous step.

        The connector uses this to request an access token from the ServiceNow instance. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_client_secret ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_client_secret}
        '''
        result = self._values.get("oauth_client_secret")
        assert result is not None, "Required property 'oauth_client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the integration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#comment ApiAuthenticationIntegrationWithAuthorizationCodeGrant#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#id ApiAuthenticationIntegrationWithAuthorizationCodeGrant#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_access_token_validity(self) -> typing.Optional[jsii.Number]:
        '''Specifies the default lifetime of the OAuth access token (in seconds) issued by an OAuth server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_access_token_validity ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_access_token_validity}
        '''
        result = self._values.get("oauth_access_token_validity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def oauth_allowed_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of scopes to use when making a request from the OAuth by a role with USAGE on the integration during the OAuth client credentials flow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_allowed_scopes ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_allowed_scopes}
        '''
        result = self._values.get("oauth_allowed_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def oauth_authorization_endpoint(self) -> typing.Optional[builtins.str]:
        '''Specifies the URL for authenticating to the external service. If removed from the config, the resource is recreated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_authorization_endpoint ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_authorization_endpoint}
        '''
        result = self._values.get("oauth_authorization_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_client_auth_method(self) -> typing.Optional[builtins.str]:
        '''Specifies that POST is used as the authentication method to the external service.

        If removed from the config, the resource is recreated. Valid values are (case-insensitive): ``CLIENT_SECRET_POST``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_client_auth_method ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_client_auth_method}
        '''
        result = self._values.get("oauth_client_auth_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_refresh_token_validity(self) -> typing.Optional[jsii.Number]:
        '''Specifies the value to determine the validity of the refresh token obtained from the OAuth server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_refresh_token_validity ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_refresh_token_validity}
        '''
        result = self._values.get("oauth_refresh_token_validity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def oauth_token_endpoint(self) -> typing.Optional[builtins.str]:
        '''Specifies the token endpoint used by the client to obtain an access token by presenting its authorization grant or refresh token.

        The token endpoint is used with every authorization grant except for the implicit grant type (since an access token is issued directly). If removed from the config, the resource is recreated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_authorization_code_grant#oauth_token_endpoint ApiAuthenticationIntegrationWithAuthorizationCodeGrant#oauth_token_endpoint}
        '''
        result = self._values.get("oauth_token_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithAuthorizationCodeGrantConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputAuthType",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputAuthType:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputAuthType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputAuthTypeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputAuthTypeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__169bb6cac01a2b68563141fc309ca8f989350c019868c1596b1332d1f5281f1f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputAuthTypeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c9ddd6b2f9c3cdfc808a4a503cc521c8149edd4dfbfb650a7b5cc3cef01b4c9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputAuthTypeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__486d1602c746e72841c82b1e489cd12b8ea7f6e5c02c111e669af01085e4d0ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__571f283f85aba2e7d4911958a41073fa38480ff4dfbe9b649c610cb273ec2484)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69811321f236bcc65040c2d31904605c3ef903b268f1c230755055783974088d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputAuthTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputAuthTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67af5fac94d3011f50507cd21cdc76240b3f6f421acea6a5d4bb4953cd742b6f)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputAuthType]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputAuthType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputAuthType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__659021f0f8329575d3461f6b844aef66a4a2dd4752acb4df6fefa60178f22610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputComment",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputComment:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputComment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputCommentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputCommentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56e9af4512c2d5d68d7a5059dd102fb918a6d3e65e959b7b297fce73535cdb74)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputCommentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a92e3d60944e2788a7cd943566b23bbc586d44d3b333691aab8c76d6c705af5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputCommentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c779122da541c3356c343db60701717f984a4d8dbd0befa1b45f19da1fa6bee0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57d1945d4e479f23b19117df7bc6bcb5eea0c4eaae43483756834bcd7fcaaffc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b58d6f1cbd836f0f9e691a8c1958085c7e552cac0ad15b1d851bc81ac3d95bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputCommentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputCommentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c16960729627b841076e13fb0217c89e406c862b6ff6d04da8533d5570d28d35)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputComment]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputComment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputComment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dee723283b370b6c050e75aef804413a4163c66275a07b45a62677b20bf9d80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputEnabled",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputEnabled:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputEnabled(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputEnabledList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputEnabledList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c97681b712a2c9aa8bcc296526d5423f1420f7cae75c0bb663ca3a319e73d8fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputEnabledOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d7a37fdea7658d0c4f7e339b55397f550974ba575a05a6ce2d54ec00533ca0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputEnabledOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df8e272b32bc083f695b63eba242d1db0de0bf3c7ac460a7a0973881896d71d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9529cdd7d33bed74449f2b86b90a988f65effca53001aafd2c807c571724b9ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e32b445990254609044c8fa00d1cc3a1957d7a9c0d0ec0744fde6b8605efc0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputEnabledOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputEnabledOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebba71e6a1cccb20d0d0fdf3aa22c09fabde92f34a7702afcffb5d15cf96c11c)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputEnabled]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputEnabled], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputEnabled],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6431108c1f07859faa2f00afb815f8971ee97bb746b8e8b7be536e48bd8d9a12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dab73ff07425c1acea19f9b288ace71a0001a194a2808ecb9eb70fbf9805a8d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1482cfd8040b94b22a576005dbe9e89b94bbfefa551148552b7971ffd586d3a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b147bd15b480c39353b8d58131a899171f2ea641d34a12d13f93ac026406087e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9f30cc657d1af5a47f7b501661ee0e2095d8e0eb5e75725fde54ed214c0594d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c3bfd9e50f838ff7453869f6204531bc1b76ddebce41b18f3ee4fced5166c18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAccessTokenValidity",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAccessTokenValidity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAccessTokenValidity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAccessTokenValidityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAccessTokenValidityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69de72e00a93d83cde1ed68a75516514cf9dc92f6989a36529ea44bfe6514854)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAccessTokenValidityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28c17ae7732991585bc861c648df5919e9ff26bee8cf74ad08edf6b53be34759)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAccessTokenValidityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466f0a03be95426ca85dbe1af5b44ade223d56645d956400c39b4eed54485d45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b982f04900dd6d45136be510446393bcd188d9d9030449c8a5eafc20918ba254)
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
            type_hints = typing.get_type_hints(_typecheckingstub__88f391c2157d1b567fc8ca5381a86bb41ab85a18242f6fb340466df628d5ef51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAccessTokenValidityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAccessTokenValidityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a3fb0eb3a772f8651bf424a3d2871a3705237a5dee7b37c5c4a2678de751179)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAccessTokenValidity]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAccessTokenValidity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAccessTokenValidity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ab9ec6e0e124f8f04644f7756f940ea59690d1f820b937b4fb276f4fe05b5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAllowedScopes",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAllowedScopes:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAllowedScopes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAllowedScopesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAllowedScopesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42d3e3d92da959d0443080c4cbf386237ae28d59b14292b98c017488dbe01886)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAllowedScopesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__315311b7e36b59db3f177cfa5ef1b2380dc0ac02498623fd81a63d5cf0292c83)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAllowedScopesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be2368d103070a23e15ddab12e9e6aeecdf23bb31698d8abf886475408c91965)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05bdecc6b54d58b442e4479d046c460edfddf216173848ae344c064be487c786)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b27f72b348e2dc39d56cb1a607b1a3f1e2c4e070379b7bd3cd05c1cb9b2b0b06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAllowedScopesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAllowedScopesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38b9b2f37a3949e2c8c824e6470132b279a23e7193e3fd5ad24054edfd59d0c2)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAllowedScopes]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAllowedScopes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAllowedScopes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69b83ea7991c6e2836e1c36458efc94aacd9913df1f27c676511c6aa9825079e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAuthorizationEndpoint",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAuthorizationEndpoint:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAuthorizationEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAuthorizationEndpointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAuthorizationEndpointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e383b0b1d11a7b09a5c82ee2af51bb86034ee4b5074c677dd805bdb0848045c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAuthorizationEndpointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c205093dbcd801abd2e930b925e753e11b758b91b0c96a722b15893a0fcef6c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAuthorizationEndpointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f17dfd1d7f724a509823d78d2f152b1349218f1318c874179e3cb270383d8f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__faf5af9916e432cedb4451732a592d72c6eb0465de1cb8c49464c9d1d53960d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c8ef64fcb6c8ea22c7028ff3957daee82a9603c7b24972b0f915a54cbd3effe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAuthorizationEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAuthorizationEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cce7ab4d81df1448673c522b9dd9012abd0bf35e7418b79edbf6f28aff8cd4b8)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAuthorizationEndpoint]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAuthorizationEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAuthorizationEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78a62cd2a66bd80bc6426ef1551bf69866e6fe67e51aa9545a676ebdc264d60f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientAuthMethod",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientAuthMethod:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientAuthMethod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientAuthMethodList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientAuthMethodList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27dd511e4b8294934adf934daa807a83eb20c1841698b8d3ecafb9da1104ca4d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientAuthMethodOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cf963acf60df8aa305ca71b0a5a19faa7851e7a4cb546900950205d0fe61b87)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientAuthMethodOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__951bbd679434f5b79e4c5f377a6de10661a2fe1bc09f7bbc68321d49d3d92d0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f715e869ff433105f730ae2d89c08a944b46f5f7a90670da0961caa208f8be1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9076344d38ffddfdf9c29ffecd97bfa4a8629aa65643ea567f3dfe2588f1a193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientAuthMethodOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientAuthMethodOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e662239fafd65eccc6d3871b02163eff34527a406ab324e6e65727cefd94234f)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientAuthMethod]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientAuthMethod], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientAuthMethod],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36ef379ba13723d002afb718ec9edaaf36d76a04f0018ca06f2cc121c0b9c6ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientId",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientId:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientIdList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientIdList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61055d29eb3cb4cfaa29e664e1366bc6b34f04d2645e544216ea26c48345482f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientIdOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fd96ac2b096ac4848c8dc6d97b86efc730c8f211eb5a3964d102cf39692325c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientIdOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b861186cc6cb89f30e37cb90a2b7738585bc21f04e14e9244b72064be379a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22a237e94df547d098155431546692842544f2da2499ddd7eacb2b320cc75b90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d74233b9d2f3b5d035b4f0f3fe76a6c7480a787923ceb99fd7889381b874ac7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45a1a4ce5b44aa6cf482e677f5c528116afdb8e027ddd92546a7a7f5a8bafc52)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientId]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71377a82a6f5296787cb37bdc801c0ee6a69e87da18a9d79dbf278c0840f9f3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthGrant",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthGrant:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthGrant(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthGrantList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthGrantList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__867faff80fb1306a329f500b812f37a73b4c8b6606adaa89f4ff1cc25695913e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthGrantOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aed70f05c0a1ba1f56a3951c564dc867f1e9609cf05c9d50423989ef2d221518)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthGrantOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbba1ce233fcf84c44dc0b43931b5755150a7c585051887d69726ad14245b244)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8eb26998a10b776c1718b6a328fbeb927daee85c4256ebf11bd5c1d0f4f10b89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3180a3a1ded66acc4d2d524cdb9776a5c99389faf0fca739e126b6fbe42eb543)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthGrantOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthGrantOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe36ae60433726b6ad2387782a725da8cc6cd230f554b2860630b9f69935b77b)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthGrant]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthGrant], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthGrant],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e9afef7dc159130f2751a37e7683beb571760e426d2fd111c2c174cb2caac4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthRefreshTokenValidity",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthRefreshTokenValidity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthRefreshTokenValidity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthRefreshTokenValidityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthRefreshTokenValidityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2341864e18588e5c7851d083eef8d86f185425a46cc33ace89aac6bd30f6c48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthRefreshTokenValidityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48c21cf4ccbf7357568ec73142a11d82422ee2ff69c984cfe5a7e2e64efce5b1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthRefreshTokenValidityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb37230b328195e67a8ac177f61f4e90b70eb74bc98c4bc21f14db3c4e1025a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f325db5e1082308d810a09f10c6bb123ec8464aa3e6ee9b82aad137cae7fe270)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b806b74384e1073c99b84d1ab705c70d39e344873e5acbd4e665ddd9b059e34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthRefreshTokenValidityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthRefreshTokenValidityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5166780a43b72b1ccb038038aacce37562a9d2e02c0d2bc75350b6ab1e725213)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthRefreshTokenValidity]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthRefreshTokenValidity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthRefreshTokenValidity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efbc2eddf7afa94cb1e7fa60e9ca23216e1989b6b53b24ffdcf7fe50c808bf28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthTokenEndpoint",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthTokenEndpoint:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthTokenEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthTokenEndpointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthTokenEndpointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3671c9791d4f3de3a5f622f6ffb2c7422f4193562034c4d196f2263106885ce2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthTokenEndpointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0602b6d5a2a74e484c0fb6715c03ac2e2da4797e92ce2f794c63c2c4881b909c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthTokenEndpointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b640d1201bc2177a992831e8cc4157363740af9ae06299188e629876dedd0b8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d23b14779118a0a86fd296f05d6e2f8eee5b2cd339bc4156eb611129fc8393f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f7f85c4b35db7c5ff7639a85cbd432ec3632ab2148baedc9a9264eb47790322)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthTokenEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthTokenEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e3f2fd4de375c822347be85eb09ef104da3d5007d2c712cc2ab63471a8f4295)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthTokenEndpoint]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthTokenEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthTokenEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0108c4e8b985e43793d2d2d5282ac013a5d98b068d059478e92c46b6eb7e217b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39e53111252eb27153d149669fe4cc34e8cb801e4e945a1b72bb693a02b2c7b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(
        self,
    ) -> ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputAuthTypeList:
        return typing.cast(ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputAuthTypeList, jsii.get(self, "authType"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(
        self,
    ) -> ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputCommentList:
        return typing.cast(ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputCommentList, jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputEnabledList:
        return typing.cast(ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputEnabledList, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="oauthAccessTokenValidity")
    def oauth_access_token_validity(
        self,
    ) -> ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAccessTokenValidityList:
        return typing.cast(ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAccessTokenValidityList, jsii.get(self, "oauthAccessTokenValidity"))

    @builtins.property
    @jsii.member(jsii_name="oauthAllowedScopes")
    def oauth_allowed_scopes(
        self,
    ) -> ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAllowedScopesList:
        return typing.cast(ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAllowedScopesList, jsii.get(self, "oauthAllowedScopes"))

    @builtins.property
    @jsii.member(jsii_name="oauthAuthorizationEndpoint")
    def oauth_authorization_endpoint(
        self,
    ) -> ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAuthorizationEndpointList:
        return typing.cast(ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAuthorizationEndpointList, jsii.get(self, "oauthAuthorizationEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientAuthMethod")
    def oauth_client_auth_method(
        self,
    ) -> ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientAuthMethodList:
        return typing.cast(ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientAuthMethodList, jsii.get(self, "oauthClientAuthMethod"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientId")
    def oauth_client_id(
        self,
    ) -> ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientIdList:
        return typing.cast(ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientIdList, jsii.get(self, "oauthClientId"))

    @builtins.property
    @jsii.member(jsii_name="oauthGrant")
    def oauth_grant(
        self,
    ) -> ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthGrantList:
        return typing.cast(ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthGrantList, jsii.get(self, "oauthGrant"))

    @builtins.property
    @jsii.member(jsii_name="oauthRefreshTokenValidity")
    def oauth_refresh_token_validity(
        self,
    ) -> ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthRefreshTokenValidityList:
        return typing.cast(ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthRefreshTokenValidityList, jsii.get(self, "oauthRefreshTokenValidity"))

    @builtins.property
    @jsii.member(jsii_name="oauthTokenEndpoint")
    def oauth_token_endpoint(
        self,
    ) -> ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthTokenEndpointList:
        return typing.cast(ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthTokenEndpointList, jsii.get(self, "oauthTokenEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="parentIntegration")
    def parent_integration(
        self,
    ) -> "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputParentIntegrationList":
        return typing.cast("ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputParentIntegrationList", jsii.get(self, "parentIntegration"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutput]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ae90ac45e2d61ec3ae2eaecf8898ce44824fa461354f9b81693e287d63c2230)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputParentIntegration",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputParentIntegration:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputParentIntegration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputParentIntegrationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputParentIntegrationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f328e345d8c68304693f2fcd662a97ae36b3417e9e1804b1198037ecf4103890)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputParentIntegrationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d724f5cd873985c458744c6f4f5b4ffac7091f57da48202793477be395a73155)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputParentIntegrationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__567d550e53879828ac541279abea954931db2b19333775b346a35143db8aeb95)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e47bd880c38b20ee7402447750d9695913a72c994f99a26bd70fc1378048508)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1757e1ab5fd86d30f8f12f6c4b039577ee9423409337b2fd93819fcdb5cf92ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputParentIntegrationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputParentIntegrationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ebf30947621154d13b659fdd483a74c31a039a83a6fdb6648e16c728335abcd)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputParentIntegration]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputParentIntegration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputParentIntegration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad1a0af96f1246f0201d82b6a41fd948833cf9f1926fc740251b03123773b55b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithAuthorizationCodeGrantShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithAuthorizationCodeGrantShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c8f80b8728c50f8161f7314170a1e1b1ffd6822e166098c16039ea20a54e290)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithAuthorizationCodeGrantShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6487688247e86901fa984e54b9f7db67d0dcf3d2b3c183be9698f765ff08c47)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithAuthorizationCodeGrantShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__810dee316c78b7bc31860e478d75e6f0d3e553eb88bf9e0adbacfb28f9231ae4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed2b2e0ed011e42e7c0e981dcf5d3cad0bd3ba3f573d98ff66c3e51051066307)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49ef1956c0bf51d28e0ef714db6ab0116ab3c798d7542dc7bd2e4bdef4ea2025)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithAuthorizationCodeGrantShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithAuthorizationCodeGrant.ApiAuthenticationIntegrationWithAuthorizationCodeGrantShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f5e1b22effe47084d7f538cdf8d38deba196301f26ecd633f80f677cfe8d75e)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantShowOutput]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantShowOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16eef32e4b98c9134b2a9ed43ff67622fad2f974815d0b3952772b4a7822a29a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrant",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantConfig",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutput",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputAuthType",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputAuthTypeList",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputAuthTypeOutputReference",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputComment",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputCommentList",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputCommentOutputReference",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputEnabled",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputEnabledList",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputEnabledOutputReference",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputList",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAccessTokenValidity",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAccessTokenValidityList",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAccessTokenValidityOutputReference",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAllowedScopes",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAllowedScopesList",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAllowedScopesOutputReference",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAuthorizationEndpoint",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAuthorizationEndpointList",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAuthorizationEndpointOutputReference",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientAuthMethod",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientAuthMethodList",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientAuthMethodOutputReference",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientId",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientIdList",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientIdOutputReference",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthGrant",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthGrantList",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthGrantOutputReference",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthRefreshTokenValidity",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthRefreshTokenValidityList",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthRefreshTokenValidityOutputReference",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthTokenEndpoint",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthTokenEndpointList",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthTokenEndpointOutputReference",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOutputReference",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputParentIntegration",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputParentIntegrationList",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputParentIntegrationOutputReference",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantShowOutput",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantShowOutputList",
    "ApiAuthenticationIntegrationWithAuthorizationCodeGrantShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__0084e204734cbe9566934f236ce4f88073a4c278344895bea41dcfa6f3b935d2(
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
    oauth_authorization_endpoint: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__09688773116f7e222c356bd9157947acf687a9f5988ede9bd4db42936848948e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394ffabbb569bf9abc6bf079da92d5385afd263f9f015097193b99c407d99137(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e085d9208f015f1e6c6ab855cc6f91a6561e219526961d199ea35772b36391fe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a528f227bc19049c3e2b3ac21bcc684765f1bc3538ed9f1e243e570965d00e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761af68cd8584433ab50323dcd5fb100aa7c27269b2ed4cf517a887de28822d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624ac9463aabd65db10d4f6618e5540f6d41c5d83c16cb85fc2b059ee3f6de33(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__278079599ee463f3c978e69e9f9358e6cff99584e5896e19d7bd412f791348e5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d745480a115da02d11e9b62d1e7b277f13d0cd11707b5cb0dcdb45df5cf0d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53adc7bc47af44c9059e1cde578e300e6da1f5e89c63bf8dca852616c3f3de66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2cc21365add95ad956c1f3b79731d132b45b145a4d71f86aaa62980a42d71bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ead190bcd8fbff6f0164b8491bb418bdb45b933465949d48095cd6abb5f77490(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ba6d78c5e5aefab2f14354fefc1c21c107fe306ebf01f3d66b6602842f974e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3a1a35077c254fa87a9410a7f9a82bbb9ce380cbbfae1e3b43a78ad27e5df3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8140889e1be581a8fef12655e75ff030ecad70f41da4a35529228eab0866804(
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
    oauth_authorization_endpoint: typing.Optional[builtins.str] = None,
    oauth_client_auth_method: typing.Optional[builtins.str] = None,
    oauth_refresh_token_validity: typing.Optional[jsii.Number] = None,
    oauth_token_endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__169bb6cac01a2b68563141fc309ca8f989350c019868c1596b1332d1f5281f1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9ddd6b2f9c3cdfc808a4a503cc521c8149edd4dfbfb650a7b5cc3cef01b4c9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__486d1602c746e72841c82b1e489cd12b8ea7f6e5c02c111e669af01085e4d0ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__571f283f85aba2e7d4911958a41073fa38480ff4dfbe9b649c610cb273ec2484(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69811321f236bcc65040c2d31904605c3ef903b268f1c230755055783974088d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67af5fac94d3011f50507cd21cdc76240b3f6f421acea6a5d4bb4953cd742b6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__659021f0f8329575d3461f6b844aef66a4a2dd4752acb4df6fefa60178f22610(
    value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputAuthType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56e9af4512c2d5d68d7a5059dd102fb918a6d3e65e959b7b297fce73535cdb74(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a92e3d60944e2788a7cd943566b23bbc586d44d3b333691aab8c76d6c705af5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c779122da541c3356c343db60701717f984a4d8dbd0befa1b45f19da1fa6bee0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57d1945d4e479f23b19117df7bc6bcb5eea0c4eaae43483756834bcd7fcaaffc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b58d6f1cbd836f0f9e691a8c1958085c7e552cac0ad15b1d851bc81ac3d95bc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16960729627b841076e13fb0217c89e406c862b6ff6d04da8533d5570d28d35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dee723283b370b6c050e75aef804413a4163c66275a07b45a62677b20bf9d80(
    value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputComment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c97681b712a2c9aa8bcc296526d5423f1420f7cae75c0bb663ca3a319e73d8fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d7a37fdea7658d0c4f7e339b55397f550974ba575a05a6ce2d54ec00533ca0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df8e272b32bc083f695b63eba242d1db0de0bf3c7ac460a7a0973881896d71d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9529cdd7d33bed74449f2b86b90a988f65effca53001aafd2c807c571724b9ab(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e32b445990254609044c8fa00d1cc3a1957d7a9c0d0ec0744fde6b8605efc0e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebba71e6a1cccb20d0d0fdf3aa22c09fabde92f34a7702afcffb5d15cf96c11c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6431108c1f07859faa2f00afb815f8971ee97bb746b8e8b7be536e48bd8d9a12(
    value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputEnabled],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab73ff07425c1acea19f9b288ace71a0001a194a2808ecb9eb70fbf9805a8d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1482cfd8040b94b22a576005dbe9e89b94bbfefa551148552b7971ffd586d3a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b147bd15b480c39353b8d58131a899171f2ea641d34a12d13f93ac026406087e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f30cc657d1af5a47f7b501661ee0e2095d8e0eb5e75725fde54ed214c0594d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c3bfd9e50f838ff7453869f6204531bc1b76ddebce41b18f3ee4fced5166c18(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69de72e00a93d83cde1ed68a75516514cf9dc92f6989a36529ea44bfe6514854(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c17ae7732991585bc861c648df5919e9ff26bee8cf74ad08edf6b53be34759(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466f0a03be95426ca85dbe1af5b44ade223d56645d956400c39b4eed54485d45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b982f04900dd6d45136be510446393bcd188d9d9030449c8a5eafc20918ba254(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88f391c2157d1b567fc8ca5381a86bb41ab85a18242f6fb340466df628d5ef51(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a3fb0eb3a772f8651bf424a3d2871a3705237a5dee7b37c5c4a2678de751179(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ab9ec6e0e124f8f04644f7756f940ea59690d1f820b937b4fb276f4fe05b5c(
    value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAccessTokenValidity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42d3e3d92da959d0443080c4cbf386237ae28d59b14292b98c017488dbe01886(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__315311b7e36b59db3f177cfa5ef1b2380dc0ac02498623fd81a63d5cf0292c83(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be2368d103070a23e15ddab12e9e6aeecdf23bb31698d8abf886475408c91965(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05bdecc6b54d58b442e4479d046c460edfddf216173848ae344c064be487c786(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b27f72b348e2dc39d56cb1a607b1a3f1e2c4e070379b7bd3cd05c1cb9b2b0b06(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38b9b2f37a3949e2c8c824e6470132b279a23e7193e3fd5ad24054edfd59d0c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b83ea7991c6e2836e1c36458efc94aacd9913df1f27c676511c6aa9825079e(
    value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAllowedScopes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e383b0b1d11a7b09a5c82ee2af51bb86034ee4b5074c677dd805bdb0848045c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c205093dbcd801abd2e930b925e753e11b758b91b0c96a722b15893a0fcef6c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f17dfd1d7f724a509823d78d2f152b1349218f1318c874179e3cb270383d8f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faf5af9916e432cedb4451732a592d72c6eb0465de1cb8c49464c9d1d53960d7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8ef64fcb6c8ea22c7028ff3957daee82a9603c7b24972b0f915a54cbd3effe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce7ab4d81df1448673c522b9dd9012abd0bf35e7418b79edbf6f28aff8cd4b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a62cd2a66bd80bc6426ef1551bf69866e6fe67e51aa9545a676ebdc264d60f(
    value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthAuthorizationEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27dd511e4b8294934adf934daa807a83eb20c1841698b8d3ecafb9da1104ca4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cf963acf60df8aa305ca71b0a5a19faa7851e7a4cb546900950205d0fe61b87(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__951bbd679434f5b79e4c5f377a6de10661a2fe1bc09f7bbc68321d49d3d92d0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f715e869ff433105f730ae2d89c08a944b46f5f7a90670da0961caa208f8be1c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9076344d38ffddfdf9c29ffecd97bfa4a8629aa65643ea567f3dfe2588f1a193(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e662239fafd65eccc6d3871b02163eff34527a406ab324e6e65727cefd94234f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ef379ba13723d002afb718ec9edaaf36d76a04f0018ca06f2cc121c0b9c6ab(
    value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientAuthMethod],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61055d29eb3cb4cfaa29e664e1366bc6b34f04d2645e544216ea26c48345482f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd96ac2b096ac4848c8dc6d97b86efc730c8f211eb5a3964d102cf39692325c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b861186cc6cb89f30e37cb90a2b7738585bc21f04e14e9244b72064be379a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a237e94df547d098155431546692842544f2da2499ddd7eacb2b320cc75b90(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d74233b9d2f3b5d035b4f0f3fe76a6c7480a787923ceb99fd7889381b874ac7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a1a4ce5b44aa6cf482e677f5c528116afdb8e027ddd92546a7a7f5a8bafc52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71377a82a6f5296787cb37bdc801c0ee6a69e87da18a9d79dbf278c0840f9f3c(
    value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthClientId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__867faff80fb1306a329f500b812f37a73b4c8b6606adaa89f4ff1cc25695913e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed70f05c0a1ba1f56a3951c564dc867f1e9609cf05c9d50423989ef2d221518(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbba1ce233fcf84c44dc0b43931b5755150a7c585051887d69726ad14245b244(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb26998a10b776c1718b6a328fbeb927daee85c4256ebf11bd5c1d0f4f10b89(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3180a3a1ded66acc4d2d524cdb9776a5c99389faf0fca739e126b6fbe42eb543(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe36ae60433726b6ad2387782a725da8cc6cd230f554b2860630b9f69935b77b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e9afef7dc159130f2751a37e7683beb571760e426d2fd111c2c174cb2caac4(
    value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthGrant],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2341864e18588e5c7851d083eef8d86f185425a46cc33ace89aac6bd30f6c48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c21cf4ccbf7357568ec73142a11d82422ee2ff69c984cfe5a7e2e64efce5b1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb37230b328195e67a8ac177f61f4e90b70eb74bc98c4bc21f14db3c4e1025a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f325db5e1082308d810a09f10c6bb123ec8464aa3e6ee9b82aad137cae7fe270(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b806b74384e1073c99b84d1ab705c70d39e344873e5acbd4e665ddd9b059e34(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5166780a43b72b1ccb038038aacce37562a9d2e02c0d2bc75350b6ab1e725213(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efbc2eddf7afa94cb1e7fa60e9ca23216e1989b6b53b24ffdcf7fe50c808bf28(
    value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthRefreshTokenValidity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3671c9791d4f3de3a5f622f6ffb2c7422f4193562034c4d196f2263106885ce2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0602b6d5a2a74e484c0fb6715c03ac2e2da4797e92ce2f794c63c2c4881b909c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b640d1201bc2177a992831e8cc4157363740af9ae06299188e629876dedd0b8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23b14779118a0a86fd296f05d6e2f8eee5b2cd339bc4156eb611129fc8393f6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f7f85c4b35db7c5ff7639a85cbd432ec3632ab2148baedc9a9264eb47790322(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3f2fd4de375c822347be85eb09ef104da3d5007d2c712cc2ab63471a8f4295(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0108c4e8b985e43793d2d2d5282ac013a5d98b068d059478e92c46b6eb7e217b(
    value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputOauthTokenEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e53111252eb27153d149669fe4cc34e8cb801e4e945a1b72bb693a02b2c7b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ae90ac45e2d61ec3ae2eaecf8898ce44824fa461354f9b81693e287d63c2230(
    value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f328e345d8c68304693f2fcd662a97ae36b3417e9e1804b1198037ecf4103890(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d724f5cd873985c458744c6f4f5b4ffac7091f57da48202793477be395a73155(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567d550e53879828ac541279abea954931db2b19333775b346a35143db8aeb95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e47bd880c38b20ee7402447750d9695913a72c994f99a26bd70fc1378048508(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1757e1ab5fd86d30f8f12f6c4b039577ee9423409337b2fd93819fcdb5cf92ca(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ebf30947621154d13b659fdd483a74c31a039a83a6fdb6648e16c728335abcd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad1a0af96f1246f0201d82b6a41fd948833cf9f1926fc740251b03123773b55b(
    value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantDescribeOutputParentIntegration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c8f80b8728c50f8161f7314170a1e1b1ffd6822e166098c16039ea20a54e290(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6487688247e86901fa984e54b9f7db67d0dcf3d2b3c183be9698f765ff08c47(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__810dee316c78b7bc31860e478d75e6f0d3e553eb88bf9e0adbacfb28f9231ae4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2b2e0ed011e42e7c0e981dcf5d3cad0bd3ba3f573d98ff66c3e51051066307(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49ef1956c0bf51d28e0ef714db6ab0116ab3c798d7542dc7bd2e4bdef4ea2025(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5e1b22effe47084d7f538cdf8d38deba196301f26ecd633f80f677cfe8d75e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16eef32e4b98c9134b2a9ed43ff67622fad2f974815d0b3952772b4a7822a29a(
    value: typing.Optional[ApiAuthenticationIntegrationWithAuthorizationCodeGrantShowOutput],
) -> None:
    """Type checking stubs"""
    pass
