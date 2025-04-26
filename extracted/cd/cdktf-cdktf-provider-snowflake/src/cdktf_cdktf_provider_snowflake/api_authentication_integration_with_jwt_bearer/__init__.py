r'''
# `snowflake_api_authentication_integration_with_jwt_bearer`

Refer to the Terraform Registry for docs: [`snowflake_api_authentication_integration_with_jwt_bearer`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer).
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


class ApiAuthenticationIntegrationWithJwtBearer(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearer",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer snowflake_api_authentication_integration_with_jwt_bearer}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        oauth_assertion_issuer: builtins.str,
        oauth_client_id: builtins.str,
        oauth_client_secret: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        oauth_access_token_validity: typing.Optional[jsii.Number] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer snowflake_api_authentication_integration_with_jwt_bearer} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param enabled: Specifies whether this security integration is enabled or disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#enabled ApiAuthenticationIntegrationWithJwtBearer#enabled}
        :param name: Specifies the identifier (i.e. name) for the integration. This value must be unique in your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#name ApiAuthenticationIntegrationWithJwtBearer#name}
        :param oauth_assertion_issuer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_assertion_issuer ApiAuthenticationIntegrationWithJwtBearer#oauth_assertion_issuer}.
        :param oauth_client_id: Specifies the client ID for the OAuth application in the external service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_client_id ApiAuthenticationIntegrationWithJwtBearer#oauth_client_id}
        :param oauth_client_secret: Specifies the client secret for the OAuth application in the ServiceNow instance from the previous step. The connector uses this to request an access token from the ServiceNow instance. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_client_secret ApiAuthenticationIntegrationWithJwtBearer#oauth_client_secret}
        :param comment: Specifies a comment for the integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#comment ApiAuthenticationIntegrationWithJwtBearer#comment}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#id ApiAuthenticationIntegrationWithJwtBearer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param oauth_access_token_validity: Specifies the default lifetime of the OAuth access token (in seconds) issued by an OAuth server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_access_token_validity ApiAuthenticationIntegrationWithJwtBearer#oauth_access_token_validity}
        :param oauth_authorization_endpoint: Specifies the URL for authenticating to the external service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_authorization_endpoint ApiAuthenticationIntegrationWithJwtBearer#oauth_authorization_endpoint}
        :param oauth_client_auth_method: Specifies that POST is used as the authentication method to the external service. If removed from the config, the resource is recreated. Valid values are (case-insensitive): ``CLIENT_SECRET_POST``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_client_auth_method ApiAuthenticationIntegrationWithJwtBearer#oauth_client_auth_method}
        :param oauth_refresh_token_validity: Specifies the value to determine the validity of the refresh token obtained from the OAuth server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_refresh_token_validity ApiAuthenticationIntegrationWithJwtBearer#oauth_refresh_token_validity}
        :param oauth_token_endpoint: Specifies the token endpoint used by the client to obtain an access token by presenting its authorization grant or refresh token. The token endpoint is used with every authorization grant except for the implicit grant type (since an access token is issued directly). If removed from the config, the resource is recreated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_token_endpoint ApiAuthenticationIntegrationWithJwtBearer#oauth_token_endpoint}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aab358670db22bcdfc93f1e7f5abf359a65d41854ff747c6a5fa93c6f694d42)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApiAuthenticationIntegrationWithJwtBearerConfig(
            enabled=enabled,
            name=name,
            oauth_assertion_issuer=oauth_assertion_issuer,
            oauth_client_id=oauth_client_id,
            oauth_client_secret=oauth_client_secret,
            comment=comment,
            id=id,
            oauth_access_token_validity=oauth_access_token_validity,
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
        '''Generates CDKTF code for importing a ApiAuthenticationIntegrationWithJwtBearer resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApiAuthenticationIntegrationWithJwtBearer to import.
        :param import_from_id: The id of the existing ApiAuthenticationIntegrationWithJwtBearer that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApiAuthenticationIntegrationWithJwtBearer to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf1447f067d8cd19db09000352b131c7b930899cb3fb872f58ca5f27f01928fc)
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
    ) -> "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputList":
        return typing.cast("ApiAuthenticationIntegrationWithJwtBearerDescribeOutputList", jsii.get(self, "describeOutput"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "ApiAuthenticationIntegrationWithJwtBearerShowOutputList":
        return typing.cast("ApiAuthenticationIntegrationWithJwtBearerShowOutputList", jsii.get(self, "showOutput"))

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
    @jsii.member(jsii_name="oauthAssertionIssuerInput")
    def oauth_assertion_issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthAssertionIssuerInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e7b290651b6a4f9a484aacfecff984ffebb03fb520bcb3bd33f669e8637433c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5861bfb5ecb2e5882857afa19e69c30bd6fc143e3e0aa4b8552caab8bf9c03ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ceb44cef5468c0f07f253de8f7da0b9938b3a88f2c0a971f170323aafbc338a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25edfabe9571598b80c200b9e747ec8bdce0d59cd0a2cef51c93b3a771a5a7d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthAccessTokenValidity")
    def oauth_access_token_validity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "oauthAccessTokenValidity"))

    @oauth_access_token_validity.setter
    def oauth_access_token_validity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2fff1880d84ab2de89b30cbf06750b7857b7959a7e863ce0c279052127a9c19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthAccessTokenValidity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthAssertionIssuer")
    def oauth_assertion_issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthAssertionIssuer"))

    @oauth_assertion_issuer.setter
    def oauth_assertion_issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f26a354d4d7b16f1d23d0d0a43c1cf2cc2be4f654d9a76040712ee9f98f072ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthAssertionIssuer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthAuthorizationEndpoint")
    def oauth_authorization_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthAuthorizationEndpoint"))

    @oauth_authorization_endpoint.setter
    def oauth_authorization_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4ca457bb792795397d7f72e564a7a6032be0068684f5c671dcccd777809e9b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthAuthorizationEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthClientAuthMethod")
    def oauth_client_auth_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthClientAuthMethod"))

    @oauth_client_auth_method.setter
    def oauth_client_auth_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7bef978787c9bb63ad3c29f96d94a3933e848138516b11325bd99512f936b2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthClientAuthMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthClientId")
    def oauth_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthClientId"))

    @oauth_client_id.setter
    def oauth_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85898ca45b2381cb52b20483479eae473500c70b95555bef22477b50eec59e4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthClientSecret")
    def oauth_client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthClientSecret"))

    @oauth_client_secret.setter
    def oauth_client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4698cf250a54abda52750ff313e12b7351ec899bdeb924d92e1c1e768d69dd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthClientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthRefreshTokenValidity")
    def oauth_refresh_token_validity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "oauthRefreshTokenValidity"))

    @oauth_refresh_token_validity.setter
    def oauth_refresh_token_validity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__240775c1a30c66c5188c46d21e5d712f7da738eec8ab234046f38923d8534ec4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthRefreshTokenValidity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthTokenEndpoint")
    def oauth_token_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthTokenEndpoint"))

    @oauth_token_endpoint.setter
    def oauth_token_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78d8812b75d23cca59ae233ac519e11b69a1d79f623dbfbf4bf449a82949bb1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthTokenEndpoint", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerConfig",
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
        "oauth_assertion_issuer": "oauthAssertionIssuer",
        "oauth_client_id": "oauthClientId",
        "oauth_client_secret": "oauthClientSecret",
        "comment": "comment",
        "id": "id",
        "oauth_access_token_validity": "oauthAccessTokenValidity",
        "oauth_authorization_endpoint": "oauthAuthorizationEndpoint",
        "oauth_client_auth_method": "oauthClientAuthMethod",
        "oauth_refresh_token_validity": "oauthRefreshTokenValidity",
        "oauth_token_endpoint": "oauthTokenEndpoint",
    },
)
class ApiAuthenticationIntegrationWithJwtBearerConfig(
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
        oauth_assertion_issuer: builtins.str,
        oauth_client_id: builtins.str,
        oauth_client_secret: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        oauth_access_token_validity: typing.Optional[jsii.Number] = None,
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
        :param enabled: Specifies whether this security integration is enabled or disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#enabled ApiAuthenticationIntegrationWithJwtBearer#enabled}
        :param name: Specifies the identifier (i.e. name) for the integration. This value must be unique in your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#name ApiAuthenticationIntegrationWithJwtBearer#name}
        :param oauth_assertion_issuer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_assertion_issuer ApiAuthenticationIntegrationWithJwtBearer#oauth_assertion_issuer}.
        :param oauth_client_id: Specifies the client ID for the OAuth application in the external service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_client_id ApiAuthenticationIntegrationWithJwtBearer#oauth_client_id}
        :param oauth_client_secret: Specifies the client secret for the OAuth application in the ServiceNow instance from the previous step. The connector uses this to request an access token from the ServiceNow instance. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_client_secret ApiAuthenticationIntegrationWithJwtBearer#oauth_client_secret}
        :param comment: Specifies a comment for the integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#comment ApiAuthenticationIntegrationWithJwtBearer#comment}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#id ApiAuthenticationIntegrationWithJwtBearer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param oauth_access_token_validity: Specifies the default lifetime of the OAuth access token (in seconds) issued by an OAuth server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_access_token_validity ApiAuthenticationIntegrationWithJwtBearer#oauth_access_token_validity}
        :param oauth_authorization_endpoint: Specifies the URL for authenticating to the external service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_authorization_endpoint ApiAuthenticationIntegrationWithJwtBearer#oauth_authorization_endpoint}
        :param oauth_client_auth_method: Specifies that POST is used as the authentication method to the external service. If removed from the config, the resource is recreated. Valid values are (case-insensitive): ``CLIENT_SECRET_POST``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_client_auth_method ApiAuthenticationIntegrationWithJwtBearer#oauth_client_auth_method}
        :param oauth_refresh_token_validity: Specifies the value to determine the validity of the refresh token obtained from the OAuth server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_refresh_token_validity ApiAuthenticationIntegrationWithJwtBearer#oauth_refresh_token_validity}
        :param oauth_token_endpoint: Specifies the token endpoint used by the client to obtain an access token by presenting its authorization grant or refresh token. The token endpoint is used with every authorization grant except for the implicit grant type (since an access token is issued directly). If removed from the config, the resource is recreated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_token_endpoint ApiAuthenticationIntegrationWithJwtBearer#oauth_token_endpoint}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860042642c23480ad82f298ebd9bb61f0c1d67ecdaa51de1c1159c52a57d19f9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument oauth_assertion_issuer", value=oauth_assertion_issuer, expected_type=type_hints["oauth_assertion_issuer"])
            check_type(argname="argument oauth_client_id", value=oauth_client_id, expected_type=type_hints["oauth_client_id"])
            check_type(argname="argument oauth_client_secret", value=oauth_client_secret, expected_type=type_hints["oauth_client_secret"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument oauth_access_token_validity", value=oauth_access_token_validity, expected_type=type_hints["oauth_access_token_validity"])
            check_type(argname="argument oauth_authorization_endpoint", value=oauth_authorization_endpoint, expected_type=type_hints["oauth_authorization_endpoint"])
            check_type(argname="argument oauth_client_auth_method", value=oauth_client_auth_method, expected_type=type_hints["oauth_client_auth_method"])
            check_type(argname="argument oauth_refresh_token_validity", value=oauth_refresh_token_validity, expected_type=type_hints["oauth_refresh_token_validity"])
            check_type(argname="argument oauth_token_endpoint", value=oauth_token_endpoint, expected_type=type_hints["oauth_token_endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "name": name,
            "oauth_assertion_issuer": oauth_assertion_issuer,
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#enabled ApiAuthenticationIntegrationWithJwtBearer#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the identifier (i.e. name) for the integration. This value must be unique in your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#name ApiAuthenticationIntegrationWithJwtBearer#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oauth_assertion_issuer(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_assertion_issuer ApiAuthenticationIntegrationWithJwtBearer#oauth_assertion_issuer}.'''
        result = self._values.get("oauth_assertion_issuer")
        assert result is not None, "Required property 'oauth_assertion_issuer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oauth_client_id(self) -> builtins.str:
        '''Specifies the client ID for the OAuth application in the external service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_client_id ApiAuthenticationIntegrationWithJwtBearer#oauth_client_id}
        '''
        result = self._values.get("oauth_client_id")
        assert result is not None, "Required property 'oauth_client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oauth_client_secret(self) -> builtins.str:
        '''Specifies the client secret for the OAuth application in the ServiceNow instance from the previous step.

        The connector uses this to request an access token from the ServiceNow instance. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_client_secret ApiAuthenticationIntegrationWithJwtBearer#oauth_client_secret}
        '''
        result = self._values.get("oauth_client_secret")
        assert result is not None, "Required property 'oauth_client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the integration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#comment ApiAuthenticationIntegrationWithJwtBearer#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#id ApiAuthenticationIntegrationWithJwtBearer#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_access_token_validity(self) -> typing.Optional[jsii.Number]:
        '''Specifies the default lifetime of the OAuth access token (in seconds) issued by an OAuth server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_access_token_validity ApiAuthenticationIntegrationWithJwtBearer#oauth_access_token_validity}
        '''
        result = self._values.get("oauth_access_token_validity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def oauth_authorization_endpoint(self) -> typing.Optional[builtins.str]:
        '''Specifies the URL for authenticating to the external service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_authorization_endpoint ApiAuthenticationIntegrationWithJwtBearer#oauth_authorization_endpoint}
        '''
        result = self._values.get("oauth_authorization_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_client_auth_method(self) -> typing.Optional[builtins.str]:
        '''Specifies that POST is used as the authentication method to the external service.

        If removed from the config, the resource is recreated. Valid values are (case-insensitive): ``CLIENT_SECRET_POST``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_client_auth_method ApiAuthenticationIntegrationWithJwtBearer#oauth_client_auth_method}
        '''
        result = self._values.get("oauth_client_auth_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_refresh_token_validity(self) -> typing.Optional[jsii.Number]:
        '''Specifies the value to determine the validity of the refresh token obtained from the OAuth server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_refresh_token_validity ApiAuthenticationIntegrationWithJwtBearer#oauth_refresh_token_validity}
        '''
        result = self._values.get("oauth_refresh_token_validity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def oauth_token_endpoint(self) -> typing.Optional[builtins.str]:
        '''Specifies the token endpoint used by the client to obtain an access token by presenting its authorization grant or refresh token.

        The token endpoint is used with every authorization grant except for the implicit grant type (since an access token is issued directly). If removed from the config, the resource is recreated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_authentication_integration_with_jwt_bearer#oauth_token_endpoint ApiAuthenticationIntegrationWithJwtBearer#oauth_token_endpoint}
        '''
        result = self._values.get("oauth_token_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithJwtBearerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithJwtBearerDescribeOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithJwtBearerDescribeOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputAuthType",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputAuthType:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputAuthType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputAuthTypeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputAuthTypeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56696820c3701f125f5403f55e720596b7a5fa5c869115be5687faab005c7180)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputAuthTypeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c360b2d2bb94ae48e5635ebe5d0f79b06189e8833fd1eb75b11125063ab8525c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithJwtBearerDescribeOutputAuthTypeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__657027f8574de42ce51e11a6b29e57937076588e9c561e5b71da52fa21175f3f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b45fdc8ae3389ab0e3a7ce167ee9ed5942caab611243be82b1ca323fb06dfb8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcff786842d2a7ca15314541ac27c5450537dd9b0d881f7385dc1d60a9043b3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputAuthTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputAuthTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db7408b0f3403bb4d7cbe35268b0f2f29828658add4d1f7791e1bd62b97fe7e9)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputAuthType]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputAuthType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputAuthType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25a340f50118395909adf650490fcc1a2c1eba73c78706883e59d9cfcc8db73b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputComment",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputComment:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputComment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputCommentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputCommentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2be749bb4e6a673229cdb3f5b6aa71cae8de194fd4695cda6f7b7f5eca1b0700)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputCommentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c589ba5f20dc84aeae873e0cf361e54b985be27beb8d658511dd936e803ec6bf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithJwtBearerDescribeOutputCommentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f15ad4b9565a529b13a4296b009accafcd92ab1656da996feaac2a7a5b34a2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__694e578feceecd36f416b2ce57e516fba06866d17b31c2ee8cb8964c981bdb9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__082dbff2717d6d9a04ef73b79f796324794c501f34c95caa14789afdc03d8ce0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputCommentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputCommentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f4e66c9e09775f8334b43aed9b8d3fc9afd07e13c6fba0f580f9144f74ca0d9)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputComment]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputComment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputComment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f199a60c794cdf6940435faddb42e600b1001c46de3c5a526ce7f69f3513cf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputEnabled",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputEnabled:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputEnabled(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputEnabledList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputEnabledList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b4a12b30a565b28c3eb8ef098211ba00251bf377e19ca8f03f3f7f917ef3a65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputEnabledOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__187615bc84a692ee9f256ab71f3641fd402cfe81506ae299b92081b9112f3d39)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithJwtBearerDescribeOutputEnabledOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8928cc0a7ab3b5b5b162dd100f0b3f13e5e90b04721bdfe6a023f2fb36d298b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed692b87b9d62c22172ad5ee0f7001887bab6e4dfd84bafe0d01f37736cd5a79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a3bec86918d7d83ec33c4bdc192a38ef8db3bc32faeb230584d1517621f4bc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputEnabledOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputEnabledOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0148000a4250d64354ee8cca9de3ce8b09c0a5761aac71affb6c7df7fc7ecd4)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputEnabled]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputEnabled], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputEnabled],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bab73c93f04c305a0198186bf20d27a5fcdfefeba8610fc0bc1781f5b185bd31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab8e96d556b796a99860b0d8561abe0a5be58fffeede94a42fcac0f65b60e595)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3816ab39b4d06285c28c95c3528eb1ee6112b8b4bd9138cbfaec76d1fe92f838)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a5cb0a1e56da7122234410811f73614d6015a000d701a229574dd2d25a0be9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00257592c4932bf9401f65201ed49c7253d3e3070a099057c7b1a91d30298f29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef02c1125b7dfec073f14954b45a888abfe4bfc6d3163bf05123716380b15f86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAccessTokenValidity",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAccessTokenValidity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAccessTokenValidity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAccessTokenValidityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAccessTokenValidityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aefb4cd1c75e6db9589076279c522e5415af36715e7c3452dfa1f12ee063dff1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAccessTokenValidityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__971eadef843bf9a7fd890d0ecde5d003f1907c1dfe8ecf413806d1eda6c8a709)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAccessTokenValidityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__486e09f938fee519a3ffdf12b1a0dea7fa87fef25564421b91cb152c01638168)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6d1ff0b18014afd8c6f25f4cd3a30f3c149fa2a53f2d401c59416a98f4592ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d7d2561db2642095df0f016b28c1e082141a999c8b0ab983461d9fce8283f2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAccessTokenValidityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAccessTokenValidityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ab8365418e97331cc8a9dd89b7fae515d56c8c0aa0ed011c208dc329160adb2)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAccessTokenValidity]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAccessTokenValidity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAccessTokenValidity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac2b6fa29b385930426bda08b9752e5acfb69ac4d7d15015042b0fda5c1b4d19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAllowedScopes",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAllowedScopes:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAllowedScopes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAllowedScopesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAllowedScopesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__797896729d7ff9d3833b263e89c48e5b3903455283e24a028562df91819db3c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAllowedScopesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f149cdb90769fc3178615557656a5ac06b7c9aac97df7a4715457667d6aa15ff)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAllowedScopesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e882ca631fcc14b78584430fc47a0313df0e992296e5aaedc684b1f9dd0e5e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09b1a3c0c290c388cc541c16250b90e203ed65984108efcc2cc67526c5836a0e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38d925e0c41fb852c28af4b743b3e643e7ecf9af3a7df657c118f3f159f471a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAllowedScopesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAllowedScopesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__868c50fd586c6b28915544fe7ee36aa6bdaf99f564d53dddcad930061d76d7eb)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAllowedScopes]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAllowedScopes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAllowedScopes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__689ab9ae07a35a88cd2f2757ff35ce79beaeede51798207d97c95c5d373b90e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAuthorizationEndpoint",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAuthorizationEndpoint:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAuthorizationEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAuthorizationEndpointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAuthorizationEndpointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50b9767e2fd602dc9d2980319ecb5b654e6cd679a1467769584ca0e8ff33eaca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAuthorizationEndpointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e34e69bad2e91bf1c72ee60c682f42707e25018d45179ef14e01d4b1fd8a3906)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAuthorizationEndpointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9f3c49216a8d7d7c0156033905628f99d0bbe1a3ab7a9bcf6646f71669af85a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__297401fd52ca65a83b83107d190fe5a82926aaf06e3172e33165494e57c96dab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdddf731415fc78aabdee0e98bee2bce5de67bd7aa3be7883d30eb1a0f930cf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAuthorizationEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAuthorizationEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efffa23d122bfbb3474bc53354019ddf3047a5eb7d7640ff1fa0f8a551c6d55d)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAuthorizationEndpoint]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAuthorizationEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAuthorizationEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__912086d962c8f902046f562951a5c0f5f575cd592547432507569b7d897a7741)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientAuthMethod",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientAuthMethod:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientAuthMethod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientAuthMethodList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientAuthMethodList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a9c0c64c48c0f9326339a1d3683f94e1b106ed0cd63a7f95aeff4133d887a0c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientAuthMethodOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b3fabbe4fb99742f03db2f2878a78fe5af63574debb8d2b5280be1282059674)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientAuthMethodOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f62a07511aff5a1e104e19def20829c5ed28c523465b1dae370e4a60f1cf335)
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
            type_hints = typing.get_type_hints(_typecheckingstub__523eb0ae7369dcfde3e18752b42f58cefcd5f434c0f3e5af79e6c399741c18ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e12ac73759bd90bc93b82963c2afd58f6cac5fbc80d15666ea0654cf3f3ba8bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientAuthMethodOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientAuthMethodOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c13ce58383bcdea351ced3a334a10d317e6adbefcf52e2d1e2ecc5e9448cbe04)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientAuthMethod]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientAuthMethod], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientAuthMethod],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e9d3090f45e4243dd06ffc7da876d5e0b3c32519ed307fcec2a9257b6e17ed6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientId",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientId:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientIdList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientIdList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c2a293c85551febd8275276afb3f75d11afeba6bd7214d2f8a66f94db46d547)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientIdOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2576a8bdfd8a5b1026e3b355a59fc44219d751f629e814be849db7f0a279cd7a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientIdOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75aa66f68141a1a4ab77f45ccce8468e5c750ff3e65df5ebc84f7529ddda48a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__657cd0a390b99e05049e2ad7d0df1ba1559fbe51b9bd017e85bfec2cbc2bf301)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42f334dd7ec25a661ced726856781f26a2aa70c5f1c225e3852469e2dc530805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__109abc09a667173b7581b2875c3eca7182890a03260e26f802de107cb15ed02b)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientId]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c8b198e6f6c3ade82ac89a3302b1c82979e60adf72b5019d1fbec5733a0f5c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthGrant",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthGrant:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthGrant(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthGrantList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthGrantList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d74f95406a6f07facd98dfb6596a578d0478456f5882bbbd7d2813ecbb731a4d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthGrantOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e646d7e17bc1db4e70f9ebc0dccb8866547e1cdb05f184b247f9a7f50d52d6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthGrantOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c35fe62a3ff31672ea527093cd5f7bbdd01d513f3e5679a78012a3fae32433d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1698ac4f1fb8c47f65490c3c8041a23dfe551ce7c09d4a2a8b1560ca98d92ad6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abed2b1faef879ab252a87f9b4fdd595fe3978a7a11918bab208bf88105bdb53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthGrantOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthGrantOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d0364ad2155a9ef5fd96b63e33ece01f60d4d39faa665aba854660a1600386d)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthGrant]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthGrant], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthGrant],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6382cf8938f975a8128e5426138b69793a99f3493215bea2c69ef97b2963047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthRefreshTokenValidity",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthRefreshTokenValidity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthRefreshTokenValidity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthRefreshTokenValidityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthRefreshTokenValidityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6dff6ea63640f22fd9e0d131657782eceb30196c0eac053d56abc3d4c0bd8a8a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthRefreshTokenValidityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4b2f8247d11b5898e326e90c661f88f52d3033a3ad21aa1389b8fab5f5bc063)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthRefreshTokenValidityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc5c86b84d6b31c52466a00fe845d7e09367f9438813001e8020b521ba8353c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c819e3d752d42407f11f32ad7471bc55aa345168d6bb0ba21b593f32b3ba1698)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3aec6f5ca6a250b4874a936b1fbef9b9945abbc9ee835968abd85e06c38ca18c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthRefreshTokenValidityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthRefreshTokenValidityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb22fae5eb61e8264302884fbc77d36217dfbf66f68dc4a32ea687b3c7151c0d)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthRefreshTokenValidity]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthRefreshTokenValidity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthRefreshTokenValidity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4561225f8fca4402a4fab6bdb8f25280a093058b02258f8af87519c357074e48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthTokenEndpoint",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthTokenEndpoint:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthTokenEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthTokenEndpointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthTokenEndpointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f6224ff94346aedbf886bca8120a6bd8f3615f10294b029c9bcbd2b0062ab50)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthTokenEndpointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c8dcd100751614e04ff5e88288b733a5b58819f1088448e0067ef287aa5247c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthTokenEndpointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a653eff107296caaff01851820d80690de90c60428cb214e29f8927d1a3bf6db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d95f98131ef005920964ad1b0213ef863215aea0d3755c344cad0725c702fa9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37f0500bda0675de720c062e63728934c2eccc595d2913fe861676f76dcfb226)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthTokenEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthTokenEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ee1761453f3df972419434e86eedc210fc8a3de3fc333bc3312e5edcdfcddb7)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthTokenEndpoint]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthTokenEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthTokenEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b8ab948ace1948dde4131c1d67be03fcd0e70d4d808333cabea4febd768924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32903a04206c60be5f9115d577091dc262128ba40f663957871715e894fb1088)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(
        self,
    ) -> ApiAuthenticationIntegrationWithJwtBearerDescribeOutputAuthTypeList:
        return typing.cast(ApiAuthenticationIntegrationWithJwtBearerDescribeOutputAuthTypeList, jsii.get(self, "authType"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(
        self,
    ) -> ApiAuthenticationIntegrationWithJwtBearerDescribeOutputCommentList:
        return typing.cast(ApiAuthenticationIntegrationWithJwtBearerDescribeOutputCommentList, jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> ApiAuthenticationIntegrationWithJwtBearerDescribeOutputEnabledList:
        return typing.cast(ApiAuthenticationIntegrationWithJwtBearerDescribeOutputEnabledList, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="oauthAccessTokenValidity")
    def oauth_access_token_validity(
        self,
    ) -> ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAccessTokenValidityList:
        return typing.cast(ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAccessTokenValidityList, jsii.get(self, "oauthAccessTokenValidity"))

    @builtins.property
    @jsii.member(jsii_name="oauthAllowedScopes")
    def oauth_allowed_scopes(
        self,
    ) -> ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAllowedScopesList:
        return typing.cast(ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAllowedScopesList, jsii.get(self, "oauthAllowedScopes"))

    @builtins.property
    @jsii.member(jsii_name="oauthAuthorizationEndpoint")
    def oauth_authorization_endpoint(
        self,
    ) -> ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAuthorizationEndpointList:
        return typing.cast(ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAuthorizationEndpointList, jsii.get(self, "oauthAuthorizationEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientAuthMethod")
    def oauth_client_auth_method(
        self,
    ) -> ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientAuthMethodList:
        return typing.cast(ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientAuthMethodList, jsii.get(self, "oauthClientAuthMethod"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientId")
    def oauth_client_id(
        self,
    ) -> ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientIdList:
        return typing.cast(ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientIdList, jsii.get(self, "oauthClientId"))

    @builtins.property
    @jsii.member(jsii_name="oauthGrant")
    def oauth_grant(
        self,
    ) -> ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthGrantList:
        return typing.cast(ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthGrantList, jsii.get(self, "oauthGrant"))

    @builtins.property
    @jsii.member(jsii_name="oauthRefreshTokenValidity")
    def oauth_refresh_token_validity(
        self,
    ) -> ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthRefreshTokenValidityList:
        return typing.cast(ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthRefreshTokenValidityList, jsii.get(self, "oauthRefreshTokenValidity"))

    @builtins.property
    @jsii.member(jsii_name="oauthTokenEndpoint")
    def oauth_token_endpoint(
        self,
    ) -> ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthTokenEndpointList:
        return typing.cast(ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthTokenEndpointList, jsii.get(self, "oauthTokenEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="parentIntegration")
    def parent_integration(
        self,
    ) -> "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputParentIntegrationList":
        return typing.cast("ApiAuthenticationIntegrationWithJwtBearerDescribeOutputParentIntegrationList", jsii.get(self, "parentIntegration"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutput]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__719efcb2f5f7b6cc5d5b853b2d5431a1a89f6cfccb1499151d2c6cd72e8479c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputParentIntegration",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputParentIntegration:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputParentIntegration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputParentIntegrationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputParentIntegrationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33aa62f1a2dcd4c41e8bf2eb57c0afa490cb769077d67709431c8ea684e72de6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputParentIntegrationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3591675f4340bd40cdccf46493eca68433de3a3c07c1d72d97bc79be3f5518b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithJwtBearerDescribeOutputParentIntegrationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8220a3447f22f4a6ab5893bf6716d96e4bdb05e3d90eb3a9c938276b7c50174d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cde835a24ddbfe143d9ad1fe58229124750516e3a438e7cc24664749833119a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2df9b87e25947485419270338d784d32eacb3e38e42f7996e077f5424b7b5894)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithJwtBearerDescribeOutputParentIntegrationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerDescribeOutputParentIntegrationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0de566fa2a4c33d939c5c40ab005b20e5d056f2dd7aa692686420b60ee2b1691)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputParentIntegration]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputParentIntegration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputParentIntegration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f191da2d5b248145fa5b7716111756c13711fb8a6bfd5bbee892d1b51627b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApiAuthenticationIntegrationWithJwtBearerShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiAuthenticationIntegrationWithJwtBearerShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiAuthenticationIntegrationWithJwtBearerShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ce29dec99e0a94dee05f9c5d2948eb64cd6aa5473b7eab312312e82a984dfa9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiAuthenticationIntegrationWithJwtBearerShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f93a7a43c7837c4ddbbd0ae34abbe3add0020a6ad75f1bd61d613f047df7f44)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiAuthenticationIntegrationWithJwtBearerShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0ee616b8911dd7e88d86231ed6bdf9ea6c1a27ab6faea37c2d61912c0517c62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c0f7b6b1126f206914df661ef5c9b8c330a6c60a0343e2b7f7af8222d52cd8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fc1168bdca5e04a9ed04e68f3319f8df6c166be2f7a75a45eb85bfebc7a0082)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApiAuthenticationIntegrationWithJwtBearerShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiAuthenticationIntegrationWithJwtBearer.ApiAuthenticationIntegrationWithJwtBearerShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__58eedc4caf4610ed8044e7b058b744bed62a1d50fbbd003c1712dc318ab71e7c)
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
    ) -> typing.Optional[ApiAuthenticationIntegrationWithJwtBearerShowOutput]:
        return typing.cast(typing.Optional[ApiAuthenticationIntegrationWithJwtBearerShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerShowOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27be1f761e63e0566c6967671d00b7905bf0d85479c760d71880f5ea6c00b09d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApiAuthenticationIntegrationWithJwtBearer",
    "ApiAuthenticationIntegrationWithJwtBearerConfig",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutput",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputAuthType",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputAuthTypeList",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputAuthTypeOutputReference",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputComment",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputCommentList",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputCommentOutputReference",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputEnabled",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputEnabledList",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputEnabledOutputReference",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputList",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAccessTokenValidity",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAccessTokenValidityList",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAccessTokenValidityOutputReference",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAllowedScopes",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAllowedScopesList",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAllowedScopesOutputReference",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAuthorizationEndpoint",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAuthorizationEndpointList",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAuthorizationEndpointOutputReference",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientAuthMethod",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientAuthMethodList",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientAuthMethodOutputReference",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientId",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientIdList",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientIdOutputReference",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthGrant",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthGrantList",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthGrantOutputReference",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthRefreshTokenValidity",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthRefreshTokenValidityList",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthRefreshTokenValidityOutputReference",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthTokenEndpoint",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthTokenEndpointList",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthTokenEndpointOutputReference",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOutputReference",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputParentIntegration",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputParentIntegrationList",
    "ApiAuthenticationIntegrationWithJwtBearerDescribeOutputParentIntegrationOutputReference",
    "ApiAuthenticationIntegrationWithJwtBearerShowOutput",
    "ApiAuthenticationIntegrationWithJwtBearerShowOutputList",
    "ApiAuthenticationIntegrationWithJwtBearerShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__4aab358670db22bcdfc93f1e7f5abf359a65d41854ff747c6a5fa93c6f694d42(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    oauth_assertion_issuer: builtins.str,
    oauth_client_id: builtins.str,
    oauth_client_secret: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    oauth_access_token_validity: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__cf1447f067d8cd19db09000352b131c7b930899cb3fb872f58ca5f27f01928fc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b290651b6a4f9a484aacfecff984ffebb03fb520bcb3bd33f669e8637433c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5861bfb5ecb2e5882857afa19e69c30bd6fc143e3e0aa4b8552caab8bf9c03ef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ceb44cef5468c0f07f253de8f7da0b9938b3a88f2c0a971f170323aafbc338a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25edfabe9571598b80c200b9e747ec8bdce0d59cd0a2cef51c93b3a771a5a7d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2fff1880d84ab2de89b30cbf06750b7857b7959a7e863ce0c279052127a9c19(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f26a354d4d7b16f1d23d0d0a43c1cf2cc2be4f654d9a76040712ee9f98f072ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ca457bb792795397d7f72e564a7a6032be0068684f5c671dcccd777809e9b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7bef978787c9bb63ad3c29f96d94a3933e848138516b11325bd99512f936b2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85898ca45b2381cb52b20483479eae473500c70b95555bef22477b50eec59e4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4698cf250a54abda52750ff313e12b7351ec899bdeb924d92e1c1e768d69dd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__240775c1a30c66c5188c46d21e5d712f7da738eec8ab234046f38923d8534ec4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78d8812b75d23cca59ae233ac519e11b69a1d79f623dbfbf4bf449a82949bb1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860042642c23480ad82f298ebd9bb61f0c1d67ecdaa51de1c1159c52a57d19f9(
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
    oauth_assertion_issuer: builtins.str,
    oauth_client_id: builtins.str,
    oauth_client_secret: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    oauth_access_token_validity: typing.Optional[jsii.Number] = None,
    oauth_authorization_endpoint: typing.Optional[builtins.str] = None,
    oauth_client_auth_method: typing.Optional[builtins.str] = None,
    oauth_refresh_token_validity: typing.Optional[jsii.Number] = None,
    oauth_token_endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56696820c3701f125f5403f55e720596b7a5fa5c869115be5687faab005c7180(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c360b2d2bb94ae48e5635ebe5d0f79b06189e8833fd1eb75b11125063ab8525c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__657027f8574de42ce51e11a6b29e57937076588e9c561e5b71da52fa21175f3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b45fdc8ae3389ab0e3a7ce167ee9ed5942caab611243be82b1ca323fb06dfb8b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcff786842d2a7ca15314541ac27c5450537dd9b0d881f7385dc1d60a9043b3e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db7408b0f3403bb4d7cbe35268b0f2f29828658add4d1f7791e1bd62b97fe7e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a340f50118395909adf650490fcc1a2c1eba73c78706883e59d9cfcc8db73b(
    value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputAuthType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2be749bb4e6a673229cdb3f5b6aa71cae8de194fd4695cda6f7b7f5eca1b0700(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c589ba5f20dc84aeae873e0cf361e54b985be27beb8d658511dd936e803ec6bf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f15ad4b9565a529b13a4296b009accafcd92ab1656da996feaac2a7a5b34a2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__694e578feceecd36f416b2ce57e516fba06866d17b31c2ee8cb8964c981bdb9f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__082dbff2717d6d9a04ef73b79f796324794c501f34c95caa14789afdc03d8ce0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f4e66c9e09775f8334b43aed9b8d3fc9afd07e13c6fba0f580f9144f74ca0d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f199a60c794cdf6940435faddb42e600b1001c46de3c5a526ce7f69f3513cf8(
    value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputComment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4a12b30a565b28c3eb8ef098211ba00251bf377e19ca8f03f3f7f917ef3a65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187615bc84a692ee9f256ab71f3641fd402cfe81506ae299b92081b9112f3d39(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8928cc0a7ab3b5b5b162dd100f0b3f13e5e90b04721bdfe6a023f2fb36d298b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed692b87b9d62c22172ad5ee0f7001887bab6e4dfd84bafe0d01f37736cd5a79(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a3bec86918d7d83ec33c4bdc192a38ef8db3bc32faeb230584d1517621f4bc6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0148000a4250d64354ee8cca9de3ce8b09c0a5761aac71affb6c7df7fc7ecd4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bab73c93f04c305a0198186bf20d27a5fcdfefeba8610fc0bc1781f5b185bd31(
    value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputEnabled],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab8e96d556b796a99860b0d8561abe0a5be58fffeede94a42fcac0f65b60e595(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3816ab39b4d06285c28c95c3528eb1ee6112b8b4bd9138cbfaec76d1fe92f838(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5cb0a1e56da7122234410811f73614d6015a000d701a229574dd2d25a0be9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00257592c4932bf9401f65201ed49c7253d3e3070a099057c7b1a91d30298f29(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef02c1125b7dfec073f14954b45a888abfe4bfc6d3163bf05123716380b15f86(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aefb4cd1c75e6db9589076279c522e5415af36715e7c3452dfa1f12ee063dff1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__971eadef843bf9a7fd890d0ecde5d003f1907c1dfe8ecf413806d1eda6c8a709(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__486e09f938fee519a3ffdf12b1a0dea7fa87fef25564421b91cb152c01638168(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6d1ff0b18014afd8c6f25f4cd3a30f3c149fa2a53f2d401c59416a98f4592ce(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d7d2561db2642095df0f016b28c1e082141a999c8b0ab983461d9fce8283f2e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ab8365418e97331cc8a9dd89b7fae515d56c8c0aa0ed011c208dc329160adb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac2b6fa29b385930426bda08b9752e5acfb69ac4d7d15015042b0fda5c1b4d19(
    value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAccessTokenValidity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797896729d7ff9d3833b263e89c48e5b3903455283e24a028562df91819db3c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f149cdb90769fc3178615557656a5ac06b7c9aac97df7a4715457667d6aa15ff(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e882ca631fcc14b78584430fc47a0313df0e992296e5aaedc684b1f9dd0e5e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b1a3c0c290c388cc541c16250b90e203ed65984108efcc2cc67526c5836a0e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38d925e0c41fb852c28af4b743b3e643e7ecf9af3a7df657c118f3f159f471a3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868c50fd586c6b28915544fe7ee36aa6bdaf99f564d53dddcad930061d76d7eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__689ab9ae07a35a88cd2f2757ff35ce79beaeede51798207d97c95c5d373b90e5(
    value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAllowedScopes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b9767e2fd602dc9d2980319ecb5b654e6cd679a1467769584ca0e8ff33eaca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34e69bad2e91bf1c72ee60c682f42707e25018d45179ef14e01d4b1fd8a3906(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f3c49216a8d7d7c0156033905628f99d0bbe1a3ab7a9bcf6646f71669af85a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297401fd52ca65a83b83107d190fe5a82926aaf06e3172e33165494e57c96dab(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdddf731415fc78aabdee0e98bee2bce5de67bd7aa3be7883d30eb1a0f930cf4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efffa23d122bfbb3474bc53354019ddf3047a5eb7d7640ff1fa0f8a551c6d55d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__912086d962c8f902046f562951a5c0f5f575cd592547432507569b7d897a7741(
    value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthAuthorizationEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9c0c64c48c0f9326339a1d3683f94e1b106ed0cd63a7f95aeff4133d887a0c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3fabbe4fb99742f03db2f2878a78fe5af63574debb8d2b5280be1282059674(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f62a07511aff5a1e104e19def20829c5ed28c523465b1dae370e4a60f1cf335(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__523eb0ae7369dcfde3e18752b42f58cefcd5f434c0f3e5af79e6c399741c18ba(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12ac73759bd90bc93b82963c2afd58f6cac5fbc80d15666ea0654cf3f3ba8bf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13ce58383bcdea351ced3a334a10d317e6adbefcf52e2d1e2ecc5e9448cbe04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e9d3090f45e4243dd06ffc7da876d5e0b3c32519ed307fcec2a9257b6e17ed6(
    value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientAuthMethod],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2a293c85551febd8275276afb3f75d11afeba6bd7214d2f8a66f94db46d547(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2576a8bdfd8a5b1026e3b355a59fc44219d751f629e814be849db7f0a279cd7a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75aa66f68141a1a4ab77f45ccce8468e5c750ff3e65df5ebc84f7529ddda48a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__657cd0a390b99e05049e2ad7d0df1ba1559fbe51b9bd017e85bfec2cbc2bf301(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f334dd7ec25a661ced726856781f26a2aa70c5f1c225e3852469e2dc530805(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__109abc09a667173b7581b2875c3eca7182890a03260e26f802de107cb15ed02b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c8b198e6f6c3ade82ac89a3302b1c82979e60adf72b5019d1fbec5733a0f5c5(
    value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthClientId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d74f95406a6f07facd98dfb6596a578d0478456f5882bbbd7d2813ecbb731a4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e646d7e17bc1db4e70f9ebc0dccb8866547e1cdb05f184b247f9a7f50d52d6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c35fe62a3ff31672ea527093cd5f7bbdd01d513f3e5679a78012a3fae32433d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1698ac4f1fb8c47f65490c3c8041a23dfe551ce7c09d4a2a8b1560ca98d92ad6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abed2b1faef879ab252a87f9b4fdd595fe3978a7a11918bab208bf88105bdb53(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d0364ad2155a9ef5fd96b63e33ece01f60d4d39faa665aba854660a1600386d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6382cf8938f975a8128e5426138b69793a99f3493215bea2c69ef97b2963047(
    value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthGrant],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dff6ea63640f22fd9e0d131657782eceb30196c0eac053d56abc3d4c0bd8a8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b2f8247d11b5898e326e90c661f88f52d3033a3ad21aa1389b8fab5f5bc063(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc5c86b84d6b31c52466a00fe845d7e09367f9438813001e8020b521ba8353c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c819e3d752d42407f11f32ad7471bc55aa345168d6bb0ba21b593f32b3ba1698(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aec6f5ca6a250b4874a936b1fbef9b9945abbc9ee835968abd85e06c38ca18c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb22fae5eb61e8264302884fbc77d36217dfbf66f68dc4a32ea687b3c7151c0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4561225f8fca4402a4fab6bdb8f25280a093058b02258f8af87519c357074e48(
    value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthRefreshTokenValidity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6224ff94346aedbf886bca8120a6bd8f3615f10294b029c9bcbd2b0062ab50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c8dcd100751614e04ff5e88288b733a5b58819f1088448e0067ef287aa5247c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a653eff107296caaff01851820d80690de90c60428cb214e29f8927d1a3bf6db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d95f98131ef005920964ad1b0213ef863215aea0d3755c344cad0725c702fa9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f0500bda0675de720c062e63728934c2eccc595d2913fe861676f76dcfb226(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee1761453f3df972419434e86eedc210fc8a3de3fc333bc3312e5edcdfcddb7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b8ab948ace1948dde4131c1d67be03fcd0e70d4d808333cabea4febd768924(
    value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputOauthTokenEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32903a04206c60be5f9115d577091dc262128ba40f663957871715e894fb1088(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__719efcb2f5f7b6cc5d5b853b2d5431a1a89f6cfccb1499151d2c6cd72e8479c2(
    value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33aa62f1a2dcd4c41e8bf2eb57c0afa490cb769077d67709431c8ea684e72de6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3591675f4340bd40cdccf46493eca68433de3a3c07c1d72d97bc79be3f5518b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8220a3447f22f4a6ab5893bf6716d96e4bdb05e3d90eb3a9c938276b7c50174d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cde835a24ddbfe143d9ad1fe58229124750516e3a438e7cc24664749833119a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2df9b87e25947485419270338d784d32eacb3e38e42f7996e077f5424b7b5894(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0de566fa2a4c33d939c5c40ab005b20e5d056f2dd7aa692686420b60ee2b1691(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f191da2d5b248145fa5b7716111756c13711fb8a6bfd5bbee892d1b51627b5(
    value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerDescribeOutputParentIntegration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ce29dec99e0a94dee05f9c5d2948eb64cd6aa5473b7eab312312e82a984dfa9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f93a7a43c7837c4ddbbd0ae34abbe3add0020a6ad75f1bd61d613f047df7f44(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ee616b8911dd7e88d86231ed6bdf9ea6c1a27ab6faea37c2d61912c0517c62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c0f7b6b1126f206914df661ef5c9b8c330a6c60a0343e2b7f7af8222d52cd8b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc1168bdca5e04a9ed04e68f3319f8df6c166be2f7a75a45eb85bfebc7a0082(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58eedc4caf4610ed8044e7b058b744bed62a1d50fbbd003c1712dc318ab71e7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27be1f761e63e0566c6967671d00b7905bf0d85479c760d71880f5ea6c00b09d(
    value: typing.Optional[ApiAuthenticationIntegrationWithJwtBearerShowOutput],
) -> None:
    """Type checking stubs"""
    pass
